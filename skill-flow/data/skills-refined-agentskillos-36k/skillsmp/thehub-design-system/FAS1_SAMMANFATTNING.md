# FAS 1: KARTLÄGGNING - SAMMANFATTNING
*Datum: 2026-01-17*

## 📊 TOTALT ANTAL CSS-FILER: **58 filer** (inte 39 som estimerat!)

### Filfördelning:
- **Core CSS:** 11 filer (3,328 rader totalt)
- **Page-specific:** 37 filer i assets/css/pages/
- **Extra CSS:** 8 filer (achievements, badge-system, map, etc.)
- **Admin CSS:** 2 filer (4,320 rader totalt!)

---

## 🔴 KRITISKA FYND

### 1. ENORMA FILER (Kräver konsolidering)
```
admin.css                  3,807 rader  91KB  ← KRITISK!
rider.css                  2,700 rader  57KB
database-rider.css         2,700 rader  512B  ← SUSPEKT! (samma radantal, minimal storlek)
club.css                   1,668 rader  36KB
database-club.css          1,668 rader  512B  ← SUSPEKT! (samma radantal, minimal storlek)
calendar-event.css         1,358 rader  512B  ← SUSPEKT!
event.css                  1,358 rader  30KB
compatibility.css          1,212 rader  28KB  ← Bör granskas!
achievements.css           1,118 rader  24KB
```

**ANALYS:** Många page-specific filer har 512 bytes storlek trots höga radantal - troligen symboliska länkar eller duplikatmarkörer!

### 2. DUPLICERADE SELEKTORER: **110 stycken**
Exempel på duplicerade selektorer som finns i flera filer:
- `.btn`, `.btn--primary`, `.btn--secondary` (core components)
- `.card`, `.card-header`, `.card-title`
- `.alert`, `.alert--success`, `.alert--error`
- `.flex`, `.grid`, `.container`
- Alla utility classes (`.mt-lg`, `.mb-md`, etc.)

**ÅTGÄRD:** Dessa bör ENDAST finnas i en fil (components.css eller utilities.css)

### 3. HARDKODADE FÄRGER: **150 unika färger**
Top 10 mest använda:
```
26× #61CE70   (grön - bör vara --color-success)
19× #ef4444   (röd - bör vara --color-error)
19× #e5e7eb   (grå border)
14× #ffffff   (vit - bör vara --color-bg-surface i light mode)
14× #9ca3af   (grå text)
12× #FFD700   (guld - medalj färg)
10× #fff      (vit variant)
10× #f3f4f6   (ljusgrå bakgrund)
10× #22c55e   (grön variant)
```

**ÅTGÄRD:** Definiera dessa i tokens.css eller theme.css

### 4. CSS-VARIABLER ANALYS
```
Använda variabler:      154
Definierade i tokens:    27
Definierade i theme:     46
SAKNAS/OKLAR KÄLLA:      81 ← PROBLEM!
```

**81 variabler** används men är INTE definierade i tokens.css eller theme.css!
Dessa finns troligen i:
- achievements.css
- badge-system.css
- admin.css
- Inline i andra filer

**ÅTGÄRD:** Alla variabler måste centraliseras till tokens.css eller theme.css

### 5. INLINE CSS: **23 rader** (bättre än väntat!)
Finns i `includes/layout-header.php` rad 131-153:
- FOUC prevention (opacity fade-in)
- Fallback animation

**ÅTGÄRD:** Flytta till ny fil `critical-inline.css`

### 6. CSS LADDNINGSORDNING
```
1. Google Fonts
2. reset.css
3. tokens.css
4. theme.css
5. layout.css
6. components.css
7. tables.css
8. utilities.css
9. grid.css
10. pwa.css
11. compatibility.css
12. sponsors-blog.css
```

**PROBLEM:** Page-specific CSS laddas INTE automatiskt!

---

## 🎯 IDENTIFIERADE ÖVERLAPPNINGAR

### A. Layout-system dubletter
```
layout.css (297 rader)   → Grundläggande layout
grid.css (233 rader)     → Grid system
responsive.css (333 rader) → Media queries
```
**→ Kan troligen slås ihop till en fil: `layout.css`**

### B. Tema-dubletter
```
theme.css (243 rader)         → Dark/Light mode variabler
theme-base.css (949 rader)    → ??? (behöver granskas)
```
**→ Undersök om theme-base.css är gammal/legacy**

### C. Page-specific dubletter
```
calendar.css         504 rader  512B
calendar-index.css   504 rader  11KB   ← Använd denna!
calendar-event.css  1358 rader  512B

database.css         403 rader  8.5KB  ← Använd denna!
database-index.css   403 rader  512B
database-club.css   1668 rader  512B
database-rider.css  2700 rader  512B

results.css          590 rader  512B
results-index.css    590 rader  12KB   ← Använd denna!
results-event.css   1358 rader  512B

profile.css          957 rader  23KB   ← Använd denna!
profile-index.css    957 rader  512B
profile-edit.css     957 rader  512B
profile-children.css 957 rader  512B
... (8 profile-*.css filer med 512B)
```

**ANALYS:** 512-byte filer är troligen tomma/minimal CSS. Behåll endast de stora filerna!

---

## 📋 REKOMMENDERADE ÅTGÄRDER

### Prioritet 1: Rensa page-specific CSS
```bash
# Ta bort 512-byte filer (troligen tomma)
find assets/css/pages/ -size 512c -name "*.css"
# Resultat: 20+ filer att granska/radera
```

### Prioritet 2: Konsolidera page-specific CSS
Slå ihop till moduler:
```
pages/auth.css          → login, register, forgot-password, reset-password, activate
pages/profile.css       → ALLA profile-* sidor
pages/calendar.css      → calendar-index, calendar-event
pages/database.css      → database-index, database-club, database-rider
pages/ranking.css       → ranking-index, ranking-clubs, ranking-riders
pages/results.css       → results-index, results-event
pages/series.css        → series-index, series-show
```

**Från 37 filer → 10-12 filer**

### Prioritet 3: Slå ihop core CSS
```
layout.css + grid.css + responsive.css → layout.css
theme.css + theme-base.css → theme.css (ta reda på vad theme-base gör först)
```

### Prioritet 4: Flytta variabler
- Extrahera alla CSS-variabler från achievements.css, badge-system.css, admin.css
- Flytta till tokens.css eller theme.css
- Ersätt hardkodade färger med variabler

### Prioritet 5: Admin CSS
```
admin.css (3807 rader, 91KB) är ENORM!
→ Dela upp i moduler eller optimera
```

---

## ⏱️ UPPDATERAD TIDSESTIMAT

| Fas | Aktivitet | Tid |
|-----|-----------|-----|
| 1 | Kartläggning | ✅ KLAR |
| 2 | Backup | 15 min |
| 3 | Extrahera inline CSS | 30 min |
| 4 | Konsolidera core CSS | 3-4 timmar (mer än estimerat) |
| 5 | Page-specific CSS | 2-3 timmar (mer arbete än estimerat) |
| **TOTALT** | | **6-8 timmar** |

---

## 📦 SKAPADE FILER

- `CSS_AUDIT.txt` - Detaljerad analys av varje CSS-fil
- `CSS_FILE_SIZES.txt` - Filstorlekar och radantal
- `DUPLICATED_SELECTORS.txt` - 110 duplicerade selektorer
- `HARDCODED_COLORS.txt` - 150 hardkodade färger
- `CSS_VARIABLES_AUDIT.txt` - Variabel-användning vs definition
- `INLINE_CSS_AUDIT.txt` - Inline CSS analys
- `CSS_LOADING_ORDER.txt` - CSS laddningsordning
- `FAS1_SAMMANFATTNING.md` - Denna fil

---

## ✅ NÄSTA STEG

**Rekommendation:** Börja med FAS 2 (Backup) följt av FAS 3 (Extrahera inline CSS) som quick win.

Alternativt: Börja direkt med att ta bort 512-byte filer för omedelbar impact.

