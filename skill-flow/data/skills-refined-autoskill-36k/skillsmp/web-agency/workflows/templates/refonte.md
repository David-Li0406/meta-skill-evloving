---
id: wf-refonte
name: Workflow Refonte
type: template
version: 1.1.0
description: Workflow pour la refonte d'un existant
duration_range: "8-20 jours"
phases: 5
applicable_to:
  - refonte-site
  - refonte-identite
  - migration
  - modernisation
references:
  - acceptance/matrice-positionnement.md
  - acceptance/livrables-par-workflow.md
  - acceptance/criteres-acceptation.md
---

# Workflow Refonte

> Template pour tout projet de refonte ou migration d'existant.

## Vue d'Ensemble

```
AUDIT → ANALYSE → CONCEPTION → MIGRATION → BASCULE
```

| Phase | Durée | Validation |
|-------|-------|------------|
| Audit | 15-20% | Rapport d'audit |
| Analyse | 10-15% | Décisions validées |
| Conception | 20-25% | Nouvelle version specs |
| Migration | 35-40% | Recette OK |
| Bascule | 10-15% | Production live |

---

## Phase 1: Audit

### Objectif
Comprendre l'existant et identifier les problèmes.

### Activités
1. Inventaire de l'existant
2. Analyse technique (dette, performance)
3. Analyse fonctionnelle (usages, pain points)
4. Interviews stakeholders

### Livrables et Critères d'Acceptation

| Livrable | Critères d'Acceptation | Niveau |
|----------|------------------------|--------|
| **Rapport audit existant** | Analyse complète technique et fonctionnelle | Tous |
| **Inventaire contenu** | Liste exhaustive des assets et contenus | Tous |
| **Dette technique** | Identification et priorisation des problèmes | Tous |
| **Interviews stakeholders** | Comptes-rendus avec pain points identifiés | Tous |

```yaml
livrables_audit:
  rapport_audit_existant:
    criteres:
      - CA-AUD-001: "Analyse technique complète (performance, sécurité, code)"
      - CA-AUD-002: "Analyse fonctionnelle (usages, parcours)"
      - CA-AUD-003: "Identification des pain points"
      - CA-AUD-004: "Benchmark concurrentiel si pertinent"
    preuve: "Document d'audit signé"

  inventaire_contenu:
    criteres:
      - CA-AUD-010: "Liste exhaustive des pages/fonctionnalités"
      - CA-AUD-011: "Cartographie des contenus (textes, médias)"
      - CA-AUD-012: "Identification des contenus à migrer/supprimer"
      - CA-AUD-013: "Mapping des URLs existantes"
    preuve: "Spreadsheet inventaire"

  dette_technique:
    criteres:
      - CA-AUD-020: "Liste des problèmes techniques priorisés"
      - CA-AUD-021: "Estimation effort de correction"
      - CA-AUD-022: "Risques identifiés et évalués"
      - CA-AUD-023: "Dépendances obsolètes listées"
    preuve: "Rapport dette technique"
```

### Critères de Sortie
- Vision claire de l'existant
- Problèmes identifiés et priorisés
- Inventaire complet validé

---

## Phase 2: Analyse

### Objectif
Définir la stratégie de refonte.

### Activités
1. Définir ce qu'on garde/jette/améliore
2. Identifier les risques de migration
3. Proposer les options de refonte
4. Chiffrer et planifier

### Livrables et Critères d'Acceptation

| Livrable | Critères d'Acceptation | Niveau |
|----------|------------------------|--------|
| **Gap analysis** | Écart existant vs cible documenté | Tous |
| **Plan de migration** | Stratégie et étapes détaillées | Tous |
| **Matrice de traçabilité** | Mapping ancien vers nouveau système | Tous |
| **Analyse des risques** | Risques identifiés avec mitigation | Tous |

```yaml
livrables_analyse:
  gap_analysis:
    criteres:
      - CA-ANAL-001: "État actuel documenté (as-is)"
      - CA-ANAL-002: "État cible défini (to-be)"
      - CA-ANAL-003: "Écarts identifiés et priorisés"
      - CA-ANAL-004: "Effort de comblement estimé"
    preuve: "Document gap analysis"

  plan_migration:
    criteres:
      - CA-ANAL-010: "Stratégie migration choisie (big bang/progressive)"
      - CA-ANAL-011: "Phases et jalons définis"
      - CA-ANAL-012: "Dépendances identifiées"
      - CA-ANAL-013: "Plan de rollback prévu"
    preuve: "Plan de migration validé"

  matrice_tracabilite:
    criteres:
      - CA-ANAL-020: "Mapping fonctionnalités ancien/nouveau"
      - CA-ANAL-021: "Mapping contenus ancien/nouveau"
      - CA-ANAL-022: "Mapping URLs (redirections)"
      - CA-ANAL-023: "Couverture 100% de l'existant"
    preuve: "Matrice traçabilité complète"

  analyse_risques:
    criteres:
      - CA-ANAL-030: "Risques techniques identifiés"
      - CA-ANAL-031: "Risques business évalués"
      - CA-ANAL-032: "Plans de mitigation définis"
      - CA-ANAL-033: "Critères de rollback établis"
    preuve: "Registre des risques"
```

### Critères de Sortie
- Stratégie validée par le client
- Risques acceptés et mitigés
- Matrice de traçabilité complète

---

## Phase 3: Conception

### Objectif
Concevoir la nouvelle version.

### Activités
1. Spécifications de la cible
2. Plan de migration des données
3. Mapping ancien → nouveau
4. Design de la nouvelle version

### Livrables et Critères d'Acceptation (selon positionnement)

| Livrable | Minimal | Standard | Premium |
|----------|---------|----------|---------|
| **Maquettes** | Wireframes | HD responsive | Pixel-perfect + DS |
| **Specs techniques** | Schéma archi | C4 + OpenAPI | + POC technique |
| **Prototype** | - | Cliquable | Interactif animé |
| **ADR** | - | Choix majeurs | Complet |

```yaml
livrables_conception:
  maquettes:
    niveau_minimal:
      criteres:
        - CA-CONC-001: "Wireframes pages principales"
        - CA-CONC-002: "1 résolution cible"
      preuve: "Fichiers Figma/Sketch"
    niveau_standard:
      criteres:
        - CA-CONC-001: "Maquettes HD toutes pages"
        - CA-CONC-002: "3 breakpoints (mobile/tablet/desktop)"
        - CA-CONC-003: "Design system tokens définis"
      preuve: "Fichiers Figma + DS"
    niveau_premium:
      criteres:
        - CA-CONC-001: "Maquettes pixel-perfect"
        - CA-CONC-002: "5 breakpoints"
        - CA-CONC-003: "Design system complet"
        - CA-CONC-004: "Micro-interactions spécifiées"
      preuve: "Fichiers Figma + DS + prototypes"

  specifications:
    niveau_minimal:
      criteres:
        - CA-CONC-010: "Schéma architecture global"
        - CA-CONC-011: "Liste des endpoints"
      preuve: "Document technique"
    niveau_standard:
      criteres:
        - CA-CONC-010: "Diagrammes C4 (context, container)"
        - CA-CONC-011: "Specs API OpenAPI 3.0"
        - CA-CONC-012: "Modèle de données"
      preuve: "Specs + OpenAPI"
    niveau_premium:
      criteres:
        - CA-CONC-010: "C4 complet (+ component)"
        - CA-CONC-011: "OpenAPI + exemples"
        - CA-CONC-012: "Modèle données + migrations"
        - CA-CONC-013: "POC technique validé"
      preuve: "Specs + POC fonctionnel"
```

### Critères de Sortie
- Cible clairement définie
- Plan de migration validé
- Conception validée selon niveau positionné

---

## Phase 4: Migration

### Objectif
Réaliser la migration et la nouvelle version.

### Activités
1. Setup environnement cible
2. Migration des données
3. Développement/adaptation
4. Tests de non-régression
5. Recette sur environnement parallèle

### Livrables et Critères d'Acceptation (selon positionnement)

| Livrable | Minimal | Standard | Premium |
|----------|---------|----------|---------|
| **Scripts migration** | Scripts manuels | Automatisés | + Rollback auto |
| **Données migrées** | Vérification manuelle | Validation auto | + Audit trail |
| **Redirections** | Liste 301 | + Tests auto | + Monitoring SEO |
| **Tests** | Smoke tests | Tests complets | + Tests charge |

```yaml
livrables_migration:
  scripts_migration:
    niveau_minimal:
      criteres:
        - CA-MIG-001: "Scripts migration documentés"
        - CA-MIG-002: "Exécution manuelle possible"
      preuve: "Scripts + documentation"
    niveau_standard:
      criteres:
        - CA-MIG-001: "Scripts automatisés et testés"
        - CA-MIG-002: "Logs d'exécution"
        - CA-MIG-003: "Reprise sur erreur"
      preuve: "Scripts + logs + tests"
    niveau_premium:
      criteres:
        - CA-MIG-001: "Pipeline migration CI/CD"
        - CA-MIG-002: "Rollback automatique"
        - CA-MIG-003: "Validation données intégrée"
        - CA-MIG-004: "Monitoring migration"
      preuve: "Pipeline + dashboards"

  donnees_migrees:
    niveau_minimal:
      criteres:
        - CA-MIG-010: "Données migrées sans perte"
        - CA-MIG-011: "Vérification par échantillonnage"
      preuve: "Rapport vérification"
    niveau_standard:
      criteres:
        - CA-MIG-010: "Validation automatique 100% données"
        - CA-MIG-011: "Intégrité référentielle vérifiée"
        - CA-MIG-012: "Comparaison source/cible"
      preuve: "Rapports validation"
    niveau_premium:
      criteres:
        - CA-MIG-010: "Audit trail complet"
        - CA-MIG-011: "Traçabilité chaque enregistrement"
        - CA-MIG-012: "Réconciliation automatique"
        - CA-MIG-013: "Rapport anomalies traité"
      preuve: "Audit trail + rapports"

  redirections:
    niveau_minimal:
      criteres:
        - CA-MIG-020: "Liste redirections 301 complète"
        - CA-MIG-021: "Fichier .htaccess ou équivalent"
      preuve: "Fichier redirections"
    niveau_standard:
      criteres:
        - CA-MIG-020: "Redirections testées automatiquement"
        - CA-MIG-021: "0 erreur 404 sur URLs principales"
        - CA-MIG-022: "Sitemap mis à jour"
      preuve: "Rapport tests + sitemap"
    niveau_premium:
      criteres:
        - CA-MIG-020: "Monitoring SEO configuré"
        - CA-MIG-021: "Alertes perte de trafic"
        - CA-MIG-022: "Suivi positions clés"
        - CA-MIG-023: "Plan réaction SEO"
      preuve: "Dashboard SEO + alertes"
```

### Critères de Sortie
- Nouvelle version testée
- Données migrées et vérifiées
- Parité fonctionnelle confirmée
- Redirections en place

---

## Phase 5: Bascule

### Objectif
Basculer en production sans interruption.

### Activités
1. Plan de bascule détaillé
2. Communication aux utilisateurs
3. Bascule (big bang ou progressive)
4. Monitoring post-bascule
5. Rollback si nécessaire

### Livrables et Critères d'Acceptation

| Livrable | Critères d'Acceptation | Niveau |
|----------|------------------------|--------|
| **Checklist go-live** | Tous points vérifiés et validés | Tous |
| **Plan de rollback** | Procédure testée et documentée | Tous |
| **Communication** | Utilisateurs informés avant/après | Tous |
| **PV mise en production** | Signature client et équipe | Tous |

```yaml
livrables_bascule:
  checklist_golive:
    criteres:
      - CA-BAS-001: "DNS prêt à basculer"
      - CA-BAS-002: "SSL/TLS configuré et testé"
      - CA-BAS-003: "Backups effectués"
      - CA-BAS-004: "Monitoring opérationnel"
      - CA-BAS-005: "Équipe de garde identifiée"
      - CA-BAS-006: "Smoke tests prêts"
    preuve: "Checklist signée"

  plan_rollback:
    criteres:
      - CA-BAS-010: "Procédure rollback documentée"
      - CA-BAS-011: "Critères de déclenchement définis"
      - CA-BAS-012: "Temps de rollback estimé < 30min"
      - CA-BAS-013: "Test rollback effectué"
      - CA-BAS-014: "Responsable rollback identifié"
    preuve: "Document rollback testé"

  communication:
    criteres:
      - CA-BAS-020: "Communication pré-bascule envoyée"
      - CA-BAS-021: "Date et durée annoncées"
      - CA-BAS-022: "Communication post-bascule préparée"
      - CA-BAS-023: "Canal support communiqué"
    preuve: "Emails/communications"

  pv_mise_en_production:
    criteres:
      - CA-BAS-030: "Smoke tests passés"
      - CA-BAS-031: "Fonctionnalités critiques validées"
      - CA-BAS-032: "Performance acceptable"
      - CA-BAS-033: "Signatures obtenues"
    preuve: "PV signé"
```

### Critères de Sortie
- Production live et stable
- Ancien système décommissionné
- Support en place
- Client satisfait

---

## Points de Contrôle

| Checkpoint | Timing | Décision |
|------------|--------|----------|
| Go/No-Go Refonte | Fin Phase 2 | Confirmer la refonte |
| Go/No-Go Migration | Fin Phase 3 | Valider le plan |
| Go/No-Go Bascule | Fin Phase 4 | Prêt pour production |

## Rollback

Conditions de rollback:
- Perte de données détectée
- Fonctionnalité critique cassée
- Performance dégradée > 50%

Procédure:
1. Activer le plan de rollback
2. Restaurer l'ancien système
3. Communiquer aux utilisateurs
4. Analyser la cause
5. Replanifier la bascule
