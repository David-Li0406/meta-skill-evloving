---
name: security-threat-review
description: Security review and pragmatic threat modeling for endpoints, authentication, sensitive data, and integrations. Use when there is user input, authentication, sensitive data handling, or payments.
---

# Name

security-threat-review

---

## Purpose

Guide **pragmatic security and threat analysis** for applications, APIs, and integrations **without assuming tooling, maturity, or security posture upfront**.

This skill helps identify **realistic threats, attack surfaces, and failure modes** based on what actually exists in the repo and system context — not on generic checklists.  
The goal is to produce **defensible, technically grounded security decisions** that scale from early-stage repositories to mature systems and are compatible with **Codex, Copilot, and human review**.

---

## When to use

Use this skill when:

- Introducing new user inputs, APIs, or endpoints  
- Handling authentication, authorization, or identity flows  
- Processing, storing, or transmitting sensitive data (PII, tokens, secrets, payments)  
- Integrating external services, webhooks, or third-party SDKs  
- Preparing for a release with elevated risk or exposure  
- Investigating security concerns, incidents, or near-misses  

---

## Inputs required

Before analyzing threats or proposing mitigations, gather:

- Critical user flows and system boundaries  
- Types of data handled (public, internal, sensitive, regulated)  
- Authentication and authorization model (if any)  
- External dependencies and integrations  
- Deployment environments and access patterns  
- Risk tolerance and business constraints  

If any of this context is missing, **stop and ask the DEV**.

### Mandatory DEV questions

- What data or capabilities would cause the most damage if compromised?
- How do users and systems authenticate and gain access today?
- Which inputs are user-controlled or externally sourced?
- Are there regulatory, compliance, or contractual constraints?
- What level of risk is acceptable for this system at its current stage?

---

## Repo Signals (observation)

Capture **only observable facts** from a quick repository scan.  
If something is unclear, record it as **Unknown** and confirm with the DEV.

- **Stack**: Languages, runtimes, frameworks
- **Entry points**: APIs, forms, CLIs, jobs, webhooks
- **Auth signals**: Presence of auth middleware, tokens, sessions, RBAC hints
- **Data handling**: Storage layers, serialization, encryption hints
- **Secrets management**: Env vars, config files, secret usage patterns
- **Testing maturity**: Security tests, negative tests, fuzzing
- **CI/CD**: Automation, secret scanning, deploy gates
- **Operational exposure**: Public endpoints, admin paths, internal tooling

Do **not** infer intent or best practices. Record what is visible.

---

## Implications (interpretation)

From the observed Repo Signals and inputs, derive implications such as:

- Likely attack surfaces and trust boundaries
- High-impact vs high-probability threat areas
- Gaps between data sensitivity and current protections
- Risk introduced by missing tests, logging, or isolation
- Operational or organizational limits on mitigation depth

Explicitly state assumptions and unknowns.

---

## Process

1. **Validate observations**  
   Ask the DEV:  
   > “Can I proceed assuming these repository signals are accurate?”

2. **Define assets and trust boundaries**  
   Identify what must be protected and where trust changes.

3. **Map attack surfaces and threat scenarios**  
   Focus on realistic misuse, abuse, and failure modes.

4. **Identify constraints**  
   Technical, organizational, time, cost, or compliance-related.

5. **Generate options from context**  
   Produce **at least two and preferably three** mitigation approaches grounded in the analysis above.

6. **Evaluate options objectively**  
   Compare risk reduction, cost, complexity, and residual exposure.

7. **Recommend and confirm**  
   Make a defensible recommendation and request approval before action.

---

## Options & trade-offs

Based on the analysis above, generate **context-specific options**.  
Do **not** use predefined security templates or fixed models.

Each option must differ meaningfully in **scope, cost, risk reduction, and operational impact**.

For **each option**, include:

- **Description**: What changes or controls are introduced
- **Threats addressed**: Which risks this option mitigates
- **Pros**: Concrete security and operational benefits
- **Cons**: Limitations, complexity, or residual risks
- **Implementation cost**: Engineering and coordination effort
- **Operational impact**: Ongoing maintenance or monitoring
- **Residual risk**: What remains exposed
- **Preconditions**: Tests, tooling, access, or process changes required

If only two options are viable, explain why a third is not reasonable.

---

## Recommendation

Select the option that provides the **best cost–benefit trade-off** given:

- Severity and likelihood of identified threats
- Data sensitivity and blast radius
- Repo and team maturity
- Time-to-mitigate requirements
- Benchmarks from similar systems or prior incidents (if available)

### Rationale (required)

Provide a concise rationale (3–6 bullets) explaining:

- Why this option fits the current constraints
- Which trade-offs are consciously accepted
- Which risks are deferred and why
- How remaining risk can be monitored or reduced later
- What assumptions are being made if benchmarks are missing

---

## Output format

The final response must include:

1. Confirmed Repo Signals  
2. Asset and threat mapping  
3. Identified gaps and constraints  
4. Generated options with trade-offs  
5. Clear recommendation with rationale  
6. Mitigation rollout and validation plan  
7. Open questions for the DEV  

---

## Safety checks

- Do not log secrets, credentials, or sensitive payloads
- Avoid security controls that silently break user flows
- Prevent false sense of security from partial mitigations
- Ensure mitigations are testable and observable
- Treat early threat analysis as iterative, not final

---

## Dev confirmation gates

Explicit DEV approval is required before:

- Changing authentication or authorization behavior
- Introducing new security middleware or infrastructure
- Collecting or storing sensitive or regulated data
- Enforcing breaking security constraints
- Accepting or documenting residual risk

Without confirmation, **do not proceed**.
