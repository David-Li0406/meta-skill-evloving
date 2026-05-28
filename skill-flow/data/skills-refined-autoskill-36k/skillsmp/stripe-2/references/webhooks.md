# Stripe - Webhooks

**Pages:** 20

---

## Receive Stripe events in your webhook endpoint

**URL:** https://docs.stripe.com/webhooks

**Contents:**
- Receive Stripe events in your webhook endpoint
- Listen for events from Stripe on your webhook endpoint so your integration can automatically trigger reactions.
    - Send events to your AWS account
- Get started
- Unsupported event type behaviors for organization event destinations
- Create a handler
    - Note
    - Example endpoint
    - Using context
- Test your handler

You can now send events directly to Amazon EventBridge as an event destination.

Create an event destination to receive events at an HTTPS webhook endpoint. After you register a webhook endpoint, Stripe can push real-time event data to your application’s webhook endpoint when events happen in your Stripe account. Stripe uses HTTPS to send webhook events to your app as a JSON payload that includes an Event object.

Receiving webhook events helps you respond to asynchronous events, such as when a customer’s bank confirms a payment, a customer disputes a charge, or a recurring payment succeeds.

To start receiving webhook events in your app:

You can register and create one endpoint to handle several different event types at the same time, or set up individual endpoints for specific events.

Stripe sends most event types asynchronously, but waits for a response for some event types. In these cases, Stripe behaves differently based on whether or not the event destination responds.

If your event destination receives Organization events, those requiring a response have the following limitations:

Set up an HTTP or HTTPS endpoint function that can accept webhook requests with a POST method. If you’re still developing your endpoint function on your local machine, it can use HTTP. After it’s publicly accessible, your webhook endpoint function must use HTTPS.

Set up your endpoint function so that it:

This code snippet is a webhook function configured to check for received events from a Stripe account, handle the events, and return a 200 responses. Reference the snapshot event handler when you use API v1 resources, and reference the thin event handler when you use API v2 resources.

When you create a snapshot event handler, use the API object definition at the time of the event for your logic by accessing the event’s data.object fields. You can also retrieve the API resource from the Stripe API to access the latest and up-to-date object definition.

This code snippet is a webhook function configured to check for received events, detect the originating account if applicable, handle the event, and return a 200 response.

Before you go-live with your webhook endpoint function, we recommend that you test your application integration. You can do so by configuring a local listener to send events to your local machine, and sending test events. You need to use the CLI to test.

To forward events to your local endpoint, run the following command with the CLI to set up a local listener. The --forward-to flag sends all Stripe events in a sandbox to your local webhook endpoint. Use the appropriate CLI commands below depending on whether you use thin or snapshot events.

Use the following command to forward snapshot events to your local listener.

You can also run stripe listen to see events in Stripe Shell, although you won’t be able to forward events from the shell to your local endpoint.

Useful configurations to help you test with your local listener include the following:

Use the following command to forward target snapshot events to your local listener.

Use the following command to forward snapshot events from a public webhook endpoint to your local listener.

To send test events, trigger an event type that your event destination is subscribed to by manually creating an object in the Stripe Dashboard. Learn how to trigger events with Stripe for VS Code.

You can use the following command in either Stripe Shell or Stripe CLI. This example triggers a payment_intent.succeeded event:

After testing your webhook endpoint function, use the API or the Webhooks tab in Workbench to register your webhook endpoint’s accessible URL so Stripe knows where to deliver events. You can register up to 16 webhook endpoints with Stripe. Registered webhook endpoints must be publicly accessible HTTPS URLs.

The URL format to register a webhook endpoint is:

For example, if your domain is https://mycompanysite.com and the route to your webhook endpoint is @app.route('/stripe_webhooks', methods=['POST']), specify https://mycompanysite.com/stripe_webhooks as the Endpoint URL.

Create an event destination using Workbench in the Dashboard or programmatically with the API. You can register up to 16 event destinations on each Stripe account.

To create a new webhook endpoint in the Dashboard:

If you create a webhook endpoint in an organization account, select Accounts to listen to events from accounts in your organization. If you have Connect platforms as members of your organizations and want to listen to events from the all the platforms’ connected accounts, select Connected accounts.

Workbench replaces the existing Developers Dashboard. If you’re still using the Developers Dashboard, see how to create a new webhook endpoint.

After confirming that your endpoint works as expected, secure it by implementing webhook best practices.

Secure your integration by making sure your handler verifies that all webhook requests are generated by Stripe. You can verify webhook signatures using our official libraries or verify them manually.

We recommend using our official libraries to verify signatures. You perform the verification by providing the event payload, the Stripe-Signature header, and the endpoint’s secret. If verification fails, you get an error.

If you get a signature verification error, read our guide about troubleshooting it.

Stripe requires the raw body of the request to perform signature verification. If you’re using a framework, make sure it doesn’t manipulate the raw body. Any manipulation to the raw body of the request causes the verification to fail.

Multiple types of issues can occur when delivering events to your webhook endpoint:

To view event deliveries, select the webhook endpoint under Webhooks, then select the Events tab. The Events tab provides a list of events and whether they’re Delivered, Pending, or Failed. Click an event to view metadata, including the HTTP status code of the delivery attempt and the time of pending future deliveries.

You can also use the Stripe CLI to listen for events directly in your terminal.

When an event displays a status code of 200, it indicates successful delivery to the webhook endpoint. You might also receive a status code other than 200. View the table below for a list of common HTTP status codes and recommended solutions.

This section helps you understand different behaviors to expect regarding how Stripe sends events to your webhook endpoint.

Stripe attempts to deliver events to your destination for up to three days with an exponential back off in live mode. View when the next retry will occur, if applicable, in your event destination’s Event deliveries tab. We retry event deliveries created in a sandbox three times over the course of a few hours. If your destination has been disabled or deleted when we attempt a retry, we prevent future retries of that event. However, if you disable and then re-enable the event destination before we’re able to retry, you still see future retry attempts.

There are two ways to manually retry events:

Manually resending an event that had previous delivery failures to a webhook endpoint doesn’t dismiss Stripe’s automatic retry behavior. Automatic retries still happen until you respond to one of them with a 2xx status code.

Stripe doesn’t guarantee the delivery of events in the order that they’re generated. For example, creating a subscription might generate the following events:

Make sure that your event destination isn’t dependent on receiving events in a specific order. Be prepared to manage their delivery appropriately. You can also use the API to retrieve any missing objects. For example, you can retrieve the invoice, charge, and subscription objects with the information from invoice.paid if you receive this event first.

The API version in your account settings when the event occurs dictates the API version, and therefore the structure of an Event sent to your destination. For example, if your account is set to an older API version, such as 2015-02-16, and you change the API version for a specific request with versioning, the Event object generated and sent to your destination is still based on the 2015-02-16 API version. You can’t change Event objects after creation. For example, if you update a charge, the original charge event remains unchanged. As a result, subsequent updates to your account’s API version don’t retroactively alter existing Event objects. Retrieving an older Event by calling /v1/events using a newer API version also has no impact on the structure of the received event. You can set test event destinations to either your default API version or the latest API version. The Event sent to the destination is structured for the event destination’s specified version.

Review these best practices to make sure your webhook endpoints remain secure and function well with your integration.

Webhook endpoints might occasionally receive the same event more than once. You can guard against duplicated event receipts by logging the event IDs you’ve processed, and then not processing already-logged events.

In some cases, two separate Event objects are generated and sent. To identify these duplicates, use the ID of the object in data.object along with the event.type.

Configure your webhook endpoints to receive only the types of events required by your integration. Listening for extra events (or all events) puts undue strain on your server and we don’t recommend it.

You can change the events that a webhook endpoint receives in the Dashboard or with the API.

Configure your handler to process incoming events with an asynchronous queue. You might encounter scalability issues if you choose to process events synchronously. Any large spike in webhook deliveries (for example, during the beginning of the month when all subscriptions renew) might overwhelm your endpoint hosts.

Asynchronous queues allow you to process the concurrent events at a rate your system can support.

If you’re using Rails, Django, or another web framework, your site might automatically check that every POST request contains a CSRF token. This is an important security feature that helps protect you and your users from cross-site request forgery attempts. However, this security measure might also prevent your site from processing legitimate events. If so, you might need to exempt the webhooks route from CSRF protection.

If you use an HTTPS URL for your webhook endpoint (required in live mode), Stripe validates that the connection to your server is secure before sending your webhook data. For this to work, your server must be correctly configured to support HTTPS with a valid server certificate. Stripe webhooks support only TLS versions v1.2 and v1.3.

The secret used for verifying that events come from Stripe is modifiable in the Webhooks tab in Workbench. To keep them safe, we recommend that you roll (change) secrets periodically, or when you suspect a compromised secret.

Stripe sends webhook events from a set list of IP addresses. Only trust events coming from these IP addresses.

Also verify webhook signatures to confirm that Stripe sent the received events. Stripe signs webhook events it sends to your endpoints by including a signature in each event’s Stripe-Signature header. This allows you to verify that the events were sent by Stripe, not by a third party. You can verify signatures either using our official libraries, or verify manually using your own solution.

The following section describes how to verify webhook signatures:

Use Workbench and go to the Webhooks tab to view all your endpoints. Select an endpoint that you want to obtain the secret for, then click Click to reveal.

Stripe generates a unique secret key for each endpoint. If you use the same endpoint for both test and live API keys, the secret is different for each one. Additionally, if you use multiple endpoints, you must obtain a secret for each one you want to verify signatures on. After this setup, Stripe starts to sign each webhook it sends to the endpoint.

A replay attack is when an attacker intercepts a valid payload and its signature, then re-transmits them. To mitigate such attacks, Stripe includes a timestamp in the Stripe-Signature header. Because this timestamp is part of the signed payload, it’s also verified by the signature, so an attacker can’t change the timestamp without invalidating the signature. If the signature is valid but the timestamp is too old, you can have your application reject the payload.

Our libraries have a default tolerance of 5 minutes between the timestamp and the current time. You can change this tolerance by providing an additional parameter when verifying signatures. Use Network Time Protocol (NTP) to make sure that your server’s clock is accurate and synchronizes with the time on Stripe’s servers.

Don’t use a tolerance value of 0. Using a tolerance value of 0 disables the recency check entirely.

Stripe generates the timestamp and signature each time we send an event to your endpoint. If Stripe retries an event (for example, your endpoint previously replied with a non-2xx status code), then we generate a new signature and timestamp for the new delivery attempt.

Your endpoint must quickly return a successful status code (2xx) prior to any complex logic that could cause a timeout. For example, you must return a 200 response before updating a customer’s invoice as paid in your accounting system.

**Examples:**

Example 1 (javascript):
```javascript
require 'json'

# Replace this endpoint secret with your unique endpoint secret key
# If you're testing with the CLI, run 'stripe listen' to find the secret key
# If you defined your endpoint using the API or the Dashboard, check your webhook settings for your endpoint secret: https://dashboard.stripe.com/webhooks
endpoint_secret = 'whsec_...';

# Using Sinatra
post '/webhook' do
  payload = request.body.read
  event = nil

  begin
    event = Stripe::Event.construct_from(
      JSON.parse(payload, symbolize_names: true)
    )
  rescue JSON::ParserError => e
    # Invalid payload
    status 400
    return
  end

  # Check that you have configured webhook signing
  if endpoint_secret
    # Retrieve the event by verifying the signature using the raw body and the endpoint secret
    signature = request.env['HTTP_STRIPE_SIGNATURE'];
    begin
      event = Stripe::Webhook.construct_event(
        payload, signature, endpoint_secret
      )
    rescue Stripe::SignatureVerificationError => e
      puts "⚠️  Webhook signature verification failed. #{e.message}"
      status 400
    end
  end

  # Handle the event
  case event.type
  when 'payment_intent.succeeded'
    payment_intent = event.data.object # contains a Stripe::PaymentIntent
    # Then define and call a method to handle the successful payment intent.
    # handle_payment_intent_succeeded(payment_intent)
  when 'payment_method.attached'
    payment_method = event.data.object # contains a Stripe::PaymentMethod
    # Then define and call a method to handle the successful attachment of a PaymentMethod.
    # handle_payment_method_attached(payment_method)
  # ... handle other event types
  else
    puts "Unhandled event type: #{event.type}"
  end

  status 200
end
```

Example 2 (javascript):
```javascript
require 'json'

# Replace this endpoint secret with your unique endpoint secret key
# If you're testing with the CLI, run 'stripe listen' to find the secret key
# If you defined your endpoint using the API or the Dashboard, check your webhook settings for your endpoint secret: https://dashboard.stripe.com/webhooks
endpoint_secret = 'whsec_...';

# Using Sinatra
post '/webhook' do
  payload = request.body.read
  event = nil

  begin
    event = Stripe::Event.construct_from(
      JSON.parse(payload, symbolize_names: true)
    )
  rescue JSON::ParserError => e
    # Invalid payload
    status 400
    return
  end

  # Check that you have configured webhook signing
  if endpoint_secret
    # Retrieve the event by verifying the signature using the raw body and the endpoint secret
    signature = request.env['HTTP_STRIPE_SIGNATURE'];
    begin
      event = Stripe::Webhook.construct_event(
        payload, signature, endpoint_secret
      )
    rescue Stripe::SignatureVerificationError => e
      puts "⚠️  Webhook signature verification failed. #{e.message}"
      status 400
    end
  end

  # Handle the event
  case event.type
  when 'payment_intent.succeeded'
    payment_intent = event.data.object # contains a Stripe::PaymentIntent
    # Then define and call a method to handle the successful payment intent.
    # handle_payment_intent_succeeded(payment_intent)
  when 'payment_method.attached'
    payment_method = event.data.object # contains a Stripe::PaymentMethod
    # Then define and call a method to handle the successful attachment of a PaymentMethod.
    # handle_payment_method_attached(payment_method)
  # ... handle other event types
  else
    puts "Unhandled event type: #{event.type}"
  end

  status 200
end
```

Example 3 (javascript):
```javascript
require 'json'

# Using Sinatra
post '/webhook' do
  payload = request.body.read
  event = nil

  begin
    event = Stripe::Event.construct_from(
      JSON.parse(payload, symbolize_names: true)
    )
  rescue JSON::ParserError => e
    # Invalid payload
    status 400
    return
  end

  # Extract the context
  context = event.context

  # Define your API key variables (ideally loaded securely)
  ACCOUNT_123_API_KEY = "sk_test_123"
  ACCOUNT_456_API_KEY = "sk_test_456"

  account_api_keys = {
    "account_123" => ACCOUNT_123_API_KEY,
    "account_456" => ACCOUNT_456_API_KEY
  }

  api_key = account_api_keys[context]

  if api_key.nil?
    puts "No API key found for context: #{context}"
    status 400
    return
  end

  # Handle the event
  case event.type
  when 'customer.created'
    customer = event.data.object

    begin
      latest_customer = Stripe::Customer.retrieve(
        customer.id,
        { api_key: api_key }
      )
      handle_customer_created(latest_customer, context)
    rescue => e
      puts "Error retrieving customer: #{e.message}"
      status 500
      return
    end

  when 'payment_method.attached'
    payment_method = event.data.object

    begin
      latest_payment_method = Stripe::PaymentMethod.retrieve(
        payment_method.id,
        { api_key: api_key }
      )
      handle_payment_method_attached(latest_payment_method, context)
    rescue => e
      puts "Error retrieving payment method: #{e.message}"
      status 500
      return
    end

  else
    puts "Unhandled event type: #{event.type}"
  end

  status 200
end
```

Example 4 (javascript):
```javascript
require 'json'

# Using Sinatra
post '/webhook' do
  payload = request.body.read
  event = nil

  begin
    event = Stripe::Event.construct_from(
      JSON.parse(payload, symbolize_names: true)
    )
  rescue JSON::ParserError => e
    # Invalid payload
    status 400
    return
  end

  # Extract the context
  context = event.context

  # Define your API key variables (ideally loaded securely)
  ACCOUNT_123_API_KEY = "sk_test_123"
  ACCOUNT_456_API_KEY = "sk_test_456"

  account_api_keys = {
    "account_123" => ACCOUNT_123_API_KEY,
    "account_456" => ACCOUNT_456_API_KEY
  }

  api_key = account_api_keys[context]

  if api_key.nil?
    puts "No API key found for context: #{context}"
    status 400
    return
  end

  # Handle the event
  case event.type
  when 'customer.created'
    customer = event.data.object

    begin
      latest_customer = Stripe::Customer.retrieve(
        customer.id,
        { api_key: api_key }
      )
      handle_customer_created(latest_customer, context)
    rescue => e
      puts "Error retrieving customer: #{e.message}"
      status 500
      return
    end

  when 'payment_method.attached'
    payment_method = event.data.object

    begin
      latest_payment_method = Stripe::PaymentMethod.retrieve(
        payment_method.id,
        { api_key: api_key }
      )
      handle_payment_method_attached(latest_payment_method, context)
    rescue => e
      puts "Error retrieving payment method: #{e.message}"
      status 500
      return
    end

  else
    puts "Unhandled event type: #{event.type}"
  end

  status 200
end
```

---

## Types of events

**URL:** https://docs.stripe.com/api/events/types

**Contents:**
- Types of events
  - Event types
    - account.application.authorizeddata.object is an application
    - account.application.deauthorizeddata.object is an application
    - account.external_account.createddata.object is an external account (e.g., card or bank account)
    - account.external_account.deleteddata.object is an external account (e.g., card or bank account)
    - account.external_account.updateddata.object is an external account (e.g., card or bank account)
    - account.updateddata.object is an account
    - application_fee.createddata.object is an application fee
    - application_fee.refund.updateddata.object is a fee refund

This is a list of all public snapshot events we currently send for /v1 resources, which is continually evolving and expanding.

Stripe events use the resource.event naming convention. Events that occur on subresources like customer.subscription.updated don’t trigger a corresponding event for the parent resource (customer.updated).

Stripe creates event types marked as Selection required only when at least one webhook is listening for it. A webhook set to listen to all events doesn’t satisfy this requirement and won’t generate Selection required event types.

Occurs whenever a user authorizes an application. Sent to the related application only.

Occurs whenever a user deauthorizes an application. Sent to the related application only.

Occurs whenever an external account is created.

Occurs whenever an external account is deleted.

Occurs whenever an external account is updated.

Occurs whenever an account status or property has changed.

Occurs whenever an application fee is created on a charge.

Occurs whenever an application fee refund is updated.

Occurs whenever an application fee is refunded, whether from refunding a charge or from refunding the application fee directly. This includes partial refunds.

Occurs whenever a balance settings status or property has changed.

Occurs whenever your Stripe balance has been updated (e.g., when a charge is available to be paid out). By default, Stripe automatically transfers funds in your balance to your bank account on a daily basis. This event is not fired for negative transactions.

Occurs whenever a portal configuration is created.

Occurs whenever a portal configuration is updated.

Occurs whenever a portal session is created.

Occurs whenever your custom alert threshold is met.

Occurs when a credit balance transaction is created

Occurs when a credit grant is created

Occurs when a credit grant is updated

Occurs when a meter is created

Occurs when a meter is deactivated

Occurs when a meter is reactivated

Occurs when a meter is updated

Occurs whenever a capability has new requirements or a new status.

Occurs whenever there is a positive remaining cash balance after Stripe automatically reconciles new funds into the cash balance. If you enabled manual reconciliation, this webhook will fire whenever there are new funds into the cash balance.

Occurs whenever a previously uncaptured charge is captured.

Occurs when a dispute is closed and the dispute status changes to lost, warning_closed, or won.

Occurs whenever a customer disputes a charge with their bank.

Occurs when funds are reinstated to your account after a dispute is closed. This includes partially refunded payments.

Occurs when funds are removed from your account due to a dispute.

Occurs when the dispute is updated (usually with evidence).

Occurs whenever an uncaptured charge expires.

Occurs whenever a failed charge attempt occurs.

Occurs whenever a pending charge is created.

Occurs whenever a refund is updated on selected payment methods. For updates on all refunds, listen to refund.updated instead.

Occurs whenever a charge is refunded, including partial refunds. Listen to refund.created for information about the refund.

Occurs whenever a charge is successful.

Occurs whenever a charge description or metadata is updated, or upon an asynchronous capture.

Occurs when a payment intent using a delayed payment method fails.

Occurs when a payment intent using a delayed payment method finally succeeds.

Occurs when a Checkout Session has been successfully completed.

Occurs when a Checkout Session is expired.

Occurs when a Climate order is canceled.

Occurs when a Climate order is created.

Occurs when a Climate order is delayed.

Occurs when a Climate order is delivered.

Occurs when a Climate order’s product is substituted for another.

Occurs when a Climate product is created.

Occurs when a Climate product is updated.

Occurs whenever a coupon is created.

Occurs whenever a coupon is deleted.

Occurs whenever a coupon is updated.

Occurs whenever a credit note is created.

Occurs whenever a credit note is updated.

Occurs whenever a credit note is voided.

Occurs whenever a new customer cash balance transactions is created.

Occurs whenever a new customer is created.

Occurs whenever a customer is deleted.

Occurs whenever a coupon is attached to a customer.

Occurs whenever a coupon is removed from a customer.

Occurs whenever a customer is switched from one coupon to another.

Occurs whenever a new source is created for a customer.

Occurs whenever a source is removed from a customer.

Occurs whenever a card or source will expire at the end of the month. This event only works with legacy integrations using Card or Source objects. If you use the PaymentMethod API, this event won’t occur.

Occurs whenever a source’s details are changed.

Occurs whenever a customer is signed up for a new plan.

Occurs whenever a customer’s subscription ends.

Occurs whenever a customer’s subscription is paused. Only applies when subscriptions enter status=paused, not when payment collection is paused.

Occurs whenever a customer’s subscription’s pending update is applied, and the subscription is updated.

Occurs whenever a customer’s subscription’s pending update expires before the related invoice is paid.

Occurs whenever a customer’s subscription is no longer paused. Only applies when a status=paused subscription is resumed, not when payment collection is resumed.

Occurs three days before a subscription’s trial period is scheduled to end, or when a trial is ended immediately (using trial_end=now).

Occurs whenever a subscription changes (e.g., switching from one plan to another, or changing the status from trial to active).

Occurs whenever a tax ID is created for a customer.

Occurs whenever a tax ID is deleted from a customer.

Occurs whenever a customer’s tax ID is updated.

Occurs whenever any property of a customer changes.

Occurs whenever a customer’s entitlements change.

Occurs whenever a new Stripe-generated file is available for your account.

Occurs when a Financial Connections account’s account numbers are updated.

Occurs when a new Financial Connections account is created.

Occurs when a Financial Connections account’s status is updated from active to inactive.

Occurs when a Financial Connections account is disconnected.

Occurs when a Financial Connections account’s status is updated from inactive to active.

Occurs when an Account’s balance_refresh status transitions from pending to either succeeded or failed.

Occurs when an Account’s ownership_refresh status transitions from pending to either succeeded or failed.

Occurs when an Account’s transaction_refresh status transitions from pending to either succeeded or failed.

Occurs when an Account’s tokenized account number is about to expire.

Occurs whenever a VerificationSession is canceled

Occurs whenever a VerificationSession is created

Occurs whenever a VerificationSession transitions to processing

Occurs whenever a VerificationSession is redacted.

Occurs whenever a VerificationSession transitions to require user input

Occurs whenever a VerificationSession transitions to verified

Occurs when an InvoicePayment is successfully paid.

Occurs whenever a new invoice is created. To learn how webhooks can be used with this event, and how they can affect it, see Using Webhooks with Subscriptions.

Occurs whenever a draft invoice is deleted. Note: This event is not sent for invoice previews.

Occurs whenever a draft invoice cannot be finalized. See the invoice’s last finalization error for details.

Occurs whenever a draft invoice is finalized and updated to be an open invoice.

Occurs whenever an invoice is marked uncollectible.

Occurs X number of days after an invoice becomes due—where X is determined by Automations

Occurs when an invoice transitions to paid with a non-zero amount_overpaid.

Occurs whenever an invoice payment attempt succeeds or an invoice is marked as paid out-of-band.

Occurs whenever an invoice payment attempt requires further user action to complete.

Occurs when an invoice requires a payment using a payment method that cannot be processed by Stripe.

Occurs whenever an invoice payment attempt fails, due to either a declined payment, including soft decline, or to the lack of a stored payment method.

Occurs whenever an invoice payment attempt succeeds.

Occurs whenever an invoice email is sent out.

Occurs X number of days before a subscription is scheduled to create an invoice that is automatically charged—where X is determined by your subscriptions settings. Note: The received Invoice object will not have an invoice ID.

Occurs whenever an invoice changes (e.g., the invoice amount).

Occurs whenever an invoice is voided.

Occurs X number of days before an invoice becomes due—where X is determined by Automations

Occurs whenever an invoice item is created.

Occurs whenever an invoice item is deleted.

Occurs whenever an authorization is created.

Represents a synchronous request for authorization, see Using your integration to handle authorization requests.

Occurs whenever an authorization is updated.

Occurs whenever a card is created.

Occurs whenever a card is updated.

Occurs whenever a cardholder is created.

Occurs whenever a cardholder is updated.

Occurs whenever a dispute is won, lost or expired.

Occurs whenever a dispute is created.

Occurs whenever funds are reinstated to your account for an Issuing dispute.

Occurs whenever funds are deducted from your account for an Issuing dispute.

Occurs whenever a dispute is submitted.

Occurs whenever a dispute is updated.

Occurs whenever a personalization design is activated following the activation of the physical bundle that belongs to it.

Occurs whenever a personalization design is deactivated following the deactivation of the physical bundle that belongs to it.

Occurs whenever a personalization design is rejected by design review.

Occurs whenever a personalization design is updated.

Occurs whenever an issuing digital wallet token is created.

Occurs whenever an issuing digital wallet token is updated.

Occurs whenever an issuing transaction is created.

Occurs whenever an issuing transaction is updated with receipt data.

Occurs whenever an issuing transaction is updated.

Occurs whenever a Mandate is updated.

Occurs when a PaymentIntent has funds to be captured. Check the amount_capturable property on the PaymentIntent to determine the amount that can be captured. You may capture the PaymentIntent with an amount_to_capture value up to the specified amount. Learn more about capturing PaymentIntents.

Occurs when a PaymentIntent is canceled.

Occurs when a new PaymentIntent is created.

Occurs when funds are applied to a customer_balance PaymentIntent and the ‘amount_remaining’ changes.

Occurs when a PaymentIntent has failed the attempt to create a payment method or a payment.

Occurs when a PaymentIntent has started processing.

Occurs when a PaymentIntent transitions to requires_action state

Occurs when a PaymentIntent has successfully completed payment.

Occurs when a payment link is created.

Occurs when a payment link is updated.

Occurs whenever a new payment method is attached to a customer.

Occurs whenever a payment method’s details are automatically updated by the network.

Occurs whenever a payment method is detached from a customer.

Occurs whenever a payment method is updated via the PaymentMethod update API.

Occurs whenever a payout is canceled.

Occurs whenever a payout is created.

Occurs whenever a payout attempt fails.

Occurs whenever a payout is expected to be available in the destination account. If the payout fails, a payout.failed notification is also sent, at a later time.

Occurs whenever balance transactions paid out in an automatic payout can be queried.

Occurs whenever a payout is updated.

Occurs whenever a person associated with an account is created.

Occurs whenever a person associated with an account is deleted.

Occurs whenever a person associated with an account is updated.

Occurs whenever a plan is created.

Occurs whenever a plan is deleted.

Occurs whenever a plan is updated.

Occurs whenever a price is created.

Occurs whenever a price is deleted.

Occurs whenever a price is updated.

Occurs whenever a product is created.

Occurs whenever a product is deleted.

Occurs whenever a product is updated.

Occurs whenever a promotion code is created.

Occurs whenever a promotion code is updated.

Occurs whenever a quote is accepted.

Occurs whenever a quote is canceled.

Occurs whenever a quote is created.

Occurs whenever a quote is finalized.

Occurs X number of days before a quote is scheduled to expire—where X is determined by Automations

Occurs whenever an early fraud warning is created.

Occurs whenever an early fraud warning is updated.

Occurs whenever a refund is created.

Occurs whenever a refund has failed.

Occurs whenever a refund is updated.

Occurs whenever a requested ReportRun failed to complete.

Occurs whenever a requested ReportRun completed successfully.

Occurs whenever a ReportType is updated (typically to indicate that a new day’s data has come available).

Occurs whenever a review is closed. The review’s reason field indicates why: approved, disputed, refunded, refunded_as_fraud, or canceled.

Occurs whenever a review is opened.

Occurs when a SetupIntent is canceled.

Occurs when a new SetupIntent is created.

Occurs when a SetupIntent is in requires_action state.

Occurs when a SetupIntent has failed the attempt to setup a payment method.

Occurs when an SetupIntent has successfully setup a payment method.

Occurs whenever a Sigma scheduled query run finishes.

Occurs whenever a source is canceled.

Occurs whenever a source transitions to chargeable.

Occurs whenever a source fails.

Occurs whenever a source mandate notification method is set to manual.

Occurs whenever the refund attributes are required on a receiver source to process a refund or a mispayment.

Occurs whenever a source transaction is created.

Occurs whenever a source transaction is updated.

Occurs whenever a subscription schedule is canceled due to the underlying subscription being canceled because of delinquency.

Occurs whenever a subscription schedule is canceled.

Occurs whenever a new subscription schedule is completed.

Occurs whenever a new subscription schedule is created.

Occurs 7 days before a subscription schedule will expire.

Occurs whenever a new subscription schedule is released.

Occurs whenever a subscription schedule is updated.

Occurs whenever a new tax rate is created.

Occurs whenever a tax rate is updated.

Occurs whenever tax settings is updated.

Occurs whenever an action sent to a Terminal reader failed.

Occurs whenever an action sent to a Terminal reader was successful.

Occurs whenever an action sent to a Terminal reader is updated.

Occurs whenever a test clock starts advancing.

Occurs whenever a test clock is created.

Occurs whenever a test clock is deleted.

Occurs whenever a test clock fails to advance its frozen time.

Occurs whenever a test clock transitions to a ready status.

Occurs whenever a top-up is canceled.

Occurs whenever a top-up is created.

Occurs whenever a top-up fails.

Occurs whenever a top-up is reversed.

Occurs whenever a top-up succeeds.

Occurs whenever a transfer is created.

Occurs whenever a transfer is reversed, including partial reversals.

Occurs whenever a transfer’s description or metadata is updated.

---

## Migrate from snapshot events to thin events

**URL:** https://docs.stripe.com/webhooks/migrate-snapshot-to-thin-events

**Contents:**
- Migrate from snapshot events to thin events
- Learn how to migrate to thin events without disrupting production.
    - Private preview
- Thin versions of snapshot events
- Before you begin
    - Warning
- Phased migration strategy
- Add a thin webhook route
    - Note
- Create a thin event destination

Thin events for API v1 resources are available in private preview. Previously, thin events only supported API v2 resources. Learn more and request access.

Thin events provide a lightweight, version-stable alternative to snapshot events. Instead of receiving full resource objects in webhook payloads, you receive compact notifications and fetch the details you need. This eliminates the need to update webhook handlers when upgrading API versions.

Use this guide to migrate from snapshot events to thin events without disrupting production. The migration uses a dual-destination strategy where both handlers run in parallel during the transition. For a complete overview of thin events, including benefits and use cases, see Thin events.

To help with migration, Stripe creates thin event versions of your existing snapshot events. For example, customer.created has a thin version v1.customer.created. During migration, when a single action triggers both events, the thin version includes a snapshot_event field containing the original snapshot event ID. Use this as your idempotency key to prevent duplicate processing when running both handlers simultaneously.

Complete this entire migration process in a sandbox or test mode before attempting it in live mode.

The migration consists of the following phases:

This strategy ensures you don’t have any downtime and gives you multiple opportunities to validate and revert it if needed.

Create a new endpoint in your application specifically for thin events. Start with a minimal implementation that only verifies signatures and returns a 200 status code.

To access the snapshot_event field, configure your Stripe SDK to use a preview API version:

Stable API versions (.clover) don’t include private preview features like snapshot_event.

Deploy this change and verify that the endpoint is accessible.

In the Stripe Dashboard or API, create a new event destination configured for thin events.

Store the new webhook signing secret separately from your snapshot webhook secret. Label them clearly (for example, SNAPSHOT_WEBHOOK_SECRET and THIN_WEBHOOK_SECRET) to avoid mixing them up.

At this point, both destinations are active and delivering events to your application.

Update your thin webhook handler to fetch event details and related objects—but don’t write to your database yet. Instead, log what actions you would take so you can monitor that your thin handler behaves the same as your snapshot handler.

Add these components to your handler from step 1:

Run shadow mode for at least 24-48 hours and monitor:

If your thin handler’s shadow logs diverge from what the snapshot handler actually does, investigate and fix the discrepancy now (while there’s no production impact).

For interop events, the snapshot_event field contains the original snapshot event ID. Log both the thin event.id and event.snapshot_event to correlate events across both handlers during the transition.

When shadow mode runs cleanly, enable real writes in your thin handler. Keep both destinations active during a brief overlap window to make sure you don’t miss any events.

During the overlap, you might receive the same logical event twice: once as a snapshot event and once as a thin event. Use idempotency keys to prevent duplicate processing.

The snapshot_event field in thin interop events contains the original snapshot event ID. By using this field as your idempotency key, both handlers can deduplicate against the same key.

First, set up an idempotency database table:

Next, implement the idempotency helper:

Update both handlers to use this pattern. First, the snapshot handler:

Next, the thin handler:

How this prevents duplicates:

When a customer is created, Stripe generates both events:

Both handlers receive events simultaneously:

Both handlers try to insert the same key:

Result: The customer is created.

With both handlers writing to your database:

If anything looks wrong, disable writes in the thin handler and investigate. Your snapshot handler remains your point of reference until you’re confident in the thin path.

Keep the overlap window short (a few hours to a day at most). This limits the period during which you process events twice, and it simplifies troubleshooting if issues arise.

After the thin handler processes events reliably for a comfortable period of time, you can retire the snapshot destination.

This stops Stripe from sending events to your snapshot endpoint, but leaves your code in place as a safety measure. Monitor your thin-only flow to confirm stability.

If everything remains stable:

Check your endpoint URL: Verify the thin destination points to the correct URL (for example, /webhook/thin, not /webhook).

Test locally: Use a tunneling tool such as ngrok to expose your local endpoint, then create a thin event destination pointing to that URL.

Check webhook secret: Make sure THIN_WEBHOOK_SECRET contains the signing secret from your thin event destination, not your snapshot destination.

Inspect raw payload: Signature verification requires the raw request body. Don’t parse the JSON before verifying:

We recommend that you migrate event-by-event by subscribing to specific thin event types in your new destination. For example, start with v1.customer.created and v1.customer.updated, validate, then add more event types.

We don’t recommend running dual handlers or letting them run indefinitely. Running dual handlers increases operational complexity, costs (bandwidth and processing), and increases the risk of divergent behavior. Complete the migration within a few weeks.

A key benefit of thin events is that your webhook payload doesn’t change. The push notification remains stable, and you fetch versioned resource details when you need them using your current API version.

**Examples:**

Example 1 (javascript):
```javascript
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY, {
  apiVersion: '2025-11-17.preview'
});
```

Example 2 (javascript):
```javascript
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY, {
  apiVersion: '2025-11-17.preview'
});
```

Example 3 (javascript):
```javascript
const express = require('express');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY, {
  apiVersion: '2025-11-17.preview'
});

const app = express();

// New thin event endpoint
app.post(
  '/webhook/thin',
  express.raw({type: 'application/json'}),
  async (req, res) => {
    const sig = req.headers['stripe-signature'];
    const thinWebhookSecret = process.env.THIN_WEBHOOK_SECRET;

    try {
      // Verify the signature using the same method as snapshot events
      const thinNotification = stripe.webhooks.constructEvent(
        req.body,
        sig,
        thinWebhookSecret
      );

      console.log(`Verified thin event: ${thinNotification.id}`);

      // For now, just acknowledge receipt
      res.sendStatus(200);
    } catch (err) {
      console.log(`Webhook Error: ${err.message}`);
      res.status(400).send(`Webhook Error: ${err.message}`);
    }
  }
);

app.listen(3000, () => console.log('Running on port 3000'));
```

Example 4 (javascript):
```javascript
const express = require('express');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY, {
  apiVersion: '2025-11-17.preview'
});

const app = express();

// New thin event endpoint
app.post(
  '/webhook/thin',
  express.raw({type: 'application/json'}),
  async (req, res) => {
    const sig = req.headers['stripe-signature'];
    const thinWebhookSecret = process.env.THIN_WEBHOOK_SECRET;

    try {
      // Verify the signature using the same method as snapshot events
      const thinNotification = stripe.webhooks.constructEvent(
        req.body,
        sig,
        thinWebhookSecret
      );

      console.log(`Verified thin event: ${thinNotification.id}`);

      // For now, just acknowledge receipt
      res.sendStatus(200);
    } catch (err) {
      console.log(`Webhook Error: ${err.message}`);
      res.status(400).send(`Webhook Error: ${err.message}`);
    }
  }
);

app.listen(3000, () => console.log('Running on port 3000'));
```

---

## The Event object

**URL:** https://docs.stripe.com/api/events/object

**Contents:**
- The Event object
  - Attributes
    - idstring
    - api_versionnullable string
    - dataobject
    - requestnullable object
    - typestring
  - More attributesExpand all
    - objectstring
    - accountnullable stringConnect only

Unique identifier for the object.

The Stripe API version used to render data when the event was created. The contents of data never change, so this value remains static regardless of the API version currently in use. This property is populated only for events created on or after October 31, 2014.

Object containing data associated with the event.

Information on the API request that triggers the event.

Description of the event (for example, invoice.created or charge.refunded).

Retrieves the details of an event if it was created in the last 30 days. Supply the unique identifier of the event, which you might have received in a webhook.

Returns an event object if a valid identifier was provided. All events share a common structure, detailed to the right. The only property that will differ is the data property.

In each case, the data dictionary will have an attribute called object and its value will be the same as retrieving the same object directly from the API. For example, a customer.created event will have the same information as retrieving the relevant customer would.

In cases where the attributes of an object have changed, data will also contain a dictionary containing the changes.

List events, going back up to 30 days. Each event data is rendered according to Stripe API version at its creation time, specified in event object api_version attribute (not according to your current Stripe API version or Stripe-Version header).

An array of up to 20 strings containing specific event names. The list will be filtered to include only events with a matching event property. You may pass either type or types, but not both.

A dictionary with a data property that contains an array of up to limit events, starting after event starting_after. Each entry in the array is a separate event object. If no more events are available, the resulting array will be empty.

This is a list of all public snapshot events we currently send for /v1 resources, which is continually evolving and expanding.

Stripe events use the resource.event naming convention. Events that occur on subresources like customer.subscription.updated don’t trigger a corresponding event for the parent resource (customer.updated).

Stripe creates event types marked as Selection required only when at least one webhook is listening for it. A webhook set to listen to all events doesn’t satisfy this requirement and won’t generate Selection required event types.

Occurs whenever a user authorizes an application. Sent to the related application only.

Occurs whenever a user deauthorizes an application. Sent to the related application only.

Occurs whenever an external account is created.

Occurs whenever an external account is deleted.

Occurs whenever an external account is updated.

Occurs whenever an account status or property has changed.

Occurs whenever an application fee is created on a charge.

Occurs whenever an application fee refund is updated.

Occurs whenever an application fee is refunded, whether from refunding a charge or from refunding the application fee directly. This includes partial refunds.

Occurs whenever a balance settings status or property has changed.

Occurs whenever your Stripe balance has been updated (e.g., when a charge is available to be paid out). By default, Stripe automatically transfers funds in your balance to your bank account on a daily basis. This event is not fired for negative transactions.

Occurs whenever a portal configuration is created.

Occurs whenever a portal configuration is updated.

Occurs whenever a portal session is created.

Occurs whenever your custom alert threshold is met.

Occurs when a credit balance transaction is created

Occurs when a credit grant is created

Occurs when a credit grant is updated

Occurs when a meter is created

Occurs when a meter is deactivated

Occurs when a meter is reactivated

Occurs when a meter is updated

Occurs whenever a capability has new requirements or a new status.

Occurs whenever there is a positive remaining cash balance after Stripe automatically reconciles new funds into the cash balance. If you enabled manual reconciliation, this webhook will fire whenever there are new funds into the cash balance.

Occurs whenever a previously uncaptured charge is captured.

Occurs when a dispute is closed and the dispute status changes to lost, warning_closed, or won.

Occurs whenever a customer disputes a charge with their bank.

Occurs when funds are reinstated to your account after a dispute is closed. This includes partially refunded payments.

Occurs when funds are removed from your account due to a dispute.

Occurs when the dispute is updated (usually with evidence).

Occurs whenever an uncaptured charge expires.

Occurs whenever a failed charge attempt occurs.

Occurs whenever a pending charge is created.

Occurs whenever a refund is updated on selected payment methods. For updates on all refunds, listen to refund.updated instead.

Occurs whenever a charge is refunded, including partial refunds. Listen to refund.created for information about the refund.

Occurs whenever a charge is successful.

Occurs whenever a charge description or metadata is updated, or upon an asynchronous capture.

Occurs when a payment intent using a delayed payment method fails.

Occurs when a payment intent using a delayed payment method finally succeeds.

Occurs when a Checkout Session has been successfully completed.

Occurs when a Checkout Session is expired.

Occurs when a Climate order is canceled.

Occurs when a Climate order is created.

Occurs when a Climate order is delayed.

Occurs when a Climate order is delivered.

Occurs when a Climate order’s product is substituted for another.

Occurs when a Climate product is created.

Occurs when a Climate product is updated.

Occurs whenever a coupon is created.

Occurs whenever a coupon is deleted.

Occurs whenever a coupon is updated.

Occurs whenever a credit note is created.

Occurs whenever a credit note is updated.

Occurs whenever a credit note is voided.

Occurs whenever a new customer cash balance transactions is created.

Occurs whenever a new customer is created.

Occurs whenever a customer is deleted.

Occurs whenever a coupon is attached to a customer.

Occurs whenever a coupon is removed from a customer.

Occurs whenever a customer is switched from one coupon to another.

Occurs whenever a new source is created for a customer.

Occurs whenever a source is removed from a customer.

Occurs whenever a card or source will expire at the end of the month. This event only works with legacy integrations using Card or Source objects. If you use the PaymentMethod API, this event won’t occur.

Occurs whenever a source’s details are changed.

Occurs whenever a customer is signed up for a new plan.

Occurs whenever a customer’s subscription ends.

Occurs whenever a customer’s subscription is paused. Only applies when subscriptions enter status=paused, not when payment collection is paused.

Occurs whenever a customer’s subscription’s pending update is applied, and the subscription is updated.

Occurs whenever a customer’s subscription’s pending update expires before the related invoice is paid.

Occurs whenever a customer’s subscription is no longer paused. Only applies when a status=paused subscription is resumed, not when payment collection is resumed.

Occurs three days before a subscription’s trial period is scheduled to end, or when a trial is ended immediately (using trial_end=now).

Occurs whenever a subscription changes (e.g., switching from one plan to another, or changing the status from trial to active).

Occurs whenever a tax ID is created for a customer.

Occurs whenever a tax ID is deleted from a customer.

Occurs whenever a customer’s tax ID is updated.

Occurs whenever any property of a customer changes.

Occurs whenever a customer’s entitlements change.

Occurs whenever a new Stripe-generated file is available for your account.

Occurs when a Financial Connections account’s account numbers are updated.

Occurs when a new Financial Connections account is created.

Occurs when a Financial Connections account’s status is updated from active to inactive.

Occurs when a Financial Connections account is disconnected.

Occurs when a Financial Connections account’s status is updated from inactive to active.

Occurs when an Account’s balance_refresh status transitions from pending to either succeeded or failed.

Occurs when an Account’s ownership_refresh status transitions from pending to either succeeded or failed.

Occurs when an Account’s transaction_refresh status transitions from pending to either succeeded or failed.

Occurs when an Account’s tokenized account number is about to expire.

Occurs whenever a VerificationSession is canceled

Occurs whenever a VerificationSession is created

Occurs whenever a VerificationSession transitions to processing

Occurs whenever a VerificationSession is redacted.

Occurs whenever a VerificationSession transitions to require user input

Occurs whenever a VerificationSession transitions to verified

Occurs when an InvoicePayment is successfully paid.

Occurs whenever a new invoice is created. To learn how webhooks can be used with this event, and how they can affect it, see Using Webhooks with Subscriptions.

Occurs whenever a draft invoice is deleted. Note: This event is not sent for invoice previews.

Occurs whenever a draft invoice cannot be finalized. See the invoice’s last finalization error for details.

Occurs whenever a draft invoice is finalized and updated to be an open invoice.

Occurs whenever an invoice is marked uncollectible.

Occurs X number of days after an invoice becomes due—where X is determined by Automations

Occurs when an invoice transitions to paid with a non-zero amount_overpaid.

Occurs whenever an invoice payment attempt succeeds or an invoice is marked as paid out-of-band.

Occurs whenever an invoice payment attempt requires further user action to complete.

Occurs when an invoice requires a payment using a payment method that cannot be processed by Stripe.

Occurs whenever an invoice payment attempt fails, due to either a declined payment, including soft decline, or to the lack of a stored payment method.

Occurs whenever an invoice payment attempt succeeds.

Occurs whenever an invoice email is sent out.

Occurs X number of days before a subscription is scheduled to create an invoice that is automatically charged—where X is determined by your subscriptions settings. Note: The received Invoice object will not have an invoice ID.

Occurs whenever an invoice changes (e.g., the invoice amount).

Occurs whenever an invoice is voided.

Occurs X number of days before an invoice becomes due—where X is determined by Automations

Occurs whenever an invoice item is created.

Occurs whenever an invoice item is deleted.

Occurs whenever an authorization is created.

Represents a synchronous request for authorization, see Using your integration to handle authorization requests.

Occurs whenever an authorization is updated.

Occurs whenever a card is created.

Occurs whenever a card is updated.

Occurs whenever a cardholder is created.

Occurs whenever a cardholder is updated.

Occurs whenever a dispute is won, lost or expired.

Occurs whenever a dispute is created.

Occurs whenever funds are reinstated to your account for an Issuing dispute.

Occurs whenever funds are deducted from your account for an Issuing dispute.

Occurs whenever a dispute is submitted.

Occurs whenever a dispute is updated.

Occurs whenever a personalization design is activated following the activation of the physical bundle that belongs to it.

Occurs whenever a personalization design is deactivated following the deactivation of the physical bundle that belongs to it.

Occurs whenever a personalization design is rejected by design review.

Occurs whenever a personalization design is updated.

Occurs whenever an issuing digital wallet token is created.

Occurs whenever an issuing digital wallet token is updated.

Occurs whenever an issuing transaction is created.

Occurs whenever an issuing transaction is updated with receipt data.

Occurs whenever an issuing transaction is updated.

Occurs whenever a Mandate is updated.

Occurs when a PaymentIntent has funds to be captured. Check the amount_capturable property on the PaymentIntent to determine the amount that can be captured. You may capture the PaymentIntent with an amount_to_capture value up to the specified amount. Learn more about capturing PaymentIntents.

Occurs when a PaymentIntent is canceled.

Occurs when a new PaymentIntent is created.

Occurs when funds are applied to a customer_balance PaymentIntent and the ‘amount_remaining’ changes.

Occurs when a PaymentIntent has failed the attempt to create a payment method or a payment.

Occurs when a PaymentIntent has started processing.

Occurs when a PaymentIntent transitions to requires_action state

Occurs when a PaymentIntent has successfully completed payment.

Occurs when a payment link is created.

Occurs when a payment link is updated.

Occurs whenever a new payment method is attached to a customer.

Occurs whenever a payment method’s details are automatically updated by the network.

Occurs whenever a payment method is detached from a customer.

Occurs whenever a payment method is updated via the PaymentMethod update API.

Occurs whenever a payout is canceled.

Occurs whenever a payout is created.

Occurs whenever a payout attempt fails.

Occurs whenever a payout is expected to be available in the destination account. If the payout fails, a payout.failed notification is also sent, at a later time.

Occurs whenever balance transactions paid out in an automatic payout can be queried.

Occurs whenever a payout is updated.

Occurs whenever a person associated with an account is created.

Occurs whenever a person associated with an account is deleted.

Occurs whenever a person associated with an account is updated.

Occurs whenever a plan is created.

Occurs whenever a plan is deleted.

Occurs whenever a plan is updated.

Occurs whenever a price is created.

Occurs whenever a price is deleted.

Occurs whenever a price is updated.

Occurs whenever a product is created.

Occurs whenever a product is deleted.

Occurs whenever a product is updated.

Occurs whenever a promotion code is created.

Occurs whenever a promotion code is updated.

Occurs whenever a quote is accepted.

Occurs whenever a quote is canceled.

Occurs whenever a quote is created.

Occurs whenever a quote is finalized.

Occurs X number of days before a quote is scheduled to expire—where X is determined by Automations

Occurs whenever an early fraud warning is created.

Occurs whenever an early fraud warning is updated.

Occurs whenever a refund is created.

Occurs whenever a refund has failed.

Occurs whenever a refund is updated.

Occurs whenever a requested ReportRun failed to complete.

Occurs whenever a requested ReportRun completed successfully.

Occurs whenever a ReportType is updated (typically to indicate that a new day’s data has come available).

Occurs whenever a review is closed. The review’s reason field indicates why: approved, disputed, refunded, refunded_as_fraud, or canceled.

Occurs whenever a review is opened.

Occurs when a SetupIntent is canceled.

Occurs when a new SetupIntent is created.

Occurs when a SetupIntent is in requires_action state.

Occurs when a SetupIntent has failed the attempt to setup a payment method.

Occurs when an SetupIntent has successfully setup a payment method.

Occurs whenever a Sigma scheduled query run finishes.

Occurs whenever a source is canceled.

Occurs whenever a source transitions to chargeable.

Occurs whenever a source fails.

Occurs whenever a source mandate notification method is set to manual.

Occurs whenever the refund attributes are required on a receiver source to process a refund or a mispayment.

Occurs whenever a source transaction is created.

Occurs whenever a source transaction is updated.

Occurs whenever a subscription schedule is canceled due to the underlying subscription being canceled because of delinquency.

Occurs whenever a subscription schedule is canceled.

Occurs whenever a new subscription schedule is completed.

Occurs whenever a new subscription schedule is created.

Occurs 7 days before a subscription schedule will expire.

Occurs whenever a new subscription schedule is released.

Occurs whenever a subscription schedule is updated.

Occurs whenever a new tax rate is created.

Occurs whenever a tax rate is updated.

Occurs whenever tax settings is updated.

Occurs whenever an action sent to a Terminal reader failed.

Occurs whenever an action sent to a Terminal reader was successful.

Occurs whenever an action sent to a Terminal reader is updated.

Occurs whenever a test clock starts advancing.

Occurs whenever a test clock is created.

Occurs whenever a test clock is deleted.

Occurs whenever a test clock fails to advance its frozen time.

Occurs whenever a test clock transitions to a ready status.

Occurs whenever a top-up is canceled.

Occurs whenever a top-up is created.

Occurs whenever a top-up fails.

Occurs whenever a top-up is reversed.

Occurs whenever a top-up succeeds.

Occurs whenever a transfer is created.

Occurs whenever a transfer is reversed, including partial reversals.

Occurs whenever a transfer’s description or metadata is updated.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "evt_1NG8Du2eZvKYlo2CUI79vXWy",  "object": "event",  "api_version": "2019-02-19",  "created": 1686089970,  "data": {    "object": {      "id": "seti_1NG8Du2eZvKYlo2C9XMqbR0x",      "object": "setup_intent",      "application": null,      "automatic_payment_methods": null,      "cancellation_reason": null,      "client_secret": "seti_1NG8Du2eZvKYlo2C9XMqbR0x_secret_O2CdhLwGFh2Aej7bCY7qp8jlIuyR8DJ",      "created": 1686089970,      "customer": null,      "description": null,      "flow_directions": null,      "last_setup_error": null,      "latest_attempt": null,      "livemode": false,      "mandate": null,      "metadata": {},      "next_action": null,      "on_behalf_of": null,      "payment_method": "pm_1NG8Du2eZvKYlo2CYzzldNr7",      "payment_method_options": {        "acss_debit": {          "currency": "cad",          "mandate_options": {            "interval_description": "First day of every month",            "payment_schedule": "interval",            "transaction_type": "personal"          },          "verification_method": "automatic"        }      },      "payment_method_types": [        "acss_debit"      ],      "single_use_mandate": null,      "status": "requires_confirmation",      "usage": "off_session"    }  },  "livemode": false,  "pending_webhooks": 0,  "request": {    "id": null,    "idempotency_key": null  },  "type": "setup_intent.created"}
```

Example 2 (unknown):
```unknown
{  "id": "evt_1NG8Du2eZvKYlo2CUI79vXWy",  "object": "event",  "api_version": "2019-02-19",  "created": 1686089970,  "data": {    "object": {      "id": "seti_1NG8Du2eZvKYlo2C9XMqbR0x",      "object": "setup_intent",      "application": null,      "automatic_payment_methods": null,      "cancellation_reason": null,      "client_secret": "seti_1NG8Du2eZvKYlo2C9XMqbR0x_secret_O2CdhLwGFh2Aej7bCY7qp8jlIuyR8DJ",      "created": 1686089970,      "customer": null,      "description": null,      "flow_directions": null,      "last_setup_error": null,      "latest_attempt": null,      "livemode": false,      "mandate": null,      "metadata": {},      "next_action": null,      "on_behalf_of": null,      "payment_method": "pm_1NG8Du2eZvKYlo2CYzzldNr7",      "payment_method_options": {        "acss_debit": {          "currency": "cad",          "mandate_options": {            "interval_description": "First day of every month",            "payment_schedule": "interval",            "transaction_type": "personal"          },          "verification_method": "automatic"        }      },      "payment_method_types": [        "acss_debit"      ],      "single_use_mandate": null,      "status": "requires_confirmation",      "usage": "off_session"    }  },  "livemode": false,  "pending_webhooks": 0,  "request": {    "id": null,    "idempotency_key": null  },  "type": "setup_intent.created"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/events/evt_1NG8Du2eZvKYlo2CUI79vXWy \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/events/evt_1NG8Du2eZvKYlo2CUI79vXWy \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

---

## Retrieve an event v2

**URL:** https://docs.stripe.com/api/v2/core/events/retrieve

**Contents:**
- Retrieve an event v2
  - Parameters
    - idstringRequired
  - Returns
  - Response attributes
    - idstring
    - objectstring, value is "v2.core.event"
    - changesnullable object
    - contextnullable string
    - createdtimestamp

Retrieves the details of an event.

Unique identifier for the object.

Unique identifier for the event.

String representing the object’s type. Objects of the same type share the same value of the object field.

Before and after changes for the primary related object.

Authentication context needed to fetch the event or related object.

Time at which the object was created.

Additional data about the event.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Reason for the event.

Object containing the reference to API resource relevant to the event.

The type of the event.

The resource wasn’t found.

List events, going back up to 30 days.

Set of filters to query events within a range of created timestamps.

Primary object ID used to retrieve related events.

An array of up to 20 strings containing specific event names.

The previous page url.

Send a ping event to an event destination.

Identifier for the event destination to ping.

Unique identifier for the event.

String representing the object’s type. Objects of the same type share the same value of the object field.

Before and after changes for the primary related object.

Authentication context needed to fetch the event or related object.

Time at which the object was created.

Additional data about the event.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Reason for the event.

Object containing the reference to API resource relevant to the event.

The type of the event.

The resource wasn’t found.

This is a list of all public thin events we currently send for /v1 and /v2 resources, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v2/core/events/evt_test_65RCjj4EqW1sabcjs2Z16RCMoNQdSQkOWvfL6L5uU2K40u \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v2/core/events/evt_test_65RCjj4EqW1sabcjs2Z16RCMoNQdSQkOWvfL6L5uU2K40u \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 3 (unknown):
```unknown
{  "id": "evt_test_65RCjj4EqW1sabcjs2Z16RCMoNQdSQkOWvfL6L5uU2K40u",  "object": "v2.core.event",  "context": null,  "created": "2024-09-26T17:46:22.134Z",  "data": {    "developer_message_summary": "There is 1 invalid event",    "reason": {      "error_count": 1,      "error_types": [        {          "code": "meter_event_no_customer_defined",          "error_count": 1,          "sample_errors": [            {              "error_message": "Customer mapping key stripe_customer_id not found in payload.",              "request": {                "identifier": "cb447754-6880-45c2-8f2f-ef19b6ce81e9"              }            }          ]        }      ]    },    "validation_end": "2024-09-26T17:46:20.000Z",    "validation_start": "2024-09-26T17:46:10.000Z"  },  "livemode": false,  "reason": null,  "related_object": {    "id": "mtr_test_61RCjiqdTDC91zgip41IqPCzPnxqqSVc",    "type": "billing.meter",    "url": "/v1/billing/meters/mtr_test_61RCjiqdTDC91zgip41IqPCzPnxqqSVc"  },  "type": "v1.billing.meter.error_report_triggered"}
```

Example 4 (unknown):
```unknown
{  "id": "evt_test_65RCjj4EqW1sabcjs2Z16RCMoNQdSQkOWvfL6L5uU2K40u",  "object": "v2.core.event",  "context": null,  "created": "2024-09-26T17:46:22.134Z",  "data": {    "developer_message_summary": "There is 1 invalid event",    "reason": {      "error_count": 1,      "error_types": [        {          "code": "meter_event_no_customer_defined",          "error_count": 1,          "sample_errors": [            {              "error_message": "Customer mapping key stripe_customer_id not found in payload.",              "request": {                "identifier": "cb447754-6880-45c2-8f2f-ef19b6ce81e9"              }            }          ]        }      ]    },    "validation_end": "2024-09-26T17:46:20.000Z",    "validation_start": "2024-09-26T17:46:10.000Z"  },  "livemode": false,  "reason": null,  "related_object": {    "id": "mtr_test_61RCjiqdTDC91zgip41IqPCzPnxqqSVc",    "type": "billing.meter",    "url": "/v1/billing/meters/mtr_test_61RCjiqdTDC91zgip41IqPCzPnxqqSVc"  },  "type": "v1.billing.meter.error_report_triggered"}
```

---

## Types of events v2

**URL:** https://docs.stripe.com/api/v2/core/events/event-types

**Contents:**
- Types of events v2
- Event types
  - v1.billing.meter.error_report_triggered
  - v1.billing.meter.no_meter_found
  - v2.core.account_link.returned
  - v2.core.account_person.created
  - v2.core.account_person.deleted
  - v2.core.account_person.updated
  - v2.core.account.closed
  - v2.core.account.created

This is a list of all public thin events we currently send for /v1 and /v2 resources, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

---

## Resolve webhook signature verification errors

**URL:** https://docs.stripe.com/webhooks/signature

**Contents:**
- Resolve webhook signature verification errors
- Learn how to fix a common error when listening to webhook events.
- Check the endpoint secret
- Check the request body
  - Retrieve the raw request body
  - AWS API Gateway with Lambda function
- Check the signature

When processing webhook events, we recommend securing your endpoint by verifying that the event is coming from Stripe. To do this, use the Stripe-Signature header and call the constructEvent() function with three parameters:

This function might look like this:

If you get the following Webhook signature verification failed error, at least one of the three parameters you passed to the constructEvent() function is incorrect.

The most common error is using the wrong endpoint secret. If you’re using a webhook endpoint created in the Dashboard, open the endpoint in the Dashboard and click the Reveal secret link near the top of the page to view the secret. If you’re using the Stripe CLI, the secret is printed in the Terminal when you run the stripe listen command.

In both cases, the secret starts with a whsec_ prefix, but the secret itself is different. Don’t verify signatures on events forwarded by the CLI using the secret from a Dashboard-managed endpoint, or the other way around. Finally, print the endpointSecret used in your code, and make sure that it matches the one you found above.

The request body must be the body string that Stripe sends in UTF-8 encoding without any changes. When you print it as a string, it looks similar to this:

Some frameworks might edit the request body by doing things like adding or removing whitespace, reordering the key-value pairs, converting the string to JSON, or changing the encoding. All of these cases lead to a failed signature verification.

The following is a non-exhaustive list of frameworks that might parse or mutate the data using common configurations, and some tips on how to get the raw request body.

If you’re using the stripe-node library with Express, make sure that app.use(express.json()) is placed after the webhook route. In Express, the order of middleware configuration matters. If express.json() is applied before your webhook route, it parses the request body before signature verification, causing the verification to fail. For example:

To retrieve the raw request body for the AWS API Gateway with Lambda function, in the API Gateway, set up a Body Mapping Template of content type application/json:

Then, in the Lambda function, access the raw body with the event’s rawBody property and the headers with the event’s headers property.

Print the signature parameter, and confirm that it looks similar to this:

If not, check if you have an issue in your code when trying to extract the signature from the header.

**Examples:**

Example 1 (unknown):
```unknown
Stripe::Webhook.construct_event(request_body, signature, endpoint_secret)
```

Example 2 (unknown):
```unknown
Stripe::Webhook.construct_event(request_body, signature, endpoint_secret)
```

Example 3 (unknown):
```unknown
Webhook signature verification failed. Err: No signatures found matching the expected signature for payload.
```

Example 4 (unknown):
```unknown
Webhook signature verification failed. Err: No signatures found matching the expected signature for payload.
```

---

## Process undelivered webhook events

**URL:** https://docs.stripe.com/webhooks/process-undelivered-events

**Contents:**
- Process undelivered webhook events
- Learn how to manually process undelivered webhook events.
- List webhook events
- Process the events
- Respond to automatic retries

If your webhook endpoint temporarily can’t process events, Stripe automatically resends the undelivered events to your endpoint for up to three days, increasing the time for your webhook endpoint to eventually receive and process all events.

This guide explains how to speed up that process by manually processing the undelivered events.

Call the List Events API with the following parameters:

Stripe only returns events created in the last 30 days.

By default, the response returns up to 10 events. To retrieve all events, use auto-pagination after retrieving the results.

Using ending_before with auto-pagination returns events in chronological order. This lets you process events in their created order.

Process only unsuccessfully processed events according to your own logic to avoid processing a single event multiple times by, for example:

Define the following functions that prevent processing duplication:

Stripe still considers your manually preocessed events as undelivered, so continues to automaticly retry them.

When your webhook endpoint receives an already processed event, ignore the event and return a successful response to stop future retries.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v1/events \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d ending_before=evt_001 \
  -d "types[]"="payment_intent.succeeded" \
  -d "types[]"="payment_intent.payment_failed" \
  -d delivery_success=false
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v1/events \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d ending_before=evt_001 \
  -d "types[]"="payment_intent.succeeded" \
  -d "types[]"="payment_intent.payment_failed" \
  -d delivery_success=false
```

Example 3 (unknown):
```unknown
events = Stripe::Event.list({
  ending_before: 'evt_001',
  types: ['payment_intent.succeeded', 'payment_intent.payment_failed'],
  delivery_success: false,
})

events.auto_paging_each do |event|
  # This function is defined in the next section
  process_event(event)
end
```

Example 4 (unknown):
```unknown
events = Stripe::Event.list({
  ending_before: 'evt_001',
  types: ['payment_intent.succeeded', 'payment_intent.payment_failed'],
  delivery_success: false,
})

events.auto_paging_each do |event|
  # This function is defined in the next section
  process_event(event)
end
```

---

## Events v2

**URL:** https://docs.stripe.com/api/v2/core/events

**Contents:**
- Events v2
- The Event object
  - Attributes
    - idstring
    - objectstring, value is "v2.core.event"
    - changesnullable object
    - contextnullable string
    - createdtimestamp
    - datanullable object
    - livemodeboolean

Events are generated to keep you informed of activity in your business account. APIs in the /v2 namespace generate thin events which have small, unversioned payloads that include a reference to the ID of the object that has changed. The Events v2 API returns these new thin events. Retrieve the event object for additional data about the event. Use the related object ID in the event payload to fetch the API resource of the object associated with the event. Comparatively, events generated by most API v1 include a versioned snapshot of an API object in their payload.

Unique identifier for the event.

String representing the object’s type. Objects of the same type share the same value of the object field.

Before and after changes for the primary related object.

Authentication context needed to fetch the event or related object.

Time at which the object was created.

Additional data about the event.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Reason for the event.

Object containing the reference to API resource relevant to the event.

The type of the event.

Retrieves the details of an event.

Unique identifier for the object.

Unique identifier for the event.

String representing the object’s type. Objects of the same type share the same value of the object field.

Before and after changes for the primary related object.

Authentication context needed to fetch the event or related object.

Time at which the object was created.

Additional data about the event.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Reason for the event.

Object containing the reference to API resource relevant to the event.

The type of the event.

The resource wasn’t found.

List events, going back up to 30 days.

Set of filters to query events within a range of created timestamps.

Primary object ID used to retrieve related events.

An array of up to 20 strings containing specific event names.

The previous page url.

Send a ping event to an event destination.

Identifier for the event destination to ping.

Unique identifier for the event.

String representing the object’s type. Objects of the same type share the same value of the object field.

Before and after changes for the primary related object.

Authentication context needed to fetch the event or related object.

Time at which the object was created.

Additional data about the event.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Reason for the event.

Object containing the reference to API resource relevant to the event.

The type of the event.

The resource wasn’t found.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "evt_test_65RCjj4EqW1sabcjs2Z16RCMoNQdSQkOWvfL6L5uU2K40u",  "object": "v2.core.event",  "context": null,  "created": "2024-09-26T17:46:22.134Z",  "data": {    "developer_message_summary": "There is 1 invalid event",    "reason": {      "error_count": 1,      "error_types": [        {          "code": "meter_event_no_customer_defined",          "error_count": 1,          "sample_errors": [            {              "error_message": "Customer mapping key stripe_customer_id not found in payload.",              "request": {                "identifier": "cb447754-6880-45c2-8f2f-ef19b6ce81e9"              }            }          ]        }      ]    },    "validation_end": "2024-09-26T17:46:20.000Z",    "validation_start": "2024-09-26T17:46:10.000Z"  },  "livemode": false,  "reason": null,  "related_object": {    "id": "mtr_test_61RCjiqdTDC91zgip41IqPCzPnxqqSVc",    "type": "billing.meter",    "url": "/v1/billing/meters/mtr_test_61RCjiqdTDC91zgip41IqPCzPnxqqSVc"  },  "type": "v1.billing.meter.error_report_triggered"}
```

Example 2 (unknown):
```unknown
{  "id": "evt_test_65RCjj4EqW1sabcjs2Z16RCMoNQdSQkOWvfL6L5uU2K40u",  "object": "v2.core.event",  "context": null,  "created": "2024-09-26T17:46:22.134Z",  "data": {    "developer_message_summary": "There is 1 invalid event",    "reason": {      "error_count": 1,      "error_types": [        {          "code": "meter_event_no_customer_defined",          "error_count": 1,          "sample_errors": [            {              "error_message": "Customer mapping key stripe_customer_id not found in payload.",              "request": {                "identifier": "cb447754-6880-45c2-8f2f-ef19b6ce81e9"              }            }          ]        }      ]    },    "validation_end": "2024-09-26T17:46:20.000Z",    "validation_start": "2024-09-26T17:46:10.000Z"  },  "livemode": false,  "reason": null,  "related_object": {    "id": "mtr_test_61RCjiqdTDC91zgip41IqPCzPnxqqSVc",    "type": "billing.meter",    "url": "/v1/billing/meters/mtr_test_61RCjiqdTDC91zgip41IqPCzPnxqqSVc"  },  "type": "v1.billing.meter.error_report_triggered"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v2/core/events/evt_test_65RCjj4EqW1sabcjs2Z16RCMoNQdSQkOWvfL6L5uU2K40u \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v2/core/events/evt_test_65RCjj4EqW1sabcjs2Z16RCMoNQdSQkOWvfL6L5uU2K40u \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

---

## List events v2

**URL:** https://docs.stripe.com/api/v2/core/events/list

**Contents:**
- List events v2
  - Parameters
    - createdobject
    - limitinteger
    - object_idstring
    - pagestring
    - typesarray of strings
  - Returns
  - Response attributes
    - dataarray of objects

List events, going back up to 30 days.

Set of filters to query events within a range of created timestamps.

Primary object ID used to retrieve related events.

An array of up to 20 strings containing specific event names.

The previous page url.

Send a ping event to an event destination.

Identifier for the event destination to ping.

Unique identifier for the event.

String representing the object’s type. Objects of the same type share the same value of the object field.

Before and after changes for the primary related object.

Authentication context needed to fetch the event or related object.

Time at which the object was created.

Additional data about the event.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Reason for the event.

Object containing the reference to API resource relevant to the event.

The type of the event.

The resource wasn’t found.

This is a list of all public thin events we currently send for /v1 and /v2 resources, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v2/core/events \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  -d object_id=mtr_test_61RCjiqdTDC91zgip41IqPCzPnxqqSVc
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v2/core/events \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  -d object_id=mtr_test_61RCjiqdTDC91zgip41IqPCzPnxqqSVc
```

Example 3 (unknown):
```unknown
{  "data": [    {      "id": "evt_test_65RCjj4EqW1sabcjs2Z16RCMoNQdSQkOWvfL6L5uU2K40u",      "object": "v2.core.event",      "context": null,      "created": "2024-09-26T17:46:22.134Z",      "data": {        "developer_message_summary": "There is 1 invalid event",        "reason": {          "error_count": 1,          "error_types": [            {              "code": "meter_event_no_customer_defined",              "error_count": 1,              "sample_errors": [                {                  "error_message": "Customer mapping key stripe_customer_id not found in payload.",                  "request": {                    "identifier": "cb447754-6880-45c2-8f2f-ef19b6ce81e9"                  }                }              ]            }          ]        },        "validation_end": "2024-09-26T17:46:20.000Z",        "validation_start": "2024-09-26T17:46:10.000Z"      },      "livemode": false,      "reason": null,      "related_object": {        "id": "mtr_test_61RCjiqdTDC91zgip41IqPCzPnxqqSVc",        "type": "billing.meter",        "url": "/v1/billing/meters/mtr_test_61RCjiqdTDC91zgip41IqPCzPnxqqSVc"      },      "type": "v1.billing.meter.error_report_triggered"    }  ],  "next_page_url": null,  "previous_page_url": null}
```

Example 4 (unknown):
```unknown
{  "data": [    {      "id": "evt_test_65RCjj4EqW1sabcjs2Z16RCMoNQdSQkOWvfL6L5uU2K40u",      "object": "v2.core.event",      "context": null,      "created": "2024-09-26T17:46:22.134Z",      "data": {        "developer_message_summary": "There is 1 invalid event",        "reason": {          "error_count": 1,          "error_types": [            {              "code": "meter_event_no_customer_defined",              "error_count": 1,              "sample_errors": [                {                  "error_message": "Customer mapping key stripe_customer_id not found in payload.",                  "request": {                    "identifier": "cb447754-6880-45c2-8f2f-ef19b6ce81e9"                  }                }              ]            }          ]        },        "validation_end": "2024-09-26T17:46:20.000Z",        "validation_start": "2024-09-26T17:46:10.000Z"      },      "livemode": false,      "reason": null,      "related_object": {        "id": "mtr_test_61RCjiqdTDC91zgip41IqPCzPnxqqSVc",        "type": "billing.meter",        "url": "/v1/billing/meters/mtr_test_61RCjiqdTDC91zgip41IqPCzPnxqqSVc"      },      "type": "v1.billing.meter.error_report_triggered"    }  ],  "next_page_url": null,  "previous_page_url": null}
```

---

## Handle irrecoverable webhook eventsPublic preview

**URL:** https://docs.stripe.com/webhooks/handle-irrecoverable-events

**Contents:**
- Handle irrecoverable webhook eventsPublic preview
- Learn how to handle webhooks that fail to generate.
- Delivery of failed events
  - Workbench
  - Webhook endpoints
- How to use the health event

In very rare cases, Stripe can fail to generate the Event object. In these cases, the event is irrecoverable. Stripe can’t deliver it to your event destinations, nor publish it in the Dashboard or in the List Events API. Instead, Stripe creates a v2.core.health.event_generation_failure.resolved event to inform you that the Event generation failed. This guide explains how the alert works, and what you can do to recover from it.

Stripe delivers v2.core.health.event_generation_failure.resolved events to both Workbench and to any webhook endpoints you configure to listen for them.

The v2.core.health.event_generation_failure.resolved events appear in two places in Workbench:

Follow the webhook setup guide to register a webhook endpoint that listens to v2.core.health.event_generation_failure.resolved thin events. After you register the correct webhook endpoint, Stripe sends v2.core.health.event_generation_failure.resolved events to it.

When Stripe fails to generate an event, you can process the generated event notification to retrieve the v2.core.health.event_generation_failure.resolved object, as shown in the following example.

The example event provides the following information about the failure:

If your integration relies on receiving webhooks for the payment_intent.requires_action event, this failure makes it out of sync with the Stripe state. To realign your integration after you receive a v2.core.health.event_generation_failure.resolved webhook, poll the relevant API (in this case the Payment Intents API) to retrieve the related object:

**Examples:**

Example 1 (unknown):
```unknown
{
  "alert_id": "halert_61RFBMa6o6H87usts16RFBM10hSQlYfddqcFoEMR6CPY",
  "grouping_key": "_grouping_s8PgTvizbkORV9z5PhaJSvc4dUcAMmfRpEHKm4EeJ1glsQ5XMf",
  "impact": {
    "event_type": "payment_intent.requires_action",
    "related_object_id": "pi_1QA8PKDTvO5jCVb3TVDZP75a",
    "related_object": {
      "id": "pi_1QA8PKDTvO5jCVb3TVDZP75a",
      "type": "payment_intent",
      "url": "https://dashboard.stripe.com/payment_intents/pi_1QA8PKDTvO5jCVb3TVDZP75a"
    },
  },
  "resolved_at": "2025-10-30T16:05:44.000Z",
  "summary": "We have failed to create a notification for your Stripe account.",
}
```

Example 2 (unknown):
```unknown
{
  "alert_id": "halert_61RFBMa6o6H87usts16RFBM10hSQlYfddqcFoEMR6CPY",
  "grouping_key": "_grouping_s8PgTvizbkORV9z5PhaJSvc4dUcAMmfRpEHKm4EeJ1glsQ5XMf",
  "impact": {
    "event_type": "payment_intent.requires_action",
    "related_object_id": "pi_1QA8PKDTvO5jCVb3TVDZP75a",
    "related_object": {
      "id": "pi_1QA8PKDTvO5jCVb3TVDZP75a",
      "type": "payment_intent",
      "url": "https://dashboard.stripe.com/payment_intents/pi_1QA8PKDTvO5jCVb3TVDZP75a"
    },
  },
  "resolved_at": "2025-10-30T16:05:44.000Z",
  "summary": "We have failed to create a notification for your Stripe account.",
}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents/pi_1QA8PKDTvO5jCVb3TVDZP75a \
  -u "sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents/pi_1QA8PKDTvO5jCVb3TVDZP75a \
  -u "sk_test_YOUR_TEST_KEY_HERE:"
```

---

## List all events

**URL:** https://docs.stripe.com/api/events/list

**Contents:**
- List all events
  - Parameters
    - typesarray of strings
  - More parametersExpand all
    - createdobject
    - delivery_successboolean
    - ending_beforestring
    - limitinteger
    - starting_afterstring
    - typestring

List events, going back up to 30 days. Each event data is rendered according to Stripe API version at its creation time, specified in event object api_version attribute (not according to your current Stripe API version or Stripe-Version header).

An array of up to 20 strings containing specific event names. The list will be filtered to include only events with a matching event property. You may pass either type or types, but not both.

A dictionary with a data property that contains an array of up to limit events, starting after event starting_after. Each entry in the array is a separate event object. If no more events are available, the resulting array will be empty.

This is a list of all public snapshot events we currently send for /v1 resources, which is continually evolving and expanding.

Stripe events use the resource.event naming convention. Events that occur on subresources like customer.subscription.updated don’t trigger a corresponding event for the parent resource (customer.updated).

Stripe creates event types marked as Selection required only when at least one webhook is listening for it. A webhook set to listen to all events doesn’t satisfy this requirement and won’t generate Selection required event types.

Occurs whenever a user authorizes an application. Sent to the related application only.

Occurs whenever a user deauthorizes an application. Sent to the related application only.

Occurs whenever an external account is created.

Occurs whenever an external account is deleted.

Occurs whenever an external account is updated.

Occurs whenever an account status or property has changed.

Occurs whenever an application fee is created on a charge.

Occurs whenever an application fee refund is updated.

Occurs whenever an application fee is refunded, whether from refunding a charge or from refunding the application fee directly. This includes partial refunds.

Occurs whenever a balance settings status or property has changed.

Occurs whenever your Stripe balance has been updated (e.g., when a charge is available to be paid out). By default, Stripe automatically transfers funds in your balance to your bank account on a daily basis. This event is not fired for negative transactions.

Occurs whenever a portal configuration is created.

Occurs whenever a portal configuration is updated.

Occurs whenever a portal session is created.

Occurs whenever your custom alert threshold is met.

Occurs when a credit balance transaction is created

Occurs when a credit grant is created

Occurs when a credit grant is updated

Occurs when a meter is created

Occurs when a meter is deactivated

Occurs when a meter is reactivated

Occurs when a meter is updated

Occurs whenever a capability has new requirements or a new status.

Occurs whenever there is a positive remaining cash balance after Stripe automatically reconciles new funds into the cash balance. If you enabled manual reconciliation, this webhook will fire whenever there are new funds into the cash balance.

Occurs whenever a previously uncaptured charge is captured.

Occurs when a dispute is closed and the dispute status changes to lost, warning_closed, or won.

Occurs whenever a customer disputes a charge with their bank.

Occurs when funds are reinstated to your account after a dispute is closed. This includes partially refunded payments.

Occurs when funds are removed from your account due to a dispute.

Occurs when the dispute is updated (usually with evidence).

Occurs whenever an uncaptured charge expires.

Occurs whenever a failed charge attempt occurs.

Occurs whenever a pending charge is created.

Occurs whenever a refund is updated on selected payment methods. For updates on all refunds, listen to refund.updated instead.

Occurs whenever a charge is refunded, including partial refunds. Listen to refund.created for information about the refund.

Occurs whenever a charge is successful.

Occurs whenever a charge description or metadata is updated, or upon an asynchronous capture.

Occurs when a payment intent using a delayed payment method fails.

Occurs when a payment intent using a delayed payment method finally succeeds.

Occurs when a Checkout Session has been successfully completed.

Occurs when a Checkout Session is expired.

Occurs when a Climate order is canceled.

Occurs when a Climate order is created.

Occurs when a Climate order is delayed.

Occurs when a Climate order is delivered.

Occurs when a Climate order’s product is substituted for another.

Occurs when a Climate product is created.

Occurs when a Climate product is updated.

Occurs whenever a coupon is created.

Occurs whenever a coupon is deleted.

Occurs whenever a coupon is updated.

Occurs whenever a credit note is created.

Occurs whenever a credit note is updated.

Occurs whenever a credit note is voided.

Occurs whenever a new customer cash balance transactions is created.

Occurs whenever a new customer is created.

Occurs whenever a customer is deleted.

Occurs whenever a coupon is attached to a customer.

Occurs whenever a coupon is removed from a customer.

Occurs whenever a customer is switched from one coupon to another.

Occurs whenever a new source is created for a customer.

Occurs whenever a source is removed from a customer.

Occurs whenever a card or source will expire at the end of the month. This event only works with legacy integrations using Card or Source objects. If you use the PaymentMethod API, this event won’t occur.

Occurs whenever a source’s details are changed.

Occurs whenever a customer is signed up for a new plan.

Occurs whenever a customer’s subscription ends.

Occurs whenever a customer’s subscription is paused. Only applies when subscriptions enter status=paused, not when payment collection is paused.

Occurs whenever a customer’s subscription’s pending update is applied, and the subscription is updated.

Occurs whenever a customer’s subscription’s pending update expires before the related invoice is paid.

Occurs whenever a customer’s subscription is no longer paused. Only applies when a status=paused subscription is resumed, not when payment collection is resumed.

Occurs three days before a subscription’s trial period is scheduled to end, or when a trial is ended immediately (using trial_end=now).

Occurs whenever a subscription changes (e.g., switching from one plan to another, or changing the status from trial to active).

Occurs whenever a tax ID is created for a customer.

Occurs whenever a tax ID is deleted from a customer.

Occurs whenever a customer’s tax ID is updated.

Occurs whenever any property of a customer changes.

Occurs whenever a customer’s entitlements change.

Occurs whenever a new Stripe-generated file is available for your account.

Occurs when a Financial Connections account’s account numbers are updated.

Occurs when a new Financial Connections account is created.

Occurs when a Financial Connections account’s status is updated from active to inactive.

Occurs when a Financial Connections account is disconnected.

Occurs when a Financial Connections account’s status is updated from inactive to active.

Occurs when an Account’s balance_refresh status transitions from pending to either succeeded or failed.

Occurs when an Account’s ownership_refresh status transitions from pending to either succeeded or failed.

Occurs when an Account’s transaction_refresh status transitions from pending to either succeeded or failed.

Occurs when an Account’s tokenized account number is about to expire.

Occurs whenever a VerificationSession is canceled

Occurs whenever a VerificationSession is created

Occurs whenever a VerificationSession transitions to processing

Occurs whenever a VerificationSession is redacted.

Occurs whenever a VerificationSession transitions to require user input

Occurs whenever a VerificationSession transitions to verified

Occurs when an InvoicePayment is successfully paid.

Occurs whenever a new invoice is created. To learn how webhooks can be used with this event, and how they can affect it, see Using Webhooks with Subscriptions.

Occurs whenever a draft invoice is deleted. Note: This event is not sent for invoice previews.

Occurs whenever a draft invoice cannot be finalized. See the invoice’s last finalization error for details.

Occurs whenever a draft invoice is finalized and updated to be an open invoice.

Occurs whenever an invoice is marked uncollectible.

Occurs X number of days after an invoice becomes due—where X is determined by Automations

Occurs when an invoice transitions to paid with a non-zero amount_overpaid.

Occurs whenever an invoice payment attempt succeeds or an invoice is marked as paid out-of-band.

Occurs whenever an invoice payment attempt requires further user action to complete.

Occurs when an invoice requires a payment using a payment method that cannot be processed by Stripe.

Occurs whenever an invoice payment attempt fails, due to either a declined payment, including soft decline, or to the lack of a stored payment method.

Occurs whenever an invoice payment attempt succeeds.

Occurs whenever an invoice email is sent out.

Occurs X number of days before a subscription is scheduled to create an invoice that is automatically charged—where X is determined by your subscriptions settings. Note: The received Invoice object will not have an invoice ID.

Occurs whenever an invoice changes (e.g., the invoice amount).

Occurs whenever an invoice is voided.

Occurs X number of days before an invoice becomes due—where X is determined by Automations

Occurs whenever an invoice item is created.

Occurs whenever an invoice item is deleted.

Occurs whenever an authorization is created.

Represents a synchronous request for authorization, see Using your integration to handle authorization requests.

Occurs whenever an authorization is updated.

Occurs whenever a card is created.

Occurs whenever a card is updated.

Occurs whenever a cardholder is created.

Occurs whenever a cardholder is updated.

Occurs whenever a dispute is won, lost or expired.

Occurs whenever a dispute is created.

Occurs whenever funds are reinstated to your account for an Issuing dispute.

Occurs whenever funds are deducted from your account for an Issuing dispute.

Occurs whenever a dispute is submitted.

Occurs whenever a dispute is updated.

Occurs whenever a personalization design is activated following the activation of the physical bundle that belongs to it.

Occurs whenever a personalization design is deactivated following the deactivation of the physical bundle that belongs to it.

Occurs whenever a personalization design is rejected by design review.

Occurs whenever a personalization design is updated.

Occurs whenever an issuing digital wallet token is created.

Occurs whenever an issuing digital wallet token is updated.

Occurs whenever an issuing transaction is created.

Occurs whenever an issuing transaction is updated with receipt data.

Occurs whenever an issuing transaction is updated.

Occurs whenever a Mandate is updated.

Occurs when a PaymentIntent has funds to be captured. Check the amount_capturable property on the PaymentIntent to determine the amount that can be captured. You may capture the PaymentIntent with an amount_to_capture value up to the specified amount. Learn more about capturing PaymentIntents.

Occurs when a PaymentIntent is canceled.

Occurs when a new PaymentIntent is created.

Occurs when funds are applied to a customer_balance PaymentIntent and the ‘amount_remaining’ changes.

Occurs when a PaymentIntent has failed the attempt to create a payment method or a payment.

Occurs when a PaymentIntent has started processing.

Occurs when a PaymentIntent transitions to requires_action state

Occurs when a PaymentIntent has successfully completed payment.

Occurs when a payment link is created.

Occurs when a payment link is updated.

Occurs whenever a new payment method is attached to a customer.

Occurs whenever a payment method’s details are automatically updated by the network.

Occurs whenever a payment method is detached from a customer.

Occurs whenever a payment method is updated via the PaymentMethod update API.

Occurs whenever a payout is canceled.

Occurs whenever a payout is created.

Occurs whenever a payout attempt fails.

Occurs whenever a payout is expected to be available in the destination account. If the payout fails, a payout.failed notification is also sent, at a later time.

Occurs whenever balance transactions paid out in an automatic payout can be queried.

Occurs whenever a payout is updated.

Occurs whenever a person associated with an account is created.

Occurs whenever a person associated with an account is deleted.

Occurs whenever a person associated with an account is updated.

Occurs whenever a plan is created.

Occurs whenever a plan is deleted.

Occurs whenever a plan is updated.

Occurs whenever a price is created.

Occurs whenever a price is deleted.

Occurs whenever a price is updated.

Occurs whenever a product is created.

Occurs whenever a product is deleted.

Occurs whenever a product is updated.

Occurs whenever a promotion code is created.

Occurs whenever a promotion code is updated.

Occurs whenever a quote is accepted.

Occurs whenever a quote is canceled.

Occurs whenever a quote is created.

Occurs whenever a quote is finalized.

Occurs X number of days before a quote is scheduled to expire—where X is determined by Automations

Occurs whenever an early fraud warning is created.

Occurs whenever an early fraud warning is updated.

Occurs whenever a refund is created.

Occurs whenever a refund has failed.

Occurs whenever a refund is updated.

Occurs whenever a requested ReportRun failed to complete.

Occurs whenever a requested ReportRun completed successfully.

Occurs whenever a ReportType is updated (typically to indicate that a new day’s data has come available).

Occurs whenever a review is closed. The review’s reason field indicates why: approved, disputed, refunded, refunded_as_fraud, or canceled.

Occurs whenever a review is opened.

Occurs when a SetupIntent is canceled.

Occurs when a new SetupIntent is created.

Occurs when a SetupIntent is in requires_action state.

Occurs when a SetupIntent has failed the attempt to setup a payment method.

Occurs when an SetupIntent has successfully setup a payment method.

Occurs whenever a Sigma scheduled query run finishes.

Occurs whenever a source is canceled.

Occurs whenever a source transitions to chargeable.

Occurs whenever a source fails.

Occurs whenever a source mandate notification method is set to manual.

Occurs whenever the refund attributes are required on a receiver source to process a refund or a mispayment.

Occurs whenever a source transaction is created.

Occurs whenever a source transaction is updated.

Occurs whenever a subscription schedule is canceled due to the underlying subscription being canceled because of delinquency.

Occurs whenever a subscription schedule is canceled.

Occurs whenever a new subscription schedule is completed.

Occurs whenever a new subscription schedule is created.

Occurs 7 days before a subscription schedule will expire.

Occurs whenever a new subscription schedule is released.

Occurs whenever a subscription schedule is updated.

Occurs whenever a new tax rate is created.

Occurs whenever a tax rate is updated.

Occurs whenever tax settings is updated.

Occurs whenever an action sent to a Terminal reader failed.

Occurs whenever an action sent to a Terminal reader was successful.

Occurs whenever an action sent to a Terminal reader is updated.

Occurs whenever a test clock starts advancing.

Occurs whenever a test clock is created.

Occurs whenever a test clock is deleted.

Occurs whenever a test clock fails to advance its frozen time.

Occurs whenever a test clock transitions to a ready status.

Occurs whenever a top-up is canceled.

Occurs whenever a top-up is created.

Occurs whenever a top-up fails.

Occurs whenever a top-up is reversed.

Occurs whenever a top-up succeeds.

Occurs whenever a transfer is created.

Occurs whenever a transfer is reversed, including partial reversals.

Occurs whenever a transfer’s description or metadata is updated.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v1/events \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v1/events \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 3 (unknown):
```unknown
{  "object": "list",  "url": "/v1/events",  "has_more": false,  "data": [    {      "id": "evt_1NG8Du2eZvKYlo2CUI79vXWy",      "object": "event",      "api_version": "2019-02-19",      "created": 1686089970,      "data": {        "object": {          "id": "seti_1NG8Du2eZvKYlo2C9XMqbR0x",          "object": "setup_intent",          "application": null,          "automatic_payment_methods": null,          "cancellation_reason": null,          "client_secret": "seti_1NG8Du2eZvKYlo2C9XMqbR0x_secret_O2CdhLwGFh2Aej7bCY7qp8jlIuyR8DJ",          "created": 1686089970,          "customer": null,          "description": null,          "flow_directions": null,          "last_setup_error": null,          "latest_attempt": null,          "livemode": false,          "mandate": null,          "metadata": {},          "next_action": null,          "on_behalf_of": null,          "payment_method": "pm_1NG8Du2eZvKYlo2CYzzldNr7",          "payment_method_options": {            "acss_debit": {              "currency": "cad",              "mandate_options": {                "interval_description": "First day of every month",                "payment_schedule": "interval",                "transaction_type": "personal"              },              "verification_method": "automatic"            }          },          "payment_method_types": [            "acss_debit"          ],          "single_use_mandate": null,          "status": "requires_confirmation",          "usage": "off_session"        }      },      "livemode": false,      "pending_webhooks": 0,      "request": {        "id": null,        "idempotency_key": null      },      "type": "setup_intent.created"    }  ]}
```

Example 4 (unknown):
```unknown
{  "object": "list",  "url": "/v1/events",  "has_more": false,  "data": [    {      "id": "evt_1NG8Du2eZvKYlo2CUI79vXWy",      "object": "event",      "api_version": "2019-02-19",      "created": 1686089970,      "data": {        "object": {          "id": "seti_1NG8Du2eZvKYlo2C9XMqbR0x",          "object": "setup_intent",          "application": null,          "automatic_payment_methods": null,          "cancellation_reason": null,          "client_secret": "seti_1NG8Du2eZvKYlo2C9XMqbR0x_secret_O2CdhLwGFh2Aej7bCY7qp8jlIuyR8DJ",          "created": 1686089970,          "customer": null,          "description": null,          "flow_directions": null,          "last_setup_error": null,          "latest_attempt": null,          "livemode": false,          "mandate": null,          "metadata": {},          "next_action": null,          "on_behalf_of": null,          "payment_method": "pm_1NG8Du2eZvKYlo2CYzzldNr7",          "payment_method_options": {            "acss_debit": {              "currency": "cad",              "mandate_options": {                "interval_description": "First day of every month",                "payment_schedule": "interval",                "transaction_type": "personal"              },              "verification_method": "automatic"            }          },          "payment_method_types": [            "acss_debit"          ],          "single_use_mandate": null,          "status": "requires_confirmation",          "usage": "off_session"        }      },      "livemode": false,      "pending_webhooks": 0,      "request": {        "id": null,        "idempotency_key": null      },      "type": "setup_intent.created"    }  ]}
```

---

## Ping an event destination v2

**URL:** https://docs.stripe.com/api/v2/core/events/ping

**Contents:**
- Ping an event destination v2
  - Parameters
    - idstringRequired
  - Returns
  - Response attributes
    - idstring
    - objectstring, value is "v2.core.event"
    - changesnullable object
    - contextnullable string
    - createdtimestamp

Send a ping event to an event destination.

Identifier for the event destination to ping.

Unique identifier for the event.

String representing the object’s type. Objects of the same type share the same value of the object field.

Before and after changes for the primary related object.

Authentication context needed to fetch the event or related object.

Time at which the object was created.

Additional data about the event.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Reason for the event.

Object containing the reference to API resource relevant to the event.

The type of the event.

The resource wasn’t found.

This is a list of all public thin events we currently send for /v1 and /v2 resources, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/event_destinations/evt_test_65RM8sQH2oXnebF5Rpc16RJyfa2xSQLHJJh1sxm7H0KI92/ping \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/event_destinations/evt_test_65RM8sQH2oXnebF5Rpc16RJyfa2xSQLHJJh1sxm7H0KI92/ping \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 3 (unknown):
```unknown
{  "id": "evt_test_65RM8sQH2oXnebF5Rpc16RJyfa2xSQLHJJh1sxm7H0KI92",  "object": "v2.core.event",  "context": null,  "created": "2024-10-22T16:26:54.063Z",  "data": null,  "livemode": false,  "reason": null,  "related_object": {    "id": "ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6",    "type": "event_destination",    "url": "/v2/core/event_destinations/ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6"  },  "type": "v2.core.event_destination.ping"}
```

Example 4 (unknown):
```unknown
{  "id": "evt_test_65RM8sQH2oXnebF5Rpc16RJyfa2xSQLHJJh1sxm7H0KI92",  "object": "v2.core.event",  "context": null,  "created": "2024-10-22T16:26:54.063Z",  "data": null,  "livemode": false,  "reason": null,  "related_object": {    "id": "ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6",    "type": "event_destination",    "url": "/v2/core/event_destinations/ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6"  },  "type": "v2.core.event_destination.ping"}
```

---

## Use the API to respond to disputes

**URL:** https://docs.stripe.com/disputes/api

**Contents:**
- Use the API to respond to disputes
- Learn how to manage disputes programmatically.
- Retrieve a dispute
- Update a dispute
    - Note
- Multiple disputes on a single payment
- See also

You can programmatically manage disputes using the API. With the API, you can upload evidence, respond to disputes, and receive dispute events using webhooks.

If you want to manage disputes using the Dashboard instead of using the API, see Respond to disputes.

For details about a dispute, retrieve a Dispute object:

The response contains information about the dispute and any response or evidence that’s already been provided.

You update the Dispute object and pass structured evidence with the evidence parameter.

To view all available fields for the evidence parameter, see Dispute evidence. There are two types of evidence you can provide, depending on the field being updated:

The combined character count for all text-based evidence field submissions is limited to 150,000.

You can provide documents or images (for example, a contract or screenshot) as part of dispute evidence using the File Upload API. You first upload a document with the purpose of dispute_evidence, which generates a File_upload object that you can use when submitting evidence. Make sure the file meets Stripe’s recommendations before uploading it for evidence submission.

If you’re only interested in submitting a single file or a large amount of plaintext as evidence, use uncategorized_text or uncategorized_file. However, fill in as many fields as possible so you have the best chance at overturning a dispute.

It’s not typical, but it’s possible for a customer to dispute the same payment more than once. For example, a customer might partially dispute a payment for one of the items in an order if it was damaged in delivery, and then file a second dispute against a different item in the same order because the item didn’t work properly.

Stripe distinguishes all disputes by a unique identifier, regardless of whether they’re related to a single payment. When you list disputes, you can filter the results to show only disputes for a particular payment by specifying the id of the PaymentIntent or Charge object and including the payment_intent or charge filter.

When a payment has multiple disputes, use the id provided for each returned dispute in the list to make sure you’re responding to the correct dispute by specifying its id when you retrieve or update the dispute.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/disputes/{{DISPUTE_ID}} \
  -u "sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/disputes/{{DISPUTE_ID}} \
  -u "sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{
  object: "dispute"
  id: "{{DISPUTE_ID}}",
  charge: "ch_5Q4BjL06oPWwho",
  evidence: {
    customer_name: "Jane Austen",
    customer_purchase_ip: "127.0.0.1",
    product_description: "Widget ABC, color: red",
    shipping_tracking_number: "Z01234567890",
    uncategorized_text: "Additional notes and comments",
  },
  evidence_details: {
    due_by: 1403047735,
    submission_count: 1
  }
  ...
}
```

Example 4 (unknown):
```unknown
{
  object: "dispute"
  id: "{{DISPUTE_ID}}",
  charge: "ch_5Q4BjL06oPWwho",
  evidence: {
    customer_name: "Jane Austen",
    customer_purchase_ip: "127.0.0.1",
    product_description: "Widget ABC, color: red",
    shipping_tracking_number: "Z01234567890",
    uncategorized_text: "Additional notes and comments",
  },
  evidence_details: {
    due_by: 1403047735,
    submission_count: 1
  }
  ...
}
```

---

## Process incoming webhooks with event notification handlersPublic preview

**URL:** https://docs.stripe.com/webhooks/event-notification-handlers

**Contents:**
- Process incoming webhooks with event notification handlersPublic preview
    - Public preview
- Before you begin
- Write a fallback callback
- Initialize your handler
- Write & register a callback
- Process events
- See also

Event notification handlers are available in public preview.

This feature doesn’t support event destinations that use EventBridge in public preview.

In each of our SDKs, we’ve created a specialized class that encapsulates the mechanics of parsing and validating a Stripe webhook. Event notification handlers take care of validating, parsing, and routing incoming webhooks to your business logic.

To use this feature, you must write a function for each event type you want to handle. After you register these functions on the handler, Stripe will call them when you receive the corresponding event notification.

You must use the following SDK version (or higher) to use event notification handlers.

Write a function that runs whenever a dedicated callback hasn’t been registered for a specific event type. It will receive the EventNotification, plus a StripeClient and additional information about the event.

This function might log the fact that you received an unexpected event or throw an error to alert you to the unexpected state. You can also add business logic in this function if you’re handling events that your SDK doesn’t have types for.

As part of your migration, consider moving all of your webhook endpoint code into this function. Then, you can migrate individual event types to their own functions.

In your webhook endpoint, initialize an EventNotificationHandler, passing it your fallback callback. There’s a convenience method on StripeClient to simplify this step.

Next, write a function responsible for handling a specific event type. It uses the event types released with the Clover API version in September 2025.

Your callback will receive the event notification cast to the correct class. You’ll also get a StripeClient, bound to the context of the notification, which makes it easy to make additional API calls without juggling account ids.

You can register zero or more callbacks. If you don’t register any, all events will be routed to your fallback callback.

Send incoming POST bodies into the handler. This replaces most of the original code in your webhook endpoint.

**Examples:**

Example 1 (python):
```python
def fallback_callback(notif: EventNotification, client: StripeClient, details: UnhandledNotificationDetails):
    print(f'Got an unhandled event of type {notif.type}!')
```

Example 2 (python):
```python
def fallback_callback(notif: EventNotification, client: StripeClient, details: UnhandledNotificationDetails):
    print(f'Got an unhandled event of type {notif.type}!')
```

Example 3 (unknown):
```unknown
client = StripeClient(api_key)
handler = client.notification_handler(webhook_secret, fallback_callback)
```

Example 4 (unknown):
```unknown
client = StripeClient(api_key)
handler = client.notification_handler(webhook_secret, fallback_callback)
```

---

## Handle payment events with webhooks

**URL:** https://docs.stripe.com/webhooks/handling-payment-events

**Contents:**
- Handle payment events with webhooks
- How to use webhooks to respond to offline payment events.
- Build your own webhook
- Create a webhook endpoint
- Install and set up the Stripe CLI
    - Note
- Test your webhook locally
- OptionalCheck webhook signature
- Deploy your webhook endpoint

A webhook is an HTTP endpoint that receives events from Stripe.

Webhooks allow you to be notified about payment events that happen outside of your payment flow such as:

You can use the Dashboard for one-off actions like refunding a payment or updating a customer’s information, while webhooks help you scale your payments integration and process large volumes of business-critical events.

You can build a webhook handler on your own server to manage all your offline payment flows. Start by exposing an endpoint that can receive requests from Stripe and use the CLI to locally test your integration. Each request from Stripe contains an Event object with a reference to the object on Stripe that was modified.

Add a new endpoint in your application. You can act on certain events by checking the type field of the event object sent in the request body. Then you can print to standard output to make sure your webhook is working.

Start your server after adding the new endpoint.

For additional install options, see Get started with the Stripe CLI.

After you have the Stripe CLI installed, run stripe login in the command line to generate a pairing code to link to your Stripe account. Press Enter to launch your browser and log in to your Stripe account to allow access. The generated API key is valid for 90 days. You can modify or delete the key under API Keys in the Dashboard.

You can create a project-specific configuration by including the –project-name flag when you log in and when you run commands for that project.

If you want to use an existing API key, use the --api-key flag:

Use the CLI to forward events to your local webhook endpoint using the listen command.

Assuming your application is running on port 4242, run:

In a different terminal tab, use the trigger CLI command to trigger a mock webhook event.

The following event appears in your listen tab:

“PaymentIntent was successful!” appears in the terminal tab your server is running.

When you’re ready to deploy your webhook endpoint to production you need to do the following:

Your application is now ready to accept live events. For more information on configuring your webhook endpoint, see the Webhook Endpoint API. For testing in a sandbox, see our Development guide.

**Examples:**

Example 1 (javascript):
```javascript
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
Stripe.api_key = 'sk_test_YOUR_TEST_KEY_HERE'

require 'stripe'
require 'sinatra'
require 'json'

# Using the Sinatra framework
set :port, 4242

post '/webhook' do
  payload = request.body.read
  event = nil

  begin
    event = Stripe::Event.construct_from(
      JSON.parse(payload, symbolize_names: true)
    )
  rescue JSON::ParserError => e
    # Invalid payload
    status 400
    return
  end

  # Handle the event
  case event.type
  when 'payment_intent.succeeded'
    payment_intent = event.data.object # contains a Stripe::PaymentIntent
    puts 'PaymentIntent was successful!'
  when 'payment_method.attached'
    payment_method = event.data.object # contains a Stripe::PaymentMethod
    puts 'PaymentMethod was attached to a Customer!'
  # ... handle other event types
  else
    puts "Unhandled event type: #{event.type}"
  end

  status 200
end
```

Example 2 (javascript):
```javascript
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
Stripe.api_key = 'sk_test_YOUR_TEST_KEY_HERE'

require 'stripe'
require 'sinatra'
require 'json'

# Using the Sinatra framework
set :port, 4242

post '/webhook' do
  payload = request.body.read
  event = nil

  begin
    event = Stripe::Event.construct_from(
      JSON.parse(payload, symbolize_names: true)
    )
  rescue JSON::ParserError => e
    # Invalid payload
    status 400
    return
  end

  # Handle the event
  case event.type
  when 'payment_intent.succeeded'
    payment_intent = event.data.object # contains a Stripe::PaymentIntent
    puts 'PaymentIntent was successful!'
  when 'payment_method.attached'
    payment_method = event.data.object # contains a Stripe::PaymentMethod
    puts 'PaymentMethod was attached to a Customer!'
  # ... handle other event types
  else
    puts "Unhandled event type: #{event.type}"
  end

  status 200
end
```

Example 3 (unknown):
```unknown
# Install Homebrew to run this command: https://brew.sh/
brew install stripe/stripe-cli/stripe

# Connect the CLI to your dashboard
stripe login
```

Example 4 (unknown):
```unknown
# Install Homebrew to run this command: https://brew.sh/
brew install stripe/stripe-cli/stripe

# Connect the CLI to your dashboard
stripe login
```

---

## Events

**URL:** https://docs.stripe.com/api/events

**Contents:**
- Events
- The Event object
  - Attributes
    - idstring
    - api_versionnullable string
    - dataobject
    - requestnullable object
    - typestring
  - More attributesExpand all
    - objectstring

Snapshot events allow you to track and react to activity in your Stripe integration. When the state of another API resource changes, Stripe creates an Event object that contains all the relevant information associated with that action, including the affected API resource. For example, a successful payment triggers a charge.succeeded event, which contains the Charge in the event’s data property. Some actions trigger multiple events. For example, if you create a new subscription for a customer, it triggers both a customer.subscription.created event and a charge.succeeded event.

Configure an event destination in your account to listen for events that represent actions your integration needs to respond to. Additionally, you can retrieve an individual event or a list of events from the API.

Connect platforms can also receive event notifications that occur in their connected accounts. These events include an account attribute that identifies the relevant connected account.

You can access events through the Retrieve Event API for 30 days.

Unique identifier for the object.

The Stripe API version used to render data when the event was created. The contents of data never change, so this value remains static regardless of the API version currently in use. This property is populated only for events created on or after October 31, 2014.

Object containing data associated with the event.

Information on the API request that triggers the event.

Description of the event (for example, invoice.created or charge.refunded).

Retrieves the details of an event if it was created in the last 30 days. Supply the unique identifier of the event, which you might have received in a webhook.

Returns an event object if a valid identifier was provided. All events share a common structure, detailed to the right. The only property that will differ is the data property.

In each case, the data dictionary will have an attribute called object and its value will be the same as retrieving the same object directly from the API. For example, a customer.created event will have the same information as retrieving the relevant customer would.

In cases where the attributes of an object have changed, data will also contain a dictionary containing the changes.

List events, going back up to 30 days. Each event data is rendered according to Stripe API version at its creation time, specified in event object api_version attribute (not according to your current Stripe API version or Stripe-Version header).

An array of up to 20 strings containing specific event names. The list will be filtered to include only events with a matching event property. You may pass either type or types, but not both.

A dictionary with a data property that contains an array of up to limit events, starting after event starting_after. Each entry in the array is a separate event object. If no more events are available, the resulting array will be empty.

This is a list of all public snapshot events we currently send for /v1 resources, which is continually evolving and expanding.

Stripe events use the resource.event naming convention. Events that occur on subresources like customer.subscription.updated don’t trigger a corresponding event for the parent resource (customer.updated).

Stripe creates event types marked as Selection required only when at least one webhook is listening for it. A webhook set to listen to all events doesn’t satisfy this requirement and won’t generate Selection required event types.

Occurs whenever a user authorizes an application. Sent to the related application only.

Occurs whenever a user deauthorizes an application. Sent to the related application only.

Occurs whenever an external account is created.

Occurs whenever an external account is deleted.

Occurs whenever an external account is updated.

Occurs whenever an account status or property has changed.

Occurs whenever an application fee is created on a charge.

Occurs whenever an application fee refund is updated.

Occurs whenever an application fee is refunded, whether from refunding a charge or from refunding the application fee directly. This includes partial refunds.

Occurs whenever a balance settings status or property has changed.

Occurs whenever your Stripe balance has been updated (e.g., when a charge is available to be paid out). By default, Stripe automatically transfers funds in your balance to your bank account on a daily basis. This event is not fired for negative transactions.

Occurs whenever a portal configuration is created.

Occurs whenever a portal configuration is updated.

Occurs whenever a portal session is created.

Occurs whenever your custom alert threshold is met.

Occurs when a credit balance transaction is created

Occurs when a credit grant is created

Occurs when a credit grant is updated

Occurs when a meter is created

Occurs when a meter is deactivated

Occurs when a meter is reactivated

Occurs when a meter is updated

Occurs whenever a capability has new requirements or a new status.

Occurs whenever there is a positive remaining cash balance after Stripe automatically reconciles new funds into the cash balance. If you enabled manual reconciliation, this webhook will fire whenever there are new funds into the cash balance.

Occurs whenever a previously uncaptured charge is captured.

Occurs when a dispute is closed and the dispute status changes to lost, warning_closed, or won.

Occurs whenever a customer disputes a charge with their bank.

Occurs when funds are reinstated to your account after a dispute is closed. This includes partially refunded payments.

Occurs when funds are removed from your account due to a dispute.

Occurs when the dispute is updated (usually with evidence).

Occurs whenever an uncaptured charge expires.

Occurs whenever a failed charge attempt occurs.

Occurs whenever a pending charge is created.

Occurs whenever a refund is updated on selected payment methods. For updates on all refunds, listen to refund.updated instead.

Occurs whenever a charge is refunded, including partial refunds. Listen to refund.created for information about the refund.

Occurs whenever a charge is successful.

Occurs whenever a charge description or metadata is updated, or upon an asynchronous capture.

Occurs when a payment intent using a delayed payment method fails.

Occurs when a payment intent using a delayed payment method finally succeeds.

Occurs when a Checkout Session has been successfully completed.

Occurs when a Checkout Session is expired.

Occurs when a Climate order is canceled.

Occurs when a Climate order is created.

Occurs when a Climate order is delayed.

Occurs when a Climate order is delivered.

Occurs when a Climate order’s product is substituted for another.

Occurs when a Climate product is created.

Occurs when a Climate product is updated.

Occurs whenever a coupon is created.

Occurs whenever a coupon is deleted.

Occurs whenever a coupon is updated.

Occurs whenever a credit note is created.

Occurs whenever a credit note is updated.

Occurs whenever a credit note is voided.

Occurs whenever a new customer cash balance transactions is created.

Occurs whenever a new customer is created.

Occurs whenever a customer is deleted.

Occurs whenever a coupon is attached to a customer.

Occurs whenever a coupon is removed from a customer.

Occurs whenever a customer is switched from one coupon to another.

Occurs whenever a new source is created for a customer.

Occurs whenever a source is removed from a customer.

Occurs whenever a card or source will expire at the end of the month. This event only works with legacy integrations using Card or Source objects. If you use the PaymentMethod API, this event won’t occur.

Occurs whenever a source’s details are changed.

Occurs whenever a customer is signed up for a new plan.

Occurs whenever a customer’s subscription ends.

Occurs whenever a customer’s subscription is paused. Only applies when subscriptions enter status=paused, not when payment collection is paused.

Occurs whenever a customer’s subscription’s pending update is applied, and the subscription is updated.

Occurs whenever a customer’s subscription’s pending update expires before the related invoice is paid.

Occurs whenever a customer’s subscription is no longer paused. Only applies when a status=paused subscription is resumed, not when payment collection is resumed.

Occurs three days before a subscription’s trial period is scheduled to end, or when a trial is ended immediately (using trial_end=now).

Occurs whenever a subscription changes (e.g., switching from one plan to another, or changing the status from trial to active).

Occurs whenever a tax ID is created for a customer.

Occurs whenever a tax ID is deleted from a customer.

Occurs whenever a customer’s tax ID is updated.

Occurs whenever any property of a customer changes.

Occurs whenever a customer’s entitlements change.

Occurs whenever a new Stripe-generated file is available for your account.

Occurs when a Financial Connections account’s account numbers are updated.

Occurs when a new Financial Connections account is created.

Occurs when a Financial Connections account’s status is updated from active to inactive.

Occurs when a Financial Connections account is disconnected.

Occurs when a Financial Connections account’s status is updated from inactive to active.

Occurs when an Account’s balance_refresh status transitions from pending to either succeeded or failed.

Occurs when an Account’s ownership_refresh status transitions from pending to either succeeded or failed.

Occurs when an Account’s transaction_refresh status transitions from pending to either succeeded or failed.

Occurs when an Account’s tokenized account number is about to expire.

Occurs whenever a VerificationSession is canceled

Occurs whenever a VerificationSession is created

Occurs whenever a VerificationSession transitions to processing

Occurs whenever a VerificationSession is redacted.

Occurs whenever a VerificationSession transitions to require user input

Occurs whenever a VerificationSession transitions to verified

Occurs when an InvoicePayment is successfully paid.

Occurs whenever a new invoice is created. To learn how webhooks can be used with this event, and how they can affect it, see Using Webhooks with Subscriptions.

Occurs whenever a draft invoice is deleted. Note: This event is not sent for invoice previews.

Occurs whenever a draft invoice cannot be finalized. See the invoice’s last finalization error for details.

Occurs whenever a draft invoice is finalized and updated to be an open invoice.

Occurs whenever an invoice is marked uncollectible.

Occurs X number of days after an invoice becomes due—where X is determined by Automations

Occurs when an invoice transitions to paid with a non-zero amount_overpaid.

Occurs whenever an invoice payment attempt succeeds or an invoice is marked as paid out-of-band.

Occurs whenever an invoice payment attempt requires further user action to complete.

Occurs when an invoice requires a payment using a payment method that cannot be processed by Stripe.

Occurs whenever an invoice payment attempt fails, due to either a declined payment, including soft decline, or to the lack of a stored payment method.

Occurs whenever an invoice payment attempt succeeds.

Occurs whenever an invoice email is sent out.

Occurs X number of days before a subscription is scheduled to create an invoice that is automatically charged—where X is determined by your subscriptions settings. Note: The received Invoice object will not have an invoice ID.

Occurs whenever an invoice changes (e.g., the invoice amount).

Occurs whenever an invoice is voided.

Occurs X number of days before an invoice becomes due—where X is determined by Automations

Occurs whenever an invoice item is created.

Occurs whenever an invoice item is deleted.

Occurs whenever an authorization is created.

Represents a synchronous request for authorization, see Using your integration to handle authorization requests.

Occurs whenever an authorization is updated.

Occurs whenever a card is created.

Occurs whenever a card is updated.

Occurs whenever a cardholder is created.

Occurs whenever a cardholder is updated.

Occurs whenever a dispute is won, lost or expired.

Occurs whenever a dispute is created.

Occurs whenever funds are reinstated to your account for an Issuing dispute.

Occurs whenever funds are deducted from your account for an Issuing dispute.

Occurs whenever a dispute is submitted.

Occurs whenever a dispute is updated.

Occurs whenever a personalization design is activated following the activation of the physical bundle that belongs to it.

Occurs whenever a personalization design is deactivated following the deactivation of the physical bundle that belongs to it.

Occurs whenever a personalization design is rejected by design review.

Occurs whenever a personalization design is updated.

Occurs whenever an issuing digital wallet token is created.

Occurs whenever an issuing digital wallet token is updated.

Occurs whenever an issuing transaction is created.

Occurs whenever an issuing transaction is updated with receipt data.

Occurs whenever an issuing transaction is updated.

Occurs whenever a Mandate is updated.

Occurs when a PaymentIntent has funds to be captured. Check the amount_capturable property on the PaymentIntent to determine the amount that can be captured. You may capture the PaymentIntent with an amount_to_capture value up to the specified amount. Learn more about capturing PaymentIntents.

Occurs when a PaymentIntent is canceled.

Occurs when a new PaymentIntent is created.

Occurs when funds are applied to a customer_balance PaymentIntent and the ‘amount_remaining’ changes.

Occurs when a PaymentIntent has failed the attempt to create a payment method or a payment.

Occurs when a PaymentIntent has started processing.

Occurs when a PaymentIntent transitions to requires_action state

Occurs when a PaymentIntent has successfully completed payment.

Occurs when a payment link is created.

Occurs when a payment link is updated.

Occurs whenever a new payment method is attached to a customer.

Occurs whenever a payment method’s details are automatically updated by the network.

Occurs whenever a payment method is detached from a customer.

Occurs whenever a payment method is updated via the PaymentMethod update API.

Occurs whenever a payout is canceled.

Occurs whenever a payout is created.

Occurs whenever a payout attempt fails.

Occurs whenever a payout is expected to be available in the destination account. If the payout fails, a payout.failed notification is also sent, at a later time.

Occurs whenever balance transactions paid out in an automatic payout can be queried.

Occurs whenever a payout is updated.

Occurs whenever a person associated with an account is created.

Occurs whenever a person associated with an account is deleted.

Occurs whenever a person associated with an account is updated.

Occurs whenever a plan is created.

Occurs whenever a plan is deleted.

Occurs whenever a plan is updated.

Occurs whenever a price is created.

Occurs whenever a price is deleted.

Occurs whenever a price is updated.

Occurs whenever a product is created.

Occurs whenever a product is deleted.

Occurs whenever a product is updated.

Occurs whenever a promotion code is created.

Occurs whenever a promotion code is updated.

Occurs whenever a quote is accepted.

Occurs whenever a quote is canceled.

Occurs whenever a quote is created.

Occurs whenever a quote is finalized.

Occurs X number of days before a quote is scheduled to expire—where X is determined by Automations

Occurs whenever an early fraud warning is created.

Occurs whenever an early fraud warning is updated.

Occurs whenever a refund is created.

Occurs whenever a refund has failed.

Occurs whenever a refund is updated.

Occurs whenever a requested ReportRun failed to complete.

Occurs whenever a requested ReportRun completed successfully.

Occurs whenever a ReportType is updated (typically to indicate that a new day’s data has come available).

Occurs whenever a review is closed. The review’s reason field indicates why: approved, disputed, refunded, refunded_as_fraud, or canceled.

Occurs whenever a review is opened.

Occurs when a SetupIntent is canceled.

Occurs when a new SetupIntent is created.

Occurs when a SetupIntent is in requires_action state.

Occurs when a SetupIntent has failed the attempt to setup a payment method.

Occurs when an SetupIntent has successfully setup a payment method.

Occurs whenever a Sigma scheduled query run finishes.

Occurs whenever a source is canceled.

Occurs whenever a source transitions to chargeable.

Occurs whenever a source fails.

Occurs whenever a source mandate notification method is set to manual.

Occurs whenever the refund attributes are required on a receiver source to process a refund or a mispayment.

Occurs whenever a source transaction is created.

Occurs whenever a source transaction is updated.

Occurs whenever a subscription schedule is canceled due to the underlying subscription being canceled because of delinquency.

Occurs whenever a subscription schedule is canceled.

Occurs whenever a new subscription schedule is completed.

Occurs whenever a new subscription schedule is created.

Occurs 7 days before a subscription schedule will expire.

Occurs whenever a new subscription schedule is released.

Occurs whenever a subscription schedule is updated.

Occurs whenever a new tax rate is created.

Occurs whenever a tax rate is updated.

Occurs whenever tax settings is updated.

Occurs whenever an action sent to a Terminal reader failed.

Occurs whenever an action sent to a Terminal reader was successful.

Occurs whenever an action sent to a Terminal reader is updated.

Occurs whenever a test clock starts advancing.

Occurs whenever a test clock is created.

Occurs whenever a test clock is deleted.

Occurs whenever a test clock fails to advance its frozen time.

Occurs whenever a test clock transitions to a ready status.

Occurs whenever a top-up is canceled.

Occurs whenever a top-up is created.

Occurs whenever a top-up fails.

Occurs whenever a top-up is reversed.

Occurs whenever a top-up succeeds.

Occurs whenever a transfer is created.

Occurs whenever a transfer is reversed, including partial reversals.

Occurs whenever a transfer’s description or metadata is updated.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "evt_1NG8Du2eZvKYlo2CUI79vXWy",  "object": "event",  "api_version": "2019-02-19",  "created": 1686089970,  "data": {    "object": {      "id": "seti_1NG8Du2eZvKYlo2C9XMqbR0x",      "object": "setup_intent",      "application": null,      "automatic_payment_methods": null,      "cancellation_reason": null,      "client_secret": "seti_1NG8Du2eZvKYlo2C9XMqbR0x_secret_O2CdhLwGFh2Aej7bCY7qp8jlIuyR8DJ",      "created": 1686089970,      "customer": null,      "description": null,      "flow_directions": null,      "last_setup_error": null,      "latest_attempt": null,      "livemode": false,      "mandate": null,      "metadata": {},      "next_action": null,      "on_behalf_of": null,      "payment_method": "pm_1NG8Du2eZvKYlo2CYzzldNr7",      "payment_method_options": {        "acss_debit": {          "currency": "cad",          "mandate_options": {            "interval_description": "First day of every month",            "payment_schedule": "interval",            "transaction_type": "personal"          },          "verification_method": "automatic"        }      },      "payment_method_types": [        "acss_debit"      ],      "single_use_mandate": null,      "status": "requires_confirmation",      "usage": "off_session"    }  },  "livemode": false,  "pending_webhooks": 0,  "request": {    "id": null,    "idempotency_key": null  },  "type": "setup_intent.created"}
```

Example 2 (unknown):
```unknown
{  "id": "evt_1NG8Du2eZvKYlo2CUI79vXWy",  "object": "event",  "api_version": "2019-02-19",  "created": 1686089970,  "data": {    "object": {      "id": "seti_1NG8Du2eZvKYlo2C9XMqbR0x",      "object": "setup_intent",      "application": null,      "automatic_payment_methods": null,      "cancellation_reason": null,      "client_secret": "seti_1NG8Du2eZvKYlo2C9XMqbR0x_secret_O2CdhLwGFh2Aej7bCY7qp8jlIuyR8DJ",      "created": 1686089970,      "customer": null,      "description": null,      "flow_directions": null,      "last_setup_error": null,      "latest_attempt": null,      "livemode": false,      "mandate": null,      "metadata": {},      "next_action": null,      "on_behalf_of": null,      "payment_method": "pm_1NG8Du2eZvKYlo2CYzzldNr7",      "payment_method_options": {        "acss_debit": {          "currency": "cad",          "mandate_options": {            "interval_description": "First day of every month",            "payment_schedule": "interval",            "transaction_type": "personal"          },          "verification_method": "automatic"        }      },      "payment_method_types": [        "acss_debit"      ],      "single_use_mandate": null,      "status": "requires_confirmation",      "usage": "off_session"    }  },  "livemode": false,  "pending_webhooks": 0,  "request": {    "id": null,    "idempotency_key": null  },  "type": "setup_intent.created"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/events/evt_1NG8Du2eZvKYlo2CUI79vXWy \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/events/evt_1NG8Du2eZvKYlo2CUI79vXWy \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

---

## Retrieve an event

**URL:** https://docs.stripe.com/api/events/retrieve

**Contents:**
- Retrieve an event
  - Parameters
  - Returns
- List all events
  - Parameters
    - typesarray of strings
  - More parametersExpand all
    - createdobject
    - delivery_successboolean
    - ending_beforestring

Retrieves the details of an event if it was created in the last 30 days. Supply the unique identifier of the event, which you might have received in a webhook.

Returns an event object if a valid identifier was provided. All events share a common structure, detailed to the right. The only property that will differ is the data property.

In each case, the data dictionary will have an attribute called object and its value will be the same as retrieving the same object directly from the API. For example, a customer.created event will have the same information as retrieving the relevant customer would.

In cases where the attributes of an object have changed, data will also contain a dictionary containing the changes.

List events, going back up to 30 days. Each event data is rendered according to Stripe API version at its creation time, specified in event object api_version attribute (not according to your current Stripe API version or Stripe-Version header).

An array of up to 20 strings containing specific event names. The list will be filtered to include only events with a matching event property. You may pass either type or types, but not both.

A dictionary with a data property that contains an array of up to limit events, starting after event starting_after. Each entry in the array is a separate event object. If no more events are available, the resulting array will be empty.

This is a list of all public snapshot events we currently send for /v1 resources, which is continually evolving and expanding.

Stripe events use the resource.event naming convention. Events that occur on subresources like customer.subscription.updated don’t trigger a corresponding event for the parent resource (customer.updated).

Stripe creates event types marked as Selection required only when at least one webhook is listening for it. A webhook set to listen to all events doesn’t satisfy this requirement and won’t generate Selection required event types.

Occurs whenever a user authorizes an application. Sent to the related application only.

Occurs whenever a user deauthorizes an application. Sent to the related application only.

Occurs whenever an external account is created.

Occurs whenever an external account is deleted.

Occurs whenever an external account is updated.

Occurs whenever an account status or property has changed.

Occurs whenever an application fee is created on a charge.

Occurs whenever an application fee refund is updated.

Occurs whenever an application fee is refunded, whether from refunding a charge or from refunding the application fee directly. This includes partial refunds.

Occurs whenever a balance settings status or property has changed.

Occurs whenever your Stripe balance has been updated (e.g., when a charge is available to be paid out). By default, Stripe automatically transfers funds in your balance to your bank account on a daily basis. This event is not fired for negative transactions.

Occurs whenever a portal configuration is created.

Occurs whenever a portal configuration is updated.

Occurs whenever a portal session is created.

Occurs whenever your custom alert threshold is met.

Occurs when a credit balance transaction is created

Occurs when a credit grant is created

Occurs when a credit grant is updated

Occurs when a meter is created

Occurs when a meter is deactivated

Occurs when a meter is reactivated

Occurs when a meter is updated

Occurs whenever a capability has new requirements or a new status.

Occurs whenever there is a positive remaining cash balance after Stripe automatically reconciles new funds into the cash balance. If you enabled manual reconciliation, this webhook will fire whenever there are new funds into the cash balance.

Occurs whenever a previously uncaptured charge is captured.

Occurs when a dispute is closed and the dispute status changes to lost, warning_closed, or won.

Occurs whenever a customer disputes a charge with their bank.

Occurs when funds are reinstated to your account after a dispute is closed. This includes partially refunded payments.

Occurs when funds are removed from your account due to a dispute.

Occurs when the dispute is updated (usually with evidence).

Occurs whenever an uncaptured charge expires.

Occurs whenever a failed charge attempt occurs.

Occurs whenever a pending charge is created.

Occurs whenever a refund is updated on selected payment methods. For updates on all refunds, listen to refund.updated instead.

Occurs whenever a charge is refunded, including partial refunds. Listen to refund.created for information about the refund.

Occurs whenever a charge is successful.

Occurs whenever a charge description or metadata is updated, or upon an asynchronous capture.

Occurs when a payment intent using a delayed payment method fails.

Occurs when a payment intent using a delayed payment method finally succeeds.

Occurs when a Checkout Session has been successfully completed.

Occurs when a Checkout Session is expired.

Occurs when a Climate order is canceled.

Occurs when a Climate order is created.

Occurs when a Climate order is delayed.

Occurs when a Climate order is delivered.

Occurs when a Climate order’s product is substituted for another.

Occurs when a Climate product is created.

Occurs when a Climate product is updated.

Occurs whenever a coupon is created.

Occurs whenever a coupon is deleted.

Occurs whenever a coupon is updated.

Occurs whenever a credit note is created.

Occurs whenever a credit note is updated.

Occurs whenever a credit note is voided.

Occurs whenever a new customer cash balance transactions is created.

Occurs whenever a new customer is created.

Occurs whenever a customer is deleted.

Occurs whenever a coupon is attached to a customer.

Occurs whenever a coupon is removed from a customer.

Occurs whenever a customer is switched from one coupon to another.

Occurs whenever a new source is created for a customer.

Occurs whenever a source is removed from a customer.

Occurs whenever a card or source will expire at the end of the month. This event only works with legacy integrations using Card or Source objects. If you use the PaymentMethod API, this event won’t occur.

Occurs whenever a source’s details are changed.

Occurs whenever a customer is signed up for a new plan.

Occurs whenever a customer’s subscription ends.

Occurs whenever a customer’s subscription is paused. Only applies when subscriptions enter status=paused, not when payment collection is paused.

Occurs whenever a customer’s subscription’s pending update is applied, and the subscription is updated.

Occurs whenever a customer’s subscription’s pending update expires before the related invoice is paid.

Occurs whenever a customer’s subscription is no longer paused. Only applies when a status=paused subscription is resumed, not when payment collection is resumed.

Occurs three days before a subscription’s trial period is scheduled to end, or when a trial is ended immediately (using trial_end=now).

Occurs whenever a subscription changes (e.g., switching from one plan to another, or changing the status from trial to active).

Occurs whenever a tax ID is created for a customer.

Occurs whenever a tax ID is deleted from a customer.

Occurs whenever a customer’s tax ID is updated.

Occurs whenever any property of a customer changes.

Occurs whenever a customer’s entitlements change.

Occurs whenever a new Stripe-generated file is available for your account.

Occurs when a Financial Connections account’s account numbers are updated.

Occurs when a new Financial Connections account is created.

Occurs when a Financial Connections account’s status is updated from active to inactive.

Occurs when a Financial Connections account is disconnected.

Occurs when a Financial Connections account’s status is updated from inactive to active.

Occurs when an Account’s balance_refresh status transitions from pending to either succeeded or failed.

Occurs when an Account’s ownership_refresh status transitions from pending to either succeeded or failed.

Occurs when an Account’s transaction_refresh status transitions from pending to either succeeded or failed.

Occurs when an Account’s tokenized account number is about to expire.

Occurs whenever a VerificationSession is canceled

Occurs whenever a VerificationSession is created

Occurs whenever a VerificationSession transitions to processing

Occurs whenever a VerificationSession is redacted.

Occurs whenever a VerificationSession transitions to require user input

Occurs whenever a VerificationSession transitions to verified

Occurs when an InvoicePayment is successfully paid.

Occurs whenever a new invoice is created. To learn how webhooks can be used with this event, and how they can affect it, see Using Webhooks with Subscriptions.

Occurs whenever a draft invoice is deleted. Note: This event is not sent for invoice previews.

Occurs whenever a draft invoice cannot be finalized. See the invoice’s last finalization error for details.

Occurs whenever a draft invoice is finalized and updated to be an open invoice.

Occurs whenever an invoice is marked uncollectible.

Occurs X number of days after an invoice becomes due—where X is determined by Automations

Occurs when an invoice transitions to paid with a non-zero amount_overpaid.

Occurs whenever an invoice payment attempt succeeds or an invoice is marked as paid out-of-band.

Occurs whenever an invoice payment attempt requires further user action to complete.

Occurs when an invoice requires a payment using a payment method that cannot be processed by Stripe.

Occurs whenever an invoice payment attempt fails, due to either a declined payment, including soft decline, or to the lack of a stored payment method.

Occurs whenever an invoice payment attempt succeeds.

Occurs whenever an invoice email is sent out.

Occurs X number of days before a subscription is scheduled to create an invoice that is automatically charged—where X is determined by your subscriptions settings. Note: The received Invoice object will not have an invoice ID.

Occurs whenever an invoice changes (e.g., the invoice amount).

Occurs whenever an invoice is voided.

Occurs X number of days before an invoice becomes due—where X is determined by Automations

Occurs whenever an invoice item is created.

Occurs whenever an invoice item is deleted.

Occurs whenever an authorization is created.

Represents a synchronous request for authorization, see Using your integration to handle authorization requests.

Occurs whenever an authorization is updated.

Occurs whenever a card is created.

Occurs whenever a card is updated.

Occurs whenever a cardholder is created.

Occurs whenever a cardholder is updated.

Occurs whenever a dispute is won, lost or expired.

Occurs whenever a dispute is created.

Occurs whenever funds are reinstated to your account for an Issuing dispute.

Occurs whenever funds are deducted from your account for an Issuing dispute.

Occurs whenever a dispute is submitted.

Occurs whenever a dispute is updated.

Occurs whenever a personalization design is activated following the activation of the physical bundle that belongs to it.

Occurs whenever a personalization design is deactivated following the deactivation of the physical bundle that belongs to it.

Occurs whenever a personalization design is rejected by design review.

Occurs whenever a personalization design is updated.

Occurs whenever an issuing digital wallet token is created.

Occurs whenever an issuing digital wallet token is updated.

Occurs whenever an issuing transaction is created.

Occurs whenever an issuing transaction is updated with receipt data.

Occurs whenever an issuing transaction is updated.

Occurs whenever a Mandate is updated.

Occurs when a PaymentIntent has funds to be captured. Check the amount_capturable property on the PaymentIntent to determine the amount that can be captured. You may capture the PaymentIntent with an amount_to_capture value up to the specified amount. Learn more about capturing PaymentIntents.

Occurs when a PaymentIntent is canceled.

Occurs when a new PaymentIntent is created.

Occurs when funds are applied to a customer_balance PaymentIntent and the ‘amount_remaining’ changes.

Occurs when a PaymentIntent has failed the attempt to create a payment method or a payment.

Occurs when a PaymentIntent has started processing.

Occurs when a PaymentIntent transitions to requires_action state

Occurs when a PaymentIntent has successfully completed payment.

Occurs when a payment link is created.

Occurs when a payment link is updated.

Occurs whenever a new payment method is attached to a customer.

Occurs whenever a payment method’s details are automatically updated by the network.

Occurs whenever a payment method is detached from a customer.

Occurs whenever a payment method is updated via the PaymentMethod update API.

Occurs whenever a payout is canceled.

Occurs whenever a payout is created.

Occurs whenever a payout attempt fails.

Occurs whenever a payout is expected to be available in the destination account. If the payout fails, a payout.failed notification is also sent, at a later time.

Occurs whenever balance transactions paid out in an automatic payout can be queried.

Occurs whenever a payout is updated.

Occurs whenever a person associated with an account is created.

Occurs whenever a person associated with an account is deleted.

Occurs whenever a person associated with an account is updated.

Occurs whenever a plan is created.

Occurs whenever a plan is deleted.

Occurs whenever a plan is updated.

Occurs whenever a price is created.

Occurs whenever a price is deleted.

Occurs whenever a price is updated.

Occurs whenever a product is created.

Occurs whenever a product is deleted.

Occurs whenever a product is updated.

Occurs whenever a promotion code is created.

Occurs whenever a promotion code is updated.

Occurs whenever a quote is accepted.

Occurs whenever a quote is canceled.

Occurs whenever a quote is created.

Occurs whenever a quote is finalized.

Occurs X number of days before a quote is scheduled to expire—where X is determined by Automations

Occurs whenever an early fraud warning is created.

Occurs whenever an early fraud warning is updated.

Occurs whenever a refund is created.

Occurs whenever a refund has failed.

Occurs whenever a refund is updated.

Occurs whenever a requested ReportRun failed to complete.

Occurs whenever a requested ReportRun completed successfully.

Occurs whenever a ReportType is updated (typically to indicate that a new day’s data has come available).

Occurs whenever a review is closed. The review’s reason field indicates why: approved, disputed, refunded, refunded_as_fraud, or canceled.

Occurs whenever a review is opened.

Occurs when a SetupIntent is canceled.

Occurs when a new SetupIntent is created.

Occurs when a SetupIntent is in requires_action state.

Occurs when a SetupIntent has failed the attempt to setup a payment method.

Occurs when an SetupIntent has successfully setup a payment method.

Occurs whenever a Sigma scheduled query run finishes.

Occurs whenever a source is canceled.

Occurs whenever a source transitions to chargeable.

Occurs whenever a source fails.

Occurs whenever a source mandate notification method is set to manual.

Occurs whenever the refund attributes are required on a receiver source to process a refund or a mispayment.

Occurs whenever a source transaction is created.

Occurs whenever a source transaction is updated.

Occurs whenever a subscription schedule is canceled due to the underlying subscription being canceled because of delinquency.

Occurs whenever a subscription schedule is canceled.

Occurs whenever a new subscription schedule is completed.

Occurs whenever a new subscription schedule is created.

Occurs 7 days before a subscription schedule will expire.

Occurs whenever a new subscription schedule is released.

Occurs whenever a subscription schedule is updated.

Occurs whenever a new tax rate is created.

Occurs whenever a tax rate is updated.

Occurs whenever tax settings is updated.

Occurs whenever an action sent to a Terminal reader failed.

Occurs whenever an action sent to a Terminal reader was successful.

Occurs whenever an action sent to a Terminal reader is updated.

Occurs whenever a test clock starts advancing.

Occurs whenever a test clock is created.

Occurs whenever a test clock is deleted.

Occurs whenever a test clock fails to advance its frozen time.

Occurs whenever a test clock transitions to a ready status.

Occurs whenever a top-up is canceled.

Occurs whenever a top-up is created.

Occurs whenever a top-up fails.

Occurs whenever a top-up is reversed.

Occurs whenever a top-up succeeds.

Occurs whenever a transfer is created.

Occurs whenever a transfer is reversed, including partial reversals.

Occurs whenever a transfer’s description or metadata is updated.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/events/evt_1NG8Du2eZvKYlo2CUI79vXWy \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/events/evt_1NG8Du2eZvKYlo2CUI79vXWy \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "evt_1NG8Du2eZvKYlo2CUI79vXWy",  "object": "event",  "api_version": "2019-02-19",  "created": 1686089970,  "data": {    "object": {      "id": "seti_1NG8Du2eZvKYlo2C9XMqbR0x",      "object": "setup_intent",      "application": null,      "automatic_payment_methods": null,      "cancellation_reason": null,      "client_secret": "seti_1NG8Du2eZvKYlo2C9XMqbR0x_secret_O2CdhLwGFh2Aej7bCY7qp8jlIuyR8DJ",      "created": 1686089970,      "customer": null,      "description": null,      "flow_directions": null,      "last_setup_error": null,      "latest_attempt": null,      "livemode": false,      "mandate": null,      "metadata": {},      "next_action": null,      "on_behalf_of": null,      "payment_method": "pm_1NG8Du2eZvKYlo2CYzzldNr7",      "payment_method_options": {        "acss_debit": {          "currency": "cad",          "mandate_options": {            "interval_description": "First day of every month",            "payment_schedule": "interval",            "transaction_type": "personal"          },          "verification_method": "automatic"        }      },      "payment_method_types": [        "acss_debit"      ],      "single_use_mandate": null,      "status": "requires_confirmation",      "usage": "off_session"    }  },  "livemode": false,  "pending_webhooks": 0,  "request": {    "id": null,    "idempotency_key": null  },  "type": "setup_intent.created"}
```

Example 4 (unknown):
```unknown
{  "id": "evt_1NG8Du2eZvKYlo2CUI79vXWy",  "object": "event",  "api_version": "2019-02-19",  "created": 1686089970,  "data": {    "object": {      "id": "seti_1NG8Du2eZvKYlo2C9XMqbR0x",      "object": "setup_intent",      "application": null,      "automatic_payment_methods": null,      "cancellation_reason": null,      "client_secret": "seti_1NG8Du2eZvKYlo2C9XMqbR0x_secret_O2CdhLwGFh2Aej7bCY7qp8jlIuyR8DJ",      "created": 1686089970,      "customer": null,      "description": null,      "flow_directions": null,      "last_setup_error": null,      "latest_attempt": null,      "livemode": false,      "mandate": null,      "metadata": {},      "next_action": null,      "on_behalf_of": null,      "payment_method": "pm_1NG8Du2eZvKYlo2CYzzldNr7",      "payment_method_options": {        "acss_debit": {          "currency": "cad",          "mandate_options": {            "interval_description": "First day of every month",            "payment_schedule": "interval",            "transaction_type": "personal"          },          "verification_method": "automatic"        }      },      "payment_method_types": [        "acss_debit"      ],      "single_use_mandate": null,      "status": "requires_confirmation",      "usage": "off_session"    }  },  "livemode": false,  "pending_webhooks": 0,  "request": {    "id": null,    "idempotency_key": null  },  "type": "setup_intent.created"}
```

---

## The Event object

**URL:** https://docs.stripe.com/api/v2/core/events/object

**Contents:**
- The Event object
  - Attributes
    - idstring
    - objectstring, value is "v2.core.event"
    - changesnullable object
    - contextnullable string
    - createdtimestamp
    - datanullable object
    - livemodeboolean
    - reasonnullable object

Unique identifier for the event.

String representing the object’s type. Objects of the same type share the same value of the object field.

Before and after changes for the primary related object.

Authentication context needed to fetch the event or related object.

Time at which the object was created.

Additional data about the event.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Reason for the event.

Object containing the reference to API resource relevant to the event.

The type of the event.

Retrieves the details of an event.

Unique identifier for the object.

Unique identifier for the event.

String representing the object’s type. Objects of the same type share the same value of the object field.

Before and after changes for the primary related object.

Authentication context needed to fetch the event or related object.

Time at which the object was created.

Additional data about the event.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Reason for the event.

Object containing the reference to API resource relevant to the event.

The type of the event.

The resource wasn’t found.

List events, going back up to 30 days.

Set of filters to query events within a range of created timestamps.

Primary object ID used to retrieve related events.

An array of up to 20 strings containing specific event names.

The previous page url.

Send a ping event to an event destination.

Identifier for the event destination to ping.

Unique identifier for the event.

String representing the object’s type. Objects of the same type share the same value of the object field.

Before and after changes for the primary related object.

Authentication context needed to fetch the event or related object.

Time at which the object was created.

Additional data about the event.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Reason for the event.

Object containing the reference to API resource relevant to the event.

The type of the event.

The resource wasn’t found.

This is a list of all public thin events we currently send for /v1 and /v2 resources, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "evt_test_65RCjj4EqW1sabcjs2Z16RCMoNQdSQkOWvfL6L5uU2K40u",  "object": "v2.core.event",  "context": null,  "created": "2024-09-26T17:46:22.134Z",  "data": {    "developer_message_summary": "There is 1 invalid event",    "reason": {      "error_count": 1,      "error_types": [        {          "code": "meter_event_no_customer_defined",          "error_count": 1,          "sample_errors": [            {              "error_message": "Customer mapping key stripe_customer_id not found in payload.",              "request": {                "identifier": "cb447754-6880-45c2-8f2f-ef19b6ce81e9"              }            }          ]        }      ]    },    "validation_end": "2024-09-26T17:46:20.000Z",    "validation_start": "2024-09-26T17:46:10.000Z"  },  "livemode": false,  "reason": null,  "related_object": {    "id": "mtr_test_61RCjiqdTDC91zgip41IqPCzPnxqqSVc",    "type": "billing.meter",    "url": "/v1/billing/meters/mtr_test_61RCjiqdTDC91zgip41IqPCzPnxqqSVc"  },  "type": "v1.billing.meter.error_report_triggered"}
```

Example 2 (unknown):
```unknown
{  "id": "evt_test_65RCjj4EqW1sabcjs2Z16RCMoNQdSQkOWvfL6L5uU2K40u",  "object": "v2.core.event",  "context": null,  "created": "2024-09-26T17:46:22.134Z",  "data": {    "developer_message_summary": "There is 1 invalid event",    "reason": {      "error_count": 1,      "error_types": [        {          "code": "meter_event_no_customer_defined",          "error_count": 1,          "sample_errors": [            {              "error_message": "Customer mapping key stripe_customer_id not found in payload.",              "request": {                "identifier": "cb447754-6880-45c2-8f2f-ef19b6ce81e9"              }            }          ]        }      ]    },    "validation_end": "2024-09-26T17:46:20.000Z",    "validation_start": "2024-09-26T17:46:10.000Z"  },  "livemode": false,  "reason": null,  "related_object": {    "id": "mtr_test_61RCjiqdTDC91zgip41IqPCzPnxqqSVc",    "type": "billing.meter",    "url": "/v1/billing/meters/mtr_test_61RCjiqdTDC91zgip41IqPCzPnxqqSVc"  },  "type": "v1.billing.meter.error_report_triggered"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v2/core/events/evt_test_65RCjj4EqW1sabcjs2Z16RCMoNQdSQkOWvfL6L5uU2K40u \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v2/core/events/evt_test_65RCjj4EqW1sabcjs2Z16RCMoNQdSQkOWvfL6L5uU2K40u \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

---

## Handle webhook versioning

**URL:** https://docs.stripe.com/webhooks/versioning

**Contents:**
- Handle webhook versioning
- Learn how to upgrade the API version of your webhook endpoint.
    - Private preview
- Figure out if the new API version has breaking changes
- Create a new disabled webhook endpoint
- Update your webhook code to ignore events sent to the new endpoint
- Update your webhook code to process events for the new endpoint
- Monitor your new webhook endpoint
- Disable the old webhook endpoint

Thin events for API v1 resources are available in private preview. You can use them to streamline integration upgrades without changing your webhook configuration. Previously, thin events only supported API v2 resources. Learn more and request access.

Webhook endpoints either have a specific API version set or use the default API version of the Stripe account. If you use any of our static language SDKs (.NET, Java or Go) to process events, the API version set for webhooks should match the version used to generate the SDKs. Matching these versions ensures successful deserialization of the event object.

Use this guide to safely upgrade your webhook endpoints to a newer API version that may have breaking changes.

Every API version prior to 2024-09-30.acacia has breaking changes.

Starting with the 2024-09-30.acacia release, Stripe follows a new API release process where we release new API versions monthly with no breaking changes. Twice a year, we issue a new release (for example, Acacia) that starts with an API version that has breaking changes. You can safely upgrade your webhook endpoints to any API version in the same release without making changes to your integration.

Create a new webhook endpoint with the following parameters:

After you create the new webhook endpoint, disable it. You will re-enable it in the next step.

Update your event processing code:

Next, enable the new webhook endpoint that you created in the previous step. At this point every event is sent twice: once with the old API version and once with the new one.

Update the version of the Stripe library you’re using to match the version of your new webhook endpoint. Make sure to read the changelog and handle any breaking changes.

Update your event processing code:

If events aren’t being correctly handled by your new code, try the following:

Once the upgrade is successful, disable the old webhook endpoint to stop your server from returning 400 status. If you don’t disable it, this may cause issues with integrations that relies on a 200 response.

After you disable the old webhook endpoint, Stripe won’t re-deliver events that returned a 400.

---
