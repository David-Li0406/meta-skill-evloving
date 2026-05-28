# Sample Readiness Report Output

Example output for a TypeScript monorepo project.

```
╔══════════════════════════════════════════════════════════════════╗
║                   AGENT READINESS REPORT                         ║
║                      acme/web-platform                           ║
╠══════════════════════════════════════════════════════════════════╣
║  LEVEL: 3          SCORE: 58/81 (72%)          APPS: 3           ║
╚══════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────┐
│ PILLAR OVERVIEW                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Code Quality    ██████████████████░░ 90%  (9/10)  ✓            │
│ Build           ████████████░░░░░░░░ 60%  (6/10)  ⚠            │
│ Testing         ████████████████████ 100% (8/8)   ✓            │
│ Documentation   ████████░░░░░░░░░░░░ 40%  (4/10)  ✗            │
│ Dev Environment ██████████████░░░░░░ 70%  (7/10)  ⚠            │
│ Quality Gates   ████████████████░░░░ 80%  (8/10)  ✓            │
│ Security        ██████████░░░░░░░░░░ 50%  (5/10)  ⚠            │
│ Observability   ████████████████████ 100% (6/6)   ✓            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ LEVEL PROGRESSION                                               │
├─────────────────────────────────────────────────────────────────┤
│ L1 Functional   ████████████████████ 100%  ✓ ACHIEVED          │
│ L2 Documented   ████████████████░░░░  82%  ✓ ACHIEVED          │
│ L3 Standardized ██████████████░░░░░░  72%  ⚠ IN PROGRESS       │
│ L4 Optimized    ████████░░░░░░░░░░░░  45%  ✗ NOT STARTED       │
│ L5 Autonomous   ░░░░░░░░░░░░░░░░░░░░   0%  ✗ NOT STARTED       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ ▼ CODE QUALITY (90%)                                            │
├─────────────────────────────────────────────────────────────────┤
│ ✓ lint_config          ESLint configured with recommended rules │
│ ✓ type_check           TypeScript strict mode enabled           │
│ ✓ formatter            Prettier configured                      │
│ ✓ unit_tests_exist     Jest tests found in all 3 apps           │
│ ✓ pre_commit_hooks     Husky + lint-staged configured           │
│ ✓ strict_typing        strict: true in tsconfig.json            │
│ ✓ unit_tests_runnable  npm test exits 0                         │
│ ✓ test_coverage        80% threshold in jest.config.js          │
│ ✓ linting_ci           ESLint runs in GitHub Actions            │
│ ✗ dead_code_analysis   No dead code detection tool found        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ ▼ BUILD (60%)                                                   │
├─────────────────────────────────────────────────────────────────┤
│ ✓ build_cmd_doc        Build commands in README                 │
│ ✓ deps_pinned          package-lock.json committed              │
│ ✓ monorepo_tooling     Turborepo configured                     │
│ ✓ release_automation   GitHub Actions deploys to Vercel         │
│ ✓ single_command_setup npm install && npm run dev works         │
│ ✓ build_ci             Build runs in CI pipeline                │
│ ✗ fast_ci_feedback     CI takes 18 minutes (>10 min threshold)  │
│ ✗ build_perf_tracking  No build timing metrics found            │
│ ✗ version_drift        No syncpack or manypkg configured        │
│ ○ docker_build         Skipped - no Dockerfile present          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ ▼ DOCUMENTATION (40%)                                           │
├─────────────────────────────────────────────────────────────────┤
│ ✓ readme               README.md with setup instructions        │
│ ✓ env_template         .env.example present                     │
│ ✗ agents_md            No AGENTS.md found                       │
│ ✗ automated_docs       No Swagger/JSDoc generation              │
│ ✗ runbooks             No runbook links found                   │
│ ✗ service_flow_docs    No architecture diagrams                 │
│ ✗ doc_freshness        README last updated 210 days ago         │
│ ✗ api_documentation    No API docs found                        │
│ ○ changelog            Skipped - using release notes            │
│ ○ adr                  Skipped - no ADR requirement             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ TOP 5 PRIORITY ACTIONS                                          │
├─────────────────────────────────────────────────────────────────┤
│ 1. [HIGH] Add AGENTS.md                                         │
│    Create AGENTS.md with agent-specific instructions for        │
│    autonomous AI workflows. Include build/test/lint commands.   │
│                                                                  │
│ 2. [HIGH] Update documentation freshness                        │
│    README.md was last updated 210 days ago. Review and update   │
│    to reflect current project state.                            │
│                                                                  │
│ 3. [MED]  Add architecture documentation                        │
│    Create service flow diagrams or dependency documentation     │
│    to help agents understand system structure.                  │
│                                                                  │
│ 4. [MED]  Configure dead code analysis                          │
│    Add ts-prune or knip to detect unused exports and files.     │
│                                                                  │
│ 5. [LOW]  Optimize CI pipeline                                  │
│    Current CI takes 18 minutes. Add caching and parallelization │
│    to reduce feedback time below 10 minutes.                    │
└─────────────────────────────────────────────────────────────────┘

─────────────────────────────────────────────────────────────────
Generated: 2025-01-22T20:15:00Z
Repository: /Users/dev/projects/acme/web-platform
Apps analyzed: 3 (api, web, admin)
─────────────────────────────────────────────────────────────────
```

## JSON Input Format

The HTML report generator expects this JSON structure:

```json
{
  "repoName": "acme/web-platform",
  "level": 3,
  "score": 58,
  "total": 81,
  "appsCount": 3,
  "pillars": [
    { "name": "Code Quality", "score": 90, "passed": 9, "total": 10 },
    { "name": "Build", "score": 60, "passed": 6, "total": 10 },
    { "name": "Testing", "score": 100, "passed": 8, "total": 8 },
    { "name": "Documentation", "score": 40, "passed": 4, "total": 10 },
    { "name": "Dev Environment", "score": 70, "passed": 7, "total": 10 },
    { "name": "Quality Gates", "score": 80, "passed": 8, "total": 10 },
    { "name": "Security", "score": 50, "passed": 5, "total": 10 },
    { "name": "Observability", "score": 100, "passed": 6, "total": 6 }
  ],
  "levels": [
    { "level": "L1", "score": 100, "achieved": true },
    { "level": "L2", "score": 82, "achieved": true },
    { "level": "L3", "score": 72, "achieved": false },
    { "level": "L4", "score": 45, "achieved": false },
    { "level": "L5", "score": 0, "achieved": false }
  ],
  "actions": [
    { "priority": "HIGH", "title": "Add AGENTS.md", "description": "Create agent-specific instructions" },
    { "priority": "HIGH", "title": "Update documentation", "description": "README outdated by 210 days" },
    { "priority": "MED", "title": "Add architecture docs", "description": "Service flow diagrams needed" }
  ],
  "criteria": [
    { "pillar": "Code Quality", "id": "lint_config", "status": "pass", "rationale": "ESLint configured" },
    { "pillar": "Documentation", "id": "agents_md", "status": "fail", "rationale": "No AGENTS.md found" }
  ]
}
```
