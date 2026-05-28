# Phase-by-Phase Guide

Comprehensive guidance for each discovery phase with questioning strategies, research approaches, and transition criteria.

## Phase 1: Problem Space Exploration

### Objective

Understand the problem deeply before proposing any solutions. Resist the temptation to jump to user stories—they will emerge naturally from understanding.

### Core Questions to Explore

#### The Problem Itself

- What problem are we solving?
- How do people experience this problem today?
- What triggers this problem or makes it worse?
- How frequently does this problem occur?
- What's the impact when this problem happens?
- What have people tried to solve this problem?
- Why haven't those solutions worked?

#### The People Affected

- Who experiences this problem most directly?
- Who else is affected by this problem?
- What roles do these people have?
- What are their goals in this context?
- What tools do they use today?
- What workflows does this problem interrupt?

#### Current vs. Desired State

- How do people work around this problem today?
- What pain points exist in current workarounds?
- What would success look like?
- How would we know if this problem is solved?
- What would change in people's daily work?

#### Constraints and Context

- What technical constraints exist?
- What business constraints affect this?
- Are there timeline or scope constraints?
- What are the non-negotiables?
- What's explicitly out of scope?

### Questioning Strategies

#### Open-Ended Questions

Start broad to avoid constraining thinking:

- "Tell me about how you currently handle [situation]"
- "Walk me through what happens when [trigger occurs]"
- "Describe a recent time when [problem] happened"

#### Follow-Up Probes

Dig deeper on interesting threads:

- "Can you give me a specific example?"
- "What makes that particularly challenging?"
- "How does that affect [other aspect]?"
- "What would need to change for that to work better?"

#### Quantifying Questions

Replace vague terms with specifics:

- "How often does this happen?" → "Daily, weekly, monthly?"
- "How many [entities] are involved?" → "Tens, hundreds, thousands?"
- "How long does [process] take?" → "Minutes, hours, days?"
- "How critical is this?" → "Blocks work, slows work, minor annoyance?"

#### Clarifying Questions

Ensure shared understanding:

- "When you say [term], do you mean [interpretation]?"
- "Is [entity A] the same as [entity B]?"
- "Does [workflow] always happen, or only when [condition]?"

### Research Approaches

#### Industry Pattern Research

Investigate how others solve similar problems:

- What products exist in this space?
- How do they approach this problem?
- What patterns are common?
- What patterns are emerging?
- What do users complain about in existing solutions?

#### Technical Pattern Research

Explore implementation approaches:

- What technologies are commonly used?
- What are the tradeoffs of different approaches?
- What are common pitfalls?
- What edge cases do others encounter?

#### Domain Knowledge Research

Build understanding of the domain:

- What's the standard terminology?
- What regulations or standards apply?
- What are industry best practices?
- What's the historical context?

### Capturing Understanding in STATE.md

#### Problem Statement Evolution

**Iteration 1** (rough):
"Users have trouble managing their tasks"

**Iteration 2** (more specific):
"Software development teams struggle to track work across multiple tools, leading to duplicate effort and missed dependencies"

**Iteration 3** (well-defined):
"Engineering teams working on features spanning 3+ services lose visibility into cross-service dependencies because each service team uses different tracking tools, resulting in integration issues discovered late in the development cycle"

#### Persona Identification

Start simple, add detail through conversation:

**Initial**:
| Persona | Description | Primary Goals |
|---------|-------------|---------------|
| Developer | Builds features | Complete assigned work |

**Refined**:
| Persona | Description | Primary Goals |
|---------|-------------|---------------|
| Feature Developer | Implements features spanning multiple services | Understand all dependencies, Coordinate with other teams, Deliver integrated feature |
| Service Owner | Maintains a specific service | Maintain service stability, Review incoming changes, Plan service roadmap |

#### Current vs. Desired State

**Current State**:
- Each service team uses different project management tools
- Dependencies discovered through Slack conversations
- Integration issues found during deployment
- No single source of truth for feature status

**Desired State**:
- Visibility into cross-service work
- Dependencies identified early
- Proactive integration testing
- Unified view of feature progress

#### Emerging Themes

As you understand the problem, themes will emerge:

- "Need to visualize dependencies across services"
- "Want to be notified about relevant changes"
- "Should track integration testing status"
- "Must see feature status across all services"

These are proto-stories—not fully formed yet, but they're emerging from understanding.

### Transition Criteria to Phase 2

Ready to move to Story Crystallization when:

- [ ] Problem statement is clear and user-confirmed
- [ ] Can articulate problem in one paragraph
- [ ] Primary personas identified
- [ ] Current vs. desired state mapped
- [ ] At least 2-3 clear themes emerging
- [ ] User agrees: "Yes, you understand the problem"

**Don't transition if**:
- Still discovering new aspects of the problem
- Personas remain vague or undefined
- Can't clearly articulate current pain points
- No themes have emerged yet

## Phase 2: Story Crystallization

### Objective

Transform emerging themes into concrete, prioritized user stories. Stories should be independently testable and valuable.

### From Themes to Stories

#### Story Structure

Every story needs:

**Actor** (Persona):
- Who is the primary user of this capability?
- Which persona does this serve?

**Goal** (What they want):
- What are they trying to accomplish?
- What capability do they need?

**Value** (So that...):
- Why does this matter?
- What benefit do they get?
- What problem does this solve?

**Example Transformation**:

**Theme**: "Need to visualize dependencies across services"

**Story**: "As a Feature Developer, I want to see which other services my feature depends on, so that I can coordinate with the relevant teams early and avoid late-stage integration issues"

#### Story Validation Questions

**Independence**:
- Can this story be tested without other stories?
- Does it deliver value on its own?
- Could we ship just this story?

**Testability**:
- How would we verify this is working?
- What would "done" look like?
- Can we describe specific test scenarios?

**Size**:
- Is this small enough to develop thoroughly?
- Or is this actually multiple stories?

**Value**:
- Why would a user care about this?
- What problem does it solve?
- What's the benefit?

### Prioritization

#### Priority Levels

**P1 (Must Have for MVP)**:
- Core value proposition
- Without this, the feature doesn't work
- Foundational capabilities

**P2 (Important but not MVP)**:
- Enhances core value
- Important for usability
- Can be added after P1

**P3 (Nice to Have)**:
- Polish and refinement
- Edge cases
- Future enhancements

#### Prioritization Questions

For each story, ask:

- "If we had to ship without this, would the feature still be valuable?"
- "Does this enable other stories, or depend on them?"
- "What's the impact if we delay this?"
- "How many users need this capability?"

### Dependency Mapping

Identify relationships between stories:

**Hard Dependencies**:
"Story B cannot exist without Story A"
```
Story A (View dependencies) ───► Story B (Get notifications about dependency changes)
```

**Soft Dependencies**:
"Story B is much better with Story A, but could work independently"
```
Story A (View dependencies)
Story B (Visualize on timeline) ~~~► Works better together
```

**Independent Stories**:
```
Story A (View dependencies)
Story C (Track testing status) ◄── No dependency
```

### Story Backlog Presentation

Present crystallized stories for user confirmation:

```markdown
Based on our discussion, here are the stories I've identified:

| # | Story | Actor | Goal | Value | Priority |
|---|-------|-------|------|-------|----------|
| 1 | View cross-service dependencies | Feature Developer | See which services my feature depends on | Coordinate early, avoid late integration issues | P1 |
| 2 | Get dependency change notifications | Feature Developer | Be notified when dependencies change | React quickly to changes affecting my work | P2 |
| 3 | Track integration test status | Feature Developer | See test results across services | Know when it's safe to deploy | P1 |
| 4 | Visualize feature timeline | Service Owner | See feature progress across services | Plan service changes accordingly | P2 |
| 5 | Export dependency graph | Feature Developer | Share dependency view with stakeholders | Communicate scope and complexity | P3 |

**Dependencies**:
- Story 2 builds on Story 1 (need to view dependencies before getting notifications)
- Story 3 is independent
- Story 4 is independent
- Story 5 builds on Story 1

Does this capture the right scope? Any stories missing? Do the priorities feel right?
```

### Refining the Backlog

Based on user feedback:

**Adding Stories**:
"You're right, we should also have: [new story]"
→ Add to backlog, discuss priority

**Splitting Stories**:
"Story 1 feels too big"
→ Break into Story 1A and 1B

**Merging Stories**:
"Stories 2 and 3 are really the same thing"
→ Combine into single story

**Reprioritizing**:
"Story 4 is actually more important than Story 3"
→ Adjust priorities

### Transition Criteria to Phase 3

Ready to move to Story Development when:

- [ ] Story backlog presented and discussed
- [ ] User confirmed: "Yes, these are the right stories"
- [ ] Priorities agreed upon
- [ ] Dependencies identified
- [ ] Each story passes independence/testability check
- [ ] Ready to deep-dive on highest priority story

**Don't transition if**:
- User uncertain about story scope
- Priorities not clear
- Major stories missing
- Stories too vague to develop

## Phase 3: Story Development (Iterative)

### Objective

Develop each story to graduation-ready clarity through focused questioning, research, and validation.

### Story Development Workflow

#### 1. Select Story by Priority

Always work on highest priority unfinished story:
- P1 stories before P2
- P2 stories before P3
- Within same priority, consider dependencies

#### 2. Deep-Dive Questions

**Scenario Exploration**:
- "Walk me through how a [persona] would use this"
- "What happens first? Then what?"
- "Where does the [entity] come from?"
- "What if [edge case]?"

**Acceptance Criteria**:
- "How would we know this is working correctly?"
- "What specific outcomes must happen?"
- "What should NOT happen?"

**Edge Cases**:
- "What if there are zero [entities]?"
- "What if there are thousands?"
- "What if [entity] is missing or invalid?"
- "What happens when [error condition]?"

**Requirements Discovery**:
- "How fast does this need to be?"
- "How many [entities] should this support?"
- "What permissions are needed?"
- "What data needs to persist?"

#### 3. Research

**Pattern Research**:
- How do similar products handle this?
- What UX patterns are common?
- What technical approaches work well?

**Technical Investigation**:
- What data is available?
- What APIs exist?
- What are the performance implications?
- What are the technical constraints?

**Validation Research**:
- What do users expect?
- What are common complaints about existing solutions?
- What edge cases do others encounter?

#### 4. Draft Acceptance Scenarios

Use Given/When/Then format for clarity:

**Template**:
```
Given [initial state/context]
When [action taken]
Then [expected outcome]
```

**Example Development**:

**Draft 1** (vague):
```
When user views dependencies
Then they see the services
```

**Draft 2** (more specific):
```
Given a feature affecting 3 services
When the Feature Developer views dependencies
Then they see a list of those 3 services
```

**Draft 3** (specific and testable):
```
Given a feature "User Authentication" that modifies:
  - auth-service
  - user-service
  - api-gateway
When the Feature Developer views the dependency graph
Then they see:
  - All 3 services listed
  - The relationships between services
  - Their own service highlighted
  - The last update time for each service
```

#### 5. Identify Edge Cases

Systematically explore boundaries:

**Volume Edge Cases**:
- Zero entities
- One entity
- Maximum entities
- Too many entities

**State Edge Cases**:
- Entity missing
- Entity invalid
- Entity in unexpected state
- Multiple states simultaneously

**Timing Edge Cases**:
- First time use
- Concurrent operations
- Stale data
- Race conditions

**Permission Edge Cases**:
- No permissions
- Read-only permissions
- Partial permissions
- Administrative permissions

#### 6. Extract Requirements

From scenarios and edge cases, extract formal requirements:

**Functional Requirements**:
- System MUST support up to 50 service dependencies per feature
- System MUST update dependency graph within 30 seconds of service changes
- System MUST highlight services the user has permissions to modify

**Non-Functional Requirements**:
- Response time MUST be under 200ms for graphs with < 20 services
- System MUST support 500 concurrent users
- System MUST persist dependency data for 90 days

**Automation Tip**: Use Tier 4 scripts (`add-functional-requirement.py`, `add-edge-case.py`, `add-success-criteria.py`) to extract and organize requirements into SPEC.md tables. See `references/scripts-tier-4.md` for detailed extraction workflow.

#### 7. Define Success Criteria

Make success measurable:

**Vague**: "Users can easily find dependencies"

**Specific**: "Feature Developers can identify all service dependencies in under 30 seconds, measured by user testing with 90% success rate"

### Managing Emerging Complexity

#### New Stories Emerging

While developing Story 3, user mentions: "Oh, we'd also need to export this data"

**Response**:
1. Acknowledge: "That's a good point about export capability"
2. Capture: Add to proto-stories in STATE.md
3. Prioritize: "Is this P1 (needed for MVP), P2 (important), or P3 (nice to have)?"
4. Continue: Return focus to current story

#### Stories Need to Split

Story feels too complex during development:

**Indicators**:
- More than 5-6 acceptance scenarios
- Multiple distinct workflows
- Different personas for different parts
- Some parts ready to graduate, others not

**Response**:
1. Propose split: "Story 3 feels like it's actually two stories..."
2. Define boundaries: "Story 3A: [focused scope], Story 3B: [focused scope]"
3. Update dependencies: "Story 5 depends on 3A, not 3B"
4. Continue with 3A first

#### Stories Need to Merge

Developing Stories 4 and 5, realize they're tightly coupled:

**Indicators**:
- Can't test one without the other
- Share all the same data
- Same acceptance scenarios
- Can't explain why they're separate

**Response**:
1. Propose merge: "Stories 4 and 5 seem inseparable..."
2. Create combined story: "Story 4 (merged with 5): [unified scope]"
3. Update backlog: Remove Story 5, update Story 4
4. Continue development

#### Questions Affect Graduated Stories

While developing Story 4, answer to Q45 reveals gap in Story 1:

**Response**:
1. Flag immediately: "This answer suggests Story 1 needs revision..."
2. Explain impact: "Specifically, we need to add handling for [edge case]"
3. Add to Watching list in OPEN_QUESTIONS.md
4. Continue Story 4 development
5. When Story 4 complete, propose Story 1 revision

### Graduation Criteria Checklist

Before proposing graduation:

- [ ] **100% confidence** on story scope
- [ ] **All blocking questions** resolved
- [ ] **Acceptance scenarios** are specific and testable
- [ ] **Edge cases** identified with handling defined
- [ ] **Requirements** extractable and quantified
- [ ] **Success criteria** measurable with specific numbers
- [ ] **No major unknowns** remaining
- [ ] **User validated** draft scenarios

### Graduation Protocol

**Step 1: Propose Graduation**
```
"Story 3 feels complete. Here's the summary:

- 4 acceptance scenarios covering all major workflows
- 8 edge cases identified with handling defined
- 6 functional requirements extracted
- 2 success criteria with measurable thresholds
- All blocking questions (Q23, Q25) resolved

Ready to graduate to SPEC.md?"
```

**Step 2: User Confirmation**
Wait for user to confirm: "Yes, looks complete" or raise concerns

**Step 3: Graduate**

**Manual approach:**
- Write full story to SPEC.md
- Update STATE.md story status
- Update OPEN_QUESTIONS.md (remove resolved questions)
- Log decisions to archive/DECISIONS.md
- Log research to archive/RESEARCH.md
- Update iteration summary

**Automated approach (recommended):**
Use `graduate-story.py` (Tier 2 Automation) to perform validation, extraction, formatting, and atomic updates automatically. See `references/scripts-tier-2.md` for complete usage guide and dry-run option.

**Step 4: Move to Next Story**
Select next priority story and begin development

### Transition Criteria to Phase 4

Phase 4 (Continuous Refinement) begins automatically when the first story graduates. You're now always in "refinement mode"—watching for information that affects graduated stories while continuing to develop remaining stories.

## Phase 4: Continuous Refinement

### Objective

Maintain quality of graduated stories while developing remaining stories. Later discovery may reveal gaps, conflicts, or edge cases requiring revision.

### Watching for Revision Triggers

#### Question Answers

Track questions flagged as "may affect graduated stories":

**Example**:
- Q45: "Should service owners be notified of dependency changes?"
- Flagged as: May affect Story 1 (dependency viewing)

**When answered**:
- If "Yes": Story 1 needs additional acceptance scenario
- If "No": No revision needed, remove from watching list

#### Story Development Insights

Developing Story 5, discover assumption in Story 1 was wrong:

**Trigger**: "Wait, service dependencies aren't always bidirectional"
**Impact**: Story 1 acceptance scenarios assume bidirectional relationships
**Action**: Flag for revision

#### Cross-Cutting Concerns

Identify concerns affecting multiple stories:

**Example**: "All stories need to handle the case where service data is stale"

**Response**:
1. Identify affected stories
2. Propose consistent handling approach
3. Update each affected story
4. Log as cross-cutting decision

### Revision Proposal Process

#### Step 1: Identify Need for Revision

**Triggers**:
- Question answer reveals gap
- New story reveals conflict
- Edge case spans multiple stories
- Technical constraint not previously known

#### Step 2: Analyze Impact

**Questions to answer**:
- Which stories are affected?
- What specifically needs to change?
- Is this additive, modificative, or structural?
- What dependencies are impacted?

#### Step 3: Propose Revision

```
"This answer (Q45) suggests we need to revise Story 1. Specifically:

**Current**: Story 1 only shows dependencies to the Feature Developer
**Proposed**: Story 1 should also notify Service Owners when their service becomes a dependency

This would add:
- 1 new acceptance scenario (Service Owner notification)
- 1 new requirement (notification delivery within 1 hour)
- 1 new edge case (Service Owner not found)

Should I proceed with this revision, or do you want to discuss first?"
```

#### Step 4: User Confirmation

Wait for explicit confirmation before modifying SPEC.md:
- "Yes, proceed with revision"
- "Let's discuss first" (answer questions before revising)
- "No, that's out of scope" (don't revise)

#### Step 5: Execute Revision

**Update SPEC.md**:
- Modify affected story section
- Increment revision number (v1.0 → v1.1)
- Update "Last Updated" date
- Add entry to appendix revision table

**Log Revision**:
Use `add-revision.py` (Tier 3 Enhancement) to automatically log the revision to `archive/REVISIONS.md` with:
- Document trigger
- Show before/after
- Reference decision
- Note user confirmation

See `references/scripts-tier-3.md` for revision logging details.

**Update Cross-References**:
- Update affected requirements with Tier 4 scripts if needed
- Update edge cases table
- Update success criteria if needed
- Link to decision log

**Update STATE.md**:
- Remove from watching list
- Update completed stories summary
- Note revision in completion record

### Types of Revisions

#### Additive Revisions

Adding without changing existing content:

**Examples**:
- New acceptance scenario for edge case
- Additional requirement discovered
- New success criterion

**Impact**: Low - extends without breaking

#### Modificative Revisions

Changing existing content:

**Examples**:
- Correcting wrong assumption
- Adjusting quantified threshold
- Refining scenario specificity

**Impact**: Medium - changes understanding

#### Structural Revisions

Reorganizing stories:

**Examples**:
- Splitting overly complex story
- Merging tightly coupled stories
- Reordering dependencies

**Impact**: High - affects multiple stories

### Maintaining Spec Quality

#### Consistency Checks

Periodically verify:
- All scenarios use consistent terminology
- All requirements use MUST/SHOULD consistently
- All success criteria are quantified
- All edge cases have defined handling

#### Completeness Checks

Verify graduated stories still have:
- Clear actor/goal/value
- Specific acceptance scenarios
- Defined edge case handling
- Extracted requirements
- Measurable success criteria

#### Dependency Checks

When revising stories, verify:
- Dependent stories still make sense
- Dependency graph still valid
- Priority order still appropriate

### Completion Indicators

Track progress toward completion:

**In STATE.md Story Status Overview**:
```
| # | Story | Priority | Status | Confidence | Blocked By |
|---|-------|----------|--------|------------|------------|
| 1 | Dependencies | P1 | ✅ In SPEC | 100% | - |
| 2 | Notifications | P2 | ✅ In SPEC | 100% | - |
| 3 | Testing | P1 | ✅ In SPEC | 100% | - |
| 4 | Timeline | P2 | 🔄 In Progress | 85% | Q52 |
| 5 | Export | P3 | ⏳ Queued | 20% | Story 4 |
```

**Completion metrics**:
- 3 of 5 stories graduated
- 1 story in active development
- 1 story queued
- 1 blocking question remaining
- 0 proto-stories (all crystallized)

### Final Specification Review

When all stories graduated and no open questions:

#### Deliverable Check

```
Before marking complete, verify:
- [ ] Every story independently testable
- [ ] Every acceptance scenario specific (no ambiguity)
- [ ] Every edge case has defined handling
- [ ] Every requirement is specific and measurable
- [ ] Every success criterion has numbers, not vibes
- [ ] Glossary captures all domain terms
- [ ] Cross-references complete (decisions, research)
- [ ] User has done final review and approved
```

#### Present for Final Approval

```
"The specification appears complete:

✅ 5 stories fully developed and graduated
✅ All stories independently testable
✅ 18 specific acceptance scenarios
✅ 23 edge cases with defined handling
✅ 14 quantified functional requirements
✅ 6 measurable success criteria
✅ No open questions
✅ No proto-stories remaining

Ready for your final review. Please review SPEC.md and confirm this captures everything needed for implementation."
```

#### Iteration and Archive

If approved:
- Update SPEC.md status to "Ready for Review" or "Complete"
- Create final iteration summary in archive/ITERATIONS.md
- Update STATE.md phase to "Complete"

If not approved:
- Capture feedback
- Identify what's missing or needs revision
- Return to appropriate phase
- Continue discovery

## Cross-Phase Considerations

### Context Recovery

**Between sessions**:
1. Read SPEC.md header
2. Read STATE.md current state
3. Read OPEN_QUESTIONS.md
4. Provide status summary
5. Ask: "Ready to continue? Or do you want to discuss something specific?"

### Question Management Throughout

**Adding Questions**:
- Assign sequential ID (never reuse)
- Categorize appropriately (blocking, clarifying, research, watching)
- Add context about why needed
- Link to relevant story

**Resolving Questions**:
- Remove from OPEN_QUESTIONS.md immediately
- Reference in decisions or research logs
- Update story confidence when blockers resolved

**Migrating Questions**:
- Recategorize as blocking status changes
- Move to watching list when graduation risk identified

### Decision Logging Throughout

**When to log decisions**:
- Choosing between multiple options
- Making assumptions explicit
- Resolving ambiguity
- Setting quantified thresholds

**Decision format**:
- Context (why decision needed)
- Options considered (with tradeoffs)
- Decision made
- Rationale
- Implications

### Research Logging Throughout

**When to log research**:
- Industry pattern investigation
- Technical approach exploration
- Domain knowledge building
- User expectation validation

**Research format**:
- Purpose
- Approach
- Findings
- Implications
- Stories informed

## Best Practices Across All Phases

### Maintain User Partnership

- Regularly summarize understanding: "So what I'm hearing is..."
- Validate before moving forward: "Does that sound right?"
- Offer options when multiple paths exist
- Respect user's domain expertise
- Challenge assumptions respectfully

### Manage Scope Carefully

- Capture out-of-scope items in notes, don't discard
- Distinguish P1 (MVP) from P2/P3 clearly
- Push back on scope creep: "That's valuable, but is it P1?"
- Keep MVP focused and achievable

### Quantify Relentlessly

Replace every vague term:
- "Fast" → "Under 200ms"
- "Many" → "Up to 10,000"
- "Large" → "Files up to 100MB"
- "Reliable" → "99.9% uptime"

### Track Everything

- Questions → OPEN_QUESTIONS.md
- Decisions → archive/DECISIONS.md
- Research → archive/RESEARCH.md
- Revisions → archive/REVISIONS.md
- Progress → STATE.md

This creates complete traceability.

### Update Frequently

- STATE.md: After every significant conversation
- OPEN_QUESTIONS.md: Immediately when questions added/resolved
- SPEC.md: When stories graduate or are revised
- Archive files: When decisions made or research conducted

Don't batch updates—maintain currency.
