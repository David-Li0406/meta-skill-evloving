---
name: worker-retrospective
description: Retrospective contribution format for Developer, Tech Artist, QA, and Game Designer worker agents
category: orchestration
depends-on: [ralph-core]
---

# Worker Retrospective Contributions

**WHEN PM INITIATES A RETROSPECTIVE, YOU MUST CONTRIBUTE YOUR PERSPECTIVE.**

---

## Detecting Retrospective

**POLL for retrospective.txt**:

- When `agents.{agent}.status == "awaiting_retrospective"` in coordinator-state.json
- Check if `.claude/session/retrospective.txt` exists

---

## What to Do When Retrospective is Triggered

1. **READ** `.claude/session/retrospective.txt`
2. **FIND** your section:
   - Developer: `### Developer Perspective`
   - Tech Artist: `### Tech Artist Perspective`
   - QA: `### QA Perspective`
   - Game Designer: `### Game Designer Perspective`
3. **ADD** your contribution replacing the `<!-- WAITING -->` comment
4. **UPDATE** the completion checkbox in retrospective.txt
5. **UPDATE** your status in coordinator-state.json to "idle"
6. **LOG** in your progress file
7. **CONTINUE** polling for next task

---

## Developer Perspective Format

```markdown
### Developer Perspective

**Implementation Decisions**:

- {{Describe key technical decisions you made}}
- {{Why you chose specific approaches}}

**Technical Challenges Faced**:

- {{What was difficult about this task}}
- {{How you overcame those challenges}}

**What Worked Well**:

- {{Solutions or patterns that worked effectively}}

**Areas for Improvement**:

- {{What could be done better next time}}
- {{Any technical debt or shortcuts taken}}

**Lessons Learned**:

- {{What would help with similar future tasks}}
- {{Suggestions for PRD clarifications}}

_**Contributed by**: Developer Agent | {{ISO_TIMESTAMP}}_
```

---

## QA Perspective Format

```markdown
### QA Perspective

**Validation Results Summary**:

- TypeScript: {{pass/fail}}
- Lint: {{pass/fail}}
- Tests: {{pass/fail}}
- Build: {{pass/fail}}
- Manual/Browser: {{pass/fail}}

**Code Quality Observations**:

- {{Is the code maintainable?}}
- {{Any code smells or anti-patterns?}}
- {{Is there proper error handling?}}
- {{Is the code well-structured?}}

**Quality Concerns**:

- {{Should this be refactored before continuing?}}
- {{Any performance concerns?}}
- {{Is test coverage adequate?}}
- {{Does this follow project patterns?}}

**Suggestions for Improvement**:

- {{What would make this code better?}}
- {{Any areas that need refactoring?}}
- {{Missing tests or coverage?}}

_**Contributed by**: QA Agent | {{ISO_TIMESTAMP}}_
```

---

## Tech Artist Perspective Format

```markdown
### Tech Artist Perspective

**Visual Assets Created**:

- {{Assets/materials/shaders created}}
- {{3D models, textures, effects implemented}}

**Visual Quality Assessment**:

- {{How well visuals match GDD specifications}}
- {{Artistic direction alignment}}
- {{Overall visual polish achieved}}

**Performance Metrics**:

- {{Frame rate impact}}
- {{Draw calls, triangle count}}
- {{Texture memory usage}}
- {{Shader complexity}}

**Challenges Faced**:

- {{What was difficult about visual implementation}}
- {{Shader compilation or optimization issues}}
- {{Asset integration challenges}}

**What Worked Well**:

- {{Visual techniques that were effective}}
- {{Performance optimizations that succeeded}}
- {{Artistic solutions that pleased the Game Designer}}

**Areas for Improvement**:

- {{What could be improved visually}}
- {{Performance bottlenecks to address}}
- {{Asset workflow refinements needed}}

**Lessons Learned**:

- {{What would help with similar visual tasks}}
- {{Shader patterns to reuse}}
- {{Asset pipeline improvements}}

_**Contributed by**: Tech Artist Agent | {{ISO_TIMESTAMP}}_
```

---

## Contribution Guidelines

### Be Specific

- Mention specific files, functions, or patterns you used
- Note any unexpected issues you encountered
- Share what surprised you about the work

### Be Honest

- If you took shortcuts, mention them
- If something felt hacky, say so
- If the PRD was unclear, explain what was confusing

### Be Constructive

- Suggest improvements for future tasks
- Note what would have made this task easier
- Identify areas that might need refactoring later

---

## DO NOT

- ❌ Skip contributing to retrospective
- ❌ Write generic/vague contributions
- ❌ Edit the other agent's sections
- ❌ Delete or modify the retrospective structure

---

## Reference

- [ralph-core.md](ralph-core.md) — Session structure and state management
- [ralph-event-protocol.md](ralph-event-protocol.md) — Event-driven messaging protocol
