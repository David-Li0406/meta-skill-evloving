# Report Long Polling API Reference

Complete API documentation for the `tweaks.utils.report_long_polling` module.

## API Endpoints

### 1. Start Job

**Endpoint:** `/api/method/tweaks.utils.report_long_polling.start_job`

**Purpose:** Create a new Prepared Report job

**Parameters:**
- `report_name` (required): Name of the Frappe report to execute
- `**kwargs`: Report filters (optional, varies by report)

**Returns:** Job ID (Prepared Report name)

**Example:**
```
GET /api/method/tweaks.utils.report_long_polling.start_job?report_name=Item%20Prices
```

**Response:**
```json
{
    "message": "prep-report-job-id-12345"
}
```

### 2. Check Status

**Endpoint:** `/api/method/tweaks.utils.report_long_polling.check_status`

**Purpose:** Poll job status with built-in retry logic

**Parameters:**
- `job_id` (required): Job ID from start_job
- `attempts` (optional): Max polling attempts (default: 2)
- `sleep` (optional): Seconds between attempts (default: 5)

**Returns:** 1 if completed/error, 0 if still running

**Example:**
```
GET /api/method/tweaks.utils.report_long_polling.check_status?job_id=prep-report-job-id-12345&attempts=2&sleep=5
```

**Response:**
```json
{
    "message": 1
}
```

**Behavior:**
- Polls up to `attempts` times with `sleep` seconds between attempts
- Returns 1 if status is "Completed" or "Error"
- Returns 1 if job not found (DoesNotExistError)
- Returns 0 if still running after all attempts

### 3. Get Result

**Endpoint:** `/api/method/tweaks.utils.report_long_polling.get_result`

**Purpose:** Retrieve completed report data

**Parameters:**
- `job_id` (required): Job ID from start_job

**Returns:** Report result with columns metadata and data rows

**Example:**
```
GET /api/method/tweaks.utils.report_long_polling.get_result?job_id=prep-report-job-id-12345
```

**Response:**
```json
{
    "message": {
        "columns": [
            {"fieldname": "item_code", "label": "Item Code", "fieldtype": "Link"},
            {"fieldname": "item_name", "label": "Item Name", "fieldtype": "Data"},
            {"fieldname": "price_list_rate", "label": "Rate", "fieldtype": "Currency"}
        ],
        "result": [
            {"item_code": "ITEM-001", "item_name": "Product A", "price_list_rate": 100.00},
            {"item_code": "ITEM-002", "item_name": "Product B", "price_list_rate": 250.00}
        ]
    }
}
```

**Error Cases:**
- Status "Error": Returns empty columns/result with error message
- Job not found: Returns empty columns/result with "not found" message
- Still processing: Returns empty columns/result with "still generating" message

## Column Metadata

The `columns` array provides metadata for each column:

```json
{
    "fieldname": "item_code",      // Database field name
    "label": "Item Code",           // User-friendly label
    "fieldtype": "Link"             // Frappe field type
}
```

**Usage:**
- Rename columns using labels
- Apply data types based on fieldtype
- Reorder columns to match report definition

## Type Mapping Reference

Frappe field types to Power Query types:

| Frappe Type | Power Query Type | Notes |
|-------------|------------------|-------|
| Int, Long Int | Int64.Type | Whole numbers |
| Float | Number.Type | Decimals |
| Currency | Currency.Type | Formatted currency |
| Percent | Percentage.Type | Percentage formatting |
| Date | Date.Type | Date only |
| Datetime | DateTime.Type | Date + time |
| Time | Time.Type | Time only |
| Duration | Duration.Type | Time duration |
| Check | Logical.Type | Boolean (true/false) |
| Data, Text, Small Text, Long Text | type text | Text strings |
| Text Editor, HTML Editor, Markdown Editor | type text | Rich text content |
| Code | type text | Code content |
| Link, Dynamic Link | type text | Document links |
| Select | type text | Dropdown values |
| Attach, Attach Image, Signature | type text | File paths |
| Barcode, Phone, Geolocation, JSON | type text | Special formats |
| Rating | Number.Type | Numeric rating |

## Implementation Details

**Location:** `tweaks/utils/report_long_polling.py`

**Dependencies:**
- `frappe.core.doctype.prepared_report.prepared_report.make_prepared_report`
- `frappe.desk.query_report.get_prepared_report_result`

**Requirements:**
- Background workers must be running (`bench worker`)
- User must have report access permissions
- Report must be a valid Query Report or Script Report

## Polling Configuration

Configure polling behavior based on report characteristics:

| Report Size | Max Attempts | Sleep (seconds) | Notes |
|-------------|--------------|-----------------|-------|
| Small (< 1000 rows) | 10 | 2 | Usually completes in 1-2 attempts |
| Medium (1000-10000) | 50 | 5 | May take 30-60 seconds |
| Large (> 10000) | 100 | 5 | Can take several minutes |
| Complex queries | 150 | 10 | Depends on database performance |
