# Critères d'Acceptation par Livrable

> Chaque livrable doit satisfaire des critères mesurables pour être considéré comme accepté.

---

## Structure d'un Critère d'Acceptation

```yaml
critere:
  id: "CA-XXX-000"
  categorie: fonctionnel|technique|qualite|documentation
  description: "Description claire et mesurable"
  verification:
    methode: automatique|manuelle|mixte
    outil: "Outil ou processus de vérification"
    responsable: client|agence|tiers
  seuil:
    minimal: "Valeur minimale acceptable"
    standard: "Valeur cible"
    premium: "Valeur excellence"
  preuve: "Type de preuve à fournir"
```

---

## Critères par Type de Livrable

### CODE SOURCE

#### CA-CODE-001 : Qualité du Code
```yaml
critere:
  id: "CA-CODE-001"
  description: "Le code respecte les standards de qualité définis"
  verification:
    methode: automatique
    outil: ESLint/Prettier/SonarQube
  seuil:
    minimal:
      erreurs_lint: 0
      warnings_lint: < 50
    standard:
      erreurs_lint: 0
      warnings_lint: < 10
      code_smells: < 20
    premium:
      lint_clean: true
      code_smells: 0
      duplication: < 3%
  preuve: Rapport SonarQube
```

#### CA-CODE-002 : Couverture de Tests
```yaml
critere:
  id: "CA-CODE-002"
  description: "Le code est couvert par des tests automatisés"
  verification:
    methode: automatique
    outil: Jest/Vitest + Coverage
  seuil:
    minimal:
      coverage_global: 40%
      coverage_critiques: 80%
    standard:
      coverage_global: 70%
      coverage_branches: 60%
    premium:
      coverage_global: 85%
      coverage_branches: 80%
      mutation_score: 60%
  preuve: Rapport de couverture
```

#### CA-CODE-003 : Sécurité du Code
```yaml
critere:
  id: "CA-CODE-003"
  description: "Aucune vulnérabilité connue dans le code et les dépendances"
  verification:
    methode: automatique
    outil: npm audit / Snyk / OWASP Dependency-Check
  seuil:
    minimal:
      vulnerabilites_critiques: 0
      vulnerabilites_hautes: < 5
    standard:
      vulnerabilites_critiques: 0
      vulnerabilites_hautes: 0
      vulnerabilites_moyennes: < 10
    premium:
      vulnerabilites: 0
      audit_externe: passé
  preuve: Rapport d'audit sécurité
```

#### CA-CODE-004 : Maintenabilité
```yaml
critere:
  id: "CA-CODE-004"
  description: "Le code est maintenable et compréhensible"
  verification:
    methode: mixte
    outil: SonarQube + Code Review
  seuil:
    minimal:
      complexite_cyclomatique_max: 20
      fichiers_longs: < 10% (>500 lignes)
    standard:
      complexite_cyclomatique_max: 15
      fichiers_longs: < 5%
      fonctions_longues: < 5% (>50 lignes)
    premium:
      complexite_cyclomatique_max: 10
      dette_technique: < 2h
  preuve: Rapport SonarQube + PV revue code
```

---

### PERFORMANCE

#### CA-PERF-001 : Core Web Vitals
```yaml
critere:
  id: "CA-PERF-001"
  description: "Les Core Web Vitals sont dans les seuils acceptables"
  verification:
    methode: automatique
    outil: Lighthouse / PageSpeed Insights
  seuil:
    minimal:  # "Needs Improvement"
      LCP: < 4s
      FID: < 300ms
      CLS: < 0.25
    standard:  # "Good"
      LCP: < 2.5s
      FID: < 100ms
      CLS: < 0.1
    premium:  # Top 10%
      LCP: < 1.5s
      FID: < 50ms
      CLS: < 0.05
  preuve: Rapport Lighthouse (moyenne 5 runs)
```

#### CA-PERF-002 : Temps de Chargement
```yaml
critere:
  id: "CA-PERF-002"
  description: "Le temps de chargement est acceptable"
  verification:
    methode: automatique
    outil: WebPageTest / Lighthouse
  seuil:
    minimal:
      ttfb: < 800ms
      fcp: < 3s
      tti: < 7s
    standard:
      ttfb: < 400ms
      fcp: < 1.8s
      tti: < 4s
    premium:
      ttfb: < 200ms
      fcp: < 1s
      tti: < 2.5s
  preuve: Rapport WebPageTest
```

#### CA-PERF-003 : Bundle Size
```yaml
critere:
  id: "CA-PERF-003"
  description: "La taille des bundles est optimisée"
  verification:
    methode: automatique
    outil: webpack-bundle-analyzer / source-map-explorer
  seuil:
    minimal:
      js_initial: < 500KB
      css_initial: < 150KB
    standard:
      js_initial: < 250KB
      css_initial: < 75KB
      code_splitting: actif
    premium:
      js_initial: < 150KB
      css_initial: < 50KB
      tree_shaking: optimal
  preuve: Rapport bundle analyzer
```

---

### ACCESSIBILITÉ

#### CA-A11Y-001 : Conformité WCAG
```yaml
critere:
  id: "CA-A11Y-001"
  description: "Le site est conforme aux standards WCAG"
  verification:
    methode: mixte
    outil: axe-core / WAVE + audit manuel
  seuil:
    minimal:  # WCAG 2.1 A
      erreurs_A: 0
      audit_manuel: non requis
    standard:  # WCAG 2.1 AA
      erreurs_A: 0
      erreurs_AA: 0
      audit_manuel: parcours critiques
    premium:  # WCAG 2.1 AAA
      erreurs_A: 0
      erreurs_AA: 0
      erreurs_AAA: < 5
      audit_expert: complet
  preuve: Rapport axe + audit manuel si applicable
```

#### CA-A11Y-002 : Navigation Clavier
```yaml
critere:
  id: "CA-A11Y-002"
  description: "Toutes les fonctionnalités sont accessibles au clavier"
  verification:
    methode: manuelle
    outil: Test manuel + checklist
  seuil:
    minimal:
      focus_visible: toujours
      ordre_focus: logique
    standard:
      skip_links: présents
      raccourcis: documentés
    premium:
      roving_tabindex: si applicable
      focus_trap: modales
  preuve: PV de test accessibilité
```

#### CA-A11Y-003 : Lecteurs d'Écran
```yaml
critere:
  id: "CA-A11Y-003"
  description: "Le contenu est compréhensible via lecteur d'écran"
  verification:
    methode: manuelle
    outil: NVDA / VoiceOver
  seuil:
    minimal:
      aria_labels: éléments interactifs
      alt_images: toutes images informatives
    standard:
      landmarks: structure claire
      live_regions: notifications
    premium:
      test_utilisateur: avec personne handicapée
  preuve: Rapport de test lecteur d'écran
```

---

### DOCUMENTATION

#### CA-DOC-001 : README
```yaml
critere:
  id: "CA-DOC-001"
  description: "Le README permet de démarrer rapidement"
  verification:
    methode: manuelle
    outil: Checklist
  seuil:
    minimal:
      sections:
        - description_projet
        - installation
        - lancement
    standard:
      sections:
        - description_projet
        - prerequis
        - installation
        - configuration
        - lancement
        - tests
        - contribution
    premium:
      sections: toutes_standard
      badges: CI/coverage/version
      screenshots: si applicable
  preuve: Fichier README.md
```

#### CA-DOC-002 : Documentation API
```yaml
critere:
  id: "CA-DOC-002"
  description: "Les APIs sont documentées et exploitables"
  verification:
    methode: automatique
    outil: OpenAPI / Swagger
  seuil:
    minimal:
      endpoints: listés
      parametres: documentés
    standard:
      format: OpenAPI 3.0+
      exemples: requête/réponse
      erreurs: documentées
    premium:
      playground: interactif
      sdk: généré
      versioning: documenté
  preuve: Fichier OpenAPI + UI Swagger
```

#### CA-DOC-003 : Documentation Utilisateur
```yaml
critere:
  id: "CA-DOC-003"
  description: "Les utilisateurs peuvent utiliser l'application de manière autonome"
  verification:
    methode: manuelle
    outil: Test utilisateur
  seuil:
    minimal:
      format: FAQ (10 questions)
    standard:
      format: Guide utilisateur
      couverture: fonctionnalités principales
      screenshots: annotés
    premium:
      format: Base de connaissances
      tutoriels_video: parcours clés
      recherche: disponible
  preuve: Documentation publiée
```

---

### SÉCURITÉ

#### CA-SEC-001 : OWASP Top 10
```yaml
critere:
  id: "CA-SEC-001"
  description: "L'application est protégée contre les vulnérabilités OWASP Top 10"
  verification:
    methode: mixte
    outil: OWASP ZAP / Burp Suite
  seuil:
    minimal:
      injection: protégé
      auth_broken: protégé
      xss: protégé
    standard:
      owasp_top_10: tous protégés
      headers_security: configurés
    premium:
      pentest: externe passé
      bug_bounty: optionnel
  preuve: Rapport scan sécurité
```

#### CA-SEC-002 : Headers HTTP
```yaml
critere:
  id: "CA-SEC-002"
  description: "Les headers de sécurité HTTP sont configurés"
  verification:
    methode: automatique
    outil: securityheaders.com / Mozilla Observatory
  seuil:
    minimal:
      score: D+
      headers:
        - X-Content-Type-Options
        - X-Frame-Options
    standard:
      score: B+
      headers:
        - tous_minimal
        - Content-Security-Policy
        - Strict-Transport-Security
    premium:
      score: A+
      csp: strict
      hsts: preload
  preuve: Rapport securityheaders.com
```

#### CA-SEC-003 : RGPD
```yaml
critere:
  id: "CA-SEC-003"
  description: "L'application est conforme au RGPD"
  verification:
    methode: mixte
    outil: Checklist CNIL + audit
  seuil:
    minimal:
      mentions_legales: présentes
      politique_confidentialite: présente
      consentement_cookies: basique
    standard:
      registre_traitements: documenté
      dpo: désigné si requis
      consentement: granulaire
      droits_utilisateurs: exercables
    premium:
      pia: réalisée
      audit_externe: passé
  preuve: Documents RGPD + PV audit
```

---

## Processus de Validation

### 1. Préparation
```yaml
preparation:
  - identifier_livrables
  - selectionner_criteres_applicables
  - definir_niveau_exigence  # selon positionnement client
  - planifier_verifications
```

### 2. Vérification
```yaml
verification:
  - executer_tests_automatiques
  - realiser_verifications_manuelles
  - collecter_preuves
  - documenter_resultats
```

### 3. Décision
```yaml
decision:
  tous_criteres_ok:
    action: valider_livrable
  criteres_bloquants_ko:
    action: rejeter_livrable
    suivi: plan_correction
  criteres_mineurs_ko:
    action: accepter_avec_reserves
    suivi: plan_amelioration
```

### 4. Documentation
```yaml
documentation:
  pv_recette:
    - liste_criteres_evalues
    - resultats_par_critere
    - preuves_collectees
    - decision_finale
    - signatures
```

---

## Exemple PV de Recette

```markdown
# Procès-Verbal de Recette

**Projet** : [Nom du projet]
**Livrable** : [Nom du livrable]
**Date** : [Date]
**Version** : [Version]

## Critères Évalués

| ID | Critère | Niveau Exigé | Résultat | Statut |
|----|---------|--------------|----------|--------|
| CA-CODE-001 | Qualité code | Standard | 0 erreurs, 5 warnings | ✅ OK |
| CA-CODE-002 | Couverture tests | Standard | 72% global | ✅ OK |
| CA-PERF-001 | Core Web Vitals | Standard | LCP 2.1s | ✅ OK |
| CA-A11Y-001 | WCAG | Standard | 0 erreurs AA | ✅ OK |

## Preuves Fournies
- [ ] Rapport SonarQube
- [ ] Rapport de couverture
- [ ] Rapport Lighthouse
- [ ] Rapport axe-core

## Décision
- [ ] ✅ Livrable ACCEPTÉ
- [ ] ⚠️ Accepté avec réserves
- [ ] ❌ Livrable REFUSÉ

## Réserves (si applicable)
_[Liste des points à améliorer]_

## Signatures

| Rôle | Nom | Signature | Date |
|------|-----|-----------|------|
| Client | | | |
| Chef de projet | | | |
| Tech Lead | | | |
```
