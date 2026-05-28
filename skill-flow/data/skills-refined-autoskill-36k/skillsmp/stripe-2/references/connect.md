# Stripe - Connect

**Pages:** 55

---

## List persons v2

**URL:** https://docs.stripe.com/api/v2/core/accounts/list-persons

**Contents:**
- List persons v2
  - Parameters
    - account_idstringRequired
    - limitinteger
    - pagestring
  - Returns
  - Response attributes
    - dataarray of objects
    - next_page_urlnullable string
    - previous_page_urlnullable string

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

Delete a Person associated with an Account.

The Account the Person is associated with.

The ID of the Person to delete.

String representing the object’s type. Objects of the same type share the same value.

Always true for a deleted object.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

The resource wasn’t found.

This is a list of all public thin events we currently send for updates to Person, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/persons \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/persons \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 3 (unknown):
```unknown
{  "data": [    {      "id": "person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",      "object": "v2.core.account_person",      "account": "acct_1Nv0FGQ9RKHgCVdK",      "additional_addresses": [],      "additional_names": [],      "address": {        "city": "Brothers",        "country": "us",        "line1": "27 Fredrick Ave",        "postal_code": "97712",        "state": "OR"      },      "created": "2024-11-26T17:10:07.000Z",      "date_of_birth": {        "day": 28,        "month": 1,        "year": 2000      },      "email": "jenny.rosen@example.com",      "given_name": "Jenny",      "id_numbers": [        {          "type": "us_ssn_last_4"        }      ],      "livemode": true,      "metadata": {},      "nationalities": [],      "relationship": {        "owner": true,        "percent_ownership": "0.8",        "representative": true,        "title": "CEO"      },      "surname": "Rosen",      "updated": "2024-11-26T17:12:55.000Z"    }  ]}
```

Example 4 (unknown):
```unknown
{  "data": [    {      "id": "person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",      "object": "v2.core.account_person",      "account": "acct_1Nv0FGQ9RKHgCVdK",      "additional_addresses": [],      "additional_names": [],      "address": {        "city": "Brothers",        "country": "us",        "line1": "27 Fredrick Ave",        "postal_code": "97712",        "state": "OR"      },      "created": "2024-11-26T17:10:07.000Z",      "date_of_birth": {        "day": 28,        "month": 1,        "year": 2000      },      "email": "jenny.rosen@example.com",      "given_name": "Jenny",      "id_numbers": [        {          "type": "us_ssn_last_4"        }      ],      "livemode": true,      "metadata": {},      "nationalities": [],      "relationship": {        "owner": true,        "percent_ownership": "0.8",        "representative": true,        "title": "CEO"      },      "surname": "Rosen",      "updated": "2024-11-26T17:12:55.000Z"    }  ]}
```

---

## Create an event destination v2

**URL:** https://docs.stripe.com/api/v2/core/event_destinations/create

**Contents:**
- Create an event destination v2
  - Parameters
    - enabled_eventsarray of stringsRequired
    - event_payloadenumRequired
    - namestringRequired
    - typeenumRequired
    - amazon_eventbridgeobject
    - descriptionstring
    - events_fromarray of enums
    - includearray of enums

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

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/event_destinations \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "name": "My Event Destination",    "description": "This is my event destination, I like it a lot",    "enabled_events": [        "v1.billing.meter.error_report_triggered"    ],    "type": "webhook_endpoint",    "webhook_endpoint": {        "url": "https://example.com/my/webhook/endpoint"    },    "event_payload": "thin",    "include": [        "webhook_endpoint.url"    ]  }'
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/event_destinations \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "name": "My Event Destination",    "description": "This is my event destination, I like it a lot",    "enabled_events": [        "v1.billing.meter.error_report_triggered"    ],    "type": "webhook_endpoint",    "webhook_endpoint": {        "url": "https://example.com/my/webhook/endpoint"    },    "event_payload": "thin",    "include": [        "webhook_endpoint.url"    ]  }'
```

Example 3 (unknown):
```unknown
{  "id": "ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6",  "object": "v2.core.event_destination",  "created": "2024-10-22T16:20:09.931Z",  "description": "This is my event destination, I like it a lot",  "enabled_events": [    "v1.billing.meter.error_report_triggered"  ],  "event_payload": "thin",  "events_from": [    "self"  ],  "livemode": false,  "metadata": {},  "name": "My Event Destination",  "snapshot_api_version": null,  "status": "enabled",  "status_details": null,  "type": "webhook_endpoint",  "updated": "2024-10-22T16:20:09.937Z",  "webhook_endpoint": {    "signing_secret": null,    "url": "https://example.com/my/webhook/endpoint"  }}
```

Example 4 (unknown):
```unknown
{  "id": "ed_test_61RM8ltWcTW4mbsxf16RJyfa2xSQLHJJh1sxm7H0KVT6",  "object": "v2.core.event_destination",  "created": "2024-10-22T16:20:09.931Z",  "description": "This is my event destination, I like it a lot",  "enabled_events": [    "v1.billing.meter.error_report_triggered"  ],  "event_payload": "thin",  "events_from": [    "self"  ],  "livemode": false,  "metadata": {},  "name": "My Event Destination",  "snapshot_api_version": null,  "status": "enabled",  "status_details": null,  "type": "webhook_endpoint",  "updated": "2024-10-22T16:20:09.937Z",  "webhook_endpoint": {    "signing_secret": null,    "url": "https://example.com/my/webhook/endpoint"  }}
```

---

## Making API calls for connected accounts

**URL:** https://docs.stripe.com/connect/authentication

**Contents:**
- Making API calls for connected accounts
- Learn how to add the right information to your API calls so you can make calls for your connected accounts.
- Add the Stripe-Account header server-side
- Add the connected account ID to a client-side application
- Use Connect embedded components
- See also

You can make API calls for your connected accounts:

To help with performance and reliability, Stripe has established rate limits and allocations for API endpoints.

To make server-side API calls for connected accounts, use the Stripe-Account header with the account identifier, which begins with the prefix acct_. Here are four examples using your platform’s API secret key and the connected account’s Account identifier:

The Stripe-Account header approach is implied in any API request that includes the Stripe account ID in the URL. Here’s an example that shows how to Retrieve an account with your user’s Account identifier in the URL.

All of Stripe’s server-side libraries support this approach on a per-request basis:

Client-side libraries set the connected account ID as an argument to the client application:

The JavaScript code for passing the connected account ID client-side is the same for plain JS and for ESNext.

Instead of directly integrating with Stripe’s APIs, you can use Connect embedded components to provide Stripe functionality to your connected accounts in your platform’s UI. These components require less code to implement and handle all API calls internally.

For example, to show payments data to your connected accounts, embed the Payments component in your platform’s UI. This eliminates the need to make separate calls to the Charges, Payment Intents, Refunds, and Disputes API.

For a complete list of the available embedded components, see Supported components.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -H "Stripe-Account: {{CONNECTED_ACCOUNT_ID}}" \
  -d amount=1000 \
  -d currency=usd
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -H "Stripe-Account: {{CONNECTED_ACCOUNT_ID}}" \
  -d amount=1000 \
  -d currency=usd
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/accounts/{{CONNECTED_ACCOUNT_ID}} \
  -u "sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/accounts/{{CONNECTED_ACCOUNT_ID}} \
  -u "sk_test_YOUR_TEST_KEY_HERE:"
```

---

## Transfers

**URL:** https://docs.stripe.com/api/transfers

**Contents:**
- Transfers
- The Transfer object
  - Attributes
    - idstring
    - amountinteger
    - currencyenum
    - descriptionnullable string
    - destinationnullable stringExpandable
    - metadataobject
  - More attributesExpand all

A Transfer object is created when you move funds between Stripe accounts as part of Connect.

Before April 6, 2017, transfers also represented movement of funds from a Stripe account to a card or bank account. This behavior has since been split out into a Payout object, with corresponding payout endpoints. For more information, read about the transfer/payout split.

Related guide: Creating separate charges and transfers

Unique identifier for the object.

Amount in cents to be transferred.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

An arbitrary string attached to the object. Often useful for displaying to users.

ID of the Stripe account the transfer was sent to.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

To send funds from your Stripe account to a connected account, you create a new transfer object. Your Stripe balance must be able to cover the transfer amount, or you’ll receive an “Insufficient Funds” error.

Three-letter ISO code for currency in lowercase. Must be a supported currency.

The ID of a connected Stripe account. See the Connect documentation for details.

A positive integer in cents representing how much to transfer.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a transfer object if there were no initial errors with the transfer creation (e.g., insufficient funds).

Updates the specified transfer by setting the values of the parameters passed. Any parameters not provided will be left unchanged.

This request accepts only metadata as an argument.

An arbitrary string attached to the object. Often useful for displaying to users.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the transfer object if the update succeeded. This call will raise an error if update parameters are invalid.

Retrieves the details of an existing transfer. Supply the unique transfer ID from either a transfer creation request or the transfer list, and Stripe will return the corresponding transfer information.

Returns a transfer object if a valid identifier was provided, and raises an error otherwise.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "tr_1MiN3gLkdIwHu7ixNCZvFdgA",  "object": "transfer",  "amount": 400,  "amount_reversed": 0,  "balance_transaction": "txn_1MiN3gLkdIwHu7ixxapQrznl",  "created": 1678043844,  "currency": "usd",  "description": null,  "destination": "acct_1MTfjCQ9PRzxEwkZ",  "destination_payment": "py_1MiN3gQ9PRzxEwkZWTPGNq9o",  "livemode": false,  "metadata": {},  "reversals": {    "object": "list",    "data": [],    "has_more": false,    "total_count": 0,    "url": "/v1/transfers/tr_1MiN3gLkdIwHu7ixNCZvFdgA/reversals"  },  "reversed": false,  "source_transaction": null,  "source_type": "card",  "transfer_group": "ORDER_95"}
```

Example 2 (unknown):
```unknown
{  "id": "tr_1MiN3gLkdIwHu7ixNCZvFdgA",  "object": "transfer",  "amount": 400,  "amount_reversed": 0,  "balance_transaction": "txn_1MiN3gLkdIwHu7ixxapQrznl",  "created": 1678043844,  "currency": "usd",  "description": null,  "destination": "acct_1MTfjCQ9PRzxEwkZ",  "destination_payment": "py_1MiN3gQ9PRzxEwkZWTPGNq9o",  "livemode": false,  "metadata": {},  "reversals": {    "object": "list",    "data": [],    "has_more": false,    "total_count": 0,    "url": "/v1/transfers/tr_1MiN3gLkdIwHu7ixNCZvFdgA/reversals"  },  "reversed": false,  "source_transaction": null,  "source_type": "card",  "transfer_group": "ORDER_95"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/transfers \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=400 \  -d currency=usd \  -d destination=acct_1MTfjCQ9PRzxEwkZ \  -d transfer_group=ORDER_95
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/transfers \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=400 \  -d currency=usd \  -d destination=acct_1MTfjCQ9PRzxEwkZ \  -d transfer_group=ORDER_95
```

---

## The EventDestination object

**URL:** https://docs.stripe.com/api/v2/core/event_destinations/object

**Contents:**
- The EventDestination object
  - Attributes
    - idstring
    - objectstring, value is "v2.core.event_destination"
    - amazon_eventbridgenullable object
    - createdtimestamp
    - descriptionstring
    - enabled_eventsarray of strings
    - event_payloadenum
    - events_fromnullable array of enums

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

Lists all event destinations.

Additional fields to include in the response. Currently supports webhook_endpoint.url.

Include parameter to expose webhook_endpoint.url.

List of event destinations.

The previous page url.

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

## Use Terminal with Connect

**URL:** https://docs.stripe.com/terminal/features/connect

**Contents:**
- Use Terminal with Connect
- Integrate Stripe Terminal with your Connect platform.
    - Note
- Connected accounts own readers
  - Create locations and readers Server-side
  - Create connection tokens Server-side
    - Note
  - Create PaymentIntents Client-side Server-side
    - Client-side
    - Server-side

Stripe Terminal is compatible with Connect, allowing your platform and connected accounts to accept in-person payments.

Integrate Terminal with Connect according to how your platform processes payments for your connected accounts.

In all cases, use locations to group readers applicably.

Terminal connected accounts must have the card_payments capability to perform transactions.

With this integration, all API resources belong to the connected account rather than your platform. The connected account is responsible for the cost of Stripe fees, refunds, and chargebacks.

In the Dashboard, you can view your Terminal data by logging in as the connected account.

Create Locations and Readers for connected accounts by including the Stripe-Account header in the API requests.

When using Connect OAuth authentication, you must authorize the connected account separately for live mode and sandboxes using each mode’s respective application Client ID.

When creating a ConnectionToken for the Terminal SDK, set the Stripe-Account header to the connected account accepting payments. You can also provide a location parameter to control access to readers. If you provide a location, only readers assigned to that location can use the ConnectionToken. If you don’t provide a location, all readers can use the ConnectionToken.

If you’re using a server-driven integration, you don’t need to create a connection token.

With the iOS, Android, and React Native SDKs, you can create a PaymentIntent on the client or server. The JavaScript SDK only supports server-side creation.

When creating a PaymentIntent client-side for direct charges, don’t specify any additional parameters for the PaymentIntent. Instead, create a ConnectionToken with the Stripe-Account header for the connected account accepting payments. The client SDKs create the PaymentIntent on the same connected account the ConnectionToken belongs to. For more information, see Create PaymentIntents client-side.

The JavaScript SDK requires you to create the PaymentIntent on your server. For the other client SDKs, you might want to create the PaymentIntent on your server if the information required to start a payment isn’t readily available in your app. For more information, see Create PaymentIntents Server-side.

When creating a PaymentIntent server-side for direct charges, set the Stripe-Account header to the connected account.

Then follow the steps to collect a payment to process the PaymentIntent.

Contact us if you’re interested in letting the platform own and manage readers with direct charges. This private preview feature is currently available for smart readers using a server-driven integration. This integration works only with connected accounts that you control through a single platform.

With this integration, your platform owns device resources like Locations and Readers, and your connected accounts own payment resources like PaymentIntents. This allows your platform to manage a single reader that processes payments for multiple connected accounts. The connected accounts are responsible for the cost of Stripe fees, refunds, and chargebacks.

In the Dashboard, you can view your Terminal device management data directly when logged into your platform account. You can view payment data by logging in as the connected account.

The best way to group Reader objects by connected account is by assigning them to Locations. On your platform account, create a Location for a connected account using a display name that identifies the account.

Before you can connect your application to a smart reader, you must register the reader to your platform account.

When creating a PaymentIntent for direct charges, set the Stripe-Account header to the connected account.

The platform can only process PaymentIntents later if you create them for connected accounts that you control through a single platform.

The platform can process the connected account’s PaymentIntent with the platform-owned reader.

The PaymentIntent can only be processed if you create it using the Stripe-Account header.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/locations \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -H "Stripe-Account: {{CONNECTED_ACCOUNT_ID}}" \
  -d display_name=HQ \
  -d "address[line1]"="1272 Valencia Street" \
  -d "address[city]"="San Francisco" \
  -d "address[state]"=CA \
  -d "address[country]"=US \
  -d "address[postal_code]"=94110
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/locations \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -H "Stripe-Account: {{CONNECTED_ACCOUNT_ID}}" \
  -d display_name=HQ \
  -d "address[line1]"="1272 Valencia Street" \
  -d "address[city]"="San Francisco" \
  -d "address[state]"=CA \
  -d "address[country]"=US \
  -d "address[postal_code]"=94110
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/readers \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -H "Stripe-Account: {{CONNECTED_ACCOUNT_ID}}" \
  -d registration_code={{READER_REGISTRATION_CODE}} \
  --data-urlencode label="Alice's reader" \
  -d location="{{LOCATION_ID}}"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/terminal/readers \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -H "Stripe-Account: {{CONNECTED_ACCOUNT_ID}}" \
  -d registration_code={{READER_REGISTRATION_CODE}} \
  --data-urlencode label="Alice's reader" \
  -d location="{{LOCATION_ID}}"
```

---

## Get started with Connect embedded components

**URL:** https://docs.stripe.com/connect/get-started-connect-embedded-components

**Contents:**
- Get started with Connect embedded components
- Learn how to embed dashboard functionality into your website.
- Initialize Connect.jsClient-sideServer-side
  - Create an AccountSession Server
  - Create Account Session API
  - Set up Connect.js Client
  - Load and initialize Connect.js Client
- Configure Connect.jsClient-side
  - Customize the look of Connect embedded components
    - Necessary popups

Use Connect embedded components to add connected account dashboard functionality to your website. These libraries and their supporting API allow you to grant your users access to Stripe products directly in your dashboard and mobile applications.

For an immersive version of this guide, see the Connect embedded components integration quickstart. You can also download a sample integration from there. To customize the appearance of Connect embedded components, use the appearance options when you initialize StripeConnectInstance. See the full list of appearance parameters.

Stripe uses an AccountSession to express your intent to delegate API access to your connected account.

The AccountSessions API returns a client secret that allows an embedded component to access a connected account’s resources as if you were making the API calls for them.

In a single page application, your client initiates a request to obtain the account session to your server. You can create a new endpoint on your server that returns the client secret to the browser:

The Create Account Session API determines component and feature access for Connect embedded components. Stripe enforces these parameters for any components that correspond to the account session. If your site supports multiple user roles, make sure components and features that are enabled for that account session correspond to the current user’s role. For example, you can enable refund management only for administrators of your site, but not for other users. To make sure user role access are enforced, you must map your site’s user role to account session components.

We recommend setting up Connect.js with npm as shown in the following example, but it’s also possible without npm.

Install the npm package to use Connect.js as a module.

Call loadConnectAndInitialize with your publishable key and a function that retrieves a client secret by calling the new endpoint you created on your server. Use the returned StripeConnectInstance to create embedded components. After initializing Connect.js, you can mount components to or unmount components from the DOM at any time. That includes any elements rendered inside React or Vue portals.

To create a component, call create on the StripeConnectInstance that you created above, then pass in the component name. This returns a custom element that Connect.js registers and uses to automatically wire your DOM up to Stripe. You can then append this element to your DOM.

Call create with payments, then add the result to your DOM to render a payments UI.

See a complete list of supported embedded components →

The loadConnectAndInitialize method on the client takes several different options to configure Connect.js.

The embedded components Figma UI toolkit contains every component, common patterns, and an example application. You can use it to visualize and design embedded UIs on your website.

We offer a set of options to customize the look and feel of Connect embedded components. These customizations affect buttons, icons, and other accents in our design system.

Some behavior in embedded components, such as user authentication, must be presented in a popup. You can’t customize the embedded component to eliminate such popups.

You can set these options when initializing StripeConnectInstance by passing an Appearance to the appearance object. You can only use the Connect.js options to modify styles in Connect embedded components. The font family and background color of Connect embedded components are inherited from the parent HTML container. You must explicitly set all other options.

See the full list of appearance variables.

The fonts object in stripeConnect.initialize takes an array of CssFontSource or CustomFontSource objects.

If you use custom fonts on your page (for example, .woff or .tff files), you must specify the font files when initializing Connect embedded components. Doing so allows Connect embedded components to properly render the fonts. You can specify the files as:

Use this object to pass a stylesheet URL that defines your custom fonts when creating a StripeConnectInstance. With a CssFontSource object, your CSP configuration must allow fetching the domains associated with the CSS file URLs specified as CssFontSource.

Use this object to pass custom fonts when creating a StripeConnectInstance.

The update method supports updating Connect embedded components after initialization. You can use it to switch appearance options at runtime (without refreshing the page). To do so, use the same stripeConnectInstance object you created with initialize and call the update method on it:

Not all options (for example, fonts) are updatable. The supported options for this method are a subset of the options offered in initialize. This supports updating the appearance and locale.

Connect embedded components behave like regular block HTML elements. By default, they take 100% of the width of their parent HTML element, and grow in height according to the content rendered inside. You can control the width of Connect embedded components by specifying the width of the HTML parent. You can’t directly control the height as that depends on the rendered content, however, you can limit the height with maxHeight and overflow: scroll, the same way you can with other HTML block elements.

We offer a set of APIs to manage account sessions and user credentials in Connect embedded components.

On long running sessions, the session from the initially provided client secret might expire. When it expires, we automatically use fetchClientSecret to retrieve a new client secret and refresh the session. You don’t need to pass in any additional parameters.

We recommend that you call logout on the stripeConnectInstance to destroy the associated account session object after a user logs out of your app. This disables all Connect embedded components that link to that stripeConnectInstance.

Only call logout when your user logs out of your app. Don’t call logout when a component unmounts (when navigating to another page or closing the page) or when loading other components as this method entirely invalidates the current account session and stripe user session. After calling logout, components no longer render for the associated stripeConnectInstance.

If your website implements a Content Security Policy, you need to update the policy by adding the following rules:

If you’re using a CSS file to load web fonts for use with Connect embedded components, its URL must be allowed by your connect-src CSP directive.

Setting certain HTTP response headers enables the full functionality of Connect embedded components:

We support the same set of browsers that the Stripe Dashboard currently supports:

Connect embedded components are only supported in web browsers and can’t be used in embedded web views inside mobile or desktop applications. To use Connect embedded components in a mobile application, use the iOS or Android SDK.

If an embedded component isn’t supported yet by our mobile SDKs, we recommend linking to a web browser where you can render the embedded components.

When initializing Connect.js, you can pass a locale parameter. To match an embedded component’s locale to your website’s locale, pass the locale parameter with the locale of the UI your website renders.

The default value of the locale parameter is determined by the browser configured locale. If the specified locale isn’t directly supported, a reasonable alternative is used (for example fr-be might fall back to fr-fr).

Connect embedded components support the following locales:

If a component fails to load, you can react to the failure by providing a load error handler to any embedded component. Depending on the cause of failure, the load error handler can be called multiple times. Any logic triggered by a load error handler must be idempotent.

Every time there’s a load failure, an error object is passed to the load error handler with the following properties.

When a component fails to load, we detect the type of failure and map it to one of the types below. If the load error type can’t be determined it is marked as an api_error.

In most cases, embedded components render an error message when they fail to load, so you don’t need to. You can use a load error handler for analytics or for other elements of your site that a load error might affect.

However, embedded components don’t render any message for errors that occur prior to invoking the onLoaderStart callback, because that means they haven’t rendered any UI at all. In that case, your code should render the error UI.

After a component is created, no UI is displayed to users until the javascript for the component is loaded and parsed in the browser. This can cause components to appear to pop-in after they complete loading. To avoid this, display your own loading UI before the component is created and hide the UI after the component is displayed. All embedded components can accept a callback function that is called immediately when any UI (including loading indicators) is displayed to the user.

We recommend integrating with our javascript and React component wrappers, which simplify the loading of Connect embedded components and provide TypeScript definitions for our supported interfaces. If your build system currently doesn’t support taking a dependency on packages, you can integrate without these packages.

Manually add the Connect.js script tag to the <head> of each page on your site.

After Connect.js completes loading, it initializes the global window variable StripeConnect and calls StripeConnect.onLoad, if defined. You can safely initialize Connect.js by setting up an onload function and calling StripeConnect.init with the same Connect.js options as loadConnectAndInitialize. You can use the Connect instance returned by init in the same way you use the instance returned by loadConnectAndInitialize to create embedded components in an HTML + JS integration.

Connect embedded components typically don’t require user authentication. In some scenarios, Connect embedded components require the connected account to sign in with their Stripe account before accessing the component to provide the necessary functionality (for example, writing information to the account legal entity in the case of the account onboarding component). Other components might require authentication within the component after they initially render.

Authentication is required for connected accounts where Stripe is responsible for collecting updated information when requirements change. For connected accounts where you’re responsible for collecting updated information when requirements are due or change, such as Custom accounts, Stripe authentication is controlled by the disable_stripe_user_authentication Account Session feature. We recommend implementing 2FA or equivalent security measures as a best practice. For account configurations that support this feature, like Custom, you assume liability for connected accounts if they can’t pay back negative balances.

Authentication includes a popup to a Stripe-owned window. The connected account must authenticate before they can continue their workflow.

The following components require connected accounts to authenticate in certain scenarios:

To make sure the load time of Connect embedded components is as low as possible, follow these recommendations:

**Examples:**

Example 1 (javascript):
```javascript
require 'sinatra'
require 'stripe'
# This is a placeholder - it should be replaced with your secret API key.
# Sign in to see your own test API key embedded in code samples.
# Don’t submit any personally identifiable information in requests made with this key.
Stripe.api_key = 'sk_test_YOUR_TEST_KEY_HERE'

post '/account_session' do
  content_type 'application/json'

  # Create an AccountSession
  begin
    account_session = Stripe::AccountSession.create({
      account: '{{CONNECTED_ACCOUNT_ID}}',
      components: {
        payments: {
          enabled: true,
          features: {
            refund_management: true,
            dispute_management: true,
            capture_payments: true
          }
        }
      }
    })

    {
      client_secret: account_session[:client_secret]
    }.to_json
  rescue => error
    puts "An error occurred when calling the Stripe API to create an account session: #{error.message}";
    return [500, { error: error.message }.to_json]
  end
end
```

Example 2 (javascript):
```javascript
require 'sinatra'
require 'stripe'
# This is a placeholder - it should be replaced with your secret API key.
# Sign in to see your own test API key embedded in code samples.
# Don’t submit any personally identifiable information in requests made with this key.
Stripe.api_key = 'sk_test_YOUR_TEST_KEY_HERE'

post '/account_session' do
  content_type 'application/json'

  # Create an AccountSession
  begin
    account_session = Stripe::AccountSession.create({
      account: '{{CONNECTED_ACCOUNT_ID}}',
      components: {
        payments: {
          enabled: true,
          features: {
            refund_management: true,
            dispute_management: true,
            capture_payments: true
          }
        }
      }
    })

    {
      client_secret: account_session[:client_secret]
    }.to_json
  rescue => error
    puts "An error occurred when calling the Stripe API to create an account session: #{error.message}";
    return [500, { error: error.message }.to_json]
  end
end
```

Example 3 (unknown):
```unknown
npm install --save @stripe/connect-js
```

Example 4 (unknown):
```unknown
npm install --save @stripe/connect-js
```

---

## Retrieve a person v2

**URL:** https://docs.stripe.com/api/v2/core/accounts/retrieve-person

**Contents:**
- Retrieve a person v2
  - Parameters
    - account_idstringRequired
    - idstringRequired
  - Returns
  - Response attributes
    - idstring
    - objectstring, value is "v2.core.account_person"
    - accountstring
    - additional_addressesnullable array of objects

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

Delete a Person associated with an Account.

The Account the Person is associated with.

The ID of the Person to delete.

String representing the object’s type. Objects of the same type share the same value.

Always true for a deleted object.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

The resource wasn’t found.

This is a list of all public thin events we currently send for updates to Person, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/persons/person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/persons/person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 3 (unknown):
```unknown
{  "id": "person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_person",  "account": "acct_1Nv0FGQ9RKHgCVdK",  "additional_addresses": [],  "additional_names": [],  "address": {    "city": "Brothers",    "country": "us",    "line1": "27 Fredrick Ave",    "postal_code": "97712",    "state": "OR"  },  "created": "2024-11-26T17:10:07.000Z",  "date_of_birth": {    "day": 28,    "month": 1,    "year": 2000  },  "email": "jenny.rosen@example.com",  "given_name": "Jenny",  "id_numbers": [    {      "type": "us_ssn_last_4"    }  ],  "livemode": true,  "metadata": {},  "nationalities": [],  "relationship": {    "owner": true,    "percent_ownership": "0.8",    "representative": true,    "title": "CEO"  },  "surname": "Rosen",  "updated": "2024-11-26T17:12:55.000Z"}
```

Example 4 (unknown):
```unknown
{  "id": "person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_person",  "account": "acct_1Nv0FGQ9RKHgCVdK",  "additional_addresses": [],  "additional_names": [],  "address": {    "city": "Brothers",    "country": "us",    "line1": "27 Fredrick Ave",    "postal_code": "97712",    "state": "OR"  },  "created": "2024-11-26T17:10:07.000Z",  "date_of_birth": {    "day": 28,    "month": 1,    "year": 2000  },  "email": "jenny.rosen@example.com",  "given_name": "Jenny",  "id_numbers": [    {      "type": "us_ssn_last_4"    }  ],  "livemode": true,  "metadata": {},  "nationalities": [],  "relationship": {    "owner": true,    "percent_ownership": "0.8",    "representative": true,    "title": "CEO"  },  "surname": "Rosen",  "updated": "2024-11-26T17:12:55.000Z"}
```

---

## The Account object

**URL:** https://docs.stripe.com/api/v2/core/accounts/object

**Contents:**
- The Account object
  - Attributes
    - idstring
    - objectstring, value is "v2.core.account"
    - applied_configurationsarray of enums
    - closednullable boolean
    - configurationnullable object
    - contact_emailnullable string
    - createdtimestamp
    - dashboardnullable enum

Unique identifier for the Account.

String representing the object’s type. Objects of the same type share the same value of the object field.

The configurations that have been applied to this account.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Indicates whether the account has been closed.

An Account represents a company, individual, or other entity that a user interacts with. Accounts store identity information and one or more configurations that enable product-specific capabilities. You can assign configurations at creation or add them later.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values for settings shared across Account configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the future requirements for the Account that will eventually come into effect, including what information needs to be collected, and by when.

Information about the company, individual, and business represented by the Account.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the active requirements for the Account, including what information needs to be collected, and by when.

An Account is a representation of a company, individual or other entity that a user interacts with. Accounts contain identifying information about the entity, and configurations that store the features an account has access to. An account can be configured as any or all of the following configurations: Customer, Merchant and/or Recipient.

The account token generated by the account token api.

An Account Configuration which allows the Account to take on a key persona across Stripe products.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values to be used on Account Configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the company, individual, and business represented by the Account.

Additional fields to include in the response.

Include parameter to expose configuration.customer on an Account.

Include parameter to expose configuration.merchant on an Account.

Include parameter to expose configuration.recipient on an Account.

Include parameter to expose defaults on an Account.

Include parameter to expose future_requirements on an Account.

Include parameter to expose identity on an Account.

Include parameter to expose requirements on an Account.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Unique identifier for the Account.

String representing the object’s type. Objects of the same type share the same value of the object field.

The configurations that have been applied to this account.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Indicates whether the account has been closed.

An Account represents a company, individual, or other entity that a user interacts with. Accounts store identity information and one or more configurations that enable product-specific capabilities. You can assign configurations at creation or add them later.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values for settings shared across Account configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the future requirements for the Account that will eventually come into effect, including what information needs to be collected, and by when.

Information about the company, individual, and business represented by the Account.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the active requirements for the Account, including what information needs to be collected, and by when.

Requested capability is not available.

If dashboard is express, fees_collector must be application and losses_collector must be application.

If losses_collector is application, fees_collector must also be application.

Connect integration combination is not supported when UA beta is enabled.

Connect integration combination is not supported when UA beta is disabled.

Responsibility combinations is not supported in private preview.

Currency is not allowed for the account’s country.

Platform must be activated to create connected accounts.

Account creation is invalid.

Account creation error - liability unacknowledged.

Account creation error - requirement collection and liability unacknowledged.

Account creation error - requirement collection unacknowledged.

Terms of service must be accepted before adding merchant configuration.

Account token required for platforms in mandated countries (e.g., France).

Accounts v2 is not enabled for your platform.

Invalid characters are provided for address fields.

Address country doesn’t match identity country.

Address postal code is invalid.

Address state is invalid.

Address town is invalid.

Creating accounts with the BGN currency is no longer supported, as Bulgaria is now using the Euro as of 2026-01-01.

Dormant accounts cannot create accounts where requirements collector is application (this is an account takeover prevention measure).

Platform is in an invalid state and cannot create connected accounts.

Platform is in a rejected state and cannot create connected accounts.

Feature cannot be unrequested due to being a requirement for another feature.

Feature cannot be requested for the dashboard type.

Requested feature is not available for the entity type in your country.

Requested capability is not available in your country.

Feature cannot be requested given the platform’s country.

Requested feature is not available without also requesting a different feature.

Requested feature is not available without also requesting a different feature in your country.

Cannot create an account with an invalid configuration.

Platform is not verified and cannot create connected accounts.

Platform has not completed platform questionnaire and cannot create connected accounts.

Cross-border connected account creation is not allowed for this platform/account country combination.

Custom accounts cannot be created in certain countries.

Representative date of birth does not meet the age limit.

Representative date of birth is provided an invalid date or a future date.

Cannot change defaults.currency post account activation.

Default payment method provided for a customer does not exist or is otherwise invalid.

Specified payment method exists but its type is not allowed to be the default payment method.

Directorship declaration is not allowed during account creation.

Provided file tokens for documents are invalid, not found, deleted, or belong to a different account.

Provided file tokens for documents are of the wrong purpose.

Email contains unsupported domain.

Incorrect email is provided.

The identity.entity_type value is not supported in a given identity.country.

NONE is combined with another value in the HighRiskActivities list.

Provided ID number is of the wrong format for the given type.

The identity.country value is required but not provided.

Incorrect ID number is provided for a country.

The incorrect token type is provided .

ID number is provided that is not permitted for the Identity’s entity type and business structure.

The identity.business_details.id_numbers.registrar value is an invalid DE registrar.

Konbini Payments Support Hours is Invalid.

Konbini Payments Support Phone Number is Invalid.

Invoice rendering template does not exist or is otherwise invalid.

Invalid IP address is provided.

MCC is invalid for configuration.merchant.mcc.

Kana Kanji script addresses must have JP country.

Ownership declaration is not allowed during account creation.

Parameter cannot be passed alongside account_token.

Error returned when relationship.owner is set to true but the ownership percentage is set to 0%.

Phone number is invalid.

Platform has not signed up for Connect and cannot create connected accounts.

Postal code is required for Japanese addresses.

PurposeOfFundsDescription is not empty while PurposeOfFunds is not OTHER.

Provided script characters are invalid for the script.

Shipping address is required within the shipping hash.

Shipping name is required within the shipping hash.

Statement descriptor is invalid.

The business_details.structure value is not valid for identity.country and identity.entity_type.

Cannot set a test clock on a livemode customer.

Test clock does not exist or is otherwise invalid.

Cannot modify a test clock that is currently advancing.

Cannot add customer to a test clock that has already reached its customer limit.

The token is re-used with a different idempotency key.

TOS cannot be accepted on behalf of accounts when requirement collection is stripe.

Cannot set responsibilities on the current configurations.

Cannot set identity fields when the Account is only configured as a customer.

Address is in an unsupported postal code.

Address is in an unsupported state.

A v1 token ID is passed in v2 APIs.

Invalid account token.

An idempotent retry occurred with different request parameters.

Updates the details of an Account.

The ID of the Account to update.

The account token generated by the account token api.

An Account Configuration which allows the Account to take on a key persona across Stripe products.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values to be used on Account Configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the company, individual, and business represented by the Account.

Additional fields to include in the response.

Include parameter to expose configuration.customer on an Account.

Include parameter to expose configuration.merchant on an Account.

Include parameter to expose configuration.recipient on an Account.

Include parameter to expose defaults on an Account.

Include parameter to expose future_requirements on an Account.

Include parameter to expose identity on an Account.

Include parameter to expose requirements on an Account.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Unique identifier for the Account.

String representing the object’s type. Objects of the same type share the same value of the object field.

The configurations that have been applied to this account.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Indicates whether the account has been closed.

An Account represents a company, individual, or other entity that a user interacts with. Accounts store identity information and one or more configurations that enable product-specific capabilities. You can assign configurations at creation or add them later.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values for settings shared across Account configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the future requirements for the Account that will eventually come into effect, including what information needs to be collected, and by when.

Information about the company, individual, and business represented by the Account.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the active requirements for the Account, including what information needs to be collected, and by when.

Requested capability is not available.

If dashboard is express, fees_collector must be application and losses_collector must be application.

If losses_collector is application, fees_collector must also be application.

Connect integration combination is not supported when UA beta is disabled.

Responsibility combinations is not supported in private preview.

Currency is not allowed for the account’s country.

Account is not yet compatible with V2 APIs.

Terms of service must be accepted before adding merchant configuration.

Account token required for platforms in mandated countries (e.g., France).

Accounts v2 is not enabled for your platform.

Invalid characters are provided for address fields.

Address country doesn’t match identity country.

Address postal code is invalid.

Address state is invalid.

Address town is invalid.

Default payment method is added to the customer config before attaching it to the account using /v1/payment_methods.

Creating accounts with the BGN currency is no longer supported, as Bulgaria is now using the Euro as of 2026-01-01.

Dormant accounts cannot create accounts where requirements collector is application (this is an account takeover prevention measure).

Cannot set automatic_indirect_tax.validate_location when initially creating a customer configuration.

Feature cannot be unrequested due to being a requirement for another feature.

Feature cannot be requested for the dashboard type.

Requested feature is not available for the entity type in your country.

Requested capability is not available in your country.

Feature cannot be requested given the platform’s country.

Requested feature is not available without also requesting a different feature.

Requested feature is not available without also requesting a different feature in your country.

Configuration cannot be deactivated.

Configuration cannot be deactivated due to a dependency with another capability.

Cannot deactivate a configuration due to another configuration depending on it.

Configuration cannot be updated while deactivated.

Cannot create an account with an invalid configuration.

Cross-border connected account creation is not allowed for this platform/account country combination.

Custom accounts cannot be created in certain countries.

Invalid customer tax location.

Representative date of birth does not meet the age limit.

Representative date of birth is provided an invalid date or a future date.

Cannot change defaults.currency post account activation.

Outbound Destination ID is invalid.

Default payment method provided for a customer does not exist or is otherwise invalid.

Provided file tokens for documents are invalid, not found, deleted, or belong to a different account.

Provided file tokens for documents are of the wrong purpose.

Duplicate person is added to an account.

Email contains unsupported domain.

Incorrect email is provided.

The identity.entity_type value is not supported in a given identity.country.

NONE is combined with another value in the HighRiskActivities list.

Provided ID number is of the wrong format for the given type.

The identity.country value is required but not provided.

Identity param has been made immutable due to the state of the account.

Incorrect ID number is provided for a country.

The incorrect token type is provided .

ID number is provided that is not permitted for the Identity’s entity type and business structure.

The identity.business_details.id_numbers.registrar value is an invalid DE registrar.

Konbini Payments Support Hours is Invalid.

Konbini Payments Support Phone Number is Invalid.

Invalid IP address is provided.

MCC is invalid for configuration.merchant.mcc.

Kana Kanji script addresses must have JP country.

Parameter cannot be passed alongside account_token.

Error returned when relationship.owner is set to true but the ownership percentage is set to 0%.

Phone number is invalid.

Postal code is required for Japanese addresses.

PurposeOfFundsDescription is not empty while PurposeOfFunds is not OTHER.

Provided script characters are invalid for the script.

Shipping address is required within the shipping hash.

Shipping name is required within the shipping hash.

Statement descriptor is invalid.

The business_details.structure value is not valid for identity.country and identity.entity_type.

Cannot set a test clock on a livemode customer.

Test clock does not exist or is otherwise invalid.

The token is re-used with a different idempotency key.

TOS cannot be accepted on behalf of accounts when requirement collection is stripe.

Total ownership percentages of all Persons on the account exceeds 100%.

Cannot set responsibilities on the current configurations.

Cannot set identity fields when the Account is only configured as a customer.

Address is in an unsupported postal code.

Address is in an unsupported state.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

A v1 token ID is passed in v2 APIs.

Invalid account token.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

Retrieves the details of an Account.

The ID of the Account to retrieve.

Additional fields to include in the response.

Include parameter to expose configuration.customer on an Account.

Include parameter to expose configuration.merchant on an Account.

Include parameter to expose configuration.recipient on an Account.

Include parameter to expose defaults on an Account.

Include parameter to expose future_requirements on an Account.

Include parameter to expose identity on an Account.

Include parameter to expose requirements on an Account.

Unique identifier for the Account.

String representing the object’s type. Objects of the same type share the same value of the object field.

The configurations that have been applied to this account.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Indicates whether the account has been closed.

An Account represents a company, individual, or other entity that a user interacts with. Accounts store identity information and one or more configurations that enable product-specific capabilities. You can assign configurations at creation or add them later.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values for settings shared across Account configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the future requirements for the Account that will eventually come into effect, including what information needs to be collected, and by when.

Information about the company, individual, and business represented by the Account.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the active requirements for the Account, including what information needs to be collected, and by when.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

The resource wasn’t found.

Returns a list of Accounts.

Filter only accounts that have all of the configurations specified. If omitted, returns all accounts regardless of which configurations they have.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Filter by whether the account is closed. If omitted, returns only Accounts that are not closed.

The upper limit on the number of accounts returned by the List Account request.

The page token to navigate to next or previous batch of accounts given by the list request.

A list of retrieved Account objects.

URL with page token to navigate to next batch of accounts given by the list request.

URL with page token to navigate to previous batch of accounts given by the list request.

Accounts v2 is not enabled for your platform.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "acct_1Nv0FGQ9RKHgCVdK",  "object": "v2.core.account",  "applied_configurations": [    "customer",    "merchant"  ],  "configuration": {    "customer": {      "automatic_indirect_tax": {        "exempt": "none",        "location": {          "country": "US",          "state": "NY"        },        "location_source": "identity_address"      },      "billing": {        "invoice": {          "next_sequence": 1,          "prefix": "5626C87C",          "custom_fields": []        }      },      "capabilities": {        "automatic_indirect_tax": {          "status": "active",          "status_details": []        }      }    },    "merchant": {      "card_payments": {        "decline_on": {          "avs_failure": false,          "cvc_failure": false        }      },      "capabilities": {        "card_payments": {          "status": "active",          "status_details": []        },        "stripe_balance": {          "payouts": {            "status": "active",            "status_details": []          }        }      }    }  },  "contact_email": "furever@example.com",  "created": "2025-03-28T19:59:16.000Z",  "dashboard": "full",  "identity": {    "business_details": {      "registered_name": "Furever",      "address": {        "country": "US",        "postal_code": "10001"      }    },    "country": "US",    "entity_type": "company"  },  "defaults": {    "currency": "usd",    "responsibilities": {      "fees_collector": "stripe",      "losses_collector": "stripe",      "requirements_collector": "stripe"    }  },  "display_name": "Furever"}
```

Example 2 (unknown):
```unknown
{  "id": "acct_1Nv0FGQ9RKHgCVdK",  "object": "v2.core.account",  "applied_configurations": [    "customer",    "merchant"  ],  "configuration": {    "customer": {      "automatic_indirect_tax": {        "exempt": "none",        "location": {          "country": "US",          "state": "NY"        },        "location_source": "identity_address"      },      "billing": {        "invoice": {          "next_sequence": 1,          "prefix": "5626C87C",          "custom_fields": []        }      },      "capabilities": {        "automatic_indirect_tax": {          "status": "active",          "status_details": []        }      }    },    "merchant": {      "card_payments": {        "decline_on": {          "avs_failure": false,          "cvc_failure": false        }      },      "capabilities": {        "card_payments": {          "status": "active",          "status_details": []        },        "stripe_balance": {          "payouts": {            "status": "active",            "status_details": []          }        }      }    }  },  "contact_email": "furever@example.com",  "created": "2025-03-28T19:59:16.000Z",  "dashboard": "full",  "identity": {    "business_details": {      "registered_name": "Furever",      "address": {        "country": "US",        "postal_code": "10001"      }    },    "country": "US",    "entity_type": "company"  },  "defaults": {    "currency": "usd",    "responsibilities": {      "fees_collector": "stripe",      "losses_collector": "stripe",      "requirements_collector": "stripe"    }  },  "display_name": "Furever"}
```

Example 3 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "contact_email": "furever@example.com",    "display_name": "Furever",    "identity": {        "country": "us",        "entity_type": "company",        "business_details": {            "registered_name": "Furever"        }    },    "configuration": {        "customer": {            "capabilities": {                "automatic_indirect_tax": {                    "requested": true                }            }        },        "merchant": {            "capabilities": {                "card_payments": {                    "requested": true                }            }        }    },    "defaults": {        "responsibilities": {            "fees_collector": "stripe",            "losses_collector": "stripe"        }    },    "dashboard": "full",    "include": [        "configuration.merchant",        "configuration.customer",        "identity",        "defaults"    ]  }'
```

Example 4 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "contact_email": "furever@example.com",    "display_name": "Furever",    "identity": {        "country": "us",        "entity_type": "company",        "business_details": {            "registered_name": "Furever"        }    },    "configuration": {        "customer": {            "capabilities": {                "automatic_indirect_tax": {                    "requested": true                }            }        },        "merchant": {            "capabilities": {                "card_payments": {                    "requested": true                }            }        }    },    "defaults": {        "responsibilities": {            "fees_collector": "stripe",            "losses_collector": "stripe"        }    },    "dashboard": "full",    "include": [        "configuration.merchant",        "configuration.customer",        "identity",        "defaults"    ]  }'
```

---

## Handle verification with tokens

**URL:** https://docs.stripe.com/connect/account-tokens

**Contents:**
- Handle verification with tokens
- Connect platforms can use Stripe.js, the API, or mobile client libraries to securely collect account details from their users.
  - Applicable connected accounts
    - Regional considerationsFrance
- Create and use tokens
- Create an HTML form
  - Collect account and person details
  - Present the Stripe Connected Account Agreement
    - Note
- Add JavaScript

Before we can enable charges and payouts for connected accounts, you must fulfill Know Your Customer (KYC) requirements. To do so, provide identity verification information about your accounts to Stripe, which we then verify. You can perform this task with Account Tokens and Person Tokens. Tokens ensure that personally identifiable information (PII) doesn’t touch your servers, so your integration can operate securely. These tokens also allow Stripe to more accurately detect potential fraud.

You can only use tokens for:

You can’t use tokens for any other account information, including:

You create tokens using Stripe.js, the API, or one of the mobile client libraries. The process is effectively the same as tokenizing payment details or external accounts. Your connected account’s information is sent directly to Stripe and exchanged for a token that you can use in create and update API calls.

French platforms must use account tokens, which are an alternative to the agent model for platform PSD2 compliance. The key benefit of tokens for French platforms is that information is transferred from the user directly to Stripe. Not having to store PII data is still a benefit, but not necessarily a requirement. For platforms in other countries, account tokens are optional but recommended.

Tokens require both client-side and server-side code:

The following example shows how to use account tokens and person tokens. Both types are required when providing legal entity and person details for companies. If you onboard only individuals, you don’t need person tokens. Instead, create account tokens and pass the individual hash on the Account object to provide the required information.

The first step is to create an HTML form that collects the required information for the account and the person. This includes acceptance of the Stripe Connected Account Agreement.

Create form elements to collect the required information, such as name, address, and anything else required by the user’s country.

As the platform, you must make clear to your users that processing of payments is provided subject to the Stripe Connected Account Agreement. Indicating acceptance of the Stripe Connected Account Agreement is a requirement for using an account token to create a new connected account.

Only platforms that can accept the service agreement through the API can create Account Tokens that specify tos_shown_and_accepted.

We recommend you include language like the following, including links to both our agreement and your terms of service.

Next, the page needs JavaScript that:

For simplicity, data validation and error handling are omitted in the following code, but remember to add both to your actual integration.

Provide two arguments to the stripe.createToken() method:

The JavaScript object provided as the second argument needs to parallel the structure of the Account or Person object you’re tokenizing. Account tokens need either a top-level company or individual property, and person tokens need a top-level person property. Follow the object’s structure through all the required attributes. For example, line1 within address in the code block below is provided as person.address.line1.

To represent the user’s acceptance of the Stripe Connected Account Agreement, provide a top-level tos_shown_and_accepted property with a value of true (only account tokens are used for this).

You must still use tokens (to create or update a person) using server-side code. You can send the token ID to your server using whatever approach makes sense for your application (for example, an XHR request). For simplicity, this code example stores the token ID in a hidden form input and then submits the form.

Upon successfully receiving the tokens from Stripe, the JavaScript stores the token IDs in a hidden form input and then submits the form (to your server). The final steps are for your server-side code to use the tokens to create an account and a person.

Use the account token ID to create the account. The country and business type are provided outside the token.

When creating an account token, setting tos_shown_and_accepted to true automatically populates the date, ip, and user_agent attributes of the Account object’s tos_acceptance attribute. If you create an account without using an account token, you must provide values for those attributes.

Make sure to note the account ID that’s returned so that you can use it to create Person objects for the account.

Create a person by providing the ID of the person token as the value for the person_token parameter (you also need the account ID the person is for). You can use the requirements hash on the Account object to determine what information needs to be collected and from which persons.

You can also create an account token with our Android or iOS SDKs (mobile only supports account tokens). This is sufficient for creating an individual account, but you must use Stripe.js to create the person token that you need for a company account.

When a connected account needs to provide Stripe with a scan of an identity document such as a passport, you can use an account token. However, the JavaScript is more complicated because the file must be sent to Stripe as part of an XHR request. In this flow, the JavaScript:

To begin, add a file element to the form. The uploaded file needs to be a color image (smaller than 8,000 pixels by 8,000 pixels), in JPG, PNG, or PDF format, and less than 10MB in size.

Next, in your JavaScript that handles the form’s submission, send the uploaded file to Stripe. This needs to happen before creating the account token.

Finally, include the returned file ID as the verification.document.front value in the generic object provided to the createToken() call:

You can use tokens to update an existing account’s legal entity and person information. Create the tokens you need using the same combination of HTML and JavaScript as above, and then perform an update account or update person call providing the new token ID.

You must create and provide a new token when updating legal entity details previously set using an account token.

You can retrieve legal entity and person details after the fact using a retrieve account or retrieve person call.

When using tokens for updates:

For example, if an account is created with a token containing only a name and date of birth, you’d create a subsequent token containing only the address information, and then perform an update account call to add the address details to the account.

To clear any legal entity or person details or to explicitly set a value as null, pass an empty string in an update account or update person call. Use an update call, not a token, even if you originally used a token. You can assign empty strings only to optional attributes (for example, the second line of an address). You can’t assign them to any required attributes.

**Examples:**

Example 1 (unknown):
```unknown
<form class="my-form" action="/create-person" method="post">
  <input type="hidden" name="token-account" id="token-account">
  <input type="hidden" name="token-person" id="token-person">
  <label>
    <span>Business Name</span>
    <input class="inp-company-name">
  </label>
  <fieldset>
    <legend>Business Address</legend>
    <label>
      <span>Street Address Line 1</span>
```

Example 2 (unknown):
```unknown
<form class="my-form" action="/create-person" method="post">
  <input type="hidden" name="token-account" id="token-account">
  <input type="hidden" name="token-person" id="token-person">
  <label>
    <span>Business Name</span>
    <input class="inp-company-name">
  </label>
  <fieldset>
    <legend>Business Address</legend>
    <label>
      <span>Street Address Line 1</span>
```

Example 3 (unknown):
```unknown
<p>By clicking, you agree to <a href="#">our terms</a> and the <a href="https://stripe.com/connect-account/legal">Stripe Connected Account Agreement</a>.</p>
```

Example 4 (unknown):
```unknown
<p>By clicking, you agree to <a href="#">our terms</a> and the <a href="https://stripe.com/connect-account/legal">Stripe Connected Account Agreement</a>.</p>
```

---

## Retrieve an account v2

**URL:** https://docs.stripe.com/api/v2/core/accounts/retrieve

**Contents:**
- Retrieve an account v2
  - Parameters
    - idstringRequired
    - includearray of enums
  - Returns
  - Response attributes
    - idstring
    - objectstring, value is "v2.core.account"
    - applied_configurationsarray of enums
    - closednullable boolean

Retrieves the details of an Account.

The ID of the Account to retrieve.

Additional fields to include in the response.

Include parameter to expose configuration.customer on an Account.

Include parameter to expose configuration.merchant on an Account.

Include parameter to expose configuration.recipient on an Account.

Include parameter to expose defaults on an Account.

Include parameter to expose future_requirements on an Account.

Include parameter to expose identity on an Account.

Include parameter to expose requirements on an Account.

Unique identifier for the Account.

String representing the object’s type. Objects of the same type share the same value of the object field.

The configurations that have been applied to this account.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Indicates whether the account has been closed.

An Account represents a company, individual, or other entity that a user interacts with. Accounts store identity information and one or more configurations that enable product-specific capabilities. You can assign configurations at creation or add them later.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values for settings shared across Account configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the future requirements for the Account that will eventually come into effect, including what information needs to be collected, and by when.

Information about the company, individual, and business represented by the Account.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the active requirements for the Account, including what information needs to be collected, and by when.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

The resource wasn’t found.

Returns a list of Accounts.

Filter only accounts that have all of the configurations specified. If omitted, returns all accounts regardless of which configurations they have.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Filter by whether the account is closed. If omitted, returns only Accounts that are not closed.

The upper limit on the number of accounts returned by the List Account request.

The page token to navigate to next or previous batch of accounts given by the list request.

A list of retrieved Account objects.

URL with page token to navigate to next batch of accounts given by the list request.

URL with page token to navigate to previous batch of accounts given by the list request.

Accounts v2 is not enabled for your platform.

Removes access to the Account and its associated resources. Closed Accounts can no longer be operated on, but limited information can still be retrieved through the API in order to be able to track their history.

The ID of the Account to close.

Configurations on the Account to be closed. All configurations on the Account must be passed in for this request to succeed.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Unique identifier for the Account.

String representing the object’s type. Objects of the same type share the same value of the object field.

The configurations that have been applied to this account.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Indicates whether the account has been closed.

An Account represents a company, individual, or other entity that a user interacts with. Accounts store identity information and one or more configurations that enable product-specific capabilities. You can assign configurations at creation or add them later.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values for settings shared across Account configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the future requirements for the Account that will eventually come into effect, including what information needs to be collected, and by when.

Information about the company, individual, and business represented by the Account.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the active requirements for the Account, including what information needs to be collected, and by when.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

Account with Merchant or Recipient configuration with transfers feature cannot be closed because the account has a cash balance.

Account with Customer configuration cannot be closed because the customer has a cash balance.

Account cannot be closed without specifying the right configurations.

Account cannot be closed due to other pending resources.

Platform has not signed up for Connect and cannot create connected accounts.

Account with Stripe-owned loss liability and dashboard cannot be deleted.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

The resource wasn’t found.

This is a list of all public thin events we currently send for updates to Account, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  -d "include[0]"=defaults \  -d "include[1]"=identity \  -d "include[2]"="configuration.merchant"
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  -d "include[0]"=defaults \  -d "include[1]"=identity \  -d "include[2]"="configuration.merchant"
```

Example 3 (unknown):
```unknown
{  "id": "acct_1Nv0FGQ9RKHgCVdK",  "object": "v2.core.account",  "applied_configurations": [    "customer",    "merchant"  ],  "configuration": {    "merchant": {      "applied": "2024-11-26T16:33:03.000Z",      "card_payments": {        "decline_on": {          "avs_failure": false,          "cvc_failure": false        }      },      "capabilities": {        "card_payments": {          "status": "restricted",          "status_details": [            {              "code": "requirements_past_due",              "resolution": "provide_info"            }          ]        }      },      "statement_descriptor": {        "descriptor": "accessible.stripe.com"      }    }  },  "contact_email": "furever@example.com",  "created": "2024-11-26T16:33:03.000Z",  "dashboard": "full",  "identity": {    "business_details": {      "address": {        "country": "us"      },      "id_numbers": [        {          "type": "us_ein"        }      ],      "structure": "sole_proprietorship"    },    "country": "us",    "entity_type": "company"  },  "defaults": {    "currency": "usd",    "locales": [],    "profile": {      "business_url": "http://accessible.stripe.com",      "doing_business_as": "FurEver",      "product_description": "Saas pet grooming platform at furever.dev using Connect embedded components"    },    "responsibilities": {      "fees_collector": "stripe",      "losses_collector": "stripe",      "requirements_collector": "stripe"    }  },  "display_name": "Furever",  "livemode": true,  "metadata": {}}
```

Example 4 (unknown):
```unknown
{  "id": "acct_1Nv0FGQ9RKHgCVdK",  "object": "v2.core.account",  "applied_configurations": [    "customer",    "merchant"  ],  "configuration": {    "merchant": {      "applied": "2024-11-26T16:33:03.000Z",      "card_payments": {        "decline_on": {          "avs_failure": false,          "cvc_failure": false        }      },      "capabilities": {        "card_payments": {          "status": "restricted",          "status_details": [            {              "code": "requirements_past_due",              "resolution": "provide_info"            }          ]        }      },      "statement_descriptor": {        "descriptor": "accessible.stripe.com"      }    }  },  "contact_email": "furever@example.com",  "created": "2024-11-26T16:33:03.000Z",  "dashboard": "full",  "identity": {    "business_details": {      "address": {        "country": "us"      },      "id_numbers": [        {          "type": "us_ein"        }      ],      "structure": "sole_proprietorship"    },    "country": "us",    "entity_type": "company"  },  "defaults": {    "currency": "usd",    "locales": [],    "profile": {      "business_url": "http://accessible.stripe.com",      "doing_business_as": "FurEver",      "product_description": "Saas pet grooming platform at furever.dev using Connect embedded components"    },    "responsibilities": {      "fees_collector": "stripe",      "losses_collector": "stripe",      "requirements_collector": "stripe"    }  },  "display_name": "Furever",  "livemode": true,  "metadata": {}}
```

---

## Create a person v2

**URL:** https://docs.stripe.com/api/v2/core/accounts/create-person

**Contents:**
- Create a person v2
  - Parameters
    - account_idstringRequired
    - additional_addressesarray of objects
    - additional_namesarray of objects
    - additional_terms_of_serviceobject
    - addressobject
    - date_of_birthobject
    - documentsobject
    - emailstring

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

Delete a Person associated with an Account.

The Account the Person is associated with.

The ID of the Person to delete.

String representing the object’s type. Objects of the same type share the same value.

Always true for a deleted object.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

The resource wasn’t found.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/persons \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "given_name": "Jenny",    "surname": "Rosen",    "email": "jenny.rosen@example.com",    "address": {        "line1": "27 Fredrick Ave",        "city": "Brothers",        "postal_code": "97712",        "state": "OR",        "country": "us"    },    "id_numbers": [        {            "type": "us_ssn_last_4",            "value": "0000"        }    ],    "relationship": {        "owner": true,        "percent_ownership": "0.8",        "representative": true,        "title": "CEO"    }  }'
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/persons \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "given_name": "Jenny",    "surname": "Rosen",    "email": "jenny.rosen@example.com",    "address": {        "line1": "27 Fredrick Ave",        "city": "Brothers",        "postal_code": "97712",        "state": "OR",        "country": "us"    },    "id_numbers": [        {            "type": "us_ssn_last_4",            "value": "0000"        }    ],    "relationship": {        "owner": true,        "percent_ownership": "0.8",        "representative": true,        "title": "CEO"    }  }'
```

Example 3 (unknown):
```unknown
{  "id": "person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_person",  "account": "acct_1Nv0FGQ9RKHgCVdK",  "additional_addresses": [],  "additional_names": [],  "address": {    "city": "Brothers",    "country": "us",    "line1": "27 Fredrick Ave",    "postal_code": "97712",    "state": "OR"  },  "created": "2024-11-26T17:10:07.000Z",  "email": "jenny.rosen@example.com",  "given_name": "Jenny",  "id_numbers": [    {      "type": "us_ssn_last_4"    }  ],  "livemode": true,  "metadata": {},  "nationalities": [],  "relationship": {    "owner": true,    "percent_ownership": "0.8",    "representative": true,    "title": "CEO"  },  "surname": "Rosen",  "updated": "2024-11-26T17:10:07.000Z"}
```

Example 4 (unknown):
```unknown
{  "id": "person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_person",  "account": "acct_1Nv0FGQ9RKHgCVdK",  "additional_addresses": [],  "additional_names": [],  "address": {    "city": "Brothers",    "country": "us",    "line1": "27 Fredrick Ave",    "postal_code": "97712",    "state": "OR"  },  "created": "2024-11-26T17:10:07.000Z",  "email": "jenny.rosen@example.com",  "given_name": "Jenny",  "id_numbers": [    {      "type": "us_ssn_last_4"    }  ],  "livemode": true,  "metadata": {},  "nationalities": [],  "relationship": {    "owner": true,    "percent_ownership": "0.8",    "representative": true,    "title": "CEO"  },  "surname": "Rosen",  "updated": "2024-11-26T17:10:07.000Z"}
```

---

## 

**URL:** https://docs.stripe.com/connect/required-verification-information

---

## Retrieve an account token v2

**URL:** https://docs.stripe.com/api/v2/core/accounts/retrieve-account-token

**Contents:**
- Retrieve an account token v2
  - Parameters
    - idstringRequired
  - Returns
  - Response attributes
    - idstring
    - objectstring, value is "v2.core.account_token"
    - createdtimestamp
    - expires_attimestamp
    - livemodeboolean

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
curl https://api.stripe.com/v2/core/account_tokens/accttok_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v2/core/account_tokens/accttok_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 3 (unknown):
```unknown
{  "id": "accttok_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_token",  "created": "2025-11-17T14:00:00.000Z",  "expires_at": "2025-11-17T14:10:00.000Z",  "livemode": true,  "used": true}
```

Example 4 (unknown):
```unknown
{  "id": "accttok_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_token",  "created": "2025-11-17T14:00:00.000Z",  "expires_at": "2025-11-17T14:10:00.000Z",  "livemode": true,  "used": true}
```

---

## Update an account v2

**URL:** https://docs.stripe.com/api/v2/core/accounts/update

**Contents:**
- Update an account v2
  - Parameters
    - idstringRequired
    - account_tokenstring
    - configurationobject
    - contact_emailstring
    - dashboardenum
    - defaultsobject
    - display_namestring
    - identityobject

Updates the details of an Account.

The ID of the Account to update.

The account token generated by the account token api.

An Account Configuration which allows the Account to take on a key persona across Stripe products.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values to be used on Account Configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the company, individual, and business represented by the Account.

Additional fields to include in the response.

Include parameter to expose configuration.customer on an Account.

Include parameter to expose configuration.merchant on an Account.

Include parameter to expose configuration.recipient on an Account.

Include parameter to expose defaults on an Account.

Include parameter to expose future_requirements on an Account.

Include parameter to expose identity on an Account.

Include parameter to expose requirements on an Account.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Unique identifier for the Account.

String representing the object’s type. Objects of the same type share the same value of the object field.

The configurations that have been applied to this account.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Indicates whether the account has been closed.

An Account represents a company, individual, or other entity that a user interacts with. Accounts store identity information and one or more configurations that enable product-specific capabilities. You can assign configurations at creation or add them later.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values for settings shared across Account configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the future requirements for the Account that will eventually come into effect, including what information needs to be collected, and by when.

Information about the company, individual, and business represented by the Account.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the active requirements for the Account, including what information needs to be collected, and by when.

Requested capability is not available.

If dashboard is express, fees_collector must be application and losses_collector must be application.

If losses_collector is application, fees_collector must also be application.

Connect integration combination is not supported when UA beta is disabled.

Responsibility combinations is not supported in private preview.

Currency is not allowed for the account’s country.

Account is not yet compatible with V2 APIs.

Terms of service must be accepted before adding merchant configuration.

Account token required for platforms in mandated countries (e.g., France).

Accounts v2 is not enabled for your platform.

Invalid characters are provided for address fields.

Address country doesn’t match identity country.

Address postal code is invalid.

Address state is invalid.

Address town is invalid.

Default payment method is added to the customer config before attaching it to the account using /v1/payment_methods.

Creating accounts with the BGN currency is no longer supported, as Bulgaria is now using the Euro as of 2026-01-01.

Dormant accounts cannot create accounts where requirements collector is application (this is an account takeover prevention measure).

Cannot set automatic_indirect_tax.validate_location when initially creating a customer configuration.

Feature cannot be unrequested due to being a requirement for another feature.

Feature cannot be requested for the dashboard type.

Requested feature is not available for the entity type in your country.

Requested capability is not available in your country.

Feature cannot be requested given the platform’s country.

Requested feature is not available without also requesting a different feature.

Requested feature is not available without also requesting a different feature in your country.

Configuration cannot be deactivated.

Configuration cannot be deactivated due to a dependency with another capability.

Cannot deactivate a configuration due to another configuration depending on it.

Configuration cannot be updated while deactivated.

Cannot create an account with an invalid configuration.

Cross-border connected account creation is not allowed for this platform/account country combination.

Custom accounts cannot be created in certain countries.

Invalid customer tax location.

Representative date of birth does not meet the age limit.

Representative date of birth is provided an invalid date or a future date.

Cannot change defaults.currency post account activation.

Outbound Destination ID is invalid.

Default payment method provided for a customer does not exist or is otherwise invalid.

Provided file tokens for documents are invalid, not found, deleted, or belong to a different account.

Provided file tokens for documents are of the wrong purpose.

Duplicate person is added to an account.

Email contains unsupported domain.

Incorrect email is provided.

The identity.entity_type value is not supported in a given identity.country.

NONE is combined with another value in the HighRiskActivities list.

Provided ID number is of the wrong format for the given type.

The identity.country value is required but not provided.

Identity param has been made immutable due to the state of the account.

Incorrect ID number is provided for a country.

The incorrect token type is provided .

ID number is provided that is not permitted for the Identity’s entity type and business structure.

The identity.business_details.id_numbers.registrar value is an invalid DE registrar.

Konbini Payments Support Hours is Invalid.

Konbini Payments Support Phone Number is Invalid.

Invalid IP address is provided.

MCC is invalid for configuration.merchant.mcc.

Kana Kanji script addresses must have JP country.

Parameter cannot be passed alongside account_token.

Error returned when relationship.owner is set to true but the ownership percentage is set to 0%.

Phone number is invalid.

Postal code is required for Japanese addresses.

PurposeOfFundsDescription is not empty while PurposeOfFunds is not OTHER.

Provided script characters are invalid for the script.

Shipping address is required within the shipping hash.

Shipping name is required within the shipping hash.

Statement descriptor is invalid.

The business_details.structure value is not valid for identity.country and identity.entity_type.

Cannot set a test clock on a livemode customer.

Test clock does not exist or is otherwise invalid.

The token is re-used with a different idempotency key.

TOS cannot be accepted on behalf of accounts when requirement collection is stripe.

Total ownership percentages of all Persons on the account exceeds 100%.

Cannot set responsibilities on the current configurations.

Cannot set identity fields when the Account is only configured as a customer.

Address is in an unsupported postal code.

Address is in an unsupported state.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

A v1 token ID is passed in v2 APIs.

Invalid account token.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

Retrieves the details of an Account.

The ID of the Account to retrieve.

Additional fields to include in the response.

Include parameter to expose configuration.customer on an Account.

Include parameter to expose configuration.merchant on an Account.

Include parameter to expose configuration.recipient on an Account.

Include parameter to expose defaults on an Account.

Include parameter to expose future_requirements on an Account.

Include parameter to expose identity on an Account.

Include parameter to expose requirements on an Account.

Unique identifier for the Account.

String representing the object’s type. Objects of the same type share the same value of the object field.

The configurations that have been applied to this account.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Indicates whether the account has been closed.

An Account represents a company, individual, or other entity that a user interacts with. Accounts store identity information and one or more configurations that enable product-specific capabilities. You can assign configurations at creation or add them later.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values for settings shared across Account configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the future requirements for the Account that will eventually come into effect, including what information needs to be collected, and by when.

Information about the company, individual, and business represented by the Account.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the active requirements for the Account, including what information needs to be collected, and by when.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

The resource wasn’t found.

Returns a list of Accounts.

Filter only accounts that have all of the configurations specified. If omitted, returns all accounts regardless of which configurations they have.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Filter by whether the account is closed. If omitted, returns only Accounts that are not closed.

The upper limit on the number of accounts returned by the List Account request.

The page token to navigate to next or previous batch of accounts given by the list request.

A list of retrieved Account objects.

URL with page token to navigate to next batch of accounts given by the list request.

URL with page token to navigate to previous batch of accounts given by the list request.

Accounts v2 is not enabled for your platform.

Removes access to the Account and its associated resources. Closed Accounts can no longer be operated on, but limited information can still be retrieved through the API in order to be able to track their history.

The ID of the Account to close.

Configurations on the Account to be closed. All configurations on the Account must be passed in for this request to succeed.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Unique identifier for the Account.

String representing the object’s type. Objects of the same type share the same value of the object field.

The configurations that have been applied to this account.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Indicates whether the account has been closed.

An Account represents a company, individual, or other entity that a user interacts with. Accounts store identity information and one or more configurations that enable product-specific capabilities. You can assign configurations at creation or add them later.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values for settings shared across Account configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the future requirements for the Account that will eventually come into effect, including what information needs to be collected, and by when.

Information about the company, individual, and business represented by the Account.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the active requirements for the Account, including what information needs to be collected, and by when.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

Account with Merchant or Recipient configuration with transfers feature cannot be closed because the account has a cash balance.

Account with Customer configuration cannot be closed because the customer has a cash balance.

Account cannot be closed without specifying the right configurations.

Account cannot be closed due to other pending resources.

Platform has not signed up for Connect and cannot create connected accounts.

Account with Stripe-owned loss liability and dashboard cannot be deleted.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

The resource wasn’t found.

This is a list of all public thin events we currently send for updates to Account, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "defaults": {        "profile": {            "business_url": "http://accessible.stripe.com",            "doing_business_as": "FurEver",            "product_description": "Saas pet grooming platform at furever.dev using Connect embedded components"        }    },    "identity": {        "business_details": {            "structure": "sole_proprietorship",            "id_numbers": [                {                    "type": "us_ein",                    "value": "000000000"                }            ]        }    },    "include": [        "defaults",        "identity"    ]  }'
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "defaults": {        "profile": {            "business_url": "http://accessible.stripe.com",            "doing_business_as": "FurEver",            "product_description": "Saas pet grooming platform at furever.dev using Connect embedded components"        }    },    "identity": {        "business_details": {            "structure": "sole_proprietorship",            "id_numbers": [                {                    "type": "us_ein",                    "value": "000000000"                }            ]        }    },    "include": [        "defaults",        "identity"    ]  }'
```

Example 3 (unknown):
```unknown
{  "id": "acct_1Nv0FGQ9RKHgCVdK",  "object": "v2.core.account",  "applied_configurations": [    "customer",    "merchant"  ],  "contact_email": "furever@example.com",  "created": "2024-11-26T16:33:03.000Z",  "dashboard": "full",  "identity": {    "business_details": {      "id_numbers": [        {          "type": "us_ein"        }      ],      "registered_name": "Furever",      "structure": "sole_proprietorship"    },    "country": "us",    "entity_type": "company"  },  "defaults": {    "currency": "usd",    "locales": [],    "profile": {      "business_url": "http://accessible.stripe.com",      "doing_business_as": "FurEver",      "product_description": "Saas pet grooming platform at furever.dev using Connect embedded components"    },    "responsibilities": {      "fees_collector": "stripe",      "losses_collector": "stripe",      "requirements_collector": "stripe"    }  },  "display_name": "Furever",  "livemode": true,  "metadata": {}}
```

Example 4 (unknown):
```unknown
{  "id": "acct_1Nv0FGQ9RKHgCVdK",  "object": "v2.core.account",  "applied_configurations": [    "customer",    "merchant"  ],  "contact_email": "furever@example.com",  "created": "2024-11-26T16:33:03.000Z",  "dashboard": "full",  "identity": {    "business_details": {      "id_numbers": [        {          "type": "us_ein"        }      ],      "registered_name": "Furever",      "structure": "sole_proprietorship"    },    "country": "us",    "entity_type": "company"  },  "defaults": {    "currency": "usd",    "locales": [],    "profile": {      "business_url": "http://accessible.stripe.com",      "doing_business_as": "FurEver",      "product_description": "Saas pet grooming platform at furever.dev using Connect embedded components"    },    "responsibilities": {      "fees_collector": "stripe",      "losses_collector": "stripe",      "requirements_collector": "stripe"    }  },  "display_name": "Furever",  "livemode": true,  "metadata": {}}
```

---

## Update a person v2

**URL:** https://docs.stripe.com/api/v2/core/accounts/update-person

**Contents:**
- Update a person v2
  - Parameters
    - account_idstringRequired
    - idstringRequired
    - additional_addressesarray of objects
    - additional_namesarray of objects
    - additional_terms_of_serviceobject
    - addressobject
    - date_of_birthobject
    - documentsobject

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

Delete a Person associated with an Account.

The Account the Person is associated with.

The ID of the Person to delete.

String representing the object’s type. Objects of the same type share the same value.

Always true for a deleted object.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

The resource wasn’t found.

This is a list of all public thin events we currently send for updates to Person, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/persons/person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "date_of_birth": {        "day": 28,        "month": 1,        "year": 2000    }  }'
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/persons/person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "date_of_birth": {        "day": 28,        "month": 1,        "year": 2000    }  }'
```

Example 3 (unknown):
```unknown
{  "id": "person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_person",  "account": "acct_1Nv0FGQ9RKHgCVdK",  "additional_addresses": [],  "additional_names": [],  "address": {    "city": "Brothers",    "country": "us",    "line1": "27 Fredrick Ave",    "postal_code": "97712",    "state": "OR"  },  "created": "2024-11-26T17:10:07.000Z",  "date_of_birth": {    "day": 28,    "month": 1,    "year": 2000  },  "email": "jenny.rosen@example.com",  "given_name": "Jenny",  "id_numbers": [    {      "type": "us_ssn_last_4"    }  ],  "livemode": true,  "metadata": {},  "nationalities": [],  "relationship": {    "owner": true,    "percent_ownership": "0.8",    "representative": true,    "title": "CEO"  },  "surname": "Rosen",  "updated": "2024-11-26T17:12:55.000Z"}
```

Example 4 (unknown):
```unknown
{  "id": "person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_person",  "account": "acct_1Nv0FGQ9RKHgCVdK",  "additional_addresses": [],  "additional_names": [],  "address": {    "city": "Brothers",    "country": "us",    "line1": "27 Fredrick Ave",    "postal_code": "97712",    "state": "OR"  },  "created": "2024-11-26T17:10:07.000Z",  "date_of_birth": {    "day": 28,    "month": 1,    "year": 2000  },  "email": "jenny.rosen@example.com",  "given_name": "Jenny",  "id_numbers": [    {      "type": "us_ssn_last_4"    }  ],  "livemode": true,  "metadata": {},  "nationalities": [],  "relationship": {    "owner": true,    "percent_ownership": "0.8",    "representative": true,    "title": "CEO"  },  "surname": "Rosen",  "updated": "2024-11-26T17:12:55.000Z"}
```

---

## Create an account token v2

**URL:** https://docs.stripe.com/api/v2/core/accounts/create-account-token

**Contents:**
- Create an account token v2
  - Parameters
    - contact_emailstring
    - display_namestring
    - identityobject
  - Returns
  - Response attributes
    - idstring
    - objectstring, value is "v2.core.account_token"
    - createdtimestamp

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
curl -X POST https://api.stripe.com/v2/core/account_tokens \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "contact_email": "furever@example.com",    "display_name": "Furever",    "identity": {        "attestations": {            "terms_of_service": {                "account": {                    "shown_and_accepted": true                }            }        },        "entity_type": "company",        "business_details": {            "registered_name": "Furever"        }    }  }'
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/account_tokens \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "contact_email": "furever@example.com",    "display_name": "Furever",    "identity": {        "attestations": {            "terms_of_service": {                "account": {                    "shown_and_accepted": true                }            }        },        "entity_type": "company",        "business_details": {            "registered_name": "Furever"        }    }  }'
```

Example 3 (unknown):
```unknown
{  "id": "accttok_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_token",  "created": "2025-11-17T14:00:00.000Z",  "expires_at": "2025-11-17T14:10:00.000Z",  "livemode": true,  "used": false}
```

Example 4 (unknown):
```unknown
{  "id": "accttok_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_token",  "created": "2025-11-17T14:00:00.000Z",  "expires_at": "2025-11-17T14:10:00.000Z",  "livemode": true,  "used": false}
```

---

## Accounts v2

**URL:** https://docs.stripe.com/api/v2/core/accounts

**Contents:**
- Accounts v2
- The Account object
  - Attributes
    - idstring
    - objectstring, value is "v2.core.account"
    - applied_configurationsarray of enums
    - closednullable boolean
    - configurationnullable object
    - contact_emailnullable string
    - createdtimestamp

An Account v2 object represents a company, individual, or other entity that interacts with a platform on Stripe. It contains both identifying information and properties that control its behavior and functionality. An Account can have one or more configurations that enable sets of related features, such as allowing it to act as a merchant or customer.

The Accounts v2 API is generally available for Connect and supports the Global Payouts public preview.

Unique identifier for the Account.

String representing the object’s type. Objects of the same type share the same value of the object field.

The configurations that have been applied to this account.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Indicates whether the account has been closed.

An Account represents a company, individual, or other entity that a user interacts with. Accounts store identity information and one or more configurations that enable product-specific capabilities. You can assign configurations at creation or add them later.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values for settings shared across Account configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the future requirements for the Account that will eventually come into effect, including what information needs to be collected, and by when.

Information about the company, individual, and business represented by the Account.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the active requirements for the Account, including what information needs to be collected, and by when.

An Account is a representation of a company, individual or other entity that a user interacts with. Accounts contain identifying information about the entity, and configurations that store the features an account has access to. An account can be configured as any or all of the following configurations: Customer, Merchant and/or Recipient.

The account token generated by the account token api.

An Account Configuration which allows the Account to take on a key persona across Stripe products.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values to be used on Account Configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the company, individual, and business represented by the Account.

Additional fields to include in the response.

Include parameter to expose configuration.customer on an Account.

Include parameter to expose configuration.merchant on an Account.

Include parameter to expose configuration.recipient on an Account.

Include parameter to expose defaults on an Account.

Include parameter to expose future_requirements on an Account.

Include parameter to expose identity on an Account.

Include parameter to expose requirements on an Account.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Unique identifier for the Account.

String representing the object’s type. Objects of the same type share the same value of the object field.

The configurations that have been applied to this account.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Indicates whether the account has been closed.

An Account represents a company, individual, or other entity that a user interacts with. Accounts store identity information and one or more configurations that enable product-specific capabilities. You can assign configurations at creation or add them later.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values for settings shared across Account configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the future requirements for the Account that will eventually come into effect, including what information needs to be collected, and by when.

Information about the company, individual, and business represented by the Account.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the active requirements for the Account, including what information needs to be collected, and by when.

Requested capability is not available.

If dashboard is express, fees_collector must be application and losses_collector must be application.

If losses_collector is application, fees_collector must also be application.

Connect integration combination is not supported when UA beta is enabled.

Connect integration combination is not supported when UA beta is disabled.

Responsibility combinations is not supported in private preview.

Currency is not allowed for the account’s country.

Platform must be activated to create connected accounts.

Account creation is invalid.

Account creation error - liability unacknowledged.

Account creation error - requirement collection and liability unacknowledged.

Account creation error - requirement collection unacknowledged.

Terms of service must be accepted before adding merchant configuration.

Account token required for platforms in mandated countries (e.g., France).

Accounts v2 is not enabled for your platform.

Invalid characters are provided for address fields.

Address country doesn’t match identity country.

Address postal code is invalid.

Address state is invalid.

Address town is invalid.

Creating accounts with the BGN currency is no longer supported, as Bulgaria is now using the Euro as of 2026-01-01.

Dormant accounts cannot create accounts where requirements collector is application (this is an account takeover prevention measure).

Platform is in an invalid state and cannot create connected accounts.

Platform is in a rejected state and cannot create connected accounts.

Feature cannot be unrequested due to being a requirement for another feature.

Feature cannot be requested for the dashboard type.

Requested feature is not available for the entity type in your country.

Requested capability is not available in your country.

Feature cannot be requested given the platform’s country.

Requested feature is not available without also requesting a different feature.

Requested feature is not available without also requesting a different feature in your country.

Cannot create an account with an invalid configuration.

Platform is not verified and cannot create connected accounts.

Platform has not completed platform questionnaire and cannot create connected accounts.

Cross-border connected account creation is not allowed for this platform/account country combination.

Custom accounts cannot be created in certain countries.

Representative date of birth does not meet the age limit.

Representative date of birth is provided an invalid date or a future date.

Cannot change defaults.currency post account activation.

Default payment method provided for a customer does not exist or is otherwise invalid.

Specified payment method exists but its type is not allowed to be the default payment method.

Directorship declaration is not allowed during account creation.

Provided file tokens for documents are invalid, not found, deleted, or belong to a different account.

Provided file tokens for documents are of the wrong purpose.

Email contains unsupported domain.

Incorrect email is provided.

The identity.entity_type value is not supported in a given identity.country.

NONE is combined with another value in the HighRiskActivities list.

Provided ID number is of the wrong format for the given type.

The identity.country value is required but not provided.

Incorrect ID number is provided for a country.

The incorrect token type is provided .

ID number is provided that is not permitted for the Identity’s entity type and business structure.

The identity.business_details.id_numbers.registrar value is an invalid DE registrar.

Konbini Payments Support Hours is Invalid.

Konbini Payments Support Phone Number is Invalid.

Invoice rendering template does not exist or is otherwise invalid.

Invalid IP address is provided.

MCC is invalid for configuration.merchant.mcc.

Kana Kanji script addresses must have JP country.

Ownership declaration is not allowed during account creation.

Parameter cannot be passed alongside account_token.

Error returned when relationship.owner is set to true but the ownership percentage is set to 0%.

Phone number is invalid.

Platform has not signed up for Connect and cannot create connected accounts.

Postal code is required for Japanese addresses.

PurposeOfFundsDescription is not empty while PurposeOfFunds is not OTHER.

Provided script characters are invalid for the script.

Shipping address is required within the shipping hash.

Shipping name is required within the shipping hash.

Statement descriptor is invalid.

The business_details.structure value is not valid for identity.country and identity.entity_type.

Cannot set a test clock on a livemode customer.

Test clock does not exist or is otherwise invalid.

Cannot modify a test clock that is currently advancing.

Cannot add customer to a test clock that has already reached its customer limit.

The token is re-used with a different idempotency key.

TOS cannot be accepted on behalf of accounts when requirement collection is stripe.

Cannot set responsibilities on the current configurations.

Cannot set identity fields when the Account is only configured as a customer.

Address is in an unsupported postal code.

Address is in an unsupported state.

A v1 token ID is passed in v2 APIs.

Invalid account token.

An idempotent retry occurred with different request parameters.

Updates the details of an Account.

The ID of the Account to update.

The account token generated by the account token api.

An Account Configuration which allows the Account to take on a key persona across Stripe products.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values to be used on Account Configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the company, individual, and business represented by the Account.

Additional fields to include in the response.

Include parameter to expose configuration.customer on an Account.

Include parameter to expose configuration.merchant on an Account.

Include parameter to expose configuration.recipient on an Account.

Include parameter to expose defaults on an Account.

Include parameter to expose future_requirements on an Account.

Include parameter to expose identity on an Account.

Include parameter to expose requirements on an Account.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Unique identifier for the Account.

String representing the object’s type. Objects of the same type share the same value of the object field.

The configurations that have been applied to this account.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Indicates whether the account has been closed.

An Account represents a company, individual, or other entity that a user interacts with. Accounts store identity information and one or more configurations that enable product-specific capabilities. You can assign configurations at creation or add them later.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values for settings shared across Account configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the future requirements for the Account that will eventually come into effect, including what information needs to be collected, and by when.

Information about the company, individual, and business represented by the Account.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the active requirements for the Account, including what information needs to be collected, and by when.

Requested capability is not available.

If dashboard is express, fees_collector must be application and losses_collector must be application.

If losses_collector is application, fees_collector must also be application.

Connect integration combination is not supported when UA beta is disabled.

Responsibility combinations is not supported in private preview.

Currency is not allowed for the account’s country.

Account is not yet compatible with V2 APIs.

Terms of service must be accepted before adding merchant configuration.

Account token required for platforms in mandated countries (e.g., France).

Accounts v2 is not enabled for your platform.

Invalid characters are provided for address fields.

Address country doesn’t match identity country.

Address postal code is invalid.

Address state is invalid.

Address town is invalid.

Default payment method is added to the customer config before attaching it to the account using /v1/payment_methods.

Creating accounts with the BGN currency is no longer supported, as Bulgaria is now using the Euro as of 2026-01-01.

Dormant accounts cannot create accounts where requirements collector is application (this is an account takeover prevention measure).

Cannot set automatic_indirect_tax.validate_location when initially creating a customer configuration.

Feature cannot be unrequested due to being a requirement for another feature.

Feature cannot be requested for the dashboard type.

Requested feature is not available for the entity type in your country.

Requested capability is not available in your country.

Feature cannot be requested given the platform’s country.

Requested feature is not available without also requesting a different feature.

Requested feature is not available without also requesting a different feature in your country.

Configuration cannot be deactivated.

Configuration cannot be deactivated due to a dependency with another capability.

Cannot deactivate a configuration due to another configuration depending on it.

Configuration cannot be updated while deactivated.

Cannot create an account with an invalid configuration.

Cross-border connected account creation is not allowed for this platform/account country combination.

Custom accounts cannot be created in certain countries.

Invalid customer tax location.

Representative date of birth does not meet the age limit.

Representative date of birth is provided an invalid date or a future date.

Cannot change defaults.currency post account activation.

Outbound Destination ID is invalid.

Default payment method provided for a customer does not exist or is otherwise invalid.

Provided file tokens for documents are invalid, not found, deleted, or belong to a different account.

Provided file tokens for documents are of the wrong purpose.

Duplicate person is added to an account.

Email contains unsupported domain.

Incorrect email is provided.

The identity.entity_type value is not supported in a given identity.country.

NONE is combined with another value in the HighRiskActivities list.

Provided ID number is of the wrong format for the given type.

The identity.country value is required but not provided.

Identity param has been made immutable due to the state of the account.

Incorrect ID number is provided for a country.

The incorrect token type is provided .

ID number is provided that is not permitted for the Identity’s entity type and business structure.

The identity.business_details.id_numbers.registrar value is an invalid DE registrar.

Konbini Payments Support Hours is Invalid.

Konbini Payments Support Phone Number is Invalid.

Invalid IP address is provided.

MCC is invalid for configuration.merchant.mcc.

Kana Kanji script addresses must have JP country.

Parameter cannot be passed alongside account_token.

Error returned when relationship.owner is set to true but the ownership percentage is set to 0%.

Phone number is invalid.

Postal code is required for Japanese addresses.

PurposeOfFundsDescription is not empty while PurposeOfFunds is not OTHER.

Provided script characters are invalid for the script.

Shipping address is required within the shipping hash.

Shipping name is required within the shipping hash.

Statement descriptor is invalid.

The business_details.structure value is not valid for identity.country and identity.entity_type.

Cannot set a test clock on a livemode customer.

Test clock does not exist or is otherwise invalid.

The token is re-used with a different idempotency key.

TOS cannot be accepted on behalf of accounts when requirement collection is stripe.

Total ownership percentages of all Persons on the account exceeds 100%.

Cannot set responsibilities on the current configurations.

Cannot set identity fields when the Account is only configured as a customer.

Address is in an unsupported postal code.

Address is in an unsupported state.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

A v1 token ID is passed in v2 APIs.

Invalid account token.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

Retrieves the details of an Account.

The ID of the Account to retrieve.

Additional fields to include in the response.

Include parameter to expose configuration.customer on an Account.

Include parameter to expose configuration.merchant on an Account.

Include parameter to expose configuration.recipient on an Account.

Include parameter to expose defaults on an Account.

Include parameter to expose future_requirements on an Account.

Include parameter to expose identity on an Account.

Include parameter to expose requirements on an Account.

Unique identifier for the Account.

String representing the object’s type. Objects of the same type share the same value of the object field.

The configurations that have been applied to this account.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Indicates whether the account has been closed.

An Account represents a company, individual, or other entity that a user interacts with. Accounts store identity information and one or more configurations that enable product-specific capabilities. You can assign configurations at creation or add them later.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values for settings shared across Account configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the future requirements for the Account that will eventually come into effect, including what information needs to be collected, and by when.

Information about the company, individual, and business represented by the Account.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the active requirements for the Account, including what information needs to be collected, and by when.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

The resource wasn’t found.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "acct_1Nv0FGQ9RKHgCVdK",  "object": "v2.core.account",  "applied_configurations": [    "customer",    "merchant"  ],  "configuration": {    "customer": {      "automatic_indirect_tax": {        "exempt": "none",        "location": {          "country": "US",          "state": "NY"        },        "location_source": "identity_address"      },      "billing": {        "invoice": {          "next_sequence": 1,          "prefix": "5626C87C",          "custom_fields": []        }      },      "capabilities": {        "automatic_indirect_tax": {          "status": "active",          "status_details": []        }      }    },    "merchant": {      "card_payments": {        "decline_on": {          "avs_failure": false,          "cvc_failure": false        }      },      "capabilities": {        "card_payments": {          "status": "active",          "status_details": []        },        "stripe_balance": {          "payouts": {            "status": "active",            "status_details": []          }        }      }    }  },  "contact_email": "furever@example.com",  "created": "2025-03-28T19:59:16.000Z",  "dashboard": "full",  "identity": {    "business_details": {      "registered_name": "Furever",      "address": {        "country": "US",        "postal_code": "10001"      }    },    "country": "US",    "entity_type": "company"  },  "defaults": {    "currency": "usd",    "responsibilities": {      "fees_collector": "stripe",      "losses_collector": "stripe",      "requirements_collector": "stripe"    }  },  "display_name": "Furever"}
```

Example 2 (unknown):
```unknown
{  "id": "acct_1Nv0FGQ9RKHgCVdK",  "object": "v2.core.account",  "applied_configurations": [    "customer",    "merchant"  ],  "configuration": {    "customer": {      "automatic_indirect_tax": {        "exempt": "none",        "location": {          "country": "US",          "state": "NY"        },        "location_source": "identity_address"      },      "billing": {        "invoice": {          "next_sequence": 1,          "prefix": "5626C87C",          "custom_fields": []        }      },      "capabilities": {        "automatic_indirect_tax": {          "status": "active",          "status_details": []        }      }    },    "merchant": {      "card_payments": {        "decline_on": {          "avs_failure": false,          "cvc_failure": false        }      },      "capabilities": {        "card_payments": {          "status": "active",          "status_details": []        },        "stripe_balance": {          "payouts": {            "status": "active",            "status_details": []          }        }      }    }  },  "contact_email": "furever@example.com",  "created": "2025-03-28T19:59:16.000Z",  "dashboard": "full",  "identity": {    "business_details": {      "registered_name": "Furever",      "address": {        "country": "US",        "postal_code": "10001"      }    },    "country": "US",    "entity_type": "company"  },  "defaults": {    "currency": "usd",    "responsibilities": {      "fees_collector": "stripe",      "losses_collector": "stripe",      "requirements_collector": "stripe"    }  },  "display_name": "Furever"}
```

Example 3 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "contact_email": "furever@example.com",    "display_name": "Furever",    "identity": {        "country": "us",        "entity_type": "company",        "business_details": {            "registered_name": "Furever"        }    },    "configuration": {        "customer": {            "capabilities": {                "automatic_indirect_tax": {                    "requested": true                }            }        },        "merchant": {            "capabilities": {                "card_payments": {                    "requested": true                }            }        }    },    "defaults": {        "responsibilities": {            "fees_collector": "stripe",            "losses_collector": "stripe"        }    },    "dashboard": "full",    "include": [        "configuration.merchant",        "configuration.customer",        "identity",        "defaults"    ]  }'
```

Example 4 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "contact_email": "furever@example.com",    "display_name": "Furever",    "identity": {        "country": "us",        "entity_type": "company",        "business_details": {            "registered_name": "Furever"        }    },    "configuration": {        "customer": {            "capabilities": {                "automatic_indirect_tax": {                    "requested": true                }            }        },        "merchant": {            "capabilities": {                "card_payments": {                    "requested": true                }            }        }    },    "defaults": {        "responsibilities": {            "fees_collector": "stripe",            "losses_collector": "stripe"        }    },    "dashboard": "full",    "include": [        "configuration.merchant",        "configuration.customer",        "identity",        "defaults"    ]  }'
```

---

## Choose your onboarding configuration

**URL:** https://docs.stripe.com/connect/onboarding

**Contents:**
- Choose your onboarding configuration
- Learn about the different options for onboarding your connected accounts.
- Stripe-hosted onboarding
- Embedded onboarding
- API onboarding

Stripe offers several different onboarding options:

Choose the onboarding option that best fits your business. We recommend using Stripe-hosted onboarding or Embedded onboarding. These options automatically update to handle changing requirements when they apply to a connected account.

Stripe-hosted onboarding is a web form hosted by Stripe with your brand’s name, color, and icon, and is localized for all Stripe-supported countries. Stripe-hosted onboarding uses the Accounts API to read an account’s requirements and generate a custom guided flow. It lets the account user upload documents and applies data validation, including real-time verification when possible.

Additionally, Stripe-hosted onboarding lets existing connected accounts update their business type or previously submitted details.

Stripe-hosted onboarding with Accounts v1 supports networked onboarding, which allows owners of multiple Stripe accounts to share certain types of business information between them. When they onboard an account, they can reuse that information from an existing account instead of resubmitting it.

Use Stripe-hosted onboarding if you want Stripe to handle onboarding and reduce the amount of effort for your platform.

See Stripe-hosted onboarding to learn more.

Embedded onboarding is a themeable onboarding UI with limited Stripe branding, and it’s localized for all Stripe-supported countries. Your platform embeds the Account onboarding component in your application, and your connected accounts interact with the embedded component without leaving your application. Embedded onboarding uses the Accounts API to read an account’s requirements and generate a custom guided flow. It lets the account user upload documents and applies data validation, including real-time verification when possible.

Additionally, Embedded onboarding lets existing connected accounts update their business type or previously submitted details.

Embedded onboarding with Accounts v1 supports networked onboarding, which allows owners of multiple Stripe accounts to share certain types of business information between them. When they onboard an account, they can reuse that information from an existing account instead of resubmitting it.

With embedded onboarding, you get a customized onboarding flow and don’t need to update your onboarding integration as compliance requirements change.

See Embedded onboarding to learn more.

You use the Accounts API to build an onboarding flow and handle identity verification, localization, and error handling for each country your connected accounts onboard in. Your platform is responsible for all interactions with your connected accounts and for collecting all the information needed to verify each account. You must plan on reviewing and updating onboarding requirements at least every 6 months.

We don’t recommend this option unless you’re committed to the operational complexity required to build and maintain an API onboarding flow. For a customized onboarding flow, use embedded onboarding.

See API onboarding to learn more.

---

## List accounts v2

**URL:** https://docs.stripe.com/api/v2/core/accounts/list

**Contents:**
- List accounts v2
  - Parameters
    - applied_configurationsarray of enums
    - closedboolean
    - limitinteger
    - pagestring
  - Returns
  - Response attributes
    - dataarray of objects
    - next_page_urlnullable string

Returns a list of Accounts.

Filter only accounts that have all of the configurations specified. If omitted, returns all accounts regardless of which configurations they have.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Filter by whether the account is closed. If omitted, returns only Accounts that are not closed.

The upper limit on the number of accounts returned by the List Account request.

The page token to navigate to next or previous batch of accounts given by the list request.

A list of retrieved Account objects.

URL with page token to navigate to next batch of accounts given by the list request.

URL with page token to navigate to previous batch of accounts given by the list request.

Accounts v2 is not enabled for your platform.

Removes access to the Account and its associated resources. Closed Accounts can no longer be operated on, but limited information can still be retrieved through the API in order to be able to track their history.

The ID of the Account to close.

Configurations on the Account to be closed. All configurations on the Account must be passed in for this request to succeed.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Unique identifier for the Account.

String representing the object’s type. Objects of the same type share the same value of the object field.

The configurations that have been applied to this account.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Indicates whether the account has been closed.

An Account represents a company, individual, or other entity that a user interacts with. Accounts store identity information and one or more configurations that enable product-specific capabilities. You can assign configurations at creation or add them later.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values for settings shared across Account configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the future requirements for the Account that will eventually come into effect, including what information needs to be collected, and by when.

Information about the company, individual, and business represented by the Account.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the active requirements for the Account, including what information needs to be collected, and by when.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

Account with Merchant or Recipient configuration with transfers feature cannot be closed because the account has a cash balance.

Account with Customer configuration cannot be closed because the customer has a cash balance.

Account cannot be closed without specifying the right configurations.

Account cannot be closed due to other pending resources.

Platform has not signed up for Connect and cannot create connected accounts.

Account with Stripe-owned loss liability and dashboard cannot be deleted.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

The resource wasn’t found.

This is a list of all public thin events we currently send for updates to Account, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v2/core/accounts \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  -d limit=2 \  -d "applied_configurations[0]"=customer
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v2/core/accounts \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  -d limit=2 \  -d "applied_configurations[0]"=customer
```

Example 3 (unknown):
```unknown
{  "data": [    {      "id": "acct_1QP3oLBUFVXWiKFB",      "object": "v2.core.account",      "applied_configurations": [        "customer"      ],      "contact_email": "jenny.rosen@example.com",      "created": "2024-11-25T15:02:50.000Z",      "display_name": "Jenny Rosen",      "livemode": true,      "metadata": {}    },    {      "id": "acct_1QO24tPeVxUa6gV6",      "object": "v2.core.account",      "applied_configurations": [        "recipient",        "customer",        "merchant"      ],      "contact_email": "jenny.rosen@example.com",      "created": "2024-11-22T18:59:45.000Z",      "dashboard": "none",      "display_name": "Jenny Rosen 2",      "livemode": true,      "metadata": {        "my_key": "my_value"      }    }  ],  "next_page_url": "/v2/core/accounts?page=page_5dr8SFDbv7rZ2aj4ZSGuf4J1Dv58yE0YM4BhBqb2tg94CD5PDoUA7RD2AE7VBEH5C0E0qGJi1wMFPf9MEBbh6M125&limit=2&applied_configurations=customer"}
```

Example 4 (unknown):
```unknown
{  "data": [    {      "id": "acct_1QP3oLBUFVXWiKFB",      "object": "v2.core.account",      "applied_configurations": [        "customer"      ],      "contact_email": "jenny.rosen@example.com",      "created": "2024-11-25T15:02:50.000Z",      "display_name": "Jenny Rosen",      "livemode": true,      "metadata": {}    },    {      "id": "acct_1QO24tPeVxUa6gV6",      "object": "v2.core.account",      "applied_configurations": [        "recipient",        "customer",        "merchant"      ],      "contact_email": "jenny.rosen@example.com",      "created": "2024-11-22T18:59:45.000Z",      "dashboard": "none",      "display_name": "Jenny Rosen 2",      "livemode": true,      "metadata": {        "my_key": "my_value"      }    }  ],  "next_page_url": "/v2/core/accounts?page=page_5dr8SFDbv7rZ2aj4ZSGuf4J1Dv58yE0YM4BhBqb2tg94CD5PDoUA7RD2AE7VBEH5C0E0qGJi1wMFPf9MEBbh6M125&limit=2&applied_configurations=customer"}
```

---

## Bank Accounts

**URL:** https://docs.stripe.com/api/customer_bank_accounts

**Contents:**
- Bank Accounts
- The Bank Account object
  - Attributes
    - idstring
    - account_holder_namenullable string
    - account_holder_typenullable string
    - bank_namenullable string
    - countrystring
    - currencyenum
    - customernullable stringExpandable

These bank accounts are payment methods on Customer objects.

On the other hand External Accounts are transfer destinations on Account objects for connected accounts. They can be bank accounts or debit cards as well, and are documented in the links above.

Related guide: Bank debits and transfers

Unique identifier for the object.

The name of the person or business that owns the bank account.

The type of entity that holds the account. This can be either individual or company.

Name of the bank associated with the routing number (e.g., WELLS FARGO).

Two-letter ISO code representing the country the bank account is located in.

Three-letter ISO code for the currency paid out to the bank account.

The ID of the customer that the bank account is associated with.

Uniquely identifies this particular bank account. You can use this attribute to check whether two bank accounts are the same.

The last four digits of the bank account number.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The routing transit number for the bank account.

When you create a new bank account, you must specify a Customer object on which to create it.

Either a token, like the ones returned by Stripe.js, or a dictionary containing a user’s bank account details (with the options shown below).

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the bank account object.

Updates the account_holder_name, account_holder_type, and metadata of a bank account belonging to a customer. Other bank account details are not editable, by design.

The name of the person or business that owns the bank account.

The type of entity that holds the account. This can be either individual or company.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the bank account object.

By default, you can see the 10 most recent sources stored on a Customer directly on the object, but you can also retrieve details about a specific bank account stored on the Stripe account.

Returns the bank account object.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "ba_1MvoIJ2eZvKYlo2CO9f0MabO",  "object": "bank_account",  "account_holder_name": "Jane Austen",  "account_holder_type": "company",  "account_type": null,  "bank_name": "STRIPE TEST BANK",  "country": "US",  "currency": "usd",  "customer": "cus_9s6XI9OFIdpjIg",  "fingerprint": "1JWtPxqbdX5Gamtc",  "last4": "6789",  "metadata": {},  "routing_number": "110000000",  "status": "new"}
```

Example 2 (unknown):
```unknown
{  "id": "ba_1MvoIJ2eZvKYlo2CO9f0MabO",  "object": "bank_account",  "account_holder_name": "Jane Austen",  "account_holder_type": "company",  "account_type": null,  "bank_name": "STRIPE TEST BANK",  "country": "US",  "currency": "usd",  "customer": "cus_9s6XI9OFIdpjIg",  "fingerprint": "1JWtPxqbdX5Gamtc",  "last4": "6789",  "metadata": {},  "routing_number": "110000000",  "status": "new"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/customers/cus_9s6XI9OFIdpjIg/sources \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d source=btok_1MvoS32eZvKYlo2CDhGTErAe
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/customers/cus_9s6XI9OFIdpjIg/sources \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d source=btok_1MvoS32eZvKYlo2CDhGTErAe
```

---

## Cancel a payout

**URL:** https://docs.stripe.com/api/payouts/cancel

**Contents:**
- Cancel a payout
  - Parameters
  - Returns
- Reverse a payout
  - Parameters
    - metadataobject
  - Returns

You can cancel a previously created payout if its status is pending. Stripe refunds the funds to your available balance. You can’t cancel automatic Stripe payouts.

Returns the payout object if the cancellation succeeds. Returns an error if the payout is already canceled or can’t be canceled.

Reverses a payout by debiting the destination bank account. At this time, you can only reverse payouts for connected accounts to US and Canadian bank accounts. If the payout is manual and in the pending status, use /v1/payouts/:id/cancel instead.

By requesting a reversal through /v1/payouts/:id/reverse, you confirm that the authorized signatory of the selected bank account authorizes the debit on the bank account and that no other authorization is required.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the reversing payout object if the reversal is successful. Returns an error if the payout is already reversed or can’t be reversed.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/payouts/po_1OaFDbEcg9tTZuTgNYmX0PKB/cancel \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/payouts/po_1OaFDbEcg9tTZuTgNYmX0PKB/cancel \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "po_1OaFDbEcg9tTZuTgNYmX0PKB",  "object": "payout",  "amount": 1100,  "arrival_date": 1680652800,  "automatic": false,  "balance_transaction": "txn_1OaFDcEcg9tTZuTgYMR25tSe",  "created": 1680648691,  "currency": "usd",  "description": null,  "destination": "ba_1MtIhL2eZvKYlo2CAElKwKu2",  "failure_balance_transaction": "txn_1OaFJKEcg9tTZuTg2RdsWQhi",  "failure_code": null,  "failure_message": null,  "livemode": false,  "metadata": {},  "method": "standard",  "original_payout": null,  "reconciliation_status": "not_applicable",  "reversed_by": null,  "source_type": "card",  "statement_descriptor": null,  "status": "canceled",  "type": "bank_account"}
```

Example 4 (unknown):
```unknown
{  "id": "po_1OaFDbEcg9tTZuTgNYmX0PKB",  "object": "payout",  "amount": 1100,  "arrival_date": 1680652800,  "automatic": false,  "balance_transaction": "txn_1OaFDcEcg9tTZuTgYMR25tSe",  "created": 1680648691,  "currency": "usd",  "description": null,  "destination": "ba_1MtIhL2eZvKYlo2CAElKwKu2",  "failure_balance_transaction": "txn_1OaFJKEcg9tTZuTg2RdsWQhi",  "failure_code": null,  "failure_message": null,  "livemode": false,  "metadata": {},  "method": "standard",  "original_payout": null,  "reconciliation_status": "not_applicable",  "reversed_by": null,  "source_type": "card",  "statement_descriptor": null,  "status": "canceled",  "type": "bank_account"}
```

---

## Account capabilities and configurations

**URL:** https://docs.stripe.com/connect/account-capabilities

**Contents:**
- Account capabilities and configurations
- Learn about capabilities you can enable for accounts, the account configurations they belong to, and their requirements.
    - Testing capabilities
    - Note
- Supported capabilities
  - Transfers
  - Card payments
  - US tax reporting
  - Payment methods
  - India international payments

Capabilities represent functionality that you can request for your connected accounts, such as accepting card payments or receiving transferred funds from your platform account. A capability must be active for a connected account to perform actions associated with that capability.

Sandboxes and test mode might not enforce some capabilities. In certain cases, they can allow an account to perform capability-dependent actions even when the associated capability’s status isn’t active.

Most capabilities require verification of certain information about the connected account’s business before Stripe enables them for that account. The capabilities you request for a connected account determine the information you’re required to collect for that account. To reduce onboarding effort, only request the capabilities that your accounts need. Requesting more capabilities means the onboarding flow must verify more information.

You can start by completing the platform profile to understand which capabilities might be appropriate for your platform.

For some capabilities, requesting them enables them permanently. Attempting to remove or unrequest a permanent capability returns an error.

After creating an account, you can request additional capabilities and remove existing non-permanent capabilities. For connected accounts that other platforms control, you can’t unrequest capabilities.

Following is a list of available capabilities. Click an item to expand or collapse it.

Requesting multiple capabilities for a connected account is common, but involves the following considerations:

Capabilities also allow you to collect information for multiple purposes at the same time. For example, you can collect both required tax information and the information required for a requested capability.

Capabilities are set on the Account object. To get the list of available capabilities for an Account, use the list_capabilities endpoint.

Account creation and requesting capabilities differ for connected accounts in different configurations.

Information requirements vary depending on the capability, but they often relate to identity verification or other information specific to a payment type.

When your connected account is successfully created, you can retrieve a list of its requirements:

In the response, the requirements hash specifies the required information. The values for payouts_enabled and charges_enabled indicate whether payouts and charges are enabled for the account.

The following sections describe how to preview information requirements or manage capabilities for existing connected accounts using the Capabilities API.

You can preview what information is needed from your connected account for a particular capability either before or after that capability has been requested.

When you request capabilities, account.updated webhooks fire and the account’s requirements can change. To enable a requirement faster and avoid disabling the account, preview the requirements and collect any required information before requesting the capability.

The following example lists the requirements for the card_payments capability for a specific account.

In the response, check the requirements hash to see what information is needed:

The value for status identifies whether the capability has been requested. When the value is requested, the account’s requirements are active.

In addition to previewing a capability’s requirements before requesting it, you can use the same endpoint to view a capability’s current requirements. That can help you stay informed when requirements change.

To request a capability for an account, set the capability’s requested value to true by updating the account. If the request succeeds, the API returns requested: true in the response.

To unrequest a capability for an account, set the capability’s requested value to false by updating the account. If the capability can’t be removed, the call returns an error. If the call succeeds, the API returns requested: false in the response.

You can also request and remove an account’s capabilities from the Dashboard. If a capability can’t be removed, its Remove button is disabled.

The example below requests the transfers capability for a specific connected account:

The example below requests multiple capabilities for a specific connected account:

Capabilities described in the following sections are deprecated. If possible, don’t request them for new accounts. If you have existing accounts that use deprecated capabilities, we recommend that you update them to use other capabilities instead.

The legacy_payments capability enables charges, payouts, and transfers. Newer accounts enable those actions using the card_payments and transfers capabilities, which support more flexible configurations.

We recommend that you take the following steps:

Update your connected account onboarding process to request the appropriate combination of card_payments and transfers instead of legacy_payments.

Update your existing connected accounts to request the appropriate combination of card_payments and transfers.

Update any code that checks the status of legacy_payments to check the status of either legacy_payments or the appropriate new capability. For example, update code that relies on an account’s ability to make card payments to run when either legacy_payments or card_payments is active. Similarly, update code that relies on an account’s ability to accept transfers to run when either legacy_payments or transfers is active. The updated code works throughout the process of transitioning to the new capabilities, regardless of when the new capabilities become active.

After the new capabilities are active for all of your connected accounts, remove references to legacy_payments from your code.

You can’t unrequest the legacy_payments capability. Stripe will notify you in advance before we remove it.

If you do business in Canada, Stripe automatically requests card_payments and transfers for your accounts that use legacy_payments, to comply with updated requirements. During the process, you might see the following values in your connected accounts’ API responses.

During the transition, card_payments and transfers requirements might appear in past_due. However, if legacy_payments is active, then charges, transfers, and payouts remain enabled.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/accounts \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d "controller[fees][payer]"=application \
  -d "controller[losses][payments]"=application \
  -d "controller[stripe_dashboard][type]"=none \
  -d "controller[requirement_collection]"=application \
  -d country=US \
  -d "capabilities[card_payments][requested]"=true \
  -d "capabilities[transfers][requested]"=true
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/accounts \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d "controller[fees][payer]"=application \
  -d "controller[losses][payments]"=application \
  -d "controller[stripe_dashboard][type]"=none \
  -d "controller[requirement_collection]"=application \
  -d country=US \
  -d "capabilities[card_payments][requested]"=true \
  -d "capabilities[transfers][requested]"=true
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/accounts/{{CONNECTED_ACCOUNT_ID}} \
  -u "sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/accounts/{{CONNECTED_ACCOUNT_ID}} \
  -u "sk_test_YOUR_TEST_KEY_HERE:"
```

---

## Retrieve a person token v2

**URL:** https://docs.stripe.com/api/v2/core/accounts/retrieve-person-token

**Contents:**
- Retrieve a person token v2
  - Parameters
    - account_idstringRequired
    - idstringRequired
  - Returns
  - Response attributes
    - idstring
    - objectstring, value is "v2.core.account_person_token"
    - createdtimestamp
    - expires_attimestamp

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
curl https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/person_tokens/perstok_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/person_tokens/perstok_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 3 (unknown):
```unknown
{  "id": "perstok_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_person_token",  "created": "2025-11-17T14:00:00.000Z",  "expires_at": "2025-11-17T14:10:00.000Z",  "livemode": true,  "used": true}
```

Example 4 (unknown):
```unknown
{  "id": "perstok_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_person_token",  "created": "2025-11-17T14:00:00.000Z",  "expires_at": "2025-11-17T14:10:00.000Z",  "livemode": true,  "used": true}
```

---

## Monitor readers

**URL:** https://docs.stripe.com/terminal/fleet/monitor-readers

**Contents:**
- Monitor readers
- Access real-time status and insights for your Stripe Terminal devices.
- Readers list
- Reader details
  - Reader events Public preview
    - Note

You can monitor and track the performance, health, and operational data of your Stripe Terminal devices using the Stripe Dashboard.

Use the Readers list in the Stripe Dashboard to view all registered readers in your account. You can apply filters to view a subset of your readers. Additionally, you can export this list for use outside of Stripe.

For platforms or marketplaces using Terminal with Connect, if you use direct charges with readers owned by connected accounts, you must log in as a connected account to view the list of its readers.

The Reader details page displays information about a particular terminal device. To open it, click the reader in the Readers list.

The reader information section includes the following details:

The device connectivity information section includes the following details:

Learn more about network requirements and troubleshooting at Terminal network requirements.

The page also displays a summary of recent payments processed by the reader, including details about successful payments and any errors. You can’t filter or export this summary. You can use the Transactions page to view all your customer payments, including the Terminal location and Terminal reader that processed each transaction. You can filter and export this transactions list.

The reader event log displays the last 30 days of events related to the reader, such as software updates, network disconnections, and boot-ups. Events can take several minutes to appear in the log.

Your account level time zone setting determines the reader event time zone.

The following table describes the reader events that can appear in the log, including their types and sub-types.

---

## Connect and the Accounts v2 API

**URL:** https://docs.stripe.com/connect/accounts-v2

**Contents:**
- Connect and the Accounts v2 API
- Create connected accounts with a unified identity across Stripe.
- Accounts v2 API
- Represent connected accounts using Accounts v2
    - API v2 response structure
- Use Accounts as customers
- Connect platforms using Accounts v1 and Customers v1
- Considerations

As a Connect platform, you enable your connected accounts to accept payments. You can also accept payments from your connected accounts when they purchase products or subscribe to your services. In the Accounts v1 API, associating these purchases and subscriptions with your connected account requires a separate Customer object that you manually associate with the connected account’s Account object.

The Accounts v2 API allows you to create one Account object that supports all interactions with your connected account, so you don’t need to create and track separate Customer objects.

The Accounts v2 API provides:

In the Accounts v2 API, you assign one or more configurations to an Account to enable different functionality. For example:

The following example creates an Account using API v2. Notice that the structure of the Account object differs from the structure of an Account object in API v1.

By default, Accounts v2 API calls return values for certain properties and null for other properties, regardless of their actual values. To retrieve additional property values, request them using the include parameter.

In the v1 API, you must create an Account object for a connected account to accept payments, and a separate Customer object to associate that same business with payments they make to your platform. Accounts v1 and Customers v1 have no explicit relationship, so you must manage those objects separately and maintain a map of Account IDs to Customer IDs.

Any API that accepts a customer parameter also accepts a customer_account parameter where you can pass a customer-configured Account ID.

Learn more about using Accounts as customers.

Stripe still supports the Accounts v1 and Customers v1 APIs. However, you can use the Accounts v2 API to manage Accounts created using the Accounts v1 API, including assigning them the customer configuration.

Stripe discourages indefinitely maintaining both Accounts API versions simultaneously. Continue using the v1 APIs if your platform:

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts \
  -H "Authorization: Bearer sk_test_YOUR_TEST_KEY_HERE" \
  -H "Stripe-Version: 2025-09-30.preview" \
  --json '{
    "contact_email": "jenny.rosen@example.com",
    "display_name": "Jenny Rosen",
    "dashboard": "full",
    "identity": {
        "business_details": {
            "registered_name": "Furever"
        },
        "country": "us",
        "entity_type": "company"
    },
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
    },
    "defaults": {
        "currency": "usd",
        "responsibilities": {
            "fees_collector": "stripe",
            "losses_collector": "stripe"
        },
        "locales": [
            "en-US"
        ]
    },
    "include": [
        "configuration.customer",
        "configuration.merchant",
        "identity",
        "requirements"
    ]
  }'
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts \
  -H "Authorization: Bearer sk_test_YOUR_TEST_KEY_HERE" \
  -H "Stripe-Version: 2025-09-30.preview" \
  --json '{
    "contact_email": "jenny.rosen@example.com",
    "display_name": "Jenny Rosen",
    "dashboard": "full",
    "identity": {
        "business_details": {
            "registered_name": "Furever"
        },
        "country": "us",
        "entity_type": "company"
    },
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
    },
    "defaults": {
        "currency": "usd",
        "responsibilities": {
            "fees_collector": "stripe",
            "losses_collector": "stripe"
        },
        "locales": [
            "en-US"
        ]
    },
    "include": [
        "configuration.customer",
        "configuration.merchant",
        "identity",
        "requirements"
    ]
  }'
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/accounts \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d country=US \
  -d "controller[fees][payer]"=application \
  -d "controller[losses][payments]"=application \
  -d "controller[stripe_dashboard][type]"=express
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/accounts \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d country=US \
  -d "controller[fees][payer]"=application \
  -d "controller[losses][payments]"=application \
  -d "controller[stripe_dashboard][type]"=express
```

---

## Connected Accounts

**URL:** https://docs.stripe.com/api/connected-accounts

**Contents:**
- Connected Accounts
- Versioning

If you use Stripe Connect, you can issue requests on behalf of your connected accounts. To act as a connected account, include a Stripe-Account header containing the connected account ID, which typically starts with the acct_ prefix.

The connected account ID is set per-request. Methods on the returned object reuse the same account ID.

Each major release, such as Acacia, includes changes that aren’t backward-compatible with previous releases. Upgrading to a new major release can require updates to existing code. Each monthly release includes only backward-compatible changes, and uses the same name as the last major release. You can safely upgrade to a new monthly release without breaking any existing code. The current version is 2025-12-15.clover. For information on all API versions, view our API changelog.

You can upgrade your API version in Workbench. As a precaution, use API versioning to test a new API version before committing to an upgrade.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/charges/ch_3LmjFA2eZvKYlo2C09TLIsrw \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -H "Stripe-Account: acct_1032D82eZvKYlo2C" \  -G
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/charges/ch_3LmjFA2eZvKYlo2C09TLIsrw \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -H "Stripe-Account: acct_1032D82eZvKYlo2C" \  -G
```

---

## Reverse a payout

**URL:** https://docs.stripe.com/api/payouts/reverse

**Contents:**
- Reverse a payout
  - Parameters
    - metadataobject
  - Returns

Reverses a payout by debiting the destination bank account. At this time, you can only reverse payouts for connected accounts to US and Canadian bank accounts. If the payout is manual and in the pending status, use /v1/payouts/:id/cancel instead.

By requesting a reversal through /v1/payouts/:id/reverse, you confirm that the authorized signatory of the selected bank account authorizes the debit on the bank account and that no other authorization is required.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the reversing payout object if the reversal is successful. Returns an error if the payout is already reversed or can’t be reversed.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/payouts/po_1OaFDbEcg9tTZuTgNYmX0PKB/reverse \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v1/payouts/po_1OaFDbEcg9tTZuTgNYmX0PKB/reverse \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 3 (unknown):
```unknown
{  "id": "po_1Oj6B8rU4sY9X3L2mQ6T5fZ1",  "object": "payout",  "amount": -1100,  "arrival_date": 1680652800,  "automatic": false,  "balance_transaction": "txn_1O5G7H8k1p2Q9a6c0N8elkI0",  "created": 1680648691,  "currency": "usd",  "description": null,  "destination": "ba_1MtIhL2eZvKYlo2CAElKwKu2",  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "livemode": false,  "metadata": {},  "method": "standard",  "original_payout": "po_1OaFDbEcg9tTZuTgNYmX0PKB",  "reconciliation_status": "not_applicable",  "reversed_by": null,  "source_type": "card",  "statement_descriptor": null,  "status": "pending",  "type": "bank_account"}
```

Example 4 (unknown):
```unknown
{  "id": "po_1Oj6B8rU4sY9X3L2mQ6T5fZ1",  "object": "payout",  "amount": -1100,  "arrival_date": 1680652800,  "automatic": false,  "balance_transaction": "txn_1O5G7H8k1p2Q9a6c0N8elkI0",  "created": 1680648691,  "currency": "usd",  "description": null,  "destination": "ba_1MtIhL2eZvKYlo2CAElKwKu2",  "failure_balance_transaction": null,  "failure_code": null,  "failure_message": null,  "livemode": false,  "metadata": {},  "method": "standard",  "original_payout": "po_1OaFDbEcg9tTZuTgNYmX0PKB",  "reconciliation_status": "not_applicable",  "reversed_by": null,  "source_type": "card",  "statement_descriptor": null,  "status": "pending",  "type": "bank_account"}
```

---

## Platforms and marketplaces with Stripe Connect

**URL:** https://docs.stripe.com/connect

**Contents:**
- Platforms and marketplaces with Stripe Connect
- Build a SaaS platform or marketplace with Connect.
- Build a SaaS platform or marketplace
- Manage your connected accounts
- Process payments
- Platform administration
- More resources

Use Connect to build a platform, marketplace, or other business that manages payments and moves money between multiple parties.

Provide platform services to businesses that collect payments from their own customers.

Collect payments from customers and automatically pay out a portion to sellers or service providers on your marketplace.

Create a unified identity to represent each of your platform’s connected accounts with one or more configurations, such as merchant or customer.

Learn about the different options for onboarding your connected accounts.

Enable capabilities for your connected accounts.

Learn what information you need to collect and verify for each connected account.

Create a charge and split payments between your platform and your sellers or service providers.

Learn about platform and connected account balances.

Manage payouts and external accounts for your connected accounts.

Set platform processing fees for your connected accounts.

Review and take action on your connected accounts.

Calculate, collect, and report taxes for your platform or connected accounts.

Learn how to use Stripe Radar to identify fraud in Connect account charges.

Add connected account dashboard functionality to your website and mobile applications.

---

## Balance Settings

**URL:** https://docs.stripe.com/api/balance-settings

**Contents:**
- Balance Settings
- The Balance Setting object
  - Attributes
    - objectstring
    - paymentsobject
- Update balance settings
  - Parameters
    - paymentsobject
  - Returns
- Retrieve balance settings

Options for customizing account balances and payout settings for a Stripe platform’s connected accounts.

String representing the object’s type. Objects of the same type share the same value.

Settings that apply to the Payments Balance.

Updates balance settings for a given connected account. Related guide: Making API calls for connected accounts

Settings that apply to the Payments Balance.

Returns the updated balance settings object for the account that was authenticated in the request.

Retrieves balance settings for a given connected account. Related guide: Making API calls for connected accounts

Returns a balance settings object for the account specified in the request.

**Examples:**

Example 1 (unknown):
```unknown
{  "object": "balance_settings",  "payments": {    "debit_negative_balances": true,    "payouts": {      "minimum_balance_by_currency": {        "usd": 1500,        "cad": 8000      },      "schedule": {        "interval": "weekly",        "weekly_payout_days": [          "monday",          "wednesday"        ]      },      "statement_descriptor": null,      "status": "enabled"    },    "settlement_timing": {      "delay_days_override": 3,      "delay_days": 3    }  }}
```

Example 2 (unknown):
```unknown
{  "object": "balance_settings",  "payments": {    "debit_negative_balances": true,    "payouts": {      "minimum_balance_by_currency": {        "usd": 1500,        "cad": 8000      },      "schedule": {        "interval": "weekly",        "weekly_payout_days": [          "monday",          "wednesday"        ]      },      "statement_descriptor": null,      "status": "enabled"    },    "settlement_timing": {      "delay_days_override": 3,      "delay_days": 3    }  }}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/balance_settings \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -H "Stripe-Account: {{CONNECTED_ACCOUNT_ID}}" \  -d "payments[payouts][schedule][interval]"=monthly \  -d "payments[payouts][schedule][monthly_payout_days][]"=5 \  -d "payments[payouts][schedule][monthly_payout_days][]"=20
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/balance_settings \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -H "Stripe-Account: {{CONNECTED_ACCOUNT_ID}}" \  -d "payments[payouts][schedule][interval]"=monthly \  -d "payments[payouts][schedule][monthly_payout_days][]"=5 \  -d "payments[payouts][schedule][monthly_payout_days][]"=20
```

---

## Create an account v2

**URL:** https://docs.stripe.com/api/v2/core/accounts/create

**Contents:**
- Create an account v2
  - Parameters
    - account_tokenstring
    - configurationobject
    - contact_emailstring
    - dashboardenum
    - defaultsobject
    - display_namestring
    - identityobject
    - includearray of enums

An Account is a representation of a company, individual or other entity that a user interacts with. Accounts contain identifying information about the entity, and configurations that store the features an account has access to. An account can be configured as any or all of the following configurations: Customer, Merchant and/or Recipient.

The account token generated by the account token api.

An Account Configuration which allows the Account to take on a key persona across Stripe products.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values to be used on Account Configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the company, individual, and business represented by the Account.

Additional fields to include in the response.

Include parameter to expose configuration.customer on an Account.

Include parameter to expose configuration.merchant on an Account.

Include parameter to expose configuration.recipient on an Account.

Include parameter to expose defaults on an Account.

Include parameter to expose future_requirements on an Account.

Include parameter to expose identity on an Account.

Include parameter to expose requirements on an Account.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Unique identifier for the Account.

String representing the object’s type. Objects of the same type share the same value of the object field.

The configurations that have been applied to this account.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Indicates whether the account has been closed.

An Account represents a company, individual, or other entity that a user interacts with. Accounts store identity information and one or more configurations that enable product-specific capabilities. You can assign configurations at creation or add them later.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values for settings shared across Account configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the future requirements for the Account that will eventually come into effect, including what information needs to be collected, and by when.

Information about the company, individual, and business represented by the Account.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the active requirements for the Account, including what information needs to be collected, and by when.

Requested capability is not available.

If dashboard is express, fees_collector must be application and losses_collector must be application.

If losses_collector is application, fees_collector must also be application.

Connect integration combination is not supported when UA beta is enabled.

Connect integration combination is not supported when UA beta is disabled.

Responsibility combinations is not supported in private preview.

Currency is not allowed for the account’s country.

Platform must be activated to create connected accounts.

Account creation is invalid.

Account creation error - liability unacknowledged.

Account creation error - requirement collection and liability unacknowledged.

Account creation error - requirement collection unacknowledged.

Terms of service must be accepted before adding merchant configuration.

Account token required for platforms in mandated countries (e.g., France).

Accounts v2 is not enabled for your platform.

Invalid characters are provided for address fields.

Address country doesn’t match identity country.

Address postal code is invalid.

Address state is invalid.

Address town is invalid.

Creating accounts with the BGN currency is no longer supported, as Bulgaria is now using the Euro as of 2026-01-01.

Dormant accounts cannot create accounts where requirements collector is application (this is an account takeover prevention measure).

Platform is in an invalid state and cannot create connected accounts.

Platform is in a rejected state and cannot create connected accounts.

Feature cannot be unrequested due to being a requirement for another feature.

Feature cannot be requested for the dashboard type.

Requested feature is not available for the entity type in your country.

Requested capability is not available in your country.

Feature cannot be requested given the platform’s country.

Requested feature is not available without also requesting a different feature.

Requested feature is not available without also requesting a different feature in your country.

Cannot create an account with an invalid configuration.

Platform is not verified and cannot create connected accounts.

Platform has not completed platform questionnaire and cannot create connected accounts.

Cross-border connected account creation is not allowed for this platform/account country combination.

Custom accounts cannot be created in certain countries.

Representative date of birth does not meet the age limit.

Representative date of birth is provided an invalid date or a future date.

Cannot change defaults.currency post account activation.

Default payment method provided for a customer does not exist or is otherwise invalid.

Specified payment method exists but its type is not allowed to be the default payment method.

Directorship declaration is not allowed during account creation.

Provided file tokens for documents are invalid, not found, deleted, or belong to a different account.

Provided file tokens for documents are of the wrong purpose.

Email contains unsupported domain.

Incorrect email is provided.

The identity.entity_type value is not supported in a given identity.country.

NONE is combined with another value in the HighRiskActivities list.

Provided ID number is of the wrong format for the given type.

The identity.country value is required but not provided.

Incorrect ID number is provided for a country.

The incorrect token type is provided .

ID number is provided that is not permitted for the Identity’s entity type and business structure.

The identity.business_details.id_numbers.registrar value is an invalid DE registrar.

Konbini Payments Support Hours is Invalid.

Konbini Payments Support Phone Number is Invalid.

Invoice rendering template does not exist or is otherwise invalid.

Invalid IP address is provided.

MCC is invalid for configuration.merchant.mcc.

Kana Kanji script addresses must have JP country.

Ownership declaration is not allowed during account creation.

Parameter cannot be passed alongside account_token.

Error returned when relationship.owner is set to true but the ownership percentage is set to 0%.

Phone number is invalid.

Platform has not signed up for Connect and cannot create connected accounts.

Postal code is required for Japanese addresses.

PurposeOfFundsDescription is not empty while PurposeOfFunds is not OTHER.

Provided script characters are invalid for the script.

Shipping address is required within the shipping hash.

Shipping name is required within the shipping hash.

Statement descriptor is invalid.

The business_details.structure value is not valid for identity.country and identity.entity_type.

Cannot set a test clock on a livemode customer.

Test clock does not exist or is otherwise invalid.

Cannot modify a test clock that is currently advancing.

Cannot add customer to a test clock that has already reached its customer limit.

The token is re-used with a different idempotency key.

TOS cannot be accepted on behalf of accounts when requirement collection is stripe.

Cannot set responsibilities on the current configurations.

Cannot set identity fields when the Account is only configured as a customer.

Address is in an unsupported postal code.

Address is in an unsupported state.

A v1 token ID is passed in v2 APIs.

Invalid account token.

An idempotent retry occurred with different request parameters.

Updates the details of an Account.

The ID of the Account to update.

The account token generated by the account token api.

An Account Configuration which allows the Account to take on a key persona across Stripe products.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values to be used on Account Configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the company, individual, and business represented by the Account.

Additional fields to include in the response.

Include parameter to expose configuration.customer on an Account.

Include parameter to expose configuration.merchant on an Account.

Include parameter to expose configuration.recipient on an Account.

Include parameter to expose defaults on an Account.

Include parameter to expose future_requirements on an Account.

Include parameter to expose identity on an Account.

Include parameter to expose requirements on an Account.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Unique identifier for the Account.

String representing the object’s type. Objects of the same type share the same value of the object field.

The configurations that have been applied to this account.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Indicates whether the account has been closed.

An Account represents a company, individual, or other entity that a user interacts with. Accounts store identity information and one or more configurations that enable product-specific capabilities. You can assign configurations at creation or add them later.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values for settings shared across Account configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the future requirements for the Account that will eventually come into effect, including what information needs to be collected, and by when.

Information about the company, individual, and business represented by the Account.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the active requirements for the Account, including what information needs to be collected, and by when.

Requested capability is not available.

If dashboard is express, fees_collector must be application and losses_collector must be application.

If losses_collector is application, fees_collector must also be application.

Connect integration combination is not supported when UA beta is disabled.

Responsibility combinations is not supported in private preview.

Currency is not allowed for the account’s country.

Account is not yet compatible with V2 APIs.

Terms of service must be accepted before adding merchant configuration.

Account token required for platforms in mandated countries (e.g., France).

Accounts v2 is not enabled for your platform.

Invalid characters are provided for address fields.

Address country doesn’t match identity country.

Address postal code is invalid.

Address state is invalid.

Address town is invalid.

Default payment method is added to the customer config before attaching it to the account using /v1/payment_methods.

Creating accounts with the BGN currency is no longer supported, as Bulgaria is now using the Euro as of 2026-01-01.

Dormant accounts cannot create accounts where requirements collector is application (this is an account takeover prevention measure).

Cannot set automatic_indirect_tax.validate_location when initially creating a customer configuration.

Feature cannot be unrequested due to being a requirement for another feature.

Feature cannot be requested for the dashboard type.

Requested feature is not available for the entity type in your country.

Requested capability is not available in your country.

Feature cannot be requested given the platform’s country.

Requested feature is not available without also requesting a different feature.

Requested feature is not available without also requesting a different feature in your country.

Configuration cannot be deactivated.

Configuration cannot be deactivated due to a dependency with another capability.

Cannot deactivate a configuration due to another configuration depending on it.

Configuration cannot be updated while deactivated.

Cannot create an account with an invalid configuration.

Cross-border connected account creation is not allowed for this platform/account country combination.

Custom accounts cannot be created in certain countries.

Invalid customer tax location.

Representative date of birth does not meet the age limit.

Representative date of birth is provided an invalid date or a future date.

Cannot change defaults.currency post account activation.

Outbound Destination ID is invalid.

Default payment method provided for a customer does not exist or is otherwise invalid.

Provided file tokens for documents are invalid, not found, deleted, or belong to a different account.

Provided file tokens for documents are of the wrong purpose.

Duplicate person is added to an account.

Email contains unsupported domain.

Incorrect email is provided.

The identity.entity_type value is not supported in a given identity.country.

NONE is combined with another value in the HighRiskActivities list.

Provided ID number is of the wrong format for the given type.

The identity.country value is required but not provided.

Identity param has been made immutable due to the state of the account.

Incorrect ID number is provided for a country.

The incorrect token type is provided .

ID number is provided that is not permitted for the Identity’s entity type and business structure.

The identity.business_details.id_numbers.registrar value is an invalid DE registrar.

Konbini Payments Support Hours is Invalid.

Konbini Payments Support Phone Number is Invalid.

Invalid IP address is provided.

MCC is invalid for configuration.merchant.mcc.

Kana Kanji script addresses must have JP country.

Parameter cannot be passed alongside account_token.

Error returned when relationship.owner is set to true but the ownership percentage is set to 0%.

Phone number is invalid.

Postal code is required for Japanese addresses.

PurposeOfFundsDescription is not empty while PurposeOfFunds is not OTHER.

Provided script characters are invalid for the script.

Shipping address is required within the shipping hash.

Shipping name is required within the shipping hash.

Statement descriptor is invalid.

The business_details.structure value is not valid for identity.country and identity.entity_type.

Cannot set a test clock on a livemode customer.

Test clock does not exist or is otherwise invalid.

The token is re-used with a different idempotency key.

TOS cannot be accepted on behalf of accounts when requirement collection is stripe.

Total ownership percentages of all Persons on the account exceeds 100%.

Cannot set responsibilities on the current configurations.

Cannot set identity fields when the Account is only configured as a customer.

Address is in an unsupported postal code.

Address is in an unsupported state.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

A v1 token ID is passed in v2 APIs.

Invalid account token.

The resource wasn’t found.

An idempotent retry occurred with different request parameters.

Retrieves the details of an Account.

The ID of the Account to retrieve.

Additional fields to include in the response.

Include parameter to expose configuration.customer on an Account.

Include parameter to expose configuration.merchant on an Account.

Include parameter to expose configuration.recipient on an Account.

Include parameter to expose defaults on an Account.

Include parameter to expose future_requirements on an Account.

Include parameter to expose identity on an Account.

Include parameter to expose requirements on an Account.

Unique identifier for the Account.

String representing the object’s type. Objects of the same type share the same value of the object field.

The configurations that have been applied to this account.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Indicates whether the account has been closed.

An Account represents a company, individual, or other entity that a user interacts with. Accounts store identity information and one or more configurations that enable product-specific capabilities. You can assign configurations at creation or add them later.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values for settings shared across Account configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the future requirements for the Account that will eventually come into effect, including what information needs to be collected, and by when.

Information about the company, individual, and business represented by the Account.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the active requirements for the Account, including what information needs to be collected, and by when.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

The resource wasn’t found.

Returns a list of Accounts.

Filter only accounts that have all of the configurations specified. If omitted, returns all accounts regardless of which configurations they have.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Filter by whether the account is closed. If omitted, returns only Accounts that are not closed.

The upper limit on the number of accounts returned by the List Account request.

The page token to navigate to next or previous batch of accounts given by the list request.

A list of retrieved Account objects.

URL with page token to navigate to next batch of accounts given by the list request.

URL with page token to navigate to previous batch of accounts given by the list request.

Accounts v2 is not enabled for your platform.

Removes access to the Account and its associated resources. Closed Accounts can no longer be operated on, but limited information can still be retrieved through the API in order to be able to track their history.

The ID of the Account to close.

Configurations on the Account to be closed. All configurations on the Account must be passed in for this request to succeed.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Unique identifier for the Account.

String representing the object’s type. Objects of the same type share the same value of the object field.

The configurations that have been applied to this account.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Indicates whether the account has been closed.

An Account represents a company, individual, or other entity that a user interacts with. Accounts store identity information and one or more configurations that enable product-specific capabilities. You can assign configurations at creation or add them later.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values for settings shared across Account configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the future requirements for the Account that will eventually come into effect, including what information needs to be collected, and by when.

Information about the company, individual, and business represented by the Account.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the active requirements for the Account, including what information needs to be collected, and by when.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

Account with Merchant or Recipient configuration with transfers feature cannot be closed because the account has a cash balance.

Account with Customer configuration cannot be closed because the customer has a cash balance.

Account cannot be closed without specifying the right configurations.

Account cannot be closed due to other pending resources.

Platform has not signed up for Connect and cannot create connected accounts.

Account with Stripe-owned loss liability and dashboard cannot be deleted.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

The resource wasn’t found.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "contact_email": "furever@example.com",    "display_name": "Furever",    "identity": {        "country": "us",        "entity_type": "company",        "business_details": {            "registered_name": "Furever"        }    },    "configuration": {        "customer": {            "capabilities": {                "automatic_indirect_tax": {                    "requested": true                }            }        },        "merchant": {            "capabilities": {                "card_payments": {                    "requested": true                }            }        }    },    "defaults": {        "responsibilities": {            "fees_collector": "stripe",            "losses_collector": "stripe"        }    },    "dashboard": "full",    "include": [        "configuration.merchant",        "configuration.customer",        "identity",        "defaults"    ]  }'
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "contact_email": "furever@example.com",    "display_name": "Furever",    "identity": {        "country": "us",        "entity_type": "company",        "business_details": {            "registered_name": "Furever"        }    },    "configuration": {        "customer": {            "capabilities": {                "automatic_indirect_tax": {                    "requested": true                }            }        },        "merchant": {            "capabilities": {                "card_payments": {                    "requested": true                }            }        }    },    "defaults": {        "responsibilities": {            "fees_collector": "stripe",            "losses_collector": "stripe"        }    },    "dashboard": "full",    "include": [        "configuration.merchant",        "configuration.customer",        "identity",        "defaults"    ]  }'
```

Example 3 (unknown):
```unknown
{  "id": "acct_1Nv0FGQ9RKHgCVdK",  "object": "v2.core.account",  "applied_configurations": [    "customer",    "merchant"  ],  "configuration": {    "customer": {      "applied": "2025-03-28T19:59:16.000Z",      "automatic_indirect_tax": {        "exempt": "none",        "location_source": "identity_address"      },      "billing": {        "invoice": {          "next_sequence": 1,          "prefix": "5626C87C",          "custom_fields": []        }      },      "capabilities": {        "automatic_indirect_tax": {          "status": "active",          "status_details": []        }      }    },    "merchant": {      "applied": "2025-03-28T19:59:16.000Z",      "card_payments": {        "decline_on": {          "avs_failure": false,          "cvc_failure": false        }      },      "capabilities": {        "card_payments": {          "status": "active",          "status_details": []        },        "stripe_balance": {          "payouts": {            "status": "active",            "status_details": []          }        }      }    }  },  "contact_email": "furever@example.com",  "created": "2025-03-28T19:59:16.000Z",  "dashboard": "full",  "identity": {    "business_details": {      "registered_name": "Furever"    },    "country": "US",    "entity_type": "company"  },  "livemode": false,  "defaults": {    "currency": "usd",    "responsibilities": {      "fees_collector": "stripe",      "losses_collector": "stripe",      "requirements_collector": "stripe"    }  },  "display_name": "Furever"}
```

Example 4 (unknown):
```unknown
{  "id": "acct_1Nv0FGQ9RKHgCVdK",  "object": "v2.core.account",  "applied_configurations": [    "customer",    "merchant"  ],  "configuration": {    "customer": {      "applied": "2025-03-28T19:59:16.000Z",      "automatic_indirect_tax": {        "exempt": "none",        "location_source": "identity_address"      },      "billing": {        "invoice": {          "next_sequence": 1,          "prefix": "5626C87C",          "custom_fields": []        }      },      "capabilities": {        "automatic_indirect_tax": {          "status": "active",          "status_details": []        }      }    },    "merchant": {      "applied": "2025-03-28T19:59:16.000Z",      "card_payments": {        "decline_on": {          "avs_failure": false,          "cvc_failure": false        }      },      "capabilities": {        "card_payments": {          "status": "active",          "status_details": []        },        "stripe_balance": {          "payouts": {            "status": "active",            "status_details": []          }        }      }    }  },  "contact_email": "furever@example.com",  "created": "2025-03-28T19:59:16.000Z",  "dashboard": "full",  "identity": {    "business_details": {      "registered_name": "Furever"    },    "country": "US",    "entity_type": "company"  },  "livemode": false,  "defaults": {    "currency": "usd",    "responsibilities": {      "fees_collector": "stripe",      "losses_collector": "stripe",      "requirements_collector": "stripe"    }  },  "display_name": "Furever"}
```

---

## External Bank Accounts

**URL:** https://docs.stripe.com/api/external_accounts

**Contents:**
- External Bank Accounts
- The External Bank Account object
  - Attributes
    - idstring
    - accountnullable stringExpandableAvailable conditionally
    - bank_namenullable string
    - countrystring
    - currencyenum
    - default_for_currencynullable boolean
    - last4string

External bank accounts are financial accounts associated with a Stripe platform’s connected accounts for the purpose of transferring funds to or from the connected account’s Stripe balance.

Unique identifier for the object.

The account this bank account belongs to. Only applicable on Accounts (not customers or recipients) This property is only available when returned as an External Account where controller.is_controller is true.

Name of the bank associated with the routing number (e.g., WELLS FARGO).

Two-letter ISO code representing the country the bank account is located in.

Three-letter ISO code for the currency paid out to the bank account.

Whether this bank account is the default external account for its currency.

The last four digits of the bank account number.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The routing transit number for the bank account.

For bank accounts, possible values are new, validated, verified, verification_failed, tokenized_account_number_deactivated or errored. A bank account that hasn’t had any activity or validation performed is new. If Stripe can determine that the bank account exists, its status will be validated. Note that there often isn’t enough information to know (e.g., for smaller credit unions), and the validation is not always run. If customer bank account verification has succeeded, the bank account status will be verified. If the verification failed for any reason, such as microdeposit failure, the status will be verification_failed. If the status is tokenized_account_number_deactivated, the account utilizes a tokenized account number which has been deactivated due to expiration or revocation. This account will need to be reverified to continue using it for money movement. If a payout sent to this bank account fails, we’ll set the status to errored and will not continue to send scheduled payouts until the bank details are updated.

For external accounts, possible values are new, errored, verification_failed, and tokenized_account_number_deactivated. If a payout fails, the status is set to errored and scheduled payouts are stopped until account details are updated. In the US and India, if we can’t verify the owner of the bank account, we’ll set the status to verification_failed. Other validations aren’t run against external accounts because they’re only used for payouts. This means the other statuses don’t apply.

When you create a new bank account, you must specify a connected account to create it on. You can only specify connected accounts where account.controller.requirement_collection is application (includes Custom accounts).

If the bank account’s owner has no other external account in the bank account’s currency, the new bank account will become the default for that currency. However, if the owner already has a bank account for that currency, the new account will become the default only if the default_for_currency parameter is set to true.

Either a token, like the ones returned by Stripe.js, or a dictionary containing a user’s bank account details (with the options shown below).

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the bank account object

Updates the metadata, account holder name, account holder type of a bank account belonging to a connected account and optionally sets it as the default for its currency. Other bank account details are not editable by design.

You can only update bank accounts when account.controller.requirement_collection is application, which includes Custom accounts.

You can re-enable a disabled bank account by performing an update call without providing any arguments or changes.

When set to true, this becomes the default external account for its currency.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the bank account object.

By default, you can see the 10 most recent external accounts stored on a connected account directly on the object. You can also retrieve details about a specific bank account stored on the account.

Unique identifier for the external account to be retrieved.

Returns the bank account object.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "ba_1N9DrD2eZvKYlo2C58f4DaIa",  "object": "bank_account",  "account": "acct_1032D82eZvKYlo2C",  "account_holder_name": "Jane Austen",  "account_holder_type": "individual",  "account_type": null,  "available_payout_methods": [    "standard"  ],  "bank_name": "STRIPE TEST BANK",  "country": "US",  "currency": "usd",  "fingerprint": "1JWtPxqbdX5Gamtz",  "last4": "6789",  "metadata": {},  "routing_number": "110000000",  "status": "new"}
```

Example 2 (unknown):
```unknown
{  "id": "ba_1N9DrD2eZvKYlo2C58f4DaIa",  "object": "bank_account",  "account": "acct_1032D82eZvKYlo2C",  "account_holder_name": "Jane Austen",  "account_holder_type": "individual",  "account_type": null,  "available_payout_methods": [    "standard"  ],  "bank_name": "STRIPE TEST BANK",  "country": "US",  "currency": "usd",  "fingerprint": "1JWtPxqbdX5Gamtz",  "last4": "6789",  "metadata": {},  "routing_number": "110000000",  "status": "new"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/accounts/acct_1032D82eZvKYlo2C/external_accounts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d external_account=btok_1NAiJy2eZvKYlo2Cnh6bIs9c
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/accounts/acct_1032D82eZvKYlo2C/external_accounts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d external_account=btok_1NAiJy2eZvKYlo2Cnh6bIs9c
```

---

## Create a bank account token

**URL:** https://docs.stripe.com/api/tokens/create_bank_account

**Contents:**
- Create a bank account token
  - Parameters
    - bank_accountobject
  - More parametersExpand all
    - customerstringConnect only
  - Returns
- Create a card token
  - Parameters
    - cardobject | string
  - Returns

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

Creates a single-use token that represents the details of personally identifiable information (PII). You can use this token in place of an id_number or id_number_secondary in Account or Person Update API methods. You can only use a PII token once.

The PII this token represents.

Returns the created PII token if it’s successful. Otherwise, this call raises an error.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/tokens \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "bank_account[country]"=US \  -d "bank_account[currency]"=usd \  -d "bank_account[account_holder_name]"="Jenny Rosen" \  -d "bank_account[account_holder_type]"=individual \  -d "bank_account[routing_number]"=110000000 \  -d "bank_account[account_number]"=000123456789
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/tokens \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d "bank_account[country]"=US \  -d "bank_account[currency]"=usd \  -d "bank_account[account_holder_name]"="Jenny Rosen" \  -d "bank_account[account_holder_type]"=individual \  -d "bank_account[routing_number]"=110000000 \  -d "bank_account[account_number]"=000123456789
```

Example 3 (unknown):
```unknown
{  "id": "tok_1N3T00LkdIwHu7ixt44h1F8k",  "object": "token",  "bank_account": {    "id": "ba_1NWScr2eZvKYlo2C8MgV5Cwn",    "object": "bank_account",    "account_holder_name": "Jenny Rosen",    "account_holder_type": "individual",    "account_type": null,    "bank_name": "STRIPE TEST BANK",    "country": "US",    "currency": "usd",    "fingerprint": "1JWtPxqbdX5Gamtz",    "last4": "6789",    "routing_number": "110000000",    "status": "new"  },  "client_ip": null,  "created": 1689981645,  "livemode": false,  "redaction": null,  "type": "bank_account",  "used": false}
```

Example 4 (unknown):
```unknown
{  "id": "tok_1N3T00LkdIwHu7ixt44h1F8k",  "object": "token",  "bank_account": {    "id": "ba_1NWScr2eZvKYlo2C8MgV5Cwn",    "object": "bank_account",    "account_holder_name": "Jenny Rosen",    "account_holder_type": "individual",    "account_type": null,    "bank_name": "STRIPE TEST BANK",    "country": "US",    "currency": "usd",    "fingerprint": "1JWtPxqbdX5Gamtz",    "last4": "6789",    "routing_number": "110000000",    "status": "new"  },  "client_ip": null,  "created": 1689981645,  "livemode": false,  "redaction": null,  "type": "bank_account",  "used": false}
```

---

## Request IDs

**URL:** https://docs.stripe.com/api/request_ids

**Contents:**
- Request IDs
- Connected Accounts
- Versioning

Each API request has an associated request identifier. You can find this value in the response headers, under Request-Id. You can also find request identifiers in the URLs of individual request logs in your Dashboard.

To expedite the resolution process, provide the request identifier when you contact us about a specific request.

If you use Stripe Connect, you can issue requests on behalf of your connected accounts. To act as a connected account, include a Stripe-Account header containing the connected account ID, which typically starts with the acct_ prefix.

The connected account ID is set per-request. Methods on the returned object reuse the same account ID.

Each major release, such as Acacia, includes changes that aren’t backward-compatible with previous releases. Upgrading to a new major release can require updates to existing code. Each monthly release includes only backward-compatible changes, and uses the same name as the last major release. You can safely upgrade to a new monthly release without breaking any existing code. The current version is 2025-12-15.clover. For information on all API versions, view our API changelog.

You can upgrade your API version in Workbench. As a precaution, use API versioning to test a new API version before committing to an upgrade.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/customers \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -D "-" \  -X POST
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/customers \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -D "-" \  -X POST
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/charges/ch_3LmjFA2eZvKYlo2C09TLIsrw \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -H "Stripe-Account: acct_1032D82eZvKYlo2C" \  -G
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/charges/ch_3LmjFA2eZvKYlo2C09TLIsrw \  -u sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE: \  -H "Stripe-Account: acct_1032D82eZvKYlo2C" \  -G
```

---

## Account Links

**URL:** https://docs.stripe.com/api/account_links

**Contents:**
- Account Links
- The Account Link object
  - Attributes
    - expires_attimestamp
    - urlstring
  - More attributesExpand all
    - objectstring
    - createdtimestamp
- Create an account link
  - Parameters

Account Links are the means by which a Connect platform grants a connected account permission to access Stripe-hosted applications, such as Connect Onboarding.

Related guide: Connect Onboarding

The timestamp at which this account link will expire.

The URL for the account link.

Creates an AccountLink object that includes a single-use Stripe URL that the platform can redirect their user to in order to take them through the Connect Onboarding flow.

The identifier of the account to create an account link for.

The type of account link the user is requesting.

You can create Account Links of type account_update only for connected accounts where your platform is responsible for collecting requirements, including Custom accounts. You can’t create them for accounts that have access to a Stripe-hosted Dashboard. If you use Connect embedded components, you can include components that allow your connected accounts to update their own information. For an account without Stripe-hosted Dashboard access where Stripe is liable for negative balances, you must use embedded components.

Provides a form for inputting outstanding requirements. Send the user to the form in this mode to just collect the new information you need.

Displays the fields that are already populated on the account object, and allows your user to edit previously provided information. Consider framing this as “edit my profile” or “update my verification information”.

The URL the user will be redirected to if the account link is expired, has been previously-visited, or is otherwise invalid. The URL you specify should attempt to generate a new account link with the same parameters used to create the original account link, then redirect the user to the new account link’s URL so they can continue with Connect Onboarding. If a new account link cannot be generated or the redirect fails you should display a useful error to the user.

The URL that the user will be redirected to upon leaving or completing the linked flow.

Returns an account link object if the call succeeded.

**Examples:**

Example 1 (unknown):
```unknown
{  "object": "account_link",  "created": 1680577733,  "expires_at": 1680578033,  "url": "https://connect.stripe.com/setup/c/acct_1Mt0CORHFI4mz9Rw/TqckGNUHg2mG"}
```

Example 2 (unknown):
```unknown
{  "object": "account_link",  "created": 1680577733,  "expires_at": 1680578033,  "url": "https://connect.stripe.com/setup/c/acct_1Mt0CORHFI4mz9Rw/TqckGNUHg2mG"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/account_links \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d account=acct_1Mt0CORHFI4mz9Rw \  --data-urlencode refresh_url="https://example.com/reauth" \  --data-urlencode return_url="https://example.com/return" \  -d type=account_onboarding
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/account_links \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d account=acct_1Mt0CORHFI4mz9Rw \  --data-urlencode refresh_url="https://example.com/reauth" \  --data-urlencode return_url="https://example.com/return" \  -d type=account_onboarding
```

---

## Financing Summary Preview

**URL:** https://docs.stripe.com/api/capital/financing_summary

**Contents:**
- Financing Summary Preview
- The Financing Summary object Preview
  - Attributes
    - objectstring
    - detailsnullable object
    - financing_offernullable string
    - statusnullable enumDeprecated
- Retrieve financing summary
  - Parameters
  - Returns

A financing summary object describes a connected account’s financing status in real time. A financing status is either accepted, delivered, or none. You can read the status of your connected accounts.

The object type: financing_summary

Additional information about the financing summary. Describes currency, advance amount, fee amount, withhold rate, remaining amount, paid amount, current repayment interval, repayment start date, and advance payout date.

Only present for financing offers with the paid_out status.

The unique identifier of the Financing Offer object that corresponds to the Financing Summary object.

The financing status of the connected account.

The connected account has an active financing offer that has been paid out.

A financing offer has been marketed to the connected account, but the account hasn’t accepted it yet.

The connected account doesn’t have any active financing.

Retrieve the financing summary object for the account.

Returns a financing summary object for the account.

**Examples:**

Example 1 (unknown):
```unknown
{  "object": "capital.financing_summary",  "details": {    "advance_amount": 100000,    "advance_paid_out_at": 1688424277.0578003,    "currency": "usd",    "current_repayment_interval": null,    "fee_amount": 10000,    "paid_amount": 100263,    "remaining_amount": 9737,    "repayments_begin_at": 1688424277.0577993,    "withhold_rate": 0.05  },  "financing_offer": "financingoffer_1NPvU12eZvKYlo2CotjdGRzu",  "status": "accepted"}
```

Example 2 (unknown):
```unknown
{  "object": "capital.financing_summary",  "details": {    "advance_amount": 100000,    "advance_paid_out_at": 1688424277.0578003,    "currency": "usd",    "current_repayment_interval": null,    "fee_amount": 10000,    "paid_amount": 100263,    "remaining_amount": 9737,    "repayments_begin_at": 1688424277.0577993,    "withhold_rate": 0.05  },  "financing_offer": "financingoffer_1NPvU12eZvKYlo2CotjdGRzu",  "status": "accepted"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/capital/financing_summary \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -H "Stripe-Account: {{CONNECTED_ACCOUNT_ID}}"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/capital/financing_summary \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -H "Stripe-Account: {{CONNECTED_ACCOUNT_ID}}"
```

---

## Accounts

**URL:** https://docs.stripe.com/api/accounts

**Contents:**
- Accounts
- The Account object
  - Attributes
    - idstring
    - business_typenullable enum
    - capabilitiesnullable object
    - companynullable object
    - countrystring
    - emailnullable string
    - individualnullable object

This is an object representing a Stripe account. You can retrieve it to see properties on the account like its current requirements or if the account is enabled to make live charges or receive payouts.

For accounts where controller.requirement_collection is application, which includes Custom accounts, the properties below are always returned.

For accounts where controller.requirement_collection is stripe, which includes Standard and Express accounts, some properties are only returned until you create an Account Link or Account Session to start Connect Onboarding. Learn about the differences between accounts.

Unique identifier for the object.

A hash containing the set of capabilities that was requested for this account and their associated states. Keys are names of capabilities. You can see the full list here. Values may be active, inactive, or pending.

Information about the company or business. This property is available for any business_type. After you create an Account Link or Account Session, only a subset of this property is returned for accounts where controller.requirement_collection is stripe, which includes Standard and Express accounts.

The account’s country.

An email address associated with the account. It’s not used for authentication and Stripe doesn’t market to this field without explicit approval from the platform.

Information about the person represented by the account. This property is null unless business_type is set to individual. After you create an Account Link or Account Session, only a subset of this property is returned for accounts where controller.requirement_collection is stripe, which includes Standard and Express accounts.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Details about the requirements for the account, including what information needs to be collected, verified, or reviewed, and by when. After a requirement is collected, verified, or reviewed, it is considered resolved. Most requirements can be addressed programmatically, however, some must be completed through a form or challenge using the Stripe Interface. Learn more about handling requirements.

Details on the acceptance of the Stripe Services Agreement by the account representative.

The Stripe account type. Can be standard, express, custom, or none.

Indicates that the account was created with controller attributes that don’t map to a type of standard, express, or custom.

With Connect, you can create Stripe accounts for your users. To do this, you’ll first need to register your platform.

If you’ve already collected information for your connected accounts, you can prefill that information when creating the account. Connect Onboarding won’t ask for the prefilled information during account onboarding. You can prefill any information on the account.

The business type. Once you create an Account Link or Account Session, this property can only be updated for accounts where controller.requirement_collection is application, which includes Custom accounts.

Each key of the dictionary represents a capability, and each capability maps to its settings (for example, whether it has been requested or not). Each capability is inactive until you have provided its specific requirements and Stripe has verified them. An account might have some of its requested capabilities be active and some be inactive.

Required when account.controller.stripe_dashboard.type is none, which includes Custom accounts.

Information about the company or business. This field is available for any business_type. Once you create an Account Link or Account Session, this property can only be updated for accounts where controller.requirement_collection is application, which includes Custom accounts.

A hash of configuration describing the account controller’s attributes.

The country in which the account holder resides, or in which the business is legally established. This should be an ISO 3166-1 alpha-2 country code. For example, if you are in the United States and the business for which you’re creating an account is legally represented in Canada, you would use CA as the country for the account being created. Available countries include Stripe’s global markets as well as countries where cross-border payouts are supported.

The email address of the account holder. This is only to make the account easier to identify to you. If controller.requirement_collection is application, which includes Custom accounts, Stripe doesn’t email the account without your consent.

The maximum length is 800 characters.

Information about the person represented by the account. This field is null unless business_type is set to individual. Once you create an Account Link or Account Session, this property can only be updated for accounts where controller.requirement_collection is application, which includes Custom accounts.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Details on the account’s acceptance of the Stripe Services Agreement. This property can only be updated for accounts where controller.requirement_collection is application, which includes Custom accounts. This property defaults to a full service agreement when empty.

The type of Stripe account to create. May be one of custom, express or standard.

Returns an Account object if the call succeeds.

Updates a connected account by setting the values of the parameters passed. Any parameters not provided are left unchanged.

For accounts where controller.requirement_collection is application, which includes Custom accounts, you can update any information on the account.

For accounts where controller.requirement_collection is stripe, which includes Standard and Express accounts, you can update all information until you create an Account Link or Account Session to start Connect onboarding, after which some properties can no longer be updated.

To update your own account, use the Dashboard. Refer to our Connect documentation to learn more about updating accounts.

The business type. Once you create an Account Link or Account Session, this property can only be updated for accounts where controller.requirement_collection is application, which includes Custom accounts.

Each key of the dictionary represents a capability, and each capability maps to its settings (for example, whether it has been requested or not). Each capability is inactive until you have provided its specific requirements and Stripe has verified them. An account might have some of its requested capabilities be active and some be inactive.

Required when account.controller.stripe_dashboard.type is none, which includes Custom accounts.

Information about the company or business. This field is available for any business_type. Once you create an Account Link or Account Session, this property can only be updated for accounts where controller.requirement_collection is application, which includes Custom accounts.

The email address of the account holder. This is only to make the account easier to identify to you. If controller.requirement_collection is application, which includes Custom accounts, Stripe doesn’t email the account without your consent.

The maximum length is 800 characters.

Information about the person represented by the account. This field is null unless business_type is set to individual. Once you create an Account Link or Account Session, this property can only be updated for accounts where controller.requirement_collection is application, which includes Custom accounts.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Details on the account’s acceptance of the Stripe Services Agreement. This property can only be updated for accounts where controller.requirement_collection is application, which includes Custom accounts. This property defaults to a full service agreement when empty.

Returns an Account object if the call succeeds. If the account ID does not exist or another issue occurs, this call raises an error. Some validations will not raise an error but will instead populate the requirements.errors array.

Retrieves the details of an account.

Returns an Account object if the call succeeds. If the account ID does not exist, this call raises an error.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "acct_1Nv0FGQ9RKHgCVdK",  "object": "account",  "business_profile": {    "annual_revenue": null,    "estimated_worker_count": null,    "mcc": null,    "name": null,    "product_description": null,    "support_address": null,    "support_email": null,    "support_phone": null,    "support_url": null,    "url": null  },  "business_type": null,  "capabilities": {},  "charges_enabled": false,  "controller": {    "fees": {      "payer": "application"    },    "is_controller": true,    "losses": {      "payments": "application"    },    "requirement_collection": "stripe",    "stripe_dashboard": {      "type": "express"    },    "type": "application"  },  "country": "US",  "created": 1695830751,  "default_currency": "usd",  "details_submitted": false,  "email": "jenny.rosen@example.com",  "external_accounts": {    "object": "list",    "data": [],    "has_more": false,    "total_count": 0,    "url": "/v1/accounts/acct_1Nv0FGQ9RKHgCVdK/external_accounts"  },  "future_requirements": {    "alternatives": [],    "current_deadline": null,    "currently_due": [],    "disabled_reason": null,    "errors": [],    "eventually_due": [],    "past_due": [],    "pending_verification": []  },  "login_links": {    "object": "list",    "total_count": 0,    "has_more": false,    "url": "/v1/accounts/acct_1Nv0FGQ9RKHgCVdK/login_links",    "data": []  },  "metadata": {},  "payouts_enabled": false,  "requirements": {    "alternatives": [],    "current_deadline": null,    "currently_due": [      "business_profile.mcc",      "business_profile.url",      "business_type",      "external_account",      "representative.first_name",      "representative.last_name",      "tos_acceptance.date",      "tos_acceptance.ip"    ],    "disabled_reason": "requirements.past_due",    "errors": [],    "eventually_due": [      "business_profile.mcc",      "business_profile.url",      "business_type",      "external_account",      "representative.first_name",      "representative.last_name",      "tos_acceptance.date",      "tos_acceptance.ip"    ],    "past_due": [      "business_profile.mcc",      "business_profile.url",      "business_type",      "external_account",      "representative.first_name",      "representative.last_name",      "tos_acceptance.date",      "tos_acceptance.ip"    ],    "pending_verification": []  },  "settings": {    "bacs_debit_payments": {      "display_name": null,      "service_user_number": null    },    "branding": {      "icon": null,      "logo": null,      "primary_color": null,      "secondary_color": null    },    "card_issuing": {      "tos_acceptance": {        "date": null,        "ip": null      }    },    "card_payments": {      "decline_on": {        "avs_failure": false,        "cvc_failure": false      },      "statement_descriptor_prefix": null,      "statement_descriptor_prefix_kanji": null,      "statement_descriptor_prefix_kana": null    },    "dashboard": {      "display_name": null,      "timezone": "Etc/UTC"    },    "invoices": {      "default_account_tax_ids": null    },    "payments": {      "statement_descriptor": null,      "statement_descriptor_kana": null,      "statement_descriptor_kanji": null    },    "payouts": {      "debit_negative_balances": true,      "schedule": {        "delay_days": 2,        "interval": "daily"      },      "statement_descriptor": null    },    "sepa_debit_payments": {}  },  "tos_acceptance": {    "date": null,    "ip": null,    "user_agent": null  },  "type": "none"}
```

Example 2 (unknown):
```unknown
{  "id": "acct_1Nv0FGQ9RKHgCVdK",  "object": "account",  "business_profile": {    "annual_revenue": null,    "estimated_worker_count": null,    "mcc": null,    "name": null,    "product_description": null,    "support_address": null,    "support_email": null,    "support_phone": null,    "support_url": null,    "url": null  },  "business_type": null,  "capabilities": {},  "charges_enabled": false,  "controller": {    "fees": {      "payer": "application"    },    "is_controller": true,    "losses": {      "payments": "application"    },    "requirement_collection": "stripe",    "stripe_dashboard": {      "type": "express"    },    "type": "application"  },  "country": "US",  "created": 1695830751,  "default_currency": "usd",  "details_submitted": false,  "email": "jenny.rosen@example.com",  "external_accounts": {    "object": "list",    "data": [],    "has_more": false,    "total_count": 0,    "url": "/v1/accounts/acct_1Nv0FGQ9RKHgCVdK/external_accounts"  },  "future_requirements": {    "alternatives": [],    "current_deadline": null,    "currently_due": [],    "disabled_reason": null,    "errors": [],    "eventually_due": [],    "past_due": [],    "pending_verification": []  },  "login_links": {    "object": "list",    "total_count": 0,    "has_more": false,    "url": "/v1/accounts/acct_1Nv0FGQ9RKHgCVdK/login_links",    "data": []  },  "metadata": {},  "payouts_enabled": false,  "requirements": {    "alternatives": [],    "current_deadline": null,    "currently_due": [      "business_profile.mcc",      "business_profile.url",      "business_type",      "external_account",      "representative.first_name",      "representative.last_name",      "tos_acceptance.date",      "tos_acceptance.ip"    ],    "disabled_reason": "requirements.past_due",    "errors": [],    "eventually_due": [      "business_profile.mcc",      "business_profile.url",      "business_type",      "external_account",      "representative.first_name",      "representative.last_name",      "tos_acceptance.date",      "tos_acceptance.ip"    ],    "past_due": [      "business_profile.mcc",      "business_profile.url",      "business_type",      "external_account",      "representative.first_name",      "representative.last_name",      "tos_acceptance.date",      "tos_acceptance.ip"    ],    "pending_verification": []  },  "settings": {    "bacs_debit_payments": {      "display_name": null,      "service_user_number": null    },    "branding": {      "icon": null,      "logo": null,      "primary_color": null,      "secondary_color": null    },    "card_issuing": {      "tos_acceptance": {        "date": null,        "ip": null      }    },    "card_payments": {      "decline_on": {        "avs_failure": false,        "cvc_failure": false      },      "statement_descriptor_prefix": null,      "statement_descriptor_prefix_kanji": null,      "statement_descriptor_prefix_kana": null    },    "dashboard": {      "display_name": null,      "timezone": "Etc/UTC"    },    "invoices": {      "default_account_tax_ids": null    },    "payments": {      "statement_descriptor": null,      "statement_descriptor_kana": null,      "statement_descriptor_kanji": null    },    "payouts": {      "debit_negative_balances": true,      "schedule": {        "delay_days": 2,        "interval": "daily"      },      "statement_descriptor": null    },    "sepa_debit_payments": {}  },  "tos_acceptance": {    "date": null,    "ip": null,    "user_agent": null  },  "type": "none"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/accounts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d country=US \  --data-urlencode email="jenny.rosen@example.com" \  -d "controller[fees][payer]"=application \  -d "controller[losses][payments]"=application \  -d "controller[stripe_dashboard][type]"=express
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/accounts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d country=US \  --data-urlencode email="jenny.rosen@example.com" \  -d "controller[fees][payer]"=application \  -d "controller[losses][payments]"=application \  -d "controller[stripe_dashboard][type]"=express
```

---

## Manage locations

**URL:** https://docs.stripe.com/terminal/fleet/locations-and-zones

**Contents:**
- Manage locations
- Group and manage your readers by physical location.
    - Note
- Locations
    - Common mistake
- Zones
- Create locations and zones
  - Create a location
  - Create a zone
  - Create a nested zone

You can streamline the management of multiple readers across different physical sites by using locations and zones.

Locations and zones help by associating each reader with specific operational sites and guarantee that the correct regional configurations are downloaded.

Locations: Allows you to group readers, monitor their connectivity status, and modify your settings based on physical location. This functionality is beneficial for marketplaces with multiple connected accounts.

Zones: Offers an optional method to further categorize locations and readers. Zones enable you to represent broader groups of readers or locations, such as larger geographic regions (for example, countries) or organizational sub-brands. Multiple locations can belong to a single zone, and you can create a hierarchical structure by grouping multiple zones under a single zone.

Zones provide an additional way to group locations. You must still assign readers to a location, and you can assign a location to only one zone.

You can create a location for each physical place where your readers operate. You can register multiple readers to each location, and nest these locations within zones. Before you can use a reader, you must register it to a location.

The required address properties for a location vary by country:

You can use the Dashboard or API to update a Location object. After you create a location, you can’t change its country. Instead, create a new location in the new country, and then re-register any readers associated with the old location.

Zones are the top-level groups that can consist of either more zones or locations. You can add more zones nested under an existing one, creating additional hierarchy levels, such as “West coast.” However, organizing your locations into zones is optional.

First, you must register your reader to a location to accept payments. You can manage your locations and zones in the Manage locations page. To open this page, click the Manage locations button on the Locations tab.

To create a location:

You can also create a specific configuration for that location.

To create a nested zone:

To add or move a location to a zone:

To delete a location, you must remove the readers associate with it:

To delete a zone, you must remove the readers associate with it:

---

## Delete a person v2

**URL:** https://docs.stripe.com/api/v2/core/accounts/delete-person

**Contents:**
- Delete a person v2
  - Parameters
    - account_idstringRequired
    - idstringRequired
  - Returns
  - Response attributes
    - idstring
    - objectstring
    - deletedboolean
- Person event types v2

Delete a Person associated with an Account.

The Account the Person is associated with.

The ID of the Person to delete.

String representing the object’s type. Objects of the same type share the same value.

Always true for a deleted object.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

The resource wasn’t found.

This is a list of all public thin events we currently send for updates to Person, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

**Examples:**

Example 1 (unknown):
```unknown
curl -X DELETE https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/persons/person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 2 (unknown):
```unknown
curl -X DELETE https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/persons/person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 3 (unknown):
```unknown
{  "id": "person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_person",  "deleted": true}
```

Example 4 (unknown):
```unknown
{  "id": "person_test_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_person",  "deleted": true}
```

---

## Person

**URL:** https://docs.stripe.com/api/persons

**Contents:**
- Person
- The Person object
  - Attributes
    - idstring
    - accountstring
    - addressnullable object
    - dobnullable object
    - emailnullable string
    - first_namenullable string
    - last_namenullable string

This is an object representing a person associated with a Stripe account.

A platform can only access a subset of data in a person for an account where account.controller.requirement_collection is stripe, which includes Standard and Express accounts, after creating an Account Link or Account Session to start Connect onboarding.

See the Standard onboarding or Express onboarding documentation for information about prefilling information and account onboarding steps. Learn more about handling identity verification with the API.

Unique identifier for the object.

The account the person is associated with.

The person’s address.

The person’s date of birth.

The person’s email address. Also available for accounts where controller.requirement_collection is stripe.

The person’s first name. Also available for accounts where controller.requirement_collection is stripe.

The person’s last name. Also available for accounts where controller.requirement_collection is stripe.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The person’s phone number.

Describes the person’s relationship to the account. Also available for accounts where controller.requirement_collection is stripe.

Information about the requirements for this person, including what information needs to be collected, and by when.

Creates a new person.

The person’s address.

The person’s date of birth.

The person’s email address.

The maximum length is 800 characters.

The person’s first name.

The person’s ID number, as appropriate for their country. For example, a social security number in the U.S., social insurance number in Canada, etc. Instead of the number itself, you can also provide a PII token provided by Stripe.js.

The person’s last name.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The person’s phone number.

The relationship that this person has with the account’s legal entity.

The last four digits of the person’s Social Security number (U.S. only).

Returns a person object.

Updates an existing person.

The person’s address.

The person’s date of birth.

The person’s email address.

The maximum length is 800 characters.

The person’s first name.

The person’s ID number, as appropriate for their country. For example, a social security number in the U.S., social insurance number in Canada, etc. Instead of the number itself, you can also provide a PII token provided by Stripe.js.

The person’s last name.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The person’s phone number.

The relationship that this person has with the account’s legal entity.

The last four digits of the person’s Social Security number (U.S. only).

Returns a person object.

Retrieves an existing person.

Returns a person object.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/accounts/acct_1032D82eZvKYlo2C/persons \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d first_name=John \  -d last_name=Doe
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/accounts/acct_1032D82eZvKYlo2C/persons \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d first_name=John \  -d last_name=Doe
```

Example 3 (unknown):
```unknown
{  "id": "person_1N9XNb2eZvKYlo2CjPX7xF6F",  "object": "person",  "account": "acct_1032D82eZvKYlo2C",  "created": 1684518375,  "dob": {    "day": null,    "month": null,    "year": null  },  "first_name": "John",  "future_requirements": {    "alternatives": [],    "currently_due": [],    "errors": [],    "eventually_due": [],    "past_due": [],    "pending_verification": []  },  "id_number_provided": false,  "last_name": "Doe",  "metadata": {},  "relationship": {    "director": false,    "executive": false,    "owner": false,    "percent_ownership": null,    "representative": false,    "title": null  },  "requirements": {    "alternatives": [],    "currently_due": [],    "errors": [],    "eventually_due": [],    "past_due": [],    "pending_verification": []  },  "ssn_last_4_provided": false,  "verification": {    "additional_document": {      "back": null,      "details": null,      "details_code": null,      "front": null    },    "details": null,    "details_code": null,    "document": {      "back": null,      "details": null,      "details_code": null,      "front": null    },    "status": "unverified"  }}
```

Example 4 (unknown):
```unknown
{  "id": "person_1N9XNb2eZvKYlo2CjPX7xF6F",  "object": "person",  "account": "acct_1032D82eZvKYlo2C",  "created": 1684518375,  "dob": {    "day": null,    "month": null,    "year": null  },  "first_name": "John",  "future_requirements": {    "alternatives": [],    "currently_due": [],    "errors": [],    "eventually_due": [],    "past_due": [],    "pending_verification": []  },  "id_number_provided": false,  "last_name": "Doe",  "metadata": {},  "relationship": {    "director": false,    "executive": false,    "owner": false,    "percent_ownership": null,    "representative": false,    "title": null  },  "requirements": {    "alternatives": [],    "currently_due": [],    "errors": [],    "eventually_due": [],    "past_due": [],    "pending_verification": []  },  "ssn_last_4_provided": false,  "verification": {    "additional_document": {      "back": null,      "details": null,      "details_code": null,      "front": null    },    "details": null,    "details_code": null,    "document": {      "back": null,      "details": null,      "details_code": null,      "front": null    },    "status": "unverified"  }}
```

---

## Close an account v2

**URL:** https://docs.stripe.com/api/v2/core/accounts/close

**Contents:**
- Close an account v2
  - Parameters
    - idstringRequired
    - applied_configurationsarray of enums
  - Returns
  - Response attributes
    - idstring
    - objectstring, value is "v2.core.account"
    - applied_configurationsarray of enums
    - closednullable boolean

Removes access to the Account and its associated resources. Closed Accounts can no longer be operated on, but limited information can still be retrieved through the API in order to be able to track their history.

The ID of the Account to close.

Configurations on the Account to be closed. All configurations on the Account must be passed in for this request to succeed.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Unique identifier for the Account.

String representing the object’s type. Objects of the same type share the same value of the object field.

The configurations that have been applied to this account.

The Account can be used as a customer.

The Account can be used as a merchant.

The Account can be used as a recipient.

Indicates whether the account has been closed.

An Account represents a company, individual, or other entity that a user interacts with. Accounts store identity information and one or more configurations that enable product-specific capabilities. You can assign configurations at creation or add them later.

The default contact email address for the Account. Required when configuring the account as a merchant or recipient.

Time at which the object was created. Represented as a RFC 3339 date & time UTC value in millisecond precision, for example: 2022-09-18T13:22:18.123Z.

A value indicating the Stripe dashboard this Account has access to. This will depend on which configurations are enabled for this account.

The Account has access to the Express hosted dashboard.

The Account has access to the full Stripe hosted dashboard.

The Account does not have access to any Stripe hosted dashboard.

Default values for settings shared across Account configurations.

A descriptive name for the Account. This name will be surfaced in the Stripe Dashboard and on any invoices sent to the Account.

Information about the future requirements for the Account that will eventually come into effect, including what information needs to be collected, and by when.

Information about the company, individual, and business represented by the Account.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Information about the active requirements for the Account, including what information needs to be collected, and by when.

Account is not yet compatible with V2 APIs.

Accounts v2 is not enabled for your platform.

Account with Merchant or Recipient configuration with transfers feature cannot be closed because the account has a cash balance.

Account with Customer configuration cannot be closed because the customer has a cash balance.

Account cannot be closed without specifying the right configurations.

Account cannot be closed due to other pending resources.

Platform has not signed up for Connect and cannot create connected accounts.

Account with Stripe-owned loss liability and dashboard cannot be deleted.

V1 Account ID cannot be used in V2 Account APIs.

V1 Customer ID cannot be used in V2 Account APIs.

The resource wasn’t found.

This is a list of all public thin events we currently send for updates to Account, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

**Examples:**

Example 1 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/close \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "applied_configurations": [        "merchant"    ]  }'
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/close \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "applied_configurations": [        "merchant"    ]  }'
```

Example 3 (unknown):
```unknown
{  "id": "acct_1Nv0FGQ9RKHgCVdK",  "object": "v2.core.account",  "applied_configurations": [    "merchant"  ],  "contact_email": "jenny.rosen@example.com",  "created": "2024-11-26T16:33:03.000Z",  "dashboard": "none",  "display_name": "Jenny Rosen",  "livemode": true,  "metadata": {}}
```

Example 4 (unknown):
```unknown
{  "id": "acct_1Nv0FGQ9RKHgCVdK",  "object": "v2.core.account",  "applied_configurations": [    "merchant"  ],  "contact_email": "jenny.rosen@example.com",  "created": "2024-11-26T16:33:03.000Z",  "dashboard": "none",  "display_name": "Jenny Rosen",  "livemode": true,  "metadata": {}}
```

---

## Interactive platform guide

**URL:** https://docs.stripe.com/connect/interactive-platform-guide

**Contents:**
- Interactive platform guide
- Create a personalized platform integration guide for your business.
  - 1. Select your business model
  - 2. Select a monetization strategy
- Setup
  - Accept a payment
  - Risk and compliance responsibilities
- Preview the user experience

Generate a personalized integration guide by selecting the options that best apply to your business.

Your business model determines the appropriate flow of funds for your integration.

You can select one or more ways for your platform to charge connected accounts.

Based on your selections, the sections below provide a personalized setup.

A direct charge is a customer payment made directly to a connected account. Customers directly transact with your connected account, often unaware of your platform’s existence.

This charge type is best suited for platforms providing software as a service. For example, Shopify provides tools for building online storefronts, and Thinkific enables educators to sell online courses.

Stripe monitors risk signals on connected accounts, implements risk interventions on connected accounts in response to observed signals, and seeks to recover negative balances from your connected accounts.

For most software as a service platforms, this is the best choice, especially for those that are new to embedding payments:

Learn about managing funds movement for payment reversals specifically for SaaS platforms, including how to handle refunds and dispute chargebacks effectively.

Connected accounts use hosted onboarding and manage their accounts from a hosted surface.

Stripe-hosted onboarding handles the collection of business and identity verification information from connected accounts, requiring minimal effort from the platform. A web form hosted by Stripe renders dynamically, based on the capabilities, country, and business type of each connected account.

Get started with a code quickstart or copy these setup steps as a prompt.

---

## Manage payout schedule

**URL:** https://docs.stripe.com/connect/manage-payout-schedule

**Contents:**
- Manage payout schedule
- Manage the automatic payout schedule to your connected accounts.
    - Note
- delay_days property
- Interval property

This guide shows how to configure payouts using the Balance Settings API. Use Balance Settings to manage payout settings for Accounts v2. The Balance Settings object follows similar structure and behavior to the Accounts v1 settings.payouts hash. If you’re currently using settings.payouts on Accounts v1, you can continue to do so.

When using automatic payouts, the payments.payouts.schedule hash contains details on when a Stripe account’s funds are available and when the balance is automatically paid out:

The settlement_timing.delay_days property reflects how long it takes for on_behalf_of charges (or direct charges performed on the connected account) to become available for payout. You can edit this property on accounts where you own fraud and dispute liability. This property can be overridden by setting delay_days_override to a number up to 31. Passing an empty string to delay_days_override will return delay_days to the default, which is the lowest available value for the account.

This field is useful for dictating automatic payouts. Stripe calculates the delay in business days or calendar days, depending on the connected accounts’ country. For example, if you want a connected account based in Singapore (which uses calendar day delays) to receive their funds two weeks after the charge is made, set interval to daily and delay_days_override to 14.

For accounts where Stripe manages fraud and dispute liability (for example, Standard accounts), the default is the lowest permitted value for the account, determined by the connected account’s country. For accounts where you own fraud and dispute liability, the value remains at your original payout speed by default.

Platforms that manage fraud and dispute liability, or have platform controls, can adjust the payout interval. There are four possible settings for the interval property:

**Examples:**

Example 1 (unknown):
```unknown
{
  "object": "balance_settings",
  "payments": {
    "debit_negative_balances": true,
    "payouts": {
      "minimum_balance_by_currency": {
        "usd": 1500,
        "cad": 8000
      },
      "schedule": {
        "interval": "weekly",
        "weekly_payout_days": ["monday", "wednesday"],
        "monthly_payout_days": null
      },
      "statement_descriptor": null,
      "status": "enabled"
    },
    "settlement_timing": {
      "delay_days_override": 3,
      "delay_days": 3
    }
  }
}
```

Example 2 (unknown):
```unknown
{
  "object": "balance_settings",
  "payments": {
    "debit_negative_balances": true,
    "payouts": {
      "minimum_balance_by_currency": {
        "usd": 1500,
        "cad": 8000
      },
      "schedule": {
        "interval": "weekly",
        "weekly_payout_days": ["monday", "wednesday"],
        "monthly_payout_days": null
      },
      "statement_descriptor": null,
      "status": "enabled"
    },
    "settlement_timing": {
      "delay_days_override": 3,
      "delay_days": 3
    }
  }
}
```

---

## The Account object

**URL:** https://docs.stripe.com/api/accounts/object

**Contents:**
- The Account object
  - Attributes
    - idstring
    - business_typenullable enum
    - capabilitiesnullable object
    - companynullable object
    - countrystring
    - emailnullable string
    - individualnullable object
    - metadatanullable object

Unique identifier for the object.

A hash containing the set of capabilities that was requested for this account and their associated states. Keys are names of capabilities. You can see the full list here. Values may be active, inactive, or pending.

Information about the company or business. This property is available for any business_type. After you create an Account Link or Account Session, only a subset of this property is returned for accounts where controller.requirement_collection is stripe, which includes Standard and Express accounts.

The account’s country.

An email address associated with the account. It’s not used for authentication and Stripe doesn’t market to this field without explicit approval from the platform.

Information about the person represented by the account. This property is null unless business_type is set to individual. After you create an Account Link or Account Session, only a subset of this property is returned for accounts where controller.requirement_collection is stripe, which includes Standard and Express accounts.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Details about the requirements for the account, including what information needs to be collected, verified, or reviewed, and by when. After a requirement is collected, verified, or reviewed, it is considered resolved. Most requirements can be addressed programmatically, however, some must be completed through a form or challenge using the Stripe Interface. Learn more about handling requirements.

Details on the acceptance of the Stripe Services Agreement by the account representative.

The Stripe account type. Can be standard, express, custom, or none.

Indicates that the account was created with controller attributes that don’t map to a type of standard, express, or custom.

With Connect, you can create Stripe accounts for your users. To do this, you’ll first need to register your platform.

If you’ve already collected information for your connected accounts, you can prefill that information when creating the account. Connect Onboarding won’t ask for the prefilled information during account onboarding. You can prefill any information on the account.

The business type. Once you create an Account Link or Account Session, this property can only be updated for accounts where controller.requirement_collection is application, which includes Custom accounts.

Each key of the dictionary represents a capability, and each capability maps to its settings (for example, whether it has been requested or not). Each capability is inactive until you have provided its specific requirements and Stripe has verified them. An account might have some of its requested capabilities be active and some be inactive.

Required when account.controller.stripe_dashboard.type is none, which includes Custom accounts.

Information about the company or business. This field is available for any business_type. Once you create an Account Link or Account Session, this property can only be updated for accounts where controller.requirement_collection is application, which includes Custom accounts.

A hash of configuration describing the account controller’s attributes.

The country in which the account holder resides, or in which the business is legally established. This should be an ISO 3166-1 alpha-2 country code. For example, if you are in the United States and the business for which you’re creating an account is legally represented in Canada, you would use CA as the country for the account being created. Available countries include Stripe’s global markets as well as countries where cross-border payouts are supported.

The email address of the account holder. This is only to make the account easier to identify to you. If controller.requirement_collection is application, which includes Custom accounts, Stripe doesn’t email the account without your consent.

The maximum length is 800 characters.

Information about the person represented by the account. This field is null unless business_type is set to individual. Once you create an Account Link or Account Session, this property can only be updated for accounts where controller.requirement_collection is application, which includes Custom accounts.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Details on the account’s acceptance of the Stripe Services Agreement. This property can only be updated for accounts where controller.requirement_collection is application, which includes Custom accounts. This property defaults to a full service agreement when empty.

The type of Stripe account to create. May be one of custom, express or standard.

Returns an Account object if the call succeeds.

Updates a connected account by setting the values of the parameters passed. Any parameters not provided are left unchanged.

For accounts where controller.requirement_collection is application, which includes Custom accounts, you can update any information on the account.

For accounts where controller.requirement_collection is stripe, which includes Standard and Express accounts, you can update all information until you create an Account Link or Account Session to start Connect onboarding, after which some properties can no longer be updated.

To update your own account, use the Dashboard. Refer to our Connect documentation to learn more about updating accounts.

The business type. Once you create an Account Link or Account Session, this property can only be updated for accounts where controller.requirement_collection is application, which includes Custom accounts.

Each key of the dictionary represents a capability, and each capability maps to its settings (for example, whether it has been requested or not). Each capability is inactive until you have provided its specific requirements and Stripe has verified them. An account might have some of its requested capabilities be active and some be inactive.

Required when account.controller.stripe_dashboard.type is none, which includes Custom accounts.

Information about the company or business. This field is available for any business_type. Once you create an Account Link or Account Session, this property can only be updated for accounts where controller.requirement_collection is application, which includes Custom accounts.

The email address of the account holder. This is only to make the account easier to identify to you. If controller.requirement_collection is application, which includes Custom accounts, Stripe doesn’t email the account without your consent.

The maximum length is 800 characters.

Information about the person represented by the account. This field is null unless business_type is set to individual. Once you create an Account Link or Account Session, this property can only be updated for accounts where controller.requirement_collection is application, which includes Custom accounts.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Details on the account’s acceptance of the Stripe Services Agreement. This property can only be updated for accounts where controller.requirement_collection is application, which includes Custom accounts. This property defaults to a full service agreement when empty.

Returns an Account object if the call succeeds. If the account ID does not exist or another issue occurs, this call raises an error. Some validations will not raise an error but will instead populate the requirements.errors array.

Retrieves the details of an account.

Returns an Account object if the call succeeds. If the account ID does not exist, this call raises an error.

Returns a list of accounts connected to your platform via Connect. If you’re not a platform, the list is empty.

A dictionary with a data property that contains an array of up to limit accounts, starting after account starting_after. Each entry in the array is a separate Account object. If no more accounts are available, the resulting array is empty.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "acct_1Nv0FGQ9RKHgCVdK",  "object": "account",  "business_profile": {    "annual_revenue": null,    "estimated_worker_count": null,    "mcc": null,    "name": null,    "product_description": null,    "support_address": null,    "support_email": null,    "support_phone": null,    "support_url": null,    "url": null  },  "business_type": null,  "capabilities": {},  "charges_enabled": false,  "controller": {    "fees": {      "payer": "application"    },    "is_controller": true,    "losses": {      "payments": "application"    },    "requirement_collection": "stripe",    "stripe_dashboard": {      "type": "express"    },    "type": "application"  },  "country": "US",  "created": 1695830751,  "default_currency": "usd",  "details_submitted": false,  "email": "jenny.rosen@example.com",  "external_accounts": {    "object": "list",    "data": [],    "has_more": false,    "total_count": 0,    "url": "/v1/accounts/acct_1Nv0FGQ9RKHgCVdK/external_accounts"  },  "future_requirements": {    "alternatives": [],    "current_deadline": null,    "currently_due": [],    "disabled_reason": null,    "errors": [],    "eventually_due": [],    "past_due": [],    "pending_verification": []  },  "login_links": {    "object": "list",    "total_count": 0,    "has_more": false,    "url": "/v1/accounts/acct_1Nv0FGQ9RKHgCVdK/login_links",    "data": []  },  "metadata": {},  "payouts_enabled": false,  "requirements": {    "alternatives": [],    "current_deadline": null,    "currently_due": [      "business_profile.mcc",      "business_profile.url",      "business_type",      "external_account",      "representative.first_name",      "representative.last_name",      "tos_acceptance.date",      "tos_acceptance.ip"    ],    "disabled_reason": "requirements.past_due",    "errors": [],    "eventually_due": [      "business_profile.mcc",      "business_profile.url",      "business_type",      "external_account",      "representative.first_name",      "representative.last_name",      "tos_acceptance.date",      "tos_acceptance.ip"    ],    "past_due": [      "business_profile.mcc",      "business_profile.url",      "business_type",      "external_account",      "representative.first_name",      "representative.last_name",      "tos_acceptance.date",      "tos_acceptance.ip"    ],    "pending_verification": []  },  "settings": {    "bacs_debit_payments": {      "display_name": null,      "service_user_number": null    },    "branding": {      "icon": null,      "logo": null,      "primary_color": null,      "secondary_color": null    },    "card_issuing": {      "tos_acceptance": {        "date": null,        "ip": null      }    },    "card_payments": {      "decline_on": {        "avs_failure": false,        "cvc_failure": false      },      "statement_descriptor_prefix": null,      "statement_descriptor_prefix_kanji": null,      "statement_descriptor_prefix_kana": null    },    "dashboard": {      "display_name": null,      "timezone": "Etc/UTC"    },    "invoices": {      "default_account_tax_ids": null    },    "payments": {      "statement_descriptor": null,      "statement_descriptor_kana": null,      "statement_descriptor_kanji": null    },    "payouts": {      "debit_negative_balances": true,      "schedule": {        "delay_days": 2,        "interval": "daily"      },      "statement_descriptor": null    },    "sepa_debit_payments": {}  },  "tos_acceptance": {    "date": null,    "ip": null,    "user_agent": null  },  "type": "none"}
```

Example 2 (unknown):
```unknown
{  "id": "acct_1Nv0FGQ9RKHgCVdK",  "object": "account",  "business_profile": {    "annual_revenue": null,    "estimated_worker_count": null,    "mcc": null,    "name": null,    "product_description": null,    "support_address": null,    "support_email": null,    "support_phone": null,    "support_url": null,    "url": null  },  "business_type": null,  "capabilities": {},  "charges_enabled": false,  "controller": {    "fees": {      "payer": "application"    },    "is_controller": true,    "losses": {      "payments": "application"    },    "requirement_collection": "stripe",    "stripe_dashboard": {      "type": "express"    },    "type": "application"  },  "country": "US",  "created": 1695830751,  "default_currency": "usd",  "details_submitted": false,  "email": "jenny.rosen@example.com",  "external_accounts": {    "object": "list",    "data": [],    "has_more": false,    "total_count": 0,    "url": "/v1/accounts/acct_1Nv0FGQ9RKHgCVdK/external_accounts"  },  "future_requirements": {    "alternatives": [],    "current_deadline": null,    "currently_due": [],    "disabled_reason": null,    "errors": [],    "eventually_due": [],    "past_due": [],    "pending_verification": []  },  "login_links": {    "object": "list",    "total_count": 0,    "has_more": false,    "url": "/v1/accounts/acct_1Nv0FGQ9RKHgCVdK/login_links",    "data": []  },  "metadata": {},  "payouts_enabled": false,  "requirements": {    "alternatives": [],    "current_deadline": null,    "currently_due": [      "business_profile.mcc",      "business_profile.url",      "business_type",      "external_account",      "representative.first_name",      "representative.last_name",      "tos_acceptance.date",      "tos_acceptance.ip"    ],    "disabled_reason": "requirements.past_due",    "errors": [],    "eventually_due": [      "business_profile.mcc",      "business_profile.url",      "business_type",      "external_account",      "representative.first_name",      "representative.last_name",      "tos_acceptance.date",      "tos_acceptance.ip"    ],    "past_due": [      "business_profile.mcc",      "business_profile.url",      "business_type",      "external_account",      "representative.first_name",      "representative.last_name",      "tos_acceptance.date",      "tos_acceptance.ip"    ],    "pending_verification": []  },  "settings": {    "bacs_debit_payments": {      "display_name": null,      "service_user_number": null    },    "branding": {      "icon": null,      "logo": null,      "primary_color": null,      "secondary_color": null    },    "card_issuing": {      "tos_acceptance": {        "date": null,        "ip": null      }    },    "card_payments": {      "decline_on": {        "avs_failure": false,        "cvc_failure": false      },      "statement_descriptor_prefix": null,      "statement_descriptor_prefix_kanji": null,      "statement_descriptor_prefix_kana": null    },    "dashboard": {      "display_name": null,      "timezone": "Etc/UTC"    },    "invoices": {      "default_account_tax_ids": null    },    "payments": {      "statement_descriptor": null,      "statement_descriptor_kana": null,      "statement_descriptor_kanji": null    },    "payouts": {      "debit_negative_balances": true,      "schedule": {        "delay_days": 2,        "interval": "daily"      },      "statement_descriptor": null    },    "sepa_debit_payments": {}  },  "tos_acceptance": {    "date": null,    "ip": null,    "user_agent": null  },  "type": "none"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/accounts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d country=US \  --data-urlencode email="jenny.rosen@example.com" \  -d "controller[fees][payer]"=application \  -d "controller[losses][payments]"=application \  -d "controller[stripe_dashboard][type]"=express
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/accounts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d country=US \  --data-urlencode email="jenny.rosen@example.com" \  -d "controller[fees][payer]"=application \  -d "controller[losses][payments]"=application \  -d "controller[stripe_dashboard][type]"=express
```

---

## Build a marketplace

**URL:** https://docs.stripe.com/connect/marketplace

**Contents:**
- Build a marketplace
- Build a marketplace to connect sellers with customers and facilitate the exchange of physical or digital items or services.
- Monetization
- Merchant risk
- Resources

A marketplace provides a single storefront that offers products and services from many sellers. Customers pay the marketplace, and see the marketplace’s name on their receipt. The marketplace then pays the sellers. Traditional marketplaces, like Amazon and TixTrack, facilitate the sale of physical or digital items. Businesses such as Lyft and Instacart, which connect customers to vendors that offer services, are also considered marketplaces.

Use this guide if you’re creating a marketplace where:

We recommend using this configuration when you get started with building a marketplace with Connect. You also have other options, including using embedded or custom configurations.

In addition to the essential tasks you need to complete to set up a marketplace, you also need to consider how your marketplace will monetize and how you will handle merchant risk.

Marketplaces typically charge a commission or fee to their connected accounts for listing their services on their platform. As a marketplace, you’re responsible for paying Stripe fees, which include payment fees (such as transaction and dispute fees) and Connect fees (such as per-account fees and payout fees). In this model, you can earn revenue by:

Charging an application fee allows you to earn revenue and cover your costs to keep your balance from becoming negative. Use the platform pricing tool to automatically set pricing logic for the application fees you charge your connected accounts.

Your marketplace platform is responsible for covering the negative balances of your connected accounts. Use Radar for Platforms to prevent, detect, and mitigate both buyer risk and financially risky connected accounts.

Use this guided API Blueprint in the Dashboard to learn how to collect payments, then pay out on your marketplace.

See all the steps you need to complete to set up your marketplace on Stripe.

Learn more about every step required to build your marketplace and enable your connected accounts.

---

## External Account Cards

**URL:** https://docs.stripe.com/api/external_account_cards

**Contents:**
- External Account Cards
- The External Account Card object
  - Attributes
    - idstring
    - accountnullable stringExpandableAvailable conditionally
    - address_citynullable string
    - address_countrynullable string
    - address_line1nullable string
    - address_line2nullable string
    - address_statenullable string

External account cards are debit cards associated with a Stripe platform’s connected accounts for the purpose of transferring funds to or from the connected accounts Stripe balance.

Unique identifier for the object.

The account this card belongs to. This attribute will not be in the card object if the card belongs to a customer or recipient instead. This property is only available for accounts where controller.is_controller is true.

City/District/Suburb/Town/Village.

Billing address country, if provided when creating card.

Address line 1 (Street address/PO Box/Company name).

Address line 2 (Apartment/Suite/Unit/Building).

State/County/Province/Region.

If address_zip was provided, results of the check: pass, fail, unavailable, or unchecked.

Card brand. Can be American Express, Cartes Bancaires, Diners Club, Discover, Eftpos Australia, Girocard, JCB, MasterCard, UnionPay, Visa, or Unknown.

Two-letter ISO code representing the country of the card. You could use this attribute to get a sense of the international breakdown of cards you’ve collected.

Three-letter ISO code for currency in lowercase. Must be a supported currency. Only applicable on accounts (not customers or recipients). The card can be used as a transfer destination for funds in this currency. This property is only available for accounts where controller.is_controller is true.

If a CVC was provided, results of the check: pass, fail, unavailable, or unchecked. A result of unchecked indicates that CVC was provided but hasn’t been checked yet. Checks are typically performed when attaching a card to a Customer object, or when creating a charge. For more details, see Check if a card is valid without a charge.

Whether this card is the default external account for its currency. This property is only available for accounts where controller.requirement_collection is application, which includes Custom accounts.

Two-digit number representing the card’s expiration month.

Four-digit number representing the card’s expiration year.

Uniquely identifies this particular card number. You can use this attribute to check whether two customers who’ve signed up with you are using the same card number, for example. For payment methods that tokenize card information (Apple Pay, Google Pay), the tokenized number might be provided instead of the underlying card number.

As of May 1, 2021, card fingerprint in India for Connect changed to allow two fingerprints for the same card—one for India and one for the rest of the world.

Card funding type. Can be credit, debit, prepaid, or unknown.

The last four digits of the card.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

For external accounts that are cards, possible values are new and errored. If a payout fails, the status is set to errored and scheduled payouts are stopped until account details are updated.

When you create a new debit card, you must specify a connected account to create it on. You can only specify connected accounts where account.controller.requirement_collection is application (includes Custom accounts).

If the account has no default destination card, then the new card will become the default. However, if the owner already has a default then it will not change. To change the default, you should set default_for_currency to true.

A token, like the ones returned by Stripe.js or a dictionary containing a user’s card details (with the options shown below). Stripe will automatically validate the card.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the card object

If you need to update only some card details, like the billing address or expiration date, you can do so without having to re-enter the full card details. Stripe also works directly with card networks so that your customers can continue using your service without interruption.

When set to true, this becomes the default external account for its currency.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the card object.

By default, you can see the 10 most recent external accounts stored on a connected account directly on the object. You can also retrieve details about a specific card stored on the account.

Unique identifier for the external account to be retrieved.

Returns the card object.

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
curl https://api.stripe.com/v1/accounts/acct_1032D82eZvKYlo2C/external_accounts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d external_account=tok_visa_debit
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/accounts/acct_1032D82eZvKYlo2C/external_accounts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d external_account=tok_visa_debit
```

---

## Connect account typesLegacy

**URL:** https://docs.stripe.com/connect/accounts

**Contents:**
- Connect account typesLegacy
- Learn about older connected account configurations.
    - Newer Connect integrations
- Choose an account type
- Express connected accounts
  - Express connected account availability
- Standard connected accounts
    - Country can't be changed
- Custom connected accounts
  - Custom connected account availability

When using Connect, you create a connected account for each business or individual that signs up to access your platform’s services. You can configure your platform and connected accounts to fit your business model, distributing specific responsibilities between your platform, Stripe, and your connected accounts.

The information on this page applies only to platforms that already use legacy connected account types. If you’re setting up a new Connect platform, or your integration uses the Accounts v2 API, see the Interactive platform guide. If your existing integration uses the Accounts v1 API, see Design an advanced integration.

If your existing connected accounts are configured as a type, you can migrate your platform to support new connected accounts using the Accounts v2 API or v1 Accounts with controller properties. During and after migration, your platform can continue to support your existing connected accounts without interruption.

Connect supports the following account types:

You must consider several factors when choosing an account type. Integration effort and connected account user experience are especially important because they can affect engineering resource expenditure and conversion rates. After you create a connected account, you can’t change its type.

Extensions building on Connect must use OAuth to connect to Standard connected accounts.

Stripe recommends that you use controller properties instead of account types. If you want to use account types, we recommend Express or Standard connected accounts because they require less integration effort. For more control over your connected accounts, consider using Custom connected accounts. To learn which account type we recommend for your business, refer to your platform profile.

There’s an additional cost for using Express or Custom connected accounts.

With Standard connected accounts, the connected account is responsible for fraud and disputes when using direct charges, but that can vary when using destination charges.

With Express connected accounts, Stripe handles the onboarding and identity verification processes. The platform has the ability to specify charge types and set the connected account’s payout settings programmatically. The platform is responsible for handling disputes and refunds, which is similar to a Custom connected account.

Although your connected account has interactions with Stripe, they primarily interact with your platform, particularly for the core payment processing functionality. For Express connected account holders, Stripe provides an Express Dashboard (a lighter version of the Dashboard) that allows them to manage their personal information and see payouts to their bank.

Use Express connected accounts when you:

Some examples of platforms that use Express connected accounts are home-rental marketplaces, such as Airbnb, and ride-hailing services, such as Lyft.

Global compliance requirements do evolve and change over time. With Express, Stripe proactively collects information when requirements change. For best practices on how to communicate to your connected accounts when that happens, visit the guide for Express accounts.

Select one of the available countries when you create an Express connected account. You can’t change the country later.

Some countries are available only when using cross-border payouts.

To know when Express connected accounts are available in your country, contact Stripe.

A Standard connected account is a conventional Stripe account where the connected account has a direct relationship with Stripe, is able to log in to the Dashboard, and can process charges on their own.

Use Standard connected accounts when you:

Some examples of platforms that use Standard connected accounts are store builders, such as Shopify, and Software as a Service (SaaS) platforms, such as an online invoicing and payment service.

Global compliance requirements do evolve and change over time. With Standard connected accounts, Stripe proactively collects information when requirements change. For best practices on how to communicate to your connected accounts when that happens, visit the guide for Standard accounts.

After you create a Standard connected account, you can’t change its country.

A Custom connected account is almost completely invisible to the account holder. You—the platform—are responsible for all interactions with your connected accounts, including collecting any information Stripe needs. You have the ability to change all of the account’s settings, including the payout bank or debit card account, programmatically.

Custom connected account holders don’t have access to the Dashboard, and Stripe doesn’t contact them directly.

Use Custom connected accounts when you:

Creating and managing Custom connected accounts requires a larger integration effort than the other account types. To learn more, see Using Connect with Custom accounts.

Global compliance requirements do evolve and change over time. For best practices on how to communicate to your connected accounts when requirements change, see the guide for Custom accounts.

If you decide to use Custom connected accounts, Stripe recommends that you use Connect Onboarding for Custom accounts to collect onboarding and verification information from your connected accounts. That decreases your integration effort and eliminates the need to update your onboarding form when requirements change.

Select one of the available countries when you create a Custom connected account. You can’t change the country later.

Some countries are available only when using cross-border payouts.

To request notification when Custom connected accounts are available in your country, contact Stripe.

---

## Payouts to connected accounts

**URL:** https://docs.stripe.com/connect/payouts-connected-accounts

**Contents:**
- Payouts to connected accounts
- Manage payouts and external accounts for your platform's connected accounts.
- Payout management configurations
- Supported settlement currencies
    - Note
  - Use webhooks with payouts
    - Accounts v2 API

By default, any charge you make on behalf of a connected account accumulates in the connected account’s balance and is paid out on a daily rolling basis. Depending on the configuration of your connected accounts, your platform can manage their payouts as follows:

For connected accounts with access to the full Stripe Dashboard or Express Dashboard, the account holder manages their external payout accounts (bank accounts and debit cards), but the platform can schedule payouts. To schedule payouts for an account that has access to the full Stripe Dashboard, the platform must configure Platform controls for the account.

For connected accounts without access to a Stripe-hosted Dashboard, the platform manages their external payout accounts and can schedule their payouts.

To see which currencies you can use to settle funds in a particular country, select that country from the following dropdown.

For a list of supported presentment currencies, see the currencies documentation.

Platforms can also enable their connected accounts to settle funds and pay out to banks in certain non-primary currencies, or pay out to non-domestic bank accounts in the local currency. In some cases, Stripe charges a fee. For more information, see multi-currency settlement for Connect marketplaces and platforms.

You can track all payout activity on connected accounts with webhooks by creating an event destination and listening for these events:

Regardless of the Accounts API version that you use, payouts trigger only the v1 events described here. They don’t have equivalent v2 events.

For most payouts, event notifications occur over a series of days. Instant payouts typically send payout.paid within 30 minutes.

When a payout can’t be completed, a payout.failed event occurs. The event’s failure_code property indicates the reason. A failed payout also disables the external account involved in that payout, triggering an account.external_account.updated event. That external account can’t receive payouts until the platform updates the connected account’s external accounts.

---

## Transfer Reversals

**URL:** https://docs.stripe.com/api/transfer_reversals

**Contents:**
- Transfer Reversals
- The Transfer Reversal object
  - Attributes
    - idstring
    - amountinteger
    - currencyenum
    - metadatanullable object
    - transferstringExpandable
  - More attributesExpand all
    - objectstring

Stripe Connect platforms can reverse transfers made to a connected account, either entirely or partially, and can also specify whether to refund any related application fees. Transfer reversals add to the platform’s balance and subtract from the destination account’s balance.

Reversing a transfer that was made for a destination charge is allowed only up to the amount of the charge. It is possible to reverse a transfer_group transfer only if the destination account has enough balance to cover the reversal.

Related guide: Reverse transfers

Unique identifier for the object.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

ID of the transfer that was reversed.

When you create a new reversal, you must specify a transfer to create it on.

When reversing transfers, you can optionally reverse part of the transfer. You can do so as many times as you wish until the entire transfer has been reversed.

Once entirely reversed, a transfer can’t be reversed again. This method will return an error when called on an already-reversed transfer, or when trying to reverse more money than is left on a transfer.

A positive integer in cents representing how much of this transfer to reverse. Can only reverse up to the unreversed amount remaining of the transfer. Partial transfer reversals are only allowed for transfers to Stripe Accounts. Defaults to the entire transfer amount.

An arbitrary string which you can attach to a reversal object. This will be unset if you POST an empty value.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns a transfer reversal object if the reversal succeeded. Raises an error if the transfer has already been reversed or an invalid transfer identifier was provided.

Updates the specified reversal by setting the values of the parameters passed. Any parameters not provided will be left unchanged.

This request only accepts metadata and description as arguments.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the reversal object if the update succeeded. This call will raise an error if update parameters are invalid.

By default, you can see the 10 most recent reversals stored directly on the transfer object, but you can also retrieve details about a specific reversal stored on the transfer.

Returns the reversal object.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "trr_1Mio2eLkdIwHu7ixN5LPJS4a",  "object": "transfer_reversal",  "amount": 400,  "balance_transaction": "txn_1Mio2eLkdIwHu7ixosfrbjhW",  "created": 1678147568,  "currency": "usd",  "destination_payment_refund": "pyr_1Mio2eQ9PRzxEwkZYewpaIFB",  "metadata": {},  "source_refund": null,  "transfer": "tr_1Mio2dLkdIwHu7ixsUuCxJpu"}
```

Example 2 (unknown):
```unknown
{  "id": "trr_1Mio2eLkdIwHu7ixN5LPJS4a",  "object": "transfer_reversal",  "amount": 400,  "balance_transaction": "txn_1Mio2eLkdIwHu7ixosfrbjhW",  "created": 1678147568,  "currency": "usd",  "destination_payment_refund": "pyr_1Mio2eQ9PRzxEwkZYewpaIFB",  "metadata": {},  "source_refund": null,  "transfer": "tr_1Mio2dLkdIwHu7ixsUuCxJpu"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/transfers/tr_1Mio2dLkdIwHu7ixsUuCxJpu/reversals \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=400
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/transfers/tr_1Mio2dLkdIwHu7ixsUuCxJpu/reversals \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=400
```

---

## Account event types v2

**URL:** https://docs.stripe.com/api/v2/core/accounts/event-types

**Contents:**
- Account event types v2
- Event types
  - v2.core.account.closed
  - v2.core.account.created
  - v2.core.account.updated
  - v2.core.account[configuration.customer].capability_status_updated
  - v2.core.account[configuration.customer].updated
  - v2.core.account[configuration.merchant].capability_status_updated
  - v2.core.account[configuration.merchant].updated
  - v2.core.account[configuration.recipient].capability_status_updated

This is a list of all public thin events we currently send for updates to Account, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

---

## Account Session

**URL:** https://docs.stripe.com/api/account_sessions

**Contents:**
- Account Session
- The Account Session object
  - Attributes
    - accountstring
    - client_secretstring
    - componentsobject
    - expires_attimestamp
  - More attributesExpand all
    - objectstring
    - livemodeboolean

An AccountSession allows a Connect platform to grant access to a connected account in Connect embedded components.

We recommend that you create an AccountSession each time you need to display an embedded component to your user. Do not save AccountSessions to your database as they expire relatively quickly, and cannot be used more than once.

Related guide: Connect embedded components

The ID of the account the AccountSession was created for

The client secret of this AccountSession. Used on the client to set up secure access to the given account.

The client secret can be used to provide access to account from your frontend. It should not be stored, logged, or exposed to anyone other than the connected account. Make sure that you have TLS enabled on any page that includes the client secret.

Refer to our docs to setup Connect embedded components and learn about how client_secret should be handled.

Information about which embedded components and component features are enabled for this Account Session. Components that have no features have an empty features hash.

The timestamp at which this AccountSession will expire.

Creates a AccountSession object that includes a single-use token that the platform can use on their front-end to grant client-side API access.

The identifier of the account to create an Account Session for.

Each key of the dictionary represents an embedded component, and each embedded component maps to its configuration (e.g. whether it has been enabled or not).

Returns an Account Session object if the call succeeded.

**Examples:**

Example 1 (unknown):
```unknown
{  "object": "account_session",  "account": "acct_1NkDjjJyhOZfPCWt",  "client_secret": "_OXIKXxEihJokDBnDoe2sgG5OGSO2Q12shKvbeboxpALZGng",  "expires_at": 1693261123,  "livemode": false,  "components": {    "account_management": {      "enabled": false,      "features": {        "external_account_collection": true,        "disable_stripe_user_authentication": false      }    },    "account_onboarding": {      "enabled": true,      "features": {        "external_account_collection": true,        "disable_stripe_user_authentication": false      }    },    "balances": {      "enabled": true,      "features": {        "edit_payout_schedule": false,        "instant_payouts": false,        "standard_payouts": false,        "external_account_collection": true,        "disable_stripe_user_authentication": false      }    },    "documents": {      "enabled": false,      "features": {}    },    "financial_account": {      "enabled": false,      "features": {        "disable_stripe_user_authentication": false,        "external_account_collection": false,        "money_movement": false,        "send_money": false,        "transfer_balance": false      }    },    "financial_account_transactions": {      "enabled": false,      "features": {        "card_spend_dispute_management": false      }    },    "issuing_card": {      "enabled": false,      "features": {        "card_management": false,        "card_spend_dispute_management": false,        "cardholder_management": false,        "spend_control_management": false      }    },    "issuing_cards_list": {      "enabled": false,      "features": {        "card_management": false,        "card_spend_dispute_management": false,        "cardholder_management": false,        "disable_stripe_user_authentication": false,        "spend_control_management": false      }    },    "notification_banner": {      "enabled": false,      "features": {        "external_account_collection": true,        "disable_stripe_user_authentication": false      }    },    "payment_details": {      "enabled": false,      "features": {        "capture_payments": true,        "destination_on_behalf_of_charge_management": false,        "dispute_management": true,        "refund_management": true      }    },    "payments": {      "enabled": true,      "features": {        "capture_payments": true,        "destination_on_behalf_of_charge_management": false,        "dispute_management": true,        "refund_management": true      }    },    "payouts": {      "enabled": true,      "features": {        "edit_payout_schedule": false,        "instant_payouts": false,        "standard_payouts": false,        "external_account_collection": true,        "disable_stripe_user_authentication": false      }    },    "payouts_list": {      "enabled": false,      "features": {}    },    "tax_registrations": {      "enabled": false,      "features": {}    },    "tax_settings": {      "enabled": false,      "features": {}    }  }}
```

Example 2 (unknown):
```unknown
{  "object": "account_session",  "account": "acct_1NkDjjJyhOZfPCWt",  "client_secret": "_OXIKXxEihJokDBnDoe2sgG5OGSO2Q12shKvbeboxpALZGng",  "expires_at": 1693261123,  "livemode": false,  "components": {    "account_management": {      "enabled": false,      "features": {        "external_account_collection": true,        "disable_stripe_user_authentication": false      }    },    "account_onboarding": {      "enabled": true,      "features": {        "external_account_collection": true,        "disable_stripe_user_authentication": false      }    },    "balances": {      "enabled": true,      "features": {        "edit_payout_schedule": false,        "instant_payouts": false,        "standard_payouts": false,        "external_account_collection": true,        "disable_stripe_user_authentication": false      }    },    "documents": {      "enabled": false,      "features": {}    },    "financial_account": {      "enabled": false,      "features": {        "disable_stripe_user_authentication": false,        "external_account_collection": false,        "money_movement": false,        "send_money": false,        "transfer_balance": false      }    },    "financial_account_transactions": {      "enabled": false,      "features": {        "card_spend_dispute_management": false      }    },    "issuing_card": {      "enabled": false,      "features": {        "card_management": false,        "card_spend_dispute_management": false,        "cardholder_management": false,        "spend_control_management": false      }    },    "issuing_cards_list": {      "enabled": false,      "features": {        "card_management": false,        "card_spend_dispute_management": false,        "cardholder_management": false,        "disable_stripe_user_authentication": false,        "spend_control_management": false      }    },    "notification_banner": {      "enabled": false,      "features": {        "external_account_collection": true,        "disable_stripe_user_authentication": false      }    },    "payment_details": {      "enabled": false,      "features": {        "capture_payments": true,        "destination_on_behalf_of_charge_management": false,        "dispute_management": true,        "refund_management": true      }    },    "payments": {      "enabled": true,      "features": {        "capture_payments": true,        "destination_on_behalf_of_charge_management": false,        "dispute_management": true,        "refund_management": true      }    },    "payouts": {      "enabled": true,      "features": {        "edit_payout_schedule": false,        "instant_payouts": false,        "standard_payouts": false,        "external_account_collection": true,        "disable_stripe_user_authentication": false      }    },    "payouts_list": {      "enabled": false,      "features": {}    },    "tax_registrations": {      "enabled": false,      "features": {}    },    "tax_settings": {      "enabled": false,      "features": {}    }  }}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/account_sessions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d account=acct_1NkDjjJyhOZfPCWt \  -d "components[account_onboarding][enabled]"=true \  -d "components[payments][enabled]"=true \  -d "components[payouts][enabled]"=true \  -d "components[balances][enabled]"=true
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/account_sessions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d account=acct_1NkDjjJyhOZfPCWt \  -d "components[account_onboarding][enabled]"=true \  -d "components[payments][enabled]"=true \  -d "components[payouts][enabled]"=true \  -d "components[balances][enabled]"=true
```

---

## Understanding Connect account balances

**URL:** https://docs.stripe.com/connect/account-balances

**Contents:**
- Understanding Connect account balances
- Learn how Stripe account balances work when using Connect.
  - Balances by source
    - Note
- Check a connected account’s balance
- Accounting for negative balances
  - Validating connected banks
  - Automatically debit connected accounts
    - Caution
- Understanding connected reserve balances

Stripe accounts additionally have separate balances by payment source. But for simplicity’s sake, this page focuses on the broader concept of account balances regardless of the source.

Both your platform account and a connected account are still just Stripe accounts, each with their own, separate account balance.

All Stripe accounts can have balances in two states:

With non-Connect accounts, processing charges increases the Stripe account balance. The charged amount, less any Stripe fees, is initially reflected on the pending balance, and becomes available on a 2-day rolling basis. (This timing can vary by country and account.) Available funds can be paid out to a bank account or debit card. Payouts reduce the Stripe account balance accordingly.

With Connect, your platform account and each connected account has its own pending and available balances. The allocation of funds between them depends on the type of charges that you use.

Further, a platform account can also have a connect_reserved balance, used to offset negative balances on connected accounts.

When you transfer funds between your platform’s balance and a connected account’s balance, Stripe doesn’t automatically retry failures. For example, if you attempt to transfer funds from your platform’s balance to a connected account’s balance, but your platform has insufficient available funds, that transfer attempt fails. If you then add funds to your available balance, they don’t automatically transfer to the connected account’s balance. You must explicitly attempt the transfer again.

To check the balance of a connected account, perform a retrieve balance call authenticated as the connected account. The returned Balance object reflects the pending and available balances.

To reduce the risk of financial loss, make sure each connected account has a valid bank account.

Some actions, such as refunds and chargebacks, create negative transactions in a Stripe account. Stripe handles negative transactions to help maintain a positive Stripe balance for related accounts:

Despite these measures, if a connected account balance becomes negative, ultimate responsibility depends on the account’s controller.losses.payments property:

If a connected account balance is negative, Stripe debits their external account on file up to the maximum number of attempts allowed. If all attempts fail, Stripe pauses payouts to and debits from the external account until the external account on file is updated.

While an account’s balance is negative, you can’t send payouts to the account’s bank or debit card on their behalf. Stripe will resume sending payouts to the connected account when the account’s Stripe balance becomes positive.

If Stripe hasn’t already attempted to debit a connected account’s external account for a negative balance, you can allow Stripe to do so by setting debit_negative_balances to true.

Stripe can’t correct a negative Stripe account balance using a debit card.

Auto debit for negative balances is supported for banks in the following countries:

See the Auto Debit FAQ for a detailed breakdown of which countries and account types are supported.

Enabling debit_negative_balances triggers debits as needed, even when the connected account is on manual payouts. For more details, see Impact from chargebacks and negative balances.

To protect against negative connected account available balances that your platform is responsible for, Stripe holds a reserve on your platform account’s available balance. Depending on the connected account’s country, Stripe initiates a bank withdrawal on the account’s bank account to cover the negative balance. Although the available balance for the account zeroes out as soon as the withdrawal posts, we hold the platform reserve for that account for an additional 3 business days. You see this reserve reflected in the Dashboard and exported reports (as a reserve transaction).

There are three kinds of balance activities related to reserves:

To see the current reserves held on your account, perform a retrieve balance API call but for your own account (that is, not authorized as another user as in the above).

To clear a connected account’s negative balance, and thereby remove the reserve on your account, send a transfer to the applicable account. If a connected account has a negative balance for more than 180 days, Stripe will automatically transfer your reserves to the connected account to zero out the balance. Dashboard pages and reports show these transfers as Connect collection transfers.

After a connected account’s balance is cleared through a collection transfer, we recommend that you reject the account to prevent future losses.

If you need more granular control over scheduling payouts to connected accounts where your platform is responsible for negative balances, you can take one of the following approaches:

We recommend that platforms hold funds only when there’s a clear purpose and a commitment to transfer them or pay them out when an event occurs or a precondition is satisfied. The typical use case for holding funds is on-demand services platforms, where the marketplace usually waits for the service to be completed and confirmed before paying out to the service provider (for example, rentals, delivery services, and ride-sharing).

Platforms should refrain from holding funds arbitrarily, and instead pay out to their connected accounts as soon as they’re identified. This is usually when the charge is made. If you aren’t sure about holding funds, speak with your legal advisor.

For compliance reasons, we can hold funds in reserve for a period of time that’s based on the merchant’s country, as shown below:

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/balance \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -H "Stripe-Account: {{CONNECTED_ACCOUNT_ID}}"
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/balance \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -H "Stripe-Account: {{CONNECTED_ACCOUNT_ID}}"
```

---

## Create a person token v2

**URL:** https://docs.stripe.com/api/v2/core/accounts/create-person-token

**Contents:**
- Create a person token v2
  - Parameters
    - account_idstringRequired
    - additional_addressesarray of objects
    - additional_namesarray of objects
    - additional_terms_of_serviceobject
    - addressobject
    - date_of_birthobject
    - documentsobject
    - emailstring

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
curl -X POST https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/person_tokens \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "given_name": "Jenny",    "surname": "Rosen",    "email": "jenny.rosen@example.com",    "address": {        "line1": "27 Fredrick Ave",        "city": "Brothers",        "postal_code": "97712",        "state": "OR",        "country": "US"    },    "id_numbers": [        {            "type": "us_ssn_last_4",            "value": "0000"        }    ],    "relationship": {        "owner": true,        "percent_ownership": "0.8",        "representative": true,        "title": "CEO"    }  }'
```

Example 2 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/core/accounts/acct_1Nv0FGQ9RKHgCVdK/person_tokens \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "given_name": "Jenny",    "surname": "Rosen",    "email": "jenny.rosen@example.com",    "address": {        "line1": "27 Fredrick Ave",        "city": "Brothers",        "postal_code": "97712",        "state": "OR",        "country": "US"    },    "id_numbers": [        {            "type": "us_ssn_last_4",            "value": "0000"        }    ],    "relationship": {        "owner": true,        "percent_ownership": "0.8",        "representative": true,        "title": "CEO"    }  }'
```

Example 3 (unknown):
```unknown
{  "id": "perstok_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_person_token",  "created": "2025-11-17T14:00:00.000Z",  "expires_at": "2025-11-17T14:10:00.000Z",  "livemode": true,  "used": false}
```

Example 4 (unknown):
```unknown
{  "id": "perstok_61RS0CgWt1xBt8M1Q16RS0Cg0WSQO5ZXUVpZxZ9tAIbY",  "object": "v2.core.account_person_token",  "created": "2025-11-17T14:00:00.000Z",  "expires_at": "2025-11-17T14:10:00.000Z",  "livemode": true,  "used": false}
```

---

## Build a SaaS platform

**URL:** https://docs.stripe.com/connect/saas

**Contents:**
- Build a SaaS platform
- Provide a platform where merchants accept payments directly from their customers through your integration.
    - Note
  - SaaS business subscriptions
- Monetization
  - Stripe-owned pricing model
  - Buy rate model
- Resources

This guide uses Accounts v2 to create and manage connected accounts. For a guide that uses Accounts v1, see Build a SaaS platform with Accounts v1.

If you’re a subscription-based SaaS business, but don’t extend Stripe products or payment processing to your merchants, you don’t need Connect.

As a software as a service (SaaS) platform, you extend your integration of Stripe products to your merchant connected accounts. Those merchants can access Stripe through your platform to accept payments from their own customers and receive payouts from their Stripe balance.

A SaaS platform can design its revenue strategy using a referrer or wholesale model.

Your platform refers merchants to Stripe to process payments and use other financial products. In this model, the platform’s connected accounts:

Stripe doesn’t charge your platform in this model and you can earn revenue by:

Your platform purchases and white labels payment processing and other products from Stripe, and offers them to your connected accounts. In this model, the platform’s connected accounts:

Stripe charges your platform in this model and you can earn revenue by:

Use this guided API Blueprint in the Dashboard to learn how to add connected accounts to your platform and charge them a subscription fee through Billing.

Review an annotated sample SaaS platform integration and download its code to use as a starting point for your integration.

Follow the sequence of essential tasks to build your SaaS platform and onboard your connected accounts.

---

## Platform pricing tool

**URL:** https://docs.stripe.com/connect/platform-pricing-tools

**Contents:**
- Platform pricing tool
- Set platform processing fees for your connected accounts from your Stripe Dashboard.
- Demo
- Eligibility for payments
  - Requirements
  - Fee payer reference
- Eligibility for Instant Payouts
    - Instant payout application fees API integration impact
- Subscriptions and invoices
- Access platform pricing tools

If your platform is responsible for paying Stripe fees, the platform pricing tool allows you to set pricing logic for all platform processing fees you charge your connected accounts. You can use this fee, known as an “application fee," for different purposes depending on your platform’s Connect configuration and business model:

With the platform pricing tool, platforms can implement a range of pricing strategies for different payment processing use-cases, without the need to write any code:

The values available for defining your pricing scheme depend on which Stripe products you use and how you’ve integrated them. The following sections describe which platform configurations can use and access the platform pricing tools.

Stripe applies pricing schemes to a payment when the payment meets all of the following requirements:

In addition to the requirements, pricing schemes observe the following limitations:

Support for platform pricing tools also depends on your funds flow configuration for your connected accounts.

Stripe applies pricing schemes to an Instant Payout when:

Connected accounts can’t pay out more than their available balance. Instant Payout fees reflect in the Payout object to help with reporting and reconciliation. See Transactions in the Dashboard to view your collected fees. If an Instant Payout fails, we automatically refund the application fee.

Enabling pricing tools for Instant Payouts without using the Balance API net-of-fees attribute can break your API integration.

Stripe also applies your pricing scheme-defined application fees to invoice and subscription payments. As with standard purchase payments, when you apply an explicit application fee to an invoice or subscription, that fee overrides any matching scheme-defined fee.

Different roles have different levels of access to pricing schemes.

Roles that don’t have access to the platform’s default pricing can review the version copied to the connected accounts. Connected accounts can’t view or edit any pricing schemes.

The following roles can access pricing schemes that apply to all connected accounts.

---
