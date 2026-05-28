# Prompt Engineering Templates

Quick reference for proven prompting frameworks. Use these templates to structure your prompts effectively.

---

## CO-STAR: Writing & Content Creation

**Use for**: Marketing copy, technical documentation, business communications, content generation

**Components**: **C**ontext, **O**bjective, **S**tyle, **T**one, **A**udience, **R**esponse format

**Template**:
```
Context: [Background and situation]
Objective: [What you want to accomplish]
Style: [Writing style - formal, casual, technical, etc.]
Tone: [Emotional quality - professional, enthusiastic, etc.]
Audience: [Who will read this and their characteristics]
Response format:
- [Section 1]
- [Section 2]
- [etc.]
```

**Example**:
```
Context: Launching new API feature for real-time webhook notifications for payment events.
Objective: Write product announcement blog post generating excitement and driving adoption.
Style: Technical but accessible, conversational yet professional
Tone: Enthusiastic and developer-friendly
Audience: Software developers integrating with our payment API
Response format:
- Catchy headline (under 60 characters)
- Opening paragraph (2-3 sentences)
- "What's New" section with technical details
- "Why This Matters" section
- "Getting Started" with code example
- Call-to-action
```

---

## ROSES: Decision Support

**Use for**: Strategic business decisions, technical architecture choices, resource allocation, risk assessment

**Components**: **R**ole, **O**bjective, **S**cenario, **E**xpected Output, **S**tyle

**Template**:
```
Role: [Perspective to take, expertise level]
Objective: [Specific decision to be made]
Scenario:
- [Current state]
- [Key constraints]
- [Available resources]
- [Relevant background]
Expected Output:
- [Format element 1]
- [Format element 2]
- [etc.]
Style: [How to present - data-driven, practical, etc.]
```

**Example**:
```
Role: CTO evaluating infrastructure decisions for rapidly growing startup
Objective: Decide whether to adopt Kubernetes for microservices architecture
Scenario:
- 12 microservices on EC2 with manual bash deployment
- Team of 8 engineers, 3 have container experience
- Growing 30% quarter-over-quarter
- Deployment issues causing 2-3 hour downtime monthly
- Budget allows 2-3 months of infrastructure work
Expected Output:
- Clear recommendation (Kubernetes, stay on EC2, or hybrid)
- 3-5 key decision factors ranked by importance
- Risk assessment with mitigation strategies
- Implementation timeline
- Estimated engineering time investment
Style: Data-driven and practical, focused on team capabilities and business impact
```

---

## Architecture-First: Software Development

**Use for**: New features, components, refactoring, integrations, code generation

**Pattern**: Context → Goal → Constraints → Technical Requirements

**Template**:
```
Context: [Existing system architecture, tech stack, current implementation]
- [Tech stack]
- [Current implementation]
- [Integration points]

Goal: [What to implement]

Constraints:
- [Non-negotiable limit 1]
- [Non-negotiable limit 2]
- [Non-negotiable limit 3]

Technical Requirements:
- [Specific approach/tool 1]
- [Specific approach/tool 2]
- [Specific approach/tool 3]

[Request architecture design first, then implementation]
```

**Example**:
```
Context: Express.js API with PostgreSQL. JWT tokens in PostgreSQL sessions table.
API serves 5000+ requests/minute during peak. Running on AWS with 4 EC2 instances.

Goal: Implement rate limiting to prevent API abuse on authentication endpoints.

Constraints:
- Must work with existing JWT auth without code changes
- Should not add latency >10ms (p95)
- Scale across multiple instances (shared state)
- Cannot require additional database queries per request

Technical Requirements:
- Use Redis for distributed rate limit tracking (already running for cache)
- Implement sliding window algorithm
- Different limits for authenticated vs unauthenticated
- Configurable limits per endpoint
- Return 429 with Retry-After header
- Integrate with existing structured logging

Provide architecture design first, then implement rate limiting middleware.
```

---

## Security-First Two-Stage: Security-Critical Code

**CRITICAL**: Research shows 40%+ of AI code has vulnerabilities without explicit security prompting.

**Use for**: User input handling, authentication, payments, database queries, file operations, API integrations

**Pattern**: Stage 1 (Functional) → Stage 2 (Security Hardening)

**Stage 1 Template**:
```
Implement [feature description]:
- [Functional requirement 1]
- [Functional requirement 2]
- [Functional requirement 3]

Provide the implementation.
```

**Stage 2 Template**:
```
Review the [feature name] for security vulnerabilities:

[PASTE CODE FROM STAGE 1]

Harden against:
- SQL injection / NoSQL injection
- XSS (Cross-Site Scripting)
- CSRF (Cross-Site Request Forgery)
- Command injection / Path traversal
- Input validation bypass
- Authentication/authorization bypass
- Information disclosure in errors
- Hard-coded credentials
- [Other relevant vulnerabilities]

Provide security-hardened version with security comments.
```

**Example**:

*Stage 1*:
```
Implement user registration endpoint for Express.js API:
- Accept email, password, username
- Validate email format
- Hash password with bcrypt
- Store in PostgreSQL users table
- Return success with user ID or error response
```

*Stage 2*:
```
Review this registration endpoint for security vulnerabilities:

[PASTE CODE]

Harden against:
- SQL injection (parameterized queries)
- Email injection
- Password policy (min 12 chars, complexity)
- Rate limiting (prevent brute force)
- Input sanitization (username restrictions)
- Error message disclosure (don't reveal if email exists)
- Timing attacks on checks
- Bcrypt salt rounds (secure hashing)
- Input length limits (prevent DoS)

Provide security-hardened version.
```

---

## Quick Selection Guide

| Task Type | Framework | Key Benefit |
|-----------|-----------|-------------|
| Blog posts, docs, marketing | CO-STAR | Complete content specification |
| Business decisions, architecture | ROSES | Structured analysis & recommendation |
| Code generation, features | Architecture-First | Prevents misaligned solutions |
| Auth, payments, user input | Security Two-Stage | 50%+ vulnerability reduction |

---

## General Tips

1. **Be specific** - Vague inputs produce vague outputs
2. **Include examples** - Show desired format when possible (except reasoning models)
3. **State constraints explicitly** - "Must" and "Cannot" are clear
4. **Provide context about WHY** - Helps models make better decisions
5. **Match format to output** - Structure your prompt like desired output
6. **For Claude 4**: Be even more explicit, don't assume error handling
7. **For security code**: Always use two-stage approach
