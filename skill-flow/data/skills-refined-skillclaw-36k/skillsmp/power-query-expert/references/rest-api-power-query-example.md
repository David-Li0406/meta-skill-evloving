# REST API Power Query Example

Power Query M code template for fetching all records from Frappe using the Report View API with automatic pagination.

## Overview

This template provides a complete solution for fetching all records from any Frappe DocType with:
- **Automatic pagination** - Fetches all records across multiple pages
- **Filters** - Filter records server-side
- **Sorting** - Order results by any field
- **Custom fields** - Select specific fields to return
- **Child table fields** - Access child table data directly in results
- **Link expansion** - Optionally expand linked documents

**Use this for datasets < 10,000 records.** For larger datasets or complex queries, use the [long-polling API](long-polling-power-query-example.md) instead.

**Note:** This uses `frappe.desk.reportview.get` which returns a compressed format (`keys` and `values`). The M code automatically expands this into a proper table.

## Authentication

Authentication is handled automatically by Excel and Power BI through their built-in authentication forms:

- **Username/Password**: Use your Frappe account credentials
- **API Key/Token**: Enter API Key as username, API Secret as password

Excel/Power BI automatically adds the `Authorization` header using **HTTP Basic Authentication** format: `Authorization: Basic base64(username:password)`. Frappe's API accepts this format alongside its native token format.

**Do not include authentication headers in your M code** - they are added automatically by Excel/Power BI.

### Create API Keys in Frappe

1. Go to User → API Access
2. Click "Generate Keys"
3. Copy API Key and Secret
4. When Excel/Power BI prompts for credentials, enter:
   - **Username**: Your API Key
   - **Password**: Your API Secret
5. Complete Template: Fetch

## Fetching All Records with Pagination

```fsharp
let
    // ========== LOAD PARAMETERS FROM TABLE (OPTIONAL) ==========
    // To use this: Create a table named "Parameters" in Excel with columns:
    // Parameter | Value
    // Then uncomment this section and use GetParam() in your filters
    
    // ParametersTable = Excel.CurrentWorkbook(){[Name="Parameters"]}[Content],
    // GetParam = (paramName as text) => 
    //     let Row = Table.SelectRows(ParametersTable, each [Parameter] = paramName)
    //     in if Table.RowCount(Row) > 0 then Row{0}[Value] else null,
    
    // ========== CONFIGURATION ==========
    BaseUrl = "https://your-site.frappe.cloud",
    DocType = "Quotation",
    
    // OPTIONAL: Set if you want to include child table fields
    // Leave as "" to only query parent fields
    ChildDocType = "Quotation Item",
    
    // Fields: {DocType or ChildDocType, FieldName}
    FieldList = {
        {DocType, "name"},
        {DocType, "party_name"},
        {DocType, "transaction_date"},
        {DocType, "grand_total"},
        {DocType, "status"},
        {DocType, "valid_till"},
        // Child table fields (optional - only if ChildDocType is set)
        {ChildDocType, "item_code"},
        {ChildDocType, "qty"},
        {ChildDocType, "rate"},
        {ChildDocType, "amount"}
    },
    
    // Filters: {DocType, Field, Operator, Value}
    // Use DocType for parent, ChildDocType for child fields
    // Leave empty {} for no filters
    // All conditions in FilterList are combined with AND
    // To use parameters: GetParam("StartDate"), GetParam("CardName"), etc.
    FilterList = {
        {DocType, "transaction_date", ">=", "2026-01-15"},
        {DocType, "docstatus", "=", "1"}
        // Filter by child field:
        // {ChildDocType, "item_code", "=", "ITEM-001"}
        // Using parameters (uncomment GetParam section above first):
        // {DocType, "transaction_date", ">=", GetParam("StartDate")},
        // {DocType, "party_name", "=", GetParam("CardName")},
        // {DocType, "grand_total", ">=", Number.From(GetParam("MinAmount"))}
    },
    
    // All conditions in OrFilterList are combined with OR
    // Leave empty {} if not needed
    OrFilterList = {
        // Example: Get quotes from multiple customers
        // {DocType, "customer", "=", "Customer A"},
        // {DocType, "customer", "=", "Customer B"}
    },
    
    // Sort: List of {DocType or ChildDocType, FieldName, "asc" or "desc"}
    // Leave as {} for no sorting
    OrderByList = {
        {DocType, "transaction_date", "desc"}
        // Add more sort fields if needed:
        // {DocType, "name", "asc"}
    },
    
    PageSize = 100,
    
    // OPTIONAL: Set a maximum number of records to fetch
    // Set to 0 to fetch all records (no limit)
    // Set to a number (e.g., 1000) to stop after fetching that many records
    RecordLimit = 0,
    // ====================================
    
    // Format OrderBy clauses
    OrderByClause = if List.Count(OrderByList) > 0 then
        Text.Combine(
            List.Transform(
                OrderByList,
                each "`tab" & _{0} & "`.`" & _{1} & "` " & _{2}
            ),
            ", "
        )
        else "",
    
    // Helper function to format field with backticks and alias
    FormatField = (fieldDef as list) as text =>
        let
            doctype = fieldDef{0},
            fieldname = fieldDef{1},
            
            // Format: `tabDocType`.`fieldname`
            fullField = "`tab" & doctype & "`.`" & fieldname & "`",
            
            // Add alias for child tables
            withAlias = if doctype <> DocType then
                fullField & " as '" & doctype & ":" & fieldname & "'"
                else fullField
        in
            withAlias,
    
    // Convert fields to JSON array
    Fields = "[" & Text.Combine(
        List.Transform(FieldList, each """" & FormatField(_) & """"),
        ", "
    ) & "]",
    
    // Convert filters to JSON array
    Filters = if List.Count(FilterList) > 0 then
        "[" & Text.Combine(
            List.Transform(FilterList, 
                each "[""" & _{0} & """, """ & _{1} & """, """ & _{2} & """, """ & Text.From(_{3}) & """]"
            ),
            ", "
        ) & "]"
        else "[]",
    
    // Convert OR filters to JSON array
    OrFilters = if List.Count(OrFilterList) > 0 then
        "[" & Text.Combine(
            List.Transform(OrFilterList, 
                each "[""" & _{0} & """, """ & _{1} & """, """ & _{2} & """, """ & Text.From(_{3}) & """]"
            ),
            ", "
        ) & "]"
        else "[]",
    
    // Function to fetch a single page using reportview.get
    FetchPage = (StartIndex as number) =>
        let
            // Build API URL for frappe.desk.reportview.get
            ApiUrl = BaseUrl & "/api/method/frappe.desk.reportview.get"
                & "?doctype=" & Uri.EscapeDataString(DocType)
                & "&fields=" & Uri.EscapeDataString(Fields)
                & "&filters=" & Uri.EscapeDataString(Filters)
                & "&or_filters=" & Uri.EscapeDataString(OrFilters)
                & "&start=" & Number.ToText(StartIndex)
                & "&page_length=" & Number.ToText(PageSize)
                & "&view=Report"
                & (if OrderByClause <> "" then "&order_by=" & Uri.EscapeDataString(OrderByClause) else ""),
            
            Response = Json.Document(Web.Contents(ApiUrl)),
            
            // Handle compressed response format
            Message = Response[message],
            Keys = Message[keys],
            Values = Message[values],
            
            // Convert compressed format to records
            Records = List.Transform(
                Values,
                each Record.FromList(_, Keys)
            )
        in
            Records,
    
    // Fetch all pages recursively
    FetchAllPages = (StartIndex as number, RemainingLimit as number) as list =>
        let
            // Determine how many records to fetch this page
            ActualPageSize = if RemainingLimit > 0 and RemainingLimit < PageSize 
                then RemainingLimit 
                else PageSize,
            
            CurrentPage = FetchPage(StartIndex),
            CurrentPageCount = List.Count(CurrentPage),
            
            // Trim current page if we've exceeded the limit
            TrimmedPage = if RemainingLimit > 0 and CurrentPageCount > RemainingLimit
                then List.FirstN(CurrentPage, RemainingLimit)
                else CurrentPage,
            
            TrimmedPageCount = List.Count(TrimmedPage),
            
            // Calculate new remaining limit
            NewRemainingLimit = if RemainingLimit > 0 
                then RemainingLimit - TrimmedPageCount 
                else 0,
            
            // Determine if we should continue fetching
            ShouldContinue = 
                CurrentPageCount = PageSize and  // We got a full page
                (RemainingLimit = 0 or NewRemainingLimit > 0),  // And we haven't hit the limit
            
            NextPages = if ShouldContinue
                then @FetchAllPages(StartIndex + PageSize, NewRemainingLimit) 
                else {}
        in
            List.Combine({TrimmedPage, NextPages}),
    
    AllData = FetchAllPages(0, RecordLimit),
    Table = Table.FromRecords(AllData)
in
    Table
```

**How it works:**
- Uses `frappe.desk.reportview.get` which supports child table fields
- Properly formats fields with backticks: `` `tabDocType`.`fieldname` ``
- Adds aliases for child table fields to match Frappe's format
- Automatically decompresses the response format (`keys` + `values` → records)
- Fetches all records across multiple pages
- Stops when fewer records than `PageSize` are returned or when `RecordLimit` is reached

## Populating Filter Values from a Workbook Table

For a more user-friendly approach, you can create a "Parameters" sheet where end users can modify filter values without touching Power Query code. The filter structure remains in the query, but values come from the table.

### Creating a Parameters Sheet

1. **Create a table in Excel** with parameter names and values:

| Parameter | Value |
|-----------|-------|
| StartDate | 2026-01-01 |
| EndDate | 2026-12-31 |
| CardName | Customer ABC |
| MinAmount | 1000 |

2. **Convert to a table**: Select the data → Insert → Table (or Ctrl+T)

3. **Name the table**: Right-click the table → Table Design → Table Name: "Parameters"

### Using Parameters in Filter Values

Add this code at the beginning of your query to load parameters:

```fsharp
let
    // ========== LOAD PARAMETERS FROM TABLE ==========
    ParametersTable = Excel.CurrentWorkbook(){[Name="Parameters"]}[Content],
    
    // Helper function to get parameter value
    GetParam = (paramName as text) as any =>
        let
            Row = Table.SelectRows(ParametersTable, each [Parameter] = paramName),
            Value = if Table.RowCount(Row) > 0 then Row{0}[Value] else null
        in
            Value,
    
    // ========== CONFIGURATION ==========
    BaseUrl = "https://your-site.frappe.cloud",
    DocType = "Quotation",
    ChildDocType = "Quotation Item",
    
    FieldList = {
        {DocType, "name"},
        {DocType, "party_name"},
        {DocType, "transaction_date"},
        {DocType, "grand_total"},
        {ChildDocType, "item_code"},
        {ChildDocType, "qty"}
    },
    
    // Use GetParam() to reference parameter values in filters
    FilterList = {
        {DocType, "transaction_date", ">=", GetParam("StartDate")},
        {DocType, "transaction_date", "<=", GetParam("EndDate")},
        {DocType, "party_name", "=", GetParam("CardName")},
        {DocType, "grand_total", ">=", GetParam("MinAmount")}
    },
    
    OrFilterList = {},
    
    OrderByList = {
        {DocType, "transaction_date", "desc"}
    },
    
    PageSize = 100,
    RecordLimit = 0,
    // ====================================
    
    // ... rest of the query code remains the same ...
```

### Handling Optional Parameters

To make parameters optional (skip filter if empty):

```fsharp
let
    // Load parameters
    ParametersTable = Excel.CurrentWorkbook(){[Name="Parameters"]}[Content],
    
    GetParam = (paramName as text) as any =>
        let
            Row = Table.SelectRows(ParametersTable, each [Parameter] = paramName),
            Value = if Table.RowCount(Row) > 0 then Row{0}[Value] else null
        in
            Value,
    
    // Get parameter values
    StartDate = GetParam("StartDate"),
    EndDate = GetParam("EndDate"),
    CardName = GetParam("CardName"),
    MinAmount = GetParam("MinAmount"),
    
    // Build filter list conditionally
    FilterList = List.RemoveNulls({
        if StartDate <> null then {DocType, "transaction_date", ">=", StartDate} else null,
        if EndDate <> null then {DocType, "transaction_date", "<=", EndDate} else null,
        if CardName <> null and CardName <> "" then {DocType, "party_name", "=", CardName} else null,
        if MinAmount <> null then {DocType, "grand_total", ">=", MinAmount} else null
    }),
    
    // ... rest of configuration ...
```

**How it works:**
- Each parameter is checked before adding to the filter list
- If parameter is null or empty, that filter is skipped
- `List.RemoveNulls()` cleans up the list
- Users can leave parameters blank to disable specific filters

### Type Conversion for Parameters

Always convert parameter values to the correct type:

```fsharp
// Numbers
MinAmount = try Number.From(GetParam("MinAmount")) otherwise 0,

// Dates (if stored as text in parameters table)
StartDate = try Date.From(GetParam("StartDate")) otherwise #date(2026, 1, 1),

// Text - use directly
CardName = GetParam("CardName"),

// With defaults if missing
MaxAmount = try Number.From(GetParam("MaxAmount")) otherwise 999999,
```

### Example: Complete Integration

Here's a practical example with date range, customer, and amount filters:

**Parameters Table:**

| Parameter | Value |
|-----------|-------|
| StartDate | 2026-01-01 |
| EndDate | 2026-01-31 |
| CustomerName | ACME Corp |
| MinAmount | 5000 |
| Status | Open |

**Power Query Code:**

```fsharp
let
    // Load parameters
    ParametersTable = Excel.CurrentWorkbook(){[Name="Parameters"]}[Content],
    GetParam = (paramName as text) => 
        let Row = Table.SelectRows(ParametersTable, each [Parameter] = paramName)
        in if Table.RowCount(Row) > 0 then Row{0}[Value] else null,
    
    // Configuration
    BaseUrl = "https://your-site.frappe.cloud",
    DocType = "Quotation",
    
    // Build filters using parameters
    FilterList = {
        {DocType, "transaction_date", ">=", GetParam("StartDate")},
        {DocType, "transaction_date", "<=", GetParam("EndDate")},
        {DocType, "party_name", "=", GetParam("CustomerName")},
        {DocType, "grand_total", ">=", Number.From(GetParam("MinAmount"))},
        {DocType, "status", "=", GetParam("Status")}
    },
    
    // ... rest of template code ...
```

### Best Practices

1. **Simple values only**: Use parameters for filter values (dates, names, amounts), not for entire filter structures

2. **Clear parameter names**: Use descriptive names like `StartDate`, `MinAmount`, `CustomerName` so users understand what to enter

3. **Add a Help sheet**: Document what each parameter does and what format to use (especially for dates)

4. **Type conversion**: Convert numbers and dates from text using `Number.From()` or `Date.From()`

5. **Optional parameters**: Use conditional logic to skip filters when parameters are empty

## How to Use This Template

### 1. Set Your DocType and Fields

Edit the configuration section at the top:

```fsharp
DocType = "Quotation",  // Change to your DocType

// OPTIONAL: Set only if you want child table fields
ChildDocType = "Quotation Item",  // Or "" to skip child table

// Fields: {DocType or ChildDocType, FieldName}
FieldList = {
    {DocType, "name"},
    {DocType, "party_name"},
    {DocType, "transaction_date"},
    {DocType, "grand_total"},
    // Child table fields (optional)
    {ChildDocType, "item_code"},
    {ChildDocType, "qty"},
    {ChildDocType, "rate"}
},
```

**Note:** When including child table fields, you'll get one row per child record. For example, a Quotation with 3 items will return 3 rows with the parent data duplicated.

### 2. Set Record Limit (Optional)

Control how many records to fetch:

```fsharp
// Fetch all records (no limit) - default
RecordLimit = 0,

// Fetch only first 1000 records
RecordLimit = 1000,

// Fetch only first 500 records
RecordLimit = 500,
```

**When to use `RecordLimit`:**
- **Testing:** Quickly preview data without fetching everything
- **Performance:** Limit data for faster initial loads
- **Data sampling:** Get a representative sample for analysis
- **Development:** Work with smaller datasets during report development

**Important notes:**
- The limit is applied **after** filtering and sorting
- Records are fetched in pages until the limit is reached
- If you set `RecordLimit = 500` with `PageSize = 100`, it will fetch 5 pages and stop
- The actual number of records may be slightly less if the last page is incomplete
- Use `0` to fetch all available records (default behavior)

### 3. Add Filters (Optional)

Use `{DocType, field, operator, value}` format. Use `DocType` for parent fields or `ChildDocType` for child fields:

```fsharp
// AND Filters - all conditions must be true
FilterList = {
    {DocType, "transaction_date", ">=", "2024-01-01"},
    {DocType, "status", "=", "Open"},
    // Filter by child table field
    {ChildDocType, "item_code", "=", "ITEM-001"}
},

// OR Filters - at least one condition must be true
OrFilterList = {
    {DocType, "customer", "=", "Customer A"},
    {DocType, "customer", "=", "Customer B"}
},

// Or leave both empty for no filters:
FilterList = {},
OrFilterList = {},
```

**Filter Format:** `{DocType or ChildDocType, FieldName, Operator, Value}`

**Available operators:** `=`, `!=`, `>`, `<`, `>=`, `<=`, `like`, `in`, `not in`

**Combining AND and OR:**
- All conditions in `FilterList` are combined with AND
- All conditions in `OrFilterList` are combined with OR
- If both are used, the query becomes: `(FilterList conditions) AND (OrFilterList conditions)`

**Example:** Get open quotations from 2024 for either Customer A or Customer B:
```fsharp
FilterList = {
    {DocType, "transaction_date", ">=", "2024-01-01"},
    {DocType, "status", "=", "Open"}
},
OrFilterList = {
    {DocType, "customer", "=", "Customer A"},
    {DocType, "customer", "=", "Customer B"}
},
// Result: date >= 2024 AND status = Open AND (customer = A OR customer = B)
```

### 4. Set Sorting (Optional)

Use a list of `{DocType or ChildDocType, FieldName, "asc" or "desc"}` tuples. You can specify multiple sort fields:

```fsharp
OrderByList = {
    {DocType, "transaction_date", "desc"},     // Primary sort
    {DocType, "name", "asc"}                    // Secondary sort
},
// or single sort:
OrderByList = {
    {ChildDocType, "qty", "asc"}
},
// or no sorting:
OrderByList = {},
```

**Sort Format:** `{DocType or ChildDocType, FieldName, Direction}`

**Direction:** `"asc"` (ascending) or `"desc"` (descending)

**Multiple sorts:** Add multiple tuples to sort by multiple fields. First tuple is primary sort, second is secondary, etc.

## Accessing Child Table Fields

To include child table fields, set `ChildDocType` and add field names to `ChildFields`.

### Example: Sales Order with Items

```fsharp
DocType = "Sales Order",
ChildDocType = "Sales Order Item",

FieldList = {
    {DocType, "name"},
    {DocType, "customer"},
    {DocType, "transaction_date"},
    {DocType, "grand_total"},
    {ChildDocType, "item_code"},
    {ChildDocType, "qty"},
    {ChildDocType, "rate"},
    {ChildDocType, "amount"}
},
```

**Important:** When you include child table fields:
- You get **one row per child record**
- A Sales Order with 3 items returns **3 rows**
- Parent fields are duplicated across rows
- This is a LEFT JOIN, so orders with no items return 1 row with null child values

### Filtering by Child Table Fields

Use `ChildDocType` in your filters:

```fsharp
FilterList = {
    {DocType, "transaction_date", ">=", "2024-01-01"},
    {ChildDocType, "item_code", "=", "ITEM-001"}  // Filter by child field
},
```

### Querying Only Parent Fields

To query without child tables, just set `ChildDocType = ""` and only use `DocType` in your field list:

```fsharp
DocType = "Sales Order",
ChildDocType = "",  // No child table

FieldList = {
    {DocType, "name"},
    {DocType, "customer"},
    {DocType, "transaction_date"},
    {DocType, "grand_total"}
    // No ChildDocType fields
},
```

## Expanding Link Fields

To fetch data from linked documents, you need to use the Link doctype and its fields.

### Example: Expand Customer Link

```fsharp
FieldList = {
    {"Quotation", "name", null},
    {"Quotation", "party_name", null},
    {"Quotation", "customer", null},           // Link field itself
    {"Customer", "customer_name", "Customer Name"},  // Expanded field
    {"Customer", "customer_group", "Customer Group"},
    {"Customer", "territory", "Territory"},
    {"Quotation", "transaction_date", null},
    {"Quotation", "grand_total", null}
},
```

**Note:** The link field (e.g., `customer`) must exist in the parent DocType's schema for the expansion to work.

### Combining Child Tables and Link Expansion

You can use both child table fields and link expansion together:

```fsharp
FieldList = {
    // Parent fields
    {"Quotation", "name", null},
    {"Quotation", "customer", null},
    
    // Expand parent link
    {"Customer", "customer_name", "Customer Name"},
    {"Customer", "territory", "Territory"},
    
    // Child table fields
    {"Quotation Item", "item_code", "Item Code"},
    {"Quotation Item", "qty", "Qty"},
    {"Quotation Item", "rate", "Rate"},
    
    // Expand link in child table
    {"Item", "item_name", "Item Name"},
    {"Item", "item_group", "Item Group"}
},
```

**Note:** Each expanded field and child table join adds to response size and query time. Only include what you need.

## Performance Tips

1. **Limit Fields**: Only request fields you need - this significantly reduces data transfer and improves speed

2. **Use Filters**: Filter on the server, not in Power Query - this reduces the number of records fetched

3. **Adjust PageSize**: 
   - Smaller pages (50-100): Better for slower connections
   - Larger pages (200-500): Faster for good connections, but may timeout on slow queries

4. **Avoid Over-Expansion**: Expanding many link fields increases query complexity - only expand what you need

5. **For Large Datasets**: If you have > 10,000 records, consider using the [long-polling API](long-polling-power-query-example.md) instead

## Troubleshooting

**Query times out:**
- Reduce `PageSize` to 50 or lower
- Add more specific filters to reduce total records
- Consider using long-polling API for heavy queries

**Missing data:**
- Verify field names match exactly (case-sensitive)
- Check filter syntax: `{field, operator, value}`
- Ensure you have permission to access the DocType

**Child table fields not showing:**
- Make sure `ChildDocType` is set correctly
- Use `{ChildDocType, "field_name"}` format in `FieldList`
- Remember: Including child fields returns one row per child record
- Verify the child table field exists and is accessible

**Link fields not expanding:**
- Specify the linked DocType: `{"Customer", "customer_name", "Customer Name"}`
- The link field itself must exist in the main DocType
- Check that linked document has the field you're requesting

**Getting error "Invalid field name":**
- Check for typos in field names (case-sensitive)
- Ensure you're using the correct DocType name
- Verify you have read permission on the fields you're requesting

**Sort not working:**
- Use format: `{DocType, "fieldname", "asc"}` or `{DocType, "fieldname", "desc"}`
- Example: `OrderByList = {{DocType, "transaction_date", "desc"}}`
- Make sure direction is `"asc"` or `"desc"` (lowercase, in quotes)
- For multiple sorts, add more tuples: `{{DocType, "date", "desc"}, {DocType, "name", "asc"}}`
