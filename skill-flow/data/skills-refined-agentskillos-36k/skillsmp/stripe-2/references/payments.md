# Stripe - Payments

**Pages:** 49

---

## Save a customer's payment method when they use it for a payment

**URL:** https://docs.stripe.com/payments/save-during-payment

**Contents:**
- Save a customer's payment method when they use it for a payment
- Learn how to save your customer's payment details for future purchases when they make a payment.
- Compliance
    - Note
- Set up StripeServer-side
- Create a CustomerServer-side
    - Compare Customers v1 and Accounts v2 references
- Enable saved payment methods
    - Caution
    - Note

Use the Checkout Sessions API to save payment details during a purchase. This is useful for situations such as:

You’re responsible for your compliance with all applicable laws, regulations, and network rules when saving a customer’s payment details. These requirements generally apply if you want to save your customer’s payment method for future use, such as displaying a customer’s payment method to them in the checkout flow for a future purchase or charging them when they’re not actively using your website or app. Add terms to your website or app that state how you plan to save payment method details and allow customers to opt in.

When you save a payment method, you can only use it for the specific usage you have included in your terms. To charge a payment method when a customer is offline and save it as an option for future purchases, make sure that you explicitly collect consent from the customer for this specific use. For example, include a “Save my payment method for future use” checkbox to collect consent.

To charge a customer when they’re offline, make sure your terms include the following:

Make sure you keep a record of your customer’s written agreement to these terms.

When using Elements with the Checkout Sessions API, only cards are supported for saved payment methods. You can’t save other payment methods, such as bank accounts.

First, register for a Stripe account.

Use our official libraries to access the Stripe API from your application:

To set a card up for future payments, you must attach it to a Customer. Create a Customer object when your customer creates an account with your business. Customer objects allow for reusing payment methods and tracking across multiple payments.

If your Connect platform uses customer-configured Accounts, use our guide to replace Customer and event references in your code with the equivalent Accounts v2 API references.

Successful creation returns the Customer object. You can inspect the object for the customer id and store the value in your database for later retrieval.

You can find these customers in the Customers page in the Dashboard.

Global privacy laws are complicated and nuanced. Before implementing the ability to store customer payment method details, work with your legal team to make sure that it complies with your privacy and compliance framework.

To allow a customer to save their payment method for future use, specify the saved_payment_method_options.payment_method_save parameter when creating the Checkout Session.

Saving a payment method requires a Customer. Pass an existing customer or create a new one by setting customer_creation to always on the Checkout Session.

After you create the Checkout Session, use the client secret returned in the response to build your checkout page.

In the latest version of Stripe.js, specifying enableSave to auto is optional because that’s the default value when saved payment methods are enabled on the Checkout Session.

The Payment Element automatically displays a consent collection checkbox when saved payment methods are enabled on the Checkout Session. You can explicitly configure this behavior using elementsOptions on initCheckout.

Each saved payment method is linked to a Customer object. Before creating the Checkout Session, authenticate your customer, and pass the corresponding Customer ID to the Checkout Session.

In the latest version of Stripe.js, enableRedisplay defaults to auto when saved payment methods are enabled on the Checkout Session.

The Payment Element automatically redisplays previously saved payment methods for your customer to use during checkout when saved payment methods are enabled on the Checkout Session.

You can explicitly configure the redisplay behavior using elementsOptions on initCheckout.

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

## Cards

**URL:** https://docs.stripe.com/payments/cards

**Contents:**
- Cards
- Learn more about accepting card payments with Stripe.
- Payment flow
- Supported card brands
    - Note
  - Online card brand capabilities
    - Note
  - Exclude card brands
- Geographic considerations
  - SCA and 3D Secure

Cards are linked to a debit or credit account at a bank. To complete a payment online, customers enter their card information at checkout. Cards are enabled by default and are supported by online payments integration paths. You can manage payment methods from the Dashboard. Stripe handles the return of eligible payment methods based on factors such as the transaction’s amount, currency, and payment flow.

A customer initiates a card payment at checkout by entering their credit card information. Depending on their card network and country location, customers might have additional security verification steps.

Cards can act as the funding source for other Stripe payment products and methods like Link and wallets. For instance, customers can leverage Link to save their card payment data for fast checkout with any business that has Link enabled.

With wallets, customers can store their card details in a digital wallet. From your end, their payment method is managed using a wallet, but for the customer, the transaction shows up in their card history as a charge from their digital wallet provider.

Stripe supports several card brands, from large global networks like Visa and Mastercard to local networks like Cartes Bancaires in France or Interac in Canada. When you integrate Stripe, you can begin accepting a diversity of card brands without any additional configurations, including:

Some card brands require additional configuration, such as Cartes Bancaires and Interac.

In integrations that handle Link payments as card payments, non-card payment methods saved to Link can have a card brand of link.

The following table describes some of the different features and restrictions of each card brand online, including limitations on countries where Stripe users can accept the brand (Stripe Account Country), countries where most cardholders of the brand are located (Customer Country) and support for key features like 3D Secure Authentication, and Wallets (like Apple Pay and Google Pay).

Other payment scenarios like setting up future payments, saving a card or placing a hold are supported across all card brands.

Stripe supports processing payments in 135+ currencies, but some card brand networks have limitations on supported currencies that charges can be made with.

1 For more information, see American Express card support for India-based businesses.

2 Supports Apple Pay. For more information, see Cartes Bancaires with Apple Pay.

You can disallow the use of specific card brands in the following ways:

Stripe, along with other platforms, offer a solid infrastructure that handles secure payments and complies with specific regulations from different regions. This becomes particularly important with the roll-out of Strong Customer Authentication (SCA) rules in regulated markets like Europe and India, wherein additional verification steps are usually necessary.

It’s essential to ensure your Stripe integration is lined up with SCA rules and 3D Secure (3DS) criteria. Moreover, adjusting your approach to suit regional nuances—like installment payments and card brand preferences—is vital for seamless, compliant, and user-centered transactions.

Some banks, especially in regulated regions like Europe and India, might prompt the customer to authenticate a purchase (for example, by texting the customer a code to enter on the bank’s website). This authentication step is part of Strong Customer Authentication (SCA) Requirements. Making sure that your integration meets SCA requirements for 3DS can sometimes require extra steps.

SCA, a rule in effect as of September 14, 2019, as part of PSD2 regulation in Europe, requires changes to how your European customers authenticate online payments. Card payments require a different user experience, namely 3DS, to meet SCA requirements.

Stripe supports 3DS by default in Stripe Checkout, Payment Links, and a Hosted Invoice Page. You can configure your integration to use 3DS with Subscriptions and Connect with the following:

Some regions have card brands that support installment payments managed by the card issuer. In such cases, you can’t use Subscriptions or SetupIntents to create installments.

If you want to create recurring payments and your region or card network doesn’t support Meses sin intereses, see how to set up future payments or Subscriptions.

The European Union requires businesses to allow their customers the option to pick which card brand processes their transaction because cards in the EU might have both a local network, like Cartes Bancaires, and an affiliated card network, like Visa or Mastercard. You can enable this choice using Elements or Payments APIs so that customers can choose which card brand processes their payment.

The Reserve Bank of India (RBI) has specific regulations for online transactions that apply to Stripe accounts in India. Stripe Support includes a consolidated list of important resources, for many payment methods in the India FAQs.

---

## Connect to a reader

**URL:** https://docs.stripe.com/terminal/payments/connect-reader

**Contents:**
- Connect to a reader
- Connect your application to a Stripe Terminal reader.
    - Note
- Create a simulated reader
- Query your simulated reader
- Next steps

If you haven’t chosen a reader yet, compare the available Terminal readers and choose one that best suits your needs.

Stripe provides a simulated server-driven reader so you can develop and test your app and simulate Terminal payments, without connecting to physical hardware.

To create a simulated reader, use the designated registration code (simulated-wpe or simulated-s700) when registering the reader. This registration code creates a simulated WisePOS E or Stripe S700 reader object in a sandbox only. You can register the simulated reader using the Stripe API:

This returns a reader object representing your simulated reader:

The simulated reader behaves like a real reader. You can retrieve its information from the reader endpoint:

You’ve connected your application to the reader. Next, collect your first Stripe Terminal payment.

The BBPOS and Chipper™ name and logo are trademarks or registered trademarks of BBPOS Limited in the United States or other countries. The Verifone® name and logo are either trademarks or registered trademarks of Verifone in the United States and/or other countries. Use of the trademarks doesn’t imply any endorsement by BBPOS or Verifone.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/readers \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d location="{{LOCATION_ID}}" \
  -d registration_code=simulated-wpe
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/readers \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d location="{{LOCATION_ID}}" \
  -d registration_code=simulated-wpe
```

Example 3 (unknown):
```unknown
{
  "id": "tmr_xxx",
  "object": "terminal.reader",
  "device_sw_version": "2.37.2.0",
  "device_type": "simulated_wisepos_e",
  "ip_address": "0.0.0.0",
  "label": "simulated-wpe-xxx-xxx-xx-xxx",
  "livemode": false,
  "location": "tml_xxx",
  "serial_number": "simulated-wpe-xxx-xxx-xx-xxx",
  "status": "online"
}
```

Example 4 (unknown):
```unknown
{
  "id": "tmr_xxx",
  "object": "terminal.reader",
  "device_sw_version": "2.37.2.0",
  "device_type": "simulated_wisepos_e",
  "ip_address": "0.0.0.0",
  "label": "simulated-wpe-xxx-xxx-xx-xxx",
  "livemode": false,
  "location": "tml_xxx",
  "serial_number": "simulated-wpe-xxx-xxx-xx-xxx",
  "status": "online"
}
```

---

## List all charges

**URL:** https://docs.stripe.com/api/charges/list

**Contents:**
- List all charges
  - Parameters
    - customerstring
  - More parametersExpand all
    - createdobject
    - ending_beforestring
    - limitinteger
    - payment_intentstring
    - starting_afterstring
    - transfer_groupstringConnect only

Returns a list of charges you’ve previously created. The charges are returned in sorted order, with the most recent charges appearing first.

Only return charges for the customer specified by this customer ID.

A dictionary with a data property that contains an array of up to limit charges, starting after charge starting_after. Each entry in the array is a separate charge object. If no more charges are available, the resulting array will be empty. If you provide a non-existent customer ID, this call raises an error.

Capture the payment of an existing, uncaptured charge that was created with the capture option set to false.

Uncaptured payments expire a set number of days after they are created (7 by default), after which they are marked as refunded and capture attempts will fail.

Don’t use this method to capture a PaymentIntent-initiated charge. Use Capture a PaymentIntent.

The amount to capture, which must be less than or equal to the original amount.

The email address to send this charge’s receipt to. This will override the previously-specified email address for this charge, if one was set. Receipts will not be sent in test mode.

The maximum length is 800 characters.

For a non-card charge, text that appears on the customer’s statement as the statement descriptor. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

For a card charge, this value is ignored unless you don’t specify a statement_descriptor_suffix, in which case this value is used as the suffix.

Provides information about a card charge. Concatenated to the account’s statement descriptor prefix to form the complete statement descriptor that appears on the customer’s statement. If the account has no prefix value, the suffix is concatenated to the account’s statement descriptor.

Returns the charge object, with an updated captured property (set to true). Capturing a charge will always succeed, unless the charge is already refunded, expired, captured, or an invalid capture amount is specified, in which case this method will raise an error.

Search for charges you’ve previously created using Stripe’s Search Query Language. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.

The search query string. See search query language and the list of supported query fields for charges.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A dictionary with a data property that contains an array of up to limit charges. If no objects match the query, the resulting array will be empty. See the related guide on expanding properties in lists.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v1/charges \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v1/charges \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 3 (unknown):
```unknown
{  "object": "list",  "url": "/v1/charges",  "has_more": false,  "data": [    {      "id": "ch_3MmlLrLkdIwHu7ix0snN0B15",      "object": "charge",      "amount": 1099,      "amount_captured": 1099,      "amount_refunded": 0,      "application": null,      "application_fee": null,      "application_fee_amount": null,      "balance_transaction": "txn_3MmlLrLkdIwHu7ix0uke3Ezy",      "billing_details": {        "address": {          "city": null,          "country": null,          "line1": null,          "line2": null,          "postal_code": null,          "state": null        },        "email": null,        "name": null,        "phone": null      },      "calculated_statement_descriptor": "Stripe",      "captured": true,      "created": 1679090539,      "currency": "usd",      "customer": null,      "description": null,      "disputed": false,      "failure_balance_transaction": null,      "failure_code": null,      "failure_message": null,      "fraud_details": {},      "livemode": false,      "metadata": {},      "on_behalf_of": null,      "outcome": {        "network_status": "approved_by_network",        "reason": null,        "risk_level": "normal",        "risk_score": 32,        "seller_message": "Payment complete.",        "type": "authorized"      },      "paid": true,      "payment_intent": null,      "payment_method": "card_1MmlLrLkdIwHu7ixIJwEWSNR",      "payment_method_details": {        "card": {          "brand": "visa",          "checks": {            "address_line1_check": null,            "address_postal_code_check": null,            "cvc_check": null          },          "country": "US",          "exp_month": 3,          "exp_year": 2024,          "fingerprint": "mToisGZ01V71BCos",          "funding": "credit",          "installments": null,          "last4": "4242",          "mandate": null,          "network": "visa",          "three_d_secure": null,          "wallet": null        },        "type": "card"      },      "receipt_email": null,      "receipt_number": null,      "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xTTJKVGtMa2RJd0h1N2l4KOvG06AGMgZfBXyr1aw6LBa9vaaSRWU96d8qBwz9z2J_CObiV_H2-e8RezSK_sw0KISesp4czsOUlVKY",      "refunded": false,      "review": null,      "shipping": null,      "source_transfer": null,      "statement_descriptor": null,      "statement_descriptor_suffix": null,      "status": "succeeded",      "transfer_data": null,      "transfer_group": null    }  ]}
```

Example 4 (unknown):
```unknown
{  "object": "list",  "url": "/v1/charges",  "has_more": false,  "data": [    {      "id": "ch_3MmlLrLkdIwHu7ix0snN0B15",      "object": "charge",      "amount": 1099,      "amount_captured": 1099,      "amount_refunded": 0,      "application": null,      "application_fee": null,      "application_fee_amount": null,      "balance_transaction": "txn_3MmlLrLkdIwHu7ix0uke3Ezy",      "billing_details": {        "address": {          "city": null,          "country": null,          "line1": null,          "line2": null,          "postal_code": null,          "state": null        },        "email": null,        "name": null,        "phone": null      },      "calculated_statement_descriptor": "Stripe",      "captured": true,      "created": 1679090539,      "currency": "usd",      "customer": null,      "description": null,      "disputed": false,      "failure_balance_transaction": null,      "failure_code": null,      "failure_message": null,      "fraud_details": {},      "livemode": false,      "metadata": {},      "on_behalf_of": null,      "outcome": {        "network_status": "approved_by_network",        "reason": null,        "risk_level": "normal",        "risk_score": 32,        "seller_message": "Payment complete.",        "type": "authorized"      },      "paid": true,      "payment_intent": null,      "payment_method": "card_1MmlLrLkdIwHu7ixIJwEWSNR",      "payment_method_details": {        "card": {          "brand": "visa",          "checks": {            "address_line1_check": null,            "address_postal_code_check": null,            "cvc_check": null          },          "country": "US",          "exp_month": 3,          "exp_year": 2024,          "fingerprint": "mToisGZ01V71BCos",          "funding": "credit",          "installments": null,          "last4": "4242",          "mandate": null,          "network": "visa",          "three_d_secure": null,          "wallet": null        },        "type": "card"      },      "receipt_email": null,      "receipt_number": null,      "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xTTJKVGtMa2RJd0h1N2l4KOvG06AGMgZfBXyr1aw6LBa9vaaSRWU96d8qBwz9z2J_CObiV_H2-e8RezSK_sw0KISesp4czsOUlVKY",      "refunded": false,      "review": null,      "shipping": null,      "source_transfer": null,      "statement_descriptor": null,      "statement_descriptor_suffix": null,      "status": "succeeded",      "transfer_data": null,      "transfer_group": null    }  ]}
```

---

## Dynamic payment methods

**URL:** https://docs.stripe.com/payments/payment-methods/dynamic-payment-methods

**Contents:**
- Dynamic payment methods
- Simplify your payment methods code by dynamically ordering and displaying payment methods.
- Integration options
  - Migrate to dynamic payment methods
- Dashboard-based customization features
- How dynamic payment methods work
  - Apple and Google Pay
  - Dashboard settings
    - Note
  - Exclude payment methods

Dynamic payment methods is part of the default Stripe integration and enables you to configure payment methods settings from the Dashboard—no code required. When you use dynamic payment methods in an Element, Checkout, Payment Links, or Hosted Invoice Page integration, Stripe handles the logic for dynamically displaying the most relevant eligible payment methods to each customer to maximize conversion. Dynamic payment methods also unlocks customization features to help you customize and experiment with payment methods.

Use dynamic payment methods to:

Use Checkout or Payment Element with dynamic payment methods to have Stripe handle the logic for displaying eligible payment methods in your frontend for each transaction. If you have a platform account, follow our Connect integration.

Access the following features with dynamic payment methods to control how and when payment methods render.

This section doesn’t cover Apple Pay and Google Pay, because they use different criteria.

Review this section to understand the criteria that Stripe uses to eligible payment methods, decide whether to hide or show them, and in what order. If a specific payment method isn’t appearing in your payment flow, one or more of these criteria might not be met.

View the available payment methods in your Stripe Dashboard. Only payment methods that you enabled can be shown to your customers.

If a payment method isn’t listed in your Dashboard settings, it’s either not supported by Stripe or not supported in the country where your account is registered. For example, PayNow is only available to Stripe accounts in Singapore.

Learn more about country support.

When using Stripe Connect with Direct Charges or on_behalf_of, the settings of the connected account determines the available payment methods. You can configure them in your connect settings.

While dynamic payment methods allows you to manage payment methods through the Dashboard, you can also exclude specific payment methods on a per-transaction basis using the excluded_payment_method_types parameter when creating a PaymentIntent. This gives you control over which payment methods are available for each transaction, even if they’re enabled in your Dashboard settings.

Today, excluded_payment_method_types is available using PaymentIntents, SetupIntents, Checkout, and Payment Element. To exclude payment methods for a specific PaymentIntent:

To disallow the Apple Pay, Google Pay, or Link payment methods from being used in a particular PaymentIntent, use the wallets hash parameters that are specified per integration type. For example, see the PaymentElements wallets parameter. If you exclude apple_pay, google_pay, or link using excluded_payment_method_types rather than the wallets hash, it generates an error.

Several Stripe products allow you to charge customers, such as Checkout Sessions and Payment Element. Not all payment methods are available in all products. For example, Bacs Direct Debit isn’t available in the Mobile Payment Element. Some payment methods, such as Swish, don’t support recurring payments.

Learn more about product support.

Stripe supports over 135 presentment currencies, but most payment methods only support a subset of these. For example, ACH Direct Debit is only available for payments in USD currency.

Learn more about currency support.

On top of the general minimum and maximum amount Stripe supports, some payment methods have their own minimum and maximum. For example, SEPA Direct Debit is only available for payments below 10,000 EUR.

The final amount, including tax and discounts, is the amount used to determine available payment methods.

To learn more, go to the a payment method’s overview page.

Some payment methods, such as TWINT, can’t be set up for future usage. When you set setup_future_usage, some payment methods are automatically filtered out.

Similarly, some payment methods, such as iDEAL, don’t support manual capture. When you set capture_method: manual, some payment methods are automatically filtered out.

Learn more about API support.

A customer’s country impacts which payment methods are available on the payment page, because most payment methods are available in a predefined number of countries. For example, BLIK is only available for customers in Poland.

Learn more about country support.

The following features can also impact the availability of some payment methods:

For every checkout session, the AI models in the Optimized Checkout Suite dynamically determine how eligible payment methods are displayed, including their order. These models incorporate more than 100 on-session signals—such as real-time payment method uptime and popularity among similar customers—as well as broader network signals, such as preferred payment methods used by similar businesses. The AI models work alongside any payment method logic you add in code or any rules you set up in the Dashboard.

Our AI models use an exploration-exploitation framework, delivering proven strategies while continuously testing new approaches. As a result, payment method ordering quickly adapts to changing customer expectations and systematically improves over time.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=1000 \
  -d currency=usd \
  -d "automatic_payment_methods[enabled]"=true \
  -d "excluded_payment_method_types[]"=affirm \
  -d "excluded_payment_method_types[]"=acss_debit
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=1000 \
  -d currency=usd \
  -d "automatic_payment_methods[enabled]"=true \
  -d "excluded_payment_method_types[]"=affirm \
  -d "excluded_payment_method_types[]"=acss_debit
```

---

## Testing use cases

**URL:** https://docs.stripe.com/testing-use-cases

**Contents:**
- Testing use cases
- Learn how to test your integration.
- Testing environments
    - Impact on live mode when using test mode
  - Compare testing environments
  - Differences in functionality between test mode and Sandboxes
- Transition from test mode to Sandboxes
  - Testing environments versus live mode
  - Test card numbers
  - Delete test data

Stripe’s testing environments, test mode and Sandboxes, allow you to test your integration without making actual charges or payments. These environments simulate creating real objects without affecting actual transactions or moving real money. We recommend using our quality assurance (QA) testing use cases, and importing our Postman collection to aid you in the testing process.

In a testing environment, you can charge test credit cards and create test products and prices. These environments let you simulate transactions to make sure that your integration works correctly. This feature helps to identify any bugs or errors in your Stripe implementation before you go live with actual payments. Learn how to decide between using test mode and Sandboxes.

After you create a Stripe account, you can find a set of test API keys in the Stripe Dashboard. You can use these API keys to create and retrieve simulated data by making requests to the Stripe API. To start accepting real payments, you need to activate your account, exit your testing environment using the account picker, and use the live API keys in your integration. Stripe provides a number of resources for testing your integration.

If you change settings in the Dashboard while in test mode, you might also change them in live mode. Many Dashboard pages have a white notification box and disable live mode settings while in test mode. In this case, any settings still enabled are safe to use. If you don’t see a white callout, assume any changes made in test mode affect live mode settings (unless you see an orange or blue test data banner).

Test mode and Sandboxes are testing environments that simulate creating real objects without the risk of affecting real transactions or moving actual money. Understanding when to use each can help you build your testing strategy.

We recommend using Sandboxes for your testing needs because they offer additional functionality and greater flexibility compared to test mode. By transitioning to Sandboxes, you can enhance your testing capabilities with multiple environments, granular access control, and isolated settings, allowing you to build a more robust and comprehensive testing strategy.

View the table below to understand the differences and choose the most suitable environment for your needs.

To transition from test mode to Sandboxes in the Dashboard:

All Stripe API requests occur in either testing environments or live mode. API objects in one mode aren’t accessible to the other. For example, a test product object can’t be part of a live mode payment.

Being in a testing environment in the Dashboard doesn’t affect your integration code. Your test and live mode API keys affect the behavior of your code.

Stripe provides a set of test card numbers that you can use to simulate various payment scenarios. You can use these test card numbers to create simulated payments in testing environments without processing actual payments or charges.

When you use test card numbers, you can enter any expiration date in the future and any three-digit CVC code to simulate a successful payment. If you want to simulate a failed payment, you can use specific test card numbers and CVC codes provided by Stripe.

Test card numbers are only valid in testing environments. Don’t use them for real payments.

To delete all of your test data from your Stripe account, complete the following steps:

Testing environments are temporarily unusable while the deletion process occurs.

You must manually delete Meters because the object isn’t supported by the automated test data deletion process.

By default, Stripe doesn’t email customers in testing environments. For example, paying an invoice in a sandbox doesn’t send a receipt email to the customer. Invoices finalized through the API in testing environments also don’t send a receipt email to the customer.

If you want Stripe to email customers in a testing environment, you can do the following in the Dashboard:

To verify emails for invoices and receipts, set the email address for your Team on the Customer object or receipt_email attribute on the PaymentIntent.

The following table contains quality assurance (QA) testing use cases:

Charge inquiry opened

Inquiries are similar to disputes, with three key distinctions: no funds are withdrawn unless we elevate an inquiry to a dispute, they remain refundable until disputed, and have a different set of statuses. In this case, Stripe fires a charge.dispute.created event.

When a customer loses a dispute, Stripe updates the existing Dispute object, and fires a charge.dispute.closed event.

When you win an inquiry, your balance remains the same, as no funds were removed when you initially opened the inquiry. Stripe updates the existing Dispute object, and fires a charge.dispute.closed event.

The charge appears as Refunded in the Dashboard under Payments.

Charge partially refunded

Postman is a widely-used API development tool. To make integrating Stripe easier, we provide a Payments-specific Postman collection with the tools you need to test the server-side component of your integration.

To begin, you need to access the Postman app. You can use either the browser or desktop version. After launching the app, import the collection.

To start this process on the web, press the Import button at the top-left corner, followed by the Link option. Insert the Payments collection link. If you’re using the Postman desktop app, click File > Import. After successfully importing, the collection appears under Collections.

To use the collection, go to the collection you just imported and click Variables. Copy your test mode Stripe secret key from the Stripe Dashboard, and paste it into the Initial Value field of the secret_key row. After you complete this step, you can begin making requests.

During collection runtime, scripts populate other variables. For example, when creating a customer, price, charge or PaymentIntent, the system saves that ID through a script in the collection, making it accessible for later requests, such as issuing a refund.

**Examples:**

Example 1 (unknown):
```unknown
{
  ...
  "capture_method": "manual",
  ...
  "status": "requires_capture",
  ...
}
```

Example 2 (unknown):
```unknown
{
  ...
  "capture_method": "manual",
  ...
  "status": "requires_capture",
  ...
}
```

Example 3 (unknown):
```unknown
{
    ...
    "status": "succeeded",
    ...
  }
```

Example 4 (unknown):
```unknown
{
    ...
    "status": "succeeded",
    ...
  }
```

---

## The Payment Intents API

**URL:** https://docs.stripe.com/payments/payment-intents

**Contents:**
- The Payment Intents API
- Learn how to use the Payment Intents API for Stripe payments.
- A complete set of APIs
- Creating a PaymentIntent
  - Best practices
- Passing the client secret to the client side
  - Retrieve the client secret
    - Caution
- After the payment
- Optimizing payment methods for future payments

Use the Payment Intents API to build an integration that can handle complex payment flows with a status that changes over the PaymentIntent’s lifecycle. It tracks a payment from creation through checkout, and triggers additional authentication steps when required.

Some of the advantages of using the Payment Intents API include:

Use the Payment Intents API together with the Setup Intents and Payment Methods APIs. These APIs help you handle dynamic payments (for example, additional authentication like 3D Secure) and prepare you for expansion to other countries while allowing you to support new regulations and regional payment methods.

Building an integration with the Payment Intents API involves two actions: creating and confirming a PaymentIntent. Each PaymentIntent typically correlates with a single shopping cart or customer session in your application. The PaymentIntent encapsulates details about the transaction, such as the supported payment methods, the amount to collect, and the desired currency.

To get started, see the accept a payment guide. It describes how to create a PaymentIntent on the server and pass its client secret to the client instead of passing the entire PaymentIntent object.

When you create the PaymentIntent, you can specify options like the amount and currency:

We recommend creating a PaymentIntent as soon as you know the amount, such as when the customer begins the checkout process, to help track your purchase funnel. If the amount changes, you can update its amount. For example, if your customer backs out of the checkout process and adds new items to their cart, you may need to update the amount when they start the checkout process again.

If the checkout process is interrupted and resumes later, attempt to reuse the same PaymentIntent instead of creating a new one. Each PaymentIntent has a unique ID that you can use to retrieve it if you need it again. In the data model of your application, you can store the ID of the PaymentIntent on the customer’s shopping cart or session to facilitate retrieval. The benefit of reusing the PaymentIntent is that the object state helps track any failed payment attempts for a given cart or session.

Remember to provide an idempotency key to prevent the creation of duplicate PaymentIntents for the same purchase. This key is typically based on the ID that you associate with the cart or customer session in your application.

The PaymentIntent contains a client secret, a key that’s unique to the individual PaymentIntent. On the client side of your application, Stripe.js uses the client secret as a parameter when invoking functions (such as stripe.confirmCardPayment or stripe.handleCardAction) to complete the payment.

The PaymentIntent includes a client secret that the client side uses to securely complete the payment process. You can use different approaches to pass the client secret to the client side.

Retrieve the client secret from an endpoint on your server, using the browser’s fetch function. This approach is best if your client side is a single-page application, particularly one built with a modern frontend framework like React. Create the server endpoint that serves the client secret:

And then fetch the client secret with JavaScript on the client side:

You can use the client secret to complete the payment process with the amount specified on the PaymentIntent. Don’t log it, embed it in URLs, or expose it to anyone other than the customer. Make sure that you have TLS on any page that includes the client secret.

After the client confirms the payment, it is a best practice for your server to monitor webhooks to detect when the payment successfully completes or fails.

A PaymentIntent might have more than one Charge object associated with it if there were multiple payment attempts. For example, retries can create multiple Charges. For each charge you can inspect the outcome and details of the payment method used.

The setup_future_usage parameter saves payment methods to use again in the future. For cards, it also optimizes authorization rates in compliance with regional legislation and network rules, such as SCA. To determine which value to use, consider how you want to use this payment method in the future.

You can still accept off-session payments with a card set up for on-session payments, but the bank is more likely to reject the off-session payment and require authentication from the cardholder.

The following example shows how to create a PaymentIntent and specify setup_future_usage:

Setups for off-session payments are more likely to incur additional friction. Use on-session setup if you don’t intend to accept off-session payments with the saved card.

By default, your Stripe account’s statement descriptor appears on customer statements whenever you charge their card. To provide a different description on a per-payment basis, include the statement_descriptor parameter.

Statement descriptors are limited to 22 characters, can’t use the special characters <, >, ', ", or *, and must not consist solely of numbers. When using dynamic statement descriptors, the dynamic text is appended to the statement descriptor prefix set in the Stripe Dashboard. An asterisk (*) and an empty space are also added to separate the default statement descriptor from the dynamic portion. These 2 characters count towards the 22 character limit.

Stripe supports adding metadata to the most common requests you make, such as processing payments. Metadata isn’t shown to customers or factored into whether or not a payment is declined or blocked by our fraud prevention system.

Through metadata, you can associate information that’s meaningful to you with Stripe activity.

Any metadata you include is viewable in the Dashboard (for example, when looking at the page for an individual payment), and is also available in common reports. As an example, you can attach the order ID for your store to the PaymentIntent for that order. Doing so allows you to easily reconcile payments in Stripe to orders in your system.

If you’re using Radar for Fraud Teams, consider passing additional customer information and order information as metadata. Then you can write Radar rules using metadata attributes and have more information available within the Dashboard, which can expedite your review process.

When a PaymentIntent creates a charge, the PaymentIntent copies its metadata to the charge. Subsequent updates to the PaymentIntent’s metadata won’t modify the metadata of charges previously created by the PaymentIntent.

Don’t store any sensitive information (personally identifiable information, card details, and so on) as metadata or in the description parameter of the PaymentIntent.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=1099 \
  -d currency=usd
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=1099 \
  -d currency=usd
```

Example 3 (unknown):
```unknown
get '/secret' do
  intent = # ... Create or retrieve the PaymentIntent
  {client_secret: intent.client_secret}.to_json
end
```

Example 4 (unknown):
```unknown
get '/secret' do
  intent = # ... Create or retrieve the PaymentIntent
  {client_secret: intent.client_secret}.to_json
end
```

---

## Accept offline payments

**URL:** https://docs.stripe.com/terminal/features/operate-offline/overview

**Contents:**
- Accept offline payments
- Accept payments when you have internet connectivity issues.
- Availability
  - Payment methods
  - Readers
  - Features
- Collect a payment while offline
  - Forward stored payments when online
- See also

If you have internet connectivity issues, Stripe Terminal allows you to store payments locally on your POS device or smart reader. When a network connection is restored, the SDK or smart reader automatically forwards any stored payments to Stripe.

From your application’s perspective, the payment collection process is similar to operating online. While offline, the smart reader or SDK securely stores the payment information and automatically forwards the stored payments when connectivity is restored. The SDK allows you to handle offline-related events using callbacks to your application.

1 Physical cards and NFC-based mobile wallets are supported. Swiping isn’t allowed. 2 If you’re collecting payments in the European Economic Area, customers are required to insert their card and enter a PIN. 3 Co-branded cards are routed through the international scheme. For more information, see Cartes Bancaires or eftpos Australia

The following diagram describes the payment collection process when the Terminal SDK is offline. When storing payments, the SDK stores the payments to disk. You can safely reboot the POS device even if it has stored offline payments. When you re-initialize the SDK and it has reestablished a connection to the internet, and the SDK resumes forwarding any remaining stored payments.

The following diagram describes how stored payments are forwarded after connectivity is restored.

---

## Save a customer's payment method without making a payment

**URL:** https://docs.stripe.com/payments/save-and-reuse

**Contents:**
- Save a customer's payment method without making a payment
- Learn how to save a payment method and charge it later.
    - Card-present transactions
- Compliance
    - Note
- Set up StripeServer-side
- Create a CustomerServer-side
    - Compare Customers v1 and Accounts v2 references
- Use setup modeServer-side
- Attach the payment method to a CustomerServer-side

The Checkout Sessions API in setup mode lets you save a customer’s payment details without an initial payment. This is helpful if you want to onboard customers now, set them up for payments, and charge them using the Payment Intents API in the future—when they’re offline.

Use this integration to set up recurring payments or to create one-time payments with a final amount determined later, often after the customer receives your service.

Card-present transactions, such as collecting card details through Stripe Terminal, use a different process for saving the payment method.

You’re responsible for your compliance with all applicable laws, regulations, and network rules when saving a customer’s payment details. These requirements generally apply if you want to save your customer’s payment method for future use, such as displaying a customer’s payment method to them in the checkout flow for a future purchase or charging them when they’re not actively using your website or app. Add terms to your website or app that state how you plan to save payment method details and allow customers to opt in.

When you save a payment method, you can only use it for the specific usage you have included in your terms. To charge a payment method when a customer is offline and save it as an option for future purchases, make sure that you explicitly collect consent from the customer for this specific use. For example, include a “Save my payment method for future use” checkbox to collect consent.

To charge a customer when they’re offline, make sure your terms include the following:

Make sure you keep a record of your customer’s written agreement to these terms.

If you need to use manual server-side confirmation or your integration requires presenting payment methods separately, see our alternative guide.

First, create a Stripe account or sign in.

Use our official libraries to access the Stripe API from your application:

To set up a payment method for future payments, you must attach it to a Customer. Create a Customer object when your customer creates an account with your business. Customer objects allow for reusing payment methods and tracking across multiple payments.

If your Connect platform uses customer-configured Accounts, use our guide to replace Customer and event references in your code with the equivalent Accounts v2 API references.

Create a Checkout Session with mode=setup.

If you didn’t create the Checkout Session with an existing customer, use the ID of the PaymentMethod to attach the payment method to a customer.

Otherwise, the payment method automatically attaches to the customer you provided when creating the Checkout Session.

After a customer successfully completes their Checkout Session, handle the checkout.session.completed webhook. Retrieve the Session object in the webhook, and then do the following:

Learn more about setting up webhooks.

After you attach the PaymentMethod to a customer, you can make an off-session payment using a PaymentIntent:

If a payment attempt fails, the request also fails with a 402 HTTP status code, and the PaymentIntent status is requires_payment_method. Notify your customer to return to your application (for example, by sending an email or in-app notification) and direct your customer to a new Checkout Session to select another payment method.

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

## Finalize payments on the server

**URL:** https://docs.stripe.com/payments/finalize-payments-on-the-server

**Contents:**
- Finalize payments on the server
- Build an integration where you render the Payment Element before you create a PaymentIntent or SetupIntent, then confirm the Intent from your server.
    - Compare Customers v1 and Accounts v2 references
- Set up StripeServer-side
- Enable payment methods
    - Caution
- Collect payment detailsClient-side
    - Conflicting iFrames
  - Set up Stripe.js
  - Add the Payment Element to your checkout page

If your Connect platform uses customer-configured Accounts, use our guide to replace Customer and event references in your code with the equivalent Accounts v2 API references.

The Payment Element allows you to accept multiple payment methods using a single integration. This integration builds a custom payment flow where you render the Payment Element, create the PaymentIntent, and confirm the payment from your server.

First, create a Stripe account or sign in.

Use our official libraries to access the Stripe API from your application:

This integration path doesn’t support BLIK or pre-authorized debits that use the Automated Clearing Settlement System (ACSS).

View your payment methods settings and enable the payment methods you want to support. You need at least one payment method enabled to create a PaymentIntent.

By default, Stripe enables cards and other prevalent payment methods that can help you reach more customers, but we recommend turning on additional payment methods that are relevant for your business and customers. See Payment method support for product and payment method support, and our pricing page for fees.

Use the Payment Element to securely send payment information collected in an iFrame to Stripe over an HTTPS connection.

Avoid placing the Payment Element within another iframe because it conflicts with payment methods that require redirecting to another page for payment confirmation.

Your checkout page URL must start with https:// rather than http:// for your integration to work. You can test your integration without using HTTPS, but remember to enable it when you’re ready to accept live payments.

The Payment Element is automatically available as a feature of Stripe.js. Include the Stripe.js script on your checkout page by adding it to the head of your HTML file. Always load Stripe.js directly from js.stripe.com to remain PCI compliant. Don’t include the script in a bundle or host a copy of it yourself.

Create an instance of Stripe with the following JavaScript on your checkout page:

The Payment Element needs a place to live on your checkout page. Create an empty DOM node (container) with a unique ID in your payment form:

After your form loads, create an Elements instance with the mode, amount, and currency. These values determine which payment methods the Element presents to your customer.

Then, create an instance of the Payment Element and mount it to the container DOM node.

The Payment Element renders a dynamic form that allows your customer to pick a payment method. The form automatically collects all necessary payments details for the payment method selected by the customer.

You can customize the Payment Element to match the design of your site by passing the appearance object into options when creating the Elements provider.

By default, the Payment Element only collects the necessary billing address details. Some behavior, such as calculating tax or entering shipping details, requires your customer’s full address. You can:

If you’re using a legacy implementation, you might be using the information from stripe.createPaymentMethod to finalize payments on the server. While we encourage you to follow this guide to Migrate to Confirmation Tokens you can still access our old documentation to Finalize payments on the server

When the customer submits your payment form, call stripe.createConfirmationToken to create a ConfirmationToken to send to your server for additional validation or business logic before payment confirmation.

Confirming the PaymentIntent generates a PaymentMethod. You can read the payment_method ID off the PaymentIntent confirmation response.

You must immediately use the created ConfirmationToken to confirm a PaymentIntent; if unused, it expires after 12 hours.

When the customer submits your payment form, use a PaymentIntent to facilitate the confirmation and payment process. Create a PaymentIntent on your server with an amount and currency specified. In the latest version of the API, specifying the automatic_payment_methods parameter is optional because Stripe enables its functionality by default. You can manage payment methods from the Dashboard. Stripe handles the return of eligible payment methods based on factors such as the transaction’s amount, currency, and payment flow. To prevent malicious customers from choosing their own prices, always decide how much to charge on the server-side (a trusted environment) and not the client.

You can use the ConfirmationToken sent by your client to create and confirm the PaymentIntent in a single request.

When the PaymentIntent requires additional action from the customer, such as authenticating with 3D Secure or redirecting to a different site, you need to trigger those actions. Use stripe.handleNextAction to trigger the UI for handling customer action and completing the payment.

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

## Search charges

**URL:** https://docs.stripe.com/api/charges/search

**Contents:**
- Search charges
  - Parameters
    - querystringRequired
    - limitinteger
    - pagestring
  - Returns

Search for charges you’ve previously created using Stripe’s Search Query Language. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.

The search query string. See search query language and the list of supported query fields for charges.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A dictionary with a data property that contains an array of up to limit charges. If no objects match the query, the resulting array will be empty. See the related guide on expanding properties in lists.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v1/charges/search \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  --data-urlencode query="amount>999 AND metadata['order_id']:'6735'"
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v1/charges/search \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  --data-urlencode query="amount>999 AND metadata['order_id']:'6735'"
```

Example 3 (unknown):
```unknown
{  "object": "search_result",  "url": "/v1/charges/search",  "has_more": false,  "data": [    {      "id": "ch_3MrVHGLkdIwHu7ix3VP9P8qH",      "object": "charge",      "amount": 1000,      "amount_captured": 1000,      "amount_refunded": 0,      "application": null,      "application_fee": null,      "application_fee_amount": null,      "balance_transaction": "txn_3MrVHGLkdIwHu7ix33fWgyw1",      "billing_details": {        "address": {          "city": null,          "country": null,          "line1": null,          "line2": null,          "postal_code": null,          "state": null        },        "email": null,        "name": null,        "phone": null      },      "calculated_statement_descriptor": "Stripe",      "captured": true,      "created": 1680220390,      "currency": "usd",      "customer": null,      "description": null,      "disputed": false,      "failure_balance_transaction": null,      "failure_code": null,      "failure_message": null,      "fraud_details": {},      "livemode": false,      "metadata": {        "order_id": "6735"      },      "on_behalf_of": null,      "outcome": {        "network_status": "approved_by_network",        "reason": null,        "risk_level": "normal",        "risk_score": 28,        "seller_message": "Payment complete.",        "type": "authorized"      },      "paid": true,      "payment_intent": null,      "payment_method": "card_1MrVHGLkdIwHu7ixi93aSYS2",      "payment_method_details": {        "card": {          "brand": "visa",          "checks": {            "address_line1_check": null,            "address_postal_code_check": null,            "cvc_check": null          },          "country": "US",          "exp_month": 3,          "exp_year": 2024,          "fingerprint": "mToisGZ01V71BCos",          "funding": "credit",          "installments": null,          "last4": "4242",          "mandate": null,          "network": "visa",          "network_token": {            "used": false          },          "three_d_secure": null,          "wallet": null        },        "type": "card"      },      "receipt_email": null,      "receipt_number": null,      "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xTTJKVGtMa2RJd0h1N2l4KOfBmKEGMgY6smXCZpA6LBZYyAwZTSPplSpB7KwcptJiKqQfv6nQiL75NRCxebjOIiABDK3odR96wc2r",      "refunded": false,      "review": null,      "shipping": null,      "source_transfer": null,      "statement_descriptor": null,      "statement_descriptor_suffix": null,      "status": "succeeded",      "transfer_data": null,      "transfer_group": null    }  ]}
```

Example 4 (unknown):
```unknown
{  "object": "search_result",  "url": "/v1/charges/search",  "has_more": false,  "data": [    {      "id": "ch_3MrVHGLkdIwHu7ix3VP9P8qH",      "object": "charge",      "amount": 1000,      "amount_captured": 1000,      "amount_refunded": 0,      "application": null,      "application_fee": null,      "application_fee_amount": null,      "balance_transaction": "txn_3MrVHGLkdIwHu7ix33fWgyw1",      "billing_details": {        "address": {          "city": null,          "country": null,          "line1": null,          "line2": null,          "postal_code": null,          "state": null        },        "email": null,        "name": null,        "phone": null      },      "calculated_statement_descriptor": "Stripe",      "captured": true,      "created": 1680220390,      "currency": "usd",      "customer": null,      "description": null,      "disputed": false,      "failure_balance_transaction": null,      "failure_code": null,      "failure_message": null,      "fraud_details": {},      "livemode": false,      "metadata": {        "order_id": "6735"      },      "on_behalf_of": null,      "outcome": {        "network_status": "approved_by_network",        "reason": null,        "risk_level": "normal",        "risk_score": 28,        "seller_message": "Payment complete.",        "type": "authorized"      },      "paid": true,      "payment_intent": null,      "payment_method": "card_1MrVHGLkdIwHu7ixi93aSYS2",      "payment_method_details": {        "card": {          "brand": "visa",          "checks": {            "address_line1_check": null,            "address_postal_code_check": null,            "cvc_check": null          },          "country": "US",          "exp_month": 3,          "exp_year": 2024,          "fingerprint": "mToisGZ01V71BCos",          "funding": "credit",          "installments": null,          "last4": "4242",          "mandate": null,          "network": "visa",          "network_token": {            "used": false          },          "three_d_secure": null,          "wallet": null        },        "type": "card"      },      "receipt_email": null,      "receipt_number": null,      "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xTTJKVGtMa2RJd0h1N2l4KOfBmKEGMgY6smXCZpA6LBZYyAwZTSPplSpB7KwcptJiKqQfv6nQiL75NRCxebjOIiABDK3odR96wc2r",      "refunded": false,      "review": null,      "shipping": null,      "source_transfer": null,      "statement_descriptor": null,      "statement_descriptor_suffix": null,      "status": "succeeded",      "transfer_data": null,      "transfer_group": null    }  ]}
```

---

## More payment scenarios

**URL:** https://docs.stripe.com/payments/more-payment-scenarios

**Contents:**
- More payment scenarios
- Find a payments integration to support your use case.

The Payment Intents and Setup Intents APIs handle any changing regulations and bank behaviors for you. Tell Stripe how you intend to use a payment method and we’ll route payments in a way that can improve payment acceptance rates.

---

## Charges

**URL:** https://docs.stripe.com/api/charges

**Contents:**
- Charges
- The Charge object
  - Attributes
    - idstring
    - amountinteger
    - balance_transactionnullable stringExpandable
    - billing_detailsobject
    - currencyenum
    - customernullable stringExpandable
    - descriptionnullable string

The Charge object represents a single attempt to move money into your Stripe account. PaymentIntent confirmation is the most common way to create Charges, but Account Debits may also create Charges. Some legacy payment flows create Charges directly, which is not recommended for new integrations.

Unique identifier for the object.

Amount intended to be collected by this payment. A positive integer representing how much to charge in the smallest currency unit (e.g., 100 cents to charge $1.00 or 100 to charge ¥100, a zero-decimal currency). The minimum amount is $0.50 US or equivalent in charge currency. The amount value supports up to eight digits (e.g., a value of 99999999 for a USD charge of $999,999.99).

ID of the balance transaction that describes the impact of this charge on your account balance (not including refunds or disputes).

Billing information associated with the payment method at the time of the transaction.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

ID of the customer this charge is for if one exists.

An arbitrary string attached to the object. Often useful for displaying to users.

Whether the charge has been disputed.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

ID of the PaymentIntent associated with this charge, if one exists.

Details about the payment method at the time of the transaction.

This is the email address that the receipt for this charge was sent to.

Whether the charge has been fully refunded. If the charge is only partially refunded, this attribute will still be false.

Shipping information for the charge.

For a non-card charge, text that appears on the customer’s statement as the statement descriptor. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

For a card charge, this value is ignored unless you don’t specify a statement_descriptor_suffix, in which case this value is used as the suffix.

Provides information about a card charge. Concatenated to the account’s statement descriptor prefix to form the complete statement descriptor that appears on the customer’s statement. If the account has no prefix value, the suffix is concatenated to the account’s statement descriptor.

The status of the payment is either succeeded, pending, or failed.

This method is no longer recommended—use the Payment Intents API to initiate a new payment instead. Confirmation of the PaymentIntent creates the Charge object used to request payment.

Amount intended to be collected by this payment. A positive integer representing how much to charge in the smallest currency unit (e.g., 100 cents to charge $1.00 or 100 to charge ¥100, a zero-decimal currency). The minimum amount is $0.50 US or equivalent in charge currency. The amount value supports up to eight digits (e.g., a value of 99999999 for a USD charge of $999,999.99).

Three-letter ISO currency code, in lowercase. Must be a supported currency.

The ID of an existing customer that will be charged in this request.

The maximum length is 500 characters.

An arbitrary string which you can attach to a Charge object. It is displayed when in the web interface alongside the charge. Note that if you use Stripe to send automatic email receipts to your customers, your receipt emails will include the description of the charge(s) that they are describing.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The email address to which this charge’s receipt will be sent. The receipt will not be sent until the charge is paid, and no receipts will be sent for test mode charges. If this charge is for a Customer, the email address specified here will override the customer’s email address. If receipt_email is specified for a charge in live mode, a receipt will be sent regardless of your email settings.

The maximum length is 800 characters.

Shipping information for the charge. Helps prevent fraud on charges for physical goods.

A payment source to be charged. This can be the ID of a card (i.e., credit or debit card), a bank account, a source, a token, or a connected account. For certain sources—namely, cards, bank accounts, and attached sources—you must also pass the ID of the associated customer.

For a non-card charge, text that appears on the customer’s statement as the statement descriptor. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

For a card charge, this value is ignored unless you don’t specify a statement_descriptor_suffix, in which case this value is used as the suffix.

Provides information about a card charge. Concatenated to the account’s statement descriptor prefix to form the complete statement descriptor that appears on the customer’s statement. If the account has no prefix value, the suffix is concatenated to the account’s statement descriptor.

Returns the charge object if the charge succeeded. This call raises an error if something goes wrong. A common source of error is an invalid or expired card, or a valid card with insufficient available balance.

Updates the specified charge by setting the values of the parameters passed. Any parameters not provided will be left unchanged.

The ID of an existing customer that will be associated with this request. This field may only be updated if there is no existing associated customer with this charge.

An arbitrary string which you can attach to a charge object. It is displayed when in the web interface alongside the charge. Note that if you use Stripe to send automatic email receipts to your customers, your receipt emails will include the description of the charge(s) that they are describing.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

This is the email address that the receipt for this charge will be sent to. If this field is updated, then a new email receipt will be sent to the updated address.

Shipping information for the charge. Helps prevent fraud on charges for physical goods.

Returns the charge object if the update succeeded. This call will raise an error if update parameters are invalid.

Retrieves the details of a charge that has previously been created. Supply the unique charge ID that was returned from your previous request, and Stripe will return the corresponding charge information. The same information is returned when creating or refunding the charge.

Returns a charge if a valid identifier was provided, and raises an error otherwise.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "ch_3MmlLrLkdIwHu7ix0snN0B15",  "object": "charge",  "amount": 1099,  "amount_captured": 1099,  "amount_refunded": 0,  "application": null,  "application_fee": null,  "application_fee_amount": null,  "balance_transaction": "txn_3MmlLrLkdIwHu7ix0uke3Ezy",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": null,    "phone": null  },  "calculated_statement_descriptor": "Stripe",  "captured": true,  "created": 1679090539,  "currency": "usd",  "customer": null,  "description": null,  "disputed": false,  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "fraud_details": {},  "livemode": false,  "metadata": {},  "on_behalf_of": null,  "outcome": {    "network_status": "approved_by_network",    "reason": null,    "risk_level": "normal",    "risk_score": 32,    "seller_message": "Payment complete.",    "type": "authorized"  },  "paid": true,  "payment_intent": null,  "payment_method": "card_1MmlLrLkdIwHu7ixIJwEWSNR",  "payment_method_details": {    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": null      },      "country": "US",      "exp_month": 3,      "exp_year": 2024,      "fingerprint": "mToisGZ01V71BCos",      "funding": "credit",      "installments": null,      "last4": "4242",      "mandate": null,      "network": "visa",      "three_d_secure": null,      "wallet": null    },    "type": "card"  },  "receipt_email": null,  "receipt_number": null,  "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xTTJKVGtMa2RJd0h1N2l4KOvG06AGMgZfBXyr1aw6LBa9vaaSRWU96d8qBwz9z2J_CObiV_H2-e8RezSK_sw0KISesp4czsOUlVKY",  "refunded": false,  "review": null,  "shipping": null,  "source_transfer": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "succeeded",  "transfer_data": null,  "transfer_group": null}
```

Example 2 (unknown):
```unknown
{  "id": "ch_3MmlLrLkdIwHu7ix0snN0B15",  "object": "charge",  "amount": 1099,  "amount_captured": 1099,  "amount_refunded": 0,  "application": null,  "application_fee": null,  "application_fee_amount": null,  "balance_transaction": "txn_3MmlLrLkdIwHu7ix0uke3Ezy",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": null,    "phone": null  },  "calculated_statement_descriptor": "Stripe",  "captured": true,  "created": 1679090539,  "currency": "usd",  "customer": null,  "description": null,  "disputed": false,  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "fraud_details": {},  "livemode": false,  "metadata": {},  "on_behalf_of": null,  "outcome": {    "network_status": "approved_by_network",    "reason": null,    "risk_level": "normal",    "risk_score": 32,    "seller_message": "Payment complete.",    "type": "authorized"  },  "paid": true,  "payment_intent": null,  "payment_method": "card_1MmlLrLkdIwHu7ixIJwEWSNR",  "payment_method_details": {    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": null      },      "country": "US",      "exp_month": 3,      "exp_year": 2024,      "fingerprint": "mToisGZ01V71BCos",      "funding": "credit",      "installments": null,      "last4": "4242",      "mandate": null,      "network": "visa",      "three_d_secure": null,      "wallet": null    },    "type": "card"  },  "receipt_email": null,  "receipt_number": null,  "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xTTJKVGtMa2RJd0h1N2l4KOvG06AGMgZfBXyr1aw6LBa9vaaSRWU96d8qBwz9z2J_CObiV_H2-e8RezSK_sw0KISesp4czsOUlVKY",  "refunded": false,  "review": null,  "shipping": null,  "source_transfer": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "succeeded",  "transfer_data": null,  "transfer_group": null}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/charges \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=1099 \  -d currency=usd \  -d source=tok_visa
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/charges \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=1099 \  -d currency=usd \  -d source=tok_visa
```

---

## Build two-step confirmation

**URL:** https://docs.stripe.com/payments/build-a-two-step-confirmation

**Contents:**
- Build two-step confirmation
- Add an optional review page or run validations after a user enters their payment details.
- Set up Stripe
- Enable payment methods
    - Caution
- Collect payment detailsClient-side
    - Conflicting iFrames
  - Set up Stripe.js
  - Add the Payment Element to your checkout page
  - Collect addresses

While we recommend the standard integration for most scenarios, this integration allows you to add an extra step in your checkout. This allows you to perform other actions before confirming the order, such as:

First, you need a Stripe account. Register now.

Use our official libraries for access to the Stripe API from your application:

This integration path doesn’t support BLIK or pre-authorized debits that use the Automated Clearing Settlement System (ACSS).

View your payment methods settings and enable the payment methods you want to support. You need at least one payment method enabled to create a PaymentIntent.

By default, Stripe enables cards and other prevalent payment methods that can help you reach more customers, but we recommend turning on additional payment methods that are relevant for your business and customers. See Payment method support for product and payment method support, and our pricing page for fees.

Use the Payment Element to securely send payment information collected in an iFrame to Stripe over an HTTPS connection.

Avoid placing the Payment Element within another iframe because it conflicts with payment methods that require redirecting to another page for payment confirmation.

Your checkout page URL must start with https:// rather than http:// for your integration to work. You can test your integration without using HTTPS, but remember to enable it when you’re ready to accept live payments.

The Payment Element is automatically available as a feature of Stripe.js. Include the Stripe.js script on your checkout page by adding it to the head of your HTML file. Always load Stripe.js directly from js.stripe.com to remain PCI compliant. Don’t include the script in a bundle or host a copy of it yourself.

Create an instance of Stripe with the following JavaScript on your checkout page:

The Payment Element needs a place to live on your checkout page. Create an empty DOM node (container) with a unique ID in your payment form:

After your form loads, create an Elements instance with the mode, amount, and currency. These values determine which payment methods the Element presents to your customer.

Then, create an instance of the Payment Element and mount it to the container DOM node.

The Payment Element renders a dynamic form that allows your customer to pick a payment method. The form automatically collects all necessary payments details for the payment method selected by the customer.

You can customize the Payment Element to match the design of your site by passing the appearance object into options when creating the Elements provider.

By default, the Payment Element only collects the necessary billing address details. Some behavior, such as calculating tax or entering shipping details, requires your customer’s full address. You can:

If you’re using a legacy implementation, you might be using the information from stripe.createPaymentMethod to finalize payments on the server. Although we encourage you to follow this guide to Migrate to Confirmation Tokens, you can still access our old documentation to Build two-step confirmation.

When the customer submits your payment form, call stripe.createConfirmationToken to create a ConfirmationToken to send to your server for additional validation or business logic before confirmation. You can inspect the payment_method_preview field to run the additional logic.

At this point, you have all of the information you need to render the confirmation page. Call the server to obtain the necessary information and render the confirmation page accordingly.

Navigate to step 5 in the finalize payments guide to run your custom business logic immediately before payment confirmation. Otherwise, follow the steps below for a simpler integration, which uses stripe.confirmPayment on the client to both confirm the payment and handle any next actions.

When the customer submits your payment form, create a PaymentIntent on your server with an amount and currency enabled.

Return the client secret value to your client for Stripe.js to use to complete the payment process.

The following example includes commented code to illustrate the optional Tax Calculation.

Use stripe.confirmPayment to complete the payment using details from the Payment Element.

Provide the confirmation_token parameter with the ID of the ConfirmationToken you created on the previous page, which contains the payment information collected from the Payment Element.

Provide a return_url to this function to indicate where Stripe redirects the user after they complete the payment. Your user might be initially redirected to an intermediate site, such as a bank authorization page, before being redirected to the return_url. Card payments immediately redirect to the return_url when a payment is successful.

If you don’t want to redirect for card payments after payment completion, you can set redirect to if_required. This only redirects customers that check out with redirect-based payment methods.

Stripe collects information on customer interactions with Elements to provide services to you, prevent fraud, and improve its services. This includes using cookies and IP addresses to identify which Elements a customer saw during a single checkout session. You’re responsible for disclosing and obtaining all rights and consents necessary for Stripe to use data in these ways. For more information, visit our privacy center.

Design an integration

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

## Accept a payment

**URL:** https://docs.stripe.com/payments/accept-a-payment?platform=web

**Contents:**
- Accept a payment
- Securely accept payments online.
  - Integration effort
  - Integration type
  - UI customization
- Redirect your customer to Stripe CheckoutClient-sideServer-side
    - Note
  - Payment methods
  - Confirm your endpoint
  - Testing

Build a payment form or use a prebuilt checkout page to start accepting online payments.

Redirect to a Stripe-hosted payment page using Stripe Checkout. See how this integration compares to Stripe’s other integration types.

Redirect to Stripe-hosted payment page

First, register for a Stripe account.

Use our official libraries to access the Stripe API from your application:

Add a checkout button to your website that calls a server-side endpoint to create a Checkout Session.

You can also create a Checkout Session for an existing customer, allowing you to prefill Checkout fields with known contact information and unify your purchase history for that customer.

A Checkout Session is the programmatic representation of what your customer sees when they’re redirected to the payment form. You can configure it with options such as:

You must populate success_url with the URL value of a page on your website that Checkout returns your customer to after they complete the payment.

Checkout Sessions expire 24 hours after creation by default.

After creating a Checkout Session, redirect your customer to the URL returned in the response.

By default, Stripe enables cards and other common payment methods. You can turn individual payment methods on or off in the Stripe Dashboard. In Checkout, Stripe evaluates the currency and any restrictions, then dynamically presents the supported payment methods to the customer.

To see how your payment methods appear to customers, enter a transaction ID or set an order amount and currency in the Dashboard.

You can enable Apple Pay and Google Pay in your payment methods settings. By default, Apple Pay is enabled and Google Pay is disabled. However, in some cases Stripe filters them out even when they’re enabled. We filter Google Pay if you enable automatic tax without collecting a shipping address.

Checkout’s Stripe-hosted pages don’t need integration changes to enable Apple Pay or Google Pay. Stripe handles these payments the same way as other card payments.

Confirm your endpoint is accessible by starting your web server (for example, localhost:4242) and running the following command:

You should see a response in your terminal that looks like this:

You should now have a working checkout button that redirects your customer to Stripe Checkout.

If your integration isn’t working:

It’s important for your customer to see a success page after they successfully submit the payment form. Host this success page on your site.

Create a minimal success page:

Next, update the Checkout Session creation endpoint to use this new page:

If you want to customize your success page, read the custom success page guide.

Next, find the new payment in the Stripe Dashboard. Successful payments appear in the Dashboard’s list of payments. When you click a payment, it takes you to the payment details page. The Checkout summary section contains billing information and the list of items purchased, which you can use to manually fulfill the order.

Stripe sends a checkout.session.completed event when a customer completes a Checkout Session payment. Use the Dashboard webhook tool or follow the webhook guide to receive and handle these events, which might trigger you to:

Listen for these events rather than waiting for your customer to be redirected back to your website. Triggering fulfillment only from your Checkout landing page is unreliable. Setting up your integration to listen for asynchronous events allows you to accept different types of payment methods with a single integration.

Learn more in our fulfillment guide for Checkout.

Handle the following events when collecting payments with the Checkout:

To test your Stripe-hosted payment form integration:

Learn more about testing your integration.

See Testing for additional information to test your integration.

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

## Additional payment methodsPublic preview

**URL:** https://docs.stripe.com/terminal/payments/additional-payment-methods

**Contents:**
- Additional payment methodsPublic preview
- Accept supported payment methods by displaying a QR code on Terminal smart readers.
    - Note
- Create a PaymentIntent
  - Capture type
- Handle the payment
    - Note
  - API reference
  - Free up the reader to take another payment
- Customer experience

Terminal’s smart readers can display transaction-specific QR codes for payment methods besides cards. Your customers can then scan this code to complete their checkout on their mobile devices.

The flow below shows a payment that supports both card and non-card payment methods. Alternatively, if you want to support multiple non-card payment methods without accepting cards, the reader bypasses the tap or insert prompt and instead shows the menu of non-card payment method options. If you want to support a single non-card payment method, the reader loads the QR code directly.

For US-based readers, don’t use setReaderDisplay if you only want to support QR-based payment methods in your checkout flow. The setReaderDisplay screen shows the NFC logo and supports pre-dipping cards to tokenize card details before a PaymentIntent is created.

Collect payment method screen

Payment method selection screen

Supported payment methods: WeChat Pay1, Affirm, and PayNow

Supported readers: Stripe Reader S700, BBPOS WisePOS E

1WeChat Pay isn’t available for Terminal in Japan due to regional limitations.

Connected accounts must have the requisite capability to perform transactions for each payment method. Learn more about Connect compatibility with Affirm, WeChat Pay, and PayNow.

To test non-card payment methods on Stripe Terminal, use a physical reader. The simulated reader isn’t supported.

All transactions must be made with a functional network connection, not while offline.

To accept non-card payment methods through the QR code interface, create a PaymentIntent and include your preferred payment method types in the payment_method_types parameter.

Many payment methods don’t support manual capture. Create your PaymentIntent with the capture_method parameter automatic to support the broadest set of payment methods. To support manual capture for card payments while also accepting payment methods that require automatic capture, set capture_method on the nested payment_method_options.card_present attribute to manual.

Unlike card payments, processing QR code payments occurs asynchronously. When processing a PaymentIntent with a QR code payment method, Stripe generates a QR code unique to that payment. After processing the payment, the reader displays the QR code for the customer to scan with their mobile device. Shortly after the customer completes the payment on their device, the reader updates to reflect the completed payment.

The time it takes for the reader to display the result of the payment might differ depending on the payment method used. The reader usually updates after a few seconds.

QR code payments support both processing the payment immediately and the two-step collect-and-confirm flow.

To collect payment, make a request to Stripe with the ID of the PaymentIntent you created and the reader you want to use for the transaction.

Some payment methods (for example, Affirm) require a return_url when confirming a PaymentIntent to redirect your customer to after they authenticate or cancel their payment on the payment method’s app or site. You can provide your own return_url when processing the PaymentIntent. If you don’t provide one, the customer sees a generic landing page hosted by Stripe.

When you process a payment, Stripe immediately responds to the request with an HTTP 200 status code as an acknowledgement that the reader received the action. In most cases, the request returns a reader with an in_progress status. However, because processing occurs asynchronously, the action status might already reflect the final state (succeeded or failed) if the payment completes quickly.

Simultaneously, the reader screen switches to a UI that prompts the customer to insert their card or select a QR code payment method. For QR code payments, the customer completing the payment on their device updates the status of the payment. To verify the reader state, listen to the terminal.reader.action_succeeded webhook or poll the Reader and PaymentIntent status to receive the status of the payment.

It might take multiple minutes for a customer to complete the payment on their device. Instead of waiting for the reader to reflect the result of the completed payment, you can free up the reader to take a payment for a different customer.

After the customer scans the QR code and switches to their device to complete the payment, use the cancel_action endpoint to reset the reader.

After you cancel the reader’s action to process the payment, the payment intent remains in the requires_action state, allowing the customer to complete the payment. Use the payment_intent.succeeded and payment_intent.payment_failed webhooks to reconcile the result of the completed payment. Learn how to monitor a PaymentIntent with webhooks.

After you process the PaymentIntent, the customer scans a QR code rendered on the reader screen. Depending on the payment method, the customer might quickly finalize the payment in their mobile application (most digital wallets), or complete a more extended process of evaluating financing offers (BNPL payment methods). Below are demonstrations of the payment flow for supported payment methods:

Learn more about how to provide the best customer experience and promote awareness of BNPL options in a store through these Affirm training resources.

In a sandbox, you can scan the QR code using a regular QR code scanning application on your mobile phone. The QR code payload contains a URL that takes you to a Stripe-hosted test payment page where you can choose to authorize or decline the test payment.

If your account is onboarded with Affirm, the QR code URL takes you to an Affirm-hosted sandbox page where you can complete the payment process. When you’re redirected to the Affirm sandbox, you might receive a prompt to enter the last four digits of your SSN. Affirm recommends using either 0000 or 5678 for testing purposes.

If your account isn’t onboarded with Affirm, you’ll be directed to the Stripe-hosted test payment page.

The present_payment_method endpoint doesn’t support specifying QR code payment method types.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=1000 \
  -d currency=usd \
  -d "payment_method_types[]"=card_present \
  -d "payment_method_types[]"=wechat_pay \
  -d capture_method=automatic \
  -d "payment_method_options[card_present][capture_method]"=manual
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=1000 \
  -d currency=usd \
  -d "payment_method_types[]"=card_present \
  -d "payment_method_types[]"=wechat_pay \
  -d capture_method=automatic \
  -d "payment_method_options[card_present][capture_method]"=manual
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/readers/tmr_xxx/process_payment_intent \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d payment_intent=pi_xxx \
  --data-urlencode "process_config[return_url]"="https://my.store.com/payment-completed"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/readers/tmr_xxx/process_payment_intent \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d payment_intent=pi_xxx \
  --data-urlencode "process_config[return_url]"="https://my.store.com/payment-completed"
```

---

## Capture a charge

**URL:** https://docs.stripe.com/api/charges/capture

**Contents:**
- Capture a charge
  - Parameters
    - amountinteger
    - receipt_emailstring
    - statement_descriptorstring
    - statement_descriptor_suffixstring
  - More parametersExpand all
    - application_fee_amountintegerConnect only
    - transfer_dataobjectConnect only
    - transfer_groupstringConnect only

Capture the payment of an existing, uncaptured charge that was created with the capture option set to false.

Uncaptured payments expire a set number of days after they are created (7 by default), after which they are marked as refunded and capture attempts will fail.

Don’t use this method to capture a PaymentIntent-initiated charge. Use Capture a PaymentIntent.

The amount to capture, which must be less than or equal to the original amount.

The email address to send this charge’s receipt to. This will override the previously-specified email address for this charge, if one was set. Receipts will not be sent in test mode.

The maximum length is 800 characters.

For a non-card charge, text that appears on the customer’s statement as the statement descriptor. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

For a card charge, this value is ignored unless you don’t specify a statement_descriptor_suffix, in which case this value is used as the suffix.

Provides information about a card charge. Concatenated to the account’s statement descriptor prefix to form the complete statement descriptor that appears on the customer’s statement. If the account has no prefix value, the suffix is concatenated to the account’s statement descriptor.

Returns the charge object, with an updated captured property (set to true). Capturing a charge will always succeed, unless the charge is already refunded, expired, captured, or an invalid capture amount is specified, in which case this method will raise an error.

Search for charges you’ve previously created using Stripe’s Search Query Language. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.

The search query string. See search query language and the list of supported query fields for charges.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A dictionary with a data property that contains an array of up to limit charges. If no objects match the query, the resulting array will be empty. See the related guide on expanding properties in lists.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/charges/ch_3MrVHGLkdIwHu7ix1mN3zEiP/capture \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/charges/ch_3MrVHGLkdIwHu7ix1mN3zEiP/capture \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "ch_3MrVHGLkdIwHu7ix1mN3zEiP",  "object": "charge",  "amount": 1099,  "amount_captured": 1099,  "amount_refunded": 0,  "application": null,  "application_fee": null,  "application_fee_amount": null,  "balance_transaction": "txn_3MrVHGLkdIwHu7ix1Yb1LdXJ",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": null,    "phone": null  },  "calculated_statement_descriptor": "Stripe",  "captured": true,  "created": 1680220390,  "currency": "usd",  "customer": null,  "description": null,  "destination": null,  "dispute": null,  "disputed": false,  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "fraud_details": {},  "livemode": false,  "metadata": {},  "on_behalf_of": null,  "order": null,  "outcome": {    "network_status": "approved_by_network",    "reason": null,    "risk_level": "normal",    "risk_score": 0,    "seller_message": "Payment complete.",    "type": "authorized"  },  "paid": true,  "payment_intent": null,  "payment_method": "card_1MrVHGLkdIwHu7ix7H1PgERt",  "payment_method_details": {    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": null      },      "country": "US",      "exp_month": 3,      "exp_year": 2024,      "fingerprint": "mToisGZ01V71BCos",      "funding": "credit",      "installments": null,      "last4": "4242",      "mandate": null,      "network": "visa",      "network_token": {        "used": false      },      "three_d_secure": null,      "wallet": null    },    "type": "card"  },  "receipt_email": null,  "receipt_number": null,  "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xTTJKVGtMa2RJd0h1N2l4KOfBmKEGMgarecoy8cU6LBYTBSk6QLeqixDK3Wp7agsQfREj3vSXJTrg8SjoxhuNjSJzxMcN6QHTlEDG",  "refunded": false,  "review": null,  "shipping": null,  "source": {    "id": "card_1MrVHGLkdIwHu7ix7H1PgERt",    "object": "card",    "address_city": null,    "address_country": null,    "address_line1": null,    "address_line1_check": null,    "address_line2": null,    "address_state": null,    "address_zip": null,    "address_zip_check": null,    "brand": "Visa",    "country": "US",    "customer": null,    "cvc_check": null,    "dynamic_last4": null,    "exp_month": 3,    "exp_year": 2024,    "fingerprint": "mToisGZ01V71BCos",    "funding": "credit",    "last4": "4242",    "metadata": {},    "name": null,    "tokenization_method": null  },  "source_transfer": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "succeeded",  "transfer_data": null,  "transfer_group": null}
```

Example 4 (unknown):
```unknown
{  "id": "ch_3MrVHGLkdIwHu7ix1mN3zEiP",  "object": "charge",  "amount": 1099,  "amount_captured": 1099,  "amount_refunded": 0,  "application": null,  "application_fee": null,  "application_fee_amount": null,  "balance_transaction": "txn_3MrVHGLkdIwHu7ix1Yb1LdXJ",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": null,    "phone": null  },  "calculated_statement_descriptor": "Stripe",  "captured": true,  "created": 1680220390,  "currency": "usd",  "customer": null,  "description": null,  "destination": null,  "dispute": null,  "disputed": false,  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "fraud_details": {},  "livemode": false,  "metadata": {},  "on_behalf_of": null,  "order": null,  "outcome": {    "network_status": "approved_by_network",    "reason": null,    "risk_level": "normal",    "risk_score": 0,    "seller_message": "Payment complete.",    "type": "authorized"  },  "paid": true,  "payment_intent": null,  "payment_method": "card_1MrVHGLkdIwHu7ix7H1PgERt",  "payment_method_details": {    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": null      },      "country": "US",      "exp_month": 3,      "exp_year": 2024,      "fingerprint": "mToisGZ01V71BCos",      "funding": "credit",      "installments": null,      "last4": "4242",      "mandate": null,      "network": "visa",      "network_token": {        "used": false      },      "three_d_secure": null,      "wallet": null    },    "type": "card"  },  "receipt_email": null,  "receipt_number": null,  "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xTTJKVGtMa2RJd0h1N2l4KOfBmKEGMgarecoy8cU6LBYTBSk6QLeqixDK3Wp7agsQfREj3vSXJTrg8SjoxhuNjSJzxMcN6QHTlEDG",  "refunded": false,  "review": null,  "shipping": null,  "source": {    "id": "card_1MrVHGLkdIwHu7ix7H1PgERt",    "object": "card",    "address_city": null,    "address_country": null,    "address_line1": null,    "address_line1_check": null,    "address_line2": null,    "address_state": null,    "address_zip": null,    "address_zip_check": null,    "brand": "Visa",    "country": "US",    "customer": null,    "cvc_check": null,    "dynamic_last4": null,    "exp_month": 3,    "exp_year": 2024,    "fingerprint": "mToisGZ01V71BCos",    "funding": "credit",    "last4": "4242",    "metadata": {},    "name": null,    "tokenization_method": null  },  "source_transfer": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "succeeded",  "transfer_data": null,  "transfer_group": null}
```

---

## Upgrade your integration

**URL:** https://docs.stripe.com/payments/upgrades

**Contents:**
- Upgrade your integration
- Increase conversion and get access to new features by upgrading your integration.
- Payment integration upgrades
- Feature upgrades

Discover the recommended options for upgrading both your entire payments integration, and individual features. For a comprehensive list of changes to the API, see API upgrades.

Take advantage of new features by upgrading your existing integration.

We recommend upgrading these features to enhance your checkout process.

---

## Wallets

**URL:** https://docs.stripe.com/payments/wallets

**Contents:**
- Wallets
- Learn about wallet payments with Stripe.
- Payment flow
  - Customer-facing mobile flow
  - Customer-facing web flow
- Product support
- API support

Customers can use wallets to pay online with a saved card or a digital wallet balance. Retailers often use wallets to:

Wallets might not be a good fit for your business if you sell subscriptions. Some wallets don’t support recurring payments.

Customers confirm the transaction by authenticating their wallet credentials at checkout. If using mobile, they can authenticate with fingerprint or face recognition, their mobile passcode, or by logging into their wallet app. On the web, they can also scan a QR code with their mobile phone to complete the transaction.

Selects wallet at checkout

Enters wallet credentials

Gets notification that payment is complete

Selects wallet at checkout

Uses mobile to confirm payment

Gets notification that payment is complete

The following table shows which Stripe products support each wallet:

1 Not supported when using Checkout in subscription mode.2 Not supported when using Checkout in setup mode.3 Not supported when saving payment details during payment (setup_future_usage).4 Invoices and Subscriptions only support the send_invoice collection method.5 Checkout with ui_mode set to embedded supports only Safari version 17 or later and iOS version 17 or later.6 The Payment Element doesn’t support Link in Brazil or India.7 Stripe doesn’t display Apple Pay or Google Pay for IP addresses in India.8 Request an invite to use Connect.

The following table describes each wallet’s compatibility with API-based payment flows:

1 Cards and bank debit methods including SEPA debit, AU BECS direct debit, and ACSS debit support both on_session and off_session with setup future usage. All other payment method types either don’t support setup_future_usage or only support off_session.2 Payment methods might require confirmation with return_url to indicate where Stripe should redirect your customer after they complete the payment.

---

## Payment Method Configurations

**URL:** https://docs.stripe.com/api/payment_method_configurations

**Contents:**
- Payment Method Configurations
- The Payment Method Configuration object
  - Attributes
    - idstringretrievable with publishable key
    - objectstring
    - activeboolean
    - applicationnullable string
    - is_defaultboolean
    - namestring
    - parentnullable string

PaymentMethodConfigurations control which payment methods are displayed to your customers when you don’t explicitly specify payment method types. You can have multiple configurations with different sets of payment methods for different scenarios.

There are two types of PaymentMethodConfigurations. Which is used depends on the charge type:

Direct configurations apply to payments created on your account, including Connect destination charges, Connect separate charges and transfers, and payments not involving Connect.

Child configurations apply to payments created on your connected accounts using direct charges, and charges with the on_behalf_of parameter.

Child configurations have a parent that sets default values and controls which settings connected accounts may override. You can specify a parent ID at payment time, and Stripe will automatically resolve the connected account’s associated child configuration. Parent configurations are managed in the dashboard and are not available in this API.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value.

Whether the configuration can be used for new payments.

For child configs, the Connect application associated with the configuration.

The default configuration is used whenever a payment method configuration is not specified.

The configuration’s name.

For child configs, the configuration’s parent configuration.

Creates a payment method configuration

The maximum length is 100 characters.

Configuration’s parent configuration. Specify to create a child configuration.

The maximum length is 100 characters.

Returns the payment method configuration object

Update payment method configuration

Whether the configuration can be used for new payments.

The maximum length is 100 characters.

An object with the updated account payment method configuration

Retrieve payment method configuration

A payment method configuration object.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "pmc_abcdef",  "object": "payment_method_configuration",  "acss_debit": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "active": true,  "affirm": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "afterpay_clearpay": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "alipay": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "apple_pay": {    "available": true,    "display_preference": {      "overridable": null,      "preference": "on",      "value": "on"    }  },  "bancontact": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "card": {    "available": true,    "display_preference": {      "overridable": null,      "preference": "on",      "value": "on"    }  },  "cartes_bancaires": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "eps": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "giropay": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "google_pay": {    "available": true,    "display_preference": {      "overridable": null,      "preference": "on",      "value": "on"    }  },  "ideal": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "is_default": true,  "klarna": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "link": {    "available": true,    "display_preference": {      "overridable": null,      "preference": "on",      "value": "on"    }  },  "livemode": false,  "name": "Default",  "p24": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "sepa_debit": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "sofort": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "us_bank_account": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "wechat_pay": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  }}
```

Example 2 (unknown):
```unknown
{  "id": "pmc_abcdef",  "object": "payment_method_configuration",  "acss_debit": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "active": true,  "affirm": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "afterpay_clearpay": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "alipay": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "apple_pay": {    "available": true,    "display_preference": {      "overridable": null,      "preference": "on",      "value": "on"    }  },  "bancontact": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "card": {    "available": true,    "display_preference": {      "overridable": null,      "preference": "on",      "value": "on"    }  },  "cartes_bancaires": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "eps": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "giropay": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "google_pay": {    "available": true,    "display_preference": {      "overridable": null,      "preference": "on",      "value": "on"    }  },  "ideal": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "is_default": true,  "klarna": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "link": {    "available": true,    "display_preference": {      "overridable": null,      "preference": "on",      "value": "on"    }  },  "livemode": false,  "name": "Default",  "p24": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "sepa_debit": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "sofort": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "us_bank_account": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  },  "wechat_pay": {    "available": false,    "display_preference": {      "overridable": null,      "preference": "off",      "value": "off"    }  }}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_method_configurations \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d name="Buy Now Pay Laters"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_method_configurations \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d name="Buy Now Pay Laters"
```

---

## Refund and cancel payments

**URL:** https://docs.stripe.com/refunds

**Contents:**
- Refund and cancel payments
- Learn how to cancel or refund a payment.
- Refund requests
- Issue refunds
    - Bulk refunds
  - Refunds through a Connect platform
- Refund destinations
- Handle failed refunds
- Cancel a refund
- Refund and reversal

You can cancel a payment before it’s completed at no cost. Or you can refund all or part of a payment after it succeeds, which might incur a fee. Go to our pricing page for more information.

Refunds use your available Stripe balance (not including pending amounts). If your available balance doesn’t cover the amount of the refund, Stripe holds the refund as pending until your Stripe balance becomes sufficient. You can resolve a negative Stripe balance by collecting payments or topping up your account balance. In regions where applicable, Stripe might debit your bank accounts automatically to recover a negative Stripe balance.

We submit refund requests to your customer’s bank or card issuer. Successful refunds appear on the bank statement of your customers in real time, depending on the card network and issuing bank. Disputes and chargebacks aren’t possible on credit card charges that are fully refunded.

If all of the following conditions apply, we send an email to your customer notifying them of the refund:

You can view your refunded payments in the Dashboard.

You can issue refunds by using the Refunds API or the Dashboard. You can issue more than one refund against a charge, but you can’t refund a total greater than the original charge amount.

To refund a payment using the Dashboard:

Alternatively, you can click on a specific payment and issue a refund from its details page. You can also send refund receipts automatically or manually send a receipt for each refund.

The Dashboard supports the bulk refunding of full payments. Select what payments you want to refund by checking the box to the left of each payment—even over multiple pages of results. Then, click Refund and select a reason. You can only issue full refunds in this way; partial refunds must be issued individually.

Refund behavior depends on the Connect charge type used in your integration.

Connect platforms can enable their connected accounts to provide refunds to customers from their site by using Connect embedded components such as the payments or the payment details component.

Refunds can only be sent back to the original payment method used in a charge. You can’t send a refund to a different destination, such as another card or bank account.

Refunds to expired or canceled cards are handled by the customer’s card issuer and, in most cases, credited to the customer’s replacement card. If no replacement exists, the card issuer usually delivers the refund to the customer using an alternate method (for example, check or bank account deposit). In rare cases, a refund back to a card might fail.

For other payment methods, like ACH and iDEAL, refund handling varies from bank to bank. If a customer has closed their method of payment, the bank might return the refund to us—at which point it’s marked as failed.

A refund can fail if the customer’s bank or card issuer can’t process it. For example, a closed bank account or a problem with the card can cause a refund to fail. When this happens, the bank returns the refunded amount to us and we add it back to your Stripe account balance. This process can take up to 30 days from the post date.

When using the API, a Refund object’s status transitions to failed and includes these attributes:

For some payment methods, the decline code provided by our financial partners, which indicates the reason the refund failed, is available in the network_decline_code field of the destination_details hash:

In the rare instance that a refund fails, we notify you using the refund.failed event (see all refund-related events). If this occurs, you need to arrange an alternative way to provide your customer with a refund.

If your platform uses Connect with destination charges, funds from a failed refund deposit to your platform account’s Stripe balance.

Depending on the type of refund, you might be able to cancel a refund before it reaches the customer. Some card refunds support cancellation for a short period of time. The refund must not have been processed as a charge reversal. Only Dashboard cancellations are currently supported for card refunds.

For some payment methods, Stripe reaches out to the customer to collect banking information before processing the refund. You can cancel these refunds while banking information hasn’t been collected. Both the API and Dashboard cancellations are supported for this type of refund.

Canceled refunds transit to a canceled status. As cancellations are a type of refund failure, the attributes failure_reason and failure_balance_transaction are included on the Refund.

If your platform uses Connect with destination charges, funds from a cancelled refund deposit to your platform account’s Stripe balance.

To cancel a refund using the Dashboard:

Alternatively, you can click a specific payment and cancel the refund from its details page.

Some refunds—those issued shortly after the original charge—appear in the form of a reversal instead of a refund. In the case of a reversal, the original charge drops off the customer’s statement, and a separate credit isn’t issued.

IC+ users might see a difference in cost between reversals and refunds because reversals usually incur lower network fees.

To verify if a refund goes through as a reversal on the Dashboard:

After you initiate a refund, Stripe submits refund requests to your customer’s bank or card issuer. Your customer sees the refund as a credit approximately 5-10 business days later, depending upon the bank. A customer might contact you if they don’t see the refund. A refund might not be visible to the customer for several reasons:

If a customer is asking about a refund, it can be helpful to give them the primary reference number corresponding to the refund. For card refunds, it can be an Acquirer Reference Number (ARN), System Trace Audit Number (STAN), or Retrieval Reference Number (RRN). An ARN, STAN, or RRN is a reference number assigned to a card transaction as it moves through the payment flow. For local payment method refunds, it can be a reference number generated by Stripe or our financial partners which is propagated to the beneficiary banks or institutions. Your customer can then take this reference to their bank, which can provide more information about when the refund is available. Having a reference number can also increase your customer’s confidence that the refund has been initiated.

Refund references are available under the following conditions:

To find the reference of a refund using the Dashboard:

You can cancel a payment using the Dashboard only when its status is uncaptured. To cancel a payment with other statuses, you must use the API.

To cancel uncaptured payments using the Dashboard:

Stripe triggers events every time a refund is created or changed. Some other actions, like reviews closing, also trigger events that are relevant to refunds.

Make sure that your integration is set up to handle events. You must also build internal logic for notifying customers or your team about the state of the refund process. At a minimum, Stripe recommends that you listen for the refund.created event.

The following table describes the most common events related to refunds.

If your business processes a large volume of refunds close to the time of transaction, we recommend using manual authorization and capture to reduce your refund costs. Manual authorization and capture lets you better control costs by canceling payments before they’re captured, or by reducing your captured amount rather than processing a refund.

**Examples:**

Example 1 (unknown):
```unknown
{
  id: "pyr_1234",
  destination_details: {
    blik: {
      network_decline_code: "decline_code"
    },
    type: 'blik',
  }
}
```

Example 2 (unknown):
```unknown
{
  id: "pyr_1234",
  destination_details: {
    blik: {
      network_decline_code: "decline_code"
    },
    type: 'blik',
  }
}
```

---

## Accept a payment

**URL:** https://docs.stripe.com/payments/accept-a-payment

**Contents:**
- Accept a payment
- Securely accept payments online.
  - Integration effort
  - Integration type
  - UI customization
- Redirect your customer to Stripe CheckoutClient-sideServer-side
    - Note
  - Payment methods
  - Confirm your endpoint
  - Testing

Build a payment form or use a prebuilt checkout page to start accepting online payments.

Redirect to a Stripe-hosted payment page using Stripe Checkout. See how this integration compares to Stripe’s other integration types.

Redirect to Stripe-hosted payment page

First, register for a Stripe account.

Use our official libraries to access the Stripe API from your application:

Add a checkout button to your website that calls a server-side endpoint to create a Checkout Session.

You can also create a Checkout Session for an existing customer, allowing you to prefill Checkout fields with known contact information and unify your purchase history for that customer.

A Checkout Session is the programmatic representation of what your customer sees when they’re redirected to the payment form. You can configure it with options such as:

You must populate success_url with the URL value of a page on your website that Checkout returns your customer to after they complete the payment.

Checkout Sessions expire 24 hours after creation by default.

After creating a Checkout Session, redirect your customer to the URL returned in the response.

By default, Stripe enables cards and other common payment methods. You can turn individual payment methods on or off in the Stripe Dashboard. In Checkout, Stripe evaluates the currency and any restrictions, then dynamically presents the supported payment methods to the customer.

To see how your payment methods appear to customers, enter a transaction ID or set an order amount and currency in the Dashboard.

You can enable Apple Pay and Google Pay in your payment methods settings. By default, Apple Pay is enabled and Google Pay is disabled. However, in some cases Stripe filters them out even when they’re enabled. We filter Google Pay if you enable automatic tax without collecting a shipping address.

Checkout’s Stripe-hosted pages don’t need integration changes to enable Apple Pay or Google Pay. Stripe handles these payments the same way as other card payments.

Confirm your endpoint is accessible by starting your web server (for example, localhost:4242) and running the following command:

You should see a response in your terminal that looks like this:

You should now have a working checkout button that redirects your customer to Stripe Checkout.

If your integration isn’t working:

It’s important for your customer to see a success page after they successfully submit the payment form. Host this success page on your site.

Create a minimal success page:

Next, update the Checkout Session creation endpoint to use this new page:

If you want to customize your success page, read the custom success page guide.

Next, find the new payment in the Stripe Dashboard. Successful payments appear in the Dashboard’s list of payments. When you click a payment, it takes you to the payment details page. The Checkout summary section contains billing information and the list of items purchased, which you can use to manually fulfill the order.

Stripe sends a checkout.session.completed event when a customer completes a Checkout Session payment. Use the Dashboard webhook tool or follow the webhook guide to receive and handle these events, which might trigger you to:

Listen for these events rather than waiting for your customer to be redirected back to your website. Triggering fulfillment only from your Checkout landing page is unreliable. Setting up your integration to listen for asynchronous events allows you to accept different types of payment methods with a single integration.

Learn more in our fulfillment guide for Checkout.

Handle the following events when collecting payments with the Checkout:

To test your Stripe-hosted payment form integration:

Learn more about testing your integration.

See Testing for additional information to test your integration.

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

## Testing

**URL:** https://docs.stripe.com/testing?testing-method=payment-methods

**Contents:**
- Testing
- Simulate payments to test your integration.
- How to use test cards
    - Don't use real card details
  - Testing interactively
  - Test code
- Cards by brand
- Cards by country
    - Security tip
    - Security tip

To test your integration, simulate transactions without moving any money using special testing values in a sandbox. You can access your sandboxes using the account picker at the top right of the page or in the Dashboard.

Test cards act as fake credit cards, and allow you to simulate the following scenarios:

Testing non-card payments works similarly. Non-card payments are payment methods that aren’t credit or debit cards. Stripe supports various non-card payment options, such as digital wallets and bank transfers. Each payment method has its own special values.

Don’t use testing environments to load test your integration because you might hit rate limits. To load test your integration, see load testing.

Any time you work with a test card, use test API keys in all API calls. This is true whether you’re serving a payment form to test interactively or writing test code.

Don’t use real card details. The Stripe Services Agreement prohibits testing in live mode using real payment method details. Use your test API keys and the card numbers below.

When testing interactively, use a card number, such as 4242 4242 4242 4242. Enter the card number in the Dashboard or in any payment form.

When writing test code, use a PaymentMethod such as pm_card_visa instead of a card number. We don’t recommend using card numbers directly in API calls or server-side code, even in testing environments. If you do use them, your code might not be PCI-compliant when you go live. By default, a PaymentMethod isn’t attached to a Customer.

Most integrations don’t use Tokens anymore, but we make test Tokens such as tok_visa available if you need them.

When you’re ready to take your integration live, replace your test publishable and secret API keys with live ones. You can’t process live payments if your integration is still using your test API keys.

To simulate a successful payment for a specific card brand, use test cards from the following list.

Cross-border fees are assessed based on the country of the card issuer. Cards where the issuer country isn’t the US (such as JCB and UnionPay) might be subject to a cross-border fee, even in testing environments.

Most Cartes Bancaires and eftpos cards are co-branded with either Visa or Mastercard. The test cards in the following table simulate successful payments with co-branded cards.

To simulate successful payments from specific countries, use test cards from the following sections.

Strong Customer Authentication regulations require 3D Secure authentication for online payments within the European Economic Area. The test cards in the Europe and Middle East section simulate a payment that succeeds without authentication. We also recommend testing authentication scenarios using 3D Secure test cards.

Strong Customer Authentication regulations require 3D Secure authentication for online payments within the European Economic Area. The test cards in this section simulate a payment that succeeds without authentication. We recommend also testing scenarios that involve authentication, using 3D Secure test cards.

To test subscriptions that require mandates and pre-debit notifications, see India recurring payments.

Below are test card numbers for simulating transactions using Health Savings Accounts (HSA) and Flexible Spending Accounts (FSA). These accounts are commonly used for medical expenses, and testing with them ensures proper handling of healthcare-related transactions within your application.

To test your integration’s error-handling logic by simulating payments that the issuer declines for various reasons, use test cards from this section. Using one of these cards results in a card error with the given error code and decline code.

To simulate an incorrect CVC, you must provide one using any three-digit number. If you don’t provide a CVC, Stripe doesn’t perform the CVC check, so the check can’t fail.

The cards in the previous table can’t be attached to a Customer object. To simulate a declined payment with a successfully attached card, use the next one.

Stripe’s fraud prevention system, Radar, can block payments when they have a high risk level or fail verification checks. You can use the cards in this section to test your Radar settings. You can also use them to test how your integration responds to blocked payments.

Each card simulates specific risk factors. Your Radar settings determine which risk factors cause it to block a payment. Blocked payments result in card errors with an error code of fraud.

To simulate a failed CVC check, you must provide a CVC using any three-digit number. To simulate a failed postal code check, you must provide any valid postal code. If you don’t provide those values, Radar doesn’t perform the corresponding checks, so the checks can’t fail.

The charge has a risk level of “highest”

Radar always blocks it.

pm_card_riskLevelHighest

The charge has a risk level of “highest”

Radar might block it depending on your settings.

pm_card_riskLevelElevated

The charge has a risk level of “elevated”

If you use Radar for Fraud Teams, Radar might queue it for review.

If you provide a CVC number, the CVC check fails.

Radar might block it depending on your settings.

Postal code check fails

If you provide a postal code, the postal code check fails.

Radar might block it depending on your settings.

CVC check fails with elevated risk

pm_card_cvcCheckFailElevatedRisk

If you provide a CVC number, the CVC check fails with a risk level of “elevated”

Radar might block it depending on your settings.

Postal code check fails with elevated risk

pm_card_avsZipFailElevatedRisk

If you provide a postal code, the postal code check fails with a risk level of “elevated”

Radar might block it depending on your settings.

The address line 1 check fails.

The payment succeeds unless you block it with a custom Radar rule.

The address postal code check and address line 1 check both fail.

Radar might block it depending on your settings.

The address postal code check and address line 1 check are both unavailable.

The payment succeeds unless you block it with a custom Radar rule.

To test errors resulting from invalid data, provide invalid details. You don’t need a special test card for this. Any invalid value works. For instance:

To simulate a disputed transaction, use the test cards in this section. Then, to simulate winning or losing the dispute, provide winning or losing evidence.

To simulate winning or losing the dispute, respond with one of the evidence values from the table below.

In live mode, refunds are asynchronous: a refund can appear to succeed and later fail, or can appear as pending at first and later succeed. To simulate refunds with those behaviors, use the test cards in this section. (With all other test cards, refunds succeed immediately and don’t change status after that.)

You can cancel a card refund only by using the Dashboard. In live mode, you can cancel a card refund within a short but nonspecific period of time. Testing environments simulate that period by allowing you to cancel a card refund within 30 minutes.

To send the funds from a test transaction directly to your available balance, use the test cards in this section. Other test cards send funds from a successful payment to your pending balance.

3D Secure requires an additional layer of authentication for credit card transactions. The test cards in this section allow you to simulate triggering authentication in different payment flows.

Only cards in this section effectively test your 3D Secure integration by simulating defined 3DS behavior, such as a challenge flow or an unsupported card. Other Stripe testing cards might still trigger 3DS, but we return attempt_acknowledged to bypass the additional steps since 3DS testing isn’t the objective for those cards.

3D Secure redirects won’t occur for payments created directly in the Stripe Dashboard. Instead, use your integration’s own frontend or an API call.

To simulate payment flows that include authentication, use the test cards in this section. Some of these cards can also be set up for future payments, or have already been.

Stripe requests authentication when required by regulation or when triggered by your Radar rules or custom code. Even if authentication is requested, it can’t always be performed—for instance, the customer’s card might not be enrolled, or an error might occur. Use the test cards in this section to simulate various combinations of these factors.

All 3DS references indicate 3D Secure 2.

In a mobile payment, several challenge flows for authentication—where the customer has to interact with prompts in the UI—are available. Use the test cards in this section to trigger a specific challenge flow for test purposes. These cards aren’t useful in browser-based payment forms or in API calls. In those environments, they work but don’t trigger any special behavior. Because they’re not useful in API calls, we don’t provide any PaymentMethod or Token values to test with.

To prevent fraud, Stripe might display a captcha challenge to the user on the payment page. Use the test cards below to simulate this flow.

Use the test cards in this section to simulate successful in-person payments where a PIN is involved. There are many other options for testing in-person payments, including a simulated reader and physical test cards. See Test Stripe Terminal for more information.

To test your webhook endpoint or event destination, choose one of these two options:

If your requests in your testing environments begin to receive 429 HTTP errors, make them less frequently. These errors come from our rate limiter, which is more strict in testing environments than in live mode.

We don’t recommend load testing your integration using the Stripe API in testing environments. Because the load limiter is stricter in testing environments, you might see errors that you wouldn’t see in production. See load testing for an alternative approach.

Any time you use a test non-card payment method, use test API keys in all API calls. This is true whether you’re serving a payment form you can test interactively or writing test code.

Different payment methods have different test procedures:

Learn how to test scenarios with instant verifications using Financial Connections.

After you collect the bank account details and accept a mandate, send the mandate confirmation and microdeposit verification emails in a sandbox.

If your domain is {domain} and your username is {username}, use the following email format to send test transaction emails: {username}+test_email@{domain}.

For example, if your domain is example.com and your username is info, use the format info+test_email@example.com for testing ACH Direct Debit payments. This format ensures that emails route correctly. If you don’t include the +test_email suffix, we won’t send the email.

You need to activate your Stripe account before you can trigger these emails while testing.

Stripe provides several test account numbers and corresponding tokens you can use to make sure your integration for manually-entered bank accounts is ready for production.

Before test transactions can complete, you need to verify all test accounts that automatically succeed or fail the payment. To do so, use the test microdeposit amounts or descriptor codes below.

To mimic different scenarios, use these microdeposit amounts or 0.01 descriptor code values.

Test transactions settle instantly and are added to your available test balance. This behavior differs from livemode, where transactions can take multiple days to settle in your available balance.

Don’t store real user data in sandbox Link accounts. Treat them as if they’re publicly available, because these test accounts are associated with your publishable key.

Currently, Link only works with credit cards, debit cards, and qualified US bank account purchases. Link requires domain registration.

You can create sandbox accounts for Link using any valid email address. The following table shows the fixed one-time passcode values that Stripe accepts for authenticating sandbox accounts:

As Stripe adds additional funding source support, you don’t need to update your integration. Stripe automatically supports them with the same transaction settlement time and guarantees as card and bank account payments.

To test your integration’s redirect-handling logic by simulating a payment that uses a redirect flow (for example, iDEAL), use a supported payment method that requires redirects.

To create a test PaymentIntent that either succeeds or fails:

Make sure that the page (corresponding to return_url) on your website provides the status of the payment.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=500 \
  -d currency=gbp \
  -d payment_method=pm_card_visa \
  -d "payment_method_types[]"=card
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=500 \
  -d currency=gbp \
  -d payment_method=pm_card_visa \
  -d "payment_method_types[]"=card
```

---

## Collect card payments

**URL:** https://docs.stripe.com/terminal/payments/collect-card-payment

**Contents:**
- Collect card payments
- Prepare your application and back end to collect card payments using Stripe Terminal.
  - Learn More
    - Note
- Create a PaymentIntent
  - API reference
    - Common mistake
- Process the payment
  - API reference
- Capture the payment

For BBPOS WisePOS E and Stripe Reader S700, we recommend server-side integration because it uses the Stripe API instead of a Terminal SDK to collect payments.

New to the Payment Intents API? Here are some helpful resources:

Collecting payments with Stripe Terminal requires writing a payment flow in your application. Use the Stripe Terminal SDK to create and update a PaymentIntent, an object representing a single payment session.

While the core concepts are similar to SDK-based integrations, you follow slightly different steps with the server-driven integration:

This integration shape doesn’t support offline card payments.

The first step in collecting payments is to start the payment flow. When a customer begins checking out, your backend must create a PaymentIntent object that represents a new payment session on Stripe. With the server-driven integration, you create the PaymentIntent server-side.

In a sandbox, you can use test amounts to simulate different error scenarios. In live mode, the amount of the PaymentIntent displays on the reader for payment.

For Terminal payments, the payment_method_types parameter must include card_present.

To accept Interac payments in Canada, you must also include interac_present in payment_method_types. Learn about regional considerations for Canada.

To accept non-card payment methods in supported countries, you must also specify your preferred types in payment_method_types. Learn about additional payment methods.

You can control the payment flow as follows:

Don’t recreate a PaymentIntent if a card is declined. Instead, re-use the same PaymentIntent to help avoid double charges.

You can process a payment immediately with the card presented by a customer, or instead inspect card details before proceeding to process the payment. For most use cases, we recommend processing immediately, as it is a simpler integration with less API calls and webhook events. However, if you would like to insert your own business logic before the card is authorized, you can use the two-step collect-and-confirm flow.

After you create a PaymentIntent, the next step is to process the payment. The reader prompts the customer to insert or tap their card and then authorizes the payment.

To collect payment, make a request to Stripe with the ID of the PaymentIntent you created and the reader you want to use for the transaction.

Processing the payment happens asynchronously. A cardholder might take a few seconds to get their card from their wallet or pose a question to the operator during payment. When you process a payment, Stripe immediately responds to the request with an HTTP 200 status code as an acknowledgement that the reader received the action. In most cases, the request returns a reader with an in_progress status. However, because processing occurs asynchronously, the action status might already reflect the final state (succeeded or failed) if the payment completes quickly.

Simultaneously, the reader screen switches to a UI that prompts the customer to insert their card. To verify the reader state, listen to the terminal.reader.action_succeeded webhook or poll the Reader and PaymentIntent status to receive the status of the payment.

If you’re using a simulated reader, use the present_payment_method endpoint to simulate a cardholder tapping or inserting their card on the reader. Use test cards to simulate different success or failure scenarios.

If you defined capture_method as manual during PaymentIntent creation in Step 1, the SDK returns an authorized but not captured PaymentIntent to your application. Learn more about the difference between authorization and capture. When your application receives a confirmed PaymentIntent, make sure it notifies your backend to capture the PaymentIntent. To do so, create an endpoint on your backend that accepts a PaymentIntent ID and sends a request to the Stripe API to capture it.

A successful capture call results in a PaymentIntent with a status of succeeded.

You must manually capture PaymentIntents within two days or the authorization expires and funds are released to the customer.

To make sure the reader completed an action, your application must verify the reader state before initiating a new reader action or continuing to capture the payment. In most cases, this verification allows you to confirm a successful (approved) payment and show any relevant UX to your operator for them to complete the transaction. In other cases, you might need to handle errors, including declined payments.

Use one of the following to check the reader status:

For maximum resiliency, we recommend your application listens to webhooks from Stripe to receive real-time notifications of the reader status. Stripe sends three webhooks to notify your application of a reader’s action status:

To listen for these webhooks, create a webhook endpoint. We recommend having a dedicated webhook endpoint for only these events because they’re high priority and in the critical payment path.

In case of webhook delivery issues, you can poll the Stripe API by adding a check status button to your point-of-sale interface that the operator can invoke, if needed.

You can retrieve the PaymentIntent that you passed to the reader for processing. When you create a PaymentIntent it has an initial status of requires_payment_method. After you successfully collect the payment method, the status updates to requires_confirmation. After the payment processes successfully, the status updates to requires_capture.

You can use the Reader object, which contains an action attribute that shows the latest action received by the reader and its status. Your application can retrieve a Reader to check if the status of the reader action has changed.

The Reader object is also returned as the response to the process payment step. The action type when processing a payment is process_payment_intent.

The action.status updates to succeeded for a successful payment. This means you can proceed with completing the transaction. Other values for action.status include failed or in_progress.

The following errors are the most common types your application needs to handle:

The PaymentIntent object enables money movement at Stripe—use a single PaymentIntent to represent a transaction.

Re-use the same PaymentIntent after a card is declined (for example, if it has insufficient funds), so your customer can try again with a different card.

If you edit the PaymentIntent, you must call process_payment_intent to update the payment information on the reader.

A PaymentIntent must be in the requires_payment_method state before Stripe can process it. An authorized, captured, or canceled PaymentIntent can’t be processed by a reader and results in an intent_invalid_state error:

The most common payment failure is a failed payment authorization (for example, a payment that’s declined by the customer’s bank due to insufficient funds).

When a payment authorization fails, Stripe sends the terminal.reader.action_failed webhook. Check the action.failure_code and action.failure_message attributes to know why a payment is declined:

In the case of a declined card, prompt the customer for an alternative form of payment. Use the same PaymentIntent in another request to the process_payment_intent endpoint. If you create a new PaymentIntent, you must cancel the failed PaymentIntent to prevent double charges.

For card read errors (for example, an error reading the chip), the reader automatically prompts the customer to retry without any notification to your application. If multiple retries fail, you can prompt for another payment method by making another process_payment_intent request.

A reader with unreliable internet connectivity can fail to process a payment because of a networking request timeout when authorizing the card. The reader shows a processing screen for several seconds, followed by a failure screen, and you receive a terminal.reader.action_failed webhook with a failure_code of connection_error:

The payment confirmation request might have been processed by Stripe’s backend systems, but the reader might have disconnected before receiving the response from Stripe. When receiving a webhook with this failure code, fetch the PaymentIntent status to verify if the payment is successfully authorized.

Make sure your network meets our network requirements to minimize timeouts.

You might need to cancel an in-flight payment. For example, if a customer adds items to their purchase after your integration has already initiated payment collection on the reader. Use the cancel_action endpoint to reset the reader:

You can’t cancel a reader action in the middle of a payment authorization. If a customer has already presented their card to pay on the reader, you must wait for processing to complete. An authorization normally takes a few seconds to complete. Calling cancel_action during an authorization results in a terminal_reader_busy error.

Users can set the value of enable_customer_cancellation on these endpoints:

When set to true, smart reader users see a cancel button.

Payment collection with cancellation enabled

Tapping the cancel button cancels the active transaction. Stripe sends a terminal.reader.action_failed webhook with a failure_code of customer_canceled.

A reader can process only one payment at a time. While it’s processing a payment, attempting a new payment fails with a terminal_reader_busy error:

Payments that have not begun processing can be replaced with a new payment.

A reader also rejects an API request if it’s busy performing updates, changing settings or if a card is inserted from the previous transaction.

On rare occasions, a reader might fail to respond to an API request on time because of temporary networking issues. If this happens, you receive a terminal_reader_timeout error code:

In this case, we recommend you retry the API request. Make sure your network meets our network requirements to minimize timeouts.

On rare occasions, a terminal_reader_timeout error code is a false negative. In this scenario, you receive a terminal_reader_timeout error from the API as described above, but the reader has actually received the command successfully. False negatives happen when Stripe sends a message to the reader, but doesn’t receive an acknowledgement back from the reader due to temporary networking failures.

A location losing its internet connection might result in interrupted communication between the reader and Stripe. In this case, a reader is unresponsive to events initiated from your point-of-sale application and backend infrastructure.

A reader that consistently fails to respond to API requests is most likely powered off (for example, the power cord is disconnected or it’s out of battery) or not correctly connected to the internet.

A reader is considered offline if Stripe hasn’t received any signal from that reader in the past 2 minutes. Attempting to call API methods on a reader that’s offline results in a terminal_reader_offline error code:

Refer to our network requirements to make sure a reader is correctly connected to the internet.

When a reader disconnects in the middle of a payment, it can’t update its action status in the API. In this scenario, the reader shows an error screen after a card is presented. However, the Reader object in the API doesn’t update to reflect the failure on the device, and you also don’t get reader action webhooks. A reader might be left with an action status of in_progress when this happens, and a cashier has to intervene by calling the cancel_action endpoint to reset the reader state.

On rare occasions, if Stripe is having an outage, reader action webhooks might be late. You can query the status of the Reader or the PaymentIntent objects to know what their latest state is.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d currency=usd \
  -d "payment_method_types[]"=card_present \
  -d capture_method=manual \
  -d amount=1000
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d currency=usd \
  -d "payment_method_types[]"=card_present \
  -d capture_method=manual \
  -d amount=1000
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/readers/tmr_xxx/process_payment_intent \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d payment_intent=pi_xxx
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/readers/tmr_xxx/process_payment_intent \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d payment_intent=pi_xxx
```

---

## Customers

**URL:** https://docs.stripe.com/api/customers

**Contents:**
- Customers
- The Customer object
  - Attributes
    - idstring
    - addressnullable object
    - customer_accountnullable string
    - descriptionnullable string
    - emailnullable string
    - metadataobject
    - namenullable string

This object represents a customer of your business. Use it to create recurring charges, save payment and contact information, and track payments that belong to the same customer.

Unique identifier for the object.

The customer’s address.

The ID of an Account representing a customer. You can use this ID with any v1 API that accepts a customer_account parameter.

An arbitrary string attached to the object. Often useful for displaying to users.

The customer’s email address.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The customer’s full name or business name.

The customer’s phone number.

Mailing and shipping address for the customer. Appears on invoices emailed to this customer.

Tax details for the customer.

The customer’s address. Learn about country-specific requirements for calculating tax.

An arbitrary string that you can attach to a customer object. It is displayed alongside the customer in the dashboard.

Customer’s email address. It’s displayed alongside the customer in your dashboard and can be useful for searching and tracking. This may be up to 512 characters.

The maximum length is 512 characters.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The customer’s full name or business name.

The maximum length is 256 characters.

The ID of the PaymentMethod to attach to the customer.

The customer’s phone number.

The maximum length is 20 characters.

The customer’s shipping information. Appears on invoices emailed to this customer.

Tax details about the customer.

Returns the Customer object after successful customer creation. Raises an error if create parameters are invalid (for example, specifying an invalid coupon or an invalid source).

Updates the specified customer by setting the values of the parameters passed. Any parameters not provided will be left unchanged. For example, if you pass the source parameter, that becomes the customer’s active source (e.g., a card) to be used for all charges in the future. When you update a customer to a new valid card source by passing the source parameter: for each of the customer’s current subscriptions, if the subscription bills automatically and is in the past_due state, then the latest open invoice for the subscription with automatic collection enabled will be retried. This retry will not count as an automatic retry, and will not affect the next regularly scheduled payment for the invoice. Changing the default_source for a customer will not trigger this behavior.

This request accepts mostly the same arguments as the customer creation call.

The customer’s address. Learn about country-specific requirements for calculating tax.

An arbitrary string that you can attach to a customer object. It is displayed alongside the customer in the dashboard.

Customer’s email address. It’s displayed alongside the customer in your dashboard and can be useful for searching and tracking. This may be up to 512 characters.

The maximum length is 512 characters.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The customer’s full name or business name.

The maximum length is 256 characters.

The customer’s phone number.

The maximum length is 20 characters.

The customer’s shipping information. Appears on invoices emailed to this customer.

Tax details about the customer.

Returns the customer object if the update succeeded. Raises an error if update parameters are invalid (e.g. specifying an invalid coupon or an invalid source).

Retrieves a Customer object.

Returns the Customer object for a valid identifier. If it’s for a deleted Customer, a subset of the customer’s information is returned, including a deleted property that’s set to true.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "cus_NffrFeUfNV2Hib",  "object": "customer",  "address": null,  "balance": 0,  "created": 1680893993,  "currency": null,  "default_source": null,  "delinquent": false,  "description": null,  "email": "jennyrosen@example.com",  "invoice_prefix": "0759376C",  "invoice_settings": {    "custom_fields": null,    "default_payment_method": null,    "footer": null,    "rendering_options": null  },  "livemode": false,  "metadata": {},  "name": "Jenny Rosen",  "next_invoice_sequence": 1,  "phone": null,  "preferred_locales": [],  "shipping": null,  "tax_exempt": "none",  "test_clock": null}
```

Example 2 (unknown):
```unknown
{  "id": "cus_NffrFeUfNV2Hib",  "object": "customer",  "address": null,  "balance": 0,  "created": 1680893993,  "currency": null,  "default_source": null,  "delinquent": false,  "description": null,  "email": "jennyrosen@example.com",  "invoice_prefix": "0759376C",  "invoice_settings": {    "custom_fields": null,    "default_payment_method": null,    "footer": null,    "rendering_options": null  },  "livemode": false,  "metadata": {},  "name": "Jenny Rosen",  "next_invoice_sequence": 1,  "phone": null,  "preferred_locales": [],  "shipping": null,  "tax_exempt": "none",  "test_clock": null}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/customers \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d name="Jenny Rosen" \  --data-urlencode email="jennyrosen@example.com"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/customers \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d name="Jenny Rosen" \  --data-urlencode email="jennyrosen@example.com"
```

---

## Online payments

**URL:** https://docs.stripe.com/payments/online-payments

**Contents:**
- Online payments
- Learn about your integration options for accepting payments online.
- Payment UIs
- Add payment methods
- Add Link for faster checkout
- Compare features and availability
  - Compare payment scenario support
  - Compare features
  - Compare product support
  - Detailed Billing feature support

Optimize your payments integration and increase revenue with the Optimized Checkout Suite, which includes payment UIs, dynamic payment methods, and faster checkout with Link. To get started, find the integration that meets your business needs or explore the demo to see how the features work.

Use prebuilt payment UIs to accept payments online.

Accept more payment methods to help your business expand its global reach and improve checkout conversion.

Simplify your payment methods code by dynamically ordering and displaying payment methods.

Launch an A/B test for a new payment method in the Dashboard.

Control when payment methods are available to your customers.

Create different sets of payment methods to display to customers based on specific checkout scenarios.

Use Link to let your customers select a saved payment method at checkout instead of entering payment information. Your customers can save their credit cards, debit cards, or US bank accounts for faster checkout at any Link-enabled business. Link also lets you accept Instant Bank Payments.

Use Link with the Stripe prebuilt payment page.

Embed Link into your custom payment page for faster checkout.

Add Link to your native iOS, Android, and React Native apps.

All integrations support one-time and recurring payments, fraud protection, and global payments.

1Limited customization provides 20 preset fonts, 3 preset border radius options, logo and background customization, and custom button color.

2For detailed support for each payment method, see learn more about payment methods.

3Wallet payment methods require registering your domain.

See how Stripe supports different payment scenarios by each integration path.

1 Not supported on Dashboard-created Payment Links.

2 Only available on IC+ pricing.

3 We’re actively working on supporting this feature and expect to launch in 2025.

1 Requires additional integration.

2 Available for subscriptions and invoices only.

3 We’re actively working on supporting this feature and expect to launch in 2025.

See how the various integration options work with other Stripe products.

1 Requires integration with Stripe Tax API.

2 Requires integration with Subscriptions API.

3 Requires integration with Terminal.

Stripe partners with thousands of popular platforms and supports plugins to bring Stripe payments into your website. See all of our integration solutions in our online directory.

---

## Testing Stripe Connect

**URL:** https://docs.stripe.com/connect/testing

**Contents:**
- Testing Stripe Connect
- Before going live, test your Connect integration for account creation, identity verification, and payouts.
    - Testing capabilities
- Create test accounts
- Test the OAuth flow
- Identity verification
  - Testing verification guide
  - Test dates of birth
  - Test addresses
  - Test personal ID numbers

Use testing to make sure your Connect integration handles different flows correctly. You can use Sandboxes to simulate live mode while taking advantage of Stripe-provided special tokens to use in your tests. See the payments testing guide for more information on testing charges, disputes, and so on.

Sandboxes and test mode might not enforce some capabilities. In certain cases, they can allow an account to perform capability-dependent actions even when the associated capability’s status isn’t active.

You can create multiple test accounts with different account types or controller properties that you want to test.

You can create test accounts using the Accounts API or in the Stripe Dashboard.

Use 000-000 as the SMS code when prompted for test accounts.

You can test your OAuth integration with connected accounts that use a Stripe-hosted Dashboard using your test client_id.

Your test client_id is ca_FkyHCg7X8mlvCUdMDao4mMxagUfhIwXb. You can find this in your Connect OAuth settings.

Your test client_id allows you to:

To test the OAuth flow, create a new account after clicking the OAuth link. You can also test connecting an existing Stripe account only if the email is different from your platform account.

Verification is a crucial component for onboarding accounts. Use our dedicated guide to testing verification.

After creating a test connected account, you can use tokens to test different verification statuses to make sure you’re handling different requirements and account states. You can use the following tokens to test verification with test accounts.

Use these dates of birth (DOB) to trigger certain verification conditions.

Use these addresses for line1 to trigger certain verification conditions. You must pass in legitimate values for the city, state, and postal_code arguments.

Use these personal ID numbers for the individual.id_number attribute on the Account or the id_number attribute on the Person object to trigger certain verification conditions.

For testing, use test images or file tokens instead of uploading your own test IDs. For details, refer to Uploading a file.

You can use a verified image that causes the ID number to match successfully. You can use an unverified image that causes a mismatch on the ID number, leading to currently_due requirements.

Test images take precedence over test ID numbers. If you upload a verified image, the ID number matching succeeds, even if you also provide an unsuccessful test ID value. Similarly, an unverified image automatically fails ID matching regardless of the value of other test artifacts.

Use these file tokens to trigger certain identity verification conditions.

In some countries, the business address associated with your connected account must be validated before charges, payouts, or both can be enabled on the connected account.

Use these addresses for line1 to trigger certain validation conditions. You must pass in legitimate values for the city, state, and postal_code arguments.

Make sure you start with an address token that has the least permissive validation condition you want to test for. This is because you can’t use an address token that has a more restrictive validation condition than the previous token used. For example, if you provided address_full_match to have both charges and payouts enabled, you can’t disable payouts or charges afterward by changing the token to an invalid one. You can work around this by creating a new account with the relevant token.

Use these business tax ID numbers for company.tax_id to trigger certain verification conditions. The test behavior might change depending on the Connected Account countries and the regulations in those countries. Depending on the country’s regulation, a valid tax document can mark tax ID verified in these countries.

Stripe performs directorship verification by comparing the list of directors on the Account object against a list retrieved from local registries. If the country requires it, you can trigger verification for an Account object by using these tokens for the first_name attribute on the associated Person and setting the relationship.director attribute on the Person to true.

The verification errors can trigger if multiple directors on the Account object use these magic tokens.

Trigger company name verification for an Account object by using this token for the company.name attribute.

Trigger statement descriptor verification for an Account object by using this token for the settings.payments.statement_descriptor attribute.

Trigger statement descriptor prefix verification for an Account object by using this token for the settings.card_payments.statement_descriptor_prefix attribute.

Trigger URL verification for an Account object by using this token for the business_profile.url attribute.

Trigger assignment of a specific requirements.disabled_reason to all of an Account object’s inactive Capability objects by using this token for the account’s business_profile.url attribute.

Trigger DBA verification for an Account object by using this token for the business_profile.name attribute.

Trigger product description verification for an Account object by using this token for the business_profile.product_description attribute.

Clear phone number validation for an Account object by using this token for the following attributes:

Clear phone number validation for a Person object by using this token for the phone attribute.

Use these card numbers to trigger various conditions when you’re testing both requirements and tiered verification. For the trigger actions to work, you must use these cards with a Connect charge by setting on_behalf_of or creating a direct charge on the connected account. The connected account must have an eventually_due requirement.

Live mode can require additional verification information when a connected account processes a certain amount of volume. This card sets any additional verification information to be required immediately. If no additional information is required, nothing appears.

If required information isn’t provided by the deadline, Stripe disables the connected account’s charges or payouts. These cards disable the connected account and move any currently due requirements to overdue. These cards have no effect until an account provides the initial information that’s required to enable charges and payouts.

Connected accounts in the United States and India are subject to Bank account ownership verification. You can complete this verification by uploading supporting documents with the Connect Dashboard or with the API through the documents[bank_account_ownership_verification] hash.

While you’re testing, you can simulate the US bank account ownership verification process. Use the following test bank account numbers to trigger the verification process. One number presumes successful verification and the other prompts you to upload test images or file tokens to complete the verification process. These test accounts are only available for US accounts.

To test adding funds to your Stripe balance from a bank account in the Dashboard, create a sandbox and select the desired test bank account in the dropdown menu within the Add to balance dialog. You can simulate success or failure due to insufficient funds.

To test adding funds in the API, use the following test bank tokens as the source while you’re testing. Each token simulates a specific kind of event.

Use the following test bank and debit card numbers to trigger certain events when testing payouts. You can only use these values while testing with test secret keys.

Test payouts simulate a live payout but aren’t processed with the bank. Test accounts with Stripe Dashboard access always have payouts enabled, as long as valid external bank information and other relevant conditions are met, and never requires real identity verification.

You can’t use test bank and debit card numbers in the Stripe Dashboard on a live mode connected account. If you’ve entered your bank account information on a live mode account, you can still use a sandbox, and test payouts will simulate a live payout without processing actual money.

Use these test bank account numbers to test payouts. You can only use them with test secret keys.

Use these test debit card numbers to test payouts to a debit card. You can only use them with test secret keys.

---

## Accept in-person payments with Terminal

**URL:** https://docs.stripe.com/terminal/overview

**Contents:**
- Accept in-person payments with Terminal
- Learn how Terminal works.
  - No-code integrations
- Features
- How Terminal works
- Use cases
- Scope of integration
- Encryption
  - Contact sales
- See also

Stripe partners with platforms that provide no-code POS solutions.

With Stripe Terminal, you can integrate Stripe payments into your existing in-person checkout flow or build in-person payments into your native mobile or web-based application.

Terminal comes with SDKs built for modern development environments, Tap to Pay on iPhone and Android, pre-certified readers, and tools for ordering and managing readers from the Stripe Dashboard. Build a SaaS platform or marketplace using Connect or initiate subscriptions in-store with Billing.

Learn about global availability for Terminal.

Use Terminal to take the complexity out of in-person payments:

A Stripe Terminal deployment consists of four main components:

The SDK facilitates communication between your point of sale application logic, the firmware running on the reader, and the Stripe API so you can accept in-person payments in the same way as you accept online payments with Stripe. The SDK is available for JavaScript, iOS, Android applications. You can develop desktop applications using a server-driven integration.

Stripe Terminal offers a selection of pre-certified readers that accept payment details (EMV, contactless, and swiped), encrypt sensitive card information, and return a token to your application (through the Stripe Terminal SDK) so you can confirm payment.

Stripe Terminal works only with our pre-certified card readers and compatible Tap to Pay iPhone and Android devices. This ensures secure transactions by our end-to-end encryption, by default, and up-to-date readers through our remote management tools.

You can order readers and accessories from the Stripe Dashboard and get them shipped to a location of your choice. As a Connect platform, you can even enable your connected accounts to receive readers and accessories at their business location.

Stripe Terminal is built with developers in mind. Its flexible design supports a wide range of use cases:

Choose an SDK that works best for you and combine it with a reader that works best for you. This documentation provides all the information you need to design your in-person payments solution, order readers and accessories, integrate, and deploy.

The full scope of an integration consists of four major steps.

From there, explore the docs to see all you can do with your Terminal integration. We recommend testing your integration and reviewing the checklist before going live.

Businesses using Terminal for in-person payments can choose between two levels of encryption. All payments using Terminal are securely encrypted using end-to-end encryption (E2EE) by default. Businesses in certain industries, such as healthcare and education, can also use the PCI-audited point-to-point encryption (P2PE) solution from Stripe.

Stripe P2PE is an optional, paid feature. See pricing for more information. If you’re interested in P2PE, contact your sales representative to discuss whether P2PE is a good fit for your business.

P2PE standards, which are developed by the PCI Council, add an additional decryption step through hardware security modules (HSM) before Stripe sends payment data to card networks. Our P2PE solution simplifies PCI compliance and reduces PCI audit scope and audit costs. It’s validated by a third party, ensuring compliance with PCI P2PE standards, and doesn’t require any additional integration to get started.

If you’ve enabled P2PE, consult the P2PE Instruction Manual (PIM) for detailed guidance. This manual provides instructions on how to properly implement our validated P2PE solution.

---

## Collect payment details before creating an Intent

**URL:** https://docs.stripe.com/payments/accept-a-payment-deferred?platform=web&type=payment

**Contents:**
- Collect payment details before creating an Intent
- Build an integration where you can render the Payment Element prior to creating a PaymentIntent or SetupIntent.
    - Compare Customers v1 and Accounts v2 references
- Set up StripeServer-side
- Enable payment methods
    - Caution
- Collect payment detailsClient-side
    - Conflicting iFrames
  - Set up Stripe.js
  - Add the Payment Element to your checkout page

If your Connect platform uses customer-configured Accounts, use our guide to replace Customer and event references in your code with the equivalent Accounts v2 API references.

The Payment Element allows you to accept multiple payment methods using a single integration. In this integration, learn how to build a custom payment flow where you render the Payment Element, create the PaymentIntent, and confirm the payment from the buyer’s browser. If you prefer to confirm the payment from the server instead, see Finalize payments on the server.

First, create a Stripe account or sign in.

Use our official libraries to access the Stripe API from your application:

This integration path doesn’t support BLIK or pre-authorized debits that use the Automated Clearing Settlement System (ACSS).

View your payment methods settings and enable the payment methods you want to support. You need at least one payment method enabled to create a PaymentIntent.

By default, Stripe enables cards and other prevalent payment methods that can help you reach more customers, but we recommend turning on additional payment methods that are relevant for your business and customers. See Payment method support for product and payment method support, and our pricing page for fees.

Use the Payment Element to securely send payment information collected in an iFrame to Stripe over an HTTPS connection.

Avoid placing the Payment Element within another iframe because it conflicts with payment methods that require redirecting to another page for payment confirmation.

Your checkout page URL must start with https:// rather than http:// for your integration to work. You can test your integration without using HTTPS, but remember to enable it when you’re ready to accept live payments.

The Payment Element is automatically available as a feature of Stripe.js. Include the Stripe.js script on your checkout page by adding it to the head of your HTML file. Always load Stripe.js directly from js.stripe.com to remain PCI compliant. Don’t include the script in a bundle or host a copy of it yourself.

Create an instance of Stripe with the following JavaScript on your checkout page:

The Payment Element needs a place to live on your checkout page. Create an empty DOM node (container) with a unique ID in your payment form:

After your form loads, create an Elements instance with the mode, amount, and currency. These values determine which payment methods the Element presents to your customer.

Then, create an instance of the Payment Element and mount it to the container DOM node.

The Payment Element renders a dynamic form that allows your customer to pick a payment method. The form automatically collects all necessary payments details for the payment method selected by the customer.

You can customize the Payment Element to match the design of your site by passing the appearance object into options when creating the Elements provider.

By default, the Payment Element only collects the necessary billing address details. Some behavior, such as calculating tax or entering shipping details, requires your customer’s full address. You can:

Navigate to step 5 in the finalize payments guide to run your custom business logic immediately before payment confirmation. Otherwise, follow the steps below for a simpler integration, which uses stripe.confirmPayment on the client to both confirm the payment and handle any next actions.

When the customer submits your payment form, create a PaymentIntent on your server with an amount and currency enabled.

Return the client secret value to your client for Stripe.js to use to complete the payment process.

The following example includes commented code to illustrate the optional Tax Calculation.

Use stripe.confirmPayment to complete the payment using details from the Payment Element.

Provide a return_url to this function to indicate where Stripe should redirect the user after they complete the payment. Your user might be initially redirected to an intermediate site, like a bank authorization page, before being redirected to the return_url. Card payments immediately redirect to the return_url when a payment is successful.

If you don’t want to redirect for card payments after payment completion, you can set redirect to if_required. This only redirects customers that check out with redirect-based payment methods.

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

## Build an in-app payments integration

**URL:** https://docs.stripe.com/payments/mobile

**Contents:**
- Build an in-app payments integration
    - US apps selling digital goods
- Choose a UI
- Choose an API
  - Accept a payment
  - Set up a payment method
  - Accept and set up a payment
- Saved payment methods
- Features and availability

Use Stripe’s In-app Payments to build a customized payments integration and checkout flows for your iOS, Android, and React Native apps. This overview helps you plan your integration.

Android apps in the US that sell digital goods can now process payments in-app using Stripe. If you sell digital goods on iOS, see how to implement an app-to-web flow using Stripe Checkout in Sell in-app digital goods and subscriptions.

With Stripe In-App Payments, you can:

Choose from three different UI integrations depending on your preferred UX and design needs.

This integration displays payment methods, collects payment information, and completes payment all in a single prebuilt sheet. We recommend using this UI to take payments in your app for most users.

You can customize more than 50 aspects of the appearance, including colors and fonts, with the Appearance API guide.

Try the demo: Scan the QR code with your iOS device or use this link to try an interactive demo.

Consider another option for…

Stripe’s In-App Payments integration uses either PaymentIntents or SetupIntents.

Collect payment and charge the customer immediately.

Our UI displays a “Save my info” checkbox, allowing customers to save their payment method for future checkouts. Learn more about saved payment methods.

Charge the customer now and save their payment method for future use by configuring your PaymentIntent to save the payment method.

You can require all payment methods to be saved by configuring setup_future_usage. Using setup_future_usage disables one-time payment methods, like most BNPLs. To support both one-time and reusable payment methods, configure future usage on specific payment methods, such as payment_method_options[card][setup_future_usage] to save cards.

Stripe’s In-App Payments supports saving, displaying, and managing saved card, US Bank account, and SEPA Debit payment methods. Consent collection is handled automatically, ensuring global compliance.

Access saved payment methods in Payment Sheet

The CustomerSessions API provides additional control over:

Extensive, using the Appearance API

iOS, Android, and React Native

One-time and recurring payments

1Wallet payment methods require registering your domain.

---

## Payment method support

**URL:** https://docs.stripe.com/payments/payment-methods/payment-method-support

**Contents:**
- Payment method support
- Learn how your integration choices affect payment method support.
  - Link and your integration
- Troubleshoot a payment method
- Country and currency support
    - Connected accounts
- Product support
    - Checkout modes
  - Bank debits product support
  - Bank redirects product support

Link is a payment method network. With Link, users save their payment details one time, and can then pay any business on the Link network for future purchases.

Payment methods support certain currencies, countries, products, and API options. Make sure your chosen payment methods work for your scenario before choosing an integration option by viewing these tables:

All payment methods have specific requirements for their use and might contain additional restrictions that you must comply with, such as marketing guidelines, additional prohibited and restricted businesses, and information about handling disputes and refunds. These usage requirements and restrictions are described in the documentation for that payment method or in the applicable payment terms.

If a customer doesn’t see a specific payment method, follow these steps to troubleshoot the issue using the Dashboard payment method troubleshooting tool.

Refer to the following table to see where each payment method is supported and what presentment currencies it accepts. This table contains all of the supported currencies and countries for a given payment method. In some cases, not all of the countries listed can accept payments in all of the listed presentment currencies. For more details on exactly what currencies are accepted, see the individual payment method’s page.

If you have a platform or marketplace integration that uses Connect, your connected accounts might have different eligibility requirements than your account. To learn about connected account eligibility and capabilities, see Adding payment method capabilities.

To determine which payment methods each Stripe product supports, refer to the following tables:

Checkout has three modes: payment, subscription, and setup. Unless specified otherwise, the payment method is available in all modes.

1 You can’t use the Payment Element to create SetupIntents for Bacs Direct Debit. Use Checkout in setup mode instead.2 Not supported when using Checkout in subscription mode.3 Supports ACSS debit if you create a PaymentIntent before rendering the Payment Element.4 Not supported when using Elements with the Checkout Sessions API.

Contact us to request a new bank debit method.

1 Not supported when using Checkout in subscription mode.2 Not supported when using Checkout in setup mode.3 Not supported when collecting payment details before creating a PaymentIntent.4 Not supported when using Elements with the Checkout Sessions API.5 Only supported when using Checkout in subscription mode.6 Not supported when using charge_automatically for subscriptions or invoices. iDEAL is a single use payment method where customers are required to authenticate each payment.7 Invoices and Subscriptions only support the send_invoice collection method.

Contact us to request a new bank redirect payment method.

1 Not supported when using Checkout in subscription mode.2 Not supported when using Checkout in setup mode.

1 Not supported when using Checkout in subscription mode.2 Not supported when using Checkout in setup mode.3 Not supported when saving payment details during payment (setup_future_usage).4 Invoices and Subscriptions only support the send_invoice collection method.

1 Not supported when using Checkout in subscription mode.2 Not supported when using Checkout in setup mode.3 Invoices and Subscriptions only support the send_invoice collection method.

1 Supported with send_invoice collection method subscriptions.

1 Not supported when using Checkout in subscription mode.2 Not supported when using Checkout in setup mode.3 Invoices and Subscriptions only support the send_invoice collection method.4Request an invite to create charges on behalf of other accounts.

1 Not supported when using Checkout in subscription mode.2 Not supported when using Checkout in setup mode.3 Not supported when saving payment details during payment (setup_future_usage).4 Invoices and Subscriptions only support the send_invoice collection method.5 Checkout with ui_mode set to embedded supports only Safari version 17 or later and iOS version 17 or later.6 The Payment Element doesn’t support Link in Brazil or India.7 Stripe doesn’t display Apple Pay or Google Pay for IP addresses in India.8 Request an invite to use Connect.

To learn about payment method API support, refer to the following tables:

1 Cards and bank debit methods including SEPA debit, AU BECS direct debit, and ACSS debit support both on_session and off_session with setup future usage. All other payment method types either don’t support setup_future_usage or only support off_session.2 Payment methods might require confirmation with return_url to indicate where Stripe should redirect your customer after they complete the payment.3 PaymentIntents support confirmation with Bacs Direct Debit payment methods when the Mandate has been collected by a Stripe-owned flow such as Checkout, Payment Element, and Payment Links.4 You can create SetupIntents for Bacs Direct Debit through Checkout using setup mode.5 Pre-authorized debit in Canada doesn’t support the deferred intent creation integration path.

1 Cards and bank debit methods including SEPA debit, AU BECS direct debit, and ACSS debit support both on_session and off_session with setup future usage. All other payment method types either don’t support setup_future_usage or only support off_session.2 Payment methods might require confirmation with return_url to indicate where Stripe should redirect your customer after they complete the payment.3 BLIK doesn’t support the deferred intent creation integration path.

1 Cards and bank debit methods including SEPA debit, AU BECS direct debit, and ACSS debit support both on_session and off_session with setup future usage. All other payment method types either don’t support setup_future_usage or only support off_session.2 Payment methods might require confirmation with return_url to indicate where Stripe should redirect your customer after they complete the payment.

1 Cards and bank debit methods including SEPA debit, AU BECS direct debit, and ACSS debit support both on_session and off_session with setup future usage. All other payment method types either don’t support setup_future_usage or only support off_session.2 Payment methods might require confirmation with return_url to indicate where Stripe should redirect your customer after they complete the payment.

1 Cards and bank debit methods including SEPA debit, AU BECS direct debit, and ACSS debit support both on_session and off_session with setup future usage. All other payment method types either don’t support setup_future_usage or only support off_session.2 Payment methods might require confirmation with return_url to indicate where Stripe redirects your customer after they complete the payment.

1 Cards and bank debit methods including SEPA debit, AU BECS direct debit, and ACSS debit support both on_session and off_session with setup future usage. All other payment method types either don’t support setup_future_usage or only support off_session.2 Payment methods might require confirmation with return_url to indicate where Stripe redirects your customer after they complete the payment.

1 Cards and bank debit methods including SEPA debit, AU BECS direct debit, and ACSS debit support both on_session and off_session with setup future usage. All other payment method types either don’t support setup_future_usage or only support off_session.2 Payment methods might require confirmation with return_url to indicate where Stripe should redirect your customer after they complete the payment.

1 Cards and bank debit methods including SEPA debit, AU BECS direct debit, and ACSS debit support both on_session and off_session with setup future usage. All other payment method types either don’t support setup_future_usage or only support off_session.2 Payment methods might require confirmation with return_url to indicate where Stripe should redirect your customer after they complete the payment.

1 Cards and bank debit methods including SEPA debit, AU BECS direct debit, and ACSS debit support both on_session and off_session with setup future usage. All other payment method types either don’t support setup_future_usage or only support off_session.2 Payment methods might require confirmation with return_url to indicate where Stripe should redirect your customer after they complete the payment.

If you need a payment method not offered on this page, consider custom payment methods.

1 Not compatible with the Checkout Sessions API

---

## Bank redirects

**URL:** https://docs.stripe.com/payments/bank-redirects

**Contents:**
- Bank redirects
- Learn about bank redirects with Stripe.
- Payment flow
- Product support
- API support
- Migrating from the Sources or Tokens APIs

Bank redirects let customers pay online using their bank account. They drive more than half of online commerce in Germany, the Netherlands, and Malaysia. Bank redirects are often used by:

Bank redirects might not be a good fit for your business if you sell subscriptions. Some bank redirects don’t support recurring payments.

At checkout, the customer is redirected to their online banking portal, logs in with their bank credentials, approves the transaction, and then returns to your site. Some bank redirects verify the user through SMS or other two-factor authentication for additional security.

We’ve created a single integration for all bank redirects that works across Stripe products. With Stripe Checkout, you can add any bank redirect by changing one line of code.

1 Not supported when using Checkout in subscription mode.2 Not supported when using Checkout in setup mode.3 Not supported when collecting payment details before creating a PaymentIntent.4 Not supported when using Elements with the Checkout Sessions API.5 Only supported when using Checkout in subscription mode.6 Not supported when using charge_automatically for subscriptions or invoices. iDEAL is a single use payment method where customers are required to authenticate each payment.7 Invoices and Subscriptions only support the send_invoice collection method.

Contact us to request a new bank redirect payment method.

1 Cards and bank debit methods including SEPA debit, AU BECS direct debit, and ACSS debit support both on_session and off_session with setup future usage. All other payment method types either don’t support setup_future_usage or only support off_session.2 Payment methods might require confirmation with return_url to indicate where Stripe should redirect your customer after they complete the payment.3 BLIK doesn’t support the deferred intent creation integration path.

If you currently use the Sources or Tokens API, see migrating to PaymentIntents to use the latest integrations.

---

## Tour of the API

**URL:** https://docs.stripe.com/payments-api/tour

**Contents:**
- Tour of the API
- See how Stripe API objects fit together and learn best practices for combining them.
  - Compare Customers v1 and Accounts v2 references
- Core concepts
  - Everything is an object
  - Objects have lives
  - An integration is made out of cooperating objects
- Payment objects
- The path to a payment
  - Payment methods

If your Connect platform uses customer-configured Accounts, use our guide to replace Customer and event references in your code with the equivalent Accounts v2 API references.

The Stripe APIs are powerful and flexible if you know how to use them. This tour of the API covers key information to help you understand the APIs more deeply:

Understanding these patterns helps you move beyond the pre-written code in Stripe tutorials. You can migrate old integrations to use more modern patterns, combine simple patterns in novel ways, and plan for future growth.

Everything in your Stripe account is an object, whether you create it with the API or not. Your balance corresponds to a Balance object, you track customers with Customer objects, you store payment details in PaymentMethod objects, and so on.

Even low-code and no-code integrations produce these objects. So do actions you perform in the Dashboard. For instance, when you manually create a customer in the Dashboard, it still creates a Customer object.

Stripe integrations handle complicated processes.

The API uses a single object to track each process. You create the object at the start of the process, and after every step you can check its status to see what needs to happen next—This is sometimes referred to as a state machine.

For instance, while completing a payment, a customer might try several payment methods. If one payment method fails, a status of requires_payment_method lets you know to prompt the customer for another.

To accept a payment, a system needs to create several core objects and manage them through several states.

Your Stripe integration is a system that handles this creation and management by communicating with Stripe.

Some integrations do a lot more than that: track customers, manage subscriptions, and so on. But their core payment functionality still comes from the same objects and steps, with more objects added around that core.

Stripe uses a variety of related objects to facilitate payments. Before you can build an integration that suits your specific needs, you must familiarize yourself with how these objects work together.

Check out this video for an overview of payment object roles and capabilities.

To learn more about Stripe’s payment integration options, see the following guides:

In a modern Stripe integration, every payment uses an object called a PaymentIntent. As its name suggests, it represents your intent to collect a payment. This object tracks the steps you go through along the way to fulfilling that intent.

For instance, suppose a customer clicks a Check out button with a 100 USD item in their cart. They haven’t bought it yet, and they might never buy it (maybe at some point they abandon the payment flow, or their card issuer declines the payment). But clicking Check out indicates their intent to buy—and you intend to help them. At that point, an integration creates a PaymentIntent object in the amount of 100 USD to track the rest of the process.

The PaymentIntent’s path to success goes through several statuses—here’s a simplified version:

A PaymentIntent starts with the status requires_payment_method. To move it forward, Stripe needs details about the customer’s payment method—either a card number or credentials for some other payment system.

An integration represents these details using an API object called a PaymentMethod. In some integrations, you write the code that creates that object and attaches it to the PaymentIntent. In others, Stripe gathers the details and does the work for you. You can also create and save a payment method for use with future PaymentIntents using the Setup Intents API.

The next status is requires_confirmation. In an interactive payment flow, the customer must confirm that they intend to pay—and that they intend to do it using the method they provided. In a one-time online payment, this usually happens when they click the Pay button.

When the customer clicks Pay or otherwise confirms their intent, an integration notifies Stripe with an API call. In some integrations, you write the code that makes this call. Stripe provides drop-in UI elements, called Stripe Elements, to enable this while still providing flexibility to build a custom integration. In other integrations, like a Stripe Checkout or Payment Links integration, Stripe makes the call and handles the next steps. There are many ways to integrate Stripe and combine different objects to handle your use case. Learn more about integration options for online payments.

In most cases a Charge will be created when a PaymentIntent is confirmed to represent that specific attempt to move money. The Charge might succeed or fail. If it fails the payment can be retried by confirming the PaymentIntent again, usually with new payment details. Allowing retries immediately, without the need to create a new PaymentIntent, tends to increase conversion rates.

The intent’s state is now processing, and at this point Stripe attempts to process the payment.

Stripe always does this part for you—and it can have several steps. (For credit cards, these steps are part of how cards work.) As we work through the steps, we update the intent’s state with the outcome: either succeeded or back to requires_payment_method if it fails.

When we’re done, one last object comes into play: the Event. We use Event objects to represent activity. In this case, the activity might be “the charge succeeded” or “the charge failed.” In some integrations, you write custom code to respond to events using webhook endpoints. In others, such as Checkout or Payment Links integrations, Stripe listens for the event and provides a pre-written response.

---

## Supported payment methods

**URL:** https://docs.stripe.com/payments/payment-methods/overview

**Contents:**
- Supported payment methods
- Learn about the types of payment methods that your Stripe integration can support.
  - Pricing and fees
- Cards
- Bank debits
- Bank redirects
- Bank transfers
- Buy now, pay later
- Real-time payments
- Vouchers

We categorize payment methods into eight families:

For information on payment method transaction fees, refer to pricing details.

Each family has similar features, a single integration, and common checkout experiences. After you’ve integrated one payment method, you can add another within the same family with minimal changes to your integration.

To learn more about which payment methods are right for your business, see our payment method guide.

Cards are a common way for consumers and businesses to pay online or in person. Stripe supports global and local card networks. See the card brands that Stripe supports.

In-person payments support different card brands, depending on the country and card reader type. For more information, see Terminal’s supported card brands.

By debiting your customer’s bank account directly, you can save on transaction fees when compared to cards. For details, see the bank debits documentation.

Bank redirects let customers pay online using their bank account, using a secure, intuitive checkout flow. They’re popular among European and Asian consumers and can improve conversion and reduce fraud. See bank redirects to learn more.

To request access to one of our invite only payment methods, contact us.

Customers or other businesses can use bank transfers to send money directly to your bank account and are common for accepting large payments from other businesses. In some countries, bank transfers are popular for consumer payments as well. See bank transfers to learn more.

Buy now, pay later payment methods help retailers reach customers that want to pay in installments. Your business is paid immediately and in full, and your customer pays nothing or a portion of the total cost at checkout. See buy now, pay later to learn more.

To request access to one of our invite only payment methods, contact us.

Real-time payments let customers send money directly from their bank account or other funding source using an intermediary to authenticate, such as a phone number or other account. They’re a common payment type in Asia and Latin America. See real-time payments to learn more.

To request access to one of our invite only payment methods, contact us.

Vouchers are a popular way for customers in Asia and Latin America to complete online purchases in-person. At checkout, customers receive a digital voucher with pending transaction details and then complete the payment at local stores. See vouchers to learn more.

Wallets provide a fast and secure way for consumers to pay with a saved card or a stored balance. Wallets improve conversion and reduce fraud, especially on mobile. See wallets to learn more.

To request access to one of our invite only payment methods, contact us.

If you need a payment method not offered on this page, consider custom payment methods.

---

## Payment Methods API

**URL:** https://docs.stripe.com/payments/payment-methods

**Contents:**
- Payment Methods API
- Learn more about the API that powers a range of global payment methods.
- Supported payment methods
- Customer actions
    - Note
- Immediate or delayed notification of payment success
    - Note
- Single-use or reusable
- Use webhooks to track payment status
- The PaymentMethod object

The Payment Methods API allows you to accept a variety of payment methods through a single API. A PaymentMethod object contains the payment method details to create payments. With the Payment Methods API, you can combine a PaymentMethod:

To determine which payment methods to use for specific locales, see the guide to payment methods.

The guide includes available payment methods for different regions, a detailed description of each payment method’s characteristics, and the geographic regions where they’re most relevant. You can enable any payment methods available to you in the Dashboard. Activation is generally instantaneous and doesn’t require additional contracts.

​​Some payment methods require your customer to take additional steps to complete the payment. The PaymentIntent object’s next_action parameter specifies the type of customer action.

Some common actions that customers need to perform are:

Not all payment methods require additional customer actions. For example, card payments (excluding 3D Secure) require no additional authentication beyond collecting card details.

For payment methods that require customer action, configure webhook endpoints for notifications on whether a payment has succeeded or not.

Some payment methods immediately return payment status when a transaction is attempted (for example, card payments) but other methods have a delay such as ACH debits. For those that immediately return payment status, the PaymentIntent status either changes to succeeded or requires_payment_method. A status of succeeded guarantees that you will receive the funds from your customers.

Payment methods with delayed notification can’t guarantee payment during the delay. The status of the PaymentIntent object will be processing until the payment status is either successful or failed. It’s common for businesses to hold an order in a pending state during this time, not fulfilling the order until the payment is successful.

​​For payment methods with delayed notification, configure webhook endpoints for notifications on whether a payment has succeeded or not.

You can reuse certain payment methods (for example, cards or bank debits) for additional payments without authorizing and collecting payment details again.

You should always set up reusable payment methods for future use to reduce the chance of future declines and payment friction (such as authentication being required). Reusable payment methods can be set up for future use when accepting a payment or set up for future use without taking a payment.

Single-use payment methods (for example, some kinds of bank transfers) can’t be attached to customers because they’re consumed after a payment attempt.

Configure webhooks by creating a webhook endpoint or other type of event destination for payment methods that either require customer action or when payment notification is delayed. Stripe sends the following events when the PaymentIntent status is updated:

​​You can also use the following options instead of setting up an event destination to listen to events:

A PaymentMethod contains reusable payment method details for creating payments (for example, card expiration date or billing address), it doesn’t include transaction-specific information (for example, amount, currency). A PaymentMethod is attached to a PaymentIntent to represent the states of a payment lifecycle. Each PaymentMethod has a type attribute (for example, "type": "sepa_debit" ) and an additional hash whose name matches the type and contains information specific to the PaymentMethod type (for example, "sepa_debit":{}). Example of a sepa_debit PaymentMethod object:

To safely handle sensitive payment information and automatically handle customer actions, Stripe recommends that you create payment methods using Stripe.js.

**Examples:**

Example 1 (unknown):
```unknown
{
  "id": "pm_123456789",
  "object": "payment_method",
  "billing_details": {
    "address": {...},
    "email": "jenny@example.com",
    "name": "Jenny Rosen",
    "phone": "+335555555555"
  },
  "sepa_debit": {
    "bank_code": "37040044",
    "branch_code": "94832",
    "country": "FR",
    "fingerprint": "ygEJfUjzWMGyWnZg",
    "last4": "3000"
  },
  "type": "sepa_debit",
  (...)
}
```

Example 2 (unknown):
```unknown
{
  "id": "pm_123456789",
  "object": "payment_method",
  "billing_details": {
    "address": {...},
    "email": "jenny@example.com",
    "name": "Jenny Rosen",
    "phone": "+335555555555"
  },
  "sepa_debit": {
    "bank_code": "37040044",
    "branch_code": "94832",
    "country": "FR",
    "fingerprint": "ygEJfUjzWMGyWnZg",
    "last4": "3000"
  },
  "type": "sepa_debit",
  (...)
}
```

---

## Bank Debits

**URL:** https://docs.stripe.com/payments/bank-debits

**Contents:**
- Bank Debits
- Learn how to accept bank debits with Stripe.
- Payment flow
- Product support
- API support
- Migrating from the Sources, Tokens, or Charges APIs

With bank debits, you can pull funds directly from your customer’s bank account for both one-time and recurring purchases. Bank debits are often used by:

Bank debits might not be a good fit for your business if:

To initiate a bank debit, a customer enters their bank account details during checkout and gives you permission to debit the account. This permission is called a mandate.

To reduce fraud with some bank debits, verify the bank account before the payment by confirming microdeposits or bank login. Verifying bank login can improve the user experience because customers pay by logging into their bank rather than entering bank account details.

You can use a single integration for all bank debits that works across Stripe products. With Stripe Checkout, Payment Element, and Payment Links, you can enable bank debits directly from the Dashboard with no integration work.

1 You can’t use the Payment Element to create SetupIntents for Bacs Direct Debit. Use Checkout in setup mode instead.2 Not supported when using Checkout in subscription mode.3 Supports ACSS debit if you create a PaymentIntent before rendering the Payment Element.4 Not supported when using Elements with the Checkout Sessions API.

Contact us to request a new bank debit method.

1 Cards and bank debit methods including SEPA debit, AU BECS direct debit, and ACSS debit support both on_session and off_session with setup future usage. All other payment method types either don’t support setup_future_usage or only support off_session.2 Payment methods might require confirmation with return_url to indicate where Stripe should redirect your customer after they complete the payment.3 PaymentIntents support confirmation with Bacs Direct Debit payment methods when the Mandate has been collected by a Stripe-owned flow such as Checkout, Payment Element, and Payment Links.4 You can create SetupIntents for Bacs Direct Debit through Checkout using setup mode.5 Pre-authorized debit in Canada doesn’t support the deferred intent creation integration path.

If your current bank debit integration uses the Sources, Tokens, or Bank Accounts API, we recommend following the appropriate migration guide to transition to Payment Intents API:

---

## Payments

**URL:** https://docs.stripe.com/payments

**Contents:**
- Payments
- Use Stripe to start accepting payments.
- Payment options
- Payment methods
- Beyond payments
- Platforms and marketplaces
- Clone a sample project
- More guides

Not ready for a full integration? Get started without writing code.

Integrate a Stripe product to start accepting payments online and in person, embed financial services, power custom revenue models, and more.

Build a payment form or use a prebuilt payment page to accept online payments.

Set up recurring billing for your SaaS or e-commerce business.

Let your customers check out faster with Link.

Learn about the types of payment methods that your Stripe integration can support.

Dynamically order and display payment methods.

Let your customers check out faster with Link.

Start a US company from most places in the world using Stripe Atlas.

Let your users pay in crypto, pay out in crypto, or embed a fiat-to-crypto onramp.

Access permissioned data from your users’ financial accounts.

Set up a Connect SaaS platform to provide platform services to businesses that collect direct payments from their own customers.

Set up a Connect marketplace to collect payments from customers and pay out a portion to sellers or service providers.

Send funds directly to your sellers or service providers in their local currency.

---

## Understand how charges work in a Connect integration

**URL:** https://docs.stripe.com/connect/charges

**Contents:**
- Understand how charges work in a Connect integration
- Learn about the types of charges used in Connect integrations and how funds move between the platform and connected accounts.
- Charge types
  - Direct charges
    - Note
  - Destination charges
    - Regional considerations
  - Separate charges and transfers
    - Regional considerations
  - Indirect charges using the on_behalf_of parameter

In a Connect integration, for your platform or a connected account to accept a payment from a customer, you must first create a charge. The type of charge you create determines how the funds are distributed between your platform, the connected account, and Stripe. It also determines whether your platform’s or the connected account’s information appears on the customer’s bank or billing statement and which account Stripe debits for refunds and chargebacks.

Connect uses three types of charges in two general categories:

The following table describes many factors to consider when choosing which charge type to use. Your platform’s business model is particularly important because it can affect how funds flow through Stripe. To review Stripe’s recommendations for your business, refer to your platform profile.

You can use multiple charge types, if that’s appropriate for your business.

Create a charge directly on a connected account. The account’s customers are often unaware of your platform’s existence. You can specify an application fee, which transfers to your platform’s account balance when the connected account collects the payment.

Your connected accounts must have the card_payments capability active in order to use direct charges.

This charge type is best suited for platforms providing Software as a Service (SaaS). For example, Shopify provides tools for building online storefronts, and Thinkific enables educators to sell online courses.

With this charge type:

Funds flow for direct charges

For more information about direct charges, see Direct charges.

Create a charge on the platform and immediately transfer funds to the connected account. You decide whether some or all of those funds are transferred, and whether to deduct an application fee.

This charge type is best suited for marketplaces, such as a home rental marketplace or a ridesharing app.

With this charge type:

Funds flow for destination charges with the platform fee deducted from the transferred amount

Funds flow for destination charges with the platform fee paid after transferring the full amount

Destination charges support cross-region funds flows between platforms and connected accounts only in certain regions. For other regions, the platform and connected account must be in the same region unless using on_behalf_of. For more information about cross-region support, see Cross-border transfers.

For more information about destination charges, see Destination charges.

Create charges on your platform and split funds between multiple connected accounts, or hold them when you don’t know the specific user at the time of the charge. The charge on your platform account is decoupled from the transfers to your connected accounts.

This charge type is best suited for marketplaces that need to split payments between multiple parties, such as DoorDash, a restaurant delivery platform.

For Express and Custom accounts, Stripe recommends that you create separate charges and transfers if destination charges don’t meet your business needs.

With this charge type:

Separate charges and transfers require a more complex Connect integration. Use them only if your business use case requires them:

In some cases, the transfer amount can be greater than the charge amount, or the transfer is made before the payment is processed. You must monitor your account balance carefully to make sure it has enough available funds to cover the transfer amount. You can also associate a transfer with a charge so the transfer doesn’t occur until the funds from that charge are available.

Funds flow for separate charges and transfers with multiple connected accounts

Separate charges and transfers support cross-region funds flows between platforms and connected accounts only in certain regions. For other regions, the platform and connected account must be in the same region unless using on_behalf_of. For more information about cross-region support, see Cross-border transfers.

For more information about separate charges and transfers, see Separate charges and transfers.

To make the connected account the business of record for the payment, use the on_behalf_of parameter. When on_behalf_of is set to the ID of the connected account, Stripe automatically:

There are two components to Stripe fees with Connect: which pricing plan applies to the payment and which account pays Stripe fees.

When using Direct charges, you can choose how Stripe fees are billed to your connected accounts.

Read more about fee billing behaviors with Direct charges.

Destination charges and separate charges and transfers typically use the platform’s pricing plan and are assessed on the platform. When the on_behalf_of field is set, the country of the connected account is used to determine the country specific fees charged to your platform account.

For more information on Connect fees and how to request custom pricing, see the Connect pricing page.

You can issue a refund to pay a customer back for money spent on a returned good or to compensate for unsatisfactory service. Stripe handles refunds differently for each of the charge types:

Stripe debits the refund amount from the connected account’s balance directly when you create a refund.

If the connected account’s balance is insufficient, we set the refund status to pending. When the connected account’s balance has enough funds, Stripe automatically processes pending refunds in the order they were created and updates their status to successful.

Stripe debits your platform balance for the refund amount. You can reverse the transfers made to your connected accounts to recover your refund cost.

If your platform’s account balance doesn’t have the funds when you issue the Refund, we set the refund status to pending. When your platform’s balance has enough funds, Stripe automatically processes pending refunds and updates their status to successful.

If the refund request also attempts a transfer reversal, but the connected account has an insufficient balance, the refund request returns an error instead of creating a refund with pending status.

Separate charges and transfers

Stripe debits your platform balance for the refund amount. You can reverse the transfers made to your connected accounts to recover your refund cost.

If your platform’s account balance doesn’t have the funds when you issue the Refund, we set the refund status to pending. When you platform balance has enough funds, Stripe automatically processes pending refunds and updates their status to successful.

For disputes on payments created using direct charges, Stripe debits the disputed amount from the connected account’s balance, not your platform’s balance. Stripe can bill the dispute fee to either the platform or the connected account, depending on the connected account’s configuration. For more detail about how we bill fees for disputes on direct charges, see Fee behavior on connected accounts.

For disputes where payments were created on your platform using destination charges or separate charges and transfers, with or without on_behalf_of, your platform balance is automatically debited for the disputed amount and fee. When this happens, your platform can attempt to recover funds from the connected account by reversing the transfer either through the Dashboard or using the API.

If there’s a negative balance on the connected account, Stripe attempts to debit the external account on file for the connected account only if debit_negative_balances is set to true.

For more details, see Disputes and fraud and Dispute categories. You can also use Fraud Stripe Apps to automate dispute management and handle chargebacks.

---

## Retrieve a charge

**URL:** https://docs.stripe.com/api/charges/retrieve

**Contents:**
- Retrieve a charge
  - Parameters
  - Returns
- List all charges
  - Parameters
    - customerstring
  - More parametersExpand all
    - createdobject
    - ending_beforestring
    - limitinteger

Retrieves the details of a charge that has previously been created. Supply the unique charge ID that was returned from your previous request, and Stripe will return the corresponding charge information. The same information is returned when creating or refunding the charge.

Returns a charge if a valid identifier was provided, and raises an error otherwise.

Returns a list of charges you’ve previously created. The charges are returned in sorted order, with the most recent charges appearing first.

Only return charges for the customer specified by this customer ID.

A dictionary with a data property that contains an array of up to limit charges, starting after charge starting_after. Each entry in the array is a separate charge object. If no more charges are available, the resulting array will be empty. If you provide a non-existent customer ID, this call raises an error.

Capture the payment of an existing, uncaptured charge that was created with the capture option set to false.

Uncaptured payments expire a set number of days after they are created (7 by default), after which they are marked as refunded and capture attempts will fail.

Don’t use this method to capture a PaymentIntent-initiated charge. Use Capture a PaymentIntent.

The amount to capture, which must be less than or equal to the original amount.

The email address to send this charge’s receipt to. This will override the previously-specified email address for this charge, if one was set. Receipts will not be sent in test mode.

The maximum length is 800 characters.

For a non-card charge, text that appears on the customer’s statement as the statement descriptor. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

For a card charge, this value is ignored unless you don’t specify a statement_descriptor_suffix, in which case this value is used as the suffix.

Provides information about a card charge. Concatenated to the account’s statement descriptor prefix to form the complete statement descriptor that appears on the customer’s statement. If the account has no prefix value, the suffix is concatenated to the account’s statement descriptor.

Returns the charge object, with an updated captured property (set to true). Capturing a charge will always succeed, unless the charge is already refunded, expired, captured, or an invalid capture amount is specified, in which case this method will raise an error.

Search for charges you’ve previously created using Stripe’s Search Query Language. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.

The search query string. See search query language and the list of supported query fields for charges.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A dictionary with a data property that contains an array of up to limit charges. If no objects match the query, the resulting array will be empty. See the related guide on expanding properties in lists.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/charges/ch_3MmlLrLkdIwHu7ix0snN0B15 \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/charges/ch_3MmlLrLkdIwHu7ix0snN0B15 \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "ch_3MmlLrLkdIwHu7ix0snN0B15",  "object": "charge",  "amount": 1099,  "amount_captured": 1099,  "amount_refunded": 0,  "application": null,  "application_fee": null,  "application_fee_amount": null,  "balance_transaction": "txn_3MmlLrLkdIwHu7ix0uke3Ezy",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": null,    "phone": null  },  "calculated_statement_descriptor": "Stripe",  "captured": true,  "created": 1679090539,  "currency": "usd",  "customer": null,  "description": null,  "disputed": false,  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "fraud_details": {},  "livemode": false,  "metadata": {},  "on_behalf_of": null,  "outcome": {    "network_status": "approved_by_network",    "reason": null,    "risk_level": "normal",    "risk_score": 32,    "seller_message": "Payment complete.",    "type": "authorized"  },  "paid": true,  "payment_intent": null,  "payment_method": "card_1MmlLrLkdIwHu7ixIJwEWSNR",  "payment_method_details": {    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": null      },      "country": "US",      "exp_month": 3,      "exp_year": 2024,      "fingerprint": "mToisGZ01V71BCos",      "funding": "credit",      "installments": null,      "last4": "4242",      "mandate": null,      "network": "visa",      "three_d_secure": null,      "wallet": null    },    "type": "card"  },  "receipt_email": null,  "receipt_number": null,  "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xTTJKVGtMa2RJd0h1N2l4KOvG06AGMgZfBXyr1aw6LBa9vaaSRWU96d8qBwz9z2J_CObiV_H2-e8RezSK_sw0KISesp4czsOUlVKY",  "refunded": false,  "review": null,  "shipping": null,  "source_transfer": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "succeeded",  "transfer_data": null,  "transfer_group": null}
```

Example 4 (unknown):
```unknown
{  "id": "ch_3MmlLrLkdIwHu7ix0snN0B15",  "object": "charge",  "amount": 1099,  "amount_captured": 1099,  "amount_refunded": 0,  "application": null,  "application_fee": null,  "application_fee_amount": null,  "balance_transaction": "txn_3MmlLrLkdIwHu7ix0uke3Ezy",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": null,    "phone": null  },  "calculated_statement_descriptor": "Stripe",  "captured": true,  "created": 1679090539,  "currency": "usd",  "customer": null,  "description": null,  "disputed": false,  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "fraud_details": {},  "livemode": false,  "metadata": {},  "on_behalf_of": null,  "outcome": {    "network_status": "approved_by_network",    "reason": null,    "risk_level": "normal",    "risk_score": 32,    "seller_message": "Payment complete.",    "type": "authorized"  },  "paid": true,  "payment_intent": null,  "payment_method": "card_1MmlLrLkdIwHu7ixIJwEWSNR",  "payment_method_details": {    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": null      },      "country": "US",      "exp_month": 3,      "exp_year": 2024,      "fingerprint": "mToisGZ01V71BCos",      "funding": "credit",      "installments": null,      "last4": "4242",      "mandate": null,      "network": "visa",      "three_d_secure": null,      "wallet": null    },    "type": "card"  },  "receipt_email": null,  "receipt_number": null,  "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xTTJKVGtMa2RJd0h1N2l4KOvG06AGMgZfBXyr1aw6LBa9vaaSRWU96d8qBwz9z2J_CObiV_H2-e8RezSK_sw0KISesp4czsOUlVKY",  "refunded": false,  "review": null,  "shipping": null,  "source_transfer": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "succeeded",  "transfer_data": null,  "transfer_group": null}
```

---

## Mail order and telephone order (MOTO) payments

**URL:** https://docs.stripe.com/terminal/features/mail-telephone-orders/overview

**Contents:**
- Mail order and telephone order (MOTO) payments
- Learn how to process mail order and telephone order payments using Stripe Terminal.
    - Requesting access
    - Note
- Integration options
- Compliance
- Availability
    - Regional considerationsMalaysia

Mail order and telephone order (MOTO) enables you to take payments over the phone or by mail by entering card details on a Stripe Terminal reader.

Supported readers: Stripe Reader S700, BBPOS WisePOS E

To begin taking MOTO payments, contact Stripe support for access.

Stripe Terminal provides you a user interface to input card details when taking payments or saving cards with MOTO. When using MOTO, the reader prompts you to enter the cardholder’s card number, CVC, expiration date, and postal code. The reader then displays a summary of the card details, before submitting them for confirmation.

MOTO transactions are card-not-present (CNP) transactions, and features available to card-present transactions (such as liability shifts and pricing) don’t apply to these subsequent charges.

You can collect MOTO payments in two ways, depending on your business needs:

You can only submit MOTO transactions when the cardholder isn’t present and they initiate the instruction over the phone or by mail. You must only submit transactions as MOTO transactions if you have determined they’re eligible. When building your checkout flow, make sure you obtain all necessary customer consents and agreements to save card details for future use. You must comply with all applicable laws and rules in your region. Review your compliance obligations, including PCI requirements.

MOTO isn’t available in Malaysia.

---

## The Charge object

**URL:** https://docs.stripe.com/api/charges/object

**Contents:**
- The Charge object
  - Attributes
    - idstring
    - amountinteger
    - balance_transactionnullable stringExpandable
    - billing_detailsobject
    - currencyenum
    - customernullable stringExpandable
    - descriptionnullable string
    - disputedboolean

Unique identifier for the object.

Amount intended to be collected by this payment. A positive integer representing how much to charge in the smallest currency unit (e.g., 100 cents to charge $1.00 or 100 to charge ¥100, a zero-decimal currency). The minimum amount is $0.50 US or equivalent in charge currency. The amount value supports up to eight digits (e.g., a value of 99999999 for a USD charge of $999,999.99).

ID of the balance transaction that describes the impact of this charge on your account balance (not including refunds or disputes).

Billing information associated with the payment method at the time of the transaction.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

ID of the customer this charge is for if one exists.

An arbitrary string attached to the object. Often useful for displaying to users.

Whether the charge has been disputed.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

ID of the PaymentIntent associated with this charge, if one exists.

Details about the payment method at the time of the transaction.

This is the email address that the receipt for this charge was sent to.

Whether the charge has been fully refunded. If the charge is only partially refunded, this attribute will still be false.

Shipping information for the charge.

For a non-card charge, text that appears on the customer’s statement as the statement descriptor. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

For a card charge, this value is ignored unless you don’t specify a statement_descriptor_suffix, in which case this value is used as the suffix.

Provides information about a card charge. Concatenated to the account’s statement descriptor prefix to form the complete statement descriptor that appears on the customer’s statement. If the account has no prefix value, the suffix is concatenated to the account’s statement descriptor.

The status of the payment is either succeeded, pending, or failed.

This method is no longer recommended—use the Payment Intents API to initiate a new payment instead. Confirmation of the PaymentIntent creates the Charge object used to request payment.

Amount intended to be collected by this payment. A positive integer representing how much to charge in the smallest currency unit (e.g., 100 cents to charge $1.00 or 100 to charge ¥100, a zero-decimal currency). The minimum amount is $0.50 US or equivalent in charge currency. The amount value supports up to eight digits (e.g., a value of 99999999 for a USD charge of $999,999.99).

Three-letter ISO currency code, in lowercase. Must be a supported currency.

The ID of an existing customer that will be charged in this request.

The maximum length is 500 characters.

An arbitrary string which you can attach to a Charge object. It is displayed when in the web interface alongside the charge. Note that if you use Stripe to send automatic email receipts to your customers, your receipt emails will include the description of the charge(s) that they are describing.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The email address to which this charge’s receipt will be sent. The receipt will not be sent until the charge is paid, and no receipts will be sent for test mode charges. If this charge is for a Customer, the email address specified here will override the customer’s email address. If receipt_email is specified for a charge in live mode, a receipt will be sent regardless of your email settings.

The maximum length is 800 characters.

Shipping information for the charge. Helps prevent fraud on charges for physical goods.

A payment source to be charged. This can be the ID of a card (i.e., credit or debit card), a bank account, a source, a token, or a connected account. For certain sources—namely, cards, bank accounts, and attached sources—you must also pass the ID of the associated customer.

For a non-card charge, text that appears on the customer’s statement as the statement descriptor. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

For a card charge, this value is ignored unless you don’t specify a statement_descriptor_suffix, in which case this value is used as the suffix.

Provides information about a card charge. Concatenated to the account’s statement descriptor prefix to form the complete statement descriptor that appears on the customer’s statement. If the account has no prefix value, the suffix is concatenated to the account’s statement descriptor.

Returns the charge object if the charge succeeded. This call raises an error if something goes wrong. A common source of error is an invalid or expired card, or a valid card with insufficient available balance.

Updates the specified charge by setting the values of the parameters passed. Any parameters not provided will be left unchanged.

The ID of an existing customer that will be associated with this request. This field may only be updated if there is no existing associated customer with this charge.

An arbitrary string which you can attach to a charge object. It is displayed when in the web interface alongside the charge. Note that if you use Stripe to send automatic email receipts to your customers, your receipt emails will include the description of the charge(s) that they are describing.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

This is the email address that the receipt for this charge will be sent to. If this field is updated, then a new email receipt will be sent to the updated address.

Shipping information for the charge. Helps prevent fraud on charges for physical goods.

Returns the charge object if the update succeeded. This call will raise an error if update parameters are invalid.

Retrieves the details of a charge that has previously been created. Supply the unique charge ID that was returned from your previous request, and Stripe will return the corresponding charge information. The same information is returned when creating or refunding the charge.

Returns a charge if a valid identifier was provided, and raises an error otherwise.

Returns a list of charges you’ve previously created. The charges are returned in sorted order, with the most recent charges appearing first.

Only return charges for the customer specified by this customer ID.

A dictionary with a data property that contains an array of up to limit charges, starting after charge starting_after. Each entry in the array is a separate charge object. If no more charges are available, the resulting array will be empty. If you provide a non-existent customer ID, this call raises an error.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "ch_3MmlLrLkdIwHu7ix0snN0B15",  "object": "charge",  "amount": 1099,  "amount_captured": 1099,  "amount_refunded": 0,  "application": null,  "application_fee": null,  "application_fee_amount": null,  "balance_transaction": "txn_3MmlLrLkdIwHu7ix0uke3Ezy",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": null,    "phone": null  },  "calculated_statement_descriptor": "Stripe",  "captured": true,  "created": 1679090539,  "currency": "usd",  "customer": null,  "description": null,  "disputed": false,  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "fraud_details": {},  "livemode": false,  "metadata": {},  "on_behalf_of": null,  "outcome": {    "network_status": "approved_by_network",    "reason": null,    "risk_level": "normal",    "risk_score": 32,    "seller_message": "Payment complete.",    "type": "authorized"  },  "paid": true,  "payment_intent": null,  "payment_method": "card_1MmlLrLkdIwHu7ixIJwEWSNR",  "payment_method_details": {    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": null      },      "country": "US",      "exp_month": 3,      "exp_year": 2024,      "fingerprint": "mToisGZ01V71BCos",      "funding": "credit",      "installments": null,      "last4": "4242",      "mandate": null,      "network": "visa",      "three_d_secure": null,      "wallet": null    },    "type": "card"  },  "receipt_email": null,  "receipt_number": null,  "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xTTJKVGtMa2RJd0h1N2l4KOvG06AGMgZfBXyr1aw6LBa9vaaSRWU96d8qBwz9z2J_CObiV_H2-e8RezSK_sw0KISesp4czsOUlVKY",  "refunded": false,  "review": null,  "shipping": null,  "source_transfer": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "succeeded",  "transfer_data": null,  "transfer_group": null}
```

Example 2 (unknown):
```unknown
{  "id": "ch_3MmlLrLkdIwHu7ix0snN0B15",  "object": "charge",  "amount": 1099,  "amount_captured": 1099,  "amount_refunded": 0,  "application": null,  "application_fee": null,  "application_fee_amount": null,  "balance_transaction": "txn_3MmlLrLkdIwHu7ix0uke3Ezy",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": null,    "phone": null  },  "calculated_statement_descriptor": "Stripe",  "captured": true,  "created": 1679090539,  "currency": "usd",  "customer": null,  "description": null,  "disputed": false,  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "fraud_details": {},  "livemode": false,  "metadata": {},  "on_behalf_of": null,  "outcome": {    "network_status": "approved_by_network",    "reason": null,    "risk_level": "normal",    "risk_score": 32,    "seller_message": "Payment complete.",    "type": "authorized"  },  "paid": true,  "payment_intent": null,  "payment_method": "card_1MmlLrLkdIwHu7ixIJwEWSNR",  "payment_method_details": {    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": null      },      "country": "US",      "exp_month": 3,      "exp_year": 2024,      "fingerprint": "mToisGZ01V71BCos",      "funding": "credit",      "installments": null,      "last4": "4242",      "mandate": null,      "network": "visa",      "three_d_secure": null,      "wallet": null    },    "type": "card"  },  "receipt_email": null,  "receipt_number": null,  "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xTTJKVGtMa2RJd0h1N2l4KOvG06AGMgZfBXyr1aw6LBa9vaaSRWU96d8qBwz9z2J_CObiV_H2-e8RezSK_sw0KISesp4czsOUlVKY",  "refunded": false,  "review": null,  "shipping": null,  "source_transfer": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "succeeded",  "transfer_data": null,  "transfer_group": null}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/charges \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=1099 \  -d currency=usd \  -d source=tok_visa
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/charges \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=1099 \  -d currency=usd \  -d source=tok_visa
```

---

## Authenticate with 3D Secure

**URL:** https://docs.stripe.com/payments/3d-secure/authentication-flow

**Contents:**
- Authenticate with 3D Secure
- Integrate 3D Secure (3DS) into your checkout flow.
    - Caution
- Control the 3DS flow
  - Use Radar rules in the Dashboard
  - Manually request 3DS with the API
    - Caution
- Display the 3DS flow
  - Redirect to the bank website
  - Display in an iframe

Major card brands no longer support 3D Secure 1. If your implementation uses 3D Secure 1, update it to use the Payment Intents and Setup Intents APIs. Using those APIs:

You can integrate 3D Secure (3DS) authentication into your checkout flow on multiple platforms, including Web, iOS, Android, and React Native. This integration runs 3D Secure 2 (3DS2) when supported by the customer’s bank and falls back to 3D Secure 1 otherwise. You can also perform 3DS authentication on Stripe while acquiring the transaction with another payment service provider (PSP) by using the Standalone 3DS product.

The customer enters their card details.

The customer’s bank assesses the transaction and can complete 3D Secure at this step.

If required by their bank, the customer completes an additional authentication step.

Stripe triggers 3DS automatically if mandated by regulations such as Strong Customer Authentication in Europe, industry guidelines such as the Credit Card Security Guidelines in Japan, if requested by an issuer with a soft decline code, or if certain Stripe optimizations apply.

You can also use Radar or the API to decide when to prompt users for 3DS authentication. This allows you to customize the authentication process for each user based on your chosen parameters. However, not all transactions support 3DS, for example wallets or off-session payments.

When a payment triggers 3DS, the card issuer might require the customer to authenticate to complete the payment, as long as 3DS authentication is supported for that card. While Stripe initiates the authentication request, the requirement comes from the issuer. Depending on the front end you’re using, this might require you to display the 3DS flow.

In a typical Payment Intent API flow that triggers 3DS:

To track whether 3DS was supported and attempted on a card payment, read the three_d_secure property on the card information in the Charge’s payment_method_details. Stripe populates the three_d_secure property when the customer attempts to authenticate the card—three_d_secure.result indicates the authentication outcome.

Stripe provides fraud controls to dynamically request 3DS when creating or confirming a PaymentIntent or SetupIntent. You can configure these rules in your Dashboard.

If you have Radar for Fraud Teams, you can add custom 3DS rules.

The default method to trigger 3DS is using Radar to dynamically request 3D Secure based on risk level and other requirements. Triggering 3DS manually is for advanced users integrating Stripe with their own fraud engine.

To trigger 3DS manually, set payment_method_options[card][request_three_d_secure] depending on what you want to optimize for when either creating or confirming a PaymentIntent or SetupIntent, or creating a Checkout Session. This process is the same for one-time payments or when setting up a payment method for future payments. When you provide this parameter, Stripe attempts to perform 3DS and overrides any dynamic 3D Secure Radar rules on the PaymentIntent, SetupIntent, or Checkout Session.

When to provide this parameter depends on when your fraud engine detects risk. For example, if your fraud engine only inspects card details, you know whether to request 3DS before you create the PaymentIntent or SetupIntent. If your fraud engine inspects both card and transaction details, provide the parameter during confirmation—when you have more information. Then pass the resulting PaymentIntent or SetupIntent to your client to complete the process.

Explore the request_three_d_secure parameter’s usage for each case in the API reference:

Set request_three_d_secure to any to manually request 3DS with a preference for a frictionless flow, increasing the likelihood of the authentication being completed without any additional input from the customer.

Set request_three_d_secure to challenge to request 3DS with a preference for a challenge flow, where the customer must respond to a prompt for active authentication.

Stripe can’t guarantee your preference because the issuer determines the ultimate authentication flow. You can find out what the ultimate authentication flow was by inspecting the authentication_flow on the three_d_secure property of the Charge or SetupAttempt. To learn more about 3DS flows, read our guide.

Stripe only prompts your customer to perform authentication if 3DS authentication is available for a card. If it’s not available for the given card or if an error occurred during the authentication process, the payment proceeds normally.

Stripe’s mandatory authentication rules run automatically, regardless of whether or not you manually request 3DS. Any 3DS requests from you are additional to those required for SCA.

Stripe automatically displays the authentication UI in a pop-up modal when calling confirmCardPayment and handleCardAction. You can also redirect to the bank’s website or use an iframe.

Stripe.js collects basic device information during 3DS2 authentication and sends it to the issuing bank for their risk analysis.

To redirect your customer to the 3DS authentication page, pass a return_url to the PaymentIntent when confirming on the server or on the client.

After confirmation, if a PaymentIntent has a requires_action status, inspect the PaymentIntent’s next_action. If it contains redirect_to_url, that means 3DS is required.

In the browser, redirect the customer to the url in the redirect_to_url hash to complete authentication.

When the customer finishes the authentication process, the redirect sends them back to the return_url you specified when you created or confirmed the PaymentIntent. The redirect also adds payment_intent and payment_intent_client_secret URL query parameters that your application can use to identify the PaymentIntent associated with the purchase.

You can’t customize the authentication UI on the web to match your website’s design—the bank that issued the card controls the fonts and colors.

However, you can choose how and where to show the 3DS UI. Most businesses show it in a modal dialog above their payment page. If you have your own modal component, you can place the 3DS frame inside of it. You can also show the authentication content inline with your payment form.

When your customer is ready to complete their purchase, you confirm the PaymentIntent to begin the process of collecting their payment.

If you want to control how to display 3DS, provide a return_url, which is where the 3DS <iframe> is redirected when authentication is complete. If your site uses a content security policy, check that it allows iframes from https://js.stripe.com, https://hooks.stripe.com, and the origin of the URL you passed to return_url.

If you’re confirming from the frontend, use the confirmCardPayment method in Stripe.js. For example, if you’re gathering card information using Stripe Elements:

If you confirm from your server, provide a return_url. Depending on your integration, you might want to pass other information to confirm as well.

Next, inspect the status property property of the confirmed PaymentIntent to determine whether the payment completed successfully. The following list describes possible status values and their significance:

On versions of the API before 2019-02-11, requires_payment_method appears as requires_source and requires_action appears as requires_source_action.

When the value of the status property is requires_action, you need to complete an additional step before processing the payment. For a card payment that requires 3DS, the PaymentIntent’s status shows as requires_action and its next_action property appears as redirect_to_url. The redirect_to_url payload contains a URL that opens in an iframe to display 3DS:

For 3DS2, card issuers are required to support showing the 3DS content at sizes of 250x400, 390x400, 500x600, 600x400, and full screen (dimensions are width by height). You might enhance the 3DS UI by opening the iframe at exactly one of those sizes.

You can’t use the sandbox attribute on the 3DS iframe. In live mode, the card issuer controls some content inside this iframe. Some issuers’ implementations fail if they’re sandboxed, and the payment won’t succeed.

After the customer completes 3DS, the iframe redirects to the return_url you provided when confirming the PaymentIntent. That page needs to postMessage to your top-level page to inform it that 3DS authentication is complete. Your top-level page then needs to determine whether the payment succeeded or requires further action from your customer.

For example, you might have your return_url page execute:

Your top payment page needs to listen for this postMessage to know when authentication has finished. You then need to retrieve the updated PaymentIntent and check on the status of the payment. If the authentication failed, the PaymentIntent’s status is requires_payment_method. If the payment completed successfully, the status is succeeded. If you use separate authorize and capture, the status is requires_capture instead.

Use a Stripe test card with any CVC, postal code, and future expiration date to trigger 3DS authentication challenge flows while in a sandbox.

When you build an integration with your test API keys, the authentication process displays a mock authentication page. On that page, you can either authorize or cancel the payment. Authorizing the payment simulates successful authentication and redirects you to the specified return URL. Clicking the Failure button simulates an unsuccessful attempt at authentication.

All other Visa and Mastercard test cards don’t require authentication from the customer’s card issuer.

You can write custom Radar rules in a test environment to trigger authentication on test cards. Learn more about testing your Radar rules.

The liability shift rule typically applies to payments successfully authenticated using 3DS. In some cases, liability shift applies with equivalent cryptograms, such as Apple Pay or Google Pay. If a cardholder disputes a 3DS payment as fraudulent, the liability typically shifts from you to the card issuer.

If a card doesn’t support 3DS or an error occurs during the authentication process, the payment proceeds normally. When this occurs, liability doesn’t generally shift to the issuer, because a successful 3DS authentication hasn’t taken place.

In practice, this means you typically won’t receive disputes marked as fraudulent if the payment is covered by the liability shift rule, but you might still receive an Early Fraud Warning. You might still receive a low percentage of fraudulent disputes, and we list a few cases below where the liability shift rule might not apply.

You might receive a dispute inquiry on a successfully authenticated payment using 3DS. This type of dispute doesn’t precipitate a chargeback because it’s only a request for information.

If you receive an inquiry for a 3D-Secure-authenticated charge, you must respond. If you don’t, the cardholder’s bank can initiate a financial chargeback known as a “no-reply” chargeback that could invalidate the liability shift. To prevent no-reply chargebacks on 3DS charges, submit sufficient information about the charge. Include information about what was ordered, how it was delivered, and who it was delivered to (whether it was physical or electronic goods, or services).

If a customer disputes a payment for any other reason (for example, product not received), then the standard dispute process applies. Make informed decisions about your business management, especially in handling and completely avoiding disputes.

Liability shift might also occur when the card network requires 3DS, but it isn’t available for the card or issuer. This can happen if the issuer’s 3DS provider is down or if the issuer doesn’t support it, despite the card network requiring support. During the payment process, the cardholder isn’t prompted to complete 3DS authentication, because the card isn’t enrolled. Although the cardholder didn’t complete 3DS authentication, liability can still shift to the issuer.

Stripe returns the requested Electronic Commerce Indicator (ECI) in the electronic_commerce_indicator of the 3DS authentication outcome. This indicator can aid in determining whether a charge should adhere to the liability shift rule. As 3DS occurs subsequent to the initial payment intent response, you typically get this from a charge.succeeded event that’s sent to one of your configured webhook endpoints or other event destinations. A requested ECI might be degraded in the issuer response, which we don’t reveal.

Sometimes payments that are successfully authenticated using 3DS don’t fall under liability shift. This is rare and can happen, for example, if you have an excessive level of fraud on your account and are enrolled in a fraud monitoring program. Certain networks have also exempted some industries from liability shift. For example, Visa doesn’t support liability shift for businesses engaging in wire transfer or money orders, non-financial institutions offering foreign or non-fiat currency, or stored-value card purchase or load.

It’s also possible for liability shift to get downgraded post-authorization, or the card network’s dispute rejection system might fail to catch liability shift for a transaction. In these cases, if you counter the dispute, Stripe automatically adds the requested ECI and the 3DS authentication outcome of the payment to your evidence details, but we recommend you also include additional details to increase your chance of winning the dispute.

If you have Radar for Fraud Teams, you can customize your rules to control when to request 3DS and how to handle each specific authentication outcome and liability shift. Stripe’s Strong Customer Authentication (SCA) rules run automatically and independently of custom Radar rules, and block unauthenticated payments unless exempted.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=1000 \
  -d currency=usd \
  -d "payment_method_options[card][request_three_d_secure]"=any
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=1000 \
  -d currency=usd \
  -d "payment_method_options[card][request_three_d_secure]"=any
```

Example 3 (unknown):
```unknown
next_action: {
    type: 'redirect_to_url',
    redirect_to_url: {
      url: 'https://hooks.stripe.com/...',
      return_url: 'https://mysite.com'
    }
}
```

Example 4 (unknown):
```unknown
next_action: {
    type: 'redirect_to_url',
    redirect_to_url: {
      url: 'https://hooks.stripe.com/...',
      return_url: 'https://mysite.com'
    }
}
```

---

## Regional considerations

**URL:** https://docs.stripe.com/terminal/payments/regional

**Contents:**
- Regional considerations
- Learn about regional considerations for integrating Terminal in different countries.
    - Note
- Availability
- Regional considerations by country
- Integrate Terminal in the United States
  - Use locations

​​For the most part, you’ll be able to use a single Terminal integration in all supported countries. However, due to local payment methods or regulations there are some country-specific requirements. After going through the sample integration, use this guide to learn about country-specific requirements for Terminal.

To process Terminal payments, both the Stripe account receiving the funds and the location associated with the reader must be in the same country, accepting local currency only.

Refer to the following table to understand which readers you can use in each country.

Select a country to view its specific regional considerations

Stripe supports Visa, Mastercard, American Express, and Discover payments in the United States. All transactions must be made in US dollars (USD). To accept Terminal charges in the United States, either your platform account or connected account must be in the United States.

Create Locations for your business with addresses in the United States and associate your readers to them. This will ensure that they automatically download the configuration needed to properly process charges in the United States. A valid address for a Location in the United States must contain the line1, city, state, postal_code, and country properties.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/locations \
  -u sk_test_YOUR_TEST_KEY_HERE: \
  -d "display_name"="HQ" \
  -d "address[line1]"="1272 Valencia Street" \
  -d "address[city]"="San Francisco" \
  -d "address[state]"="CA" \
  -d "address[country]"="US" \
  -d "address[postal_code]"="94110" \
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/locations \
  -u sk_test_YOUR_TEST_KEY_HERE: \
  -d "display_name"="HQ" \
  -d "address[line1]"="1272 Valencia Street" \
  -d "address[city]"="San Francisco" \
  -d "address[state]"="CA" \
  -d "address[country]"="US" \
  -d "address[postal_code]"="94110" \
```

---

## Migrate to the Payment Intents and Payment Methods APIs

**URL:** https://docs.stripe.com/payments/payment-methods/transitioning

**Contents:**
- Migrate to the Payment Intents and Payment Methods APIs
- Learn how to transition from the Sources and Tokens APIs to the Payment Methods API.
- Migrate local payment methods from the Sources API to the Payment Intents API
    - Caution
  - Checking payment status
  - Refunds
  - Error handling
  - Webhooks
- Transitioning to the Payment Methods API
    - Note

The Payment Methods API replaces the existing Tokens and Sources APIs as the recommended way for integrations to collect and store payment information. It works with the Payment Intents API to create payments for a wide range of payment methods.

We plan to turn off Sources API support for local payment methods. If you currently handle any local payment methods using the Sources API, you must migrate them to the Payment Methods API. We’ll send email communication with more information about the end of support for the Sources and Tokens APIs.

While we don’t plan to turn off support for card payment methods, we still recommend that you migrate them to the Payment Methods and Payment Intents APIs. For more information about migrating card payment methods, see Migrating to the Payment Intents API.

To migrate your integration for local payment methods, update your server and front end to use the PaymentIntents API. There are three typical integration options:

If you use Stripe Checkout or the Payment Element, you can add and manage most payment methods from the Stripe Dashboard without making code changes.

For specific information about integrating a local payment method using the Payment Methods API, see the instructions for that payment method in the payment methods documentation. The following table provides a high-level comparison of the different payment types.

A PaymentIntent object represents a payment in the new integration, and it creates a Charge when you confirm the payment on the front end. If you previously stored references to the Charge, you can continue to do so by fetching the Charge ID from the PaymentIntent after the customer completes the payment. However, we also recommend that you store the PaymentIntent ID.

Previously, your integration should have checked both the status of the Source and the status of the Charge after each API call. You no longer need to check two statuses—you only need to check the status of the PaymentIntent or the Checkout Session after you confirm it on the front end.

Always confirm the status of the PaymentIntent by fetching it on your server or listening for the webhooks on your server. Don’t rely solely on the user returning to the return_url that’s provided when you confirm the PaymentIntent.

You can continue to call the Refunds API with a Charge that the PaymentIntent creates. The ID of the Charge is accessible on the latest_charge parameter.

Alternatively, you can provide the PaymentIntent ID to the Refunds API instead of the Charge.

Previously, you had to handle errors on the Sources. With PaymentIntents, instead of checking for errors on a Source, you check for errors on the PaymentIntent when it’s created and after the customer has authorized the payment. Most errors on the PaymentIntent are of invalid_request_error type, returned in an invalid request.

When you migrate your integration, keep in mind that PaymentIntent error codes can differ from the corresponding error codes for Sources.

If you previously listened to Source events, you might need to update your integration to listen to new event types. The following table shows some examples.

The main difference between the Payment Methods and Sources APIs is that Sources describes the transaction state through the status property. That means that each Source object must transition to a chargeable state before you can use it for a payment. By contrast, a PaymentMethod is stateless, relying on the PaymentIntent object to represent payment state.

The following table isn’t a comprehensive list of payment methods. If you integrate other payment methods with the Sources API, migrate them to the Payment Methods API as well.

After you choose the API to integrate with, use the guide to payment methods to help you determine the right payment method types you need to support.

This guide includes detailed descriptions of each payment method and describes the differences in the customer-facing flows, along with the geographic regions where they’re most relevant. You can enable any payment method available to you within the Dashboard. Activation is generally instantaneous and doesn’t require additional contracts.

If you previously processed any of the following reusable payment methods using Sources, the existing saved sources don’t migrate automatically:

To preserve your existing customers’ saved payment methods, you must convert those sources to payment methods using a data migration tool in the Stripe Dashboard. For instructions on how to convert them, see the support page.

If you previously collected card customer payment details with Stripe using cards or Sources, you can start using the Payment Methods API immediately without migrating any payment information.

Compatible payment methods that have been saved to a Customer are usable in any API that accepts a PaymentMethod object. For example, you can use a saved card as a PaymentMethod when creating a PaymentIntent:

Remember to provide the customer ID that your compatible payment method is saved to when attaching the object to a PaymentIntent.

You can retrieve all saved compatible payment methods through the Payment Methods API.

With this compatibility, no new objects are created; the Payment Methods API provides a different view of the same underlying object. For example, updates to a compatible payment method through the Payment Methods API is visible through the Sources API, and vice versa.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d "payment_method_types[]"=card \
  -d amount=1099 \
  -d currency=usd \
  -d customer="{{CUSTOMER_ID}}" \
  -d payment_method="{{CARD_ID}}"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d "payment_method_types[]"=card \
  -d amount=1099 \
  -d currency=usd \
  -d customer="{{CUSTOMER_ID}}" \
  -d payment_method="{{CARD_ID}}"
```

Example 3 (unknown):
```unknown
{
  "id": "card_1EBXBSDuWL9wT9brGOaALeD2",
  "object": "card",
  "address_city": "San Francisco",
  "address_country": "US",
  "address_line1": "1234 Fake Street",
  "address_line1_check": null,
  "address_line2": null,
  "address_state": null,
  "address_zip": null,
```

Example 4 (unknown):
```unknown
{
  "id": "card_1EBXBSDuWL9wT9brGOaALeD2",
  "object": "card",
  "address_city": "San Francisco",
  "address_country": "US",
  "address_line1": "1234 Fake Street",
  "address_line1_check": null,
  "address_line2": null,
  "address_state": null,
  "address_zip": null,
```

---

## Create a charge Deprecated

**URL:** https://docs.stripe.com/api/charges/create

**Contents:**
- Create a charge Deprecated
  - Parameters
    - amountintegerRequired
    - currencyenumRequired
    - customerstring
    - descriptionstring
    - metadataobject
    - receipt_emailstring
    - shippingobject
    - sourcestring

This method is no longer recommended—use the Payment Intents API to initiate a new payment instead. Confirmation of the PaymentIntent creates the Charge object used to request payment.

Amount intended to be collected by this payment. A positive integer representing how much to charge in the smallest currency unit (e.g., 100 cents to charge $1.00 or 100 to charge ¥100, a zero-decimal currency). The minimum amount is $0.50 US or equivalent in charge currency. The amount value supports up to eight digits (e.g., a value of 99999999 for a USD charge of $999,999.99).

Three-letter ISO currency code, in lowercase. Must be a supported currency.

The ID of an existing customer that will be charged in this request.

The maximum length is 500 characters.

An arbitrary string which you can attach to a Charge object. It is displayed when in the web interface alongside the charge. Note that if you use Stripe to send automatic email receipts to your customers, your receipt emails will include the description of the charge(s) that they are describing.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The email address to which this charge’s receipt will be sent. The receipt will not be sent until the charge is paid, and no receipts will be sent for test mode charges. If this charge is for a Customer, the email address specified here will override the customer’s email address. If receipt_email is specified for a charge in live mode, a receipt will be sent regardless of your email settings.

The maximum length is 800 characters.

Shipping information for the charge. Helps prevent fraud on charges for physical goods.

A payment source to be charged. This can be the ID of a card (i.e., credit or debit card), a bank account, a source, a token, or a connected account. For certain sources—namely, cards, bank accounts, and attached sources—you must also pass the ID of the associated customer.

For a non-card charge, text that appears on the customer’s statement as the statement descriptor. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

For a card charge, this value is ignored unless you don’t specify a statement_descriptor_suffix, in which case this value is used as the suffix.

Provides information about a card charge. Concatenated to the account’s statement descriptor prefix to form the complete statement descriptor that appears on the customer’s statement. If the account has no prefix value, the suffix is concatenated to the account’s statement descriptor.

Returns the charge object if the charge succeeded. This call raises an error if something goes wrong. A common source of error is an invalid or expired card, or a valid card with insufficient available balance.

Updates the specified charge by setting the values of the parameters passed. Any parameters not provided will be left unchanged.

The ID of an existing customer that will be associated with this request. This field may only be updated if there is no existing associated customer with this charge.

An arbitrary string which you can attach to a charge object. It is displayed when in the web interface alongside the charge. Note that if you use Stripe to send automatic email receipts to your customers, your receipt emails will include the description of the charge(s) that they are describing.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

This is the email address that the receipt for this charge will be sent to. If this field is updated, then a new email receipt will be sent to the updated address.

Shipping information for the charge. Helps prevent fraud on charges for physical goods.

Returns the charge object if the update succeeded. This call will raise an error if update parameters are invalid.

Retrieves the details of a charge that has previously been created. Supply the unique charge ID that was returned from your previous request, and Stripe will return the corresponding charge information. The same information is returned when creating or refunding the charge.

Returns a charge if a valid identifier was provided, and raises an error otherwise.

Returns a list of charges you’ve previously created. The charges are returned in sorted order, with the most recent charges appearing first.

Only return charges for the customer specified by this customer ID.

A dictionary with a data property that contains an array of up to limit charges, starting after charge starting_after. Each entry in the array is a separate charge object. If no more charges are available, the resulting array will be empty. If you provide a non-existent customer ID, this call raises an error.

Capture the payment of an existing, uncaptured charge that was created with the capture option set to false.

Uncaptured payments expire a set number of days after they are created (7 by default), after which they are marked as refunded and capture attempts will fail.

Don’t use this method to capture a PaymentIntent-initiated charge. Use Capture a PaymentIntent.

The amount to capture, which must be less than or equal to the original amount.

The email address to send this charge’s receipt to. This will override the previously-specified email address for this charge, if one was set. Receipts will not be sent in test mode.

The maximum length is 800 characters.

For a non-card charge, text that appears on the customer’s statement as the statement descriptor. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

For a card charge, this value is ignored unless you don’t specify a statement_descriptor_suffix, in which case this value is used as the suffix.

Provides information about a card charge. Concatenated to the account’s statement descriptor prefix to form the complete statement descriptor that appears on the customer’s statement. If the account has no prefix value, the suffix is concatenated to the account’s statement descriptor.

Returns the charge object, with an updated captured property (set to true). Capturing a charge will always succeed, unless the charge is already refunded, expired, captured, or an invalid capture amount is specified, in which case this method will raise an error.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/charges \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=1099 \  -d currency=usd \  -d source=tok_visa
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/charges \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=1099 \  -d currency=usd \  -d source=tok_visa
```

Example 3 (unknown):
```unknown
{  "id": "ch_3MmlLrLkdIwHu7ix0snN0B15",  "object": "charge",  "amount": 1099,  "amount_captured": 1099,  "amount_refunded": 0,  "application": null,  "application_fee": null,  "application_fee_amount": null,  "balance_transaction": "txn_3MmlLrLkdIwHu7ix0uke3Ezy",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": null,    "phone": null  },  "calculated_statement_descriptor": "Stripe",  "captured": true,  "created": 1679090539,  "currency": "usd",  "customer": null,  "description": null,  "disputed": false,  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "fraud_details": {},  "livemode": false,  "metadata": {},  "on_behalf_of": null,  "outcome": {    "network_status": "approved_by_network",    "reason": null,    "risk_level": "normal",    "risk_score": 32,    "seller_message": "Payment complete.",    "type": "authorized"  },  "paid": true,  "payment_intent": null,  "payment_method": "card_1MmlLrLkdIwHu7ixIJwEWSNR",  "payment_method_details": {    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": null      },      "country": "US",      "exp_month": 3,      "exp_year": 2024,      "fingerprint": "mToisGZ01V71BCos",      "funding": "credit",      "installments": null,      "last4": "4242",      "mandate": null,      "network": "visa",      "three_d_secure": null,      "wallet": null    },    "type": "card"  },  "receipt_email": null,  "receipt_number": null,  "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xTTJKVGtMa2RJd0h1N2l4KOvG06AGMgZfBXyr1aw6LBa9vaaSRWU96d8qBwz9z2J_CObiV_H2-e8RezSK_sw0KISesp4czsOUlVKY",  "refunded": false,  "review": null,  "shipping": null,  "source_transfer": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "succeeded",  "transfer_data": null,  "transfer_group": null}
```

Example 4 (unknown):
```unknown
{  "id": "ch_3MmlLrLkdIwHu7ix0snN0B15",  "object": "charge",  "amount": 1099,  "amount_captured": 1099,  "amount_refunded": 0,  "application": null,  "application_fee": null,  "application_fee_amount": null,  "balance_transaction": "txn_3MmlLrLkdIwHu7ix0uke3Ezy",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": null,    "phone": null  },  "calculated_statement_descriptor": "Stripe",  "captured": true,  "created": 1679090539,  "currency": "usd",  "customer": null,  "description": null,  "disputed": false,  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "fraud_details": {},  "livemode": false,  "metadata": {},  "on_behalf_of": null,  "outcome": {    "network_status": "approved_by_network",    "reason": null,    "risk_level": "normal",    "risk_score": 32,    "seller_message": "Payment complete.",    "type": "authorized"  },  "paid": true,  "payment_intent": null,  "payment_method": "card_1MmlLrLkdIwHu7ixIJwEWSNR",  "payment_method_details": {    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": null      },      "country": "US",      "exp_month": 3,      "exp_year": 2024,      "fingerprint": "mToisGZ01V71BCos",      "funding": "credit",      "installments": null,      "last4": "4242",      "mandate": null,      "network": "visa",      "three_d_secure": null,      "wallet": null    },    "type": "card"  },  "receipt_email": null,  "receipt_number": null,  "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xTTJKVGtMa2RJd0h1N2l4KOvG06AGMgZfBXyr1aw6LBa9vaaSRWU96d8qBwz9z2J_CObiV_H2-e8RezSK_sw0KISesp4czsOUlVKY",  "refunded": false,  "review": null,  "shipping": null,  "source_transfer": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "succeeded",  "transfer_data": null,  "transfer_group": null}
```

---

## 3D Secure authentication

**URL:** https://docs.stripe.com/payments/3d-secure

**Contents:**
- 3D Secure authentication
- Reduce fraud and meet regulatory requirements through 3D Secure (3DS) authentication.

3D Secure (3DS) is an authentication protocol that adds an additional security layer to card transactions. By verifying that the person making a purchase is the legitimate cardholder, 3DS helps protect both your business and your customers from fraudulent activity. When 3DS is activated, the issuing bank might request cardholders authenticate—typically through a familiar security prompt like a password, one-time code sent to their mobile device, or biometric verification. Customers may recognize this process through card network branding such as Visa Secure, Mastercard Identity Check or American Express SafeKey.

The Strong Customer Authentication (SCA) regulation, as part of PSD2 in the EEA and similar regulations in the UK, India, Japan, and Australia, might require using 3DS for card payments. 3DS is optional in other regions but you can still use it as a tool to reduce fraud.

Integrate 3D Secure (3DS) into your checkout flow.

Use SCA exemptions and Data Only to reduce cardholder friction on eligible transactions.

Run 3D Secure on Stripe while processing the subsequent payment on a third-party gateway.

Process payments when 3D Secure (3DS) runs outside of Stripe.

Learn how 3D Secure affects your payment success rate in the Dashboard.

---

## Balances and settlement time

**URL:** https://docs.stripe.com/payments/balances

**Contents:**
- Balances and settlement time
- Learn about balance states, settlement timing, and best practices for balance management.
- Balance types
  - Payments balance
  - Refunds and disputes balance
  - Reserve balance
  - Financial account US and UK only
- Balance states
  - Pending
  - Available

Your Stripe account can have one or more balances that hold funds for different products and currencies. Understanding balance states, settlement time, and potential ways to accelerate settlement can help you manage your funds and avoid negative balances.

The following are available balance types. There are other balance types, such as Connect balances and Issuing balance, but you need to onboard to their respective products to access them.

Your payments balance represents all of your incoming transactions from customer charges. When a customer makes a purchase using a card or local payment method, the funds pass through the payments balance and eventually settle. When a customer initiates a refund or files a dispute, funds are also deducted from the payments balance. You can also use your payments balance to reconcile all of your transactions and payouts to an external bank account.

You can choose to set aside funds for future refunds or disputes in your refunds and dispute balance. You can fund this balance by making an external top up.

Sometimes, Stripe might create a reserve balance on your behalf to ensure that your Stripe account can cover any expected incoming refunds or disputes. The reserve balance holds funds that you can’t pay out or transfer until the reserve hold period is complete.

Your financial account allows you to store funds on Stripe in USD, GBP, or EUR. You can fund this balance with earnings from your payments balance or external top ups from your bank account. You can use your financial account to send money to others, create a card to spend from, or instantly convert between currencies.

When Stripe processes a payment or a funding transaction, funds move through different balance states before you can use them: pending and available. These two states are generally affected by the settlement timing, which can vary by location and sometimes by payment method. Funds in a Balance transition from pending to available at the corresponding available_on time for each balance transaction.

Funds in the pending state represent incoming transactions that haven’t settled into your balance. For example, when a customer makes a card payment, the charge amount (minus Stripe’s fee) appears in your pending balance until settlement. You can’t withdraw or spend these funds until they’re available.

Eligible users have options to immediately access pending funds using Instant Payouts, or to reduce settlement time using Stripe features. For more details, see Accelerate settlement timing.

After the funds settle, they move to your available balance. You can use these funds for payouts to bank accounts, refunds, transfers, or any other debit transaction.

Settlement time is the time between when a payment or a funding transaction is made and when the funds become available in your Stripe balance.

For example, if a customer makes a 100 USD card payment on Monday in the US, the funds are initially pending. Then the funds are available in your balance on Wednesday, 2 business days later.

Settlement timing varies based on your country and the payment method used.

There are two definitions of days that affect settlement and payout timing:

For example, a charge created on a Saturday could have two different timings depending on which definition of day you use:

Use the following collapsed table to determine your country’s settlement timing. The initial settlement timing applies to your first payout, and the default settlement timing applies to subsequent payouts.

In some cases, risk criteria might prevent your account from changing to the default settlement timing.

Bank debit payment methods typically have longer settlement times than card payments because of the underlying banking systems. These payments have a higher risk of returns or reversals, which factors into their longer settlement periods.

To manage your cash flow and cover potential refunds, disputes, and fees that might lead to negative balances, you can set a minimum balance in your Stripe account.

Stripe offers products and payment methods that have reduced settlement time depending on your location and are subject to eligibility criteria.

For eligible US merchants, Stripe offers faster ACH settlement that reduces the settlement time from 4 business days to 2 business days from payment creation. For more details about eligibility and activation, see the ACH support page.

Instant Payouts gives you access to your funds immediately following a successful card charge. To learn about eligibility requirements, fees, and supported countries, see Instant Payouts.

---

## Update a charge

**URL:** https://docs.stripe.com/api/charges/update

**Contents:**
- Update a charge
  - Parameters
    - customerstring
    - descriptionstring
    - metadataobject
    - receipt_emailstring
    - shippingobject
  - More parametersExpand all
    - fraud_detailsobject
    - transfer_groupstringConnect only

Updates the specified charge by setting the values of the parameters passed. Any parameters not provided will be left unchanged.

The ID of an existing customer that will be associated with this request. This field may only be updated if there is no existing associated customer with this charge.

An arbitrary string which you can attach to a charge object. It is displayed when in the web interface alongside the charge. Note that if you use Stripe to send automatic email receipts to your customers, your receipt emails will include the description of the charge(s) that they are describing.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

This is the email address that the receipt for this charge will be sent to. If this field is updated, then a new email receipt will be sent to the updated address.

Shipping information for the charge. Helps prevent fraud on charges for physical goods.

Returns the charge object if the update succeeded. This call will raise an error if update parameters are invalid.

Retrieves the details of a charge that has previously been created. Supply the unique charge ID that was returned from your previous request, and Stripe will return the corresponding charge information. The same information is returned when creating or refunding the charge.

Returns a charge if a valid identifier was provided, and raises an error otherwise.

Returns a list of charges you’ve previously created. The charges are returned in sorted order, with the most recent charges appearing first.

Only return charges for the customer specified by this customer ID.

A dictionary with a data property that contains an array of up to limit charges, starting after charge starting_after. Each entry in the array is a separate charge object. If no more charges are available, the resulting array will be empty. If you provide a non-existent customer ID, this call raises an error.

Capture the payment of an existing, uncaptured charge that was created with the capture option set to false.

Uncaptured payments expire a set number of days after they are created (7 by default), after which they are marked as refunded and capture attempts will fail.

Don’t use this method to capture a PaymentIntent-initiated charge. Use Capture a PaymentIntent.

The amount to capture, which must be less than or equal to the original amount.

The email address to send this charge’s receipt to. This will override the previously-specified email address for this charge, if one was set. Receipts will not be sent in test mode.

The maximum length is 800 characters.

For a non-card charge, text that appears on the customer’s statement as the statement descriptor. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

For a card charge, this value is ignored unless you don’t specify a statement_descriptor_suffix, in which case this value is used as the suffix.

Provides information about a card charge. Concatenated to the account’s statement descriptor prefix to form the complete statement descriptor that appears on the customer’s statement. If the account has no prefix value, the suffix is concatenated to the account’s statement descriptor.

Returns the charge object, with an updated captured property (set to true). Capturing a charge will always succeed, unless the charge is already refunded, expired, captured, or an invalid capture amount is specified, in which case this method will raise an error.

Search for charges you’ve previously created using Stripe’s Search Query Language. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.

The search query string. See search query language and the list of supported query fields for charges.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A dictionary with a data property that contains an array of up to limit charges. If no objects match the query, the resulting array will be empty. See the related guide on expanding properties in lists.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/charges/ch_3MmlLrLkdIwHu7ix0snN0B15 \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[shipping]"=express
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/charges/ch_3MmlLrLkdIwHu7ix0snN0B15 \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[shipping]"=express
```

Example 3 (unknown):
```unknown
{  "id": "ch_3MmlLrLkdIwHu7ix0snN0B15",  "object": "charge",  "amount": 1099,  "amount_captured": 1099,  "amount_refunded": 0,  "application": null,  "application_fee": null,  "application_fee_amount": null,  "balance_transaction": "txn_3MmlLrLkdIwHu7ix0uke3Ezy",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": null,    "phone": null  },  "calculated_statement_descriptor": "Stripe",  "captured": true,  "created": 1679090539,  "currency": "usd",  "customer": null,  "description": null,  "disputed": false,  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "fraud_details": {},  "livemode": false,  "metadata": {    "shipping": "express"  },  "on_behalf_of": null,  "outcome": {    "network_status": "approved_by_network",    "reason": null,    "risk_level": "normal",    "risk_score": 32,    "seller_message": "Payment complete.",    "type": "authorized"  },  "paid": true,  "payment_intent": null,  "payment_method": "card_1MmlLrLkdIwHu7ixIJwEWSNR",  "payment_method_details": {    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": null      },      "country": "US",      "exp_month": 3,      "exp_year": 2024,      "fingerprint": "mToisGZ01V71BCos",      "funding": "credit",      "installments": null,      "last4": "4242",      "mandate": null,      "network": "visa",      "network_token": {        "used": false      },      "three_d_secure": null,      "wallet": null    },    "type": "card"  },  "receipt_email": null,  "receipt_number": null,  "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xTTJKVGtMa2RJd0h1N2l4KPDLl6UGMgawkab5iK86LBYtkq0XrhiQf1RsA2ubesH4GHiixEU8_1-Wp7h4oQEdfSUGiZpJwtQHBErT",  "refunded": false,  "refunds": {    "object": "list",    "data": [],    "has_more": false,    "total_count": 0,    "url": "/v1/charges/ch_3MmlLrLkdIwHu7ix0snN0B15/refunds"  },  "review": null,  "shipping": null,  "source_transfer": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "succeeded",  "transfer_data": null,  "transfer_group": null}
```

Example 4 (unknown):
```unknown
{  "id": "ch_3MmlLrLkdIwHu7ix0snN0B15",  "object": "charge",  "amount": 1099,  "amount_captured": 1099,  "amount_refunded": 0,  "application": null,  "application_fee": null,  "application_fee_amount": null,  "balance_transaction": "txn_3MmlLrLkdIwHu7ix0uke3Ezy",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": null,    "phone": null  },  "calculated_statement_descriptor": "Stripe",  "captured": true,  "created": 1679090539,  "currency": "usd",  "customer": null,  "description": null,  "disputed": false,  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "fraud_details": {},  "livemode": false,  "metadata": {    "shipping": "express"  },  "on_behalf_of": null,  "outcome": {    "network_status": "approved_by_network",    "reason": null,    "risk_level": "normal",    "risk_score": 32,    "seller_message": "Payment complete.",    "type": "authorized"  },  "paid": true,  "payment_intent": null,  "payment_method": "card_1MmlLrLkdIwHu7ixIJwEWSNR",  "payment_method_details": {    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": null      },      "country": "US",      "exp_month": 3,      "exp_year": 2024,      "fingerprint": "mToisGZ01V71BCos",      "funding": "credit",      "installments": null,      "last4": "4242",      "mandate": null,      "network": "visa",      "network_token": {        "used": false      },      "three_d_secure": null,      "wallet": null    },    "type": "card"  },  "receipt_email": null,  "receipt_number": null,  "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xTTJKVGtMa2RJd0h1N2l4KPDLl6UGMgawkab5iK86LBYtkq0XrhiQf1RsA2ubesH4GHiixEU8_1-Wp7h4oQEdfSUGiZpJwtQHBErT",  "refunded": false,  "refunds": {    "object": "list",    "data": [],    "has_more": false,    "total_count": 0,    "url": "/v1/charges/ch_3MmlLrLkdIwHu7ix0snN0B15/refunds"  },  "review": null,  "shipping": null,  "source_transfer": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "succeeded",  "transfer_data": null,  "transfer_group": null}
```

---

## Managed PaymentsPrivate preview

**URL:** https://docs.stripe.com/payments/managed-payments

**Contents:**
- Managed PaymentsPrivate preview
- Sell your digital products globally and let Stripe manage global tax, fraud prevention, dispute management, and customer support for transactions.
    - Private preview
- Sign up
- Eligibility
  - Supported business locations
  - North America
  - Europe
  - Asia
  - Available customer countries

Managed Payments is in private-preview. Sign up for the wait-list

Use Managed Payments to sell digital products such as SaaS, software, and digital content or downloads worldwide. When you use Managed Payments, Stripe acts as your merchant of record. This means Stripe manages the following for you:

Managed Payments has compliance requirements and restrictions in addition to those needed for Stripe Payments.

Your business must be based in one of the following supported countries:

You can sell to customers globally, with the exception of the following restricted countries:

Managed Payments supports the sale of digital products that meet all of the following criteria:

Checkout page compatible with

If you sell physical products, services, or have a business type that’s not supported by Managed Payments, you can integrate with Stripe Payments and Tax to automate tax compliance. Stripe also offers numerous partners to support tax processes.

---
