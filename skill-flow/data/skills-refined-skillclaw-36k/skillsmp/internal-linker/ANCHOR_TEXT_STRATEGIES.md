# Anchor Text Strategies

## Warum Anchor Text wichtig ist

- **SEO Signal:** Google nutzt Anchor Text als Relevanz-Indikator
- **User Experience:** Sagt dem Leser, was ihn erwartet
- **Click-Through:** Guter Anchor = mehr Klicks

---

## Anchor Text Typen

### 1. Exact Match
```
Zielseite: "Content Marketing Strategie"
Anchor: "Content Marketing Strategie"
```
**Nutzung:** Sparsam (max 20% aller Anchors)
**Risiko:** Überoptimierung

### 2. Partial Match
```
Zielseite: "Content Marketing Strategie"
Anchor: "Strategie für Content"
Anchor: "Marketing-Strategie entwickeln"
```
**Nutzung:** Häufig (40-50%)
**Risiko:** Gering

### 3. Branded
```
Zielseite: Über uns
Anchor: "ContentAI Team"
Anchor: "unser Unternehmen"
```
**Nutzung:** Für interne Seiten
**Risiko:** Keins

### 4. Generic
```
Anchor: "hier klicken"
Anchor: "mehr erfahren"
Anchor: "dieser Artikel"
```
**Nutzung:** Minimieren (<10%)
**Risiko:** Verschwendetes Potenzial

### 5. Naked URL
```
Anchor: "www.example.com/artikel"
```
**Nutzung:** Fast nie für interne Links
**Risiko:** Schlechte UX

### 6. Long-Tail / Natural
```
Zielseite: "Content Marketing Strategie"
Anchor: "wie du eine effektive Content Strategie entwickelst"
Anchor: "unser Guide zur Content-Planung"
```
**Nutzung:** Häufig (30-40%)
**Risiko:** Keins

---

## Optimale Anchor-Verteilung

```
┌─────────────────────────────────────┐
│ Partial Match          45%         │
│ Long-Tail/Natural      30%         │
│ Exact Match            15%         │
│ Branded                 5%         │
│ Generic                 5%         │
└─────────────────────────────────────┘
```

---

## Best Practices

### DO ✅

**1. Natürlich integrieren**
```
❌ "Lies unseren Content Marketing Strategie Artikel."
✅ "Eine durchdachte Content Marketing Strategie ist entscheidend."
```

**2. Kontext-relevant**
```
Paragraph über SEO:
✅ "...wie wir in unserem SEO-Guide erklären..."
❌ "...hier ist unser Produkt..."
```

**3. Variieren**
```
Link zu gleichem Artikel, verschiedene Anchors:
- "Content Strategie"
- "strategische Content-Planung"
- "wie du Content planst"
```

**4. Beschreibend**
```
✅ "die wichtigsten SEO-Faktoren"
✅ "unsere Analyse der Ranking-Faktoren"
❌ "hier" oder "mehr"
```

**5. Angemessene Länge**
```
Ideal: 2-5 Wörter
OK: 1 Wort (wenn beschreibend)
Zu lang: Ganze Sätze
```

### DON'T ❌

**1. Keyword Stuffing**
```
❌ "Content Marketing Content Marketing Strategie Content"
```

**2. Irreführend**
```
❌ Anchor "Kostenloser Download" → Seite ohne Download
```

**3. Überoptimierung**
```
❌ Immer exakt "Content Marketing Strategie" als Anchor
```

**4. Generisch**
```
❌ "Klicke hier für mehr Informationen."
✅ "Erfahre mehr über Content Marketing Strategien."
```

**5. Zu viele Links in einem Absatz**
```
❌ "In unserem Blog findest du Artikel über SEO,
    Content Marketing, Social Media und Email Marketing."
    (4 Links in einem Satz)

✅ Ein Link pro Absatz als Faustregel
```

---

## Anchor Text Generator

### Input
```
target_url: "/content-marketing-strategie"
target_title: "Content Marketing Strategie: Der ultimative Guide"
target_keywords: ["content marketing", "strategie", "content planung"]
context_paragraph: "Eine gute Marketingstrategie beginnt mit der Planung..."
```

### Output
```json
{
  "anchor_suggestions": [
    {
      "text": "Content Marketing Strategie",
      "type": "partial_match",
      "natural_context": "...eine durchdachte Content Marketing Strategie ist..."
    },
    {
      "text": "strategische Content-Planung",
      "type": "long_tail",
      "natural_context": "...mehr über strategische Content-Planung erfahren..."
    },
    {
      "text": "wie du Content planst",
      "type": "natural",
      "natural_context": "...in unserem Guide zeigen wir, wie du Content planst..."
    },
    {
      "text": "Marketing-Strategie entwickeln",
      "type": "partial_match",
      "natural_context": "...wenn du eine Marketing-Strategie entwickeln möchtest..."
    }
  ]
}
```

---

## Kontextuelle Einbettung

### Natürliche Link-Phrasen

**Für Erklärungen:**
```
"...wie wir in unserem [Artikel über X] erklären..."
"...mehr dazu findest du in unserem [Guide zu Y]..."
"...die Grundlagen haben wir in [Artikel Z] behandelt..."
```

**Für Vertiefung:**
```
"...wenn du tiefer einsteigen möchtest: [Thema X]..."
"...für fortgeschrittene Strategien siehe [Artikel Y]..."
"...ausführlicher behandeln wir das in [Guide Z]..."
```

**Für Verwandte Themen:**
```
"...ähnlich wie bei [verwandtes Thema]..."
"...das gilt auch für [anderer Bereich]..."
"...in Kombination mit [ergänzendes Thema]..."
```

**Für Beispiele:**
```
"...ein Beispiel dafür ist [Case Study]..."
"...wie [Firma X] zeigt..."
"...praktische Anwendung in [Artikel]..."
```

---

## Anchor Text Checkliste

- [ ] Beschreibt der Anchor, wohin der Link führt?
- [ ] Ist der Anchor 2-5 Wörter lang?
- [ ] Passt der Anchor natürlich in den Satz?
- [ ] Wird nicht der gleiche Anchor überall verwendet?
- [ ] Ist der Anchor unique auf der Seite (gleicher Anchor → gleiche URL)?
- [ ] Kein "hier klicken" oder "mehr erfahren"?
- [ ] Nicht überoptimiert (zu viele Exact-Match)?
