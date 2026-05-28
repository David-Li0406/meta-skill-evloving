# Codec / Protocol Pipeline Postmortem Template

Use this template when reviewing implementations involving protocol codecs, framing strategies, message serialization, or network protocol handlers.

## Architecture-Specific Dimensions

### Codec Trait Design

The codec abstraction must support arbitrary frame-based protocols without imposing protocol-specific assumptions.

**Examine:**
- Does the `Encode`/`Decode` trait surface match design goals?
- Can codecs be derived, or is manual implementation required?
- Are trait bounds minimal, or do they impose unnecessary constraints?
- How does error representation work?

**Specific questions:**
- Can a codec handle partial reads without losing state?
- Does the design accommodate context-aware deserialization?
- Are there implicit assumptions about endianness, alignment, or integer encoding?
- How does the codec interact with buffer types (contiguous vs non-contiguous)?

**Smell test:** Implement a codec for a protocol with:
1. Variable-length fields
2. Conditional fields (present based on flags)
3. Nested structures with their own length prefixes

How much ceremony was required? Where did the abstraction fight you?

### Framing Strategy Composability

**Per-strategy assessment:**

| Strategy | Status | Composable | Opt-out Overhead | Notes |
|----------|--------|------------|------------------|-------|
| Length-prefixed | | | | |
| Delimiter-based | | | | |
| COBS | | | | |
| Fixed-size | | | | |
| Custom | | | | |

**Integration questions:**
- Are framing strategies truly composable/stackable?
- Can you layer compression → framing → encryption without special-casing?
- Where in the stack does fragmentation sit?
- Can a protocol opt out of features with zero overhead?
- How do codecs signal "need more bytes" vs "frame complete" vs "malformed"?

### Connection/Actor Integration

**State management:**
- How are codec instances managed—per-connection, shared, cloned?
- Can a codec maintain per-connection state (sequence counters, compression dictionaries)?
- Does the codec expose appropriate I/O traits?

**Write path:**
- Single response → codec → socket: friction points?
- Batched responses → codec → socket: batching opportunities exploited?
- Streaming response → codec → socket: back-pressure correctly propagated?

**Read path:**
- Socket → codec → router: how are partial frames buffered?
- What happens when the codec returns an error mid-stream?
- Does the codec interact correctly with protocol hooks?

### Fragment Strategy Implementation

If the protocol supports message fragmentation:

**Examine:**
- Does the trait surface match canonical primitives (message ID, fragment index, is-last)?
- Can strategies be tested in isolation from the full codec stack?
- Are the primitives sufficient for all protocol patterns encountered?

**Edge cases:**
- Out-of-order fragments: handled or rejected?
- Duplicate fragments: handled or rejected?
- Fragment index overflow: handled gracefully?
- Zero-length fragments: legitimate or error?
- Single-fragment "fragmented" messages: degenerate case handled?

**Resource management:**
- Is max message size enforced before or after reassembly completes?
- Are stale partial assemblies purged? (timeout, memory pressure)
- Per-connection memory budgets enforced?

### Serialization Library Integration

**Examine:**
- Which library was chosen? Why?
- Were derivable traits available, or did the project provide wrappers?
- How does the serialization library affect trait bounds and error types?

**Abstraction questions:**
- Is the serialization library abstracted or does it leak into the public API?
- Can users bring their own serialization without forking?
- How are schema evolution / versioning concerns addressed?

### Error Handling & Recovery

**Error taxonomy:**
- Codec errors vs protocol errors vs I/O errors: correctly distinguished?
- Does the error type accommodate codec-specific variants?
- Can the connection survive a codec error, or does any error terminate?

**Recovery semantics:**
- Malformed frame: discard and continue, or terminate?
- Incomplete frame at connection close: how surfaced?
- Reassembly timeout: observable by handlers?

**Observability:**
- Are codec errors logged with sufficient context?
- Can codec errors be distinguished from protocol errors in metrics?

### Performance Characteristics

**Examine:**
- Allocation patterns: per-frame or amortized?
- Zero-copy potential: can frames be decoded directly from receive buffer?
- Overhead for non-fragmented messages: acceptable?

**Benchmarks to validate:**
- Small frame encode/decode latency
- Large frame throughput (saturate codec, not I/O)
- Fragmentation overhead vs non-fragmented path
- Memory usage under concurrent reassembly

## Codec-Specific Smells

| Smell | Symptom | Likely Cause |
|-------|---------|--------------|
| Leaky abstraction | Protocol details in generic codec code | Missing strategy abstraction |
| Buffer bloat | Excessive copying between buffers | Missing zero-copy path |
| State confusion | Codec behaves differently on same input | Per-connection state not isolated |
| Error amnesia | Errors lose context crossing codec boundary | Error type too generic |
| Framing friction | Adding new framing requires touching codec core | Framing not properly abstracted |

## Design Document Conformance

If design documents exist, assess conformance:

| Document | Conformance | Deviations | Spec Gaps Discovered |
|----------|-------------|------------|----------------------|
| | | | |

For each deviation:
- Intentional (update spec) or accidental (fix code)?
- If spec gap: what question did the spec fail to answer?

## Testing Strategy Assessment

| Layer | Test Type | Coverage | Notes |
|-------|-----------|----------|-------|
| Codec unit | Encode/decode round-trip | | |
| Framing | Partial read simulation | | |
| Fragmentation | Interleaved reassembly | | |
| Integration | Full pipeline | | |
| Fuzz | Malformed input | | |

**Questions:**
- Are codecs unit-testable without standing up a full connection?
- Property-based testing for round-trip correctness?
- Have malformed inputs been fuzzed?
- Interleaved fragment reassembly tested?
- DoS scenarios (oversized messages, abandoned assemblies) tested?
