---
name: log-decision
description: Append an entry to a JARVIS decision lane the ONE safe way. Use whenever Bill approves logging a §-axis decision crossing or any decision must be written to ~/jarvis-vault/05-Decisions/<lane>/decisions.jsonl. decision_id is PER-LANE (jarvis, buffalo-strive, and HPV each count from 1). Computes the lane's next id, injects the system date, validates v2.1 schema, snapshots, appends atomically, reparses, and restores on failure. Never hand-append with a heredoc or cat >>.
---

# log-decision

Atomic writer for a JARVIS decision lane. Replaces hand-rolled `cat >> decisions.jsonl` appends (heredoc-corruption class) and manual id math (wrong-id class). **decision_id is a per-lane sequence** — `jarvis`, `buffalo-strive`, and `HPV` each maintain their own 1..N; they do NOT share a global counter.

## When to use
- Bill approved logging a decision (§axis crossing, architectural call, infra change), or any write to a lane's `decisions.jsonl`.

## How to use
1. Draft the entry as JSON **without** `decision_id` or `date` (helper injects both — id = target lane max+1, date = system date). Min fields: `source`, `axis_affected` (list), `summary`. Include `rationale`, `alternatives_considered`, `expected_outcome`, `revisit_trigger`, `phase`, `linked_wrap` to match established entries.
2. Write to a temp file, e.g. `/tmp/decision.json`.
3. Dry-run: `python3 ~/.claude/skills/log-decision/log_decision.py --project jarvis --entry-file /tmp/decision.json --dry-run`
4. If correct, commit (drop `--dry-run`).

## Rules
- `--project` is exactly `jarvis`, `buffalo-strive`, or `HPV` — these are `ALLOWED_LANES` in `log_decision.py`. Hard-fails on anything else (health-os, pending, spec-* are NOT lanes). **`ALLOWED_LANES` in the source is authoritative**; if this line ever disagrees with it, the source wins and this line is the bug. (It was: this doc omitted `HPV` while the helper accepted it, so a 2026-08-10 session had to read the source to log D23.)
- Never pass `decision_id`.
- Axes: data_access, operational_scope, judgment_depth, compounding, infra. Source: claude-chat, claude-code, joint, jarvis-agent.
- On reparse failure the helper auto-restores the snapshot and exits non-zero.

## Superseding a prior decision (D129)
- To correct/replace earlier entries, add `"supersedes": [<id>, ...]` to the new entry (a non-empty list of distinct ints). The lane is append-only — you never edit or delete the old entry; the new one marks it SUPERSEDED.
- The writer enforces: backward-only (every id `< next_id`) and must-exist (each id present in the *same* lane). Forward, duplicate, non-int, or absent ids hard-fail with the lane untouched.
- `check_decisions.py` reads the result: a superseded entry shows `[SUPERSEDED by D<n>]`, all others `[ACTIVE]`.

## How the write is guarded (why this is the ONE safe path)
Every commit is fail-closed on both sides of the write:
- **Pre-write gate (D138):** the candidate line is built into a temp file in the lane dir, the real `~/JARVIS/guard/validate_lane.py` runs against the *whole* candidate, and the lane is promoted (atomic `os.replace`) only on validator exit 0 — so a non-monotonic / duplicate / malformed candidate never touches the live lane. If the validator is absent it WARNs and falls back to the post-write guard (degradation is visible, not silent).
- **Trailing-newline refusal:** a truncated lane (missing final `\n`) is refused before any write (kills the D120 two-ids-on-one-line class at the source).
- **Post-write guard (D120/D125):** after `os.replace`, the appended line is reparsed and the single-`decision_id` invariant re-checked; our own malformed line restores from the snapshot, pre-existing corruption elsewhere is kept + warned (exit 3) rather than silently dropping the good entry.
- Snapshots land beside the lane as `decisions.jsonl.pre_logdecision_<UTC-ts>`.
