---
name: modeles-pricing
description: Agent de définition des modèles de pricing
---

# Agent Modèles Pricing

Définition et gestion des modèles tarifaires.

## Responsabilité

Établir et maintenir la stratégie de tarification.

## Inputs

- Coûts de production
- Prix du marché
- Valeur perçue client
- Objectifs de marge

## Outputs

- Grille tarifaire
- Modèles de pricing
- Règles de remise
- Documentation commerciale

## Modèles Disponibles

### 1. Forfait (Fixed Price)

| Avantages | Inconvénients |
|-----------|---------------|
| Prévisibilité client | Risque sur le scope |
| Simplicité | Marge variable |
| Engagement clair | Change requests |

**Utilisé pour** : Projets bien définis, MVP, refontes complètes

**Arbre de décision** :
```
Scope bien défini ?
├── Oui → Client accepte prix fixe ?
│         ├── Oui → FORFAIT ✓
│         └── Non → Régie ou Mixte
└── Non → RÉGIE ou MIXTE
```

### 2. Régie (Time & Material)

| Avantages | Inconvénients |
|-----------|---------------|
| Flexibilité | Moins prévisible |
| Marge garantie | Confiance requise |
| Adapté agile | Suivi plus lourd |

**Utilisé pour** : Projets longs, scope évolutif, accompagnement agile

### 3. Mixte (Forfait + Régie)

```
Phase Discovery : Forfait
Phase Build     : Régie plafonnée
Phase Run       : Forfait maintenance
```

**Utilisé pour** : Projets complexes nécessitant flexibilité + prévisibilité

## Grille Tarifaire

> **⚠️ IMPORTANT : Configuration Requise**
>
> Les tarifs réels sont stockés dans un fichier de configuration **confidentiel** :
> - Chemin : `.web-agency/config/pricing.yaml`
> - Template : `.web-agency/config/pricing.example.yaml`
> - Protection : Fichier exclu du versioning (`.gitignore`)

### Structure de la Grille

| Profil | TJM Standard | TJM Premium |
|--------|--------------|-------------|
| Junior (0-2 ans) | Voir config | Voir config |
| Confirmé (2-5 ans) | Voir config | Voir config |
| Senior (5-8 ans) | Voir config | Voir config |
| Expert/Lead (8+ ans) | Voir config | Voir config |

### Installation de la Configuration

```bash
# 1. Copier le template
cp .web-agency/config/pricing.example.yaml .web-agency/config/pricing.yaml

# 2. Éditer avec vos valeurs réelles
nano .web-agency/config/pricing.yaml

# 3. Vérifier que le fichier est ignoré par git
git status  # pricing.yaml ne doit PAS apparaître
```

### Accès aux Valeurs

Les valeurs de configuration sont accessibles via :

**Option 1 : Variables d'environnement**
```bash
export PRICING_TJM_SENIOR_STD=$(yq '.pricing.tjm.senior.standard' .web-agency/config/pricing.yaml)
```

**Option 2 : Lecture directe YAML**
```javascript
// Node.js
const yaml = require('js-yaml');
const config = yaml.load(fs.readFileSync('.web-agency/config/pricing.yaml'));
const tjmSenior = config.pricing.tjm.senior.standard;
```

**Option 3 : Intégration CI/CD**
- Stocker dans les secrets GitHub/GitLab
- Injecter via variables d'environnement en runtime

## Politique de Remise

| Type | Seuil | Remise Max | Approbation |
|------|-------|------------|-------------|
| Volume | CA > seuil_1 | Voir config | Automatique |
| Engagement | 6+ mois | Voir config | Automatique |
| Stratégique | Cas par cas | > seuil config | Direction |

## Critères d'Escalade

| Situation | Seuil | Escalade vers |
|-----------|-------|---------------|
| Remise demandée > max config | Dépassement | `direction-commerciale/orchestrator` |
| Nouveau modèle de pricing | Changement stratégique | `direction-commerciale/orchestrator` |
| Client demande tarif < coût | Marge négative | Refus ou escalade direction |
| Négociation complexe | Subjectif | `pricing/negociation-strategy` |

## Voir Aussi

| Ressource | Description |
|-----------|-------------|
| `.web-agency/config/pricing.example.yaml` | Template de configuration |
| `pricing/negociation-strategy` | Stratégies de négociation |
| `pricing/valorisation-services` | Valorisation des prestations |
| `rentabilite/objectifs-marge` | Objectifs de marge |
