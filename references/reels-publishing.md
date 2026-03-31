# Reels Publishing API

## Overview

Publish short-form video reels (3-90 seconds) directly to Facebook Pages using the Video API.

## Key Limitations

- Only publish to Facebook Pages (not individual profiles)
- Rate limit: 30 API-published reels per 24-hour period per Page
- Reels on Pages (when published as Stories) max 60 seconds
- Full reels can be up to 90 seconds

## Video Specifications

| Property | Specification |
|----------|---|
| File Type | .mp4 (recommended) |
| Aspect Ratio | 9 x 16 (vertical) |
| Resolution | 1080 x 1920 pixels (min: 540 x 960) |
| Frame Rate | 24-60 fps |
| Duration | 3-90 seconds |
| Compression | H.264, H.265, VP9, AV1 |
| Closed GOP | 2-5 seconds |
| Frame Type | Progressive scan (not interlaced) |
| Chroma | 4:2:0 subsampling |

## Audio Specifications

- Bitrate: 128 kbps or higher
- Channels: Stereo
- Codec: AAC Low Complexity
- Sample rate: 48 kHz

## Required Permissions

User must grant these Facebook Login permissions:
- `pages_show_list` — List Pages
- `pages_read_engagement` — Read Page engagement
- `pages_manage_posts` — Publish posts on Page

## Step 1: Initialize Upload Session

**Endpoint:** `POST /v25.0/{page-id}/video_reels`

**Host:** `graph.facebook.com`

**Parameters:**
- `upload_phase=start`
- `access_token={page_access_token}`

**Example:**
```bash
curl -X POST "https://graph.facebook.com/v25.0/{page_id}/video_reels" \
  -H "Content-Type: application/json" \
  -d '{
    "upload_phase": "start",
    "access_token": "{page_access_token}"
  }'
```

**Response:**
```json
{
  "video_id": "...",
  "upload_url": "https://rupload.facebook.com/video-upload/{video-id}"
}
```

## Step 2: Upload Video File

**Endpoint:** `POST /video-upload/{video-id}`

**Host:** `rupload.facebook.com` (NOT graph.facebook.com)

**Headers:**
- `Authorization: OAuth {page_access_token}`
- `offset: 0` (or byte offset for chunked uploads)
- `file_size: {bytes}` (total file size in bytes)

**Content-Type:** `application/octet-stream`

**Example:**
```bash
curl -X POST "https://rupload.facebook.com/video-upload/{video-id}" \
  -H "Authorization: OAuth {page_access_token}" \
  -H "offset: 0" \
  -H "file_size: {file_size_bytes}" \
  --data-binary "@my_video.mp4"
```

## Step 3: Publish Reel

**Endpoint:** `POST /v25.0/{page-id}/video_reels`

**Host:** `graph.facebook.com`

**Parameters:**
- `upload_phase=finish`
- `access_token={page_access_token}`
- `video_id={video_id_from_step_1}`
- `description` (optional) — reel caption
- `privacy` (optional) — public/private

**Example:**
```bash
curl -X POST "https://graph.facebook.com/v25.0/{page_id}/video_reels" \
  -H "Content-Type: application/json" \
  -d '{
    "upload_phase": "finish",
    "video_id": "{video_id}",
    "description": "Check out this reel!",
    "access_token": "{page_access_token}"
  }'
```

**Response:**
```json
{
  "id": "{reel_id}",
  "success": true
}
```

## Sharing & Privacy

- App users should be presented with audience/privacy controls
- Pages default to "Public" visibility
- Disclose how reels are used on Facebook

## Common Issues

1. **Wrong host for upload** — Step 2 MUST use `rupload.facebook.com`, not `graph.facebook.com`
2. **Missing permissions** — Ensure `pages_manage_posts` scope is granted
3. **Rate limit exceeded** — Implement client-side rate limiting (30 per 24h)
4. **Invalid video specs** — Check aspect ratio (9:16), codec (H.264), audio (AAC)

## Official Docs

https://developers.facebook.com/docs/video-api/guides/reels-publishing
