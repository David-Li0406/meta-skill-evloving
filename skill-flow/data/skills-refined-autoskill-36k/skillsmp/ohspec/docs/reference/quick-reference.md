# Quick Reference

## First Time Setup

```bash
# 初始化权限配置（首次使用必须）
/ohspec:init
```

或手动创建 `.claude/settings.json`：
```json
{
  "permissions": {
    "allow": ["Read(*)", "Write(*.md)", "Write(*.json)", "Glob(*)", "Grep(*)"],
    "deny": ["Bash(rm:*)", "Write(/tmp/*)"]
  }
}
```

---

## Core Pattern

### Orchestration Mode
```
User Requirement → Dispatcher Analysis → Assess Complexity → Select Experts → Coordinate Execution → Output RFC
```

### Complexity Levels

| Level | Characteristics | Execution Mode |
|-------|----------------|----------------|
| SIMPLE | Single file, single interface, clear intent | Fast track (analyze+design merged) |
| MEDIUM | Multiple files, single subsystem | Standard flow (analyze→design→audit) |
| COMPLEX | Cross-subsystem, architecture-level changes | Full flow + user confirmation per phase |

### Expert Combination

**Core Experts** (always loaded):
- **Dispatcher**: Analyze requirements, assess complexity, coordinate workflow
- **Requirements Analyst**: Understand requirements, clarify ambiguities, output RFC §1-§2
- **Solution Architect**: Design contracts, define interfaces, output RFC §3-§5
- **Quality Auditor**: DFX checks, quality gates, comprehensive scoring

**Extension Experts** (loaded on-demand):
- **Diplomat**: Cross-subsystem dependency coordination
- **API Designer**: Developer-friendly API design
- **Prototyper**: Spike validation for feasibility

## Basic Usage

```bash
# Unified entry point (recommended)
/ohspec "Add 3D sound effect toggle to audio service"

# Fast track (simple requirements)
/ohspec --mode=fast "Simple configuration item modification"
```

## Workflow

1. **Requirements Analysis** (analyze): Understand requirements, clarify ambiguities, output RFC §1-§2
2. **Feasibility Validation** (spike, optional): Technical probe validation
3. **Solution Design** (design): Design contracts, define interfaces, output RFC §3-§5
4. **Automatic Precheck** (precheck): Structure completeness, scenario coverage, DFX checklist
5. **Quality Audit** (audit): Manual review, comprehensive scoring, decision

## Deliverables

- `{RFC_DIR}/rfc.md` - Complete RFC document (5 sections)
- `{RFC_DIR}/findings.json` - Code scan findings and decision records
- `{RFC_DIR}/progress.json` - Execution process and status tracking

---

## Commands

| 命令 | 说明 |
|------|------|
| `/ohspec:init` | 初始化权限配置（首次使用） |
| `/ohspec "需求"` | 启动 RFC 生成流程 |
| `/ohspec --model=high "需求"` | 使用最高质量模型 |
| `/ohspec --model=fast "需求"` | 使用最快模型 |
| `/ohspec:list` | 列出所有 RFC |
| `/ohspec:resume RFC-ID` | 恢复指定 RFC |

---

## Model Selection

| 策略 | 命令参数 | 说明 |
|------|----------|------|
| **auto** (默认) | 无 | 按复杂度自动选择 |
| **high_quality** | `--model=high` | 全部使用 sonnet |
| **fast** | `--model=fast` | 全部使用 haiku |

**默认模型分配**:
| 阶段 | SIMPLE | MEDIUM | COMPLEX |
|------|--------|--------|---------|
| Dispatcher | sonnet | sonnet | sonnet |
| Analyze | haiku | sonnet | sonnet |
| Design | haiku | sonnet | sonnet |
| Audit | sonnet | sonnet | sonnet |

---

## User Confirmation Points

| 复杂度 | 确认次数 | 确认点 |
|--------|----------|--------|
| SIMPLE | 1 | 最终审批 |
| MEDIUM | 2 | 设计确认 + 最终审批 |
| COMPLEX | 4 | 每阶段确认 |
