---
name: session-retrospective
description: "Claude Codeのセッションを分析し、設定改善案（permissions/memory/rules/skills/agents/hooks）を提案する。完了セッションの振り返り時に使用する。トリガー例: retrospective / session analysis / improve Claude config / セッションID指定。"
---

# Session Retrospective

Claude Codeのセッションログを分析し、設定改善案を提案する。

## 入力

- **Session ID**: 引数で渡される（例: `/session-retrospective abc-123-def`）
- **Session File**: `~/.claude/projects/*/<SESSION_ID>.jsonl`
- **Debug Log**: `~/.claude/debug/<SESSION_ID>.txt`（任意）

## セッションログ形式

JSONL with records like:
```json
{"type": "user", "message": {"role": "user", "content": "..."}}
{"type": "assistant", "message": {"role": "assistant", "content": [{"type": "tool_use", "name": "...", "input": {...}}]}}
```

## 分析手順

### 1. セッションファイルを読む

```bash
# セッションファイルを探す
find ~/.claude/projects -name "<SESSION_ID>.jsonl" 2>/dev/null

# セッションログを読む
cat <SESSION_FILE>

# デバッグログがあれば読む
cat ~/.claude/debug/<SESSION_ID>.txt 2>/dev/null
```

### 2. 分析して改善案を出す

#### Permissions（`settings.json`）
- Look for `Permission suggestions for` in debug log
- Identify commands that required manual approval
- Suggest `permissions.allow` rules

#### Memory / Rules（`CLAUDE.md`, `.claude/rules/`）
- Find repeated explanations from user
- Find `AskUserQuestion` tool calls with similar questions
- Suggest content for CLAUDE.md or path-specific rules

#### Skills（`.claude/skills/<name>/SKILL.md`）
- Identify repeated multi-step workflows
- Find manual instructions given multiple times
- Suggest skill definitions with frontmatter

#### Agents（`.claude/agents/<name>.md`）
- Find repeated `Task` tool delegations with same patterns
- Identify common subagent_type + description combinations
- Suggest custom agent definitions

#### Hooks（`settings.json`）
- Find repeated pre/post processing steps
- Identify manual formatting or validation tasks
- Suggest hook configurations

### 3. レポートを作成する

Save to `~/.claude/retrospectives/<SESSION_ID>.md`:

```markdown
# Session Retrospective: <SESSION_ID>

**Date**: YYYY-MM-DD
**Project**: /path/to/project

## Session Summary
[What was accomplished]

## What Went Well
- [Successes]

## Suggested Improvements

### 1. Permissions
```json
{"permissions": {"allow": ["Bash(command:*)"]}}
```
**Reason**: [Why this helps]

### 2. Memory / Rules
```markdown
# Content to add
```
**Reason**: [Why this helps]

### 3. Skills
```yaml
---
name: skill-name
description: ...
---
```
**Reason**: [Why this helps]

### 4. Agents
```yaml
---
name: agent-name
tools: Read, Grep
---
```
**Reason**: [Why this helps]

### 5. Hooks
```json
{"hooks": {...}}
```
**Reason**: [Why this helps]

## Action Items
- [ ] Specific action 1
- [ ] Specific action 2
```

## 参照ドキュメント

- Memory: https://code.claude.com/docs/en/memory
- Skills: https://code.claude.com/docs/en/skills
- Slash Commands: https://code.claude.com/docs/en/slash-commands
- Sub-agents: https://code.claude.com/docs/en/sub-agents
- Hooks: https://code.claude.com/docs/en/hooks-guide
