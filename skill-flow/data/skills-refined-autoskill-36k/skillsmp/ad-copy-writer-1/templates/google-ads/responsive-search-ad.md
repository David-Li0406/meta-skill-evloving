# Google Responsive Search Ad Template

## Specs
- **Headlines:** Max 15 (min 3), je 30 Zeichen
- **Descriptions:** Max 4 (min 2), je 90 Zeichen
- **Display Paths:** 2 x 15 Zeichen
- **Final URL:** Landing Page URL

---

## Headline-Kategorien

Liefere Headlines aus jeder Kategorie für maximale Kombinationsmöglichkeiten:

### 1. Keyword-Headlines (3-4 Stück)
Das Haupt-Keyword muss enthalten sein.
```
[Keyword] für [Zielgruppe]
[Keyword] - Jetzt entdecken
Professionelle [Keyword]
[Keyword] vom Experten
```

### 2. Benefit-Headlines (3-4 Stück)
Der Hauptnutzen für den Kunden.
```
[Zeitersparnis] sparen
[Ergebnis] erreichen
Mehr [gewünschtes Outcome]
[Problem] endlich lösen
```

### 3. CTA-Headlines (2-3 Stück)
Klare Handlungsaufforderung.
```
Jetzt kostenlos testen
Demo vereinbaren
Angebot anfordern
Heute starten
```

### 4. Social Proof (2-3 Stück)
Vertrauen aufbauen.
```
[Zahl]+ zufriedene Kunden
Trusted by [Branche]
[Award/Zertifizierung]
⭐ [Bewertung]/5 Sterne
```

### 5. USP/Differentiator (2-3 Stück)
Was macht uns einzigartig?
```
Made in Germany
[Unique Feature] inklusive
Ohne [unerwünschtes]
[Garantie] garantiert
```

---

## Description-Kategorien

### Description 1: Vollständiger Value Prop
```
[Hauptbenefit in einem Satz]. [Keyword] für [Zielgruppe]. [CTA].
```
Beispiel: "Erstelle professionelle Reports in Minuten statt Stunden. Marketing-Automation für wachsende Teams. Jetzt kostenlos testen."

### Description 2: Problem → Lösung
```
[Problem]? Mit [Produkt] [Lösung]. [Proof-Element]. [CTA].
```
Beispiel: "Zeitaufwändige manuelle Prozesse? Automatisiere mit ContentAI. Über 500 Teams sparen 15h/Woche. Demo buchen."

### Description 3: Features + Benefits
```
✓ [Feature 1] ✓ [Feature 2] ✓ [Feature 3]. [Hauptbenefit]. [Garantie/Angebot].
```
Beispiel: "✓ KI-Texte ✓ Automatische Planung ✓ Analytics. Alles für besseres Content Marketing. 14 Tage kostenlos."

### Description 4: Social Proof + Dringlichkeit
```
[Social Proof Zahl] [Kunden/Nutzer] vertrauen uns. [Ergebnis das sie erzielen]. [Zeitlich begrenztes Angebot wenn vorhanden].
```
Beispiel: "2.000+ Marketing-Teams steigern ihre Leads um durchschnittlich 47%. Starte heute mit dem kostenlosen Plan."

---

## Output-Format

```json
{
  "campaign_type": "google_responsive_search",
  "ad_group": "[Name]",
  "headlines": [
    {"text": "[Max 30 Zeichen]", "category": "keyword"},
    {"text": "[Max 30 Zeichen]", "category": "benefit"},
    {"text": "[Max 30 Zeichen]", "category": "cta"},
    // ... (min 8, max 15)
  ],
  "descriptions": [
    {"text": "[Max 90 Zeichen]", "category": "value_prop"},
    {"text": "[Max 90 Zeichen]", "category": "problem_solution"},
    {"text": "[Max 90 Zeichen]", "category": "features"},
    {"text": "[Max 90 Zeichen]", "category": "social_proof"}
  ],
  "paths": {
    "path1": "[Max 15 Zeichen]",
    "path2": "[Max 15 Zeichen]"
  },
  "final_url": "https://..."
}
```

---

## Beispiel-Output

**Input:** Content-Marketing-Tool für B2B

```json
{
  "campaign_type": "google_responsive_search",
  "ad_group": "Content Marketing Tool - Broad",
  "headlines": [
    {"text": "Content Marketing Tool", "category": "keyword"},
    {"text": "B2B Content Marketing", "category": "keyword"},
    {"text": "Content-Erstellung leicht", "category": "keyword"},
    {"text": "10x schneller Content", "category": "benefit"},
    {"text": "Mehr Leads generieren", "category": "benefit"},
    {"text": "Zeit sparen beim Content", "category": "benefit"},
    {"text": "Jetzt kostenlos testen", "category": "cta"},
    {"text": "Demo vereinbaren", "category": "cta"},
    {"text": "Gratis starten", "category": "cta"},
    {"text": "500+ Teams vertrauen uns", "category": "social_proof"},
    {"text": "4.8/5 Sterne Bewertung", "category": "social_proof"},
    {"text": "KI-gestützte Texte", "category": "usp"},
    {"text": "Made in Germany", "category": "usp"},
    {"text": "DSGVO-konform", "category": "usp"},
    {"text": "Ohne Vorkenntnisse", "category": "usp"}
  ],
  "descriptions": [
    {
      "text": "Erstelle B2B-Content in Minuten statt Stunden. KI-Tool für Marketing-Teams. 14 Tage kostenlos testen.",
      "category": "value_prop"
    },
    {
      "text": "Content-Erstellung zu aufwändig? Automatisiere mit KI. Über 500 Teams sparen 15 Stunden pro Woche.",
      "category": "problem_solution"
    },
    {
      "text": "✓ Blog-Artikel ✓ Social Posts ✓ Ads-Texte. Alles aus einer Plattform. Jetzt gratis starten.",
      "category": "features"
    },
    {
      "text": "2.000+ Marketing-Profis nutzen unser Tool täglich. Durchschnittlich 47% mehr Content-Output.",
      "category": "social_proof"
    }
  ],
  "paths": {
    "path1": "content-tool",
    "path2": "kostenlos"
  },
  "final_url": "https://example.com/content-marketing-tool"
}
```

---

## Checkliste

- [ ] Min. 8 Headlines geliefert?
- [ ] Alle Kategorien abgedeckt?
- [ ] Keyword in mind. 3 Headlines?
- [ ] Alle 4 Descriptions geliefert?
- [ ] Jede Headline ≤ 30 Zeichen?
- [ ] Jede Description ≤ 90 Zeichen?
- [ ] Headlines funktionieren einzeln UND kombiniert?
- [ ] Keine Duplikate oder sehr ähnliche Texte?
- [ ] Paths relevant und keyword-haltig?
