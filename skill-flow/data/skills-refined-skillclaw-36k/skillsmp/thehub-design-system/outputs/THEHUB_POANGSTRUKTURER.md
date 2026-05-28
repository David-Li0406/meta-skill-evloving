# TheHUB - Komplett Poängstruktur

## Översikt

TheHUB använder tre parallella poängsystem som fungerar oberoende av varandra men kompletterar varandra:

1. **SERIER** - Event-baserade poäng per specifik serie
2. **RANKING** - Globalt rankingsystem för alla event (rullande 24 månader)
3. **KLUBBPOÄNG** - Finns i två varianter: per serie OCH global ranking

**Kritisk distinktion:** Seriepoäng ≠ Rankingpoäng. Detta är två separata system med olika syften och beräkningsregler.

---

## 1. SERIER (Event-baserade, per serie)

### 1.1 Individuell serieställning

Serier är event-baserade tävlingsserier där endast specifika event ingår i varje serie.

#### Administration
- **Admin-sida:** `/admin/series-events.php?series_id=X`
- **Bestämmer:**
  - Vilka event som ingår i serien
  - Hur många event som räknas ("bästa X resultat av Y")
  - Vilken poängmall som används för seriepoäng

#### Beräkning
- **Metod:** Strikt event-baserad enligt seriens valda poängmall
- **Omfattning:** Endast event som är kopplade till den specifika serien
- **Tidsram:** Per säsong (vanligtvis ett kalenderår)
- **Exempel:** Om en serie använder "bästa 4 av 6 event" räknas endast de 4 bästa resultaten från dessa specifika 6 event

#### Exempel på serier
- **GravitySeries Enduro** - Nationell serie, bästa 4 av 6 event
- **Capital GravitySeries** - Regional serie Stockholm, bästa 3 event
- **Götaland GravitySeries** - Regional serie Göteborg, bästa 3 event
- **GravitySeries Total** - Summering av alla nationella event

### 1.2 Klubbpoäng per serie

Varje serie genererar sin egen klubbranking baserad på seriepoäng.

#### Beräkningsregel
För varje klass i varje event som ingår i serien:
- **Bästa åkaren från klubben:** 100% av sina seriepoäng → klubben
- **Näst bästa åkaren från klubben:** 50% av sina seriepoäng → klubben
- **Övriga åkare från klubben:** 0% (räknas inte)

#### Resultat
- Varje serie får sin **egen separata klubbranking**
- Baseras på **seriepoäng** (inte rankingpoäng)
- Uppdateras när serieresultat publiceras

#### Exempel
**GravitySeries Enduro - Klubbpoäng:**
- Klubb A: Bästa åkare har 250 seriepoäng + näst bästa har 180 seriepoäng
- Klubbpoäng = 250 × 100% + 180 × 50% = 250 + 90 = **340 poäng**

---

## 2. RANKING (Globalt, alla event, rullande 24 månader)

Ranking är ett globalt system som omfattar **ALLA event** oavsett vilken serie de tillhör eller om de ens ingår i någon serie.

### 2.1 Event-reglemente

#### Administration
- **Admin-sida:** `/admin/series.php?edit=X` (när du editerar ett enskilt event)
- **Bestämmer:** Vilket reglemente eventet har

#### Reglemente-typer
- **Nationellt reglemente** → Ger rankingpoäng enligt nationell poängtabell
- **Sportmotion reglemente** → Ger rankingpoäng enligt sportmotion-poängtabell

#### Viktigt att förstå
- Reglementet är kopplat till **EVENTET**, inte serien
- Ett event kan ingå i en serie MEN ha sitt eget reglemente för ranking
- Alla event (med eller utan serie-koppling) kan ge rankingpoäng

### 2.2 Individuellt ranking

#### Omfattning
- **ALLA event räknas in** oavsett:
  - Vilken serie de tillhör
  - Om de tillhör någon serie alls
  - Om det är nationella, regionala eller lokala event

#### Poängberäkning
- Bestäms av **eventets reglemente** (nationellt/sportmotion)
- Olika poängtabeller ger olika poäng för samma placering

#### Tidsram - Rullande 24 månader
Rankingpoäng har ett automatiskt avskrivningssystem:

| Ålder på resultat | Vikt | Beskrivning |
|-------------------|------|-------------|
| Månad 1-12 | **100%** | Full poäng under första året |
| Månad 13-24 | **50%** | Halva poängen under andra året |
| Månad 25+ | **0%** | Poängen försvinner helt |

#### Uppdatering
- **Automatisk avräkning:** Den 1:a varje månad
- Äldre resultat får lägre vikt
- Efter 24 månader försvinner resultatet helt från ranking

#### Exempel
**En åkares ranking över tid:**
- April 2024: Vinner event → 100 rankingpoäng (100%)
- April 2025: Samma resultat → 50 rankingpoäng (50%)
- April 2026: Samma resultat → 0 rankingpoäng (försvinner)

### 2.3 Klubbranking (global)

#### Omfattning
- Baseras på **ALLA event från ALLA serier**
- Inkluderar även event som inte ingår i någon serie

#### Beräkning
- **Summan av alla åkarnas individuella rankingpoäng per klubb**
- Varje åkares fullständiga rankingpoäng (efter 24-månadersavskrivning) räknas
- Ingen 100%/50%-regel här - alla åkares poäng räknas fullt ut

#### Tidsram
- Samma **rullande 24-månadersregel** som individuellt ranking
- Automatisk uppdatering den 1:a varje månad

#### Exempel
**Klubb X har 3 aktiva åkare:**
- Åkare A: 450 rankingpoäng
- Åkare B: 320 rankingpoäng
- Åkare C: 180 rankingpoäng
- **Total klubbranking = 450 + 320 + 180 = 950 poäng**

---

## 3. KLUBBPOÄNG - SAMMANFATTNING

Klubbpoäng existerar i **TVÅ separata varianter** som fungerar parallellt:

### 3.1 Klubbpoäng per serie

| Aspekt | Beskrivning |
|--------|-------------|
| **Bas** | Seriepoäng från event i specifik serie |
| **Omfattning** | Endast event som ingår i den serien |
| **Regel** | 100% för bästa åkaren + 50% för näst bästa per klass |
| **Tidsram** | Per säsong |
| **Resultat** | Varje serie får sin egen klubbranking |

### 3.2 Global klubbranking

| Aspekt | Beskrivning |
|--------|-------------|
| **Bas** | Rankingpoäng från alla event |
| **Omfattning** | Alla event från alla serier |
| **Regel** | Summa av alla åkarnas rankingpoäng |
| **Tidsram** | Rullande 24 månader |
| **Resultat** | En global klubbranking |

---

## 4. KRITISKA SKILLNADER

### 4.1 Seriepoäng vs Rankingpoäng

| Aspekt | Seriepoäng | Rankingpoäng |
|--------|------------|--------------|
| **Källa** | Bestäms av seriens poängmall | Bestäms av eventets reglemente |
| **Admin-sida** | `/admin/series-events.php` | `/admin/series.php?edit=X` |
| **Omfattning** | Endast event i just den serien | ALLA event oavsett serie |
| **Tidsram** | Per säsong | Rullande 24 månader med avskrivning |
| **Poängmall** | Seriens valda poängmall | Event-reglemente (nationellt/sportmotion) |
| **Används för** | Serietabell + klubbpoäng per serie | Individuellt ranking + global klubbranking |
| **Avskrivning** | Ingen (gäller hela säsongen) | Automatisk efter 12 och 24 månader |

### 4.2 Klubbpoäng - Två system

| Typ | Bas | Omfattning | Beräkningsregel | Tidsram |
|-----|-----|------------|-----------------|---------|
| **Per serie** | Seriepoäng | Event i specifik serie | 100% + 50% per klass | Per säsong |
| **Global ranking** | Rankingpoäng | Alla event från alla serier | Summa av alla åkares poäng | Rullande 24 mån |

---

## 5. ADMIN-SIDOR OCH FUNKTIONER

### 5.1 Serie-administration
**URL:** `/admin/series-events.php?series_id=X`

**Funktioner:**
- Koppla event till serier
- Bestämma "bästa X av Y"-regler
- Välja poängmall för seriepoäng
- Konfigurera seriespecifika inställningar

### 5.2 Event-administration
**URL:** `/admin/series.php?edit=X`

**Funktioner:**
- Sätta event-reglemente (nationellt/sportmotion)
- Bestämma rankingpoäng-tabell
- Konfigurera event-specifika inställningar
- Kopiera inställningar från tidigare event

### 5.3 Resultatadministration
**URL:** `/admin/event-results.php?event_id=X`

**Funktioner:**
- Registrera resultat per klass
- Automatisk beräkning av både seriepoäng och rankingpoäng
- Publicera resultat (uppdaterar alla poängsystem)

---

## 6. TEKNISK ÖVERSIKT

### 6.1 Databastabeller (förenklad översikt)

```
series
├── series_id
├── series_name
└── points_template_id → Bestämmer seriepoäng-mall

series_events
├── series_id → Kopplar event till serie
├── event_id
└── best_of_rule → "Bästa X av Y"

events
├── event_id
├── event_name
├── event_date
└── regulation_type → "national" eller "sportmotion" (för ranking)

event_results
├── result_id
├── event_id
├── rider_id
├── class_id
├── position
├── series_points → Beräknas från seriens poängmall
└── ranking_points → Beräknas från eventets reglemente

rider_ranking (cache-tabell)
├── rider_id
├── total_ranking_points → Summa alla rankingpoäng (24 mån)
└── last_updated

club_ranking_series (per serie)
├── club_id
├── series_id
└── total_points → Beräknat med 100%/50%-regeln

club_ranking_global (global)
├── club_id
└── total_ranking_points → Summa alla åkares rankingpoäng
```

### 6.2 Beräkningsflöde

#### När ett resultat publiceras:

1. **Seriepoäng beräknas:**
   - Kollar om eventet ingår i någon serie
   - Använder seriens poängmall
   - Sparar i `event_results.series_points`

2. **Rankingpoäng beräknas:**
   - Kollar eventets reglemente-typ
   - Använder motsvarande poängtabell
   - Sparar i `event_results.ranking_points`

3. **Klubbpoäng per serie uppdateras:**
   - För varje serie eventet ingår i
   - Tillämpar 100%/50%-regeln per klass
   - Uppdaterar `club_ranking_series`

4. **Global klubbranking uppdateras:**
   - Summerar alla åkares rankingpoäng
   - Tillämpar 24-månadersavskrivning
   - Uppdaterar `club_ranking_global`

---

## 7. VISUALISERING

```
┌─────────────────────────────────────────────────────────────────┐
│                          ALLA EVENT                              │
│  (Nationella, regionala, lokala - med eller utan serie)         │
└────────────────┬───────────────────────────┬────────────────────┘
                 │                           │
                 ▼                           ▼
    ┌────────────────────────┐  ┌──────────────────────────┐
    │   EVENT-REGLEMENTE     │  │   SERIE-KOPPLING         │
    │   (per event)          │  │   (per serie)            │
    ├────────────────────────┤  ├──────────────────────────┤
    │ • Nationellt           │  │ • GravitySeries Enduro   │
    │ • Sportmotion          │  │ • Capital GravitySeries  │
    │                        │  │ • Götaland GravitySeries │
    │ Bestäms i:             │  │ • etc.                   │
    │ /admin/series.php      │  │                          │
    │        ?edit=X         │  │ Bestäms i:               │
    │                        │  │ /admin/series-events.php │
    └───────────┬────────────┘  └─────────────┬────────────┘
                │                             │
                ▼                             ▼
    ┌────────────────────────┐  ┌──────────────────────────┐
    │   RANKINGPOÄNG         │  │   SERIEPOÄNG             │
    │   (Globalt system)     │  │   (Per serie)            │
    ├────────────────────────┤  ├──────────────────────────┤
    │ • ALLA event räknas    │  │ • Endast event i serien  │
    │ • Rullande 24 mån      │  │ • Per säsong             │
    │ • 100%/50%/0% vikt     │  │ • Bästa X av Y           │
    │                        │  │                          │
    │ Används för:           │  │ Används för:             │
    │ ✓ Individuellt ranking │  │ ✓ Serietabell            │
    │ ✓ Global klubbranking  │  │ ✓ Klubbpoäng per serie   │
    └────────────────────────┘  └──────────────────────────┘
                │                             │
                │                             │
                ▼                             ▼
    ┌────────────────────────┐  ┌──────────────────────────┐
    │  GLOBAL KLUBBRANKING   │  │  KLUBBPOÄNG PER SERIE    │
    ├────────────────────────┤  ├──────────────────────────┤
    │ Summa av alla åkarnas  │  │ Bästa åkare: 100%        │
    │ rankingpoäng per klubb │  │ Näst bästa: 50%          │
    │                        │  │ (per klass i serien)     │
    │ • Rullande 24 månader  │  │                          │
    │ • Alla event räknas    │  │ • Per säsong             │
    │                        │  │ • Varje serie separat    │
    └────────────────────────┘  └──────────────────────────┘
```

---

## 8. VANLIGA MISSFÖRSTÅND (KORRIGERADE)

### ❌ FEL: "Ranking är kopplat till GravitySeries Total"
**✅ RÄTT:** Ranking är ett globalt system som omfattar ALLA event oavsett serie. GravitySeries Total är bara en av många serier som använder seriepoäng.

### ❌ FEL: "Ranking beror på vilka serier event ingår i"
**✅ RÄTT:** Ranking bestäms av eventets reglemente (nationellt/sportmotion), inte av serie-koppling. Ett event utan serie-koppling kan ge rankingpoäng.

### ❌ FEL: "Klubbpoäng är ett enda system"
**✅ RÄTT:** Klubbpoäng finns i två varianter:
- Per serie (baserat på seriepoäng, 100%/50%-regel)
- Global ranking (baserat på rankingpoäng, summa av alla åkare)

### ❌ FEL: "Seriepoäng och rankingpoäng är samma sak"
**✅ RÄTT:** Två helt separata system:
- Seriepoäng: Per serie, seriens poängmall, per säsong
- Rankingpoäng: Globalt, event-reglemente, rullande 24 månader

---

## 9. PRAKTISKA EXEMPEL

### Exempel 1: En åkare tävlar i ett event

**Event:** GravitySeries Enduro - Tävling 3, Åre
**Åkare:** Anna från Klubb Stockholm
**Klass:** Elite Women
**Placering:** 2:a plats

#### Vad händer?

**1. Seriepoäng (för GravitySeries Enduro):**
- Eventet ingår i GravitySeries Enduro
- Serien använder sin poängmall: 2:a plats = 80 seriepoäng
- Anna får **80 seriepoäng** i GravitySeries Enduro
- Dessa räknas för hennes serieställning (om det är bland hennes bästa 4 av 6)

**2. Rankingpoäng (globalt):**
- Eventet har "nationellt reglemente"
- Nationell poängtabell: 2:a plats Elite = 95 rankingpoäng
- Anna får **95 rankingpoäng** för sitt globala ranking
- Dessa poäng gäller i 24 månader (100% i 12 mån, 50% i 12 mån)

**3. Klubbpoäng för GravitySeries Enduro:**
- Om Anna är bästa från Klubb Stockholm i Elite Women: 80 × 100% = 80p
- Om Anna är näst bästa från Klubb Stockholm i Elite Women: 80 × 50% = 40p

**4. Global klubbranking:**
- Annas 95 rankingpoäng läggs till Klubb Stockholms totala ranking
- Summan av alla medlemmars rankingpoäng = klubbens globala ranking

### Exempel 2: Jämförelse mellan två event

| Aspekt | Event A: GS Enduro Åre | Event B: Lokalt race utan serie |
|--------|------------------------|----------------------------------|
| **Ingår i serie** | Ja (GravitySeries Enduro) | Nej |
| **Seriepoäng** | Ja (enligt seriens mall) | Nej (ingen serie-koppling) |
| **Event-reglemente** | Nationellt | Sportmotion |
| **Rankingpoäng** | Ja (nationell tabell) | Ja (sportmotion-tabell) |
| **Klubbpoäng per serie** | Ja (GS Enduro klubbranking) | Nej |
| **Global klubbranking** | Ja (via rankingpoäng) | Ja (via rankingpoäng) |

**Slutsats:** Även event utan serie-koppling bidrar till ranking och global klubbranking!

---

## 10. SAMMANFATTNING

TheHUBs poängstruktur bygger på tre oberoende men kompletterande system:

### 🏆 SERIER
- Event-baserade per specifik serie
- Seriepoäng enligt seriens poängmall
- Klubbpoäng per serie (100%/50%-regel)
- Tidsram: Per säsong

### 📊 RANKING
- Globalt system för ALLA event
- Rankingpoäng enligt event-reglemente
- Rullande 24 månader med avskrivning
- Global klubbranking (summa av åkares poäng)

### 👥 KLUBBPOÄNG
- **Variant 1:** Per serie (seriepoäng, 100%/50%)
- **Variant 2:** Global (rankingpoäng, summa)

### 🔑 Nyckelinsikter
1. Seriepoäng ≠ Rankingpoäng (två separata beräkningar)
2. Event-reglemente bestämmer ranking (inte serie-koppling)
3. Klubbpoäng finns i två varianter
4. Alla event kan ge rankingpoäng (även utan serie)
5. Ranking är rullande 24 månader, serier är per säsong

---

**Dokumentet uppdaterat:** 2025-11-25
**Författare:** TheHUB Development Team
**Syfte:** Officiell referens för TheHUBs poängstrukturer
