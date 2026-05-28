---
name: oe-real-e2e-verification
description: Full E2E verification with REAL APIs (OpenAI + Gemini). Use when stub tests pass but you need to verify real LLM behavior. Requires hybrid mode (I:ope/E:gem/V:ope). NEVER uses AGENT_MODE=stub.
---

# oe-real-e2e-verification

> **PURPOSE:** Stub tests prove code paths work. This skill proves REAL LLM responses work.
> Deterministic stub tests are useful for fast CI, but they CANNOT catch:
> - LLM misclassifying intent (e.g., question vs change request)
> - Detection signal merging bugs
> - Feature interference under real LLM uncertainty

## When to Use

- After fixing detection/routing bugs (BUG-036 through BUG-044 pattern)
- Before claiming "E2E verified" for hybrid/detour/Q&A features
- When stub tests pass but Playwright shows different behavior

## Prerequisites

1. **API Keys in Keychain:**
   ```bash
   security find-generic-password -s 'openevent-api-test-key' -w  # OpenAI
   security find-generic-password -s 'openevent-gemini-key' -w    # Gemini
   ```

2. **Backend with Hybrid Providers:**
   ```bash
   USER=$(whoami) INTENT_PROVIDER=openai ENTITY_PROVIDER=gemini VERBALIZER_PROVIDER=openai \
     ./scripts/dev/dev_server.sh start
   ```

3. **Frontend:**
   ```bash
   cd atelier-ai-frontend && npm run dev
   ```

## The Mandatory Test Sequence

Test ALL 6 core features in ONE session without restart:

### Phase 1: Initial Booking (Shortcuts + Gates)
```
Client: "Hi, I would like to book Room B for 50 guests on April 15, 2026."
Expected: Offer generated (Step 4), deposit panel shown
```

### Phase 2: Hybrid Acceptance + Q&A
```
Client: "Room B looks perfect. Do you offer catering services?"
Expected:
  - Acceptance detected → advances to billing
  - Q&A answered → catering info appended
  - Deposit "Pay" button enabled
```

### Phase 3: Detour During Billing
```
Client: "Actually, can we change the date to May 20, 2026?"
Expected:
  - Detour triggered (Step 1 → 2 → 3 → 4)
  - NEW offer generated with updated date
  - Deposit due date updated
```

### Phase 4: Confirm Second Offer
```
Client: "Yes, we accept the updated offer."
Expected: Billing prompt or deposit gate activated
```

### Phase 5: Complete Flow to Site Visit
```
Pay Deposit → Should reach Step 7 site visit prompt
```

## Failure Modes to Watch

| Symptom | Likely Bug | Check |
|---------|------------|-------|
| Hybrid Q&A not answered | BUG-040 | `matches_acceptance_pattern()` |
| Detour blocked during billing | BUG-042 | `_merge_signal_flags()` in unified.py |
| "Pure Q&A" instead of new offer | BUG-041 | Step 4 QNA_GUARD ignoring `caller_step` |
| Second offer not generated | BUG-043 | Step 3 Q&A short-circuit |

## Evidence Required

Before claiming "E2E verified", capture:

1. **Playwright screenshot** of final site-visit message
2. **Backend logs** showing:
   - `[UNIFIED_DETECTION]` signals for each message
   - `[Step*]` routing decisions
   - No `[FALLBACK]` blocks

Save to: `e2e-scenarios/YYYY-MM-DD_<feature>-verification.md`

## DO NOT

- ❌ Use `AGENT_MODE=stub` - defeats the purpose
- ❌ Skip Phase 3 (detour) - this is where feature interference happens
- ❌ Claim "verified" without reaching site visit
- ❌ Test on a conversation that already has history