# Benchmark Results Comparison

Generated: 2026-01-17 00:42:15


## Performance Comparison

| Benchmark | Javascript | Python |
|-----------|-------------|---------|
| Basic Computation (n=1) | 815.21 ns | 1.51 µs |
| Basic Computation (n=10) | 2.21 µs | 1.58 µs |
| Basic Computation (n=20) | 1.61 µs | 1.80 µs |
| Contradiction Resolution | 18.81 µs | 32.41 µs |
| Evolution (10 steps) | 16.52 µs | 8.33 µs |
| Evolution (100 steps) | 291.24 µs | 178.94 µs |
| Fibonacci Generation (n=12) | 737.00 ns | 1.37 µs |
| Fibonacci Generation (n=50) | 1.25 µs | 3.18 µs |
| State Access | 1.70 µs | 3.34 µs |

## Operations Per Second

| Benchmark | Javascript | Python |
|-----------|-------------|---------|
| Basic Computation (n=1) | 1226673.27 | 661471.03 |
| Basic Computation (n=10) | 452333.54 | 634570.92 |
| Basic Computation (n=20) | 622287.99 | 554178.73 |
| Contradiction Resolution | 53163.72 | 30857.78 |
| Evolution (10 steps) | 60547.57 | 120061.86 |
| Evolution (100 steps) | 3433.63 | 5588.39 |
| Fibonacci Generation (n=12) | 1356848.42 | 732514.33 |
| Fibonacci Generation (n=50) | 801180.62 | 314545.43 |
| State Access | 587922.66 | 299664.26 |