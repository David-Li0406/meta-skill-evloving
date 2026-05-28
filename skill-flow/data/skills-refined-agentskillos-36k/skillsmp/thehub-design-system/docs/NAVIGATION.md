# TheHUB Navigation Architecture

**Senast uppdaterad:** 2026-01-12

---

## Primär navigationsfil

`/components/sidebar.php` - Enda navigationsfilen som ska användas för rendering.

**Använd ALDRIG:**
- `admin-sidebar.php` (deprecated)
- `navigation.php` (deprecated)

---

## Konfiguration

`/includes/config/admin-tabs-config.php` - Definierar alla admin-flikar och grupper.

### Struktur i admin-tabs-config.php:

```php
$ADMIN_TABS = [
    'competitions' => [
        'title' => 'Tävlingar',
        'icon' => 'calendar-check',
        'tabs' => [
            ['id' => 'events', 'label' => 'Events', 'url' => '/admin/events.php', 'pages' => [...]]
        ]
    ],
    // ... fler grupper
];
```

### Grupper:
1. **competitions** - Tävlingar, resultat, texter, elimination
2. **standings** - Serier, ranking, klubbpoäng
3. **database** - Deltagare, klubbar, anläggningar
4. **config** - Ekonomi, klasser, sponsorer, media, mm
5. **import** - All dataimport
6. **settings** - System (endast super_admin)

---

## Rollbaserad visning

Navigationen anpassas automatiskt baserat på användarens roll:

| Roll | Vad visas |
|------|-----------|
| `rider` | Publik navigation endast |
| `promotor` | Promotor-sektion + begränsad admin |
| `admin` | Full admin (utom System) |
| `super_admin` | Allt |

### Rollkontroll i kod:

```php
// Hierarkisk kontroll (promotor kan INTE accessa admin)
if (hasRole('admin')) { ... }

// Exakt kontroll (är EXAKT denna roll)
if (isRole('promotor')) { ... }
```

---

## Filer och deras syfte

| Fil | Syfte |
|-----|-------|
| `/components/sidebar.php` | **PRIMÄR** - Renderar all navigation |
| `/includes/config/admin-tabs-config.php` | Definierar admin-menystruktur |
| `/admin/components/admin-mobile-nav.php` | Mobilnavigation (håll i sync med config) |
| `/components/icons.php` | `hub_icon()` för Lucide-ikoner |

---

## Deprecated filer (TA INTE BORT FRÅN ARKIV)

Dessa filer finns kvar för referens men ska ALDRIG användas:

- `/admin/components/archived/admin-sidebar.php.deprecated`
- `/admin/components/archived/admin-layout.php.deprecated`
- `/includes/archived/navigation.php.deprecated`

---

## Hur man lägger till nya menyalternativ

### 1. Redigera admin-tabs-config.php

```php
// Lägg till ny flik i befintlig grupp
'config' => [
    'tabs' => [
        // ... befintliga flikar
        [
            'id' => 'new-feature',
            'label' => 'Ny Funktion',
            'icon' => 'star',           // Lucide icon name
            'url' => '/admin/new-feature.php',
            'pages' => ['new-feature.php', 'new-feature-edit.php'],
            'role' => 'admin'           // Valfritt: begränsa till viss roll
        ]
    ]
]
```

### 2. Uppdatera admin-mobile-nav.php (om mobil ska ha snabbåtkomst)

Om den nya funktionen ska vara direkt åtkomlig i mobilmenyn, lägg till i `$adminNav` arrayen.

### 3. Sätt rätt `role` för åtkomstkontroll

- `'role' => 'promotor'` - Alla inloggade
- `'role' => 'admin'` - Admin och super_admin
- `'role' => 'super_admin'` - Endast super_admin

---

## Layout-filer

### Unified Layout (ANVÄND DENNA)

```php
$page_title = 'Min Sida';
include __DIR__ . '/components/unified-layout.php';
?>

<!-- Ditt innehåll här -->

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
```

### Legacy Layout (undvik)

Följande filer använder fortfarande gammal layout och bör migreras:
- `fix-rider-clubs.php`
- `settings-imgbb.php`
- `simple-merge-duplicates.php`

---

## Mobilnavigation

Mobilnavigeringen hanteras av:
- `/admin/components/admin-mobile-nav.php` - Admin-sidor
- `/components/mobile-nav.php` - Publika sidor

Dessa är separata från sidebar.php och måste hållas manuellt i sync.

---

## Troubleshooting

### Problem: Ny menypost syns inte
1. Kontrollera att posten finns i `admin-tabs-config.php`
2. Kontrollera att användarrollen har rätt åtkomst
3. Rensa eventuell cache

### Problem: Aktiv-markering fungerar inte
1. Kontrollera att sidans filnamn finns i `pages`-arrayen
2. Kontrollera `isAdminPageActive()` i sidebar.php

### Problem: Ikon visas inte
1. Kontrollera att ikonnamnet finns i Lucide-biblioteket
2. Kontrollera att `hub_icon()` är korrekt anropad
