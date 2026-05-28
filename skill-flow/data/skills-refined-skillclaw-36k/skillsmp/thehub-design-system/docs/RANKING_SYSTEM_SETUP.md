# TheHUB Ranking System - Komplett Uppsättningsguide

## Översikt

TheHUB:s ranking-system beräknar viktade rankingpoäng för Enduro, Downhill och Gravity-tävlingar baserat på:
- **Eventpoäng** från placering i tävling
- **Fältstorlek-multiplier** (0.75 - 1.00 beroende på antal startande)
- **Event-nivå-multiplier** (1.0 för nationell, 0.5 för sportmotion)
- **Tidsviktning** (1.0 för 0-12 månader, 0.5 för 13-24 månader, 0 för äldre)

## Databas-struktur

### Tabeller som behövs

#### 1. `ranking_points` - Huvudtabellen för viktade poäng
Skapad av: `/database/migrations/034_restore_ranking_points_table.sql`

Innehåller:
- `rider_id` - Förare-ID
- `event_id` - Event-ID
- `class_id` - Klass-ID
- `discipline` - Disciplin (ENDURO, DH, GRAVITY)
- `original_points` - Originalpoäng från results-tabellen
- `position` - Placering i tävlingen
- `field_size` - Antal startande i klassen
- `field_multiplier` - Fältstorlek-multiplier (0.75 - 1.00)
- `event_level_multiplier` - Event-nivå multiplier (1.0 eller 0.5)
- `time_multiplier` - Tidsviktning (1.0, 0.5 eller 0)
- `ranking_points` - Slutlig beräknad poäng
- `event_date` - Event-datum

**Formel**:
```
ranking_points = original_points × field_multiplier × event_level_multiplier × time_multiplier
```

#### 2. `ranking_settings` - Konfiguration
Innehåller JSON-konfiguration för:
- `field_multipliers` - Fältstorlek-multiplierar (1-15+ startande)
- `event_level_multipliers` - Event-nivå (national, sportmotion)
- `time_decay` - Tidsviktning (0-12, 13-24, 25+ månader)
- `last_calculation` - Timestamp för senaste omräkning

#### 3. `ranking_snapshots` - Historik
Sparar månatliga snapshots av ranking för varje förare/disciplin:
- Total rankingpoäng
- Ranking-position
- Positionsförändring
- Antal events

#### 4. `events.event_level` - Event-klassificering
Kolumn i events-tabellen som anger:
- `national` = 1.0 multiplier (SweCup, etc.)
- `sportmotion` = 0.5 multiplier

## Installation

### Steg 1: Kör migration

```bash
# Kör migrationen för att skapa ranking_points tabellen
mysql -u username -p database_name < /home/user/TheHUB/database/migrations/034_restore_ranking_points_table.sql
```

Eller via admin-gränssnitt om du har migrations-system.

### Steg 2: Verifiera tabellerna

Kontrollera att alla nödvändiga tabeller finns:
```sql
SHOW TABLES LIKE 'ranking%';
```

Bör visa:
- `ranking_points`
- `ranking_settings`
- `ranking_snapshots`
- `ranking_history` (valfri)

### Steg 3: Verifiera event_level kolumn

```sql
DESCRIBE events;
```

Kolumnen `event_level` ska vara av typen `ENUM('national', 'sportmotion')` med default `'national'`.

Om den saknas, kör:
```sql
ALTER TABLE events ADD COLUMN event_level ENUM('national', 'sportmotion') DEFAULT 'national';
```

### Steg 4: Sätt event_level på befintliga events

Uppdatera events baserat på deras typ:

```sql
-- Sätt SweCup events till national
UPDATE events
SET event_level = 'national'
WHERE name LIKE '%SweCup%';

-- Sätt GravitySeries events till national
UPDATE events
SET event_level = 'national'
WHERE name LIKE '%GravitySeries%';

-- Sätt övriga till sportmotion (eller vice versa beroende på policy)
UPDATE events
SET event_level = 'sportmotion'
WHERE event_level IS NULL
AND discipline IN ('ENDURO', 'DH');
```

## Första körning - Populera ranking_points

### Via Admin-gränssnittet (Rekommenderat)

1. Logga in som admin
2. Gå till `/admin/recalculate-all-points.php`
3. Klicka "Start Recalculation"
4. Följ stegen:
   - **Steg 1**: Räkna om event-poäng (från results)
   - **Steg 2**: Populera ranking_points + uppdatera snapshots
   - **Steg 3**: Räkna om klubbpoäng

### Via PHP direkt (För debugging)

```php
<?php
require_once 'config.php';
require_once 'includes/ranking_functions.php';

$db = getDB();

// Populera ranking_points
$stats = populateRankingPoints($db, true);

echo "Processed: {$stats['total_processed']}\n";
echo "Inserted: {$stats['total_inserted']}\n";
echo "Time: {$stats['elapsed_time']}s\n";

if (!empty($stats['errors'])) {
    echo "Errors: " . count($stats['errors']) . "\n";
    foreach ($stats['errors'] as $error) {
        echo "  - {$error}\n";
    }
}
```

## Rider-sidan visning

### Mobil Portrait (≤767px)
Visar 3 kolumner:
- Placering (🥇🥈🥉 eller #4)
- Event-namn
- Poäng (t.ex. "520p")

### Mobil Landscape (768-1279px)
Visar 4 kolumner:
- Placering
- Event-namn
- Poäng
- **Beräkning** (t.ex. "450 × 0.75" eller "450 × 0.75 × 0.50" vid sportmotion)

### Desktop (≥1280px)
Visar alla kolumner:
- Placering
- Event-namn
- Poäng
- Datum
- Klass
- Fältstorlek
- Event-poäng (originalpoäng)

## Underhåll

### Automatisk uppdatering

Ranking-systemet uppdateras automatiskt när:
- Nya results läggs till
- Event-poäng räknas om
- `/admin/recalculate-all-points.php` körs

### Manuell omräkning

För att räkna om alla ranking-poäng:
1. Gå till `/admin/recalculate-all-points.php`
2. Kör steg 2 för att populera ranking_points

### Manatlig snapshot-uppdatering

Kör detta via cron en gång i månaden:

```php
<?php
require_once 'config.php';
require_once 'includes/ranking_functions.php';

$db = getDB();
$stats = runFullRankingUpdate($db, false);
```

Detta skapar snapshots i `ranking_snapshots` för historisk tracking.

## Felsökning

### Problem: Inga events visas under "Race som gett rankingpoäng"

**Lösning 1**: Kontrollera att ranking_points tabellen finns
```sql
SHOW TABLES LIKE 'ranking_points';
```

Om den saknas, kör migration 034.

**Lösning 2**: Kontrollera att tabellen har data
```sql
SELECT COUNT(*) FROM ranking_points;
```

Om den är tom, kör populateRankingPoints() via `/admin/recalculate-all-points.php`.

**Lösning 3**: Fallback till results-tabellen
Om ranking_points saknas eller är tom, använder systemet automatiskt results-tabellen som fallback. Men poängen kommer då inte vara viktade.

### Problem: Poäng visar 0p eller fel värden

**Kontrollera multipliers**:
```sql
SELECT * FROM ranking_settings WHERE setting_key IN ('field_multipliers', 'event_level_multipliers', 'time_decay');
```

**Kontrollera en specifik riders poäng**:
```sql
SELECT
    e.name,
    e.date,
    e.event_level,
    rp.original_points,
    rp.field_size,
    rp.field_multiplier,
    rp.event_level_multiplier,
    rp.time_multiplier,
    rp.ranking_points
FROM ranking_points rp
JOIN events e ON rp.event_id = e.id
WHERE rp.rider_id = 7726
ORDER BY e.date DESC;
```

### Problem: Ranking-position är fel

**Räkna om ranking-snapshots**:
```php
<?php
require_once 'config.php';
require_once 'includes/ranking_functions.php';

$db = getDB();

// Räkna om för alla discipliner
foreach (['ENDURO', 'DH', 'GRAVITY'] as $discipline) {
    createRankingSnapshot($db, $discipline);
    echo "Updated {$discipline}\n";
}
```

## API / Funktioner

### PHP-funktioner tillgängliga

```php
// Populera ranking_points från results
populateRankingPoints($db, $debug = false);

// Hämta field-multipliers
getRankingFieldMultipliers($db);

// Hämta event-level multipliers
getEventLevelMultipliers($db);

// Hämta time-decay inställningar
getRankingTimeDecay($db);

// Beräkna ranking on-the-fly (utan att spara)
calculateRankingData($db, $discipline, $debug = false);

// Skapa ranking-snapshot
createRankingSnapshot($db, $discipline, $snapshotDate = null, $debug = false);

// Kör full ranking-uppdatering
runFullRankingUpdate($db, $debug = false);
```

## Prestanda

### Optimeringar i rider.php

1. **Try/catch på ranking_points query** - Faller tillbaka till results om tabellen saknas
2. **Display: table-cell !important** - Garanterar att poäng-kolumn visas på mobil
3. **Batch-inserts** - Insertar 100 records åt gången i populateRankingPoints()
4. **Index på ranking_points** - För snabba queries baserat på discipline och datum

### Prestanda-tips

- Kör populateRankingPoints() efter stora imports/uppdateringar
- Använd ranking_points tabell för visning (snabbt)
- Kör snapshots månadsvis via cron
- Undvik att räkna on-the-fly i produktionsmiljö

## Sammanfattning - Snabb start

För att få systemet att fungera:

1. **Kör migration**: `034_restore_ranking_points_table.sql`
2. **Uppdatera events**: Sätt `event_level` på alla events (national/sportmotion)
3. **Populera data**: Kör `/admin/recalculate-all-points.php` → Steg 2
4. **Verifiera**: Besök en rider-profil och kontrollera "Race som gett rankingpoäng"

Klart! Systemet visar nu:
- ✅ Korrekt viktade ranking-poäng
- ✅ Event-lista med alla poäng
- ✅ Beräkningar i landscape mobile
- ✅ Historiska snapshots för positionsändringar

## Support & Frågor

Vid problem, kontrollera:
1. Att alla tabeller finns (SHOW TABLES)
2. Att ranking_points har data (SELECT COUNT(*) FROM ranking_points)
3. Att event_level är satt på events
4. Att multipliers finns i ranking_settings

För debugging:
- Använd `/debug-rider-points.php?rider_id=XXXX` för att se rå data
- Använd `/check-ranking-points.php?rider_id=XXXX` för att verifiera data
- Kolla PHP error logs för exceptions
