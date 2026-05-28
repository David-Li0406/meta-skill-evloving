# TheHUB CSS ARKITEKTUR - VISUELL GUIDE

## 📐 CSS LADDNINGSORDNING (CASCADE)

```
┌─────────────────────────────────────────────────────────────┐
│  components/head.php - MASTER CSS LOADER                    │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
        ▼                                       ▼
┌───────────────┐                     ┌───────────────┐
│  1. reset.css │                     │ Google Fonts  │
│  (15 lines)   │                     │  - Oswald     │
└───────┬───────┘                     │  - Cabin      │
        │                             │  - Manrope    │
        ▼                             │  - Roboto     │
┌───────────────┐                     └───────────────┘
│ 2. tokens.css │ ← CSS VARIABLES (spacing, fonts, radii)
│  (48 lines)   │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ 3. theme.css  │ ← COLORS (dark/light mode)
│  (121 lines)  │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ 4. layout.css │ ← GRID, CONTAINERS, SPACING
│  (159 lines)  │
└───────┬───────┘
        │
        ▼
┌────────────────┐
│5. components   │ ← BUTTONS, CARDS, HEADER, FORMS
│   .css         │   ⚠️ HAR EDGE-TO-EDGE PROBLEM!
│  (432 lines)   │
└────────┬───────┘
         │
         ▼
┌────────────────┐
│ 6. tables.css  │ ← TABLE STYLING
│  (84 lines)    │
└────────┬───────┘
         │
         ▼
┌────────────────┐
│7. utilities    │ ← HELPER CLASSES (.text-center, .mt-lg)
│   .css         │
│  (58 lines)    │
└────────┬───────┘
         │
         ▼
┌────────────────┐
│8. badge-system │ ← ACHIEVEMENT BADGES
│   .css         │
│  (567 lines)   │
└────────┬───────┘
         │
         ▼
┌────────────────┐
│  9. pwa.css    │ ← PROGRESSIVE WEB APP
│  (345 lines)   │
└────────┬───────┘
         │
         ▼
┌────────────────┐
│  BRANDING.JSON │ ← ⚠️ LADDAS INTE JUST NU!
│  (admin colors)│   FIX: Lägg till loader i head.php
└────────────────┘
```

## 🎨 CSS VARIABLER SYSTEM

```
┌─────────────────────────────────────────────────────────┐
│  :root (tokens.css)                                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  SPACING:                                               │
│  --space-2xs: 4px                                       │
│  --space-xs:  8px                                       │
│  --space-sm:  12px                                      │
│  --space-md:  16px   ← Standard padding                 │
│  --space-lg:  24px   ← Card padding                     │
│  --space-xl:  32px                                      │
│  --space-2xl: 48px                                      │
│  --space-3xl: 64px                                      │
│                                                         │
│  FONTS:                                                 │
│  --font-heading:    'Oswald'          (H1)              │
│  --font-heading-secondary: 'Cabin'    (H2-H3)           │
│  --font-body:       'Manrope'         (body, p)         │
│  --font-link:       'Roboto'          (a)               │
│  --font-mono:       'SF Mono'         (code)            │
│                                                         │
│  RADIUS:                                                │
│  --radius-sm:   6px                                     │
│  --radius-md:   10px                                    │
│  --radius-lg:   14px  ← Cards                           │
│  --radius-xl:   20px                                    │
│  --radius-full: 9999px                                  │
│                                                         │
│  DIMENSIONS:                                            │
│  --sidebar-width:     72px                              │
│  --header-height:     60px                              │
│  --mobile-nav-height: 64px                              │
│  --content-max-width: 1400px                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  html[data-theme="dark"] (DEFAULT)  - theme.css         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  BACKGROUNDS:                                           │
│  --color-bg-page:    #0A0C14  (body)                    │
│  --color-bg-surface: #12141C  (header, footer)          │
│  --color-bg-card:    #1A1D28  (cards)                   │
│  --color-bg-sunken:  #06080E  (inset areas)             │
│                                                         │
│  TEXT:                                                  │
│  --color-text-primary:   #F9FAFB  (headings, main)      │
│  --color-text-secondary: #D1D5DB  (descriptions)        │
│  --color-text-tertiary:  #9CA3AF  (labels)              │
│  --color-text-muted:     #6B7280  (hints)               │
│                                                         │
│  ACCENT:                                                │
│  --color-accent:       #3B9EFF  (buttons, links)        │
│  --color-accent-hover: #60B0FF  (hover state)           │
│                                                         │
│  STATUS:                                                │
│  --color-success: #10B981  (green)                      │
│  --color-warning: #FBBF24  (yellow)                     │
│  --color-error:   #EF4444  (red)                        │
│  --color-info:    #38BDF8  (blue)                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  html[data-theme="light"] - theme.css                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  BACKGROUNDS:                                           │
│  --color-bg-page:    #F4F5F7                            │
│  --color-bg-surface: #FFFFFF                            │
│  --color-bg-card:    #FFFFFF                            │
│  --color-bg-sunken:  #E9EBEE                            │
│                                                         │
│  TEXT:                                                  │
│  --color-text-primary:   #171717                        │
│  --color-text-secondary: #4B5563                        │
│                                                         │
│  ACCENT:                                                │
│  --color-accent:       #004A98  (darker blue)           │
│  --color-accent-hover: #003B7C                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  branding.json (CUSTOM ADMIN OVERRIDES)                 │
│  ⚠️ FUNGERAR EJ ÄNNU - BEHÖVER LOADER!                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  {                                                      │
│    "colors": {                                          │
│      "--color-accent": "#CUSTOM_COLOR",                 │
│      "--color-bg-card": "#CUSTOM_BG"                    │
│    }                                                    │
│  }                                                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 📱 RESPONSIVE BREAKPOINTS (MODERNA 2025)

```
┌──────────────┬──────────────┬──────────────┐
│  0-767px     │  768-1023px  │  1024px+     │
│  Mobile      │  Tablet      │  Desktop     │
│  (360-430px) │              │              │
├──────────────┼──────────────┼──────────────┤
│              │              │              │
│ 16px padding │ 24px padding │ 32px padding │
│              │              │              │
│  Cards       │ Cards with   │ Full layout  │
│  edge-to-    │ rounded      │ with sidebar │
│  edge        │ corners      │              │
│              │              │              │
│  1 column    │ 2 columns    │ 3+ columns   │
│              │              │              │
│  Bottom nav  │ Top nav      │ Top nav +    │
│              │ visible      │ sidebar      │
│              │              │              │
└──────────────┴──────────────┴──────────────┘

VARFÖR 16PX PÅ MOBIL?
- Moderna mobiler: iPhone 15 Pro (393px), S24 (360px), Pixel 8 (412px)
- Apple HIG 2025: 16-20px margins
- Material Design 3: 16px standard
- 16px ger 92% content area - perfekt balans!
- 8px var för trångt för 2020-talet (från 320px iPhone 5-eran)
```

## 🔧 MOBILE EDGE-TO-EDGE SYSTEM

```
DESKTOP (1024px+):
┌──────────────────────────────────────────────────────────────┐
│ CONTAINER (max-width: 1400px, padding: 32px)                 │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ CARD (border-radius: 14px, margin: normal)             │  │
│  │                                                        │  │
│  │  Content här                                           │  │
│  │                                                        │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘

MOBILE (0-767px):
┌──────────────────────────────────────────────────────────────┐
│ CONTAINER (padding: 16px)                                    │
┌┴────────────────────────────────────────────────────────────┴┐
│  CARD (margin: -16px, border-radius: 0)                      │
│                                                              │
│  Content här (padding-left/right: 16px restored)             │
│                                                              │
└──────────────────────────────────────────────────────────────┘

PRINCIPLE:
1. Container has 16px padding
2. Cards use margin: -16px to break out
3. Cards restore 16px padding inside
4. Result: Card edges touch screen edges!
```

## 🎯 COMPONENT CSS PATTERNS

### CARD ANATOMY
```css
.card {
  /* Structure */
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);     /* 14px */
  padding: var(--space-lg);             /* 24px */
  
  /* Effects */
  box-shadow: var(--shadow-sm);
  
  /* Responsive */
  max-width: 100%;
  overflow: hidden;
}

/* Mobile override */
@media (max-width: 767px) {
  .card {
    margin-left: calc(-1 * var(--container-padding));   /* -16px */
    margin-right: calc(-1 * var(--container-padding));  /* -16px */
    border-radius: 0;
    border-left: none;
    border-right: none;
  }
}
```

### BUTTON ANATOMY
```css
.btn {
  /* Base styles */
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);                /* 8px */
  padding: var(--space-sm) var(--space-md);  /* 12px 16px */
  
  /* Typography */
  font-family: var(--font-link);       /* Roboto */
  font-weight: var(--weight-medium);   /* 500 */
  font-size: var(--text-base);         /* 0.875rem */
  
  /* Colors */
  background: var(--color-accent);     /* #3B9EFF dark, #004A98 light */
  color: var(--color-text-inverse);
  
  /* Border & Radius */
  border: none;
  border-radius: var(--radius-md);     /* 10px */
  
  /* Effects */
  transition: all var(--transition-fast);  /* 150ms */
  cursor: pointer;
}

.btn:hover {
  background: var(--color-accent-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}
```

## 🚫 ANTI-PATTERNS (UNDVIK!)

### ❌ DÅLIGT: Hardcoded värden
```css
.card {
  padding: 24px;           /* BAD */
  border-radius: 14px;     /* BAD */
  color: #F9FAFB;          /* BAD */
}
```

### ✅ BRA: CSS-variabler
```css
.card {
  padding: var(--space-lg);
  border-radius: var(--radius-lg);
  color: var(--color-text-primary);
}
```

### ❌ DÅLIGT: !important överallt
```css
.card {
  width: 100% !important;
  margin: 0 !important;
}
```

### ✅ BRA: Högre specificitet
```css
.container .card,
.page-content .card {
  width: 100%;
  margin: 0;
}
```

### ❌ DÅLIGT: Fixed breakpoints överallt
```css
@media (max-width: 768px) { }
@media (max-width: 767px) { }
@media (max-width: 640px) { }
@media (max-width: 480px) { }
```

### ✅ BRA: Konsistenta breakpoints
```css
@media (max-width: 599px) and (orientation: portrait) { }
@media (max-width: 767px) { }
@media (min-width: 768px) and (max-width: 1023px) { }
@media (min-width: 1024px) { }
```

## 🗂️ FILSTRUKTUR

```
/assets/css/
├── reset.css          - Browser normalization
├── tokens.css         - CSS variables (spacing, fonts, radii)
├── theme.css          - Colors (dark/light mode)
├── layout.css         - Grid, containers, spacing
├── components.css     - Reusable components (buttons, cards, etc.)
├── tables.css         - Table-specific styles
├── utilities.css      - Helper classes
├── badge-system.css   - Achievement badges
├── pwa.css           - PWA-specific styles
├── grid.css          - Grid system (loaded in layout-header)
├── compatibility.css - Browser compatibility (loaded in layout-header)
├── responsive.css    - Additional responsive (not always loaded)
├── map.css          - Leaflet map overrides
├── achievements.css - Achievement system
└── theme-base.css   - Theme base (alternative?)

/public/css/           ← LEGACY! Ska tas bort?
├── gravityseries-main.css (52K) ⚠️ OANVÄND
├── gravityseries-admin.css (35K) ⚠️ OANVÄND
└── [modular structure]

/admin/assets/css/
└── admin.css         - Admin panel specific
```

## 📖 HUR MAN LÄGGER TILL NYA STYLES

### 1. Kolla om det finns en CSS-variabel
```css
/* INTE detta */
.my-card {
  padding: 16px;
}

/* UTAN detta */
.my-card {
  padding: var(--space-md);
}
```

### 2. Lägg nya komponenter i components.css
```css
/* MY NEW COMPONENT */
.my-component {
  background: var(--color-bg-card);
  padding: var(--space-lg);
  border-radius: var(--radius-lg);
}
```

### 3. Responsiva styles med mobile-first
```css
/* Base (mobile) */
.my-component {
  font-size: var(--text-base);
}

/* Desktop */
@media (min-width: 1024px) {
  .my-component {
    font-size: var(--text-lg);
  }
}
```

### 4. Använd utilities för snabba fixes
```css
/* components.css */
.mt-lg { margin-top: var(--space-lg); }
.p-md { padding: var(--space-md); }
.text-center { text-align: center; }
```

## 🎨 BRANDING WORKFLOW

```
┌──────────────────┐
│  Admin Panel     │
│  /admin/branding │
│  .php            │
└────────┬─────────┘
         │
         ▼ (sparar)
┌──────────────────┐
│ branding.json    │
│ /uploads/        │
└────────┬─────────┘
         │
         ▼ (laddas av)
┌──────────────────┐
│ branding-loader  │
│ i head.php       │
│ (NYA KODEN!)     │
└────────┬─────────┘
         │
         ▼ (applicerar)
┌──────────────────┐
│ :root CSS vars   │
│ overrides        │
└──────────────────┘
```

## 🔍 DEBUG CHECKLIST

När CSS inte fungerar:

- [ ] Öppna DevTools → Elements
- [ ] Kolla Computed styles
- [ ] Leta efter överstrukna properties (= overstyrt)
- [ ] Kolla vilka CSS-filer som faktiskt laddas (Network tab)
- [ ] Verifiera CSS-variabelvärden med getComputedStyle
- [ ] Använd `outline` istället för `border` för debug (påverkar inte layout)
- [ ] Kolla console för CSS-errors
- [ ] Verifiera mobile med DevTools device emulation

```javascript
// I console:
const root = document.documentElement;
const accent = getComputedStyle(root).getPropertyValue('--color-accent');
console.log('Accent color:', accent);
```

---

**NÄSTA STEG:**
1. Implementera branding-loader i head.php
2. Fixa edge-to-edge mobile CSS
3. Ta bort legacy CSS-filer
4. Konsolidera breakpoints
5. Dokumentera alla CSS-variabler
