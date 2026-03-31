# HTTP Request Templates (Graph API)

## Create Page post
POST `/{page-id}/feed`
```json
{
  "message": "Hello from the bot",
  "published": true
}
```

## Schedule Page post
POST `/{page-id}/feed`
```json
{
  "message": "Scheduled post",
  "published": false,
  "scheduled_publish_time": 1735689600
}
```

## Create photo post
POST `/{page-id}/photos`
```json
{
  "url": "https://example.com/image.jpg",
  "caption": "Caption",
  "published": true
}
```

## Create video post
POST `https://graph-video.facebook.com/{page-id}/videos`
```bash
curl -F "source=@/path/to/video.mp4" \
     -F "title=My Video Title" \
     -F "description=My Video Description" \
     -F "access_token=PAGE_ACCESS_TOKEN" \
     "https://graph-video.facebook.com/v20.0/{page-id}/videos"
```

## List posts
GET `/{page-id}/posts?fields=id,message,created_time,permalink_url&limit=5`

## Add comment
POST `/{post-id}/comments`
```json
{
  "message": "Thanks for your feedback!"
}
```

## Hide comment
POST `/{comment-id}`
```json
{
  "is_hidden": true
}
```

## Delete comment
DELETE `/{comment-id}`
