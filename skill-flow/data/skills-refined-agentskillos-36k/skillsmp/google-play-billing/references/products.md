# Google-Play-Billing - Products

**Pages:** 15

---

## 供用户自选的其他结算方式的应用内集成指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/alternative/alternative-billing-with-user-choice-in-app?hl=zh-cn

**Contents:**
- 供用户自选的其他结算方式的应用内集成指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- Play 结算库设置
- 连接到 Google Play
  - Kotlin
  - Java
- 显示可购买的商品
- 启动用户自选结算流程
- 处理用户选择
  - 当用户选择备选结算系统时
  - Kotlin

本指南介绍了如何集成相关 API，以便在应用中提供需用户自选的其他结算方式。

向您的 Android 应用添加 Play 结算库依赖项。如需使用备选结算系统 API，您需要使用 5.2 或更高版本。如果您需要从较早版本迁移，请先按照迁移指南中的说明操作，然后再尝试实现备选结算系统。

集成流程的最初步骤与 Google Play 结算服务集成指南中所述的一些步骤相同，在初始化您的 BillingClient 时需进行一些调整：

以下示例演示了如何通过这些调整来初始化 BillingClient：

初始化 BillingClient 后，您需要按照集成指南中的说明与 Google Play 建立连接。

您可以采用集成 Google Play 结算系统的相同方式向用户显示可购买的商品。当用户看到可供购买的商品并选择购买时，请启动用户自选结算流程（如下一部分所述）。

通过调用 launchBillingFlow() 启动用户自选结算流程。这与通过集成 Google Play 结算系统来启动购买流程的方式相同：您需要提供 ProductDetails 实例和 offerToken（对应于用户想要获得的商品及服务）。如果用户选择 Google Play 结算系统，此信息将用于继续执行购买流程。

当开发者调用 launchBillingFlow() 时，Google Play 结算系统会执行以下检查：

在 BillingClient 设置期间调用 enableUserChoiceBilling

用户会看到标准的 Google Play 结算系统用户体验

在 BillingClient 设置期间未调用 enableUserChoiceBilling

用户会看到标准的 Google Play 结算系统用户体验

用户会看到标准的 Google Play 结算系统用户体验

购买流程其余部分的处理方式不尽相同，具体取决于用户选择的是 Google Play 结算系统还是一种备选结算系统。

如果用户选择备选结算系统，Google Play 会调用 UserChoiceBillingListener 来通知应用需在备选结算系统中启动购买流程。具体而言，系统会调用 userSelectedAlternativeBilling() 方法。

UserChoiceDetails 对象中提供的外部交易令牌表示用户选择进入备选结算流程时提供的签名。如后端集成指南中所述，使用此令牌可报告这一选择产生的任何交易。

UserChoiceBillingListener 应执行以下操作：

如果用户使用备选结算系统完成购买交易，您必须在 24 小时内从后端调用 Google Play Developer API 并提供 externalTransactionToken 以及其他交易详情，向 Google Play 报告此交易。如需了解详情，请参阅后端集成指南。

以下示例演示了如何实现 UserChoiceBillingListener：

如果用户选择 Google Play 结算系统，则可以继续通过 Google Play 进行购买交易。

如果开发者使用需用户自选的其他结算方式，则需要通过 Google Play 结算系统处理购买交易或使用 externalTransactionId 报告购买交易，具体取决于用户的选择。在订阅到期之前，通过用户选择流程来处理的对现有订阅的变更可通过同一结算系统实现。

本部分介绍了如何处理一些常见的订阅变更场景。

订阅方案变更（包括升级和降级流程）的处理方式应有所不同，具体取决于订阅最初是通过 Google Play 结算系统购买的，还是通过备选结算系统购买的。

依赖于现有订阅、共用相同付款方式且定期扣款时间一致的加购项将作为升级处理。对于其他加购项，用户应该能够选择要使用的结算系统。使用 launchBillingFlow() 启动新的购买体验，如启动用户自选结算流程中所述。

对于最初在用户选择后通过开发者的备选结算系统购买的订阅，请求升级或降级的用户应通过开发者的备选结算系统继续操作，无需用户再次选择。

为此，当用户请求升级或降级时，请调用 launchBillingFlow()。请使用 setOriginalExternalTransactionId 提供原始购买交易的外部交易 ID，而不是在参数中指定 SubscriptionUpdateParams 对象。采用这种方式不会显示用户选择界面，因为系统会保留原始购买交易的相关用户选择以用于升级和降级。在此使用场景中，调用 launchBillingFlow() 会为您可以从回调中检索的交易生成新的外部交易令牌。

在备选结算系统中完成升级或降级后，您需要使用通过之前针对新订阅购买交易的调用所获得的外部交易令牌来报告新交易。

同样，如果用户选择通过 Google Play 结算系统购买其当前订阅，系统应向该用户显示 Google Play 结算系统中的升级或降级流程。以下说明介绍了如何通过 Google Play 结算系统启动用于实现升级或降级的购买流程：

确定新方案所选产品/服务的 offerToken：

将正确的信息发送到 Google Play 结算系统以处理新的购买交易，包括现有订阅的购买令牌：

此购买交易会在 Google Play 结算系统中继续，您的应用会收到包含购买交易结果的 PurchasesUpdatedListener.onPurchaseUpdated 调用。如果购买交易成功，onPurchaseUpdated() 方法也会收到新的购买交易信息，而后端会收到 SUBSCRIPTION_PURCHASED 实时开发者通知。拉取新购买交易的状态时，linkedPurchaseToken 属性会关联到旧的订阅购买交易，以便您可以根据建议将其停用。

用户应该能够随时取消订阅。用户取消订阅后，使用权可能直到付费期结束才会终止。例如，如果用户在月中取消了月度订阅，可以在剩下的大约 2 周内继续使用该服务，直到其使用权限被撤消为止。在此期间，订阅在技术层面上仍处于活跃状态，因此用户可以使用该服务。

在这一活跃期内，用户决定撤消取消订阅操作的情况并不少见。在本指南中，此情况称为“恢复”。以下部分介绍了如何在备选结算系统 API 集成中处理恢复场景。

如果您有一项已取消的订阅的外部交易 ID，则无需调用 launchBillingFlow() 即可恢复该订阅，因此它不应被用于此类激活。如果用户在已取消的订阅的有效期内恢复订阅，则不会发生任何交易；如果当前周期到期后发生下次续订，您只需继续报告续订即可。这包括以下情形：用户在恢复期间会收到赠送金额或获享特殊续订价格（例如，一项旨在鼓励用户继续订阅的促销活动）。

通常，用户可以在 Google Play 结算系统中恢复订阅。对于最初通过 Google Play 结算系统购买的订阅，用户可以在订阅处于活跃状态时通过 Google Play 的重新订阅功能选择撤消之前的取消操作。在这种情况下，您会在后端收到 SUBSCRIPTION_RESTARTED 实时开发者通知，并且系统不会发放新的购买令牌，而会使用原始令牌来继续订阅。如需了解如何在 Google Play 结算系统中管理恢复订阅事宜，请参阅订阅管理指南中的恢复。

您还可以通过调用 launchBillingFlow()，从应用中触发 Google Play 结算系统中的恢复订阅流程。如需了解实现方法，请参阅订阅到期之前 - 应用内。如果用户完成了原始购买交易的用户选择流程（已取消，但仍处于活跃状态），系统会自动检测用户的选择，并显示用于恢复这些购买交易的界面。系统会提示用户通过 Google Play 确认重新购买相应订阅，但用户无需再次经历用户选择流程。在这种情况下，系统会为用户发放新的购买令牌。您的后端会收到 SUBSCRIPTION_PURCHASED 实时开发者通知，并且新购买交易状态的 linkedPurchaseToken 值会设为升级或降级情形下的状态，采用被取消的订阅之前所用的购买令牌。

如果订阅完全过期，无论是由于被取消还是未恢复且付款遭拒（账号保留期已过），如果用户想要重获使用权，必须重新订阅。

也可通过该应用来实现重新订阅，处理方法与标准订阅方式类似。用户应该能够选择要使用的结算系统。在这种情况下，系统可能会调用 launchBillingFlow()，如启动用户自选结算流程中所述。

许可测试人员应用于测试备选结算系统集成。您不会收到许可测试人员账号发起的交易的账单。如需详细了解如何配置许可测试人员，请参阅使用应用许可来测试应用内购结算功能。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-11-07。

**Examples:**

Example 1 (unknown):
```unknown
val purchasesUpdatedListener =
   PurchasesUpdatedListener { billingResult, purchases ->
       // Handle new Google Play purchase.
   }

val userChoiceBillingListener =
   UserChoiceBillingListener { userChoiceDetails ->
       // Handle alternative billing choice.
   }

val billingClient = BillingClient.newBuilder(context)
   .setListener(purchasesUpdatedListener)
   .enablePendingPurchases()
   .enableUserChoiceBilling(userChoiceBillingListener)
   .build()
```

Example 2 (unknown):
```unknown
val purchasesUpdatedListener =
   PurchasesUpdatedListener { billingResult, purchases ->
       // Handle new Google Play purchase.
   }

val userChoiceBillingListener =
   UserChoiceBillingListener { userChoiceDetails ->
       // Handle alternative billing choice.
   }

val billingClient = BillingClient.newBuilder(context)
   .setListener(purchasesUpdatedListener)
   .enablePendingPurchases()
   .enableUserChoiceBilling(userChoiceBillingListener)
   .build()
```

Example 3 (unknown):
```unknown
private PurchasesUpdatedListener purchasesUpdatedListener = new PurchasesUpdatedListener() {
    @Override
    public void onPurchasesUpdated(BillingResult billingResult, List<Purchase> purchases) {
        // Handle new Google Play purchase.
    }
};

private UserChoiceBillingListener userChoiceBillingListener = new UserChoiceBillingListener() {
    @Override
    public void userSelectedAlternativeBilling(
        UserChoiceDetails userChoiceDetails) {
        // Handle new Google Play purchase.
    }
};

private BillingClient billingClient = BillingClient.newBuilder(context)
    .setListener(purchasesUpdatedListener)
    .enablePendingPurchases()
    .enableUserChoiceBilling(userChoiceBillingListener)
    .build();
```

Example 4 (unknown):
```unknown
private PurchasesUpdatedListener purchasesUpdatedListener = new PurchasesUpdatedListener() {
    @Override
    public void onPurchasesUpdated(BillingResult billingResult, List<Purchase> purchases) {
        // Handle new Google Play purchase.
    }
};

private UserChoiceBillingListener userChoiceBillingListener = new UserChoiceBillingListener() {
    @Override
    public void userSelectedAlternativeBilling(
        UserChoiceDetails userChoiceDetails) {
        // Handle new Google Play purchase.
    }
};

private BillingClient billingClient = BillingClient.newBuilder(context)
    .setListener(purchasesUpdatedListener)
    .enablePendingPurchases()
    .enableUserChoiceBilling(userChoiceBillingListener)
    .build();
```

---

## 处理 BillingResult 响应代码 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/errors?hl=zh-cn

**Contents:**
- 处理 BillingResult 响应代码 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 重试策略
  - 简单重试策略
  - 指数退避算法重试策略
- 可重试的 BillingResult 响应
  - NETWORK_ERROR（错误代码 12）
    - 问题
    - 可能的解决方案
  - SERVICE_TIMEOUT（错误代码 -3）
    - 问题

当 Play 结算库调用触发操作时，该库会返回 BillingResult 响应，并将结果告知开发者。例如，如果您使用 queryProductDetailsAsync 获取用户可用的优惠，则响应代码包含 OK 代码，并提供正确的 ProductDetails 对象；或者包含其他响应，指示无法提供 ProductDetails 对象的原因。

并非所有响应代码都是错误。BillingResponseCode 参考页面详细说明了本指南中讨论的每个响应。下面列举了一些未指示错误的响应代码：

当响应代码指示出现错误时，有时是因为暂时性条件而导致的，因此可以恢复。调用 Play 结算库方法时，如果返回的 BillingResponseCode 值指示可恢复的条件，您应重试调用。在其他情况下，条件不会被视为暂时条件，因此不建议重试。

暂时性错误需要采用不同的重试策略，具体取决于特定的因素，例如错误是发生在用户会话期间（例如，当用户正在进行购买流程时），还是发生在后台（例如，当您在 onResume 期间查询用户的现有购买交易时）。下面的重试策略部分提供了这些不同策略的示例，并且可重试的 BillingResult 响应部分给出了每个响应代码最适合的策略建议。

除了响应代码之外，一些错误响应还包括用于调试和记录的消息。

当用户正在会话中时，建议实现一个简单的重试策略，以便尽可能避免错误干扰用户体验。在这种情况下，我们建议采用简单的重试策略，将尝试次数上限作为退出条件。

以下示例展示了处理在建立 BillingClient 连接时出现的错误的简单重试策略：

我们建议对在后台发生的 Play 结算库操作使用指数退避算法，该算法在用户进行会话时不影响用户体验。

例如，在确认新购买交易时可以实现此算法，因为此操作可以在后台进行，如果出现错误，则不需要实时进行确认。

此错误表示设备和 Play 系统之间的网络连接出现问题。

若要恢复，请使用简单的重试策略或指数退避算法，具体取决于哪个操作触发了错误。

此错误表示在 Google Play 能够响应之前，请求已达到超时时间上限。例如，这可能是由于延迟执行 Play 结算库调用请求的操作所致。

这通常是暂时性问题。使用简单策略或指数退避算法策略重试请求，具体取决于哪个操作返回了错误。

与下面的 SERVICE_DISCONNECTED 不同，与 Google Play 结算服务的连接未中断，您只需重试任何尝试过的 Play 结算库操作。

此严重错误表示客户端应用通过 BillingClient 与 Google Play 商店服务的连接已中断。

Play 结算库 8.0.0 版引入了 enableAutoServiceReconnection() 功能。构建 BillingClient 时，强烈建议您启用此功能。这样一来，当服务处于断开连接状态时，库便会在进行结算 API 调用时自动尝试重新建立连接，从而显著减少此类错误的发生。

Play 结算库会自动尝试重新连接。如果您在进行 API 调用时仍收到 SERVICE_DISCONNECTED 响应代码，则表示该库在自动尝试后无法重新连接。在这种情况下，您应在应用中实现重试逻辑：

为尽可能避免此错误，请务必通过调用 BillingClient.isReady() 先检查与 Google Play 服务的连接，然后再使用 Play 结算库进行调用。

如需尝试从 SERVICE_DISCONNECTED 进行恢复，您的客户端应用应尝试使用 BillingClient.startConnection 重新建立连接。

与 SERVICE_TIMEOUT 一样，请使用简单的重试策略或指数退避算法，具体取决于哪个操作触发了错误。

从 Google Play 结算库 6.0.0 开始，网络问题将不再返回 SERVICE_UNAVAILABLE。在结算服务不可用且 SERVICE_TIMEOUT 已废弃的情况下，系统才会返回此错误。

此暂时性错误表示 Google Play 结算服务目前不可用。在大多数情况下，这意味着客户端设备与 Google Play 结算服务之间的任何位置出现网络连接问题。

这通常是暂时性问题。使用简单策略或指数退避算法策略重试请求，具体取决于哪个操作返回了错误。

与 SERVICE_DISCONNECTED 不同，与 Google Play 结算服务的连接未中断，您需要重试任何正在尝试的操作。

此错误表示购买过程中发生了用户结算错误。可能出现此问题的示例包括：

在这种情况下，自动重试不太可能有帮助。但是，如果用户解决了导致问题的情况，手动重试会有所帮助。例如，如果用户将其 Play 商店版本更新为受支持的版本，则手动重试初始操作可以解决问题。

如果用户没有处于会话状态时发生此错误，那么重试可能没有意义。 如果您因购买流程收到 BILLING_UNAVAILABLE 错误，很可能是因为用户在购买过程中收到了 Google Play 的反馈，并且可能知道错误所在。在这种情况下，您可以显示一条错误消息，说明出现了问题，并提供一个“重试”按钮，以便用户在解决问题后进行手动重试。

这是一个严重错误，表示 Google Play 本身存在内部问题。

有时，导致 ERROR 的内部 Google Play 问题是暂时性的，可以通过指数退避算法进行重试来缓解此问题。如果用户在会话中，建议进行简单的重试。

此响应表明，Google Play 用户已经拥有其尝试购买的订阅或一次性购买商品。在大多数情况下，这并非暂时性错误，除非它是由过时的 Google Play 缓存导致的。

为了避免此错误不是由缓存问题引起的，请勿在用户已经拥有某个商品时向其提供此商品供购买。在展示可供购买的商品时，请务必检查用户的权限，并相应地过滤用户可以购买的商品。当客户端应用因缓存问题而收到此错误时，此错误会触发 Google Play 的缓存，以便使用来自 Play 后端的最新数据进行更新。在这种情况下，在出现错误后重试应该能解决这个特定的瞬态情况。获得 ITEM_ALREADY_OWNED 后调用 BillingClient.queryPurchasesAsync()，检查用户是否已经购买了相应商品，如果没有，请实现一个简单的重试逻辑来重新尝试购买。

此购买响应表明，Google Play 用户并不拥有用户尝试替换、确认或使用的订阅或一次性购买商品。在大多数情况下，这并非暂时性错误，除非它是由 Google Play 的缓存进入过时状态导致的。

如果由于缓存问题而收到此错误，此错误会触发 Google Play 的缓存，以便使用来自 Play 后端的最新数据进行更新。出错后，通过一个简单的重试策略重试应能解决此特定瞬态错误。获得 ITEM_NOT_OWNED 后调用 BillingClient.queryPurchasesAsync()，检查用户是否已获取相应商品。如果没有，使用简单的重试逻辑重新尝试购买。

这一不可重试的错误表示用户的设备不支持 Google Play 结算服务功能，原因可能是 Play 商店版本较旧。

例如，某些用户的设备可能不支持应用内消息。

在调用 Play 结算库之前，请使用 BillingClient.isFeatureSupported() 检查功能支持情况。

此解决方案仅供参考，可能会以一种不引起中断的方式失败。

此用户无法购买 Google Play 结算服务订阅或一次性购买商品。

请确保您的应用按照建议通过 queryProductDetailsAsync 刷新商品详情。请考虑您的商品详情在 Play 管理中心配置上发生更改的频率，以在需要时实现额外的刷新。 仅尝试在 Google Play 结算服务上销售通过 queryProductDetailsAsync 返回正确信息的商品。检查商品资格配置是否存在不一致问题。例如，您可能正在查询某个商品，该商品仅在用户尝试购买的地区之外销售。若要让商品可供购买，必须将商品的状态设为有效，同时其所属的应用必须已发布并已在用户所在的国家/地区上架。

有时，尤其是在测试期间，商品配置一切都正确无误，但用户仍会看到此错误。这可能是由于商品详情在 Google 服务器上的传播延迟所致。请稍后再试。

这是一个严重错误，表明您未正确使用 API。例如，向 BillingClient.launchBillingFlow 提供不正确的参数可能会导致此错误。

确保您正确地使用了不同的 Play 结算库调用。此外，如需详细了解此错误，请查看调试消息。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

**Examples:**

Example 1 (javascript):
```javascript
class BillingClientWrapper(context: Context) : PurchasesUpdatedListener {
  // Initialize the BillingClient.
  private val billingClient = BillingClient.newBuilder(context)
    .setListener(this)
    .enablePendingPurchases()
    .build()

  // Establish a connection to Google Play.
  fun startBillingConnection() {
    billingClient.startConnection(object : BillingClientStateListener {
      override fun onBillingSetupFinished(billingResult: BillingResult) {
        if (billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
          Log.d(TAG, "Billing response OK")
          // The BillingClient is ready. You can now query Products Purchases.
        } else {
          Log.e(TAG, billingResult.debugMessage)
          retryBillingServiceConnection()
        }
      }

      override fun onBillingServiceDisconnected() {
        Log.e(TAG, "GBPL Service disconnected")
        retryBillingServiceConnection()
      }
    })
  }

  // Billing connection retry logic. This is a simple max retry pattern
  private fun retryBillingServiceConnection() {
    val maxTries = 3
    var tries = 1
    var isConnectionEstablished = false
    do {
      try {
        billingClient.startConnection(object : BillingClientStateListener {
          override fun onBillingSetupFinished(billingResult: BillingResult) {
            if (billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
              isConnectionEstablished = true
              Log.d(TAG, "Billing connection retry succeeded.")
            } else {
              Log.e(
                TAG,
                "Billing connection retry failed: ${billingResult.debugMessage}"
              )
            }
          }
        })
      } catch (e: Exception) {
        e.message?.let { Log.e(TAG, it) }
      } finally {
        tries++
      }
    } while (tries <= maxTries && !isConnectionEstablished)
  }
  ...
}
```

Example 2 (javascript):
```javascript
class BillingClientWrapper(context: Context) : PurchasesUpdatedListener {
  // Initialize the BillingClient.
  private val billingClient = BillingClient.newBuilder(context)
    .setListener(this)
    .enablePendingPurchases()
    .build()

  // Establish a connection to Google Play.
  fun startBillingConnection() {
    billingClient.startConnection(object : BillingClientStateListener {
      override fun onBillingSetupFinished(billingResult: BillingResult) {
        if (billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
          Log.d(TAG, "Billing response OK")
          // The BillingClient is ready. You can now query Products Purchases.
        } else {
          Log.e(TAG, billingResult.debugMessage)
          retryBillingServiceConnection()
        }
      }

      override fun onBillingServiceDisconnected() {
        Log.e(TAG, "GBPL Service disconnected")
        retryBillingServiceConnection()
      }
    })
  }

  // Billing connection retry logic. This is a simple max retry pattern
  private fun retryBillingServiceConnection() {
    val maxTries = 3
    var tries = 1
    var isConnectionEstablished = false
    do {
      try {
        billingClient.startConnection(object : BillingClientStateListener {
          override fun onBillingSetupFinished(billingResult: BillingResult) {
            if (billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
              isConnectionEstablished = true
              Log.d(TAG, "Billing connection retry succeeded.")
            } else {
              Log.e(
                TAG,
                "Billing connection retry failed: ${billingResult.debugMessage}"
              )
            }
          }
        })
      } catch (e: Exception) {
        e.message?.let { Log.e(TAG, it) }
      } finally {
        tries++
      }
    } while (tries <= maxTries && !isConnectionEstablished)
  }
  ...
}
```

Example 3 (unknown):
```unknown
private fun acknowledge(purchaseToken: String): BillingResult {
  val params = AcknowledgePurchaseParams.newBuilder()
    .setPurchaseToken(purchaseToken)
    .build()
  var ackResult = BillingResult()
  billingClient.acknowledgePurchase(params) { billingResult ->
    ackResult = billingResult
  }
  return ackResult
}

suspend fun acknowledgePurchase(purchaseToken: String) {

  val retryDelayMs = 2000L
  val retryFactor = 2
  val maxTries = 3

  withContext(Dispatchers.IO) {
    acknowledge(purchaseToken)
  }

  AcknowledgePurchaseResponseListener { acknowledgePurchaseResult ->
    val playBillingResponseCode =
    PlayBillingResponseCode(acknowledgePurchaseResult.responseCode)
    when (playBillingResponseCode) {
      BillingClient.BillingResponseCode.OK -> {
        Log.i(TAG, "Acknowledgement was successful")
      }
      BillingClient.BillingResponseCode.ITEM_NOT_OWNED -> {
        // This is possibly related to a stale Play cache.
        // Querying purchases again.
        Log.d(TAG, "Acknowledgement failed with ITEM_NOT_OWNED")
        billingClient.queryPurchasesAsync(
          QueryPurchasesParams.newBuilder()
            .setProductType(BillingClient.ProductType.SUBS)
            .build()
        )
        { billingResult, purchaseList ->
          when (billingResult.responseCode) {
            BillingClient.BillingResponseCode.OK -> {
              purchaseList.forEach { purchase ->
                acknowledge(purchase.purchaseToken)
              }
            }
          }
        }
      }
      in setOf(
         BillingClient.BillingResponseCode.ERROR,
         BillingClient.BillingResponseCode.SERVICE_DISCONNECTED,
         BillingClient.BillingResponseCode.SERVICE_UNAVAILABLE,
       ) -> {
        Log.d(
          TAG,
          "Acknowledgement failed, but can be retried --
          Response Code: ${acknowledgePurchaseResult.responseCode} --
          Debug Message: ${acknowledgePurchaseResult.debugMessage}"
        )
        runBlocking {
          exponentialRetry(
            maxTries = maxTries,
            initialDelay = retryDelayMs,
            retryFactor = retryFactor
          ) { acknowledge(purchaseToken) }
        }
      }
      in setOf(
         BillingClient.BillingResponseCode.BILLING_UNAVAILABLE,
         BillingClient.BillingResponseCode.DEVELOPER_ERROR,
         BillingClient.BillingResponseCode.FEATURE_NOT_SUPPORTED,
       ) -> {
        Log.e(
          TAG,
          "Acknowledgement failed and cannot be retried --
          Response Code: ${acknowledgePurchaseResult.responseCode} --
          Debug Message: ${acknowledgePurchaseResult.debugMessage}"
        )
        throw Exception("Failed to acknowledge the purchase!")
      }
    }
  }
}

private suspend fun <T> exponentialRetry(
  maxTries: Int = Int.MAX_VALUE,
  initialDelay: Long = Long.MAX_VALUE,
  retryFactor: Int = Int.MAX_VALUE,
  block: suspend () -> T
): T? {
  var currentDelay = initialDelay
  var retryAttempt = 1
  do {
    runCatching {
      delay(currentDelay)
      block()
    }
      .onSuccess {
        Log.d(TAG, "Retry succeeded")
        return@onSuccess;
      }
      .onFailure { throwable ->
        Log.e(
          TAG,
          "Retry Failed -- Cause: ${throwable.cause} -- Message: ${throwable.message}"
        )
      }
    currentDelay *= retryFactor
    retryAttempt++
  } while (retryAttempt < maxTries)

  return block() // last attempt
}
```

Example 4 (unknown):
```unknown
private fun acknowledge(purchaseToken: String): BillingResult {
  val params = AcknowledgePurchaseParams.newBuilder()
    .setPurchaseToken(purchaseToken)
    .build()
  var ackResult = BillingResult()
  billingClient.acknowledgePurchase(params) { billingResult ->
    ackResult = billingResult
  }
  return ackResult
}

suspend fun acknowledgePurchase(purchaseToken: String) {

  val retryDelayMs = 2000L
  val retryFactor = 2
  val maxTries = 3

  withContext(Dispatchers.IO) {
    acknowledge(purchaseToken)
  }

  AcknowledgePurchaseResponseListener { acknowledgePurchaseResult ->
    val playBillingResponseCode =
    PlayBillingResponseCode(acknowledgePurchaseResult.responseCode)
    when (playBillingResponseCode) {
      BillingClient.BillingResponseCode.OK -> {
        Log.i(TAG, "Acknowledgement was successful")
      }
      BillingClient.BillingResponseCode.ITEM_NOT_OWNED -> {
        // This is possibly related to a stale Play cache.
        // Querying purchases again.
        Log.d(TAG, "Acknowledgement failed with ITEM_NOT_OWNED")
        billingClient.queryPurchasesAsync(
          QueryPurchasesParams.newBuilder()
            .setProductType(BillingClient.ProductType.SUBS)
            .build()
        )
        { billingResult, purchaseList ->
          when (billingResult.responseCode) {
            BillingClient.BillingResponseCode.OK -> {
              purchaseList.forEach { purchase ->
                acknowledge(purchase.purchaseToken)
              }
            }
          }
        }
      }
      in setOf(
         BillingClient.BillingResponseCode.ERROR,
         BillingClient.BillingResponseCode.SERVICE_DISCONNECTED,
         BillingClient.BillingResponseCode.SERVICE_UNAVAILABLE,
       ) -> {
        Log.d(
          TAG,
          "Acknowledgement failed, but can be retried --
          Response Code: ${acknowledgePurchaseResult.responseCode} --
          Debug Message: ${acknowledgePurchaseResult.debugMessage}"
        )
        runBlocking {
          exponentialRetry(
            maxTries = maxTries,
            initialDelay = retryDelayMs,
            retryFactor = retryFactor
          ) { acknowledge(purchaseToken) }
        }
      }
      in setOf(
         BillingClient.BillingResponseCode.BILLING_UNAVAILABLE,
         BillingClient.BillingResponseCode.DEVELOPER_ERROR,
         BillingClient.BillingResponseCode.FEATURE_NOT_SUPPORTED,
       ) -> {
        Log.e(
          TAG,
          "Acknowledgement failed and cannot be retried --
          Response Code: ${acknowledgePurchaseResult.responseCode} --
          Debug Message: ${acknowledgePurchaseResult.debugMessage}"
        )
        throw Exception("Failed to acknowledge the purchase!")
      }
    }
  }
}

private suspend fun <T> exponentialRetry(
  maxTries: Int = Int.MAX_VALUE,
  initialDelay: Long = Long.MAX_VALUE,
  retryFactor: Int = Int.MAX_VALUE,
  block: suspend () -> T
): T? {
  var currentDelay = initialDelay
  var retryAttempt = 1
  do {
    runCatching {
      delay(currentDelay)
      block()
    }
      .onSuccess {
        Log.d(TAG, "Retry succeeded")
        return@onSuccess;
      }
      .onFailure { throwable ->
        Log.e(
          TAG,
          "Retry Failed -- Cause: ${throwable.cause} -- Message: ${throwable.message}"
        )
      }
    currentDelay *= retryFactor
    retryAttempt++
  } while (retryAttempt < maxTries)

  return block() // last attempt
}
```

---

## 添加奖励商品专用功能 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/billing_rewarded_products?hl=zh-cn

**Contents:**
- 添加奖励商品专用功能 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 确定应用的奖励商品
- 声明适合相应年龄段的广告
  - Kotlin
  - Java
- 加载视频广告
  - Kotlin
  - Java
- 向用户提供奖励购买
- 消耗购买

如需让您的用户能够获得应用内商品和福利，有种方法是创建奖励商品，即用户在观看视频广告后收到的商品。您为用户提供奖励商品后，他们就能获得应用内奖励和福利，而不必直接购买。

本文档介绍了如何实现奖励商品专用功能，并在本页的工作流程示意图部分说明了该过程。

奖励商品的 SkuType 为 INAPP。为了确保用户能够观看多个广告并获得多项奖励，需要消耗这些商品。

您必须先获取奖励商品的 SkuDetails，然后才能向用户提供相应商品。为此，请调用 querySkuDetailsAsync()，并指定 SkuType.INAPP 作为商品类型。

为帮助您遵守与儿童和未成年用户相关的法律义务（包括《儿童在线隐私保护法》(COPPA) 和《一般数据保护条例》(GDPR)），您的应用应声明哪些广告应在美国视为面向儿童的广告，以及哪些广告面向所在国家/地区适用的同意年龄以下的用户。AdMob 帮助中心的文章阐明了在哪些情况下应将广告请求标记为面向儿童的内容，以及在哪些情况下应将其标记为适合未满规定年龄的用户的内容，并说明了这样做的影响。

在创建应用的结算客户端时，请考虑是否应将激励广告请求视为面向儿童的内容，或此类请求是否应面向未满规定年龄的用户。如果广告请求应设有这些限制，请调用 setChildDirected() 和 setUnderAgeOfConsent() 方法，并将适当的值传递到每个方法中。

以下代码段显示了如何声明视频广告应适合儿童或未满规定年龄的用户：

在向您的用户显示用来观看视频广告以获得奖励商品的选项之前，您需要先加载相应视频。为此，请创建一个 RewardLoadParams 对象，将其与代表奖励商品的 SkuDetails 对象相关联。然后，调用结算客户端的 loadRewardedSku() 方法，传入 RewardLoadParams 对象和 RewardResponseListener 对象。

视频加载完毕后，系统会通知 RewardResponseListener 监听器。如果视频不可用或出现其他错误（例如，服务器超时），系统也会通知该监听器。

加载与应用的奖励商品关联的视频时，若要保持设备性能，请记住以下最佳做法：

在决定何时加载视频时，请在带宽使用率和应用响应能力之间找到适当的平衡，选择最适合您用例的时间：

以下代码段演示了加载在用户收到奖励商品之前播放的视频广告的过程：

如果 Google Play 结算库成功加载与奖励商品关联的视频（即，如果 RewardResponseListener 收到的 responseCode 为 BillingResponse.OK），您便可以启动结算流程。

您可以调用 launchBillingFlow() 以开始播放与奖励商品相关的广告，对其他所有类型的应用内商品使用的也是相同的方法。虽然用户不会通过直接购买获取奖励商品，但您仍然需要启用结算流程，因为只有这样用户才能获取并使用相应商品。

如需通知结算客户端用户已收到并消耗了奖励商品，请在结算客户端监听器的 onPurchasesUpdated() 方法中处理购买交易。请注意，需要消耗奖励购买。

要测试您的应用如何加载视频广告并为用户提供奖励商品，可让已获许可的测试人员来执行。默认情况下，他们会获得测试广告而不是真实广告。如需了解如何为这些测试人员设置账号，请参阅用户测试 Google Play 结算服务应用。

另一种测试方法是使用 android.test.reward 商品 ID。此特定商品是 Google Play 结算服务中的保留名称，因此您无需将其添加到 Play 管理中心内的应用内商品列表。

注意：在测试应用的奖励商品时，请勿使用实际商品；否则，您的账号可能会被标记为存在滥用或欺诈行为的账号。

不过，测试完成后，在向最终用户部署您的正式版应用之前，务必将 android.test.reward 替换为实际奖励商品的商品 ID。

以下序列图显示了用户、您的应用和 Google Play 结算库如何协同工作，向用户展示视频广告并授予用户访问奖励商品的权限：

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

**Examples:**

Example 1 (unknown):
```unknown
val billingClient = BillingClient.newBuilder(context)
        .setListener(this)
        .setChildDirected(ChildDirected.CHILD_DIRECTED)
        .setUnderAgeOfConsent(UnderAgeOfConsent.UNDER_AGE_OF_CONSENT)
        .build()
```

Example 2 (unknown):
```unknown
BillingClient billingClient =
    BillingClient.newBuilder(context)
        .setListener(this)
        .setChildDirected(ChildDirected.CHILD_DIRECTED)
        .setUnderAgeOfConsent(UnderAgeOfConsent.UNDER_AGE_OF_CONSENT)
        .build();
```

Example 3 (unknown):
```unknown
if (skuDetails.isRewarded()) {
    val params = RewardLoadParams.Builder()
            .setSkuDetails(skuDetails)
            .build()
    mBillingClient.loadRewardedSku(params.build(),
            object : RewardResponseListener {
        override fun onRewardResponse(@BillingResponse responseCode : Int) {
            if (responseCode == BillingResponse.OK) {
                // Enable the reward product, or make
                // any necessary updates to the UI.
            }
        }
    })
}
```

Example 4 (unknown):
```unknown
if (skuDetails.isRewarded()) {
    RewardLoadParams.Builder params = RewardLoadParams.newBuilder();
    params.setSkuDetails(skuDetails);
    mBillingClient.loadRewardedSku(params.build(),
        new RewardResponseListener() {
            @Override
            public void onRewardResponse(int responseCode) {
                if (responseCode == BillingResponse.OK) {
                      // Enable the reward product, or make
                      // any necessary updates to the UI.
                  }
            }
        });
}
```

---

## 处理 BillingResult 响应代码 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/errors

**Contents:**
- 处理 BillingResult 响应代码 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 重试策略
  - 简单重试策略
  - 指数退避算法重试策略
- 可重试的 BillingResult 响应
  - NETWORK_ERROR（错误代码 12）
    - 问题
    - 可能的解决方案
  - SERVICE_TIMEOUT（错误代码 -3）
    - 问题

当 Play 结算库调用触发操作时，该库会返回 BillingResult 响应，并将结果告知开发者。例如，如果您使用 queryProductDetailsAsync 获取用户可用的优惠，则响应代码包含 OK 代码，并提供正确的 ProductDetails 对象；或者包含其他响应，指示无法提供 ProductDetails 对象的原因。

并非所有响应代码都是错误。BillingResponseCode 参考页面详细说明了本指南中讨论的每个响应。下面列举了一些未指示错误的响应代码：

当响应代码指示出现错误时，有时是因为暂时性条件而导致的，因此可以恢复。调用 Play 结算库方法时，如果返回的 BillingResponseCode 值指示可恢复的条件，您应重试调用。在其他情况下，条件不会被视为暂时条件，因此不建议重试。

暂时性错误需要采用不同的重试策略，具体取决于特定的因素，例如错误是发生在用户会话期间（例如，当用户正在进行购买流程时），还是发生在后台（例如，当您在 onResume 期间查询用户的现有购买交易时）。下面的重试策略部分提供了这些不同策略的示例，并且可重试的 BillingResult 响应部分给出了每个响应代码最适合的策略建议。

除了响应代码之外，一些错误响应还包括用于调试和记录的消息。

当用户正在会话中时，建议实现一个简单的重试策略，以便尽可能避免错误干扰用户体验。在这种情况下，我们建议采用简单的重试策略，将尝试次数上限作为退出条件。

以下示例展示了处理在建立 BillingClient 连接时出现的错误的简单重试策略：

我们建议对在后台发生的 Play 结算库操作使用指数退避算法，该算法在用户进行会话时不影响用户体验。

例如，在确认新购买交易时可以实现此算法，因为此操作可以在后台进行，如果出现错误，则不需要实时进行确认。

此错误表示设备和 Play 系统之间的网络连接出现问题。

若要恢复，请使用简单的重试策略或指数退避算法，具体取决于哪个操作触发了错误。

此错误表示在 Google Play 能够响应之前，请求已达到超时时间上限。例如，这可能是由于延迟执行 Play 结算库调用请求的操作所致。

这通常是暂时性问题。使用简单策略或指数退避算法策略重试请求，具体取决于哪个操作返回了错误。

与下面的 SERVICE_DISCONNECTED 不同，与 Google Play 结算服务的连接未中断，您只需重试任何尝试过的 Play 结算库操作。

此严重错误表示客户端应用通过 BillingClient 与 Google Play 商店服务的连接已中断。

Play 结算库 8.0.0 版引入了 enableAutoServiceReconnection() 功能。构建 BillingClient 时，强烈建议您启用此功能。这样一来，当服务处于断开连接状态时，库便会在进行结算 API 调用时自动尝试重新建立连接，从而显著减少此类错误的发生。

Play 结算库会自动尝试重新连接。如果您在进行 API 调用时仍收到 SERVICE_DISCONNECTED 响应代码，则表示该库在自动尝试后无法重新连接。在这种情况下，您应在应用中实现重试逻辑：

为尽可能避免此错误，请务必通过调用 BillingClient.isReady() 先检查与 Google Play 服务的连接，然后再使用 Play 结算库进行调用。

如需尝试从 SERVICE_DISCONNECTED 进行恢复，您的客户端应用应尝试使用 BillingClient.startConnection 重新建立连接。

与 SERVICE_TIMEOUT 一样，请使用简单的重试策略或指数退避算法，具体取决于哪个操作触发了错误。

从 Google Play 结算库 6.0.0 开始，网络问题将不再返回 SERVICE_UNAVAILABLE。在结算服务不可用且 SERVICE_TIMEOUT 已废弃的情况下，系统才会返回此错误。

此暂时性错误表示 Google Play 结算服务目前不可用。在大多数情况下，这意味着客户端设备与 Google Play 结算服务之间的任何位置出现网络连接问题。

这通常是暂时性问题。使用简单策略或指数退避算法策略重试请求，具体取决于哪个操作返回了错误。

与 SERVICE_DISCONNECTED 不同，与 Google Play 结算服务的连接未中断，您需要重试任何正在尝试的操作。

此错误表示购买过程中发生了用户结算错误。可能出现此问题的示例包括：

在这种情况下，自动重试不太可能有帮助。但是，如果用户解决了导致问题的情况，手动重试会有所帮助。例如，如果用户将其 Play 商店版本更新为受支持的版本，则手动重试初始操作可以解决问题。

如果用户没有处于会话状态时发生此错误，那么重试可能没有意义。 如果您因购买流程收到 BILLING_UNAVAILABLE 错误，很可能是因为用户在购买过程中收到了 Google Play 的反馈，并且可能知道错误所在。在这种情况下，您可以显示一条错误消息，说明出现了问题，并提供一个“重试”按钮，以便用户在解决问题后进行手动重试。

这是一个严重错误，表示 Google Play 本身存在内部问题。

有时，导致 ERROR 的内部 Google Play 问题是暂时性的，可以通过指数退避算法进行重试来缓解此问题。如果用户在会话中，建议进行简单的重试。

此响应表明，Google Play 用户已经拥有其尝试购买的订阅或一次性购买商品。在大多数情况下，这并非暂时性错误，除非它是由过时的 Google Play 缓存导致的。

为了避免此错误不是由缓存问题引起的，请勿在用户已经拥有某个商品时向其提供此商品供购买。在展示可供购买的商品时，请务必检查用户的权限，并相应地过滤用户可以购买的商品。当客户端应用因缓存问题而收到此错误时，此错误会触发 Google Play 的缓存，以便使用来自 Play 后端的最新数据进行更新。在这种情况下，在出现错误后重试应该能解决这个特定的瞬态情况。获得 ITEM_ALREADY_OWNED 后调用 BillingClient.queryPurchasesAsync()，检查用户是否已经购买了相应商品，如果没有，请实现一个简单的重试逻辑来重新尝试购买。

此购买响应表明，Google Play 用户并不拥有用户尝试替换、确认或使用的订阅或一次性购买商品。在大多数情况下，这并非暂时性错误，除非它是由 Google Play 的缓存进入过时状态导致的。

如果由于缓存问题而收到此错误，此错误会触发 Google Play 的缓存，以便使用来自 Play 后端的最新数据进行更新。出错后，通过一个简单的重试策略重试应能解决此特定瞬态错误。获得 ITEM_NOT_OWNED 后调用 BillingClient.queryPurchasesAsync()，检查用户是否已获取相应商品。如果没有，使用简单的重试逻辑重新尝试购买。

这一不可重试的错误表示用户的设备不支持 Google Play 结算服务功能，原因可能是 Play 商店版本较旧。

例如，某些用户的设备可能不支持应用内消息。

在调用 Play 结算库之前，请使用 BillingClient.isFeatureSupported() 检查功能支持情况。

此解决方案仅供参考，可能会以一种不引起中断的方式失败。

此用户无法购买 Google Play 结算服务订阅或一次性购买商品。

请确保您的应用按照建议通过 queryProductDetailsAsync 刷新商品详情。请考虑您的商品详情在 Play 管理中心配置上发生更改的频率，以在需要时实现额外的刷新。 仅尝试在 Google Play 结算服务上销售通过 queryProductDetailsAsync 返回正确信息的商品。检查商品资格配置是否存在不一致问题。例如，您可能正在查询某个商品，该商品仅在用户尝试购买的地区之外销售。若要让商品可供购买，必须将商品的状态设为有效，同时其所属的应用必须已发布并已在用户所在的国家/地区上架。

有时，尤其是在测试期间，商品配置一切都正确无误，但用户仍会看到此错误。这可能是由于商品详情在 Google 服务器上的传播延迟所致。请稍后再试。

这是一个严重错误，表明您未正确使用 API。例如，向 BillingClient.launchBillingFlow 提供不正确的参数可能会导致此错误。

确保您正确地使用了不同的 Play 结算库调用。此外，如需详细了解此错误，请查看调试消息。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

**Examples:**

Example 1 (javascript):
```javascript
class BillingClientWrapper(context: Context) : PurchasesUpdatedListener {
  // Initialize the BillingClient.
  private val billingClient = BillingClient.newBuilder(context)
    .setListener(this)
    .enablePendingPurchases()
    .build()

  // Establish a connection to Google Play.
  fun startBillingConnection() {
    billingClient.startConnection(object : BillingClientStateListener {
      override fun onBillingSetupFinished(billingResult: BillingResult) {
        if (billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
          Log.d(TAG, "Billing response OK")
          // The BillingClient is ready. You can now query Products Purchases.
        } else {
          Log.e(TAG, billingResult.debugMessage)
          retryBillingServiceConnection()
        }
      }

      override fun onBillingServiceDisconnected() {
        Log.e(TAG, "GBPL Service disconnected")
        retryBillingServiceConnection()
      }
    })
  }

  // Billing connection retry logic. This is a simple max retry pattern
  private fun retryBillingServiceConnection() {
    val maxTries = 3
    var tries = 1
    var isConnectionEstablished = false
    do {
      try {
        billingClient.startConnection(object : BillingClientStateListener {
          override fun onBillingSetupFinished(billingResult: BillingResult) {
            if (billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
              isConnectionEstablished = true
              Log.d(TAG, "Billing connection retry succeeded.")
            } else {
              Log.e(
                TAG,
                "Billing connection retry failed: ${billingResult.debugMessage}"
              )
            }
          }
        })
      } catch (e: Exception) {
        e.message?.let { Log.e(TAG, it) }
      } finally {
        tries++
      }
    } while (tries <= maxTries && !isConnectionEstablished)
  }
  ...
}
```

Example 2 (javascript):
```javascript
class BillingClientWrapper(context: Context) : PurchasesUpdatedListener {
  // Initialize the BillingClient.
  private val billingClient = BillingClient.newBuilder(context)
    .setListener(this)
    .enablePendingPurchases()
    .build()

  // Establish a connection to Google Play.
  fun startBillingConnection() {
    billingClient.startConnection(object : BillingClientStateListener {
      override fun onBillingSetupFinished(billingResult: BillingResult) {
        if (billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
          Log.d(TAG, "Billing response OK")
          // The BillingClient is ready. You can now query Products Purchases.
        } else {
          Log.e(TAG, billingResult.debugMessage)
          retryBillingServiceConnection()
        }
      }

      override fun onBillingServiceDisconnected() {
        Log.e(TAG, "GBPL Service disconnected")
        retryBillingServiceConnection()
      }
    })
  }

  // Billing connection retry logic. This is a simple max retry pattern
  private fun retryBillingServiceConnection() {
    val maxTries = 3
    var tries = 1
    var isConnectionEstablished = false
    do {
      try {
        billingClient.startConnection(object : BillingClientStateListener {
          override fun onBillingSetupFinished(billingResult: BillingResult) {
            if (billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
              isConnectionEstablished = true
              Log.d(TAG, "Billing connection retry succeeded.")
            } else {
              Log.e(
                TAG,
                "Billing connection retry failed: ${billingResult.debugMessage}"
              )
            }
          }
        })
      } catch (e: Exception) {
        e.message?.let { Log.e(TAG, it) }
      } finally {
        tries++
      }
    } while (tries <= maxTries && !isConnectionEstablished)
  }
  ...
}
```

Example 3 (unknown):
```unknown
private fun acknowledge(purchaseToken: String): BillingResult {
  val params = AcknowledgePurchaseParams.newBuilder()
    .setPurchaseToken(purchaseToken)
    .build()
  var ackResult = BillingResult()
  billingClient.acknowledgePurchase(params) { billingResult ->
    ackResult = billingResult
  }
  return ackResult
}

suspend fun acknowledgePurchase(purchaseToken: String) {

  val retryDelayMs = 2000L
  val retryFactor = 2
  val maxTries = 3

  withContext(Dispatchers.IO) {
    acknowledge(purchaseToken)
  }

  AcknowledgePurchaseResponseListener { acknowledgePurchaseResult ->
    val playBillingResponseCode =
    PlayBillingResponseCode(acknowledgePurchaseResult.responseCode)
    when (playBillingResponseCode) {
      BillingClient.BillingResponseCode.OK -> {
        Log.i(TAG, "Acknowledgement was successful")
      }
      BillingClient.BillingResponseCode.ITEM_NOT_OWNED -> {
        // This is possibly related to a stale Play cache.
        // Querying purchases again.
        Log.d(TAG, "Acknowledgement failed with ITEM_NOT_OWNED")
        billingClient.queryPurchasesAsync(
          QueryPurchasesParams.newBuilder()
            .setProductType(BillingClient.ProductType.SUBS)
            .build()
        )
        { billingResult, purchaseList ->
          when (billingResult.responseCode) {
            BillingClient.BillingResponseCode.OK -> {
              purchaseList.forEach { purchase ->
                acknowledge(purchase.purchaseToken)
              }
            }
          }
        }
      }
      in setOf(
         BillingClient.BillingResponseCode.ERROR,
         BillingClient.BillingResponseCode.SERVICE_DISCONNECTED,
         BillingClient.BillingResponseCode.SERVICE_UNAVAILABLE,
       ) -> {
        Log.d(
          TAG,
          "Acknowledgement failed, but can be retried --
          Response Code: ${acknowledgePurchaseResult.responseCode} --
          Debug Message: ${acknowledgePurchaseResult.debugMessage}"
        )
        runBlocking {
          exponentialRetry(
            maxTries = maxTries,
            initialDelay = retryDelayMs,
            retryFactor = retryFactor
          ) { acknowledge(purchaseToken) }
        }
      }
      in setOf(
         BillingClient.BillingResponseCode.BILLING_UNAVAILABLE,
         BillingClient.BillingResponseCode.DEVELOPER_ERROR,
         BillingClient.BillingResponseCode.FEATURE_NOT_SUPPORTED,
       ) -> {
        Log.e(
          TAG,
          "Acknowledgement failed and cannot be retried --
          Response Code: ${acknowledgePurchaseResult.responseCode} --
          Debug Message: ${acknowledgePurchaseResult.debugMessage}"
        )
        throw Exception("Failed to acknowledge the purchase!")
      }
    }
  }
}

private suspend fun <T> exponentialRetry(
  maxTries: Int = Int.MAX_VALUE,
  initialDelay: Long = Long.MAX_VALUE,
  retryFactor: Int = Int.MAX_VALUE,
  block: suspend () -> T
): T? {
  var currentDelay = initialDelay
  var retryAttempt = 1
  do {
    runCatching {
      delay(currentDelay)
      block()
    }
      .onSuccess {
        Log.d(TAG, "Retry succeeded")
        return@onSuccess;
      }
      .onFailure { throwable ->
        Log.e(
          TAG,
          "Retry Failed -- Cause: ${throwable.cause} -- Message: ${throwable.message}"
        )
      }
    currentDelay *= retryFactor
    retryAttempt++
  } while (retryAttempt < maxTries)

  return block() // last attempt
}
```

Example 4 (unknown):
```unknown
private fun acknowledge(purchaseToken: String): BillingResult {
  val params = AcknowledgePurchaseParams.newBuilder()
    .setPurchaseToken(purchaseToken)
    .build()
  var ackResult = BillingResult()
  billingClient.acknowledgePurchase(params) { billingResult ->
    ackResult = billingResult
  }
  return ackResult
}

suspend fun acknowledgePurchase(purchaseToken: String) {

  val retryDelayMs = 2000L
  val retryFactor = 2
  val maxTries = 3

  withContext(Dispatchers.IO) {
    acknowledge(purchaseToken)
  }

  AcknowledgePurchaseResponseListener { acknowledgePurchaseResult ->
    val playBillingResponseCode =
    PlayBillingResponseCode(acknowledgePurchaseResult.responseCode)
    when (playBillingResponseCode) {
      BillingClient.BillingResponseCode.OK -> {
        Log.i(TAG, "Acknowledgement was successful")
      }
      BillingClient.BillingResponseCode.ITEM_NOT_OWNED -> {
        // This is possibly related to a stale Play cache.
        // Querying purchases again.
        Log.d(TAG, "Acknowledgement failed with ITEM_NOT_OWNED")
        billingClient.queryPurchasesAsync(
          QueryPurchasesParams.newBuilder()
            .setProductType(BillingClient.ProductType.SUBS)
            .build()
        )
        { billingResult, purchaseList ->
          when (billingResult.responseCode) {
            BillingClient.BillingResponseCode.OK -> {
              purchaseList.forEach { purchase ->
                acknowledge(purchase.purchaseToken)
              }
            }
          }
        }
      }
      in setOf(
         BillingClient.BillingResponseCode.ERROR,
         BillingClient.BillingResponseCode.SERVICE_DISCONNECTED,
         BillingClient.BillingResponseCode.SERVICE_UNAVAILABLE,
       ) -> {
        Log.d(
          TAG,
          "Acknowledgement failed, but can be retried --
          Response Code: ${acknowledgePurchaseResult.responseCode} --
          Debug Message: ${acknowledgePurchaseResult.debugMessage}"
        )
        runBlocking {
          exponentialRetry(
            maxTries = maxTries,
            initialDelay = retryDelayMs,
            retryFactor = retryFactor
          ) { acknowledge(purchaseToken) }
        }
      }
      in setOf(
         BillingClient.BillingResponseCode.BILLING_UNAVAILABLE,
         BillingClient.BillingResponseCode.DEVELOPER_ERROR,
         BillingClient.BillingResponseCode.FEATURE_NOT_SUPPORTED,
       ) -> {
        Log.e(
          TAG,
          "Acknowledgement failed and cannot be retried --
          Response Code: ${acknowledgePurchaseResult.responseCode} --
          Debug Message: ${acknowledgePurchaseResult.debugMessage}"
        )
        throw Exception("Failed to acknowledge the purchase!")
      }
    }
  }
}

private suspend fun <T> exponentialRetry(
  maxTries: Int = Int.MAX_VALUE,
  initialDelay: Long = Long.MAX_VALUE,
  retryFactor: Int = Int.MAX_VALUE,
  block: suspend () -> T
): T? {
  var currentDelay = initialDelay
  var retryAttempt = 1
  do {
    runCatching {
      delay(currentDelay)
      block()
    }
      .onSuccess {
        Log.d(TAG, "Retry succeeded")
        return@onSuccess;
      }
      .onFailure { throwable ->
        Log.e(
          TAG,
          "Retry Failed -- Cause: ${throwable.cause} -- Message: ${throwable.message}"
        )
      }
    currentDelay *= retryFactor
    retryAttempt++
  } while (retryAttempt < maxTries)

  return block() // last attempt
}
```

---

## 供用户自选的其他结算方式的应用内集成指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/alternative/alternative-billing-with-user-choice-in-app

**Contents:**
- 供用户自选的其他结算方式的应用内集成指南 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- Play 结算库设置
- 连接到 Google Play
  - Kotlin
  - Java
- 显示可购买的商品
- 启动用户自选结算流程
- 处理用户选择
  - 当用户选择备选结算系统时
  - Kotlin

本指南介绍了如何集成相关 API，以便在应用中提供需用户自选的其他结算方式。

向您的 Android 应用添加 Play 结算库依赖项。如需使用备选结算系统 API，您需要使用 5.2 或更高版本。如果您需要从较早版本迁移，请先按照迁移指南中的说明操作，然后再尝试实现备选结算系统。

集成流程的最初步骤与 Google Play 结算服务集成指南中所述的一些步骤相同，在初始化您的 BillingClient 时需进行一些调整：

以下示例演示了如何通过这些调整来初始化 BillingClient：

初始化 BillingClient 后，您需要按照集成指南中的说明与 Google Play 建立连接。

您可以采用集成 Google Play 结算系统的相同方式向用户显示可购买的商品。当用户看到可供购买的商品并选择购买时，请启动用户自选结算流程（如下一部分所述）。

通过调用 launchBillingFlow() 启动用户自选结算流程。这与通过集成 Google Play 结算系统来启动购买流程的方式相同：您需要提供 ProductDetails 实例和 offerToken（对应于用户想要获得的商品及服务）。如果用户选择 Google Play 结算系统，此信息将用于继续执行购买流程。

当开发者调用 launchBillingFlow() 时，Google Play 结算系统会执行以下检查：

在 BillingClient 设置期间调用 enableUserChoiceBilling

用户会看到标准的 Google Play 结算系统用户体验

在 BillingClient 设置期间未调用 enableUserChoiceBilling

用户会看到标准的 Google Play 结算系统用户体验

用户会看到标准的 Google Play 结算系统用户体验

购买流程其余部分的处理方式不尽相同，具体取决于用户选择的是 Google Play 结算系统还是一种备选结算系统。

如果用户选择备选结算系统，Google Play 会调用 UserChoiceBillingListener 来通知应用需在备选结算系统中启动购买流程。具体而言，系统会调用 userSelectedAlternativeBilling() 方法。

UserChoiceDetails 对象中提供的外部交易令牌表示用户选择进入备选结算流程时提供的签名。如后端集成指南中所述，使用此令牌可报告这一选择产生的任何交易。

UserChoiceBillingListener 应执行以下操作：

如果用户使用备选结算系统完成购买交易，您必须在 24 小时内从后端调用 Google Play Developer API 并提供 externalTransactionToken 以及其他交易详情，向 Google Play 报告此交易。如需了解详情，请参阅后端集成指南。

以下示例演示了如何实现 UserChoiceBillingListener：

如果用户选择 Google Play 结算系统，则可以继续通过 Google Play 进行购买交易。

如果开发者使用需用户自选的其他结算方式，则需要通过 Google Play 结算系统处理购买交易或使用 externalTransactionId 报告购买交易，具体取决于用户的选择。在订阅到期之前，通过用户选择流程来处理的对现有订阅的变更可通过同一结算系统实现。

本部分介绍了如何处理一些常见的订阅变更场景。

订阅方案变更（包括升级和降级流程）的处理方式应有所不同，具体取决于订阅最初是通过 Google Play 结算系统购买的，还是通过备选结算系统购买的。

依赖于现有订阅、共用相同付款方式且定期扣款时间一致的加购项将作为升级处理。对于其他加购项，用户应该能够选择要使用的结算系统。使用 launchBillingFlow() 启动新的购买体验，如启动用户自选结算流程中所述。

对于最初在用户选择后通过开发者的备选结算系统购买的订阅，请求升级或降级的用户应通过开发者的备选结算系统继续操作，无需用户再次选择。

为此，当用户请求升级或降级时，请调用 launchBillingFlow()。请使用 setOriginalExternalTransactionId 提供原始购买交易的外部交易 ID，而不是在参数中指定 SubscriptionUpdateParams 对象。采用这种方式不会显示用户选择界面，因为系统会保留原始购买交易的相关用户选择以用于升级和降级。在此使用场景中，调用 launchBillingFlow() 会为您可以从回调中检索的交易生成新的外部交易令牌。

在备选结算系统中完成升级或降级后，您需要使用通过之前针对新订阅购买交易的调用所获得的外部交易令牌来报告新交易。

同样，如果用户选择通过 Google Play 结算系统购买其当前订阅，系统应向该用户显示 Google Play 结算系统中的升级或降级流程。以下说明介绍了如何通过 Google Play 结算系统启动用于实现升级或降级的购买流程：

确定新方案所选产品/服务的 offerToken：

将正确的信息发送到 Google Play 结算系统以处理新的购买交易，包括现有订阅的购买令牌：

此购买交易会在 Google Play 结算系统中继续，您的应用会收到包含购买交易结果的 PurchasesUpdatedListener.onPurchaseUpdated 调用。如果购买交易成功，onPurchaseUpdated() 方法也会收到新的购买交易信息，而后端会收到 SUBSCRIPTION_PURCHASED 实时开发者通知。拉取新购买交易的状态时，linkedPurchaseToken 属性会关联到旧的订阅购买交易，以便您可以根据建议将其停用。

用户应该能够随时取消订阅。用户取消订阅后，使用权可能直到付费期结束才会终止。例如，如果用户在月中取消了月度订阅，可以在剩下的大约 2 周内继续使用该服务，直到其使用权限被撤消为止。在此期间，订阅在技术层面上仍处于活跃状态，因此用户可以使用该服务。

在这一活跃期内，用户决定撤消取消订阅操作的情况并不少见。在本指南中，此情况称为“恢复”。以下部分介绍了如何在备选结算系统 API 集成中处理恢复场景。

如果您有一项已取消的订阅的外部交易 ID，则无需调用 launchBillingFlow() 即可恢复该订阅，因此它不应被用于此类激活。如果用户在已取消的订阅的有效期内恢复订阅，则不会发生任何交易；如果当前周期到期后发生下次续订，您只需继续报告续订即可。这包括以下情形：用户在恢复期间会收到赠送金额或获享特殊续订价格（例如，一项旨在鼓励用户继续订阅的促销活动）。

通常，用户可以在 Google Play 结算系统中恢复订阅。对于最初通过 Google Play 结算系统购买的订阅，用户可以在订阅处于活跃状态时通过 Google Play 的重新订阅功能选择撤消之前的取消操作。在这种情况下，您会在后端收到 SUBSCRIPTION_RESTARTED 实时开发者通知，并且系统不会发放新的购买令牌，而会使用原始令牌来继续订阅。如需了解如何在 Google Play 结算系统中管理恢复订阅事宜，请参阅订阅管理指南中的恢复。

您还可以通过调用 launchBillingFlow()，从应用中触发 Google Play 结算系统中的恢复订阅流程。如需了解实现方法，请参阅订阅到期之前 - 应用内。如果用户完成了原始购买交易的用户选择流程（已取消，但仍处于活跃状态），系统会自动检测用户的选择，并显示用于恢复这些购买交易的界面。系统会提示用户通过 Google Play 确认重新购买相应订阅，但用户无需再次经历用户选择流程。在这种情况下，系统会为用户发放新的购买令牌。您的后端会收到 SUBSCRIPTION_PURCHASED 实时开发者通知，并且新购买交易状态的 linkedPurchaseToken 值会设为升级或降级情形下的状态，采用被取消的订阅之前所用的购买令牌。

如果订阅完全过期，无论是由于被取消还是未恢复且付款遭拒（账号保留期已过），如果用户想要重获使用权，必须重新订阅。

也可通过该应用来实现重新订阅，处理方法与标准订阅方式类似。用户应该能够选择要使用的结算系统。在这种情况下，系统可能会调用 launchBillingFlow()，如启动用户自选结算流程中所述。

许可测试人员应用于测试备选结算系统集成。您不会收到许可测试人员账号发起的交易的账单。如需详细了解如何配置许可测试人员，请参阅使用应用许可来测试应用内购结算功能。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-11-07。

**Examples:**

Example 1 (unknown):
```unknown
val purchasesUpdatedListener =
   PurchasesUpdatedListener { billingResult, purchases ->
       // Handle new Google Play purchase.
   }

val userChoiceBillingListener =
   UserChoiceBillingListener { userChoiceDetails ->
       // Handle alternative billing choice.
   }

val billingClient = BillingClient.newBuilder(context)
   .setListener(purchasesUpdatedListener)
   .enablePendingPurchases()
   .enableUserChoiceBilling(userChoiceBillingListener)
   .build()
```

Example 2 (unknown):
```unknown
val purchasesUpdatedListener =
   PurchasesUpdatedListener { billingResult, purchases ->
       // Handle new Google Play purchase.
   }

val userChoiceBillingListener =
   UserChoiceBillingListener { userChoiceDetails ->
       // Handle alternative billing choice.
   }

val billingClient = BillingClient.newBuilder(context)
   .setListener(purchasesUpdatedListener)
   .enablePendingPurchases()
   .enableUserChoiceBilling(userChoiceBillingListener)
   .build()
```

Example 3 (unknown):
```unknown
private PurchasesUpdatedListener purchasesUpdatedListener = new PurchasesUpdatedListener() {
    @Override
    public void onPurchasesUpdated(BillingResult billingResult, List<Purchase> purchases) {
        // Handle new Google Play purchase.
    }
};

private UserChoiceBillingListener userChoiceBillingListener = new UserChoiceBillingListener() {
    @Override
    public void userSelectedAlternativeBilling(
        UserChoiceDetails userChoiceDetails) {
        // Handle new Google Play purchase.
    }
};

private BillingClient billingClient = BillingClient.newBuilder(context)
    .setListener(purchasesUpdatedListener)
    .enablePendingPurchases()
    .enableUserChoiceBilling(userChoiceBillingListener)
    .build();
```

Example 4 (unknown):
```unknown
private PurchasesUpdatedListener purchasesUpdatedListener = new PurchasesUpdatedListener() {
    @Override
    public void onPurchasesUpdated(BillingResult billingResult, List<Purchase> purchases) {
        // Handle new Google Play purchase.
    }
};

private UserChoiceBillingListener userChoiceBillingListener = new UserChoiceBillingListener() {
    @Override
    public void userSelectedAlternativeBilling(
        UserChoiceDetails userChoiceDetails) {
        // Handle new Google Play purchase.
    }
};

private BillingClient billingClient = BillingClient.newBuilder(context)
    .setListener(purchasesUpdatedListener)
    .enablePendingPurchases()
    .enableUserChoiceBilling(userChoiceBillingListener)
    .build();
```

---

## 一次性商品 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/one-time-products

**Contents:**
- 一次性商品 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 后续课程

一次性商品（以前称为应用内商品）是指用户可以通过一次性付费（通过用户的付款方式扣款）购买的数字商品或内容。与涉及定期付款的订阅不同，一次性商品是指一次性交易，可永久或在特定的非可续期使用情形下授予对所购内容的访问权限。

消耗型商品 - 用户为了获得应用内内容而消耗的商品，可以多次购买。使用后，商品会被“消耗”，之后可以再次购买。例如游戏代币（如金币或宝石）、额外生命或强化道具。

非消耗型商品 - 这类商品购买一次就能永久使用。购买后，此类商品会与用户的账号永久关联，且无法再次购买。例如，付费升级、解锁额外的游戏关卡或应用的无广告版本。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

---

## 订阅加购服务 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/subscription-with-addons

**Contents:**
- 订阅加购服务 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 注意事项
- 与 Play 结算库集成
  - 启动购买流程
    - Java
    - 适用于购买交易中商品的规则
- 处理购买交易
- 修改包含加购项的订阅
    - Java
  - 订阅修改方案

含加购项的订阅可让您将多个订阅产品捆绑在一起，以便一起购买、结算和管理。您可以将现有产品目录订阅无缝地作为加购项提供，而无需任何预先指定或额外配置。您可以启动包含多个现有订阅产品的购买流程，并将这些产品作为加购项进行销售。

使用含附加项的订阅功能时，请考虑以下几点：

含附加服务的订阅仅支持自动续订型基础方案。

购买交易中的所有商品必须具有相同的周期性结算周期。例如，您不能拥有按年结算的订阅，但附加服务却按月结算。

如果购买了加购项，订阅中最多可以包含 50 项内容。

此功能在印度 (IN) 和韩国 (KR) 地区不可用。

本部分介绍了如何将“含附加项的订阅”功能与 Play 结算库 (PBL) 集成。本文假定您熟悉初始 PBL 集成步骤，例如向应用添加 PBL 依赖项、初始化 BillingClient 和连接到 Google Play。本部分重点介绍与含附加项的订阅相关的 PBL 集成方面。

如需为包含附加服务的订阅启动购买流程，请执行以下步骤：

使用 BillingClient.queryProductDetailsAsync 方法提取所有订阅项。

为每个商品设置 ProductDetailsParams 对象。

由 ProductDetailsParams 对象表示的商品，用于指定表示订阅商品的 ProductDetails 和选择特定订阅 base plan 或 offer 的 offerToken。

在 BillingFlowParams.Builder.setProductDetailsParamsList 方法中指定商品详情。BillingFlowParams 类用于指定购买流程的详细信息。

以下示例展示了如何针对包含多个商品的订阅购买交易启动结算流程：

处理含附加项的订阅与处理单件商品购买交易相同，如将 Google Play 结算库集成到您的应用中中所述。唯一的区别是，用户可以通过一次购买交易获得多项授权。购买包含加购项的订阅会返回多个商品，这些商品可以使用 Google Play 结算库中的 Purchase.getProducts() 进行检索，然后使用 Google Play Developer API 的 purchases.subscriptionsv2.get 中的 lineItems 列表进行检索。

对含附加服务的订阅所做的任何更改都会导致升级或降级。如需了解详情，请参阅升级或降级订阅。

如需在应用中更改或恢复包含加购项的现有订阅购买交易，您必须使用其他参数调用 launchBillingFlow API，并确保满足以下条件：

以下示例展示了在更改包含加购项的现有订阅购买交易时，如何调用 launchBillingFlow API：

下表列出了含加购项的订阅的各种修改场景，以及相应的行为。

对于包含多个商品使用权的附加服务订阅的购买交易，RTDN 中未提供 subscriptionId 字段。不过，您可以使用 Play Developer API 获取购买交易并查看关联的商品使用权。

更改包含加购项的订阅的现有订阅者的订阅价格，与更改单项订阅的订阅价格类似，如更改订阅价格中所述。不过，如本部分所述，存在一些限制和功能差异。

停用旧同类群组也会影响包含加购项的订阅购买交易。以下规则适用：

所有未完成的“用户选择接受才生效”类型的价格上调都应与新价格具有相同的续订时间。如果含加购项的订阅中的某项商品的价格上调采用“用户接受才生效”机制，但用户尚未确认，那么除非其他商品的新价格上调会导致新价格的生效续订时间与处于 OUTSTANDING 状态的现有价格上调相同，否则系统会忽略其他商品的新价格上调。用户确认价格上调后，系统会注册任何更新的价格变动。 用户只能一次性接受所有未确认的“用户选择接受才生效”类型的价格上调。

在这种情况下，在用户接受商品 A 的价格变动之前（即在商品 A 的价格变动处于 CONFIRMED 状态之前），系统不会为相应订阅购买交易注册商品 B 的价格变动，并且 SubscriptionPurchaseV2 不会返回商品 B 的价格变动详情。在用户确认商品 A 的价格变动后，商品 B 的价格变动开始。用户只有在接受商品 A 的“用户接受才生效”价格上调后，才会收到商品 B 的“用户接受才生效”价格上调。

Google Play 的电子邮件包含一份列表，其中列出了所有价格上调或下调的商品，这些价格变动会在同一天生效。

用户可以在 Play 订阅中心内取消包含加购项的整个订阅，而您只能使用 Google Play Developer API 取消包含加购项的整个订阅。

如果取消订阅购买交易，但不撤消交易，则购买交易中的所有商品都不会自动续订，但用户在相应结算周期结束之前仍可继续访问有权访问的商品。

使用 Play 管理中心为特定订单发放基于金额的退款，而无需撤消订阅访问权限。

调用 orders.refund 可全额退还用户已支付的特定订阅款项，而不会撤消用户对相应订阅的访问权限。

调用 purchases.subscriptionsv2.revoke 可立即撤消对所有订阅商品的访问权限。借助此 API，您可以：

撤消对所有商品的访问权限，并提供按比例退款。

如果使用按比例退款的方式撤消含加购项的订阅，系统会针对每个商品的最新订单按比例退款，退款金额取决于距离下次续订的剩余时间。

撤消对所有商品的访问权限，并提供全额退款。

撤消单个商品的访问权限，并全额退还该商品的款项。

如需在不撤消整个购买交易的情况下撤消含附加项的订阅中的单个订阅项，请在 RevocationContext 中设置 ItemBasedRefund 字段，然后调用 purchases.subscriptionsv2.revoke。应撤消并退款的商品的 productId 可在 ItemBasedRefund 字段中设置。

对于包含一项或多项自动续订型订阅商品的购买交易，可以设置 ItemBasedRefund 字段。

对于购买了附加服务的订阅，某些续订可能只需要延长部分商品使用权，而不会影响未来到期的商品。

无论续订涉及哪些商品，如果续订付款遭拒，整个订阅购买交易都会进入宽限期，并且账号会进入中止状态，如下面的文档中所述。

由于宽限期本身仍会授予用户使用权，因此在购买包含加购项的订阅后，如果续订付款遭拒，系统会选择所有有效商品中宽限期最短的商品，并将其宽限期和账号冻结期作为恢复期应用于此次续订。

有效商品包括在续订尝试之前购买含附加项的订阅时有效的商品，但不包括任何新添加的商品（在恢复之前不会获得授权），也不包括因移除或停用而不再有效的任何商品。

系统会应用所选最短宽限期商品的账号冻结设置。如果有多件商品的最短宽限期相同，但账号冻结期不同，则系统会应用最长的账号冻结期。

当订阅续订付款遭拒时，相应订阅购买交易将进入宽限期状态。在宽限期内，用户将继续有权访问上一个续订周期中的所有有效内容。宽限期结束后，如果付款方式仍未修正，整个订阅购买交易将进入账号保留状态。如果在宽限期内有任何其他商品的续订日期到来，那么在订阅因付款遭拒而恢复后，系统会立即尝试为这些商品收取新费用。

在订阅购买交易处于账号保留状态期间，用户将无法访问所有订阅内容，直到付款恢复为止。

如果恢复了处于账号保留状态的订阅，则订阅购买会继续保持现有状态。如果未恢复订阅，则付款遭拒的商品将过期，而其他商品的使用权限将在剩余结算周期内恢复。

某用户订阅了我的基础方案，该方案每月 1 日续订。然后，该用户在 8 月 15 日添加了附加方案，该方案每月 10 美元，并提供 7 天免费试用期。这两项商品均未设置宽限期，且账号保留期均为 30 天。

8 月 22 日，系统会向用户收取 2.90 美元（10*9/31），以按比例计算 8 月 31 日之前的费用，但用户的付款方式在此之前已过期，因此订阅在 8 月 22 日进入付款被拒状态。

如果订阅因付款被拒而进入账号保留状态，用户将无法访问包含加项的订阅中的任何内容。当订阅因付款已恢复或已取消而退出账号保留状态时，系统会将未续订的商品的剩余时间返还给用户。

在前面的示例中，订阅于 8 月 22 日进入账号保留状态。

如果用户在 9 月 1 日的续订截止日期之前（即 8 月 25 日）恢复了账号，则当天即可重新获得基础方案和加购方案的访问权限。下一个结算日期已更改为 9 月 4 日。

如果 30 天后仍未恢复账号，则订阅将于 9 月 21 日取消，用户将无法再使用加购方案，但可以继续使用我的基础方案，直到 9 月 30 日。

在此示例中，您必须获取包含附加服务的订阅中所有商品的更新后的 expiryTime，因为某些商品可能会在宽限期和账号中止期结束后恢复其使用权。

您可以使用收入报告来核对有效订阅与 Play 上的交易。每个交易订单项都有一个订单 ID。如果购买交易涉及多件商品，“收入”和“估算的销售额”报告将针对每件商品涉及的每笔交易（例如扣款、费用、税费和退款）分别显示一行。

控制台财务报告部分中显示的收入统计信息按商品细分。

订单管理反映了包含加购项的订阅购买交易，并显示了所购商品的明细列表。在订单管理中，您可以撤消、取消或全额退款给用户。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-11-06。

**Examples:**

Example 1 (unknown):
```unknown
BillingClient billingClient = …;

    // ProductDetails obtained from queryProductDetailsAsync().
    ProductDetailsParams productDetails1 = ...;
    ProductDetailsParams productDetails2 = ...;
    ArrayList productDetailsList = new ArrayList<>();
    productDetailsList.add(productDetails1);
    productDetailsList.add(productDetails2);

    BillingFlowParams billingFlowParams =
        BillingFlowParams.newBuilder()
           .setProductDetailsParamsList(productDetailsList)
           .build();
    billingClient.launchBillingFlow(billingFlowParams);
```

Example 2 (unknown):
```unknown
BillingClient billingClient = …;

int replacementMode =…;

// ProductDetails obtained from queryProductDetailsAsync().
ProductDetailsParams productDetails1 = ...;
ProductDetailsParams productDetails2 = ...;
ProductDetailsParams productDetails3 = ...;

ArrayList newProductDetailsList = new ArrayList<>();
newProductDetailsList.add(productDetails1);
newProductDetailsList.add(productDetails1);
newProductDetailsList.add(productDetails1);

BillingFlowParams billingFlowParams =
    BillingFlowParams.newBuilder()
        .setSubscriptionUpdateParams(
          SubscriptionUpdateParams.newBuilder()
              .setOldPurchaseToken(purchaseTokenOfExistingSubscription)
              // No need to set if change does not affect the base item.
             .setSubscriptionReplacementMode(replacementMode)
             .build())
        .setProductDetailsParamsList(productDetailsList)
        .build();

billingClient.launchBillingFlow(billingFlowParams);
```

---

## Google Play 结算库版本说明 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/release-notes

**Contents:**
- Google Play 结算库版本说明 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- Google Play 结算库 8.1.0 版 (2025-11-06)
  - 变更摘要
- Google Play 结算库 8.0.0 版 (2025-06-30)
  - 变更摘要
- Google Play 结算库 7.1.1 版 (2024-10-03)
  - 问题修复
- Google Play 结算库 7.1.0 版 (2024-09-19)
  - 变更摘要
- Google Play 结算库 7.0.0 版 (2024-05-14)

本文档包含 Google Play 结算库的版本说明。

8.1.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

BillingClient.queryPurchasesAsync() 方法中新增了一个参数，用于在查询订阅时包含暂停的订阅。暂停的订阅仍归因于相应用户，但处于非有效状态，原因可能是用户暂停了订阅，也可能是用户的续订付款方式遭拒。

监听器中返回的 Purchase 对象将针对任何暂停的订阅返回 isSuspended() = true。在这种情况下，您不应授予对所购订阅的访问权限，而应引导用户前往订阅中心，以便用户管理其付款方式或暂停状态，从而重新激活订阅。

BillingFlowParams.ProductDetailsParams 对象现在具有 setSubscriptionProductReplacementParams() 方法，您可以在其中指定商品级替换信息。

SubscriptionProductReplacementParams 对象具有两个 setter 方法：

SubscriptionUpdateParams setSubscriptionReplacementMode 将被弃用。您应改用 SubscriptionProductReplacementParams.setReplacementMode。

将 minSdkVersion 更新为 23。

用于获取预订详情的 ProductDetails.oneTimePurchaseOfferDetails.getPreorderDetails() API 现已可供使用。

Google Play 结算库现在支持 Kotlin 版本 2.2.0。

8.0.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

现在，您可以为一次性商品设置多个购买选项和优惠。这样，您就可以灵活地销售商品，并降低管理商品的复杂性。

改进了 queryProductDetailsAsync() 方法。

在 PBL 8.0.0 之前的版本中，queryProductDetailsAsync() 方法不会返回无法提取的商品。这可能是因为找不到相应商品，或者没有可供用户使用的优惠。在 PBL 8.0.0 中，未提取的商品会返回新的商品级状态代码，其中包含有关未提取商品的信息。请注意，ProductDetailsResponseListener.onProductDetailsResponse() 的签名发生了变化，这需要您更改应用。如需了解详情，请参阅处理结果。

借助新的 BillingClient.Builder.enableAutoServiceReconnection() 构建器形参，开发者可以选择启用自动重新连接服务功能，该功能可自动处理与 Play 结算服务的重新连接，从而简化连接管理，并消除在服务断开连接时手动调用 startConnection() 的需求。 如需了解详情，请参阅自动重新建立连接。

launchBillingFlow() 方法的子响应代码。

从 launchBillingFlow() 返回的 BillingResult 现在将包含一个子响应代码字段。此字段仅在某些情况下填充，以提供更具体的失败原因。在 PBL 8.0.0 中，如果用户资金不足以支付其尝试购买的商品的价款，系统会返回 PAYMENT_DECLINED_DUE_TO_INSUFFICIENT_FUNDS 子代码。

移除了 queryPurchaseHistory() 方法。

移除了之前标记为已废弃的 queryPurchaseHistory() 方法。如需详细了解应改用哪些替代 API，请参阅查询购买历史记录。

移除了 querySkuDetailsAsync() 方法。

移除了之前标记为已弃用的 querySkuDetailsAsync() 方法。您应改用 queryProductDetailsAsync。

移除了 BillingClient.Builder.enablePendingPurchases() 方法。

移除了之前标记为已废弃的不带参数的 enablePendingPurchases() 方法。您应改用 enablePendingPurchases(PendingPurchaseParams params)。请注意，已废弃的 enablePendingPurchases() 在功能上等同于 enablePendingPurchases(PendingPurchasesParams.newBuilder().enableOneTimeProducts().build())。

移除了采用 skuType 的重载 queryPurchasesAsync() 方法。

移除了之前标记为已废弃的 queryPurchasesAsync(String skuType, PurchasesResponseListener listener) 方法。或者，您也可以使用 queryPurchasesAsync(QueryPurchasesParams queryPurchasesParams, PurchasesResponseListener listener)。

7.1.1 版 Google Play 结算库和 Kotlin 扩展现已推出。

7.1.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

7.0.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

添加了 PendingPurchasesParams 和 BillingClient.Builder.enablePendingPurchases(PendingPurchaseParams)，以替换此版本中已废弃的 BillingClient.Builder.enablePendingPurchases()。

添加了 API，以支持订阅预付费方案的待处理交易：

移除了 BillingClient.Builder.enableAlternativeBilling()、AlternativeBillingListener 和 AlternativeChoiceDetails。

移除了 BillingFlowParams.ProrationMode、BillingFlowParams.SubscriptionUpdateParams.Builder.setReplaceProrationMode() 和 BillingFlowParams.SubscriptionUpdateParams.Builder.setReplaceSkusProrationMode()。 - 开发者应改用 BillingFlowParams.SubscriptionUpdateParams.ReplacementMode 和 BillingFlowParams.SubscriptionUpdateParams.Builder#setSubscriptionReplacementMode(int)。 - BillingFlowParams.SubscriptionUpdateParams.Builder.setReplaceProrationMode()。 - BillingFlowParams.SubscriptionUpdateParams.Builder.setReplaceSkusProrationMode()。

移除了 BillingFlowParams.SubscriptionUpdateParams.Builder#setOldSkuPurchaseToken()。 - 开发者应改用 BillingFlowParams.SubscriptionUpdateParams.Builder#setOldPurchaseToken(java.lang.String)。

BillingClient.queryPurchaseHistoryAsync() 已弃用，并将在未来的版本中移除。开发者应改用以下替代方案：

现在，如果开发者指定了空的 offerToken，BillingFlowParams.ProductDetailsParams.setOfferToken() 会抛出异常。

将 minSdkVersion 更新为 21，并将 targetSdkVersion 更新为 34。

6.2.1 版 Google Play 结算库和 Kotlin 扩展现已推出。

6.2.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

6.1.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

6.0.1 版 Google Play 结算库和 Kotlin 扩展现已推出。

更新 Play 结算库以与 Android 14 兼容。

6.0.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

添加了新的 ReplacementMode 枚举，以取代 ProrationMode。

请注意，为实现向后兼容性，ProrationMode 仍然可用。

移除了 PENDING 购买交易的订单 ID。

之前，即使购买交易仍待处理，系统一律会创建订单 ID。从 6.0.0 版开始，系统不再为待处理的购买交易创建订单 ID。当购买交易变为 PURCHASED 状态后，系统才会为这类购买交易填充订单 ID。

移除了 queryPurchases 和 launchPriceConfirmationFlow 方法。

从 Play 结算库 6.0.0 中移除了之前标记为已废弃的 queryPurchases 和 launchPriceConfirmationFlow 方法。开发者应使用 queryPurchasesAsync，而不是 queryPurchases。如需了解 launchPriceConfirmationFlow 替代方法，请参阅价格变动。

从 PBL 6.0.0 版开始，新增了网络连接错误响应代码 NETWORK_ERROR。因网络连接问题而发生错误时，系统便会返回此代码。这类网络连接错误之前报告为 SERVICE_UNAVAILABLE。

更新了 SERVICE_UNAVAILABLE 和 SERVICE_TIMEOUT。

从 PBL 6.0.0 版开始，由于处理超时而导致的错误将返回 SERVICE_UNAVAILABLE，而非当前的 SERVICE_TIMEOUT。

在早期版本的 PBL 中，此行为不会发生改变。

从 PBL 6.0.0 版开始，系统将不再返回 SERVICE_TIMEOUT。旧版 PBL 仍会返回此代码。

Play 结算库 6 版包含额外的日志记录，可让您深入了解 API 的使用情况（例如成功和失败）和服务连接问题。此信息将用于提升 Play 结算库的性能，并为修正错误提供更好的支持。

5.2.1 版 Google Play 结算库和 Kotlin 扩展现已推出。

更新 Play 结算库以与 Android 14 兼容。

5.2.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

5.1.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

5.0.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

4.1.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

4.0.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

添加了 BillingClient.queryPurchasesAsync() 以替换 BillingClient.queryPurchases()，我们将在未来的版本中移除后者。

添加了新的订阅替换模式 IMMEDIATE_AND_CHARGE_FULL_PRICE。

添加了 BillingClient.getConnectionState() 方法，用于检索 Play 结算库的连接状态。

更新了 Javadoc 和实现，用于指明可在哪个线程上调用方法以及发布哪些线程结果。

添加了 BillingFlowParams.Builder.setSubscriptionUpdateParams() 作为发起订阅更新的新方式。用于替换已移除的 BillingFlowParams#getReplaceSkusProrationMode、BillingFlowParams#getOldSkuPurchaseToken、BillingFlowParams#getOldSku、BillingFlowParams.Builder#setReplaceSkusProrationMode 和 BillingFlowParams.Builder#setOldSku。

添加了 Purchase.getQuantity() 和 PurchaseHistoryRecord.getQuantity()。

添加了 Purchase#getSkus() 和 PurchaseHistoryRecord#getSkus()。用于替换已移除的 Purchase#getSku 和 PurchaseHistoryRecord#getSku。

移除了 BillingFlowParams#getSku、BillingFlowParams#getSkuDetails 和 BillingFlowParams#getSkuType。

3.0.3 版 Google Play 结算库、Kotlin 扩展和 Unity 插件现已推出。

3.0.2 版 Google Play 结算库和 Kotlin 扩展现已推出。

3.0.1 版 Google Play 结算库和 Kotlin 扩展现已推出。

3.0.0 版 Google Play 结算库、Kotlin 扩展和 Unity 插件现已推出。

Google Play 结算库 2.2.1 版现已推出。

Google Play 结算服务 2.2.0 版提供的功能可帮助开发者确保将购买交易归因于正确的用户。这些更改消除了基于开发者载荷构建自定义解决方案的需求。在此次更新中，开发者载荷功能现已弃用并将在未来的版本中移除。如需了解更多信息（包括推荐的替代方法），请参阅开发者载荷。

除了当前的 Java 和 Kotlin 版 Google Play 结算库 2 之外，我们还发布了一个适用于 Unity 的库版本。使用 Unity 内购 API 的游戏开发者可以立即升级，以便充分利用 Google Play 结算库 2 的所有功能，并方便以后升级到 Google Play 结算库的更高版本。

如需了解详情，请参阅通过 Unity 使用 Google Play 结算服务。

2.1.0 版 Google Play 结算库和全新 Kotlin 扩展现已推出。Play 结算库 Kotlin 扩展提供符合惯例规则的 API 替代选项，具有更好的 null 安全性和协程，可供开发者在进行 Kotlin 开发时选用。如需查看代码示例，请参阅使用 Google Play 结算库。

Google Play 结算库 2.0.3 版现已推出。

Google Play 结算库 2.0.2 版现已推出。此版本包含对参考文档的更新，没有更改库功能。

Google Play 结算库 2.0.1 版现已推出。此版本包含以下变更。

Google Play 结算库 2.0 版现已推出。此版本包含以下变更。

Google Play 支持从您的应用内部（应用内）或您的应用外部（应用外）购买商品。为了确保无论用户在哪里购买您的商品，Google Play 都能提供一致的购买体验，您必须在授予用户权利后尽快确认通过 Google Play 结算库收到的所有购买交易。如果您在三天内未确认购买交易，则用户会自动收到退款，并且 Google Play 会撤消该购买交易。对于待处理的交易（2.0 版中的新功能），三天期限从购买交易变为 PURCHASED 状态时起算，而购买交易处于 PENDING 状态的时间将不算在内。

对于订阅，您必须确认包含新购买令牌的任何购买交易。这意味着，需要确认所有初始购买、方案变更和重新注册，但无需确认后续续订。要确定购买交易是否需要确认，您可以检查购买交易中的确认字段。

Purchase 对象现在包含 isAcknowledged() 方法，该方法可以指示购买交易是否已得到确认。此外，Google Play Developer API 也包含Purchases.products和Purchases.subscriptions的确认布尔值。在确认购买交易之前，请务必使用这些方法确定购买交易是否已得到确认。

此版本已移除之前废弃的 BillingFlowParams#setSku() 方法。现在，在购买流程中渲染商品之前，您必须先调用 BillingClient.querySkuDetailsAsync()，将生成的 SkuDetails 对象传递给 BillingFlowParams.Builder.setSkuDetails()。

如需查看代码示例，请参阅使用 Google Play 结算库。

Google Play 结算库 2.0 版添加了对开发者载荷（即，可附加到购买交易的任意字符串）的支持。您可以将开发者载荷参数附加到购买交易，但只有在已确认购买交易或已消耗所购商品时才能附加。这与 AIDL 中的开发者载荷不同，在 AIDL 中，可以在启动购买流程时指定载荷。因为现在可以从您的应用外部发起购买交易，所以此变更可确保您始终有机会将载荷添加到购买交易。

Purchase 对象现在包含一个 getDeveloperPayload() 方法，用于访问新库中的载荷。

当您提供折扣 SKU 时，Google Play 现在会返回 SKU 的原价，以便您向用户显示他们正在享受折扣。

SkuDetails 包含两种检索 SKU 原价的新方法：

在 Google Play 结算库 2.0 版中，您必须支持在授予权利之前需要执行其他操作的购买交易。例如，用户可能会选择使用现金在实体店购买您的应用内商品。也就是说，交易是在应用外部完成的。在这种情况下，您应仅在用户完成交易之后授予权利。

如要启用“待处理的购买交易”功能，请在初始化应用期间调用 enablePendingPurchases()。

使用 Purchase.getPurchaseState() 方法确定购买交易的状态是 PURCHASED 还是 PENDING。请注意，只有在状态为 PURCHASED 时，您才能授予权利。您应通过执行以下操作来检查 Purchase 的状态更新：

此外，Google Play Developer API 还包含 Purchases.products 的 PENDING 状态。订阅不支持待处理的交易。

此版本还引入了一个新的实时开发者通知类型，即 OneTimeProductNotification。此通知类型包含一个消息，其值为 ONE_TIME_PRODUCT_PURCHASED 或 ONE_TIME_PRODUCT_CANCELED。仅针对与延迟付款方式（例如现金）相关的购买交易发送此类通知。

在确认待处理的购买交易时，请确保只有在购买状态是 PURCHASED（而不是 PENDING）时才确认。

Google Play 结算库 2.0 版包含多项 API 变更，以支持新特性并澄清现有功能。

consumeAsync() 现在采用 ConsumeParams 对象，而非 purchaseToken。ConsumeParams 包含 purchaseToken 以及可选的开发者载荷。

先前版本的 consumeAsync() 已从此版本中移除。

为了尽量避免混淆，queryPurchaseHistoryAsync() 现在会返回 PurchaseHistoryRecord 对象，而不是 Purchase 对象。PurchaseHistoryRecord 对象与 Purchase 对象相同，只不过它仅反映由 queryPurchaseHistoryAsync() 返回的值，并且不包含 autoRenewing、orderId 和 packageName 字段。请注意，返回的数据没有任何变化 - queryPurchaseHistoryAsync() 返回的数据与以前相同。

先前返回一个 BillingResponse 整数值的 API 现在会返回一个 BillingResult 对象。BillingResult 包含 BillingResponse 整数以及可用于诊断错误的调试字符串。该调试字符串使用 en-US 语言环境，不会向最终用户显示。

Google Play 结算库 1.2.2 版现已推出。此版本包含以下变更。

Google Play 结算库 1.2.1 版现已推出。此版本包含以下变更。

Google Play 结算库 1.2 版现已推出。此版本包含以下变更。

您现在可以在 Google Play 管理中心内更改订阅的价格，并在用户进入您的应用时提示他们查看并接受新价格。

要使用此 API，请使用订阅产品的 skuDetails 创建 PriceChangeFlowParams 对象，然后调用 launchPriceChangeConfirmationFlow()。当价格变动确认流程完成时，实现 PriceChangeConfirmationListener 来处理结果，如以下代码段所示：

价格变动确认流程会显示一个包含新定价信息的对话框，要求用户接受新价格。此流程会返回 BillingClient.BillingResponse 类型的响应代码。

当升级或降级用户的订阅时，您可以使用新的按比例计费模式 DEFERRED。此模式会在下次续订时更新用户的订阅。要详细了解如何设置此按比例计费模式，请参阅设置按比例计费模式。

在 BillingFlowParams 类中，已废弃 setSku() 方法。此变更有助于优化 Google Play 结算服务流程。

在您的应用内购买结算客户端中构造新的 BillingFlowParams 实例时，我们建议您直接使用 setSkuDetails() 来处理 JSON 对象，如以下代码段所示。

在 BillingFlowParams Builder 类中，已废弃 setSku() 方法。请改用 setSkuDetails() 方法，如以下代码段所示。传入 setSkuDetails() 对象的对象来自 querySkuDetailsAsync() 方法。

Google Play 结算库 1.1 版现已推出。此版本包含以下变更。

Google Play 结算库 1.1 版包含以下行为变更。

在升级或降级用户的订阅时，ProrationMode 会提供有关按比例计费类型的更多详情。

Google Play 支持以下按比例计费模式：

开发者过去可以设置一个布尔标记来针对订阅升级请求收取按比例计算的金额。鉴于我们现已支持 ProrationMode，它包含更详细的按比例计费说明，因此不再支持此布尔标记。

结算库一律会触发 PurhcasesUpdatedListener 回调并异步返回 BillingResponse，并且 BillingResponse 的同步返回值也会被保留。

Google Play 结算库 1.0 版现已推出。此版本包含以下变更。

Google Play 结算库 1.0 版包含以下行为变更。

BillingClient.Builder 现在通过 newBuilder 模式初始化：

为购买交易或订阅启动结算流程时，launchBillingFlow() 方法会收到使用请求专用参数初始化的 BillingFlowParams 实例：

queryPurchaseHistoryAsync() 和 querySkuDetailsAsync() 方法的参数已封装到 Builder 模式中：

现在，为了方便您查看和在我们的 API 之间保持一致，结果会以结果代码和 SkuDetails 对象列表（而不是先前的封装容器类）的形式返回：

为了在我们的 API 之间保持一致，已更改 ConsumeResponseListener 接口中的 onConsumeResponse 的参数顺序：

为了在我们的 API 之间保持一致，PurchaseResult 已解除封装：

发布了开发者预览版，该版本旨在简化结算方面的开发过程，让开发者能够集中精力实现 Android 应用专用逻辑，如应用架构和导航结构。

该库包含多个便捷的类和功能，供您在将 Android 应用与 Google Play 结算服务 API 集成时使用。该库还在 Android 接口定义语言 (AIDL) 服务之上提供了一个抽象层，使开发者能够更轻松地定义应用与 Google Play 结算 API 之间的接口。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-11-06。

**Examples:**

Example 1 (unknown):
```unknown
val priceChangeFlowParams = PriceChangeFlowParams.newBuilder()
    .setSkuDetails(skuDetailsOfThePriceChangedSubscription)
    .build()

billingClient.launchPriceChangeConfirmationFlow(activity,
        priceChangeFlowParams,
        object : PriceChangeConfirmationListener() {
            override fun onPriceChangeConfirmationResult(responseCode: Int) {
                // Handle the result.
            }
        })
```

Example 2 (unknown):
```unknown
PriceChangeFlowParams priceChangeFlowParams =
        PriceChangeFlowParams.newBuilder()
    .setSkuDetails(skuDetailsOfThePriceChangedSubscription)
    .build();

billingClient.launchPriceChangeConfirmationFlow(activity,
        priceChangeFlowParams,
        new PriceChangeConfirmationListener() {
            @Override
            public void onPriceChangeConfirmationResult(int responseCode) {
                // Handle the result.
            }
        });
```

Example 3 (unknown):
```unknown
private lateinit var mBillingClient: BillingClient
private val mSkuDetailsMap = HashMap<String, SkuDetails>()

private fun querySkuDetails() {
    val skuDetailsParamsBuilder = SkuDetailsParams.newBuilder()
    mBillingClient.querySkuDetailsAsync(skuDetailsParamsBuilder.build()
    ) { responseCode, skuDetailsList ->
        if (responseCode == 0) {
            for (skuDetails in skuDetailsList) {
                mSkuDetailsMap[skuDetails.sku] = skuDetails
            }
        }
    }
}

private fun startPurchase(skuId: String) {
    val billingFlowParams = BillingFlowParams.newBuilder()
    .setSkuDetails(mSkuDetailsMap[skuId])
    .build()
}
```

Example 4 (unknown):
```unknown
private BillingClient mBillingClient;
private Map<String, SkuDetails> mSkuDetailsMap = new HashMap<>();

private void querySkuDetails() {
    SkuDetailsParams.Builder skuDetailsParamsBuilder
            = SkuDetailsParams.newBuilder();
    mBillingClient.querySkuDetailsAsync(skuDetailsParamsBuilder.build(),
            new SkuDetailsResponseListener() {
                @Override
                public void onSkuDetailsResponse(int responseCode,
                        List<SkuDetails> skuDetailsList) {
                    if (responseCode == 0) {
                        for (SkuDetails skuDetails : skuDetailsList) {
                            mSkuDetailsMap.put(skuDetails.getSku(), skuDetails);
                        }
                    }
                }
            });
}

private void startPurchase(String skuId) {
    BillingFlowParams billingFlowParams = BillingFlowParams.newBuilder()
            .setSkuDetails(mSkuDetailsMap.get(skuId))
            .build();
}
```

---

## Google Play 结算库版本说明 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/release-notes?hl=zh-cn

**Contents:**
- Google Play 结算库版本说明 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- Google Play 结算库 8.1.0 版 (2025-11-06)
  - 变更摘要
- Google Play 结算库 8.0.0 版 (2025-06-30)
  - 变更摘要
- Google Play 结算库 7.1.1 版 (2024-10-03)
  - 问题修复
- Google Play 结算库 7.1.0 版 (2024-09-19)
  - 变更摘要
- Google Play 结算库 7.0.0 版 (2024-05-14)

本文档包含 Google Play 结算库的版本说明。

8.1.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

BillingClient.queryPurchasesAsync() 方法中新增了一个参数，用于在查询订阅时包含暂停的订阅。暂停的订阅仍归因于相应用户，但处于非有效状态，原因可能是用户暂停了订阅，也可能是用户的续订付款方式遭拒。

监听器中返回的 Purchase 对象将针对任何暂停的订阅返回 isSuspended() = true。在这种情况下，您不应授予对所购订阅的访问权限，而应引导用户前往订阅中心，以便用户管理其付款方式或暂停状态，从而重新激活订阅。

BillingFlowParams.ProductDetailsParams 对象现在具有 setSubscriptionProductReplacementParams() 方法，您可以在其中指定商品级替换信息。

SubscriptionProductReplacementParams 对象具有两个 setter 方法：

SubscriptionUpdateParams setSubscriptionReplacementMode 将被弃用。您应改用 SubscriptionProductReplacementParams.setReplacementMode。

将 minSdkVersion 更新为 23。

用于获取预订详情的 ProductDetails.oneTimePurchaseOfferDetails.getPreorderDetails() API 现已可供使用。

Google Play 结算库现在支持 Kotlin 版本 2.2.0。

8.0.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

现在，您可以为一次性商品设置多个购买选项和优惠。这样，您就可以灵活地销售商品，并降低管理商品的复杂性。

改进了 queryProductDetailsAsync() 方法。

在 PBL 8.0.0 之前的版本中，queryProductDetailsAsync() 方法不会返回无法提取的商品。这可能是因为找不到相应商品，或者没有可供用户使用的优惠。在 PBL 8.0.0 中，未提取的商品会返回新的商品级状态代码，其中包含有关未提取商品的信息。请注意，ProductDetailsResponseListener.onProductDetailsResponse() 的签名发生了变化，这需要您更改应用。如需了解详情，请参阅处理结果。

借助新的 BillingClient.Builder.enableAutoServiceReconnection() 构建器形参，开发者可以选择启用自动重新连接服务功能，该功能可自动处理与 Play 结算服务的重新连接，从而简化连接管理，并消除在服务断开连接时手动调用 startConnection() 的需求。 如需了解详情，请参阅自动重新建立连接。

launchBillingFlow() 方法的子响应代码。

从 launchBillingFlow() 返回的 BillingResult 现在将包含一个子响应代码字段。此字段仅在某些情况下填充，以提供更具体的失败原因。在 PBL 8.0.0 中，如果用户资金不足以支付其尝试购买的商品的价款，系统会返回 PAYMENT_DECLINED_DUE_TO_INSUFFICIENT_FUNDS 子代码。

移除了 queryPurchaseHistory() 方法。

移除了之前标记为已废弃的 queryPurchaseHistory() 方法。如需详细了解应改用哪些替代 API，请参阅查询购买历史记录。

移除了 querySkuDetailsAsync() 方法。

移除了之前标记为已弃用的 querySkuDetailsAsync() 方法。您应改用 queryProductDetailsAsync。

移除了 BillingClient.Builder.enablePendingPurchases() 方法。

移除了之前标记为已废弃的不带参数的 enablePendingPurchases() 方法。您应改用 enablePendingPurchases(PendingPurchaseParams params)。请注意，已废弃的 enablePendingPurchases() 在功能上等同于 enablePendingPurchases(PendingPurchasesParams.newBuilder().enableOneTimeProducts().build())。

移除了采用 skuType 的重载 queryPurchasesAsync() 方法。

移除了之前标记为已废弃的 queryPurchasesAsync(String skuType, PurchasesResponseListener listener) 方法。或者，您也可以使用 queryPurchasesAsync(QueryPurchasesParams queryPurchasesParams, PurchasesResponseListener listener)。

7.1.1 版 Google Play 结算库和 Kotlin 扩展现已推出。

7.1.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

7.0.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

添加了 PendingPurchasesParams 和 BillingClient.Builder.enablePendingPurchases(PendingPurchaseParams)，以替换此版本中已废弃的 BillingClient.Builder.enablePendingPurchases()。

添加了 API，以支持订阅预付费方案的待处理交易：

移除了 BillingClient.Builder.enableAlternativeBilling()、AlternativeBillingListener 和 AlternativeChoiceDetails。

移除了 BillingFlowParams.ProrationMode、BillingFlowParams.SubscriptionUpdateParams.Builder.setReplaceProrationMode() 和 BillingFlowParams.SubscriptionUpdateParams.Builder.setReplaceSkusProrationMode()。 - 开发者应改用 BillingFlowParams.SubscriptionUpdateParams.ReplacementMode 和 BillingFlowParams.SubscriptionUpdateParams.Builder#setSubscriptionReplacementMode(int)。 - BillingFlowParams.SubscriptionUpdateParams.Builder.setReplaceProrationMode()。 - BillingFlowParams.SubscriptionUpdateParams.Builder.setReplaceSkusProrationMode()。

移除了 BillingFlowParams.SubscriptionUpdateParams.Builder#setOldSkuPurchaseToken()。 - 开发者应改用 BillingFlowParams.SubscriptionUpdateParams.Builder#setOldPurchaseToken(java.lang.String)。

BillingClient.queryPurchaseHistoryAsync() 已弃用，并将在未来的版本中移除。开发者应改用以下替代方案：

现在，如果开发者指定了空的 offerToken，BillingFlowParams.ProductDetailsParams.setOfferToken() 会抛出异常。

将 minSdkVersion 更新为 21，并将 targetSdkVersion 更新为 34。

6.2.1 版 Google Play 结算库和 Kotlin 扩展现已推出。

6.2.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

6.1.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

6.0.1 版 Google Play 结算库和 Kotlin 扩展现已推出。

更新 Play 结算库以与 Android 14 兼容。

6.0.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

添加了新的 ReplacementMode 枚举，以取代 ProrationMode。

请注意，为实现向后兼容性，ProrationMode 仍然可用。

移除了 PENDING 购买交易的订单 ID。

之前，即使购买交易仍待处理，系统一律会创建订单 ID。从 6.0.0 版开始，系统不再为待处理的购买交易创建订单 ID。当购买交易变为 PURCHASED 状态后，系统才会为这类购买交易填充订单 ID。

移除了 queryPurchases 和 launchPriceConfirmationFlow 方法。

从 Play 结算库 6.0.0 中移除了之前标记为已废弃的 queryPurchases 和 launchPriceConfirmationFlow 方法。开发者应使用 queryPurchasesAsync，而不是 queryPurchases。如需了解 launchPriceConfirmationFlow 替代方法，请参阅价格变动。

从 PBL 6.0.0 版开始，新增了网络连接错误响应代码 NETWORK_ERROR。因网络连接问题而发生错误时，系统便会返回此代码。这类网络连接错误之前报告为 SERVICE_UNAVAILABLE。

更新了 SERVICE_UNAVAILABLE 和 SERVICE_TIMEOUT。

从 PBL 6.0.0 版开始，由于处理超时而导致的错误将返回 SERVICE_UNAVAILABLE，而非当前的 SERVICE_TIMEOUT。

在早期版本的 PBL 中，此行为不会发生改变。

从 PBL 6.0.0 版开始，系统将不再返回 SERVICE_TIMEOUT。旧版 PBL 仍会返回此代码。

Play 结算库 6 版包含额外的日志记录，可让您深入了解 API 的使用情况（例如成功和失败）和服务连接问题。此信息将用于提升 Play 结算库的性能，并为修正错误提供更好的支持。

5.2.1 版 Google Play 结算库和 Kotlin 扩展现已推出。

更新 Play 结算库以与 Android 14 兼容。

5.2.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

5.1.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

5.0.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

4.1.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

4.0.0 版 Google Play 结算库和 Kotlin 扩展现已推出。

添加了 BillingClient.queryPurchasesAsync() 以替换 BillingClient.queryPurchases()，我们将在未来的版本中移除后者。

添加了新的订阅替换模式 IMMEDIATE_AND_CHARGE_FULL_PRICE。

添加了 BillingClient.getConnectionState() 方法，用于检索 Play 结算库的连接状态。

更新了 Javadoc 和实现，用于指明可在哪个线程上调用方法以及发布哪些线程结果。

添加了 BillingFlowParams.Builder.setSubscriptionUpdateParams() 作为发起订阅更新的新方式。用于替换已移除的 BillingFlowParams#getReplaceSkusProrationMode、BillingFlowParams#getOldSkuPurchaseToken、BillingFlowParams#getOldSku、BillingFlowParams.Builder#setReplaceSkusProrationMode 和 BillingFlowParams.Builder#setOldSku。

添加了 Purchase.getQuantity() 和 PurchaseHistoryRecord.getQuantity()。

添加了 Purchase#getSkus() 和 PurchaseHistoryRecord#getSkus()。用于替换已移除的 Purchase#getSku 和 PurchaseHistoryRecord#getSku。

移除了 BillingFlowParams#getSku、BillingFlowParams#getSkuDetails 和 BillingFlowParams#getSkuType。

3.0.3 版 Google Play 结算库、Kotlin 扩展和 Unity 插件现已推出。

3.0.2 版 Google Play 结算库和 Kotlin 扩展现已推出。

3.0.1 版 Google Play 结算库和 Kotlin 扩展现已推出。

3.0.0 版 Google Play 结算库、Kotlin 扩展和 Unity 插件现已推出。

Google Play 结算库 2.2.1 版现已推出。

Google Play 结算服务 2.2.0 版提供的功能可帮助开发者确保将购买交易归因于正确的用户。这些更改消除了基于开发者载荷构建自定义解决方案的需求。在此次更新中，开发者载荷功能现已弃用并将在未来的版本中移除。如需了解更多信息（包括推荐的替代方法），请参阅开发者载荷。

除了当前的 Java 和 Kotlin 版 Google Play 结算库 2 之外，我们还发布了一个适用于 Unity 的库版本。使用 Unity 内购 API 的游戏开发者可以立即升级，以便充分利用 Google Play 结算库 2 的所有功能，并方便以后升级到 Google Play 结算库的更高版本。

如需了解详情，请参阅通过 Unity 使用 Google Play 结算服务。

2.1.0 版 Google Play 结算库和全新 Kotlin 扩展现已推出。Play 结算库 Kotlin 扩展提供符合惯例规则的 API 替代选项，具有更好的 null 安全性和协程，可供开发者在进行 Kotlin 开发时选用。如需查看代码示例，请参阅使用 Google Play 结算库。

Google Play 结算库 2.0.3 版现已推出。

Google Play 结算库 2.0.2 版现已推出。此版本包含对参考文档的更新，没有更改库功能。

Google Play 结算库 2.0.1 版现已推出。此版本包含以下变更。

Google Play 结算库 2.0 版现已推出。此版本包含以下变更。

Google Play 支持从您的应用内部（应用内）或您的应用外部（应用外）购买商品。为了确保无论用户在哪里购买您的商品，Google Play 都能提供一致的购买体验，您必须在授予用户权利后尽快确认通过 Google Play 结算库收到的所有购买交易。如果您在三天内未确认购买交易，则用户会自动收到退款，并且 Google Play 会撤消该购买交易。对于待处理的交易（2.0 版中的新功能），三天期限从购买交易变为 PURCHASED 状态时起算，而购买交易处于 PENDING 状态的时间将不算在内。

对于订阅，您必须确认包含新购买令牌的任何购买交易。这意味着，需要确认所有初始购买、方案变更和重新注册，但无需确认后续续订。要确定购买交易是否需要确认，您可以检查购买交易中的确认字段。

Purchase 对象现在包含 isAcknowledged() 方法，该方法可以指示购买交易是否已得到确认。此外，Google Play Developer API 也包含Purchases.products和Purchases.subscriptions的确认布尔值。在确认购买交易之前，请务必使用这些方法确定购买交易是否已得到确认。

此版本已移除之前废弃的 BillingFlowParams#setSku() 方法。现在，在购买流程中渲染商品之前，您必须先调用 BillingClient.querySkuDetailsAsync()，将生成的 SkuDetails 对象传递给 BillingFlowParams.Builder.setSkuDetails()。

如需查看代码示例，请参阅使用 Google Play 结算库。

Google Play 结算库 2.0 版添加了对开发者载荷（即，可附加到购买交易的任意字符串）的支持。您可以将开发者载荷参数附加到购买交易，但只有在已确认购买交易或已消耗所购商品时才能附加。这与 AIDL 中的开发者载荷不同，在 AIDL 中，可以在启动购买流程时指定载荷。因为现在可以从您的应用外部发起购买交易，所以此变更可确保您始终有机会将载荷添加到购买交易。

Purchase 对象现在包含一个 getDeveloperPayload() 方法，用于访问新库中的载荷。

当您提供折扣 SKU 时，Google Play 现在会返回 SKU 的原价，以便您向用户显示他们正在享受折扣。

SkuDetails 包含两种检索 SKU 原价的新方法：

在 Google Play 结算库 2.0 版中，您必须支持在授予权利之前需要执行其他操作的购买交易。例如，用户可能会选择使用现金在实体店购买您的应用内商品。也就是说，交易是在应用外部完成的。在这种情况下，您应仅在用户完成交易之后授予权利。

如要启用“待处理的购买交易”功能，请在初始化应用期间调用 enablePendingPurchases()。

使用 Purchase.getPurchaseState() 方法确定购买交易的状态是 PURCHASED 还是 PENDING。请注意，只有在状态为 PURCHASED 时，您才能授予权利。您应通过执行以下操作来检查 Purchase 的状态更新：

此外，Google Play Developer API 还包含 Purchases.products 的 PENDING 状态。订阅不支持待处理的交易。

此版本还引入了一个新的实时开发者通知类型，即 OneTimeProductNotification。此通知类型包含一个消息，其值为 ONE_TIME_PRODUCT_PURCHASED 或 ONE_TIME_PRODUCT_CANCELED。仅针对与延迟付款方式（例如现金）相关的购买交易发送此类通知。

在确认待处理的购买交易时，请确保只有在购买状态是 PURCHASED（而不是 PENDING）时才确认。

Google Play 结算库 2.0 版包含多项 API 变更，以支持新特性并澄清现有功能。

consumeAsync() 现在采用 ConsumeParams 对象，而非 purchaseToken。ConsumeParams 包含 purchaseToken 以及可选的开发者载荷。

先前版本的 consumeAsync() 已从此版本中移除。

为了尽量避免混淆，queryPurchaseHistoryAsync() 现在会返回 PurchaseHistoryRecord 对象，而不是 Purchase 对象。PurchaseHistoryRecord 对象与 Purchase 对象相同，只不过它仅反映由 queryPurchaseHistoryAsync() 返回的值，并且不包含 autoRenewing、orderId 和 packageName 字段。请注意，返回的数据没有任何变化 - queryPurchaseHistoryAsync() 返回的数据与以前相同。

先前返回一个 BillingResponse 整数值的 API 现在会返回一个 BillingResult 对象。BillingResult 包含 BillingResponse 整数以及可用于诊断错误的调试字符串。该调试字符串使用 en-US 语言环境，不会向最终用户显示。

Google Play 结算库 1.2.2 版现已推出。此版本包含以下变更。

Google Play 结算库 1.2.1 版现已推出。此版本包含以下变更。

Google Play 结算库 1.2 版现已推出。此版本包含以下变更。

您现在可以在 Google Play 管理中心内更改订阅的价格，并在用户进入您的应用时提示他们查看并接受新价格。

要使用此 API，请使用订阅产品的 skuDetails 创建 PriceChangeFlowParams 对象，然后调用 launchPriceChangeConfirmationFlow()。当价格变动确认流程完成时，实现 PriceChangeConfirmationListener 来处理结果，如以下代码段所示：

价格变动确认流程会显示一个包含新定价信息的对话框，要求用户接受新价格。此流程会返回 BillingClient.BillingResponse 类型的响应代码。

当升级或降级用户的订阅时，您可以使用新的按比例计费模式 DEFERRED。此模式会在下次续订时更新用户的订阅。要详细了解如何设置此按比例计费模式，请参阅设置按比例计费模式。

在 BillingFlowParams 类中，已废弃 setSku() 方法。此变更有助于优化 Google Play 结算服务流程。

在您的应用内购买结算客户端中构造新的 BillingFlowParams 实例时，我们建议您直接使用 setSkuDetails() 来处理 JSON 对象，如以下代码段所示。

在 BillingFlowParams Builder 类中，已废弃 setSku() 方法。请改用 setSkuDetails() 方法，如以下代码段所示。传入 setSkuDetails() 对象的对象来自 querySkuDetailsAsync() 方法。

Google Play 结算库 1.1 版现已推出。此版本包含以下变更。

Google Play 结算库 1.1 版包含以下行为变更。

在升级或降级用户的订阅时，ProrationMode 会提供有关按比例计费类型的更多详情。

Google Play 支持以下按比例计费模式：

开发者过去可以设置一个布尔标记来针对订阅升级请求收取按比例计算的金额。鉴于我们现已支持 ProrationMode，它包含更详细的按比例计费说明，因此不再支持此布尔标记。

结算库一律会触发 PurhcasesUpdatedListener 回调并异步返回 BillingResponse，并且 BillingResponse 的同步返回值也会被保留。

Google Play 结算库 1.0 版现已推出。此版本包含以下变更。

Google Play 结算库 1.0 版包含以下行为变更。

BillingClient.Builder 现在通过 newBuilder 模式初始化：

为购买交易或订阅启动结算流程时，launchBillingFlow() 方法会收到使用请求专用参数初始化的 BillingFlowParams 实例：

queryPurchaseHistoryAsync() 和 querySkuDetailsAsync() 方法的参数已封装到 Builder 模式中：

现在，为了方便您查看和在我们的 API 之间保持一致，结果会以结果代码和 SkuDetails 对象列表（而不是先前的封装容器类）的形式返回：

为了在我们的 API 之间保持一致，已更改 ConsumeResponseListener 接口中的 onConsumeResponse 的参数顺序：

为了在我们的 API 之间保持一致，PurchaseResult 已解除封装：

发布了开发者预览版，该版本旨在简化结算方面的开发过程，让开发者能够集中精力实现 Android 应用专用逻辑，如应用架构和导航结构。

该库包含多个便捷的类和功能，供您在将 Android 应用与 Google Play 结算服务 API 集成时使用。该库还在 Android 接口定义语言 (AIDL) 服务之上提供了一个抽象层，使开发者能够更轻松地定义应用与 Google Play 结算 API 之间的接口。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-11-06。

**Examples:**

Example 1 (unknown):
```unknown
val priceChangeFlowParams = PriceChangeFlowParams.newBuilder()
    .setSkuDetails(skuDetailsOfThePriceChangedSubscription)
    .build()

billingClient.launchPriceChangeConfirmationFlow(activity,
        priceChangeFlowParams,
        object : PriceChangeConfirmationListener() {
            override fun onPriceChangeConfirmationResult(responseCode: Int) {
                // Handle the result.
            }
        })
```

Example 2 (unknown):
```unknown
PriceChangeFlowParams priceChangeFlowParams =
        PriceChangeFlowParams.newBuilder()
    .setSkuDetails(skuDetailsOfThePriceChangedSubscription)
    .build();

billingClient.launchPriceChangeConfirmationFlow(activity,
        priceChangeFlowParams,
        new PriceChangeConfirmationListener() {
            @Override
            public void onPriceChangeConfirmationResult(int responseCode) {
                // Handle the result.
            }
        });
```

Example 3 (unknown):
```unknown
private lateinit var mBillingClient: BillingClient
private val mSkuDetailsMap = HashMap<String, SkuDetails>()

private fun querySkuDetails() {
    val skuDetailsParamsBuilder = SkuDetailsParams.newBuilder()
    mBillingClient.querySkuDetailsAsync(skuDetailsParamsBuilder.build()
    ) { responseCode, skuDetailsList ->
        if (responseCode == 0) {
            for (skuDetails in skuDetailsList) {
                mSkuDetailsMap[skuDetails.sku] = skuDetails
            }
        }
    }
}

private fun startPurchase(skuId: String) {
    val billingFlowParams = BillingFlowParams.newBuilder()
    .setSkuDetails(mSkuDetailsMap[skuId])
    .build()
}
```

Example 4 (unknown):
```unknown
private BillingClient mBillingClient;
private Map<String, SkuDetails> mSkuDetailsMap = new HashMap<>();

private void querySkuDetails() {
    SkuDetailsParams.Builder skuDetailsParamsBuilder
            = SkuDetailsParams.newBuilder();
    mBillingClient.querySkuDetailsAsync(skuDetailsParamsBuilder.build(),
            new SkuDetailsResponseListener() {
                @Override
                public void onSkuDetailsResponse(int responseCode,
                        List<SkuDetails> skuDetailsList) {
                    if (responseCode == 0) {
                        for (SkuDetails skuDetails : skuDetailsList) {
                            mSkuDetailsMap.put(skuDetails.getSku(), skuDetails);
                        }
                    }
                }
            });
}

private void startPurchase(String skuId) {
    BillingFlowParams billingFlowParams = BillingFlowParams.newBuilder()
            .setSkuDetails(mSkuDetailsMap.get(skuId))
            .build();
}
```

---

## 查询交易记录 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/query-purchase-history

**Contents:**
- 查询交易记录 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 处理购买交易
- 处理作废的购买交易
- 跟踪历史购买交易

queryPurchaseHistory() 已在 Play 结算库 7 中废弃。本页介绍了针对您的应用可能依赖 queryPurchaseHistory() 的用例推荐的替代方案。

如需检索要处理的购买交易，请使用 queryPurchasesAsync(QueryPurchaseParams, PurchasesResponseListener)。

如需了解详情，请参阅集成指南的处理购买交易部分。

如需提取作废或已取消的购买交易，请使用作废的购买交易服务器开发者 API。

如果您的应用想要跟踪用户的购买交易记录，则应在应用后端跟踪该记录。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

---

## 一次性商品的多个购买选项和优惠 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/one-time-product-multi-purchase-options-offers?hl=zh-cn

**Contents:**
- 一次性商品的多个购买选项和优惠 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
  - 前提条件
  - 查询商品详情
- 启动结算流程
    - Java
- 购买选项和优惠
  - 购买选项“购买”
  - 购买选项“租借”
    - 将“租借”购买选项与 PBL 集成
    - 针对租借选项启动购买流程

本文档详细介绍了如何将一次性商品 (OTP) 与 Play 结算库集成。本文还进一步介绍了如何集成与一次性商品相关的各种购买选项和优惠。

您可以为一次性商品配置多个购买选项和优惠。例如，您可以为同一一次性商品配置购买购买选项和预订优惠。

如需为一次性商品配置多个优惠，您必须使用 queryProductDetailsAsync() API。不支持已弃用的 querySkuDetailsAsync() API。如需了解如何使用 queryProductDetailsAsync() 以及将 ProductDetailsParams 作为输入的 launchBillingFlow() 版本，请参阅迁移步骤。

如果您为一次性商品配置了多项优惠或购买选项，则 queryProductDetailsAsync() 方法返回的 ProductDetails 对象可以包含多项可供购买和/或租借的购买选项（针对每款一次性商品）。如需获取每个 ProductDetails 对象的所有符合条件的优惠的列表，请使用 getOneTimePurchaseOfferDetailsList() 方法。此列表只会返回用户有资格享受的优惠和购买选项。onProductDetailsResponse() 方法中的代码应处理返回的优惠。

如需从应用发起购买请求，请从应用的主线程调用 launchBillingFlow() 方法。此方法接受对 BillingFlowParams 对象的引用，该对象包含通过调用 queryProductDetailsAsync() 获取的相关 ProductDetails 对象。如需创建 BillingFlowParams 对象，请使用 BillingFlowParams.Builder 类。请注意，创建 BillingFlowParams 对象时，您必须设置与用户选择的优惠相对应的优惠令牌。

以下示例展示了如何针对具有多个优惠的一次性商品启动购买流程：

offerToken 可在 OneTimePurchaseOfferDetails 中找到。向用户展示优惠时，请务必使用可从 oneTimePurchaseOfferDetails.getOfferToken() 方法中获取的正确优惠令牌来配置结算流程参数。

购买选项用于定义向用户授予使用权的途径、商品价格以及供应商品的地区。单款商品可设有多个购买选项，这些选项可表示您销售商品的地点和方式。

Google Play 支持以下一次性商品的购买选项：

优惠是指您可以为一次性商品创建的定价方案。 例如，您可以为一次性商品创建折扣优惠。

Google Play 支持以下一次性商品购买优惠：

购买购买选项表示一次性商品的标准直接购买交易。它具有一个可选的 legacyCompatible 字段，用于指示相应购买选项是否可在不支持新模型的旧版 Play 结算库（版本 7 或更低版本）流程中使用。为了实现向后兼容，至少应将一个“购买”购买选项标记为“与旧版兼容”。

将购买和租借购买选项与 PBL 集成的步骤相同。如需了解如何将购买购买选项与 PBL 集成，请参阅将租赁购买选项与 PBL 集成。

借助租借购买选项，用户可以在指定的时间段内使用一次性商品。您可以指定租期及其到期时间。本文档介绍了将租借购买选项与 Play 结算库 (PBL) 集成的步骤。

本部分介绍了如何将租借购买选项与 Play 结算库 (PBL) 集成。本文假设您熟悉初始 PBL 集成步骤，例如向应用添加 PBL 依赖项、初始化 BillingClient 和连接到 Google Play。本部分重点介绍特定于租购选项的 PBL 集成方面。

如需配置可供租借的商品，您需要使用 Play Developer API 的新 monetization.onetimeproducts 服务或 Play 管理中心界面。如需使用该服务，您可以直接调用 REST API，也可以使用 Java 客户端库。

如需启动租借优惠的购买流程，请执行以下步骤：

使用 ProductDetails.oneTimePurchaseOfferDetails.getRentalDetails() 方法提取租借购买选项元数据。

如需从应用发起购买请求，请从应用的主线程调用 launchBillingFlow() 方法。此方法接受对 BillingFlowParams 对象的引用，该对象包含通过调用 queryProductDetailsAsync() 获取的相关 ProductDetails 对象。如需创建 BillingFlowParams 对象，请使用 BillingFlowParams.Builder 类。请注意，创建 BillingFlowParams 对象时，您必须设置与用户选择的优惠对应的优惠令牌。如果用户符合租购选项的条件，他们将在 queryProductDetailsAsync() 中收到包含 RentalDetails 和 offerId 的优惠。

offerToken 可在 OneTimePurchaseOfferDetails 中找到。 向用户显示优惠时，请务必使用可从 oneTimePurchaseOfferDetails.getOfferToken() 方法中获取的正确优惠令牌来配置结算流程参数。

借助预订，您可设置一次性商品以便用户在商品发布前抢先购买。用户预订您的商品即表示同意在商品发布时付款，除非用户在发布日期之前取消相应预订。在发布日期当天，系统会向买家收取费用，并且 Google Play 会通过电子邮件通知买家商品已发布。

本文档介绍了将预订购买优惠与 Play 结算库 (PBL) 集成的步骤。

本部分介绍了如何将预订优惠与 Play Billing 库 (PBL) 集成。本文假设您熟悉初始 PBL 集成步骤，例如向应用添加 PBL 依赖项、初始化 BillingClient 和连接到 Google Play。本部分重点介绍特定于预订优惠的 PBL 集成方面。

如需针对预订优惠启动购买流程，请执行以下步骤：

使用 ProductDetails.oneTimePurchaseOfferDetails.getPreorderDetails() 方法提取预订优惠元数据。以下示例展示了如何获取预订优惠元数据：

如需从应用发起购买请求，请从应用的主线程调用 launchBillingFlow() 方法。此方法接受对 BillingFlowParams 对象的引用，该对象包含通过调用 queryProductDetailsAsync() 获取的相关 ProductDetails 对象。如需创建 BillingFlowParams 对象，请使用 BillingFlowParams.Builder class。请注意，创建 BillingFlowParams 对象时，您必须设置与用户所选优惠对应的优惠令牌。如果用户符合预订优惠条件，他们将在 queryProductDetailsAsync() 方法中收到包含 PreorderDetails 和 offerId 的优惠。

offerToken 可在 OneTimePurchaseOfferDetails 中找到。 向用户显示优惠时，请务必使用可从 oneTimePurchaseOfferDetails.getOfferToken() 方法中获取的正确优惠令牌来配置结算流程参数。

您可以在一次性商品折扣优惠中配置以下 4 种不同的参数：

折扣优惠价格：指定有关原价折扣百分比或绝对价格折扣的详细信息。

国家或地区资格条件：指定一次性产品优惠在某个国家或地区的适用范围。

购买限制（可选）：用于确定用户可以兑换同一优惠的次数。如果用户超出购买限额，则不符合享受相应优惠的条件。

限时（可选）：指定优惠的有效时间段。如果超出此时间段，则无法购买相应优惠。

对于折扣优惠，您可以检索所提供的折扣百分比或绝对折扣。

以下示例展示了如何获取折扣优惠的原始全价及其折扣百分比。请注意，折扣百分比信息仅针对折扣优惠返回。

以下示例展示了如何获取折扣优惠的原始全价（以微为单位）及其绝对折扣（以微为单位）。请注意，以微为单位的绝对折扣信息仅针对折扣优惠返回。对于折扣优惠，必须指定绝对折扣或百分比折扣。

您可以使用 OneTimePurchaseOfferDetails.getValidTimeWindow() 方法获取优惠的有效时间窗口。此对象包含时间窗口的开始时间和结束时间（以毫秒为单位）。

以下示例展示了如何获取优惠的有效时间窗口：

您可以在折扣优惠一级指定数量上限，该上限仅在优惠一级适用。下面举例说明：

以下示例展示了如何获取折扣优惠级别的限量：

当用户用完某优惠可兑换的最大数量时，getOneTimePurchaseOfferDetailsList() 方法不会返回该优惠。

以下示例展示了如何获取有关特定折扣优惠的限量信息。您可以获取当前用户的最大允许数量和剩余数量。请注意，限量功能适用于消耗型和非消耗型一次性商品优惠。此功能仅在优惠级别受支持。

Google Play 会通过从您设置的最大允许数量中减去用户拥有的数量来计算剩余数量。在统计用户拥有的数量时，Google Play 会考虑已消耗的购买交易或待处理的购买交易。已取消、退款或退单的购买交易不会计入用户的自有数量。例如：

超级屏保设置的折扣优惠的最大允许数量为 1，因此用户最多可以购买一个折扣屏保。

用户购买了其中一款折扣屏保。如果用户随后尝试购买第二个折扣屏保，系统会出错，并且 PurchasesUpdatedListener 会收到 ITEM_UNAVAILABLE 响应代码。

用户要求退还最初购买的折扣屏保，并成功收到退款。用户尝试购买其中一个折扣屏保，购买交易将成功完成。

您可以选择向用户提供购买选项优惠或折扣优惠的国家/地区。Google Play 将根据 Play 国家/地区评估用户是否符合条件。为优惠配置地区性供应情况后，只有当用户位于目标国家/地区时，该优惠才会作为 getOneTimePurchaseOfferDetailsList() 的一部分返回；否则，当您调用 queryProductDetailsAsync() 时，该优惠不会包含在返回的优惠列表中。

以下示例展示了如何检索与优惠相关联的优惠标记。

您可以为商品、购买选项或折扣优惠设置优惠标签。 折扣优惠会继承其购买选项优惠的优惠标记。 同样，如果在商品级指定了优惠标记，购买选项优惠和折扣优惠都会继承商品优惠标记。

例如，“超级屏保”为屏保产品提供了两项优惠：购买选项屏保和折扣屏保。

在此示例中，购买选项优惠的 oneTimePurchaseOfferDetails.getOfferTagsList() 方法返回 SSProductTag 和 SSPurchaseOptionTag。对于折扣优惠，该方法会返回 SSProductTag、SSPurchaseOptionTag 和 SSDiscountOfferTag。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-29。

**Examples:**

Example 1 (unknown):
```unknown
// An activity reference from which the billing flow will launch.
Activity activity = ...;
ImmutableList<ProductDetailsParams> productDetailsParamsList =
    ImmutableList.of(
        ProductDetailsParams.newBuilder()
             // retrieve a value for productDetails by calling queryProductDetailsAsync()
            .setProductDetails(productDetails)
            // to get an offer token, call
            // ProductDetails.getOneTimePurchaseOfferDetailsList() for a list of offers
            // that are available to the user
            .setOfferToken(selectedOfferToken)
            .build()
    );
BillingFlowParams billingFlowParams = BillingFlowParams.newBuilder()
    .setProductDetailsParamsList(productDetailsParamsList)
    .build();
// Launch the billing flow
BillingResult billingResult = billingClient.launchBillingFlow(activity, billingFlowParams);
```

Example 2 (unknown):
```unknown
billingClient.queryProductDetailsAsync(
queryProductDetailsParams,
new ProductDetailsResponseListener() {
  public void onProductDetailsResponse(
      BillingResult billingResult, QueryProductDetailsResult productDetailsResult) {
    // check billingResult
    // …
    // process productDetailsList returned by QueryProductDetailsResult
    for (ProductDetails productDetails : productDetailsResult.getProductDetailsList()) {
      for (OneTimePurchaseOfferDetails oneTimePurchaseOfferDetails :
          productDetails.getOneTimePurchaseOfferDetailsList()) {
        // Checks if the offer is a rent purchase option.
        if (oneTimePurchaseOfferDetails.getRentalDetails() != null) {
          // process the returned RentalDetails
          OneTimePurchaseOfferDetails.RentalDetails rentalDetails =
              oneTimePurchaseOfferDetails.getRentalDetails();
          // Get rental period in ISO 8601 format.
          String rentalPeriod = rentalDetails.getRentalPeriod();
          // Get rental expiration period in ISO 8601 format, if present.
          if (rentalDetails.getRentalExpirationPeriod() != null) {
            String rentalExpirationPeriod = rentalDetails.getRentalExpirationPeriod();
          }
          // Get offer token
            String offerToken = oneTimePurchaseOfferDetails.getOfferToken();
          // Get the associated purchase option ID
          if (oneTimePurchaseOfferDetails.getPurchaseOptionId() != null) {
            String purchaseOptionId = oneTimePurchaseOfferDetails.getPurchaseOptionId();
          }
        }
      }
    }
  }
});
```

Example 3 (unknown):
```unknown
// An activity reference from which the billing flow will be launched.
val activity : Activity = ...;

val productDetailsParamsList = listOf(
    BillingFlowParams.ProductDetailsParams.newBuilder()
        // retrieve a value for productDetails by calling queryProductDetailsAsync()
        .setProductDetails(productDetails)
        // Get the offer token:
        // a. For one-time products, call ProductDetails.getOneTimePurchaseOfferDetailsList()
        // for a list of offers that are available to the user.
        // b. For subscriptions, call ProductDetails.subscriptionOfferDetails()
        // for a list of offers that are available to the user.
        .setOfferToken(selectedOfferToken)
        .build()
)

val billingFlowParams = BillingFlowParams.newBuilder()
    .setProductDetailsParamsList(productDetailsParamsList)
    .build()

// Launch the billing flow
val billingResult = billingClient.launchBillingFlow(activity, billingFlowParams)
```

Example 4 (unknown):
```unknown
// An activity reference from which the billing flow will be launched.
Activity activity = ...;

ImmutableList<ProductDetailsParams> productDetailsParamsList =
    ImmutableList.of(
        ProductDetailsParams.newBuilder()
             // retrieve a value for "productDetails" by calling queryProductDetailsAsync()
            .setProductDetails(productDetails)
            // Get the offer token:
            // a. For one-time products, call ProductDetails.getOneTimePurchaseOfferDetailsList()
            // for a list of offers that are available to the user.
            // b. For subscriptions, call ProductDetails.subscriptionOfferDetails()
            // for a list of offers that are available to the user.
            .setOfferToken(selectedOfferToken)
            .build()
    );

BillingFlowParams billingFlowParams = BillingFlowParams.newBuilder()
    .setProductDetailsParamsList(productDetailsParamsList)
    .build();

// Launch the billing flow
BillingResult billingResult = billingClient.launchBillingFlow(activity, billingFlowParams);
```

---

## 一次性商品的多个购买选项和优惠 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/one-time-product-multi-purchase-options-offers

**Contents:**
- 一次性商品的多个购买选项和优惠 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
  - 前提条件
  - 查询商品详情
- 启动结算流程
    - Java
- 购买选项和优惠
  - 购买选项“购买”
  - 购买选项“租借”
    - 将“租借”购买选项与 PBL 集成
    - 针对租借选项启动购买流程

本文档详细介绍了如何将一次性商品 (OTP) 与 Play 结算库集成。本文还进一步介绍了如何集成与一次性商品相关的各种购买选项和优惠。

您可以为一次性商品配置多个购买选项和优惠。例如，您可以为同一一次性商品配置购买购买选项和预订优惠。

如需为一次性商品配置多个优惠，您必须使用 queryProductDetailsAsync() API。不支持已弃用的 querySkuDetailsAsync() API。如需了解如何使用 queryProductDetailsAsync() 以及将 ProductDetailsParams 作为输入的 launchBillingFlow() 版本，请参阅迁移步骤。

如果您为一次性商品配置了多项优惠或购买选项，则 queryProductDetailsAsync() 方法返回的 ProductDetails 对象可以包含多项可供购买和/或租借的购买选项（针对每款一次性商品）。如需获取每个 ProductDetails 对象的所有符合条件的优惠的列表，请使用 getOneTimePurchaseOfferDetailsList() 方法。此列表只会返回用户有资格享受的优惠和购买选项。onProductDetailsResponse() 方法中的代码应处理返回的优惠。

如需从应用发起购买请求，请从应用的主线程调用 launchBillingFlow() 方法。此方法接受对 BillingFlowParams 对象的引用，该对象包含通过调用 queryProductDetailsAsync() 获取的相关 ProductDetails 对象。如需创建 BillingFlowParams 对象，请使用 BillingFlowParams.Builder 类。请注意，创建 BillingFlowParams 对象时，您必须设置与用户选择的优惠相对应的优惠令牌。

以下示例展示了如何针对具有多个优惠的一次性商品启动购买流程：

offerToken 可在 OneTimePurchaseOfferDetails 中找到。向用户展示优惠时，请务必使用可从 oneTimePurchaseOfferDetails.getOfferToken() 方法中获取的正确优惠令牌来配置结算流程参数。

购买选项用于定义向用户授予使用权的途径、商品价格以及供应商品的地区。单款商品可设有多个购买选项，这些选项可表示您销售商品的地点和方式。

Google Play 支持以下一次性商品的购买选项：

优惠是指您可以为一次性商品创建的定价方案。 例如，您可以为一次性商品创建折扣优惠。

Google Play 支持以下一次性商品购买优惠：

购买购买选项表示一次性商品的标准直接购买交易。它具有一个可选的 legacyCompatible 字段，用于指示相应购买选项是否可在不支持新模型的旧版 Play 结算库（版本 7 或更低版本）流程中使用。为了实现向后兼容，至少应将一个“购买”购买选项标记为“与旧版兼容”。

将购买和租借购买选项与 PBL 集成的步骤相同。如需了解如何将购买购买选项与 PBL 集成，请参阅将租赁购买选项与 PBL 集成。

借助租借购买选项，用户可以在指定的时间段内使用一次性商品。您可以指定租期及其到期时间。本文档介绍了将租借购买选项与 Play 结算库 (PBL) 集成的步骤。

本部分介绍了如何将租借购买选项与 Play 结算库 (PBL) 集成。本文假设您熟悉初始 PBL 集成步骤，例如向应用添加 PBL 依赖项、初始化 BillingClient 和连接到 Google Play。本部分重点介绍特定于租购选项的 PBL 集成方面。

如需配置可供租借的商品，您需要使用 Play Developer API 的新 monetization.onetimeproducts 服务或 Play 管理中心界面。如需使用该服务，您可以直接调用 REST API，也可以使用 Java 客户端库。

如需启动租借优惠的购买流程，请执行以下步骤：

使用 ProductDetails.oneTimePurchaseOfferDetails.getRentalDetails() 方法提取租借购买选项元数据。

如需从应用发起购买请求，请从应用的主线程调用 launchBillingFlow() 方法。此方法接受对 BillingFlowParams 对象的引用，该对象包含通过调用 queryProductDetailsAsync() 获取的相关 ProductDetails 对象。如需创建 BillingFlowParams 对象，请使用 BillingFlowParams.Builder 类。请注意，创建 BillingFlowParams 对象时，您必须设置与用户选择的优惠对应的优惠令牌。如果用户符合租购选项的条件，他们将在 queryProductDetailsAsync() 中收到包含 RentalDetails 和 offerId 的优惠。

offerToken 可在 OneTimePurchaseOfferDetails 中找到。 向用户显示优惠时，请务必使用可从 oneTimePurchaseOfferDetails.getOfferToken() 方法中获取的正确优惠令牌来配置结算流程参数。

借助预订，您可设置一次性商品以便用户在商品发布前抢先购买。用户预订您的商品即表示同意在商品发布时付款，除非用户在发布日期之前取消相应预订。在发布日期当天，系统会向买家收取费用，并且 Google Play 会通过电子邮件通知买家商品已发布。

本文档介绍了将预订购买优惠与 Play 结算库 (PBL) 集成的步骤。

本部分介绍了如何将预订优惠与 Play Billing 库 (PBL) 集成。本文假设您熟悉初始 PBL 集成步骤，例如向应用添加 PBL 依赖项、初始化 BillingClient 和连接到 Google Play。本部分重点介绍特定于预订优惠的 PBL 集成方面。

如需针对预订优惠启动购买流程，请执行以下步骤：

使用 ProductDetails.oneTimePurchaseOfferDetails.getPreorderDetails() 方法提取预订优惠元数据。以下示例展示了如何获取预订优惠元数据：

如需从应用发起购买请求，请从应用的主线程调用 launchBillingFlow() 方法。此方法接受对 BillingFlowParams 对象的引用，该对象包含通过调用 queryProductDetailsAsync() 获取的相关 ProductDetails 对象。如需创建 BillingFlowParams 对象，请使用 BillingFlowParams.Builder class。请注意，创建 BillingFlowParams 对象时，您必须设置与用户所选优惠对应的优惠令牌。如果用户符合预订优惠条件，他们将在 queryProductDetailsAsync() 方法中收到包含 PreorderDetails 和 offerId 的优惠。

offerToken 可在 OneTimePurchaseOfferDetails 中找到。 向用户显示优惠时，请务必使用可从 oneTimePurchaseOfferDetails.getOfferToken() 方法中获取的正确优惠令牌来配置结算流程参数。

您可以在一次性商品折扣优惠中配置以下 4 种不同的参数：

折扣优惠价格：指定有关原价折扣百分比或绝对价格折扣的详细信息。

国家或地区资格条件：指定一次性产品优惠在某个国家或地区的适用范围。

购买限制（可选）：用于确定用户可以兑换同一优惠的次数。如果用户超出购买限额，则不符合享受相应优惠的条件。

限时（可选）：指定优惠的有效时间段。如果超出此时间段，则无法购买相应优惠。

对于折扣优惠，您可以检索所提供的折扣百分比或绝对折扣。

以下示例展示了如何获取折扣优惠的原始全价及其折扣百分比。请注意，折扣百分比信息仅针对折扣优惠返回。

以下示例展示了如何获取折扣优惠的原始全价（以微为单位）及其绝对折扣（以微为单位）。请注意，以微为单位的绝对折扣信息仅针对折扣优惠返回。对于折扣优惠，必须指定绝对折扣或百分比折扣。

您可以使用 OneTimePurchaseOfferDetails.getValidTimeWindow() 方法获取优惠的有效时间窗口。此对象包含时间窗口的开始时间和结束时间（以毫秒为单位）。

以下示例展示了如何获取优惠的有效时间窗口：

您可以在折扣优惠一级指定数量上限，该上限仅在优惠一级适用。下面举例说明：

以下示例展示了如何获取折扣优惠级别的限量：

当用户用完某优惠可兑换的最大数量时，getOneTimePurchaseOfferDetailsList() 方法不会返回该优惠。

以下示例展示了如何获取有关特定折扣优惠的限量信息。您可以获取当前用户的最大允许数量和剩余数量。请注意，限量功能适用于消耗型和非消耗型一次性商品优惠。此功能仅在优惠级别受支持。

Google Play 会通过从您设置的最大允许数量中减去用户拥有的数量来计算剩余数量。在统计用户拥有的数量时，Google Play 会考虑已消耗的购买交易或待处理的购买交易。已取消、退款或退单的购买交易不会计入用户的自有数量。例如：

超级屏保设置的折扣优惠的最大允许数量为 1，因此用户最多可以购买一个折扣屏保。

用户购买了其中一款折扣屏保。如果用户随后尝试购买第二个折扣屏保，系统会出错，并且 PurchasesUpdatedListener 会收到 ITEM_UNAVAILABLE 响应代码。

用户要求退还最初购买的折扣屏保，并成功收到退款。用户尝试购买其中一个折扣屏保，购买交易将成功完成。

您可以选择向用户提供购买选项优惠或折扣优惠的国家/地区。Google Play 将根据 Play 国家/地区评估用户是否符合条件。为优惠配置地区性供应情况后，只有当用户位于目标国家/地区时，该优惠才会作为 getOneTimePurchaseOfferDetailsList() 的一部分返回；否则，当您调用 queryProductDetailsAsync() 时，该优惠不会包含在返回的优惠列表中。

以下示例展示了如何检索与优惠相关联的优惠标记。

您可以为商品、购买选项或折扣优惠设置优惠标签。 折扣优惠会继承其购买选项优惠的优惠标记。 同样，如果在商品级指定了优惠标记，购买选项优惠和折扣优惠都会继承商品优惠标记。

例如，“超级屏保”为屏保产品提供了两项优惠：购买选项屏保和折扣屏保。

在此示例中，购买选项优惠的 oneTimePurchaseOfferDetails.getOfferTagsList() 方法返回 SSProductTag 和 SSPurchaseOptionTag。对于折扣优惠，该方法会返回 SSProductTag、SSPurchaseOptionTag 和 SSDiscountOfferTag。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-29。

**Examples:**

Example 1 (unknown):
```unknown
// An activity reference from which the billing flow will launch.
Activity activity = ...;
ImmutableList<ProductDetailsParams> productDetailsParamsList =
    ImmutableList.of(
        ProductDetailsParams.newBuilder()
             // retrieve a value for productDetails by calling queryProductDetailsAsync()
            .setProductDetails(productDetails)
            // to get an offer token, call
            // ProductDetails.getOneTimePurchaseOfferDetailsList() for a list of offers
            // that are available to the user
            .setOfferToken(selectedOfferToken)
            .build()
    );
BillingFlowParams billingFlowParams = BillingFlowParams.newBuilder()
    .setProductDetailsParamsList(productDetailsParamsList)
    .build();
// Launch the billing flow
BillingResult billingResult = billingClient.launchBillingFlow(activity, billingFlowParams);
```

Example 2 (unknown):
```unknown
billingClient.queryProductDetailsAsync(
queryProductDetailsParams,
new ProductDetailsResponseListener() {
  public void onProductDetailsResponse(
      BillingResult billingResult, QueryProductDetailsResult productDetailsResult) {
    // check billingResult
    // …
    // process productDetailsList returned by QueryProductDetailsResult
    for (ProductDetails productDetails : productDetailsResult.getProductDetailsList()) {
      for (OneTimePurchaseOfferDetails oneTimePurchaseOfferDetails :
          productDetails.getOneTimePurchaseOfferDetailsList()) {
        // Checks if the offer is a rent purchase option.
        if (oneTimePurchaseOfferDetails.getRentalDetails() != null) {
          // process the returned RentalDetails
          OneTimePurchaseOfferDetails.RentalDetails rentalDetails =
              oneTimePurchaseOfferDetails.getRentalDetails();
          // Get rental period in ISO 8601 format.
          String rentalPeriod = rentalDetails.getRentalPeriod();
          // Get rental expiration period in ISO 8601 format, if present.
          if (rentalDetails.getRentalExpirationPeriod() != null) {
            String rentalExpirationPeriod = rentalDetails.getRentalExpirationPeriod();
          }
          // Get offer token
            String offerToken = oneTimePurchaseOfferDetails.getOfferToken();
          // Get the associated purchase option ID
          if (oneTimePurchaseOfferDetails.getPurchaseOptionId() != null) {
            String purchaseOptionId = oneTimePurchaseOfferDetails.getPurchaseOptionId();
          }
        }
      }
    }
  }
});
```

Example 3 (unknown):
```unknown
// An activity reference from which the billing flow will be launched.
val activity : Activity = ...;

val productDetailsParamsList = listOf(
    BillingFlowParams.ProductDetailsParams.newBuilder()
        // retrieve a value for productDetails by calling queryProductDetailsAsync()
        .setProductDetails(productDetails)
        // Get the offer token:
        // a. For one-time products, call ProductDetails.getOneTimePurchaseOfferDetailsList()
        // for a list of offers that are available to the user.
        // b. For subscriptions, call ProductDetails.subscriptionOfferDetails()
        // for a list of offers that are available to the user.
        .setOfferToken(selectedOfferToken)
        .build()
)

val billingFlowParams = BillingFlowParams.newBuilder()
    .setProductDetailsParamsList(productDetailsParamsList)
    .build()

// Launch the billing flow
val billingResult = billingClient.launchBillingFlow(activity, billingFlowParams)
```

Example 4 (unknown):
```unknown
// An activity reference from which the billing flow will be launched.
Activity activity = ...;

ImmutableList<ProductDetailsParams> productDetailsParamsList =
    ImmutableList.of(
        ProductDetailsParams.newBuilder()
             // retrieve a value for "productDetails" by calling queryProductDetailsAsync()
            .setProductDetails(productDetails)
            // Get the offer token:
            // a. For one-time products, call ProductDetails.getOneTimePurchaseOfferDetailsList()
            // for a list of offers that are available to the user.
            // b. For subscriptions, call ProductDetails.subscriptionOfferDetails()
            // for a list of offers that are available to the user.
            .setOfferToken(selectedOfferToken)
            .build()
    );

BillingFlowParams billingFlowParams = BillingFlowParams.newBuilder()
    .setProductDetailsParamsList(productDetailsParamsList)
    .build();

// Launch the billing flow
BillingResult billingResult = billingClient.launchBillingFlow(activity, billingFlowParams);
```

---

## 一次性商品的多商品 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/multi-product-for-one-time-product

**Contents:**
- 一次性商品的多商品 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 注意事项
- 与 Play 结算库集成
  - 启动购买流程
    - Java
    - Java
- 处理购买交易
- 实时开发者通知
- 退款
- 财务报告和对账

本文档介绍了如何将应用与 Play 结算库 (PBL) 的多商品功能集成。

借助一次性商品 (OTP) 的多商品功能，您可以将多个一次性商品组合成一个单元。然后，您可以统一购买、结算和管理这些捆绑产品。您还可以为这些捆绑式 OTP 创建折扣优惠，以激励用户购买商品。

本部分假定您熟悉 PBL 的初始集成步骤，例如向应用添加 PBL 依赖项、初始化 BillingClient 和连接到 Google Play。本部分重点介绍特定于多产品 OTP 购买交易的 PBL 集成方面。

如需针对多商品一次性商品启动购买流程，请执行以下步骤：

使用 QueryProductDetailsParams.Builder.setProductList 方法创建包含所有一次性商品的商品列表。

使用 BillingClient.queryProductDetailsAsync 方法提取所有一次性商品。

为每件一次性商品设置 ProductDetails 对象。

在 BillingFlowParams.Builder.setProductDetailsParamsList 方法中指定一次性商品详情。BillingFlowParams 类用于指定购买流程的详细信息。

以下示例展示了如何针对多商品一次性购买交易启动结算流程：

处理多商品一次性购买交易与处理现有单商品购买交易的方式相同，如将 Google Play 结算库集成到您的应用中中所述。唯一的区别在于，对于多商品一次性购买交易，您需要授予所有商品的授权，而不是仅授予一个商品的授权，这样用户才能通过一次购买交易获得多项授权。多商品一次性购买交易会返回多个商品，您可以使用 Google Play 结算库中的 Purchase.getProducts() 检索这些商品，然后检索 Google Play Developer API 的 purchases.products.get 中的 lineItems 列表。

对于多商品 OTP 购买交易，RTDN 中未提供 sku 字段。 多产品 OTP 购买交易表示购买了多种产品。因此，您可以使用 Play Developer API 获取购买数据，并查看其中的所有商品。

在多商品一次性付款购买交易中，用户无法针对单件商品申请退款，您也无法针对单件商品办理退款。不过，允许针对整个多产品 OTP 购买交易申请和发放退款。如果您要为用户取消多商品 OTP 购买交易，则与该购买交易关联的所有授权都会被取消。

您可以使用收入报告来核对 Google Payoffs 和 Play 上的交易与您当前有效的多产品一次性付款购买交易。每个交易订单项都有一个订单 ID。对于多商品 OTP 购买交易，“收入”和“估计销售额”报告将包含单独的行（具有相同的订单 ID），用于显示每笔交易（例如费用、税费和退款）以及所涉及的每件商品的费用。

管理中心的财务报告部分中显示的收入统计信息按各个产品细分。

订单管理功能可反映多商品一次性付款购买交易，并显示所购商品的明细列表。在订单管理中，您可以撤消、取消或全额退款给用户。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

**Examples:**

Example 1 (unknown):
```unknown
billingClient.queryProductDetailsAsync(
queryProductDetailsParams,
new ProductDetailsResponseListener() {
  public void onProductDetailsResponse(
      BillingResult billingResult, QueryProductDetailsResult productDetailsResult) {
    // check billingResult
    // …
    // process productDetailsList returned by QueryProductDetailsResult
    ImmutableList productDetailsList = productDetailsResult.getProductDetailsList();
    for (ProductDetails productDetails : productDetailsList) {
      for (OneTimePurchaseOfferDetails oneTimePurchaseOfferDetails :
          productDetails.getOneTimePurchaseOfferDetailsList()) {
             // …
      }
    }
  }
});
```

Example 2 (unknown):
```unknown
BillingClient billingClient =
   BillingClient.newBuilder()
    // set other options
    .build();
// ProductDetails obtained from queryProductDetailsAsync().
ProductDetails productDetails1 = ...;
ProductDetails productDetails2 = ...;
ArrayList productDetailsList = new ArrayList<>();
productDetailsList.add(productDetails1);
productDetailsList.add(productDetails2);
BillingFlowParams billingFlowParams =
BillingFlowParams.newBuilder()
    .setProductDetailsParamsList(productDetailsList)
    .build();
billingClient.launchBillingFlow(billingFlowParams);
```

---

## 查询交易记录 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/query-purchase-history?hl=zh-cn

**Contents:**
- 查询交易记录 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 处理购买交易
- 处理作废的购买交易
- 跟踪历史购买交易

queryPurchaseHistory() 已在 Play 结算库 7 中废弃。本页介绍了针对您的应用可能依赖 queryPurchaseHistory() 的用例推荐的替代方案。

如需检索要处理的购买交易，请使用 queryPurchasesAsync(QueryPurchaseParams, PurchasesResponseListener)。

如需了解详情，请参阅集成指南的处理购买交易部分。

如需提取作废或已取消的购买交易，请使用作废的购买交易服务器开发者 API。

如果您的应用想要跟踪用户的购买交易记录，则应在应用后端跟踪该记录。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-10-17。

---

## 订阅加购服务 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/subscription-with-addons?hl=zh-cn

**Contents:**
- 订阅加购服务 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 注意事项
- 与 Play 结算库集成
  - 启动购买流程
    - Java
    - 适用于购买交易中商品的规则
- 处理购买交易
- 修改包含加购项的订阅
    - Java
  - 订阅修改方案

含加购项的订阅可让您将多个订阅产品捆绑在一起，以便一起购买、结算和管理。您可以将现有产品目录订阅无缝地作为加购项提供，而无需任何预先指定或额外配置。您可以启动包含多个现有订阅产品的购买流程，并将这些产品作为加购项进行销售。

使用含附加项的订阅功能时，请考虑以下几点：

含附加服务的订阅仅支持自动续订型基础方案。

购买交易中的所有商品必须具有相同的周期性结算周期。例如，您不能拥有按年结算的订阅，但附加服务却按月结算。

如果购买了加购项，订阅中最多可以包含 50 项内容。

此功能在印度 (IN) 和韩国 (KR) 地区不可用。

本部分介绍了如何将“含附加项的订阅”功能与 Play 结算库 (PBL) 集成。本文假定您熟悉初始 PBL 集成步骤，例如向应用添加 PBL 依赖项、初始化 BillingClient 和连接到 Google Play。本部分重点介绍与含附加项的订阅相关的 PBL 集成方面。

如需为包含附加服务的订阅启动购买流程，请执行以下步骤：

使用 BillingClient.queryProductDetailsAsync 方法提取所有订阅项。

为每个商品设置 ProductDetailsParams 对象。

由 ProductDetailsParams 对象表示的商品，用于指定表示订阅商品的 ProductDetails 和选择特定订阅 base plan 或 offer 的 offerToken。

在 BillingFlowParams.Builder.setProductDetailsParamsList 方法中指定商品详情。BillingFlowParams 类用于指定购买流程的详细信息。

以下示例展示了如何针对包含多个商品的订阅购买交易启动结算流程：

处理含附加项的订阅与处理单件商品购买交易相同，如将 Google Play 结算库集成到您的应用中中所述。唯一的区别是，用户可以通过一次购买交易获得多项授权。购买包含加购项的订阅会返回多个商品，这些商品可以使用 Google Play 结算库中的 Purchase.getProducts() 进行检索，然后使用 Google Play Developer API 的 purchases.subscriptionsv2.get 中的 lineItems 列表进行检索。

对含附加服务的订阅所做的任何更改都会导致升级或降级。如需了解详情，请参阅升级或降级订阅。

如需在应用中更改或恢复包含加购项的现有订阅购买交易，您必须使用其他参数调用 launchBillingFlow API，并确保满足以下条件：

以下示例展示了在更改包含加购项的现有订阅购买交易时，如何调用 launchBillingFlow API：

下表列出了含加购项的订阅的各种修改场景，以及相应的行为。

对于包含多个商品使用权的附加服务订阅的购买交易，RTDN 中未提供 subscriptionId 字段。不过，您可以使用 Play Developer API 获取购买交易并查看关联的商品使用权。

更改包含加购项的订阅的现有订阅者的订阅价格，与更改单项订阅的订阅价格类似，如更改订阅价格中所述。不过，如本部分所述，存在一些限制和功能差异。

停用旧同类群组也会影响包含加购项的订阅购买交易。以下规则适用：

所有未完成的“用户选择接受才生效”类型的价格上调都应与新价格具有相同的续订时间。如果含加购项的订阅中的某项商品的价格上调采用“用户接受才生效”机制，但用户尚未确认，那么除非其他商品的新价格上调会导致新价格的生效续订时间与处于 OUTSTANDING 状态的现有价格上调相同，否则系统会忽略其他商品的新价格上调。用户确认价格上调后，系统会注册任何更新的价格变动。 用户只能一次性接受所有未确认的“用户选择接受才生效”类型的价格上调。

在这种情况下，在用户接受商品 A 的价格变动之前（即在商品 A 的价格变动处于 CONFIRMED 状态之前），系统不会为相应订阅购买交易注册商品 B 的价格变动，并且 SubscriptionPurchaseV2 不会返回商品 B 的价格变动详情。在用户确认商品 A 的价格变动后，商品 B 的价格变动开始。用户只有在接受商品 A 的“用户接受才生效”价格上调后，才会收到商品 B 的“用户接受才生效”价格上调。

Google Play 的电子邮件包含一份列表，其中列出了所有价格上调或下调的商品，这些价格变动会在同一天生效。

用户可以在 Play 订阅中心内取消包含加购项的整个订阅，而您只能使用 Google Play Developer API 取消包含加购项的整个订阅。

如果取消订阅购买交易，但不撤消交易，则购买交易中的所有商品都不会自动续订，但用户在相应结算周期结束之前仍可继续访问有权访问的商品。

使用 Play 管理中心为特定订单发放基于金额的退款，而无需撤消订阅访问权限。

调用 orders.refund 可全额退还用户已支付的特定订阅款项，而不会撤消用户对相应订阅的访问权限。

调用 purchases.subscriptionsv2.revoke 可立即撤消对所有订阅商品的访问权限。借助此 API，您可以：

撤消对所有商品的访问权限，并提供按比例退款。

如果使用按比例退款的方式撤消含加购项的订阅，系统会针对每个商品的最新订单按比例退款，退款金额取决于距离下次续订的剩余时间。

撤消对所有商品的访问权限，并提供全额退款。

撤消单个商品的访问权限，并全额退还该商品的款项。

如需在不撤消整个购买交易的情况下撤消含附加项的订阅中的单个订阅项，请在 RevocationContext 中设置 ItemBasedRefund 字段，然后调用 purchases.subscriptionsv2.revoke。应撤消并退款的商品的 productId 可在 ItemBasedRefund 字段中设置。

对于包含一项或多项自动续订型订阅商品的购买交易，可以设置 ItemBasedRefund 字段。

对于购买了附加服务的订阅，某些续订可能只需要延长部分商品使用权，而不会影响未来到期的商品。

无论续订涉及哪些商品，如果续订付款遭拒，整个订阅购买交易都会进入宽限期，并且账号会进入中止状态，如下面的文档中所述。

由于宽限期本身仍会授予用户使用权，因此在购买包含加购项的订阅后，如果续订付款遭拒，系统会选择所有有效商品中宽限期最短的商品，并将其宽限期和账号冻结期作为恢复期应用于此次续订。

有效商品包括在续订尝试之前购买含附加项的订阅时有效的商品，但不包括任何新添加的商品（在恢复之前不会获得授权），也不包括因移除或停用而不再有效的任何商品。

系统会应用所选最短宽限期商品的账号冻结设置。如果有多件商品的最短宽限期相同，但账号冻结期不同，则系统会应用最长的账号冻结期。

当订阅续订付款遭拒时，相应订阅购买交易将进入宽限期状态。在宽限期内，用户将继续有权访问上一个续订周期中的所有有效内容。宽限期结束后，如果付款方式仍未修正，整个订阅购买交易将进入账号保留状态。如果在宽限期内有任何其他商品的续订日期到来，那么在订阅因付款遭拒而恢复后，系统会立即尝试为这些商品收取新费用。

在订阅购买交易处于账号保留状态期间，用户将无法访问所有订阅内容，直到付款恢复为止。

如果恢复了处于账号保留状态的订阅，则订阅购买会继续保持现有状态。如果未恢复订阅，则付款遭拒的商品将过期，而其他商品的使用权限将在剩余结算周期内恢复。

某用户订阅了我的基础方案，该方案每月 1 日续订。然后，该用户在 8 月 15 日添加了附加方案，该方案每月 10 美元，并提供 7 天免费试用期。这两项商品均未设置宽限期，且账号保留期均为 30 天。

8 月 22 日，系统会向用户收取 2.90 美元（10*9/31），以按比例计算 8 月 31 日之前的费用，但用户的付款方式在此之前已过期，因此订阅在 8 月 22 日进入付款被拒状态。

如果订阅因付款被拒而进入账号保留状态，用户将无法访问包含加项的订阅中的任何内容。当订阅因付款已恢复或已取消而退出账号保留状态时，系统会将未续订的商品的剩余时间返还给用户。

在前面的示例中，订阅于 8 月 22 日进入账号保留状态。

如果用户在 9 月 1 日的续订截止日期之前（即 8 月 25 日）恢复了账号，则当天即可重新获得基础方案和加购方案的访问权限。下一个结算日期已更改为 9 月 4 日。

如果 30 天后仍未恢复账号，则订阅将于 9 月 21 日取消，用户将无法再使用加购方案，但可以继续使用我的基础方案，直到 9 月 30 日。

在此示例中，您必须获取包含附加服务的订阅中所有商品的更新后的 expiryTime，因为某些商品可能会在宽限期和账号中止期结束后恢复其使用权。

您可以使用收入报告来核对有效订阅与 Play 上的交易。每个交易订单项都有一个订单 ID。如果购买交易涉及多件商品，“收入”和“估算的销售额”报告将针对每件商品涉及的每笔交易（例如扣款、费用、税费和退款）分别显示一行。

控制台财务报告部分中显示的收入统计信息按商品细分。

订单管理反映了包含加购项的订阅购买交易，并显示了所购商品的明细列表。在订单管理中，您可以撤消、取消或全额退款给用户。

本页面上的内容和代码示例受内容许可部分所述许可的限制。Java 和 OpenJDK 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-11-06。

**Examples:**

Example 1 (unknown):
```unknown
BillingClient billingClient = …;

    // ProductDetails obtained from queryProductDetailsAsync().
    ProductDetailsParams productDetails1 = ...;
    ProductDetailsParams productDetails2 = ...;
    ArrayList productDetailsList = new ArrayList<>();
    productDetailsList.add(productDetails1);
    productDetailsList.add(productDetails2);

    BillingFlowParams billingFlowParams =
        BillingFlowParams.newBuilder()
           .setProductDetailsParamsList(productDetailsList)
           .build();
    billingClient.launchBillingFlow(billingFlowParams);
```

Example 2 (unknown):
```unknown
BillingClient billingClient = …;

int replacementMode =…;

// ProductDetails obtained from queryProductDetailsAsync().
ProductDetailsParams productDetails1 = ...;
ProductDetailsParams productDetails2 = ...;
ProductDetailsParams productDetails3 = ...;

ArrayList newProductDetailsList = new ArrayList<>();
newProductDetailsList.add(productDetails1);
newProductDetailsList.add(productDetails1);
newProductDetailsList.add(productDetails1);

BillingFlowParams billingFlowParams =
    BillingFlowParams.newBuilder()
        .setSubscriptionUpdateParams(
          SubscriptionUpdateParams.newBuilder()
              .setOldPurchaseToken(purchaseTokenOfExistingSubscription)
              // No need to set if change does not affect the base item.
             .setSubscriptionReplacementMode(replacementMode)
             .build())
        .setProductDetailsParamsList(productDetailsList)
        .build();

billingClient.launchBillingFlow(billingFlowParams);
```

---
