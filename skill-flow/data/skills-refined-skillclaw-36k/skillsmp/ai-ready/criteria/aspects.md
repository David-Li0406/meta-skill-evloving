# Aspect Criteria Reference

## Contents
- [Aspect 1: Documentation (15%)](#aspect-1-documentation)
- [Aspect 2: Architecture (15%)](#aspect-2-architecture)
- [Aspect 3: Testing (12%)](#aspect-3-testing)
- [Aspect 4: Type Safety (12%)](#aspect-4-type-safety)
- [Aspect 5: Agent Instructions (15%)](#aspect-5-agent-instructions)
- [Aspect 6: File Structure (10%)](#aspect-6-file-structure)
- [Aspect 7: Context Optimization (11%)](#aspect-7-context-optimization)
- [Aspect 8: Security (10%)](#aspect-8-security)

---

## Aspect 1: Documentation

**Weight: 15% | Max: 190 points (19 criteria)**

| # | Criterion | 0 | 5 | 10 |
|---|-----------|---|---|-----|
| 1.1 | README exists | Missing | Minimal | Comprehensive |
| 1.2 | Getting started section | Missing | Basic | Step-by-step |
| 1.3 | Project overview | Missing | Brief | Detailed |
| 1.4 | API documentation | Missing | Partial | Complete |
| 1.5 | JSDoc/docstrings coverage | None | <50% | >80% |
| 1.6 | ARCHITECTURE.md | Missing | Minimal | C4-style |
| 1.7 | ADRs | None | Some | Active practice |
| 1.8 | Diagrams | None | Basic | Comprehensive |
| 1.9 | CONTRIBUTING.md | Missing | Basic | Detailed |
| 1.10 | CHANGELOG | None | Inconsistent | keep-a-changelog |
| 1.11 | Code examples | None | Few | Comprehensive |
| 1.12 | Error handling docs | None | Partial | Complete |
| 1.13 | Environment setup | Missing | Basic | With troubleshooting |
| 1.14 | Deployment docs | Missing | Basic | Full runbook |
| 1.15 | Inline why-comments | None | Some | Appropriate |
| 1.16 | Executable specs (specs/) | Missing | Some | Comprehensive |
| 1.17 | Storybook/CSF3 | Missing | Basic | Comprehensive |
| 1.18 | NPM scripts standardized | Missing | Some | All present |
| 1.19 | Repository map | Missing | Basic tree | Comprehensive |

**Check:** `**/*.md`, `docs/`, `specs/`, `.storybook`, `package.json` scripts

---

## Aspect 2: Architecture

**Weight: 15% | Max: 180 points (18 criteria)**

| # | Criterion | 0 | 5 | 10 |
|---|-----------|---|---|-----|
| 2.1 | Module boundaries | Spaghetti | Some separation | Clean |
| 2.2 | Dependency direction | Circular | Some issues | Unidirectional |
| 2.3 | Layer separation | Mixed | Partial | Clean |
| 2.4 | Single responsibility | God objects | Mixed | Focused |
| 2.5 | Coupling | Tight | Moderate | Loose |
| 2.6 | Cohesion | Scattered | Moderate | High |
| 2.7 | Vertical slices | Horizontal | Mixed | Feature-based |
| 2.8 | Config externalized | Hardcoded | Partial | Full |
| 2.9 | Error boundaries | None | Partial | Clear |
| 2.10 | Interface segregation | Fat | Some | Focused |
| 2.11 | Dependency injection | Hard deps | Partial | Full DI |
| 2.12 | Pattern consistency | Ad-hoc | Mostly | Uniform |
| 2.13 | Architecture enforcement | None | Linter | dep-cruiser |
| 2.14 | Module size | >100 files | 50-100 | 30-50 |
| 2.15 | Event-driven decoupling | Direct only | Some | Typed bus |
| 2.16 | FSD structure | None | Partial | Full |
| 2.17 | State machines (XState) | Implicit | Redux | Explicit |
| 2.18 | API contract (OpenAPI) | Missing | Outdated | Current |

**Check:** imports for cycles, `features/`, `entities/`, `openapi.yaml`, dep-cruiser config

---

## Aspect 3: Testing

**Weight: 12% | Max: 230 points (23 criteria)**

| # | Criterion | 0 | 5 | 10 |
|---|-----------|---|---|-----|
| 3.1 | Test files exist | None | Some | Comprehensive |
| 3.2 | Coverage | <20% | 50-70% | >80% |
| 3.3 | Co-location | Separate | Mixed | Co-located |
| 3.4 | Naming | Poor | Inconsistent | Clear |
| 3.5 | Unit tests | None | Some | Comprehensive |
| 3.6 | Integration tests | None | Some | Key paths |
| 3.7 | E2E tests | None | Basic | Critical flows |
| 3.8 | Fixtures organized | None | Basic | Well-organized |
| 3.9 | Mocking approach | Over-mocking | Inconsistent | Strategic |
| 3.10 | Test documentation | None | Some | Clear purpose |
| 3.11 | CI integration | None | Basic | Full pipeline |
| 3.12 | Test data | Hardcoded | Partial | Factories |
| 3.13 | Stable selectors | Brittle | Mixed | data-testid |
| 3.14 | Page Object Model | Mixed | Partial | Clean POM |
| 3.15 | A11y checks | None | Manual | Automated |
| 3.16 | Visual regression | None | Basic | Chromatic |
| 3.17 | No hardcoded delays | Common | Some | Auto-wait |
| 3.18 | Test independence | Order-dependent | Some shared | Isolated |
| 3.19 | Failure artifacts | None | Manual | Auto capture |
| 3.20 | Flaky management | Ignored | Retry-only | Root cause |
| 3.21 | TestIds constants | Scattered | Partial | Centralized |
| 3.22 | Test case IDs | None | Some | MM-T pattern |
| 3.23 | Screenplay pattern | N/A | Basic POM | Full |

**Check:** `**/*.test.*`, `**/*.spec.*`, coverage config, playwright.config, CI files

---

## Aspect 4: Type Safety

**Weight: 12% | Max: 100 points (10 criteria)**

| # | Criterion | 0 | 5 | 10 |
|---|-----------|---|---|-----|
| 4.1 | Static typing | None | Optional | Strict |
| 4.2 | `any` usage | Widespread | Limited | None |
| 4.3 | Null safety | Unchecked | Partial | strictNullChecks |
| 4.4 | Type exports | Missing | Partial | Complete |
| 4.5 | Generics | None | Basic | Appropriate |
| 4.6 | Branded types | None | N/A | For IDs |
| 4.7 | Type narrowing | instanceof | Mixed | Discriminants |
| 4.8 | Return types | Implicit | Mixed | Explicit |
| 4.9 | Parameter types | Implicit | Mixed | All typed |
| 4.10 | Type assertions | Excessive | Minimal | Rare |

**Language adaptations:**
- **TypeScript:** tsconfig strict, branded types
- **Python:** type hints, mypy/pyright
- **Go:** interface{}/any usage
- **Rust:** unsafe blocks, newtype

---

## Aspect 5: Agent Instructions

**Weight: 15% | Max: 250 points (25 criteria)**

| # | Criterion | 0 | 5 | 10 |
|---|-----------|---|---|-----|
| 5.1 | CLAUDE.md/AGENTS.md | Missing | Basic | Comprehensive |
| 5.2 | Project overview | Missing | Brief | Clear |
| 5.3 | Tech stack | Missing | Listed | With versions |
| 5.4 | Code conventions | Missing | Basic | With examples |
| 5.5 | File structure | Missing | Tree | Annotated |
| 5.6 | Commands listed | Missing | Few | Complete |
| 5.7 | Testing instructions | Missing | Basic | Comprehensive |
| 5.8 | NEVER rules | Missing | Few | Comprehensive |
| 5.9 | ALWAYS rules | Missing | Few | Comprehensive |
| 5.10 | Error patterns | Missing | Basic | Detailed |
| 5.11 | Key abstractions | Missing | Some | All major |
| 5.12 | Workflows | Missing | Basic | Detailed |
| 5.13 | Security rules | Missing | Basic | Comprehensive |
| 5.14 | Dependencies explained | Missing | Listed | Why each |
| 5.15 | Quick reference | Missing | Basic | Complete |
| 5.16 | Instruction count | >300 | 200-300 | ~150-200 |
| 5.17 | ASK FIRST rules | Missing | Few | Clear |
| 5.18 | .cursor/rules | Missing | Basic | Comprehensive |
| 5.19 | .windsurf/rules | Missing | Basic | Comprehensive |
| 5.20 | .clinerules | Missing | Basic | Comprehensive |
| 5.21 | Multi-agent symlinks | Separate | Partial | Unified |
| 5.22 | copilot-instructions | Missing | Basic | With filters |
| 5.23 | Custom commands | None | Basic | .cursor/commands/ |
| 5.24 | .aider.conf.yml | Missing | Basic | Comprehensive |
| 5.25 | Path-scoped instructions | None | Some | Full router |

**Check:** CLAUDE.md, AGENTS.md, .cursor/, .github/copilot-instructions.md, symlinks

---

## Aspect 6: File Structure

**Weight: 10% | Max: 130 points (13 criteria)**

| # | Criterion | 0 | 5 | 10 |
|---|-----------|---|---|-----|
| 6.1 | Lines per file | >1000 | 500-1000 | 150-500 |
| 6.2 | Nesting depth | >7 | 5-7 | ≤4 |
| 6.3 | Files per dir | >30 | 15-30 | ≤15 |
| 6.4 | File naming | Inconsistent | Mostly | Uniform |
| 6.5 | Dir naming | Unclear | Somewhat | Self-documenting |
| 6.6 | Index/barrel files | None/excessive | Some | Strategic |
| 6.7 | Colocation | Scattered | Partial | Well colocated |
| 6.8 | Config organization | Scattered | Root | config/ |
| 6.9 | Assets | Mixed | Partial | Dedicated |
| 6.10 | Monorepo structure | Unclear | Basic | Nx/Turborepo |
| 6.11 | Nested instructions | Root only | Some | Per package |
| 6.12 | Kebab-case folders | Inconsistent | Mostly | All |
| 6.13 | Import aliases | Relative | Partial | @/ aliases |

**Check:** sample file LOC, directory depth, naming patterns, tsconfig paths

---

## Aspect 7: Context Optimization

**Weight: 11% | Max: 200 points (20 criteria)**

| # | Criterion | 0 | 5 | 10 |
|---|-----------|---|---|-----|
| 7.1 | llms.txt | Missing | Basic | Comprehensive |
| 7.2 | llms-full.txt | Missing | N/A | Present |
| 7.3 | Chunking-friendly | Long functions | Mixed | Small units |
| 7.4 | Self-documenting names | Cryptic | Mostly | Excellent |
| 7.5 | Why-comments | None/what | Mixed | Appropriate |
| 7.6 | Magic numbers | Common | Some | Named constants |
| 7.7 | Dead code | Significant | Some | Clean |
| 7.8 | Formatting | Inconsistent | Mostly | Enforced |
| 7.9 | Import organization | Random | Grouped | Sorted |
| 7.10 | Single export per file | Multiple | Mixed | Clean |
| 7.11 | Error messages | Generic | Basic | With context |
| 7.12 | Hierarchical context | Root only | Some | Full router |
| 7.13 | prompts/ directory | Missing | Some | Organized |
| 7.14 | Design tokens (JSON) | Hardcoded | CSS vars | W3C standard |
| 7.15 | Semantic HTML | Div soup | Mixed | Semantic |
| 7.16 | MCP integration | None | Manual | Figma/Storybook |
| 7.17 | Progress files | None | Ad-hoc | Structured |
| 7.18 | Token hierarchy | Flat | Semantic | 3-tier |
| 7.19 | Atomic Design | None | Partial | Full |
| 7.20 | Screaming architecture | Framework-centric | Mixed | Domain-centric |

**Check:** llms.txt, naming patterns, .prettierrc, prompts/, tokens.json

---

## Aspect 8: Security

**Weight: 10% | Max: 120 points (12 criteria)**

| # | Criterion | 0 | 5 | 10 |
|---|-----------|---|---|-----|
| 8.1 | .aiignore | Missing | Basic | Comprehensive |
| 8.2 | .gitignore secrets | Missing | Basic | Complete |
| 8.3 | Hardcoded secrets | Found | Suspicious | Clean |
| 8.4 | PII in code | Found | Minor | Clean |
| 8.5 | Env vars for secrets | Hardcoded | Mixed | All external |
| 8.6 | NEVER rules (sensitive) | None | Basic | Comprehensive |
| 8.7 | Input validation | None | Partial | Comprehensive |
| 8.8 | Output encoding | None | Partial | Proper |
| 8.9 | Dependency security | Vulnerable | Some updates | Regular |
| 8.10 | Security docs | None | Basic | Threat model |
| 8.11 | AI commit attribution | None | Manual | Automated |
| 8.12 | .cursorignore | Missing | Basic | Comprehensive |

**Check:** .aiignore, .gitignore, grep for `API_KEY=`, `password=`, git log for Co-authored-by

---

## Scoring Formula

```
Aspect Score = (Sum of criteria / Max points) × 100

Overall = (Doc × 0.15) + (Arch × 0.15) + (Test × 0.12) + (Type × 0.12)
        + (Agent × 0.15) + (File × 0.10) + (Context × 0.11) + (Security × 0.10)
```

## Grade Scale

| Grade | Range | Description |
|-------|-------|-------------|
| A | 90-100 | AI-ready |
| B | 75-89 | Minor improvements |
| C | 60-74 | Notable gaps |
| D | 45-59 | Significant work |
| F | 0-44 | Major overhaul |
