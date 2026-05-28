---
name: Generate RFC
description: Instructions for generating detailed RFC documentation in Chinese with Mermaid diagrams
---

# Generate RFC Skill

Use this skill when the user asks to create an RFC (Request for Comments) or when documenting a significant bug fix or feature implementation.

## Rules

1.  **Language**: The RFC MUST be written in **Chinese** (Simplified).
2.  **Visuals**: You MUST include at least one **Mermaid diagram** (flowchart, sequence diagram, etc.) to explain the logic or architecture.
3.  **Mermaid Syntax**:
    -   **ALWAYS quote node labels** if they contain special characters, emojis, HTML tags `<br/>`, or spaces.
        -   ✅ `A["用户点击 (User Click)"]`
        -   ❌ `A[用户点击 (User Click)]`
    -   **Dark Mode Compatibility**: Do NOT use hardcoded colors (like `#ffcccc`). Use `classDef` with high-contrast, theme-neutral colors.
        -   ✅ `classDef error fill:#f9f2f4,stroke:#c00,stroke-width:2px,color:#c00`
        -   ❌ `style A fill:#ffcccc`
4.  **Content Structure**:
    -   **Problem Statement (问题陈述)**: Describe the observed behavior and root cause.
    -   **Investigation (调查流程)**: How the issue was found (use Mermaid flowchart).
    -   **Solution (解决方案)**: Detailed code changes and Logic flow (use Mermaid).
    -   **Technical Details (技术细节)**: Tables, comparisons, sequence diagrams.
    -   **Verification (验证)**: Test cases and results.

## Template

```markdown
# RFC {Number}: {Title in Chinese}

- **状态**: {Status}
- **创建时间**: {Date}
- **作者**: AI Assistant
- **相关问题**: {Related Issue}

## 概述
{Brief summary in Chinese}

## 问题陈述
### 观察到的行为
### 根本原因
{Explain root cause clearly}

## 调查流程
{Mermaid flowchart showing investigation steps}

## 解决方案
### 代码更改
### 修复流程
{Mermaid flowchart showing the fix logic}

## 技术细节
### {Specific Detail}
{Tables or Sequence Diagrams}

## 验证
### 测试用例
| 场景 | 预期行为 | 状态 |
|-----|---------|------|
| ... | ... | ... |
```
