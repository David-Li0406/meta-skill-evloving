---
name: machina-ui
description: Debug and understand MachinaMed frontend UI data flow. Use for investigating UI display issues, tracing data from backend API to React components, and understanding how biomarkers and reference ranges are rendered at /markers page (port 3000). Includes browser automation for visual verification and testing.
---

# Machina UI Skill

Debug and understand the MachinaMed frontend UI, particularly the `/markers` page. This skill helps investigate how data flows from the backend API through React components to the final UI display.

## When to Use This Skill

Use this skill when you need to:
- Debug why UI elements aren't displaying correctly (e.g., blank sections, missing data)
- Trace data flow from backend API → frontend TypeScript → React components → rendered UI
- Understand the `/markers` page biomarker display and modal popup
- Investigate reference range display issues
- Verify what data the backend sends vs. what the UI renders

## Frontend Architecture Overview

### /markers Page Stack

**Route**: `/markers` (port 3000)

**Component Hierarchy**:
```
app/(app)/markers/page.tsx
  └── FHIRStorageView (fhir-storage-view.tsx)
      ├── FHIRStorageTableView OR FHIRStorageGridView
      └── ObservationMetricModal (observation-metric-modal.tsx)  <-- Biomarker popup
          ├── ObservationHistoryChart
          ├── ReferenceRangeDisplay (reference-range-display.tsx)  <-- Reference Ranges section
          ├── BodySystemsTable
          └── BiomarkerDescription
```

### Data Flow

1. **Backend API** (`GET /api/v1/graph-memory/medical/observations/grouped`)
   - Returns `ObservationsResponse` with biomarkers and reference ranges
   - See "Backend API Response Structure" section below

2. **API Service Layer** (`src/services/api/fhir-storage.ts`)
   - `getObservations()` fetches from backend
   - `getObservationTypeByUuid()` fetches biomarker description

3. **Data Transformation** (`src/lib/observation-transformers.ts`)
   - `transformObservationTypeGroupedResponse()` converts API response to `ObservationMetric`
   - Extracts `reference_range` from `document_reference_range.reference_range`

4. **React Components** (TypeScript)
   - `ObservationMetricModal` displays popup when clicking a biomarker
   - `ReferenceRangeDisplay` renders reference ranges section
   - Types defined in `src/types/fhir-storage.ts`

5. **UI Rendering** (HTML/CSS)
   - Mantine/HeroUI components
   - Flexoki color system

## Known Issues

### Issue #1: Reference Ranges Section Blank [FIXED]

**Status**: ✅ **FIXED** - Backend now populates `category` field

**Problem**: When clicking on a biomarker (e.g., "Total Cholesterol") in the `/markers` page, the popup modal shows a graph and "REFERENCE RANGES" section, but the reference ranges section was completely blank.

**Root Cause**: The `ReferenceRangeDisplay` component filters out intervals where `category` is `null`:

```tsx
// File: src/components/fhir-storage/reference-range-display.tsx (line 22)
.filter((interval) => interval.category !== null && interval.category !== undefined)
```

**Previous Backend Behavior**: The backend was sending reference ranges with `category: null`:

```json
{
  "document_reference_range": {
    "reference_range": {
      "intervals": [{
        "label": "Document Range",
        "category": null,    // <-- This was NULL!
        "text": "<200"
      }]
    }
  }
}
```

**Fix Applied**: Updated backend to set `category: "Normal"` for document-extracted reference ranges:

```python
# File: repos/dem2/services/medical-data-engine/src/machina/medical_data_engine/engine/processors/biomarker/observation_converter.py (line 349-355)
interval = RangeInterval(
    label="Document Range",
    category=IntervalCategory.NORMAL,  # <-- Now set to NORMAL
    text=reference_range_text,
    low=None,
    high=None,
)
```

**Rationale**: Document-extracted reference ranges represent the "normal" or expected range from lab reports, so `IntervalCategory.NORMAL` is the appropriate default category.

**After Fix**: Backend now sends:

```json
{
  "document_reference_range": {
    "reference_range": {
      "intervals": [{
        "label": "Document Range",
        "category": "Normal",    // <-- Now populated!
        "text": "<200"
      }]
    }
  }
}
```

**Testing**: To verify the fix works:
1. Upload and process a document with biomarkers:
   - Upload: `(cd repos/dem2 && just curl_api '{"function": "upload_file", "path": "datasets/documents/test.pdf"}')`
   - Process: `(cd repos/dem2 && just curl_api '{"function": "process_document", "file_id": "file-id-from-upload"}')`
2. Check reference ranges in API response: `(cd repos/dem2 && bash -c 'source scripts/curl_api.sh && _get_patient_id_internal && auth_backend "/graph-memory/medical/observations/grouped?q=cholesterol" | jq ".items[0].document_reference_range.reference_range.intervals[0].category"')`
3. Expected output: `"Normal"` (not `null`)
4. Open `/markers` in browser and click on a biomarker - reference ranges section should now display

**Related Files**:
- **Backend (Fixed)**: `repos/dem2/services/medical-data-engine/src/machina/medical_data_engine/engine/processors/biomarker/observation_converter.py` (lines 29-32, 349-355)
- **Frontend (Filter)**: `repos/dem2-webui/src/components/fhir-storage/reference-range-display.tsx` (line 22)
- **Types**: `repos/dem2-webui/src/types/fhir-storage.ts` (lines 598-637, 749-760)

## Backend API Reference

### Authentication

Uses `curl_api.sh` helper functions from `repos/dem2/scripts/curl_api.sh`.

**Default Context**:
- **Email**: `dbeal@numberone.ai` (set via `AUTH_EMAIL` env var)
- **Patient**: Stuart McClure, DOB: 1969-03-03 (default patient context)
- **Backend API**: `http://localhost:8000/api/v1`

### Endpoints

#### 1. List Health Markers

**Endpoint**: `GET /api/v1/graph-memory/medical/observations/grouped`

**Purpose**: Retrieve all health markers (observations grouped by type) for the current patient context.

**Authentication Required**: Yes (JWT token + `X-Patient-Context-ID` header)

**Example Usage**:
```bash
# From repos/dem2 directory
(cd repos/dem2 && bash -c '
source scripts/curl_api.sh
_get_patient_id_internal
auth_backend "/graph-memory/medical/observations/grouped"
')
```

**Query Parameters**:
- `per_type_values_limit` - Limit number of most recent values per type (e.g., 2 for latest 2 values)
- `codes` - Filter by specific biomarker codes (comma-separated)
- `body_systems` - Filter by body systems
- `q` - Search query for observation names

**Example with Parameters**:
```bash
(cd repos/dem2 && bash -c '
source scripts/curl_api.sh
_get_patient_id_internal
auth_backend "/graph-memory/medical/observations/grouped?per_type_values_limit=5&q=cholesterol"
')
```

#### 2. Get Observation Statistics

**Endpoint**: `GET /api/v1/graph-memory/medical/observations/stats`

**Example Usage**:
```bash
(cd repos/dem2 && bash -c '
source scripts/curl_api.sh
_get_patient_id_internal
auth_backend "/graph-memory/medical/observations/stats"
')
```

**Response**:
```json
{
  "green_count": 0,
  "yellow_count": 0,
  "red_count": 0,
  "white_count": 132,
  "total_count": 132
}
```

#### 3. Get Document References

**Endpoint**: `GET /api/v1/graph-memory/medical/document_references`

**Example Usage**:
```bash
(cd repos/dem2 && bash -c '
source scripts/curl_api.sh
_get_patient_id_internal
auth_backend "/graph-memory/medical/document_references"
')
```

#### 4. Get Observation Type Details

**Endpoint**: `GET /api/v1/graph-memory/medical/observations/types/by-uuid/{uuid}`

**Purpose**: Get detailed biomarker description (shows in right sidebar of modal)

**Example Usage**:
```bash
(cd repos/dem2 && bash -c '
source scripts/curl_api.sh
_get_patient_id_internal
auth_backend "/graph-memory/medical/observations/types/by-uuid/{uuid}"
')
```

## Backend API Response Structure

### ObservationsResponse (from /observations/grouped)

```json
{
  "total_count": 132,
  "items": [
    {
      "observation_type": {
        "uid": "e85369a2-d208-4241-89e7-ae635cc6ffb1",
        "code": "bm_ba6f81de69e27fbc",
        "name": "Cholesterol",
        "display_name": "Total Cholesterol",
        "unit": "mg/dL"
      },
      "clinical_importance": 1.9605,
      "values": [
        {
          "uid": "d24dbbde-79b0-40fe-aa10-efde850b2f53",
          "value_numeric": 163.0,
          "value_text": "163",
          "observed_at": "2025-07-03T00:00:00Z",
          "unit": "mg/dL",
          "document_interpretation": null,
          "document_value_color": null,
          "value_status": null
        }
      ],
      "values_count": 4,
      "body_systems": [
        {
          "system": "cardiovascular",
          "weight": 0.85,
          "impact_type": "marker"
        }
      ],
      "document_reference_range": {
        "uid": "ac799880-bc18-4c32-8eb0-fee4d2965552",
        "reference_range": {
          "intervals": [
            {
              "label": "Document Range",
              "category": null,
              "color": null,
              "low": null,
              "high": null,
              "low_inclusive": true,
              "high_inclusive": true,
              "text": "<200"
            }
          ]
        },
        "range_type": "document",
        "source_type": "document",
        "source_id": "1c6ca887-3fcd-41f1-b6a4-d6b481a26473"
      },
      "standard_reference_range": null
    }
  ]
}
```

**Key Fields**:
- `observation_type.uid` - UUID for the biomarker type
- `observation_type.display_name` - Display name shown in UI
- `values[]` - Array of observation values (historical data)
- `document_reference_range.reference_range` - **This is where reference ranges come from!**
- `document_reference_range.reference_range.intervals[]` - Array of intervals with `category`, `label`, `text`

## Common Debugging Patterns

### List All Biomarker Names

```bash
(cd repos/dem2 && bash -c '
source scripts/curl_api.sh
_get_patient_id_internal
auth_backend "/graph-memory/medical/observations/grouped"
' | jq -r '.items[] | "\(.observation_type.display_name) (\(.observation_type.unit))"')
```

### Check Reference Ranges for a Specific Biomarker

```bash
(cd repos/dem2 && bash -c '
source scripts/curl_api.sh
_get_patient_id_internal
auth_backend "/graph-memory/medical/observations/grouped?q=cholesterol"
' | jq '.items[].document_reference_range.reference_range')
```

### Count Total Biomarkers

```bash
(cd repos/dem2 && bash -c '
source scripts/curl_api.sh
_get_patient_id_internal
auth_backend "/graph-memory/medical/observations/stats"
' | jq '.total_count')
```

### Verify Reference Range Data Exists

```bash
# Check if intervals have category field
(cd repos/dem2 && bash -c '
source scripts/curl_api.sh
_get_patient_id_internal
auth_backend "/graph-memory/medical/observations/grouped?per_type_values_limit=1"
' | jq '.items[0].document_reference_range.reference_range.intervals[0]')
```

## Frontend Code References

**Key Files**:
- **Page**: `repos/dem2-webui/src/app/(app)/markers/page.tsx`
- **Main View**: `repos/dem2-webui/src/components/fhir-storage/fhir-storage-view.tsx`
- **Modal Popup**: `repos/dem2-webui/src/components/fhir-storage/observation-metric-modal.tsx` (line 302-305 for reference range display)
- **Reference Range Display**: `repos/dem2-webui/src/components/fhir-storage/reference-range-display.tsx` (line 22 for filter bug)
- **API Service**: `repos/dem2-webui/src/services/api/fhir-storage.ts` (line 47-48 for getObservations)
- **Transformers**: `repos/dem2-webui/src/lib/observation-transformers.ts` (line 54 for reference_range extraction)
- **Types**: `repos/dem2-webui/src/types/fhir-storage.ts` (lines 598-637 for RangeInterval, lines 749-760 for IntervalCategory)

## Error Handling

If authentication fails or the backend is not running:

```
curl: (7) Failed to connect to localhost port 8000
```

**Solutions**:
1. Ensure backend is running: `(cd repos/dem2 && just run)`
2. Check backend health: `curl http://localhost:8000/health`
3. Verify user exists: `(cd repos/dem2 && scripts/user_manager.py user list)`
4. Check patient context: `(cd repos/dem2 && scripts/user_manager.py patient list)`

## Example Workflow: Debug Reference Ranges Issue

```bash
# 1. Start backend
(cd repos/dem2 && just run)

# 2. Check if reference ranges exist in backend response
(cd repos/dem2 && bash -c '
source scripts/curl_api.sh
_get_patient_id_internal
auth_backend "/graph-memory/medical/observations/grouped?q=cholesterol"
' | jq '.items[0].document_reference_range.reference_range')

# 3. Verify the category field
(cd repos/dem2 && bash -c '
source scripts/curl_api.sh
_get_patient_id_internal
auth_backend "/graph-memory/medical/observations/grouped?q=cholesterol"
' | jq '.items[0].document_reference_range.reference_range.intervals[0].category')

# Output: null  <-- This is the problem!

# 4. Check frontend code
# Open repos/dem2-webui/src/components/fhir-storage/reference-range-display.tsx
# Line 22: .filter((interval) => interval.category !== null && interval.category !== undefined)
# This filter removes all intervals with category: null

# 5. Test the fix: Remove the filter or update backend to populate category
```

## Browser Automation for Visual Verification

This skill includes browser automation capabilities for testing the `/markers` page and verifying UI rendering.

### ⚠️ IMPORTANT: Browser Authentication Required

**The `/markers` page requires authentication.** Before navigating to any authenticated page, you MUST set authentication cookies in the browser.

**How to get authentication cookies:**

```bash
cd repos/dem2 && ./scripts/user_manager.py user token dbeal@numberone.ai --export-cookie
```

**Output example:**
```
export AUTH_HEADER="Cookie: access_token=eyJhbG...; refresh_token=eyJhbG...; __stripe_mid=..."
```

**Set cookies in Playwright browser:**

```javascript
await page.context().addCookies([
  {
    name: 'access_token',
    value: 'eyJhbG...', // Copy from user_manager.py output
    domain: 'localhost',
    path: '/',
    httpOnly: true,
    secure: false,
    sameSite: 'Lax'
  },
  {
    name: 'refresh_token',
    value: 'eyJhbG...', // Copy from user_manager.py output
    domain: 'localhost',
    path: '/',
    httpOnly: true,
    secure: false,
    sameSite: 'Lax'
  },
  {
    name: '__stripe_mid',
    value: '...', // Copy from user_manager.py output
    domain: 'localhost',
    path: '/',
    httpOnly: false,
    secure: false,
    sameSite: 'Lax'
  }
]);
```

**Then navigate to the page:**
```javascript
await page.goto('http://localhost:3000/markers');
```

**Without authentication, the browser will redirect to the login page (`/auth`).**

### When to Use Browser Automation

Use browser automation for:
- **Visual verification** of UI rendering issues (screenshots and snapshots)
- **Testing workflows** on the /markers page (clicking biomarkers, opening modals)
- **Element interaction** testing (verify modals open, forms work correctly)
- **Content extraction** to verify what's actually rendered in the DOM
- **Regression testing** after fixing UI bugs
- **Accessibility analysis** to understand page structure

### Common Testing Workflows

#### Test the /markers Page Loading

Navigate to the markers page and verify it loads correctly:

**Example**: Check that biomarker cards are displayed
- Navigate to `http://localhost:3000/markers`
- Take a snapshot to see the page structure
- Take a screenshot to verify visual rendering
- Look for biomarker cards and data

#### Test Biomarker Modal Interaction

Click on a biomarker card and verify the modal opens with correct data:

**Example workflow**:
1. Navigate to the markers page
2. Get a snapshot to find biomarker card elements
3. Click on a specific biomarker (e.g., "Total Cholesterol")
4. Verify the modal opens
5. Check that reference ranges section displays correctly
6. Screenshot the modal for visual verification

**Common elements to verify**:
- Biomarker name and current value displayed
- Historical chart renders correctly
- Reference ranges section shows intervals (not blank)
- Body systems table populated
- Biomarker description appears

#### Debug Reference Ranges Display Issue

Test whether reference ranges are showing in the modal:

**Workflow**:
1. Verify backend sends reference range data (use curl_api.sh)
2. Navigate to markers page in browser
3. Click on a biomarker with known reference ranges
4. Snapshot the modal to verify DOM structure
5. Check if "REFERENCE RANGES" section has content
6. If blank, inspect the intervals data in snapshot

**Example verification**:
- Backend API shows `category: "Normal"` in reference range intervals
- Frontend snapshot shows reference range intervals in DOM
- Visual screenshot confirms reference ranges section displays text

#### Compare Before/After UI Fixes

When fixing a UI bug, capture evidence:

**Workflow**:
1. Navigate to page with the bug
2. Screenshot "before fix" state
3. Apply code changes (backend or frontend)
4. Restart affected service
5. Navigate to same page
6. Screenshot "after fix" state
7. Compare screenshots to verify fix

**Example**:
- Before: Reference ranges section blank
- After: Reference ranges section shows "Document Range: <200 mg/dL"

### Testing After Code Changes

After fixing a UI bug:

1. **Restart frontend** (if TypeScript changes): `(cd repos/dem2-webui && pnpm dev)`
2. **Restart backend** (if API changes): `(cd repos/dem2 && just run)`
3. **Use browser automation** to verify the fix
4. **Capture screenshots** as evidence

### Browser Automation vs Manual Testing

**Browser Automation Advantages**:
- ✅ Automated and repeatable
- ✅ Fresh browser context (no cached state)
- ✅ Captures screenshots as artifacts
- ✅ Faster than manual clicking
- ✅ Can extract DOM structure programmatically

**Manual Testing Advantages**:
- ✅ Browser DevTools for inspecting elements
- ✅ Network tab for debugging API calls
- ✅ React DevTools for component inspection

**Best Practice**: Use browser automation for regression testing and screenshots, use manual testing for deep debugging with DevTools.

### Screenshots Storage

Screenshots are saved to: `.playwright-mcp/`

**Example structure**:
```
.playwright-mcp/
  markers-page-loaded.png
  cholesterol-modal-before-fix.png
  cholesterol-modal-after-fix.png
  reference-ranges-displayed.png
```

### Integration with machina-ui Debugging

When debugging UI issues with this skill:

1. **Backend Verification**: Use `curl_api.sh` commands to verify backend data
2. **Code Tracing**: Read TypeScript/React source code to understand logic
3. **Visual Verification**: Use browser automation to capture screenshots and test UI
4. **Root Cause Analysis**: Combine all three to identify the issue
5. **Fix Validation**: Use browser automation to prove the fix works

## Related Skills

- **machina-git**: For git operations in the workspace
- **kubernetes**: For deployment and cluster operations

## Notes

- The frontend runs on port 3000 (Next.js)
- The backend runs on port 8000 (FastAPI)
- All API calls require authentication (JWT token)
- Patient context is required for most endpoints (`X-Patient-Context-ID` header)
- The skill calls backend APIs directly to verify data, then traces through TypeScript/React code to understand UI rendering
- Browser automation tools are available for visual verification and testing workflows
