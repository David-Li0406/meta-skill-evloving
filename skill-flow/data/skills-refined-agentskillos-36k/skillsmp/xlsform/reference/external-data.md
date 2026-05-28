# External Data Reference

Load choice lists from external CSV files instead of the choices worksheet. Use this for very large choice lists (1000+) to keep your Excel file small and fast.

## When to Use External Data

| Scenario | Use External File |
|----------|---|
| 1-100 choices | Use choices sheet |
| 100-500 choices | Either method works |
| 500-1000 choices | Either method works |
| 1000+ choices | Use external file ✓ |
| Data changes frequently | Use external file ✓ |
| Data from database | Use external file ✓ |
| Very large hospitals/schools list | Use external file ✓ |

---

## Single-Select from File

Use `select_one_from_file` question type.

### Survey
```
| type | name | label |
| select_one_from_file hospitals | hospital | Nearest hospital |
```

### External File: hospitals.csv
```
name,label
h001,Nairobi General Hospital
h002,Kenyatta National Hospital
h003,Mombasa Hospital
h004,Kisumu Hospital
(... thousands more)
```

### File Requirements

**CSV Format:**
- First column: `name` (choice identifier, stored in data)
- Second column: `label` (displayed to user)
- Plain text encoding (UTF-8)

**File Naming:**
- Match the list name from survey
- Survey has `select_one_from_file hospitals`
- File must be named `hospitals.csv`

**File Location:**
- Same directory as .xlsx form file
- Or online URL (if platform supports)

---

## Multiple-Select from File

Use `select_multiple_from_file` question type.

```
| type | name | label |
| select_multiple_from_file services | services | Available services |
```

File format same as single-select.

---

## File Format Details

### Basic Format
```
name,label
h001,Hospital A
h002,Hospital B
h003,Hospital C
```

### With Extra Columns (for filtering)
```
name,label,region,district
h001,Hospital A,central,nairobi
h002,Hospital B,coast,mombasa
h003,Hospital C,coast,kilifi
h004,Hospital D,rift,nakuru
```

Extra columns can be used for cascading/filtering:
```
| type | name | label | choice_filter |
| select_one_from_file hospitals | hospital | Hospital | hospital in ${district} |
```

### Special Characters and Unicode
```
name,label
h001,Hôpital Central
h002,مستشفى الصحة
h003,Больница №1
```

---

## Building External Data Files

### Step 1: Identify Data Source
- Database export
- Google Sheet
- Manual list
- API endpoint

### Step 2: Create CSV File

**From Database:**
```sql
SELECT hospital_id as name, hospital_name as label FROM hospitals
```

**From Google Sheet:**
1. Create sheet with name, label columns
2. Download as CSV

**From Manual List:**
1. Open Excel/Sheets
2. Create columns: name, label
3. Save as CSV

### Step 3: Name File Correctly
- Survey: `select_one_from_file hospitals`
- File: `hospitals.csv` (exact match)

### Step 4: Package Form
```
form.xlsx
hospitals.csv
schools.csv (if another file-based list)
```

### Step 5: Deploy
- Upload .xlsx and .csv together to platform
- Platform loads lists from CSV files

---

## Cascading with External Data

Use `choice_filter` with extra CSV columns:

**Survey:**
```
| type | name | label | choice_filter |
| select_one district | district | District | |
| select_one_from_file hospitals | hospital | Hospital | hospital in ${district} |
```

**hospitals.csv:**
```
name,label,district
h001,Nairobi General,nairobi
h002,Kenyatta,nairobi
h003,Mombasa Hospital,mombasa
h004,Coastal Hospital,mombasa
h005,Nakuru Hospital,nakuru
```

**Flow:**
1. User selects district (from choices worksheet)
2. Hospital list loads from hospitals.csv
3. Only hospitals matching selected district show

---

## Multilingual External Data

Include language columns in CSV:

```
name,label,label_fr,label_sw
h001,Nairobi General,Hôpital Nairobi,Hospitali la Nairobi
h002,Mombasa Hospital,Hôpital Mombasa,Hospitali la Mombasa
h003,Kisumu Hospital,Hôpital Kisumu,Hospitali la Kisumu
```

Platform displays appropriate language based on device language.

---

## Example: Large Hospital List

**File size:** hospitals.csv (1000+ hospitals)

**hospitals.csv:**
```
name,label,region,district
facility_001,Nairobi General Hospital,central,nairobi
facility_002,Kenyatta National Hospital,central,nairobi
facility_003,City Hospital,central,nairobi
facility_004,Nairobi West Health Center,central,nairobi
facility_005,Mombasa General Hospital,coast,mombasa
facility_006,Mombasa Teaching Hospital,coast,mombasa
facility_007,Coastal Regional Hospital,coast,mombasa
facility_008,Malindi District Hospital,coast,malindi
facility_009,Kisumu County Hospital,western,kisumu
facility_010,Kisumu Teaching Hospital,western,kisumu
(... 990+ more)
```

**Form (form.xlsx):**
```
Survey:
| type | name | label | choice_filter |
| select_one region | region | Region | |
| select_one district | district | District | district in ${region} |
| select_one_from_file hospitals | hospital | Health facility | hospital in ${district} |

Choices (for region/district):
(Regional and district lists in worksheet, keep smaller)
```

**File package:**
```
form.xlsx (small, no huge choice lists)
hospitals.csv (large list, loaded from file)
```

---

## Platform Support

| Platform | File Support |
|----------|---|
| ODK Collect | ✓ (CSV files) |
| KoBoToolbox | ✓ (CSV files) |
| SurveyCTO | ✓ (Custom format) |
| Enketo | ✓ (CSV files) |
| ODK Central | ✓ (CSV files) |

Check platform documentation for specific requirements.

---

## Best Practices

### Do's
✓ Name CSV file exactly as list_name
✓ Include name and label columns
✓ Use UTF-8 encoding
✓ Put files in same directory as .xlsx
✓ Test before deployment
✓ Version control your CSV files

### Don'ts
✗ Don't use spaces in filename
✗ Don't use Excel format (.xlsx) for large lists
✗ Don't include extra columns unless filtering
✗ Don't have duplicate names in a list
✗ Don't forget to include both files when deploying

---

## Troubleshooting

### List Not Showing

1. **File name mismatch**
   - Survey: `select_one_from_file hospitals`
   - File: `hospitals.csv` ✓ or `Hospital.csv` ✗
   - Must match exactly (case-sensitive)

2. **File location**
   - File must be in same directory as .xlsx
   - Or on online server if platform supports

3. **File format**
   - Must be valid CSV (comma-separated)
   - First row: name,label
   - Check for extra spaces or quotes

4. **Upload**
   - If uploading to platform, upload both files
   - Don't upload only .xlsx

### Cascading Not Working with External Files

1. **Check extra column exists** in CSV
   ```
   hospital in ${district}
   (hospitals.csv must have 'district' column)
   ```

2. **Check values match** between files
   ```
   Choices: | list_name | name | label |
            | district | nbi | Nairobi |

   CSV: name,label,district
        h001,Hospital,nbi ✓
   ```

3. **Check syntax** in choice_filter
   ```
   ✓ hospital in ${district}
   ✗ hospital = ${district} (wrong operator)
   ```

---

## Performance

- **Small lists** (< 500): Choices worksheet fine
- **Medium lists** (500-2000): Either method acceptable
- **Large lists** (2000+): External files recommended
- **Very large lists** (10000+): External files essential

External files load faster on mobile devices and keep Excel file small.

---

## Data Sync and Updates

### Keeping Data Current

If external file changes:
1. Update CSV file
2. Re-deploy to platform
3. Forms launched after update use new data
4. Previously downloaded forms use old data (offline)

### Database Integration

For dynamic data from database:
1. Create automated process to export database → CSV
2. Upload CSV to server/platform
3. Forms reference remote CSV file
4. Data stays current automatically

---

## Example Workflow

### Step 1: Export Data
```python
# Export hospitals from database to CSV
import pandas as pd
df = pd.read_sql("SELECT hospital_id as name, hospital_name as label FROM hospitals")
df.to_csv('hospitals.csv', index=False)
```

### Step 2: Create Form
```
Survey:
| type | name | label |
| select_one_from_file hospitals | hospital | Select hospital |
```

### Step 3: Package
```
form.xlsx
hospitals.csv
```

### Step 4: Deploy
- Upload both files to platform
- Forms automatically use external list

---

## See Also

- [choices-sheet.md](choices-sheet.md) - Choices worksheet reference
- [cascading-selects.md](cascading-selects.md) - Cascading with external data
- [examples.md](../examples.md) - Example form with external data
