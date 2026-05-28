# Meta Single Image Ad Template

## Specs
- **Primary Text:** 125 Zeichen sichtbar (max 2.200)
- **Headline:** 40 Zeichen
- **Description:** 30 Zeichen (optional)
- **Image:** 1080x1080 (1:1) oder 1080x1350 (4:5)
- **CTA Button:** Vordefinierte Optionen

---

## CTA-Button Optionen

| Button | Beste für |
|--------|-----------|
| Learn More | Awareness, Content |
| Shop Now | E-Commerce |
| Sign Up | Lead Gen, Newsletter |
| Get Offer | Rabatte, Deals |
| Book Now | Termine, Services |
| Contact Us | B2B, High-Touch |
| Download | Lead Magnets |
| Get Quote | Services, B2B |
| Subscribe | Subscriptions |
| Apply Now | Jobs, Programme |

---

## Primary Text Templates

### Template A: PAS (Problem-Agitate-Solve)
```
[Problem als Frage]? 😤

[Agitation - das Problem verstärken, 1-2 Sätze]

Die Lösung: [Produkt/Service] [Hauptbenefit].

✓ [Vorteil 1]
✓ [Vorteil 2]
✓ [Vorteil 3]

[CTA] 👇
```

### Template B: Story-Hook
```
[Überraschende Aussage oder Ergebnis] 🎯

[Kurze Story/Kontext - 2-3 Sätze]

Das Geheimnis? [Produkt/Service].

Erfahre mehr →
```

### Template C: Social Proof
```
[Zahl]+ [Zielgruppe] haben bereits [Ergebnis erreicht].

"[Kurzes Testimonial]" - [Name, Titel]

Du bist als Nächstes dran.

[CTA] →
```

### Template D: Direct Benefit
```
[Hauptbenefit in einem Satz] ⚡

Kein [Unerwünschtes 1].
Kein [Unerwünschtes 2].
Nur [Erwünschtes Ergebnis].

[Angebot: z.B. "14 Tage kostenlos"]

[CTA] →
```

### Template E: Curiosity
```
Die meisten [Zielgruppe] machen diesen Fehler... 🤔

[Problem kurz beschreiben]

Wir zeigen dir, wie es besser geht.

[CTA] →
```

---

## Headline Templates

### Benefit-First
```
[Ergebnis] in [Zeitraum]
```
Beispiel: "Mehr Leads in 30 Tagen"

### How-To
```
So erreichst du [Ergebnis]
```
Beispiel: "So verdoppelst du deinen Traffic"

### Number
```
[Zahl] Wege zu [Ergebnis]
```
Beispiel: "5 Wege zu mehr Conversions"

### Question
```
Bereit für [Ergebnis]?
```
Beispiel: "Bereit für mehr Umsatz?"

### Social Proof
```
Von [Zahl]+ [Zielgruppe] empfohlen
```
Beispiel: "Von 2.000+ Marketern empfohlen"

---

## Description Templates

```
[Angebot kurz] | [Trust-Element]
```
Beispiele:
- "Kostenlos testen | Keine Kreditkarte"
- "14 Tage gratis | Jederzeit kündbar"
- "Ab 29€/Monat | Made in Germany"

---

## Output-Format

```json
{
  "platform": "meta",
  "ad_type": "single_image",
  "variations": [
    {
      "variation_name": "A - PAS",
      "primary_text": "[Max 125 Zeichen sichtbar]",
      "headline": "[Max 40 Zeichen]",
      "description": "[Max 30 Zeichen]",
      "cta_button": "Learn More",
      "image_prompt": "[Beschreibung für Bild-Generierung]"
    },
    {
      "variation_name": "B - Social Proof",
      "primary_text": "...",
      "headline": "...",
      "description": "...",
      "cta_button": "Sign Up",
      "image_prompt": "..."
    },
    {
      "variation_name": "C - Direct Benefit",
      "primary_text": "...",
      "headline": "...",
      "description": "...",
      "cta_button": "Get Offer",
      "image_prompt": "..."
    }
  ]
}
```

---

## Beispiel-Output

**Input:** SaaS Content-Tool, Ziel: Free Trial Signups

```json
{
  "platform": "meta",
  "ad_type": "single_image",
  "objective": "conversions",
  "variations": [
    {
      "variation_name": "A - Problem/Pain",
      "primary_text": "Content-Erstellung frisst deine Zeit? 😤\n\nStunden für einen Blog-Post. Tage für einen Content-Plan. Wochen bis zum Ergebnis.\n\nMit ContentAI erstellst du professionellen Content in Minuten.\n\n✓ KI-generierte Texte\n✓ Automatische Planung\n✓ SEO-optimiert\n\n14 Tage kostenlos testen 👇",
      "headline": "Content erstellen in Minuten",
      "description": "14 Tage gratis | Keine Karte",
      "cta_button": "Sign Up",
      "image_prompt": "Frustrated marketer at desk with clock, then happy marketer with completed content, split image, modern office, clean design"
    },
    {
      "variation_name": "B - Social Proof",
      "primary_text": "2.000+ Marketing-Teams sparen 15 Stunden pro Woche. 💪\n\n\"ContentAI hat unsere Content-Produktion revolutioniert. Wir erstellen jetzt 3x mehr Content bei gleichem Team.\" - Sarah M., Marketing Lead\n\nDu bist als Nächstes dran.\n\nKostenlos starten →",
      "headline": "Von 2.000+ Teams genutzt",
      "description": "4.8/5 Sterne | Gratis testen",
      "cta_button": "Learn More",
      "image_prompt": "Happy diverse marketing team celebrating, modern office, screens showing content dashboard, professional but warm atmosphere"
    },
    {
      "variation_name": "C - Direct Benefit",
      "primary_text": "10x mehr Content. Null extra Aufwand. ⚡\n\nKein stundenlanges Schreiben.\nKein teures Outsourcing.\nNur professioneller Content auf Knopfdruck.\n\n14 Tage kostenlos - keine Kreditkarte nötig.\n\nJetzt starten →",
      "headline": "10x schneller Content erstellen",
      "description": "Kostenlos starten | DSGVO-konform",
      "cta_button": "Sign Up",
      "image_prompt": "Clean product mockup showing content AI interface, before/after comparison, modern minimal design, brand colors navy and orange"
    }
  ]
}
```

---

## A/B Testing Empfehlung

Teste diese Elemente gegeneinander:

| Test | Variation A | Variation B |
|------|-------------|-------------|
| Hook | Problem-fokussiert | Benefit-fokussiert |
| Social Proof | Zahlen (2.000+) | Quote/Testimonial |
| CTA | "Kostenlos testen" | "Mehr erfahren" |
| Emoji | Mit Emojis | Ohne Emojis |
| Image | Product Shot | Lifestyle/People |

---

## Checkliste

- [ ] Hook in ersten 125 Zeichen?
- [ ] Min. 3 Varianten erstellt?
- [ ] Headline ≤ 40 Zeichen?
- [ ] Description ≤ 30 Zeichen?
- [ ] CTA-Button passend zum Ziel?
- [ ] Bild-Prompt für jede Variation?
- [ ] Verschiedene Ansätze getestet (Pain, Benefit, Proof)?
- [ ] Compliance-Check bestanden?
