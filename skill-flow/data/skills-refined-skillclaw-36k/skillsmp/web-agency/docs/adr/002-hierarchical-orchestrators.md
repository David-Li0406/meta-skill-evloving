# ADR-002 : Orchestrateurs Hiérarchiques

## Statut

Accepté

## Contexte

Avec l'adoption du SRP (ADR-001), nous avons 24+ agents spécialisés. Se pose la question : **comment l'utilisateur sait-il quel agent invoquer ?**

Options :
1. L'utilisateur connaît tous les agents
2. Un orchestrateur unique route tout
3. Des orchestrateurs hiérarchiques par niveau

## Décision

Adopter une **architecture d'orchestrateurs hiérarchiques** à 3 niveaux :

```
SKILL.md (Niveau 1)
    └── Routing par domaine métier
        │
        ├── project-management/orchestrator.md (Niveau 2)
        │   └── Routing par sous-domaine
        │       │
        │       ├── avant-projet/orchestrator.md (Niveau 3)
        │       │   └── Routing vers agents spécifiques
        │       │       ├── collecte-besoin.md
        │       │       ├── formalisation-brief.md
        │       │       └── ...
        │       │
        │       ├── pilotage/orchestrator.md
        │       ├── communication/orchestrator.md
        │       └── ...
        │
        ├── strategy/orchestrator.md (à venir)
        └── ...
```

### Règles de Routage

Chaque orchestrateur définit des **règles de routage** basées sur les mots-clés :

```markdown
## Règles de Routage

| Requête | Agent |
|---------|-------|
| "J'ai reçu un email du client" | `collecte-besoin` |
| "Structure le brief" | `formalisation-brief` |
| "Combien ça va coûter ?" | `chiffrage` |
```

## Conséquences

### Positives

- **Découvrabilité** : L'utilisateur n'a pas besoin de connaître tous les agents
- **Scalabilité** : Ajout de domaines sans surcharger un orchestrateur central
- **Contexte préservé** : Chaque niveau ajoute du contexte pertinent
- **Maintenance distribuée** : Chaque sous-domaine gère son routage

### Négatives

- **Latence potentielle** : 3 niveaux = 3 décisions de routage
- **Complexité** : Plus de fichiers orchestrator.md à maintenir
- **Risque de mauvais routage** : Si les règles sont ambiguës

## Alternatives Considérées

### 1. Orchestrateur unique plat

Un seul orchestrateur connaissant tous les agents.

**Rejeté car** :
- Prompt trop long avec 24+ agents
- Difficile à maintenir
- Pas de contexte par domaine

### 2. Pas d'orchestrateur (accès direct)

L'utilisateur invoque directement l'agent souhaité.

**Rejeté car** :
- Courbe d'apprentissage élevée
- Erreurs d'invocation fréquentes
- Pas adapté aux non-experts

### 3. Orchestrateur IA dynamique

Un LLM décide dynamiquement du routage.

**Rejeté car** :
- Imprévisible et non-déterministe
- Difficile à déboguer
- Coût computationnel

## Implémentation

```
web-agency/
├── SKILL.md                           # Orchestrateur Niveau 1
├── agents/
│   └── project-management/
│       ├── orchestrator.md            # Orchestrateur Niveau 2
│       ├── avant-projet/
│       │   ├── orchestrator.md        # Orchestrateur Niveau 3
│       │   ├── collecte-besoin.md     # Agent leaf
│       │   └── ...
│       └── ...
```

## Métriques de Succès

- Taux de routage correct > 95%
- Temps de routage < 1 seconde par niveau
- Pas plus de 3 niveaux de profondeur
