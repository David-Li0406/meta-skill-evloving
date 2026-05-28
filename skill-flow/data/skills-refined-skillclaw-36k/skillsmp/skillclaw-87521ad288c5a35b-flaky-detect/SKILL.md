---
name: flaky-detect
description: Use this skill to identify flaky tests from CI history and test execution patterns when debugging intermittent test failures, auditing test reliability, or improving CI stability.
---

# Flaky Detect Skill

## Purpose

Identify flaky tests (tests that pass and fail non-deterministically) by analyzing CI history, execution patterns, and test characteristics. Google research shows 4.56% of tests are flaky, costing millions in developer productivity.

## Research Foundation

| Finding | Source | Reference |
|---------|--------|-----------|
| 4.56% flaky rate | Google (2016) | [Flaky Tests at Google](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html) |
| ML Classification | FlaKat (2024) | [arXiv:2403.01003](https://arxiv.org/abs/2403.01003) - 85%+ accuracy |
| LLM Auto-repair | FlakyFix (2023) | [arXiv:2307.00012](https://arxiv.org/html/2307.00012v4) |
| Flaky Taxonomy | Luo et al. (2014) | "An Empirical Analysis of Flaky Tests" |

## When This Skill Applies

- User reports "tests sometimes fail" or "intermittent failures"
- CI has been unstable or unreliable
- User wants to audit test suite reliability
- Pre-release quality assessment
- Debugging non-deterministic behavior

## Trigger Phrases

| Natural Language | Action |
|------------------|--------|
| "Find flaky tests" | Analyze CI history for flaky patterns |
| "Why does CI keep failing?" | Identify flaky tests causing failures |
| "Test suite is unreliable" | Full flaky test audit |
| "This test sometimes passes" | Analyze specific test for flakiness |
| "Audit test reliability" | Comprehensive flaky detection |
| "Quarantine flaky tests" | Identify and isolate flaky tests |

## Flaky Test Taxonomy (Google Research)

| Category | Percentage | Root Causes |
|----------|------------|-------------|
| **Async/Timing** | 45% | Race conditions, insufficient waits, timeouts |
| **Test Order** | 20% | Shared state, execution order dependencies |
| **Environment** | 15% | File system, network, configuration differences |
| **Resource Limits** | 10% | Memory, threads, connection pools |
| **Non-deterministic** | 10% | Random values, timestamps, UUIDs |

## Detection Methods

### 1. CI History Analysis

Parse GitHub Actions / CI logs to find inconsistent results:

```python
def analyze_ci_history(repo, days=30):
    """Analyze CI runs for flaky patterns"""
    runs = get_ci_runs(repo, days)
    test_results = {}

    for run in runs:
        for test in run.tests:
            # Logic to analyze test results
```