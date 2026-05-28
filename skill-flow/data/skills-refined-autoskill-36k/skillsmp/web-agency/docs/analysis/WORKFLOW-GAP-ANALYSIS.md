# Analyse des Trous - Workflows Manquants

## Date: 2024-12-28

## Constat

### Statistiques Globales

| Indicateur | Valeur |
|------------|--------|
| **Total agents** | 690 |
| **Agents avec workflows** | 3 (0.43%) |
| **Agents sans workflows** | 687 (99.57%) |
| **Orchestrators** (pas besoin) | ~13 |
| **Templates** (pas besoin) | ~3 |
| **TROUS REELS** | **~671 agents** |

### Agents avec Workflows (3)

| Skill | Agent | Workflows |
|-------|-------|-----------|
| ux-ui-design | direction-artistique | 2 (nouveau-projet, refonte) |
| ux-ui-design | brand-identity | 2 (creation, refonte) |
| marketing | ligne-editoriale | 2 (creation, audit) |

---

## Catégorisation par Priorité

### Priorité 1 - Coeur Métier Agence (196 agents)

Ces skills représentent les activités client-facing principales.

| Skill | Agents | Importance |
|-------|--------|------------|
| project-management | 29 | Gestion projet, relation client |
| commercial-crm | 18 | Acquisition, conversion |
| ux-ui-design | 27 | Conception utilisateur |
| marketing | 117 | Stratégie, contenu, acquisition |
| client-intake | 5 | Point d'entrée client |

**Patterns de workflows typiques:**
- Nouveau projet / Refonte / Evolution
- Audit / Diagnostic / Recommandation
- Creation / Validation / Livraison

### Priorité 2 - Process Core (89 agents)

Ces skills définissent le "comment travailler".

| Skill | Agents | Importance |
|-------|--------|------------|
| web-dev-process | 64 | 7 phases projet |
| testing-process | 25 | Stratégie qualité |

**Patterns de workflows typiques:**
- Phase initiale → Phase finale
- Audit → Remediation → Validation

### Priorité 3 - Implementation Technique (206 agents)

Ces skills implémentent le code.

| Skill | Agents | Importance |
|-------|--------|------------|
| frontend-developer | 33 | HTML/CSS/JS |
| backend-developer | 38 | API/DB |
| react-expert | 28 | React patterns |
| nextjs-expert | 35 | Next.js apps |
| wordpress-gutenberg-expert | 42 | WordPress/Gutenberg |
| devops | 30 | CI/CD, infrastructure |

**Patterns de workflows typiques:**
- Creation / Migration / Optimisation
- Debug / Fix / Refactor
- Setup → Config → Deploy

### Priorité 4 - Support Functions (97 agents)

Ces skills supportent l'activité.

| Skill | Agents | Importance |
|-------|--------|------------|
| direction-technique | 59 | Stratégie technique |
| finance-analytics | 17 | KPIs, facturation |
| legal-compliance | 16 | RGPD, CGV |
| support-client | 16 | Tickets, FAQ |
| lead-dev | 27 | Code review, coordination |
| task-orchestrator | 20 | Routage tâches |
| design-system-foundations | 21 | Tokens, composants |

---

## Plan de Comblement

### Phase 1 - Templates de Workflows (1 semaine)

Créer 5 templates de workflows réutilisables:

1. **workflow-creation.template.md**
   - Nouveau projet, création from scratch
   - Phases: Brief → Conception → Production → Livraison

2. **workflow-refonte.template.md**
   - Refonte existant
   - Phases: Audit → Analyse → Migration → Validation

3. **workflow-evolution.template.md**
   - Évolution/amélioration
   - Phases: Demande → Spec → Dev → Test → Deploy

4. **workflow-audit.template.md**
   - Diagnostic/analyse
   - Phases: Collecte → Analyse → Rapport → Recommandations

5. **workflow-support.template.md**
   - Ticket/incident
   - Phases: Reception → Diagnostic → Resolution → Clôture

### Phase 2 - Skills Priorité 1 (2-3 semaines)

| Skill | Agents à traiter | Effort estimé |
|-------|-----------------|---------------|
| project-management | 29 | 3 jours |
| commercial-crm | 18 | 2 jours |
| ux-ui-design | 25 restants | 3 jours |
| marketing | 116 restants | 5 jours |
| client-intake | 5 | 1 jour |

### Phase 3 - Skills Priorité 2 (1-2 semaines)

| Skill | Agents à traiter | Effort estimé |
|-------|-----------------|---------------|
| web-dev-process | 64 | 4 jours |
| testing-process | 25 | 2 jours |

### Phase 4 - Skills Priorité 3 (3-4 semaines)

| Skill | Agents à traiter | Effort estimé |
|-------|-----------------|---------------|
| frontend-developer | 33 | 2 jours |
| backend-developer | 38 | 2 jours |
| react-expert | 28 | 2 jours |
| nextjs-expert | 35 | 2 jours |
| wordpress-gutenberg-expert | 42 | 3 jours |
| devops | 30 | 2 jours |

### Phase 5 - Skills Priorité 4 (2 semaines)

Compléter les skills support restants.

---

## Architecture Cible

### Vision Utilisateur

> "Chaque skills, workflow, roles sont indépendants de tout système d'IA.
> Le dossier .web-agency/ contient les instructions agnostiques (skills, learnings).
> Le dossier .claude/commands/ contient uniquement les points d'entrée spécifiques à Claude,
> qui référencent les skills dans .web-agency/ sans duplication."

### Structure Proposée

```
/agency/                          # Racine indépendante
├── roles/                        # Définitions des rôles
│   ├── ux-designer.md
│   ├── developer.md
│   └── ...
├── workflows/                    # Workflows réutilisables
│   ├── templates/
│   │   ├── creation.md
│   │   ├── refonte.md
│   │   └── audit.md
│   └── instances/
│       ├── ux/
│       ├── dev/
│       └── ...
├── skills/                       # Skills techniques
│   ├── ux-ui-design/
│   ├── frontend-developer/
│   └── ...
└── .web-agency/                  # Instructions agnostiques
    ├── skills/                   # Skills métier
    ├── learnings/                # Learning loop
    └── workflows/                # Workflows réutilisables
```

### Mapping Rôle → Workflows

Chaque rôle référence ses workflows associés:

```yaml
# roles/ux-designer.md
---
name: UX Designer
workflows:
  - ../workflows/templates/creation.md
  - ../workflows/templates/refonte.md
  - ../workflows/templates/audit.md
skills:
  - ux-ui-design
  - design-system-foundations
---
```

---

## Métriques de Succès

| Métrique | Baseline | Cible Phase 1 | Cible Final |
|----------|----------|---------------|-------------|
| Couverture workflows | 0.43% | 10% | 80% |
| Skills avec 100% | 0 | 2 | 15+ |
| Agents sans workflow | 671 | 600 | <100 |
| Templates disponibles | 0 | 5 | 10 |

---

## Prochaines Actions

1. [ ] Créer les 5 templates de workflows (Phase 1)
2. [ ] Choisir 1 skill Priorité 1 comme pilote
3. [ ] Appliquer les templates au skill pilote
4. [ ] Valider l'approche avant industrialisation
5. [ ] Documenter le process dans un ADR

---

## Références

- [ADR-001: Single Responsibility Agents](../adr/001-single-responsibility-agents.md)
- [ADR-003: Markdown Agent Format](../adr/003-markdown-agent-format.md)
- [ADR-006: Learning Loop System](../adr/006-learning-loop-system.md)
