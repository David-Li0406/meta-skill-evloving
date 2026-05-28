---
name: specification-technique
description: Politique et standards de rédaction des spécifications techniques (Niveau POURQUOI)
workflows:
  - id: wf-creation
    phase: Conception
---

# Politique de Spécification Technique

Tu définis les **standards et politiques** pour la rédaction des spécifications techniques.

## Rôle de cet Agent (Niveau POURQUOI)

> **Ce que tu fais** : Définir les STANDARDS de documentation technique
> **Ce que tu ne fais pas** : Rédiger les spécifications détaillées ou le code
>
> → Process de spécification : `web-dev-process/agents/design/technical-spec`
> → Implémentation : Skills technologiques spécialisés

```
┌─────────────────────────────────────────────────────────────────┐
│  NIVEAU 1 : POURQUOI (direction-technique) ← ICI                │
│  → "Pourquoi ces standards ? Pour clarté et maintenabilité"     │
│  → "Politiques : structure, contenu obligatoire, validation"    │
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 2 : QUOI (web-dev-process)                              │
│  → "Quoi documenter ? Architecture, données, API, tests"        │
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 3 : COMMENT (skills technologiques)                     │
│  → "Templates, code, migrations, configurations"                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Questions de Clarification

Avant de décider, pose ces questions :

### Contexte
- Quelle fonctionnalité ou module doit être spécifié ?
- Quel est le niveau de maturité du besoin ? (Idée, brief, maquettes)
- Qui sont les lecteurs de la spécification ? (Dev junior, senior, équipe externe)
- Existe-t-il des spécifications de référence ou templates ?

### Objectifs
- Quel niveau de détail est attendu ? (Vue d'ensemble, détaillé, très détaillé)
- Quels sont les cas d'usage critiques à documenter ?
- La spécification servira-t-elle de base contractuelle ?
- Quels aspects techniques sont prioritaires ? (Architecture, données, API, UI)

### Risques
- Quelles zones d'incertitude doivent être clarifiées ?
- Y a-t-il des risques de sur-spécification ou sous-spécification ?
- Les spécifications seront-elles maintenues à jour pendant le développement ?
- Y a-t-il des dépendances entre modules à documenter ?

---

## Standards de Spécification

### Principes Fondamentaux

| Principe | Description | Objectif |
|----------|-------------|----------|
| **Clarté** | Langage précis, pas d'ambiguïté | Compréhension |
| **Complétude** | Tous les aspects couverts | Pas de surprises |
| **Traçabilité** | Lien vers user stories | Justification |
| **Testabilité** | Critères d'acceptation mesurables | Validation |
| **Maintenabilité** | Mise à jour facile | Durabilité |

### Niveaux de Spécification

| Niveau | Contenu | Audience |
|--------|---------|----------|
| **Haut niveau** | Vision, objectifs, contraintes | Stakeholders |
| **Fonctionnel** | User stories, règles métier | Product, QA |
| **Technique** | Architecture, API, données | Développeurs |
| **Implémentation** | Code, tests, config | Développeurs |

---

## Contenu Obligatoire

### Par Spécification Technique

| Section | Obligatoire | Description |
|---------|-------------|-------------|
| **Métadonnées** | ✅ | ID, version, auteur, date, statut |
| **Résumé** | ✅ | Description en 2-3 phrases |
| **User Story** | ✅ | Lien vers le besoin |
| **Critères d'Acceptation** | ✅ | Liste vérifiable |
| **Architecture** | ✅ | Composants impactés |
| **Modèle de Données** | Si applicable | Entités, relations |
| **API** | Si applicable | Endpoints, contrats |
| **Interface** | Si applicable | États, composants UI |
| **Sécurité** | ✅ | Auth, autorisations, données sensibles |
| **Performance** | Recommandé | Objectifs, optimisations |
| **Tests** | ✅ | Scénarios, types de tests |
| **Dépendances** | ✅ | Liées, bloquantes |

### Métadonnées Standards

| Champ | Format | Exemple |
|-------|--------|---------|
| **ID** | SPEC-[PROJET]-[NUM] | SPEC-SHOP-042 |
| **Version** | SemVer | 1.2.0 |
| **Statut** | Enum | Draft, En review, Validé, Obsolète |
| **Priorité** | P0/P1/P2/P3 | P1 |
| **Auteur** | Nom | Jean Dupont |
| **Reviewers** | Liste | Marie, Pierre |
| **Date création** | ISO 8601 | 2024-01-15 |
| **Date mise à jour** | ISO 8601 | 2024-02-01 |

---

## Critères d'Acceptation

### Format Standard

| Type | Format |
|------|--------|
| **Fonctionnel** | "L'utilisateur peut [action]" |
| **Technique** | "Le système [comportement attendu]" |
| **Performance** | "[Métrique] doit être [cible]" |
| **Sécurité** | "[Contrôle] est appliqué pour [risque]" |

### Qualités d'un Bon Critère

| Qualité | Description | Exemple |
|---------|-------------|---------|
| **Spécifique** | Pas d'ambiguïté | "Email validé par regex RFC 5322" |
| **Mesurable** | Vérifiable | "Temps de réponse < 200ms" |
| **Atteignable** | Réalisable techniquement | - |
| **Pertinent** | Lié à la user story | - |
| **Temporel** | Délai si applicable | - |

---

## Processus de Spécification

### Workflow Standard

```
Cadrage validé
     │
     ▼
┌─────────────────┐
│ 1. Identifier   │  ← Lister les features
│    les features │
└───────┬─────────┘
        │
        ▼
┌─────────────────┐
│ 2. Analyser     │  ← Comprendre le besoin
│    chaque       │
│    feature      │
└───────┬─────────┘
        │
        ▼
┌─────────────────┐
│ 3. Concevoir    │  ← Architecture, API, données
│    la solution  │
└───────┬─────────┘
        │
        ▼
┌─────────────────┐
│ 4. Rédiger      │  ← Document complet
│    la spec      │
└───────┬─────────┘
        │
        ▼
┌─────────────────┐
│ 5. Review       │  ← Validation technique
│    technique    │
└───────┬─────────┘
        │
        ▼
┌─────────────────┐
│ 6. Validation   │  ← Approbation finale
│    finale       │
└─────────────────┘
```

### Responsabilités

| Rôle | Responsabilité |
|------|----------------|
| **Tech Lead** | Valider architecture, reviewer specs |
| **Développeur** | Rédiger specs, implémenter |
| **Product** | Valider critères fonctionnels |
| **QA** | Valider testabilité |

---

## Templates par Type

### Feature Standard

| Section | Contenu |
|---------|---------|
| Résumé | Description fonctionnelle |
| User Story | "En tant que... je veux... afin de..." |
| Critères d'Acceptation | Liste vérifiable |
| Architecture | Composants impactés |
| Modèle de Données | Si modifications |
| API | Si endpoints modifiés |
| Tests | Scénarios unitaires, intégration, e2e |

### Feature CRUD

| Section | Contenu |
|---------|---------|
| Entité | Nom, attributs, validations |
| Opérations | Create, Read, Update, Delete, List |
| Autorisations | Par opération et rôle |
| Pagination | Si applicable |
| Filtres/Tri | Si applicable |

### Intégration Externe

| Section | Contenu |
|---------|---------|
| Service | Nom, documentation |
| Authentification | Type, credentials |
| Endpoints | Utilisés, rate limits |
| Mapping | Données externes → internes |
| Gestion d'erreurs | Retry, fallback |
| Monitoring | Alertes, logs |

### Feature Temps Réel

| Section | Contenu |
|---------|---------|
| Technologie | WebSocket/SSE/Polling |
| Events | Types, payloads |
| Connexion | Reconnexion, heartbeat |
| Scalabilité | Redis pub/sub, etc. |

---

## Politique de Validation

### Niveaux de Review

| Niveau | Reviewers | Critères |
|--------|-----------|----------|
| **Self-review** | Auteur | Checklist complète |
| **Peer review** | 1-2 devs | Faisabilité technique |
| **Tech lead review** | Tech lead | Architecture, standards |
| **Cross-functional** | Product, QA | Complétude, testabilité |

### Checklist de Validation

#### Avant Review

- [ ] Toutes les sections obligatoires remplies
- [ ] Critères d'acceptation testables
- [ ] Pas d'ambiguïté
- [ ] Liens vers dépendances

#### Review Technique

- [ ] Architecture cohérente
- [ ] Pas de sur-ingénierie
- [ ] Performance considérée
- [ ] Sécurité considérée
- [ ] Tests définis

#### Validation Finale

- [ ] Tous les reviewers approuvent
- [ ] Critères fonctionnels validés par Product
- [ ] Estimation réaliste

---

## Politique de Mise à Jour

### Quand Mettre à Jour

| Situation | Action |
|-----------|--------|
| Découverte en dev | Mettre à jour + notifier |
| Changement de scope | Nouvelle version |
| Clarification | Mise à jour mineure |
| Obsolescence | Marquer comme obsolète |

### Gestion des Versions

| Type de Changement | Incrément Version |
|--------------------|-------------------|
| Correction typo | Aucun |
| Clarification | Patch (1.0.x) |
| Ajout de détails | Minor (1.x.0) |
| Changement de scope | Major (x.0.0) |

---

## Points d'Escalade

| Situation | Action | Responsable |
|-----------|--------|-------------|
| Ambiguïté fonctionnelle | Retour Product | Product Owner |
| Complexité excessive | Review architecture | Tech Lead |
| Impact sécurité | Consultation securite/ | Security |
| Impact performance | Consultation performance/ | DevOps |
| Blocage de dépendance | Escalade projet | Project Manager |

---

## Références

| Aspect | Agent de Référence |
|--------|-------------------|
| Templates détaillés | `web-dev-process/agents/design/technical-spec` |
| Modélisation données | `specification/modelisation-donnees` |
| Spécification API | `specification/specification-api` |
| Cadrage technique | `specification/cadrage-technique` |

### Ressources

- IEEE 830 - Software Requirements Specifications
- RFC 2119 - Key words for use in RFCs

## Livrables

| Livrable | Description |
|----------|-------------|
| Document de spécifications techniques | Specs détaillées par fonctionnalité avec critères d'acceptation |
| User stories techniques | Récits utilisateur avec conditions de réalisation et tests associés |
| Matrice de traçabilité | Mapping entre besoins fonctionnels et spécifications techniques |
