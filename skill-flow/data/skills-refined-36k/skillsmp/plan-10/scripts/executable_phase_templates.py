#!/usr/bin/env python3
"""
Phase Templates - Provides structured templates for each phase type.

Each template defines:
- Phase objectives
- Required inputs
- Expected outputs
- Memory management guidelines
"""

from pathlib import Path
from typing import Dict


PHASE_TEMPLATES: Dict[str, str] = {
    "research": """# Research Phase

**Objective:** Gather information to understand problem space

**Outputs Required:**
- `research_findings.md` - Key findings
- `phase_summary.md` - <500 words summary
- `.plans/knowledge-base/*.md` - Reference docs (as needed)

## Process

1. **Identify Information Needs**
   - What needs understanding?
   - Relevant existing code/systems?
   - Constraints?

2. **Gather Information**
   - Search codebase for patterns
   - Read existing documentation
   - Identify dependencies

3. **Document Findings**
   - Create knowledge-base files for cross-phase references
   - Write research_findings.md with insights
   - Write concise phase_summary.md (<500 words)

4. **Prepare for Planning**
   - List key considerations
   - Identify approaches
   - Note constraints

**Checklist:**
- [ ] Critical information gathered
- [ ] Findings in knowledge-base
- [ ] phase_summary.md created (<500 words)
- [ ] Ready for planning
""",

    "planning": """# Planning Phase

**Objective:** Design solution based on research

**Inputs:** `../research/phase_summary.md` ONLY (not full research)

**Outputs Required:**
- `plan.md` - Implementation plan
- `architecture.md` - Design decisions
- `phase_summary.md` - <500 words summary

## Process

1. **Review Research**
   - Load research/phase_summary.md ONLY
   - Identify constraints and requirements

2. **Design Solution**
   - Define architecture
   - Break into steps
   - Order by dependencies

3. **Create Plan**
   - Write plan.md with implementation steps
   - Document architecture decisions
   - List required resources

4. **Write Summary**
   - Summarize approach (<300 words)
   - List critical decisions
   - Note key files/components

**Checklist:**
- [ ] Implementation plan created
- [ ] Architecture documented
- [ ] phase_summary.md created (<500 words)
- [ ] Ready for revision
""",

    "revision": """# Revision Phase

**Objective:** Review and refine plan

**Inputs:**
- `../planning/phase_summary.md`
- `../planning/plan.md`

**Outputs Required:**
- `review_notes.md` - Findings
- `revised_plan.md` - Updates (if needed)
- `phase_summary.md` - <500 words summary

## Process

1. **Review Plan**
   - Check completeness and feasibility
   - Identify gaps or risks

2. **Provide Feedback**
   - Document concerns in review_notes.md
   - Suggest improvements
   - Validate against requirements

3. **Revise if Needed**
   - Update plan or approve as-is
   - Create revised_plan.md if changed

4. **Write Summary**
   - Summarize review outcomes
   - List key changes (if any)

**Checklist:**
- [ ] Plan reviewed
- [ ] Feedback documented
- [ ] Revisions made (if needed)
- [ ] phase_summary.md created (<500 words)
- [ ] Ready for building
""",

    "building": """# Building Phase

**Objective:** Implement the solution

**Inputs:**
- `../revision/phase_summary.md`
- `../planning/plan.md`
- Knowledge base (on-demand)

**Outputs Required:**
- Implementation artifacts (code, configs)
- `implementation_log.md` - Deviations and key decisions
- `phase_summary.md` - <500 words summary

## Process

1. **Load Plan**
   - Read planning/plan.md and revision/phase_summary.md
   - Prepare checklist

2. **Execute Implementation**
   - Follow plan step-by-step
   - Document deviations in implementation_log.md
   - Reference knowledge base as needed

3. **Track Progress**
   - Note issues or changes from plan
   - Document new decisions

4. **Write Summary**
   - Summarize what was built
   - Note deviations
   - List artifacts

**Checklist:**
- [ ] All planned items implemented
- [ ] Deviations documented
- [ ] implementation_log.md created
- [ ] phase_summary.md created (<500 words)
- [ ] Ready for validation
""",

    "validation": """# Validation Phase

**Objective:** Verify implementation works correctly

**Inputs:**
- `../building/phase_summary.md`
- `../building/implementation_log.md` (if needed)

**Outputs Required:**
- `validation_results.md` - Test results
- `issues.md` - Problems found (if any)
- `phase_summary.md` - <500 words summary

## Process

1. **Review Implementation**
   - Load building/phase_summary.md
   - Understand what was built

2. **Execute Validation**
   - Run tests if applicable
   - Verify against requirements
   - Check for issues

3. **Document Results**
   - Write validation_results.md
   - List issues in issues.md (if any)
   - Note pass/fail per requirement

4. **Write Summary**
   - Summarize outcomes
   - List critical issues (if any)

**Checklist:**
- [ ] Validation executed
- [ ] Results documented
- [ ] phase_summary.md created (<500 words)
- [ ] Ready for cleanup or iteration
""",

    "cleanup": """# Cleanup Phase

**Objective:** Finalize project

**Inputs:** All phase summaries ONLY

**Outputs Required:**
- `final_summary.md` - Complete project summary

## Process

1. **Review Phase Summaries**
   - Load each phase/phase_summary.md
   - Understand project flow

2. **Create Final Summary**
   - Project goal and what was accomplished
   - Key decisions and outcomes
   - Final artifacts and locations

3. **Confirm Cleanup**
   - Ask user if plan files should be removed
   - Run cleanup utility if yes

**Checklist:**
- [ ] final_summary.md created
- [ ] User consulted about cleanup
- [ ] Project finalized
"""
}


def create_phase_plan(phase: str, output_path: Path) -> None:
    """Create a phase plan file from template."""
    if phase not in PHASE_TEMPLATES:
        raise ValueError(f"Unknown phase: {phase}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(PHASE_TEMPLATES[phase])
    print(f"✅ Created phase plan: {output_path}")


def main():
    """CLI interface for phase templates."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate phase plan templates")
    parser.add_argument("phase", choices=list(PHASE_TEMPLATES.keys()), help="Phase name")
    parser.add_argument("output", help="Output file path")

    args = parser.parse_args()
    create_phase_plan(args.phase, Path(args.output))


if __name__ == "__main__":
    main()
