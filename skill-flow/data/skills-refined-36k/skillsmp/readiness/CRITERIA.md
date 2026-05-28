# Evaluation Criteria (81 total)

Reference for all criteria evaluated by the readiness skill.

## Repository-Scoped Checks (43 criteria)

Evaluated once for the entire repository. Denominator is always 1.

### Level 1 (Baseline)

| ID | Description |
|----|-------------|
| **readme** | README.md present with basic setup instructions |
| **env_template** | `.env.example` or env vars documented in README/AGENTS.md |
| **gitignore_comprehensive** | `.gitignore` covers `.env`, `node_modules`, build outputs, IDE files, OS files |

### Level 2 (Documented)

| ID | Description |
|----|-------------|
| **build_cmd_doc** | Build commands documented in README or AGENTS.md |
| **deps_pinned** | Lockfile committed (package-lock, yarn.lock, pnpm-lock, poetry.lock, or pinned requirements.txt) |
| **vcs_cli_tools** | `gh` or `glab` CLI installed and authenticated |
| **automated_pr_review** | [Skip] Bot-generated PR review comments (danger.js, AI reviewers) |
| **monorepo_tooling** | [Skip] Turborepo/Nx/Lerna configured for monorepos |
| **agents_md** | AGENTS.md at root with agent-focused instructions (>100 chars) |
| **automated_doc_generation** | Auto-generated docs (Swagger, JSDoc, Sphinx, changelog generators) |
| **devcontainer** | `.devcontainer/devcontainer.json` configured |
| **local_services_setup** | [Skip] docker-compose for local deps (DB, Redis, etc.) |
| **runbooks_documented** | Links to runbooks/playbooks in docs |
| **branch_protection** | [Skip] Branch protection via `gh api` (rulesets or legacy) |
| **codeowners** | CODEOWNERS file with valid assignments |
| **automated_security_review** | [Skip] SAST reports in PRs (Semgrep, CodeQL, Snyk) |
| **dependency_update_automation** | Dependabot or Renovate configured |
| **secrets_management** | Secrets manager integration or proper `.env` handling |
| **issue_templates** | `.github/ISSUE_TEMPLATE/` or `.gitlab/issue_templates/` |
| **issue_labeling_system** | Consistent labels (priority, type, area) |
| **pr_templates** | PR template with description/testing sections |

### Level 3 (Standardized)

| ID | Description |
|----|-------------|
| **large_file_detection** | Git hooks, LFS, or linter rules for file size limits |
| **tech_debt_tracking** | TODO/FIXME scanning, SonarQube debt tracking |
| **agentic_development** | Evidence of AI agents in git history or CI |
| **single_command_setup** | One command from clone to running dev server |
| **release_notes_automation** | Auto-generated changelogs (semantic-release, changesets) |
| **version_drift_detection** | [Skip] Monorepo version sync tools (syncpack, manypkg) |
| **release_automation** | CD pipelines, GitOps, or auto Docker publishing |
| **dead_feature_flag_detection** | [Skip] Stale flag detection (requires feature_flag_infrastructure) |
| **skills** | Skills directory with valid SKILL.md files |
| **documentation_freshness** | Key docs updated within 180 days |
| **service_flow_documented** | Architecture diagrams or service dependency docs |
| **devcontainer_runnable** | [Skip] Devcontainer builds successfully |
| **secret_scanning** | [Skip] Gitleaks, trufflehog, or GitHub secret scanning |

### Level 4 (Optimized)

| ID | Description |
|----|-------------|
| **fast_ci_feedback** | [Skip] CI completes in under 10 minutes |
| **build_performance_tracking** | [Skip] Build caching and timing metrics |
| **deployment_frequency** | [Skip] Multiple deploys per week |
| **feature_flag_infrastructure** | LaunchDarkly, Statsig, Unleash, or similar |
| **progressive_rollout** | [Skip] Canary or percentage-based deploys |
| **rollback_automation** | [Skip] One-click rollback capability |
| **agents_md_validation** | CI validates AGENTS.md commands work |
| **privacy_compliance** | [Skip] GDPR/CCPA handling, consent management |
| **backlog_health** | [Skip] >70% issues have titles >10 chars + labels |

---

## Application-Scoped Checks (38 criteria)

Evaluated per deployable unit. Denominator is N (total apps found).

### Level 1 (Baseline)

| ID | Description |
|----|-------------|
| **lint_config** | Linter configured (ESLint, ruff, flake8, SonarQube) |
| **type_check** | Type checker (tsconfig strict, mypy) |
| **formatter** | Code formatter (Prettier, Black) |
| **unit_tests_exist** | Test files present (*.test.ts, test_*.py) |

### Level 2 (Documented)

| ID | Description |
|----|-------------|
| **pre_commit_hooks** | Husky/lint-staged or .pre-commit-config.yaml |
| **strict_typing** | [Skip] Strict mode enabled in type checker |
| **unit_tests_runnable** | Test command works (use --listTests or --collect-only) |
| **test_coverage_thresholds** | Minimum coverage enforced |
| **database_schema** | [Skip] Schema files (Prisma, TypeORM, SQLAlchemy) |
| **structured_logging** | Logging library configured (pino, winston, structlog) |
| **error_tracking_contextualized** | Sentry/Bugsnag with source maps and context |

### Level 3 (Standardized)

| ID | Description |
|----|-------------|
| **naming_consistency** | Naming conventions enforced via linter or docs |
| **dead_code_detection** | Unused code detection (knip, vulture, ESLint no-unused-vars) |
| **duplicate_code_detection** | Copy-paste detection (jscpd, SonarQube CPD) |
| **unused_dependencies_detection** | Unused deps check (depcheck, knip, deptry) |
| **integration_tests_exist** | E2E or integration tests (Playwright, Cypress, pytest integration) |
| **test_naming_conventions** | Test file naming patterns enforced |
| **api_schema_docs** | [Skip] OpenAPI/Swagger or GraphQL schema |
| **distributed_tracing** | Trace ID propagation (OpenTelemetry, X-Request-ID) |
| **metrics_collection** | Metrics instrumentation (Datadog, Prometheus, CloudWatch) |
| **alerting_configured** | PagerDuty, OpsGenie, or custom alerts |
| **health_checks** | [Skip] /health endpoints or K8s probes |
| **pii_handling** | [Skip] PII detection/masking tooling |
| **log_scrubbing** | Log redaction configured |
| **product_analytics_instrumentation** | Mixpanel, Amplitude, PostHog, or GA4 |

### Level 4 (Optimized)

| ID | Description |
|----|-------------|
| **code_modularization** | [Skip] Module boundary enforcement (eslint-plugin-boundaries, ArchUnit) |
| **n_plus_one_detection** | [Skip] N+1 query detection (bullet, nplusone, DataLoader) |
| **heavy_dependency_detection** | [Skip] Bundle size analysis |
| **test_performance_tracking** | Test timing tracked in CI |
| **flaky_test_detection** | [Skip] Test retry config or flaky tracking |
| **test_isolation** | Parallel test execution configured |
| **code_quality_metrics** | [Skip] Coverage/complexity tracking |
| **deployment_observability** | Dashboard links or deploy notifications |
| **circuit_breakers** | [Skip] Resilience patterns (opossum, resilience4j) |
| **profiling_instrumentation** | [Skip] APM or profiling tools |
| **dast_scanning** | [Skip] OWASP ZAP or DAST in CI |

### Level 5 (Autonomous)

| ID | Description |
|----|-------------|
| **cyclomatic_complexity** | Complexity analysis (ESLint complexity, radon, SonarQube) |
| **error_to_insight_pipeline** | Error tracking → issue creation automation |

---

## Pillar Groupings

Map criteria to 8 pillars for reporting:

| Pillar | Criteria IDs |
|--------|-------------|
| **Code Quality** | lint_config, type_check, formatter, pre_commit_hooks, strict_typing, naming_consistency, cyclomatic_complexity, dead_code_detection, duplicate_code_detection, code_modularization |
| **Build Tooling** | build_cmd_doc, deps_pinned, single_command_setup, release_notes_automation, release_automation, monorepo_tooling, version_drift_detection, dead_feature_flag_detection, n_plus_one_detection, heavy_dependency_detection, unused_dependencies_detection |
| **Testing** | unit_tests_exist, unit_tests_runnable, test_coverage_thresholds, integration_tests_exist, test_naming_conventions, test_performance_tracking, flaky_test_detection, test_isolation |
| **Documentation** | readme, agents_md, automated_doc_generation, skills, documentation_freshness, service_flow_documented, agents_md_validation, runbooks_documented |
| **Dev Environment** | env_template, devcontainer, devcontainer_runnable, local_services_setup, vcs_cli_tools, agentic_development |
| **Quality Gates** | large_file_detection, tech_debt_tracking, fast_ci_feedback, build_performance_tracking, deployment_frequency, feature_flag_infrastructure, progressive_rollout, rollback_automation |
| **Security** | gitignore_comprehensive, branch_protection, secret_scanning, codeowners, automated_security_review, dependency_update_automation, secrets_management, privacy_compliance, pii_handling, log_scrubbing, dast_scanning |
| **Observability** | structured_logging, distributed_tracing, metrics_collection, code_quality_metrics, error_tracking_contextualized, alerting_configured, deployment_observability, health_checks, circuit_breakers, profiling_instrumentation, product_analytics_instrumentation, error_to_insight_pipeline |
| **Issue Management** | issue_templates, issue_labeling_system, pr_templates, backlog_health, automated_pr_review |
| **API & Data** | api_schema_docs, database_schema |

---

## Validation Checklist

Before generating report, verify all 81 criteria are present:

```
large_file_detection, tech_debt_tracking, build_cmd_doc, deps_pinned, vcs_cli_tools,
automated_pr_review, agentic_development, fast_ci_feedback, build_performance_tracking,
deployment_frequency, single_command_setup, feature_flag_infrastructure, release_notes_automation,
progressive_rollout, rollback_automation, monorepo_tooling, version_drift_detection,
release_automation, dead_feature_flag_detection, agents_md, readme, automated_doc_generation,
skills, documentation_freshness, service_flow_documented, agents_md_validation, devcontainer,
env_template, local_services_setup, devcontainer_runnable, runbooks_documented, branch_protection,
secret_scanning, codeowners, automated_security_review, dependency_update_automation,
gitignore_comprehensive, privacy_compliance, secrets_management, issue_templates,
issue_labeling_system, backlog_health, pr_templates, lint_config, type_check, formatter,
pre_commit_hooks, strict_typing, naming_consistency, cyclomatic_complexity, dead_code_detection,
duplicate_code_detection, code_modularization, n_plus_one_detection, heavy_dependency_detection,
unused_dependencies_detection, unit_tests_exist, integration_tests_exist, unit_tests_runnable,
test_performance_tracking, flaky_test_detection, test_coverage_thresholds, test_naming_conventions,
test_isolation, api_schema_docs, database_schema, structured_logging, distributed_tracing,
metrics_collection, code_quality_metrics, error_tracking_contextualized, alerting_configured,
deployment_observability, health_checks, circuit_breakers, profiling_instrumentation,
dast_scanning, pii_handling, log_scrubbing, product_analytics_instrumentation, error_to_insight_pipeline
```
