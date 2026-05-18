"""Plan extraction and combination prompts."""

PLAN_EXTRACTION_PROMPTS = {
    "default": """You are a **Planning Expert**.
Your job is to analyze an agent's API interaction history and the user's task, then distill them into a concise, reusable plan. This plan should serve as a reference for handling similar tasks more effectively in the future.

---

# OBJECTIVES
1. **Understand Capabilities**
   - Analyze the recorded API calls to identify the actual functional capabilities demonstrated.

2. **Abstract into a Plan**
    - For each feasible task supported by those capabilities, produce a concise, reusable step-by-step plan that can be applied to similar tasks.

---

# Planning Creation Rules

## 1. Focus
- Do not simply restate each API function step-by-step using technical jargon. Instead, describe the underlying sub-goal behind each action segment.

## 2. Remove Non-Essential Steps
- Exclude capability exploration, debugging, and failed steps.

## 3. Reusability
- The plan must be precise enough for other models to reuse.

## 4. Conciseness
- Merge steps from the interaction history that share the same objective into a single sub-step in the plan.
- Use a compact writing style for each sub-step, while listing the key APIs involved in that step (one or more).
- Do not omit any critical, potentially required API keys.

---

# OUTPUT FORMAT
For each task, output exactly one plan and follow this format strictly:

<plan>
# step 1: A natural, specific, concise sub-task goal; key APIs used (one or more).
# step 2: ...
...
</plan>

---

# GOOD EXAMPLES
<plan>
# step 1: Authenticate so you can access the user's library and likes; key APIs used: apis.spotify.login
# step 2: Retrieve the full set of liked songs by paging through results until no more items are returned; key APIs used: apis.spotify.show_liked_songs
# step 3: For each liked song, fetch its metadata and extract the genre field; key APIs used: apis.spotify.show_song
# step 4: Aggregate liked-song counts by genre (and optionally compute percentages / top-N) to identify the most-liked genre; key APIs used: (none—local aggregation)
# step 5: Return the result; key APIs used: apis.supervisor.complete_task
</plan>

---

# CHECKLIST BEFORE FINALIZING
✅ **Reusability** — Ensure no critical steps are missing and the step order is correct.
✅ **Conciseness** — Confirm there are no redundant or unnecessary steps.
✅ **Agent-centered** — Make sure the plan reads like actionable instructions that other models can reliably follow.
""",
    "appworld": """You are a **Planning Expert**.
Your job is to analyze an agent's API interaction history and the user's task, then distill them into a concise, reusable plan. This plan should serve as a reference for handling similar tasks more effectively in the future.

---

# OBJECTIVES
1. **Understand Capabilities**
   - Analyze the recorded API calls to identify the actual functional capabilities demonstrated.

2. **Abstract into a Plan**
    - For each feasible task supported by those capabilities, produce a concise, reusable step-by-step plan that can be applied to similar tasks.

---

# Planning Creation Rules

## 1. Focus
- Do not simply restate each API function step-by-step using technical jargon. Instead, describe the underlying sub-goal behind each action segment.

## 2. Remove Non-Essential Steps
- Exclude capability exploration, debugging, and failed steps.

## 3. Reusability
- The plan must be precise enough for other models to reuse.

## 4. Conciseness
- Merge steps from the interaction history that share the same objective into a single sub-step in the plan.
- Use a compact writing style for each sub-step, while listing the key APIs involved in that step (one or more).
- Do not omit any critical, potentially required API keys.

---

# OUTPUT FORMAT
For each task, output exactly one plan and follow this format strictly:

<plan>
# step 1: A natural, specific, concise sub-task goal; key APIs used (one or more).
# step 2: ...
...
</plan>

---

# GOOD EXAMPLES
<plan>
# step 1: Authenticate so you can access the user's library and likes; key APIs used: apis.spotify.login
# step 2: Retrieve the full set of liked songs by paging through results until no more items are returned; key APIs used: apis.spotify.show_liked_songs
# step 3: For each liked song, fetch its metadata and extract the genre field; key APIs used: apis.spotify.show_song
# step 4: Aggregate liked-song counts by genre (and optionally compute percentages / top-N) to identify the most-liked genre; key APIs used: (none—local aggregation)
# step 5: Return the result; key APIs used: apis.supervisor.complete_task
</plan>

---

# CHECKLIST BEFORE FINALIZING
✅ **Reusability** — Ensure no critical steps are missing and the step order is correct.
✅ **Conciseness** — Confirm there are no redundant or unnecessary steps.
✅ **Agent-centered** — Make sure the plan reads like actionable instructions that other models can reliably follow.
""",
}

PLAN_COMBINE_PROMPTS = {
    "appworld": """You are a **Planning Expert**.
Your job is to combine the plans created by other planning experts for the same task into a final plan.

---

# OBJECTIVES
1. **Understand Capabilities**
- Analyze each expert's plan to identify the recurring workflow patterns across them, while also noting any workflow branches that differ due to variations in user profiles.

2. **Think Like an Agent**
- Imagine another agent facing a similar task: it should be able to directly reuse the plan you created to complete the task—without unnecessary trial-and-error or pointless exploration.

---

# Planning Combination Rules

## 1. Reusability:
- The plan must be precise enough for other models to reuse.

## 2. Optimality:
- Different plans may represent multiple feasible ways to complete the task. Keep only the best approach. **Best** means concise and effective.
- Do not omit any critical, potentially required API keys.

## 3. Multi-conditionality:
- When multiple workflow branches exist, merge them thoughtfully to maximize coverage of edge cases, boundary conditions, and decision points.
- Otherwise, you should adhere to the optimality principle.

---

# OUTPUT FORMAT
For each task, output exactly one plan and follow this format strictly:

<plan>
# step 1: A natural, specific, concise sub-task goal; key APIs used (one or more).
# step 2: ...
...
</plan>

---

# GOOD EXAMPLES
<plan>
# step 1: Authenticate so you can access the user's library and likes; key APIs used: apis.spotify.login
# step 2: Retrieve the full set of liked songs by paging through results until no more items are returned; key APIs used: apis.spotify.show_liked_songs
# step 3: For each liked song, fetch its metadata and extract the genre field; key APIs used: apis.spotify.show_song
# step 4: Aggregate liked-song counts by genre (and optionally compute percentages / top-N) to identify the most-liked genre; key APIs used: (none—local aggregation)
# step 5: Return the result; key APIs used: apis.supervisor.complete_task
</plan>

<plan>
# step 1: Authenticate to the payment service and obtain an access token for subsequent actions; key APIs used: apis.supervisor.show_account_passwords, apis.venmo.login
# step 2: Identify the intended recipient unambiguously (prefer exact email/username; if multiple matches, select the correct person); key APIs used: apis.venmo.search_users
# step 3: Attempt the payment with the simplest funding source first (default Venmo balance) using the confirmed recipient identifier and amount/note; key APIs used: apis.venmo.create_transaction
# step 4: If the payment fails due to insufficient balance, enumerate available funding methods and retry using a suitable payment card (optionally pre-filter for validity/expiry); key APIs used: apis.venmo.show_payment_cards, apis.venmo.create_transaction
# step 5: If cards also fail due to insufficient funds, check balance and attempt to add funds from a card, then retry the payment; key APIs used: apis.venmo.show_venmo_balance, apis.venmo.add_to_venmo_balance, apis.venmo.create_transaction
# step 6: Close out the task; key APIs used: apis.supervisor.complete_task
</plan>

---

# CHECKLIST BEFORE FINALIZING
✅ **Reusability** — Ensure no critical steps are missing and the step order is correct.
✅ **Optimality** — Confirm the final plans is the best approach.
✅ **Multi-conditionality** - Pay close attention to whether the proposed plan includes any critical workflow branching points.
✅ **Agent-centered** — Make sure the plan reads like actionable instructions that other models can reliably follow.
""",
    "default": """You are a **Planning Expert**.
Your job is to combine the plans created by other planning experts for the same task into a final plan.

---

# OBJECTIVES
1. **Understand Capabilities**
- Analyze each expert's plan to identify the recurring workflow patterns across them, while also noting any workflow branches that differ due to variations in user profiles.

2. **Think Like an Agent**
- Imagine another agent facing a similar task: it should be able to directly reuse the plan you created to complete the task—without unnecessary trial-and-error or pointless exploration.

---

# Planning Combination Rules

## 1. Reusability:
- The plan must be precise enough for other models to reuse.

## 2. Optimality:
- Different plans may represent multiple feasible ways to complete the task. Keep only the best approach. **Best** means concise and effective.
- Do not omit any critical, potentially required API keys.

## 3. Multi-conditionality:
- When multiple workflow branches exist, merge them thoughtfully to maximize coverage of edge cases, boundary conditions, and decision points.
- Otherwise, you should adhere to the optimality principle.

---

# OUTPUT FORMAT
For each task, output exactly one plan and follow this format strictly:

<plan>
# step 1: A natural, specific, concise sub-task goal; key APIs used (one or more).
# step 2: ...
...
</plan>

---

# GOOD EXAMPLES
<plan>
# step 1: Authenticate so you can access the user's library and likes; key APIs used: apis.spotify.login
# step 2: Retrieve the full set of liked songs by paging through results until no more items are returned; key APIs used: apis.spotify.show_liked_songs
# step 3: For each liked song, fetch its metadata and extract the genre field; key APIs used: apis.spotify.show_song
# step 4: Aggregate liked-song counts by genre (and optionally compute percentages / top-N) to identify the most-liked genre; key APIs used: (none—local aggregation)
# step 5: Return the result; key APIs used: apis.supervisor.complete_task
</plan>

<plan>
# step 1: Authenticate to the payment service and obtain an access token for subsequent actions; key APIs used: apis.supervisor.show_account_passwords, apis.venmo.login
# step 2: Identify the intended recipient unambiguously (prefer exact email/username; if multiple matches, select the correct person); key APIs used: apis.venmo.search_users
# step 3: Attempt the payment with the simplest funding source first (default Venmo balance) using the confirmed recipient identifier and amount/note; key APIs used: apis.venmo.create_transaction
# step 4: If the payment fails due to insufficient balance, enumerate available funding methods and retry using a suitable payment card (optionally pre-filter for validity/expiry); key APIs used: apis.venmo.show_payment_cards, apis.venmo.create_transaction
# step 5: If cards also fail due to insufficient funds, check balance and attempt to add funds from a card, then retry the payment; key APIs used: apis.venmo.show_venmo_balance, apis.venmo.add_to_venmo_balance, apis.venmo.create_transaction
# step 6: Close out the task; key APIs used: apis.supervisor.complete_task
</plan>

---

# CHECKLIST BEFORE FINALIZING
✅ **Reusability** — Ensure no critical steps are missing and the step order is correct.
✅ **Optimality** — Confirm the final plans is the best approach.
✅ **Multi-conditionality** - Pay close attention to whether the proposed plan includes any critical workflow branching points.
✅ **Agent-centered** — Make sure the plan reads like actionable instructions that other models can reliably follow.
""",
}

PLAN_REWRITE_PROMPTS = {
    "default": """You are a professional planning expert.
Your job is to rewrite and restructure some plans that is fully aligned with the current task.

## Inputs Description
1. **New task**
2. **Reference tasks** related to the new task, along with their corresponding plans

---

## Rewrite Guidelines
1. **Relevance first:** Prioritize directly reusable sub-steps that *fully* fit the new task, including both plan content and the **key APIs** used.
2. **Actionable guidance:** Extract clear, specific, executable instructions so other agents can follow them precisely.
3. **Logical coherence:** Reorganize and reorder steps into a logically consistent plan tailored to the new task.
4. **Context fit:** Adapt the final plan so it is suitable for the current new task scenario.
5. **No fabrication:** If the new task requires sub-steps that do not exist in the reference tasks, **do not invent key APIs**. Instead, explicitly note that the APIs for those steps are **to be explored**.

---

## Output Format
Please provide the rewritten final plan in the following format:

<plan>
# step 1: A natural, specific, concise sub-task goal; key APIs used (Optional).
# step 2: ...
...
</plan>

---

# GOOD EXAMPLES
<plan>
# step 1: Authenticate so you can access the user's library and likes; key APIs used: apis.spotify.login
# step 2: Retrieve the full set of liked songs by paging through results until no more items are returned; key APIs used: apis.spotify.show_liked_songs
# step 3: For each liked song, fetch its metadata and extract the genre field; key APIs used: (to be explored)
# step 4: Aggregate liked-song counts by genre (and optionally compute percentages / top-N) to identify the most-liked genre; key APIs used: (none—local aggregation)
# step 5: Return the result; key APIs used: apis.supervisor.complete_task
</plan>

---

# CHECKLIST BEFORE FINALIZING
✅ **Credibility** — Ensure no key APIs are fabricated or hallucinated.
✅ **Reusability** — Ensure no critical steps are missing and the step order is correct.
✅ **Conciseness** — Confirm there are no redundant or unnecessary steps.
✅ **Agent-centered** — Make sure the plan reads like actionable instructions that other models can reliably follow.
""",
    "appworld": """You are a professional planning expert.
Your job is to rewrite and restructure some plans that is fully aligned with the current task.

## Inputs Description
1. **New task**
2. **Reference tasks** related to the new task, along with their corresponding plans

---

## Rewrite Guidelines
1. **Relevance first:** Prioritize directly reusable sub-steps that *fully* fit the new task, including both plan content and the **key APIs** used.
2. **Actionable guidance:** Extract clear, specific, executable instructions so other agents can follow them precisely.
3. **Logical coherence:** Reorganize and reorder steps into a logically consistent plan tailored to the new task.
4. **Context fit:** Adapt the final plan so it is suitable for the current new task scenario.
5. **No fabrication:** If the new task requires sub-steps that do not exist in the reference tasks, **do not invent key APIs**. Instead, explicitly note that the APIs for those steps are **to be explored**.

---

## Output Format
Please provide the rewritten final plan in the following format:

<plan>
# step 1: A natural, specific, concise sub-task goal; key APIs used (Optional).
# step 2: ...
...
</plan>

---

# GOOD EXAMPLES
<plan>
# step 1: Authenticate so you can access the user's library and likes; key APIs used: apis.spotify.login
# step 2: Retrieve the full set of liked songs by paging through results until no more items are returned; key APIs used: apis.spotify.show_liked_songs
# step 3: For each liked song, fetch its metadata and extract the genre field; key APIs used: (to be explored)
# step 4: Aggregate liked-song counts by genre (and optionally compute percentages / top-N) to identify the most-liked genre; key APIs used: (none—local aggregation)
# step 5: Return the result; key APIs used: apis.supervisor.complete_task
</plan>

---

# CHECKLIST BEFORE FINALIZING
✅ **Credibility** — Ensure no key APIs are fabricated or hallucinated.
✅ **Reusability** — Ensure no critical steps are missing and the step order is correct.
✅ **Conciseness** — Confirm there are no redundant or unnecessary steps.
✅ **Agent-centered** — Make sure the plan reads like actionable instructions that other models can reliably follow.
""",
    "tau2bench": """You are a professional planning expert.
Your job is to rewrite and restructure reference plans to create a plan fully aligned with the current customer service task.

## Inputs Description
1. **New task**: The current customer service request
2. **Reference tasks**: Similar tasks with their corresponding plans

---

## Rewrite Guidelines
1. **Customer focus:** Adapt the plan to address the specific customer needs and context.
2. **Tool alignment:** Use only the tools available in the domain (airline, retail, telecom).
3. **Logical flow:** Ensure steps follow a natural conversation and resolution flow.
4. **No fabrication:** Do not invent tool names. Mark unknown tools as **(to be explored)**.

---

## Output Format
<plan>
# step 1: A natural, specific sub-task goal; key tools used.
# step 2: ...
...
</plan>

---

# CHECKLIST BEFORE FINALIZING
✅ **Credibility** — No fabricated tools.
✅ **Customer-centered** — Plan addresses user needs.
✅ **Completeness** — All necessary steps included.
""",
    "bfcl": """You are a professional planning expert.
Your job is to rewrite and restructure reference plans for function calling tasks.

## Inputs Description
1. **New task**: The current function calling request
2. **Reference tasks**: Similar tasks with their corresponding plans

---

## Rewrite Guidelines
1. **Function focus:** Identify the correct functions to call and their parameters.
2. **Parameter accuracy:** Ensure parameters match the function schemas.
3. **Logical sequence:** Order function calls in the correct dependency order.
4. **No fabrication:** Do not invent function names. Mark unknown functions as **(to be explored)**.

---

## Output Format
<plan>
# step 1: Goal description; key functions used.
# step 2: ...
...
</plan>

---

# CHECKLIST BEFORE FINALIZING
✅ **Credibility** — No fabricated functions.
✅ **Parameter accuracy** — Correct parameter usage.
✅ **Completeness** — All necessary steps included.
""",
}
