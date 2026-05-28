# Decision Log: Cross-Service Dependency Tracker

## D1: Use bidirectional dependency tracking — 2026-01-16

**Context**: During Story 1 development, needed to decide whether dependency view should show only "what my feature depends on" (outbound) or also "what features depend on my service" (inbound).

**Question**: Should we track and display both outbound and inbound dependencies, or just outbound?

**Options Considered**:
1. **Outbound only** (what my feature depends on)
   - Pros: Simpler implementation, matches most project management tools
   - Cons: Service Owners have no visibility into incoming dependencies, doesn't solve coordination problem for them

2. **Bidirectional** (both outbound and inbound)
   - Pros: Solves problem for both personas (Feature Developers and Service Owners), enables proactive coordination
   - Cons: More complex data model, need to track both directions

3. **Separate views** (different interface for each persona)
   - Pros: Optimized UX per persona
   - Cons: Duplicate implementation effort, user confusion about which view to use

**Decision**: Bidirectional dependency tracking (Option 2)

**Rationale**:
- Both personas need this capability based on problem statement
- Service Owners specifically mentioned "need to know what's coming" in problem exploration
- Added complexity is manageable (same data, different query direction)
- Enables Story 2 (notifications) for both personas

**Implications**:
- Story 1 acceptance scenarios must cover both outbound and inbound views
- Data model needs bidirectional relationship tracking
- Service Owner persona becomes primary user alongside Feature Developer
- Story 4 (timeline for Service Owners) becomes more valuable with this foundation

**Stories Affected**: Story 1, Story 2 (indirectly), Story 4 (indirectly)

**Related Questions**: Q1, Q3, Q7

---

## D2: Support up to 50 services per dependency graph — 2026-01-16

**Context**: Needed to set performance targets for dependency graph visualization. Current architecture has 23 services, growing to 35-40 next year.

**Question**: What's the maximum number of services we should support in a single dependency graph?

**Options Considered**:
1. **Optimize for current scale (25 services)**
   - Pros: Simpler implementation, meets current needs
   - Cons: Will need rework within 1 year as architecture grows

2. **Plan for 2x growth (50 services)**
   - Pros: Future-proof for 2+ years, handles edge cases of very large features
   - Cons: More complex optimization needed upfront

3. **Unlimited/dynamic**
   - Pros: Most flexible
   - Cons: Can't guarantee performance, UI becomes unusable with hundreds of services

**Decision**: Support up to 50 services per dependency graph (Option 2)

**Rationale**:
- Current max is 15 services per feature (cross-cutting infrastructure change)
- 50 services = 2x projected architecture growth in 2 years
- Provides comfortable headroom for edge cases
- Can optimize for this target without over-engineering
- If exceeded, can paginate or provide export rather than visualization

**Implications**:
- FR-001: System MUST support up to 50 service dependencies per feature
- FR-012: System MUST handle features affecting 15+ services without degradation
- EC-02: Define edge case for >50 services (show warning, display first 50, provide export)
- UI needs grouping/collapse functionality for large graphs
- Performance testing must validate 50-service scenarios

**Stories Affected**: Story 1 (directly), Story 5 (export becomes more important for large graphs)

**Related Questions**: Q8, Q12, Q15

---

## D3: Poll for dependency data every 30 seconds — 2026-01-16

**Context**: Need to decide how to keep dependency data fresh as services and features change.

**Question**: Should we poll for changes, use webhooks, or require manual refresh?

**Options Considered**:
1. **Manual refresh only**
   - Pros: Simplest implementation, no infrastructure needed
   - Cons: Stale data problem, poor user experience

2. **Webhooks from each tool** (JIRA, Azure DevOps, Linear, GitHub Actions, etc.)
   - Pros: Real-time updates, efficient
   - Cons: Complex setup, each tool has different webhook API, brittle (webhook failures), security concerns (need to expose endpoint)

3. **Polling every 30 seconds**
   - Pros: Consistent implementation across all tools, resilient to failures, simpler security model
   - Cons: Not real-time, higher API usage, rate limiting concerns

**Decision**: Poll for updates every 30 seconds (Option 3)

**Rationale**:
- 30-second staleness is acceptable for this use case (not mission-critical real-time)
- Much simpler than webhook orchestration across 4+ different tools
- More resilient: if poll fails, next one succeeds; if webhook fails, data never updates
- Easier to implement authentication (we make outbound calls, don't expose endpoints)
- Modern APIs have sufficient rate limits for 30-second polling
- Can optimize later with webhooks if needed, but start simple

**Implications**:
- FR-002: System MUST update dependency graph data within 30 seconds of service changes
- Not true real-time (30s delay acceptable)
- Need to implement poll scheduling and error handling
- API rate limiting must be monitored
- Future enhancement: Add webhooks for critical tools (optional)

**Stories Affected**: Story 1 (dependency data freshness), Story 2 (notification delay), Story 4 (timeline updates)

**Related Questions**: Q18, Q20

---

## D4: Use Slack + Email for notifications, not in-app only — 2026-01-17

**Context**: Story 2 requires sending notifications about dependency changes. Needed to decide delivery mechanisms.

**Question**: Where should notifications be delivered?

**Options Considered**:
1. **In-app only** (notification bell in dashboard)
   - Pros: Simplest, full control over UX
   - Cons: Requires users to check dashboard regularly, easy to miss

2. **Email only**
   - Pros: Reaches everyone, standard mechanism
   - Cons: Email fatigue, may be ignored, delayed attention

3. **Slack only**
   - Pros: Real-time, where developers already work
   - Cons: Not everyone uses Slack consistently, easy to lose in channel noise

4. **Slack + Email combination**
   - Pros: Immediate Slack notification + persistent email record
   - Cons: More complex implementation, potential for duplicate notifications

**Decision**: Slack + Email combination (Option 4)

**Rationale**:
- User interviews revealed: "I live in Slack but appreciate email for important things I can come back to"
- Slack provides immediacy (5-minute delivery target)
- Email provides persistence (15-minute delivery, can search/archive)
- Users can mute Slack channel if overwhelming, still get email digest
- Different notification types can use different channels (critical→both, minor→email only)
- Matches notification preferences in FR-006 (all changes, breaking only, daily digest)

**Implications**:
- FR-004: System MUST send Slack notifications within 5 minutes
- FR-005: System MUST send email notifications within 15 minutes
- Need to integrate with Slack API and email service (SendGrid or similar)
- Need to handle delivery failures gracefully
- Notification preferences must support channel selection

**Stories Affected**: Story 2 (directly), Story 4 (timeline change notifications)

**Related Questions**: Q25, Q28, Q30

---

## D5: Integrate with existing CI/CD, don't build new test infrastructure — 2026-01-17

**Context**: Story 3 requires showing integration test status. Needed to decide whether to integrate with existing CI/CD or build new test runner.

**Question**: How should we obtain integration test results?

**Options Considered**:
1. **Build new test infrastructure**
   - Pros: Full control, optimized for our use case
   - Cons: Massive engineering effort, requires teams to migrate tests, adoption barrier

2. **Integrate with existing CI/CD** (Jenkins, GitHub Actions, CircleCI)
   - Pros: Uses existing tests, no migration needed, faster time to value
   - Cons: Complex integration (3 different APIs), limited control over test execution

3. **Hybrid**: New infrastructure for new tests, integration for existing tests
   - Pros: Best of both worlds eventually
   - Cons: Most complex, confusing for users

**Decision**: Integrate with existing CI/CD systems (Option 2)

**Rationale**:
- Teams already have integration tests running in Jenkins/GitHub Actions/CircleCI
- Building new infrastructure would delay delivery by months
- Adoption would be very slow (teams resist migrating working tests)
- Integration complexity is manageable (3 well-documented APIs)
- Can add our own test orchestration later as enhancement if needed
- Matches constraint: "Must integrate with existing tools"

**Implications**:
- FR-007: System MUST integrate with Jenkins, GitHub Actions, and CircleCI
- Need to implement 3 different API integrations for test results
- Test result format will vary by CI system (need normalization layer)
- Can't control test execution timing (depends on how teams configured CI)
- May need to cache results to handle CI system downtime (FR-009)

**Stories Affected**: Story 3 (directly)

**Related Questions**: Q35, Q38, Q42

---

## D6: Define "significant change" as version bump, API change, or status change — 2026-01-17

**Context**: Story 2 notifications need to define what constitutes a "significant change" worth notifying about.

**Question**: What changes should trigger notifications?

**Options Considered**:
1. **Every commit** to a dependency
   - Pros: Complete visibility
   - Cons: Massive notification spam, alert fatigue

2. **Version bumps only** (semantic versioning: major.minor.patch)
   - Pros: Clear signal, industry standard
   - Cons: Misses important changes if versioning discipline is inconsistent

3. **Version bumps, API contract changes, or status changes**
   - Pros: Covers the important cases, multiple signals
   - Cons: Need to define API contract changes (requires static analysis or OpenAPI)

4. **User-configurable** (let each user define their threshold)
   - Pros: Maximum flexibility
   - Cons: Complex configuration, users don't know what to choose

**Decision**: Version bumps, API contract changes (via OpenAPI diff), or status changes to Ready for Testing/Deployed (Option 3)

**Rationale**:
- Version bumps catch intentional releases (most important signal)
- API contract changes catch breaking changes even without version bump
- Status changes (Ready for Testing/Deployed) catch lifecycle events that need coordination
- Together these cover "changes that affect my work" without spam
- Can enhance with user preferences (FR-006) for filtering further

**Implications**:
- FR-006 notification preferences: All Changes, Breaking Only, Daily Digest
- D8 documents this definition explicitly
- Need to integrate with OpenAPI/Swagger specs for contract diff (technical complexity)
- Status change tracking requires integration with project management tools
- "Breaking changes" filter means: major version bump OR API contract breaking change

**Stories Affected**: Story 2 (directly)

**Related Questions**: Q30, Q32, Q34

---

## D7: Support notification preferences to prevent alert fatigue — 2026-01-17

**Context**: Story 2 notifications could become overwhelming if not controlled. User interviews revealed "I want to know about important things, but not everything."

**Question**: How should users control notification volume?

**Options Considered**:
1. **No preferences** (all users get all notifications)
   - Pros: Simplest implementation
   - Cons: Guaranteed alert fatigue, users will ignore/mute

2. **Binary on/off** (receive notifications or don't)
   - Pros: Simple choice
   - Cons: Not granular enough, forces all-or-nothing decision

3. **Tiered preferences**: All Changes, Breaking Only, Daily Digest
   - Pros: Balances simplicity and control
   - Cons: Need to define what "breaking" means

4. **Fully granular** (configure per service, per change type, per severity)
   - Pros: Maximum control
   - Cons: Configuration complexity, users won't configure properly

**Decision**: Tiered preferences (Option 3): All Changes, Breaking Only, Daily Digest

**Rationale**:
- Matches how users described their needs: "I want to know about breaking changes immediately, but minor stuff can wait"
- Simple enough to configure without decision fatigue
- Covers common use cases: active development (All Changes), maintenance mode (Breaking Only), low involvement (Daily Digest)
- Can enhance with more granularity later if users request it
- Aligns with D6 definition of "significant change"

**Implications**:
- FR-006: System MUST support notification preferences (All Changes, Breaking Only, Daily Digest)
- Need to persist user preferences
- Need to categorize each notification by severity/type
- Daily Digest requires batching and scheduled delivery (new requirement)
- Notification service must check preferences before sending

**Stories Affected**: Story 2 (directly), Story 4 (timeline notifications may reuse this mechanism)

**Related Questions**: Q34, Q36

---

## D8: Cache test results for 15 minutes to reduce CI system load — 2026-01-18

**Context**: Story 3 shows integration test status. Each page load could query multiple CI systems, causing performance issues and potentially rate limiting.

**Question**: Should we cache test results, and if so, for how long?

**Options Considered**:
1. **No caching** (query CI systems on every request)
   - Pros: Always fresh data
   - Cons: Slow page loads, high CI system load, rate limiting risk, poor user experience

2. **Cache for 5 minutes**
   - Pros: Good freshness, reduces load
   - Cons: May still be too frequent for stable tests (some run hourly)

3. **Cache for 15 minutes**
   - Pros: Balances freshness and performance, reduces CI load significantly
   - Cons: Up to 15-minute staleness for test results

4. **Smart caching** (short cache for active tests, long cache for stable tests)
   - Pros: Optimizes per scenario
   - Cons: Complex logic, hard to predict behavior

**Decision**: Cache for 15 minutes (Option 3)

**Rationale**:
- Test results don't change that frequently (most tests run every 30-60 minutes)
- 15-minute staleness is acceptable for this use case (not deploying based solely on dashboard)
- Significantly reduces load on CI systems (from potentially hundreds of requests/minute to one per 15 minutes per feature)
- Simple implementation (standard TTL cache)
- Can invalidate cache on-demand if needed (future enhancement)
- Aligns with 30-second dependency update from D3 (different data, different freshness requirements)

**Implications**:
- FR-009: System MUST cache test results for 15 minutes
- Test status may be up to 15 minutes stale (document this to users)
- Need cache invalidation strategy for when tests are manually retriggered
- EC-05: CI system unavailable → show cached data with timestamp
- Cache key should be (feature_id, service_id, test_suite)

**Stories Affected**: Story 3 (directly)

**Related Questions**: Q44, Q47

---

## D9: Support manual verification for services without CI/CD — 2026-01-18

**Context**: Story 3 integration testing. Not all services have automated integration tests configured (legacy services, services in migration).

**Question**: How should we handle services that don't have automated integration tests?

**Options Considered**:
1. **Require all services to have automated tests** (block feature until tests added)
   - Pros: Enforces best practices
   - Cons: Blocks adoption, unrealistic timeline (some services won't have tests for months)

2. **Show "No tests" and leave it at that**
   - Pros: Simple, honest
   - Cons: Provides no path forward, Feature Developer doesn't know if manual testing happened

3. **Support manual verification** (let humans mark as verified)
   - Pros: Pragmatic, provides immediate value while tests are being added
   - Cons: Less reliable than automated tests, requires trust model

4. **Partial automation** (manual verification expires, requires re-verification)
   - Pros: Encourages fresh verification
   - Cons: Adds complexity, unclear how long verification should last

**Decision**: Support manual verification with timestamp and verifier name (Option 3)

**Rationale**:
- Pragmatic: enables adoption for services currently without CI/CD
- Transparent: shows WHO verified and WHEN, not just "verified"
- Doesn't prevent automated tests (can replace manual with automated as tests are added)
- Provides value immediately rather than waiting months for test infrastructure
- Matches reality: some services will never have full CI/CD (small internal tools)

**Implications**:
- FR-010: System MUST support manual verification for services without automated tests
- Need UI for marking service as "Manually Verified" with timestamp and name
- Manual verification should show differently than automated (visual indicator)
- Consider expiration: manual verification older than 7 days shows warning
- EC-06: Service has no integration tests configured → show with manual verification option

**Stories Affected**: Story 3 (directly)

**Related Questions**: Q48, Q51

---

## Questions Resolved Through These Decisions

- Q1: Should we track outbound dependencies only, or both outbound and inbound? → D1
- Q3: Do Service Owners need visibility into features depending on their service? → D1
- Q7: How do we enable coordination for Service Owners? → D1
- Q8: What's the maximum number of services we should support? → D2
- Q12: Should we plan for architecture growth? → D2
- Q15: What happens if a feature affects >50 services? → D2
- Q18: How should we keep dependency data fresh? → D3
- Q20: Should we use webhooks or polling? → D3
- Q25: Where should notifications be delivered? → D4
- Q28: Is email sufficient for notifications? → D4
- Q30: What changes should trigger notifications? → D6, D7
- Q32: How do we define "significant change"? → D6
- Q34: How can users control notification volume? → D7
- Q35: Should we build new test infrastructure or integrate with existing CI/CD? → D5
- Q38: How do we get test results from multiple CI systems? → D5
- Q42: What if a service uses a different CI system? → D5
- Q44: Should we cache test results? → D8
- Q47: How long should test results be cached? → D8
- Q48: What about services without automated tests? → D9
- Q51: Is manual verification acceptable? → D9
