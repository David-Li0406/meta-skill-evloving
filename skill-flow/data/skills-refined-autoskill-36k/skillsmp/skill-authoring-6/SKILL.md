---
name: skill-authoring
description: Standard for authoring agent instruction documents (SKILL.md + references/) using TOON decision trees.
argument-hint: "[empty]"
---

orientation: "You are an autonomous senior engineer writing instructions for other autonomous agents. Your job is to produce cold-start safe, non-contradictory, decision-tree-based procedures with exact commands and explicit context. These instructions will govern critical work and will be reviewed by independent third parties, so write them to the highest possible standard."

title: Skill Authoring Standard
protocol:
  id: SKILL-AUTHORING-STANDARD
  version: 1.0.0
  type: executable_specification
  inputs[1]:
    - none
  outputs[1]:
    - SkillInstructionSet

references[1]:
  - path: documents/standards/instructions/AGENT_INSTRUCTION_AUTHORING_STANDARD.md
    purpose: "Human-readable standard and templates for writing SKILL.md and references/."

decision_tree:
  entrypoint: STANDARD
  nodes[1]:
    - id: STANDARD
      purpose: "Load the canonical authoring standard before writing or editing any skill instructions."
      action: invoke_reference
      reference: documents/standards/instructions/AGENT_INSTRUCTION_AUTHORING_STANDARD.md
