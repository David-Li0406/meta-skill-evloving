---
name: apple-appstore-reviewer
description: 'App Store Review Guidelines compliance checker. Kiểm tra app trước khi submit để tránh rejection, cover tất cả common issues và best practices.'
---

# Apple App Store Reviewer Skill

Skill này provide comprehensive checklist và guidelines để ensure app passes App Store review, tránh rejection.

## Khi Nào Sử Dụng

- Chuẩn bị submit app lên App Store
- Review app trước submission
- Fix app bị rejected
- Audit existing app cho compliance
- Plan features để avoid rejection

---

## Common Rejection Reasons

### Top 10 Rejection Categories

| # | Category | % |
|---|----------|---|
| 1 | Guideline 2.1 - App Completeness | 15% |
| 2 | Guideline 4.0 - Design | 12% |
| 3 | Guideline 2.3 - Accurate Metadata | 10% |
| 4 | Guideline 4.2 - Minimum Functionality | 9% |
| 5 | Guideline 5.1.1 - Data Collection | 8% |
| 6 | Guideline 2.1 - Performance: Crash | 7% |
| 7 | Guideline 3.1.1 - In-App Purchase | 6% |
| 8 | Guideline 5.1.2 - Data Use | 5% |
| 9 | Guideline 4.3 - Spam | 4% |
| 10 | Guideline 1.2 - User Generated Content | 4% |

---

## Pre-Submission Checklist

### 1. App Completeness (Guideline 2.1)

- [ ] App fully functional, không placeholder content
- [ ] All links hoạt động
- [ ] All features accessible (không "coming soon")
- [ ] Test account provided nếu cần login
- [ ] Clear instructions trong review notes
- [ ] Demo video nếu có hardware requirements

### 2. Performance

- [ ] App không crash
- [ ] No memory leaks
- [ ] Fast load times (< 5 seconds)
- [ ] Works offline (hoặc graceful degradation)
- [ ] No excessive battery/data usage
- [ ] Test trên actual devices (không chỉ simulator)

### 3. Metadata Accuracy (Guideline 2.3)

- [ ] App name matches functionality
- [ ] Description accurate và clear
- [ ] Screenshots reflect actual app
- [ ] Keywords relevant, không misleading
- [ ] No mentions of other platforms
- [ ] Age rating appropriate
- [ ] Category chính xác

### 4. Design (Guideline 4)

- [ ] Follows Human Interface Guidelines
- [ ] Native UI elements where appropriate
- [ ] Support all device sizes
- [ ] Support Dark Mode
- [ ] Consistent design language
- [ ] Clear navigation
- [ ] Accessible (VoiceOver, Dynamic Type)

### 5. Minimum Functionality (Guideline 4.2)

- [ ] Not just a website wrapper
- [ ] Not just marketing material
- [ ] Provides real utility
- [ ] Has sufficient content
- [ ] Features work as advertised
- [ ] Not too simple/limited

### 6. Privacy (Guideline 5.1)

- [ ] Privacy Policy accessible trong app
- [ ] Privacy Policy URL in App Store Connect
- [ ] Data collection disclosed
- [ ] App Privacy labels accurate
- [ ] Permissions explained (camera, location, etc.)
- [ ] ATT (App Tracking Transparency) if tracking
- [ ] GDPR/CCPA compliance if applicable

### 7. In-App Purchases (Guideline 3.1)

- [ ] Use Apple's IAP for digital goods
- [ ] IAP descriptions clear
- [ ] Restore Purchases works
- [ ] Subscription terms clear
- [ ] Free trial terms clear
- [ ] No external payment links for digital content

### 8. User Generated Content (Guideline 1.2)

- [ ] Có system để report offensive content
- [ ] Có mechanism để block users
- [ ] Content moderation plan
- [ ] Age gate if needed
- [ ] Terms of service

### 9. Legal

- [ ] No copyrighted material without permission
- [ ] No trademark violations
- [ ] Appropriate age rating
- [ ] Regional compliance (COPPA, etc.)
- [ ] Export compliance if needed

### 10. App Store Connect

- [ ] All screenshots uploaded (all device sizes)
- [ ] App Preview videos (optional but recommended)
- [ ] Keywords optimized
- [ ] Support URL works
- [ ] Contact information valid
- [ ] Build uploaded và processed

---

## Review Notes Template

```
Demo Account:
- Email: demo@example.com
- Password: Demo123!

Special Instructions:
1. [Feature X] requires [specific setup]
2. To test [Feature Y], please [instructions]

Notes:
- This app uses [external service] for [purpose]
- [Specific feature] requires [hardware/permission]

Contact:
- Email: developer@example.com
- Phone: +1-xxx-xxx-xxxx
```

---

## Common Fixes

### Crash on Launch
- Test on clean install
- Test after update from previous version
- Check for force-unwrapped optionals
- Verify all required capabilities enabled

### Metadata Issues
- Remove mentions of "beta", "test", "demo"
- Remove references to other platforms (Android, etc.)
- Use actual screenshots, không mockups
- Ensure keywords không misleading

### Design Issues
- Use standard navigation patterns
- Ensure buttons có proper tap targets (44pt min)
- Support Dynamic Type
- Implement proper loading states

### Privacy Issues
- Add privacy policy page trong app
- Request permissions contextually (không on launch)
- Explain why permissions needed
- Implement ATT if tracking users

### IAP Issues
- Ensure restore purchases works
- Clear pricing information
- No references to external payment methods

---

## Implementation & Code Examples

- **Canonical implementation**: `ios_foundation/iap_core_implementation.md` — production-ready StoreKit 2 repository, ViewModel and DI examples.
- **Compliance checklist & assets**: `ios_foundation/iap_compliance_guidelines.md` — promotional images, metadata, paywall rules.

### Quick StoreKit 2 snippet (purchase + finish)
```swift
import StoreKit

@MainActor
func purchase(product: Product) async throws -> Transaction? {
   let result = try await product.purchase()
   switch result {
   case .success(let verification):
      let transaction = try verification.payloadValue
      await transaction.finish()
      return transaction
   case .userCancelled:
      return nil
   default:
      return nil
   }
}
```

### Usage notes
- Link `ios_foundation/iap_core_implementation.md` from feature specs or PR descriptions when implementing paywalls to avoid accidental divergence.
- Before implementation, verify App Store rules in `skills/apple-appstore-reviewer/SKILL.md` and `ios_foundation/iap_compliance_guidelines.md` to minimize rejection risk.

### Conflict check
- I searched existing skills and docs: IAP guidance and code live under `ios_foundation/` and are referenced from this skill. No conflicting IAP guidance exists in other skills (design / web / localization). It's safe to adopt the `ios_foundation` implementation as canonical; prefer linking rather than copying to keep a single source of truth.

---

## Expedited Review

Khi cần review nhanh:

1. Log in to App Store Connect
2. Go to app
3. Contact Us (bottom of page)
4. Request expedited review
5. Explain reason:
   - Critical bug fix
   - Security issue
   - Time-sensitive event

---

## After Rejection

### Response Workflow

1. **Read rejection carefully** - Understand specific issue
2. **Don't argue** - Fix the issue
3. **Document changes** - Clear in review notes
4. **Respond professionally** - Via Resolution Center
5. **Request call if unclear** - Apple offers phone support

### Response Template
```
Thank you for your feedback.

We have addressed the issue as follows:
1. [Issue]: [How we fixed it]
2. [Issue]: [How we fixed it]

Additional notes:
- [Any clarification needed]

Please let us know if you need any additional information.

Best regards,
[Developer Name]
```

---

## Resources

| Resource | URL |
|----------|-----|
| App Store Review Guidelines | developer.apple.com/app-store/review/guidelines/ |
| Human Interface Guidelines | developer.apple.com/design/human-interface-guidelines/ |
| App Store Connect Help | help.apple.com/app-store-connect/ |
| Common App Rejections | developer.apple.com/app-store/review/rejections/ |
