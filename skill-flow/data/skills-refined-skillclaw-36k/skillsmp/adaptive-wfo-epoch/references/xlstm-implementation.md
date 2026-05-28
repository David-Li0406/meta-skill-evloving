# xLSTM Implementation Patterns for Financial Time Series

Machine-readable reference for implementing sLSTM and mLSTM (NeurIPS 2024) for financial time series forecasting, especially with short sequences (15-50 steps).

**Source**: xLSTM Architecture Comparison experiment (2026-01-20)
**Validated**: BiLSTM vs sLSTM vs mLSTM on BTCUSDT range bar data

---

## Critical Lesson: Normalizer State Causes Prediction Collapse

### The Problem

The original xLSTM paper uses a **normalizer state** to stabilize cell updates:

```python
# PAPER FORMULA (designed for NLP sequences 1000+ steps)
n_t = f_t * n_{t-1} + i_t       # Normalizer accumulates
c_t = (f_t * c + i_t * z) / n_t  # Division by normalizer
```

**Why this fails on short financial sequences (15 steps)**:

| Step | n_t grows | c_t shrinks | Prediction    |
| ---- | --------- | ----------- | ------------- |
| t=1  | ~2        | c/2         | Normal        |
| t=5  | ~32       | c/32        | Small         |
| t=15 | ~100+     | c/100       | **Collapsed** |

The normalizer grows monotonically (sum of exponentials), while cell state gets progressively divided, causing predictions to converge to a constant.

### Symptoms

- `pred_std_ratio < 0.01` (predictions have <1% of target variance)
- `unique_values < 10` (predictions are near-constant)
- Sharpe is negative or near zero (random noise performance)
- Training loss decreases normally (model "learns" but predicts nothing)

### The Fix: Log-Space Max-Stabilizer

Replace division with max-subtraction in log-space:

```python
# FIXED FORMULA (works on short sequences)
m_t = max(log_f + m_{t-1}, log_i)   # Max-stabilizer (bounded)
i' = exp(log_i - m_t)                # Always in [0, 1]
f' = exp(log_f + m_{t-1} - m_t)      # Always in [0, 1]
c_t = f' * c_{t-1} + i' * z_t        # No division!
```

**Why this works**:

| Property      | Normalizer (broken) | Max-stabilizer (fixed) |
| ------------- | ------------------- | ---------------------- |
| Growth        | Unbounded (sum)     | Bounded (max)          |
| Gate range    | [0, ∞)              | [0, 1]                 |
| Cell state    | Collapses to 0      | Maintains variance     |
| Gradient flow | Vanishes            | Healthy                |

### Implementation

```python
class sLSTMCell(nn.Module):
    """sLSTM cell with log-space max-stabilizer (NOT normalizer)."""

    LOG_GATE_MIN = -10.0  # exp(-10) ≈ 4.5e-5
    LOG_GATE_MAX = 10.0   # exp(10) ≈ 22026

    def forward(self, x, h, c, m=None):
        # m = max-stabilizer state (NOT normalizer!)
        if m is None:
            m = torch.zeros_like(c)

        combined = torch.cat([x, h], dim=-1)

        # Log-space gates (before exp)
        log_i = torch.clamp(self.W_i(combined), self.LOG_GATE_MIN, self.LOG_GATE_MAX)
        log_f = torch.clamp(self.W_f(combined), self.LOG_GATE_MIN, self.LOG_GATE_MAX)

        # Max-stabilizer: prevents both explosion and collapse
        m_new = torch.maximum(log_f + m, log_i)

        # Stabilized gates (always in [0, 1])
        i_prime = torch.exp(log_i - m_new)
        f_prime = torch.exp(log_f + m - m_new)

        # Cell state (NO DIVISION!)
        z = torch.tanh(self.W_c(combined))
        c_new = f_prime * c + i_prime * z

        # Output
        o = torch.sigmoid(self.W_o(combined))
        h_new = o * c_new

        return h_new, c_new, m_new
```

---

## sLSTM vs mLSTM: Architecture Selection

### When to Use sLSTM

- **Sequence length**: 15-100 steps
- **Task**: Univariate or low-dimensional forecasting
- **Memory**: Limited GPU memory
- **Speed**: Need fast inference

### When to Use mLSTM

- **Sequence length**: 50-500 steps
- **Task**: Multi-variate, correlation capture
- **Capacity**: Complex feature interactions
- **Trade-off**: 2-3x slower than sLSTM

### Comparison (from POC)

| Metric             | BiLSTM | sLSTM     | mLSTM |
| ------------------ | ------ | --------- | ----- |
| Parameters         | ~50K   | ~56K      | ~37K  |
| pred_std_ratio     | 1.9%   | **392%**  | 40.6% |
| unique_values      | 131    | **843**   | 516   |
| Sharpe (50 epochs) | -0.39  | **+0.47** | +0.05 |

**Note**: sLSTM after fix shows highest prediction diversity and best Sharpe in this run.

---

## mLSTM: Matrix Memory Considerations

### Sigmoid vs Exponential Gates

The original mLSTM paper uses exponential gates, but for financial data:

```python
# RECOMMENDED: Sigmoid gates for bounded stability
i = torch.sigmoid(self.W_i(combined))  # [0, 1]
f = torch.sigmoid(self.W_f(combined))  # [0, 1]
```

Rationale:

- Sigmoid is bounded by design
- No need for normalizer/max-stabilizer
- More stable on noisy financial data

### Matrix Memory Initialization

```python
# Initialize C (matrix memory) to zeros, not random
C = torch.zeros(batch_size, matrix_size, hidden_size)

# Initialize n (normalizer for read) to zeros
n = torch.zeros(batch_size, matrix_size)
```

---

## Hyperparameter Recommendations

### For 15-Step Financial Sequences

| Parameter     | sLSTM | mLSTM | BiLSTM (baseline) |
| ------------- | ----- | ----- | ----------------- |
| hidden_size   | 64    | 64    | 48                |
| num_layers    | 2     | 2     | 2                 |
| dropout       | 0.2   | 0.2   | 0.3               |
| matrix_size   | N/A   | 16    | N/A               |
| bidirectional | No    | No    | Yes (confound!)   |

### Learning Rate

All architectures: `lr = 0.0005` (AdamW)

If training is unstable:

- sLSTM: Try `lr = 0.0002` (exponential gates are sensitive)
- mLSTM: Try gradient clipping `max_norm = 1.0`

---

## POC Validation Checklist

Before trusting any LSTM variant on financial data:

1. **Prediction variance**: `pred_std / y_std > 0.5%`
2. **Unique values**: `> 25` distinct predictions
3. **Gradient flow**: No NaN/Inf, max norm < 1000
4. **Loss reduction**: At least 10% over 50 epochs
5. **Hit rate**: > 45% (not random)

### Fail-Fast Checks

```python
# Check 1: Not collapsed
assert pred_std / y_std > 0.004, "Predictions collapsed"

# Check 2: Diverse outputs
assert len(set(np.round(preds, 6))) > 25, "Predictions not diverse"

# Check 3: Learning happened
assert final_loss < initial_loss * 0.90, "No learning"
```

---

## Anti-Patterns

### 1. Using Normalizer State on Short Sequences

```python
# WRONG
c_new = (f * c + i * z) / (n_new + eps)  # Collapses predictions

# CORRECT
c_new = f_prime * c + i_prime * z  # Max-stabilizer, no division
```

### 2. Forgetting Causality Confound

```python
# BiLSTM sees future (bidirectional)
# sLSTM/mLSTM are causal (forward-only)
# This is an UNFAIR comparison - document it!
```

### 3. Absolute Prediction Thresholds

```python
# WRONG: Absolute threshold
assert pred_std > 1e-4  # Meaningless for tiny return scales

# CORRECT: Relative threshold
assert pred_std / y_std > 0.005  # Relative to target variance
```

### 4. Trusting 50-Epoch POC Sharpe

50 epochs is insufficient for reliable Sharpe estimates:

- Use for sanity checks (not collapsed, not exploded)
- Don't draw conclusions about model superiority
- Full experiment needs 800+ epochs per fold

---

## References

- [xLSTM Paper (NeurIPS 2024)](https://arxiv.org/abs/2405.04517) - Original architecture
- [xLSTMTime](https://arxiv.org/pdf/2407.10240) - Time series adaptation
- [PyxLSTM](https://pyxlstm.readthedocs.io/) - Reference implementation
- [Alpha Forge xlstm_models.py](examples/research/xlstm_models.py) - Working implementation

---

## Changelog

| Date       | Change                                    | Impact                   |
| ---------- | ----------------------------------------- | ------------------------ |
| 2026-01-20 | Initial: Normalizer state caused collapse | sLSTM sharpe: -0.302     |
| 2026-01-20 | Fix: Log-space max-stabilizer             | sLSTM sharpe: **+0.465** |
