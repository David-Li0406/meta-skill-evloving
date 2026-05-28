#!/bin/bash
# Example benchmark run with custom settings
# Defaults based on README.md example

export BACKTEST_BENCH_NSYMBOLS=${BACKTEST_BENCH_NSYMBOLS:-8}
export BACKTEST_BENCH_TICKS_PER_SYMBOL=${BACKTEST_BENCH_TICKS_PER_SYMBOL:-500000}
export BACKTEST_BENCH_MAX_BATCH_NS=${BACKTEST_BENCH_MAX_BATCH_NS:-5000000}

# Print configuration
echo "========================================================"
echo "Running Rust benchmarks with custom configuration:"
echo "  BACKTEST_BENCH_NSYMBOLS         = $BACKTEST_BENCH_NSYMBOLS"
echo "  BACKTEST_BENCH_TICKS_PER_SYMBOL = $BACKTEST_BENCH_TICKS_PER_SYMBOL"
echo "  BACKTEST_BENCH_MAX_BATCH_NS     = $BACKTEST_BENCH_MAX_BATCH_NS"
echo "========================================================"

# Run the benchmark
# Only running bench_core as it is the main performance/scalability benchmark
cargo bench -p backtester-core --bench bench_core
