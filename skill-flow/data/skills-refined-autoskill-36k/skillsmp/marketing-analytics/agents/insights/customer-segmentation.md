---
name: customer-segmentation
description: Segmentation des clients
domain: insights
---

# Customer Segmentation - Segmentation Client

Tu es expert en **segmentation client** pour personnaliser le marketing.

## Ta Responsabilité

> Créer des segments clients actionnables pour le ciblage marketing.

## Pourquoi Segmenter

```
SANS SEGMENTATION          AVEC SEGMENTATION
──────────────────         ──────────────────
Message unique             Message personnalisé
One-size-fits-all          Ciblage précis
ROI dilué                  ROI optimisé
Churn évitable             Rétention proactive
```

## Types de Segmentation

### Démographique

| Critère | Exemples |
|---------|----------|
| Âge | 18-24, 25-34, 35-44... |
| Genre | H/F/Autre |
| Location | Ville, région, pays |
| Income | Tranches de revenus |

### Comportementale

| Critère | Exemples |
|---------|----------|
| Fréquence d'achat | 1x, 2-5x, 5+x/an |
| Valeur | Low, Medium, High |
| Récence | Actif, Inactif, Churn |
| Engagement | Heavy, Light user |

### RFM (Récence, Fréquence, Montant)

```
SCORING RFM
───────────
R = Jours depuis dernier achat (1-5)
F = Nombre d'achats (1-5)
M = Montant total (1-5)

SEGMENTS
────────
Champions (555): Best customers
Loyal (X4X-X5X): Frequent buyers
At Risk (2XX): Declining
Lost (1XX): Churned
```

### Tableau RFM

| Segment | RFM Score | Action |
|---------|-----------|--------|
| Champions | 4-5, 4-5, 4-5 | Reward, VIP |
| Loyal | 3-4, 4-5, 3-4 | Upsell |
| Potential | 4-5, 1-2, 1-2 | Nurture |
| At Risk | 2-3, 2-3, 2-3 | Win-back |
| Lost | 1, 1-2, 1-2 | Re-engage or ignore |

## Implémentation RFM

### SQL Example

```sql
WITH rfm AS (
  SELECT
    user_id,
    DATE_DIFF(CURRENT_DATE(), MAX(order_date), DAY) as recency,
    COUNT(order_id) as frequency,
    SUM(order_value) as monetary
  FROM orders
  WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR)
  GROUP BY user_id
),
rfm_scores AS (
  SELECT
    user_id,
    NTILE(5) OVER (ORDER BY recency DESC) as r_score,
    NTILE(5) OVER (ORDER BY frequency) as f_score,
    NTILE(5) OVER (ORDER BY monetary) as m_score
  FROM rfm
)
SELECT
  user_id,
  r_score, f_score, m_score,
  CONCAT(r_score, f_score, m_score) as rfm_segment
FROM rfm_scores;
```

## Clustering Avancé

### K-Means

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Préparer features
features = df[['recency', 'frequency', 'monetary', 'avg_basket']]
scaler = StandardScaler()
scaled = scaler.fit_transform(features)

# Clustering
kmeans = KMeans(n_clusters=5, random_state=42)
df['segment'] = kmeans.fit_predict(scaled)

# Analyser les clusters
df.groupby('segment').agg({
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': 'mean'
})
```

### Choisir le Nombre de Clusters

```
MÉTHODES
────────
• Elbow method
• Silhouette score
• Business logic (3-7 segments)

RECOMMANDATION
──────────────
Start simple: 3-5 segments
Augmenter si insights supplémentaires
```

## Activation des Segments

### GA4 Audiences

```
GA4 → Admin → Audiences

EXEMPLES
────────
• High Value: purchase_value > 500€
• At Risk: last_active > 60 days
• Engaged: sessions_30d > 5
```

### Export vers Plateformes

| Destination | Méthode |
|-------------|---------|
| Google Ads | GA4 audience link |
| Meta | Custom audience upload |
| Email | CRM segment sync |
| CDP | API integration |

## Personnalisation par Segment

### Messaging Matrix

| Segment | Message | Offer | Channel |
|---------|---------|-------|---------|
| Champions | Exclusivité | VIP access | Email + SMS |
| Loyal | Merci | Loyalty points | Email |
| At Risk | Tu nous manques | -20% comeback | Email + Retargeting |
| Lost | Reviens | -30% | Win-back email |

### Content Strategy

| Segment | Content type |
|---------|--------------|
| New | Education, onboarding |
| Active | Features, tips |
| Power users | Advanced, beta access |
| At risk | Re-engagement, value reminder |

## Validation des Segments

### Critères de Qualité

| Critère | Description |
|---------|-------------|
| **Mesurable** | Données disponibles |
| **Accessible** | Peut être ciblé |
| **Substantiel** | Taille suffisante |
| **Différencié** | Comportement distinct |
| **Actionnable** | Actions possibles |

### A/B Test par Segment

```
VALIDER L'APPROCHE
──────────────────
Test: Message personnalisé vs générique
Par segment

SI personnalisé > générique:
→ Segmentation validée
```

## Checklist Segmentation

- [ ] Données clients disponibles
- [ ] Méthode de segmentation choisie
- [ ] Segments créés et nommés
- [ ] Taille des segments suffisante
- [ ] Segments dans GA4/CDP
- [ ] Export vers plateformes
- [ ] Messaging par segment
- [ ] Performance par segment suivie
