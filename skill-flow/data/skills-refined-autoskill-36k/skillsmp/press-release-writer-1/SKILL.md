---
name: press-release-writer
description: Transforms SEO articles into professional press releases following AP style guidelines. Includes headline, lead paragraph, quotes, boilerplate, and media contact. Adapts tone for B2B or B2C audiences. Generates multiple angles for different media outlets. Use when repurposing content for PR distribution.
---

# Press Release Writer

Transformiert Pillar-Content in professionelle Pressemeldungen für PR-Distribution.

## Quick Start

```
Input: Artikel-Inhalt + Firmeninfos + Anlass
Output: Vollständige Pressemeldung + Pitch-Varianten
```

## Workflow

1. **News-Wert identifizieren** → Was ist die Story?
2. **Anlass bestimmen** → [PRESS_RELEASE_TYPES.md](PRESS_RELEASE_TYPES.md)
3. **5 W's extrahieren** → Wer, Was, Wann, Wo, Warum
4. **AP Style anwenden** → [AP_STYLE_GUIDE.md](AP_STYLE_GUIDE.md)
5. **Zitate generieren** → [QUOTE_GUIDELINES.md](QUOTE_GUIDELINES.md)
6. **Boilerplate einfügen** → [BOILERPLATE_TEMPLATES.md](BOILERPLATE_TEMPLATES.md)
7. **Pitch-Winkel entwickeln** → Verschiedene Medien-Perspektiven

## Output Format

```json
{
  "press_release": {
    "headline": "Hauptüberschrift",
    "subheadline": "Optional",
    "dateline": "[Stadt], [Datum]",
    "lead_paragraph": "Die wichtigsten Fakten in 1-2 Sätzen",
    "body": ["Absatz 1", "Absatz 2", "..."],
    "quote": {
      "text": "Zitat",
      "attribution": "Name, Position bei Firma"
    },
    "additional_quote": { ... },
    "boilerplate": "Über [Firma]...",
    "media_contact": {
      "name": "...",
      "email": "...",
      "phone": "..."
    }
  },
  "pitch_angles": [
    {
      "target_media": "Fachmedien",
      "angle": "...",
      "subject_line": "..."
    }
  ]
}
```

## Pressemeldungs-Struktur

```
[HEADLINE - Max 80 Zeichen, aktiv, prägnant]

[SUBHEADLINE - Optional, erweitert Headline]

[STADT], [DATUM] – [LEAD PARAGRAPH - 5 W's in 1-2 Sätzen]

[BODY PARAGRAPH 1 - Erweitert Lead mit Details]

[BODY PARAGRAPH 2 - Hintergrund/Kontext]

"[ZITAT]", sagt [Name], [Position] bei [Firma].

[BODY PARAGRAPH 3 - Zusätzliche Details]

[OPTIONALES ZWEITES ZITAT - Partner/Kunde]

[VERFÜGBARKEIT/NEXT STEPS]

### Über [Firma]
[BOILERPLATE]

### Pressekontakt
[Name] | [Email] | [Telefon]
```

## Headline-Formeln

### News-Announcement
```
[Firma] [Verb im Präsens] [Was] für [Zielgruppe]
→ "TechCorp launcht KI-Plattform für Mittelstand"
```

### Achievement/Milestone
```
[Firma] erreicht [Milestone]: [Bedeutung]
→ "ContentAI überschreitet 10.000 Kunden-Marke"
```

### Partnership
```
[Firma A] und [Firma B] [Verb] für [Ziel]
→ "TechCorp und DataGmbH kooperieren für bessere Analytics"
```

### Study/Report
```
[Studie/Report]: [Key Finding] zeigt [Implikation]
→ "Neue Studie: 73% der Marketer setzen auf KI-Tools"
```

## Lead Paragraph (5 W's)

Der Lead muss beantworten:
- **Wer:** Welches Unternehmen/Person?
- **Was:** Was ist passiert/wird angekündigt?
- **Wann:** Zeitpunkt?
- **Wo:** Ort (wenn relevant)?
- **Warum:** Warum ist das wichtig?

**Template:**
```
[Firma] ([Beschreibung]) hat heute [Was] [bekannt gegeben/vorgestellt/gestartet].
[Warum das wichtig ist für Zielgruppe].
```

## Zitat-Guidelines

Siehe [QUOTE_GUIDELINES.md](QUOTE_GUIDELINES.md) für Details.

**Quick Reference:**
- Zitat muss Mehrwert bieten (nicht wiederholen)
- Emotionaler/visionärer als der Rest
- Attribution: "Vorname Nachname, Position bei Firma"
- Max 2-3 Sätze

## Checkliste

- [ ] Headline ≤ 80 Zeichen, aktiv, prägnant?
- [ ] Lead beantwortet 5 W's?
- [ ] Zitat von relevanter Person?
- [ ] Boilerplate aktuell?
- [ ] Kontaktdaten vollständig?
- [ ] AP Style eingehalten?
- [ ] Keine Werbesprache?
- [ ] News-Wert klar erkennbar?
