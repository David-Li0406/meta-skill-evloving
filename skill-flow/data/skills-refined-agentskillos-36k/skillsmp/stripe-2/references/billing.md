# Stripe - Billing

**Pages:** 28

---

## Alerts

**URL:** https://docs.stripe.com/api/billing/alert

**Contents:**
- Alerts
- The Alert object
  - Attributes
    - idstring
    - objectstring
    - alert_typeenum
    - livemodeboolean
    - statusnullable enum
    - titlestring
    - usage_thresholdnullable object

A billing alert is a resource that notifies you when a certain usage threshold on a meter is crossed. For example, you might create a billing alert to notify you when a certain user made 100 API requests.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value.

Defines the type of the alert.

Use usage_threshold if you intend for an alert to fire when a usage threshold on a meter is crossed.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Status of the alert. This can be active, inactive or archived.

Encapsulates configuration of the alert to monitor usage on a specific Billing Meter.

Creates a billing alert

The type of alert to create.

Use usage_threshold if you intend for an alert to fire when a usage threshold on a meter is crossed.

The title of the alert.

The maximum length is 256 characters.

The configuration of the usage threshold.

Returns a billing alert

Retrieves a billing alert given an ID

Lists billing active and inactive alerts

Filter results to only include this type of alert.

Use usage_threshold if you intend for an alert to fire when a usage threshold on a meter is crossed.

Filter results to only include alerts with the given meter.

Returns a list of billing alerts

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "alrt_12345",  "object": "billing.alert",  "title": "API Request usage alert",  "livemode": true,  "alert_type": "usage_threshold",  "usage_threshold": {    "gte": 10000,    "meter": "mtr_12345",    "recurrence": "one_time"  },  "status": "active"}
```

Example 2 (unknown):
```unknown
{  "id": "alrt_12345",  "object": "billing.alert",  "title": "API Request usage alert",  "livemode": true,  "alert_type": "usage_threshold",  "usage_threshold": {    "gte": 10000,    "meter": "mtr_12345",    "recurrence": "one_time"  },  "status": "active"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/billing/alerts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d title="API Request usage alert" \  -d alert_type=usage_threshold \  -d "usage_threshold[gte]"=10000 \  -d "usage_threshold[meter]"=mtr_12345 \  -d "usage_threshold[recurrence]"=one_time
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/billing/alerts \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d title="API Request usage alert" \  -d alert_type=usage_threshold \  -d "usage_threshold[gte]"=10000 \  -d "usage_threshold[meter]"=mtr_12345 \  -d "usage_threshold[recurrence]"=one_time
```

---

## Invoices

**URL:** https://docs.stripe.com/api/invoices

**Contents:**
- Invoices
- The Invoice object
  - Attributes
    - idstring
    - auto_advanceboolean
    - automatic_taxobject
    - collection_methodenum
    - confirmation_secretnullable objectExpandable
    - currencyenum
    - customerstringExpandable

Invoices are statements of amounts owed by a customer, and are either generated one-off, or generated periodically from a subscription.

They contain invoice items, and proration adjustments that may be caused by subscription upgrades/downgrades (if necessary).

If your invoice is configured to be billed through automatic charges, Stripe automatically finalizes your invoice and attempts payment. Note that finalizing the invoice, when automatic, does not happen immediately as the invoice is created. Stripe waits until one hour after the last webhook was successfully sent (or the last webhook timed out after failing). If you (and the platforms you may have connected to) have no webhooks configured, Stripe waits one hour after creation to finalize the invoice.

If your invoice is configured to be billed by sending an email, then based on your email settings, Stripe will email the invoice to your customer and await payment. These emails can contain a link to a hosted page to pay the invoice.

Stripe applies any customer credit on the account before determining the amount due for the invoice (i.e., the amount that will be actually charged). If the amount due for the invoice is less than Stripe’s minimum allowed charge per currency, the invoice is automatically marked paid, and we add the amount due to the customer’s credit balance which is applied to the next invoice.

More details on the customer’s credit balance are here.

Related guide: Send invoices to customers

Unique identifier for the object. For preview invoices created using the create preview endpoint, this id will be prefixed with upcoming_in.

Controls whether Stripe performs automatic collection of the invoice. If false, the invoice’s state doesn’t automatically advance without an explicit action.

Settings and latest results for automatic tax lookup for this invoice.

Either charge_automatically, or send_invoice. When charging automatically, Stripe will attempt to pay this invoice using the default source attached to the customer. When sending an invoice, Stripe will email this invoice to the customer with payment instructions.

Attempt payment using the default source attached to the customer.

Email payment instructions to the customer.

The confirmation secret associated with this invoice. Currently, this contains the client_secret of the PaymentIntent that Stripe creates during invoice finalization.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

The ID of the customer to bill.

The ID of the account representing the customer to bill.

An arbitrary string attached to the object. Often useful for displaying to users. Referenced as ‘memo’ in the Dashboard.

The URL for the hosted invoice page, which allows customers to view and pay an invoice. If the invoice has not been finalized yet, this will be null.

The individual line items that make up the invoice. lines is sorted as follows: (1) pending invoice items (including prorations) in reverse chronological order, (2) subscription items in reverse chronological order, and (3) invoice items added after invoice creation in chronological order.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The parent that generated this invoice

End of the usage period during which invoice items were added to this invoice. This looks back one period for a subscription invoice. Use the line item period to get the service period for each price.

Start of the usage period during which invoice items were added to this invoice. This looks back one period for a subscription invoice. Use the line item period to get the service period for each price.

The status of the invoice, one of draft, open, paid, uncollectible, or void. Learn more

Total after discounts and taxes.

This endpoint creates a draft invoice for a given customer. The invoice remains a draft until you finalize the invoice, which allows you to pay or send the invoice to your customers.

Controls whether Stripe performs automatic collection of the invoice. If false, the invoice’s state doesn’t automatically advance without an explicit action. Defaults to false.

Settings for automatic tax lookup for this invoice.

Either charge_automatically, or send_invoice. When charging automatically, Stripe will attempt to pay this invoice using the default source attached to the customer. When sending an invoice, Stripe will email this invoice to the customer with payment instructions. Defaults to charge_automatically.

The ID of the customer to bill.

The ID of the account to bill.

An arbitrary string attached to the object. Often useful for displaying to users. Referenced as ‘memo’ in the Dashboard.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The ID of the subscription to invoice, if any. If set, the created invoice will only include pending invoice items for that subscription. The subscription’s billing cycle and regular subscription events won’t be affected.

Returns the invoice object. Raises an error if the customer ID provided is invalid.

At any time, you can preview the upcoming invoice for a subscription or subscription schedule. This will show you all the charges that are pending, including subscription renewal charges, invoice item charges, etc. It will also show you any discounts that are applicable to the invoice.

You can also preview the effects of creating or updating a subscription or subscription schedule, including a preview of any prorations that will take place. To ensure that the actual proration is calculated exactly the same as the previewed proration, you should pass the subscription_details.proration_date parameter when doing the actual subscription update.

The recommended way to get only the prorations being previewed on the invoice is to consider line items where parent.subscription_item_details.proration is true.

Note that when you are viewing an upcoming invoice, you are simply viewing a preview – the invoice has not yet been created. As such, the upcoming invoice will not show up in invoice listing calls, and you cannot use the API to pay or edit the invoice. If you want to change the amount that your customer will be billed, you can add, remove, or update pending invoice items, or update the customer’s discount.

Note: Currency conversion calculations use the latest exchange rates. Exchange rates may vary between the time of the preview and the time of the actual invoice creation. Learn more

Settings for automatic tax lookup for this invoice preview.

The identifier of the customer whose upcoming invoice you’re retrieving. If automatic_tax is enabled then one of customer, customer_details, subscription, or schedule must be set.

The identifier of the account representing the customer whose upcoming invoice you’re retrieving. If automatic_tax is enabled then one of customer, customer_account, customer_details, subscription, or schedule must be set.

The identifier of the subscription for which you’d like to retrieve the upcoming invoice. If not provided, but a subscription_details.items is provided, you will preview creating a subscription with those items. If neither subscription nor subscription_details.items is provided, you will retrieve the next upcoming invoice from among the customer’s subscriptions.

Returns an invoice if valid customer information is provided. Raises an error otherwise.

Draft invoices are fully editable. Once an invoice is finalized, monetary values, as well as collection_method, become uneditable.

If you would like to stop the Stripe Billing engine from automatically finalizing, reattempting payments on, sending reminders for, or automatically reconciling invoices, pass auto_advance=false.

Controls whether Stripe performs automatic collection of the invoice.

Settings for automatic tax lookup for this invoice.

Either charge_automatically or send_invoice. This field can be updated only on draft invoices.

An arbitrary string attached to the object. Often useful for displaying to users. Referenced as ‘memo’ in the Dashboard.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the invoice object.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "in_1MtHbELkdIwHu7ixl4OzzPMv",  "object": "invoice",  "account_country": "US",  "account_name": "Stripe Docs",  "account_tax_ids": null,  "amount_due": 0,  "amount_paid": 0,  "amount_overpaid": 0,  "amount_remaining": 0,  "amount_shipping": 0,  "application": null,  "attempt_count": 0,  "attempted": false,  "auto_advance": false,  "automatic_tax": {    "enabled": false,    "liability": null,    "status": null  },  "billing_reason": "manual",  "collection_method": "charge_automatically",  "created": 1680644467,  "currency": "usd",  "custom_fields": null,  "customer": "cus_NeZwdNtLEOXuvB",  "customer_address": null,  "customer_email": "jennyrosen@example.com",  "customer_name": "Jenny Rosen",  "customer_phone": null,  "customer_shipping": null,  "customer_tax_exempt": "none",  "customer_tax_ids": [],  "confirmation_secret": null,  "default_payment_method": null,  "default_source": null,  "default_tax_rates": [],  "description": null,  "discounts": [],  "due_date": null,  "ending_balance": null,  "footer": null,  "from_invoice": null,  "hosted_invoice_url": null,  "invoice_pdf": null,  "issuer": {    "type": "self"  },  "last_finalization_error": null,  "latest_revision": null,  "lines": {    "object": "list",    "data": [],    "has_more": false,    "total_count": 0,    "url": "/v1/invoices/in_1MtHbELkdIwHu7ixl4OzzPMv/lines"  },  "payments": {    "object": "list",    "data": [],    "has_more": false,    "total_count": 0,    "url": "/v1/invoice_payments"  },  "livemode": false,  "metadata": {},  "next_payment_attempt": null,  "number": null,  "on_behalf_of": null,  "parent": null,  "payment_settings": {    "default_mandate": null,    "payment_method_options": null,    "payment_method_types": null  },  "period_end": 1680644467,  "period_start": 1680644467,  "post_payment_credit_notes_amount": 0,  "pre_payment_credit_notes_amount": 0,  "receipt_number": null,  "shipping_cost": null,  "shipping_details": null,  "starting_balance": 0,  "statement_descriptor": null,  "status": "draft",  "status_transitions": {    "finalized_at": null,    "marked_uncollectible_at": null,    "paid_at": null,    "voided_at": null  },  "subtotal": 0,  "subtotal_excluding_tax": 0,  "test_clock": null,  "total": 0,  "total_discount_amounts": [],  "total_excluding_tax": 0,  "total_taxes": [],  "transfer_data": null,  "webhooks_delivered_at": 1680644467}
```

Example 2 (unknown):
```unknown
{  "id": "in_1MtHbELkdIwHu7ixl4OzzPMv",  "object": "invoice",  "account_country": "US",  "account_name": "Stripe Docs",  "account_tax_ids": null,  "amount_due": 0,  "amount_paid": 0,  "amount_overpaid": 0,  "amount_remaining": 0,  "amount_shipping": 0,  "application": null,  "attempt_count": 0,  "attempted": false,  "auto_advance": false,  "automatic_tax": {    "enabled": false,    "liability": null,    "status": null  },  "billing_reason": "manual",  "collection_method": "charge_automatically",  "created": 1680644467,  "currency": "usd",  "custom_fields": null,  "customer": "cus_NeZwdNtLEOXuvB",  "customer_address": null,  "customer_email": "jennyrosen@example.com",  "customer_name": "Jenny Rosen",  "customer_phone": null,  "customer_shipping": null,  "customer_tax_exempt": "none",  "customer_tax_ids": [],  "confirmation_secret": null,  "default_payment_method": null,  "default_source": null,  "default_tax_rates": [],  "description": null,  "discounts": [],  "due_date": null,  "ending_balance": null,  "footer": null,  "from_invoice": null,  "hosted_invoice_url": null,  "invoice_pdf": null,  "issuer": {    "type": "self"  },  "last_finalization_error": null,  "latest_revision": null,  "lines": {    "object": "list",    "data": [],    "has_more": false,    "total_count": 0,    "url": "/v1/invoices/in_1MtHbELkdIwHu7ixl4OzzPMv/lines"  },  "payments": {    "object": "list",    "data": [],    "has_more": false,    "total_count": 0,    "url": "/v1/invoice_payments"  },  "livemode": false,  "metadata": {},  "next_payment_attempt": null,  "number": null,  "on_behalf_of": null,  "parent": null,  "payment_settings": {    "default_mandate": null,    "payment_method_options": null,    "payment_method_types": null  },  "period_end": 1680644467,  "period_start": 1680644467,  "post_payment_credit_notes_amount": 0,  "pre_payment_credit_notes_amount": 0,  "receipt_number": null,  "shipping_cost": null,  "shipping_details": null,  "starting_balance": 0,  "statement_descriptor": null,  "status": "draft",  "status_transitions": {    "finalized_at": null,    "marked_uncollectible_at": null,    "paid_at": null,    "voided_at": null  },  "subtotal": 0,  "subtotal_excluding_tax": 0,  "test_clock": null,  "total": 0,  "total_discount_amounts": [],  "total_excluding_tax": 0,  "total_taxes": [],  "transfer_data": null,  "webhooks_delivered_at": 1680644467}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/invoices \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_NeZwdNtLEOXuvB
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/invoices \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_NeZwdNtLEOXuvB
```

---

## Meter Event Adjustments v2

**URL:** https://docs.stripe.com/api/v2/billing-meter-adjustment

**Contents:**
- Meter Event Adjustments v2
- The MeterEventAdjustment object
  - Attributes
    - idstring
    - objectstring, value is "v2.billing.meter_event_adjustment"
    - cancelobject
    - createdtimestamp
    - event_namestring
    - livemodeboolean
    - statusenum

A billing meter event adjustment is a resource that allows you to cancel a meter event. For example, you might create a billing meter event adjustment to cancel a meter event that was created in error or attached to the wrong customer.

The unique id of this meter event adjustment.

String representing the object’s type. Objects of the same type share the same value of the object field.

Specifies which event to cancel.

The time the adjustment was created.

The name of the meter event. Corresponds with the event_name field on a meter.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The meter event adjustment’s status.

The event adjustment has been processed.

The event adjustment is still being processed.

Specifies whether to cancel a single event or a range of events for a time period. Time period cancellation is not supported yet.

Cancel a single meter event by identifier.

Creates a meter event adjustment to cancel a previously sent meter event.

Specifies which event to cancel.

The name of the meter event. Corresponds with the event_name field on a meter.

Specifies whether to cancel a single event or a range of events for a time period. Time period cancellation is not supported yet.

Cancel a single meter event by identifier.

The unique id of this meter event adjustment.

String representing the object’s type. Objects of the same type share the same value of the object field.

Specifies which event to cancel.

The time the adjustment was created.

The name of the meter event. Corresponds with the event_name field on a meter.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The meter event adjustment’s status.

The event adjustment has been processed.

The event adjustment is still being processed.

Specifies whether to cancel a single event or a range of events for a time period. Time period cancellation is not supported yet.

Cancel a single meter event by identifier.

The adjustment configuration is invalid for the adjustment type.

**Examples:**

Example 1 (unknown):
```unknown
{  "object": "v2.billing.meter_event_adjustment",  "id": "mtr_event_adj_12345678",  "livemode": false,  "created": "2024-06-01T12:00:00.000Z",  "status": "pending",  "event_name": "ai_search_api",  "type": "cancel",  "cancel": {    "identifier": "idmp_12345678"  }}
```

Example 2 (unknown):
```unknown
{  "object": "v2.billing.meter_event_adjustment",  "id": "mtr_event_adj_12345678",  "livemode": false,  "created": "2024-06-01T12:00:00.000Z",  "status": "pending",  "event_name": "ai_search_api",  "type": "cancel",  "cancel": {    "identifier": "idmp_12345678"  }}
```

Example 3 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/billing/meter_event_adjustments \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "event_name": "ai_search_api",    "type": "cancel",    "cancel": {        "identifier": "idmp_12345678"    }  }'
```

Example 4 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/billing/meter_event_adjustments \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "event_name": "ai_search_api",    "type": "cancel",    "cancel": {        "identifier": "idmp_12345678"    }  }'
```

---

## Customer Portal Session

**URL:** https://docs.stripe.com/api/customer_portal/sessions

**Contents:**
- Customer Portal Session
- The Customer Portal Session object
  - Attributes
    - idstring
    - objectstring
    - configurationstringExpandable
    - createdtimestamp
    - customerstring
    - customer_accountnullable string
    - flownullable object

The Billing customer portal is a Stripe-hosted UI for subscription and billing management.

A portal configuration describes the functionality and features that you want to provide to your customers through the portal.

A portal session describes the instantiation of the customer portal for a particular customer. By visiting the session’s URL, the customer can manage their subscriptions and billing details. For security reasons, sessions are short-lived and will expire if the customer does not visit the URL. Create sessions on-demand when customers intend to manage their subscriptions and billing details.

Related guide: Customer management

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value.

The configuration used by this session, describing the features available.

Time at which the object was created. Measured in seconds since the Unix epoch.

The ID of the customer for this session.

The ID of the account for this session.

Information about a specific flow for the customer to go through. See the docs to learn more about using customer portal deep links and flows.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The IETF language tag of the locale Customer Portal is displayed in. If blank or auto, the customer’s preferred_locales or browser’s locale is used.

The account for which the session was created on behalf of. When specified, only subscriptions and invoices with this on_behalf_of account appear in the portal. For more information, see the docs. Use the Accounts API to modify the on_behalf_of account’s branding settings, which the portal displays.

The URL to redirect customers to when they click on the portal’s link to return to your website.

The short-lived URL of the session that gives customers access to the customer portal.

Creates a session of the customer portal.

The ID of an existing configuration to use for this session, describing its functionality and features. If not specified, the session uses the default configuration.

The ID of an existing customer.

The ID of an existing account.

Information about a specific flow for the customer to go through. See the docs to learn more about using customer portal deep links and flows.

The IETF language tag of the locale customer portal is displayed in. If blank or auto, the customer’s preferred_locales or browser’s locale is used.

The on_behalf_of account to use for this session. When specified, only subscriptions and invoices with this on_behalf_of account appear in the portal. For more information, see the docs. Use the Accounts API to modify the on_behalf_of account’s branding settings, which the portal displays.

The default URL to redirect customers to when they click on the portal’s link to return to your website.

Returns a portal session object.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "bps_1MrSjzLkdIwHu7ixex0IvU9b",  "object": "billing_portal.session",  "configuration": "bpc_1MAhNDLkdIwHu7ixckACO1Jq",  "created": 1680210639,  "customer": "cus_NciAYcXfLnqBoz",  "flow": null,  "livemode": false,  "locale": null,  "on_behalf_of": null,  "return_url": "https://example.com/account",  "url": "https://billing.stripe.com/p/session/test_YWNjdF8xTTJKVGtMa2RJd0h1N2l4LF9OY2lBYjJXcHY4a2NPck96UjBEbFVYRnU5bjlwVUF50100BUtQs3bl"}
```

Example 2 (unknown):
```unknown
{  "id": "bps_1MrSjzLkdIwHu7ixex0IvU9b",  "object": "billing_portal.session",  "configuration": "bpc_1MAhNDLkdIwHu7ixckACO1Jq",  "created": 1680210639,  "customer": "cus_NciAYcXfLnqBoz",  "flow": null,  "livemode": false,  "locale": null,  "on_behalf_of": null,  "return_url": "https://example.com/account",  "url": "https://billing.stripe.com/p/session/test_YWNjdF8xTTJKVGtMa2RJd0h1N2l4LF9OY2lBYjJXcHY4a2NPck96UjBEbFVYRnU5bjlwVUF50100BUtQs3bl"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/billing_portal/sessions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_NciAYcXfLnqBoz \  --data-urlencode return_url="https://example.com/account"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/billing_portal/sessions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_NciAYcXfLnqBoz \  --data-urlencode return_url="https://example.com/account"
```

---

## Meter Event Adjustment

**URL:** https://docs.stripe.com/api/billing/meter-event-adjustment

**Contents:**
- Meter Event Adjustment
- The Meter Event Adjustment object
  - Attributes
    - objectstring
    - cancelnullable object
    - event_namestring
    - livemodeboolean
    - statusenum
    - typeenum
- Create a billing meter event adjustment

A billing meter event adjustment is a resource that allows you to cancel a meter event. For example, you might create a billing meter event adjustment to cancel a meter event that was created in error or attached to the wrong customer.

String representing the object’s type. Objects of the same type share the same value.

Specifies which event to cancel.

The name of the meter event. Corresponds with the event_name field on a meter.

The maximum length is 100 characters.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The meter event adjustment’s status.

The event adjustment has been processed.

The event adjustment is still being processed.

Specifies whether to cancel a single event or a range of events for a time period. Time period cancellation is not supported yet.

Cancel a single meter event by identifier.

Creates a billing meter event adjustment.

The name of the meter event. Corresponds with the event_name field on a meter.

The maximum length is 100 characters.

Specifies whether to cancel a single event or a range of events for a time period. Time period cancellation is not supported yet.

Cancel a single meter event by identifier.

Specifies which event to cancel.

Returns a billing meter event adjustment.

**Examples:**

Example 1 (unknown):
```unknown
{  "object": "billing.meter_event_adjustment",  "livemode": false,  "status": "pending",  "event_name": "ai_search_api",  "type": "cancel",  "cancel": {    "identifier": "identifier_123"  }}
```

Example 2 (unknown):
```unknown
{  "object": "billing.meter_event_adjustment",  "livemode": false,  "status": "pending",  "event_name": "ai_search_api",  "type": "cancel",  "cancel": {    "identifier": "identifier_123"  }}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/billing/meter_event_adjustments \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d type=cancel \  -d event_name=ai_search_api \  -d "cancel[identifier]"=identifier_123
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/billing/meter_event_adjustments \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d type=cancel \  -d event_name=ai_search_api \  -d "cancel[identifier]"=identifier_123
```

---

## Credit Grant

**URL:** https://docs.stripe.com/api/billing/credit-grant

**Contents:**
- Credit Grant
- The Credit Grant object
  - Attributes
    - idstring
    - objectstring
    - amountobject
    - applicability_configobject
    - categoryenum
    - createdtimestamp
    - customerstringExpandable

A credit grant is an API resource that documents the allocation of some billing credits to a customer.

Related guide: Billing credits

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value.

Amount of this credit grant.

Configuration specifying what this credit grant applies to. We currently only support metered prices that have a Billing Meter attached to them.

The category of this credit grant. This is for tracking purposes and isn’t displayed to the customer.

The credit grant was purchased by the customer for some amount.

The credit grant was given to the customer for free.

Time at which the object was created. Measured in seconds since the Unix epoch.

ID of the customer receiving the billing credits.

ID of the account representing the customer receiving the billing credits

The time when the billing credits become effective-when they’re eligible for use.

The time when the billing credits expire. If not present, the billing credits don’t expire.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

A descriptive name shown in dashboard.

The priority for applying this credit grant. The highest priority is 0 and the lowest is 100.

ID of the test clock this credit grant belongs to.

Time at which the object was last updated. Measured in seconds since the Unix epoch.

The time when this credit grant was voided. If not present, the credit grant hasn’t been voided.

Creates a credit grant.

Amount of this credit grant.

Configuration specifying what this credit grant applies to. We currently only support metered prices that have a Billing Meter attached to them.

The category of this credit grant. It defaults to paid if not specified.

The credit grant was purchased by the customer for some amount.

The credit grant was given to the customer for free.

ID of the customer receiving the billing credits.

ID of the account representing the customer receiving the billing credits.

The time when the billing credits become effective-when they’re eligible for use. It defaults to the current timestamp if not specified.

The time when the billing credits expire. If not specified, the billing credits don’t expire.

Set of key-value pairs that you can attach to an object. You can use this to store additional information about the object (for example, cost basis) in a structured format.

A descriptive name shown in the Dashboard.

The maximum length is 100 characters.

The desired priority for applying this credit grant. If not specified, it will be set to the default value of 50. The highest priority is 0 and the lowest is 100.

Returns a credit grant.

Updates a credit grant.

Unique identifier for the object.

The time when the billing credits created by this credit grant expire. If set to empty, the billing credits never expire.

Set of key-value pairs you can attach to an object. You can use this to store additional information about the object (for example, cost basis) in a structured format.

Returns the updated credit grant.

Retrieves a credit grant.

Unique identifier for the object.

Returns a credit grant.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "credgr_test_61R9a6NUWsRmOW3RM41L6nFOS1ekDGHo",  "object": "billing.credit_grant",  "amount": {    "monetary": {      "currency": "usd",      "value": 1000    },    "type": "monetary"  },  "applicability_config": {    "scope": {      "price_type": "metered"    }  },  "category": "paid",  "created": 1726620803,  "customer": "cus_QrvQguzkIK8zTj",  "effective_at": 1729297860,  "expires_at": null,  "livemode": false,  "metadata": {},  "name": "Purchased Credits",  "priority": 50,  "test_clock": null,  "updated": 1726620803,  "voided_at": null}
```

Example 2 (unknown):
```unknown
{  "id": "credgr_test_61R9a6NUWsRmOW3RM41L6nFOS1ekDGHo",  "object": "billing.credit_grant",  "amount": {    "monetary": {      "currency": "usd",      "value": 1000    },    "type": "monetary"  },  "applicability_config": {    "scope": {      "price_type": "metered"    }  },  "category": "paid",  "created": 1726620803,  "customer": "cus_QrvQguzkIK8zTj",  "effective_at": 1729297860,  "expires_at": null,  "livemode": false,  "metadata": {},  "name": "Purchased Credits",  "priority": 50,  "test_clock": null,  "updated": 1726620803,  "voided_at": null}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/billing/credit_grants \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d name="Purchased Credits" \  -d customer=cus_QrvQguzkIK8zTj \  -d "amount[monetary][currency]"=usd \  -d "amount[monetary][value]"=1000 \  -d "amount[type]"=monetary \  -d "applicability_config[scope][price_type]"=metered \  -d category=paid
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/billing/credit_grants \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d name="Purchased Credits" \  -d customer=cus_QrvQguzkIK8zTj \  -d "amount[monetary][currency]"=usd \  -d "amount[monetary][value]"=1000 \  -d "amount[type]"=monetary \  -d "applicability_config[scope][price_type]"=metered \  -d category=paid
```

---

## Customers

**URL:** https://docs.stripe.com/invoicing/customer

**Contents:**
- Customers
- Learn how to use the Customer resource with Stripe Invoicing.
  - Compare Customers v1 and Accounts v2 references
    - Caution
    - Note
  - Create a customer
  - Customers page
  - Edit a customer
  - Delete a customer
- Customer profiles

If your Connect platform uses customer-configured Accounts, use our guide to replace Customer and event references in your code with the equivalent Accounts v2 API references.

Create a customer for every new user or business you want to bill. When you create a new customer, set up a minimal customer profile to help generate more useful invoices, and enable Smart Retries (if you’re an Invoicing Plus user). After you set up your customer, you can issue one-off invoices or create subscriptions.

Before you create a new customer, make sure that the customer doesn’t already exist in the Dashboard. Creating multiple customer entries for the same customer can cause you problems later on, such as when you need to reconcile transaction history or coordinate saved payment methods.

You can create and manage customers on the Customers page when you don’t want to use code to create a customer, or if you want to manually bill a customer with a one-off invoice.

You can also create a customer in the Dashboard during invoice creation.

When you create a new customer, you can set their account and billing information, such as Email, Name, and Country. You can also set a customer’s preferred language, currency, and other important details.

You can also perform these actions on the Customers page:

To create a customer, complete these steps:

Verify that the customer doesn’t already exist.

Click Add customer, or press N, on the Customers page.

At a minimum, enter your customer’s Name and Account email.

Click Add customer in the dialog.

To edit a customer’s profile, complete these steps:

Find the customer you want to modify and click the name on the Customers page.

In the account information page, select Actions > Edit information.

Make your changes to the customer profile.

Click Update customer.

To delete a customer, complete these steps:

Find the customer you want to delete on the Customers page.

Click the checkbox next to your customer’s name followed by Delete. You can also click into the customer’s details page and select Actions > Delete customer.

​​Use a basic customer profile for invoice and receipt generation or as a lightweight customer relationship management system (CRM) for your application. To create a minimal customer profile, set these properties:

Stripe uses your customer’s email address to notify them of payment failures. Stripe also uses email addresses to notify customers when they need to perform an action to complete a payment.

Store the internal customer ID for your application in the metadata attribute. Like most Stripe resources, the Customer resource includes a Metadata object hash to flexibly store contextual key-value information. To aid in auditing and support, store your internal customer ID as a key-value pair on the Customer resource. This allows you to search for the customer using your internal reference ID. We recommend storing Stripe customer IDs against the internal customer model of your application.

Use the address attributes to set a billing address for invoicing and credit notes. For physical good delivery, add a shipping address.

Invoices, credit notes, and receipts display the billing address—a common requirement for tax compliance.

When you create a customer, use the Language dropdown to add their preferred language. (You can also add or edit a customer’s preferred language in the Customer details page or when creating an invoice.) Stripe uses the chosen language to localize invoice emails and PDFs, receipt emails and PDFs, and credit note PDFs.

To update the language through the API, use the preferred_locales parameter. This parameter accepts an ordered list of preferred languages sorted by preference. These preferred locale values are based on RFC-4646. Examples include en for English, or fr-CA for Canadian French. To learn more, see Customer preferred languages.

The following table contains additional customer properties:

Here are some of the common tasks you can perform with the Customer resource:

Send an invoice to a customer: After you create the customer, you can send them an invoice.

Store a customer credit balance: The customer credit balance feature allows you to assign credit and debit adjustments to a specific customer and then apply the resulting balance toward future invoices for them.

Add and validate tax ID numbers: Displaying a customer’s tax ID on an invoice is a common requirement, and Stripe allows you to add multiple tax IDs to a customer. Their tax IDs display in the header of invoice and credit note PDFs. See the Customer tax IDs page for more details.

Set the currency for a customer: You can set the default currency to charge a customer for invoices using the Dashboard by navigating to the Customers page, selecting your customer, and clicking Edit next to Details. See the Multi-currency customers page for more details on billing the same customer using a different currency than their default currency.

Create customers in bulk: Bulk upload Customers using Productivity Stripe Apps.

---

## Subscriptions

**URL:** https://docs.stripe.com/api/subscriptions

**Contents:**
- Subscriptions
- The Subscription object
  - Attributes
    - idstring
    - automatic_taxobject
    - currencyenum
    - customerstringExpandable
    - customer_accountnullable string
    - default_payment_methodnullable stringExpandable
    - descriptionnullable string

Subscriptions allow you to charge a customer on a recurring basis.

Related guide: Creating subscriptions

Unique identifier for the object.

Automatic tax settings for this subscription.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

ID of the customer who owns the subscription.

ID of the account representing the customer who owns the subscription.

ID of the default payment method for the subscription. It must belong to the customer associated with the subscription. This takes precedence over default_source. If neither are set, invoices will use the customer’s invoice_settings.default_payment_method or default_source.

The subscription’s description, meant to be displayable to the customer. Use this field to optionally store an explanation of the subscription for rendering in Stripe surfaces and certain local payment methods UIs.

The maximum length is 500 characters.

List of subscription items, each with an attached price.

The most recent invoice this subscription has generated.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

You can use this SetupIntent to collect user authentication when creating a subscription without immediate payment or updating a subscription’s payment method, allowing you to optimize for off-session payments. Learn more in the SCA Migration Guide.

If specified, pending updates that will be applied to the subscription once the latest_invoice has been paid.

Possible values are incomplete, incomplete_expired, trialing, active, past_due, canceled, unpaid, or paused.

For collection_method=charge_automatically a subscription moves into incomplete if the initial payment attempt fails. A subscription in this status can only have metadata and default_source updated. Once the first invoice is paid, the subscription moves into an active status. If the first invoice is not paid within 23 hours, the subscription transitions to incomplete_expired. This is a terminal status, the open invoice will be voided and no further invoices will be generated.

A subscription that is currently in a trial period is trialing and moves to active when the trial period is over.

A subscription can only enter a paused status when a trial ends without a payment method. A paused subscription doesn’t generate invoices and can be resumed after your customer adds their payment method. The paused status is different from pausing collection, which still generates invoices and leaves the subscription’s status unchanged.

If subscription collection_method=charge_automatically, it becomes past_due when payment is required but cannot be paid (due to failed payment or awaiting additional user actions). Once Stripe has exhausted all payment retry attempts, the subscription will become canceled or unpaid (depending on your subscriptions settings).

If subscription collection_method=send_invoice it becomes past_due when its invoice is not paid by the due date, and canceled or unpaid if it is still not paid by an additional deadline after that. Note that when a subscription has a status of unpaid, no subsequent invoices will be attempted (invoices will be created, but then immediately automatically closed). After receiving updated payment information from a customer, you may choose to reopen and pay their closed invoices.

Creates a new subscription on an existing customer. Each customer can have up to 500 active or scheduled subscriptions.

When you create a subscription with collection_method=charge_automatically, the first invoice is finalized as part of the request. The payment_behavior parameter determines the exact behavior of the initial payment.

To start subscriptions where the first invoice always begins in a draft status, use subscription schedules instead. Schedules provide the flexibility to model more complex billing configurations that change over time.

Automatic tax settings for this subscription.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

The identifier of the customer to subscribe.

The identifier of the account representing the customer to subscribe.

ID of the default payment method for the subscription. It must belong to the customer associated with the subscription. This takes precedence over default_source. If neither are set, invoices will use the customer’s invoice_settings.default_payment_method or default_source.

The subscription’s description, meant to be displayable to the customer. Use this field to optionally store an explanation of the subscription for rendering in Stripe surfaces and certain local payment methods UIs.

The maximum length is 500 characters.

A list of up to 20 subscription items, each with an attached price.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Only applies to subscriptions with collection_method=charge_automatically.

Use allow_incomplete to create Subscriptions with status=incomplete if the first invoice can’t be paid. Creating Subscriptions with this status allows you to manage scenarios where additional customer actions are needed to pay a subscription’s invoice. For example, SCA regulation may require 3DS authentication to complete payment. See the SCA Migration Guide for Billing to learn more. This is the default behavior.

Use default_incomplete to create Subscriptions with status=incomplete when the first invoice requires payment, otherwise start as active. Subscriptions transition to status=active when successfully confirming the PaymentIntent on the first invoice. This allows simpler management of scenarios where additional customer actions are needed to pay a subscription’s invoice, such as failed payments, SCA regulation, or collecting a mandate for a bank debit payment method. If the PaymentIntent is not confirmed within 23 hours Subscriptions transition to status=incomplete_expired, which is a terminal state.

Use error_if_incomplete if you want Stripe to return an HTTP 402 status code if a subscription’s first invoice can’t be paid. For example, if a payment method requires 3DS authentication due to SCA regulation and further customer action is needed, this parameter doesn’t create a Subscription and returns an error instead. This was the default behavior for API versions prior to 2019-03-14. See the changelog to learn more.

pending_if_incomplete is only used with updates and cannot be passed when creating a Subscription.

Subscriptions with collection_method=send_invoice are automatically activated regardless of the first Invoice status.

The newly created Subscription object, if the call succeeded. If the attempted charge fails, the subscription is created in an incomplete status.

Updates an existing subscription to match the specified parameters. When changing prices or quantities, we optionally prorate the price we charge next month to make up for any price changes. To preview how the proration is calculated, use the create preview endpoint.

By default, we prorate subscription changes. For example, if a customer signs up on May 1 for a 100 USD price, they’ll be billed 100 USD immediately. If on May 15 they switch to a 200 USD price, then on June 1 they’ll be billed 250 USD (200 USD for a renewal of her subscription, plus a 50 USD prorating adjustment for half of the previous month’s 100 USD difference). Similarly, a downgrade generates a credit that is applied to the next invoice. We also prorate when you make quantity changes.

Switching prices does not normally change the billing date or generate an immediate charge unless:

In these cases, we apply a credit for the unused time on the previous price, immediately charge the customer using the new price, and reset the billing date. Learn about how Stripe immediately attempts payment for subscription changes.

If you want to charge for an upgrade immediately, pass proration_behavior as always_invoice to create prorations, automatically invoice the customer for those proration adjustments, and attempt to collect payment. If you pass create_prorations, the prorations are created but not automatically invoiced. If you want to bill the customer for the prorations before the subscription’s renewal date, you need to manually invoice the customer.

If you don’t want to prorate, set the proration_behavior option to none. With this option, the customer is billed 100 USD on May 1 and 200 USD on June 1. Similarly, if you set proration_behavior to none when switching between different billing intervals (for example, from monthly to yearly), we don’t generate any credits for the old subscription’s unused time. We still reset the billing date and bill immediately for the new subscription.

Updating the quantity on a subscription many times in an hour may result in rate limiting. If you need to bill for a frequently changing quantity, consider integrating usage-based billing instead.

Automatic tax settings for this subscription. We recommend you only include this parameter when the existing value is being changed.

ID of the default payment method for the subscription. It must belong to the customer associated with the subscription. This takes precedence over default_source. If neither are set, invoices will use the customer’s invoice_settings.default_payment_method or default_source.

The subscription’s description, meant to be displayable to the customer. Use this field to optionally store an explanation of the subscription for rendering in Stripe surfaces and certain local payment methods UIs.

The maximum length is 500 characters.

A list of up to 20 subscription items, each with an attached price.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Use allow_incomplete to transition the subscription to status=past_due if a payment is required but cannot be paid. This allows you to manage scenarios where additional user actions are needed to pay a subscription’s invoice. For example, SCA regulation may require 3DS authentication to complete payment. See the SCA Migration Guide for Billing to learn more. This is the default behavior.

Use default_incomplete to transition the subscription to status=past_due when payment is required and await explicit confirmation of the invoice’s payment intent. This allows simpler management of scenarios where additional user actions are needed to pay a subscription’s invoice. Such as failed payments, SCA regulation, or collecting a mandate for a bank debit payment method.

Use pending_if_incomplete to update the subscription using pending updates. When you use pending_if_incomplete you can only pass the parameters supported by pending updates.

Use error_if_incomplete if you want Stripe to return an HTTP 402 status code if a subscription’s invoice cannot be paid. For example, if a payment method requires 3DS authentication due to SCA regulation and further user action is needed, this parameter does not update the subscription and returns an error instead. This was the default behavior for API versions prior to 2019-03-14. See the changelog to learn more.

Determines how to handle prorations when the billing cycle changes (e.g., when switching plans, resetting billing_cycle_anchor=now, or starting a trial), or if an item’s quantity changes. The default value is create_prorations.

Always invoice immediately for prorations.

Will cause proration invoice items to be created when applicable. These proration items will only be invoiced immediately under certain conditions.

Disable creating prorations in this request.

The newly updated Subscription object, if the call succeeded. If payment_behavior is error_if_incomplete and a charge is required for the update and it fails, this call raises an error, and the subscription update does not go into effect.

Retrieves the subscription with the given ID.

Returns the subscription object.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",  "object": "subscription",  "application": null,  "application_fee_percent": null,  "automatic_tax": {    "enabled": false,    "liability": null  },  "billing_cycle_anchor": 1679609767,  "cancel_at": null,  "cancel_at_period_end": false,  "canceled_at": null,  "cancellation_details": {    "comment": null,    "feedback": null,    "reason": null  },  "collection_method": "charge_automatically",  "created": 1679609767,  "currency": "usd",  "customer": "cus_Na6dX7aXxi11N4",  "days_until_due": null,  "default_payment_method": null,  "default_source": null,  "default_tax_rates": [],  "description": null,  "discounts": null,  "ended_at": null,  "invoice_settings": {    "issuer": {      "type": "self"    }  },  "items": {    "object": "list",    "data": [      {        "id": "si_Na6dzxczY5fwHx",        "object": "subscription_item",        "created": 1679609768,        "current_period_end": 1682288167,        "current_period_start": 1679609767,        "metadata": {},        "plan": {          "id": "price_1MowQULkdIwHu7ixraBm864M",          "object": "plan",          "active": true,          "amount": 1000,          "amount_decimal": "1000",          "billing_scheme": "per_unit",          "created": 1679609766,          "currency": "usd",          "discounts": null,          "interval": "month",          "interval_count": 1,          "livemode": false,          "metadata": {},          "nickname": null,          "product": "prod_Na6dGcTsmU0I4R",          "tiers_mode": null,          "transform_usage": null,          "trial_period_days": null,          "usage_type": "licensed"        },        "price": {          "id": "price_1MowQULkdIwHu7ixraBm864M",          "object": "price",          "active": true,          "billing_scheme": "per_unit",          "created": 1679609766,          "currency": "usd",          "custom_unit_amount": null,          "livemode": false,          "lookup_key": null,          "metadata": {},          "nickname": null,          "product": "prod_Na6dGcTsmU0I4R",          "recurring": {            "interval": "month",            "interval_count": 1,            "trial_period_days": null,            "usage_type": "licensed"          },          "tax_behavior": "unspecified",          "tiers_mode": null,          "transform_quantity": null,          "type": "recurring",          "unit_amount": 1000,          "unit_amount_decimal": "1000"        },        "quantity": 1,        "subscription": "sub_1MowQVLkdIwHu7ixeRlqHVzs",        "tax_rates": []      }    ],    "has_more": false,    "total_count": 1,    "url": "/v1/subscription_items?subscription=sub_1MowQVLkdIwHu7ixeRlqHVzs"  },  "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",  "livemode": false,  "metadata": {},  "next_pending_invoice_item_invoice": null,  "on_behalf_of": null,  "pause_collection": null,  "payment_settings": {    "payment_method_options": null,    "payment_method_types": null,    "save_default_payment_method": "off"  },  "pending_invoice_item_interval": null,  "pending_setup_intent": null,  "pending_update": null,  "schedule": null,  "start_date": 1679609767,  "status": "active",  "test_clock": null,  "transfer_data": null,  "trial_end": null,  "trial_settings": {    "end_behavior": {      "missing_payment_method": "create_invoice"    }  },  "trial_start": null}
```

Example 2 (unknown):
```unknown
{  "id": "sub_1MowQVLkdIwHu7ixeRlqHVzs",  "object": "subscription",  "application": null,  "application_fee_percent": null,  "automatic_tax": {    "enabled": false,    "liability": null  },  "billing_cycle_anchor": 1679609767,  "cancel_at": null,  "cancel_at_period_end": false,  "canceled_at": null,  "cancellation_details": {    "comment": null,    "feedback": null,    "reason": null  },  "collection_method": "charge_automatically",  "created": 1679609767,  "currency": "usd",  "customer": "cus_Na6dX7aXxi11N4",  "days_until_due": null,  "default_payment_method": null,  "default_source": null,  "default_tax_rates": [],  "description": null,  "discounts": null,  "ended_at": null,  "invoice_settings": {    "issuer": {      "type": "self"    }  },  "items": {    "object": "list",    "data": [      {        "id": "si_Na6dzxczY5fwHx",        "object": "subscription_item",        "created": 1679609768,        "current_period_end": 1682288167,        "current_period_start": 1679609767,        "metadata": {},        "plan": {          "id": "price_1MowQULkdIwHu7ixraBm864M",          "object": "plan",          "active": true,          "amount": 1000,          "amount_decimal": "1000",          "billing_scheme": "per_unit",          "created": 1679609766,          "currency": "usd",          "discounts": null,          "interval": "month",          "interval_count": 1,          "livemode": false,          "metadata": {},          "nickname": null,          "product": "prod_Na6dGcTsmU0I4R",          "tiers_mode": null,          "transform_usage": null,          "trial_period_days": null,          "usage_type": "licensed"        },        "price": {          "id": "price_1MowQULkdIwHu7ixraBm864M",          "object": "price",          "active": true,          "billing_scheme": "per_unit",          "created": 1679609766,          "currency": "usd",          "custom_unit_amount": null,          "livemode": false,          "lookup_key": null,          "metadata": {},          "nickname": null,          "product": "prod_Na6dGcTsmU0I4R",          "recurring": {            "interval": "month",            "interval_count": 1,            "trial_period_days": null,            "usage_type": "licensed"          },          "tax_behavior": "unspecified",          "tiers_mode": null,          "transform_quantity": null,          "type": "recurring",          "unit_amount": 1000,          "unit_amount_decimal": "1000"        },        "quantity": 1,        "subscription": "sub_1MowQVLkdIwHu7ixeRlqHVzs",        "tax_rates": []      }    ],    "has_more": false,    "total_count": 1,    "url": "/v1/subscription_items?subscription=sub_1MowQVLkdIwHu7ixeRlqHVzs"  },  "latest_invoice": "in_1MowQWLkdIwHu7ixuzkSPfKd",  "livemode": false,  "metadata": {},  "next_pending_invoice_item_invoice": null,  "on_behalf_of": null,  "pause_collection": null,  "payment_settings": {    "payment_method_options": null,    "payment_method_types": null,    "save_default_payment_method": "off"  },  "pending_invoice_item_interval": null,  "pending_setup_intent": null,  "pending_update": null,  "schedule": null,  "start_date": 1679609767,  "status": "active",  "test_clock": null,  "transfer_data": null,  "trial_end": null,  "trial_settings": {    "end_behavior": {      "missing_payment_method": "create_invoice"    }  },  "trial_start": null}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/subscriptions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_Na6dX7aXxi11N4 \  -d "items[0][price]"=price_1MowQULkdIwHu7ixraBm864M
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/subscriptions \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_Na6dX7aXxi11N4 \  -d "items[0][price]"=price_1MowQULkdIwHu7ixraBm864M
```

---

## Meter Event Summary

**URL:** https://docs.stripe.com/api/billing/meter-event-summary

**Contents:**
- Meter Event Summary
- The Meter Event Summary object
  - Attributes
    - idstring
    - objectstring
    - aggregated_valuefloat
    - end_timetimestamp
    - livemodeboolean
    - meterstring
    - start_timetimestamp

A billing meter event summary represents an aggregated view of a customer’s billing meter events within a specified timeframe. It indicates how much usage was accrued by a customer for that period.

Note: Meters events are aggregated asynchronously so the meter event summaries provide an eventually consistent view of the reported usage.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value.

Aggregated value of all the events within start_time (inclusive) and end_time (inclusive). The aggregation strategy is defined on meter via default_aggregation.

End timestamp for this event summary (exclusive). Must be aligned with minute boundaries.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The meter associated with this event summary.

Start timestamp for this event summary (inclusive). Must be aligned with minute boundaries.

Retrieve a list of billing meter event summaries.

The customer for which to fetch event summaries.

The timestamp from when to stop aggregating meter events (exclusive). Must be aligned with minute boundaries.

Unique identifier for the object.

The timestamp from when to start aggregating meter events (inclusive). Must be aligned with minute boundaries.

Specifies what granularity to use when generating event summaries. If not specified, a single event summary would be returned for the specified time range. For hourly granularity, start and end times must align with hour boundaries (e.g., 00:00, 01:00, …, 23:00). For daily granularity, start and end times must align with UTC day boundaries (00:00 UTC).

Generate event summaries per day.

Generate event summaries per hour.

Returns a list of billing meter event summaries.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "mtrusg_test_6041CMAXJrFdZ56U76ce6L35Hz7xA3Tn58z5sY7bq6gM3XN5bx5Y459D4Xt2E17ko6M86kt7kV3bl5PM7LV59l4sY50b6oU5QD7bY3HP58z5sY7bq6gM3Y57LF2Dr7od3Hb8927gh4Tt4Lo4xO4ge60T81C6Y53gl4QS2D33ft3HC3Xi3Cy3Cy3Cy",  "object": "billing.meter_event_summary",  "aggregated_value": 10,  "end_time": 1711659600,  "livemode": false,  "meter": "mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA",  "start_time": 1711656000}
```

Example 2 (unknown):
```unknown
{  "id": "mtrusg_test_6041CMAXJrFdZ56U76ce6L35Hz7xA3Tn58z5sY7bq6gM3XN5bx5Y459D4Xt2E17ko6M86kt7kV3bl5PM7LV59l4sY50b6oU5QD7bY3HP58z5sY7bq6gM3Y57LF2Dr7od3Hb8927gh4Tt4Lo4xO4ge60T81C6Y53gl4QS2D33ft3HC3Xi3Cy3Cy3Cy",  "object": "billing.meter_event_summary",  "aggregated_value": 10,  "end_time": 1711659600,  "livemode": false,  "meter": "mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA",  "start_time": 1711656000}
```

Example 3 (unknown):
```unknown
curl -G https://api.stripe.com/v1/billing/meters/mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA/event_summaries \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_Pp40waj64hdRxb \  -d start_time=1711584000 \  -d end_time=1711666800 \  -d value_grouping_window=hour
```

Example 4 (unknown):
```unknown
curl -G https://api.stripe.com/v1/billing/meters/mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA/event_summaries \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_Pp40waj64hdRxb \  -d start_time=1711584000 \  -d end_time=1711666800 \  -d value_grouping_window=hour
```

---

## Plans

**URL:** https://docs.stripe.com/api/plans

**Contents:**
- Plans
- The Plan object
  - Attributes
    - idstring
    - activeboolean
    - amountnullable integer
    - currencyenum
    - intervalenum
    - metadatanullable object
    - nicknamenullable string

You can now model subscriptions more flexibly using the Prices API. It replaces the Plans API and is backwards compatible to simplify your migration.

Plans define the base price, currency, and billing cycle for recurring purchases of products. Products help you track inventory or provisioning, and plans help you track pricing. Different physical goods or levels of service should be represented by products, and pricing options should be represented by plans. This approach lets you change prices without having to change your provisioning scheme.

For example, you might have a single “gold” product that has plans for $10/month, $100/year, €9/month, and €90/year.

Related guides: Set up a subscription and more about products and prices.

Unique identifier for the object.

Whether the plan can be used for new purchases.

The unit amount in cents to be charged, represented as a whole integer if possible. Only set if billing_scheme=per_unit.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

The frequency at which a subscription is billed. One of day, week, month or year.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

A brief description of the plan, hidden from customers.

The product whose pricing this plan determines.

You can now model subscriptions more flexibly using the Prices API. It replaces the Plans API and is backwards compatible to simplify your migration.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

Specifies billing frequency. Either day, week, month or year.

The product whose pricing the created plan will represent. This can either be the ID of an existing product, or a dictionary containing fields used to create a service product.

Whether the plan is currently available for new subscriptions. Defaults to true.

A positive integer in cents (or 0 for a free plan) representing how much to charge on a recurring basis.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

A brief description of the plan, hidden from customers.

Returns the plan object.

Updates the specified plan by setting the values of the parameters passed. Any parameters not provided are left unchanged. By design, you cannot change a plan’s ID, amount, currency, or billing cycle.

Whether the plan is currently available for new subscriptions.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

A brief description of the plan, hidden from customers.

The updated plan object is returned upon success. Otherwise, this call raises an error.

Retrieves the plan with the given ID.

Returns a plan if a valid plan ID was provided. Raises an error otherwise.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "plan_NjpIbv3g3ZibnD",  "object": "plan",  "active": true,  "amount": 1200,  "amount_decimal": "1200",  "billing_scheme": "per_unit",  "created": 1681851647,  "currency": "usd",  "interval": "month",  "interval_count": 1,  "livemode": false,  "metadata": {},  "nickname": null,  "product": "prod_NjpI7DbZx6AlWQ",  "tiers_mode": null,  "transform_usage": null,  "trial_period_days": null,  "usage_type": "licensed"}
```

Example 2 (unknown):
```unknown
{  "id": "plan_NjpIbv3g3ZibnD",  "object": "plan",  "active": true,  "amount": 1200,  "amount_decimal": "1200",  "billing_scheme": "per_unit",  "created": 1681851647,  "currency": "usd",  "interval": "month",  "interval_count": 1,  "livemode": false,  "metadata": {},  "nickname": null,  "product": "prod_NjpI7DbZx6AlWQ",  "tiers_mode": null,  "transform_usage": null,  "trial_period_days": null,  "usage_type": "licensed"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/plans \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=1200 \  -d currency=usd \  -d interval=month \  -d product=prod_NjpI7DbZx6AlWQ
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/plans \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d amount=1200 \  -d currency=usd \  -d interval=month \  -d product=prod_NjpI7DbZx6AlWQ
```

---

## Credit Balance Summary

**URL:** https://docs.stripe.com/api/billing/credit-balance-summary

**Contents:**
- Credit Balance Summary
- The Credit Balance Summary object
  - Attributes
    - objectstring
    - balancesarray of objects
    - customerstringExpandable
    - customer_accountnullable string
    - livemodeboolean
- Retrieve the credit balance summary for a customer
  - Parameters

Indicates the billing credit balance for billing credits granted to a customer.

String representing the object’s type. Objects of the same type share the same value.

The billing credit balances. One entry per credit grant currency. If a customer only has credit grants in a single currency, then this will have a single balance entry.

The customer the balance is for.

The account the balance is for.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Retrieves the credit balance summary for a customer.

The filter criteria for the credit balance summary.

The customer whose credit balance summary you’re retrieving.

The account representing the customer whose credit balance summary you’re retrieving.

Returns the credit balance summary.

**Examples:**

Example 1 (unknown):
```unknown
{  "object": "billing.credit_balance_summary",  "balances": [    {      "available_balance": {        "monetary": {          "currency": "usd",          "value": 1000        },        "type": "monetary"      },      "ledger_balance": {        "monetary": {          "currency": "usd",          "value": 1000        },        "type": "monetary"      }    }  ],  "customer": "cus_QsEHa3GKweMwih",  "livemode": false}
```

Example 2 (unknown):
```unknown
{  "object": "billing.credit_balance_summary",  "balances": [    {      "available_balance": {        "monetary": {          "currency": "usd",          "value": 1000        },        "type": "monetary"      },      "ledger_balance": {        "monetary": {          "currency": "usd",          "value": 1000        },        "type": "monetary"      }    }  ],  "customer": "cus_QsEHa3GKweMwih",  "livemode": false}
```

Example 3 (unknown):
```unknown
curl -G https://api.stripe.com/v1/billing/credit_balance_summary \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_QsEHa3GKweMwih \  -d "filter[type]"=credit_grant \  -d "filter[credit_grant]"=credgr_test_61R9rvFh1HgrFIoCp41L6nFOS1ekDCeW
```

Example 4 (unknown):
```unknown
curl -G https://api.stripe.com/v1/billing/credit_balance_summary \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_QsEHa3GKweMwih \  -d "filter[type]"=credit_grant \  -d "filter[credit_grant]"=credgr_test_61R9rvFh1HgrFIoCp41L6nFOS1ekDCeW
```

---

## Create a preview invoice

**URL:** https://docs.stripe.com/api/invoices/create_preview

**Contents:**
- Create a preview invoice
  - Parameters
    - automatic_taxobject
    - customerstring
    - customer_accountstring
    - subscriptionstring
  - More parametersExpand all
    - currencyenum
    - customer_detailsobject
    - discountsarray of objects

At any time, you can preview the upcoming invoice for a subscription or subscription schedule. This will show you all the charges that are pending, including subscription renewal charges, invoice item charges, etc. It will also show you any discounts that are applicable to the invoice.

You can also preview the effects of creating or updating a subscription or subscription schedule, including a preview of any prorations that will take place. To ensure that the actual proration is calculated exactly the same as the previewed proration, you should pass the subscription_details.proration_date parameter when doing the actual subscription update.

The recommended way to get only the prorations being previewed on the invoice is to consider line items where parent.subscription_item_details.proration is true.

Note that when you are viewing an upcoming invoice, you are simply viewing a preview – the invoice has not yet been created. As such, the upcoming invoice will not show up in invoice listing calls, and you cannot use the API to pay or edit the invoice. If you want to change the amount that your customer will be billed, you can add, remove, or update pending invoice items, or update the customer’s discount.

Note: Currency conversion calculations use the latest exchange rates. Exchange rates may vary between the time of the preview and the time of the actual invoice creation. Learn more

Settings for automatic tax lookup for this invoice preview.

The identifier of the customer whose upcoming invoice you’re retrieving. If automatic_tax is enabled then one of customer, customer_details, subscription, or schedule must be set.

The identifier of the account representing the customer whose upcoming invoice you’re retrieving. If automatic_tax is enabled then one of customer, customer_account, customer_details, subscription, or schedule must be set.

The identifier of the subscription for which you’d like to retrieve the upcoming invoice. If not provided, but a subscription_details.items is provided, you will preview creating a subscription with those items. If neither subscription nor subscription_details.items is provided, you will retrieve the next upcoming invoice from among the customer’s subscriptions.

Returns an invoice if valid customer information is provided. Raises an error otherwise.

Draft invoices are fully editable. Once an invoice is finalized, monetary values, as well as collection_method, become uneditable.

If you would like to stop the Stripe Billing engine from automatically finalizing, reattempting payments on, sending reminders for, or automatically reconciling invoices, pass auto_advance=false.

Controls whether Stripe performs automatic collection of the invoice.

Settings for automatic tax lookup for this invoice.

Either charge_automatically or send_invoice. This field can be updated only on draft invoices.

An arbitrary string attached to the object. Often useful for displaying to users. Referenced as ‘memo’ in the Dashboard.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the invoice object.

Retrieves the invoice with the given ID.

Returns an invoice object if a valid invoice ID was provided. Raises an error otherwise.

The invoice object contains a lines hash that contains information about the subscriptions and invoice items that have been applied to the invoice, as well as any prorations that Stripe has automatically calculated. Each line on the invoice has an amount attribute that represents the amount actually contributed to the invoice’s total. For invoice items and prorations, the amount attribute is the same as for the invoice item or proration respectively. For subscriptions, the amount may be different from the plan’s regular price depending on whether the invoice covers a trial period or the invoice period differs from the plan’s usual interval.

The invoice object has both a subtotal and a total. The subtotal represents the total before any discounts, while the total is the final amount to be charged to the customer after all coupons have been applied.

The invoice also has a next_payment_attempt attribute that tells you the next time (as a Unix timestamp) payment for the invoice will be automatically attempted. For invoices with manual payment collection, that have been closed, or that have reached the maximum number of retries (specified in your subscriptions settings), the next_payment_attempt will be null.

You can list all invoices, or list the invoices for a specific customer. The invoices are returned sorted by creation date, with the most recently created invoices appearing first.

Only return invoices for the customer specified by this customer ID.

Only return invoices for the account representing the customer specified by this account ID.

The status of the invoice, one of draft, open, paid, uncollectible, or void. Learn more

Only return invoices for the subscription specified by this subscription ID.

A dictionary with a data property that contains an array invoice attachments,

Permanently deletes a one-off invoice draft. This cannot be undone. Attempts to delete invoices that are no longer in a draft state will fail; once an invoice has been finalized or if an invoice is for a subscription, it must be voided.

A successfully deleted invoice. Otherwise, this call raises an error, such as if the invoice has already been deleted.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/invoices/create_preview \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_NeZwdNtLEOXuvB
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/invoices/create_preview \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_NeZwdNtLEOXuvB
```

Example 3 (unknown):
```unknown
{  "id": "upcoming_in_1MtHbELkdIwHu7ixl4OzzPMv",  "object": "invoice",  "account_country": "US",  "account_name": "Stripe Docs",  "account_tax_ids": null,  "amount_due": 0,  "amount_paid": 0,  "amount_overpaid": 0,  "amount_remaining": 0,  "amount_shipping": 0,  "application": null,  "application_fee_amount": null,  "attempt_count": 0,  "attempted": false,  "auto_advance": false,  "automatic_tax": {    "enabled": false,    "status": null  },  "billing_reason": "manual",  "collection_method": "charge_automatically",  "created": 1680644467,  "currency": "usd",  "custom_fields": null,  "customer": "cus_NeZwdNtLEOXuvB",  "customer_address": null,  "customer_email": "jennyrosen@example.com",  "customer_name": "Jenny Rosen",  "customer_phone": null,  "customer_shipping": null,  "customer_tax_exempt": "none",  "customer_tax_ids": [],  "default_payment_method": null,  "default_source": null,  "default_tax_rates": [],  "description": null,  "discounts": [],  "due_date": null,  "ending_balance": null,  "footer": null,  "from_invoice": null,  "hosted_invoice_url": null,  "invoice_pdf": null,  "last_finalization_error": null,  "latest_revision": null,  "lines": {    "object": "list",    "data": [],    "has_more": false,    "total_count": 0,    "url": "/v1/invoices/in_1MtHbELkdIwHu7ixl4OzzPMv/lines"  },  "livemode": false,  "metadata": {},  "next_payment_attempt": null,  "number": null,  "on_behalf_of": null,  "parent": null,  "payment_settings": {    "default_mandate": null,    "payment_method_options": null,    "payment_method_types": null  },  "period_end": 1680644467,  "period_start": 1680644467,  "post_payment_credit_notes_amount": 0,  "pre_payment_credit_notes_amount": 0,  "receipt_number": null,  "shipping_cost": null,  "shipping_details": null,  "starting_balance": 0,  "statement_descriptor": null,  "status": "draft",  "status_transitions": {    "finalized_at": null,    "marked_uncollectible_at": null,    "paid_at": null,    "voided_at": null  },  "subtotal": 0,  "subtotal_excluding_tax": 0,  "test_clock": null,  "total": 0,  "total_discount_amounts": [],  "total_excluding_tax": 0,  "total_taxes": [],  "webhooks_delivered_at": 1680644467}
```

Example 4 (unknown):
```unknown
{  "id": "upcoming_in_1MtHbELkdIwHu7ixl4OzzPMv",  "object": "invoice",  "account_country": "US",  "account_name": "Stripe Docs",  "account_tax_ids": null,  "amount_due": 0,  "amount_paid": 0,  "amount_overpaid": 0,  "amount_remaining": 0,  "amount_shipping": 0,  "application": null,  "application_fee_amount": null,  "attempt_count": 0,  "attempted": false,  "auto_advance": false,  "automatic_tax": {    "enabled": false,    "status": null  },  "billing_reason": "manual",  "collection_method": "charge_automatically",  "created": 1680644467,  "currency": "usd",  "custom_fields": null,  "customer": "cus_NeZwdNtLEOXuvB",  "customer_address": null,  "customer_email": "jennyrosen@example.com",  "customer_name": "Jenny Rosen",  "customer_phone": null,  "customer_shipping": null,  "customer_tax_exempt": "none",  "customer_tax_ids": [],  "default_payment_method": null,  "default_source": null,  "default_tax_rates": [],  "description": null,  "discounts": [],  "due_date": null,  "ending_balance": null,  "footer": null,  "from_invoice": null,  "hosted_invoice_url": null,  "invoice_pdf": null,  "last_finalization_error": null,  "latest_revision": null,  "lines": {    "object": "list",    "data": [],    "has_more": false,    "total_count": 0,    "url": "/v1/invoices/in_1MtHbELkdIwHu7ixl4OzzPMv/lines"  },  "livemode": false,  "metadata": {},  "next_payment_attempt": null,  "number": null,  "on_behalf_of": null,  "parent": null,  "payment_settings": {    "default_mandate": null,    "payment_method_options": null,    "payment_method_types": null  },  "period_end": 1680644467,  "period_start": 1680644467,  "post_payment_credit_notes_amount": 0,  "pre_payment_credit_notes_amount": 0,  "receipt_number": null,  "shipping_cost": null,  "shipping_details": null,  "starting_balance": 0,  "statement_descriptor": null,  "status": "draft",  "status_transitions": {    "finalized_at": null,    "marked_uncollectible_at": null,    "paid_at": null,    "voided_at": null  },  "subtotal": 0,  "subtotal_excluding_tax": 0,  "test_clock": null,  "total": 0,  "total_discount_amounts": [],  "total_excluding_tax": 0,  "total_taxes": [],  "webhooks_delivered_at": 1680644467}
```

---

## Using webhooks with subscriptions

**URL:** https://docs.stripe.com/billing/subscriptions/webhooks

**Contents:**
- Using webhooks with subscriptions
- Learn to use webhooks to receive notifications of subscription activity.
  - Compare Customers v1 and Accounts v2 references
- Subscription events
- Handle payment failures
- Handle payments that require additional action
- Track active subscriptions
- Catch subscription status changes
- Webhook endpoints and invoices
  - Webhook events related to invoice finalization

If your Connect platform uses customer-configured Accounts, use our guide to replace Customer and event references in your code with the equivalent Accounts v2 API references.

You receive notifications from Stripe in your app through webhook events. Use webhook events to manage subscriptions, as most activity happens asynchronously. Process these events at a webhook endpoint or other destinations like Amazon EventBridge by creating an event destination.

To use webhooks with your subscriptions:

If your application runs on AWS, you can configure Stripe to send events directly to AWS EventBridge in your AWS account.

Stripe triggers events every time a subscription is created or changed. Some events are sent immediately when a subscription is created, while others recur on regular billing periods.

Make sure that your integration properly handles the events. For example, you may want to email a customer if a payment fails or revoke a customer’s access when a subscription is canceled.

The following table describes the most common events related to subscriptions and, where applicable, suggests actions for handling the events.

invoice.payment_failed

A payment for an invoice failed. The PaymentIntent status changes to requires_action. The status of the subscription continues to be incomplete only for the subscription’s first invoice. If a payment fails, there are several possible actions to take:

Events provide a reliable way for Stripe to notify you of payment failures on subscription invoices. Some payment failures are temporary-for example, a card issuer might decline the initial charge but allow an automatic retry. Other payment failures are final and require action, like not having a usable payment method for the customer.

invoice.payment_failed

A payment for an invoice failed. The status of the PaymentIntent changes to requires_payment_method. The status of the subscription changes to incomplete. If a payment fails, there are several possible actions to take:

Some payment methods might require additional steps to complete, such as customer authentication. If you receive these events, your app must notify the customer to complete the required action. To learn how to handle events that require additional action, read the subscription overview guide.

invoice.payment_failed

A payment for an invoice failed. The PaymentIntent status changes to requires_action. The status of the subscription changes to incomplete. If a payment fails, there are several possible actions to take:

Subscriptions require coordination between your site and Stripe-the success or failure of a customer’s recurring payments determines whether they can continue to access to your product or service.

For typical integrations, you store customers’ credentials and a mapped timestamp value that represents the access expiration date for that customer on your site when a customer subscribes. When the customer logs in, you check whether the timestamp is still in the future. If the timestamp is in the future when the customer logs in, the account is active and the customer should still have access to the service.

When the subscription renews, Stripe bills the customer and tries to collect payment by either automatically charging the payment method on file, or emailing the invoice to customers. Stripe notifies your site of the invoice status by sending a webhook event:

Your site receives an invoice.paid event.

Your application finds the customer the payment was made for.

Your application updates the customer’s access expiration date in your database to the appropriate date in the future (plus a day or two for leeway).

Make sure that your integration properly monitors and handles transitions between the subscription statuses described in the following table.

Some status changes require special attention:

A few days before a trial ends and the subscription moves from trialing to active, you receive a customer.subscription.trial_will_end event. When you receive this event, verify that you have a payment method on the customer so you can bill them. Optionally, notify the customer that they will be charged.

When a subscription changes to past_due, notify the customer directly and ask them to update their payment details. Stripe offers several features that help automate this process-read more about revenue recovery.

When a subscription changes to canceled or unpaid, revoke access to your product.

Register a webhook endpoint to keep track of invoice statuses. Your subscription integration depends on correctly finalizing invoices and properly handling invoice finalization failures.

When you enable automatic collection, Stripe automatically finalizes and begins automatic collection of the invoice.

See a complete list of invoice event types.

Stripe waits an hour after receiving a successful response to the invoice.created event before attempting payment. If we don’t receive a successful response within 72 hours, we attempt to finalize and send the invoice.

In case you want to treat one-off invoices differently than subscription invoices, check the subscription property in the webhook body. This indicates whether the invoice was created for a subscription.

In live mode, if your webhook endpoint doesn’t respond properly, Stripe continues retrying the webhook notification for up to 3 days with an exponential back off. In a sandbox, we retry three times over a few hours. During that time, we won’t attempt to charge the customer unless we receive a successful response. We’ll also send you an email to notify you that the webhook is failing.

This behavior applies to all webhook endpoints defined on your account, including cases where a Connect application or other third-party service is having trouble handling incoming webhooks.

If Stripe can’t finalize an invoice, it sends a invoice.finalization_failed event to your webhook endpoint. Subscriptions remain active if invoices can’t be finalized, which means that users may still be able to access your product while you’re not able to collect payments. Make sure to take action on invoices that fail finalization. You can’t collect payments on an invoice that isn’t finalized.

To determine why the invoice finalization failed, look at the Invoice object’s last_finalization_error field, which provides more information about the failure, including how to proceed.

If you’re using Stripe Tax, check if the automatic_tax.status field is requires_location_inputs, indicating that the address details are invalid or insufficient. If Stripe Tax can’t find a recognized customer location, we can’t finalize the invoice. Learn how to handle invoice finalization failures.

To test your webhook endpoint or event destination, choose one of these two options:

---

## Stripe's APIs

**URL:** https://docs.stripe.com/apis

**Contents:**
- Stripe's APIs
- Learn about Stripe's APIs.
- Overview
- Authentication and security
- Make requests
- Testing and data
- Error handling

Stripe provides a unified set of REST APIs, comprised of two namespaces, for accepting payments, managing billing and subscriptions, sending payouts, and building financial workflows. You can authenticate requests, shape responses, localize data, test integrations, and handle errors consistently across Stripe products.

Learn about Stripe’s API v2, its response model, and how it compares to API v1.

Request dependent values in a single response.

Understand throttling and throughput behavior.

Authenticate requests with secret and restricted keys.

Best practices for creating, rotating, and securing keys.

Pass account and idempotency context with requests.

Allowlist domains and IP ranges used by Stripe.

Return nested objects in a single request.

Iterate through large lists of resources.

Look up objects in your Stripe data.

Attach custom key-value pairs to objects.

Common patterns for modeling data with metadata.

Test your application’s behavior and ability to handle errors.

Interpret errors and display them to users.

Work with low-level error details.

Browse common error types and parameters.

---

## Search subscriptions

**URL:** https://docs.stripe.com/api/subscriptions/search

**Contents:**
- Search subscriptions
  - Parameters
    - querystringRequired
    - limitinteger
    - pagestring
  - Returns

Search for subscriptions you’ve previously created using Stripe’s Search Query Language. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.

The search query string. See search query language and the list of supported query fields for subscriptions.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A dictionary with a data property that contains an array of up to limit subscriptions. If no objects match the query, the resulting array will be empty. See the related guide on expanding properties in lists.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v1/subscriptions/search \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  --data-urlencode query="status:'active' AND metadata['order_id']:'6735'"
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v1/subscriptions/search \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  --data-urlencode query="status:'active' AND metadata['order_id']:'6735'"
```

Example 3 (unknown):
```unknown
{  "object": "search_result",  "url": "/v1/subscriptions/search",  "has_more": false,  "data": [    {      "id": "sub_1MoG3CLkdIwHu7ixd86qvAfe",      "object": "subscription",      "application": null,      "application_fee_percent": null,      "automatic_tax": {        "enabled": false,        "liability": null      },      "billing_cycle_anchor": 1679446874,      "cancel_at": null,      "cancel_at_period_end": false,      "canceled_at": null,      "cancellation_details": {        "comment": null,        "feedback": null,        "reason": null      },      "collection_method": "charge_automatically",      "created": 1679446874,      "currency": "usd",      "customer": "cus_NZOq6LNU39H6ZI",      "days_until_due": null,      "default_payment_method": null,      "default_source": null,      "default_tax_rates": [],      "description": null,      "discounts": null,      "ended_at": null,      "invoice_settings": {        "issuer": {          "type": "self"        }      },      "items": {        "object": "list",        "data": [          {            "id": "si_NZOqmziODmZt2v",            "object": "subscription_item",            "created": 1679446875,            "current_period_end": 1682125274,            "current_period_start": 1679446874,            "metadata": {},            "plan": {              "id": "price_1MoG3BLkdIwHu7ixrHMcmj3f",              "object": "plan",              "active": true,              "amount": 1099,              "amount_decimal": "1099",              "billing_scheme": "per_unit",              "created": 1679446873,              "currency": "usd",              "interval": "month",              "interval_count": 1,              "livemode": false,              "metadata": {},              "nickname": null,              "product": "prod_NZOqsBJfaRYI1M",              "tiers_mode": null,              "transform_usage": null,              "trial_period_days": null,              "usage_type": "licensed"            },            "price": {              "id": "price_1MoG3BLkdIwHu7ixrHMcmj3f",              "object": "price",              "active": true,              "billing_scheme": "per_unit",              "created": 1679446873,              "currency": "usd",              "custom_unit_amount": null,              "livemode": false,              "lookup_key": null,              "metadata": {},              "nickname": null,              "product": "prod_NZOqsBJfaRYI1M",              "recurring": {                "interval": "month",                "interval_count": 1,                "trial_period_days": null,                "usage_type": "licensed"              },              "tax_behavior": "unspecified",              "tiers_mode": null,              "transform_quantity": null,              "type": "recurring",              "unit_amount": 1099,              "unit_amount_decimal": "1099"            },            "quantity": 1,            "subscription": "sub_1MoG3CLkdIwHu7ixd86qvAfe",            "tax_rates": []          }        ],        "has_more": false,        "total_count": 1,        "url": "/v1/subscription_items?subscription=sub_1MoG3CLkdIwHu7ixd86qvAfe"      },      "latest_invoice": "in_1MoG3CLkdIwHu7ixuBm2QIyW",      "livemode": false,      "metadata": {        "order_id": "6735"      },      "next_pending_invoice_item_invoice": null,      "on_behalf_of": null,      "pause_collection": null,      "payment_settings": {        "payment_method_options": null,        "payment_method_types": null,        "save_default_payment_method": "off"      },      "pending_invoice_item_interval": null,      "pending_setup_intent": null,      "pending_update": null,      "plan": {        "id": "price_1MoG3BLkdIwHu7ixrHMcmj3f",        "object": "plan",        "active": true,        "amount": 1099,        "amount_decimal": "1099",        "billing_scheme": "per_unit",        "created": 1679446873,        "currency": "usd",        "interval": "month",        "interval_count": 1,        "livemode": false,        "metadata": {},        "nickname": null,        "product": "prod_NZOqsBJfaRYI1M",        "tiers_mode": null,        "transform_usage": null,        "trial_period_days": null,        "usage_type": "licensed"      },      "quantity": 1,      "schedule": null,      "start_date": 1679446874,      "status": "active",      "test_clock": null,      "transfer_data": null,      "trial_end": null,      "trial_settings": {        "end_behavior": {          "missing_payment_method": "create_invoice"        }      },      "trial_start": null    }  ]}
```

Example 4 (unknown):
```unknown
{  "object": "search_result",  "url": "/v1/subscriptions/search",  "has_more": false,  "data": [    {      "id": "sub_1MoG3CLkdIwHu7ixd86qvAfe",      "object": "subscription",      "application": null,      "application_fee_percent": null,      "automatic_tax": {        "enabled": false,        "liability": null      },      "billing_cycle_anchor": 1679446874,      "cancel_at": null,      "cancel_at_period_end": false,      "canceled_at": null,      "cancellation_details": {        "comment": null,        "feedback": null,        "reason": null      },      "collection_method": "charge_automatically",      "created": 1679446874,      "currency": "usd",      "customer": "cus_NZOq6LNU39H6ZI",      "days_until_due": null,      "default_payment_method": null,      "default_source": null,      "default_tax_rates": [],      "description": null,      "discounts": null,      "ended_at": null,      "invoice_settings": {        "issuer": {          "type": "self"        }      },      "items": {        "object": "list",        "data": [          {            "id": "si_NZOqmziODmZt2v",            "object": "subscription_item",            "created": 1679446875,            "current_period_end": 1682125274,            "current_period_start": 1679446874,            "metadata": {},            "plan": {              "id": "price_1MoG3BLkdIwHu7ixrHMcmj3f",              "object": "plan",              "active": true,              "amount": 1099,              "amount_decimal": "1099",              "billing_scheme": "per_unit",              "created": 1679446873,              "currency": "usd",              "interval": "month",              "interval_count": 1,              "livemode": false,              "metadata": {},              "nickname": null,              "product": "prod_NZOqsBJfaRYI1M",              "tiers_mode": null,              "transform_usage": null,              "trial_period_days": null,              "usage_type": "licensed"            },            "price": {              "id": "price_1MoG3BLkdIwHu7ixrHMcmj3f",              "object": "price",              "active": true,              "billing_scheme": "per_unit",              "created": 1679446873,              "currency": "usd",              "custom_unit_amount": null,              "livemode": false,              "lookup_key": null,              "metadata": {},              "nickname": null,              "product": "prod_NZOqsBJfaRYI1M",              "recurring": {                "interval": "month",                "interval_count": 1,                "trial_period_days": null,                "usage_type": "licensed"              },              "tax_behavior": "unspecified",              "tiers_mode": null,              "transform_quantity": null,              "type": "recurring",              "unit_amount": 1099,              "unit_amount_decimal": "1099"            },            "quantity": 1,            "subscription": "sub_1MoG3CLkdIwHu7ixd86qvAfe",            "tax_rates": []          }        ],        "has_more": false,        "total_count": 1,        "url": "/v1/subscription_items?subscription=sub_1MoG3CLkdIwHu7ixd86qvAfe"      },      "latest_invoice": "in_1MoG3CLkdIwHu7ixuBm2QIyW",      "livemode": false,      "metadata": {        "order_id": "6735"      },      "next_pending_invoice_item_invoice": null,      "on_behalf_of": null,      "pause_collection": null,      "payment_settings": {        "payment_method_options": null,        "payment_method_types": null,        "save_default_payment_method": "off"      },      "pending_invoice_item_interval": null,      "pending_setup_intent": null,      "pending_update": null,      "plan": {        "id": "price_1MoG3BLkdIwHu7ixrHMcmj3f",        "object": "plan",        "active": true,        "amount": 1099,        "amount_decimal": "1099",        "billing_scheme": "per_unit",        "created": 1679446873,        "currency": "usd",        "interval": "month",        "interval_count": 1,        "livemode": false,        "metadata": {},        "nickname": null,        "product": "prod_NZOqsBJfaRYI1M",        "tiers_mode": null,        "transform_usage": null,        "trial_period_days": null,        "usage_type": "licensed"      },      "quantity": 1,      "schedule": null,      "start_date": 1679446874,      "status": "active",      "test_clock": null,      "transfer_data": null,      "trial_end": null,      "trial_settings": {        "end_behavior": {          "missing_payment_method": "create_invoice"        }      },      "trial_start": null    }  ]}
```

---

## Resume a subscription

**URL:** https://docs.stripe.com/api/subscriptions/resume

**Contents:**
- Resume a subscription
  - Parameters
    - billing_cycle_anchorenum
    - proration_behaviorenum
  - More parametersExpand all
    - proration_datetimestamp
  - Returns
- Search subscriptions
  - Parameters
    - querystringRequired

Initiates resumption of a paused subscription, optionally resetting the billing cycle anchor and creating prorations. If a resumption invoice is generated, it must be paid or marked uncollectible before the subscription will be unpaused. If payment succeeds the subscription will become active, and if payment fails the subscription will be past_due. The resumption invoice will void automatically if not paid by the expiration date.

The billing cycle anchor that applies when the subscription is resumed. Either now or unchanged. The default is now. For more information, see the billing cycle documentation.

Reset the subscription’s billing cycle anchor to the current time (in UTC) and start a new billing period.

Advance the subscription to the period that surrounds the current time without resetting the billing cycle anchor.

Determines how to handle prorations resulting from the billing_cycle_anchor being unchanged. When the billing_cycle_anchor is set to now (default value), no prorations are generated. If no value is passed, the default is create_prorations.

Always invoice immediately for prorations.

Will cause proration invoice items to be created when applicable. These proration items will only be invoiced immediately under certain conditions.

Disable creating prorations in this request.

The subscription object.

Search for subscriptions you’ve previously created using Stripe’s Search Query Language. Don’t use search in read-after-write flows where strict consistency is necessary. Under normal operating conditions, data is searchable in less than a minute. Occasionally, propagation of new or updated data can be up to an hour behind during outages. Search functionality is not available to merchants in India.

The search query string. See search query language and the list of supported query fields for subscriptions.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

A cursor for pagination across multiple pages of results. Don’t include this parameter on the first call. Use the next_page value returned in a previous response to request subsequent results.

A dictionary with a data property that contains an array of up to limit subscriptions. If no objects match the query, the resulting array will be empty. See the related guide on expanding properties in lists.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/subscriptions/sub_1MoGGtLkdIwHu7ixk5CfdiqC/resume \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d billing_cycle_anchor=now
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/subscriptions/sub_1MoGGtLkdIwHu7ixk5CfdiqC/resume \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d billing_cycle_anchor=now
```

Example 3 (unknown):
```unknown
{  "id": "sub_1MoGGtLkdIwHu7ixk5CfdiqC",  "object": "subscription",  "application": null,  "application_fee_percent": null,  "automatic_tax": {    "enabled": false,    "liability": null  },  "billing_cycle_anchor": 1679447726,  "cancel_at": null,  "cancel_at_period_end": false,  "canceled_at": null,  "cancellation_details": {    "comment": null,    "feedback": null,    "reason": null  },  "collection_method": "charge_automatically",  "created": 1679447723,  "currency": "usd",  "customer": "cus_NZP5i1diUz55jp",  "days_until_due": null,  "default_payment_method": null,  "default_source": null,  "default_tax_rates": [],  "description": null,  "discounts": null,  "ended_at": null,  "invoice_settings": {    "issuer": {      "type": "self"    }  },  "items": {    "object": "list",    "data": [      {        "id": "si_NZP5BhUIuWzXDG",        "object": "subscription_item",        "created": 1679447724,        "current_period_end": 1682126126,        "current_period_start": 1679447726,        "metadata": {},        "plan": {          "id": "price_1MoGGsLkdIwHu7ixA9yHsq2N",          "object": "plan",          "active": true,          "amount": 1099,          "amount_decimal": "1099",          "billing_scheme": "per_unit",          "created": 1679447722,          "currency": "usd",          "interval": "month",          "interval_count": 1,          "livemode": false,          "metadata": {},          "nickname": null,          "product": "prod_NZP5rEATBlScM9",          "tiers_mode": null,          "transform_usage": null,          "trial_period_days": null,          "usage_type": "licensed"        },        "price": {          "id": "price_1MoGGsLkdIwHu7ixA9yHsq2N",          "object": "price",          "active": true,          "billing_scheme": "per_unit",          "created": 1679447722,          "currency": "usd",          "custom_unit_amount": null,          "livemode": false,          "lookup_key": null,          "metadata": {},          "nickname": null,          "product": "prod_NZP5rEATBlScM9",          "recurring": {            "interval": "month",            "interval_count": 1,            "trial_period_days": null,            "usage_type": "licensed"          },          "tax_behavior": "unspecified",          "tiers_mode": null,          "transform_quantity": null,          "type": "recurring",          "unit_amount": 1099,          "unit_amount_decimal": "1099"        },        "quantity": 1,        "subscription": "sub_1MoGGtLkdIwHu7ixk5CfdiqC",        "tax_rates": []      }    ],    "has_more": false,    "total_count": 1,    "url": "/v1/subscription_items?subscription=sub_1MoGGtLkdIwHu7ixk5CfdiqC"  },  "latest_invoice": "in_1MoGGwLkdIwHu7ixHSrelo8X",  "livemode": false,  "metadata": {},  "next_pending_invoice_item_invoice": null,  "on_behalf_of": null,  "pause_collection": null,  "payment_settings": {    "payment_method_options": null,    "payment_method_types": null,    "save_default_payment_method": "off"  },  "pending_invoice_item_interval": null,  "pending_setup_intent": null,  "pending_update": null,  "plan": {    "id": "price_1MoGGsLkdIwHu7ixA9yHsq2N",    "object": "plan",    "active": true,    "amount": 1099,    "amount_decimal": "1099",    "billing_scheme": "per_unit",    "created": 1679447722,    "currency": "usd",    "interval": "month",    "interval_count": 1,    "livemode": false,    "metadata": {},    "nickname": null,    "product": "prod_NZP5rEATBlScM9",    "tiers_mode": null,    "transform_usage": null,    "trial_period_days": null,    "usage_type": "licensed"  },  "quantity": 1,  "schedule": null,  "start_date": 1679447723,  "status": "active",  "test_clock": null,  "transfer_data": null,  "trial_end": null,  "trial_settings": {    "end_behavior": {      "missing_payment_method": "create_invoice"    }  },  "trial_start": null}
```

Example 4 (unknown):
```unknown
{  "id": "sub_1MoGGtLkdIwHu7ixk5CfdiqC",  "object": "subscription",  "application": null,  "application_fee_percent": null,  "automatic_tax": {    "enabled": false,    "liability": null  },  "billing_cycle_anchor": 1679447726,  "cancel_at": null,  "cancel_at_period_end": false,  "canceled_at": null,  "cancellation_details": {    "comment": null,    "feedback": null,    "reason": null  },  "collection_method": "charge_automatically",  "created": 1679447723,  "currency": "usd",  "customer": "cus_NZP5i1diUz55jp",  "days_until_due": null,  "default_payment_method": null,  "default_source": null,  "default_tax_rates": [],  "description": null,  "discounts": null,  "ended_at": null,  "invoice_settings": {    "issuer": {      "type": "self"    }  },  "items": {    "object": "list",    "data": [      {        "id": "si_NZP5BhUIuWzXDG",        "object": "subscription_item",        "created": 1679447724,        "current_period_end": 1682126126,        "current_period_start": 1679447726,        "metadata": {},        "plan": {          "id": "price_1MoGGsLkdIwHu7ixA9yHsq2N",          "object": "plan",          "active": true,          "amount": 1099,          "amount_decimal": "1099",          "billing_scheme": "per_unit",          "created": 1679447722,          "currency": "usd",          "interval": "month",          "interval_count": 1,          "livemode": false,          "metadata": {},          "nickname": null,          "product": "prod_NZP5rEATBlScM9",          "tiers_mode": null,          "transform_usage": null,          "trial_period_days": null,          "usage_type": "licensed"        },        "price": {          "id": "price_1MoGGsLkdIwHu7ixA9yHsq2N",          "object": "price",          "active": true,          "billing_scheme": "per_unit",          "created": 1679447722,          "currency": "usd",          "custom_unit_amount": null,          "livemode": false,          "lookup_key": null,          "metadata": {},          "nickname": null,          "product": "prod_NZP5rEATBlScM9",          "recurring": {            "interval": "month",            "interval_count": 1,            "trial_period_days": null,            "usage_type": "licensed"          },          "tax_behavior": "unspecified",          "tiers_mode": null,          "transform_quantity": null,          "type": "recurring",          "unit_amount": 1099,          "unit_amount_decimal": "1099"        },        "quantity": 1,        "subscription": "sub_1MoGGtLkdIwHu7ixk5CfdiqC",        "tax_rates": []      }    ],    "has_more": false,    "total_count": 1,    "url": "/v1/subscription_items?subscription=sub_1MoGGtLkdIwHu7ixk5CfdiqC"  },  "latest_invoice": "in_1MoGGwLkdIwHu7ixHSrelo8X",  "livemode": false,  "metadata": {},  "next_pending_invoice_item_invoice": null,  "on_behalf_of": null,  "pause_collection": null,  "payment_settings": {    "payment_method_options": null,    "payment_method_types": null,    "save_default_payment_method": "off"  },  "pending_invoice_item_interval": null,  "pending_setup_intent": null,  "pending_update": null,  "plan": {    "id": "price_1MoGGsLkdIwHu7ixA9yHsq2N",    "object": "plan",    "active": true,    "amount": 1099,    "amount_decimal": "1099",    "billing_scheme": "per_unit",    "created": 1679447722,    "currency": "usd",    "interval": "month",    "interval_count": 1,    "livemode": false,    "metadata": {},    "nickname": null,    "product": "prod_NZP5rEATBlScM9",    "tiers_mode": null,    "transform_usage": null,    "trial_period_days": null,    "usage_type": "licensed"  },  "quantity": 1,  "schedule": null,  "start_date": 1679447723,  "status": "active",  "test_clock": null,  "transfer_data": null,  "trial_end": null,  "trial_settings": {    "end_behavior": {      "missing_payment_method": "create_invoice"    }  },  "trial_start": null}
```

---

## Meter Events v2

**URL:** https://docs.stripe.com/api/v2/billing-meter

**Contents:**
- Meter Events v2
- The MeterEvent object
  - Attributes
    - objectstring, value is "v2.billing.meter_event"
    - createdtimestamp
    - event_namestring
    - identifierstring
    - livemodeboolean
    - payloadmap
    - timestamptimestamp

Meter events are used to report customer usage of your product or service. Meter events are associated with billing meters, which define the shape of the event’s payload and how those events are aggregated. Meter events are processed asynchronously, so they may not be immediately reflected in aggregates or on upcoming invoices.

String representing the object’s type. Objects of the same type share the same value of the object field.

The creation time of this meter event.

The name of the meter event. Corresponds with the event_name field on a meter.

A unique identifier for the event. If not provided, one will be generated. We recommend using a globally unique identifier for this. We’ll enforce uniqueness within a rolling 24 hour period.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The payload of the event. This must contain the fields corresponding to a meter’s customer_mapping.event_payload_key (default is stripe_customer_id) and value_settings.event_payload_key (default is value). Read more about the payload…

The time of the event. Must be within the past 35 calendar days or up to 5 minutes in the future. Defaults to current timestamp if not specified.

Creates a meter event. Events are validated synchronously, but are processed asynchronously. Supports up to 1,000 events per second in livemode. For higher rate-limits, please use meter event streams instead.

The name of the meter event. Corresponds with the event_name field on a meter.

The payload of the event. This must contain the fields corresponding to a meter’s customer_mapping.event_payload_key (default is stripe_customer_id) and value_settings.event_payload_key (default is value). Read more about the payload.

A unique identifier for the event. If not provided, one will be generated. We recommend using a globally unique identifier for this. We’ll enforce uniqueness within a rolling 24 hour period.

The time of the event. Must be within the past 35 calendar days or up to 5 minutes in the future. Defaults to current timestamp if not specified.

String representing the object’s type. Objects of the same type share the same value of the object field.

The creation time of this meter event.

The name of the meter event. Corresponds with the event_name field on a meter.

A unique identifier for the event. If not provided, one will be generated. We recommend using a globally unique identifier for this. We’ll enforce uniqueness within a rolling 24 hour period.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The payload of the event. This must contain the fields corresponding to a meter’s customer_mapping.event_payload_key (default is stripe_customer_id) and value_settings.event_payload_key (default is value). Read more about the payload…

The time of the event. Must be within the past 35 calendar days or up to 5 minutes in the future. Defaults to current timestamp if not specified.

The meter must be Active to submit events.

A meter event with a duplicate identifier has already been submitted.

A meter must exist to submit events.

The value must be a positive integer.

The payload must have a reference to the customer.

The payload must have a value.

Cannot create multiple usage events for the same customer, meter concurrently.

**Examples:**

Example 1 (unknown):
```unknown
{  "object": "v2.billing.meter_event",  "created": "2024-06-01T12:10:00.000Z",  "livemode": false,  "identifier": "idmp_12345678",  "event_name": "ai_search_api",  "timestamp": "2024-06-01T12:00:00.000Z",  "payload": {    "stripe_customer_id": "cus_12345678",    "value": "25"  }}
```

Example 2 (unknown):
```unknown
{  "object": "v2.billing.meter_event",  "created": "2024-06-01T12:10:00.000Z",  "livemode": false,  "identifier": "idmp_12345678",  "event_name": "ai_search_api",  "timestamp": "2024-06-01T12:00:00.000Z",  "payload": {    "stripe_customer_id": "cus_12345678",    "value": "25"  }}
```

Example 3 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/billing/meter_events \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "identifier": "idmp_12345678",    "event_name": "ai_search_api",    "timestamp": "2024-06-01T12:00:00.000Z",    "payload": {        "stripe_customer_id": "cus_12345678",        "value": "25"    }  }'
```

Example 4 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/billing/meter_events \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}" \  --json '{    "identifier": "idmp_12345678",    "event_name": "ai_search_api",    "timestamp": "2024-06-01T12:00:00.000Z",    "payload": {        "stripe_customer_id": "cus_12345678",        "value": "25"    }  }'
```

---

## Coupons

**URL:** https://docs.stripe.com/api/coupons

**Contents:**
- Coupons
- The Coupon object
  - Attributes
    - idstring
    - amount_offnullable integer
    - currencynullable enum
    - durationenum
    - metadatanullable object
    - namenullable string
    - percent_offnullable float

A coupon contains information about a percent-off or amount-off discount you might want to apply to a customer. Coupons may be applied to subscriptions, invoices, checkout sessions, quotes, and more. Coupons do not work with conventional one-off charges or payment intents.

Unique identifier for the object.

Amount (in the currency specified) that will be taken off the subtotal of any invoices for this customer.

If amount_off has been set, the three-letter ISO code for the currency of the amount to take off.

One of forever, once, or repeating. Describes how long a customer who applies this coupon will get the discount.

Applies to all charges from a subscription with this coupon applied.

Applies to the first charge from a subscription with this coupon applied.

Applies to charges in the first duration_in_months months from a subscription with this coupon applied.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Name of the coupon displayed to customers on for instance invoices or receipts.

Percent that will be taken off the subtotal of any invoices for this customer for the duration of the coupon. For example, a coupon with percent_off of 50 will make a $100 invoice $50 instead.

You can create coupons easily via the coupon management page of the Stripe dashboard. Coupon creation is also accessible via the API if you need to create coupons on the fly.

A coupon has either a percent_off or an amount_off and currency. If you set an amount_off, that amount will be subtracted from any invoice’s subtotal. For example, an invoice with a subtotal of 100 USD will have a final total of 0 USD if a coupon with an amount_off of 20000 is applied to it and an invoice with a subtotal of 300 USD will have a final total of 100 USD if a coupon with an amount_off of 20000 is applied to it.

A positive integer representing the amount to subtract from an invoice total (required if percent_off is not passed).

Three-letter ISO code for the currency of the amount_off parameter (required if amount_off is passed).

Specifies how long the discount will be in effect if used on a subscription. Defaults to once.

Applies to all charges from a subscription with this coupon applied.

Applies to the first charge from a subscription with this coupon applied.

Applies to charges in the first duration_in_months months from a subscription with this coupon applied.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Name of the coupon displayed to customers on, for instance invoices, or receipts. By default the id is shown if name is not set.

The maximum length is 40 characters.

A positive float larger than 0, and smaller or equal to 100, that represents the discount the coupon will apply (required if amount_off is not passed).

Returns the coupon object.

Updates the metadata of a coupon. Other coupon details (currency, duration, amount_off) are, by design, not editable.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Name of the coupon displayed to customers on, for instance invoices, or receipts. By default the id is shown if name is not set.

The maximum length is 40 characters.

The newly updated coupon object if the call succeeded. Otherwise, this call raises an error, such as if the coupon has been deleted.

Retrieves the coupon with the given ID.

Returns a coupon if a valid coupon ID was provided. Raises an error otherwise.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "jMT0WJUD",  "object": "coupon",  "amount_off": null,  "created": 1678037688,  "currency": null,  "duration": "repeating",  "duration_in_months": 3,  "livemode": false,  "max_redemptions": null,  "metadata": {},  "name": null,  "percent_off": 25.5,  "redeem_by": null,  "times_redeemed": 0,  "valid": true}
```

Example 2 (unknown):
```unknown
{  "id": "jMT0WJUD",  "object": "coupon",  "amount_off": null,  "created": 1678037688,  "currency": null,  "duration": "repeating",  "duration_in_months": 3,  "livemode": false,  "max_redemptions": null,  "metadata": {},  "name": null,  "percent_off": 25.5,  "redeem_by": null,  "times_redeemed": 0,  "valid": true}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/coupons \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d duration=forever \  -d percent_off="25.5"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/coupons \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d duration=forever \  -d percent_off="25.5"
```

---

## List all invoices

**URL:** https://docs.stripe.com/api/invoices/list

**Contents:**
- List all invoices
  - Parameters
    - customerstring
    - customer_accountstring
    - statusenum
    - subscriptionstring
  - More parametersExpand all
    - collection_methodenum
    - createdobject
    - ending_beforestring

You can list all invoices, or list the invoices for a specific customer. The invoices are returned sorted by creation date, with the most recently created invoices appearing first.

Only return invoices for the customer specified by this customer ID.

Only return invoices for the account representing the customer specified by this account ID.

The status of the invoice, one of draft, open, paid, uncollectible, or void. Learn more

Only return invoices for the subscription specified by this subscription ID.

A dictionary with a data property that contains an array invoice attachments,

Permanently deletes a one-off invoice draft. This cannot be undone. Attempts to delete invoices that are no longer in a draft state will fail; once an invoice has been finalized or if an invoice is for a subscription, it must be voided.

A successfully deleted invoice. Otherwise, this call raises an error, such as if the invoice has already been deleted.

Attaches a PaymentIntent or an Out of Band Payment to the invoice, adding it to the list of payments.

For the PaymentIntent, when the PaymentIntent’s status changes to succeeded, the payment is credited to the invoice, increasing its amount_paid. When the invoice is fully paid, the invoice’s status becomes paid.

If the PaymentIntent’s status is already succeeded when it’s attached, it’s credited to the invoice immediately.

See: Partial payments to learn more.

The ID of the PaymentIntent to attach to the invoice.

The ID of the PaymentRecord to attach to the invoice.

Returns the invoice object that the payment was attached to.

Stripe automatically finalizes drafts before sending and attempting payment on invoices. However, if you’d like to finalize a draft invoice manually, you can do so using this method.

Controls whether Stripe performs automatic collection of the invoice. If false, the invoice’s state doesn’t automatically advance without an explicit action.

Returns an invoice object with status=open.

Marking an invoice as uncollectible is useful for keeping track of bad debts that can be written off for accounting purposes.

Returns the invoice object.

**Examples:**

Example 1 (unknown):
```unknown
curl -G https://api.stripe.com/v1/invoices \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 2 (unknown):
```unknown
curl -G https://api.stripe.com/v1/invoices \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d limit=3
```

Example 3 (unknown):
```unknown
{  "object": "list",  "url": "/v1/invoices",  "has_more": false,  "data": [    {      "id": "in_1MtHbELkdIwHu7ixl4OzzPMv",      "object": "invoice",      "account_country": "US",      "account_name": "Stripe Docs",      "account_tax_ids": null,      "amount_due": 0,      "amount_paid": 0,      "amount_overpaid": 0,      "amount_remaining": 0,      "amount_shipping": 0,      "application": null,      "attempt_count": 0,      "attempted": false,      "auto_advance": false,      "automatic_tax": {        "enabled": false,        "liability": null,        "status": null      },      "billing_reason": "manual",      "collection_method": "charge_automatically",      "created": 1680644467,      "currency": "usd",      "custom_fields": null,      "customer": "cus_NeZwdNtLEOXuvB",      "customer_address": null,      "customer_email": "jennyrosen@example.com",      "customer_name": "Jenny Rosen",      "customer_phone": null,      "customer_shipping": null,      "customer_tax_exempt": "none",      "customer_tax_ids": [],      "default_payment_method": null,      "default_source": null,      "default_tax_rates": [],      "description": null,      "discounts": [],      "due_date": null,      "ending_balance": null,      "footer": null,      "from_invoice": null,      "hosted_invoice_url": null,      "invoice_pdf": null,      "issuer": {        "type": "self"      },      "last_finalization_error": null,      "latest_revision": null,      "lines": {        "object": "list",        "data": [],        "has_more": false,        "total_count": 0,        "url": "/v1/invoices/in_1MtHbELkdIwHu7ixl4OzzPMv/lines"      },      "livemode": false,      "metadata": {},      "next_payment_attempt": null,      "number": null,      "on_behalf_of": null,      "parent": null,      "payment_settings": {        "default_mandate": null,        "payment_method_options": null,        "payment_method_types": null      },      "period_end": 1680644467,      "period_start": 1680644467,      "post_payment_credit_notes_amount": 0,      "pre_payment_credit_notes_amount": 0,      "receipt_number": null,      "shipping_cost": null,      "shipping_details": null,      "starting_balance": 0,      "statement_descriptor": null,      "status": "draft",      "status_transitions": {        "finalized_at": null,        "marked_uncollectible_at": null,        "paid_at": null,        "voided_at": null      },      "subtotal": 0,      "subtotal_excluding_tax": 0,      "test_clock": null,      "total": 0,      "total_discount_amounts": [],      "total_excluding_tax": 0,      "total_taxes": [],      "webhooks_delivered_at": 1680644467    }  ]}
```

Example 4 (unknown):
```unknown
{  "object": "list",  "url": "/v1/invoices",  "has_more": false,  "data": [    {      "id": "in_1MtHbELkdIwHu7ixl4OzzPMv",      "object": "invoice",      "account_country": "US",      "account_name": "Stripe Docs",      "account_tax_ids": null,      "amount_due": 0,      "amount_paid": 0,      "amount_overpaid": 0,      "amount_remaining": 0,      "amount_shipping": 0,      "application": null,      "attempt_count": 0,      "attempted": false,      "auto_advance": false,      "automatic_tax": {        "enabled": false,        "liability": null,        "status": null      },      "billing_reason": "manual",      "collection_method": "charge_automatically",      "created": 1680644467,      "currency": "usd",      "custom_fields": null,      "customer": "cus_NeZwdNtLEOXuvB",      "customer_address": null,      "customer_email": "jennyrosen@example.com",      "customer_name": "Jenny Rosen",      "customer_phone": null,      "customer_shipping": null,      "customer_tax_exempt": "none",      "customer_tax_ids": [],      "default_payment_method": null,      "default_source": null,      "default_tax_rates": [],      "description": null,      "discounts": [],      "due_date": null,      "ending_balance": null,      "footer": null,      "from_invoice": null,      "hosted_invoice_url": null,      "invoice_pdf": null,      "issuer": {        "type": "self"      },      "last_finalization_error": null,      "latest_revision": null,      "lines": {        "object": "list",        "data": [],        "has_more": false,        "total_count": 0,        "url": "/v1/invoices/in_1MtHbELkdIwHu7ixl4OzzPMv/lines"      },      "livemode": false,      "metadata": {},      "next_payment_attempt": null,      "number": null,      "on_behalf_of": null,      "parent": null,      "payment_settings": {        "default_mandate": null,        "payment_method_options": null,        "payment_method_types": null      },      "period_end": 1680644467,      "period_start": 1680644467,      "post_payment_credit_notes_amount": 0,      "pre_payment_credit_notes_amount": 0,      "receipt_number": null,      "shipping_cost": null,      "shipping_details": null,      "starting_balance": 0,      "statement_descriptor": null,      "status": "draft",      "status_transitions": {        "finalized_at": null,        "marked_uncollectible_at": null,        "paid_at": null,        "voided_at": null      },      "subtotal": 0,      "subtotal_excluding_tax": 0,      "test_clock": null,      "total": 0,      "total_discount_amounts": [],      "total_excluding_tax": 0,      "total_taxes": [],      "webhooks_delivered_at": 1680644467    }  ]}
```

---

## Meter Events

**URL:** https://docs.stripe.com/api/billing/meter-event

**Contents:**
- Meter Events
- The Meter Event object
  - Attributes
    - objectstring
    - createdtimestamp
    - event_namestring
    - identifierstring
    - livemodeboolean
    - payloadobject
    - timestamptimestamp

Meter events represent actions that customers take in your system. You can use meter events to bill a customer based on their usage. Meter events are associated with billing meters, which define both the contents of the event’s payload and how to aggregate those events.

String representing the object’s type. Objects of the same type share the same value.

Time at which the object was created. Measured in seconds since the Unix epoch.

The name of the meter event. Corresponds with the event_name field on a meter.

The maximum length is 100 characters.

A unique identifier for the event.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The payload of the event. This contains the fields corresponding to a meter’s customer_mapping.event_payload_key (default is stripe_customer_id) and value_settings.event_payload_key (default is value). Read more about the payload.

The timestamp passed in when creating the event. Measured in seconds since the Unix epoch.

Creates a billing meter event.

The name of the meter event. Corresponds with the event_name field on a meter.

The maximum length is 100 characters.

The payload of the event. This must contain the fields corresponding to a meter’s customer_mapping.event_payload_key (default is stripe_customer_id) and value_settings.event_payload_key (default is value). Read more about the payload.

A unique identifier for the event. If not provided, one is generated. We recommend using UUID-like identifiers. We will enforce uniqueness within a rolling period of at least 24 hours. The enforcement of uniqueness primarily addresses issues arising from accidental retries or other problems occurring within extremely brief time intervals. This approach helps prevent duplicate entries and ensures data integrity in high-frequency operations.

The maximum length is 100 characters.

The time of the event. Measured in seconds since the Unix epoch. Must be within the past 35 calendar days or up to 5 minutes in the future. Defaults to current timestamp if not specified.

Returns a billing meter event.

**Examples:**

Example 1 (unknown):
```unknown
{  "object": "billing.meter_event",  "created": 1704824589,  "event_name": "ai_search_api",  "identifier": "identifier_123",  "livemode": true,  "payload": {    "value": "25",    "stripe_customer_id": "cus_NciAYcXfLnqBoz"  },  "timestamp": 1680210639}
```

Example 2 (unknown):
```unknown
{  "object": "billing.meter_event",  "created": 1704824589,  "event_name": "ai_search_api",  "identifier": "identifier_123",  "livemode": true,  "payload": {    "value": "25",    "stripe_customer_id": "cus_NciAYcXfLnqBoz"  },  "timestamp": 1680210639}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/billing/meter_events \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d event_name=ai_search_api \  -d "payload[value]"=25 \  -d "payload[stripe_customer_id]"=cus_NciAYcXfLnqBoz \  -d identifier=identifier_123
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/billing/meter_events \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d event_name=ai_search_api \  -d "payload[value]"=25 \  -d "payload[stripe_customer_id]"=cus_NciAYcXfLnqBoz \  -d identifier=identifier_123
```

---

## Subscription Items

**URL:** https://docs.stripe.com/api/subscription_items

**Contents:**
- Subscription Items
- The Subscription Item object
  - Attributes
    - idstring
    - metadataobject
    - priceobject
    - quantitynullable integer
    - subscriptionstring
  - More attributesExpand all
    - objectstring

Subscription items allow you to create customer subscriptions with more than one plan, making it easy to represent complex billing relationships.

Unique identifier for the object.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The price the customer is subscribed to.

The quantity of the plan to which the customer should be subscribed.

The subscription this subscription_item belongs to.

Adds a new item to an existing subscription. No existing items will be changed or replaced.

The identifier of the subscription to modify.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Use allow_incomplete to transition the subscription to status=past_due if a payment is required but cannot be paid. This allows you to manage scenarios where additional user actions are needed to pay a subscription’s invoice. For example, SCA regulation may require 3DS authentication to complete payment. See the SCA Migration Guide for Billing to learn more. This is the default behavior.

Use default_incomplete to transition the subscription to status=past_due when payment is required and await explicit confirmation of the invoice’s payment intent. This allows simpler management of scenarios where additional user actions are needed to pay a subscription’s invoice. Such as failed payments, SCA regulation, or collecting a mandate for a bank debit payment method.

Use pending_if_incomplete to update the subscription using pending updates. When you use pending_if_incomplete you can only pass the parameters supported by pending updates.

Use error_if_incomplete if you want Stripe to return an HTTP 402 status code if a subscription’s invoice cannot be paid. For example, if a payment method requires 3DS authentication due to SCA regulation and further user action is needed, this parameter does not update the subscription and returns an error instead. This was the default behavior for API versions prior to 2019-03-14. See the changelog to learn more.

The ID of the price object.

Determines how to handle prorations when the billing cycle changes (e.g., when switching plans, resetting billing_cycle_anchor=now, or starting a trial), or if an item’s quantity changes. The default value is create_prorations.

Always invoice immediately for prorations.

Will cause proration invoice items to be created when applicable. These proration items will only be invoiced immediately under certain conditions.

Disable creating prorations in this request.

The quantity you’d like to apply to the subscription item you’re creating.

Returns the created Subscription Item object, if successful. Otherwise, this call raises an error.

Updates the plan or quantity of an item on a current subscription.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Use allow_incomplete to transition the subscription to status=past_due if a payment is required but cannot be paid. This allows you to manage scenarios where additional user actions are needed to pay a subscription’s invoice. For example, SCA regulation may require 3DS authentication to complete payment. See the SCA Migration Guide for Billing to learn more. This is the default behavior.

Use default_incomplete to transition the subscription to status=past_due when payment is required and await explicit confirmation of the invoice’s payment intent. This allows simpler management of scenarios where additional user actions are needed to pay a subscription’s invoice. Such as failed payments, SCA regulation, or collecting a mandate for a bank debit payment method.

Use pending_if_incomplete to update the subscription using pending updates. When you use pending_if_incomplete you can only pass the parameters supported by pending updates.

Use error_if_incomplete if you want Stripe to return an HTTP 402 status code if a subscription’s invoice cannot be paid. For example, if a payment method requires 3DS authentication due to SCA regulation and further user action is needed, this parameter does not update the subscription and returns an error instead. This was the default behavior for API versions prior to 2019-03-14. See the changelog to learn more.

The ID of the price object. One of price or price_data is required. When changing a subscription item’s price, quantity is set to 1 unless a quantity parameter is provided.

Determines how to handle prorations when the billing cycle changes (e.g., when switching plans, resetting billing_cycle_anchor=now, or starting a trial), or if an item’s quantity changes. The default value is create_prorations.

Always invoice immediately for prorations.

Will cause proration invoice items to be created when applicable. These proration items will only be invoiced immediately under certain conditions.

Disable creating prorations in this request.

The quantity you’d like to apply to the subscription item you’re creating.

Retrieves the subscription item with the given ID.

Returns a subscription item if a valid subscription item ID was provided. Raises an error otherwise.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "si_NcLYdDxLHxlFo7",  "object": "subscription_item",  "created": 1680126546,  "metadata": {},  "price": {    "id": "price_1Mr6rdLkdIwHu7ixwPmiybbR",    "object": "price",    "active": true,    "billing_scheme": "per_unit",    "created": 1680126545,    "currency": "usd",    "custom_unit_amount": null,    "discounts": null,    "livemode": false,    "lookup_key": null,    "metadata": {},    "nickname": null,    "product": "prod_NcLYGKH0eY5b8s",    "recurring": {      "interval": "month",      "interval_count": 1,      "trial_period_days": null,      "usage_type": "licensed"    },    "tax_behavior": "unspecified",    "tiers_mode": null,    "transform_quantity": null,    "type": "recurring",    "unit_amount": 1000,    "unit_amount_decimal": "1000"  },  "quantity": 2,  "subscription": "sub_1Mr6rbLkdIwHu7ix4Xm9Ahtd",  "tax_rates": []}
```

Example 2 (unknown):
```unknown
{  "id": "si_NcLYdDxLHxlFo7",  "object": "subscription_item",  "created": 1680126546,  "metadata": {},  "price": {    "id": "price_1Mr6rdLkdIwHu7ixwPmiybbR",    "object": "price",    "active": true,    "billing_scheme": "per_unit",    "created": 1680126545,    "currency": "usd",    "custom_unit_amount": null,    "discounts": null,    "livemode": false,    "lookup_key": null,    "metadata": {},    "nickname": null,    "product": "prod_NcLYGKH0eY5b8s",    "recurring": {      "interval": "month",      "interval_count": 1,      "trial_period_days": null,      "usage_type": "licensed"    },    "tax_behavior": "unspecified",    "tiers_mode": null,    "transform_quantity": null,    "type": "recurring",    "unit_amount": 1000,    "unit_amount_decimal": "1000"  },  "quantity": 2,  "subscription": "sub_1Mr6rbLkdIwHu7ix4Xm9Ahtd",  "tax_rates": []}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/subscription_items \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d subscription=sub_1Mr6rbLkdIwHu7ix4Xm9Ahtd \  -d price=price_1Mr6rdLkdIwHu7ixwPmiybbR \  -d quantity=2
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/subscription_items \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d subscription=sub_1Mr6rbLkdIwHu7ix4Xm9Ahtd \  -d price=price_1Mr6rdLkdIwHu7ixwPmiybbR \  -d quantity=2
```

---

## Debit connected accounts

**URL:** https://docs.stripe.com/connect/account-debits

**Contents:**
- Debit connected accounts
- Collect funds from a connected account by debiting its Stripe balance.
    - Note
- Requirements
    - Note
- Availability
  - Domestic availability
  - International availability
- Charge a connected account
- See also

At times, your platform might need to collect funds from your connected accounts:

When your platform is responsible for negative balances, such as with Express and Custom connected accounts, you can debit a connected account’s Stripe balance, transferring funds to your platform balance.

To bill connected accounts where Stripe is responsible for negative balances, create a customer for each connected account and charge them using Stripe Billing subscriptions.

This creates a Transfer on the connected account and a Payment on the platform account.

This functionality is only supported for connected accounts where your platform is responsible for negative balances, including Express and Custom accounts. Additionally:

Contact the sales team if you need to discuss adjusting these requirements.

Account debits are available for platforms and connected accounts according to whether they’re in the same region (domestic) or cross-border regions (international).

You can use account debits when the platform and connected account are both in one of the following regions:

You can use cross-border account debits when the platform and connected account match the following corridors:

If you’re interested in other regions, contact our sales team.

To pull funds from a connected account:

---

## The Invoice object

**URL:** https://docs.stripe.com/api/invoices/object

**Contents:**
- The Invoice object
  - Attributes
    - idstring
    - auto_advanceboolean
    - automatic_taxobject
    - collection_methodenum
    - confirmation_secretnullable objectExpandable
    - currencyenum
    - customerstringExpandable
    - customer_accountnullable string

Unique identifier for the object. For preview invoices created using the create preview endpoint, this id will be prefixed with upcoming_in.

Controls whether Stripe performs automatic collection of the invoice. If false, the invoice’s state doesn’t automatically advance without an explicit action.

Settings and latest results for automatic tax lookup for this invoice.

Either charge_automatically, or send_invoice. When charging automatically, Stripe will attempt to pay this invoice using the default source attached to the customer. When sending an invoice, Stripe will email this invoice to the customer with payment instructions.

Attempt payment using the default source attached to the customer.

Email payment instructions to the customer.

The confirmation secret associated with this invoice. Currently, this contains the client_secret of the PaymentIntent that Stripe creates during invoice finalization.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

The ID of the customer to bill.

The ID of the account representing the customer to bill.

An arbitrary string attached to the object. Often useful for displaying to users. Referenced as ‘memo’ in the Dashboard.

The URL for the hosted invoice page, which allows customers to view and pay an invoice. If the invoice has not been finalized yet, this will be null.

The individual line items that make up the invoice. lines is sorted as follows: (1) pending invoice items (including prorations) in reverse chronological order, (2) subscription items in reverse chronological order, and (3) invoice items added after invoice creation in chronological order.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

The parent that generated this invoice

End of the usage period during which invoice items were added to this invoice. This looks back one period for a subscription invoice. Use the line item period to get the service period for each price.

Start of the usage period during which invoice items were added to this invoice. This looks back one period for a subscription invoice. Use the line item period to get the service period for each price.

The status of the invoice, one of draft, open, paid, uncollectible, or void. Learn more

Total after discounts and taxes.

This endpoint creates a draft invoice for a given customer. The invoice remains a draft until you finalize the invoice, which allows you to pay or send the invoice to your customers.

Controls whether Stripe performs automatic collection of the invoice. If false, the invoice’s state doesn’t automatically advance without an explicit action. Defaults to false.

Settings for automatic tax lookup for this invoice.

Either charge_automatically, or send_invoice. When charging automatically, Stripe will attempt to pay this invoice using the default source attached to the customer. When sending an invoice, Stripe will email this invoice to the customer with payment instructions. Defaults to charge_automatically.

The ID of the customer to bill.

The ID of the account to bill.

An arbitrary string attached to the object. Often useful for displaying to users. Referenced as ‘memo’ in the Dashboard.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

The ID of the subscription to invoice, if any. If set, the created invoice will only include pending invoice items for that subscription. The subscription’s billing cycle and regular subscription events won’t be affected.

Returns the invoice object. Raises an error if the customer ID provided is invalid.

At any time, you can preview the upcoming invoice for a subscription or subscription schedule. This will show you all the charges that are pending, including subscription renewal charges, invoice item charges, etc. It will also show you any discounts that are applicable to the invoice.

You can also preview the effects of creating or updating a subscription or subscription schedule, including a preview of any prorations that will take place. To ensure that the actual proration is calculated exactly the same as the previewed proration, you should pass the subscription_details.proration_date parameter when doing the actual subscription update.

The recommended way to get only the prorations being previewed on the invoice is to consider line items where parent.subscription_item_details.proration is true.

Note that when you are viewing an upcoming invoice, you are simply viewing a preview – the invoice has not yet been created. As such, the upcoming invoice will not show up in invoice listing calls, and you cannot use the API to pay or edit the invoice. If you want to change the amount that your customer will be billed, you can add, remove, or update pending invoice items, or update the customer’s discount.

Note: Currency conversion calculations use the latest exchange rates. Exchange rates may vary between the time of the preview and the time of the actual invoice creation. Learn more

Settings for automatic tax lookup for this invoice preview.

The identifier of the customer whose upcoming invoice you’re retrieving. If automatic_tax is enabled then one of customer, customer_details, subscription, or schedule must be set.

The identifier of the account representing the customer whose upcoming invoice you’re retrieving. If automatic_tax is enabled then one of customer, customer_account, customer_details, subscription, or schedule must be set.

The identifier of the subscription for which you’d like to retrieve the upcoming invoice. If not provided, but a subscription_details.items is provided, you will preview creating a subscription with those items. If neither subscription nor subscription_details.items is provided, you will retrieve the next upcoming invoice from among the customer’s subscriptions.

Returns an invoice if valid customer information is provided. Raises an error otherwise.

Draft invoices are fully editable. Once an invoice is finalized, monetary values, as well as collection_method, become uneditable.

If you would like to stop the Stripe Billing engine from automatically finalizing, reattempting payments on, sending reminders for, or automatically reconciling invoices, pass auto_advance=false.

Controls whether Stripe performs automatic collection of the invoice.

Settings for automatic tax lookup for this invoice.

Either charge_automatically or send_invoice. This field can be updated only on draft invoices.

An arbitrary string attached to the object. Often useful for displaying to users. Referenced as ‘memo’ in the Dashboard.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.

Returns the invoice object.

Retrieves the invoice with the given ID.

Returns an invoice object if a valid invoice ID was provided. Raises an error otherwise.

The invoice object contains a lines hash that contains information about the subscriptions and invoice items that have been applied to the invoice, as well as any prorations that Stripe has automatically calculated. Each line on the invoice has an amount attribute that represents the amount actually contributed to the invoice’s total. For invoice items and prorations, the amount attribute is the same as for the invoice item or proration respectively. For subscriptions, the amount may be different from the plan’s regular price depending on whether the invoice covers a trial period or the invoice period differs from the plan’s usual interval.

The invoice object has both a subtotal and a total. The subtotal represents the total before any discounts, while the total is the final amount to be charged to the customer after all coupons have been applied.

The invoice also has a next_payment_attempt attribute that tells you the next time (as a Unix timestamp) payment for the invoice will be automatically attempted. For invoices with manual payment collection, that have been closed, or that have reached the maximum number of retries (specified in your subscriptions settings), the next_payment_attempt will be null.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "in_1MtHbELkdIwHu7ixl4OzzPMv",  "object": "invoice",  "account_country": "US",  "account_name": "Stripe Docs",  "account_tax_ids": null,  "amount_due": 0,  "amount_paid": 0,  "amount_overpaid": 0,  "amount_remaining": 0,  "amount_shipping": 0,  "application": null,  "attempt_count": 0,  "attempted": false,  "auto_advance": false,  "automatic_tax": {    "enabled": false,    "liability": null,    "status": null  },  "billing_reason": "manual",  "collection_method": "charge_automatically",  "created": 1680644467,  "currency": "usd",  "custom_fields": null,  "customer": "cus_NeZwdNtLEOXuvB",  "customer_address": null,  "customer_email": "jennyrosen@example.com",  "customer_name": "Jenny Rosen",  "customer_phone": null,  "customer_shipping": null,  "customer_tax_exempt": "none",  "customer_tax_ids": [],  "confirmation_secret": null,  "default_payment_method": null,  "default_source": null,  "default_tax_rates": [],  "description": null,  "discounts": [],  "due_date": null,  "ending_balance": null,  "footer": null,  "from_invoice": null,  "hosted_invoice_url": null,  "invoice_pdf": null,  "issuer": {    "type": "self"  },  "last_finalization_error": null,  "latest_revision": null,  "lines": {    "object": "list",    "data": [],    "has_more": false,    "total_count": 0,    "url": "/v1/invoices/in_1MtHbELkdIwHu7ixl4OzzPMv/lines"  },  "payments": {    "object": "list",    "data": [],    "has_more": false,    "total_count": 0,    "url": "/v1/invoice_payments"  },  "livemode": false,  "metadata": {},  "next_payment_attempt": null,  "number": null,  "on_behalf_of": null,  "parent": null,  "payment_settings": {    "default_mandate": null,    "payment_method_options": null,    "payment_method_types": null  },  "period_end": 1680644467,  "period_start": 1680644467,  "post_payment_credit_notes_amount": 0,  "pre_payment_credit_notes_amount": 0,  "receipt_number": null,  "shipping_cost": null,  "shipping_details": null,  "starting_balance": 0,  "statement_descriptor": null,  "status": "draft",  "status_transitions": {    "finalized_at": null,    "marked_uncollectible_at": null,    "paid_at": null,    "voided_at": null  },  "subtotal": 0,  "subtotal_excluding_tax": 0,  "test_clock": null,  "total": 0,  "total_discount_amounts": [],  "total_excluding_tax": 0,  "total_taxes": [],  "transfer_data": null,  "webhooks_delivered_at": 1680644467}
```

Example 2 (unknown):
```unknown
{  "id": "in_1MtHbELkdIwHu7ixl4OzzPMv",  "object": "invoice",  "account_country": "US",  "account_name": "Stripe Docs",  "account_tax_ids": null,  "amount_due": 0,  "amount_paid": 0,  "amount_overpaid": 0,  "amount_remaining": 0,  "amount_shipping": 0,  "application": null,  "attempt_count": 0,  "attempted": false,  "auto_advance": false,  "automatic_tax": {    "enabled": false,    "liability": null,    "status": null  },  "billing_reason": "manual",  "collection_method": "charge_automatically",  "created": 1680644467,  "currency": "usd",  "custom_fields": null,  "customer": "cus_NeZwdNtLEOXuvB",  "customer_address": null,  "customer_email": "jennyrosen@example.com",  "customer_name": "Jenny Rosen",  "customer_phone": null,  "customer_shipping": null,  "customer_tax_exempt": "none",  "customer_tax_ids": [],  "confirmation_secret": null,  "default_payment_method": null,  "default_source": null,  "default_tax_rates": [],  "description": null,  "discounts": [],  "due_date": null,  "ending_balance": null,  "footer": null,  "from_invoice": null,  "hosted_invoice_url": null,  "invoice_pdf": null,  "issuer": {    "type": "self"  },  "last_finalization_error": null,  "latest_revision": null,  "lines": {    "object": "list",    "data": [],    "has_more": false,    "total_count": 0,    "url": "/v1/invoices/in_1MtHbELkdIwHu7ixl4OzzPMv/lines"  },  "payments": {    "object": "list",    "data": [],    "has_more": false,    "total_count": 0,    "url": "/v1/invoice_payments"  },  "livemode": false,  "metadata": {},  "next_payment_attempt": null,  "number": null,  "on_behalf_of": null,  "parent": null,  "payment_settings": {    "default_mandate": null,    "payment_method_options": null,    "payment_method_types": null  },  "period_end": 1680644467,  "period_start": 1680644467,  "post_payment_credit_notes_amount": 0,  "pre_payment_credit_notes_amount": 0,  "receipt_number": null,  "shipping_cost": null,  "shipping_details": null,  "starting_balance": 0,  "statement_descriptor": null,  "status": "draft",  "status_transitions": {    "finalized_at": null,    "marked_uncollectible_at": null,    "paid_at": null,    "voided_at": null  },  "subtotal": 0,  "subtotal_excluding_tax": 0,  "test_clock": null,  "total": 0,  "total_discount_amounts": [],  "total_excluding_tax": 0,  "total_taxes": [],  "transfer_data": null,  "webhooks_delivered_at": 1680644467}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/invoices \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_NeZwdNtLEOXuvB
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/invoices \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d customer=cus_NeZwdNtLEOXuvB
```

---

## Credit Balance Transaction

**URL:** https://docs.stripe.com/api/billing/credit-balance-transaction

**Contents:**
- Credit Balance Transaction
- The Credit Balance Transaction object
  - Attributes
    - idstring
    - objectstring
    - createdtimestamp
    - creditnullable object
    - credit_grantstringExpandable
    - debitnullable object
    - effective_attimestamp

A credit balance transaction is a resource representing a transaction (either a credit or a debit) against an existing credit grant.

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value.

Time at which the object was created. Measured in seconds since the Unix epoch.

Credit details for this credit balance transaction. Only present if type is credit.

The credit grant associated with this credit balance transaction.

Debit details for this credit balance transaction. Only present if type is debit.

The effective time of this credit balance transaction.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

ID of the test clock this credit balance transaction belongs to.

The type of credit balance transaction (credit or debit).

A credit transaction.

Retrieves a credit balance transaction.

Unique identifier for the object.

Returns a credit balance transaction.

Retrieve a list of credit balance transactions.

The credit grant for which to fetch credit balance transactions.

The customer whose credit balance transactions you’re retrieving.

The account representing the customer whose credit balance transactions you’re retrieving.

Returns a list of credit balance transactions.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "cbtxn_test_61R9ZljjaFmdidb6e41L6nFOS1ekD9Ue",  "object": "billing.credit_balance_transaction",  "created": 1726619524,  "credit": null,  "credit_grant": "credgr_test_61R9ZkIkIzLSp0xze41L6nFOS1ekDTPE",  "debit": {    "amount": {      "monetary": {        "currency": "usd",        "value": 1000      },      "type": "monetary"    },    "credits_applied": {      "invoice": "in_1Q0BoLL6nFOS1ekDbwBM5ER1",      "invoice_line_item": "il_1QB443L6nFOS1ekDwRiN3Z4n"    },    "type": "credits_applied"  },  "effective_at": 1729211351,  "livemode": false,  "test_clock": "clock_1Q0BoJL6nFOS1ekDbyYYuseM",  "type": "debit"}
```

Example 2 (unknown):
```unknown
{  "id": "cbtxn_test_61R9ZljjaFmdidb6e41L6nFOS1ekD9Ue",  "object": "billing.credit_balance_transaction",  "created": 1726619524,  "credit": null,  "credit_grant": "credgr_test_61R9ZkIkIzLSp0xze41L6nFOS1ekDTPE",  "debit": {    "amount": {      "monetary": {        "currency": "usd",        "value": 1000      },      "type": "monetary"    },    "credits_applied": {      "invoice": "in_1Q0BoLL6nFOS1ekDbwBM5ER1",      "invoice_line_item": "il_1QB443L6nFOS1ekDwRiN3Z4n"    },    "type": "credits_applied"  },  "effective_at": 1729211351,  "livemode": false,  "test_clock": "clock_1Q0BoJL6nFOS1ekDbyYYuseM",  "type": "debit"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/billing/credit_balance_transactions/cbtxn_test_61R9ZljjaFmdidb6e41L6nFOS1ekD9Ue \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/billing/credit_balance_transactions/cbtxn_test_61R9ZljjaFmdidb6e41L6nFOS1ekD9Ue \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:"
```

---

## Testing Stripe Billing

**URL:** https://docs.stripe.com/billing/testing

**Contents:**
- Testing Stripe Billing
- Learn how to test your Billing integration.
  - Testing resources
- Go-live principles
  - Compare Customers v1 and Accounts v2 references
- Test clocks
- Test subscription trial periods
  - Test trial periods without test clocks
- Test subscription webhook notifications
- Test payment failures

Thoroughly test your integration before you expose it to customers or use it for any live activity. Use the resources on this page in addition to any organizational guidelines (for example, runbooks, quality gates, or development checklists) to help determine whether your integration is production-ready.

Before taking your integration live, review these Stripe checklists:

Here’s what a typical integration flow looks like.

If your Connect platform uses customer-configured Accounts, use our guide to replace Customer and event references in your code with the equivalent Accounts v2 API references.

For subscription and recurring revenue integrations, make sure that, at a minimum, the following components work as expected.

The table lists the event notifications for each component. You can configure your integration to listen for these events with webhooks. Read this guide to learn more about event notifications and testing.

Test clocks allow you to simulate Billing objects, like subscriptions, through time in a sandbox so you don’t have to wait a year to see how your integration handles a payment failure for an annual renewal. You don’t need to write any code with test clocks: you can create simulations in the Dashboard. You can also access them through the API. Learn more about test clocks and common use cases for them.

First, follow these steps to start using test clocks:

Next, you can start testing trials with test clocks. Let’s say that you want customers to try your product for free with a seven-day trial before they start paying and want to collect payment information up front. To simulate this situation using test clocks, follow these steps:

To add a trial period to an existing subscription using the Dashboard:

Find the subscription you want to change.

Subscriptions integrations rely heavily on webhooks. You set up a webhook endpoint on your server and specify which event notifications to listen for. Stripe emits notifications for events like a subscription upgrade or cancellation.

You can test webhooks by either creating actual test subscriptions or by triggering event notifications with the Stripe CLI or through the Dashboard.

After you set up the Stripe CLI and link to your Stripe account, you can trigger events from the subscription lifecycle to test your webhook integration. If you use the Stripe CLI to trigger events, you can see event notifications on your server as they come in, which allows you to check your webhook integration directly without network tunnels or firewalls.

When you use the Stripe CLI or the Dashboard to trigger events, the event your webhook receives contains fake data that doesn’t correlate to subscription information. The most reliable way to test webhook notifications is to create actual test subscriptions and handle the corresponding events.

The following table describes the most common events related to subscriptions and, where applicable, suggests actions for handling the events.

invoice.payment_failed

A payment for an invoice failed. The PaymentIntent status changes to requires_action. The status of the subscription continues to be incomplete only for the subscription’s first invoice. If a payment fails, there are several possible actions to take:

Use specific test credit card numbers to trigger payment failures for subscriptions and invoices.

Some subscription updates cause Stripe to invoice the subscription and attempt payment immediately (this synchronous payment attempt can occur on the initial invoice, or on certain invoice updates). If this attempt fails, the subscription is created in an incomplete status.

To test the effects of payment failure on an active subscription, attach the 4000 0000 0000 0341 card as the customer’s default payment method, but use a trial period to defer the attempt (a trial of a few seconds or minutes is sufficient). The subscription becomes active immediately, with a draft invoice created when the trial period ends. It takes approximately one hour for the invoice status changes to open, at which time payment collection is attempted and fails.

Use test clocks to simulate the forward movement of time in a sandbox, which causes Billing resources, like Subscriptions, to change status and trigger webhook events. This allows you to see how your integration handles a payment failure for a quarterly or annual renewal without waiting a year.

Use the 4000 0027 6000 3184 card to simulate 3D Secure triggering for subscriptions and invoices.

When a 3D Secure authentication flow is triggered, you can test authenticating or failing the payment attempt in the 3DS dialog that opens. If the payment is authenticated successfully, the invoice is paid. If the invoice belongs to a subscription in an incomplete status, the subscription becomes active. When a payment attempt fails, the authentication attempt is unsuccessful and the invoice remains open.

To test manual payments on invoices through Bank Transfer:

Use specific test card IDs to simulate default payment methods being used for subscriptions and invoices.

The provided payment method must be attached to the subscription or invoice’s customer setting it as the default_payment method. For example, if using pm_card_visa to create a test Visa payment method:

Now, the subscription or invoice will charge this payment method.

Learn more about using default payment methods for subscriptions and invoices.

Use these magic tax IDs to trigger certain verification conditions in testing environments. The tax ID type must be either the EU VAT Number or Australian Business Number (ABN).

You can set up automated testing for your integration. To optimize the testing:

---

## Meters

**URL:** https://docs.stripe.com/api/billing/meter

**Contents:**
- Meters
- The Meter object
  - Attributes
    - idstring
    - objectstring
    - createdtimestamp
    - customer_mappingobject
    - default_aggregationobject
    - display_namestring
    - event_namestring

Meters specify how to aggregate meter events over a billing period. Meter events represent the actions that customers take in your system. Meters attach to prices and form the basis of the bill.

Related guide: Usage based billing

Unique identifier for the object.

String representing the object’s type. Objects of the same type share the same value.

Time at which the object was created. Measured in seconds since the Unix epoch.

Fields that specify how to map a meter event to a customer.

The default settings to aggregate a meter’s events with.

The name of the meter event to record usage for. Corresponds with the event_name field on meter events.

The time window which meter events have been pre-aggregated for, if any.

Events are pre-aggregated in daily buckets.

Events are pre-aggregated in hourly buckets.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The meter is inactive. No more events for this meter will be accepted. The meter cannot be attached to a price.

The timestamps at which the meter status changed.

Time at which the object was last updated. Measured in seconds since the Unix epoch.

Fields that specify how to calculate a meter event’s value.

Creates a billing meter.

The default settings to aggregate a meter’s events with.

The meter’s name. Not visible to the customer.

The maximum length is 250 characters.

The name of the meter event to record usage for. Corresponds with the event_name field on meter events.

The maximum length is 100 characters.

Fields that specify how to map a meter event to a customer.

The time window which meter events have been pre-aggregated for, if any.

Events are pre-aggregated in daily buckets.

Events are pre-aggregated in hourly buckets.

Fields that specify how to calculate a meter event’s value.

Returns a billing meter.

Updates a billing meter.

The meter’s name. Not visible to the customer.

The maximum length is 250 characters.

Returns a billing meter.

Retrieves a billing meter given an ID.

Returns a billing meter.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA",  "object": "billing.meter",  "created": 1704824589,  "customer_mapping": {    "type": "by_id",    "event_payload_key": "stripe_customer_id"  },  "default_aggregation": {    "formula": "sum"  },  "display_name": "Search API Calls",  "event_name": "ai_search_api",  "event_time_window": null,  "livemode": false,  "status": "active",  "status_transitions": {    "deactivated_at": null  },  "updated": 1704898330,  "value_settings": {    "event_payload_key": "value"  }}
```

Example 2 (unknown):
```unknown
{  "id": "mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA",  "object": "billing.meter",  "created": 1704824589,  "customer_mapping": {    "type": "by_id",    "event_payload_key": "stripe_customer_id"  },  "default_aggregation": {    "formula": "sum"  },  "display_name": "Search API Calls",  "event_name": "ai_search_api",  "event_time_window": null,  "livemode": false,  "status": "active",  "status_transitions": {    "deactivated_at": null  },  "updated": 1704898330,  "value_settings": {    "event_payload_key": "value"  }}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/billing/meters \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d display_name="Search API Calls" \  -d event_name=ai_search_api \  -d "default_aggregation[formula]"=sum \  -d "value_settings[event_payload_key]"=value \  -d "customer_mapping[type]"=by_id \  -d "customer_mapping[event_payload_key]"=stripe_customer_id
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/billing/meters \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d display_name="Search API Calls" \  -d event_name=ai_search_api \  -d "default_aggregation[formula]"=sum \  -d "value_settings[event_payload_key]"=value \  -d "customer_mapping[type]"=by_id \  -d "customer_mapping[event_payload_key]"=stripe_customer_id
```

---

## Meter Event Streams v2

**URL:** https://docs.stripe.com/api/v2/billing-meter-stream

**Contents:**
- Meter Event Streams v2
- The MeterEventSession object
  - Attributes
    - idstring
    - objectstring, value is "v2.billing.meter_event_session"
    - authentication_tokenstring
    - createdtimestamp
    - expires_attimestamp
    - livemodeboolean
- Create billing meter event stream authentication session v2

You can send a higher-throughput of meter events using meter event streams. For this flow, you must first create a meter event session, which will provide you with a session token. You can then create meter events through the meter event stream endpoint, using the session token for authentication. The session tokens are short-lived and you will need to create a new meter event session when the token expires.

The unique id of this auth session.

String representing the object’s type. Objects of the same type share the same value of the object field.

The authentication token for this session. Use this token when calling the high-throughput meter event API.

The creation time of this session.

The time at which this session will expire.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Creates a meter event session to send usage on the high-throughput meter event stream. Authentication tokens are only valid for 15 minutes, so you will need to create a new meter event session when your token expires.

The unique id of this auth session.

String representing the object’s type. Objects of the same type share the same value of the object field.

The authentication token for this session. Use this token when calling the high-throughput meter event API.

The creation time of this session.

The time at which this session will expire.

Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Creates meter events. Events are processed asynchronously, including validation. Requires a meter event session for authentication. Supports up to 10,000 requests per second in livemode. For even higher rate-limits, contact sales.

List of meter events to include in the request. Supports up to 100 events per request.

No response attributes.

The temporary session token has expired.

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "<AUTH_SESSION_ID>",  "livemode": "false",  "object": "v2.billing.meter_event_session",  "authentication_token": "token_12345678",  "created": "2024-06-01T12:00:00.000Z",  "expires_at": "2024-06-01T12:15:00.000Z"}
```

Example 2 (unknown):
```unknown
{  "id": "<AUTH_SESSION_ID>",  "livemode": "false",  "object": "v2.billing.meter_event_session",  "authentication_token": "token_12345678",  "created": "2024-06-01T12:00:00.000Z",  "expires_at": "2024-06-01T12:15:00.000Z"}
```

Example 3 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/billing/meter_event_session \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

Example 4 (unknown):
```unknown
curl -X POST https://api.stripe.com/v2/billing/meter_event_session \  -H "Authorization: Bearer sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE" \  -H "Stripe-Version: {{STRIPE_API_VERSION}}"
```

---

## Prices

**URL:** https://docs.stripe.com/api/prices

**Contents:**
- Prices
- The Price object
  - Attributes
    - idstring
    - activeboolean
    - currencyenum
    - metadataobject
    - nicknamenullable string
    - productstringExpandable
    - recurringnullable object

Prices define the unit cost, currency, and (optional) billing cycle for both recurring and one-time purchases of products. Products help you track inventory or provisioning, and prices help you track payment terms. Different physical goods or levels of service should be represented by products, and pricing options should be represented by prices. This approach lets you change prices without having to change your provisioning scheme.

For example, you might have a single “gold” product that has prices for $10/month, $100/year, and €9 once.

Related guides: Set up a subscription, create an invoice, and more about products and prices.

Unique identifier for the object.

Whether the price can be used for new purchases.

Three-letter ISO currency code, in lowercase. Must be a supported currency.

Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

A brief description of the price, hidden from customers.

The ID of the product this price is associated with.

The recurring components of a price such as interval and usage_type.

Only required if a default tax behavior was not provided in the Stripe Tax settings. Specifies whether the price is considered inclusive of taxes or exclusive of taxes. One of inclusive, exclusive, or unspecified. Once specified as either inclusive or exclusive, it cannot be changed.

One of one_time or recurring depending on whether the price is for a one-time purchase or a recurring (subscription) purchase.

The unit amount in cents to be charged, represented as a whole integer if possible. Only set if billing_scheme=per_unit.

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

**Examples:**

Example 1 (unknown):
```unknown
{  "id": "price_1MoBy5LkdIwHu7ixZhnattbh",  "object": "price",  "active": true,  "billing_scheme": "per_unit",  "created": 1679431181,  "currency": "usd",  "custom_unit_amount": null,  "livemode": false,  "lookup_key": null,  "metadata": {},  "nickname": null,  "product": "prod_NZKdYqrwEYx6iK",  "recurring": {    "interval": "month",    "interval_count": 1,    "trial_period_days": null,    "usage_type": "licensed"  },  "tax_behavior": "unspecified",  "tiers_mode": null,  "transform_quantity": null,  "type": "recurring",  "unit_amount": 1000,  "unit_amount_decimal": "1000"}
```

Example 2 (unknown):
```unknown
{  "id": "price_1MoBy5LkdIwHu7ixZhnattbh",  "object": "price",  "active": true,  "billing_scheme": "per_unit",  "created": 1679431181,  "currency": "usd",  "custom_unit_amount": null,  "livemode": false,  "lookup_key": null,  "metadata": {},  "nickname": null,  "product": "prod_NZKdYqrwEYx6iK",  "recurring": {    "interval": "month",    "interval_count": 1,    "trial_period_days": null,    "usage_type": "licensed"  },  "tax_behavior": "unspecified",  "tiers_mode": null,  "transform_quantity": null,  "type": "recurring",  "unit_amount": 1000,  "unit_amount_decimal": "1000"}
```

Example 3 (unknown):
```unknown
curl https://api.stripe.com/v1/prices \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d currency=usd \  -d unit_amount=1000 \  -d "recurring[interval]"=month \  -d "product_data[name]"="Gold Plan"
```

Example 4 (unknown):
```unknown
curl https://api.stripe.com/v1/prices \  -u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_YOUR_TEST_KEY_HERE:" \  -d currency=usd \  -d unit_amount=1000 \  -d "recurring[interval]"=month \  -d "product_data[name]"="Gold Plan"
```

---
