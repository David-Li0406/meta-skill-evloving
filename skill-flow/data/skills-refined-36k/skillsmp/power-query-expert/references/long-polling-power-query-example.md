# Power Query M Code Example

This example demonstrates how to integrate the report_long_polling API with Microsoft Power Query for Power BI or Excel.

## Complete Power Query M Code

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
    BaseUrl = "http://127.0.0.1:8000",
    ReportName = "Item Prices",
    
    // Add your filters here (optional)
    // To use parameters: [price_list = GetParam("PriceList"), from_date = GetParam("StartDate")]
    Filters = [],
    
    // Helper function to build query string
    BuildQueryString = (params as record) =>
        Text.Combine(
            List.Transform(
                Record.FieldNames(params),
                each _ & "=" & Uri.EscapeDataString(Text.From(Record.Field(params, _)))
            ),
            "&"
        ),
    
    // Step 1: Start the report job
    StartJobParams = Record.Combine({[report_name = ReportName], Filters}),
    StartJobUrl = BaseUrl & "/api/method/tweaks.utils.report_long_polling.start_job?" & BuildQueryString(StartJobParams),
    StartJobResponse = Json.Document(Web.Contents(StartJobUrl)),
    JobId = StartJobResponse[message],
    
    // Step 2: Base URL for polling
    CheckStatusUrl = BaseUrl & "/api/method/tweaks.utils.report_long_polling.check_status?job_id=" & Uri.EscapeDataString(JobId),
    
    // Recursive polling function
    PollUntilComplete = (baseUrl as text, maxAttempts as number) as logical =>
        let
            Poll = (attemptNumber as number) as logical =>
                if attemptNumber > maxAttempts then
                    error "Report generation timed out after " & Text.From(maxAttempts) & " attempts"
                else
                    let
                        PollTimestamp = Text.From(Number.Round(Duration.TotalSeconds(DateTime.LocalNow() - #datetime(1970, 1, 1, 0, 0, 0)) * 1000)),
                        UrlWithCacheBuster = baseUrl & "&attempts=2&sleep=5&_attempt=" & Text.From(attemptNumber) & "&_ts=" & PollTimestamp,
                        StatusResponse = Json.Document(Web.Contents(UrlWithCacheBuster)),
                        Status = StatusResponse[message],
                        IsComplete = Status = 1
                    in
                        if IsComplete then
                            true
                        else
                            @Poll(attemptNumber + 1)
        in
            Poll(1),
    
    // Wait for completion (max 100 attempts)
    IsComplete = PollUntilComplete(CheckStatusUrl, 100),
    
    // Step 3: Get the report result (only after polling confirms completion)
    ResultTimestamp = Text.From(Number.Round(Duration.TotalSeconds(DateTime.LocalNow() - #datetime(1970, 1, 1, 0, 0, 0)) * 1000)),
    GetResultUrl = BaseUrl & "/api/method/tweaks.utils.report_long_polling.get_result?job_id=" & Uri.EscapeDataString(JobId) & "&_ts=" & ResultTimestamp,
    // Force evaluation by using IsComplete in a conditional
    ResultResponse = if IsComplete then Json.Document(Web.Contents(GetResultUrl)) else error "Report generation failed",
    ResultData = ResultResponse[message],
    
    // Step 4: Convert columns metadata to a usable format
    Columns = ResultData[columns],
    ColumnNames = List.Transform(Columns, each [fieldname]),
    ColumnLabels = List.Transform(Columns, each if Record.HasFields(_, "label") then [label] else [fieldname]),
    
    // Step 5: Extract result rows and convert to table
    ResultRows = ResultData[result],
    Table = Table.FromRecords(ResultRows),
    
    // Step 6: Get actual columns in the table
    ActualColumns = Table.ColumnNames(Table),
    
    // Step 7: Build rename list only for columns that exist in the table
    RenameList = List.Select(
        List.Zip({ColumnNames, ColumnLabels}),
        each List.Contains(ActualColumns, _{0})
    ),
    
    // Step 8: Rename columns with proper labels
    RenamedTable = Table.RenameColumns(Table, RenameList),
    
    // Step 9: Apply column types if available
    TypedTable = 
        let
            // Manual column type overrides (use column labels, not fieldnames)
            // Example: ManualTypeMap = [Price = Currency.Type, Quantity = Int64.Type]
            ManualTypeMap = [],
            
            // Comprehensive Frappe field type to Power Query type mapping
            TypeMapping = [
                // Numeric types
                Int = Int64.Type,
                #"Long Int" = Int64.Type,
                Float = Number.Type,
                Currency = Currency.Type,
                Percent = Percentage.Type,
                
                // Date/Time types
                Date = Date.Type,
                Datetime = DateTime.Type,
                Time = Time.Type,
                Duration = Duration.Type,
                
                // Boolean type
                Check = Logical.Type,
                
                // Text types (all map to text)
                Data = type text,
                Text = type text,
                #"Small Text" = type text,
                #"Long Text" = type text,
                #"Text Editor" = type text,
                #"HTML Editor" = type text,
                #"Markdown Editor" = type text,
                Code = type text,
                Password = type text,
                #"Read Only" = type text,
                
                // Link types
                Link = type text,
                #"Dynamic Link" = type text,
                Select = type text,
                
                // Attachment types
                Attach = type text,
                #"Attach Image" = type text,
                Signature = type text,
                
                // Special types
                Barcode = type text,
                Phone = type text,
                Geolocation = type text,
                JSON = type text,
                Autocomplete = type text,
                Icon = type text,
                Color = type text,
                Rating = Number.Type,
                Image = type text,
                Button = type text,
                HTML = type text
            ],
            
            // Build type list only for columns that exist in the table
            FinalColumnNames = Table.ColumnNames(RenamedTable),
            ColumnTypes = List.Select(
                List.Transform(
                    Columns,
                    each 
                        let
                            fieldname = [fieldname],
                            fieldtype = if Record.HasFields(_, "fieldtype") then [fieldtype] else "Data",
                            label = if Record.HasFields(_, "label") then [label] else fieldname,
                            // Use manual override if specified, otherwise use auto-mapping
                            powerQueryType = if Record.HasFields(ManualTypeMap, label) then 
                                Record.Field(ManualTypeMap, label) 
                            else 
                                Record.FieldOrDefault(TypeMapping, fieldtype, type text),
                            // Use label as the column name after renaming
                            finalName = if List.Contains(ActualColumns, fieldname) then label else fieldname
                        in
                            {finalName, powerQueryType}
                ),
                each List.Contains(FinalColumnNames, _{0})
            ),
            
            // Apply types to the table
            TypedTable = Table.TransformColumnTypes(RenamedTable, ColumnTypes)
        in
            TypedTable,
    
    // Step 10: Reorder columns to match the order in the columns list
    ReorderedTable = 
        let
            // Get labels for columns that exist in the table
            FinalColumnNames = Table.ColumnNames(TypedTable),
            OrderedLabels = List.Select(ColumnLabels, each List.Contains(FinalColumnNames, _))
        in
            Table.ReorderColumns(TypedTable, OrderedLabels)
in
    ReorderedTable
```

## Key Implementation Details

### 1. Configuration

```fsharp
BaseUrl = "http://127.0.0.1:8000",
ReportName = "Item Prices",
Filters = []
```

Replace with your Frappe instance URL and report name. Add filters as needed:

```fsharp
Filters = [price_list = "Standard Selling", item_group = "Products"]
```

**Using parameters from a table:**

If you uncommented the parameter loading section at the top, you can reference values from your Parameters table:

```fsharp
Filters = [
    price_list = GetParam("PriceList"), 
    from_date = GetParam("StartDate"),
    to_date = GetParam("EndDate"),
    item_group = GetParam("ItemGroup")
]
```

To make parameters optional (skip filter if empty):

```fsharp
// Get parameter values
PriceList = GetParam("PriceList"),
StartDate = GetParam("StartDate"),
EndDate = GetParam("EndDate"),

// Build filters conditionally
Filters = Record.FromList(
    List.RemoveNulls({
        if PriceList <> null and PriceList <> "" then {"price_list", PriceList} else null,
        if StartDate <> null then {"from_date", StartDate} else null,
        if EndDate <> null then {"to_date", EndDate} else null
    }),
    List.RemoveNulls({
        if PriceList <> null and PriceList <> "" then "price_list" else null,
        if StartDate <> null then "from_date" else null,
        if EndDate <> null then "to_date" else null
    })
),
```

### 2. Manual Type Overrides

Override automatic type detection for specific columns:

```fsharp
ManualTypeMap = [
    Price = Currency.Type,
    Quantity = Int64.Type,
    #"Item Code" = type text,
    #"Modified Date" = Date.Type
]
```

**Important:** Use column labels (after renaming), not fieldnames. Manual types take precedence over automatic type mapping.

### 3. Cache Busting

Power Query aggressively caches API responses. Use timestamps to force fresh requests:

```fsharp
PollTimestamp = Text.From(Number.Round(Duration.TotalSeconds(DateTime.LocalNow() - #datetime(1970, 1, 1, 0, 0, 0)) * 1000)),
UrlWithCacheBuster = baseUrl & "&_attempt=" & Text.From(attemptNumber) & "&_ts=" & PollTimestamp
```

### 4. Recursive Polling

The `PollUntilComplete` function recursively calls `check_status` until the job completes:

```fsharp
PollUntilComplete = (baseUrl as text, maxAttempts as number) as logical =>
    let
        Poll = (attemptNumber as number) as logical =>
            if attemptNumber > maxAttempts then
                error "Report generation timed out"
            else
                let
                    StatusResponse = Json.Document(Web.Contents(UrlWithCacheBuster)),
                    Status = StatusResponse[message],
                    IsComplete = Status = 1
                in
                    if IsComplete then true else @Poll(attemptNumber + 1)
    in
        Poll(1)
```

### 5. Column Metadata Processing

Frappe returns column metadata with each result. Use it to:

- **Rename columns**: Map `fieldname` to `label`
- **Apply types**: Map `fieldtype` to Power Query types (or use manual overrides)
- **Reorder columns**: Match report definition order

### 6. Type Mapping

The code includes comprehensive Frappe-to-Power Query type mapping:

| Frappe Type | Power Query Type |
|-------------|------------------|
| Int, Long Int | Int64.Type |
| Float | Number.Type |
| Currency | Currency.Type |
| Date | Date.Type |
| Datetime | DateTime.Type |
| Check | Logical.Type |
| Data, Text, Link | type text |

**Manual overrides** take precedence over automatic mapping. Use the `ManualTypeMap` record at the top of Step 9:

```fsharp
ManualTypeMap = [
    #"Stock Qty" = Int64.Type,  // Force integer instead of float
    Rate = Currency.Type,       // Force currency formatting
    Description = type text     // Keep as text even if detected differently
]
```

## Usage in Power BI/Excel

### Power BI

1. Get Data → Blank Query
2. Open Advanced Editor
3. Paste the M code
4. Update `BaseUrl` and `ReportName`
5. When prompted, configure authentication:
   - **Username**: API Key or Frappe username
   - **Password**: API Secret or Frappe password
6. Close & Apply

### Excel

1. Data → Get Data → From Other Sources → Blank Query
2. Open Advanced Editor
3. Paste the M code
4. Update `BaseUrl` and `ReportName`
5. When prompted, configure authentication:
   - **Username**: API Key or Frappe username
   - **Password**: API Secret or Frappe password
6. Load to worksheet

## Authentication

Excel and Power BI handle authentication automatically through their built-in forms. When you first connect, they will prompt for credentials:

**Option 1 - Username/Password:**
- Enter your Frappe username and password
- Excel/Power BI uses HTTP Basic Authentication
- Header format: `Authorization: Basic base64(username:password)`

**Option 2 - API Key/Token (Recommended):**
- Create API keys in Frappe: User → API Access → Generate Keys
- In the Excel/Power BI authentication prompt:
  - **Username**: Enter your API Key
  - **Password**: Enter your API Secret
- Excel/Power BI uses HTTP Basic Authentication
- Header format: `Authorization: Basic base64(api_key:api_secret)`

**Note:** Excel/Power BI uses HTTP Basic Authentication (not Frappe's `token` format). Frappe's API accepts both formats, so authentication works seamlessly.

**No need to include authorization headers in M code** - Excel and Power BI add them automatically based on the credentials you provide.

## Troubleshooting

**"Report generation timed out":**
- Increase `maxAttempts` in `PollUntilComplete(CheckStatusUrl, 100)`
- Check that background workers are running in Frappe

**Empty table returned:**
- Verify report permissions for the API user
- Check report filters are valid
- Review Prepared Report status in Frappe

**Type conversion errors:**
- Check column metadata matches actual data
- Add missing field types to `TypeMapping`
- Use `type text` as fallback for unknown types

**Caching issues:**
- Ensure cache-busting timestamps are included
- Clear Power Query cache (Data → Refresh → Clear)
- Use unique `_attempt` parameter for each poll
