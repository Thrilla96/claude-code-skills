# Model selection & params

Always confirm against the live catalog (`models_explore action:get model_id:<id>`) — this is a
snapshot, not gospel. Names and params change.

## Images

| Goal | Model | Notes |
|---|---|---|
| Trained reusable identity | `soul_2` (Soul V2) | Pass `soul_id`. One person per gen. `quality` 1.5k/2k. Aspect incl. 16:9. |
| Multi-character / two-fighter keyframe | `nano_banana_2` (Nano Banana Pro) | Embed `<<<element_id>>>` placeholders in `prompt`. May route/report as `nano_banana_flash`; that's fine. ~1.5 cr. |
| One-off character ref, no training | `soul_2` (no soul_id) or `nano_banana_pro` | Good for a villain you won't retrain. |
| 4K / text / diagram | `nano_banana_pro` | |

Soul V2 generations are often heavily discounted/free under plan promos — preflight to see the
real number (frequently ~0.12 cr), don't assume.

## Video (image-to-video)

| Goal | Model | Notes |
|---|---|---|
| Identity-preserving image→video (default) | `seedance_2_0` | `start_image` role, 4–15s, 480/720/1080p, `mode` std/fast, `genre` (action/epic/noir/…). ~45 cr for 5s/1080p/std. Generates audio. |
| Multi-shot / audio-sync / motion-transfer | `kling3_0` | start_image+end_image; `mode` std/pro/4k; `sound` on/off. |
| Real choreography transfer | `motion_control` (Kling 3.0 MC) | `image_id` + `motion_video_id`; `scene_control:'image'` keeps the character's background, `'video'` uses the driving clip's. **No `get_cost`.** Puppeteers one body. ~9 cr/4s @720p. |

Preset interrupt: a `generate_video` call may return a `preset_recommendation` notice instead of
a cost/job. For identity work, decline it — resubmit with `declined_preset_id:<that id>` — so you
get the literal generation, not a canned look that won't hold the character.

## Choreography control tiers (cheap → controlled)

1. **Text-prompted action** — Seedance `genre:action`, one start frame. Model improvises motion.
2. **Keyframe interpolation** — `start_image` + `end_image`; model fills the motion between two
   intentional poses. Best control-per-credit for clean hits.
3. **Motion transfer** — `motion_control` with a real driving clip. Most realistic, needs source
   footage, single body only.

## Useful extras

- `upscale_video` (bytedance/topaz) — final 4K. No get_cost. Pass source w/h for bytedance.
- `outpaint_image` / `reframe` — change canvas/aspect of stills/videos. Have get_cost.
- `remove_background`, `upscale_image` (has get_cost).
