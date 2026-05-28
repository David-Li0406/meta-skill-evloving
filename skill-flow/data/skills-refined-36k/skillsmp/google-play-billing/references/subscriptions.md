# Google-Play-Billing - Subscriptions

**Pages:** 5

---

## 订阅简介 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/subscriptions?hl=zh-cn

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

## 订阅简介 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/subscriptions

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

## 订阅生命周期 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/lifecycle/subscriptions

**Contents:**
- 订阅生命周期 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 处理自动续订型订阅的生命周期
  - 新自动续订型订阅购买交易
  - 续订
  - 宽限期
    - 宽限期访问权限和恢复订阅
  - 静默宽限期
  - 账号保留功能
    - 账号保留权限和恢复订阅
  - 到期

订阅购买交易在其生命周期中可能会经历多种不同状态，具体取决于许多因素，包括自动续订行为、付款遭拒情况和开发者管理操作。

当用户的订阅状态发生更改时，后端服务器会收到 SubscriptionNotification 消息。

如需更新后端中的状态，请使用通知中随附的购买令牌调用 purchases.subscriptionsv2.get API。此端点会根据购买令牌提供最新的订阅状态，同时被视为订阅管理的可信来源。

购买令牌的有效期是从订阅成功到订阅到期后 60 天。此日期过后，购买令牌不再有效，不能再用于调用 Google Play Developer API。

当用户购买订阅时，系统会向您的 RTDN 客户端发送一条类型为 SUBSCRIPTION_PURCHASED 的 SubscriptionNotification 消息。无论您接收此通知或注册新应用内购买交易的方法是通过 PurchasesUpdatedListener，还是在应用内以 onResume() 方法手动提取购买交易，都应在安全的后端处理新购买交易。为此，请按以下步骤操作：

Play 结算库还包含用于确认订阅的方法 acknowledgePurchase()，以及检查确认状态的方法 isAcknowledged()。不过，我们建议您在后端处理购买交易，以提高安全性。

对于非分期付款的自动续订型订阅，系统会在订阅续订时发送 SUBSCRIPTION_RENEWED 通知。对于分期付款订阅，系统会在每次在结算日期从订阅中扣款时发送 SUBSCRIPTION_RENEWED 通知。确保用户仍有权使用相应的订阅内容，然后使用从 Google Play Developer API 返回的订阅资源中提供的新 expiryTime 来更新订阅状态。订阅资源与以下示例类似：

如果订阅续订存在付款问题，Google 会通知用户，并在订阅到期前的一段时间内定期尝试续订。此恢复续订期可以由宽限期及后续的账号冻结期组成。在宽限期内，用户应仍有权访问其订阅内容。

queryPurchasesAsync() 方法会继续返回处于宽限期的购买交易。如果您的应用仅依赖于 queryPurchasesAsync 来检查用户是否有权访问订阅，则应自动处理宽限期，因为这些订阅会在 Play 结算库中显示为有效。

将订阅状态与后端同步可让您更清楚地了解付款遭拒的情况，并为您提供更多背景信息，助您尽力减少非自愿流失。监听类型为 SUBSCRIPTION_IN_GRACE_PERIOD 的 SubscriptionNotification 消息，以便在用户进入宽限期时收到通知。当用户处于宽限期时，订阅资源包含 autoRenewEnabled = true。Google Play 会动态扩大 expiryTime 值，直到宽限期届满为止。因为必须等到用户取消订阅或宽限期达到上限时，授权才失效。在此期间，subscriptionState 字段的值为 SUBSCRIPTION_STATE_IN_GRACE_PERIOD。订阅资源与以下示例类似：

Play 会在宽限期内通知用户付款遭拒，并提示他们在 Play 商店中修正付款方式问题。当用户进入宽限期时，您还应鼓励用户修正付款方式，以防发生非自愿的付款失败问题。可采用一个简单的方法执行此操作，即使用 In-App Messaging API。如果您在用户打开您的应用时调用此 API，用户会在临时信息条中看到一条告知其付款遭拒的 Play 消息。此消息还包含一个深层链接，以便用户修正 Google Play 中的付款方式。

一旦用户修正了付款方式，订阅就会按其原续订日期续订，而您可以按照续订中的说明处理续订。

如果用户在宽限期内未修正付款方式，那么订阅会进入账号保留状态，而用户会失去使用权。

图 2 展示了订阅进入宽限期、然后在用户解决付款方式问题后恢复订阅的时间线。宽限期结束后，用户应失去订阅权益并进入账号保留状态。

您可以将宽限期设置为 0 天，但 Play 至少会等待 1 天，以确保有足够的时间重试付款。此静默宽限期可为付款处理提供安全保障。在此 24 小时内，相应订阅会保持 ACTIVE 状态。

若要及时了解订阅状态变化，最好的方式是监听实时开发者通知 (RTDN) 并做出相应反应。在 RTDN 时间（而非到期时间）调用 purchases.subscriptionsv2.get() 方法，以获取更准确的订阅状态。

根据 24 小时的静默宽限期过后订阅的状态，您应该会收到以下通知之一：

您还可以在 24 小时的静默宽限期过后随时调用 subscriptionV2.get() 方法，以获取订阅的最新状态。

如果订阅续订存在付款问题，在任何宽限期结束后，账号冻结期便会开始。当订阅进入账号保留状态后，您应阻止用户访问订阅内容。

在账号冻结期间，您应根据需要处理任何取消、恢复或重新购买订阅的事件，因为当订阅处于冻结状态时，用户可能会做出这些更改。

在用户进入账号保留期时，系统会发送 RTDN 通知，以便您尽快告知他们订阅内容暂时无法访问的原因。可采用一个简单的方法执行此操作，即使用 In-App Messaging API。如果当用户打开应用时调用此 API，用户会在临时信息条中看到一条告知其付款遭拒的消息。此消息还包含一个深层链接，以便用户修正 Google Play 中的付款方式。

如果用户可以在您的应用外访问订阅内容，他们可能会发现自己已在不同平台上失去访问权限。您可能需要向用户发送推送通知或电子邮件，告知用户其订阅已因付款遭拒而失效。

在账号保留期间，queryPurchasesAsync() 方法不会返回订阅，因此，如果应用依赖于此方法显示现有购买交易，则您应默认支持账号保留功能。

利用实时开发者通知，当订阅进入账号保留状态时，您会收到类型为 SUBSCRIPTION_ON_HOLD 的 SubscriptionNotification。从安全的后端服务器调用 purchases.subscriptionsv2.get 可检索新的订阅信息。在账号保留期间，订阅资源的 expiryTime 设为过去的时间戳，并且subscriptionState 字段设为 SUBSCRIPTION_STATE_ON_HOLD：

要恢复访问权限，用户必须修正其付款方式。Play 会通知用户账号因付款遭拒而处于账号保留状态，而您应鼓励他们修正付款方式。

用户修正其付款方式后，订阅会恢复为活动状态，您随后必须恢复用户对订阅内容的访问权限。在这种情况下，购买令牌与账号保留状态开始之前相同，因为系统正在恢复同一购买交易，并且您会收到类型为 SUBSCRIPTION_RECOVERED 的 RTDN。

对于分期付款订阅，任何一次付款尝试都可能出现付款遭拒和付款恢复的情况。

恢复后，Play 结算库会通过 queryPurchasesAsync() 方法再次返回订阅。如果您使用此方法确定用户是否有权访问订阅，则您的应用应自动处理订阅从账号冻结状态的恢复。

监听类型为 SUBSCRIPTION_RECOVERED 的 SubscriptionNotification 消息，以便在订阅已恢复且用户应重新获得访问权限时收到通知。如果您在收到此通知后查询订阅，则 expiryTime 字段会设为将来的时间戳，并且 subscriptionState 字段会再次设为 SUBSCRIPTION_STATE_ACTIVE：

如果用户在账号保留期结束之前未修正付款方式，系统会改为发送类型为 SUBSCRIPTION_CANCELED 的 RTDN。有关处理取消的说明，请参阅取消。当您查询以这种方式取消的订阅时，返回的 expiryTime 字段会设为过去的时间戳：

您在账号保留期间收到取消通知后，系统会立即发送类型为 SUBSCRIPTION_EXPIRED 的 RTDN，因为用户已失去付费使用权，并因订阅取消而流失。您可以按照常规方式处理这种到期情况。

在原购买交易的账号保留期间，用户可以重新购买订阅方案或您通过应用提供的任何其他方案，从而重新获得访问权限。在这种情况下，系统会签发新的购买令牌，并返回新值，作为代表此新实例的 SUBSCRIPTION_PURCHASED 事件的一部分。

图 3 展示了订阅进入账号保留状态、然后在用户解决付款方式问题后恢复订阅的时间线。

与上一个示例类似，图 4 显示了订阅在进入账号保留状态之前先进入宽限期的，然后在处于保留状态时恢复订阅的时间线。

订阅到期后，用户应失去对订阅的访问权限。在这种情况下，系统会发送类型为 SUBSCRIPTION_EXPIRED 的 SubscriptionNotification 消息。当您收到此通知时，应查询 Google Play Developer API，以获取最新的订阅资源。在确认 subscriptionState 为 SUBSCRIPTION_STATE_EXPIRED 后，请移除使用权并在后端中将购买状态注册为无效。订阅资源与以下示例类似：

用户可以主动从 Play 订阅中心取消订阅，也可以让订阅自动取消（如果在处于账号保留状态后没有恢复）。开发者还可以通过 purchases.subscriptionsv2.cancel 触发取消操作；取消订阅后，用户仍可继续访问相关内容，直到当前结算周期结束为止。结算周期结束后，访问权限应会被撤消。

取消非分期付款的自动续订型订阅会触发 SUBSCRIPTION_CANCELED 通知。当您收到此通知时，从 Google Play Developer API 返回的订阅资源会把 subscriptionState 字段设置为 SUBSCRIPTION_STATE_CANCELED，而 expiryTime 字段中会包含用户应失去对订阅的访问权限的日期。如果当天是过去的日期，用户应立即失去使用权。例如，如果用户在账号保留期间因付款遭拒而取消订阅，就可能会发生这种情况。

已取消的购买交易的订阅资源与以下示例类似：

对于分期付款型订阅，如果用户在承诺期内发起取消，但仍有款项未付，系统会发送 SUBSCRIPTION_CANCELLATION_SCHEDULED 通知。取消操作处于待处理状态，将在当前合约期结束时生效。当您收到此通知时，从 Google Play Developer API 返回的订阅资源会将 subscriptionState 字段设置为 SUBSCRIPTION_STATE_ACTIVE，因为分期付款订阅在承诺期结束之前仍处于有效状态。不过，存在一个空的 pendingCancellation 对象。 在合约期结束时，系统会先发送 SUBSCRIPTION_CANCELED 通知，然后发送 SUBSCRIPTION_EXPIRED 通知。

待取消的分期付款订阅购买交易的订阅资源与以下示例类似：

您可以查看订阅资源中的 canceledStateContext 字段，了解订阅被取消的原因（例如，订阅是由用户、系统还是您自己取消的）。如果订阅被用户取消，您可以查看 userInitiatedCancellation 字段，以了解用户取消订阅的原因。这有助于制定明智的通信策略。

如果订阅被取消但尚未到期，queryPurchasesAsync() 仍会返回该订阅。您可能需要在应用中显示一条消息，告知用户其订阅已被取消并提供到期日期。

系统可能会出于各种原因撤消订阅，包括您的后端使用 purchases.subscriptionsv2.revoke 撤消订阅或购买交易被退款。在这种情况下，请立即撤消用户的权限。此时，系统会发送类型为 SUBSCRIPTION_REVOKED 的 SubscriptionNotification 消息。当您收到此通知时，从 Google Play Developer API 返回的订阅资源会把 subscriptionState 字段设置为 SUBSCRIPTION_STATE_EXPIRED。

已撤消的购买交易的订阅资源与以下示例类似：

需要延长用户使用权的原因有很多。例如，您可能想要将免费访问权限作为一种特别优惠提供给用户，如购买电影时免费一周，或向客户提供免费访问权限以表达善意。您可以使用 Play Developer API 中的 purchases.subscriptions.defer 方法，将自动续订型的下一个结算日期延后。执行此操作时，系统会发送一条类型为 SUBSCRIPTION_DEFERRED 的 SubscriptionNotification 消息。在推迟期内，用户会订阅您的内容并且拥有完全访问权限，但不会被扣款。订阅续订日期会更新以反映新的日期。

对于预付费方案，您可以使用推迟结算 API 来推迟到期时间。

您可以通过让用户能够暂停订阅来防止主动取消订阅的用户流失。在您启用暂停功能后，用户可以选择暂停订阅一段时间（介于一周到三个月之间），具体取决于订阅的续订周期。

只有在当前结算周期结束后，订阅暂停才会生效。订阅暂停后，用户将无法访问订阅，也无需支付续订费用。在暂停期结束时，订阅将恢复，并且 Google 会尝试续订订阅。如果恢复成功，订阅将再次变为活动状态。如果由于付款问题导致恢复失败，用户将进入账号保留状态，如图 5 和图 6 所示：

用户也可以选择在暂停期内随时手动恢复订阅，如图 6 所示。当用户手动恢复订阅时，结算日期将更改为手动恢复日期。

用户的订阅暂停后，除非将相应订阅的 isSuspended 参数设置为 true，否则 Play 结算库不会通过 queryPurchasesAsync() 方法返回订阅。如果恢复了订阅，queryPurchasesAsync() 方法会再次返回订阅。

监听 RTDN，了解用户何时暂停订阅。利用这些通知，还可以在您的应用中通知用户他们已暂停订阅，因而无法访问订阅。您还应使用 Google Play 深层链接来为用户提供一种随时手动恢复订阅的方法。

当用户发起订阅暂停时，系统会发送类型为 SUBSCRIPTION_PAUSE_SCHEDULE_CHANGED 的 SubscriptionNotification 消息。此时，用户应保持对订阅的访问权限，直到下一个续订日期，并且订阅资源包含 autoRenewEnabled = true。此时，subscriptionState 字段的值为 SUBSCRIPTION_STATE_ACTIVE。

当暂停生效时，系统会发送类型为 SUBSCRIPTION_PAUSED 的 SubscriptionNotification 消息。此时，用户应失去对订阅的访问权限，并且订阅资源包含 autoRenewEnabled = true，subscriptionState 字段设为 SUBSCRIPTION_STATE_PAUSED。您可以通过查看 PausedStateContext 对象来了解订阅预计何时再次续订。

如果在暂停期结束时自动恢复了订阅或用户选择了手动恢复订阅，系统会发送类型为 SUBSCRIPTION_RECOVERED 的 SubscriptionNotification 消息。

如果尝试恢复订阅时付款失败，系统会发送类型为 SUBSCRIPTION_ON_HOLD 的 SubscriptionNotification 消息。

对于自动续订型订阅基础方案，Google Play 商店可能会显示重新订阅按钮。通过此按钮，用户可以重新获得对订阅的访问权限。此按钮可能会出于各种原因而未显示，例如订阅在很久以前就已到期。

虽然该按钮始终带有重新订阅标签，但其功能取决于订阅状态。

当订阅被取消但尚未到期时，用户仍保持订阅状态并享受订阅权益。如果用户点按“重新订阅”，取消操作会被有效地撤消，订阅会继续续订。此操作在 Play 开发者文档和 API 中被称为“恢复”。

在自动续订型订阅到期后，您可以允许用户购买相同的订阅基础方案。此操作在 Play 开发者文档和 API 中被称为“重新订阅”。您可以在 Play 管理中心内或使用 API 为每个基础方案配置此选项。

如果您的应用仅依赖于 queryPurchasesAsync() 方法来确定用户是否有权访问订阅，则应自动处理恢复，因为 queryPurchasesAsync() 方法会在到期日之前继续返回已取消的购买内容。已恢复的订阅会继续续订，就像未取消过一样。

如果您的应用与后端同步订阅状态，您就应监听类型为 SUBSCRIPTION_RESTARTED 的 SubscriptionNotification 消息。收到此 RTDN 后，您的应用可以对其做出响应，记录订阅现已设为续订，并停止在您的应用中显示恢复消息。订阅资源与下面的内容类似：

如果使用 Google Play 管理中心或 API 将自动续订型基础方案配置为允许重新订阅，用户就可以在 Google Play 商店中重新购买已到期的订阅。

这些是新的购买交易。Google Play 会签发全新的购买令牌，而您的后端会收到类型为 SUBSCRIPTION_PURCHASED 的 RTDN。在这种情况下，此类应用外购买交易的状态不包含与原始购买交易关联的 linkedPurchaseToken，因为原始订阅已完全到期。

为确保重新购买的订阅与用户正确关联，并防止系统因未确认的购买交易而自动退款，您必须在后端服务器上确认重新购买交易：

使用来自 RTDN 的新购买令牌调用 purchases.subscriptionsv2.get。此类应用外购买交易的响应包含 outOfAppPurchaseContext 字段，该字段仅适用于未经确认的重新订阅购买交易。此字段提供：

您可以使用任一标识符在后端中查找新购买交易，并将其与正确的用户账号相关联。

调用 purchases.subscriptions.acknowledge 以确认购买。

借助这种服务器端方法，即使在用户未打开应用的情况下，您也可以在购买交易完成后的三天内确认购买交易。

如果用户升级、降级或在订阅到期之前从应用中取消后又订阅，旧订阅会失效，并且新订阅会通过新的购买令牌创建。

此外，订阅资源从 Google Play Developer API 返回的这个网页中包含linkedPurchaseToken表示用户升级、降级或重新订阅时所基于的旧购买交易的字段。您可以在该字段中使用购买令牌查找旧订阅并识别现有用户账号，以便将新购买交易与同一账号关联。

在应用中向用户提供升级、降级或重新订阅选项之前，您必须确认现有订阅。如果现有订阅正在等待确认，任何方案更改或重新订阅操作都会被阻止。

如果用户通过购买交易成功升级/降级了订阅或重新订阅，这就是一笔您必须确认的新购买交易。建议您使用 Google Play Developer API 进行确认。订阅资源与以下示例类似：

请参阅价格变动最佳做法指南，了解如何更改自动续订价格并在适当情况下通知用户。

添加价格变动时以及价格变动状态发生任何更新时，您都会收到 SUBSCRIPTION_PRICE_CHANGE_UPDATED RTDN。您可以查询 purchases.subscriptionsv2.get 端点，以获取订阅资源，该资源将包含订阅中每个商品的价格变动详细信息。

当价格变动作为旧式订阅应用到现有订阅者时，如果用户采取措施确认或拒绝新价格，您将收到 RTDN。

当用户接受订阅价格上调时，您会收到类型为 SUBSCRIPTION_PRICE_CHANGE_UPDATED 的 SubscriptionNotification 消息。

如果价格下调，或者在订阅价格上调后续订，您会收到类型为 SUBSCRIPTION_RENEWED 的 SubscriptionNotification 消息。将此通知视为其他任何续订。

如果用户未在需要以更高价格续订之前选择接受价格上调，则会自动退订，并且您会收到类型为 SUBSCRIPTION_CANCELED 的 SubscriptionNotification 消息。可以按照取消部分的说明来处理此事件。

用户也可以按照同样的机制取消订阅，以免价格上调。

根据韩国 (KR) 新法规，韩国境内的订阅用户必须同意在免费试用期或初次体验期结束后进行的价格上调。

为帮助您遵守相关法规，Play 会向韩国地区的用户告知意见征求要求，并存储用户的意见征求响应。如果用户未在价格上调生效之前表示同意，系统会自动取消其订阅。除了 Play 发送的通知之外，您还可以向用户发送自定义的价格上调通知，并可以在通知中提供指向特定管理页面的链接。

当同意期限开始或用户已提供同意声明时，您将收到类型为 SUBSCRIPTION_PRICE_STEP_UP_CONSENT_UPDATED 的 SubscriptionNotification 消息。

price step-up是指因从一个优惠阶段过渡到另一个优惠阶段而导致的订阅价格上涨。例如，订阅从免费试用期过渡到正常价格。

不过，price change是指您（开发者）针对订阅的基础方案价格发起的价格更新。例如，用户接受才生效的价格上调或用户拒绝才无效的价格上调。

与自动续订型订阅一样，您必须在每次新购买后确认预付费方案。对于预付费方案，您必须同时处理初始购买交易和所有充值交易，因为用户每次都必须完成购买流程。

由于预付费方案的时长有可能比较短，因此请务必尽快确认购买交易。时长为一周或更长时间的预付费方案必须在三天内确认。对于时长不到一周的预付费方案，其确认时间不得晚于方案时长过半之时。例如，开发者必须在 1.5 天内确认购买时长为三天的预付费方案。

每当购买预付费方案订阅（包括每次充值）时，系统都会向您的 RTDN 客户端发送类型为 SUBSCRIPTION_PURCHASED 的 SubscriptionNotification 消息。调用 purchases.subscriptionsv2.get 方法可检查最新的预付费方案订阅状态。

系统会针对充值购买交易发放新的购买令牌，并且作为新订阅购买状态的一部分，您会在 linkedPurchaseToken 字段中收到之前的购买令牌。购买令牌的有效期是从订阅成功到订阅到期后 60 天。此日期过后，购买令牌不再有效，不能再用于调用 Google Play Developer API。

您可以在 expiryTime 字段中查看使用权何时结束。充值购买通过累积使用权来增加权限有效期。这意味着，如果用户在初始使用权结束之前充值，系统会在其先前的到期日期之前添加新时间。

您可能需要在应用中显示一条消息，告知用户可通过充值来续订他们的预付费订阅。如需了解用户何时能够充值，请查看订阅资源中的 allowExtendAfterTime 字段。

预付费方案不会自动续订，因此无法取消。如果用户想要取消预付费方案，则可以让其到期。

为了支持由用户延期而不是自动续订的预付费方案，新增了一些字段。所有字段都适用于预付费方案，正如其适用于自动续订型订阅一样，但以下字段除外：

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-11-19。

**Examples:**

Example 1 (unknown):
```unknown
{
  "kind": "androidpublisher#subscriptionPurchaseV2",
  "startTime": "2022-04-22T18:39:58.270Z",
  "regionCode": "US",
  "subscriptionState": "SUBSCRIPTION_STATE_ACTIVE",
  "latestOrderId": "GPA.3333-4137-0319-36762",
  "acknowledgementState": "ACKNOWLEDGEMENT_STATE_PENDING", // need to acknowledge new purchases
  "lineItems": [
    {
      "productId": "sub_variant_plan01",
      "expiryTime": next_renewal_date,
      "autoRenewingPlan": {
        "autoRenewEnabled": true
      }
    }
  ],
}
```

Example 2 (unknown):
```unknown
{
  "kind": "androidpublisher#subscriptionPurchaseV2",
  "startTime": "2022-04-22T18:39:58.270Z",
  "regionCode": "US",
  "subscriptionState": "SUBSCRIPTION_STATE_ACTIVE",
  "latestOrderId": "GPA.3333-4137-0319-36762",
  "acknowledgementState": "ACKNOWLEDGEMENT_STATE_PENDING", // need to acknowledge new purchases
  "lineItems": [
    {
      "productId": "sub_variant_plan01",
      "expiryTime": next_renewal_date,
      "autoRenewingPlan": {
        "autoRenewEnabled": true
      }
    }
  ],
}
```

Example 3 (unknown):
```unknown
{
  "kind": "androidpublisher#subscriptionPurchaseV2",
  "startTime": "2022-04-22T18:39:58.270Z",
  "regionCode": "US",
  "subscriptionState": "SUBSCRIPTION_STATE_ACTIVE",
  "latestOrderId": "GPA.3333-4137-0319-36762",
  "acknowledgementState": "ACKNOWLEDGEMENT_STATE_ACKNOWLEDGED",
  "lineItems": [
    {
      "productId": "sub_variant_plan01",
      "expiryTime": next_renewal_date,
      "autoRenewingPlan": {
        "autoRenewEnabled": true
      }
    }
  ]
}
```

Example 4 (unknown):
```unknown
{
  "kind": "androidpublisher#subscriptionPurchaseV2",
  "startTime": "2022-04-22T18:39:58.270Z",
  "regionCode": "US",
  "subscriptionState": "SUBSCRIPTION_STATE_ACTIVE",
  "latestOrderId": "GPA.3333-4137-0319-36762",
  "acknowledgementState": "ACKNOWLEDGEMENT_STATE_ACKNOWLEDGED",
  "lineItems": [
    {
      "productId": "sub_variant_plan01",
      "expiryTime": next_renewal_date,
      "autoRenewingPlan": {
        "autoRenewEnabled": true
      }
    }
  ]
}
```

---

## 订阅简介 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/billing_subscriptions?hl=zh-cn

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

## 订阅生命周期 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/lifecycle/subscriptions?hl=zh-cn

**Contents:**
- 订阅生命周期 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 处理自动续订型订阅的生命周期
  - 新自动续订型订阅购买交易
  - 续订
  - 宽限期
    - 宽限期访问权限和恢复订阅
  - 静默宽限期
  - 账号保留功能
    - 账号保留权限和恢复订阅
  - 到期

订阅购买交易在其生命周期中可能会经历多种不同状态，具体取决于许多因素，包括自动续订行为、付款遭拒情况和开发者管理操作。

当用户的订阅状态发生更改时，后端服务器会收到 SubscriptionNotification 消息。

如需更新后端中的状态，请使用通知中随附的购买令牌调用 purchases.subscriptionsv2.get API。此端点会根据购买令牌提供最新的订阅状态，同时被视为订阅管理的可信来源。

购买令牌的有效期是从订阅成功到订阅到期后 60 天。此日期过后，购买令牌不再有效，不能再用于调用 Google Play Developer API。

当用户购买订阅时，系统会向您的 RTDN 客户端发送一条类型为 SUBSCRIPTION_PURCHASED 的 SubscriptionNotification 消息。无论您接收此通知或注册新应用内购买交易的方法是通过 PurchasesUpdatedListener，还是在应用内以 onResume() 方法手动提取购买交易，都应在安全的后端处理新购买交易。为此，请按以下步骤操作：

Play 结算库还包含用于确认订阅的方法 acknowledgePurchase()，以及检查确认状态的方法 isAcknowledged()。不过，我们建议您在后端处理购买交易，以提高安全性。

对于非分期付款的自动续订型订阅，系统会在订阅续订时发送 SUBSCRIPTION_RENEWED 通知。对于分期付款订阅，系统会在每次在结算日期从订阅中扣款时发送 SUBSCRIPTION_RENEWED 通知。确保用户仍有权使用相应的订阅内容，然后使用从 Google Play Developer API 返回的订阅资源中提供的新 expiryTime 来更新订阅状态。订阅资源与以下示例类似：

如果订阅续订存在付款问题，Google 会通知用户，并在订阅到期前的一段时间内定期尝试续订。此恢复续订期可以由宽限期及后续的账号冻结期组成。在宽限期内，用户应仍有权访问其订阅内容。

queryPurchasesAsync() 方法会继续返回处于宽限期的购买交易。如果您的应用仅依赖于 queryPurchasesAsync 来检查用户是否有权访问订阅，则应自动处理宽限期，因为这些订阅会在 Play 结算库中显示为有效。

将订阅状态与后端同步可让您更清楚地了解付款遭拒的情况，并为您提供更多背景信息，助您尽力减少非自愿流失。监听类型为 SUBSCRIPTION_IN_GRACE_PERIOD 的 SubscriptionNotification 消息，以便在用户进入宽限期时收到通知。当用户处于宽限期时，订阅资源包含 autoRenewEnabled = true。Google Play 会动态扩大 expiryTime 值，直到宽限期届满为止。因为必须等到用户取消订阅或宽限期达到上限时，授权才失效。在此期间，subscriptionState 字段的值为 SUBSCRIPTION_STATE_IN_GRACE_PERIOD。订阅资源与以下示例类似：

Play 会在宽限期内通知用户付款遭拒，并提示他们在 Play 商店中修正付款方式问题。当用户进入宽限期时，您还应鼓励用户修正付款方式，以防发生非自愿的付款失败问题。可采用一个简单的方法执行此操作，即使用 In-App Messaging API。如果您在用户打开您的应用时调用此 API，用户会在临时信息条中看到一条告知其付款遭拒的 Play 消息。此消息还包含一个深层链接，以便用户修正 Google Play 中的付款方式。

一旦用户修正了付款方式，订阅就会按其原续订日期续订，而您可以按照续订中的说明处理续订。

如果用户在宽限期内未修正付款方式，那么订阅会进入账号保留状态，而用户会失去使用权。

图 2 展示了订阅进入宽限期、然后在用户解决付款方式问题后恢复订阅的时间线。宽限期结束后，用户应失去订阅权益并进入账号保留状态。

您可以将宽限期设置为 0 天，但 Play 至少会等待 1 天，以确保有足够的时间重试付款。此静默宽限期可为付款处理提供安全保障。在此 24 小时内，相应订阅会保持 ACTIVE 状态。

若要及时了解订阅状态变化，最好的方式是监听实时开发者通知 (RTDN) 并做出相应反应。在 RTDN 时间（而非到期时间）调用 purchases.subscriptionsv2.get() 方法，以获取更准确的订阅状态。

根据 24 小时的静默宽限期过后订阅的状态，您应该会收到以下通知之一：

您还可以在 24 小时的静默宽限期过后随时调用 subscriptionV2.get() 方法，以获取订阅的最新状态。

如果订阅续订存在付款问题，在任何宽限期结束后，账号冻结期便会开始。当订阅进入账号保留状态后，您应阻止用户访问订阅内容。

在账号冻结期间，您应根据需要处理任何取消、恢复或重新购买订阅的事件，因为当订阅处于冻结状态时，用户可能会做出这些更改。

在用户进入账号保留期时，系统会发送 RTDN 通知，以便您尽快告知他们订阅内容暂时无法访问的原因。可采用一个简单的方法执行此操作，即使用 In-App Messaging API。如果当用户打开应用时调用此 API，用户会在临时信息条中看到一条告知其付款遭拒的消息。此消息还包含一个深层链接，以便用户修正 Google Play 中的付款方式。

如果用户可以在您的应用外访问订阅内容，他们可能会发现自己已在不同平台上失去访问权限。您可能需要向用户发送推送通知或电子邮件，告知用户其订阅已因付款遭拒而失效。

在账号保留期间，queryPurchasesAsync() 方法不会返回订阅，因此，如果应用依赖于此方法显示现有购买交易，则您应默认支持账号保留功能。

利用实时开发者通知，当订阅进入账号保留状态时，您会收到类型为 SUBSCRIPTION_ON_HOLD 的 SubscriptionNotification。从安全的后端服务器调用 purchases.subscriptionsv2.get 可检索新的订阅信息。在账号保留期间，订阅资源的 expiryTime 设为过去的时间戳，并且subscriptionState 字段设为 SUBSCRIPTION_STATE_ON_HOLD：

要恢复访问权限，用户必须修正其付款方式。Play 会通知用户账号因付款遭拒而处于账号保留状态，而您应鼓励他们修正付款方式。

用户修正其付款方式后，订阅会恢复为活动状态，您随后必须恢复用户对订阅内容的访问权限。在这种情况下，购买令牌与账号保留状态开始之前相同，因为系统正在恢复同一购买交易，并且您会收到类型为 SUBSCRIPTION_RECOVERED 的 RTDN。

对于分期付款订阅，任何一次付款尝试都可能出现付款遭拒和付款恢复的情况。

恢复后，Play 结算库会通过 queryPurchasesAsync() 方法再次返回订阅。如果您使用此方法确定用户是否有权访问订阅，则您的应用应自动处理订阅从账号冻结状态的恢复。

监听类型为 SUBSCRIPTION_RECOVERED 的 SubscriptionNotification 消息，以便在订阅已恢复且用户应重新获得访问权限时收到通知。如果您在收到此通知后查询订阅，则 expiryTime 字段会设为将来的时间戳，并且 subscriptionState 字段会再次设为 SUBSCRIPTION_STATE_ACTIVE：

如果用户在账号保留期结束之前未修正付款方式，系统会改为发送类型为 SUBSCRIPTION_CANCELED 的 RTDN。有关处理取消的说明，请参阅取消。当您查询以这种方式取消的订阅时，返回的 expiryTime 字段会设为过去的时间戳：

您在账号保留期间收到取消通知后，系统会立即发送类型为 SUBSCRIPTION_EXPIRED 的 RTDN，因为用户已失去付费使用权，并因订阅取消而流失。您可以按照常规方式处理这种到期情况。

在原购买交易的账号保留期间，用户可以重新购买订阅方案或您通过应用提供的任何其他方案，从而重新获得访问权限。在这种情况下，系统会签发新的购买令牌，并返回新值，作为代表此新实例的 SUBSCRIPTION_PURCHASED 事件的一部分。

图 3 展示了订阅进入账号保留状态、然后在用户解决付款方式问题后恢复订阅的时间线。

与上一个示例类似，图 4 显示了订阅在进入账号保留状态之前先进入宽限期的，然后在处于保留状态时恢复订阅的时间线。

订阅到期后，用户应失去对订阅的访问权限。在这种情况下，系统会发送类型为 SUBSCRIPTION_EXPIRED 的 SubscriptionNotification 消息。当您收到此通知时，应查询 Google Play Developer API，以获取最新的订阅资源。在确认 subscriptionState 为 SUBSCRIPTION_STATE_EXPIRED 后，请移除使用权并在后端中将购买状态注册为无效。订阅资源与以下示例类似：

用户可以主动从 Play 订阅中心取消订阅，也可以让订阅自动取消（如果在处于账号保留状态后没有恢复）。开发者还可以通过 purchases.subscriptionsv2.cancel 触发取消操作；取消订阅后，用户仍可继续访问相关内容，直到当前结算周期结束为止。结算周期结束后，访问权限应会被撤消。

取消非分期付款的自动续订型订阅会触发 SUBSCRIPTION_CANCELED 通知。当您收到此通知时，从 Google Play Developer API 返回的订阅资源会把 subscriptionState 字段设置为 SUBSCRIPTION_STATE_CANCELED，而 expiryTime 字段中会包含用户应失去对订阅的访问权限的日期。如果当天是过去的日期，用户应立即失去使用权。例如，如果用户在账号保留期间因付款遭拒而取消订阅，就可能会发生这种情况。

已取消的购买交易的订阅资源与以下示例类似：

对于分期付款型订阅，如果用户在承诺期内发起取消，但仍有款项未付，系统会发送 SUBSCRIPTION_CANCELLATION_SCHEDULED 通知。取消操作处于待处理状态，将在当前合约期结束时生效。当您收到此通知时，从 Google Play Developer API 返回的订阅资源会将 subscriptionState 字段设置为 SUBSCRIPTION_STATE_ACTIVE，因为分期付款订阅在承诺期结束之前仍处于有效状态。不过，存在一个空的 pendingCancellation 对象。 在合约期结束时，系统会先发送 SUBSCRIPTION_CANCELED 通知，然后发送 SUBSCRIPTION_EXPIRED 通知。

待取消的分期付款订阅购买交易的订阅资源与以下示例类似：

您可以查看订阅资源中的 canceledStateContext 字段，了解订阅被取消的原因（例如，订阅是由用户、系统还是您自己取消的）。如果订阅被用户取消，您可以查看 userInitiatedCancellation 字段，以了解用户取消订阅的原因。这有助于制定明智的通信策略。

如果订阅被取消但尚未到期，queryPurchasesAsync() 仍会返回该订阅。您可能需要在应用中显示一条消息，告知用户其订阅已被取消并提供到期日期。

系统可能会出于各种原因撤消订阅，包括您的后端使用 purchases.subscriptionsv2.revoke 撤消订阅或购买交易被退款。在这种情况下，请立即撤消用户的权限。此时，系统会发送类型为 SUBSCRIPTION_REVOKED 的 SubscriptionNotification 消息。当您收到此通知时，从 Google Play Developer API 返回的订阅资源会把 subscriptionState 字段设置为 SUBSCRIPTION_STATE_EXPIRED。

已撤消的购买交易的订阅资源与以下示例类似：

需要延长用户使用权的原因有很多。例如，您可能想要将免费访问权限作为一种特别优惠提供给用户，如购买电影时免费一周，或向客户提供免费访问权限以表达善意。您可以使用 Play Developer API 中的 purchases.subscriptions.defer 方法，将自动续订型的下一个结算日期延后。执行此操作时，系统会发送一条类型为 SUBSCRIPTION_DEFERRED 的 SubscriptionNotification 消息。在推迟期内，用户会订阅您的内容并且拥有完全访问权限，但不会被扣款。订阅续订日期会更新以反映新的日期。

对于预付费方案，您可以使用推迟结算 API 来推迟到期时间。

您可以通过让用户能够暂停订阅来防止主动取消订阅的用户流失。在您启用暂停功能后，用户可以选择暂停订阅一段时间（介于一周到三个月之间），具体取决于订阅的续订周期。

只有在当前结算周期结束后，订阅暂停才会生效。订阅暂停后，用户将无法访问订阅，也无需支付续订费用。在暂停期结束时，订阅将恢复，并且 Google 会尝试续订订阅。如果恢复成功，订阅将再次变为活动状态。如果由于付款问题导致恢复失败，用户将进入账号保留状态，如图 5 和图 6 所示：

用户也可以选择在暂停期内随时手动恢复订阅，如图 6 所示。当用户手动恢复订阅时，结算日期将更改为手动恢复日期。

用户的订阅暂停后，除非将相应订阅的 isSuspended 参数设置为 true，否则 Play 结算库不会通过 queryPurchasesAsync() 方法返回订阅。如果恢复了订阅，queryPurchasesAsync() 方法会再次返回订阅。

监听 RTDN，了解用户何时暂停订阅。利用这些通知，还可以在您的应用中通知用户他们已暂停订阅，因而无法访问订阅。您还应使用 Google Play 深层链接来为用户提供一种随时手动恢复订阅的方法。

当用户发起订阅暂停时，系统会发送类型为 SUBSCRIPTION_PAUSE_SCHEDULE_CHANGED 的 SubscriptionNotification 消息。此时，用户应保持对订阅的访问权限，直到下一个续订日期，并且订阅资源包含 autoRenewEnabled = true。此时，subscriptionState 字段的值为 SUBSCRIPTION_STATE_ACTIVE。

当暂停生效时，系统会发送类型为 SUBSCRIPTION_PAUSED 的 SubscriptionNotification 消息。此时，用户应失去对订阅的访问权限，并且订阅资源包含 autoRenewEnabled = true，subscriptionState 字段设为 SUBSCRIPTION_STATE_PAUSED。您可以通过查看 PausedStateContext 对象来了解订阅预计何时再次续订。

如果在暂停期结束时自动恢复了订阅或用户选择了手动恢复订阅，系统会发送类型为 SUBSCRIPTION_RECOVERED 的 SubscriptionNotification 消息。

如果尝试恢复订阅时付款失败，系统会发送类型为 SUBSCRIPTION_ON_HOLD 的 SubscriptionNotification 消息。

对于自动续订型订阅基础方案，Google Play 商店可能会显示重新订阅按钮。通过此按钮，用户可以重新获得对订阅的访问权限。此按钮可能会出于各种原因而未显示，例如订阅在很久以前就已到期。

虽然该按钮始终带有重新订阅标签，但其功能取决于订阅状态。

当订阅被取消但尚未到期时，用户仍保持订阅状态并享受订阅权益。如果用户点按“重新订阅”，取消操作会被有效地撤消，订阅会继续续订。此操作在 Play 开发者文档和 API 中被称为“恢复”。

在自动续订型订阅到期后，您可以允许用户购买相同的订阅基础方案。此操作在 Play 开发者文档和 API 中被称为“重新订阅”。您可以在 Play 管理中心内或使用 API 为每个基础方案配置此选项。

如果您的应用仅依赖于 queryPurchasesAsync() 方法来确定用户是否有权访问订阅，则应自动处理恢复，因为 queryPurchasesAsync() 方法会在到期日之前继续返回已取消的购买内容。已恢复的订阅会继续续订，就像未取消过一样。

如果您的应用与后端同步订阅状态，您就应监听类型为 SUBSCRIPTION_RESTARTED 的 SubscriptionNotification 消息。收到此 RTDN 后，您的应用可以对其做出响应，记录订阅现已设为续订，并停止在您的应用中显示恢复消息。订阅资源与下面的内容类似：

如果使用 Google Play 管理中心或 API 将自动续订型基础方案配置为允许重新订阅，用户就可以在 Google Play 商店中重新购买已到期的订阅。

这些是新的购买交易。Google Play 会签发全新的购买令牌，而您的后端会收到类型为 SUBSCRIPTION_PURCHASED 的 RTDN。在这种情况下，此类应用外购买交易的状态不包含与原始购买交易关联的 linkedPurchaseToken，因为原始订阅已完全到期。

为确保重新购买的订阅与用户正确关联，并防止系统因未确认的购买交易而自动退款，您必须在后端服务器上确认重新购买交易：

使用来自 RTDN 的新购买令牌调用 purchases.subscriptionsv2.get。此类应用外购买交易的响应包含 outOfAppPurchaseContext 字段，该字段仅适用于未经确认的重新订阅购买交易。此字段提供：

您可以使用任一标识符在后端中查找新购买交易，并将其与正确的用户账号相关联。

调用 purchases.subscriptions.acknowledge 以确认购买。

借助这种服务器端方法，即使在用户未打开应用的情况下，您也可以在购买交易完成后的三天内确认购买交易。

如果用户升级、降级或在订阅到期之前从应用中取消后又订阅，旧订阅会失效，并且新订阅会通过新的购买令牌创建。

此外，订阅资源从 Google Play Developer API 返回的这个网页中包含linkedPurchaseToken表示用户升级、降级或重新订阅时所基于的旧购买交易的字段。您可以在该字段中使用购买令牌查找旧订阅并识别现有用户账号，以便将新购买交易与同一账号关联。

在应用中向用户提供升级、降级或重新订阅选项之前，您必须确认现有订阅。如果现有订阅正在等待确认，任何方案更改或重新订阅操作都会被阻止。

如果用户通过购买交易成功升级/降级了订阅或重新订阅，这就是一笔您必须确认的新购买交易。建议您使用 Google Play Developer API 进行确认。订阅资源与以下示例类似：

请参阅价格变动最佳做法指南，了解如何更改自动续订价格并在适当情况下通知用户。

添加价格变动时以及价格变动状态发生任何更新时，您都会收到 SUBSCRIPTION_PRICE_CHANGE_UPDATED RTDN。您可以查询 purchases.subscriptionsv2.get 端点，以获取订阅资源，该资源将包含订阅中每个商品的价格变动详细信息。

当价格变动作为旧式订阅应用到现有订阅者时，如果用户采取措施确认或拒绝新价格，您将收到 RTDN。

当用户接受订阅价格上调时，您会收到类型为 SUBSCRIPTION_PRICE_CHANGE_UPDATED 的 SubscriptionNotification 消息。

如果价格下调，或者在订阅价格上调后续订，您会收到类型为 SUBSCRIPTION_RENEWED 的 SubscriptionNotification 消息。将此通知视为其他任何续订。

如果用户未在需要以更高价格续订之前选择接受价格上调，则会自动退订，并且您会收到类型为 SUBSCRIPTION_CANCELED 的 SubscriptionNotification 消息。可以按照取消部分的说明来处理此事件。

用户也可以按照同样的机制取消订阅，以免价格上调。

根据韩国 (KR) 新法规，韩国境内的订阅用户必须同意在免费试用期或初次体验期结束后进行的价格上调。

为帮助您遵守相关法规，Play 会向韩国地区的用户告知意见征求要求，并存储用户的意见征求响应。如果用户未在价格上调生效之前表示同意，系统会自动取消其订阅。除了 Play 发送的通知之外，您还可以向用户发送自定义的价格上调通知，并可以在通知中提供指向特定管理页面的链接。

当同意期限开始或用户已提供同意声明时，您将收到类型为 SUBSCRIPTION_PRICE_STEP_UP_CONSENT_UPDATED 的 SubscriptionNotification 消息。

price step-up是指因从一个优惠阶段过渡到另一个优惠阶段而导致的订阅价格上涨。例如，订阅从免费试用期过渡到正常价格。

不过，price change是指您（开发者）针对订阅的基础方案价格发起的价格更新。例如，用户接受才生效的价格上调或用户拒绝才无效的价格上调。

与自动续订型订阅一样，您必须在每次新购买后确认预付费方案。对于预付费方案，您必须同时处理初始购买交易和所有充值交易，因为用户每次都必须完成购买流程。

由于预付费方案的时长有可能比较短，因此请务必尽快确认购买交易。时长为一周或更长时间的预付费方案必须在三天内确认。对于时长不到一周的预付费方案，其确认时间不得晚于方案时长过半之时。例如，开发者必须在 1.5 天内确认购买时长为三天的预付费方案。

每当购买预付费方案订阅（包括每次充值）时，系统都会向您的 RTDN 客户端发送类型为 SUBSCRIPTION_PURCHASED 的 SubscriptionNotification 消息。调用 purchases.subscriptionsv2.get 方法可检查最新的预付费方案订阅状态。

系统会针对充值购买交易发放新的购买令牌，并且作为新订阅购买状态的一部分，您会在 linkedPurchaseToken 字段中收到之前的购买令牌。购买令牌的有效期是从订阅成功到订阅到期后 60 天。此日期过后，购买令牌不再有效，不能再用于调用 Google Play Developer API。

您可以在 expiryTime 字段中查看使用权何时结束。充值购买通过累积使用权来增加权限有效期。这意味着，如果用户在初始使用权结束之前充值，系统会在其先前的到期日期之前添加新时间。

您可能需要在应用中显示一条消息，告知用户可通过充值来续订他们的预付费订阅。如需了解用户何时能够充值，请查看订阅资源中的 allowExtendAfterTime 字段。

预付费方案不会自动续订，因此无法取消。如果用户想要取消预付费方案，则可以让其到期。

为了支持由用户延期而不是自动续订的预付费方案，新增了一些字段。所有字段都适用于预付费方案，正如其适用于自动续订型订阅一样，但以下字段除外：

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-11-19。

**Examples:**

Example 1 (unknown):
```unknown
{
  "kind": "androidpublisher#subscriptionPurchaseV2",
  "startTime": "2022-04-22T18:39:58.270Z",
  "regionCode": "US",
  "subscriptionState": "SUBSCRIPTION_STATE_ACTIVE",
  "latestOrderId": "GPA.3333-4137-0319-36762",
  "acknowledgementState": "ACKNOWLEDGEMENT_STATE_PENDING", // need to acknowledge new purchases
  "lineItems": [
    {
      "productId": "sub_variant_plan01",
      "expiryTime": next_renewal_date,
      "autoRenewingPlan": {
        "autoRenewEnabled": true
      }
    }
  ],
}
```

Example 2 (unknown):
```unknown
{
  "kind": "androidpublisher#subscriptionPurchaseV2",
  "startTime": "2022-04-22T18:39:58.270Z",
  "regionCode": "US",
  "subscriptionState": "SUBSCRIPTION_STATE_ACTIVE",
  "latestOrderId": "GPA.3333-4137-0319-36762",
  "acknowledgementState": "ACKNOWLEDGEMENT_STATE_PENDING", // need to acknowledge new purchases
  "lineItems": [
    {
      "productId": "sub_variant_plan01",
      "expiryTime": next_renewal_date,
      "autoRenewingPlan": {
        "autoRenewEnabled": true
      }
    }
  ],
}
```

Example 3 (unknown):
```unknown
{
  "kind": "androidpublisher#subscriptionPurchaseV2",
  "startTime": "2022-04-22T18:39:58.270Z",
  "regionCode": "US",
  "subscriptionState": "SUBSCRIPTION_STATE_ACTIVE",
  "latestOrderId": "GPA.3333-4137-0319-36762",
  "acknowledgementState": "ACKNOWLEDGEMENT_STATE_ACKNOWLEDGED",
  "lineItems": [
    {
      "productId": "sub_variant_plan01",
      "expiryTime": next_renewal_date,
      "autoRenewingPlan": {
        "autoRenewEnabled": true
      }
    }
  ]
}
```

Example 4 (unknown):
```unknown
{
  "kind": "androidpublisher#subscriptionPurchaseV2",
  "startTime": "2022-04-22T18:39:58.270Z",
  "regionCode": "US",
  "subscriptionState": "SUBSCRIPTION_STATE_ACTIVE",
  "latestOrderId": "GPA.3333-4137-0319-36762",
  "acknowledgementState": "ACKNOWLEDGEMENT_STATE_ACKNOWLEDGED",
  "lineItems": [
    {
      "productId": "sub_variant_plan01",
      "expiryTime": next_renewal_date,
      "autoRenewingPlan": {
        "autoRenewEnabled": true
      }
    }
  ]
}
```

---
