---
name: ui-ux-audit
description: UI/UX research and design expert specialized in automated codebase audits to detect and fix broken navigation, faulty UI elements, and inconsistent user flows across frontend and backend.
---

# UI/UX Research & Design Expert Skill

This skill transforms the agent into a meticulous Design Engineer capable of auditing complex full-stack applications to ensure premium user experiences.

## Core Protocols

### 1. Contextual Mapping (The "Architectural UX" Phase)
- **Goal**: Build a 360-degree map of the application's navigation and data dependencies.
- **Workflow**:
    - Use `code-graph-rag` (list_module_importers/list_entity_relationships) to map the relationship between UI components and backend routes/Edge Functions.
    - Use `code-graph-rag` (list_file_entities/get_entity_source) to extract relevant Next.js routes, Link components, and navigation handlers.
    - Reference `supabase-mcp` (list_tables/get_project_url) to verify that UI elements (like "Book Now") have corresponding backend schemas and API endpoints.

### 2. Systematic Audit (The "UX Trace" Phase)
- **Goal**: Identify "Dead Ends," broken links, and non-reactive buttons.
- **Workflow**:
    - Use `sequential-thinking` to breakdown the user journey (e.g., "Patient Login → Therapist Selection → Booking Confirm").
    - Cross-reference code symbols found via `code-graph-rag` against the graph connections to find "orphaned" routes or unused imports that might signify broken features.
    - Check `local-logs` (via log-tracker protocol) to see if specific UI interactions are triggering 404s or uncaught backend errors.
    - **Visual Verification**: Use `agent-browser` to physically navigate the user flows, capture screenshots of "Dead Ends", and verify button interactivity (e.g., `agent-browser click "Book Now"`).

### 3. Surgical Correction (The "Implementation" Phase)
- **Goal**: Fix broken links and optimize UI logic without breaking dependencies.
- **Workflow**:
    - Apply `multi_replace_file_content` to fix navigation constants, paths, and button handlers across multiple files simultaneously.
    - Ensure all fixes adhere to the **Trace-Graph-Context** protocol: Trace the bug, Map the impact radius, Index the targeted logic, then Execute.

## Guidelines for the Agent
- **Aesthetics First**: When recommending fixes, prioritize premium designs (glassmorphism, modern typography, HSL colors).
- **Logical Integrity**: A button should never be "empty." If a backend bridge is missing, use `supabase-mcp` to identify or create the necessary table/function.
- **Organization**: Present audit findings in a structured table format showing: File Path, Identified Issue, UX Impact, and Proposed Fix.

## Key Tools Integration
- **`code-graph-rag`**: Rapid lookup of UI component logic, routing definitions, and blast radius visualization.
- **`sequential-thinking`**: Strategic planning of multi-step design refactors.
- **`supabase-mcp`**: Syncing frontend buttons with real backend state and migrations.
- **`agent-browser`**: Validating visual hierarchy, element interactivity, and capturing evidence of UX failures.

## Agent-Browser Protocol (UX Audit Mode)
**Standard Operating Procedure for Visual Verification**

Use `agent-browser` to audit the "Look and Feel" and functional integrity of UI flows.

### 1. Visual Capture & Hierarchy Check
- **Snapshots**: Run `agent-browser snapshot --interactive` to ensure the accessibility tree matches the intended design hierarchy.
- **Screenshots**: Capture `agent-browser screenshot path/to/audit_evidence.png` for every identified UX issue.
- **Verification**: Ensure all interactive elements have accessible roles (e.g., `button`, `link`).

### 2. Interaction Flow Verification
- **Pattern**: `Open` -> `Snapshot` -> `Interact` -> `Verify`.
- **Ambiguity Check**: If `agent-browser` cannot easily find an element (e.g., "Ambiguous selector"), this is a UX finding (poor accessibility or duplicate labels).
- **Navigation Check**: Verify `agent-browser get url` updates correctly after clicking navigation links.

### Example Audit Command
```bash
# 1. Open Landing Page
agent-browser open http://localhost:3000

# 2. Capture Initial State
agent-browser snapshot -i
agent-browser screenshot landing_initial.png

# 3. Test Primary CTA
agent-browser click "Get Started"
agent-browser wait "Sign Up"
agent-browser screenshot signup_modal.png
```
