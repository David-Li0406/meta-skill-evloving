# Single Article Newsletter Template

## Verwendung
Promotion eines einzelnen Artikels/Blog-Posts an die Email-Liste.

---

## Input
```
- article_title: Titel des Artikels
- article_url: URL zum Artikel
- article_summary: Kurzzusammenfassung
- key_takeaways: 3-5 Hauptpunkte
- target_audience: Zielgruppe
- sender_name: Name des Absenders
- sender_title: Position
```

---

## Output Format

```json
{
  "subject_lines": [
    {
      "text": "[Subject Line 1]",
      "type": "curiosity|benefit|question|number"
    },
    {
      "text": "[Subject Line 2]",
      "type": "..."
    },
    {
      "text": "[Subject Line 3]",
      "type": "..."
    }
  ],
  "preview_text": "[40-90 Zeichen Preview]",
  "email_body": {
    "greeting": "Hallo {{first_name}},",
    "hook": "[Erster Absatz - Aufmerksamkeit]",
    "main_content": "[Hauptteil mit Artikel-Einführung]",
    "takeaways": [
      "[Takeaway 1]",
      "[Takeaway 2]",
      "[Takeaway 3]"
    ],
    "cta": {
      "text": "[CTA Button Text]",
      "url": "[article_url]"
    },
    "signature": {
      "greeting": "Beste Grüße",
      "name": "[sender_name]",
      "title": "[sender_title]"
    },
    "ps": "[Optional P.S. Zeile]"
  }
}
```

---

## Template-Varianten

### Variante A: Problem-fokussiert

```
Hallo {{first_name}},

[Problem als Frage oder Aussage]?

Das ist ein Thema, das viele [Zielgruppe] beschäftigt. Und genau
deshalb habe ich diesen Artikel geschrieben:

👉 [Artikel-Titel]

Darin erfährst du:

• [Takeaway 1]
• [Takeaway 2]
• [Takeaway 3]

[CTA: Jetzt lesen →]

Beste Grüße,
[Name]

P.S. [Teaser für nächsten Artikel oder zusätzlicher Nutzen]
```

### Variante B: Story/Personal

```
Hallo {{first_name}},

[Kurze persönliche Story oder Beobachtung - 2 Sätze].

Das hat mich dazu gebracht, tiefer in [Thema] einzutauchen.
Das Ergebnis: Mein neuer Artikel "[Artikel-Titel]".

Was dich erwartet:

✓ [Takeaway 1]
✓ [Takeaway 2]
✓ [Takeaway 3]

[CTA: Zum Artikel →]

Lass mich wissen, was du davon hältst!

[Name]
```

### Variante C: Nutzen-fokussiert

```
Hallo {{first_name}},

Wusstest du, dass [überraschende Statistik oder Fakt]?

In meinem neuen Artikel zeige ich dir, wie du [Hauptnutzen].

📌 "[Artikel-Titel]"

Du lernst:

1. [Takeaway 1]
2. [Takeaway 2]
3. [Takeaway 3]

Lesezeit: ca. [X] Minuten

[CTA: Artikel lesen →]

Viel Erfolg bei der Umsetzung!
[Name]
```

---

## Beispiel-Output

**Input:**
- Artikel: "10 Content-Marketing-Strategien für mehr Traffic"
- URL: https://example.com/content-strategien
- Zielgruppe: Marketing-Manager

```json
{
  "subject_lines": [
    {
      "text": "10 Strategien, die deinen Traffic verdoppeln",
      "type": "number"
    },
    {
      "text": "Warum dein Content nicht performt (und wie du es änderst)",
      "type": "curiosity"
    },
    {
      "text": "{{first_name}}, das fehlt deiner Content-Strategie",
      "type": "personalized"
    }
  ],
  "preview_text": "Diese Strategien haben unseren Traffic um 147% gesteigert",
  "email_body": {
    "greeting": "Hallo {{first_name}},",
    "hook": "73% der B2B-Marketer sagen, dass Content Marketing funktioniert – aber nur 30% haben eine dokumentierte Strategie. Gehörst du zur ersten oder zweiten Gruppe?",
    "main_content": "Ich habe die letzten 3 Monate damit verbracht, die erfolgreichsten Content-Strategien zu analysieren. Das Ergebnis: Mein neuer Artikel mit 10 erprobten Strategien für mehr Traffic.\n\n👉 \"10 Content-Marketing-Strategien für mehr Traffic\"",
    "takeaways": [
      "Warum die 'Pillar Content'-Methode 3x mehr Traffic bringt",
      "Das optimale Verhältnis von SEO- zu Social-Content",
      "Wie du mit Repurposing 5x mehr aus jedem Artikel holst"
    ],
    "cta": {
      "text": "Jetzt lesen (5 Min Lesezeit)",
      "url": "https://example.com/content-strategien"
    },
    "signature": {
      "greeting": "Beste Grüße",
      "name": "Thomas",
      "title": "Head of Content"
    },
    "ps": "Nächste Woche: Wie wir unsere Email-Open-Rate auf 42% gesteigert haben."
  }
}
```

---

## Formatierter Email-Text

```
Hallo {{first_name}},

73% der B2B-Marketer sagen, dass Content Marketing funktioniert –
aber nur 30% haben eine dokumentierte Strategie.

Gehörst du zur ersten oder zweiten Gruppe?

Ich habe die letzten 3 Monate damit verbracht, die erfolgreichsten
Content-Strategien zu analysieren. Das Ergebnis:

👉 "10 Content-Marketing-Strategien für mehr Traffic"

Darin erfährst du:

• Warum die 'Pillar Content'-Methode 3x mehr Traffic bringt
• Das optimale Verhältnis von SEO- zu Social-Content
• Wie du mit Repurposing 5x mehr aus jedem Artikel holst

[BUTTON: Jetzt lesen (5 Min Lesezeit)]

Beste Grüße,
Thomas
Head of Content

P.S. Nächste Woche: Wie wir unsere Email-Open-Rate auf 42%
gesteigert haben. Stay tuned!
```

---

## Checkliste

- [ ] 3 Subject Line Varianten erstellt?
- [ ] Preview Text 40-90 Zeichen?
- [ ] Hook weckt Interesse?
- [ ] 3-5 klare Takeaways?
- [ ] Ein klarer CTA?
- [ ] Lesezeit angegeben?
- [ ] P.S. mit Mehrwert?
- [ ] Spam-Wörter vermieden?
