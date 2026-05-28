# Angular Migration Workflow

Complete Angular migration workflow documentation, including skill usage and best practices.

## Skills Classification Overview

| Category | Skills | Purpose |
| -------- | ------ | ------- |
| **Automated Pipeline** | `full-migration-pipeline` | One-click complete migration |
| **Primary Migration Flow** | `migrate-page`, `migrate-page-gitlab` | Execute full migration |
| **Core Reference** | `one-ui-migration`, `migration-patterns` | Migration principles and pattern queries |
| **Quality Assurance** | `migration-lint`, `migration-review` | Code compliance checks |
| **QA Verification** | `generate-qa-test-cases`, `verify-legacy-with-qa-testcases` | Test case generation and verification |
| **Auxiliary Tools** | `form-extraction`, `compare-i18n-keys`, `icon-replacement`, `ui-layout-guide`, `check-barrel-files` | Task-specific assistance |

## Migration Workflow Diagram

```mermaid
flowchart TB
    subgraph Phase1["Phase 1: Analysis"]
        START([Start Migration]) --> MIGRATE["/migrate-page\nor\n/migrate-page-gitlab"]
        MIGRATE --> ANALYSIS["Generate MIGRATION-ANALYSIS.md"]
        ANALYSIS --> FORM_EXT["/form-extraction\nExtract form controls"]
        ANALYSIS --> I18N_EXT["Extract translation keys"]
    end

    subgraph Phase2["Phase 2: Implementation"]
        FORM_EXT --> DOMAIN["Create Domain Layer\n- *.model.ts\n- *.api.ts\n- *.store.ts"]
        I18N_EXT --> DOMAIN
        DOMAIN --> UI["Create UI Layer\n- Tables\n- Forms"]
        UI --> FEATURES["Create Features Layer\n- Page Component\n- Dialogs"]
        FEATURES --> SHELL["Create Shell Layer\n- Routes"]
    end

    subgraph Phase3["Phase 3: Quality Assurance"]
        SHELL --> LINT["/migration-lint\nCompliance check + auto-fix"]
        LINT --> REVIEW["/migration-review\nMigration completeness check"]
        REVIEW --> I18N_CMP["/compare-i18n-keys\nTranslation key comparison"]
        I18N_CMP --> BARREL["/check-barrel-files\nCheck redundant barrels"]
    end

    subgraph Phase4["Phase 4: QA Verification"]
        BARREL --> QA_GEN["/generate-qa-test-cases\nGenerate QA test cases"]
        QA_GEN --> QA_VERIFY["/verify-legacy-with-qa-testcases\nVerify legacy code"]
        QA_VERIFY --> DONE([Migration Complete])
    end

    subgraph Support["Auxiliary Skills (Available Anytime)"]
        PATTERNS["/migration-patterns\nQuery migration patterns"]
        ICONS["/icon-replacement\nIcon replacement"]
        LAYOUT["/ui-layout-guide\nUI layout guidelines"]
    end

    DOMAIN -.->|Query| PATTERNS
    UI -.->|Query| PATTERNS
    UI -.->|Query| ICONS
    UI -.->|Query| LAYOUT
    FEATURES -.->|Query| PATTERNS

    style Phase1 fill:#e1f5fe
    style Phase2 fill:#fff3e0
    style Phase3 fill:#f3e5f5
    style Phase4 fill:#e8f5e9
    style Support fill:#fafafa
```

## Skills Dependency Diagram

```mermaid
graph LR
    subgraph Core["Core Knowledge Base"]
        MIG["one-ui-migration\n(Core Principles)"]
        PAT["migration-patterns\n(Pattern Queries)"]
    end

    subgraph MainFlow["Primary Flow Skills"]
        MP["migrate-page"]
        MG["migrate-page-gitlab"]
    end

    subgraph QualityCheck["Quality Check Skills"]
        LINT["migration-lint"]
        REV["migration-review"]
    end

    subgraph QATools["QA Tool Skills"]
        GEN["generate-qa-test-cases"]
        VER["verify-legacy-with-qa-testcases"]
    end

    subgraph Helpers["Auxiliary Skills"]
        FORM["form-extraction"]
        I18N["compare-i18n-keys"]
        ICON["icon-replacement"]
        UI["ui-layout-guide"]
        BARREL["check-barrel-files"]
    end

    MIG -->|Reference| MP
    MIG -->|Reference| MG
    MIG -->|Reference| LINT
    MIG -->|Reference| REV
    PAT -->|Provides Query| MP
    PAT -->|Provides Query| MG

    FORM -->|Referenced By| REV
    FORM -->|Referenced By| LINT

    GEN -->|Outputs To| VER

    MP --> REV
    MG --> REV
    REV --> LINT
```

## Detailed Phase Descriptions

### Phase 1: Analysis

**Objective:** Understand legacy code structure, generate migration analysis document

| Step | Skill | Output |
| ---- | ----- | ------ |
| 1 | `/migrate-page --from=<source> --to=<target>` | `MIGRATION-ANALYSIS.md` |
| 2 | `/form-extraction` (auxiliary) | Form controls list |

**Output Location:** `{target}/domain/src/lib/docs/MIGRATION-ANALYSIS.md`

### Phase 2: Implementation

**Objective:** Create each layer following DDD architecture

| Layer | Contents | Query Skill |
| ----- | -------- | ----------- |
| Domain | `*.model.ts`, `*.api.ts`, `*.store.ts`, `*.helper.ts` | `/migration-patterns store` |
| UI | Tables, Forms (input/output only) | `/migration-patterns table`, `/ui-layout-guide` |
| Features | Page Component, Dialogs | `/migration-patterns dialog` |
| Shell | Routes, Resolvers | - |

### Phase 3: Quality Assurance

**Objective:** Ensure code compliance with migration standards

| Step | Skill | Description |
| ---- | ----- | ----------- |
| 1 | `/migration-lint <path>` | Auto-fix + generate compliance report |
| 2 | `/migration-review --from=<old> --to=<new>` | Compare migration completeness |
| 3 | `/compare-i18n-keys --from=<old.html> --to=<new.html>` | Verify translation key consistency |
| 4 | `/check-barrel-files <path>` | Remove redundant barrel files |

### Phase 4: QA Verification

**Objective:** Generate test cases, confirm functional consistency

| Step | Skill | Output |
| ---- | ----- | ------ |
| 1 | `/generate-qa-test-cases <path>` | `QA-TEST-CASES.md` |
| 2 | `/verify-legacy-with-qa-testcases <legacy-path>` | `LEGACY-VERIFICATION-REPORT.md` |

**Output Location:** `{target}/domain/src/lib/docs/`

## Best Practice Workflow (Sequence)

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant M as migrate-page
    participant L as migration-lint
    participant R as migration-review
    participant Q as generate-qa-test-cases
    participant V as verify-legacy-with-qa-testcases

    Dev->>M: 1. Execute migration analysis
    M-->>Dev: Output MIGRATION-ANALYSIS.md
    Dev->>Dev: 2. Manually implement each Layer
    Dev->>L: 3. Execute compliance check
    L-->>Dev: Auto-fix + report
    Dev->>R: 4. Check migration completeness
    R-->>Dev: Missing items report
    Dev->>Dev: 5. Fix missing items
    Dev->>Q: 6. Generate QA test cases
    Q-->>Dev: QA-TEST-CASES.md
    Dev->>V: 7. Verify legacy code
    V-->>Dev: LEGACY-VERIFICATION-REPORT.md
    Dev->>Dev: 8. Confirm functional consistency
```

## Auxiliary Skills Usage Timing

| Skill | When to Use |
| ----- | ----------- |
| `/migration-patterns <keyword>` | Whenever querying migration patterns (table, form, dialog, layout, button, store, syntax, validator) |
| `/icon-replacement <icon-name>` | When encountering legacy icons that need replacement |
| `/ui-layout-guide <query>` | When querying best practices for UI layout creation |
| `/form-extraction` | When needing to extract form structure for comparison |

## Notes

- E2E test generation and API Mock generation are not currently required
- Performance checks are secondary to migration, implementation deferred

## Quick Command Reference

```bash
# One-click complete migration workflow (recommended)
/full-migration-pipeline --from=/path/to/old --to=libs/mxsecurity/xxx-page
/full-migration-pipeline --page=xxx  # From GitLab

# Manual execution of each phase
/migrate-page --from=/path/to/old --to=libs/mxsecurity/xxx-page
/migration-lint libs/mxsecurity/xxx-page
/migration-review --from=/path/to/old --to=libs/mxsecurity/xxx-page
/generate-qa-test-cases libs/mxsecurity/xxx-page
/verify-legacy-with-qa-testcases /path/to/old

# Query patterns
/migration-patterns table
/migration-patterns form
/migration-patterns dialog

# Auxiliary tools
/icon-replacement settings
/ui-layout-guide card
/check-barrel-files libs/mxsecurity/xxx-page
```
