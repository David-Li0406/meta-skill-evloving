---
name: hlab-planner
description: Designs atomic specs from ambiguous requests when you need a modular plan; use it to define scope, architecture, and inputs. Output is a docs/specs/<TASK_ID>-SPEC.md with user story, flow diagram, file manifest, env interface, and step logic.
metadata:
  version: "2.0"
  architecture: "Wizard-Executor-Separation"
---

# HLab Planner Skill

## Core Philosophy
You are designing for the **Horizon CLI Framework**, a modular Linux ops system.
**Rule #1**: Separation of Concerns.
- **Wizard (Brain)**: Pure interaction. Collects inputs. Generates a `.env` file. NEVER modifies the system.
- **Executor (Hand)**: Pure execution. Reads `.env` file. Idempotent. Logs to file. NEVER asks questions.

## Knowledge Base (Constraints)
1. **LOMP-Lite**: Target RAM < 1GB. Must enforce Swap checks, PHP concurrency limits, and log rotation.
2. **Directory Structure**:
   - `modules/<category>/wizards/`: Interactive scripts (e.g., `ask_db_pass.sh`).
   - `modules/<category>/executors/`: Action scripts (e.g., `install_mariadb.sh`).
   - `lib/`: Shared libraries (must be sourced via absolute path).
3. **Extension Points**: Design hooks for future "Pro/Private" modules (e.g., `hook_post_install_seo`).

## Output Format (The Spec)
Your output must be a `docs/specs/<TASK_ID>-SPEC.md` containing:
1. **User Story**: What are we building?
2. **Architecture**: Diagram of Wizard -> Config -> Executor flow.
3. **File Manifest**: List of files to create/modify.
4. **Env Interface**: Define the variables passed from Wizard to Executor (e.g., `DB_ROOT_PASS`, `ENABLE_FAIL2BAN`).
5. **Step-by-Step Logic**: Pseudo-code for complex logic.
