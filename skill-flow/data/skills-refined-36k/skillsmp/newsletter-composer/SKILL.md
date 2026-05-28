---
name: newsletter-composer
description: Creates engaging email newsletter content from pillar articles. Structures emails with compelling subject lines, preview text, sections, and CTAs. Supports different newsletter formats (digest, single-topic, announcement). Optimizes for open rates and click-through. Use when distributing content via email marketing.
---

# Newsletter Composer

Transformiert Pillar-Content in Newsletter-Emails, die geöffnet und geklickt werden.

## Quick Start

```
Input: Artikel + Newsletter-Typ + Zielgruppe
Output: Vollständige Email mit Subject Lines, Preview, Body, CTAs
```

## Workflow

1. **Content analysieren** → Kernbotschaft, Key Takeaways extrahieren
2. **Newsletter-Typ wählen** → [NEWSLETTER_TYPES.md](NEWSLETTER_TYPES.md)
3. **Subject Line erstellen** → [SUBJECT_LINE_FORMULAS.md](SUBJECT_LINE_FORMULAS.md)
4. **Email strukturieren** → [EMAIL_STRUCTURE.md](EMAIL_STRUCTURE.md)
5. **Spam-Check** → [SPAM_TRIGGER_WORDS.md](SPAM_TRIGGER_WORDS.md)
6. **Personalisierung** → Merge Tags einbauen

## Output Format

```json
{
  "newsletter": {
    "subject_lines": [
      {"text": "Option 1", "type": "curiosity"},
      {"text": "Option 2", "type": "benefit"},
      {"text": "Option 3", "type": "urgency"}
    ],
    "preview_text": "[40-90 Zeichen]",
    "body": {
      "greeting": "[Personalisierte Anrede]",
      "hook": "[Erster Absatz - Aufmerksamkeit]",
      "main_content": "[Hauptteil]",
      "cta_primary": {
        "text": "[Button-Text]",
        "url": "[Link]"
      },
      "secondary_content": "[Optional]",
      "cta_secondary": { ... },
      "signature": "[Absender]",
      "ps": "[Optional: P.S. Zeile]"
    },
    "metadata": {
      "word_count": 250,
      "estimated_read_time": "2 min",
      "links_count": 3
    }
  }
}
```

## Newsletter-Typen

| Typ | Beschreibung | Frequenz |
|-----|--------------|----------|
| Single Article | Ein Artikel im Fokus | Ad-hoc |
| Weekly Digest | Mehrere Artikel zusammengefasst | Wöchentlich |
| Announcement | Produkt/Feature-News | Ad-hoc |
| Nurture | Bildungs-Serie | Automatisiert |
| Event | Einladung/Reminder | Event-bezogen |

Details: [NEWSLETTER_TYPES.md](NEWSLETTER_TYPES.md)

## Subject Line Quick Reference

| Formel | Beispiel |
|--------|----------|
| How-To | "Wie du [Ergebnis] erreichst" |
| Number | "5 Wege zu [Ziel]" |
| Question | "Machst du diesen Fehler auch?" |
| Curiosity | "Das wissen die wenigsten über [Thema]" |
| Urgency | "Nur noch heute: [Angebot]" |
| Personal | "[Name], das solltest du wissen" |

Details: [SUBJECT_LINE_FORMULAS.md](SUBJECT_LINE_FORMULAS.md)

## Key Metrics Benchmarks (B2B)

| Metrik | Durchschnitt | Gut | Sehr gut |
|--------|--------------|-----|----------|
| Open Rate | 20% | 25% | 30%+ |
| Click Rate | 2.5% | 4% | 6%+ |
| Unsub Rate | 0.5% | <0.3% | <0.1% |

## Personalisierung

Verfügbare Merge Tags:
```
{{first_name}} - Vorname
{{company}} - Firmenname
{{industry}} - Branche
{{last_article}} - Letzter gelesener Artikel
```

## Checkliste

- [ ] Subject Line ≤ 50 Zeichen?
- [ ] Preview Text 40-90 Zeichen?
- [ ] Hook in ersten 2 Sätzen?
- [ ] Klarer CTA?
- [ ] Mobile-optimiert (kurze Absätze)?
- [ ] Spam-Wörter vermieden?
- [ ] Personalisierung eingebaut?
- [ ] Unsubscribe-Link vorhanden?
