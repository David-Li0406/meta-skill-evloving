# Realistic Data Patterns

## General Rules
- Encode the claim in the ordering and slope, then add mild local variation.
- Avoid perfectly parallel curves or identical wiggles across methods.
- Keep values plausible and away from hard 0/1 unless justified.
- Preserve monotonic direction if the claim depends on it, but allow small bumps.

## Trend Construction
- Start with a base curve (linear, concave, or logistic).
- Add small periodic wiggles and Gaussian noise with method-specific phases.
- Use smaller wiggle and noise for the strongest method to look stable.

## Example Snippet (Matplotlib/NumPy)
```python
rng = np.random.default_rng(7)
x = np.linspace(0, 1, n)
base = start + (end - start) * (x**curve)
wiggle = 0.015 * np.sin(2 * np.pi * x + phase)
jitter = rng.normal(0.0, 0.006, n)
trend = np.clip(base + wiggle + jitter, 0.2, 0.7)
```

## Bar Chart Patterns
- Use small method-specific offsets to avoid ties.
- Keep the relative ordering consistent with the narrative.
- If highlighting a method, increase its value slightly but avoid large gaps.
