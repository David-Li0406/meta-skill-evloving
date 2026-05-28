# Guide de Contribution

Ce guide explique comment ajouter de nouveaux agents au skill web-agency.

## Principes Fondamentaux

### 1. Single Responsibility Principle (SRP)

Chaque agent doit avoir **une seule responsabilité** clairement définie.

**Mauvais exemple :**
```
Agent "gestion-projet" qui fait tout : planning, estimation, communication...
```

**Bon exemple :**
```
Agent "chiffrage" → Estimer les charges en jours/homme
Agent "creation-planning" → Créer le planning projet
Agent "email-relance" → Rédiger les emails de relance
```

### 2. Délégation Claire

Un agent doit explicitement indiquer ce qu'il **NE fait PAS** et vers quel agent déléguer.

```markdown
Tu NE fais PAS :
- L'estimation budgétaire (→ `chiffrage`)
- La communication client (→ `communication/orchestrator`)
```

## Structure d'un Agent

### Fichier Agent (`.md`)

```markdown
---
name: nom-agent
description: Description courte de la responsabilité unique
---

# Agent [Nom]

Tu es spécialisé dans **[responsabilité unique]**.

## Ta Responsabilité Unique

> [Description précise en une phrase]

Tu NE fais PAS :
- [Tâche 1] (→ `agent-1`)
- [Tâche 2] (→ `agent-2`)

## Input Attendu

| Type | Description |
|------|-------------|
| [Type 1] | [Description] |

## Processus

```
INPUT
  ↓
1. ÉTAPE 1
  ↓
2. ÉTAPE 2
  ↓
OUTPUT
```

## Template de Sortie

```markdown
# [Titre]

## Section 1
[Contenu attendu]

## Section 2
[Contenu attendu]
```

## Règles

1. [Règle 1]
2. [Règle 2]
```

### Sections Obligatoires

| Section | Description |
|---------|-------------|
| `name` (frontmatter) | Identifiant unique de l'agent |
| `description` (frontmatter) | Description courte |
| `Ta Responsabilité Unique` | Définition précise du périmètre |
| `Tu NE fais PAS` | Délégations explicites |
| `Template de Sortie` | Format de l'output attendu |

### Sections Recommandées

| Section | Description |
|---------|-------------|
| `Input Attendu` | Types d'entrées acceptées |
| `Processus` | Étapes de traitement |
| `Règles` | Contraintes et bonnes pratiques |

## Ajouter un Nouvel Agent

### Étape 1 : Identifier le Sous-Domaine

```
agents/
└── project-management/
    ├── avant-projet/      ← Phase commerciale
    ├── pilotage/          ← Suivi projet
    ├── communication/     ← Échanges client
    ├── livraison/         ← Recette et livraison
    └── facturation/       ← Facturation
```

### Étape 2 : Créer le Fichier Agent

```bash
# Exemple : nouvel agent de communication
touch agents/project-management/communication/email-rappel-paiement.md
```

### Étape 3 : Rédiger l'Agent

Utiliser la structure décrite ci-dessus avec toutes les sections obligatoires.

### Étape 4 : Mettre à Jour l'Orchestrateur

Ajouter le nouvel agent dans l'orchestrateur du sous-domaine :

```markdown
## Tes Agents Spécialisés

| Agent | Responsabilité unique |
|-------|----------------------|
| `email-rappel-paiement` | Emails de rappel de paiement |  ← NOUVEAU
```

Et dans les règles de routage :

```markdown
## Règles de Routage

| Requête | Agent |
|---------|-------|
| "Le client n'a pas payé" | `email-rappel-paiement` |  ← NOUVEAU
```

### Étape 5 : Ajouter les Tests

1. **Ajouter le cas de test** dans `tests/config.js` :

```javascript
const AGENT_TEST_CASES = {
  // ...
  'email-rappel-paiement': {
    category: 'communication',
    sampleInput: 'Facture impayée depuis 30 jours',
    expectedBehavior: [
      'professional tone',
      'reference invoice',
      'clear deadline'
    ],
    outputContains: ['Facture', 'Échéance', 'Paiement']
  }
};
```

2. **Mettre à jour le routage attendu** :

```javascript
const EXPECTED_ROUTING = {
  'communication': [
    // ...
    { intent: 'rappel paiement', agent: 'email-rappel-paiement' }
  ]
};
```

### Étape 6 : Lancer les Tests

```bash
cd .web-agency/orchestration-framework/tests
bash run-tests.sh
```

**Tous les tests doivent passer avant de soumettre.**

Les tests vérifient :
- Structure des agents (frontmatter, sections SRP)
- Cohérence du routage (références valides)
- Existence des templates
- Workflows d'intégration
- Correspondance routage/capacités agents

## Ajouter un Nouveau Template

### Emplacement

```
templates/
└── project-management/
    ├── brief-client.md
    ├── estimation.md
    └── nouveau-template.md  ← NOUVEAU
```

### Structure d'un Template

```markdown
# Template : [Nom du Template]

## Section 1

| Champ | Valeur |
|-------|--------|
| **Champ 1** | [Placeholder] |

---

## Section 2

### Sous-section
<!-- Instructions pour remplir -->

[Contenu avec placeholders]

---

## Validation

| Rôle | Nom | Date | Signature |
|------|-----|------|-----------|
| [Rôle] | | | |
```

### Règles pour les Templates

1. **Placeholders** : Utiliser `[texte]` pour les champs à remplir
2. **Instructions** : Utiliser `<!-- commentaires -->` pour guider
3. **Sections** : Minimum 3 sections avec `##`
4. **Tableaux** : Privilégier les tableaux pour les données structurées

### Mettre à Jour les Tests

Ajouter le template dans `tests/validate-templates.test.js` :

```javascript
const EXPECTED_TEMPLATES = [
  // ...
  'nouveau-template.md'
];
```

## Conventions de Nommage

### Agents

| Pattern | Exemple | Usage |
|---------|---------|-------|
| `action-objet` | `collecte-besoin` | Action sur un objet |
| `type-action` | `email-relance` | Type de communication |
| `analyse-objet` | `analyse-ecarts` | Analyse spécifique |

### Templates

| Pattern | Exemple |
|---------|---------|
| `objet.md` | `brief-client.md` |
| `action-objet.md` | `compte-rendu.md` |

### Orchestrateurs

Toujours nommés `orchestrator.md` dans leur répertoire.

## Checklist de Contribution

### Avant de coder

- [ ] Lire un agent existant similaire comme référence
- [ ] Identifier le bon sous-domaine
- [ ] Vérifier qu'un agent similaire n'existe pas déjà

### Pendant le développement

- [ ] Agent a une responsabilité unique claire
- [ ] Section "Tu NE fais PAS" présente avec délégations
- [ ] Template de sortie défini
- [ ] Orchestrateur mis à jour avec règles de routage
- [ ] Tests ajoutés dans `config.js`

### Avant de soumettre

```bash
# OBLIGATOIRE : Lancer tous les tests
cd .web-agency/orchestration-framework/tests
bash run-tests.sh

# Vérifier : 7 suites passent, 0 échec
```

- [ ] **Tous les tests passent** (7/7 suites)
- [ ] Documentation à jour si nécessaire
- [ ] Commit message suit le format conventionnel

## Besoin d'Aide ?

- Consulter les agents existants comme référence
- Lire `docs/examples.md` pour des exemples d'utilisation
- Consulter `docs/adr/` pour les décisions d'architecture
- Exécuter les tests pour valider la structure
