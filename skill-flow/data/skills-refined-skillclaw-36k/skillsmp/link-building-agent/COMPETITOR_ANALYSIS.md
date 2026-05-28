# Competitor Link Analysis

## Übersicht

```
Ziel: Verstehen, woher Konkurrenten ihre Links bekommen,
      und replizierbare Strategien identifizieren.
```

---

## 1. Konkurrenten identifizieren

### Methoden

**SEO-Konkurrenten (wichtiger als Business-Konkurrenten):**
```
1. Keywords identifizieren, für die du ranken willst
2. Wer rankt auf Seite 1 für diese Keywords?
3. Diese sind deine SEO-Konkurrenten

Tools:
- Ahrefs → Organic Competitors
- SEMrush → Organic Competitors
- Google Suche → Top 10 analysieren
```

### Konkurrenten-Matrix

| Konkurrent | Domain | DA | Keywords | Überlappung |
|------------|--------|----|-----------| ------------|
| [Name 1] | competitor1.com | 65 | 5.000 | Hoch |
| [Name 2] | competitor2.com | 58 | 3.200 | Hoch |
| [Name 3] | competitor3.com | 72 | 8.500 | Mittel |
| [Name 4] | competitor4.com | 45 | 1.800 | Mittel |
| [Name 5] | competitor5.com | 51 | 2.100 | Niedrig |

---

## 2. Backlink-Profile exportieren

### Ahrefs Export

```
Site Explorer → [Domain] → Backlinks

Filter:
- Dofollow only
- One link per domain
- DR > 20

Export: Full export (CSV)
```

### SEMrush Export

```
Backlink Analytics → [Domain]

Filter:
- Active links
- Follow links
- Authority Score > 20

Export: Full export
```

### Daten pro Konkurrent

```
Zu sammeln:
- Total Referring Domains
- Total Backlinks
- Backlinks by Type (text, image, redirect)
- Top Referring Domains (Top 100)
- Anchor Text Distribution
- Link Velocity (neue Links/Monat)
```

---

## 3. Link Gap Analysis

### Konzept

```
Link Gap = Links, die zu Konkurrenten zeigen,
           aber nicht zu dir

Diese sind die wertvollsten Opportunities!
```

### Ahrefs Link Intersect

```
1. More → Link Intersect
2. Show links to: Konkurrent 1, 2, 3 (bis zu 10)
3. But don't link to: Deine Domain
4. Filter: One link per domain

Ergebnis: Domains, die zu mehreren Konkurrenten verlinken
```

### Analyse-Template

| Referring Domain | Links zu K1 | Links zu K2 | Links zu K3 | DA | Opportunity |
|------------------|-------------|-------------|-------------|----|----|
| example.com | ✅ | ✅ | ✅ | 65 | Hoch |
| blog.com | ✅ | ✅ | ❌ | 52 | Mittel |
| news.de | ❌ | ✅ | ✅ | 71 | Hoch |

### Priorisierung

```
Hohe Priorität:
- Links zu 3+ Konkurrenten
- DA > 50
- Thematisch relevant

Mittlere Priorität:
- Links zu 2 Konkurrenten
- DA 30-50

Niedrige Priorität:
- Links zu 1 Konkurrent
- DA < 30
- Wenig relevant
```

---

## 4. Strategie-Reverse-Engineering

### Was analysieren?

**Content-Typen mit meisten Links:**
```
Ahrefs → Best by Links

Was fällt auf?
- Welche Content-Typen bekommen Links? (Guides, Tools, Data)
- Welche Themen performen?
- Welche Formate (Infografiken, Videos)?
```

**Link-Quellen-Typen:**
```
Kategorisiere Top 50 Referring Domains:
- Guest Posts (%)
- Resource Pages (%)
- News/PR (%)
- Directories (%)
- Forums/Communities (%)
- Education (.edu) (%)
- Government (.gov) (%)
```

**Anchor Text Analyse:**
```
Ahrefs → Anchors

Verteilung analysieren:
- Branded (%)
- Exact Match (%)
- Partial Match (%)
- Generic (%)
- Naked URL (%)

Vergleiche mit deiner Distribution
```

---

## 5. Replizierbare Strategien identifizieren

### Strategie-Matrix

| Strategie | Konkurrent 1 | Konkurrent 2 | Replizierbar? | Aufwand |
|-----------|--------------|--------------|---------------|---------|
| Guest Posting | 30% | 25% | Ja | Mittel |
| PR/News | 20% | 15% | Ja | Hoch |
| Resource Pages | 15% | 20% | Ja | Niedrig |
| Infografiken | 10% | 5% | Ja | Mittel |
| Directories | 5% | 10% | Ja | Niedrig |
| .edu Links | 10% | 8% | Schwer | Hoch |

### Action Items

```
Basierend auf Analyse:

1. Guest Posting ist Hauptstrategie der Konkurrenz
   → Identifiziere 20 Publikationen, die K1 + K2 akzeptiert haben
   → Pitche eigene Artikel

2. K2 hat starke Resource Page Links
   → Finde diese Resource Pages
   → Pitche eigenen Content

3. K1 hat PR-Coverage auf News-Sites
   → Analysiere, welche Stories Coverage bekommen haben
   → Entwickle ähnliche Story Angles
```

---

## 6. Link Velocity Tracking

### Was ist Link Velocity?

```
Link Velocity = Neue Referring Domains pro Zeiteinheit
                (typisch: pro Monat)

Wichtig für:
- Wettbewerbs-Benchmarking
- Eigenes Ziel-Setting
- Erkennen von Link-Building-Kampagnen
```

### Tracking-Setup

```
Monatlich tracken für jeden Konkurrenten:
- Neue Referring Domains
- Verlorene Referring Domains
- Netto-Veränderung
- DA-Veränderung
```

### Velocity-Vergleich

| Monat | Deine Domain | K1 | K2 | K3 |
|-------|--------------|-----|-----|-----|
| Jan | +8 | +15 | +12 | +5 |
| Feb | +10 | +18 | +10 | +7 |
| März | +12 | +20 | +14 | +8 |
| Trend | ↑ | ↑↑ | ↑ | → |

### Insights

```
Wenn K1 plötzlich +50 Links/Monat hat:
→ Neue Link-Building-Kampagne?
→ Viral Content?
→ PR-Push?

Analysiere NEUE Links des Monats, um Strategie zu verstehen
```

---

## 7. Opportunity Scoring

### Formel

```
Opportunity Score =
  (Links zu Konkurrenten × 0.25) +
  (DA × 0.25) +
  (Traffic × 0.15) +
  (Relevanz × 0.20) +
  (Kontaktierbarkeit × 0.15)
```

### Scoring-Beispiel

| Domain | Links K | DA | Traffic | Relevanz | Kontakt | Score |
|--------|---------|-----|---------|----------|---------|-------|
| site-a.com | 3 | 65 | 50k | Hoch | Email | 0.87 |
| site-b.com | 2 | 45 | 20k | Mittel | Form | 0.62 |
| site-c.com | 1 | 72 | 100k | Hoch | Keine | 0.55 |

### Priorisierung

```
Score 0.8+: Sofort kontaktieren (Tier A)
Score 0.6-0.8: In der nächsten Woche (Tier B)
Score 0.4-0.6: Bei Kapazität (Tier C)
Score <0.4: Nicht priorisieren
```

---

## 8. Report Template

### Monatlicher Competitor Link Report

```markdown
# Competitor Link Analysis - [Monat] [Jahr]

## Executive Summary
- Wichtigste Insights
- Top Opportunities
- Empfohlene Actions

## Link Metrics Vergleich

| Metrik | Wir | K1 | K2 | K3 |
|--------|-----|----|----|-----|
| Referring Domains | | | | |
| Link Velocity | | | | |
| DA | | | | |

## Link Gap Analysis
- X Domains verlinken zu 2+ Konkurrenten, aber nicht zu uns
- Top 10 Opportunities: [Liste]

## Strategie-Insights
- K1 Hauptstrategie: [Beschreibung]
- K2 Hauptstrategie: [Beschreibung]
- Replizierbare Taktiken: [Liste]

## Action Items
1. [Action 1]
2. [Action 2]
3. [Action 3]

## Nächster Review: [Datum]
```
