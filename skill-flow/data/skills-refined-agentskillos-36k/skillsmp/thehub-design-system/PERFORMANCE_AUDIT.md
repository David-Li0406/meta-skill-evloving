# TheHUB Prestandarapport

**Datum:** 2025-12-10
**Version:** 1.0

---

## Sammanfattning

| Kategori | Status | Prioritet |
|----------|--------|-----------|
| **Databasoptimering** | Kritisk | Hög |
| **Asset-hantering** | Medel | Medel |
| **PHP-kod** | Bra | Låg |
| **Caching** | Bra | Låg |
| **Säkerhet** | Utmärkt | - |

**Kodbasstatistik:**
- 324 PHP-filer
- ~108,000 rader PHP-kod
- 1,191 include/require-anrop
- 213 KB CSS (10 filer)
- 73 KB JavaScript (10 filer)

---

## 1. KRITISKA PROBLEM - DATABAS

### 1.1 N+1 Query Problem (7 instanser)

Dessa skapar exponentiellt många databasanrop och är den största prestandaboven:

| Fil | Rad | Beskrivning | Impact |
|-----|-----|-------------|--------|
| `includes/series-points.php` | 114-155 | Query per resultat i loop | 100+ extra anrop |
| `includes/series-points.php` | 188-194 | Query per event i loop | 10-50 extra anrop |
| `includes/series-points.php` | 332-337 | Query per series_event | 5-20 extra anrop |
| `includes/class-calculations.php` | 128-150 | Update per resultat | Per resultat |
| `includes/rebuild-rider-stats.php` | 156-170 | Query per rider | 1000+ anrop |
| `admin/diagnose-series.php` | 34-62 | Nästlade loopar | Exponentiellt |
| `admin/normalize-names.php` | 118 | Alla riders utan limit | Memory overflow |

**Lösning:** Byt till batch-operationer med JOINs istället för loopar.

### 1.2 Saknade LIMIT-klausuler

Filer som hämtar ALLA rader utan begränsning:

```php
// Risk för memory exhaustion
$riders = $db->getAll("SELECT id, firstname, lastname FROM riders");
$seriesData = $db->getAll("SELECT * FROM series");
```

**Påverkade filer:**
- `admin/normalize-names.php:118`
- `admin/diagnose-series.php:250-265`
- Flera admin-verktyg

### 1.3 Rekommenderade Index

```sql
-- Lägg till dessa index för bättre prestanda
ALTER TABLE results ADD INDEX idx_event_cyclist (event_id, cyclist_id);
ALTER TABLE series_events ADD INDEX idx_series_event (series_id, event_id);
ALTER TABLE series_results ADD INDEX idx_series_event_cyclist (series_id, event_id, cyclist_id);
ALTER TABLE riders ADD INDEX idx_license_number (license_number);
ALTER TABLE results ADD INDEX idx_class_id (class_id);
ALTER TABLE riders ADD INDEX idx_club_id (club_id);
```

---

## 2. MEDEL PRIORITET - ASSETS

### 2.1 CSS inte bundlad/minifierad

**Nuläge:**
- 10 separata CSS-filer laddas (213 KB)
- Varje fil = 1 HTTP-request
- Ingen minifiering i utvecklingsmiljö

**Rekommendation:**
1. Bundla alla CSS till en fil
2. Minifiera för produktion
3. Förväntat resultat: ~100 KB (50% minskning)

**Påverkad fil:** `includes/layout-header.php:249-276`

### 2.2 JavaScript inte optimerat

**Nuläge:**
- 10 separata JS-filer (73 KB)
- `event-map.js` (25 KB) laddas på alla sidor
- Ingen lazy loading

**Rekommendation:**
1. Ladda `event-map.js` endast på event-sidor
2. Bundla och minifiera JS
3. Använd `defer` attribut på scripts

### 2.3 Inline CSS (1,093 instanser)

Många inline `style=""` attribut i PHP-filer, främst i admin:
- `/admin/` - 742 instanser
- Övriga - 351 instanser

**Rekommendation:** Flytta till CSS-klasser för bättre cachebarhet.

### 2.4 Lucide Icons saknar SRI

```html
<!-- NULÄGE (osäkert) -->
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>

<!-- REKOMMENDERAT -->
<script src="https://unpkg.com/lucide@0.x.x/dist/umd/lucide.min.js"
        integrity="sha384-..." crossorigin="anonymous"></script>
```

---

## 3. BRA - SAKER SOM FUNGERAR

### 3.1 Caching i .htaccess

```apache
# Redan konfigurerat korrekt:
ExpiresByType text/css "access plus 1 week"
ExpiresByType application/javascript "access plus 1 week"
ExpiresByType image/png "access plus 1 month"
```

### 3.2 Gzip komprimering

```apache
# Aktiverat:
AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json
```

### 3.3 Cache busting med filemtime

```php
// Korrekt implementerat:
<link rel="stylesheet" href="/assets/css/reset.css?v=<?= filemtime(...) ?>">
```

### 3.4 Service Worker (PWA)

- Cache-first strategi för statiska resurser
- Precaching av viktiga filer
- Offline-stöd

### 3.5 Säkra sessioner

```php
// Implementerat:
- httponly cookies
- samesite=Lax
- session_regenerate_id()
- Rate limiting (5 försök/15 min)
- CSRF-skydd
```

### 3.6 Prepared Statements

Alla databasfrågor använder prepared statements - ingen SQL-injection risk.

---

## 4. ERROR_LOG ANVÄNDNING

**159 error_log() anrop i 39 filer**

Flera är i produktion-känsliga filer:
- `includes/db.php` - 14 anrop (loggar vid varje anslutning!)
- `includes/point-calculations.php` - 20 anrop
- `admin/import-uci.php` - 17 anrop

**Problem:** Överdriven loggning kan:
1. Fylla loggfiler snabbt
2. Sakta ner I/O
3. Exponera känslig information

**Rekommendation:** Villkora loggning med DEBUG-flagga:
```php
if (defined('APP_DEBUG') && APP_DEBUG) {
    error_log("Debug info...");
}
```

---

## 5. ÅTGÄRDSPLAN

### Fas 1 - Kritiskt (Gör först)

| Åtgärd | Fil | Förväntat resultat |
|--------|-----|-------------------|
| Fixa N+1 i series-points.php | `includes/series-points.php` | 90% färre DB-anrop |
| Lägg till databas-index | SQL-migrering | 2-5x snabbare queries |
| Lägg till LIMIT på admin-sidor | `admin/*.php` | Förhindra memory overflow |

### Fas 2 - Optimering (Gör sen)

| Åtgärd | Beskrivning |
|--------|-------------|
| Bundla CSS | Kombinera till 1 fil + minifiera |
| Lazy-load event-map.js | Ladda endast på event-sidor |
| Minska inline styles | Flytta till CSS-klasser |
| SRI för externa scripts | Lägg till integrity hash |

### Fas 3 - Underhåll (Löpande)

| Åtgärd | Beskrivning |
|--------|-------------|
| Rensa error_log | Lägg till DEBUG-villkor |
| Ta bort V2-kod | Legacy-filer kan tas bort |
| Query monitoring | Implementera slow query log |

---

## 6. PRESTANDAMÄTNING

För att mäta förbättringar, övervaka:

1. **Databas:**
   - Antal queries per sidladdning
   - Genomsnittlig query-tid
   - Slow query log

2. **Frontend:**
   - Page load time (< 3s mål)
   - Time to First Byte (< 500ms mål)
   - Number of requests (< 20 mål)

3. **Server:**
   - Memory usage per request
   - CPU usage
   - Error log storlek

---

## 7. QUICK WINS

Snabba åtgärder som ger omedelbar förbättring:

### 7.1 Lägg till index (5 min)
```sql
ALTER TABLE results ADD INDEX idx_event_cyclist (event_id, cyclist_id);
ALTER TABLE series_results ADD INDEX idx_series_event_cyclist (series_id, event_id, cyclist_id);
```

### 7.2 Villkorad laddning av map.js

I `includes/layout-footer.php`:
```php
<?php if (isset($needsMap) && $needsMap): ?>
<script src="/assets/js/event-map.js"></script>
<?php endif; ?>
```

### 7.3 Begränsa admin-queries

I admin-verktyg, lägg till:
```php
// Istället för:
$riders = $db->getAll("SELECT * FROM riders");

// Använd:
$riders = $db->getAll("SELECT * FROM riders LIMIT 1000");
```

---

## Slutsats

TheHUB har en **solid kodbas** med bra säkerhetspraktiker och fungerande caching. De kritiska förbättringarna handlar främst om **databasoptimering** (N+1-problem och saknade index).

**Prioritera:**
1. Fixa N+1 queries i `series-points.php`
2. Lägg till databas-index
3. Bundla/minifiera CSS/JS

Med dessa åtgärder förväntas sidladdningstiden minska med **50-70%** för tunga sidor som rankings och resultat.
