# V1 Templates

V1 = "ready for autonomous agent execution". these templates define the quality bar for each project type.

## template structure

```yaml
name: {template-name}
applies_to: [project1, project2]

code:
  test_coverage: {percentage}
  build: {status}
  types: {status}
  lint: {status}

architecture:
  cycles: {status}
  dead_code: {percentage}
  packages: {status}

linear:
  issues_have_context: {bool}
  context_freshness: {duration}
  no_vague_issues: {bool}

docs:
  agents_md: {status}
  readme: {status}

ci:
  tests: {status}
  deploy: {status}
```

---

## convex-next-v1

for Convex + Next.js monorepo projects.

```yaml
name: convex-next-v1
applies_to: [arbor, kumori, koto, webs, squish, pal, saya]

code:
  test_coverage: 80%
  build: passing
  types: clean (no errors)
  lint: clean (biome check passes)

architecture:
  cycles: none (layer --check-cycles clean)
  dead_code: <5% (outline --unused minimal)
  packages: documented (each package has purpose in README)

linear:
  all_issues_have_context: true
  context_freshness: <14 days
  no_vague_issues: true (title + description + acceptance criteria)

docs:
  agents_md: present and accurate (reflects current architecture)
  readme: present with setup instructions

ci:
  tests: automated (vitest + convex-test)
  deploy: automated (Vercel + Convex)
```

### convex-next checklist

- [ ] `pnpm test` passes (verify --format=summary)
- [ ] `pnpm build` succeeds
- [ ] `pnpm typecheck` clean
- [ ] `pnpm lint` clean (biome check)
- [ ] `layer . --check-cycles` reports no cycles
- [ ] `outline --unused -r` shows <5% dead exports
- [ ] All Linear issues have `<!-- issue-context:analysis -->` markers
- [ ] No issue context older than 14 days
- [ ] AGENTS.md/CLAUDE.md reflects current codebase
- [ ] README has setup instructions
- [ ] CI runs tests on PR
- [ ] Deploy is automated

---

## library-v1

for CLI tools and utility packages.

```yaml
name: library-v1
applies_to: [agents-cli, layer, outline, verify, trails, slack-cli, linear-cli]

code:
  test_coverage: 90%
  build: passing
  types: strict (no any, no type assertions)
  lint: clean

architecture:
  exports: documented (each export has JSDoc or README entry)
  deps: minimal (no unnecessary dependencies)
  api: stable (no breaking changes without semver major)

linear:
  issues_have_context: true

docs:
  readme: comprehensive (installation, usage, examples)
  api_docs: generated or manual
  changelog: maintained
```

### library checklist

- [ ] Test coverage >= 90%
- [ ] Build passes
- [ ] No `any` types
- [ ] All exports documented
- [ ] Dependencies justified
- [ ] README has usage examples
- [ ] CHANGELOG up to date

---

## cli-v1

for command-line tools (subset of library-v1 with CLI-specific requirements).

```yaml
name: cli-v1
applies_to: [agents, layer, outline, verify, slack, linear, trails, mem]

code:
  test_coverage: 85%
  build: passing
  types: clean

cli:
  help_text: comprehensive (--help shows all commands and options)
  error_messages: actionable (tells user what to do)
  json_output: all commands (--json flag works everywhere)
  exit_codes: documented

docs:
  rules_md: present in ~/.agents/rules/{tool}.md
  readme: has quick start
```

### cli checklist

- [ ] `{tool} --help` shows all commands
- [ ] Error messages explain how to fix
- [ ] `--json` flag on all commands
- [ ] Exit codes are consistent
- [ ] `~/.agents/rules/{tool}.md` exists and is current
- [ ] README has quick start example

---

## swift-v1

for iOS/macOS Swift projects.

```yaml
name: swift-v1
applies_to: [arbor-apple, kumori-apple, sine-apple]

code:
  test_coverage: 70%
  build: passing (xcodebuild)
  types: clean (no warnings)
  lint: clean (swiftlint)

architecture:
  cycles: none
  dead_code: minimal
  patterns: documented (MVVM, etc.)

linear:
  issues_have_context: true

docs:
  readme: setup + signing instructions
  agents_md: present

ci:
  tests: automated (xcodebuild test)
  archive: works (xcodebuild archive)
```

### swift checklist

- [ ] `xcodebuild test` passes
- [ ] `xcodebuild build` succeeds
- [ ] No compiler warnings
- [ ] SwiftLint passes
- [ ] README has signing setup
- [ ] CI runs tests

---

## slack-bot-v1

for Slack bot projects.

```yaml
name: slack-bot-v1
applies_to: [saya]

code:
  test_coverage: 80%
  build: passing
  types: clean

bot:
  slash_commands: documented
  event_handlers: documented
  permissions: minimal (only needed scopes)

linear:
  issues_have_context: true

docs:
  readme: setup + OAuth instructions
  agents_md: present

ci:
  tests: automated
  deploy: automated
```

### slack-bot checklist

- [ ] All slash commands documented
- [ ] Event handlers have tests
- [ ] OAuth scopes are minimal
- [ ] README has OAuth setup
- [ ] CI runs tests
- [ ] Deploy is automated

---

## generic-v1

fallback for unknown project types.

```yaml
name: generic-v1
applies_to: [unknown]

code:
  test_coverage: 70%
  build: passing
  lint: passing

linear:
  issues_have_context: true

docs:
  readme: present
```

### generic checklist

- [ ] Tests pass
- [ ] Build passes
- [ ] Lint passes
- [ ] README exists
- [ ] Linear issues have context

---

## scoring rubric

| criterion | weight | measurement |
|-----------|--------|-------------|
| test coverage | 25% | `verify --coverage` output |
| build health | 20% | `pnpm build` exit code |
| type safety | 15% | `pnpm typecheck` errors |
| architecture | 15% | `layer --check-cycles` + `outline --unused` |
| linear context | 15% | % issues with `issue-context:` markers |
| docs | 10% | AGENTS.md + README presence and accuracy |

### V1 readiness score

| score | status | meaning |
|-------|--------|---------|
| 90-100 | ready | safe for autonomous execution |
| 75-89 | almost | minor gaps, can proceed with caution |
| 50-74 | not ready | significant gaps, address blockers first |
| <50 | blocked | major issues, needs focused work |

---

## applying templates

```bash
# Determine template
PROJECT_TYPE=$(detect_project_type "$PROJECT_PATH")
TEMPLATE="${PROJECT_TYPE}-v1"

# Load template
TEMPLATE_FILE="~/.agents/skills/linear-audit/references/v1-templates.md"

# Score against template
# ... scoring logic per criterion ...

# Generate gap report
# ... gaps = template requirements - current state ...
```
