# AI Writer: Determinism and Reproducibility Specification

This document specifies how to achieve reproducible branch proposal generation while maintaining the creative variation needed for engaging gameplay.

## The Determinism Challenge

**The Problem**: LLMs are probabilistic. Given the same prompt and seed, different implementations/versions may produce slightly different outputs due to:
- Floating-point arithmetic differences across hardware
- Sampling strategy variations (different random number generators)
- Tokenization differences in newer model versions
- Different hardware acceleration (CPU vs GPU vs TPU)

**The Requirement**: For audit, learning, and reproducibility, we need to be able to regenerate the same proposal given the same LORE context + seed.

**The Solution**: Implement a **determinism protocol** that handles both exact reproducibility (for verification) and controlled variation (for creative gameplay).

## Determinism Layers

### Layer 1: Input Hashing (Fully Deterministic)

Hash the LORE context to create a stable input identifier:

```python
def compute_proposal_input_hash(
    lore: dict,
    branch_type: str,
    generation_stage: str,  # 'outline' or 'detail'
    director_creativity: float,  # 0.0–1.0
    director_seed: int  # Random seed from Director
) -> str:
    """
    Compute a deterministic hash of all inputs to Writer.
    This hash serves as the canonical "request ID" for reproducibility.
    """
    hashable_data = {
        # LORE: only deterministic fields (exclude timestamps)
        'character_id': lore['player']['character']['name'],
        'scene_id': lore['game_state']['current_scene']['id'],
        'narrative_arc': lore['narrative_context']['story_arc'],
        'player_alignment': lore['player']['alignment'],
        'relationships': sorted([
            (char_id, data['disposition']) 
            for char_id, data in lore['player']['relationships'].items()
        ]),
        'established_lore': sorted(lore['narrative_context']['established_lore']),
        'player_choices_history': [
            (choice['choice_text'], choice['consequence'])
            for choice in lore['narrative_context']['player_choices_history'][-10:]
        ],
        
        # Request parameters
        'branch_type': branch_type,
        'generation_stage': generation_stage,
        'director_creativity': director_creativity,
        'director_seed': director_seed,
        
        # Version tracking
        'writer_version': WRITER_VERSION,  # e.g., "1.0.0"
        'schema_version': SCHEMA_VERSION,  # e.g., "2.0"
    }
    
    json_str = json.dumps(hashable_data, sort_keys=True)
    return hashlib.sha256(json_str.encode()).hexdigest()
```

**Usage**: 
- Compute input hash immediately after LORE capture
- Include hash in all proposal metadata
- Use hash as cache key for proposal storage/retrieval

### Layer 2: LLM Seed Management (Deterministic with Variance Control)

Map the input hash and creativity parameter to an LLM seed:

```python
def compute_llm_seed(
    input_hash: str,
    director_creativity: float,  # 0.0–1.0
    model_version: str
) -> int:
    """
    Derive a deterministic LLM seed from input hash and creativity parameter.
    
    Determinism: Same input_hash + creativity → Same seed
    Variation: Different creativity values → Different seeds (controlled)
    """
    # Combine input hash with creativity value
    seed_material = f"{input_hash}_{director_creativity:.2f}_{model_version}"
    seed_int = int(hashlib.sha256(seed_material.encode()).hexdigest(), 16)
    
    # Clamp to valid seed range (usually 0 to 2^31-1)
    return seed_int % (2**31)
```

**Usage**:
- Compute LLM seed deterministically from input hash + creativity
- Pass seed to LLM API (if supported)
- If LLM doesn't support seed: use seed to control temperature/sampling parameters deterministically

### Layer 3: Temperature/Sampling Mapping (Controlled Variation)

Map creativity parameter to LLM sampling settings:

```python
def map_creativity_to_sampling(
    director_creativity: float,  # 0.0–1.0
    llm_seed: int,
    model_type: str  # 'gpt-4', 'claude-3', 'gemini', etc.
) -> dict:
    """
    Deterministically map creativity parameter to LLM sampling settings.
    
    Creativity 0.0 = Deterministic (low temperature, no randomness)
    Creativity 1.0 = Maximum variation (high temperature, sampling)
    """
    
    if model_type in ['gpt-4', 'gpt-3.5']:
        # OpenAI models: temperature + top_p
        return {
            'temperature': director_creativity * 1.5,  # 0.0–1.5
            'top_p': 0.8 + (director_creativity * 0.2),  # 0.8–1.0
            'seed': llm_seed,  # OpenAI supports seed (API 2024+)
        }
    
    elif model_type in ['claude-3', 'claude-opus']:
        # Anthropic models: temperature only
        return {
            'temperature': director_creativity * 1.2,  # 0.0–1.2
        }
    
    elif model_type == 'gemini':
        # Google models: temperature + top_k + top_p
        return {
            'temperature': director_creativity * 1.5,
            'top_p': 0.85 + (director_creativity * 0.15),
            'top_k': max(1, int(40 * (1.0 - director_creativity * 0.5))),
        }
    
    return {'temperature': director_creativity}
```

**Properties**:
- **Deterministic**: Given same input + creativity + model, always produces same sampling params
- **Controlled variation**: Creativity slider directly controls variance
- **Model-agnostic**: Each model type gets appropriate parameters

### Layer 4: Proposal Versioning (Historical Tracking)

Track proposal versions for reproducibility and learning:

```json
{
  "id": "proposal-uuid",
  "version_info": {
    "input_hash": "sha256hash",
    "llm_seed": 12345678,
    "llm_model": "gpt-4-turbo",
    "llm_version": "2024-01-15",
    "writer_version": "1.2.3",
    "schema_version": "2.0",
    "creativity_parameter": 0.65,
    "generation_timestamp": "2026-01-16T14:30:00Z"
  },
  "reproducibility": {
    "can_regenerate": true,
    "regeneration_procedure": "Call Writer with same input_hash + llm_seed",
    "expected_variance": "0% if LLM supports deterministic mode; <5% if not"
  }
}
```

## Determinism Guarantees by Scenario

### Scenario 1: Exact Reproducibility (For Audit)

**Goal**: Regenerate the exact same proposal for debugging/verification.

**Procedure**:
1. Retrieve stored proposal with `input_hash` and `llm_seed`
2. Call Writer with identical LORE + LLM seed
3. Compare outputs

**Expected Result**: Byte-for-byte identical (if LLM supports deterministic seed)

**Caveats**:
- Requires LLM API with seed support (e.g., OpenAI, Anthropic with future updates)
- May fail if model version was retired or API changed
- Different hardware may introduce 0.1–1% numerical variance

### Scenario 2: Controlled Variation (For Gameplay)

**Goal**: Generate a fresh, creative proposal while tracking variation.

**Procedure**:
1. Keep `director_creativity` low (0.3–0.5) for consistent narrative coherence
2. Vary `director_seed` across different proposals (Director makes this decision)
3. Same LORE → Different seed → Different proposal (but similar quality)

**Expected Result**: Proposals feel fresh and varied, but remain coherent and on-brand

**Control**:
- Director controls creativity slider based on player engagement
- Low creativity (0.2) = very consistent, few surprises
- High creativity (0.8) = highly varied, more experimental

### Scenario 3: Post-Launch Learning (For Analysis)

**Goal**: Re-examine proposals to improve policies and Director heuristics.

**Procedure**:
1. Load proposal with `input_hash`, `llm_seed`, `writer_version`
2. Re-run validation pipeline on stored proposal
3. Extract metrics: success rate, policy violations, player coherence feedback
4. Use metrics to tune Director and validation rules

**Expected Result**: Learn which LORE patterns → successful proposals

## Implementing Determinism

### For Outline Stage (Fast, Lower Stakes)

Outline generation can be less strict about determinism:

```python
def generate_outline(
    lore: dict,
    branch_type: str,
    director_creativity: float
) -> BranchOutline:
    """
    Generate a story outline. Less deterministic than Detail stage.
    Multiple outlines can be generated and Director ranks them.
    """
    input_hash = compute_proposal_input_hash(lore, branch_type, 'outline', director_creativity, seed=0)
    
    # Generate 3–5 outlines in parallel with different seeds
    outline_candidates = []
    for seed_offset in range(5):
        llm_seed = compute_llm_seed(input_hash, director_creativity, MODEL_VERSION)
        llm_seed += seed_offset  # Vary seed for each candidate
        
        outline = call_writer_api(
            prompt=build_outline_prompt(lore, branch_type),
            temperature=director_creativity * 1.5,
            seed=llm_seed,
            max_tokens=500
        )
        
        outline_candidates.append({
            'outline': outline,
            'seed': llm_seed,
            'input_hash': input_hash
        })
    
    # Director ranks candidates and picks best
    chosen = director.rank_outlines(outline_candidates, lore)
    return chosen['outline']
```

### For Detail Stage (Slower, Higher Stakes)

Detail generation should be more deterministic:

```python
def generate_detail(
    lore: dict,
    approved_outline: BranchOutline,
    director_creativity: float,
    director_seed: int  # Director provides specific seed
) -> BranchProposal:
    """
    Generate full branch details from outline. More deterministic.
    Uses Director's chosen seed for reproducibility.
    """
    input_hash = compute_proposal_input_hash(
        lore, 
        approved_outline.branch_type, 
        'detail', 
        director_creativity,
        director_seed
    )
    
    llm_seed = compute_llm_seed(input_hash, director_creativity, MODEL_VERSION)
    
    sampling_params = map_creativity_to_sampling(
        director_creativity,
        llm_seed,
        model_type='gpt-4-turbo'
    )
    
    proposal = call_writer_api(
        prompt=build_detail_prompt(lore, approved_outline),
        **sampling_params,
        max_tokens=2000
    )
    
    # Attach determinism metadata
    proposal['version_info'] = {
        'input_hash': input_hash,
        'llm_seed': llm_seed,
        'director_seed': director_seed,
        'director_creativity': director_creativity,
        'llm_model': 'gpt-4-turbo',
        'llm_version': '2024-01-15',
        'writer_version': WRITER_VERSION,
        'generation_timestamp': datetime.utcnow().isoformat()
    }
    
    return proposal
```

## Variance Analysis and Testing

### Test Case 1: Same Input + Seed → Identical Output

```python
def test_determinism_exact():
    """Verify that identical inputs produce identical outputs."""
    lore = load_test_lore('scenario_1')
    
    # Generate proposal twice
    proposal_1 = generate_detail(lore, outline, creativity=0.5, seed=42)
    proposal_2 = generate_detail(lore, outline, creativity=0.5, seed=42)
    
    # Should be byte-for-byte identical
    assert proposal_1['branch_content'] == proposal_2['branch_content']
    assert proposal_1['metadata']['coherence_confidence'] == proposal_2['metadata']['coherence_confidence']
```

### Test Case 2: Same Input + Different Seeds → Similar but Varied

```python
def test_determinism_variation():
    """Verify that different seeds produce reasonably similar but varied outputs."""
    lore = load_test_lore('scenario_1')
    
    proposals = []
    for seed in [42, 43, 44, 45, 46]:
        proposal = generate_detail(lore, outline, creativity=0.5, seed=seed)
        proposals.append(proposal)
    
    # All should have high coherence confidence
    coherence_scores = [p['metadata']['coherence_confidence'] for p in proposals]
    assert all(score > 0.75 for score in coherence_scores)
    
    # But dialogue should vary
    dialogues = [p['branch_content']['dialogue_options'] for p in proposals]
    assert len(set(str(d) for d in dialogues)) >= 3  # At least 3 unique variations
```

### Test Case 3: Model Version Change → Track Compatibility

```python
def test_model_version_compatibility():
    """Verify that proposal metadata helps track version compatibility."""
    proposal_old = load_proposal('2024-01-15')  # Generated with older model
    proposal_new = generate_detail(lore, outline, creativity=0.5, seed=proposal_old['version_info']['director_seed'])
    
    # Can't guarantee exact match, but can track:
    assert proposal_old['version_info']['llm_model'] != proposal_new['version_info']['llm_model']
    
    # Log variance for learning
    variance = compute_semantic_similarity(proposal_old, proposal_new)
    assert variance < 20  # Less than 20% different (semantic)
```

## Handling Non-Deterministic LLMs

For LLMs that don't support explicit seeding (e.g., older OpenAI models, local models without seed support):

```python
def generate_with_fallback_determinism(
    lore: dict,
    outline: BranchOutline,
    director_creativity: float,
    director_seed: int
) -> BranchProposal:
    """
    Fallback determinism for LLMs without native seed support.
    Uses low temperature + prompt engineering for consistency.
    """
    
    # Can't guarantee exact reproducibility, but can minimize variance
    sampling_params = {
        'temperature': max(0.1, director_creativity * 0.8),  # Lower temperature = more deterministic
        'top_p': 0.95,  # Restrict sampling space
    }
    
    # Generate same proposal 3 times and use consensus
    proposals = []
    for _ in range(3):
        proposal = call_writer_api(
            prompt=build_detail_prompt(lore, outline),
            **sampling_params,
            max_tokens=2000
        )
        proposals.append(proposal)
    
    # Merge proposals via consensus (pick most common dialogue, resolve conflicts)
    consensus_proposal = merge_proposals_consensus(proposals)
    
    # Mark as low-determinism
    consensus_proposal['version_info']['determinism_level'] = 'low'
    consensus_proposal['version_info']['note'] = 'Generated via 3x sampling + consensus (LLM has no seed support)'
    
    return consensus_proposal
```

## Open Questions for Implementation

1. **Determinism Level**: How much variance is acceptable? (Suggested: 0% for Detail stage, <5% for Outline stage)
2. **Version Tracking**: Should old proposals be re-validated when Writer version updates? (Answer: Yes, track compatibility)
3. **Cache Strategy**: How long to cache proposals? Indefinitely, or prune old ones? (Answer: Keep indefinitely for audit; prune >1 year for performance)
4. **Reproducibility Window**: If LLM retires a model, how to handle stored proposals? (Answer: Attempt regeneration with latest model; if quality differs, flag for manual review)
5. **Testing Infrastructure**: What determinism tests should be automated? (Answer: All 3 test cases above, run before each Writer deployment)

---

**Status**: Determinism specification complete. Ready for implementation with LLM integration. Key insight: Determinism is achievable via input hashing + seed management, with graceful degradation for non-deterministic LLMs.
