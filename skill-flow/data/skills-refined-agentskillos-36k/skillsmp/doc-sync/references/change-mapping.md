# Code Change to Documentation Mapping

Reference guide for understanding how different types of code changes map to
documentation needs.

## File Pattern Categories

### Feature Changes

Files that typically indicate new or changed features:

| Pattern                | Framework            | Documentation Impact                  |
| ---------------------- | -------------------- | ------------------------------------- |
| `src/app/*/page.tsx`   | Next.js App Router   | New route - document in features      |
| `src/pages/*.tsx`      | Next.js Pages Router | New route - document in features      |
| `app/*/page.tsx`       | Next.js              | New route - document in features      |
| `routes/*.ts`          | Express/Fastify      | New endpoint - document in API        |
| `src/components/*.tsx` | React                | New component - may need design docs  |
| `views/*.py`           | Django               | New view - document in features       |
| `controllers/*.rb`     | Rails                | New controller - document in features |
| `handlers/*.go`        | Go                   | New handler - document in API         |

**Documentation checklist for feature changes:**

- [ ] Feature doc exists or created
- [ ] Route documented with path, params, response
- [ ] Components documented if reusable
- [ ] Status is IMPLEMENTED (not PLANNED)

### Architecture Changes

Files that indicate structural or infrastructure changes:

| Pattern            | What It Means     | Documentation Impact  |
| ------------------ | ----------------- | --------------------- |
| `src/lib/*.ts`     | Core utilities    | Architecture overview |
| `src/utils/*.ts`   | Helpers           | Quick reference       |
| `migrations/*`     | Schema changes    | Data model docs       |
| `supabase/*`       | DB integration    | ADR + tech stack      |
| `prisma/*`         | ORM config        | Data model docs       |
| `src/middleware/*` | Request handling  | Architecture          |
| `src/providers/*`  | Context providers | Architecture          |

**Documentation checklist for architecture changes:**

- [ ] ADR created for significant decisions
- [ ] Architecture overview updated
- [ ] Data model docs if schema changed
- [ ] Tech stack updated if new tool

### Dependency Changes

Files indicating dependency modifications:

| Pattern             | Framework | Documentation Impact       |
| ------------------- | --------- | -------------------------- |
| `package.json`      | Node.js   | Tech stack reference       |
| `package-lock.json` | Node.js   | Usually just version bumps |
| `requirements.txt`  | Python    | Tech stack reference       |
| `pyproject.toml`    | Python    | Tech stack reference       |
| `go.mod`            | Go        | Tech stack reference       |
| `Cargo.toml`        | Rust      | Tech stack reference       |
| `Gemfile`           | Ruby      | Tech stack reference       |

**Documentation checklist for dependency changes:**

- [ ] New dep added to tech stack
- [ ] Purpose documented
- [ ] Key files using it noted
- [ ] ADR if it's a major addition

### Configuration Changes

Files indicating config modifications:

| Pattern        | What It Is        | Documentation Impact |
| -------------- | ----------------- | -------------------- |
| `*.config.ts`  | Build/tool config | May need guides      |
| `*.config.js`  | Build/tool config | May need guides      |
| `.env*`        | Environment vars  | Deployment docs      |
| `docker*`      | Containerization  | Deployment docs      |
| `deployment/*` | Deploy config     | Deployment docs      |
| `vercel.json`  | Vercel config     | Deployment docs      |
| `.github/*`    | CI/CD             | Contributing docs    |

**Documentation checklist for config changes:**

- [ ] Deployment docs updated
- [ ] New env vars documented
- [ ] Setup instructions current

### Style Changes

Files indicating design/styling changes:

| Pattern             | What It Is      | Documentation Impact |
| ------------------- | --------------- | -------------------- |
| `globals.css`       | Global styles   | Design system        |
| `*.css`             | Stylesheets     | Design system        |
| `tailwind.config.*` | Tailwind config | Design system        |
| `theme*`            | Theme config    | Design system        |
| `tokens*`           | Design tokens   | Design system        |
| `design/*`          | Design files    | Design system        |

**Documentation checklist for style changes:**

- [ ] Design system docs updated
- [ ] New colors/tokens documented
- [ ] Component variants documented

### Documentation Changes

Files that are already documentation:

| Pattern           | What It Is     | Documentation Impact |
| ----------------- | -------------- | -------------------- |
| `docs/*`          | Documentation  | Already documented   |
| `*.md` (non-root) | Markdown docs  | Already documented   |
| `README.md`       | Project readme | Root documentation   |
| `CLAUDE.md`       | AI context     | AI assistant docs    |
| `CHANGELOG.md`    | Change log     | Version history      |

**Note:** Changes to existing docs should still be reviewed for:

- Consistency with code changes in same commit
- Updated `last_updated` dates
- Cross-reference validity

---

## Impact Assessment Matrix

How to assess documentation impact of changes:

| Change Type      | High Impact       | Medium Impact       | Low Impact   |
| ---------------- | ----------------- | ------------------- | ------------ |
| **Feature**      | New feature       | Feature enhancement | Bug fix      |
| **Architecture** | New pattern/tool  | Refactor            | Optimization |
| **Dependency**   | Major new dep     | Version bump        | Dev dep      |
| **Config**       | New env var       | Config tweak        | Comment      |
| **Style**        | New design system | Theme change        | Color tweak  |

---

## Commit Message Patterns

Commit messages often indicate documentation needs:

| Message Contains                | Likely Documentation  |
| ------------------------------- | --------------------- |
| `feat:`, `feature:`, `add:`     | Feature docs          |
| `BREAKING:`, `BREAKING CHANGE:` | Migration guide       |
| `fix:`, `bug:`                  | Usually none          |
| `refactor:`                     | Architecture if major |
| `deps:`, `dependency:`          | Tech stack            |
| `config:`, `env:`               | Deployment docs       |
| `style:`, `design:`             | Design system         |
| `docs:`                         | Already documentation |
| `chore:`                        | Usually none          |
| `test:`                         | Usually none          |

---

## Priority Determination

How to prioritize documentation updates:

### Critical Priority

- Security-related changes undocumented
- Breaking changes without migration guide
- Wrong/misleading existing documentation

### High Priority

- New feature with no documentation
- PLANNED status on implemented feature
- Major architectural decision without ADR

### Medium Priority

- New dependency not in tech stack
- Missing route documentation
- Outdated code examples

### Low Priority

- Minor wording improvements
- Cross-reference fixes
- Date updates

---

## Multi-Category Changes

A single commit often affects multiple categories:

**Example:** "Add article system"

- `src/app/articles/page.tsx` → feature
- `src/lib/articles.ts` → architecture
- `package.json` (add marked) → dependency
- `supabase/migrations/*` → architecture

**Best practice:** Document all categories, but link them together in a cohesive
feature doc that references the architecture decisions and dependencies.
