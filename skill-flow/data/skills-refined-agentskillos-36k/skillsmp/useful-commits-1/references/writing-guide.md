# Writing Good Commit Messages: A Philosophy

## Core Philosophy

A commit message is a communication tool. Write for readers who don't have your context—future you, teammates, bug investigators, and anyone using `git blame` or `git bisect`. Focus on information content: what changed, why it changed, and what effects it has.

## What Makes a Commit Message Good?

### Information Over Style

Good commit messages prioritize substance over formatting. While structure matters (Conventional Commits format), the real value lies in what you communicate:

**Information content:**
- What changed in user-visible behavior
- Why the change was needed
- What problem it solves
- What effects it has

**Not:**
- Perfect grammar
- Literary flair
- Stylistic flourishes

### Clarity Without Context

Assume the reader does not have access to:
- The story or ticket that prompted the change
- The discussion that led to this solution
- The code review comments
- Your intimate knowledge of why this matters

**Your commit message is often the only documentation that survives.**

## Questions to Answer

Before writing a commit message, consider:

1. **Why have I made these changes?**
   - What problem does this solve?
   - What was broken or missing?
   - Why is this change necessary?

2. **What effect have my changes made?**
   - How does the program behave differently?
   - What is now possible that wasn't before?
   - What works that was broken?

3. **Why was the change needed?**
   - What was the root cause?
   - Why was the existing approach insufficient?
   - What constraints or requirements drove this?

4. **What are the changes in reference to?**
   - Related issues or PRs?
   - Previous attempts to fix this?
   - Dependencies on other changes?

## Writing Principles

### 1. Don't Expect Code to Be Self-Explanatory

What seems obvious to you now won't be obvious in 6 months. Code shows *what* changed, but rarely explains *why*.

**Bad:**
```
fix: add margin
```

**Good:**
```
fix: add margin to nav items to prevent overlapping the logo

Navigation items were rendering too close to the logo on smaller
screens, causing visual overlap. Add 16px margin to create proper
spacing.
```

**Why good:** Explains the problem (overlap), the symptom (visual issue on small screens), and the solution (16px margin).

### 2. Make It Clear Why the Change Was Needed

State the problem being solved, not just what was done.

**Bad:**
```
refactor: update user component
```
Doesn't explain why or what improvement was made.

**Good:**
```
refactor: extract user validation logic to separate service

Move validation logic from UserComponent to UserValidationService
to enable reuse across registration and profile edit flows. This
eliminates duplicated validation code and ensures consistent rules.
```

**Why good:** Explains the motivation (code reuse), the benefit (eliminates duplication), and the impact (consistent rules).

### 3. Include What Changed + Why

Don't assume the reader understands the context. You may have access to a detailed specification, but they don't.

**Bad:**
```
perf: add caching
```

**Good:**
```
perf: cache user preferences to reduce database queries

User preferences were being fetched on every page load, causing
unnecessary database queries. Implement in-memory cache with 5-minute
TTL to reduce database load by ~80%.
```

**Why good:** Describes the problem (repeated queries), the solution (caching), and the measurable impact (80% reduction).

### 4. Describe User-Visible Changes

Explain how the program behaves differently from the user's perspective. This helps readers understand the impact without reading the patch.

**Example:**
```
fix(ui): correct tab navigation order in settings dialog

Tab key now moves through form fields in logical order (top to
bottom) instead of jumping randomly. This fixes keyboard navigation
for accessibility.
```

This tells users exactly what they'll experience differently.

### 5. Provide Rationale and Context

Explain *why* this change matters, including:
- The problem being solved
- Why this solution is appropriate
- Future work that depends on this
- Known side effects and why they're acceptable

**Example:**
```
refactor(api): switch from callbacks to promises

Migrate all API methods from callback-based to promise-based for
better error handling and async/await compatibility. This is
preparation for introducing async request batching in v3.0.

Note: This doesn't change external API since callbacks are still
supported via compatibility wrapper.
```

## Structural Guidelines

### Use Pyramid Structure

Place the most important information first, ordered by audience breadth:

1. **Subject line**: Most distinctive, specific identifier
2. **First paragraph**: User-visible changes and primary impact
3. **Second paragraph**: Technical rationale and implementation details
4. **Later paragraphs**: Background, alternatives considered, future work

Readers can stop when they've found what they need. Don't bury the key information.

**Example:**
```
feat(api): add rate limiting to authentication endpoints

Authentication endpoints now limit requests to 5 per minute per IP
to prevent brute force attacks. Exceeding the limit returns 429
status code with Retry-After header.

Implementation uses token bucket algorithm with Redis for distributed
rate limiting across multiple API servers. Configuration is available
via RATE_LIMIT_* environment variables.

This addresses the security audit finding from Q4 2024 (AUDIT-234).
Future work includes adding user-specific rate limits (per account
rather than per IP) for authenticated requests.
```

Order: user impact → technical approach → context → future work.

### Be Explicit About Before vs. After

Use clear markers like "Previously," "Before this change," or "Now" rather than relying on verb tense alone.

**Unclear:**
```
The parser handles nested objects.
```
Is this what it does now, or what it did before?

**Clear:**
```
Previously, the parser rejected nested objects. Now it handles them
correctly by recursively processing each level.
```

### Write Distinctive Subject Lines

The subject line should uniquely identify the commit when viewed in `git log --oneline`. Generic descriptions don't help:

**Too generic:**
```
fix: bug fix
refactor: code cleanup
feat: add feature
```

**Distinctive:**
```
fix(auth): prevent token leakage in error responses
refactor(parser): extract JSON validation to separate module
feat(billing): add Stripe subscription webhooks
```

Include function names, component names, or specific identifiers.

## Special Considerations

### Complex Patches: Guide the Reader

For large or complex changes, explain the patch structure:

```
refactor: restructure authentication system

This refactor extracts authentication into three new modules:

1. TokenService - JWT generation and validation
2. SessionStore - Redis-backed session storage
3. AuthMiddleware - Express middleware for route protection

Note: The UserService changes are minimal in this commit, focusing
only on integration with the new TokenService. Full UserService
refactoring is planned for next sprint.

Migration impact: Existing sessions remain valid, but new sessions
use the updated structure.
```

This helps reviewers know where to look and what to expect.

### External References

Link relevant context:

**Examples:**
```
Fixes #234
Refs: #456, #789
Related to PR #123
Implements RFC-001
Addresses CVE-2024-12345
Based on: https://tools.ietf.org/html/rfc7519
```

These create a paper trail and help future investigators understand the full context.

### Known Side Effects

If you're aware of side effects, mention them and explain why they're acceptable:

```
perf(api): add response caching

Cache GET requests for 60 seconds to reduce database load during
traffic spikes. This improves response time from ~200ms to ~10ms
for cached requests.

Note: This introduces eventual consistency for read operations.
Data may be up to 60 seconds stale during the cache window. This
is acceptable for our use case since data doesn't change frequently
and staleness is preferable to timeout errors during high load.
```

Acknowledging trade-offs demonstrates thoughtfulness.

## Who Reads Your Commits?

Understanding your audience shapes what to include:

### Project Users
Want to know if updates affect their workflow. Focus on behavior changes and new capabilities.

### Bug Investigators
Using `git bisect` to find where issues were introduced. Need to distinguish intended changes from side effects.

### Code Reviewers
Evaluating safety and necessity. Need rationale and context to assess the change.

### Teammates
Staying informed about codebase evolution. Need to understand the "why" behind changes.

### Release Managers
Deciding what to cherry-pick or backport. Need to understand dependencies and impact.

### Archaeologists
Understanding historical decisions months or years later. Need complete context since they can't ask you.

### Your Future Self
"What was I thinking?" when debugging at 2am. Need clear rationale and known issues.

## Practical Strategies

### Think Like a News Article

**Headline (subject line):** Sum up what happened and what is important
- Make it distinctive and specific
- Include identifiers (function names, component names)
- Focus on the most critical aspect

**Lead paragraph (first body paragraph):** Answer who, what, when, where, why
- User-visible changes
- Primary impact
- Immediate consequences

**Body paragraphs (remaining):** Additional details in descending importance
- Technical rationale
- Implementation details
- Background and context
- Future work

### Check for Logical Separation

If it's difficult to summarize the commit within character limits, you may be combining multiple logical changes:

**Signs of over-packed commits:**
- Hard to write a specific subject line
- Body keeps saying "Also, ..." or "Additionally, ..."
- Multiple unrelated files changed
- Would be easier to write multiple messages

**Solution:**
Use `git add -p` to stage changes interactively and create multiple focused commits.

### Answer the "Why" Explicitly

Every commit should answer: "Why was this change necessary?"

**Bad (missing why):**
```
refactor: move validation to utils
```

**Good (includes why):**
```
refactor: move validation to utils for reuse across components

Extract email validation logic from UserForm to shared utils to
enable reuse in ProfileEdit and AdminPanel. This ensures consistent
validation rules across all forms.
```

### Pretend You're Explaining to Someone Who Wasn't There

Imagine explaining the change to a new team member who wasn't in the meetings, didn't read the spec, and doesn't have your context.

What would they need to know to understand:
- What the code now does?
- Why it does it that way?
- What problem it solves?

## Common Pitfalls

### Pitfall 1: Vague Descriptions

❌ **Bad:**
```
fix: fix bug
update: update code
refactor: clean up
```

✅ **Good:**
```
fix: prevent race condition in event handlers
update: upgrade React from 17 to 18 for concurrent rendering
refactor: extract validation logic to separate service
```

### Pitfall 2: Missing Context

❌ **Bad:**
```
fix: add null check
```
Why was the null check needed? What was breaking?

✅ **Good:**
```
fix: add null check to prevent crash when user has no avatar

Users without profile pictures caused a null reference exception
when rendering the avatar component. Add null check and display
default placeholder avatar instead.

Fixes #234
```

### Pitfall 3: Assuming Code Is Self-Documenting

❌ **Bad:**
```
refactor: update UserService
```
The code shows what changed, but not why.

✅ **Good:**
```
refactor: extract user validation to support admin overrides

Move validation from UserService to UserValidator to enable
admin users to bypass certain validation rules when creating
accounts on behalf of customers.
```

### Pitfall 4: Describing Implementation Instead of Intent

❌ **Bad:**
```
feat: add if statement to check condition
```

✅ **Good:**
```
feat: skip email validation for admin-created accounts

Allow administrators to create accounts without email validation
when onboarding enterprise customers who use SSO. Email is still
required but doesn't need verification link.
```

### Pitfall 5: Too Much Verbosity Without Substance

❌ **Bad:**
```
fix: fix the really bad bug in the authentication system that was
causing all sorts of problems for users when they tried to log in
and it wouldn't work properly and kept showing error messages
```

✅ **Good:**
```
fix: prevent infinite redirect loop on authentication failure

Authentication errors caused redirect to /login, which redirected
back to /auth, creating infinite loop. Break the loop by adding
explicit error state handling.
```

## Line Wrapping and Format

### Why Wrap Lines?

Many tools display commit messages without reformatting:
- `git log` in terminal
- SSH sessions
- Email patches
- Offline repositories
- Plain text editors

Hard-wrapped text at 72-80 characters ensures readability across all environments.

### Markdown Considerations

If using Markdown idioms (backticks, emphasis), ensure text remains readable without rendering:

**Good (readable without rendering):**
```
Update `UserService.create()` to require email parameter.
```

**Bad (poor without rendering):**
```
Update UserService.create to require _email_ parameter with **validation**.
```

Tables should align in plain text:
```
Status | Count
-------|------
Active | 123
Paused | 45
```

## Incremental Improvement

You don't need to master everything at once. Consider adopting one improvement at a time:

1. **Week 1:** Make subject lines more distinctive
2. **Week 2:** Add explicit "why" reasoning
3. **Week 3:** Use "Previously" and "Now" markers
4. **Week 4:** Structure messages in pyramid form
5. **Week 5:** Check for logical separation before committing

Small iterative improvements compound into significantly better commit histories.

## Temporary Development Messages

During initial development, abbreviated messages are acceptable:

```
WIP: experimenting with new auth flow
fixup: oops forgot to save
temp: trying different approach
```

Use `git rebase -i` to rewrite these before sharing or merging to permanent history.

Once commits enter permanent history or are shared with others, proper messages become important.

## Summary

Good commit messages:
- **Inform** - Explain what, why, and effect
- **Contextualize** - Provide background and rationale
- **Guide** - Help readers navigate complex changes
- **Reference** - Link to related context
- **Anticipate** - Address questions before they're asked

Focus on information content over formatting perfection. A commit message is documentation that survives longer than code comments, bug tracker entries, or chat histories.

When in doubt, ask: "If I'm debugging this at 2am in 6 months, what would I need to know?"

Write that down.
