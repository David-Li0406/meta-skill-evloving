# Semantic Analysis für Internal Linking

## Übersicht

Semantische Analyse identifiziert thematisch verwandte Inhalte für sinnvolle Verlinkungen.

---

## Analyse-Ebenen

### 1. Keyword-Ebene

**Exact Match**
```
Artikel A: "Content Marketing Strategie"
Artikel B: "Content Marketing Strategie für B2B"
→ Hohe Relevanz (Exact Keyword Match)
```

**Partial Match**
```
Artikel A: "Content Marketing Strategie"
Artikel B: "Marketing Strategie entwickeln"
→ Mittlere Relevanz (Partial Match)
```

### 2. Topic-Ebene

**Topic Cluster Identifikation**
```
Pillar: "Content Marketing" (Hauptthema)
├── Cluster: "Blog-Strategie"
├── Cluster: "Social Media Content"
├── Cluster: "Video Marketing"
├── Cluster: "Content Distribution"
└── Cluster: "Content Analytics"
```

**Linking-Regel:**
- Pillar → alle Cluster (bidirektional)
- Cluster → Pillar
- Cluster → verwandte Cluster

### 3. Entity-Ebene

**Entity-Extraktion:**
```
Artikel enthält:
- Personen: "Neil Patel", "Gary Vaynerchuk"
- Tools: "HubSpot", "Ahrefs", "Semrush"
- Konzepte: "SEO", "Conversion Rate", "Funnel"
- Marken: "Google", "LinkedIn"
```

**Entity-Matching:**
- Artikel über HubSpot → Link zu "Marketing Automation Tools"
- Artikel erwähnt SEO → Link zu "SEO Grundlagen"

### 4. Intent-Ebene

**Search Intent Typen:**
```
Informational: "Was ist Content Marketing?"
Navigational: "HubSpot Login"
Transactional: "Content Marketing Tool kaufen"
Commercial: "Beste Content Marketing Tools"
```

**Linking nach Intent:**
- Informational → Informational (Wissen vertiefen)
- Informational → Commercial (Lösungen zeigen)
- Commercial → Transactional (Conversion-Pfad)

---

## Relevanz-Scoring

### Scoring-Formel

```
Relevanz-Score =
  (Keyword-Match × 0.3) +
  (Topic-Match × 0.3) +
  (Entity-Match × 0.2) +
  (Intent-Match × 0.1) +
  (Link-Need × 0.1)
```

### Score-Interpretation

| Score | Bedeutung | Aktion |
|-------|-----------|--------|
| 0.8-1.0 | Sehr relevant | Definitiv verlinken |
| 0.6-0.8 | Relevant | Verlinken empfohlen |
| 0.4-0.6 | Möglicherweise relevant | Manuell prüfen |
| <0.4 | Wenig relevant | Nicht verlinken |

---

## Praktische Analyse-Methoden

### Methode 1: TF-IDF Ähnlichkeit

Berechnet Textähnlichkeit basierend auf Wort-Häufigkeit.

```python
# Pseudocode
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(all_articles)
similarity = cosine_similarity(new_article_vector, tfidf_matrix)
```

### Methode 2: Keyword-Overlap

Vergleicht extrahierte Keywords.

```python
# Pseudocode
article_a_keywords = extract_keywords(article_a)
article_b_keywords = extract_keywords(article_b)

overlap = len(article_a_keywords & article_b_keywords)
similarity = overlap / len(article_a_keywords | article_b_keywords)
```

### Methode 3: Topic Modeling

Identifiziert latente Themen.

```python
# Pseudocode (LDA)
from sklearn.decomposition import LatentDirichletAllocation

lda = LatentDirichletAllocation(n_components=10)
topic_distribution = lda.fit_transform(tfidf_matrix)

# Artikel mit ähnlicher Topic-Verteilung sind verwandt
```

### Methode 4: Embedding-Similarity

Nutzt semantische Embeddings (z.B. OpenAI, Sentence-Transformers).

```python
# Pseudocode
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
embeddings = model.encode(all_articles)

similarity = cosine_similarity(new_article_embedding, embeddings)
```

---

## Link-Kontext-Analyse

### Natürliche Link-Stellen finden

**Gute Kontexte:**
```
"...mehr über [Thema] erfahren..."
"...wie in unserem Artikel über [Thema]..."
"...ein wichtiger Aspekt ist [Konzept]..."
"...ähnlich wie bei [verwandtes Thema]..."
"...die Grundlagen von [Thema]..."
```

**Schlechte Kontexte:**
```
❌ Mitten in einer Liste
❌ In einer Überschrift
❌ In einem Zitat
❌ Im ersten Satz des Artikels
```

### Paragraph-Analyse

```
Für jeden Absatz analysieren:
1. Enthält verwandte Keywords?
2. Ist der Kontext erklärend (gut für Links)?
3. Ist Platz für einen natürlichen Link?
4. Würde ein Link dem Leser helfen?
```

---

## Topic Cluster Mapping

### Beispiel-Cluster: "Content Marketing"

```yaml
pillar:
  title: "Der ultimative Guide zu Content Marketing"
  url: "/content-marketing-guide"

clusters:
  - topic: "Content Strategie"
    keywords: ["content strategie", "redaktionsplan", "content planung"]
    articles:
      - "/content-strategie-entwickeln"
      - "/redaktionsplan-erstellen"

  - topic: "Content Erstellung"
    keywords: ["content erstellen", "blog schreiben", "texten"]
    articles:
      - "/blog-artikel-schreiben"
      - "/content-formate"

  - topic: "Content Distribution"
    keywords: ["content verbreiten", "seeding", "promotion"]
    articles:
      - "/content-distribution-strategie"
      - "/social-media-content"
```

### Linking-Regeln pro Cluster

```
1. Pillar verlinkt zu allen Cluster-Artikeln
2. Jeder Cluster-Artikel verlinkt zum Pillar
3. Cluster-Artikel verlinken untereinander (wenn sinnvoll)
4. Max. 2-3 Links zwischen verschiedenen Pillars
```

---

## Output: Analyse-Report

```json
{
  "analyzed_article": {
    "id": "uuid",
    "title": "Content Marketing für B2B",
    "detected_topics": ["content marketing", "b2b", "lead generation"],
    "detected_entities": ["HubSpot", "LinkedIn"],
    "detected_intent": "informational"
  },
  "related_articles": [
    {
      "id": "uuid",
      "title": "B2B Lead Generation Strategien",
      "relevance_score": 0.87,
      "match_reasons": [
        "Topic Match: B2B (0.9)",
        "Entity Match: LinkedIn (0.8)",
        "Intent Match: informational (1.0)"
      ],
      "suggested_link_contexts": [
        "...wie wir in unserem Artikel über [Lead Generation] zeigen...",
        "...ähnlich wie bei [B2B Marketing]..."
      ]
    }
  ]
}
```
