---
name: background-planning-implementation
description: Use this skill when you need to perform background planning and implementation tasks with multiple AI agents in parallel, ensuring context safety and efficient execution.
---

# Background Planning and Implementation Skill

## Purpose

This skill enables safe multi-LLM background planning and implementation. Multiple AI agents, such as **Claude, Codex, and Gemini**, can perform planning and implementation tasks in parallel based on provided documents, ensuring results are saved independently.

**Key Features:**
- **Multi-LLM Support**: Utilize various providers like Claude (Task), Codex CLI, Gemini API, and Ollama.
- **Context Safety**: Agents run with `run_in_background: true`, independent of the main session.
- **Automatic Saving**: Each agent saves results directly to designated output files.
- **Progress Tracking**: Monitor progress through file-based status tracking.
- **Task Extraction**: Automatically extract implementation tasks from planning documents.
- **Parallel Execution**: Execute independent tasks simultaneously.

## When to Invoke

Activate this skill when requests include keywords such as:
- "백그라운드 기획", "bg plan", "background plan"
- "백그라운드 구현", "bg impl", "parallel implement"
- "기획서 기반 구현", "PRD 구현"
- "여러 기능 동시 구현"
- "Codex로 구현", "Gemini로 구현"
- "멀티 AI 기획", "여러 LLM으로 구현"

**Examples:**
- "API 토큰 기능을 백그라운드로 기획해줘"
- "5개 기능을 병렬로 구현해주세요"
- "이 기획서들 기반으로 bg impl 해줘"
- "Codex로 백엔드, Claude로 프론트엔드 구현해줘"
- "여러 AI로 병렬 기획 (claude, codex, gemini)"

## Supported LLM Providers

### Provider Overview

| Provider | Execution Method | Strengths | Recommended Tasks |
|----------|------------------|-----------|-------------------|
| **Claude** | Task Tool | Complex logic, context retention | Business logic, API design |
| **Codex** | Bash (CLI) | Code generation, refactoring | Backend, DB migration |
| **Gemini** | Bash (API) | Long codebase understanding | Documentation, test generation |
| **Ollama** | Bash (CLI) | Local, free | Simple utilities, type definitions |

### Environment Variable Setup

```bash
# Codex CLI (OpenAI)
export OPENAI_API_KEY="sk-..."

# Gemini
export GOOGLE_API_KEY="..."

# Ollama (local, no API key needed)
ollama serve  # Start service
```

### CLI Installation

```bash
# Codex CLI
npm install -g @openai/codex

# Gemini CLI
pip install google-generativeai

# Ollama
brew install ollama
ollama pull codellama  # Code specialized model
```

## Instructions

### Overall Workflow

```
User Request (Planning documents)
    │
    ▼
┌─────────────────────────────────────────┐
│  1. Analyze planning documents           │
│     - Extract tasks for implementation   │
│     - Identify dependencies               │
│     - Identify parallelizable tasks       │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  2. Decompose tasks                      │
│     - Separate into independent units     │
│     - Assign planning context to each task│
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  3. Prepare output directory             │
│     - Create .context/impl/{timestamp}/ │
│     - Initialize status.json             │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  4. Execute background agents (parallel) │
│     - run_in_background: true            │
│     - Each agent writes code directly     │
│     - Save results upon completion        │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  5. Collect and integrate results        │
│     - List of changed files              │
│     - Summary of implementations          │
│     - Remaining TODOs                     │
└─────────────────────────────────────────┘
```

### Step 1: Analyze Planning Documents

Extract implementable tasks from the planning documents.

**Analysis Points:**
- DB migrations
- Rust models/structures
- API endpoints (handlers)
- Service logic
- Frontend components
- Type definitions

### Step 2: Decompose Tasks

Separate each feature into independent tasks.

**Example: API Token Feature**
```yaml
feature: api-tokens
tasks:
  - id: api-tokens-migration
    type: migration
    description: "Create api_tokens and api_token_usage_logs tables"
    files: ["migrations/xxx_api_tokens.sql"]
    depends_on: []

  - id: api-tokens-models
    type: model
    description: "ApiToken, TokenScopes structures"
    files: ["src/models/api_token.rs", "src/models/mod.rs"]
    depends_on: [api-tokens-migration]

  - id: api-tokens-handlers
    type: handler
    description: "Token CRUD API endpoints"
    files: ["src/handlers/tokens.rs", "src/handlers/mod.rs", "src/main.rs"]
    depends_on: [api-tokens-models]

  - id: api-tokens-frontend
    type: frontend
    description: "Token management UI component"
    files: ["src/pages/Settings/ApiTokens.tsx", "src/types/index.ts"]
    depends_on: []  # Can proceed independently
```

### Step 3: Prepare Output Directory

```bash
# Create directory
mkdir -p .context/impl/20260115_api-tokens

# Initialize status.json (multi-LLM included)
{
  "feature": "api-tokens",
  "started_at": "2026-01-15T01:00:00Z",
  "tasks": [
    {
      "id": "api-tokens-migration",
      "type": "migration",
      "provider": "codex",
      "status": "pending",
      "agent_id": null,
      "output_file": "01-migration-result.md",
      "files_changed": []
    },
    {
      "id": "api-tokens-models",
      "type": "model",
      "provider": "codex",
      "status": "pending",
      "agent_id": null,
      "output_file": "02-models-result.md",
      "files_changed": []
    },
    {
      "id": "api-tokens-handlers",
      "type": "handler",
      "provider": "claude",
      "status": "pending",
      "agent_id": null,
      "output_file": "03-handlers-result.md",
      "files_changed": []
    },
    {
      "id": "api-tokens-frontend",
      "type": "frontend",
      "provider": "claude",
      "status": "pending",
      "agent_id": null,
      "output_file": "04-frontend-result.md",
      "files_changed": []
    }
  ],
  "completed": 0,
  "total": 4
}
```

### Step 4: Execute Background Agents

Use appropriate execution methods for each provider.

---

#### Provider 1: Claude (Task Tool)

**Suitable for complex business logic and API implementation**

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `You are a senior developer responsible for implementing "${task_type}".

## Project Context
- Path: ${project_path}
- Language: Rust (backend), TypeScript/React (frontend)
- Planning Document: ${planning_doc_path}

## Implementation Task
${task_description}

## Files to Create
${files_to_create_or_modify}

## Instructions
1. Follow the schema/API design from the planning document accurately.
2. Create/modify actual files using Write/Edit tools.
3. Save results to ${output_file} upon completion.`,
  description: `${task_type} implementation (Claude)`,
  run_in_background: true
})
```

---

#### Provider 2: Codex CLI

**Suitable for DB migrations, model creation, and backend code**

```bash
# Execute implementation task with Codex CLI
codex --approval-mode full-auto \
  --quiet \
  "You are a senior developer. Please perform the following implementation task:

Project: ${PROJECT_PATH}
Task: ${TASK_DESCRIPTION}
Files: ${FILES_TO_CREATE}

Planning Document Content:
${PLANNING_CONTENT}

Instructions:
1. Create/modify the files.
2. Save the summary of results to ${OUTPUT_FILE}" \
  > /dev/null 2>&1 &
```

**Execute with Bash tool:**
```typescript
Bash({
  command: `cd ${project_path} && codex --approval-mode full-auto "${prompt}" 2>&1 | tee "${output_file}"`,
  run_in_background: true,
  description: `${task_type} implementation (Codex)`
})
```

---

#### Provider 3: Gemini API

**Suitable for test generation, documentation, and long codebase analysis**

```bash
# Generate tests with Gemini
gemini -m gemini-2.0-flash \
  "Please write unit tests for the following code:

${CODE_CONTENT}

Test File: ${TEST_FILE_PATH}" \
  > "${OUTPUT_FILE}" 2>&1 &
```

**Execute with Bash tool:**
```typescript
Bash({
  command: `gemini -m gemini-2.0-flash "${prompt}" > "${output_file}" 2>&1`,
  run_in_background: true,
  description: `${task_type} implementation (Gemini)`
})
```

---

#### Provider 4: Ollama (Local LLM)

**Suitable for type definitions, simple utilities, and sensitive code**

```bash
# Generate type definitions with Ollama
ollama run codellama \
  "Please generate TypeScript types for the following API response:

${API_RESPONSE_EXAMPLE}" \
  > "${OUTPUT_FILE}" 2>&1 &
```

**Execute with Bash tool:**
```typescript
Bash({
  command: `ollama run codellama "${prompt}" > "${output_file}" 2>&1`,
  run_in_background: true,
  description: `${task_type} implementation (Ollama)`
})
```

---

#### Multi-Provider Parallel Execution Example

**Identify optimal AI based on task type:**

```typescript
// Wave 1: Independent tasks (parallel)

// Codex - DB Migration (strong in code generation)
Bash({
  command: `codex --approval-mode full-auto "${migrationPrompt}" 2>&1`,
  run_in_background: true,
  description: "DB Migration (Codex)"
})

// Claude - Frontend Component (complex logic)
Task({
  subagent_type: "general-purpose",
  prompt: frontendPrompt,
  description: "Frontend UI (Claude)",
  run_in_background: true
})

// Ollama - Type Definitions (simple task, free)
Bash({
  command: `ollama run codellama "${typesPrompt}" > types.ts`,
  run_in_background: true,
  description: "TypeScript Types (Ollama)"
})

// Wave 2: Dependent tasks (after Wave 1 completion)

// Codex - Rust Models (after migration)
// Claude - API Handlers (after models)
```

### Step 5: Collect and Integrate Results

Upon completion of all agents, generate a consolidated result:

```markdown
# Implementation Results: {feature_name}

## Completed Tasks

### 1. DB Migration
- File: migrations/xxx_api_tokens.sql
- Status: ✅ Completed

### 2. Rust Models
- File: src/models/api_token.rs
- Status: ✅ Completed

### 3. API Handlers
- File: src/handlers/tokens.rs
- Status: ✅ Completed

### 4. Frontend
- File: src/pages/Settings/ApiTokens.tsx
- Status: ✅ Completed

## Changed Files List
- migrations/xxx_api_tokens.sql (new)
- src/models/api_token.rs (new)
- src/models/mod.rs (modified)
- src/handlers/tokens.rs (new)
- src/handlers/mod.rs (modified)
- src/main.rs (modified)
- src/pages/Settings/ApiTokens.tsx (new)
- src/types/index.ts (modified)

## Next Steps
1. Run `cargo check` to verify compilation.
2. Apply DB migration.
3. Write tests.
4. Conduct frontend integration tests.
```

## Parallel Execution Strategy

### Wave-based Execution

Execute tasks in waves based on dependencies:

```
Wave 1 (no dependencies, parallel):
├── DB Migration (all features)
└── Frontend Types (all features)

Wave 2 (after Migration, parallel):
├── Rust Models (all features)
└── Frontend Components (all features)

Wave 3 (after Models, parallel):
└── API Handlers (all features)

Wave 4 (integration):
└── Update main.rs routing
```

### Identify Concurrently Executable Tasks

| Task Type | Parallelizable | Reason |
|-----------|----------------|--------|
| DB Migration (different features) | ✅ | Independent tables |
| Same feature Model → Handler | ❌ | Sequential dependency |
| Different feature Handlers | ✅ | Independent modules |
| Frontend (different features) | ✅ | Independent components |
| Same file modification | ❌ | Potential conflicts |

## Examples

### Example 1: Single Feature Implementation (Claude Only)

**User**: "Implement API token feature in the background"

**Actions:**

1. Analyze planning document: `07-api-tokens-backend.md`

2. Decompose tasks:
   - Migration (independent)
   - Models (after Migration)
   - Handlers (after Models)
   - Frontend (independent)

3. Execute Wave 1: Migration + Frontend (parallel)

4. Execute Wave 2: Models

5. Execute Wave 3: Handlers

6. Collect results

### Example 2: Multi-LLM Implementation

**User**: "Implement backend with Codex, frontend with Claude"

**Actions:**

1. Assign tasks by provider:
   ```
   Codex:
   ├── DB Migration (strong in SQL generation)
   ├── Rust Models (type system)
   └── API Handlers (code generation)

   Claude:
   ├── Frontend Components (complex logic)
   └── State Management (business logic)
   ```

2. Initialize status.json:
   ```json
   {
     "tasks": [
       {"id": "migration", "provider": "codex", "status": "pending"},
       {"id": "models", "provider": "codex", "status": "pending"},
       {"id": "handlers", "provider": "codex", "status": "pending"},
       {"id": "frontend", "provider": "claude", "status": "pending"}
     ]
   }
   ```

3. Execute in parallel:
   ```
   Bash (Codex) ─── Migration ──┐
   Task (Claude) ── Frontend ───┼── Wave 1 parallel
   ```

4. Collect and integrate results

### Example 3: Multiple Features Multi-LLM Implementation

**User**: "Implement 5 features with Codex, Claude, and Ollama"

**Actions:**

1. Map tasks by provider:
   ```
   Feature          | Migration  | Models   | Handlers | Frontend | Types
   ─────────────────|------------|----------|----------|----------|-------
   API Tokens       | Codex      | Codex    | Claude   | Claude   | Ollama
   Custom Status    | Codex      | Codex    | Claude   | Claude   | Ollama
   Webhooks         | Codex      | Codex    | Claude   | Claude   | Ollama
   Automations      | Codex      | Codex    | Claude   | Claude   | Ollama
   Filters Ext      | Codex      | Codex    | Claude   | Claude   | Ollama
   ```

2. Execute waves (mixed providers):
   ```
   Wave 1 (independent