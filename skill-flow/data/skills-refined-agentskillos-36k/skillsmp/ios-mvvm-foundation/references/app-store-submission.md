# App Store Submission

> Checklist và guidelines cho App Store submission.

---

## 🎯 Pre-Submission Checklist

### Technical Requirements

- [ ] Build với Xcode production certificate
- [ ] Archive với Release configuration
- [ ] Test trên device thật (không chỉ simulator)
- [ ] Remove debug code và print statements
- [ ] Verify API endpoints point to production

### App Store Connect

- [ ] App name unique và available
- [ ] Bundle ID matches App Store Connect
- [ ] Version number incremented
- [ ] Build number unique cho mỗi upload

---

## 📱 Required Assets

### App Icons

| Size | Purpose |
|------|---------|
| 1024x1024 | App Store |
| 180x180 | iPhone @3x |
| 120x120 | iPhone @2x |
| 167x167 | iPad Pro |
| 152x152 | iPad @2x |

**Requirements**:
- PNG format
- No alpha channel (no transparency)
- No rounded corners (system adds)
- sRGB color space

### Screenshots

| Device | Size | Required |
|--------|------|----------|
| iPhone 6.9" | 1320x2868 | ✅ Required |
| iPhone 6.7" | 1290x2796 | ✅ Required |
| iPhone 6.5" | 1284x2778 | ✅ Required |
| iPad 12.9" | 2048x2732 | If supports iPad |

**Requirements**:
- PNG hoặc JPEG
- Không có device frame
- Tối đa 10 screenshots/locale
- Tối thiểu 3 screenshots

---

## 📝 Metadata

### Required Fields

```
App Name: 30 characters max
Subtitle: 30 characters max
Description: 4000 characters max
Keywords: 100 characters total (comma-separated)
Support URL: Required
Privacy Policy URL: Required
```

### Description Template

```markdown
[Mô tả ngắn gọn app làm gì - 1-2 câu]

**Tính năng chính:**
• Feature 1
• Feature 2
• Feature 3

**Tại sao chọn [App Name]:**
• Benefit 1
• Benefit 2

**Yêu cầu:**
• iOS 15.0 trở lên
• [Other requirements]

Liên hệ: support@example.com
```

---

## 🔒 Privacy

### Privacy Policy

Required URL trỏ tới privacy policy bao gồm:
- Data thu thập
- Cách sử dụng data
- Third-party sharing
- Data retention
- User rights (GDPR, CCPA)

### App Privacy Details

Khai báo trong App Store Connect:

| Category | Examples |
|----------|----------|
| Contact Info | Email, phone, name |
| Health & Fitness | Health data |
| Financial Info | Payment info |
| Location | Precise, coarse |
| Identifiers | User ID, device ID |
| Usage Data | Product interaction |
| Diagnostics | Crash data, performance |

---

## ⚠️ Common Rejection Reasons

### 1. Guideline 2.1 - Performance

```
❌ App crashes hoặc bugs
❌ Placeholder content
❌ Incomplete features
```

**Fix**: Test thoroughly, remove beta features

### 2. Guideline 2.3 - Accurate Metadata

```
❌ Screenshots không match actual UI
❌ Description sai lệch
❌ Wrong category
```

**Fix**: Update screenshots, accurate description

### 3. Guideline 4.0 - Design

```
❌ Poor UI (buttons quá nhỏ)
❌ Non-standard navigation
❌ Web view wrapper without functionality
```

**Fix**: Follow HIG, native UI patterns

### 4. Guideline 5.1 - Privacy

```
❌ Missing privacy policy
❌ Undeclared data collection
❌ Excessive permissions
```

**Fix**: Complete privacy policy, accurate declarations

### 5. Guideline 3.1 - Payments

```
❌ External payment links
❌ In-app purchase bypass
```

**Fix**: Use StoreKit for digital goods

---

## 📤 Submission Process

### 1. Prepare Build

```bash
# Archive
xcodebuild archive \
  -scheme "YourApp" \
  -archivePath build/YourApp.xcarchive

# Export
xcodebuild -exportArchive \
  -archivePath build/YourApp.xcarchive \
  -exportOptionsPlist ExportOptions.plist \
  -exportPath build/
```

### 2. Upload via Transporter/Xcode

### 3. App Store Connect

1. Select build
2. Fill metadata
3. Add screenshots
4. Complete App Privacy
5. Submit for Review

---

## ⏱️ Review Timeline

| Type | Duration |
|------|----------|
| Standard | 24-48 hours |
| Expedited | 24 hours (special request) |
| Rejection response | 24-48 hours |

---

## 🔗 Related

- [Apple App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)

