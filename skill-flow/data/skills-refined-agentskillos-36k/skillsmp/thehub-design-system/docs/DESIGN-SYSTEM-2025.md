# TheHUB Design System 2025

> Last updated: 2025-12-12

## Desktop Width Standards

### Container Max-Width
- **Standard container**: `1400px` (via `--content-max-width` CSS variable)
- **Previous value**: `1280px` (deprecated)
- **Implementation**: Use `var(--content-max-width, 1400px)` for fallback support

### Breakpoints (UNCHANGED)
- `1024px` = Breakpoint for desktop/mobile layout switch
- **IMPORTANT**: 1024px is ONLY a breakpoint, NEVER a container width

```css
/* CORRECT - Breakpoint usage */
@media (min-width: 1024px) { ... }
@media (max-width: 1023px) { ... }

/* INCORRECT - Never use 1024px as container width */
.container { max-width: 1024px; } /* DON'T DO THIS */
```

## Event Page Isolation

### Automatic Detection
Event pages are automatically detected via URL pattern `/event/{ID}` in `layout-header.php`.

```php
// Automatic - NO manual body class needed
$isEventPage = preg_match('#^/event/\d+#', $requestUri) === 1;
if ($isEventPage) {
    $bodyClasses[] = 'event-page';
}
```

### CSS Protection
Event pages have their container constraints removed to allow full-width results display:

```css
.event-page .main-content,
.event-page .container,
.event-page .page-wrap,
.event-page .content-wrap,
.event-page .content-prose {
    max-width: none;
}
```

### Rules
1. Event pages are **SACRED** - their layout must not be affected by global changes
2. Event page detection is **AUTOMATIC** via URL
3. **NEVER** manually add `event-page` class to body
4. If event results display changes, **REVERT IMMEDIATELY**

## Body Classes

The system automatically applies these body classes:

| Class | Description |
|-------|-------------|
| `admin-page` | Admin section pages |
| `public-page` | Public-facing pages |
| `is-admin` | Admin context (redundant with admin-page) |
| `is-public` | Public context (redundant with public-page) |
| `event-page` | Event detail pages (auto-detected) |

## CSS Variable Reference

### Layout Variables (tokens.css)
```css
:root {
    --content-max-width: 1400px;
    --sidebar-width: 72px;
    --header-height: 60px;
    --mobile-nav-height: 64px;
}
```

### Spacing Variables
```css
:root {
    --space-2xs: 4px;
    --space-xs: 8px;
    --space-sm: 12px;
    --space-md: 16px;
    --space-lg: 24px;
    --space-xl: 32px;
    --space-2xl: 48px;
    --space-3xl: 64px;
}
```

### Radius Variables
```css
:root {
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 14px;
    --radius-xl: 20px;
    --radius-full: 9999px;
}
```

## File Structure

### Core CSS Files (in load order)
1. `reset.css` - CSS reset
2. `tokens.css` - Design tokens and variables
3. `theme.css` - Light/dark theme colors
4. `layout.css` - Layout structure including event isolation
5. `components.css` - UI components
6. `tables.css` - Table styles
7. `utilities.css` - Utility classes
8. `grid.css` - Grid system
9. `pwa.css` - PWA support
10. `compatibility.css` - Legacy class mapping

### Legacy Files
These files exist for backwards compatibility:
- `gravityseries-theme.css`
- `gravityseries-main.css`
- `gravityseries-admin.css`

## Admin Menu Structure

The admin menu is organized into these groups (see `admin-tabs-config.php`):

1. **Tävlingar** - Events, Results, Venues, Economy, Sponsors
2. **Serier** - Series, Ranking, Club Points
3. **Databas** - Riders, Clubs
4. **Konfiguration** - Classes, Licenses, Point Scales, Rules, Public, Texts
5. **Import** - Overview, Riders, Results, Events, UCI, Venues, History
6. **System** (Super Admin) - Users, Permissions, Database, Tools, Media

## Migration Notes

### From v3.0 to v1.0
- Container max-width changed from `1280px` to `1400px`
- Use CSS variable `var(--content-max-width)` instead of hardcoded values
- Event pages now have automatic isolation via `.event-page` class
