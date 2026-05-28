# Extracted Constitution Patterns

Normalized patterns extracted from real project constitutions. Use these as building blocks.

## Table of Contents
1. [Preamble Examples](#preamble-examples)
2. [Core Principle Templates](#core-principle-templates)
3. [Development Standards](#development-standards)
4. [Technical Standards](#technical-standards)
5. [Naming Conventions](#naming-conventions)
6. [Voice & Tone](#voice--tone)
7. [Governance Templates](#governance-templates)

---

## Preamble Examples

### For Personal Tools
> Ship it. Use it. Fix what hurts. Repeat.
>
> We build tools to eliminate friction in development environments, not to achieve theoretical perfection. Every interaction should feel effortless, predictable, and occasionally delightful.

### For Hackathons
> This is a hackathon project. Speed is critical, but not at the cost of a foundation that needs immediate rewriting. Build the MVP fast with practices that won't embarrass you if this continues. Good enough to ship, good enough to evolve.

### For Production Systems
> [Project] prioritizes performance and reliability. All code contributions MUST consider performance implications and operational excellence.

### For Team Projects
> We build for clarity and maintainability. Code should be understandable without requiring the original author's consultation.

---

## Core Principle Templates

### Ship Fast, Fix What Hurts
**Build the smallest useful thing, dogfood it immediately, iterate based on real pain.**

- **Dogfood Relentlessly**: Use the tool daily. If you're not using it, you're guessing.
- **Fix Actual Friction**: Prioritize real annoyances over hypothetical edge cases.
- **Get It Working First**: Working with mediocre quality beats perfect that doesn't exist.
- **Refactor When It Hurts**: When velocity suffers or code is genuinely hard to understand. Not because it "feels messy."
- **Premature Optimization is Evil**: Don't optimize until real usage proves there's a problem.

**Rationale**: Shipping working software creates value. Optimizing non-existent or broken software wastes time.

---

### Build for Joy, Not Scale
**Personal tool used daily. Every interaction should feel effortless, predictable, and occasionally delightful.**

- **Good Enough Ships**: Perfect is the enemy of done.
- **Responsive & Predictable**: Clean invocation, useful results, actionable errors.
- **Anticipate Needs**: Design with empathy. What saves 30 seconds fifty times a day?
- **Don't Gold-Plate**: Ship, iterate, polish what matters.

**Rationale**: Tools you lean on daily should feel like a well-worn keyboard—responsive, predictable, occasionally surprising you with how well they anticipate your needs.

---

### Simplicity & Pragmatism (KISS & YAGNI)
**Do the simplest thing that could possibly work. Resist architecting for scenarios that don't exist yet.**

- **No Speculative Features**: Build when needed, not "just in case."
- **Minimal Complexity**: If you can't explain it in one sentence, it's too complex.
- **Dependencies Must Earn Their Keep**: Every package must solve a real, immediate problem.
- **Embrace Good Enough**: Ship working software, not perfect architecture.

**Rationale**: Simplicity enables fast iteration, easier maintenance, and clearer reasoning. Complexity is the primary source of bugs.

---

### Make It Work, Then Make It Fast
**Correctness and utility always come first. Performance is a feature, not a prerequisite.**

- **Correctness First**: Working functionality before performance tuning.
- **No Premature Optimization**: Avoid complexity for theoretical gains.
- **Measure Before Optimizing**: Don't guess what's slow, profile it.
- **"Fast Enough" is Good Enough**: Until users complain.

**What to defer**: Performance benchmarks, SLAs, caching layers, query optimization.
**What NOT to defer**: Security, data integrity, clear error messages.

**Rationale**: Most performance problems don't exist until measured. Premature optimization wastes time and adds complexity.

---

### Modularity & Single Responsibility
**Every component MUST do one thing and do it well.**

- **Single Purpose**: Clear responsibility per component.
- **Composable Design**: Complex workflows from simple, atomic parts.
- **Clarity in Naming**: Unambiguous names. `code-compiler` not `smart-helper`.
- **No Circular Dependencies**: Explicit, minimized cross-component dependencies.

**Rationale**: Predictability through clarity. Single purpose makes debugging, testing, and extension straightforward.

---

### User Experience First
**Design for humans, then automation.**

- **Frictionless Setup**: One command to install, one to run.
- **Human-Readable Errors**: "API connection failed: returned 503. Check network." Not "ECONNREFUSED."
- **Actionable Feedback**: Every error suggests what to do next.
- **Empathetic Design**: Assume user is frustrated and in a hurry.

**Rationale**: Friction kills adoption. If it's annoying to use, it won't be used.

---

### Performance First (Production Systems)
**Prioritize performance in critical paths.**

- Transaction finality target: ~Xms
- Code MUST NOT introduce unnecessary latency in critical paths
- Performance-critical code MUST be benchmarked before merge
- Memory allocations in hot paths MUST be minimized or justified
- Async operations MUST NOT block the runtime

**Rationale**: Performance degradation directly impacts user experience and competitiveness.

---

### Unix Philosophy (CLI Tools)
**Every command follows Unix fundamentals.**

- **Single tool, single purpose**: Each command does one thing well.
- **Text I/O**: stdin, args, or files for input; stdout/stderr for output.
- **Composable output**: Human-readable default, `--json` for structured.
- **Predictable exit codes**: 0 success, non-zero failure.
- **Pipeable design**: Chain commands naturally.

**Rationale**: Unix conventions ensure seamless integration with tools, scripts, and workflows.

---

### Demo-First Development (Hackathons)
**Every feature must be demo-able at every checkpoint.**

- **UI Gets Attention**: Polish the screens you'll demo.
- **Happy Path Priority**: Main flow first, obvious errors only, skip exotic edge cases.
- **Basic Validation**: Don't skip entirely. Prevent demo crashes.
- **Testing Is Optional**: Manual testing fine. Automated only if it saves time.

**Rationale**: Judges and users respond to working software. Build what you can show.

---

## Development Standards

### Commit Standards (Conventional Commits)

Format: `<type>(<scope>): <subject>`

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: No behavior change
- `test`: Adding/updating tests
- `chore`: Maintenance, deps, tooling
- `perf`: Performance improvement

**Rules:**
- Imperative mood ("add" not "added")
- Lowercase first letter
- No period at end
- Max 72 characters

**Example**: `feat(search): add hybrid search with keyword fallback`

---

### Testing Standards

**Integration Tests First:**
- Test real workflows against real environments
- Mocks only for: destructive ops, costly APIs, specific error states
- If tests pass but real integration fails, tests are useless

**Test What Matters:**
- Critical paths, not coverage metrics
- Easy to run locally before pushing
- Flaky tests get fixed or deleted immediately

**Dogfooding is Testing:**
- Daily use by developer is valid testing

---

### Testing Tiers

**Priority 1 (MUST TEST):**
- Security-critical functions
- Payment/financial logic
- Core business rules

**Priority 2 (ONLY IF REQUESTED):**
- Response formatting
- Error handling paths
- Edge cases

**Priority 3 (SKIP FOR HACKATHON):**
- UI components
- Configuration loading
- Demo scripts

---

## Technical Standards

### Error Handling

- **Fail Loudly & Clearly**: Say what failed, why, and what to do.
- **No Silent Failures**: Log errors, surface to user, provide context.
- **Graceful Degradation**: If service is down, say so clearly.

**Error Format:**
```
✗ Failed to [action]: [specific reason]

Try: [suggested fix command]
Or: [alternative solution]

More info: [link to docs]
```

---

### Configuration

- **Externalize Config**: Environment-specific values configurable.
- **Sane Defaults**: Work out-of-box for 80% of users.
- **Zero-Config UX**: Advanced users can tweak if needed.
- **No Hardcoded Secrets**: Environment variables only.

---

### Documentation

- **README First**: Installation, setup, basic usage.
- **Code Comments**: The *why*, not the *what*.
- **Self-Documenting Code**: Clear naming > comments.

---

## Naming Conventions

### General Rules
- Lowercase, kebab-case: `my-project` not `MyProject`
- Descriptive over clever: `code-compiler` not `smart-helper`
- No corporate jargon

### CLI Commands
- Namespace with colons: `namespace:action`
- Short aliases: `ns:a`
- Example: `agent:create` → `ag:c`

### Files
- kebab-case for directories and files
- Match directory name in module files
- One primary concept per file
- Max 300 lines (split if longer)

---

## Voice & Tone

### Documentation
- **Conversational but precise**: "This queries your knowledge base" not "This facilitates knowledge retrieval operations"
- **Active voice**: "The compiler detects" not "are detected by"
- **No corporate-speak**: Avoid "leverage," "utilize," "synergize"
- **Builder language**: "Ship it," "dogfood," "it just works"

### Error Messages
- **Direct & actionable**: Say what's wrong and how to fix
- **No blame**: Not "You forgot" but "Missing X. Try Y."
- **Context-aware**: Specific to the actual failure

### Code Comments
- **Comment the why**: `// Cache indefinitely since blocks are immutable`
- **Not the what**: `// Set cache to true` (useless)
- **Personality allowed**: `// TODO: Janky but works. Refactor when it breaks.`

---

## Governance Templates

### Amendment Procedure
- Changes MUST be documented with rationale
- Version MUST increment per semver:
  - **MAJOR**: Breaking principle changes/removals
  - **MINOR**: New principles/sections added
  - **PATCH**: Clarifications, wording fixes
- Dependent templates MUST be updated before ratification

### Compliance
- Constitution supersedes all other practices
- All PRs verify compliance
- Complexity requires explicit justification
- Deviations documented in PR description

### Version Footer
```
**Version**: X.Y.Z | **Ratified**: YYYY-MM-DD | **Last Amended**: YYYY-MM-DD
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Example | Correct |
|--------------|---------|---------|
| Inconsistent casing | `My-Project`, `myProject` | `my-project` |
| Verbose names | `data-explorer-service-manager` | `data-explorer` |
| Corporate jargon | "facilitates workflows" | "makes development less painful" |
| Vague errors | "Operation failed" | "API returned 503: [url]" |
| Shouting | `SEARCH_QUERY` | `search-query` |
| Silent failures | catch and ignore | catch, log, return error |
| Testing mocks only | 100% mocked tests | Integration tests first |
