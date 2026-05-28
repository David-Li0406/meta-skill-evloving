# Error Patterns Reference

Comprehensive reference for identifying error conditions in browser screenshots and accessibility snapshots.

## Astro Error Patterns

### 404 Page (Not Found)

**Visual indicators:**
- Large "404" heading text
- "Not Found" or "Page Not Found" message
- Empty page with navigation only
- Default Astro 404 styling

**Snapshot patterns:**
```
heading "404"
text "Not Found"
text "Page Not Found"
```

### 500 Page (Server Error)

**Visual indicators:**
- "500" heading or error code
- "Internal Server Error" message
- Stack trace visible (development mode)
- Red error box with details

**Snapshot patterns:**
```
heading "500"
text "Internal Server Error"
text "Error"
code block with stack trace
```

### Build Errors

**Visual indicators:**
- Red error overlay
- Stack trace with file paths
- "Build failed" message
- Component import errors
- HMR (Hot Module Replacement) error overlay

**Snapshot patterns:**
```
text "Build failed"
text "Error:"
code block with "at" lines (stack trace)
text "Module not found"
text "Cannot find module"
```

## React Error Patterns

### Error Boundary Triggered

**Visual indicators:**
- "Something went wrong" message
- "Error" heading
- Fallback UI instead of expected content
- Stack trace in development

**Snapshot patterns:**
```
heading "Error"
text "Something went wrong"
text "An error occurred"
button "Try again" or "Reload"
```

### Uncaught Runtime Errors

**Visual indicators:**
- Red overlay covering the page
- Error message with component stack
- "Uncaught Error" or "Unhandled Rejection"
- File and line number references

**Snapshot patterns:**
```
text "Uncaught Error"
text "TypeError"
text "ReferenceError"
text "Cannot read property"
text "is not defined"
```

### Hydration Errors

**Visual indicators:**
- Content mismatch between server and client render
- Layout shift after page load
- Missing interactive elements
- Console warnings about hydration

**Console signatures:**
```
"Hydration failed"
"Text content mismatch"
"Expected server HTML to contain"
"There was an error while hydrating"
```

## Network Error Indicators

### Broken Images

**Visual indicators:**
- Alt text visible instead of image
- Placeholder/broken image icon
- Empty image containers
- Image border with no content

**Snapshot patterns:**
```
img[alt="..."] with no loaded src
text where image expected
```

### Missing CSS (Unstyled Content)

**Visual indicators:**
- Times New Roman or default serif font
- No colors/background
- Elements stacked vertically (no flexbox/grid)
- Full-width content without margins
- Links in default blue with underlines

**Snapshot patterns:**
```
Link elements with no styling
Plain text layout
No semantic structure visible
```

### Failed API Calls

**Visual indicators:**
- Empty data states where content expected
- "undefined" or "null" rendered as text
- "No data" or "No results" when data should exist
- Error messages about fetch failures
- Missing list items in expected lists

**Snapshot patterns:**
```
text "undefined"
text "null"
text "No data"
text "Failed to load"
text "Error loading"
list with 0 items
empty group/container
```

### Infinite Loading

**Visual indicators:**
- Loading spinner that never resolves
- Skeleton UI that never populates
- "Loading..." text persisting
- Pulsing/animated placeholders stuck

**Snapshot patterns:**
```
text "Loading..."
text "Loading" (persisting after 5+ seconds)
progressbar role elements
img[alt="loading"] or similar
```

## Console Error Signatures

### JavaScript Errors

| Error Type | Indicates |
|------------|-----------|
| `TypeError` | Accessing property of null/undefined |
| `ReferenceError` | Using undefined variable |
| `SyntaxError` | Invalid JavaScript syntax |
| `RangeError` | Value out of allowed range |

### Network Errors

| Error Pattern | Indicates |
|---------------|-----------|
| `Failed to fetch` | Network request failed |
| `NetworkError` | Connection issue |
| `net::ERR_CONNECTION_REFUSED` | Backend not running |
| `CORS error` | Cross-origin blocked |
| `AbortError` | Request cancelled |

### React/Framework Errors

| Error Pattern | Indicates |
|---------------|-----------|
| `Hydration failed` | Server/client mismatch |
| `Text content mismatch` | Hydration issue |
| `Invalid hook call` | Hook used outside component |
| `Maximum update depth exceeded` | Infinite render loop |
| `Cannot update during render` | State update in render |

### Module Loading Errors

| Error Pattern | Indicates |
|---------------|-----------|
| `ChunkLoadError` | Failed to load code chunk |
| `Loading chunk X failed` | Bundle loading issue |
| `Module not found` | Import path wrong |
| `Cannot find module` | Missing dependency |

## Expected Page Structures for Guitar Tone Shootout

### Landing Page (`/`)

**Expected elements:**
- Navigation bar with logo and links
- Hero section with main call-to-action
- Feature highlights or recent shootouts
- Footer with links

**Snapshot should contain:**
```
navigation landmark
heading (main title)
link "Browse" or similar
link "Login" or similar
footer or contentinfo landmark
```

**Error indicators:**
- Missing navigation
- No hero content
- Empty main section
- Missing footer

### Gear Browse Page (`/gear`)

**Expected elements:**
- Grid of gear pack cards
- Search or filter controls
- Pagination or infinite scroll
- Card with title, thumbnail, metadata

**Snapshot should contain:**
```
navigation landmark
search textbox or filter controls
list or grid of items
link elements (to individual shootouts)
img elements (thumbnails)
```

**Error indicators:**
- "No shootouts found" when data should exist
- Empty grid/list
- Missing thumbnails (broken images)
- No filter controls

### Builder Page (`/builder`)

**Expected elements:**
- Multi-step form or single form
- Tone selection interface
- File upload controls
- Submit button
- Validation feedback

**Snapshot should contain:**
```
form landmark or role
textbox elements (title, description)
combobox or listbox (tone selection)
button "Submit" or "Create"
```

**Error indicators:**
- Form not rendering
- Missing input fields
- No submit button
- Validation errors before input

### Shootout Detail (`/shootout/[id]`)

**Expected elements:**
- Shootout title and description
- Audio/video player controls
- Tone comparison interface
- Voting or rating UI
- Comments section (if applicable)

**Snapshot should contain:**
```
heading (shootout title)
button elements (play, pause, etc.)
slider or progress controls
button "Vote" or comparison controls
```

**Error indicators:**
- "Shootout not found" message
- Missing player controls
- No comparison UI
- Error loading media

## Quick Reference: Pass/Fail Patterns

### Patterns That Always Indicate FAIL

- `TypeError:` in console
- `500 Internal Server Error` on page
- `undefined` or `null` rendered as text
- Empty lists where data expected
- Loading state persisting > 5 seconds
- Error boundary fallback UI
- Stack trace visible on page

### Patterns That Usually Indicate PASS

- Expected headings present
- Navigation functional
- Data rendered in lists/grids
- Forms have expected inputs
- No console errors
- All network requests 2xx
- Interactive elements respond
