# Internal Linking Strategies

## Strategie-Übersicht

| Strategie | Ziel | Anwendung |
|-----------|------|-----------|
| Topic Cluster | Themen-Autorität | Pillar Pages |
| Silo Structure | Kategorie-Stärke | E-Commerce, große Blogs |
| Hub & Spoke | Zentrale Seiten stärken | Landing Pages |
| Contextual | User Experience | Alle Artikel |
| Footer/Sidebar | Navigation | Site-wide |

---

## 1. Topic Cluster Strategie

### Konzept
```
                    ┌─────────────┐
                    │   PILLAR    │
                    │   (Hub)     │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌─────▼─────┐      ┌────▼────┐
   │ Cluster │       │  Cluster  │      │ Cluster │
   │    A    │       │     B     │      │    C    │
   └────┬────┘       └─────┬─────┘      └────┬────┘
        │                  │                  │
   ┌────▼────┐       ┌─────▼─────┐      ┌────▼────┐
   │Sub-Topic│       │ Sub-Topic │      │Sub-Topic│
   └─────────┘       └───────────┘      └─────────┘
```

### Linking-Regeln
1. **Pillar → Cluster:** Pillar verlinkt zu allen Cluster-Artikeln
2. **Cluster → Pillar:** Jeder Cluster verlinkt zurück zum Pillar
3. **Cluster → Cluster:** Verwandte Cluster verlinken zueinander
4. **Sub-Topic → Cluster:** Nach oben verlinken

### Beispiel: "Content Marketing" Pillar
```
Pillar: /content-marketing-guide
├── /content-strategie-entwickeln
│   ├── /redaktionsplan-erstellen
│   └── /content-audit-durchfuehren
├── /content-erstellung
│   ├── /blog-artikel-schreiben
│   └── /video-content-erstellen
└── /content-distribution
    ├── /social-media-content
    └── /email-marketing-content
```

---

## 2. Silo Structure

### Konzept
Strikte thematische Trennung in "Silos".

```
┌─────────────────────────────────────────────┐
│                 HOMEPAGE                     │
└───────┬─────────────┬───────────────┬───────┘
        │             │               │
   ┌────▼────┐   ┌────▼────┐    ┌────▼────┐
   │ SILO A  │   │ SILO B  │    │ SILO C  │
   │(Kategorie)│  │(Kategorie)│   │(Kategorie)│
   └────┬────┘   └────┬────┘    └────┬────┘
        │             │               │
   ┌────▼────┐   ┌────▼────┐    ┌────▼────┐
   │Artikel 1│   │Artikel 1│    │Artikel 1│
   │Artikel 2│   │Artikel 2│    │Artikel 2│
   │Artikel 3│   │Artikel 3│    │Artikel 3│
   └─────────┘   └─────────┘    └─────────┘
```

### Linking-Regeln
1. **Innerhalb Silo:** Frei verlinken
2. **Zwischen Silos:** Nur über Kategorieseite oder Homepage
3. **Nach oben:** Immer zur Kategorieseite verlinken

### Wann nutzen
- E-Commerce (Produktkategorien)
- Große Blogs (100+ Artikel)
- Klare thematische Trennung gewünscht

---

## 3. Hub & Spoke

### Konzept
Eine zentrale Seite (Hub) sammelt Links von vielen Spokes.

```
         ┌─────────┐
         │ Spoke 1 │────┐
         └─────────┘    │
                        │
    ┌─────────┐    ┌────▼────┐    ┌─────────┐
    │ Spoke 2 │───►│   HUB   │◄───│ Spoke 4 │
    └─────────┘    └────▲────┘    └─────────┘
                        │
         ┌─────────┐    │
         │ Spoke 3 │────┘
         └─────────┘
```

### Anwendung
- **Money Pages** stärken (Produkt, Pricing, Demo)
- **Conversion Pages** boosten
- **Wichtige Landing Pages** pushen

### Beispiel
```
Hub: /marketing-automation-tool (Produkt-Seite)

Spokes (alle verlinken zum Hub):
- /was-ist-marketing-automation (Informational)
- /marketing-automation-vorteile (Consideration)
- /marketing-automation-vergleich (Comparison)
- /marketing-automation-einrichten (How-To)
- /case-study-firma-x (Social Proof)
```

---

## 4. Contextual Linking

### Konzept
Links dort setzen, wo sie dem Leser helfen.

### Best Practices

**Natürlicher Lesefluss:**
```
"Bevor du mit Content Marketing startest, solltest du
deine Zielgruppe definieren. In unserem Guide zur
Zielgruppenanalyse zeigen wir dir, wie das geht."
```

**Vertiefung anbieten:**
```
"SEO ist ein wichtiger Faktor für Content-Erfolg.
Die Grundlagen haben wir in unserem SEO-Einsteiger-Guide
zusammengefasst."
```

**Verwandte Themen:**
```
"Ähnlich wie bei der Content-Erstellung gilt auch
für Social Media: Qualität vor Quantität."
```

---

## 5. Footer/Sidebar Links

### Verwendung
- Wichtige Seiten site-wide verlinken
- Kategorien/Themen zugänglich machen
- NICHT für SEO-Manipulation

### Beispiel Footer
```
Ressourcen        Produkt          Unternehmen
- Blog            - Features       - Über uns
- Guides          - Pricing        - Karriere
- Webinare        - Integrationen  - Kontakt
- Case Studies    - Sicherheit     - Impressum
```

---

## Link-Verteilung

### Ideale Verteilung pro Artikel

| Link-Typ | Anzahl | Ziel |
|----------|--------|------|
| Outbound (zu anderen Artikeln) | 3-5 | Thematisch verwandt |
| Inbound (von anderen Artikeln) | 3+ | Orphan Prevention |
| Externe Links | 1-3 | Autoritäts-Quellen |

### Link-Equity-Fluss

```
Seiten mit viel Autorität (viele Backlinks):
→ Sollten zu wichtigen Seiten verlinken

Neue/schwache Seiten:
→ Sollten Links von starken Seiten erhalten
```

---

## Orphan Page Prevention

### Was ist eine Orphan Page?
Eine Seite ohne interne Links zu ihr.

### Identifikation
```
SELECT * FROM articles
WHERE id NOT IN (
  SELECT target_article_id FROM internal_links
)
```

### Lösung
1. Thematisch passende Artikel finden
2. Links zu Orphan Page einbauen
3. Mindestens 3 interne Links pro Seite

---

## Link-Audit Checkliste

### Monatlich prüfen:
- [ ] Keine Orphan Pages?
- [ ] Keine Broken Links?
- [ ] Wichtige Seiten gut verlinkt?
- [ ] Neue Artikel verlinkt?
- [ ] Anchor-Text-Vielfalt gegeben?
- [ ] Keine übermäßige Verlinkung?

### Jährlich:
- [ ] Topic Cluster noch aktuell?
- [ ] Alte Artikel updaten und neu verlinken?
- [ ] Redirect-Chains prüfen?
- [ ] Link-Equity-Verteilung analysieren?
