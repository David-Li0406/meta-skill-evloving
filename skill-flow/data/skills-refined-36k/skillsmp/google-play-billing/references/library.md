# Google-Play-Billing - Library

**Pages:** 5

---

## 从 Google Play 结算库版本 5 或 6 迁移到版本 7 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/migrate-gpblv7?hl=zh-cn

**Contents:**
- 从 Google Play 结算库版本 5 或 6 迁移到版本 7 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 概览
- 向后兼容的 Play 结算库升级
- 从 PBL 5 升级到 PBL 7
  - 更新 Google Play 结算库
  - 更改用户的订阅购买交易
  - 处理订阅价格变动
  - 处理与订阅相关的 API 变更
  - 处理 Play 结算库错误
  - 处理待处理的交易

本文档介绍了如何从 Google Play 结算库版本 5 或 6 迁移到 Google Play 结算库版本 7，以及如何集成新的可选订阅功能。

如需查看版本 7.0.0 的完整变更列表，请参阅版本说明。

Google Play 结算库版本 7 改进了现有订阅功能的付款处理。这些可选改进增添了对分期付款的支持，以及对预付费订阅的待处理购买交易的支持。

所有新的 Google Play 结算库 7 API 都是可选的，开发者无需实现任何 API 更改即可进行更新。

如需进行迁移，您需要更新 API 引用并从应用中移除某些 API，如版本说明和本迁移指南后面部分所述。

以下部分介绍了如何从 PBL 5 升级到 PBL 7。

更新应用的 build.gradle 文件中的 Play 结算库依赖项版本。

接下来，按照以下部分中的说明更新您的 API 参考。

Play 结算库 5 及更低版本使用 ProrationMode 将更改应用于用户的订阅购买交易，例如升级或降级。此 API 已被移除，取而代之的是 ReplacementMode。

移除了之前已废弃的 launchPriceConfirmationFlow API。如需了解替代方案，请参阅价格变动指南。

移除了之前已废弃的 API setOldSkuPurchaseToken、setReplaceProrationMode 和 setReplaceSkusProrationMode。

新增了 NETWORK_ERROR 代码，用于指明用户设备和 Google Play 系统之间的网络连接问题。

SERVICE_TIMEOUT 和 SERVICE_UNAVAILABLE 代码也已更新。

如需了解详情，请参阅处理 BillingResult 响应代码。

Play 结算库不再为待处理的购买交易创建订单 ID。只有在购买交易变为 PURCHASED 状态后，系统才会为这类购买交易填充订单 ID。确保您的集成仅预期在交易全部完成后获得订单 ID。您仍可将购买令牌用作记录。

如需详细了解如何处理待处理的购买交易，请参阅 Play 结算库集成指南和购买生命周期管理指南。

移除了 BillingClient.Builder.enableAlternativeBilling、AlternativeBillingListener 和 AlternativeChoiceDetails。开发者应改为在监听器回调中将 BillingClient.Builder.enableUserChoiceBilling() 与 UserChoiceBillingListener 和 UserChoiceDetails 搭配使用。

此次更新是对已废弃 API 的重命名，没有任何行为变更。

以下部分介绍了如何从 PBL 6 升级到 PBL 7。

更新应用的 build.gradle 文件中的 Play 结算库依赖项版本。

接下来，按照以下部分中的说明更新您的 API 参考。

移除了之前已废弃的 API setOldSkuPurchaseToken、setReplaceProrationMode 和 setReplaceSkusProrationMode。

移除了 BillingClient.Builder.enableAlternativeBilling、AlternativeBillingListener 和 AlternativeChoiceDetails。开发者应改为在监听器回调中将 BillingClient.Builder.enableUserChoiceBilling() 与 UserChoiceBillingListener 和 UserChoiceDetails 搭配使用。

如需了解如何将这些更改集成到您的应用中，请参阅分期付款订阅集成指南。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

**Examples:**

Example 1 (python):
```python
dependencies {
    def billingVersion = 7.0.0

    implementation "com.android.billingclient:billing:$billingVersion"
}
```

Example 2 (python):
```python
dependencies {
    def billingVersion = 7.0.0

    implementation "com.android.billingclient:billing:$billingVersion"
}
```

Example 3 (python):
```python
dependencies {
    def billingVersion = 7.0.0

    implementation "com.android.billingclient:billing:$billingVersion"
}
```

Example 4 (python):
```python
dependencies {
    def billingVersion = 7.0.0

    implementation "com.android.billingclient:billing:$billingVersion"
}
```

---

## 从 Google Play 结算库版本 6 或 7 迁移到版本 8 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/migrate-gpblv8

**Contents:**
- 从 Google Play 结算库版本 6 或 7 迁移到版本 8 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 概览
- PBL 升级的向后兼容性
- 从 PBL 6 或 7 升级到 PBL 8
  - 从以下版本升级
  - 从以下版本升级

本文档介绍了如何从 Google Play 结算库 (PBL) 6 或 7 迁移到 PBL 8，以及如何与新的可选订阅功能集成。

如需查看版本 8.0.0 的完整变更列表，请参阅版本说明。

PBL 8 改进了现有 API，并移除了之前已弃用的 API。此版本的库还包含一次性商品的新 API。

如需迁移到 PBL 8，您需要更新或移除应用中的一些现有 API 引用，如版本说明和本迁移指南的后续部分中所述。

如需从 PBL 6 或 7 升级到 PBL 8，请执行以下步骤：

更新应用 build.gradle 文件中的 Play 结算库依赖项版本。

（仅适用于从 PBL 6 升级到 PBL 8）。在应用中处理与订阅相关的 API 变更。

下表列出了在 PBL 8 中移除的与订阅相关的 API，以及您必须在应用中使用的相应替代 API。

更新 queryProductDetailsAsync 方法的实现。

ProductDetailsResponseListener.onProductDetailsResponse 方法的签名发生了变化，这需要您在应用中更改 queryProductDetailsAsync 实现。如需了解详情，请参阅显示可供购买的产品。

PBL 8 不再支持下表中列出的 API。 如果您的实现使用了任何这些已移除的 API，请参阅下表了解其对应的替代 API。 在 PBL 8 中移除了之前已弃用的 API 要使用的替代 API queryPurchaseHistoryAsync API 请参阅查询购买历史记录 querySkuDetailsAsync queryProductDetailsAsync enablePendingPurchases()（不带参数的 API） enablePendingPurchases(PendingPurchaseParams params) 请注意，已废弃的 enablePendingPurchases() 在功能上等同于 enablePendingPurchases(PendingPurchasesParams.newBuilder().enableOneTimeProducts().build())。 queryPurchasesAsync(String skuType, PurchasesResponseListener listener) queryPurchasesAsync BillingClient.Builder.enableAlternativeBilling BillingClient.Builder.enableUserChoiceBilling AlternativeBillingListener UserChoiceBillingListener AlternativeChoiceDetails UserChoiceDetails

下表列出了 PBL 8 中移除的 API，以及您必须在应用中使用的相应替代 API。 在 PBL 8 中移除了之前已弃用的 API 要使用的替代 API queryPurchaseHistoryAsync API 请参阅查询购买历史记录 querySkuDetailsAsync queryProductDetailsAsync enablePendingPurchases()（不带参数的 API） enablePendingPurchases(PendingPurchaseParams params) 请注意，已废弃的 enablePendingPurchases() 在功能上等同于 enablePendingPurchases(PendingPurchasesParams.newBuilder().enableOneTimeProducts().build())。 queryPurchasesAsync(String skuType, PurchasesResponseListener listener) queryPurchasesAsync

如果在服务断开连接时进行 API 调用，Play 结算库可以尝试自动重新建立服务连接。如需了解详情，请参阅启用自动重新连接服务。

支持预付费方案的待处理购买交易。如需了解详情，请参阅处理订阅和待处理的交易。

虚拟分期付款订阅。如需了解详情，请参阅分期付款订阅集成。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

**Examples:**

Example 1 (python):
```python
dependencies {
  def billingVersion = 8.0.0
  implementation "com.android.billingclient:billing:$billingVersion"
}
```

Example 2 (python):
```python
dependencies {
  def billingVersion = 8.0.0
  implementation "com.android.billingclient:billing:$billingVersion"
}
```

---

## 从 Google Play 结算库版本 4 或 5 迁移到版本 6 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/migrate-gpblv6?hl=zh-cn

**Contents:**
- 从 Google Play 结算库版本 4 或 5 迁移到版本 6 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 概览
- 向后兼容的 Play 结算库升级
  - 旧版应用仍可正常运行
  - 升级到 Play 结算库 5 或 6
- 完整的迁移步骤
  - 在后端商品清单中创建新订阅
  - 使用新 API 管理后端订阅清单
  - 更新 Google Play 结算库
  - 初始化结算客户端并与 Google Play 建立连接

本主题将介绍如何从 Google Play 结算库版本 4 或 5 迁移到 Google Play 结算库版本 6，以及如何使用新的订阅功能。

如需查看版本 6.0.0 的完整变更列表，请参阅版本说明。

Google Play 结算库版本 6 以版本 5 为基础，引入了新订阅功能，并做出了多项改进。借助这些功能，您能以更多方式销售订阅内容，还能降低运营费用，因为无需创建和管理越来越多的 SKU。

如需详细了解 Play 结算库 5 中引入的新功能，请参阅 Play 管理中心内订阅方面的近期变更。

作为 2022 年 5 月发布的 Play 结算库版本 5 和新订阅平台的一部分，所有现有的订阅产品都会自动转换为这种新范例。这意味着，您无需更改订阅产品配置，即可获得与新版 Play 结算库兼容的目录。如需详细了解如何将订阅 SKU 转换为向后兼容的订阅，请参阅 Play 管理中心帮助文章中的“使用旧版订阅”部分。

如果您有向后兼容的订阅目录，那么您所有现有版本的应用仍应按预期适用于这些产品。一次性商品购买交易应该仍然可以继续在旧版中正常进行。

使用已废弃方法（例如 querySkuDetailsAsync()）的应用版本将无法销售任何不向后兼容的基础方案或优惠。如需了解向后兼容的优惠，请参阅相关的 Play 管理中心帮助中心文章。

Play 结算库 5 和 6 包含已废弃的 querySkuDetailsAsync 和 BillingFlowParams.Builder.setSkuDetails 方法，其中这些方法的结算流程参数为 SkuDetails。这意味着，您可以通过规划不同的迁移阶段，逐步迁移至 Play 结算库 6。

如要迁移，首先更新库版本，保持目录和后端不变，然后在其仍使用已废弃方法时测试应用。如果未使用 queryPurchases、launchPriceChangeFlow 或 setVrPurchaseFlow，则它应仍可按预期运行。之后，您可以通过迭代来全面采用 2022 年 5 月发布的新订阅功能。

如果您之前已通过 Google Play 结算库版本 5 迁移采用了这些功能，则可以直接跳至标记为更新 Google Play 结算库和更改用户的订阅购买交易的部分。如果您是从早期版本开始迁移，或尚未全面采用新功能，请参阅完整的迁移步骤，了解如何采用这些功能。

现在，使用 Play 管理中心或 Play Developer API，您可以配置包含多个基础方案的单个订阅，每个基础方案可提供多项优惠。您可以为订阅优惠设置灵活的定价模式和资格条件。您可以使用各种各样的自动续订服务和预付费方案，在整个订阅生命周期中创建优惠。

我们建议在迁移应用之前，按照新订阅平台中的实体结构为 Play 结算库版本 6 集成创建新产品。您可以在单个订阅下合并旧清单中提供相同使用权福利的重复产品，并使用基础方案和优惠配置来表示您希望提供的所有选项。如需详细了解此建议，请参阅 Play 管理中心帮助文章的“使用旧版订阅”部分。

建议您不要修改在 2022 年 5 月版本之后转换的订阅产品，应该保持不变，即使用已废弃的方法（例如，querySkuDetailsAsync()）随应用版本一起销售，避免引入可能影响这些旧 build 的变更。

转换流程会使 2022 年 5 月之前的清单中的订阅产品变为只读状态，以避免可能导致现有集成出现问题的意外更改。可以更改这些订阅，但可能对您的前端和后端集成产生影响：

在前端，使用 querySkuDetailsAsync() 获取订阅产品详情的应用版本只能销售向后兼容的基础方案和优惠，并且只能有一个向后兼容的基础方案和优惠组合，因此如果您向转换后的订阅添加新的方案或优惠，新的额外基础方案或优惠将无法在这些旧版应用中销售。

在后端，如果您在 Play 管理中心界面中修改转换后的订阅，则无法使用 inappproducts 端点管理这些订阅（如果您为此目的调用了该端点）。您还应迁移到新的订阅购买状态端点 (purchases.subscriptionsv2.get) 来管理这些订阅的购买交易，因为旧购买状态端点 (purchases.subscriptions.get) 仅返回处理向后兼容的基础方案和优惠购买交易所需的数据。如需了解详情，请参阅管理订阅购买状态部分。

如果您使用 Google Play Developer API 自动管理订阅产品清单，则需要使用新的订阅产品定义端点来创建和管理订阅、基础方案和优惠。请参阅 2022 年 5 月的订阅功能指南，详细了解此版本的产品清单 API 变更。

如需迁移 Google Play 结算服务订阅的自动产品清单管理模块，请将 inappproducts API 替换为新的 Subscription Publishing API 来管理和发布订阅清单。有三个新端点：

这些新端点具有利用清单中的所有新功能所需的所有功能：基础方案和优惠标签、区域定位、预付费方案等。

您应该依然使用 inappproducts API 来管理一次性购买产品的应用内产品清单。

使用已废弃方法（例如 querySkuDetailsAsync()）的应用版本将无法销售任何不向后兼容的基础方案或优惠。您可以在此处了解向后兼容的优惠。

创建新的订阅产品清单后，您可以将应用迁移到 Google Play 结算库版本 5。使用应用 build.gradle 文件更新后的版本替换现有的 Play 结算库依赖项。

即使您没有修改任何方法调用，您的项目应该也会立即构建，因为我们已在 Play 结算库版本 6 中实现了向后兼容性。SKU 的概念被视为已废弃，但仍会存在，目的是使应用移植流程更简单且更循序渐进。

从 Android 应用启动购买交易的前几步保持不变：

为了获取用户符合购买条件的所有优惠，请按以下步骤操作：

请注意，查询结果现在是 ProductDetails，而不是 SkuDetails。每个 ProductDetails 项目都包含商品的相关信息（ID、商品名、类型等）。对于订阅商品，ProductDetails 包含一个 List<ProductDetails.SubscriptionOfferDetails>，即订阅优惠详情列表。对于一次性购买商品，ProductDetails 包含一个 ProductDetails.OneTimePurchaseOfferDetails。它们可用于确定要向用户显示哪些优惠。

queryProductDetailsAsync 的回调会返回一个 List<ProductDetails>。每个 ProductDetails 项目都包含商品的相关信息（ID、商品名、类型等）。主要区别在于，订阅商品现在还包含一个 List<ProductDetails.SubscriptionOfferDetails>，其中包含用户可以享受的所有优惠。

由于以前的 Play 结算库版本不支持新对象（订阅、基础方案、优惠等），因此新系统将每个订阅 SKU 转换为单个向后兼容的基础方案和优惠。可用的一次性购买商品也改为使用 ProductDetails 对象。您可以使用 getOneTimePurchaseOfferDetails() 方法访问一次性购买商品的优惠详情。

在极少数情况下，某些设备无法支持 ProductDetails 和 queryProductDetailsAsync()，这通常是因为 Google Play 服务版本已过时。为了确保对此场景提供适当的支持，请先针对 PRODUCT_DETAILS 功能调用 isFeatureSupported()，然后再调用 queryProductDetailsAsync。如果响应为 OK，表示设备支持该功能，您可以继续调用 queryProductDetailsAsync()。如果响应为 FEATURE_NOT_SUPPORTED，您可以改用 querySkuDetailsAsync() 请求可用的向后兼容产品列表。如需详细了解如何使用向后兼容功能，请参阅 2022 年 5 月的订阅功能指南。

启动优惠的购买流程与启动 SKU 的流程非常相似。如需使用版本 6 发起购买请求，请执行以下操作：

为了销售提供用户所选优惠的商品，请获取所选优惠的 offerToken，并将其传入 ProductDetailsParams 对象。

创建 BillingFlowParams 对象后，使用 BillingClient 启动结算流程的操作保持不变。

使用 Google Play 结算库版本 6 处理购买交易的操作与以前的版本类似。

如需拉取用户拥有的所有有效购买交易并查询新购买交易，请执行以下操作：

用于管理应用外购买和待处理交易的步骤没有变化。

您应该迁移后端中的订阅购买状态管理组件，以便处理在前面步骤中创建的新产品的购买交易。对于您在 2022 年 5 月发布之前定义的转换后订阅产品，您当前的订阅购买状态管理组件应该可以正常工作，它应该足以管理向后兼容优惠的购买交易，但不支持任何新功能。

您需要为订阅购买状态管理模块实现新的 Subscription Purchases API，该模块会在后端检查购买状态并管理 Play 结算服务订阅使用权。该 API 的旧版本不会返回在新平台中管理购买交易所需的所有详细信息。如需详细了解与先前版本相比的变化，请参阅 2022 年 5 月新订阅功能指南。

通常在每次收到 SubscriptionNotification 实时开发者通知时调用 Subscription Purchases API，即可拉取有关订阅状态的最新信息。您需要将对 purchases.subscriptions.get 的调用替换为新版本的 Subscription Purchases API purchases.subscriptionsv2.get。在新模型中，有一个名为 SubscriptionPurchaseV2 的新资源，可提供足够的信息来管理订阅的购买使用权。

此新端点会返回所有订阅产品和所有购买交易的状态，无论销售该产品的应用版本是什么，也不管该产品是何时定义的（2022 年 5 月版本之前或之后），因此在迁移后，您只需使用此版本的订阅购买状态管理模块。

在 Play 结算库 5 及更低版本中，ProrationMode 用于将更改应用于用户的订阅购买交易，例如升级或降级。在版本 6 中，它已被废弃，取而代之的是 ReplacementMode。

先前已废弃的 launchPriceConfirmationFlow API 已从 Play 结算库 6 中移除。如需了解替代方案，请参阅价格变动指南。

Play 结算库 6 中新增了 NETWORK_ERROR 代码，用于指明用户设备和 Google Play 系统之间的网络连接问题。代码 SERVICE_TIMEOUT 和 SERVICE_UNAVAILABLE 也发生了变化。如需了解详情，请参阅处理 BillingResult 响应代码。

从 6.0.0 版开始，Play 结算库不再为待处理的购买交易创建订单 ID。只有在购买交易变为 PURCHASED 状态后，系统才会为这类购买交易填充订单 ID。确保您的集成仅预期在交易全部完成后获得订单 ID。您仍可将购买令牌用作记录。如需详细了解如何处理待处理的购买交易，请参阅 Play 结算库集成指南和购买生命周期管理指南。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-21。

**Examples:**

Example 1 (python):
```python
dependencies {
    def billingVersion = "6.0.0"

    implementation "com.android.billingclient:billing:$billingVersion"
}
```

Example 2 (python):
```python
dependencies {
    def billingVersion = "6.0.0"

    implementation "com.android.billingclient:billing:$billingVersion"
}
```

Example 3 (unknown):
```unknown
val skuList = ArrayList<String>()

skuList.add("up_basic_sub")

val params = SkuDetailsParams.newBuilder()

params.setSkusList(skuList).setType(BillingClient.SkuType.SUBS).build()

billingClient.querySkuDetailsAsync(params) {
    billingResult,
    skuDetailsList ->
    // Process the result
}
```

Example 4 (unknown):
```unknown
List<String> skuList = new ArrayList<>();

skuList.add("up_basic_sub");

SkuDetailsParams.Builder params = SkuDetailsParams.newBuilder();

params.setSkusList(skuList).setType(SkuType.SUBS).build();

billingClient.querySkuDetailsAsync(params,
    new SkuDetailsResponseListener() {
        @Override
        public void onSkuDetailsResponse(BillingResult billingResult,
                List<SkuDetails> skuDetailsList) {
            // Process the result.
        }
    }
);
```

---

## 从 Google Play 结算库版本 6 或 7 迁移到版本 8 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/migrate-gpblv8?hl=zh-cn

**Contents:**
- 从 Google Play 结算库版本 6 或 7 迁移到版本 8 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 概览
- PBL 升级的向后兼容性
- 从 PBL 6 或 7 升级到 PBL 8
  - 从以下版本升级
  - 从以下版本升级

本文档介绍了如何从 Google Play 结算库 (PBL) 6 或 7 迁移到 PBL 8，以及如何与新的可选订阅功能集成。

如需查看版本 8.0.0 的完整变更列表，请参阅版本说明。

PBL 8 改进了现有 API，并移除了之前已弃用的 API。此版本的库还包含一次性商品的新 API。

如需迁移到 PBL 8，您需要更新或移除应用中的一些现有 API 引用，如版本说明和本迁移指南的后续部分中所述。

如需从 PBL 6 或 7 升级到 PBL 8，请执行以下步骤：

更新应用 build.gradle 文件中的 Play 结算库依赖项版本。

（仅适用于从 PBL 6 升级到 PBL 8）。在应用中处理与订阅相关的 API 变更。

下表列出了在 PBL 8 中移除的与订阅相关的 API，以及您必须在应用中使用的相应替代 API。

更新 queryProductDetailsAsync 方法的实现。

ProductDetailsResponseListener.onProductDetailsResponse 方法的签名发生了变化，这需要您在应用中更改 queryProductDetailsAsync 实现。如需了解详情，请参阅显示可供购买的产品。

PBL 8 不再支持下表中列出的 API。 如果您的实现使用了任何这些已移除的 API，请参阅下表了解其对应的替代 API。 在 PBL 8 中移除了之前已弃用的 API 要使用的替代 API queryPurchaseHistoryAsync API 请参阅查询购买历史记录 querySkuDetailsAsync queryProductDetailsAsync enablePendingPurchases()（不带参数的 API） enablePendingPurchases(PendingPurchaseParams params) 请注意，已废弃的 enablePendingPurchases() 在功能上等同于 enablePendingPurchases(PendingPurchasesParams.newBuilder().enableOneTimeProducts().build())。 queryPurchasesAsync(String skuType, PurchasesResponseListener listener) queryPurchasesAsync BillingClient.Builder.enableAlternativeBilling BillingClient.Builder.enableUserChoiceBilling AlternativeBillingListener UserChoiceBillingListener AlternativeChoiceDetails UserChoiceDetails

下表列出了 PBL 8 中移除的 API，以及您必须在应用中使用的相应替代 API。 在 PBL 8 中移除了之前已弃用的 API 要使用的替代 API queryPurchaseHistoryAsync API 请参阅查询购买历史记录 querySkuDetailsAsync queryProductDetailsAsync enablePendingPurchases()（不带参数的 API） enablePendingPurchases(PendingPurchaseParams params) 请注意，已废弃的 enablePendingPurchases() 在功能上等同于 enablePendingPurchases(PendingPurchasesParams.newBuilder().enableOneTimeProducts().build())。 queryPurchasesAsync(String skuType, PurchasesResponseListener listener) queryPurchasesAsync

如果在服务断开连接时进行 API 调用，Play 结算库可以尝试自动重新建立服务连接。如需了解详情，请参阅启用自动重新连接服务。

支持预付费方案的待处理购买交易。如需了解详情，请参阅处理订阅和待处理的交易。

虚拟分期付款订阅。如需了解详情，请参阅分期付款订阅集成。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

**Examples:**

Example 1 (python):
```python
dependencies {
  def billingVersion = 8.0.0
  implementation "com.android.billingclient:billing:$billingVersion"
}
```

Example 2 (python):
```python
dependencies {
  def billingVersion = 8.0.0
  implementation "com.android.billingclient:billing:$billingVersion"
}
```

---

## 从 Google Play 结算库版本 4 或 5 迁移到版本 6 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/migrate-gpblv5?hl=zh-cn

**Contents:**
- 从 Google Play 结算库版本 4 或 5 迁移到版本 6 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 概览
- 向后兼容的 Play 结算库升级
  - 旧版应用仍可正常运行
  - 升级到 Play 结算库 5 或 6
- 完整的迁移步骤
  - 在后端商品清单中创建新订阅
  - 使用新 API 管理后端订阅清单
  - 更新 Google Play 结算库
  - 初始化结算客户端并与 Google Play 建立连接

本主题将介绍如何从 Google Play 结算库版本 4 或 5 迁移到 Google Play 结算库版本 6，以及如何使用新的订阅功能。

如需查看版本 6.0.0 的完整变更列表，请参阅版本说明。

Google Play 结算库版本 6 以版本 5 为基础，引入了新订阅功能，并做出了多项改进。借助这些功能，您能以更多方式销售订阅内容，还能降低运营费用，因为无需创建和管理越来越多的 SKU。

如需详细了解 Play 结算库 5 中引入的新功能，请参阅 Play 管理中心内订阅方面的近期变更。

作为 2022 年 5 月发布的 Play 结算库版本 5 和新订阅平台的一部分，所有现有的订阅产品都会自动转换为这种新范例。这意味着，您无需更改订阅产品配置，即可获得与新版 Play 结算库兼容的目录。如需详细了解如何将订阅 SKU 转换为向后兼容的订阅，请参阅 Play 管理中心帮助文章中的“使用旧版订阅”部分。

如果您有向后兼容的订阅目录，那么您所有现有版本的应用仍应按预期适用于这些产品。一次性商品购买交易应该仍然可以继续在旧版中正常进行。

使用已废弃方法（例如 querySkuDetailsAsync()）的应用版本将无法销售任何不向后兼容的基础方案或优惠。如需了解向后兼容的优惠，请参阅相关的 Play 管理中心帮助中心文章。

Play 结算库 5 和 6 包含已废弃的 querySkuDetailsAsync 和 BillingFlowParams.Builder.setSkuDetails 方法，其中这些方法的结算流程参数为 SkuDetails。这意味着，您可以通过规划不同的迁移阶段，逐步迁移至 Play 结算库 6。

如要迁移，首先更新库版本，保持目录和后端不变，然后在其仍使用已废弃方法时测试应用。如果未使用 queryPurchases、launchPriceChangeFlow 或 setVrPurchaseFlow，则它应仍可按预期运行。之后，您可以通过迭代来全面采用 2022 年 5 月发布的新订阅功能。

如果您之前已通过 Google Play 结算库版本 5 迁移采用了这些功能，则可以直接跳至标记为更新 Google Play 结算库和更改用户的订阅购买交易的部分。如果您是从早期版本开始迁移，或尚未全面采用新功能，请参阅完整的迁移步骤，了解如何采用这些功能。

现在，使用 Play 管理中心或 Play Developer API，您可以配置包含多个基础方案的单个订阅，每个基础方案可提供多项优惠。您可以为订阅优惠设置灵活的定价模式和资格条件。您可以使用各种各样的自动续订服务和预付费方案，在整个订阅生命周期中创建优惠。

我们建议在迁移应用之前，按照新订阅平台中的实体结构为 Play 结算库版本 6 集成创建新产品。您可以在单个订阅下合并旧清单中提供相同使用权福利的重复产品，并使用基础方案和优惠配置来表示您希望提供的所有选项。如需详细了解此建议，请参阅 Play 管理中心帮助文章的“使用旧版订阅”部分。

建议您不要修改在 2022 年 5 月版本之后转换的订阅产品，应该保持不变，即使用已废弃的方法（例如，querySkuDetailsAsync()）随应用版本一起销售，避免引入可能影响这些旧 build 的变更。

转换流程会使 2022 年 5 月之前的清单中的订阅产品变为只读状态，以避免可能导致现有集成出现问题的意外更改。可以更改这些订阅，但可能对您的前端和后端集成产生影响：

在前端，使用 querySkuDetailsAsync() 获取订阅产品详情的应用版本只能销售向后兼容的基础方案和优惠，并且只能有一个向后兼容的基础方案和优惠组合，因此如果您向转换后的订阅添加新的方案或优惠，新的额外基础方案或优惠将无法在这些旧版应用中销售。

在后端，如果您在 Play 管理中心界面中修改转换后的订阅，则无法使用 inappproducts 端点管理这些订阅（如果您为此目的调用了该端点）。您还应迁移到新的订阅购买状态端点 (purchases.subscriptionsv2.get) 来管理这些订阅的购买交易，因为旧购买状态端点 (purchases.subscriptions.get) 仅返回处理向后兼容的基础方案和优惠购买交易所需的数据。如需了解详情，请参阅管理订阅购买状态部分。

如果您使用 Google Play Developer API 自动管理订阅产品清单，则需要使用新的订阅产品定义端点来创建和管理订阅、基础方案和优惠。请参阅 2022 年 5 月的订阅功能指南，详细了解此版本的产品清单 API 变更。

如需迁移 Google Play 结算服务订阅的自动产品清单管理模块，请将 inappproducts API 替换为新的 Subscription Publishing API 来管理和发布订阅清单。有三个新端点：

这些新端点具有利用清单中的所有新功能所需的所有功能：基础方案和优惠标签、区域定位、预付费方案等。

您应该依然使用 inappproducts API 来管理一次性购买产品的应用内产品清单。

使用已废弃方法（例如 querySkuDetailsAsync()）的应用版本将无法销售任何不向后兼容的基础方案或优惠。您可以在此处了解向后兼容的优惠。

创建新的订阅产品清单后，您可以将应用迁移到 Google Play 结算库版本 5。使用应用 build.gradle 文件更新后的版本替换现有的 Play 结算库依赖项。

即使您没有修改任何方法调用，您的项目应该也会立即构建，因为我们已在 Play 结算库版本 6 中实现了向后兼容性。SKU 的概念被视为已废弃，但仍会存在，目的是使应用移植流程更简单且更循序渐进。

从 Android 应用启动购买交易的前几步保持不变：

为了获取用户符合购买条件的所有优惠，请按以下步骤操作：

请注意，查询结果现在是 ProductDetails，而不是 SkuDetails。每个 ProductDetails 项目都包含商品的相关信息（ID、商品名、类型等）。对于订阅商品，ProductDetails 包含一个 List<ProductDetails.SubscriptionOfferDetails>，即订阅优惠详情列表。对于一次性购买商品，ProductDetails 包含一个 ProductDetails.OneTimePurchaseOfferDetails。它们可用于确定要向用户显示哪些优惠。

queryProductDetailsAsync 的回调会返回一个 List<ProductDetails>。每个 ProductDetails 项目都包含商品的相关信息（ID、商品名、类型等）。主要区别在于，订阅商品现在还包含一个 List<ProductDetails.SubscriptionOfferDetails>，其中包含用户可以享受的所有优惠。

由于以前的 Play 结算库版本不支持新对象（订阅、基础方案、优惠等），因此新系统将每个订阅 SKU 转换为单个向后兼容的基础方案和优惠。可用的一次性购买商品也改为使用 ProductDetails 对象。您可以使用 getOneTimePurchaseOfferDetails() 方法访问一次性购买商品的优惠详情。

在极少数情况下，某些设备无法支持 ProductDetails 和 queryProductDetailsAsync()，这通常是因为 Google Play 服务版本已过时。为了确保对此场景提供适当的支持，请先针对 PRODUCT_DETAILS 功能调用 isFeatureSupported()，然后再调用 queryProductDetailsAsync。如果响应为 OK，表示设备支持该功能，您可以继续调用 queryProductDetailsAsync()。如果响应为 FEATURE_NOT_SUPPORTED，您可以改用 querySkuDetailsAsync() 请求可用的向后兼容产品列表。如需详细了解如何使用向后兼容功能，请参阅 2022 年 5 月的订阅功能指南。

启动优惠的购买流程与启动 SKU 的流程非常相似。如需使用版本 6 发起购买请求，请执行以下操作：

为了销售提供用户所选优惠的商品，请获取所选优惠的 offerToken，并将其传入 ProductDetailsParams 对象。

创建 BillingFlowParams 对象后，使用 BillingClient 启动结算流程的操作保持不变。

使用 Google Play 结算库版本 6 处理购买交易的操作与以前的版本类似。

如需拉取用户拥有的所有有效购买交易并查询新购买交易，请执行以下操作：

用于管理应用外购买和待处理交易的步骤没有变化。

您应该迁移后端中的订阅购买状态管理组件，以便处理在前面步骤中创建的新产品的购买交易。对于您在 2022 年 5 月发布之前定义的转换后订阅产品，您当前的订阅购买状态管理组件应该可以正常工作，它应该足以管理向后兼容优惠的购买交易，但不支持任何新功能。

您需要为订阅购买状态管理模块实现新的 Subscription Purchases API，该模块会在后端检查购买状态并管理 Play 结算服务订阅使用权。该 API 的旧版本不会返回在新平台中管理购买交易所需的所有详细信息。如需详细了解与先前版本相比的变化，请参阅 2022 年 5 月新订阅功能指南。

通常在每次收到 SubscriptionNotification 实时开发者通知时调用 Subscription Purchases API，即可拉取有关订阅状态的最新信息。您需要将对 purchases.subscriptions.get 的调用替换为新版本的 Subscription Purchases API purchases.subscriptionsv2.get。在新模型中，有一个名为 SubscriptionPurchaseV2 的新资源，可提供足够的信息来管理订阅的购买使用权。

此新端点会返回所有订阅产品和所有购买交易的状态，无论销售该产品的应用版本是什么，也不管该产品是何时定义的（2022 年 5 月版本之前或之后），因此在迁移后，您只需使用此版本的订阅购买状态管理模块。

在 Play 结算库 5 及更低版本中，ProrationMode 用于将更改应用于用户的订阅购买交易，例如升级或降级。在版本 6 中，它已被废弃，取而代之的是 ReplacementMode。

先前已废弃的 launchPriceConfirmationFlow API 已从 Play 结算库 6 中移除。如需了解替代方案，请参阅价格变动指南。

Play 结算库 6 中新增了 NETWORK_ERROR 代码，用于指明用户设备和 Google Play 系统之间的网络连接问题。代码 SERVICE_TIMEOUT 和 SERVICE_UNAVAILABLE 也发生了变化。如需了解详情，请参阅处理 BillingResult 响应代码。

从 6.0.0 版开始，Play 结算库不再为待处理的购买交易创建订单 ID。只有在购买交易变为 PURCHASED 状态后，系统才会为这类购买交易填充订单 ID。确保您的集成仅预期在交易全部完成后获得订单 ID。您仍可将购买令牌用作记录。如需详细了解如何处理待处理的购买交易，请参阅 Play 结算库集成指南和购买生命周期管理指南。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-21。

**Examples:**

Example 1 (python):
```python
dependencies {
    def billingVersion = "6.0.0"

    implementation "com.android.billingclient:billing:$billingVersion"
}
```

Example 2 (python):
```python
dependencies {
    def billingVersion = "6.0.0"

    implementation "com.android.billingclient:billing:$billingVersion"
}
```

Example 3 (unknown):
```unknown
val skuList = ArrayList<String>()

skuList.add("up_basic_sub")

val params = SkuDetailsParams.newBuilder()

params.setSkusList(skuList).setType(BillingClient.SkuType.SUBS).build()

billingClient.querySkuDetailsAsync(params) {
    billingResult,
    skuDetailsList ->
    // Process the result
}
```

Example 4 (unknown):
```unknown
List<String> skuList = new ArrayList<>();

skuList.add("up_basic_sub");

SkuDetailsParams.Builder params = SkuDetailsParams.newBuilder();

params.setSkusList(skuList).setType(SkuType.SUBS).build();

billingClient.querySkuDetailsAsync(params,
    new SkuDetailsResponseListener() {
        @Override
        public void onSkuDetailsResponse(BillingResult billingResult,
                List<SkuDetails> skuDetailsList) {
            // Process the result.
        }
    }
);
```

---
