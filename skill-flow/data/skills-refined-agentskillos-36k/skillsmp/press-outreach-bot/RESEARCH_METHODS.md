# Journalisten-Recherche Methoden

## Übersicht

```
Ziel: Relevante Journalisten finden, die über dein Thema schreiben
      und aktuell für Pitches empfänglich sind.
```

---

## 1. Google News Search

### Methode

```
1. Suche nach Keywords + "site:publikation.de"
2. Filter: Letzte 30 Tage
3. Identifiziere wiederkehrende Autorennamen
4. Extrahiere Kontaktdaten aus Autorenprofile
```

### Suchoperatoren

```
"[Thema]" site:t3n.de
"[Thema]" site:handelsblatt.com
"[Thema]" inurl:autor
"[Thema]" "Kontakt" OR "Email"
```

### Beispiel

```
Thema: "Marketing Automation"

Suchen:
- "Marketing Automation" site:t3n.de
- "Marketing Automation" site:gruenderszene.de
- "Marketing Automation" site:omr.com

Ergebnis: Liste von Artikeln + Autoren
```

---

## 2. LinkedIn Recherche

### Methode

```
1. Sales Navigator nutzen (wenn verfügbar)
2. Suche: "Journalist" + "[Publikation]"
3. Filter: Standort, aktuelle Position
4. Verbindungsanfrage oder InMail
```

### Suchfilter

```
Keywords: Journalist, Redakteur, Editor, Reporter, Autor
Current Company: [Publikation]
Location: Deutschland / DACH
Industry: Media & Communications
```

### Kontaktaufnahme

```
Verbindungsanfrage (kurz):
"Hi [Name], ich folge Ihrer Berichterstattung über [Beat]
bei [Publikation] - würde mich freuen, uns zu vernetzen."

InMail (wenn Premium):
[Siehe Pitch-Templates]
```

---

## 3. Twitter/X Recherche

### Methode

```
1. Suche nach Publikations-Handles
2. "Followers" der Publikation durchsuchen
3. Bio-Keywords: "Journalist", "Reporter", "Schreibe über"
4. Listen von Journalisten finden
```

### Suchoperatoren

```
from:@publikation filter:replies
"journalist" "[publikation]" -filter:retweets
"schreibe über" "[thema]"
```

### Twitter-Listen

```
Viele Publikationen haben öffentliche Listen:
- @handelsblatt/team
- @t3n/redaktion
- @slopeone/german-tech-journalists
```

### Engagement-Recherche

```
1. Wer retweetet/kommentiert zu [Thema]?
2. Wer nutzt Hashtags wie #MarTech #SaaS?
3. Wer hat kürzlich nach Story-Ideen gefragt?
```

---

## 4. Muck Rack / Cision

### Muck Rack (wenn Zugang)

```
Features:
- Journalisten-Database nach Beat
- Kontaktdaten verifiziert
- Artikel-History
- Pitch-Tracking

Workflow:
1. Search by Beat/Topic
2. Filter by Publication Tier
3. Export Media List
4. Track Pitches in Platform
```

### Cision (Enterprise)

```
Features:
- Größte Journalisten-Datenbank
- Medienbeobachtung
- Distribution
- Analytics

Ideal für: Große PR-Kampagnen, regelmäßige Pressearbeit
```

---

## 5. Publikations-Websites

### Autorenprofile

```
Typische URLs:
- /autor/[name]
- /team
- /impressum
- /redaktion

Extrahieren:
- Bio & Beat-Beschreibung
- Soziale Profile
- Email (manchmal)
- Recent Articles
```

### Beispiel-Struktur

```
Handelsblatt: handelsblatt.com/autoren/[name]
t3n: t3n.de/autoren/[name]
Spiegel: spiegel.de/impressum/autor-[id].html
```

### Kontakt-Patterns

```
Email-Formate erkennen:
vorname.nachname@publikation.de
v.nachname@publikation.de
vorname@publikation.de
redaktion+[name]@publikation.de

Tools zur Verifizierung:
- Hunter.io
- Voila Norbert
- Clearbit Connect
```

---

## 6. HARO / Journalisten-Anfragen

### Help a Reporter Out (HARO)

```
1. Kostenlos anmelden (haro.help)
2. Relevante Kategorien wählen
3. Auf Anfragen antworten
4. Journalisten-Beziehung aufbauen
```

### Qwoted

```
- Alternative zu HARO
- Fokus auf Expertise
- Direkte Journalisten-Anfragen
```

### ResponseSource (EU)

```
- Europäischer Fokus
- Anfragen von UK/EU-Journalisten
- Kostenpflichtig, aber qualitativ
```

---

## Daten-Extraktion

### Was sammeln?

```json
{
  "name": "Max Mustermann",
  "email": "m.mustermann@t3n.de",
  "publication": "t3n",
  "position": "Senior Editor",
  "beats": ["SaaS", "Marketing Tech", "Startups"],
  "social": {
    "twitter": "@maxmustermann",
    "linkedin": "linkedin.com/in/maxmustermann"
  },
  "recent_articles": [
    {
      "title": "...",
      "url": "...",
      "date": "2024-01-15",
      "topic": "Marketing Tech"
    }
  ],
  "contact_preferences": {
    "prefers_email": true,
    "active_on_twitter": true,
    "best_time": "mornings"
  },
  "notes": "Hat Interesse an AI gezeigt, antwortet schnell"
}
```

### Datenquellen-Matrix

| Datenfeld | Google | LinkedIn | Twitter | Website |
|-----------|--------|----------|---------|---------|
| Name | ✅ | ✅ | ✅ | ✅ |
| Email | ⚠️ | ❌ | ❌ | ✅ |
| Publikation | ✅ | ✅ | ✅ | ✅ |
| Beat | ⚠️ | ✅ | ✅ | ✅ |
| Recent Articles | ✅ | ❌ | ⚠️ | ✅ |
| Social Links | ⚠️ | ✅ | ✅ | ✅ |
| Contact Pref | ❌ | ❌ | ⚠️ | ⚠️ |

✅ = Zuverlässig | ⚠️ = Manchmal | ❌ = Nicht verfügbar

---

## Automatisierung

### Web Scraping (ethisch)

```python
# Beispiel: Autorenprofil scrapen (nur öffentliche Daten)
import requests
from bs4 import BeautifulSoup

def get_author_info(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    return {
        'name': soup.find('h1', class_='author-name').text,
        'bio': soup.find('div', class_='author-bio').text,
        'articles': [
            a['href'] for a in soup.find_all('a', class_='article-link')
        ]
    }
```

### API-Integration

```typescript
// Hunter.io Email-Finder
const findEmail = async (name: string, domain: string) => {
  const response = await fetch(
    `https://api.hunter.io/v2/email-finder?` +
    `domain=${domain}&full_name=${name}&api_key=${HUNTER_API_KEY}`
  );
  return response.json();
};
```

---

## Qualitätssicherung

### Verifizierung

```
Vor dem Pitch prüfen:
1. Email-Adresse gültig? (Bounce-Check)
2. Person noch bei Publikation? (LinkedIn Check)
3. Beat noch aktuell? (Letzte Artikel)
4. Nicht im Urlaub? (Social Media Check)
```

### Red Flags

```
❌ Keine Artikel in letzten 90 Tagen
❌ Position geändert (LinkedIn)
❌ "Freelance" ohne aktive Publikation
❌ Auto-Reply aktiv
❌ Hat öffentlich um weniger Pitches gebeten
```

### Best Practices

```
✅ Daten regelmäßig aktualisieren (alle 30 Tage)
✅ Bounce-Rate tracken
✅ Opt-Outs respektieren
✅ DSGVO beachten (legitimes Interesse für B2B)
✅ Manuelle Prüfung vor wichtigen Pitches
```
