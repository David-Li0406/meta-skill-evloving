---
name: consultant:orchestrator
description: "Main entry point for Consultant Stack. Léo guides you through the entire B2B consulting project lifecycle from discovery to delivery."
invocation: user
---

# Consultant Orchestrator

Launch the Consultant Stack orchestrator (Léo) for B2B project management.

## What This Does

Activates Léo, your intelligent project guide who:
- Understands your intent from natural language
- Routes to the right workflow automatically
- Tracks project progress across phases
- Manages checkpoints and approvals
- Coordinates specialized agents

## Usage

Simply invoke `/consultant:orchestrator` or use intents like:
- "Je veux créer un nouveau projet" → /init
- "Où en est le projet?" → /status
- "On passe au devis" → /quote

## Project Phases

```
0. Analysis (brownfield only)
1. Discovery → Clarify requirements
2. Quotation → Estimate & quote
3. Specs → Technical specification
4. Planning → Create stories
5. Development → Implement
6. Delivery → Document & handoff
```

## Key Commands

| Command | Description |
|---------|-------------|
| `/consultant:init` | Initialize new project |
| `/consultant:status` | View project status |
| `/consultant:next` | Execute next recommended action |

## Agent

This skill uses the `consultant-orchestrator` subagent.
