"""Skill extraction prompts for functional and atomic skills."""

# Functional skill extraction (step-based, AppWorld/BFCL style)
FUNCTIONAL_SKILL_PROMPT = """An agent system is provided with a **Skill Library** and has tried to solve the task multiple times with a successful solution. Review the task-solving attempt and extract generalizable skills.

# 1. Inputs Description
- **User Task**
- **Trajectory**: A record of an agent's interactions successfully with the environment as it attempts to complete a user task.
- **Skill Library**: A collection of all currently available skills that can be directly reused.
- **Specific-step**: Given a concrete step, extract only one reusable skill for the specified step.

---

# 2. Skill Definition Rule
- Skill is a dictionary with four keys: `name`, `document`, `content` and `tools`.
1) `name`: the skill's name.
2) `document`: the skill's functionality, the key parameters, the final output of the skill and any important notes.
3) `content`: the concrete implementation of the skill.
4) `tools`: the key tools used in the skill (list).
- The skill is abstract, modular, and reusable. Specifically, the skill name must be generic under one application (e.g., `spotify get songs by genre` instead of `get pop songs`). The skill must use parameters instead of hard-coded values (e.g., specific email address "jay@gmail.com"). The skill body must be self-contained.
- Explicitly declare the key parameters and the final output data types using type hints. Example: `Parameters: param: str; Outputs: output: list[dict]:`
- Include detailed description of the skill with input and output explanation.
- The skill should not be similar to the existing skills in the skill library.
- The skill must involve multiple processing steps. Simply using the result of an API call without additional logic does not qualify as a valid skill.
- Never call other skills from the skill library or any previously defined skills.
- Do not import any Python packages.
- Avoid a functional style; there's no need to use return.

---

# 3. Update Existing Skills
Your goal is to ensure the system retains actionable skill that helps it behave correctly in the future.

You have three options: **[modify, add, keep]**
- **modify**: revise an existing skill to make it more effective (e.g., improving documents). Only change `content` when necessary, and ensure the resulting skill remains broadly reusable/general-purpose.
- **add**: introduce a new skill only when existing skills cannot support a critical step, in order to improve future performance.
- **keep**: Preserve the skill unchanged when there are no clear issues.

Common actions:
- add a new skill
- update a skill's usage instructions/documentation
- revise a skill's variable/parameter definitions to make it more generalizable
- if a skill is overly complex, refactor it into more modular skills (involving both **modify** and **add**)
- keep a skill unchanged
- ...

---

# 4. Requirements for each skill that is modified or added.
- **Avoid duplication**: If a skill library is provided, do not add new skills that are similar to existing ones—use **keep** or **modify** instead.
- **Exclude non-solution behavior**: Do not include capability exploration, debugging activities, or any failed/incorrect steps.
- **Ensure domain specificity**: The skill must reference domain-specific libraries/APIs, e.g., apis.spotify.show_playlist_library.
- **Avoid over-wrapping**: Verify the implementation is not merely a thin wrapper around another skill (i.e., not just calling a single underlying skill without meaningful additional logic).
- **Specific-step guided extraction**: Only focus on the specified step in the trajectory when extracting skills.

---

# 5. Good Skill Example

{
    "name": "spotify get all user playlists",
    "document": "Retrieve every playlist in the authenticated user's library by paging through results until none remain.\\n\\nParameters\\n----------\\naccess_token : str\\n    Valid Spotify access token for the user.\\n\\nOutputs\\n-------\\nlist[dict]\\n    A list containing every playlist object in the user's library.\\n\\nNotes:\\n-------\\n1. Use a moderate page_limit, avoid setting it too high to prevent exceeding the page limit error.\\n2. Avoid printing the entire retrieved list to prevent overly long outputs; instead, inspect only a small subset to verify the structure.\\n",
    "content": "playlists = []\\n\\npage = 0\\nwhile True:\\n    batch = apis.spotify.show_playlist_library(\\n        access_token=access_token,\\n        page_index=page,\\n        page_limit=20\\n    )\\n    if not batch:          # empty page signals end\\n        break\\n    playlists.extend(batch)\\n    page += 1",
    "tools": ["apis.spotify.show_playlist_library"]
}

---

# 6. Output Format
you will finish by returning in this JSON format as follows:
```json
[
    {
        "option": "add",
        "skill": {
            "name": "skill_name",
            "document": "The skill's functionality, parameters, outputs, and important notes...",
            "content": "The concrete implementation code...",
            "tools": ["apis.app.method"]
        }
    },
    {
        "option": "modify",
        "skill": {
            "name": "existing_skill_name",
            "document": "Updated documentation...",
            "content": "Updated implementation...",
            "tools": ["apis.app.method"]
        },
        "modified_from": "existing_skill_name"
    },
    {
        "option": "keep",
        "skill_name": "the kept skill name"
    }
]
```
Note that your updated skills may not need to cover all the options. You can only use one type of updates or choose to remain all skills unchanged.

---

# 7. CHECKLIST BEFORE FINALIZING
✅ **Reusability** — Ensure no critical steps are missing, each skill is modular, all parameters are abstract rather than specific.
✅ **Optimality** — Ensure each skill meets the required definition standards.
✅ **Agent-centered** — Add helpful notes in each skill to guide other models in using it correctly.
✅ **Specific-step focus** — Whether the extracted skill includes any content that does not belong to this step?
"""

# Atomic skill extraction (tool-centric, τ²-Bench style)
ATOMIC_SKILL_PROMPT = """An agent system is provided with a **Skill Library** and has tried to solve the task multiple times with a successful solution. Review the task-solving attempt and extract generalizable skills.

# 1. Inputs Description
- **User Task**
- **Trajectory**: A record of an agent's interactions successfully with the environment as it attempts to complete a user task.
- **Skill Library**: A collection of all currently available skills that can be directly reused.
- **Specific-Tool**: Given a specific tool, extract only one reusable skill for the specified tool.

---

# 2. Skill Definition Rule
- Skill is a dictionary with four keys: `name`, `document`, `content` and `tools`.
1) `name`: the specific tool's name.
2) `document`: the tool's functionality, the key parameters, the final output of the skill and any important notes.
3) `content`: the tool's usage examples, and examples of combining it with other tools (if applicable).
4) `tools`: the key tools used in the `content` (list).
- The skill is centered around a specific tool, describing its core functionality, important notes, and common usage examples.
- Explicitly declare the key parameters and the final output data types using type hints. Example: `Parameters: param: str; Outputs: output: dict:`
- Include detailed description of the skill with input and output explanation.
- The skill should not be similar to the existing skills in the skill library.
- The parameters used in `content` must be reusable instead of hard-coded values (e.g., specific email address "jay@gmail.com")
- The usage examples of `content` may involve one or more tool uses.
- The `document` must clearly and thoroughly document all relevant details of the specific tool use.
- Never call other skills from the skill library or any previously defined skills.
- Do not import any Python packages.
- Avoid a functional style and Python code style; there's no need to use return.

---

# 3. Update Existing Skills
Your goal is to ensure the system retains actionable skill that helps it behave correctly in the future.

You have three options: **[modify, add, keep]**
- **modify**: revise an existing skill to make it more effective (e.g., improving documents). Only change `content` when necessary, and ensure the resulting skill remains broadly general-purpose.
- **add**: introduce a new skill only when existing skill library missing the the specified tool.
- **keep**: Preserve the skill unchanged when there are no clear issues.

Common actions:
- add a new skill
- update a skill's usage instructions/documentation
- revise a skill's variable/parameter definitions to make it more generalizable
- keep a skill unchanged
- ...

---

# 4. Requirements for each skill that is modified or added.
- **Avoid duplication**: If a skill library is provided, do not add new skills that are similar to existing ones—use **keep** or **modify** instead.
- **Ensure domain specificity**: The skill must contain domain-specific tool.
- **Specific-Tool guided extraction**: Only focus on the specified tool in the trajectory when extracting skills.

---

# 5. Good Skill Example

{
    "name": "get_flight_status",
    "document": "This tool retrieves the real-time status of a specific flight on a given date. It is essential for verifying flight delays, cancellations, or confirming if a flight has landed to address customer inquiries or complaints. \\nParameters: \\n- `flight_number`: str. The unique identifier of the flight (e.g., 'HAT018').\\n- `date`: str. The date of the flight in 'YYYY-MM-DD' format.\\nOutputs: \\n- `status`: str. A string representing the flight's status (e.g., 'delayed', 'landed', 'on-time', 'cancelled').\\nImportant Notes: \\n- To get an accurate status, both the `flight_number` and the correct `date` must be provided, as the same flight number may operate on multiple days.",
    "content": "Example1: A user complains about a past flight being delayed.\\n\\nassistant:\\nFirst, the assistant identifies the user and retrieves their reservation history to locate the relevant flight.\\nget_user_details(user_id='the_user_id')\\nTo investigate the user's claim, first retrieve the details of their reservation to find the flight number and date.\\nget_reservation_details(reservation_id='a_reservation_id')\\nAfter identifying the specific flight number and date from the reservation details, check its status.\\nget_flight_status(flight_number='flight_number_from_reservation', date='flight_date_from_reservation')",
    "tools": ["get_user_details", "get_reservation_details", "get_flight_status"]
}

---

# 6. Output Format
you will finish by returning in this JSON format as follows:
```json
[
    {
        "option": "add",
        "skill": {
            "name": "the_tool_name",
            "document": "The tool's functionality, parameters, outputs, and important notes...",
            "content": "Example usage showing how to use this tool...",
            "tools": ["the_tool_name", "other_tools_if_any"]
        }
    },
    {
        "option": "modify",
        "skill": {
            "name": "existing_tool_name",
            "document": "Updated documentation...",
            "content": "Updated examples...",
            "tools": ["tool1", "tool2"]
        },
        "modified_from": "existing_tool_name"
    },
    {
        "option": "keep",
        "skill_name": "the kept skill name"
    }
]
```
Note that your updated skills may not need to cover all the options. You can only use one type of updates or choose to remain all skills unchanged.

---

# 7. CHECKLIST BEFORE FINALIZING
✅ **Reusability** — Ensure no critical steps are missing, each skill is modular, all parameters are abstract rather than specific.
✅ **Optimality** — Ensure each skill meets the required definition standards.
✅ **Agent-centered** — Add helpful notes in each skill to guide other models in using it correctly.
✅ **Specific-Tool focus** — Whether the extracted skill doesn't center around this Tool?
"""

SKILL_EXTRACTION_PROMPTS = {
    "default": FUNCTIONAL_SKILL_PROMPT,
    "appworld": FUNCTIONAL_SKILL_PROMPT,
    "bfcl": FUNCTIONAL_SKILL_PROMPT,
    "tau2bench": ATOMIC_SKILL_PROMPT,
    "functional": FUNCTIONAL_SKILL_PROMPT,
    "atomic": ATOMIC_SKILL_PROMPT,
}
