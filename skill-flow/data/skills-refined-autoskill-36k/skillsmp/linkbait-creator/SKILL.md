---
name: linkbait-creator
description: Creates viral, shareable content designed to attract natural backlinks. Generates data studies, interactive tools, controversial takes, and visual assets that journalists and bloggers want to reference. Use when you need content specifically designed for link acquisition.
---

# Linkbait Creator

Erstellt Inhalte, die natürliche Backlinks anziehen durch Mehrwert, Originalität und Shareability.

## Quick Start

```
Input: Topic + Industrie + Zielgruppe (Journalisten/Blogger)
Output: Linkbait-Konzept + Ausgearbeiteter Content + Outreach-Pitch
```

## Linkbait-Typen

| Typ | Beschreibung | Link-Potenzial | Aufwand |
|-----|--------------|----------------|---------|
| Data Study | Original-Daten, Statistiken | Sehr hoch | Hoch |
| Interactive Tool | Rechner, Quiz, Checker | Sehr hoch | Hoch |
| Definitive Guide | Ultimativer Leitfaden | Hoch | Mittel |
| Expert Roundup | Experten-Meinungen | Hoch | Mittel |
| Infographic | Visuelle Datenaufbereitung | Hoch | Mittel |
| Controversy | Kontroverse These | Mittel-Hoch | Niedrig |
| Resource List | Kuratierte Listen | Mittel | Niedrig |
| Case Study | Erfolgsgeschichte mit Zahlen | Mittel | Mittel |

Details: [LINKBAIT_TYPES.md](LINKBAIT_TYPES.md)

## Workflow

1. **Topic-Analyse** → Keyword + Wettbewerb + Link-Gap analysieren
2. **Format wählen** → Passenden Linkbait-Typ auswählen
3. **Unique Angle finden** → Was macht den Content einzigartig?
4. **Content erstellen** → Hochwertig, gut recherchiert, visuell ansprechend
5. **Assets erstellen** → Embeddable graphics, shareable snippets
6. **Outreach vorbereiten** → Pitch-Templates für Journalisten

## Output Format

```json
{
  "linkbait": {
    "title": "State of [Industry] Report 2024",
    "type": "data_study",
    "unique_angle": "Erste Studie zu [spezifischem Aspekt]",
    "target_audience": ["Tech-Journalisten", "Marketing-Blogger"],
    "key_findings": [
      "72% der Unternehmen...",
      "Der Markt wächst um 34%..."
    ],
    "embeddable_assets": [
      {
        "type": "infographic",
        "title": "Key Findings Infographic",
        "embed_code": "<iframe>...</iframe>"
      },
      {
        "type": "chart",
        "title": "Market Growth 2020-2024",
        "embed_code": "<img src='...'>"
      }
    ],
    "shareable_snippets": [
      {
        "platform": "twitter",
        "text": "🔬 Neue Studie: 72% der Unternehmen... [Link]"
      }
    ],
    "outreach": {
      "subject_line": "Exklusive Daten: [Industry] Report 2024",
      "pitch_template": "Hi [Name],\n\nwir haben gerade..."
    }
  }
}
```

## Erfolgs-Kriterien

### Was macht guten Linkbait?

1. **Originalität** - Neue Daten, neue Perspektive
2. **Zitierbarkeit** - Leicht zu referenzieren
3. **Glaubwürdigkeit** - Fundierte Methodik
4. **Visualität** - Teilbare Grafiken
5. **Aktualität** - Timely, relevant

### Red Flags (vermeiden!)

- Clickbait ohne Substanz
- Kopierte Daten anderer
- Übertriebene Claims
- Schlechte Quellenarbeit
- Nur für SEO, nicht für Menschen

## Promotion-Strategie

Details: [PROMOTION_PLAYBOOK.md](PROMOTION_PLAYBOOK.md)

```
Week 1: Pre-Launch
├── Teaser auf Social Media
├── Vorab-Zugang für Key Influencer
└── Medien-Embargo vorbereiten

Week 2: Launch
├── Blog-Post veröffentlichen
├── Press Release versenden
├── Social Media Push
└── Outreach an Journalisten

Week 3-4: Amplification
├── Guest Posts auf anderen Blogs
├── HARO-Anfragen beantworten
├── Community-Seeding (Reddit, Foren)
└── Paid Promotion (optional)
```

## Checkliste

- [ ] Unique Angle identifiziert?
- [ ] Quellenarbeit dokumentiert?
- [ ] Daten verifizierbar?
- [ ] Embeddable Assets erstellt?
- [ ] Outreach-Liste vorbereitet?
- [ ] Social Snippets geschrieben?
- [ ] Promotion-Kalender geplant?
