# Permissions and Tokens

## 1) Token types

| Token | Lifetime | Use case |
|-------|----------|----------|
| Short-lived User Token | ~1-2 hours | Lấy từ Graph API Explorer, dùng tạm |
| Long-lived User Token | ~60 days | Đổi từ short-lived, dùng để lấy Page Token |
| Page Access Token (from long-lived) | **Never expire** | Dùng cho mọi Page operations |
| App Token (`APP_ID\|APP_SECRET`) | Never expire | Dùng để debug token, không publish được |

## 2) Lấy Never-Expire Page Token (step-by-step)

### Bước 1: Short-lived User Token
- Vào [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- Chọn app → chọn permissions → Generate Access Token
- Permissions cần: `pages_manage_posts`, `pages_read_engagement`, `pages_manage_engagement`, `pages_show_list`

### Bước 2: Đổi sang Long-lived User Token
```bash
curl -s "https://graph.facebook.com/v21.0/oauth/access_token?\
grant_type=fb_exchange_token&\
client_id={APP_ID}&\
client_secret={APP_SECRET}&\
fb_exchange_token={SHORT_LIVED_TOKEN}"
```
→ Response: `{"access_token": "EAAL...", "token_type": "bearer", "expires_in": 5184000}`

### Bước 3: Lấy Page Token vĩnh viễn
```bash
# Lấy token cho 1 page cụ thể
curl -s "https://graph.facebook.com/v21.0/{PAGE_ID}?fields=access_token&access_token={LONG_LIVED_USER_TOKEN}"

# Hoặc list tất cả pages
curl -s "https://graph.facebook.com/v21.0/me/accounts?fields=id,name,access_token&access_token={LONG_LIVED_USER_TOKEN}"
```
→ Page Token trả về sẽ **never expire** (`expires_at: 0`)

### Bước 4: Verify
```bash
curl -s "https://graph.facebook.com/v21.0/debug_token?\
input_token={PAGE_TOKEN}&\
access_token={APP_ID}|{APP_SECRET}"
```
Kiểm tra: `"expires_at": 0` = ✅ never expire

## 3) Common Page permissions

| Permission | Mô tả |
|-----------|-------|
| `pages_manage_posts` | Đăng & sửa bài trên Page |
| `pages_read_engagement` | Đọc nội dung & insights |
| `pages_manage_engagement` | Quản lý comment (reply, hide, delete) |
| `pages_show_list` | List các Pages user quản lý |
| `pages_read_user_content` | Đọc nội dung user đăng lên Page |

## 4) Khi nào token hết hiệu lực?
Never-expire Page Token sẽ bị vô hiệu nếu:
- User đổi mật khẩu Facebook
- User gỡ quyền app
- App bị xoá hoặc bị Facebook disable
- User bị xoá khỏi admin/editor của Page

## 5) Tự động refresh token (nếu cần)
Nếu token bị lỗi `190` (expired/invalid):
1. Cần user tạo lại Short-lived Token từ Graph API Explorer
2. Lặp lại Bước 2-3 ở trên
3. Update `.env` với token mới

Không có cách tự động refresh mà không cần user interaction (do Facebook security policy).
