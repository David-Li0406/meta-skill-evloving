# External Datasets

Use external CSV files, Entity Lists, and GeoJSON for dynamic data.

## CSV Files

### Select from CSV

Reference CSV files in select questions:

| type | name | label |
|------|------|-------|
| select_one_from_file locations.csv | location | Select Location |
| select_multiple_from_file services.csv | services | Select Services |

### CSV Requirements

- Must have `name` column (value saved)
- Must have `label` column (displayed text)
- Additional columns for filtering/lookup

### Example CSV (locations.csv)

```csv
name,label,region,district
loc1,Nairobi Central,central,nairobi
loc2,Mombasa Port,coast,mombasa
loc3,Kisumu Town,western,kisumu
```

---

## Direct CSV Attachment

Attach CSV for lookups without select questions:

| type | name |
|------|------|
| csv-external | products |

---

## Lookup from External Data

### Syntax

```
instance("dataset_name")/root/item[filter]/property
```

### Examples

**Get property after selection:**
```
instance("locations")/root/item[name = ${location}]/region
```

**Lookup by any field:**
```
instance("products")/root/item[barcode = ${scanned_code}]/product_name
```

**With calculation:**

| type | name | calculation |
|------|------|-------------|
| select_one_from_file people.csv | person | |
| calculate | person_phone | instance("people")/root/item[name = ${person}]/phone |
| calculate | person_email | instance("people")/root/item[name = ${person}]/email |

---

## Aggregate Functions on External Data

### Count Matching Items

```
count(instance("inventory")/root/item[category = 'electronics'])
```

### Sum Values

```
sum(instance("orders")/root/item[status = 'pending']/amount)
```

---

## Choice Filters (Cascading Selects)

Filter choices based on previous answers.

### Choices Sheet

| list_name | name | label | region |
|-----------|------|-------|--------|
| district | d1 | District A | north |
| district | d2 | District B | north |
| district | d3 | District C | south |
| district | d4 | District D | south |

### Survey Sheet

| type | name | label | choice_filter |
|------|------|-------|---------------|
| select_one region | region | Region | |
| select_one district | district | District | region = ${region} |

### Multi-Level Cascade

| type | name | label | choice_filter |
|------|------|-------|---------------|
| select_one country | country | Country | |
| select_one region | region | Region | country = ${country} |
| select_one district | district | District | region = ${region} |
| select_one facility | facility | Facility | district = ${district} |

### Filter with Multiple Conditions

```
region = ${region} and type = 'hospital'
```

---

## GeoJSON Files

Use `.geojson` files for geographic selections.

### Requirements

- File must have `.geojson` extension
- Single FeatureCollection
- Unique identifiers for features
- Supports Point, LineString, Polygon

### Example

| type | name | label | appearance |
|------|------|-------|------------|
| select_one_from_file areas.geojson | area | Select Area | map |

### Accessing GeoJSON Properties

```
instance("areas")/root/item[name = ${area}]/properties/population
```

---

## Entity Lists

Managed datasets in ODK Central.

### Benefits

- Data shared across forms in project
- Updated automatically from submissions
- No need to re-upload CSV files

### Usage

Same as CSV files:

| type | name | label |
|------|------|-------|
| select_one_from_file patients.csv | patient | Select Patient |

See [09-entities.md](09-entities.md) for creating and managing entities.

---

## pulldata() Function

Alternative lookup method:

```
pulldata('filename', 'column_to_get', 'lookup_column', lookup_value)
```

### Example

| type | name | label | calculation |
|------|------|-------|-------------|
| barcode | product_barcode | Scan Product | |
| calculate | product_name | | pulldata('products', 'name', 'barcode', ${product_barcode}) |
| calculate | product_price | | pulldata('products', 'price', 'barcode', ${product_barcode}) |

---

## Best Practices

### File Naming

- Use lowercase with underscores
- Keep names short but descriptive
- Example: `health_facilities.csv`

### File Size

- Keep files reasonably sized
- Consider device memory limitations
- Large files slow down form loading

### Data Updates

- Version your CSV files
- Document data sources
- Test after updates

### Performance

- Use choice_filter to reduce displayed options
- Index frequently-filtered columns
- Consider splitting large datasets
