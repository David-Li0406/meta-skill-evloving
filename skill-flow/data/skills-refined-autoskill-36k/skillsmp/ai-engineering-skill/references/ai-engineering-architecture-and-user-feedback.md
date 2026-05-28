# AI Engineering Architecture and User Feedback — Practitioner Reference

This reference distills Chapter 10 into actionable patterns, decision frameworks, and code you can reuse to design, scale, and monitor AI applications and collect high-quality user feedback.

---

## System Architecture Progression (When to Add What)

- Start simple: App → Model API → Response
- Add components only when a pain is clear (quality, cost, latency, risk)

Architecture expansion path:
1) Enhance Context (RAG, tools) when the model needs facts or current data
2) Guardrails when you see safety, leakage, or format failures
3) Router and Gateway when you have multiple models, vendors, or need governance
4) Caching when latency/cost matters and results repeat
5) Agent Patterns for loops, branching, and write actions
6) Monitoring and Observability from day one, deepen with complexity
7) Orchestration when pipelines become multi-step and fragile to hand-wire

---

## Step 1: Enhance Context (RAG + Tools)

When to use
- The base model hallucinates or lacks domain facts
- Outputs require proprietary or fresh data (docs, DBs, APIs)

What to add
- Retrieval: text, images, tables; tune chunking, filters, rerankers
- Tools: web search, news, weather, DB/SQL, code interpreter, custom APIs

Decision framework
- Vendor attachments/tools vs custom RAG:
  - Use vendor attachments/tools if: small document sets, low complexity, speed > control
  - Use custom RAG if: large corpora, custom chunking/reranking, hybrid search, control over retrieval metrics/logging

Implementation notes
- Track retrieval quality (precision, relevance)
- Keep a retrieval budget per query (tokens/time)
- Use source citations for trust
- Consider per-tool latency SLA and graceful timeouts

---

## Step 2: Guardrails (Input and Output)

Goals
- Reduce sensitive data leakage, prompt injection, abuse
- Catch low-quality or unsafe outputs; define recovery policies

Where to place
- Input: PII/redaction, prompt-attack filters, scope checks
- Output: JSON/schema validation, moderation, fact checking, brand safety
- Trade-off: more guardrails → more latency; choose by risk tolerance

Streaming caveat
- Output guardrails struggle with streaming; consider:
  - Pre-generation safety checks (e.g., task intent)
  - Small “preview window” internal buffer before streaming tokens to users
  - Inline repair post-stream (e.g., append correction note)

Retry/fallback policy
- Empty/malformed → retry N times (or run K calls in parallel and pick best)
- Unsafe → regenerate with stricter prompt; redact; route to human
- Complex/angry users → handoff to human after threshold turns/sentiment

Common guardrail tools
- Moderation APIs (OpenAI, Perspective)
- Frameworks (NVIDIA NeMo Guardrails, Purple Llama, Azure content filters/PyRIT)
- Your classifiers for domain-specific risks

Code pattern: Input PII masking with reversible map
```python
import re, uuid

SENSITIVE_PATTERNS = {
    "PHONE": r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?){2}\d{4}\b",
    "EMAIL": r"\b[a-zA-Z0-9._%+-]+@[\w.-]+\.[A-Za-z]{2,}\b",
}

def mask_pii(text: str):
    reverse_map = {}
    masked = text
    for label, pattern in SENSITIVE_PATTERNS.items():
        def repl(m):
            token = f"[{label}:{uuid.uuid4().hex[:8]}]"
            reverse_map[token] = m.group(0)
            return token
        masked = re.sub(pattern, repl, masked)
    return masked, reverse_map

def unmask_pii(text: str, reverse_map: dict):
    for tok, original in reverse_map.items():
        text = text.replace(tok, original)
    return text

# usage
masked, rev = mask_pii(user_input)
safe_output = call_external_model(masked)
final = unmask_pii(safe_output, rev)
```

Code pattern: Robust JSON extraction with repair loop
```python
import json, time

def generate_valid_json(prompt, call_model, max_attempts=3):
    repair_prompt = "Return only valid JSON that matches this schema: ..."

    for attempt in range(1, max_attempts+1):
        text = call_model(prompt if attempt==1 else repair_prompt + "\n" + text)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            time.sleep(0.2 * attempt)

    # last attempt: ask model to fix malformed json string explicitly
    fixer_prompt = f"Fix this to valid JSON only. No explanations.\n{text}"
    fixed = call_model(fixer_prompt)
    return json.loads(fixed)  # may still throw; handle upstream
```

Code pattern: Parallel “speculative” calls to reduce tail latency
```python
import concurrent.futures as cf

def parallel_generate(prompt, providers, pick_best):
    # providers: list of callables returning (text, score_meta)
    with cf.ThreadPoolExecutor() as ex:
        futures = [ex.submit(p, prompt) for p in providers]
        results = [f.result() for f in cf.as_completed(futures)]

    # pick_best inspects quality/format/safety meta and selects
    return pick_best(results)
```

Checklist: Minimal guardrail MVP
- Input: PII mask + out-of-scope intent rejection
- Output: Schema/format validator + moderation + retry/fallback
- Logging: all violations with trace IDs, redacted data
- Handoff: human-in-loop path on high-risk or repeated failures

---

## Step 3: Model Router and Gateway

### Routers

Use when
- Different tasks need different models/pipelines
- Save cost by routing simple queries to smaller models
- Handle out-of-scope/ambiguous queries early

Router types
- Rules: keywords, regexes (fast, brittle)
- Small classifiers: BERT/Llama-7B finetunes (fast, robust)
- LM-as-router: few-shot classification with prompting (flexible, slower)

What routers predict
- Intent (billing vs tech support vs sales)
- Next action (search vs code interpreter vs DB query)
- Memory source (conversation vs attached doc vs internet)
- Human handoff triggers

Performance targets
- <15 ms eval for intent routers
- High precision for “block/unsafe” routes to avoid false refusals

Router flow (before retrieval)
- In-scope? If no → stock decline response; log
- Needs retrieval? If yes → pick data sources, chunking, filters
- Needs tools? If yes → select and budget time

Code pattern: Router skeleton
```python
def route(query, clf, tools_registry):
    intent = clf.predict(query)  # returns label + confidence
    if intent == "out_of_scope":
        return {"action": "respond_stock", "template": "decline"}

    needs_retrieval = intent in {"troubleshoot", "research"}
    next_tool = None
    if needs_retrieval:
        next_tool = "search_api"
    elif "code" in query.lower():
        next_tool = "code_interpreter"

    return {"intent": intent, "next_tool": next_tool}
```

Context-fit decision
- If new context exceeds target model limit, either:
  - Truncate context strategically (keep high-relevance chunks), or
  - Re-route to larger-context model
- Prefer re-route when truncation risks quality

### Gateways

Use when
- Multiple providers (OpenAI/Claude/Gemini/self-hosted)
- Need access control, cost caps, usage quotas, fallbacks
- Centralized logging/analytics/AB testing

Gateway responsibilities
- Unified API across vendors; decouple app code from vendor changes
- AuthN/AuthZ, per-user/app quotas, rate-limit smoothing
- Fallbacks for errors/rate limits; retries with jitter
- Load balancing, caching, guardrails (optional), logging/metrics

Code skeleton: Gateway with fallback and quotas (FastAPI-style)
```python
from fastapi import FastAPI, Request, HTTPException
import time, uuid

app = FastAPI()

PROVIDERS = {
    "openai:gpt-4o": call_openai,
    "anthropic:claude-3.5": call_anthropic,
    "google:gemini-1.5-pro": call_gemini,
    "local:llama-3-8b": call_local_llm,
}

QUOTAS = {}  # {api_key: {"tokens_used": 0, "reset_at": ts}}

def pick_provider(route_hint):
    # simple policy; expand with AB tests, price, SLA
    return route_hint if route_hint in PROVIDERS else "openai:gpt-4o"

@app.post("/generate")
async def generate(req: Request):
    payload = await req.json()
    api_key = req.headers.get("X-API-Key")
    if not api_key or not authorized(api_key):
        raise HTTPException(401, "Unauthorized")

    enforce_quota(api_key, payload)

    trace_id = str(uuid.uuid4())
    model = pick_provider(payload.get("model"))
    input_data = payload["input"]

    try:
        text, meta = try_with_fallbacks(model, input_data)
    except Exception as e:
        log_error(trace_id, payload, e)
        raise HTTPException(503, "Upstream failure")

    record_usage(api_key, meta)
    log_success(trace_id, payload, meta)
    return {"trace_id": trace_id, "text": text, "meta": meta}

def try_with_fallbacks(primary, input_data):
    providers = [primary, "anthropic:claude-3.5", "local:llama-3-8b"]
    for pid in providers:
        try:
            return PROVIDERS[pid](input_data)
        except TransientError:
            time.sleep(0.2)
            continue
    raise RuntimeError("All providers failed")
```

Governance checklist
- Single org token per vendor kept in gateway only
- Per-app/user model allowlist; per-route spending caps
- Usage dashboard: tokens, RPM/TPM, failures, P95 latency per model
- Fallback matrix + alerting for escalation

---

## Step 4: Caching to Reduce Latency/Cost

Cache types
- Exact cache: reuse when inputs are identical
- Semantic cache: reuse when inputs are semantically similar (embedding + threshold)

What to cache
- Full generations for deterministic prompts
- Retrieval results (vector search hits, SQL query results, web search)
- Tool outputs (API calls), reranker results
- Post-processed outputs (validated JSON)

Eviction and validity
- Eviction: LRU/LFU/FIFO; tiered storage (memory → Redis → disk)
- TTL by content type (short for time-sensitive; longer for static)
- Per-tenant segmentation; never mix user-scoped outputs in shared cache without scoping keys

Security warning
- Do not cache user-personalized outputs globally. Key cache by user_id + query_fingerprint.
- Include a “context fingerprint” (e.g., hash of retrieved doc IDs) so a cache hit only returns if the same context was used.

Decision table: Exact vs Semantic Caching
| Aspect | Exact Cache | Semantic Cache |
|---|---|---|
| Hit condition | Identical key | Similarity above threshold |
| Dependencies | Hash KV store | Embeddings + vector DB |
| Risk | Low (if keys scoped) | Higher (wrong matches) |
| Cost/latency | Very low | Higher (embedding + search) |
| Best for | Repeated prompts, tool outputs | High-repeat FAQ-like queries |

Code pattern: Exact cache wrapper (Redis)
```python
import hashlib, json, redis
r = redis.Redis()

def cache_key(user_id, prompt, context_ids=None, model=None):
    payload = {
        "u": user_id,
        "p": prompt,
        "c": context_ids or [],
        "m": model
    }
    return "gen:" + hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

def cached_generate(user_id, prompt, context_ids, model, gen_fn, ttl=3600):
    key = cache_key(user_id, prompt, context_ids, model)
    hit = r.get(key)
    if hit:
        return json.loads(hit)

    out = gen_fn(prompt, context_ids)
    r.setex(key, ttl, json.dumps(out))
    return out
```

Code pattern: Semantic cache check
```python
def semantic_cache_lookup(query, embed, vdb, threshold=0.86):
    qv = embed(query)
    # vdb returns [(key, score, result), ...] sorted desc
    top = vdb.search(qv, top_k=1)
    if top and top[0].score >= threshold:
        return top[0].result
    return None
```

Should-I-cache classifier
- Train a small classifier to predict cache-worthiness:
  - Features: user scope, time sensitivity, expected reuse, cost of generation
  - Label: future hit within time window

---

## Step 5: Agent Patterns and Write Actions

Agent patterns
- Loops: reflect → retrieve → refine → generate
- Parallel: plan subtasks and run tools concurrently
- Conditional branching: next-action prediction with budget control

Write actions (high risk, high leverage)
- Examples: send email, create ticket, place order, bank transfer
- Controls:
  - Approval gates: ask user “Proceed?” with diff of changes
  - Dry-run mode: show intended actions before execution
  - Scopes: least privilege API keys per tool; RBAC enforced
  - Sandboxes: execute code in jailed runtime with resource limits
  - Rate limits: per-user/action thresholds
  - Audit logs: tamper-evident trail; idempotency keys; retries safe

Checklist: Enabling write actions safely
- Model-to-tool contract schema with strict validation
- User-visible confirmation for side-effectful actions
- Rollback/undo paths where possible
- Alert on abnormal burst patterns or high-risk actions
- Periodic red-team tests for prompt-injection to trigger write actions

---

## Monitoring and Observability

Core goals
- Reduce MTTD (detect issues fast) and MTTR (fix faster)
- Keep CFR low by catching issues pre-deploy and correlating post-deploy

Metrics by category
- Quality:
  - Format failure rate (invalid JSON); auto-repair success rate
  - Factual consistency (AI judge), relevance/grounding, hallucination flags
  - Refusal rate; toxicity or brand-risk incidence
- Retrieval:
  - Context precision, relevance, coverage; reranker gains; zero-hit rate
- Latency:
  - TTFT (time to first token), TPOT (time per output token), total latency
  - Breakdown per step: routing, retrieval, model, tool calls
- Cost/usage:
  - Input/output tokens per request, TPS/RPS, per-user quotas, cache hit rate
- Feedback:
  - Early termination rate; regeneration rate; thumbs up/down; complaint categories
  - Conversation length vs diversity; handoff-to-human rate
- Guardrails:
  - Trigger counts by type; false refusal estimates; streaming leaks

Make metrics sliceable by
- User segment, app/version, prompt/chain version, model/provider, time window

Logging: log everything, structure it
- Log fields:
  - trace_id, user_id (pseudonymized), session_id
  - model/provider, version, sampling params
  - prompt template version, system prompt hash
  - input text (redacted), retrieved doc IDs/hashes, tool calls + outputs (redacted)
  - output text (redacted), tokens in/out, latency per step, cost estimates
  - guardrail triggers, retries, fallbacks used
- Use JSON logs; ensure PII redaction consistent before persistence

Traces: reconstruct end-to-end path
- Each span: name, start/end, latency, cost, inputs (hash/ids), outputs (hash/ids), status
- Visualize pipeline: route → retrieve → rerank → prompt → generate → validate → post-process
- Alert on anomalies: e.g., retrieval span = 0 docs, decode error spikes

Drift detection
- System prompt drift: hash and alert on changes
- User behavior drift: query length distribution, topics, sentiment trends
- Model drift (API updates): monitor reference suites nightly; canary route traffic and compare metrics
- Retrieval/data drift: doc churn, index size, embedding distribution shift

Sampling for monitoring
- Exhaustive checks for format/latency; sampled AI-judged quality for cost control
- Daily manual review of a small random set; refine prompts/metrics based on findings

---

## Orchestration (When to Introduce + Requirements)

When to add an orchestrator
- You have multi-step pipelines with branching/loops/tools
- Hand-coded chains are brittle; need reuse, visibility, testing

Evaluate orchestrators by
- Integration: supports your models, vector DBs, tools, evaluators
- Extensibility: easy to add unsupported components
- Pipeline features: branching, parallelism, retries, error handling, typed IO
- Performance: minimal hidden calls/latency; scalable under load
- Observability: IDs, spans, costs surfaced; easy tracing
- Avoid lock-in: keep chain logic declarative and testable

Parallelization tip
- Do routing and PII stripping concurrently
- Parallel tool calls with independent inputs; fan-in with timeouts

Warning
- Start simple without an orchestrator if possible; add later to avoid premature complexity

---

## Conversational User Feedback (Extraction and Use)

Feedback types
- Explicit: thumbs up/down, ratings, side-by-side votes, “Did this solve your problem?”
- Implicit: user actions and language in conversation

Use feedback for
- Evaluation: health metrics; failure taxonomy
- Development: preference finetuning; prompt/chain evolution
- Personalization: user-specific preferences and constraints

Natural language signals
- Early termination: stop generation, exit app, “stop” in voice → negative signal
- Error correction: “No,” “I meant,” rephrasing → previous reply off-target
- Direct complaints: wrong/irrelevant/unsafe/too long/lacking detail/repetitive
- Source/trust cues: “show sources,” “are you sure?” → confidence gap
- Sentiment shifts: frustration vs resolution
- Model refusal phrases: refusal rate is a strong UX risk signal

Other conversational signals
- Regeneration: indicates dissatisfaction (but can also seek alternatives)
- Conversation organization: delete (bad or private), rename (good but title poor), bookmark/share (useful or surprising)
- Conversation length and diversity:
  - Productivity bots: long threads may indicate inefficiency (or complex tasks)
  - Companions: long, diverse threads are positive
  - Watch for loops (low diversity, repetitive bot content)

When to collect feedback
- Onboarding: optional calibration (persona, tone, goals); avoid friction
- On errors: downvote, explain issue; offer fix/regenerate/handoff
- Low-confidence: ask targeted choice (short vs detailed summary)
- Exceptional wins: occasionally solicit positive feedback (rate-limit to avoid annoyance)

How to collect (UI patterns)
- Minimize disruption; 1-click actions; keyboard shortcuts
- Provide “edit response” surfaces (edits become strong preference data)
- Side-by-side comparison:
  - Full or partial previews; randomize order; track dwell/click
  - Offer “I can’t tell/I don’t know” option
- Midjourney-style affordances (upscale/variations/regenerate) to infer preference strength
- Code assistants: implicit accept (Tab) vs ignore (continue typing)

Context capture and consent
- Tie feedback to recent context (last N turns, tools, retrieved docs) with explicit consent
- Clearly state use: personalization only vs product analytics vs model training
- Offer opt-out and data deletion controls

Biases and mitigations
- Leniency bias: avoid punitive flows for low ratings; use descriptive labels instead of star numbers
- Randomness: ask for rationale occasionally; add gold checks; filter low-effort signals
- Position bias: randomize order; debias with position-aware metrics
- Recency/length bias: normalize comparisons; limit display length differences

Degenerate feedback loops (avoid)
- Exploration/exploitation:
  - Use epsilon-greedy or Thompson sampling in selection of prompts/models
  - Diversify slates; cap exposures of popular items
- Counterfactual logging:
  - Log propensities/probabilities for chosen actions for IPS (inverse propensity scoring)
- Periodic resets and audits:
  - Evaluate on unbiased test sets; detect sycophancy and overfitting to preferences
- Guardrails over feedback:
  - Don’t let feedback override safety or factuality checks

---

## Data Governance and Privacy for Feedback

- PII redaction on logs/feedback; reversible mapping only inside secure boundary
- Tenant isolation: scope caches and feedback by tenant/user where required
- Policy flags:
  - Personalization only
  - Analytics only
  - Train global models
- On-device processing where feasible; aggregate/federated signals for privacy
- Data retention limits; DSAR compliance; transparent user controls

---

## Quick Reference Checklists

Architecture rollout MVP
- [ ] Single model via gateway
- [ ] PII input mask; simple moderation on output
- [ ] JSON/schema validator with retry
- [ ] Basic logs with trace_id; TTFT and total latency metrics

Add context (RAG/tools)
- [ ] Chunking tuned; retriever precision validated
- [ ] Tool timeouts and budgets
- [ ] Source citations included
- [ ] Retrieval metrics dashboards

Guardrails baseline
- [ ] Input: PII + prompt injection patterns
- [ ] Output: moderation + schema validate/repair
- [ ] Parallel speculative calls for reliability without latency spike
- [ ] Handoff criteria and flow

Router/gateway
- [ ] Intent classifier <15 ms
- [ ] Out-of-scope declines
- [ ] Model allowlist per app/user; quotas and caps
- [ ] Fallbacks + AB testing harness

Caching
- [ ] Exact cache keys scoped by user + context fingerprint
- [ ] TTL by content type; LRU eviction
- [ ] Optional semantic cache only if hit rate > cost
- [ ] “Should I cache?” classifier

Agent/write actions
- [ ] Tool schemas + strict validators
- [ ] Approvals for side-effectful actions
- [ ] Idempotency keys; audit trail
- [ ] Sandboxed code execution

Observability
- [ ] JSON structured logs with redaction
- [ ] Traces per step (route/retrieve/generate/validate)
- [ ] Quality/latency/cost dashboards; alerts on spikes
- [ ] Drift monitors for prompts/models/user behavior

Feedback system MVP
- [ ] Thumbs up/down + optional rationale
- [ ] Regenerate + compare; randomize order; “can’t tell” option
- [ ] Edit response UI for code/text; capture diffs
- [ ] Consent flow for context sharing

---

## Common Pitfalls and Remedies

- Pitfall: Streaming unsafe content before moderation
  - Remedy: Pre-check task intent; micro-buffers; rapid inline moderation
- Pitfall: Caching leaks user info across tenants
  - Remedy: Include user_id and context fingerprint in cache keys; segregate caches
- Pitfall: Overzealous guardrails (false refusals)
  - Remedy: Measure false refusal rate; tune thresholds; add escalate-on-uncertainty
- Pitfall: Router adds more latency than it saves
  - Remedy: Use tiny classifiers; cache router decisions per session
- Pitfall: Semantic cache degrades quality
  - Remedy: Start with exact-only; require high similarity; track quality delta
- Pitfall: Write actions triggered by prompt injection
  - Remedy: Tool-use confirmation; strict schema; dual-model approval; content origin filters
- Pitfall: Opaque pipelines hard to debug
  - Remedy: Trace IDs everywhere; span timing/costs; reproducible replay with redacted payloads
- Pitfall: Feedback loops biasing the system
  - Remedy: Enforce exploration; counterfactual evaluation; regular audits

---

## Decision Tables

Guardrail placement
| Placement | Pros | Cons | Use when |
|---|---|---|---|
| Provider-level (vendor defaults) | Zero-integration | Limited control, opaque | Low-risk apps; quick start |
| Gateway | Centralized policy, per-app/user control | Requires build/ops | Multi-app org; want governance |
| App layer | Full context; custom logic | Duplicated effort per app | App-specific risks/format checks |

Streaming vs non-streaming
| Mode | Pros | Cons | Use when |
|---|---|---|---|
| Streaming | Low perceived latency; better UX | Harder safety/format checks | Chat UX; long generations |
| Non-streaming | Full validation before display | Higher wait time | High-risk outputs; strict JSON/API responses |

Orchestrator adoption
| Signal | Recommendation |
|---|---|
| 1–2 steps, rare branching | Hand-wire; keep simple |
| 3–6 steps, branching/loops, retries | Introduce orchestrator |
| Many apps share components | Orchestrate + library of reusable blocks |
| Heavy SLAs/observability needs | Orchestrator with tracing integration |

---

## Reusable Prompts/Patterns

Router prompt (LM-as-router)
```
You are a router. Given the user message, output a JSON object:
{ "intent": one of ["billing","tech_support","sales","out_of_scope"],
  "needs_retrieval": true|false,
  "next_tool": one of ["search_api","code_interpreter","none"] }

Respond with JSON only. Message: "<USER_MESSAGE>"
```

Hallucination check (AI judge)
```
Given: (Question), (Context), (Answer).
Decide if the Answer is supported by the Context. Output one of:
"supported", "unsupported", or "partially_supported", and a brief reason.
Return JSON: {"label": "...", "reason": "..."}.
```

JSON schema enforcement (system instructions)
```
Always return a single JSON object that validates against this schema:
<insert JSON Schema>.
Do not include explanations or extra fields.
```

Comparative feedback UI copy
- “Which response better answers your question?”
- Buttons: “A”, “B”, “About the same”, “I can’t tell”
- Tooltip: “We use your selection to improve future answers. No personal data is shared.”

---

## Example: End-to-End Flow (Putting It Together)

1) Preprocess
- PII mask input; assign trace_id; parallel-run router and PII
2) Route
- Intent classifier: tech_support; needs retrieval: yes
3) Retrieve
- Vector search (top-8); rerank (keep top-4); context fingerprint computed
4) Prompt
- Assemble with system prompt v12; template v3; sampling params logged
5) Generate
- Gateway calls primary model; parallel speculative second call
6) Validate
- JSON schema check; moderation; hallucination judge (if high-risk)
- If fail: retry/repair or fallback to other model; if still fail: handoff to human
7) Cache
- Exact cache store with user_id + context_fingerprint key
8) Stream/Return
- Stream tokens or return full; unmask PII
9) Observe
- Log spans, latencies, tokens, costs; update dashboards
10) Feedback
- Offer “good/bad”; if regenerate, side-by-side with randomized order

---

## Minimal Implementations (Copy/Paste Starters)

Structured logging with trace_id
```python
import json, time, uuid, sys

def log(event, **kwargs):
    payload = {"ts": time.time(), "event": event, **kwargs}
    sys.stdout.write(json.dumps(payload) + "\n")

trace_id = str(uuid.uuid4())
log("request_start", trace_id=trace_id, user="anon", model="gpt-4o")

# later
log("retrieval", trace_id=trace_id, docs=["d12","d58"], latency_ms=43)
log("generate", trace_id=trace_id, tokens_in=834, tokens_out=215, latency_ms=1220, provider="openai")
log("guardrail", trace_id=trace_id, type="moderation_ok")
log("response_end", trace_id=trace_id, total_latency_ms=1520)
```

Sentiment/complaint classifier (lightweight rules fallback)
```python
NEGATIVE_CUES = ["this is wrong", "not what i asked", "too long", "irrelevant", "useless", "stop"]
CORRECTION_CUES = ["no,", "i meant", "that's not", "actually,"]

def feedback_signals(user_msg, action):
    s = user_msg.lower()
    signals = []
    if action == "stop_generation": signals.append("early_termination")
    if any(c in s for c in NEGATIVE_CUES): signals.append("complaint")
    if any(c in s for c in CORRECTION_CUES): signals.append("correction")
    return signals
```

---

This reference gives you the essential patterns and decisions to assemble robust AI apps, control risk and cost, and build a feedback flywheel that improves both models and UX.