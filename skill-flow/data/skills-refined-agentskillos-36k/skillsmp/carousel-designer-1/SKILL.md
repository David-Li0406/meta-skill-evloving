---
name: carousel-designer
description: Designs multi-slide carousel content for Instagram and LinkedIn. Creates slide sequences with visual hierarchy, copy, and CTAs. Handles slide count optimization and platform-specific formatting. Use when creating educational or storytelling carousel content.
---

# Carousel Designer

Erstellt Multi-Slide Carousel Content für Instagram und LinkedIn.

## Quick Start

```
Input: Topic + Key Points + Platform + Ziel
Output: Slide-Content + Visual Direction + Captions
```

## Plattform-Spezifikationen

| Plattform | Slides | Ratio | Größe | Max Text |
|-----------|--------|-------|-------|----------|
| Instagram | 2-10 | 1:1 oder 4:5 | 1080x1080 / 1080x1350 | Wenig |
| LinkedIn | 2-20 | 1:1 oder 4:5 | 1080x1080 / 1080x1350 | Mehr OK |

## Output Format

```json
{
  "carousel": {
    "title": "5 Content Marketing Fehler",
    "platform": "instagram",
    "slides": 7,
    "aspect_ratio": "4:5",
    "goal": "education + engagement"
  },
  "slides": [
    {
      "number": 1,
      "type": "cover",
      "headline": "5 Content Marketing Fehler",
      "subheadline": "Die du 2024 vermeiden musst",
      "visual_direction": "Bold typography, Brand colors, Eye-catching graphic",
      "cta": null
    },
    {
      "number": 2,
      "type": "content",
      "headline": "Fehler #1",
      "body": "Ohne Strategie posten",
      "detail": "Random Content bringt keine Ergebnisse",
      "visual_direction": "Number prominent, Icon or illustration",
      "icon_suggestion": "🎯"
    },
    {
      "number": 7,
      "type": "cta",
      "headline": "Speichern für später!",
      "body": "Teile mit einem Marketer",
      "visual_direction": "Save icon, Arrow pointing up",
      "cta": "Folge @brand für mehr"
    }
  ],
  "caption": {
    "hook": "Diese 5 Fehler ruinieren dein Content Marketing 👇",
    "body": "Machst du auch Fehler #3? Ehrlich gesagt, das war mein größter Fehler am Anfang...",
    "cta": "Speichern und an jemanden schicken, der das braucht! 💾",
    "hashtags": ["#contentmarketing", "#marketingtipps", "#digitalmarketing"]
  },
  "design_notes": {
    "colors": ["#003366", "#ff6600", "#ffffff"],
    "fonts": ["Bold Sans for Headlines", "Regular Sans for Body"],
    "style": "Clean, professional, consistent across all slides"
  }
}
```

## Slide-Typen

### 1. Cover Slide

```
Ziel: Attention grabben, zum Swipen motivieren

Elemente:
- Starke Headline
- Neugier wecken
- Swipe-Indicator (optional)
- Brand Elements

Beispiele:
"5 Dinge die ich gerne früher gewusst hätte"
"Der Unterschied zwischen X und Y"
"Warum [bekannte Methode] nicht funktioniert"
```

### 2. Content Slides

```
Ziel: Wert liefern, weiter swipen

Struktur:
- Headline / Nummer
- 1 Key Point pro Slide
- Kurze Erklärung
- Visual/Icon

Regeln:
- Max 30-40 Wörter pro Slide
- Lesbar in 3-5 Sekunden
- Konsistentes Layout
```

### 3. Beispiel/Illustration Slide

```
Ziel: Punkt mit Beispiel verdeutlichen

Elemente:
- Screenshot
- Before/After
- Diagramm
- Quote

Wichtig:
- Nicht zu komplex
- Mobile-optimiert
```

### 4. CTA Slide (letzte)

```
Ziel: Engagement, Follow, Save

CTAs:
- "Speichern für später 💾"
- "Folge für mehr Tipps"
- "Teile mit einem Freund"
- "Link in Bio"
- "Kommentiere deine Meinung"
```

## Struktur-Templates

### Listicle (5-7 Slides)

```
Slide 1: Cover - "5 Tipps für..."
Slide 2: Tipp #1
Slide 3: Tipp #2
Slide 4: Tipp #3
Slide 5: Tipp #4
Slide 6: Tipp #5
Slide 7: CTA - "Speichern & Teilen"
```

### How-To (6-8 Slides)

```
Slide 1: Cover - "Wie du..."
Slide 2: Schritt 1
Slide 3: Schritt 2
Slide 4: Schritt 3
Slide 5: Schritt 4
Slide 6: Ergebnis/Beispiel
Slide 7: Pro-Tipp
Slide 8: CTA
```

### Storytelling (7-10 Slides)

```
Slide 1: Cover - Hook
Slide 2: Kontext/Problem
Slide 3: Die Situation
Slide 4: Der Wendepunkt
Slide 5: Die Lösung
Slide 6: Das Ergebnis
Slide 7: Learning #1
Slide 8: Learning #2
Slide 9: Takeaway
Slide 10: CTA
```

### Vergleich (5-6 Slides)

```
Slide 1: Cover - "X vs Y"
Slide 2: Was ist X?
Slide 3: Was ist Y?
Slide 4: Vergleich (Tabelle/Split)
Slide 5: Empfehlung
Slide 6: CTA
```

### Myth-Busting (6-8 Slides)

```
Slide 1: Cover - "Mythen über..."
Slide 2: Mythos #1 ❌ → Wahrheit ✅
Slide 3: Mythos #2
Slide 4: Mythos #3
Slide 5: Mythos #4
Slide 6: Die Wahrheit zusammengefasst
Slide 7: CTA
```

## Design-Richtlinien

### Typography

```
Headlines:
- Bold, Sans-Serif
- 24-48pt (je nach Länge)
- Kontrast-Farbe

Body:
- Regular oder Medium
- 16-24pt
- Gut lesbar

Zahlen/Hervorhebungen:
- Extra Bold
- Akzentfarbe
```

### Farben

```
Brand-Farben verwenden:
- Primary: Headlines, Akzente
- Accent: CTAs, Highlights
- Neutral: Hintergründe, Body Text

Kontrast:
- Mindestens 4.5:1 für Text
- Lesbar auf Mobile
```

### Layout

```
Safe Zones:
- Rand: min 40px
- Keine Text am äußersten Rand
- Wichtiges in der Mitte

Grid:
- Konsistent über alle Slides
- Headline-Position gleich
- Body-Position gleich
```

### Visuelle Elemente

```
Icons:
- Einfach, erkennbar
- Passend zum Inhalt
- Konsistenter Stil

Grafiken:
- Nicht zu komplex
- Mobile-optimiert
- Brand-Colors

Fotos:
- Hochwertig
- Passend zum Thema
- Als Hintergrund: Overlay verwenden
```

## Caption-Struktur

### Instagram

```
Hook (Erste Zeile):
"Diese Fehler kosten dich Kunden 👇"
[WICHTIG: Zeile 1 wird im Feed angezeigt!]

Body:
- Erweitere den Carousel-Inhalt
- Persönliche Note
- Storytelling
- 150-300 Wörter

CTA:
- Speichern
- Kommentieren
- Teilen
- Folgen

Hashtags:
- 5-15 relevante
- Mix aus groß/klein
- Am Ende oder in Kommentar
```

### LinkedIn

```
Hook:
"Content Marketing ist nicht tot. Dein Content ist es vielleicht."

Body:
- Mehr Text OK (LinkedIn mag Text)
- Professional Tone
- Mehrwert & Insights
- 500-1000 Zeichen

CTA:
- Repost
- Kommentar
- Follow
- "Was denkst du?"

Hashtags:
- 3-5 relevant
- Am Ende
```

## Engagement-Optimierung

### Swipe-Trigger

```
Slide 1 → 2:
- Neugier wecken
- "Swipe für mehr"
- Anschneiden des nächsten Points

Zwischen Slides:
- Cliffhanger
- "Aber es gibt noch mehr..."
- Visuelle Kontinuität
```

### Save-Trigger

```
- "Speichern für später"
- Wertvoller, praktischer Content
- Checklisten, Tipps, How-Tos
- Reference-Material
```

### Kommentar-Trigger

```
- Frage stellen
- Meinung erfragen
- "Was ist dein größter Fehler?"
- Kontroverse (mild)
```

## Checkliste

### Content
- [ ] Hook im ersten Slide?
- [ ] 1 Point pro Slide?
- [ ] Max 40 Wörter pro Slide?
- [ ] CTA im letzten Slide?
- [ ] Caption geschrieben?

### Design
- [ ] Konsistentes Layout?
- [ ] Brand Colors?
- [ ] Lesbar auf Mobile?
- [ ] Safe Zones beachtet?
- [ ] Hochwertige Grafiken?

### Plattform
- [ ] Richtiges Aspect Ratio?
- [ ] Slide-Count optimal?
- [ ] Hashtags relevant?
- [ ] Alt-Text für Accessibility?
