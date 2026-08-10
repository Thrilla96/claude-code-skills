#!/usr/bin/env python3
"""log_decision.py — atomic, self-verifying append to a JARVIS decision lane.
decision_id is a PER-LANE sequence; each lane in ALLOWED_LANES counts from 1
independently. ALLOWED_LANES (below) is the authoritative list — keep this
docstring and SKILL.md in step with it, not the other way round."""
import argparse, json, sys, shutil, datetime, pathlib, os, subprocess, tempfile

# ---------------------------------------------------------------------------
# LANE RELOCK — Layer 1 (writer-only enforcement).
# Decision lanes are mode 400 so no raw open()/echo/tee can write them. The
# atomic swap this writer performs (os.replace) succeeds against a 400 file
# because rename needs DIRECTORY write permission, not file write permission —
# but it replaces the inode, so the lane inherits the temp file's mode and the
# protection would silently lapse after one legitimate append (a D139-class
# silent degradation). Re-locking at interpreter exit closes that, on both the
# success and the failure path.
# Strictly additive: this does not touch the D138 pre-write gate ordering, the
# snapshot series, or the D139 validator-absent WARN.
import atexit as _atexit, os as _os, glob as _glob, sys as _sys

def _relock_decision_lanes():
    for _p in _glob.glob(_os.path.expanduser(
            "~/jarvis-vault/05-Decisions/*/decisions.jsonl")):
        try:
            if (_os.stat(_p).st_mode & 0o777) != 0o400:
                _os.chmod(_p, 0o400)
        except OSError as _e:
            print("WARN: could not re-lock %s to 400: %s" % (_p, _e),
                  file=_sys.stderr)
    # shutil.copy2 copies permission bits, so a snapshot taken FROM a locked
    # lane is itself created at 400 — and any later write to that same snapshot
    # name then dies with PermissionError, which would break the snapshot
    # series. Keep the archive at 600, which is what it has always been.
    for _d in _glob.glob(_os.path.expanduser("~/jarvis-vault/05-Decisions/*/")):
        for _s in (_glob.glob(_d + "decisions.jsonl.*") +
                   _glob.glob(_d + ".backups/decisions.jsonl.*")):
            try:
                if (_os.stat(_s).st_mode & 0o777) == 0o400:
                    _os.chmod(_s, 0o600)
            except OSError:
                pass

_atexit.register(_relock_decision_lanes)
# --------------------------------------------------------------------------

VALIDATOR = os.path.expanduser("~/JARVIS/guard/validate_lane.py")   # canonical pre-write gate

ALLOWED_LANES = {"jarvis", "buffalo-strive", "HPV"}
REQUIRED = ["source", "axis_affected", "summary"]
EXPECTED = ["rationale","alternatives_considered","expected_outcome","revisit_trigger","phase","linked_wrap"]
VALID_AXES = {"data_access","operational_scope","judgment_depth","compounding","infra"}
VALID_SOURCE = {"claude-chat","claude-code","joint","jarvis-agent"}

def lane_ids(path):
    """Every decision_id present in the lane. max+1 is the next id; membership backs
    the supersedes existence check (D128 read-side expects forward-only references)."""
    ids=set()
    if path.exists():
        for ln in path.read_text().splitlines():
            s=ln.strip()
            if not s or s.startswith("#"): continue
            try:
                i=json.loads(s).get("decision_id")
                if isinstance(i,int) and not isinstance(i,bool): ids.add(i)
            except json.JSONDecodeError: pass
    return ids

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--entry-file", required=True)
    ap.add_argument("--decisions-root", default=str(pathlib.Path.home()/"jarvis-vault"/"05-Decisions"))
    ap.add_argument("--dry-run", action="store_true")
    a=ap.parse_args()
    if a.project not in ALLOWED_LANES:
        sys.exit(f"FATAL: --project '{a.project}' is not a decision lane. Allowed: {sorted(ALLOWED_LANES)}")
    root=pathlib.Path(a.decisions_root).expanduser()
    target=root/a.project/"decisions.jsonl"
    if not target.exists():
        sys.exit(f"FATAL: target lane file does not exist: {target}")
    entry=json.loads(pathlib.Path(a.entry_file).read_text())
    lane=lane_ids(target)
    # --- Change 1: trailing-newline refusal (fail closed BEFORE snapshot or write) ---
    raw=target.read_text(encoding="utf-8")   # target existence already checked above
    if raw and not raw.endswith("\n"):
        sys.exit("FATAL: lane does not end in a newline — refusing to append "
                 "(previous write may be truncated; fix the lane before logging)")
    next_id=(max(lane) if lane else 0)+1
    if "decision_id" in entry and entry["decision_id"]!=next_id:
        sys.exit(f"FATAL: entry decision_id {entry['decision_id']} != computed lane-next {next_id}")
    entry["decision_id"]=next_id
    today=datetime.date.today().isoformat()
    if entry.get("date") and entry["date"]!=today:
        print(f"WARN: entry date {entry['date']} != system {today}; using system", file=sys.stderr)
    entry["date"]=today
    miss=[k for k in REQUIRED if k not in entry]
    if miss: sys.exit(f"FATAL: missing required field(s): {miss}")
    if not isinstance(entry["axis_affected"],list) or not entry["axis_affected"]:
        sys.exit("FATAL: axis_affected must be a non-empty list")
    bad=set(entry["axis_affected"])-VALID_AXES
    if bad: sys.exit(f"FATAL: unknown axis value(s): {sorted(bad)}")
    if "supersedes" in entry:
        sup=entry["supersedes"]
        if not isinstance(sup,list) or not sup:
            sys.exit("FATAL: supersedes must be a non-empty list of decision_id ints")
        nonint=[x for x in sup if isinstance(x,bool) or not isinstance(x,int)]
        if nonint: sys.exit(f"FATAL: supersedes must contain ints only; offending: {nonint}")
        dupes=sorted({x for x in sup if sup.count(x)>1})
        if dupes: sys.exit(f"FATAL: supersedes has duplicate id(s): {dupes}")
        fwd=sorted(x for x in sup if x>=next_id)
        if fwd: sys.exit(f"FATAL: supersedes must be backward-only (ids < {next_id}); offending: {fwd}")
        missing=sorted(x for x in sup if x not in lane)
        if missing: sys.exit(f"FATAL: supersedes references id(s) absent from the {a.project} lane: {missing}")
    if entry["source"] not in VALID_SOURCE:
        print(f"WARN: unusual source '{entry['source']}' (known: {sorted(VALID_SOURCE)})", file=sys.stderr)
    warn=[k for k in EXPECTED if k not in entry]
    if warn: print(f"WARN: missing expected field(s): {warn}", file=sys.stderr)
    line=json.dumps(entry, ensure_ascii=False)
    if "\n" in line: sys.exit("FATAL: serialized entry contains newline")
    # --- Change 3: single-decision_id assertion (D120 invariant, pre-write) ---
    if line.count('"decision_id"') != 1:
        sys.exit('FATAL: serialized entry contains "decision_id" %d× (expected 1) — aborting'
                 % line.count('"decision_id"'))
    print(f"writing D{next_id} -> {a.project} lane ({target})")
    if a.dry_run:
        print("DRY-RUN: no write. Candidate line:"); print(line); return
    # --- Change 2: pre-promote validate_lane.py gate (build candidate -> validate -> promote) ---
    # raw ends in "\n" (or is empty) per Change 1, so this appends cleanly.
    candidate=raw+line+"\n"
    fd, tmp=tempfile.mkstemp(prefix="cand_", dir=str(target.parent))  # non-dot prefix; same fs as lane
    snap=None
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(candidate)
        if os.path.exists(VALIDATOR):
            r=subprocess.run([sys.executable, VALIDATOR, tmp],
                             capture_output=True, text=True, timeout=30)
            if r.returncode != 0:
                os.unlink(tmp)
                sys.exit("FATAL: candidate failed validate_lane.py — nothing written:\n"+r.stdout+r.stderr)
        else:
            print(f"WARN: pre-promote validator absent at {VALIDATOR} — degraded to "
                  "catch-after-write (POSTGUARD) only; pre-write gate NOT enforced", file=sys.stderr)
        # candidate is clean (or validator absent -> fall through to existing inline+POSTGUARD checks)
        ts=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        # Snapshot filename carries the decision_id being written (unique by construction) in
        # addition to the timestamp, so two appends inside one UTC second can no longer collide
        # onto one filename and silently overwrite a rollback floor (2026-07-30 snapshot-collision fix).
        snap=target.with_name(f"decisions.jsonl.pre_logdecision_D{next_id}_{ts}")
        # Refuse rather than overwrite: if the computed snapshot path already exists, a prior floor
        # would be clobbered. Abort with a non-zero exit and NO append — an append without its own
        # distinct rollback floor must fail, not proceed quietly.
        if snap.exists():
            os.unlink(tmp)
            sys.exit(f"FATAL: snapshot path already exists; refusing to overwrite a rollback floor: {snap}")
        shutil.copy2(target, snap)     # [SNAPSHOT] pre-write rollback floor
        os.replace(tmp, str(target))   # [WRITE] atomic promote
    finally:
        if os.path.exists(tmp):
            try: os.unlink(tmp)
            except OSError: pass
    # --- post-write integrity guard (D120-class aware) ---
    def line_problem(s):
        s=s.strip()
        if s.count('"decision_id"') != 1:
            return "decision_id appears %dx (expected 1) -- D120-class corruption" % s.count('"decision_id"')
        try: json.loads(s)
        except Exception as e: return "parse fail: %s" % e
        return None
    lines_after = target.read_text().splitlines()
    our = lines_after[-1] if lines_after else ""
    p = line_problem(our)
    if p is not None:
        shutil.copy2(snap, target)
        sys.exit(f"FATAL: this append is malformed ({p}); RESTORED from {snap}")
    n=0; pre=[]
    for i,ln in enumerate(lines_after,1):
        s=ln.strip()
        if not s or s.startswith("#"): continue
        pr=line_problem(s)
        if pr is None: n+=1
        else: pre.append("line %d: %s" % (i,pr))
    if pre:
        print("!!! WARNING: lane has corruption NOT from this append -- entry KEPT; lane needs repair:", file=sys.stderr)
        for x in pre: print("    "+x, file=sys.stderr)
        print(f"OK-WITH-WARNING: appended D{next_id} to {a.project}. entries={n}. snapshot={snap}. RUN validate_lane.py AND REPAIR.")
        sys.exit(3)
    print(f"OK: appended D{next_id} to {a.project}. entries={n}. snapshot={snap}. parse+guard OK.")

if __name__=="__main__": main()
