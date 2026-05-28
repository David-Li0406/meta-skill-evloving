---
name: press-outreach-bot
description: Automates journalist research, media list building, and personalized outreach. Finds relevant journalists based on beat, previous coverage, and publication. Generates customized pitch emails with proper follow-up sequences. Use when distributing press releases or seeking media coverage.
---

# Press Outreach Bot

Automatisierte Journalisten-Recherche und personalisierter Outreach für PR-Kampagnen.

## Quick Start

```
Input: Press Release / Story Angle + Industrie + Region
Output: Journalisten-Liste + Personalisierte Pitches + Follow-Up Sequenz
```

## Workflow

1. **Story definieren** → Kern-Message und Newsworthy-Faktor identifizieren
2. **Journalisten recherchieren** → Basierend auf Beat, Publication, bisherige Coverage
3. **Media List erstellen** → Priorisierte Liste mit Kontaktdaten
4. **Pitches personalisieren** → Individuell auf jeden Journalisten zugeschnitten
5. **Outreach starten** → Emails versenden mit Tracking
6. **Follow-Up automatisieren** → Strukturierte Nachfass-Sequenz
7. **Ergebnisse tracken** → Opens, Replies, Coverage

## Output Format

```json
{
  "campaign": {
    "name": "Product Launch Q1 2024",
    "story_angle": "Erste KI-gestützte Lösung für...",
    "target_coverage": 10,
    "timeline": "2 weeks"
  },
  "media_list": [
    {
      "journalist": {
        "name": "Max Mustermann",
        "email": "m.mustermann@techpublication.de",
        "publication": "TechPublication",
        "beat": ["SaaS", "Marketing Tech", "AI"],
        "tier": 1,
        "linkedin": "linkedin.com/in/maxmustermann",
        "twitter": "@maxmustermann"
      },
      "relevance": {
        "score": 0.92,
        "reasons": [
          "Schreibt regelmäßig über Marketing-Tech",
          "Hat kürzlich über ähnliches Produkt berichtet",
          "Interesse an AI-Themen (3 Artikel in 30 Tagen)"
        ],
        "recent_articles": [
          {
            "title": "Die Zukunft von Marketing Automation",
            "url": "https://...",
            "date": "2024-01-10"
          }
        ]
      },
      "pitch": {
        "subject_line": "Exklusiv: Erste KI-Lösung für [Bereich]",
        "body": "Personalisierter Pitch...",
        "personalization_hooks": [
          "Bezug auf Artikel über Marketing Automation",
          "Interesse an AI erwähnt"
        ]
      }
    }
  ],
  "outreach_sequence": {
    "day_1": "Initial Pitch",
    "day_4": "Follow-Up 1 (Value Add)",
    "day_8": "Follow-Up 2 (Social Proof)",
    "day_14": "Final Follow-Up"
  }
}
```

## Journalisten-Recherche

### Recherche-Quellen

| Quelle | Typ | Daten |
|--------|-----|-------|
| LinkedIn | Profil | Name, Publikation, Kontakte |
| Twitter/X | Social | Beat, Interessen, Kontakt |
| Muck Rack | Database | Kontaktdaten, Artikel-History |
| Cision | Database | Full Contact Info, Beats |
| Publikations-Websites | Direct | Autoren-Profile, Recent Articles |
| Google News | Search | Recent Coverage nach Topic |

Details: [RESEARCH_METHODS.md](RESEARCH_METHODS.md)

### Journalist-Scoring

```
Relevanz-Score =
  (Beat Match × 0.35) +
  (Recent Coverage × 0.25) +
  (Publication Tier × 0.20) +
  (Response History × 0.10) +
  (Social Activity × 0.10)
```

### Tier-System

| Tier | Beschreibung | Beispiele |
|------|--------------|-----------|
| 1 | Nationale Top-Medien | Handelsblatt, FAZ, Spiegel |
| 2 | Fach-Leitmedien | t3n, OMR, Gründerszene |
| 3 | Branchenmedien | Fachmagazine, Verticals |
| 4 | Blogger/Influencer | Relevante Blogs, Podcasts |
| 5 | Lokale/Nische | Regionalmedien, Spezial-Blogs |

## Pitch-Personalisierung

### Personalisierungs-Hooks

1. **Artikel-Referenz**
   ```
   "Ihr Artikel über [Thema] hat mich angesprochen, weil..."
   ```

2. **Beat-Connection**
   ```
   "Als jemand, der regelmäßig über [Beat] schreibt..."
   ```

3. **Timing-Hook**
   ```
   "Passend zu Ihrer kürzlichen Serie über [Thema]..."
   ```

4. **Social Proof**
   ```
   "Kollegen von [ähnliche Publikation] fanden das spannend..."
   ```

5. **Exklusivitäts-Angebot**
   ```
   "Ich möchte Ihnen exklusiv vor dem offiziellen Launch..."
   ```

Details: [PITCH_TEMPLATES.md](PITCH_TEMPLATES.md)

### Subject Line Formeln

```
Newsworthy:
"[Publikation] Exklusiv: [News-Hook]"
"Erste [Innovation] in [Branche]"
"Daten: [Überraschendes Finding]"

Personal:
"Re: Ihr Artikel über [Thema]"
"Für Ihre [Beat]-Coverage"
"[Gemeinsamer Kontakt] empfahl den Kontakt"

Curiosity:
"Warum [Trend] sich gerade ändert"
"Die Zahlen hinter [Phänomen]"
```

## Follow-Up Sequenz

Details: [FOLLOW_UP_TEMPLATES.md](FOLLOW_UP_TEMPLATES.md)

### Timing

```
Tag 1: Initial Pitch
├── Morgens (Di-Do, 9-10 Uhr)
├── Nicht: Montag, Freitag, Wochenende

Tag 3-4: Follow-Up 1
├── "Quick follow-up" mit zusätzlichem Value
├── Neuer Angle oder Daten

Tag 7-8: Follow-Up 2
├── Social Proof hinzufügen
├── "Andere Publikation X hat berichtet..."

Tag 14: Final Follow-Up
├── "Letzter Check" - respektvoll schließen
├── Offen für zukünftige Stories
```

### Anti-Patterns

```
❌ Mehr als 3 Follow-Ups
❌ Follow-Up am selben Tag
❌ Wochenend-Emails
❌ "Checking in" ohne Value
❌ Guilt-Tripping ("Sie antworten nicht...")
```

## Integration

### Mit CRM/Database

```typescript
// Journalisten-Daten speichern
await supabase.from('journalists').upsert({
  name: journalist.name,
  email: journalist.email,
  publication: journalist.publication,
  beats: journalist.beats,
  last_contacted: new Date(),
  response_status: 'pending'
});
```

### Mit Email-Tools

```typescript
// Outreach-Sequenz starten
await emailSequencer.start({
  recipient: journalist.email,
  sequence: [
    { delay: 0, template: 'initial_pitch' },
    { delay: '3d', template: 'follow_up_1' },
    { delay: '7d', template: 'follow_up_2' }
  ],
  trackOpens: true,
  trackClicks: true
});
```

## Tracking & Reporting

### KPIs

| Metrik | Ziel | Berechnung |
|--------|------|------------|
| Open Rate | >40% | Opens / Sent |
| Reply Rate | >15% | Replies / Sent |
| Coverage Rate | >5% | Articles / Contacted |
| Positive Response | >25% | Positive / Replies |

### Pipeline-Tracking

```
Contacted → Opened → Replied → Interested → Coverage
   100    →   45   →   18   →     8     →    4
```

## Checkliste

- [ ] Story-Angle klar und newsworthy?
- [ ] Journalisten zum Beat passend?
- [ ] Pitches personalisiert (nicht generisch)?
- [ ] Timing beachtet (nicht Montag/Freitag)?
- [ ] Follow-Up-Sequenz geplant?
- [ ] Tracking aktiviert?
- [ ] Exclusivity-Angebote bedacht?
- [ ] Assets bereit (Bilder, Daten, Zitate)?
