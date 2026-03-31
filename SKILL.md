---
name: facebook
description: Quản lý Facebook Pages qua Graph API — đăng bài, ảnh, video, Reels, lên lịch, comment, moderation. Hỗ trợ nhiều page từ .env config.
---

# Facebook Page Management Skill

## Purpose
Quản lý Facebook Pages: đăng bài (text/ảnh/video/Reels), lên lịch, comment, moderation — tất cả qua Graph API.

## Best fit
- Đăng bài kèm ảnh/video lên Facebook Page
- Lên lịch đăng bài tự động
- Comment link sản phẩm (affiliate/tiếp thị liên kết)
- Quản lý comment (reply, hide, delete)
- Đăng Reels (video ngắn dọc)

## Not a fit
- Facebook Ads / Marketing API
- Facebook Shop / Commerce Manager
- Branded Content / Liên kết tiếp thị (chỉ quản lý trên web)
- Đọc bài từ page khác (Facebook hạn chế)

## Setup

### 1. Tạo Facebook App
1. Vào [Facebook Developers](https://developers.facebook.com/) → **Create App**
2. Chọn loại app phù hợp → tạo xong ghi lại **App ID** và **App Secret**

### 2. Lấy Page Access Token (never-expire)

**Bước 1:** Lấy Short-lived User Token từ [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- Chọn app của bạn
- Chọn permissions: `pages_manage_posts`, `pages_read_engagement`, `pages_manage_engagement`, `pages_show_list`
- Click **Generate Access Token**

**Bước 2:** Đổi sang Long-lived User Token (60 ngày):
```bash
curl -s "https://graph.facebook.com/v21.0/oauth/access_token?\
grant_type=fb_exchange_token&\
client_id={APP_ID}&\
client_secret={APP_SECRET}&\
fb_exchange_token={SHORT_LIVED_USER_TOKEN}"
```

**Bước 3:** Lấy Page Token vĩnh viễn từ Long-lived User Token:
```bash
curl -s "https://graph.facebook.com/v21.0/{PAGE_ID}?fields=access_token&access_token={LONG_LIVED_USER_TOKEN}"
```
→ Page Token trả về sẽ **không bao giờ hết hạn** (`expires_at: 0`)

**Verify token:**
```bash
curl -s "https://graph.facebook.com/v21.0/debug_token?\
input_token={PAGE_TOKEN}&\
access_token={APP_ID}|{APP_SECRET}"
```
→ Kiểm tra `expires_at: 0` = never expire ✅

### 3. Config trong .env

Mỗi page cần một block trong `.env`:
```
APP: TenApp
App ID: 123456789
App Secret: abc123def456

Facebook page: Ten Page
Page_ID=123456789
page_access_token=EAAL...xyz
```

Có thể config nhiều page, mỗi page một block riêng.

## Quick reference

### Đăng bài text
```bash
curl -X POST "https://graph.facebook.com/v21.0/{PAGE_ID}/feed" \
  -F "message=Nội dung bài viết" \
  -F "access_token={PAGE_TOKEN}"
```

### Đăng bài kèm ảnh (upload trực tiếp)
```bash
curl -X POST "https://graph.facebook.com/v21.0/{PAGE_ID}/photos" \
  -F "source=@/path/to/image.jpg" \
  -F "caption=Caption cho ảnh" \
  -F "access_token={PAGE_TOKEN}"
```

### Lên lịch đăng ảnh
```bash
# scheduled_publish_time = Unix timestamp (UTC)
curl -X POST "https://graph.facebook.com/v21.0/{PAGE_ID}/photos" \
  -F "source=@/path/to/image.jpg" \
  -F "caption=Caption cho ảnh" \
  -F "published=false" \
  -F "scheduled_publish_time={UNIX_TIMESTAMP}" \
  -F "access_token={PAGE_TOKEN}"
```

### Xem bài đã lên lịch
```bash
curl -s "https://graph.facebook.com/v21.0/{PAGE_ID}/scheduled_posts?\
fields=id,message,scheduled_publish_time,is_published&\
access_token={PAGE_TOKEN}"
```

### Comment vào bài
```bash
curl -X POST "https://graph.facebook.com/v21.0/{POST_ID}/comments" \
  -F "message=Nội dung comment" \
  -F "access_token={PAGE_TOKEN}"
```

### Xoá bài
```bash
curl -X DELETE "https://graph.facebook.com/v21.0/{POST_ID}?access_token={PAGE_TOKEN}"
```

### Đăng video
```bash
curl -X POST "https://graph-video.facebook.com/v21.0/{PAGE_ID}/videos" \
  -F "source=@/path/to/video.mp4" \
  -F "description=Mô tả video" \
  -F "access_token={PAGE_TOKEN}"
```
Hoặc dùng script: `python3 scripts/post_video.py video.mp4 --page-id "PAGE_ID" --token "PAGE_TOKEN"`

### Đăng Reels
Xem chi tiết: `references/reels-publishing.md` (3 bước: init → upload → publish)

## Detailed references
- `references/graph-api-overview.md` — Base URLs, versioning, request patterns
- `references/page-posting.md` — Page posting workflows
- `references/reels-publishing.md` — Reels publishing (3-90s vertical video)
- `references/comments-moderation.md` — Comment actions & moderation
- `references/permissions-and-tokens.md` — Token types & permissions
- `references/http-request-templates.md` — HTTP request examples

## Best practices (từ kinh nghiệm thực tế)

### Content
- **Không ghi giá** trong bài đăng hay comment — để người xem inbox hỏi hoặc tự xem trên link
- **Không đặt link trong caption** — Facebook giảm reach bài có link. Thay vào đó kêu gọi xem link ở comment, rồi comment link riêng
- **Caption tự nhiên** — viết như người thật, không quá "quảng cáo", dùng ngôn ngữ đời thường

### Technical
- Dùng **never-expire Page Token** (xem Setup phía trên)
- Luôn dùng versioned URL (`v21.0`)
- Video upload dùng domain `graph-video.facebook.com` (khác với domain thường)
- Reels upload Step 2 dùng `rupload.facebook.com`
- Rate limit: 30 Reels / 24h / Page

## Security
- Không log token hay App Secret
- Lưu token trong `.env`, không commit lên git
- Dùng least-privilege permissions
