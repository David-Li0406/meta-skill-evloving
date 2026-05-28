# 🚀 QUICK START - För Claude Code

**Detta är din 5-minuters guide för att starta uppdraget.**

---

## ⚡ SNABBSTART (5 MIN)

### 1. LÄS DESSA FILER FÖRST (2 min)
```
/CLAUDE.md                                    # Utvecklingsregler
/docs/DESIGN-SYSTEM-2025.md                   # Design guidelines
/docs/css-analysis/CSS_ARKITEKTUR_GUIDE.md    # CSS struktur
```

### 2. LÄS DEN FULLSTÄNDIGA PROMTEN (2 min)
```
CLAUDE_CODE_ULTIMATE_PROMPT.md                # Komplett mission brief
```

### 3. VÄLJ APPROACH (1 min)

**OPTION A: Override CSS (REKOMMENDERAD)**
- Skapa `/admin/assets/css/admin-color-fix.css`
- Kopiera CSS från `THEHUB_CORRECT_CSS_FIX.css`
- Inkludera sist i admin pages
- ✅ Safest, snabbast, lättast att reversa

**OPTION B: Edit Source Files**
- Editera `/assets/css/theme.css`
- Editera `/admin/assets/css/admin.css`
- ✅ Mer permanent, renare solution

---

## 🎯 DIT UPPDRAG I 3 STEG

### STEG 1: Fix Accent Color
**Fil:** `/assets/css/theme.css`

Ändra ALLA instanser av:
- `#37d4d6` → `#0066CC`
- `#2bc4c6` → `#0066CC`
- `rgba(55, 212, 214, ...)` → `rgba(0, 102, 204, ...)`

### STEG 2: Fix Stat Cards
**Fil:** `/admin/assets/css/admin.css`

Ändra gradient definitions:
- `--admin-gradient-primary` → `transparent`
- `--admin-gradient-success` → `transparent`
- etc.

Remove colored backgrounds från `.admin-stat-card` variants.

### STEG 3: Fix Icon Sizes
**Fil:** `/admin/assets/css/admin.css`

Ändra icon sizes:
- `48px` → `40px` (container)
- SVG icons → `24px`

---

## ✅ VERIFIERING (2 MIN)

Efter ändringarna, öppna:
1. `/admin/dashboard.php` - Kolla stat cards
2. `/admin/series.php` - Kolla series cards
3. Toggle light/dark mode - Fungerar i både?

**Success = Allt är blue (#0066CC), INGET cyan!**

---

## 📁 FILER DU BEHÖVER

```
CRITICAL FILES:
├── CLAUDE_CODE_ULTIMATE_PROMPT.md     ← LÄSÖBLIGATORISK - Main mission brief
├── THEHUB_CORRECT_CSS_FIX.css         ← CSS fix (för Option A)
├── THEHUB_CSS_PROBLEM_ANALYSIS.md     ← Detaljerad problemanalys
└── QUICK_START.md                     ← Denna fil

SOURCE FILES TO MODIFY:
├── /assets/css/theme.css              ← Accent colors
└── /admin/assets/css/admin.css        ← Stat cards, icons

REFERENCE FILES (läs dessa):
├── /CLAUDE.md                         ← Workflow rules
├── /docs/DESIGN-SYSTEM-2025.md        ← Design system
└── /docs/css-analysis/
    └── CSS_ARKITEKTUR_GUIDE.md        ← CSS structure
```

---

## 🎨 FÄRGER ATT KOMMA IHÅG

```
FEL (Nuvarande):     RÄTT (Ska vara):
#37d4d6 (Cyan)  →    #0066CC (Blue)
#2bc4c6 (Cyan)  →    #0066CC (Blue)
```

**Kom ihåg:** ONE blue to rule them all! 💙

---

## 🚨 VARNINGSSIGNALER

Om du ser NÅGON av dessa EFTER din fix, något är fel:

- [ ] Cyan color (#37d4d6) ANYWHERE
- [ ] Färgade gradient backgrounds på stat cards
- [ ] Ikoner större än 24px
- [ ] Borders i cyan-färg
- [ ] Links i cyan istället för blue

---

## 💡 PRO TIPS

1. **Använd DevTools** - Ctrl+Shift+I → Computed styles
2. **Clear cache** - Ctrl+Shift+R mellan tester
3. **Test båda modes** - Light OCH dark
4. **!important når nödvändigt** - Men bara i override-fil
5. **Git commit tidigt** - Commit innan större ändringar

---

## 🆘 PROBLEM? KOLLA DETTA

### "Färger ändras inte!"
→ Clear cache (Ctrl+Shift+R)
→ Kolla CSS laddningsordning (DevTools → Network)
→ Verifiera CSS-variabel: `getComputedStyle(document.documentElement).getPropertyValue('--color-accent')`

### "Stat cards fortfarande färgade!"
→ Kolla om gradients är removed
→ Verifiera background med DevTools
→ Säkerställ override CSS laddas sist

### "Fungerar i dark men inte light!"
→ Kolla att DU ändrat BÅDA mode-definitionerna
→ Verifiera `html[data-theme="light"]` section

---

## ⏱️ TIDSPLAN

```
00:00 - 00:02  Läs obligatoriska filer
00:02 - 00:04  Läs full prompt
00:04 - 00:05  Välj approach
00:05 - 00:15  Implementera fixes
00:15 - 00:20  Testa och verifiera
00:20 - 00:25  Git commit och push
```

**Total tid: 25 minuter** för komplett fix.

---

## 🎯 LYCKAS-DEFINITION

✅ Accent color är #0066CC överallt  
✅ Stat cards är vita med subtle shadows  
✅ Ikoner är små (24px) och blue  
✅ Inga gradient backgrounds  
✅ Fungerar i light och dark mode  
✅ Matchar originalbilden EXAKT  

---

**Nu har du allt du behöver. LÄS SEDAN → IMPLEMENTERA → VERIFIERA → PUSHA! 🚀**
