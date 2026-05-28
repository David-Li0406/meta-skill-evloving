---
name: social-post-creator
description: Creates platform-optimized social media posts from pillar content. Generates variations for LinkedIn, Instagram, Facebook, TikTok, X/Twitter, and Pinterest. Handles hashtags, mentions, CTAs, and character limits per platform. Differentiates between company and personal account styles. Use when repurposing content for social distribution.
---

# Social Post Creator

Transformiert Pillar-Content (SEO-Artikel) in plattform-optimierte Social Media Posts.

## Quick Start

```
Input: Artikel-Inhalt (Markdown)
Output: Posts für alle Plattformen in JSON-Format
```

## Workflow

1. **Artikel analysieren** → Kernaussagen, Hooks, Zitate extrahieren
2. **Platform auswählen** → Specs aus [PLATFORM_SPECS.md](PLATFORM_SPECS.md) laden
3. **Account-Typ bestimmen** → Company vs. Personal (siehe [TONE_GUIDELINES.md](TONE_GUIDELINES.md))
4. **Posts generieren** → Templates aus `/templates/{platform}/` nutzen
5. **Hashtags hinzufügen** → Strategien aus [HASHTAG_STRATEGIES.md](HASHTAG_STRATEGIES.md)
6. **Output formatieren** → JSON mit allen Varianten

## Output Format

```json
{
  "article_id": "uuid",
  "created_at": "ISO-8601",
  "posts": [
    {
      "platform": "linkedin",
      "account_type": "company",
      "content": "Post-Text...",
      "hashtags": ["#hashtag1", "#hashtag2"],
      "cta": "Link in Bio",
      "image_prompt": "Beschreibung für Bild-Generierung",
      "scheduled_time": "ISO-8601 (optional)"
    }
  ]
}
```

## Platform-Specific Guidelines

| Platform | Siehe Template |
|----------|----------------|
| LinkedIn | [templates/linkedin/](templates/linkedin/) |
| Instagram | [templates/instagram/](templates/instagram/) |
| Facebook | [templates/facebook/](templates/facebook/) |
| TikTok | [templates/tiktok/](templates/tiktok/) |
| X/Twitter | [templates/twitter/](templates/twitter/) |
| Pinterest | [templates/pinterest/](templates/pinterest/) |

## Company vs. Personal Posts

**Company Account:**
- Formeller Ton
- Marken-Voice
- Produkt-fokussiert
- "Wir" statt "Ich"

**Personal Account (Employee Advocacy):**
- Persönliche Perspektive
- Storytelling
- Thought Leadership
- Authentische Erfahrungen

Details: [TONE_GUIDELINES.md](TONE_GUIDELINES.md)

## Hooks & Attention Grabbers

Erste Zeile entscheidet über Engagement. Bewährte Formate:

1. **Kontroverse Aussage:** "Die meisten machen [X] falsch..."
2. **Überraschende Statistik:** "97% der [Zielgruppe] wissen nicht..."
3. **Persönliche Story:** "Letzte Woche ist mir etwas passiert..."
4. **Direkte Frage:** "Kennst du das Gefühl, wenn...?"
5. **Bold Statement:** "[Unpopuläre Meinung] ist eigentlich [Wahrheit]"

## CTA Library

Siehe [CTA_LIBRARY.md](CTA_LIBRARY.md) für plattform-spezifische Call-to-Actions.
