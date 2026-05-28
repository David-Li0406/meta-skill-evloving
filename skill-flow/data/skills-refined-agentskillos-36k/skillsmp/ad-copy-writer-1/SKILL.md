---
name: ad-copy-writer
description: Creates performance-optimized advertising copy for paid campaigns. Generates headlines, descriptions, CTAs, and ad variations following platform-specific requirements. Includes A/B test variants and audience-specific messaging. Supports Google Ads, Meta Ads, LinkedIn Ads, TikTok Ads, and Pinterest Ads. Use when creating paid advertising campaigns from content.
---

# Ad Copy Writer

Erstellt conversion-optimierte Werbetexte für alle Paid-Advertising-Plattformen.

## Quick Start

```
Input: Pillar Content (Artikel) + Zielgruppe + Kampagnenziel
Output: Vollständige Ad-Sets für alle Plattformen in JSON
```

## Workflow

1. **Content analysieren** → USPs, Benefits, Pain Points extrahieren
2. **Zielgruppe definieren** → Persona aus [AUDIENCE_PERSONAS.md](AUDIENCE_PERSONAS.md)
3. **Kampagnenziel festlegen** → Awareness, Traffic, Leads, Sales
4. **Copywriting-Formel wählen** → [COPYWRITING_FORMULAS.md](COPYWRITING_FORMULAS.md)
5. **Platform-Specs laden** → [PLATFORM_REQUIREMENTS.md](PLATFORM_REQUIREMENTS.md)
6. **Varianten erstellen** → Min. 3 pro Ad-Set für A/B Testing
7. **Compliance prüfen** → [COMPLIANCE_RULES.md](COMPLIANCE_RULES.md)

## Output Format

```json
{
  "campaign": {
    "name": "Kampagnenname",
    "objective": "conversions|traffic|awareness|leads",
    "source_content_id": "uuid"
  },
  "ad_sets": [
    {
      "platform": "google_ads",
      "ad_type": "responsive_search",
      "variations": [
        {
          "headlines": ["H1", "H2", "H3", "..."],
          "descriptions": ["D1", "D2", "..."],
          "paths": ["path1", "path2"],
          "final_url": "https://..."
        }
      ]
    }
  ]
}
```

## Unterstützte Plattformen

| Platform | Templates | Specs |
|----------|-----------|-------|
| Google Ads | [templates/google-ads/](templates/google-ads/) | Search, Display, Performance Max |
| Meta Ads | [templates/meta-ads/](templates/meta-ads/) | Facebook, Instagram |
| LinkedIn Ads | [templates/linkedin-ads/](templates/linkedin-ads/) | Sponsored Content, Message Ads |
| TikTok Ads | [templates/tiktok-ads/](templates/tiktok-ads/) | In-Feed, Spark Ads |
| Pinterest Ads | [templates/pinterest-ads/](templates/pinterest-ads/) | Standard, Video, Shopping |

## Copywriting-Grundprinzipien

### Benefits > Features
```
❌ "Unser Tool hat 50+ Integrationen"
✅ "Verbinde alle deine Tools in 5 Minuten"
```

### Spezifisch > Vage
```
❌ "Steigere deinen Umsatz"
✅ "Steigere deinen Umsatz um 47% in 90 Tagen"
```

### Du > Wir
```
❌ "Wir bieten die beste Lösung"
✅ "Du bekommst Ergebnisse ab Tag 1"
```

### Dringlichkeit (wenn authentisch)
```
❌ "Kaufe jetzt!!!"
✅ "Noch 3 Plätze im März verfügbar"
```

## A/B Testing Strategie

Für jede Kampagne mindestens **3 Varianten** erstellen:

| Variante | Fokus | Beispiel-Hook |
|----------|-------|---------------|
| A | Problem/Pain | "Frustriert von [Problem]?" |
| B | Benefit/Outcome | "Erreiche [Ergebnis] in [Zeit]" |
| C | Social Proof | "[X] Unternehmen vertrauen uns" |

## Quick Reference: Zeichenlimits

| Platform | Headline | Description |
|----------|----------|-------------|
| Google Search | 30 chars | 90 chars |
| Google Display | 30 chars | 90 chars |
| Meta | 40 chars | 125 chars (primary) |
| LinkedIn | 70 chars | 150 chars (intro) |
| TikTok | 100 chars | 100 chars |
| Pinterest | 100 chars | 500 chars |

Details: [PLATFORM_REQUIREMENTS.md](PLATFORM_REQUIREMENTS.md)
