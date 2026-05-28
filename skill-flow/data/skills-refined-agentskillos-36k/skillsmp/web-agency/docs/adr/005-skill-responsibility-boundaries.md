# ADR-005 : Frontières de Responsabilités entre Skills Techniques

## Statut

Accepté (v2.0 - Clarification du modèle)

## Date

2024-12-23

## Contexte

L'analyse SRP a révélé des **chevauchements significatifs** entre trois skills techniques :
- `direction-technique` (59 agents)
- `web-dev-process` (64 agents)
- `wordpress-gutenberg-expert` (42 agents)

### Problèmes identifiés

1. **Duplications CI/CD** : 4 agents dans 3 skills parlent de CI/CD
2. **Duplications Code Review** : 2 agents quasi-identiques
3. **Confusion sur qui fait quoi** : Où s'arrête la stratégie ? Où commence l'implémentation ?
4. **Manque de clarification** : Les agents ne posent pas assez de questions avant d'agir

## Décision

Adopter une **séparation en 3 niveaux de responsabilité** avec des rôles clairement définis :

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    NIVEAU 1 : POURQUOI                                       │
│                   (direction-technique)                                      │
│                                                                              │
│  Rôle : QUESTIONNER et CLARIFIER le besoin                                  │
│                                                                              │
│  → Poser un MAXIMUM de questions pour comprendre le contexte                │
│  → Identifier les objectifs réels derrière la demande                       │
│  → Valider les hypothèses avant de déléguer                                 │
│  → Prendre les décisions stratégiques                                       │
│                                                                              │
│  Output : Décisions documentées, ADRs, Politiques validées                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                      (besoin clarifié, décisions prises)
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       NIVEAU 2 : QUOI                                        │
│                    (web-dev-process)                                         │
│                                                                              │
│  Rôle : CONTEXTUALISER en 3 couches                                         │
│                                                                              │
│  1. GLOBAL "Métier"     → Quel process métier standard appliquer ?          │
│  2. AGENCE "Spécifique" → Quelles particularités de l'agence ?              │
│  3. PROJET "Exception"  → Quelles exceptions projet outrepassent ?          │
│                                                                              │
│  Output : Process adapté, Templates contextualisés, Checklists              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                      (process identifié, contexte établi)
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      NIVEAU 3 : COMMENT                                      │
│                (wordpress-gutenberg-expert, etc.)                            │
│                                                                              │
│  Rôle : EXÉCUTER avec spécifications                                        │
│                                                                              │
│  → Dans quel environnement ?                                                │
│  → Avec quelles spécifications techniques ?                                 │
│  → Quels critères d'acceptance ?                                            │
│  → Qu'est-ce qu'il y a à produire concrètement ?                            │
│                                                                              │
│  Output : Code, Configs, Scripts, Livrables testables                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Détail des Responsabilités

### NIVEAU 1 : POURQUOI (direction-technique)

#### Rôle Principal

**Poser un MAXIMUM de questions** avant toute délégation pour :
- Comprendre le vrai besoin (pas juste la demande)
- Identifier les contraintes cachées
- Valider les hypothèses
- Prendre des décisions éclairées

#### Questions Types à Poser

```markdown
## Questions de Clarification (Niveau POURQUOI)

### Contexte Business
- Quel est l'objectif business derrière cette demande ?
- Qui sont les utilisateurs finaux ?
- Quelles sont les contraintes de délai ?
- Y a-t-il des dépendances avec d'autres projets ?

### Contraintes Techniques
- Quelles sont les contraintes d'infrastructure existantes ?
- Y a-t-il des choix technologiques imposés ?
- Quels sont les SLAs attendus (dispo, perf, sécurité) ?

### Risques et Priorités
- Qu'est-ce qui est non-négociable ?
- Qu'est-ce qui peut être simplifié si besoin ?
- Quels sont les risques identifiés ?

### Validation
- Comment saura-t-on que c'est réussi ?
- Qui valide les livrables ?
```

#### Output Attendu

- Décisions documentées dans un ADR ou compte-rendu
- Politiques et standards à appliquer
- Critères de succès définis
- Feu vert pour déléguer au niveau QUOI

---

### NIVEAU 2 : QUOI (web-dev-process)

#### Rôle Principal

**Contextualiser le process** en 3 couches successives :

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  COUCHE 1 : GLOBAL "Métier"                                                  │
│  ──────────────────────────────────────────────────────────────────────     │
│  → Quel est le process métier standard pour ce type de demande ?            │
│  → Quelles sont les bonnes pratiques universelles ?                         │
│                                                                              │
│  Exemple : "Pour un setup env local, le process standard est :              │
│            Clone → Install deps → Config env → Start → Verify"              │
├─────────────────────────────────────────────────────────────────────────────┤
│  COUCHE 2 : AGENCE "Spécifique"                                              │
│  ──────────────────────────────────────────────────────────────────────     │
│  → Quelles particularités l'agence a-t-elle pour ce process ?               │
│  → Quels outils/conventions l'agence impose-t-elle ?                        │
│                                                                              │
│  Exemple : "L'agence utilise wp-env plutôt que Docker custom.               │
│            Les .env doivent suivre le template agence."                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  COUCHE 3 : PROJET "Exception"                                               │
│  ──────────────────────────────────────────────────────────────────────     │
│  → Quelles particularités projet outrepassent les règles ci-dessus ?        │
│  → Quelles exceptions sont justifiées pour CE projet ?                      │
│                                                                              │
│  Exemple : "Ce projet nécessite WooCommerce, donc dépendance MySQL          │
│            obligatoire. Exception : PHP 7.4 pour compat plugin legacy."     │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Questions Types à Poser

```markdown
## Questions de Contextualisation (Niveau QUOI)

### Couche Métier
- Ce cas correspond-il à un process standard existant ?
- Quelles étapes du process standard s'appliquent ?

### Couche Agence
- Y a-t-il des conventions agence spécifiques ?
- Quels outils sont imposés par l'agence ?
- Y a-t-il des templates agence à réutiliser ?

### Couche Projet
- Quelles contraintes projet modifient le process ?
- Y a-t-il des exceptions documentées à appliquer ?
- Des décisions ADR projet changent-elles la donne ?
```

#### Output Attendu

- Process adapté au contexte (Métier + Agence + Projet)
- Templates et checklists contextualisés
- Instructions claires pour le niveau COMMENT

---

### NIVEAU 3 : COMMENT (wordpress-gutenberg-expert, etc.)

#### Rôle Principal

**Exécuter avec précision** en répondant à :

| Question | Réponse à Fournir |
|----------|-------------------|
| **Environnement ?** | Local wp-env, Staging, CI, Prod |
| **Spécifications ?** | Versions, configs, dépendances |
| **Critères d'acceptance ?** | Tests à passer, validations |
| **Livrables ?** | Fichiers créés, code produit |

#### Structure d'Exécution

```markdown
## Exécution (Niveau COMMENT)

### Environnement Cible
- Type : [Local / Staging / CI / Prod]
- Versions : PHP X.Y, WP X.Y, MySQL X.Y
- Particularités : [Debug ON, Multisite, etc.]

### Spécifications Techniques
- Fichiers à créer : [liste]
- Dépendances : [packages]
- Configuration : [paramètres]

### Critères d'Acceptance
- [ ] Critère 1 mesurable
- [ ] Critère 2 mesurable
- [ ] Critère 3 mesurable

### Livrables
1. [Fichier/Code/Script 1]
2. [Fichier/Code/Script 2]
3. [Documentation mise à jour]
```

#### Output Attendu

- Code fonctionnel et testé
- Configurations prêtes à l'emploi
- Scripts exécutables
- Critères d'acceptance validés

---

## Exemple Complet : Setup Environnement Local WordPress

### Étape 1 : POURQUOI

```markdown
## Questions Posées (direction-technique)

❓ Pourquoi avez-vous besoin d'un env local ?
   → "Pour développer un nouveau plugin de réservation"

❓ Quelles contraintes de parité avec la prod ?
   → "PHP 8.2, WP 6.4, MySQL 8.0 obligatoires"

❓ Y a-t-il des plugins spécifiques requis ?
   → "WooCommerce pour les paiements"

❓ Quel est l'objectif de temps de setup ?
   → "Nouveau dev opérationnel en < 15 min"

## Décision
✅ Utiliser wp-env (standard agence) avec config WooCommerce
✅ Objectif 15 min validé
✅ Déléguer à web-dev-process
```

### Étape 2 : QUOI

```markdown
## Contextualisation (web-dev-process)

### Couche Métier (Process Standard)
→ Process "Setup Env Local" : Clone → Install → Config → Start → Verify

### Couche Agence (Spécificités)
→ Agence utilise wp-env comme standard
→ Template .wp-env.json agence disponible
→ Convention : port 8888 pour tous les projets

### Couche Projet (Exceptions)
→ Exception : WooCommerce requis (pas dans template agence)
→ Exception : Données de démo produits à charger

## Process Adapté
1. Clone repo
2. npm install (wp-env)
3. Créer .wp-env.json (base agence + WooCommerce)
4. wp-env start
5. Charger données démo WooCommerce
6. Vérifier accès
```

### Étape 3 : COMMENT

```markdown
## Exécution (wordpress-gutenberg-expert)

### Environnement
- Local wp-env
- PHP 8.2, WP 6.4, MySQL 8.0
- Debug activé

### Spécifications
{
  "core": "WordPress/WordPress#6.4",
  "phpVersion": "8.2",
  "plugins": ["woocommerce"],
  "config": { "WP_DEBUG": true }
}

### Critères d'Acceptance
- [ ] wp-env start sans erreur
- [ ] localhost:8888 accessible
- [ ] WooCommerce visible dans admin
- [ ] Setup < 15 min

### Livrables
- .wp-env.json
- package.json (scripts)
- README.md (Getting Started)
- scripts/seed-woo.sh (données démo)
```

---

## Matrice de Responsabilités Mise à Jour

| Domaine | POURQUOI (Questions) | QUOI (3 Couches) | COMMENT (Exécution) |
|---------|----------------------|------------------|---------------------|
| **Env Local** | Contraintes ? Parité ? Délai ? | Métier/Agence/Projet | wp-env, configs, scripts |
| **CI/CD** | Objectifs qualité ? SLA ? | Process standard + exceptions | GitHub Actions YAML |
| **Sécurité** | Données sensibles ? RGPD ? | Politique + adaptations projet | Nonces, sanitize, code |
| **Performance** | SLO cibles ? Budget ? | Audit + optimisations | Core Web Vitals, code |

---

## Conséquences

### Positives

- **Clarification systématique** : On ne code plus sans avoir compris
- **Contextualisation fine** : 3 couches évitent les solutions génériques
- **Traçabilité** : Chaque décision est documentée
- **Qualité** : Les critères d'acceptance sont définis avant l'exécution

### Négatives

- **Plus de questions** : Peut sembler ralentir au début
- **Documentation** : Chaque niveau doit produire un output clair
- **Discipline** : Respecter la séparation demande de la rigueur

## Références

- [Analyse SRP v2.0](../../../../docs/analysis/SRP-ANALYSIS.md)
- [Workflow Setup Local WordPress](../../workflows/setup-local-wordpress.md)
