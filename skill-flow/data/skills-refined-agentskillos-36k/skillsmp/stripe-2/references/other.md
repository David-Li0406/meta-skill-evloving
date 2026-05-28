# Stripe - Other

**Pages:** 28

---

## Design a custom POS integration

**URL:** https://docs.stripe.com/terminal/designing-integration

**Contents:**
- Design a custom POS integration
- Choose your country, reader, and integration type to learn how to build your custom point of sale.
    - Reader details
- S700 reader
- Use it in a server-driven integration
  - Limitations
- Architecture
- Prototyping
  - Using the simulated reader
  - Using a physical reader

For more information about the differences between readers, see Select your reader.

Set up your integration

Server-driven integration doesn’t support:

If you don’t write code, you can find a Stripe partner who supports Terminal.

In a server-driven integration, your POS device connects to your server. Your server then makes Stripe API calls, and Stripe updates the reader and returns the result.

The structure of the integration looks like this:

When you begin writing your application, you can test it with a simulated reader and simulated cards—no reader hardware required. This lets you build and verify your complete integration without needing physical hardware. The Terminal Quickstart demonstrates an app at this stage of development.

When you’re ready to work with actual hardware, you can extend your integration to a physical device. Follow these steps:

Stripe requires a Location to be associated with every Terminal reader, including a simulated reader. Before you connect a reader to a Terminal integration, you must create one or more Locations, either in the Dashboard or using the API. When you connect to your reader, specify one of those locations.

Locations represent physical places where your readers operate. Stripe needs location information to process payments correctly and keep your reader up to date. If your business requires you to move your readers frequently, your locations can use addresses that represent a primary place of business.

---

## Terminal

**URL:** https://docs.stripe.com/terminal

**Contents:**
- Terminal
- Use Stripe Terminal to accept in-person payments and extend Stripe payments to your point of sale.
- Learn about Terminal
- Integration options
- Platforms with in-person payments
- In-person fundamentals
- Features

Stripe Terminal allows businesses to accept in-person card payments using card readers. You can manage both in-person payments and online payments in a unified system in the Dashboard. You can also integrate Terminal with your Connect platform.

Learn more about Terminal’s features and availability by country.

Use Stripe Terminal to unify online and in-person payments.

Learn about Stripe Terminal through example use cases and the architecture of an integration.

Understand interactions between Terminal SDKs and readers, and your backend and point-of-sale application.

Build a starter integration with our code-based tour that includes downloadable files so you can follow along.

Build a custom POS integration tailored to your business. Terminal supports an API-based integration in addition to SDKs for Android, iOS, JavaScript, and React Native.

Accept contactless payments using a compatible iPhone or Android device with the Stripe Terminal SDK.

Deploy your Android POS app to Stripe smart readers.

You can incorporate Stripe Terminal into your existing stack using third-party POS, hardware, and commerce integrations—no code required.

Combine the Stripe payments suite with gateway supported POS systems, third-party hardware options, gift cards, and other commerce integrations—no code required.

Learn how to integrate Stripe Terminal with your Connect platform.

Integrate Stripe Terminal with your Connect platform.

Save cards to initiate a subscription, attach payment details to a customer’s online account, or defer payment.

Understand the two-step authorization and capture process and how to perform a cancellation or refund.

Dynamically update a smart reader’s screen with individual items in the transaction, along with total price.

Provide your customers with receipts that meet card network rules and local regulatory requirements.

In-person payments: Accept payments using physical card readers for in-person and Tap to Pay transactions that can automatically allow for tip adjustments during checkout.

Multiple payment methods: Accept various payment types, including debit and credit cards, contactless payments, and mobile wallets.

Reader choices: Choose from different readers, depending on your business needs.

Multiple platform support: Integrate Stripe Terminal into any platform using a server-driven integration. For example, add Terminal to your mobile app for iOS or Android.

Accept payments offline: Accept payments with intermittent, limited, or no internet connectivity.

---

## Collect swiped dataPrivate preview

**URL:** https://docs.stripe.com/terminal/features/collect-data

**Contents:**
- Collect swiped dataPrivate preview
- Use Terminal for collecting non-PCI data with the reader hardware interfaces.
    - Private preview
- Collect data
  - SDK Reference
    - Note
- Fetch collected data
    - Note

Request access to the Collect data private preview by sending an email to terminal-collect-data@stripe.com with the following information:

Use the Terminal SDK and the reader’s hardware interfaces (such as the magnetic stripe reader) to read non-PCI payment methods such as gift cards. This feature isn’t available offline.

After swiping the card, the Terminal SDK provides a tokenized data object. Use the token to securely retrieve the cleartext track data on your back end.

The Terminal reader only reads and stores cleartext magstripe data that follows these formats:

Contact the Terminal team with your card format and BIN ranges if your card numbers don’t match one of these approved formats.

Collecting swiped data is available in:

Use Terminal.collectData() to prompt your point-of-sale application to collect data. Specify the type of data you want to receive in the configuration passed to the function, such as .magstripe. After a customer swipes a card, the SDK returns a token that represents the data or an error if the swipe fails. Use this token in your integration to refer to the data.

On supported readers, the ability for customers to cancel transactions is now enabled by default. To disable customer cancellation on smart readers, set customerCancellation to .disableIfAvailable.

When you need to perform operations such as redeeming a gift card, fetch the cleartext data from your backend using the collected data token. The collected data is stored on Stripe’s servers for 24 hours.

Stripe doesn’t perform and isn’t responsible for the authentication of collected data or the authorization of transactions using collected data. Stripe isn’t liable for any illegal conduct or fraud by any third party associated with the collected data.

**Examples:**

Example 1 (javascript):
```javascript
import UIKit
import StripeTerminal

class PaymentViewController: UIViewController {
    func readGiftCard() throws {
        let config = try CollectDataConfigurationBuilder()
            .setCollectDataType(.magstripe)
            .build()
        self.cancelable = Terminal.shared.collectData(config) { collectedData, collectError in
            if let error = collectError {
                // Handle read errors
                print("Collect data failed: \(error)")
            } else if let data = collectedData, let stripeId = data.stripeId {
                print("Received collected data token: \(stripeId)")
            }
        }
    }
}
```

Example 2 (javascript):
```javascript
import UIKit
import StripeTerminal

class PaymentViewController: UIViewController {
    func readGiftCard() throws {
        let config = try CollectDataConfigurationBuilder()
            .setCollectDataType(.magstripe)
            .build()
        self.cancelable = Terminal.shared.collectData(config) { collectedData, collectError in
            if let error = collectError {
                // Handle read errors
                print("Collect data failed: \(error)")
            } else if let data = collectedData, let stripeId = data.stripeId {
                print("Received collected data token: \(stripeId)")
            }
        }
    }
}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/reader_collected_data/tmrcd_xxxxxxxx \
  -u "sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/reader_collected_data/tmrcd_xxxxxxxx \
  -u "sk_test_YOUR_TEST_KEY_HERE:"
```

---

## Collect tips

**URL:** https://docs.stripe.com/terminal/features/collecting-tips/overview

**Contents:**
- Collect tips
- Learn about the different ways you can collect tips from customers.
- On-receipt versus on-reader tipping
- How tips are displayed on-receipt or on-reader
    - Caution

Use Terminal to collect tips from your customer before or after authorizing a payment. You can collect voluntary tips in two ways:

For mandatory tips, you must include the tip amount in the original PaymentIntent amount. You can’t use on-receipt or on-reader tipping.

The table below outlines some differences between on-receipt tipping and on-reader tipping.

Stripe Reader S700 and BBPOS WisePOS E:

BBPOS WisePOS E and Stripe Reader S700:

All SDKs, server-driven

On-receipt and on-reader tipping use the PaymentIntents API, work with all Terminal SDKs, and require manual capture.

Choose only one tipping method per PaymentIntent. If you use on-reader tipping, you can’t use the same PaymentIntent for on-receipt tipping.

The table below summarizes the specific API behavior.

Tips in the underlying Charge object

Tips aren’t directly represented in the Charge object.

After capture, the fields below all show the same value inclusive of the tip.

Tips can be derived from the Charge object. You can derive the tip by subtracting amount_authorized from amount.

---

## Example applications

**URL:** https://docs.stripe.com/terminal/example-applications

**Contents:**
- Example applications
- Try Stripe Terminal by using the example applications and simulated reader.
    - Note
- Deploy the example backend
- Run the example application
- Connect to a simulated reader
- Collect your first payment
    - Note
- Next steps

For a more immersive guide including details on server driven integration using only the Stripe API, check out the sample integration.

A Stripe Terminal integration starts with your point-of-sale application running at a physical location. Your point-of-sale application communicates with a reader through the Terminal SDK to collect in-person payments from your customers. Your backend works with your point-of-sale application to authenticate the Terminal SDK and finalize payments.

Before starting your own integration, we recommend setting up one of the Terminal example applications. This will give you a better feel for how the components of a Terminal integration fit together and show you the interactions between the SDK, the reader, your point-of-sale application, and your backend code.

To get started with the example applications, set up the Sinatra-based example backend by following the instructions in the README. You can either run the backend locally or deploy it to Render with a free account. The example backend works with the example application to authenticate the Terminal SDK and finalize payments.

Build and run one of the example applications:

After you have the example running, select Use simulator to connect to a simulated reader.

The JavaScript example app connected to a simulated reader

The simulated reader handles events just like a physical reader, so you can continue to collecting your first payment.

The simulated reader functionality is built into the SDK, so you can use it to develop and test your own point-of-sale application without connecting to a physical device.

Collect your first payment using the example application and a simulated reader. Each of the examples features an event log for you to reference as you integrate Terminal in your own application. As you collect your first payment, you’ll see the following sequence:

(Optional) Use separate authorization and capture to add a reconciliation step before finalizing the transaction. You can also automatically capture Terminal transactions.

Collecting a payment, using the JavaScript example app and a simulated reader

**Examples:**

Example 1 (unknown):
```unknown
git clone https://github.com/stripe/stripe-terminal-js-demo.git
```

Example 2 (unknown):
```unknown
git clone https://github.com/stripe/stripe-terminal-js-demo.git
```

Example 3 (unknown):
```unknown
cd stripe-terminal-js-demo
npm install
npm run start
```

Example 4 (unknown):
```unknown
cd stripe-terminal-js-demo
npm install
npm run start
```

---

## Collect on-screen inputs

**URL:** https://docs.stripe.com/terminal/features/collect-inputs

**Contents:**
- Collect on-screen inputs
- Use Terminal to collect inputs from your customers.
    - Note
- Collect inputs
  - Customization
  - Metadata
- Customer interaction
    - Note
- Receive input data
- Download signature images

Readers: Stripe Reader S700 and BBPOS WisePOS E

With Terminal smart readers, you can display input forms and collect information from your customers. You can choose from six input types and they can be used in a variety of use cases.

You can display input forms anytime before payment, post payment and outside of a payment cycle.

Supported input types.

Don’t use collect_inputs to collect sensitive data (including protected health information and customer payment card information), or any information restricted by law.

To collect inputs using Terminal’s smart readers, use the collect_inputs command. The API communicates with the reader to display a prebuilt UI.

You can customize the appearance and behavior of all input types:

Email and selection form with toggle

Primary and secondary selection choice styles

You can include metadata, like a customer or order ID, in your request. The request payload includes the specified metadata, which appears in both the synchronous response and the success or failure events. By including a unique identifier, you can more easily identify and handle the incoming event.

When the reader begins collecting inputs, it displays the first input from the list. The customer must make a selection, provide a signature, or use the keyboard to proceed with required inputs. For optional inputs, the customer has the option to skip to the next requested input.

After the customer has completed all the inputs, the reader changes to a transitional state for 3 seconds, waiting for a subsequent request. If there is no subsequent request after 3 seconds, the reader changes back to the splash screen.

You are fully responsible for being aware of, and complying with all applicable laws and regulations governing your use of this feature, and must in relation to such use, obtain, as applicable, all necessary consents, authorizations, licenses, rights, and permissions. If you use input collected by, or output displayed from a Terminal smart reader to enter into contracts with, or provide notices to your customers, you are fully responsible for ensuring the legal validity and enforceability of such contracts or notices.

When all inputs have been collected or skipped, Stripe sends a request to your webhook endpoint. The request payload is identical to the response when calling collect_inputs, but adds a few additional parameters:

Use the curl command below as an example to create a webhook endpoint to receive the collected inputs.

Subscribe to events to receive collected inputs as soon as they’re available. Alternatively, you can retrieve the events from the reader as a backup if your backend fails to consume the event. Stripe sends two webhooks to notify your backend of the reader’s status:

To download the collected signature image, retrieve the file and use your secret key to access its url.

Stripe stores the signature images you collect for 7 days. If you need to use signature images more than 7 days after collecting them, download the file and store it. You are fully responsible for being aware of and complying with all laws that apply to your use, storage, and disclosure of your customers’ signatures.

You can test your integration by using a simulated reader. After creating a simulated reader, start collecting inputs using the simulated reader.

The simulated reader supports simulating the following scenarios:

When simulating successful input collection, the simulated reader returns a hard-coded value for each input based on the type.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/readers/{{READER_ID}}/collect_inputs \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d "inputs[0][type]"=signature \
  -d "inputs[0][custom_text][title]"="Rental Agreement" \
  -d "inputs[0][custom_text][description]"="Please sign below to indicate that you agree to the rental agreement." \
  -d "inputs[0][custom_text][submit_button]"=Submit \
  -d "inputs[0][required]"=true \
  -d "inputs[1][type]"=selection \
  -d "inputs[1][selection][choices][0][style]"=primary \
  -d "inputs[1][selection][choices][0][text]"=Email \
  -d "inputs[1][selection][choices][0][id]"=email_id \
  -d "inputs[1][selection][choices][1][style]"=primary \
  -d "inputs[1][selection][choices][1][text]"=Printed \
  -d "inputs[1][selection][choices][1][id]"=printed_id \
  -d "inputs[1][selection][choices][2][style]"=secondary \
  -d "inputs[1][selection][choices][2][text]"="No thanks" \
  -d "inputs[1][selection][choices][2][id]"=no_thanks_id \
  -d "inputs[1][custom_text][title]"=Receipt \
  --data-urlencode "inputs[1][custom_text][description]"="How would you like your receipt?" \
  -d "inputs[1][required]"=true \
  -d "inputs[2][type]"=email \
  -d "inputs[2][custom_text][title]"="Enter your email" \
  --data-urlencode "inputs[2][custom_text][description]"="We'll send updates on your order and occasional deals" \
  -d "inputs[2][required]"=true \
  -d "inputs[2][toggles][0][title]"="Opt-in for marketing emails" \
  -d "inputs[2][toggles][0][default_value]"=enabled \
  -d "metadata[order_number]"=12345
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/readers/{{READER_ID}}/collect_inputs \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d "inputs[0][type]"=signature \
  -d "inputs[0][custom_text][title]"="Rental Agreement" \
  -d "inputs[0][custom_text][description]"="Please sign below to indicate that you agree to the rental agreement." \
  -d "inputs[0][custom_text][submit_button]"=Submit \
  -d "inputs[0][required]"=true \
  -d "inputs[1][type]"=selection \
  -d "inputs[1][selection][choices][0][style]"=primary \
  -d "inputs[1][selection][choices][0][text]"=Email \
  -d "inputs[1][selection][choices][0][id]"=email_id \
  -d "inputs[1][selection][choices][1][style]"=primary \
  -d "inputs[1][selection][choices][1][text]"=Printed \
  -d "inputs[1][selection][choices][1][id]"=printed_id \
  -d "inputs[1][selection][choices][2][style]"=secondary \
  -d "inputs[1][selection][choices][2][text]"="No thanks" \
  -d "inputs[1][selection][choices][2][id]"=no_thanks_id \
  -d "inputs[1][custom_text][title]"=Receipt \
  --data-urlencode "inputs[1][custom_text][description]"="How would you like your receipt?" \
  -d "inputs[1][required]"=true \
  -d "inputs[2][type]"=email \
  -d "inputs[2][custom_text][title]"="Enter your email" \
  --data-urlencode "inputs[2][custom_text][description]"="We'll send updates on your order and occasional deals" \
  -d "inputs[2][required]"=true \
  -d "inputs[2][toggles][0][title]"="Opt-in for marketing emails" \
  -d "inputs[2][toggles][0][default_value]"=enabled \
  -d "metadata[order_number]"=12345
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/webhook_endpoints \
  -u sk_test_YOUR_TEST_KEY_HERE: \
  --header "Stripe-Version: 2025-05-28.basil;" \
  --data-urlencode "url"="https://example.com/webhook/endpoint" \
  --data-urlencode "api_version"="2025-05-28.basil;" \
  --data-urlencode "enabled_events[]"="terminal.reader.action_succeeded" \
  --data-urlencode "enabled_events[]"="terminal.reader.action_failed"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/webhook_endpoints \
  -u sk_test_YOUR_TEST_KEY_HERE: \
  --header "Stripe-Version: 2025-05-28.basil;" \
  --data-urlencode "url"="https://example.com/webhook/endpoint" \
  --data-urlencode "api_version"="2025-05-28.basil;" \
  --data-urlencode "enabled_events[]"="terminal.reader.action_succeeded" \
  --data-urlencode "enabled_events[]"="terminal.reader.action_failed"
```

---

## Terminal configurations

**URL:** https://docs.stripe.com/terminal/fleet/configurations-overview

**Contents:**
- Terminal configurations
- Use the Terminal Configurations object to apply configurations to your readers.
    - Private preview
    - Note
- Update the default configuration for the account
- Create a new configuration for a location
    - From the location details page
    - From the manage locations page
- Update an existing configuration
    - From the location details page

The Terminal Configuration object contains all relevant configurations for a reader, such as the splash screen, tipping settings, offline mode, and so on (see individual configuration guides for specific instructions and options).

Because these settings are hierarchical, you can apply a configuration at either the account level or at the individual location level. You can set configurations in the following ways:

You can override account-level settings with location-level settings. If you don’t configure settings at the location level, they inherit the account-level settings.

Creating configurations for zones is in private preview. You can email us to request to join the preview.

For example, you can model your Configuration objects as follows:

In this scenario, Location 3 inherits the configurations from the account “Default configuration”, while Locations 1 and 2 have their own configuration.

If you don’t set a configuration on the location-level, the Location inherits the default configuration on the account. For example, if you don’t set the splash screen on the Location, it inherits it from the default configuration set at the account level.

Any configuration changes made with the API or Dashboard can take up to 10 minutes to reflect on the target readers.

You can view and manage your configurations in the Stripe Dashboard. To manage your configurations, click Manage locations on the Readers tab. Stripe displays a list of configurations on the right hand side of the page. To view additional configurations, click View more at the bottom of the list.

All readers across all locations inherit the configuration settings that you set, unless there’s an override set on the configuration for the location. The reader updates within 10 minutes after you add the configuration.

All readers in the location inherit the configuration settings that you set. The reader updates within 10 minutes after you add the configuration.

All the readers in the location update within 10 minutes.

After you delete the configuration, the readers in the location default back to the account’s default configuration within 10 minutes.

---

## ES Module Stripe.js SDK

**URL:** https://docs.stripe.com/sdks/stripejs-esmodule

**Contents:**
- ES Module Stripe.js SDK
- Set up the ES Module Stripe.js client-side SDK in your web application.
  - See the code
- Before you begin
- Manually load the Stripe.js script
  - Installation
  - Stripe.js constructor
- Load Stripe.js as an ES Module
  - Installation
  - Stripe.js constructor

To see how ES Module Stripe.js works or to help develop it, check out the project on GitHub.

This introductory guide shows you how to install the ES Module Stripe.js client-side SDK with a script tag or package manager. The SDK wraps the global Stripe function provided by the Stripe.js script as an ES module. It allows you to use Elements, our prebuilt UI components, to create a payment form that lets you securely collect a customer’s card details without handling the sensitive data.

Enable the payment methods you want to support on the payment methods settings page.

To install by script, add the Stripe.js ES Module as a script to the <head> element of your HTML. This allows any newly created Stripe objects to be globally accessible in your code.

Next, set the API publishable key to allow Stripe to tokenize customer information and collect sensitive payment details. For example:

To install by package manager, install the Stripe.js ES Module from the npm public registry.

Next, import the module into a JavaScript file. The following function returns a Promise that resolves with a newly created Stripe object after Stripe.js loads.

This wraps up the introductory guide to setting up the ES Module Stripe.js SDK. See the links below to get started with your integration.

**Examples:**

Example 1 (unknown):
```unknown
<head>
  <title>Checkout</title>
  <script src="https://js.stripe.com/clover/stripe.js" async></script>
</head>
```

Example 2 (unknown):
```unknown
<head>
  <title>Checkout</title>
  <script src="https://js.stripe.com/clover/stripe.js" async></script>
</head>
```

Example 3 (unknown):
```unknown
var stripe = Stripe('pk_test_TYooMQauvdEDq54NiTphI7jx');
```

Example 4 (unknown):
```unknown
var stripe = Stripe('pk_test_TYooMQauvdEDq54NiTphI7jx');
```

---

## Stripe.js versioning and support policy

**URL:** https://docs.stripe.com/sdks/stripejs-versioning

**Contents:**
- Stripe.js versioning and support policy
- Learn about the Stripe.js versioning and support policy.
- Types of changes
  - Optimizations and new features
  - Breaking changes
- Usage
  - With a script tag
  - With stripe-js on npm
  - With react-stripe-js on npm
- Version lifecycle

Stripe.js uses an evergreen model, which means it receives updates continuously over time. Stripe.js v3, the scripts backing js.stripe.com/v3, was the most recent version of Stripe.js for many years. We release new major versions such as Acacia on a biannual basis. These versions allow us to introduce major features and breaking changes on a predictable schedule, so you can plan your upgrades.

Changes to Stripe.js fall into two main categories:

The most common type of change we make to Stripe.js are optimizations and new features.

We add new features, make optimizations, and fix bugs such as critical security issues, without any required integration changes. This happens automatically for all Stripe.js integrations, and will continue for all versions of Stripe.js. All versions continue to get these non-breaking updates and are regularly updated together in our internal release process.

Some examples of optimizations we consider to be non-breaking:

Some changes require integration changes to gain access to, but aren’t breaking changes. One example might be adding a new function on the Stripe object. We safely release these features across some existing Stripe.js versions in our regular release process. This process is called backporting.

The Stripe.js versioning system is a tool that enables us to release new features that might otherwise be constrained by our need to support backward compatibility. We release these breaking changes in Stripe releases, done twice per year.

A breaking change is something that could cause your integration to fail or appear broken. For example:

There are three ways to use versioned Stripe.js: with a script tag, with the @stripe/stripe-js package on npm, or with the @stripe/react-stripe-js package on npm.

To use versioned Stripe.js, include the version name in the script tag’s URL.

We recommend that you stay up to date with the latest version of Stripe.js. Stripe.js v3 is no longer recommended for integrations, but we’ll continue to support it.

If you use Stripe.js with the @stripe/stripe-js package on npm, you can continue to consume Stripe.js this way. Starting with @stripe/stripe-js@6.0.0, each major version of Stripe.js consumes a specific fixed version of Stripe.js. For example, @stripe/stripe-js@6.0.0 consumes Stripe.js acacia. For information about the relationships between specific @stripe/stripe-js versions and their corresponding Stripe.js versions, see the releases page.

Although non-breaking runtime functionality of Stripe.js is backported to old versions of Stripe.js, the TypeScript types on npm aren’t backported to old major versions in @stripe/stripe-js. To stay up to date with the most recent TypeScript types, update to the most recent release of Stripe.js and @stripe/stripe-js.

The @stripe/react-stripe-js package continues to work with the @stripe/stripe-js package using its peerDependencies.

We release Stripe.js major versions alongside the API release trains twice per year. We release non-breaking changes, including both optimizations and backported features, on our ongoing frequent release schedule. We continue to support and update older versions.

When performing API requests, each versioned Stripe.js automatically uses the API version associated with the Stripe.js version. That is, the Stripe.js acacia version uses a compatible API version such as 2024-12-18.acacia (which includes the date) to represent the release date of the API version. You can’t override the API version.

The changelog shows the history of versioned changes in Stripe.js over time. It includes all breaking changes and other important changes and is the best place to understand what integration changes you need to make to upgrade Stripe.js versions.

Review the following considerations before you upgrade from Stripe.js v3 to a newer version.

Updating Stripe.js from v3 to a named version such as Acacia can break API requests, depending on the API version you previously used for the requests. To upgrade older accounts, we recommend this process:

API versions can contain breaking changes for previews that aren’t listed in the changelog, so you need to upgrade your Stripe.js version carefully if you’re on a preview such as the Elements with Checkout Sessions beta.

Historically, some preview features involved adding beta headers to your apiVersion used by Stripe.js requests (for example, '2025-02-24.acacia; custom_checkout_beta=v1'). Because we no longer support this API version override, you can’t explicitly add beta headers directly to API requests. Instead, any supported Stripe.js previews add necessary headers automatically when the corresponding beta flag (for example custom_checkout_beta_5) is set when you initialize Stripe.js.

For acacia, this is expressly supported for custom_checkout_beta and nz_bank_account_beta. If you provide API headers for other previews, contact the email provided to you for preview support to determine your options for upgrading Stripe.js or migrating to GA behavior.

We’ll continue to support js.stripe.com/v3 for the foreseeable future. We’ll backport features to this version and continue to maintain Stripe.js v3 as an evergreen version. Stripe.js v3 isn’t deprecated, but we encourage you to regularly update your applications to the newest version of Stripe.js to access recent features that can’t be backported because of their breaking changes.

**Examples:**

Example 1 (unknown):
```unknown
<script src="https://js.stripe.com/clover/stripe.js"></script>
```

Example 2 (unknown):
```unknown
<script src="https://js.stripe.com/clover/stripe.js"></script>
```

---

## Apps on Devices

**URL:** https://docs.stripe.com/terminal/features/apps-on-devices/overview

**Contents:**
- Apps on Devices
- Learn about deploying your Android POS apps on Stripe smart readers.
  - Contact Stripe
- Supported integrations
    - Point of sale app on a Stripe smart reader
    - Point-of-sale app paired with consumer-facing app on a Stripe smart reader
- App requirements
    - APK size limit
    - Device specs
    - Device storage

Apps on Devices isn’t available to all users. If you pay standard pricing on card present transactions, Apps on Devices is available at no extra cost. If you’re interested in using it, contact your sales representative so they can assess your eligibility and pricing. If you do not have a sales representative, contact us using the form at Stripe support to enable this feature.

To be eligible, you must have either an existing Android-based POS application or the resources to build an Android application. When using direct charges, a single platform must control your connected account.

Use Apps on Devices to run your point-of-sale (POS) application along with other apps on your device. You can deploy your POS app to Stripe smart readers to provide an all-in-one solution, or build a customer-facing app for payments, driven by your POS running on another device.

Stripe handles all payments and compliance with the Terminal SDK. Android and React Native SDKs support Apps on Devices.

Apps on Devices enables the key phases of your app lifecycle:

View the sample app to learn integration best practices, how to collect and confirm a payment, and more.

Apps on Devices supports two types of integrations:

In this integration, both your POS app and the Stripe Reader app run on a Stripe smart reader. When the device starts, it launches your POS app instead of the Stripe Reader app. When initiating a transaction, the Stripe Reader app becomes the primary. At the end of the transaction, the Stripe Reader app finishes and your POS app becomes the primary.

In this integration, your POS app runs on a device that’s separate from the Stripe smart reader. Your consumer-facing Android app runs on the Stripe smart reader and supports the payment transaction.

You manage the communication between your POS app and consumer-facing app over TCP/IP.

App resources are limited by the device specs, and app functionality might be constrained by differences from standard Android development. Make sure your app can run successfully by operating within the requirements below.

APK files that you upload to the Stripe API have a 200MB size limit.

Stripe manages updates over the air for all apps and software components that run on the device. Make sure your app uses 8GB or less of storage on the device.

The Stripe SmartPOS OS is built for security and PCI-compliance based on the Android Open Source Project (AOSP). It differs from standard consumer Android in the following ways:

You can use a DevKit device for development purposes.

During installation, the Stripe SmartPOS OS automatically grants Android permissions in your app’s manifest. The device user isn’t prompted for permission approval at runtime. Your app’s permissions are verified against the allowed permissions list, and apps requesting permissions in excess of the allowlist are rejected.

The camera, Bluetooth, and location capabilities and APIs are still in the experimental phase and haven’t been fully tested, validated, and approved by Stripe. Their performance, reliability, and stability aren’t guaranteed. Use this functionality at your discretion.

The NFC functionality in the devices only supports payments—it can’t be used for non-payment related features.

Platforms using Apps on Devices can deploy apps only to connected accounts that are controlled by a single platform. A connected account is supported if its controller.is_controller property is true. That prevents multiple platforms from deploying apps to the same connected account.

---

## Stripe Terminal reader product sheets

**URL:** https://docs.stripe.com/terminal/readers/product-sheets

**Contents:**
- Stripe Terminal reader product sheets
- Learn about Stripe Terminal hardware specifications.
- Stripe S700
- Stripe Reader M2
- BBPOS
- See also

In the Dashboard, browse and purchase available readers and accessories.

These product sheets contain important device specifications, operating information and instructions, and disclosures and warnings provided by the manufacturer.

---

## Dispute reason code categories

**URL:** https://docs.stripe.com/disputes/categories

**Contents:**
- Dispute reason code categories
- Learn about reason code categories and evidence guidelines.
- Reason code categories
- Category defense guidelines
  - How to prevent it
  - How to overturn it
- See also

Each payment method (such as a card, digital wallet, Buy now, Pay Later), defines hundreds of codes that represent specific reasons for dispute claims. These reasons often overlap across all of the different payment networks, thus Stripe organizes each payment method’s codes into one of eight categories. Each category is based on the general type of claim and the evidence required to effectively challenge it. You can manage disputes using the Dashboard or the API.

The following tables show the Stripe categories for each payment method’s dispute reason codes. The reason code is available on the dispute object. For more information about Visa, Mastercard, and Amex, see Dispute reason codes.

Use the selector to choose the category that matches the reason given for your dispute to see guidelines for responding.

The customer claims they’re entitled to a full or partial refund because they returned the purchased product or didn’t fully use it, or the transaction was otherwise canceled or not fully fulfilled, but you haven’t yet provided a refund or credit.

Explain and demonstrate one or more of the following:

Choose the product type of the disputed transaction to see relevant evidence suggestions.

Whether or not the customer attempted to resolve the issue with you prior to filing a dispute. If they didn’t reach out to you before the dispute, state that clearly.

If you did communicate with them prior to the dispute, or if later conversations shed light on the facts of the case, submit this with your evidence. This could look like:

customer_communication

Any argument invalidating the dispute reason, such as a PDF or screenshot showing:

uncategorized_text uncategorized_file

---

## Stripe Terminal smart readers

**URL:** https://docs.stripe.com/terminal/smart-readers

**Contents:**
- Stripe Terminal smart readers
- Learn about Stripe's pre-certified in-person payment readers.
- Reader software updates
    - Note

In the Dashboard, browse and purchase available readers and accessories.

Terminal’s smart readers are compatible with the JavaScript, iOS, Android, and React Native SDKs. In addition to the Terminal SDKs, the BBPOS WisePOS, the Stripe Reader S700, and Verifone readers are compatible with a server-driven integration. Smart readers communicate with the SDKs and Stripe API over the internet.

Stripe maintains the software that controls smart readers. The readers receive updates automatically from Stripe when not in use. Leave your reader connected to power to receive automatic software updates. This ensures that updates happen at midnight (in the timezone of the assigned location) to avoid interruption to sales. If you unplug the reader at night, an update could start when you turn it back on. To manually check for an update, reboot the reader.

Smart readers restart every day at midnight for PCI compliance, and disconnect from the POS app every morning.

---

## Receive payouts

**URL:** https://docs.stripe.com/payouts

**Contents:**
- Receive payouts
- Set up your bank account to receive payouts.
- Add or update your bank account
  - Supported bank account types
    - Note
  - Supported accounts and settlement currencies
  - Multiple bank accounts for different settlement currencies
- Payout schedule
    - Time zone difference
  - How payout timing works

You receive funds when Stripe (or your platform) makes payouts to your bank account. Payout availability varies depending on your industry and country of operation. When you start processing live payments, Stripe typically schedules your initial payout for 7-14 days after you successfully receive your first payment. Your first payout might take longer, depending on your industry risk level and country of operation. Subsequent payouts follow your account’s payout schedule.

You can see a comprehensive list of your payouts and the expected dates of deposit into your bank account in the Dashboard. If you’re a Connect platform, see Connect payouts.

You can add a new bank account or update existing account details from your Payout settings in the Dashboard. Based on your bank’s location, Stripe might require different account details to activate your bank account. You must match the currency of the bank account to the currency in your Payout settings. To modify banking information, click Edit next to the bank account you want to update.

Use the following table to see the required bank details for specific countries:

You can use various types of bank accounts for your Stripe payouts, including traditional accounts offered by established financial institutions (such as checking and savings accounts), virtual bank accounts (such as N26, Revolut, and Wise), and debit cards for instant payouts (if eligible).

While Stripe supports non-standard bank accounts, you might see higher payout failures for these accounts.

In most cases, bank accounts must be located in the country where the settlement currency is the official currency. For example, SEK bank accounts must be based in Sweden. Stripe also allows you to settle and pay out to banks in select additional currencies, or pay out to non-domestic bank accounts in the local currency, for a fee. Learn more about presenting and settling in multiple currencies.

At times, Stripe supports non-primary currencies that don’t incur a fee. See the following table for the list of supported free currencies per country:

Acquiring fees, where applicable, are based on the settlement currency. You can find these acquiring fees listed by currency on your country’s pricing page.

In some countries, you can enable settlements and payouts in additional currencies by adding one bank account per supported settlement currency. If you use multiple bank accounts, you must select a default settlement currency, which you can change at any time.

Charges that are presented in any enabled settlement currency settle without currency conversion. Payments presented in a currency that you haven’t configured an additional bank account for automatically convert to your default currency.

For example, you’re based in the United Kingdom and added both GBP and USD bank accounts, with GBP selected as the default settlement currency. USD payments (where USD is the presentment currency) are automatically paid out to the USD bank account without conversion, while payments in all other currencies are converted into GBP.

You can manage your bank accounts and default settlement currency from the Bank accounts and currencies settings in the Dashboard.

Your payout schedule determines when Stripe sends money to your bank account. You can select your preferred payout schedule during onboarding or update it any time in the Stripe Dashboard.

All payments and payouts are processed according to UTC time, except for Asia-Pacific (APAC) markets. As a result, the processed date might not be the same as your local time zone.

Choosing a payout schedule doesn’t change how long it takes for your pending balance to become available. It only controls when payouts are sent.

For example, if your account is set to daily payouts with a 3-business-day settlement timing, Stripe pays out funds daily from transactions that were captured three business days earlier.

Some countries have preset payout schedules due to local regulations:

These restrictions don’t apply if you use cross-border payouts.

If you turn off automatic payouts, you must manually send funds to your bank account. You can do this in the Dashboard or by using the API to create payouts.

Manual payouts are available in all regions except Brazil and India, where payouts are always automatic and daily. In most regions, manual payouts typically take 1-4 business days to arrive in your bank account after initiating the manual payout.

If your Stripe account that operates in the United Kingdom has a standard T+3 settlement timing and you initiate a manual payout during business hours, the funds typically arrive in your bank account on the same business day. This same-day payout is limited to 10 same-day manual payouts per day, with a maximum transaction amount of 1 million GBP each. All other manual payouts typically arrive within 2 business days in your bank account.

If your Stripe account that operates in the United States has a standard T+2 settlement timing and you initiate a manual payout during business hours, the funds typically arrive in your bank account on the same business day. This payout is subject to an account limit of 10 manual payouts per day and a maximum transaction amount of 1 million USD. All other manual payouts typically arrive within 1 business day in your bank account.

The payout schedule refers to the cadence that your funds are paid out, for example, day of the week. The settlement timing refers to the amount of time it takes for your funds to become available. Settlement timing varies per country and is typically expressed as “T+X” days. Some payment processors might start “T” from their internal settlement time, meaning when the funds land in their bank accounts.

Stripe uses “T” to refer to the transaction time, which indicates the time of the original payment confirmation or capture, and the counting starts earlier. If your Stripe account is in a country with a T+3 standard settlement timing and you use a manual payout schedule, your Stripe balance is available for payout within three business days of capturing a payment. However, if you use a daily automatic payout schedule with a T+3 speed, Stripe pays out funds daily from transactions captured 3 business days earlier.

Most banks deposit payouts into your bank account as soon as they receive them, though some might take a few extra days to make them available. The type of business and the country you’re in can also affect payout timing.

There are two definitions of days that affect settlement and payout timing:

For example, a charge created on a Saturday could have two different timings depending on which definition of day you use:

As the platform, you can set delay_days on your connected accounts. The delay applies as a business day or calendar day delay, based on the country of the connected account. The following table shows which countries apply the delay by business or calendar day.

1 Delays for Pix, Boleto, debit, and prepaid payouts in Brazil apply in business days.

2 Delays for PayNow in Singapore apply in business days.

Use the following collapsed table to determine your country’s settlement timing. The initial settlement timing applies to your first payout, and the default settlement timing applies to subsequent payouts.

In some cases, risk criteria might prevent your account from changing to the default settlement timing.

Bank debit payment methods typically have longer settlement times than card payments because of the underlying banking systems. These payments have a higher risk of returns or reversals, which factors into their longer settlement periods.

To manage your cash flow and cover potential refunds, disputes, and fees that might lead to negative balances, you can set a minimum balance in your Stripe account.

Stripe offers products and payment methods that have reduced settlement time depending on your location and are subject to eligibility criteria.

For eligible US merchants, Stripe offers faster ACH settlement that reduces the settlement time from 4 business days to 2 business days from payment creation. For more details about eligibility and activation, see the ACH support page.

With Instant Payouts, you can instantly send funds to a supported debit card or bank account. You can request Instant Payouts any time, including weekends and holidays, and funds usually appear in the associated bank account within 30 minutes. New Stripe users aren’t immediately eligible for Instant Payouts. You can check your eligibility in the Dashboard.

The minimum payout amount depends on the lowest amount we can support with our banking partners. For example, if you’re located in the US and you have less than 1 cent (0.01 of 1 dollar) USD in your Stripe account, you must wait until you accept more payments and increase your balance before you can receive a payout. If your available account balance is less than the minimum payout amount, it remains in your Stripe account until your balance increases.

If you’re in a supported country, you can use multi-currency settlement to send a payout to your local bank accounts in a foreign currency. For example, if you’re based in France, you can receive a USD payout in your French bank account, instead of paying for multiple currency exchanges.

Minimum payout amounts are typically one base unit of the local currency. See the following collapsed table for a list of countries and their minimum payout amounts:

Each payout reflects your available account balance at the time it was created. In some cases, you might have a negative account balance. For example, if you receive 100 USD in payments but refund 200 USD of prior payments, your account balance would be -100 USD. If you don’t receive further payments to balance out the negative amount, Stripe creates a payout that debits your bank account.

Your bank account must support both credit and debit transactions so that Stripe can perform any required payouts.

Use the following test bank and debit card numbers to trigger certain events when testing payouts. You can only use these values while testing with test secret keys.

Test payouts simulate a live payout but aren’t processed with the bank. Test accounts with Stripe Dashboard access always have payouts enabled, as long as valid external bank information and other relevant conditions are met, and never requires real identity verification.

You can’t use test bank and debit card numbers in the Stripe Dashboard on a live mode connected account. If you’ve entered your bank account information on a live mode account, you can still use a sandbox, and test payouts will simulate a live payout without processing actual money.

Use these test bank account numbers to test payouts. You can only use them with test secret keys.

Use these test debit card numbers to test payouts to a debit card. You can only use them with test secret keys.

If your bank account can’t receive a payout for any reason, your bank returns the funds to us. You’ll receive an error with the reason for the failure. It can take up to 5 additional business days for your bank to return the payout and inform us that it failed. If this happens, you’re notified by email and in the Dashboard. If a payout fails, make sure your bank account details are correct by re-entering them. Stripe then reattempts the payout at the next scheduled payout interval.

When a payout fails, the status might initially show as paid, but then change to failed within 5 business days.

Stripe sends the funds using the bank account information that you enter. If you provide incorrect information, such as a mistyped account number or an incorrect routing number, Stripe might send payouts to the wrong bank account and might not be able to recover the funds.

Any fees or losses that you incur because of incorrect information fall under your responsibility. If your banking details are correct and the payout failure is for other reasons, contact your bank. After you resolve any issues with your bank, you can reactivate the payouts by clicking Resume Payouts. If you don’t receive a payout from Stripe after clicking Resume Payouts, and you haven’t received a failure notification within a reasonable time frame, please contact us.

Stripe doesn’t charge you a fee to initiate normal payouts. However, most non-primary currency payouts, where you pay out money in a currency other than your Stripe account’s local currency, do incur Stripe fees.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payouts \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=5000 \
  -d currency=usd
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payouts \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=5000 \
  -d currency=usd
```

---

## Stripe Terminal mobile readers

**URL:** https://docs.stripe.com/terminal/mobile-readers

**Contents:**
- Stripe Terminal mobile readers
- Learn about Stripe's pre-certified in-person payment mobile readers.
  - Shop Now
- Reader software updates
    - Note

Ready to buy? Browse available readers and accessories.

Terminal’s mobile readers work with iOS, Android, and React Native SDKs and use Bluetooth Low Energy or USB (on Android devices only) to connect to the SDKs on a mobile device.

Stripe and our hardware partners periodically release reader software updates, which can include improvements and required security updates. Mobile readers update themselves automatically upon connection to your point of sale. You must support updating the readers from your application. Failing to install a required update can prevent a reader from accepting payments.

Mobile readers force a reboot and disconnect from the POS app 24 hours after the last boot.

---

## Mobile SDK versioning and support policy

**URL:** https://docs.stripe.com/sdks/mobile-sdk-versioning

**Contents:**
- Mobile SDK versioning and support policy
- Learn about the Mobile SDK versioning and support policy.
- Migration guides and changelog
- Support policy
- Compatibility with Stripe API versions on your backend
- See also

This page describes Stripe’s mobile SDK versioning policy, compatibility with Stripe API versions, and how to update to newer SDK versions.

The iOS SDK is open source and fully documented.

Stripe’s iOS SDK follows semantic versioning (semver). This means that version numbers are structured as MAJOR.MINOR.PATCH, where:

We recommend staying up to date with the latest SDK versions to take advantage of new features, improvements, and bug fixes.

New features and bug fixes are released on the latest major version of the SDK. If you’re on an older major version, we recommend upgrading to the latest major version to take advantage of these features and bug fixes. Older major versions of the SDK continue to be available for use, but won’t receive any additional updates.

Unless specifically noted in an SDK API, the mobile SDKs is compatible with any Stripe API version you use on your backend.

---

## Stripe Terminal Tap to Pay readers

**URL:** https://docs.stripe.com/terminal/tap-to-pay-readers

**Contents:**
- Stripe Terminal Tap to Pay readers
- Learn about Terminal's commercial off-the-shelf Tap to Pay readers.
  - Accept Payments
- Reader software updates
- Compliance

Start accepting payments in person with Tap to Pay in the Dashboard App.

Terminal’s Tap to Pay readers are compatible with the iOS, Android, and React Native SDKs.

Tap to Pay readers often initiate automatic software updates upon connecting to your point of sale system. Your application needs to support these automatic updates. Failing to install critical updates can prevent a reader from processing payments, potentially disrupting your business operations.

Stripe is committed to the security and compliance of payments processed through Tap to Pay. We have partnered directly with Apple and Google to build a solution that supports the security features of each mobile OS.

For Tap to Pay on iPhone, Apple completed an MPoC (Mobile Payments on COTS) certification as a Monolithic Solution.

For Tap to Pay on Android, Stripe is actively undergoing an MPoC evaluation, and you can see our MPoC Security Guidance.

Prior to the PCI Security Standards Council (PCI SSC) releasing the MPoC standard, Stripe completed security assessments directly with the major payment networks. These assessments demonstrated that our Tap to Pay solutions are secure and comply with all network requirements applicable to Stripe.

Stripe is a PCI Principal Participating Organization and a member of the PCI Board of Advisors, and continues to be involved with development of the MPoC standard.

---

## Refund transactions

**URL:** https://docs.stripe.com/terminal/features/refunds

**Contents:**
- Refund transactions
- Cancel or refund Stripe Terminal payments.
- Availability
- Cancel payments Client-sideServer-side
  - SDK Reference
    - Client-side
    - Note
    - Server-side
  - API Reference
- Perform refunds Server-side

Stripe Terminal supports both automatic and manual capture.

When the SDK returns a confirmed PaymentIntent to your app, the payment is authorized but not captured. You can cancel payments that are authorized and not captured. If the PaymentIntent has already been captured, you must refund the underlying charge created by the PaymentIntent, using the refunds API or Dashboard.

We recommend reconciling payments on your backend after a day’s activity to prevent unintended authorizations and uncollected funds.

Canceling payments is available on Visa, Mastercard, American Express, Discover, and girocard. For single-message payment methods like Interac and eftpos, PaymentIntents are automatically captured. In lieu of canceling PaymentIntents, make sure your application can allow initiating a refund at the end of the checkout flow.

Online refunds are available on all card networks except for Interac.

In-person refunds are only available on Interac.

You can cancel a card_present PaymentIntent at any time before it has been captured. Canceling a PaymentIntent releases all uncaptured funds, and a canceled PaymentIntent can no longer be used to perform charges.

Use this when, for example, your customer decides to use a different payment method or pay with cash after the payment has been processed. In your application’s UI, consider allowing the user to cancel after they confirm the payment, and before you finalize it and notify your backend to capture.

Cancel a PaymentIntent from your client using the iOS, Android, or React Native SDK:

Client-side PaymentIntent cancellation is possible with the iOS, Android, and React Native SDKs. If you’re using a server-driven integration, cancel the PaymentIntent server-side.

The JavaScript SDK and server-driven integration require you to cancel the PaymentIntent on your server. For the other client SDKs, you can cancel the PaymentIntent on your server if the information required to start a payment isn’t readily available in your app.

When you use a PaymentIntent to collect payment from a customer, Stripe creates a charge behind the scenes. To refund the customer’s payment after the PaymentIntent has succeeded, create a refund by passing in the PaymentIntent ID or the charge ID. You can also optionally refund part of a payment by specifying an amount.

You can perform refunds with the API or through the Dashboard. For Interac transactions in Canada, you can provide in-person refunds on the BBPOS WisePOS E reader, Stripe Reader S700, or Tay to Pay on iPhone.

Online refunds don’t require a cardholder to present their card again at the point of sale. The following example shows how to create a full refund by passing in the PaymentIntent ID.

To refund part of a PaymentIntent, provide an amount parameter, as an integer in cents (or the charge currency’s smallest currency unit):

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/payment_intents/pi_ANipwO3zNfjeWODtRPIg/cancel \
  -u "sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/payment_intents/pi_ANipwO3zNfjeWODtRPIg/cancel \
  -u "sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/refunds \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d payment_intent=pi_Aabcxyz01aDfoo
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/refunds \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d payment_intent=pi_Aabcxyz01aDfoo
```

---

## Collect and save payment details for future use

**URL:** https://docs.stripe.com/terminal/features/saving-payment-details/overview

**Contents:**
- Collect and save payment details for future use
- Use your Stripe Terminal integration to collect and save payment methods for returning customers.
- Collect and save reusable payment details
- Create a reusable PaymentMethod
- Charge a saved PaymentMethod
- Charge customers outside the checkout flow
- Track customer behavior with card fingerprints
- Compliance

Use Stripe Terminal to collect and save payment methods (including NFC-based mobile wallets) for online reuse. Use an in-person payment to initiate an online subscription using Billing, save payment details to a customer’s online account, or defer payment.

You can collect reusable payment details and save them for online use with Terminal:

When you create a PaymentIntent or SetupIntent with a card-present payment method, you can’t save the PaymentMethod directly. However, in most cases, Stripe can create a reusable generated_card PaymentMethod using the payment information. It represents the same payment method and can be reused for online payments.

You can charge customers at a later date using payment details that were saved during an earlier transaction.

Create and confirm a PaymentIntent with the saved payment method.

To save a card or mobile wallet from a Terminal PaymentIntent, attach the generated_card PaymentMethod to a Customer. This allows you to reuse it without having to collect payment details again. If you attach a PaymentMethod to a PaymentIntent without also attaching the PaymentMethod to a Customer, you won’t be able to reuse the Payment Method in future transactions.

If the customer isn’t in your checkout flow when you charge the customer, set off_session to true. This causes the PaymentIntent to throw an error if customer authentication is required.

When charging a saved card or mobile wallet, you can’t use the confirmPaymentIntent method. Payments with generated cards are online payments and can’t be processed with Terminal SDK methods.

Use the Stripe API to recognize repeat customers across online and retail channels by correlating transactions by the same card. Like card payment methods, each card_present payment method has a fingerprint attribute that uniquely identifies a particular card number. Cards from mobile wallets (for example, Apple Pay or Google Pay) don’t share a fingerprint with cards used online.

Starting with API version 2018-01-23, Connect platforms see a fingerprint on card_present and card PaymentMethods that’s uniform across all connected accounts. You can use this fingerprint to look up a specific card’s charges in a connected account.

You’re responsible for your compliance with all applicable laws, regulations, and network rules when saving a customer’s payment details. For example, the European Data Protection Board has issued guidance regarding saving payment details. These requirements generally apply if you want to save your customer’s payment method for future use. This applies in situations such as presenting a customer’s payment method to them in the checkout flow for a future purchase, or charging them when they’re not actively using your website or app, placing a MOTO order, or in your store.

Add terms to your checkout flow that state how you plan to save payment method details and allow customers to opt in. If you plan to charge the customer while they’re not actively checking out, make sure (at a minimum) that your terms also cover the following:

Make sure you keep a record of your customer’s written agreement to these terms.

When you save a payment method, you can only use it for the specific purpose that you included in your terms. If you want to charge customers when they’re not actively checking out and also save the customer’s payment method to present to them as a saved payment method for future purchases, you must explicitly collect consent from the customer. One way to do so is with a “Save my payment method for future use” checkbox.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u sk_test_YOUR_TEST_KEY_HERE: \
  -d "payment_method_types[]"="card" \
  -d "amount"=1099 \
  -d "currency"="usd" \
  -d "customer"="{{CUSTOMER_ID}}" \
  -d "payment_method"="{{PAYMENT_METHOD_ID}}"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u sk_test_YOUR_TEST_KEY_HERE: \
  -d "payment_method_types[]"="card" \
  -d "amount"=1099 \
  -d "currency"="usd" \
  -d "customer"="{{CUSTOMER_ID}}" \
  -d "payment_method"="{{PAYMENT_METHOD_ID}}"
```

---

## Incremental authorizations

**URL:** https://docs.stripe.com/terminal/features/incremental-authorizations

**Contents:**
- Incremental authorizations
- Increase the authorized amount before capturing a payment.
- Availability
    - Availability by card network and merchant category
- Request incremental authorization supportServer-sideClient-side
- Confirm the PaymentIntentClient-side
- Perform an incremental authorizationServer-side
- Capture the PaymentIntentServer-side
    - Note

Incremental authorizations allow you to increase the authorized amount on a confirmed PaymentIntent before you capture it. This is helpful if the total price changes or the customer adds goods or services and you need to update the amount on the payment.

Depending on the issuing bank, cardholders might see the amount of the original pending authorization increase in place, or they might see each increment as an additional pending authorization. After capture, the total captured amount appears as one entry.

When using incremental authorizations, be aware of the following restrictions:

Use incremental authorizations on payments that fulfill the criteria below. You can find your user category in the Dashboard.

Attempting to perform an incremental authorization on a payment that doesn’t fulfill the below criteria results in an error.

When you create a PaymentIntent, you can request the ability to capture increments of the payment. Set the request_incremental_authorization_support field to true and the capture_method to manual. This updates the text from Total to Pre-authorization in the payment collection screen.

Check the incremental_authorization_supported field in the confirm response to determine if the PaymentIntent is eligible for incremental authorization.

You can only perform incremental authorizations on uncaptured payments after confirmation. To adjust the amount of a payment before confirmation, use the update method instead.

Not all PaymentIntents are eligible for incremental authorizations. To determine whether a PaymentIntent is eligible based on the restrictions listed in the Availability section, check the incremental_authorization_supported field on the PaymentIntent’s latest charge after a successful confirmation.

To increase the authorized amount on a payment, use the increment_authorization endpoint and provide the updated total amount to increment to, which must be greater than the original authorized amount. This attempts to authorize for the difference between the previous amount and the incremented amount. Each PaymentIntent can have a maximum of 10 incremental authorization attempts, including declines.

A single PaymentIntent can call this endpoint multiple times to further increase the authorized amount.

An authorization can either:

To capture the authorized amount on a PaymentIntent that has prior incremental authorizations, use the capture endpoint. To increase the authorized amount and simultaneously capture that updated amount, provide an updated amount_to_capture.

Providing an amount_to_capture that’s higher than the currently authorized amount results in an automatic incremental authorization attempt.

If you’re eligible to collect on-receipt tips, using an amount_to_capture that’s higher than the currently authorized amount won’t result in an automatic incremental authorization attempt. Capture requests always succeed.

The possible outcomes of an incremental authorization attempt are:

Regardless, when using amount_to_capture we recommend that you always check for potential failures.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=1000 \
  -d currency=usd \
  -d "payment_method_types[]"=card_present \
  -d capture_method=manual \
  -d "payment_method_options[card_present][request_incremental_authorization_support]"=true
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=1000 \
  -d currency=usd \
  -d "payment_method_types[]"=card_present \
  -d capture_method=manual \
  -d "payment_method_options[card_present][request_incremental_authorization_support]"=true
```

Example 3 (javascript):
```javascript
async () => {
  const result = await terminal.processPayment(paymentIntent);
  if (result.error) {
    // Placeholder for handling result.error
  } else if (result.paymentIntent) {
    // Now you're ready to increment the authorization using your backend
  }
}
```

Example 4 (javascript):
```javascript
async () => {
  const result = await terminal.processPayment(paymentIntent);
  if (result.error) {
    // Placeholder for handling result.error
  } else if (result.paymentIntent) {
    // Now you're ready to increment the authorization using your backend
  }
}
```

---

## How disputes work

**URL:** https://docs.stripe.com/disputes/how-disputes-work

**Contents:**
- How disputes work
- The lifecycle of payment card disputes.
- Before the dispute
  - Early fraud warnings
    - Cases where refunding makes more sense
  - Inquiries
    - Unwinnable chargebacks
- During the dispute
  - Receive a dispute
  - Dispute timing

A dispute occurs when an account owner contacts their bank to contest a payment to you for a number of possible reasons. When someone files a dispute, the process varies slightly across different card networks, but typically follows this standard pattern:

When an account owner disputes a charge to their payment account, Stripe:

Throughout this process, Stripe facilitates your case, but doesn’t have influence over the outcome, which is at the sole discretion of the account owner’s bank.

Sometimes, Stripe alerts you to pre-dispute notifications before an actual dispute is filed. Pay attention to these notifications because:

Early fraud warnings (EFWs) are messages sourced from reports that card issuers on the Visa, Mastercard, and JCB networks generate to flag payments they suspect might be fraudulent. These include Visa TC40 reports and Mastercard’s System to Avoid Fraud Effectively (SAFE) reports. The networks require issuers to report fraud, but that requirement doesn’t affect an issuer’s decision about whether to initiate a dispute.

As with any fraud signal, EFWs don’t require any action or response from you. You can proactively refund the charge to prevent the cardholder from initiating a dispute, or you might wait and see if a fraud dispute happens. Unless the payment was covered by the liability shift rule, 80% of EFWs convert into a fraud dispute if you do nothing. If the payment was covered by liability shift, then you might still receive a dispute. In that case, Stripe automatically provides some evidence for you, such as data from 3D Secure.

Automatically refunding all EFWs regardless of the likelihood of escalation isn’t a good strategy. If you’re too aggressive in issuing refunds for all EFWs, you’ll inevitably refund some transactions that would never have become disputes.

All other things being equal, our analysis suggests that the optimal point for issuing a refund on early fraud warnings is on charges that are roughly less than or equal to your dispute fee. It’s likely not worthwhile to refund EFWs on charges more than 35 percent higher than your dispute fee.

Proactively refunding a flagged payment doesn’t affect the fraud warning. The only time a refund can prevent a fraud report is when it’s processed as a reversal, which usually happens within 2 hours of the payment capture.

Although it’s called an early fraud warning, it’s possible to receive an EFW even after you receive a fraud dispute on a charge. This is generally because the systems the networks use to process EFWs are separate from the systems they use to process disputes, and the two aren’t necessarily in sync. Note that you can listen for EFW webhooks using our API.

The main exception to the optimal refund strategy previously described is if you have reason to worry about the effect of the dispute itself on your business or account.

If any of the conditions described under the Best practices for preventing fraud apply to your situation, it makes sense to more aggressively refund EFWs.

Some card networks initiate a preliminary phase before creating a formal dispute, and chargeback. Stripe calls this preliminary phase an inquiry, though these are sometimes also called a “retrieval” or a “request for information.” American Express and Discover are the networks that most often use this phase, while Mastercard and Visa no longer use it. Note that Mexico Domestic charges that are disputed across card brands use inquiries before creating a formal dispute. If left unanswered, some disputes might escalate to unwinnable chargebacks.

During the inquiry phase, the cardholder’s bank requests transaction clarification, often because the cardholder doesn’t recognize the transaction description. You can resolve the case without incurring a dispute fee by either:

Inquiries on partially refunded charges can still escalate to a chargeback.

Failing to respond to an inquiry can signal to the issuer your implicit acceptance of the claim, resulting in an escalation to a formal, and likely unwinnable, chargeback. Unless you intend to accept financial liability, always respond to inquiries immediately, making every effort to amicably resolve issues with your customer during this stage.

The Dashboard payment page describes inquiries as an inquiry or dispute inquiry. In the API events summary, they’re described as a warning or dispute warning to mirror the language in the API.

If an inquiry remains open for 120 days without escalating to a chargeback, Stripe marks it as closed in both the Dashboard and API. At this point, the card network won’t escalate it. Card networks don’t provide an explicit “win” message for inquiries.

When an account owner files a formal dispute against a payment, whether due to an escalated inquiry or for another reason, it initiates a chargeback. During this process:

To learn why the debited amount might differ from the original payment, see disputed amounts.

The initiation of a dispute triggers several processes:

Card networks typically allow cardholders to initiate disputes within 120 days of the original payment, but their rules allow more time in some situations. Certain industries, such as travel or event ticketing, are prone to longer intervals between the original purchase and a dispute. Generally, when a customer pays for a future event or service (like a vacation reservation, professional services appointment, or event ticket), the dispute window starts on the event date, not the payment date.

After a chargeback is created, you have a limited time to respond to the card issuer: usually 7-21 days, depending on the card network.

If you submit evidence, the issuer has a limited time to evaluate it and decide the outcome: usually 60-75 days, depending on the card network.

The full dispute lifecycle, from initiation to the final decision, can take 2-3 months to complete. You can’t reliably accelerate this timeline, except by accepting the dispute in the Dashboard or API.

At the end of the dispute process, the issuer either:

Overturns the dispute in your favor:

Upholds the dispute in their cardholder’s favor:

The dispute fees for your country can be found on Stripe’s Pricing page. The fee for receiving a dispute is deducted from your account balance when a cardholder initiates a dispute. Dispute fees vary based on your business location:

If you counter a dispute, a dispute countered fee applies, in addition to the dispute received fee. The cardholder’s bank reviews it and decides the dispute outcome. This can take up to 3 months. When Stripe receives the decision, you receive an email from us.

Stripe returns the dispute countered fee if you win the dispute. Unless otherwise stated in your Stripe contract, we never return the dispute received fee.

The dispute countered fee doesn’t apply to businesses in Mexico and Japan.

In most cases, you have the ability to challenge a disputed payment, as long as you submit strong evidence to the card issuer that invalidates the dispute claim before the deadline.

As soon as a dispute is active, the only way to overturn it is by submitting evidence in a response. Even in cases where your customer claims to have withdrawn the dispute, you must respond with evidence for the dispute to be closed in your favor. Submitting evidence is what signals to the issuer that you don’t accept the dispute and want to have the funds returned to you.

See Respond to disputes for information on how to:

You can’t challenge some types of disputes under the rules of the card network they were processed on or due to local regulations. In general, Stripe immediately closes them as lost as soon as we notify you about them, and you have no opportunity to present evidence to the issuer.

The Dashboard payment page and timeline describes these disputes as those where the card issuer doesn’t allow you to submit evidence.

Inquiries for Discover cards can turn into unchallengeable disputes if you don’t submit evidence for the inquiry.

The Cartes Bancaires network requires a higher standard of evidence from the cardholder before allowing them to initiate a dispute, but then prohibits you from challenging the dispute. This affects only businesses in the Single Euro Payments Area (SEPA) processing payments on the Cartes Bancaires network, and not businesses elsewhere charging cards issued by Cartes Bancaires. Learn more at Cartes Bancaires.

In extremely rare cases, you might receive more than one dispute per payment. This can happen when a customer files a new dispute with a different reason code, for a new line item in the original transaction, on multi-capture payments or simply because the issuer acquired new information about the payment allowing them to refile a dispute.

Handle each dispute the same way as any other dispute; each dispute requires you to either accept or counter the dispute. Pay special attention to the outlined amount, currency, category, and claim details before managing the dispute.

A disputed amount might be lower or higher than the amount of the original charge. The following table outlines some of the most common reasons for this difference:

After you submit your evidence, the next notification from the card issuer to both Stripe and you is the final decision. As soon as the issuer makes its decision, Stripe updates the status of the dispute to won or lost, notifying you through the Dashboard, email, and any other communication channels you configured.

This outcome is final for all parties. Neither you nor your customer can overturn a lost dispute. However, a customer can withdraw a dispute, even after a loss.

Stripe doesn’t support the arbitration phase for disputes, which means that you can’t escalate disputes to arbitrators through our platform.

Although the outcome of a dispute is normally final, in rare cases the status can change from lost to won. When this occurs, Stripe labels the dispute as a late win and returns the funds to your balance. These late-win results happen when issuers credit or debit Stripe for a dispute outside of the regular dispute lifecycle. They might do this to handle money movement or to correct amounts or decisions. Because late wins are driven by the issuer, Stripe can’t predict when or why they happen.

---

## Disputes

**URL:** https://docs.stripe.com/disputes

**Contents:**
- Disputes
- Learn about disputes, how they work, and what you can do to prevent them.
- Handle disputes
- Analyze disputes
- Automate dispute management

A dispute (also known as a chargeback) occurs when a cardholder questions your payment with their card issuer.

To process a chargeback, the issuer creates a formal dispute on the card network, which immediately reverses the payment. This pulls the money for the payment—as well as one or more network dispute fees—from Stripe. After that, Stripe debits your balance for the payment amount and dispute fee.

To help our users submit the best possible response for each dispute, Stripe guides you through the process within the Dashboard. Here, you can provide the appropriate text and images for the dispute reason, and your counterargument. If you need help with a dispute, contact support.

Learn how to challenge or accept a dispute.

Learn about reason code categories and broad evidence guidelines.

Refer to common Visa, Mastercard, and American Express reason codes.

Learn about the issues that can occur from excessive disputes, and how to avoid them.

Learn about the monitoring programs operated by the card networks.

Automatically prevent disputes and lower your dispute rate.

Use Smart Disputes to automate the evidence collection and submission process for eligible disputes.

---

## Collect tapped data for NFC instrumentsPrivate preview

**URL:** https://docs.stripe.com/terminal/features/collect-nfc-data

**Contents:**
- Collect tapped data for NFC instrumentsPrivate preview
- Use Terminal for data collection of NFC instruments with the reader hardware interfaces.
    - Private preview
    - Warning
- Collect data
  - SDK Reference
    - Note

Request access to the Collect data private preview by sending an email to terminal-collect-data@stripe.com. Provide your use case, Terminal device, and integration type.

Use the Terminal SDK and the reader’s contactless interface to read the unique identifier (UID) of NFC instruments, such as cards or wristbands. This feature is available offline.

After tapping your NFC instrument, the Terminal SDK provides a collected data object with the NFC UID, or an error if one occurred.

You can’t use this feature to collect card payments. Follow these instructions to collect payments using Stripe Terminal.

Collecting tapped data for NFC instruments is available in:

Use Terminal.collectData() to prompt for data collection from your point-of-sale application. Specify the type of collected data you want to receive, such as .nfcUid, in a configuration passed to the function. After a customer taps an NFC instrument, the SDK collects a data object with the NFC UID or returns an error if the read is unsuccessful.

On supported readers, the ability for customers to cancel transactions is now enabled by default. To disable customer cancellation on smart readers, set customerCancellation to .disableIfAvailable.

**Examples:**

Example 1 (javascript):
```javascript
import UIKit
import StripeTerminal

class PaymentViewController: UIViewController {
    func readNfcUid() throws {
        let config = try CollectDataConfigurationBuilder().setCollectDataType(.nfcUid).build()
        self.cancelable = Terminal.shared.collectData(config) { collectedData, collectError in
            if let error = collectError {
                // Placeholder for handling exceptions
            } else if let nfcUid = collectedData?.nfcUid {
                // Placeholder for receiving NFC UID
                print("NFC UID is: \(nfcUid)")
            }
        }
    }
}
```

Example 2 (javascript):
```javascript
import UIKit
import StripeTerminal

class PaymentViewController: UIViewController {
    func readNfcUid() throws {
        let config = try CollectDataConfigurationBuilder().setCollectDataType(.nfcUid).build()
        self.cancelable = Terminal.shared.collectData(config) { collectedData, collectError in
            if let error = collectError {
                // Placeholder for handling exceptions
            } else if let nfcUid = collectedData?.nfcUid {
                // Placeholder for receiving NFC UID
                print("NFC UID is: \(nfcUid)")
            }
        }
    }
}
```

---

## Community SDKs

**URL:** https://docs.stripe.com/sdks/community

**Contents:**
- Community SDKs
- Browse the community SDKs available for a Stripe integration.

You can use the following open-source, community-supported libraries. However, Stripe doesn’t support or review them for accuracy or completeness.

---

## Stripe versioning and support policy

**URL:** https://docs.stripe.com/sdks/versioning

**Contents:**
- Stripe versioning and support policy
- Learn about Stripe's versioning and support policy.
- Stripe API versions
  - Organization API keys
- Stripe SDK versions
- Stripe SDK support policy
  - Migration guides
- Stripe SDK language runtime version support policy
    - Warning
  - Language policies

Starting with the 2024-09-30.acacia release, Stripe follows a new API release process where we release new API versions monthly with no breaking changes. Twice a year, we issue a new release (for example, acacia) that starts with an API version that will have breaking changes.

You can expect new minor versions of the SDKs with each monthly API version and new major versions of the SDKs with each of the twice a year major releases.

You might sometimes see a major version update to the SDKs coincide with the monthly API version updates. This happens when the SDKs need to ship a breaking change.

The current version of the API is 2025-12-15.clover.

To understand what to expect from a new API version, see API upgrades.

All API requests made with an organization API key must include the Stripe-Version header to ensure consistency and predictability across your organization’s integrations.

Stripe’s SDK versioning policy is based on the semantic versioning standard. For example, in version 4.3.2, 4 is the major, 3 is the minor, and 2 is the patch. When we release a new SDK version for new features or bug fixes, we increment one of these three version components depending on the type of change introduced.

Each SDK version uses the API version that is current at the time of its release to make API requests. Refer to the versioning page to see how to override this.

New features and bug fixes are released on the latest major version of the SDK. If you’re on an older major SDK version, we recommend upgrading to the latest major version to take advantage of these features and bug fixes. Older major versions of the package continue to be available for use, but won’t receive any additional updates.

We provide migration guides to help you upgrade from older major SDK versions. You can find them in the wiki section of our SDK GitHub repositories. The same wiki also has the mapping between SDK major versions and the API versions.

When a language runtime version reaches its end of life, we mark it as “deprecated” in the tables below and begin its extended support window. The exact length of the extended support window varies by language, but the range is 1 to 2 years.

After the extended support window for a language version ends, the following major version of the SDK will no longer support that language version. However, previous versions of the SDK will still be compatible with those older language versions. We’ll pre-announce all runtime deprecations on this page, in each SDK’s README, and in each language’s changelog.

Though an SDK might continue to work on an unsupported language version, don’t continue to use it. SDKs that run on unsupported versions might break unexpectedly in any release, and the cause of that breakage might not be included in the changelog.

Python 3.10 reaches end of life in October 2026. We’ll keep supporting it for the March and September 2027 API releases. We’ll remove support for it in the March 2028 major release.

We support Python 3.7+. This includes all versions of Python that are currently receiving security support, plus those within the extended support window.

Python versions that have reached their end of life dates will begin an extended support window of 1 year (two major API releases). We’ll drop support for the oldest supported Python version with the March API release every year.

Here’s the deprecation schedule:

We have a public preview release channel, which uses preview API versions that are distinct from general availability (GA) versions. For example, 2025-04-30.preview instead of 2025-04-30.basil. The current preview API version is 2025-12-15.preview.

To access the new features and enhancements in the preview stage, use versions of our SDKs that have the beta or b suffix. For example, 5.1.0b3 in Python and 5.1.0-beta.3 in other language SDKs.

For installation instructions and details about passing preview headers in the Stripe-Version header, see the Public Preview SDKs section in the README files in the respective SDK GitHub repositories.

We also publish features in the private preview phase that require invite-only access. These features also use the preview API versions.

To access private preview features and enhancements after invitation, use versions of our SDKs that have the alpha or a suffix. For example, 5.1.0a3 in Python and 5.1.0-alpha.3 in other language SDKs.

For installation instructions and details about passing preview headers in the Stripe-Version header, see the Private Preview SDKs section in the README files in the respective SDK GitHub repositories.

---

## Respond to disputes

**URL:** https://docs.stripe.com/disputes/responding

**Contents:**
- Respond to disputes
- Learn how to challenge or accept a dispute in the Dashboard.
- Automatically manage disputes in the Dashboard
- Review the dispute category
  - Inquiries
    - Note
  - Visa compliance disputes
    - Note
  - Fraudulent disputes
    - Visa CE 3.0 Eligibility

A dispute occurs when an account owner contacts their bank to contest a payment to you for a number of possible reasons. When an account owner files a dispute against a payment, their bank alerts Stripe. We then notify you through the following channels:

Each of these notification channels provides a link to the Dispute details page in the Dashboard, where you can learn more about the reason for the dispute and take appropriate action. When you receive a dispute notification, take action to resolve it before the deadline (usually 7 to 21 days depending on the card network). If you don’t respond before the deadline, you automatically lose the dispute and can’t retrieve the disputed funds. You can see a detailed list of all your disputes in the Disputes tab.

If you want to manage disputes programmatically instead of using the Dashboard, you can use the API.

The following methods describe how you can automate the management of disputes-related tasks in the Dashboard.

When you get a dispute, you can see the corresponding category or reason in your Dashboard and see the same information as the reason attribute for the Dispute object.

Each dispute category specifies different response requirements and recommendations to appropriately respond to the root claim of the cardholder. Your first step is to review our response guidelines for the dispute category. This helps you collect the best evidence to counter the dispute claim.

To review to a dispute, open its details page by selecting the applicable dispute in the list. If you use Organizations, the detailed list of disputed payments includes all your accounts. You can filter this list by account. In this view, you can also respond to disputes across any account.

Inquiries appear as disputed payments in the Dashboard, but they actually represent a pre-dispute stage that’s typically issued when an account owner doesn’t recognize a transaction on their account. Respond in this stage to resolve any questions and prevent a formal dispute escalation, which saves you time, fees, and your rating with the card networks.

If an inquiry escalates to a chargeback, you must submit another response for the dispute.

Businesses receive Visa compliance disputes in certain cases when the card issuer believes the disputed transaction doesn’t conform to Visa’s network rules. If Visa compliance disputes can’t be resolved between the parties, the network resolves the dispute in exchange for a fee.

If you contest a Visa compliance dispute, Stripe collects a 500 USD (or local equivalent) amount in addition to the applicable Stripe dispute fee or fees. This amount covers the network costs associated with resolving Visa compliance disputes. Stripe refunds the 500 USD network fee if you win the dispute. Learn how to respond to Visa compliance disputes using the API.

Compliance cases filed by issuers are referred to as pre-compliance disputes by Visa. To learn more, see Visa rules.

To help you navigate fraudulent disputes, Stripe offers Visa CE 3.0 Eligibility and liability shift.

For fraudulent disputes with the Visa 10.4 (Card absent fraud) code, Stripe automatically evaluates your transaction history to determine eligibility with Visa Compelling Evidence 3.0. If your dispute is eligible, we notify you in the Dashboard and in the dispute email. In these cases, we encourage submitting evidence, because this eligibility typically translates to a significantly higher likelihood of overturning the dispute in your favor.

For fraudulent disputes that might be covered by the liability shift rule, Stripe automatically provides most of the evidence, such as the Electronic Commerce Indicator (ECI) from 3D Secure.

When possible, the Dispute details page provides you with a copy of the bank’s submission to Stripe based on the account owner’s claim. These are actual documents attached by card networks and can provide additional information about the disputed transaction, such as a text description from the account owner describing the specific complaint. When responding to the dispute, make sure to properly address the issue described in these files.

If the dispute is still open and the bank has provided these files, select Review the claim details under step 1 of the checklist modal in the Dashboard to view them.

The Dispute details page might also provide you with a way to email the account owner. We recommend contacting them, as it might give you insight to better understand the complaint and help you decide how to proceed. Be sure to keep a record of all communication with your customer during this process, as it provides evidence to submit with your response.

When you have a clear picture of the dispute details, decide whether to accept or challenge the dispute. If you prefer to handle disputes programmatically, use the API to respond to disputes. Always address a formally disputed payment through this process. The issuing bank has already refunded the account owner, and it’s the only way you can attempt to retrieve the disputed funds. Consider the following in your determination:

Make sure the account owner’s claim is valid. If it’s not, gather the evidence required to disprove the claim.

See if you can convince the account owner to withdraw their dispute if you resolve their complaint amicably. For example, you could offer a store credit or a replacement item.

Check to see if the dispute is CE 3.0 Eligible. If it is, consider responding because Stripe provides most of the required evidence from your transaction history.

Check to see if the dispute is covered by the liability shift rule. If it is, consider responding with evidence on top of what Stripe automatically provides, such as the 3D Secure outcome.

When you’ve decided how to respond, select the corresponding button on the Dispute details page in the Dashboard:

Accept dispute: Submits a response to the issuing bank affirming that you aren’t contesting the refunded amount.

Counter dispute: Opens a form that guides you through the submission process, prompts you for evidence relevant to both the dispute and response type, and allows you to upload supporting files.

If you counter a dispute, a dispute countered fee applies, in addition to the dispute received fee. The cardholder’s bank reviews it and decides the dispute outcome. This can take up to 3 months. When Stripe receives the decision, you receive an email from us.

Stripe returns the dispute countered fee if you win the dispute. Unless otherwise stated in your Stripe contract, we never return the dispute received fee.

The dispute countered fee doesn’t apply to businesses in Mexico and Japan.

You have only one opportunity to submit your response. Stripe immediately forwards your response and all supporting files to the issuing bank. You can’t edit the response or submit additional files, so make sure you’ve assembled all your evidence before you submit.

Open the dispute response form: Click Counter dispute to open the Stripe dispute response form.

Tell us about the dispute: In the first page of the form, tell us why you believe the dispute is in error and the product type of the original purchase. This information, along with the dispute category, helps Stripe recommend the most relevant evidence to support your challenge on the next page of the form. For example, you don’t need to provide shipping details for an online service. When your integration supports it, Stripe automatically captures the product type based on the original payment.

Assemble your evidence: The second page of the form has a dynamic set of sections representing the most relevant details you can provide for your individual case.

In the Supporting Files section, use the File Upload tool to attach evidence that matches the checklist of evidence types relevant to your dispute type and counter argument. For each uploaded file, specify which type of evidence it satisfies. You can only submit one file per type of evidence, so if you have several files representing one type of evidence, combine them into a single, multi-page file.

Consider the following guidelines to make sure your supporting files are effective:

Consult the evidence recommendations for your specific dispute category.

For fraudulent disputes in particular, if your dispute is Visa CE 3.0 eligible, look for the Required for CE 3.0 badge throughout the response form. In most cases, Stripe pre-populates these fields with the required data from your transaction history.

If your dispute might be covered by the liability shift rule, we populate 3D Secure information such as the Electronic Commerce Indicator (ECI) automatically for you.

Organize each piece of evidence according to the evidence type it satisfies—be as succinct as possible.

Combine items of the same evidence type into a single file.

Limit your evidence file size to the combined maximum of 4.5 MB.

Limit your Mastercard evidence file length to the combined maximum of 19 pages.

Banks evaluating the dispute won’t review any external content, so don’t include:

Background evidence: The other sections of the second page vary depending on the dispute type and your answers on the first page. When your integration supports it, Stripe automatically captures the data for these sections and pre-populates both the API evidence object attributes and the form fields in the Dashboard. If any of these fields aren’t pre-populated, include as much information as you can before you submit your response. These sections can include:

The more information your integration collects and passes to Stripe when your customer makes a payment, the better your ability to prevent disputes and fraud from occurring, and challenge them effectively when they do.

Submit evidence: Click the checkbox to acknowledge your understanding that your response is final. After you submit it, Stripe automatically puts the evidence you provide into a format accepted by the issuing bank and submits it for consideration. At this point, you can’t amend what you’ve submitted or provide any additional information, so make sure to include every relevant detail.

In some cases, you might have multiple disputes associated with a single payment. If this occurs, consider responding to each dispute individually.

After you submit a response, the status of the dispute changes to under review. When the issuer informs Stripe of its decision, we inform you of the outcome by email, in the charge.dispute.closed event, and by updating the dispute status in the Dashboard and the Dispute API object to one of the following:

won: Indicates that the bank decided in your favor and overturned the dispute. In this case, the issuing bank returns the debited chargeback amount to Stripe, and Stripe passes this amount back to you. For businesses in Mexico, the dispute fee might also be returned. Otherwise, the dispute fee isn’t returned.

lost: Indicates that the bank decided in the account owner’s favor and upheld the dispute. In this case, the refund is permanent and the dispute fee isn’t returned.

In some cases, the bank provides additional details about the dispute decision. Select View issuing bank response under Relevant documents in the dispute details to view them.

---

## Stripe SDKs

**URL:** https://docs.stripe.com/sdks

**Contents:**
- Stripe SDKs
- Libraries and tools for interacting with your Stripe integration.
- Server-side SDKs
- Web SDKs
- Mobile SDKs
- Community SDKs
- Stripe versioning
- Stripe OpenAPI specification

Stripe provides several SDKs and libraries to help you integrate with Stripe’s APIs across different platforms and languages. Whether you’re building a server-side application, a web frontend, or a mobile app, you can use our official libraries to securely interact with Stripe, reduce boilerplate code, and access the latest features.

We use the semantic versioning standard for SDKs, and version APIs by release date. Breaking API changes increase the SDK’s major version.

---

## Display cart details

**URL:** https://docs.stripe.com/terminal/features/display

**Contents:**
- Display cart details
- Dynamically update cart details on the reader screen.
- Set the reader display
  - SDK Reference
- Pre-dip a card
    - Note
- Pre-dip disabled

The built-in screen of the Verifone P400, BBPOS WisePOS E and Stripe Reader S700 can display line items. During the checkout process, you can update the reader’s screen to show individual items in the transaction, along with the total price.

To display the line items and total on the reader, call setReaderDisplay before processing the payment and pass the information in the cart parameter.

The amounts passed to the setReaderDisplay method are only used for display purposes. The reader won’t automatically calculate tax or the total—your application must calculate the tax and total before displaying the values. You can use the Stripe Tax API to calculate taxes. Similarly, the total passed to setReaderDisplay doesn’t control the amount charged to the customer. Make sure the amount displayed on the reader matches the amount you’re charging your customer.

To clear reader display on the server-driven integration, call the cancel_action endpoint.

Pre-dipping a card is only supported for payments in the US.

The Verifone P400, BBPOS WisePOS E, and Stripe Reader S700 support the ability to present a card to the reader before the transaction amount is finalized.

This option—known as pre-dip, pre-tap, or pre-swipe—can help speed up transaction times by allowing a customer to present a payment method before the end of the transaction.

The setReaderDisplay method prepares the reader for pre-dipping. Your customer can present a payment method at any point after this method is called. You can call setReaderDisplay multiple times to update the information displayed without impacting the pre-dipping process. Updating the display doesn’t invalidate a pre-dip, if one has already occurred.

Pre-dipping allows your customer to present a card early in the payment process without completing the associated transaction. Instead, the reader captures the presented payment method and saves it to use later, although Stripe doesn’t provide updates or events to indicate that the customer pre-dipped their card. You can process the transaction normally. For example, you can create and process a PaymentIntent to complete the transaction without special handling.

If pre-dip isn’t available in your country, the screen shows only the subtotal and line items.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/readers/tmr_xxx/set_reader_display \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d type=cart \
  -d "cart[line_items][0][description]"="Caramel latte" \
  -d "cart[line_items][0][amount]"=659 \
  -d "cart[line_items][0][quantity]"=1 \
  -d "cart[line_items][1][description]"="Dozen donuts" \
  -d "cart[line_items][1][amount]"=1239 \
  -d "cart[line_items][1][quantity]"=1 \
  -d "cart[currency]"=usd \
  -d "cart[tax]"=100 \
  -d "cart[total]"=1998
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/readers/tmr_xxx/set_reader_display \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d type=cart \
  -d "cart[line_items][0][description]"="Caramel latte" \
  -d "cart[line_items][0][amount]"=659 \
  -d "cart[line_items][0][quantity]"=1 \
  -d "cart[line_items][1][description]"="Dozen donuts" \
  -d "cart[line_items][1][amount]"=1239 \
  -d "cart[line_items][1][quantity]"=1 \
  -d "cart[currency]"=usd \
  -d "cart[tax]"=100 \
  -d "cart[total]"=1998
```

---
