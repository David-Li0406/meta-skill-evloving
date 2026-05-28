# Google-Play-Billing - Other

**Pages:** 43

---

## 开发者载荷 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/developer-payload?hl=zh-cn

**Contents:**
- 开发者载荷 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 购物验证
- 购买交易归因
- 将元数据与购买交易相关联

开发者载荷向来被用于各种不同用途，包括防欺诈以及将购买交易归因于正确的用户。在 Google Play 结算库 2.2 及更高版本中，以前依赖于开发者载荷的预期用例现在也在该库的其他部分获得完全支持。

因为有了这样的支持，从 Google Play 结算库 2.2 版开始，我们已弃用开发者载荷。与开发者载荷关联的方法在 2.2 版中已废弃，且在 3.0 版中已移除。请注意，对于使用先前版本的库或 AIDL 完成的购买交易，应用可继续检索开发者载荷。

如需查看详细的变更清单，请参阅 Google Play 结算库 2.2 版本说明和 Google Play 结算库 3.0 版本说明。

为确保购买交易的真实性并防止伪造或重播，Google 建议您将购买令牌（通过 Purchase 对象中的 getPurchaseToken() 方法获取）与 Google Play Developer API 配合使用，验证购买交易的真实性。如需了解详情，请参阅打击欺诈和滥用行为。

许多应用（特别是游戏）需要确保将购买交易正确归因于发起购买交易的游戏内角色/头像或应用内用户个人资料。从 Google Play 结算库 2.2 开始，应用在启动购买对话框时可将经过混淆处理的账号和个人资料标识符传递给 Google，而在应用检索购买交易时也会返回相应信息。

在 BillingFlowParams 中使用 setObfuscatedAccountId() 和 setObfuscatedProfileId() 参数，并使用 Purchase 对象中的 getAccountIdentifiers() 方法检索这些参数。

Google 建议您将有关购买交易的元数据存储在您维护的安全后端服务器上。此购买交易元数据应与通过 Purchase 对象中的 getPurchaseToken 方法获取的购买令牌相关联。在成功完成购买交易后调用 PurchasesUpdatedListener 时将购买令牌和元数据传递到您的后端，就可以保留这些数据。

为确保在购买流程中断的情况下关联元数据，Google 建议在启动购买对话框之前将元数据存储在后端服务器上，并将其与用户的账号 ID、正在购买的 SKU 和当前时间戳相关联。

如果购买流程在调用 PurchasesUpdatedListener 之前中断，当应用恢复并调用 BillingClient.queryPurchasesAsync() 后，应用会立即发现购买交易。然后，您可以将从 Purchase 对象的 getPurchaseTime()、getSku() 和 getPurchaseToken() 方法检索到的值发送到后端服务器，以查询元数据，将元数据与购买令牌关联，并继续处理购买交易。请注意，您最初存储的时间戳与 Purchase 对象的 getPurchaseTime() 中的值不会完全匹配，因此您需要大致地对比二者。例如，您可以检查值之间是否相隔在特定时间段内。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

---

## 有关替代的应用内购结算系统的临时用户体验指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/alternative/interim-ux/billing-choice

**Contents:**
- 有关替代的应用内购结算系统的临时用户体验指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 概览
- 面向用户的信息
  - 何时显示
  - 何时显示价格
  - 如何显示
  - 用户操作
    - 继续
    - 了解详情
    - 关闭

为了维持一致的用户体验并帮助用户做出明智的选择，您需要显示信息屏幕；如果除了 Google Play 结算系统以外，您还提供替代的应用内购结算系统，则还需要显示单独的结算方式选择屏幕。信息屏幕只需在每位用户首次发起购买交易时向其显示即可，而结算方式选择屏幕应在每次购买交易前向用户显示。应根据以下准则为这两个屏幕实现面向用户的消息和界面规范。

信息屏幕可以帮助用户了解相关更改的背景，并提供更多信息以帮助用户做出明智的选择。

添加替代应用内购结算系统后，应在用户开始进行首次购买交易时向其显示信息屏幕。当同一用户以后再次进行购买交易时，就不需要再显示该信息了。在用户执行明确操作以发起购买交易之后，系统应立即显示信息屏幕。

应在显示信息屏幕或结算方式选择屏幕之前，在显眼的位置向用户显示购买价格。

信息屏幕应显示在模态底部动作条中。模态底部动作条与模态对话框类似，它会从屏幕底部向上呈现动画效果，并固定在屏幕底部。它位于底层屏幕中的所有界面元素的上层。底层屏幕会被深色纱罩遮挡，以表示它不会响应用户互动。

如需详细了解模态底部动作条的设计和实现，请参阅 Google Material Design。

当用户点按应用中用于发起购买交易的按钮或其他界面元素时，底部动作条应触发。用户可以在信息屏幕中执行 3 种可能的操作：

点按“继续”按钮会关闭信息屏幕，并启动结算方式选择屏幕。

点按“了解详情”按钮可在网络浏览器中打开相应的 Google 帮助中心文章。

如果用户要关闭底部动作条并返回底层屏幕，可以通过以下方式关闭底部动作条：

在用户关闭信息屏幕或点按“继续”后，无需再次显示信息屏幕。

示例：在用户发起购买交易之前，购买交易已明确显示。点按“立即加入”按钮会触发信息屏幕。

信息屏幕分为 3 个组件：标题、消息和按钮。所有这 3 个组件都是必需的，其包含的文字和界面元素必须与本准则中的定义完全一致。请勿在该屏幕中添加任何其他文字或图像，但您可以在其他屏幕中添加额外的文字和图像。

在横向视图中，底部动作条的宽度大于纵向视图中的宽度，但在其他方面都遵循相同的设计规范和功能。

结算方式选择界面向用户展示两种结账选项，用于完成购买交易。为了帮助用户做出明智的决策，每个结算服务选项还会向用户显示可用的付款方式。在用户做出选择后，他们将继续通过所选的结算服务完成购买交易。

如果用户已查看过信息屏幕，则在其执行明确操作以发起购买交易后，系统应立即显示结算方式选择屏幕。

结算方式选择屏幕应该显示在模态底部动作条中，并遵循与信息屏幕相同的规范。

您应该采用公平且均等的方式来展示其他应用内购结算系统的按钮和 Google Play 结算服务的按钮。这包括但不限于相同的按钮大小、文字大小/样式、点按目标和图标大小。请勿添加本指南中未定义的任何其他文字、图片或样式更改。

示例：点按“立即加入”按钮会触发结算方式选择屏幕。

结算方式选择屏幕包含 4 个不同的组件：标题、说明、开发者按钮和 Google Play 按钮。您应使用所有组件，并且这些组件包含的文字和界面元素应与本准则中的定义完全一致。请勿在该屏幕中添加任何其他文字或图像，但您可以在您拥有的其他屏幕中添加其他文字和图像。

您可以通过以下链接获取 Google Play 的可视化资源和付款图标。

示例：在纵向视图中，底部动作条的跨度应该与屏幕总宽度相等。

示例：在横向视图中，底部动作条的宽度大于纵向视图中的宽度，但在其他方面都遵循相同的设计规范和功能。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

---

## 外部优惠 API 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/external

**Contents:**
- 外部优惠 API 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 术语词汇表
- 支持外部优惠
  - 在 Play 管理中心内配置
  - 面向用户的信息界面
  - 后续步骤

在某些国家/地区，符合条件的开发者可以将用户引导到应用以外，包括宣传应用内数字功能和服务的相关优惠。本指南将介绍用于启用外部优惠的 API。您应该先查看计划要求并加入外部优惠计划，然后再使用这些 API。

本部分介绍如何支持外部商品。 使用这些 API 之前，请确保以下几点：

如需在 Play 管理中心内配置外部优惠，请按照计划要求中列出的步骤操作。

信息界面有助于用户了解他们将要访问一个外部网站。系统每次都会向用户显示信息界面，然后才会使用外部优惠 API 将用户定向到应用之外。

如需开始集成外部优惠 API，请遵循应用内集成和后端集成的深度指南。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

---

## 有关 Google Play 结算服务之外的变现的后端集成指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/alternative/backend?hl=zh-cn

**Contents:**
- 有关 Google Play 结算服务之外的变现的后端集成指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 向 Google Play 报告新的外部交易
  - 外部交易报告
  - 报告新购买交易
  - 报告购买交易的后续交易
  - 报告升级或降级
  - 停止手动报告备选结算系统交易
  - 举报 Play 合作伙伴计划
- 向 Google Play 报告购买交易退款
- API 配额

Google Play Developer API 现在包含 报告来自备选结算系统的交易，或 外部优惠系统。本指南将介绍如何报告替代性数据， 结算或外部优惠交易。

从后端处理应用内购买交易时，可能需要用到一些组件。如需构建这些组件，您需要按照配置 Google Play Developer API 中的说明设置后端集成。对于 所有不特定于备选结算系统的开发者后端功能 或外部优惠 API 的说明， Google Play 结算系统文档适用。

与 Externaltransactions APIs 集成 报告 Google Play 结算系统以外发生的交易， 支持的国家/地区，包括通过免费试用产生的 0 美元交易 购买。通过备选结算系统或外部优惠系统进行的交易 仅在系统允许的情况下，才应针对符合条件的用户所在国家/地区启动和报告 在备选结算系统下，或者 外部优惠计划，否则，API 调用将 已被拒绝。这适用于所有交易，包括新购买、续订 充值、升级、降级等操作。

您应该调用 Externaltransactions API 来报告外部交易 在通过备选结算系统获得授权后，或者 外部优惠系统这适用于所有交易，包括 扣款、续订、退款等。所有交易都必须 会在交易发生 24 小时内报告。

系统会为每一笔外部交易报告一个外部交易 ID。对于周期性购买交易（例如自动续订型订阅），您需要发送与这笔周期性购买交易中的第一笔交易相关联的外部交易 ID，以用作后续所有交易（包括退款）的参数。这样就能记录相应购买交易的一系列交易。如果商品发生变化（例如升级或降级），或者周期性交易被取消或过期且之后同一商品再次被购买，您就需要针对相应交易发送新的外部交易 ID。您不得添加任何个人身份信息 这些信息、专有信息或机密信息， 交易 ID。

每当通过备选结算系统完成新购买交易时 或外部优惠系统，对 Externaltransactions API 的调用会 必填字段。对于这些新的购买交易，您需要提供唯一 externalTransactionId 以查询的形式与后端中的购买交易相关联 参数。此externalTransactionId不能在同一应用的 软件包 ID。

应用通过externalTransactionToken UserChoiceBillingListener、AlternativeBillingOnlyReportingDetailsListener、 或 ExternalOfferReportingDetailsListener 回调作为 一次性购买和首次交易的请求正文 周期性购买（例如订阅）。无论是哪种情况，都称为 初始交易。完成初始交易后， externalTransactionToken 不再需要，您后续报告 通过提供新的唯一身份 externalTransactionId。请参阅报告购买交易的后续交易 ，详细了解如何报告后续交易。

如果与印度境内的用户进行交易，由于该国税费因用户所在的行政区（例如州或省）而异，请务必在 userTaxAddress 下包含该行政区。如需了解适用的行政区，请参阅 API 参考指南中的预定义字符串列表。

在某些情况下，同一外部购买交易有多笔相关联的用户付款（例如，续订或预付费方案充值）。您可以在 Externaltransactions 中使用同一 API 报告这些后续交易。如报告新购买交易中所述，后续交易不需要 externalTransactionToken。不过，系统会为每笔续订或充值交易发送新的唯一 externalTransactionId 作为查询参数，并将初始交易的 ID 包含在 initialExternalTransactionId 字段中。

若要当用户拥有一项订阅的情况下在备选结算系统中报告升级或降级，您可在 Externaltransactions API 中使用相同的端点和函数，发送为升级或降级交易而提供给应用的 externalTransactionToken。这与报告新购买交易类似。

如需迁移您以非自动化报告方式提供备选结算系统期间开始的有效订阅，请使用 migratedTransactionProgram 字段（而不是指定 initialExternalTransactionId 或 externalTransactionToken）创建一笔新的 0 费用交易。将每项有效订阅的 transactionTime 设置为用户最初注册该订阅的时间。之后，照常通过 API 报告这些订阅的每一笔后续交易，并提供之前使用的 initialExternalTransactionId 创建续订交易。迁移订阅后，您无需再手动报告订阅的后续交易，但前提是这些交易是通过本页介绍的自动化方式报告的。

迁移订阅时，请留意当前的配额限制，以确保迁移不会用尽配额。如果有很多订阅需要 分几天进行迁移，或申请提高配额 配额 ，了解所有最新动态。

只有在从手动报告迁移时，才可以使用 migratedTransactionProgram 字段。当手动报告不再受支持后，该字段将被废弃。

参与合作伙伴计划（例如 Play 媒体体验计划必须提供 transaction_program_code（报告外部交易时）。如果您 如果您是符合条件的开发者，请与您的业务发展经理联系以了解详情 了解如何设置此字段。

与 Externaltransactions API 集成后，您可报告在 Google Play 结算系统以外向用户退款的交易。为了让 Play 正确识别哪一笔交易已退款，您应将之前所报告交易的相应 externalTransactionId 添加为网址参数的一部分。

报告订阅购买交易的退款时，请引用被退款订阅的具体周期性交易的 externalTransactionId。

如需报告该订阅所有交易的退款，您需要发出三个单独的退款请求：一个针对初始交易，两个针对后续交易。

此方法接受全额退款 （其中金额与用户在原始外部 交易）和部分退款 （金额小于用户在原始外部 交易）。对于部分退款，您需要指定退还的税前金额。

Externaltransactions API 受每日 API 配额限制 就像 Google Play Developer API 中的任何其他端点一样。

此外，在调用 Externaltransactions.createexternaltransaction 或 Externaltransactions.refundexternaltransaction 时，Externaltransactions API 的每分钟查询数量 (QPM) 上限为 1,200 个。对 Externaltransactions.getexternaltransaction 的调用不会计入此 1,200 QPM 的限额。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

**Examples:**

Example 1 (unknown):
```unknown
POST /androidpublisher/v3/applications/com.myapp.android/externalTransactions?externalTransactionId=123-456-789

Body
 {
"originalPreTaxAmount" : {
   "priceMicros": "0",
   "currency": "KRW"
 },
 "originalTaxAmount" : {
   "priceMicros": "0",
   "currency": "KRW"
 },
"transactionTime" : "2022-02-22T12:45:00Z",
 "recurringTransaction" : {
   "externalTransactionToken": "my_token",
   "externalSubscription" {
     "subscriptionType": "RECURRING"
   }
 },
 "userTaxAddress" : {
   "regionCode": "KR"
 }
}
```

Example 2 (unknown):
```unknown
POST /androidpublisher/v3/applications/com.myapp.android/externalTransactions?externalTransactionId=123-456-789

Body
 {
"originalPreTaxAmount" : {
   "priceMicros": "0",
   "currency": "KRW"
 },
 "originalTaxAmount" : {
   "priceMicros": "0",
   "currency": "KRW"
 },
"transactionTime" : "2022-02-22T12:45:00Z",
 "recurringTransaction" : {
   "externalTransactionToken": "my_token",
   "externalSubscription" {
     "subscriptionType": "RECURRING"
   }
 },
 "userTaxAddress" : {
   "regionCode": "KR"
 }
}
```

Example 3 (unknown):
```unknown
POST /androidpublisher/v3/applications/com.myapp.android/externalTransactions?externalTransactionId=123-456-789

Body
 {
"originalPreTaxAmount" : {
   "priceMicros": "0",
   "currency": "INR"
 },
 "originalTaxAmount" : {
   "priceMicros": "0",
   "currency": "INR"
 },
"transactionTime" : "2023-11-01T12:45:00Z",
 "recurringTransaction" : {
   "externalTransactionToken": "my_token",
   "externalSubscription" {
     "subscriptionType": "RECURRING"
   }
 },
 "userTaxAddress" : {
   # Tax varies in India based on state, so include that information in
   # administrativeArea
   "regionCode": "IN"
   "administrativeArea": "KERALA"
 }
}
```

Example 4 (unknown):
```unknown
POST /androidpublisher/v3/applications/com.myapp.android/externalTransactions?externalTransactionId=123-456-789

Body
 {
"originalPreTaxAmount" : {
   "priceMicros": "0",
   "currency": "INR"
 },
 "originalTaxAmount" : {
   "priceMicros": "0",
   "currency": "INR"
 },
"transactionTime" : "2023-11-01T12:45:00Z",
 "recurringTransaction" : {
   "externalTransactionToken": "my_token",
   "externalSubscription" {
     "subscriptionType": "RECURRING"
   }
 },
 "userTaxAddress" : {
   # Tax varies in India based on state, so include that information in
   # administrativeArea
   "regionCode": "IN"
   "administrativeArea": "KERALA"
 }
}
```

---

## 购买生命周期和 RTDN 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/lifecycle

**Contents:**
- 购买生命周期和 RTDN 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 构建实时开发者通知客户端
  - RTDN 发布端
  - RTDN 订阅端
- 处理购买状态转换

当您通过应用销售数字商品时，必须考虑用户体验的方方面面。借助应用内集成，您可以启动购买流程并管理用户体验，但请务必确保您的后端能及时了解用户购买交易的最新权限。这对于跟踪购买交易以及管理用户体验的其他方面（例如跨平台权限）而言非常重要。

如需监控购买生命周期事件并快速响应用户权限的变化，您应该在后端为订阅和一次性购买交易构建购买交易状态管理系统。这个系统可确保无论设备状态如何，都能快速安全地处理购买交易，在所有平台上维持一致的用户权限，并能够在后端查询交易记录和权限数据。

Google Play 提供实时开发者通知 (RTDN)，可监控购买生命周期事件。如需根据这些事件执行必要的操作，请使用适用于订阅和应用内购买的 Play Developer API。只要使用这些工具并构建完善的购买生命周期管理系统，您就可以提供无缝的用户体验，并高效地管理购买交易和权限。

在 Google Play 结算系统上进行的购买交易可能会在其生命周期中发生多次权限更改。许多操作都可能触发这些更改，包括：

后端必须了解购买交易可能会经历的不同状态，并据此采取所有必要的措施来及时调整权限。

虽然可以使用 Google Play Developer API 手动检查购买交易状态，但通过定期检查来跟踪更改，不仅效率不高，并且容易出错和发生延迟。RTDN 有助于您立即响应更改，且无需为 Google Play 购买交易构建生命周期跟踪逻辑。

本部分介绍如何为 RTDN 构建客户端。RTDN 是使用 Google Cloud Pub/Sub 构建的一个功能，可在用户权限状态发生变化时，向后端发送即时通知。Pub/Sub 系统包括发送通知的发布端和订阅通知的客户端。通过实现 RTDN，您可以实时跟踪并及时响应用户权限状态的所有变化。

Google Play 的后端可充当 RTDN 的发布端。如需为您的应用设置 RTDN，请按照设置指南中的说明操作。完成这些步骤后，Google Play 结算系统就能充当您应用的 RTDN 发布端。如需完成此设置，您应熟悉 Google Cloud Platform Console，以设置基本的 Pub/Sub 配置。

设置完发布端之后，您应该为自己的后端做好使用 RTDN 的准备。为此，您需要构建一个客户端来接收 Google Cloud Pub/Sub 消息。RTDN 客户端的基本功能包括接收 PubSubMessage 实例，方法为使用已注册端点中的 HTTPS 请求，或使用 Cloud Pub/Sub 客户端库。如需了解如何使用推送或拉取策略，请参阅 Pub/Sub 文档。如需了解如何选择最符合需求的策略，请参阅 RTDN 设置文档。

对于您收到的每条消息，您的后端都应执行以下操作：

一次性购买和订阅购买交易具有不同的生命周期，具体取决于会影响它们的不同状态和事件。得益于 RTDN，您无需构建逻辑即可确认状态转换。您需要做的是定义后端收到各类通知时会发生的情况。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

---

## 有关替代的应用内购结算系统的临时用户体验指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/alternative/interim-ux/billing-choice?hl=zh-cn

**Contents:**
- 有关替代的应用内购结算系统的临时用户体验指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 概览
- 面向用户的信息
  - 何时显示
  - 何时显示价格
  - 如何显示
  - 用户操作
    - 继续
    - 了解详情
    - 关闭

为了维持一致的用户体验并帮助用户做出明智的选择，您需要显示信息屏幕；如果除了 Google Play 结算系统以外，您还提供替代的应用内购结算系统，则还需要显示单独的结算方式选择屏幕。信息屏幕只需在每位用户首次发起购买交易时向其显示即可，而结算方式选择屏幕应在每次购买交易前向用户显示。应根据以下准则为这两个屏幕实现面向用户的消息和界面规范。

信息屏幕可以帮助用户了解相关更改的背景，并提供更多信息以帮助用户做出明智的选择。

添加替代应用内购结算系统后，应在用户开始进行首次购买交易时向其显示信息屏幕。当同一用户以后再次进行购买交易时，就不需要再显示该信息了。在用户执行明确操作以发起购买交易之后，系统应立即显示信息屏幕。

应在显示信息屏幕或结算方式选择屏幕之前，在显眼的位置向用户显示购买价格。

信息屏幕应显示在模态底部动作条中。模态底部动作条与模态对话框类似，它会从屏幕底部向上呈现动画效果，并固定在屏幕底部。它位于底层屏幕中的所有界面元素的上层。底层屏幕会被深色纱罩遮挡，以表示它不会响应用户互动。

如需详细了解模态底部动作条的设计和实现，请参阅 Google Material Design。

当用户点按应用中用于发起购买交易的按钮或其他界面元素时，底部动作条应触发。用户可以在信息屏幕中执行 3 种可能的操作：

点按“继续”按钮会关闭信息屏幕，并启动结算方式选择屏幕。

点按“了解详情”按钮可在网络浏览器中打开相应的 Google 帮助中心文章。

如果用户要关闭底部动作条并返回底层屏幕，可以通过以下方式关闭底部动作条：

在用户关闭信息屏幕或点按“继续”后，无需再次显示信息屏幕。

示例：在用户发起购买交易之前，购买交易已明确显示。点按“立即加入”按钮会触发信息屏幕。

信息屏幕分为 3 个组件：标题、消息和按钮。所有这 3 个组件都是必需的，其包含的文字和界面元素必须与本准则中的定义完全一致。请勿在该屏幕中添加任何其他文字或图像，但您可以在其他屏幕中添加额外的文字和图像。

在横向视图中，底部动作条的宽度大于纵向视图中的宽度，但在其他方面都遵循相同的设计规范和功能。

结算方式选择界面向用户展示两种结账选项，用于完成购买交易。为了帮助用户做出明智的决策，每个结算服务选项还会向用户显示可用的付款方式。在用户做出选择后，他们将继续通过所选的结算服务完成购买交易。

如果用户已查看过信息屏幕，则在其执行明确操作以发起购买交易后，系统应立即显示结算方式选择屏幕。

结算方式选择屏幕应该显示在模态底部动作条中，并遵循与信息屏幕相同的规范。

您应该采用公平且均等的方式来展示其他应用内购结算系统的按钮和 Google Play 结算服务的按钮。这包括但不限于相同的按钮大小、文字大小/样式、点按目标和图标大小。请勿添加本指南中未定义的任何其他文字、图片或样式更改。

示例：点按“立即加入”按钮会触发结算方式选择屏幕。

结算方式选择屏幕包含 4 个不同的组件：标题、说明、开发者按钮和 Google Play 按钮。您应使用所有组件，并且这些组件包含的文字和界面元素应与本准则中的定义完全一致。请勿在该屏幕中添加任何其他文字或图像，但您可以在您拥有的其他屏幕中添加其他文字和图像。

您可以通过以下链接获取 Google Play 的可视化资源和付款图标。

示例：在纵向视图中，底部动作条的跨度应该与屏幕总宽度相等。

示例：在横向视图中，底部动作条的宽度大于纵向视图中的宽度，但在其他方面都遵循相同的设计规范和功能。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

---

## 适用于欧洲经济区 (EEA) 计划的无需用户自选的其他结算方式临时用户体验指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/alt-billing?hl=zh-cn

**Contents:**
- 适用于欧洲经济区 (EEA) 计划的无需用户自选的其他结算方式临时用户体验指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 概览
- 选择语言
- 面向用户的信息
  - 何时显示
  - 何时显示价格
  - 如何显示
  - 用户操作
    - 知道了
    - 了解详情

这些指南面向参与我们计划的开发者，用于向欧洲经济区 (EEA) 的用户提供 Google Play 结算系统之外的其他结算方式，但无需用户自行选择。如果开发者有欧洲经济区 (EEA) 境内的用户，并且参与了用户自选结算方式试行计划，且除了 Google Play 结算系统之外还提供备选结算系统，则应遵循用户自选结算方式用户体验指南。这些用户体验指南旨在要求开发者在每位用户首次发起购买交易时向其显示信息屏幕，从而保持一致的用户体验。应按照以下准则为信息屏幕实现面向用户的消息和界面规范。

选择用户的语言，以便在以下设计规范中查看对应的界面文本字符串。

信息屏幕必须在用户开始进行首次购买时向其显示。当同一用户以后再次进行购买交易时，就不需要再显示该信息了。在用户执行明确操作以发起购买交易之后，系统应立即显示信息屏幕。

应在显示信息屏幕之前，在显眼的位置向用户显示购买价格。

信息屏幕必须显示在模态底部动作条中。模态底部动作条与模态对话框类似，它会从屏幕底部向上呈现动画效果，并固定在屏幕底部。它位于底层屏幕中的所有界面元素的上层。底层屏幕会被深色纱罩遮挡，表示它不会响应用户的任何互动。

如需详细了解模态底部动作条的设计和实现，请参阅 Google Material Design。

当用户点按应用中用于发起购买交易的按钮或其他界面元素时，底部动作条必须触发。用户可以在信息屏幕中执行 2 种可能的操作：

点按“知道了”按钮会关闭信息屏幕，并启动付款流程中的下一个屏幕。

点按“了解详情”按钮可在网络浏览器中打开相应的 Google 帮助中心文章。

如果用户要关闭底部动作条并返回底层屏幕，可以通过以下方式关闭底部动作条：

在用户关闭信息屏幕或点按“知道了”后，无需再次显示信息屏幕。

示例：当用户在应用中点按进行购买时，该按钮会触发信息屏幕。

信息屏幕分为 3 个组件：标题、消息和按钮。所有这 3 个组件都是必需的，其包含的文字和界面元素必须与本指南中的定义完全一致。请勿在该屏幕中添加任何其他文字或图像，但您可以在其他屏幕中添加额外的文字和图像。

在横向视图中，底部动作条的宽度大于纵向视图中的宽度，但在其他方面都遵循相同的设计规范和功能。

如需进一步了解适用于欧洲经济区 (EEA) 计划的无需用户自选的其他结算方式和常见问题解答，请访问我们的帮助中心。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

---

## 有关用户自选结算方式试行计划的临时用户体验指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/alternative/interim-ux/user-choice

**Contents:**
- 有关用户自选结算方式试行计划的临时用户体验指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 概览
- 选择国家/地区和语言
- 面向用户的信息
  - 何时显示
  - 何时显示价格
  - 如何显示
  - 用户操作
    - 继续
    - 了解详情

参与用户自选结算方式试行计划的开发者可在提供 Google Play 结算系统的同时，测试提供备选结算系统。该计划旨在帮助我们了解为用户提供这种选择的效果。这些用户体验指南旨在确保提供一致的用户体验，并帮助用户做出明智的决策。

如果您参与该试行计划，则需要显示一个信息界面和一个单独的结算方式选择界面。信息屏幕只需在每位用户首次发起购买交易时向其显示，而结算方式选择屏幕则必须在每次购买交易前都向用户显示。必须根据以下准则为这两个屏幕实现面向用户的消息和界面规范。

选择用户的国家/地区和语言，以便在以下设计规范中查看对应的界面文本字符串。

信息屏幕可以帮助用户了解相关更改的背景，并提供更多信息以帮助用户做出明智的选择。

添加备选结算系统后，必须在用户开始进行首次购买交易时向其显示信息屏幕。当同一用户以后再次进行购买交易时，就不需要再显示该信息了。在用户执行明确操作以发起购买交易之后，系统应立即显示信息屏幕。

必须在显示信息屏幕或结算方式选择屏幕之前，在显眼的位置向用户显示购买价格。

信息屏幕必须显示在模态底部动作条中。模态底部动作条与模态对话框类似，它会从屏幕底部向上呈现动画效果，并固定在屏幕底部。它位于底层屏幕中的所有界面元素的上层。底层屏幕会被深色纱罩遮挡，表示它不会响应用户的任何互动。

如需详细了解模态底部动作条的设计和实现，请参阅 Google Material Design。

当用户点按应用中用于发起购买交易的按钮或其他界面元素时，底部动作条应触发。用户可以在信息屏幕中执行三种可能的操作：

点按“继续”按钮会关闭信息屏幕，并启动结算方式选择屏幕。

点按“了解详情”按钮可在网络浏览器中打开相应的 Google 帮助中心文章。

如果用户要关闭底部动作条并返回底层屏幕，可以通过以下方式关闭底部动作条：

在用户关闭信息屏幕或点按“继续”后，无需再次显示信息屏幕。

示例：当用户在应用中点按进行购买时，该按钮会触发信息屏幕。

信息屏幕分为 3 个组件：标题、消息和按钮。所有这 3 个组件都是必需的，其包含的文字和界面元素必须与本指南中的定义完全一致。请勿在该屏幕中添加任何其他文字或图像，但您可以在其他屏幕中添加额外的文字和图像。

在横向视图中，底部动作条的宽度大于纵向视图中的宽度，但在其他方面都遵循相同的设计规范和功能。

结算方式选择界面向用户展示两种结账选项，用于完成购买交易。为了帮助用户做出明智的决策，每个结算服务选项还会向用户显示可用的付款方式。在用户做出选择后，他们将继续通过所选的结算系统完成购买交易。

如果用户已在之前的购买交易中查看过信息屏幕，则在其执行明确操作以发起购买交易后，系统应立即显示结算方式选择屏幕。

结算方式选择屏幕必须显示在模态底部动作条中，并遵循与信息屏幕相同的规范。

应以公平、均等的方式呈现备选结算系统和 Google Play 结算系统的按钮。这包括但不限于相同的按钮大小、文字大小/样式、点按目标和图标大小。请勿添加本指南中未定义的任何其他文字、图片或样式更改。

示例：当用户在应用中点按进行购买时，只有当用户已在之前的购买交易中查看过信息屏幕时，该按钮才会触发结算方式选择屏幕。

结算方式选择屏幕包含 4 个不同的组件：标题、说明、开发者按钮和 Google Play 按钮。您必须使用所有组件，并且这些组件包含的文字和界面元素必须与本指南中的定义完全一致。请勿在该屏幕中添加任何其他文字或图像，但您可以在您拥有的其他屏幕中添加其他文字和图像。

您可以通过以下链接获取 Google Play 的可视化资源和付款图标。

示例：在纵向视图中，底部动作条的跨度应该与屏幕总宽度相等。

示例：在横向视图中，底部动作条的宽度大于纵向视图中的宽度，但在其他方面都遵循相同的设计规范和功能。

如需进一步了解用户自选结算方式试行计划和常见问题解答，请访问我们的帮助中心。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

---

## 将 Google Play 与服务器后端集成 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/backend

**Contents:**
- 将 Google Play 与服务器后端集成 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 自动化数字商品清单管理
- 购买生命周期管理和授权同步
- 防范欺诈和滥用行为
- 自动化财务对账和报告
- 外部交易管理

在通过 Google Play 管理应用的应用内购买交易方面，您的安全服务器后端发挥着重要作用。借助 Google Play 结算系统，您可以管理数字商品业务的最重要方面，包括从设置清单到跟踪交易。

Google Play Developer API 包含多个端点，可让您的后端与 Google Play 后端保持同步。尤其是 Subscriptions and In-App Purchases API 可处理与 Google Play 上的数字商品销售相关的功能。

在许多使用情形中，在后端集成数字商品清单管理集成可能会非常有用。例如，通过此集成，您可以执行以下操作：

您可以使用 monetization.subscriptions 和 inappproducts 端点来管理您的数字商品清单。

如需快速准确地响应用户权限的变化，请务必监控购买生命周期事件。您应针对订阅和一次性购买交易，将购买状态管理构建到后端中，确保您的所有购买交易都安全无虞，且所有权限都保持一致。

Google Play 结算系统会为这两类购买交易发送实时开发者通知 (RTDN)，您的后端应准备好导入这些消息并做出必要更改。如需了解如何利用 RTDN 客户端和 Google Play Developer API 来管理您的购买生命周期，请参阅购买生命周期指南。

请将敏感逻辑移至后端并监控 Google Play 上的已作废购买交易，以防范滥用行为。Google Play Developer API 提供多项功能，可确认新的购买交易、消耗应用内商品购买交易并处理已作废购买交易。如需详细了解如何防范欺诈和滥用行为，请参阅打击欺诈和滥用行为。

您可以通过下载 Play 管理中心报告，从 Google Play 导入报告数据。您可以利用 Google Cloud Storage API 下载 Play 管理中心为您提供的信息，以解决与此信息相关的任何用例。

如果您要集成备选结算系统或外部优惠 API，请使用 Externaltransactions APIs 报告和管理已完成的交易。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

---

## 有关 Google Play 结算服务之外的变现的后端集成指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/outside-gpb-backend

**Contents:**
- 有关 Google Play 结算服务之外的变现的后端集成指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 向 Google Play 报告新的外部交易
  - 外部交易报告
  - 报告新购买交易
  - 报告购买交易的后续交易
  - 报告升级或降级
  - 停止手动报告备选结算系统交易
  - 举报 Play 合作伙伴计划
- 向 Google Play 报告购买交易退款
- API 配额

Google Play Developer API 现在包含 报告来自备选结算系统的交易，或 外部优惠系统。本指南将介绍如何报告替代性数据， 结算或外部优惠交易。

从后端处理应用内购买交易时，可能需要用到一些组件。如需构建这些组件，您需要按照配置 Google Play Developer API 中的说明设置后端集成。对于 所有不特定于备选结算系统的开发者后端功能 或外部优惠 API 的说明， Google Play 结算系统文档适用。

与 Externaltransactions APIs 集成 报告 Google Play 结算系统以外发生的交易， 支持的国家/地区，包括通过免费试用产生的 0 美元交易 购买。通过备选结算系统或外部优惠系统进行的交易 仅在系统允许的情况下，才应针对符合条件的用户所在国家/地区启动和报告 在备选结算系统下，或者 外部优惠计划，否则，API 调用将 已被拒绝。这适用于所有交易，包括新购买、续订 充值、升级、降级等操作。

您应该调用 Externaltransactions API 来报告外部交易 在通过备选结算系统获得授权后，或者 外部优惠系统这适用于所有交易，包括 扣款、续订、退款等。所有交易都必须 会在交易发生 24 小时内报告。

系统会为每一笔外部交易报告一个外部交易 ID。对于周期性购买交易（例如自动续订型订阅），您需要发送与这笔周期性购买交易中的第一笔交易相关联的外部交易 ID，以用作后续所有交易（包括退款）的参数。这样就能记录相应购买交易的一系列交易。如果商品发生变化（例如升级或降级），或者周期性交易被取消或过期且之后同一商品再次被购买，您就需要针对相应交易发送新的外部交易 ID。您不得添加任何个人身份信息 这些信息、专有信息或机密信息， 交易 ID。

每当通过备选结算系统完成新购买交易时 或外部优惠系统，对 Externaltransactions API 的调用会 必填字段。对于这些新的购买交易，您需要提供唯一 externalTransactionId 以查询的形式与后端中的购买交易相关联 参数。此externalTransactionId不能在同一应用的 软件包 ID。

应用通过externalTransactionToken UserChoiceBillingListener、AlternativeBillingOnlyReportingDetailsListener、 或 ExternalOfferReportingDetailsListener 回调作为 一次性购买和首次交易的请求正文 周期性购买（例如订阅）。无论是哪种情况，都称为 初始交易。完成初始交易后， externalTransactionToken 不再需要，您后续报告 通过提供新的唯一身份 externalTransactionId。请参阅报告购买交易的后续交易 ，详细了解如何报告后续交易。

如果与印度境内的用户进行交易，由于该国税费因用户所在的行政区（例如州或省）而异，请务必在 userTaxAddress 下包含该行政区。如需了解适用的行政区，请参阅 API 参考指南中的预定义字符串列表。

在某些情况下，同一外部购买交易有多笔相关联的用户付款（例如，续订或预付费方案充值）。您可以在 Externaltransactions 中使用同一 API 报告这些后续交易。如报告新购买交易中所述，后续交易不需要 externalTransactionToken。不过，系统会为每笔续订或充值交易发送新的唯一 externalTransactionId 作为查询参数，并将初始交易的 ID 包含在 initialExternalTransactionId 字段中。

若要当用户拥有一项订阅的情况下在备选结算系统中报告升级或降级，您可在 Externaltransactions API 中使用相同的端点和函数，发送为升级或降级交易而提供给应用的 externalTransactionToken。这与报告新购买交易类似。

如需迁移您以非自动化报告方式提供备选结算系统期间开始的有效订阅，请使用 migratedTransactionProgram 字段（而不是指定 initialExternalTransactionId 或 externalTransactionToken）创建一笔新的 0 费用交易。将每项有效订阅的 transactionTime 设置为用户最初注册该订阅的时间。之后，照常通过 API 报告这些订阅的每一笔后续交易，并提供之前使用的 initialExternalTransactionId 创建续订交易。迁移订阅后，您无需再手动报告订阅的后续交易，但前提是这些交易是通过本页介绍的自动化方式报告的。

迁移订阅时，请留意当前的配额限制，以确保迁移不会用尽配额。如果有很多订阅需要 分几天进行迁移，或申请提高配额 配额 ，了解所有最新动态。

只有在从手动报告迁移时，才可以使用 migratedTransactionProgram 字段。当手动报告不再受支持后，该字段将被废弃。

参与合作伙伴计划（例如 Play 媒体体验计划必须提供 transaction_program_code（报告外部交易时）。如果您 如果您是符合条件的开发者，请与您的业务发展经理联系以了解详情 了解如何设置此字段。

与 Externaltransactions API 集成后，您可报告在 Google Play 结算系统以外向用户退款的交易。为了让 Play 正确识别哪一笔交易已退款，您应将之前所报告交易的相应 externalTransactionId 添加为网址参数的一部分。

报告订阅购买交易的退款时，请引用被退款订阅的具体周期性交易的 externalTransactionId。

如需报告该订阅所有交易的退款，您需要发出三个单独的退款请求：一个针对初始交易，两个针对后续交易。

此方法接受全额退款 （其中金额与用户在原始外部 交易）和部分退款 （金额小于用户在原始外部 交易）。对于部分退款，您需要指定退还的税前金额。

Externaltransactions API 受每日 API 配额限制 就像 Google Play Developer API 中的任何其他端点一样。

此外，在调用 Externaltransactions.createexternaltransaction 或 Externaltransactions.refundexternaltransaction 时，Externaltransactions API 的每分钟查询数量 (QPM) 上限为 1,200 个。对 Externaltransactions.getexternaltransaction 的调用不会计入此 1,200 QPM 的限额。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

**Examples:**

Example 1 (unknown):
```unknown
POST /androidpublisher/v3/applications/com.myapp.android/externalTransactions?externalTransactionId=123-456-789

Body
 {
"originalPreTaxAmount" : {
   "priceMicros": "0",
   "currency": "KRW"
 },
 "originalTaxAmount" : {
   "priceMicros": "0",
   "currency": "KRW"
 },
"transactionTime" : "2022-02-22T12:45:00Z",
 "recurringTransaction" : {
   "externalTransactionToken": "my_token",
   "externalSubscription" {
     "subscriptionType": "RECURRING"
   }
 },
 "userTaxAddress" : {
   "regionCode": "KR"
 }
}
```

Example 2 (unknown):
```unknown
POST /androidpublisher/v3/applications/com.myapp.android/externalTransactions?externalTransactionId=123-456-789

Body
 {
"originalPreTaxAmount" : {
   "priceMicros": "0",
   "currency": "KRW"
 },
 "originalTaxAmount" : {
   "priceMicros": "0",
   "currency": "KRW"
 },
"transactionTime" : "2022-02-22T12:45:00Z",
 "recurringTransaction" : {
   "externalTransactionToken": "my_token",
   "externalSubscription" {
     "subscriptionType": "RECURRING"
   }
 },
 "userTaxAddress" : {
   "regionCode": "KR"
 }
}
```

Example 3 (unknown):
```unknown
POST /androidpublisher/v3/applications/com.myapp.android/externalTransactions?externalTransactionId=123-456-789

Body
 {
"originalPreTaxAmount" : {
   "priceMicros": "0",
   "currency": "INR"
 },
 "originalTaxAmount" : {
   "priceMicros": "0",
   "currency": "INR"
 },
"transactionTime" : "2023-11-01T12:45:00Z",
 "recurringTransaction" : {
   "externalTransactionToken": "my_token",
   "externalSubscription" {
     "subscriptionType": "RECURRING"
   }
 },
 "userTaxAddress" : {
   # Tax varies in India based on state, so include that information in
   # administrativeArea
   "regionCode": "IN"
   "administrativeArea": "KERALA"
 }
}
```

Example 4 (unknown):
```unknown
POST /androidpublisher/v3/applications/com.myapp.android/externalTransactions?externalTransactionId=123-456-789

Body
 {
"originalPreTaxAmount" : {
   "priceMicros": "0",
   "currency": "INR"
 },
 "originalTaxAmount" : {
   "priceMicros": "0",
   "currency": "INR"
 },
"transactionTime" : "2023-11-01T12:45:00Z",
 "recurringTransaction" : {
   "externalTransactionToken": "my_token",
   "externalSubscription" {
     "subscriptionType": "RECURRING"
   }
 },
 "userTaxAddress" : {
   # Tax varies in India based on state, so include that information in
   # administrativeArea
   "regionCode": "IN"
   "administrativeArea": "KERALA"
 }
}
```

---

## 仅适用于备选结算系统的应用内集成指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/alternative/alternative-billing-without-user-choice-in-app?hl=zh-cn

**Contents:**
- 仅适用于备选结算系统的应用内集成指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- Play 结算库设置
- 连接到 Google Play
  - Kotlin
  - Java
- 检查可用性
  - Kotlin
  - Java
- 面向用户的信息对话框
  - Kotlin

本指南介绍了如何集成相关 API，以便在符合条件的应用中提供仅限备选结算系统（即无需用户自选）的结算方式。如需详细了解相关计划（包括资格要求和地理范围），请参阅备选结算系统简介。

向您的 Android 应用添加 Play 结算库依赖项。如需使用备选结算系统 API，您需要使用 6.1 或更高版本。

集成流程的最初步骤与 Google Play 结算服务集成指南中所述的一些步骤相同，在初始化您的 BillingClient 时需进行一些调整：

以下示例演示了如何通过这些调整来初始化 BillingClient：

初始化 BillingClient 后，您需要按照集成指南中的说明与 Google Play 建立连接。

您的应用应通过调用 isAlternativeBillingOnlyAvailableAsync 来确认可以使用仅限备选结算系统的结算方式。

如果可以使用仅限备选结算系统的结算方式，此 API 将返回 BillingResponseCode.OK。如需详细了解您的应用应如何响应其他响应代码，请参阅响应处理部分。

如需集成仅限备选结算系统的结算方式，符合条件的应用必须显示一个信息界面，以帮助用户了解结算将不受 Google Play 的管理。每次启动备选结算流程之前，必须通过调用 showAlternativeBillingOnlyInformationDialog API 向用户显示此信息界面。如果用户已确认该对话框，此 API 通常不会再次显示该对话框。但在某些情况下（例如用户清除了设备上的缓存），系统可能会再次向用户显示该对话框。

如果此方法返回 BillingResponseCode.OK，您的应用可以继续进行交易。如果返回 BillingResponseCode.USER_CANCELED，您的应用应调用 showAlternativeBillingOnlyInformationDialog 以再次向用户显示该对话框。如需了解其他响应代码，请参阅“响应处理”部分。

通过备选结算系统进行的所有交易都必须在 24 小时内从后端调用 Google Play Developer API 并提供 externalTransactionToken（使用下文介绍的 API 获取），向 Google Play 报告相应交易。每笔一次性购买交易、每项新订阅以及对现有订阅的任何升级/降级都应生成新的 externalTransactionToken。如需了解在获取 externalTransactionToken 后如何报告交易，请参阅后端集成指南。

如果出现错误，上述方法 isAlternativeBillingOnlyAvailableAsync(), showAlternativeBillingOnlyInformationDialog() 和 createAlternativeBillingOnlyReportingDetailsAsync() 可能会返回非 BillingResponseCode.OK 响应。建议按如下所述的方法处理错误：

许可测试人员应该用于测试备选结算系统集成。您 对于许可测试人员发起的交易，系统不会开具账单 账号。如需了解详情，请参阅使用应用许可测试应用内购结算功能 了解如何配置许可测试人员

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

**Examples:**

Example 1 (unknown):
```unknown
var billingClient = BillingClient.newBuilder(context)
    .enableAlternativeBillingOnly()
    .build()
```

Example 2 (unknown):
```unknown
var billingClient = BillingClient.newBuilder(context)
    .enableAlternativeBillingOnly()
    .build()
```

Example 3 (unknown):
```unknown
private BillingClient billingClient = BillingClient.newBuilder(context)
    .enableAlternativeBillingOnly()
    .build();
```

Example 4 (unknown):
```unknown
private BillingClient billingClient = BillingClient.newBuilder(context)
    .enableAlternativeBillingOnly()
    .build();
```

---

## 适用于欧洲经济区 (EEA) 计划的无需用户自选的其他结算方式临时用户体验指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/alternative/interim-ux/alt-billing

**Contents:**
- 适用于欧洲经济区 (EEA) 计划的无需用户自选的其他结算方式临时用户体验指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 概览
- 选择语言
- 面向用户的信息
  - 何时显示
  - 何时显示价格
  - 如何显示
  - 用户操作
    - 知道了
    - 了解详情

这些指南面向参与我们计划的开发者，用于向欧洲经济区 (EEA) 的用户提供 Google Play 结算系统之外的其他结算方式，但无需用户自行选择。如果开发者有欧洲经济区 (EEA) 境内的用户，并且参与了用户自选结算方式试行计划，且除了 Google Play 结算系统之外还提供备选结算系统，则应遵循用户自选结算方式用户体验指南。这些用户体验指南旨在要求开发者在每位用户首次发起购买交易时向其显示信息屏幕，从而保持一致的用户体验。应按照以下准则为信息屏幕实现面向用户的消息和界面规范。

选择用户的语言，以便在以下设计规范中查看对应的界面文本字符串。

信息屏幕必须在用户开始进行首次购买时向其显示。当同一用户以后再次进行购买交易时，就不需要再显示该信息了。在用户执行明确操作以发起购买交易之后，系统应立即显示信息屏幕。

应在显示信息屏幕之前，在显眼的位置向用户显示购买价格。

信息屏幕必须显示在模态底部动作条中。模态底部动作条与模态对话框类似，它会从屏幕底部向上呈现动画效果，并固定在屏幕底部。它位于底层屏幕中的所有界面元素的上层。底层屏幕会被深色纱罩遮挡，表示它不会响应用户的任何互动。

如需详细了解模态底部动作条的设计和实现，请参阅 Google Material Design。

当用户点按应用中用于发起购买交易的按钮或其他界面元素时，底部动作条必须触发。用户可以在信息屏幕中执行 2 种可能的操作：

点按“知道了”按钮会关闭信息屏幕，并启动付款流程中的下一个屏幕。

点按“了解详情”按钮可在网络浏览器中打开相应的 Google 帮助中心文章。

如果用户要关闭底部动作条并返回底层屏幕，可以通过以下方式关闭底部动作条：

在用户关闭信息屏幕或点按“知道了”后，无需再次显示信息屏幕。

示例：当用户在应用中点按进行购买时，该按钮会触发信息屏幕。

信息屏幕分为 3 个组件：标题、消息和按钮。所有这 3 个组件都是必需的，其包含的文字和界面元素必须与本指南中的定义完全一致。请勿在该屏幕中添加任何其他文字或图像，但您可以在其他屏幕中添加额外的文字和图像。

在横向视图中，底部动作条的宽度大于纵向视图中的宽度，但在其他方面都遵循相同的设计规范和功能。

如需进一步了解适用于欧洲经济区 (EEA) 计划的无需用户自选的其他结算方式和常见问题解答，请访问我们的帮助中心。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

---

## Google Play 结算库版本废弃 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/deprecation-faq

**Contents:**
- Google Play 结算库版本废弃 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 不同版本的支持时间表

正如 2019 年 Google I/O 大会和 Google Play 结算库版本 3 博文所宣布的，所有版本的 Play 结算库都将遵循两年的废弃周期。

本主题回答了关于结算库版本废弃和迁移到更高版本的常见问题。

将您版本中的依赖项更新为使用表中指示的支持版本。如需了解各版本之间有哪些变化，请参阅版本说明。

此外，我们还提供了关于如何迁移到 PBL 8 的深度指南。

如果我想在 11 月 1 日之前继续向所有 Google Play 用户分发应用，在哪里可以找到延期表单？

如果您的应用仍在使用已过时的 Play 结算库版本，您将在 Play 管理中心内收到警告和收件箱消息。可通过相应警告或问题的详情页面（位于 Play 管理中心的政策状态页面）找到延期表单。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

---

## 弃用 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/play-developer-apis-deprecations

**Contents:**
- 弃用 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 废弃时间表 - 2025 年 5 月 21 日至 2027 年 8 月 31 日
  - 已废弃的订阅 API
  - 周期性订阅的 SubscriptionPurchaseV2 字段
  - 其他订阅管理函数

本文档列出了处于弃用期的 Google Play Developer API 和相关功能。

本部分中的功能和 API 自 2025 年 5 月 21 日起已被弃用，并将于 2027 年 8 月 31 日关停。不过，您可以申请延长已废弃商品的使用期限，最晚可延至 2027 年 11 月 1 日。

purchases.subscriptionv2 包含一些新字段，用于提供有关新订阅对象的更多详细信息。下表显示了旧订阅端点中的字段与 purchases.subscriptionv2 中相应字段的对应关系。

虽然 purchases.subscriptions:get 已升级到 purchases.subscriptionsv2:get，但 purchases.subscriptions 端点中的其余开发者订阅管理函数目前保持不变，因此您可以像以前一样继续使用 purchases.subscriptions:acknowledge、purchases.subscriptions:cancel、purchases.subscriptions:defer、purchases.subscriptions:refund 和 purchases.subscriptions:revoke。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

---

## Google Play Developer API 版本说明 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/play-developer-apis-release-notes

**Contents:**
- Google Play Developer API 版本说明 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 2025 年 11 月 19 日
  - 新功能
- 2025 年 9 月 11 日
  - 新功能
- 2025 年 6 月 30 日
  - 新功能
- 2025 年 5 月 21 日
  - 废弃
  - 新功能

本文档包含 Google Play Developer API 的版本说明。

SubscriptionPurchaseV2 中现在提供 SubscriptionPurchaseLineItem.itemReplacement 字段，用于提供有关被替换商品的详细信息（如果适用）。

Orders API 现在包含 offerPhaseDetails 字段，可提供有关按比例分摊时段的订单资金的更详细信息。

目前，这些新功能仅通过 API 提供，而不通过客户端库提供。

SubscriptionPurchaseV2 API 现在提供 cancel 方法。

此方法通过在客户端库中引入对 cancellationType 参数的支持，增强了现有的 purchases.subscriptions.cancel 功能。

SubscriptionPurchaseV2 中添加了一个新字段：SubscriptionPurchaseLineItem.auto_renewing_plan.price_step_up_consent_details。

新增了实时开发者通知类型 SUBSCRIPTION_PRICE_STEP_UP_CONSENT_UPDATED。

SubscriptionPurchaseV2 中提供了以下新字段：

subscriptionsv2.revoke 方法现在提供 item_based_refund 选项。

Orders API 现在提供 get 和 batchGet 方法。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-11-19。

---

## 有关用户自选结算方式试行计划的临时用户体验指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/alternative/interim-ux/user-choice?hl=zh-cn

**Contents:**
- 有关用户自选结算方式试行计划的临时用户体验指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 概览
- 选择国家/地区和语言
- 面向用户的信息
  - 何时显示
  - 何时显示价格
  - 如何显示
  - 用户操作
    - 继续
    - 了解详情

参与用户自选结算方式试行计划的开发者可在提供 Google Play 结算系统的同时，测试提供备选结算系统。该计划旨在帮助我们了解为用户提供这种选择的效果。这些用户体验指南旨在确保提供一致的用户体验，并帮助用户做出明智的决策。

如果您参与该试行计划，则需要显示一个信息界面和一个单独的结算方式选择界面。信息屏幕只需在每位用户首次发起购买交易时向其显示，而结算方式选择屏幕则必须在每次购买交易前都向用户显示。必须根据以下准则为这两个屏幕实现面向用户的消息和界面规范。

选择用户的国家/地区和语言，以便在以下设计规范中查看对应的界面文本字符串。

信息屏幕可以帮助用户了解相关更改的背景，并提供更多信息以帮助用户做出明智的选择。

添加备选结算系统后，必须在用户开始进行首次购买交易时向其显示信息屏幕。当同一用户以后再次进行购买交易时，就不需要再显示该信息了。在用户执行明确操作以发起购买交易之后，系统应立即显示信息屏幕。

必须在显示信息屏幕或结算方式选择屏幕之前，在显眼的位置向用户显示购买价格。

信息屏幕必须显示在模态底部动作条中。模态底部动作条与模态对话框类似，它会从屏幕底部向上呈现动画效果，并固定在屏幕底部。它位于底层屏幕中的所有界面元素的上层。底层屏幕会被深色纱罩遮挡，表示它不会响应用户的任何互动。

如需详细了解模态底部动作条的设计和实现，请参阅 Google Material Design。

当用户点按应用中用于发起购买交易的按钮或其他界面元素时，底部动作条应触发。用户可以在信息屏幕中执行三种可能的操作：

点按“继续”按钮会关闭信息屏幕，并启动结算方式选择屏幕。

点按“了解详情”按钮可在网络浏览器中打开相应的 Google 帮助中心文章。

如果用户要关闭底部动作条并返回底层屏幕，可以通过以下方式关闭底部动作条：

在用户关闭信息屏幕或点按“继续”后，无需再次显示信息屏幕。

示例：当用户在应用中点按进行购买时，该按钮会触发信息屏幕。

信息屏幕分为 3 个组件：标题、消息和按钮。所有这 3 个组件都是必需的，其包含的文字和界面元素必须与本指南中的定义完全一致。请勿在该屏幕中添加任何其他文字或图像，但您可以在其他屏幕中添加额外的文字和图像。

在横向视图中，底部动作条的宽度大于纵向视图中的宽度，但在其他方面都遵循相同的设计规范和功能。

结算方式选择界面向用户展示两种结账选项，用于完成购买交易。为了帮助用户做出明智的决策，每个结算服务选项还会向用户显示可用的付款方式。在用户做出选择后，他们将继续通过所选的结算系统完成购买交易。

如果用户已在之前的购买交易中查看过信息屏幕，则在其执行明确操作以发起购买交易后，系统应立即显示结算方式选择屏幕。

结算方式选择屏幕必须显示在模态底部动作条中，并遵循与信息屏幕相同的规范。

应以公平、均等的方式呈现备选结算系统和 Google Play 结算系统的按钮。这包括但不限于相同的按钮大小、文字大小/样式、点按目标和图标大小。请勿添加本指南中未定义的任何其他文字、图片或样式更改。

示例：当用户在应用中点按进行购买时，只有当用户已在之前的购买交易中查看过信息屏幕时，该按钮才会触发结算方式选择屏幕。

结算方式选择屏幕包含 4 个不同的组件：标题、说明、开发者按钮和 Google Play 按钮。您必须使用所有组件，并且这些组件包含的文字和界面元素必须与本指南中的定义完全一致。请勿在该屏幕中添加任何其他文字或图像，但您可以在您拥有的其他屏幕中添加其他文字和图像。

您可以通过以下链接获取 Google Play 的可视化资源和付款图标。

示例：在纵向视图中，底部动作条的跨度应该与屏幕总宽度相等。

示例：在横向视图中，底部动作条的宽度大于纵向视图中的宽度，但在其他方面都遵循相同的设计规范和功能。

如需进一步了解用户自选结算方式试行计划和常见问题解答，请访问我们的帮助中心。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

---

## 一次性购买生命周期 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/lifecycle/one-time

**Contents:**
- 一次性购买生命周期 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 新的一次性商品购买交易
  - 实时开发者通知
  - 处理已完成的交易
  - 处理已取消的交易
- 在后端处理一次性商品购买交易

相较于订阅商品，一次性购买商品的生命周期更为简单，但您的后端仍然需要能够妥善处理多种状态和转换事件。

用户完成结算流程后，您的应用可以通过以下方式之一查看新购买交易的相关信息：

收到新的购买交易后，请使用 getPurchaseState 方法或 purchases.productsv2.getproductpurchasev2 in Play Developer API

当用户购买或取消购买一次性商品时，Google Play 会发送 OneTimeProductNotification 消息。如需更新后端购买交易状态，请使用 OneTimeProductNotification 对象中提供的购买令牌来调用 purchases.productsv2.getproductpurchasev2 方法。此方法可提供指定购买令牌的最新购买和消费状态。

当预订商品完成配送且其购买状态更改为 PURCHASED 时，系统会向您的客户端发送 RTDN。收到 RTDN 后，请按照在后端处理一次性商品购买交易中所述的方式处理预订购买交易。

您应在安全的后端中处理与交易相关的 RTDN。

当用户完成一次性商品购买交易时，Google Play 会发送一条类型为 ONE_TIME_PRODUCT_PURCHASED 的 OneTimeProductNotification 消息。收到此 RTDN 后，请按照在后端处理一次性商品购买交易中所述的方式处理购买交易。

如果您已配置为接收实时开发者通知，那么当一次性商品购买交易被取消时，Google Play 会发送一条类型为 ONE_TIME_PRODUCT_CANCELED 的 OneTimeProductNotification 消息。例如，如果用户未在规定的时间范围内完成付款，或者开发者或客户请求撤消购买交易，就可能会发生这种情况。当您的后端服务器收到此通知时，请调用 purchases.productsv2.getproductpurchasev2 方法来获取最新的购买交易状态，然后据此更新后端，包括用户权限。

如果处于 Purchased 状态的一次性商品购买交易发生退款，您也会通过 Voided Purchases API 获知。

无论您是通过 ONE_TIME_PRODUCT_PURCHASED RTDN 检测新的购买交易，通过 PurchasesUpdatedListener 获知应用内购买交易，还是在应用内以 onResume() 方法手动提取购买交易，您都必须处理新的购买交易。我们建议您在后端处理购买交易，以提高安全性。

如要处理新的一次性购买交易，请按以下步骤操作：

Play 结算库中还提供了购买交易确认和消耗方法，可让您通过应用处理购买交易，但如果您可以在后端进行处理，我们建议您采用这种更安全的实现方法。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

---

## 弃用 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/play-developer-apis-deprecations?hl=zh-cn

**Contents:**
- 弃用 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 废弃时间表 - 2025 年 5 月 21 日至 2027 年 8 月 31 日
  - 已废弃的订阅 API
  - 周期性订阅的 SubscriptionPurchaseV2 字段
  - 其他订阅管理函数

本文档列出了处于弃用期的 Google Play Developer API 和相关功能。

本部分中的功能和 API 自 2025 年 5 月 21 日起已被弃用，并将于 2027 年 8 月 31 日关停。不过，您可以申请延长已废弃商品的使用期限，最晚可延至 2027 年 11 月 1 日。

purchases.subscriptionv2 包含一些新字段，用于提供有关新订阅对象的更多详细信息。下表显示了旧订阅端点中的字段与 purchases.subscriptionv2 中相应字段的对应关系。

虽然 purchases.subscriptions:get 已升级到 purchases.subscriptionsv2:get，但 purchases.subscriptions 端点中的其余开发者订阅管理函数目前保持不变，因此您可以像以前一样继续使用 purchases.subscriptions:acknowledge、purchases.subscriptions:cancel、purchases.subscriptions:defer、purchases.subscriptions:refund 和 purchases.subscriptions:revoke。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

---

## 管理商品清单 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/manage-catalog

**Contents:**
- 管理商品清单 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 目录管理 API
  - 一次性商品
  - 订阅产品
  - 批处理方法
  - 更新传播延迟时间与吞吐量
  - 配额配置
  - Catalog Management API 使用建议
    - 监控您的用量
    - 优化 API 配额用量

本指南介绍了如何使用 Google Play Developer API 为您的 Play 应用创建和管理产品目录。

如需通过 Google Play 结算系统在应用中销售商品，您需要设置一个目录，其中包含您希望供用户购买的所有商品。您可以通过 Play 管理中心执行此操作，也可以使用 Google Play Developer API 自动执行目录管理。自动化有助于确保您的目录始终保持最新状态，并可扩展到手动协调不切实际的大型目录。本指南将介绍如何使用 Play Developer API 为您的 Play 应用创建和管理产品目录。如需了解如何为后端集成设置 Google Play Developer API，请参阅我们的准备工作指南。

如需了解您可以使用 Google Play 结算系统销售的不同类型的商品，请参阅了解应用内商品类型和商品清单注意事项。Google 针对 Play 上的目录管理提供了两组主要 API，分别对应于两个主要商品类别：

一次性商品（以前称为“应用内商品”）使用一次性商品对象模型，让您能够为一次性商品配置多个购买选项和优惠。一次性商品对象模型可让您以更灵活的方式销售商品，并降低管理商品的复杂性。您现有的应用内商品将迁移到一次性商品对象模型。 如需了解详情，请参阅迁移应用内商品。

借助 monetization.onetimeproducts 和 inappproducts 端点，您可以从后端管理一次性商品。这包括创建、更新和删除商品，以及管理价格和库存状况。根据您处理一次性商品购买交易的方式，您将对消耗型商品（可根据需要多次购买）或永久性授权（同一用户无法购买两次）进行建模。您可以决定哪些一次性商品应为消耗型商品，哪些不应为消耗型商品。

借助 monetization.subscriptions 端点，您可以从开发者后端管理订阅商品。您可以执行创建、更新和删除订阅等操作，也可以控制订阅的地区性库存状况和价格。除了 monetization.subscriptions 端点之外，我们还提供 monetization.subscriptions.basePlans 和 monetization.subscriptions.basePlans.offers，分别用于管理订阅的基础方案和优惠。

onetimeproducts、inappproducts 和 monetization.subscriptions 端点提供了一些批量方法，可用于同时检索或管理同一应用下的最多 100 个实体。

批量方法在与启用的延迟容忍度搭配使用时，可支持更高的吞吐量，尤其适用于大型目录开发者进行初始目录创建或目录协调。

在商品创建或修改请求完成后，由于网络或后端处理延迟，最终用户可能无法立即在设备上看到相应更改。默认情况下，所有商品修改请求都对延迟时间非常敏感。这意味着它们经过优化，可在后端系统中快速传播，通常会在几分钟内反映在最终用户设备上。不过，此类修改请求的数量存在每小时限制。 如果您需要创建或更新大量商品（例如，在初始创建大型商品目录期间），可以使用将 latencyTolerance 字段设置为 PRODUCT_UPDATE_LATENCY_TOLERANCE_LATENCY_TOLERANT 的批量方法。这将显著提高更新吞吐量。延迟容忍型更新最多需要 24 小时才能传播到最终用户设备。

使用 Play Developer API 管理商品目录时，您应注意以下几项配额限制：

以下是一些示例，可帮助您了解不同请求的配额用量：

遵循这些准则有助于优化您与 API 的互动，确保获得顺畅高效的商品目录管理体验。

您应注意高用量进程。例如，在集成开始时，您的目录管理端点可能会消耗更多配额来创建完整的初始目录，如果您接近总体使用量上限，这可能会影响其他端点（例如购买状态 API）的生产使用量。您需要监控配额消耗情况，确保不会超出 API 配额。您可以通过多种方式监控使用情况。例如，您可以使用 Google Cloud API 配额信息中心，也可以使用您选择的任何其他内部或第三方 API 监控工具。

强烈建议您优化速率消耗，以尽可能减少 API 错误的发生。为了有效实现此目标，我们建议您：

无论您构建目录管理逻辑的效率有多高，都应使其能够应对意外的配额限制，因为每日配额由集成中独立模块使用的端点共享。请务必在错误处理中包含配额限制错误，并实现适当的等待时间。对 Google Play Developer API 的每次调用都会生成响应。如果调用失败，您将收到一个失败响应，其中包含 HTTP 响应状态代码和一个 errors 对象，用于提供有关错误网域和调试消息的更多详细信息。例如，如果您超出每日限额，可能会遇到类似于以下内容的错误：

开发者使用 Google Play Developer API 产品发布端点来确保其目录在后端与 Google Play 之间保持同步。确保您的 Google Play 目录始终与后端目录的最新信息保持同步，有助于打造更好的用户体验。例如：

在 Google Play 上创建产品目录时，您应注意某些限制和注意事项。了解这些限制并确定目录的结构后，您就可以决定同步策略了。

借助 Google Play Developer API 发布端点，您可以在目录发生变化时对其进行更新。有时，您可能需要采用定期更新方法，即在同一流程中发送一系列更改。每种方法都需要不同的设计选择。每种同步策略都更适合某些使用情形，而您可能需要同时采用这两种策略，具体取决于具体情况。有时，您可能希望在发现新变化的那一刻立即更新商品，例如处理紧急商品更新（即需要尽快更正错误的价格）。在其他情况下，您可以使用定期后台同步来确保后端和 Play 目录始终保持一致。了解一些常见的使用情形，在这些情形下，您可能需要实施这些不同的目录管理策略。

理想情况下，一旦后端的产品目录发生任何变化，就应立即进行更新，以最大限度地减少差异。

这种方法实现起来更简单，并且可让您以最小的差异窗口保持目录同步。

定期更新会在后端异步运行到产品版本，在以下情况下，定期更新是不错的选择：

对于大型目录，请考虑使用对延迟时间不敏感的批量更新方法，以实现最大吞吐量。

如果您要将大量目录上传到 Google Play，可能需要自动执行初始加载。如果采用周期性策略并结合容忍延迟的批处理方法，这种重型进程的效果最佳。

对于初始的一次性商品清单创建，我们建议使用 monetization.onetimeproducts.batchUpdate 或 inapp_products.insert 方法，并将 allowMissing 字段设置为 true，将 latencyTolerance 字段设置为 PRODUCT_UPDATE_LATENCY_TOLERANCE_LATENCY_TOLERANT。这样可以最大限度地缩短在配额限制内创建目录所需的时间。

对于初始订阅大型目录创建，我们建议使用 monetization.subscriptions.batchUpdate 方法，并将 allowMissing 字段设置为 true，将 latencyTolerance 字段设置为 PRODUCT_UPDATE_LATENCY_TOLERANCE_LATENCY_TOLERANT。这样可以最大限度地缩短在配额限制内创建目录所需的时间。

对于较小的订阅清单，Play Developer API 提供了 monetization.subscriptions.create 方法。或者，您也可以使用 allowMissing 参数通过 monetization.subscriptions.patch 方法创建订阅，如“产品更新”部分中所述。

之前的所有方法都会创建订阅及其基础方案（在 Subscription 对象中提供）。这些基础方案最初处于非有效状态。如需管理基础方案的状态，您可以使用 monetization.subscriptions.basePlans 端点，包括启用基础方案以使其可供购买。此外，您还可以使用 monetization.subscriptions.basePlans.offers 端点创建和管理优惠。

借助以下方法，您可以高效地修改现有商品，确保商品与您的最新调整保持一致。

您可以使用以下方法来更新现有的一次性商品。

如需更新现有订阅，您可以使用 monetization.subscriptions.patch 方法。此方法采用以下必需参数：

除非您使用 allowMissing 参数创建新订阅，否则必须提供 updateMask 参数。此参数是一个以英文逗号分隔的列表，其中包含您要更新的字段。

例如，如果您只想更新订阅商品的商品详情，则应将 listings 字段指定给 updateMask 参数。

您可以使用 monetization.subscriptions.batchUpdate 同时更新多个订阅。 将其与设置为 PRODUCT_UPDATE_LATENCY_TOLERANCE_LATENCY_TOLERANT 的 latencyTolerance 字段搭配使用，可实现更高的吞吐量。

如需激活、停用或删除基础方案，或者将订阅者迁移到最新的基础方案价格版本，请使用 monetization.subscriptions.basePlans 端点。

此外，您还可以使用 monetization.subscriptions.basePlans.offers.patch 方法更新基础方案的优惠。

无论您是选择在每次后端目录发生变化时更新 Google Play 目录，还是定期更新，如果您在 Google Play 目录之外有目录管理系统或数据库，都可能会出现这种情况：后端目录与 Play 上应用配置中的目录不同步。这可能是因为 Play 管理中心内紧急手动更改了目录、目录管理系统出现中断，或者您丢失了最新数据。

您可以构建目录对账流程，以避免出现长时间的差异窗口。

我们建议构建一个差异系统来检测不一致之处，并协调这两个系统。在构建差异系统以帮助保持目录同步时，您需要考虑以下事项：

Google Play Developer API 提供以下方法来帮助您弃用商品：

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-08-25。

**Examples:**

Example 1 (unknown):
```unknown
{
  "code" : 403,
  "errors" : [ {
    "domain" : "usageLimits",
    "message" : "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API
  Console: https://console.developers.google.com/apis/api/androidpublisher.googleapis.com/quotas?project=xxxxxxx",
  "reason" : "dailyLimitExceeded",
  "extendedHelp" : "https://console.developers.google.com/apis/api/androidpublisher.googleapis.com/quotas?project=xxxxxx"
  } ],
}
```

Example 2 (unknown):
```unknown
{
  "code" : 403,
  "errors" : [ {
    "domain" : "usageLimits",
    "message" : "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API
  Console: https://console.developers.google.com/apis/api/androidpublisher.googleapis.com/quotas?project=xxxxxxx",
  "reason" : "dailyLimitExceeded",
  "extendedHelp" : "https://console.developers.google.com/apis/api/androidpublisher.googleapis.com/quotas?project=xxxxxx"
  } ],
}
```

---

## 有关替代的应用内购结算系统的临时用户体验指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/billing-choice?hl=zh-cn

**Contents:**
- 有关替代的应用内购结算系统的临时用户体验指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 概览
- 面向用户的信息
  - 何时显示
  - 何时显示价格
  - 如何显示
  - 用户操作
    - 继续
    - 了解详情
    - 关闭

为了维持一致的用户体验并帮助用户做出明智的选择，您需要显示信息屏幕；如果除了 Google Play 结算系统以外，您还提供替代的应用内购结算系统，则还需要显示单独的结算方式选择屏幕。信息屏幕只需在每位用户首次发起购买交易时向其显示即可，而结算方式选择屏幕应在每次购买交易前向用户显示。应根据以下准则为这两个屏幕实现面向用户的消息和界面规范。

信息屏幕可以帮助用户了解相关更改的背景，并提供更多信息以帮助用户做出明智的选择。

添加替代应用内购结算系统后，应在用户开始进行首次购买交易时向其显示信息屏幕。当同一用户以后再次进行购买交易时，就不需要再显示该信息了。在用户执行明确操作以发起购买交易之后，系统应立即显示信息屏幕。

应在显示信息屏幕或结算方式选择屏幕之前，在显眼的位置向用户显示购买价格。

信息屏幕应显示在模态底部动作条中。模态底部动作条与模态对话框类似，它会从屏幕底部向上呈现动画效果，并固定在屏幕底部。它位于底层屏幕中的所有界面元素的上层。底层屏幕会被深色纱罩遮挡，以表示它不会响应用户互动。

如需详细了解模态底部动作条的设计和实现，请参阅 Google Material Design。

当用户点按应用中用于发起购买交易的按钮或其他界面元素时，底部动作条应触发。用户可以在信息屏幕中执行 3 种可能的操作：

点按“继续”按钮会关闭信息屏幕，并启动结算方式选择屏幕。

点按“了解详情”按钮可在网络浏览器中打开相应的 Google 帮助中心文章。

如果用户要关闭底部动作条并返回底层屏幕，可以通过以下方式关闭底部动作条：

在用户关闭信息屏幕或点按“继续”后，无需再次显示信息屏幕。

示例：在用户发起购买交易之前，购买交易已明确显示。点按“立即加入”按钮会触发信息屏幕。

信息屏幕分为 3 个组件：标题、消息和按钮。所有这 3 个组件都是必需的，其包含的文字和界面元素必须与本准则中的定义完全一致。请勿在该屏幕中添加任何其他文字或图像，但您可以在其他屏幕中添加额外的文字和图像。

在横向视图中，底部动作条的宽度大于纵向视图中的宽度，但在其他方面都遵循相同的设计规范和功能。

结算方式选择界面向用户展示两种结账选项，用于完成购买交易。为了帮助用户做出明智的决策，每个结算服务选项还会向用户显示可用的付款方式。在用户做出选择后，他们将继续通过所选的结算服务完成购买交易。

如果用户已查看过信息屏幕，则在其执行明确操作以发起购买交易后，系统应立即显示结算方式选择屏幕。

结算方式选择屏幕应该显示在模态底部动作条中，并遵循与信息屏幕相同的规范。

您应该采用公平且均等的方式来展示其他应用内购结算系统的按钮和 Google Play 结算服务的按钮。这包括但不限于相同的按钮大小、文字大小/样式、点按目标和图标大小。请勿添加本指南中未定义的任何其他文字、图片或样式更改。

示例：点按“立即加入”按钮会触发结算方式选择屏幕。

结算方式选择屏幕包含 4 个不同的组件：标题、说明、开发者按钮和 Google Play 按钮。您应使用所有组件，并且这些组件包含的文字和界面元素应与本准则中的定义完全一致。请勿在该屏幕中添加任何其他文字或图像，但您可以在您拥有的其他屏幕中添加其他文字和图像。

您可以通过以下链接获取 Google Play 的可视化资源和付款图标。

示例：在纵向视图中，底部动作条的跨度应该与屏幕总宽度相等。

示例：在横向视图中，底部动作条的宽度大于纵向视图中的宽度，但在其他方面都遵循相同的设计规范和功能。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

---

## 针对外部优惠计划的应用内集成指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/external/integration

**Contents:**
- 针对外部优惠计划的应用内集成指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- Play 结算库设置
- 连接到 Google Play
  - Kotlin
  - Java
- 查看空房情况
  - Kotlin
  - Java
- 准备外部交易令牌
  - Kotlin

本指南介绍了如何集成 API 以支持外部优惠 在符合条件的应用和地区推出。详细了解外部优惠计划 包括资格要求和地理范围，请参阅 计划要求。

如需使用外部优惠 API，请执行以下操作： 添加 6.2.1 版或更高版本的 Play 结算库依赖项 您的 Android 应用如果您需要从早期版本迁移，请按照 请参阅迁移指南中的说明，然后再尝试实施 外部优惠。

集成流程的最初步骤与 结算集成指南中有一些建议， 初始化 BillingClient：

以下示例演示了如何通过这些调整来初始化 BillingClient：

初始化 BillingClient 后，您需要按照集成指南中的说明与 Google Play 建立连接。

您的应用应通过调用 isExternalOfferAvailableAsync。

如果有外部优惠，此 API 会返回 BillingResponseCode.OK。 如需详细了解您的应用应如何处理，请参阅响应处理 对其他响应代码进行响应。

要向 Google Play 报告外部交易，您必须拥有一个外部 Play 结算库生成的交易令牌。新的外部 每次用户访问外部 通过外部优惠 API 访问网站。这可以通过调用 createExternalOfferReportingDetailsAsync API。此令牌应为 系统会在用户被定向到应用外部紧接着生成它应该 永不缓存，并且每次引导用户时都应生成一个新的密钥 。

如需与外部优惠集成，符合条件的应用必须显示相关信息 这个界面可以帮助用户了解 将应用关联到外部网站信息屏幕必须通过 先调用 showExternalOfferInformationDialog API，然后再链接到 每次外部优惠

如果此方法返回 BillingResponseCode.OK，您的应用可以继续 将用户定向到外部网站。如果该方法返回 BillingResponseCode.USER_CANCELED，您的应用不得继续打开 网站。

所有外部交易都必须报告给 Google Play 从后端调用 Google Play Developer API。外部交易 同时提供 externalTransactionToken 通过 createExternalOfferReportingDetailsAsync API。如果用户多次提交 购买时，您可以使用 externalTransactionToken来报告每笔购买交易。要了解如何举报 请参阅后端集成指南。

发生错误时，isExternalOfferAvailableAsync 方法、 createExternalOfferReportingDetailsAsync和 showExternalOfferInformationDialog 可能会返回 BillingResponseCode.OK。请考虑按如下方式处理这些响应代码：

许可测试人员应该用于测试外部优惠集成。您 对于许可测试人员发起的交易，系统不会开具账单 账号。如需了解详情，请参阅使用应用许可测试应用内购结算功能 了解如何配置许可测试人员

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

**Examples:**

Example 1 (unknown):
```unknown
var billingClient = BillingClient.newBuilder(context)
  .enableExternalOffer()
  .build()
```

Example 2 (unknown):
```unknown
var billingClient = BillingClient.newBuilder(context)
  .enableExternalOffer()
  .build()
```

Example 3 (unknown):
```unknown
private BillingClient billingClient = BillingClient.newBuilder(context)
    .enableExternalOffer()
    .build();
```

Example 4 (unknown):
```unknown
private BillingClient billingClient = BillingClient.newBuilder(context)
    .enableExternalOffer()
    .build();
```

---

## 订阅简介 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/subs?hl=zh-cn

**Contents:**
- 订阅简介 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 订阅概览
- 预付费方案集成
  - 预付费购买交易确认
- 分期付款型订阅集成
- 使用深层链接让用户能够管理订阅
  - 指向订阅中心的链接
  - 指向特定订阅的管理页面的链接（推荐）
- 允许用户升级、降级或更改订阅
  - 替换模式

本文档介绍了如何处理订阅生命周期事件，如续订和到期。此外，还介绍了其他订阅功能，如提供促销活动以及允许用户管理他们自己的订阅。

如果您还没有为您的应用配置订阅商品，请参阅创建和配置您的商品。

订阅是一种定期交易，可授予用户特定使用权。授权代表用户在指定时间段内可以享受的一系列权益。例如，订阅可授予用户高级访问权限。

您可以通过基础方案和优惠，为同一订阅商品创建多个配置。例如，您可以针对从未订阅过您的应用的用户创建初次体验优惠。同样，您也可以针对已经订阅的用户创建升级优惠。

如需详细了解订阅商品、基础方案和优惠，请参阅 Play 管理中心帮助中心内的相关文档。

单项订阅 - 在这种类型的订阅中，一项商品对应一项授权。例如，订阅音乐在线播放服务。

含加购项的订阅 - 在这种类型中，一次购买可以包含多项不同的授权。例如，同时订阅音乐在线播放服务和视频订阅。如需了解包含加购项的订阅的具体信息，请参阅包含加购项的订阅。

预付费方案到期后不会自动续订。如需延长订阅内容使用权而不出现中断，用户必须给同一项订阅内容的预付费方案充值。

对于充值，请按照与原始购买交易相同的方式启动结算流程。 您无需指明购买交易是充值。

预付费方案充值始终使用 CHARGE_FULL_PRICE 替换模式，您无需明确设置此模式。系统会立即向用户收取整个结算周期的费用，并按充值时指定的时长延长其使用权。

充值后，Purchase 结果对象中的以下字段会更新，以反映最新的充值交易：

以下 Purchase 字段中包含的数据始终与原始购买交易中的数据相同：

与自动续订型订阅类似，您必须在购买交易完成后确认预付费方案。初始购买交易和所有充值都需要进行确认。如需了解详情，请参阅处理购买交易。

由于预付费方案的时长有可能比较短，因此请务必尽快确认购买交易。

时长为一周或更长时间的预付费方案必须在三天内确认。

对于时长不到一周的预付费方案，其确认时间不得晚于方案时长过半之时。例如，开发者必须在 1.5 天内确认时长为三天的预付费方案。

分期付款型订阅是一种订阅，用户可以在一段时间内分多次支付订阅费用，而不是一次性预付全部订阅费用。

实时开发者通知 (RTDN)：如果用户在承诺期内仍有待付金额，则在用户发起取消时，系统会立即发送 SUBSCRIPTION_CANCELLATION_SCHEDULED RTDN。取消处于待处理状态，仅在合约期结束时生效。然后，如果用户未恢复，系统会在合约期结束时发送 SUBSCRIPTION_CANCELED 和 SUBSCRIPTION_EXPIRED RTDN。

付款 / 收入确认：用户每月付款后，开发者才会收到款项，但需遵守与其他所有订阅相同的条款。用户注册分期付款订阅时，开发者不会收到预付款。

未收取的款项：如果用户未能支付任何分期付款订阅费用，Google 和开发者都不会尝试向用户收取任何此类未付或未结款项，但 Google 可能会在任何适用的宽限期或账号中止期内，根据其正常的付款重试做法定期重试付款。对于任何未付的剩余分期付款，Google 均不对开发者承担任何责任。

Play 结算库可用性：installmentDetails 字段仅适用于 PBL 7 或更高版本。对于 PBL 5 及更高版本，分期付款订阅使用 queryProductDetails() 返回，但订阅不会包含详细的分期付款信息，例如方案的承诺付款次数。

您的应用应在设置或偏好设置界面上添加一个链接，让用户能够管理订阅，您可将链接与应用的自然外观和风格融为一体。

对于未过期的订阅，您可以添加从您的应用到 Google Play 订阅中心的深层链接，您可以使用订阅资源的 subscriptionState 字段来确定订阅是否未过期。基于此，您可以通过多种方式深层链接到 Play 商店订阅中心。

使用以下网址将用户定向到显示其所有订阅的页面，如图 1 和图 2 所示：

此深层链接可能有助于用户从 Play 商店订阅中心恢复已取消的订阅。

若要直接链接到一项未过期订阅的管理页面，请指明与购买的订阅关联的软件包名称和 productId。若要以程序化方式确定一项现有订阅的 productId，请在应用的后端查询，或针对与特定用户关联的订阅列表调用 BillingClient.queryPurchasesAsync()。每项订阅都包含相应的 productId，作为订阅状态信息的一部分。与订阅购买交易关联的每个 SubscriptionPurchaseLineItem 对象都包含与用户在该订单项中购买的订阅关联的 productId 值。

使用以下网址将用户定向到特定订阅的管理界面，并将“your-sub-product-id”和“your-app-package”分别替换为 productId 和应用软件包名称：

然后，用户就能管理其付款方式并使用取消、重新订阅和暂停等功能。

您可以为现有订阅者提供各种选项，方便他们更改订阅方案以更好地满足个人需求：

您可以通过订阅优惠向符合条件的用户提供折扣，鼓励用户进行上述任何更改。例如，您可以创建一个从包月方案改为包年方案第一年可享 5 折价格的优惠，并将此优惠限制为仅面向订阅了包月方案但尚未购买此优惠的用户。如需详细了解优惠资格条件，请访问帮助中心

图 3 显示了一款提供 3 种不同方案的示例应用：

应用可以显示类似于图 3 的界面，为用户提供更改其订阅的选项。在任何情况下，应用都必须向用户清楚展示当前采用的订阅方案是什么，以及可采用的方案更改选项。

当用户决定升级、降级或更改其订阅时，您可以指定替换模式，确定如何采用目前付费结算周期的按比例计费值，以及任何使用权变更的生效时间。

下表列出了可用的替换模式和用法示例，以及被视为已付款的付款次数。

已记录为已支付的承诺付款（适用于分期付款订阅替换）

订阅商品会立即升级或降级。系统会根据差价调整任何剩余时长，并将下一个结算日期往后推延，将剩余时长计入新的订阅。这是默认行为。

升级到费用更高的层级，无需立即支付额外费用。

CHARGE_PRORATED_PRICE

订阅项会立即升级，结算周期保持不变。用户随后需要补足剩余订阅期的差价。

注意：此选项仅适用于每时间单位的价格会提高的订阅商品升级。

订阅项会立即升级或降级，并且系统会即刻按全价向用户收取新使用权的费用。如果使用权不变，系统会将之前订阅的剩余价值结转；如果使用权有变化，系统会将剩余价值按比例折算成时间。

注意：如果新订阅提供免费试订或初次体验优惠，则在升级或降级时，用户需支付 0 美元或初次体验价费用（以适用者为准）。

1（注意：如果新订阅提供免费试用，则为 0）

订阅商品会立即升级或降级，在订阅续订时将按新价格收取费用。结算周期保持不变。

升级到更高的订阅层级，同时保留所有剩余的免费试用期。

只有在订阅续订时，订阅项才会升级或降级，但新购买的内容会立即发放，其中包含以下两项：

注意：对于分期付款订阅，方案更改会在下一个付款日期开始时生效。

替换后，相应订阅商品的付款时间表保持不变。

在包含加购项的订阅中添加或移除订阅项，同时确保特定项保持不变。

如需详细了解如何将升级或降级优惠应用在各种追加销售和客户赢回活动中，请参阅优惠与促销活动指南。

您可以根据自己的偏好设置和业务逻辑，为不同类型的订阅转换采用不同的替换模式。本部分介绍如何针对订阅更改设置替换模式以及适用的限制。

您可以在 Google Play 管理中心内指定默认替换模式。如果当前订阅者购买同一订阅的不同基础方案或优惠，或者在取消订阅后重新订阅，您可以通过此设置选择何时向其收费。可用选项包括“立即收费”（等同于 CHARGE_FULL_PRICE）和“在下一个结算日收费”（等同于 WITHOUT_PRORATION）。在同一订阅中切换基础方案时，这些是仅有的相关替换模式。

例如，如果您要在用户取消订阅后、订阅结束前针对同一方案实现赢回优惠，则可以将新购买交易作为常规购买交易处理，无需在 SubscriptionUpdateParams 中指定任何值。系统会使用您在订阅中配置的默认替换模式，并自动处理从旧购买交易到新购买交易的方案转换。

如果用户更改订阅产品（即购买其他订阅），或者如果您出于任何原因想要替换默认替换模式，您可在购买流程参数中指定运行时按比例计费费率。

若要在 SubscriptionProductReplacementParams 或 SubscriptionUpdateParams 中正确提供 ReplacementMode 作为运行时购买流程配置的一部分，请注意以下限制：

为了理解各种按比例计费模式的运作原理，我们来考虑下面的场景：

Samwise 订阅了 Country Gardener 应用的在线内容。他按月订阅第 1 层级版的内容，该内容只包含文字。此订阅的费用为每月 2 美元，并且在每月的第一天续订。

在 4 月 15 日，李明选择升级到第 2 层级按年订阅，该内容包含视频更新，费用为每年 36 美元。

升级订阅时，开发者会选择一种按比例计费模式。以下列表说明了各种按比例计费模式对李明的订阅有何影响：

李明的第 1 层级订阅会立即终止。由于他支付了一整个月（4 月 1 日至 30 日）的费用，但在订阅期刚过一半时升级了订阅，因此剩余半个月的订阅费用（1 美元）会应用到新订阅。不过，由于新订阅的费用为每年 36 美元，1 美元的余额只够 10 天（4 月 16 日至 25 日）的费用，因此在 4 月 26 日，他需要为新订阅支付 36 美元的费用，并且此后每年的 4 月 26 日需要再支付 36 美元。

您应在购买交易成功时调用应用的 PurchasesUpdatedListener，并且您能通过 queryPurchasesAsync() 调用检索新购买交易。您的后端会立即收到 SUBSCRIPTION_PURCHASED 实时开发者通知。

CHARGE_PRORATED_PRICE

可以使用此模式，因为第 2 层级的每时间单位的订阅价格（36 美元/年 = 3 美元/月）高于第 1 层级的每时间单位的订阅价格（2 美元/月）。李明的第 1 层级订阅会立即终止。由于他支付了一整个月的费用，但只用了一半，因此剩余半个月的订阅费用（1 美元）会应用到新订阅。不过，由于新订阅的费用为每年 36 美元，剩余 15 天的费用为 1.50 美元，因此他需要为新订阅支付 0.50 美元的差价。在 5 月 1 日，李明需要为新订阅层级支付 36 美元，并且此后每年的 5 月 1 日都需要再支付 36 美元。

您应在购买交易成功时调用应用的 PurchasesUpdatedListener，并且您能通过 queryPurchasesAsync() 调用检索新购买交易。您的后端会立即收到 SUBSCRIPTION_PURCHASED 实时开发者通知。

李明的第 1 层级订阅会立即升级到第 2 层级，无需支付额外的费用，而在 5 月 1 日，他需要为新订阅层级支付 36 美元，并且此后每年的 5 月 1 日都需要再支付 36 美元。

您应在购买交易成功时调用应用的 PurchasesUpdatedListener，并且您能通过 queryPurchasesAsync() 调用检索新购买交易。您的后端会立即收到 SUBSCRIPTION_PURCHASED 实时开发者通知。

李明的第 1 层级订阅会一直持续到 4 月 30 日到期。在 5 月 1 日，第 2 层级订阅开始生效，李明需要为新订阅层级支付 36 美元。

您应在购买交易成功时调用应用的 PurchasesUpdatedListener，并且您能通过 queryPurchasesAsync() 调用检索新购买交易。您的后端会立即收到 SUBSCRIPTION_PURCHASED 实时开发者通知。您应该处理购买交易，采用与此时处理任何其他新购买交易相同的方式。尤其需要注意的是，请务必确认新的购买交易。请注意，在替换生效时（即旧订阅到期时），系统会填充新订阅的 startTime。届时，您会收到新订阅方案的 SUBSCRIPTION_RENEWED RTDN。如需详细了解 ReplacementMode.DEFERRED 行为，请参阅处理延迟替换。

李明的第 1 层级订阅会立即终止。他的第 2 层级订阅当天开始生效，他需要支付 36 美元。由于他支付了一整个月的费用，但只用了一半，因此剩余半个月的订阅费用（1 美元）会应用到新订阅。由于新订阅的费用为每年 36 美元，因此他的订阅期限会延长一年的 1/36（约 10 天）。这样一来，李明的下一次扣款时间距离现在还有 1 年零 10 天，下次扣款金额为 36 美元。此后，他每年需要支付 36 美元。

选择按比例计费模式时，请务必查看我们的替换建议。

Samwise 订阅了 Country Gardener 应用的在线内容。他按月订阅了包含基本内容的方案 1。此订阅的初次体验价为每月 2 美元，为期 3 个月，之后为每月 4 美元。Samwise 于 4 月 1 日购买了此商品。Country Gardener 应用提供方案 2，作为附加的专业内容，每月 3 美元。4 月 15 日，Samwise 在保留现有方案 1 的同时，为 Country Gardener 应用的订阅添加了方案 2。Samwise 的付款时间安排如下：

您的应用可以使用与启动购买流程相同的步骤来为用户提供升级或降级。不过，在升级或降级时，您需要提供当前订阅、将来（升级或降级的）订阅以及要使用的替换模式的详细信息。

以下示例展示了如何使用 SubscriptionProductReplacementParams 更新订阅。

BillingFlowParams.ProductDetailsParams 对象现在具有 setSubscriptionProductReplacementParams() 方法，用于指定商品级替换信息。

SubscriptionProductReplacementParams 有两个 setter 方法：

现有的购买级别更新参数 BillingFlowParams.setSubscriptionUpdateParams() 应使用 setOldPurchaseToken() 构建。

一旦针对任何 ProductDetailsParams 调用 setSubscriptionProductReplacementParams()，SubscriptionUpdateParams.setSubscriptionReplacementMode() 将不会产生任何影响。

以下代码示例演示了如何将订阅方案从 (old_product_1, old_product_2) 更改为 (product_1, product_2, product_3)。在此方案中，product_1 会替换 old_product_1，product_2 会替换 old_product_2，并且 product_3 会立即添加到订阅中。

以下示例展示了如何使用 SubscriptionUpdateParams 更新订阅。

下表显示了不同的按比例计费场景以及我们针对各种场景给出的建议：

就所有条款和用途而言，方案的更改是指新的购买交易，且在结算流程成功完成后应该以此形式处理及确认。除了适当处理新购买交易之外，您还必须停用将被替换的购买交易。

应用内行为与任何新购买交易的行为一样。您的应用会在 PurchasesUpdatedListener 中收到新购买交易的结果，而新购买交易会在 queryPurchasesAsync 中可用。

当购买交易替换现有购买交易时，Google Play Developer API 会在订阅资源中返回一个 linkedPurchaseToken。您可以查看新购买交易中 SubscriptionPurchaseLineItem 下的 itemReplacement，了解商品级换货详情。请务必使在 linkedPurchaseToken 中提供的令牌无效，确保旧令牌不会被用于获取对您服务的访问权限。如需了解如何处理升级购买交易和降级购买交易，请参阅升级、降级和重新注册。

当您收到购买令牌时，请遵循与验证新购买令牌相同的验证流程。请务必使用 Google Play 结算库中的 BillingClient.acknowledgePurchase() 或 Google Play Developer API 中的 Purchases.subscriptions:acknowledge 确认这些购买交易。

通过延迟替换模式，您可允许用户先用完旧方案中的剩余使用权，再开始使用新方案。

当您针对新购买交易使用 ReplaceMode.DEFERRED 时，queryPurchasesAsync() 会在购买流程结束后返回一个新购买令牌，该令牌仍与旧购买交易相关联，直到在下一个续订日期延迟替换模式生效后，系统才会返回新产品。

过去，您可以使用已废弃的 ProrationMode.DEFERRED 实现这种用户体验，但 Play 结算库 6 中废弃了 ProrationMode.DEFERRED。请参阅下表，了解此行为在哪些方面有所不同：

ProrationMode.DEFERRED（已废弃）

购买交易完成后，系统会调用 PurchasesUpdatedListener，并附带升级或降级是否成功的状态。

您可以保有对旧方案的使用权，直到下一个续订日期为止。为确保应用提供适当的使用权，queryPurchasesAsync() 会返回一个包含原始购买令牌和原始使用权的 Purchase 对象，直至替换发生。

购买交易完成后，系统会调用 PurchasesUpdatedListener，并附带升级或降级是否成功的状态。

queryPurchasesAsync() 会立即返回带有新购买令牌的购买交易以及与其关联的原始使用权。

新购买令牌已显示，考虑到替换的生效时间，应在此时进行处理。

购买流程结束后，不发送 SUBSCRIPTION_PURCHASED RTDN。后端尚未获知新购买交易。

购买流程结束后，立即针对新购买令牌发送带有旧 product_id 的 SUBSCRIPTION_PURCHASED RTDN。

使用新购买令牌调用 purchases.subscriptionsv2.get 方法会返回包含两个订单项且具有“startTime”（指示购买时间）的购买交易：

针对旧购买令牌发送 SUBSCRIPTION_EXPIRED。使用旧购买令牌调用 purchases.subscriptionsv2.get 方法时，显示为已过期（旧方案剩余时长的使用权会转移到新购买交易）。

queryPurchasesAsync() 会返回一个包含新购买令牌和使用权的新 Purchase 对象。

queryPurchasesAsync() 会立即返回带有新购买令牌的购买交易以及与其关联的新使用权。

新购买交易应在购买流程成功后已处理完毕，因此除了确保正确授予使用权之外，应用不应执行任何特殊操作。

现在，新购买交易可在系统发送第一个 SUBSCRIPTION_RENEWED RTDN 时处理和确认。

订阅资源中的 linkedPurchaseToken 可用于确定订阅后端的哪个用户（如果适用）应更新为拥有新的使用权。

针对新购买令牌发送 SUBSCRIPTION_PURCHASED RTDN 时处理并确认新购买交易，并将其记录为“startTime”。

使用 ReplaceMode.DEFERRED 时，首次续订将遵循任何其他续订的标准行为，并且当此事件发生时，您无需针对替换处理特殊逻辑。

使用新购买令牌调用 purchases.subscriptionsv2.get 方法会返回包含两个订单项的购买交易：

从现在开始，应使用 ReplaceMode.DEFERRED，而非已废弃的 ProrationMode.DEFERRED，因为前者虽然执行与使用权更改相同的行为，但提供的购买交易管理方式与其他新购买交易的行为更加一致。

使用实时开发者通知，当用户决定取消订阅时，您可以实时检测到。如果用户在订阅到期之前取消了订阅，您可以向他们发送推送通知或应用内消息，让他们重新订阅。

在用户取消订阅后，您可以尝试在应用内或通过 Play 商店赢回他们。下表介绍了各种订阅场景以及相关的赢回操作和应用要求。

未采用结算库 2.0 及以上版本的应用：否

采用结算库 2.0 及以上版本的应用：是。开发者可以在管理中心中选择停用该功能。

如果使用相同的 SKU：当前结算周期结束时。

如果使用不同的 SKU：取决于按比例计费模式。

对于已被取消但尚未过期的订阅，您可以通过应用与新订阅者相同的应用内商品购买流程，允许订阅者在您的应用中恢复他们的订阅。请确保界面中会显示用户的现有订阅。例如，您不妨显示用户当前的到期日期、定期支付的费用以及重新激活按钮。

大多数情况下，建议您向用户提供与已订阅内容相同的价格和 SKU，如下所示：

如果您想提供不同的价格（例如，新的免费试订或赢回折扣），则可以改为为用户提供不同的 SKU：

当您收到购买令牌时，应该就像处理新订阅一样来处理购买交易。此外，Google Play Developer API 还会在订阅资源中返回一个 linkedPurchaseToken。请务必让 linkedPurchaseToken 中提供的令牌失效，以确保旧令牌不会被用于获取对您服务的访问权限。

在订阅被取消但仍然处于有效状态时，用户可以通过点击重新订阅（以前称为恢复）在 Google Play 订阅中心恢复订阅。这样会让订阅和购买令牌保持不变。

您可以允许订阅已过期的订阅者在您的应用中重新订阅，方法是应用与新订阅者相同的应用内商品购买流程。请注意以下几点：

当您收到购买令牌时，应该就像处理新订阅一样来处理购买交易。您将不会在订阅资源中收到 linkedPurchaseToken。

如果您启用了重新订阅功能，用户便可在订阅到期后最长一年时间内，通过在 Google Play 订阅中心点击重新订阅来重新订阅同一 SKU。这样会生成新的订阅和购买令牌。

重新订阅属于应用外购买，因此请务必遵循相关最佳实践，从后端正确确认这些交易。

您可以创建促销代码，让部分用户能够免费试订现有订阅更长时间。如需了解详情，请参阅促销代码。

对于免费试订，Google Play 会在免费试订开始之前验证用户是否具有有效的付款方式。某些用户可能会看到此验证的结果显示为付款方式被暂停或产生扣款。这种暂停或扣款是暂时的，稍后会撤消或退还。

试订期结束后，系统会通过用户的付款方式，按照全价收取订阅费用。

如果用户在免费试订期间的任一时刻取消了订阅，订阅将保持活动状态，直到试订期结束，当免费试订期结束时，用户不会被扣款。

您可以使用 Google Play Developer API 取消或撤消订阅。 Google Play 管理中心也提供了此功能。

取消：用户可以在 Google Play 上取消订阅。您也可为用户提供一个在您的应用中或您的网站上取消订阅的选项。您的应用应按照取消中的说明来处理这些取消事件。

撤消：当您撤消时，用户会立即失去对订阅的访问权限。例如，如果因技术错误而导致用户无法访问您的商品，因而用户不想继续使用该商品，则可以使用此选项。您的应用应按照撤消中的说明来处理这些取消事件。

您可以使用 Google Play Developer API 中的 Purchases.subscriptions:defer 将自动续订订阅者的下一个结算日期向前推。在推迟期内，用户会订阅您的内容并且拥有完全访问权限，但不会被扣款。订阅续订日期会更新以反映新的日期。

对于预付费方案，您可以使用推迟结算 API 来推迟到期时间。

每次调用该 API，结算最短可推迟一天，最长为一年。如需进一步推迟结算，您可以在新的结算日期到来之前再次调用该 API。

例如，Darcy 按月订阅了 Fishing Quarterly 应用的在线内容。正常情况下，她在每个月第一天都需要支付 1.25 英镑的费用。在 3 月，她参与了应用发布商的在线问卷调查。该发布商为她提供了免费六周的奖励，将下一笔付款推迟到 5 月 15 日，也就是在她先前预定结算日期（即 4 月 1 日）的六周后。

推迟结算时，您可能需要通过电子邮件或在应用中通知用户，告知用户他们的结算日期发生了变化。

如果订阅续订存在付款问题，Google 会在取消订阅前的一段时间内定期尝试续订。此恢复续订期可以由宽限期及后续的账号冻结期组成。在此期间，Google 会向用户发送电子邮件和通知，提醒他们更新付款方式。

付款遭拒后，如果配置了宽限期，订阅会进入宽限期。在宽限期内，您应确保用户仍有权使用订阅内容。

任何宽限期结束后，订阅将进入账号冻结期。在账号冻结期间，您应确保用户无法访问订阅内容使用权。

您可以在 Google Play 管理中心内指定每个自动续订基础方案的宽限期和账号中止期。如果指定的时长小于默认值，可能会导致从付款被拒中恢复的订阅量减少。

为了在付款遭拒期间最大限度提高恢复订阅的可能性，您可以将付款问题告知用户，并请他们解决此问题。

您可以自行执行此操作（如宽限期和账号冻结部分中所述）；也可以实现 In-App Messaging API，通过此方法让 Google 在应用中向用户显示消息。

如果您使用 InAppMessageCategoryId.TRANSACTIONAL 启用了 In-App Messaging 功能，Google Play 会在宽限期和账号冻结期内每天向用户显示一次消息，并使用户能够无需离开应用即可解决付款问题。

我们建议您在用户每次打开应用时都调用此 API，以确定是否应该显示此消息。

如果用户成功恢复了订阅，您会收到响应代码 SUBSCRIPTION_STATUS_UPDATED 以及购买令牌。然后，您应使用此购买令牌调用 Google Play Developer API 并刷新应用中的订阅状态。

如需向用户显示应用内消息，请使用 BillingClient.showInAppMessages()。

以下是触发 In-App Messaging 流程的示例：

待处理的交易可能发生在初始购买、充值、升级或降级时。订阅购买交易从 SUBSCRIPTION_STATE_PENDING 状态开始，然后转换为 SUBSCRIPTION_STATE_ACTIVE。如果交易过期或被用户取消，则会进入 SUBSCRIPTION_STATE_PENDING_PURCHASE_EXPIRED。您必须且只能在交易完成后更新用户的授权。

对于包含待处理交易的初始购买交易，订阅状态更改非常简单。当用户发起待处理交易时，您的应用会收到状态为 PENDING 的 Purchase。交易完成后，您的应用会再次收到 Purchase，但状态已更新为 PURCHASED。系统会向您的 RTDN 客户端发送类型为 SUBSCRIPTION_PURCHASED 的 SubscriptionNotification 消息。按照正常流程验证购买交易、向用户授予内容访问权限并确认购买交易。如果交易过期或被取消，系统会向您的 RTDN 客户端发送一条类型为 SUBSCRIPTION_PENDING_PURCHASE_CANCELED 的 SubscriptionNotification 消息。在这种情况下，用户不应获得对相应内容的访问权限。

充值、升级或降级（如果交易待处理）会涉及新旧订阅的状态变化。当用户发起待处理的充值、升级或降级交易时，您的应用会收到旧订阅的 Purchase，其中包含 PendingPurchaseUpdate 对象。此时，用户仍拥有旧订阅，但尚未获得新订阅。对 PendingPurchaseUpdate 对象调用 getProducts() 和 getPurchaseToken() 会返回新订阅的商品 ID 和购买令牌。交易完成后，您的应用会收到一个 Purchase，其中包含为新订阅设置的顶级购买交易令牌，并且状态设置为 PURCHASED。系统会向您的 RTDN 客户端发送类型为 SUBSCRIPTION_PURCHASED 的 SubscriptionNotification 消息。只有在这个时候，您才应将旧购买令牌替换为新购买令牌，并更新用户对内容的访问权限。如果交易过期或被取消，系统会向您的 RTDN 客户端发送一条类型为 SUBSCRIPTION_PENDING_PURCHASE_CANCELED 的 SubscriptionNotification 消息。在这种情况下，用户应仍有权访问旧订阅的内容。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-11-19。

**Examples:**

Example 1 (unknown):
```unknown
https://play.google.com/store/account/subscriptions
```

Example 2 (unknown):
```unknown
https://play.google.com/store/account/subscriptions
```

Example 3 (unknown):
```unknown
https://play.google.com/store/account/subscriptions?sku=your-sub-product-id&package=your-app-package
```

Example 4 (unknown):
```unknown
https://play.google.com/store/account/subscriptions?sku=your-sub-product-id&package=your-app-package
```

---

## 备选结算系统 API 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/alternative?hl=zh-cn

**Contents:**
- 备选结算系统 API 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 术语词汇表
- 提供需用户自选的备选结算系统
  - 在 Play 管理中心内进行配置
  - 用户体验
    - 用户选择界面
    - 备选结算系统选项剖析
  - 付款方式的图片素材资源
  - 付款方式变体版本
  - 卡片规范

符合条件的开发者能够在其应用中向某些国家/地区的用户提供备选结算系统，并向 Google 报告最终交易。根据分发应用的国家/地区和资格条件，您的应用可以构建两个版本的备选结算系统：

本指南介绍了提供上述任一结算系统需要使用的 API。您在使用这些 API 之前，应先查看计划页面并加入相关计划。

本部分介绍了在已提供 Google Play 结算系统这一选项的情况下，如何为用户提供备选结算系统。使用这些 API 之前，请确保以下几点：

Google Play 结算服务集成推荐模块的其余部分与开发者当前集成中所含的内容相同。

此外，我们建议您完成 Google Play Developer API 集成设置，因为后端集成将用到它。

如果开发者已完成相应需用户自选的备选结算系统计划的注册流程，并集成了备选结算系统 API，则可以通过 Play 管理中心来管理其备选结算系统设置：

用户选择界面会向用户提供选项，以便其选用开发者的备选结算系统或 Google Play 结算系统。

用户选择界面上的备选结算系统选项包括以下界面元素：

单个图片素材资源由多张付款方式卡片组成，且必须遵循下方准则中定义的规范。

开发者可以选择希望在图片素材资源中包含的可用付款方式图标数量，最多 5 个。

图片素材资源中包含的付款方式卡片必须遵循以下关于大小、间距和样式的准则。

如需开始集成备选结算系统 API（需用户自选），请遵循应用内集成和后端集成的深度指南。

本部分介绍了在不提供 Google Play 结算系统这一选项的情况下，如何为用户提供备选结算系统。使用这些 API 之前，请确保以下几点：

建议您完成 Google Play Developer API 集成设置，因为后端集成将用到它。

如果开发者已完成注册流程，并集成了备选结算系统 API，则可以通过 Play 管理中心来管理其备选结算系统设置：

信息界面有助于用户了解符合条件的应用内仅提供备选结算系统。添加备选结算系统后，系统会在用户开始进行首次购买交易时向其显示该信息界面。同一用户使用同一设备在您的应用中进行后续购买交易时，系统不会向其显示此消息。请注意，在某些情况下（例如用户清除了设备上的缓存），系统可能会再次向用户显示该对话框。

如需开始集成备选结算系统 API，请遵循应用内集成和后端集成的深度指南。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

---

## Google Play 结算库版本废弃 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/deprecation-faq?hl=zh-cn

**Contents:**
- Google Play 结算库版本废弃 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 不同版本的支持时间表

正如 2019 年 Google I/O 大会和 Google Play 结算库版本 3 博文所宣布的，所有版本的 Play 结算库都将遵循两年的废弃周期。

本主题回答了关于结算库版本废弃和迁移到更高版本的常见问题。

将您版本中的依赖项更新为使用表中指示的支持版本。如需了解各版本之间有哪些变化，请参阅版本说明。

此外，我们还提供了关于如何迁移到 PBL 8 的深度指南。

如果我想在 11 月 1 日之前继续向所有 Google Play 用户分发应用，在哪里可以找到延期表单？

如果您的应用仍在使用已过时的 Play 结算库版本，您将在 Play 管理中心内收到警告和收件箱消息。可通过相应警告或问题的详情页面（位于 Play 管理中心的政策状态页面）找到延期表单。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

---

## 仅适用于备选结算系统的应用内集成指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/alternative/alternative-billing-without-user-choice-in-app

**Contents:**
- 仅适用于备选结算系统的应用内集成指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- Play 结算库设置
- 连接到 Google Play
  - Kotlin
  - Java
- 检查可用性
  - Kotlin
  - Java
- 面向用户的信息对话框
  - Kotlin

本指南介绍了如何集成相关 API，以便在符合条件的应用中提供仅限备选结算系统（即无需用户自选）的结算方式。如需详细了解相关计划（包括资格要求和地理范围），请参阅备选结算系统简介。

向您的 Android 应用添加 Play 结算库依赖项。如需使用备选结算系统 API，您需要使用 6.1 或更高版本。

集成流程的最初步骤与 Google Play 结算服务集成指南中所述的一些步骤相同，在初始化您的 BillingClient 时需进行一些调整：

以下示例演示了如何通过这些调整来初始化 BillingClient：

初始化 BillingClient 后，您需要按照集成指南中的说明与 Google Play 建立连接。

您的应用应通过调用 isAlternativeBillingOnlyAvailableAsync 来确认可以使用仅限备选结算系统的结算方式。

如果可以使用仅限备选结算系统的结算方式，此 API 将返回 BillingResponseCode.OK。如需详细了解您的应用应如何响应其他响应代码，请参阅响应处理部分。

如需集成仅限备选结算系统的结算方式，符合条件的应用必须显示一个信息界面，以帮助用户了解结算将不受 Google Play 的管理。每次启动备选结算流程之前，必须通过调用 showAlternativeBillingOnlyInformationDialog API 向用户显示此信息界面。如果用户已确认该对话框，此 API 通常不会再次显示该对话框。但在某些情况下（例如用户清除了设备上的缓存），系统可能会再次向用户显示该对话框。

如果此方法返回 BillingResponseCode.OK，您的应用可以继续进行交易。如果返回 BillingResponseCode.USER_CANCELED，您的应用应调用 showAlternativeBillingOnlyInformationDialog 以再次向用户显示该对话框。如需了解其他响应代码，请参阅“响应处理”部分。

通过备选结算系统进行的所有交易都必须在 24 小时内从后端调用 Google Play Developer API 并提供 externalTransactionToken（使用下文介绍的 API 获取），向 Google Play 报告相应交易。每笔一次性购买交易、每项新订阅以及对现有订阅的任何升级/降级都应生成新的 externalTransactionToken。如需了解在获取 externalTransactionToken 后如何报告交易，请参阅后端集成指南。

如果出现错误，上述方法 isAlternativeBillingOnlyAvailableAsync(), showAlternativeBillingOnlyInformationDialog() 和 createAlternativeBillingOnlyReportingDetailsAsync() 可能会返回非 BillingResponseCode.OK 响应。建议按如下所述的方法处理错误：

许可测试人员应该用于测试备选结算系统集成。您 对于许可测试人员发起的交易，系统不会开具账单 账号。如需了解详情，请参阅使用应用许可测试应用内购结算功能 了解如何配置许可测试人员

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

**Examples:**

Example 1 (unknown):
```unknown
var billingClient = BillingClient.newBuilder(context)
    .enableAlternativeBillingOnly()
    .build()
```

Example 2 (unknown):
```unknown
var billingClient = BillingClient.newBuilder(context)
    .enableAlternativeBillingOnly()
    .build()
```

Example 3 (unknown):
```unknown
private BillingClient billingClient = BillingClient.newBuilder(context)
    .enableAlternativeBillingOnly()
    .build();
```

Example 4 (unknown):
```unknown
private BillingClient billingClient = BillingClient.newBuilder(context)
    .enableAlternativeBillingOnly()
    .build();
```

---

## 购买生命周期和 RTDN 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/lifecycle?hl=zh-cn

**Contents:**
- 购买生命周期和 RTDN 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 构建实时开发者通知客户端
  - RTDN 发布端
  - RTDN 订阅端
- 处理购买状态转换

当您通过应用销售数字商品时，必须考虑用户体验的方方面面。借助应用内集成，您可以启动购买流程并管理用户体验，但请务必确保您的后端能及时了解用户购买交易的最新权限。这对于跟踪购买交易以及管理用户体验的其他方面（例如跨平台权限）而言非常重要。

如需监控购买生命周期事件并快速响应用户权限的变化，您应该在后端为订阅和一次性购买交易构建购买交易状态管理系统。这个系统可确保无论设备状态如何，都能快速安全地处理购买交易，在所有平台上维持一致的用户权限，并能够在后端查询交易记录和权限数据。

Google Play 提供实时开发者通知 (RTDN)，可监控购买生命周期事件。如需根据这些事件执行必要的操作，请使用适用于订阅和应用内购买的 Play Developer API。只要使用这些工具并构建完善的购买生命周期管理系统，您就可以提供无缝的用户体验，并高效地管理购买交易和权限。

在 Google Play 结算系统上进行的购买交易可能会在其生命周期中发生多次权限更改。许多操作都可能触发这些更改，包括：

后端必须了解购买交易可能会经历的不同状态，并据此采取所有必要的措施来及时调整权限。

虽然可以使用 Google Play Developer API 手动检查购买交易状态，但通过定期检查来跟踪更改，不仅效率不高，并且容易出错和发生延迟。RTDN 有助于您立即响应更改，且无需为 Google Play 购买交易构建生命周期跟踪逻辑。

本部分介绍如何为 RTDN 构建客户端。RTDN 是使用 Google Cloud Pub/Sub 构建的一个功能，可在用户权限状态发生变化时，向后端发送即时通知。Pub/Sub 系统包括发送通知的发布端和订阅通知的客户端。通过实现 RTDN，您可以实时跟踪并及时响应用户权限状态的所有变化。

Google Play 的后端可充当 RTDN 的发布端。如需为您的应用设置 RTDN，请按照设置指南中的说明操作。完成这些步骤后，Google Play 结算系统就能充当您应用的 RTDN 发布端。如需完成此设置，您应熟悉 Google Cloud Platform Console，以设置基本的 Pub/Sub 配置。

设置完发布端之后，您应该为自己的后端做好使用 RTDN 的准备。为此，您需要构建一个客户端来接收 Google Cloud Pub/Sub 消息。RTDN 客户端的基本功能包括接收 PubSubMessage 实例，方法为使用已注册端点中的 HTTPS 请求，或使用 Cloud Pub/Sub 客户端库。如需了解如何使用推送或拉取策略，请参阅 Pub/Sub 文档。如需了解如何选择最符合需求的策略，请参阅 RTDN 设置文档。

对于您收到的每条消息，您的后端都应执行以下操作：

一次性购买和订阅购买交易具有不同的生命周期，具体取决于会影响它们的不同状态和事件。得益于 RTDN，您无需构建逻辑即可确认状态转换。您需要做的是定义后端收到各类通知时会发生的情况。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

---

## 针对外部优惠计划的应用内集成指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/external/integration?hl=zh-cn

**Contents:**
- 针对外部优惠计划的应用内集成指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- Play 结算库设置
- 连接到 Google Play
  - Kotlin
  - Java
- 查看空房情况
  - Kotlin
  - Java
- 准备外部交易令牌
  - Kotlin

本指南介绍了如何集成 API 以支持外部优惠 在符合条件的应用和地区推出。详细了解外部优惠计划 包括资格要求和地理范围，请参阅 计划要求。

如需使用外部优惠 API，请执行以下操作： 添加 6.2.1 版或更高版本的 Play 结算库依赖项 您的 Android 应用如果您需要从早期版本迁移，请按照 请参阅迁移指南中的说明，然后再尝试实施 外部优惠。

集成流程的最初步骤与 结算集成指南中有一些建议， 初始化 BillingClient：

以下示例演示了如何通过这些调整来初始化 BillingClient：

初始化 BillingClient 后，您需要按照集成指南中的说明与 Google Play 建立连接。

您的应用应通过调用 isExternalOfferAvailableAsync。

如果有外部优惠，此 API 会返回 BillingResponseCode.OK。 如需详细了解您的应用应如何处理，请参阅响应处理 对其他响应代码进行响应。

要向 Google Play 报告外部交易，您必须拥有一个外部 Play 结算库生成的交易令牌。新的外部 每次用户访问外部 通过外部优惠 API 访问网站。这可以通过调用 createExternalOfferReportingDetailsAsync API。此令牌应为 系统会在用户被定向到应用外部紧接着生成它应该 永不缓存，并且每次引导用户时都应生成一个新的密钥 。

如需与外部优惠集成，符合条件的应用必须显示相关信息 这个界面可以帮助用户了解 将应用关联到外部网站信息屏幕必须通过 先调用 showExternalOfferInformationDialog API，然后再链接到 每次外部优惠

如果此方法返回 BillingResponseCode.OK，您的应用可以继续 将用户定向到外部网站。如果该方法返回 BillingResponseCode.USER_CANCELED，您的应用不得继续打开 网站。

所有外部交易都必须报告给 Google Play 从后端调用 Google Play Developer API。外部交易 同时提供 externalTransactionToken 通过 createExternalOfferReportingDetailsAsync API。如果用户多次提交 购买时，您可以使用 externalTransactionToken来报告每笔购买交易。要了解如何举报 请参阅后端集成指南。

发生错误时，isExternalOfferAvailableAsync 方法、 createExternalOfferReportingDetailsAsync和 showExternalOfferInformationDialog 可能会返回 BillingResponseCode.OK。请考虑按如下方式处理这些响应代码：

许可测试人员应该用于测试外部优惠集成。您 对于许可测试人员发起的交易，系统不会开具账单 账号。如需了解详情，请参阅使用应用许可测试应用内购结算功能 了解如何配置许可测试人员

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

**Examples:**

Example 1 (unknown):
```unknown
var billingClient = BillingClient.newBuilder(context)
  .enableExternalOffer()
  .build()
```

Example 2 (unknown):
```unknown
var billingClient = BillingClient.newBuilder(context)
  .enableExternalOffer()
  .build()
```

Example 3 (unknown):
```unknown
private BillingClient billingClient = BillingClient.newBuilder(context)
    .enableExternalOffer()
    .build();
```

Example 4 (unknown):
```unknown
private BillingClient billingClient = BillingClient.newBuilder(context)
    .enableExternalOffer()
    .build();
```

---

## 促销代码 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/promo

**Contents:**
- 促销代码 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 创建和管理促销活动
- 用户兑换流程
- 实现促销代码
- 深层链接
- 测试促销代码

利用促销活动或促销代码，您可以向数量有限的用户免费提供一次性商品或试订服务。用户在您的应用或 Google Play 商店应用中输入促销代码，即可免费获得相应的商品或试订服务。

在 Play 管理中心内，您可以创建以下类型的促销代码：

您可以充分发挥创意，使用促销代码以多种方式来吸引用户，这些方式包括：

在您于 Play 管理中心指定的促销活动结束日期之前，用户可以随时在 Google Play 商店中兑换促销代码。促销活动最长可以持续一年。

如需了解如何设置和管理促销活动，请参阅创建促销活动。

用户获得促销代码后，可通过以下某种方式进行兑换：

例如，图 1 显示了订阅的购买屏幕。如需输入促销代码，请点按当前付款方式旁边的箭头以显示付款方式屏幕，如图 2 所示。接下来，点按兑换代码以转到兑换礼品卡或促销代码屏幕，如图 3 所示。您随后可以在此屏幕上输入促销代码，点按“兑换”即可完成。

为了确保应用已经准备好处理促销代码，应用需要正确处理发生在应用之外的兑换。如需了解详情，请参阅将 Google Play 结算库集成到您的应用中里的处理购买交易、提取购买交易和处理在您的应用外进行的购买交易部分。

您也可以生成一个网址，使用户转到 Google Play 商店并自动填写输入代码字段，由此分享促销代码。促销代码网址采用以下格式：

图 4 显示了 Google Play 应用的兑换代码对话框：

用户按兑换后，如果安装了应用的最新版本，Google Play 商店会提示用户打开该应用。否则，Google Play 商店会提示用户更新或下载您的应用。

如需测试您的促销代码实现，请参阅测试促销代码。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

**Examples:**

Example 1 (unknown):
```unknown
https://play.google.com/redeem?code=promo_code
```

Example 2 (unknown):
```unknown
https://play.google.com/redeem?code=promo_code
```

---

## 更改订阅价格 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/price-changes?hl=zh-cn

**Contents:**
- 更改订阅价格 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 新订阅购买交易的价格变动
- 现有订阅者的价格变动
- 停用旧价格同类群组
  - 使用 Google Play Developer API 停用旧价格同类群组
- 价格下调
- 价格上调
- 通知用户价格变动
- 处理用户选择接受价格变动的响应
- 意外的价格上调

您可以更改订阅基础方案和优惠的价格。例如，您可能有需要调整价格的数字产品，或者您可能会更改产品的某组福利并希望在价格中反映这些变化。

如需了解如何使用 Play 管理中心更改订阅价格，请参阅 Play 管理中心帮助中心内的相关文档。

如需程序化地更改订阅基础方案价格，请使用 monetization.subscriptions.patch 方法。此方法会收到包含要更改的订阅产品配置的 Subscription 对象。在订阅的 basePlans 集合内相应基础方案下的 RegionalBasePlanConfig 对象中设置新价格。如果您的产品清单规模庞大，并且您需要在短时间内更新所有产品，或者有产品清单管理系统在发生更改时自动更改您的 Google Play 订阅产品，那么这么设置很有用。

建议您访问 Play 管理中心的更新日志，查找过往的价格变动相关信息。您可以在其中找到的信息包括价格更新时间、发起变更的用户、更新的地区等。当您需要查看过去的价格变动或意外的价格变动，以评估后续步骤时，这样做可能会很有帮助。

当您更改基础方案或优惠的价格后，新价格将在几个小时内对所有新购买交易生效，而无需您执行任何其他操作。

默认情况下，当您更改订阅价格时，现有订阅者不会受到影响；这些订阅者会被置于旧价格同类群组中，他们将在续订时继续按原始基础方案价格付费。

您可以根据需要，将现有订阅者调到当前的基础方案价格。此操作称为停用旧价格同类群组。对优惠定价阶段的更改不适用于现有订阅者。对于分期付款订阅，旧版同类群组的价格变动会在有效承诺期结束时生效。您无法更改正在分期付款的用户当前支付的价格。

您可以随时停用旧价格同类群组。您还可以针对每个区域单独执行此操作。如需通过 Play 管理中心停用旧价格，请参阅 Play 管理中心帮助中心。

如需程序化地停用旧价格同类群组，请使用 monetization.subscriptions.basePlans.migratePrices 方法。此方法会将接收历史订阅价格的订阅者迁移到指定地区的当前基础方案价格。该方法还将触发价格变更通知，并发送给当前接收早于所提供时间戳的历史价格的用户。发送此请求时，请在请求正文中添加 RegionalPriceMigrationConfig 对象列表，以配置价格同类群组迁移。

如需详细了解如何使用旧价格同类群组，请参阅 Play 管理中心帮助中心。

当您停用旧价格同类群组，且新购买价格低于同类群组中用户支付的价格时，Google Play 会通过电子邮件通知用户，同时这些订阅者会在下次支付基础方案的费用时，开始享受更低的价格。

注意：在用户的下一个续订周期开始前，系统最多可能会提前 48 小时发起付款授权验证。不过，对于印度或巴西的用户，此期限会延长至下一个续订周期开始前最多 5 天。对于之前已按较高价格获得授权的用户，系统不会立即按较低价格扣款；他们将在下次续订时按较低价格续订。

许可测试人员也会收到价格下调的电子邮件通知。

当您停用旧价格同类群组，且新价格高于同类群组中用户支付的价格时，即表示价格上调。价格上调时，用户不一定要采取行动。

默认情况下，现有订阅者需“选择接受”价格上调。在首次收费之前，用户必须明确接受较高的价格，否则 Google Play 会自动取消其订阅。在 37 天的提前通知期结束后，用户在下次为基础方案付费时，必须按更高的价格付费。从扣款前的 30 天开始，Play 会通过电子邮件和推送通知告知现有订阅者。

在触发同类群组迁移的前七天内，Google Play 不会向用户发送通知。这意味着，从您推出“用户选择接受才生效”类型的价格上调起，您将有 7 天时间来通知现有订阅者，之后 Google Play 才会开始直接通知他们。在此期间，您可以再次改回原始价格，有效取消待处理的价格上调。

7 天过后，每位用户均会在首次以新价格续订的前 30 天，收到 Google Play 的自动通知。

在某些情况下，面向现有订阅者上调价格时，您可以选择提前通知用户即将涨价，但无需用户采取任何操作。如果选择此选项，除非用户通过更改订阅方案或取消订阅来选择拒绝，否则在提前通知期结束后，用户下次必须按新价格支付基础方案的费用。此期限因国家/地区而异，可以是 30 天或 60 天。视该期限的时长而定，Play 会从扣款前的 30 天或 60 天开始，通过电子邮件和推送通知告知现有订阅者。

“用户选择拒绝才无效”类型的价格上调仅适用于特定地区，并且对调价幅度和频率设有限制，还需要遵守特定的开发者规定。

如果旧价格同类群组迁移符合这些条件，您可以将其标记为“用户选择拒绝才无效”类型的价格上调，如图 1 所示。

无论何时停用旧价格同类群组，您都应通知现有订阅者。

对于“用户选择拒绝才无效”类型的价格上调，您应该提前通知用户，并向用户显示应用内通知。不同于“用户选择接受才生效”类型的价格上调，Google Play 会直接通知用户，没有七天的等待期。

对于“用户选择接受才生效”类型的价格上调，请提前通知用户，告知他们需要接受价格上调。从您推出“用户选择接受才生效”类型的价格上调起，您将有 7 天时间来通知现有订阅者，之后 Google Play 才会开始直接通知他们。我们建议您在应用中通知受影响的用户，并提供指向 Play 商店订阅界面的深层链接，以便他们轻松查看新价格。当用户在 Play 商店订阅界面上查看“用户选择接受才生效”类型的价格上调时，系统会显示一个类似于图 2 的对话框。

您向现有订阅者通知价格变动并说明它是“用户选择接受才生效”类型的价格上调后，他们可能会在新价格生效之前采取行动，选择是否接受价格上调。如果他们采取行动，系统会向您发送 RTDN 来告知您结果。请参阅购买生命周期指南，了解如何处理这些通知。

如果用户没有采取行动，且在“用户选择接受才生效”的价格生效之前，就到了首次续订日期，那么订阅会自动取消，并会在续订日期当天到期。

“用户选择接受才生效”类型的价格上调 - 如果您意外推出了“用户选择接受才生效”类型的价格上调，只需将价格调回原价，即可立即撤消更改。

将基础方案价格改回原价，然后前往旧版价格点页面，发起将价格降至原价的请求。如果价格在七天内还原，现有订阅者就不会收到有关意外价格变动的通知。如果价格在七天后还原为旧价格，则对于尚未支付新价格的任何用户，价格变动都将被取消。在最长五天的付款授权期限过后，价格变动会被取消。根据续订日期，部分用户可能已收到选择加入电子邮件通知。

用户拒绝才无效的价格上调 - 您可以将价格恢复为原价，以取消意外发起的“用户拒绝才无效的价格上调”。将基础方案价格改回原价，然后前往旧价格点页面，发起将价格下调至原价的操作。如果用户尚未支付上调后的价格，则价格恢复时间取决于付款授权期限（最长为 5 天）。在此期限过后，系统会取消价格上调。根据续订日期，部分用户可能已经收到了价格上涨通知电子邮件。

价格降低 - 您可以使用 Google Play 管理中心将订阅的价格恢复为原始值，从而取消价格降低。将基础方案价格改回原价，然后前往“旧价位”页面，将价格上调至原价。开发者可以发起选择启用或停用（如果符合条件）来取消价格下调。如果使用选择停用，则会将其计入频次。Google Play 会根据此反转操作相对于相应用户个人续订日期的时机，确定取消操作是否对该用户的下一次续订有效。

如果将价格恢复为原价的时间与用户按新价格续订的预期时间之间的间隔超过了相关国家/地区的特定通知期限（30 天或 60 天），则价格降幅取消有效。用户下次续订时，系统会按原来的较高价格收费。

如果将价格恢复为原价的时间与用户按新价格续订的预期时间之间的间隔短于或等于相关国家/地区的特定通知期限（30 天或 60 天），则价格降幅取消无效。用户在下次续订时至少按较低价格付费一次后，才会进入价格上调流程。然后，用户会收到有关价格上调的通知。 根据价格迁移期间选择的模式，用户需要接受“用户接受才生效的价格上调”，或者会收到有关“用户拒绝才无效的价格上调”的通知。在这种情况下，任何有关选择停用后增加的频次和金额限制都将适用。

确保一次只进行 1 次价格调整。不过，如果您在更改某一价格时进行了多次调整，受影响的用户只需同意最新的价格调整。例如，如果您已停用实施“用户接受才生效的价格上调”的旧版价格同类群组，接着再次调整价格，然后再次实施“用户接受才生效的价格上调”，那么受影响的用户无需响应第一次价格上调，因为现在只会应用第二次价格上调。此行为适用于旧版“用户接受才生效”和“用户拒绝才无效”类型的价格上调和价格下调。

如果您为正在进行旧版价格迁移的商品启动新的价格迁移，Google Play 会按如下方式处理：

Google Play 会停止旧价格迁移。在 SubscriptionPurchaseV2 API 中，您会看到标记为 CANCELED 的旧价格变动详情。您还会收到 SUBSCRIPTION_PRICE_CHANGE_UPDATED RTDN。

紧接着，Google Play 会开始迁移到新价格。这将在 SubscriptionPurchaseV2 中显示为 OUTSTANDING（对于“用户接受才生效”类型的价格上调）或 CONFIRMED（对于“用户拒绝才无效”类型的价格上调或价格下调）。您会收到另一条针对相应商品的 SUBSCRIPTION_PRICE_CHANGE_UPDATED RTDN。

用户现在将迁移到新的价格，并且不会完成之前的价格变动。用户会收到有关新价格的标准通知期。

请勿出于测试目的而更改有效订阅者所拥有的商品的订阅价格。

您可以使用 Play 结算服务实验室应用并配备许可测试人员，来测试订阅价格变动，而不会影响其他活跃订阅者。

如需详细了解如何测试价格变动，请参阅测试指南。

本部分中的示例演示了如何在不同的价格变动场景中应用最佳实践。

在 3 月 3 日，AltoStrat 通过结束旧价格同类群组，上调了付费视频在线播放订阅 AltoStrat Pro 的价格。他们将旧价格同类群组中的 1 美元用户转移到当前的 2 美元基础方案价格。价格变动的生效日期为 4 月 9 日（3 月 3 日之后的 37 天）。

Alice 是现有订阅者，下次续订日期为 3 月 5 日。生效日期之后的第一次续订日期为 5 月 5 日，因此她在 3 月 5 日和 4 月 5 日按旧价格（1 美元）续订。当她在 5 月 5 日再次续订时，则按新价格（2 美元）支付费用。Google Play 将于 4 月 5 日（即采用新价格的首次续订日期前 30 天）开始通知 Alice 价格变动。

Bob 是现有订阅者，下次续订日期为 3 月 29 日。由于价格变动尚未生效，因此他在 3 月 29 日以旧价格（1 美元）续订。当他在 4 月 29 日再次续订时，则按新价格（2 美元）支付费用。他于 3 月 30 日（即采用新价格的首次续订日期前 30 天）开始收到价格变动通知。

在 3 月 3 日，FindMyLove 结束了旧价格同类群组，将 FindMyLove Premium 的 3 个月费用从 1 美元上调至 2 美元的基础方案价格。价格变动的生效日期为 4 月 9 日（3 月 3 日之后的 37 天）。

Alice 是现有订阅者，下次续订日期为 3 月 5 日。Alice 以旧价格（1 美元）续订，因为价格变动尚未生效。当她在 6 月 5 日再次续订时，则按新价格（2 美元）支付费用。她于 5 月 6 日（即采用新价格的首次续订日期前 30 天）开始收到价格变动通知。

Bob 是现有订阅者，下次续订日期为 4 月 11 日。Bob 会按新价格（2 美元）续订，因为该日期晚于价格变动的生效日期。他于 3 月 12 日（即采用新价格的首次续订日期前 30 天）开始收到价格变动通知。

在 3 月 3 日，CutePetsNews 结束了旧价格同类群组，将 Weekly Dog Alerts 的每周费用从 1 美元上调至 2 美元。价格变动的生效日期为 4 月 9 日。

Alice 是现有订阅者，下周续订的时间是 3 月 6 日。她于 3 月 6 日、3 月 13 日、3 月 20 日、3 月 27 日和 4 月 3 日以旧价格（1 美元）续订，因为价格变动尚未生效。当她在 4 月 10 日再次续订时，则按新价格（2 美元）支付费用。她于 3 月 11 日（即采用新价格的首次续订日期前 30 天）开始收到价格变动通知。

在 3 月 3 日，AltoStrat 变动了其付费视频订阅 AltoStrat Pro，将价格从每月 1 美元上调至 2 美元。在 3 月 10 日，开发者再次触发了价格变动，将价格上调至每月 3 美元。

首次价格变动的生效日期为 4 月 9 日（3 月 3 日之后的 37 天）。第二次价格变动的生效日期为 4 月 16 日（3 月 10 日之后的 37 天）。

Alice 的下次续订日期是 3 月 5 日。生效日期之后的第一次续订日期为 5 月 5 日，因此她在 3 月 5 日和 4 月 5 日按旧价格（1 美元）续订。当她在 5 月 5 日再次续订时，则按最新价格（3 美元）支付费用。由于价格变动发生在 7 天冻结期内，因此她仅会收到第二次价格变动的通知。她于 4 月 5 日（即采用新价格的首次续订日期前 30 天）开始收到价格变动的通知。

此示例展示了如何处理分期付款订阅的价格上调。

在 3 月 3 日，AltoStrat 通过结束旧价格同类群组，上调了付费视频在线播放订阅 AltoStrat Pro 的价格。他们将旧价格同类群组中的 1 美元用户转移到当前的 2 美元基础方案价格。价格变动的生效日期为 4 月 9 日（3 月 3 日之后的 37 天）。

Alice 是现有订阅者，她在上一年 6 月 10 日订阅了 12 个月的分期付款方案，之后改为按月自动续订。她的首次续订日期为当年 6 月 10 日。由于 Alice 正在分期付款，因此她会在 3 月 10 日、4 月 10 日和 5 月 10 日继续支付 1 美元。她在 6 月 10 日首次续订，并按新价格（2 美元）支付费用，同时改为按月自动续订。Google Play 将于 5 月 11 日（即采用新价格的首次续订日期前 30 天）开始通知 Alice 价格变动。

此示例展示了如何处理选择拒绝价格上调的情况。

因编程费用不断增加，AltoStrat 需要每年调整价格。在 1 月 2 日，他们将 AltoStrat Pro（付费视频在线播放订阅）的价格从 1 美元上调至 1.30 美元。此价格上调符合“用户选择拒绝才无效”类型的价格迁移的条件。他们会立即停用旧价格同类群组，并指定“用户选择拒绝才无效”类型的迁移。根据此同类群组中用户所在地区的规定，必须设有至少 30 天的选择停用通知期，因此新价格将于 2 月 1 日生效。

Alice 是现有订阅者，收费日为每个月的 14 号。由于通知期限至少 30 天，因此她会在 1 月 14 日按旧价格（1 美元）支付费用。Google Play 从 1 月 15 日开始通知 Alice，并于 2 月 14 日开始按新价格（1.30 美元）向她收费。

本部分中的价格上调同意示例仅适用于韩国 (KR) 地区。

3 月 3 日，韩国境内的用户订阅了某项服务，并获得了 10 天的免费试用期。用户在注册时同意价格逐步上调。在这种情况下，Play 会在 3 月 13 日应用价格上调。

3 月 3 日，韩国境内的用户订阅了某项服务，并获得了 10 天的免费试用期。用户在注册或免费试用期间未同意价格上调。以下是此场景中的事件序列：

3 月 3 日，韩国境内的用户订阅了某项服务，并获得了 10 天的免费试用期。用户在免费试用期间同意价格上调。以下是此方案中的事件序列：

3 月 3 日，韩国境内的用户订阅了某个方案，该方案的促销价格期为 60 天。用户在注册时不同意价格上调。以下是此场景中的事件序列：

如果您同时为订阅提供免费试用和初次体验优惠，Play 会在以下情况下征求用户同意：

例如，某用户于 3 月 3 日在韩国境内订阅了某项服务，该服务提供 10 天的免费试用期和 30 天的初次体验价期。 用户在免费试用期和初次体验价期间均同意价格上调。以下是此场景中的事件序列：

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-09-11。

---

## 一次性购买生命周期 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/lifecycle/one-time?hl=zh-cn

**Contents:**
- 一次性购买生命周期 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 新的一次性商品购买交易
  - 实时开发者通知
  - 处理已完成的交易
  - 处理已取消的交易
- 在后端处理一次性商品购买交易

相较于订阅商品，一次性购买商品的生命周期更为简单，但您的后端仍然需要能够妥善处理多种状态和转换事件。

用户完成结算流程后，您的应用可以通过以下方式之一查看新购买交易的相关信息：

收到新的购买交易后，请使用 getPurchaseState 方法或 purchases.productsv2.getproductpurchasev2 in Play Developer API

当用户购买或取消购买一次性商品时，Google Play 会发送 OneTimeProductNotification 消息。如需更新后端购买交易状态，请使用 OneTimeProductNotification 对象中提供的购买令牌来调用 purchases.productsv2.getproductpurchasev2 方法。此方法可提供指定购买令牌的最新购买和消费状态。

当预订商品完成配送且其购买状态更改为 PURCHASED 时，系统会向您的客户端发送 RTDN。收到 RTDN 后，请按照在后端处理一次性商品购买交易中所述的方式处理预订购买交易。

您应在安全的后端中处理与交易相关的 RTDN。

当用户完成一次性商品购买交易时，Google Play 会发送一条类型为 ONE_TIME_PRODUCT_PURCHASED 的 OneTimeProductNotification 消息。收到此 RTDN 后，请按照在后端处理一次性商品购买交易中所述的方式处理购买交易。

如果您已配置为接收实时开发者通知，那么当一次性商品购买交易被取消时，Google Play 会发送一条类型为 ONE_TIME_PRODUCT_CANCELED 的 OneTimeProductNotification 消息。例如，如果用户未在规定的时间范围内完成付款，或者开发者或客户请求撤消购买交易，就可能会发生这种情况。当您的后端服务器收到此通知时，请调用 purchases.productsv2.getproductpurchasev2 方法来获取最新的购买交易状态，然后据此更新后端，包括用户权限。

如果处于 Purchased 状态的一次性商品购买交易发生退款，您也会通过 Voided Purchases API 获知。

无论您是通过 ONE_TIME_PRODUCT_PURCHASED RTDN 检测新的购买交易，通过 PurchasesUpdatedListener 获知应用内购买交易，还是在应用内以 onResume() 方法手动提取购买交易，您都必须处理新的购买交易。我们建议您在后端处理购买交易，以提高安全性。

如要处理新的一次性购买交易，请按以下步骤操作：

Play 结算库中还提供了购买交易确认和消耗方法，可让您通过应用处理购买交易，但如果您可以在后端进行处理，我们建议您采用这种更安全的实现方法。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

---

## 更改订阅价格 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/price-changes

**Contents:**
- 更改订阅价格 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 新订阅购买交易的价格变动
- 现有订阅者的价格变动
- 停用旧价格同类群组
  - 使用 Google Play Developer API 停用旧价格同类群组
- 价格下调
- 价格上调
- 通知用户价格变动
- 处理用户选择接受价格变动的响应
- 意外的价格上调

您可以更改订阅基础方案和优惠的价格。例如，您可能有需要调整价格的数字产品，或者您可能会更改产品的某组福利并希望在价格中反映这些变化。

如需了解如何使用 Play 管理中心更改订阅价格，请参阅 Play 管理中心帮助中心内的相关文档。

如需程序化地更改订阅基础方案价格，请使用 monetization.subscriptions.patch 方法。此方法会收到包含要更改的订阅产品配置的 Subscription 对象。在订阅的 basePlans 集合内相应基础方案下的 RegionalBasePlanConfig 对象中设置新价格。如果您的产品清单规模庞大，并且您需要在短时间内更新所有产品，或者有产品清单管理系统在发生更改时自动更改您的 Google Play 订阅产品，那么这么设置很有用。

建议您访问 Play 管理中心的更新日志，查找过往的价格变动相关信息。您可以在其中找到的信息包括价格更新时间、发起变更的用户、更新的地区等。当您需要查看过去的价格变动或意外的价格变动，以评估后续步骤时，这样做可能会很有帮助。

当您更改基础方案或优惠的价格后，新价格将在几个小时内对所有新购买交易生效，而无需您执行任何其他操作。

默认情况下，当您更改订阅价格时，现有订阅者不会受到影响；这些订阅者会被置于旧价格同类群组中，他们将在续订时继续按原始基础方案价格付费。

您可以根据需要，将现有订阅者调到当前的基础方案价格。此操作称为停用旧价格同类群组。对优惠定价阶段的更改不适用于现有订阅者。对于分期付款订阅，旧版同类群组的价格变动会在有效承诺期结束时生效。您无法更改正在分期付款的用户当前支付的价格。

您可以随时停用旧价格同类群组。您还可以针对每个区域单独执行此操作。如需通过 Play 管理中心停用旧价格，请参阅 Play 管理中心帮助中心。

如需程序化地停用旧价格同类群组，请使用 monetization.subscriptions.basePlans.migratePrices 方法。此方法会将接收历史订阅价格的订阅者迁移到指定地区的当前基础方案价格。该方法还将触发价格变更通知，并发送给当前接收早于所提供时间戳的历史价格的用户。发送此请求时，请在请求正文中添加 RegionalPriceMigrationConfig 对象列表，以配置价格同类群组迁移。

如需详细了解如何使用旧价格同类群组，请参阅 Play 管理中心帮助中心。

当您停用旧价格同类群组，且新购买价格低于同类群组中用户支付的价格时，Google Play 会通过电子邮件通知用户，同时这些订阅者会在下次支付基础方案的费用时，开始享受更低的价格。

注意：在用户的下一个续订周期开始前，系统最多可能会提前 48 小时发起付款授权验证。不过，对于印度或巴西的用户，此期限会延长至下一个续订周期开始前最多 5 天。对于之前已按较高价格获得授权的用户，系统不会立即按较低价格扣款；他们将在下次续订时按较低价格续订。

许可测试人员也会收到价格下调的电子邮件通知。

当您停用旧价格同类群组，且新价格高于同类群组中用户支付的价格时，即表示价格上调。价格上调时，用户不一定要采取行动。

默认情况下，现有订阅者需“选择接受”价格上调。在首次收费之前，用户必须明确接受较高的价格，否则 Google Play 会自动取消其订阅。在 37 天的提前通知期结束后，用户在下次为基础方案付费时，必须按更高的价格付费。从扣款前的 30 天开始，Play 会通过电子邮件和推送通知告知现有订阅者。

在触发同类群组迁移的前七天内，Google Play 不会向用户发送通知。这意味着，从您推出“用户选择接受才生效”类型的价格上调起，您将有 7 天时间来通知现有订阅者，之后 Google Play 才会开始直接通知他们。在此期间，您可以再次改回原始价格，有效取消待处理的价格上调。

7 天过后，每位用户均会在首次以新价格续订的前 30 天，收到 Google Play 的自动通知。

在某些情况下，面向现有订阅者上调价格时，您可以选择提前通知用户即将涨价，但无需用户采取任何操作。如果选择此选项，除非用户通过更改订阅方案或取消订阅来选择拒绝，否则在提前通知期结束后，用户下次必须按新价格支付基础方案的费用。此期限因国家/地区而异，可以是 30 天或 60 天。视该期限的时长而定，Play 会从扣款前的 30 天或 60 天开始，通过电子邮件和推送通知告知现有订阅者。

“用户选择拒绝才无效”类型的价格上调仅适用于特定地区，并且对调价幅度和频率设有限制，还需要遵守特定的开发者规定。

如果旧价格同类群组迁移符合这些条件，您可以将其标记为“用户选择拒绝才无效”类型的价格上调，如图 1 所示。

无论何时停用旧价格同类群组，您都应通知现有订阅者。

对于“用户选择拒绝才无效”类型的价格上调，您应该提前通知用户，并向用户显示应用内通知。不同于“用户选择接受才生效”类型的价格上调，Google Play 会直接通知用户，没有七天的等待期。

对于“用户选择接受才生效”类型的价格上调，请提前通知用户，告知他们需要接受价格上调。从您推出“用户选择接受才生效”类型的价格上调起，您将有 7 天时间来通知现有订阅者，之后 Google Play 才会开始直接通知他们。我们建议您在应用中通知受影响的用户，并提供指向 Play 商店订阅界面的深层链接，以便他们轻松查看新价格。当用户在 Play 商店订阅界面上查看“用户选择接受才生效”类型的价格上调时，系统会显示一个类似于图 2 的对话框。

您向现有订阅者通知价格变动并说明它是“用户选择接受才生效”类型的价格上调后，他们可能会在新价格生效之前采取行动，选择是否接受价格上调。如果他们采取行动，系统会向您发送 RTDN 来告知您结果。请参阅购买生命周期指南，了解如何处理这些通知。

如果用户没有采取行动，且在“用户选择接受才生效”的价格生效之前，就到了首次续订日期，那么订阅会自动取消，并会在续订日期当天到期。

“用户选择接受才生效”类型的价格上调 - 如果您意外推出了“用户选择接受才生效”类型的价格上调，只需将价格调回原价，即可立即撤消更改。

将基础方案价格改回原价，然后前往旧版价格点页面，发起将价格降至原价的请求。如果价格在七天内还原，现有订阅者就不会收到有关意外价格变动的通知。如果价格在七天后还原为旧价格，则对于尚未支付新价格的任何用户，价格变动都将被取消。在最长五天的付款授权期限过后，价格变动会被取消。根据续订日期，部分用户可能已收到选择加入电子邮件通知。

用户拒绝才无效的价格上调 - 您可以将价格恢复为原价，以取消意外发起的“用户拒绝才无效的价格上调”。将基础方案价格改回原价，然后前往旧价格点页面，发起将价格下调至原价的操作。如果用户尚未支付上调后的价格，则价格恢复时间取决于付款授权期限（最长为 5 天）。在此期限过后，系统会取消价格上调。根据续订日期，部分用户可能已经收到了价格上涨通知电子邮件。

价格降低 - 您可以使用 Google Play 管理中心将订阅的价格恢复为原始值，从而取消价格降低。将基础方案价格改回原价，然后前往“旧价位”页面，将价格上调至原价。开发者可以发起选择启用或停用（如果符合条件）来取消价格下调。如果使用选择停用，则会将其计入频次。Google Play 会根据此反转操作相对于相应用户个人续订日期的时机，确定取消操作是否对该用户的下一次续订有效。

如果将价格恢复为原价的时间与用户按新价格续订的预期时间之间的间隔超过了相关国家/地区的特定通知期限（30 天或 60 天），则价格降幅取消有效。用户下次续订时，系统会按原来的较高价格收费。

如果将价格恢复为原价的时间与用户按新价格续订的预期时间之间的间隔短于或等于相关国家/地区的特定通知期限（30 天或 60 天），则价格降幅取消无效。用户在下次续订时至少按较低价格付费一次后，才会进入价格上调流程。然后，用户会收到有关价格上调的通知。 根据价格迁移期间选择的模式，用户需要接受“用户接受才生效的价格上调”，或者会收到有关“用户拒绝才无效的价格上调”的通知。在这种情况下，任何有关选择停用后增加的频次和金额限制都将适用。

确保一次只进行 1 次价格调整。不过，如果您在更改某一价格时进行了多次调整，受影响的用户只需同意最新的价格调整。例如，如果您已停用实施“用户接受才生效的价格上调”的旧版价格同类群组，接着再次调整价格，然后再次实施“用户接受才生效的价格上调”，那么受影响的用户无需响应第一次价格上调，因为现在只会应用第二次价格上调。此行为适用于旧版“用户接受才生效”和“用户拒绝才无效”类型的价格上调和价格下调。

如果您为正在进行旧版价格迁移的商品启动新的价格迁移，Google Play 会按如下方式处理：

Google Play 会停止旧价格迁移。在 SubscriptionPurchaseV2 API 中，您会看到标记为 CANCELED 的旧价格变动详情。您还会收到 SUBSCRIPTION_PRICE_CHANGE_UPDATED RTDN。

紧接着，Google Play 会开始迁移到新价格。这将在 SubscriptionPurchaseV2 中显示为 OUTSTANDING（对于“用户接受才生效”类型的价格上调）或 CONFIRMED（对于“用户拒绝才无效”类型的价格上调或价格下调）。您会收到另一条针对相应商品的 SUBSCRIPTION_PRICE_CHANGE_UPDATED RTDN。

用户现在将迁移到新的价格，并且不会完成之前的价格变动。用户会收到有关新价格的标准通知期。

请勿出于测试目的而更改有效订阅者所拥有的商品的订阅价格。

您可以使用 Play 结算服务实验室应用并配备许可测试人员，来测试订阅价格变动，而不会影响其他活跃订阅者。

如需详细了解如何测试价格变动，请参阅测试指南。

本部分中的示例演示了如何在不同的价格变动场景中应用最佳实践。

在 3 月 3 日，AltoStrat 通过结束旧价格同类群组，上调了付费视频在线播放订阅 AltoStrat Pro 的价格。他们将旧价格同类群组中的 1 美元用户转移到当前的 2 美元基础方案价格。价格变动的生效日期为 4 月 9 日（3 月 3 日之后的 37 天）。

Alice 是现有订阅者，下次续订日期为 3 月 5 日。生效日期之后的第一次续订日期为 5 月 5 日，因此她在 3 月 5 日和 4 月 5 日按旧价格（1 美元）续订。当她在 5 月 5 日再次续订时，则按新价格（2 美元）支付费用。Google Play 将于 4 月 5 日（即采用新价格的首次续订日期前 30 天）开始通知 Alice 价格变动。

Bob 是现有订阅者，下次续订日期为 3 月 29 日。由于价格变动尚未生效，因此他在 3 月 29 日以旧价格（1 美元）续订。当他在 4 月 29 日再次续订时，则按新价格（2 美元）支付费用。他于 3 月 30 日（即采用新价格的首次续订日期前 30 天）开始收到价格变动通知。

在 3 月 3 日，FindMyLove 结束了旧价格同类群组，将 FindMyLove Premium 的 3 个月费用从 1 美元上调至 2 美元的基础方案价格。价格变动的生效日期为 4 月 9 日（3 月 3 日之后的 37 天）。

Alice 是现有订阅者，下次续订日期为 3 月 5 日。Alice 以旧价格（1 美元）续订，因为价格变动尚未生效。当她在 6 月 5 日再次续订时，则按新价格（2 美元）支付费用。她于 5 月 6 日（即采用新价格的首次续订日期前 30 天）开始收到价格变动通知。

Bob 是现有订阅者，下次续订日期为 4 月 11 日。Bob 会按新价格（2 美元）续订，因为该日期晚于价格变动的生效日期。他于 3 月 12 日（即采用新价格的首次续订日期前 30 天）开始收到价格变动通知。

在 3 月 3 日，CutePetsNews 结束了旧价格同类群组，将 Weekly Dog Alerts 的每周费用从 1 美元上调至 2 美元。价格变动的生效日期为 4 月 9 日。

Alice 是现有订阅者，下周续订的时间是 3 月 6 日。她于 3 月 6 日、3 月 13 日、3 月 20 日、3 月 27 日和 4 月 3 日以旧价格（1 美元）续订，因为价格变动尚未生效。当她在 4 月 10 日再次续订时，则按新价格（2 美元）支付费用。她于 3 月 11 日（即采用新价格的首次续订日期前 30 天）开始收到价格变动通知。

在 3 月 3 日，AltoStrat 变动了其付费视频订阅 AltoStrat Pro，将价格从每月 1 美元上调至 2 美元。在 3 月 10 日，开发者再次触发了价格变动，将价格上调至每月 3 美元。

首次价格变动的生效日期为 4 月 9 日（3 月 3 日之后的 37 天）。第二次价格变动的生效日期为 4 月 16 日（3 月 10 日之后的 37 天）。

Alice 的下次续订日期是 3 月 5 日。生效日期之后的第一次续订日期为 5 月 5 日，因此她在 3 月 5 日和 4 月 5 日按旧价格（1 美元）续订。当她在 5 月 5 日再次续订时，则按最新价格（3 美元）支付费用。由于价格变动发生在 7 天冻结期内，因此她仅会收到第二次价格变动的通知。她于 4 月 5 日（即采用新价格的首次续订日期前 30 天）开始收到价格变动的通知。

此示例展示了如何处理分期付款订阅的价格上调。

在 3 月 3 日，AltoStrat 通过结束旧价格同类群组，上调了付费视频在线播放订阅 AltoStrat Pro 的价格。他们将旧价格同类群组中的 1 美元用户转移到当前的 2 美元基础方案价格。价格变动的生效日期为 4 月 9 日（3 月 3 日之后的 37 天）。

Alice 是现有订阅者，她在上一年 6 月 10 日订阅了 12 个月的分期付款方案，之后改为按月自动续订。她的首次续订日期为当年 6 月 10 日。由于 Alice 正在分期付款，因此她会在 3 月 10 日、4 月 10 日和 5 月 10 日继续支付 1 美元。她在 6 月 10 日首次续订，并按新价格（2 美元）支付费用，同时改为按月自动续订。Google Play 将于 5 月 11 日（即采用新价格的首次续订日期前 30 天）开始通知 Alice 价格变动。

此示例展示了如何处理选择拒绝价格上调的情况。

因编程费用不断增加，AltoStrat 需要每年调整价格。在 1 月 2 日，他们将 AltoStrat Pro（付费视频在线播放订阅）的价格从 1 美元上调至 1.30 美元。此价格上调符合“用户选择拒绝才无效”类型的价格迁移的条件。他们会立即停用旧价格同类群组，并指定“用户选择拒绝才无效”类型的迁移。根据此同类群组中用户所在地区的规定，必须设有至少 30 天的选择停用通知期，因此新价格将于 2 月 1 日生效。

Alice 是现有订阅者，收费日为每个月的 14 号。由于通知期限至少 30 天，因此她会在 1 月 14 日按旧价格（1 美元）支付费用。Google Play 从 1 月 15 日开始通知 Alice，并于 2 月 14 日开始按新价格（1.30 美元）向她收费。

本部分中的价格上调同意示例仅适用于韩国 (KR) 地区。

3 月 3 日，韩国境内的用户订阅了某项服务，并获得了 10 天的免费试用期。用户在注册时同意价格逐步上调。在这种情况下，Play 会在 3 月 13 日应用价格上调。

3 月 3 日，韩国境内的用户订阅了某项服务，并获得了 10 天的免费试用期。用户在注册或免费试用期间未同意价格上调。以下是此场景中的事件序列：

3 月 3 日，韩国境内的用户订阅了某项服务，并获得了 10 天的免费试用期。用户在免费试用期间同意价格上调。以下是此方案中的事件序列：

3 月 3 日，韩国境内的用户订阅了某个方案，该方案的促销价格期为 60 天。用户在注册时不同意价格上调。以下是此场景中的事件序列：

如果您同时为订阅提供免费试用和初次体验优惠，Play 会在以下情况下征求用户同意：

例如，某用户于 3 月 3 日在韩国境内订阅了某项服务，该服务提供 10 天的免费试用期和 30 天的初次体验价期。 用户在免费试用期和初次体验价期间均同意价格上调。以下是此场景中的事件序列：

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-09-11。

---

## 在 Unity 项目中使用 Google Play 结算库 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/unity?hl=zh-cn

**Contents:**
- 在 Unity 项目中使用 Google Play 结算库 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
  - 设置 Google Play 结算服务插件
    - 启用 Unity IAP 抽象层
    - 下载并导入插件
    - 配置构建设置
    - 启用插件
- 在游戏中实现 Google Play 结算库功能
  - 启用推迟购买功能
  - 向 Google Play 传递经过混淆处理的账号 ID
  - 向 Google Play 传递经过混淆处理的个人资料 ID

Google Play 结算服务插件扩展了 Unity 的应用内购买内置服务和资产（名为 Unity IAP），可以为您的游戏提供 Google Play 结算库的所有最新功能。本指南介绍了如何设置您的项目以使用此插件，以及如何在通过 Unity 开发的游戏中实现 Google Play 结算库功能。

如需设置此插件，请完成以下每个链接部分中的步骤：

Google Play 结算服务插件基于 Unity IAP 中自带的抽象层，因此您需要启用此抽象层后才能下载并导入该插件。如需启用 Unity IAP 抽象层，请执行以下操作：

插件将作为 .unitypackage 格式的 Unity 软件包提供。如需下载并导入插件，请按以下步骤操作：

在 Unity 菜单栏中，依次点击 Assets > Import Package > Custom Package。

找到 .unitypackage 文件的下载位置并选择该文件。

在 Import Unity Package 对话框中，选择所有资产并点击 Import。

软件包导入后，系统会在项目的资产中添加一个名为 GooglePlayPlugins 的新文件夹（位于 Assets 文件夹的根目录下）。此文件夹包含该插件的所有 Google Play 结算库资源。

由于插件扩展了 Unity IAP，因此除非从 build 中移除 Unity IAP 中一些较旧的重叠依赖项，否则 Unity 会遇到冲突且无法构建 Android APK。插件提供了一种从项目中自动移除冲突库的方法。如需解决这些冲突，请按以下步骤操作：

从 Unity 菜单栏中依次选择 Google > Play Billing > Build Settings。

在“Play Billing Build Settings”窗口中，点击 Fix。这样就可以解决冲突并将冲突的 Unity IAP 文件移至备份目录。点击 Fix 后，该按钮会变成 Restore，点击后可恢复原始的冲突文件。

如需启用插件，请将 Google Play 的 Unity IAP 实现替换为 Google Play 结算服务插件。例如，使用 Unity IAP 购买者脚本时，您要更改传递到 IAP 构建器中的 StandardPurchaseModule 以使用 Google.Play.Billing.GooglePlayStoreModule：

如果您的游戏将同一个购买者脚本用于多个平台，应添加一项平台检查，确保 Unity 针对其他平台继续使用自己的 IAP 解决方案：

如果您在除 Google Play 商店以外的其他 Android 应用商店中发布游戏，则只有在选择 Google Play 商店时才应替换默认的 Unity IAP 实现：

Google Play 结算服务插件扩展了 Unity IAP 服务，因此您可以使用相同的 Unity API 管理通用的购买流程。请注意，由于 Google Play 结算库与其他应用商店的 Unity 标准 IAP 实现之间存在差异，因此 API 行为也发生了一些细微变化。如果您刚开始接触 Unity IAP API，请参阅 Unity IAP 教程中的“Making a Purchase Script”部分，通过示例了解如何实现基本购买流程。

Google Play 结算库还包含一些 Google Play 商店独有的功能。您可以通过扩展接口访问这些功能。本部分的其余内容介绍了如何在游戏中实现这些独有的 Google Play 结算库功能。

Google Play 支持推迟购买（也称为待处理的交易或待处理的购买交易），在这种情况下，用户可以创建购买交易并稍后在实体店中使用现金完成购买交易。

如需启用推迟购买功能，请在 IAP 构建器中调用 EnableDeferredPurchase() 方法修改模块配置：

接下来，使用 Play 商店扩展程序实现推迟购买回调：

您可以向 Google Play 传递经过混淆处理的用户账号 ID 以方便检测滥用行为，例如检测是否有大量设备在短时间内使用同一账号进行购买。

如需传递经过混淆处理的账号 ID，请从扩展程序 API 调用 SetObfuscatedAccountId() 方法：

您可以向 Google Play 传递经过混淆处理的个人资料 ID 以方便检测欺诈行为，例如检测是否有大量设备在短时间内使用同一账号进行购买。这与传递经过混淆处理的用户账号 ID 类似。在这两种情况下，ID 都代表单个用户，但是个人资料 ID 可以帮助您从单个应用中的多份个人资料里唯一识别出单个用户。向 Google Play 传递经过混淆处理的个人资料 ID 后，您日后便可以在购买交易收据中检索此 ID。

如需传递经过混淆处理的个人资料 ID，请在 IAP 构建器中调用 SetObfuscatedProfileId() 方法修改模块配置：

您可以通过 Google Play 更改有效订阅的价格。游戏的用户必须先确认任何价格变动，然后更改才能生效。如需提示用户确认其订阅的价格变动，请调用 ConfirmSubscriptionPriceChange() 方法：

在您使用 Google Play 结算服务插件时，大多数 API 行为与其他应用商店的 Unity 标准 IAP 实现的行为相同。但在某些情况下，API 的行为会有所不同。本部分介绍了这些行为差异。

Google Play 已废弃开发者载荷，并用更有意义且更相关的替代方法代替它。因此，API 不支持开发者载荷。如需详细了解替代方法，请参阅开发者载荷 的相关页面。

您可以继续在其他应用商店中使用 Unity 标准 IAP 实现所定义的接口，包括 IStoreController。当您提示购买时，您仍可使用 IStoreController 并调用 InitiatePurchase() 方法：

但是，您传入的任何载荷都不会生效（不会出现在最终收据中）。

Unity IAP 提供了用于管理订阅的 SubscriptionManager 类。由于此类的 Unity 标准 IAP 实现使用开发者载荷，因此不支持此类。您仍然可以创建此类，但是当您使用该类的任何 getter 方法时，您可能会收到不可靠的数据。

Google Play 结算服务插件不支持使用 SubscriptionManager.UpdateSubscription() 和 SubscriptionManager.UpdateSubscriptionInGooglePlayStore() 方法升级和降级您的订阅。如果您的游戏调用了这些方法，系统会抛出 GooglePlayStoreUnsupportedException。

Google Play 结算库提供了一个替代 API 来代替这些方法。如需升级或降级订阅，请调用使用按比例计费模式的 UpdateSubscription() 方法：

您可以用平台检查封装此方法调用，也可以在捕获 GooglePlayStoreUnsupportedException 时将其封装在 catch 块中。

如需了解按比例计费模式的详细使用方法和示例，请参阅设置按比例计费模式。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-11-10。

**Examples:**

Example 1 (unknown):
```unknown
// Create a builder using the GooglePlayStoreModule.
var configurationBuilder =
    ConfigurationBuilder.Instance(Google.Play.Billing.GooglePlayStoreModule.Instance());
```

Example 2 (unknown):
```unknown
// Create a builder using the GooglePlayStoreModule.
var configurationBuilder =
    ConfigurationBuilder.Instance(Google.Play.Billing.GooglePlayStoreModule.Instance());
```

Example 3 (unknown):
```unknown
ConfigurationBuilder builder;
if (Application.platform == RuntimePlatform.Android)
{
  builder = ConfigurationBuilder.Instance(
      Google.Play.Billing.GooglePlayStoreModule.Instance());
}
else
{
  builder = ConfigurationBuilder.Instance(StandardPurchasingModule.Instance());
}
```

Example 4 (unknown):
```unknown
ConfigurationBuilder builder;
if (Application.platform == RuntimePlatform.Android)
{
  builder = ConfigurationBuilder.Instance(
      Google.Play.Billing.GooglePlayStoreModule.Instance());
}
else
{
  builder = ConfigurationBuilder.Instance(StandardPurchasingModule.Instance());
}
```

---

## Google Play 结算库的其他开发者资源 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/additional-resources

**Contents:**
- Google Play 结算库的其他开发者资源 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 视频
- 博文和其他文章
- Google Play 应用开发者学院

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

---

## 实时开发者通知参考指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/rtdn-reference

**Contents:**
- 实时开发者通知参考指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 编码
- SubscriptionNotification
  - 示例
- OneTimeProductNotification
  - 示例
- VoidedPurchaseNotification
  - 示例
  - 使用 VoidedPurchaseNotification
- TestNotification

本文档列出并描述了您可以从 Google Play 收到的 实时开发者通知的类型。

发布到 Cloud Pub/Sub 主题的每条消息都包含一个以 base64 编码的数据字段。

对以 base64 编码的数据字段进行解码后，DeveloperNotification 包含以下字段：

SubscriptionNotification 包含以下字段：

OneTimeProductNotification 包含以下字段：

VoidedPurchaseNotification 包含以下字段：

与作废的购买交易关联的令牌。当有新的购买交易发生时，系统会向开发者提供此信息。

与作废的交易关联的唯一订单 ID。对于一次性购买，此字段代表了为这笔购买交易生成的唯一订单 ID。对于自动续订型订阅，系统会为每笔续订交易生成一个新的订单 ID。

作废的购买交易的 productType 可以具有以下值：

作废的购买交易的 refundType 可以具有以下值：

请注意，当多数量购买交易的剩余总数量得到退款时，refundType 将为 REFUND_TYPE_FULL_REFUND。

当您的 RTDN 客户端收到 VoidedPurchaseNotification 时，请注意以下信息：

TestNotification 包含以下字段：

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

**Examples:**

Example 1 (unknown):
```unknown
{
  "message": {
    "attributes": {
      "key": "value"
    },
    "data": "eyAidmVyc2lvbiI6IHN0cmluZywgInBhY2thZ2VOYW1lIjogc3RyaW5nLCAiZXZlbnRUaW1lTWlsbGlzIjogbG9uZywgIm9uZVRpbWVQcm9kdWN0Tm90aWZpY2F0aW9uIjogT25lVGltZVByb2R1Y3ROb3RpZmljYXRpb24sICJzdWJzY3JpcHRpb25Ob3RpZmljYXRpb24iOiBTdWJzY3JpcHRpb25Ob3RpZmljYXRpb24sICJ0ZXN0Tm90aWZpY2F0aW9uIjogVGVzdE5vdGlmaWNhdGlvbiB9",
    "messageId": "136969346945"
  },
  "subscription": "projects/myproject/subscriptions/mysubscription"
}
```

Example 2 (unknown):
```unknown
{
  "message": {
    "attributes": {
      "key": "value"
    },
    "data": "eyAidmVyc2lvbiI6IHN0cmluZywgInBhY2thZ2VOYW1lIjogc3RyaW5nLCAiZXZlbnRUaW1lTWlsbGlzIjogbG9uZywgIm9uZVRpbWVQcm9kdWN0Tm90aWZpY2F0aW9uIjogT25lVGltZVByb2R1Y3ROb3RpZmljYXRpb24sICJzdWJzY3JpcHRpb25Ob3RpZmljYXRpb24iOiBTdWJzY3JpcHRpb25Ob3RpZmljYXRpb24sICJ0ZXN0Tm90aWZpY2F0aW9uIjogVGVzdE5vdGlmaWNhdGlvbiB9",
    "messageId": "136969346945"
  },
  "subscription": "projects/myproject/subscriptions/mysubscription"
}
```

Example 3 (unknown):
```unknown
{
  "version": string,
  "packageName": string,
  "eventTimeMillis": long,
  "oneTimeProductNotification": OneTimeProductNotification,
  "subscriptionNotification": SubscriptionNotification,
  "voidedPurchaseNotification": VoidedPurchaseNotification,
  "testNotification": TestNotification
}
```

Example 4 (unknown):
```unknown
{
  "version": string,
  "packageName": string,
  "eventTimeMillis": long,
  "oneTimeProductNotification": OneTimeProductNotification,
  "subscriptionNotification": SubscriptionNotification,
  "voidedPurchaseNotification": VoidedPurchaseNotification,
  "testNotification": TestNotification
}
```

---

## 适用于欧洲经济区 (EEA) 计划的无需用户自选的其他结算方式临时用户体验指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/alternative/interim-ux/alt-billing?hl=zh-cn

**Contents:**
- 适用于欧洲经济区 (EEA) 计划的无需用户自选的其他结算方式临时用户体验指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 概览
- 选择语言
- 面向用户的信息
  - 何时显示
  - 何时显示价格
  - 如何显示
  - 用户操作
    - 知道了
    - 了解详情

这些指南面向参与我们计划的开发者，用于向欧洲经济区 (EEA) 的用户提供 Google Play 结算系统之外的其他结算方式，但无需用户自行选择。如果开发者有欧洲经济区 (EEA) 境内的用户，并且参与了用户自选结算方式试行计划，且除了 Google Play 结算系统之外还提供备选结算系统，则应遵循用户自选结算方式用户体验指南。这些用户体验指南旨在要求开发者在每位用户首次发起购买交易时向其显示信息屏幕，从而保持一致的用户体验。应按照以下准则为信息屏幕实现面向用户的消息和界面规范。

选择用户的语言，以便在以下设计规范中查看对应的界面文本字符串。

信息屏幕必须在用户开始进行首次购买时向其显示。当同一用户以后再次进行购买交易时，就不需要再显示该信息了。在用户执行明确操作以发起购买交易之后，系统应立即显示信息屏幕。

应在显示信息屏幕之前，在显眼的位置向用户显示购买价格。

信息屏幕必须显示在模态底部动作条中。模态底部动作条与模态对话框类似，它会从屏幕底部向上呈现动画效果，并固定在屏幕底部。它位于底层屏幕中的所有界面元素的上层。底层屏幕会被深色纱罩遮挡，表示它不会响应用户的任何互动。

如需详细了解模态底部动作条的设计和实现，请参阅 Google Material Design。

当用户点按应用中用于发起购买交易的按钮或其他界面元素时，底部动作条必须触发。用户可以在信息屏幕中执行 2 种可能的操作：

点按“知道了”按钮会关闭信息屏幕，并启动付款流程中的下一个屏幕。

点按“了解详情”按钮可在网络浏览器中打开相应的 Google 帮助中心文章。

如果用户要关闭底部动作条并返回底层屏幕，可以通过以下方式关闭底部动作条：

在用户关闭信息屏幕或点按“知道了”后，无需再次显示信息屏幕。

示例：当用户在应用中点按进行购买时，该按钮会触发信息屏幕。

信息屏幕分为 3 个组件：标题、消息和按钮。所有这 3 个组件都是必需的，其包含的文字和界面元素必须与本指南中的定义完全一致。请勿在该屏幕中添加任何其他文字或图像，但您可以在其他屏幕中添加额外的文字和图像。

在横向视图中，底部动作条的宽度大于纵向视图中的宽度，但在其他方面都遵循相同的设计规范和功能。

如需进一步了解适用于欧洲经济区 (EEA) 计划的无需用户自选的其他结算方式和常见问题解答，请访问我们的帮助中心。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

---

## 备选结算系统 API 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/alternative

**Contents:**
- 备选结算系统 API 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 术语词汇表
- 提供需用户自选的备选结算系统
  - 在 Play 管理中心内进行配置
  - 用户体验
    - 用户选择界面
    - 备选结算系统选项剖析
  - 付款方式的图片素材资源
  - 付款方式变体版本
  - 卡片规范

符合条件的开发者能够在其应用中向某些国家/地区的用户提供备选结算系统，并向 Google 报告最终交易。根据分发应用的国家/地区和资格条件，您的应用可以构建两个版本的备选结算系统：

本指南介绍了提供上述任一结算系统需要使用的 API。您在使用这些 API 之前，应先查看计划页面并加入相关计划。

本部分介绍了在已提供 Google Play 结算系统这一选项的情况下，如何为用户提供备选结算系统。使用这些 API 之前，请确保以下几点：

Google Play 结算服务集成推荐模块的其余部分与开发者当前集成中所含的内容相同。

此外，我们建议您完成 Google Play Developer API 集成设置，因为后端集成将用到它。

如果开发者已完成相应需用户自选的备选结算系统计划的注册流程，并集成了备选结算系统 API，则可以通过 Play 管理中心来管理其备选结算系统设置：

用户选择界面会向用户提供选项，以便其选用开发者的备选结算系统或 Google Play 结算系统。

用户选择界面上的备选结算系统选项包括以下界面元素：

单个图片素材资源由多张付款方式卡片组成，且必须遵循下方准则中定义的规范。

开发者可以选择希望在图片素材资源中包含的可用付款方式图标数量，最多 5 个。

图片素材资源中包含的付款方式卡片必须遵循以下关于大小、间距和样式的准则。

如需开始集成备选结算系统 API（需用户自选），请遵循应用内集成和后端集成的深度指南。

本部分介绍了在不提供 Google Play 结算系统这一选项的情况下，如何为用户提供备选结算系统。使用这些 API 之前，请确保以下几点：

建议您完成 Google Play Developer API 集成设置，因为后端集成将用到它。

如果开发者已完成注册流程，并集成了备选结算系统 API，则可以通过 Play 管理中心来管理其备选结算系统设置：

信息界面有助于用户了解符合条件的应用内仅提供备选结算系统。添加备选结算系统后，系统会在用户开始进行首次购买交易时向其显示该信息界面。同一用户使用同一设备在您的应用中进行后续购买交易时，系统不会向其显示此消息。请注意，在某些情况下（例如用户清除了设备上的缓存），系统可能会再次向用户显示该对话框。

如需开始集成备选结算系统 API，请遵循应用内集成和后端集成的深度指南。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

---

## 2022 年 5 月订阅变更指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/compatibility?hl=zh-cn

**Contents:**
- 2022 年 5 月订阅变更指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 订阅配置
  - 通过 Google Play 管理中心管理订阅
  - 通过 Subscriptions Publishing API 管理订阅
- Play 结算库变更
- 管理订阅状态
  - 实时开发者通知
  - Subscriptions Purchases API：获取订阅状态
    - 预付费方案的 SubscriptionPurchaseV2 字段
    - 周期性订阅的 SubscriptionPurchaseV2 字段

Google Play 结算系统是一项可让您在 Android 应用中销售数字商品和内容的服务。在 2022 年 5 月的版本中，我们更改了订阅商品的定义方式，这项变更将影响您在应用内销售和在后端管理订阅商品的方式。如果您是首次集成 Google Play 结算服务，可以阅读做好准备来开始集成。

如果您在 2022 年 5 月之前一直通过 Google Play 结算服务销售订阅内容，请务必了解如何在保留现有订阅的情况下采用新功能。

首先要知道的是，您的所有现有订阅、应用和后端集成的工作方式与 2022 年 5 月的版本之前相同。您不必立即做出更改，可以逐步采用这些新功能。每个主要版本的 Google Play 结算库在发布后都有两年支持期。与 Google Play Developer API 的现有集成将继续像以前一样工作。

下面概括介绍了 2022 年 5 月的更新：

自 2022 年 5 月起，Google Play 管理中心会出现一些变化。

单个订阅现在可以有多个基础方案和优惠。以前创建的订阅 SKU 现在会在 Play 管理中心内显示为这些新的订阅、基础方案和优惠对象。请参阅 Play 管理中心内订阅方面的近期变更（如果您尚未查看相关内容），查看有关这些新对象的说明（包括其功能和配置）。此前已有的所有订阅商品都会以这种新格式显示于 Google Play 管理中心内。现在，每个 SKU 都以一个订阅对象表示，该对象包含一个基础方案和向后兼容的优惠（如有）。

由于较旧的集成要求每个订阅包含一个优惠（以 SkuDetails 对象表示），因此每个订阅可以有一个向后兼容的基础方案或优惠。如果应用使用的是现已废弃的 querySkuDetailsAsync() 方法，向后兼容的基础方案或优惠将作为 SKU 的一部分返回。如需详细了解如何配置和管理向后兼容的优惠，请参阅了解订阅。待您的应用仅使用 queryProductDetailsAsync() 并且没有旧版应用仍在进行购买后，您就无需再使用向后兼容的优惠了。

Play Developer API 包含订阅购买方面的新功能。用于 SKU 管理的 inappproducts API 将继续像以前一样工作，包括处理一次性购买商品和订阅，因此您无需立即做出任何更改，即可保留您的集成。

但请务必注意，Google Play 管理中心仅使用新的订阅实体。在管理中心开始修改订阅后，inappproducts API 将无法再用于订阅。

如果您在 2022 年 5 月之前使用过 Publishing API，为避免任何问题，所有现有订阅现在都会在 Google Play 管理中心内显示为只读状态。如果您尝试进行更改，可能会收到说明此限制的警告。在管理中心进一步修改订阅之前，您应该更新后端集成，以使用新的订阅发布端点。新的 monetization.subscriptions、monetization.subscriptions.baseplans 和 monetization.subscriptions.offers 端点可让您管理所有可用的基础方案和优惠。您可以在下表中看到不同字段如何从 InAppProduct 实体映射到 monetization.subscriptions 下的新对象：

这项必需的 API 更新仅适用于 Publishing API（SKU 管理）。

为了支持逐步迁移，Play 结算库囊括了以前的版本中提供的所有方法和对象。SkuDetails 对象和函数（例如 querySkuDetailsAsync()）仍然存在，因此您可以通过升级使用新功能，而不必立即更新现有订阅代码。您还可以通过这些方法将相关优惠标记为向后兼容，从而控制哪些优惠可用。

除了保留旧方法之外，Play 结算库 5 现在还添加了一个新的 ProductDetails 对象和一个对应的 queryProductDetailsAsync() 方法，用于处理新的实体和功能。现在，ProductDetails 也支持现有的应用内商品（一次性购买和消耗品）。

对于订阅，ProductDetails.getSubscriptionOfferDetails() 会返回一个列表，列出用户符合购买条件的所有基础方案和优惠。这意味着，您可以访问用户符合购买条件的所有基础方案和优惠，无论其向后兼容性如何。对于非订阅商品，getSubscriptionOfferDetails() 会返回 null。对于一次性购买，您可以使用 getOneTimePurchaseOfferDetails()。

Play 结算库 5 还包含用于启动购买流程的新方法和旧方法。如果使用 SkuDetails 对象配置传递给 BillingClient.launchBillingFlow() 的 BillingFlowParams 对象，系统会从与 SKU 相对应的向后兼容基础方案或优惠中提取销售信息。如果使用 ProductDetailsParams 对象配置传递给 BillingClient.launchBillingFlow() 的 BillingFlowParams 对象，因为前者包含 ProductDetails 和一个表示购买交易专用优惠令牌的 String，所以系统会使用该信息标识用户将获得的商品。

queryPurchasesAsync() 会返回用户拥有的所有购买交易。如需指明所请求的商品类型，您可以传入一个 BillingClient.SkuType 值（与旧版本一样）或一个 QueryPurchasesParams 对象（包含一个表示新订阅实体的 BillingClient.ProductType 值）。

我们建议您尽快将您的应用更新到该库的版本 5，以便您开始充分利用这些新的订阅功能。

本部分将介绍迁移到版本 5 需要实现的 Google Play 结算系统集成后端组件的主要变更。

很快，SubscriptionNotification 对象将不再包含 subscriptionId。如果您依靠此字段来标识订阅商品，应进行更新，以便在收到通知后使用 purchases.subscriptionv2:get 从订阅状态中获取此信息。作为购买状态的一部分返回的 lineItems 集合中的每个 SubscriptionPurchaseLineItem 元素都将包含相应的 productId。

在以前版本的 Subscriptions Purchases API 中，您可以使用 purchases.subscriptions:get 查询订阅状态。此端点保持不变，仍将适用于向后兼容的订阅购买。此端点不支持 2022 年 5 月发布的任何新功能。

在新版本的 Subscriptions Purchases API 中，使用 purchases.subscriptionsv2:get 获取订阅购买状态。此 API 与迁移的订阅、新订阅（预付费和自动续订）以及各种类型的购买交易兼容。您可以在收到通知后使用此端点检查订阅状态。返回的对象 SubscriptionPurchaseV2 包含一些新字段，但仍包含继续支持现有订阅所需的旧数据。

为了支持由用户延期而不是自动续订的预付费方案，新增了一些字段。所有字段都适用于预付费方案，正如其适用于自动续订型订阅一样，但以下字段除外：

purchases.subscriptionv2 包含一些新字段，用于提供有关新订阅对象的更多详细信息。下表显示了旧订阅端点中的字段与 purchases.subscriptionv2 中相应字段的对应关系。

虽然 purchases.subscriptions:get 已升级到 purchases.subscriptionsv2:get，但 purchases.subscriptions 端点中的其余开发者订阅管理函数目前保持不变，因此您可以像以前一样继续使用 purchases.subscriptions:acknowledge、purchases.subscriptions:cancel、purchases.subscriptions:defer、purchases.subscriptions:refund 和 purchases.subscriptions:revoke。

您可以使用 monetization.convertRegionPrices 端点计算地区性价格，就像通过 Play 管理中心计算一样。对于可通过 Google Play 进行购买的所有地区，此方法接受 Play 支持的任意币种的单个价格，并返回相应地区的换算价格（包括适用的默认税率）。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

---

## 将 Google Play 结算库集成到您的应用中 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/billing_onetime?hl=zh-cn

**Contents:**
- 将 Google Play 结算库集成到您的应用中 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 购买交易的生命周期
- 初始化与 Google Play 的连接
  - 添加 Google Play 结算库依赖项
  - Groovy
  - Kotlin
  - Groovy
  - Kotlin
  - 初始化 BillingClient
  - Kotlin

本文档介绍了如何将 Google Play 结算库集成到您的应用中以开始销售商品。

订阅会自动续订，直到被取消。订阅可处于下面这几种状态：

与 Google Play 结算系统集成的第一步是将 Google Play 结算库添加到您的应用并初始化连接。

将 Google Play 结算库依赖项添加到应用的 build.gradle 文件中，如下所示：

如果您使用的是 Kotlin，Google Play 结算库 KTX 模块包含了 Kotlin 扩展和协程支持，可让您在使用 Google Play 结算库时编写惯用的 Kotlin 代码。如需将这些扩展包含在项目中，请将以下依赖项添加到应用的 build.gradle 文件中，如下所示：

添加对 Google Play 结算库的依赖项后，您需要初始化 BillingClient 实例。BillingClient 是 Google Play 结算库与应用的其余部分之间进行通信的主接口。BillingClient 为许多常见的结算操作提供了方便的方法，既有同步方法，又有异步方法。请注意以下几点：

如需创建 BillingClient，请使用 newBuilder。您可以将任何上下文传递给 newBuilder()，以供 BillingClient 用于获取应用上下文。这意味着您不必担心内存泄漏。为了接收有关购买交易的更新，您还必须调用 setListener，并传递对 PurchasesUpdatedListener 的引用。此监听器可接收应用中所有购买交易的更新。

创建 BillingClient 后，您需要与 Google Play 建立连接。

如需连接到 Google Play，请调用 startConnection。连接过程是异步进行的，因此您必须实现 BillingClientStateListener，以便在客户端的设置完成后且它准备好发出进一步的请求时接收回调。

此外，您还必须实现重试逻辑，以处理与 Google Play 失去连接的问题。如需实现重试逻辑，请替换 onBillingServiceDisconnected() 回调方法，并确保 BillingClient 先调用 startConnection() 方法以重新连接到 Google Play，然后再发出进一步的请求。

以下示例演示了如何启动连接并测试它是否已准备就绪可供使用：

随着版本 8.0.0 中引入了 BillingClient.Builder 中的 enableAutoServiceReconnection() 方法，如果服务断开连接时进行了 API 调用，Play 结算库现在可以自动重新建立服务连接。由于在进行 API 调用之前，系统会在内部处理重新连接，因此这可能会导致 SERVICE_DISCONNECTED 响应减少。

构建 BillingClient 实例时，请使用 BillingClient.Builder 中的 enableAutoServiceReconnection() 方法来启用自动重新连接。

与 Google Play 建立连接后，您就可以查询可售的商品并将其展示给用户了。

在将商品展示给用户之前，查询商品详情是非常重要的一步，因为查询会返回本地化的商品信息。对于订阅，请验证您的商品展示符合所有 Play 政策。

如需查询一次性商品详情，请调用 queryProductDetailsAsync 方法。此方法可以根据您的一次性商品配置返回多个优惠。如需了解详情，请参阅一次性商品的多项购买选项和优惠。

为了处理该异步操作的结果，您还必须指定实现 ProductDetailsResponseListener 接口的监听器。然后，您可以替换 onProductDetailsResponse，该方法会在查询完成时通知监听器，如以下示例所示：

查询商品详情时，应传递 QueryProductDetailsParams 的实例，用于指定在 Google Play 管理中心内创建的商品 ID 字符串列表以及 ProductType。ProductType 可以是 ProductType.INAPP（针对一次性商品），也可以是 ProductType.SUBS（针对订阅）。

如果您使用 Kotlin 扩展，可以通过调用 queryProductDetails() 扩展函数查询一次性商品详情。

queryProductDetails() 会利用 Kotlin 协程，因此您无需定义单独的监听器。相反，该函数会挂起，直到查询完成，然后您可以处理查询结果：

在极少数情况下，某些设备无法支持 ProductDetails 和 queryProductDetailsAsync()，这通常是因为 Google Play 服务版本已过时。为确保对此场景提供适当的支持，请参阅 Play 结算库版本 7 迁移指南，了解如何使用向后兼容的功能。

Google Play 结算库会将查询结果存储在 QueryProductDetailsResult 对象中。QueryProductDetailsResult 包含 ProductDetails 对象的 List。您随后可以对该列表中的每个 ProductDetails 对象调用各种方法，以查看成功提取的一次性商品的相关信息，如其价格或说明。如需查看可用的商品详情，请参阅 ProductDetails 类中的方法列表。

QueryProductDetailsResult 还包含 UnfetchedProduct 对象的 List。然后，您可以查询每个 UnfetchedProduct，以获取与提取失败原因对应的状态代码。如需查看可用的未提取商品信息，请参阅 UnfetchedProduct 类中的方法列表。

在提供待售商品之前，检查用户是否尚未拥有该商品。如果用户的消耗型商品仍在其商品库中，用户必须先消耗掉该商品，然后才能再次购买。

在提供订阅之前，验证用户是否尚未订阅。此外，还请注意以下事项：

对于订阅，queryProductDetailsAsync() 方法会返回订阅商品详情，并且每项订阅最多包含 50 个用户符合条件的优惠。如果用户尝试购买不符合条件的优惠（例如，应用显示的是过时的可享优惠列表），Play 会通知用户其不符合优惠条件，并且用户可以改为选择购买基础方案。

对于一次性商品，queryProductDetailsAsync() 方法仅返回用户有资格享受的优惠。如果用户尝试购买他们没有资格享受的优惠（例如，用户已达到购买数量上限），Play 会通知用户他们不符合优惠条件，并且用户可以改为选择购买其购买选项优惠。

如需从应用发起购买请求，请从应用的主线程调用 launchBillingFlow() 方法。此方法接受对 BillingFlowParams 对象的引用，该对象包含通过调用 queryProductDetailsAsync 获取的相关 ProductDetails 对象。如需创建 BillingFlowParams 对象，请使用 BillingFlowParams.Builder 类。

launchBillingFlow() 方法会返回 BillingClient.BillingResponseCode 中列出的几个响应代码之一。请务必检查此结果，以验证在启动购买流程时没有错误。BillingResponseCode 为 OK 表示成功启动。

成功调用 launchBillingFlow() 后，系统会显示 Google Play 购买界面。图 1 显示了一项订阅的购买界面：

Google Play 会调用 onPurchasesUpdated()，以将购买操作的结果传送给实现 PurchasesUpdatedListener 接口的监听器。您可以在初始化客户端时使用 setListener() 方法指定监听器。

您必须实现 onPurchasesUpdated() 来处理可能的响应代码。以下示例展示了如何替换 onPurchasesUpdated()：

如果成功购买商品，系统会显示 Google Play 购买成功界面，类似于图 2。

如果成功购买商品，系统还会生成购买令牌，它是一个唯一标识符，表示用户及其所购一次性商品的商品 ID。应用可以在本地存储购买令牌，不过我们强烈建议您将令牌传递到安全的后端服务器，您随后可以在该服务器上验证购买交易及防范欺诈行为。如需详细了解此流程，请参阅检测和处理购买交易。

用户还会收到包含交易收据的电子邮件，收据内含订单 ID 或交易的唯一 ID。用户每次购买一次性商品时，都会收到包含唯一订单 ID 的电子邮件。此外，用户最初购买订阅时以及后续定期自动续订时，也会收到这样的电子邮件。您可以在 Google Play 管理中心内使用订单 ID 来管理退款。

如果应用可能会面向欧盟用户分发，请在调用 launchBillingFlow 时使用 setIsOfferPersonalized() 方法向用户披露您的商品价格已通过自动化决策进行了个性化设置。

您必须参阅《欧盟消费者权益指令》2011/83/EU 6 (1) (ea) CRD 条款，确定您向用户提供的价格是否进行了个性化设置。

setIsOfferPersonalized() 接受布尔值输入。当该值为 true 时，Play 界面会包含披露声明。当该值为 false 时，Play 界面会忽略披露声明。默认值为 false。

当您启动购买流程时，您的应用可以使用 obfuscatedAccountId 或 obfuscatedProfileId 附加您拥有的购买用户的任何用户标识符。标识符示例可以是用户在您系统中的登录名的混淆版本。设置这些参数有助于 Google 检测欺诈行为。此外，它还可以帮助您确保购买交易归因于正确的用户，如向用户授予使用权中所述。

本部分中描述的购买交易检测和处理适用于所有类型的购买交易，包括应用外购买交易（如促销活动兑换）。

您的应用可以通过以下方式之一检测新的购买交易和已完成的待处理购买交易：

对于第 1 步，只要您的应用正在运行并具有有效的 Google Play 结算库连接，系统就会自动针对新购买交易或已完成的购买交易调用 onPurchasesUpdated。如果您的应用未运行，或者您的应用没有有效的 Google Play 结算库连接，则不会调用 onPurchasesUpdated。请注意，建议您的应用在前台运行时，尽可能保持有效连接，以便及时获取购买交易更新。

对于第 2 步，您必须调用 BillingClient.queryPurchasesAsync()，以确保您的应用处理所有购买交易。建议您在应用成功与 Google Play 结算库建立连接时执行此操作（建议在应用启动或进入前台时执行此操作，如初始化 BillingClient 中所述）。为此，您可以在收到 onServiceConnected 的成功结果时调用 queryPurchasesAsync。遵循此建议对于处理以下事件和情况至关重要：

一旦应用检测到新的购买交易或已完成的购买交易，就应执行以下操作：

以下各部分将详细讨论这些步骤，最后一部分将总结所有步骤。

在向用户授予福利之前，您的应用应始终验证购买交易的合法性。为此，您可以按照在授予权利前验证购买交易中所述的准则进行操作。只有在验证购买交易后，您的应用才能继续处理购买交易并向用户授予权利，这将在下一部分中讨论。

应用验证购买交易后，可以继续向用户授予使用权并通知用户。在授予权利之前，请验证您的应用是否正在检查购买交易的状态是否为 PURCHASED。如果购买交易处于 PENDING 状态，您的应用应通知用户，他们仍需完成一些操作才能完成购买交易，然后才能获得相应权利。只有在购买交易从 PENDING 转换为 SUCCESS 时，才授予权利。 如需了解详情，请参阅处理待处理的交易。

如果您已按照附加用户标识符中所述将用户标识符附加到购买交易，则可以检索并使用这些标识符在您的系统中归因给正确的用户。当您的应用可能丢失了有关购买交易是为哪个用户进行的上下文信息时，此方法在协调购买交易方面非常有用。请注意，在您的应用外进行的购买交易不会设置这些标识符。在这种情况下，您的应用可以向已登录的用户授予使用权，也可以提示用户选择首选账号。

对于预订，在到达发布时间之前，购买交易处于“待处理”状态。预订购买交易将在发布时完成，并将状态更改为“已购买”，无需执行其他操作。

在向用户授予使用权后，您的应用应显示一条通知，确认购买交易已成功完成。由于有通知，用户不会对购买交易是否成功完成感到困惑，否则可能会导致用户停止使用您的应用、与用户支持团队联系，或在社交媒体上抱怨。请注意，您的应用可能会在应用生命周期的任何时间检测到购买交易更新。例如，家长在另一部设备上批准了待处理的购买交易，在这种情况下，您的应用可能希望延迟向用户发送通知，直到合适的时间再发送。以下是一些适合使用延迟的示例：

在通知用户有关购买交易时，Google Play 建议采用以下机制：

通知应告知用户其获得的福利。例如，“您购买了 100 个金币！”。此外，如果购买交易是因 Play Pass 等计划的福利而产生的，您的应用会将此信息传达给用户。例如，“已收到商品！您刚刚使用 Play Pass 兑换了 100 颗宝石。 继续。”。每个计划都可能会提供有关向用户显示哪些推荐文本来传达福利的指南。

在您的应用向用户授予使用权并通知用户交易成功后，您的应用需要通知 Google 购买交易已成功处理。为此，您需要确认购买交易，并且必须在三天内完成此操作，以免系统自动退款并撤消相应授权。以下部分介绍了确认不同类型购买交易的流程。

对于消耗型商品，如果您的应用具有安全后端，我们建议您使用 Purchases.products:consume 可靠地消耗所购商品。若要确保所购商品未被消耗掉，请查看 Purchases.products:get 调用结果中的 consumptionState。如果您的应用只有客户端而没有后端，请使用 Google Play 结算库中的 consumeAsync()。这两种方法都符合确认要求，并且表明您的应用已将使用权授予用户。这些方法也支持您的应用提供与输入购买令牌对应的一次性商品，供用户再次购买。如果使用 consumeAsync()，您还必须传递一个实现 ConsumeResponseListener 接口的对象。该对象用于处理消耗操作的结果。您可以替换 onConsumeResponse() 方法，Google Play 结算库会在消耗操作完成时调用该方法。

以下示例展示了如何使用关联的购买令牌，通过 Google Play 结算库来消耗商品：

如需确认非消耗型商品的购买交易，如果您的应用具有安全后端，我们建议您使用 Purchases.products:acknowledge 可靠地确认购买交易。若要确保购买交易尚未确认，请查看 Purchases.products:get 调用结果中的 acknowledgementState。

如果您的应用只有客户端，请在应用中使用 Google Play 结算库中的 BillingClient.acknowledgePurchase()。在确认购买交易之前，您的应用应检查它是否已通过使用 Google Play 结算库中的 isAcknowledged() 方法进行确认。

以下示例展示了如何使用 Google Play 结算库来确认购买交易：

订阅的处理方式与非消耗型商品类似。如果可能，请使用 Google Play Developer API 中的 Purchases.subscriptions.acknowledge 通过安全后端可靠地确认购买交易。若要验证购买交易尚未确认，请通过 Purchases.subscriptions:get 查看购买资源中的 acknowledgementState。另外，您也可以在查看 isAcknowledged() 后，使用 Google Play 结算库中的 BillingClient.acknowledgePurchase() 确认订阅。所有初始订阅购买交易都需要确认。续订购买交易不需要确认。如需详细了解订阅何时需要确认，请参阅销售订阅内容主题。

如需验证您的应用是否已正确实现这些步骤，您可以按照测试指南操作。

Google Play 支持待处理的交易，即从用户发起购买交易到购买交易的付款方式得到处理期间需要执行一个或多个额外步骤的交易。在 Google 通知您已通过用户的付款方式成功扣款之前，您的应用不得授予对这些类型的购买交易的权利。

例如，用户可以选择一家实体店，以便稍后使用现金付款，从而发起交易。用户会通过通知和电子邮件收到一个代码。当用户到达实体店时，可以在收银员处兑换该代码并用现金支付。Google 随后会通知您和用户付款已收到。您的应用随后就可以授予用户权利了。

在初始化 BillingClient 的过程中调用 enablePendingPurchases()，以针对应用启用待处理的交易。应用必须针对一次性商品启用并支持待处理的交易。在添加支持之前，请务必了解待处理交易的购买生命周期。

当应用通过 PurchasesUpdatedListener 或由于调用 queryPurchasesAsync 而收到新的购买交易时，使用 getPurchaseState() 方法确定购买交易的状态是 PURCHASED 还是 PENDING。只有在状态为 PURCHASED 时，您才能授予使用权。

如果您的应用在用户完成购买交易时正在运行，并且您拥有有效的 Play 结算库连接，系统会再次调用 PurchasesUpdatedListener，并且 PurchaseState 现在为 PURCHASED。此时，您的应用可以使用检测和处理购买交易的标准方法处理购买交易。此外，应用还应在其 onResume() 方法中调用 queryPurchasesAsync()，以处理在应用未运行时已转换为 PURCHASED 状态的购买交易。

当购买交易从 PENDING 过渡到 PURCHASED 时，real_time_developer_notifications 客户端会收到 ONE_TIME_PRODUCT_PURCHASED 或 SUBSCRIPTION_PURCHASED 通知。如果购买交易被取消，您会收到 ONE_TIME_PRODUCT_CANCELED 或 SUBSCRIPTION_PENDING_PURCHASE_CANCELED 通知。如果客户没有在规定的时间范围内完成付款，就会发生这种情况。请注意，您始终可以使用 Google Play Developer API 检查购买交易的当前状态。

Google Play 允许客户在一笔交易中购买多件相同的一次性商品，只需在购物车中指定商品数量即可（4.0 及更高版本的 Google Play 结算库支持该功能）。应用应根据指定的购买数量来处理多件购买交易并授予使用权。

为了实现多件购买，应用的配置逻辑需要检查商品数量。您可以通过以下 API 访问 quantity 字段：

添加用于处理多件购买交易的逻辑后，您需要在 Google Play 管理中心的一次性商品管理页面上为相应的商品启用多件购买功能。

getBillingConfigAsync() 提供用户在 Google Play 中使用的国家/地区设置。

您可以在创建 BillingClient 后查询用户的结算配置。以下代码段说明了如何调用 getBillingConfigAsync()。通过实现 BillingConfigResponseListener 来处理响应。此监听器可接收应用中发起的所有结算配置查询的更新。

如果返回的 BillingResult 不含错误，您可以查看 BillingConfig 对象中的 countryCode 字段，以获取用户的 Play 国家/地区信息。

对于通过一次性商品创收的游戏开发者，在 Google Play 管理中心内处于有效状态的库存单位 (SKU) 可在您的应用之外销售，方法是使用“弃购提醒”功能，该功能会在用户浏览 Google Play 商店时提醒他们完成之前放弃的购买交易。这些购买交易发生在您的应用之外，即在 Google Play 商店的 Google Play Games 首页中。

此功能默认处于启用状态，可帮助用户从上次中断的地方继续观看，并帮助开发者最大限度地提高销售额。不过，您可以提交“弃购提醒”功能停用表单，为您的应用停用此功能。 如需了解在 Google Play 管理中心内管理 SKU 的最佳实践，请参阅创建应用内商品。

以下图片展示了在 Google Play 商店中显示的购物车遗弃提醒：

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

**Examples:**

Example 1 (python):
```python
dependencies {
    def billing_version = "8.0.0"

    implementation "com.android.billingclient:billing:$billing_version"
}
```

Example 2 (unknown):
```unknown
dependencies {
    val billing_version = "8.0.0"

    implementation("com.android.billingclient:billing:$billing_version")
}
```

Example 3 (python):
```python
dependencies {
    def billing_version = "8.0.0"

    implementation "com.android.billingclient:billing-ktx:$billing_version"
}
```

Example 4 (unknown):
```unknown
dependencies {
    val billing_version = "8.0.0"

    implementation("com.android.billingclient:billing-ktx:$billing_version")
}
```

---

## 有关用户自选结算方式试行计划的临时用户体验指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/user-choice?hl=zh-cn

**Contents:**
- 有关用户自选结算方式试行计划的临时用户体验指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 概览
- 选择国家/地区和语言
- 面向用户的信息
  - 何时显示
  - 何时显示价格
  - 如何显示
  - 用户操作
    - 继续
    - 了解详情

参与用户自选结算方式试行计划的开发者可在提供 Google Play 结算系统的同时，测试提供备选结算系统。该计划旨在帮助我们了解为用户提供这种选择的效果。这些用户体验指南旨在确保提供一致的用户体验，并帮助用户做出明智的决策。

如果您参与该试行计划，则需要显示一个信息界面和一个单独的结算方式选择界面。信息屏幕只需在每位用户首次发起购买交易时向其显示，而结算方式选择屏幕则必须在每次购买交易前都向用户显示。必须根据以下准则为这两个屏幕实现面向用户的消息和界面规范。

选择用户的国家/地区和语言，以便在以下设计规范中查看对应的界面文本字符串。

信息屏幕可以帮助用户了解相关更改的背景，并提供更多信息以帮助用户做出明智的选择。

添加备选结算系统后，必须在用户开始进行首次购买交易时向其显示信息屏幕。当同一用户以后再次进行购买交易时，就不需要再显示该信息了。在用户执行明确操作以发起购买交易之后，系统应立即显示信息屏幕。

必须在显示信息屏幕或结算方式选择屏幕之前，在显眼的位置向用户显示购买价格。

信息屏幕必须显示在模态底部动作条中。模态底部动作条与模态对话框类似，它会从屏幕底部向上呈现动画效果，并固定在屏幕底部。它位于底层屏幕中的所有界面元素的上层。底层屏幕会被深色纱罩遮挡，表示它不会响应用户的任何互动。

如需详细了解模态底部动作条的设计和实现，请参阅 Google Material Design。

当用户点按应用中用于发起购买交易的按钮或其他界面元素时，底部动作条应触发。用户可以在信息屏幕中执行三种可能的操作：

点按“继续”按钮会关闭信息屏幕，并启动结算方式选择屏幕。

点按“了解详情”按钮可在网络浏览器中打开相应的 Google 帮助中心文章。

如果用户要关闭底部动作条并返回底层屏幕，可以通过以下方式关闭底部动作条：

在用户关闭信息屏幕或点按“继续”后，无需再次显示信息屏幕。

示例：当用户在应用中点按进行购买时，该按钮会触发信息屏幕。

信息屏幕分为 3 个组件：标题、消息和按钮。所有这 3 个组件都是必需的，其包含的文字和界面元素必须与本指南中的定义完全一致。请勿在该屏幕中添加任何其他文字或图像，但您可以在其他屏幕中添加额外的文字和图像。

在横向视图中，底部动作条的宽度大于纵向视图中的宽度，但在其他方面都遵循相同的设计规范和功能。

结算方式选择界面向用户展示两种结账选项，用于完成购买交易。为了帮助用户做出明智的决策，每个结算服务选项还会向用户显示可用的付款方式。在用户做出选择后，他们将继续通过所选的结算系统完成购买交易。

如果用户已在之前的购买交易中查看过信息屏幕，则在其执行明确操作以发起购买交易后，系统应立即显示结算方式选择屏幕。

结算方式选择屏幕必须显示在模态底部动作条中，并遵循与信息屏幕相同的规范。

应以公平、均等的方式呈现备选结算系统和 Google Play 结算系统的按钮。这包括但不限于相同的按钮大小、文字大小/样式、点按目标和图标大小。请勿添加本指南中未定义的任何其他文字、图片或样式更改。

示例：当用户在应用中点按进行购买时，只有当用户已在之前的购买交易中查看过信息屏幕时，该按钮才会触发结算方式选择屏幕。

结算方式选择屏幕包含 4 个不同的组件：标题、说明、开发者按钮和 Google Play 按钮。您必须使用所有组件，并且这些组件包含的文字和界面元素必须与本指南中的定义完全一致。请勿在该屏幕中添加任何其他文字或图像，但您可以在您拥有的其他屏幕中添加其他文字和图像。

您可以通过以下链接获取 Google Play 的可视化资源和付款图标。

示例：在纵向视图中，底部动作条的跨度应该与屏幕总宽度相等。

示例：在横向视图中，底部动作条的宽度大于纵向视图中的宽度，但在其他方面都遵循相同的设计规范和功能。

如需进一步了解用户自选结算方式试行计划和常见问题解答，请访问我们的帮助中心。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

---

## 促销代码 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/promo?hl=zh-cn

**Contents:**
- 促销代码 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 创建和管理促销活动
- 用户兑换流程
- 实现促销代码
- 深层链接
- 测试促销代码

利用促销活动或促销代码，您可以向数量有限的用户免费提供一次性商品或试订服务。用户在您的应用或 Google Play 商店应用中输入促销代码，即可免费获得相应的商品或试订服务。

在 Play 管理中心内，您可以创建以下类型的促销代码：

您可以充分发挥创意，使用促销代码以多种方式来吸引用户，这些方式包括：

在您于 Play 管理中心指定的促销活动结束日期之前，用户可以随时在 Google Play 商店中兑换促销代码。促销活动最长可以持续一年。

如需了解如何设置和管理促销活动，请参阅创建促销活动。

用户获得促销代码后，可通过以下某种方式进行兑换：

例如，图 1 显示了订阅的购买屏幕。如需输入促销代码，请点按当前付款方式旁边的箭头以显示付款方式屏幕，如图 2 所示。接下来，点按兑换代码以转到兑换礼品卡或促销代码屏幕，如图 3 所示。您随后可以在此屏幕上输入促销代码，点按“兑换”即可完成。

为了确保应用已经准备好处理促销代码，应用需要正确处理发生在应用之外的兑换。如需了解详情，请参阅将 Google Play 结算库集成到您的应用中里的处理购买交易、提取购买交易和处理在您的应用外进行的购买交易部分。

您也可以生成一个网址，使用户转到 Google Play 商店并自动填写输入代码字段，由此分享促销代码。促销代码网址采用以下格式：

图 4 显示了 Google Play 应用的兑换代码对话框：

用户按兑换后，如果安装了应用的最新版本，Google Play 商店会提示用户打开该应用。否则，Google Play 商店会提示用户更新或下载您的应用。

如需测试您的促销代码实现，请参阅测试促销代码。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

**Examples:**

Example 1 (unknown):
```unknown
https://play.google.com/redeem?code=promo_code
```

Example 2 (unknown):
```unknown
https://play.google.com/redeem?code=promo_code
```

---

## 开发者载荷 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/developer-payload

**Contents:**
- 开发者载荷 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 购物验证
- 购买交易归因
- 将元数据与购买交易相关联

开发者载荷向来被用于各种不同用途，包括防欺诈以及将购买交易归因于正确的用户。在 Google Play 结算库 2.2 及更高版本中，以前依赖于开发者载荷的预期用例现在也在该库的其他部分获得完全支持。

因为有了这样的支持，从 Google Play 结算库 2.2 版开始，我们已弃用开发者载荷。与开发者载荷关联的方法在 2.2 版中已废弃，且在 3.0 版中已移除。请注意，对于使用先前版本的库或 AIDL 完成的购买交易，应用可继续检索开发者载荷。

如需查看详细的变更清单，请参阅 Google Play 结算库 2.2 版本说明和 Google Play 结算库 3.0 版本说明。

为确保购买交易的真实性并防止伪造或重播，Google 建议您将购买令牌（通过 Purchase 对象中的 getPurchaseToken() 方法获取）与 Google Play Developer API 配合使用，验证购买交易的真实性。如需了解详情，请参阅打击欺诈和滥用行为。

许多应用（特别是游戏）需要确保将购买交易正确归因于发起购买交易的游戏内角色/头像或应用内用户个人资料。从 Google Play 结算库 2.2 开始，应用在启动购买对话框时可将经过混淆处理的账号和个人资料标识符传递给 Google，而在应用检索购买交易时也会返回相应信息。

在 BillingFlowParams 中使用 setObfuscatedAccountId() 和 setObfuscatedProfileId() 参数，并使用 Purchase 对象中的 getAccountIdentifiers() 方法检索这些参数。

Google 建议您将有关购买交易的元数据存储在您维护的安全后端服务器上。此购买交易元数据应与通过 Purchase 对象中的 getPurchaseToken 方法获取的购买令牌相关联。在成功完成购买交易后调用 PurchasesUpdatedListener 时将购买令牌和元数据传递到您的后端，就可以保留这些数据。

为确保在购买流程中断的情况下关联元数据，Google 建议在启动购买对话框之前将元数据存储在后端服务器上，并将其与用户的账号 ID、正在购买的 SKU 和当前时间戳相关联。

如果购买流程在调用 PurchasesUpdatedListener 之前中断，当应用恢复并调用 BillingClient.queryPurchasesAsync() 后，应用会立即发现购买交易。然后，您可以将从 Purchase 对象的 getPurchaseTime()、getSku() 和 getPurchaseToken() 方法检索到的值发送到后端服务器，以查询元数据，将元数据与购买令牌关联，并继续处理购买交易。请注意，您最初存储的时间戳与 Purchase 对象的 getPurchaseTime() 中的值不会完全匹配，因此您需要大致地对比二者。例如，您可以检查值之间是否相隔在特定时间段内。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

---

## 外部优惠 API 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/external?hl=zh-cn

**Contents:**
- 外部优惠 API 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 术语词汇表
- 支持外部优惠
  - 在 Play 管理中心内配置
  - 面向用户的信息界面
  - 后续步骤

在某些国家/地区，符合条件的开发者可以将用户引导到应用以外，包括宣传应用内数字功能和服务的相关优惠。本指南将介绍用于启用外部优惠的 API。您应该先查看计划要求并加入外部优惠计划，然后再使用这些 API。

本部分介绍如何支持外部商品。 使用这些 API 之前，请确保以下几点：

如需在 Play 管理中心内配置外部优惠，请按照计划要求中列出的步骤操作。

信息界面有助于用户了解他们将要访问一个外部网站。系统每次都会向用户显示信息界面，然后才会使用外部优惠 API 将用户定向到应用之外。

如需开始集成外部优惠 API，请遵循应用内集成和后端集成的深度指南。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

---

## 有关 Google Play 结算服务之外的变现的后端集成指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/outside-gpb-backend?hl=zh-cn

**Contents:**
- 有关 Google Play 结算服务之外的变现的后端集成指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 向 Google Play 报告新的外部交易
  - 外部交易报告
  - 报告新购买交易
  - 报告购买交易的后续交易
  - 报告升级或降级
  - 停止手动报告备选结算系统交易
  - 举报 Play 合作伙伴计划
- 向 Google Play 报告购买交易退款
- API 配额

Google Play Developer API 现在包含 报告来自备选结算系统的交易，或 外部优惠系统。本指南将介绍如何报告替代性数据， 结算或外部优惠交易。

从后端处理应用内购买交易时，可能需要用到一些组件。如需构建这些组件，您需要按照配置 Google Play Developer API 中的说明设置后端集成。对于 所有不特定于备选结算系统的开发者后端功能 或外部优惠 API 的说明， Google Play 结算系统文档适用。

与 Externaltransactions APIs 集成 报告 Google Play 结算系统以外发生的交易， 支持的国家/地区，包括通过免费试用产生的 0 美元交易 购买。通过备选结算系统或外部优惠系统进行的交易 仅在系统允许的情况下，才应针对符合条件的用户所在国家/地区启动和报告 在备选结算系统下，或者 外部优惠计划，否则，API 调用将 已被拒绝。这适用于所有交易，包括新购买、续订 充值、升级、降级等操作。

您应该调用 Externaltransactions API 来报告外部交易 在通过备选结算系统获得授权后，或者 外部优惠系统这适用于所有交易，包括 扣款、续订、退款等。所有交易都必须 会在交易发生 24 小时内报告。

系统会为每一笔外部交易报告一个外部交易 ID。对于周期性购买交易（例如自动续订型订阅），您需要发送与这笔周期性购买交易中的第一笔交易相关联的外部交易 ID，以用作后续所有交易（包括退款）的参数。这样就能记录相应购买交易的一系列交易。如果商品发生变化（例如升级或降级），或者周期性交易被取消或过期且之后同一商品再次被购买，您就需要针对相应交易发送新的外部交易 ID。您不得添加任何个人身份信息 这些信息、专有信息或机密信息， 交易 ID。

每当通过备选结算系统完成新购买交易时 或外部优惠系统，对 Externaltransactions API 的调用会 必填字段。对于这些新的购买交易，您需要提供唯一 externalTransactionId 以查询的形式与后端中的购买交易相关联 参数。此externalTransactionId不能在同一应用的 软件包 ID。

应用通过externalTransactionToken UserChoiceBillingListener、AlternativeBillingOnlyReportingDetailsListener、 或 ExternalOfferReportingDetailsListener 回调作为 一次性购买和首次交易的请求正文 周期性购买（例如订阅）。无论是哪种情况，都称为 初始交易。完成初始交易后， externalTransactionToken 不再需要，您后续报告 通过提供新的唯一身份 externalTransactionId。请参阅报告购买交易的后续交易 ，详细了解如何报告后续交易。

如果与印度境内的用户进行交易，由于该国税费因用户所在的行政区（例如州或省）而异，请务必在 userTaxAddress 下包含该行政区。如需了解适用的行政区，请参阅 API 参考指南中的预定义字符串列表。

在某些情况下，同一外部购买交易有多笔相关联的用户付款（例如，续订或预付费方案充值）。您可以在 Externaltransactions 中使用同一 API 报告这些后续交易。如报告新购买交易中所述，后续交易不需要 externalTransactionToken。不过，系统会为每笔续订或充值交易发送新的唯一 externalTransactionId 作为查询参数，并将初始交易的 ID 包含在 initialExternalTransactionId 字段中。

若要当用户拥有一项订阅的情况下在备选结算系统中报告升级或降级，您可在 Externaltransactions API 中使用相同的端点和函数，发送为升级或降级交易而提供给应用的 externalTransactionToken。这与报告新购买交易类似。

如需迁移您以非自动化报告方式提供备选结算系统期间开始的有效订阅，请使用 migratedTransactionProgram 字段（而不是指定 initialExternalTransactionId 或 externalTransactionToken）创建一笔新的 0 费用交易。将每项有效订阅的 transactionTime 设置为用户最初注册该订阅的时间。之后，照常通过 API 报告这些订阅的每一笔后续交易，并提供之前使用的 initialExternalTransactionId 创建续订交易。迁移订阅后，您无需再手动报告订阅的后续交易，但前提是这些交易是通过本页介绍的自动化方式报告的。

迁移订阅时，请留意当前的配额限制，以确保迁移不会用尽配额。如果有很多订阅需要 分几天进行迁移，或申请提高配额 配额 ，了解所有最新动态。

只有在从手动报告迁移时，才可以使用 migratedTransactionProgram 字段。当手动报告不再受支持后，该字段将被废弃。

参与合作伙伴计划（例如 Play 媒体体验计划必须提供 transaction_program_code（报告外部交易时）。如果您 如果您是符合条件的开发者，请与您的业务发展经理联系以了解详情 了解如何设置此字段。

与 Externaltransactions API 集成后，您可报告在 Google Play 结算系统以外向用户退款的交易。为了让 Play 正确识别哪一笔交易已退款，您应将之前所报告交易的相应 externalTransactionId 添加为网址参数的一部分。

报告订阅购买交易的退款时，请引用被退款订阅的具体周期性交易的 externalTransactionId。

如需报告该订阅所有交易的退款，您需要发出三个单独的退款请求：一个针对初始交易，两个针对后续交易。

此方法接受全额退款 （其中金额与用户在原始外部 交易）和部分退款 （金额小于用户在原始外部 交易）。对于部分退款，您需要指定退还的税前金额。

Externaltransactions API 受每日 API 配额限制 就像 Google Play Developer API 中的任何其他端点一样。

此外，在调用 Externaltransactions.createexternaltransaction 或 Externaltransactions.refundexternaltransaction 时，Externaltransactions API 的每分钟查询数量 (QPM) 上限为 1,200 个。对 Externaltransactions.getexternaltransaction 的调用不会计入此 1,200 QPM 的限额。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-07-27。

**Examples:**

Example 1 (unknown):
```unknown
POST /androidpublisher/v3/applications/com.myapp.android/externalTransactions?externalTransactionId=123-456-789

Body
 {
"originalPreTaxAmount" : {
   "priceMicros": "0",
   "currency": "KRW"
 },
 "originalTaxAmount" : {
   "priceMicros": "0",
   "currency": "KRW"
 },
"transactionTime" : "2022-02-22T12:45:00Z",
 "recurringTransaction" : {
   "externalTransactionToken": "my_token",
   "externalSubscription" {
     "subscriptionType": "RECURRING"
   }
 },
 "userTaxAddress" : {
   "regionCode": "KR"
 }
}
```

Example 2 (unknown):
```unknown
POST /androidpublisher/v3/applications/com.myapp.android/externalTransactions?externalTransactionId=123-456-789

Body
 {
"originalPreTaxAmount" : {
   "priceMicros": "0",
   "currency": "KRW"
 },
 "originalTaxAmount" : {
   "priceMicros": "0",
   "currency": "KRW"
 },
"transactionTime" : "2022-02-22T12:45:00Z",
 "recurringTransaction" : {
   "externalTransactionToken": "my_token",
   "externalSubscription" {
     "subscriptionType": "RECURRING"
   }
 },
 "userTaxAddress" : {
   "regionCode": "KR"
 }
}
```

Example 3 (unknown):
```unknown
POST /androidpublisher/v3/applications/com.myapp.android/externalTransactions?externalTransactionId=123-456-789

Body
 {
"originalPreTaxAmount" : {
   "priceMicros": "0",
   "currency": "INR"
 },
 "originalTaxAmount" : {
   "priceMicros": "0",
   "currency": "INR"
 },
"transactionTime" : "2023-11-01T12:45:00Z",
 "recurringTransaction" : {
   "externalTransactionToken": "my_token",
   "externalSubscription" {
     "subscriptionType": "RECURRING"
   }
 },
 "userTaxAddress" : {
   # Tax varies in India based on state, so include that information in
   # administrativeArea
   "regionCode": "IN"
   "administrativeArea": "KERALA"
 }
}
```

Example 4 (unknown):
```unknown
POST /androidpublisher/v3/applications/com.myapp.android/externalTransactions?externalTransactionId=123-456-789

Body
 {
"originalPreTaxAmount" : {
   "priceMicros": "0",
   "currency": "INR"
 },
 "originalTaxAmount" : {
   "priceMicros": "0",
   "currency": "INR"
 },
"transactionTime" : "2023-11-01T12:45:00Z",
 "recurringTransaction" : {
   "externalTransactionToken": "my_token",
   "externalSubscription" {
     "subscriptionType": "RECURRING"
   }
 },
 "userTaxAddress" : {
   # Tax varies in India based on state, so include that information in
   # administrativeArea
   "regionCode": "IN"
   "administrativeArea": "KERALA"
 }
}
```

---
