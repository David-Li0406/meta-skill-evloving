---
name: video-creator
description: Creates video scripts, storyboards, and production briefs for marketing videos. Handles format-specific requirements (Reels, TikTok, YouTube Shorts, explainer videos). Includes hook writing, scene breakdowns, and call-to-action placement. Use when creating video content from articles or standalone.
---

# Video Creator

Erstellt Video-Scripts, Storyboards und Production Briefs für Marketing-Videos.

## Quick Start

```
Input: Content/Topic + Platform + Video-Typ + Ziel
Output: Script + Storyboard + Shot List + Production Notes
```

## Video-Formate

| Format | Länge | Aspect Ratio | Plattform |
|--------|-------|--------------|-----------|
| Reel/TikTok | 15-60s | 9:16 | Instagram, TikTok |
| YouTube Short | 15-60s | 9:16 | YouTube |
| Explainer | 60-180s | 16:9 | YouTube, Website |
| Tutorial | 3-10 min | 16:9 | YouTube |
| Talking Head | 1-5 min | 16:9 | LinkedIn, YouTube |
| Product Demo | 30-90s | 16:9 / 1:1 | Social, Website |

Details: [VIDEO_FORMATS.md](VIDEO_FORMATS.md)

## Output Format

```json
{
  "video": {
    "title": "5 Content Marketing Fehler",
    "format": "reel",
    "duration": "45s",
    "aspect_ratio": "9:16",
    "platform": "instagram"
  },
  "script": {
    "hook": "Die meisten machen DIESEN Fehler bei Content Marketing...",
    "scenes": [
      {
        "scene_number": 1,
        "duration": "5s",
        "visual": "Host vor Kamera, überraschter Blick",
        "audio": "Die meisten machen DIESEN Fehler...",
        "text_overlay": "😱 FEHLER #1",
        "b_roll": null
      },
      {
        "scene_number": 2,
        "duration": "8s",
        "visual": "B-Roll: Laptop mit Analytics",
        "audio": "Sie posten Content ohne Strategie...",
        "text_overlay": "Ohne Plan posten",
        "b_roll": "laptop_analytics.mp4"
      }
    ],
    "cta": {
      "text": "Folge für mehr Marketing-Tipps",
      "visual": "Follow-Button Animation",
      "timing": "letzte 3 Sekunden"
    }
  },
  "production": {
    "equipment": ["Smartphone/Kamera", "Ring Light", "Mikrofon"],
    "location": "Büro / Homeoffice",
    "props": ["Laptop", "Whiteboard"],
    "b_roll_needed": ["laptop_analytics", "social_media_scrolling"],
    "music": "Upbeat, trending audio",
    "editing_notes": "Schnelle Schnitte, Zoom-Ins bei Key Points"
  }
}
```

## Script-Struktur

### Hook (erste 3 Sekunden)

```
Ziel: Attention grabben, Scroll stoppen

Techniken:
1. Shocking Statement: "90% scheitern an..."
2. Frage: "Machst du auch diesen Fehler?"
3. Provokation: "Das wird dein Chef nicht mögen..."
4. Teaser: "Der Trick, den niemand kennt..."
5. Pain Point: "Warum dein Content nicht performt..."
```

### Body (Hauptinhalt)

```
Short-Form (15-60s):
- 1 Hauptidee
- 3-5 Punkte
- Schnelle Übergänge

Long-Form (1-10min):
- Intro + Problem
- 3-7 Kapitel
- Beispiele & Beweise
- Zusammenfassung
```

### CTA (letzten Sekunden)

```
Arten:
- Follow/Subscribe
- Kommentar ("Welcher Fehler war's bei dir?")
- Share ("Teile mit einem Marketer")
- Link ("Link in Bio")
- Next Video ("Teil 2 kommt...")
```

Details: [SCRIPT_TEMPLATES.md](SCRIPT_TEMPLATES.md)

## Plattform-Spezifikationen

### TikTok / Instagram Reels

```
Länge: 15-60s (Sweet Spot: 30-45s)
Aspect Ratio: 9:16 (1080x1920)
Safe Zone: 150px top, 250px bottom (für UI)

Stil:
- Native, authentisch
- Trending Audio
- Text Overlays
- Schnelle Schnitte
- Eye Contact

Hooks die funktionieren:
- "Hier ist der Beweis dass..."
- "3 Dinge die ich gelernt habe..."
- "Das hat alles verändert..."
- "Unpopuläre Meinung:..."
```

### YouTube Shorts

```
Länge: 15-60s
Aspect Ratio: 9:16 (1080x1920)
Titel: Max 100 Zeichen

Besonderheiten:
- Kann Musik verwenden (YouTube Library)
- Hashtag #Shorts im Titel
- Looping Content funktioniert gut
- Mehr "informational" als TikTok
```

### YouTube Long-Form

```
Länge: 8-15 min (optimal für Algorithm)
Aspect Ratio: 16:9 (1920x1080)

Struktur:
0:00 - Hook (30s)
0:30 - Intro/Problem (1-2min)
2:00 - Hauptinhalt (Kapitel)
X:00 - Zusammenfassung (1min)
X:00 - CTA (30s)

Retention-Tipps:
- Pattern Interrupts alle 30-60s
- Cliffhanger vor Ad Breaks
- End Screens mit Next Video
```

### LinkedIn

```
Länge: 30s - 3min
Aspect Ratio: 16:9, 1:1, oder 9:16
Untertitel: PFLICHT (80% schauen ohne Ton)

Stil:
- Professionell aber personable
- Thought Leadership
- Keine Trendingd Audios
- Talking Head funktioniert gut
```

## Storyboard-Template

```
┌─────────────────────────────────────────────┐
│ SZENE 1                        Dauer: 3s    │
├─────────────────────────────────────────────┤
│ ┌─────────────┐                             │
│ │             │  VISUAL:                    │
│ │  [Sketch]   │  Host in Frame, Center      │
│ │             │  Background: Büro           │
│ │             │                             │
│ └─────────────┘                             │
│                                             │
│ AUDIO: "Die meisten machen DIESEN Fehler"  │
│                                             │
│ TEXT: 😱 FEHLER #1                          │
│ Position: Upper Third                       │
│                                             │
│ MOVEMENT: Leichter Zoom In                  │
│                                             │
│ NOTES: Überraschter Gesichtsausdruck       │
└─────────────────────────────────────────────┘
```

Details: [STORYBOARD_TEMPLATE.md](templates/storyboard-template.md)

## B-Roll Planung

### Kategorien

```
Interview/Talking Head:
- Laptop-Arbeit
- Whiteboard-Skizzen
- Analytics-Dashboard
- Team-Meeting

Product:
- Produkt in Aktion
- Features-Close-ups
- Before/After
- Unboxing

Lifestyle:
- Arbeitsumgebung
- Kaffee/Büro
- Erfolgsmomente
```

### Shot List Template

```markdown
| Shot # | Beschreibung | Dauer | Equipment | Notes |
|--------|--------------|-------|-----------|-------|
| B01 | Laptop mit Dashboard | 5s | Slider | Langsame Bewegung |
| B02 | Hände tippen | 3s | Macro | Close-up |
| B03 | Reaktion auf Screen | 4s | Handheld | Über Schulter |
```

## Audio & Musik

### Voice-Over Tipps

```
Tempo: 130-150 Wörter/Minute (Short-Form)
        120-140 Wörter/Minute (Long-Form)

Stil:
- Conversational, nicht scripted
- Energy passend zum Content
- Betonungen bei Key Points
- Pausen für Emphasis
```

### Musik-Auswahl

```
Short-Form:
- Trending Audio (TikTok/IG)
- Upbeat, energetisch
- Passt zum Hook-Moment

Long-Form:
- Royalty-Free (Epidemic Sound, Artlist)
- Background Level (-20dB)
- Genre passend zum Thema
```

## Text Overlays

### Formatierung

```
Font: Bold, Sans-Serif
Größe: Lesbar auf Mobile!
Position: Safe Zones beachten
Animation: Simple (Pop, Slide)

Arten:
- Headline Text (groß)
- Keyword Highlight (Farbe)
- Captions (durchlaufend)
- Bullet Points
```

### Captions/Untertitel

```
Stil: Kurze Zeilen (max 2 Wörter pro Highlight)
Animation: Word-by-Word oder Phrase
Farbe: Kontrast zum Video
Position: Unteres Drittel (aber über UI)
```

## Checkliste

### Pre-Production
- [ ] Hook definiert?
- [ ] Script geschrieben?
- [ ] Storyboard erstellt?
- [ ] B-Roll Liste?
- [ ] Equipment bereit?
- [ ] Location geplant?

### Production
- [ ] Gute Beleuchtung?
- [ ] Sauberer Ton?
- [ ] Mehrere Takes?
- [ ] B-Roll aufgenommen?

### Post-Production
- [ ] Hook in ersten 3 Sekunden?
- [ ] Text Overlays lesbar?
- [ ] Untertitel vorhanden?
- [ ] Musik passend?
- [ ] CTA am Ende?
- [ ] Thumbnail erstellt?
