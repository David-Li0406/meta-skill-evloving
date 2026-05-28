---
name: invoicing
description: Interact with the Eenvoudig Factureren API to manage clients, invoices, quotes, orders, and more. Use me when dealing with invoicing, clients, quotes, orders, deliveries, receipts, payments, stock items, or subscriptions.
---

# Eenvoudig Factureren API Integration

This skill provides instructions for interacting with the Eenvoudig Factureren invoicing platform API.

## Base URL

```
https://eenvoudigfactureren.be/api/v1
```

## Authentication

The API supports two authentication methods:

### API Key (Recommended)

Pass the API key via the `X-API-Key` header:

```
X-API-Key: your-api-key
```

**Environment Variable:** The API key should be stored in `EENVOUDIG_FACTUREREN_API_KEY`. Always use this environment variable rather than hardcoding the key.

Example usage:

```bash
curl -H "X-API-Key: $EENVOUDIG_FACTUREREN_API_KEY" https://eenvoudigfactureren.be/api/v1/clients
```

### Basic Authentication

Use email and password with standard Basic Authentication via the `Authorization` header.
If the user has access to multiple accounts, specify the account via the `X-AccountId` header.

## Response Formats

Add `?format=` parameter to specify response format:

- `json` - JSON format
- `xml` - XML format (default)
- `csv` - CSV format (Excel compatible)
- `html` - HTML table
- `pdf` - PDF document (invoices, receipts, quotes, orders, deliveries only)
- `efff`, `ublbe`, `peppol`, `peppolbis3` - Electronic invoice formats (invoices only)

## HTTP Methods

- `GET` - Retrieve data
- `POST` - Create or partially update data (unmentioned fields remain unchanged)
- `PUT` - Replace data completely (unmentioned fields are deleted)
- `DELETE` - Delete data

## Result Codes

- `200` - Success
- `201` - Created
- `400` - Bad request (invalid data)
- `401` - Authentication failed
- `403` - Access denied
- `404` - Not found
- `500` - Internal error

## Available Domains

### Clients (`/clients`)

Manage customer data including contacts and custom fields.

**Endpoints:**

- `GET /clients` - List all clients
- `GET /clients/{id}` - Get specific client
- `POST /clients` - Create client
- `POST /clients?bulk` - Bulk create/update clients (max 100)
- `PUT /clients/{id}` - Update client
- `DELETE /clients/{id}` - Delete client

**Key fields:**

- `client_id` - Unique ID (auto-generated)
- `name` - Client name (required, max 75 chars)
- `number` - Client number
- `email_address` - Email address
- `tax_code` - VAT number
- `street`, `city`, `postal_code`, `country_code` - Address fields
- `contacts` - List of contact persons
- `delivery_address`, `site_address` - Additional addresses
- `state` - 'active' or 'archived'

### Invoices (`/invoices`)

Manage invoices and credit notes. Credit notes have negative totals.

**Endpoints:**

- `GET /invoices` - List all invoices
- `GET /invoices/{id}` - Get specific invoice
- `POST /invoices` - Create invoice
- `PUT /invoices/{id}` - Update invoice
- `DELETE /invoices/{id}` - Delete invoice

**Subdomains:**

- `/invoices/{id}/items` - Invoice line items
- `/invoices/{id}/payments` - Payments received
- `/invoices/{id}/remarks` - Internal remarks
- `/invoices/{id}/costs` - Reminder costs
- `/invoices/{id}/events` - Events/history

**Key fields:**

- `invoice_id` - Unique ID (auto-generated)
- `client_id` - Client ID (required)
- `number` - Invoice number (auto-generated if not provided)
- `date` - Invoice date (YYYY-MM-DD)
- `days_due` - Payment term in days
- `status` - 'open', 'overdue', 'closed' (auto-determined)
- `type` - 'invoice' or 'creditnote' (auto-determined)
- `items` - List of invoice items
- `total_with_tax` - Total including VAT (calculated)
- `structured_message` - Belgian payment reference (12 digits)
- `note` - Note shown on invoice

**Invoice items:**

- `description` - Item description (required)
- `amount` - Unit price excl. VAT
- `amount_with_tax` - Unit price incl. VAT
- `quantity` - Number of units (default: 1)
- `tax_rate` - VAT percentage
- `stockitem_id` - Link to stock item (auto-adjusts inventory)

### Quotes (`/quotes`)

Manage quotations/offers.

**Endpoints:** Same structure as invoices

- `GET /quotes`, `GET /quotes/{id}`, `POST /quotes`, etc.

### Orders (`/orders`)

Manage order confirmations.

**Endpoints:** Same structure as invoices

### Deliveries (`/deliveries`)

Manage delivery notes.

**Endpoints:** Same structure as invoices

### Receipts (`/receipts`)

Manage cash register receipts.

**Endpoints:** Same structure as invoices

### Subscriptions (`/subscriptions`)

Manage recurring invoices.

### Stock Items (`/stockitems`)

Manage product/service catalog.

**Endpoints:**

- `GET /stockitems` - List all items
- `POST /stockitems?bulk` - Bulk create/update (max 100)

### Layouts (`/layouts`)

Manage document templates.

### Activities (`/activities`)

View activity log/events.

## Common Query Parameters

### Filtering

```
?filter=field%3Dvalue,field2%3D%7Etext
```

Operators (URL-encoded):

- `=` (%3D) - equals
- `!=` (%21%3D) - not equals
- `<` (%3C), `>` (%3E), `<=` (%3C%3D), `>=` (%3E%3D) - comparisons
- `=~` (%3D%7E) - contains

### Searching

```
?search=searchterm
```

### Sorting

```
?sort=field1%2B-field2
```

Prefix with `-` for descending order. Separate multiple fields with `+` (%2B).

### Pagination

```
?skip=30&take=10
```

Recommended: max 100 documents per request.

### Field Selection

```
?fields=name,email_address
```

## Sending Documents

### Send via Email

```
POST /invoices/{id}?send_mail
```

Body parameters:

- `recipient` - Email address, contact_id, or: 'myself', 'main_contact', 'first_contact', 'all_contacts'
- `recipients` - List of recipients
- `subject` - Email subject (optional)
- `message` - Email body (optional)
- `document_type` - 'pdf', 'ubl', 'both', 'duplicate', 'reminder', 'reminder_summary'
- `attachments` - List of attachments (upload_id, filename)

### Send via PEPPOL

```
POST /invoices/{id}?send_peppol
```

### Send via Postal Mail (BPost)

```
POST /invoices/{id}?send_postalmail
```

Body parameters:

- `address_type` - 'billing', 'delivery', 'site'
- `send_registered` - 0 (non-prior) or 1 (registered)

### Send to Accountant

```
POST /invoices/{id}?send_accountant
```

## File Uploads (Attachments)

```
POST /uploads
```

Upload files as form-data with key 'file' (max 5MB). Returns `upload_id` to use with email attachments.

## Example: Create Invoice with Items

```json
{
  "client_id": 101,
  "number": "INV2024-001",
  "days_due": 30,
  "items": [
    {
      "description": "Product A",
      "amount": 100.00,
      "quantity": 2,
      "tax_rate": 21
    },
    {
      "description": "Shipping",
      "amount": 10.00,
      "tax_rate": 21
    }
  ]
}
```

## Example: Register Payment

```json
POST /invoices/{id}/payments
{
  "date": "2024-01-15",
  "amount": 250.00,
  "method": "transfer",
  "description": "Bank transfer"
}
```

Payment methods: `transfer`, `cash`, `debitcard`, `creditcard`, `directcollection`, `online`, `bancontact`, `ideal`

## Important Notes

1. Always use HTTPS
2. Rate limiting applies - avoid too many consecutive requests
3. Use bulk endpoints for importing large datasets
4. Invoice numbers must be unique
5. Dates use format YYYY-MM-DD
6. Currency defaults to EUR
7. Language options: 'dutch', 'french', 'english', 'german'
