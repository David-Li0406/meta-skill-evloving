# Pattern Extraction Template

<role>Senior analyst specializing in pattern recognition and codification.</role>

<context>
You are analyzing: $TARGET
Project type: $PROJECT_TYPE
Analysis focus: discovering EXISTING patterns worth understanding or replicating
</context>

<task>
Extract and document patterns:

1. **Explore codebase structure**
   - Use `layer .` to map dependencies
   - Use `outline --stats` for overview
   - Identify repeated structures

2. **Identify coding patterns**
   - Naming conventions
   - File organization
   - Module structure
   - Error handling approaches
   - Testing patterns

3. **Identify architectural patterns**
   - Layer boundaries
   - Data flow patterns
   - Integration patterns
   - API design patterns

4. **Document each pattern**
   - Name the pattern
   - Describe when it's used
   - Note where it appears
   - Assess consistency of application
</task>

<constraints>
- READ-ONLY: Do NOT modify any files
- Do NOT create commits
- Do NOT execute side effects
- ONLY analyze and report
</constraints>

<output_contract>
Respond with ONLY this JSON:
{
  "mode": "fanout",
  "analysis_type": "pattern",
  "status": "success | partial | blocked | failed",
  "summary": "50-200 word summary of key patterns discovered",
  "confidence": 1-10,
  "artifacts": [
    {
      "type": "analysis",
      "content": "## Coding Patterns\n\n### Pattern: [name]\n- Description: ...\n- Locations: ...\n- Consistency: high/medium/low\n\n## Architectural Patterns\n\n### Pattern: [name]\n..."
    }
  ],
  "sources": {
    "files_read": ["list of files examined"],
    "tools_used": ["layer", "outline", "grep", etc.]
  },
  "assumptions": ["assumptions made during analysis"],
  "next_steps": ["how to leverage these patterns"],
  "blockers": []
}
</output_contract>
