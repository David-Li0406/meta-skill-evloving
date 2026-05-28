# Livrables par Workflow

> Chaque workflow produit des livrables avec des critères d'acceptation adaptés au positionnement client.

---

## wf-creation : Projet de Création

### Phase BRIEF

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **Cahier des charges** | Document de spécifications | Validé par le client, périmètre défini |
| **Planning macro** | Jalons et dates clés | Réaliste, ressources identifiées |
| **Estimation budgétaire** | Chiffrage détaillé | Marge d'erreur < 20% |
| **Matrice de positionnement** | Triangle Budget/Qualité/Délai | Signé par le client |

```yaml
livrable_brief:
  cahier_des_charges:
    format: markdown | pdf
    sections_obligatoires:
      - contexte_projet
      - objectifs_mesurables
      - perimetre_fonctionnel
      - contraintes_techniques
      - criteres_succes
    validation: signature_client

  planning_macro:
    format: gantt | timeline
    contenu:
      - phases_principales
      - jalons_cles
      - points_validation
    precision: semaine

  estimation:
    format: devis_detaille
    contenu:
      - postes_budgetaires
      - hypotheses
      - exclusions
    marge_erreur: 20%
```

### Phase CONCEPTION

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **Maquettes UI** | Designs haute fidélité | Validées sur écrans cibles |
| **Spécifications techniques** | Architecture, stack, APIs | Revue technique OK |
| **Prototype interactif** | Démo cliquable | Parcours utilisateur validés |
| **ADR** | Architecture Decision Records | Choix justifiés et documentés |

```yaml
livrable_conception:
  maquettes:
    niveau_minimal:
      - wireframes_principaux
      - 1_resolution
    niveau_standard:
      - maquettes_hd
      - responsive_3_breakpoints
      - design_system_base
    niveau_premium:
      - maquettes_pixel_perfect
      - responsive_5_breakpoints
      - design_system_complet
      - micro_interactions

  specifications:
    niveau_minimal:
      - schema_architecture
      - liste_endpoints
    niveau_standard:
      - diagrammes_c4
      - specs_api_openapi
      - modele_donnees
    niveau_premium:
      - documentation_exhaustive
      - poc_technique
      - benchmarks_performance
```

### Phase PRODUCTION

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **Code source** | Application fonctionnelle | Tests passants, lint OK |
| **Documentation technique** | README, API docs | Suffisante pour maintenance |
| **Environnement de recette** | URL de test | Accessible, données de test |
| **Rapport de tests** | Couverture, résultats | Seuils atteints |

```yaml
livrable_production:
  code:
    niveau_minimal:
      couverture_tests: 40%
      lint_errors: 0
      documentation: inline_comments
    niveau_standard:
      couverture_tests: 70%
      lint_errors: 0
      lint_warnings: < 10
      documentation: readme_complet
    niveau_premium:
      couverture_tests: 85%
      mutation_score: > 60%
      lint_clean: true
      documentation: complète

  environnement_recette:
    obligatoire:
      - url_accessible
      - donnees_test
      - credentials_client
    optionnel:
      - reset_donnees
      - logs_accessibles
```

### Phase LIVRAISON

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **Application en production** | Déployée et fonctionnelle | Smoke tests OK |
| **Documentation utilisateur** | Guide d'utilisation | Adapté au public cible |
| **PV de recette** | Validation formelle | Signé par le client |
| **Dossier de maintenance** | Runbooks, contacts | Complet et à jour |

```yaml
livrable_livraison:
  production:
    checks_obligatoires:
      - smoke_tests_ok
      - monitoring_actif
      - backups_configures
      - ssl_valide
      - dns_configure

  documentation_utilisateur:
    niveau_minimal:
      - faq_5_questions
    niveau_standard:
      - guide_utilisation
      - tutoriels_video_3
    niveau_premium:
      - formation_complete
      - base_connaissances
      - chatbot_support

  pv_recette:
    contenu:
      - liste_fonctionnalites_validees
      - anomalies_residuelles
      - engagement_correction
    signatures:
      - client
      - chef_projet
```

---

## wf-refonte : Projet de Refonte

### Phase AUDIT

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **Rapport d'audit existant** | État des lieux complet | Objectif, chiffré |
| **Inventaire contenu** | Mapping pages/contenus | Exhaustif |
| **Analyse dette technique** | Points critiques identifiés | Priorisé |
| **Benchmark concurrence** | Comparatif marché | 3-5 concurrents analysés |

```yaml
livrable_audit:
  rapport:
    sections:
      - etat_technique
      - performance_actuelle
      - accessibilite
      - seo
      - securite
    metriques:
      - lighthouse_scores
      - temps_chargement
      - taux_erreur
    recommandations: priorisees

  inventaire:
    contenu:
      - urls_existantes
      - statut_chaque_page
      - decision: garder|modifier|supprimer|fusionner
```

### Phase ANALYSE

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **Gap analysis** | Écarts existant/cible | Quantifié |
| **Plan de migration** | Stratégie de transition | Risques identifiés |
| **Matrice de traçabilité** | Ancien → Nouveau | Complète |

### Phase CONCEPTION

*(Voir wf-creation)*

### Phase MIGRATION

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **Script de migration** | Code de transfert | Testé, réversible |
| **Données migrées** | Contenu transféré | Intégrité vérifiée |
| **Redirections** | Map 301 | SEO préservé |

```yaml
livrable_migration:
  scripts:
    exigences:
      - idempotent
      - logs_detailles
      - dry_run_disponible
      - rollback_possible

  donnees:
    verification:
      - comptage_avant_apres
      - controle_integrite
      - validation_metier

  redirections:
    format: csv | htaccess | nginx
    contenu:
      - url_source
      - url_cible
      - code_http: 301
    verification: test_automatise
```

### Phase BASCULE

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **Checklist go-live** | Vérifications pré-bascule | 100% validé |
| **Plan de rollback** | Procédure de retour arrière | Testé |
| **Communication** | Annonce aux utilisateurs | Envoyée |

---

## wf-evolution : Projet d'Évolution

### Phase DEMANDE

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **Ticket de demande** | Description du besoin | Clair, contextualisé |
| **Impact assessment** | Analyse d'impact | Risques identifiés |
| **Estimation** | Charge de travail | Validée |

```yaml
livrable_demande:
  ticket:
    champs_obligatoires:
      - titre
      - description_besoin
      - valeur_business
      - criteres_acceptation
      - priorite
    champs_optionnels:
      - maquettes
      - specs_techniques
```

### Phase SPEC

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **User stories** | Fonctionnalités décrites | Format Given/When/Then |
| **Critères d'acceptation** | Conditions de validation | Testables |
| **Design (si UI)** | Maquettes modifications | Cohérent avec existant |

### Phase RÉALISATION

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **Code** | Fonctionnalité implémentée | PR approuvée |
| **Tests** | Couverture du changement | Non régression |
| **Documentation** | Mise à jour docs | Changelog |

### Phase DÉPLOIEMENT

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **Release notes** | Description changements | Claire pour utilisateurs |
| **Déploiement** | Mise en production | Zero downtime |
| **Validation** | Confirmation fonctionnement | Smoke tests OK |

---

## wf-audit : Mission d'Audit

### Phase CADRAGE

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **Périmètre d'audit** | Scope défini | Validé par client |
| **Grille d'évaluation** | Critères et métriques | Objectifs mesurables |
| **Planning audit** | Dates et accès requis | Confirmés |

```yaml
livrable_cadrage:
  perimetre:
    inclus:
      - composants_audites
      - environnements
      - periode
    exclus:
      - hors_scope explicite

  grille:
    categories:
      - nom_categorie
      - criteres[]
      - poids
      - seuils_acceptation
```

### Phase COLLECTE

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **Données brutes** | Métriques collectées | Horodatées, sourcées |
| **Screenshots/preuves** | Captures d'écran | Annotées |
| **Logs d'outils** | Rapports automatisés | Complets |

### Phase ANALYSE

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **Synthèse par critère** | Évaluation détaillée | Factuelle, sourcée |
| **Score global** | Note agrégée | Méthodologie expliquée |
| **Points critiques** | Problèmes majeurs | Priorisés |

### Phase RESTITUTION

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **Rapport d'audit** | Document complet | Executive summary inclus |
| **Présentation** | Support de restitution | Vulgarisé |
| **Plan de remédiation** | Actions recommandées | Chiffrées, priorisées |

```yaml
livrable_restitution:
  rapport:
    format: pdf | markdown
    sections:
      - executive_summary (1 page max)
      - methodologie
      - resultats_detailles
      - recommandations
      - annexes_techniques

  plan_remediation:
    par_action:
      - description
      - priorite: critique|haute|moyenne|basse
      - effort: jours
      - impact: score_amelioration
      - prerequis
```

---

## wf-support : Ticket Support

### Phase RÉCEPTION

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **Ticket créé** | Demande enregistrée | Numéro attribué |
| **Accusé réception** | Confirmation client | Délai < 1h (SLA) |
| **Catégorisation** | Type et priorité | Automatique ou manuel |

```yaml
livrable_reception:
  ticket:
    champs:
      - numero_unique
      - date_creation
      - canal_origine
      - description
      - pieces_jointes
    categorisation:
      type: incident|demande|question
      priorite: critique|haute|normale|basse
      composant: affected_system
```

### Phase DIAGNOSTIC

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **Analyse cause** | Origine identifiée | Documentée |
| **Estimation résolution** | Temps prévu | Communiqué au client |
| **Escalade (si besoin)** | Transfert niveau 2/3 | Justifié |

### Phase RÉSOLUTION

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **Correction appliquée** | Fix déployé | Testé |
| **Communication client** | Explication solution | Compréhensible |
| **Documentation** | KB mise à jour (si récurrent) | Réutilisable |

### Phase CLÔTURE

| Livrable | Description | Critères d'Acceptation |
|----------|-------------|------------------------|
| **Ticket fermé** | Statut résolu | Accord client |
| **Enquête satisfaction** | NPS/CSAT | Envoyée |
| **Analyse récurrence** | Pattern identifié | Action préventive si > 3 occurrences |

```yaml
livrable_cloture:
  ticket:
    statut: resolu
    resolution:
      - description_solution
      - temps_resolution
      - cause_racine
    satisfaction:
      enquete_envoyee: true
      score: null  # rempli après réponse
```

---

## Matrice Livrables × Positionnement

| Livrable | Startup MVP | Enterprise | Urgence Marché |
|----------|-------------|------------|----------------|
| Documentation | Minimal | Complète | Essentielle |
| Tests | Critiques | Pyramide complète | Automatisés |
| Revue code | Auto | Manuelle | Rapide |
| Accessibilité | A | AA | AA |
| Performance | Acceptable | Optimale | Optimale |
| Sécurité | Top 10 | Audit complet | OWASP complet |
| Maquettes | Wireframes | HD + DS | HD |
| Formation | FAQ | Complète | Guide rapide |
