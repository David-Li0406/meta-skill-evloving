# GravitySeries Rankingsystem

## Översikt

Rankingsystemet beräknar tre separata rankingar baserat på resultaten från de senaste 24 månaderna:
- **Enduro** - endast Enduro-event
- **Downhill (DH)** - endast Downhill-event
- **Gravity** - kombinerad ranking (Enduro + DH)

## Rankingformel

```
Rankingpoäng = Originalpoäng × Fältstorlek-multiplikator × Eventnivå-multiplikator × Tidsmultiplikator
```

### 1. Originalpoäng
Poäng från eventets poängmall baserat på placering (t.ex. 1:a plats = 100p, 2:a plats = 95p, etc.)

### 2. Fältstorlek-multiplikator
Poäng viktas efter antal deltagare i klassen:

| Deltagare | Multiplikator |
|-----------|---------------|
| 1         | 0.75          |
| 2         | 0.77          |
| 3         | 0.79          |
| ...       | ...           |
| 14        | 0.99          |
| 15+       | 1.00          |

**Exempel:** 1:a plats (100p) i fält på 15+ deltagare = 100p × 1.00 = 100p
**Exempel:** 1:a plats (100p) i fält på 5 deltagare = 100p × 0.83 = 83p

### 3. Eventnivå-multiplikator
Olika multiplikatorer beroende på eventtyp:

| Eventnivå  | Multiplikator | Justerbar |
|------------|---------------|-----------|
| National   | 100% (1.00)   | Ja        |
| Sportmotion| 50% (0.50)    | Ja        |

**Exempel:** National event: 100p × 1.00 = 100p
**Exempel:** Sportmotion event: 100p × 0.50 = 50p

### 4. Tidsmultiplikator (24-månaders rullande fönster)
Poäng viktning baserat på hur gammalt resultatet är:

| Period       | Multiplikator | Viktning |
|--------------|---------------|----------|
| 0-12 månader | 100% (1.00)   | Full     |
| 13-24 månader| 50% (0.50)    | Halv     |
| 25+ månader  | 0% (0.00)     | Ingen    |

**Exempel:** Resultat från 6 månader sedan: 100p × 1.00 = 100p
**Exempel:** Resultat från 18 månader sedan: 100p × 0.50 = 50p
**Exempel:** Resultat från 26 månader sedan: 100p × 0.00 = 0p (räknas inte)

## Komplett Exempel

**Scenario:** Åkare vinner (1:a plats, 100p) ett Sportmotion Enduro-event för 8 månader sedan i ett fält på 12 deltagare.

**Beräkning:**
```
Rankingpoäng = 100p × 0.95 × 0.50 × 1.00
             = 100p × 0.95 (12 deltagare)
             × 0.50 (Sportmotion)
             × 1.00 (0-12 månader)
             = 47.5p
```

## Automatisk Uppdatering

Rankingen uppdateras automatiskt **den 1:a varje månad kl 02:00** via ett cronjobb.

**Cron-schema:**
```bash
0 2 1 * * /usr/bin/php /path/to/TheHUB/cron/ranking_update.php
```

Detta säkerställer att:
- Tidsmultiplikatorn uppdateras korrekt (äldre resultat får lägre vikt)
- Resultat äldre än 24 månader tas bort från rankingen
- Nya resultat från senaste månaden inkluderas

## Klubbranking

Klubbrankingen beräknas genom att summera alla åkares rankingpoäng i varje klubb.

## Teknisk Implementation

- **Beräkning:** Live-beräkning från `results` tabellen (ingen mellanlagring)
- **Snapshots:** Månatliga snapshots sparas i `ranking_snapshots` för historik
- **Kod:** `includes/ranking_functions.php`
- **Cron:** `cron/ranking_update.php`
- **Visning:** `pages/ranking.php`

## Inställningar

Multipliktatorerna kan justeras i admin-gränssnittet:
- Fältstorlek-multiplikatorer: `/admin/ranking.php?tab=field_multipliers`
- Eventnivå-multiplikatorer: `/admin/ranking.php?tab=event_levels`
- Tidsmultiplikatorer: `/admin/ranking.php?tab=time_decay`

## Viktiga Anteckningar

1. **Seriepoäng vs Rankingpoäng:** Dessa är SEPARATA system
   - Seriepoäng: Lagras i `series_results`, används för serietabeller
   - Rankingpoäng: Beräknas live från `results.points`, används för rankingen

2. **Klassbegränsningar:** Endast klasser med `awards_points=1` och `series_eligible=1` räknas

3. **E-bikes:** Får inga rankingpoäng (is_ebike=1)

4. **Statusfilter:** Endast resultat med `status='finished'` räknas
