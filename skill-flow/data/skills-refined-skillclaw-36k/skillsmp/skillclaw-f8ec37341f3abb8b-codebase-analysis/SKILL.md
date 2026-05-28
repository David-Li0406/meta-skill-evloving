---
name: codebase-analysis
description: Use this skill when you need to analyze a codebase, understand its architecture, or investigate specific patterns and behaviors within the code.
---

# Skill Body

## When to Use
- Codebase exploration and understanding
- Architecture analysis and mapping
- Pattern extraction and recognition
- Technical research within code
- Performance or security analysis

**NOT for:** wild guessing, assumptions without evidence, conclusions before investigation.

## Confidence Levels

| Bar | Lvl | Name        | Action                                      |
|-----|-----|-------------|---------------------------------------------|
| `░░░░░` | 0   | Gathering   | Collect initial evidence                     |
| `▓░░░░` | 1   | Surveying   | Broad scan, surface patterns                 |
| `▓▓░░░` | 2   | Investigating| Deep dive, verify patterns                   |
| `▓▓▓░░` | 3   | Analyzing   | Cross-reference, fill gaps                   |
| `▓▓▓▓░` | 4   | Synthesizing | Connect findings, high confidence            |
| `▓▓▓▓▓` | 5   | Concluded   | Deliver findings                             |

*Calibration: 0=0–19%, 1=20–39%, 2=40–59%, 3=60–74%, 4=75–89%, 5=90–100%*

Start honest. Clear codebase + focused question → level 2–3. Vague or complex → level 0–1.

At level 4: "High confidence in findings. One more angle would reach full certainty. Continue or deliver now?"

Below level 5: include `△ Caveats` section.

## Core Methodology
- **Evidence over assumption** — investigate when you can, guess only when you must.
- **Multi-source gathering** — code, docs, tests, history, web research, runtime behavior.
- **Multiple angles** — examine from different perspectives before concluding.
- **Document gaps** — flag uncertainty with △, track what's unknown.
- **Show your work** — findings include supporting evidence, not just conclusions.
- **Calibrate confidence** — distinguish fact from inference from assumption.

## Evidence Gathering

### Source Priority
1. **Direct observation** — read code, run searches, examine files
2. **Documentation** — official docs, inline comments, ADRs
3. **Tests** — reveal intended behavior and edge cases
4. **History** — git log, commit messages, PR discussions
5. **External research** — library docs, Stack Overflow, RFCs
6. **Inference** — logical deduction from available evidence
7. **Assumption** — clearly flagged when other sources unavailable

### Investigation Patterns
**Start broad, then narrow:**
- File tree → identify relevant areas
- Search patterns and keywords