---
name: higgsfield-cinematic
description: >-
  End-to-end workflow for the Higgsfield MCP — train consistent characters (Soul / Elements),
  generate cinematic stills and image-to-video shots, transfer real motion onto a character,
  and assemble multi-shot fight/action sequences with ffmpeg. Use this skill whenever the user
  is doing AI character or short-film work with Higgsfield: creating a reusable character or
  "digital twin", hero stills, image-to-video, motion transfer / puppeteering, multi-character
  fight or action scenes, or stitching several generated shots into one graded cut — even if
  they don't say "Higgsfield" by name but are clearly driving the Higgsfield tools. It also
  encodes the credit/workspace gate, the cost-preflight discipline, and the media-ingestion
  workarounds (Google Drive, blocked browser cookies) that are easy to get wrong.
---

# Higgsfield cinematic pipeline

This skill captures a battle-tested workflow for producing consistent characters and multi-shot
cinematic sequences with the Higgsfield MCP. The tools are powerful but have sharp edges around
credits, identity consistency, and getting source media onto the machine. Follow the discipline
below and you avoid the traps that cost the most time and credits.

## Three golden rules (do these first, every session)

1. **Bind to the live catalog before calling anything.** Tool names and params drift. Confirm
   the exact tool name, required params, and allowed enum values from the live tool list before
   you invoke — don't trust memory or this doc's examples verbatim. (This is how you catch things
   like `nano_banana_2` vs `nano_banana_flash`, the `soul_id` param shape, or a model's real
   `aspect_ratios`.) Use `mcp__higgsfield__models_explore` (`action:get`/`recommend`) to inspect
   a model's parameters and supported ratios before building a call.

2. **Gate on workspace + balance.** Call `list_workspaces`; if the target workspace shows
   `is_selected: false`, call `select_workspace` with its id **before** anything else. An
   unselected workspace makes `balance` falsely report `8 credits / free` even on a funded Plus/
   Ultra plan — that "out of credits" panic is almost always just a missing workspace selection.
   The selection persists across sessions, but re-verify.

3. **Cost-preflight everything that spends.** Image/video/3d/audio generators accept
   `get_cost: true` in `params` — call it, **report the credit quote to the user, then submit the
   real job.** Capture `balance` before and after to confirm the actual charge.
   **Exception:** `motion_control`, `upscale_video`, and a few others have **no `get_cost`** — say
   so, give a rough estimate from prior runs, and report the measured delta afterward.

4. **Approval gate on video spend — get an explicit go-ahead per shot.** Video generation
   (`seedance_2_0`, `kling3_0`, etc.) costs real money — roughly **45 credits per 5s/1080p shot**,
   and a multi-shot sequence adds up fast. **Never auto-cascade from a still into a video, and
   never batch-fire multiple video shots, without Bill explicitly approving that spend.** The
   correct rhythm is: build/verify the keyframe still (cheap) → preflight the video cost → state
   the quote → **wait for Bill's go-ahead** → generate that one shot. Stills, keyframes, Elements,
   and local ffmpeg work are cheap/free and don't need this gate; the gate is specifically about
   the per-shot video burn. When in doubt, stop and ask rather than spend.

## Characters: Soul vs Elements

Consistency is the whole game. There are two mechanisms and they are NOT interchangeable:

- **Soul** (`show_characters action:'train'`, type `soul_2`) — a trained identity model from
  5–20 reference photos (~10 min). Highest-fidelity likeness. **One person per generation.** Use
  it for solo hero shots. Generate with `generate_image model:'soul_2'` + the returned `soul_id`.
- **Elements** (`show_reference_elements action:'create'`) — instant reusable reference from a
  single image. Embed `<<<element_id>>>` placeholders inside the `prompt` of a multi-subject
  model (`nano_banana_2` / Nano Banana Pro). **This is the only way to put two characters in one
  frame** (warrior + villain), because a Soul can't. Cheap (~1.5 credits/keyframe).

Rule of thumb: **solo, identity-critical → Soul; any two-or-more-character shot → Elements +
Nano Banana keyframe.** For a fight scene you typically train one Soul for the hero, save both
hero and villain as Elements, and build two-fighter keyframes with Elements.

Poll training with `show_characters action:'status'` + `soul_id` until `status:'ready'`.

## Getting source media onto the machine

Generation inputs must be confirmed Higgsfield `media_id`s or completed job ids — never raw
paths or URLs in `medias[].value`. See `references/ingestion.md` for the full playbook,
including the **age-restricted-YouTube / blocked-cookie workaround** (the single biggest
time-sink). Short version:

- **Local file you can reach:** `media_upload` → PUT bytes to the presigned url → `media_confirm`.
- **Public web URL:** `media_import_url`, then use the returned `media_id`.
- **YouTube / anything needing login:** browser-cookie extraction is effectively dead on modern
  Macs (Chrome App-Bound Encryption; Safari blocked by TCC even with Full Disk Access). The
  reliable path is **Google Drive**: have the user upload the file, set it to "Anyone with the
  link", then `curl "https://drive.google.com/uc?export=download&id=FILEID"` straight to disk.
  Read `references/ingestion.md` before going down any cookie path.

## The shot pipeline

For each shot: make a **keyframe still**, then **animate** it.

- **Keyframe:** Soul (solo) or Elements+`nano_banana_2` (multi-character). Aspect `16:9` for
  cinematic. Verify the keyframe (download + look at it) before spending on animation.
- **Animate:** `generate_video`. Pick the model from the live catalog via `models_explore
  recommend`. As of writing: `seedance_2_0` is the identity-preserving image-to-video default
  (start_image, 4–15s, 480/720/1080p, genre hints like `action`); `kling3_0` for multi-shot /
  audio-sync / motion transfer. If a preset-recommendation notice interrupts a `generate_video`
  call, decline it for identity work by passing `declined_preset_id` and resubmitting literally.
- **Motion transfer (real choreography):** `motion_control` takes `image_id` (character still) +
  `motion_video_id` (a driving clip) and copies that clip's motion onto the character. Set
  `scene_control:'image'` to keep the character's own background (not the driving clip's). It
  puppeteers ONE body — use solo character motion, not two tangled fighters. No `get_cost`.

See `references/models.md` for model selection, params, and the identity-vs-control tradeoffs.

## Polling jobs

Generations are async. Poll with `job_status` and `sync:true` (server waits up to ~25s and
returns on terminal state). Images ~10–20s, videos ~1–3 min. For long renders, wait in intervals
(a backgrounded `sleep`) and re-poll rather than hammering. `job_status` returns a result URL on
completion.

## Assembling a multi-shot cut

Higgsfield has no concatenation tool — assemble locally with ffmpeg. The shots will vary in
resolution (e.g. a 720p motion-transfer shot among 1080p Seedance shots) and audio presence, so
**normalize before concatenating**. Use the bundled script:

```
scripts/assemble.sh out.mp4 shotA.mp4 shotB.mp4 shotC.mp4 ...
```

It normalizes every input to 1920×1080@30, applies one **unified teal-orange grade** (so shots
from different generations read as one scene), **loudnorm's** the audio (keeping each shot's
generated SFX at an even level), and concats via the demuxer. Read the script header for flags
(e.g. `--no-audio`, custom grade). To play a finished local cut back to the user inline, upload
it (`media_upload`→PUT→`media_confirm`) and share the returned public cloudfront URL — local
paths won't stream and the visualize widget's CSP blocks non-allowlisted video origins.

## Worked reference (this user's project)

A concrete, working instance lives in the user's memory file
`~/.claude/projects/-Users-wdco96/memory/higgsfield-warrior-bill.md`: a trained `warrior_bill`
Soul, a `columbus-villain` Element, and a 4-shot graded fight cut (reveal → beatdown → clash →
drop). Read it for real ids and a known-good end-to-end example before starting related work.

## Typical end-to-end flow

1. `select_workspace` + `balance`.
2. Upload references → `show_characters action:'train'` (Soul) and/or `show_reference_elements`
   (Elements). Poll to ready.
3. Plan a shot list (reveal → action beats → finisher).
4. Per shot: keyframe (`get_cost`, report, generate) → verify → animate (`get_cost`, report,
   generate) → poll.
5. Ingest any real motion clips (see ingestion ref) → `motion_control` for choreographed beats.
6. `scripts/assemble.sh` → upload the cut → share the URL.
7. Offer polish: audio/grade pass, speed-ramp, 4K `upscale_video`, title card.
