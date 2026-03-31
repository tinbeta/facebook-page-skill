# Page Posting Guide

## 1) Create a Page post (text only)
```bash
curl -X POST "https://graph.facebook.com/v21.0/{PAGE_ID}/feed" \
  -F "message=Nội dung bài viết" \
  -F "access_token={PAGE_TOKEN}"
```

## 2) Create a photo post
```bash
# Upload từ file local
curl -X POST "https://graph.facebook.com/v21.0/{PAGE_ID}/photos" \
  -F "source=@/path/to/image.jpg" \
  -F "caption=Caption cho ảnh" \
  -F "access_token={PAGE_TOKEN}"

# Hoặc từ URL
curl -X POST "https://graph.facebook.com/v21.0/{PAGE_ID}/photos" \
  -F "url=https://example.com/image.jpg" \
  -F "caption=Caption cho ảnh" \
  -F "access_token={PAGE_TOKEN}"
```

## 3) Lên lịch đăng ảnh
```bash
curl -X POST "https://graph.facebook.com/v21.0/{PAGE_ID}/photos" \
  -F "source=@/path/to/image.jpg" \
  -F "caption=Caption cho ảnh" \
  -F "published=false" \
  -F "scheduled_publish_time={UNIX_TIMESTAMP}" \
  -F "access_token={PAGE_TOKEN}"
```
⚠️ `scheduled_publish_time` phải là Unix timestamp (UTC), ít nhất 10 phút sau hiện tại, tối đa 6 tháng.

## 4) Xem bài đã lên lịch
```bash
curl -s "https://graph.facebook.com/v21.0/{PAGE_ID}/scheduled_posts?\
fields=id,message,scheduled_publish_time,is_published&\
access_token={PAGE_TOKEN}"
```

## 5) Create a video post
- **Domain khác:** `https://graph-video.facebook.com` (không phải `graph.facebook.com`)
```bash
curl -X POST "https://graph-video.facebook.com/v21.0/{PAGE_ID}/videos" \
  -F "source=@/path/to/video.mp4" \
  -F "description=Mô tả video" \
  -F "title=Tiêu đề" \
  -F "access_token={PAGE_TOKEN}"
```
Hoặc dùng script:
```bash
python3 scripts/post_video.py path/to/video.mp4 --page-id "PAGE_ID" --token "PAGE_TOKEN"
```

## 6) Read posts
```bash
curl -s "https://graph.facebook.com/v21.0/{PAGE_ID}/posts?\
fields=id,message,created_time,permalink_url&limit=5&\
access_token={PAGE_TOKEN}"
```

## 7) Update or delete
```bash
# Update
curl -X POST "https://graph.facebook.com/v21.0/{POST_ID}" \
  -F "message=Nội dung mới" \
  -F "access_token={PAGE_TOKEN}"

# Delete
curl -X DELETE "https://graph.facebook.com/v21.0/{POST_ID}?access_token={PAGE_TOKEN}"
```

## Best practices
- **Không ghi giá** trong bài đăng hay comment
- **Không để link trong caption** — Facebook giảm reach. Comment link riêng
- **Video upload** dùng simple method (script `post_video.py`) — tránh Resumable Upload (có bug truncation)
- Caption viết tự nhiên, ngôn ngữ đời thường
