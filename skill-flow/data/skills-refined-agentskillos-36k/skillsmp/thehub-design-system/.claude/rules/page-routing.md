# TheHUB Page Routing Rules

## CRITICAL: V1.0 Section-Based Routing

The router (`/router.php`) uses section-based routing. **Always check `router.php` before editing any page file!**

### Series Pages
| URL Pattern | Actual File | Purpose |
|-------------|-------------|---------|
| `/series` | `/pages/series/index.php` | List all series |
| `/series/9` | `/pages/series/show.php` | **Single series view** |
| `/series-single` | `/pages/series-single.php` | LEGACY - NOT USED for /series/X |

**IMPORTANT:** When user asks to edit `/series/9`, edit `/pages/series/show.php` NOT `/pages/series-single.php`!

### Other Common Routes
| URL Pattern | Actual File |
|-------------|-------------|
| `/rider/123` | `/pages/rider.php` |
| `/event/456` | `/pages/event.php` |
| `/club/789` | `/pages/club.php` |
| `/ranking` | `/pages/ranking.php` |
| `/calendar` | `/pages/calendar/index.php` |
| `/calendar/event/123` | `/pages/calendar/event.php` |

### Routing Logic (from router.php)
```php
$sectionRoutes = [
    'series' => [
        'index' => '/pages/series/index.php',
        'show' => '/pages/series/show.php'   // <-- /series/9 uses this!
    ],
    'calendar' => [
        'index' => '/pages/calendar/index.php',
        'event' => '/pages/calendar/event.php'
    ],
    // ...
];

// If second segment is numeric (like /series/9), it's an ID:
$detailPages = [
    'series' => 'show',   // /series/9 -> show.php
    'calendar' => 'event',
    // ...
];
```

## Database Helpers

- **V3 pages** use `hub_db()` which returns raw `PDO`
- **Admin pages** use `getDB()` which returns `Database` wrapper class
- **Club points system** (`/includes/club-points-system.php`) expects `Database` wrapper

## Key Files for Series

| File | Purpose |
|------|---------|
| `/pages/series/show.php` | Main series detail page (standings, club championship) |
| `/pages/series/index.php` | Series listing page |
| `/includes/series-points.php` | Series points calculation functions |
| `/includes/club-points-system.php` | Club championship 100%/50% rule |
| `/admin/series-events.php` | Admin: manage series events and point templates |

## Series Points System

- **Individual standings**: Uses `series_results` table (or fallback to `results`)
- **Club standings**: 100%/50% rule - best rider per club/class/event = 100%, second = 50%, others = 0%
- **Template-based**: Points determined by `series_events.template_id` -> `point_scales` -> `point_scale_values`
- **NOT affected by**: `event_level` (sportmotion/national) - that's only for ranking points!

## Before Editing Any Page

1. Check the URL the user mentions
2. Look up the route in `/router.php`
3. Edit the CORRECT file based on routing
4. Test locally if possible
