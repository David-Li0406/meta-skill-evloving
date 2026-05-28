# PRISM Best Practices

This document consolidates best practices for the PRISM methodology for effective AI-driven development.

## Core PRISM Principles

### The PRISM Framework

**P - Predictability**
- Structured processes with measurement
- Quality gates at each step
- PSP (Personal Software Process) tracking
- Clear acceptance criteria

**R - Resilience**
- Test-driven development (TDD)
- Graceful error handling
- Defensive programming
- Comprehensive test coverage

**I - Intentionality**
- Clear, purposeful code
- SOLID principles
- Clean Code practices
- Explicit over implicit

**S - Sustainability**
- Maintainable code
- Documentation that doesn't go stale
- Continuous improvement
- Technical debt management

**M - Maintainability**
- Domain-driven design where applicable
- Clear boundaries and interfaces
- Expressive naming
- Minimal coupling, high cohesion

## Guiding Principles

### 1. Lean Dev Agents

**Minimize Context Overhead:**
- Small files loaded on demand
- Story contains all needed info
- Never load PRDs/architecture unless directed
- Keep `devLoadAlwaysFiles` minimal

**Why:** Large context windows slow development and increase errors. Focused context improves quality.

### 2. Natural Language First

**Markdown Over Code:**
- Use plain English throughout
- No code in core workflows
- Instructions as prose, not programs
- Leverage LLM natural language understanding

**Why:** LLMs excel at natural language. Code-based workflows fight against their strengths.

### 3. Clear Role Separation

**Each Agent Has Specific Expertise:**
- Architect: System design
- PM/PO: Requirements and stories
- Dev: Implementation
- QA: Quality and testing
- SM: Epic decomposition and planning

**Why:** Focused roles prevent scope creep and maintain quality.

## Architecture Best Practices

### DO:

✅ **Start with User Journeys**
- Understand user needs before technology
- Work backward from experience
- Map critical paths

✅ **Document Decisions and Trade-offs**
- Why this choice over alternatives?
- What constraints drove decisions?
- What are the risks?

✅ **Include Diagrams**
- System architecture diagrams
- Data flow diagrams
- Deployment diagrams
- Sequence diagrams for critical flows

✅ **Specify Non-Functional Requirements**
- Performance targets
- Security requirements
- Scalability needs
- Reliability expectations

✅ **Plan for Observability**
- Logging strategy
- Metrics and monitoring
- Alerting thresholds
- Debug capabilities

✅ **Choose Boring Technology Where Possible**
- Proven, stable technologies for foundations
- Exciting technology only where necessary
- Consider team expertise

✅ **Design for Change**
- Modular architecture
- Clear interfaces
- Loose coupling
- Feature flags for rollback

### DON'T:

❌ **Over-engineer for Hypothetical Futures**
- YAGNI (You Aren't Gonna Need It)
- Build for current requirements
- Make future changes easier, but don't implement them now

❌ **Choose Technology Based on Hype**
- Evaluate objectively
- Consider maturity and support
- Match to team skills

❌ **Neglect Security and Performance**
- Security must be architected in
- Performance requirements drive design
- Don't defer these concerns

❌ **Create Documentation That Goes Stale**
- Living architecture docs
- Keep with code where possible
- Regular reviews and updates

❌ **Ignore Developer Experience**
- Complex setups hurt productivity
- Consider onboarding time
- Optimize for daily workflows

## Story Creation Best Practices

### DO:

✅ **Define Clear, Testable Acceptance Criteria**
```markdown
✅ GOOD:
- User can login with email and password
- Invalid credentials show "Invalid email or password" error
- Successful login redirects to dashboard

❌ BAD:
- Login works correctly
- Errors are handled
- User can access the system
```

✅ **Include Technical Context in Dev Notes**
- Relevant architecture decisions
- Integration points
- Performance considerations
- Security requirements

✅ **Break into Specific, Implementable Tasks**
- Each task is atomic
- Clear success criteria
- Estimated in hours
- Can be done in order

✅ **Size Appropriately (1-3 days)**
- Not too large (>8 points = split it)
- Not too small (<2 points = combine)
- Can be completed in one development session

✅ **Document Dependencies Explicitly**
- Technical dependencies (services, libraries)
- Story dependencies (what must be done first)
- External dependencies (APIs, third-party)

✅ **Link to Source Documents**
- Reference PRD sections
- Reference architecture docs
- Reference Jira epics

✅ **Set Status to "Draft" Until Approved**
- Requires user review
- May need refinement
- Not ready for development

### DON'T:

❌ **Create Vague or Ambiguous Stories**
- "Improve performance" ← What does this mean?
- "Fix bugs" ← Which ones?
- "Update UI" ← Update how?

❌ **Skip Acceptance Criteria**
- Every story needs measurable success
- AC drives test design
- AC enables validation

❌ **Make Stories Too Large**
- >8 points is too large
- Split along feature boundaries
- Maintain logical cohesion

❌ **Forget Dependencies**
- Hidden dependencies cause delays
- Map all prerequisites
- Note integration points

❌ **Mix Multiple Features in One Story**
- One user need per story
- Clear single purpose
- Easier to test and validate

❌ **Approve Without Validation**
- Run validation checklist
- Ensure completeness
- Verify testability

## Development Best Practices

### Test-Driven Development (TDD)

**Red-Green-Refactor:**
1. **Red**: Write failing test first
2. **Green**: Implement minimal code to pass
3. **Refactor**: Improve code while keeping tests green

**Benefits:**
- Tests actually verify behavior (you saw them fail)
- Better design (testable code is better code)
- Confidence in changes
- Living documentation

**Example:**
```
1. Write test: test_user_login_with_valid_credentials()
2. Run test → FAILS (no implementation)
3. Implement login functionality
4. Run test → PASSES
5. Refactor: Extract validation logic
6. Run test → Still PASSES
```

### Clean Code Principles

✅ **Meaningful Names**
```python
# ✅ GOOD
def calculate_monthly_payment(principal, rate, term_months):
    return principal * rate / (1 - (1 + rate) ** -term_months)

# ❌ BAD
def calc(p, r, t):
    return p * r / (1 - (1 + r) ** -t)
```

✅ **Small Functions**
- One responsibility per function
- Maximum 20-30 lines
- Single level of abstraction

✅ **No Magic Numbers**
```python
# ✅ GOOD
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30

# ❌ BAD
if retries > 3:  # What's 3? Why 3?
    time.sleep(30)  # Why 30?
```

✅ **Explicit Error Handling**
```python
# ✅ GOOD
try:
    result = api.call()
except APIError as e:
    logger.error(f"API call failed: {e}")
    return fallback_response()

# ❌ BAD
try:
    result = api.call()
except:
    pass
```

### SOLID Principles

**S - Single Responsibility Principle**
- Class has one reason to change
- Function does one thing
- Module has cohesive purpose

**O - Open/Closed Principle**
- Open for extension
- Closed for modification
- Use composition and interfaces

**L - Liskov Substitution Principle**
- Subtypes must be substitutable for base types
- Maintain contracts
- Don't break expectations

**I - Interface Segregation Principle**
- Many specific interfaces > one general interface
- Clients shouldn't depend on unused methods
- Keep interfaces focused

**D - Dependency Inversion Principle**
- Depend on abstractions, not concretions
- High-level modules don't depend on low-level
- Both depend on abstractions

### Story Implementation

✅ **Update Story File Correctly**
- ONLY update Dev Agent Record sections
- Mark tasks complete when ALL tests pass
- Update File List with every change
- Document issues in Debug Log

✅ **Run Full Regression Before Completion**
- All tests must pass
- No skipped tests
- Linting clean
- Build successful

✅ **Track PSP Accurately**
- Set Started timestamp when beginning
- Set Completed when done
- Calculate Actual Hours
- Compare to estimates for improvement

### DON'T:

❌ **Modify Restricted Story Sections**
- Don't change Story content
- Don't change Acceptance Criteria
- Don't change Testing approach
- Only Dev Agent Record sections

❌ **Skip Tests or Validations**
- Tests are not optional
- Validations must pass
- No "TODO: add tests later"

❌ **Mark Tasks Complete With Failing Tests**
- Complete = ALL validations pass
- Includes unit + integration + E2E
- No exceptions

❌ **Load External Docs Without Direction**
- Story has what you need
- Don't load PRD "just in case"
- Keep context minimal

❌ **Implement Without Understanding**
- If unclear, ask user
- Don't guess requirements
- Better to HALT than implement wrong

## Testing Best Practices

### Test Level Selection

**Unit Tests - Use For:**
- Pure functions
- Business logic
- Calculations and algorithms
- Validation rules
- Data transformations

**Integration Tests - Use For:**
- Component interactions
- Database operations
- API endpoints
- Service integrations
- Message queue operations

**E2E Tests - Use For:**
- Critical user journeys
- Cross-system workflows
- Compliance requirements
- Revenue-impacting flows

### Test Priorities

**P0 - Critical (>90% coverage):**
- Revenue-impacting features
- Security paths
- Data integrity operations
- Compliance requirements
- Authentication/authorization

**P1 - High (Happy path + key errors):**
- Core user journeys
- Frequently used features
- Complex business logic
- Integration points

**P2 - Medium (Happy path + basic errors):**
- Secondary features
- Admin functionality
- Reporting and analytics

**P3 - Low (Smoke tests):**
- Rarely used features
- Cosmetic improvements
- Nice-to-have functionality

### Test Quality Standards

✅ **No Flaky Tests**
- Tests must be deterministic
- No random failures
- Reproducible results

✅ **Dynamic Waiting**
```python
# ✅ GOOD
wait_for(lambda: element.is_visible(), timeout=5)

# ❌ BAD
time.sleep(5)  # What if it takes 6 seconds? Or 2?
```

✅ **Stateless and Parallel-Safe**
- Tests don't depend on order
- Can run in parallel
- No shared state

✅ **Self-Cleaning Test Data**
- Setup in test
- Cleanup in test
- No manual database resets

✅ **Explicit Assertions in Tests**
```python
# ✅ GOOD
def test_user_creation():
    user = create_user("test@example.com")
    assert user.email == "test@example.com"
    assert user.is_active is True

# ❌ BAD
def test_user_creation():
    user = create_user("test@example.com")
    verify_user(user)  # Assertion hidden in helper
```

### Test Anti-Patterns

❌ **Testing Mock Behavior**
- Test real code, not mocks
- Mocks should simulate real behavior
- Integration tests often better than heavily mocked unit tests

❌ **Production Pollution**
- No test-only methods in production code
- No test-specific conditionals
- Keep test code separate

❌ **Mocking Without Understanding**
- Understand what you're mocking
- Know why you're mocking it
- Consider integration test instead

## Quality Assurance Best Practices

### Risk Assessment (Before Development)

✅ **Always Run for Brownfield**
- Legacy code = high risk
- Integration points = complexity
- Use risk-profile task

✅ **Score by Probability × Impact**

**Risk Score Formula**: Probability (1-9) × Impact (1-9)

**Probability Factors:**
- Code complexity (higher = more likely to have bugs)
- Number of integration points (more = higher chance of issues)
- Developer experience level (less experience = higher probability)
- Time constraints (rushed = more bugs)
- Technology maturity (new tech = higher risk)

**Impact Factors:**
- Number of users affected (more users = higher impact)
- Revenue impact (money at stake)
- Security implications (data breach potential)
- Compliance requirements (legal/regulatory)
- Business process disruption (operational impact)

**Risk Score Interpretation:**
- **1-9**: Low risk - Basic testing sufficient
- **10-29**: Medium risk - Standard testing required
- **30-54**: High risk - Comprehensive testing needed
- **55+**: Critical risk - Extensive testing + design review

**Gate Decisions by Risk Score:**
- Score ≥9 on any single risk = FAIL gate (must address before proceeding)
- Score ≥6 on multiple risks = CONCERNS gate (enhanced testing required)

✅ **Document Mitigation Strategies**
- How to reduce risk (technical approaches)
- What testing is needed (test coverage requirements)
- What monitoring to add (observability needs)
- Rollback procedures (safety nets)

### Test Design (Before Development)

✅ **Create Comprehensive Strategy**
- Map all acceptance criteria
- Choose appropriate test levels
- Assign priorities (P0/P1/P2/P3)

✅ **Avoid Duplicate Coverage**
- Unit for logic
- Integration for interactions
- E2E for journeys
- Don't test same thing at multiple levels

✅ **Plan Regression Tests for Brownfield**
- Existing functionality must still work
- Test touchpoints with legacy
- Validate backward compatibility

### Requirements Tracing (During Development)

✅ **Map Every AC to Tests**
- Given-When-Then scenarios
- Traceability matrix
- Audit trail

✅ **Identify Coverage Gaps**
- Missing test scenarios
- Untested edge cases
- Incomplete validation

### Review (After Development)

✅ **Comprehensive Analysis**
- Code quality
- Test coverage
- Security concerns
- Performance issues

✅ **Active Refactoring**
- QA can suggest improvements
- Not just finding problems
- Collaborative quality

✅ **Advisory, Not Blocking**
- PASS/CONCERNS/FAIL/WAIVED gates
- Teams set their quality bar
- Document trade-offs

### Quality Gate Decisions

**PASS** ✅ - All criteria met, ready for production

Criteria:
- All acceptance criteria tested
- Test coverage adequate for risk level
- No critical or high severity issues
- NFRs validated
- Technical debt acceptable

**CONCERNS** ⚠️ - Issues exist but not blocking

When to use:
- Minor issues that don't block release
- Technical debt documented for future
- Nice-to-have improvements identified
- Low-risk issues with workarounds
- Document clearly what concerns exist

**FAIL** ❌ - Blocking issues must be fixed

Blocking criteria:
- Acceptance criteria not met
- Critical/high severity bugs
- Security vulnerabilities
- Performance unacceptable
- Missing required tests
- Technical debt too high
- Clear action items required

**WAIVED** 🔓 - Issues acknowledged, explicitly waived

When to use:
- User accepts known issues
- Conscious technical debt decision
- Time constraints prioritized
- Workarounds acceptable
- Require explicit user approval with documentation

## Brownfield Best Practices

### Always Document First

✅ **Run document-project**
- Even if you "know" the codebase
- AI agents need context
- Discover undocumented patterns

### Respect Existing Patterns

✅ **Match Current Style**
- Coding conventions
- Architectural patterns
- Technology choices
- Team preferences

### Plan for Gradual Rollout

✅ **Feature Flags**
- Toggle new functionality
- Enable rollback
- Gradual user migration

✅ **Backwards Compatibility**
- Don't break existing APIs
- Support legacy consumers
- Migration paths

✅ **Migration Scripts**
- Data transformations
- Schema updates
- Rollback procedures

### Test Integration Thoroughly

✅ **Enhanced QA for Brownfield**
- ALWAYS run risk assessment first
- Design regression test strategy
- Test all integration points
- Validate performance unchanged

**Critical Brownfield Sequence:**
```
1. QA: *risk {story}        # FIRST - before any dev
2. QA: *design {story}      # Plan regression tests
3. Dev: Implement
4. QA: *trace {story}       # Verify coverage
5. QA: *nfr {story}         # Check performance
6. QA: *review {story}      # Deep integration analysis
```

## Process Best Practices

### Multiple Focused Tasks > One Branching Task

**Why:** Keeps developer context minimal and focused

✅ **GOOD:**
```
- Task 1: Create User model
- Task 2: Implement registration endpoint
- Task 3: Add email validation
- Task 4: Write integration tests
```

❌ **BAD:**
```
- Task 1: Implement user registration
  - Create model
  - Add endpoint
  - Validate email
  - Write tests
  - Handle errors
  - Add logging
  - Document API
```

### Reuse Templates

✅ **Use create-doc with Templates**
- Maintain consistency
- Proven structure
- Embedded generation instructions

❌ **Don't Create Template Duplicates**
- One template per document type
- Customize through prompts, not duplication

### Progressive Loading

✅ **Load On-Demand**
- Don't load everything at activation
- Load when command executed
- Keep context focused

❌ **Don't Front-Load Context**
- Overwhelming context window
- Slower processing
- More errors

### Human-in-the-Loop

✅ **Critical Checkpoints**
- PRD/Architecture: User reviews before proceeding
- Story drafts: User approves before dev
- QA gates: User decides on CONCERNS/WAIVED

❌ **Don't Blindly Proceed**
- Ambiguous requirements → HALT and ask
- Risky changes → Get approval
- Quality concerns → Communicate

## Anti-Patterns to Avoid

### Development Anti-Patterns

❌ **"I'll Add Tests Later"**
- Tests are never added
- Code becomes untestable
- TDD prevents this

❌ **"Just Ship It"**
- Skipping quality gates
- Incomplete testing
- Technical debt accumulates

❌ **"It Works On My Machine"**
- Environment-specific behavior
- Not reproducible
- Integration issues

❌ **"We'll Refactor It Later"**
- Later never comes
- Code degrades
- Costs compound

### Testing Anti-Patterns

❌ **Testing Implementation Instead of Behavior**
```python
# ❌ BAD - Testing implementation
assert user_service._hash_password.called

# ✅ GOOD - Testing behavior
assert user_service.authenticate(email, password) is True
```

❌ **Sleeping Instead of Waiting**
```javascript
// ❌ BAD
await sleep(5000);
expect(element).toBeVisible();

// ✅ GOOD
await waitFor(() => expect(element).toBeVisible());
```

❌ **Shared Test State**
```python
# ❌ BAD
class TestUser:
    user = None  # Shared across tests!

    def test_create_user(self):
        self.user = User.create()

    def test_user_login(self):
        # Depends on test_create_user running first!
        self.user.login()

# ✅ GOOD
class TestUser:
    def test_create_user(self):
        user = User.create()
        assert user.id is not None

    def test_user_login(self):
        user = User.create()  # Independent!
        assert user.login() is True
```

### Process Anti-Patterns

❌ **Skipping Risk Assessment on Brownfield**
- Hidden dependencies
- Integration failures
- Regression bugs

❌ **Approval Without Validation**
- Incomplete stories
- Vague requirements
- Downstream failures

❌ **Loading Context "Just In Case"**
- Bloated context window
- Slower processing
- More errors

❌ **Ignoring Quality Gates**
- Accumulating technical debt
- Production issues
- Team frustration

## Summary: The Path to Excellence

### For Architects:
1. Start with user needs
2. Choose pragmatic technology
3. Document decisions and trade-offs
4. Design for change
5. Plan observability from the start

### For Product Owners:
1. Clear, testable acceptance criteria
2. Appropriate story sizing (1-3 days)
3. Explicit dependencies
4. Technical context for developers
5. Validation before approval

### For Developers:
1. TDD - tests first, always
2. Clean Code and SOLID principles
3. Update only authorized story sections
4. Full regression before completion
5. Keep context lean and focused

### For QA:
1. Risk assessment before development (especially brownfield)
2. Test design with appropriate levels and priorities
3. Requirements traceability
4. Advisory gates, not blocking
5. Comprehensive review with active refactoring

### For Everyone:
1. Follow PRISM principles (Predictability, Resilience, Intentionality, Sustainability, Maintainability)
2. Lean dev agents, natural language first, clear roles
3. Progressive loading, human-in-the-loop
4. Quality is everyone's responsibility
5. Continuous improvement through measurement

---

**Last Updated**: 2025-10-22
