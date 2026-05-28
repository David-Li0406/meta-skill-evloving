# TheHUB - Poängberäkning Omräkning

## Översikt

Detta dokument beskriver hur poängomräkningen genomförs i TheHUB.

## Datum för omräkning
**2025-11-25**

## Problem som åtgärdades

### 1. GravitySeries Total felaktiga poäng
- **Problem:** Seriepoäng beräknades felaktigt för GravitySeries Total
- **Orsak:** Results.points beräknades från events.point_scale_id istället för series.point_scale_id
- **Lösning:** Omräkning av alla event-poäng baserat på korrekt point scale

### 2. Rankingpoäng
- **Problem:** Rankingpoäng behövde räknas om från start
- **Orsak:** Uppdaterad förståelse av systemet
- **Lösning:** Fullständig omräkning av alla rankingpoäng

### 3. Klubbpoäng
- **Problem:** Klubbpoäng behövde räknas om för alla serier
- **Orsak:** Beroende på korrekta seriepoäng och rankingpoäng
- **Lösning:** Omräkning av alla klubbpoäng

## Omräkningsprocess

Omräkningen görs i följande ordning:

### Steg 1: Event-poäng (results.points)
**Vad:** Räkna om `results.points` baserat på `events.point_scale_id`
**Varför:** Dessa poäng är basen för allt annat
**Script:** `/admin/recalculate-all-points.php?step=1`

**Detaljer:**
- För varje event:
  - Hämta eventets point_scale_id
  - För varje resultat i eventet:
    - Beräkna poäng baserat på position och point scale
    - Uppdatera results.points
    - För DH-event: Hantera run_1_points och run_2_points

### Steg 2: Rankingpoäng
**Vad:** Räkna om alla rankingpoäng med korrekt formel
**Varför:** Rankingpoäng används för individuellt ranking och global klubbranking
**Script:** `/admin/recalculate-all-points.php?step=2`

**Formel:**
```
Ranking Points = Original Points × Field Multiplier × Event Level Multiplier × Time Multiplier

Där:
- Original Points = results.points
- Field Multiplier = Baserat på antal deltagare i klassen (1-15+ riders)
- Event Level Multiplier = 1.00 för nationellt, 0.50 för sportmotion
- Time Multiplier = 1.00 för 0-12 mån, 0.50 för 13-24 mån, 0.00 för 25+ mån
```

**Detaljer:**
- Räkna om ranking för alla discipliner: ENDURO, DH, GRAVITY
- Skapa snapshots för månatlig tracking
- Uppdatera ranking_points tabell
- Uppdatera ranking_snapshots tabell

### Steg 3: Klubbpoäng per serie
**Vad:** Räkna om klubbpoäng för varje serie
**Varför:** Klubbpoäng baseras på seriepoäng (results.points)
**Script:** `/admin/recalculate-all-points.php?step=3`

**Regel:**
För varje klass i varje event i serien:
- Bästa åkaren från klubben: 100% av sina seriepoäng → klubben
- Näst bästa åkaren från klubben: 50% av sina seriepoäng → klubben
- Övriga: 0%

**Detaljer:**
- För varje aktiv serie:
  - Rensa befintliga club_rider_points, club_event_points, club_standings_cache
  - Hämta alla event i serien (via series_events ELLER events.series_id)
  - För varje event:
    - Beräkna klubbpoäng per klass med 100%/50%-regeln
    - Uppdatera club_rider_points
    - Uppdatera club_event_points
  - Uppdatera club_standings_cache för serien

### Steg 4: Global klubbranking
**Vad:** Uppdatera global klubbranking baserat på rankingpoäng
**Varför:** Global klubbranking baseras på summan av alla åkares rankingpoäng
**Script:** Ingår i steg 2 (runFullRankingUpdate)

**Detaljer:**
- Summera alla åkares rankingpoäng per klubb
- Sortera klubbar efter total rankingpoäng
- Tillämpa samma 24-månadersregel som individuellt ranking

## Tekniska detaljer

### Databasstrukturer som påverkas

1. **results** - Huvudtabell för resultat
   - `points` - Event-poäng (från events.point_scale_id)
   - `run_1_points`, `run_2_points` - För DH-event

2. **ranking_points** - Rankingpoäng per event/class
   - `original_points` - Från results.points
   - `field_multiplier` - Baserat på antal deltagare
   - `event_level_multiplier` - Nationellt vs sportmotion
   - `ranking_points` - Beräknad slutpoäng

3. **ranking_snapshots** - Månatliga snapshots
   - `total_ranking_points` - Total efter tidsmultiplikator
   - `points_last_12_months` - Poäng från senaste 12 månaderna
   - `points_months_13_24` - Poäng från månad 13-24

4. **club_rider_points** - Ryttarnas bidrag till klubbpoäng
   - `original_points` - Ryttarens seriepoäng
   - `club_points` - Efter 100%/50%-regel
   - `percentage_applied` - 100 eller 50

5. **club_event_points** - Klubbpoäng per event
   - `total_points` - Summa för alla klasser

6. **club_standings_cache** - Klubbställning per serie
   - `total_points` - Total seriepoäng

7. **club_ranking_snapshots** - Global klubbranking (via ranking_functions.php)
   - Baserat på summan av alla åkares rankingpoäng

## Verifiering

Efter omräkning, verifiera följande:

### 1. Event-poäng
```sql
-- Kontrollera att alla resultat har korrekta poäng
SELECT e.name, e.date, COUNT(r.id) as results, SUM(r.points) as total_points
FROM events e
JOIN results r ON e.id = r.event_id
WHERE r.status = 'finished'
GROUP BY e.id
ORDER BY e.date DESC
LIMIT 10;
```

### 2. Rankingpoäng
```sql
-- Kontrollera ranking för ENDURO
SELECT r.firstname, r.lastname, rs.total_ranking_points, rs.events_count
FROM ranking_snapshots rs
JOIN riders r ON rs.rider_id = r.id
WHERE rs.discipline = 'ENDURO'
AND rs.snapshot_date = (SELECT MAX(snapshot_date) FROM ranking_snapshots WHERE discipline = 'ENDURO')
ORDER BY rs.ranking_position ASC
LIMIT 10;
```

### 3. Klubbpoäng per serie
```sql
-- Kontrollera klubbställning för GravitySeries Total
SELECT c.name, csc.total_points, csc.total_participants, csc.events_count
FROM club_standings_cache csc
JOIN clubs c ON csc.club_id = c.id
WHERE csc.series_id = 8  -- GravitySeries Total
ORDER BY csc.total_points DESC
LIMIT 10;
```

### 4. Global klubbranking
```sql
-- Kontrollera global klubbranking
SELECT c.name, crs.total_ranking_points, crs.riders_count, crs.events_count
FROM club_ranking_snapshots crs
JOIN clubs c ON crs.club_id = c.id
WHERE crs.discipline = 'GRAVITY'
AND crs.snapshot_date = (SELECT MAX(snapshot_date) FROM club_ranking_snapshots WHERE discipline = 'GRAVITY')
ORDER BY crs.ranking_position ASC
LIMIT 10;
```

## Körning av omräkning

### Web-gränssnitt (Rekommenderat)
1. Gå till: `/admin/recalculate-all-points.php`
2. Granska statistik
3. Klicka "Dry Run" för att se vad som skulle hända
4. Klicka "Start Recalculation" för att köra omräkningen
5. Följ steg 1 → 2 → 3 → Complete

### Manuell körning (för debugging)
```bash
# Steg 1: Event-poäng
curl "http://localhost/admin/recalculate-all-points.php?step=1"

# Steg 2: Rankingpoäng
curl "http://localhost/admin/recalculate-all-points.php?step=2"

# Steg 3: Klubbpoäng
curl "http://localhost/admin/recalculate-all-points.php?step=3"
```

## Tidsuppskattning

Baserat på antal resultat:
- **< 1000 resultat:** ~30 sekunder
- **1000-5000 resultat:** 1-3 minuter
- **5000-10000 resultat:** 3-7 minuter
- **> 10000 resultat:** 7-15 minuter

## Backup

**VIKTIGT:** Ta alltid backup innan omräkning!

```bash
# Backup av databas
mysqldump -u root -p thehub > backup_before_recalc_$(date +%Y%m%d_%H%M%S).sql

# Backup av specifika tabeller
mysqldump -u root -p thehub \
  results \
  ranking_points \
  ranking_snapshots \
  club_rider_points \
  club_event_points \
  club_standings_cache \
  > backup_points_tables_$(date +%Y%m%d_%H%M%S).sql
```

## Rollback (om något går fel)

```bash
# Återställ från backup
mysql -u root -p thehub < backup_before_recalc_YYYYMMDD_HHMMSS.sql
```

## Kontakter

Om problem uppstår:
- **Utvecklare:** Claude Code
- **Datum:** 2025-11-25
- **Dokumentation:** `/outputs/THEHUB_POANGSTRUKTURER.md`
