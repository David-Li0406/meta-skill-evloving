---
name: seo-content-writer
description: Creates SEO-optimized pillar content based on NeuronWriter briefs. Handles keyword integration, content structure, meta tags, and semantic optimization. Produces long-form articles (2000-5000 words) following Topic Cluster strategy. Use when creating new SEO articles from keyword research.
---

# SEO Content Writer

Erstellt SEO-optimierte Pillar-Artikel basierend auf Keyword-Recherche und NeuronWriter-Briefs.

## Quick Start

```
Input: NeuronWriter Brief + Keywords + Zielgruppe
Output: SEO-Artikel (Markdown) + Meta-Tags + Struktur-Empfehlungen
```

## Workflow

1. **Brief analysieren** → Keywords, Suchintent, Wettbewerb verstehen
2. **Struktur planen** → Outline basierend auf Top-Ranking-Content
3. **Content schreiben** → SEO-optimiert aber lesbar
4. **Keywords integrieren** → Natürlich, nicht stuffed
5. **Meta-Tags erstellen** → Title, Description, OG-Tags
6. **Qualität prüfen** → SEO-Score, Lesbarkeit, Keyword-Dichte

## Output Format

```json
{
  "article": {
    "title": "SEO-optimierter Titel",
    "slug": "seo-optimierter-slug",
    "meta_description": "155 Zeichen Beschreibung mit Keyword",
    "content": "# Markdown Content...",
    "word_count": 2500,
    "reading_time": "12 min",
    "structure": {
      "h1": "Haupttitel",
      "h2_count": 8,
      "h3_count": 15
    }
  },
  "seo": {
    "primary_keyword": "Content Marketing",
    "secondary_keywords": ["Content Strategie", "Marketing Tipps"],
    "keyword_density": {
      "primary": "1.2%",
      "secondary": ["0.8%", "0.6%"]
    },
    "internal_links_suggested": 5,
    "external_links": 3
  },
  "meta_tags": {
    "title_tag": "Content Marketing Guide 2024 | [Brand]",
    "og_title": "Content Marketing: Der ultimative Guide",
    "og_description": "...",
    "twitter_card": "summary_large_image"
  }
}
```

## Content-Typen

| Typ | Wortanzahl | Struktur | Ziel |
|-----|------------|----------|------|
| Pillar Page | 3000-5000 | Umfassend, viele H2/H3 | Topic Authority |
| Cluster Article | 1500-2500 | Fokussiert, tiefgehend | Long-Tail Keywords |
| How-To Guide | 2000-3000 | Schritte, Listen, Bilder | Informational Intent |
| Comparison | 2000-3500 | Tabellen, Pro/Contra | Commercial Intent |
| Listicle | 1500-2500 | Nummeriert, scannable | Traffic + Shares |

Details: [CONTENT_TYPES.md](CONTENT_TYPES.md)

## SEO Best Practices

### Keyword-Integration

```
Title Tag:        Keyword am Anfang
H1:               Keyword enthalten
Erste 100 Wörter: Keyword natürlich platziert
H2s:              2-3x Keyword-Variationen
Content:          1-2% Density (nicht mehr!)
Meta Description: Keyword + CTA
URL/Slug:         Keyword (kurz)
Alt-Texte:        Beschreibend + Keyword
```

### Content-Struktur

```
Ideale Struktur:
├── H1 (1x - Titel)
├── Intro (Hook + Keyword + Was erwartet den Leser)
├── H2 (Was ist [Thema]?)
│   ├── H3 Definition
│   └── H3 Warum wichtig
├── H2 (Hauptteil 1)
│   ├── H3 Unterpunkt
│   └── H3 Unterpunkt
├── H2 (Hauptteil 2)
│   └── ...
├── H2 (Praxis/Beispiele)
├── H2 (FAQ) ← Schema Markup
└── H2 (Fazit + CTA)
```

Details: [CONTENT_STRUCTURE.md](CONTENT_STRUCTURE.md)

### Lesbarkeit

```
Satzlänge:      Max 20 Wörter (Durchschnitt 15)
Absatzlänge:    Max 3-4 Sätze
Flesch-Index:   60+ (leicht verständlich)
Aktive Sprache: 80%+ aktive Sätze
Fachbegriffe:   Erklären oder verlinken
```

## NeuronWriter Integration

### Brief-Analyse

```
Aus NeuronWriter-Brief extrahieren:
1. Primary Keyword + Search Volume
2. Secondary Keywords (5-10)
3. Questions (für FAQ)
4. Wettbewerber-Analyse
5. Content Score Ziel
6. Empfohlene Wortanzahl
```

### Während des Schreibens

```
NeuronWriter prüft:
- Keyword-Abdeckung
- Content Score
- Semantische Begriffe
- Wettbewerber-Vergleich
→ Live-Feedback während der Erstellung
```

## Topic Cluster Strategie

Details: [TOPIC_CLUSTERS.md](TOPIC_CLUSTERS.md)

### Pillar-Cluster Beziehung

```
Pillar Page: /content-marketing-guide
├── Cluster: /content-strategie-entwickeln
│   └── Links zurück zu Pillar
├── Cluster: /blog-artikel-schreiben
│   └── Links zurück zu Pillar
├── Cluster: /content-distribution
│   └── Links zurück zu Pillar
└── Pillar verlinkt zu allen Clustern
```

### Linking-Regeln

```
Pillar Page:
- Verlinkt zu ALLEN Cluster-Artikeln
- Erhält Links von ALLEN Cluster-Artikeln
- 5-10 interne Links zu anderen Pillars

Cluster Article:
- MUSS zu Pillar verlinken (früh im Text)
- Verlinkt zu verwandten Clustern
- 3-5 interne Links gesamt
```

## E-E-A-T Signale

### Experience (Erfahrung)

```
Zeigen durch:
- Eigene Beispiele / Case Studies
- "In unserer Erfahrung..."
- Screenshots eigener Projekte
- Konkrete Zahlen aus eigener Arbeit
```

### Expertise

```
Zeigen durch:
- Tiefgehendes Fachwissen
- Aktuelle Informationen
- Quellenangaben
- Autor-Bio mit Credentials
```

### Authoritativeness

```
Zeigen durch:
- Zitate von Experten
- Backlinks von Authority Sites
- Erwähnungen in Medien
- Branchenauszeichnungen
```

### Trustworthiness

```
Zeigen durch:
- Transparente Quellenarbeit
- Aktuelles Datum / Updates
- Kontaktmöglichkeiten
- Impressum / Datenschutz
```

## Schema Markup

### Empfohlene Schemas

```json
{
  "@type": "Article",
  "headline": "...",
  "author": {...},
  "datePublished": "...",
  "dateModified": "..."
}

{
  "@type": "FAQPage",
  "mainEntity": [...]
}

{
  "@type": "HowTo",
  "step": [...]
}
```

## Checkliste

### Vor dem Schreiben
- [ ] NeuronWriter-Brief analysiert?
- [ ] Suchintent verstanden?
- [ ] Top 5 Wettbewerber gelesen?
- [ ] Outline erstellt?
- [ ] Unique Angle identifiziert?

### Beim Schreiben
- [ ] Keyword in Title, H1, Intro?
- [ ] Struktur klar (H2/H3)?
- [ ] Absätze kurz (<4 Sätze)?
- [ ] Aktive Sprache?
- [ ] Beispiele/Daten integriert?

### Nach dem Schreiben
- [ ] NeuronWriter Score >80?
- [ ] Meta Description geschrieben?
- [ ] Interne Links gesetzt?
- [ ] Bilder mit Alt-Text?
- [ ] FAQ Schema vorbereitet?
