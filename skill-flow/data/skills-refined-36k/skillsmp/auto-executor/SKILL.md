---
name: auto-executor
description: Task tool 강제 사용 자동화 엔진
version: 2.0.0

triggers:
  keywords:
    - "auto"
    - "자동 실행"
    - "서브 에이전트"
    - "작업 위임"
  file_patterns:
    - "**/*.py"
    - "**/*.ts"
    - "**/*.tsx"
    - "**/*.js"
  context:
    - "자동화 작업"
    - "서브에이전트 위임"

capabilities:
  - task_delegation
  - agent_selection
  - session_management

model_preference: opus
auto_trigger: false
token_budget: 2000
---

# auto-executor 스킬

Task tool을 **반드시** 사용하여 서브에이전트에 작업을 위임하는 자동화 엔진입니다.

## 핵심 원칙

- **모든 작업은 서브에이전트가 처리**
- Python 스크립트가 Claude CLI 호출 시 Task tool 사용 강제
- 메인 에이전트는 조정만, 실제 작업은 서브에이전트

## 사용법

```bash
# /auto 커맨드에서 자동 호출
/auto

# 직접 스크립트 실행
python .claude/skills/auto-executor/scripts/auto_executor.py
python .claude/skills/auto-executor/scripts/auto_executor.py --task "API 분석"
python .claude/skills/auto-executor/scripts/auto_executor.py --status
python .claude/skills/auto-executor/scripts/auto_executor.py --stop
```

## 스크립트 구조

```
scripts/
├── auto_executor.py      # 메인 실행 스크립트 (CLI 진입점)
├── task_runner.py        # Task tool 강제 호출 로직
├── session_manager.py    # 세션 YAML 관리
└── agent_selector.py     # 에이전트 자동 선택
```

## Task tool 강제 메커니즘

```python
# task_runner.py에서 Claude CLI 호출 시
prompt = f"""
**중요: 반드시 Task tool을 사용하세요. 직접 처리 금지.**

다음 작업을 Task tool로 서브에이전트에 위임하세요:
- 작업: {task_description}
- 에이전트: {agent_type}

Task tool 호출 형식:
Task(
    subagent_type="{agent_type}",
    prompt="...",
    description="..."
)

**직접 처리하면 실패로 간주됩니다.**
"""

subprocess.run(["claude", "-p", prompt])
```
