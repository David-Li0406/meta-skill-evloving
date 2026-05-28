# Google-Play-Billing - Purchases

**Pages:** 4

---

## 打击欺诈和滥用行为 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/security

**Contents:**
- 打击欺诈和滥用行为 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 将敏感逻辑移至后端
- 在授予权利前验证购买交易
- 保护未锁定内容
- 检测并处理作废的购买交易
- 帮助 Google 在欺诈发生前及时发现欺诈行为
- 针对商标和版权侵犯行为采取行动

随着您的应用越来越受欢迎，它也会引起恶意用户的注意，他们可能会滥用您的应用。本主题介绍了一些建议，您应该利用这些建议帮助防止这些针对结算服务集成的攻击，并减少滥用行为对您的应用的影响。

在应用设计允许的范围内，尽可能将敏感数据和逻辑移至您控制的后端服务器。前端设备中的数据和逻辑越多，就越容易遭到修改或篡改。

例如，在线国际象棋游戏应该在后端验证每一步，而不是相信前端发送的每一步始终都是合法的。

此外，如果发现了漏洞或安全问题，根据您的系统设计，在后端而非前端进行调试、修复和发布更新可能也会更容易。

应该在后端处理敏感数据和逻辑的一种特殊情况是购买交易验证和确认。用户完成购买交易后，您应该执行以下操作：

授予权利后，如果您想消耗和确认消耗型商品，请在安全的后端服务器上使用 Purchases.products:consume Play Developer API。如需确认非消耗型商品或订阅，请在安全的后端服务器上调用相关的 Play Developer API 端点（Purchases.products:acknowledge 或 Purchases.subscriptions:acknowledge）。必须进行确认，这样才能向 Google Play 告知用户已获得购买交易的权利。您应在授予权利后立即确认购买交易。

请注意，虽然您可以通过应用在客户端确认或消耗购买交易，但服务器端 API 可以针对网络连接不佳和恶意活动等问题多提供一重保护。例如，假设用户已从您的应用购买商品，但在购买交易验证期间网络连接中断了。如果没有服务器确认，他们可能需要通过应用重新登录才能完成确认流程。否则，如果用户在三天内未重新登录，购买交易会因未经确认而自动退款。服务器确认可防止出现这种情况，因为它会在 Google Play 将购买交易有效的消息告知服务器后立即发送确认信息。

如需详细了解购买交易确认和消耗，请参阅处理购买交易。

为防止恶意用户重新分发您未锁定的内容，请勿将这种内容放入您的 APK 文件中，而是执行以下操作之一：

通过远程服务器或实时服务发送内容时，您可以将未锁定内容存储在设备内存中或设备的 SD 卡上。如果将内容存储在 SD 卡上，请务必加密内容并使用设备专用加密密钥。

作废的购买交易是指已经取消、撤消或退款的购买交易。如果作废的购买交易此前已向用户授予应用内商品或其他内容，您可以使用 Voided Purchases API 获悉购买交易作废的原因并获得您可以收回的任何关联内容。

购买应用内商品和订阅的交易可能出于各种原因而作废，其中包括：

您可以根据购买交易作废的原因并考虑用户以前的行为数据来决定相应的操作。我们建议您执行以下一项或多项操作：

实施某些类型的欺诈行为的恶意用户会创建多个 Google 账号和应用内账号来隐藏他们的活动。

将 builder 中的 setObfuscatedAccountId 和 setObfuscatedProfileId 方法用于 BillingFlowParams 可帮助 Google 将 Google 账号映射到应用内账号。

Google 会使用这些数据检测可疑行为，并在某些类型的欺诈性交易完成之前及时加以阻止。

如果您使用远程服务器发送或管理内容，请确保当用户访问内容时，应用能够验证未锁定内容的购买状态。这样，您就可以根据需要撤消使用权，并最大限度地减少盗版。如果您看到自己的内容在 Google Play 上被重新分发，请务必迅速、果断地采取行动。如需了解更多详情，请参阅版权帮助中心内的版权常见问题解答页面。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

---

## 打击欺诈和滥用行为 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/security?hl=zh-cn

**Contents:**
- 打击欺诈和滥用行为 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 将敏感逻辑移至后端
- 在授予权利前验证购买交易
- 保护未锁定内容
- 检测并处理作废的购买交易
- 帮助 Google 在欺诈发生前及时发现欺诈行为
- 针对商标和版权侵犯行为采取行动

随着您的应用越来越受欢迎，它也会引起恶意用户的注意，他们可能会滥用您的应用。本主题介绍了一些建议，您应该利用这些建议帮助防止这些针对结算服务集成的攻击，并减少滥用行为对您的应用的影响。

在应用设计允许的范围内，尽可能将敏感数据和逻辑移至您控制的后端服务器。前端设备中的数据和逻辑越多，就越容易遭到修改或篡改。

例如，在线国际象棋游戏应该在后端验证每一步，而不是相信前端发送的每一步始终都是合法的。

此外，如果发现了漏洞或安全问题，根据您的系统设计，在后端而非前端进行调试、修复和发布更新可能也会更容易。

应该在后端处理敏感数据和逻辑的一种特殊情况是购买交易验证和确认。用户完成购买交易后，您应该执行以下操作：

授予权利后，如果您想消耗和确认消耗型商品，请在安全的后端服务器上使用 Purchases.products:consume Play Developer API。如需确认非消耗型商品或订阅，请在安全的后端服务器上调用相关的 Play Developer API 端点（Purchases.products:acknowledge 或 Purchases.subscriptions:acknowledge）。必须进行确认，这样才能向 Google Play 告知用户已获得购买交易的权利。您应在授予权利后立即确认购买交易。

请注意，虽然您可以通过应用在客户端确认或消耗购买交易，但服务器端 API 可以针对网络连接不佳和恶意活动等问题多提供一重保护。例如，假设用户已从您的应用购买商品，但在购买交易验证期间网络连接中断了。如果没有服务器确认，他们可能需要通过应用重新登录才能完成确认流程。否则，如果用户在三天内未重新登录，购买交易会因未经确认而自动退款。服务器确认可防止出现这种情况，因为它会在 Google Play 将购买交易有效的消息告知服务器后立即发送确认信息。

如需详细了解购买交易确认和消耗，请参阅处理购买交易。

为防止恶意用户重新分发您未锁定的内容，请勿将这种内容放入您的 APK 文件中，而是执行以下操作之一：

通过远程服务器或实时服务发送内容时，您可以将未锁定内容存储在设备内存中或设备的 SD 卡上。如果将内容存储在 SD 卡上，请务必加密内容并使用设备专用加密密钥。

作废的购买交易是指已经取消、撤消或退款的购买交易。如果作废的购买交易此前已向用户授予应用内商品或其他内容，您可以使用 Voided Purchases API 获悉购买交易作废的原因并获得您可以收回的任何关联内容。

购买应用内商品和订阅的交易可能出于各种原因而作废，其中包括：

您可以根据购买交易作废的原因并考虑用户以前的行为数据来决定相应的操作。我们建议您执行以下一项或多项操作：

实施某些类型的欺诈行为的恶意用户会创建多个 Google 账号和应用内账号来隐藏他们的活动。

将 builder 中的 setObfuscatedAccountId 和 setObfuscatedProfileId 方法用于 BillingFlowParams 可帮助 Google 将 Google 账号映射到应用内账号。

Google 会使用这些数据检测可疑行为，并在某些类型的欺诈性交易完成之前及时加以阻止。

如果您使用远程服务器发送或管理内容，请确保当用户访问内容时，应用能够验证未锁定内容的购买状态。这样，您就可以根据需要撤消使用权，并最大限度地减少盗版。如果您看到自己的内容在 Google Play 上被重新分发，请务必迅速、果断地采取行动。如需了解更多详情，请参阅版权帮助中心内的版权常见问题解答页面。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

---

## 管理订阅和一次性购买交易 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/manage-purchases

**Contents:**
- 管理订阅和一次性购买交易 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 取消订阅
  - 用户发起的取消
  - 开发者发起的取消
    - 允许用户恢复尚未过期的订阅
    - 允许用户重新订阅已过期的订阅
    - 允许用户仅在您的应用中重新订阅
- 延迟结算
- 发放退款和撤消
  - 根据订单 ID 全额退款

在日常业务中，您可能需要对订阅或一次性购买交易执行管理操作。例如，您的客户服务团队可能需要为用户办理全额或部分退款，或者您可能需要在某些情况下撤消使用权。您可以通过 Play 管理中心管理订单，也可以使用 Google Play Developer API 通过自己的系统进行管理。

用户可以随时使用 Play 商店取消 Google Play 订阅。此外，您还必须为用户提供在您的应用和网站上取消订阅的选项（如果适用）。

如需让用户能够自愿取消订阅，最简单的方法是在应用中提供指向 Play 商店的深层链接，以便用户在其中查看和管理其订阅。

作为开发者，您可能还需要从后端触发取消。借助 purchases.subscriptions.cancel API，您可以取消订阅购买交易。例如，您可以使用此方法关闭旧版服务。取消订阅后，系统不会退款，但用户仍可继续访问相关订阅内容，直到当前结算周期结束为止。

借助此方法，您可以在 cancellationType 请求正文参数中指定以下类型的取消：

USER_REQUESTED_STOP_RENEWALS：取消订阅，就像用户在 Play 商店中取消订阅一样。所有分期付款将在当前承诺期的剩余时间内继续。用户可以在订阅到期前从 Play 商店恢复订阅，或在订阅到期后重新订阅（如果基础方案支持）。

DEVELOPER_REQUESTED_STOP_PAYMENTS：取消订阅并阻止任何进一步付款。用户无法通过 Play 商店恢复或重新订阅，但您可以允许他们在您的应用中重新订阅。

在某些情况下，您可能需要允许用户在您作为开发者触发取消后，从 Play 订阅中心恢复未到期的订阅。例如，您可能需要提供自定义的应用内取消流程。根据您的业务逻辑，您可以决定用户可以恢复哪些从后端触发的取消。

如需指明用户可以恢复取消操作，请向 purchases.subscriptions.cancel API 发出 POST 请求，并将 cancellationType 请求参数设置为 USER_REQUESTED_STOP_RENEWAL 值。

如需允许重新订阅已过期的订阅，您必须在订阅的基础方案中启用重新订阅选项，然后将 cancellationType 参数设置为 USER_REQUESTED_STOP_RENEWAL 值以取消订阅。

如果您已将 cancellationType 参数设置为 DEVELOPER_REQUESTED_STOP _PAYMENTS 或未设置 cancellationType 参数，用户将无法通过 Play 订阅中心恢复其订阅。不过，如果需要，用户可以通过您的应用重新订阅。

执行此操作会触发 SUBSCRIPTION_CANCELED 实时开发者通知。请按照取消中的说明来处理这些取消事件。

使用 subscriptions.defer 可延长订阅的使用权期限。在推迟期内，用户仍会订阅您的内容，但不会为额外时间付费。当您推迟订阅的结算时，状态信息会相应更新，您会在购买交易状态信息的 expiryTime 字段中看到相应信息：

每次调用该 API，结算最短可推迟一天，最长为一年。如需进一步推迟使用权到期时间，请在新到期日期到来之前再次调用该 API。

执行此操作会触发 SUBSCRIPTION_DEFERRED 实时开发者通知。如需了解如何处理这些事件，请参阅订阅简介中的为订阅者推迟结算。

FitnessGoals 在线媒体服务希望在 2 月开展促销活动，鼓励用户定期锻炼。

他们决定，如果订阅者在 2 月份使用 FitnessGoals 锻炼了至少 10 次，则可额外获享一个月的服务。

他们会跟踪挑战的结果，并在 3 月 1 日针对 2 月份完成挑战的用户的每笔有效订阅购买交易调用 subscriptions.defer API。

这些用户可以额外免费获享一个月的常规锻炼视频，并告诉所有朋友 FitnessGoals 如何帮助他们保持健康！

在很多情况下，您可能需要针对订阅或一次性购买交易发放退款或撤消访问权限。

借助 orders.refund API，您可以针对购买后的三年内任何订单发放全额退款。orders.refund 方法会接收一个 revoke 参数，用于指明是否应在提供退款的同时撤消访问权限。

如果您通过针对订阅购买交易的退款调用发出撤消请求，系统会立即终止订阅，并触发 SUBSCRIPTION_REVOKED 实时开发者通知。请参阅订阅生命周期管理指南的“撤消”部分，了解如何处理这些事件。

为了庆祝新世界杯的开始，电子竞技应用 Football-Not-Soccer 决定为在前 24 小时内购买新球队套装的所有用户抽奖，送出免费的虚拟球衣。

Football-Not-Soccer 使用 orders.refund API，但未传递撤消参数，因此无法向胜出者退还球衣购买交易款项。

对于某些用例，您可能需要撤消对用户订阅的访问权限并提供退款。Play 结算服务提供通过 subscriptionsv2.revoke API 进行撤消的方法，包括全额退款和按比例退款。通过此端点，您可以指定 revocationContext 以确定退款的计算方式。

执行此操作会触发 SUBSCRIPTION_REVOKED 实时开发者通知。您的应用应按照撤消中的说明来处理这些取消事件。

如果您需要终止订阅并退还当前结算周期的全额款项，请全额退款。使用 purchases.subscriptionsv2.revoke 函数，并将 "fullRefund": {} 设置为退款类型。

Maria 订阅了 SuperMovies 在线影音月度方案，并选择了 30 天自动续订。Maria 遇到了一些技术问题，导致她无法访问内容。她在账单周期的第 3 天联系了客户服务团队，表示自己从未获得对该订阅的访问权限。

客户服务团队在其系统中找到了 Maria 的订阅购买交易详情，并触发了对 purchases.subscriptionsv2.revoke 的调用，请求全额退款。

客户服务人员告诉 Maria，她应该会收到全额订阅费用退款，并且她不再订阅该方案。

如果您需要终止订阅并针对剩余的使用权时长退款，请按比例退款。使用 purchases.subscriptionsv2.revoke 函数，并将 "proratedRefund": {} 设置为退款类型。

Maria 订阅了 SuperMovies 在线影音月度方案，并选择了 30 天自动续订。她已经愉快地使用该服务一段时间了。 Maria 在结算周期的第 15 天联系了客户服务团队，表示她要移居海外，从次日起将无法再使用该服务。

客户服务团队在其系统中找到了 Maria 的订阅购买交易详情，并触发了对 purchases.subscriptionsv2.revoke 的调用，请求按比例退款。

客户服务人员告诉 Maria，她应该会收到约 50% 的订阅费用退款，并且服务访问权限将立即终止。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

**Examples:**

Example 1 (unknown):
```unknown
https://androidpublisher.googleapis.com/androidpublisher/v3/applications/com.your.app/purchases/subscriptions/your-subscription-product/tokens/1a2b3c4d5e6f7g8h9i0j:cancel
```

Example 2 (unknown):
```unknown
https://androidpublisher.googleapis.com/androidpublisher/v3/applications/com.your.app/purchases/subscriptions/your-subscription-product/tokens/1a2b3c4d5e6f7g8h9i0j:cancel
```

Example 3 (unknown):
```unknown
{
  "cancellationType": "USER_REQUESTED_STOP_RENEWAL"
}
```

Example 4 (unknown):
```unknown
{
  "cancellationType": "USER_REQUESTED_STOP_RENEWAL"
}
```

---

## 管理订阅和一次性购买交易 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/manage-purchases?hl=zh-cn

**Contents:**
- 管理订阅和一次性购买交易 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 取消订阅
  - 用户发起的取消
  - 开发者发起的取消
    - 允许用户恢复尚未过期的订阅
    - 允许用户重新订阅已过期的订阅
    - 允许用户仅在您的应用中重新订阅
- 延迟结算
- 发放退款和撤消
  - 根据订单 ID 全额退款

在日常业务中，您可能需要对订阅或一次性购买交易执行管理操作。例如，您的客户服务团队可能需要为用户办理全额或部分退款，或者您可能需要在某些情况下撤消使用权。您可以通过 Play 管理中心管理订单，也可以使用 Google Play Developer API 通过自己的系统进行管理。

用户可以随时使用 Play 商店取消 Google Play 订阅。此外，您还必须为用户提供在您的应用和网站上取消订阅的选项（如果适用）。

如需让用户能够自愿取消订阅，最简单的方法是在应用中提供指向 Play 商店的深层链接，以便用户在其中查看和管理其订阅。

作为开发者，您可能还需要从后端触发取消。借助 purchases.subscriptions.cancel API，您可以取消订阅购买交易。例如，您可以使用此方法关闭旧版服务。取消订阅后，系统不会退款，但用户仍可继续访问相关订阅内容，直到当前结算周期结束为止。

借助此方法，您可以在 cancellationType 请求正文参数中指定以下类型的取消：

USER_REQUESTED_STOP_RENEWALS：取消订阅，就像用户在 Play 商店中取消订阅一样。所有分期付款将在当前承诺期的剩余时间内继续。用户可以在订阅到期前从 Play 商店恢复订阅，或在订阅到期后重新订阅（如果基础方案支持）。

DEVELOPER_REQUESTED_STOP_PAYMENTS：取消订阅并阻止任何进一步付款。用户无法通过 Play 商店恢复或重新订阅，但您可以允许他们在您的应用中重新订阅。

在某些情况下，您可能需要允许用户在您作为开发者触发取消后，从 Play 订阅中心恢复未到期的订阅。例如，您可能需要提供自定义的应用内取消流程。根据您的业务逻辑，您可以决定用户可以恢复哪些从后端触发的取消。

如需指明用户可以恢复取消操作，请向 purchases.subscriptions.cancel API 发出 POST 请求，并将 cancellationType 请求参数设置为 USER_REQUESTED_STOP_RENEWAL 值。

如需允许重新订阅已过期的订阅，您必须在订阅的基础方案中启用重新订阅选项，然后将 cancellationType 参数设置为 USER_REQUESTED_STOP_RENEWAL 值以取消订阅。

如果您已将 cancellationType 参数设置为 DEVELOPER_REQUESTED_STOP _PAYMENTS 或未设置 cancellationType 参数，用户将无法通过 Play 订阅中心恢复其订阅。不过，如果需要，用户可以通过您的应用重新订阅。

执行此操作会触发 SUBSCRIPTION_CANCELED 实时开发者通知。请按照取消中的说明来处理这些取消事件。

使用 subscriptions.defer 可延长订阅的使用权期限。在推迟期内，用户仍会订阅您的内容，但不会为额外时间付费。当您推迟订阅的结算时，状态信息会相应更新，您会在购买交易状态信息的 expiryTime 字段中看到相应信息：

每次调用该 API，结算最短可推迟一天，最长为一年。如需进一步推迟使用权到期时间，请在新到期日期到来之前再次调用该 API。

执行此操作会触发 SUBSCRIPTION_DEFERRED 实时开发者通知。如需了解如何处理这些事件，请参阅订阅简介中的为订阅者推迟结算。

FitnessGoals 在线媒体服务希望在 2 月开展促销活动，鼓励用户定期锻炼。

他们决定，如果订阅者在 2 月份使用 FitnessGoals 锻炼了至少 10 次，则可额外获享一个月的服务。

他们会跟踪挑战的结果，并在 3 月 1 日针对 2 月份完成挑战的用户的每笔有效订阅购买交易调用 subscriptions.defer API。

这些用户可以额外免费获享一个月的常规锻炼视频，并告诉所有朋友 FitnessGoals 如何帮助他们保持健康！

在很多情况下，您可能需要针对订阅或一次性购买交易发放退款或撤消访问权限。

借助 orders.refund API，您可以针对购买后的三年内任何订单发放全额退款。orders.refund 方法会接收一个 revoke 参数，用于指明是否应在提供退款的同时撤消访问权限。

如果您通过针对订阅购买交易的退款调用发出撤消请求，系统会立即终止订阅，并触发 SUBSCRIPTION_REVOKED 实时开发者通知。请参阅订阅生命周期管理指南的“撤消”部分，了解如何处理这些事件。

为了庆祝新世界杯的开始，电子竞技应用 Football-Not-Soccer 决定为在前 24 小时内购买新球队套装的所有用户抽奖，送出免费的虚拟球衣。

Football-Not-Soccer 使用 orders.refund API，但未传递撤消参数，因此无法向胜出者退还球衣购买交易款项。

对于某些用例，您可能需要撤消对用户订阅的访问权限并提供退款。Play 结算服务提供通过 subscriptionsv2.revoke API 进行撤消的方法，包括全额退款和按比例退款。通过此端点，您可以指定 revocationContext 以确定退款的计算方式。

执行此操作会触发 SUBSCRIPTION_REVOKED 实时开发者通知。您的应用应按照撤消中的说明来处理这些取消事件。

如果您需要终止订阅并退还当前结算周期的全额款项，请全额退款。使用 purchases.subscriptionsv2.revoke 函数，并将 "fullRefund": {} 设置为退款类型。

Maria 订阅了 SuperMovies 在线影音月度方案，并选择了 30 天自动续订。Maria 遇到了一些技术问题，导致她无法访问内容。她在账单周期的第 3 天联系了客户服务团队，表示自己从未获得对该订阅的访问权限。

客户服务团队在其系统中找到了 Maria 的订阅购买交易详情，并触发了对 purchases.subscriptionsv2.revoke 的调用，请求全额退款。

客户服务人员告诉 Maria，她应该会收到全额订阅费用退款，并且她不再订阅该方案。

如果您需要终止订阅并针对剩余的使用权时长退款，请按比例退款。使用 purchases.subscriptionsv2.revoke 函数，并将 "proratedRefund": {} 设置为退款类型。

Maria 订阅了 SuperMovies 在线影音月度方案，并选择了 30 天自动续订。她已经愉快地使用该服务一段时间了。 Maria 在结算周期的第 15 天联系了客户服务团队，表示她要移居海外，从次日起将无法再使用该服务。

客户服务团队在其系统中找到了 Maria 的订阅购买交易详情，并触发了对 purchases.subscriptionsv2.revoke 的调用，请求按比例退款。

客户服务人员告诉 Maria，她应该会收到约 50% 的订阅费用退款，并且服务访问权限将立即终止。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

**Examples:**

Example 1 (unknown):
```unknown
https://androidpublisher.googleapis.com/androidpublisher/v3/applications/com.your.app/purchases/subscriptions/your-subscription-product/tokens/1a2b3c4d5e6f7g8h9i0j:cancel
```

Example 2 (unknown):
```unknown
https://androidpublisher.googleapis.com/androidpublisher/v3/applications/com.your.app/purchases/subscriptions/your-subscription-product/tokens/1a2b3c4d5e6f7g8h9i0j:cancel
```

Example 3 (unknown):
```unknown
{
  "cancellationType": "USER_REQUESTED_STOP_RENEWAL"
}
```

Example 4 (unknown):
```unknown
{
  "cancellationType": "USER_REQUESTED_STOP_RENEWAL"
}
```

---
