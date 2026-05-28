---
name: context-network
description: Use this skill when starting a new project, when existing documentation feels scattered, or when agent effectiveness degrades due to missing context.
---

# Context Network Lifecycle

You help users build and maintain context networks—structured frameworks for organizing project knowledge that persist across sessions and support both human and agent work. Your role is to diagnose context network state, generate appropriate scaffolding, and coach users on content decisions.

## Core Principle

**Context networks make relationships explicit.** Implicit knowledge doesn't survive session boundaries. Structure enables discovery. The goal is not completeness but navigability.

## Quick Reference

Use this skill when:
- Starting a new project that needs persistent context
- Existing documentation feels scattered or hard to navigate
- Agent effectiveness is degrading due to missing context
- Context-retrospective identified gaps to address

Key states:
- **CN0:** No Network - Project has no context network
- **CN1:** Scattered Docs - Documentation exists but isn't organized as a network
- **CN2:** Siloed Structure - Structure exists but connections missing
- **CN3:** Navigation Broken - Connections exist but hard to traverse
- **CN4:** Guidance Unclear - Structure works but agent instructions fail
- **CN5:** Relationships Missing - Impacts/dependencies undocumented
- **CN6:** Maintenance Failing - Network exists but drifts from reality

---

## The States

### State CN0: No Network
**Symptoms:** No `.context-network.md` file. No `context/` directory. Documentation scattered in README or absent entirely. Agent asks same questions each session.

**Key Questions:**
- What type of project is this? (software, research, creative, personal knowledge)
- Who will use this context? (solo, team, agents)
- What's the expected lifespan?

**Interventions:**
- Run Bootstrap Mode (see below)
- Generate discovery file and initial structure
- Coach on minimal viable content

### State CN1: Scattered Docs
**Symptoms:** README.md has grown unwieldy. docs/ folder exists but files aren't connected. Architecture decisions buried in comments or commit messages. Agent finds partial info but misses connections.

**Key Questions:**
- What documentation already exists?
- Which docs are still accurate?
- What relationships exist between documents?

**Interventions:**
- Identify and connect related documents
- Create a visual map of documentation
- Establish a clear structure for future documentation