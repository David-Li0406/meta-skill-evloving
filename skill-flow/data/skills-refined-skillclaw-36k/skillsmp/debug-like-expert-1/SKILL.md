---
name: debug-like-expert
description: Deep analysis debugging mode for complex issues. Activates methodical investigation protocol.
---

<objective>
Deep analysis debugging mode for complex issues. This skill activates methodical investigation protocols with evidence gathering, hypothesis testing, and rigorous verification when standard troubleshooting has failed.

The skill emphasizes treating code you wrote with MORE skepticism than unfamiliar code, as cognitive biases about "how it should work" can blind you to actual implementation errors. Use scientific method to systematically identify root causes rather than applying quick fixes.
</objective>

<context_scan>
**Run on every invocation to detect domain-specific debugging expertise:**

**Run on every invocation to detect domain-specific debugging expertise:**

```bash
# What files are we debugging?
echo "FILE_TYPES:"
find . -maxdepth 2 -type f 2>/dev/null | grep -E '\.(py|js|jsx|ts|tsx|rs|swift|c|cpp|go|java)$' | head -10

# Check for domain indicators
[ -f "package.json" ] && echo "DETECTED: JavaScript/Node project"
[ -f "Cargo.toml" ] && echo "DETECTED: Rust project"
[ -f "setup.py" ] || [ -f "pyproject.toml" ] && echo "DETECTED: Python project"
[ -f "*.xcodeproj" ] || [ -f "Package.swift" ] && echo "DETECTED: Swift/macOS project"
[ -f "go.mod" ] && echo "DETECTED: Go project"

# Scan for available domain expertise (LOCAL PROJECT)
echo "EXPERTISE_SKILLS:"
ls .agent/skills/expertise/ 2>/dev/null | head -5
```

**Present findings before starting investigation.**
</context_scan>

<domain_expertise>
**Domain-specific expertise lives in `.agent/skills/expertise/`**

Domain skills contain comprehensive knowledge including debugging, testing, performance, and common pitfalls. Before investigation, determine if domain expertise should be loaded.

<scan_domains>
```bash
ls .agent/skills/expertise/ 2>/dev/null
```

This reveals available domain expertise (e.g., macos-apps, iphone-apps, python-games, unity-games).

**If no expertise skills found:** Proceed without domain expertise (graceful degradation). The skill works fine with general debugging methodology.
</scan_domains>

<inference_rules>
If user's description or codebase contains domain keywords, INFER the domain and look for it in `.agent/skills/expertise`:

| Keywords/Files | Domain Skill |
|----------------|--------------|
| "Python", "game", "pygame", ".py" + game loop | expertise/python-games |
| "React", "Next.js", ".jsx/.tsx" | expertise/nextjs-ecommerce |
| "Rust", "cargo", ".rs" files | expertise/rust-systems |
| "Swift", "macOS", ".swift" + AppKit/SwiftUI | expertise/macos-apps |
| "iOS", "iPhone", ".swift" + UIKit | expertise/iphone-apps |
| "Unity", ".cs" + Unity imports | expertise/unity-games |

If domain inferred, confirm:
```
Detected: [domain] issue -> expertise/[skill-name]
Load this debugging expertise? (Y / see other options / none)
```
</inference_rules>

<load_domain>
When domain selected, READ all references from that skill:

```bash
cat .agent/skills/expertise/[domain]/references/*.md 2>/dev/null
```

This loads comprehensive domain knowledge BEFORE investigation.

**If domain skill not found:** Inform user and offer to proceed with general methodology.
</load_domain>
</domain_expertise>

<context>
This skill activates when standard troubleshooting has failed. The issue requires methodical investigation, not quick fixes. You are entering the mindset of a senior engineer who debugs with scientific rigor.

**Important**: If you wrote or modified any of the code being debugged, you have cognitive biases about how it works. Your mental model of "how it should work" may be wrong. Treat code you wrote with MORE skepticism than unfamiliar code - you're blind to your own assumptions.
</context>

<core_principle>
**VERIFY, DON'T ASSUME.** Every hypothesis must be tested. Every "fix" must be validated. No solutions without evidence.

**ESPECIALLY**: Code you designed or implemented is guilty until proven innocent. Your intent doesn't matter - only the code's actual behavior matters. Question your own design decisions as rigorously as you'd question anyone else's.
</core_principle>

<quick_start>

<evidence_gathering>

Before proposing any solution:

**A. Document Current State**
- What is the EXACT error message or unexpected behavior?
- What are the EXACT steps to reproduce?
- What is the ACTUAL output vs EXPECTED output?
- When did this start working incorrectly (if known)?

**B. Map the System**
- Trace the execution path from entry point to failure point
- Identify all components involved
- Read relevant source files completely, not just scanning
- Note dependencies, imports, configurations affecting this area

**C. Gather External Knowledge (when needed)**
- Use MCP servers for API documentation, library details, or domain knowledge
- Use web search for error messages, framework-specific behaviors, or recent changes
- Check official docs for intended behavior vs what you observe

</evidence_gathering>

<root_cause_analysis>

**A. Form Hypotheses**

Based on evidence, list possible causes:
1. [Hypothesis 1] - because [specific evidence]
2. [Hypothesis 2] - because [specific evidence]

**B. Test Each Hypothesis**

For each hypothesis:
- What would prove this true?
- What would prove this false?
- Design a minimal test
- Execute and document results

**C. Eliminate or Confirm**

Don't move forward until you can answer:
- Which hypothesis is supported by evidence?
- What evidence contradicts other hypotheses?

</root_cause_analysis>

<solution_development>

**Only after confirming root cause:**

**A. Design Solution**
- What is the MINIMAL change that addresses the root cause?
- What are potential side effects?
- What could this break?

**B. Implement with Verification**
- Make the change
- Add logging/debugging output if needed to verify behavior
- Document why this change addresses the root cause

**C. Test Thoroughly**
- Does the original issue still occur?
- Do the reproduction steps now work?
- Run relevant tests if they exist
- Check for regressions in related functionality

</solution_development>

</quick_start>

<critical_rules>
1. **NO DRIVE-BY FIXES**: If you can't explain WHY a change works, don't make it
2. **VERIFY EVERYTHING**: Test your assumptions. Read the actual code. Check the actual behavior
3. **USE ALL TOOLS**: MCP, Web Search, Thinking.
4. **THINK OUT LOUD**: Document your reasoning at each step
5. **ONE VARIABLE**: Change one thing at a time, verify, then proceed
6. **COMPLETE READS**: Don't skim code. Read entire relevant files
</critical_rules>

<success_criteria>
Before starting:
- [ ] Context scan executed to detect domain
- [ ] Domain expertise loaded if available and relevant

During investigation:
- [ ] Do you understand WHY the issue occurred?
- [ ] Have you verified the fix actually works?
- [ ] Have you tested the original reproduction steps?
- [ ] Have you checked for side effects?
- [ ] Can you explain the solution to someone else?

If you can't answer "yes" to all of these, keep investigating.
</success_criteria>

<output_format>
```markdown
## Issue: [Problem Description]

### Evidence
[What you observed - exact errors, behaviors, outputs]

### Investigation
[What you checked, what you found, what you ruled out]

### Root Cause
[The actual underlying problem with evidence]

### Solution
[What you changed and WHY it addresses the root cause]

### Verification
[How you confirmed this works and doesn't break anything else]
```
</output_format>
