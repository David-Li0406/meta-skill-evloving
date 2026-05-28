# IAP Integration Reference

Tài liệu tóm tắt để implement In-App Purchase (IAP) / Paywall trong features iOS.

## Khi nào dùng
- Khi feature cần unlock content/functionality bằng mua trong app.
- Khi cần thiết kế paywall, restore purchases, subscription handling.

## Canonical Implementation
- Full code và patterns nằm tại: `ios_foundation/iap_core_implementation.md`
- Compliance & App Store guidance: `ios_foundation/iap_compliance_guidelines.md`

## Quick Guidelines
- Use StoreKit 2 (iOS 15+) where possible.
- Keep paywall content accurate with App Store metadata.
- Provide unique promotional images per IAP.
- Implement Restore Purchases and `restoreCompletedTransactions`-equivalent flow.
- Persist minimal purchase state (Keychain/UserDefaults) and validate receipts via StoreKit APIs.

## Quick StoreKit 2 Example
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

## How to use this reference
- Link `ios_foundation/iap_core_implementation.md` from feature specs or PRs that implement paywalls.
- Prefer linking rather than copying large code blocks to avoid divergence.
- Validate App Store requirements (metadata, privacy, promotional images) before submitting.

## Notes on conflicts
- IAP guidance exists in `ios_foundation/` and `skills/apple-appstore-reviewer/SKILL.md` references it. This reference is a convenience link for iOS implementers; it intentionally delegates to the canonical `ios_foundation` docs to avoid duplication.
