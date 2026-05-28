# LaTeX/MathJax Quick Reference

## Inline vs Display Math

**Inline** (within text): `$formula$`
```markdown
The value $x = 5$ is used here.
```

**Display** (centered, standalone): `$$formula$$`
```markdown
$$
x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}
$$
```

## Common Symbols

### Greek Letters
| Symbol | Code | Symbol | Code |
|--------|------|--------|------|
| $\alpha$ | `\alpha` | $\Alpha$ | `\Alpha` |
| $\beta$ | `\beta` | $\Beta$ | `\Beta` |
| $\gamma$ | `\gamma` | $\Gamma$ | `\Gamma` |
| $\delta$ | `\delta` | $\Delta$ | `\Delta` |
| $\theta$ | `\theta` | $\Theta$ | `\Theta` |
| $\pi$ | `\pi` | $\Pi$ | `\Pi` |
| $\sigma$ | `\sigma` | $\Sigma$ | `\Sigma` |
| $\omega$ | `\omega` | $\Omega$ | `\Omega` |

### Operators
| Symbol | Code |
|--------|------|
| $\times$ | `\times` |
| $\div$ | `\div` |
| $\pm$ | `\pm` |
| $\cdot$ | `\cdot` |
| $\leq$ | `\leq` |
| $\geq$ | `\geq` |
| $\neq$ | `\neq` |
| $\approx$ | `\approx` |
| $\infty$ | `\infty` |

### Arrows
| Symbol | Code |
|--------|------|
| $\rightarrow$ | `\rightarrow` |
| $\leftarrow$ | `\leftarrow` |
| $\Rightarrow$ | `\Rightarrow` |
| $\Leftrightarrow$ | `\Leftrightarrow` |

## Common Structures

### Subscripts and Superscripts
```latex
$x_0$           → x₀
$x_{max}$       → x with "max" subscript
$x^2$           → x²
$x^{n+1}$       → x^(n+1)
$x_i^2$         → x subscript i, squared
$P_{\text{handle}}$  → P with text subscript
```

### Fractions
```latex
$\frac{a}{b}$                    → a/b
$\frac{n!}{i!(n-i)!}$           → binomial denominator
$\frac{\partial f}{\partial x}$  → partial derivative
```

### Square Roots
```latex
$\sqrt{x}$       → √x
$\sqrt[3]{x}$    → ³√x
$\sqrt{b^2-4ac}$ → quadratic discriminant
```

### Summations and Products
```latex
$\sum_{i=0}^{n}$           → Σ from i=0 to n
$\sum_{i=0}^{n} x_i$       → sum of x_i
$\prod_{i=1}^{n}$          → Π from i=1 to n
```

### Integrals
```latex
$\int_a^b f(x) dx$         → definite integral
$\int f(x) dx$             → indefinite integral
$\oint$                    → contour integral
```

### Binomial Coefficients
```latex
$\binom{n}{i}$             → "n choose i"
$\binom{n}{k} = \frac{n!}{k!(n-k)!}$
```

### Matrices
```latex
$$
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
$$
```

### Cases (Piecewise Functions)
```latex
$$
f(x) = \begin{cases}
x^2 & \text{if } x \geq 0 \\
-x & \text{if } x < 0
\end{cases}
$$
```

## Common Formulas

### Bezier Curves
```latex
$B(t) = (1-t)^2 P_0 + 2(1-t)t P_1 + t^2 P_2$

$B(t) = \sum_{i=0}^{n} \binom{n}{i} (1-t)^{n-i} t^i P_i$
```

### Linear Interpolation
```latex
$\text{lerp}(A, B, t) = (1-t) \cdot A + t \cdot B$
```

### Derivatives
```latex
$B'(t) = 2(1-t)(P_1 - P_0) + 2t(P_2 - P_1)$

$\frac{df}{dx}$   → derivative notation
```

### Trigonometry
```latex
$\sin\theta$, $\cos\theta$, $\tan\theta$
$(\cos\theta, \sin\theta)$  → point on unit circle
```

## Text in Math

```latex
$P_{\text{handle}}$       → subscript with text
$x \text{ where } x > 0$  → text within formula
$\quad$                   → space
$\qquad$                  → larger space
```

## Continuity Notation

```latex
$C^0$    → C-zero continuous
$C^1$    → C-one continuous
$C^\infty$  → infinitely differentiable
```

## Common Patterns for Documentation

### Formula with conditions
```latex
$$
B(t) = (1-t)^2 P_0 + 2(1-t)t P_1 + t^2 P_2 \quad \text{where } t \in [0, 1]
$$
```

### Multiple aligned equations
```latex
$$
\begin{align}
c_0 &= P_0 \\
c_1 &= 2(P_1 - P_0) \\
c_2 &= P_0 - 2P_1 + P_2
\end{align}
$$
```

### Numbered equation list
```latex
- $B'(0) = 2(P_1 - P_0)$ → tangent at start
- $B'(1) = 2(P_2 - P_1)$ → tangent at end
```
