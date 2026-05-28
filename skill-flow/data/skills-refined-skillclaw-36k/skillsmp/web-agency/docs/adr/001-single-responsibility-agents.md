# ADR-001 : Single Responsibility Principle pour les Agents

## Statut

Accepté

## Contexte

Les premières versions des agents IA tendaient à être "omniscients" - un seul agent gérant tout le cycle de vie d'un projet. Cela posait plusieurs problèmes :

- **Prompts trop longs** : Difficiles à maintenir et à déboguer
- **Hallucinations** : Plus le scope est large, plus l'IA peut dériver
- **Réutilisabilité faible** : Impossible d'utiliser une partie sans le tout
- **Tests difficiles** : Comment valider un comportement global ?

## Décision

Appliquer le **Single Responsibility Principle (SRP)** à chaque agent :

> Chaque agent a une seule responsabilité clairement définie.

Concrètement :
- Un agent = une tâche atomique
- Chaque agent déclare explicitement ce qu'il NE fait PAS
- Les délégations vers d'autres agents sont explicites

### Exemple

**Avant (agent monolithique)** :
```
Agent "gestion-projet" :
- Collecte le besoin
- Rédige le brief
- Fait l'estimation
- Crée le planning
- Gère la communication
- ...
```

**Après (agents SRP)** :
```
Agent "collecte-besoin" : Extraire les infos des sources client
Agent "formalisation-brief" : Structurer le brief
Agent "chiffrage" : Estimer les charges
Agent "creation-planning" : Créer le planning
Agent "email-relance" : Rédiger les emails de relance
```

## Conséquences

### Positives

- **Prompts courts et maintenables** : ~100-150 lignes par agent
- **Comportement prévisible** : Scope limité = moins de dérive
- **Réutilisabilité** : Agents composables comme des LEGO
- **Testabilité** : Validation facile du comportement
- **Évolutivité** : Ajout/modification d'agents sans impact global

### Négatives

- **Plus de fichiers** : 24 agents au lieu de 3-4 gros agents
- **Orchestration nécessaire** : Besoin de coordonner les agents
- **Courbe d'apprentissage** : Comprendre quel agent utiliser

## Alternatives Considérées

### 1. Agents par domaine métier

Un agent par grand domaine (Avant-projet, Pilotage, Communication...).

**Rejeté car** : Prompts encore trop longs (~500 lignes), difficulté à maintenir.

### 2. Un seul agent avec modes

Un agent unique avec des "modes" activables.

**Rejeté car** : Confusion sur le mode actif, difficile à déboguer.

### 3. Agents dynamiques générés

Générer les agents à la volée selon le besoin.

**Rejeté car** : Imprévisible, pas de garantie de qualité.

## Références

- [Single Responsibility Principle](https://en.wikipedia.org/wiki/Single-responsibility_principle)
- [Unix Philosophy](https://en.wikipedia.org/wiki/Unix_philosophy) : "Do one thing and do it well"
