# Standard Press Release Template

## Input-Anforderungen

```
- source_article: Pillar Content (Markdown)
- company_name: Firmenname
- company_description: Kurzbeschreibung
- news_type: product_launch | partnership | milestone | study | event
- spokesperson: Name, Titel
- contact_person: Name, Email, Telefon
- key_facts: Liste der wichtigsten Fakten
```

---

## Output-Format

```json
{
  "press_release": {
    "headline": {
      "main": "[Max 80 Zeichen]",
      "sub": "[Optional, max 100 Zeichen]"
    },
    "dateline": "[STADT], [Tag]. [Monat] [Jahr] –",
    "lead": "[1-2 Sätze mit 5 W's]",
    "body": [
      "[Absatz 1: Erweitert Lead]",
      "[Absatz 2: Kontext/Hintergrund]",
      "[Absatz 3: Details]"
    ],
    "primary_quote": {
      "text": "[Zitat]",
      "attribution": "[Name], [Position] bei [Firma]"
    },
    "secondary_quote": {
      "text": "[Optional: Zitat von Partner/Kunde]",
      "attribution": "[Name], [Position] bei [Firma]"
    },
    "closing": "[Verfügbarkeit/Next Steps]",
    "boilerplate": "[Über [Firma]...]",
    "media_contact": {
      "name": "[Name]",
      "position": "[Position]",
      "email": "[Email]",
      "phone": "[Telefon]"
    }
  },
  "metadata": {
    "word_count": 400,
    "target_media": ["Fachmedien", "Wirtschaftspresse"],
    "embargo": null,
    "assets": ["Produktbild", "Logo", "Headshot CEO"]
  },
  "pitch_variants": [
    {
      "target": "Fachmedien [Branche]",
      "angle": "[Spezifischer Winkel für diese Medien]",
      "subject_line": "[Email-Betreff für Pitch]"
    },
    {
      "target": "Wirtschaftspresse",
      "angle": "[Business-Angle]",
      "subject_line": "[Email-Betreff]"
    },
    {
      "target": "Regionalmedien",
      "angle": "[Lokaler Bezug]",
      "subject_line": "[Email-Betreff]"
    }
  ]
}
```

---

## Vollständiges Beispiel

**Input:**
- Artikel über "10 Content-Marketing-Strategien"
- ContentAI GmbH
- News-Typ: Studie

**Output:**

```json
{
  "press_release": {
    "headline": {
      "main": "Studie: 73% der Marketing-Teams planen KI-Einsatz für Content",
      "sub": "ContentAI-Report zeigt Wandel im B2B-Marketing"
    },
    "dateline": "BERLIN, 15. Januar 2024 –",
    "lead": "Eine neue Studie der ContentAI GmbH zeigt: Drei von vier Marketing-Teams planen, bis Ende 2024 KI-Tools für die Content-Erstellung einzusetzen. Der Report basiert auf einer Befragung von 500 Marketing-Entscheidern in der DACH-Region.",
    "body": [
      "Die Studie „Content Marketing Trends 2024" untersuchte, wie B2B-Unternehmen ihre Content-Strategien anpassen. Zentrale Erkenntnis: Der Druck, mehr Content in kürzerer Zeit zu produzieren, treibt die KI-Adoption voran. 68% der Befragten gaben an, dass ihr Content-Bedarf im vergangenen Jahr gestiegen ist, während die Budgets stagnierten.",
      "Weitere Ergebnisse der Studie: 45% der Unternehmen haben bereits KI-Tools im Einsatz, weitere 28% planen die Einführung innerhalb der nächsten 12 Monate. Als größte Hürden werden Qualitätsbedenken (52%) und fehlende interne Expertise (41%) genannt.",
      "Der vollständige Report mit allen Ergebnissen und Handlungsempfehlungen steht ab sofort zum kostenlosen Download bereit unter www.contentai.de/studie-2024."
    ],
    "primary_quote": {
      "text": "Die Ergebnisse zeigen einen klaren Trend: Marketing-Teams suchen nach Wegen, effizienter zu arbeiten, ohne bei der Qualität Kompromisse einzugehen. KI ist dabei kein Ersatz für Kreativität, sondern ein Werkzeug, das Teams entlastet und ihnen mehr Zeit für strategische Arbeit gibt.",
      "attribution": "Dr. Anna Schmidt, CEO der ContentAI GmbH"
    },
    "secondary_quote": null,
    "closing": "Der Report „Content Marketing Trends 2024" steht zum kostenlosen Download bereit. Interessierte Journalisten erhalten auf Anfrage Zugang zu den vollständigen Studiendaten.",
    "boilerplate": "ContentAI ist eine KI-gestützte Content-Marketing-Plattform für B2B-Unternehmen. Die 2021 in Berlin gegründete Firma unterstützt über 2.000 Marketing-Teams dabei, professionellen Content in einem Bruchteil der Zeit zu erstellen. Mehr unter www.contentai.de.",
    "media_contact": {
      "name": "Thomas Müller",
      "position": "Head of Communications",
      "email": "presse@contentai.de",
      "phone": "+49 30 1234567"
    }
  },
  "metadata": {
    "word_count": 387,
    "target_media": ["Marketing-Fachmedien", "Wirtschaftspresse", "Tech-Blogs"],
    "embargo": null,
    "assets": ["Infografik Key Findings", "Logo", "Headshot CEO"]
  },
  "pitch_variants": [
    {
      "target": "Marketing-Fachmedien",
      "angle": "Wie sich Content-Marketing-Teams auf KI vorbereiten",
      "subject_line": "Exklusiv: 73% der Marketing-Teams setzen 2024 auf KI – neue Studie"
    },
    {
      "target": "Wirtschaftspresse",
      "angle": "KI-Adoption im Mittelstand: Marketing als Vorreiter",
      "subject_line": "Studie: B2B-Marketing wird zum KI-Pionier"
    },
    {
      "target": "HR/Arbeitswelt-Medien",
      "angle": "Wie KI Marketing-Jobs verändert (nicht ersetzt)",
      "subject_line": "Studie zeigt: KI entlastet Marketing-Teams statt Jobs zu kosten"
    }
  ]
}
```

---

## Text-Ausgabe (für Copy/Paste)

```markdown
# Studie: 73% der Marketing-Teams planen KI-Einsatz für Content

**ContentAI-Report zeigt Wandel im B2B-Marketing**

BERLIN, 15. Januar 2024 – Eine neue Studie der ContentAI GmbH zeigt: Drei von vier Marketing-Teams planen, bis Ende 2024 KI-Tools für die Content-Erstellung einzusetzen. Der Report basiert auf einer Befragung von 500 Marketing-Entscheidern in der DACH-Region.

Die Studie „Content Marketing Trends 2024" untersuchte, wie B2B-Unternehmen ihre Content-Strategien anpassen. Zentrale Erkenntnis: Der Druck, mehr Content in kürzerer Zeit zu produzieren, treibt die KI-Adoption voran. 68% der Befragten gaben an, dass ihr Content-Bedarf im vergangenen Jahr gestiegen ist, während die Budgets stagnierten.

Weitere Ergebnisse der Studie: 45% der Unternehmen haben bereits KI-Tools im Einsatz, weitere 28% planen die Einführung innerhalb der nächsten 12 Monate. Als größte Hürden werden Qualitätsbedenken (52%) und fehlende interne Expertise (41%) genannt.

„Die Ergebnisse zeigen einen klaren Trend: Marketing-Teams suchen nach Wegen, effizienter zu arbeiten, ohne bei der Qualität Kompromisse einzugehen. KI ist dabei kein Ersatz für Kreativität, sondern ein Werkzeug, das Teams entlastet und ihnen mehr Zeit für strategische Arbeit gibt", sagt Dr. Anna Schmidt, CEO der ContentAI GmbH.

Der vollständige Report mit allen Ergebnissen und Handlungsempfehlungen steht ab sofort zum kostenlosen Download bereit unter www.contentai.de/studie-2024.

---

### Über ContentAI

ContentAI ist eine KI-gestützte Content-Marketing-Plattform für B2B-Unternehmen. Die 2021 in Berlin gegründete Firma unterstützt über 2.000 Marketing-Teams dabei, professionellen Content in einem Bruchteil der Zeit zu erstellen. Mehr unter www.contentai.de.

### Pressekontakt

Thomas Müller
Head of Communications
ContentAI GmbH
E-Mail: presse@contentai.de
Telefon: +49 30 1234567
```

---

## Checkliste vor Versand

- [ ] Headline ≤ 80 Zeichen?
- [ ] Lead beantwortet 5 W's?
- [ ] Alle Fakten korrekt und aktuell?
- [ ] Zitat freigegeben?
- [ ] Boilerplate aktuell?
- [ ] Kontaktdaten korrekt?
- [ ] Keine Tippfehler?
- [ ] Assets vorbereitet (Bilder, Logo)?
- [ ] Pitch-Emails vorbereitet?
