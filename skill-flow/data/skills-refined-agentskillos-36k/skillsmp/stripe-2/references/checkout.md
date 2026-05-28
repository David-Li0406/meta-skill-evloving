# Stripe - Checkout

**Pages:** 14

---

## Design a payments integration

**URL:** https://docs.stripe.com/payments/use-cases/get-started

**Contents:**
- Design a payments integration
- Learn which payments integration fits your business.
- Explore no-code integrations

Use Stripe to accept payments for your business online and around the world with scalable payments solutions. This guide helps you understand which Stripe payments products and services best fit your business. Explore the differences between Checkout and Elements integrations in our interactive demo.

You have to register for a Stripe account and verify your email before you use any of these products or solutions. After you register, you can access the Dashboard to manage and configure your account and business.

Use Payment Links to accept payments without a website or mobile app. Create a payment link to get started.

Use Checkout to set up a Stripe-hosted page, embed a payments form, or use payments embedded components.

Use Stripe Elements to build a customizable payments form and checkout for your customers.

Use Mobile Elements to accept payments in iOS and Android apps.

Accept payments without building a website or app.

Support and automate your subscribers’ lifecycle.

Create, customize, and send invoices from the Dashboard.

Take payments in person with your iPhone or Android mobile device.

Offer customers a way to pay what they want.

---

## Fulfill orders

**URL:** https://docs.stripe.com/checkout/fulfillment

**Contents:**
- Fulfill orders
- Learn how to fulfill payments received with the Checkout Sessions API.
- Automatic fulfillment
    - Note
- Create a fulfillment functionServer-side
  - Prevent extra fulfillments
    - Note
    - Note
- Create a payment event handlerServer-side
  - Immediate versus delayed payment methods

When you receive a payment with the Checkout Sessions API (including Payment Links), you might need to take action to provide your customer with what they paid for. For example, you might need to grant them access to a service, or you might need to ship them physical goods. This process is known as fulfillment, and you have two ways to handle this process:

The first option works for low volume or experimental ventures, but for most situations we recommend automating fulfillment. The rest of this guide shows you how to build an automatic fulfillment system.

The automatic fulfillment system outlined below uses a combination of webhooks and a redirect to your website to trigger fulfillment. You must use webhooks to make sure fulfillment happens for every payment, and redirects let your customers access services or fulfillment details immediately after paying.

Payment Links use Checkout, so all of the information below applies to both Payment Links and Checkout unless otherwise noted.

Create a function on your server to fulfill successful payments. Webhooks trigger this function, and it’s called when customers are sent to your website after completing checkout. This guide refers to this function as fulfill_checkout, but you can name the function whatever you wish.

Perform fulfillment only once per payment. Because of how this integration and the internet work, your fulfill_checkout function might be called multiple times, possibly concurrently, for the same Checkout Session. Performing checkout only once ensures this won’t cause undesired behavior.

Your fulfill_checkout function must:

Use the code below as a starting point for your fulfill_checkout function. The TODO comments indicate any functionality you must implement.

The code snippets below might name the fulfill_checkout function fulfillCheckout or FulfillCheckout depending on the language selected, but they all represent the same function.

If a Checkout Session has many line items, use auto-pagination with the API for Checkout line items to retrieve all of them.

Depending on the payment methods you accept and your business needs, you might want to have your fulfill_checkout function do the following:

To trigger fulfillment, create a webhook event handler to listen for payment events and trigger your fulfill_checkout function.

When someone pays you, it creates a checkout.session.completed event. Set up an endpoint on your server to accept, process, and confirm receipt of these events.

Some payment methods aren’t instant, such as ACH direct debit and other bank transfers. This means, funds won’t be immediately available when Checkout completes. Delayed payment methods generate a checkout.session.async_payment_succeeded event when payment succeeds later. The status of the object is in processing until the payment status either succeeds or fails.

The webhook secret (whsec_...) shown in the code below comes from either the Stripe CLI or your webhook endpoint. You can use the Stripe CLI for local testing, and Stripe uses a webhook endpoint to send events to your handler when it’s running on a server. See the next section for more details.

You might also want to listen for and handle checkout.session.async_payment_failed events. For example, you can send an email to your customer when a delayed payment fails.

The quickest way to develop and test your webhook event handler is with the Stripe CLI. If you don’t have the Stripe CLI, follow the install guide to get started.

When the Stripe CLI is installed, you can test your event handler locally. Run your server (for example, on localhost:4242), then run the stripe listen command to have the Stripe CLI forward events to your local server:

Add the webhook secret (whsec_...) to your event handling code, then test fulfillment by going through Checkout as a customer:

When the payment completes, verify the following:

After testing locally, get your webhook event handler up and running on your server. Next, create a webhook endpoint to send checkout.session.completed events to your server, then test the Checkout flow again.

Configure Checkout to send your customer to a page on your website after they complete Checkout. Include the {CHECKOUT_SESSION_ID} placeholder in your page’s URL, which is replaced with the Checkout Session ID when your customer is redirected from Checkout.

For Checkout Sessions with the default ui_mode of hosted, set the success_url.

When you have a webhook endpoint set up to listen for checkout.session.completed events and you set a success_url, Checkout waits up to 10 seconds for your server to respond to the webhook event delivery before redirecting your customer. If you use this approach, make sure your server responds to checkout.session.completed events as quickly as possible. If you’re using the Stripe CLI for local testing, Checkout redirects to the success_url immediately.

This behavior isn’t supported for webhook endpoints registered in an organization account. Stripe doesn’t wait for organization webhook endpoints that listen to checkout.session.completed to respond when redirecting Checkout customers.

For Payment Links you create with the API, set the after_completion.redirect.url.

For Payment Links you create in the Dashboard:

Listening to webhooks is required to make sure you always trigger fulfillment for every payment, but webhooks can sometimes be delayed. To optimize your payment flow and guarantee immediate fulfillment when your customer is present, trigger fulfillment from your landing page as well.

Use the Checkout Session ID from the URL you specified in the previous step to do the following:

When you render your landing page you can display the following:

You can’t rely on triggering fulfillment only from your Checkout landing page, because your customers aren’t guaranteed to visit that page. For example, someone can pay successfully in Checkout and then lose their connection to the internet before your landing page loads.

Set up a webhook event handler so Stripe can send payment events directly to your server, bypassing the client entirely. Webhooks provide the most reliable way to confirm when you get paid. If webhook event delivery fails, Stripe retries multiple times.

**Examples:**

Example 1 (python):
```python
def fulfill_checkout(session_id)
  # Set your secret key. Remember to switch to your live secret key in production.
  # See your keys here: https://dashboard.stripe.com/apikeys
  Stripe.api_key = 'sk_test_YOUR_TEST_KEY_HERE'

  puts "Fullfilling Checkout Session #{session_id}"

  # TODO: Make this function safe to run multiple times,
  # even concurrently, with the same session ID

  # TODO: Make sure fulfillment hasn't already been
  # performed for this Checkout Session

  # Retrieve the Checkout Session from the API with line_items expanded
  checkout_session = Stripe::Checkout::Session.retrieve({
    id: session_id,
    expand: ['line_items'],
  })

  # Check the Checkout Session's payment_status property
  # to determine if fulfillment should be performed
  if checkout_session.payment_status != 'unpaid'
    # TODO: Perform fulfillment of the line items

    # TODO: Record/save fulfillment status for this
    # Checkout Session
  end
end
```

Example 2 (python):
```python
def fulfill_checkout(session_id)
  # Set your secret key. Remember to switch to your live secret key in production.
  # See your keys here: https://dashboard.stripe.com/apikeys
  Stripe.api_key = 'sk_test_YOUR_TEST_KEY_HERE'

  puts "Fullfilling Checkout Session #{session_id}"

  # TODO: Make this function safe to run multiple times,
  # even concurrently, with the same session ID

  # TODO: Make sure fulfillment hasn't already been
  # performed for this Checkout Session

  # Retrieve the Checkout Session from the API with line_items expanded
  checkout_session = Stripe::Checkout::Session.retrieve({
    id: session_id,
    expand: ['line_items'],
  })

  # Check the Checkout Session's payment_status property
  # to determine if fulfillment should be performed
  if checkout_session.payment_status != 'unpaid'
    # TODO: Perform fulfillment of the line items

    # TODO: Record/save fulfillment status for this
    # Checkout Session
  end
end
```

Example 3 (javascript):
```javascript
require 'sinatra'

# Use the secret provided by Stripe CLI for local testing
# or your webhook endpoint's secret.
endpoint_secret = 'whsec_...'

post '/webhook' do
  event = nil

  # Verify webhook signature and extract the event
  # See https://stripe.com/docs/webhooks#verify-events for more information.
  begin
    sig_header = request.env['HTTP_STRIPE_SIGNATURE']
    payload = request.body.read
    event = Stripe::Webhook.construct_event(payload, sig_header, endpoint_secret)
  rescue JSON::ParserError => e
    # Invalid payload
    return status 400
  rescue Stripe::SignatureVerificationError => e
    # Invalid signature
    return status 400
  end

  if event['type'] == 'checkout.session.completed' ||
  event['type'] == 'checkout.session.async_payment_succeeded'
    fulfill_checkout(event['data']['object']['id'])
  end

  status 200
end
```

Example 4 (javascript):
```javascript
require 'sinatra'

# Use the secret provided by Stripe CLI for local testing
# or your webhook endpoint's secret.
endpoint_secret = 'whsec_...'

post '/webhook' do
  event = nil

  # Verify webhook signature and extract the event
  # See https://stripe.com/docs/webhooks#verify-events for more information.
  begin
    sig_header = request.env['HTTP_STRIPE_SIGNATURE']
    payload = request.body.read
    event = Stripe::Webhook.construct_event(payload, sig_header, endpoint_secret)
  rescue JSON::ParserError => e
    # Invalid payload
    return status 400
  rescue Stripe::SignatureVerificationError => e
    # Invalid signature
    return status 400
  end

  if event['type'] == 'checkout.session.completed' ||
  event['type'] == 'checkout.session.async_payment_succeeded'
    fulfill_checkout(event['data']['object']['id'])
  end

  status 200
end
```

---

## Stripe Android SDK

**URL:** https://docs.stripe.com/sdks/android

**Contents:**
- Stripe Android SDK
- Build a payment experience in your Android mobile app.
- See also

The Stripe Android SDK allows you to quickly build a payment flow in your Android app. We provide powerful and customizable UI elements that you can use out-of-the-box to collect your users’ payment details. We also expose the low-level APIs that underpin those UIs so that you can build fully custom experiences.

Integrate Stripe’s prebuilt PaymentSheet UI into the checkout of your Android app.

Build a custom payment UI using PaymentSheet FlowController.

Use the basic card field in your own payment UI.

Autofill your customers’ billing and shipping addresses quickly and accurately.

Customize the look and feel of PaymentSheet to match the design of your app.

Present a prebuilt UI for managing a customer’s saved payment methods.

Add a separate Google Pay button to the checkout of your app.

---

## Checkout Sessions

**URL:** https://docs.stripe.com/api/checkout/sessions

**Contents:**
- Checkout Sessions
- The Checkout Session object
  - Attributes
    - idstring
    - automatic_taxobject
    - client_reference_idnullable string
    - currencynullable enum
    - customernullable stringExpandable
    - customer_emailnullable string
    - line_itemsnullable objectExpandable

A Checkout Session represents your customer’s session as they pay for one-time purchases or subscriptions through Checkout or Payment Links. We recommend creating a new Session each time your customer attempts to pay.

Once payment is successful, the Checkout Session will contain a reference to the Customer, and either the successful PaymentIntent or an active Subscription.

You can create a Checkout Session on your server and redirect to its URL to begin Checkout.

Related guide: Checkout quickstart

Unique identifier for the object.

Details on the state of automatic tax for the session, including the status of the latest tax calculation.

A unique string to reference the Checkout Session. This can be a customer ID, a cart ID, or similar, and can be used to reconcile the Session with your internal systems.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

The ID of the customer for this Session. For Checkout Sessions in subscription mode or Checkout Sessions with customer_creation set as always in payment mode, Checkout will create a new customer object based on information provided during the payment flow unless an existing customer was provided when the Session was created.

If provided, this value will be used when the Customer object is created. If not provided, customers will be asked to enter their email address. Use this parameter to prefill customer data if you already have an email on file. To access information about the customer once the payment flow is complete, use the customer attribute.

The line items purchased by the customer.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The mode of the Checkout Session.

Accept one-time payments for cards, iDEAL, and more.

Save payment details to charge your customers later.

Use Stripe Billing to set up fixed-price subscriptions.

The ID of the PaymentIntent for Checkout Sessions in payment mode. You can’t confirm or cancel the PaymentIntent for a Checkout Session. To cancel, expire the Checkout Session instead.

The payment status of the Checkout Session, one of paid, unpaid, or no_payment_required. You can use this value to decide when to fulfill your customer’s order.

The payment is delayed to a future date, or the Checkout Session is in setup mode and doesn’t require a payment at this time.

The payment funds are available in your account.

The payment funds are not yet available in your account.

Applies to Checkout Sessions with ui_mode: embedded or ui_mode: custom. The URL to redirect your customer back to after they authenticate or cancel their payment on the payment method’s app or site.

The status of the Checkout Session, one of open, complete, or expired.

The checkout session is complete. Payment processing may still be in progress

The checkout session has expired. No further processing will occur

The checkout session is still in progress. Payment processing has not started

The URL the customer will be directed to after the payment or subscription creation is successful.

The UI mode of the Session. Defaults to hosted.

The Checkout Session will be displayed using embedded components on your website

The Checkout Session will be displayed as an embedded form on your website.

The Checkout Session will be displayed on a hosted page that customers will be redirected to.

The URL to the Checkout Session. Applies to Checkout Sessions with ui_mode: hosted. Redirect customers to this URL to take them to Checkout. If you’re using Custom Domains, the URL will use your subdomain. Otherwise, it’ll use checkout.stripe.com. This value is only present when the session is active.

Creates a Checkout Session object.

Settings for automatic tax lookup for this session and resulting payments, invoices, and subscriptions.

A unique string to reference the Checkout Session. This can be a customer ID, a cart ID, or similar, and can be used to reconcile the session with your internal systems.

The maximum length is 200 characters.

ID of an existing Customer, if one exists. In payment mode, the customer’s most recently saved card payment method will be used to prefill the email, name, card details, and billing address on the Checkout page. In subscription mode, the customer’s default payment method will be used if it’s a card, otherwise the most recently saved card will be used. A valid billing address, billing name and billing email are required on the payment method for Checkout to prefill the customer’s card details.

If the Customer already has a valid email set, the email will be prefilled and not editable in Checkout. If the Customer does not have a valid email, Checkout will set the email entered during the session on the Customer.

If blank for Checkout Sessions in subscription mode or with customer_creation set as always in payment mode, Checkout will create a new Customer object based on information provided during the payment flow.

You can set payment_intent_data.setup_future_usage to have Checkout automatically attach the payment method to the Customer you pass in for future reuse.

If provided, this value will be used when the Customer object is created. If not provided, customers will be asked to enter their email address. Use this parameter to prefill customer data if you already have an email on file. To access information about the customer once a session is complete, use the customer field.

The maximum length is 800 characters.

A list of items the customer is purchasing. Use this parameter to pass one-time or recurring Prices. The parameter is required for payment and subscription mode.

For payment mode, there is a maximum of 100 line items, however it is recommended to consolidate line items if there are more than a few dozen.

For subscription mode, there is a maximum of 20 line items with recurring Prices and 20 line items with one-time Prices. Line items with one-time Prices will be on the initial invoice only.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The mode of the Checkout Session. Pass subscription if the Checkout Session includes at least one recurring item.

Accept one-time payments for cards, iDEAL, and more.

Save payment details to charge your customers later.

Use Stripe Billing to set up fixed-price subscriptions.

The URL to redirect your customer back to after they authenticate or cancel their payment on the payment method’s app or site. This parameter is required if ui_mode is embedded or custom and redirect-based payment methods are enabled on the session.

The URL to which Stripe should send customers when payment or setup is complete. This parameter is not allowed if ui_mode is embedded or custom. If you’d like to use information from the successful Checkout Session on your page, read the guide on customizing your success page.

The UI mode of the Session. Defaults to hosted.

The Checkout Session will be displayed using embedded components on your website

The Checkout Session will be displayed as an embedded form on your website.

The Checkout Session will be displayed on a hosted page that customers will be redirected to.

Returns a Checkout Session object.

Updates a Checkout Session object.

Related guide: Dynamically update Checkout

A list of items the customer is purchasing.

When updating line items, you must retransmit the entire array of line items.

To retain an existing line item, specify its id.

To update an existing line item, specify its id along with the new values of the fields to update.

To add a new line item, specify one of price or price_data and quantity.

To remove an existing line item, omit the line item’s ID from the retransmitted array.

To reorder a line item, specify it at the desired position in the retransmitted array.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a Checkout Session object.

Retrieves a Checkout Session object.

Returns a Checkout Session object.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "cs_test_a11YYufWQzNY63zpQ6QSNRQhkUpVph4WRmzW0zWJO2znZKdVujZ0N0S22u",  "object": "checkout.session",  "after_expiration": null,  "allow_promotion_codes": null,  "amount_subtotal": 2198,  "amount_total": 2198,  "automatic_tax": {    "enabled": false,    "liability": null,    "status": null  },  "billing_address_collection": null,  "cancel_url": null,  "client_reference_id": null,  "consent": null,  "consent_collection": null,  "created": 1679600215,  "currency": "usd",  "custom_fields": [],  "custom_text": {    "shipping_address": null,    "submit": null  },  "customer": null,  "customer_creation": "if_required",  "customer_details": null,  "customer_email": null,  "expires_at": 1679686615,  "invoice": null,  "invoice_creation": {    "enabled": false,    "invoice_data": {      "account_tax_ids": null,      "custom_fields": null,      "description": null,      "footer": null,      "issuer": null,      "metadata": {},      "rendering_options": null    }  },  "livemode": false,  "locale": null,  "metadata": {},  "mode": "payment",  "payment_intent": null,  "payment_link": null,  "payment_method_collection": "always",  "payment_method_options": {},  "payment_method_types": [    "card"  ],  "payment_status": "unpaid",  "phone_number_collection": {    "enabled": false  },  "recovered_from": null,  "setup_intent": null,  "shipping_address_collection": null,  "shipping_cost": null,  "shipping_details": null,  "shipping_options": [],  "status": "open",  "submit_type": null,  "subscription": null,  "success_url": "https://example.com/success",  "total_details": {    "amount_discount": 0,    "amount_shipping": 0,    "amount_tax": 0  },  "url": "https://checkout.stripe.com/c/pay/cs_test_a11YYufWQzNY63zpQ6QSNRQhkUpVph4WRmzW0zWJO2znZKdVujZ0N0S22u#fidkdWxOYHwnPyd1blpxYHZxWjA0SDdPUW5JbmFMck1wMmx9N2BLZjFEfGRUNWhqTmJ%2FM2F8bUA2SDRySkFdUV81T1BSV0YxcWJcTUJcYW5rSzN3dzBLPUE0TzRKTTxzNFBjPWZEX1NKSkxpNTVjRjN8VHE0YicpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl"}
```

Example 2 (unknown):
```unknown
{  "id": "cs_test_a11YYufWQzNY63zpQ6QSNRQhkUpVph4WRmzW0zWJO2znZKdVujZ0N0S22u",  "object": "checkout.session",  "after_expiration": null,  "allow_promotion_codes": null,  "amount_subtotal": 2198,  "amount_total": 2198,  "automatic_tax": {    "enabled": false,    "liability": null,    "status": null  },  "billing_address_collection": null,  "cancel_url": null,  "client_reference_id": null,  "consent": null,  "consent_collection": null,  "created": 1679600215,  "currency": "usd",  "custom_fields": [],  "custom_text": {    "shipping_address": null,    "submit": null  },  "customer": null,  "customer_creation": "if_required",  "customer_details": null,  "customer_email": null,  "expires_at": 1679686615,  "invoice": null,  "invoice_creation": {    "enabled": false,    "invoice_data": {      "account_tax_ids": null,      "custom_fields": null,      "description": null,      "footer": null,      "issuer": null,      "metadata": {},      "rendering_options": null    }  },  "livemode": false,  "locale": null,  "metadata": {},  "mode": "payment",  "payment_intent": null,  "payment_link": null,  "payment_method_collection": "always",  "payment_method_options": {},  "payment_method_types": [    "card"  ],  "payment_status": "unpaid",  "phone_number_collection": {    "enabled": false  },  "recovered_from": null,  "setup_intent": null,  "shipping_address_collection": null,  "shipping_cost": null,  "shipping_details": null,  "shipping_options": [],  "status": "open",  "submit_type": null,  "subscription": null,  "success_url": "https://example.com/success",  "total_details": {    "amount_discount": 0,    "amount_shipping": 0,    "amount_tax": 0  },  "url": "https://checkout.stripe.com/c/pay/cs_test_a11YYufWQzNY63zpQ6QSNRQhkUpVph4WRmzW0zWJO2znZKdVujZ0N0S22u#fidkdWxOYHwnPyd1blpxYHZxWjA0SDdPUW5JbmFMck1wMmx9N2BLZjFEfGRUNWhqTmJ%2FM2F8bUA2SDRySkFdUV81T1BSV0YxcWJcTUJcYW5rSzN3dzBLPUE0TzRKTTxzNFBjPWZEX1NKSkxpNTVjRjN8VHE0YicpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/checkout/sessions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  --data-urlencode success_url="https://example.com/success" \  -d "line_items[0][price]"=price_1MotwRLkdIwHu7ixYcPLm5uZ \  -d "line_items[0][quantity]"=2 \  -d mode=payment
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/checkout/sessions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  --data-urlencode success_url="https://example.com/success" \  -d "line_items[0][price]"=price_1MotwRLkdIwHu7ixYcPLm5uZ \  -d "line_items[0][quantity]"=2 \  -d mode=payment
```

---

## Stripe React Native SDK

**URL:** https://docs.stripe.com/sdks/react-native

**Contents:**
- Stripe React Native SDK
- Build payments into your React Native mobile app.
- See also

The Stripe React Native SDK allows you to build payments into your native Android and iOS apps using React Native. We provide powerful and customizable UI screens and elements that you can use out-of-the-box to collect your users’ payment details.

Integrate the Stripe prebuilt PaymentSheet UI into the checkout of your React Native app.

Complete the payment in your own UI using PaymentSheet.

Use the basic card field in your own payment UI.

Autofill the billing and shipping addresses of your customers quickly and accurately.

Customize the look and feel of PaymentSheet to match the design of your app.

Present a prebuilt UI for managing a customer’s saved payment methods.

Add a separate Apple Pay button to the checkout of your app.

Add a separate Google Pay button to the checkout of your app.

---

## Faster checkout with Link

**URL:** https://docs.stripe.com/payments/link

**Contents:**
- Faster checkout with Link
- Let your customers check out faster with Link.
    - Country availability
- Link authentication
- Link on no-code options
- Link with Elements
- Link integrations
- See also

Link allows your customers to select a saved payment method at checkout instead of entering payment information. Your customers can save their credit cards, debit cards, or US bank accounts for faster checkout at any Link-enabled business. Link also lets you accept Instant Bank Payments. All Link transactions confirm immediately, and successful payments settle to your Stripe balance on the same timeline as card payments, regardless of the payment method that funds the payment.

Customers can make changes to their account, view their purchase history, or reach out to the Link customer support team by visiting link.com. For information about how your payment integration affects Link, see Link in different payment integrations.

Link isn’t available in India. In Brazil and Thailand, the Payment Element doesn’t support Link.

Add Link to your prebuilt checkout page

Here’s how Link authenticates existing customers:

After a customer enrolls with Link, they can add backup payment methods and change shipping addresses.

Link works with Checkout, Payment Links, Web Elements, Mobile Elements, and Invoicing. To accept payments using Link, go to your payment method settings.

Use Link in your prebuilt checkout page, allowing your customers to securely save and reuse their payment information.

Enable Link in the Hosted Invoice Page.

Enable Klarna on Link as a payment method for your customers. Public preview

Trigger Link in the Payment Element whenever a customer selects a supported payment method.

Display Link alongside Apple Pay, Google Pay, and PayPal using the Express Checkout Element.

Add Link to your native iOS, Android, and React Native apps.

Learn about using Link with dynamic payment methods and other integrations.

Use the Payment Intents API with the Link Authentication Element or Payment Element to create a Link-enabled custom checkout page.

Save your Link customers’ details and charge them later.

---

## Stripe Web Elements

**URL:** https://docs.stripe.com/payments/elements

**Contents:**
- Stripe Web Elements
- Create your own checkout flows with prebuilt UI components.
- Get started
- Compatible APIs

Stripe Elements is a set of prebuilt UI components for building your web checkout flow. It’s available as a feature of Stripe.js, our foundational JavaScript library for building payment flows. Stripe.js tokenizes sensitive payment details within an Element without ever having them touch your server.

Global payment methods: Access to over 100 global payment methods, including wallets like Apple Pay.

Link: Help your customers check out faster by letting them select a saved payment method at checkout instead of entering payment information.

Saved payment methods: Save, reuse, and manage cards and bank accounts with built-in features.

Compliance: Stripe provides a globally compliant interface and handles requirements for displaying mandates and consent notices to buyers.

Up-to-date forms: Localized forms with built-in error handling. Stripe keeps each payment method provider’s requirements up to date.

Address collection: Collect full or partial billing addresses with any payment method.

Appearance customization: Customize the look and feel of Elements to match the design of your site.

Other features: Additional features like CVC recollection and control over which card brands you accept.

If you don’t see your Element below, find more in the Stripe.js API Reference.

Stripe offers two core payments APIs compatible with Elements that give you the flexibility to accept various types of payments from your customers. You can integrate these APIs into Stripe’s prebuilt payment interfaces. The APIs serve different use cases depending on how you choose to structure your checkout flow and how much control you require. For most use cases, we recommend using Checkout Sessions.

Use the Checkout Sessions API to model your customer’s complete checkout flow, including the line items in their purchase, billing and shipping addresses, applicable tax rates, and coupons or discounts. The Checkout Session allows you to create subscriptions, calculate tax rates with Stripe Tax, and initiate payments using a single integration.

Build a checkout page with the Checkout Sessions API.

Use the Payment Intents API to model just the payments step with more granular control. Unlike the Checkout Sessions API, which requires line item details, you only pass in the final amount you want to charge. This is suitable for advanced payment flows where you want to manually compute the final amount. When using Payment Intents, you must build separate integrations with the Stripe Tax API if you want to use Stripe to calculate applicable taxes or with the Subscriptions API if you want to use Stripe to create subscriptions.

Build an advanced integration with the Payment Intents API.

---

## Accept a payment

**URL:** https://docs.stripe.com/payments/accept-a-payment?ui=elements

**Contents:**
- Accept a payment
- Securely accept payments online.
  - Integration effort
  - Integration type
  - UI customization
    - Interested in using Stripe Tax, discounts, shipping, or currency conversion?
- Set up StripeServer-side
- Create a PaymentIntentServer-side
    - Note
  - Create the PaymentIntent

Build a payment form or use a prebuilt checkout page to start accepting online payments.

Build a custom payments integration by embedding UI components on your site, using Stripe Elements. See how this integration compares to Stripe’s other integration types.

The client-side and server-side code builds a checkout form that accepts various payment methods.

Combine UI components into a custom payment flow

CSS-level customization with the Appearance API

Stripe has a Payment Element integration that manages tax, discounts, shipping, and currency conversion for you. See build a checkout page to learn more.

First, create a Stripe account or sign in.

Use our official libraries to access the Stripe API from your application:

If you want to render the Payment Element without first creating a PaymentIntent, see Collect payment details before creating an Intent.

The PaymentIntent object represents your intent to collect payment from a customer and tracks charge attempts and state changes throughout the payment process.

Create a PaymentIntent on your server with an amount and currency. In the latest version of the API, specifying the automatic_payment_methods parameter is optional because Stripe enables its functionality by default. You can manage payment methods from the Dashboard. Stripe handles the return of eligible payment methods based on factors such as the transaction’s amount, currency, and payment flow.

Stripe uses your payment methods settings to display the payment methods you have enabled. To see how your payment methods appear to customers, enter a transaction ID or set an order amount and currency in the Dashboard. To override payment methods, manually list any that you want to enable using the payment_method_types attribute.

Always decide how much to charge on the server side, a trusted environment, as opposed to the client. This prevents malicious customers from being able to choose their own prices.

The PaymentIntent includes a client secret that the client side uses to securely complete the payment process. You can use different approaches to pass the client secret to the client side.

Retrieve the client secret from an endpoint on your server, using the browser’s fetch function. This approach is best if your client side is a single-page application, particularly one built with a modern frontend framework like React. Create the server endpoint that serves the client secret:

And then fetch the client secret with JavaScript on the client side:

Collect payment details on the client with the Payment Element. The Payment Element is a prebuilt UI component that simplifies collecting payment details for a variety of payment methods.

The Payment Element contains an iframe that securely sends payment information to Stripe over an HTTPS connection. Avoid placing the Payment Element within another iframe because some payment methods require redirecting to another page for payment confirmation.

If you do choose to use an iframe and want to accept Apple Pay or Google Pay, the iframe must have the allow attribute set to equal "payment *".

The checkout page address must start with https:// rather than http:// for your integration to work. You can test your integration without using HTTPS, but remember to enable it when you’re ready to accept live payments.

The Payment Element is automatically available as a feature of Stripe.js. Include the Stripe.js script on your checkout page by adding it to the head of your HTML file. Always load Stripe.js directly from js.stripe.com to remain PCI compliant. Don’t include the script in a bundle or host a copy of it yourself.

Create an instance of Stripe with the following JavaScript on your checkout page:

The Payment Element needs a place to live on your payment page. Create an empty DOM node (container) with a unique ID in your payment form:

When the previous form loads, create an instance of the Payment Element and mount it to the container DOM node. Pass the client secret from the previous step into options when you create the Elements instance:

Handle the client secret carefully because it can complete the charge. Don’t log it, embed it in URLs, or expose it to anyone but the customer.

Stripe Elements is a collection of drop-in UI components. To further customize your form or collect different customer information, browse the Elements docs.

The Payment Element renders a dynamic form that allows your customer to pick a payment method. For each payment method, the form automatically asks the customer to fill in all necessary payment details.

Customize the Payment Element to match the design of your site by passing the appearance object into options when creating the Elements provider.

By default, the Payment Element only collects the necessary billing address details. Some behavior, such as calculating tax or entering shipping details, requires your customer’s full address. You can:

If you’ve configured your integration to accept Apple Pay payments, we recommend configuring the Apple Pay interface to return a merchant token to enable merchant initiated transactions (MIT). Request the relevant merchant token type in the Payment Element.

Use stripe.confirmPayment to complete the payment using details from the Payment Element. Provide a return_url to this function to indicate where Stripe should redirect the user after they complete the payment. Your user may be first redirected to an intermediate site, like a bank authorization page, before being redirected to the return_url. Card payments immediately redirect to the return_url when a payment is successful.

If you don’t want to redirect for card payments after payment completion, you can set redirect to if_required. This only redirects customers that check out with redirect-based payment methods.

Make sure the return_url corresponds to a page on your website that provides the status of the payment. When Stripe redirects the customer to the return_url, we provide the following URL query parameters:

If you have tooling that tracks the customer’s browser session, you might need to add the stripe.com domain to the referrer exclude list. Redirects cause some tools to create new sessions, which prevents you from tracking the complete session.

Use one of the query parameters to retrieve the PaymentIntent. Inspect the status of the PaymentIntent to decide what to show your customers. You can also append your own query parameters when providing the return_url, which persist through the redirect process.

Stripe sends a payment_intent.succeeded event when the payment completes. Use the Dashboard webhook tool or follow the webhook guide to receive these events and run actions, such as sending an order confirmation email to your customer, logging the sale in a database, or starting a shipping workflow.

Listen for these events rather than waiting on a callback from the client. On the client, the customer could close the browser window or quit the app before the callback executes, and malicious clients could manipulate the response. Setting up your integration to listen for asynchronous events is what enables you to accept different types of payment methods with a single integration.

In addition to handling the payment_intent.succeeded event, we recommend handling these other events when collecting payments with the Payment Element:

To test your custom payments integration:

Learn more about testing your integration.

See Testing for additional information to test your integration.

Stripe collects information on customer interactions with Elements to provide services to you, prevent fraud, and improve its services. This includes using cookies and IP addresses to identify which Elements a customer saw during a single checkout session. You’re responsible for disclosing and obtaining all rights and consents necessary for Stripe to use data in these ways. For more information, visit our privacy center.

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

## Use a prebuilt Stripe-hosted payment page

**URL:** https://docs.stripe.com/payments/checkout

**Contents:**
- Use a prebuilt Stripe-hosted payment page
- Payment UIs
- Customize checkout
- Change when and how you collect payment
- Manage your business
- Sample projects

Checkout is a low-code, prebuilt payment page that Stripe hosts or that you can embed into your website. Checkout uses the Checkout Sessions API.

Accept one-time and subscription payments from more than 40 local payment methods.

You can use two different payment UIs with the Checkout Sessions API. The following images highlight which aspects of the checkout UI Stripe hosts in each option. You can also see these options by exploring our demo.

Stripe-hosted page Customers enter their payment details in a Stripe-hosted payment page, then return to your site after payment completion.

Embedded form Customers enter their payment details in an embedded payment form on your site without redirection.

1Limited customization provides 20 preset fonts, 3 preset border radius options, logo and background customization, and custom button color.

Customize the appearance and behavior of the checkout flow.

Collect shipping details and other customer information during checkout.

Collect taxes for one-time payments in Stripe Checkout.

Make updates while your customer checks out.

Add promotions, such as trials, discounts, and optional items.

Create a subscription with recurring payments for your customers.

Save your customers’ payment details to charge them later.

Accept a payment and save your customer’s payment details for future purchases.

Use Adaptive Pricing to allow customers to pay in their local currency.

Handle your inventory and fulfillment with Checkout.

Migrate the management of your payment methods to the Dashboard.

Customize the post-payment checkout process.

---

## Accept payments online without writing code

**URL:** https://docs.stripe.com/payment-links

**Contents:**
- Accept payments online without writing code
- Create a payment link and share it on social media, in emails, or on your website.
- Features and availability
- Get started
- Additional no-code capabilities
- Compare Invoicing and Payment Links

Allow your customers to pay from any channel, in their local language and currency, with their preferred payment method.

If you don’t have a Stripe account, sign up to create a payment link.

Preferred language rendering

Local currency with Adaptive Pricing

1Limited customization provides 20 preset fonts, 3 preset border radius options, and custom logo, background, and button colors.

Create a custom payment page without code.

Share payment links across social media, emails, or your website.

Use URL parameters and UTM codes to track a payment link.

Use Payment Links to create an embeddable buy button for your website.

Collect additional information, taxes, or update your branding.

Collect addresses and phone numbers without writing code.

Create different shipping rates for your customers.

Add promotion codes, upsells, and optional items to offer discounts.

Track payments, manage fulfillment automatically, and view metrics.

Create and manage payment links with the API.

Invoicing and Payment Links are two ways you can start using Stripe to accept payments without writing any code. Use the following table to compare the two products and to understand which works best for your use case.

1 Use the editable template to incorporate your own icons, brand colors, payment terms, page sizes, as well as memo and footer fields.2 With limited customization, you can access 20 preset fonts, three predefined border radiuses, and options for adjusting your logo, background, product images, and the color of your own button.3 Dynamic payment methods filter for eligibility, displaying the most relevant payment methods to maximize conversion. Payment method availability varies by product.4 Learn how to customize invoices for global compliance.

---

## Stripe iOS SDK

**URL:** https://docs.stripe.com/sdks/ios

**Contents:**
- Stripe iOS SDK
- Build payments into your iOS mobile app.
- See also

The Stripe iOS SDK allows you to accept payments into your iOS app using Swift or Objective-C. You can use our UI screens, elements, and low-level APIs to build fully custom payment forms and collect your customer’s payment details.

Integrate the Stripe prebuilt PaymentSheet UI into the checkout of your iOS app.

Build a custom payment UI using PaymentSheet FlowController.

Use the basic card field in your own payment UI.

Autofill the billing and shipping addresses of your customers quickly and accurately.

Customize the look and feel of PaymentSheet to match the design of your app.

Present a prebuilt UI for managing a customer’s saved payment methods.

Add a separate Apple Pay button to the checkout of your app.

---

## Create an embeddable buy button

**URL:** https://docs.stripe.com/payment-links/buy-button

**Contents:**
- Create an embeddable buy button
- Use Payment Links to create an embeddable buy button for your website.
- Customize the button
- Embed the button
    - Caution
- Attributes to customize checkout
    - Compare Customers v1 and Accounts v2 references
- Pass an existing customer
- Content Security Policy
- Limitations

Create an embeddable buy button to sell a product, subscription, or accept a payment on your website. Start by selecting an existing link from the Payment Links list view or by creating a new link where you can decide which products to sell and customize the checkout UI. After you create your link, click Buy button to configure the buy button design and generate the code that you can copy and paste into your website.

By default, your buy button uses the same branding and call to action configured for your payment link. You can:

Customize the buy button

Stripe provides an embed code composed of a <script> tag and a <stripe-buy-button> web component. Click Copy code to copy the code and paste it into your website.

If you’re using HTML, paste the embed code into the HTML. If you’re using React, include the script tag in your index.html page to mount the <stripe-buy-button> component.

The buy button uses your account’s publishable API key. If you revoke the API key, you need to update the embed code with your new publishable API key.

If your Connect platform uses customer-configured Accounts, use our guide to replace Customer and event references in your code with the equivalent Accounts v2 API references.

You can provide an existing Customer object to Checkout Sessions created from the buy button. Create a CustomerSession for a customer you’ve already authenticated server-side, and return the client_secret to the client.

Set the customer-session-client-secret attribute on the <stripe-buy-button> web component to the client_secret from the Customer Session.

You must provide the client_secret within 30 minutes. After providing the client secret, you have an additional 30 minutes until the Customer Session expires. Any resulting Checkout Sessions created from the buy button will fail. Don’t cache the client secret, instead generate a new one every time you render each buy button.

If you’ve deployed a Content Security Policy, the policy directives that the buy button requires are:

Rendering the buy button requires a website domain. To test the buy button locally, run a local HTTP server to host your website’s index.html file over the localhost domain. To run a local HTTP server, use Python’s SimpleHTTPServer or the http-server npm module.

After your customer makes a payment using a payment link, you can see it in the payments overview in the Dashboard.

If you’re new to Stripe, you’ll receive an email after your first payment. To receive emails for all successful payments, update your notification preferences in your Personal details settings.

Stripe creates a new guest customer for one-time payments and a new Customer object when selling a subscription or saving a payment method for future use.

Learn more about handling payment links post-payment, like how to configure post-payment behavior for a buy button or payment link.

**Examples:**

Example 1 (unknown):
```unknown
<body>
  <h1>Purchase your new kit</h1>
  <!-- Paste your embed code script here. -->
  <script
    async
    src="https://js.stripe.com/v3/buy-button.js">
  </script>
  <stripe-buy-button
    buy-button-id="{{BUY_BUTTON_ID}}"
    publishable-key="pk_test_TYooMQauvdEDq54NiTphI7jx"
  >
  </stripe-buy-button>
</body>
```

Example 2 (unknown):
```unknown
<body>
  <h1>Purchase your new kit</h1>
  <!-- Paste your embed code script here. -->
  <script
    async
    src="https://js.stripe.com/v3/buy-button.js">
  </script>
  <stripe-buy-button
    buy-button-id="{{BUY_BUTTON_ID}}"
    publishable-key="pk_test_TYooMQauvdEDq54NiTphI7jx"
  >
  </stripe-buy-button>
</body>
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/customer_sessions \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d customer="{{CUSTOMER_ID}}" \
  -d "components[buy_button][enabled]"=true
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/customer_sessions \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d customer="{{CUSTOMER_ID}}" \
  -d "components[buy_button][enabled]"=true
```

---

## Embeddable pricing table for subscriptions

**URL:** https://docs.stripe.com/payments/checkout/pricing-table

**Contents:**
- Embeddable pricing table for subscriptions
- Display a subscription pricing table on your website and take customers directly to Stripe Checkout.
- Create a pricing table
    - Confirm maximum quantity
- Embed a pricing table
    - Caution
- Customize a pricing table
  - Add product marketing features Optional
  - Add a custom call-to-action Optional
  - Add custom fields Optional

You can use the Stripe Dashboard to create an embeddable pricing table to:

The diagram below summarizes how the customer goes from viewing a pricing table to completing checkout.

If you have tiered pricing that supports quantities greater than the default maximum of 99, check the Let customers adjust quantity property and increase the Max value accordingly. Tiered pricing options for quantities above the maximum don’t appear in the selector.

After creating a pricing table, Stripe automatically returns an embed code composed of a <script> tag and a <stripe-pricing-table> web component. Click the Copy code button to copy the code and paste it into your website.

If you’re using HTML, paste the embed code into the HTML. If you’re using React, include the script tag in your index.html page to mount the <stripe-pricing-table> component.

The pricing table uses your account’s publishable API key. If you revoke the API key, you need to update the embed code with your new publishable API key.

Optionally, you can customize your pricing table.

The pricing table can display your products’ marketing features to help your customers decide what to purchase. To add marketing features to a product in your pricing table, go to Additional options > Feature list.

You can also add marketing features when creating or updating products with the API.

The pricing table allows you to configure a product with a custom call-to-action that redirects to any URL. You can use this if you have custom pricing or a high-touch sales process for one of your products. You can only set one product to have a custom call-to-action button.

Click Add product with custom call-to-action button to choose a product and a custom call-to-action, and to set the correct URL.

Custom call-to-action supports these formats:

You can add custom fields on each of your products and prices in your pricing table to collect additional information from your customers. The information is available after the payment is complete and is useful for fulfilling the purchase.

Don’t use custom fields to collect personal, protected, or sensitive data, or information restricted by law.

You can add the following types of fields:

After your customer completes the payment, you can view the fields on the payment details page in the Dashboard.

The custom fields are also sent in the checkout.session.completed event after payment completion. Register an event destination to receive the event at your endpoint.

Automatically display prices in your pricing table or checkout flow in your customers’ local currency by configuring multi-currency prices. Use the customer-email attribute to test how your pricing table and payment page appear to customers in different countries.

In the stripe-pricing-table, set the customer_email property and include a suffix of the form +location_XX in the local part of the email. XX must be a valid two-letter ISO country code.

When you view the pricing table, the currency matches the default currency of the country you specify in the customer_email (in this case, France).

After a successful payment, your customer sees a localized confirmation message thanking them for their purchase. You can customize the confirmation message or redirect to a URL of your choice. To change the confirmation behavior on a pricing table, click the Confirmation page section when creating or updating the pricing table.

If you redirect your customers to your own confirmation page, you can include {CHECKOUT_SESSION_ID} in the redirect URL to dynamically pass the customer’s current Checkout Session ID. This can be helpful if you want to tailor the success message on your website based on the information in the Checkout Session.

To offer a free trial for a price, select Include a free trial and set the length of the trial when you create or edit a pricing table. After customers confirm their payment details, they’re redirected to a page where they can start their trial. The new page is part of a Checkout Session.

To allow customers to sign up for a subscription without providing their payment method details, select Include a free trial, then click Continue. Next, select Only collect payment method information if required.

Make sure to set up email reminders to collect payment method information from customers before their trial ends. Otherwise, Stripe pauses the trial.

If your Connect platform uses customer-configured Accounts, use our guide to replace Customer and event references in your code with the equivalent Accounts v2 API references.

The <stripe-pricing-table> web component supports setting the customer-email property. When the property is set, the pricing table passes it to the Checkout Session’s customer_email attribute, automatically entering the email address on the payment page.

If your Connect platform uses customer-configured Accounts, use our guide to replace Customer and event references in your code with the equivalent Accounts v2 API references.

You can provide an existing Customer object to Checkout Sessions created from the pricing table. Create a customer session for a user you’ve already authenticated server-side and return the client_secret to the client.

Set the customer-session-client-secret attribute on the <stripe-pricing-table> web component to the client_secret from the Customer Session.

You have 30 minutes to include the client secret in the pricing table. After rendering the pricing table, you have an additional 30 minutes to complete a payment before the customer session expires. If you create a Checkout Session with an expired customer session, we discard the client secret and create the Checkout Session with no associated customer.

If the customer session expires after Checkout Session creation, but before confirmation, payment confirmation fails.

You can update a pricing table from its details page in the Dashboard. On the Product catalog page, select the Pricing tables tab, then find and select the pricing table you want to edit.

On the pricing table details page, click Edit pricing table. You can change which products and prices you display and configure the payment page settings. When you save your changes, Stripe automatically updates the pricing table UI.

When a customer purchases a subscription, you’ll see it on the subscriptions page in the Dashboard.

The pricing table component uses Stripe Checkout to render a prebuilt, hosted payment page. When a payment is completed using Checkout, Stripe sends the checkout.session.completed event. Register an event destination to receive the event at your endpoint to process fulfillment and reconciliation. See the Checkout fulfillment guide for more details.

The <stripe-pricing-table> web component supports setting the client-reference-id property. When the property is set, the pricing table passes it to the Checkout Session’s client_reference_id attribute to help you reconcile the Checkout Session with your internal system. This can be an authenticated user ID or a similar string. client-reference-id can be composed of alphanumeric characters, dashes, or underscores, and be any value up to 200 characters. Invalid values are silently dropped and your pricing table will continue to work as expected.

Since the pricing table is embedded on your website and is accessible to anyone, check that client-reference-id doesn’t include sensitive information or secrets, such as passwords or API keys.

You can redirect customers that already have a subscription to the customer portal or your website to manage their subscription. Learn more about limiting customers to one subscription.

Share a link to your customer portal, where customers can log in with their email to manage subscriptions, update payment methods, and so on. Learn how to create and share your customer portal link.

If you’ve deployed a Content Security Policy, the policy directives that pricing table requires are:

**Examples:**

Example 1 (unknown):
```unknown
<body>
  <h1>We offer plans that help any business!</h1>
  <!-- Paste your embed code script here. -->
  <script
    async
    src="https://js.stripe.com/v3/pricing-table.js">
  </script>
  <stripe-pricing-table
    pricing-table-id="{{PRICING_TABLE_ID}}"
    publishable-key="pk_test_TYooMQauvdEDq54NiTphI7jx"
  >
  </stripe-pricing-table>
</body>
```

Example 2 (unknown):
```unknown
<body>
  <h1>We offer plans that help any business!</h1>
  <!-- Paste your embed code script here. -->
  <script
    async
    src="https://js.stripe.com/v3/pricing-table.js">
  </script>
  <stripe-pricing-table
    pricing-table-id="{{PRICING_TABLE_ID}}"
    publishable-key="pk_test_TYooMQauvdEDq54NiTphI7jx"
  >
  </stripe-pricing-table>
</body>
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/products \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d name=Professional \
  -d "marketing_features[0][name]"="Unlimited boards" \
  -d "marketing_features[1][name]"="Up to 20 seats"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/products \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d name=Professional \
  -d "marketing_features[0][name]"="Unlimited boards" \
  -d "marketing_features[1][name]"="Up to 20 seats"
```

---

## Register domains for payment methods

**URL:** https://docs.stripe.com/payments/payment-methods/pmd-registration

**Contents:**
- Register domains for payment methods
- Register domains to use payment methods (including Link, Apple Pay, and Google Pay) in Elements or Checkout's embeddable payment form.
    - Apple Pay and merchant validation
- Testing
    - Using Connect
- Register your domain
  - Using an iframe
- Manage your domain
- Register your domain while using Connect

For certain payment methods, you must register every web domain that shows the payment method if your integration uses Elements or Checkout’s embeddable payment form. This includes registering top-level domains and subdomains. For example, if you have the domain example.com and subdomains like shop.example.com and www.example.com, this guide explains how to register them.

After you register a domain, that domain is ready for use with other payment methods that you might enable in the future.

Register your domains for the following payment methods:

The Apple Pay documentation describes their process of “merchant validation," which Stripe handles for you behind the scenes. You don’t need to create an Apple Merchant ID or CSR. Instead, follow the steps in this guide.

You also need to register domains for testing. When testing locally, you can use a tool such as ngrok to get an HTTPS domain. You can either register in a sandbox, or register in live mode and the domain will also be registered in sandboxes automatically. Remember to register your domains in live mode before going live.

You can create and manage domains in the Dashboard on the Payment method domains page for use in production and testing.

Connect platforms that create direct charges must use the API to manage domains for their connected accounts, not the Stripe Dashboard.

To register a domain:

After completing these steps, your domain shows up on the Payment method domains page.

You can see a list of all of your domains in the Dashboard.

To disable a domain, click the row action and then click Disable. If a domain is disabled, the payment methods no longer appear in Elements or Checkout’s embeddable payment form on that domain.

To enable a disabled domain, click the row action and then click Enable.

Connect platforms must register all domains where Elements or Checkout’s embeddable payment form displays the payment methods listed above. The domain where the charge is being run needs to be registered for the user running the charge.

If the platform creates direct charges, use your platform’s secret key to authenticate the request and set the Stripe-Account header to your connected account’s Stripe ID.

If the platform creates destination charges or separate charges and transfers, use your platform’s secret key to authenticate the request and omit the Stripe-Account header.

Learn more about Making API calls for connected accounts.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_method_domains \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -H "Stripe-Account: {{CONNECTED_ACCOUNT_ID}}" \
  -d domain_name="example.com"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_method_domains \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -H "Stripe-Account: {{CONNECTED_ACCOUNT_ID}}" \
  -d domain_name="example.com"
```

---
