---
name: editorial-researcher
description: Researches and builds databases of journalists, editors, and influencers. Analyzes beats, coverage patterns, and contact preferences. Creates targeted media lists for PR campaigns. Use when building or updating journalist databases for outreach.
---

# Editorial Researcher

Recherchiert und pflegt Datenbanken von Journalisten, Redakteuren und Influencern.

## Quick Start

```
Input: Industrie + Thema + Region + Ziel-Publikationen
Output: Journalist-Profile + Kontaktdaten + Beat-Analyse + Media List
```

## Workflow

1. **Ziel definieren** → Welche Coverage brauchen wir?
2. **Publikationen identifizieren** → Relevante Medien finden
3. **Journalisten recherchieren** → Wer schreibt über unser Thema?
4. **Profile anlegen** → Kontaktdaten, Beat, History
5. **Priorisieren** → Tier 1, 2, 3 Einteilung
6. **Pflegen** → Regelmäßig aktualisieren

## Output Format

```json
{
  "research_project": {
    "name": "MarTech Journalisten DE",
    "industry": "Marketing Technology",
    "region": "DACH",
    "date": "2024-01-15"
  },
  "publications": [
    {
      "name": "t3n",
      "type": "Fachmedium",
      "tier": 1,
      "reach": "500k monthly",
      "focus": ["Digital Business", "Tech", "Marketing"],
      "journalists": [...]
    }
  ],
  "journalists": [
    {
      "id": "JOUR-001",
      "name": "Max Mustermann",
      "email": "m.mustermann@t3n.de",
      "phone": "+49...",
      "publication": "t3n",
      "position": "Senior Editor",
      "beats": ["Marketing Tech", "SaaS", "Automation"],
      "social": {
        "linkedin": "linkedin.com/in/maxmustermann",
        "twitter": "@maxmustermann"
      },
      "coverage_analysis": {
        "topics_covered": ["CRM", "Marketing Automation", "AI in Marketing"],
        "recent_articles": [
          {
            "title": "Die Zukunft von Marketing Automation",
            "url": "https://...",
            "date": "2024-01-10",
            "relevance": "high"
          }
        ],
        "writing_style": "analytical",
        "preferred_angle": "Trends und Daten"
      },
      "contact_preferences": {
        "best_channel": "email",
        "response_likelihood": "high",
        "previous_contact": null,
        "notes": "Bevorzugt Daten-basierte Pitches"
      },
      "tier": 1,
      "relevance_score": 0.92
    }
  ],
  "summary": {
    "total_journalists": 45,
    "tier_1": 10,
    "tier_2": 20,
    "tier_3": 15,
    "coverage_gaps": ["Podcast-Hosts", "Newsletter-Autoren"]
  }
}
```

## Recherche-Methoden

### 1. Publikations-Analyse

```
Schritt 1: Top-Publikationen identifizieren
├── Google: "[Branche] News"
├── Similar Web: Traffic-Daten
├── LinkedIn: Follower-Zahlen
└── Branchenverbände: Empfehlungen

Schritt 2: Redaktion analysieren
├── Impressum/Team-Seite
├── Autoren-Verzeichnis
├── LinkedIn Company Page
└── Bylines in Artikeln
```

### 2. Journalist-Research

```
Pro Journalist sammeln:
├── Name & Position
├── Email (Pattern erkennen)
├── LinkedIn-Profil
├── Twitter/X-Handle
├── Letzte 5-10 Artikel
├── Themen-Fokus (Beats)
└── Writing Style
```

### 3. Email-Pattern-Erkennung

```
Gängige Formate:
- vorname.nachname@publikation.de
- v.nachname@publikation.de
- vorname@publikation.de
- nachname@publikation.de
- redaktion@publikation.de (allgemein)

Tools zur Verifizierung:
- Hunter.io
- Voila Norbert
- Clearbit Connect
- NeverBounce
```

### 4. Social-Media-Analyse

```
LinkedIn:
- Aktuelle Position
- Vorherige Stationen
- Posts & Artikel
- Connections

Twitter/X:
- Bio (oft Beat-Beschreibung)
- Recent Tweets
- Engagement Patterns
- DM-Präferenz

Mastodon/Threads:
- Alternative Kontaktmöglichkeit
- Oft offener für Kontakt
```

## Datenbank-Struktur

### Journalist-Profil

```yaml
Stammdaten:
  name: "Max Mustermann"
  email: "m.mustermann@t3n.de"
  phone: "+49 30 123456" (optional)
  publication: "t3n"
  position: "Senior Editor"

Social:
  linkedin: "url"
  twitter: "@handle"
  other: []

Beats:
  primary: "Marketing Technology"
  secondary: ["SaaS", "Automation", "AI"]
  avoids: ["Hardware", "Gaming"]

Coverage:
  recent_articles: []
  topics_written: []
  writing_style: "analytical/narrative/technical"
  avg_article_length: "1000-2000 Wörter"

Contact:
  preferred_channel: "email"
  best_time: "mornings"
  response_history: []
  notes: "Freier Text"

Classification:
  tier: 1
  relevance_score: 0.92
  last_updated: "2024-01-15"
```

### Publikations-Profil

```yaml
Stammdaten:
  name: "t3n"
  url: "https://t3n.de"
  type: "Online-Fachmedium"

Metrics:
  monthly_traffic: "500k"
  social_followers:
    linkedin: 50000
    twitter: 100000
  domain_authority: 75

Focus:
  industries: ["Digital Business", "Tech", "Startups"]
  topics: ["Marketing", "Development", "Karriere"]
  audience: "Digital Professionals, Entscheider"

Team:
  total_journalists: 25
  key_contacts: []

Submission:
  accepts_pitches: true
  pitch_email: "redaktion@t3n.de"
  guest_posts: true
  advertorials: true
```

## Tier-Klassifizierung

### Tier 1 - Priority

```
Kriterien:
- Nationale/Internationale Top-Medien
- Hohe Reichweite (100k+ monatlich)
- Direkter Beat-Match
- Nachgewiesene Coverage ähnlicher Themen

Beispiele:
- Handelsblatt, FAZ, Spiegel
- t3n, Gründerszene für Tech/Startup
- Branchenführende Fachmedien

Outreach: Persönlich, stark personalisiert
```

### Tier 2 - Important

```
Kriterien:
- Etablierte Fachmedien
- Mittlere Reichweite (20-100k)
- Guter Beat-Match
- Regelmäßige relevante Coverage

Beispiele:
- Spezialisierte B2B-Magazine
- Regionale Wirtschaftsmedien
- Beliebte Branchenblogs

Outreach: Semi-personalisiert
```

### Tier 3 - Nice to Have

```
Kriterien:
- Nischen-Publikationen
- Kleinere Reichweite (<20k)
- Partieller Beat-Match
- Gelegentlich relevant

Beispiele:
- Lokale Medien
- Kleine Fachblogs
- Nischen-Newsletter

Outreach: Template-basiert mit leichter Anpassung
```

## Pflege & Updates

### Wöchentlich

```
- Neue Artikel der Top-Journalisten prüfen
- Social-Media-Aktivität checken
- Neue Journalisten identifizieren
```

### Monatlich

```
- Kontaktdaten verifizieren
- Positions-Änderungen updaten
- Neue Publikationen hinzufügen
- Inaktive Profile markieren
```

### Quartalsweise

```
- Tier-Einteilung überprüfen
- Coverage-Analyse aktualisieren
- Lücken identifizieren
- Neue Beats/Themen hinzufügen
```

## Tools & Ressourcen

### Research-Tools

```
Journalist-Datenbanken:
- Muck Rack (paid)
- Cision (enterprise)
- Meltwater (enterprise)
- Presseportal.de (kostenlos)

Email-Finder:
- Hunter.io
- Voila Norbert
- Snov.io
- Apollo.io

Verification:
- NeverBounce
- ZeroBounce
- Bouncer
```

### Monitoring

```
Google Alerts:
- "[Journalist Name]"
- "site:publikation.de [Thema]"

Social Listening:
- Mention.com
- Brand24
- Hootsuite

News Aggregation:
- Feedly
- Flipboard
- Google News
```

## Quality-Checks

### Datenqualität

```
Jeder Eintrag muss haben:
✅ Verifizierte Email
✅ Aktuelle Position (letzte 3 Monate)
✅ Mindestens 2 relevante Artikel
✅ Beat-Klassifizierung
✅ Tier-Einteilung

Red Flags:
❌ Keine Artikel in 6+ Monaten
❌ Position geändert (LinkedIn)
❌ Email bouncet
❌ "Do not contact" Notiz
```

### Relevanz-Scoring

```
Score = (Beat Match × 0.4) +
        (Recent Coverage × 0.3) +
        (Publication Tier × 0.2) +
        (Response History × 0.1)

0.8-1.0: Sehr relevant (Tier 1)
0.6-0.8: Relevant (Tier 2)
0.4-0.6: Möglicherweise relevant (Tier 3)
<0.4: Nicht priorisieren
```

## Export-Formate

### Media List (CSV)

```csv
Name,Email,Publication,Position,Beats,Tier,Score,LinkedIn,Twitter,Notes
Max Mustermann,m.mustermann@t3n.de,t3n,Senior Editor,"MarTech,SaaS",1,0.92,url,@handle,Daten-basiert
```

### Pitch-Ready List

```markdown
## Tier 1 - Sofort kontaktieren

### Max Mustermann | t3n
- **Email:** m.mustermann@t3n.de
- **Beat:** Marketing Tech, SaaS
- **Recent:** "Die Zukunft von Marketing Automation" (Jan 2024)
- **Angle:** Daten und Trends
- **Notes:** Antwortet schnell auf gut recherchierte Pitches
```

## Checkliste

### Research-Phase
- [ ] Ziel-Publikationen definiert?
- [ ] Journalisten identifiziert?
- [ ] Kontaktdaten verifiziert?
- [ ] Social Profile gefunden?
- [ ] Artikel analysiert?

### Datenbank-Qualität
- [ ] Alle Pflichtfelder ausgefüllt?
- [ ] Tier-Klassifizierung?
- [ ] Relevanz-Score berechnet?
- [ ] Duplikate entfernt?
- [ ] Aktualisierungsdatum?

### Export-Ready
- [ ] Media List erstellt?
- [ ] Pitch-Notizen ergänzt?
- [ ] Team-Zugang eingerichtet?
- [ ] Tracking vorbereitet?
