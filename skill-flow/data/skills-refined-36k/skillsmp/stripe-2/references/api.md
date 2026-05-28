# Stripe - Api

**Pages:** 156

---

## Customer Session

**URL:** https://docs.stripe.com/api/customer_sessions

**Contents:**
- Customer Session
- The Customer Session object
  - Attributes
    - client_secretstring
    - componentsobject
    - customerstringExpandable
    - expires_attimestamp
  - More attributesExpand all
    - objectstring
    - createdtimestamp

A Customer Session allows you to grant Stripe’s frontend SDKs (like Stripe.js) client-side access control over a Customer.

Related guides: Customer Session with the Payment Element, Customer Session with the Pricing Table, Customer Session with the Buy Button.

The client secret of this Customer Session. Used on the client to set up secure access to the given customer.

The client secret can be used to provide access to customer from your frontend. It should not be stored, logged, or exposed to anyone other than the relevant customer. Make sure that you have TLS enabled on any page that includes the client secret.

This hash defines which component is enabled and the features it supports.

The Customer the Customer Session was created for.

The timestamp at which this Customer Session will expire.

Creates a Customer Session object that includes a single-use client secret that you can use on your front-end to grant client-side API access for certain customer resources.

Configuration for each component. At least 1 component must be enabled.

The ID of an existing customer for which to create the Customer Session.

Returns a Customer Session object.

**Examples:**

Example 1 (unknown):
```unknown
{  "object": "customer_session",  "client_secret": "_POpxYpmkXdtttYtZQYhrsOJZ2RCQ9kCqqXRU6qrP5c4Jgje",  "components": {    "buy_button": {      "enabled": false    },    "pricing_table": {      "enabled": true    }  },  "customer": "cus_PO34b57IOUb83c",  "expires_at": 1684790027,  "livemode": false}
```

Example 2 (unknown):
```unknown
{  "object": "customer_session",  "client_secret": "_POpxYpmkXdtttYtZQYhrsOJZ2RCQ9kCqqXRU6qrP5c4Jgje",  "components": {    "buy_button": {      "enabled": false    },    "pricing_table": {      "enabled": true    }  },  "customer": "cus_PO34b57IOUb83c",  "expires_at": 1684790027,  "livemode": false}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/customer_sessions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_PO34b57IOUb83c \  -d "components[pricing_table][enabled]"=true
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/customer_sessions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_PO34b57IOUb83c \  -d "components[pricing_table][enabled]"=true
```

---

## Delete an event destination v2

**URL:** https://docs.stripe.com/api/v2/core/event_destinations/delete

**Contents:**
- Delete an event destination v2
  - Parameters
    - idstringRequired
  - Returns
  - Response attributes
    - idstring
- Disable an event destination v2
  - Parameters
    - idstringRequired
  - Returns

Delete an event destination.

Identifier for the event destination to delete.

Identifier for the deleted event destination.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

Disable an event destination.

Identifier for the event destination to disable.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value of the object field.

Amazon EventBridge configuration.

Time at which the object was created.

An optional description of what the event destination is used for.

The list of events to enable for this endpoint.

Payload type of events being subscribed to.

Where events should be routed from.

Receive events from accounts connected to the account that owns the event destination.

Receive events from the account that owns the event destination.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Event destination name.

If using the snapshot event payload, the API version events are rendered as.

Status. It can be set to either enabled or disabled.

Event destination is disabled.

Event destination is enabled.

Additional information about event destination status.

Event destination type.

Time at which the object was last updated.

Webhook endpoint configuration.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

Enable an event destination.

Identifier for the event destination to enable.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value of the object field.

Amazon EventBridge configuration.

Time at which the object was created.

An optional description of what the event destination is used for.

The list of events to enable for this endpoint.

Payload type of events being subscribed to.

Where events should be routed from.

Receive events from accounts connected to the account that owns the event destination.

Receive events from the account that owns the event destination.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Event destination name.

If using the snapshot event payload, the API version events are rendered as.

Status. It can be set to either enabled or disabled.

Event destination is disabled.

Event destination is enabled.

Additional information about event destination status.

Event destination type.

Time at which the object was last updated.

Webhook endpoint configuration.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

This is a list of all public thin events we currently send for updates to EventDestination, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

**Examples:**

Example 1 (unknown):
```unknown
curl -X DELETE https://api.stripe.com/v2/core/event_destinations/ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6 \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 2 (unknown):
```unknown
curl -X DELETE https://api.stripe.com/v2/core/event_destinations/ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6 \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 3 (unknown):
```unknown
{  "id": "ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6"}
```

Example 4 (unknown):
```unknown
{  "id": "ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6"}
```

---

## Handling errors

**URL:** https://docs.stripe.com/api/errors/handling

**Contents:**
- Handling errors
- Expanding Responses
- Idempotent requests
- Include-dependent response values (API v2)
- Metadata
- Sample metadata use cases

Our Client libraries raise exceptions for many reasons, such as a failed charge, invalid parameters, authentication errors, and network unavailability. We recommend writing code that gracefully handles all possible API exceptions.

Many objects allow you to request additional information as an expanded response by using the expand request parameter. This parameter is available on all API requests, and applies to the response of that request only. You can expand responses in two ways.

In many cases, an object contains the ID of a related object in its response properties. For example, a Charge might have an associated Customer ID. You can expand these objects in line with the expand request parameter. The expandable label in this documentation indicates ID fields that you can expand into objects.

Some available fields aren’t included in the responses by default, such as the number and cvc fields for the Issuing Card object. You can request these fields as an expanded response by using the expand request parameter.

You can expand recursively by specifying nested fields after a dot (.). For example, requesting payment_intent.customer on a charge expands the payment_intent property into a full PaymentIntent object, then expands the customer property on that payment intent into a full Customer object.

You can use the expand parameter on any endpoint that returns expandable fields, including list, create, and update endpoints.

Expansions on list requests start with the data property. For example, you can expand data.customers on a request to list charges and associated customers. Performing deep expansions on numerous list requests might result in slower processing times.

Expansions have a maximum depth of four levels (for example, the deepest expansion allowed when listing charges is data.payment_intent.customer.default_source).

You can expand multiple objects at the same time by identifying multiple items in the expand array.

The API supports idempotency for safely retrying requests without accidentally performing the same operation twice. When creating or updating an object, use an idempotency key. Then, if a connection error occurs, you can safely repeat the request without risk of creating a second object or performing the update twice.

To perform an idempotent request, provide an additional IdempotencyKey element to the request options.

Stripe’s idempotency works by saving the resulting status code and body of the first request made for any given idempotency key, regardless of whether it succeeds or fails. Subsequent requests with the same key return the same result, including 500 errors.

A client generates an idempotency key, which is a unique key that the server uses to recognize subsequent retries of the same request. How you create unique keys is up to you, but we suggest using V4 UUIDs, or another random string with enough entropy to avoid collisions. Idempotency keys are up to 255 characters long.

You can remove keys from the system automatically after they’re at least 24 hours old. We generate a new request if a key is reused after the original is pruned. The idempotency layer compares incoming parameters to those of the original request and errors if they’re not the same to prevent accidental misuse.

We save results only after the execution of an endpoint begins. If incoming parameters fail validation, or the request conflicts with another request that’s executing concurrently, we don’t save the idempotent result because no API endpoint initiates the execution. You can retry these requests. Learn more about when you can retry idempotent requests.

All POST requests accept idempotency keys. Don’t send idempotency keys in GET and DELETE requests because it has no effect. These requests are idempotent by definition.

Some API v2 responses contain null values for certain properties by default, regardless of their actual values. That reduces the size of response payloads while maintaining the basic response structure. To retrieve the actual values for those properties, specify them in the include array request parameter.

To determine whether you need to use the include parameter in a given request, look at the request description. The include parameter’s enum values represent the response properties that depend on the include parameter.

Whether a response property defaults to null depends on the request endpoint, not the object that the endpoint references. If multiple endpoints return data from the same object, a particular property can depend on include in one endpoint and return its actual value by default for a different endpoint.

A hash property can depend on a single include value, or on multiple include values associated with its child properties. For example, when updating an Account, to return actual values for the entire identity hash, specify identity in the include parameter. Otherwise, the identity hash is null in the response. However, to return actual values for the configuration hash, you must specify individual configurations in the request. If you specify at least one configuration, but not all of them, specified configurations return actual values and unspecified configurations return null. If you don’t specify any configurations, the configuration hash is null in the response.

The response includes actual values for the properties specified in the include parameter, and null for all other include-dependent properties.

Updateable Stripe objects—including Account, Charge, Customer, PaymentIntent, Refund, Subscription, and Transfer have a metadata parameter. You can use this parameter to attach key-value data to these Stripe objects.

You can specify up to 50 keys, with key names up to 40 characters long and values up to 500 characters long. Keys and values are stored as strings and can contain any characters with one exception: you can’t use square brackets ([ and ]) in keys.

You can use metadata to store additional, structured information on an object. For example, you could store your user’s full name and corresponding unique identifier from your system on a Stripe Customer object. Stripe doesn’t use metadata—for example, we don’t use it to authorize or decline a charge and it won’t be seen by your users unless you choose to show it to them.

Some of the objects listed above also support a description parameter. You can use the description parameter to annotate a charge-for example, a human-readable description such as 2 shirts for test@example.com. Unlike metadata, description is a single string, which your users might see (for example, in email receipts Stripe sends on your behalf).

Don’t store any sensitive information (bank account numbers, card details, and so on) as metadata or in the description parameter.

**Examples:**

Example 1 (unknown):
```unknown
# Select a client library to see examples of# handling different kinds of errors.
```

Example 2 (unknown):
```unknown
# Select a client library to see examples of# handling different kinds of errors.
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/charges/ch_3LmzzQ2eZvKYlo2C0XjzUzJV \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -d "expand[]"=customer \  -d "expand[]"="payment_intent.customer" \  -G
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/charges/ch_3LmzzQ2eZvKYlo2C0XjzUzJV \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -d "expand[]"=customer \  -d "expand[]"="payment_intent.customer" \  -G
```

---

## Invoice Payment

**URL:** https://docs.stripe.com/api/invoice-payment

**Contents:**
- Invoice Payment
- The Invoice Payment object
  - Attributes
    - idstring
    - amount_paidnullable integer
    - amount_requestedinteger
    - invoicestringExpandable
    - is_defaultboolean
    - paymentobject
    - statusstring

Invoice Payments represent payments made against invoices. Invoice Payments can be accessed in two ways:

Invoice Payments include the mapping between payment objects, such as Payment Intent, and Invoices. This resource and its endpoints allows you to easily track if a payment is associated with a specific invoice and monitor the allocation details of the payments.

Unique identifier for the object.

Amount that was actually paid for this invoice, in cents. This field is null until the payment is paid. This amount can be less than the amount_requested if the PaymentIntent’s amount_received is not sufficient to pay all of the invoices that it is attached to.

Amount intended to be paid toward this invoice, in cents

The invoice that was paid.

Stripe automatically creates a default InvoicePayment when the invoice is finalized, and keeps it synchronized with the invoice’s amount_remaining. The PaymentIntent associated with the default payment can’t be edited or canceled directly.

The details on the payment.

The status of the payment, one of open, paid, or canceled.

Retrieves the invoice payment with the given ID.

Returns an invoice_payment object if a valid invoice payment ID was provided. Otherwise, this call raises an error.

When retrieving an invoice, there is an includable payments property containing the first handful of those items. There is also a URL where you can retrieve the full (paginated) list of payments.

The identifier of the invoice whose payments to return.

The payment details of the invoice payments to return.

The status of the invoice payments to return.

The payment has been canceled; it will not be credited to the invoice.

The payment is incomplete and isn’t credited to the invoice. More fine-grained information available on the payment intent

The payment is complete and has been credited to the invoice.

A dictionary with a data property that contains an array of up to limit invoice payments, starting after invoice payment starting_after. Each entry in the array is a separate invoice_payment object. If no more invoice payments are available, the resulting array will be empty.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "inpay_1M3USa2eZvKYlo2CBjuwbq0N",  "object": "invoice_payment",  "amount_paid": 2000,  "amount_requested": 2000,  "created": 1391288554,  "currency": "usd",  "invoice": "in_103Q0w2eZvKYlo2C5PYwf6Wf",  "is_default": true,  "livemode": false,  "payment": {    "type": "payment_intent",    "payment_intent": "pi_103Q0w2eZvKYlo2C364X582Z"  },  "status": "paid",  "status_transitions": {    "canceled_at": null,    "paid_at": 1391288554  }}
```

Example 2 (unknown):
```unknown
{  "id": "inpay_1M3USa2eZvKYlo2CBjuwbq0N",  "object": "invoice_payment",  "amount_paid": 2000,  "amount_requested": 2000,  "created": 1391288554,  "currency": "usd",  "invoice": "in_103Q0w2eZvKYlo2C5PYwf6Wf",  "is_default": true,  "livemode": false,  "payment": {    "type": "payment_intent",    "payment_intent": "pi_103Q0w2eZvKYlo2C364X582Z"  },  "status": "paid",  "status_transitions": {    "canceled_at": null,    "paid_at": 1391288554  }}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/invoice_payments/inpay_1M3USa2eZvKYlo2CBjuwbq0N \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/invoice_payments/inpay_1M3USa2eZvKYlo2CBjuwbq0N \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

---

## Balance

**URL:** https://docs.stripe.com/api/balance

**Contents:**
- Balance
- The Balance object
  - Attributes
    - availablearray of objects
    - pendingarray of objects
  - More attributesExpand all
    - objectstring
    - connect_reservednullable array of objectsConnect only
    - instant_availablenullable array of objects
    - issuingnullable object

This is an object representing your Stripe balance. You can retrieve it to see the balance currently on your Stripe account.

The top-level available and pending comprise your “payments balance.”

Related guide: Balances and settlement time, Understanding Connect account balances

Available funds that you can transfer or pay out automatically by Stripe or explicitly through the Transfers API or Payouts API. You can find the available balance for each currency and payment type in the source_types property.

Funds that aren’t available in the balance yet. You can find the pending balance for each currency and each payment type in the source_types property.

Retrieves the current account balance, based on the authentication that was used to make the request. For a sample request, see Accounting for negative balances.

Returns a balance object for the account that was authenticated in the request.

**Examples:**

Example 1 (unknown):
```unknown
{  "object": "balance",  "available": [    {      "amount": 666670,      "currency": "usd",      "source_types": {        "card": 666670      }    }  ],  "connect_reserved": [    {      "amount": 0,      "currency": "usd"    }  ],  "livemode": false,  "pending": [    {      "amount": 61414,      "currency": "usd",      "source_types": {        "card": 61414      }    }  ]}
```

Example 2 (unknown):
```unknown
{  "object": "balance",  "available": [    {      "amount": 666670,      "currency": "usd",      "source_types": {        "card": 666670      }    }  ],  "connect_reserved": [    {      "amount": 0,      "currency": "usd"    }  ],  "livemode": false,  "pending": [    {      "amount": 61414,      "currency": "usd",      "source_types": {        "card": 61414      }    }  ]}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/balance \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/balance \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

---

## Retrieve a balance transaction

**URL:** https://docs.stripe.com/api/balance_transactions/retrieve

**Contents:**
- Retrieve a balance transaction
  - Parameters
  - Returns
- List all balance transactions
  - Parameters
    - payoutstring
    - typestring
  - More parametersExpand all
    - createdobject
    - currencyenum

Retrieves the balance transaction with the given ID.

Note that this endpoint previously used the path /v1/balance/history/:id.

Returns a balance transaction if a valid balance transaction ID was provided. Raises an error otherwise.

Returns a list of transactions that have contributed to the Stripe account balance (e.g., charges, transfers, and so forth). The transactions are returned in sorted order, with the most recent transactions appearing first.

Note that this endpoint was previously called “Balance history” and used the path /v1/balance/history.

For automatic Stripe payouts only, only returns transactions that were paid out on the specified payout ID.

Only returns transactions of the given type. One of: adjustment, advance, advance_funding, anticipation_repayment, application_fee, application_fee_refund, charge, climate_order_purchase, climate_order_refund, connect_collection_transfer, contribution, issuing_authorization_hold, issuing_authorization_release, issuing_dispute, issuing_transaction, obligation_outbound, obligation_reversal_inbound, payment, payment_failure_refund, payment_network_reserve_hold, payment_network_reserve_release, payment_refund, payment_reversal, payment_unreconciled, payout, payout_cancel, payout_failure, payout_minimum_balance_hold, payout_minimum_balance_release, refund, refund_failure, reserve_transaction, reserved_funds, stripe_fee, stripe_fx_fee, stripe_balance_payment_debit, stripe_balance_payment_debit_reversal, tax_fee, topup, topup_reversal, transfer, transfer_cancel, transfer_failure, or transfer_refund.

A dictionary with a data property that contains an array of up to limit transactions, starting after transaction starting_after. Each entry in the array is a separate transaction history object. If no more transactions are available, the resulting array will be empty.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/balance_transactions/txn_1MiN3gLkdIwHu7ixxapQrznl \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/balance_transactions/txn_1MiN3gLkdIwHu7ixxapQrznl \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "txn_1MiN3gLkdIwHu7ixxapQrznl",  "object": "balance_transaction",  "amount": -400,  "available_on": 1678043844,  "created": 1678043844,  "currency": "usd",  "description": null,  "exchange_rate": null,  "fee": 0,  "fee_details": [],  "net": -400,  "reporting_category": "transfer",  "source": "tr_1MiN3gLkdIwHu7ixNCZvFdgA",  "status": "available",  "type": "transfer"}
```

Example 4 (unknown):
```unknown
{  "id": "txn_1MiN3gLkdIwHu7ixxapQrznl",  "object": "balance_transaction",  "amount": -400,  "available_on": 1678043844,  "created": 1678043844,  "currency": "usd",  "description": null,  "exchange_rate": null,  "fee": 0,  "fee_details": [],  "net": -400,  "reporting_category": "transfer",  "source": "tr_1MiN3gLkdIwHu7ixNCZvFdgA",  "status": "available",  "type": "transfer"}
```

---

## Tokens

**URL:** https://docs.stripe.com/api/tokens

**Contents:**
- Tokens
- The Token object
  - Attributes
    - idstring
    - cardnullable object
  - More attributesExpand all
    - objectstring
    - bank_accountnullable object
    - client_ipnullable string
    - createdtimestamp

Tokenization is the process Stripe uses to collect sensitive card or bank account details, or personally identifiable information (PII), directly from your customers in a secure manner. A token representing this information is returned to your server to use. Use our recommended payments integrations to perform this process on the client-side. This guarantees that no sensitive card data touches your server, and allows your integration to operate in a PCI-compliant way.

If you can’t use client-side tokenization, you can also create tokens using the API with either your publishable or secret API key. If your integration uses this method, you’re responsible for any PCI compliance that it might require, and you must keep your secret API key safe. Unlike with client-side tokenization, your customer’s information isn’t sent directly to Stripe, so we can’t determine how it’s handled or stored.

You can’t store or use tokens more than once. To store card or bank account information for later use, create Customer objects or External accounts. Radar, our integrated solution for automatic fraud protection, performs best with integrations that use client-side tokenization.

Unique identifier for the object.

Hash describing the card used to make the charge.

Creates a single-use token that wraps a user’s legal entity information. Use this when creating or updating a Connect account. Learn more about account tokens.

In live mode, you can only create account tokens with your application’s publishable key. In test mode, you can only create account tokens with your secret key or publishable key.

Information for the account this token represents.

Returns the created account token if it’s successful. Otherwise, this call raises an error.

Creates a single-use token that represents a bank account’s details. You can use this token with any v1 API method in place of a bank account dictionary. You can only use this token once. To do so, attach it to a connected account where controller.requirement_collection is application, which includes Custom accounts.

The bank account this token will represent.

Returns the created bank account token if it’s successful. Otherwise, this call raises an error.

Creates a single-use token that represents a credit card’s details. You can use this token in place of a credit card dictionary with any v1 API method. You can only use these tokens once by creating a new Charge object or by attaching them to a Customer object.

To use this functionality, you need to enable access to the raw card data APIs. In most cases, you can use our recommended payments integrations instead of using the API.

The card this token will represent. If you also pass in a customer, the card must be the ID of a card belonging to the customer. Otherwise, if you do not pass in a customer, this is a dictionary containing a user’s credit card details, with the options described below.

Returns the created card token if it’s successful. Otherwise, this call raises an error.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "tok_1N3T00LkdIwHu7ixt44h1F8k",  "object": "token",  "card": {    "id": "card_1N3T00LkdIwHu7ixRdxpVI1Q",    "object": "card",    "address_city": null,    "address_country": null,    "address_line1": null,    "address_line1_check": null,    "address_line2": null,    "address_state": null,    "address_zip": null,    "address_zip_check": null,    "brand": "Visa",    "country": "US",    "cvc_check": "unchecked",    "dynamic_last4": null,    "exp_month": 5,    "exp_year": 2026,    "fingerprint": "mToisGZ01V71BCos",    "funding": "credit",    "last4": "4242",    "metadata": {},    "name": null,    "tokenization_method": null,    "wallet": null  },  "client_ip": "52.35.78.6",  "created": 1683071568,  "livemode": false,  "type": "card",  "used": false}
```

Example 2 (unknown):
```unknown
{  "id": "tok_1N3T00LkdIwHu7ixt44h1F8k",  "object": "token",  "card": {    "id": "card_1N3T00LkdIwHu7ixRdxpVI1Q",    "object": "card",    "address_city": null,    "address_country": null,    "address_line1": null,    "address_line1_check": null,    "address_line2": null,    "address_state": null,    "address_zip": null,    "address_zip_check": null,    "brand": "Visa",    "country": "US",    "cvc_check": "unchecked",    "dynamic_last4": null,    "exp_month": 5,    "exp_year": 2026,    "fingerprint": "mToisGZ01V71BCos",    "funding": "credit",    "last4": "4242",    "metadata": {},    "name": null,    "tokenization_method": null,    "wallet": null  },  "client_ip": "52.35.78.6",  "created": 1683071568,  "livemode": false,  "type": "card",  "used": false}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/tokens \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "account[business_type]"=individual \  -d "account[individual][first_name]"=Jane \  -d "account[individual][last_name]"=Doe \  -d "account[tos_shown_and_accepted]"=true
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/tokens \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "account[business_type]"=individual \  -d "account[individual][first_name]"=Jane \  -d "account[individual][last_name]"=Doe \  -d "account[tos_shown_and_accepted]"=true
```

---

## Create an account token

**URL:** https://docs.stripe.com/api/tokens/create_account

**Contents:**
- Create an account token
  - Parameters
    - accountobjectRequired
  - Returns
- Create a bank account token
  - Parameters
    - bank_accountobject
  - More parametersExpand all
    - customerstringConnect only
  - Returns

Creates a single-use token that wraps a user’s legal entity information. Use this when creating or updating a Connect account. Learn more about account tokens.

In live mode, you can only create account tokens with your application’s publishable key. In test mode, you can only create account tokens with your secret key or publishable key.

Information for the account this token represents.

Returns the created account token if it’s successful. Otherwise, this call raises an error.

Creates a single-use token that represents a bank account’s details. You can use this token with any v1 API method in place of a bank account dictionary. You can only use this token once. To do so, attach it to a connected account where controller.requirement_collection is application, which includes Custom accounts.

The bank account this token will represent.

Returns the created bank account token if it’s successful. Otherwise, this call raises an error.

Creates a single-use token that represents a credit card’s details. You can use this token in place of a credit card dictionary with any v1 API method. You can only use these tokens once by creating a new Charge object or by attaching them to a Customer object.

To use this functionality, you need to enable access to the raw card data APIs. In most cases, you can use our recommended payments integrations instead of using the API.

The card this token will represent. If you also pass in a customer, the card must be the ID of a card belonging to the customer. Otherwise, if you do not pass in a customer, this is a dictionary containing a user’s credit card details, with the options described below.

Returns the created card token if it’s successful. Otherwise, this call raises an error.

Creates a single-use token that represents an updated CVC value that you can use for CVC re-collection. Use this token when you confirm a card payment or use a saved card on a PaymentIntent with confirmation_method: manual.

For most cases, use our JavaScript library instead of using the API. For a PaymentIntent with confirmation_method: automatic, use our recommended payments integration without tokenizing the CVC value.

The updated CVC value this token represents.

Returns the created CVC update token if it’s successful. Otherwise, this call raises an error.

Creates a single-use token that represents the details for a person. Use this when you create or update persons associated with a Connect account. Learn more about account tokens.

You can only create person tokens with your application’s publishable key and in live mode. You can use your application’s secret key to create person tokens only in test mode.

Information for the person this token represents.

Returns the created person token if it’s successful. Otherwise, this call raises an error.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/tokens \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "account[business_type]"=individual \  -d "account[individual][first_name]"=Jane \  -d "account[individual][last_name]"=Doe \  -d "account[tos_shown_and_accepted]"=true
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/tokens \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "account[business_type]"=individual \  -d "account[individual][first_name]"=Jane \  -d "account[individual][last_name]"=Doe \  -d "account[tos_shown_and_accepted]"=true
```

Example 3 (unknown):
```unknown
{  "id": "ct_1BZ6xr2eZvKYlo2CsSOhuTfi",  "object": "token",  "client_ip": "104.198.25.169",  "created": 1513297331,  "livemode": false,  "redaction": null,  "type": "account",  "used": false}
```

Example 4 (unknown):
```unknown
{  "id": "ct_1BZ6xr2eZvKYlo2CsSOhuTfi",  "object": "token",  "client_ip": "104.198.25.169",  "created": 1513297331,  "livemode": false,  "redaction": null,  "type": "account",  "used": false}
```

---

## Create a file link

**URL:** https://docs.stripe.com/api/file_links/create

**Contents:**
- Create a file link
  - Parameters
    - filestringRequired
    - expires_attimestamp
    - metadataobject
  - Returns
- Update a file link
  - Parameters
    - expires_atstring | timestamp
    - metadataobject

Creates a new file link object.

The ID of the file. The file’s purpose must be one of the following: business_icon, business_logo, customer_signature, dispute_evidence, finance_report_run, financial_account_statement, identity_document_downloadable, issuing_regulatory_reporting, pci_document, selfie, sigma_scheduled_query, tax_document_user_upload, terminal_android_apk, or terminal_reader_splashscreen.

The link isn’t usable after this future timestamp.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the file link object if successful and raises an error otherwise.

Updates an existing file link object. Expired links can no longer be updated.

A future timestamp after which the link will no longer be usable, or now to expire the link immediately.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the file link object if successful, and raises an error otherwise.

Retrieves the file link with the given ID.

If the identifier you provide is valid, a file link object returns. If not, Stripe raises an error.

Returns a list of file links.

A dictionary with a data property that contains an array of up to limit file links, starting after the starting_after file link. Each entry in the array is a separate file link object. If there aren’t additional available file links, the resulting array is empty.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/file_links \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d file=file_1Mr23iLkdIwHu7ixQkCV3CBR
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/file_links \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d file=file_1Mr23iLkdIwHu7ixQkCV3CBR
```

Example 3 (unknown):
```unknown
{  "id": "link_1Mr23jLkdIwHu7ix65betcoo",  "object": "file_link",  "created": 1680108075,  "expired": false,  "expires_at": null,  "file": "file_1Mr23iLkdIwHu7ixQkCV3CBR",  "livemode": false,  "metadata": {},  "url": "https://files.stripe.com/links/MDB8YWNjdF8xTTJKVGtMa2RJd0h1N2l4fGZsX3Rlc3RfaXVoY2hrUnJPMzlBR3dPb01XMmFkSTVq00yUPLFf3h"}
```

Example 4 (unknown):
```unknown
{  "id": "link_1Mr23jLkdIwHu7ix65betcoo",  "object": "file_link",  "created": 1680108075,  "expired": false,  "expires_at": null,  "file": "file_1Mr23iLkdIwHu7ixQkCV3CBR",  "livemode": false,  "metadata": {},  "url": "https://files.stripe.com/links/MDB8YWNjdF8xTTJKVGtMa2RJd0h1N2l4fGZsX3Rlc3RfaXVoY2hrUnJPMzlBR3dPb01XMmFkSTVq00yUPLFf3h"}
```

---

## Reconcile a customer_balance PaymentIntent

**URL:** https://docs.stripe.com/api/payment_intents/apply_customer_balance

**Contents:**
- Reconcile a customer_balance PaymentIntent
  - Parameters
    - amountinteger
    - currencyenum
  - Returns
- Search PaymentIntents
  - Parameters
    - querystringRequired
    - limitinteger
    - pagestring

Manually reconcile the remaining amount for a customer_balance PaymentIntent.

Amount that you intend to apply to this PaymentIntent from the customer’s cash balance. If the PaymentIntent was created by an Invoice, the full amount of the PaymentIntent is applied regardless of this parameter.

A positive integer representing how much to charge in the smallest currency unit (for example, 100 cents to charge 1 USD or 100 to charge 100 JPY, a zero-decimal currency). The maximum amount is the amount of the PaymentIntent.

When you omit the amount, it defaults to the remaining amount requested on the PaymentIntent.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

Returns a PaymentIntent object.

Search for PaymentIntents you’ve previously created using Stripe’s Search Query Language. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.

The search query string. See search query language and the list of supported query fields for payment intents.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A dictionary with a data property that contains an array of up to limit PaymentIntents. If no objects match the query, the resulting array will be empty. See the related guide on expanding properties in lists.

Verifies microdeposits on a PaymentIntent object.

Two positive integers, in cents, equal to the values of the microdeposits sent to the bank account.

A six-character code starting with SM present in the microdeposit sent to the bank account.

Returns a PaymentIntent object.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/payment_intents/pi_1GszwY2eZvKYlo2CohCEmT6b/apply_customer_balance \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/payment_intents/pi_1GszwY2eZvKYlo2CohCEmT6b/apply_customer_balance \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "pi_1GszwY2eZvKYlo2CohCEmT6b",  "object": "payment_intent",  "amount": 1000,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 0,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": null,  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_1GszwY2eZvKYlo2CohCEmT6b_secret_1jQJzqkrQvx4BpwI5hn6WSEO5",  "confirmation_method": "automatic",  "created": 1591918582,  "currency": "usd",  "customer": null,  "description": "Created by stripe.com/docs demo",  "last_payment_error": null,  "latest_charge": null,  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": null,  "payment_method_options": {    "card": {      "installments": null,      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    }  },  "payment_method_types": [    "card"  ],  "processing": null,  "receipt_email": null,  "redaction": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "requires_payment_method",  "transfer_data": null,  "transfer_group": null}
```

Example 4 (unknown):
```unknown
{  "id": "pi_1GszwY2eZvKYlo2CohCEmT6b",  "object": "payment_intent",  "amount": 1000,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 0,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": null,  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_1GszwY2eZvKYlo2CohCEmT6b_secret_1jQJzqkrQvx4BpwI5hn6WSEO5",  "confirmation_method": "automatic",  "created": 1591918582,  "currency": "usd",  "customer": null,  "description": "Created by stripe.com/docs demo",  "last_payment_error": null,  "latest_charge": null,  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": null,  "payment_method_options": {    "card": {      "installments": null,      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    }  },  "payment_method_types": [    "card"  ],  "processing": null,  "receipt_email": null,  "redaction": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "requires_payment_method",  "transfer_data": null,  "transfer_group": null}
```

---

## The Confirmation Token object

**URL:** https://docs.stripe.com/api/confirmation_tokens/object

**Contents:**
- The Confirmation Token object
  - Attributes
    - idstring
    - objectstring
    - createdtimestamp
    - expires_atnullable timestamp
    - livemodeboolean
    - mandate_datanullable object
    - payment_intentnullable string
    - payment_method_optionsnullable object

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value.

Time at which the object was created. Measured in seconds since the Unix epoch.

Time at which this ConfirmationToken expires and can no longer be used to confirm a PaymentIntent or SetupIntent.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Data used for generating a Mandate.

ID of the PaymentIntent that this ConfirmationToken was used to confirm, or null if this ConfirmationToken has not yet been used.

Payment-method-specific configuration for this ConfirmationToken.

Payment details collected by the Payment Element, used to create a PaymentMethod when a PaymentIntent or SetupIntent is confirmed with this ConfirmationToken.

Return URL used to confirm the Intent.

Indicates that you intend to make future payments with this ConfirmationToken’s payment method.

The presence of this property will attach the payment method to the PaymentIntent’s Customer, if present, after the PaymentIntent is confirmed and any required actions from the user are complete.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

ID of the SetupIntent that this ConfirmationToken was used to confirm, or null if this ConfirmationToken has not yet been used.

Shipping information collected on this ConfirmationToken.

Indicates whether the Stripe SDK is used to handle confirmation flow. Defaults to true on ConfirmationToken.

Retrieves an existing ConfirmationToken object

Returns the specified ConfirmationToken

Creates a test mode Confirmation Token server side for your integration tests.

ID of an existing PaymentMethod.

If provided, this hash will be used to create a PaymentMethod.

Payment-method-specific configuration for this ConfirmationToken.

Return URL used to confirm the Intent.

Indicates that you intend to make future payments with this ConfirmationToken’s payment method.

The presence of this property will attach the payment method to the PaymentIntent’s Customer, if present, after the PaymentIntent is confirmed and any required actions from the user are complete.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

Shipping information for this ConfirmationToken.

Returns a testmode Confirmation Token

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "ctoken_1NnQUf2eZvKYlo2CIObdtbnb",  "object": "confirmation_token",  "created": 1694025025,  "expires_at": 1694068225,  "livemode": true,  "mandate_data": null,  "payment_intent": null,  "payment_method": null,  "payment_method_preview": {    "billing_details": {      "address": {        "city": "Hyde Park",        "country": "US",        "line1": "50 Sprague St",        "line2": "",        "postal_code": "02136",        "state": "MA"      },      "email": "jennyrosen@stripe.com",      "name": "Jenny Rosen",      "phone": null    },    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": null      },      "country": "US",      "display_brand": "visa",      "exp_month": 8,      "exp_year": 2026,      "funding": "credit",      "generated_from": null,      "last4": "4242",      "networks": {        "available": [          "visa"        ],        "preferred": null      },      "three_d_secure_usage": {        "supported": true      },      "wallet": null    },    "type": "card"  },  "return_url": "https://example.com/return",  "setup_future_usage": "off_session",  "setup_intent": null,  "shipping": {    "address": {      "city": "Hyde Park",      "country": "US",      "line1": "50 Sprague St",      "line2": "",      "postal_code": "02136",      "state": "MA"    },    "name": "Jenny Rosen",    "phone": null  }}
```

Example 2 (unknown):
```unknown
{  "id": "ctoken_1NnQUf2eZvKYlo2CIObdtbnb",  "object": "confirmation_token",  "created": 1694025025,  "expires_at": 1694068225,  "livemode": true,  "mandate_data": null,  "payment_intent": null,  "payment_method": null,  "payment_method_preview": {    "billing_details": {      "address": {        "city": "Hyde Park",        "country": "US",        "line1": "50 Sprague St",        "line2": "",        "postal_code": "02136",        "state": "MA"      },      "email": "jennyrosen@stripe.com",      "name": "Jenny Rosen",      "phone": null    },    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": null      },      "country": "US",      "display_brand": "visa",      "exp_month": 8,      "exp_year": 2026,      "funding": "credit",      "generated_from": null,      "last4": "4242",      "networks": {        "available": [          "visa"        ],        "preferred": null      },      "three_d_secure_usage": {        "supported": true      },      "wallet": null    },    "type": "card"  },  "return_url": "https://example.com/return",  "setup_future_usage": "off_session",  "setup_intent": null,  "shipping": {    "address": {      "city": "Hyde Park",      "country": "US",      "line1": "50 Sprague St",      "line2": "",      "postal_code": "02136",      "state": "MA"    },    "name": "Jenny Rosen",    "phone": null  }}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/confirmation_tokens/ctoken_1NnQUf2eZvKYlo2CIObdtbnb \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/confirmation_tokens/ctoken_1NnQUf2eZvKYlo2CIObdtbnb \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

---

## List all file links

**URL:** https://docs.stripe.com/api/file_links/list

**Contents:**
- List all file links
  - Parameters
  - More parametersExpand all
    - createdobject
    - ending_beforestring
    - expiredboolean
    - filestring
    - limitinteger
    - starting_afterstring
  - Returns

Returns a list of file links.

A dictionary with a data property that contains an array of up to limit file links, starting after the starting_after file link. Each entry in the array is a separate file link object. If there aren’t additional available file links, the resulting array is empty.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v1/file_links \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v1/file_links \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 3 (unknown):
```unknown
{  "object": "list",  "url": "/v1/file_links",  "has_more": false,  "data": [    {      "id": "link_1Mr23jLkdIwHu7ix65betcoo",      "object": "file_link",      "created": 1680108075,      "expired": false,      "expires_at": null,      "file": "file_1Mr23iLkdIwHu7ixQkCV3CBR",      "livemode": false,      "metadata": {},      "url": "https://files.stripe.com/links/MDB8YWNjdF8xTTJKVGtMa2RJd0h1N2l4fGZsX3Rlc3RfaXVoY2hrUnJPMzlBR3dPb01XMmFkSTVq00yUPLFf3h"    }  ]}
```

Example 4 (unknown):
```unknown
{  "object": "list",  "url": "/v1/file_links",  "has_more": false,  "data": [    {      "id": "link_1Mr23jLkdIwHu7ix65betcoo",      "object": "file_link",      "created": 1680108075,      "expired": false,      "expires_at": null,      "file": "file_1Mr23iLkdIwHu7ixQkCV3CBR",      "livemode": false,      "metadata": {},      "url": "https://files.stripe.com/links/MDB8YWNjdF8xTTJKVGtMa2RJd0h1N2l4fGZsX3Rlc3RfaXVoY2hrUnJPMzlBR3dPb01XMmFkSTVq00yUPLFf3h"    }  ]}
```

---

## List all customers

**URL:** https://docs.stripe.com/api/customers/list

**Contents:**
- List all customers
  - Parameters
    - emailstring
  - More parametersExpand all
    - createdobject
    - ending_beforestring
    - limitinteger
    - starting_afterstring
    - test_clockstring
  - Returns

Returns a list of your customers. The customers are returned sorted by creation date, with the most recent customers appearing first.

A case-sensitive filter on the list based on the customer’s email field. The value must be a string.

The maximum length is 512 characters.

A dictionary with a data property that contains an array of up to limit customers, starting after customer starting_after. Passing an optional email will result in filtering to customers with only that exact email address. Each entry in the array is a separate customer object. If no more customers are available, the resulting array will be empty.

Permanently deletes a customer. It cannot be undone. Also immediately cancels any active subscriptions on the customer.

Returns an object with a deleted parameter on success. If the customer ID does not exist, this call raises an error.

Unlike other objects, deleted customers can still be retrieved through the API in order to be able to track their history. Deleting customers removes all credit card details and prevents any further operations to be performed (such as adding a new subscription).

Search for customers you’ve previously created using Stripe’s Search Query Language. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.

The search query string. See search query language and the list of supported query fields for customers.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A dictionary with a data property that contains an array of up to limit customers. If no objects match the query, the resulting array will be empty. See the related guide on expanding properties in lists.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v1/customers \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v1/customers \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 3 (unknown):
```unknown
{  "object": "list",  "url": "/v1/customers",  "has_more": false,  "data": [    {      "id": "cus_NffrFeUfNV2Hib",      "object": "customer",      "address": null,      "balance": 0,      "created": 1680893993,      "currency": null,      "default_source": null,      "delinquent": false,      "description": null,      "email": "jennyrosen@example.com",      "invoice_prefix": "0759376C",      "invoice_settings": {        "custom_fields": null,        "default_payment_method": null,        "footer": null,        "rendering_options": null      },      "livemode": false,      "metadata": {},      "name": "Jenny Rosen",      "next_invoice_sequence": 1,      "phone": null,      "preferred_locales": [],      "shipping": null,      "tax_exempt": "none",      "test_clock": null    }  ]}
```

Example 4 (unknown):
```unknown
{  "object": "list",  "url": "/v1/customers",  "has_more": false,  "data": [    {      "id": "cus_NffrFeUfNV2Hib",      "object": "customer",      "address": null,      "balance": 0,      "created": 1680893993,      "currency": null,      "default_source": null,      "delinquent": false,      "description": null,      "email": "jennyrosen@example.com",      "invoice_prefix": "0759376C",      "invoice_settings": {        "custom_fields": null,        "default_payment_method": null,        "footer": null,        "rendering_options": null      },      "livemode": false,      "metadata": {},      "name": "Jenny Rosen",      "next_invoice_sequence": 1,      "phone": null,      "preferred_locales": [],      "shipping": null,      "tax_exempt": "none",      "test_clock": null    }  ]}
```

---

## Subscription Schedule

**URL:** https://docs.stripe.com/api/subscription_schedules

**Contents:**
- Subscription Schedule
- The Subscription Schedule object
  - Attributes
    - idstring
    - current_phasenullable object
    - customerstringExpandable
    - metadatanullable object
    - phasesarray of objects
    - statusenum
    - subscriptionnullable stringExpandable

A subscription schedule allows you to create and manage the lifecycle of a subscription by predefining expected changes.

Related guide: Subscription schedules

Unique identifier for the object.

Object representing the start and end dates for the current phase of the subscription schedule, if it is active.

ID of the customer who owns the subscription schedule.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Configuration for the subscription schedule’s phases.

The present status of the subscription schedule. Possible values are not_started, active, completed, released, and canceled. You can read more about the different states in our behavior guide.

ID of the subscription managed by the subscription schedule.

Creates a new subscription schedule object. Each customer can have up to 500 active or scheduled subscriptions.

The identifier of the customer to create the subscription schedule for.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

List representing phases of the subscription schedule. Each phase can be customized to have different durations, plans, and coupons. If there are multiple phases, the end_date of one phase will always equal the start_date of the next phase.

When the subscription schedule starts. We recommend using now so that it starts the subscription immediately. You can also use a Unix timestamp to backdate the subscription so that it starts on a past date, or set a future date for the subscription to start on.

Returns a subscription schedule object if the call succeeded.

Updates an existing subscription schedule.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

List representing phases of the subscription schedule. Each phase can be customized to have different durations, plans, and coupons. If there are multiple phases, the end_date of one phase will always equal the start_date of the next phase. Note that past phases can be omitted.

If the update changes the billing configuration (item price, quantity, etc.) of the current phase, indicates how prorations from this change should be handled. The default value is create_prorations.

Prorate changes, and force an invoice to be immediately created for any prorations.

Prorate changes, but leave any prorations as pending invoice items to be picked up on the customer’s next invoice.

Does not create any prorations.

Returns an updated subscription schedule object if the call succeeded.

Retrieves the details of an existing subscription schedule. You only need to supply the unique subscription schedule identifier that was returned upon subscription schedule creation.

Returns a subscription schedule object if a valid identifier was provided.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/subscription_schedules \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_NcI8FsMbh0OeFs \  -d start_date=1787130418 \  -d end_behavior=release \  -d "phases[0][items][0][price]"=price_1Mr3YcLkdIwHu7ixYCFhXHNb \  -d "phases[0][items][0][quantity]"=1 \  -d "phases[0][duration][interval]"=month \  -d "phases[0][duration][interval_count]"=1
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/subscription_schedules \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_NcI8FsMbh0OeFs \  -d start_date=1787130418 \  -d end_behavior=release \  -d "phases[0][items][0][price]"=price_1Mr3YcLkdIwHu7ixYCFhXHNb \  -d "phases[0][items][0][quantity]"=1 \  -d "phases[0][duration][interval]"=month \  -d "phases[0][duration][interval_count]"=1
```

Example 3 (unknown):
```unknown
{  "id": "sub_sched_1Mr3YdLkdIwHu7ixjop3qtff",  "object": "subscription_schedule",  "application": null,  "canceled_at": null,  "completed_at": null,  "created": 1724058651,  "current_phase": null,  "customer": "cus_NcI8FsMbh0OeFs",  "default_settings": {    "application_fee_percent": null,    "automatic_tax": {      "enabled": false,      "liability": null    },    "billing_cycle_anchor": "automatic",    "collection_method": "charge_automatically",    "default_payment_method": null,    "default_source": null,    "description": null,    "invoice_settings": {      "issuer": {        "type": "self"      }    },    "on_behalf_of": null,    "transfer_data": null  },  "end_behavior": "release",  "livemode": false,  "metadata": {},  "phases": [    {      "add_invoice_items": [],      "application_fee_percent": null,      "billing_cycle_anchor": null,      "collection_method": null,      "currency": "usd",      "default_payment_method": null,      "default_tax_rates": [],      "description": null,      "discounts": null,      "end_date": 1818666418,      "invoice_settings": null,      "items": [        {          "discounts": null,          "metadata": {},          "plan": "price_1Mr3YcLkdIwHu7ixYCFhXHNb",          "price": "price_1Mr3YcLkdIwHu7ixYCFhXHNb",          "quantity": 1,          "tax_rates": []        }      ],      "metadata": {},      "on_behalf_of": null,      "proration_behavior": "create_prorations",      "start_date": 1787130418,      "transfer_data": null,      "trial_end": null    }  ],  "released_at": null,  "released_subscription": null,  "renewal_interval": null,  "status": "not_started",  "subscription": null,  "test_clock": null}
```

Example 4 (unknown):
```unknown
{  "id": "sub_sched_1Mr3YdLkdIwHu7ixjop3qtff",  "object": "subscription_schedule",  "application": null,  "canceled_at": null,  "completed_at": null,  "created": 1724058651,  "current_phase": null,  "customer": "cus_NcI8FsMbh0OeFs",  "default_settings": {    "application_fee_percent": null,    "automatic_tax": {      "enabled": false,      "liability": null    },    "billing_cycle_anchor": "automatic",    "collection_method": "charge_automatically",    "default_payment_method": null,    "default_source": null,    "description": null,    "invoice_settings": {      "issuer": {        "type": "self"      }    },    "on_behalf_of": null,    "transfer_data": null  },  "end_behavior": "release",  "livemode": false,  "metadata": {},  "phases": [    {      "add_invoice_items": [],      "application_fee_percent": null,      "billing_cycle_anchor": null,      "collection_method": null,      "currency": "usd",      "default_payment_method": null,      "default_tax_rates": [],      "description": null,      "discounts": null,      "end_date": 1818666418,      "invoice_settings": null,      "items": [        {          "discounts": null,          "metadata": {},          "plan": "price_1Mr3YcLkdIwHu7ixYCFhXHNb",          "price": "price_1Mr3YcLkdIwHu7ixYCFhXHNb",          "quantity": 1,          "tax_rates": []        }      ],      "metadata": {},      "on_behalf_of": null,      "proration_behavior": "create_prorations",      "start_date": 1787130418,      "transfer_data": null,      "trial_end": null    }  ],  "released_at": null,  "released_subscription": null,  "renewal_interval": null,  "status": "not_started",  "subscription": null,  "test_clock": null}
```

---

## Update a PaymentMethod

**URL:** https://docs.stripe.com/api/payment_methods/update

**Contents:**
- Update a PaymentMethod
  - Parameters
    - billing_detailsobject
    - metadataobject
  - More parametersExpand all
    - allow_redisplayenum
    - cardobject
    - paytoobject
    - us_bank_accountobject
  - Returns

Updates a PaymentMethod object. A PaymentMethod must be attached to a customer to be updated.

Billing information associated with the PaymentMethod that may be used or required by particular types of payment methods.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a PaymentMethod object.

Retrieves a PaymentMethod object for a given Customer.

Returns a PaymentMethod object.

Retrieves a PaymentMethod object attached to the StripeAccount. To retrieve a payment method attached to a Customer, you should use Retrieve a Customer’s PaymentMethods

Returns a PaymentMethod object.

Returns a list of PaymentMethods for a given Customer

An optional filter on the list, based on the object type field. Without the filter, the list includes all current and future payment method types. If your integration expects only one type of payment method in the response, make sure to provide a type value in the request.

A dictionary with a data property that contains an array of up to limit PaymentMethods of type type, starting after PaymentMethods starting_after. Each entry in the array is a separate PaymentMethod object. If no more PaymentMethods are available, the resulting array will be empty.

Returns a list of all PaymentMethods.

Filters the list by the object type field. Unfiltered, the list returns all payment method types except custom. If your integration expects only one type of payment method in the response, specify that type value in the request to reduce your payload.

A dictionary with a data property that contains an array of up to limit PaymentMethods of type type, starting after PaymentMethods starting_after. Each entry in the array is a separate PaymentMethod object. If no more PaymentMethods are available, the resulting array will be empty.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_methods/pm_1Q0PsIJvEtkwdCNYMSaVuRz6 \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_methods/pm_1Q0PsIJvEtkwdCNYMSaVuRz6 \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

Example 3 (unknown):
```unknown
{  "id": "pm_1Q0PsIJvEtkwdCNYMSaVuRz6",  "object": "payment_method",  "allow_redisplay": "unspecified",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": "John Doe",    "phone": null  },  "created": 1726673582,  "customer": null,  "livemode": false,  "metadata": {    "order_id": "6735"  },  "type": "us_bank_account",  "us_bank_account": {    "account_holder_type": "individual",    "account_type": "checking",    "bank_name": "STRIPE TEST BANK",    "financial_connections_account": null,    "fingerprint": "LstWJFsCK7P349Bg",    "last4": "6789",    "networks": {      "preferred": "ach",      "supported": [        "ach"      ]    },    "routing_number": "110000000",    "status_details": {}  }}
```

Example 4 (unknown):
```unknown
{  "id": "pm_1Q0PsIJvEtkwdCNYMSaVuRz6",  "object": "payment_method",  "allow_redisplay": "unspecified",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": "John Doe",    "phone": null  },  "created": 1726673582,  "customer": null,  "livemode": false,  "metadata": {    "order_id": "6735"  },  "type": "us_bank_account",  "us_bank_account": {    "account_holder_type": "individual",    "account_type": "checking",    "bank_name": "STRIPE TEST BANK",    "financial_connections_account": null,    "fingerprint": "LstWJFsCK7P349Bg",    "last4": "6789",    "networks": {      "preferred": "ach",      "supported": [        "ach"      ]    },    "routing_number": "110000000",    "status_details": {}  }}
```

---

## Person Tokens v2

**URL:** https://docs.stripe.com/api/v2/person-tokens

**Contents:**
- Person Tokens v2
- The PersonToken object
  - Attributes
    - idstring
    - objectstring, value is "v2.core.account_person_token"
    - createdtimestamp
    - expires_attimestamp
    - livemodeboolean
    - usedboolean
- Create a person token v2

Person Tokens are single-use tokens which tokenize person information, and are used for creating or updating a Person.

Unique identifier for the token.

String representing the object’s type. Objects of the same type share the same value of the object field.

Time at which the token was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Time at which the token will expire.

Has the value true if the token exists in live mode or the value false if the object exists in test mode.

Determines if the token has already been used (tokens can only be used once).

Creates a Person Token associated with an Account.

The Account the Person is associated with.

Additional addresses associated with the person.

Additional names (e.g. aliases) associated with the person.

Attestations of accepted terms of service agreements.

The person’s residential address.

The person’s date of birth.

Documents that may be submitted to satisfy various informational requests.

The person’s first name.

The identification numbers (e.g., SSN) associated with the person.

The person’s gender (International regulations require either “male” or “female”).

Female gender person.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The nationalities (countries) this person is associated with.

The phone number for this person.

The person’s political exposure.

The person has disclosed that they do have political exposure.

The person has disclosed that they have no political exposure.

The relationship that this person has with the Account’s business or legal entity.

The script addresses (e.g., non-Latin characters) associated with the person.

The script names (e.g. non-Latin characters) associated with the person.

The person’s last name.

Unique identifier for the token.

String representing the object’s type. Objects of the same type share the same value of the object field.

Time at which the token was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Time at which the token will expire.

Has the value true if the token exists in live mode or the value false if the object exists in test mode.

Determines if the token has already been used (tokens can only be used once).

Token must be created with publishable key.

Retrieves a Person Token associated with an Account.

The Account the Person is associated with.

The ID of the Person Token to retrieve.

Unique identifier for the token.

String representing the object’s type. Objects of the same type share the same value of the object field.

Time at which the token was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Time at which the token will expire.

Has the value true if the token exists in live mode or the value false if the object exists in test mode.

Determines if the token has already been used (tokens can only be used once).

The resource wasn’t found.

**Examples:**

Example 1 (unknown):
```unknown
{  "created": "2025-01-01T00:00:00.000Z",  "expires_at": "2025-01-01T00:00:00.000Z",  "id": "4242",  "livemode": true,  "object": "4242",  "used": true}
```

Example 2 (unknown):
```unknown
{  "created": "2025-01-01T00:00:00.000Z",  "expires_at": "2025-01-01T00:00:00.000Z",  "id": "4242",  "livemode": true,  "object": "4242",  "used": true}
```

Example 3 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/person_tokens \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "given_name": "Jenny",    "surname": "Rosen",    "email": "jenny.rosen@example.com",    "address": {        "line1": "27 Fredrick Ave",        "city": "Brothers",        "postal_code": "97712",        "state": "OR",        "country": "US"    },    "id_numbers": [        {            "type": "us_ssn_last_4",            "value": "0000"        }    ],    "relationship": {        "owner": true,        "percent_ownership": "0.8",        "representative": true,        "title": "CEO"    }  }'
```

Example 4 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/person_tokens \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "given_name": "Jenny",    "surname": "Rosen",    "email": "jenny.rosen@example.com",    "address": {        "line1": "27 Fredrick Ave",        "city": "Brothers",        "postal_code": "97712",        "state": "OR",        "country": "US"    },    "id_numbers": [        {            "type": "us_ssn_last_4",            "value": "0000"        }    ],    "relationship": {        "owner": true,        "percent_ownership": "0.8",        "representative": true,        "title": "CEO"    }  }'
```

---

## List all PaymentIntent LineItems

**URL:** https://docs.stripe.com/api/payment_intents/amount_details_line_items

**Contents:**
- List all PaymentIntent LineItems
  - Parameters
  - More parametersExpand all
    - ending_beforestring
    - limitinteger
    - starting_afterstring
  - Returns
- List all PaymentIntents
  - Parameters
    - customerstring

Lists all LineItems of a given PaymentIntent.

A dictionary with a data property that contains an array of up to limit line items of the given PaymentIntent, starting after line item starting_after. Each entry in the array is a separate line item object. If no other line items are available, the resulting array is empty.

Returns a list of PaymentIntents.

Only return PaymentIntents for the customer that this customer ID specifies.

Only return PaymentIntents for the account representing the customer that this ID specifies.

A dictionary with a data property that contains an array of up to limit PaymentIntents, starting after PaymentIntent starting_after. Each entry in the array is a separate PaymentIntent object. If no other PaymentIntents are available, the resulting array is empty.

You can cancel a PaymentIntent object when it’s in one of these statuses: requires_payment_method, requires_capture, requires_confirmation, requires_action or, in rare cases, processing.

After it’s canceled, no additional charges are made by the PaymentIntent and any operations on the PaymentIntent fail with an error. For PaymentIntents with a status of requires_capture, the remaining amount_capturable is automatically refunded.

You can’t cancel the PaymentIntent for a Checkout Session. Expire the Checkout Session instead.

Reason for canceling this PaymentIntent. Possible values are: duplicate, fraudulent, requested_by_customer, or abandoned

Returns a PaymentIntent object if the cancellation succeeds. Returns an error if the PaymentIntent is already canceled or isn’t in a cancelable state.

Capture the funds of an existing uncaptured PaymentIntent when its status is requires_capture.

Uncaptured PaymentIntents are cancelled a set number of days (7 by default) after their creation.

Learn more about separate authorization and capture.

The amount to capture from the PaymentIntent, which must be less than or equal to the original amount. Defaults to the full amount_capturable if it’s not provided.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a PaymentIntent object with status="succeeded" if the PaymentIntent is capturable. Returns an error if the PaymentIntent isn’t capturable or if an invalid amount to capture is provided.

Confirm that your customer intends to pay with current or provided payment method. Upon confirmation, the PaymentIntent will attempt to initiate a payment.

If the selected payment method requires additional authentication steps, the PaymentIntent will transition to the requires_action status and suggest additional actions via next_action. If payment fails, the PaymentIntent transitions to the requires_payment_method status or the canceled status if the confirmation limit is reached. If payment succeeds, the PaymentIntent will transition to the succeeded status (or requires_capture, if capture_method is set to manual).

If the confirmation_method is automatic, payment may be attempted using our client SDKs and the PaymentIntent’s client_secret. After next_actions are handled by the client, no additional confirmation is required to complete the payment.

If the confirmation_method is manual, all payment attempts must be initiated using a secret key.

If any actions are required for the payment, the PaymentIntent will return to the requires_confirmation state after those actions are completed. Your server needs to then explicitly re-confirm the PaymentIntent to initiate the next payment attempt.

There is a variable upper limit on how many times a PaymentIntent can be confirmed. After this limit is reached, any further calls to this endpoint will transition the PaymentIntent to the canceled state.

ID of the payment method (a PaymentMethod, Card, or compatible Source object) to attach to this PaymentIntent. If the payment method is attached to a Customer, it must match the customer that is set on this PaymentIntent.

Email address that the receipt for the resulting payment will be sent to. If receipt_email is specified for a payment in live mode, a receipt will be sent regardless of your email settings.

Indicates that you intend to make future payments with this PaymentIntent’s payment method.

If you provide a Customer with the PaymentIntent, you can use this parameter to attach the payment method to the Customer after the PaymentIntent is confirmed and the customer completes any required actions. If you don’t provide a Customer, you can still attach the payment method to a Customer after the transaction completes.

If the payment method is card_present and isn’t a digital wallet, Stripe creates and attaches a generated_card payment method representing the card to the Customer instead.

When processing card payments, Stripe uses setup_future_usage to help you comply with regional legislation and network rules, such as SCA.

If you’ve already set setup_future_usage and you’re performing a request using a publishable key, you can only update the value from on_session to off_session.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

Shipping information for this PaymentIntent.

Returns the resulting PaymentIntent after all possible transitions are applied.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents/pi_3MtwBwLkdIwHu7ix28a3tqPa/amount_details_line_items \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents/pi_3MtwBwLkdIwHu7ix28a3tqPa/amount_details_line_items \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "object": "list",  "url": "/v1/payment_intents/pi_3MtwBwLkdIwHu7ix28a3tqPa/amount_details_line_items",  "has_more": false,  "data": [    {      "id": "uli_T1KmwLEvkprqQb",      "object": "payment_intent_amount_details_line_item",      "discount_amount": 50,      "payment_method_options": null,      "product_code": "SKU001",      "product_name": "Product 001",      "quantity": 1,      "tax": {        "total_tax_amount": 20      },      "unit_cost": 2000,      "unit_of_measure": "each"    }  ]}
```

Example 4 (unknown):
```unknown
{  "object": "list",  "url": "/v1/payment_intents/pi_3MtwBwLkdIwHu7ix28a3tqPa/amount_details_line_items",  "has_more": false,  "data": [    {      "id": "uli_T1KmwLEvkprqQb",      "object": "payment_intent_amount_details_line_item",      "discount_amount": 50,      "payment_method_options": null,      "product_code": "SKU001",      "product_name": "Product 001",      "quantity": 1,      "tax": {        "total_tax_amount": 20      },      "unit_cost": 2000,      "unit_of_measure": "each"    }  ]}
```

---

## Terminal SDK migration guide

**URL:** https://docs.stripe.com/terminal/references/sdk-migration-guide

**Contents:**
- Terminal SDK migration guide
- Learn how to migrate to version 5.0.0 of the Stripe Terminal SDK.
    - Note
- Migrate to version 5.0.0
- Update your minimum supported version to iOS 15 or higher
- Simplified payment integration
  - Update to unified payment processing
    - Processing payments with processPaymentIntent
    - Processing refunds with processRefund
    - Processing setup intents with processSetupIntent

The Stripe Terminal iOS and Android SDKs have been updated with a number of breaking changes in APIs and behavior, some of which require you to update your integration with the Stripe Terminal SDK. To improve consistency between our SDKs and to simplify your application logic and integration, we regularly make changes in major version updates that might affect the way your integration works or behaves. This guide explains the latest changes to help you upgrade your integration.

Building a new Stripe Terminal integration? Visit our Design an integration page to learn how to get started.

Here’s what you need to know about the version 5.0.0 Stripe Terminal iOS and Android SDKs:

If your application currently uses a Terminal iOS SDK version earlier than 5.0.0, there are several changes you need to make to upgrade. For a detailed list of the changes from version 4.x to 5.0.0, see the SDK changelog.

We regularly update the minimum supported version of our SDKs to streamline our developer support efforts.

Existing 4.X versions of the Terminal iOS SDK will continue to support devices running iOS 14 and higher.

The v5 SDK includes methods that combine the collect and confirm steps into a single operation. While the existing collectPaymentMethod and confirmPaymentIntent methods continue to work, we recommend using the unified methods for simpler integrations.

Replace two-step collect and confirm with a single processPaymentIntent method call.

The collectRefundPaymentMethod and confirmRefund methods are now deprecated. Use processRefund instead.

Replace two-step collect and confirm with a single processSetupIntent method call.

The SDK now provides async variants for Terminal methods. You can write cleaner, sequential code instead of nesting completion handlers.

The setTokenProvider method has been removed. You must now initialize the SDK with the static Terminal.initWithTokenProvider(_tokenProvider:) method before accessing the Terminal.shared singleton.

You can no longer initialize DiscoveryConfiguration objects directly with init or new. You must now use their associated builder classes.

A new .reconnecting value has been added to the ConnectionStatus enum. During a reconnect, Terminal.shared.connectedReader will now be nil until the reconnection is successful.

For smart readers and Tap to Pay integrations using iOS SDK 5.1 or newer, you can now use Terminal.shared.easyConnect, which combines discovery and connection into a single method call.

Internet reader discovery now supports filtering by reader ID or serial number. Set the discoveryFilter property on InternetDiscoveryConfigurationBuilder to discover a specific reader.

On supported readers, the ability for customers to cancel transactions is now enabled by default. The customerCancellation property has changed from a Bool to the new SCPCustomerCancellation enum.

If you create SCPRefundParameters for an Interac refund using a PaymentIntent ID, you must now also pass the PaymentIntent’s clientSecret. You can alternatively continue using the charge ID, which doesn’t require the clientSecret.

**Examples:**

Example 1 (javascript):
```javascript
// Step 1: Collect payment method
Terminal.shared.collectPaymentMethod(paymentIntent, collectConfig: collectConfig) { collectedPaymentIntent, collectError in
    guard let collectedPaymentIntent = collectedPaymentIntent else {
        // Payment method collection failed
        return
    }
    // Step 2: Confirm the payment
    Terminal.shared.confirmPaymentIntent(collectedPaymentIntent) { confirmedPaymentIntent, confirmError in
        if let confirmedPaymentIntent = confirmedPaymentIntent {
            // Payment successful
        } else {
            // Payment confirmation failed
        }
    }
}
```

Example 2 (javascript):
```javascript
// Step 1: Collect payment method
Terminal.shared.collectPaymentMethod(paymentIntent, collectConfig: collectConfig) { collectedPaymentIntent, collectError in
    guard let collectedPaymentIntent = collectedPaymentIntent else {
        // Payment method collection failed
        return
    }
    // Step 2: Confirm the payment
    Terminal.shared.confirmPaymentIntent(collectedPaymentIntent) { confirmedPaymentIntent, confirmError in
        if let confirmedPaymentIntent = confirmedPaymentIntent {
            // Payment successful
        } else {
            // Payment confirmation failed
        }
    }
}
```

Example 3 (javascript):
```javascript
// Process and confirm the payment in one step
Terminal.shared.processPaymentIntent(paymentIntent, collectConfig: collectConfig) { processedPaymentIntent, processError in
    if let processedPaymentIntent = processedPaymentIntent {
        // Payment successful
    } else {
        // Payment failed
    }
}
```

Example 4 (javascript):
```javascript
// Process and confirm the payment in one step
Terminal.shared.processPaymentIntent(paymentIntent, collectConfig: collectConfig) { processedPaymentIntent, processError in
    if let processedPaymentIntent = processedPaymentIntent {
        // Payment successful
    } else {
        // Payment failed
    }
}
```

---

## Versioning

**URL:** https://docs.stripe.com/api/versioning

**Contents:**
- Versioning

Each major release, such as Acacia, includes changes that aren’t backward-compatible with previous releases. Upgrading to a new major release can require updates to existing code. Each monthly release includes only backward-compatible changes, and uses the same name as the last major release. You can safely upgrade to a new monthly release without breaking any existing code. The current version is 2025-12-15.clover. For information on all API versions, view our API changelog.

You can upgrade your API version in Workbench. As a precaution, use API versioning to test a new API version before committing to an upgrade.

---

## Financing Offer Preview

**URL:** https://docs.stripe.com/api/capital/financing_offers

**Contents:**
- Financing Offer Preview
- The Financing offer object Preview
  - Attributes
    - idstring
    - objectstring
    - accepted_termsnullable object
    - accountstring
    - charged_off_atnullable timestamp
    - createdinteger
    - expires_afterfloat

This is an object representing an offer of financing from Stripe Capital to a Connect subaccount.

A unique identifier for the financing object.

The object type: financing_offer.

Information about the current financing object. Describes currency, advance amount, fee amount, withhold rate, and fee discount of previous financing.

The ID of the merchant associated with this financing object.

The time at which this financing offer was charged off, if applicable. Given in seconds since unix epoch.

Time at which the offer was created. Given in seconds since unix epoch.

Time at which the offer expires. Given in seconds since unix epoch.

The type of financing being offered.

Capital’s Merchant Cash Advance program.

Capital’s fixed-term loan offering. See the integration guide for more information.

Capital’s flex loan offering. See the integration guide for more information.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the financing offer. Describes currency, offered advance amount, offered fee amount, campaign type, withhold rate, and fee discount rate of previous financing.

Financing product identifier.

A “refill” financing offer extended through Stripe Capital. Refills are a form of discounted refinancing. See the integration guide for more information.

A standard financing offer extended through Stripe Capital.

The ID of the financing offer that replaced this offer.

The ID of the financing offer that this offer is a replacement for.

The current status of the offer.

Set once an offer has been accepted by the Connected account.

Set when the Connected account has reached out to Capital’s servicing team within 48 hours of acceptance and requested cancellation of their offer.

Set when the financing offer has fully repaid. This status is no longer in use. See fully_repaid instead.

Once an offer has been delivered, mark it so using the mark_delivered endpoint.

Set when the financing offer has expired, usually 30 days after creation.

Set when the financing offer has been fully repaid.

Set once an offer has been paid out to the Connected account.

Set when Capital’s servicing team has rejected the application for financing. The Connected account receives an email with the reason for rejection.

Set when the financing offer has been replaced.

All offers begin in this state. A financing offer must be delivered to its Connected account using approved marketing materials.

Hash containing timestamps of when the offer transitioned to a particular status.

Get the details of the financing offer

Returns the financing offer object

Retrieves the financing offers available for Connected accounts that belong to your platform.

limit list to offers belonging to given connected account

Only return offers that were created during the given date interval.

limit list to offers with given status

Returns a list of financing offers for Connected accounts on your platform.

Acknowledges that platform has received and delivered the financing_offer to the intended merchant recipient.

Returns the financing offer object

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "financingoffer_1NPvKg2eZvKYlo2CnEEmlCVh",  "object": "capital.financing_offer",  "account": "acct_1NPvKgBY65lDjjDk",  "created": 1688423699,  "expires_after": 1690934400,  "financing_type": "flex_loan",  "livemode": true,  "offered_terms": {    "advance_amount": 10000,    "campaign_type": "newly_eligible_user",    "currency": "usd",    "fee_amount": 1000,    "previous_financing_fee_discount_rate": null,    "withhold_rate": 0.05  },  "product_type": "standard",  "status": "undelivered"}
```

Example 2 (unknown):
```unknown
{  "id": "financingoffer_1NPvKg2eZvKYlo2CnEEmlCVh",  "object": "capital.financing_offer",  "account": "acct_1NPvKgBY65lDjjDk",  "created": 1688423699,  "expires_after": 1690934400,  "financing_type": "flex_loan",  "livemode": true,  "offered_terms": {    "advance_amount": 10000,    "campaign_type": "newly_eligible_user",    "currency": "usd",    "fee_amount": 1000,    "previous_financing_fee_discount_rate": null,    "withhold_rate": 0.05  },  "product_type": "standard",  "status": "undelivered"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/capital/financing_offers/financingoffer_1NPvKg2eZvKYlo2CnEEmlCVh \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/capital/financing_offers/financingoffer_1NPvKg2eZvKYlo2CnEEmlCVh \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

---

## The File object

**URL:** https://docs.stripe.com/api/files/object

**Contents:**
- The File object
  - Attributes
    - idstring
    - purposeenum
    - typenullable string
  - More attributesExpand all
    - objectstring
    - createdtimestamp
    - expires_atnullable timestamp
    - filenamenullable string

Unique identifier for the object.

The purpose of the uploaded file.

Additional documentation requirements that can be requested for an account.

Additional verification for custom accounts.

Customer signature image.

Evidence to submit with a dispute response.

User-accessible copies of query results from the Reporting dataset.

Financial account statements.

A document to verify the identity of an account owner during account provisioning.

Image of a document collected by Stripe Identity.

The returned file type (for example, csv, pdf, jpg, or png).

To upload a file to Stripe, you need to send a request of type multipart/form-data. Include the file you want to upload in the request, and the parameters for creating a file.

All of Stripe’s officially supported Client libraries support sending multipart/form-data.

A file to upload. Make sure that the specifications follow RFC 2388, which defines file transfers for the multipart/form-data protocol.

The purpose of the uploaded file.

Additional documentation requirements that can be requested for an account.

Additional verification for custom accounts.

Customer signature image.

Evidence to submit with a dispute response.

A document to verify the identity of an account owner during account provisioning.

Additional regulatory reporting requirements for Issuing.

A self-assessment PCI questionnaire.

A copy of the platform’s Terms of Service.

Returns the file object.

Retrieves the details of an existing file object. After you supply a unique file ID, Stripe returns the corresponding file object. Learn how to access file contents.

If the identifier you provide is valid, a file object returns. If not, Stripe raises an error.

Returns a list of the files that your account has access to. Stripe sorts and returns the files by their creation dates, placing the most recently created files at the top.

Filter queries by the file purpose. If you don’t provide a purpose, the queries return unfiltered files.

A dictionary with a data property that contains an array of up to limit files, starting after the starting_after file. Each entry in the array is a separate file object. If there aren’t additional available files, the resulting array is empty.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "file_1Mr4LDLkdIwHu7ixFCz0dZiH",  "object": "file",  "created": 1680116847,  "expires_at": 1703444847,  "filename": "file.png",  "links": {    "object": "list",    "data": [],    "has_more": false,    "url": "/v1/file_links?file=file_1Mr4LDLkdIwHu7ixFCz0dZiH"  },  "purpose": "dispute_evidence",  "size": 8429,  "title": null,  "type": "png",  "url": "https://files.stripe.com/v1/files/file_1Mr4LDLkdIwHu7ixFCz0dZiH/contents"}
```

Example 2 (unknown):
```unknown
{  "id": "file_1Mr4LDLkdIwHu7ixFCz0dZiH",  "object": "file",  "created": 1680116847,  "expires_at": 1703444847,  "filename": "file.png",  "links": {    "object": "list",    "data": [],    "has_more": false,    "url": "/v1/file_links?file=file_1Mr4LDLkdIwHu7ixFCz0dZiH"  },  "purpose": "dispute_evidence",  "size": 8429,  "title": null,  "type": "png",  "url": "https://files.stripe.com/v1/files/file_1Mr4LDLkdIwHu7ixFCz0dZiH/contents"}
```

Example 3 (unknown):
```unknown
curl https://files.stripe.com/v1/files \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -F purpose=dispute_evidence \  -F file="@/path/to/a/file.jpg"
```

Example 4 (unknown):
```unknown
curl https://files.stripe.com/v1/files \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -F purpose=dispute_evidence \  -F file="@/path/to/a/file.jpg"
```

---

## Create a product

**URL:** https://docs.stripe.com/api/products/create

**Contents:**
- Create a product
  - Parameters
    - namestringRequired
    - activeboolean
    - descriptionstring
    - idstring
    - metadataobject
    - tax_codestringRecommended if calculating taxes
  - More parametersExpand all
    - default_price_dataobject

Creates a new product object.

The product’s name, meant to be displayable to the customer.

Whether the product is currently available for purchase. Defaults to true.

The product’s description, meant to be displayable to the customer. Use this field to optionally store a long form explanation of the product being sold for your own rendering purposes.

An identifier will be randomly generated by Stripe. You can optionally override this ID, but the ID must be unique across all products in your Stripe account.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a product object if the call succeeded.

Updates the specific product by setting the values of the parameters passed. Any parameters not provided will be left unchanged.

Whether the product is available for purchase.

The ID of the Price object that is the default price for this product.

The product’s description, meant to be displayable to the customer. Use this field to optionally store a long form explanation of the product being sold for your own rendering purposes.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The product’s name, meant to be displayable to the customer.

Returns the product object if the update succeeded.

Retrieves the details of an existing product. Supply the unique product ID from either a product creation request or the product list, and Stripe will return the corresponding product information.

Returns a product object if a valid identifier was provided.

Returns a list of your products. The products are returned sorted by creation date, with the most recently created products appearing first.

Only return products that are active or inactive (e.g., pass false to list all inactive products).

A dictionary with a data property that contains an array of up to limit products, starting after product starting_after. Each entry in the array is a separate product object. If no more products are available, the resulting array will be empty.

Delete a product. Deleting a product is only possible if it has no prices associated with it. Additionally, deleting a product with type=good is only possible if it has no SKUs associated with it.

Returns a deleted object on success. Otherwise, this call raises an error.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/products \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d name="Gold Plan"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/products \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d name="Gold Plan"
```

Example 3 (unknown):
```unknown
{  "id": "prod_NWjs8kKbJWmuuc",  "object": "product",  "active": true,  "created": 1678833149,  "default_price": null,  "description": null,  "images": [],  "marketing_features": [],  "livemode": false,  "metadata": {},  "name": "Gold Plan",  "package_dimensions": null,  "shippable": null,  "statement_descriptor": null,  "tax_code": null,  "unit_label": null,  "updated": 1678833149,  "url": null}
```

Example 4 (unknown):
```unknown
{  "id": "prod_NWjs8kKbJWmuuc",  "object": "product",  "active": true,  "created": 1678833149,  "default_price": null,  "description": null,  "images": [],  "marketing_features": [],  "livemode": false,  "metadata": {},  "name": "Gold Plan",  "package_dimensions": null,  "shippable": null,  "statement_descriptor": null,  "tax_code": null,  "unit_label": null,  "updated": 1678833149,  "url": null}
```

---

## List all refunds

**URL:** https://docs.stripe.com/api/refunds/list

**Contents:**
- List all refunds
  - Parameters
    - chargestring
    - payment_intentstring
  - More parametersExpand all
    - createdobject
    - ending_beforestring
    - limitinteger
    - starting_afterstring
  - Returns

Returns a list of all refunds you created. We return the refunds in sorted order, with the most recent refunds appearing first. The 10 most recent refunds are always available by default on the Charge object.

Only return refunds for the charge specified by this charge ID.

Only return refunds for the PaymentIntent specified by this ID.

A dictionary with a data property that contains an array of up to limit refunds, starting after the starting_after refund. Each entry in the array is a separate Refund object. If no other refunds are available, the resulting array is empty. If you provide a non-existent charge ID, this call raises an error.

Cancels a refund with a status of requires_action.

You can’t cancel refunds in other states. Only refunds for payment methods that require customer action can enter the requires_action state.

Returns the refund object if the cancellation succeeds. This call raises an error if you can’t cancel the refund.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v1/refunds \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v1/refunds \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 3 (unknown):
```unknown
{  "object": "list",  "url": "/v1/refunds",  "has_more": false,  "data": [    {      "id": "re_1Nispe2eZvKYlo2Cd31jOCgZ",      "object": "refund",      "amount": 1000,      "balance_transaction": "txn_1Nispe2eZvKYlo2CYezqFhEx",      "charge": "ch_1NirD82eZvKYlo2CIvbtLWuY",      "created": 1692942318,      "currency": "usd",      "destination_details": {        "card": {          "reference": "123456789012",          "reference_status": "available",          "reference_type": "acquirer_reference_number",          "type": "refund"        },        "type": "card"      },      "metadata": {},      "payment_intent": "pi_1GszsK2eZvKYlo2CfhZyoZLp",      "reason": null,      "receipt_number": null,      "source_transfer_reversal": null,      "status": "succeeded",      "transfer_reversal": null    }  ]}
```

Example 4 (unknown):
```unknown
{  "object": "list",  "url": "/v1/refunds",  "has_more": false,  "data": [    {      "id": "re_1Nispe2eZvKYlo2Cd31jOCgZ",      "object": "refund",      "amount": 1000,      "balance_transaction": "txn_1Nispe2eZvKYlo2CYezqFhEx",      "charge": "ch_1NirD82eZvKYlo2CIvbtLWuY",      "created": 1692942318,      "currency": "usd",      "destination_details": {        "card": {          "reference": "123456789012",          "reference_status": "available",          "reference_type": "acquirer_reference_number",          "type": "refund"        },        "type": "card"      },      "metadata": {},      "payment_intent": "pi_1GszsK2eZvKYlo2CfhZyoZLp",      "reason": null,      "receipt_number": null,      "source_transfer_reversal": null,      "status": "succeeded",      "transfer_reversal": null    }  ]}
```

---

## Update a webhook endpoint

**URL:** https://docs.stripe.com/api/webhook_endpoints/update

**Contents:**
- Update a webhook endpoint
  - Parameters
    - descriptionstring
    - enabled_eventsarray of enums
    - metadataobject
    - urlstring
  - More parametersExpand all
    - disabledboolean
  - Returns
- Retrieve a webhook endpoint

Updates the webhook endpoint. You may edit the url, the list of enabled_events, and the status of your endpoint.

An optional description of what the webhook is used for.

The list of events to enable for this endpoint. You may specify ['*'] to enable all events, except those that require explicit selection.

Occurs whenever a user authorizes an application. Sent to the related application only.

Occurs whenever a user deauthorizes an application. Sent to the related application only.

Occurs whenever an external account is created.

Occurs whenever an external account is deleted.

Occurs whenever an external account is updated.

Occurs whenever an account status or property has changed.

Occurs whenever an application fee is created on a charge.

Occurs whenever an application fee refund is updated.

Occurs whenever an application fee is refunded, whether from refunding a charge or from refunding the application fee directly. This includes partial refunds.

Occurs whenever your Stripe balance has been updated (e.g., when a charge is available to be paid out). By default, Stripe automatically transfers funds in your balance to your bank account on a daily basis. This event is not fired for negative transactions.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The URL of the webhook endpoint.

The updated webhook endpoint object if successful. Otherwise, this call raises an error.

Retrieves the webhook endpoint with the given ID.

Returns a webhook endpoint if a valid webhook endpoint ID was provided. Raises an error otherwise.

Returns a list of your webhook endpoints.

A dictionary with a data property that contains an array of up to limit webhook endpoints, starting after webhook endpoint starting_after. Each entry in the array is a separate webhook endpoint object. If no more webhook endpoints are available, the resulting array will be empty. This request should never raise an error.

You can also delete webhook endpoints via the webhook endpoint management page of the Stripe dashboard.

An object with the deleted webhook endpoints’s ID. Otherwise, this call raises an error, such as if the webhook endpoint has already been deleted.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/webhook_endpoints/we_1Mr5jULkdIwHu7ix1ibLTM0x \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "enabled_events[]"="charge.succeeded" \  -d "enabled_events[]"="charge.failed" \  --data-urlencode url="https://example.com/new_endpoint"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/webhook_endpoints/we_1Mr5jULkdIwHu7ix1ibLTM0x \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "enabled_events[]"="charge.succeeded" \  -d "enabled_events[]"="charge.failed" \  --data-urlencode url="https://example.com/new_endpoint"
```

Example 3 (unknown):
```unknown
{  "id": "we_1Mr5jULkdIwHu7ix1ibLTM0x",  "object": "webhook_endpoint",  "api_version": null,  "application": null,  "created": 1680122196,  "description": null,  "enabled_events": [    "charge.succeeded",    "charge.failed"  ],  "livemode": false,  "metadata": {},  "status": "disabled",  "url": "https://example.com/new_endpoint"}
```

Example 4 (unknown):
```unknown
{  "id": "we_1Mr5jULkdIwHu7ix1ibLTM0x",  "object": "webhook_endpoint",  "api_version": null,  "application": null,  "created": 1680122196,  "description": null,  "enabled_events": [    "charge.succeeded",    "charge.failed"  ],  "livemode": false,  "metadata": {},  "status": "disabled",  "url": "https://example.com/new_endpoint"}
```

---

## Retrieve a ConfirmationToken

**URL:** https://docs.stripe.com/api/confirmation_tokens/retrieve

**Contents:**
- Retrieve a ConfirmationToken
  - Parameters
  - Returns
- Create a test Confirmation Token Test helper
  - Parameters
    - payment_methodstring
    - payment_method_dataobject
    - payment_method_optionsobject
    - return_urlstring
    - setup_future_usageenum

Retrieves an existing ConfirmationToken object

Returns the specified ConfirmationToken

Creates a test mode Confirmation Token server side for your integration tests.

ID of an existing PaymentMethod.

If provided, this hash will be used to create a PaymentMethod.

Payment-method-specific configuration for this ConfirmationToken.

Return URL used to confirm the Intent.

Indicates that you intend to make future payments with this ConfirmationToken’s payment method.

The presence of this property will attach the payment method to the PaymentIntent’s Customer, if present, after the PaymentIntent is confirmed and any required actions from the user are complete.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

Shipping information for this ConfirmationToken.

Returns a testmode Confirmation Token

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/confirmation_tokens/ctoken_1NnQUf2eZvKYlo2CIObdtbnb \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/confirmation_tokens/ctoken_1NnQUf2eZvKYlo2CIObdtbnb \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "ctoken_1NnQUf2eZvKYlo2CIObdtbnb",  "object": "confirmation_token",  "created": 1694025025,  "expires_at": 1694068225,  "livemode": true,  "mandate_data": null,  "payment_intent": null,  "payment_method": null,  "payment_method_preview": {    "billing_details": {      "address": {        "city": "Hyde Park",        "country": "US",        "line1": "50 Sprague St",        "line2": "",        "postal_code": "02136",        "state": "MA"      },      "email": "jennyrosen@stripe.com",      "name": "Jenny Rosen",      "phone": null    },    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": null      },      "country": "US",      "display_brand": "visa",      "exp_month": 8,      "exp_year": 2026,      "funding": "credit",      "generated_from": null,      "last4": "4242",      "networks": {        "available": [          "visa"        ],        "preferred": null      },      "three_d_secure_usage": {        "supported": true      },      "wallet": null    },    "type": "card"  },  "return_url": "https://example.com/return",  "setup_future_usage": "off_session",  "setup_intent": null,  "shipping": {    "address": {      "city": "Hyde Park",      "country": "US",      "line1": "50 Sprague St",      "line2": "",      "postal_code": "02136",      "state": "MA"    },    "name": "Jenny Rosen",    "phone": null  }}
```

Example 4 (unknown):
```unknown
{  "id": "ctoken_1NnQUf2eZvKYlo2CIObdtbnb",  "object": "confirmation_token",  "created": 1694025025,  "expires_at": 1694068225,  "livemode": true,  "mandate_data": null,  "payment_intent": null,  "payment_method": null,  "payment_method_preview": {    "billing_details": {      "address": {        "city": "Hyde Park",        "country": "US",        "line1": "50 Sprague St",        "line2": "",        "postal_code": "02136",        "state": "MA"      },      "email": "jennyrosen@stripe.com",      "name": "Jenny Rosen",      "phone": null    },    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": null      },      "country": "US",      "display_brand": "visa",      "exp_month": 8,      "exp_year": 2026,      "funding": "credit",      "generated_from": null,      "last4": "4242",      "networks": {        "available": [          "visa"        ],        "preferred": null      },      "three_d_secure_usage": {        "supported": true      },      "wallet": null    },    "type": "card"  },  "return_url": "https://example.com/return",  "setup_future_usage": "off_session",  "setup_intent": null,  "shipping": {    "address": {      "city": "Hyde Park",      "country": "US",      "line1": "50 Sprague St",      "line2": "",      "postal_code": "02136",      "state": "MA"    },    "name": "Jenny Rosen",    "phone": null  }}
```

---

## Disputes

**URL:** https://docs.stripe.com/api/disputes

**Contents:**
- Disputes
- The Dispute object
  - Attributes
    - idstring
    - amountinteger
    - chargestringExpandable
    - currencyenum
    - evidenceobject
    - metadataobject
    - payment_intentnullable stringExpandable

A dispute occurs when a customer questions your charge with their card issuer. When this happens, you have the opportunity to respond to the dispute with evidence that shows that the charge is legitimate.

Related guide: Disputes and fraud

Unique identifier for the object.

Disputed amount. Usually the amount of the charge, but it can differ (usually because of currency fluctuation or because only part of the order is disputed).

ID of the charge that’s disputed.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

Evidence provided to respond to a dispute. Updating any field in the hash submits all fields in the hash for review.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

ID of the PaymentIntent that’s disputed.

Reason given by cardholder for dispute. Possible values are bank_cannot_process, check_returned, credit_not_processed, customer_initiated, debit_not_authorized, duplicate, fraudulent, general, incorrect_account_details, insufficient_funds, noncompliant, product_not_received, product_unacceptable, subscription_canceled, or unrecognized. Learn more about dispute reasons.

The current status of a dispute. Possible values include:warning_needs_response, warning_under_review, warning_closed, needs_response, under_review, won, lost, or prevented.

A dispute resolved in the customer’s favor.

A dispute that requires a response.

A dispute that was prevented from becoming a formal chargeback.

A dispute under review after evidence submission.

An inquiry closed without becoming a formal dispute.

An inquiry that requires a response.

An inquiry under review after evidence submission.

A dispute resolved in the merchant’s favor.

When you get a dispute, contacting your customer is always the best first step. If that doesn’t work, you can submit evidence to help us resolve the dispute in your favor. You can do this in your dashboard, but if you prefer, you can use the API to submit evidence programmatically.

Depending on your dispute type, different evidence fields will give you a better chance of winning your dispute. To figure out which evidence fields to provide, see our guide to dispute types.

Evidence to upload, to respond to a dispute. Updating any field in the hash will submit all fields in the hash for review. The combined character count of all fields is limited to 150,000.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Whether to immediately submit evidence to the bank. If false, evidence is staged on the dispute. Staged evidence is visible in the API and Dashboard, and can be submitted to the bank by making another request with this attribute set to true (the default).

Returns the dispute object.

Retrieves the dispute with the given ID.

Returns a dispute if a valid dispute ID was provided. Raises an error otherwise.

Returns a list of your disputes.

Only return disputes associated to the charge specified by this charge ID.

Only return disputes associated to the PaymentIntent specified by this PaymentIntent ID.

A dictionary with a data property that contains an array of up to limit disputes, starting after dispute starting_after. Each entry in the array is a separate dispute object. If no more disputes are available, the resulting array will be empty.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "du_1MtJUT2eZvKYlo2CNaw2HvEv",  "object": "dispute",  "amount": 1000,  "balance_transactions": [],  "charge": "ch_1AZtxr2eZvKYlo2CJDX8whov",  "created": 1680651737,  "currency": "usd",  "evidence": {    "access_activity_log": null,    "billing_address": null,    "cancellation_policy": null,    "cancellation_policy_disclosure": null,    "cancellation_rebuttal": null,    "customer_communication": null,    "customer_email_address": null,    "customer_name": null,    "customer_purchase_ip": null,    "customer_signature": null,    "duplicate_charge_documentation": null,    "duplicate_charge_explanation": null,    "duplicate_charge_id": null,    "product_description": null,    "receipt": null,    "refund_policy": null,    "refund_policy_disclosure": null,    "refund_refusal_explanation": null,    "service_date": null,    "service_documentation": null,    "shipping_address": null,    "shipping_carrier": null,    "shipping_date": null,    "shipping_documentation": null,    "shipping_tracking_number": null,    "uncategorized_file": null,    "uncategorized_text": null  },  "evidence_details": {    "due_by": 1682294399,    "has_evidence": false,    "past_due": false,    "submission_count": 0  },  "is_charge_refundable": true,  "livemode": false,  "metadata": {},  "payment_intent": null,  "reason": "general",  "status": "warning_needs_response"}
```

Example 2 (unknown):
```unknown
{  "id": "du_1MtJUT2eZvKYlo2CNaw2HvEv",  "object": "dispute",  "amount": 1000,  "balance_transactions": [],  "charge": "ch_1AZtxr2eZvKYlo2CJDX8whov",  "created": 1680651737,  "currency": "usd",  "evidence": {    "access_activity_log": null,    "billing_address": null,    "cancellation_policy": null,    "cancellation_policy_disclosure": null,    "cancellation_rebuttal": null,    "customer_communication": null,    "customer_email_address": null,    "customer_name": null,    "customer_purchase_ip": null,    "customer_signature": null,    "duplicate_charge_documentation": null,    "duplicate_charge_explanation": null,    "duplicate_charge_id": null,    "product_description": null,    "receipt": null,    "refund_policy": null,    "refund_policy_disclosure": null,    "refund_refusal_explanation": null,    "service_date": null,    "service_documentation": null,    "shipping_address": null,    "shipping_carrier": null,    "shipping_date": null,    "shipping_documentation": null,    "shipping_tracking_number": null,    "uncategorized_file": null,    "uncategorized_text": null  },  "evidence_details": {    "due_by": 1682294399,    "has_evidence": false,    "past_due": false,    "submission_count": 0  },  "is_charge_refundable": true,  "livemode": false,  "metadata": {},  "payment_intent": null,  "reason": "general",  "status": "warning_needs_response"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/disputes/du_1MtJUT2eZvKYlo2CNaw2HvEv \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/disputes/du_1MtJUT2eZvKYlo2CNaw2HvEv \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

---

## Create a test Confirmation Token Test helper

**URL:** https://docs.stripe.com/api/confirmation_tokens/test_create

**Contents:**
- Create a test Confirmation Token Test helper
  - Parameters
    - payment_methodstring
    - payment_method_dataobject
    - payment_method_optionsobject
    - return_urlstring
    - setup_future_usageenum
    - shippingobject
  - Returns

Creates a test mode Confirmation Token server side for your integration tests.

ID of an existing PaymentMethod.

If provided, this hash will be used to create a PaymentMethod.

Payment-method-specific configuration for this ConfirmationToken.

Return URL used to confirm the Intent.

Indicates that you intend to make future payments with this ConfirmationToken’s payment method.

The presence of this property will attach the payment method to the PaymentIntent’s Customer, if present, after the PaymentIntent is confirmed and any required actions from the user are complete.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

Shipping information for this ConfirmationToken.

Returns a testmode Confirmation Token

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/test_helpers/confirmation_tokens \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d payment_method=pm_card_visa
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/test_helpers/confirmation_tokens \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d payment_method=pm_card_visa
```

Example 3 (unknown):
```unknown
{  "id": "ctoken_1Ow71CL4FhS6zgoxWjxc7sfr",  "object": "confirmation_token",  "created": 1710871450,  "expires_at": 1710914650,  "livemode": false,  "payment_intent": null,  "payment_method_preview": {    "billing_details": {      "address": {        "city": null,        "country": null,        "line1": null,        "line2": null,        "postal_code": null,        "state": null      },      "email": null,      "name": null,      "phone": null    },    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": "unchecked"      },      "country": "US",      "display_brand": "visa",      "exp_month": 3,      "exp_year": 2025,      "fingerprint": "jbGyCKrSRsFpOBWP",      "funding": "credit",      "generated_from": null,      "last4": "4242",      "networks": {        "available": [          "visa"        ],        "preferred": null      },      "three_d_secure_usage": {        "supported": true      },      "wallet": null    },    "type": "card"  },  "return_url": null,  "setup_future_usage": null,  "setup_intent": null,  "shipping": null,  "use_stripe_sdk": true}
```

Example 4 (unknown):
```unknown
{  "id": "ctoken_1Ow71CL4FhS6zgoxWjxc7sfr",  "object": "confirmation_token",  "created": 1710871450,  "expires_at": 1710914650,  "livemode": false,  "payment_intent": null,  "payment_method_preview": {    "billing_details": {      "address": {        "city": null,        "country": null,        "line1": null,        "line2": null,        "postal_code": null,        "state": null      },      "email": null,      "name": null,      "phone": null    },    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": "unchecked"      },      "country": "US",      "display_brand": "visa",      "exp_month": 3,      "exp_year": 2025,      "fingerprint": "jbGyCKrSRsFpOBWP",      "funding": "credit",      "generated_from": null,      "last4": "4242",      "networks": {        "available": [          "visa"        ],        "preferred": null      },      "three_d_secure_usage": {        "supported": true      },      "wallet": null    },    "type": "card"  },  "return_url": null,  "setup_future_usage": null,  "setup_intent": null,  "shipping": null,  "use_stripe_sdk": true}
```

---

## Files

**URL:** https://docs.stripe.com/api/files

**Contents:**
- Files
- The File object
  - Attributes
    - idstring
    - purposeenum
    - typenullable string
  - More attributesExpand all
    - objectstring
    - createdtimestamp
    - expires_atnullable timestamp

This object represents files hosted on Stripe’s servers. You can upload files with the create file request (for example, when uploading dispute evidence). Stripe also creates files independently (for example, the results of a Sigma scheduled query).

Related guide: File upload guide

Unique identifier for the object.

The purpose of the uploaded file.

Additional documentation requirements that can be requested for an account.

Additional verification for custom accounts.

Customer signature image.

Evidence to submit with a dispute response.

User-accessible copies of query results from the Reporting dataset.

Financial account statements.

A document to verify the identity of an account owner during account provisioning.

Image of a document collected by Stripe Identity.

The returned file type (for example, csv, pdf, jpg, or png).

To upload a file to Stripe, you need to send a request of type multipart/form-data. Include the file you want to upload in the request, and the parameters for creating a file.

All of Stripe’s officially supported Client libraries support sending multipart/form-data.

A file to upload. Make sure that the specifications follow RFC 2388, which defines file transfers for the multipart/form-data protocol.

The purpose of the uploaded file.

Additional documentation requirements that can be requested for an account.

Additional verification for custom accounts.

Customer signature image.

Evidence to submit with a dispute response.

A document to verify the identity of an account owner during account provisioning.

Additional regulatory reporting requirements for Issuing.

A self-assessment PCI questionnaire.

A copy of the platform’s Terms of Service.

Returns the file object.

Retrieves the details of an existing file object. After you supply a unique file ID, Stripe returns the corresponding file object. Learn how to access file contents.

If the identifier you provide is valid, a file object returns. If not, Stripe raises an error.

Returns a list of the files that your account has access to. Stripe sorts and returns the files by their creation dates, placing the most recently created files at the top.

Filter queries by the file purpose. If you don’t provide a purpose, the queries return unfiltered files.

A dictionary with a data property that contains an array of up to limit files, starting after the starting_after file. Each entry in the array is a separate file object. If there aren’t additional available files, the resulting array is empty.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "file_1Mr4LDLkdIwHu7ixFCz0dZiH",  "object": "file",  "created": 1680116847,  "expires_at": 1703444847,  "filename": "file.png",  "links": {    "object": "list",    "data": [],    "has_more": false,    "url": "/v1/file_links?file=file_1Mr4LDLkdIwHu7ixFCz0dZiH"  },  "purpose": "dispute_evidence",  "size": 8429,  "title": null,  "type": "png",  "url": "https://files.stripe.com/v1/files/file_1Mr4LDLkdIwHu7ixFCz0dZiH/contents"}
```

Example 2 (unknown):
```unknown
{  "id": "file_1Mr4LDLkdIwHu7ixFCz0dZiH",  "object": "file",  "created": 1680116847,  "expires_at": 1703444847,  "filename": "file.png",  "links": {    "object": "list",    "data": [],    "has_more": false,    "url": "/v1/file_links?file=file_1Mr4LDLkdIwHu7ixFCz0dZiH"  },  "purpose": "dispute_evidence",  "size": 8429,  "title": null,  "type": "png",  "url": "https://files.stripe.com/v1/files/file_1Mr4LDLkdIwHu7ixFCz0dZiH/contents"}
```

Example 3 (unknown):
```unknown
curl https://files.stripe.com/v1/files \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -F purpose=dispute_evidence \  -F file="@/path/to/a/file.jpg"
```

Example 4 (unknown):
```unknown
curl https://files.stripe.com/v1/files \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -F purpose=dispute_evidence \  -F file="@/path/to/a/file.jpg"
```

---

## Invoice Line Item

**URL:** https://docs.stripe.com/api/invoice-line-item

**Contents:**
- Invoice Line Item
- The Invoice Line Item object
  - Attributes
    - idstring
    - amountinteger
    - currencyenum
    - descriptionnullable string
    - invoicenullable string
    - metadataobject
    - parentnullable object

Invoice Line Items represent the individual lines within an invoice and only exist within the context of an invoice.

Each line item is backed by either an invoice item or a subscription item.

Unique identifier for the object.

The amount, in cents.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

An arbitrary string attached to the object. Often useful for displaying to users.

The ID of the invoice that contains this line item.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Note that for line items with type=subscription, metadata reflects the current metadata from the subscription associated with the line item, unless the invoice line was directly updated with different metadata after creation.

The parent that generated this line item.

The period this line_item covers. For subscription line items, this is the subscription period. For prorations, this starts when the proration was calculated, and ends at the period end of the subscription. For invoice items, this is the time at which the invoice item was created or the period of the item. If you have Stripe Revenue Recognition enabled, the period will be used to recognize and defer revenue. See the Revenue Recognition documentation for details.

The pricing information of the line item.

The quantity of the subscription, if the line item is a subscription or a proration.

Updates an invoice’s line item. Some fields, such as tax_amounts, only live on the invoice line item, so they can only be updated through this endpoint. Other fields, such as amount, live on both the invoice item and the invoice line item, so updates on this endpoint will propagate to the invoice item as well. Updating an invoice’s line item is only possible before the invoice is finalized.

Invoice ID of line item

The integer amount in cents of the charge to be applied to the upcoming invoice. If you want to apply a credit to the customer’s account, pass a negative amount.

An arbitrary string which you can attach to the invoice item. The description is displayed in the invoice for easy tracking.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata. For type=subscription line items, the incoming metadata specified on the request is directly used to set this value, in contrast to type=invoiceitem line items, where any existing metadata on the invoice line is merged with the incoming data.

The period associated with this invoice item. When set to different values, the period will be rendered on the invoice. If you have Stripe Revenue Recognition enabled, the period will be used to recognize and defer revenue. See the Revenue Recognition documentation for details.

The pricing information for the invoice item.

Non-negative integer. The quantity of units for the line item.

The updated invoice’s line item object is returned upon success. Otherwise, this call raises an error.

When retrieving an invoice, you’ll get a lines property containing the total count of line items and the first handful of those items. There is also a URL where you can retrieve the full (paginated) list of line items.

Returns a list of line_item objects.

Adds multiple line items to an invoice. This is only possible when an invoice is still a draft.

The line items to add.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The updated invoice with newly added line items is returned upon success. Otherwise, this call raises an error.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "il_tmp_1Nzo1ZGgdF1VjufLzD1UUn9R",  "object": "line_item",  "amount": 1000,  "currency": "usd",  "description": "My First Invoice Item (created for API docs)",  "discount_amounts": [],  "discountable": true,  "discounts": [],  "livemode": false,  "metadata": {},  "parent": {    "type": "invoice_item_details",    "invoice_item_details": {      "invoice_item": "ii_1NpHiK2eZvKYlo2C9NdV8VrI",      "proration": false,      "proration_details": {        "credited_items": null      },      "subscription": null    }  },  "period": {    "end": 1696975413,    "start": 1696975413  },  "pricing": {    "price_details": {      "price": "price_1NzlYfGgdF1VjufL0cVjLJVI",      "product": "prod_OnMHDH6VBmYlTr"    },    "type": "price_details",    "unit_amount_decimal": "1000"  },  "quantity": 1,  "taxes": []}
```

Example 2 (unknown):
```unknown
{  "id": "il_tmp_1Nzo1ZGgdF1VjufLzD1UUn9R",  "object": "line_item",  "amount": 1000,  "currency": "usd",  "description": "My First Invoice Item (created for API docs)",  "discount_amounts": [],  "discountable": true,  "discounts": [],  "livemode": false,  "metadata": {},  "parent": {    "type": "invoice_item_details",    "invoice_item_details": {      "invoice_item": "ii_1NpHiK2eZvKYlo2C9NdV8VrI",      "proration": false,      "proration_details": {        "credited_items": null      },      "subscription": null    }  },  "period": {    "end": 1696975413,    "start": 1696975413  },  "pricing": {    "price_details": {      "price": "price_1NzlYfGgdF1VjufL0cVjLJVI",      "product": "prod_OnMHDH6VBmYlTr"    },    "type": "price_details",    "unit_amount_decimal": "1000"  },  "quantity": 1,  "taxes": []}
```

Example 3 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/invoices/in_1NuhUa2eZvKYlo2CWYVhyvD9/lines/il_tmp_1Nzo1ZGgdF1VjufLzD1UUn9R \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/invoices/in_1NuhUa2eZvKYlo2CWYVhyvD9/lines/il_tmp_1Nzo1ZGgdF1VjufLzD1UUn9R \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

---

## The Payout object

**URL:** https://docs.stripe.com/api/payouts/object

**Contents:**
- The Payout object
  - Attributes
    - idstring
    - amountinteger
    - arrival_datetimestamp
    - currencyenum
    - descriptionnullable string
    - metadatanullable object
    - statement_descriptornullable string
    - statusstring

Unique identifier for the object.

The amount (in cents) that transfers to your bank account or debit card.

Date that you can expect the payout to arrive in the bank. This factors in delays to account for weekends or bank holidays.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Extra information about a payout that displays on the user’s bank statement.

Current status of the payout: paid, pending, in_transit, canceled or failed. A payout is pending until it’s submitted to the bank, when it becomes in_transit. The status changes to paid if the transaction succeeds, or to failed or canceled (within 5 business days). Some payouts that fail might initially show as paid, then change to failed.

To send funds to your own bank account, create a new payout object. Your Stripe balance must cover the payout amount. If it doesn’t, you receive an “Insufficient Funds” error.

If your API key is in test mode, money won’t actually be sent, though every other action occurs as if you’re in live mode.

If you create a manual payout on a Stripe account that uses multiple payment source types, you need to specify the source type balance that the payout draws from. The balance object details available and pending amounts by source type.

A positive integer in cents representing how much to payout.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

A string that displays on the recipient’s bank or card statement (up to 22 characters). A statement_descriptor that’s longer than 22 characters return an error. Most banks truncate this information and display it inconsistently. Some banks might not display it at all.

Returns a payout object if no initial errors are present during the payout creation (invalid routing number, insufficient funds, and so on). We initially mark the status of the payout object as pending.

Updates the specified payout by setting the values of the parameters you pass. We don’t change parameters that you don’t provide. This request only accepts the metadata as arguments.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the payout object if the update succeeds. This call raises an error if update parameters are invalid.

Retrieves the details of an existing payout. Supply the unique payout ID from either a payout creation request or the payout list. Stripe returns the corresponding payout information.

Returns a payout object if a you provide a valid identifier. raises An error occurs otherwise.

Returns a list of existing payouts sent to third-party bank accounts or payouts that Stripe sent to you. The payouts return in sorted order, with the most recently created payouts appearing first.

Only return payouts that have the given status: pending, paid, failed, or canceled.

A dictionary with a data property that contains an array of up to limit payouts, starting after payout starting_after. Each entry in the array is a separate payout object. If no other payouts are available, the resulting array is empty.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "po_1OaFDbEcg9tTZuTgNYmX0PKB",  "object": "payout",  "amount": 1100,  "arrival_date": 1680652800,  "automatic": false,  "balance_transaction": "txn_1OaFDcEcg9tTZuTgYMR25tSe",  "created": 1680648691,  "currency": "usd",  "description": null,  "destination": "ba_1MtIhL2eZvKYlo2CAElKwKu2",  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "livemode": false,  "metadata": {},  "method": "standard",  "original_payout": null,  "reconciliation_status": "not_applicable",  "reversed_by": null,  "source_type": "card",  "statement_descriptor": null,  "status": "pending",  "type": "bank_account"}
```

Example 2 (unknown):
```unknown
{  "id": "po_1OaFDbEcg9tTZuTgNYmX0PKB",  "object": "payout",  "amount": 1100,  "arrival_date": 1680652800,  "automatic": false,  "balance_transaction": "txn_1OaFDcEcg9tTZuTgYMR25tSe",  "created": 1680648691,  "currency": "usd",  "description": null,  "destination": "ba_1MtIhL2eZvKYlo2CAElKwKu2",  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "livemode": false,  "metadata": {},  "method": "standard",  "original_payout": null,  "reconciliation_status": "not_applicable",  "reversed_by": null,  "source_type": "card",  "statement_descriptor": null,  "status": "pending",  "type": "bank_account"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/payouts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=1100 \  -d currency=usd
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/payouts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=1100 \  -d currency=usd
```

---

## Retrieve an event destination v2

**URL:** https://docs.stripe.com/api/v2/core/event_destinations/retrieve

**Contents:**
- Retrieve an event destination v2
  - Parameters
    - idstringRequired
    - includearray of enums
  - Returns
  - Response attributes
    - idstring
    - objectstring, value is "v2.core.event_destination"
    - amazon_eventbridgenullable object
    - createdtimestamp

Retrieves the details of an event destination.

Identifier for the event destination to retrieve.

Additional fields to include in the response.

Include parameter to expose webhook_endpoint.url.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value of the object field.

Amazon EventBridge configuration.

Time at which the object was created.

An optional description of what the event destination is used for.

The list of events to enable for this endpoint.

Payload type of events being subscribed to.

Where events should be routed from.

Receive events from accounts connected to the account that owns the event destination.

Receive events from the account that owns the event destination.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Event destination name.

If using the snapshot event payload, the API version events are rendered as.

Status. It can be set to either enabled or disabled.

Event destination is disabled.

Event destination is enabled.

Additional information about event destination status.

Event destination type.

Time at which the object was last updated.

Webhook endpoint configuration.

The resource wasn’t found.

Lists all event destinations.

Additional fields to include in the response. Currently supports webhook_endpoint.url.

Include parameter to expose webhook_endpoint.url.

List of event destinations.

The previous page url.

Delete an event destination.

Identifier for the event destination to delete.

Identifier for the deleted event destination.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

Disable an event destination.

Identifier for the event destination to disable.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value of the object field.

Amazon EventBridge configuration.

Time at which the object was created.

An optional description of what the event destination is used for.

The list of events to enable for this endpoint.

Payload type of events being subscribed to.

Where events should be routed from.

Receive events from accounts connected to the account that owns the event destination.

Receive events from the account that owns the event destination.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Event destination name.

If using the snapshot event payload, the API version events are rendered as.

Status. It can be set to either enabled or disabled.

Event destination is disabled.

Event destination is enabled.

Additional information about event destination status.

Event destination type.

Time at which the object was last updated.

Webhook endpoint configuration.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

Enable an event destination.

Identifier for the event destination to enable.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value of the object field.

Amazon EventBridge configuration.

Time at which the object was created.

An optional description of what the event destination is used for.

The list of events to enable for this endpoint.

Payload type of events being subscribed to.

Where events should be routed from.

Receive events from accounts connected to the account that owns the event destination.

Receive events from the account that owns the event destination.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Event destination name.

If using the snapshot event payload, the API version events are rendered as.

Status. It can be set to either enabled or disabled.

Event destination is disabled.

Event destination is enabled.

Additional information about event destination status.

Event destination type.

Time at which the object was last updated.

Webhook endpoint configuration.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v2/core/event_destinations/ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6 \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  -d "include[0]"="webhook_endpoint.url"
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v2/core/event_destinations/ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6 \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  -d "include[0]"="webhook_endpoint.url"
```

Example 3 (unknown):
```unknown
{  "id": "ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6",  "object": "v2.core.event_destination",  "created": "2024-10-22T16:20:09.931Z",  "description": "This is my event destination, I like it a lot",  "enabled_events": [    "v1.billing.meter.error_report_triggered"  ],  "event_payload": "thin",  "events_from": [    "self"  ],  "livemode": false,  "metadata": {},  "name": "My Event Destination",  "snapshot_api_version": null,  "status": "disabled",  "status_details": {    "disabled": {      "reason": "user"    }  },  "type": "webhook_endpoint",  "updated": "2024-10-22T16:22:02.524Z",  "webhook_endpoint": {    "signing_secret": null,    "url": null  }}
```

Example 4 (unknown):
```unknown
{  "id": "ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6",  "object": "v2.core.event_destination",  "created": "2024-10-22T16:20:09.931Z",  "description": "This is my event destination, I like it a lot",  "enabled_events": [    "v1.billing.meter.error_report_triggered"  ],  "event_payload": "thin",  "events_from": [    "self"  ],  "livemode": false,  "metadata": {},  "name": "My Event Destination",  "snapshot_api_version": null,  "status": "disabled",  "status_details": {    "disabled": {      "reason": "user"    }  },  "type": "webhook_endpoint",  "updated": "2024-10-22T16:22:02.524Z",  "webhook_endpoint": {    "signing_secret": null,    "url": null  }}
```

---

## Application Fees

**URL:** https://docs.stripe.com/api/application_fees

**Contents:**
- Application Fees
- The Application Fee object
  - Attributes
    - idstring
    - accountstringExpandable
    - amountinteger
    - amount_refundedinteger
    - chargestringExpandable
    - currencyenum
    - refundedboolean

When you collect a transaction fee on top of a charge made for your user (using Connect), an Application Fee object is created in your account. You can list, retrieve, and refund application fees.

Related guide: Collecting application fees

Unique identifier for the object.

ID of the Stripe account this fee was taken from.

Amount earned, in cents.

Amount in cents refunded (can be less than the amount attribute on the fee if a partial refund was issued)

ID of the charge that the application fee was taken from.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

Whether the fee has been fully refunded. If the fee is only partially refunded, this attribute will still be false.

Retrieves the details of an application fee that your account has collected. The same information is returned when refunding the application fee.

Returns an application fee object if a valid identifier was provided, and raises an error otherwise.

Returns a list of application fees you’ve previously collected. The application fees are returned in sorted order, with the most recent fees appearing first.

Only return application fees for the charge specified by this charge ID.

A dictionary with a data property that contains an array of up to limit application fees, starting after application fee starting_after. Each entry in the array is a separate application fee object. If no more fees are available, the resulting array will be empty.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "fee_1B73DOKbnvuxQXGuhY8Aw0TN",  "object": "application_fee",  "account": "acct_164wxjKbnvuxQXGu",  "amount": 105,  "amount_refunded": 105,  "application": "ca_32D88BD1qLklliziD7gYQvctJIhWBSQ7",  "balance_transaction": "txn_1032HU2eZvKYlo2CEPtcnUvl",  "charge": "ch_1B73DOKbnvuxQXGurbwPqzsu",  "created": 1506609734,  "currency": "gbp",  "livemode": false,  "originating_transaction": null,  "refunded": true,  "refunds": {    "object": "list",    "data": [      {        "id": "fr_1MBoU0KbnvuxQXGu2wCCz4Bb",        "object": "fee_refund",        "amount": 38,        "balance_transaction": null,        "created": 1670284441,        "currency": "usd",        "fee": "fee_1B73DOKbnvuxQXGuhY8Aw0TN",        "metadata": {}      },      {        "id": "fr_D0s7fGBKB40Twy",        "object": "fee_refund",        "amount": 100,        "balance_transaction": "txn_1CaqNg2eZvKYlo2C75cA3Euk",        "created": 1528486576,        "currency": "usd",        "fee": "fee_1B73DOKbnvuxQXGuhY8Aw0TN",        "metadata": {}      }    ],    "has_more": false,    "url": "/v1/application_fees/fee_1B73DOKbnvuxQXGuhY8Aw0TN/refunds"  },  "fee_source": {    "charge": "ch_1B73DOKbnvuxQXGurbwPqzsu",    "type": "charge"  }}
```

Example 2 (unknown):
```unknown
{  "id": "fee_1B73DOKbnvuxQXGuhY8Aw0TN",  "object": "application_fee",  "account": "acct_164wxjKbnvuxQXGu",  "amount": 105,  "amount_refunded": 105,  "application": "ca_32D88BD1qLklliziD7gYQvctJIhWBSQ7",  "balance_transaction": "txn_1032HU2eZvKYlo2CEPtcnUvl",  "charge": "ch_1B73DOKbnvuxQXGurbwPqzsu",  "created": 1506609734,  "currency": "gbp",  "livemode": false,  "originating_transaction": null,  "refunded": true,  "refunds": {    "object": "list",    "data": [      {        "id": "fr_1MBoU0KbnvuxQXGu2wCCz4Bb",        "object": "fee_refund",        "amount": 38,        "balance_transaction": null,        "created": 1670284441,        "currency": "usd",        "fee": "fee_1B73DOKbnvuxQXGuhY8Aw0TN",        "metadata": {}      },      {        "id": "fr_D0s7fGBKB40Twy",        "object": "fee_refund",        "amount": 100,        "balance_transaction": "txn_1CaqNg2eZvKYlo2C75cA3Euk",        "created": 1528486576,        "currency": "usd",        "fee": "fee_1B73DOKbnvuxQXGuhY8Aw0TN",        "metadata": {}      }    ],    "has_more": false,    "url": "/v1/application_fees/fee_1B73DOKbnvuxQXGuhY8Aw0TN/refunds"  },  "fee_source": {    "charge": "ch_1B73DOKbnvuxQXGurbwPqzsu",    "type": "charge"  }}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/application_fees/fee_1B73DOKbnvuxQXGuhY8Aw0TN \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/application_fees/fee_1B73DOKbnvuxQXGuhY8Aw0TN \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

---

## Update a refund

**URL:** https://docs.stripe.com/api/refunds/update

**Contents:**
- Update a refund
  - Parameters
    - metadataobject
  - Returns
- Retrieve a refund
  - Parameters
  - Returns
- List all refunds
  - Parameters
    - chargestring

Updates the refund that you specify by setting the values of the passed parameters. Any parameters that you don’t provide remain unchanged.

This request only accepts metadata as an argument.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the refund object if the update succeeds. This call raises an error if update parameters are invalid.

Retrieves the details of an existing refund.

Returns a refund if you provide a valid ID. Raises an error otherwise.

Returns a list of all refunds you created. We return the refunds in sorted order, with the most recent refunds appearing first. The 10 most recent refunds are always available by default on the Charge object.

Only return refunds for the charge specified by this charge ID.

Only return refunds for the PaymentIntent specified by this ID.

A dictionary with a data property that contains an array of up to limit refunds, starting after the starting_after refund. Each entry in the array is a separate Refund object. If no other refunds are available, the resulting array is empty. If you provide a non-existent charge ID, this call raises an error.

Cancels a refund with a status of requires_action.

You can’t cancel refunds in other states. Only refunds for payment methods that require customer action can enter the requires_action state.

Returns the refund object if the cancellation succeeds. This call raises an error if you can’t cancel the refund.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/refunds/re_1Nispe2eZvKYlo2Cd31jOCgZ \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/refunds/re_1Nispe2eZvKYlo2Cd31jOCgZ \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

Example 3 (unknown):
```unknown
{  "id": "re_1Nispe2eZvKYlo2Cd31jOCgZ",  "object": "refund",  "amount": 1000,  "balance_transaction": "txn_1Nispe2eZvKYlo2CYezqFhEx",  "charge": "ch_1NirD82eZvKYlo2CIvbtLWuY",  "created": 1692942318,  "currency": "usd",  "destination_details": {    "card": {      "reference": "123456789012",      "reference_status": "available",      "reference_type": "acquirer_reference_number",      "type": "refund"    },    "type": "card"  },  "metadata": {    "order_id": "6735"  },  "payment_intent": "pi_1GszsK2eZvKYlo2CfhZyoZLp",  "reason": null,  "receipt_number": null,  "source_transfer_reversal": null,  "status": "succeeded",  "transfer_reversal": null}
```

Example 4 (unknown):
```unknown
{  "id": "re_1Nispe2eZvKYlo2Cd31jOCgZ",  "object": "refund",  "amount": 1000,  "balance_transaction": "txn_1Nispe2eZvKYlo2CYezqFhEx",  "charge": "ch_1NirD82eZvKYlo2CIvbtLWuY",  "created": 1692942318,  "currency": "usd",  "destination_details": {    "card": {      "reference": "123456789012",      "reference_status": "available",      "reference_type": "acquirer_reference_number",      "type": "refund"    },    "type": "card"  },  "metadata": {    "order_id": "6735"  },  "payment_intent": "pi_1GszsK2eZvKYlo2CfhZyoZLp",  "reason": null,  "receipt_number": null,  "source_transfer_reversal": null,  "status": "succeeded",  "transfer_reversal": null}
```

---

## Include-dependent response values (API v2)

**URL:** https://docs.stripe.com/api/include_dependent_response_values

**Contents:**
- Include-dependent response values (API v2)
- Metadata
- Sample metadata use cases
- Pagination
  - Parameters
    - limitoptional, default is 10
    - starting_afteroptional object ID
    - ending_beforeoptional object ID
  - List Response Format
    - objectstring, value is "list"

Some API v2 responses contain null values for certain properties by default, regardless of their actual values. That reduces the size of response payloads while maintaining the basic response structure. To retrieve the actual values for those properties, specify them in the include array request parameter.

To determine whether you need to use the include parameter in a given request, look at the request description. The include parameter’s enum values represent the response properties that depend on the include parameter.

Whether a response property defaults to null depends on the request endpoint, not the object that the endpoint references. If multiple endpoints return data from the same object, a particular property can depend on include in one endpoint and return its actual value by default for a different endpoint.

A hash property can depend on a single include value, or on multiple include values associated with its child properties. For example, when updating an Account, to return actual values for the entire identity hash, specify identity in the include parameter. Otherwise, the identity hash is null in the response. However, to return actual values for the configuration hash, you must specify individual configurations in the request. If you specify at least one configuration, but not all of them, specified configurations return actual values and unspecified configurations return null. If you don’t specify any configurations, the configuration hash is null in the response.

The response includes actual values for the properties specified in the include parameter, and null for all other include-dependent properties.

Updateable Stripe objects—including Account, Charge, Customer, PaymentIntent, Refund, Subscription, and Transfer have a metadata parameter. You can use this parameter to attach key-value data to these Stripe objects.

You can specify up to 50 keys, with key names up to 40 characters long and values up to 500 characters long. Keys and values are stored as strings and can contain any characters with one exception: you can’t use square brackets ([ and ]) in keys.

You can use metadata to store additional, structured information on an object. For example, you could store your user’s full name and corresponding unique identifier from your system on a Stripe Customer object. Stripe doesn’t use metadata—for example, we don’t use it to authorize or decline a charge and it won’t be seen by your users unless you choose to show it to them.

Some of the objects listed above also support a description parameter. You can use the description parameter to annotate a charge-for example, a human-readable description such as 2 shirts for test@example.com. Unlike metadata, description is a single string, which your users might see (for example, in email receipts Stripe sends on your behalf).

Don’t store any sensitive information (bank account numbers, card details, and so on) as metadata or in the description parameter.

All top-level API resources have support for bulk fetches through “list” API methods. For example, you can list charges, list customers, and list invoices. These list API methods share a common structure and accept, at a minimum, the following three parameters: limit, starting_after, and ending_before.

Stripe’s list API methods use cursor-based pagination through the starting_after and ending_before parameters. Both parameters accept an existing object ID value (see below) and return objects in reverse chronological order. The ending_before parameter returns objects listed before the named object. The starting_after parameter returns objects listed after the named object. These parameters are mutually exclusive. You can use either the starting_after or ending_before parameter, but not both simultaneously.

Our client libraries offer auto-pagination helpers to traverse all pages of a list.

This specifies a limit on the number of objects to return, ranging between 1 and 100.

A cursor to use in pagination. starting_after is an object ID that defines your place in the list. For example, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include starting_after=obj_foo to fetch the next page of the list.

A cursor to use in pagination. ending_before is an object ID that defines your place in the list. For example, if you make a list request and receive 100 objects, starting with obj_bar, your subsequent call can include ending_before=obj_bar to fetch the previous page of the list.

A string that provides a description of the object type that returns.

An array containing the actual response elements, paginated by any request parameters.

Whether or not there are more elements available after this set. If false, this set comprises the end of the list.

The URL for accessing this list.

APIs within the /v2 namespace contain a different pagination interface than the v1 namespace.

Some top-level API resource have support for retrieval via “search” API methods. For example, you can search charges, search customers, and search subscriptions.

Stripe’s search API methods utilize cursor-based pagination via the page request parameter and next_page response parameter. For example, if you make a search request and receive "next_page": "pagination_key" in the response, your subsequent call can include page=pagination_key to fetch the next page of results.

Our client libraries offer auto-pagination helpers to easily traverse all pages of a search result.

The search query string. See search query language.

A limit on the number of objects returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A string describing the object type returned.

The URL for accessing this list.

Whether or not there are more elements available after this set. If false, this set comprises the end of the list.

An array containing the actual response elements, paginated by any request parameters.

A cursor for use in pagination. If has_more is true, you can pass the value of next_page to a subsequent call to fetch the next page of results.

The total number of objects that match the query, only accurate up to 10,000. This field isn’t included by default. To include it in the response, expand the total_count field.

Our libraries support auto-pagination. This feature allows you to easily iterate through large lists of resources without having to manually perform the requests to fetch subsequent pages.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "include": [        "identity",        "configuration.customer"    ]  }'
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "include": [        "identity",        "configuration.customer"    ]  }'
```

Example 3 (unknown):
```unknown
{  "id": "acct_123",  "object": "v2.core.account",  "applied_configurations": [    "customer",    "merchant"  ],  "configuration": {    "customer": {      "automatic_indirect_tax": {        ...      },      "billing": {        ...      },      "capabilities": {        ...      },      ...    },    "merchant": null,    "recipient": null  },  "contact_email": "furever@example.com",  "created": "2025-06-09T21:16:03.000Z",  "dashboard": "full",  "defaults": null,  "display_name": "Furever",  "identity": {    "business_details": {      "doing_business_as": "FurEver",      "id_numbers": [        {          "type": "us_ein"        }      ],      "product_description": "Saas pet grooming platform at furever.dev using Connect embedded components",      "structure": "sole_proprietorship",      "url": "http://accessible.stripe.com"    },    "country": "US"  },  "livemode": true,  "metadata": {},  "requirements": null}
```

Example 4 (unknown):
```unknown
{  "id": "acct_123",  "object": "v2.core.account",  "applied_configurations": [    "customer",    "merchant"  ],  "configuration": {    "customer": {      "automatic_indirect_tax": {        ...      },      "billing": {        ...      },      "capabilities": {        ...      },      ...    },    "merchant": null,    "recipient": null  },  "contact_email": "furever@example.com",  "created": "2025-06-09T21:16:03.000Z",  "dashboard": "full",  "defaults": null,  "display_name": "Furever",  "identity": {    "business_details": {      "doing_business_as": "FurEver",      "id_numbers": [        {          "type": "us_ein"        }      ],      "product_description": "Saas pet grooming platform at furever.dev using Connect embedded components",      "structure": "sole_proprietorship",      "url": "http://accessible.stripe.com"    },    "country": "US"  },  "livemode": true,  "metadata": {},  "requirements": null}
```

---

## API keys

**URL:** https://docs.stripe.com/keys

**Contents:**
- API keys
- Use API keys to authenticate API requests.
- Key types
    - Restricted API keys
  - Example API keys
  - Protect your keys
- Sandbox versus live mode
    - Live mode key access
- Organization API keys
  - Behavior

Stripe authenticates your API requests using your account’s API keys. If a request doesn’t include a valid key, Stripe returns an invalid request error. If a request includes a deleted or expired key, Stripe returns an authentication error.

Use the Developers Dashboard to create, reveal, delete, and rotate API keys. You can access your v1 API keys on the API keys tab.

By default, all accounts have a total of four API keys:

Your secret and publishable keys are on the API keys tab in the Dashboard. If you can’t view your API keys, ask the owner of your Stripe account to add you to their team with the proper permissions.

You can generate restricted API keys in the Dashboard to enable customizable and limited access to the API. However, Stripe doesn’t offer any restricted keys by default.

If you’re logged in to Stripe, our documentation populates code examples with your test API keys. Only you can see these values. If you’re not logged in, our code examples include randomly generated API keys that you can replace with your test keys. Or you can log in to see the code examples populated with your test API keys.

The following table shows randomly generated examples of secret and publishable keys:

Anyone can use your live mode secret key to make an API call on behalf of your account, such as creating a charge or performing a refund. Follow these best practices to keep your secret API keys safe.

All Stripe API requests occur in either a sandbox or live mode. You can use a sandbox to access test data, and live mode to access actual account data. Each mode has its own set of API keys, and objects in one mode aren’t accessible to the other. For example, a sandbox product object can’t be part of a live mode payment.

You can only reveal a live mode secret or restricted API key one time. If you lose it, you can’t retrieve it from the Dashboard. In that case, rotate or delete it, and then create a new one.

If you have multiple Stripe business accounts in an organization, you can configure a single API key at the organization level. Organization-level API keys provide the following functionality:

Organization API keys behave differently from account-level API keys, including:

When you use an organization API key, you must also:

For example, given the following organization structure:

You can use the organization API key to access the balance of the standalone account. You can also use the same key to make the same call for the platform connected account.

In the preceding code example, replace {{CONTEXT}} with the relevant value:

You must specify the relevant account using the context and the API version in any API request using an organization key.

Organizations don’t have publishable API keys because they can’t accept payments. You can use your organization API key to create a PaymentIntent for any account in your organization, but you must use existing account-specific publishable keys for the client-side operations.

Use the Dashboard to create, reveal, modify, delete, and rotate secret and restricted keys.

You can create a secret API key or a restricted API key. A restricted API key only allows the level of access that you specify.

You can reveal a secret API key or a restricted API key in a sandbox or live mode.

In live mode, Stripe only shows you the API key one time (for security purposes). Store the key in a place where you won’t lose it. To remind yourself where you stored it, you can add a note on the key in the Dashboard. If you lose the key, you can rotate or delete it and create another.

After you create a secret or restricted API key in live mode, we display it before you save it. You must copy the key before saving it because you can’t copy it later. You can only reveal a default secret key or a key generated by a scheduled rotation.

Keys that you created before Stripe introduced this feature aren’t automatically hidden when they’re revealed. You must manually hide them by clicking Hide live key.

You can limit a secret API key or a restricted API key to a range of IP addresses, or one or more specific IP addresses.

IP addresses must use the IPv4 protocol, and you can specify any valid CIDR range. For example, you can specify the 100.10.38.0 - 100.10.38.255 range as 100.10.38.0/24. All IP addresses in the range must start with 100.10.38.

On the API keys tab, in the Standard keys or Restricted keys list, click the overflow menu () for the key you want to reveal.

Select Manage IP restrictions > Limit use to a set of IP addresses.

Do one of the following:

You can also enter individual IP addresses and ranges (separated by spaces) on the Bulk manage tab. Changes you make in one tab appear in the other tab.

To add another IP address or range, click + Add.

If you delete a secret API key or a restricted API key, you must create a new one and update any code that uses the deleted key. Any code that uses the deleted key can no longer make API calls.

You can’t delete a publishable key.

Rotating an API key revokes it and generates a replacement key that’s ready to use immediately. You can also schedule an API key to rotate after a certain time. The replacement key is named as follows:

You can rename a secret or restricted API key by editing the key.

Rotate an API key in scenarios such as:

To open the API request logs, click the overflow menu () for any key, then select View request logs. Opening the logs redirects you to the Stripe Dashboard.

**Examples:**

Example 1 (unknown):
```unknown
Organization (org_6SD3oI0eSQemPzdmaGLJ5j6)
  ├── Platform account  (acct_1R3fqDP6919yCiFv)
  |   └── Connected account (acct_1032D82eZvKYlo2C)
  └── Standalone account (acct_1aTnTtAAB0hHJ26p)
```

Example 2 (unknown):
```unknown
Organization (org_6SD3oI0eSQemPzdmaGLJ5j6)
  ├── Platform account  (acct_1R3fqDP6919yCiFv)
  |   └── Connected account (acct_1032D82eZvKYlo2C)
  └── Standalone account (acct_1aTnTtAAB0hHJ26p)
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/balance \
  -u {{ORG_SECRET_KEY}}: \
  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \
  -H "Stripe-Context: {{CONTEXT}}"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/balance \
  -u {{ORG_SECRET_KEY}}: \
  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \
  -H "Stripe-Context: {{CONTEXT}}"
```

---

## List all PaymentIntents

**URL:** https://docs.stripe.com/api/payment_intents/list

**Contents:**
- List all PaymentIntents
  - Parameters
    - customerstring
    - customer_accountstring
  - More parametersExpand all
    - createdobject
    - ending_beforestring
    - limitinteger
    - starting_afterstring
  - Returns

Returns a list of PaymentIntents.

Only return PaymentIntents for the customer that this customer ID specifies.

Only return PaymentIntents for the account representing the customer that this ID specifies.

A dictionary with a data property that contains an array of up to limit PaymentIntents, starting after PaymentIntent starting_after. Each entry in the array is a separate PaymentIntent object. If no other PaymentIntents are available, the resulting array is empty.

You can cancel a PaymentIntent object when it’s in one of these statuses: requires_payment_method, requires_capture, requires_confirmation, requires_action or, in rare cases, processing.

After it’s canceled, no additional charges are made by the PaymentIntent and any operations on the PaymentIntent fail with an error. For PaymentIntents with a status of requires_capture, the remaining amount_capturable is automatically refunded.

You can’t cancel the PaymentIntent for a Checkout Session. Expire the Checkout Session instead.

Reason for canceling this PaymentIntent. Possible values are: duplicate, fraudulent, requested_by_customer, or abandoned

Returns a PaymentIntent object if the cancellation succeeds. Returns an error if the PaymentIntent is already canceled or isn’t in a cancelable state.

Capture the funds of an existing uncaptured PaymentIntent when its status is requires_capture.

Uncaptured PaymentIntents are cancelled a set number of days (7 by default) after their creation.

Learn more about separate authorization and capture.

The amount to capture from the PaymentIntent, which must be less than or equal to the original amount. Defaults to the full amount_capturable if it’s not provided.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a PaymentIntent object with status="succeeded" if the PaymentIntent is capturable. Returns an error if the PaymentIntent isn’t capturable or if an invalid amount to capture is provided.

Confirm that your customer intends to pay with current or provided payment method. Upon confirmation, the PaymentIntent will attempt to initiate a payment.

If the selected payment method requires additional authentication steps, the PaymentIntent will transition to the requires_action status and suggest additional actions via next_action. If payment fails, the PaymentIntent transitions to the requires_payment_method status or the canceled status if the confirmation limit is reached. If payment succeeds, the PaymentIntent will transition to the succeeded status (or requires_capture, if capture_method is set to manual).

If the confirmation_method is automatic, payment may be attempted using our client SDKs and the PaymentIntent’s client_secret. After next_actions are handled by the client, no additional confirmation is required to complete the payment.

If the confirmation_method is manual, all payment attempts must be initiated using a secret key.

If any actions are required for the payment, the PaymentIntent will return to the requires_confirmation state after those actions are completed. Your server needs to then explicitly re-confirm the PaymentIntent to initiate the next payment attempt.

There is a variable upper limit on how many times a PaymentIntent can be confirmed. After this limit is reached, any further calls to this endpoint will transition the PaymentIntent to the canceled state.

ID of the payment method (a PaymentMethod, Card, or compatible Source object) to attach to this PaymentIntent. If the payment method is attached to a Customer, it must match the customer that is set on this PaymentIntent.

Email address that the receipt for the resulting payment will be sent to. If receipt_email is specified for a payment in live mode, a receipt will be sent regardless of your email settings.

Indicates that you intend to make future payments with this PaymentIntent’s payment method.

If you provide a Customer with the PaymentIntent, you can use this parameter to attach the payment method to the Customer after the PaymentIntent is confirmed and the customer completes any required actions. If you don’t provide a Customer, you can still attach the payment method to a Customer after the transaction completes.

If the payment method is card_present and isn’t a digital wallet, Stripe creates and attaches a generated_card payment method representing the card to the Customer instead.

When processing card payments, Stripe uses setup_future_usage to help you comply with regional legislation and network rules, such as SCA.

If you’ve already set setup_future_usage and you’re performing a request using a publishable key, you can only update the value from on_session to off_session.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

Shipping information for this PaymentIntent.

Returns the resulting PaymentIntent after all possible transitions are applied.

Perform an incremental authorization on an eligible PaymentIntent. To be eligible, the PaymentIntent’s status must be requires_capture and incremental_authorization_supported must be true.

Incremental authorizations attempt to increase the authorized amount on your customer’s card to the new, higher amount provided. Similar to the initial authorization, incremental authorizations can be declined. A single PaymentIntent can call this endpoint multiple times to further increase the authorized amount.

If the incremental authorization succeeds, the PaymentIntent object returns with the updated amount. If the incremental authorization fails, a card_declined error returns, and no other fields on the PaymentIntent or Charge update. The PaymentIntent object remains capturable for the previously authorized amount.

Each PaymentIntent can have a maximum of 10 incremental authorization attempts, including declines. After it’s captured, a PaymentIntent can no longer be incremented.

Learn more about incremental authorizations.

The updated total amount that you intend to collect from the cardholder. This amount must be greater than the currently authorized amount.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Text that appears on the customer’s statement as the statement descriptor for a non-card or card charge. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

Returns a PaymentIntent object with the updated amount if the incremental authorization succeeds. Returns an error if the incremental authorization failed or the PaymentIntent isn’t eligible for incremental authorizations.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v1/payment_intents \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v1/payment_intents \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 3 (unknown):
```unknown
{  "object": "list",  "url": "/v1/payment_intents",  "has_more": false,  "data": [    {      "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",      "object": "payment_intent",      "amount": 2000,      "amount_capturable": 0,      "amount_details": {        "tip": {}      },      "amount_received": 0,      "application": null,      "application_fee_amount": null,      "automatic_payment_methods": {        "enabled": true      },      "canceled_at": null,      "cancellation_reason": null,      "capture_method": "automatic",      "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",      "confirmation_method": "automatic",      "created": 1680800504,      "currency": "usd",      "customer": null,      "description": null,      "last_payment_error": null,      "latest_charge": null,      "livemode": false,      "metadata": {},      "next_action": null,      "on_behalf_of": null,      "payment_method": null,      "payment_method_options": {        "card": {          "installments": null,          "mandate_options": null,          "network": null,          "request_three_d_secure": "automatic"        },        "link": {          "persistent_token": null        }      },      "payment_method_types": [        "card",        "link"      ],      "processing": null,      "receipt_email": null,      "review": null,      "setup_future_usage": null,      "shipping": null,      "source": null,      "statement_descriptor": null,      "statement_descriptor_suffix": null,      "status": "requires_payment_method",      "transfer_data": null,      "transfer_group": null    }  ]}
```

Example 4 (unknown):
```unknown
{  "object": "list",  "url": "/v1/payment_intents",  "has_more": false,  "data": [    {      "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",      "object": "payment_intent",      "amount": 2000,      "amount_capturable": 0,      "amount_details": {        "tip": {}      },      "amount_received": 0,      "application": null,      "application_fee_amount": null,      "automatic_payment_methods": {        "enabled": true      },      "canceled_at": null,      "cancellation_reason": null,      "capture_method": "automatic",      "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",      "confirmation_method": "automatic",      "created": 1680800504,      "currency": "usd",      "customer": null,      "description": null,      "last_payment_error": null,      "latest_charge": null,      "livemode": false,      "metadata": {},      "next_action": null,      "on_behalf_of": null,      "payment_method": null,      "payment_method_options": {        "card": {          "installments": null,          "mandate_options": null,          "network": null,          "request_three_d_secure": "automatic"        },        "link": {          "persistent_token": null        }      },      "payment_method_types": [        "card",        "link"      ],      "processing": null,      "receipt_email": null,      "review": null,      "setup_future_usage": null,      "shipping": null,      "source": null,      "statement_descriptor": null,      "statement_descriptor_suffix": null,      "status": "requires_payment_method",      "transfer_data": null,      "transfer_group": null    }  ]}
```

---

## Deployment checklist

**URL:** https://docs.stripe.com/terminal/references/checklist

**Contents:**
- Deployment checklist
- Use this checklist to help ensure a smooth deployment of Stripe Terminal.
  - Checklist progress

As you complete each item and check it off, the state of each checkbox is stored within your browser’s cache. You can refer back to this page at any time to see what you have completed so far.

Stripe Terminal requires integrating hardware and software to bring Stripe to the physical world. As you develop your integration, refer to this checklist to make sure you cover all the critical steps.

It’s fine to go out of order, but understanding the full scope of a Terminal integration helps you connect all the pieces.

After following the integration guides for Stripe Terminal, check that your application is set up correctly.

To handle the ConnectionToken lifecycle, set up an endpoint on your backend that creates a ConnectionToken for your client application. Authenticate this endpoint to control who can access your readers. Don’t hard-code the ConnectionToken in your application—it prevents you from reconnecting to a reader. To further control access to smart readers like the Verifone P400 and BBPOS WisePOS E, use Locations.

If you defined the PaymentIntent capture_method as manual, the payment is authorized but not captured when the SDK returns a processed PaymentIntent to your application. To complete collection of funds, you must capture the PaymentIntent.

When your application receives a processed PaymentIntent from the SDK, make sure it notifies your backend to capture the PaymentIntent.

Provide your customer with the option to receive a paper or email receipt. You can use Stripe’s prebuilt receipts, or use receipt data from the Stripe API to build custom receipts that are on-brand for your business. Test that you receive a receipt when you create a live mode payment using your application.

If you provide your customers with custom receipts, save a copy of each receipt as dispute evidence. If you use Stripe’s prebuilt receipts, a copy of the receipt is saved automatically and available in the Dashboard.

Reconcile payments with your internal orders system on your server at the end of a day’s activity to avoid unintended authorizations or un-captured funds:

The BBPOS Chipper 2X BT doesn’t auto-update, so your application needs to support updates. Although they’re rare, updates usually contain important features or critical fixes. Make sure your app supports the following:

Refer to our example applications (iOS, Android) for a reference UI.

For smart readers like the Verifone P400 and BBPOS WisePOS E, you must register the reader to your account before you can connect your application to the reader.

How you handle reader registration depends on your use case:

Deployment size: For smaller deployments, register each reader in the Stripe Dashboard. For larger deployments that require shipping readers to various locations, make sure site managers can add new readers to your company’s Stripe account. Build a workflow into your application to let others register readers to your Stripe account. The endpoint for registering a reader must be called server side. If you support registering readers from your client application, the app must communicate with your backend to register the reader.

Using Connect: If you use Connect direct charges, use the Stripe-Account header to register the reader to the connected account. With destination charges, register new readers to the platform account.

Create a Terminal Location object for each physical operating site at which your business accepts in-person payments. You must register each reader to a location to ensure that it downloads the proper regional configuration.

For smart readers, support specifying a location while registering the reader. For Bluetooth readers, support specifying a location while connecting to the reader.

Make sure your application can display an updating list of discovered readers, with the label and/or serial number of each. Refer to our example applications for a sample UI.

If you expect your mobile app to be used with multiple Bluetooth readers, use the Bluetooth Proximity discovery method. Include in your app instructions to hold the reader close to the app device, and wait for it to begin flashing multiple colors. Make sure your app’s UI allows canceling the reader discovery process.

If you use the Verifone P400 or BBPOS WisePOS E, check that the reader and the device running your application are both on the correct LAN. Include in your application instructions for verifying the correct LAN.

Stripe periodically releases updates which can include new functionality, bug fixes, and security updates. Update your SDK as soon as a new version is available. The currently available SDKs are:

The default admin menu passcode for your smart readers is 07139. For security, you should set your own custom 5 digit passcode.

The BBPOS and Chipper™ name and logo are trademarks or registered trademarks of BBPOS Limited in the United States or other countries. The Verifone® name and logo are either trademarks or registered trademarks of Verifone in the United States and/or other countries. Use of the trademarks doesn’t imply any endorsement by BBPOS or Verifone.

---

## Create a payout

**URL:** https://docs.stripe.com/api/payouts/create

**Contents:**
- Create a payout
  - Parameters
    - amountintegerRequired
    - currencyenumRequired
    - descriptionstring
    - metadataobject
    - statement_descriptorstring
  - More parametersExpand all
    - destinationstring
    - methodstring

To send funds to your own bank account, create a new payout object. Your Stripe balance must cover the payout amount. If it doesn’t, you receive an “Insufficient Funds” error.

If your API key is in test mode, money won’t actually be sent, though every other action occurs as if you’re in live mode.

If you create a manual payout on a Stripe account that uses multiple payment source types, you need to specify the source type balance that the payout draws from. The balance object details available and pending amounts by source type.

A positive integer in cents representing how much to payout.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

A string that displays on the recipient’s bank or card statement (up to 22 characters). A statement_descriptor that’s longer than 22 characters return an error. Most banks truncate this information and display it inconsistently. Some banks might not display it at all.

Returns a payout object if no initial errors are present during the payout creation (invalid routing number, insufficient funds, and so on). We initially mark the status of the payout object as pending.

Updates the specified payout by setting the values of the parameters you pass. We don’t change parameters that you don’t provide. This request only accepts the metadata as arguments.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the payout object if the update succeeds. This call raises an error if update parameters are invalid.

Retrieves the details of an existing payout. Supply the unique payout ID from either a payout creation request or the payout list. Stripe returns the corresponding payout information.

Returns a payout object if a you provide a valid identifier. raises An error occurs otherwise.

Returns a list of existing payouts sent to third-party bank accounts or payouts that Stripe sent to you. The payouts return in sorted order, with the most recently created payouts appearing first.

Only return payouts that have the given status: pending, paid, failed, or canceled.

A dictionary with a data property that contains an array of up to limit payouts, starting after payout starting_after. Each entry in the array is a separate payout object. If no other payouts are available, the resulting array is empty.

You can cancel a previously created payout if its status is pending. Stripe refunds the funds to your available balance. You can’t cancel automatic Stripe payouts.

Returns the payout object if the cancellation succeeds. Returns an error if the payout is already canceled or can’t be canceled.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payouts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=1100 \  -d currency=usd
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payouts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=1100 \  -d currency=usd
```

Example 3 (unknown):
```unknown
{  "id": "po_1OaFDbEcg9tTZuTgNYmX0PKB",  "object": "payout",  "amount": 1100,  "arrival_date": 1680652800,  "automatic": false,  "balance_transaction": "txn_1OaFDcEcg9tTZuTgYMR25tSe",  "created": 1680648691,  "currency": "usd",  "description": null,  "destination": "ba_1MtIhL2eZvKYlo2CAElKwKu2",  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "livemode": false,  "metadata": {},  "method": "standard",  "original_payout": null,  "reconciliation_status": "not_applicable",  "reversed_by": null,  "source_type": "card",  "statement_descriptor": null,  "status": "pending",  "type": "bank_account"}
```

Example 4 (unknown):
```unknown
{  "id": "po_1OaFDbEcg9tTZuTgNYmX0PKB",  "object": "payout",  "amount": 1100,  "arrival_date": 1680652800,  "automatic": false,  "balance_transaction": "txn_1OaFDcEcg9tTZuTgYMR25tSe",  "created": 1680648691,  "currency": "usd",  "description": null,  "destination": "ba_1MtIhL2eZvKYlo2CAElKwKu2",  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "livemode": false,  "metadata": {},  "method": "standard",  "original_payout": null,  "reconciliation_status": "not_applicable",  "reversed_by": null,  "source_type": "card",  "statement_descriptor": null,  "status": "pending",  "type": "bank_account"}
```

---

## List all disputes

**URL:** https://docs.stripe.com/api/disputes/list

**Contents:**
- List all disputes
  - Parameters
    - chargestring
    - payment_intentstring
  - More parametersExpand all
    - createdobject
    - ending_beforestring
    - limitinteger
    - starting_afterstring
  - Returns

Returns a list of your disputes.

Only return disputes associated to the charge specified by this charge ID.

Only return disputes associated to the PaymentIntent specified by this PaymentIntent ID.

A dictionary with a data property that contains an array of up to limit disputes, starting after dispute starting_after. Each entry in the array is a separate dispute object. If no more disputes are available, the resulting array will be empty.

Closing the dispute for a charge indicates that you do not have any evidence to submit and are essentially dismissing the dispute, acknowledging it as lost.

The status of the dispute will change from needs_response to lost. Closing a dispute is irreversible.

Returns the dispute object.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v1/disputes \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v1/disputes \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 3 (unknown):
```unknown
{  "object": "list",  "url": "/v1/disputes",  "has_more": false,  "data": [    {      "id": "du_1MtJUT2eZvKYlo2CNaw2HvEv",      "object": "dispute",      "amount": 1000,      "balance_transactions": [],      "charge": "ch_1AZtxr2eZvKYlo2CJDX8whov",      "created": 1680651737,      "currency": "usd",      "evidence": {        "access_activity_log": null,        "billing_address": null,        "cancellation_policy": null,        "cancellation_policy_disclosure": null,        "cancellation_rebuttal": null,        "customer_communication": null,        "customer_email_address": null,        "customer_name": null,        "customer_purchase_ip": null,        "customer_signature": null,        "duplicate_charge_documentation": null,        "duplicate_charge_explanation": null,        "duplicate_charge_id": null,        "product_description": null,        "receipt": null,        "refund_policy": null,        "refund_policy_disclosure": null,        "refund_refusal_explanation": null,        "service_date": null,        "service_documentation": null,        "shipping_address": null,        "shipping_carrier": null,        "shipping_date": null,        "shipping_documentation": null,        "shipping_tracking_number": null,        "uncategorized_file": null,        "uncategorized_text": null      },      "evidence_details": {        "due_by": 1682294399,        "has_evidence": false,        "past_due": false,        "submission_count": 0      },      "is_charge_refundable": true,      "livemode": false,      "metadata": {},      "payment_intent": null,      "reason": "general",      "status": "warning_needs_response"    }  ]}
```

Example 4 (unknown):
```unknown
{  "object": "list",  "url": "/v1/disputes",  "has_more": false,  "data": [    {      "id": "du_1MtJUT2eZvKYlo2CNaw2HvEv",      "object": "dispute",      "amount": 1000,      "balance_transactions": [],      "charge": "ch_1AZtxr2eZvKYlo2CJDX8whov",      "created": 1680651737,      "currency": "usd",      "evidence": {        "access_activity_log": null,        "billing_address": null,        "cancellation_policy": null,        "cancellation_policy_disclosure": null,        "cancellation_rebuttal": null,        "customer_communication": null,        "customer_email_address": null,        "customer_name": null,        "customer_purchase_ip": null,        "customer_signature": null,        "duplicate_charge_documentation": null,        "duplicate_charge_explanation": null,        "duplicate_charge_id": null,        "product_description": null,        "receipt": null,        "refund_policy": null,        "refund_policy_disclosure": null,        "refund_refusal_explanation": null,        "service_date": null,        "service_documentation": null,        "shipping_address": null,        "shipping_carrier": null,        "shipping_date": null,        "shipping_documentation": null,        "shipping_tracking_number": null,        "uncategorized_file": null,        "uncategorized_text": null      },      "evidence_details": {        "due_by": 1682294399,        "has_evidence": false,        "past_due": false,        "submission_count": 0      },      "is_charge_refundable": true,      "livemode": false,      "metadata": {},      "payment_intent": null,      "reason": "general",      "status": "warning_needs_response"    }  ]}
```

---

## Retrieve a Mandate

**URL:** https://docs.stripe.com/api/mandates/retrieve

**Contents:**
- Retrieve a Mandate
  - Parameters
  - Returns

Retrieves a Mandate object.

Returns a Mandate object.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/mandates/mandate_1MvojA2eZvKYlo2CvqTABjZs \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/mandates/mandate_1MvojA2eZvKYlo2CvqTABjZs \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "mandate_1MvojA2eZvKYlo2CvqTABjZs",  "object": "mandate",  "customer_acceptance": {    "accepted_at": 123456789,    "online": {      "ip_address": "127.0.0.0",      "user_agent": "device"    },    "type": "online"  },  "livemode": false,  "multi_use": {},  "payment_method": "pm_123456789",  "payment_method_details": {    "sepa_debit": {      "reference": "123456789",      "url": ""    },    "type": "sepa_debit"  },  "status": "active",  "type": "multi_use"}
```

Example 4 (unknown):
```unknown
{  "id": "mandate_1MvojA2eZvKYlo2CvqTABjZs",  "object": "mandate",  "customer_acceptance": {    "accepted_at": 123456789,    "online": {      "ip_address": "127.0.0.0",      "user_agent": "device"    },    "type": "online"  },  "livemode": false,  "multi_use": {},  "payment_method": "pm_123456789",  "payment_method_details": {    "sepa_debit": {      "reference": "123456789",      "url": ""    },    "type": "sepa_debit"  },  "status": "active",  "type": "multi_use"}
```

---

## Invoice Rendering Templates

**URL:** https://docs.stripe.com/api/invoice-rendering-template

**Contents:**
- Invoice Rendering Templates
- The Invoice Rendering Template object
  - Attributes
    - idstring
    - objectstring
    - createdtimestamp
    - livemodeboolean
    - metadatanullable object
    - nicknamenullable string
    - statusenum

Invoice Rendering Templates are used to configure how invoices are rendered on surfaces like the PDF. Invoice Rendering Templates can be created from within the Dashboard, and they can be used over the API when creating invoices.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value.

Time at which the object was created. Measured in seconds since the Unix epoch.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

A brief description of the template, hidden from customers

The status of the template, one of active or archived.

Version of this template; version increases by one when an update on the template changes any field that controls invoice rendering

Retrieves an invoice rendering template with the given ID. It by default returns the latest version of the template. Optionally, specify a version to see previous versions.

Returns an invoice_payment object if a valid invoice payment ID and matching invoice ID were provided. Otherwise, this call raises an error.

List all templates, ordered by creation date, with the most recently created template appearing first.

A dictionary with a data property that contains an array of up to limit templates, starting after template starting_after. Each entry in the array is a separate template object. If no more templates are available, the resulting array will be empty.

Updates the status of an invoice rendering template to ‘archived’ so no new Stripe objects (customers, invoices, etc.) can reference it. The template can also no longer be updated. However, if the template is already set on a Stripe object, it will continue to be applied on invoices generated by it.

The updated template object is returned if successful. Otherwise, this call raises an error.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "inrtem_abc",  "object": "invoice_rendering_template",  "nickname": "My Invoice Template",  "status": "active",  "version": 1,  "created": 1678942624,  "livemode": false}
```

Example 2 (unknown):
```unknown
{  "id": "inrtem_abc",  "object": "invoice_rendering_template",  "nickname": "My Invoice Template",  "status": "active",  "version": 1,  "created": 1678942624,  "livemode": false}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/invoice_rendering_templates/inrtem_abc \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/invoice_rendering_templates/inrtem_abc \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

---

## Confirmation Token

**URL:** https://docs.stripe.com/api/confirmation_tokens

**Contents:**
- Confirmation Token
- The Confirmation Token object
  - Attributes
    - idstring
    - objectstring
    - createdtimestamp
    - expires_atnullable timestamp
    - livemodeboolean
    - mandate_datanullable object
    - payment_intentnullable string

ConfirmationTokens help transport client side data collected by Stripe JS over to your server for confirming a PaymentIntent or SetupIntent. If the confirmation is successful, values present on the ConfirmationToken are written onto the Intent.

To learn more about how to use ConfirmationToken, visit the related guides:

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value.

Time at which the object was created. Measured in seconds since the Unix epoch.

Time at which this ConfirmationToken expires and can no longer be used to confirm a PaymentIntent or SetupIntent.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Data used for generating a Mandate.

ID of the PaymentIntent that this ConfirmationToken was used to confirm, or null if this ConfirmationToken has not yet been used.

Payment-method-specific configuration for this ConfirmationToken.

Payment details collected by the Payment Element, used to create a PaymentMethod when a PaymentIntent or SetupIntent is confirmed with this ConfirmationToken.

Return URL used to confirm the Intent.

Indicates that you intend to make future payments with this ConfirmationToken’s payment method.

The presence of this property will attach the payment method to the PaymentIntent’s Customer, if present, after the PaymentIntent is confirmed and any required actions from the user are complete.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

ID of the SetupIntent that this ConfirmationToken was used to confirm, or null if this ConfirmationToken has not yet been used.

Shipping information collected on this ConfirmationToken.

Indicates whether the Stripe SDK is used to handle confirmation flow. Defaults to true on ConfirmationToken.

Retrieves an existing ConfirmationToken object

Returns the specified ConfirmationToken

Creates a test mode Confirmation Token server side for your integration tests.

ID of an existing PaymentMethod.

If provided, this hash will be used to create a PaymentMethod.

Payment-method-specific configuration for this ConfirmationToken.

Return URL used to confirm the Intent.

Indicates that you intend to make future payments with this ConfirmationToken’s payment method.

The presence of this property will attach the payment method to the PaymentIntent’s Customer, if present, after the PaymentIntent is confirmed and any required actions from the user are complete.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

Shipping information for this ConfirmationToken.

Returns a testmode Confirmation Token

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "ctoken_1NnQUf2eZvKYlo2CIObdtbnb",  "object": "confirmation_token",  "created": 1694025025,  "expires_at": 1694068225,  "livemode": true,  "mandate_data": null,  "payment_intent": null,  "payment_method": null,  "payment_method_preview": {    "billing_details": {      "address": {        "city": "Hyde Park",        "country": "US",        "line1": "50 Sprague St",        "line2": "",        "postal_code": "02136",        "state": "MA"      },      "email": "jennyrosen@stripe.com",      "name": "Jenny Rosen",      "phone": null    },    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": null      },      "country": "US",      "display_brand": "visa",      "exp_month": 8,      "exp_year": 2026,      "funding": "credit",      "generated_from": null,      "last4": "4242",      "networks": {        "available": [          "visa"        ],        "preferred": null      },      "three_d_secure_usage": {        "supported": true      },      "wallet": null    },    "type": "card"  },  "return_url": "https://example.com/return",  "setup_future_usage": "off_session",  "setup_intent": null,  "shipping": {    "address": {      "city": "Hyde Park",      "country": "US",      "line1": "50 Sprague St",      "line2": "",      "postal_code": "02136",      "state": "MA"    },    "name": "Jenny Rosen",    "phone": null  }}
```

Example 2 (unknown):
```unknown
{  "id": "ctoken_1NnQUf2eZvKYlo2CIObdtbnb",  "object": "confirmation_token",  "created": 1694025025,  "expires_at": 1694068225,  "livemode": true,  "mandate_data": null,  "payment_intent": null,  "payment_method": null,  "payment_method_preview": {    "billing_details": {      "address": {        "city": "Hyde Park",        "country": "US",        "line1": "50 Sprague St",        "line2": "",        "postal_code": "02136",        "state": "MA"      },      "email": "jennyrosen@stripe.com",      "name": "Jenny Rosen",      "phone": null    },    "card": {      "brand": "visa",      "checks": {        "address_line1_check": null,        "address_postal_code_check": null,        "cvc_check": null      },      "country": "US",      "display_brand": "visa",      "exp_month": 8,      "exp_year": 2026,      "funding": "credit",      "generated_from": null,      "last4": "4242",      "networks": {        "available": [          "visa"        ],        "preferred": null      },      "three_d_secure_usage": {        "supported": true      },      "wallet": null    },    "type": "card"  },  "return_url": "https://example.com/return",  "setup_future_usage": "off_session",  "setup_intent": null,  "shipping": {    "address": {      "city": "Hyde Park",      "country": "US",      "line1": "50 Sprague St",      "line2": "",      "postal_code": "02136",      "state": "MA"    },    "name": "Jenny Rosen",    "phone": null  }}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/confirmation_tokens/ctoken_1NnQUf2eZvKYlo2CIObdtbnb \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/confirmation_tokens/ctoken_1NnQUf2eZvKYlo2CIObdtbnb \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

---

## The Balance object

**URL:** https://docs.stripe.com/api/balance/balance_object

**Contents:**
- The Balance object
  - Attributes
    - availablearray of objects
    - pendingarray of objects
  - More attributesExpand all
    - objectstring
    - connect_reservednullable array of objectsConnect only
    - instant_availablenullable array of objects
    - issuingnullable object
    - livemodeboolean

Available funds that you can transfer or pay out automatically by Stripe or explicitly through the Transfers API or Payouts API. You can find the available balance for each currency and payment type in the source_types property.

Funds that aren’t available in the balance yet. You can find the pending balance for each currency and each payment type in the source_types property.

Retrieves the current account balance, based on the authentication that was used to make the request. For a sample request, see Accounting for negative balances.

Returns a balance object for the account that was authenticated in the request.

**Examples:**

Example 1 (unknown):
```unknown
{  "object": "balance",  "available": [    {      "amount": 666670,      "currency": "usd",      "source_types": {        "card": 666670      }    }  ],  "connect_reserved": [    {      "amount": 0,      "currency": "usd"    }  ],  "livemode": false,  "pending": [    {      "amount": 61414,      "currency": "usd",      "source_types": {        "card": 61414      }    }  ]}
```

Example 2 (unknown):
```unknown
{  "object": "balance",  "available": [    {      "amount": 666670,      "currency": "usd",      "source_types": {        "card": 666670      }    }  ],  "connect_reserved": [    {      "amount": 0,      "currency": "usd"    }  ],  "livemode": false,  "pending": [    {      "amount": 61414,      "currency": "usd",      "source_types": {        "card": 61414      }    }  ]}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/balance \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/balance \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

---

## Search customers

**URL:** https://docs.stripe.com/api/customers/search

**Contents:**
- Search customers
  - Parameters
    - querystringRequired
    - limitinteger
    - pagestring
  - Returns

Search for customers you’ve previously created using Stripe’s Search Query Language. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.

The search query string. See search query language and the list of supported query fields for customers.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A dictionary with a data property that contains an array of up to limit customers. If no objects match the query, the resulting array will be empty. See the related guide on expanding properties in lists.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v1/customers/search \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  --data-urlencode query="name:'Jane Doe' AND metadata['foo']:'bar'"
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v1/customers/search \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  --data-urlencode query="name:'Jane Doe' AND metadata['foo']:'bar'"
```

Example 3 (unknown):
```unknown
{  "object": "search_result",  "url": "/v1/customers/search",  "has_more": false,  "data": [    {      "id": "cus_NeGfPRiPKxeBi1",      "object": "customer",      "address": null,      "balance": 0,      "created": 1680569616,      "currency": null,      "default_source": null,      "delinquent": false,      "description": null,      "email": null,      "invoice_prefix": "47D37F8F",      "invoice_settings": {        "custom_fields": null,        "default_payment_method": "pm_1Msy7wLkdIwHu7ixsxmFvcz7",        "footer": null,        "rendering_options": null      },      "livemode": false,      "metadata": {        "foo": "bar"      },      "name": "Jane Doe",      "next_invoice_sequence": 1,      "phone": null,      "preferred_locales": [],      "shipping": null,      "tax_exempt": "none",      "test_clock": null    }  ]}
```

Example 4 (unknown):
```unknown
{  "object": "search_result",  "url": "/v1/customers/search",  "has_more": false,  "data": [    {      "id": "cus_NeGfPRiPKxeBi1",      "object": "customer",      "address": null,      "balance": 0,      "created": 1680569616,      "currency": null,      "default_source": null,      "delinquent": false,      "description": null,      "email": null,      "invoice_prefix": "47D37F8F",      "invoice_settings": {        "custom_fields": null,        "default_payment_method": "pm_1Msy7wLkdIwHu7ixsxmFvcz7",        "footer": null,        "rendering_options": null      },      "livemode": false,      "metadata": {        "foo": "bar"      },      "name": "Jane Doe",      "next_invoice_sequence": 1,      "phone": null,      "preferred_locales": [],      "shipping": null,      "tax_exempt": "none",      "test_clock": null    }  ]}
```

---

## Enable an event destination v2

**URL:** https://docs.stripe.com/api/v2/core/event_destinations/enable

**Contents:**
- Enable an event destination v2
  - Parameters
    - idstringRequired
  - Returns
  - Response attributes
    - idstring
    - objectstring, value is "v2.core.event_destination"
    - amazon_eventbridgenullable object
    - createdtimestamp
    - descriptionstring

Enable an event destination.

Identifier for the event destination to enable.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value of the object field.

Amazon EventBridge configuration.

Time at which the object was created.

An optional description of what the event destination is used for.

The list of events to enable for this endpoint.

Payload type of events being subscribed to.

Where events should be routed from.

Receive events from accounts connected to the account that owns the event destination.

Receive events from the account that owns the event destination.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Event destination name.

If using the snapshot event payload, the API version events are rendered as.

Status. It can be set to either enabled or disabled.

Event destination is disabled.

Event destination is enabled.

Additional information about event destination status.

Event destination type.

Time at which the object was last updated.

Webhook endpoint configuration.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

This is a list of all public thin events we currently send for updates to EventDestination, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/event_destinations/ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6/enable \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/event_destinations/ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6/enable \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 3 (unknown):
```unknown
{  "id": "ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6",  "object": "v2.core.event_destination",  "created": "2024-10-22T16:20:09.931Z",  "description": "This is my event destination, I like it a lot",  "enabled_events": [    "v1.billing.meter.error_report_triggered"  ],  "event_payload": "thin",  "events_from": [    "self"  ],  "livemode": false,  "metadata": {},  "name": "My Event Destination",  "snapshot_api_version": null,  "status": "enabled",  "status_details": null,  "type": "webhook_endpoint",  "updated": "2024-10-22T16:21:38.634Z",  "webhook_endpoint": {    "signing_secret": null,    "url": null  }}
```

Example 4 (unknown):
```unknown
{  "id": "ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6",  "object": "v2.core.event_destination",  "created": "2024-10-22T16:20:09.931Z",  "description": "This is my event destination, I like it a lot",  "enabled_events": [    "v1.billing.meter.error_report_triggered"  ],  "event_payload": "thin",  "events_from": [    "self"  ],  "livemode": false,  "metadata": {},  "name": "My Event Destination",  "snapshot_api_version": null,  "status": "enabled",  "status_details": null,  "type": "webhook_endpoint",  "updated": "2024-10-22T16:21:38.634Z",  "webhook_endpoint": {    "signing_secret": null,    "url": null  }}
```

---

## Invoice Items

**URL:** https://docs.stripe.com/api/invoiceitems

**Contents:**
- Invoice Items
- The Invoice Item object
  - Attributes
    - idstring
    - amountinteger
    - currencyenum
    - customerstringExpandable
    - customer_accountnullable string
    - descriptionnullable string
    - metadatanullable object

Invoice Items represent the component lines of an invoice. When you create an invoice item with an invoice field, it is attached to the specified invoice and included as an invoice line item within invoice.lines.

Invoice Items can be created before you are ready to actually send the invoice. This can be particularly useful when combined with a subscription. Sometimes you want to add a charge or credit to a customer, but actually charge or credit the customer’s card only at the end of a regular billing cycle. This is useful for combining several charges (to minimize per-transaction fees), or for having Stripe tabulate your usage-based billing totals.

Related guides: Integrate with the Invoicing API, Subscription Invoices.

Unique identifier for the object.

Amount (in the currency specified) of the invoice item. This should always be equal to unit_amount * quantity.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

The ID of the customer to bill for this invoice item.

The ID of the account to bill for this invoice item.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The parent that generated this invoice item.

The period associated with this invoice item. When set to different values, the period will be rendered on the invoice. If you have Stripe Revenue Recognition enabled, the period will be used to recognize and defer revenue. See the Revenue Recognition documentation for details.

The pricing information of the invoice item.

Whether the invoice item was created automatically as a proration adjustment when the customer switched plans.

Creates an item to be added to a draft invoice (up to 250 items per invoice). If no invoice is specified, the item will be on the next invoice created for the customer specified.

The integer amount in cents of the charge to be applied to the upcoming invoice. Passing in a negative amount will reduce the amount_due on the invoice.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

The ID of the customer to bill for this invoice item.

The ID of the account representing the customer to bill for this invoice item.

An arbitrary string which you can attach to the invoice item. The description is displayed in the invoice for easy tracking.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The period associated with this invoice item. When set to different values, the period will be rendered on the invoice. If you have Stripe Revenue Recognition enabled, the period will be used to recognize and defer revenue. See the Revenue Recognition documentation for details.

The pricing information for the invoice item.

The created invoice item object is returned if successful. Otherwise, this call raises an error.

Updates the amount or description of an invoice item on an upcoming invoice. Updating an invoice item is only possible before the invoice it’s attached to is closed.

The integer amount in cents of the charge to be applied to the upcoming invoice. If you want to apply a credit to the customer’s account, pass a negative amount.

An arbitrary string which you can attach to the invoice item. The description is displayed in the invoice for easy tracking.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The period associated with this invoice item. When set to different values, the period will be rendered on the invoice. If you have Stripe Revenue Recognition enabled, the period will be used to recognize and defer revenue. See the Revenue Recognition documentation for details.

The pricing information for the invoice item.

The updated invoice item object is returned upon success. Otherwise, this call raises an error.

Retrieves the invoice item with the given ID.

Returns an invoice item if a valid invoice item ID was provided. Raises an error otherwise.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "ii_1MtGUtLkdIwHu7ixBYwjAM00",  "object": "invoiceitem",  "amount": 1099,  "currency": "usd",  "customer": "cus_NeZei8imSbMVvi",  "date": 1680640231,  "description": "T-shirt",  "discountable": true,  "discounts": [],  "invoice": null,  "livemode": false,  "metadata": {},  "parent": null,  "period": {    "end": 1680640231,    "start": 1680640231  },  "pricing": {    "price_details": {      "price": "price_1MtGUsLkdIwHu7ix1be5Ljaj",      "product": "prod_NeZe7xbBdJT8EN"    },    "type": "price_details",    "unit_amount_decimal": "1099"  },  "proration": false,  "quantity": 1,  "tax_rates": [],  "test_clock": null}
```

Example 2 (unknown):
```unknown
{  "id": "ii_1MtGUtLkdIwHu7ixBYwjAM00",  "object": "invoiceitem",  "amount": 1099,  "currency": "usd",  "customer": "cus_NeZei8imSbMVvi",  "date": 1680640231,  "description": "T-shirt",  "discountable": true,  "discounts": [],  "invoice": null,  "livemode": false,  "metadata": {},  "parent": null,  "period": {    "end": 1680640231,    "start": 1680640231  },  "pricing": {    "price_details": {      "price": "price_1MtGUsLkdIwHu7ix1be5Ljaj",      "product": "prod_NeZe7xbBdJT8EN"    },    "type": "price_details",    "unit_amount_decimal": "1099"  },  "proration": false,  "quantity": 1,  "tax_rates": [],  "test_clock": null}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/invoiceitems \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_NeZei8imSbMVvi \  -d "pricing[price]"=price_1MtGUsLkdIwHu7ix1be5Ljaj
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/invoiceitems \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_NeZei8imSbMVvi \  -d "pricing[price]"=price_1MtGUsLkdIwHu7ix1be5Ljaj
```

---

## Create a card token

**URL:** https://docs.stripe.com/api/tokens/create_card

**Contents:**
- Create a card token
  - Parameters
    - cardobject | string
  - Returns
- Create a CVC update token
  - Parameters
    - cvc_updateobjectRequired
  - Returns
- Create a person token
  - Parameters

Creates a single-use token that represents a credit card’s details. You can use this token in place of a credit card dictionary with any v1 API method. You can only use these tokens once by creating a new Charge object or by attaching them to a Customer object.

To use this functionality, you need to enable access to the raw card data APIs. In most cases, you can use our recommended payments integrations instead of using the API.

The card this token will represent. If you also pass in a customer, the card must be the ID of a card belonging to the customer. Otherwise, if you do not pass in a customer, this is a dictionary containing a user’s credit card details, with the options described below.

Returns the created card token if it’s successful. Otherwise, this call raises an error.

Creates a single-use token that represents an updated CVC value that you can use for CVC re-collection. Use this token when you confirm a card payment or use a saved card on a PaymentIntent with confirmation_method: manual.

For most cases, use our JavaScript library instead of using the API. For a PaymentIntent with confirmation_method: automatic, use our recommended payments integration without tokenizing the CVC value.

The updated CVC value this token represents.

Returns the created CVC update token if it’s successful. Otherwise, this call raises an error.

Creates a single-use token that represents the details for a person. Use this when you create or update persons associated with a Connect account. Learn more about account tokens.

You can only create person tokens with your application’s publishable key and in live mode. You can use your application’s secret key to create person tokens only in test mode.

Information for the person this token represents.

Returns the created person token if it’s successful. Otherwise, this call raises an error.

Creates a single-use token that represents the details of personally identifiable information (PII). You can use this token in place of an id_number or id_number_secondary in Account or Person Update API methods. You can only use a PII token once.

The PII this token represents.

Returns the created PII token if it’s successful. Otherwise, this call raises an error.

Retrieves the token with the given ID.

Returns a token if you provide a valid ID. Raises an error otherwise.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/tokens \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "card[number]"=4242424242424242 \  -d "card[exp_month]"=5 \  -d "card[exp_year]"=2026 \  -d "card[cvc]"=314
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/tokens \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "card[number]"=4242424242424242 \  -d "card[exp_month]"=5 \  -d "card[exp_year]"=2026 \  -d "card[cvc]"=314
```

Example 3 (unknown):
```unknown
{  "id": "tok_1N3T00LkdIwHu7ixt44h1F8k",  "object": "token",  "card": {    "id": "card_1N3T00LkdIwHu7ixRdxpVI1Q",    "object": "card",    "address_city": null,    "address_country": null,    "address_line1": null,    "address_line1_check": null,    "address_line2": null,    "address_state": null,    "address_zip": null,    "address_zip_check": null,    "brand": "Visa",    "country": "US",    "cvc_check": "unchecked",    "dynamic_last4": null,    "exp_month": 5,    "exp_year": 2026,    "fingerprint": "mToisGZ01V71BCos",    "funding": "credit",    "last4": "4242",    "metadata": {},    "name": null,    "tokenization_method": null,    "wallet": null  },  "client_ip": "52.35.78.6",  "created": 1683071568,  "livemode": false,  "type": "card",  "used": false}
```

Example 4 (unknown):
```unknown
{  "id": "tok_1N3T00LkdIwHu7ixt44h1F8k",  "object": "token",  "card": {    "id": "card_1N3T00LkdIwHu7ixRdxpVI1Q",    "object": "card",    "address_city": null,    "address_country": null,    "address_line1": null,    "address_line1_check": null,    "address_line2": null,    "address_state": null,    "address_zip": null,    "address_zip_check": null,    "brand": "Visa",    "country": "US",    "cvc_check": "unchecked",    "dynamic_last4": null,    "exp_month": 5,    "exp_year": 2026,    "fingerprint": "mToisGZ01V71BCos",    "funding": "credit",    "last4": "4242",    "metadata": {},    "name": null,    "tokenization_method": null,    "wallet": null  },  "client_ip": "52.35.78.6",  "created": 1683071568,  "livemode": false,  "type": "card",  "used": false}
```

---

## Application Fee Refunds

**URL:** https://docs.stripe.com/api/fee_refunds

**Contents:**
- Application Fee Refunds
- The Application Fee Refund object
  - Attributes
    - idstring
    - amountinteger
    - currencyenum
    - feestringExpandable
    - metadatanullable object
  - More attributesExpand all
    - objectstring

Application Fee Refund objects allow you to refund an application fee that has previously been created but not yet refunded. Funds will be refunded to the Stripe account from which the fee was originally collected.

Related guide: Refunding application fees

Unique identifier for the object.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

ID of the application fee that was refunded.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Refunds an application fee that has previously been collected but not yet refunded. Funds will be refunded to the Stripe account from which the fee was originally collected.

You can optionally refund only part of an application fee. You can do so multiple times, until the entire fee has been refunded.

Once entirely refunded, an application fee can’t be refunded again. This method will raise an error when called on an already-refunded application fee, or when trying to refund more money than is left on an application fee.

A positive integer, in cents, representing how much of this fee to refund. Can refund only up to the remaining unrefunded amount of the fee.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the Application Fee Refund object if the refund succeeded. Raises an error if the fee has already been refunded, or if an invalid fee identifier was provided.

Updates the specified application fee refund by setting the values of the parameters passed. Any parameters not provided will be left unchanged.

This request only accepts metadata as an argument.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the application fee refund object if the update succeeded. This call will raise an error if update parameters are invalid.

By default, you can see the 10 most recent refunds stored directly on the application fee object, but you can also retrieve details about a specific refund stored on the application fee.

Returns the application fee refund object.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "fr_1MtJRpKbnvuxQXGuM6Ww0D24",  "object": "fee_refund",  "amount": 100,  "balance_transaction": null,  "created": 1680651573,  "currency": "usd",  "fee": "fee_1B73DOKbnvuxQXGuhY8Aw0TN",  "metadata": {}}
```

Example 2 (unknown):
```unknown
{  "id": "fr_1MtJRpKbnvuxQXGuM6Ww0D24",  "object": "fee_refund",  "amount": 100,  "balance_transaction": null,  "created": 1680651573,  "currency": "usd",  "fee": "fee_1B73DOKbnvuxQXGuhY8Aw0TN",  "metadata": {}}
```

Example 3 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/application_fees/fee_1B73DOKbnvuxQXGuhY8Aw0TN/refunds \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/application_fees/fee_1B73DOKbnvuxQXGuhY8Aw0TN/refunds \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

---

## Create a file

**URL:** https://docs.stripe.com/api/files/create

**Contents:**
- Create a file
  - Parameters
    - fileobjectRequired
    - purposeenumRequired
  - More parametersExpand all
    - file_link_dataobject
  - Returns
- Retrieve a file
  - Parameters
  - Returns

To upload a file to Stripe, you need to send a request of type multipart/form-data. Include the file you want to upload in the request, and the parameters for creating a file.

All of Stripe’s officially supported Client libraries support sending multipart/form-data.

A file to upload. Make sure that the specifications follow RFC 2388, which defines file transfers for the multipart/form-data protocol.

The purpose of the uploaded file.

Additional documentation requirements that can be requested for an account.

Additional verification for custom accounts.

Customer signature image.

Evidence to submit with a dispute response.

A document to verify the identity of an account owner during account provisioning.

Additional regulatory reporting requirements for Issuing.

A self-assessment PCI questionnaire.

A copy of the platform’s Terms of Service.

Returns the file object.

Retrieves the details of an existing file object. After you supply a unique file ID, Stripe returns the corresponding file object. Learn how to access file contents.

If the identifier you provide is valid, a file object returns. If not, Stripe raises an error.

Returns a list of the files that your account has access to. Stripe sorts and returns the files by their creation dates, placing the most recently created files at the top.

Filter queries by the file purpose. If you don’t provide a purpose, the queries return unfiltered files.

A dictionary with a data property that contains an array of up to limit files, starting after the starting_after file. Each entry in the array is a separate file object. If there aren’t additional available files, the resulting array is empty.

**Examples:**

Example 1 (unknown):
```unknown
curl https://files.stripe.com/v1/files \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -F purpose=dispute_evidence \  -F file="@/path/to/a/file.jpg"
```

Example 2 (unknown):
```unknown
curl https://files.stripe.com/v1/files \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -F purpose=dispute_evidence \  -F file="@/path/to/a/file.jpg"
```

Example 3 (unknown):
```unknown
{  "id": "file_1Mr4LDLkdIwHu7ixFCz0dZiH",  "object": "file",  "created": 1680116847,  "expires_at": 1703444847,  "filename": "file.png",  "links": {    "object": "list",    "data": [],    "has_more": false,    "url": "/v1/file_links?file=file_1Mr4LDLkdIwHu7ixFCz0dZiH"  },  "purpose": "dispute_evidence",  "size": 8429,  "title": null,  "type": "png",  "url": "https://files.stripe.com/v1/files/file_1Mr4LDLkdIwHu7ixFCz0dZiH/contents"}
```

Example 4 (unknown):
```unknown
{  "id": "file_1Mr4LDLkdIwHu7ixFCz0dZiH",  "object": "file",  "created": 1680116847,  "expires_at": 1703444847,  "filename": "file.png",  "links": {    "object": "list",    "data": [],    "has_more": false,    "url": "/v1/file_links?file=file_1Mr4LDLkdIwHu7ixFCz0dZiH"  },  "purpose": "dispute_evidence",  "size": 8429,  "title": null,  "type": "png",  "url": "https://files.stripe.com/v1/files/file_1Mr4LDLkdIwHu7ixFCz0dZiH/contents"}
```

---

## Terminal API and SDK references

**URL:** https://docs.stripe.com/terminal/references/api

**Contents:**
- Terminal API and SDK references
- Explore the API references for the server-driven integration and Terminal SDKs.

Explore the API reference for the Terminal server-driven integration

Explore the API reference for the Terminal JavaScript SDK v1

Explore the API reference for the Terminal iOS SDK

Explore the API reference for the Terminal Android SDK

Explore the API reference for the Terminal React Native SDK

---

## The PaymentMethod object

**URL:** https://docs.stripe.com/api/payment_methods/object

**Contents:**
- The PaymentMethod object
  - Attributes
    - idstring
    - billing_detailsobject
    - customernullable stringExpandable
    - metadatanullable object
    - typeenum
  - More attributesExpand all
    - objectstring
    - acss_debitnullable object

Unique identifier for the object.

Billing information associated with the PaymentMethod that may be used or required by particular types of payment methods.

The ID of the Customer to which this PaymentMethod is saved. This will not be set when the PaymentMethod has not been saved to a Customer.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The type of the PaymentMethod. An additional hash is included on the PaymentMethod with a name matching this value. It contains additional information specific to the PaymentMethod type.

Pre-authorized debit payments are used to debit Canadian bank accounts through the Automated Clearing Settlement System (ACSS).

Affirm is a buy now, pay later payment method in the US.

Afterpay / Clearpay is a buy now, pay later payment method used in Australia, Canada, France, New Zealand, Spain, the UK, and the US.

Alipay is a digital wallet payment method used in China.

Alma is a Buy Now, Pay Later payment method that lets customers pay in 2, 3, or 4 installments.

Amazon Pay is a Wallet payment method that lets hundreds of millions of Amazon customers pay their way, every day.

BECS Direct Debit is used to debit Australian bank accounts through the Bulk Electronic Clearing System (BECS).

Bacs Direct Debit is used to debit UK bank accounts.

Bancontact is a bank redirect payment method used in Belgium.

Billie is a payment method.

Creates a PaymentMethod object. Read the Stripe.js reference to learn how to create PaymentMethods via Stripe.js.

Instead of creating a PaymentMethod directly, we recommend using the PaymentIntents API to accept a payment immediately or the SetupIntent API to collect payment method details ahead of a future payment.

The type of the PaymentMethod. An additional hash is included on the PaymentMethod with a name matching this value. It contains additional information specific to the PaymentMethod type.

Pre-authorized debit payments are used to debit Canadian bank accounts through the Automated Clearing Settlement System (ACSS).

Affirm is a buy now, pay later payment method in the US.

Afterpay / Clearpay is a buy now, pay later payment method used in Australia, Canada, France, New Zealand, Spain, the UK, and the US.

Alipay is a digital wallet payment method used in China.

Alma is a Buy Now, Pay Later payment method that lets customers pay in 2, 3, or 4 installments.

Amazon Pay is a Wallet payment method that lets hundreds of millions of Amazon customers pay their way, every day.

BECS Direct Debit is used to debit Australian bank accounts through the Bulk Electronic Clearing System (BECS).

Bacs Direct Debit is used to debit UK bank accounts.

Bancontact is a bank redirect payment method used in Belgium.

Billie is a payment method.

Billing information associated with the PaymentMethod that may be used or required by particular types of payment methods.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a PaymentMethod object.

Updates a PaymentMethod object. A PaymentMethod must be attached to a customer to be updated.

Billing information associated with the PaymentMethod that may be used or required by particular types of payment methods.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a PaymentMethod object.

Retrieves a PaymentMethod object for a given Customer.

Returns a PaymentMethod object.

Retrieves a PaymentMethod object attached to the StripeAccount. To retrieve a payment method attached to a Customer, you should use Retrieve a Customer’s PaymentMethods

Returns a PaymentMethod object.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "pm_1Q0PsIJvEtkwdCNYMSaVuRz6",  "object": "payment_method",  "allow_redisplay": "unspecified",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": "John Doe",    "phone": null  },  "created": 1726673582,  "customer": null,  "livemode": false,  "metadata": {},  "type": "us_bank_account",  "us_bank_account": {    "account_holder_type": "individual",    "account_type": "checking",    "bank_name": "STRIPE TEST BANK",    "financial_connections_account": null,    "fingerprint": "LstWJFsCK7P349Bg",    "last4": "6789",    "networks": {      "preferred": "ach",      "supported": [        "ach"      ]    },    "routing_number": "110000000",    "status_details": {}  }}
```

Example 2 (unknown):
```unknown
{  "id": "pm_1Q0PsIJvEtkwdCNYMSaVuRz6",  "object": "payment_method",  "allow_redisplay": "unspecified",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": "John Doe",    "phone": null  },  "created": 1726673582,  "customer": null,  "livemode": false,  "metadata": {},  "type": "us_bank_account",  "us_bank_account": {    "account_holder_type": "individual",    "account_type": "checking",    "bank_name": "STRIPE TEST BANK",    "financial_connections_account": null,    "fingerprint": "LstWJFsCK7P349Bg",    "last4": "6789",    "networks": {      "preferred": "ach",      "supported": [        "ach"      ]    },    "routing_number": "110000000",    "status_details": {}  }}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_methods \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d type=us_bank_account \  -d "us_bank_account[account_holder_type]"=individual \  -d "us_bank_account[account_number]"=000123456789 \  -d "us_bank_account[routing_number]"=110000000 \  -d "billing_details[name]"="John Doe"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_methods \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d type=us_bank_account \  -d "us_bank_account[account_holder_type]"=individual \  -d "us_bank_account[account_number]"=000123456789 \  -d "us_bank_account[routing_number]"=110000000 \  -d "billing_details[name]"="John Doe"
```

---

## Discounts

**URL:** https://docs.stripe.com/api/discounts

**Contents:**
- Discounts
- The Discount object
  - Attributes
    - idstring
    - customernullable stringExpandable
    - customer_accountnullable string
    - endnullable timestamp
    - sourceobject
    - starttimestamp
    - subscriptionnullable string

A discount represents the actual application of a coupon or promotion code. It contains information about when the discount began, when it will end, and what it is applied to.

Related guide: Applying discounts to subscriptions

The ID of the discount object. Discounts cannot be fetched by ID. Use expand[]=discounts in API calls to expand discount IDs in an array.

The ID of the customer associated with this discount.

The ID of the account representing the customer associated with this discount.

If the coupon has a duration of repeating, the date that this discount will end. If the coupon has a duration of once or forever, this attribute will be null.

The source of the discount.

Date that the coupon was applied.

The subscription that this coupon is applied to, if it is applied to a particular subscription.

Removes the currently applied discount on a customer.

An object with a deleted flag set to true upon success. This call returns an error otherwise, such as if no discount exists on this customer.

Removes the currently applied discount on a subscription.

An object with a deleted flag set to true upon success. This call returns an error otherwise, such as if no discount exists on this subscription.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "di_1M6vk22eZvKYlo2CYMGIhk14",  "object": "discount",  "checkout_session": "cs_test_b1mywbZHtQCQW2ncaItVPFqupwmfqNU4IMMdw3lArEBGt0QD0CZDrNQswR",  "source": {    "type": "coupon",    "coupon": "nVJYDOag"  },  "customer": "cus_9s6XKzkNRiz8i3",  "end": null,  "invoice": null,  "invoice_item": null,  "promotion_code": null,  "start": 1669120702,  "subscription": null}
```

Example 2 (unknown):
```unknown
{  "id": "di_1M6vk22eZvKYlo2CYMGIhk14",  "object": "discount",  "checkout_session": "cs_test_b1mywbZHtQCQW2ncaItVPFqupwmfqNU4IMMdw3lArEBGt0QD0CZDrNQswR",  "source": {    "type": "coupon",    "coupon": "nVJYDOag"  },  "customer": "cus_9s6XKzkNRiz8i3",  "end": null,  "invoice": null,  "invoice_item": null,  "promotion_code": null,  "start": 1669120702,  "subscription": null}
```

Example 3 (unknown):
```unknown
curl -X DELETE https://api.stripe.com/v1/customers/cus_9s6XKzkNRiz8i3/discount \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl -X DELETE https://api.stripe.com/v1/customers/cus_9s6XKzkNRiz8i3/discount \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

---

## Expanding Responses

**URL:** https://docs.stripe.com/api/expanding_objects

**Contents:**
- Expanding Responses
- Idempotent requests
- Include-dependent response values (API v2)
- Metadata
- Sample metadata use cases
- Pagination
  - Parameters
    - limitoptional, default is 10
    - starting_afteroptional object ID
    - ending_beforeoptional object ID

Many objects allow you to request additional information as an expanded response by using the expand request parameter. This parameter is available on all API requests, and applies to the response of that request only. You can expand responses in two ways.

In many cases, an object contains the ID of a related object in its response properties. For example, a Charge might have an associated Customer ID. You can expand these objects in line with the expand request parameter. The expandable label in this documentation indicates ID fields that you can expand into objects.

Some available fields aren’t included in the responses by default, such as the number and cvc fields for the Issuing Card object. You can request these fields as an expanded response by using the expand request parameter.

You can expand recursively by specifying nested fields after a dot (.). For example, requesting payment_intent.customer on a charge expands the payment_intent property into a full PaymentIntent object, then expands the customer property on that payment intent into a full Customer object.

You can use the expand parameter on any endpoint that returns expandable fields, including list, create, and update endpoints.

Expansions on list requests start with the data property. For example, you can expand data.customers on a request to list charges and associated customers. Performing deep expansions on numerous list requests might result in slower processing times.

Expansions have a maximum depth of four levels (for example, the deepest expansion allowed when listing charges is data.payment_intent.customer.default_source).

You can expand multiple objects at the same time by identifying multiple items in the expand array.

The API supports idempotency for safely retrying requests without accidentally performing the same operation twice. When creating or updating an object, use an idempotency key. Then, if a connection error occurs, you can safely repeat the request without risk of creating a second object or performing the update twice.

To perform an idempotent request, provide an additional IdempotencyKey element to the request options.

Stripe’s idempotency works by saving the resulting status code and body of the first request made for any given idempotency key, regardless of whether it succeeds or fails. Subsequent requests with the same key return the same result, including 500 errors.

A client generates an idempotency key, which is a unique key that the server uses to recognize subsequent retries of the same request. How you create unique keys is up to you, but we suggest using V4 UUIDs, or another random string with enough entropy to avoid collisions. Idempotency keys are up to 255 characters long.

You can remove keys from the system automatically after they’re at least 24 hours old. We generate a new request if a key is reused after the original is pruned. The idempotency layer compares incoming parameters to those of the original request and errors if they’re not the same to prevent accidental misuse.

We save results only after the execution of an endpoint begins. If incoming parameters fail validation, or the request conflicts with another request that’s executing concurrently, we don’t save the idempotent result because no API endpoint initiates the execution. You can retry these requests. Learn more about when you can retry idempotent requests.

All POST requests accept idempotency keys. Don’t send idempotency keys in GET and DELETE requests because it has no effect. These requests are idempotent by definition.

Some API v2 responses contain null values for certain properties by default, regardless of their actual values. That reduces the size of response payloads while maintaining the basic response structure. To retrieve the actual values for those properties, specify them in the include array request parameter.

To determine whether you need to use the include parameter in a given request, look at the request description. The include parameter’s enum values represent the response properties that depend on the include parameter.

Whether a response property defaults to null depends on the request endpoint, not the object that the endpoint references. If multiple endpoints return data from the same object, a particular property can depend on include in one endpoint and return its actual value by default for a different endpoint.

A hash property can depend on a single include value, or on multiple include values associated with its child properties. For example, when updating an Account, to return actual values for the entire identity hash, specify identity in the include parameter. Otherwise, the identity hash is null in the response. However, to return actual values for the configuration hash, you must specify individual configurations in the request. If you specify at least one configuration, but not all of them, specified configurations return actual values and unspecified configurations return null. If you don’t specify any configurations, the configuration hash is null in the response.

The response includes actual values for the properties specified in the include parameter, and null for all other include-dependent properties.

Updateable Stripe objects—including Account, Charge, Customer, PaymentIntent, Refund, Subscription, and Transfer have a metadata parameter. You can use this parameter to attach key-value data to these Stripe objects.

You can specify up to 50 keys, with key names up to 40 characters long and values up to 500 characters long. Keys and values are stored as strings and can contain any characters with one exception: you can’t use square brackets ([ and ]) in keys.

You can use metadata to store additional, structured information on an object. For example, you could store your user’s full name and corresponding unique identifier from your system on a Stripe Customer object. Stripe doesn’t use metadata—for example, we don’t use it to authorize or decline a charge and it won’t be seen by your users unless you choose to show it to them.

Some of the objects listed above also support a description parameter. You can use the description parameter to annotate a charge-for example, a human-readable description such as 2 shirts for test@example.com. Unlike metadata, description is a single string, which your users might see (for example, in email receipts Stripe sends on your behalf).

Don’t store any sensitive information (bank account numbers, card details, and so on) as metadata or in the description parameter.

All top-level API resources have support for bulk fetches through “list” API methods. For example, you can list charges, list customers, and list invoices. These list API methods share a common structure and accept, at a minimum, the following three parameters: limit, starting_after, and ending_before.

Stripe’s list API methods use cursor-based pagination through the starting_after and ending_before parameters. Both parameters accept an existing object ID value (see below) and return objects in reverse chronological order. The ending_before parameter returns objects listed before the named object. The starting_after parameter returns objects listed after the named object. These parameters are mutually exclusive. You can use either the starting_after or ending_before parameter, but not both simultaneously.

Our client libraries offer auto-pagination helpers to traverse all pages of a list.

This specifies a limit on the number of objects to return, ranging between 1 and 100.

A cursor to use in pagination. starting_after is an object ID that defines your place in the list. For example, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include starting_after=obj_foo to fetch the next page of the list.

A cursor to use in pagination. ending_before is an object ID that defines your place in the list. For example, if you make a list request and receive 100 objects, starting with obj_bar, your subsequent call can include ending_before=obj_bar to fetch the previous page of the list.

A string that provides a description of the object type that returns.

An array containing the actual response elements, paginated by any request parameters.

Whether or not there are more elements available after this set. If false, this set comprises the end of the list.

The URL for accessing this list.

APIs within the /v2 namespace contain a different pagination interface than the v1 namespace.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/charges/ch_3LmzzQ2eZvKYlo2C0XjzUzJV \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -d "expand[]"=customer \  -d "expand[]"="payment_intent.customer" \  -G
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/charges/ch_3LmzzQ2eZvKYlo2C0XjzUzJV \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -d "expand[]"=customer \  -d "expand[]"="payment_intent.customer" \  -G
```

Example 3 (unknown):
```unknown
{  "id": "ch_3LmzzQ2eZvKYlo2C0XjzUzJV",  "object": "charge",  "customer": {    "id": "cu_14HOpH2eZvKYlo2CxXIM7Pb2",    "object": "customer",    // ...  },  "payment_intent": {    "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",    "object": "payment_intent",    "customer": {      "id": "cus_NffrFeUfNV2Hib",      "object": "customer",      // ...    },    // ...  },  // ...}
```

Example 4 (unknown):
```unknown
{  "id": "ch_3LmzzQ2eZvKYlo2C0XjzUzJV",  "object": "charge",  "customer": {    "id": "cu_14HOpH2eZvKYlo2CxXIM7Pb2",    "object": "customer",    // ...  },  "payment_intent": {    "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",    "object": "payment_intent",    "customer": {      "id": "cus_NffrFeUfNV2Hib",      "object": "customer",      // ...    },    // ...  },  // ...}
```

---

## Retrieve balance

**URL:** https://docs.stripe.com/api/balance/balance_retrieve

**Contents:**
- Retrieve balance
  - Parameters
  - Returns

Retrieves the current account balance, based on the authentication that was used to make the request. For a sample request, see Accounting for negative balances.

Returns a balance object for the account that was authenticated in the request.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/balance \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/balance \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "object": "balance",  "available": [    {      "amount": 666670,      "currency": "usd",      "source_types": {        "card": 666670      }    }  ],  "connect_reserved": [    {      "amount": 0,      "currency": "usd"    }  ],  "livemode": false,  "pending": [    {      "amount": 61414,      "currency": "usd",      "source_types": {        "card": 61414      }    }  ]}
```

Example 4 (unknown):
```unknown
{  "object": "balance",  "available": [    {      "amount": 666670,      "currency": "usd",      "source_types": {        "card": 666670      }    }  ],  "connect_reserved": [    {      "amount": 0,      "currency": "usd"    }  ],  "livemode": false,  "pending": [    {      "amount": 61414,      "currency": "usd",      "source_types": {        "card": 61414      }    }  ]}
```

---

## Promotion Code

**URL:** https://docs.stripe.com/api/promotion_codes

**Contents:**
- Promotion Code
- The Promotion Code object
  - Attributes
    - idstring
    - codestring
    - metadatanullable object
    - promotionobject
  - More attributesExpand all
    - objectstring
    - activeboolean

A Promotion Code represents a customer-redeemable code for an underlying promotion. You can create multiple codes for a single promotion.

If you enable promotion codes in your customer portal configuration, then customers can redeem a code themselves when updating a subscription in the portal. Customers can also view the currently active promotion codes and coupons on each of their subscriptions in the portal.

Unique identifier for the object.

The customer-facing code. Regardless of case, this code must be unique across all active promotion codes for each customer. Valid characters are lower case letters (a-z), upper case letters (A-Z), and digits (0-9).

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The promotion referenced by this promotion code.

A promotion code points to an underlying promotion. You can optionally restrict the code to a specific customer, redemption limit, and expiration date.

The promotion referenced by this promotion code.

The customer-facing code. Regardless of case, this code must be unique across all active promotion codes for a specific customer. Valid characters are lower case letters (a-z), upper case letters (A-Z), and digits (0-9).

If left blank, we will generate one automatically.

The maximum length is 500 characters.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the promotion code object.

Updates the specified promotion code by setting the values of the parameters passed. Most fields are, by design, not editable.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The updated promotion code object is returned upon success. Otherwise, this call raises an error.

Retrieves the promotion code with the given ID. In order to retrieve a promotion code by the customer-facing code use list with the desired code.

Returns a promotion code if a valid promotion code ID was provided. Raises an error otherwise.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "promo_1MiM6KLkdIwHu7ixrIaX4wgn",  "object": "promotion_code",  "active": true,  "code": "A1H1Q1MG",  "promotion": {    "type": "coupon",    "coupon": "nVJYDOag"  },  "created": 1678040164,  "customer": null,  "expires_at": null,  "livemode": false,  "max_redemptions": null,  "metadata": {},  "restrictions": {    "first_time_transaction": false,    "minimum_amount": null,    "minimum_amount_currency": null  },  "times_redeemed": 0}
```

Example 2 (unknown):
```unknown
{  "id": "promo_1MiM6KLkdIwHu7ixrIaX4wgn",  "object": "promotion_code",  "active": true,  "code": "A1H1Q1MG",  "promotion": {    "type": "coupon",    "coupon": "nVJYDOag"  },  "created": 1678040164,  "customer": null,  "expires_at": null,  "livemode": false,  "max_redemptions": null,  "metadata": {},  "restrictions": {    "first_time_transaction": false,    "minimum_amount": null,    "minimum_amount_currency": null  },  "times_redeemed": 0}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/promotion_codes \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "promotion[type]"=coupon \  -d "promotion[coupon]"=nVJYDOag
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/promotion_codes \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "promotion[type]"=coupon \  -d "promotion[coupon]"=nVJYDOag
```

---

## Disable an event destination v2

**URL:** https://docs.stripe.com/api/v2/core/event_destinations/disable

**Contents:**
- Disable an event destination v2
  - Parameters
    - idstringRequired
  - Returns
  - Response attributes
    - idstring
    - objectstring, value is "v2.core.event_destination"
    - amazon_eventbridgenullable object
    - createdtimestamp
    - descriptionstring

Disable an event destination.

Identifier for the event destination to disable.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value of the object field.

Amazon EventBridge configuration.

Time at which the object was created.

An optional description of what the event destination is used for.

The list of events to enable for this endpoint.

Payload type of events being subscribed to.

Where events should be routed from.

Receive events from accounts connected to the account that owns the event destination.

Receive events from the account that owns the event destination.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Event destination name.

If using the snapshot event payload, the API version events are rendered as.

Status. It can be set to either enabled or disabled.

Event destination is disabled.

Event destination is enabled.

Additional information about event destination status.

Event destination type.

Time at which the object was last updated.

Webhook endpoint configuration.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

Enable an event destination.

Identifier for the event destination to enable.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value of the object field.

Amazon EventBridge configuration.

Time at which the object was created.

An optional description of what the event destination is used for.

The list of events to enable for this endpoint.

Payload type of events being subscribed to.

Where events should be routed from.

Receive events from accounts connected to the account that owns the event destination.

Receive events from the account that owns the event destination.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Event destination name.

If using the snapshot event payload, the API version events are rendered as.

Status. It can be set to either enabled or disabled.

Event destination is disabled.

Event destination is enabled.

Additional information about event destination status.

Event destination type.

Time at which the object was last updated.

Webhook endpoint configuration.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

This is a list of all public thin events we currently send for updates to EventDestination, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/event_destinations/ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6/disable \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/event_destinations/ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6/disable \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 3 (unknown):
```unknown
{  "id": "ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6",  "object": "v2.core.event_destination",  "created": "2024-10-22T16:20:09.931Z",  "description": "This is my event destination, I like it a lot",  "enabled_events": [    "v1.billing.meter.error_report_triggered"  ],  "event_payload": "thin",  "events_from": [    "self"  ],  "livemode": false,  "metadata": {},  "name": "My Event Destination",  "snapshot_api_version": null,  "status": "disabled",  "status_details": {    "disabled": {      "reason": "user"    }  },  "type": "webhook_endpoint",  "updated": "2024-10-22T16:21:38.634Z",  "webhook_endpoint": {    "signing_secret": null,    "url": null  }}
```

Example 4 (unknown):
```unknown
{  "id": "ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6",  "object": "v2.core.event_destination",  "created": "2024-10-22T16:20:09.931Z",  "description": "This is my event destination, I like it a lot",  "enabled_events": [    "v1.billing.meter.error_report_triggered"  ],  "event_payload": "thin",  "events_from": [    "self"  ],  "livemode": false,  "metadata": {},  "name": "My Event Destination",  "snapshot_api_version": null,  "status": "disabled",  "status_details": {    "disabled": {      "reason": "user"    }  },  "type": "webhook_endpoint",  "updated": "2024-10-22T16:21:38.634Z",  "webhook_endpoint": {    "signing_secret": null,    "url": null  }}
```

---

## Errors

**URL:** https://docs.stripe.com/api/errors

**Contents:**
- Errors
  - Attributes
    - codenullable string
    - decline_codenullable string
    - messagenullable string
    - paramnullable string
    - payment_intentnullable object
    - typeenum
  - MoreExpand all
    - advice_codenullable string

Stripe uses conventional HTTP response codes to indicate the success or failure of an API request. In general: Codes in the 2xx range indicate success. Codes in the 4xx range indicate an error that failed given the information provided (e.g., a required parameter was omitted, a charge failed, etc.). Codes in the 5xx range indicate an error with Stripe’s servers (these are rare).

Some 4xx errors that could be handled programmatically (e.g., a card is declined) include an error code that briefly explains the error reported.

For some errors that could be handled programmatically, a short string indicating the error code reported.

For card errors resulting from a card issuer decline, a short string indicating the card issuer’s reason for the decline if they provide one.

A human-readable message providing more details about the error. For card errors, these messages can be shown to your users.

If the error is parameter-specific, the parameter related to the error. For example, you can use this to display a message near the correct form field.

The PaymentIntent object for errors returned on a request involving a PaymentIntent.

The type of error returned. One of api_error, card_error, idempotency_error, or invalid_request_error

Our Client libraries raise exceptions for many reasons, such as a failed charge, invalid parameters, authentication errors, and network unavailability. We recommend writing code that gracefully handles all possible API exceptions.

Many objects allow you to request additional information as an expanded response by using the expand request parameter. This parameter is available on all API requests, and applies to the response of that request only. You can expand responses in two ways.

In many cases, an object contains the ID of a related object in its response properties. For example, a Charge might have an associated Customer ID. You can expand these objects in line with the expand request parameter. The expandable label in this documentation indicates ID fields that you can expand into objects.

Some available fields aren’t included in the responses by default, such as the number and cvc fields for the Issuing Card object. You can request these fields as an expanded response by using the expand request parameter.

You can expand recursively by specifying nested fields after a dot (.). For example, requesting payment_intent.customer on a charge expands the payment_intent property into a full PaymentIntent object, then expands the customer property on that payment intent into a full Customer object.

You can use the expand parameter on any endpoint that returns expandable fields, including list, create, and update endpoints.

Expansions on list requests start with the data property. For example, you can expand data.customers on a request to list charges and associated customers. Performing deep expansions on numerous list requests might result in slower processing times.

Expansions have a maximum depth of four levels (for example, the deepest expansion allowed when listing charges is data.payment_intent.customer.default_source).

You can expand multiple objects at the same time by identifying multiple items in the expand array.

The API supports idempotency for safely retrying requests without accidentally performing the same operation twice. When creating or updating an object, use an idempotency key. Then, if a connection error occurs, you can safely repeat the request without risk of creating a second object or performing the update twice.

To perform an idempotent request, provide an additional IdempotencyKey element to the request options.

Stripe’s idempotency works by saving the resulting status code and body of the first request made for any given idempotency key, regardless of whether it succeeds or fails. Subsequent requests with the same key return the same result, including 500 errors.

A client generates an idempotency key, which is a unique key that the server uses to recognize subsequent retries of the same request. How you create unique keys is up to you, but we suggest using V4 UUIDs, or another random string with enough entropy to avoid collisions. Idempotency keys are up to 255 characters long.

You can remove keys from the system automatically after they’re at least 24 hours old. We generate a new request if a key is reused after the original is pruned. The idempotency layer compares incoming parameters to those of the original request and errors if they’re not the same to prevent accidental misuse.

We save results only after the execution of an endpoint begins. If incoming parameters fail validation, or the request conflicts with another request that’s executing concurrently, we don’t save the idempotent result because no API endpoint initiates the execution. You can retry these requests. Learn more about when you can retry idempotent requests.

All POST requests accept idempotency keys. Don’t send idempotency keys in GET and DELETE requests because it has no effect. These requests are idempotent by definition.

Some API v2 responses contain null values for certain properties by default, regardless of their actual values. That reduces the size of response payloads while maintaining the basic response structure. To retrieve the actual values for those properties, specify them in the include array request parameter.

To determine whether you need to use the include parameter in a given request, look at the request description. The include parameter’s enum values represent the response properties that depend on the include parameter.

Whether a response property defaults to null depends on the request endpoint, not the object that the endpoint references. If multiple endpoints return data from the same object, a particular property can depend on include in one endpoint and return its actual value by default for a different endpoint.

A hash property can depend on a single include value, or on multiple include values associated with its child properties. For example, when updating an Account, to return actual values for the entire identity hash, specify identity in the include parameter. Otherwise, the identity hash is null in the response. However, to return actual values for the configuration hash, you must specify individual configurations in the request. If you specify at least one configuration, but not all of them, specified configurations return actual values and unspecified configurations return null. If you don’t specify any configurations, the configuration hash is null in the response.

The response includes actual values for the properties specified in the include parameter, and null for all other include-dependent properties.

**Examples:**

Example 1 (unknown):
```unknown
# Select a client library to see examples of# handling different kinds of errors.
```

Example 2 (unknown):
```unknown
# Select a client library to see examples of# handling different kinds of errors.
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/charges/ch_3LmzzQ2eZvKYlo2C0XjzUzJV \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -d "expand[]"=customer \  -d "expand[]"="payment_intent.customer" \  -G
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/charges/ch_3LmzzQ2eZvKYlo2C0XjzUzJV \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -d "expand[]"=customer \  -d "expand[]"="payment_intent.customer" \  -G
```

---

## Payouts

**URL:** https://docs.stripe.com/api/payouts

**Contents:**
- Payouts
- The Payout object
  - Attributes
    - idstring
    - amountinteger
    - arrival_datetimestamp
    - currencyenum
    - descriptionnullable string
    - metadatanullable object
    - statement_descriptornullable string

A Payout object is created when you receive funds from Stripe, or when you initiate a payout to either a bank account or debit card of a connected Stripe account. You can retrieve individual payouts, and list all payouts. Payouts are made on varying schedules, depending on your country and industry.

Related guide: Receiving payouts

Unique identifier for the object.

The amount (in cents) that transfers to your bank account or debit card.

Date that you can expect the payout to arrive in the bank. This factors in delays to account for weekends or bank holidays.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Extra information about a payout that displays on the user’s bank statement.

Current status of the payout: paid, pending, in_transit, canceled or failed. A payout is pending until it’s submitted to the bank, when it becomes in_transit. The status changes to paid if the transaction succeeds, or to failed or canceled (within 5 business days). Some payouts that fail might initially show as paid, then change to failed.

To send funds to your own bank account, create a new payout object. Your Stripe balance must cover the payout amount. If it doesn’t, you receive an “Insufficient Funds” error.

If your API key is in test mode, money won’t actually be sent, though every other action occurs as if you’re in live mode.

If you create a manual payout on a Stripe account that uses multiple payment source types, you need to specify the source type balance that the payout draws from. The balance object details available and pending amounts by source type.

A positive integer in cents representing how much to payout.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

A string that displays on the recipient’s bank or card statement (up to 22 characters). A statement_descriptor that’s longer than 22 characters return an error. Most banks truncate this information and display it inconsistently. Some banks might not display it at all.

Returns a payout object if no initial errors are present during the payout creation (invalid routing number, insufficient funds, and so on). We initially mark the status of the payout object as pending.

Updates the specified payout by setting the values of the parameters you pass. We don’t change parameters that you don’t provide. This request only accepts the metadata as arguments.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the payout object if the update succeeds. This call raises an error if update parameters are invalid.

Retrieves the details of an existing payout. Supply the unique payout ID from either a payout creation request or the payout list. Stripe returns the corresponding payout information.

Returns a payout object if a you provide a valid identifier. raises An error occurs otherwise.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "po_1OaFDbEcg9tTZuTgNYmX0PKB",  "object": "payout",  "amount": 1100,  "arrival_date": 1680652800,  "automatic": false,  "balance_transaction": "txn_1OaFDcEcg9tTZuTgYMR25tSe",  "created": 1680648691,  "currency": "usd",  "description": null,  "destination": "ba_1MtIhL2eZvKYlo2CAElKwKu2",  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "livemode": false,  "metadata": {},  "method": "standard",  "original_payout": null,  "reconciliation_status": "not_applicable",  "reversed_by": null,  "source_type": "card",  "statement_descriptor": null,  "status": "pending",  "type": "bank_account"}
```

Example 2 (unknown):
```unknown
{  "id": "po_1OaFDbEcg9tTZuTgNYmX0PKB",  "object": "payout",  "amount": 1100,  "arrival_date": 1680652800,  "automatic": false,  "balance_transaction": "txn_1OaFDcEcg9tTZuTgYMR25tSe",  "created": 1680648691,  "currency": "usd",  "description": null,  "destination": "ba_1MtIhL2eZvKYlo2CAElKwKu2",  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "livemode": false,  "metadata": {},  "method": "standard",  "original_payout": null,  "reconciliation_status": "not_applicable",  "reversed_by": null,  "source_type": "card",  "statement_descriptor": null,  "status": "pending",  "type": "bank_account"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/payouts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=1100 \  -d currency=usd
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/payouts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=1100 \  -d currency=usd
```

---

## Person event types v2

**URL:** https://docs.stripe.com/api/v2/core/persons/event-types

**Contents:**
- Person event types v2
- Event types
  - v2.core.account_person.created
  - v2.core.account_person.deleted
  - v2.core.account_person.updated

This is a list of all public thin events we currently send for updates to Person, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

---

## Retrieve a customer

**URL:** https://docs.stripe.com/api/customers/retrieve

**Contents:**
- Retrieve a customer
  - Parameters
  - Returns
- List all customers
  - Parameters
    - emailstring
  - More parametersExpand all
    - createdobject
    - ending_beforestring
    - limitinteger

Retrieves a Customer object.

Returns the Customer object for a valid identifier. If it’s for a deleted Customer, a subset of the customer’s information is returned, including a deleted property that’s set to true.

Returns a list of your customers. The customers are returned sorted by creation date, with the most recent customers appearing first.

A case-sensitive filter on the list based on the customer’s email field. The value must be a string.

The maximum length is 512 characters.

A dictionary with a data property that contains an array of up to limit customers, starting after customer starting_after. Passing an optional email will result in filtering to customers with only that exact email address. Each entry in the array is a separate customer object. If no more customers are available, the resulting array will be empty.

Permanently deletes a customer. It cannot be undone. Also immediately cancels any active subscriptions on the customer.

Returns an object with a deleted parameter on success. If the customer ID does not exist, this call raises an error.

Unlike other objects, deleted customers can still be retrieved through the API in order to be able to track their history. Deleting customers removes all credit card details and prevents any further operations to be performed (such as adding a new subscription).

Search for customers you’ve previously created using Stripe’s Search Query Language. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.

The search query string. See search query language and the list of supported query fields for customers.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A dictionary with a data property that contains an array of up to limit customers. If no objects match the query, the resulting array will be empty. See the related guide on expanding properties in lists.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/customers/cus_NffrFeUfNV2Hib \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/customers/cus_NffrFeUfNV2Hib \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "cus_NffrFeUfNV2Hib",  "object": "customer",  "address": null,  "balance": 0,  "created": 1680893993,  "currency": null,  "default_source": null,  "delinquent": false,  "description": null,  "email": "jennyrosen@example.com",  "invoice_prefix": "0759376C",  "invoice_settings": {    "custom_fields": null,    "default_payment_method": null,    "footer": null,    "rendering_options": null  },  "livemode": false,  "metadata": {},  "name": "Jenny Rosen",  "next_invoice_sequence": 1,  "phone": null,  "preferred_locales": [],  "shipping": null,  "tax_exempt": "none",  "test_clock": null}
```

Example 4 (unknown):
```unknown
{  "id": "cus_NffrFeUfNV2Hib",  "object": "customer",  "address": null,  "balance": 0,  "created": 1680893993,  "currency": null,  "default_source": null,  "delinquent": false,  "description": null,  "email": "jennyrosen@example.com",  "invoice_prefix": "0759376C",  "invoice_settings": {    "custom_fields": null,    "default_payment_method": null,    "footer": null,    "rendering_options": null  },  "livemode": false,  "metadata": {},  "name": "Jenny Rosen",  "next_invoice_sequence": 1,  "phone": null,  "preferred_locales": [],  "shipping": null,  "tax_exempt": "none",  "test_clock": null}
```

---

## Balance Transactions

**URL:** https://docs.stripe.com/api/balance_transactions

**Contents:**
- Balance Transactions
- The Balance Transaction object
  - Attributes
    - idstring
    - amountinteger
    - currencyenum
    - descriptionnullable string
    - feeinteger
    - fee_detailsarray of objects
    - netinteger

Balance transactions represent funds moving through your Stripe account. Stripe creates them for every type of transaction that enters or leaves your Stripe account balance.

Related guide: Balance transaction types

Unique identifier for the object.

Gross amount of this transaction (in cents). A positive value represents funds charged to another party, and a negative value represents funds sent to another party.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

An arbitrary string attached to the object. Often useful for displaying to users.

Fees (in cents) paid for this transaction. Represented as a positive integer when assessed.

Detailed breakdown of fees (in cents) paid for this transaction.

Net impact to a Stripe balance (in cents). A positive value represents incrementing a Stripe balance, and a negative value decrementing a Stripe balance. You can calculate the net impact of a transaction on a balance by amount - fee

This transaction relates to the Stripe object.

The transaction’s net funds status in the Stripe balance, which are either available or pending.

Transaction type: adjustment, advance, advance_funding, anticipation_repayment, application_fee, application_fee_refund, charge, climate_order_purchase, climate_order_refund, connect_collection_transfer, contribution, issuing_authorization_hold, issuing_authorization_release, issuing_dispute, issuing_transaction, obligation_outbound, obligation_reversal_inbound, payment, payment_failure_refund, payment_network_reserve_hold, payment_network_reserve_release, payment_refund, payment_reversal, payment_unreconciled, payout, payout_cancel, payout_failure, payout_minimum_balance_hold, payout_minimum_balance_release, refund, refund_failure, reserve_transaction, reserved_funds, stripe_fee, stripe_fx_fee, stripe_balance_payment_debit, stripe_balance_payment_debit_reversal, tax_fee, topup, topup_reversal, transfer, transfer_cancel, transfer_failure, or transfer_refund. Learn more about balance transaction types and what they represent. To classify transactions for accounting purposes, consider reporting_category instead.

Retrieves the balance transaction with the given ID.

Note that this endpoint previously used the path /v1/balance/history/:id.

Returns a balance transaction if a valid balance transaction ID was provided. Raises an error otherwise.

Returns a list of transactions that have contributed to the Stripe account balance (e.g., charges, transfers, and so forth). The transactions are returned in sorted order, with the most recent transactions appearing first.

Note that this endpoint was previously called “Balance history” and used the path /v1/balance/history.

For automatic Stripe payouts only, only returns transactions that were paid out on the specified payout ID.

Only returns transactions of the given type. One of: adjustment, advance, advance_funding, anticipation_repayment, application_fee, application_fee_refund, charge, climate_order_purchase, climate_order_refund, connect_collection_transfer, contribution, issuing_authorization_hold, issuing_authorization_release, issuing_dispute, issuing_transaction, obligation_outbound, obligation_reversal_inbound, payment, payment_failure_refund, payment_network_reserve_hold, payment_network_reserve_release, payment_refund, payment_reversal, payment_unreconciled, payout, payout_cancel, payout_failure, payout_minimum_balance_hold, payout_minimum_balance_release, refund, refund_failure, reserve_transaction, reserved_funds, stripe_fee, stripe_fx_fee, stripe_balance_payment_debit, stripe_balance_payment_debit_reversal, tax_fee, topup, topup_reversal, transfer, transfer_cancel, transfer_failure, or transfer_refund.

A dictionary with a data property that contains an array of up to limit transactions, starting after transaction starting_after. Each entry in the array is a separate transaction history object. If no more transactions are available, the resulting array will be empty.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "txn_1MiN3gLkdIwHu7ixxapQrznl",  "object": "balance_transaction",  "amount": -400,  "available_on": 1678043844,  "created": 1678043844,  "currency": "usd",  "description": null,  "exchange_rate": null,  "fee": 0,  "fee_details": [],  "net": -400,  "reporting_category": "transfer",  "source": "tr_1MiN3gLkdIwHu7ixNCZvFdgA",  "status": "available",  "type": "transfer"}
```

Example 2 (unknown):
```unknown
{  "id": "txn_1MiN3gLkdIwHu7ixxapQrznl",  "object": "balance_transaction",  "amount": -400,  "available_on": 1678043844,  "created": 1678043844,  "currency": "usd",  "description": null,  "exchange_rate": null,  "fee": 0,  "fee_details": [],  "net": -400,  "reporting_category": "transfer",  "source": "tr_1MiN3gLkdIwHu7ixNCZvFdgA",  "status": "available",  "type": "transfer"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/balance_transactions/txn_1MiN3gLkdIwHu7ixxapQrznl \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/balance_transactions/txn_1MiN3gLkdIwHu7ixxapQrznl \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

---

## Authentication

**URL:** https://docs.stripe.com/api/authentication

**Contents:**
- Authentication
- Errors
  - Attributes
    - codenullable string
    - decline_codenullable string
    - messagenullable string
    - paramnullable string
    - payment_intentnullable object
    - typeenum
  - MoreExpand all

The Stripe API uses API keys to authenticate requests. You can view and manage your API keys in the Stripe Dashboard.

Test mode secret keys have the prefix sk_test_ and live mode secret keys have the prefix sk_live_. Alternatively, you can use restricted API keys for granular permissions.

Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.

All API requests must be made over HTTPS. Calls made over plain HTTP will fail. API requests without authentication will also fail.

A sample test API key is included in all the examples here, so you can test any example right away. Do not submit any personally identifiable information in requests made with this key.

To test requests using your account, replace the sample API key with your actual API key or sign in.

Stripe uses conventional HTTP response codes to indicate the success or failure of an API request. In general: Codes in the 2xx range indicate success. Codes in the 4xx range indicate an error that failed given the information provided (e.g., a required parameter was omitted, a charge failed, etc.). Codes in the 5xx range indicate an error with Stripe’s servers (these are rare).

Some 4xx errors that could be handled programmatically (e.g., a card is declined) include an error code that briefly explains the error reported.

For some errors that could be handled programmatically, a short string indicating the error code reported.

For card errors resulting from a card issuer decline, a short string indicating the card issuer’s reason for the decline if they provide one.

A human-readable message providing more details about the error. For card errors, these messages can be shown to your users.

If the error is parameter-specific, the parameter related to the error. For example, you can use this to display a message near the correct form field.

The PaymentIntent object for errors returned on a request involving a PaymentIntent.

The type of error returned. One of api_error, card_error, idempotency_error, or invalid_request_error

Our Client libraries raise exceptions for many reasons, such as a failed charge, invalid parameters, authentication errors, and network unavailability. We recommend writing code that gracefully handles all possible API exceptions.

Many objects allow you to request additional information as an expanded response by using the expand request parameter. This parameter is available on all API requests, and applies to the response of that request only. You can expand responses in two ways.

In many cases, an object contains the ID of a related object in its response properties. For example, a Charge might have an associated Customer ID. You can expand these objects in line with the expand request parameter. The expandable label in this documentation indicates ID fields that you can expand into objects.

Some available fields aren’t included in the responses by default, such as the number and cvc fields for the Issuing Card object. You can request these fields as an expanded response by using the expand request parameter.

You can expand recursively by specifying nested fields after a dot (.). For example, requesting payment_intent.customer on a charge expands the payment_intent property into a full PaymentIntent object, then expands the customer property on that payment intent into a full Customer object.

You can use the expand parameter on any endpoint that returns expandable fields, including list, create, and update endpoints.

Expansions on list requests start with the data property. For example, you can expand data.customers on a request to list charges and associated customers. Performing deep expansions on numerous list requests might result in slower processing times.

Expansions have a maximum depth of four levels (for example, the deepest expansion allowed when listing charges is data.payment_intent.customer.default_source).

You can expand multiple objects at the same time by identifying multiple items in the expand array.

The API supports idempotency for safely retrying requests without accidentally performing the same operation twice. When creating or updating an object, use an idempotency key. Then, if a connection error occurs, you can safely repeat the request without risk of creating a second object or performing the update twice.

To perform an idempotent request, provide an additional IdempotencyKey element to the request options.

Stripe’s idempotency works by saving the resulting status code and body of the first request made for any given idempotency key, regardless of whether it succeeds or fails. Subsequent requests with the same key return the same result, including 500 errors.

A client generates an idempotency key, which is a unique key that the server uses to recognize subsequent retries of the same request. How you create unique keys is up to you, but we suggest using V4 UUIDs, or another random string with enough entropy to avoid collisions. Idempotency keys are up to 255 characters long.

You can remove keys from the system automatically after they’re at least 24 hours old. We generate a new request if a key is reused after the original is pruned. The idempotency layer compares incoming parameters to those of the original request and errors if they’re not the same to prevent accidental misuse.

We save results only after the execution of an endpoint begins. If incoming parameters fail validation, or the request conflicts with another request that’s executing concurrently, we don’t save the idempotent result because no API endpoint initiates the execution. You can retry these requests. Learn more about when you can retry idempotent requests.

All POST requests accept idempotency keys. Don’t send idempotency keys in GET and DELETE requests because it has no effect. These requests are idempotent by definition.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/charges \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:# The colon prevents curl from asking for a password.
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/charges \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:# The colon prevents curl from asking for a password.
```

Example 3 (unknown):
```unknown
# Select a client library to see examples of# handling different kinds of errors.
```

Example 4 (unknown):
```unknown
# Select a client library to see examples of# handling different kinds of errors.
```

---

## Sources Deprecated

**URL:** https://docs.stripe.com/api/sources

**Contents:**
- Sources Deprecated
- The Source object Deprecated
  - Attributes
    - idstring
    - amountnullable integer
    - currencynullable enum
    - customernullable string
    - metadatanullable object
    - ownernullable object
    - redirectnullable object

Source objects allow you to accept a variety of payment methods. They represent a customer’s payment instrument, and can be used with the Stripe API just like a Card object: once chargeable, they can be charged, or can be attached to customers.

Stripe doesn’t recommend using the deprecated Sources API. We recommend that you adopt the PaymentMethods API. This newer API provides access to our latest features and payment method types.

Related guides: Sources API and Sources & Customers.

Unique identifier for the object.

A positive integer in the smallest currency unit (that is, 100 cents for $1.00, or 1 for ¥1, Japanese Yen being a zero-decimal currency) representing the total amount associated with the source. This is the amount for which the source will be chargeable once ready. Required for single_use sources.

Three-letter ISO code for the currency associated with the source. This is the currency for which the source will be chargeable once ready. Required for single_use sources.

The ID of the customer to which this source is attached. This will not be present when the source has not been attached to a customer.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the owner of the payment instrument that may be used or required by particular source types.

Information related to the redirect flow. Present if the source is authenticated by a redirect (flow is redirect).

Extra information about a source. This will appear on your customer’s statement every time you charge the source.

The status of the source, one of canceled, chargeable, consumed, failed, or pending. Only chargeable sources can be used to create a charge.

The type of the source. The type is a payment method, one of ach_credit_transfer, ach_debit, alipay, bancontact, card, card_present, eps, giropay, ideal, multibanco, klarna, p24, sepa_debit, sofort, three_d_secure, or wechat. An additional hash is included on the source with a name matching this value. It contains additional information specific to the payment method used.

Creates a new source object.

The type of the source to create. Required unless customer and original_source are specified (see the Cloning card Sources guide)

Amount associated with the source. This is the amount for which the source will be chargeable once ready. Required for single_use sources. Not supported for receiver type sources, where charge amount may not be specified until funds land.

Three-letter ISO code for the currency associated with the source. This is the currency for which the source will be chargeable once ready.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Information about the owner of the payment instrument that may be used or required by particular source types.

Parameters required for the redirect flow. Required if the source is authenticated by a redirect (flow is redirect).

An arbitrary string to be displayed on your customer’s statement. As an example, if your website is RunClub and the item you’re charging for is a race ticket, you may want to specify a statement_descriptor of RunClub 5K race ticket. While many payment types will display this information, some may not display it at all.

Returns a newly created source.

Updates the specified source by setting the values of the parameters passed. Any parameters not provided will be left unchanged.

This request accepts the metadata and owner as arguments. It is also possible to update type specific information for selected payment methods. Please refer to our payment method guides for more detail.

Amount associated with the source.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Information about the owner of the payment instrument that may be used or required by particular source types.

Returns the source object if the update succeeded. This call will raise an error if update parameters are invalid.

Retrieves an existing source object. Supply the unique source ID from a source creation request and Stripe will return the corresponding up-to-date source object information.

Returns a source if a valid identifier was provided.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "src_1N3lxdLkdIwHu7ixPHXy8UcI",  "object": "source",  "ach_credit_transfer": {    "account_number": "test_eb829353ed79",    "bank_name": "TEST BANK",    "fingerprint": "kBQsBk9KtfCgjEYK",    "refund_account_holder_name": null,    "refund_account_holder_type": null,    "refund_routing_number": null,    "routing_number": "110000000",    "swift_code": "TSTEZ122"  },  "amount": null,  "client_secret": "src_client_secret_ZaOIRUD8a9uGmQobLxGvqKSr",  "created": 1683144457,  "currency": "usd",  "flow": "receiver",  "livemode": false,  "metadata": {},  "owner": {    "address": null,    "email": "jenny.rosen@example.com",    "name": null,    "phone": null,    "verified_address": null,    "verified_email": null,    "verified_name": null,    "verified_phone": null  },  "receiver": {    "address": "110000000-test_eb829353ed79",    "amount_charged": 0,    "amount_received": 0,    "amount_returned": 0,    "refund_attributes_method": "email",    "refund_attributes_status": "missing"  },  "statement_descriptor": null,  "status": "pending",  "type": "ach_credit_transfer",  "usage": "reusable"}
```

Example 2 (unknown):
```unknown
{  "id": "src_1N3lxdLkdIwHu7ixPHXy8UcI",  "object": "source",  "ach_credit_transfer": {    "account_number": "test_eb829353ed79",    "bank_name": "TEST BANK",    "fingerprint": "kBQsBk9KtfCgjEYK",    "refund_account_holder_name": null,    "refund_account_holder_type": null,    "refund_routing_number": null,    "routing_number": "110000000",    "swift_code": "TSTEZ122"  },  "amount": null,  "client_secret": "src_client_secret_ZaOIRUD8a9uGmQobLxGvqKSr",  "created": 1683144457,  "currency": "usd",  "flow": "receiver",  "livemode": false,  "metadata": {},  "owner": {    "address": null,    "email": "jenny.rosen@example.com",    "name": null,    "phone": null,    "verified_address": null,    "verified_email": null,    "verified_name": null,    "verified_phone": null  },  "receiver": {    "address": "110000000-test_eb829353ed79",    "amount_charged": 0,    "amount_received": 0,    "amount_returned": 0,    "refund_attributes_method": "email",    "refund_attributes_status": "missing"  },  "statement_descriptor": null,  "status": "pending",  "type": "ach_credit_transfer",  "usage": "reusable"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/sources \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d type=ach_credit_transfer \  -d currency=usd \  --data-urlencode "owner[email]"="jenny.rosen@example.com"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/sources \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d type=ach_credit_transfer \  -d currency=usd \  --data-urlencode "owner[email]"="jenny.rosen@example.com"
```

---

## Test Stripe Terminal

**URL:** https://docs.stripe.com/terminal/references/testing

**Contents:**
- Test Stripe Terminal
- Learn how to effectively test your Terminal integration.
    - Note
- Simulated reader
  - Reference
- Simulated test cards
  - Reference
  - Standard test cards
  - Test cards for specific success cases
  - Test cards for specific error cases

Much of the process for testing Stripe Terminal is similar to that for testing online Stripe payments. Also, you can’t use Stripe Terminal with mobile wallets (for example, Apple Pay or Google Pay) in testmode. For more information, see the general Stripe testing guide.

The best way to achieve a successful Terminal deployment is to test every part of your integration. We provide testing tools for each stage:

Stripe Terminal SDKs and server-driven integration come with a built-in simulated card reader, so you can develop and test your app without connecting to physical hardware. Whether your integration is complete or you’re still building it, use the simulated reader to emulate all the Terminal flows in your app.

The simulated reader doesn’t provide a UI. After connecting to it in your app, you can see it working when calls to the Stripe SDK or API succeed.

Simulated readers for SDKs automatically simulate card presentment as needed. For the server-driven integration, update your integration to simulate card presentment.

The simulated reader can be configured to use a simulated test card, enabling you to test different flows within your point of sale application.

Before collecting a payment method, configure the simulated reader to use one of the following test card numbers or test payment methods to produce specific responses.

Using these specific cards for saving directly without charging and SetupIntents returns a setup_intent_authentication_failure response.

When using the server-driven integration, use the present_payment_method endpoint to simulate a cardholder tapping or inserting their card on the reader.

If you don’t specify parameters, the simulated payment defaults to a valid test card based on the payment method type of the PaymentIntent. Below are the default test cards for Terminal payment method types:

With the standard test cards, you can also use test amounts to simulate failure scenarios

During connection to a simulated Bluetooth reader, you can configure a simulated reader update.

Set the Terminal.shared.simulatorConfiguration.availableReaderUpdate to any of the following configurations. Calling connectReader triggers a simulated reader update.

Test payments with your Stripe Terminal reader using a physical test card. You can purchase readers and physical test cards from the Terminal tab in the Stripe Dashboard. We also support physical test cards from providers, such as B2.

This physical test card supports both chip entry and contactless payments. It only works with Stripe’s pre-certified readers, and only against the Stripe API in a sandbox. If you attempt to use your physical test card in live mode, the Stripe API returns an error. Unless stated otherwise, use the PIN 1234 when prompted.

When creating payments using a physical test card, use amounts ending in the following decimal values to produce specific responses:

For example, a payment processed using a physical test card for the amount 25.00 USD succeeds; a payment processed for the amount 10.05 USD is declined.

To test your Interac integration, you can use the simulated interac test card or an Interac physical test card. You can order it from the Terminal hardware shop in the Dashboard. You can’t use the Stripe-branded physical test card as an Interac card.

The Interac test card works for both interac_present payments and interac_present refunds. You can use the same test amounts you use for testing card_present payments. Unless stated otherwise, use the PIN 1234 when prompted. To test a declined refund, create a partial refund with an amount ending with the following decimal values: 01, 05, 55, 65, or 75.

The Interac test card doesn’t support contactless payments.

To test your eftpos integration, you can use the simulated eftpos test card or an eftpos physical test card. You can order it from the Terminal hardware shop in the Dashboard. You can’t use the Stripe-branded physical test card as an eftpos card.

You can use the same test amounts you use for testing card_present payments. Unless stated otherwise, use the PIN 1234 when prompted.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/test_helpers/terminal/readers/tmr_xxx/present_payment_method \
  -u "sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/test_helpers/terminal/readers/tmr_xxx/present_payment_method \
  -u "sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{
  "id": "tmr_xxx",
  "object": "terminal.reader",
  "action": {
    "failure_code": null,
    "failure_message": null,
    "process_payment_intent": {
      "payment_intent": "pi_xxx"
    },
    "status": "succeeded",
    "type": "process_payment_intent"
  },
  …
}
```

Example 4 (unknown):
```unknown
{
  "id": "tmr_xxx",
  "object": "terminal.reader",
  "action": {
    "failure_code": null,
    "failure_message": null,
    "process_payment_intent": {
      "payment_intent": "pi_xxx"
    },
    "status": "succeeded",
    "type": "process_payment_intent"
  },
  …
}
```

---

## Set a Stripe API version

**URL:** https://docs.stripe.com/sdks/set-version

**Contents:**
- Set a Stripe API version
- Follow these guidelines to target a different API version than your SDKs use.
  - Setting the API version
    - Note
  - Upgrading your API version
- See also

Your account has a default API version, which defines how you call the API, what functionality you have access to, and what you’re guaranteed to get back as part of the response. However, when using our server-side SDKs, your API calls to Stripe use the API version that was current when the SDK was released. You can’t target a different version when using a strongly typed language such as Java, Go, or .NET.

The stripe-ruby library allows you to set the API version globally or on a per-request basis. If you don’t set an API version, recent versions of stripe-ruby use the API version that was latest at the time your version of stripe-ruby was released. Versions of stripe-ruby before v9 use your account’s default API version.

To set the API version globally with the SDK, assign the version to the Stripe.api_version property:

Or set the version per-request:

When you override the version globally or per-request, the API response objects are also returned in that version.

Before upgrading your API version, carefully review the following resources:

You can upgrade your account’s default API version in Workbench. Update your code to use the latest version of the SDK and set the new API version when making your calls.

Stripe SDKs follow their own versioning policy. See the link below to learn more.

**Examples:**

Example 1 (unknown):
```unknown
require 'stripe'
Stripe.api_key = sk_test_YOUR_TEST_KEY_HERE
Stripe.api_version = '2025-12-15.clover'
```

Example 2 (unknown):
```unknown
require 'stripe'
Stripe.api_key = sk_test_YOUR_TEST_KEY_HERE
Stripe.api_version = '2025-12-15.clover'
```

Example 3 (unknown):
```unknown
require 'stripe'
intent = Stripe::PaymentIntent.retrieve(
  'pi_1DlIVK2eZvKYlo2CW4yj5l2C',
  {
    stripe_version: '2025-12-15.clover',
  }
)
intent.capture
```

Example 4 (unknown):
```unknown
require 'stripe'
intent = Stripe::PaymentIntent.retrieve(
  'pi_1DlIVK2eZvKYlo2CW4yj5l2C',
  {
    stripe_version: '2025-12-15.clover',
  }
)
intent.capture
```

---

## The Balance Transaction object

**URL:** https://docs.stripe.com/api/balance_transactions/object

**Contents:**
- The Balance Transaction object
  - Attributes
    - idstring
    - amountinteger
    - currencyenum
    - descriptionnullable string
    - feeinteger
    - fee_detailsarray of objects
    - netinteger
    - sourcenullable stringExpandable

Unique identifier for the object.

Gross amount of this transaction (in cents). A positive value represents funds charged to another party, and a negative value represents funds sent to another party.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

An arbitrary string attached to the object. Often useful for displaying to users.

Fees (in cents) paid for this transaction. Represented as a positive integer when assessed.

Detailed breakdown of fees (in cents) paid for this transaction.

Net impact to a Stripe balance (in cents). A positive value represents incrementing a Stripe balance, and a negative value decrementing a Stripe balance. You can calculate the net impact of a transaction on a balance by amount - fee

This transaction relates to the Stripe object.

The transaction’s net funds status in the Stripe balance, which are either available or pending.

Transaction type: adjustment, advance, advance_funding, anticipation_repayment, application_fee, application_fee_refund, charge, climate_order_purchase, climate_order_refund, connect_collection_transfer, contribution, issuing_authorization_hold, issuing_authorization_release, issuing_dispute, issuing_transaction, obligation_outbound, obligation_reversal_inbound, payment, payment_failure_refund, payment_network_reserve_hold, payment_network_reserve_release, payment_refund, payment_reversal, payment_unreconciled, payout, payout_cancel, payout_failure, payout_minimum_balance_hold, payout_minimum_balance_release, refund, refund_failure, reserve_transaction, reserved_funds, stripe_fee, stripe_fx_fee, stripe_balance_payment_debit, stripe_balance_payment_debit_reversal, tax_fee, topup, topup_reversal, transfer, transfer_cancel, transfer_failure, or transfer_refund. Learn more about balance transaction types and what they represent. To classify transactions for accounting purposes, consider reporting_category instead.

Retrieves the balance transaction with the given ID.

Note that this endpoint previously used the path /v1/balance/history/:id.

Returns a balance transaction if a valid balance transaction ID was provided. Raises an error otherwise.

Returns a list of transactions that have contributed to the Stripe account balance (e.g., charges, transfers, and so forth). The transactions are returned in sorted order, with the most recent transactions appearing first.

Note that this endpoint was previously called “Balance history” and used the path /v1/balance/history.

For automatic Stripe payouts only, only returns transactions that were paid out on the specified payout ID.

Only returns transactions of the given type. One of: adjustment, advance, advance_funding, anticipation_repayment, application_fee, application_fee_refund, charge, climate_order_purchase, climate_order_refund, connect_collection_transfer, contribution, issuing_authorization_hold, issuing_authorization_release, issuing_dispute, issuing_transaction, obligation_outbound, obligation_reversal_inbound, payment, payment_failure_refund, payment_network_reserve_hold, payment_network_reserve_release, payment_refund, payment_reversal, payment_unreconciled, payout, payout_cancel, payout_failure, payout_minimum_balance_hold, payout_minimum_balance_release, refund, refund_failure, reserve_transaction, reserved_funds, stripe_fee, stripe_fx_fee, stripe_balance_payment_debit, stripe_balance_payment_debit_reversal, tax_fee, topup, topup_reversal, transfer, transfer_cancel, transfer_failure, or transfer_refund.

A dictionary with a data property that contains an array of up to limit transactions, starting after transaction starting_after. Each entry in the array is a separate transaction history object. If no more transactions are available, the resulting array will be empty.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "txn_1MiN3gLkdIwHu7ixxapQrznl",  "object": "balance_transaction",  "amount": -400,  "available_on": 1678043844,  "created": 1678043844,  "currency": "usd",  "description": null,  "exchange_rate": null,  "fee": 0,  "fee_details": [],  "net": -400,  "reporting_category": "transfer",  "source": "tr_1MiN3gLkdIwHu7ixNCZvFdgA",  "status": "available",  "type": "transfer"}
```

Example 2 (unknown):
```unknown
{  "id": "txn_1MiN3gLkdIwHu7ixxapQrznl",  "object": "balance_transaction",  "amount": -400,  "available_on": 1678043844,  "created": 1678043844,  "currency": "usd",  "description": null,  "exchange_rate": null,  "fee": 0,  "fee_details": [],  "net": -400,  "reporting_category": "transfer",  "source": "tr_1MiN3gLkdIwHu7ixNCZvFdgA",  "status": "available",  "type": "transfer"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/balance_transactions/txn_1MiN3gLkdIwHu7ixxapQrznl \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/balance_transactions/txn_1MiN3gLkdIwHu7ixxapQrznl \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

---

## Cancel a PaymentIntent

**URL:** https://docs.stripe.com/api/payment_intents/cancel

**Contents:**
- Cancel a PaymentIntent
  - Parameters
    - cancellation_reasonstring
  - Returns
- Capture a PaymentIntent
  - Parameters
    - amount_to_captureinteger
    - metadataobject
  - More parametersExpand all
    - amount_detailsobject

You can cancel a PaymentIntent object when it’s in one of these statuses: requires_payment_method, requires_capture, requires_confirmation, requires_action or, in rare cases, processing.

After it’s canceled, no additional charges are made by the PaymentIntent and any operations on the PaymentIntent fail with an error. For PaymentIntents with a status of requires_capture, the remaining amount_capturable is automatically refunded.

You can’t cancel the PaymentIntent for a Checkout Session. Expire the Checkout Session instead.

Reason for canceling this PaymentIntent. Possible values are: duplicate, fraudulent, requested_by_customer, or abandoned

Returns a PaymentIntent object if the cancellation succeeds. Returns an error if the PaymentIntent is already canceled or isn’t in a cancelable state.

Capture the funds of an existing uncaptured PaymentIntent when its status is requires_capture.

Uncaptured PaymentIntents are cancelled a set number of days (7 by default) after their creation.

Learn more about separate authorization and capture.

The amount to capture from the PaymentIntent, which must be less than or equal to the original amount. Defaults to the full amount_capturable if it’s not provided.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a PaymentIntent object with status="succeeded" if the PaymentIntent is capturable. Returns an error if the PaymentIntent isn’t capturable or if an invalid amount to capture is provided.

Confirm that your customer intends to pay with current or provided payment method. Upon confirmation, the PaymentIntent will attempt to initiate a payment.

If the selected payment method requires additional authentication steps, the PaymentIntent will transition to the requires_action status and suggest additional actions via next_action. If payment fails, the PaymentIntent transitions to the requires_payment_method status or the canceled status if the confirmation limit is reached. If payment succeeds, the PaymentIntent will transition to the succeeded status (or requires_capture, if capture_method is set to manual).

If the confirmation_method is automatic, payment may be attempted using our client SDKs and the PaymentIntent’s client_secret. After next_actions are handled by the client, no additional confirmation is required to complete the payment.

If the confirmation_method is manual, all payment attempts must be initiated using a secret key.

If any actions are required for the payment, the PaymentIntent will return to the requires_confirmation state after those actions are completed. Your server needs to then explicitly re-confirm the PaymentIntent to initiate the next payment attempt.

There is a variable upper limit on how many times a PaymentIntent can be confirmed. After this limit is reached, any further calls to this endpoint will transition the PaymentIntent to the canceled state.

ID of the payment method (a PaymentMethod, Card, or compatible Source object) to attach to this PaymentIntent. If the payment method is attached to a Customer, it must match the customer that is set on this PaymentIntent.

Email address that the receipt for the resulting payment will be sent to. If receipt_email is specified for a payment in live mode, a receipt will be sent regardless of your email settings.

Indicates that you intend to make future payments with this PaymentIntent’s payment method.

If you provide a Customer with the PaymentIntent, you can use this parameter to attach the payment method to the Customer after the PaymentIntent is confirmed and the customer completes any required actions. If you don’t provide a Customer, you can still attach the payment method to a Customer after the transaction completes.

If the payment method is card_present and isn’t a digital wallet, Stripe creates and attaches a generated_card payment method representing the card to the Customer instead.

When processing card payments, Stripe uses setup_future_usage to help you comply with regional legislation and network rules, such as SCA.

If you’ve already set setup_future_usage and you’re performing a request using a publishable key, you can only update the value from on_session to off_session.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

Shipping information for this PaymentIntent.

Returns the resulting PaymentIntent after all possible transitions are applied.

Perform an incremental authorization on an eligible PaymentIntent. To be eligible, the PaymentIntent’s status must be requires_capture and incremental_authorization_supported must be true.

Incremental authorizations attempt to increase the authorized amount on your customer’s card to the new, higher amount provided. Similar to the initial authorization, incremental authorizations can be declined. A single PaymentIntent can call this endpoint multiple times to further increase the authorized amount.

If the incremental authorization succeeds, the PaymentIntent object returns with the updated amount. If the incremental authorization fails, a card_declined error returns, and no other fields on the PaymentIntent or Charge update. The PaymentIntent object remains capturable for the previously authorized amount.

Each PaymentIntent can have a maximum of 10 incremental authorization attempts, including declines. After it’s captured, a PaymentIntent can no longer be incremented.

Learn more about incremental authorizations.

The updated total amount that you intend to collect from the cardholder. This amount must be greater than the currently authorized amount.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Text that appears on the customer’s statement as the statement descriptor for a non-card or card charge. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

Returns a PaymentIntent object with the updated amount if the incremental authorization succeeds. Returns an error if the incremental authorization failed or the PaymentIntent isn’t eligible for incremental authorizations.

Manually reconcile the remaining amount for a customer_balance PaymentIntent.

Amount that you intend to apply to this PaymentIntent from the customer’s cash balance. If the PaymentIntent was created by an Invoice, the full amount of the PaymentIntent is applied regardless of this parameter.

A positive integer representing how much to charge in the smallest currency unit (for example, 100 cents to charge 1 USD or 100 to charge 100 JPY, a zero-decimal currency). The maximum amount is the amount of the PaymentIntent.

When you omit the amount, it defaults to the remaining amount requested on the PaymentIntent.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

Returns a PaymentIntent object.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/payment_intents/pi_3MtwBwLkdIwHu7ix28a3tqPa/cancel \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/payment_intents/pi_3MtwBwLkdIwHu7ix28a3tqPa/cancel \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",  "object": "payment_intent",  "amount": 2000,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 0,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": {    "enabled": true  },  "canceled_at": 1680801569,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",  "confirmation_method": "automatic",  "created": 1680800504,  "currency": "usd",  "customer": null,  "description": null,  "last_payment_error": null,  "latest_charge": null,  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": null,  "payment_method_options": {    "card": {      "installments": null,      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    },    "link": {      "persistent_token": null    }  },  "payment_method_types": [    "card",    "link"  ],  "processing": null,  "receipt_email": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "source": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "canceled",  "transfer_data": null,  "transfer_group": null}
```

Example 4 (unknown):
```unknown
{  "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",  "object": "payment_intent",  "amount": 2000,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 0,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": {    "enabled": true  },  "canceled_at": 1680801569,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",  "confirmation_method": "automatic",  "created": 1680800504,  "currency": "usd",  "customer": null,  "description": null,  "last_payment_error": null,  "latest_charge": null,  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": null,  "payment_method_options": {    "card": {      "installments": null,      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    },    "link": {      "persistent_token": null    }  },  "payment_method_types": [    "card",    "link"  ],  "processing": null,  "receipt_email": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "source": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "canceled",  "transfer_data": null,  "transfer_group": null}
```

---

## Retrieve a file

**URL:** https://docs.stripe.com/api/files/retrieve

**Contents:**
- Retrieve a file
  - Parameters
  - Returns
- List all files
  - Parameters
    - purposestring
  - More parametersExpand all
    - createdobject
    - ending_beforestring
    - limitinteger

Retrieves the details of an existing file object. After you supply a unique file ID, Stripe returns the corresponding file object. Learn how to access file contents.

If the identifier you provide is valid, a file object returns. If not, Stripe raises an error.

Returns a list of the files that your account has access to. Stripe sorts and returns the files by their creation dates, placing the most recently created files at the top.

Filter queries by the file purpose. If you don’t provide a purpose, the queries return unfiltered files.

A dictionary with a data property that contains an array of up to limit files, starting after the starting_after file. Each entry in the array is a separate file object. If there aren’t additional available files, the resulting array is empty.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/files/file_1Mr4LDLkdIwHu7ixFCz0dZiH \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/files/file_1Mr4LDLkdIwHu7ixFCz0dZiH \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "file_1Mr4LDLkdIwHu7ixFCz0dZiH",  "object": "file",  "created": 1680116847,  "expires_at": 1703444847,  "filename": "file.png",  "links": {    "object": "list",    "data": [],    "has_more": false,    "url": "/v1/file_links?file=file_1Mr4LDLkdIwHu7ixFCz0dZiH"  },  "purpose": "dispute_evidence",  "size": 8429,  "title": null,  "type": "png",  "url": "https://files.stripe.com/v1/files/file_1Mr4LDLkdIwHu7ixFCz0dZiH/contents"}
```

Example 4 (unknown):
```unknown
{  "id": "file_1Mr4LDLkdIwHu7ixFCz0dZiH",  "object": "file",  "created": 1680116847,  "expires_at": 1703444847,  "filename": "file.png",  "links": {    "object": "list",    "data": [],    "has_more": false,    "url": "/v1/file_links?file=file_1Mr4LDLkdIwHu7ixFCz0dZiH"  },  "purpose": "dispute_evidence",  "size": 8429,  "title": null,  "type": "png",  "url": "https://files.stripe.com/v1/files/file_1Mr4LDLkdIwHu7ixFCz0dZiH/contents"}
```

---

## Create a PII token

**URL:** https://docs.stripe.com/api/tokens/create_pii

**Contents:**
- Create a PII token
  - Parameters
    - piiobjectRequired
  - Returns
- Retrieve a token
  - Parameters
  - Returns

Creates a single-use token that represents the details of personally identifiable information (PII). You can use this token in place of an id_number or id_number_secondary in Account or Person Update API methods. You can only use a PII token once.

The PII this token represents.

Returns the created PII token if it’s successful. Otherwise, this call raises an error.

Retrieves the token with the given ID.

Returns a token if you provide a valid ID. Raises an error otherwise.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/tokens \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "pii[id_number]"=000000000
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/tokens \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "pii[id_number]"=000000000
```

Example 3 (unknown):
```unknown
{  "id": "pii_18PwbX2eZvKYlo2CzRXgwN3J",  "object": "token",  "client_ip": "124.123.76.134",  "created": 1466783547,  "livemode": false,  "redaction": null,  "type": "pii",  "used": false}
```

Example 4 (unknown):
```unknown
{  "id": "pii_18PwbX2eZvKYlo2CzRXgwN3J",  "object": "token",  "client_ip": "124.123.76.134",  "created": 1466783547,  "livemode": false,  "redaction": null,  "type": "pii",  "used": false}
```

---

## The Token object

**URL:** https://docs.stripe.com/api/tokens/object

**Contents:**
- The Token object
  - Attributes
    - idstring
    - cardnullable object
  - More attributesExpand all
    - objectstring
    - bank_accountnullable object
    - client_ipnullable string
    - createdtimestamp
    - descriptionnullable string

Unique identifier for the object.

Hash describing the card used to make the charge.

Creates a single-use token that wraps a user’s legal entity information. Use this when creating or updating a Connect account. Learn more about account tokens.

In live mode, you can only create account tokens with your application’s publishable key. In test mode, you can only create account tokens with your secret key or publishable key.

Information for the account this token represents.

Returns the created account token if it’s successful. Otherwise, this call raises an error.

Creates a single-use token that represents a bank account’s details. You can use this token with any v1 API method in place of a bank account dictionary. You can only use this token once. To do so, attach it to a connected account where controller.requirement_collection is application, which includes Custom accounts.

The bank account this token will represent.

Returns the created bank account token if it’s successful. Otherwise, this call raises an error.

Creates a single-use token that represents a credit card’s details. You can use this token in place of a credit card dictionary with any v1 API method. You can only use these tokens once by creating a new Charge object or by attaching them to a Customer object.

To use this functionality, you need to enable access to the raw card data APIs. In most cases, you can use our recommended payments integrations instead of using the API.

The card this token will represent. If you also pass in a customer, the card must be the ID of a card belonging to the customer. Otherwise, if you do not pass in a customer, this is a dictionary containing a user’s credit card details, with the options described below.

Returns the created card token if it’s successful. Otherwise, this call raises an error.

Creates a single-use token that represents an updated CVC value that you can use for CVC re-collection. Use this token when you confirm a card payment or use a saved card on a PaymentIntent with confirmation_method: manual.

For most cases, use our JavaScript library instead of using the API. For a PaymentIntent with confirmation_method: automatic, use our recommended payments integration without tokenizing the CVC value.

The updated CVC value this token represents.

Returns the created CVC update token if it’s successful. Otherwise, this call raises an error.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "tok_1N3T00LkdIwHu7ixt44h1F8k",  "object": "token",  "card": {    "id": "card_1N3T00LkdIwHu7ixRdxpVI1Q",    "object": "card",    "address_city": null,    "address_country": null,    "address_line1": null,    "address_line1_check": null,    "address_line2": null,    "address_state": null,    "address_zip": null,    "address_zip_check": null,    "brand": "Visa",    "country": "US",    "cvc_check": "unchecked",    "dynamic_last4": null,    "exp_month": 5,    "exp_year": 2026,    "fingerprint": "mToisGZ01V71BCos",    "funding": "credit",    "last4": "4242",    "metadata": {},    "name": null,    "tokenization_method": null,    "wallet": null  },  "client_ip": "52.35.78.6",  "created": 1683071568,  "livemode": false,  "type": "card",  "used": false}
```

Example 2 (unknown):
```unknown
{  "id": "tok_1N3T00LkdIwHu7ixt44h1F8k",  "object": "token",  "card": {    "id": "card_1N3T00LkdIwHu7ixRdxpVI1Q",    "object": "card",    "address_city": null,    "address_country": null,    "address_line1": null,    "address_line1_check": null,    "address_line2": null,    "address_state": null,    "address_zip": null,    "address_zip_check": null,    "brand": "Visa",    "country": "US",    "cvc_check": "unchecked",    "dynamic_last4": null,    "exp_month": 5,    "exp_year": 2026,    "fingerprint": "mToisGZ01V71BCos",    "funding": "credit",    "last4": "4242",    "metadata": {},    "name": null,    "tokenization_method": null,    "wallet": null  },  "client_ip": "52.35.78.6",  "created": 1683071568,  "livemode": false,  "type": "card",  "used": false}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/tokens \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "account[business_type]"=individual \  -d "account[individual][first_name]"=Jane \  -d "account[individual][last_name]"=Doe \  -d "account[tos_shown_and_accepted]"=true
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/tokens \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "account[business_type]"=individual \  -d "account[individual][first_name]"=Jane \  -d "account[individual][last_name]"=Doe \  -d "account[tos_shown_and_accepted]"=true
```

---

## Account Tokens v2

**URL:** https://docs.stripe.com/api/v2/account-tokens

**Contents:**
- Account Tokens v2
- The AccountToken object
  - Attributes
    - idstring
    - objectstring, value is "v2.core.account_token"
    - createdtimestamp
    - expires_attimestamp
    - livemodeboolean
    - usedboolean
- Create an account token v2

Account tokens are single-use tokens which tokenize company/individual/business information, and are used for creating or updating an Account.

Unique identifier for the token.

String representing the object’s type. Objects of the same type share the same value of the object field.

Time at which the token was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Time at which the token will expire.

Has the value true if the token exists in live mode or the value false if the object exists in test mode.

Determines if the token has already been used (tokens can only be used once).

Creates an Account Token.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the company, individual, and business represented by the Account.

Unique identifier for the token.

String representing the object’s type. Objects of the same type share the same value of the object field.

Time at which the token was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Time at which the token will expire.

Has the value true if the token exists in live mode or the value false if the object exists in test mode.

Determines if the token has already been used (tokens can only be used once).

Token must be created with publishable key.

Retrieves an Account Token.

The ID of the Account Token to retrieve.

Unique identifier for the token.

String representing the object’s type. Objects of the same type share the same value of the object field.

Time at which the token was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Time at which the token will expire.

Has the value true if the token exists in live mode or the value false if the object exists in test mode.

Determines if the token has already been used (tokens can only be used once).

The resource wasn’t found.

**Examples:**

Example 1 (unknown):
```unknown
{  "created": "2025-01-01T00:00:00.000Z",  "expires_at": "2025-01-01T00:00:00.000Z",  "id": "4242",  "livemode": true,  "object": "4242",  "used": true}
```

Example 2 (unknown):
```unknown
{  "created": "2025-01-01T00:00:00.000Z",  "expires_at": "2025-01-01T00:00:00.000Z",  "id": "4242",  "livemode": true,  "object": "4242",  "used": true}
```

Example 3 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/account_tokens \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "contact_email": "furever@example.com",    "display_name": "Furever",    "identity": {        "attestations": {            "terms_of_service": {                "account": {                    "shown_and_accepted": true                }            }        },        "entity_type": "company",        "business_details": {            "registered_name": "Furever"        }    }  }'
```

Example 4 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/account_tokens \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "contact_email": "furever@example.com",    "display_name": "Furever",    "identity": {        "attestations": {            "terms_of_service": {                "account": {                    "shown_and_accepted": true                }            }        },        "entity_type": "company",        "business_details": {            "registered_name": "Furever"        }    }  }'
```

---

## Update an event destination v2

**URL:** https://docs.stripe.com/api/v2/core/event_destinations/update

**Contents:**
- Update an event destination v2
  - Parameters
    - idstringRequired
    - descriptionstring
    - enabled_eventsarray of strings
    - includearray of enums
    - metadatamap
    - namestring
    - webhook_endpointobject
  - Returns

Update the details of an event destination.

Identifier for the event destination to update.

An optional description of what the event destination is used for.

The list of events to enable for this endpoint.

Additional fields to include in the response. Currently supports webhook_endpoint.url.

Include parameter to expose webhook_endpoint.url.

Event destination name.

Webhook endpoint configuration.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value of the object field.

Amazon EventBridge configuration.

Time at which the object was created.

An optional description of what the event destination is used for.

The list of events to enable for this endpoint.

Payload type of events being subscribed to.

Where events should be routed from.

Receive events from accounts connected to the account that owns the event destination.

Receive events from the account that owns the event destination.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Event destination name.

If using the snapshot event payload, the API version events are rendered as.

Status. It can be set to either enabled or disabled.

Event destination is disabled.

Event destination is enabled.

Additional information about event destination status.

Event destination type.

Time at which the object was last updated.

Webhook endpoint configuration.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

Retrieves the details of an event destination.

Identifier for the event destination to retrieve.

Additional fields to include in the response.

Include parameter to expose webhook_endpoint.url.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value of the object field.

Amazon EventBridge configuration.

Time at which the object was created.

An optional description of what the event destination is used for.

The list of events to enable for this endpoint.

Payload type of events being subscribed to.

Where events should be routed from.

Receive events from accounts connected to the account that owns the event destination.

Receive events from the account that owns the event destination.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Event destination name.

If using the snapshot event payload, the API version events are rendered as.

Status. It can be set to either enabled or disabled.

Event destination is disabled.

Event destination is enabled.

Additional information about event destination status.

Event destination type.

Time at which the object was last updated.

Webhook endpoint configuration.

The resource wasn’t found.

Lists all event destinations.

Additional fields to include in the response. Currently supports webhook_endpoint.url.

Include parameter to expose webhook_endpoint.url.

List of event destinations.

The previous page url.

Delete an event destination.

Identifier for the event destination to delete.

Identifier for the deleted event destination.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

Disable an event destination.

Identifier for the event destination to disable.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value of the object field.

Amazon EventBridge configuration.

Time at which the object was created.

An optional description of what the event destination is used for.

The list of events to enable for this endpoint.

Payload type of events being subscribed to.

Where events should be routed from.

Receive events from accounts connected to the account that owns the event destination.

Receive events from the account that owns the event destination.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Event destination name.

If using the snapshot event payload, the API version events are rendered as.

Status. It can be set to either enabled or disabled.

Event destination is disabled.

Event destination is enabled.

Additional information about event destination status.

Event destination type.

Time at which the object was last updated.

Webhook endpoint configuration.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/event_destinations/ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6 \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "description": "A better description",    "enabled_events": [        "v1.billing.meter.error_report_triggered",        "v1.billing.meter.no_meter_found"    ],    "include": [        "webhook_endpoint.url"    ]  }'
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/event_destinations/ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6 \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "description": "A better description",    "enabled_events": [        "v1.billing.meter.error_report_triggered",        "v1.billing.meter.no_meter_found"    ],    "include": [        "webhook_endpoint.url"    ]  }'
```

Example 3 (unknown):
```unknown
{  "id": "ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6",  "object": "v2.core.event_destination",  "created": "2024-10-22T16:20:09.931Z",  "description": "A better description",  "enabled_events": [    "v1.billing.meter.error_report_triggered",    "v1.billing.meter.no_meter_found"  ],  "event_payload": "thin",  "events_from": [    "self"  ],  "livemode": false,  "metadata": {},  "name": "My Event Destination",  "snapshot_api_version": null,  "status": "disabled",  "status_details": {    "disabled": {      "reason": "user"    }  },  "type": "webhook_endpoint",  "updated": "2024-10-22T16:25:48.976Z",  "webhook_endpoint": {    "signing_secret": null,    "url": "https://example.com/my/webhook/endpoint"  }}
```

Example 4 (unknown):
```unknown
{  "id": "ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6",  "object": "v2.core.event_destination",  "created": "2024-10-22T16:20:09.931Z",  "description": "A better description",  "enabled_events": [    "v1.billing.meter.error_report_triggered",    "v1.billing.meter.no_meter_found"  ],  "event_payload": "thin",  "events_from": [    "self"  ],  "livemode": false,  "metadata": {},  "name": "My Event Destination",  "snapshot_api_version": null,  "status": "disabled",  "status_details": {    "disabled": {      "reason": "user"    }  },  "type": "webhook_endpoint",  "updated": "2024-10-22T16:25:48.976Z",  "webhook_endpoint": {    "signing_secret": null,    "url": "https://example.com/my/webhook/endpoint"  }}
```

---

## Credit Note

**URL:** https://docs.stripe.com/api/credit_notes

**Contents:**
- Credit Note
- The Credit Note object
  - Attributes
    - idstring
    - currencyenum
    - invoicestringExpandable
    - linesobject
    - memonullable string
    - metadatanullable object
    - reasonnullable enum

Issue a credit note to adjust an invoice’s amount after the invoice is finalized.

Related guide: Credit notes

Unique identifier for the object.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

Line items that make up the credit note

Customer-facing text that appears on the credit note PDF.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Reason for issuing this credit note, one of duplicate, fraudulent, order_change, or product_unsatisfactory

Credit issued for a duplicate payment or charge

Credit note issued for fraudulent activity

Credit note issued for order change

Credit note issued for unsatisfactory product

Status of this credit note, one of issued or void. Learn more about voiding credit notes.

The credit note has been issued.

The credit note has been voided.

The integer amount in cents representing the amount of the credit note, excluding exclusive tax and invoice level discounts.

The integer amount in cents representing the total amount of the credit note, including tax and all discount.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value.

The integer amount in cents representing the gross amount being credited for this line item, excluding (exclusive) tax and discounts.

Description of the item being credited.

The integer amount in cents representing the discount being credited for this line item.

The amount of discount calculated per discount for this line item

ID of the invoice line item being credited

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The pretax credit amounts (ex: discount, credit grants, etc) for this line item.

The number of units of product being credited.

The tax rates which apply to the line item.

The tax information of the line item.

The type of the credit note line item, one of invoice_line_item or custom_line_item. When the type is invoice_line_item there is an additional invoice_line_item property on the resource the value of which is the id of the credited line item on the invoice.

The cost of each unit of product being credited.

Same as unit_amount, but contains a decimal value with at most 12 decimal places.

Issue a credit note to adjust the amount of a finalized invoice. A credit note will first reduce the invoice’s amount_remaining (and amount_due), but not below zero. This amount is indicated by the credit note’s pre_payment_amount. The excess amount is indicated by post_payment_amount, and it can result in any combination of the following:

The sum of refunds, customer balance credits, and outside of Stripe credits must equal the post_payment_amount.

You may issue multiple credit notes for an invoice. Each credit note may increment the invoice’s pre_payment_credit_notes_amount, post_payment_credit_notes_amount, or both, depending on the invoice’s amount_remaining at the time of credit note creation.

Line items that make up the credit note. One of amount, lines, or shipping_cost must be provided.

The credit note’s memo appears on the credit note PDF.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Reason for issuing this credit note, one of duplicate, fraudulent, order_change, or product_unsatisfactory

Credit issued for a duplicate payment or charge

Credit note issued for fraudulent activity

Credit note issued for order change

Credit note issued for unsatisfactory product

Returns a credit note object if the call succeeded.

Updates an existing credit note.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the updated credit note object if the call succeeded.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "cn_1MxvRqLkdIwHu7ixY0xbUcxk",  "object": "credit_note",  "amount": 1099,  "amount_shipping": 0,  "created": 1681750958,  "currency": "usd",  "customer": "cus_NjLgPhUokHubJC",  "customer_balance_transaction": null,  "discount_amount": 0,  "discount_amounts": [],  "invoice": "in_1MxvRkLkdIwHu7ixABNtI99m",  "lines": {    "object": "list",    "data": [      {        "id": "cnli_1MxvRqLkdIwHu7ixFpdhBFQf",        "object": "credit_note_line_item",        "amount": 1099,        "description": "T-shirt",        "discount_amount": 0,        "discount_amounts": [],        "invoice_line_item": "il_1MxvRlLkdIwHu7ixnkbntxUV",        "livemode": false,        "quantity": 1,        "tax_rates": [],        "taxes": [],        "type": "invoice_line_item",        "unit_amount": 1099,        "unit_amount_decimal": "1099"      }    ],    "has_more": false,    "url": "/v1/credit_notes/cn_1MxvRqLkdIwHu7ixY0xbUcxk/lines"  },  "livemode": false,  "memo": null,  "metadata": {},  "number": "C9E0C52C-0036-CN-01",  "out_of_band_amount": null,  "pdf": "https://pay.stripe.com/credit_notes/acct_1M2JTkLkdIwHu7ix/test_YWNjdF8xTTJKVGtMa2RJd0h1N2l4LF9Oak9FOUtQNFlPdk52UXhFd2Z4SU45alpEd21kd0Y4LDcyMjkxNzU50200cROQsSK2/pdf?s=ap",  "pre_payment_amount": 1099,  "post_payment_amount": 0,  "reason": null,  "refunds": [],  "shipping_cost": null,  "status": "issued",  "subtotal": 1099,  "subtotal_excluding_tax": 1099,  "total": 1099,  "total_excluding_tax": 1099,  "total_taxes": [],  "type": "pre_payment",  "voided_at": null}
```

Example 2 (unknown):
```unknown
{  "id": "cn_1MxvRqLkdIwHu7ixY0xbUcxk",  "object": "credit_note",  "amount": 1099,  "amount_shipping": 0,  "created": 1681750958,  "currency": "usd",  "customer": "cus_NjLgPhUokHubJC",  "customer_balance_transaction": null,  "discount_amount": 0,  "discount_amounts": [],  "invoice": "in_1MxvRkLkdIwHu7ixABNtI99m",  "lines": {    "object": "list",    "data": [      {        "id": "cnli_1MxvRqLkdIwHu7ixFpdhBFQf",        "object": "credit_note_line_item",        "amount": 1099,        "description": "T-shirt",        "discount_amount": 0,        "discount_amounts": [],        "invoice_line_item": "il_1MxvRlLkdIwHu7ixnkbntxUV",        "livemode": false,        "quantity": 1,        "tax_rates": [],        "taxes": [],        "type": "invoice_line_item",        "unit_amount": 1099,        "unit_amount_decimal": "1099"      }    ],    "has_more": false,    "url": "/v1/credit_notes/cn_1MxvRqLkdIwHu7ixY0xbUcxk/lines"  },  "livemode": false,  "memo": null,  "metadata": {},  "number": "C9E0C52C-0036-CN-01",  "out_of_band_amount": null,  "pdf": "https://pay.stripe.com/credit_notes/acct_1M2JTkLkdIwHu7ix/test_YWNjdF8xTTJKVGtMa2RJd0h1N2l4LF9Oak9FOUtQNFlPdk52UXhFd2Z4SU45alpEd21kd0Y4LDcyMjkxNzU50200cROQsSK2/pdf?s=ap",  "pre_payment_amount": 1099,  "post_payment_amount": 0,  "reason": null,  "refunds": [],  "shipping_cost": null,  "status": "issued",  "subtotal": 1099,  "subtotal_excluding_tax": 1099,  "total": 1099,  "total_excluding_tax": 1099,  "total_taxes": [],  "type": "pre_payment",  "voided_at": null}
```

Example 3 (unknown):
```unknown
{  "id": "cnli_1NPtOx2eZvKYlo2CBH1NpUsU",  "object": "credit_note_line_item",  "amount": 749,  "description": "My First Invoice Item (created for API docs)",  "discount_amount": 0,  "discount_amounts": [],  "invoice_line_item": "il_1NPtOx2eZvKYlo2CAUuq0WVl",  "livemode": false,  "quantity": 1,  "taxes": [],  "tax_rates": [],  "type": "invoice_line_item",  "unit_amount": null,  "unit_amount_decimal": null}
```

Example 4 (unknown):
```unknown
{  "id": "cnli_1NPtOx2eZvKYlo2CBH1NpUsU",  "object": "credit_note_line_item",  "amount": 749,  "description": "My First Invoice Item (created for API docs)",  "discount_amount": 0,  "discount_amounts": [],  "invoice_line_item": "il_1NPtOx2eZvKYlo2CAUuq0WVl",  "livemode": false,  "quantity": 1,  "taxes": [],  "tax_rates": [],  "type": "invoice_line_item",  "unit_amount": null,  "unit_amount_decimal": null}
```

---

## Pagination

**URL:** https://docs.stripe.com/api/pagination

**Contents:**
- Pagination
  - Parameters
    - limitoptional, default is 10
    - starting_afteroptional object ID
    - ending_beforeoptional object ID
  - List Response Format
    - objectstring, value is "list"
    - dataarray
    - has_moreboolean
    - urlurl

All top-level API resources have support for bulk fetches through “list” API methods. For example, you can list charges, list customers, and list invoices. These list API methods share a common structure and accept, at a minimum, the following three parameters: limit, starting_after, and ending_before.

Stripe’s list API methods use cursor-based pagination through the starting_after and ending_before parameters. Both parameters accept an existing object ID value (see below) and return objects in reverse chronological order. The ending_before parameter returns objects listed before the named object. The starting_after parameter returns objects listed after the named object. These parameters are mutually exclusive. You can use either the starting_after or ending_before parameter, but not both simultaneously.

Our client libraries offer auto-pagination helpers to traverse all pages of a list.

This specifies a limit on the number of objects to return, ranging between 1 and 100.

A cursor to use in pagination. starting_after is an object ID that defines your place in the list. For example, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include starting_after=obj_foo to fetch the next page of the list.

A cursor to use in pagination. ending_before is an object ID that defines your place in the list. For example, if you make a list request and receive 100 objects, starting with obj_bar, your subsequent call can include ending_before=obj_bar to fetch the previous page of the list.

A string that provides a description of the object type that returns.

An array containing the actual response elements, paginated by any request parameters.

Whether or not there are more elements available after this set. If false, this set comprises the end of the list.

The URL for accessing this list.

APIs within the /v2 namespace contain a different pagination interface than the v1 namespace.

Some top-level API resource have support for retrieval via “search” API methods. For example, you can search charges, search customers, and search subscriptions.

Stripe’s search API methods utilize cursor-based pagination via the page request parameter and next_page response parameter. For example, if you make a search request and receive "next_page": "pagination_key" in the response, your subsequent call can include page=pagination_key to fetch the next page of results.

Our client libraries offer auto-pagination helpers to easily traverse all pages of a search result.

The search query string. See search query language.

A limit on the number of objects returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A string describing the object type returned.

The URL for accessing this list.

Whether or not there are more elements available after this set. If false, this set comprises the end of the list.

An array containing the actual response elements, paginated by any request parameters.

A cursor for use in pagination. If has_more is true, you can pass the value of next_page to a subsequent call to fetch the next page of results.

The total number of objects that match the query, only accurate up to 10,000. This field isn’t included by default. To include it in the response, expand the total_count field.

Our libraries support auto-pagination. This feature allows you to easily iterate through large lists of resources without having to manually perform the requests to fetch subsequent pages.

Each API request has an associated request identifier. You can find this value in the response headers, under Request-Id. You can also find request identifiers in the URLs of individual request logs in your Dashboard.

To expedite the resolution process, provide the request identifier when you contact us about a specific request.

If you use Stripe Connect, you can issue requests on behalf of your connected accounts. To act as a connected account, include a Stripe-Account header containing the connected account ID, which typically starts with the acct_ prefix.

The connected account ID is set per-request. Methods on the returned object reuse the same account ID.

**Examples:**

Example 1 (unknown):
```unknown
{  "object": "list",  "url": "/v1/customers",  "has_more": false,  "data": [    {      "id": "cus_4QFJOjw2pOmAGJ",      "object": "customer",      "address": null,      "balance": 0,      "created": 1405641735,      "currency": "usd",      "default_source": "card_14HOpG2eZvKYlo2Cz4u5AJG5",      "delinquent": false,      "description": "New customer",      "discount": null,      "email": null,      "invoice_prefix": "7D11B54",      "invoice_settings": {        "custom_fields": null,        "default_payment_method": null,        "footer": null,        "rendering_options": null      },      "livemode": false,      "metadata": {        "order_id": "6735"      },      "name": "cus_4QFJOjw2pOmAGJ",      "next_invoice_sequence": 25,      "phone": null,      "preferred_locales": [],      "shipping": null,      "tax_exempt": "none",      "test_clock": null    },  ]}
```

Example 2 (unknown):
```unknown
{  "object": "list",  "url": "/v1/customers",  "has_more": false,  "data": [    {      "id": "cus_4QFJOjw2pOmAGJ",      "object": "customer",      "address": null,      "balance": 0,      "created": 1405641735,      "currency": "usd",      "default_source": "card_14HOpG2eZvKYlo2Cz4u5AJG5",      "delinquent": false,      "description": "New customer",      "discount": null,      "email": null,      "invoice_prefix": "7D11B54",      "invoice_settings": {        "custom_fields": null,        "default_payment_method": null,        "footer": null,        "rendering_options": null      },      "livemode": false,      "metadata": {        "order_id": "6735"      },      "name": "cus_4QFJOjw2pOmAGJ",      "next_invoice_sequence": 25,      "phone": null,      "preferred_locales": [],      "shipping": null,      "tax_exempt": "none",      "test_clock": null    },  ]}
```

Example 3 (unknown):
```unknown
{  "object": "search_result",  "url": "/v1/customers/search",  "has_more": false,  "data": [    {      "id": "cus_4QFJOjw2pOmAGJ",      "object": "customer",      "address": null,      "balance": 0,      "created": 1405641735,      "currency": "usd",      "default_source": "card_14HOpG2eZvKYlo2Cz4u5AJG5",      "delinquent": false,      "description": "someone@example.com for Coderwall",      "discount": null,      "email": null,      "invoice_prefix": "7D11B54",      "invoice_settings": {        "custom_fields": null,        "default_payment_method": null,        "footer": null,        "rendering_options": null      },      "livemode": false,      "metadata": {        "foo": "bar"      },      "name": "fakename",      "next_invoice_sequence": 25,      "phone": null,      "preferred_locales": [],      "shipping": null,      "tax_exempt": "none",      "test_clock": null    }  ]}
```

Example 4 (unknown):
```unknown
{  "object": "search_result",  "url": "/v1/customers/search",  "has_more": false,  "data": [    {      "id": "cus_4QFJOjw2pOmAGJ",      "object": "customer",      "address": null,      "balance": 0,      "created": 1405641735,      "currency": "usd",      "default_source": "card_14HOpG2eZvKYlo2Cz4u5AJG5",      "delinquent": false,      "description": "someone@example.com for Coderwall",      "discount": null,      "email": null,      "invoice_prefix": "7D11B54",      "invoice_settings": {        "custom_fields": null,        "default_payment_method": null,        "footer": null,        "rendering_options": null      },      "livemode": false,      "metadata": {        "foo": "bar"      },      "name": "fakename",      "next_invoice_sequence": 25,      "phone": null,      "preferred_locales": [],      "shipping": null,      "tax_exempt": "none",      "test_clock": null    }  ]}
```

---

## Create a person token

**URL:** https://docs.stripe.com/api/tokens/create_person

**Contents:**
- Create a person token
  - Parameters
    - personobjectRequired
  - Returns
- Create a PII token
  - Parameters
    - piiobjectRequired
  - Returns
- Retrieve a token
  - Parameters

Creates a single-use token that represents the details for a person. Use this when you create or update persons associated with a Connect account. Learn more about account tokens.

You can only create person tokens with your application’s publishable key and in live mode. You can use your application’s secret key to create person tokens only in test mode.

Information for the person this token represents.

Returns the created person token if it’s successful. Otherwise, this call raises an error.

Creates a single-use token that represents the details of personally identifiable information (PII). You can use this token in place of an id_number or id_number_secondary in Account or Person Update API methods. You can only use a PII token once.

The PII this token represents.

Returns the created PII token if it’s successful. Otherwise, this call raises an error.

Retrieves the token with the given ID.

Returns a token if you provide a valid ID. Raises an error otherwise.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/tokens \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "person[first_name]"=Jane \  -d "person[last_name]"=Doe \  -d "person[relationship][owner]"=true
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/tokens \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "person[first_name]"=Jane \  -d "person[last_name]"=Doe \  -d "person[relationship][owner]"=true
```

Example 3 (unknown):
```unknown
{  "id": "cpt_1EDww82eZvKYlo2CsdelTHFu",  "object": "token",  "client_ip": "8.21.168.117",  "created": 1552582904,  "livemode": false,  "redaction": null,  "type": "person",  "used": false}
```

Example 4 (unknown):
```unknown
{  "id": "cpt_1EDww82eZvKYlo2CsdelTHFu",  "object": "token",  "client_ip": "8.21.168.117",  "created": 1552582904,  "livemode": false,  "redaction": null,  "type": "person",  "used": false}
```

---

## Create a customer

**URL:** https://docs.stripe.com/api/customers/create

**Contents:**
- Create a customer
  - Parameters
    - addressobjectRequired if calculating taxes
    - descriptionstring
    - emailstring
    - metadataobject
    - namestring
    - payment_methodstring
    - phonestring
    - shippingobject

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

Returns a list of your customers. The customers are returned sorted by creation date, with the most recent customers appearing first.

A case-sensitive filter on the list based on the customer’s email field. The value must be a string.

The maximum length is 512 characters.

A dictionary with a data property that contains an array of up to limit customers, starting after customer starting_after. Passing an optional email will result in filtering to customers with only that exact email address. Each entry in the array is a separate customer object. If no more customers are available, the resulting array will be empty.

Permanently deletes a customer. It cannot be undone. Also immediately cancels any active subscriptions on the customer.

Returns an object with a deleted parameter on success. If the customer ID does not exist, this call raises an error.

Unlike other objects, deleted customers can still be retrieved through the API in order to be able to track their history. Deleting customers removes all credit card details and prevents any further operations to be performed (such as adding a new subscription).

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/customers \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d name="Jenny Rosen" \  --data-urlencode email="jennyrosen@example.com"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/customers \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d name="Jenny Rosen" \  --data-urlencode email="jennyrosen@example.com"
```

Example 3 (unknown):
```unknown
{  "id": "cus_NffrFeUfNV2Hib",  "object": "customer",  "address": null,  "balance": 0,  "created": 1680893993,  "currency": null,  "default_source": null,  "delinquent": false,  "description": null,  "email": "jennyrosen@example.com",  "invoice_prefix": "0759376C",  "invoice_settings": {    "custom_fields": null,    "default_payment_method": null,    "footer": null,    "rendering_options": null  },  "livemode": false,  "metadata": {},  "name": "Jenny Rosen",  "next_invoice_sequence": 1,  "phone": null,  "preferred_locales": [],  "shipping": null,  "tax_exempt": "none",  "test_clock": null}
```

Example 4 (unknown):
```unknown
{  "id": "cus_NffrFeUfNV2Hib",  "object": "customer",  "address": null,  "balance": 0,  "created": 1680893993,  "currency": null,  "default_source": null,  "delinquent": false,  "description": null,  "email": "jennyrosen@example.com",  "invoice_prefix": "0759376C",  "invoice_settings": {    "custom_fields": null,    "default_payment_method": null,    "footer": null,    "rendering_options": null  },  "livemode": false,  "metadata": {},  "name": "Jenny Rosen",  "next_invoice_sequence": 1,  "phone": null,  "preferred_locales": [],  "shipping": null,  "tax_exempt": "none",  "test_clock": null}
```

---

## Secrets

**URL:** https://docs.stripe.com/api/secret_management

**Contents:**
- Secrets
- The Secret object
  - Attributes
    - idstring
    - objectstring
    - createdtimestamp
    - deletednullable boolean
    - expires_atnullable timestamp
    - livemodeboolean
    - namestring

Secret Store is an API that allows Stripe Apps developers to securely persist secrets for use by UI Extensions and app backends.

The primary resource in Secret Store is a secret. Other apps can’t view secrets created by an app. Additionally, secrets are scoped to provide further permission control.

All Dashboard users and the app backend share account scoped secrets. Use the account scope for secrets that don’t change per-user, like a third-party API key.

A user scoped secret is accessible by the app backend and one specific Dashboard user. Use the user scope for per-user secrets like per-user OAuth tokens, where different users might have different permissions.

Related guide: Store data between page reloads

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value.

Time at which the object was created. Measured in seconds since the Unix epoch.

If true, indicates that this secret has been deleted

The Unix timestamp for the expiry time of the secret, after which the secret deletes.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

A name for the secret that’s unique within the scope.

The plaintext secret value to be stored.

Specifies the scoping of the secret. Requests originating from UI extensions can only access account-scoped secrets or secrets scoped to their own user.

List all secrets stored on the given scope.

Specifies the scoping of the secret. Requests originating from UI extensions can only access account-scoped secrets or secrets scoped to their own user.

A dictionary with a data property that contains an array of up to limit Secrets, starting after Secret starting_after. Each entry in the array is a separate Secret object. If no more Secrets are available, the resulting array will be empty.

Deletes a secret from the secret store by name and scope.

A name for the secret that’s unique within the scope.

Specifies the scoping of the secret. Requests originating from UI extensions can only access account-scoped secrets or secrets scoped to their own user.

Returns the deleted secret object.

Finds a secret in the secret store by name and scope.

A name for the secret that’s unique within the scope.

Specifies the scoping of the secret. Requests originating from UI extensions can only access account-scoped secrets or secrets scoped to their own user.

Returns a secret object.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "appsecret_5110hHS1707T6fjBnah1LkdIwHu7ix",  "object": "apps.secret",  "created": 1680209063,  "expires_at": null,  "livemode": false,  "name": "my-api-key",  "scope": {    "type": "account"  }}
```

Example 2 (unknown):
```unknown
{  "id": "appsecret_5110hHS1707T6fjBnah1LkdIwHu7ix",  "object": "apps.secret",  "created": 1680209063,  "expires_at": null,  "livemode": false,  "name": "my-api-key",  "scope": {    "type": "account"  }}
```

Example 3 (unknown):
```unknown
curl -G https://api.stripe.com/v1/apps/secrets \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "scope[type]"=account
```

Example 4 (unknown):
```unknown
curl -G https://api.stripe.com/v1/apps/secrets \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "scope[type]"=account
```

---

## The AccountToken object

**URL:** https://docs.stripe.com/api/v2/account-tokens/object

**Contents:**
- The AccountToken object
  - Attributes
    - idstring
    - objectstring, value is "v2.core.account_token"
    - createdtimestamp
    - expires_attimestamp
    - livemodeboolean
    - usedboolean
- Create an account token v2
  - Parameters

Unique identifier for the token.

String representing the object’s type. Objects of the same type share the same value of the object field.

Time at which the token was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Time at which the token will expire.

Has the value true if the token exists in live mode or the value false if the object exists in test mode.

Determines if the token has already been used (tokens can only be used once).

Creates an Account Token.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the company, individual, and business represented by the Account.

Unique identifier for the token.

String representing the object’s type. Objects of the same type share the same value of the object field.

Time at which the token was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Time at which the token will expire.

Has the value true if the token exists in live mode or the value false if the object exists in test mode.

Determines if the token has already been used (tokens can only be used once).

Token must be created with publishable key.

Retrieves an Account Token.

The ID of the Account Token to retrieve.

Unique identifier for the token.

String representing the object’s type. Objects of the same type share the same value of the object field.

Time at which the token was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Time at which the token will expire.

Has the value true if the token exists in live mode or the value false if the object exists in test mode.

Determines if the token has already been used (tokens can only be used once).

The resource wasn’t found.

**Examples:**

Example 1 (unknown):
```unknown
{  "created": "2025-01-01T00:00:00.000Z",  "expires_at": "2025-01-01T00:00:00.000Z",  "id": "4242",  "livemode": true,  "object": "4242",  "used": true}
```

Example 2 (unknown):
```unknown
{  "created": "2025-01-01T00:00:00.000Z",  "expires_at": "2025-01-01T00:00:00.000Z",  "id": "4242",  "livemode": true,  "object": "4242",  "used": true}
```

Example 3 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/account_tokens \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "contact_email": "furever@example.com",    "display_name": "Furever",    "identity": {        "attestations": {            "terms_of_service": {                "account": {                    "shown_and_accepted": true                }            }        },        "entity_type": "company",        "business_details": {            "registered_name": "Furever"        }    }  }'
```

Example 4 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/account_tokens \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "contact_email": "furever@example.com",    "display_name": "Furever",    "identity": {        "attestations": {            "terms_of_service": {                "account": {                    "shown_and_accepted": true                }            }        },        "entity_type": "company",        "business_details": {            "registered_name": "Furever"        }    }  }'
```

---

## Visa compliance disputes

**URL:** https://docs.stripe.com/disputes/api/visa-compliance

**Contents:**
- Visa compliance disputes
- Use the API to respond to Visa compliance disputes.
    - Note
- Identify Visa compliance disputes
- Close Visa compliance disputes using the API
    - Warning
- Respond to Visa compliance disputes using the API
    - Warning
- Testing
    - Note

Businesses receive Visa compliance disputes in certain cases when the card issuer believes the disputed transaction doesn’t conform to Visa’s network rules. If Visa compliance disputes can’t be resolved between the parties, the dispute is resolved by the network in exchange for a fee.

If you contest a Visa compliance dispute, in addition to the applicable Stripe dispute fees, Stripe collects a 500 USD (or local equivalent) amount to cover the network costs associated with resolving Visa compliance disputes. Stripe refunds the 500 USD if you win the dispute.

Compliance cases filed by issuers are referred to as pre-compliance disputes by Visa.

Learn more about Visa rules.

You can identify a Visa compliance dispute from the dispute object.

Use any of the following indicators to identify a Visa compliance dispute:

Closing a Visa compliance dispute indicates that you don’t have any evidence to submit and are essentially dismissing the dispute, acknowledging it as lost. You aren’t charged the 500 USD Visa compliance network fee if you choose to close the dispute.

To close a dispute, use the close API.

Closing a dispute is irreversible.

The process of responding to a Visa compliance dispute is similar to responding to other disputes. You can use the update API to submit evidence to counter a dispute.

For Visa compliance disputes, you must explicitly acknowledge a 500 USD using the enhanced evidence object. Stripe withdraws the 500 USD network fee from your account when you submit evidence. Stripe refunds this network fee if you win the dispute.

To acknowledge the network fee, you must set evidence.enhanced_evidence.visa_compliance.fee_acknowledged to true when submitting evidence.

If you acknowledge the Visa compliance network fee, evidence_details.enhanced_eligibility.visa_compliance.status changes to fee_acknowledged, indicating your acknowledgement.

If you attempt to submit evidence for a Visa compliance dispute without acknowledging the network fee, Stripe returns an error response and doesn’t submit your provided evidence.

To test responding to Visa compliance disputes, use the following test card, which creates a Visa compliance dispute:

Similar to live mode Visa compliance disputes, Stripe returns an error response if you submit evidence without acknowledging the network fee.

To simulate a won or lost state for the overall dispute, set uncategorized_text to winning_evidence or losing_evidence as outlined in Testing.

**Examples:**

Example 1 (unknown):
```unknown
{
  "id": "du_TFCU9xJ2Gsj7BAiAoQok8Icp",
  "charge": "ch_vEUUPELhHVkPbMN1md3B0vG7",
  "enhanced_eligibility_types": ["visa_compliance"],
  "reason": "noncompliant",
  "payment_method_details": {
    "card": {
      "brand": "visa",
      "case_type": "compliance"
    }
  }
}
```

Example 2 (unknown):
```unknown
{
  "id": "du_TFCU9xJ2Gsj7BAiAoQok8Icp",
  "charge": "ch_vEUUPELhHVkPbMN1md3B0vG7",
  "enhanced_eligibility_types": ["visa_compliance"],
  "reason": "noncompliant",
  "payment_method_details": {
    "card": {
      "brand": "visa",
      "case_type": "compliance"
    }
  }
}
```

Example 3 (unknown):
```unknown
{
  "id": "du_TFCU9xJ2Gsj7BAiAoQok8Icp",
  "charge": "ch_vEUUPELhHVkPbMN1md3B0vG7",
  "evidence": {
    ...
    "enhanced_evidence": {
      "visa_compliance": {
        "fee_acknowledged": true
    },
  }
  ...
}
```

Example 4 (unknown):
```unknown
{
  "id": "du_TFCU9xJ2Gsj7BAiAoQok8Icp",
  "charge": "ch_vEUUPELhHVkPbMN1md3B0vG7",
  "evidence": {
    ...
    "enhanced_evidence": {
      "visa_compliance": {
        "fee_acknowledged": true
    },
  }
  ...
}
```

---

## Retrieve a dispute

**URL:** https://docs.stripe.com/api/disputes/retrieve

**Contents:**
- Retrieve a dispute
  - Parameters
  - Returns
- List all disputes
  - Parameters
    - chargestring
    - payment_intentstring
  - More parametersExpand all
    - createdobject
    - ending_beforestring

Retrieves the dispute with the given ID.

Returns a dispute if a valid dispute ID was provided. Raises an error otherwise.

Returns a list of your disputes.

Only return disputes associated to the charge specified by this charge ID.

Only return disputes associated to the PaymentIntent specified by this PaymentIntent ID.

A dictionary with a data property that contains an array of up to limit disputes, starting after dispute starting_after. Each entry in the array is a separate dispute object. If no more disputes are available, the resulting array will be empty.

Closing the dispute for a charge indicates that you do not have any evidence to submit and are essentially dismissing the dispute, acknowledging it as lost.

The status of the dispute will change from needs_response to lost. Closing a dispute is irreversible.

Returns the dispute object.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/disputes/du_1MtJUT2eZvKYlo2CNaw2HvEv \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/disputes/du_1MtJUT2eZvKYlo2CNaw2HvEv \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "du_1MtJUT2eZvKYlo2CNaw2HvEv",  "object": "dispute",  "amount": 1000,  "balance_transactions": [],  "charge": "ch_1AZtxr2eZvKYlo2CJDX8whov",  "created": 1680651737,  "currency": "usd",  "evidence": {    "access_activity_log": null,    "billing_address": null,    "cancellation_policy": null,    "cancellation_policy_disclosure": null,    "cancellation_rebuttal": null,    "customer_communication": null,    "customer_email_address": null,    "customer_name": null,    "customer_purchase_ip": null,    "customer_signature": null,    "duplicate_charge_documentation": null,    "duplicate_charge_explanation": null,    "duplicate_charge_id": null,    "product_description": null,    "receipt": null,    "refund_policy": null,    "refund_policy_disclosure": null,    "refund_refusal_explanation": null,    "service_date": null,    "service_documentation": null,    "shipping_address": null,    "shipping_carrier": null,    "shipping_date": null,    "shipping_documentation": null,    "shipping_tracking_number": null,    "uncategorized_file": null,    "uncategorized_text": null  },  "evidence_details": {    "due_by": 1682294399,    "has_evidence": false,    "past_due": false,    "submission_count": 0  },  "is_charge_refundable": true,  "livemode": false,  "metadata": {},  "payment_intent": null,  "reason": "general",  "status": "warning_needs_response"}
```

Example 4 (unknown):
```unknown
{  "id": "du_1MtJUT2eZvKYlo2CNaw2HvEv",  "object": "dispute",  "amount": 1000,  "balance_transactions": [],  "charge": "ch_1AZtxr2eZvKYlo2CJDX8whov",  "created": 1680651737,  "currency": "usd",  "evidence": {    "access_activity_log": null,    "billing_address": null,    "cancellation_policy": null,    "cancellation_policy_disclosure": null,    "cancellation_rebuttal": null,    "customer_communication": null,    "customer_email_address": null,    "customer_name": null,    "customer_purchase_ip": null,    "customer_signature": null,    "duplicate_charge_documentation": null,    "duplicate_charge_explanation": null,    "duplicate_charge_id": null,    "product_description": null,    "receipt": null,    "refund_policy": null,    "refund_policy_disclosure": null,    "refund_refusal_explanation": null,    "service_date": null,    "service_documentation": null,    "shipping_address": null,    "shipping_carrier": null,    "shipping_date": null,    "shipping_documentation": null,    "shipping_tracking_number": null,    "uncategorized_file": null,    "uncategorized_text": null  },  "evidence_details": {    "due_by": 1682294399,    "has_evidence": false,    "past_due": false,    "submission_count": 0  },  "is_charge_refundable": true,  "livemode": false,  "metadata": {},  "payment_intent": null,  "reason": "general",  "status": "warning_needs_response"}
```

---

## List all balance transactions

**URL:** https://docs.stripe.com/api/balance_transactions/list

**Contents:**
- List all balance transactions
  - Parameters
    - payoutstring
    - typestring
  - More parametersExpand all
    - createdobject
    - currencyenum
    - ending_beforestring
    - limitinteger
    - sourcestring

Returns a list of transactions that have contributed to the Stripe account balance (e.g., charges, transfers, and so forth). The transactions are returned in sorted order, with the most recent transactions appearing first.

Note that this endpoint was previously called “Balance history” and used the path /v1/balance/history.

For automatic Stripe payouts only, only returns transactions that were paid out on the specified payout ID.

Only returns transactions of the given type. One of: adjustment, advance, advance_funding, anticipation_repayment, application_fee, application_fee_refund, charge, climate_order_purchase, climate_order_refund, connect_collection_transfer, contribution, issuing_authorization_hold, issuing_authorization_release, issuing_dispute, issuing_transaction, obligation_outbound, obligation_reversal_inbound, payment, payment_failure_refund, payment_network_reserve_hold, payment_network_reserve_release, payment_refund, payment_reversal, payment_unreconciled, payout, payout_cancel, payout_failure, payout_minimum_balance_hold, payout_minimum_balance_release, refund, refund_failure, reserve_transaction, reserved_funds, stripe_fee, stripe_fx_fee, stripe_balance_payment_debit, stripe_balance_payment_debit_reversal, tax_fee, topup, topup_reversal, transfer, transfer_cancel, transfer_failure, or transfer_refund.

A dictionary with a data property that contains an array of up to limit transactions, starting after transaction starting_after. Each entry in the array is a separate transaction history object. If no more transactions are available, the resulting array will be empty.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v1/balance_transactions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v1/balance_transactions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 3 (unknown):
```unknown
{  "object": "list",  "url": "/v1/balance_transactions",  "has_more": false,  "data": [    {      "id": "txn_1MiN3gLkdIwHu7ixxapQrznl",      "object": "balance_transaction",      "amount": -400,      "available_on": 1678043844,      "created": 1678043844,      "currency": "usd",      "description": null,      "exchange_rate": null,      "fee": 0,      "fee_details": [],      "net": -400,      "reporting_category": "transfer",      "source": "tr_1MiN3gLkdIwHu7ixNCZvFdgA",      "status": "available",      "type": "transfer"    }  ]}
```

Example 4 (unknown):
```unknown
{  "object": "list",  "url": "/v1/balance_transactions",  "has_more": false,  "data": [    {      "id": "txn_1MiN3gLkdIwHu7ixxapQrznl",      "object": "balance_transaction",      "amount": -400,      "available_on": 1678043844,      "created": 1678043844,      "currency": "usd",      "description": null,      "exchange_rate": null,      "fee": 0,      "fee_details": [],      "net": -400,      "reporting_category": "transfer",      "source": "tr_1MiN3gLkdIwHu7ixNCZvFdgA",      "status": "available",      "type": "transfer"    }  ]}
```

---

## Test Clocks Test helper

**URL:** https://docs.stripe.com/api/test_clocks

**Contents:**
- Test Clocks Test helper
- The Test Clock object Test helper
  - Attributes
    - idstring
    - objectstring
    - createdtimestamp
    - deletes_aftertimestamp
    - frozen_timetimestamp
    - livemodeboolean
    - namenullable string

A test clock enables deterministic control over objects in testmode. With a test clock, you can create objects at a frozen time in the past or future, and advance to a specific future time to observe webhooks and state changes. After the clock advances, you can either validate the current state of your scenario (and test your assumptions), change the current state of your scenario (and test more complex scenarios), or keep advancing forward in time.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value.

Time at which the object was created. Measured in seconds since the Unix epoch.

Time at which this clock is scheduled to auto delete.

Time at which all objects belonging to this clock are frozen.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The custom name supplied at creation.

The status of the Test Clock.

In the process of advancing time for the test clock objects.

Failed to advance time. Future requests to advance time will fail.

All test clock objects have advanced to the frozen_time.

Details on the current state of the Test Clock.

Creates a new test clock that can be attached to new customers and quotes.

The initial frozen time for this test clock.

The name for this test clock.

The maximum length is 300 characters.

The newly created TestClock object is returned upon success. Otherwise, this call raises an error.

Retrieves a test clock.

Returns the TestClock object. Otherwise, this call raises an error.

Returns a list of your test clocks.

A dictionary with a data property that contains an array of up to limit test clocks, starting after starting_after. Each entry in the array is a separate test clock object. If no more test clocks are available, the resulting array will be empty.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "clock_1Mr3I22eZvKYlo2Ck0rgMqd7",  "object": "test_helpers.test_clock",  "created": 1680112806,  "deletes_after": 1680717606,  "frozen_time": 1577836800,  "livemode": false,  "name": null,  "status": "ready"}
```

Example 2 (unknown):
```unknown
{  "id": "clock_1Mr3I22eZvKYlo2Ck0rgMqd7",  "object": "test_helpers.test_clock",  "created": 1680112806,  "deletes_after": 1680717606,  "frozen_time": 1577836800,  "livemode": false,  "name": null,  "status": "ready"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/test_helpers/test_clocks \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d frozen_time=1577836800
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/test_helpers/test_clocks \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d frozen_time=1577836800
```

---

## Create a refund

**URL:** https://docs.stripe.com/api/refunds/create

**Contents:**
- Create a refund
  - Parameters
    - amountinteger
    - chargestring
    - metadataobject
    - payment_intentstring
    - reasonstring
  - More parametersExpand all
    - instructions_emailstring
    - originenum

When you create a new refund, you must specify a Charge or a PaymentIntent object on which to create it.

Creating a new refund will refund a charge that has previously been created but not yet refunded. Funds will be refunded to the credit or debit card that was originally charged.

You can optionally refund only part of a charge. You can do so multiple times, until the entire charge has been refunded.

Once entirely refunded, a charge can’t be refunded again. This method will raise an error when called on an already-refunded charge, or when trying to refund more money than is left on a charge.

A positive integer in the smallest currency unit representing how much of this charge to refund. Can refund only up to the remaining, unrefunded amount of the charge.

The identifier of the charge to refund.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The identifier of the PaymentIntent to refund.

String indicating the reason for the refund. If set, possible values are duplicate, fraudulent, and requested_by_customer. If you believe the charge to be fraudulent, specifying fraudulent as the reason will add the associated card and email to your block lists, and will also help us improve our fraud detection algorithms.

Returns the Refund object if the refund succeeded. Raises an error if the Charge/PaymentIntent has already been refunded, or if an invalid identifier was provided.

Updates the refund that you specify by setting the values of the passed parameters. Any parameters that you don’t provide remain unchanged.

This request only accepts metadata as an argument.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the refund object if the update succeeds. This call raises an error if update parameters are invalid.

Retrieves the details of an existing refund.

Returns a refund if you provide a valid ID. Raises an error otherwise.

Returns a list of all refunds you created. We return the refunds in sorted order, with the most recent refunds appearing first. The 10 most recent refunds are always available by default on the Charge object.

Only return refunds for the charge specified by this charge ID.

Only return refunds for the PaymentIntent specified by this ID.

A dictionary with a data property that contains an array of up to limit refunds, starting after the starting_after refund. Each entry in the array is a separate Refund object. If no other refunds are available, the resulting array is empty. If you provide a non-existent charge ID, this call raises an error.

Cancels a refund with a status of requires_action.

You can’t cancel refunds in other states. Only refunds for payment methods that require customer action can enter the requires_action state.

Returns the refund object if the cancellation succeeds. This call raises an error if you can’t cancel the refund.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/refunds \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d charge=ch_1NirD82eZvKYlo2CIvbtLWuY
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/refunds \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d charge=ch_1NirD82eZvKYlo2CIvbtLWuY
```

Example 3 (unknown):
```unknown
{  "id": "re_1Nispe2eZvKYlo2Cd31jOCgZ",  "object": "refund",  "amount": 1000,  "balance_transaction": "txn_1Nispe2eZvKYlo2CYezqFhEx",  "charge": "ch_1NirD82eZvKYlo2CIvbtLWuY",  "created": 1692942318,  "currency": "usd",  "destination_details": {    "card": {      "reference": "123456789012",      "reference_status": "available",      "reference_type": "acquirer_reference_number",      "type": "refund"    },    "type": "card"  },  "metadata": {},  "payment_intent": "pi_1GszsK2eZvKYlo2CfhZyoZLp",  "reason": null,  "receipt_number": null,  "source_transfer_reversal": null,  "status": "succeeded",  "transfer_reversal": null}
```

Example 4 (unknown):
```unknown
{  "id": "re_1Nispe2eZvKYlo2Cd31jOCgZ",  "object": "refund",  "amount": 1000,  "balance_transaction": "txn_1Nispe2eZvKYlo2CYezqFhEx",  "charge": "ch_1NirD82eZvKYlo2CIvbtLWuY",  "created": 1692942318,  "currency": "usd",  "destination_details": {    "card": {      "reference": "123456789012",      "reference_status": "available",      "reference_type": "acquirer_reference_number",      "type": "refund"    },    "type": "card"  },  "metadata": {},  "payment_intent": "pi_1GszsK2eZvKYlo2CfhZyoZLp",  "reason": null,  "receipt_number": null,  "source_transfer_reversal": null,  "status": "succeeded",  "transfer_reversal": null}
```

---

## The Refund object

**URL:** https://docs.stripe.com/api/refunds/object

**Contents:**
- The Refund object
  - Attributes
    - idstring
    - amountinteger
    - chargenullable stringExpandable
    - currencyenum
    - descriptionnullable string
    - metadatanullable object
    - payment_intentnullable stringExpandable
    - reasonnullable enum

Unique identifier for the object.

ID of the charge that’s refunded.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

An arbitrary string attached to the object. You can use this for displaying to users (available on non-card refunds only).

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

ID of the PaymentIntent that’s refunded.

Reason for the refund, which is either user-provided (duplicate, fraudulent, or requested_by_customer) or generated by Stripe internally (expired_uncaptured_charge).

Status of the refund. This can be pending, requires_action, succeeded, failed, or canceled. Learn more about failed refunds.

When you create a new refund, you must specify a Charge or a PaymentIntent object on which to create it.

Creating a new refund will refund a charge that has previously been created but not yet refunded. Funds will be refunded to the credit or debit card that was originally charged.

You can optionally refund only part of a charge. You can do so multiple times, until the entire charge has been refunded.

Once entirely refunded, a charge can’t be refunded again. This method will raise an error when called on an already-refunded charge, or when trying to refund more money than is left on a charge.

A positive integer in the smallest currency unit representing how much of this charge to refund. Can refund only up to the remaining, unrefunded amount of the charge.

The identifier of the charge to refund.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The identifier of the PaymentIntent to refund.

String indicating the reason for the refund. If set, possible values are duplicate, fraudulent, and requested_by_customer. If you believe the charge to be fraudulent, specifying fraudulent as the reason will add the associated card and email to your block lists, and will also help us improve our fraud detection algorithms.

Returns the Refund object if the refund succeeded. Raises an error if the Charge/PaymentIntent has already been refunded, or if an invalid identifier was provided.

Updates the refund that you specify by setting the values of the passed parameters. Any parameters that you don’t provide remain unchanged.

This request only accepts metadata as an argument.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the refund object if the update succeeds. This call raises an error if update parameters are invalid.

Retrieves the details of an existing refund.

Returns a refund if you provide a valid ID. Raises an error otherwise.

Returns a list of all refunds you created. We return the refunds in sorted order, with the most recent refunds appearing first. The 10 most recent refunds are always available by default on the Charge object.

Only return refunds for the charge specified by this charge ID.

Only return refunds for the PaymentIntent specified by this ID.

A dictionary with a data property that contains an array of up to limit refunds, starting after the starting_after refund. Each entry in the array is a separate Refund object. If no other refunds are available, the resulting array is empty. If you provide a non-existent charge ID, this call raises an error.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "re_1Nispe2eZvKYlo2Cd31jOCgZ",  "object": "refund",  "amount": 1000,  "balance_transaction": "txn_1Nispe2eZvKYlo2CYezqFhEx",  "charge": "ch_1NirD82eZvKYlo2CIvbtLWuY",  "created": 1692942318,  "currency": "usd",  "destination_details": {    "card": {      "reference": "123456789012",      "reference_status": "available",      "reference_type": "acquirer_reference_number",      "type": "refund"    },    "type": "card"  },  "metadata": {},  "payment_intent": "pi_1GszsK2eZvKYlo2CfhZyoZLp",  "reason": null,  "receipt_number": null,  "source_transfer_reversal": null,  "status": "succeeded",  "transfer_reversal": null}
```

Example 2 (unknown):
```unknown
{  "id": "re_1Nispe2eZvKYlo2Cd31jOCgZ",  "object": "refund",  "amount": 1000,  "balance_transaction": "txn_1Nispe2eZvKYlo2CYezqFhEx",  "charge": "ch_1NirD82eZvKYlo2CIvbtLWuY",  "created": 1692942318,  "currency": "usd",  "destination_details": {    "card": {      "reference": "123456789012",      "reference_status": "available",      "reference_type": "acquirer_reference_number",      "type": "refund"    },    "type": "card"  },  "metadata": {},  "payment_intent": "pi_1GszsK2eZvKYlo2CfhZyoZLp",  "reason": null,  "receipt_number": null,  "source_transfer_reversal": null,  "status": "succeeded",  "transfer_reversal": null}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/refunds \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d charge=ch_1NirD82eZvKYlo2CIvbtLWuY
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/refunds \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d charge=ch_1NirD82eZvKYlo2CIvbtLWuY
```

---

## The PaymentIntent object

**URL:** https://docs.stripe.com/api/payment_intents/object

**Contents:**
- The PaymentIntent object
  - Attributes
    - idstringretrievable with publishable key
    - amountintegerretrievable with publishable key
    - automatic_payment_methodsnullable objectretrievable with publishable key
    - client_secretnullable stringretrievable with publishable key
    - currencyenumretrievable with publishable key
    - customernullable stringExpandable
    - customer_accountnullable string
    - descriptionnullable stringretrievable with publishable key

Unique identifier for the object.

Amount intended to be collected by this PaymentIntent. A positive integer representing how much to charge in the smallest currency unit (e.g., 100 cents to charge $1.00 or 100 to charge ¥100, a zero-decimal currency). The minimum amount is $0.50 US or equivalent in charge currency. The amount value supports up to eight digits (e.g., a value of 99999999 for a USD charge of $999,999.99).

Settings to configure compatible payment methods from the Stripe Dashboard

The client secret of this PaymentIntent. Used for client-side retrieval using a publishable key.

The client secret can be used to complete a payment from your frontend. It should not be stored, logged, or exposed to anyone other than the customer. Make sure that you have TLS enabled on any page that includes the client secret.

Refer to our docs to accept a payment and learn about how client_secret should be handled.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

ID of the Customer this PaymentIntent belongs to, if one exists.

Payment methods attached to other Customers cannot be used with this PaymentIntent.

If setup_future_usage is set and this PaymentIntent’s payment method is not card_present, then the payment method attaches to the Customer after the PaymentIntent has been confirmed and any required actions from the user are complete. If the payment method is card_present and isn’t a digital wallet, then a generated_card payment method representing the card is created and attached to the Customer instead.

ID of the Account representing the customer that this PaymentIntent belongs to, if one exists.

Payment methods attached to other Accounts cannot be used with this PaymentIntent.

If setup_future_usage is set and this PaymentIntent’s payment method is not card_present, then the payment method attaches to the Account after the PaymentIntent has been confirmed and any required actions from the user are complete. If the payment method is card_present and isn’t a digital wallet, then a generated_card payment method representing the card is created and attached to the Account instead.

An arbitrary string attached to the object. Often useful for displaying to users.

The payment error encountered in the previous PaymentIntent confirmation. It will be cleared if the PaymentIntent is later updated for any reason.

ID of the latest Charge object created by this PaymentIntent. This property is null until PaymentIntent confirmation is attempted.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Learn more about storing information in metadata.

If present, this property tells you what actions you need to take in order for your customer to fulfill a payment using the provided source.

ID of the payment method used in this PaymentIntent.

Email address that the receipt for the resulting payment will be sent to. If receipt_email is specified for a payment in live mode, a receipt will be sent regardless of your email settings.

Indicates that you intend to make future payments with this PaymentIntent’s payment method.

If you provide a Customer with the PaymentIntent, you can use this parameter to attach the payment method to the Customer after the PaymentIntent is confirmed and the customer completes any required actions. If you don’t provide a Customer, you can still attach the payment method to a Customer after the transaction completes.

If the payment method is card_present and isn’t a digital wallet, Stripe creates and attaches a generated_card payment method representing the card to the Customer instead.

When processing card payments, Stripe uses setup_future_usage to help you comply with regional legislation and network rules, such as SCA.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

Shipping information for this PaymentIntent.

Text that appears on the customer’s statement as the statement descriptor for a non-card charge. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

Setting this value for a card charge returns an error. For card charges, set the statement_descriptor_suffix instead.

Provides information about a card charge. Concatenated to the account’s statement descriptor prefix to form the complete statement descriptor that appears on the customer’s statement.

Status of this PaymentIntent, one of requires_payment_method, requires_confirmation, requires_action, processing, requires_capture, canceled, or succeeded. Read more about each PaymentIntent status.

The PaymentIntent has been canceled.

The PaymentIntent is currently being processed.

The PaymentIntent requires additional action from the customer.

The PaymentIntent has been confirmed and requires capture.

The PaymentIntent requires confirmation.

The PaymentIntent requires a payment method to be attached.

The PaymentIntent has succeeded.

Creates a PaymentIntent object.

After the PaymentIntent is created, attach a payment method and confirm to continue the payment. Learn more about the available payment flows with the Payment Intents API.

When you use confirm=true during creation, it’s equivalent to creating and confirming the PaymentIntent in the same call. You can use any parameters available in the confirm API when you supply confirm=true.

Amount intended to be collected by this PaymentIntent. A positive integer representing how much to charge in the smallest currency unit (e.g., 100 cents to charge $1.00 or 100 to charge ¥100, a zero-decimal currency). The minimum amount is $0.50 US or equivalent in charge currency. The amount value supports up to eight digits (e.g., a value of 99999999 for a USD charge of $999,999.99).

Three-letter ISO currency code, in lowercase. Must be a supported currency.

When you enable this parameter, this PaymentIntent accepts payment methods that you enable in the Dashboard and that are compatible with this PaymentIntent’s other parameters.

Set to true to attempt to confirm this PaymentIntent immediately. This parameter defaults to false. When creating and confirming a PaymentIntent at the same time, you can also provide the parameters available in the Confirm API.

ID of the Customer this PaymentIntent belongs to, if one exists.

Payment methods attached to other Customers cannot be used with this PaymentIntent.

If setup_future_usage is set and this PaymentIntent’s payment method is not card_present, then the payment method attaches to the Customer after the PaymentIntent has been confirmed and any required actions from the user are complete. If the payment method is card_present and isn’t a digital wallet, then a generated_card payment method representing the card is created and attached to the Customer instead.

ID of the Account representing the customer that this PaymentIntent belongs to, if one exists.

Payment methods attached to other Accounts cannot be used with this PaymentIntent.

If setup_future_usage is set and this PaymentIntent’s payment method is not card_present, then the payment method attaches to the Account after the PaymentIntent has been confirmed and any required actions from the user are complete. If the payment method is card_present and isn’t a digital wallet, then a generated_card payment method representing the card is created and attached to the Account instead.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Set to true to indicate that the customer isn’t in your checkout flow during this payment attempt and can’t authenticate. Use this parameter in scenarios where you collect card details and charge them later. This parameter can only be used with confirm=true.

ID of the payment method (a PaymentMethod, Card, or compatible Source object) to attach to this PaymentIntent.

If you omit this parameter with confirm=true, customer.default_source attaches as this PaymentIntent’s payment instrument to improve migration for users of the Charges API. We recommend that you explicitly provide the payment_method moving forward. If the payment method is attached to a Customer, you must also provide the ID of that Customer as the customer parameter of this PaymentIntent.

Email address to send the receipt to. If you specify receipt_email for a payment in live mode, you send a receipt regardless of your email settings.

Indicates that you intend to make future payments with this PaymentIntent’s payment method.

If you provide a Customer with the PaymentIntent, you can use this parameter to attach the payment method to the Customer after the PaymentIntent is confirmed and the customer completes any required actions. If you don’t provide a Customer, you can still attach the payment method to a Customer after the transaction completes.

If the payment method is card_present and isn’t a digital wallet, Stripe creates and attaches a generated_card payment method representing the card to the Customer instead.

When processing card payments, Stripe uses setup_future_usage to help you comply with regional legislation and network rules, such as SCA.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

Shipping information for this PaymentIntent.

Text that appears on the customer’s statement as the statement descriptor for a non-card charge. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

Setting this value for a card charge returns an error. For card charges, set the statement_descriptor_suffix instead.

Provides information about a card charge. Concatenated to the account’s statement descriptor prefix to form the complete statement descriptor that appears on the customer’s statement.

Returns a PaymentIntent object.

Updates properties on a PaymentIntent object without confirming.

Depending on which properties you update, you might need to confirm the PaymentIntent again. For example, updating the payment_method always requires you to confirm the PaymentIntent again. If you prefer to update and confirm at the same time, we recommend updating properties through the confirm API instead.

Amount intended to be collected by this PaymentIntent. A positive integer representing how much to charge in the smallest currency unit (e.g., 100 cents to charge $1.00 or 100 to charge ¥100, a zero-decimal currency). The minimum amount is $0.50 US or equivalent in charge currency. The amount value supports up to eight digits (e.g., a value of 99999999 for a USD charge of $999,999.99).

Three-letter ISO currency code, in lowercase. Must be a supported currency.

ID of the Customer this PaymentIntent belongs to, if one exists.

Payment methods attached to other Customers cannot be used with this PaymentIntent.

If setup_future_usage is set and this PaymentIntent’s payment method is not card_present, then the payment method attaches to the Customer after the PaymentIntent has been confirmed and any required actions from the user are complete. If the payment method is card_present and isn’t a digital wallet, then a generated_card payment method representing the card is created and attached to the Customer instead.

ID of the Account representing the customer that this PaymentIntent belongs to, if one exists.

Payment methods attached to other Accounts cannot be used with this PaymentIntent.

If setup_future_usage is set and this PaymentIntent’s payment method is not card_present, then the payment method attaches to the Account after the PaymentIntent has been confirmed and any required actions from the user are complete. If the payment method is card_present and isn’t a digital wallet, then a generated_card payment method representing the card is created and attached to the Account instead.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

ID of the payment method (a PaymentMethod, Card, or compatible Source object) to attach to this PaymentIntent. To unset this field to null, pass in an empty string.

Email address that the receipt for the resulting payment will be sent to. If receipt_email is specified for a payment in live mode, a receipt will be sent regardless of your email settings.

Indicates that you intend to make future payments with this PaymentIntent’s payment method.

If you provide a Customer with the PaymentIntent, you can use this parameter to attach the payment method to the Customer after the PaymentIntent is confirmed and the customer completes any required actions. If you don’t provide a Customer, you can still attach the payment method to a Customer after the transaction completes.

If the payment method is card_present and isn’t a digital wallet, Stripe creates and attaches a generated_card payment method representing the card to the Customer instead.

When processing card payments, Stripe uses setup_future_usage to help you comply with regional legislation and network rules, such as SCA.

If you’ve already set setup_future_usage and you’re performing a request using a publishable key, you can only update the value from on_session to off_session.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

Shipping information for this PaymentIntent.

Text that appears on the customer’s statement as the statement descriptor for a non-card charge. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

Setting this value for a card charge returns an error. For card charges, set the statement_descriptor_suffix instead.

Provides information about a card charge. Concatenated to the account’s statement descriptor prefix to form the complete statement descriptor that appears on the customer’s statement.

Returns a PaymentIntent object.

Retrieves the details of a PaymentIntent that has previously been created.

You can retrieve a PaymentIntent client-side using a publishable key when the client_secret is in the query string.

If you retrieve a PaymentIntent with a publishable key, it only returns a subset of properties. Refer to the payment intent object reference for more details.

The client secret of the PaymentIntent. We require it if you use a publishable key to retrieve the source.

Returns a PaymentIntent if a valid identifier was provided.

Lists all LineItems of a given PaymentIntent.

A dictionary with a data property that contains an array of up to limit line items of the given PaymentIntent, starting after line item starting_after. Each entry in the array is a separate line item object. If no other line items are available, the resulting array is empty.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",  "object": "payment_intent",  "amount": 2000,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 0,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": {    "enabled": true  },  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",  "confirmation_method": "automatic",  "created": 1680800504,  "currency": "usd",  "customer": null,  "description": null,  "last_payment_error": null,  "latest_charge": null,  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": null,  "payment_method_options": {    "card": {      "installments": null,      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    },    "link": {      "persistent_token": null    }  },  "payment_method_types": [    "card",    "link"  ],  "processing": null,  "receipt_email": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "source": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "requires_payment_method",  "transfer_data": null,  "transfer_group": null}
```

Example 2 (unknown):
```unknown
{  "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",  "object": "payment_intent",  "amount": 2000,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 0,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": {    "enabled": true  },  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",  "confirmation_method": "automatic",  "created": 1680800504,  "currency": "usd",  "customer": null,  "description": null,  "last_payment_error": null,  "latest_charge": null,  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": null,  "payment_method_options": {    "card": {      "installments": null,      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    },    "link": {      "persistent_token": null    }  },  "payment_method_types": [    "card",    "link"  ],  "processing": null,  "receipt_email": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "source": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "requires_payment_method",  "transfer_data": null,  "transfer_group": null}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=2000 \  -d currency=usd \  -d "automatic_payment_methods[enabled]"=true
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=2000 \  -d currency=usd \  -d "automatic_payment_methods[enabled]"=true
```

---

## Top-ups

**URL:** https://docs.stripe.com/api/topups

**Contents:**
- Top-ups
- The Top-up object
  - Attributes
    - idstring
    - amountinteger
    - currencystring
    - descriptionnullable string
    - metadataobject
    - statusenum
  - More attributesExpand all

To top up your Stripe balance, you create a top-up object. You can retrieve individual top-ups, as well as list all top-ups. Top-ups are identified by a unique, random ID.

Related guide: Topping up your platform account

Unique identifier for the object.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The status of the top-up is either canceled, failed, pending, reversed, or succeeded.

Top up the balance of an account

A positive integer representing how much to transfer.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the top-up object.

Updates the metadata of a top-up. Other top-up details are not editable by design.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The newly updated top-up object if the call succeeded. Otherwise, this call raises an error.

Retrieves the details of a top-up that has previously been created. Supply the unique top-up ID that was returned from your previous request, and Stripe will return the corresponding top-up information.

Returns a top-up if a valid identifier was provided, and raises an error otherwise.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "tu_1NG6yj2eZvKYlo2C1FOBiHya",  "object": "topup",  "amount": 2000,  "balance_transaction": null,  "created": 123456789,  "currency": "usd",  "description": "Top-up for Jenny Rosen",  "expected_availability_date": 123456789,  "failure_code": null,  "failure_message": null,  "livemode": false,  "source": null,  "statement_descriptor": "Top-up",  "status": "pending",  "transfer_group": null}
```

Example 2 (unknown):
```unknown
{  "id": "tu_1NG6yj2eZvKYlo2C1FOBiHya",  "object": "topup",  "amount": 2000,  "balance_transaction": null,  "created": 123456789,  "currency": "usd",  "description": "Top-up for Jenny Rosen",  "expected_availability_date": 123456789,  "failure_code": null,  "failure_message": null,  "livemode": false,  "source": null,  "statement_descriptor": "Top-up",  "status": "pending",  "transfer_group": null}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/topups \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=2000 \  -d currency=usd \  -d description="Top-up for Jenny Rosen" \  -d statement_descriptor=Top-up
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/topups \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=2000 \  -d currency=usd \  -d description="Top-up for Jenny Rosen" \  -d statement_descriptor=Top-up
```

---

## API v2 overview

**URL:** https://docs.stripe.com/api-v2-overview

**Contents:**
- API v2 overview
- Understand the behavior of APIs in the v2 namespace.
- Key differences between the v1 and v2 namespace
- SDKs that support API v2
  - Using API v2 with the Stripe CLI
- SDK, CLI, and API versioning
    - Include Stripe-Version without SDK or CLI
- Using APIs from the v1 and v2 namespaces in the same integration
- List pagination
- Idempotency

The Stripe API provides two namespaces that contain different sets of endpoints:

Test your integration

Validate APIs in the /v1 namespace using Sandboxes, an isolated environment. Additionally, you can use test mode to test your integration.

Validate APIs in the /v2 namespace using Sandboxes, an isolated environment. Test mode is unsupported.

Send idempotent requests

When providing the Idempotency-Key header with a unique identifier, if the API already processed the request, it returns the previously stored request.

When providing the Idempotency-Key header with a unique identifier, the API retries any failed requests without producing side effects (any extraneous change or observable behavior that occurs as a result of an API call).

Read more: Idempotency

Receive events from Stripe

Most events emitted from APIs in the /v1 namespace include a snapshot of an API object in their payload. Some APIs in the /v1 namespace generate thin events, which include a minimal, unversioned push payload.

Events emitted from APIs in the /v2 namespace are thin events.

Read more: Event destinations

Paginating through a list

Specify an object’s ID as the starting element for list API requests. Use the starting_after, ending_before, and has_more properties from the API response to paginate through a list.

Specify the page token for list API requests. Use the previous_page_url and next_page_url properties in the API response to paginate through a list.

Read more: List pagination

Fetch additional data with expansion

Use the expand parameter to replace IDs for related API objects with fully-expanded child objects.

Read more: Expanding responses

The expand parameter isn’t supported. Some APIs in this namespace might provide additional fields in their responses by using the include parameter.

All server-side SDKs support APIs in the /v2 namespace.

Use stripe trigger and stripe listen to test your integration’s event handling. You can’t access APIs in the /v2 namespace using the Stripe CLI.

SDKs and the Stripe CLI automatically include an API version for all requests. After you update your SDK or CLI version, Stripe simultaneously updates the API version of your requests and responses.

All API requests to the API /v2 namespace must include the Stripe-Version header to specify the underlying API version.

For example, a curl request using API version 2024-09-30.acacia looks like:

You can use any combination of APIs in the /v1 or /v2 namespace in the same integration.

If you’re not using an official SDK or the CLI, always include the namespace in the URL path for your API calls. For example:

APIs within the /v2 namespace (for example, GET /v2/core/event_destinations) contain a different pagination interface compared to those in the /v1 namespace.

You can use these URLs to make requests without using our SDKs. Conversely, when you use our SDKs, you don’t need to use these URLs because the SDKs handle auto-pagination automatically.

You can’t change list filters after the first request.

APIs in the /v2 namespace provide improved support for idempotency behavior, preventing unintended side effects when requests are performed multiple times using the same idempotency key. When the API receives two requests with the same idempotency key:

Two requests are considered idempotent if the following are all true:

To specify an idempotency key, use the Idempotency-Key header and provide a unique value to represent the operation (we recommend a UUID). If no key is provided, Stripe automatically generates a UUID for you.

All POST and DELETE API v2 requests accept idempotency keys and behave idempotently. GET requests are idempotent by definition, so sending an idempotency key has no effect.

API v1 and API v2 idempotency have a few key differences:

Using the SDK, provide an idempotency key with the idempotencyKey property in API requests.

For example, to make an API request with a specific idempotency key:

If you’re not using a SDK or the CLI, requests can include the Idempotency-Key header:

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v2/core/event_destinations \
  -H "Authorization: Bearer {{YOUR_API_KEY}}" \
  -H "Stripe-Version: 2024-09-30.acacia" \
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v2/core/event_destinations \
  -H "Authorization: Bearer {{YOUR_API_KEY}}" \
  -H "Stripe-Version: 2024-09-30.acacia" \
```

Example 3 (unknown):
```unknown
import com.stripe.StripeClient;

StripeClient stripe = new StripeClient("{{YOUR_API_KEY}}");

// Call a v2 API
EventDestination eventDestination = stripe.v2().core().eventDestinations().retrieve("ed_123");

// Call a v1 API
Customer customer = stripe.customers().retrieve("cus_123");
```

Example 4 (unknown):
```unknown
import com.stripe.StripeClient;

StripeClient stripe = new StripeClient("{{YOUR_API_KEY}}");

// Call a v2 API
EventDestination eventDestination = stripe.v2().core().eventDestinations().retrieve("ed_123");

// Call a v1 API
Customer customer = stripe.customers().retrieve("cus_123");
```

---

## Idempotent requests

**URL:** https://docs.stripe.com/api/idempotent_requests

**Contents:**
- Idempotent requests
- Include-dependent response values (API v2)
- Metadata
- Sample metadata use cases
- Pagination
  - Parameters
    - limitoptional, default is 10
    - starting_afteroptional object ID
    - ending_beforeoptional object ID
  - List Response Format

The API supports idempotency for safely retrying requests without accidentally performing the same operation twice. When creating or updating an object, use an idempotency key. Then, if a connection error occurs, you can safely repeat the request without risk of creating a second object or performing the update twice.

To perform an idempotent request, provide an additional IdempotencyKey element to the request options.

Stripe’s idempotency works by saving the resulting status code and body of the first request made for any given idempotency key, regardless of whether it succeeds or fails. Subsequent requests with the same key return the same result, including 500 errors.

A client generates an idempotency key, which is a unique key that the server uses to recognize subsequent retries of the same request. How you create unique keys is up to you, but we suggest using V4 UUIDs, or another random string with enough entropy to avoid collisions. Idempotency keys are up to 255 characters long.

You can remove keys from the system automatically after they’re at least 24 hours old. We generate a new request if a key is reused after the original is pruned. The idempotency layer compares incoming parameters to those of the original request and errors if they’re not the same to prevent accidental misuse.

We save results only after the execution of an endpoint begins. If incoming parameters fail validation, or the request conflicts with another request that’s executing concurrently, we don’t save the idempotent result because no API endpoint initiates the execution. You can retry these requests. Learn more about when you can retry idempotent requests.

All POST requests accept idempotency keys. Don’t send idempotency keys in GET and DELETE requests because it has no effect. These requests are idempotent by definition.

Some API v2 responses contain null values for certain properties by default, regardless of their actual values. That reduces the size of response payloads while maintaining the basic response structure. To retrieve the actual values for those properties, specify them in the include array request parameter.

To determine whether you need to use the include parameter in a given request, look at the request description. The include parameter’s enum values represent the response properties that depend on the include parameter.

Whether a response property defaults to null depends on the request endpoint, not the object that the endpoint references. If multiple endpoints return data from the same object, a particular property can depend on include in one endpoint and return its actual value by default for a different endpoint.

A hash property can depend on a single include value, or on multiple include values associated with its child properties. For example, when updating an Account, to return actual values for the entire identity hash, specify identity in the include parameter. Otherwise, the identity hash is null in the response. However, to return actual values for the configuration hash, you must specify individual configurations in the request. If you specify at least one configuration, but not all of them, specified configurations return actual values and unspecified configurations return null. If you don’t specify any configurations, the configuration hash is null in the response.

The response includes actual values for the properties specified in the include parameter, and null for all other include-dependent properties.

Updateable Stripe objects—including Account, Charge, Customer, PaymentIntent, Refund, Subscription, and Transfer have a metadata parameter. You can use this parameter to attach key-value data to these Stripe objects.

You can specify up to 50 keys, with key names up to 40 characters long and values up to 500 characters long. Keys and values are stored as strings and can contain any characters with one exception: you can’t use square brackets ([ and ]) in keys.

You can use metadata to store additional, structured information on an object. For example, you could store your user’s full name and corresponding unique identifier from your system on a Stripe Customer object. Stripe doesn’t use metadata—for example, we don’t use it to authorize or decline a charge and it won’t be seen by your users unless you choose to show it to them.

Some of the objects listed above also support a description parameter. You can use the description parameter to annotate a charge-for example, a human-readable description such as 2 shirts for test@example.com. Unlike metadata, description is a single string, which your users might see (for example, in email receipts Stripe sends on your behalf).

Don’t store any sensitive information (bank account numbers, card details, and so on) as metadata or in the description parameter.

All top-level API resources have support for bulk fetches through “list” API methods. For example, you can list charges, list customers, and list invoices. These list API methods share a common structure and accept, at a minimum, the following three parameters: limit, starting_after, and ending_before.

Stripe’s list API methods use cursor-based pagination through the starting_after and ending_before parameters. Both parameters accept an existing object ID value (see below) and return objects in reverse chronological order. The ending_before parameter returns objects listed before the named object. The starting_after parameter returns objects listed after the named object. These parameters are mutually exclusive. You can use either the starting_after or ending_before parameter, but not both simultaneously.

Our client libraries offer auto-pagination helpers to traverse all pages of a list.

This specifies a limit on the number of objects to return, ranging between 1 and 100.

A cursor to use in pagination. starting_after is an object ID that defines your place in the list. For example, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include starting_after=obj_foo to fetch the next page of the list.

A cursor to use in pagination. ending_before is an object ID that defines your place in the list. For example, if you make a list request and receive 100 objects, starting with obj_bar, your subsequent call can include ending_before=obj_bar to fetch the previous page of the list.

A string that provides a description of the object type that returns.

An array containing the actual response elements, paginated by any request parameters.

Whether or not there are more elements available after this set. If false, this set comprises the end of the list.

The URL for accessing this list.

APIs within the /v2 namespace contain a different pagination interface than the v1 namespace.

Some top-level API resource have support for retrieval via “search” API methods. For example, you can search charges, search customers, and search subscriptions.

Stripe’s search API methods utilize cursor-based pagination via the page request parameter and next_page response parameter. For example, if you make a search request and receive "next_page": "pagination_key" in the response, your subsequent call can include page=pagination_key to fetch the next page of results.

Our client libraries offer auto-pagination helpers to easily traverse all pages of a search result.

The search query string. See search query language.

A limit on the number of objects returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A string describing the object type returned.

The URL for accessing this list.

Whether or not there are more elements available after this set. If false, this set comprises the end of the list.

An array containing the actual response elements, paginated by any request parameters.

A cursor for use in pagination. If has_more is true, you can pass the value of next_page to a subsequent call to fetch the next page of results.

The total number of objects that match the query, only accurate up to 10,000. This field isn’t included by default. To include it in the response, expand the total_count field.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/customers \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -H "Idempotency-Key: KG5LxwFBepaKHyUD" \  -d description="My First Test Customer (created for API docs at https://docs.stripe.com/api)"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/customers \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -H "Idempotency-Key: KG5LxwFBepaKHyUD" \  -d description="My First Test Customer (created for API docs at https://docs.stripe.com/api)"
```

Example 3 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "include": [        "identity",        "configuration.customer"    ]  }'
```

Example 4 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "include": [        "identity",        "configuration.customer"    ]  }'
```

---

## Create a PaymentMethod

**URL:** https://docs.stripe.com/api/payment_methods/create

**Contents:**
- Create a PaymentMethod
  - Parameters
    - typeenumRequired
    - billing_detailsobject
    - metadataobject
  - More parametersExpand all
    - acss_debitobject
    - affirmobject
    - afterpay_clearpayobject
    - alipayobject

Creates a PaymentMethod object. Read the Stripe.js reference to learn how to create PaymentMethods via Stripe.js.

Instead of creating a PaymentMethod directly, we recommend using the PaymentIntents API to accept a payment immediately or the SetupIntent API to collect payment method details ahead of a future payment.

The type of the PaymentMethod. An additional hash is included on the PaymentMethod with a name matching this value. It contains additional information specific to the PaymentMethod type.

Pre-authorized debit payments are used to debit Canadian bank accounts through the Automated Clearing Settlement System (ACSS).

Affirm is a buy now, pay later payment method in the US.

Afterpay / Clearpay is a buy now, pay later payment method used in Australia, Canada, France, New Zealand, Spain, the UK, and the US.

Alipay is a digital wallet payment method used in China.

Alma is a Buy Now, Pay Later payment method that lets customers pay in 2, 3, or 4 installments.

Amazon Pay is a Wallet payment method that lets hundreds of millions of Amazon customers pay their way, every day.

BECS Direct Debit is used to debit Australian bank accounts through the Bulk Electronic Clearing System (BECS).

Bacs Direct Debit is used to debit UK bank accounts.

Bancontact is a bank redirect payment method used in Belgium.

Billie is a payment method.

Billing information associated with the PaymentMethod that may be used or required by particular types of payment methods.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a PaymentMethod object.

Updates a PaymentMethod object. A PaymentMethod must be attached to a customer to be updated.

Billing information associated with the PaymentMethod that may be used or required by particular types of payment methods.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a PaymentMethod object.

Retrieves a PaymentMethod object for a given Customer.

Returns a PaymentMethod object.

Retrieves a PaymentMethod object attached to the StripeAccount. To retrieve a payment method attached to a Customer, you should use Retrieve a Customer’s PaymentMethods

Returns a PaymentMethod object.

Returns a list of PaymentMethods for a given Customer

An optional filter on the list, based on the object type field. Without the filter, the list includes all current and future payment method types. If your integration expects only one type of payment method in the response, make sure to provide a type value in the request.

A dictionary with a data property that contains an array of up to limit PaymentMethods of type type, starting after PaymentMethods starting_after. Each entry in the array is a separate PaymentMethod object. If no more PaymentMethods are available, the resulting array will be empty.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_methods \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d type=us_bank_account \  -d "us_bank_account[account_holder_type]"=individual \  -d "us_bank_account[account_number]"=000123456789 \  -d "us_bank_account[routing_number]"=110000000 \  -d "billing_details[name]"="John Doe"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_methods \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d type=us_bank_account \  -d "us_bank_account[account_holder_type]"=individual \  -d "us_bank_account[account_number]"=000123456789 \  -d "us_bank_account[routing_number]"=110000000 \  -d "billing_details[name]"="John Doe"
```

Example 3 (unknown):
```unknown
{  "id": "pm_1Q0PsIJvEtkwdCNYMSaVuRz6",  "object": "payment_method",  "allow_redisplay": "unspecified",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": "John Doe",    "phone": null  },  "created": 1726673582,  "customer": null,  "livemode": false,  "metadata": {},  "type": "us_bank_account",  "us_bank_account": {    "account_holder_type": "individual",    "account_type": "checking",    "bank_name": "STRIPE TEST BANK",    "financial_connections_account": null,    "fingerprint": "LstWJFsCK7P349Bg",    "last4": "6789",    "networks": {      "preferred": "ach",      "supported": [        "ach"      ]    },    "routing_number": "110000000",    "status_details": {}  }}
```

Example 4 (unknown):
```unknown
{  "id": "pm_1Q0PsIJvEtkwdCNYMSaVuRz6",  "object": "payment_method",  "allow_redisplay": "unspecified",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": "John Doe",    "phone": null  },  "created": 1726673582,  "customer": null,  "livemode": false,  "metadata": {},  "type": "us_bank_account",  "us_bank_account": {    "account_holder_type": "individual",    "account_type": "checking",    "bank_name": "STRIPE TEST BANK",    "financial_connections_account": null,    "fingerprint": "LstWJFsCK7P349Bg",    "last4": "6789",    "networks": {      "preferred": "ach",      "supported": [        "ach"      ]    },    "routing_number": "110000000",    "status_details": {}  }}
```

---

## Payment Link

**URL:** https://docs.stripe.com/api/payment-link

**Contents:**
- Payment Link
- The Payment Link object
  - Attributes
    - idstring
    - activeboolean
    - line_itemsobjectExpandable
    - metadataobject
    - urlstring
  - More attributesExpand all
    - objectstring

A payment link is a shareable URL that will take your customers to a hosted payment page. A payment link can be shared and used multiple times.

When a customer opens a payment link it will open a new checkout session to render the payment page. You can use checkout session events to track payments through payment links.

Related guide: Payment Links API

Unique identifier for the object.

Whether the payment link’s url is active. If false, customers visiting the URL will be shown a page saying that the link has been deactivated.

The line items representing what is being sold.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The public URL that can be shared with customers.

Creates a payment link.

The line items representing what is being sold. Each line item represents an item being sold. Up to 20 line items are supported.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata. Metadata associated with this Payment Link will automatically be copied to checkout sessions created by this payment link.

Returns the payment link.

Updates a payment link.

Whether the payment link’s url is active. If false, customers visiting the URL will be shown a page saying that the link has been deactivated.

The line items representing what is being sold. Each line item represents an item being sold. Up to 20 line items are supported.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata. Metadata associated with this Payment Link will automatically be copied to checkout sessions created by this payment link.

Updated payment link.

When retrieving a payment link, there is an includable line_items property containing the first handful of those items. There is also a URL where you can retrieve the full (paginated) list of line items.

A dictionary with a data property that contains an array of up to limit payment link line items, starting after Line Item starting_after. Each entry in the array is a separate Line Item object. If no more line items are available, the resulting array will be empty.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "plink_1MoC3ULkdIwHu7ixZjtGpVl2",  "object": "payment_link",  "active": true,  "after_completion": {    "hosted_confirmation": {      "custom_message": null    },    "type": "hosted_confirmation"  },  "allow_promotion_codes": false,  "application_fee_amount": null,  "application_fee_percent": null,  "automatic_tax": {    "enabled": false,    "liability": null  },  "billing_address_collection": "auto",  "consent_collection": null,  "currency": "usd",  "custom_fields": [],  "custom_text": {    "shipping_address": null,    "submit": null  },  "customer_creation": "if_required",  "invoice_creation": {    "enabled": false,    "invoice_data": {      "account_tax_ids": null,      "custom_fields": null,      "description": null,      "footer": null,      "issuer": null,      "metadata": {},      "rendering_options": null    }  },  "livemode": false,  "metadata": {},  "on_behalf_of": null,  "payment_intent_data": null,  "payment_method_collection": "always",  "payment_method_types": null,  "phone_number_collection": {    "enabled": false  },  "shipping_address_collection": null,  "shipping_options": [],  "submit_type": "auto",  "subscription_data": {    "description": null,    "invoice_settings": {      "issuer": {        "type": "self"      }    },    "trial_period_days": null  },  "tax_id_collection": {    "enabled": false  },  "transfer_data": null,  "url": "https://buy.stripe.com/test_cN25nr0iZ7bUa7meUY"}
```

Example 2 (unknown):
```unknown
{  "id": "plink_1MoC3ULkdIwHu7ixZjtGpVl2",  "object": "payment_link",  "active": true,  "after_completion": {    "hosted_confirmation": {      "custom_message": null    },    "type": "hosted_confirmation"  },  "allow_promotion_codes": false,  "application_fee_amount": null,  "application_fee_percent": null,  "automatic_tax": {    "enabled": false,    "liability": null  },  "billing_address_collection": "auto",  "consent_collection": null,  "currency": "usd",  "custom_fields": [],  "custom_text": {    "shipping_address": null,    "submit": null  },  "customer_creation": "if_required",  "invoice_creation": {    "enabled": false,    "invoice_data": {      "account_tax_ids": null,      "custom_fields": null,      "description": null,      "footer": null,      "issuer": null,      "metadata": {},      "rendering_options": null    }  },  "livemode": false,  "metadata": {},  "on_behalf_of": null,  "payment_intent_data": null,  "payment_method_collection": "always",  "payment_method_types": null,  "phone_number_collection": {    "enabled": false  },  "shipping_address_collection": null,  "shipping_options": [],  "submit_type": "auto",  "subscription_data": {    "description": null,    "invoice_settings": {      "issuer": {        "type": "self"      }    },    "trial_period_days": null  },  "tax_id_collection": {    "enabled": false  },  "transfer_data": null,  "url": "https://buy.stripe.com/test_cN25nr0iZ7bUa7meUY"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_links \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "line_items[0][price]"=price_1MoC3TLkdIwHu7ixcIbKelAC \  -d "line_items[0][quantity]"=1
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_links \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "line_items[0][price]"=price_1MoC3TLkdIwHu7ixcIbKelAC \  -d "line_items[0][quantity]"=1
```

---

## The AccountLink object

**URL:** https://docs.stripe.com/api/v2/core/account-links/object

**Contents:**
- The AccountLink object
  - Attributes
    - objectstring, value is "v2.core.account_link"
    - accountstring
    - createdtimestamp
    - expires_attimestamp
    - livemodeboolean
    - urlstring
    - use_caseobject
- Create an account link v2

String representing the object’s type. Objects of the same type share the same value of the object field.

The ID of the connected account this Account Link applies to.

The timestamp at which this Account Link was created.

The timestamp at which this Account Link will expire.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The URL at which the account can access the Stripe-hosted flow.

Hash containing usage options.

Creates an AccountLink object that includes a single-use URL that an account can use to access a Stripe-hosted flow for collecting or updating required information.

The ID of the Account to create link for.

The use case of the AccountLink.

String representing the object’s type. Objects of the same type share the same value of the object field.

The ID of the connected account this Account Link applies to.

The timestamp at which this Account Link was created.

The timestamp at which this Account Link will expire.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The URL at which the account can access the Stripe-hosted flow.

Hash containing usage options.

Accounts v2 is not enabled for your platform.

Account cannot be onboard via v2/core/account_links without specifying the right configurations.

The resource wasn’t found.

**Examples:**

Example 1 (unknown):
```unknown
{  "object": "v2.core.account_link",  "account": "acct_1Nv0FGQ9RKHgCVdK",  "created": "2025-03-27T17:15:18.000Z",  "expires_at": "2025-03-27T17:25:18.000Z",  "url": "https://accounts.stripe.com/r/acct_1Nv0FGQ9RKHgCVdK#alu_test_61SGhyomRuz7xsw5216SGhyj0ASQdCLwMKdRUF3mi3H6",  "use_case": {    "account_onboarding": {      "configurations": [        "recipient"      ],      "refresh_url": "https://example.com/reauth",      "return_url": "https://example.com/return"    },    "type": "account_onboarding"  }}
```

Example 2 (unknown):
```unknown
{  "object": "v2.core.account_link",  "account": "acct_1Nv0FGQ9RKHgCVdK",  "created": "2025-03-27T17:15:18.000Z",  "expires_at": "2025-03-27T17:25:18.000Z",  "url": "https://accounts.stripe.com/r/acct_1Nv0FGQ9RKHgCVdK#alu_test_61SGhyomRuz7xsw5216SGhyj0ASQdCLwMKdRUF3mi3H6",  "use_case": {    "account_onboarding": {      "configurations": [        "recipient"      ],      "refresh_url": "https://example.com/reauth",      "return_url": "https://example.com/return"    },    "type": "account_onboarding"  }}
```

Example 3 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/account_links \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "account": "acct_1Nv0FGQ9RKHgCVdK",    "use_case": {        "type": "account_onboarding",        "account_onboarding": {            "configurations": [                "recipient"            ],            "return_url": "https://example.com/return",            "refresh_url": "https://example.com/reauth"        }    }  }'
```

Example 4 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/account_links \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "account": "acct_1Nv0FGQ9RKHgCVdK",    "use_case": {        "type": "account_onboarding",        "account_onboarding": {            "configurations": [                "recipient"            ],            "return_url": "https://example.com/return",            "refresh_url": "https://example.com/reauth"        }    }  }'
```

---

## Create a PaymentIntent

**URL:** https://docs.stripe.com/api/payment_intents/create

**Contents:**
- Create a PaymentIntent
  - Parameters
    - amountintegerRequired
    - currencyenumRequired
    - automatic_payment_methodsobject
    - confirmboolean
    - customerstring
    - customer_accountstring
    - descriptionstring
    - metadataobject

Creates a PaymentIntent object.

After the PaymentIntent is created, attach a payment method and confirm to continue the payment. Learn more about the available payment flows with the Payment Intents API.

When you use confirm=true during creation, it’s equivalent to creating and confirming the PaymentIntent in the same call. You can use any parameters available in the confirm API when you supply confirm=true.

Amount intended to be collected by this PaymentIntent. A positive integer representing how much to charge in the smallest currency unit (e.g., 100 cents to charge $1.00 or 100 to charge ¥100, a zero-decimal currency). The minimum amount is $0.50 US or equivalent in charge currency. The amount value supports up to eight digits (e.g., a value of 99999999 for a USD charge of $999,999.99).

Three-letter ISO currency code, in lowercase. Must be a supported currency.

When you enable this parameter, this PaymentIntent accepts payment methods that you enable in the Dashboard and that are compatible with this PaymentIntent’s other parameters.

Set to true to attempt to confirm this PaymentIntent immediately. This parameter defaults to false. When creating and confirming a PaymentIntent at the same time, you can also provide the parameters available in the Confirm API.

ID of the Customer this PaymentIntent belongs to, if one exists.

Payment methods attached to other Customers cannot be used with this PaymentIntent.

If setup_future_usage is set and this PaymentIntent’s payment method is not card_present, then the payment method attaches to the Customer after the PaymentIntent has been confirmed and any required actions from the user are complete. If the payment method is card_present and isn’t a digital wallet, then a generated_card payment method representing the card is created and attached to the Customer instead.

ID of the Account representing the customer that this PaymentIntent belongs to, if one exists.

Payment methods attached to other Accounts cannot be used with this PaymentIntent.

If setup_future_usage is set and this PaymentIntent’s payment method is not card_present, then the payment method attaches to the Account after the PaymentIntent has been confirmed and any required actions from the user are complete. If the payment method is card_present and isn’t a digital wallet, then a generated_card payment method representing the card is created and attached to the Account instead.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Set to true to indicate that the customer isn’t in your checkout flow during this payment attempt and can’t authenticate. Use this parameter in scenarios where you collect card details and charge them later. This parameter can only be used with confirm=true.

ID of the payment method (a PaymentMethod, Card, or compatible Source object) to attach to this PaymentIntent.

If you omit this parameter with confirm=true, customer.default_source attaches as this PaymentIntent’s payment instrument to improve migration for users of the Charges API. We recommend that you explicitly provide the payment_method moving forward. If the payment method is attached to a Customer, you must also provide the ID of that Customer as the customer parameter of this PaymentIntent.

Email address to send the receipt to. If you specify receipt_email for a payment in live mode, you send a receipt regardless of your email settings.

Indicates that you intend to make future payments with this PaymentIntent’s payment method.

If you provide a Customer with the PaymentIntent, you can use this parameter to attach the payment method to the Customer after the PaymentIntent is confirmed and the customer completes any required actions. If you don’t provide a Customer, you can still attach the payment method to a Customer after the transaction completes.

If the payment method is card_present and isn’t a digital wallet, Stripe creates and attaches a generated_card payment method representing the card to the Customer instead.

When processing card payments, Stripe uses setup_future_usage to help you comply with regional legislation and network rules, such as SCA.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

Shipping information for this PaymentIntent.

Text that appears on the customer’s statement as the statement descriptor for a non-card charge. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

Setting this value for a card charge returns an error. For card charges, set the statement_descriptor_suffix instead.

Provides information about a card charge. Concatenated to the account’s statement descriptor prefix to form the complete statement descriptor that appears on the customer’s statement.

Returns a PaymentIntent object.

Updates properties on a PaymentIntent object without confirming.

Depending on which properties you update, you might need to confirm the PaymentIntent again. For example, updating the payment_method always requires you to confirm the PaymentIntent again. If you prefer to update and confirm at the same time, we recommend updating properties through the confirm API instead.

Amount intended to be collected by this PaymentIntent. A positive integer representing how much to charge in the smallest currency unit (e.g., 100 cents to charge $1.00 or 100 to charge ¥100, a zero-decimal currency). The minimum amount is $0.50 US or equivalent in charge currency. The amount value supports up to eight digits (e.g., a value of 99999999 for a USD charge of $999,999.99).

Three-letter ISO currency code, in lowercase. Must be a supported currency.

ID of the Customer this PaymentIntent belongs to, if one exists.

Payment methods attached to other Customers cannot be used with this PaymentIntent.

If setup_future_usage is set and this PaymentIntent’s payment method is not card_present, then the payment method attaches to the Customer after the PaymentIntent has been confirmed and any required actions from the user are complete. If the payment method is card_present and isn’t a digital wallet, then a generated_card payment method representing the card is created and attached to the Customer instead.

ID of the Account representing the customer that this PaymentIntent belongs to, if one exists.

Payment methods attached to other Accounts cannot be used with this PaymentIntent.

If setup_future_usage is set and this PaymentIntent’s payment method is not card_present, then the payment method attaches to the Account after the PaymentIntent has been confirmed and any required actions from the user are complete. If the payment method is card_present and isn’t a digital wallet, then a generated_card payment method representing the card is created and attached to the Account instead.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

ID of the payment method (a PaymentMethod, Card, or compatible Source object) to attach to this PaymentIntent. To unset this field to null, pass in an empty string.

Email address that the receipt for the resulting payment will be sent to. If receipt_email is specified for a payment in live mode, a receipt will be sent regardless of your email settings.

Indicates that you intend to make future payments with this PaymentIntent’s payment method.

If you provide a Customer with the PaymentIntent, you can use this parameter to attach the payment method to the Customer after the PaymentIntent is confirmed and the customer completes any required actions. If you don’t provide a Customer, you can still attach the payment method to a Customer after the transaction completes.

If the payment method is card_present and isn’t a digital wallet, Stripe creates and attaches a generated_card payment method representing the card to the Customer instead.

When processing card payments, Stripe uses setup_future_usage to help you comply with regional legislation and network rules, such as SCA.

If you’ve already set setup_future_usage and you’re performing a request using a publishable key, you can only update the value from on_session to off_session.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

Shipping information for this PaymentIntent.

Text that appears on the customer’s statement as the statement descriptor for a non-card charge. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

Setting this value for a card charge returns an error. For card charges, set the statement_descriptor_suffix instead.

Provides information about a card charge. Concatenated to the account’s statement descriptor prefix to form the complete statement descriptor that appears on the customer’s statement.

Returns a PaymentIntent object.

Retrieves the details of a PaymentIntent that has previously been created.

You can retrieve a PaymentIntent client-side using a publishable key when the client_secret is in the query string.

If you retrieve a PaymentIntent with a publishable key, it only returns a subset of properties. Refer to the payment intent object reference for more details.

The client secret of the PaymentIntent. We require it if you use a publishable key to retrieve the source.

Returns a PaymentIntent if a valid identifier was provided.

Lists all LineItems of a given PaymentIntent.

A dictionary with a data property that contains an array of up to limit line items of the given PaymentIntent, starting after line item starting_after. Each entry in the array is a separate line item object. If no other line items are available, the resulting array is empty.

Returns a list of PaymentIntents.

Only return PaymentIntents for the customer that this customer ID specifies.

Only return PaymentIntents for the account representing the customer that this ID specifies.

A dictionary with a data property that contains an array of up to limit PaymentIntents, starting after PaymentIntent starting_after. Each entry in the array is a separate PaymentIntent object. If no other PaymentIntents are available, the resulting array is empty.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=2000 \  -d currency=usd \  -d "automatic_payment_methods[enabled]"=true
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=2000 \  -d currency=usd \  -d "automatic_payment_methods[enabled]"=true
```

Example 3 (unknown):
```unknown
{  "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",  "object": "payment_intent",  "amount": 2000,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 0,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": {    "enabled": true  },  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",  "confirmation_method": "automatic",  "created": 1680800504,  "currency": "usd",  "customer": null,  "description": null,  "last_payment_error": null,  "latest_charge": null,  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": null,  "payment_method_options": {    "card": {      "installments": null,      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    },    "link": {      "persistent_token": null    }  },  "payment_method_types": [    "card",    "link"  ],  "processing": null,  "receipt_email": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "source": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "requires_payment_method",  "transfer_data": null,  "transfer_group": null}
```

Example 4 (unknown):
```unknown
{  "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",  "object": "payment_intent",  "amount": 2000,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 0,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": {    "enabled": true  },  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",  "confirmation_method": "automatic",  "created": 1680800504,  "currency": "usd",  "customer": null,  "description": null,  "last_payment_error": null,  "latest_charge": null,  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": null,  "payment_method_options": {    "card": {      "installments": null,      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    },    "link": {      "persistent_token": null    }  },  "payment_method_types": [    "card",    "link"  ],  "processing": null,  "receipt_email": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "source": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "requires_payment_method",  "transfer_data": null,  "transfer_group": null}
```

---

## Update a dispute

**URL:** https://docs.stripe.com/api/disputes/update

**Contents:**
- Update a dispute
  - Parameters
    - evidenceobject
    - metadataobject
    - submitboolean
  - Returns
- Retrieve a dispute
  - Parameters
  - Returns
- List all disputes

When you get a dispute, contacting your customer is always the best first step. If that doesn’t work, you can submit evidence to help us resolve the dispute in your favor. You can do this in your dashboard, but if you prefer, you can use the API to submit evidence programmatically.

Depending on your dispute type, different evidence fields will give you a better chance of winning your dispute. To figure out which evidence fields to provide, see our guide to dispute types.

Evidence to upload, to respond to a dispute. Updating any field in the hash will submit all fields in the hash for review. The combined character count of all fields is limited to 150,000.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Whether to immediately submit evidence to the bank. If false, evidence is staged on the dispute. Staged evidence is visible in the API and Dashboard, and can be submitted to the bank by making another request with this attribute set to true (the default).

Returns the dispute object.

Retrieves the dispute with the given ID.

Returns a dispute if a valid dispute ID was provided. Raises an error otherwise.

Returns a list of your disputes.

Only return disputes associated to the charge specified by this charge ID.

Only return disputes associated to the PaymentIntent specified by this PaymentIntent ID.

A dictionary with a data property that contains an array of up to limit disputes, starting after dispute starting_after. Each entry in the array is a separate dispute object. If no more disputes are available, the resulting array will be empty.

Closing the dispute for a charge indicates that you do not have any evidence to submit and are essentially dismissing the dispute, acknowledging it as lost.

The status of the dispute will change from needs_response to lost. Closing a dispute is irreversible.

Returns the dispute object.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/disputes/du_1MtJUT2eZvKYlo2CNaw2HvEv \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/disputes/du_1MtJUT2eZvKYlo2CNaw2HvEv \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

Example 3 (unknown):
```unknown
{  "id": "du_1MtJUT2eZvKYlo2CNaw2HvEv",  "object": "dispute",  "amount": 1000,  "balance_transactions": [],  "charge": "ch_1AZtxr2eZvKYlo2CJDX8whov",  "created": 1680651737,  "currency": "usd",  "evidence": {    "access_activity_log": null,    "billing_address": null,    "cancellation_policy": null,    "cancellation_policy_disclosure": null,    "cancellation_rebuttal": null,    "customer_communication": null,    "customer_email_address": null,    "customer_name": null,    "customer_purchase_ip": null,    "customer_signature": null,    "duplicate_charge_documentation": null,    "duplicate_charge_explanation": null,    "duplicate_charge_id": null,    "product_description": null,    "receipt": null,    "refund_policy": null,    "refund_policy_disclosure": null,    "refund_refusal_explanation": null,    "service_date": null,    "service_documentation": null,    "shipping_address": null,    "shipping_carrier": null,    "shipping_date": null,    "shipping_documentation": null,    "shipping_tracking_number": null,    "uncategorized_file": null,    "uncategorized_text": null  },  "evidence_details": {    "due_by": 1682294399,    "has_evidence": false,    "past_due": false,    "submission_count": 0  },  "is_charge_refundable": true,  "livemode": false,  "metadata": {    "order_id": "6735"  },  "payment_intent": null,  "reason": "general",  "status": "warning_needs_response"}
```

Example 4 (unknown):
```unknown
{  "id": "du_1MtJUT2eZvKYlo2CNaw2HvEv",  "object": "dispute",  "amount": 1000,  "balance_transactions": [],  "charge": "ch_1AZtxr2eZvKYlo2CJDX8whov",  "created": 1680651737,  "currency": "usd",  "evidence": {    "access_activity_log": null,    "billing_address": null,    "cancellation_policy": null,    "cancellation_policy_disclosure": null,    "cancellation_rebuttal": null,    "customer_communication": null,    "customer_email_address": null,    "customer_name": null,    "customer_purchase_ip": null,    "customer_signature": null,    "duplicate_charge_documentation": null,    "duplicate_charge_explanation": null,    "duplicate_charge_id": null,    "product_description": null,    "receipt": null,    "refund_policy": null,    "refund_policy_disclosure": null,    "refund_refusal_explanation": null,    "service_date": null,    "service_documentation": null,    "shipping_address": null,    "shipping_carrier": null,    "shipping_date": null,    "shipping_documentation": null,    "shipping_tracking_number": null,    "uncategorized_file": null,    "uncategorized_text": null  },  "evidence_details": {    "due_by": 1682294399,    "has_evidence": false,    "past_due": false,    "submission_count": 0  },  "is_charge_refundable": true,  "livemode": false,  "metadata": {    "order_id": "6735"  },  "payment_intent": null,  "reason": "general",  "status": "warning_needs_response"}
```

---

## The Customer object

**URL:** https://docs.stripe.com/api/customers/object

**Contents:**
- The Customer object
  - Attributes
    - idstring
    - addressnullable object
    - customer_accountnullable string
    - descriptionnullable string
    - emailnullable string
    - metadataobject
    - namenullable string
    - phonenullable string

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

Returns a list of your customers. The customers are returned sorted by creation date, with the most recent customers appearing first.

A case-sensitive filter on the list based on the customer’s email field. The value must be a string.

The maximum length is 512 characters.

A dictionary with a data property that contains an array of up to limit customers, starting after customer starting_after. Passing an optional email will result in filtering to customers with only that exact email address. Each entry in the array is a separate customer object. If no more customers are available, the resulting array will be empty.

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

## Update a customer

**URL:** https://docs.stripe.com/api/customers/update

**Contents:**
- Update a customer
  - Parameters
    - addressobjectRequired if calculating taxes
    - descriptionstring
    - emailstring
    - metadataobject
    - namestring
    - phonestring
    - shippingobject
    - taxobjectRecommended if calculating taxes

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

Returns a list of your customers. The customers are returned sorted by creation date, with the most recent customers appearing first.

A case-sensitive filter on the list based on the customer’s email field. The value must be a string.

The maximum length is 512 characters.

A dictionary with a data property that contains an array of up to limit customers, starting after customer starting_after. Passing an optional email will result in filtering to customers with only that exact email address. Each entry in the array is a separate customer object. If no more customers are available, the resulting array will be empty.

Permanently deletes a customer. It cannot be undone. Also immediately cancels any active subscriptions on the customer.

Returns an object with a deleted parameter on success. If the customer ID does not exist, this call raises an error.

Unlike other objects, deleted customers can still be retrieved through the API in order to be able to track their history. Deleting customers removes all credit card details and prevents any further operations to be performed (such as adding a new subscription).

Search for customers you’ve previously created using Stripe’s Search Query Language. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.

The search query string. See search query language and the list of supported query fields for customers.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A dictionary with a data property that contains an array of up to limit customers. If no objects match the query, the resulting array will be empty. See the related guide on expanding properties in lists.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/customers/cus_NffrFeUfNV2Hib \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/customers/cus_NffrFeUfNV2Hib \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

Example 3 (unknown):
```unknown
{  "id": "cus_NffrFeUfNV2Hib",  "object": "customer",  "address": null,  "balance": 0,  "created": 1680893993,  "currency": null,  "default_source": null,  "delinquent": false,  "description": null,  "email": "jennyrosen@example.com",  "invoice_prefix": "0759376C",  "invoice_settings": {    "custom_fields": null,    "default_payment_method": null,    "footer": null,    "rendering_options": null  },  "livemode": false,  "metadata": {    "order_id": "6735"  },  "name": "Jenny Rosen",  "next_invoice_sequence": 1,  "phone": null,  "preferred_locales": [],  "shipping": null,  "tax_exempt": "none",  "test_clock": null}
```

Example 4 (unknown):
```unknown
{  "id": "cus_NffrFeUfNV2Hib",  "object": "customer",  "address": null,  "balance": 0,  "created": 1680893993,  "currency": null,  "default_source": null,  "delinquent": false,  "description": null,  "email": "jennyrosen@example.com",  "invoice_prefix": "0759376C",  "invoice_settings": {    "custom_fields": null,    "default_payment_method": null,    "footer": null,    "rendering_options": null  },  "livemode": false,  "metadata": {    "order_id": "6735"  },  "name": "Jenny Rosen",  "next_invoice_sequence": 1,  "phone": null,  "preferred_locales": [],  "shipping": null,  "tax_exempt": "none",  "test_clock": null}
```

---

## Products

**URL:** https://docs.stripe.com/api/products

**Contents:**
- Products
- The Product object
  - Attributes
    - idstring
    - activeboolean
    - default_pricenullable stringExpandable
    - descriptionnullable string
    - metadataobject
    - namestring
    - tax_codenullable stringExpandable

Products describe the specific goods or services you offer to your customers. For example, you might offer a Standard and Premium version of your goods or service; each version would be a separate Product. They can be used in conjunction with Prices to configure pricing in Payment Links, Checkout, and Subscriptions.

Related guides: Set up a subscription, share a Payment Link, accept payments with Checkout, and more about Products and Prices

Unique identifier for the object.

Whether the product is currently available for purchase.

The ID of the Price object that is the default price for this product.

The product’s description, meant to be displayable to the customer. Use this field to optionally store a long form explanation of the product being sold for your own rendering purposes.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The product’s name, meant to be displayable to the customer.

Creates a new product object.

The product’s name, meant to be displayable to the customer.

Whether the product is currently available for purchase. Defaults to true.

The product’s description, meant to be displayable to the customer. Use this field to optionally store a long form explanation of the product being sold for your own rendering purposes.

An identifier will be randomly generated by Stripe. You can optionally override this ID, but the ID must be unique across all products in your Stripe account.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a product object if the call succeeded.

Updates the specific product by setting the values of the parameters passed. Any parameters not provided will be left unchanged.

Whether the product is available for purchase.

The ID of the Price object that is the default price for this product.

The product’s description, meant to be displayable to the customer. Use this field to optionally store a long form explanation of the product being sold for your own rendering purposes.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The product’s name, meant to be displayable to the customer.

Returns the product object if the update succeeded.

Retrieves the details of an existing product. Supply the unique product ID from either a product creation request or the product list, and Stripe will return the corresponding product information.

Returns a product object if a valid identifier was provided.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "prod_NWjs8kKbJWmuuc",  "object": "product",  "active": true,  "created": 1678833149,  "default_price": null,  "description": null,  "images": [],  "marketing_features": [],  "livemode": false,  "metadata": {},  "name": "Gold Plan",  "package_dimensions": null,  "shippable": null,  "statement_descriptor": null,  "tax_code": null,  "unit_label": null,  "updated": 1678833149,  "url": null}
```

Example 2 (unknown):
```unknown
{  "id": "prod_NWjs8kKbJWmuuc",  "object": "product",  "active": true,  "created": 1678833149,  "default_price": null,  "description": null,  "images": [],  "marketing_features": [],  "livemode": false,  "metadata": {},  "name": "Gold Plan",  "package_dimensions": null,  "shippable": null,  "statement_descriptor": null,  "tax_code": null,  "unit_label": null,  "updated": 1678833149,  "url": null}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/products \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d name="Gold Plan"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/products \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d name="Gold Plan"
```

---

## Mandates

**URL:** https://docs.stripe.com/api/mandates

**Contents:**
- Mandates
- The Mandate object
  - Attributes
    - idstring
    - customer_acceptanceobject
    - payment_methodstringExpandable
    - payment_method_detailsobject
    - statusenum
    - typeenum
  - More attributesExpand all

A Mandate is a record of the permission that your customer gives you to debit their payment method.

Unique identifier for the object.

Details about the customer’s acceptance of the mandate.

ID of the payment method associated with this mandate.

Additional mandate information specific to the payment method type.

The mandate status indicates whether or not you can use it to initiate a payment.

The mandate can be used to initiate a payment.

The mandate was rejected, revoked, or previously used, and may not be used to initiate future payments.

The mandate is newly created and is not yet active or inactive.

The type of the mandate.

Represents permission given for multiple payments.

Represents a one-time permission given for a single payment.

Retrieves a Mandate object.

Returns a Mandate object.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "mandate_1MvojA2eZvKYlo2CvqTABjZs",  "object": "mandate",  "customer_acceptance": {    "accepted_at": 123456789,    "online": {      "ip_address": "127.0.0.0",      "user_agent": "device"    },    "type": "online"  },  "livemode": false,  "multi_use": {},  "payment_method": "pm_123456789",  "payment_method_details": {    "sepa_debit": {      "reference": "123456789",      "url": ""    },    "type": "sepa_debit"  },  "status": "active",  "type": "multi_use"}
```

Example 2 (unknown):
```unknown
{  "id": "mandate_1MvojA2eZvKYlo2CvqTABjZs",  "object": "mandate",  "customer_acceptance": {    "accepted_at": 123456789,    "online": {      "ip_address": "127.0.0.0",      "user_agent": "device"    },    "type": "online"  },  "livemode": false,  "multi_use": {},  "payment_method": "pm_123456789",  "payment_method_details": {    "sepa_debit": {      "reference": "123456789",      "url": ""    },    "type": "sepa_debit"  },  "status": "active",  "type": "multi_use"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/mandates/mandate_1MvojA2eZvKYlo2CvqTABjZs \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/mandates/mandate_1MvojA2eZvKYlo2CvqTABjZs \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

---

## The Person object

**URL:** https://docs.stripe.com/api/v2/core/persons/object

**Contents:**
- The Person object
  - Attributes
    - idstring
    - objectstring, value is "v2.core.account_person"
    - accountstring
    - additional_addressesnullable array of objects
    - additional_namesnullable array of objects
    - additional_terms_of_servicenullable object
    - addressnullable object
    - createdtimestamp

Unique identifier for the Person.

String representing the object’s type. Objects of the same type share the same value of the object field.

The account ID which the individual belongs to.

Additional addresses associated with the person.

Additional names (e.g. aliases) associated with the person.

Attestations of accepted terms of service agreements.

The person’s residential address.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

The person’s date of birth.

Documents that may be submitted to satisfy various informational requests.

The person’s email address.

The person’s first name.

The identification numbers (e.g., SSN) associated with the person.

The person’s gender (International regulations require either “male” or “female”).

Female gender person.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The countries where the person is a national. Two-letter country code (ISO 3166-1 alpha-2).

The person’s phone number.

The person’s political exposure.

The person has disclosed that they do have political exposure.

The person has disclosed that they have no political exposure.

The relationship that this person has with the Account’s business or legal entity.

The script addresses (e.g., non-Latin characters) associated with the person.

The script names (e.g. non-Latin characters) associated with the person.

The person’s last name.

Time at which the object was last updated. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Create a Person. Adds an individual to an Account’s identity. You can set relationship attributes and identity information at creation.

Account the Person should be associated with.

Additional addresses associated with the person.

Additional names (e.g. aliases) associated with the person.

Attestations of accepted terms of service agreements.

The person’s residential address.

The person’s date of birth.

Documents that may be submitted to satisfy various informational requests.

The person’s first name.

The identification numbers (e.g., SSN) associated with the person.

The person’s gender (International regulations require either “male” or “female”).

Female gender person.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The nationalities (countries) this person is associated with.

The person token generated by the person token api.

The phone number for this person.

The person’s political exposure.

The person has disclosed that they do have political exposure.

The person has disclosed that they have no political exposure.

The relationship that this person has with the Account’s business or legal entity.

The script addresses (e.g., non-Latin characters) associated with the person.

The script names (e.g. non-Latin characters) associated with the person.

The person’s last name.

Unique identifier for the Person.

String representing the object’s type. Objects of the same type share the same value of the object field.

The account ID which the individual belongs to.

Additional addresses associated with the person.

Additional names (e.g. aliases) associated with the person.

Attestations of accepted terms of service agreements.

The person’s residential address.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

The person’s date of birth.

Documents that may be submitted to satisfy various informational requests.

The person’s email address.

The person’s first name.

The identification numbers (e.g., SSN) associated with the person.

The person’s gender (International regulations require either “male” or “female”).

Female gender person.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The countries where the person is a national. Two-letter country code (ISO 3166-1 alpha-2).

The person’s phone number.

The person’s political exposure.

The person has disclosed that they do have political exposure.

The person has disclosed that they have no political exposure.

The relationship that this person has with the Account’s business or legal entity.

The script addresses (e.g., non-Latin characters) associated with the person.

The script names (e.g. non-Latin characters) associated with the person.

The person’s last name.

Time at which the object was last updated. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

More than one legal guardian is added to an account.

More than one representative is added to an account.

Additional terms of service are signed by someone other than the legal guardian.

Invalid characters are provided for address fields.

Address country doesn’t match identity country.

Registered/script address country doesn’t match residential address country.

Address country is required but not provided.

Address postal code is invalid.

Address state is invalid.

Address town is invalid.

There can only be one authorizer.

An authorizer cannot be a representative.

Representative date of birth does not meet the age limit.

Representative date of birth is provided an invalid date or a future date.

Provided file tokens for documents are invalid, not found, deleted, or belong to a different account.

Provided file tokens for documents are of the wrong purpose.

Duplicate person is added to an account.

Email contains unsupported domain.

Incorrect email is provided.

Provided ID number is of the wrong format for the given type.

The identity.country value is required but not provided.

A person token is created with one account but used on a different account.

Incorrect ID number is provided for a country.

The incorrect token type is provided .

Additional person is added for an individual business type.

Some relationships are specific to type, structure, and country.

Invalid IP address is provided.

Person is designated as both legal guardian and representative.

A legal guardian may not be added to the account without an existing representative.

Kana Kanji script addresses must have JP country.

Parameter cannot be passed alongside person_token.

Error returned when relationship.owner is set to true but the ownership percentage is set to 0%.

Person token required for platforms in mandated countries (e.g., France).

Phone number is invalid.

Postal code is required for Japanese addresses.

Provided script characters are invalid for the script.

The token is re-used with a different idempotency key.

Total ownership percentages of all Persons on the account exceeds 100%.

Address is in an unsupported postal code.

Address is in an unsupported state.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

A v1 token ID is passed in v2 APIs.

Invalid person token.

Updates a Person associated with an Account.

The Account the Person is associated with.

The ID of the Person to update.

Additional addresses associated with the person.

Additional names (e.g. aliases) associated with the person.

Attestations of accepted terms of service agreements.

The primary address associated with the person.

The person’s date of birth.

Documents that may be submitted to satisfy various informational requests.

The person’s first name.

The identification numbers (e.g., SSN) associated with the person.

The person’s gender (International regulations require either “male” or “female”).

Female gender person.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The nationalities (countries) this person is associated with.

The person token generated by the person token api.

The phone number for this person.

The person’s political exposure.

The person has disclosed that they do have political exposure.

The person has disclosed that they have no political exposure.

The relationship that this person has with the Account’s business or legal entity.

The script addresses (e.g., non-Latin characters) associated with the person.

The script names (e.g. non-Latin characters) associated with the person.

The person’s last name.

Unique identifier for the Person.

String representing the object’s type. Objects of the same type share the same value of the object field.

The account ID which the individual belongs to.

Additional addresses associated with the person.

Additional names (e.g. aliases) associated with the person.

Attestations of accepted terms of service agreements.

The person’s residential address.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

The person’s date of birth.

Documents that may be submitted to satisfy various informational requests.

The person’s email address.

The person’s first name.

The identification numbers (e.g., SSN) associated with the person.

The person’s gender (International regulations require either “male” or “female”).

Female gender person.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The countries where the person is a national. Two-letter country code (ISO 3166-1 alpha-2).

The person’s phone number.

The person’s political exposure.

The person has disclosed that they do have political exposure.

The person has disclosed that they have no political exposure.

The relationship that this person has with the Account’s business or legal entity.

The script addresses (e.g., non-Latin characters) associated with the person.

The script names (e.g. non-Latin characters) associated with the person.

The person’s last name.

Time at which the object was last updated. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

More than one legal guardian is added to an account.

More than one representative is added to an account.

Additional terms of service are signed by someone other than the legal guardian.

Invalid characters are provided for address fields.

Address country doesn’t match identity country.

Registered/script address country doesn’t match residential address country.

Address country is required but not provided.

Address postal code is invalid.

Address state is invalid.

Address town is invalid.

Representative date of birth does not meet the age limit.

Representative date of birth is provided an invalid date or a future date.

Provided file tokens for documents are invalid, not found, deleted, or belong to a different account.

Provided file tokens for documents are of the wrong purpose.

Duplicate person is added to an account.

Email contains unsupported domain.

Incorrect email is provided.

Provided ID number is of the wrong format for the given type.

The identity.country value is required but not provided.

Identity param has been made immutable due to the state of the account.

A person token is created with one account but used on a different account.

Incorrect ID number is provided for a country.

The incorrect token type is provided .

Invalid IP address is provided.

Person is designated as both legal guardian and representative.

A legal guardian may not be added to the account without an existing representative.

Kana Kanji script addresses must have JP country.

Parameter cannot be passed alongside person_token.

Error returned when relationship.owner is set to true but the ownership percentage is set to 0%.

Person token required for platforms in mandated countries (e.g., France).

Phone number is invalid.

Postal code is required for Japanese addresses.

Provided script characters are invalid for the script.

The token is re-used with a different idempotency key.

Total ownership percentages of all Persons on the account exceeds 100%.

Address is in an unsupported postal code.

Address is in an unsupported state.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

A v1 token ID is passed in v2 APIs.

Invalid person token.

The resource wasn’t found.

Retrieves a Person associated with an Account.

The Account the Person is associated with.

The ID of the Person to retrieve.

Unique identifier for the Person.

String representing the object’s type. Objects of the same type share the same value of the object field.

The account ID which the individual belongs to.

Additional addresses associated with the person.

Additional names (e.g. aliases) associated with the person.

Attestations of accepted terms of service agreements.

The person’s residential address.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

The person’s date of birth.

Documents that may be submitted to satisfy various informational requests.

The person’s email address.

The person’s first name.

The identification numbers (e.g., SSN) associated with the person.

The person’s gender (International regulations require either “male” or “female”).

Female gender person.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The countries where the person is a national. Two-letter country code (ISO 3166-1 alpha-2).

The person’s phone number.

The person’s political exposure.

The person has disclosed that they do have political exposure.

The person has disclosed that they have no political exposure.

The relationship that this person has with the Account’s business or legal entity.

The script addresses (e.g., non-Latin characters) associated with the person.

The script names (e.g. non-Latin characters) associated with the person.

The person’s last name.

Time at which the object was last updated. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

The resource wasn’t found.

Returns a paginated list of Persons associated with an Account.

Account the Persons are associated with.

The upper limit on the number of accounts returned by the List Account request.

The page token to navigate to next or previous batch of accounts given by the list request.

A list of retrieved Person objects.

URL with page token to navigate to next batch of Persons given by the list request.

URL with page token to previous to next batch of Persons given by the list request.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_person",  "account": "acct_1Nv0FGQ9RKHgCVdK",  "additional_addresses": [],  "additional_names": [],  "address": {    "city": "Brothers",    "country": "us",    "line1": "27 Fredrick Ave",    "postal_code": "97712",    "state": "OR"  },  "created": "2024-11-26T17:10:07.000Z",  "email": "jenny.rosen@example.com",  "given_name": "Jenny",  "id_numbers": [    {      "type": "us_ssn_last_4"    }  ],  "metadata": {},  "nationalities": [],  "relationship": {    "owner": true,    "percent_ownership": "0.8",    "representative": true,    "title": "CEO"  },  "surname": "Rosen",  "updated": "2024-11-26T17:10:07.000Z"}
```

Example 2 (unknown):
```unknown
{  "id": "person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_person",  "account": "acct_1Nv0FGQ9RKHgCVdK",  "additional_addresses": [],  "additional_names": [],  "address": {    "city": "Brothers",    "country": "us",    "line1": "27 Fredrick Ave",    "postal_code": "97712",    "state": "OR"  },  "created": "2024-11-26T17:10:07.000Z",  "email": "jenny.rosen@example.com",  "given_name": "Jenny",  "id_numbers": [    {      "type": "us_ssn_last_4"    }  ],  "metadata": {},  "nationalities": [],  "relationship": {    "owner": true,    "percent_ownership": "0.8",    "representative": true,    "title": "CEO"  },  "surname": "Rosen",  "updated": "2024-11-26T17:10:07.000Z"}
```

Example 3 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/persons \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "given_name": "Jenny",    "surname": "Rosen",    "email": "jenny.rosen@example.com",    "address": {        "line1": "27 Fredrick Ave",        "city": "Brothers",        "postal_code": "97712",        "state": "OR",        "country": "us"    },    "id_numbers": [        {            "type": "us_ssn_last_4",            "value": "0000"        }    ],    "relationship": {        "owner": true,        "percent_ownership": "0.8",        "representative": true,        "title": "CEO"    }  }'
```

Example 4 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/persons \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "given_name": "Jenny",    "surname": "Rosen",    "email": "jenny.rosen@example.com",    "address": {        "line1": "27 Fredrick Ave",        "city": "Brothers",        "postal_code": "97712",        "state": "OR",        "country": "us"    },    "id_numbers": [        {            "type": "us_ssn_last_4",            "value": "0000"        }    ],    "relationship": {        "owner": true,        "percent_ownership": "0.8",        "representative": true,        "title": "CEO"    }  }'
```

---

## Auto-pagination

**URL:** https://docs.stripe.com/api/pagination/auto

**Contents:**
- Auto-pagination
- Request IDs
- Connected Accounts
- Versioning

Our libraries support auto-pagination. This feature allows you to easily iterate through large lists of resources without having to manually perform the requests to fetch subsequent pages.

Each API request has an associated request identifier. You can find this value in the response headers, under Request-Id. You can also find request identifiers in the URLs of individual request logs in your Dashboard.

To expedite the resolution process, provide the request identifier when you contact us about a specific request.

If you use Stripe Connect, you can issue requests on behalf of your connected accounts. To act as a connected account, include a Stripe-Account header containing the connected account ID, which typically starts with the acct_ prefix.

The connected account ID is set per-request. Methods on the returned object reuse the same account ID.

Each major release, such as Acacia, includes changes that aren’t backward-compatible with previous releases. Upgrading to a new major release can require updates to existing code. Each monthly release includes only backward-compatible changes, and uses the same name as the last major release. You can safely upgrade to a new monthly release without breaking any existing code. The current version is 2025-12-15.clover. For information on all API versions, view our API changelog.

You can upgrade your API version in Workbench. As a precaution, use API versioning to test a new API version before committing to an upgrade.

**Examples:**

Example 1 (unknown):
```unknown
# The auto-pagination feature is specific to Stripe's# libraries and cannot be used directly with curl.
```

Example 2 (unknown):
```unknown
# The auto-pagination feature is specific to Stripe's# libraries and cannot be used directly with curl.
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/customers \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -D "-" \  -X POST
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/customers \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -D "-" \  -X POST
```

---

## Create a Customer Session

**URL:** https://docs.stripe.com/api/customer_sessions/create

**Contents:**
- Create a Customer Session
  - Parameters
    - componentsobjectRequired
    - customerstring
  - More parametersExpand all
    - customer_accountstring
  - Returns

Creates a Customer Session object that includes a single-use client secret that you can use on your front-end to grant client-side API access for certain customer resources.

Configuration for each component. At least 1 component must be enabled.

The ID of an existing customer for which to create the Customer Session.

Returns a Customer Session object.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/customer_sessions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_PO34b57IOUb83c \  -d "components[pricing_table][enabled]"=true
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/customer_sessions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_PO34b57IOUb83c \  -d "components[pricing_table][enabled]"=true
```

Example 3 (unknown):
```unknown
{  "object": "customer_session",  "client_secret": "_POpxYpmkXdtttYtZQYhrsOJZ2RCQ9kCqqXRU6qrP5c4Jgje",  "components": {    "buy_button": {      "enabled": false    },    "pricing_table": {      "enabled": true    }  },  "customer": "cus_PO34b57IOUb83c",  "expires_at": 1684790027,  "livemode": false}
```

Example 4 (unknown):
```unknown
{  "object": "customer_session",  "client_secret": "_POpxYpmkXdtttYtZQYhrsOJZ2RCQ9kCqqXRU6qrP5c4Jgje",  "components": {    "buy_button": {      "enabled": false    },    "pricing_table": {      "enabled": true    }  },  "customer": "cus_PO34b57IOUb83c",  "expires_at": 1684790027,  "livemode": false}
```

---

## Country Specs

**URL:** https://docs.stripe.com/api/country_specs

**Contents:**
- Country Specs
- The Country Spec object
  - Attributes
    - idstring
    - default_currencystring
    - supported_bank_account_currenciesobject
    - supported_payment_currenciesarray of strings
    - supported_payment_methodsarray of strings
    - supported_transfer_countriesarray of strings
  - More attributesExpand all

Stripe needs to collect certain pieces of information about each account created. These requirements can differ depending on the account’s country. The Country Specs API makes these rules available to your integration.

You can also view the information from this API call as an online guide.

Unique identifier for the object. Represented as the ISO country code for this country.

The default currency for this country. This applies to both payment methods and bank accounts.

Currencies that can be accepted in the specific country (for transfers).

Currencies that can be accepted in the specified country (for payments).

Payment methods available in the specified country. You may need to enable some payment methods (e.g., ACH) on your account before they appear in this list. The stripe payment method refers to charging through your platform.

Countries that can accept transfers from the specified country.

Returns a Country Spec for a given Country code.

Returns a country_spec object if a valid country code is provided, and raises an error otherwise.

Lists all Country Spec objects available in the API.

Returns a list of country_spec objects.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "US",  "object": "country_spec",  "default_currency": "usd",  "supported_bank_account_currencies": {    "usd": [      "US"    ]  },  "supported_payment_currencies": [    "usd",    "aed",    "afn",    "..."  ],  "supported_payment_methods": [    "ach",    "card",    "stripe"  ],  "supported_transfer_countries": [    "US",    "AE",    "AG",    "AL",    "AM",    "AR",    "AT",    "AU",    "BA",    "BE",    "BG",    "BH",    "BO",    "CA",    "CH",    "CI",    "CL",    "CO",    "CR",    "CY",    "CZ",    "DE",    "DK",    "DO",    "EC",    "EE",    "EG",    "ES",    "ET",    "FI",    "FR",    "GB",    "GH",    "GM",    "GR",    "GT",    "GY",    "HK",    "HR",    "HU",    "ID",    "IE",    "IL",    "IS",    "IT",    "JM",    "JO",    "JP",    "KE",    "KH",    "KR",    "KW",    "LC",    "LI",    "LK",    "LT",    "LU",    "LV",    "MA",    "MD",    "MG",    "MK",    "MN",    "MO",    "MT",    "MU",    "MX",    "MY",    "NA",    "NG",    "NL",    "NO",    "NZ",    "OM",    "PA",    "PE",    "PH",    "PL",    "PT",    "PY",    "QA",    "RO",    "RS",    "RW",    "SA",    "SE",    "SG",    "SI",    "SK",    "SN",    "SV",    "TH",    "TN",    "TR",    "TT",    "TZ",    "UY",    "UZ",    "VN",    "ZA",    "BD",    "BJ",    "MC",    "NE",    "SM",    "AZ",    "BN",    "BT",    "AO",    "DZ",    "TW",    "BS",    "BW",    "GA",    "LA",    "MZ",    "KZ",    "PK"  ],  "verification_fields": {    "company": {      "additional": [],      "minimum": [        "business_profile.mcc",        "business_profile.url",        "business_type",        "company.address.city",        "company.address.line1",        "company.address.postal_code",        "company.address.state",        "company.name",        "company.owners_provided",        "company.phone",        "company.tax_id",        "external_account",        "owners.address.city",        "owners.address.line1",        "owners.address.postal_code",        "owners.address.state",        "owners.dob.day",        "owners.dob.month",        "owners.dob.year",        "owners.email",        "owners.first_name",        "owners.id_number",        "owners.last_name",        "owners.phone",        "owners.ssn_last_4",        "owners.verification.document",        "representative.address.city",        "representative.address.line1",        "representative.address.postal_code",        "representative.address.state",        "representative.dob.day",        "representative.dob.month",        "representative.dob.year",        "representative.email",        "representative.first_name",        "representative.id_number",        "representative.last_name",        "representative.phone",        "representative.relationship.executive",        "representative.relationship.title",        "representative.ssn_last_4",        "representative.verification.document",        "tos_acceptance.date",        "tos_acceptance.ip"      ]    },    "individual": {      "additional": [],      "minimum": [        "business_profile.mcc",        "business_profile.url",        "business_type",        "external_account",        "individual.address.city",        "individual.address.line1",        "individual.address.postal_code",        "individual.address.state",        "individual.dob.day",        "individual.dob.month",        "individual.dob.year",        "individual.email",        "individual.first_name",        "individual.id_number",        "individual.last_name",        "individual.phone",        "individual.ssn_last_4",        "individual.verification.document",        "tos_acceptance.date",        "tos_acceptance.ip"      ]    }  }}
```

Example 2 (unknown):
```unknown
{  "id": "US",  "object": "country_spec",  "default_currency": "usd",  "supported_bank_account_currencies": {    "usd": [      "US"    ]  },  "supported_payment_currencies": [    "usd",    "aed",    "afn",    "..."  ],  "supported_payment_methods": [    "ach",    "card",    "stripe"  ],  "supported_transfer_countries": [    "US",    "AE",    "AG",    "AL",    "AM",    "AR",    "AT",    "AU",    "BA",    "BE",    "BG",    "BH",    "BO",    "CA",    "CH",    "CI",    "CL",    "CO",    "CR",    "CY",    "CZ",    "DE",    "DK",    "DO",    "EC",    "EE",    "EG",    "ES",    "ET",    "FI",    "FR",    "GB",    "GH",    "GM",    "GR",    "GT",    "GY",    "HK",    "HR",    "HU",    "ID",    "IE",    "IL",    "IS",    "IT",    "JM",    "JO",    "JP",    "KE",    "KH",    "KR",    "KW",    "LC",    "LI",    "LK",    "LT",    "LU",    "LV",    "MA",    "MD",    "MG",    "MK",    "MN",    "MO",    "MT",    "MU",    "MX",    "MY",    "NA",    "NG",    "NL",    "NO",    "NZ",    "OM",    "PA",    "PE",    "PH",    "PL",    "PT",    "PY",    "QA",    "RO",    "RS",    "RW",    "SA",    "SE",    "SG",    "SI",    "SK",    "SN",    "SV",    "TH",    "TN",    "TR",    "TT",    "TZ",    "UY",    "UZ",    "VN",    "ZA",    "BD",    "BJ",    "MC",    "NE",    "SM",    "AZ",    "BN",    "BT",    "AO",    "DZ",    "TW",    "BS",    "BW",    "GA",    "LA",    "MZ",    "KZ",    "PK"  ],  "verification_fields": {    "company": {      "additional": [],      "minimum": [        "business_profile.mcc",        "business_profile.url",        "business_type",        "company.address.city",        "company.address.line1",        "company.address.postal_code",        "company.address.state",        "company.name",        "company.owners_provided",        "company.phone",        "company.tax_id",        "external_account",        "owners.address.city",        "owners.address.line1",        "owners.address.postal_code",        "owners.address.state",        "owners.dob.day",        "owners.dob.month",        "owners.dob.year",        "owners.email",        "owners.first_name",        "owners.id_number",        "owners.last_name",        "owners.phone",        "owners.ssn_last_4",        "owners.verification.document",        "representative.address.city",        "representative.address.line1",        "representative.address.postal_code",        "representative.address.state",        "representative.dob.day",        "representative.dob.month",        "representative.dob.year",        "representative.email",        "representative.first_name",        "representative.id_number",        "representative.last_name",        "representative.phone",        "representative.relationship.executive",        "representative.relationship.title",        "representative.ssn_last_4",        "representative.verification.document",        "tos_acceptance.date",        "tos_acceptance.ip"      ]    },    "individual": {      "additional": [],      "minimum": [        "business_profile.mcc",        "business_profile.url",        "business_type",        "external_account",        "individual.address.city",        "individual.address.line1",        "individual.address.postal_code",        "individual.address.state",        "individual.dob.day",        "individual.dob.month",        "individual.dob.year",        "individual.email",        "individual.first_name",        "individual.id_number",        "individual.last_name",        "individual.phone",        "individual.ssn_last_4",        "individual.verification.document",        "tos_acceptance.date",        "tos_acceptance.ip"      ]    }  }}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/country_specs/US \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/country_specs/US \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

---

## Retrieve a refund

**URL:** https://docs.stripe.com/api/refunds/retrieve

**Contents:**
- Retrieve a refund
  - Parameters
  - Returns
- List all refunds
  - Parameters
    - chargestring
    - payment_intentstring
  - More parametersExpand all
    - createdobject
    - ending_beforestring

Retrieves the details of an existing refund.

Returns a refund if you provide a valid ID. Raises an error otherwise.

Returns a list of all refunds you created. We return the refunds in sorted order, with the most recent refunds appearing first. The 10 most recent refunds are always available by default on the Charge object.

Only return refunds for the charge specified by this charge ID.

Only return refunds for the PaymentIntent specified by this ID.

A dictionary with a data property that contains an array of up to limit refunds, starting after the starting_after refund. Each entry in the array is a separate Refund object. If no other refunds are available, the resulting array is empty. If you provide a non-existent charge ID, this call raises an error.

Cancels a refund with a status of requires_action.

You can’t cancel refunds in other states. Only refunds for payment methods that require customer action can enter the requires_action state.

Returns the refund object if the cancellation succeeds. This call raises an error if you can’t cancel the refund.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/refunds/re_1Nispe2eZvKYlo2Cd31jOCgZ \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/refunds/re_1Nispe2eZvKYlo2Cd31jOCgZ \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "re_1Nispe2eZvKYlo2Cd31jOCgZ",  "object": "refund",  "amount": 1000,  "balance_transaction": "txn_1Nispe2eZvKYlo2CYezqFhEx",  "charge": "ch_1NirD82eZvKYlo2CIvbtLWuY",  "created": 1692942318,  "currency": "usd",  "destination_details": {    "card": {      "reference": "123456789012",      "reference_status": "available",      "reference_type": "acquirer_reference_number",      "type": "refund"    },    "type": "card"  },  "metadata": {},  "payment_intent": "pi_1GszsK2eZvKYlo2CfhZyoZLp",  "reason": null,  "receipt_number": null,  "source_transfer_reversal": null,  "status": "succeeded",  "transfer_reversal": null}
```

Example 4 (unknown):
```unknown
{  "id": "re_1Nispe2eZvKYlo2Cd31jOCgZ",  "object": "refund",  "amount": 1000,  "balance_transaction": "txn_1Nispe2eZvKYlo2CYezqFhEx",  "charge": "ch_1NirD82eZvKYlo2CIvbtLWuY",  "created": 1692942318,  "currency": "usd",  "destination_details": {    "card": {      "reference": "123456789012",      "reference_status": "available",      "reference_type": "acquirer_reference_number",      "type": "refund"    },    "type": "card"  },  "metadata": {},  "payment_intent": "pi_1GszsK2eZvKYlo2CfhZyoZLp",  "reason": null,  "receipt_number": null,  "source_transfer_reversal": null,  "status": "succeeded",  "transfer_reversal": null}
```

---

## Account Links v2

**URL:** https://docs.stripe.com/api/v2/core/account-links

**Contents:**
- Account Links v2
- The AccountLink object
  - Attributes
    - objectstring, value is "v2.core.account_link"
    - accountstring
    - createdtimestamp
    - expires_attimestamp
    - livemodeboolean
    - urlstring
    - use_caseobject

Account Links let a platform create a temporary, single-use URL that an account can use to access a Stripe-hosted flow for collecting or updating required information.

String representing the object’s type. Objects of the same type share the same value of the object field.

The ID of the connected account this Account Link applies to.

The timestamp at which this Account Link was created.

The timestamp at which this Account Link will expire.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The URL at which the account can access the Stripe-hosted flow.

Hash containing usage options.

Creates an AccountLink object that includes a single-use URL that an account can use to access a Stripe-hosted flow for collecting or updating required information.

The ID of the Account to create link for.

The use case of the AccountLink.

String representing the object’s type. Objects of the same type share the same value of the object field.

The ID of the connected account this Account Link applies to.

The timestamp at which this Account Link was created.

The timestamp at which this Account Link will expire.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The URL at which the account can access the Stripe-hosted flow.

Hash containing usage options.

Accounts v2 is not enabled for your platform.

Account cannot be onboard via v2/core/account_links without specifying the right configurations.

The resource wasn’t found.

**Examples:**

Example 1 (unknown):
```unknown
{  "object": "v2.core.account_link",  "account": "acct_1Nv0FGQ9RKHgCVdK",  "created": "2025-03-27T17:15:18.000Z",  "expires_at": "2025-03-27T17:25:18.000Z",  "url": "https://accounts.stripe.com/r/acct_1Nv0FGQ9RKHgCVdK#alu_test_61SGhyomRuz7xsw5216SGhyj0ASQdCLwMKdRUF3mi3H6",  "use_case": {    "account_onboarding": {      "configurations": [        "recipient"      ],      "refresh_url": "https://example.com/reauth",      "return_url": "https://example.com/return"    },    "type": "account_onboarding"  }}
```

Example 2 (unknown):
```unknown
{  "object": "v2.core.account_link",  "account": "acct_1Nv0FGQ9RKHgCVdK",  "created": "2025-03-27T17:15:18.000Z",  "expires_at": "2025-03-27T17:25:18.000Z",  "url": "https://accounts.stripe.com/r/acct_1Nv0FGQ9RKHgCVdK#alu_test_61SGhyomRuz7xsw5216SGhyj0ASQdCLwMKdRUF3mi3H6",  "use_case": {    "account_onboarding": {      "configurations": [        "recipient"      ],      "refresh_url": "https://example.com/reauth",      "return_url": "https://example.com/return"    },    "type": "account_onboarding"  }}
```

Example 3 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/account_links \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "account": "acct_1Nv0FGQ9RKHgCVdK",    "use_case": {        "type": "account_onboarding",        "account_onboarding": {            "configurations": [                "recipient"            ],            "return_url": "https://example.com/return",            "refresh_url": "https://example.com/reauth"        }    }  }'
```

Example 4 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/account_links \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "account": "acct_1Nv0FGQ9RKHgCVdK",    "use_case": {        "type": "account_onboarding",        "account_onboarding": {            "configurations": [                "recipient"            ],            "return_url": "https://example.com/return",            "refresh_url": "https://example.com/reauth"        }    }  }'
```

---

## Close a dispute

**URL:** https://docs.stripe.com/api/disputes/close

**Contents:**
- Close a dispute
  - Parameters
  - Returns

Closing the dispute for a charge indicates that you do not have any evidence to submit and are essentially dismissing the dispute, acknowledging it as lost.

The status of the dispute will change from needs_response to lost. Closing a dispute is irreversible.

Returns the dispute object.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/disputes/du_1MtJUT2eZvKYlo2CNaw2HvEv/close \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/disputes/du_1MtJUT2eZvKYlo2CNaw2HvEv/close \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "du_1MtJUT2eZvKYlo2CNaw2HvEv",  "object": "dispute",  "amount": 1000,  "balance_transactions": [],  "charge": "ch_1AZtxr2eZvKYlo2CJDX8whov",  "created": 1680651737,  "currency": "usd",  "evidence": {    "access_activity_log": null,    "billing_address": null,    "cancellation_policy": null,    "cancellation_policy_disclosure": null,    "cancellation_rebuttal": null,    "customer_communication": null,    "customer_email_address": null,    "customer_name": null,    "customer_purchase_ip": null,    "customer_signature": null,    "duplicate_charge_documentation": null,    "duplicate_charge_explanation": null,    "duplicate_charge_id": null,    "product_description": null,    "receipt": null,    "refund_policy": null,    "refund_policy_disclosure": null,    "refund_refusal_explanation": null,    "service_date": null,    "service_documentation": null,    "shipping_address": null,    "shipping_carrier": null,    "shipping_date": null,    "shipping_documentation": null,    "shipping_tracking_number": null,    "uncategorized_file": null,    "uncategorized_text": null  },  "evidence_details": {    "due_by": 1682294399,    "has_evidence": false,    "past_due": false,    "submission_count": 0  },  "is_charge_refundable": true,  "livemode": false,  "metadata": {},  "payment_intent": null,  "reason": "general",  "status": "warning_needs_response"}
```

Example 4 (unknown):
```unknown
{  "id": "du_1MtJUT2eZvKYlo2CNaw2HvEv",  "object": "dispute",  "amount": 1000,  "balance_transactions": [],  "charge": "ch_1AZtxr2eZvKYlo2CJDX8whov",  "created": 1680651737,  "currency": "usd",  "evidence": {    "access_activity_log": null,    "billing_address": null,    "cancellation_policy": null,    "cancellation_policy_disclosure": null,    "cancellation_rebuttal": null,    "customer_communication": null,    "customer_email_address": null,    "customer_name": null,    "customer_purchase_ip": null,    "customer_signature": null,    "duplicate_charge_documentation": null,    "duplicate_charge_explanation": null,    "duplicate_charge_id": null,    "product_description": null,    "receipt": null,    "refund_policy": null,    "refund_policy_disclosure": null,    "refund_refusal_explanation": null,    "service_date": null,    "service_documentation": null,    "shipping_address": null,    "shipping_carrier": null,    "shipping_date": null,    "shipping_documentation": null,    "shipping_tracking_number": null,    "uncategorized_file": null,    "uncategorized_text": null  },  "evidence_details": {    "due_by": 1682294399,    "has_evidence": false,    "past_due": false,    "submission_count": 0  },  "is_charge_refundable": true,  "livemode": false,  "metadata": {},  "payment_intent": null,  "reason": "general",  "status": "warning_needs_response"}
```

---

## Retrieve a payout

**URL:** https://docs.stripe.com/api/payouts/retrieve

**Contents:**
- Retrieve a payout
  - Parameters
  - Returns
- List all payouts
  - Parameters
    - statusstring
  - More parametersExpand all
    - arrival_dateobject
    - createdobject
    - destinationstring

Retrieves the details of an existing payout. Supply the unique payout ID from either a payout creation request or the payout list. Stripe returns the corresponding payout information.

Returns a payout object if a you provide a valid identifier. raises An error occurs otherwise.

Returns a list of existing payouts sent to third-party bank accounts or payouts that Stripe sent to you. The payouts return in sorted order, with the most recently created payouts appearing first.

Only return payouts that have the given status: pending, paid, failed, or canceled.

A dictionary with a data property that contains an array of up to limit payouts, starting after payout starting_after. Each entry in the array is a separate payout object. If no other payouts are available, the resulting array is empty.

You can cancel a previously created payout if its status is pending. Stripe refunds the funds to your available balance. You can’t cancel automatic Stripe payouts.

Returns the payout object if the cancellation succeeds. Returns an error if the payout is already canceled or can’t be canceled.

Reverses a payout by debiting the destination bank account. At this time, you can only reverse payouts for connected accounts to US and Canadian bank accounts. If the payout is manual and in the pending status, use /v1/payouts/:id/cancel instead.

By requesting a reversal through /v1/payouts/:id/reverse, you confirm that the authorized signatory of the selected bank account authorizes the debit on the bank account and that no other authorization is required.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the reversing payout object if the reversal is successful. Returns an error if the payout is already reversed or can’t be reversed.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payouts/po_1OaFDbEcg9tTZuTgNYmX0PKB \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payouts/po_1OaFDbEcg9tTZuTgNYmX0PKB \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "po_1OaFDbEcg9tTZuTgNYmX0PKB",  "object": "payout",  "amount": 1100,  "arrival_date": 1680652800,  "automatic": false,  "balance_transaction": "txn_1OaFDcEcg9tTZuTgYMR25tSe",  "created": 1680648691,  "currency": "usd",  "description": null,  "destination": "ba_1MtIhL2eZvKYlo2CAElKwKu2",  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "livemode": false,  "metadata": {},  "method": "standard",  "original_payout": null,  "reconciliation_status": "not_applicable",  "reversed_by": null,  "source_type": "card",  "statement_descriptor": null,  "status": "pending",  "type": "bank_account"}
```

Example 4 (unknown):
```unknown
{  "id": "po_1OaFDbEcg9tTZuTgNYmX0PKB",  "object": "payout",  "amount": 1100,  "arrival_date": 1680652800,  "automatic": false,  "balance_transaction": "txn_1OaFDcEcg9tTZuTgYMR25tSe",  "created": 1680648691,  "currency": "usd",  "description": null,  "destination": "ba_1MtIhL2eZvKYlo2CAElKwKu2",  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "livemode": false,  "metadata": {},  "method": "standard",  "original_payout": null,  "reconciliation_status": "not_applicable",  "reversed_by": null,  "source_type": "card",  "statement_descriptor": null,  "status": "pending",  "type": "bank_account"}
```

---

## Payment Method Domains

**URL:** https://docs.stripe.com/api/payment_method_domains

**Contents:**
- Payment Method Domains
- The PaymentMethodDomain object
  - Attributes
    - idstring
    - domain_namestring
    - enabledboolean
  - More attributesExpand all
    - objectstring
    - amazon_payobject
    - apple_payobject

A payment method domain represents a web domain that you have registered with Stripe. Stripe Elements use registered payment method domains to control where certain payment methods are shown.

Related guide: Payment method domains.

Unique identifier for the object.

The domain name that this payment method domain object represents.

Whether this payment method domain is enabled. If the domain is not enabled, payment methods that require a payment method domain will not appear in Elements.

Creates a payment method domain.

The domain name that this payment method domain object represents.

Whether this payment method domain is enabled. If the domain is not enabled, payment methods that require a payment method domain will not appear in Elements or Embedded Checkout.

Returns a payment method domain object.

Updates an existing payment method domain.

Whether this payment method domain is enabled. If the domain is not enabled, payment methods that require a payment method domain will not appear in Elements or Embedded Checkout.

Returns the updated payment method domain object.

Retrieves the details of an existing payment method domain.

Returns a payment method domain object.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "pmd_1Nnrer2eZvKYlo2Cips79tWl",  "object": "payment_method_domain",  "apple_pay": {    "status": "active"  },  "created": 1694129445,  "domain_name": "example.com",  "enabled": true,  "google_pay": {    "status": "active"  },  "link": {    "status": "active"  },  "livemode": false,  "paypal": {    "status": "active"  }}
```

Example 2 (unknown):
```unknown
{  "id": "pmd_1Nnrer2eZvKYlo2Cips79tWl",  "object": "payment_method_domain",  "apple_pay": {    "status": "active"  },  "created": 1694129445,  "domain_name": "example.com",  "enabled": true,  "google_pay": {    "status": "active"  },  "link": {    "status": "active"  },  "livemode": false,  "paypal": {    "status": "active"  }}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_method_domains \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d domain_name="example.com"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_method_domains \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d domain_name="example.com"
```

---

## Confirm a PaymentIntent

**URL:** https://docs.stripe.com/api/payment_intents/confirm

**Contents:**
- Confirm a PaymentIntent
  - Parameters
    - payment_methodstring
    - receipt_emailstring
    - setup_future_usageenum
    - shippingobject
  - More parametersExpand all
    - amount_detailsobject
    - capture_methodenumsecret key only
    - confirmation_tokenstring

Confirm that your customer intends to pay with current or provided payment method. Upon confirmation, the PaymentIntent will attempt to initiate a payment.

If the selected payment method requires additional authentication steps, the PaymentIntent will transition to the requires_action status and suggest additional actions via next_action. If payment fails, the PaymentIntent transitions to the requires_payment_method status or the canceled status if the confirmation limit is reached. If payment succeeds, the PaymentIntent will transition to the succeeded status (or requires_capture, if capture_method is set to manual).

If the confirmation_method is automatic, payment may be attempted using our client SDKs and the PaymentIntent’s client_secret. After next_actions are handled by the client, no additional confirmation is required to complete the payment.

If the confirmation_method is manual, all payment attempts must be initiated using a secret key.

If any actions are required for the payment, the PaymentIntent will return to the requires_confirmation state after those actions are completed. Your server needs to then explicitly re-confirm the PaymentIntent to initiate the next payment attempt.

There is a variable upper limit on how many times a PaymentIntent can be confirmed. After this limit is reached, any further calls to this endpoint will transition the PaymentIntent to the canceled state.

ID of the payment method (a PaymentMethod, Card, or compatible Source object) to attach to this PaymentIntent. If the payment method is attached to a Customer, it must match the customer that is set on this PaymentIntent.

Email address that the receipt for the resulting payment will be sent to. If receipt_email is specified for a payment in live mode, a receipt will be sent regardless of your email settings.

Indicates that you intend to make future payments with this PaymentIntent’s payment method.

If you provide a Customer with the PaymentIntent, you can use this parameter to attach the payment method to the Customer after the PaymentIntent is confirmed and the customer completes any required actions. If you don’t provide a Customer, you can still attach the payment method to a Customer after the transaction completes.

If the payment method is card_present and isn’t a digital wallet, Stripe creates and attaches a generated_card payment method representing the card to the Customer instead.

When processing card payments, Stripe uses setup_future_usage to help you comply with regional legislation and network rules, such as SCA.

If you’ve already set setup_future_usage and you’re performing a request using a publishable key, you can only update the value from on_session to off_session.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

Shipping information for this PaymentIntent.

Returns the resulting PaymentIntent after all possible transitions are applied.

Perform an incremental authorization on an eligible PaymentIntent. To be eligible, the PaymentIntent’s status must be requires_capture and incremental_authorization_supported must be true.

Incremental authorizations attempt to increase the authorized amount on your customer’s card to the new, higher amount provided. Similar to the initial authorization, incremental authorizations can be declined. A single PaymentIntent can call this endpoint multiple times to further increase the authorized amount.

If the incremental authorization succeeds, the PaymentIntent object returns with the updated amount. If the incremental authorization fails, a card_declined error returns, and no other fields on the PaymentIntent or Charge update. The PaymentIntent object remains capturable for the previously authorized amount.

Each PaymentIntent can have a maximum of 10 incremental authorization attempts, including declines. After it’s captured, a PaymentIntent can no longer be incremented.

Learn more about incremental authorizations.

The updated total amount that you intend to collect from the cardholder. This amount must be greater than the currently authorized amount.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Text that appears on the customer’s statement as the statement descriptor for a non-card or card charge. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

Returns a PaymentIntent object with the updated amount if the incremental authorization succeeds. Returns an error if the incremental authorization failed or the PaymentIntent isn’t eligible for incremental authorizations.

Manually reconcile the remaining amount for a customer_balance PaymentIntent.

Amount that you intend to apply to this PaymentIntent from the customer’s cash balance. If the PaymentIntent was created by an Invoice, the full amount of the PaymentIntent is applied regardless of this parameter.

A positive integer representing how much to charge in the smallest currency unit (for example, 100 cents to charge 1 USD or 100 to charge 100 JPY, a zero-decimal currency). The maximum amount is the amount of the PaymentIntent.

When you omit the amount, it defaults to the remaining amount requested on the PaymentIntent.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

Returns a PaymentIntent object.

Search for PaymentIntents you’ve previously created using Stripe’s Search Query Language. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.

The search query string. See search query language and the list of supported query fields for payment intents.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A dictionary with a data property that contains an array of up to limit PaymentIntents. If no objects match the query, the resulting array will be empty. See the related guide on expanding properties in lists.

Verifies microdeposits on a PaymentIntent object.

Two positive integers, in cents, equal to the values of the microdeposits sent to the bank account.

A six-character code starting with SM present in the microdeposit sent to the bank account.

Returns a PaymentIntent object.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents/pi_3MtweELkdIwHu7ix0Dt0gF2H/confirm \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d payment_method=pm_card_visa \  --data-urlencode return_url="https://www.example.com"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents/pi_3MtweELkdIwHu7ix0Dt0gF2H/confirm \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d payment_method=pm_card_visa \  --data-urlencode return_url="https://www.example.com"
```

Example 3 (unknown):
```unknown
{  "id": "pi_3MtweELkdIwHu7ix0Dt0gF2H",  "object": "payment_intent",  "amount": 2000,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 2000,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": {    "enabled": true  },  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_3MtweELkdIwHu7ix0Dt0gF2H_secret_ALlpPMIZse0ac8YzPxkMkFgGC",  "confirmation_method": "automatic",  "created": 1680802258,  "currency": "usd",  "customer": null,  "description": null,  "last_payment_error": null,  "latest_charge": "ch_3MtweELkdIwHu7ix05lnLAFd",  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": "pm_1MtweELkdIwHu7ixxrsejPtG",  "payment_method_options": {    "card": {      "installments": null,      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    },    "link": {      "persistent_token": null    }  },  "payment_method_types": [    "card",    "link"  ],  "processing": null,  "receipt_email": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "source": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "succeeded",  "transfer_data": null,  "transfer_group": null}
```

Example 4 (unknown):
```unknown
{  "id": "pi_3MtweELkdIwHu7ix0Dt0gF2H",  "object": "payment_intent",  "amount": 2000,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 2000,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": {    "enabled": true  },  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_3MtweELkdIwHu7ix0Dt0gF2H_secret_ALlpPMIZse0ac8YzPxkMkFgGC",  "confirmation_method": "automatic",  "created": 1680802258,  "currency": "usd",  "customer": null,  "description": null,  "last_payment_error": null,  "latest_charge": "ch_3MtweELkdIwHu7ix05lnLAFd",  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": "pm_1MtweELkdIwHu7ixxrsejPtG",  "payment_method_options": {    "card": {      "installments": null,      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    },    "link": {      "persistent_token": null    }  },  "payment_method_types": [    "card",    "link"  ],  "processing": null,  "receipt_email": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "source": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "succeeded",  "transfer_data": null,  "transfer_group": null}
```

---

## File Links

**URL:** https://docs.stripe.com/api/file_links

**Contents:**
- File Links
- The File Link object
  - Attributes
    - idstring
    - expires_atnullable timestamp
    - filestringExpandable
    - metadataobject
    - urlnullable string
  - More attributesExpand all
    - objectstring

To share the contents of a File object with non-Stripe users, you can create a FileLink. FileLinks contain a URL that you can use to retrieve the contents of the file without authentication.

Unique identifier for the object.

Time that the link expires.

The file object this link points to.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The publicly accessible URL to download the file.

Creates a new file link object.

The ID of the file. The file’s purpose must be one of the following: business_icon, business_logo, customer_signature, dispute_evidence, finance_report_run, financial_account_statement, identity_document_downloadable, issuing_regulatory_reporting, pci_document, selfie, sigma_scheduled_query, tax_document_user_upload, terminal_android_apk, or terminal_reader_splashscreen.

The link isn’t usable after this future timestamp.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the file link object if successful and raises an error otherwise.

Updates an existing file link object. Expired links can no longer be updated.

A future timestamp after which the link will no longer be usable, or now to expire the link immediately.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the file link object if successful, and raises an error otherwise.

Retrieves the file link with the given ID.

If the identifier you provide is valid, a file link object returns. If not, Stripe raises an error.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "link_1Mr23jLkdIwHu7ix65betcoo",  "object": "file_link",  "created": 1680108075,  "expired": false,  "expires_at": null,  "file": "file_1Mr23iLkdIwHu7ixQkCV3CBR",  "livemode": false,  "metadata": {},  "url": "https://files.stripe.com/links/MDB8YWNjdF8xTTJKVGtMa2RJd0h1N2l4fGZsX3Rlc3RfaXVoY2hrUnJPMzlBR3dPb01XMmFkSTVq00yUPLFf3h"}
```

Example 2 (unknown):
```unknown
{  "id": "link_1Mr23jLkdIwHu7ix65betcoo",  "object": "file_link",  "created": 1680108075,  "expired": false,  "expires_at": null,  "file": "file_1Mr23iLkdIwHu7ixQkCV3CBR",  "livemode": false,  "metadata": {},  "url": "https://files.stripe.com/links/MDB8YWNjdF8xTTJKVGtMa2RJd0h1N2l4fGZsX3Rlc3RfaXVoY2hrUnJPMzlBR3dPb01XMmFkSTVq00yUPLFf3h"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/file_links \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d file=file_1Mr23iLkdIwHu7ixQkCV3CBR
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/file_links \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d file=file_1Mr23iLkdIwHu7ixQkCV3CBR
```

---

## Place hardware orders

**URL:** https://docs.stripe.com/terminal/fleet/order-and-return-readers

**Contents:**
- Place hardware orders
- Learn how to place orders for reader hardware and accessories.
  - Shop now
- What to buy
  - Pricing
- Track and cancel orders
- Self service returns
  - Countries supporting self service returns
- Selecting the Return items Button
- Confirming the number of units to be returned

Ready to buy? Browse available readers and accessories.

Order pre-certified readers compatible with Stripe Terminal from your Dashboard or using the Stripe API. Purchase readers directly from Stripe so they’re loaded with Stripe’s payment applications and secure encryption keys.

To get started, go to the Readers section in your Dashboard. Click Shop to view available products.

First, order a reader and a test card to test your full integration with physical hardware. When your integration is ready, order as many readers as you need.

Not sure which reader you need? See Designing an Integration to choose one for your integration.

You can order up to 10000 of each item in a single order. If you’re interested in volume discounts, you can contact us.

The price for each reader varies by country. You can view the most updated pricing in the Dashboard.

After placing an order, check its status in the Dashboard:

Self service returns are for orders placed and shipped within specific countries (see countries below). See the information about returns outside of supported self service countries for all other orders.

If you’ve placed an order in the Stripe Dashboard within a country supporting self service and need to return some or all of the items in your order, users with sufficient permission can initiate the return within the Stripe Dashboard. We can accept refunds for orders in original packaging (along with all accessories) within 30 days of the date of purchase. For returns past 30 days, please contact Stripe Support.

Going through the flow in the Dashboard produces a return shipping label. After you create the return shipping label, you can drop your package off at a local shipping carrier.

Stripe refunds the payment when our distribution facility receives the package. For credit cards, the process can take up to 10 days for the funds to be returned to the bank account.

To initiate a Dashboard Return, go to your Hardware Orders and select the order you want to return. After you select the order, click Return items to start the process. The Return items button is available on the Terminal order details page if the hardware order has a status of Shipped or Delivered.

When the popup opens, select the number of items you’d like to return for each product in the order (if you have more than one item). We’ll only show the number of items eligible for return. So, if you previously purchased three items and returned one, you’ll only be able to select up to two units to return.

The popup displays the amount to be refunded after you select the desired number of items.

Shipping fees are refunded on the first initiated return for a Terminal hardware order. For example, if you bought three readers and then returned one unit through a partial refund, then decided to return another unit, the second Dashboard return shows $0 for shipping fees to be refunded because these fees were returned in the first attempt.

Next, you need to select a reason for the return from the dropdown menu.

After you’ve confirmed the information is correct, select Submit return’—the option to download the shipping label appears after you select it. You can select View UPS Locations to find the nearest drop off location.

After the return is processed, you’ll be redirected back to the order details page. You can download the shipping label again from the details page if needed. Stripe issues a refund to the payment method you provided when we receive the return.

To return a device where self service returns isn’t available, contact support. Go to your order in the Dashboard and click Contact support to automatically send us your order details. We can accept refunds for orders in original packaging (along with all accessories) within 30 days of the date of purchase.

Stripe works with a distribution partner to fulfill Terminal orders. You can choose standard, express, or priority shipping, depending on the destination country. Hardware must be shipped to physical addresses (not PO boxes).

If you’re a Connect platform using Terminal, you can ship readers directly to your connected accounts by specifying the destination address during checkout.

You can add tax identification numbers in your Terminal settings. Stripe uses tax IDs you provide to apply tax on hardware orders, and includes them in tax invoices and credit notes. Each non-US order generates a tax invoice—you can find them by clicking on the orders listed in hardware orders.

The following table shows which user roles can place orders on behalf of their account through the dashboard:

The Terminal Hardware Ordering API is currently in preview. If you’re interested in gaining access, contact your sales representative, and they’ll assess your eligibility.

To qualify for preview access, you must:

The Terminal Hardware Orders API enables you to programmatically purchase Terminal readers and accessories that can be sent directly to your users. Orders are fulfilled by Stripe’s distribution partners, so you don’t have to manage complex logistics and can instead focus on building your in-person payments business.

To create a hardware order using the API, follow these steps:

You must include a beta header in your API requests with your API version and the current version of the terminal hardware order preview: Stripe-Version: 2025-12-15.clover;terminal_hardware_orders_beta=v5

To render an appropriate product page for users, your integration must request available items from Stripe. Each item is represented as a SKU and includes details about the product, such as the product token and price.

Each SKU is associated with a country: a reader available in the US has a different SKU from the same reader that’s available in Canada. To retrieve SKUs, you must specify the country parameter when making a request to the Hardware Order SKUs endpoint:

Each SKU is also associated with a Hardware Product. Products represent different categories of devices. If you’re building an e-commerce ordering system for your customers, make sure you only show the SKUs for the products that apply for your Terminal integration. For example, if your Terminal integration only uses the BBPOS WisePOS E, don’t make the BBPOS Chipper 2X BT reader available for purchase. To retrieve all BBPOS WisePOS E SKUs, you can specify the optional product parameter when making a request to the Hardware Order SKUs endpoint:

Finally, each SKU is also associated with a Provider. By default this value is set to stripe but you filter for SKUs from a different provider by specifying the optional provider parameter when making a request to the Hardware Order SKUs endpoint. All SKUs and Shipping Methods in an Order must share the same provider.

SKUs and Products might become obsolete as we replace them with newer hardware. To help you manage planned obsolescence, see the SKU and Product status that indicates which are currently available or unavailable. You can’t create an Order if the SKU status is unavailable.

Additionally, each SKU and Product has an optional unavailable_after field that indicates when it might become unavailable. Because the availabilities of these objects change over time, we recommend using an approach to query them dynamically. You can do this either by making a query before displaying the available objects to your users, or periodically (every day, for example) and caching the results you present to your users.

We don’t recommend hardcoding the tokens for these objects because such an integration requires code changes when a shipping method becomes unavailable. If you don’t perform these changes in time, you might attempt to place orders with unavailable objects, causing errors.

Another required object used as an input for creating an order is the Hardware Shipping Method. This object determines the estimated shipping time for your order as well as a portion of the price. You must use a Shipping Method available in country of the shipping address when creating an order.

Like SKUs, each Shipping Method is associated with a country: the shipping methods available in the US might be different from those available in Canada. Each Shipping Method also has a name, which denotes the basic category for this shipping method, as well as a provider. To retrieve Shipping Methods, you must specify the country and can optionally specify the name or provider parameters when making a request to the Hardware Shipping Methods endpoint:

Like SKUs and Products, Shipping Methods might change over time. To help you manage these changes, each Shipping Method has a status that indicates whether it’s currently available or unavailable. This mechanism works the same way as it does for SKUs and Products, as described above. As with SKUs and Products, we recommend fetching Shipping Methods periodically so your integration doesn’t become out of date.

To preview a hardware order, make a request to Stripe containing the SKUs, quantities, shipping address, and Shipping Method for the order.

Previewing an order allows you to perform validation on the order and determine the overall cost of the taxes associated with the order without actually placing it, which you can use for designing an e-commerce checkout page for your customers. Calling the preview endpoint doesn’t actually create an order.

Try to minimize the time between making a request to Preview Hardware Order and Create Hardware Order to reduce the (very unlikely) chance that prices change in the interim. If you’re concerned about this issue you can save the preview and create an order using the same parameters. Then you can compare the saved preview with the order and cancel the order in the event of any changes.

To create a Terminal Hardware Order, you can make a Create Hardware Order request to Stripe that looks very similar to the Preview Hardware Order request. Include the SKUs, quantities, shipping address, and Shipping Method for the order in your request.

The below example shows a US phone number. If the phone number provided by shipping.phone parameter is an international phone number, prefix it with an escaped version of the + sign (for example: shipping[phone]="%2B358131234567" instead of shipping[phone]="+358131234567").

The email address provided by the shipping.email parameter receives Stripe-branded update emails when the status of the order changes. Use an email address that you feel comfortable receiving Stripe-branded emails.

After creating an order, you can Retrieve a Terminal Hardware Order using the following request.

You can also List all Terminal Hardware Orders.

You can set up webhook events to be updated about order state transitions. You must add a header version (for example, Stripe-Version: 2025-12-15.clover;terminal_hardware_orders_beta=v5) to your webhook endpoints to receive events properly. We support the following webhook events:

You can update the status of a terminal hardware order in a sandbox using the following endpoints in the API:

You can only update the status for terminal hardware orders in a sandbox.

Upon order creation, Stripe returns the tax amounts associated with the order. We calculate these amounts based on the tax owed to Stripe for the purchase. If you charge tax to your end users for orders placed using the API, you can calculate the amounts owed to you and convey those amounts to your users. The amounts owed to you might differ from those owed to Stripe.

For Italian Tax Invoices, please visit the Italian Tax Portal to view invoices.

During preview, Stripe sends monthly invoices for any orders created with the API. You can change the email that receives invoices in the Dashboard.

As mentioned in the Shipping section, Stripe works with a distribution partner to fulfill Terminal orders. When our distribution partner gets tracking information for the order it transions to the shipped state. You can set up a webhook endpoint for the terminal_hardware_order.shipped notification to be notified when an order has a tracking number.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/hardware_skus?country=US \
  -u sk_test_YOUR_TEST_KEY_HERE: \
  -H "Stripe-Version: 2025-12-15.clover;terminal_hardware_orders_beta=v5"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/hardware_skus?country=US \
  -u sk_test_YOUR_TEST_KEY_HERE: \
  -H "Stripe-Version: 2025-12-15.clover;terminal_hardware_orders_beta=v5"
```

Example 3 (unknown):
```unknown
curl 'https://api.stripe.com/v1/terminal/hardware_skus?country=US&product={{TERMINAL_HARDWARE_PRODUCT_ID}}' \
  -u sk_test_YOUR_TEST_KEY_HERE: \
  -H "Stripe-Version: 2025-12-15.clover;terminal_hardware_orders_beta=v5"
```

Example 4 (unknown):
```unknown
curl 'https://api.stripe.com/v1/terminal/hardware_skus?country=US&product={{TERMINAL_HARDWARE_PRODUCT_ID}}' \
  -u sk_test_YOUR_TEST_KEY_HERE: \
  -H "Stripe-Version: 2025-12-15.clover;terminal_hardware_orders_beta=v5"
```

---

## Payment Intents

**URL:** https://docs.stripe.com/api/payment_intents

**Contents:**
- Payment Intents
- The PaymentIntent object
  - Attributes
    - idstringretrievable with publishable key
    - amountintegerretrievable with publishable key
    - automatic_payment_methodsnullable objectretrievable with publishable key
    - client_secretnullable stringretrievable with publishable key
    - currencyenumretrievable with publishable key
    - customernullable stringExpandable
    - customer_accountnullable string

A PaymentIntent guides you through the process of collecting a payment from your customer. We recommend that you create exactly one PaymentIntent for each order or customer session in your system. You can reference the PaymentIntent later to see the history of payment attempts for a particular session.

A PaymentIntent transitions through multiple statuses throughout its lifetime as it interfaces with Stripe.js to perform authentication flows and ultimately creates at most one successful charge.

Related guide: Payment Intents API

Unique identifier for the object.

Amount intended to be collected by this PaymentIntent. A positive integer representing how much to charge in the smallest currency unit (e.g., 100 cents to charge $1.00 or 100 to charge ¥100, a zero-decimal currency). The minimum amount is $0.50 US or equivalent in charge currency. The amount value supports up to eight digits (e.g., a value of 99999999 for a USD charge of $999,999.99).

Settings to configure compatible payment methods from the Stripe Dashboard

The client secret of this PaymentIntent. Used for client-side retrieval using a publishable key.

The client secret can be used to complete a payment from your frontend. It should not be stored, logged, or exposed to anyone other than the customer. Make sure that you have TLS enabled on any page that includes the client secret.

Refer to our docs to accept a payment and learn about how client_secret should be handled.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

ID of the Customer this PaymentIntent belongs to, if one exists.

Payment methods attached to other Customers cannot be used with this PaymentIntent.

If setup_future_usage is set and this PaymentIntent’s payment method is not card_present, then the payment method attaches to the Customer after the PaymentIntent has been confirmed and any required actions from the user are complete. If the payment method is card_present and isn’t a digital wallet, then a generated_card payment method representing the card is created and attached to the Customer instead.

ID of the Account representing the customer that this PaymentIntent belongs to, if one exists.

Payment methods attached to other Accounts cannot be used with this PaymentIntent.

If setup_future_usage is set and this PaymentIntent’s payment method is not card_present, then the payment method attaches to the Account after the PaymentIntent has been confirmed and any required actions from the user are complete. If the payment method is card_present and isn’t a digital wallet, then a generated_card payment method representing the card is created and attached to the Account instead.

An arbitrary string attached to the object. Often useful for displaying to users.

The payment error encountered in the previous PaymentIntent confirmation. It will be cleared if the PaymentIntent is later updated for any reason.

ID of the latest Charge object created by this PaymentIntent. This property is null until PaymentIntent confirmation is attempted.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Learn more about storing information in metadata.

If present, this property tells you what actions you need to take in order for your customer to fulfill a payment using the provided source.

ID of the payment method used in this PaymentIntent.

Email address that the receipt for the resulting payment will be sent to. If receipt_email is specified for a payment in live mode, a receipt will be sent regardless of your email settings.

Indicates that you intend to make future payments with this PaymentIntent’s payment method.

If you provide a Customer with the PaymentIntent, you can use this parameter to attach the payment method to the Customer after the PaymentIntent is confirmed and the customer completes any required actions. If you don’t provide a Customer, you can still attach the payment method to a Customer after the transaction completes.

If the payment method is card_present and isn’t a digital wallet, Stripe creates and attaches a generated_card payment method representing the card to the Customer instead.

When processing card payments, Stripe uses setup_future_usage to help you comply with regional legislation and network rules, such as SCA.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

Shipping information for this PaymentIntent.

Text that appears on the customer’s statement as the statement descriptor for a non-card charge. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

Setting this value for a card charge returns an error. For card charges, set the statement_descriptor_suffix instead.

Provides information about a card charge. Concatenated to the account’s statement descriptor prefix to form the complete statement descriptor that appears on the customer’s statement.

Status of this PaymentIntent, one of requires_payment_method, requires_confirmation, requires_action, processing, requires_capture, canceled, or succeeded. Read more about each PaymentIntent status.

The PaymentIntent has been canceled.

The PaymentIntent is currently being processed.

The PaymentIntent requires additional action from the customer.

The PaymentIntent has been confirmed and requires capture.

The PaymentIntent requires confirmation.

The PaymentIntent requires a payment method to be attached.

The PaymentIntent has succeeded.

Creates a PaymentIntent object.

After the PaymentIntent is created, attach a payment method and confirm to continue the payment. Learn more about the available payment flows with the Payment Intents API.

When you use confirm=true during creation, it’s equivalent to creating and confirming the PaymentIntent in the same call. You can use any parameters available in the confirm API when you supply confirm=true.

Amount intended to be collected by this PaymentIntent. A positive integer representing how much to charge in the smallest currency unit (e.g., 100 cents to charge $1.00 or 100 to charge ¥100, a zero-decimal currency). The minimum amount is $0.50 US or equivalent in charge currency. The amount value supports up to eight digits (e.g., a value of 99999999 for a USD charge of $999,999.99).

Three-letter ISO currency code, in lowercase. Must be a supported currency.

When you enable this parameter, this PaymentIntent accepts payment methods that you enable in the Dashboard and that are compatible with this PaymentIntent’s other parameters.

Set to true to attempt to confirm this PaymentIntent immediately. This parameter defaults to false. When creating and confirming a PaymentIntent at the same time, you can also provide the parameters available in the Confirm API.

ID of the Customer this PaymentIntent belongs to, if one exists.

Payment methods attached to other Customers cannot be used with this PaymentIntent.

If setup_future_usage is set and this PaymentIntent’s payment method is not card_present, then the payment method attaches to the Customer after the PaymentIntent has been confirmed and any required actions from the user are complete. If the payment method is card_present and isn’t a digital wallet, then a generated_card payment method representing the card is created and attached to the Customer instead.

ID of the Account representing the customer that this PaymentIntent belongs to, if one exists.

Payment methods attached to other Accounts cannot be used with this PaymentIntent.

If setup_future_usage is set and this PaymentIntent’s payment method is not card_present, then the payment method attaches to the Account after the PaymentIntent has been confirmed and any required actions from the user are complete. If the payment method is card_present and isn’t a digital wallet, then a generated_card payment method representing the card is created and attached to the Account instead.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Set to true to indicate that the customer isn’t in your checkout flow during this payment attempt and can’t authenticate. Use this parameter in scenarios where you collect card details and charge them later. This parameter can only be used with confirm=true.

ID of the payment method (a PaymentMethod, Card, or compatible Source object) to attach to this PaymentIntent.

If you omit this parameter with confirm=true, customer.default_source attaches as this PaymentIntent’s payment instrument to improve migration for users of the Charges API. We recommend that you explicitly provide the payment_method moving forward. If the payment method is attached to a Customer, you must also provide the ID of that Customer as the customer parameter of this PaymentIntent.

Email address to send the receipt to. If you specify receipt_email for a payment in live mode, you send a receipt regardless of your email settings.

Indicates that you intend to make future payments with this PaymentIntent’s payment method.

If you provide a Customer with the PaymentIntent, you can use this parameter to attach the payment method to the Customer after the PaymentIntent is confirmed and the customer completes any required actions. If you don’t provide a Customer, you can still attach the payment method to a Customer after the transaction completes.

If the payment method is card_present and isn’t a digital wallet, Stripe creates and attaches a generated_card payment method representing the card to the Customer instead.

When processing card payments, Stripe uses setup_future_usage to help you comply with regional legislation and network rules, such as SCA.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

Shipping information for this PaymentIntent.

Text that appears on the customer’s statement as the statement descriptor for a non-card charge. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

Setting this value for a card charge returns an error. For card charges, set the statement_descriptor_suffix instead.

Provides information about a card charge. Concatenated to the account’s statement descriptor prefix to form the complete statement descriptor that appears on the customer’s statement.

Returns a PaymentIntent object.

Updates properties on a PaymentIntent object without confirming.

Depending on which properties you update, you might need to confirm the PaymentIntent again. For example, updating the payment_method always requires you to confirm the PaymentIntent again. If you prefer to update and confirm at the same time, we recommend updating properties through the confirm API instead.

Amount intended to be collected by this PaymentIntent. A positive integer representing how much to charge in the smallest currency unit (e.g., 100 cents to charge $1.00 or 100 to charge ¥100, a zero-decimal currency). The minimum amount is $0.50 US or equivalent in charge currency. The amount value supports up to eight digits (e.g., a value of 99999999 for a USD charge of $999,999.99).

Three-letter ISO currency code, in lowercase. Must be a supported currency.

ID of the Customer this PaymentIntent belongs to, if one exists.

Payment methods attached to other Customers cannot be used with this PaymentIntent.

If setup_future_usage is set and this PaymentIntent’s payment method is not card_present, then the payment method attaches to the Customer after the PaymentIntent has been confirmed and any required actions from the user are complete. If the payment method is card_present and isn’t a digital wallet, then a generated_card payment method representing the card is created and attached to the Customer instead.

ID of the Account representing the customer that this PaymentIntent belongs to, if one exists.

Payment methods attached to other Accounts cannot be used with this PaymentIntent.

If setup_future_usage is set and this PaymentIntent’s payment method is not card_present, then the payment method attaches to the Account after the PaymentIntent has been confirmed and any required actions from the user are complete. If the payment method is card_present and isn’t a digital wallet, then a generated_card payment method representing the card is created and attached to the Account instead.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

ID of the payment method (a PaymentMethod, Card, or compatible Source object) to attach to this PaymentIntent. To unset this field to null, pass in an empty string.

Email address that the receipt for the resulting payment will be sent to. If receipt_email is specified for a payment in live mode, a receipt will be sent regardless of your email settings.

Indicates that you intend to make future payments with this PaymentIntent’s payment method.

If you provide a Customer with the PaymentIntent, you can use this parameter to attach the payment method to the Customer after the PaymentIntent is confirmed and the customer completes any required actions. If you don’t provide a Customer, you can still attach the payment method to a Customer after the transaction completes.

If the payment method is card_present and isn’t a digital wallet, Stripe creates and attaches a generated_card payment method representing the card to the Customer instead.

When processing card payments, Stripe uses setup_future_usage to help you comply with regional legislation and network rules, such as SCA.

If you’ve already set setup_future_usage and you’re performing a request using a publishable key, you can only update the value from on_session to off_session.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

Shipping information for this PaymentIntent.

Text that appears on the customer’s statement as the statement descriptor for a non-card charge. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

Setting this value for a card charge returns an error. For card charges, set the statement_descriptor_suffix instead.

Provides information about a card charge. Concatenated to the account’s statement descriptor prefix to form the complete statement descriptor that appears on the customer’s statement.

Returns a PaymentIntent object.

Retrieves the details of a PaymentIntent that has previously been created.

You can retrieve a PaymentIntent client-side using a publishable key when the client_secret is in the query string.

If you retrieve a PaymentIntent with a publishable key, it only returns a subset of properties. Refer to the payment intent object reference for more details.

The client secret of the PaymentIntent. We require it if you use a publishable key to retrieve the source.

Returns a PaymentIntent if a valid identifier was provided.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",  "object": "payment_intent",  "amount": 2000,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 0,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": {    "enabled": true  },  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",  "confirmation_method": "automatic",  "created": 1680800504,  "currency": "usd",  "customer": null,  "description": null,  "last_payment_error": null,  "latest_charge": null,  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": null,  "payment_method_options": {    "card": {      "installments": null,      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    },    "link": {      "persistent_token": null    }  },  "payment_method_types": [    "card",    "link"  ],  "processing": null,  "receipt_email": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "source": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "requires_payment_method",  "transfer_data": null,  "transfer_group": null}
```

Example 2 (unknown):
```unknown
{  "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",  "object": "payment_intent",  "amount": 2000,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 0,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": {    "enabled": true  },  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",  "confirmation_method": "automatic",  "created": 1680800504,  "currency": "usd",  "customer": null,  "description": null,  "last_payment_error": null,  "latest_charge": null,  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": null,  "payment_method_options": {    "card": {      "installments": null,      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    },    "link": {      "persistent_token": null    }  },  "payment_method_types": [    "card",    "link"  ],  "processing": null,  "receipt_email": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "source": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "requires_payment_method",  "transfer_data": null,  "transfer_group": null}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=2000 \  -d currency=usd \  -d "automatic_payment_methods[enabled]"=true
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=2000 \  -d currency=usd \  -d "automatic_payment_methods[enabled]"=true
```

---

## Customer Portal Configuration

**URL:** https://docs.stripe.com/api/customer_portal/configurations

**Contents:**
- Customer Portal Configuration
- The Customer portal configuration object
  - Attributes
    - idstring
    - objectstring
    - activeboolean
    - applicationnullable stringExpandableConnect only
    - business_profileobject
    - createdtimestamp
    - default_return_urlnullable string

A portal configuration describes the functionality and behavior you embed in a portal session. Related guide: Configure the customer portal.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value.

Whether the configuration is active and can be used to create portal sessions.

ID of the Connect Application that created the configuration.

The business information shown to customers in the portal.

Time at which the object was created. Measured in seconds since the Unix epoch.

The default URL to redirect customers to when they click on the portal’s link to return to your website. This can be overriden when creating the session.

Information about the features available in the portal.

Whether the configuration is the default. If true, this configuration can be managed in the Dashboard and portal sessions will use this configuration unless it is overriden when creating the session.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The hosted login page for this configuration. Learn more about the portal login page in our integration docs.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The name of the configuration.

Time at which the object was last updated. Measured in seconds since the Unix epoch.

Creates a configuration that describes the functionality and behavior of a PortalSession

Information about the features available in the portal.

The business information shown to customers in the portal.

The default URL to redirect customers to when they click on the portal’s link to return to your website. This can be overriden when creating the session.

The hosted login page for this configuration. Learn more about the portal login page in our integration docs.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The name of the configuration.

The maximum length is 256 characters.

Returns a portal configuration object.

Updates a configuration that describes the functionality of the customer portal.

Whether the configuration is active and can be used to create portal sessions.

The business information shown to customers in the portal.

The default URL to redirect customers to when they click on the portal’s link to return to your website. This can be overriden when creating the session.

Information about the features available in the portal.

The hosted login page for this configuration. Learn more about the portal login page in our integration docs.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The name of the configuration.

The maximum length is 256 characters.

Returns a portal configuration object.

Retrieves a configuration that describes the functionality of the customer portal.

Returns a portal configuration object.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "bpc_1MrnZsLkdIwHu7ixNiQL1xPM",  "object": "billing_portal.configuration",  "active": true,  "application": null,  "business_profile": {    "headline": null,    "privacy_policy_url": null,    "terms_of_service_url": null  },  "created": 1680290736,  "default_return_url": null,  "features": {    "customer_update": {      "allowed_updates": [        "email",        "tax_id"      ],      "enabled": true    },    "invoice_history": {      "enabled": true    },    "payment_method_update": {      "enabled": false    },    "subscription_cancel": {      "cancellation_reason": {        "enabled": false,        "options": [          "too_expensive",          "missing_features",          "switched_service",          "unused",          "other"        ]      },      "enabled": false,      "mode": "at_period_end",      "proration_behavior": "none"    },    "subscription_update": {      "default_allowed_updates": [],      "enabled": false,      "proration_behavior": "none"    }  },  "is_default": false,  "livemode": false,  "login_page": {    "enabled": false,    "url": null  },  "metadata": {},  "updated": 1680290736}
```

Example 2 (unknown):
```unknown
{  "id": "bpc_1MrnZsLkdIwHu7ixNiQL1xPM",  "object": "billing_portal.configuration",  "active": true,  "application": null,  "business_profile": {    "headline": null,    "privacy_policy_url": null,    "terms_of_service_url": null  },  "created": 1680290736,  "default_return_url": null,  "features": {    "customer_update": {      "allowed_updates": [        "email",        "tax_id"      ],      "enabled": true    },    "invoice_history": {      "enabled": true    },    "payment_method_update": {      "enabled": false    },    "subscription_cancel": {      "cancellation_reason": {        "enabled": false,        "options": [          "too_expensive",          "missing_features",          "switched_service",          "unused",          "other"        ]      },      "enabled": false,      "mode": "at_period_end",      "proration_behavior": "none"    },    "subscription_update": {      "default_allowed_updates": [],      "enabled": false,      "proration_behavior": "none"    }  },  "is_default": false,  "livemode": false,  "login_page": {    "enabled": false,    "url": null  },  "metadata": {},  "updated": 1680290736}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/billing_portal/configurations \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "features[customer_update][allowed_updates][]"=email \  -d "features[customer_update][allowed_updates][]"=tax_id \  -d "features[customer_update][enabled]"=true \  -d "features[invoice_history][enabled]"=true
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/billing_portal/configurations \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "features[customer_update][allowed_updates][]"=email \  -d "features[customer_update][allowed_updates][]"=tax_id \  -d "features[customer_update][enabled]"=true \  -d "features[invoice_history][enabled]"=true
```

---

## Retrieve a token

**URL:** https://docs.stripe.com/api/tokens/retrieve

**Contents:**
- Retrieve a token
  - Parameters
  - Returns

Retrieves the token with the given ID.

Returns a token if you provide a valid ID. Raises an error otherwise.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/tokens/tok_1N3T00LkdIwHu7ixt44h1F8k \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/tokens/tok_1N3T00LkdIwHu7ixt44h1F8k \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "tok_1N3T00LkdIwHu7ixt44h1F8k",  "object": "token",  "card": {    "id": "card_1N3T00LkdIwHu7ixRdxpVI1Q",    "object": "card",    "address_city": null,    "address_country": null,    "address_line1": null,    "address_line1_check": null,    "address_line2": null,    "address_state": null,    "address_zip": null,    "address_zip_check": null,    "brand": "Visa",    "country": "US",    "cvc_check": "unchecked",    "dynamic_last4": null,    "exp_month": 5,    "exp_year": 2026,    "fingerprint": "mToisGZ01V71BCos",    "funding": "credit",    "last4": "4242",    "metadata": {},    "name": null,    "tokenization_method": null,    "wallet": null  },  "client_ip": "52.35.78.6",  "created": 1683071568,  "livemode": false,  "type": "card",  "used": false}
```

Example 4 (unknown):
```unknown
{  "id": "tok_1N3T00LkdIwHu7ixt44h1F8k",  "object": "token",  "card": {    "id": "card_1N3T00LkdIwHu7ixRdxpVI1Q",    "object": "card",    "address_city": null,    "address_country": null,    "address_line1": null,    "address_line1_check": null,    "address_line2": null,    "address_state": null,    "address_zip": null,    "address_zip_check": null,    "brand": "Visa",    "country": "US",    "cvc_check": "unchecked",    "dynamic_last4": null,    "exp_month": 5,    "exp_year": 2026,    "fingerprint": "mToisGZ01V71BCos",    "funding": "credit",    "last4": "4242",    "metadata": {},    "name": null,    "tokenization_method": null,    "wallet": null  },  "client_ip": "52.35.78.6",  "created": 1683071568,  "livemode": false,  "type": "card",  "used": false}
```

---

## Retrieve a PaymentIntent

**URL:** https://docs.stripe.com/api/payment_intents/retrieve

**Contents:**
- Retrieve a PaymentIntent
  - Parameters
    - client_secretstringRequired if you use a publishable key.
  - Returns
- List all PaymentIntent LineItems
  - Parameters
  - More parametersExpand all
    - ending_beforestring
    - limitinteger
    - starting_afterstring

Retrieves the details of a PaymentIntent that has previously been created.

You can retrieve a PaymentIntent client-side using a publishable key when the client_secret is in the query string.

If you retrieve a PaymentIntent with a publishable key, it only returns a subset of properties. Refer to the payment intent object reference for more details.

The client secret of the PaymentIntent. We require it if you use a publishable key to retrieve the source.

Returns a PaymentIntent if a valid identifier was provided.

Lists all LineItems of a given PaymentIntent.

A dictionary with a data property that contains an array of up to limit line items of the given PaymentIntent, starting after line item starting_after. Each entry in the array is a separate line item object. If no other line items are available, the resulting array is empty.

Returns a list of PaymentIntents.

Only return PaymentIntents for the customer that this customer ID specifies.

Only return PaymentIntents for the account representing the customer that this ID specifies.

A dictionary with a data property that contains an array of up to limit PaymentIntents, starting after PaymentIntent starting_after. Each entry in the array is a separate PaymentIntent object. If no other PaymentIntents are available, the resulting array is empty.

You can cancel a PaymentIntent object when it’s in one of these statuses: requires_payment_method, requires_capture, requires_confirmation, requires_action or, in rare cases, processing.

After it’s canceled, no additional charges are made by the PaymentIntent and any operations on the PaymentIntent fail with an error. For PaymentIntents with a status of requires_capture, the remaining amount_capturable is automatically refunded.

You can’t cancel the PaymentIntent for a Checkout Session. Expire the Checkout Session instead.

Reason for canceling this PaymentIntent. Possible values are: duplicate, fraudulent, requested_by_customer, or abandoned

Returns a PaymentIntent object if the cancellation succeeds. Returns an error if the PaymentIntent is already canceled or isn’t in a cancelable state.

Capture the funds of an existing uncaptured PaymentIntent when its status is requires_capture.

Uncaptured PaymentIntents are cancelled a set number of days (7 by default) after their creation.

Learn more about separate authorization and capture.

The amount to capture from the PaymentIntent, which must be less than or equal to the original amount. Defaults to the full amount_capturable if it’s not provided.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a PaymentIntent object with status="succeeded" if the PaymentIntent is capturable. Returns an error if the PaymentIntent isn’t capturable or if an invalid amount to capture is provided.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents/pi_3MtwBwLkdIwHu7ix28a3tqPa \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents/pi_3MtwBwLkdIwHu7ix28a3tqPa \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",  "object": "payment_intent",  "amount": 2000,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 0,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": {    "enabled": true  },  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",  "confirmation_method": "automatic",  "created": 1680800504,  "currency": "usd",  "customer": null,  "description": null,  "last_payment_error": null,  "latest_charge": null,  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": null,  "payment_method_options": {    "card": {      "installments": null,      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    },    "link": {      "persistent_token": null    }  },  "payment_method_types": [    "card",    "link"  ],  "processing": null,  "receipt_email": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "source": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "requires_payment_method",  "transfer_data": null,  "transfer_group": null}
```

Example 4 (unknown):
```unknown
{  "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",  "object": "payment_intent",  "amount": 2000,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 0,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": {    "enabled": true  },  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",  "confirmation_method": "automatic",  "created": 1680800504,  "currency": "usd",  "customer": null,  "description": null,  "last_payment_error": null,  "latest_charge": null,  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": null,  "payment_method_options": {    "card": {      "installments": null,      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    },    "link": {      "persistent_token": null    }  },  "payment_method_types": [    "card",    "link"  ],  "processing": null,  "receipt_email": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "source": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "requires_payment_method",  "transfer_data": null,  "transfer_group": null}
```

---

## List all payouts

**URL:** https://docs.stripe.com/api/payouts/list

**Contents:**
- List all payouts
  - Parameters
    - statusstring
  - More parametersExpand all
    - arrival_dateobject
    - createdobject
    - destinationstring
    - ending_beforestring
    - limitinteger
    - starting_afterstring

Returns a list of existing payouts sent to third-party bank accounts or payouts that Stripe sent to you. The payouts return in sorted order, with the most recently created payouts appearing first.

Only return payouts that have the given status: pending, paid, failed, or canceled.

A dictionary with a data property that contains an array of up to limit payouts, starting after payout starting_after. Each entry in the array is a separate payout object. If no other payouts are available, the resulting array is empty.

You can cancel a previously created payout if its status is pending. Stripe refunds the funds to your available balance. You can’t cancel automatic Stripe payouts.

Returns the payout object if the cancellation succeeds. Returns an error if the payout is already canceled or can’t be canceled.

Reverses a payout by debiting the destination bank account. At this time, you can only reverse payouts for connected accounts to US and Canadian bank accounts. If the payout is manual and in the pending status, use /v1/payouts/:id/cancel instead.

By requesting a reversal through /v1/payouts/:id/reverse, you confirm that the authorized signatory of the selected bank account authorizes the debit on the bank account and that no other authorization is required.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the reversing payout object if the reversal is successful. Returns an error if the payout is already reversed or can’t be reversed.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v1/payouts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v1/payouts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 3 (unknown):
```unknown
{  "object": "list",  "url": "/v1/payouts",  "has_more": false,  "data": [    {      "id": "po_1OaFDbEcg9tTZuTgNYmX0PKB",      "object": "payout",      "amount": 1100,      "arrival_date": 1680652800,      "automatic": false,      "balance_transaction": "txn_1OaFDcEcg9tTZuTgYMR25tSe",      "created": 1680648691,      "currency": "usd",      "description": null,      "destination": "ba_1MtIhL2eZvKYlo2CAElKwKu2",      "failure_balance_transaction": null,      "failure_code": null,      "failure_message": null,      "livemode": false,      "metadata": {},      "method": "standard",      "original_payout": null,      "reconciliation_status": "not_applicable",      "reversed_by": null,      "source_type": "card",      "statement_descriptor": null,      "status": "pending",      "type": "bank_account"    }  ]}
```

Example 4 (unknown):
```unknown
{  "object": "list",  "url": "/v1/payouts",  "has_more": false,  "data": [    {      "id": "po_1OaFDbEcg9tTZuTgNYmX0PKB",      "object": "payout",      "amount": 1100,      "arrival_date": 1680652800,      "automatic": false,      "balance_transaction": "txn_1OaFDcEcg9tTZuTgYMR25tSe",      "created": 1680648691,      "currency": "usd",      "description": null,      "destination": "ba_1MtIhL2eZvKYlo2CAElKwKu2",      "failure_balance_transaction": null,      "failure_code": null,      "failure_message": null,      "livemode": false,      "metadata": {},      "method": "standard",      "original_payout": null,      "reconciliation_status": "not_applicable",      "reversed_by": null,      "source_type": "card",      "statement_descriptor": null,      "status": "pending",      "type": "bank_account"    }  ]}
```

---

## Cash Balance Transaction

**URL:** https://docs.stripe.com/api/cash_balance_transactions

**Contents:**
- Cash Balance Transaction
- The Cash Balance Transaction object
  - Attributes
    - idstring
    - objectstring
    - adjusted_for_overdraftnullable object
    - applied_to_paymentnullable object
    - createdtimestamp
    - currencystring
    - customerstringExpandable

Customers with certain payments enabled have a cash balance, representing funds that were paid by the customer to a merchant, but have not yet been allocated to a payment. Cash Balance Transactions represent when funds are moved into or out of this balance. This includes funding by the customer, allocation to payments, and refunds to the customer.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value.

If this is a type=adjusted_for_overdraft transaction, contains information about what caused the overdraft, which triggered this transaction.

If this is a type=applied_to_payment transaction, contains information about how funds were applied.

Time at which the object was created. Measured in seconds since the Unix epoch.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

The customer whose available cash balance changed as a result of this transaction.

The ID of an Account representing a customer whose available cash balance changed as a result of this transaction.

The total available cash balance for the specified currency after this transaction was applied. Represented in the smallest currency unit.

If this is a type=funded transaction, contains information about the funding.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The amount by which the cash balance changed, represented in the smallest currency unit. A positive value represents funds being added to the cash balance, a negative value represents funds being removed from the cash balance.

If this is a type=refunded_from_payment transaction, contains information about the source of the refund.

If this is a type=transferred_to_balance transaction, contains the balance transaction linked to the transfer.

The type of the cash balance transaction. New types may be added in future. See Customer Balance to learn more about these types.

A cash balance transaction type: adjusted_for_overdraft

A cash balance transaction type: applied_to_payment

A cash balance transaction type: funded

A cash balance transaction type: funding_reversed

A cash balance transaction type: refunded_from_payment

A cash balance transaction type: return_canceled

A cash balance transaction type: return_initiated

A cash balance transaction type: transferred_to_balance

A cash balance transaction type: unapplied_from_payment

If this is a type=unapplied_from_payment transaction, contains information about how funds were unapplied.

Retrieve funding instructions for a customer cash balance. If funding instructions do not yet exist for the customer, new funding instructions will be created. If funding instructions have already been created for a given customer, the same funding instructions will be retrieved. In other words, we will return the same funding instructions each time.

Additional parameters for bank_transfer funding types

Three-letter ISO currency code, in lowercase. Must be a supported currency.

The funding_type to get the instructions for.

Use a bank_transfer hash to define the bank transfer type

Returns funding instructions for a customer cash balance

Retrieves a specific cash balance transaction, which updated the customer’s cash balance.

Returns a cash balance transaction object if a valid identifier was provided.

Returns a list of transactions that modified the customer’s cash balance.

A dictionary with a data property that contains an array of up to limit cash balance transactions, starting after item starting_after. Each entry in the array is a separate cash balance transaction object. If no more items are available, the resulting array will be empty.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "ccsbtxn_1Na16B2eZvKYlo2CUhyw3dsF",  "object": "customer_cash_balance_transaction",  "created": 1690829143,  "currency": "eur",  "customer": "cus_9s6XKzkNRiz8i3",  "ending_balance": 10000,  "funded": {    "bank_transfer": {      "eu_bank_transfer": {        "bic": "BANKDEAAXXX",        "iban_last4": "7089",        "sender_name": "Sample Business GmbH"      },      "reference": "Payment for Invoice 28278FC-155",      "type": "eu_bank_transfer"    }  },  "livemode": false,  "net_amount": 5000,  "type": "funded"}
```

Example 2 (unknown):
```unknown
{  "id": "ccsbtxn_1Na16B2eZvKYlo2CUhyw3dsF",  "object": "customer_cash_balance_transaction",  "created": 1690829143,  "currency": "eur",  "customer": "cus_9s6XKzkNRiz8i3",  "ending_balance": 10000,  "funded": {    "bank_transfer": {      "eu_bank_transfer": {        "bic": "BANKDEAAXXX",        "iban_last4": "7089",        "sender_name": "Sample Business GmbH"      },      "reference": "Payment for Invoice 28278FC-155",      "type": "eu_bank_transfer"    }  },  "livemode": false,  "net_amount": 5000,  "type": "funded"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/customers/cus_9s6XKzkNRiz8i3/funding_instructions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d funding_type=bank_transfer \  -d currency=eur \  -d "bank_transfer[type]"=eu_bank_transfer \  -d "bank_transfer[eu_bank_transfer][country]"=DE
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/customers/cus_9s6XKzkNRiz8i3/funding_instructions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d funding_type=bank_transfer \  -d currency=eur \  -d "bank_transfer[type]"=eu_bank_transfer \  -d "bank_transfer[eu_bank_transfer][country]"=DE
```

---

## List all files

**URL:** https://docs.stripe.com/api/files/list

**Contents:**
- List all files
  - Parameters
    - purposestring
  - More parametersExpand all
    - createdobject
    - ending_beforestring
    - limitinteger
    - starting_afterstring
  - Returns

Returns a list of the files that your account has access to. Stripe sorts and returns the files by their creation dates, placing the most recently created files at the top.

Filter queries by the file purpose. If you don’t provide a purpose, the queries return unfiltered files.

A dictionary with a data property that contains an array of up to limit files, starting after the starting_after file. Each entry in the array is a separate file object. If there aren’t additional available files, the resulting array is empty.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v1/files \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v1/files \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 3 (unknown):
```unknown
{  "object": "list",  "url": "/v1/files",  "has_more": false,  "data": [    {      "id": "file_1Mr4LDLkdIwHu7ixFCz0dZiH",      "object": "file",      "created": 1680116847,      "expires_at": 1703444847,      "filename": "file.png",      "links": {        "object": "list",        "data": [],        "has_more": false,        "url": "/v1/file_links?file=file_1Mr4LDLkdIwHu7ixFCz0dZiH"      },      "purpose": "dispute_evidence",      "size": 8429,      "title": null,      "type": "png",      "url": "https://files.stripe.com/v1/files/file_1Mr4LDLkdIwHu7ixFCz0dZiH/contents"    }  ]}
```

Example 4 (unknown):
```unknown
{  "object": "list",  "url": "/v1/files",  "has_more": false,  "data": [    {      "id": "file_1Mr4LDLkdIwHu7ixFCz0dZiH",      "object": "file",      "created": 1680116847,      "expires_at": 1703444847,      "filename": "file.png",      "links": {        "object": "list",        "data": [],        "has_more": false,        "url": "/v1/file_links?file=file_1Mr4LDLkdIwHu7ixFCz0dZiH"      },      "purpose": "dispute_evidence",      "size": 8429,      "title": null,      "type": "png",      "url": "https://files.stripe.com/v1/files/file_1Mr4LDLkdIwHu7ixFCz0dZiH/contents"    }  ]}
```

---

## Increment an authorization

**URL:** https://docs.stripe.com/api/payment_intents/increment_authorization

**Contents:**
- Increment an authorization
  - Parameters
    - amountintegerRequired
    - descriptionstring
    - metadataobject
    - statement_descriptorstring
  - More parametersExpand all
    - amount_detailsobject
    - application_fee_amountintegerConnect only
    - hooksobject

Perform an incremental authorization on an eligible PaymentIntent. To be eligible, the PaymentIntent’s status must be requires_capture and incremental_authorization_supported must be true.

Incremental authorizations attempt to increase the authorized amount on your customer’s card to the new, higher amount provided. Similar to the initial authorization, incremental authorizations can be declined. A single PaymentIntent can call this endpoint multiple times to further increase the authorized amount.

If the incremental authorization succeeds, the PaymentIntent object returns with the updated amount. If the incremental authorization fails, a card_declined error returns, and no other fields on the PaymentIntent or Charge update. The PaymentIntent object remains capturable for the previously authorized amount.

Each PaymentIntent can have a maximum of 10 incremental authorization attempts, including declines. After it’s captured, a PaymentIntent can no longer be incremented.

Learn more about incremental authorizations.

The updated total amount that you intend to collect from the cardholder. This amount must be greater than the currently authorized amount.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Text that appears on the customer’s statement as the statement descriptor for a non-card or card charge. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

Returns a PaymentIntent object with the updated amount if the incremental authorization succeeds. Returns an error if the incremental authorization failed or the PaymentIntent isn’t eligible for incremental authorizations.

Manually reconcile the remaining amount for a customer_balance PaymentIntent.

Amount that you intend to apply to this PaymentIntent from the customer’s cash balance. If the PaymentIntent was created by an Invoice, the full amount of the PaymentIntent is applied regardless of this parameter.

A positive integer representing how much to charge in the smallest currency unit (for example, 100 cents to charge 1 USD or 100 to charge 100 JPY, a zero-decimal currency). The maximum amount is the amount of the PaymentIntent.

When you omit the amount, it defaults to the remaining amount requested on the PaymentIntent.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

Returns a PaymentIntent object.

Search for PaymentIntents you’ve previously created using Stripe’s Search Query Language. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.

The search query string. See search query language and the list of supported query fields for payment intents.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A dictionary with a data property that contains an array of up to limit PaymentIntents. If no objects match the query, the resulting array will be empty. See the related guide on expanding properties in lists.

Verifies microdeposits on a PaymentIntent object.

Two positive integers, in cents, equal to the values of the microdeposits sent to the bank account.

A six-character code starting with SM present in the microdeposit sent to the bank account.

Returns a PaymentIntent object.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents/pi_1DtBRR2eZvKYlo2CmCVxxvd7/increment_authorization \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=2099
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents/pi_1DtBRR2eZvKYlo2CmCVxxvd7/increment_authorization \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=2099
```

Example 3 (unknown):
```unknown
{  "id": "pi_1DtBRR2eZvKYlo2CmCVxxvd7",  "object": "payment_intent",  "amount": 2099,  "amount_capturable": 2099,  "amount_details": {    "tip": {}  },  "amount_received": 0,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": null,  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "manual",  "client_secret": "pi_1DtBRR2eZvKYlo2CmCVxxvd7_secret_cWsUkvyTOjhLKh5Wxu61nYc0i",  "confirmation_method": "automatic",  "created": 1680196960,  "currency": "usd",  "customer": null,  "description": null,  "last_payment_error": null,  "latest_charge": "ch_3MrPBM2eZvKYlo2C1CEBUD4A",  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": "pm_1MrPBL2eZvKYlo2CaNa8L11Z",  "payment_method_options": {    "card": {      "installments": null,      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    }  },  "payment_method_types": [    "card"  ],  "processing": null,  "receipt_email": null,  "redaction": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "requires_capture",  "transfer_data": null,  "transfer_group": null}
```

Example 4 (unknown):
```unknown
{  "id": "pi_1DtBRR2eZvKYlo2CmCVxxvd7",  "object": "payment_intent",  "amount": 2099,  "amount_capturable": 2099,  "amount_details": {    "tip": {}  },  "amount_received": 0,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": null,  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "manual",  "client_secret": "pi_1DtBRR2eZvKYlo2CmCVxxvd7_secret_cWsUkvyTOjhLKh5Wxu61nYc0i",  "confirmation_method": "automatic",  "created": 1680196960,  "currency": "usd",  "customer": null,  "description": null,  "last_payment_error": null,  "latest_charge": "ch_3MrPBM2eZvKYlo2C1CEBUD4A",  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": "pm_1MrPBL2eZvKYlo2CaNa8L11Z",  "payment_method_options": {    "card": {      "installments": null,      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    }  },  "payment_method_types": [    "card"  ],  "processing": null,  "receipt_email": null,  "redaction": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "requires_capture",  "transfer_data": null,  "transfer_group": null}
```

---

## Retrieve a file link

**URL:** https://docs.stripe.com/api/file_links/retrieve

**Contents:**
- Retrieve a file link
  - Parameters
  - Returns
- List all file links
  - Parameters
  - More parametersExpand all
    - createdobject
    - ending_beforestring
    - expiredboolean
    - filestring

Retrieves the file link with the given ID.

If the identifier you provide is valid, a file link object returns. If not, Stripe raises an error.

Returns a list of file links.

A dictionary with a data property that contains an array of up to limit file links, starting after the starting_after file link. Each entry in the array is a separate file link object. If there aren’t additional available file links, the resulting array is empty.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/file_links/link_1Mr23jLkdIwHu7ix65betcoo \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/file_links/link_1Mr23jLkdIwHu7ix65betcoo \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "link_1Mr23jLkdIwHu7ix65betcoo",  "object": "file_link",  "created": 1680108075,  "expired": false,  "expires_at": null,  "file": "file_1Mr23iLkdIwHu7ixQkCV3CBR",  "livemode": false,  "metadata": {},  "url": "https://files.stripe.com/links/MDB8YWNjdF8xTTJKVGtMa2RJd0h1N2l4fGZsX3Rlc3RfaXVoY2hrUnJPMzlBR3dPb01XMmFkSTVq00yUPLFf3h"}
```

Example 4 (unknown):
```unknown
{  "id": "link_1Mr23jLkdIwHu7ix65betcoo",  "object": "file_link",  "created": 1680108075,  "expired": false,  "expires_at": null,  "file": "file_1Mr23iLkdIwHu7ixQkCV3CBR",  "livemode": false,  "metadata": {},  "url": "https://files.stripe.com/links/MDB8YWNjdF8xTTJKVGtMa2RJd0h1N2l4fGZsX3Rlc3RfaXVoY2hrUnJPMzlBR3dPb01XMmFkSTVq00yUPLFf3h"}
```

---

## Persons v2

**URL:** https://docs.stripe.com/api/v2/core/persons

**Contents:**
- Persons v2
- The Person object
  - Attributes
    - idstring
    - objectstring, value is "v2.core.account_person"
    - accountstring
    - additional_addressesnullable array of objects
    - additional_namesnullable array of objects
    - additional_terms_of_servicenullable object
    - addressnullable object

A Person represents an individual associated with an Account’s identity (for example, an owner, director, executive, or representative). Use Persons to provide and update identity information for verification and compliance.

Unique identifier for the Person.

String representing the object’s type. Objects of the same type share the same value of the object field.

The account ID which the individual belongs to.

Additional addresses associated with the person.

Additional names (e.g. aliases) associated with the person.

Attestations of accepted terms of service agreements.

The person’s residential address.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

The person’s date of birth.

Documents that may be submitted to satisfy various informational requests.

The person’s email address.

The person’s first name.

The identification numbers (e.g., SSN) associated with the person.

The person’s gender (International regulations require either “male” or “female”).

Female gender person.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The countries where the person is a national. Two-letter country code (ISO 3166-1 alpha-2).

The person’s phone number.

The person’s political exposure.

The person has disclosed that they do have political exposure.

The person has disclosed that they have no political exposure.

The relationship that this person has with the Account’s business or legal entity.

The script addresses (e.g., non-Latin characters) associated with the person.

The script names (e.g. non-Latin characters) associated with the person.

The person’s last name.

Time at which the object was last updated. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Create a Person. Adds an individual to an Account’s identity. You can set relationship attributes and identity information at creation.

Account the Person should be associated with.

Additional addresses associated with the person.

Additional names (e.g. aliases) associated with the person.

Attestations of accepted terms of service agreements.

The person’s residential address.

The person’s date of birth.

Documents that may be submitted to satisfy various informational requests.

The person’s first name.

The identification numbers (e.g., SSN) associated with the person.

The person’s gender (International regulations require either “male” or “female”).

Female gender person.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The nationalities (countries) this person is associated with.

The person token generated by the person token api.

The phone number for this person.

The person’s political exposure.

The person has disclosed that they do have political exposure.

The person has disclosed that they have no political exposure.

The relationship that this person has with the Account’s business or legal entity.

The script addresses (e.g., non-Latin characters) associated with the person.

The script names (e.g. non-Latin characters) associated with the person.

The person’s last name.

Unique identifier for the Person.

String representing the object’s type. Objects of the same type share the same value of the object field.

The account ID which the individual belongs to.

Additional addresses associated with the person.

Additional names (e.g. aliases) associated with the person.

Attestations of accepted terms of service agreements.

The person’s residential address.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

The person’s date of birth.

Documents that may be submitted to satisfy various informational requests.

The person’s email address.

The person’s first name.

The identification numbers (e.g., SSN) associated with the person.

The person’s gender (International regulations require either “male” or “female”).

Female gender person.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The countries where the person is a national. Two-letter country code (ISO 3166-1 alpha-2).

The person’s phone number.

The person’s political exposure.

The person has disclosed that they do have political exposure.

The person has disclosed that they have no political exposure.

The relationship that this person has with the Account’s business or legal entity.

The script addresses (e.g., non-Latin characters) associated with the person.

The script names (e.g. non-Latin characters) associated with the person.

The person’s last name.

Time at which the object was last updated. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

More than one legal guardian is added to an account.

More than one representative is added to an account.

Additional terms of service are signed by someone other than the legal guardian.

Invalid characters are provided for address fields.

Address country doesn’t match identity country.

Registered/script address country doesn’t match residential address country.

Address country is required but not provided.

Address postal code is invalid.

Address state is invalid.

Address town is invalid.

There can only be one authorizer.

An authorizer cannot be a representative.

Representative date of birth does not meet the age limit.

Representative date of birth is provided an invalid date or a future date.

Provided file tokens for documents are invalid, not found, deleted, or belong to a different account.

Provided file tokens for documents are of the wrong purpose.

Duplicate person is added to an account.

Email contains unsupported domain.

Incorrect email is provided.

Provided ID number is of the wrong format for the given type.

The identity.country value is required but not provided.

A person token is created with one account but used on a different account.

Incorrect ID number is provided for a country.

The incorrect token type is provided .

Additional person is added for an individual business type.

Some relationships are specific to type, structure, and country.

Invalid IP address is provided.

Person is designated as both legal guardian and representative.

A legal guardian may not be added to the account without an existing representative.

Kana Kanji script addresses must have JP country.

Parameter cannot be passed alongside person_token.

Error returned when relationship.owner is set to true but the ownership percentage is set to 0%.

Person token required for platforms in mandated countries (e.g., France).

Phone number is invalid.

Postal code is required for Japanese addresses.

Provided script characters are invalid for the script.

The token is re-used with a different idempotency key.

Total ownership percentages of all Persons on the account exceeds 100%.

Address is in an unsupported postal code.

Address is in an unsupported state.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

A v1 token ID is passed in v2 APIs.

Invalid person token.

Updates a Person associated with an Account.

The Account the Person is associated with.

The ID of the Person to update.

Additional addresses associated with the person.

Additional names (e.g. aliases) associated with the person.

Attestations of accepted terms of service agreements.

The primary address associated with the person.

The person’s date of birth.

Documents that may be submitted to satisfy various informational requests.

The person’s first name.

The identification numbers (e.g., SSN) associated with the person.

The person’s gender (International regulations require either “male” or “female”).

Female gender person.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The nationalities (countries) this person is associated with.

The person token generated by the person token api.

The phone number for this person.

The person’s political exposure.

The person has disclosed that they do have political exposure.

The person has disclosed that they have no political exposure.

The relationship that this person has with the Account’s business or legal entity.

The script addresses (e.g., non-Latin characters) associated with the person.

The script names (e.g. non-Latin characters) associated with the person.

The person’s last name.

Unique identifier for the Person.

String representing the object’s type. Objects of the same type share the same value of the object field.

The account ID which the individual belongs to.

Additional addresses associated with the person.

Additional names (e.g. aliases) associated with the person.

Attestations of accepted terms of service agreements.

The person’s residential address.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

The person’s date of birth.

Documents that may be submitted to satisfy various informational requests.

The person’s email address.

The person’s first name.

The identification numbers (e.g., SSN) associated with the person.

The person’s gender (International regulations require either “male” or “female”).

Female gender person.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The countries where the person is a national. Two-letter country code (ISO 3166-1 alpha-2).

The person’s phone number.

The person’s political exposure.

The person has disclosed that they do have political exposure.

The person has disclosed that they have no political exposure.

The relationship that this person has with the Account’s business or legal entity.

The script addresses (e.g., non-Latin characters) associated with the person.

The script names (e.g. non-Latin characters) associated with the person.

The person’s last name.

Time at which the object was last updated. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

More than one legal guardian is added to an account.

More than one representative is added to an account.

Additional terms of service are signed by someone other than the legal guardian.

Invalid characters are provided for address fields.

Address country doesn’t match identity country.

Registered/script address country doesn’t match residential address country.

Address country is required but not provided.

Address postal code is invalid.

Address state is invalid.

Address town is invalid.

Representative date of birth does not meet the age limit.

Representative date of birth is provided an invalid date or a future date.

Provided file tokens for documents are invalid, not found, deleted, or belong to a different account.

Provided file tokens for documents are of the wrong purpose.

Duplicate person is added to an account.

Email contains unsupported domain.

Incorrect email is provided.

Provided ID number is of the wrong format for the given type.

The identity.country value is required but not provided.

Identity param has been made immutable due to the state of the account.

A person token is created with one account but used on a different account.

Incorrect ID number is provided for a country.

The incorrect token type is provided .

Invalid IP address is provided.

Person is designated as both legal guardian and representative.

A legal guardian may not be added to the account without an existing representative.

Kana Kanji script addresses must have JP country.

Parameter cannot be passed alongside person_token.

Error returned when relationship.owner is set to true but the ownership percentage is set to 0%.

Person token required for platforms in mandated countries (e.g., France).

Phone number is invalid.

Postal code is required for Japanese addresses.

Provided script characters are invalid for the script.

The token is re-used with a different idempotency key.

Total ownership percentages of all Persons on the account exceeds 100%.

Address is in an unsupported postal code.

Address is in an unsupported state.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

A v1 token ID is passed in v2 APIs.

Invalid person token.

The resource wasn’t found.

Retrieves a Person associated with an Account.

The Account the Person is associated with.

The ID of the Person to retrieve.

Unique identifier for the Person.

String representing the object’s type. Objects of the same type share the same value of the object field.

The account ID which the individual belongs to.

Additional addresses associated with the person.

Additional names (e.g. aliases) associated with the person.

Attestations of accepted terms of service agreements.

The person’s residential address.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

The person’s date of birth.

Documents that may be submitted to satisfy various informational requests.

The person’s email address.

The person’s first name.

The identification numbers (e.g., SSN) associated with the person.

The person’s gender (International regulations require either “male” or “female”).

Female gender person.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The countries where the person is a national. Two-letter country code (ISO 3166-1 alpha-2).

The person’s phone number.

The person’s political exposure.

The person has disclosed that they do have political exposure.

The person has disclosed that they have no political exposure.

The relationship that this person has with the Account’s business or legal entity.

The script addresses (e.g., non-Latin characters) associated with the person.

The script names (e.g. non-Latin characters) associated with the person.

The person’s last name.

Time at which the object was last updated. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

The resource wasn’t found.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_person",  "account": "acct_1Nv0FGQ9RKHgCVdK",  "additional_addresses": [],  "additional_names": [],  "address": {    "city": "Brothers",    "country": "us",    "line1": "27 Fredrick Ave",    "postal_code": "97712",    "state": "OR"  },  "created": "2024-11-26T17:10:07.000Z",  "email": "jenny.rosen@example.com",  "given_name": "Jenny",  "id_numbers": [    {      "type": "us_ssn_last_4"    }  ],  "metadata": {},  "nationalities": [],  "relationship": {    "owner": true,    "percent_ownership": "0.8",    "representative": true,    "title": "CEO"  },  "surname": "Rosen",  "updated": "2024-11-26T17:10:07.000Z"}
```

Example 2 (unknown):
```unknown
{  "id": "person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_person",  "account": "acct_1Nv0FGQ9RKHgCVdK",  "additional_addresses": [],  "additional_names": [],  "address": {    "city": "Brothers",    "country": "us",    "line1": "27 Fredrick Ave",    "postal_code": "97712",    "state": "OR"  },  "created": "2024-11-26T17:10:07.000Z",  "email": "jenny.rosen@example.com",  "given_name": "Jenny",  "id_numbers": [    {      "type": "us_ssn_last_4"    }  ],  "metadata": {},  "nationalities": [],  "relationship": {    "owner": true,    "percent_ownership": "0.8",    "representative": true,    "title": "CEO"  },  "surname": "Rosen",  "updated": "2024-11-26T17:10:07.000Z"}
```

Example 3 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/persons \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "given_name": "Jenny",    "surname": "Rosen",    "email": "jenny.rosen@example.com",    "address": {        "line1": "27 Fredrick Ave",        "city": "Brothers",        "postal_code": "97712",        "state": "OR",        "country": "us"    },    "id_numbers": [        {            "type": "us_ssn_last_4",            "value": "0000"        }    ],    "relationship": {        "owner": true,        "percent_ownership": "0.8",        "representative": true,        "title": "CEO"    }  }'
```

Example 4 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/persons \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "given_name": "Jenny",    "surname": "Rosen",    "email": "jenny.rosen@example.com",    "address": {        "line1": "27 Fredrick Ave",        "city": "Brothers",        "postal_code": "97712",        "state": "OR",        "country": "us"    },    "id_numbers": [        {            "type": "us_ssn_last_4",            "value": "0000"        }    ],    "relationship": {        "owner": true,        "percent_ownership": "0.8",        "representative": true,        "title": "CEO"    }  }'
```

---

## Create a price

**URL:** https://docs.stripe.com/api/prices/create

**Contents:**
- Create a price
  - Parameters
    - currencyenumRequired
    - activeboolean
    - metadataobject
    - nicknamestring
    - productstringRequired unless product_data is provided
    - recurringobject
    - tax_behaviorenumRecommended if calculating taxes
    - unit_amountintegerRequired conditionally

Creates a new Price for an existing Product. The Price can be recurring or one-time.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

Whether the price can be used for new purchases. Defaults to true.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

A brief description of the price, hidden from customers.

The ID of the Product that this Price will belong to.

The recurring components of a price such as interval and usage_type.

Only required if a default tax behavior was not provided in the Stripe Tax settings. Specifies whether the price is considered inclusive of taxes or exclusive of taxes. One of inclusive, exclusive, or unspecified. Once specified as either inclusive or exclusive, it cannot be changed.

A positive integer in cents (or 0 for a free price) representing how much to charge. One of unit_amount, unit_amount_decimal, or custom_unit_amount is required, unless billing_scheme=tiered.

The newly created Price object is returned upon success. Otherwise, this call raises an error.

Updates the specified price by setting the values of the parameters passed. Any parameters not provided are left unchanged.

Whether the price can be used for new purchases. Defaults to true.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

A brief description of the price, hidden from customers.

Only required if a default tax behavior was not provided in the Stripe Tax settings. Specifies whether the price is considered inclusive of taxes or exclusive of taxes. One of inclusive, exclusive, or unspecified. Once specified as either inclusive or exclusive, it cannot be changed.

The updated price object is returned upon success. Otherwise, this call raises an error.

Retrieves the price with the given ID.

Returns a price if a valid price or plan ID was provided. Raises an error otherwise.

Returns a list of your active prices, excluding inline prices. For the list of inactive prices, set active to false.

Only return prices that are active or inactive (e.g., pass false to list all inactive prices).

Only return prices for the given currency.

Only return prices for the given product.

Only return prices of type recurring or one_time.

A dictionary with a data property that contains an array of up to limit prices, starting after prices starting_after. Each entry in the array is a separate price object. If no more prices are available, the resulting array will be empty.

Search for prices you’ve previously created using Stripe’s Search Query Language. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.

The search query string. See search query language and the list of supported query fields for prices.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A dictionary with a data property that contains an array of up to limit prices. If no objects match the query, the resulting array will be empty. See the related guide on expanding properties in lists.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/prices \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d currency=usd \  -d unit_amount=1000 \  -d "recurring[interval]"=month \  -d "product_data[name]"="Gold Plan"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/prices \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d currency=usd \  -d unit_amount=1000 \  -d "recurring[interval]"=month \  -d "product_data[name]"="Gold Plan"
```

Example 3 (unknown):
```unknown
{  "id": "price_1MoBy5LkdIwHu7ixZhnattbh",  "object": "price",  "active": true,  "billing_scheme": "per_unit",  "created": 1679431181,  "currency": "usd",  "custom_unit_amount": null,  "livemode": false,  "lookup_key": null,  "metadata": {},  "nickname": null,  "product": "prod_NZKdYqrwEYx6iK",  "recurring": {    "interval": "month",    "interval_count": 1,    "trial_period_days": null,    "usage_type": "licensed"  },  "tax_behavior": "unspecified",  "tiers_mode": null,  "transform_quantity": null,  "type": "recurring",  "unit_amount": 1000,  "unit_amount_decimal": "1000"}
```

Example 4 (unknown):
```unknown
{  "id": "price_1MoBy5LkdIwHu7ixZhnattbh",  "object": "price",  "active": true,  "billing_scheme": "per_unit",  "created": 1679431181,  "currency": "usd",  "custom_unit_amount": null,  "livemode": false,  "lookup_key": null,  "metadata": {},  "nickname": null,  "product": "prod_NZKdYqrwEYx6iK",  "recurring": {    "interval": "month",    "interval_count": 1,    "trial_period_days": null,    "usage_type": "licensed"  },  "tax_behavior": "unspecified",  "tiers_mode": null,  "transform_quantity": null,  "type": "recurring",  "unit_amount": 1000,  "unit_amount_decimal": "1000"}
```

---

## Event Destinations v2

**URL:** https://docs.stripe.com/api/v2/core/event_destinations

**Contents:**
- Event Destinations v2
- The EventDestination object
  - Attributes
    - idstring
    - objectstring, value is "v2.core.event_destination"
    - amazon_eventbridgenullable object
    - createdtimestamp
    - descriptionstring
    - enabled_eventsarray of strings
    - event_payloadenum

Set up an event destination to receive events from Stripe across multiple destination types, including webhook endpoints and Amazon EventBridge. Event destinations support receiving thin events and snapshot events.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value of the object field.

Amazon EventBridge configuration.

Time at which the object was created.

An optional description of what the event destination is used for.

The list of events to enable for this endpoint.

Payload type of events being subscribed to.

Where events should be routed from.

Receive events from accounts connected to the account that owns the event destination.

Receive events from the account that owns the event destination.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Event destination name.

If using the snapshot event payload, the API version events are rendered as.

Status. It can be set to either enabled or disabled.

Event destination is disabled.

Event destination is enabled.

Additional information about event destination status.

Event destination type.

Time at which the object was last updated.

Webhook endpoint configuration.

Create a new event destination.

The list of events to enable for this endpoint.

Payload type of events being subscribed to.

Event destination name.

Event destination type.

Amazon EventBridge configuration.

An optional description of what the event destination is used for.

Where events should be routed from.

Receive events from accounts connected to the account that owns the event destination.

Receive events from the account that owns the event destination.

Additional fields to include in the response.

Include parameter to expose webhook_endpoint.signing_secret.

Include parameter to expose webhook_endpoint.url.

If using the snapshot event payload, the API version events are rendered as.

Webhook endpoint configuration.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value of the object field.

Amazon EventBridge configuration.

Time at which the object was created.

An optional description of what the event destination is used for.

The list of events to enable for this endpoint.

Payload type of events being subscribed to.

Where events should be routed from.

Receive events from accounts connected to the account that owns the event destination.

Receive events from the account that owns the event destination.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Event destination name.

If using the snapshot event payload, the API version events are rendered as.

Status. It can be set to either enabled or disabled.

Event destination is disabled.

Event destination is enabled.

Additional information about event destination status.

Event destination type.

Time at which the object was last updated.

Webhook endpoint configuration.

An idempotent retry occurred with different request parameters.

Update the details of an event destination.

Identifier for the event destination to update.

An optional description of what the event destination is used for.

The list of events to enable for this endpoint.

Additional fields to include in the response. Currently supports webhook_endpoint.url.

Include parameter to expose webhook_endpoint.url.

Event destination name.

Webhook endpoint configuration.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value of the object field.

Amazon EventBridge configuration.

Time at which the object was created.

An optional description of what the event destination is used for.

The list of events to enable for this endpoint.

Payload type of events being subscribed to.

Where events should be routed from.

Receive events from accounts connected to the account that owns the event destination.

Receive events from the account that owns the event destination.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Event destination name.

If using the snapshot event payload, the API version events are rendered as.

Status. It can be set to either enabled or disabled.

Event destination is disabled.

Event destination is enabled.

Additional information about event destination status.

Event destination type.

Time at which the object was last updated.

Webhook endpoint configuration.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

Retrieves the details of an event destination.

Identifier for the event destination to retrieve.

Additional fields to include in the response.

Include parameter to expose webhook_endpoint.url.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value of the object field.

Amazon EventBridge configuration.

Time at which the object was created.

An optional description of what the event destination is used for.

The list of events to enable for this endpoint.

Payload type of events being subscribed to.

Where events should be routed from.

Receive events from accounts connected to the account that owns the event destination.

Receive events from the account that owns the event destination.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Event destination name.

If using the snapshot event payload, the API version events are rendered as.

Status. It can be set to either enabled or disabled.

Event destination is disabled.

Event destination is enabled.

Additional information about event destination status.

Event destination type.

Time at which the object was last updated.

Webhook endpoint configuration.

The resource wasn’t found.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6",  "object": "v2.core.event_destination",  "created": "2024-10-22T16:20:09.931Z",  "description": "This is my event destination, I like it a lot",  "enabled_events": [    "v1.billing.meter.error_report_triggered"  ],  "event_payload": "thin",  "events_from": [    "self"  ],  "livemode": false,  "metadata": {},  "name": "My Event Destination",  "snapshot_api_version": null,  "status": "enabled",  "status_details": null,  "type": "webhook_endpoint",  "updated": "2024-10-22T16:20:09.937Z",  "webhook_endpoint": {    "signing_secret": null,    "url": "https://example.com/my/webhook/endpoint"  }}
```

Example 2 (unknown):
```unknown
{  "id": "ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6",  "object": "v2.core.event_destination",  "created": "2024-10-22T16:20:09.931Z",  "description": "This is my event destination, I like it a lot",  "enabled_events": [    "v1.billing.meter.error_report_triggered"  ],  "event_payload": "thin",  "events_from": [    "self"  ],  "livemode": false,  "metadata": {},  "name": "My Event Destination",  "snapshot_api_version": null,  "status": "enabled",  "status_details": null,  "type": "webhook_endpoint",  "updated": "2024-10-22T16:20:09.937Z",  "webhook_endpoint": {    "signing_secret": null,    "url": "https://example.com/my/webhook/endpoint"  }}
```

Example 3 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/event_destinations \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "name": "My Event Destination",    "description": "This is my event destination, I like it a lot",    "enabled_events": [        "v1.billing.meter.error_report_triggered"    ],    "type": "webhook_endpoint",    "webhook_endpoint": {        "url": "https://example.com/my/webhook/endpoint"    },    "event_payload": "thin",    "include": [        "webhook_endpoint.url"    ]  }'
```

Example 4 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/event_destinations \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "name": "My Event Destination",    "description": "This is my event destination, I like it a lot",    "enabled_events": [        "v1.billing.meter.error_report_triggered"    ],    "type": "webhook_endpoint",    "webhook_endpoint": {        "url": "https://example.com/my/webhook/endpoint"    },    "event_payload": "thin",    "include": [        "webhook_endpoint.url"    ]  }'
```

---

## API Reference

**URL:** https://docs.stripe.com/api

**Contents:**
- API Reference
- Just getting started?
- Not a developer?
- Authentication
- Errors
  - Attributes
    - codenullable string
    - decline_codenullable string
    - messagenullable string
    - paramnullable string

The Stripe API is organized around REST. Our API has predictable resource-oriented URLs, accepts form-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.

You can use the Stripe API in test mode, which doesn’t affect your live data or interact with the banking networks. The API key you use to authenticate the request determines whether the request is live mode or test mode. Test mode supports some v2 APIs.

The Stripe API doesn’t support bulk updates. You can work on only one object per request.

The Stripe API differs for every account as we release new versions and tailor functionality. Log in to see docs with your test key and data.

Check out our development quickstart guide.

Use Stripe’s no-code options or apps from our partners to get started with Stripe and to do more with your Stripe account—no code required.

By default, the Stripe API Docs demonstrate using curl to interact with the API over HTTP. Select one of our official client libraries to see examples in code.

The Stripe API uses API keys to authenticate requests. You can view and manage your API keys in the Stripe Dashboard.

Test mode secret keys have the prefix sk_test_ and live mode secret keys have the prefix sk_live_. Alternatively, you can use restricted API keys for granular permissions.

Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.

All API requests must be made over HTTPS. Calls made over plain HTTP will fail. API requests without authentication will also fail.

A sample test API key is included in all the examples here, so you can test any example right away. Do not submit any personally identifiable information in requests made with this key.

To test requests using your account, replace the sample API key with your actual API key or sign in.

Stripe uses conventional HTTP response codes to indicate the success or failure of an API request. In general: Codes in the 2xx range indicate success. Codes in the 4xx range indicate an error that failed given the information provided (e.g., a required parameter was omitted, a charge failed, etc.). Codes in the 5xx range indicate an error with Stripe’s servers (these are rare).

Some 4xx errors that could be handled programmatically (e.g., a card is declined) include an error code that briefly explains the error reported.

For some errors that could be handled programmatically, a short string indicating the error code reported.

For card errors resulting from a card issuer decline, a short string indicating the card issuer’s reason for the decline if they provide one.

A human-readable message providing more details about the error. For card errors, these messages can be shown to your users.

If the error is parameter-specific, the parameter related to the error. For example, you can use this to display a message near the correct form field.

The PaymentIntent object for errors returned on a request involving a PaymentIntent.

The type of error returned. One of api_error, card_error, idempotency_error, or invalid_request_error

Our Client libraries raise exceptions for many reasons, such as a failed charge, invalid parameters, authentication errors, and network unavailability. We recommend writing code that gracefully handles all possible API exceptions.

Many objects allow you to request additional information as an expanded response by using the expand request parameter. This parameter is available on all API requests, and applies to the response of that request only. You can expand responses in two ways.

In many cases, an object contains the ID of a related object in its response properties. For example, a Charge might have an associated Customer ID. You can expand these objects in line with the expand request parameter. The expandable label in this documentation indicates ID fields that you can expand into objects.

Some available fields aren’t included in the responses by default, such as the number and cvc fields for the Issuing Card object. You can request these fields as an expanded response by using the expand request parameter.

You can expand recursively by specifying nested fields after a dot (.). For example, requesting payment_intent.customer on a charge expands the payment_intent property into a full PaymentIntent object, then expands the customer property on that payment intent into a full Customer object.

You can use the expand parameter on any endpoint that returns expandable fields, including list, create, and update endpoints.

Expansions on list requests start with the data property. For example, you can expand data.customers on a request to list charges and associated customers. Performing deep expansions on numerous list requests might result in slower processing times.

Expansions have a maximum depth of four levels (for example, the deepest expansion allowed when listing charges is data.payment_intent.customer.default_source).

You can expand multiple objects at the same time by identifying multiple items in the expand array.

**Examples:**

Example 1 (unknown):
```unknown
https://api.stripe.com
```

Example 2 (unknown):
```unknown
https://api.stripe.com
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/charges \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:# The colon prevents curl from asking for a password.
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/charges \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:# The colon prevents curl from asking for a password.
```

---

## EventDestination event types v2

**URL:** https://docs.stripe.com/api/v2/core/event_destinations/event-types

**Contents:**
- EventDestination event types v2
- Event types
  - v2.core.event_destination.ping

This is a list of all public thin events we currently send for updates to EventDestination, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

---

## Search

**URL:** https://docs.stripe.com/api/pagination/search

**Contents:**
- Search
  - Search request format
    - queryrequired
    - limitoptional
    - pageoptional
  - Search response format
    - objectstring, value is "search_result"
    - urlstring
    - has_moreboolean
    - dataarray

Some top-level API resource have support for retrieval via “search” API methods. For example, you can search charges, search customers, and search subscriptions.

Stripe’s search API methods utilize cursor-based pagination via the page request parameter and next_page response parameter. For example, if you make a search request and receive "next_page": "pagination_key" in the response, your subsequent call can include page=pagination_key to fetch the next page of results.

Our client libraries offer auto-pagination helpers to easily traverse all pages of a search result.

The search query string. See search query language.

A limit on the number of objects returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A string describing the object type returned.

The URL for accessing this list.

Whether or not there are more elements available after this set. If false, this set comprises the end of the list.

An array containing the actual response elements, paginated by any request parameters.

A cursor for use in pagination. If has_more is true, you can pass the value of next_page to a subsequent call to fetch the next page of results.

The total number of objects that match the query, only accurate up to 10,000. This field isn’t included by default. To include it in the response, expand the total_count field.

Our libraries support auto-pagination. This feature allows you to easily iterate through large lists of resources without having to manually perform the requests to fetch subsequent pages.

Each API request has an associated request identifier. You can find this value in the response headers, under Request-Id. You can also find request identifiers in the URLs of individual request logs in your Dashboard.

To expedite the resolution process, provide the request identifier when you contact us about a specific request.

If you use Stripe Connect, you can issue requests on behalf of your connected accounts. To act as a connected account, include a Stripe-Account header containing the connected account ID, which typically starts with the acct_ prefix.

The connected account ID is set per-request. Methods on the returned object reuse the same account ID.

Each major release, such as Acacia, includes changes that aren’t backward-compatible with previous releases. Upgrading to a new major release can require updates to existing code. Each monthly release includes only backward-compatible changes, and uses the same name as the last major release. You can safely upgrade to a new monthly release without breaking any existing code. The current version is 2025-12-15.clover. For information on all API versions, view our API changelog.

You can upgrade your API version in Workbench. As a precaution, use API versioning to test a new API version before committing to an upgrade.

**Examples:**

Example 1 (unknown):
```unknown
{  "object": "search_result",  "url": "/v1/customers/search",  "has_more": false,  "data": [    {      "id": "cus_4QFJOjw2pOmAGJ",      "object": "customer",      "address": null,      "balance": 0,      "created": 1405641735,      "currency": "usd",      "default_source": "card_14HOpG2eZvKYlo2Cz4u5AJG5",      "delinquent": false,      "description": "someone@example.com for Coderwall",      "discount": null,      "email": null,      "invoice_prefix": "7D11B54",      "invoice_settings": {        "custom_fields": null,        "default_payment_method": null,        "footer": null,        "rendering_options": null      },      "livemode": false,      "metadata": {        "foo": "bar"      },      "name": "fakename",      "next_invoice_sequence": 25,      "phone": null,      "preferred_locales": [],      "shipping": null,      "tax_exempt": "none",      "test_clock": null    }  ]}
```

Example 2 (unknown):
```unknown
{  "object": "search_result",  "url": "/v1/customers/search",  "has_more": false,  "data": [    {      "id": "cus_4QFJOjw2pOmAGJ",      "object": "customer",      "address": null,      "balance": 0,      "created": 1405641735,      "currency": "usd",      "default_source": "card_14HOpG2eZvKYlo2Cz4u5AJG5",      "delinquent": false,      "description": "someone@example.com for Coderwall",      "discount": null,      "email": null,      "invoice_prefix": "7D11B54",      "invoice_settings": {        "custom_fields": null,        "default_payment_method": null,        "footer": null,        "rendering_options": null      },      "livemode": false,      "metadata": {        "foo": "bar"      },      "name": "fakename",      "next_invoice_sequence": 25,      "phone": null,      "preferred_locales": [],      "shipping": null,      "tax_exempt": "none",      "test_clock": null    }  ]}
```

Example 3 (unknown):
```unknown
# The auto-pagination feature is specific to Stripe's# libraries and cannot be used directly with curl.
```

Example 4 (unknown):
```unknown
# The auto-pagination feature is specific to Stripe's# libraries and cannot be used directly with curl.
```

---

## List event destinations v2

**URL:** https://docs.stripe.com/api/v2/core/event_destinations/list

**Contents:**
- List event destinations v2
  - Parameters
    - includearray of enums
    - limitinteger
    - pagestring
  - Returns
  - Response attributes
    - dataarray of objects
    - next_page_urlnullable string
    - previous_page_urlnullable string

Lists all event destinations.

Additional fields to include in the response. Currently supports webhook_endpoint.url.

Include parameter to expose webhook_endpoint.url.

List of event destinations.

The previous page url.

Delete an event destination.

Identifier for the event destination to delete.

Identifier for the deleted event destination.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

Disable an event destination.

Identifier for the event destination to disable.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value of the object field.

Amazon EventBridge configuration.

Time at which the object was created.

An optional description of what the event destination is used for.

The list of events to enable for this endpoint.

Payload type of events being subscribed to.

Where events should be routed from.

Receive events from accounts connected to the account that owns the event destination.

Receive events from the account that owns the event destination.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Event destination name.

If using the snapshot event payload, the API version events are rendered as.

Status. It can be set to either enabled or disabled.

Event destination is disabled.

Event destination is enabled.

Additional information about event destination status.

Event destination type.

Time at which the object was last updated.

Webhook endpoint configuration.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

Enable an event destination.

Identifier for the event destination to enable.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value of the object field.

Amazon EventBridge configuration.

Time at which the object was created.

An optional description of what the event destination is used for.

The list of events to enable for this endpoint.

Payload type of events being subscribed to.

Where events should be routed from.

Receive events from accounts connected to the account that owns the event destination.

Receive events from the account that owns the event destination.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Event destination name.

If using the snapshot event payload, the API version events are rendered as.

Status. It can be set to either enabled or disabled.

Event destination is disabled.

Event destination is enabled.

Additional information about event destination status.

Event destination type.

Time at which the object was last updated.

Webhook endpoint configuration.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

This is a list of all public thin events we currently send for updates to EventDestination, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v2/core/event_destinations \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  -d "include[0]"="webhook_endpoint.url"
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v2/core/event_destinations \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  -d "include[0]"="webhook_endpoint.url"
```

Example 3 (unknown):
```unknown
{  "data": [    {      "id": "ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6",      "object": "v2.core.event_destination",      "created": "2024-10-22T16:20:09.931Z",      "description": "This is my event destination, I like it a lot",      "enabled_events": [        "v1.billing.meter.error_report_triggered"      ],      "event_payload": "thin",      "events_from": [        "self"      ],      "livemode": false,      "metadata": {},      "name": "My Event Destination",      "snapshot_api_version": null,      "status": "disabled",      "status_details": {        "disabled": {          "reason": "user"        }      },      "type": "webhook_endpoint",      "updated": "2024-10-22T16:22:02.524Z",      "webhook_endpoint": {        "signing_secret": null,        "url": null      }    }  ],  "next_page_url": null,  "previous_page_url": null}
```

Example 4 (unknown):
```unknown
{  "data": [    {      "id": "ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6",      "object": "v2.core.event_destination",      "created": "2024-10-22T16:20:09.931Z",      "description": "This is my event destination, I like it a lot",      "enabled_events": [        "v1.billing.meter.error_report_triggered"      ],      "event_payload": "thin",      "events_from": [        "self"      ],      "livemode": false,      "metadata": {},      "name": "My Event Destination",      "snapshot_api_version": null,      "status": "disabled",      "status_details": {        "disabled": {          "reason": "user"        }      },      "type": "webhook_endpoint",      "updated": "2024-10-22T16:22:02.524Z",      "webhook_endpoint": {        "signing_secret": null,        "url": null      }    }  ],  "next_page_url": null,  "previous_page_url": null}
```

---

## The Dispute object

**URL:** https://docs.stripe.com/api/disputes/object

**Contents:**
- The Dispute object
  - Attributes
    - idstring
    - amountinteger
    - chargestringExpandable
    - currencyenum
    - evidenceobject
    - metadataobject
    - payment_intentnullable stringExpandable
    - reasonstring

Unique identifier for the object.

Disputed amount. Usually the amount of the charge, but it can differ (usually because of currency fluctuation or because only part of the order is disputed).

ID of the charge that’s disputed.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

Evidence provided to respond to a dispute. Updating any field in the hash submits all fields in the hash for review.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

ID of the PaymentIntent that’s disputed.

Reason given by cardholder for dispute. Possible values are bank_cannot_process, check_returned, credit_not_processed, customer_initiated, debit_not_authorized, duplicate, fraudulent, general, incorrect_account_details, insufficient_funds, noncompliant, product_not_received, product_unacceptable, subscription_canceled, or unrecognized. Learn more about dispute reasons.

The current status of a dispute. Possible values include:warning_needs_response, warning_under_review, warning_closed, needs_response, under_review, won, lost, or prevented.

A dispute resolved in the customer’s favor.

A dispute that requires a response.

A dispute that was prevented from becoming a formal chargeback.

A dispute under review after evidence submission.

An inquiry closed without becoming a formal dispute.

An inquiry that requires a response.

An inquiry under review after evidence submission.

A dispute resolved in the merchant’s favor.

When you get a dispute, contacting your customer is always the best first step. If that doesn’t work, you can submit evidence to help us resolve the dispute in your favor. You can do this in your dashboard, but if you prefer, you can use the API to submit evidence programmatically.

Depending on your dispute type, different evidence fields will give you a better chance of winning your dispute. To figure out which evidence fields to provide, see our guide to dispute types.

Evidence to upload, to respond to a dispute. Updating any field in the hash will submit all fields in the hash for review. The combined character count of all fields is limited to 150,000.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Whether to immediately submit evidence to the bank. If false, evidence is staged on the dispute. Staged evidence is visible in the API and Dashboard, and can be submitted to the bank by making another request with this attribute set to true (the default).

Returns the dispute object.

Retrieves the dispute with the given ID.

Returns a dispute if a valid dispute ID was provided. Raises an error otherwise.

Returns a list of your disputes.

Only return disputes associated to the charge specified by this charge ID.

Only return disputes associated to the PaymentIntent specified by this PaymentIntent ID.

A dictionary with a data property that contains an array of up to limit disputes, starting after dispute starting_after. Each entry in the array is a separate dispute object. If no more disputes are available, the resulting array will be empty.

Closing the dispute for a charge indicates that you do not have any evidence to submit and are essentially dismissing the dispute, acknowledging it as lost.

The status of the dispute will change from needs_response to lost. Closing a dispute is irreversible.

Returns the dispute object.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "du_1MtJUT2eZvKYlo2CNaw2HvEv",  "object": "dispute",  "amount": 1000,  "balance_transactions": [],  "charge": "ch_1AZtxr2eZvKYlo2CJDX8whov",  "created": 1680651737,  "currency": "usd",  "evidence": {    "access_activity_log": null,    "billing_address": null,    "cancellation_policy": null,    "cancellation_policy_disclosure": null,    "cancellation_rebuttal": null,    "customer_communication": null,    "customer_email_address": null,    "customer_name": null,    "customer_purchase_ip": null,    "customer_signature": null,    "duplicate_charge_documentation": null,    "duplicate_charge_explanation": null,    "duplicate_charge_id": null,    "product_description": null,    "receipt": null,    "refund_policy": null,    "refund_policy_disclosure": null,    "refund_refusal_explanation": null,    "service_date": null,    "service_documentation": null,    "shipping_address": null,    "shipping_carrier": null,    "shipping_date": null,    "shipping_documentation": null,    "shipping_tracking_number": null,    "uncategorized_file": null,    "uncategorized_text": null  },  "evidence_details": {    "due_by": 1682294399,    "has_evidence": false,    "past_due": false,    "submission_count": 0  },  "is_charge_refundable": true,  "livemode": false,  "metadata": {},  "payment_intent": null,  "reason": "general",  "status": "warning_needs_response"}
```

Example 2 (unknown):
```unknown
{  "id": "du_1MtJUT2eZvKYlo2CNaw2HvEv",  "object": "dispute",  "amount": 1000,  "balance_transactions": [],  "charge": "ch_1AZtxr2eZvKYlo2CJDX8whov",  "created": 1680651737,  "currency": "usd",  "evidence": {    "access_activity_log": null,    "billing_address": null,    "cancellation_policy": null,    "cancellation_policy_disclosure": null,    "cancellation_rebuttal": null,    "customer_communication": null,    "customer_email_address": null,    "customer_name": null,    "customer_purchase_ip": null,    "customer_signature": null,    "duplicate_charge_documentation": null,    "duplicate_charge_explanation": null,    "duplicate_charge_id": null,    "product_description": null,    "receipt": null,    "refund_policy": null,    "refund_policy_disclosure": null,    "refund_refusal_explanation": null,    "service_date": null,    "service_documentation": null,    "shipping_address": null,    "shipping_carrier": null,    "shipping_date": null,    "shipping_documentation": null,    "shipping_tracking_number": null,    "uncategorized_file": null,    "uncategorized_text": null  },  "evidence_details": {    "due_by": 1682294399,    "has_evidence": false,    "past_due": false,    "submission_count": 0  },  "is_charge_refundable": true,  "livemode": false,  "metadata": {},  "payment_intent": null,  "reason": "general",  "status": "warning_needs_response"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/disputes/du_1MtJUT2eZvKYlo2CNaw2HvEv \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/disputes/du_1MtJUT2eZvKYlo2CNaw2HvEv \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

---

## Cards

**URL:** https://docs.stripe.com/api/cards

**Contents:**
- Cards
- The Card object
  - Attributes
    - idstring
    - address_citynullable string
    - address_countrynullable string
    - address_line1nullable string
    - address_line2nullable string
    - address_statenullable string
    - address_zipnullable string

You can store multiple cards on a customer in order to charge the customer later. You can also store multiple debit cards on a recipient in order to transfer to those cards later.

Related guide: Card payments with Sources

Unique identifier for the object.

City/District/Suburb/Town/Village.

Billing address country, if provided when creating card.

Address line 1 (Street address/PO Box/Company name).

Address line 2 (Apartment/Suite/Unit/Building).

State/County/Province/Region.

If address_zip was provided, results of the check: pass, fail, unavailable, or unchecked.

Card brand. Can be American Express, Cartes Bancaires, Diners Club, Discover, Eftpos Australia, Girocard, JCB, MasterCard, UnionPay, Visa, or Unknown.

Two-letter ISO code representing the country of the card. You could use this attribute to get a sense of the international breakdown of cards you’ve collected.

The customer that this card belongs to. This attribute will not be in the card object if the card belongs to an account or recipient instead.

If a CVC was provided, results of the check: pass, fail, unavailable, or unchecked. A result of unchecked indicates that CVC was provided but hasn’t been checked yet. Checks are typically performed when attaching a card to a Customer object, or when creating a charge. For more details, see Check if a card is valid without a charge.

Two-digit number representing the card’s expiration month.

Four-digit number representing the card’s expiration year.

Uniquely identifies this particular card number. You can use this attribute to check whether two customers who’ve signed up with you are using the same card number, for example. For payment methods that tokenize card information (Apple Pay, Google Pay), the tokenized number might be provided instead of the underlying card number.

As of May 1, 2021, card fingerprint in India for Connect changed to allow two fingerprints for the same card—one for India and one for the rest of the world.

Card funding type. Can be credit, debit, prepaid, or unknown.

The last four digits of the card.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

When you create a new credit card, you must specify a customer or recipient on which to create it.

If the card’s owner has no default card, then the new card will become the default. However, if the owner already has a default, then it will not change. To change the default, you should update the customer to have a new default_source.

A token, like the ones returned by Stripe.js or a dictionary containing a user’s card details (with the options shown below). Stripe will automatically validate the card.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the Card object.

Updates a specified card for a given customer.

City/District/Suburb/Town/Village.

Billing address country, if provided when creating card.

Address line 1 (Street address/PO Box/Company name).

Address line 2 (Apartment/Suite/Unit/Building).

State/County/Province/Region.

Two digit number representing the card’s expiration month.

Four digit number representing the card’s expiration year.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

You can always see the 10 most recent cards directly on a customer; this method lets you retrieve details about a specific card stored on the customer.

Returns the Card object.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "card_1MvoiELkdIwHu7ixOeFGbN9D",  "object": "card",  "address_city": null,  "address_country": null,  "address_line1": null,  "address_line1_check": null,  "address_line2": null,  "address_state": null,  "address_zip": null,  "address_zip_check": null,  "brand": "Visa",  "country": "US",  "customer": "cus_NhD8HD2bY8dP3V",  "cvc_check": null,  "dynamic_last4": null,  "exp_month": 4,  "exp_year": 2024,  "fingerprint": "mToisGZ01V71BCos",  "funding": "credit",  "last4": "4242",  "metadata": {},  "name": null,  "tokenization_method": null,  "wallet": null}
```

Example 2 (unknown):
```unknown
{  "id": "card_1MvoiELkdIwHu7ixOeFGbN9D",  "object": "card",  "address_city": null,  "address_country": null,  "address_line1": null,  "address_line1_check": null,  "address_line2": null,  "address_state": null,  "address_zip": null,  "address_zip_check": null,  "brand": "Visa",  "country": "US",  "customer": "cus_NhD8HD2bY8dP3V",  "cvc_check": null,  "dynamic_last4": null,  "exp_month": 4,  "exp_year": 2024,  "fingerprint": "mToisGZ01V71BCos",  "funding": "credit",  "last4": "4242",  "metadata": {},  "name": null,  "tokenization_method": null,  "wallet": null}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/customers/cus_9s6XGDTHzA66Po/sources \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d source=tok_visa
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/customers/cus_9s6XGDTHzA66Po/sources \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d source=tok_visa
```

---

## Cancel a refund

**URL:** https://docs.stripe.com/api/refunds/cancel

**Contents:**
- Cancel a refund
  - Parameters
  - Returns

Cancels a refund with a status of requires_action.

You can’t cancel refunds in other states. Only refunds for payment methods that require customer action can enter the requires_action state.

Returns the refund object if the cancellation succeeds. This call raises an error if you can’t cancel the refund.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/refunds/re_1Nispe2eZvKYlo2Cd31jOCgZ/cancel \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/refunds/re_1Nispe2eZvKYlo2Cd31jOCgZ/cancel \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "re_1Nispe2eZvKYlo2Cd31jOCgZ",  "object": "refund",  "amount": 1000,  "balance_transaction": "txn_1Nispe2eZvKYlo2CYezqFhEx",  "charge": "ch_1NirD82eZvKYlo2CIvbtLWuY",  "created": 1692942318,  "currency": "usd",  "failure_balance_transaction": "txn_3MmlLrLkdIwHu7ix0uke3Ezy",  "failure_reason": "merchant_request",  "metadata": {},  "payment_intent": "pi_1GszsK2eZvKYlo2CfhZyoZLp",  "reason": null,  "receipt_number": null,  "source_transfer_reversal": null,  "status": "canceled",  "transfer_reversal": null}
```

Example 4 (unknown):
```unknown
{  "id": "re_1Nispe2eZvKYlo2Cd31jOCgZ",  "object": "refund",  "amount": 1000,  "balance_transaction": "txn_1Nispe2eZvKYlo2CYezqFhEx",  "charge": "ch_1NirD82eZvKYlo2CIvbtLWuY",  "created": 1692942318,  "currency": "usd",  "failure_balance_transaction": "txn_3MmlLrLkdIwHu7ix0uke3Ezy",  "failure_reason": "merchant_request",  "metadata": {},  "payment_intent": "pi_1GszsK2eZvKYlo2CfhZyoZLp",  "reason": null,  "receipt_number": null,  "source_transfer_reversal": null,  "status": "canceled",  "transfer_reversal": null}
```

---

## The Mandate object

**URL:** https://docs.stripe.com/api/mandates/object

**Contents:**
- The Mandate object
  - Attributes
    - idstring
    - customer_acceptanceobject
    - payment_methodstringExpandable
    - payment_method_detailsobject
    - statusenum
    - typeenum
  - More attributesExpand all
    - objectstring

Unique identifier for the object.

Details about the customer’s acceptance of the mandate.

ID of the payment method associated with this mandate.

Additional mandate information specific to the payment method type.

The mandate status indicates whether or not you can use it to initiate a payment.

The mandate can be used to initiate a payment.

The mandate was rejected, revoked, or previously used, and may not be used to initiate future payments.

The mandate is newly created and is not yet active or inactive.

The type of the mandate.

Represents permission given for multiple payments.

Represents a one-time permission given for a single payment.

Retrieves a Mandate object.

Returns a Mandate object.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "mandate_1MvojA2eZvKYlo2CvqTABjZs",  "object": "mandate",  "customer_acceptance": {    "accepted_at": 123456789,    "online": {      "ip_address": "127.0.0.0",      "user_agent": "device"    },    "type": "online"  },  "livemode": false,  "multi_use": {},  "payment_method": "pm_123456789",  "payment_method_details": {    "sepa_debit": {      "reference": "123456789",      "url": ""    },    "type": "sepa_debit"  },  "status": "active",  "type": "multi_use"}
```

Example 2 (unknown):
```unknown
{  "id": "mandate_1MvojA2eZvKYlo2CvqTABjZs",  "object": "mandate",  "customer_acceptance": {    "accepted_at": 123456789,    "online": {      "ip_address": "127.0.0.0",      "user_agent": "device"    },    "type": "online"  },  "livemode": false,  "multi_use": {},  "payment_method": "pm_123456789",  "payment_method_details": {    "sepa_debit": {      "reference": "123456789",      "url": ""    },    "type": "sepa_debit"  },  "status": "active",  "type": "multi_use"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/mandates/mandate_1MvojA2eZvKYlo2CvqTABjZs \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/mandates/mandate_1MvojA2eZvKYlo2CvqTABjZs \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

---

## Search PaymentIntents

**URL:** https://docs.stripe.com/api/payment_intents/search

**Contents:**
- Search PaymentIntents
  - Parameters
    - querystringRequired
    - limitinteger
    - pagestring
  - Returns
- Verify microdeposits on a PaymentIntent
  - Parameters
    - amountsarray of integers
    - descriptor_codestring

Search for PaymentIntents you’ve previously created using Stripe’s Search Query Language. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.

The search query string. See search query language and the list of supported query fields for payment intents.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A dictionary with a data property that contains an array of up to limit PaymentIntents. If no objects match the query, the resulting array will be empty. See the related guide on expanding properties in lists.

Verifies microdeposits on a PaymentIntent object.

Two positive integers, in cents, equal to the values of the microdeposits sent to the bank account.

A six-character code starting with SM present in the microdeposit sent to the bank account.

Returns a PaymentIntent object.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v1/payment_intents/search \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d query="amount>1000"
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v1/payment_intents/search \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d query="amount>1000"
```

Example 3 (unknown):
```unknown
{  "object": "search_result",  "url": "/v1/payment_intents/search",  "has_more": false,  "data": [    {      "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",      "object": "payment_intent",      "amount": 2000,      "amount_capturable": 0,      "amount_details": {        "tip": {}      },      "amount_received": 0,      "application": null,      "application_fee_amount": null,      "automatic_payment_methods": {        "enabled": true      },      "canceled_at": null,      "cancellation_reason": null,      "capture_method": "automatic",      "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",      "confirmation_method": "automatic",      "created": 1680800504,      "currency": "usd",      "customer": null,      "description": null,      "last_payment_error": null,      "latest_charge": null,      "livemode": false,      "metadata": {},      "next_action": null,      "on_behalf_of": null,      "payment_method": null,      "payment_method_options": {        "card": {          "installments": null,          "mandate_options": null,          "network": null,          "request_three_d_secure": "automatic"        },        "link": {          "persistent_token": null        }      },      "payment_method_types": [        "card",        "link"      ],      "processing": null,      "receipt_email": null,      "review": null,      "setup_future_usage": null,      "shipping": null,      "source": null,      "statement_descriptor": null,      "statement_descriptor_suffix": null,      "status": "requires_payment_method",      "transfer_data": null,      "transfer_group": null    }  ]}
```

Example 4 (unknown):
```unknown
{  "object": "search_result",  "url": "/v1/payment_intents/search",  "has_more": false,  "data": [    {      "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",      "object": "payment_intent",      "amount": 2000,      "amount_capturable": 0,      "amount_details": {        "tip": {}      },      "amount_received": 0,      "application": null,      "application_fee_amount": null,      "automatic_payment_methods": {        "enabled": true      },      "canceled_at": null,      "cancellation_reason": null,      "capture_method": "automatic",      "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",      "confirmation_method": "automatic",      "created": 1680800504,      "currency": "usd",      "customer": null,      "description": null,      "last_payment_error": null,      "latest_charge": null,      "livemode": false,      "metadata": {},      "next_action": null,      "on_behalf_of": null,      "payment_method": null,      "payment_method_options": {        "card": {          "installments": null,          "mandate_options": null,          "network": null,          "request_three_d_secure": "automatic"        },        "link": {          "persistent_token": null        }      },      "payment_method_types": [        "card",        "link"      ],      "processing": null,      "receipt_email": null,      "review": null,      "setup_future_usage": null,      "shipping": null,      "source": null,      "statement_descriptor": null,      "statement_descriptor_suffix": null,      "status": "requires_payment_method",      "transfer_data": null,      "transfer_group": null    }  ]}
```

---

## Update a file link

**URL:** https://docs.stripe.com/api/file_links/update

**Contents:**
- Update a file link
  - Parameters
    - expires_atstring | timestamp
    - metadataobject
  - Returns
- Retrieve a file link
  - Parameters
  - Returns
- List all file links
  - Parameters

Updates an existing file link object. Expired links can no longer be updated.

A future timestamp after which the link will no longer be usable, or now to expire the link immediately.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the file link object if successful, and raises an error otherwise.

Retrieves the file link with the given ID.

If the identifier you provide is valid, a file link object returns. If not, Stripe raises an error.

Returns a list of file links.

A dictionary with a data property that contains an array of up to limit file links, starting after the starting_after file link. Each entry in the array is a separate file link object. If there aren’t additional available file links, the resulting array is empty.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/file_links/link_1Mr23jLkdIwHu7ix65betcoo \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/file_links/link_1Mr23jLkdIwHu7ix65betcoo \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

Example 3 (unknown):
```unknown
{  "id": "link_1Mr23jLkdIwHu7ix65betcoo",  "object": "file_link",  "created": 1680108075,  "expired": false,  "expires_at": null,  "file": "file_1Mr23iLkdIwHu7ixQkCV3CBR",  "livemode": false,  "metadata": {    "order_id": "6735"  },  "url": "https://files.stripe.com/links/MDB8YWNjdF8xTTJKVGtMa2RJd0h1N2l4fGZsX3Rlc3RfaXVoY2hrUnJPMzlBR3dPb01XMmFkSTVq00yUPLFf3h"}
```

Example 4 (unknown):
```unknown
{  "id": "link_1Mr23jLkdIwHu7ix65betcoo",  "object": "file_link",  "created": 1680108075,  "expired": false,  "expires_at": null,  "file": "file_1Mr23iLkdIwHu7ixQkCV3CBR",  "livemode": false,  "metadata": {    "order_id": "6735"  },  "url": "https://files.stripe.com/links/MDB8YWNjdF8xTTJKVGtMa2RJd0h1N2l4fGZsX3Rlc3RfaXVoY2hrUnJPMzlBR3dPb01XMmFkSTVq00yUPLFf3h"}
```

---

## The Product object

**URL:** https://docs.stripe.com/api/products/object

**Contents:**
- The Product object
  - Attributes
    - idstring
    - activeboolean
    - default_pricenullable stringExpandable
    - descriptionnullable string
    - metadataobject
    - namestring
    - tax_codenullable stringExpandable
  - More attributesExpand all

Unique identifier for the object.

Whether the product is currently available for purchase.

The ID of the Price object that is the default price for this product.

The product’s description, meant to be displayable to the customer. Use this field to optionally store a long form explanation of the product being sold for your own rendering purposes.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The product’s name, meant to be displayable to the customer.

Creates a new product object.

The product’s name, meant to be displayable to the customer.

Whether the product is currently available for purchase. Defaults to true.

The product’s description, meant to be displayable to the customer. Use this field to optionally store a long form explanation of the product being sold for your own rendering purposes.

An identifier will be randomly generated by Stripe. You can optionally override this ID, but the ID must be unique across all products in your Stripe account.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a product object if the call succeeded.

Updates the specific product by setting the values of the parameters passed. Any parameters not provided will be left unchanged.

Whether the product is available for purchase.

The ID of the Price object that is the default price for this product.

The product’s description, meant to be displayable to the customer. Use this field to optionally store a long form explanation of the product being sold for your own rendering purposes.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The product’s name, meant to be displayable to the customer.

Returns the product object if the update succeeded.

Retrieves the details of an existing product. Supply the unique product ID from either a product creation request or the product list, and Stripe will return the corresponding product information.

Returns a product object if a valid identifier was provided.

Returns a list of your products. The products are returned sorted by creation date, with the most recently created products appearing first.

Only return products that are active or inactive (e.g., pass false to list all inactive products).

A dictionary with a data property that contains an array of up to limit products, starting after product starting_after. Each entry in the array is a separate product object. If no more products are available, the resulting array will be empty.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "prod_NWjs8kKbJWmuuc",  "object": "product",  "active": true,  "created": 1678833149,  "default_price": null,  "description": null,  "images": [],  "marketing_features": [],  "livemode": false,  "metadata": {},  "name": "Gold Plan",  "package_dimensions": null,  "shippable": null,  "statement_descriptor": null,  "tax_code": null,  "unit_label": null,  "updated": 1678833149,  "url": null}
```

Example 2 (unknown):
```unknown
{  "id": "prod_NWjs8kKbJWmuuc",  "object": "product",  "active": true,  "created": 1678833149,  "default_price": null,  "description": null,  "images": [],  "marketing_features": [],  "livemode": false,  "metadata": {},  "name": "Gold Plan",  "package_dimensions": null,  "shippable": null,  "statement_descriptor": null,  "tax_code": null,  "unit_label": null,  "updated": 1678833149,  "url": null}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/products \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d name="Gold Plan"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/products \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d name="Gold Plan"
```

---

## Visa Compelling Evidence 3.0 disputes

**URL:** https://docs.stripe.com/disputes/api/visa-ce3

**Contents:**
- Visa Compelling Evidence 3.0 disputes
- Use the API and Visa's Compelling Evidence 3.0 to respond to qualifying disputes.
- Visa CE 3.0 qualifying disputes
    - Note
- The enhanced evidence object
- The enhanced eligibility object
- Autofilled evidence
    - Note
- Submission lifecycle
    - Note

Visa Compelling Evidence 3.0 (CE 3.0) has new qualifying criteria allowing businesses to demonstrate a non-fraudulent history with cardholders to fight friendly fraud. Submitting qualifying evidence for Visa CE 3.0 eligible disputes can increase the chance of an issuer reversing friendly fraud disputes in favor of the business.

To respond to a dispute using Visa CE 3.0, the dispute must meet the following criteria:

Customer Device Fingerprint and Customer Device ID isn’t a valid evidence combination.

To submit evidence using Visa CE 3.0, use the enhanced evidence object. This exists within the dispute evidence object. The enhanced eligibility types array contains a list of eligibility types in enhanced evidence.

The enhanced eligibility object shows the status of your Visa CE 3.0 submission. This exists within the evidence details object and provides detailed information on the steps required to ensure evidence is submitted to Visa as CE 3.0.

When Stripe identifies a disputed transaction as eligible for Visa CE 3.0, Stripe attempts to autofill the disputed transaction and evidence from previous undisputed transactions. You have the option to manually add Visa CE 3.0 evidence if you believe the disputed transaction qualifies.

Stripe must have processed all past undisputed transactions.

The Visa CE 3.0 status becomes qualified or requires_action when a dispute has the Visa Compelling Evidence 3 object filled within the enhanced evidence object.

You can submit evidence using the Update dispute API. To update evidence without submitting it, make sure the submit parameter is set to false.

After submitting evidence, the status changes to not_qualified if the evidence is ineligible for Visa CE 3.0. Evidence is still submitted, but not using Visa CE 3.0.

If you have submitted qualifying evidence, track the status of the dispute in the dispute status field to see if you’ve won or lost.

To increase your chances of winning a dispute, fill out the dispute evidence object (not just the enhanced evidence object). This evidence is used in case your Visa CE 3.0 submission is disapproved, and your dispute is submitted through the standard evidence submission flow.

To test your Visa CE 3.0 integration, use the following test card, which creates a Visa CE 3.0 eligible dispute:

When providing evidence for this dispute, you can submit any two test environment transactions in the prior_undisputed_transactions.charge field.

In test environments, you can use any two test transactions as prior_undisputed_transactions. Stripe doesn’t validate the prior transactions’ payment method or transaction date while testing.

We’ll validate primary and secondary evidence elements according Visa CE 3.0 rules.

The Visa CE 3.0 status properly reflects qualified or requires_action based on the evidence provided.

After you submit evidence, the Visa CE 3.0 status is:

The Visa CE 3.0 status doesn’t impact the dispute status.

To simulate a won or lost state for the overall dispute, set uncategorized_text to winning_evidence or losing_evidence as outlined in Testing.

**Examples:**

Example 1 (unknown):
```unknown
{
  "id": "du_TFCU9xJ2Gsj7BAiAoQok8Icp",
  "charge": "ch_vEUUPELhHVkPbMN1md3B0vG7",
  "enhanced_eligibility_types": ["visa_compelling_evidence_3"],
  "evidence": {
    "enhanced_evidence": {
      "visa_compelling_evidence_3": {
        "disputed_transaction": {
          "customer_email_address": "test@example.com",
          "customer_purchase_ip": "123.123.123.123",
          "merchandise_or_services": "merchandise",
          "product_description": "Widget ABC, color: green",
        },
        "prior_undisputed_transactions": [
          {
            "charge": "ch_nE8T8mUOoy9zkkOQLHuLsr3Z",
            "customer_email_address": "test@example.com",
            "customer_purchase_ip": "123.123.123.123",
            "product_description": "Widget DEF, color: blue"
          },
          {
            "charge": "ch_PcE97JB902XNTc1JpyBFmMTF",
            "customer_email_address": "test@example.com",
            "customer_purchase_ip": "123.123.123.123",
            "product_description": "Widget XYZ, color: yellow"
          }
        ]
      }
    },
  }
  ...
}
```

Example 2 (unknown):
```unknown
{
  "id": "du_TFCU9xJ2Gsj7BAiAoQok8Icp",
  "charge": "ch_vEUUPELhHVkPbMN1md3B0vG7",
  "enhanced_eligibility_types": ["visa_compelling_evidence_3"],
  "evidence": {
    "enhanced_evidence": {
      "visa_compelling_evidence_3": {
        "disputed_transaction": {
          "customer_email_address": "test@example.com",
          "customer_purchase_ip": "123.123.123.123",
          "merchandise_or_services": "merchandise",
          "product_description": "Widget ABC, color: green",
        },
        "prior_undisputed_transactions": [
          {
            "charge": "ch_nE8T8mUOoy9zkkOQLHuLsr3Z",
            "customer_email_address": "test@example.com",
            "customer_purchase_ip": "123.123.123.123",
            "product_description": "Widget DEF, color: blue"
          },
          {
            "charge": "ch_PcE97JB902XNTc1JpyBFmMTF",
            "customer_email_address": "test@example.com",
            "customer_purchase_ip": "123.123.123.123",
            "product_description": "Widget XYZ, color: yellow"
          }
        ]
      }
    },
  }
  ...
}
```

Example 3 (unknown):
```unknown
{
  "enhanced_eligibility_types": ["visa_compelling_evidence_3"],
  "evidence_details": {
    "due_by": 1708387199,
    "enhanced_eligibility": {
      "visa_compelling_evidence_3": {
        "partner_rejected_details": null,
        "required_actions": [
          "missing_merchandise_or_services",
          "missing_disputed_transaction_description"
        ],
        "status": "requires_action"
      }
    },
    "has_evidence": false,
    "past_due": false,
    "submission_count": 0
  },
  "payment_method_details": {
    "card": {
      "brand": "visa",
      "network_reason_code": "10.4"
    },
    "type": "card"
  },
  "reason": "fraudulent",
  "status": "needs_response"
}
```

Example 4 (unknown):
```unknown
{
  "enhanced_eligibility_types": ["visa_compelling_evidence_3"],
  "evidence_details": {
    "due_by": 1708387199,
    "enhanced_eligibility": {
      "visa_compelling_evidence_3": {
        "partner_rejected_details": null,
        "required_actions": [
          "missing_merchandise_or_services",
          "missing_disputed_transaction_description"
        ],
        "status": "requires_action"
      }
    },
    "has_evidence": false,
    "past_due": false,
    "submission_count": 0
  },
  "payment_method_details": {
    "card": {
      "brand": "visa",
      "network_reason_code": "10.4"
    },
    "type": "card"
  },
  "reason": "fraudulent",
  "status": "needs_response"
}
```

---

## Customer Balance Transaction

**URL:** https://docs.stripe.com/api/customer_balance_transactions

**Contents:**
- Customer Balance Transaction
- The Customer Balance Transaction object
  - Attributes
    - idstring
    - amountinteger
    - currencyenum
    - customerstringExpandable
    - customer_accountnullable string
    - descriptionnullable string
    - ending_balanceinteger

Each customer has a Balance value, which denotes a debit or credit that’s automatically applied to their next invoice upon finalization. You may modify the value directly by using the update customer API, or by creating a Customer Balance Transaction, which increments or decrements the customer’s balance by the specified amount.

Related guide: Customer balance

Unique identifier for the object.

The amount of the transaction. A negative value is a credit for the customer’s balance, and a positive value is a debit to the customer’s balance.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

The ID of the customer the transaction belongs to.

The ID of an Account representing a customer that the transaction belongs to.

An arbitrary string attached to the object. Often useful for displaying to users.

The customer’s balance after the transaction was applied. A negative value decreases the amount due on the customer’s next invoice. A positive value increases the amount due on the customer’s next invoice.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Transaction type: adjustment, applied_to_invoice, credit_note, initial, invoice_overpaid, invoice_too_large, invoice_too_small, unspent_receiver_credit, unapplied_from_invoice, checkout_session_subscription_payment, or checkout_session_subscription_payment_canceled. See the Customer Balance page to learn more about transaction types.

An explicitly created adjustment transaction to debit or credit the credit balance.

Traces the application of credit against a linked Invoice.

Traces the customer balance applied to an Invoice to be created for the linked Checkout Session.

Traces the reversal of an applied balance by the linked Checkout Session. Paired with an earlier ‘checkout_session_subscription_payment‘ transaction.

Traces the creation of credit to a Credit Note and its associated Invoice.

The starting value of the customer’s credit balance.

Credits to the credit balance when an invoice receives payments exceeding the amount due.

Debits to the credit balance when the amount due on an invoice is greater than Stripe’s maximum chargeable amount and the customer does not have a cash balance.

Debits to the credit balance when the amount due on an invoice is less than Stripe’s minimum chargeable amount and the customer does not have a cash balance.

Funds migrated from the legacy customer credit balance.

Creates an immutable transaction that updates the customer’s credit balance.

The integer amount in cents to apply to the customer’s credit balance.

Three-letter ISO currency code, in lowercase. Must be a supported currency. Specifies the invoice_credit_balance that this transaction will apply to. If the customer’s currency is not set, it will be updated to this value.

An arbitrary string attached to the object. Often useful for displaying to users.

The maximum length is 350 characters.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a customer balance transaction object if the call succeeded.

Most credit balance transaction fields are immutable, but you may update its description and metadata.

An arbitrary string attached to the object. Often useful for displaying to users.

The maximum length is 350 characters.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a customer balance transaction object if the call succeeded.

Retrieves a specific customer balance transaction that updated the customer’s balances.

Returns a customer balance transaction object if a valid identifier was provided.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "cbtxn_1MrU9qLkdIwHu7ixhdjxGBgI",  "object": "customer_balance_transaction",  "amount": -500,  "created": 1680216086,  "credit_note": null,  "currency": "usd",  "customer": "cus_NcjdgdwZyI9Rj7",  "description": null,  "ending_balance": -500,  "invoice": null,  "livemode": false,  "metadata": {},  "type": "adjustment"}
```

Example 2 (unknown):
```unknown
{  "id": "cbtxn_1MrU9qLkdIwHu7ixhdjxGBgI",  "object": "customer_balance_transaction",  "amount": -500,  "created": 1680216086,  "credit_note": null,  "currency": "usd",  "customer": "cus_NcjdgdwZyI9Rj7",  "description": null,  "ending_balance": -500,  "invoice": null,  "livemode": false,  "metadata": {},  "type": "adjustment"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/customers/cus_NcjdgdwZyI9Rj7/balance_transactions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=-500 \  -d currency=usd
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/customers/cus_NcjdgdwZyI9Rj7/balance_transactions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=-500 \  -d currency=usd
```

---

## The PersonToken object

**URL:** https://docs.stripe.com/api/v2/person-tokens/object

**Contents:**
- The PersonToken object
  - Attributes
    - idstring
    - objectstring, value is "v2.core.account_person_token"
    - createdtimestamp
    - expires_attimestamp
    - livemodeboolean
    - usedboolean
- Create a person token v2
  - Parameters

Unique identifier for the token.

String representing the object’s type. Objects of the same type share the same value of the object field.

Time at which the token was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Time at which the token will expire.

Has the value true if the token exists in live mode or the value false if the object exists in test mode.

Determines if the token has already been used (tokens can only be used once).

Creates a Person Token associated with an Account.

The Account the Person is associated with.

Additional addresses associated with the person.

Additional names (e.g. aliases) associated with the person.

Attestations of accepted terms of service agreements.

The person’s residential address.

The person’s date of birth.

Documents that may be submitted to satisfy various informational requests.

The person’s first name.

The identification numbers (e.g., SSN) associated with the person.

The person’s gender (International regulations require either “male” or “female”).

Female gender person.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The nationalities (countries) this person is associated with.

The phone number for this person.

The person’s political exposure.

The person has disclosed that they do have political exposure.

The person has disclosed that they have no political exposure.

The relationship that this person has with the Account’s business or legal entity.

The script addresses (e.g., non-Latin characters) associated with the person.

The script names (e.g. non-Latin characters) associated with the person.

The person’s last name.

Unique identifier for the token.

String representing the object’s type. Objects of the same type share the same value of the object field.

Time at which the token was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Time at which the token will expire.

Has the value true if the token exists in live mode or the value false if the object exists in test mode.

Determines if the token has already been used (tokens can only be used once).

Token must be created with publishable key.

Retrieves a Person Token associated with an Account.

The Account the Person is associated with.

The ID of the Person Token to retrieve.

Unique identifier for the token.

String representing the object’s type. Objects of the same type share the same value of the object field.

Time at which the token was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

Time at which the token will expire.

Has the value true if the token exists in live mode or the value false if the object exists in test mode.

Determines if the token has already been used (tokens can only be used once).

The resource wasn’t found.

**Examples:**

Example 1 (unknown):
```unknown
{  "created": "2025-01-01T00:00:00.000Z",  "expires_at": "2025-01-01T00:00:00.000Z",  "id": "4242",  "livemode": true,  "object": "4242",  "used": true}
```

Example 2 (unknown):
```unknown
{  "created": "2025-01-01T00:00:00.000Z",  "expires_at": "2025-01-01T00:00:00.000Z",  "id": "4242",  "livemode": true,  "object": "4242",  "used": true}
```

Example 3 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/person_tokens \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "given_name": "Jenny",    "surname": "Rosen",    "email": "jenny.rosen@example.com",    "address": {        "line1": "27 Fredrick Ave",        "city": "Brothers",        "postal_code": "97712",        "state": "OR",        "country": "US"    },    "id_numbers": [        {            "type": "us_ssn_last_4",            "value": "0000"        }    ],    "relationship": {        "owner": true,        "percent_ownership": "0.8",        "representative": true,        "title": "CEO"    }  }'
```

Example 4 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/person_tokens \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "given_name": "Jenny",    "surname": "Rosen",    "email": "jenny.rosen@example.com",    "address": {        "line1": "27 Fredrick Ave",        "city": "Brothers",        "postal_code": "97712",        "state": "OR",        "country": "US"    },    "id_numbers": [        {            "type": "us_ssn_last_4",            "value": "0000"        }    ],    "relationship": {        "owner": true,        "percent_ownership": "0.8",        "representative": true,        "title": "CEO"    }  }'
```

---

## Refunds

**URL:** https://docs.stripe.com/api/refunds

**Contents:**
- Refunds
- The Refund object
  - Attributes
    - idstring
    - amountinteger
    - chargenullable stringExpandable
    - currencyenum
    - descriptionnullable string
    - metadatanullable object
    - payment_intentnullable stringExpandable

Refund objects allow you to refund a previously created charge that isn’t refunded yet. Funds are refunded to the credit or debit card that’s initially charged.

Related guide: Refunds

Unique identifier for the object.

ID of the charge that’s refunded.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

An arbitrary string attached to the object. You can use this for displaying to users (available on non-card refunds only).

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

ID of the PaymentIntent that’s refunded.

Reason for the refund, which is either user-provided (duplicate, fraudulent, or requested_by_customer) or generated by Stripe internally (expired_uncaptured_charge).

Status of the refund. This can be pending, requires_action, succeeded, failed, or canceled. Learn more about failed refunds.

When you create a new refund, you must specify a Charge or a PaymentIntent object on which to create it.

Creating a new refund will refund a charge that has previously been created but not yet refunded. Funds will be refunded to the credit or debit card that was originally charged.

You can optionally refund only part of a charge. You can do so multiple times, until the entire charge has been refunded.

Once entirely refunded, a charge can’t be refunded again. This method will raise an error when called on an already-refunded charge, or when trying to refund more money than is left on a charge.

A positive integer in the smallest currency unit representing how much of this charge to refund. Can refund only up to the remaining, unrefunded amount of the charge.

The identifier of the charge to refund.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The identifier of the PaymentIntent to refund.

String indicating the reason for the refund. If set, possible values are duplicate, fraudulent, and requested_by_customer. If you believe the charge to be fraudulent, specifying fraudulent as the reason will add the associated card and email to your block lists, and will also help us improve our fraud detection algorithms.

Returns the Refund object if the refund succeeded. Raises an error if the Charge/PaymentIntent has already been refunded, or if an invalid identifier was provided.

Updates the refund that you specify by setting the values of the passed parameters. Any parameters that you don’t provide remain unchanged.

This request only accepts metadata as an argument.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the refund object if the update succeeds. This call raises an error if update parameters are invalid.

Retrieves the details of an existing refund.

Returns a refund if you provide a valid ID. Raises an error otherwise.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "re_1Nispe2eZvKYlo2Cd31jOCgZ",  "object": "refund",  "amount": 1000,  "balance_transaction": "txn_1Nispe2eZvKYlo2CYezqFhEx",  "charge": "ch_1NirD82eZvKYlo2CIvbtLWuY",  "created": 1692942318,  "currency": "usd",  "destination_details": {    "card": {      "reference": "123456789012",      "reference_status": "available",      "reference_type": "acquirer_reference_number",      "type": "refund"    },    "type": "card"  },  "metadata": {},  "payment_intent": "pi_1GszsK2eZvKYlo2CfhZyoZLp",  "reason": null,  "receipt_number": null,  "source_transfer_reversal": null,  "status": "succeeded",  "transfer_reversal": null}
```

Example 2 (unknown):
```unknown
{  "id": "re_1Nispe2eZvKYlo2Cd31jOCgZ",  "object": "refund",  "amount": 1000,  "balance_transaction": "txn_1Nispe2eZvKYlo2CYezqFhEx",  "charge": "ch_1NirD82eZvKYlo2CIvbtLWuY",  "created": 1692942318,  "currency": "usd",  "destination_details": {    "card": {      "reference": "123456789012",      "reference_status": "available",      "reference_type": "acquirer_reference_number",      "type": "refund"    },    "type": "card"  },  "metadata": {},  "payment_intent": "pi_1GszsK2eZvKYlo2CfhZyoZLp",  "reason": null,  "receipt_number": null,  "source_transfer_reversal": null,  "status": "succeeded",  "transfer_reversal": null}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/refunds \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d charge=ch_1NirD82eZvKYlo2CIvbtLWuY
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/refunds \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d charge=ch_1NirD82eZvKYlo2CIvbtLWuY
```

---

## Payment Methods

**URL:** https://docs.stripe.com/api/payment_methods

**Contents:**
- Payment Methods
- The PaymentMethod object
  - Attributes
    - idstring
    - billing_detailsobject
    - customernullable stringExpandable
    - metadatanullable object
    - typeenum
  - More attributesExpand all
    - objectstring

PaymentMethod objects represent your customer’s payment instruments. You can use them with PaymentIntents to collect payments or save them to Customer objects to store instrument details for future payments.

Related guides: Payment Methods and More Payment Scenarios.

Unique identifier for the object.

Billing information associated with the PaymentMethod that may be used or required by particular types of payment methods.

The ID of the Customer to which this PaymentMethod is saved. This will not be set when the PaymentMethod has not been saved to a Customer.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The type of the PaymentMethod. An additional hash is included on the PaymentMethod with a name matching this value. It contains additional information specific to the PaymentMethod type.

Pre-authorized debit payments are used to debit Canadian bank accounts through the Automated Clearing Settlement System (ACSS).

Affirm is a buy now, pay later payment method in the US.

Afterpay / Clearpay is a buy now, pay later payment method used in Australia, Canada, France, New Zealand, Spain, the UK, and the US.

Alipay is a digital wallet payment method used in China.

Alma is a Buy Now, Pay Later payment method that lets customers pay in 2, 3, or 4 installments.

Amazon Pay is a Wallet payment method that lets hundreds of millions of Amazon customers pay their way, every day.

BECS Direct Debit is used to debit Australian bank accounts through the Bulk Electronic Clearing System (BECS).

Bacs Direct Debit is used to debit UK bank accounts.

Bancontact is a bank redirect payment method used in Belgium.

Billie is a payment method.

Creates a PaymentMethod object. Read the Stripe.js reference to learn how to create PaymentMethods via Stripe.js.

Instead of creating a PaymentMethod directly, we recommend using the PaymentIntents API to accept a payment immediately or the SetupIntent API to collect payment method details ahead of a future payment.

The type of the PaymentMethod. An additional hash is included on the PaymentMethod with a name matching this value. It contains additional information specific to the PaymentMethod type.

Pre-authorized debit payments are used to debit Canadian bank accounts through the Automated Clearing Settlement System (ACSS).

Affirm is a buy now, pay later payment method in the US.

Afterpay / Clearpay is a buy now, pay later payment method used in Australia, Canada, France, New Zealand, Spain, the UK, and the US.

Alipay is a digital wallet payment method used in China.

Alma is a Buy Now, Pay Later payment method that lets customers pay in 2, 3, or 4 installments.

Amazon Pay is a Wallet payment method that lets hundreds of millions of Amazon customers pay their way, every day.

BECS Direct Debit is used to debit Australian bank accounts through the Bulk Electronic Clearing System (BECS).

Bacs Direct Debit is used to debit UK bank accounts.

Bancontact is a bank redirect payment method used in Belgium.

Billie is a payment method.

Billing information associated with the PaymentMethod that may be used or required by particular types of payment methods.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a PaymentMethod object.

Updates a PaymentMethod object. A PaymentMethod must be attached to a customer to be updated.

Billing information associated with the PaymentMethod that may be used or required by particular types of payment methods.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a PaymentMethod object.

Retrieves a PaymentMethod object for a given Customer.

Returns a PaymentMethod object.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "pm_1Q0PsIJvEtkwdCNYMSaVuRz6",  "object": "payment_method",  "allow_redisplay": "unspecified",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": "John Doe",    "phone": null  },  "created": 1726673582,  "customer": null,  "livemode": false,  "metadata": {},  "type": "us_bank_account",  "us_bank_account": {    "account_holder_type": "individual",    "account_type": "checking",    "bank_name": "STRIPE TEST BANK",    "financial_connections_account": null,    "fingerprint": "LstWJFsCK7P349Bg",    "last4": "6789",    "networks": {      "preferred": "ach",      "supported": [        "ach"      ]    },    "routing_number": "110000000",    "status_details": {}  }}
```

Example 2 (unknown):
```unknown
{  "id": "pm_1Q0PsIJvEtkwdCNYMSaVuRz6",  "object": "payment_method",  "allow_redisplay": "unspecified",  "billing_details": {    "address": {      "city": null,      "country": null,      "line1": null,      "line2": null,      "postal_code": null,      "state": null    },    "email": null,    "name": "John Doe",    "phone": null  },  "created": 1726673582,  "customer": null,  "livemode": false,  "metadata": {},  "type": "us_bank_account",  "us_bank_account": {    "account_holder_type": "individual",    "account_type": "checking",    "bank_name": "STRIPE TEST BANK",    "financial_connections_account": null,    "fingerprint": "LstWJFsCK7P349Bg",    "last4": "6789",    "networks": {      "preferred": "ach",      "supported": [        "ach"      ]    },    "routing_number": "110000000",    "status_details": {}  }}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_methods \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d type=us_bank_account \  -d "us_bank_account[account_holder_type]"=individual \  -d "us_bank_account[account_number]"=000123456789 \  -d "us_bank_account[routing_number]"=110000000 \  -d "billing_details[name]"="John Doe"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_methods \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d type=us_bank_account \  -d "us_bank_account[account_holder_type]"=individual \  -d "us_bank_account[account_number]"=000123456789 \  -d "us_bank_account[routing_number]"=110000000 \  -d "billing_details[name]"="John Doe"
```

---

## Verify microdeposits on a PaymentIntent

**URL:** https://docs.stripe.com/api/payment_intents/verify_microdeposits

**Contents:**
- Verify microdeposits on a PaymentIntent
  - Parameters
    - amountsarray of integers
    - descriptor_codestring
  - Returns

Verifies microdeposits on a PaymentIntent object.

Two positive integers, in cents, equal to the values of the microdeposits sent to the bank account.

A six-character code starting with SM present in the microdeposit sent to the bank account.

Returns a PaymentIntent object.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents/pi_1DtBRR2eZvKYlo2CmCVxxvd7/verify_microdeposits \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "amounts[]"=32 \  -d "amounts[]"=45
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents/pi_1DtBRR2eZvKYlo2CmCVxxvd7/verify_microdeposits \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "amounts[]"=32 \  -d "amounts[]"=45
```

Example 3 (unknown):
```unknown
{  "id": "pi_1DtBRR2eZvKYlo2CmCVxxvd7",  "object": "payment_intent",  "amount": 1099,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 0,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": null,  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_1DtBRR2eZvKYlo2CmCVxxvd7_secret_l80vlOGz9kZQwnzocExJQUsJx",  "confirmation_method": "automatic",  "created": 1680800210,  "currency": "usd",  "customer": null,  "description": null,  "last_payment_error": null,  "latest_charge": null,  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": "pm_1Mtw7C2eZvKYlo2CPsW0F8g0",  "payment_method_options": {    "acss_debit": {      "mandate_options": {        "interval_description": "First day of every month",        "payment_schedule": "interval",        "transaction_type": "personal"      },      "verification_method": "automatic"    }  },  "payment_method_types": [    "acss_debit"  ],  "processing": null,  "receipt_email": null,  "redaction": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "succeeded",  "transfer_data": null,  "transfer_group": null}
```

Example 4 (unknown):
```unknown
{  "id": "pi_1DtBRR2eZvKYlo2CmCVxxvd7",  "object": "payment_intent",  "amount": 1099,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 0,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": null,  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_1DtBRR2eZvKYlo2CmCVxxvd7_secret_l80vlOGz9kZQwnzocExJQUsJx",  "confirmation_method": "automatic",  "created": 1680800210,  "currency": "usd",  "customer": null,  "description": null,  "last_payment_error": null,  "latest_charge": null,  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": "pm_1Mtw7C2eZvKYlo2CPsW0F8g0",  "payment_method_options": {    "acss_debit": {      "mandate_options": {        "interval_description": "First day of every month",        "payment_schedule": "interval",        "transaction_type": "personal"      },      "verification_method": "automatic"    }  },  "payment_method_types": [    "acss_debit"  ],  "processing": null,  "receipt_email": null,  "redaction": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "succeeded",  "transfer_data": null,  "transfer_group": null}
```

---

## Shipping Rates

**URL:** https://docs.stripe.com/api/shipping_rates

**Contents:**
- Shipping Rates
- The Shipping Rate object
  - Attributes
    - idstring
    - activeboolean
    - display_namenullable string
    - fixed_amountnullable object
    - metadataobject
    - tax_behaviornullable enum
    - tax_codenullable stringExpandable

Shipping rates describe the price of shipping presented to your customers and applied to a purchase. For more information, see Charge for shipping.

Unique identifier for the object.

Whether the shipping rate can be used for new purchases. Defaults to true.

The name of the shipping rate, meant to be displayable to the customer. This will appear on CheckoutSessions.

Describes a fixed amount to charge for shipping. Must be present if type is fixed_amount.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Specifies whether the rate is considered inclusive of taxes or exclusive of taxes. One of inclusive, exclusive, or unspecified.

A tax code ID. The Shipping tax code is txcd_92010001.

The type of calculation to use on the shipping rate.

The shipping rate is a fixed amount.

Creates a new shipping rate object.

The name of the shipping rate, meant to be displayable to the customer. This will appear on CheckoutSessions.

The maximum length is 100 characters.

Describes a fixed amount to charge for shipping. Must be present if type is fixed_amount.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Specifies whether the rate is considered inclusive of taxes or exclusive of taxes. One of inclusive, exclusive, or unspecified.

A tax code ID. The Shipping tax code is txcd_92010001.

The type of calculation to use on the shipping rate.

The shipping rate is a fixed amount.

Returns a shipping rate object if the call succeeded.

Updates an existing shipping rate object.

Whether the shipping rate can be used for new purchases. Defaults to true.

Describes a fixed amount to charge for shipping. Must be present if type is fixed_amount.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Specifies whether the rate is considered inclusive of taxes or exclusive of taxes. One of inclusive, exclusive, or unspecified.

Returns the modified shipping rate object if the call succeeded.

Returns the shipping rate object with the given ID.

Returns a shipping rate object if a valid identifier was provided.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "shr_1MrRx2LkdIwHu7ixikgEA6Wd",  "object": "shipping_rate",  "active": true,  "created": 1680207604,  "delivery_estimate": null,  "display_name": "Ground shipping",  "fixed_amount": {    "amount": 500,    "currency": "usd"  },  "livemode": false,  "metadata": {},  "tax_behavior": "unspecified",  "tax_code": null,  "type": "fixed_amount"}
```

Example 2 (unknown):
```unknown
{  "id": "shr_1MrRx2LkdIwHu7ixikgEA6Wd",  "object": "shipping_rate",  "active": true,  "created": 1680207604,  "delivery_estimate": null,  "display_name": "Ground shipping",  "fixed_amount": {    "amount": 500,    "currency": "usd"  },  "livemode": false,  "metadata": {},  "tax_behavior": "unspecified",  "tax_code": null,  "type": "fixed_amount"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/shipping_rates \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d display_name="Ground shipping" \  -d type=fixed_amount \  -d "fixed_amount[amount]"=500 \  -d "fixed_amount[currency]"=usd
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/shipping_rates \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d display_name="Ground shipping" \  -d type=fixed_amount \  -d "fixed_amount[amount]"=500 \  -d "fixed_amount[currency]"=usd
```

---

## Update a payout

**URL:** https://docs.stripe.com/api/payouts/update

**Contents:**
- Update a payout
  - Parameters
    - metadataobject
  - Returns
- Retrieve a payout
  - Parameters
  - Returns
- List all payouts
  - Parameters
    - statusstring

Updates the specified payout by setting the values of the parameters you pass. We don’t change parameters that you don’t provide. This request only accepts the metadata as arguments.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the payout object if the update succeeds. This call raises an error if update parameters are invalid.

Retrieves the details of an existing payout. Supply the unique payout ID from either a payout creation request or the payout list. Stripe returns the corresponding payout information.

Returns a payout object if a you provide a valid identifier. raises An error occurs otherwise.

Returns a list of existing payouts sent to third-party bank accounts or payouts that Stripe sent to you. The payouts return in sorted order, with the most recently created payouts appearing first.

Only return payouts that have the given status: pending, paid, failed, or canceled.

A dictionary with a data property that contains an array of up to limit payouts, starting after payout starting_after. Each entry in the array is a separate payout object. If no other payouts are available, the resulting array is empty.

You can cancel a previously created payout if its status is pending. Stripe refunds the funds to your available balance. You can’t cancel automatic Stripe payouts.

Returns the payout object if the cancellation succeeds. Returns an error if the payout is already canceled or can’t be canceled.

Reverses a payout by debiting the destination bank account. At this time, you can only reverse payouts for connected accounts to US and Canadian bank accounts. If the payout is manual and in the pending status, use /v1/payouts/:id/cancel instead.

By requesting a reversal through /v1/payouts/:id/reverse, you confirm that the authorized signatory of the selected bank account authorizes the debit on the bank account and that no other authorization is required.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the reversing payout object if the reversal is successful. Returns an error if the payout is already reversed or can’t be reversed.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payouts/po_1OaFDbEcg9tTZuTgNYmX0PKB \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payouts/po_1OaFDbEcg9tTZuTgNYmX0PKB \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

Example 3 (unknown):
```unknown
{  "id": "po_1OaFDbEcg9tTZuTgNYmX0PKB",  "object": "payout",  "amount": 1100,  "arrival_date": 1680652800,  "automatic": false,  "balance_transaction": "txn_1OaFDcEcg9tTZuTgYMR25tSe",  "created": 1680648691,  "currency": "usd",  "description": null,  "destination": "ba_1MtIhL2eZvKYlo2CAElKwKu2",  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "livemode": false,  "metadata": {    "order_id": "6735"  },  "method": "standard",  "original_payout": null,  "reconciliation_status": "not_applicable",  "reversed_by": null,  "source_type": "card",  "statement_descriptor": null,  "status": "pending",  "type": "bank_account"}
```

Example 4 (unknown):
```unknown
{  "id": "po_1OaFDbEcg9tTZuTgNYmX0PKB",  "object": "payout",  "amount": 1100,  "arrival_date": 1680652800,  "automatic": false,  "balance_transaction": "txn_1OaFDcEcg9tTZuTgYMR25tSe",  "created": 1680648691,  "currency": "usd",  "description": null,  "destination": "ba_1MtIhL2eZvKYlo2CAElKwKu2",  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "livemode": false,  "metadata": {    "order_id": "6735"  },  "method": "standard",  "original_payout": null,  "reconciliation_status": "not_applicable",  "reversed_by": null,  "source_type": "card",  "statement_descriptor": null,  "status": "pending",  "type": "bank_account"}
```

---

## Create an account link v2

**URL:** https://docs.stripe.com/api/v2/core/account-links/create

**Contents:**
- Create an account link v2
  - Parameters
    - accountstringRequired
    - use_caseobjectRequired
  - Returns
  - Response attributes
    - objectstring, value is "v2.core.account_link"
    - accountstring
    - createdtimestamp
    - expires_attimestamp

Creates an AccountLink object that includes a single-use URL that an account can use to access a Stripe-hosted flow for collecting or updating required information.

The ID of the Account to create link for.

The use case of the AccountLink.

String representing the object’s type. Objects of the same type share the same value of the object field.

The ID of the connected account this Account Link applies to.

The timestamp at which this Account Link was created.

The timestamp at which this Account Link will expire.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The URL at which the account can access the Stripe-hosted flow.

Hash containing usage options.

Accounts v2 is not enabled for your platform.

Account cannot be onboard via v2/core/account_links without specifying the right configurations.

The resource wasn’t found.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/account_links \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "account": "acct_1Nv0FGQ9RKHgCVdK",    "use_case": {        "type": "account_onboarding",        "account_onboarding": {            "configurations": [                "recipient"            ],            "return_url": "https://example.com/return",            "refresh_url": "https://example.com/reauth"        }    }  }'
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/account_links \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "account": "acct_1Nv0FGQ9RKHgCVdK",    "use_case": {        "type": "account_onboarding",        "account_onboarding": {            "configurations": [                "recipient"            ],            "return_url": "https://example.com/return",            "refresh_url": "https://example.com/reauth"        }    }  }'
```

Example 3 (unknown):
```unknown
{  "object": "v2.core.account_link",  "account": "acct_1Nv0FGQ9RKHgCVdK",  "created": "2025-03-27T17:15:18.000Z",  "expires_at": "2025-03-27T17:25:18.000Z",  "livemode": true,  "url": "https://accounts.stripe.com/r/acct_1Nv0FGQ9RKHgCVdK#alu_test_61SGhyomRuz7xsw5216SGhyj0ASQdCLwMKdRUF3mi3H6",  "use_case": {    "account_onboarding": {      "configurations": [        "recipient"      ],      "refresh_url": "https://example.com/reauth",      "return_url": "https://example.com/return"    },    "type": "account_onboarding"  }}
```

Example 4 (unknown):
```unknown
{  "object": "v2.core.account_link",  "account": "acct_1Nv0FGQ9RKHgCVdK",  "created": "2025-03-27T17:15:18.000Z",  "expires_at": "2025-03-27T17:25:18.000Z",  "livemode": true,  "url": "https://accounts.stripe.com/r/acct_1Nv0FGQ9RKHgCVdK#alu_test_61SGhyomRuz7xsw5216SGhyj0ASQdCLwMKdRUF3mi3H6",  "use_case": {    "account_onboarding": {      "configurations": [        "recipient"      ],      "refresh_url": "https://example.com/reauth",      "return_url": "https://example.com/return"    },    "type": "account_onboarding"  }}
```

---

## Update a PaymentIntent

**URL:** https://docs.stripe.com/api/payment_intents/update

**Contents:**
- Update a PaymentIntent
  - Parameters
    - amountinteger
    - currencyenum
    - customerstring
    - customer_accountstring
    - descriptionstring
    - metadataobject
    - payment_methodstring
    - receipt_emailstring

Updates properties on a PaymentIntent object without confirming.

Depending on which properties you update, you might need to confirm the PaymentIntent again. For example, updating the payment_method always requires you to confirm the PaymentIntent again. If you prefer to update and confirm at the same time, we recommend updating properties through the confirm API instead.

Amount intended to be collected by this PaymentIntent. A positive integer representing how much to charge in the smallest currency unit (e.g., 100 cents to charge $1.00 or 100 to charge ¥100, a zero-decimal currency). The minimum amount is $0.50 US or equivalent in charge currency. The amount value supports up to eight digits (e.g., a value of 99999999 for a USD charge of $999,999.99).

Three-letter ISO currency code, in lowercase. Must be a supported currency.

ID of the Customer this PaymentIntent belongs to, if one exists.

Payment methods attached to other Customers cannot be used with this PaymentIntent.

If setup_future_usage is set and this PaymentIntent’s payment method is not card_present, then the payment method attaches to the Customer after the PaymentIntent has been confirmed and any required actions from the user are complete. If the payment method is card_present and isn’t a digital wallet, then a generated_card payment method representing the card is created and attached to the Customer instead.

ID of the Account representing the customer that this PaymentIntent belongs to, if one exists.

Payment methods attached to other Accounts cannot be used with this PaymentIntent.

If setup_future_usage is set and this PaymentIntent’s payment method is not card_present, then the payment method attaches to the Account after the PaymentIntent has been confirmed and any required actions from the user are complete. If the payment method is card_present and isn’t a digital wallet, then a generated_card payment method representing the card is created and attached to the Account instead.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

ID of the payment method (a PaymentMethod, Card, or compatible Source object) to attach to this PaymentIntent. To unset this field to null, pass in an empty string.

Email address that the receipt for the resulting payment will be sent to. If receipt_email is specified for a payment in live mode, a receipt will be sent regardless of your email settings.

Indicates that you intend to make future payments with this PaymentIntent’s payment method.

If you provide a Customer with the PaymentIntent, you can use this parameter to attach the payment method to the Customer after the PaymentIntent is confirmed and the customer completes any required actions. If you don’t provide a Customer, you can still attach the payment method to a Customer after the transaction completes.

If the payment method is card_present and isn’t a digital wallet, Stripe creates and attaches a generated_card payment method representing the card to the Customer instead.

When processing card payments, Stripe uses setup_future_usage to help you comply with regional legislation and network rules, such as SCA.

If you’ve already set setup_future_usage and you’re performing a request using a publishable key, you can only update the value from on_session to off_session.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

Shipping information for this PaymentIntent.

Text that appears on the customer’s statement as the statement descriptor for a non-card charge. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

Setting this value for a card charge returns an error. For card charges, set the statement_descriptor_suffix instead.

Provides information about a card charge. Concatenated to the account’s statement descriptor prefix to form the complete statement descriptor that appears on the customer’s statement.

Returns a PaymentIntent object.

Retrieves the details of a PaymentIntent that has previously been created.

You can retrieve a PaymentIntent client-side using a publishable key when the client_secret is in the query string.

If you retrieve a PaymentIntent with a publishable key, it only returns a subset of properties. Refer to the payment intent object reference for more details.

The client secret of the PaymentIntent. We require it if you use a publishable key to retrieve the source.

Returns a PaymentIntent if a valid identifier was provided.

Lists all LineItems of a given PaymentIntent.

A dictionary with a data property that contains an array of up to limit line items of the given PaymentIntent, starting after line item starting_after. Each entry in the array is a separate line item object. If no other line items are available, the resulting array is empty.

Returns a list of PaymentIntents.

Only return PaymentIntents for the customer that this customer ID specifies.

Only return PaymentIntents for the account representing the customer that this ID specifies.

A dictionary with a data property that contains an array of up to limit PaymentIntents, starting after PaymentIntent starting_after. Each entry in the array is a separate PaymentIntent object. If no other PaymentIntents are available, the resulting array is empty.

You can cancel a PaymentIntent object when it’s in one of these statuses: requires_payment_method, requires_capture, requires_confirmation, requires_action or, in rare cases, processing.

After it’s canceled, no additional charges are made by the PaymentIntent and any operations on the PaymentIntent fail with an error. For PaymentIntents with a status of requires_capture, the remaining amount_capturable is automatically refunded.

You can’t cancel the PaymentIntent for a Checkout Session. Expire the Checkout Session instead.

Reason for canceling this PaymentIntent. Possible values are: duplicate, fraudulent, requested_by_customer, or abandoned

Returns a PaymentIntent object if the cancellation succeeds. Returns an error if the PaymentIntent is already canceled or isn’t in a cancelable state.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents/pi_3MtwBwLkdIwHu7ix28a3tqPa \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents/pi_3MtwBwLkdIwHu7ix28a3tqPa \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

Example 3 (unknown):
```unknown
{  "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",  "object": "payment_intent",  "amount": 2000,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 0,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": {    "enabled": true  },  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",  "confirmation_method": "automatic",  "created": 1680800504,  "currency": "usd",  "customer": null,  "description": null,  "last_payment_error": null,  "latest_charge": null,  "livemode": false,  "metadata": {    "order_id": "6735"  },  "next_action": null,  "on_behalf_of": null,  "payment_method": null,  "payment_method_options": {    "card": {      "installments": null,      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    },    "link": {      "persistent_token": null    }  },  "payment_method_types": [    "card",    "link"  ],  "processing": null,  "receipt_email": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "source": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "requires_payment_method",  "transfer_data": null,  "transfer_group": null}
```

Example 4 (unknown):
```unknown
{  "id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",  "object": "payment_intent",  "amount": 2000,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 0,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": {    "enabled": true  },  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH",  "confirmation_method": "automatic",  "created": 1680800504,  "currency": "usd",  "customer": null,  "description": null,  "last_payment_error": null,  "latest_charge": null,  "livemode": false,  "metadata": {    "order_id": "6735"  },  "next_action": null,  "on_behalf_of": null,  "payment_method": null,  "payment_method_options": {    "card": {      "installments": null,      "mandate_options": null,      "network": null,      "request_three_d_secure": "automatic"    },    "link": {      "persistent_token": null    }  },  "payment_method_types": [    "card",    "link"  ],  "processing": null,  "receipt_email": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "source": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "requires_payment_method",  "transfer_data": null,  "transfer_group": null}
```

---

## Metadata

**URL:** https://docs.stripe.com/api/metadata

**Contents:**
- Metadata
- Sample metadata use cases
- Pagination
  - Parameters
    - limitoptional, default is 10
    - starting_afteroptional object ID
    - ending_beforeoptional object ID
  - List Response Format
    - objectstring, value is "list"
    - dataarray

Updateable Stripe objects—including Account, Charge, Customer, PaymentIntent, Refund, Subscription, and Transfer have a metadata parameter. You can use this parameter to attach key-value data to these Stripe objects.

You can specify up to 50 keys, with key names up to 40 characters long and values up to 500 characters long. Keys and values are stored as strings and can contain any characters with one exception: you can’t use square brackets ([ and ]) in keys.

You can use metadata to store additional, structured information on an object. For example, you could store your user’s full name and corresponding unique identifier from your system on a Stripe Customer object. Stripe doesn’t use metadata—for example, we don’t use it to authorize or decline a charge and it won’t be seen by your users unless you choose to show it to them.

Some of the objects listed above also support a description parameter. You can use the description parameter to annotate a charge-for example, a human-readable description such as 2 shirts for test@example.com. Unlike metadata, description is a single string, which your users might see (for example, in email receipts Stripe sends on your behalf).

Don’t store any sensitive information (bank account numbers, card details, and so on) as metadata or in the description parameter.

All top-level API resources have support for bulk fetches through “list” API methods. For example, you can list charges, list customers, and list invoices. These list API methods share a common structure and accept, at a minimum, the following three parameters: limit, starting_after, and ending_before.

Stripe’s list API methods use cursor-based pagination through the starting_after and ending_before parameters. Both parameters accept an existing object ID value (see below) and return objects in reverse chronological order. The ending_before parameter returns objects listed before the named object. The starting_after parameter returns objects listed after the named object. These parameters are mutually exclusive. You can use either the starting_after or ending_before parameter, but not both simultaneously.

Our client libraries offer auto-pagination helpers to traverse all pages of a list.

This specifies a limit on the number of objects to return, ranging between 1 and 100.

A cursor to use in pagination. starting_after is an object ID that defines your place in the list. For example, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include starting_after=obj_foo to fetch the next page of the list.

A cursor to use in pagination. ending_before is an object ID that defines your place in the list. For example, if you make a list request and receive 100 objects, starting with obj_bar, your subsequent call can include ending_before=obj_bar to fetch the previous page of the list.

A string that provides a description of the object type that returns.

An array containing the actual response elements, paginated by any request parameters.

Whether or not there are more elements available after this set. If false, this set comprises the end of the list.

The URL for accessing this list.

APIs within the /v2 namespace contain a different pagination interface than the v1 namespace.

Some top-level API resource have support for retrieval via “search” API methods. For example, you can search charges, search customers, and search subscriptions.

Stripe’s search API methods utilize cursor-based pagination via the page request parameter and next_page response parameter. For example, if you make a search request and receive "next_page": "pagination_key" in the response, your subsequent call can include page=pagination_key to fetch the next page of results.

Our client libraries offer auto-pagination helpers to easily traverse all pages of a search result.

The search query string. See search query language.

A limit on the number of objects returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A string describing the object type returned.

The URL for accessing this list.

Whether or not there are more elements available after this set. If false, this set comprises the end of the list.

An array containing the actual response elements, paginated by any request parameters.

A cursor for use in pagination. If has_more is true, you can pass the value of next_page to a subsequent call to fetch the next page of results.

The total number of objects that match the query, only accurate up to 10,000. This field isn’t included by default. To include it in the response, expand the total_count field.

Our libraries support auto-pagination. This feature allows you to easily iterate through large lists of resources without having to manually perform the requests to fetch subsequent pages.

Each API request has an associated request identifier. You can find this value in the response headers, under Request-Id. You can also find request identifiers in the URLs of individual request logs in your Dashboard.

To expedite the resolution process, provide the request identifier when you contact us about a specific request.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/customers \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/customers \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "metadata[order_id]"=6735
```

Example 3 (unknown):
```unknown
{  "id": "cus_123456789",  "object": "customer",  "address": {    "city": "city",    "country": "US",    "line1": "line 1",    "line2": "line 2",    "postal_code": "90210",    "state": "CA"  },  "balance": 0,  "created": 1483565364,  "currency": null,  "default_source": null,  "delinquent": false,  "description": null,  "discount": null,  "email": null,  "invoice_prefix": "C11F7E1",  "invoice_settings": {    "custom_fields": null,    "default_payment_method": null,    "footer": null,    "rendering_options": null  },  "livemode": false,  "metadata": {    "order_id": "6735"  },  "name": null,  "next_invoice_sequence": 1,  "phone": null,  "preferred_locales": [],  "shipping": null,  "tax_exempt": "none"}
```

Example 4 (unknown):
```unknown
{  "id": "cus_123456789",  "object": "customer",  "address": {    "city": "city",    "country": "US",    "line1": "line 1",    "line2": "line 2",    "postal_code": "90210",    "state": "CA"  },  "balance": 0,  "created": 1483565364,  "currency": null,  "default_source": null,  "delinquent": false,  "description": null,  "discount": null,  "email": null,  "invoice_prefix": "C11F7E1",  "invoice_settings": {    "custom_fields": null,    "default_payment_method": null,    "footer": null,    "rendering_options": null  },  "livemode": false,  "metadata": {    "order_id": "6735"  },  "name": null,  "next_invoice_sequence": 1,  "phone": null,  "preferred_locales": [],  "shipping": null,  "tax_exempt": "none"}
```

---

## Include-dependent response values in API v2

**URL:** https://docs.stripe.com/api-includable-response-values

**Contents:**
- Include-dependent response values in API v2
- Learn how to manage API responses that return null by default for certain properties.
  - API v2 only
    - Endpoint dependency

The include parameter is a feature of API v2. Requests in API v1 don’t use it.

Some API v2 responses contain null values for certain properties by default, regardless of their actual values. That reduces the size of response payloads while maintaining the basic response structure. To retrieve the actual values for those properties, specify them in the include array request parameter.

To determine whether you need to use the include parameter in a given request, look at the request description. The include parameter’s enum values represent the response properties that depend on the include parameter.

Whether a response property defaults to null depends on the request endpoint, not the object that the endpoint references. If multiple endpoints return data from the same object, a particular property can depend on include in one endpoint and return its actual value by default for a different endpoint.

A hash property can depend on a single include value, or on multiple include values associated with its child properties. For example, when updating an Account, to return actual values for the entire identity hash, specify identity in the include parameter. Otherwise, the identity hash is null in the response. However, to return actual values for the configuration hash, you must specify individual configurations in the request. If you specify at least one configuration, but not all of them, specified configurations return actual values and unspecified configurations return null. If you don’t specify any configurations, the configuration hash is null in the response.

The following example updates an Account to add the customer and merchant configurations, but doesn’t specify any properties in the include parameter:

The response might look like this:

This example makes the same request, but specifies configuration.customer and identity in the include parameter:

The response includes details about the customer configuration and identity, but returns null for all other configurations:

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts/acct_123 \
  -H "Authorization: Bearer sk_test_YOUR_TEST_KEY_HERE" \
  -H "Stripe-Version: preview" \
  --json '{
    "configuration": {
        "customer": {
            "capabilities": {
                "automatic_indirect_tax": {
                    "requested": true
                }
            }
        },
        "merchant": {
            "capabilities": {
                "card_payments": {
                    "requested": true
                }
            }
        }
    }
  }'
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts/acct_123 \
  -H "Authorization: Bearer sk_test_YOUR_TEST_KEY_HERE" \
  -H "Stripe-Version: preview" \
  --json '{
    "configuration": {
        "customer": {
            "capabilities": {
                "automatic_indirect_tax": {
                    "requested": true
                }
            }
        },
        "merchant": {
            "capabilities": {
                "card_payments": {
                    "requested": true
                }
            }
        }
    }
  }'
```

Example 3 (unknown):
```unknown
{
  "id": "acct_123",
  "object": "v2.core.account",
  "applied_configurations": [
    "customer",
    "merchant"
  ],
  "configuration": null,
  "contact_email": "furever@example.com",
  "created": "2025-06-09T21:16:03.000Z",
  "dashboard": "full",
  "defaults": null,
  "display_name": "Furever",
  "identity": null,
  "livemode": true,
  "metadata": {},
  "requirements": null
}
```

Example 4 (unknown):
```unknown
{
  "id": "acct_123",
  "object": "v2.core.account",
  "applied_configurations": [
    "customer",
    "merchant"
  ],
  "configuration": null,
  "contact_email": "furever@example.com",
  "created": "2025-06-09T21:16:03.000Z",
  "dashboard": "full",
  "defaults": null,
  "display_name": "Furever",
  "identity": null,
  "livemode": true,
  "metadata": {},
  "requirements": null
}
```

---

## The Customer Session object

**URL:** https://docs.stripe.com/api/customer_sessions/object

**Contents:**
- The Customer Session object
  - Attributes
    - client_secretstring
    - componentsobject
    - customerstringExpandable
    - expires_attimestamp
  - More attributesExpand all
    - objectstring
    - createdtimestamp
    - customer_accountnullable string

The client secret of this Customer Session. Used on the client to set up secure access to the given customer.

The client secret can be used to provide access to customer from your frontend. It should not be stored, logged, or exposed to anyone other than the relevant customer. Make sure that you have TLS enabled on any page that includes the client secret.

This hash defines which component is enabled and the features it supports.

The Customer the Customer Session was created for.

The timestamp at which this Customer Session will expire.

Creates a Customer Session object that includes a single-use client secret that you can use on your front-end to grant client-side API access for certain customer resources.

Configuration for each component. At least 1 component must be enabled.

The ID of an existing customer for which to create the Customer Session.

Returns a Customer Session object.

**Examples:**

Example 1 (unknown):
```unknown
{  "object": "customer_session",  "client_secret": "_POpxYpmkXdtttYtZQYhrsOJZ2RCQ9kCqqXRU6qrP5c4Jgje",  "components": {    "buy_button": {      "enabled": false    },    "pricing_table": {      "enabled": true    }  },  "customer": "cus_PO34b57IOUb83c",  "expires_at": 1684790027,  "livemode": false}
```

Example 2 (unknown):
```unknown
{  "object": "customer_session",  "client_secret": "_POpxYpmkXdtttYtZQYhrsOJZ2RCQ9kCqqXRU6qrP5c4Jgje",  "components": {    "buy_button": {      "enabled": false    },    "pricing_table": {      "enabled": true    }  },  "customer": "cus_PO34b57IOUb83c",  "expires_at": 1684790027,  "livemode": false}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/customer_sessions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_PO34b57IOUb83c \  -d "components[pricing_table][enabled]"=true
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/customer_sessions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_PO34b57IOUb83c \  -d "components[pricing_table][enabled]"=true
```

---

## Stripe CLI keys and permissions

**URL:** https://docs.stripe.com/stripe-cli/keys

**Contents:**
- Stripe CLI keys and permissions
- Learn about default Stripe CLI keys and permissions.
- Restricted keys
  - View your keys
  - View your permissions
- Specify an API key

For more details, see the Stripe CLI reference.

By default, you can use your account’s secret keys to perform any API request without restriction. When you run the stripe login command to authenticate to the Stripe CLI, the CLI generates a set of restricted keys for your account (one for a sandbox, one in live mode) that are valid for 90 days.

Unlike an API secret key, a restricted key generated by the Stripe CLI has restrictions on the API requests that it can perform. You can create new restricted keys in the Dashboard with different restrictions, or specify any API key using the --api-key flag.

The CLI stores your keys in the Restricted keys section on the API keys page, and on your local machine in ~/.config/stripe/config.toml.

Use these steps to view the permissions associated with your restricted key:

Use the --api-key flag to specify your API secret key inline each time you send a request:

**Examples:**

Example 1 (unknown):
```unknown
stripe login --api-key sk_test_YOUR_TEST_KEY_HERE
```

Example 2 (unknown):
```unknown
stripe login --api-key sk_test_YOUR_TEST_KEY_HERE
```

---

## Provide receipts

**URL:** https://docs.stripe.com/terminal/features/receipts

**Contents:**
- Provide receipts
- Use Stripe to provide your customers with receipts that meet card network rules.
  - Receipts in a sandbox
- Prebuilt email receipts
  - SDK Reference
- Custom receipts
  - SDK Reference

Receipts for payments created using your test API keys are not sent automatically. Instead, you can view or manually send a receipt using the Dashboard.

Card network rules and local regulatory requirements are different for in-person payments. If you accept payments using Stripe Terminal, you must provide customers with the option to receive a physical or email receipt. Stripe provides everything you need to start offering receipts with your first transaction.

Receipts must contain certain fields to comply with card network rules. You can use Stripe’s prebuilt email receipts, or use receipt data from the Stripe API and your Terminal integration to generate on-brand custom receipts.

Prebuilt email receipts already include all card network-required fields. It’s the simplest way to set up compliant receipts.

If you have the customer’s email, use the receipt_email field when creating a PaymentIntent. When you provide a receipt_email, Stripe automatically emails a compliant receipt to the customer when capturing the PaymentIntent.

To trigger an automatic email receipt after the customer checks out, update the PaymentIntent’s receipt_email with the customer’s email.

For more information about automatic email receipts, see Email Receipts.

You can also customize receipts to include any design and content you want—as long as you list required information. When you accept in-person payments with EMV chip cards, card networks require you to include several fields on the receipts you provide to customers.

The Stripe API allows you to fetch necessary fields for compliance-ready receipts.

The following fields become available in the PaymentIntent object as soon as the payment is confirmed.

You can access these fields server-side using the Stripe API, or client-side using the Stripe Terminal SDKs. When using the JavaScript SDK, the PaymentIntent object matches the API object.

Whether you’re emailing or printing your custom receipts for Terminal payments, be sure to include the required fields to meet card network rules. If provided, you can also access the cardholder’s preferred language (based on the presented card’s settings), using the preferred_locales field on the Payment Method object.

---

## Capabilities

**URL:** https://docs.stripe.com/api/capabilities

**Contents:**
- Capabilities
- The Capability object
  - Attributes
    - idstring
    - accountstringExpandable
    - requestedboolean
    - requirementsobject
    - statusenum
  - More attributesExpand all
    - objectstring

This is an object representing a capability for a Stripe account.

Related guide: Account capabilities

The identifier for the capability.

The account for which the capability enables functionality.

Whether the capability has been requested.

Information about the requirements for the capability, including what information needs to be collected, and by when.

The status of the capability.

The capability is active.

The capability is inactive.

The capability is inactive with requirements pending verification.

The capability is unrequested.

Updates an existing Account Capability. Request or remove a capability by updating its requested parameter.

To request a new capability for an account, pass true. There can be a delay before the requested capability becomes active. If the capability has any activation requirements, the response includes them in the requirements arrays.

If a capability isn’t permanent, you can remove it from the account by passing false. Some capabilities are permanent after they’ve been requested. Attempting to remove a permanent capability returns an error.

Returns an Account Capability object.

Retrieves information about the specified Account Capability.

Returns an Account Capability object.

Returns a list of capabilities associated with the account. The capabilities are returned sorted by creation date, with the most recent capability appearing first.

A dictionary with a data property that contains an array of the capabilities of this account. Each entry in the array is a separate capability object.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "card_payments",  "object": "capability",  "account": "acct_1032D82eZvKYlo2C",  "future_requirements": {    "alternatives": [],    "current_deadline": null,    "currently_due": [],    "disabled_reason": null,    "errors": [],    "eventually_due": [],    "past_due": [],    "pending_verification": []  },  "requested": true,  "requested_at": 1688491010,  "requirements": {    "alternatives": [],    "current_deadline": null,    "currently_due": [],    "disabled_reason": null,    "errors": [],    "eventually_due": [],    "past_due": [],    "pending_verification": []  },  "status": "inactive"}
```

Example 2 (unknown):
```unknown
{  "id": "card_payments",  "object": "capability",  "account": "acct_1032D82eZvKYlo2C",  "future_requirements": {    "alternatives": [],    "current_deadline": null,    "currently_due": [],    "disabled_reason": null,    "errors": [],    "eventually_due": [],    "past_due": [],    "pending_verification": []  },  "requested": true,  "requested_at": 1688491010,  "requirements": {    "alternatives": [],    "current_deadline": null,    "currently_due": [],    "disabled_reason": null,    "errors": [],    "eventually_due": [],    "past_due": [],    "pending_verification": []  },  "status": "inactive"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/accounts/acct_1032D82eZvKYlo2C/capabilities/card_payments \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d requested=true
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/accounts/acct_1032D82eZvKYlo2C/capabilities/card_payments \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d requested=true
```

---

## Quote

**URL:** https://docs.stripe.com/api/quotes

**Contents:**
- Quote
- The Quote object
  - Attributes
    - idstring
    - line_itemsobjectExpandable
    - metadataobject
  - More attributesExpand all
    - objectstring
    - amount_subtotalinteger
    - amount_totalinteger

A Quote is a way to model prices that you’d like to provide to a customer. Once accepted, it will automatically create an invoice, subscription or subscription schedule.

Unique identifier for the object.

A list of items the customer is being quoted for.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

A quote models prices and services for a customer. Default options for header, description, footer, and expires_at can be set in the dashboard via the quote template.

A list of line items the customer is being quoted for. Each line item includes information about the product, the quantity, and the resulting cost.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the quote object.

A quote models prices and services for a customer.

A list of line items the customer is being quoted for. Each line item includes information about the product, the quantity, and the resulting cost.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the updated quote object.

When retrieving a quote, there is an includable line_items property containing the first handful of those items. There is also a URL where you can retrieve the full (paginated) list of line items.

A dictionary with a data property that contains an array of up to limit quote line items, starting after Line Item starting_after. Each entry in the array is a separate Line Item object. If no more line items are available, the resulting array will be empty.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "qt_1Mr7wVLkdIwHu7ixJYSiPTGq",  "object": "quote",  "amount_subtotal": 2198,  "amount_total": 2198,  "application": null,  "application_fee_amount": null,  "application_fee_percent": null,  "automatic_tax": {    "enabled": false,    "liability": null,    "status": null  },  "collection_method": "charge_automatically",  "computed": {    "recurring": null,    "upfront": {      "amount_subtotal": 2198,      "amount_total": 2198,      "total_details": {        "amount_discount": 0,        "amount_shipping": 0,        "amount_tax": 0      }    }  },  "created": 1680130691,  "currency": "usd",  "customer": "cus_NcMfB0SSFHINCV",  "default_tax_rates": [],  "description": null,  "discounts": [],  "expires_at": 1682722691,  "footer": null,  "from_quote": null,  "header": null,  "invoice": null,  "invoice_settings": {    "days_until_due": null,    "issuer": {      "type": "self"    }  },  "livemode": false,  "metadata": {},  "number": null,  "on_behalf_of": null,  "status": "draft",  "status_transitions": {    "accepted_at": null,    "canceled_at": null,    "finalized_at": null  },  "subscription": null,  "subscription_data": {    "description": null,    "effective_date": null,    "trial_period_days": null  },  "subscription_schedule": null,  "test_clock": null,  "total_details": {    "amount_discount": 0,    "amount_shipping": 0,    "amount_tax": 0  },  "transfer_data": null}
```

Example 2 (unknown):
```unknown
{  "id": "qt_1Mr7wVLkdIwHu7ixJYSiPTGq",  "object": "quote",  "amount_subtotal": 2198,  "amount_total": 2198,  "application": null,  "application_fee_amount": null,  "application_fee_percent": null,  "automatic_tax": {    "enabled": false,    "liability": null,    "status": null  },  "collection_method": "charge_automatically",  "computed": {    "recurring": null,    "upfront": {      "amount_subtotal": 2198,      "amount_total": 2198,      "total_details": {        "amount_discount": 0,        "amount_shipping": 0,        "amount_tax": 0      }    }  },  "created": 1680130691,  "currency": "usd",  "customer": "cus_NcMfB0SSFHINCV",  "default_tax_rates": [],  "description": null,  "discounts": [],  "expires_at": 1682722691,  "footer": null,  "from_quote": null,  "header": null,  "invoice": null,  "invoice_settings": {    "days_until_due": null,    "issuer": {      "type": "self"    }  },  "livemode": false,  "metadata": {},  "number": null,  "on_behalf_of": null,  "status": "draft",  "status_transitions": {    "accepted_at": null,    "canceled_at": null,    "finalized_at": null  },  "subscription": null,  "subscription_data": {    "description": null,    "effective_date": null,    "trial_period_days": null  },  "subscription_schedule": null,  "test_clock": null,  "total_details": {    "amount_discount": 0,    "amount_shipping": 0,    "amount_tax": 0  },  "transfer_data": null}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/quotes \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_NcMfB0SSFHINCV \  -d "line_items[0][price]"=price_1Mr7wULkdIwHu7ixhPkIEN2w \  -d "line_items[0][quantity]"=2
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/quotes \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_NcMfB0SSFHINCV \  -d "line_items[0][price]"=price_1Mr7wULkdIwHu7ixhPkIEN2w \  -d "line_items[0][quantity]"=2
```

---

## The File Link object

**URL:** https://docs.stripe.com/api/file_links/object

**Contents:**
- The File Link object
  - Attributes
    - idstring
    - expires_atnullable timestamp
    - filestringExpandable
    - metadataobject
    - urlnullable string
  - More attributesExpand all
    - objectstring
    - createdtimestamp

Unique identifier for the object.

Time that the link expires.

The file object this link points to.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The publicly accessible URL to download the file.

Creates a new file link object.

The ID of the file. The file’s purpose must be one of the following: business_icon, business_logo, customer_signature, dispute_evidence, finance_report_run, financial_account_statement, identity_document_downloadable, issuing_regulatory_reporting, pci_document, selfie, sigma_scheduled_query, tax_document_user_upload, terminal_android_apk, or terminal_reader_splashscreen.

The link isn’t usable after this future timestamp.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the file link object if successful and raises an error otherwise.

Updates an existing file link object. Expired links can no longer be updated.

A future timestamp after which the link will no longer be usable, or now to expire the link immediately.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the file link object if successful, and raises an error otherwise.

Retrieves the file link with the given ID.

If the identifier you provide is valid, a file link object returns. If not, Stripe raises an error.

Returns a list of file links.

A dictionary with a data property that contains an array of up to limit file links, starting after the starting_after file link. Each entry in the array is a separate file link object. If there aren’t additional available file links, the resulting array is empty.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "link_1Mr23jLkdIwHu7ix65betcoo",  "object": "file_link",  "created": 1680108075,  "expired": false,  "expires_at": null,  "file": "file_1Mr23iLkdIwHu7ixQkCV3CBR",  "livemode": false,  "metadata": {},  "url": "https://files.stripe.com/links/MDB8YWNjdF8xTTJKVGtMa2RJd0h1N2l4fGZsX3Rlc3RfaXVoY2hrUnJPMzlBR3dPb01XMmFkSTVq00yUPLFf3h"}
```

Example 2 (unknown):
```unknown
{  "id": "link_1Mr23jLkdIwHu7ix65betcoo",  "object": "file_link",  "created": 1680108075,  "expired": false,  "expires_at": null,  "file": "file_1Mr23iLkdIwHu7ixQkCV3CBR",  "livemode": false,  "metadata": {},  "url": "https://files.stripe.com/links/MDB8YWNjdF8xTTJKVGtMa2RJd0h1N2l4fGZsX3Rlc3RfaXVoY2hrUnJPMzlBR3dPb01XMmFkSTVq00yUPLFf3h"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/file_links \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d file=file_1Mr23iLkdIwHu7ixQkCV3CBR
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/file_links \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d file=file_1Mr23iLkdIwHu7ixQkCV3CBR
```

---

## React Stripe.js reference

**URL:** https://docs.stripe.com/sdks/stripejs-react

**Contents:**
- React Stripe.js reference
- Learn about React components for Stripe.js and Stripe Elements.
  - See the code
    - Note
- Before you begin
- Setup
- Checkout provider
- Element components
  - Available Element components
- useCheckout hook

Want to see how React Stripe.js works or help develop it? Check out the project on GitHub. You can also view the changelog on the Releases tab.

React Stripe.js is a thin wrapper around Stripe Elements. It allows you to add Elements to any React app.

The Stripe.js reference covers complete Elements customization details.

You can use Elements with any Stripe product to collect online payments. To find the right integration path for your business, explore our docs.

This reference covers the full React Stripe.js API. If you prefer to learn by doing, check out our documentation on accepting a payment or take a look at a sample integration.

This doc assumes that you already have a basic working knowledge of React and that you have already set up a React project. If you’re new to React, we recommend that you take a look at the Getting Started guide before continuing.

Install React Stripe.js and the Stripe.js loader from the npm public registry.

The CheckoutProvider allows you to use Element components and access the Stripe object in any nested component. Render a CheckoutProvider at the root of your React app so that it’s available everywhere you need it.

To use the CheckoutProvider, call loadStripe from @stripe/stripe-js with your publishable key. The loadStripe function asynchronously loads the Stripe.js script and initializes a Stripe object. Pass the returned Promise to the CheckoutProvider.

See Create a Checkout Session for an example of what your endpoint might look like.

required Stripe | null | Promise<Stripe | null>

A Stripe object or a Promise resolving to a Stripe object. We recommend using the Stripe.js wrapper module to initialize a Stripe object. After you set this prop, you can’t change it.

You can also pass in null or a Promise resolving to null if you’re performing an initial server-side render or when generating a static site.

CheckoutProvider configuration options. See available options. You must provide the clientSecret of the created Checkout Session. See Create a Checkout Session for an example.

Element components allow you to securely collect payment information in your React app and place the Elements wherever you want on your checkout page. You can also customize the appearance.

You can mount individual Element components inside of your CheckoutProvider tree. You can only mount one of each type of Element in a single <CheckoutProvider>.

An object containing Element configuration options. See available options for the Payment Element.

Triggered when the Element loses focus.

optional (event: Object) => void

Triggered when data exposed by this Element changes.

For more information, refer to the Stripe.js reference.

optional (event: Object) => void

Triggered when the escape key is pressed within an Element.

For more information, refer to the Stripe.js reference.

Triggered when the Element receives focus.

optional (event: Object) => void

Triggered when the Element fails to load.

For more information, refer to the Stripe.js reference.

optional (event: Object) => void

Triggered when the loader UI is mounted to the DOM and ready to be displayed.

You only receive these events from the payment and address Elements.

For more information, refer to the Stripe.js reference.

optional (element: Element) => void

Triggered when the Element is fully rendered and can accept imperative element.focus() calls. Called with a reference to the underlying Element instance.

You can use several different kinds of Elements for collecting information on your checkout page. These are the available Elements:

Use the useCheckout hook in your components to get the Checkout object, which contains data from the Checkout Session, and methods to update and confirm the Session.

We recognize that the use of iframes makes styling an Element more difficult, but they shift the burden of securely handling payment data to Stripe and allows you to keep your site compliant with industry regulations.

Each element is mounted in an iframe, which means that Elements probably won’t work with any existing styling and component frameworks that you have. Despite this, you can still configure Elements to match the design of your site. To customize Elements, you respond to events and configure Elements with the appearance option. The layout of each Element stays consistent, but you can modify colors, fonts, borders, padding, and so on.

Build an integration with React Stripe.js and Elements with the Checkout Sessions API.

**Examples:**

Example 1 (unknown):
```unknown
npm install --save @stripe/react-stripe-js @stripe/stripe-js
```

Example 2 (unknown):
```unknown
npm install --save @stripe/react-stripe-js @stripe/stripe-js
```

Example 3 (python):
```python
import {CheckoutProvider} from '@stripe/react-stripe-js/checkout';
import {loadStripe} from '@stripe/stripe-js';

// Make sure to call `loadStripe` outside of a component’s render to avoid
// recreating the `Stripe` object on every render.
const stripePromise = loadStripe('pk_test_TYooMQauvdEDq54NiTphI7jx');

export default function App() {
  const promise = useMemo(() => {
    return fetch('/create-checkout-session', {
      method: 'POST',
    })
      .then((res) => res.json())
      .then((data) => data.clientSecret);
  }, []);

  return (
    <CheckoutProvider stripe={stripePromise} options={{clientSecret: promise}}>
      <CheckoutForm />
    </CheckoutProvider>
  );
}
```

Example 4 (python):
```python
import {CheckoutProvider} from '@stripe/react-stripe-js/checkout';
import {loadStripe} from '@stripe/stripe-js';

// Make sure to call `loadStripe` outside of a component’s render to avoid
// recreating the `Stripe` object on every render.
const stripePromise = loadStripe('pk_test_TYooMQauvdEDq54NiTphI7jx');

export default function App() {
  const promise = useMemo(() => {
    return fetch('/create-checkout-session', {
      method: 'POST',
    })
      .then((res) => res.json())
      .then((data) => data.clientSecret);
  }, []);

  return (
    <CheckoutProvider stripe={stripePromise} options={{clientSecret: promise}}>
      <CheckoutForm />
    </CheckoutProvider>
  );
}
```

---

## Capture a PaymentIntent

**URL:** https://docs.stripe.com/api/payment_intents/capture

**Contents:**
- Capture a PaymentIntent
  - Parameters
    - amount_to_captureinteger
    - metadataobject
  - More parametersExpand all
    - amount_detailsobject
    - application_fee_amountintegerConnect only
    - final_captureboolean
    - hooksobject
    - payment_detailsobject

Capture the funds of an existing uncaptured PaymentIntent when its status is requires_capture.

Uncaptured PaymentIntents are cancelled a set number of days (7 by default) after their creation.

Learn more about separate authorization and capture.

The amount to capture from the PaymentIntent, which must be less than or equal to the original amount. Defaults to the full amount_capturable if it’s not provided.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a PaymentIntent object with status="succeeded" if the PaymentIntent is capturable. Returns an error if the PaymentIntent isn’t capturable or if an invalid amount to capture is provided.

Confirm that your customer intends to pay with current or provided payment method. Upon confirmation, the PaymentIntent will attempt to initiate a payment.

If the selected payment method requires additional authentication steps, the PaymentIntent will transition to the requires_action status and suggest additional actions via next_action. If payment fails, the PaymentIntent transitions to the requires_payment_method status or the canceled status if the confirmation limit is reached. If payment succeeds, the PaymentIntent will transition to the succeeded status (or requires_capture, if capture_method is set to manual).

If the confirmation_method is automatic, payment may be attempted using our client SDKs and the PaymentIntent’s client_secret. After next_actions are handled by the client, no additional confirmation is required to complete the payment.

If the confirmation_method is manual, all payment attempts must be initiated using a secret key.

If any actions are required for the payment, the PaymentIntent will return to the requires_confirmation state after those actions are completed. Your server needs to then explicitly re-confirm the PaymentIntent to initiate the next payment attempt.

There is a variable upper limit on how many times a PaymentIntent can be confirmed. After this limit is reached, any further calls to this endpoint will transition the PaymentIntent to the canceled state.

ID of the payment method (a PaymentMethod, Card, or compatible Source object) to attach to this PaymentIntent. If the payment method is attached to a Customer, it must match the customer that is set on this PaymentIntent.

Email address that the receipt for the resulting payment will be sent to. If receipt_email is specified for a payment in live mode, a receipt will be sent regardless of your email settings.

Indicates that you intend to make future payments with this PaymentIntent’s payment method.

If you provide a Customer with the PaymentIntent, you can use this parameter to attach the payment method to the Customer after the PaymentIntent is confirmed and the customer completes any required actions. If you don’t provide a Customer, you can still attach the payment method to a Customer after the transaction completes.

If the payment method is card_present and isn’t a digital wallet, Stripe creates and attaches a generated_card payment method representing the card to the Customer instead.

When processing card payments, Stripe uses setup_future_usage to help you comply with regional legislation and network rules, such as SCA.

If you’ve already set setup_future_usage and you’re performing a request using a publishable key, you can only update the value from on_session to off_session.

Use off_session if your customer may or may not be present in your checkout flow.

Use on_session if you intend to only reuse the payment method when your customer is present in your checkout flow.

Shipping information for this PaymentIntent.

Returns the resulting PaymentIntent after all possible transitions are applied.

Perform an incremental authorization on an eligible PaymentIntent. To be eligible, the PaymentIntent’s status must be requires_capture and incremental_authorization_supported must be true.

Incremental authorizations attempt to increase the authorized amount on your customer’s card to the new, higher amount provided. Similar to the initial authorization, incremental authorizations can be declined. A single PaymentIntent can call this endpoint multiple times to further increase the authorized amount.

If the incremental authorization succeeds, the PaymentIntent object returns with the updated amount. If the incremental authorization fails, a card_declined error returns, and no other fields on the PaymentIntent or Charge update. The PaymentIntent object remains capturable for the previously authorized amount.

Each PaymentIntent can have a maximum of 10 incremental authorization attempts, including declines. After it’s captured, a PaymentIntent can no longer be incremented.

Learn more about incremental authorizations.

The updated total amount that you intend to collect from the cardholder. This amount must be greater than the currently authorized amount.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Text that appears on the customer’s statement as the statement descriptor for a non-card or card charge. This value overrides the account’s default statement descriptor. For information about requirements, including the 22-character limit, see the Statement Descriptor docs.

Returns a PaymentIntent object with the updated amount if the incremental authorization succeeds. Returns an error if the incremental authorization failed or the PaymentIntent isn’t eligible for incremental authorizations.

Manually reconcile the remaining amount for a customer_balance PaymentIntent.

Amount that you intend to apply to this PaymentIntent from the customer’s cash balance. If the PaymentIntent was created by an Invoice, the full amount of the PaymentIntent is applied regardless of this parameter.

A positive integer representing how much to charge in the smallest currency unit (for example, 100 cents to charge 1 USD or 100 to charge 100 JPY, a zero-decimal currency). The maximum amount is the amount of the PaymentIntent.

When you omit the amount, it defaults to the remaining amount requested on the PaymentIntent.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

Returns a PaymentIntent object.

Search for PaymentIntents you’ve previously created using Stripe’s Search Query Language. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.

The search query string. See search query language and the list of supported query fields for payment intents.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A dictionary with a data property that contains an array of up to limit PaymentIntents. If no objects match the query, the resulting array will be empty. See the related guide on expanding properties in lists.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/payment_intents/pi_3MrPBM2eZvKYlo2C1TEMacFD/capture \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/payment_intents/pi_3MrPBM2eZvKYlo2C1TEMacFD/capture \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "pi_3MrPBM2eZvKYlo2C1TEMacFD",  "object": "payment_intent",  "amount": 1000,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 1000,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": null,  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_3MrPBM2eZvKYlo2C1TEMacFD_secret_9J35eTzWlxVmfbbQhmkNbewuL",  "confirmation_method": "automatic",  "created": 1524505326,  "currency": "usd",  "customer": null,  "description": "One blue fish",  "last_payment_error": null,  "latest_charge": "ch_1EXUPv2eZvKYlo2CStIqOmbY",  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": "pm_1EXUPv2eZvKYlo2CUkqZASBe",  "payment_method_options": {},  "payment_method_types": [    "card"  ],  "processing": null,  "receipt_email": null,  "redaction": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "succeeded",  "transfer_data": null,  "transfer_group": null}
```

Example 4 (unknown):
```unknown
{  "id": "pi_3MrPBM2eZvKYlo2C1TEMacFD",  "object": "payment_intent",  "amount": 1000,  "amount_capturable": 0,  "amount_details": {    "tip": {}  },  "amount_received": 1000,  "application": null,  "application_fee_amount": null,  "automatic_payment_methods": null,  "canceled_at": null,  "cancellation_reason": null,  "capture_method": "automatic",  "client_secret": "pi_3MrPBM2eZvKYlo2C1TEMacFD_secret_9J35eTzWlxVmfbbQhmkNbewuL",  "confirmation_method": "automatic",  "created": 1524505326,  "currency": "usd",  "customer": null,  "description": "One blue fish",  "last_payment_error": null,  "latest_charge": "ch_1EXUPv2eZvKYlo2CStIqOmbY",  "livemode": false,  "metadata": {},  "next_action": null,  "on_behalf_of": null,  "payment_method": "pm_1EXUPv2eZvKYlo2CUkqZASBe",  "payment_method_options": {},  "payment_method_types": [    "card"  ],  "processing": null,  "receipt_email": null,  "redaction": null,  "review": null,  "setup_future_usage": null,  "shipping": null,  "statement_descriptor": null,  "statement_descriptor_suffix": null,  "status": "succeeded",  "transfer_data": null,  "transfer_group": null}
```

---

## Delete a customer

**URL:** https://docs.stripe.com/api/customers/delete

**Contents:**
- Delete a customer
  - Parameters
  - Returns
- Search customers
  - Parameters
    - querystringRequired
    - limitinteger
    - pagestring
  - Returns

Permanently deletes a customer. It cannot be undone. Also immediately cancels any active subscriptions on the customer.

Returns an object with a deleted parameter on success. If the customer ID does not exist, this call raises an error.

Unlike other objects, deleted customers can still be retrieved through the API in order to be able to track their history. Deleting customers removes all credit card details and prevents any further operations to be performed (such as adding a new subscription).

Search for customers you’ve previously created using Stripe’s Search Query Language. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.

The search query string. See search query language and the list of supported query fields for customers.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A dictionary with a data property that contains an array of up to limit customers. If no objects match the query, the resulting array will be empty. See the related guide on expanding properties in lists.

**Examples:**

Example 1 (unknown):
```unknown
curl -X DELETE https://api.stripe.com/v1/customers/cus_NffrFeUfNV2Hib \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl -X DELETE https://api.stripe.com/v1/customers/cus_NffrFeUfNV2Hib \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "cus_NffrFeUfNV2Hib",  "object": "customer",  "deleted": true}
```

Example 4 (unknown):
```unknown
{  "id": "cus_NffrFeUfNV2Hib",  "object": "customer",  "deleted": true}
```

---

## Cash Balance

**URL:** https://docs.stripe.com/api/cash_balance

**Contents:**
- Cash Balance
- The Cash balance object
  - Attributes
    - objectstring
    - availablenullable object
    - customerstring
    - customer_accountnullable string
    - livemodeboolean
    - settingsobject
- Update a cash balance's settings

A customer’s Cash balance represents real funds. Customers can add funds to their cash balance by sending a bank transfer. These funds can be used for payment and can eventually be paid out to your bank account.

String representing the object’s type. Objects of the same type share the same value.

A hash of all cash balances available to this customer. You cannot delete a customer with any cash balances, even if the balance is 0. Amounts are represented in the smallest currency unit.

The ID of the customer whose cash balance this object represents.

The ID of an Account representing a customer whose cash balance this object represents.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

A hash of settings for this cash balance.

Changes the settings on a customer’s cash balance.

A hash of settings for this cash balance.

The customer’s cash balance, with the updated settings.

Retrieves a customer’s cash balance.

The Cash Balance object for a given customer.

**Examples:**

Example 1 (unknown):
```unknown
{  "object": "cash_balance",  "available": {    "eur": 10000  },  "customer": "cus_OaCLf8Fi1nbFpJ",  "livemode": false,  "settings": {    "reconciliation_mode": "automatic",    "using_merchant_default": true  }}
```

Example 2 (unknown):
```unknown
{  "object": "cash_balance",  "available": {    "eur": 10000  },  "customer": "cus_OaCLf8Fi1nbFpJ",  "livemode": false,  "settings": {    "reconciliation_mode": "automatic",    "using_merchant_default": true  }}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/customers/cus_Ob4Xiw8KXOqcvM/cash_balance \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "settings[reconciliation_mode]"=manual
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/customers/cus_Ob4Xiw8KXOqcvM/cash_balance \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "settings[reconciliation_mode]"=manual
```

---

## Create a CVC update token

**URL:** https://docs.stripe.com/api/tokens/create_cvc_update

**Contents:**
- Create a CVC update token
  - Parameters
    - cvc_updateobjectRequired
  - Returns
- Create a person token
  - Parameters
    - personobjectRequired
  - Returns
- Create a PII token
  - Parameters

Creates a single-use token that represents an updated CVC value that you can use for CVC re-collection. Use this token when you confirm a card payment or use a saved card on a PaymentIntent with confirmation_method: manual.

For most cases, use our JavaScript library instead of using the API. For a PaymentIntent with confirmation_method: automatic, use our recommended payments integration without tokenizing the CVC value.

The updated CVC value this token represents.

Returns the created CVC update token if it’s successful. Otherwise, this call raises an error.

Creates a single-use token that represents the details for a person. Use this when you create or update persons associated with a Connect account. Learn more about account tokens.

You can only create person tokens with your application’s publishable key and in live mode. You can use your application’s secret key to create person tokens only in test mode.

Information for the person this token represents.

Returns the created person token if it’s successful. Otherwise, this call raises an error.

Creates a single-use token that represents the details of personally identifiable information (PII). You can use this token in place of an id_number or id_number_secondary in Account or Person Update API methods. You can only use a PII token once.

The PII this token represents.

Returns the created PII token if it’s successful. Otherwise, this call raises an error.

Retrieves the token with the given ID.

Returns a token if you provide a valid ID. Raises an error otherwise.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/tokens \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "cvc_update[cvc]"=123
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/tokens \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "cvc_update[cvc]"=123
```

Example 3 (unknown):
```unknown
{  "id": "cvctok_1NkWsu2eZvKYlo2CFDm6ab7X",  "object": "token",  "client_ip": null,  "created": 1693334608,  "livemode": false,  "redaction": null,  "type": "cvc_update",  "used": false}
```

Example 4 (unknown):
```unknown
{  "id": "cvctok_1NkWsu2eZvKYlo2CFDm6ab7X",  "object": "token",  "client_ip": null,  "created": 1693334608,  "livemode": false,  "redaction": null,  "type": "cvc_update",  "used": false}
```

---

## Best practices for managing secret API keys

**URL:** https://docs.stripe.com/keys-best-practices

**Contents:**
- Best practices for managing secret API keys
- Learn how to manage secret API keys and handle key leaks.
- Protect against compromised secret API keys
- Customize API access with restricted API keys
- Limit the IP addresses that can send API requests
- Handle compromised secret API keys
- See also

Secret API keys are a form of account credentials, like a username and password. In contrast to publishable keys, which are safe to include in webpages and apps, you must limit secret API keys to your server environment and protect them from exposure. If a bad actor obtains your secret key, they can use it to harm your business and other parties in the Stripe ecosystem.

You must keep your secret API keys safe. Follow these best practices, including using Stripe-offered security features.

Take the following actions to prevent key leaks and secure your keys in place:

You can create restricted API keys to grant limited access to the Stripe API. Sharing restricted keys is safer than sharing your secret key.

With restricted keys, you can limit the potential impact of a compromise. For example, if you want to give a Stripe API key to a third party that monitors disputes, you can create a restricted key that grants read-only access to dispute-related resources in your Stripe account and blocks everything else. If the third party were compromised, a bad actor who stole your key would be limited to just those API calls.

You can increase the security of a secret or restricted key by limiting the IP addresses that can use it to send API requests. We recommended this if your service has stable egress IP ranges and a change management process for updating the allowlist when those egress ranges change.

For instructions about how to restrict a key to one or more IP addresses, see how to limit secret or restricted keys to a list or range of IP addresses.

If you identify a compromised secret API key, such as an accidental publication to GitHub, immediately rotate the key in the Stripe Dashboard and replace the old key in your integration. If you detect abnormal behaviors without confirming that the API key is compromised, we recommended that you rotate the API keys proactively while investigating the root cause in parallel.

If Stripe detects an exposed secret API key, we notify you immediately and request that you rotate the key. You must act promptly to reduce potential damages and financial losses caused by unauthorized use of the compromised key until you deactivate it. In some cases, we might deactivate the key proactively. In this case, we notify you about any actions we take.

Stripe doesn’t guarantee that we detect all compromised keys. You’re responsible for following these best practices to prevent compromised keys and making sure your integration with Stripe is secure.

---
