# Microservices Architecture Axioms

Core principles for designing, building, and operating microservices systems.

---

## Query & Consistency

| # | Axiom | Rationale |
|---|-------|-----------|
| 1 | **Queries are services** | Implement semantic queries once, reuse everywhere |
| 2 | **Prefer query consistency over ad-hoc convenience** | Centralized semantics enable tracing and correctness |
| 3 | **Immediate consistency means "real enough time"** | True real-time has explicit cost; near-real-time suffices |
| 4 | **Synchronous read paths must be feature-flagged** | Enable instant shutdown to protect the system |

---

## Edge & API Design

| # | Axiom | Rationale |
|---|-------|-----------|
| 5 | **Protocol-adaptive at edge, wire-native inside** | Accept any client protocol; convert to schema'd wireline objects internally |
| 6 | **[Protocol Handler → Wireline Publisher] → [Message Handler]** | Standard 2-part pattern for public APIs |

**Pattern:**
```
Client Request (HTTP/gRPC/WS)
    ↓
Protocol Handler (edge)
    ↓
Wireline Publisher (schema'd event)
    ↓
Message Bus
    ↓
Message Handling Service (internal)
```

---

## Testing & Operations

| # | Axiom | Rationale |
|---|-------|-----------|
| 7 | **If there is a knob, expose the knob** | Expose the control, the inputs, and the effect |
| 8 | **Operational sagas are first-class** | Control actions emit events: what changed, why, by whom |
| 9 | **Testing enables operation, not just correctness** | Tests validate observability, control paths, failure handling |
| 10 | **Software: 1% built, 99% operated** | Developer responsibility includes enabling safe operation |

---

## Deployment, Insight & Scope

| # | Axiom | Rationale |
|---|-------|-----------|
| 11 | **Nothing unwatched turns itself on** | Components must be observable before activation |
| 12 | **Scope defines responsibility** | Systems understand only their immediate sphere |
| 13 | **Don't reason beyond your sphere — escalate via insight** | Emit signals when something hurts; trust higher layers |
| 14 | **Systems Intelligence emerges from insight conversations** | Cross-scope systems consume insight streams for decisions |

---

## Production Readiness & Incident Response

| # | Axiom | Rationale |
|---|-------|-----------|
| 15 | **Customers report first = failure** | Breaks happen; surprise is the failure |
| 16 | **Detection precedes explanation** | Awareness and containment outrank root cause during incident |
| 17 | **No blame during incident response** | Fix first. Learn later. |
| 18 | **Postmortems exist for learning, not punishment** | Root cause analysis deferred until service is restored |

---

## Observability & Containment

| # | Axiom | Rationale |
|---|-------|-----------|
| 19 | **Observability over performance** | Trade 20-30% performance to eliminate blind spots |
| 20 | **If you cannot see it, you cannot trust it** | Incomplete visibility is an operational hazard |
| 21 | **Siloing/bulkheading is mandatory** | Choosing not to use = deployment decision; not having = architecture failure |

**Bulkheading dimensions:**
- Event slicing
- Traffic partitioning
- Fault domains
- Resource pools

---

## Security & Trust Foundations

| # | Axiom | Rationale |
|---|-------|-----------|
| 22 | **Trust must be explicit, scoped, and observable** | Implicit trust is a vulnerability |
| 23 | **Authenticate everything; authorize narrowly** | Identity = *who*; authorization = *what* and *how much* |
| 24 | **Trust is contextual, not absolute** | Trusted for one action ≠ trusted for another |
| 25 | **Loss of trust is an incident signal** | Auth failures must emit insight events |

---

## Trust Semantics & Decay

| # | Axiom | Rationale |
|---|-------|-----------|
| 26 | **Security context: explicit or implicit** | Explicit: credentials in envelope. Implicit: pointers to protected context |
| 27 | **Trust decisions belong near the resource** | Authorize close to data/actuator, not only at edge |
| 28 | **Trust is defined by promises** | Deterministic promise outputs (capabilities/scopes) |
| 29 | **Trust decays and revokes for many drivers** | Time, usage, violations, adjacency, graph participation |
| 30 | **Trust is a first-class participant** | Model as actor/service that emits promises and revocations |

---

## Jurisdiction, Audit & Provenance

| # | Axiom | Rationale |
|---|-------|-----------|
| 31 | **Jurisdiction is part of identity** | Context selection (region, regulatory, tenant) is not late-stage |
| 32 | **Critical workflows require immutable audit trails** | Safety outcomes need preserved decision paths |
| 33 | **Deterministic provenance is a trust primitive** | Prove which code/config produced an outcome |
| 34 | **Prefer dynamic identity/bootstrap over static config** | Let systems answer "who am I?" with current trust profile |

---

## Runtime Trust Profile (RTP)

| # | Axiom | Rationale |
|---|-------|-----------|
| 35 | **All execution under explicit Runtime Trust Profile** | Behavior without RTP is undefined and unsafe |
| 36 | **RTPs are time-bound, observable, revocable** | Long-lived implicit trust is a liability |
| 37 | **Policy changes via RTPs, not code patches** | Runtime behavior adapts via profiles, not emergency redeploys |

**RTP Components:**
```yaml
runtime_trust_profile:
  identity:       # Authenticated principal
  context:        # Jurisdiction, tenant, mission, regulatory scope
  capabilities:   # Allowed actions as trust promises
  constraints:    # Limits, conditions, expiries
  isolation:      # Silo/bulkhead assignment
  provenance:     # Code/config references in effect
  expiry:         # Time or signal-driven validity
```

---

## One-Line Summary

> We are not optimizing for clever code — we are optimizing for systems we can **run, trust, and evolve**.
