# Frontend Health Checker - Index

## 📋 Quick Links

| Section | Description |
|---------|-------------|
| [SKILL.md](SKILL.md) | Tài liệu chi tiết về Frontend Health Checker |
| [README.md](README.md) | Hướng dẫn sử dụng nhanh |
| [examples.js](examples.js) | Ví dụ scripts thực tế |

## 🎯 Tính năng chính

- ✅ Phát hiện **console errors** và **warnings**
- ✅ Phát hiện **network failures** (4xx, 5xx)
- ✅ Kiểm tra **broken links**
- ✅ Hỗ trợ **authentication flow**
- ✅ **Screenshot** khi có lỗi
- ✅ **Báo cáo chi tiết** per-page

## 🚀 Usage nhanh

```bash
# Cài đặt dependencies
cd frontend && npm install puppeteer

# Chạy health check
BASE_URL=http://localhost:3000 node _health_check.js
```

## 📊 Pages được check

### Public Pages
- `/` - Home
- `/login` - Login
- `/register` - Register
- `/blog` - Blog

### Protected Pages (cần auth)
- `/dashboard` - Dashboard
- `/dashboard/stats` - Statistics
- `/dashboard/posts` - Posts Manager
- `/dashboard/users-manager` - Users Manager
- `/dashboard/settings` - Settings
- `/user/profile` - User Profile

## 🔧 Related Skills

- [ui-ux-pro-max](../ui-ux-pro-max/) - Thiết kế UI/UX
- [backend-api-builder](../backend-api-builder/) - Xây dựng API backend
- [backend-api-tester](../backend-api-tester/) - Test API backend
