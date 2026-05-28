---
trigger: always_on
---

# Topic & Skill Enforcement Rule

- **Context Verification**: Before starting any task, check the current workspace for the `.agent/skills/` folder. 
- **Skill Alignment**: If a user request matches the "Description" or "Goal" of any local skill, you MUST equip that skill before providing a solution.
- **Topic Guardrail**: Our primary mission is "ADHD Medication & Supplement Tracking." If a user request is significantly off-topic (e.g., asking for cooking recipes or unrelated travel tips), verify how it relates to our mission. If it does not, politely redirect the user to stay focused on the project's core goals.
- **Compliance Audit**: Always cross-reference your generated code against our `adhd-ui-optimizer` and `med-safety-checker` skills to ensure high-contrast design and medical accuracy.