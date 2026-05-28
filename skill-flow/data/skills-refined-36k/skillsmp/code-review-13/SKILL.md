---
name: code-review
description: Review code for implementation correctness, scalability, and production readiness. Use when reviewing PRs, auditing code quality, checking for performance issues, or evaluating production readiness. Triggers on "review", "audit", "check code", "production ready", "scalability".
---

# Production Code Review

A systematic code review skill emphasizing implementation correctness, scalability, and production readiness for high-performance Python/PyTorch codebases.

## Quick Start

When asked to review code:
1. Read the files to be reviewed
2. Apply the review checklist systematically
3. Report findings by severity (Critical > High > Medium > Low)
4. Provide actionable recommendations with code examples

## Review Checklist

### 1. Correctness (Critical Priority)

**Algorithm correctness**:
- [ ] Does the implementation match the documented algorithm/formula?
- [ ] Are edge cases handled (empty inputs, single elements, boundary conditions)?
- [ ] Are mathematical operations numerically stable (log-space, overflow/underflow)?
- [ ] Are tensor shapes consistent throughout the computation?

**Type safety**:
- [ ] Are dtypes explicitly specified where precision matters (float32 vs float64)?
- [ ] Are device placements consistent (CPU/CUDA tensors not mixed)?
- [ ] Are integer divisions handled correctly (// vs /)?

**Memory correctness**:
- [ ] Are tensors properly detached when needed to prevent gradient leaks?
- [ ] Are in-place operations used safely (not on leaf tensors requiring grad)?
- [ ] Are views vs copies handled correctly?

### 2. Scalability (High Priority)

**Memory complexity**:
- [ ] What is the memory complexity? Document as O(?) in comments
- [ ] Are large intermediate tensors avoided or cleared?
- [ ] Is there unnecessary materialization of sparse/structured data?
- [ ] Can computation be chunked/streamed for large inputs?

**Compute complexity**:
- [ ] What is the time complexity? Document as O(?) in comments
- [ ] Are there nested loops that could be vectorized?
- [ ] Are redundant computations cached/memoized?
- [ ] Are expensive operations (matmul, attention) optimized?

**Scaling characteristics**:
- [ ] How does memory scale with batch size? Sequence length? Feature dimension?
- [ ] Are there O(N²) or O(N³) operations that could bottleneck at scale?
- [ ] Is the implementation suitable for the target scale (e.g., T=400K sequences)?

### 3. Production Readiness (High Priority)

**Error handling**:
- [ ] Are inputs validated with informative error messages?
- [ ] Are assertions used for internal invariants (not user-facing validation)?
- [ ] Are exceptions specific and actionable?

**Robustness**:
- [ ] Does code handle NaN/Inf gracefully?
- [ ] Are there fallbacks for numerical instability?
- [ ] Is behavior deterministic (or explicitly documented as non-deterministic)?

**Observability**:
- [ ] Are warnings issued for suspicious inputs (e.g., non-zero-centered data)?
- [ ] Can intermediate values be inspected for debugging?
- [ ] Are performance-critical paths identifiable for profiling?

**API design**:
- [ ] Is the public API minimal and well-documented?
- [ ] Are default values sensible for common use cases?
- [ ] Is the API consistent with similar functions in the codebase?

### 4. Code Quality (Medium Priority)

**Readability**:
- [ ] Do variable names convey meaning (avoid single letters except in math)?
- [ ] Are complex computations broken into named intermediate steps?
- [ ] Are magic numbers extracted into named constants?

**Documentation**:
- [ ] Do docstrings follow PyTorch conventions (see docstring skill)?
- [ ] Are mathematical formulas documented with LaTeX notation?
- [ ] Are tensor shapes documented in Args/Returns?

**Testing implications**:
- [ ] Is the code structured to be testable (pure functions, minimal side effects)?
- [ ] Are there obvious test cases suggested by the implementation?
- [ ] Are edge cases documented for test coverage?

### 5. PyTorch/CUDA Specific (Medium Priority)

**Device handling**:
- [ ] Are new tensors created on the correct device?
- [ ] Is `.to(device)` used correctly without unnecessary transfers?
- [ ] Are CUDA synchronization points minimized?

**Gradient flow**:
- [ ] Will gradients flow correctly through all necessary paths?
- [ ] Are `torch.no_grad()` contexts used appropriately?
- [ ] Are custom autograd Functions implemented correctly?

**Performance patterns**:
- [ ] Are contiguous tensors used before view operations?
- [ ] Is `torch.compile` compatible (no graph breaks)?
- [ ] Are operations fusible by the compiler?

## Severity Definitions

**Critical**: Will cause incorrect results, crashes, or data corruption
- Algorithm bugs, incorrect tensor operations, memory corruption

**High**: Significant impact on performance or reliability at scale
- O(N²) where O(N) is possible, memory leaks, silent failures

**Medium**: Affects maintainability or has minor performance impact
- Missing validation, poor naming, undocumented assumptions

**Low**: Style issues or minor improvements
- Formatting, optional optimizations, documentation gaps

## Review Output Format

Structure your review as follows:

```markdown
## Summary

[1-2 sentence overview of the code's purpose and overall assessment]

## Critical Issues

### [Issue Title]
**Location**: `file.py:123`
**Problem**: [Description of the issue]
**Impact**: [What could go wrong]
**Fix**:
```python
# Before
problematic_code()

# After
correct_code()
```

## High Priority

[Same format as Critical]

## Medium Priority

[Same format, can be briefer]

## Low Priority

[Bullet points acceptable]

## Positive Observations

- [What's done well - important for balanced feedback]

## Recommendations

1. [Prioritized list of improvements]
2. [With rationale]
```

## Common Patterns to Flag

### Memory Issues

```python
# BAD: Materializes O(T×K×C²) tensor
edge = torch.zeros(batch, T, K, C, C)
for t in range(T):
    for k in range(K):
        edge[:, t, k] = compute_edge(t, k)

# GOOD: Compute on-the-fly with O(KC) memory
for t in range(T):
    for k in range(K):
        edge_block = compute_edge(t, k)  # (batch, C, C)
        process_and_discard(edge_block)
```

### Numerical Stability

```python
# BAD: Overflow at large T
cumsum = torch.cumsum(x, dim=1)  # Values grow to O(T)

# GOOD: Zero-center to keep values O(√T)
x_centered = x - x.mean(dim=1, keepdim=True)
cumsum = torch.cumsum(x_centered, dim=1)
```

### Gradient Issues

```python
# BAD: Breaks gradient flow
if condition:
    return tensor.detach()  # Silent gradient death
return tensor

# GOOD: Explicit gradient handling
with torch.no_grad():
    # Operations that shouldn't have gradients
    ...
```

### Device Mismatches

```python
# BAD: Creates tensor on CPU, data on GPU
mask = torch.zeros(batch, T)  # CPU!
result = data * mask  # Error or silent transfer

# GOOD: Match device explicitly
mask = torch.zeros(batch, T, device=data.device)
```

## Instructions for Claude

When reviewing code:

1. **Read thoroughly**: Read all files before commenting. Understand the full context.

2. **Check the math**: Verify algorithms against any documented formulas or papers.

3. **Think at scale**: Consider behavior at 10x, 100x, 1000x the test scale.

4. **Be specific**: Point to exact lines, provide concrete fixes.

5. **Prioritize**: Focus on correctness first, then scalability, then style.

6. **Be constructive**: Explain why something is problematic, not just that it is.

7. **Acknowledge good code**: Note well-implemented patterns and clever solutions.

8. **Consider context**: A research prototype has different standards than production code.

## Example Review Invocations

```
Review the streaming.py implementation for production readiness

Audit the backward pass for numerical stability issues

Check if this code will scale to T=400K sequences

Review this PR for memory leaks and gradient issues
```
