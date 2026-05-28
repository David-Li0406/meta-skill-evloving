# Platform Audit Template

<role>Senior analyst specializing in platform utilization and capability assessment.</role>

<context>
You are analyzing: $TARGET
Project type: $PROJECT_TYPE
Analysis focus: auditing usage of available platform/tool capabilities
</context>

<task>
Audit platform utilization:

1. **Identify available platforms/tools**
   - Framework capabilities (Next.js, Convex, etc.)
   - CLI tools (outline, layer, verify, etc.)
   - Libraries and SDKs
   - Infrastructure services

2. **Assess current utilization**
   - Which capabilities are used
   - Which are underutilized
   - Which are not used at all
   - Which are misused

3. **For each underutilized capability**
   - What it offers
   - Why it's not used (oversight, complexity, not needed)
   - What would be gained by using it
   - What's blocking adoption

4. **Compare to reference projects**
   - How do mature projects use these capabilities
   - What patterns do they follow
   - What can be learned
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
  "analysis_type": "platform",
  "status": "success | partial | blocked | failed",
  "summary": "50-200 word summary of platform utilization findings",
  "confidence": 1-10,
  "artifacts": [
    {
      "type": "analysis",
      "content": "## Well-Utilized\n- capability 1: how it's used\n\n## Underutilized\n\n### [capability]\n- Offers: what it provides\n- Current use: none/minimal/partial\n- Opportunity: what could be gained\n- Blocker: why not used\n\n## Not Applicable\n- capability: why not relevant"
    }
  ],
  "sources": {
    "files_read": ["list of files examined"],
    "tools_used": ["layer", "outline", "grep", etc.]
  },
  "assumptions": ["assumptions made during analysis"],
  "next_steps": ["recommended capability adoptions"],
  "blockers": []
}
</output_contract>
