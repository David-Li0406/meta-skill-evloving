---
name: complexity
description: 'Analyze code complexity and find refactor targets using radon/gocyclo'
---

# Complexity Analysis Skill

Analyze code complexity using `radon` (Python) and `gocyclo` (Go) to identify functions that need refactoring.

**Supported Languages:** Python, Go

## Overview

This skill provides comprehensive code complexity analysis:
- Run `radon cc` on target paths
- Interpret complexity grades (A-F)
- Identify refactoring candidates
- Generate actionable recommendations
- Support enforcement checks via `xenon`
