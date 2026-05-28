# TheHUB CSS Branding System Reference

> **CLAUDE: LAS DETTA DOKUMENT INNAN DU ANDRAR NAGOT CSS ELLER STYLING**

Detta dokument beskriver TheHUBs kompletta CSS-branding-system. Alla variabler, breakpoints och layout-tokens definieras har.

---

## 1. SYSTEMARKITEKTUR

### Filstruktur

```
assets/css/
├── tokens.css        # Design tokens (spacing, radius, typography) - MASTER SOURCE
├── theme.css         # Farger (dark/light themes)
├── layout.css        # Layout-system (containers, sidebar, grids)
├── components.css    # UI-komponenter (kort, knappar, etc.)
├── tables.css        # Tabellstyling
└── responsive.css    # Responsiva overrides

uploads/
└── branding.json     # Anpassade variabler fran admin/branding.php

components/
└── head.php          # Injicerar branding.json som CSS-variabler
```

### Laddningsordning

1. `reset.css` - HTML-reset
2. `tokens.css` - Design tokens (MASTE VARA FORST)
3. `theme.css` - Tema-farger
4. `layout.css` - Layout
5. `components.css` - Komponenter
6. `tables.css` - Tabeller
7. **`<style id="custom-branding">`** - Dynamisk override fran branding.json

---

## 2. SPACING-TOKENS (Obligatoriska)

Anvand **ALLTID** dessa variabler for spacing. Hardkoda aldrig pixelvarden.

| Token | Varde | Anvandning |
|-------|-------|------------|
| `--space-2xs` | 4px | Minimal separation |
| `--space-xs` | 8px | Tight spacing |
| `--space-sm` | 12px | Small gaps |
| `--space-md` | 16px | Standard padding/margin |
| `--space-lg` | 24px | Section spacing |
| `--space-xl` | 32px | Large sections |
| `--space-2xl` | 48px | Hero areas |
| `--space-3xl` | 64px | Page sections |

### Exempel

```css
/* RATT */
padding: var(--space-md);
gap: var(--space-sm);
margin-bottom: var(--space-lg);

/* FEL - Hardkoda aldrig */
padding: 16px;
gap: 12px;
margin-bottom: 24px;
```

---

## 3. LAYOUT-TOKENS (Branding-kontrollerade)

Dessa tokens kan andras via admin/branding.php:

### Container & Content

| Token | Desktop | Tablet | Mobil | Beskrivning |
|-------|---------|--------|-------|-------------|
| `--container-padding` | 32px | 24px | 12px | Huvudinnehall sidopadding |
| `--card-padding` | 24px | 16px | 8px | Kortens inre padding |
| `--content-padding` | 24px | 16px | 8px | Generell innehallspadding |
| `--content-max-width` | 1400px | 1400px | 100% | Max bredd pa huvudinnehall |

### Tabell-padding

| Token | Desktop | Tablet | Mobil | Beskrivning |
|-------|---------|--------|-------|-------------|
| `--table-cell-padding-y` | 12px | 10px | 8px | Vertikal cell-padding |
| `--table-cell-padding-x` | 16px | 14px | 12px | Horisontell cell-padding |

### Layout-dimensioner

| Token | Varde | Beskrivning |
|-------|-------|-------------|
| `--sidebar-width` | 72px | Sidopanelens bredd |
| `--header-height` | 60px | Headerns hojd |
| `--mobile-nav-height` | 64px | Mobil-navens hojd |

---

## 4. RADIUS-TOKENS (Branding-kontrollerade)

Radius styrs per breakpoint via branding:

| Token | Desktop | Tablet | Mobil | Anvandning |
|-------|---------|--------|-------|------------|
| `--radius-sm` | 12px | 8px | 0px | Sma element (badges, inputs) |
| `--radius-md` | 12px | 8px | 0px | Medel (kort, buttons) |
| `--radius-lg` | 12px | 8px | 0px | Stora (modals, sections) |
| `--radius-xl` | 12px | 8px | 0px | Extra stora (hero-sektioner) |
| `--radius-full` | 9999px | 9999px | 9999px | Cirkulara element |

**Obs:** Pa mobil ar standard-radius 0px for edge-to-edge design.

---

## 5. FARG-TOKENS (Tema-baserade)

Alla farger definieras i `theme.css` med dark/light varianter.

### Bakgrunder

| Token | Dark | Light | Anvandning |
|-------|------|-------|------------|
| `--color-bg-page` | #0A0C14 | #F4F5F7 | Sidbakgrund |
| `--color-bg-surface` | #12141C | #FFFFFF | Ytor (kort, modals) |
| `--color-bg-card` | #1A1D28 | #FFFFFF | Kortbakgrund |
| `--color-bg-sunken` | #06080E | #E9EBEE | Nedsankta ytor |
| `--color-bg-hover` | rgba | rgba | Hover-states |

### Text

| Token | Dark | Light | Anvandning |
|-------|------|-------|------------|
| `--color-text-primary` | #F9FAFB | #171717 | Primar text |
| `--color-text-secondary` | #D1D5DB | #4B5563 | Sekundar text |
| `--color-text-tertiary` | #9CA3AF | #6B7280 | Tertiar text |
| `--color-text-muted` | #6B7280 | #9CA3AF | Dampad text |
| `--color-text-inverse` | #171717 | #FFFFFF | Inverterad text |

### Accent & Knappar

| Token | Dark | Light | Anvandning |
|-------|------|-------|------------|
| `--color-accent` | #3B9EFF | #004A98 | Primar accent |
| `--color-accent-hover` | #60B0FF | #003B7C | Accent hover |
| `--color-accent-text` | #3B9EFF | #004A98 | Accentfargad text |
| `--color-accent-light` | rgba(59,158,255,0.15) | #E8F0FB | Ljus accent-bakgrund |

### Status

| Token | Dark | Light | Anvandning |
|-------|------|-------|------------|
| `--color-success` | #10B981 | #059669 | Framgang |
| `--color-warning` | #FBBF24 | #D97706 | Varning |
| `--color-error` | #EF4444 | #DC2626 | Fel |
| `--color-info` | #38BDF8 | #0284C7 | Information |

### Kanter

| Token | Dark | Light | Anvandning |
|-------|------|-------|------------|
| `--color-border` | #2D3139 | #E5E7EB | Standard kant |
| `--color-border-strong` | #3F444D | #D1D5DB | Stark kant |

### Serie-specifika farger

| Token | Varde | Serie |
|-------|-------|-------|
| `--series-enduro` | #FFE009 | Swedish Enduro Series |
| `--series-downhill` | #FF6B35 | Downhill |
| `--series-xc` | #2E7D32 | XC |
| `--series-ges` | #EF761F | GES |
| `--series-ggs` | #8A9A5B | GGS |
| `--series-gss` | #6B4C9A | GSS |
| `--series-gravel` | #795548 | Gravel |
| `--series-dual` | #E91E63 | Dual Slalom |

---

## 6. TYPOGRAFI-TOKENS

### Font-familjer

| Token | Varde | Anvandning |
|-------|-------|------------|
| `--font-heading` | 'Oswald' | H1 rubriker |
| `--font-heading-secondary` | 'Cabin Condensed' | H2-H6 rubriker |
| `--font-body` | 'Manrope' | Brodtext |
| `--font-link` | 'Roboto' | Lankar |
| `--font-mono` | 'SF Mono', Monaco | Kod |

### Font-storlekar

| Token | Desktop | Mobil | Anvandning |
|-------|---------|-------|------------|
| `--text-xs` | 0.75rem | 0.75rem | Sma etiketter |
| `--text-sm` | 0.8125rem | 0.8125rem | Sekundar text |
| `--text-base` | 0.875rem | 0.875rem | Standard |
| `--text-md` | 1rem | 1rem | Brodtext |
| `--text-lg` | 1.125rem | 1.125rem | Stor text |
| `--text-xl` | 1.25rem | 1.125rem | Underrubriker |
| `--text-2xl` | 1.5rem | 1.25rem | Sektionsrubriker |
| `--text-3xl` | 2rem | 1.5rem | Sidrubriker |
| `--text-4xl` | 2.5rem | 2rem | Hero-rubriker |

### Font-vikter

| Token | Varde |
|-------|-------|
| `--weight-light` | 300 |
| `--weight-normal` | 400 |
| `--weight-medium` | 500 |
| `--weight-semibold` | 600 |
| `--weight-bold` | 700 |

---

## 7. RESPONSIVA BREAKPOINTS

### Breakpoint-definitioner

| Namn | Range | Beskrivning |
|------|-------|-------------|
| **Mobile Portrait** | 0-599px | Smal mobil (portrait) |
| **Mobile Landscape** | 600-767px | Mobil (landscape) |
| **Tablet** | 768-1023px | Surfplatta |
| **Desktop** | 1024px+ | Desktop och storre |

### CSS Media Queries

```css
/* Mobil (portrait) */
@media (max-width: 599px) and (orientation: portrait) { }

/* Mobil (alla) */
@media (max-width: 767px) { }

/* Tablet */
@media (min-width: 768px) and (max-width: 1023px) { }

/* Desktop */
@media (min-width: 1024px) { }

/* Stora skarmar */
@media (min-width: 1400px) { }
```

---

## 8. EDGE-TO-EDGE MOBIL-STANDARD (2025)

Pa mobil (max-width: 767px) ska innehallssektioner ga kant-till-kant:

### Komponenter som ar edge-to-edge

- `.card`
- `.filter-row`
- `.filters-bar`
- `.table-responsive`
- `.table-wrapper`
- `.result-list`
- `.event-row`
- `.alert`

### CSS-tekniken

```css
@media (max-width: 767px) {
  .card,
  .table-responsive {
    margin-left: calc(-1 * var(--container-padding));
    margin-right: calc(-1 * var(--container-padding));
    border-radius: 0 !important;
    border-left: none !important;
    border-right: none !important;
    width: calc(100% + (var(--container-padding) * 2));
  }
}
```

---

## 9. BRANDING.JSON STRUKTUR

Filen `/uploads/branding.json` lagrar anpassningar:

```json
{
  "colors": {
    "--color-bg-page": "#custom",
    "--color-accent": "#custom"
  },
  "responsive": {
    "mobile_portrait": {
      "padding": "12",
      "radius": "0"
    },
    "tablet": {
      "padding": "24",
      "radius": "8"
    },
    "desktop": {
      "padding": "32",
      "radius": "12"
    }
  },
  "layout": {
    "content_max_width": "1400",
    "sidebar_width": "72"
  }
}
```

---

## 10. SASS-LIKNANDE REGLER FOR CLAUDE

### FORBJUDET - Hardkodade varden

```css
/* ALDRIG SA HAR */
padding: 16px;
margin: 24px;
border-radius: 8px;
color: #61CE70;
background: #171717;
font-size: 14px;
```

### OBLIGATORISKT - Anvand tokens

```css
/* ALLTID SA HAR */
padding: var(--space-md);
margin: var(--space-lg);
border-radius: var(--radius-md);
color: var(--color-accent);
background: var(--color-bg-primary);
font-size: var(--text-base);
```

### UNDANTAG

Hardkodade varden ar tillatet ENDAST for:

1. **0-varden**: `margin: 0`, `padding: 0`
2. **Procent**: `width: 100%`, `height: 50%`
3. **Calc med variabler**: `calc(100% - var(--space-md))`
4. **Transitions**: `transition: 0.2s ease`
5. **SVG-specifika**: `stroke-width: 2`

---

## 11. KOMPONENT-SPECIFIKA TOKENS

### Knappar

| Token | Anvandning |
|-------|------------|
| `--btn-padding-x` | Horisontell padding |
| `--btn-padding-y` | Vertikal padding |
| `--btn-font-size` | Textstorlek |
| `--btn-radius` | Border-radius |

### Formularelement

| Token | Anvandning |
|-------|------------|
| `--input-padding-x` | Input horisontell padding |
| `--input-padding-y` | Input vertikal padding |
| `--input-radius` | Input border-radius |
| `--input-border-width` | Kantbredd |

### Kort

| Token | Anvandning |
|-------|------------|
| `--card-padding` | Inre padding |
| `--card-radius` | Border-radius (fran --radius-md) |
| `--card-border-width` | Kantbredd |
| `--card-shadow` | Box-shadow |

---

## 12. CHECKLISTA FOR KODANDRINGAR

Innan du andrar CSS, kontrollera:

- [ ] Anvander jag CSS-variabler for ALLA varden?
- [ ] Ar spacing fran `--space-*` skalan?
- [ ] Ar farger fran `--color-*` tokens?
- [ ] Ar radius fran `--radius-*` tokens?
- [ ] Fungerar det pa alla breakpoints?
- [ ] Foljer det edge-to-edge standarden pa mobil?
- [ ] Har jag testat i dark mode?

---

## 13. ADMINPANEL

**URL:** `/admin/branding.php`

Har kan du andra:

1. **Farger** - Alla `--color-*` variabler
2. **Responsiv layout** - Padding och radius per breakpoint
3. **Serie-farger** - Gradient och accent per serie

Andringar sparas i `/uploads/branding.json` och appliceras direkt via `head.php`.

---

## 14. SNABBREFERENS

### Vanliga kombinationer

```css
/* Standard kort */
.card {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--card-padding);
}

/* Standard knapp */
.btn {
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-sm);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
}

/* Standard container */
.main-content {
  padding: var(--container-padding);
  max-width: var(--content-max-width);
  margin: 0 auto;
}

/* Standard text */
.text-body {
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--color-text-primary);
}
```

---

## 15. VIEWPORT-SYSTEM (Dynamiska hojder)

Viewport-systemet laster av skarmens upplösning och sätter CSS-variabler i realtid.

### CSS-filer
- `assets/css/viewport.css` - Tokens och utility-klasser
- `assets/js/viewport.js` - JavaScript som uppdaterar variablerna

### Viewport-variabler

| Token | Beskrivning |
|-------|-------------|
| `--vh` | 1% av faktisk viewport-hojd (i px) |
| `--vw` | 1% av faktisk viewport-bredd (i px) |
| `--vh-100` | 100% av viewport-hojd |
| `--vh-50` | 50% av viewport-hojd |
| `--content-height` | Viewport minus header |

### Kart-specifika variabler

| Token | Mobil | Tablet | Desktop |
|-------|-------|--------|---------|
| `--map-height-mobile` | 60vh | - | - |
| `--map-height-tablet` | - | 65vh | - |
| `--map-height-desktop` | - | - | 70vh |
| `--map-min-height` | 400px | 400px | 400px |
| `--map-max-height` | 800px | 800px | 800px |

### Anvandning i CSS

```css
/* Karta som anpassar sig till viewport */
#map {
    height: var(--map-height-desktop);
    min-height: var(--map-min-height);
    max-height: var(--map-max-height);
}

/* Fullskarm minus header */
.fullscreen-content {
    height: var(--content-height);
}

/* Anpassad procent */
.half-screen {
    height: var(--vh-50);
}
```

### Utility-klasser

```html
<!-- Fasta viewport-hojder -->
<div class="h-vh-100">100% viewport</div>
<div class="h-vh-50">50% viewport</div>

<!-- Kartor -->
<div class="map-viewport">Standard karta</div>
<div class="map-viewport--fill">Karta som fyller allt</div>
<div class="map-viewport--16x9">16:9 aspect ratio</div>
```

### JavaScript API

```javascript
// Hamta aktuell viewport-storlek
TheHUB.viewport.height  // Hojd i px
TheHUB.viewport.width   // Bredd i px
TheHUB.viewport.getVh(50)  // 50vh i px

// Lyssna pa andringar
TheHUB.viewport.onChange(function(data) {
    console.log('Viewport andrad:', data.height, data.width);
});

// Satt elements hojd dynamiskt
TheHUB.viewport.setElementHeight('#map', 70, {
    min: 400,
    max: 800,
    offset: 60  // Minus header
});
```

### Data-attribut

```html
<!-- Element far 70vh hojd automatiskt -->
<div data-vh-height="70">Karta</div>

<!-- Med min/max -->
<div data-vh-height="70" data-vh-min-height="40" data-vh-max-height="80">
    Karta med begransningar
</div>
```

---

## 16. SID-SPECIFIK CSS (Page CSS)

Sid-specifik CSS laddas villkorligt fran `assets/css/pages/` baserat pa vilken sida som visas.

### Hur det fungerar

1. CSS-filer namnges efter sidan: `event.css`, `rider.css`, `results.css`
2. `components/head.php` laddar automatiskt ratt fil baserat pa `$pageInfo['page']`
3. Om filen inte finns, laddas ingen extra CSS

### Filstruktur

```
assets/css/pages/
├── _README.md      # Dokumentation
├── event.css       # /pages/event.php
├── rider.css       # /pages/rider.php
├── results.css     # /pages/results.php
├── ranking.css     # /pages/ranking.php
└── calendar.css    # /pages/calendar/*
```

### Migrationsprocess (inline -> extern)

1. **Kopiera** inline `<style>` fran PHP-filen till CSS-filen
2. **Testa** att sidan ser likadan ut
3. **Kommentera ut** inline CSS i PHP (behall som backup)
4. **Testa igen**
5. **Ta bort** kommenterad CSS nar allt fungerar

### Exempel: Migrera event.php

```bash
# 1. Skapa CSS-filen
touch assets/css/pages/event.css

# 2. Kopiera innehallet fran <style> i pages/event.php till event.css

# 3. Kommentera ut i event.php:
# <?php /* MIGRATED TO assets/css/pages/event.css
# <style>
# ...
# </style>
# */ ?>

# 4. Testa - om OK, ta bort kommenterad kod
```

### Laddningsordning

Page-CSS laddas **efter** alla globala CSS-filer men **fore** branding-overrides:

1. reset.css
2. tokens.css
3. theme.css
4. layout.css
5. components.css
6. tables.css
7. utilities.css
8. badge-system.css
9. pwa.css
10. viewport.css
11. **pages/{page}.css** <- Sid-specifik
12. custom-branding (inline) <- Branding overrides

---

**Version:** 1.2.0
**Senast uppdaterad:** 2025-12-14
