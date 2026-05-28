# Research Log: Cross-Service Dependency Tracker

## R1: Industry patterns for dependency visualization — 2026-01-15

**Purpose**: Understand how existing products handle service/feature dependency visualization to inform Story 1 design and avoid reinventing wheels.

**Approach**: Survey of existing tools including GitHub PR dependencies, JIRA issue linking, Azure DevOps dependency tracker, Linear relationships, and specialized tools like Dependabot dependency graphs.

**Findings**:

**GitHub PR Dependencies**:
- Visual graph showing PR relationships (blocks/blocked by)
- Bidirectional view (what blocks me, what I block)
- Color coding for PR status (open, merged, closed)
- Limitation: Only works within single repository, doesn't span services

**JIRA Issue Linking**:
- Text-based relationship display ("blocks", "is blocked by", "relates to")
- No visual graph (requires plugins like Structure or BigPicture)
- Supports custom relationship types
- Cross-project linking available but clunky
- Limitation: Poor visualization for complex dependency chains

**Azure DevOps Dependency Tracker**:
- Gantt-chart style timeline with dependency arrows
- Groups by team/area path
- Shows critical path highlighting
- Limitation: Focused on timelines, not service architecture relationships

**Linear Relationships**:
- Clean, minimal relationship display
- Inline in issue view (doesn't require separate screen)
- Supports blocks/blocked-by only (not custom types)
- Limitation: Designed for issue tracking, not service dependencies

**Dependabot/Dependency Graphs**:
- Automated dependency detection from package.json, requirements.txt, etc.
- Visual tree showing direct and transitive dependencies
- Security vulnerability highlighting
- Limitation: Code-level dependencies, not feature-level or service-level

**Industry Patterns Identified**:

1. **Bidirectional is standard**: All tools show both "what I depend on" and "who depends on me"
2. **Visual representation varies**: Graph (complex but powerful) vs. List (simple but limited)
3. **Context matters**: GitHub focuses on PRs, JIRA on issues, Dependabot on packages
4. **Performance degrades quickly**: Most tools struggle with >20 dependencies visually
5. **Grouping is essential**: Domain grouping, team grouping, or status grouping prevents overwhelming users

**Relevant Examples**:

- **GitHub**: Simple graph, handles 5-10 PRs well, degrades beyond that
- **JIRA BigPicture plugin**: Sophisticated graph with grouping, handles 50+ issues, but complex UX
- **Azure DevOps**: Timeline-focused, good for planning, less good for technical dependencies
- **Dependabot**: Automated detection is killer feature, but only works for code dependencies

**Implications**:

- **For Story 1**: Use graph visualization for <20 services (most features), fall back to grouped list for larger features
- **For Discovery**: Consider automated dependency detection (analyzing service configs, API calls) in addition to manual tracking
- **For UX**: Inline dependency view (like Linear) better than separate screen for quick reference
- **For Performance**: Need grouping/collapsing for complex dependency graphs (matches D2 decision)

**Stories Informed**: Story 1 (View dependencies)

**Related Questions**: Q4, Q6, Q10, Q11

---

## R2: Technical approaches for service discovery — 2026-01-16

**Purpose**: Evaluate technical options for discovering which services a feature affects, to inform Story 1 implementation strategy.

**Approach**: Analyzed three potential approaches: (1) Service mesh integration, (2) API polling of project management tools, (3) Static configuration file parsing. Prototyped basic versions of each to understand feasibility.

**Findings**:

**Approach 1: Service Mesh Integration** (Istio, Linkerd, Consul Connect)
- **How it works**: Service mesh has complete runtime view of service-to-service communication
- **Pros**:
  - Automatic detection of actual service dependencies based on real traffic
  - No manual configuration required
  - Always accurate (reflects runtime reality)
- **Cons**:
  - Only shows runtime dependencies, not planned dependencies (need both)
  - Requires service mesh adoption (not all teams use it yet)
  - Complex to integrate with (unfamiliar APIs)
  - Doesn't connect to features (only services), need additional layer
- **Assessment**: Good supplementary data source, but not primary solution

**Approach 2: API Polling of Project Management Tools** (JIRA, Azure DevOps, Linear, GitHub Projects)
- **How it works**: Poll each project management tool API for features and their configured service tags/labels/fields
- **Pros**:
  - Works with existing tools (matches constraint)
  - Captures planned dependencies before implementation
  - Teams already tagging features with affected services
  - Well-documented APIs (JIRA REST, Azure DevOps REST, Linear GraphQL, GitHub GraphQL)
- **Cons**:
  - Depends on teams tagging correctly (data quality concern)
  - Each tool has different API (need adapters for each)
  - Rate limiting concerns (mitigated by caching per D3)
- **Assessment**: Best primary approach, aligns with constraints and user behavior

**Approach 3: Static Configuration File Parsing** (docker-compose.yml, k8s manifests, config files)
- **How it works**: Parse repository configuration files to detect service definitions and relationships
- **Pros**:
  - Automated detection (like Dependabot)
  - Works even if teams don't tag in project management
- **Cons**:
  - Only detects services in same repository (monorepo only)
  - Doesn't work for microservices in separate repos
  - Can't connect to feature context easily
  - Deployment configs != feature scope
- **Assessment**: Useful for validation, but not primary source

**Technical Recommendations**:

**Primary approach**: API polling of project management tools (Approach 2)
- Implement adapters for: JIRA (REST API), Azure DevOps (REST API), Linear (GraphQL), GitHub Projects (GraphQL)
- Poll every 30 seconds per D3
- Cache results per D8 approach
- Require teams to tag features with affected services (using custom fields/labels)

**Supplementary validation**: Service mesh integration where available (Approach 1)
- Use to validate that tagged dependencies match runtime reality
- Show warnings when mismatch detected ("Feature tagged with auth-service but no calls detected")
- Phase 2 enhancement, not MVP

**Data quality fallback**: Configuration file parsing (Approach 3)
- Use to suggest services when team forgets to tag
- "Detected that this PR modifies user-service - should we add this dependency?"

**Implications**:

- **For Story 1**: Primary data source is project management tool APIs
- **For Architecture**: Need adapter pattern to handle 4 different APIs
- **For Data Quality**: Depend on teams tagging correctly, provide validation tools to help
- **For Implementation**: Start with JIRA (most common), add others incrementally
- **For Future**: Service mesh integration provides validation and auto-suggestions

**Stories Informed**: Story 1 (View dependencies), Story 3 (Test status - similar API integration pattern)

**Related Questions**: Q16, Q19, Q21

---

## R3: User preferences study for dependency notifications — 2026-01-17

**Purpose**: Understand what notification patterns Feature Developers and Service Owners actually want, to inform Story 2 design and prevent alert fatigue.

**Approach**: Semi-structured interviews with 12 users (8 Feature Developers, 4 Service Owners) about current notification pain points and desired behavior. Asked about current tools (email, Slack, in-app), volume preferences, and content preferences.

**Findings**:

**Current Pain Points** (what users complain about):

1. **Email overload** (10 of 12 users):
   - "I get 200+ emails per day, I can't find the important ones"
   - "I've muted JIRA notifications completely, so I miss critical updates"
   - "Email is good for things I need to come back to, bad for urgent things"

2. **Slack noise** (9 of 12 users):
   - "Too many channels, I miss things in the scroll"
   - "Slack is great for urgent things, but I can't search for them later"
   - "I want Slack for immediate action items, not FYI stuff"

3. **In-app blindness** (7 of 12 users):
   - "I don't check the dashboard unless I have a specific task"
   - "Notification bell is easy to ignore"
   - "If it's only in-app, I'll see it days later"

4. **No filtering** (11 of 12 users):
   - "I want breaking changes immediately, but minor stuff can wait"
   - "When I'm actively developing, I want everything; when maintaining, I want critical only"
   - "I wish I could get a daily summary instead of constant interruptions"

**User Preferences Patterns**:

**Notification Channels** (ranked by user preference):
1. **Slack for urgent** (11 of 12 prefer): Breaking changes, deployments, test failures
2. **Email for persistent** (9 of 12 prefer): Daily digests, non-urgent changes, audit trail
3. **In-app for history** (7 of 12 sometimes use): Looking up past notifications, context

**Volume Control** (what users want to configure):

**Tiered preferences emerged naturally**:
- **"Tell me everything"** (3 users): Active development mode, want every change
  - Use case: Working on a feature with tight integration, need constant updates
  - Preferred channel: Slack + Email

- **"Breaking changes only"** (7 users): Maintenance mode, only care about issues
  - Use case: Service owner for stable service, don't need to know about minor bumps
  - Preferred channel: Slack only (urgent)

- **"Daily digest"** (2 users): Low involvement, monitoring from distance
  - Use case: Tangentially related to feature, want awareness but not interruption
  - Preferred channel: Email only

**Content Preferences** (what users want in notifications):

All 12 users want:
- **What changed**: Service name, version, or status change
- **Who changed it**: Person or team responsible, for follow-up
- **Why it matters**: Impact on my work ("this affects your feature X")
- **What to do**: Suggested action ("review this API change", "update your code")

8 users also want:
- **Link to diff/details**: Direct link to commit, PR, or issue
- **Context**: "This is the 3rd change to this service this week" (helps assess stability)

**Surprising Insights**:

1. **Consolidation is valued**: "If 3 related changes happen, send me ONE notification explaining the cascade, not 3"
   - Informed D4 (notification consolidation for cascades)

2. **Channel preference varies by urgency**: "I want Slack for things that affect me this week, email for things that affect me next month"
   - Informed D6 (use Slack + Email together, not one or the other)

3. **Trust matters**: "I'll only trust the notifications if they're accurate; one false alarm and I'll mute them all"
   - Informed SC-005 (false positive rate <5%)

**Implications**:

- **For Story 2**: Implement tiered preferences (All Changes, Breaking Only, Daily Digest) per D7
- **For Channels**: Use Slack + Email combination per D4
- **For Content**: Include what/who/why/action in every notification
- **For Quality**: Critical that notifications are accurate (affects trust)
- **For UX**: Default to "Breaking Only" to prevent overwhelming new users

**Stories Informed**: Story 2 (Notifications)

**Related Questions**: Q22, Q26, Q29, Q31, Q33

---

## R4: CI/CD integration patterns — 2026-01-17

**Purpose**: Evaluate technical approaches for integrating with Jenkins, GitHub Actions, and CircleCI to retrieve integration test results for Story 3.

**Approach**: Reviewed API documentation for all three platforms, built prototype integrations for each, tested with sample data from real CI pipelines.

**Findings**:

**Jenkins Integration**:
- **API**: REST API (https://jenkins.io/doc/book/using/remote-access-api/)
- **Authentication**: API token or username/password
- **Test results endpoint**: `/job/{name}/{buildNumber}/testReport/api/json`
- **Data format**: JSON with test suites, cases, pass/fail/skip counts
- **Pros**:
  - Rich data (can drill into individual test failures)
  - Build history available (can track trends)
- **Cons**:
  - Need to know job name and build number upfront
  - Different installations have different auth setups
  - Slow API response (500-1000ms for large test reports)
- **Implementation notes**: Cache aggressively per D8, use /lastBuild endpoint

**GitHub Actions Integration**:
- **API**: GraphQL and REST (https://docs.github.com/en/rest/actions)
- **Authentication**: GitHub token with workflow permissions
- **Test results**: Available through workflow run artifacts or check runs API
- **Data format**: Varies (depends on test framework), need to parse JUnit XML or other formats
- **Pros**:
  - Modern API (GraphQL + REST)
  - Good documentation
  - Webhook support for real-time updates (future enhancement)
- **Cons**:
  - Test results not first-class (stored as artifacts, need parsing)
  - Need to download artifacts to parse results
  - Rate limiting (5000 requests/hour for authenticated)
- **Implementation notes**: Use Check Runs API when available, fall back to artifact parsing

**CircleCI Integration**:
- **API**: REST API v2 (https://circleci.com/docs/api/v2/)
- **Authentication**: Personal API token
- **Test results**: Available through insights API or test metadata
- **Data format**: JSON test metadata for recent runs
- **Pros**:
  - Clean API design
  - Test metadata stored separately (no artifact parsing)
  - Fast response times
- **Cons**:
  - Limited test history (last 90 days)
  - Less adoption than Jenkins/GitHub Actions
  - Requires CircleCI-specific test result upload
- **Implementation notes**: Use insights API for aggregated data

**Common Patterns Across All Three**:

1. **Authentication tokens required**: All three need user-provisioned tokens
   - Implication: Need secure token storage and management
   - Implication: Setup documentation must guide users through token creation

2. **Test result formats vary**: JUnit XML, JSON, TAP, custom formats
   - Implication: Need normalization layer to convert to common format
   - Implication: Support most common format (JUnit XML) first, expand later

3. **Build identification challenges**: Need to map feature → repository → build
   - Implication: Require teams to tag builds with feature ID (custom metadata)
   - Implication: Provide helper scripts to add feature tagging

4. **Performance varies**: 100ms (CircleCI) to 1000ms (Jenkins) response times
   - Implication: Validates D8 caching decision (15-minute cache essential)
   - Implication: Load test results in parallel for multiple services

**Technical Recommendations**:

**Adapter Pattern**:
```
TestResultService
  ├─ JenkinsAdapter
  ├─ GitHubActionsAdapter
  └─ CircleCIAdapter

All implement: getTestResults(featureId, serviceId) → NormalizedTestResult
```

**Normalized Test Result Format**:
```json
{
  "service": "auth-service",
  "feature": "user-auth-v2",
  "status": "passing|failing|in_progress|not_run",
  "passCount": 45,
  "failCount": 2,
  "skipCount": 0,
  "failureDetails": [
    {"testName": "test_login", "message": "Assertion failed", "trace": "..."}
  ],
  "timestamp": "2026-01-18T10:30:00Z",
  "buildUrl": "https://jenkins.example.com/job/auth-service/123",
  "source": "jenkins"
}
```

**Implications**:

- **For Story 3**: Use adapter pattern with 3 implementations (Jenkins, GitHub Actions, CircleCI)
- **For Setup**: Requires teams to configure API tokens and feature tagging
- **For Performance**: Parallel fetching + caching essential (validates D8)
- **For Data Quality**: Normalization layer needed for consistent UI
- **For Future**: Webhook integration to invalidate cache on test completion

**Stories Informed**: Story 3 (Track integration test status)

**Related Questions**: Q39, Q40, Q41, Q43, Q46

---

## Questions Informed by Research

- Q4: How do other tools visualize dependencies? → R1
- Q6: What works well in existing dependency tools? → R1
- Q10: Should we use graph or list visualization? → R1
- Q11: How many dependencies can tools handle before UX degrades? → R1
- Q16: How can we automatically detect service dependencies? → R2
- Q19: Should we integrate with service mesh? → R2
- Q21: Which project management tools should we support? → R2
- Q22: What notification channels do users prefer? → R3
- Q26: How much notification volume can users handle? → R3
- Q29: Should notifications consolidate related changes? → R3
- Q31: What content should notifications include? → R3
- Q33: What notification preferences should we support? → R3
- Q39: Which CI/CD systems should we integrate with? → R4
- Q40: How do we get test results from each CI system? → R4
- Q41: What test result formats do we need to support? → R4
- Q43: How do we map features to builds in CI systems? → R4
- Q46: What's the performance profile of CI APIs? → R4
