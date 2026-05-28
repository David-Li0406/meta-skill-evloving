---
name: background-executor
description: Use this skill when you need to perform planning or implementation tasks in the background using multiple AI agents, ensuring context safety and parallel execution.
---

# Background Executor Skill

## Purpose

This skill allows for context-safe background execution of planning or implementation tasks using multiple AI agents such as Claude, Codex, and Gemini. It enables parallel processing of tasks while automatically saving results, ensuring that the main session can be safely terminated without losing progress.

**Key Features:**
- **Multi-LLM Support**: Utilizes various providers like Claude (Task), Codex (CLI), Gemini (API), and Ollama.
- **Context Safety**: Agents run with `run_in_background: true`, independent of the main session.
- **Automatic Saving**: Results are saved in a designated folder upon completion.
- **Progress Tracking**: File-based tracking of task progress.
- **Task Analysis**: Compare outputs from different AI perspectives.
- **Automatic Merging**: Consolidates results from all agents into a unified output.

## When to Invoke

Activate this skill with requests containing:
- "백그라운드 기획", "bg plan", "background plan"
- "백그라운드 구현", "bg impl", "background implement"
- "병렬 기획", "parallel plan"
- "병렬 구현", "parallel implement"
- "여러 AI로 기획", "여러 AI로 구현"
- "Codex로 기획", "Codex로 구현", "Gemini로 기획", "Gemini로 구현"

**Examples:**
- "이슈 템플릿 기능을 백그라운드로 기획해줘"
- "API 토큰 기능을 백그라운드로 구현해줘"
- "3가지 관점에서 병렬로 기획해주세요"
- "5개 기능을 병렬로 구현해주세요"
- "Codex, gemini로 다각도 기획해줘"

## Supported LLM Providers

### Provider Overview

| Provider  | Execution Method | Strengths | Recommended Use |
|-----------|------------------|-----------|------------------|
| **Claude** | Task tool        | Stable, context retention | Complex analysis, business logic |
| **Codex**  | Bash (CLI)       | Fast code generation | Backend, API design |
| **Gemini** | Bash (API)       | Long context handling | Documentation, creative tasks |
| **Ollama** | Bash (CLI)       | Local, free, privacy-focused | Simple utilities, type definitions |

### Environment Variable Setup

```bash
# Codex CLI (OpenAI)
export OPENAI_API_KEY="sk-..."

# Gemini
export GOOGLE_API_KEY="..."

# Ollama (local, no API key needed)
# Default URL: http://localhost:11434
```

### CLI Installation

```bash
# Codex CLI installation (npm)
npm install -g @openai/codex

# Gemini CLI installation (pip)
pip install google-generativeai

# Ollama installation (macOS)
brew install ollama
ollama serve
ollama pull llama3.2
```

## Instructions

### Overall Workflow

```
User Request
    │
    ▼
┌─────────────────────────────────────────┐
│  1. Task Parsing                        │
│     - Extract topic and perspectives    │
│     - Determine number of agents        │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  2. Prepare Output Directory            │
│     - Create .context/plans/{timestamp}/│
│     - Initialize status.json            │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  3. Execute Tasks in Parallel           │
│     - Assign tasks to agents            │
│     - Monitor progress                   │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  4. Save Results                        │
│     - Store outputs in designated folder│
│     - Merge results if applicable       │
└─────────────────────────────────────────┘
```