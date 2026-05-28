---
name: agentic-jujutsu
description: Use this skill when you need quantum-resistant, self-learning version control for multiple AI agents working simultaneously without conflicts.
---

# Agentic Jujutsu - AI Agent Version Control

> Quantum-ready, self-learning version control designed for multiple AI agents working simultaneously without conflicts.

## When to Use This Skill

Use **agentic-jujutsu** when you need:
- ✅ Multiple AI agents modifying code simultaneously
- ✅ Lock-free version control (23x faster than Git)
- ✅ Self-learning AI that improves from experience
- ✅ Quantum-resistant security for future-proof protection
- ✅ Automatic conflict resolution (87% success rate)
- ✅ Pattern recognition and intelligent suggestions
- ✅ Multi-agent coordination without blocking

## Quick Start

### Installation

```bash
npx agentic-jujutsu
```

### Basic Usage

```javascript
const { JjWrapper } = require('agentic-jujutsu');

const jj = new JjWrapper();

// Basic operations
await jj.status();
await jj.newCommit('Add feature');
await jj.log(10);

// Self-learning trajectory
const id = jj.startTrajectory('Implement authentication');
await jj.branchCreate('feature/auth');
await jj.newCommit('Add auth');
jj.addToTrajectory();
jj.finalizeTrajectory(0.9, 'Clean implementation');

// Get AI suggestions
const suggestion = JSON.parse(jj.getSuggestion('Add logout feature'));
console.log(`Confidence: ${suggestion.confidence}`);
```

## Core Capabilities

### 1. Self-Learning with ReasoningBank

Track operations, learn patterns, and get intelligent suggestions:

```javascript
// Start learning trajectory
const trajectoryId = jj.startTrajectory('Deploy to production');

// Perform operations (automatically tracked)
await jj.execute(['git', 'push', 'origin', 'main']);
await jj.branchCreate('release/v1.0');
await jj.newCommit('Release v1.0');

// Record operations to trajectory
jj.addToTrajectory();

// Finalize with success score (0.0-1.0) and critique
jj.finalizeTrajectory(0.95, 'Deployment successful, no issues');

// Later: Get AI-powered suggestions for similar tasks
const suggestion = JSON.parse(jj.getSuggestion('Deploy to staging'));
console.log('AI Recommendation:', suggestion.reasoning);
console.log('Confidence:', (suggestion.confidence * 100).toFixed(1) + '%');
console.log('Expected Success:', (suggestion.expectedSuccessRate * 100).toFixed(1) + '%');
```