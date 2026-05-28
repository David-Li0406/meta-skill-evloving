# Question Types

Complete reference for all ODK question types.

## Text Input Types

| Type | Description | Appearances |
|------|-------------|-------------|
| `text` | Free text input | `multiline`, `numbers`, `masked` |
| `integer` | Whole numbers (max 9 digits) | `thousands-sep`, `counter` |
| `decimal` | Decimal numbers (max 15 chars) | `thousands-sep` |

### Examples

| type | name | label | appearance |
|------|------|-------|------------|
| text | patient_name | Patient Name | |
| text | notes | Additional Notes | multiline |
| text | phone | Phone Number | numbers |
| integer | age | Age (years) | |
| decimal | weight | Weight (kg) | |

---

## Selection Types

| Type | Description |
|------|-------------|
| `select_one [list_name]` | Single choice (radio buttons) |
| `select_multiple [list_name]` | Multiple choices (checkboxes) |
| `select_one_from_file [file.csv]` | Single choice from external file |
| `select_multiple_from_file [file.csv]` | Multiple from external file |
| `rank [list_name]` | Order items by dragging |

### Select Appearances

| Appearance | Description |
|------------|-------------|
| `minimal` | Dropdown/spinner |
| `quick` | Auto-advance after selection (select_one only) |
| `autocomplete` | Searchable dropdown |
| `columns` | Multi-column layout |
| `columns-n` | Specific columns (e.g., `columns-3`) |
| `no-buttons` | Image-only display |
| `likert` | Likert scale styling |
| `map` | Map-based selection |
| `horizontal` | Side-by-side choices |
| `horizontal-compact` | Compact side-by-side |

### Examples

| type | name | label | appearance |
|------|------|-------|------------|
| select_one gender | sex | Gender | minimal |
| select_multiple symptoms | symptoms | Select symptoms | |
| select_one yes_no | consent | Do you consent? | quick |
| select_one rating | satisfaction | Rating | likert |

---

## Date and Time Types

| Type | Description | Appearances |
|------|-------------|-------------|
| `date` | Calendar date picker | `no-calendar`, `month-year`, `year` |
| `time` | Time of day | |
| `dateTime` | Combined date and time | |

### Non-Gregorian Calendars

Supported: Bikram Sambat, Buddhist, Coptic, Ethiopian, Islamic, Myanmar, Persian

### Examples

| type | name | label | appearance |
|------|------|-------|------------|
| date | dob | Date of Birth | |
| date | visit_month | Visit Month | month-year |
| time | appointment | Appointment Time | |
| dateTime | event_time | Event Date/Time | |

---

## Geospatial Types

| Type | Description |
|------|-------------|
| `geopoint` | Single GPS coordinate (lat, lon, alt, accuracy) |
| `geotrace` | Line of GPS coordinates |
| `geoshape` | Closed polygon |

### Geopoint Parameters

| Parameter | Description |
|-----------|-------------|
| `capture-accuracy` | Auto-capture when accuracy reached |
| `warning-accuracy` | Visual warning threshold |
| `allow-mock-accuracy` | Allow external GPS devices |

### Geopoint Appearances

| Appearance | Description |
|------------|-------------|
| `maps` | Display captured point on map |
| `placement-map` | Manual location selection on map |

### Examples

| type | name | label | appearance | parameters |
|------|------|-------|------------|------------|
| geopoint | location | Capture Location | maps | capture-accuracy=10 |
| geoshape | boundary | Draw Boundary | | |

---

## Media Types

| Type | Description |
|------|-------------|
| `image` | Photo capture/upload |
| `audio` | Audio recording |
| `video` | Video recording |
| `file` | Generic file upload |

### Image Appearances

| Appearance | Description |
|------------|-------------|
| `annotate` | Drawing overlay |
| `draw` | Sketch pad |
| `new` | Camera only (no gallery) |
| `new-front` | Front-facing camera |
| `signature` | Signature capture |

### Image Parameters

| Parameter | Description |
|-----------|-------------|
| `max-pixels` | Auto-scale (e.g., `max-pixels=1024`) |

### Audio Quality

| Quality | Size |
|---------|------|
| `voice-only` | ~5 MB/hour |
| `low` | ~11 MB/hour |
| `normal` | ~30 MB/hour |

### Examples

| type | name | label | appearance | parameters |
|------|------|-------|------------|------------|
| image | photo | Take Photo | new | max-pixels=1024 |
| image | signature | Signature | signature | |
| audio | voice | Voice Note | | quality=voice-only |
| video | interview | Record Interview | | |

---

## Special Types

| Type | Description |
|------|-------------|
| `note` | Display-only text (no data capture) |
| `calculate` | Hidden calculation field |
| `hidden` | Hidden field |
| `acknowledge` | Confirmation checkbox |
| `barcode` | Barcode/QR code scanner |
| `range` | Slider input |

### Range Parameters

| Parameter | Description |
|-----------|-------------|
| `start` | Minimum value |
| `end` | Maximum value |
| `step` | Increment |

### Examples

| type | name | label |
|------|------|-------|
| note | intro | Welcome to this survey |
| calculate | full_name | |
| acknowledge | consent_ack | I understand the terms |
| barcode | product_code | Scan Product |
| range | pain_level | Pain Level (1-10) |

---

## Metadata Types

Automatically captured system data.

| Type | Description |
|------|-------------|
| `start` | Form start timestamp |
| `end` | Form submission timestamp |
| `today` | Current date |
| `deviceid` | Device identifier |
| `phonenumber` | SIM phone number |
| `username` | Logged-in username |
| `email` | User email |
| `audit` | Audit logging |

### Example

| type | name |
|------|------|
| start | start_time |
| end | end_time |
| today | today_date |
| deviceid | device_id |
| audit | audit |
