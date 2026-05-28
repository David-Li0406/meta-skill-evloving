# LinkedIn Sponsored Content Template

## Specs
- **Intro Text:** 600 Zeichen max (150 optimal für volle Sichtbarkeit)
- **Headline:** 70 Zeichen (60 empfohlen)
- **Description:** 100 Zeichen (oft nicht angezeigt)
- **Image:** 1200x627 (1.91:1)
- **CTA Button:** Vordefinierte Optionen

---

## CTA-Button Optionen

| Button | Beste für |
|--------|-----------|
| Learn More | Content, Awareness |
| Download | Whitepaper, Reports |
| Register | Webinare, Events |
| Sign Up | Free Trials, Newsletter |
| Apply Now | Jobs |
| Get Quote | B2B Services |
| Request Demo | SaaS, Enterprise |
| Subscribe | Subscriptions |

---

## Intro Text Templates (B2B-optimiert)

### Template A: Statistik-Hook
```
[Überraschende Statistik oder Zahl].

[Was das für die Zielgruppe bedeutet - 1-2 Sätze]

[Wie man das Problem löst/Chance nutzt]

👉 [CTA mit Link-Vorschau]
```

**Beispiel:**
```
73% der B2B-Käufer bevorzugen Self-Service gegenüber Vertriebsgesprächen.

Ist Ihr Vertriebsprozess darauf vorbereitet? Unternehmen, die digitale Buying Journeys anbieten, konvertieren 2x besser.

Unser neuer Report zeigt, wie führende B2B-Unternehmen sich anpassen.

👉 Kostenloser Download
```

### Template B: Thought Leadership
```
[Provokante These oder Beobachtung]

[Begründung/Erklärung - 2-3 Sätze]

[Einladung zum Austausch oder Ressource]
```

**Beispiel:**
```
Die meisten Content-Strategien scheitern nicht am Content - sondern an der Distribution.

Nach 200+ B2B-Projekten sehen wir immer wieder: Großartiger Content, der niemanden erreicht. Das Problem ist nicht die Qualität, sondern die Sichtbarkeit.

Wir haben unsere Learnings in einem Playbook zusammengefasst.
```

### Template C: Pain Point
```
[Problem als Frage an die Zielgruppe]

[Verstärkung des Problems - was es kostet/bedeutet]

[Lösung/Ressource anbieten]
```

**Beispiel:**
```
Verbringt Ihr Marketing-Team mehr Zeit mit Reporting als mit Strategie?

Laut unserer Umfrage gehen durchschnittlich 12 Stunden pro Woche für manuelle Reports verloren - Zeit, die für wertschöpfende Arbeit fehlt.

Erfahren Sie, wie automatisierte Dashboards das ändern.
```

### Template D: Success Story (kurz)
```
[Ergebnis das ein Kunde erzielt hat]

"[Kurzes Quote]" - [Name], [Titel] bei [Unternehmen]

[Einladung, mehr zu erfahren]
```

**Beispiel:**
```
+147% mehr qualifizierte Leads in 6 Monaten.

"Die Integration hat unseren gesamten Leadflow transformiert." - Thomas M., Head of Marketing bei TechCorp

Erfahren Sie, wie wir das erreicht haben.
```

### Template E: News/Trend
```
[Aktuelle Entwicklung oder Trend]

[Was das für die Zielgruppe bedeutet]

[Ressource oder Perspektive anbieten]
```

---

## Headline Templates (B2B)

### Daten-getrieben
```
[Zahl]% [Ergebnis] mit [Methode/Tool]
```
Beispiel: "47% mehr Leads mit Account-Based Marketing"

### How-To für Entscheider
```
Wie [Zielgruppe] [Ergebnis] erreicht
```
Beispiel: "Wie CMOs ihre Teams entlasten"

### Report/Whitepaper
```
[Thema]-Report 2024: [Key Finding]
```
Beispiel: "B2B-Vertrieb 2024: Die 5 größten Veränderungen"

### Thought Leadership
```
Warum [Status Quo] nicht mehr funktioniert
```
Beispiel: "Warum Cold Calling im B2B ausgedient hat"

### Direct Benefit
```
[Ergebnis] für [Zielgruppe]
```
Beispiel: "Mehr Pipeline für B2B-Vertriebsteams"

---

## Output-Format

```json
{
  "platform": "linkedin",
  "ad_type": "sponsored_content",
  "objective": "lead_generation|website_visits|engagement",
  "variations": [
    {
      "variation_name": "A - Statistik-Hook",
      "intro_text": "[Max 150 Zeichen für volle Sichtbarkeit]",
      "headline": "[Max 70 Zeichen]",
      "description": "[Max 100 Zeichen]",
      "cta_button": "Download",
      "image_prompt": "[Beschreibung für Bild-Generierung]",
      "targeting_suggestion": "[Empfohlenes Targeting]"
    }
  ]
}
```

---

## Beispiel-Output

**Input:** Marketing Automation Tool, Ziel: Demo Requests

```json
{
  "platform": "linkedin",
  "ad_type": "sponsored_content",
  "objective": "lead_generation",
  "variations": [
    {
      "variation_name": "A - Statistik-Hook",
      "intro_text": "Marketing-Teams verschwenden 40% ihrer Zeit mit repetitiven Tasks.\n\nAutomatisierung kann das ändern - aber nur 23% der Mittelständler nutzen sie effektiv.\n\nWir zeigen Ihnen in 30 Minuten, wie Sie dazugehören.",
      "headline": "Marketing-Automatisierung für den Mittelstand",
      "description": "30-Min Demo | Keine Verpflichtung",
      "cta_button": "Request Demo",
      "image_prompt": "Professional data visualization dashboard, marketing metrics, modern interface, navy blue color scheme with orange accents, clean corporate style",
      "targeting_suggestion": "Marketing Directors, CMOs | Company Size 50-500 | Industries: Tech, Manufacturing, Professional Services"
    },
    {
      "variation_name": "B - Pain Point",
      "intro_text": "Kommt Ihnen das bekannt vor?\n\n→ Leads fallen durch das Raster\n→ Follow-ups werden vergessen\n→ Reporting dauert Stunden\n\nMarketing-Automatisierung löst genau diese Probleme - wenn sie richtig implementiert wird.\n\nLassen Sie uns sprechen.",
      "headline": "Schluss mit verpassten Leads",
      "description": "Persönliche Demo in 30 Minuten",
      "cta_button": "Request Demo",
      "image_prompt": "Before/after comparison, chaotic desk vs organized dashboard, professional setting, transformation visual",
      "targeting_suggestion": "Marketing Managers, Demand Gen | Company Size 50-200 | Seniority: Manager+"
    },
    {
      "variation_name": "C - Social Proof",
      "intro_text": "\"Seit der Einführung sparen wir 15 Stunden pro Woche und haben unsere Lead-Qualität verdoppelt.\"\n\n- Sarah K., Marketing Lead bei TechSolutions GmbH\n\nÜber 200 Mittelständler automatisieren bereits mit uns.\n\nSind Sie dabei?",
      "headline": "200+ Mittelständler automatisieren mit uns",
      "description": "Erfahren Sie, wie | Demo buchen",
      "cta_button": "Learn More",
      "image_prompt": "Happy professional looking at laptop with positive metrics, modern office environment, authentic expression, testimonial style",
      "targeting_suggestion": "CMO, VP Marketing | Company Size 100-500 | Growth-oriented companies"
    }
  ]
}
```

---

## LinkedIn-spezifische Best Practices

### Tone of Voice
- Professionell aber nicht steif
- Datengetrieben
- Thought Leadership zeigen
- Keine übertriebenen Versprechen

### Engagement-Taktiken
- Fragen stellen (auch in Ads)
- Statistiken und Daten nutzen
- Branchen-spezifisch ansprechen
- Job-Titel der Zielgruppe erwähnen

### Was NICHT funktioniert
- Zu casual/locker
- Clickbait-Style
- Übertriebene Emojis
- "Wir sind die Besten" ohne Proof
- Lange Texte ohne Struktur

---

## Checkliste

- [ ] Intro Text ≤ 150 Zeichen für volle Sichtbarkeit?
- [ ] Headline ≤ 70 Zeichen?
- [ ] B2B-angemessener Ton?
- [ ] Daten/Social Proof enthalten?
- [ ] Min. 3 Varianten erstellt?
- [ ] CTA passend zum Kampagnenziel?
- [ ] Targeting-Empfehlung inklusive?
- [ ] Compliance für LinkedIn geprüft?
