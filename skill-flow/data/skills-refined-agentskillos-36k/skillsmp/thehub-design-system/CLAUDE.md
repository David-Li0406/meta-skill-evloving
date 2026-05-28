# TheHUB - Development Rules

> LÄS DENNA FIL INNAN DU SKRIVER NÅGON KOD

---

## VERSIONSNUMMER - OBLIGATORISKT

**UPPDATERA ALLTID versionsnumret i `config.php` vid varje push.**

```php
// config.php - Uppdatera APP_BUILD med dagens datum vid varje push
define('APP_VERSION', '1.0');          // Major.Minor version
define('APP_VERSION_NAME', 'Release');  // Version name
define('APP_BUILD', '2026-01-08');      // UPPDATERA DETTA: YYYY-MM-DD
define('DEPLOYMENT_OFFSET', 131);       // Ändra INTE
```

### Vid varje push:
1. Uppdatera `APP_BUILD` till dagens datum (YYYY-MM-DD)
2. Meddela användaren vilken version som skapades

### Format:
Version visas som: `v1.0 [2026-01-08.XXX] - Release`
- XXX = antal git commits + DEPLOYMENT_OFFSET (räknas automatiskt)

### Exempel på meddelande:
```
Pushat: TheHUB v1.0 [2026-01-08.XXX]
```

---

## ROADMAP - UPPDATERA EFTER VARJE IMPLEMENTATION

**Uppdatera ALLTID `/ROADMAP.md` efter varje implementerad funktion.**

### Vid varje avslutad uppgift:
1. Uppdatera status i ROADMAP.md (markera som KLAR)
2. Lägg till changelog-entry med datum och beskrivning
3. Dokumentera nya filer som skapats
4. Notera eventuella framtida förbättringar

### Format för changelog:
```markdown
### YYYY-MM-DD (Funktionsnamn)
- **Branch:** namn-på-branch

- **Ny funktion: Beskrivning**
  - Punkt 1
  - Punkt 2

- **Nya filer:**
  - `path/to/file.php` - Beskrivning
```

### Interaktiv roadmap:
Se `/admin/roadmap.php` för en visuell översikt av projektets status.

---

## MIGRATIONER - ALLTID I Tools/migrations

**ALLA databasmigrationer ska ligga i `/Tools/migrations/` - INGEN annanstans.**

```
Tools/
└── migrations/
    ├── 001_analytics_tables.sql
    ├── 002_...sql
    ├── 009_first_season_journey.sql
    ├── 010_longitudinal_journey.sql
    ├── 011_journey_brand_dimension.sql
    └── 012_event_participation_analysis.sql
```

### FÖRBJUDNA platser för migrationer:
```
analytics/migrations/   ← FEL! Arkiverad
admin/migrations/       ← FEL! Arkiverad
migrations/             ← FEL! Arkiverad
```

### Migreringsverktyg:
**ETT verktyg:** `/admin/migrations.php` (https://thehub.gravityseries.se/admin/migrations.php)

- Auto-detekterar vilka migrationer som körts (kollar databasstruktur)
- Visar status: Körd / Ej körd
- **Körda migrationer visas GRÖNMARKERADE**
- Kör migrationer direkt från UI
- Mobilanpassat

### Regler för nya migrationer:
1. Filnamn: `NNN_beskrivande_namn.sql` (t.ex. `013_ny_feature.sql`)
2. Ingen DELIMITER-syntax (funkar inte med PHP PDO)
3. Ingen dynamisk SQL (SET @sql / PREPARE / EXECUTE)
4. Endast standard SQL-statements
5. **Migrationer ska vara körbara via admin/migrations.php**

---

## ADMIN-VERKTYG - ALLTID I tools.php

**ALLA nya admin-verktyg ska länkas från `/admin/tools.php`**

URL: https://thehub.gravityseries.se/admin/tools.php

### Befintliga sektioner i tools.php:
- **Säsongshantering** - Årsåterställning, importgranskning
- **Klubbar & Åkare** - Synka klubbar, normalisera namn, UCI-ID
- **Datahantering** - Data Explorer, statistik, dubbletter, RF-registrering
- **Import & Resultat** - Importera, rensa, räkna om poäng
- **Felsökning** - Datakvalitet, diagnostik, fixa fel
- **Analytics - Setup** - Tabeller, historisk data
- **Analytics - Rapporter** - Dashboard, trender, kohorter
- **SCF Licenssynk** - SCF License Portal integration
- **System** - Cache, backup, migrationer

### När du skapar nya verktyg:
1. Skapa verktygets PHP-fil i `/admin/` eller `/admin/tools/`
2. **LÄGG ALLTID TILL länk i `/admin/tools.php`**
3. Placera under rätt sektion baserat på vad verktyget gör
4. Använd samma kortformat som befintliga verktyg:

```html
<div class="card">
    <div class="tool-header">
        <div class="tool-icon"><i data-lucide="ICON"></i></div>
        <div>
            <h4 class="tool-title">Verktygsnamn</h4>
            <p class="tool-description">Kort beskrivning</p>
        </div>
    </div>
    <div class="tool-actions">
        <a href="/admin/VERKTYG.php" class="btn-admin btn-admin-primary">Öppna</a>
    </div>
</div>
```

---

## INGA VERSIONSPREFIX - ALDRIG

**ANVÄND ALDRIG versionsnummer (V2, V3, V4) i filnamn, konstanter eller kod.**

Detta projekt har EN version. Alla gamla versionsreferenser är borttagna.

```php
// FEL - ALDRIG SÅ HÄR
HUB_V2_ROOT
HUB_V3_ROOT
HUB_V3_URL
include 'v2/pages/event.php';

// RÄTT - ALLTID SÅ HÄR
HUB_ROOT
HUB_URL
include 'pages/event.php';
```

### Korrekta konstanter:
- `HUB_ROOT` - Projektets rotmapp
- `HUB_URL` - Projektets bas-URL
- `ROOT_PATH` - Alias för HUB_ROOT (legacy)
- `INCLUDES_PATH` - `/includes` mappen

### Historik:
Projektet hade tidigare separata versioner (V2, V3) men dessa slogs samman 2026-01.
Alla V2/V3/V4-prefix är FÖRBJUDNA i ny kod.

---

## INGA EMOJIS - ALDRIG

**ANVÄND ALDRIG EMOJIS I KOD.** Använd alltid Lucide-ikoner istället.

```php
// FEL - ALDRIG SÅ HÄR
$icon = '🏁';
echo '📍 Plats';

// RÄTT - ALLTID SÅ HÄR
<i data-lucide="flag"></i>
<i data-lucide="map-pin"></i>
```

Vanliga Lucide-ikoner:
- `flag` - Mål/Start
- `map-pin` - Plats/POI
- `route` - Transport
- `cable-car` - Lift
- `save` - Spara
- `pencil` - Redigera
- `x` - Stäng
- `locate` - Min plats

---

## LÅSTA FILER - ÄNDRA ALDRIG

Följande filer får INTE modifieras utan explicit godkännande:

```
assets/css/tokens.css      # Design tokens (spacing, radius, fonts)
assets/css/theme.css       # Tema-variabler (Light/Dark mode)
assets/css/components.css  # UI-komponenter
assets/css/layout.css      # Layout-system
components/sidebar.php     # Sidebar navigation
components/header.php      # Sidheader
includes/layout-header.php # Layout wrapper
includes/layout-footer.php # Layout footer
```

---

## DESIGNSYSTEM - ANVÄND ALLTID

### CSS-variabler (OBLIGATORISKT)

TheHUB använder ett tema-baserat designsystem med Light/Dark Mode.
Tema styrs via `data-theme` attribut på `<html>` elementet.

```css
/* ===== DARK MODE (Default) ===== */
:root, html[data-theme="dark"] {
  /* Bakgrunder */
  --color-bg-page: #0b131e;
  --color-bg-surface: #0d1520;
  --color-bg-card: #0e1621;
  --color-bg-hover: rgba(255, 255, 255, 0.06);

  /* Text */
  --color-text-primary: #f8f2f0;
  --color-text-secondary: #c7cfdd;
  --color-text-muted: #868fa2;

  /* Accent - Cyan/Turquoise */
  --color-accent: #37d4d6;
  --color-accent-hover: #4ae0e2;
  --color-accent-light: rgba(55, 212, 214, 0.15);
  --color-accent-text: #37d4d6;

  /* Borders */
  --color-border: rgba(55, 212, 214, 0.2);
  --color-border-strong: rgba(55, 212, 214, 0.3);

  /* Status */
  --color-success: #10b981;
  --color-warning: #fbbf24;
  --color-error: #ef4444;
  --color-info: #38bdf8;
}

/* ===== LIGHT MODE ===== */
html[data-theme="light"] {
  /* Bakgrunder */
  --color-bg-page: #f8f9fa;
  --color-bg-surface: #ffffff;
  --color-bg-card: #ffffff;
  --color-bg-hover: rgba(55, 212, 214, 0.04);

  /* Text */
  --color-text-primary: #0b131e;
  --color-text-secondary: #495057;
  --color-text-muted: #868e96;

  /* Accent - Cyan/Turquoise (ljusare) */
  --color-accent: #2bc4c6;
  --color-accent-hover: #37d4d6;
  --color-accent-light: rgba(55, 212, 214, 0.1);
  --color-accent-text: #2bc4c6;

  /* Borders */
  --color-border: rgba(55, 212, 214, 0.15);
  --color-border-strong: rgba(55, 212, 214, 0.25);

  /* Status */
  --color-success: #059669;
  --color-warning: #d97706;
  --color-error: #dc2626;
  --color-info: #0284c7;
}
```

### Spacing (tokens.css)

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

  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --radius-xl: 20px;
  --radius-full: 9999px;
}
```

### Typografi

```css
:root {
  --font-heading: 'Oswald', sans-serif;           /* H1 rubriker */
  --font-heading-secondary: 'Cabin Condensed';    /* H2, H3 */
  --font-body: 'Manrope', sans-serif;             /* Brödtext */
  --font-link: 'Roboto', sans-serif;              /* Länkar */
}
```

### Serie-färger

```css
:root {
  --series-enduro: #FFE009;
  --series-downhill: #FF6B35;
  --series-xc: #2E7D32;
  --series-ges: #EF761F;
  --series-ggs: #8A9A5B;
  --series-gss: #6B4C9A;
  --series-gravel: #795548;
  --series-dual: #E91E63;
}
```

### FÖRBJUDET

```css
/* SKRIV ALDRIG DETTA */
background: #37d4d6;           /* Använd var(--color-accent) */
padding: 15px;                 /* Använd var(--space-md) eller var(--space-lg) */
border-radius: 8px;            /* Använd var(--radius-sm) */
color: gray;                   /* Använd var(--color-text-secondary) */
background: #0b131e;           /* Använd var(--color-bg-page) */
```

### KORREKT

```css
/* SKRIV ALLTID DETTA */
background: var(--color-accent);
padding: var(--space-md);
border-radius: var(--radius-sm);
color: var(--color-text-secondary);
background: var(--color-bg-page);
```

---

## MOBILDESIGN - EDGE-TO-EDGE STANDARD

**Alla innehallssektioner ska ga kant-till-kant pa mobil.**

Detta ar den globala standarden fran 2025. Pa mobil (max-width: 767px) ska alla kort, tabeller och innehallsblock fylla hela skarmbredden for att maximera datautrymme.

### Hur det fungerar

Reglerna finns i `assets/css/components.css` och tillampas automatiskt pa:
- `.card` - Alla kort
- `.filter-row` - Filterrader
- `.filters-bar` - Filterbarer
- `.table-responsive` - Tabeller
- `.table-wrapper` - Tabellwrappers
- `.result-list` - Resultatlistor
- `.event-row` - Eventrader
- `.alert` - Alerts/meddelanden

### CSS-tekniken

```css
@media(max-width:767px){
  .card,
  .filter-row,
  .table-responsive,
  .alert {
    margin-left: -16px;
    margin-right: -16px;
    border-radius: 0 !important;
    border-left: none !important;
    border-right: none !important;
    width: calc(100% + 32px);
  }
}
```

### VIKTIGT - container padding

Pa mobil anvander `.main-content` padding: `var(--space-md)` (16px).
Negativa marginaler maste matcha detta: `-16px`.

Pa extra smala skarmar (599px portrait) anvands `var(--space-sm)` (8px) istallet.

### Nar du skapar nya komponenter

Om du skapar nya innehallsblock som ska ga edge-to-edge pa mobil:

1. Lagg till klassen i components.css under mobil-regeln (max-width:767px)
2. ELLER anvand samma CSS-monster manuellt:

```css
@media(max-width:767px){
  .din-nya-komponent {
    margin-left: -16px;
    margin-right: -16px;
    border-radius: 0 !important;
    border-left: none !important;
    border-right: none !important;
    width: calc(100% + 32px);
  }
}
```

---

## SIDMALLAR

### Admin-sida (KOPIERA EXAKT)

```php
<?php
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../includes/auth.php';
requireAdmin();

$pageTitle = 'Sidtitel';
include __DIR__ . '/../includes/admin-header.php';
?>

<div class="admin-content">
    <div class="page-header">
        <h1><?= $pageTitle ?></h1>
    </div>

</div>

<?php include __DIR__ . '/../includes/admin-footer.php'; ?>
```

### Publik sida (KOPIERA EXAKT)

```php
<?php
require_once __DIR__ . '/config/database.php';

$pageTitle = 'Sidtitel';
include __DIR__ . '/includes/header.php';
?>

<main class="container">
    <!-- DITT INNEHÅLL HÄR -->
</main>

<?php include __DIR__ . '/includes/footer.php'; ?>
```

---

## 🧩 KOMPONENTER - KOPIERA, ÄNDRA INTE

### Kort (Card)

```html
<div class="card">
    <div class="card-header">
        <h3>Titel</h3>
    </div>
    <div class="card-body">
        Innehåll
    </div>
</div>
```

### Flikar (Tabs)

```html
<div class="tabs">
    <nav class="tabs-nav">
        <button class="tab-btn active" data-tab="tab1">Flik 1</button>
        <button class="tab-btn" data-tab="tab2">Flik 2</button>
    </nav>
    <div class="tab-content active" id="tab1">
        Innehåll 1
    </div>
    <div class="tab-content" id="tab2">
        Innehåll 2
    </div>
</div>
```

```js
// Tab-switching (lägg i footer eller separat JS)
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabId = btn.dataset.tab;
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(tabId).classList.add('active');
    });
});
```

### Knappar

```html
<button class="btn btn-primary">Primär</button>
<button class="btn btn-secondary">Sekundär</button>
<button class="btn btn-danger">Danger</button>
<button class="btn btn-ghost">Ghost</button>
```

### Formulär

```html
<div class="form-group">
    <label class="form-label">Etikett</label>
    <input type="text" class="form-input" placeholder="...">
</div>

<div class="form-group">
    <label class="form-label">Dropdown</label>
    <select class="form-select">
        <option>Val 1</option>
    </select>
</div>
```

### Tabell

```html
<div class="table-responsive">
    <table class="table">
        <thead>
            <tr>
                <th>Kolumn</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Data</td>
            </tr>
        </tbody>
    </table>
</div>
```

### Alerts

```html
<div class="alert alert-success">Meddelande</div>
<div class="alert alert-warning">Varning</div>
<div class="alert alert-danger">Fel</div>
```

### Badge

```html
<span class="badge badge-success">Aktiv</span>
<span class="badge badge-warning">Väntande</span>
<span class="badge badge-danger">Inaktiv</span>
```

---

## 📁 NY FIL - CHECKLISTA

När du skapar en ny sida:

1. ✅ Använd rätt sidmall (admin eller publik)
2. ✅ Inkludera INGA egna `<style>`-taggar
3. ✅ Använd befintliga komponenter
4. ✅ Använd CSS-variabler för ALLA värden
5. ✅ Testa på mobil (320px) och desktop

---

## 🚫 REGLER

1. **SKAPA ALDRIG ny CSS** utan att fråga först
2. **ÄNDRA ALDRIG** header, footer, eller sidebar
3. **ANVÄND ALLTID** befintliga komponenter
4. **HARDKODA ALDRIG** färger, spacing eller storlekar
5. **INKLUDERA ALLTID** rätt header/footer

---

## 💬 FRÅGA FÖRST

Om du behöver:
- En ny komponent → Fråga: "Ska jag lägga till X i components.css?"
- Ändra layout → Fråga: "Får jag ändra strukturen på X?"
- Ny styling → Fråga: "Behöver vi ny CSS för detta?"

---

## 🗄️ DATABAS - TABELLSCHEMA

**VIKTIGT:** Kolumnnamn är UTAN understreck!

### riders (deltagare)
```sql
id, firstname, lastname, birth_year, gender, nationality, active,
club_id,                    -- Koppling till clubs-tabellen
license_number,             -- UCI ID (t.ex. "10012345678") - DETTA ÄR UCI-NUMRET!
license_type,               -- Licenstyp (Elite, Junior, etc)
license_category,           -- Kön/kategori för licensen
license_year,               -- År licensen gäller till (avslutas 31 dec)
license_valid_until,        -- Datum licensen gäller till
discipline,                 -- Disciplin (MTB, Road, etc)
district,                   -- SCF-distrikt klubben tillhör
first_season, experience_level,
stats_total_starts, stats_total_finished, stats_total_wins, stats_total_podiums, stats_total_points,
created_at, updated_at
```

**VIKTIGT om license_number:**
- `license_number` innehåller UCI ID (11 siffror, t.ex. "10012345678")
- Svenska licenser börjar ofta med "SWE" prefix
- Detta är kolumnen som ska användas för SCF API-validering

### results (resultat)
```sql
id, event_id, cyclist_id, class_id, position,
finish_time, status, bib_number, points,
ss1, ss2, ss3, ..., ss15,  -- Split times
created_at
```

### events (tävlingar)
```sql
id, name, date, location, venue_id, series_id,
discipline, event_level, event_format, active,
is_championship, organizer_club_id,
stage_names, pricing_template_id
```

### clubs (klubbar)
```sql
id, name, city, country, active
```

### series (serier)
```sql
id, name, year, status, logo
```

### series_events (koppling event-serie) - VIKTIGT!
```sql
id, series_id, event_id, template_id
```

**VIKTIGT: Events kopplas till serier via `series_events`-tabellen (many-to-many), INTE via `events.series_id`!**

```php
// FEL - Missar events som är kopplade via series_events
JOIN series s ON e.series_id = s.id

// RÄTT - Använd series_events för att hitta ALLA events i en serie
JOIN series_events se ON se.event_id = e.id
JOIN series s ON se.series_id = s.id
```

**När ska du använda vad?**
- `LEFT JOIN series s ON e.series_id = s.id` - OK för att visa serienamn (optional)
- `JOIN series_events se ON ...` - KRÄV för analytics/aggregering per serie/brand
- Se `/analytics/includes/KPICalculator.php` för korrekt mönster

---

## PROJEKTSTRUKTUR

```
thehub/
├── index.php               # Huvudrouter (SPA-liknande)
├── hub-config.php          # Huvudkonfiguration
├── router.php              # URL-routing
├── config/
│   └── database.php
├── components/             # UI-komponenter
│   ├── sidebar.php         # LÅST - Navigation
│   ├── header.php          # LÅST - Header
│   ├── icons.php           # Lucide ikoner
│   └── mobile-nav.php
├── includes/
│   ├── layout-header.php   # LÅST - Layout wrapper
│   ├── layout-footer.php   # LÅST - Layout footer
│   ├── navigation.php      # Admin navigation
│   ├── auth.php
│   └── config/
│       └── admin-tabs-config.php  # Admin meny-konfiguration
├── assets/
│   └── css/
│       ├── tokens.css      # LÅST - Design tokens
│       ├── theme.css       # LÅST - Light/Dark mode
│       ├── components.css  # LÅST - UI-komponenter
│       ├── layout.css      # LÅST - Layout-system
│       ├── tables.css
│       └── utilities.css
├── pages/                  # Publika sidor
│   ├── calendar.php
│   ├── results.php
│   └── ...
├── admin/                  # Admin-sidor
│   ├── dashboard.php
│   ├── events.php
│   └── ...
└── api/                    # API-endpoints
```
