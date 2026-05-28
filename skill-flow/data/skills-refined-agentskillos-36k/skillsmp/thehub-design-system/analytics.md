# TheHUB Analytics Platform

> Komplett dokumentation av statistik- och analysverktyg

---

## OVERSIKT

TheHUB Analytics Platform ar ett komplett system for att analysera deltagardata,
identifiera trender, och generera insikter for svensk mountainbike-sport.

### Arkitektur

```
analytics/
├── includes/
│   ├── AnalyticsEngine.php    # Beraknar och lagrar statistik
│   ├── KPICalculator.php      # 40+ metoder for KPI-berakningar
│   └── IdentityResolver.php   # Hanterar dubbletter
├── cron/
│   └── refresh-analytics.php  # Daglig uppdatering
└── populate-historical.php    # Generera historisk data

admin/
├── analytics-dashboard.php    # KPI-oversikt
├── analytics-flow.php         # Serieflode-visualisering
├── analytics-reports.php      # 6 rapporttyper
├── analytics-trends.php       # Trend-grafer
├── analytics-populate.php     # Manuell populate
├── analytics-reset.php        # Rensa data
└── analytics-diagnose.php     # Diagnostik
```

### Databastabeller

| Tabell | Beskrivning |
|--------|-------------|
| `rider_yearly_stats` | Pre-beraknad statistik per rider/ar |
| `series_participation` | Deltagande per serie/ar |
| `series_crossover` | Kors-deltagande mellan serier |
| `club_yearly_stats` | Klubbstatistik per ar |
| `venue_yearly_stats` | Arenstatistik per ar |
| `analytics_snapshots` | Historiska snapshots |
| `analytics_cron_runs` | Cron-korningslogg med las |
| `rider_merge_map` | Identity resolution for dubbletter |

---

## RAPPORTTYPER

### 1. Arssammanfattning (Summary)

**Endpoint:** `?report=summary&year=YYYY`

Visar:
- Alla KPI:er for aret
- Tillvaxttrender (5 ar)
- Top 10 klubbar
- Disciplinfordelning
- Aldersfordelning

**Metoder:**
- `getAllKPIs(year)`
- `getGrowthTrend(5)`
- `getTopClubs(year, 10)`
- `getDisciplineDistribution(year)`
- `getAgeDistribution(year)`

---

### 2. Retention & Churn-analys

**Endpoint:** `?report=retention&year=YYYY`

Visar:
- Retention rate (andel som aterkommer)
- Churn rate (andel som slutar)
- Antal som slutat forra aret
- Antal comebacks (atervandare)
- One-timers (1-2 starter totalt)
- Inaktiva 2+ ar

**Sektioner:**

#### Oversikt
| KPI | Beskrivning |
|-----|-------------|
| Retention Rate | % som aterkommer fran forra aret |
| Churn Rate | % som slutade |
| Churned Count | Antal som slutat |
| Comebacks | Antal atervandare |

#### Trend-graf (5 ar)
Chart.js-visualisering av retention/churn over tid.

#### Hur lange borta?
Gruppering av inaktiva per antal ar:
- 1 ar inaktiv
- 2 ar inaktiv
- 3+ ar inaktiv

#### Churn per segment
- **Per aldersgrupp**: Vilka aldrar tappar vi flest fran?
- **Per disciplin**: Vilka discipliner bloder mest?
- **Per klubb**: Top 10 klubbar med flest churned

#### Listor (exporterbara)
1. **Churned Riders** - De som slutade forra aret
2. **Comebacks** - De som atervande efter uppehall
3. **Win-Back Targets** - Prioriterad kontaktlista
4. **One-Timers** - De som bara provade 1-2 ggr

**Metoder:**
- `getChurnedRiders(year, limit)`
- `getOneTimers(year, maxStarts)`
- `getComebackRiders(year, minGapYears)`
- `getInactiveByDuration(year)`
- `getRetentionTrend(years)`
- `getChurnBySegment(year)`
- `getChurnSummary(year)`
- `getWinBackTargets(year, limit)`

**CSV-exporter:**
- `?report=retention&year=YYYY&export=winback`
- `?report=retention&year=YYYY&export=churned`
- `?report=retention&year=YYYY&export=comebacks`

---

### 3. Serie-analys

**Endpoint:** `?report=series&year=YYYY`

Visar:
- Cross-participation rate (riders i 2+ serier)
- Entry points (var borjar nya riders?)
- Feeder matrix (flode mellan serier)

**Metoder:**
- `getCrossParticipationRate(year)`
- `getEntryPointDistribution(year)`
- `calculateFeederMatrix(year)`
- `getFeederConversionRate(from, to, year)`
- `getSeriesLoyaltyRate(seriesId, year)`
- `getExclusivityRate(seriesId, year)`
- `getSeriesOverlap(series1, series2, year)`

---

### 4. Klubbrapport

**Endpoint:** `?report=clubs&year=YYYY`

Visar:
- Top klubbar med flest aktiva riders
- Klubbarnas totala poang
- Vinster och pallplatser
- Tillvaxt per klubb

**Metoder:**
- `getTopClubs(year, limit)`
- `getClubGrowth(clubId, years)`

---

### 5. Demografisk Oversikt

**Endpoint:** `?report=demographics&year=YYYY`

Visar:
- Snittålder
- Konsfordelning (M/F/Okant)
- Aldersfordelning (grupper)
- Disciplinfordelning (primary)
- Faktiskt deltagande per disciplin

**Sektioner:**

#### Grunddata
| Metric | Beskrivning |
|--------|-------------|
| Snittålder | Genomsnittsalder for alla deltagare |
| Konsfordelning | Antal M/F/Okant |

#### Aldersgrupper
- Under 15
- 15-17
- 18-25
- 26-35
- 36-45
- 46-55
- Over 55

#### Disciplinfordelning
1. **Primary Discipline** - En disciplin per rider (dar de deltar mest)
2. **Faktiskt deltagande** - Unika riders per disciplin (kan finnas i flera)

**Metoder:**
- `getAverageAge(year)`
- `getGenderDistribution(year)`
- `getAgeDistribution(year)`
- `getDisciplineDistribution(year)` - Primary
- `getDisciplineParticipation(year)` - Faktiskt

---

### 6. Nya Deltagare (Rookies)

**Endpoint:** `?report=rookies&year=YYYY&series=X`

Visar:
- Antal nya deltagare
- Andel av totalt
- Snittålder for rookies
- Konsfordelning for rookies
- 5-ars trend med graf

**Sektioner:**

#### Oversikt
| KPI | Beskrivning |
|-----|-------------|
| Nya riders | Antal forstagangsdeltagare |
| Andel | % av totala deltagare |
| Snittålder | Genomsnittsalder for rookies |
| Kon | M/F-fordelning |

#### Trend-graf
5-ars rookie-trend med Chart.js.

#### Aldersfordelning
Rookies per aldersgrupp.

#### Klassfordelning
Vilka klasser startar rookies i?

#### Events med flest rookies
Top 20 events dar nya deltagare borjar.

#### Klubbar med flest rookies
Vilka klubbar attraherar nya?

#### Komplett lista
Alla rookies med lankar till profiler.

**Metoder:**
- `getNewRidersCount(year)`
- `getRookieAgeDistribution(year)`
- `getRookieClassDistribution(year)`
- `getEventsWithMostRookies(year, limit)`
- `getClubsWithMostRookies(year, limit)`
- `getRookiesList(year, seriesId)`
- `getSeriesWithRookies(year)`
- `getRookieTrend(years)`
- `getRookieAgeTrend(years)`
- `getRookieAverageAge(year)`
- `getRookieGenderDistribution(year)`
- `getRookieDisciplineParticipation(year)`

**CSV-export:**
- `?report=rookies&year=YYYY&export=1`

---

## KPI-KALKYLATOR (ALLA METODER)

### Retention & Growth

| Metod | Returtyp | Beskrivning |
|-------|----------|-------------|
| `getRetentionRate(year)` | float | Andel som aterkommer (0-100%) |
| `getChurnRate(year)` | float | Andel som slutar (0-100%) |
| `getNewRidersCount(year)` | int | Antal nya riders |
| `getTotalActiveRiders(year)` | int | Totalt antal aktiva |
| `getGrowthRate(year)` | float | Tillvaxt vs forra aret (%) |
| `getRetainedRidersCount(year)` | int | Antal atervandare |
| `getGrowthTrend(years)` | array | Tillvaxt over tid |

### Demographics

| Metod | Returtyp | Beskrivning |
|-------|----------|-------------|
| `getAverageAge(year)` | float | Snittålder |
| `getGenderDistribution(year)` | array | {M: x, F: y, unknown: z} |
| `getAgeDistribution(year)` | array | Antal per aldersgrupp |
| `getDisciplineDistribution(year)` | array | Primary discipline per rider |
| `getDisciplineParticipation(year)` | array | Faktiskt deltagande |

### Rookie Analysis

| Metod | Returtyp | Beskrivning |
|-------|----------|-------------|
| `getRookieAgeDistribution(year)` | array | Rookies per aldersgrupp |
| `getRookieClassDistribution(year)` | array | Rookies per klass |
| `getEventsWithMostRookies(year, limit)` | array | Events med flest rookies |
| `getRookiesList(year, seriesId?)` | array | Komplett rookielista |
| `getSeriesWithRookies(year)` | array | Serier for filtrering |
| `getRookieDisciplineParticipation(year)` | array | Rookies per disciplin |
| `getRookieTrend(years)` | array | Rookie-trend over tid |
| `getRookieAgeTrend(years)` | array | Aldersfordelning over tid |
| `getRookieAverageAge(year)` | float | Snittålder for rookies |
| `getRookieGenderDistribution(year)` | array | Kon for rookies |
| `getClubsWithMostRookies(year, limit)` | array | Klubbar med rookies |

### Churn & Retention Deep Analysis

| Metod | Returtyp | Beskrivning |
|-------|----------|-------------|
| `getChurnedRiders(year, limit)` | array | Lista churned riders |
| `getOneTimers(year, maxStarts)` | array | Riders med 1-2 starter |
| `getComebackRiders(year, minGapYears)` | array | Atervandare |
| `getInactiveByDuration(year)` | array | Inaktiva per ar borta |
| `getRetentionTrend(years)` | array | Retention over tid |
| `getChurnBySegment(year)` | array | Churn per alder/disciplin/klubb |
| `getChurnSummary(year)` | array | Sammanfattande nyckeltal |
| `getWinBackTargets(year, limit)` | array | Prioriterad kontaktlista |

### Series Flow

| Metod | Returtyp | Beskrivning |
|-------|----------|-------------|
| `getFeederConversionRate(from, to, year)` | float | Konvertering mellan serier |
| `getCrossParticipationRate(year)` | float | Andel i 2+ serier |
| `getSeriesLoyaltyRate(seriesId, year)` | float | Atervandare i serie |
| `getExclusivityRate(seriesId, year)` | float | Andel exklusiva |
| `getEntryPointDistribution(year)` | array | Var borjar nya? |
| `calculateFeederMatrix(year)` | array | Flode mellan serier |
| `getSeriesOverlap(s1, s2, year)` | array | Overlap mellan tva serier |

### Club Analysis

| Metod | Returtyp | Beskrivning |
|-------|----------|-------------|
| `getTopClubs(year, limit)` | array | Top klubbar |
| `getClubGrowth(clubId, years)` | array | Klubbtillvaxt over tid |

### Geographic

| Metod | Returtyp | Beskrivning |
|-------|----------|-------------|
| `getRidersByRegion(year)` | array | Riders per region |

### Utility

| Metod | Returtyp | Beskrivning |
|-------|----------|-------------|
| `getAllKPIs(year)` | array | Alla nyckeltal |
| `compareYears(year1, year2)` | array | Jamfor tva ar |

---

## ANALYTICS ENGINE (BERAKNINGAR)

AnalyticsEngine beraknar och lagrar statistik i pre-beraknade tabeller.

### Berakningsmetoder

| Metod | Beskrivning |
|-------|-------------|
| `calculateYearlyStats(year)` | Beraknar rider_yearly_stats |
| `calculateYearlyStatsBulk(year)` | Bulk-optimerad version (1 SQL) |
| `calculateSeriesParticipation(year)` | Beraknar series_participation |
| `calculateSeriesCrossover(year)` | Beraknar series_crossover |
| `calculateClubStats(year)` | Beraknar club_yearly_stats |
| `calculateVenueStats(year)` | Beraknar venue_yearly_stats |

### Refresh-metoder

| Metod | Beskrivning |
|-------|-------------|
| `refreshAllStats(year)` | Kör alla berakningar |
| `refreshAllStatsFast(year)` | Optimerad version |

### Job-hantering

| Metod | Beskrivning |
|-------|-------------|
| `startJob(name, key, force)` | Startar jobb med las |
| `endJob(status, rows, log)` | Avslutar jobb |

---

## ADMIN-VERKTYG

### Analytics Dashboard
**URL:** `/admin/analytics-dashboard.php`

Visar:
- KPI-kort med snabbstatistik
- Tillvaxttrender
- Retention oversikt

### Analytics Flow
**URL:** `/admin/analytics-flow.php`

Visualiserar:
- Serieflode (Sankey-liknande)
- Var kommer riders ifran?
- Var gar de vidare?

### Analytics Reports
**URL:** `/admin/analytics-reports.php`

6 rapporttyper med CSV-export.

### Analytics Trends
**URL:** `/admin/analytics-trends.php`

Chart.js-grafer for:
- Deltagartrender
- Retention over tid
- Aldersfordelning over tid

### Analytics Populate
**URL:** `/admin/analytics-populate.php`

Interaktiv populate med:
- AJAX-baserad progress
- Force-mode for omberakning
- Arval

### Analytics Reset
**URL:** `/admin/analytics-reset.php`

Rensa:
- Cron-runs (lasar)
- All analytics-data
- Specifikt ar

### Analytics Diagnose
**URL:** `/admin/analytics-diagnose.php`

Jamfor:
- Faktisk data i events/results
- Pre-beraknad data i analytics-tabeller
- Identifierar diskrepanser

---

## CRON & AUTOMATISERING

### Daglig Refresh
**Fil:** `analytics/cron/refresh-analytics.php`

Kors dagligen och uppdaterar:
- Aktuellt ar
- Foregaende ar (for retention)

### Las-mekanism

Anvander `analytics_cron_runs` for att:
- Forhindra parallella korningar
- Spara status och loggar
- Hantera force-mode

---

## GDPR & SEKRETESS

### Publika Insikter
**URL:** `/pages/insights.php`

Visar aggregerad statistik utan persondata:
- Segment med < 10 deltagare doljs
- Inga personnamn
- Endast statistiska trender

---

## DATAKVALITET

### Identity Resolution
Hanterar dubbletter via `rider_merge_map`:
- Canonical rider ID
- Merged riders pekar till canonical
- Audit-logg i `rider_identity_audit`

### Rookie-berakning
En rider ar "rookie" om:
- Forsta forekomst i rider_yearly_stats for det aret
- Ingen tidigare sasong registrerad

### Retention-berakning
En rider ar "retained" om:
- Finns i rider_yearly_stats for bade ar X och ar X-1

---

## TEKNISK INFORMATION

### Dependencies
- PHP 8.0+
- MySQL/MariaDB
- Chart.js (CDN)
- Lucide Icons

### Performance
- Bulk SQL for stora berakningar
- Pre-beraknade tabeller for snabb lasing
- Index pa rider_id, season_year, series_id

### Cache
- Inga cache-lager (litar pa pre-beraknade tabeller)
- Cron-refresh dagligen

---

## FRAMTIDA UTVECKLING

### Planerat
- [ ] Geografisk analys (var kommer riders ifran?)
- [ ] Rookie-statistik pa klubbsidor
- [ ] "Ny deltagar"-badge pa rider-profiler
- [ ] Integration med publik insights-sida

### Overvag
- [ ] Predictive churn (ML)
- [ ] Automated win-back emails
- [ ] Real-time dashboards

---

*Senast uppdaterad: 2026-01-14*
