# Stripe - Getting Started

**Pages:** 21

---

## Tap to Pay

**URL:** https://docs.stripe.com/terminal/payments/setup-reader/tap-to-pay

**Contents:**
- Tap to Pay
- Learn how to accept contactless payments on a compatible iPhone or Android device.
    - Note
  - Availability
    - Note
  - Availability in Public preview
- Get started
  - Entitlements and build file
- Supported devices
    - Note

Looking for a no-code solution? Accept payments from the Stripe Dashboard mobile app.

Use Tap to Pay on iPhone to accept in-person contactless payments with a compatible iPhone.

Tap to Pay on iPhone includes support for Visa, Mastercard, American Express contactless cards, and NFC-based mobile wallets (Apple Pay, Google Pay, and Samsung Pay). PIN entry is supported. Additionally, Discover is supported in the US, Interac is supported in Canada, and eftpos is supported in Australia. Stripe includes Tap to Pay on iPhone in the Terminal iOS SDK and the Terminal React Native SDK, and enables payments directly in your iOS mobile app.

For platforms, use of Tap to Pay on iPhone is subject to the Apple Acceptance Platform User Terms and Conditions.

Tap to Pay on iPhone isn’t available in Puerto Rico.

Tap to Pay on iPhone introduces an SCPDiscoveryMethodTapToPay discovery option and a connectReader method. Integrate the latest version of the Terminal iOS SDK to include the latest bug fixes and features. You can view version-specific updates and bug fixes in the SDK changelog.

Device and minimum SDK version requirements can change due to updated compliance requirements or security vulnerabilities. To make sure your solution is up to date with Tap to Pay requirements, please subscribe to terminal-announce@lists.stripe.com.

To enable Tap to Pay in your iOS application:

To use Tap to Pay on iPhone to accept payments in your application, you must first request and configure the Tap to Pay on iPhone development entitlement from your Apple Developer account. After you complete internal testing, you must request a distribution entitlement.

After you add the development entitlement file to your app build target, add the following:

Implementing Tap to Pay on iPhone is a complex process that requires submitting your app to Apple for approval. For detailed instructions, you can download our guide: Tap to Pay Guide (PDF)

Tap to Pay requires an iPhone XS or later running a one-year or later iOS version. Apple’s Business Register documentation lists supported iOS versions. Advise your users to update to the latest iOS version for the best performance.

Tap to Pay won’t work on beta releases of iOS.

Some contactless card transactions above certain amounts might require additional cardholder verification methods (CVM) such as PIN entry. Tap to Pay on iPhone supports PIN entry for devices running iOS 16.4 or later.

NFC wallet payments (Apple Pay, Google Pay, and Samsung Pay) usually don’t require a PIN. However, in the UK, Canada, and Finland, regional requirements and card issuer policies can affect contactless payments.

In the UK, depending on the issuer, Strong Customer Authentication might require some cards to be inserted into a device. In such cases, if the card isn’t inserted, the payment is declined before the PIN screen appears, with the reason offline_pin_required.

In Canada and Finland, many issued cards are offline PIN only, meaning that entering the PIN requires physical contact, such as insertion into a device, which isn’t supported with Tap to Pay.

In these scenarios, we recommend asking the customer to try a different card or collecting payment in a different way. For example, using a Terminal card reader or sending a Payment Link.

When collecting payment with your mobile device, hold the card to the reader until it reads the chip information. You might need to wait a few seconds after the initial vibration when the card makes contact. In the event of a decline, use another method to collect payment, such as a Terminal card reader. You can only have one active connection to a reader at a time.

To test PIN entry in markets where PIN is accepted, use physical test cards with amounts ending in .03. In markets where PIN isn’t accepted, a transaction ending in .03 returns an online_or_offline_pin_required error code after the card is tapped, instead of allowing the user to test PIN entry.

Follow the Human Interface Guidelines for Tap to Pay on iPhone to ensure of an optimal user experience and successful review process with Apple.

Consider the following:

---

## 

**URL:** https://docs.stripe.com/checkout/quickstart

---

## Developer resources

**URL:** https://docs.stripe.com/development

**Contents:**
- Developer resources
- Learn how to use SDKs, API keys, and integration tools.
- Versioning
- Essentials
- Tools
- Features
- AI solutions
- Security and privacy
- Extend Stripe
- Partners

Before you begin, set up your development environment.

Use the Stripe libraries and tools to build and manage your integration.

Review breaking changes and new features.

Keep track of changes and upgrades to the Stripe API.

Learn how Stripe versions its APIs and SDKs.

Use client, server, and UI SDKs to integrate with Stripe.

Use the API to authenticate requests and respond to errors.

Test your integration by simulating payments.

Debug, manage, and grow your Stripe integration.

View API request and event activity.

Build, test, and use Stripe inside Visual Studio Code.

Learn how to automate workflows without code in the Dashboard.

Send events from Stripe to webhook endpoints and cloud services.

Monitor the health of your API integrations through automated alerts.

Use Stripe to run your agent business and enhance your agents’ functionality.

Use a large language model (LLM) to help you build and manage a Stripe integration.

Use our MCP server to let your AI agents interact with Stripe.

Learn how Stripe handles security.

Remove data from your Dashboard and API.

Extend Stripe with third-party services or embed custom user experiences in the Stripe Dashboard.

Use apps to integrate with Stripe.

Join the community of Stripe partners that helps businesses with payments and financial infrastructure.

Become a Stripe-certified architect or developer.

---

## Set up your development environment

**URL:** https://docs.stripe.com/get-started/development-environment

**Contents:**
- Set up your development environment
- Get familiar with the Stripe CLI and our server-side SDKs.
  - Not a developer?
    - Chrome extensions
- What you learn
- Set up the Stripe CLI
  - Install
  - Authenticate
  - Confirm setup
- Manage third-party dependencies

Check out our no-code docs, use a prebuilt solution from our partner directory, or hire a Stripe-certified expert.

Stripe’s server-side SDKs and command-line interface (CLI) allow you to interact with Stripe’s REST APIs. Start with the Stripe CLI to streamline your development environment and make API calls.

Use the SDKs to avoid writing boilerplate code. To start sending requests from your environment, choose a language to follow a quickstart guide.

We recommend you build your payment integration with Stripe (such as Elements or Checkout) on your own website. Then, set up your Chrome extension to send users to this payment page when they’re ready to complete a purchase.

This method is more secure and easier to maintain than trying to handle payments directly within the extension.

In this quickstart, you install the Stripe CLI—an essential tool that gets you command line access to your Stripe integration. You also install the Stripe Ruby server-side SDK to get access to Stripe APIs from applications written in Ruby.

In this quickstart, you’ll learn:

First, create a Stripe account or sign in.

From the command-line, use an install script or download and extract a versioned archive file for your operating system to install the CLI.

To install the Stripe CLI with homebrew, run:

This command fails if you run it on the Linux version of homebrew, but you can use this alternative or follow the instructions on the Linux tab.

Log in and authenticate your Stripe user account to generate a set of restricted keys. To learn more, see Stripe CLI keys and permissions.

Press Enter on your keyboard to complete the authentication process in your browser.

Now that you’ve installed the CLI, you can make a single API request to Create a product.

Look for the product identifier (in id) in the response object. Save it for the next step.

If everything worked, the command-line displays the following response.

Next, call Create a price to attach a price of 30 USD. Swap the placeholder in product with your product identifier (for example, prod_LTenIrmp8Q67sa).

If everything worked, the command-line displays the following response.

We recommend managing third-party dependencies using the RubyGems command-line tool, which allows you to add new libraries and include them in your Ruby projects. Check whether RubyGems is installed:

If you get gem: command not found, download RubyGems from their downloads page.

The latest version of the Stripe Ruby server-side SDK is v18.0.0. It supports Ruby versions 2.3+.

Check your Ruby version:

Create a gem file and install the generated gem using a bundler with RubyGems.

Add the latest version of the Stripe gem to a project:

Install the required gems from your specified sources:

Now that you have the Ruby SDK installed, you can create a subscription Product and attach a Price with a couple API requests. We’re using the product identifier returned in the response to create the price in this example.

This sample uses the default keys of your Stripe user account for your sandbox environment. Only you can see these values.

Save the file as create_price.rb. From the command line, cd to the directory containing the file you just saved and run:

If everything worked, the command line shows the following response. Save these identifiers so you can use them while building your integration.

This wraps up the quickstart. See the links below for a few different ways to process a payment for the product you just created.

**Examples:**

Example 1 (unknown):
```unknown
brew install stripe/stripe-cli/stripe
```

Example 2 (unknown):
```unknown
brew install stripe/stripe-cli/stripe
```

Example 3 (unknown):
```unknown
brew install stripe-cli
```

Example 4 (unknown):
```unknown
brew install stripe-cli
```

---

## Setup Intents

**URL:** https://docs.stripe.com/api/setup_intents

**Contents:**
- Setup Intents
- The SetupIntent object
  - Attributes
    - idstringretrievable with publishable key
    - automatic_payment_methodsnullable object
    - client_secretnullable stringretrievable with publishable key
    - customernullable stringExpandable
    - customer_accountnullable string
    - descriptionnullable stringretrievable with publishable key
    - last_setup_errornullable objectretrievable with publishable key

A SetupIntent guides you through the process of setting up and saving a customer’s payment credentials for future payments. For example, you can use a SetupIntent to set up and save your customer’s card without immediately collecting a payment. Later, you can use PaymentIntents to drive the payment flow.

Create a SetupIntent when you’re ready to collect your customer’s payment credentials. Don’t maintain long-lived, unconfirmed SetupIntents because they might not be valid. The SetupIntent transitions through multiple statuses as it guides you through the setup process.

Successful SetupIntents result in payment credentials that are optimized for future payments. For example, cardholders in certain regions might need to be run through Strong Customer Authentication during payment method collection to streamline later off-session payments. If you use the SetupIntent with a Customer, it automatically attaches the resulting payment method to that Customer after successful setup. We recommend using SetupIntents or setup_future_usage on PaymentIntents to save payment methods to prevent saving invalid or unoptimized payment methods.

By using SetupIntents, you can reduce friction for your customers, even as regulations change over time.

Related guide: Setup Intents API

Unique identifier for the object.

Settings for dynamic payment methods compatible with this Setup Intent

The client secret of this SetupIntent. Used for client-side retrieval using a publishable key.

The client secret can be used to complete payment setup from your frontend. It should not be stored, logged, or exposed to anyone other than the customer. Make sure that you have TLS enabled on any page that includes the client secret.

ID of the Customer this SetupIntent belongs to, if one exists.

If present, the SetupIntent’s payment method will be attached to the Customer on successful setup. Payment methods attached to other Customers cannot be used with this SetupIntent.

ID of the Account this SetupIntent belongs to, if one exists.

If present, the SetupIntent’s payment method will be attached to the Account on successful setup. Payment methods attached to other Accounts cannot be used with this SetupIntent.

An arbitrary string attached to the object. Often useful for displaying to users.

The error encountered in the previous SetupIntent confirmation.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

If present, this property tells you what actions you need to take in order for your customer to continue payment setup.

ID of the payment method used with this SetupIntent. If the payment method is card_present and isn’t a digital wallet, then the generated_card associated with the latest_attempt is attached to the Customer instead.

Status of this SetupIntent, one of requires_payment_method, requires_confirmation, requires_action, processing, canceled, or succeeded.

Indicates how the payment method is intended to be used in the future.

Use on_session if you intend to only reuse the payment method when the customer is in your checkout flow. Use off_session if your customer may or may not be in your checkout flow. If not provided, this value defaults to off_session.

Creates a SetupIntent object.

After you create the SetupIntent, attach a payment method and confirm it to collect any required permissions to charge the payment method later.

When you enable this parameter, this SetupIntent accepts payment methods that you enable in the Dashboard and that are compatible with its other parameters.

Set to true to attempt to confirm this SetupIntent immediately. This parameter defaults to false. If a card is the attached payment method, you can provide a return_url in case further authentication is necessary.

ID of the Customer this SetupIntent belongs to, if one exists.

If present, the SetupIntent’s payment method will be attached to the Customer on successful setup. Payment methods attached to other Customers cannot be used with this SetupIntent.

ID of the Account this SetupIntent belongs to, if one exists.

If present, the SetupIntent’s payment method will be attached to the Account on successful setup. Payment methods attached to other Accounts cannot be used with this SetupIntent.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

ID of the payment method (a PaymentMethod, Card, or saved Source object) to attach to this SetupIntent.

Indicates how the payment method is intended to be used in the future. If not provided, this value defaults to off_session.

Use off_session if your customer may or may not be in your checkout flow.

Use on_session if you intend to only reuse the payment method when the customer is in your checkout flow.

Returns a SetupIntent object.

Updates a SetupIntent object.

ID of the Customer this SetupIntent belongs to, if one exists.

If present, the SetupIntent’s payment method will be attached to the Customer on successful setup. Payment methods attached to other Customers cannot be used with this SetupIntent.

ID of the Account this SetupIntent belongs to, if one exists.

If present, the SetupIntent’s payment method will be attached to the Account on successful setup. Payment methods attached to other Accounts cannot be used with this SetupIntent.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

ID of the payment method (a PaymentMethod, Card, or saved Source object) to attach to this SetupIntent. To unset this field to null, pass in an empty string.

Returns a SetupIntent object.

Retrieves the details of a SetupIntent that has previously been created.

Client-side retrieval using a publishable key is allowed when the client_secret is provided in the query string.

When retrieved with a publishable key, only a subset of properties will be returned. Please refer to the SetupIntent object reference for more details.

The client secret of the SetupIntent. We require this string if you use a publishable key to retrieve the SetupIntent.

Returns a SetupIntent if a valid identifier was provided.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "seti_1Mm8s8LkdIwHu7ix0OXBfTRG",  "object": "setup_intent",  "application": null,  "cancellation_reason": null,  "client_secret": "seti_1Mm8s8LkdIwHu7ix0OXBfTRG_secret_NXDICkPqPeiBTAFqWmkbff09lRmSVXe",  "created": 1678942624,  "customer": null,  "description": null,  "flow_directions": null,  "last_setup_error": null,  "latest_attempt": null,  "livemode": false,  "mandate": null,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": null,  "payment_method_options": {    "card": {      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    }  },  "payment_method_types": [    "card"  ],  "single_use_mandate": null,  "status": "requires_payment_method",  "usage": "off_session"}
```

Example 2 (unknown):
```unknown
{  "id": "seti_1Mm8s8LkdIwHu7ix0OXBfTRG",  "object": "setup_intent",  "application": null,  "cancellation_reason": null,  "client_secret": "seti_1Mm8s8LkdIwHu7ix0OXBfTRG_secret_NXDICkPqPeiBTAFqWmkbff09lRmSVXe",  "created": 1678942624,  "customer": null,  "description": null,  "flow_directions": null,  "last_setup_error": null,  "latest_attempt": null,  "livemode": false,  "mandate": null,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": null,  "payment_method_options": {    "card": {      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    }  },  "payment_method_types": [    "card"  ],  "single_use_mandate": null,  "status": "requires_payment_method",  "usage": "off_session"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/setup_intents \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "payment_method_types[]"=card
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/setup_intents \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "payment_method_types[]"=card
```

---

## 

**URL:** https://docs.stripe.com/webhooks/quickstart

---

## The Setup Intents API

**URL:** https://docs.stripe.com/payments/setup-intents

**Contents:**
- The Setup Intents API
- Learn more about the Setup Intents API for saving payment methods.
- Saving and reusing payment methods
    - Note
    - Get started
- Get permission to save a payment method
  - Future on-session use
  - Future off-session use
- Specify usage to increase success rate
    - Note

Use the Setup Intents API to set up a payment method for future payments. It’s similar to a payment, but no charge is created. Set up a payment method for future payments now.

The goal is to have payment credentials saved and optimized for future payments, meaning the payment method is configured correctly for any scenario. When setting up a card, for example, it may be necessary to authenticate the customer or check the card’s validity with the customer’s bank. Stripe updates the SetupIntent object throughout that process.

The Setup Intents API is useful for businesses that onboard customers but don’t charge them right away:

You can also set up payment methods for future use when you do charge them during Checkout.

You’re responsible for your compliance with all applicable laws, regulations, and network rules when saving a customer’s payment details.

If you set up a payment method for future on-session payments, such as displaying the payment method on a future checkout page, you must explicitly collect consent from the customer for this specific use. For example, include a “Save my payment method for future use” checkbox to collect consent.

If you need to differentiate between payment methods saved only for offline usages and payment methods you can present to your customer for future on-session purchases, you can utilize the allow_redisplay parameter on the PaymentMethod object.

If you set up a payment method for future off-session payments, you need permission. Creating an agreement (sometimes called a mandate) up front allows you to charge the customer when they’re not actively using your website or app.

Add terms to your website or app that state how you plan to process payments, and let customers opt in. At a minimum, ensure that your terms cover the following:

See recommended mandate text for saving cards or saving SEPA bank details.

For users impacted by SCA, this agreement helps payments succeed without interruption. When you set up your integration to properly save a card, Stripe marks any subsequent off-session payment as a merchant-initiated transaction (MIT) so that your customers don’t have to come back online and authenticate. Merchant-initiated transactions require an agreement between you and your customer.

The usage parameter tells Stripe how you plan to use payment method details later. For some payment methods, Stripe can use your usage setting to pick the most frictionless flow for the customer. This optimization is designed to increase the number of successful payments.

For example, credit and debit cards under European SCA regulation may require the customer to authenticate the card during the saving process. Setting usage to off_session properly authenticates a credit or debit card for off-session payments so that your customer doesn’t have to come back online and re-authenticate. So although it creates initial friction in the setup flow, setting usage to off_session can reduce customer intervention in later off-session payments.

However, if you only plan to use the card when the customer is checking out, set usage to on_session. This lets the bank know you plan to use the card when the customer is available to authenticate, so you can postpone authenticating the card details until then and avoid upfront friction.

Usage is an optimization. You can still use a card that’s set up for on-session payments to make off-session payments, but banks are more likely to reject the off-session payment and require authentication from the customer. Either case might still require later authentication, so build a recovery process in your app. When an off-session card payment requires authentication, bring your customer back online to complete the payment.

If not specified, usage defaults to off_session. See how to create a SetupIntent on your server and specify the usage:

Follow the guidance on this page to ensure your integration handles cards that require Strong Customer Authentication. Correctly flagging transactions allows Stripe to claim correct SCA exemptions on your behalf to minimize the need for authentication with each payment.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/setup_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d usage=on_session
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/setup_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d usage=on_session
```

---

## Setup Attempts

**URL:** https://docs.stripe.com/api/setup_attempts

**Contents:**
- Setup Attempts
- The SetupAttempt object
  - Attributes
    - idstring
    - objectstring
    - applicationnullable stringExpandable
    - attach_to_selfnullable boolean
    - createdtimestampretrievable with publishable key
    - customernullable stringExpandable
    - customer_accountnullable string

A SetupAttempt describes one attempted confirmation of a SetupIntent, whether that confirmation is successful or unsuccessful. You can use SetupAttempts to inspect details of a specific attempt at setting up a payment method using a SetupIntent.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value.

The value of application on the SetupIntent at the time of this confirmation.

If present, the SetupIntent’s payment method will be attached to the in-context Stripe Account.

It can only be used for this Stripe Account’s own money movement flows like InboundTransfer and OutboundTransfers. It cannot be set to true when setting up a PaymentMethod for a Customer, and defaults to false when attaching a PaymentMethod to a Customer.

Time at which the object was created. Measured in seconds since the Unix epoch.

The value of customer on the SetupIntent at the time of this confirmation.

The value of customer_account on the SetupIntent at the time of this confirmation.

Indicates the directions of money movement for which this payment method is intended to be used.

Include inbound if you intend to use the payment method as the origin to pull funds from. Include outbound if you intend to use the payment method as the destination to send funds to. You can include both if you intend to use the payment method for both purposes.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The value of on_behalf_of on the SetupIntent at the time of this confirmation.

ID of the payment method used with this SetupAttempt.

Details about the payment method at the time of SetupIntent confirmation.

The error encountered during this attempt to confirm the SetupIntent, if any.

ID of the SetupIntent that this attempt belongs to.

Status of this SetupAttempt, one of requires_confirmation, requires_action, processing, succeeded, failed, or abandoned.

The value of usage on the SetupIntent at the time of this confirmation, one of off_session or on_session.

Returns a list of SetupAttempts that associate with a provided SetupIntent.

Only return SetupAttempts created by the SetupIntent specified by this ID.

A dictionary with a data property that contains an array of up to limit SetupAttempts that are created by the specified SetupIntent, which start after SetupAttempts starting_after. Each entry in the array is a separate SetupAttempts object. If no other SetupAttempts are available, the resulting array is be empty. This request should never raise an error.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "setatt_1ErTsH2eZvKYlo2CI7ukcoF7",  "object": "setup_attempt",  "application": null,  "created": 1562004309,  "customer": null,  "flow_directions": null,  "livemode": false,  "on_behalf_of": null,  "payment_method": "pm_1ErTsG2eZvKYlo2CH0DNen59",  "payment_method_details": {    "card": {      "three_d_secure": null    },    "type": "card"  },  "setup_error": null,  "setup_intent": "seti_1ErTsG2eZvKYlo2CKaT8MITz",  "status": "succeeded",  "usage": "off_session"}
```

Example 2 (unknown):
```unknown
{  "id": "setatt_1ErTsH2eZvKYlo2CI7ukcoF7",  "object": "setup_attempt",  "application": null,  "created": 1562004309,  "customer": null,  "flow_directions": null,  "livemode": false,  "on_behalf_of": null,  "payment_method": "pm_1ErTsG2eZvKYlo2CH0DNen59",  "payment_method_details": {    "card": {      "three_d_secure": null    },    "type": "card"  },  "setup_error": null,  "setup_intent": "seti_1ErTsG2eZvKYlo2CKaT8MITz",  "status": "succeeded",  "usage": "off_session"}
```

Example 3 (unknown):
```unknown
curl -G https://api.stripe.com/v1/setup_attempts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3 \  -d setup_intent=seti_1ErTsG2eZvKYlo2CKaT8MITz
```

Example 4 (unknown):
```unknown
curl -G https://api.stripe.com/v1/setup_attempts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3 \  -d setup_intent=seti_1ErTsG2eZvKYlo2CKaT8MITz
```

---

## 

**URL:** https://docs.stripe.com/billing/quickstart

---

## Quickstart guides

**URL:** https://docs.stripe.com/quickstarts

**Contents:**
- Quickstart guides
- Review a list of all Stripe integration quickstart guides.
- Payments
- Platforms and marketplaces
- Developer resources

This page contains a list of all Stripe integration quickstart guides. These guides include:

---

## Attach a PaymentMethod to a Customer

**URL:** https://docs.stripe.com/api/payment_methods/attach

**Contents:**
- Attach a PaymentMethod to a Customer
  - Parameters
    - customerstring
    - customer_accountstring
  - Returns
- Detach a PaymentMethod from a Customer
  - Parameters
  - Returns

Attaches a PaymentMethod object to a Customer.

To attach a new PaymentMethod to a customer for future payments, we recommend you use a SetupIntent or a PaymentIntent with setup_future_usage. These approaches will perform any necessary steps to set up the PaymentMethod for future payments. Using the /v1/payment_methods/:id/attach endpoint without first using a SetupIntent or PaymentIntent with setup_future_usage does not optimize the PaymentMethod for future use, which makes later declines and payment friction more likely. See Optimizing cards for future payments for more information about setting up future payments.

To use this PaymentMethod as the default for invoice or subscription payments, set invoice_settings.default_payment_method, on the Customer to the PaymentMethod’s ID.

The ID of the customer to which to attach the PaymentMethod.

The ID of the Account representing the customer to which to attach the PaymentMethod.

Returns a PaymentMethod object.

Detaches a PaymentMethod object from a Customer. After a PaymentMethod is detached, it can no longer be used for a payment or re-attached to a Customer.

Returns a PaymentMethod object.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_methods/pm_1MqM05LkdIwHu7ixlDxxO6Mc/attach \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_NbZ8Ki3f322LNn
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_methods/pm_1MqM05LkdIwHu7ixlDxxO6Mc/attach \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_NbZ8Ki3f322LNn
```

Example 3 (unknown):
```unknown
{  "id": "pm_1MqM05LkdIwHu7ixlDxxO6Mc",  "object": "payment_method",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": null,    "phone": null  },  "card": {    "brand": "visa",    "checks": {      "address_line1_check": null,      "address_postal_code_check": null,      "cvc_check": "pass"    },    "country": "US",    "exp_month": 8,    "exp_year": 2026,    "fingerprint": "mToisGZ01V71BCos",    "funding": "credit",    "generated_from": null,    "last4": "4242",    "networks": {      "available": [        "visa"      ],      "preferred": null    },    "three_d_secure_usage": {      "supported": true    },    "wallet": null  },  "created": 1679946402,  "customer": "cus_NbZ8Ki3f322LNn",  "livemode": false,  "metadata": {},  "type": "card"}
```

Example 4 (unknown):
```unknown
{  "id": "pm_1MqM05LkdIwHu7ixlDxxO6Mc",  "object": "payment_method",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": null,    "phone": null  },  "card": {    "brand": "visa",    "checks": {      "address_line1_check": null,      "address_postal_code_check": null,      "cvc_check": "pass"    },    "country": "US",    "exp_month": 8,    "exp_year": 2026,    "fingerprint": "mToisGZ01V71BCos",    "funding": "credit",    "generated_from": null,    "last4": "4242",    "networks": {      "available": [        "visa"      ],      "preferred": null    },    "three_d_secure_usage": {      "supported": true    },    "wallet": null  },  "created": 1679946402,  "customer": "cus_NbZ8Ki3f322LNn",  "livemode": false,  "metadata": {},  "type": "card"}
```

---

## Select your reader

**URL:** https://docs.stripe.com/terminal/payments/setup-reader

**Contents:**
- Select your reader
- Learn about Stripe's pre-certified card readers and Tap to Pay.
- Order readers
    - Warning
- Compare readers
  - Integration support
  - Payment methods
  - Additional features and customization
  - Device specs and accessories
- Integration platform comparison

Stripe readers offer end-to-end encryption by default and remote management tools. Select your form of payment acceptance to learn how to set it up:

Verifone Private preview

Refer to the tables on this page to help you choose a reader that works with your application and physical sales environment. For detailed information about specific combinations, see Design an integration.

If you don’t have a reader, you can order readers from the Dashboard and have them shipped to a location of your choice. As a Connect platform, you can order readers centrally and assign them to your connected accounts, or enable your connected accounts to order their own readers directly.

If you don’t have a physical reader, you can use the simulated reader to build and test your Terminal integration. The simulated reader doesn’t require any setup and you can start by setting up your integration.

Stripe readers aren’t liquid-proof and we recommend that users make appropriate efforts to make sure their devices remain dry. If your device has experienced liquid ingress, we recommend that you stop using the device and let it dry thoroughly before attempting to re-use or charge the device. If your device doesn’t properly operate or charge properly after drying, you need to replace it.

This table shows the basic features of each reader. Verifone includes the following readers: V660p, UX700, P630, and M425.

Set up your reader with a Terminal SDK or server-driven integration. Verifone readers are compatible with all Terminal SDKs and the Stripe API. Learn more about the integration platforms.

This table displays the payment methods accepted by each reader.

This table displays features for each reader.

Ability to run custom POS app

Paid feature, contact your sales representative

User can implement this functionality within their iOS or Android app

Paid feature, contact your sales representative

End-to-end encryption, P2PE ready, Mail order telephone order (MO/TO) P2PE

End-to-end encryption, P2PE ready, Mail order telephone order (MO/TO) P2PE

End-to-end encryption, P2PE ready

End-to-end encryption, P2PE ready

End-to-end encryption

End-to-end encryption, P2PE capable

End-to-end encryption, P2PE capable

End-to-end encryption, P2PE capable

End-to-end encryption, P2PE capable

*Battery life information is only an estimate. Battery life varies depending on a number of factors including product specifications, settings, and applications or deployed features.

Choose an integration platform based on the following factors:

Server-driven integration, which uses the Stripe API rather than a Terminal client SDK

This table lists the features of the five integration platforms.

Not all readers are available in every country. This table lists the readers you can use in each country.

Before processing payments, you must connect a Terminal reader to your point-of-sale application using the Terminal SDK. Each reader can only connect to one instance of the SDK at a time. For example, if you want four mobile readers in your store and your app runs on iOS, you also need four iOS devices. Only one reader connects to the SDK at a time.

In-person payments must follow strict rules to meet PCI compliance, PCI certifications, and EMV certifications.

Terminal offers pre-certified readers that accept payment details (EMV, contactless, and swiped), encrypt sensitive card information, and return a token to your application through the Stripe Terminal SDK so you can confirm payment.

Stripe and our hardware partners periodically release reader software updates, which can include improvements and required security updates. Your application must include support for automatic updates. Failing to install a required update can prevent a reader from accepting payments. Smart readers update themselves automatically when powered on, sufficiently charged, and not in use. Bluetooth readers update themselves automatically upon connection to your point of sale.

---

## Send your first Stripe API request

**URL:** https://docs.stripe.com/get-started/api-request

**Contents:**
- Send your first Stripe API request
- Get started with the Stripe API.
- Before you begin
- Send your first API request
- View logs and events
- Store your API keys
    - Restricted API keys
  - Example API keys
- See also

Every call to a Stripe API must include an API secret key. After you create a Stripe account, we generate two pairs of API keys for you—a publishable client-side key and a secret server-side key—for both testing in a sandbox and in live modes. To start moving real money with your live-mode keys, you need to activate your account.

This guide walks you through a simple interaction with the Stripe API—creating a customer. For a better understanding of Stripe API objects and how they fit together, take a tour of the API or visit the API reference. If you’re ready to start accepting payments, see our quickstart.

You can begin exploring Stripe APIs using the Stripe Shell. The Stripe Shell allows you to execute Stripe CLI commands directly within the Stripe docs site. As it operates in a sandbox environment only, you don’t have to worry about initiating any real money-moving transactions.

To create a customer using the Stripe Shell, enter the following command:

If everything worked, the command line displays the following response:

(Optional) Run the same command by passing in your API secret key in a sandbox:

If everything worked, the command line displays the following response:

Whenever you make a call to Stripe APIs, Stripe creates and stores API and Events objects for your Stripe user account. The API key you specify for the request determines whether the objects are stored in a sandbox environment or in live mode. For example, the last request used your API secret key, so Stripe stored the objects in a sandbox.

To view the API request log:

To view the Event log:

By default, all accounts have a total of four API keys:

Your secret and publishable keys are on the API keys tab in the Dashboard. If you can’t view your API keys, ask the owner of your Stripe account to add you to their team with the proper permissions.

You can generate restricted API keys in the Dashboard to enable customizable and limited access to the API. However, Stripe doesn’t offer any restricted keys by default.

If you’re logged in to Stripe, our documentation populates code examples with your test API keys. Only you can see these values. If you’re not logged in, our code examples include randomly generated API keys that you can replace with your test keys. Or you can log in to see the code examples populated with your test API keys.

The following table shows randomly generated examples of secret and publishable keys:

**Examples:**

Example 1 (unknown):
```unknown
stripe customers create --email=jane.smith@email.com --name="Jane Smith" --description="My First Stripe Customer"
```

Example 2 (unknown):
```unknown
stripe customers create --email=jane.smith@email.com --name="Jane Smith" --description="My First Stripe Customer"
```

Example 3 (unknown):
```unknown
{
  "id": "cus_LfctGLAICpokzr",
  "object": "customer",
```

Example 4 (unknown):
```unknown
{
  "id": "cus_LfctGLAICpokzr",
  "object": "customer",
```

---

## The SetupAttempt object

**URL:** https://docs.stripe.com/api/setup_attempts/object

**Contents:**
- The SetupAttempt object
  - Attributes
    - idstring
    - objectstring
    - applicationnullable stringExpandable
    - attach_to_selfnullable boolean
    - createdtimestampretrievable with publishable key
    - customernullable stringExpandable
    - customer_accountnullable string
    - flow_directionsnullable array of enums

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value.

The value of application on the SetupIntent at the time of this confirmation.

If present, the SetupIntent’s payment method will be attached to the in-context Stripe Account.

It can only be used for this Stripe Account’s own money movement flows like InboundTransfer and OutboundTransfers. It cannot be set to true when setting up a PaymentMethod for a Customer, and defaults to false when attaching a PaymentMethod to a Customer.

Time at which the object was created. Measured in seconds since the Unix epoch.

The value of customer on the SetupIntent at the time of this confirmation.

The value of customer_account on the SetupIntent at the time of this confirmation.

Indicates the directions of money movement for which this payment method is intended to be used.

Include inbound if you intend to use the payment method as the origin to pull funds from. Include outbound if you intend to use the payment method as the destination to send funds to. You can include both if you intend to use the payment method for both purposes.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The value of on_behalf_of on the SetupIntent at the time of this confirmation.

ID of the payment method used with this SetupAttempt.

Details about the payment method at the time of SetupIntent confirmation.

The error encountered during this attempt to confirm the SetupIntent, if any.

ID of the SetupIntent that this attempt belongs to.

Status of this SetupAttempt, one of requires_confirmation, requires_action, processing, succeeded, failed, or abandoned.

The value of usage on the SetupIntent at the time of this confirmation, one of off_session or on_session.

Returns a list of SetupAttempts that associate with a provided SetupIntent.

Only return SetupAttempts created by the SetupIntent specified by this ID.

A dictionary with a data property that contains an array of up to limit SetupAttempts that are created by the specified SetupIntent, which start after SetupAttempts starting_after. Each entry in the array is a separate SetupAttempts object. If no other SetupAttempts are available, the resulting array is be empty. This request should never raise an error.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "setatt_1ErTsH2eZvKYlo2CI7ukcoF7",  "object": "setup_attempt",  "application": null,  "created": 1562004309,  "customer": null,  "flow_directions": null,  "livemode": false,  "on_behalf_of": null,  "payment_method": "pm_1ErTsG2eZvKYlo2CH0DNen59",  "payment_method_details": {    "card": {      "three_d_secure": null    },    "type": "card"  },  "setup_error": null,  "setup_intent": "seti_1ErTsG2eZvKYlo2CKaT8MITz",  "status": "succeeded",  "usage": "off_session"}
```

Example 2 (unknown):
```unknown
{  "id": "setatt_1ErTsH2eZvKYlo2CI7ukcoF7",  "object": "setup_attempt",  "application": null,  "created": 1562004309,  "customer": null,  "flow_directions": null,  "livemode": false,  "on_behalf_of": null,  "payment_method": "pm_1ErTsG2eZvKYlo2CH0DNen59",  "payment_method_details": {    "card": {      "three_d_secure": null    },    "type": "card"  },  "setup_error": null,  "setup_intent": "seti_1ErTsG2eZvKYlo2CKaT8MITz",  "status": "succeeded",  "usage": "off_session"}
```

Example 3 (unknown):
```unknown
curl -G https://api.stripe.com/v1/setup_attempts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3 \  -d setup_intent=seti_1ErTsG2eZvKYlo2CKaT8MITz
```

Example 4 (unknown):
```unknown
curl -G https://api.stripe.com/v1/setup_attempts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3 \  -d setup_intent=seti_1ErTsG2eZvKYlo2CKaT8MITz
```

---

## 

**URL:** https://docs.stripe.com/payments/quickstart

---

## 

**URL:** https://docs.stripe.com/terminal/quickstart

---

## Set up your integration

**URL:** https://docs.stripe.com/terminal/payments/setup-integration

**Contents:**
- Set up your integration
- Set up a Stripe Terminal SDK or server-driven integration to accept in-person payments.
- Get started
- See also

Server-driven integrations use the Stripe API instead of a Terminal SDK to connect to WisePOS E, Stripe Reader S700, and Verifone smart readers and collect in-person payments. This allows you to:

Server-driven integration doesn’t support:

You can start your server-driven integration using the Terminal Quickstart with the following components:

---

## Introduction to server-side SDKs

**URL:** https://docs.stripe.com/sdks/server-side

**Contents:**
- Introduction to server-side SDKs
- Learn how to install and use the Stripe server-side SDKs.
- Installation and setup
- Send API requests
- Access the API response
- Expanding responses
- Retrieve the request ID
- Set additional request options
- Error handling
- Undocumented params and fields

The Stripe server-side SDKs reduce the amount of work required to use our REST APIs. Stripe-maintained SDKs are available for Ruby, PHP, Java, Python, Node, .NET and Go. Community libraries are also available for other server languages.

Select your language in the language selector below, then follow the instructions to install the SDK.

After completing the installation, you need to initialize Stripe:

You can manipulate objects with the Stripe API in six primary ways: create, update, delete, retrieve, list, and search. The following examples show each of the six ways using the Customer object:

Create a customer named John Doe.

API requests can contain different types of parameters. For example, here’s how to create a customer with a name (a string), address (an object), and preferred_locales (a list):

When updating an object, you can clear some of its properties. For dynamically typed languages, send an empty string. For strongly typed languages, use specific constants. For example, here’s how to clear the name (a string) and metadata (a hash of key-value pairs) of a customer:

This example clears all metadata, but you can also clear individual keys. Learn more about managing metadata in our metadata guide.

Every time you make an API request, Stripe sends you back a response.

If you create, retrieve, or update an object, you get back the object itself:

Use a variable to access the properties of that object:

When listing or searching for objects, you get back a List object containing a data array with the objects requested:

Use a loop on the data array to access the properties of each object:

You could also use auto-pagination to iterate over all the results.

Some properties are expandable or includable, meaning you can return them by using the expand parameter. For example:

Learn more about expanding responses.

Each API request has a unique request ID (req_xxx) associated with it. You can use it to inspect the request in the Dashboard to see the parameters Stripe received, or to share it with Stripe support when you need to resolve an issue.

You can find the IDs in your Dashboard logs, or directly with code like this:

When sending API requests, you can set additional request options to:

Each server SDK interprets error responses from the Stripe API as exception types, so you don’t need to parse the response status yourself. Use error handling conventions appropriate for each language to handle those errors.

Learn more about error handling.

In some cases, you might encounter parameters on an API request or fields on an API response that aren’t available using the SDKs for strongly typed languages. Use the workarounds in this section to send undocumented parameters or access undocumented fields.

Send undocumented parameters:

Access undocumented fields:

The source code for each of our server SDKs is available on GitHub:

The StripeClient class acts as an entry point to help you discover resources and make requests to the Stripe API. The benefits of using this pattern over the older one that used global configuration are:

The Node.js SDK has always had the Stripe class which followed the same pattern. For rest of the languages, the new pattern was added in the following SDK versions. If you’re comparing code targeting older versions of these libraries with older patterns, the calls might look different.

Stripe has features in the public and private preview phases that you can access through versions of the SDKs with the beta or b suffix and the alpha or a suffix, respectively.

**Examples:**

Example 1 (unknown):
```unknown
# Available as a gem
sudo gem install stripe
```

Example 2 (unknown):
```unknown
# Available as a gem
sudo gem install stripe
```

Example 3 (unknown):
```unknown
# If you use bundler, you can add this line to your Gemfile
gem 'stripe'
```

Example 4 (unknown):
```unknown
# If you use bundler, you can add this line to your Gemfile
gem 'stripe'
```

---

## How PaymentIntents and SetupIntents work

**URL:** https://docs.stripe.com/payments/paymentintents/lifecycle

**Contents:**
- How PaymentIntents and SetupIntents work
- Learn how PaymentIntents and SetupIntents work within the payment flow.

The main difference between the Payment Intents API and Setup Intents API is their purpose:

Asynchronous payments can be challenging to manage because they can depend on customer actions that happen outside of your application. For example, a user might need to confirm a payment using 3D Secure.

To simplify payment management, Stripe uses a state machine that allows you to track the state of a payment flow. To learn the states for each API, select the applicable tab below:

When the PaymentIntent is created, it has a status of requires_payment_method1 until a payment method is attached.

We recommend creating the PaymentIntent as soon as you know how much you want to charge, so that Stripe can record all the attempted payments.

After the customer provides their payment information, the PaymentIntent is ready to be confirmed.

In most integrations, this state is skipped because payment method information is submitted at the same time that the payment is confirmed.

If the payment requires additional actions, such as authenticating with 3D Secure, the PaymentIntent has a status of requires_action1.

After required actions are handled, the PaymentIntent moves to processing for asynchronous payment methods, such as bank debits. These types of payment methods can take up to a few days to process. Other payment methods, such as cards, are processed more quickly and don’t go into the processing status.

If you’re separately authorizing and capturing funds, your PaymentIntent can instead move to requires_capture. In that case, attempting to capture the funds moves it to processing.

A PaymentIntent with a status of succeeded means that the payment flow it is driving is complete.

The funds are now in your account and you can confidently fulfill the order. If you need to refund the customer, you can use the Refunds API.

If the payment attempt fails (for example due to a decline), the PaymentIntent’s status returns to requires_payment_method so that the payment can be retried.

You can cancel a PaymentIntent at any point before it’s in a processing2 or succeeded state. Canceling it invalidates the PaymentIntent for future payment attempts, and can’t be undone. If any funds have been held, cancellation releases them.

PaymentIntents might also be automatically transitioned to the canceled state after they have been confirmed too many times.

1 Versions of the API before 2019-02-11 show requires_source instead of requires_payment_method and requires_source_action instead of requires_action.

2 You can cancel a PaymentIntent in the processing state when the associated Payment Method is ACH, ACSS, AU BECS, BACS, NZ BECS, and SEPA. However, it might fail due to a limited and varying cancellation time window.

---

## The SetupIntent object

**URL:** https://docs.stripe.com/api/setup_intents/object

**Contents:**
- The SetupIntent object
  - Attributes
    - idstringretrievable with publishable key
    - automatic_payment_methodsnullable object
    - client_secretnullable stringretrievable with publishable key
    - customernullable stringExpandable
    - customer_accountnullable string
    - descriptionnullable stringretrievable with publishable key
    - last_setup_errornullable objectretrievable with publishable key
    - metadatanullable object

Unique identifier for the object.

Settings for dynamic payment methods compatible with this Setup Intent

The client secret of this SetupIntent. Used for client-side retrieval using a publishable key.

The client secret can be used to complete payment setup from your frontend. It should not be stored, logged, or exposed to anyone other than the customer. Make sure that you have TLS enabled on any page that includes the client secret.

ID of the Customer this SetupIntent belongs to, if one exists.

If present, the SetupIntent’s payment method will be attached to the Customer on successful setup. Payment methods attached to other Customers cannot be used with this SetupIntent.

ID of the Account this SetupIntent belongs to, if one exists.

If present, the SetupIntent’s payment method will be attached to the Account on successful setup. Payment methods attached to other Accounts cannot be used with this SetupIntent.

An arbitrary string attached to the object. Often useful for displaying to users.

The error encountered in the previous SetupIntent confirmation.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

If present, this property tells you what actions you need to take in order for your customer to continue payment setup.

ID of the payment method used with this SetupIntent. If the payment method is card_present and isn’t a digital wallet, then the generated_card associated with the latest_attempt is attached to the Customer instead.

Status of this SetupIntent, one of requires_payment_method, requires_confirmation, requires_action, processing, canceled, or succeeded.

Indicates how the payment method is intended to be used in the future.

Use on_session if you intend to only reuse the payment method when the customer is in your checkout flow. Use off_session if your customer may or may not be in your checkout flow. If not provided, this value defaults to off_session.

Creates a SetupIntent object.

After you create the SetupIntent, attach a payment method and confirm it to collect any required permissions to charge the payment method later.

When you enable this parameter, this SetupIntent accepts payment methods that you enable in the Dashboard and that are compatible with its other parameters.

Set to true to attempt to confirm this SetupIntent immediately. This parameter defaults to false. If a card is the attached payment method, you can provide a return_url in case further authentication is necessary.

ID of the Customer this SetupIntent belongs to, if one exists.

If present, the SetupIntent’s payment method will be attached to the Customer on successful setup. Payment methods attached to other Customers cannot be used with this SetupIntent.

ID of the Account this SetupIntent belongs to, if one exists.

If present, the SetupIntent’s payment method will be attached to the Account on successful setup. Payment methods attached to other Accounts cannot be used with this SetupIntent.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

ID of the payment method (a PaymentMethod, Card, or saved Source object) to attach to this SetupIntent.

Indicates how the payment method is intended to be used in the future. If not provided, this value defaults to off_session.

Use off_session if your customer may or may not be in your checkout flow.

Use on_session if you intend to only reuse the payment method when the customer is in your checkout flow.

Returns a SetupIntent object.

Updates a SetupIntent object.

ID of the Customer this SetupIntent belongs to, if one exists.

If present, the SetupIntent’s payment method will be attached to the Customer on successful setup. Payment methods attached to other Customers cannot be used with this SetupIntent.

ID of the Account this SetupIntent belongs to, if one exists.

If present, the SetupIntent’s payment method will be attached to the Account on successful setup. Payment methods attached to other Accounts cannot be used with this SetupIntent.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

ID of the payment method (a PaymentMethod, Card, or saved Source object) to attach to this SetupIntent. To unset this field to null, pass in an empty string.

Returns a SetupIntent object.

Retrieves the details of a SetupIntent that has previously been created.

Client-side retrieval using a publishable key is allowed when the client_secret is provided in the query string.

When retrieved with a publishable key, only a subset of properties will be returned. Please refer to the SetupIntent object reference for more details.

The client secret of the SetupIntent. We require this string if you use a publishable key to retrieve the SetupIntent.

Returns a SetupIntent if a valid identifier was provided.

Returns a list of SetupIntents.

Only return SetupIntents for the customer specified by this customer ID.

Only return SetupIntents for the account specified by this customer ID.

Only return SetupIntents that associate with the specified payment method.

A dictionary with a data property that contains an array of up to limit SetupIntents, starting after SetupIntent starting_after. Each entry in the array is a separate SetupIntent object. If no more SetupIntents are available, the resulting array will be empty.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "seti_1Mm8s8LkdIwHu7ix0OXBfTRG",  "object": "setup_intent",  "application": null,  "cancellation_reason": null,  "client_secret": "seti_1Mm8s8LkdIwHu7ix0OXBfTRG_secret_NXDICkPqPeiBTAFqWmkbff09lRmSVXe",  "created": 1678942624,  "customer": null,  "description": null,  "flow_directions": null,  "last_setup_error": null,  "latest_attempt": null,  "livemode": false,  "mandate": null,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": null,  "payment_method_options": {    "card": {      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    }  },  "payment_method_types": [    "card"  ],  "single_use_mandate": null,  "status": "requires_payment_method",  "usage": "off_session"}
```

Example 2 (unknown):
```unknown
{  "id": "seti_1Mm8s8LkdIwHu7ix0OXBfTRG",  "object": "setup_intent",  "application": null,  "cancellation_reason": null,  "client_secret": "seti_1Mm8s8LkdIwHu7ix0OXBfTRG_secret_NXDICkPqPeiBTAFqWmkbff09lRmSVXe",  "created": 1678942624,  "customer": null,  "description": null,  "flow_directions": null,  "last_setup_error": null,  "latest_attempt": null,  "livemode": false,  "mandate": null,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": null,  "payment_method_options": {    "card": {      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    }  },  "payment_method_types": [    "card"  ],  "single_use_mandate": null,  "status": "requires_payment_method",  "usage": "off_session"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/setup_intents \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "payment_method_types[]"=card
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/setup_intents \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "payment_method_types[]"=card
```

---

## List all SetupAttempts

**URL:** https://docs.stripe.com/api/setup_attempts/list

**Contents:**
- List all SetupAttempts
  - Parameters
    - setup_intentstringRequired
  - More parametersExpand all
    - createdobject
    - ending_beforestring
    - limitinteger
    - starting_afterstring
  - Returns

Returns a list of SetupAttempts that associate with a provided SetupIntent.

Only return SetupAttempts created by the SetupIntent specified by this ID.

A dictionary with a data property that contains an array of up to limit SetupAttempts that are created by the specified SetupIntent, which start after SetupAttempts starting_after. Each entry in the array is a separate SetupAttempts object. If no other SetupAttempts are available, the resulting array is be empty. This request should never raise an error.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v1/setup_attempts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3 \  -d setup_intent=seti_1ErTsG2eZvKYlo2CKaT8MITz
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v1/setup_attempts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3 \  -d setup_intent=seti_1ErTsG2eZvKYlo2CKaT8MITz
```

Example 3 (unknown):
```unknown
{  "object": "list",  "url": "/v1/setup_attempts",  "has_more": false,  "data": [    {      "id": "setatt_1ErTsH2eZvKYlo2CI7ukcoF7",      "object": "setup_attempt",      "application": null,      "created": 1562004309,      "customer": null,      "flow_directions": null,      "livemode": false,      "on_behalf_of": null,      "payment_method": "pm_1ErTsG2eZvKYlo2CH0DNen59",      "payment_method_details": {        "card": {          "three_d_secure": null        },        "type": "card"      },      "setup_error": null,      "setup_intent": "seti_1ErTsG2eZvKYlo2CKaT8MITz",      "status": "succeeded",      "usage": "off_session"    }  ]}
```

Example 4 (unknown):
```unknown
{  "object": "list",  "url": "/v1/setup_attempts",  "has_more": false,  "data": [    {      "id": "setatt_1ErTsH2eZvKYlo2CI7ukcoF7",      "object": "setup_attempt",      "application": null,      "created": 1562004309,      "customer": null,      "flow_directions": null,      "livemode": false,      "on_behalf_of": null,      "payment_method": "pm_1ErTsG2eZvKYlo2CH0DNen59",      "payment_method_details": {        "card": {          "three_d_secure": null        },        "type": "card"      },      "setup_error": null,      "setup_intent": "seti_1ErTsG2eZvKYlo2CKaT8MITz",      "status": "succeeded",      "usage": "off_session"    }  ]}
```

---
