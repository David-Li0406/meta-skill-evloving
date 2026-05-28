# Basic Page Test Example

## Scenario

User wants to verify that the homepage loads correctly with all expected elements.

## User Request

> "Test the homepage"

## Testing Steps

### 1. Start Development Server

```bash
pnpm dev
```

Wait for: `✓ Ready in XXXms`

### 2. Open Homepage

```typescript
mcp_chrome -
  devtoo_new_page({
    url: "http://localhost:3000",
    timeout: 30000,
  });
```

**Expected**: Page opens successfully, returns list of open pages.

### 3. Take Text Snapshot

```typescript
mcp_chrome -
  devtoo_take_snapshot({
    verbose: false,
  });
```

**What to verify**:

- Title tag is correct
- Main navigation is present
- Hero section content is visible
- Footer elements are present
- All expected sections load

**Example snapshot excerpt**:

```
uid=1_0 RootWebArea "Springfield Life" url="http://localhost:3000/"
  uid=1_1 navigation
    uid=1_2 link "SPRINGFIELDLIFE" url="http://localhost:3000/"
    uid=1_5 link "EPISODES" url="http://localhost:3000/episodes"
  uid=1_13 main
    uid=1_14 button "SKIP INTRO"
    uid=1_15 heading "SPRINGFIELD LIFE" level="1"
```

### 4. Capture Screenshot

```typescript
mcp_chrome -
  devtoo_take_screenshot({
    fullPage: true,
    format: "png",
    quality: 90,
  });
```

**Visual checks**:

- Layout matches design
- Colors are correct
- Images load
- Typography is readable
- No visual glitches

### 5. Check Console Messages

```typescript
mcp_chrome -
  devtoo_list_console_messages({
    types: ["error", "warn", "issue"],
  });
```

**Look for**:

- ❌ Errors: JavaScript exceptions, network failures
- ⚠️ Warnings: Deprecations, missing props, performance issues
- ℹ️ Issues: CORS blocks, resource loading problems

**Example clean output**:

```json
{
  "messages": []
}
```

**Example with warnings**:

```json
{
  "messages": [
    {
      "msgid": 28,
      "type": "warn",
      "text": "Image with src \"...\" has \"fill\" but is missing \"sizes\" prop"
    }
  ]
}
```

### 6. Verify Network Requests

```typescript
mcp_chrome -
  devtoo_list_network_requests({
    resourceTypes: ["document", "stylesheet", "script", "fetch"],
    pageSize: 20,
  });
```

**Check for**:

- Status codes in 200-299 range
- No 404 errors
- Reasonable response times
- Correct resource loading order

### 7. Test Critical Interaction

```typescript
// Click on a main navigation link
mcp_chrome - devtoo_click({ uid: "1_5" }); // Episodes link

// Verify navigation worked
mcp_chrome - devtoo_take_snapshot();

// Check URL changed
// Expected: url="http://localhost:3000/episodes"
```

## Test Report

### ✅ Passed Checks

- Homepage loads in < 2 seconds
- All sections render correctly
- Navigation is functional
- No console errors
- All network requests succeed (200 OK)
- Layout is visually correct

### ⚠️ Warnings Found

- Image missing `sizes` prop (performance optimization)
- Audio autoplay blocked (expected browser behavior)

### ❌ Issues Found

None

### 🎯 Recommendations

1. Add `sizes` prop to `CharacterImage` component for better performance
2. Document expected audio autoplay limitation in user guide

## Automation Script

For repeated testing, combine steps:

```typescript
async function testHomepage() {
  // Open
  (await mcp_chrome) - devtoo_new_page({ url: "http://localhost:3000" });

  // Snapshot
  const snapshot = (await mcp_chrome) - devtoo_take_snapshot();

  // Screenshot
  (await mcp_chrome) -
    devtoo_take_screenshot({
      fullPage: true,
      filePath: "./test-results/homepage.png",
    });

  // Console
  const console =
    (await mcp_chrome) -
    devtoo_list_console_messages({
      types: ["error"],
    });

  // Network
  const network =
    (await mcp_chrome) -
    devtoo_list_network_requests({
      resourceTypes: ["document", "fetch", "xhr"],
    });

  // Report
  return {
    snapshot,
    console,
    network,
    passed: console.messages.length === 0,
  };
}
```

## Success Criteria

| Criterion        | Status  | Notes            |
| ---------------- | ------- | ---------------- |
| Page loads       | ✅ Pass | < 2s load time   |
| No errors        | ✅ Pass | Console clean    |
| Navigation works | ✅ Pass | Links functional |
| Visual layout    | ✅ Pass | Matches design   |
| Network requests | ✅ Pass | All 200 OK       |

**Overall**: ✅ PASSED
