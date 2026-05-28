# Handoff: Intelligent Controller Port & Performance Work

**Date**: January 10, 2026 (updated January 14, 2026)  
**Conversation**: Was getting long/cooked - this captures the state

---

## Original Goal

Implement PII extraction and identity resolution per:
- **Primary Plan**: `/docs/IDENTITY_RESOLUTION_PLAN.md`

Before starting that work, we needed to verify the compute engine was performing optimally since analysis throughput was observed to be very slow.

---

## What We Did

### Phase 1: Ported Intelligent Controller from Eve → Comms

Located the "massively parallel system with intelligent controller" in `/home/projects/eve/` and ported these components:

| Component | Source | Target |
|-----------|--------|--------|
| AdaptiveSemaphore | `eve/internal/engine/adaptive_semaphore.go` | `comms/internal/compute/adaptive_semaphore.go` |
| AdaptiveController | `eve/internal/engine/adaptive_controller.go` | `comms/internal/compute/adaptive_controller.go` |
| AutoRPMController | `eve/internal/engine/auto_rpm_controller.go` | `comms/internal/compute/auto_rpm_controller.go` |
| LeakyBucket | `eve/internal/ratelimit/leaky_bucket.go` | `comms/internal/ratelimit/leaky_bucket.go` |
| EmbeddingsBatcher | `eve/internal/embeddings/batcher.go` | `comms/internal/compute/embeddings_batcher.go` |

### Phase 2: Ported ChatStats Parallelism Settings (January 14, 2026)

Ported the high-throughput settings from ChatStats (Python/Celery) to match performance:

| Setting | Old Value | New Value | Rationale |
|---------|-----------|-----------|-----------|
| `WorkerCount` | 10 | **50** | Match ChatStats `ThreadPoolExecutor(max_workers=50)` |
| `ThinkingLevel` | (none) | **"minimal"** | Reduces per-call latency by minimizing model "thinking" phase |
| `StartRPM` | 500 | **2000** | Faster ramp-up for Tier-3 keys |
| `MaxRPM` | 20000 | **30000** | Higher ceiling for Tier-3 keys |
| `SlowStartUntilRPM` | 16000 | **20000** | Higher threshold before steady-state |

Also added **conversation pre-encoding cache** (`PreloadConversations()`) to eliminate per-job DB reads during bulk processing, matching ChatStats' pre-encoding strategy.

### Modified Files
- `comms/internal/gemini/client.go` - Added rate limiting (`SetAnalysisRPM`, `SetEmbedRPM`), fixed `BatchEmbedContents` model name format
- `comms/internal/compute/engine.go` - Integrated all controllers, batcher, wrapHandler for observation, **50 workers default**, **ThinkingLevel:minimal**, **PreloadConversations cache**
- `comms/internal/compute/auto_rpm_controller.go` - **Higher defaults for Tier-3**
- `comms/cmd/comms/main.go` - Added controller stats output, signal handling

---

## Current Performance State

### Embeddings: ✅ DONE - Hitting 20k RPM limit

```
24,740 embeddings in 101.8 seconds
= 242.92 embeddings/sec
= ~14,575 RPM (each batch API call embeds 100 texts)
```

**Important clarification**: The `batchEmbedContents` API IS **synchronous** - it returns immediately with up to 100 embeddings in one response. This is NOT the async batch API (which would return a job ID to poll). The throughput gain comes from 100 texts → 1 HTTP call.

### Analyses: 🔧 OPTIMIZED - Expected 100-200/sec with new settings

**Previous state**: ~7.85/sec with 10 workers (before ChatStats port)

**New optimizations applied** (January 14, 2026):

1. **50 concurrent workers** (was 10) - Matches ChatStats' parallelism
2. **ThinkingLevel: "minimal"** - Dramatically reduces per-call latency by minimizing model's thinking phase for structured extraction
3. **Higher RPM limits** - StartRPM: 2000, MaxRPM: 30000 for Tier-3 keys
4. **Conversation pre-encoding** - Optional `PreloadConversations()` eliminates per-job DB I/O

**Expected throughput with Tier-3 API key**:
- With `ThinkingLevel: minimal`, per-call latency drops from ~5-8s to ~0.5-1s
- With 50 workers × ~1 call/sec = ~50 calls/sec baseline
- RPM controller ramps to 20k+ within seconds
- **Target: 100-200 analyses/sec** (matching ChatStats with similar settings)

**Key insight**: The 20x improvement comes from:
1. 5x more workers (10 → 50)
2. 5-10x faster per-call latency (`ThinkingLevel: minimal`)
3. No DB I/O blocking (pre-encoding cache)

Analysis calls are still **not batchable** - each `generateContent` call is a separate LLM inference. But with enough concurrent workers and reduced latency, we can saturate the Tier-3 rate limits.

---

## How the Controllers Work

```
┌─────────────────────────────────────────────────────────────┐
│                    ADAPTIVE CONTROL SYSTEM                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  AdaptiveSemaphore                                           │
│  └── Runtime-adjustable concurrency limit (in-flight cap)   │
│                                                              │
│  AdaptiveController                                          │
│  └── Adjusts semaphore based on: latency, 429s, 5xx, errors │
│  └── Slow-start ramp up, backoff on congestion              │
│                                                              │
│  AutoRPMController (x2: analysis + embedding)                │
│  └── Adjusts LeakyBucket RPM based on error signals         │
│  └── Slow-start, backs off on rate limits                   │
│                                                              │
│  LeakyBucket (x2: analysis + embedding)                      │
│  └── Smooth, non-bursty rate limiting                       │
│  └── Prevents spiky traffic that causes 429s                │
│                                                              │
│  EmbeddingsBatcher                                           │
│  └── Collects up to 100 embedding tasks                     │
│  └── Flushes every 500ms or when full                       │
│  └── Uses BatchEmbedContents for 100x throughput            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Files Changed in This Session

### Created
- `comms/internal/compute/adaptive_semaphore.go`
- `comms/internal/compute/adaptive_controller.go`
- `comms/internal/compute/auto_rpm_controller.go`
- `comms/internal/ratelimit/leaky_bucket.go`
- `comms/internal/compute/embeddings_batcher.go`

### Modified
- `comms/internal/gemini/client.go`
- `comms/internal/compute/engine.go`
- `comms/cmd/comms/main.go`

---

## What's Left for Identity Resolution

Per `IDENTITY_RESOLUTION_PLAN.md`, implementation phases are:

### Phase 1: Schema & Infrastructure (US-030 - US-033)
- [ ] Add `person_facts` table
- [ ] Add `unattributed_facts` table  
- [ ] Add `merge_events` table
- [ ] Create fact insertion/query utilities

### Phase 2: PII Extraction Analysis Type (US-034 - US-037)
- [ ] Register `pii_extraction_v1` as analysis_type
- [ ] Implement extraction job runner
- [ ] Build facet → person_facts sync job
- [ ] Handle third-party identity creation

### Phase 3: Resolution Algorithm (US-038 - US-042)
- [ ] Identifier collision detection (O(F) algorithm)
- [ ] Hard identifier merge logic
- [ ] Compound identifier matching
- [ ] Soft identifier scoring
- [ ] Merge execution with conflict detection

### Phase 4: CLI Commands (US-043 - US-047)
- [ ] `comms extract pii`
- [ ] `comms identify resolve`
- [ ] `comms identify merges`
- [ ] `comms person facts/profile`
- [ ] `comms identify status`

### Phase 5: Channel Extraction (US-048 - US-050)
- [ ] Run on iMessage conversations
- [ ] Run on Gmail threads
- [ ] Cross-channel resolution sweep

---

## Key Decisions & Context

1. **Models**: `gemini-3-flash-preview` for analysis, `gemini-embedding-001` for embeddings (project policy)

2. **User's expectation**: "150+ analyses/sec and 300+ embeddings/sec" - embeddings achieved, analyses need different approach

3. **Batch API clarification**: User thought batch endpoints were async - they're not. `batchEmbedContents` is sync, just allows 100 texts per call.

4. **Analysis bottleneck**: The ~5-8s per GenerateContent call is the fundamental limit. Can't batch LLM inferences the same way as embeddings.

---

## Quick Test Commands

```bash
# Check comms db location
ls ~/Library/Application\ Support/Comms/

# Build and run
cd ~/nexus/home/projects/comms
go build -o /tmp/comms ./cmd/comms

# Enqueue and run embeddings (default 50 workers)
/tmp/comms compute enqueue embedding
/tmp/comms compute run 2>/dev/null

# Enqueue and run analyses (default 50 workers, ThinkingLevel:minimal)
/tmp/comms compute enqueue analysis convo-all-v1
/tmp/comms compute run 2>/dev/null

# For maximum throughput, use --preload to pre-encode conversations
/tmp/comms compute run --preload 2>/dev/null

# Check queue status
/tmp/comms compute status
```

**Note**: Default worker count is now 50 (matching ChatStats). For Tier-3 keys, the system will automatically ramp RPM from 2000 → 30000 within seconds.

---

## Related Documents

- `/docs/IDENTITY_RESOLUTION_PLAN.md` - Full implementation plan
- `/docs/SCHEMA_DESIGN_ANALYSIS.md` - Schema overview
- `/docs/EVE_COMMS_MIGRATION_ANALYSIS.md` - Eve → Comms migration notes
- `/prompts/pii-extraction-v1.prompt.md` - PII extraction prompt (to be created)
