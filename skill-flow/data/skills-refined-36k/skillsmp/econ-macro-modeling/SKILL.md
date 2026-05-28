---
name: econ-macro-modeling
description: Macroeconomic modeling, calibration, and comparative statics. Use when working with DSGE models, growth models, general equilibrium, CES production, welfare analysis, or policy counterfactuals.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
  - Edit
---

# Macroeconomic Modeling

## Model Selection Guide

| Model Type | Use When | Key Features |
|------------|----------|--------------|
| Two-period | Policy comparison, welfare | Simple, closed-form solutions |
| OLG | Demographics, pensions, debt | Generational heterogeneity |
| Infinite horizon | Long-run growth, BGP | Transversality conditions |
| DSGE | Business cycles, monetary policy | Stochastic shocks, estimation |

## Production Functions

### CES (Constant Elasticity of Substitution)
$$Y = A \left[ \beta K^\rho + (1-\beta) L^\rho \right]^{1/\rho}$$

- Elasticity of substitution: $\sigma = \frac{1}{1-\rho}$
- $\rho \to 0$: Cobb-Douglas ($Y = A K^\beta L^{1-\beta}$)
- $\rho \to -\infty$: Leontief (fixed proportions)
- $\rho = 1$: Perfect substitutes

### Factor Shares (CES)
$$s_L = (1-\beta) \left( \frac{AL}{Y} \right)^{1-\rho}$$
$$s_K = 1 - s_L$$

## Equilibrium Concepts

1. **Competitive equilibrium**: Price-taking, markets clear
2. **Walrasian**: Auctioneer, no money
3. **Monetary equilibrium**: Cash-in-advance or MIU
4. **Nash equilibrium**: Strategic interaction (games)

## Calibration Checklist

1. **Targets**: Identify moments to match (labor share, K/Y ratio, growth rate)
2. **Parameters**: List all parameters, note which are calibrated vs estimated
3. **Data sources**: National accounts, labor surveys, I-O tables
4. **Identification**: Ensure parameters are identified from chosen moments
5. **Robustness**: Test sensitivity to alternative calibrations

### Common Calibration Targets
| Parameter | Typical Target | Data Source |
|-----------|----------------|-------------|
| $\beta$ (discount) | 0.96-0.99 annual | Risk-free rate |
| $\alpha$ (capital share) | 0.33-0.40 | National accounts |
| $\delta$ (depreciation) | 0.05-0.10 | Investment data |
| $\sigma$ (IES) | 0.5-2.0 | Consumption Euler |

## Welfare Analysis

### Compensating Variation (CV)
Income needed to achieve reference utility at new prices:
$$V(p_1, y + CV) = V(p_0, y)$$

### Equivalent Variation (EV)
Income change equivalent to policy at original prices:
$$V(p_0, y - EV) = V(p_1, y)$$

### Consumption-Equivalent Welfare
$$\lambda: \quad U((1+\lambda)c_0) = U(c_1)$$

## Standard Notation

| Symbol | Meaning |
|--------|---------|
| $Y, C, I, G$ | Output, consumption, investment, govt spending |
| $K, L, H$ | Capital, labor, human capital |
| $w, r, R$ | Wage, rental rate, gross interest rate |
| $s_L, s_K$ | Labor share, capital share |
| $\beta, \delta$ | Discount factor, depreciation |
| $\rho, \sigma$ | CES parameter, elasticity of substitution |
| $A, z$ | TFP, productivity shock |

## Common Mistakes to Avoid

1. **Not checking Inada conditions**: Ensure interior solutions exist
2. **Ignoring transitional dynamics**: BGP may not be reached
3. **Over-parameterization**: More parameters than identifying moments
4. **Units mismatch**: Annual vs quarterly rates, levels vs logs
5. **Forgetting budget constraints**: Walras' law check
