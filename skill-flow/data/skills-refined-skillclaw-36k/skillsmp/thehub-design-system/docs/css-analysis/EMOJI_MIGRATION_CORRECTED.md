# EMOJI TO ICON MIGRATION - KORRIGERAD VERSION
**VIKTIGT:** Detta gäller **PRODUKTION** (pages/) - INTE v2/ backups!

---

## 🎯 EMOJIS I PRODUKTION

**Hittade i dessa RIKTIGA filer:**

```
pages/profile/results.php:    🥇 (1 förekomst)
pages/dashboard.php:          🏆 (1 förekomst)
pages/ranking.php:            🏆 (1 förekomst)
pages/club.php:               🏆 (2 förekomster)
pages/series/show.php:        🏆 (1 förekomst)
pages/series-single.php:      🥇🥈🥉 (12 förekomster!) ⚠️ VÄRST
pages/riders.php:             🏆 (1 förekomst)
```

**Total:** ~19 emoji-förekomster i 7 produktionsfiler

---

## ✅ BRA NYHETER!

**TheHUB använder REDAN SVG medalj-ikoner på event.php:**

```php
// I pages/event.php rad 1007-1015
<?php if ($result['class_position'] == 1): ?>
    <img src="/assets/icons/medal-1st.svg" alt="1:a" class="medal-icon-mobile">
<?php elseif ($result['class_position'] == 2): ?>
    <img src="/assets/icons/medal-2nd.svg" alt="2:a" class="medal-icon-mobile">
<?php elseif ($result['class_position'] == 3): ?>
    <img src="/assets/icons/medal-3rd.svg" alt="3:e" class="medal-icon-mobile">
```

**= Vi har redan en fungerande lösning!** 🎉

---

## 🔄 STRATEGI

### Option A: Använd befintliga SVG ikoner
- ✅ Redan designade
- ✅ Redan i produktion (event.php)
- ✅ Funkar på mobile
- ❌ Måste hantera som `<img>` tag

### Option B: Lucide Icons (rekommenderat)
- ✅ Inline SVG = färgbara
- ✅ Skalabara med CSS
- ✅ Enklare CSS
- ✅ Redan laddat i projektet

**REKOMMENDATION:** Använd Lucide för konsekvent!

---

## 🛠️ FIX #1: pages/series-single.php (VÄRST - 12 emojis)

### Hitta rad ~500-600:

```php
<?php if ($pos == 0): ?>🥇
<?php elseif ($pos == 1): ?>🥈
<?php elseif ($pos == 2): ?>🥉
```

### Ersätt med helper function:

**Högst upp i filen efter `<?php`:**

```php
<?php
require_once __DIR__ . '/../config.php';

// Medal icon helper
function getMedalIcon($position, $size = 'sm') {
    if ($position < 0 || $position > 2) return '';
    
    $icons = [
        0 => '<i data-lucide="trophy" class="icon-' . $size . ' icon-gold" aria-label="Första plats"></i>',
        1 => '<i data-lucide="medal" class="icon-' . $size . ' icon-silver" aria-label="Andra plats"></i>',
        2 => '<i data-lucide="award" class="icon-' . $size . ' icon-bronze" aria-label="Tredje plats"></i>'
    ];
    
    return $icons[$position];
}
?>
```

### Använd istället:

```php
<?= getMedalIcon($pos) ?>

<!-- För klubbmästerskap -->
<?= getMedalIcon($clubPos - 1) ?>  <!-- clubPos är 1-based, vår func är 0-based -->
```

---

## 🛠️ FIX #2: pages/profile/results.php

### Hitta:
```php
<span class="stat-label">Segrar 🥇</span>
```

### Ersätt med:
```php
<span class="stat-label">
    <i data-lucide="trophy" class="icon-xs icon-gold"></i>
    Segrar
</span>
```

---

## 🛠️ FIX #3: pages/dashboard.php

### Hitta:
```php
<a href="/series" class="btn btn--primary">🏆 Serier</a>
```

### Ersätt med:
```php
<a href="/series" class="btn btn--primary">
    <i data-lucide="trophy" class="icon-sm"></i>
    Serier
</a>
```

---

## 🛠️ FIX #4: pages/ranking.php

### Hitta:
```php
<div class="empty-state-icon">🏆</div>
```

### Ersätt med:
```php
<div class="empty-state-icon">
    <i data-lucide="trophy" class="icon-xl"></i>
</div>
```

---

## 🛠️ FIX #5: pages/club.php (2 förekomster)

### Hitta:
```php
<span class="podium-badge">🏆 <?= $member['podiums'] ?></span>
```

### Ersätt med:
```php
<span class="podium-badge">
    <i data-lucide="trophy" class="icon-xs icon-gold"></i>
    <?= $member['podiums'] ?>
</span>
```

### Hitta:
```php
• 🏆 ' . $member['podiums']
```

### Ersätt med:
```php
• <i data-lucide="trophy" class="icon-xs"></i> ' . $member['podiums']
```

---

## 🛠️ FIX #6: pages/riders.php

### Samma som club.php ovan

---

## 🛠️ FIX #7: pages/series/show.php

### Hitta:
```php
<span class="series-logo-placeholder">🏆</span>
```

### Ersätt med:
```php
<span class="series-logo-placeholder">
    <i data-lucide="trophy" class="icon-lg"></i>
</span>
```

---

## 🎨 CSS (lägg till i assets/css/components.css)

```css
/* Medal/Trophy Icons */
.icon-xs { width: 12px; height: 12px; }
.icon-sm { width: 16px; height: 16px; }
.icon-md { width: 20px; height: 20px; }
.icon-lg { width: 24px; height: 24px; }
.icon-xl { width: 48px; height: 48px; }

.icon-gold {
    color: #FFD700;
    stroke: #FFD700;
}

.icon-silver {
    color: #C0C0C0;
    stroke: #C0C0C0;
}

.icon-bronze {
    color: #CD7F32;
    stroke: #CD7F32;
}

/* Dark mode */
html[data-theme="dark"] .icon-gold {
    color: #FFE55C;
}

html[data-theme="dark"] .icon-silver {
    color: #E8E8E8;
}

html[data-theme="dark"] .icon-bronze {
    color: #E09142;
}
```

---

## ✅ VERIFIERING

```bash
# Ska returnera 0
grep -r "🥇\|🥈\|🥉\|🏆" --include="*.php" pages/ | wc -l
```

---

## 🎯 SAMMANFATTNING

**7 filer att fixa:**
1. ⚠️ **pages/series-single.php** (12 emojis) - 20 min
2. pages/profile/results.php (1 emoji) - 2 min
3. pages/dashboard.php (1 emoji) - 2 min
4. pages/ranking.php (1 emoji) - 2 min
5. pages/club.php (2 emojis) - 5 min
6. pages/riders.php (1 emoji) - 2 min
7. pages/series/show.php (1 emoji) - 2 min

**Total tid:** ~35 minuter

---

## 🚀 BONUS: Ta bort v2/ backups

```bash
# Skapa backup först
mkdir -p backups/v2-backup-$(date +%Y%m%d)
mv v2 backups/v2-backup-$(date +%Y%m%d)/

# Verifiera att sidan funkar
# Om OK efter 1 vecka:
rm -rf backups/v2-backup-*/
```

---

**DETTA ÄR DE RIKTIGA PRODUKTIONSFILERNA!** ✅
