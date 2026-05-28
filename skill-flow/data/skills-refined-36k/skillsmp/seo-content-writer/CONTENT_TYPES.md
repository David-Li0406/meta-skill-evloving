# Content-Typen für SEO

## 1. Pillar Page (Cornerstone Content)

### Beschreibung
Umfassender, autoritativer Guide zu einem Hauptthema. Dient als Hub für Topic Cluster.

### Spezifikationen

```
Wortanzahl:     3.000 - 5.000+
Struktur:       10-15 H2 Sections
H3 pro H2:      2-4
Interne Links:  10-20 (zu Cluster-Artikeln)
Externe Links:  5-10 (Authority Sources)
Bilder:         10-20 (inkl. Infografiken)
```

### Aufbau

```markdown
# [Hauptkeyword]: Der ultimative Guide [Jahr]

## Quick Navigation / Inhaltsverzeichnis

## Was ist [Thema]? (Definition)
- Kurze, klare Definition
- Warum es wichtig ist
- Kurze Geschichte/Entwicklung

## Warum [Thema] wichtig ist
- Statistiken
- Business Impact
- Trends

## [Hauptaspekt 1]
### Unteraspekt 1.1
### Unteraspekt 1.2

## [Hauptaspekt 2]
...

## [Hauptaspekt N]
...

## Best Practices / Tipps
- Actionable Tipps
- Do's and Don'ts

## Tools & Ressourcen
- Empfohlene Tools
- Templates

## FAQ
- 5-10 häufige Fragen
- Schema Markup

## Fazit
- Zusammenfassung
- Nächste Schritte
- CTA
```

### Beispiel-Titel

```
"Content Marketing: Der ultimative Guide für 2024"
"SEO für Anfänger: Alles was du wissen musst"
"E-Mail Marketing Strategie: Von A bis Z"
```

---

## 2. Cluster Article

### Beschreibung
Fokussierter Artikel zu einem Unterthema des Pillars. Geht tiefer auf ein spezifisches Thema ein.

### Spezifikationen

```
Wortanzahl:     1.500 - 2.500
Struktur:       5-8 H2 Sections
H3 pro H2:      1-3
Interne Links:  3-5 (inkl. Pillar!)
Externe Links:  2-5
Bilder:         5-10
```

### Aufbau

```markdown
# [Long-Tail Keyword]: [Spezifischer Angle]

## Intro
- Hook
- Was der Leser lernt
- Link zu Pillar (früh!)

## [Kernthema 1]
### Details
### Beispiele

## [Kernthema 2]
...

## Schritt-für-Schritt Anleitung
(falls relevant)

## Häufige Fehler vermeiden

## Fazit
- Key Takeaways
- Link zurück zum Pillar
```

### Beziehung zum Pillar

```
Pillar: "Content Marketing Guide"
├── Cluster: "Redaktionsplan erstellen" (How-To)
├── Cluster: "Content Audit durchführen" (Process)
├── Cluster: "Blog Traffic steigern" (Tips)
└── Cluster: "Content Marketing Tools" (Comparison)
```

---

## 3. How-To Guide

### Beschreibung
Schritt-für-Schritt Anleitung für eine konkrete Aufgabe. Beantwortet "Wie mache ich X?"

### Spezifikationen

```
Wortanzahl:     2.000 - 3.000
Struktur:       Chronologische Schritte
Bilder:         Screenshots pro Schritt
Schema:         HowTo Schema
```

### Aufbau

```markdown
# Wie du [Ziel erreichst]: Schritt-für-Schritt Anleitung

## Was du brauchst / Voraussetzungen
- Tool 1
- Vorkenntnisse
- Zeitaufwand

## Schritt 1: [Aktion]
![Screenshot]
1. Detail-Anweisung
2. Detail-Anweisung
> Tipp: [Profi-Tipp]

## Schritt 2: [Aktion]
...

## Schritt N: [Aktion]
...

## Ergebnis / Was du erreicht hast

## Troubleshooting / Häufige Probleme
- Problem 1 → Lösung
- Problem 2 → Lösung

## Nächste Schritte
```

### Schema Markup

```json
{
  "@type": "HowTo",
  "name": "Wie du...",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Schritt 1",
      "text": "..."
    }
  ]
}
```

---

## 4. Comparison / Versus Article

### Beschreibung
Vergleicht zwei oder mehr Optionen. Beantwortet "Was ist besser, A oder B?"

### Spezifikationen

```
Wortanzahl:     2.000 - 3.500
Struktur:       Vergleichstabellen + Sections
Intent:         Commercial Investigation
CTA:            Produktempfehlung
```

### Aufbau

```markdown
# [A] vs [B]: Der ultimative Vergleich [Jahr]

## Quick Answer / TL;DR
- Wähle A wenn...
- Wähle B wenn...

## Vergleichstabelle
| Feature | A | B |
|---------|---|---|

## Was ist [A]?
- Kurze Beschreibung
- Für wen geeignet

## Was ist [B]?
- Kurze Beschreibung
- Für wen geeignet

## Detaillierter Vergleich

### Kriterium 1: [z.B. Preis]
- A: ...
- B: ...
- Gewinner: [A/B]

### Kriterium 2: [z.B. Features]
...

## Vor- und Nachteile

### [A] Pros & Cons
✅ Pro 1
✅ Pro 2
❌ Con 1
❌ Con 2

### [B] Pros & Cons
...

## Unser Fazit: Was solltest du wählen?

## FAQ
```

---

## 5. Listicle

### Beschreibung
Nummerierte Liste von Items (Tools, Tipps, Beispiele). Scannable und shareable.

### Spezifikationen

```
Wortanzahl:     1.500 - 2.500
Struktur:       Nummerierte H2s
Bilder:         1 pro Item (optional)
Format:         Leicht zu scannen
```

### Aufbau

```markdown
# [Zahl] [Kategorie] für [Ziel] ([Jahr])

## Intro
- Warum diese Liste
- Was der Leser bekommt

## 1. [Item Name]
- Kurze Beschreibung
- Warum es auf der Liste ist
- Key Feature / USP
- [Link / CTA]

## 2. [Item Name]
...

## [N]. [Item Name]
...

## Bonus: [Extra Item]

## Zusammenfassung / Fazit
- Quick Picks
- Unsere Top-Empfehlung
```

### Beispiel-Titel

```
"15 Content Marketing Tools, die du 2024 brauchst"
"7 Tipps für bessere Blog-Überschriften"
"10 häufige SEO-Fehler und wie du sie vermeidest"
```

---

## 6. FAQ / Q&A Article

### Beschreibung
Beantwortet häufige Fragen zu einem Thema. Ideal für Featured Snippets.

### Spezifikationen

```
Wortanzahl:     1.500 - 2.500
Struktur:       Frage als H2, Antwort darunter
Schema:         FAQPage Schema
Featured:       Optimiert für Snippets
```

### Aufbau

```markdown
# [Thema]: Häufige Fragen und Antworten

## Intro
- Über diesen FAQ-Guide

## [Frage 1]?
[Direkte Antwort im ersten Satz.]
[Weitere Details und Kontext.]

## [Frage 2]?
...

## Weiterführende Ressourcen
```

### Schema Markup

```json
{
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Was ist...?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "..."
      }
    }
  ]
}
```

---

## Content-Typ Auswahl

### Nach Suchintent

| Intent | Content-Typ |
|--------|-------------|
| Informational | Pillar, How-To, FAQ |
| Navigational | Cluster, Brand Content |
| Commercial | Comparison, Listicle |
| Transactional | Landing Page, Product Content |

### Nach Keyword-Typ

| Keyword-Typ | Content-Typ |
|-------------|-------------|
| Head Keyword | Pillar Page |
| Long-Tail | Cluster Article |
| "How to..." | How-To Guide |
| "vs" / "oder" | Comparison |
| "beste" / "top" | Listicle |
| "was ist" / "warum" | FAQ, Pillar |
