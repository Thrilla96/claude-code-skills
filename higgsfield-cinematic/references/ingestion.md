# Media ingestion playbook

Generation tools need a confirmed Higgsfield `media_id` (or a completed generation `job_id`) in
`medias[].value`. Never pass a raw local path or external URL there. Here is how to get media in,
fastest path first.

## 1. Local file already on this machine

```
media_upload(filename, content_type)         # returns presigned upload_url + media_id
curl -X PUT -H "Content-Type: <mime>" --data-binary @file "<upload_url>"   # expect HTTP 200
media_confirm(type:'image'|'video'|'audio', media_id)   # or media_ids:[...] for a batch
```

The signed url encodes the content-type — send the matching `Content-Type` header or the PUT
fails. For Soul training the validator wants the **resolved cloudfront URL** (from the upload
response's `url`), not the bare media_id — pass those https URLs in `show_characters`' `medias`.

## 2. Public web media URL

`media_import_url(url, type)` imports it into Higgsfield storage and returns a `media_id`. Use
that id downstream. Max payload ~50 MB.

## 3. The user's own footage that lives behind a login (e.g. their own NLL game clip)

**Scope this narrowly — it is NOT a general "pull any video off the web" pattern.** Use this path
only for footage the **user owns or has clear rights to** (their own game film, their own phone
recording, their own uploads) that happens to be gated behind a login. The mechanism is always
**route it through the user's own storage** — the user puts the file in *their* Google Drive (or
hands you a local path) and you fetch from *that*. Do not scrape third-party or copyrighted video,
do not bypass paywalls/DRM, and do not treat a public URL as fair game just because it's reachable.
If ownership/rights are unclear, stop and ask the user before fetching anything.

With that boundary set: **browser-cookie extraction for yt-dlp does not work on a modern Mac:**

- **Chrome** (v127+) uses **App-Bound Encryption**; yt-dlp cannot decrypt the cookie DB and
  `--cookies-from-browser chrome` hangs.
- **Safari** cookies live in a TCC-protected container; reads fail with `Operation not permitted`
  **even after granting Full Disk Access** — because the executing binary is a nested
  `~/Library/Application Support/Claude/claude-code/<ver>/claude.app`, not the `/Applications/
  Claude.app` the user granted, so the grant doesn't attribute.
- yt-dlp age-gate bypass via alternate `player_client`s (tv_embedded, android, ios, …) is patched.

**Do not burn time on cookies.** The reliable, low-friction path is **Google Drive**:

1. User uploads the clip to Google Drive from any device (phone Photos → Share → Drive is easiest).
2. User sets it to **"Anyone with the link"** (Manage access → General access → Anyone with link).
3. Get the file id from the link and pull bytes straight to disk:
   ```
   curl -sSL "https://drive.google.com/uc?export=download&id=FILEID" -o clip.mov
   ```
   Verify it's real video, not an HTML login page: `file clip.mov` should say "ISO Media", and
   `head -c 16 clip.mov | xxd` should show an `ftyp` box. If you got HTML, the link is still
   private — sharing isn't set. (Works for files under ~100 MB; bigger ones hit Drive's
   virus-scan interstitial.)
4. If a Google Drive MCP is connected, you can instead locate the file with `search_files` and
   read metadata with `get_file_metadata`; `download_file_content` returns base64 (fine for small
   files, but a 40 MB video is too big to route through the tool result — prefer the curl above).

User can revoke link-sharing as soon as you confirm the bytes landed.

## 4. Trim before uploading a motion clip

A driving clip for `motion_control` should be a few seconds of clean, single-subject motion with
**no camera cut** (a cut mid-clip breaks motion transfer). Inspect and trim with ffmpeg:

```
ffprobe -v error -show_entries format=duration -of csv=p=0 raw.mov   # length
ffmpeg -ss <start> -i raw.mov -t <dur> -an -c:v libx264 -pix_fmt yuv420p -crf 18 clip.mp4
```

Sample frames (`ffmpeg -ss T -i raw.mov -frames:v 1 f.jpg`) and build a contact sheet
(`-vf tile=5x2`) to pick the cleanest segment before committing. Then upload via path #1.
