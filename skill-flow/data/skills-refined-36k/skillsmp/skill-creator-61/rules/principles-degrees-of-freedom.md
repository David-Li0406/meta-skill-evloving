---
title: Set Appropriate Degrees of Freedom
impact: HIGH
impactDescription: Prevents hallucinations and errors in critical tasks
tags: principles, control
---

## Set Appropriate Degrees of Freedom

**Impact: HIGH**

Match the specificity of your instructions to the fragility of the task. High freedom for creative choices, low freedom for fragile operations.

**Incorrect (mismatched freedom):**

```markdown
<!-- High freedom for a fragile task -->

To deploy the database, just check the cloud console and try to find the right button. Maybe look for "Deploy" or "Start".
```

**Correct (matched freedom):**

```markdown
<!-- Low freedom for a fragile task -->

To deploy the database, run the specific script: `scripts/deploy_db.sh --env=prod`. Do not attempt manual deployment.
```
