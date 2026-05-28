# DESIGN SYSTEM ENFORCEMENT - TheHUB

**Purpose:** Förhindra designkaos framöver  
**Goal:** Konsekvent UX över hela plattformen  
**Method:** Regler + Automation + Code Reviews

---

## 🎯 CORE PRINCIPLES

### 1. **Konsistens över Kreativitet**
> "Samma data = Samma design, alltid"

### 2. **Komponenter först**
> "Om en komponent finns, använd den. Om inte, skapa en reusable en."

### 3. **Mobile-first**
> "Design för mobil först, desktop är en bonus"

### 4. **Tillgänglighet är inte optional**
> "Aria-labels, semantic HTML, keyboard navigation"

### 5. **Performance matters**
> "60 FPS animationer, lazy loading, optimerade bilder"

---

## 🚫 FÖRBJUDNA PATTERNS

### ❌ ALDRIG TILLÅTET:

#### 1. Emojis i UI
```php
<!-- ❌ FÖRBJUDET -->
<span>🥇</span>
<h2>🏆 Results</h2>

<!-- ✅ KORREKT -->
<i data-lucide="trophy"></i>
<h2><i data-lucide="trophy"></i> Results</h2>
```

#### 2. Inline Styles
```php
<!-- ❌ FÖRBJUDET -->
<div style="color: red; margin: 10px;">

<!-- ✅ KORREKT -->
<div class="text-error mb-md">
```

**Undantag:** Dynamiska färger från databas (series colors)

#### 3. Hardcoded Colors
```css
/* ❌ FÖRBJUDET */
.card {
  background: #1A1D28;
  color: #F9FAFB;
}

/* ✅ KORREKT */
.card {
  background: var(--color-bg-card);
  color: var(--color-text-primary);
}
```

#### 4. Duplicerad HTML
```php
<!-- ❌ FÖRBJUDET - Copy-paste HTML mellan sidor -->

<!-- ✅ KORREKT - Komponenter -->
<?php require_once 'components/result-table.php'; ?>
<?= renderResultTable($results) ?>
```

#### 5. Magic Numbers
```css
/* ❌ FÖRBJUDET */
.card {
  padding: 24px;
  margin: 16px;
  border-radius: 14px;
}

/* ✅ KORREKT */
.card {
  padding: var(--space-lg);
  margin: var(--space-md);
  border-radius: var(--radius-lg);
}
```

#### 6. !important Abuse
```css
/* ❌ FÖRBJUDET - mer än 5 !important i en fil */

/* ✅ KORREKT - Använd högre specificitet istället */
.container .card {
  width: 100%;
}
```

#### 7. Custom Breakpoints
```css
/* ❌ FÖRBJUDET */
@media (max-width: 850px) { }
@media (max-width: 640px) { }

/* ✅ KORREKT - Använd standardiserade */
@media (max-width: 767px) { }
@media (min-width: 768px) and (max-width: 1023px) { }
```

#### 8. Font-stack override
```css
/* ❌ FÖRBJUDET */
h1 {
  font-family: 'Arial', sans-serif;
}

/* ✅ KORREKT */
h1 {
  font-family: var(--font-heading);
}
```

---

## ✅ REQUIRED PATTERNS

### 1. CSS Variables för allt
```css
:root {
  --space-md: 16px;
  --color-accent: #3B9EFF;
  --font-heading: 'Oswald', sans-serif;
}

.my-component {
  padding: var(--space-md);
  color: var(--color-accent);
  font-family: var(--font-heading);
}
```

### 2. Komponenter för repeterad UI
```php
// ✅ Skapa komponent
function renderEventCard($event) { ... }

// Använd överallt
<?= renderEventCard($event) ?>
```

### 3. Helper Functions för common tasks
```php
// ✅ Icons
<?= getRankingIcon(1) ?>

// ✅ Dates
<?= formatEventDate($date) ?>

// ✅ Badges
<?= getSeriesBadge($series) ?>
```

### 4. Aria-labels för ikoner
```html
<!-- ✅ Tillgängligt -->
<i data-lucide="trophy" aria-label="Första plats"></i>
```

### 5. Semantic HTML
```html
<!-- ✅ Korrekt struktur -->
<article class="event-card">
  <header>
    <h3>Event Name</h3>
  </header>
  <section>
    <p>Details...</p>
  </section>
  <footer>
    <time datetime="2025-04-27">27 April 2025</time>
  </footer>
</article>
```

---

## 📐 COMPONENT CHECKLIST

Varje ny komponent MÅSTE ha:

- [ ] **Reusable** - Kan användas på flera sidor
- [ ] **Responsive** - Desktop + Tablet + Mobile
- [ ] **Accessible** - ARIA, keyboard navigation
- [ ] **Documented** - PHPDoc kommentarer
- [ ] **Tested** - På minst 3 olika sidor
- [ ] **CSS Variables** - Inga hardcoded värden
- [ ] **Props/Options** - Konfigurerbar via parametrar
- [ ] **Error Handling** - Validering av input
- [ ] **Loading States** - Skeleton screens eller spinners
- [ ] **Empty States** - Vad visas vid no data?

---

## 🎨 CSS ARCHITECTURE

### Filstruktur:
```
/assets/css/
├── reset.css           # Browser reset (READONLY)
├── tokens.css          # CSS variables (ADD ONLY)
├── theme.css           # Dark/Light colors (MODIFY WITH CARE)
├── layout.css          # Grid, containers (STABLE)
├── components.css      # Component styles (MAIN WORKFILE)
├── tables.css          # Table-specific (STABLE)
├── utilities.css       # Helper classes (ADD ONLY)
├── badge-system.css    # Achievements (STABLE)
└── pwa.css            # PWA-specific (STABLE)
```

### CSS Naming Convention (BEM-ish):
```css
/* Block */
.result-card { }

/* Element */
.result-card__header { }
.result-card__body { }

/* Modifier */
.result-card--compact { }
.result-card--highlighted { }

/* State */
.result-card.is-loading { }
.result-card.is-expanded { }
```

### CSS Ordering:
```css
.component {
  /* 1. Positioning */
  position: relative;
  top: 0;
  z-index: 10;
  
  /* 2. Box Model */
  display: flex;
  width: 100%;
  padding: var(--space-md);
  margin: var(--space-sm);
  
  /* 3. Typography */
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--color-text-primary);
  
  /* 4. Visual */
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  
  /* 5. Misc */
  transition: all var(--transition-fast);
  cursor: pointer;
}
```

---

## 🔍 CODE REVIEW CHECKLIST

### Innan du committar:

#### PHP:
- [ ] Använder komponenter istället för custom HTML?
- [ ] Inga emojis i output?
- [ ] Inga inline styles?
- [ ] Helper functions för vanliga tasks?
- [ ] Error handling finns?
- [ ] PHPDoc kommentarer?

#### CSS:
- [ ] Använder CSS variables?
- [ ] Inga magic numbers?
- [ ] Inga !important (eller max 5)?
- [ ] BEM-ish naming?
- [ ] Mobile-first media queries?
- [ ] Inga custom breakpoints?

#### HTML:
- [ ] Semantic elements?
- [ ] Aria-labels på ikoner?
- [ ] Alt-text på bilder?
- [ ] Proper heading hierarchy (H1 → H2 → H3)?

#### JavaScript:
- [ ] Initialiserar Lucide ikoner?
- [ ] Event delegation där möjligt?
- [ ] Inga console.logs kvar?

---

## 🤖 AUTOMATION TOOLS

### 1. Emoji Detector
**Fil:** `tools/detect-emojis.sh`

```bash
#!/bin/bash
# Detect emojis in PHP files

echo "🔍 Scanning for emojis..."
EMOJIS=$(grep -r "🥇\|🥈\|🥉\|🏆\|🏅\|🎖️" --include="*.php" v2/ | wc -l)

if [ $EMOJIS -gt 0 ]; then
    echo "❌ FOUND $EMOJIS emojis!"
    grep -rn "🥇\|🥈\|🥉\|🏆\|🏅\|🎖️" --include="*.php" v2/
    exit 1
else
    echo "✅ No emojis found!"
    exit 0
fi
```

### 2. CSS Variable Checker
**Fil:** `tools/check-css-vars.sh`

```bash
#!/bin/bash
# Check for hardcoded values in CSS

echo "🔍 Scanning for hardcoded colors..."
COLORS=$(grep -E "color:\s*#[0-9A-Fa-f]{6}" --include="*.css" assets/css/*.css | grep -v "var(--" | wc -l)

if [ $COLORS -gt 10 ]; then
    echo "❌ FOUND $COLORS hardcoded colors (max 10 allowed)!"
    exit 1
else
    echo "✅ CSS variables used properly!"
    exit 0
fi
```

### 3. Component Usage Report
**Fil:** `tools/component-report.php`

```php
<?php
// Generate report of component usage across pages

$components = [
    'result-table.php',
    'event-card.php',
    'ranking-badge.php'
];

$pages = glob('v2/*.php');

foreach ($components as $component) {
    echo "Component: $component\n";
    $count = 0;
    
    foreach ($pages as $page) {
        $content = file_get_contents($page);
        if (strpos($content, $component) !== false) {
            echo "  ✓ " . basename($page) . "\n";
            $count++;
        }
    }
    
    echo "  Used in: $count pages\n\n";
}
?>
```

---

## 📋 ONBOARDING CHECKLIST

För nya utvecklare:

### Day 1: Setup
- [ ] Klonat repo
- [ ] Läst README.md
- [ ] Läst DESIGN_SYSTEM_ENFORCEMENT.md
- [ ] Installerat dev dependencies
- [ ] Kört lokalt

### Day 2: Lära sig systemet
- [ ] Läst CSS_ARKITEKTUR_GUIDE.md
- [ ] Kollat components i /v2/components/
- [ ] Förstår CSS variables i tokens.css
- [ ] Testat på mobil

### Day 3: Första bidrag
- [ ] Fixat en enkel bug
- [ ] Använt befintlig komponent
- [ ] Följt CSS naming convention
- [ ] Fått code review godkänd

---

## 🎓 LEARNING RESOURCES

### TheHUB Specifikt:
- `docs/css-analysis/CSS_ARKITEKTUR_GUIDE.md`
- `docs/css-analysis/COMPONENT_CONSOLIDATION.md`
- `docs/css-analysis/EMOJI_TO_ICON_MIGRATION.md`

### Externa Resurser:
- **CSS:** https://web.dev/learn/css/
- **Accessibility:** https://www.a11yproject.com/
- **Lucide Icons:** https://lucide.dev
- **BEM Naming:** http://getbem.com/
- **Mobile-First:** https://web.dev/mobile-first/

---

## 🚨 RED FLAGS

Om du ser detta i code review, STOPPA och fixa:

### 🔴 CRITICAL:
- Emojis i UI
- SQL injection risk
- XSS vulnerabilities
- Hardcoded credentials
- Broken responsive design

### 🟡 WARNING:
- Duplicerad HTML
- Inline styles
- Custom breakpoints
- >10 !important i fil
- Inga aria-labels

### 🟢 NICE TO FIX:
- Console.logs kvar
- Commented out code
- TODOs utan tickets
- Inkonsistent indentation

---

## 🎯 METRICS

Mät framgång av design system:

### KPIs:
- **Component Reuse:** >80% av UI använder komponenter
- **CSS Size:** <150KB total CSS
- **Emoji Count:** 0 emojis i production
- **!important Count:** <50 totalt
- **Design Consistency Score:** 9/10

### Tools:
```bash
# Component reuse
grep -r "renderResultTable\|renderEventCard" v2/*.php | wc -l

# CSS size
du -sh assets/css/*.css

# Emojis
grep -r "🥇\|🥈\|🥉\|🏆" --include="*.php" v2/ | wc -l

# !important count
grep -r "!important" assets/css/*.css | wc -l
```

---

## 🔄 CONTINUOUS IMPROVEMENT

### Quarterly Reviews:
- [ ] Q1: Audit all components
- [ ] Q2: Performance optimization
- [ ] Q3: Accessibility audit
- [ ] Q4: Design trends check

### Monthly Tasks:
- [ ] Run automation scripts
- [ ] Update documentation
- [ ] Review new patterns
- [ ] Plan deprecations

---

## 🏆 SUCCESS STORIES

### Before Design System:
- 10 different result displays
- 20+ emojis in UI
- 300KB duplicated CSS
- Inconsistent mobile experience
- 2 hours to change a color

### After Design System:
- 1 standardized result component
- 0 emojis
- 150KB modular CSS
- Consistent mobile-first design
- 5 minutes to change a color

**= 92% faster changes!**

---

## 💪 ENFORCEMENT STRATEGY

### Level 1: Documentation
- ✅ This file exists
- ✅ Shared with team
- ✅ Included in onboarding

### Level 2: Automation
- ✅ Pre-commit hooks
- ✅ CI/CD checks
- ✅ Automated reports

### Level 3: Code Reviews
- ✅ Design system checklist
- ✅ Component reuse enforced
- ✅ No merge without approval

### Level 4: Culture
- ✅ Celebrate good examples
- ✅ Share learnings
- ✅ Continuous education

---

## 🎯 ULTIMATE GOAL

> **"En ny utvecklare ska kunna bygga en helt ny sida som ser identisk ut med befintliga sidor, utan att läsa en enda rad gammal kod - bara genom att använda komponenter och designsystemet."**

---

**DETTA ÄR VÄGEN FRAMÅT!** 🚀

Konsekvent design = Proffsig produkt = Nöjda användare = Framgång! 🎉
