---
name: power-query-expert
description: Expert guidance for connecting Power Query (Power BI, Excel) to Frappe apps and reports. Use when building Power Query M code for Frappe data access, integrating Frappe reports with Power BI/Excel, implementing authentication for Power Query connections, handling heavy/long-running reports with report_long_polling API to avoid timeouts, applying column types and transformations, or troubleshooting Power Query caching and connection issues.
---

# Power Query Expert

Connect Microsoft Power Query (Power BI, Excel) to Frappe apps with M code for report data access.

## Quick Start

### Simple REST API Connection

For direct document access and small lists (< 1000 records):

```fsharp
let
    BaseUrl = "https://your-site.frappe.cloud",
    DocType = "Item",
    Fields = "[""item_code"", ""item_name"", ""standard_rate""]",
    
    ApiUrl = BaseUrl & "/api/resource/" & DocType & "?fields=" & Uri.EscapeDataString(Fields),
    Response = Json.Document(Web.Contents(ApiUrl)),
    Table = Table.FromRecords(Response[data])
in
    Table
```

**Use for:** Direct document reads, small queries, real-time data

See [references/rest-api-power-query-example.md](references/rest-api-power-query-example.md) for complete REST API examples with filters, sorting, and pagination.

### Simple Frappe Report Connection

For fast reports that won't timeout:

```fsharp
let
    BaseUrl = "https://your-site.frappe.cloud",
    ReportName = "Simple Report",
    ApiUrl = BaseUrl & "/api/method/frappe.desk.query_report.run?report_name=" & Uri.EscapeDataString(ReportName),
    Response = Json.Document(Web.Contents(ApiUrl)),
    Data = Response[message][result],
    Table = Table.FromRecords(Data)
in
    Table
```

**Use for:** Small, fast reports (< 1000 rows, < 30 seconds execution)

### Long-Running Reports with report_long_polling

For heavy reports, use the **report_long_polling API** to prevent timeouts. This API executes reports asynchronously in Frappe's background worker queue.

**Three-step workflow:**

1. **Start job** - Create Prepared Report job
2. **Poll status** - Wait for completion  
3. **Get result** - Retrieve data with column metadata

See [references/long-polling-api-reference.md](references/long-polling-api-reference.md) for API endpoint details.

## Power BI/Excel Integration

**1. Get Data → Blank Query**

**2. Advanced Editor** - Paste M code from [references/long-polling-power-query-example.md](references/long-polling-power-query-example.md)

**3. Configure:**
```fsharp
BaseUrl = "https://your-site.frappe.cloud"
ReportName = "Item Prices"
Filters = []  // Add filters as needed
```

**4. Close & Apply**

**5. Configure Authentication** when prompted:
- Excel/Power BI will prompt for credentials on first connection
- **Option 1 - Username/Password**: Enter your Frappe username and password
- **Option 2 - API Key/Token**: Enter API Key as username, API Secret as password
- Authentication is handled automatically via HTTP Basic Auth
- No need to add Authorization headers in M code

## Authentication

Excel and Power BI handle authentication automatically through their built-in authentication forms. You have two options:

### Option 1: Username/Password
- Use your Frappe account username and password
- Excel/Power BI uses HTTP Basic Authentication
- Header format: `Authorization: Basic base64(username:password)`

### Option 2: API Key/Token (Recommended for Production)
1. **Create API Keys in Frappe**: User → API Access → Generate Keys
2. **Copy API Key and Secret**
3. **In Excel/Power BI authentication prompt**:
   - Username: Enter your API Key
   - Password: Enter your API Secret
4. Excel/Power BI uses HTTP Basic Authentication
5. Header format: `Authorization: Basic base64(api_key:api_secret)`

**Note:** Excel/Power BI uses HTTP Basic Authentication, not Frappe's `token` format. Frappe's API accepts both formats, so authentication works seamlessly.

### Security Best Practices
- Use API keys instead of passwords for automated refreshes
- Grant minimal permissions to the API user
- Rotate keys regularly
- Never include credentials in M code

## Column Transformation

The report_long_polling API returns column metadata enabling automatic transformation:

```json
{"fieldname": "item_code", "label": "Item Code", "fieldtype": "Link"}
```

**Automatic type mapping:**
- Int/Long Int → Int64.Type
- Currency → Currency.Type  
- Date → Date.Type
- Datetime → DateTime.Type
- Check → Logical.Type
- Text types → type text

**Manual override:**
```fsharp
ManualTypeMap = [
    Rate = Currency.Type,          // Force currency
    #"Stock Qty" = Int64.Type      // Force integer
]
```

See [references/long-polling-api-reference.md](references/long-polling-api-reference.md) for full type mapping table.

## Cache-Busting

Power Query caches aggressively. Add timestamps to force fresh requests:

```fsharp
Timestamp = Text.From(Number.Round(
    Duration.TotalSeconds(DateTime.LocalNow() - #datetime(1970, 1, 1, 0, 0, 0)) * 1000
)),
UrlWithCacheBuster = BaseUrl & "&_ts=" & Timestamp
```

## Common Use Cases

- **Power BI Dashboards**: Live sales, inventory, financial reports
- **Excel Workbooks**: Monthly analysis with pivot tables
- **Scheduled Refresh**: Daily/hourly dataset updates
- **Cross-System Reporting**: Combine Frappe data with external sources

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md) for detailed solutions.

**Quick fixes:**

- **Timeout errors**: Increase maxAttempts, verify workers running
- **Connection errors**: Check BaseUrl, authentication, permissions
- **Empty results**: Verify filters, check Prepared Report status
- **Type errors**: Use manual type overrides, check for nulls
- **Stale data**: Add cache-busting timestamps, clear cache

## Resources

- **REST API Examples**: [references/rest-api-power-query-example.md](references/rest-api-power-query-example.md)
- **Long-Polling M Code**: [references/long-polling-power-query-example.md](references/long-polling-power-query-example.md)
- **API Details**: [references/long-polling-api-reference.md](references/long-polling-api-reference.md)
- **Troubleshooting**: [references/troubleshooting.md](references/troubleshooting.md)
