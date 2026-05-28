# TheHUB CSS-struktur och konflikter

## 🔴 KRITISKA PROBLEM

### 1. DUBBLERING AV CSS-SYSTEM
Det finns **MINST TRE olika CSS-arkitekturer** som kan skapa konflikter:

```
A) ASSETS CSS (AKTIVT SYSTEM) - Laddas i components/head.php
   /assets/css/
   ├── reset.css (15 rader, 1.0K)
   ├── tokens.css (48 rader, 2.0K) ← CSS-variabler
   ├── theme.css (121 rader, 4.0K) ← Dark/Light themes
   ├── layout.css (159 rader, 5.5K)
   ├── components.css (432 rader, 18K) ← Kärnan av komponenter
   ├── tables.css (84 rader, 5.0K)
   ├── utilities.css (58 rader, 5.5K)
   ├── badge-system.css (567 rader, 13K)
   └── pwa.css (345 rader, 8.0K)
   TOTALT: ~73K aktiv CSS

B) PUBLIC CSS (LEGACY SYSTEM?) - Möjligen ej aktivt laddat
   /public/css/
   ├── gravityseries-main.css (2627 rader, 52K) ⚠️ ENORM FIL
   ├── gravityseries-admin.css (1637 rader, 35K)
   ├── main.css (51 rader, 2.0K)
   └── Modular structure:
       ├── base/ (_reset.css, _typography.css, _variables.css)
       ├── components/ (_buttons.css, _cards.css, _forms.css, etc.)
       ├── layout/ (_containers.css, _flex.css, _grid.css)
       ├── pages/ (_admin.css, _hero.css, _results.css, etc.)
       ├── responsive/ (mobile, tablet, desktop breakpoints)
       └── utilities/ (_colors.css, _display.css, _spacing.css)
   TOTALT: ~87K legacy CSS

C) GRAVITYSERIES THEME
   /assets/gravityseries-theme.css (77K!) ⚠️ JÄTTESTOR FIL
   
D) ADMIN CSS
   /admin/assets/css/admin.css (46K)
```

### 2. SPECIFIKA KONFLIKTER

#### A. EDGE-TO-EDGE MOBIL PROBLEM
**Hittad i:** `assets/css/components.css` rad 56-102

```css
/* EDGE-TO-EDGE MOBILE STANDARD 2025 */
@media(max-width:767px){
  .card, .filter-row, .filters-bar, .table-responsive,
  .table-wrapper, .result-list, .event-row, .alert {
    margin-left:-16px;
    margin-right:-16px;
    border-radius:0!important;
    border-left:none!important;
    border-right:none!important;
    width:calc(100% + 32px);
  }
}
```

**PROBLEM:** 
- Använder `!important` överallt (kodlukt)
- Kan krocka med andra width-definitioner
- Fungerar INTE om parent container inte har rätt padding
- Kan vara anledningen till att result cards inte är full-width

#### B. CSS VARIABLER DUBBLERING
**tokens.css definierar:**
```css
:root {
  --space-md: 16px;
  --font-heading: 'Oswald', sans-serif;
  --color-accent: #3B9EFF; /* Dark mode default */
}
```

**MEN gravityseries-theme.css och public/css kan ha ANDRA värden!**

#### C. BRANDING.JSON KONFLIKT
**Branding-systemet** (`admin/branding.php`) försöker spara custom färger till:
- `/uploads/branding.json`
- Dessa laddas INTE automatiskt i CSS
- Series-specifika färger finns i DB men appliceras inte konsekvent

```php
// branding.php sparar till JSON
$customColors['--color-accent'] = '#FF0000';
saveBranding($brandingFile, $branding);

// MEN dessa laddas ALDRIG in i <head>!
```

#### D. TEMA-SWITCHING KONFLIKT
**theme.css har:**
```css
:root, html[data-theme="dark"] {
  --color-accent: #3B9EFF;
}
html[data-theme="light"] {
  --color-accent: #004A98;
}
```

**MEN branding.json kan ha andra värden som INTE respekteras!**

## 🟡 CSS LADDNINGSORDNING

**Nuvarande ordning i components/head.php:**
1. **reset.css** - Nollställer browser defaults
2. **tokens.css** - CSS-variabler (spacing, fonts, colors)
3. **theme.css** - Dark/Light mode färger
4. **layout.css** - Grid, containers, spacing
5. **components.css** - Buttons, cards, header, etc.
6. **tables.css** - Table styling
7. **utilities.css** - Helper classes
8. **badge-system.css** - Achievement badges
9. **pwa.css** - Progressive Web App styles

**PROBLEM:** Ingen av de stora legacy-filerna laddas här!

## 🟢 BRANDING-SYSTEMETS STRUKTUR

### Var färger definieras:

1. **tokens.css** - Statiska defaults
   ```css
   --color-accent: #3B9EFF;
   ```

2. **theme.css** - Dark/Light overrides
   ```css
   html[data-theme="light"] {
     --color-accent: #004A98;
   }
   ```

3. **Database** - Series-specifika färger
   ```sql
   series.gradient_start
   series.gradient_end  
   series.accent_color
   ```

4. **branding.json** - Admin custom overrides (ej implementerat i frontend!)
   ```json
   {
     "colors": {
       "--color-accent": "#custom-color"
     }
   }
   ```

**KONFLIKT:** Alla 4 system kan ha olika värden!

## 📊 CSS-FILER STORLEK OCH STATUS

| Fil | Storlek | Rader | Status | Laddas? |
|-----|---------|-------|--------|---------|
| assets/css/components.css | 18K | 432 | ✅ Aktiv | Ja |
| assets/css/badge-system.css | 13K | 567 | ✅ Aktiv | Ja |
| assets/css/pwa.css | 8.0K | 345 | ✅ Aktiv | Ja |
| **gravityseries-theme.css** | **77K** | **?** | ⚠️ Legacy? | **NEJ?** |
| **gravityseries-main.css** | **52K** | **2627** | ⚠️ Legacy? | **NEJ?** |
| **gravityseries-admin.css** | **35K** | **1637** | ⚠️ Legacy? | **NEJ?** |
| admin/assets/css/admin.css | 46K | ? | ✅ Admin | I admin |

**TOTALT OUTNYTTJAD CSS:** ~210K (!!)

## 🔧 REKOMMENDERADE FIXES

### FIX 1: TA BORT LEGACY CSS
```bash
# Backup först!
mkdir /backup-css-$(date +%Y%m%d)
mv public/css/gravityseries-*.css /backup-css-*/
mv assets/gravityseries-theme.css /backup-css-*/
```

### FIX 2: IMPLEMENTERA BRANDING.JSON I FRONTEND
**Lägg till i components/head.php:**

```php
<?php
// Load custom branding
$brandingFile = __DIR__ . '/../uploads/branding.json';
$customColors = '';
if (file_exists($brandingFile)) {
    $branding = json_decode(file_get_contents($brandingFile), true);
    if (!empty($branding['colors'])) {
        $customColors = '<style>:root{';
        foreach ($branding['colors'] as $var => $value) {
            $customColors .= $var . ':' . $value . ';';
        }
        $customColors .= '}</style>';
    }
}
echo $customColors;
?>
```

### FIX 3: FIXA EDGE-TO-EDGE MOBIL (2025 Standard)

**I tokens.css, lägg till mobile-first padding:**
```css
:root {
  --container-padding: 16px;  /* Base för alla mobiler */
}

@media (min-width: 768px) {
  :root { --container-padding: 24px; }  /* Tablet */
}

@media (min-width: 1024px) {
  :root { --container-padding: 32px; }  /* Desktop */
}
```

**I components.css, ersätt edge-to-edge med:**
```css
/* MOBILE EDGE-TO-EDGE - 2025 Mobile-first */
@media (max-width: 767px) {
  .container {
    padding-left: var(--container-padding);
    padding-right: var(--container-padding);
  }

  /* Cards break out to full width */
  .card,
  .result-list > *,
  .event-row {
    margin-left: calc(-1 * var(--container-padding));
    margin-right: calc(-1 * var(--container-padding));
    border-radius: 0;
    border-left: none;
    border-right: none;
    width: auto;
    max-width: none;
  }

  /* Restore padding inside */
  .card-header,
  .card-body {
    padding-left: var(--container-padding);
    padding-right: var(--container-padding);
  }
}
```

**OBS: Ingen 8px-variant behövs!**
- Moderna mobiler (360-430px) fungerar utmärkt med 16px
- Apple HIG och Material Design 3 rekommenderar 16px
- 16px ger 92% content area på 360px telefon

### FIX 4: KONSOLIDERA CSS-VARIABLER
**Skapa ny fil:** `assets/css/custom-properties.css`

```css
/* Custom properties från branding.json laddas här dynamiskt */
:root {
  /* Dessa kan overridas av branding-systemet */
}
```

### FIX 5: SERIES COLORS
**Applicera series colors inline i PHP:**

```php
<div class="series-card" 
     style="--series-gradient-start: <?= $series['gradient_start'] ?>; 
            --series-gradient-end: <?= $series['gradient_end'] ?>;">
```

## 🎯 ACTION PLAN

### STEG 1: AUDIT & CLEANUP (1-2h)
- [ ] Bekräfta att gravityseries-*.css INTE laddas
- [ ] Backup och ta bort legacy CSS
- [ ] Testa att sidan funkar utan dem

### STEG 2: BRANDING INTEGRATION (2-3h)  
- [ ] Implementera branding.json loader i head.php
- [ ] Testa custom colors i admin/branding.php
- [ ] Verifiera att ändringar sparas OCH appliceras

### STEG 3: MOBILE FIX (1-2h)
- [ ] Fixa edge-to-edge CSS för result cards
- [ ] Testa på olika mobila enheter
- [ ] Ta bort onödiga !important

### STEG 4: DOCUMENTATION (1h)
- [ ] Dokumentera CSS-arkitekturen
- [ ] Skapa style guide för nya komponenter
- [ ] Lista alla CSS custom properties

## 📱 MOBIL-SPECIFIKA PROBLEM

### Result Cards inte full-width
**Möjliga orsaker:**
1. Container har inte rätt padding (16px på mobil)
2. calc(100% + 32px) blir fel om parent inte är rätt storlek
3. Någon annan CSS regel overstyrer med högre specificitet
4. max-width sätts någonstans och begränsar
5. Box-sizing är inte border-box

**Debug:**
```css
/* Lägg till temporärt för att se vad som händer */
.result-list > * {
  outline: 2px solid red !important;
}
.container {
  outline: 2px solid blue !important;
}
```

## 🔍 UPPTÄCKTA CSS-PATTERNS

### POSITIVA:
- ✅ Använder CSS custom properties konsekvent
- ✅ Mobile-first approach i media queries
- ✅ Modulär struktur i /assets/css/
- ✅ Bra namnkonvention (BEM-liknande)

### NEGATIVA:
- ❌ För mycket !important (code smell)
- ❌ Dubblerad CSS i flera system
- ❌ Legacy filer som kanske inte används
- ❌ Branding-system ej integrerat i frontend
- ❌ Ingen central dokumentation

## 📋 NÄSTA STEG

1. **VERIFIERA:** Kolla vilka CSS-filer som faktiskt laddas i browser DevTools
2. **CLEANUP:** Ta bort legacy CSS efter backup
3. **FIX:** Implementera branding.json loader
4. **TEST:** Fixa mobile edge-to-edge
5. **DOCUMENT:** Skapa CSS style guide

---

**Skapad:** 2024-12-14
**Version:** 1.0
**Status:** 🔴 Kritiska problem identifierade
