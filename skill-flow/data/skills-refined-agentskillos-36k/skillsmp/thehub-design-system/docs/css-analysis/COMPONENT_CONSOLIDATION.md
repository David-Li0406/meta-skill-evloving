# COMPONENT CONSOLIDATION - TheHUB

**Problem:** Samma data visas med 4+ olika designs  
**Lösning:** EN standardiserad komponent-struktur  
**Impact:** 10+ filer, bättre UX, lättare underhåll

---

## 🚨 PROBLEMET

Från dina skärmbilder ser vi att **SAMMA DATA** (tävlingsresultat) visas på 4+ helt olika sätt:

### Variant 1: "Herrar Elit" (Desktop Table)
- Stor tabell med alla sträcktider
- Grön highlighting
- Medalj-ikoner
- Horisontell scroll

### Variant 2: "Pojkar 13-14" (Sidebar Layout)
- Sidebar navigation
- Mindre tabell
- Annan färgpalett
- Kompakt design

### Variant 3: "Motion Kids" (Lista med Checkmarks)
- Vertikal lista
- Checkmarks istället för positioner
- Minimal information
- Olika spacing

### Variant 4: "Series Standings" (Emoji Hell)
- 🥇🥈🥉 Emojis!
- Annan badge-style
- Inkonsistent färgschema

**DETTA ÄR DESIGNKAOS!** 😱

---

## 🎯 MÅL: EN STANDARDISERAD DESIGN

### Golden Rule:
> **"Samma data = Samma design, oavsett sida"**

### Principer:
1. **EN resultat-tabell komponent** som används överallt
2. **EN event-kort komponent** som används överallt
3. **EN färgpalett** för placeringar (guld/silver/brons)
4. **EN typografi** för alla resultat
5. **Responsiv** - fungerar desktop OCH mobile

---

## 📋 NUVARANDE KOMPONENTER (KAOS)

```
RESULTAT-VISNINGAR:
├── v2/results.php              (gs-result-card, gs-result-logo)
├── v2/series-standings.php     (olika table design)
├── v2/profile.php              (profile results table)
├── v2/ranking/index.php        (ranking table)
├── v2/club.php                 (club results)
├── pages-old/results.php       (legacy design)
└── pages-old/event.php         (legacy event view)

EVENT-VISNINGAR:
├── v2/events.php               (event-card-horizontal)
├── v2/profile.php              (event list)
├── pages-old/events.php        (legacy cards)
└── pages-old/home.php          (homepage events)
```

**= 10+ filer med OLIKA designs för SAMMA data!**

---

## ✅ NY STRUKTUR: REUSABLE COMPONENTS

```
/v2/components/
├── result-table.php        # Standard resultat-tabell
├── result-card.php         # Mobile resultat-kort
├── event-card.php          # Event card (horizontal/vertical)
├── ranking-badge.php       # Placering-badge (1, 2, 3...)
├── series-badge.php        # Serie-badge
└── discipline-badge.php    # Disciplin-badge
```

---

## 🏗️ KOMPONENT #1: RESULT TABLE

**Fil:** `v2/components/result-table.php`

### Features:
- Responsiv (desktop = table, mobile = cards)
- Konsistent färgschema
- Sortable columns
- Expandable sträcktider

### Props:
```php
$results = [
    [
        'position' => 1,
        'rider_name' => 'Oliver Kangas',
        'club' => 'BAUHAUS Sportklubb',
        'total_time' => '12:30.47',
        'stage_times' => ['1:24.36', '1:32.40', ...],
        'difference' => null // First place
    ],
    ...
];

$options = [
    'show_stages' => true,      // Visa sträcktider?
    'show_club' => true,        // Visa klubb?
    'show_difference' => true,  // Visa diff till topp?
    'highlight_podium' => true, // Highlighta top 3?
    'mobile_compact' => true    // Kompakt mobile view?
];
```

### Kod:

```php
<?php
/**
 * Standard Result Table Component
 * Used for all result displays across TheHUB
 * 
 * @param array $results Array of result objects
 * @param array $options Display options
 */

function renderResultTable($results, $options = []) {
    // Default options
    $defaults = [
        'show_stages' => true,
        'show_club' => true,
        'show_difference' => true,
        'highlight_podium' => true,
        'mobile_compact' => true,
        'class' => ''
    ];
    
    $opts = array_merge($defaults, $options);
    
    // Include icon helpers
    require_once __DIR__ . '/../includes/icon-helpers.php';
    ?>
    
    <div class="result-table-wrapper <?= $opts['class'] ?>">
        <!-- DESKTOP: Standard Table -->
        <table class="result-table hide-mobile">
            <thead>
                <tr>
                    <th class="col-position">#</th>
                    <th class="col-rider">Åkare</th>
                    <?php if ($opts['show_club']): ?>
                    <th class="col-club">Klubb</th>
                    <?php endif; ?>
                    <th class="col-time">Tid</th>
                    <?php if ($opts['show_difference']): ?>
                    <th class="col-diff">+Tid</th>
                    <?php endif; ?>
                    <?php if ($opts['show_stages']): ?>
                    <?php foreach ($results[0]['stage_times'] as $i => $time): ?>
                    <th class="col-stage">SS<?= $i+1 ?></th>
                    <?php endforeach; ?>
                    <?php endif; ?>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($results as $result): ?>
                <?php 
                $podiumClass = '';
                if ($opts['highlight_podium'] && $result['position'] <= 3) {
                    $podiumClass = 'podium-' . $result['position'];
                }
                ?>
                <tr class="result-row <?= $podiumClass ?>">
                    <td class="col-position">
                        <?php if ($result['position'] <= 3): ?>
                            <?= getRankingIcon($result['position']) ?>
                        <?php endif; ?>
                        <?= $result['position'] ?>
                    </td>
                    <td class="col-rider">
                        <strong><?= h($result['rider_name']) ?></strong>
                    </td>
                    <?php if ($opts['show_club']): ?>
                    <td class="col-club"><?= h($result['club']) ?></td>
                    <?php endif; ?>
                    <td class="col-time">
                        <strong><?= $result['total_time'] ?></strong>
                    </td>
                    <?php if ($opts['show_difference']): ?>
                    <td class="col-diff text-muted">
                        <?= $result['difference'] ? '+' . $result['difference'] : '-' ?>
                    </td>
                    <?php endif; ?>
                    <?php if ($opts['show_stages']): ?>
                    <?php foreach ($result['stage_times'] as $time): ?>
                    <td class="col-stage"><?= $time ?></td>
                    <?php endforeach; ?>
                    <?php endif; ?>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
        
        <!-- MOBILE: Card List -->
        <div class="result-cards show-mobile">
            <?php foreach ($results as $result): ?>
            <?php 
            $podiumClass = '';
            if ($opts['highlight_podium'] && $result['position'] <= 3) {
                $podiumClass = 'podium-' . $result['position'];
            }
            ?>
            <div class="result-card <?= $podiumClass ?>">
                <div class="result-card-header">
                    <div class="result-position">
                        <?php if ($result['position'] <= 3): ?>
                            <?= getRankingIcon($result['position'], 'md') ?>
                        <?php endif; ?>
                        <span class="position-number"><?= $result['position'] ?></span>
                    </div>
                    <div class="result-rider">
                        <strong><?= h($result['rider_name']) ?></strong>
                        <?php if ($opts['show_club'] && $result['club']): ?>
                        <span class="result-club"><?= h($result['club']) ?></span>
                        <?php endif; ?>
                    </div>
                    <div class="result-time">
                        <?= $result['total_time'] ?>
                    </div>
                </div>
                
                <?php if ($opts['show_stages'] && !$opts['mobile_compact']): ?>
                <details class="result-stages">
                    <summary>Sträcktider</summary>
                    <div class="stage-times">
                        <?php foreach ($result['stage_times'] as $i => $time): ?>
                        <div class="stage-time">
                            <span class="stage-label">SS<?= $i+1 ?></span>
                            <span class="stage-value"><?= $time ?></span>
                        </div>
                        <?php endforeach; ?>
                    </div>
                </details>
                <?php endif; ?>
            </div>
            <?php endforeach; ?>
        </div>
    </div>
    
    <?php
}
?>
```

---

## 🎨 CSS FÖR RESULT TABLE

**Fil:** `assets/css/components.css`

```css
/* ============================================================
   RESULT TABLE - Standardized Component
   ============================================================ */

.result-table-wrapper {
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

/* Desktop Table */
.result-table {
  width: 100%;
  border-collapse: collapse;
}

.result-table thead {
  background: var(--color-bg-sunken);
  position: sticky;
  top: 0;
  z-index: 10;
}

.result-table th {
  padding: var(--space-md);
  text-align: left;
  font-weight: var(--weight-semibold);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  border-bottom: 2px solid var(--color-border-strong);
}

.result-table td {
  padding: var(--space-sm) var(--space-md);
  border-bottom: 1px solid var(--color-border);
}

.result-row {
  transition: background var(--transition-fast);
}

.result-row:hover {
  background: var(--color-bg-hover);
}

/* Podium highlighting */
.podium-1 {
  background: rgba(255, 215, 0, 0.08); /* Gold tint */
}

.podium-2 {
  background: rgba(192, 192, 192, 0.08); /* Silver tint */
}

.podium-3 {
  background: rgba(205, 127, 50, 0.08); /* Bronze tint */
}

/* Column specific styles */
.col-position {
  width: 60px;
  font-weight: var(--weight-bold);
}

.col-position i {
  margin-right: 4px;
}

.col-time {
  font-family: var(--font-mono);
  font-weight: var(--weight-bold);
}

.col-diff {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
}

.col-stage {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
}

/* Mobile Cards */
.result-cards {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.result-card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-md);
  transition: all var(--transition-fast);
}

.result-card:active {
  transform: scale(0.98);
}

.result-card-header {
  display: grid;
  grid-template-columns: 48px 1fr auto;
  gap: var(--space-sm);
  align-items: center;
}

.result-position {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-xl);
  font-weight: var(--weight-bold);
}

.result-rider strong {
  display: block;
  font-size: var(--text-base);
  color: var(--color-text-primary);
}

.result-club {
  display: block;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-top: 2px;
}

.result-time {
  font-family: var(--font-mono);
  font-size: var(--text-lg);
  font-weight: var(--weight-bold);
}

/* Stage times expansion */
.result-stages {
  margin-top: var(--space-md);
  padding-top: var(--space-md);
  border-top: 1px solid var(--color-border);
}

.result-stages summary {
  cursor: pointer;
  font-size: var(--text-sm);
  color: var(--color-accent);
  font-weight: var(--weight-medium);
}

.stage-times {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  gap: var(--space-sm);
  margin-top: var(--space-sm);
}

.stage-time {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--space-xs);
  background: var(--color-bg-sunken);
  border-radius: var(--radius-sm);
}

.stage-label {
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  font-weight: var(--weight-medium);
}

.stage-value {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-text-primary);
}

/* Responsive */
@media (max-width: 767px) {
  .hide-mobile {
    display: none !important;
  }
  
  .show-mobile {
    display: flex !important;
  }
  
  /* Mobile edge-to-edge */
  .result-table-wrapper {
    margin-left: -16px;
    margin-right: -16px;
    border-radius: 0;
  }
  
  .result-cards {
    padding: 0 16px;
  }
}

@media (min-width: 768px) {
  .hide-mobile {
    display: table !important;
  }
  
  .show-mobile {
    display: none !important;
  }
}
```

---

## 🔄 MIGRATION PLAN

### STEG 1: Skapa Components (30 min)

1. **Skapa mapp:**
```bash
mkdir -p v2/components
```

2. **Skapa filer:**
- `v2/components/result-table.php`
- `v2/components/result-card.php`
- `v2/components/event-card.php`

3. **Kopiera CSS** till `assets/css/components.css`

### STEG 2: Migrera v2/results.php (20 min)

**Före:**
```php
<!-- Custom HTML för varje resultat -->
<div class="gs-result-card">...</div>
```

**Efter:**
```php
<?php 
require_once __DIR__ . '/components/result-table.php';

$results = /* fetch from DB */;
renderResultTable($results, [
    'show_stages' => true,
    'show_club' => true,
    'highlight_podium' => true
]);
?>
```

### STEG 3: Migrera v2/series-standings.php (20 min)

Ersätt custom table med `renderResultTable()`.

### STEG 4: Migrera v2/ranking/index.php (30 min)

Ersätt alla custom tables med `renderResultTable()`.

### STEG 5: Migrera v2/profile.php (20 min)

Använd samma komponent för rider results.

### STEG 6: Cleanup (15 min)

1. Ta bort gamla custom HTML
2. Ta bort duplicerad CSS
3. Test alla sidor

---

## 📊 FÖRE/EFTER

### FÖRE:
```
10 filer × 50 rader custom HTML = 500 rader
10 filer × 30 rader custom CSS = 300 rader
= 800 rader total
= 10 olika designs
= Underhållsmardröm
```

### EFTER:
```
1 komponent × 100 rader = 100 rader HTML
1 CSS-fil × 150 rader = 150 rader CSS
= 250 rader total
= 1 konsekvent design
= Lätt att underhålla
```

**SPARAT: 550 rader kod!**  
**VINST: 70% mindre kod + 100% konsekvent design!**

---

## ✅ FRAMGÅNGSKRITERIER

- [ ] Alla result displays använder samma komponent
- [ ] Desktop och mobile ser konsekventa ut
- [ ] Podium highlighting fungerar överallt
- [ ] Färgschema är enhetligt (guld/silver/brons)
- [ ] Lucide ikoner istället för emojis
- [ ] Edge-to-edge på mobile
- [ ] Expandable stage times på mobile
- [ ] Smooth animations

---

## 🎯 NÄSTA STEG

1. **Implementera result-table.php** först
2. **Testa på EN sida** (v2/results.php)
3. **Iterera** baserat på feedback
4. **Rulla ut** till alla andra sidor
5. **Ta bort** gammal custom HTML
6. **Dokumentera** komponenterna

---

**MÅLET:** 100% konsekvent design på ALLA resultat-sidor! 🎯
