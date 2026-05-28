# Google-Play-Billing - Getting Started

**Pages:** 5

---

## 做好准备 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/getting-ready

**Contents:**
- 做好准备 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 设置 Google Play 开发者账号
- 在 Google Play 管理中心内启用结算相关功能
  - 添加库依赖项
  - Groovy
  - Kotlin
  - Groovy
  - Kotlin
  - 上传应用
- 创建和配置您的商品

本主题列出并说明了在您的应用中销售商品之前需要执行的设置步骤。大体上讲，此设置包括创建开发者账号、创建和配置要销售的商品，以及启用和配置用于销售和管理商品的 API。此外，本主题还介绍了如何配置实时开发者通知，以便在商品的状态发生变化时随时收到通知。

如需在 Google Play 上发布您的应用和游戏，请使用 Google Play 管理中心。您还可以使用 Google Play 管理中心管理与结算相关的商品和设置。

如需访问 Google Play 管理中心，您需要设置 Google Play 开发者账号。

如需在 Google Play 上销售付费应用和应用内购商品，您还必须在 Google 付款中心设置付款资料，然后将该付款资料与您的 Google Play 开发者账号相关联。如需了解如何将您的付款资料与账号相关联，或者了解如何检查您是否已有关联的账号和付款资料，请参阅将 Google Play 开发者账号与您的付款资料相关联。

设置开发者账号后，您必须发布包含 Google Play 结算库的应用版本。如需在 Google Play 管理中心启用结算相关功能（如配置您要销售的商品），必须执行此步骤。

如需集成 Google Play 结算系统，请先在您的应用中添加对 Google Play 结算库的依赖项。此库可让您访问用于连接到 Google Play 的 Android API。这样，您便可以访问购买信息、查询有关购买交易的更新、提示用户进行新的购买交易，等等。

Google 的 Maven 代码库中提供了 Google Play 结算库。将依赖项添加到应用的 build.gradle 文件中，如下所示：

如果您使用的是 Kotlin，Play 结算库 KTX 模块包含了 Kotlin 扩展程序和协程支持，可让您在使用 Google Play 结算系统时编写惯用的 Kotlin 代码。如需将这些扩展程序包含在项目中，请将以下依赖项添加到应用的 build.gradle 文件中，如下所示：

本页中的 Kotlin 代码示例尽可能使用了 KTX。

将该库添加到您的应用后，构建并发布您的应用。在此步骤中，创建您的应用，然后将其发布到任何轨道，包括内部测试轨道。

为您的应用启用 Google Play 结算服务功能后，您需要配置要销售的商品。

创建一次性商品和订阅的步骤相似。对于每个商品，您需要提供唯一的商品 ID、商品名、说明和定价信息。订阅具有其他必需的信息，例如选择基础方案是自动续订类型还是预付费续订类型。

Google Play 管理中心提供了一个可用于管理商品的网页界面。

如需创建和配置一次性商品，请参阅创建受管理的商品。 请注意，Google Play 管理中心将一次性商品称为“受管理的商品”。

作为网页界面的替代方案，您还可以使用 Google Play Developer API 中的 inappproducts REST 资源（对于应用内商品）和 monetization.subscriptions REST 资源（对于订阅商品）来管理商品。

Google Play Developer API 是一种服务器到服务器 API，与 Android 平台上的 Google Play 结算库相辅相成。此 API 提供了 Google Play 结算库中未提供的功能，如安全地验证购买交易以及为用户办理退款。

在将 Google Play 结算系统集成到应用的过程中，您必须通过 Google Play 管理中心来配置对 Google Play Developer API 的访问权限。有关说明，请参阅 Google Play Developer API 使用入门。

配置对 Google Play Developer API 的访问权限后，请确保您已授予查看财务数据权限，需要具备此权限才能访问与结算相关的功能。如需了解最佳做法以及有关配置权限的详细信息，请参阅添加开发者账号用户并管理权限。

借助实时开发者通知 (RTDN) 机制，每当用户的权限在您的应用中发生变化时，您都会收到来自 Google 的通知。RTDN 利用 Google Cloud Pub/Sub，该服务可让您接收推送到您设置的网址的数据或使用客户端库轮询的数据。这些通知允许您立即对订阅状态的变化做出反应，这样就无需轮询 Google Play Developer API。请注意，如果 Google Play Developer API 的使用效率低下，可能会导致 API 配额限制。

Cloud Pub/Sub 是一种全代管式实时消息传递服务，您可以使用该服务在独立应用之间收发消息。Google Play 使用 Cloud Pub/Sub 发布有关您所订阅主题的推送通知。

为了接收通知，您需要创建后端服务器以使用发送到您主题的消息。您的服务器随后便可以使用这些消息，方法是响应对已注册端点的 HTTPS 请求，或使用 Cloud Pub/Sub 客户端库。这些库有多种语言版本。如需了解详情，另请参阅本主题的创建 Pub/Sub 订阅部分。

如需详细了解定价和配额，请参阅定价和配额。

订阅通知的流量大约为每个请求 1KB 的流量。每次发布和提取通知都需要一个单独的请求，即每个通知大约 2KB 的流量。每月的通知数量取决于您的结算周期和用户的行为。在一个结算周期内，每个用户应至少有一个通知。

如需启用实时开发者通知，您必须先使用自己的 Google Cloud Platform (GCP) 项目设置 Cloud Pub/Sub，然后再为您的应用启用通知。

如需使用 Cloud Pub/Sub，您必须拥有一个启用了 Cloud Pub/Sub API 的 GCP 项目。如果您不熟悉 GCP 和 Cloud Pub/Sub，请参阅快速入门指南。

注意：您必须分别为每个 Android 应用配置实时开发者通知。这意味着，您可以选择使用与用来访问 Play Developer API 的 GCP 项目相同的 GCP 项目，也可以为每个应用创建一个新的 GCP 项目。如果您有多个应用，必须对 Google Play Developer API 使用相同的 Google Cloud 控制台项目，但可以对各个应用使用不同的 Google Cloud 控制台项目。

如需开始接收通知，您必须创建一个主题，Google Play 会将通知发布到该主题。如需创建主题，请按照创建主题中的说明操作。

如需接收发布到某个主题的消息，您必须创建对该主题的 Pub/Sub 订阅。如需创建 Pub/Sub 订阅，请执行以下操作：

Cloud Pub/Sub 要求您向 Google Play 授予向您的主题发布通知的权限。

添加服务账号 google-play-developer-notifications@system.gserviceaccount.com，然后授予其 Pub/Sub 发布商的角色。

如需为您的应用启用实时开发者通知，请执行以下操作：

在主题名称字段中，输入您之前配置的完整 Cloud Pub/Sub 主题名称。主题名称应采用 projects/{project_id}/topics/{topic_name} 格式，其中 project_id 是项目的唯一标识符，topic_name 是之前创建的主题的名称。

点击发送测试消息以发送测试消息。执行测试发布有助于确保一切均已正确设置和配置。如果测试发布成功，则系统会显示一条消息，表明测试发布已成功。如果您已附加该主题的订阅，则应收到测试消息。

对于“拉取订阅”，请在 Cloud 控制台中找到该订阅，点击查看消息，然后继续拉取消息。您应该确认提取的任何消息，以避免 Cloud Pub/Sub 重复传送。对于推送订阅，检查测试消息是否已传送至您的推送端点。成功的响应代码将充当消息确认的作用。

如果发布失败，则系统会显示错误。请确保主题名称正确，并且 google-play-developer-notifications@system.gserviceaccount.com 服务账号拥有对该主题的 Pub/Sub 发布商访问权限。

为了接收实时开发者通知，您应创建安全的后端服务器，以使用发送到您的 Cloud Pub/Sub 主题的消息。

您可以使用 Google Play 管理中心的发送测试消息按钮来测试您的配置，如上一部分中所述。如果您尚未配置后端服务器以使用通知，可以使用 gcloud 命令行工具来验证配置。有关使用 gcloud 处理消息的说明，请参阅从订阅拉取消息。

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

## 做好准备 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/getting-ready?hl=zh-cn

**Contents:**
- 做好准备 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。
- 设置 Google Play 开发者账号
- 在 Google Play 管理中心内启用结算相关功能
  - 添加库依赖项
  - Groovy
  - Kotlin
  - Groovy
  - Kotlin
  - 上传应用
- 创建和配置您的商品

本主题列出并说明了在您的应用中销售商品之前需要执行的设置步骤。大体上讲，此设置包括创建开发者账号、创建和配置要销售的商品，以及启用和配置用于销售和管理商品的 API。此外，本主题还介绍了如何配置实时开发者通知，以便在商品的状态发生变化时随时收到通知。

如需在 Google Play 上发布您的应用和游戏，请使用 Google Play 管理中心。您还可以使用 Google Play 管理中心管理与结算相关的商品和设置。

如需访问 Google Play 管理中心，您需要设置 Google Play 开发者账号。

如需在 Google Play 上销售付费应用和应用内购商品，您还必须在 Google 付款中心设置付款资料，然后将该付款资料与您的 Google Play 开发者账号相关联。如需了解如何将您的付款资料与账号相关联，或者了解如何检查您是否已有关联的账号和付款资料，请参阅将 Google Play 开发者账号与您的付款资料相关联。

设置开发者账号后，您必须发布包含 Google Play 结算库的应用版本。如需在 Google Play 管理中心启用结算相关功能（如配置您要销售的商品），必须执行此步骤。

如需集成 Google Play 结算系统，请先在您的应用中添加对 Google Play 结算库的依赖项。此库可让您访问用于连接到 Google Play 的 Android API。这样，您便可以访问购买信息、查询有关购买交易的更新、提示用户进行新的购买交易，等等。

Google 的 Maven 代码库中提供了 Google Play 结算库。将依赖项添加到应用的 build.gradle 文件中，如下所示：

如果您使用的是 Kotlin，Play 结算库 KTX 模块包含了 Kotlin 扩展程序和协程支持，可让您在使用 Google Play 结算系统时编写惯用的 Kotlin 代码。如需将这些扩展程序包含在项目中，请将以下依赖项添加到应用的 build.gradle 文件中，如下所示：

本页中的 Kotlin 代码示例尽可能使用了 KTX。

将该库添加到您的应用后，构建并发布您的应用。在此步骤中，创建您的应用，然后将其发布到任何轨道，包括内部测试轨道。

为您的应用启用 Google Play 结算服务功能后，您需要配置要销售的商品。

创建一次性商品和订阅的步骤相似。对于每个商品，您需要提供唯一的商品 ID、商品名、说明和定价信息。订阅具有其他必需的信息，例如选择基础方案是自动续订类型还是预付费续订类型。

Google Play 管理中心提供了一个可用于管理商品的网页界面。

如需创建和配置一次性商品，请参阅创建受管理的商品。 请注意，Google Play 管理中心将一次性商品称为“受管理的商品”。

作为网页界面的替代方案，您还可以使用 Google Play Developer API 中的 inappproducts REST 资源（对于应用内商品）和 monetization.subscriptions REST 资源（对于订阅商品）来管理商品。

Google Play Developer API 是一种服务器到服务器 API，与 Android 平台上的 Google Play 结算库相辅相成。此 API 提供了 Google Play 结算库中未提供的功能，如安全地验证购买交易以及为用户办理退款。

在将 Google Play 结算系统集成到应用的过程中，您必须通过 Google Play 管理中心来配置对 Google Play Developer API 的访问权限。有关说明，请参阅 Google Play Developer API 使用入门。

配置对 Google Play Developer API 的访问权限后，请确保您已授予查看财务数据权限，需要具备此权限才能访问与结算相关的功能。如需了解最佳做法以及有关配置权限的详细信息，请参阅添加开发者账号用户并管理权限。

借助实时开发者通知 (RTDN) 机制，每当用户的权限在您的应用中发生变化时，您都会收到来自 Google 的通知。RTDN 利用 Google Cloud Pub/Sub，该服务可让您接收推送到您设置的网址的数据或使用客户端库轮询的数据。这些通知允许您立即对订阅状态的变化做出反应，这样就无需轮询 Google Play Developer API。请注意，如果 Google Play Developer API 的使用效率低下，可能会导致 API 配额限制。

Cloud Pub/Sub 是一种全代管式实时消息传递服务，您可以使用该服务在独立应用之间收发消息。Google Play 使用 Cloud Pub/Sub 发布有关您所订阅主题的推送通知。

为了接收通知，您需要创建后端服务器以使用发送到您主题的消息。您的服务器随后便可以使用这些消息，方法是响应对已注册端点的 HTTPS 请求，或使用 Cloud Pub/Sub 客户端库。这些库有多种语言版本。如需了解详情，另请参阅本主题的创建 Pub/Sub 订阅部分。

如需详细了解定价和配额，请参阅定价和配额。

订阅通知的流量大约为每个请求 1KB 的流量。每次发布和提取通知都需要一个单独的请求，即每个通知大约 2KB 的流量。每月的通知数量取决于您的结算周期和用户的行为。在一个结算周期内，每个用户应至少有一个通知。

如需启用实时开发者通知，您必须先使用自己的 Google Cloud Platform (GCP) 项目设置 Cloud Pub/Sub，然后再为您的应用启用通知。

如需使用 Cloud Pub/Sub，您必须拥有一个启用了 Cloud Pub/Sub API 的 GCP 项目。如果您不熟悉 GCP 和 Cloud Pub/Sub，请参阅快速入门指南。

注意：您必须分别为每个 Android 应用配置实时开发者通知。这意味着，您可以选择使用与用来访问 Play Developer API 的 GCP 项目相同的 GCP 项目，也可以为每个应用创建一个新的 GCP 项目。如果您有多个应用，必须对 Google Play Developer API 使用相同的 Google Cloud 控制台项目，但可以对各个应用使用不同的 Google Cloud 控制台项目。

如需开始接收通知，您必须创建一个主题，Google Play 会将通知发布到该主题。如需创建主题，请按照创建主题中的说明操作。

如需接收发布到某个主题的消息，您必须创建对该主题的 Pub/Sub 订阅。如需创建 Pub/Sub 订阅，请执行以下操作：

Cloud Pub/Sub 要求您向 Google Play 授予向您的主题发布通知的权限。

添加服务账号 google-play-developer-notifications@system.gserviceaccount.com，然后授予其 Pub/Sub 发布商的角色。

如需为您的应用启用实时开发者通知，请执行以下操作：

在主题名称字段中，输入您之前配置的完整 Cloud Pub/Sub 主题名称。主题名称应采用 projects/{project_id}/topics/{topic_name} 格式，其中 project_id 是项目的唯一标识符，topic_name 是之前创建的主题的名称。

点击发送测试消息以发送测试消息。执行测试发布有助于确保一切均已正确设置和配置。如果测试发布成功，则系统会显示一条消息，表明测试发布已成功。如果您已附加该主题的订阅，则应收到测试消息。

对于“拉取订阅”，请在 Cloud 控制台中找到该订阅，点击查看消息，然后继续拉取消息。您应该确认提取的任何消息，以避免 Cloud Pub/Sub 重复传送。对于推送订阅，检查测试消息是否已传送至您的推送端点。成功的响应代码将充当消息确认的作用。

如果发布失败，则系统会显示错误。请确保主题名称正确，并且 google-play-developer-notifications@system.gserviceaccount.com 服务账号拥有对该主题的 Pub/Sub 发布商访问权限。

为了接收实时开发者通知，您应创建安全的后端服务器，以使用发送到您的 Cloud Pub/Sub 主题的消息。

您可以使用 Google Play 管理中心的发送测试消息按钮来测试您的配置，如上一部分中所述。如果您尚未配置后端服务器以使用通知，可以使用 gcloud 命令行工具来验证配置。有关使用 gcloud 处理消息的说明，请参阅从订阅拉取消息。

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

## 将 Google Play 结算库集成到您的应用中 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/integrate?hl=zh-cn

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

## 将 Google Play 结算库集成到您的应用中 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/integrate

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

## 将 Google Play 结算库集成到您的应用中 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

**URL:** https://developer.android.google.cn/google/play/billing/billing_library_overview?hl=zh-cn

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
