# PRISM Workflow Examples

This document provides real-world examples of PRISM workflows across different scenarios.

## Table of Contents

1. [Greenfield: New E-Commerce Platform](#greenfield-new-e-commerce-platform)
2. [Brownfield: Legacy System Modernization](#brownfield-legacy-system-modernization)
3. [API Integration](#api-integration)
4. [Bug Fix in Complex System](#bug-fix-in-complex-system)
5. [Performance Optimization](#performance-optimization)
6. [Security Enhancement](#security-enhancement)

---

## Greenfield: New E-Commerce Platform

### Scenario
Building a new e-commerce platform from scratch with modern technology stack.

### Workflow

#### Phase 1: Architecture Planning

**User Request:**
> "I need to design a full-stack e-commerce platform with product catalog, shopping cart, checkout, and payment processing."

**Step 1: Create Architecture**
```
@architect
*create-fullstack-architecture
```

**Architect Process:**
1. Gathers requirements (users, products, orders, payments)
2. Designs system components:
   - Frontend: React + Redux
   - Backend: Node.js + Express
   - Database: PostgreSQL
   - Cache: Redis
   - Payments: Stripe integration
3. Creates architecture document with:
   - System diagrams
   - Data models
   - API specifications
   - Security architecture
   - Deployment strategy

**Step 2: Validate Architecture**
```
@architect
*execute-checklist
```

**Output:** `docs/architecture/ecommerce-architecture.md`

#### Phase 2: Product Planning

**Step 3: Create PRD**
```
@pm
*create-prd
```

**PM Process:**
1. Defines product requirements
2. Creates epics:
   - Epic 1: User Management
   - Epic 2: Product Catalog
   - Epic 3: Shopping Cart
   - Epic 4: Checkout & Payments
   - Epic 5: Admin Dashboard
3. Prioritizes features
4. Defines success metrics

**Output:** `docs/prd.md`

#### Phase 3: Shard into Stories

**Step 4: Break Architecture into Stories**
```
@po
*shard-doc docs/architecture/ecommerce-architecture.md docs/stories
```

**PO Process:**
1. Identifies components:
   - User service
   - Product service
   - Cart service
   - Order service
   - Payment service
2. Creates story sequence:
   - Story 1.1: User registration and authentication
   - Story 1.2: User profile management
   - Story 2.1: Product catalog API
   - Story 2.2: Product search and filtering
   - Story 2.3: Product detail pages
   - Story 3.1: Shopping cart state management
   - Story 3.2: Cart API endpoints
   - Story 4.1: Checkout workflow
   - Story 4.2: Payment integration
   - Story 4.3: Order confirmation
3. Adds dependencies (e.g., Story 3.1 requires 1.1, 2.1)

**Output:** `docs/stories/1.1.user-registration.md`, etc.

#### Phase 4: Development

**Step 5: Implement First Story**
```
@dev
*develop-story docs/stories/1.1.user-registration.md
```

**Dev Process:**
1. Sets PSP tracking started timestamp
2. **Task 1: Create User model**
   - Writes test: `test_user_creation()`
   - Implements User model with email, password fields
   - Runs test → PASSES
   - Updates File List: `models/user.py`
   - Marks task [x]
3. **Task 2: Implement registration endpoint**
   - Writes test: `test_post_register_creates_user()`
   - Implements `/api/auth/register` endpoint
   - Runs test → PASSES
   - Updates File List: `routes/auth.py`
   - Marks task [x]
4. **Task 3: Add password hashing**
   - Writes test: `test_password_is_hashed()`
   - Implements bcrypt hashing
   - Runs test → PASSES
   - Updates File List: `utils/crypto.py`
   - Marks task [x]
5. **Task 4: Write integration tests**
   - Writes E2E test: `test_user_can_register_and_login()`
   - Runs all tests → PASSES
   - Marks task [x]
6. Runs full regression → PASSES
7. Updates PSP tracking completed
8. Sets status: "Ready for Review"

#### Phase 5: Quality Review

**Step 6: QA Review**
```
@qa
*review docs/stories/1.1.user-registration.md
```

**QA Process:**
1. Reviews code quality
2. Checks test coverage (>90% for auth)
3. Validates security (password hashing, input validation)
4. Tests edge cases
5. Updates QA Results section in story
6. Creates gate: `docs/qa/gates/1.1-user-registration.yml`
7. Gate decision: **PASS**

**Step 7: Commit and Continue**
```
git add .
git commit -m "feat: Add user registration with authentication"
git push
```

Move to next story (1.2, 2.1, etc.)

### Key Takeaways

- ✅ Architecture first, then implementation
- ✅ Break into small, focused stories
- ✅ TDD throughout development
- ✅ Quality gates before merging
- ✅ Systematic progression through workflow

---

## Brownfield: Legacy System Modernization

### Scenario
Modernizing a 10-year-old PHP monolith to microservices with modern tech stack.

### Workflow

#### Phase 1: Document Existing System

**Step 1: Document Legacy Project**
```
@architect
*document-project
```

**Architect Process:**
1. Analyzes existing codebase
2. Documents:
   - Current architecture (monolithic PHP)
   - Database schema
   - API endpoints (if any)
   - Business logic patterns
   - Integration points
   - Technical debt areas
3. Creates source tree
4. Identifies modernization candidates

**Output:** `docs/architecture/legacy-system-docs.md`

#### Phase 2: Plan Modernization

**Step 2: Create Brownfield Architecture**
```
@architect
*create-brownfield-architecture
```

**Architect Process:**
1. Reviews legacy documentation
2. Designs migration strategy:
   - **Strangler Fig Pattern**: Gradually replace modules
   - **Phase 1**: Extract user service
   - **Phase 2**: Extract product service
   - **Phase 3**: Extract order service
3. Plans parallel running (old + new)
4. Defines rollback procedures
5. Specifies feature flags

**Output:** `docs/architecture/modernization-architecture.md`

#### Phase 3: Create Modernization Story

**Step 3: Create Brownfield Story**
```
@po
*create-story
```

**Story:** Extract User Service from Monolith

**Acceptance Criteria:**
- New user service handles authentication
- Facade routes requests to new service
- Legacy code still accessible via facade
- All existing user tests pass
- Feature flag controls routing
- Performance unchanged or improved

#### Phase 4: Risk Assessment (CRITICAL for Brownfield)

**Step 4: Assess Integration Risks**
```
@qa
*risk docs/stories/1.1.extract-user-service.md
```

**QA Process:**
1. **Identifies Risks:**
   - **High**: Breaking authentication for existing users (P=8, I=9, Score=72)
   - **High**: Data migration failures (P=6, I=9, Score=54)
   - **Medium**: Performance degradation (P=5, I=7, Score=35)
   - **Medium**: Session handling mismatches (P=6, I=6, Score=36)
2. **Documents Mitigation:**
   - Comprehensive integration tests
   - Parallel running with feature flag
   - Gradual rollout (5% → 25% → 50% → 100%)
   - Rollback procedure documented
   - Performance monitoring
3. **Risk Score:** 72 (High) - Requires enhanced testing

**Output:** `docs/qa/assessments/1.1-extract-user-service-risk-20251022.md`

**Step 5: Design Test Strategy**
```
@qa
*design docs/stories/1.1.extract-user-service.md
```

**QA Process:**
1. **Unit Tests** (15 scenarios):
   - User service authentication logic
   - Password validation
   - Token generation
2. **Integration Tests** (12 scenarios):
   - Facade routing logic
   - New service endpoints
   - Database operations
   - Session management
3. **E2E Tests** (8 scenarios) - P0 Critical:
   - Existing user can still login (legacy path)
   - New user registers and logs in (new path)
   - Feature flag switches between paths
   - Session persists across services
4. **Regression Tests** (20 scenarios):
   - All existing user functionality still works
   - No performance degradation
   - All legacy integrations intact

**Output:** `docs/qa/assessments/1.1-extract-user-service-test-design-20251022.md`

#### Phase 5: Strangler Pattern Implementation

**Step 6: Implement with Strangler Pattern**
```
@dev
*strangler docs/stories/1.1.extract-user-service.md
```

**Dev Process:**
1. **Task 1: Create new user service**
   - Writes unit tests for new service
   - Implements Node.js user service
   - Tests pass
2. **Task 2: Create facade layer**
   - Writes tests for routing logic
   - Implements facade in legacy codebase
   - Routes to legacy by default
   - Tests pass
3. **Task 3: Add feature flag**
   - Writes tests for flag logic
   - Implements flag: `USE_NEW_USER_SERVICE`
   - Tests both paths
4. **Task 4: Data migration script**
   - Writes tests for migration
   - Implements safe migration with rollback
   - Tests on copy of production data
5. **Task 5: Integration tests**
   - Writes tests for both old and new paths
   - Validates facade routing
   - Tests session management
6. **Task 6: Performance tests**
   - Benchmarks legacy performance
   - Tests new service performance
   - Validates no degradation

#### Phase 6: Validation During Development

**Step 7: Trace Requirements Coverage**
```
@qa
*trace docs/stories/1.1.extract-user-service.md
```

**QA Process:**
1. Maps each AC to tests:
   - AC1 (new service auth) → 8 unit, 4 integration, 2 E2E tests
   - AC2 (facade routing) → 3 integration, 2 E2E tests
   - AC3 (legacy still works) → 12 regression tests
   - AC4 (tests pass) → All 20 legacy tests + 35 new tests
   - AC5 (feature flag) → 4 integration, 3 E2E tests
   - AC6 (performance) → 5 performance benchmark tests
2. **Coverage:** 100% of ACs covered
3. **Gaps:** None identified

**Output:** `docs/qa/assessments/1.1-extract-user-service-trace-20251022.md`

**Step 8: NFR Validation**
```
@qa
*nfr docs/stories/1.1.extract-user-service.md
```

**QA Process:**
1. **Performance:**
   - Login latency: 120ms (legacy) → 95ms (new) ✅
   - Throughput: 500 req/s (legacy) → 600 req/s (new) ✅
2. **Security:**
   - Password hashing: bcrypt → argon2 (stronger) ✅
   - Token expiry: 24h → 1h (more secure) ✅
   - SQL injection tests: All pass ✅
3. **Reliability:**
   - Error handling: Comprehensive ✅
   - Retry logic: 3 retries with backoff ✅
   - Circuit breaker: Implemented ✅

**Output:** `docs/qa/assessments/1.1-extract-user-service-nfr-20251022.md`

#### Phase 7: Comprehensive Review

**Step 9: Full QA Review**
```
@qa
*review docs/stories/1.1.extract-user-service.md
```

**QA Process:**
1. **Code Quality:** Excellent, follows Node.js best practices
2. **Test Coverage:** 95% unit, 88% integration, 100% critical E2E
3. **Security:** Enhanced security with argon2, proper token handling
4. **Performance:** 20% improvement over legacy
5. **Integration Safety:** Facade pattern ensures safe rollback
6. **Regression:** All 20 legacy tests pass
7. **Documentation:** Complete rollback procedure

**Gate Decision:** **PASS** ✅

**Output:**
- QA Results in story file
- `docs/qa/gates/1.1-extract-user-service.yml`

#### Phase 8: Gradual Rollout

**Step 10: Deploy with Feature Flag**
1. Deploy with flag OFF (0% new service)
2. Enable for 5% of users
3. Monitor for 24 hours
4. If stable, increase to 25%
5. Monitor for 48 hours
6. If stable, increase to 50%
7. Monitor for 1 week
8. If stable, increase to 100%
9. Monitor for 1 month
10. If stable, remove facade, deprecate legacy

### Key Takeaways

- ✅ **ALWAYS** run risk assessment before brownfield work
- ✅ Strangler fig pattern for safe migration
- ✅ Feature flags for gradual rollout
- ✅ Comprehensive regression testing
- ✅ Performance benchmarking
- ✅ Rollback procedures documented
- ✅ Enhanced QA validation throughout

---

## API Integration

### Scenario
Integrating Stripe payment processing into existing e-commerce platform.

### Workflow

**Step 1: Create Story**
```
@po
*create-story
```

**Story:** Integrate Stripe for Payment Processing

**Step 2: Risk Assessment**
```
@qa
*risk docs/stories/3.1.stripe-integration.md
```

**Risks Identified:**
- Payment failures (P=6, I=9, Score=54) - High
- Data security (P=4, I=9, Score=36) - Medium-High
- API rate limits (P=5, I=5, Score=25) - Medium

**Step 3: Test Design**
```
@qa
*design docs/stories/3.1.stripe-integration.md
```

**Test Strategy:**
- Unit: Payment amount calculation, currency conversion
- Integration: Stripe API calls, webhook handling
- E2E: Complete checkout with test cards (P0)

**Step 4: Implement**
```
@dev
*develop-story docs/stories/3.1.stripe-integration.md
```

**Implementation:**
1. Stripe SDK integration
2. Payment intent creation
3. Webhook handler for payment events
4. Error handling and retries
5. Idempotency keys for safety
6. Comprehensive logging

**Step 5: Review**
```
@qa
*review docs/stories/3.1.stripe-integration.md
```

**QA Checks:**
- PCI compliance validation
- Error handling for all Stripe exceptions
- Webhook signature verification
- Idempotency testing
- Test card scenarios

**Gate:** **PASS WITH CONCERNS**
- Concern: Need production monitoring alerts
- Action: Add CloudWatch alerts for payment failures

### Key Takeaways

- ✅ External integrations need comprehensive error handling
- ✅ Security is critical for payment processing
- ✅ Test with provider's test environment
- ✅ Idempotency prevents duplicate charges
- ✅ Monitoring and alerting essential

---

## Bug Fix in Complex System

### Scenario
Users report intermittent authentication failures in production.

### Workflow

**Step 1: Create Bug Story**
```
@po
*create-story
```

**Story:** Fix intermittent authentication failures

**AC:**
- Identify root cause of authentication failures
- Implement fix
- Add tests to prevent regression
- No new failures in production

**Step 2: Risk Profile**
```
@qa
*risk docs/stories/2.5.fix-auth-failures.md
```

**Risks:**
- Side effects in auth system (P=6, I=8, Score=48)
- Performance impact (P=4, I=6, Score=24)

**Mitigation:**
- Comprehensive regression tests
- Performance benchmarks

**Step 3: Investigate and Implement**
```
@dev
*develop-story docs/stories/2.5.fix-auth-failures.md
```

**Investigation:**
1. Reviews logs → Finds race condition in token validation
2. Writes failing test reproducing the race condition
3. Fixes: Adds proper locking around token validation
4. Test now passes
5. Adds performance test to ensure no degradation

**Step 4: Trace Coverage**
```
@qa
*trace docs/stories/2.5.fix-auth-failures.md
```

**Coverage:**
- AC1 (root cause identified): Covered by investigation notes
- AC2 (fix implemented): Covered by 3 unit tests, 2 integration tests
- AC3 (regression tests): 5 new tests added
- AC4 (no new failures): E2E smoke tests pass

**Step 5: Review**
```
@qa
*review docs/stories/2.5.fix-auth-failures.md
```

**QA Validates:**
- Root cause analysis documented
- Fix addresses core issue (race condition)
- Regression tests comprehensive
- No performance degradation
- Error handling improved

**Gate:** **PASS** ✅

### Key Takeaways

- ✅ TDD helps: Reproduce bug in test first
- ✅ Document root cause analysis
- ✅ Regression tests prevent recurrence
- ✅ Performance validation for production fixes

---

## Performance Optimization

### Scenario
Dashboard loading time is 8 seconds, needs to be under 2 seconds.

### Workflow

**Step 1: Create Performance Story**
```
@po
*create-story
```

**Story:** Optimize dashboard loading performance

**AC:**
- Dashboard loads in <2 seconds (P50)
- <3 seconds P95
- No functionality broken
- Maintain current data freshness

**Step 2: NFR Assessment Early**
```
@qa
*nfr docs/stories/4.2.optimize-dashboard.md
```

**QA Establishes Baselines:**
- Current P50: 8.2s
- Current P95: 12.5s
- Target P50: <2s
- Target P95: <3s

**Step 3: Implement Optimizations**
```
@dev
*develop-story docs/stories/4.2.optimize-dashboard.md
```

**Optimizations:**
1. **Database Query Optimization:**
   - Added indexes on frequently queried columns
   - Reduced N+1 queries with joins
   - Result: Queries 85% faster
2. **Caching:**
   - Added Redis cache for dashboard data
   - 5-minute TTL
   - Result: 70% of requests served from cache
3. **Frontend Optimization:**
   - Lazy loading of charts
   - Virtual scrolling for tables
   - Result: Initial render 60% faster
4. **API Response Optimization:**
   - Pagination for large datasets
   - Compression enabled
   - Result: Payload size reduced 75%

**Step 4: Validate NFRs**
```
@qa
*nfr docs/stories/4.2.optimize-dashboard.md
```

**QA Measures:**
- New P50: 1.7s ✅ (Target: <2s)
- New P95: 2.4s ✅ (Target: <3s)
- Functionality: All tests pass ✅
- Data freshness: 5-min delay acceptable ✅

**Step 5: Review**
```
@qa
*review docs/stories/4.2.optimize-dashboard.md
```

**Gate:** **PASS** ✅

**Improvements:**
- 79% reduction in load time
- 81% reduction in P95
- All functionality preserved

### Key Takeaways

- ✅ Establish baselines before optimization
- ✅ Measure after each change
- ✅ Multiple optimization techniques
- ✅ Validate functionality not broken
- ✅ Early NFR assessment guides work

---

## Security Enhancement

### Scenario
Adding two-factor authentication (2FA) to user accounts.

### Workflow

**Step 1: Create Security Story**
```
@po
*create-story
```

**Story:** Add Two-Factor Authentication

**AC:**
- Users can enable 2FA with authenticator apps
- 2FA required for sensitive operations
- Backup codes provided
- SMS fallback option
- Graceful degradation if service unavailable

**Step 2: Risk Assessment**
```
@qa
*risk docs/stories/1.5.add-2fa.md
```

**Risks:**
- Lockout scenarios (P=5, I=8, Score=40)
- SMS service failures (P=4, I=6, Score=24)
- Backup code mismanagement (P=3, I=7, Score=21)

**Mitigation:**
- Admin override for lockouts
- Fallback to email if SMS fails
- Secure backup code storage

**Step 3: Security-Focused Design**
```
@qa
*design docs/stories/1.5.add-2fa.md
```

**Test Strategy:**
- **Security Tests (P0):**
  - Brute force protection on 2FA codes
  - Backup code single-use validation
  - Rate limiting on verification attempts
  - Time-based code expiration
- **Unit Tests:**
  - TOTP code generation and validation
  - Backup code generation
  - SMS formatting
- **Integration Tests:**
  - 2FA enable/disable flow
  - Verification with authenticator
  - SMS delivery
- **E2E Tests:**
  - Complete 2FA enrollment
  - Login with 2FA enabled
  - Backup code usage
  - Account recovery

**Step 4: Implement**
```
@dev
*develop-story docs/stories/1.5.add-2fa.md
```

**Implementation:**
1. TOTP library integration
2. QR code generation for authenticator setup
3. Backup codes (cryptographically secure)
4. SMS integration with Twilio
5. Rate limiting (5 attempts per 15 minutes)
6. Admin override capability
7. Audit logging for all 2FA events

**Step 5: Security Review**
```
@qa
*review docs/stories/1.5.add-2fa.md
```

**QA Security Checks:**
- ✅ TOTP implementation follows RFC 6238
- ✅ Backup codes are cryptographically random
- ✅ Codes stored hashed, not plaintext
- ✅ Rate limiting prevents brute force
- ✅ Time window appropriate (30 seconds)
- ✅ SMS service failover implemented
- ✅ Audit trail complete
- ✅ Admin override requires MFA

**Gate:** **PASS** ✅

### Key Takeaways

- ✅ Security features need comprehensive threat modeling
- ✅ Multiple fallback mechanisms
- ✅ Audit logging essential
- ✅ Admin override with safeguards
- ✅ Follow established standards (RFC 6238)

---

## Summary: Pattern Recognition

### Greenfield Projects
- Start with architecture
- Break into small stories
- TDD throughout
- Standard QA flow

### Brownfield Projects
- **Always** risk assessment first
- Strangler fig pattern
- Feature flags
- Comprehensive regression testing
- Gradual rollout

### Integrations
- Error handling comprehensive
- Test with provider sandbox
- Idempotency critical
- Monitoring essential

### Bug Fixes
- Reproduce in test first
- Document root cause
- Regression tests
- Validate no side effects

### Performance Work
- Baseline first
- Measure continuously
- Multiple techniques
- Validate functionality preserved

### Security Features
- Threat modeling
- Follow standards
- Multiple fallbacks
- Comprehensive audit trails

---

**Last Updated**: 2025-10-22
