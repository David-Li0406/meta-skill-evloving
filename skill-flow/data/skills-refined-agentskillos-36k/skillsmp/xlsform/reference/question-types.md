# Question Types Reference

XLSForm supports 20+ question types covering text input, selection, location, media, calculations, and more. Each type has specific properties and platform support.

---

## Text Input Types

### text
Accepts any text input. No restrictions on length or format (unless constrained).

| Property | Value |
|----------|-------|
| Type | text |
| Data Stored | String |
| Mobile Input | Text keyboard |
| Constraints | Optional (via `constraint` column) |
| Default | (empty) |

**Example:**
```
| type | name | label |
| text | name | What is your name? |
```

**Validation:**
```
| type | name | label | constraint | constraint_message |
| text | email | Email | .regex(., '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$') | Invalid email |
| text | phone | Phone | .regex(., '^\+?1?[0-9]{10}$') | Invalid phone number |
```

**Appearance Options:** `multiline` (larger text box), `url` (validate as URL), `email` (validate as email)

---

### integer
Whole numbers only. No decimal places.

| Property | Value |
|----------|-------|
| Type | integer |
| Data Stored | Whole number |
| Mobile Input | Numeric keyboard |
| Range | -2,147,483,648 to 2,147,483,647 |
| Constraints | Optional |
| Default | (empty) |

**Example:**
```
| type | name | label | constraint |
| integer | age | Age in years | . >= 0 and . <= 150 |
| integer | count | Number of items | . >= 0 |
```

**Appearance Options:** `thousands-sep` (format as 1,000), `default` (plain)

---

### decimal
Floating-point numbers (decimals allowed).

| Property | Value |
|----------|-------|
| Type | decimal |
| Data Stored | Decimal number |
| Mobile Input | Numeric keyboard with decimal point |
| Precision | Device-dependent, typically 15+ significant digits |
| Constraints | Optional |
| Default | (empty) |

**Example:**
```
| type | name | label | constraint |
| decimal | weight | Weight in kg | . > 0 |
| decimal | temperature | Temperature | . >= -50 and . <= 50 |
```

**Appearance Options:** `thousands-sep`, `default`

---

## Selection Types

### select_one
Single choice from a list. Only one answer allowed.

| Property | Value |
|----------|-------|
| Type | select_one list_name |
| Data Stored | Selected choice name |
| Mobile Input | Radio buttons, dropdown, or dropdown select |
| Required | Via `required` column |
| Choices | Defined in `choices` worksheet |

**Example:**
```
| type | name | label |
| select_one gender | gender | What is your gender? |

| list_name | name | label |
| gender | m | Male |
| gender | f | Female |
| gender | o | Other |
```

**Appearances:** `horizontal` (side-by-side), `vertical` (default, stacked), `likert`, `label`, `list-nolabel`

**Filtered Choices (Cascading):**
```
| type | name | label | choice_filter |
| select_one country | country | Country | |
| select_one province | province | Province | province in ${country} |
```

---

### select_multiple
Multiple answers allowed. User selects multiple options.

| Property | Value |
|----------|-------|
| Type | select_multiple list_name |
| Data Stored | Space-separated selected names |
| Mobile Input | Checkboxes |
| Required | Via `required` column |
| Choices | Defined in `choices` worksheet |

**Example:**
```
| type | name | label |
| select_multiple languages | languages | Languages you speak? |

| list_name | name | label |
| languages | english | English |
| languages | french | French |
| languages | spanish | Spanish |
```

**Appearance:** `horizontal`, `vertical` (default), `compact`, `list-nolabel`

**Validation:**
```
| type | name | label | constraint |
| select_multiple | colors | Pick 2-4 colors | selected(., 'red') + selected(., 'blue') >= 2 |
```

---

### rank
Rank options in order of preference. Returns ranked list.

| Property | Value |
|----------|-------|
| Type | rank list_name |
| Data Stored | Ordered choice names |
| Mobile Input | Drag-and-drop ranking |
| Choices | Defined in `choices` worksheet |

**Example:**
```
| type | name | label |
| rank | service_priority | Rank these services by priority |

| list_name | name | label |
| service_priority | water | Water supply |
| service_priority | health | Healthcare |
| service_priority | education | Education |
```

**Data:** Returns `water health education` (or different order if reranked).

---

## Date and Time Types

### date
Captures a date (year, month, day). Format: YYYY-MM-DD.

| Property | Value |
|----------|-------|
| Type | date |
| Data Stored | Date as YYYY-MM-DD |
| Mobile Input | Date picker |
| Constraint | Use `today()`, date comparisons |
| Example | 2024-10-30 |

**Example:**
```
| type | name | label | constraint |
| date | visit_date | Date of visit | . <= today() |
| date | dob | Birth date | . <= today() |
```

**Constraint Examples:**
```
. >= '2024-01-01'              (on or after Jan 1, 2024)
. <= today()                    (not in future)
today() - . >= 365             (at least 1 year ago)
```

---

### time
Captures a time (hours, minutes, seconds). Format: HH:MM:SS.

| Property | Value |
|----------|-------|
| Type | time |
| Data Stored | Time as HH:MM:SS |
| Mobile Input | Time picker |
| Default | `now()` for current time |

**Example:**
```
| type | name | label |
| time | arrival_time | Arrival time | |
```

**Data:** Returns `14:30:00` (24-hour format).

---

### dateTime
Captures date and time together. Format: YYYY-MM-DDTHH:MM:SS.

| Property | Value |
|----------|-------|
| Type | dateTime |
| Data Stored | ISO 8601 format |
| Mobile Input | Date picker + time picker |
| Default | `now()` for current date/time |

**Example:**
```
| type | name | label | default |
| dateTime | start_time | Survey start | now() |
```

**Data:** Returns `2024-10-30T14:30:00`.

---

## Location Types

### geopoint
Single geographic point. Latitude, longitude, elevation, accuracy.

| Property | Value |
|----------|-------|
| Type | geopoint |
| Data Stored | `latitude longitude elevation accuracy` |
| Mobile Input | GPS picker or map |
| Requires | GPS hardware, location permission |
| Appearance | `maps` (use map), `default` (GPS only) |

**Example:**
```
| type | name | label | appearance |
| geopoint | site | Mark site location | maps |
```

**Data:** Returns `0.3476 31.2316 1500 5` (lat lon elevation accuracy in meters).

**Constraints:**
```
. >= -90 1 -180 1      (valid lat/lon range)
```

---

### geotrace
Path or line of geographic points. Multiple lat/long pairs.

| Property | Value |
|----------|-------|
| Type | geotrace |
| Data Stored | Multiple `latitude longitude` pairs |
| Mobile Input | GPS path recorder or map |
| Use Case | Boundary walks, path monitoring, routes |
| Appearance | `maps` (map-based), `default` (GPS recording) |

**Example:**
```
| type | name | label | appearance |
| geotrace | walked_boundary | Trace the area boundary | maps |
```

**Data:** Returns line as space-separated points:
```
0.3476 31.2316 0.3485 31.2325 0.3490 31.2330
```

---

### geoshape
Polygon (closed area). Multiple points forming enclosed shape.

| Property | Value |
|----------|-------|
| Type | geoshape |
| Data Stored | Multiple `latitude longitude` pairs (closed) |
| Mobile Input | GPS polygon recorder or map |
| Use Case | Plot boundaries, area mapping, land parcels |
| Appearance | `maps` (map-based), `default` (GPS recording) |

**Example:**
```
| type | name | label | appearance |
| geoshape | plot | Mark plot boundaries | maps |
```

**Data:** Automatically closes polygon; last point returns to first.

---

## Media Types

### image
Capture or upload a photo/image.

| Property | Value |
|----------|-------|
| Type | image |
| Data Stored | Filename reference |
| Mobile Input | Camera or gallery |
| File Types | JPEG, PNG |
| Resolution | Device-dependent |
| Appearance | `annotate` (draw on image), `default` |

**Example:**
```
| type | name | label | appearance |
| image | damage_photo | Photo of damage | |
| image | annotated | Mark damage on photo | annotate |
```

**Appearance Options:**
- `new` (capture new photo only, no gallery)
- `new-front` (front-facing camera)
- `new-rear` (rear camera)
- `annotate` (draw on image after capture)

---

### audio
Record or upload audio clip.

| Property | Value |
|----------|-------|
| Type | audio |
| Data Stored | Filename reference |
| Mobile Input | Audio recorder |
| File Format | Device-dependent (MP3, AMR) |
| Use Case | Voice notes, interviews, audio surveys |

**Example:**
```
| type | name | label |
| audio | field_notes | Record field notes |
```

---

### video
Record or upload video clip.

| Property | Value |
|----------|-------|
| Type | video |
| Data Stored | Filename reference |
| Mobile Input | Video recorder |
| File Format | Device-dependent (MP4, MOV) |
| Resolution | Device-dependent |

**Example:**
```
| type | name | label |
| video | damage_video | Record damage video |
```

**Appearance:** `selfie` (front-facing camera), `default` (rear), `new` (recording only)

---

### file
Upload any file type.

| Property | Value |
|----------|-------|
| Type | file |
| Data Stored | Filename reference |
| Mobile Input | File picker |
| File Types | Any (device-dependent) |
| Use Case | Documents, receipts, certificates |

**Example:**
```
| type | name | label |
| file | receipt | Upload receipt |
```

---

### barcode
Scan a barcode or QR code.

| Property | Value |
|----------|-------|
| Type | barcode |
| Data Stored | Scanned barcode string |
| Mobile Input | Camera barcode scanner |
| Barcode Types | QR, EAN-13, UPC-A, Aztec, etc. |
| Constraint | Optional validation |

**Example:**
```
| type | name | label |
| barcode | product_code | Scan product barcode |
```

**Constraint:**
```
| type | name | label | constraint |
| barcode | qr_code | QR code | regex(., '^[A-Z0-9]{10,}$') |
```

---

## Calculated and Special Types

### calculate
Hidden calculated field. Not displayed to user, only computed.

| Property | Value |
|----------|-------|
| Type | calculate |
| Data Stored | Calculated value |
| Display | Hidden (not shown to user) |
| Use Case | Timestamps, audit fields, internal tracking |

**Example:**
```
| type | name | label | calculation |
| calculate | timestamp | | now() |
| calculate | submission_id | | uuid() |
| calculate | total | | ${amount1} + ${amount2} |
```

**Common Calculations:**
- `now()` - Current date/time
- `today()` - Current date
- `uuid()` - Unique ID
- Math: `${field1} + ${field2}`, `${field1} * 100 / ${field2}`
- Conditionals: `if(${condition}, 'true_value', 'false_value')`

---

### note
Display static text or information. No data collection.

| Property | Value |
|----------|-------|
| Type | note |
| Data Stored | None |
| Display | Static text message |
| Use Case | Instructions, dividers, thank you messages |
| Label | Displayed as message |

**Example:**
```
| type | name | label |
| note | instructions | Please answer all questions honestly |
| note | divider | --- Section 2: Demographics --- |
| note | thank_you | Thank you for completing the survey |
```

**Dynamic Notes:**
```
| type | name | label | relevant |
| note | age_note | You are ${age} years old | |
```

---

### acknowledge
Checkbox requiring user acknowledgment. Must be checked to proceed.

| Property | Value |
|----------|-------|
| Type | acknowledge |
| Data Stored | "yes" if checked |
| Display | Checkbox with label |
| Required | Usually yes (can't skip) |
| Use Case | Consent, agreement, confirmation |

**Example:**
```
| type | name | label | required |
| acknowledge | consent | I have read and agree to terms | yes |
| acknowledge | data_privacy | I understand my data will be encrypted | yes |
```

---

### hidden
Hidden field. Not displayed, not in prompts, used internally.

| Property | Value |
|----------|-------|
| Type | hidden |
| Data Stored | Value if provided |
| Display | Not shown |
| Use Case | Pre-filled values, system fields |
| Default | Can set via `default` column |

**Example:**
```
| type | name | label | default |
| hidden | form_version | | 2.0 |
| hidden | enumerator_id | | ${auth_username} |
```

---

## Advanced Selection Types

### select_one_from_file
Select from choices in external CSV file (avoids large choice lists in worksheet).

| Property | Value |
|----------|-------|
| Type | select_one_from_file list_name |
| Choices | Loaded from CSV file |
| File Format | CSV with name, label columns |
| Use Case | Large lists (hospitals, schools, products) |

**Example:**
```
| type | name | label |
| select_one_from_file hospitals | hospital | Nearest hospital |
```

**hospitals.csv:**
```
name,label
h001,Nairobi General Hospital
h002,Kenyatta National Hospital
h003,Kampala Hospital
```

File location: same directory as .xlsx, or online URL.

---

### select_multiple_from_file
Multiple selections from external CSV file.

| Property | Value |
|----------|-------|
| Type | select_multiple_from_file list_name |
| Choices | Loaded from CSV file |
| File Format | CSV with name, label columns |

**Example:**
```
| type | name | label |
| select_multiple_from_file services | available_services | What services available? |
```

---

## Group and Repeat Types

### begin repeat / end repeat
Repeating section. User can add multiple identical rows.

| Property | Value |
|----------|-------|
| Type | begin repeat ... end repeat |
| Display | Repeating group of fields |
| Use Case | Multiple household members, multiple purchases, multiple visits |
| Data | Multiple rows per submission |

**Example:**
```
| type | name | label |
| begin repeat | children | Children in household |
| text | child_name | Child name |
| integer | child_age | Child age |
| end repeat | | |
```

**Dynamic Repeat Limits:**
```
| type | name | label | repeat_count |
| begin repeat | purchases | Purchases | ${num_items} |
```

---

### begin group / end group
Grouped fields (visual organization, not repeating).

| Property | Value |
|----------|-------|
| Type | begin group ... end group |
| Display | Collapsible or nested field group |
| Use Case | Section organization, appearance customization |
| Data | No effect on data storage |

**Example:**
```
| type | name | label | appearance |
| begin group | demographics | Demographics | field-list |
| text | name | Name |
| integer | age | Age |
| end group | | |
```

---

## Summary Table

| Type | Input | Mobile | Use Case |
|------|-------|--------|----------|
| **text** | Keyboard | Text input | Names, descriptions |
| **integer** | Numeric | Number input | Counts, ages |
| **decimal** | Decimal | Float input | Measurements, weights |
| **select_one** | List | Radio/dropdown | Single choice |
| **select_multiple** | List | Checkboxes | Multiple choices |
| **rank** | List | Drag-drop | Ranking |
| **date** | Date picker | Calendar | Dates |
| **time** | Time picker | Clock | Times |
| **dateTime** | DateTime picker | Calendar + clock | Timestamps |
| **geopoint** | GPS | Map or GPS | Single location |
| **geotrace** | GPS path | Path recorder | Lines/boundaries |
| **geoshape** | GPS polygon | Polygon tool | Areas/plots |
| **image** | Camera | Photo capture | Photos/evidence |
| **audio** | Mic | Audio recorder | Voice notes |
| **video** | Camera | Video recorder | Video evidence |
| **file** | File picker | File picker | Documents |
| **barcode** | Scanner | Camera scanner | Barcodes/QR |
| **calculate** | Formula | Hidden | Computed values |
| **note** | N/A | Static text | Information |
| **acknowledge** | Checkbox | Checkbox | Consent |
| **hidden** | N/A | Hidden | Internal fields |

---

## Platform Support

Not all question types are supported on all platforms:

| Type | ODK Collect | KoBoToolbox | SurveyCTO | Enketo |
|------|---|---|---|---|
| Basic (text, integer, select) | ✓ | ✓ | ✓ | ✓ |
| Geolocation (geopoint, geotrace) | ✓ | ✓ | ✓ | (limited) |
| Media (image, audio, video) | ✓ | ✓ | ✓ | (image only) |
| Rank | ✓ | ✓ | ✓ | ✓ |
| Barcode | ✓ | ✓ | ✓ | (limited) |
| Calculate | ✓ | ✓ | ✓ | ✓ |
| Repeat | ✓ | ✓ | ✓ | ✓ |

Check platform documentation for latest support.
