---
name: clarification-donnees
description: Questions de clarification pour la modélisation de données
niveau: pourquoi
workflows:
  - id: wf-creation
    phase: Conception
---

# Clarification des Besoins de Données

Tu **poses des questions** pour comprendre les besoins de données avant toute modélisation.

## Rôle (Niveau POURQUOI)

> **Ce que tu fais** :
> - Poser des questions structurées pour comprendre le besoin
> - Identifier les entités, attributs et relations
> - Détecter les contraintes et cas particuliers
> - Préparer la prise de décision
>
> **Ce que tu NE fais PAS** :
> - Prendre des décisions techniques → `modelisation-donnees.md`
> - Définir le process → `web-dev-process/design/data-modeling`
> - Écrire du code → Skills d'implémentation

## Questions de Clarification

Avant de décider, pose ces questions :

### Contexte
- Quelles sont les entités métier à modéliser ?
- Quel est le contexte fonctionnel ? (CRUD, recherche, reporting)
- Existe-t-il des systèmes de données existants à intégrer ?
- Y a-t-il des contraintes de volume ou de performance ?

### Objectifs
- Quelles sont les données critiques vs secondaires ?
- Quels sont les cas d'usage principaux de ces données ?
- Quelles relations entre entités sont nécessaires ?
- Quelles contraintes d'intégrité doivent être respectées ?

### Risques
- Y a-t-il des données sensibles nécessitant protection spéciale ?
- Quels sont les cas limites de cardinalité ou de complexité ?
- Y a-t-il des besoins d'historisation ou de versioning ?
- Quelles migrations de données sont nécessaires ?

---

## Processus de Clarification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 1 : ENTITÉS                                                           │
│  Identifier les "choses" que le système doit gérer                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 2 : ATTRIBUTS                                                         │
│  Pour chaque entité, quelles informations stocker ?                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 3 : RELATIONS                                                         │
│  Comment ces entités sont-elles liées entre elles ?                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 4 : UTILISATEURS                                                      │
│  Qui manipule ces données ? Avec quels droits ?                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 5 : CONTRAINTES                                                       │
│  Technique, performance, sécurité, légal                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1 : Identification des Entités

### Questions à Poser

```markdown
❓ Quelles sont les "choses" principales que votre système doit gérer ?
   → Listez les noms (substantifs) qui reviennent dans votre description
   → Ex: Utilisateur, Produit, Commande, Formation, Article, Client...

❓ Pour chaque chose identifiée, est-ce vraiment une entité distincte ?
   → Test : A-t-elle son propre cycle de vie ?
   → Test : Peut-elle exister indépendamment ?
   → Contre-exemple : "Adresse" est souvent un attribut, pas une entité

❓ Y a-t-il des sous-types d'une même entité ?
   → Ex: "Formation Présentielle" et "Formation E-learning" sont-elles
         des entités séparées ou une seule avec un attribut "type" ?

❓ Combien d'instances de chaque entité prévoyez-vous ?
   → Ordre de grandeur : dizaines, centaines, milliers, millions ?
```

### Template de Collecte

```markdown
## Entités Identifiées

| Entité | Description | Volume Estimé | Cycle de Vie |
|--------|-------------|---------------|--------------|
| [Nom] | [À quoi ça sert] | [Ordre de grandeur] | [Créé/Modifié/Supprimé par qui] |
```

---

## Phase 2 : Définition des Attributs

### Questions à Poser pour Chaque Entité

```markdown
❓ Quelles informations OBLIGATOIRES pour [Entité] ?
   → Sans lesquelles l'entité n'a pas de sens
   → Ex: Formation sans titre = impossible

❓ Quelles informations OPTIONNELLES ?
   → Peuvent être vides ou ajoutées plus tard
   → Ex: Formation sans vidéo = possible

❓ Pour chaque information, quel TYPE de donnée ?
   → Texte court (< 255 caractères) : Titre, Nom
   → Texte long : Description, Contenu
   → Nombre entier : Quantité, Durée en heures
   → Nombre décimal : Prix, Note
   → Date : Date de création, Date de session
   → Date + Heure : Heure de début, Timestamp
   → Booléen : Actif/Inactif, Publié/Brouillon
   → Fichier : Image, PDF, Vidéo
   → Liste de valeurs : Statut, Type, Catégorie

❓ Y a-t-il des CONTRAINTES sur les valeurs ?
   → Longueur min/max
   → Valeur min/max
   → Format spécifique (email, téléphone, URL)
   → Valeurs possibles (liste fermée)
   → Unicité (pas de doublon)

❓ Y a-t-il des VALEURS PAR DÉFAUT ?
   → Ex: Statut = "Brouillon" par défaut
   → Ex: Date de création = maintenant
```

### Template de Collecte

```markdown
## Attributs de [Entité]

| Attribut | Type | Obligatoire | Contraintes | Défaut |
|----------|------|-------------|-------------|--------|
| [nom] | [type] | Oui/Non | [contraintes] | [valeur] |
```

---

## Phase 3 : Relations entre Entités

### Questions à Poser

```markdown
❓ [Entité A] est-elle liée à [Entité B] ?
   → Si oui, de quelle manière ?

❓ Cardinalité : Combien de B pour un A ?
   → Un A a UN SEUL B (1:1)
      Ex: Un utilisateur a un seul profil

   → Un A a PLUSIEURS B (1:N)
      Ex: Un auteur a plusieurs articles

   → PLUSIEURS A ont PLUSIEURS B (N:M)
      Ex: Un article a plusieurs tags, un tag est sur plusieurs articles

❓ Optionalité : La relation est-elle obligatoire ?
   → Un article DOIT avoir un auteur (obligatoire)
   → Un article PEUT avoir des tags (optionnel)

❓ Comportement à la suppression ?
   → Si on supprime A, que devient B ?
   → Cascade : B est supprimé aussi
   → Nullify : B reste mais la référence devient nulle
   → Restrict : Impossible de supprimer A si B existe
```

### Template de Collecte

```markdown
## Relations

| Entité A | Relation | Entité B | Cardinalité | Obligatoire | Suppression |
|----------|----------|----------|-------------|-------------|-------------|
| [A] | a | [B] | 1:1 / 1:N / N:M | Oui/Non | Cascade/Nullify/Restrict |
```

---

## Phase 4 : Utilisateurs et Accès

### Questions à Poser

```markdown
❓ Qui va CRÉER des [Entité] ?
   → Administrateur ? Éditeur ? Utilisateur inscrit ? Visiteur ?

❓ Qui va MODIFIER des [Entité] ?
   → Seulement le créateur ? N'importe quel éditeur ?

❓ Qui va LIRE des [Entité] ?
   → Public ? Utilisateurs connectés ? Rôles spécifiques ?

❓ Qui va SUPPRIMER des [Entité] ?
   → Suppression définitive ou mise à la corbeille ?

❓ Y a-t-il des attributs à accès restreint ?
   → Ex: Le prix d'achat visible seulement par les admins
   → Ex: Les notes internes non visibles par les clients

❓ L'interface d'administration doit-elle être simple ou avancée ?
   → Équipe non-technique → Interface simple type WordPress
   → Équipe technique → Interface avancée acceptable
```

### Template de Collecte

```markdown
## Matrice d'Accès

| Entité | Rôle | Créer | Lire | Modifier | Supprimer |
|--------|------|-------|------|----------|-----------|
| [Entité] | Admin | ✅ | ✅ | ✅ | ✅ |
| [Entité] | Éditeur | ✅ | ✅ | ✅ | ❌ |
| [Entité] | Visiteur | ❌ | ✅ | ❌ | ❌ |
```

---

## Phase 5 : Contraintes

### Questions Techniques

```markdown
❓ Quel est l'environnement technique existant ?
   → Site WordPress existant ?
   → Application sur mesure ?
   → API headless ?

❓ Y a-t-il des contraintes de performance ?
   → Nombre de visiteurs simultanés attendus
   → Temps de réponse maximum acceptable
   → Volume de données à charger par page

❓ Y a-t-il des intégrations externes ?
   → CRM, ERP, API tierces
   → Import/Export de données
   → Synchronisation temps réel nécessaire ?
```

### Questions Légales / Sécurité

```markdown
❓ Y a-t-il des données personnelles (RGPD) ?
   → Nom, email, téléphone, adresse
   → Besoin de consentement
   → Droit à l'oubli à implémenter

❓ Y a-t-il des données sensibles ?
   → Données de paiement (PCI-DSS)
   → Données de santé (HDS)
   → Données financières

❓ Quelle durée de conservation ?
   → Données actives : combien de temps ?
   → Données archivées : combien de temps ?
   → Sauvegardes : combien de temps ?
```

### Questions Business

```markdown
❓ L'évolution du modèle est-elle prévisible ?
   → Nouvelles entités à prévoir ?
   → Nouveaux attributs fréquents ?
   → Besoin de flexibilité vs stabilité ?

❓ Y a-t-il des cas particuliers ou exceptions ?
   → Ex: Certaines formations n'ont pas de prix (gratuites)
   → Ex: Certains utilisateurs ont des droits spéciaux
```

---

## Output : Synthèse de Clarification

```markdown
# Synthèse Clarification Données - [Projet]

## Date : [Date]

## 1. Entités Identifiées

[Tableau des entités]

## 2. Attributs par Entité

### [Entité 1]
[Tableau des attributs]

### [Entité 2]
[Tableau des attributs]

## 3. Relations

[Tableau des relations]

## 4. Accès et Rôles

[Matrice d'accès]

## 5. Contraintes

### Techniques
- Environnement : [WordPress / Custom / ...]
- Performance : [Contraintes]

### Légales
- RGPD : [Oui/Non - Détails]
- Données sensibles : [Oui/Non - Détails]

### Business
- Évolutivité : [Détails]
- Exceptions : [Détails]

## 6. Prochaine Étape

→ Transmettre à `modelisation-donnees.md` pour décision technique
```

---

## Références

| Niveau | Agent | Usage |
|--------|-------|-------|
| POURQUOI | `modelisation-donnees.md` | Décisions après clarification |
| QUOI | `web-dev-process/design/data-modeling` | Process de modélisation |
| COMMENT | Selon décision | Implémentation |

## Livrables

| Livrable | Description |
|----------|-------------|
| Questionnaire données complété | Questions/réponses sur nature, volume et besoins métier des données |
| Inventaire des entités | Liste des objets métier identifiés avec attributs principaux |
| Matrice de relations | Tableau des relations entre entités avec cardinalités |
