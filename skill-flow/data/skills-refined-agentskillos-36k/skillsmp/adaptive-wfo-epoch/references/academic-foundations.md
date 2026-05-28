# Academic Foundations: Adaptive Walk-Forward Epoch Selection

## Literature Review

This methodology synthesizes concepts from four distinct academic traditions:

1. **Walk-Forward Analysis** (Trading Systems Research)
2. **Deflated Sharpe Ratio** (Statistical Finance)
3. **Multi-Objective Hyperparameter Optimization** (Machine Learning)
4. **Warm-Starting Sequential Optimization** (AutoML)

## 1. Walk-Forward Efficiency (WFE)

### Origin

Walk-Forward Efficiency was introduced by **Robert E. Pardo** in his seminal work on trading system validation:

- **Pardo, R. E. (1992).** _Design, Testing, and Optimization of Trading Systems._ John Wiley & Sons.
- **Pardo, R. E. (2008).** _The Evaluation and Optimization of Trading Strategies, 2nd Edition._ John Wiley & Sons.

### Definition

```
WFE = OOS_Performance / IS_Performance
```

Typically expressed as return ratio or Sharpe ratio.

### Interpretation Guidelines (Pardo)

| WFE Value | Interpretation                         |
| --------- | -------------------------------------- |
| > 0.60    | Robust strategy, low overfitting risk  |
| 0.50-0.60 | Acceptable, reasonable generalization  |
| < 0.50    | Likely overfit, requires revision      |
| ~1.00     | Encouraging but warrants investigation |
| Variable  | Signals fragility across regimes       |

### Key Quote

> "Walk-Forward Efficiency measures the degree to which a strategy's in-sample performance translates to out-of-sample results. A strategy that cannot maintain at least 50% of its in-sample performance is likely overfit to historical data."
> — Pardo (2008), Chapter 8

## 2. Deflated Sharpe Ratio (DSR)

### Origin

**Bailey, D. H., & López de Prado, M. (2014).** "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality." _The Journal of Portfolio Management_, 40(5), 94-107.

### Problem Addressed

When testing multiple strategies (or hyperparameter configurations), the "best" Sharpe ratio is expected to be inflated due to multiple testing. DSR corrects for this selection bias.

### Formula

```
DSR = Φ[(SR - SR₀) × √T / √(1 + 0.5×SR² - γ₃×SR + (γ₄-3)/4×SR²)]
```

Where:

- SR = Observed Sharpe ratio
- SR₀ = Expected maximum Sharpe under null (depends on number of trials)
- T = Number of observations
- γ₃ = Skewness
- γ₄ = Kurtosis
- Φ = Standard normal CDF

### Expected Maximum Under Null

For N independent trials:

```
SR₀ ≈ √(2 × ln(N)) - (γ + ln(π/2)) / √(2 × ln(N))
```

Where γ ≈ 0.5772 (Euler-Mascheroni constant).

### Application to Epoch Selection

When selecting from K epochs across F folds, total trials = K × F.

For 4 epochs × 31 folds = 124 trials:

- SR₀ ≈ 2.5 × σ(SR)
- With σ(SR) ≈ 0.3: SR₀ ≈ 0.75

**A Sharpe of 1.0 deflates to ~0.25 after DSR adjustment.**

## 3. Multi-Objective Hyperparameter Optimization (MOHPO)

### Key References

- **Bischl, B., Binder, M., Lang, M., et al. (2023).** "Multi-Objective Hyperparameter Optimization in Machine Learning—An Overview." _ACM Transactions on Evolutionary Learning and Optimization._
- **Deb, K., Pratap, A., Agarwal, S., & Meyarivan, T. (2002).** "A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II." _IEEE Transactions on Evolutionary Computation_, 6(2), 182-197.

### Pareto Optimality

A solution is **Pareto-optimal** if no other solution improves one objective without worsening another.

For epoch selection with objectives:

1. **Maximize WFE** (generalization quality)
2. **Minimize training time** (computational cost)

An epoch is on the efficient frontier if no other epoch dominates it.

### Algorithms

- **NSGA-II**: Non-dominated Sorting Genetic Algorithm (Deb et al., 2002)
- **SPEA-II**: Strength Pareto Evolutionary Algorithm
- **SMS-EMOA**: S-Metric Selection Evolutionary Multi-Objective Algorithm

For discrete epoch selection (4 candidates), exhaustive evaluation is tractable; these algorithms are relevant for continuous or large search spaces.

## 4. Warm-Starting Sequential Optimization

### Key References

- **Nomura, M., & Ono, I. (2021).** "Warm Starting CMA-ES for Hyperparameter Optimization." _Proceedings of the AAAI Conference on Artificial Intelligence._
- **Perrone, V., et al. (2017).** "Learning to Transfer Initializations for Bayesian Hyperparameter Optimization." _BayesOpt Workshop at NeurIPS._

### Concept

Transfer knowledge from previous optimization runs to accelerate future searches. In the context of AWFES:

```
epoch_prior(fold_n) = optimal_epoch(fold_{n-1})
```

### Benefits

1. **Reduced search cost**: Prior narrows exploration
2. **Temporal adaptation**: Captures regime-specific patterns
3. **Stability**: Prevents erratic epoch switching

### Risk: Path Dependency

Warm-starting creates serial correlation in epoch selection. Mitigation:

- Use stability penalty for changes
- Periodically reset to prior-free search
- Monitor epoch selection variance across folds

## 5. Related Work in Finance

### Combinatorial Purged Cross-Validation (CPCV)

**López de Prado, M. (2018).** _Advances in Financial Machine Learning._ Wiley. Chapter 7.

CPCV addresses look-ahead bias in time series cross-validation by:

1. Testing all possible train/test combinations
2. Purging overlapping samples (embargo)
3. Providing distribution of performance, not point estimate

AWFES is compatible with CPCV: use CPCV for outer loop model evaluation, AWFES for inner loop epoch selection.

### Evidence-Based Technical Analysis

**Aronson, D. R. (2006).** _Evidence-Based Technical Analysis: Applying the Scientific Method and Statistical Inference to Trading Signals._ John Wiley & Sons.

Key contributions:

- Data-mining bias corrections for trading strategies
- Hypothesis testing framework for technical analysis
- Evaluated 6,400+ signaling rules with proper statistical controls

## 6. Comparison: AWFES vs Related Methods

| Method                    | Selection Criterion  | Temporal Structure      | Adaptation            |
| ------------------------- | -------------------- | ----------------------- | --------------------- |
| Early Stopping            | Validation loss      | Continuous monitoring   | None                  |
| Nested CV                 | Validation accuracy  | Shuffled splits         | None                  |
| Bayesian Optimization     | Acquisition function | Independent evaluations | Surrogate model       |
| Population-Based Training | Validation metric    | Within-training         | Weight transfer       |
| **AWFES**                 | WFE (IS/OOS ratio)   | Temporal WFO            | Epoch prior carryover |

### Key Distinctions

1. **WFE vs validation loss**: WFE directly measures generalization; validation loss measures prediction accuracy
2. **Temporal ordering**: AWFES respects time series structure; standard CV does not
3. **Discrete candidates**: AWFES evaluates all candidates; Bayesian optimization uses surrogate to reduce evaluations
4. **Carry-forward**: AWFES transfers epoch selection, not model weights

## 7. Empirical Guidelines

### From Pardo (2008)

| Guideline           | Value         | Rationale                              |
| ------------------- | ------------- | -------------------------------------- |
| Minimum WFE         | 0.50          | Below this, strategy likely overfit    |
| IS/OOS ratio        | 80/20 typical | Balance signal detection vs validation |
| Fold count          | 10-30         | Statistical significance               |
| Walk-forward period | 3+ years      | Capture multiple market cycles         |

### From López de Prado (2018)

| Guideline            | Value          | Rationale                                  |
| -------------------- | -------------- | ------------------------------------------ |
| Minimum track record | MinTRL formula | Required days for statistical significance |
| DSR threshold        | 0.95           | 95% confidence true Sharpe > 0             |
| Embargo period       | 6% of data     | Prevent look-ahead bias                    |
| CPCV paths           | 20-30          | Balance compute vs coverage                |

## Full Bibliography

```bibtex
@article{bailey2014deflated,
  title={The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality},
  author={Bailey, David H and L{\'o}pez de Prado, Marcos},
  journal={The Journal of Portfolio Management},
  volume={40},
  number={5},
  pages={94--107},
  year={2014}
}

@book{pardo2008evaluation,
  title={The Evaluation and Optimization of Trading Strategies},
  author={Pardo, Robert E},
  year={2008},
  publisher={John Wiley \& Sons},
  edition={2nd}
}

@book{lopezdeprado2018advances,
  title={Advances in Financial Machine Learning},
  author={L{\'o}pez de Prado, Marcos},
  year={2018},
  publisher={John Wiley \& Sons}
}

@article{bischl2023mohpo,
  title={Multi-Objective Hyperparameter Optimization in Machine Learning—An Overview},
  author={Bischl, Bernd and others},
  journal={ACM Transactions on Evolutionary Learning and Optimization},
  year={2023}
}

@inproceedings{nomura2021warm,
  title={Warm Starting CMA-ES for Hyperparameter Optimization},
  author={Nomura, Masahiro and Ono, Isao},
  booktitle={Proceedings of the AAAI Conference on Artificial Intelligence},
  year={2021}
}

@article{deb2002nsga2,
  title={A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II},
  author={Deb, Kalyanmoy and others},
  journal={IEEE Transactions on Evolutionary Computation},
  volume={6},
  number={2},
  pages={182--197},
  year={2002}
}

@book{aronson2006evidence,
  title={Evidence-Based Technical Analysis},
  author={Aronson, David R},
  year={2006},
  publisher={John Wiley \& Sons}
}
```
