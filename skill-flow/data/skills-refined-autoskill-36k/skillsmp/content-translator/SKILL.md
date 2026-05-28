---
name: content-translator
description: Translates marketing content while preserving SEO value, brand voice, and cultural nuances. Handles localization of keywords, CTAs, and formatting conventions. Supports DE-EN bidirectional translation with focus on marketing/technical content. Use when translating articles, ads, or other marketing materials.
---

# Content Translator

Professionelle Übersetzung von Marketing-Content mit SEO-Optimierung und kultureller Anpassung.

## Quick Start

```
Input: Source Content + Target Language + SEO Keywords (optional)
Output: Translated Content + Localized Keywords + Cultural Adaptations
```

## Supported Languages

| Von → Nach | Status | Spezialisierung |
|------------|--------|-----------------|
| DE → EN | ✅ | Marketing, Tech, SEO |
| EN → DE | ✅ | Marketing, Tech, SEO |
| DE → FR | ⚡ | Marketing |
| DE → ES | ⚡ | Marketing |
| DE → IT | ⚡ | Marketing |

✅ = Vollständig optimiert | ⚡ = Basis-Support

## Workflow

1. **Content analysieren** → Typ, Ton, Keywords identifizieren
2. **Keywords übersetzen** → SEO-Keywords lokalisieren
3. **Content übersetzen** → Mit Kontext und Ton
4. **Kulturell anpassen** → Redewendungen, Formate, Konventionen
5. **SEO validieren** → Keywords, Meta-Tags, URLs
6. **Qualitätsprüfung** → Native-Speaker-Level Check

## Output Format

```json
{
  "translation": {
    "source_language": "de",
    "target_language": "en",
    "content_type": "blog_article",
    "translated_content": {
      "title": "...",
      "meta_description": "...",
      "content": "...",
      "headings": ["H1: ...", "H2: ..."]
    },
    "keyword_mapping": {
      "original": ["Content Marketing", "SEO Strategie"],
      "translated": ["Content Marketing", "SEO Strategy"],
      "search_volume": {
        "Content Marketing": {"de": 12000, "en": 110000},
        "SEO Strategy": {"de": 2400, "en": 18000}
      }
    },
    "cultural_adaptations": [
      {
        "original": "Sie können...",
        "translated": "You can...",
        "note": "Formal 'Sie' → informal 'you' (standard in EN marketing)"
      }
    ],
    "url_suggestion": {
      "original": "/content-marketing-strategie",
      "translated": "/content-marketing-strategy"
    }
  }
}
```

## Übersetzungs-Regeln

### SEO-Kritische Elemente

| Element | Regel |
|---------|-------|
| Title Tag | Keywords vorne, max 60 Zeichen |
| Meta Description | CTA anpassen, max 155 Zeichen |
| H1 | Hauptkeyword integrieren |
| URL/Slug | Keyword + Bindestriche |
| Alt-Texte | Beschreibend + Keyword |

### Kulturelle Anpassungen

Details: [CULTURAL_ADAPTATIONS.md](CULTURAL_ADAPTATIONS.md)

**DE → EN:**
- Formelle Anrede ("Sie") → Informell ("you")
- Lange Sätze → Kürzere, direktere Sätze
- Zahlenformat: 1.000,00 → 1,000.00
- Datumsformat: 15.01.2024 → January 15, 2024
- Währung anpassen (falls relevant)

**EN → DE:**
- Informell ("you") → Formal/Informal je nach Zielgruppe
- Marketing-Anglizismen prüfen
- Rechtschreibung: US vs. UK → DE
- Gender-neutrale Sprache beachten

## Besondere Content-Typen

### Ads & CTAs

```
DE: "Jetzt kostenlos testen"
EN: "Start your free trial" (nicht: "Test now for free")

DE: "Mehr erfahren"
EN: "Learn more" (nicht: "Experience more")

DE: "Kontaktieren Sie uns"
EN: "Get in touch" / "Contact us"
```

Details: [CTA_TRANSLATIONS.md](CTA_TRANSLATIONS.md)

### Technical Content

```
DE: "Schnittstelle"
EN: "API" / "Interface" (Kontext-abhängig)

DE: "Datenschutz"
EN: "Data privacy" / "GDPR compliance"
```

Details: [TECHNICAL_GLOSSARY.md](TECHNICAL_GLOSSARY.md)

## Keyword-Lokalisierung

### Workflow

1. **Source Keywords extrahieren**
2. **Direkte Übersetzung** prüfen
3. **Suchvolumen** in Zielsprache checken
4. **Lokale Varianten** identifizieren
5. **Beste Option** wählen (Suchvolumen × Relevanz)

### Beispiel

```
Source (DE): "Inbound Marketing"
Options (EN):
├── "Inbound Marketing" (direkter Begriff, hoher SV)
├── "Inbound Marketing Strategy" (Long-Tail)
└── "Attraction Marketing" (Alternative, niedriger SV)

→ Empfehlung: "Inbound Marketing" (Begriff ist international)
```

## Integration

### Mit SEO-Workflow

```typescript
// Nach Content-Erstellung
const translation = await contentTranslator.translate({
  content: germanArticle,
  targetLanguage: 'en',
  preserveKeywords: ['brand terms'],
  adaptForMarket: 'US' // oder 'UK'
});

// Keyword-Mapping für Tracking speichern
await saveKeywordMapping(translation.keyword_mapping);
```

### Mit WordPress

```typescript
// Übersetzung als Draft erstellen
const translatedPost = await wpClient.createPost({
  ...translation.translated_content,
  status: 'draft',
  meta: {
    original_post_id: originalPost.id,
    translation_language: 'en'
  }
});
```

## Qualitäts-Checkliste

- [ ] Keywords in Zielsprache recherchiert?
- [ ] Title Tag optimiert (<60 Zeichen)?
- [ ] Meta Description angepasst (<155 Zeichen)?
- [ ] Kulturelle Anpassungen vorgenommen?
- [ ] Zahlen-/Datumsformat angepasst?
- [ ] CTAs lokalisiert (nicht nur übersetzt)?
- [ ] Brand Terms konsistent?
- [ ] Native-Speaker-Level Qualität?
- [ ] Interne Links angepasst?
- [ ] URL-Slug lokalisiert?
