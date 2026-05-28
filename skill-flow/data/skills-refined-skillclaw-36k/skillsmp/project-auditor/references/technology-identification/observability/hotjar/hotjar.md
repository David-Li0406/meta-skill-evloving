# Hotjar

**Category**: observability
**Description**: Heatmaps, session recordings, and user feedback tool
**Homepage**: https://hotjar.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Hotjar packages*

- `@hotjar/browser` - Official browser SDK
- `react-hotjar` - React Hotjar wrapper
- `hotjar-js` - Alternative wrapper

---

## TIER 2: Deep Detection (File-based)

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`, `.jsx`, `.tsx`

**Pattern**: `from\s+['"]@hotjar/browser['"]`
- Hotjar browser SDK import
- Example: `import Hotjar from '@hotjar/browser';`

**Pattern**: `from\s+['"]react-hotjar['"]`
- React Hotjar import
- Example: `import { hotjar } from 'react-hotjar';`

### Code Patterns

**Pattern**: `Hotjar\.init\(|hotjar\.initialize\(`
- Hotjar initialization
- Example: `Hotjar.init(SITE_ID, HOTJAR_VERSION);`

**Pattern**: `hj\(['"]trigger['"]|hj\(['"]event['"]`
- Hotjar tracking calls
- Example: `hj('trigger', 'survey-name');`

**Pattern**: `static\.hotjar\.com|script\.hotjar\.com`
- Hotjar script URLs
- Example: `https://static.hotjar.com/c/hotjar-`

**Pattern**: `HOTJAR_ID|HOTJAR_SITE_ID|HOTJAR_VERSION`
- Hotjar environment variables
- Example: `HOTJAR_ID=1234567`

**Pattern**: `_hjSettings|hjid|hjsv`
- Hotjar configuration variables
- Example: `h._hjSettings = { hjid: 1234567, hjsv: 6 };`

---

## Environment Variables

- `HOTJAR_ID` - Hotjar site ID
- `HOTJAR_SITE_ID` - Alternative site ID variable
- `HOTJAR_VERSION` - Hotjar snippet version
- `NEXT_PUBLIC_HOTJAR_ID` - Next.js Hotjar ID
- `REACT_APP_HOTJAR_ID` - Create React App ID
- `VITE_HOTJAR_ID` - Vite Hotjar ID

## Detection Notes

- Site ID is a numeric identifier
- Hotjar version is typically 6 (current)
- Heatmaps and recordings are core features
- Surveys and feedback widgets available
- GDPR compliance features built-in

---

## Secrets Detection

### Configuration

#### Hotjar Site ID
**Pattern**: `(?:hotjar|HOTJAR|hjid)\s*[=:]\s*['"]?([0-9]{6,8})['"]?`
**Severity**: low
**Description**: Hotjar site ID (public identifier)
**Example**: `HOTJAR_ID=1234567`

### Validation

#### API Documentation
- **JavaScript API**: https://help.hotjar.com/hc/en-us/articles/115009340387

---

## TIER 3: Configuration Extraction

### Site ID Extraction

**Pattern**: `(?:hjid|siteId|site[_-]?id)\s*[=:]\s*['"]?([0-9]{6,8})['"]?`
- Hotjar site ID
- Extracts: `site_id`
- Example: `hjid: 1234567`
