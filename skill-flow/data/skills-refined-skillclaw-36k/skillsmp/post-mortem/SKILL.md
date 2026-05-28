---
name: post-mortem
description: 'Comprehensive post-implementation validation. Combines retro (learnings), vibe (code validation), security scanning (Talos), and knowledge extraction into a single unified workflow. Triggers: "post-mortem", "validate completion", "final check", "wrap up epic", "close out", "what did we learn".'
---

# Post-Mortem Skill

**The RPI capstone: validate + learn + extract + feed back into the flywheel.**

## Role in the Brownian Ratchet

Post-mortem is the **knowledge ratchet** - the final stage that locks learnings:

| Component | Post-Mortem's Role |
|-----------|-------------------|
| **Chaos** | Implementation produced outcomes (good and bad) |
| **Filter** | Retro extracts what matters, discards noise |
| **Ratchet** | Learnings locked in `.agents/`, MCP, specs |

> **Learnings never go backward. Once ratcheted, knowledge compounds.**

Post-mortem closes the knowledge loop:
```
Implementation → POST-MORTEM → Ratcheted Knowledge → Next Research
                    │
                    ├── .agents/retros/     (locked)
                    ├── .agents/learnings/  (locked)
                    ├── .agents/patterns/   (locked)
                    └── MCP memories        (locked)
```

**The Flywheel Effect:** Each ratcheted learning makes the next cycle faster.
This is why `/post-mortem` is mandatory - skipping it breaks the compounding.

## Philosophy

> "Implementation isn't done until we've validated it, learned from it, and fed that knowledge back into the system."

Post-mortem is the comprehensive POST phase of RPI that closes the knowledge loop. It combines everything that feeds back into the flywheel:

| Component | Purpose | Flywheel Feed |
|-----------|---------|---------------|
| **Retro** | What went wrong/right? | `.agents/retros/`, `.agents/learnings/` |
| **Vibe** | Code quality validation | Issues for findings, quality metrics |
| **Security** | Vulnerability scanning (Talos) | Security posture, CVE tracking |
| **Extract** | Knowledge persistence | MCP memories, `.agents/patterns/` |
| **Spec Update** | Lessons back to source | Enhanced specs for next iteration |

**All roads lead back to Research.** Every output feeds the next cycle.

## Quick Start

```bash
/post-mortem <epic-id>           # Full post-mortem on completed epic
/post-mortem                      # Auto-discover recently completed epic
/post-mortem --skip-security      # Skip security scan (faster)
/post-mortem --update-spec        # Update original spec with lessons
```
