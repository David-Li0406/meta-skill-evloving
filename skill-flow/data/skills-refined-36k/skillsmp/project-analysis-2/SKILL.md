---
name: project-analysis
description: Analyze project structure, complexity, and health metrics
author: StrRay Framework
version: 1.0.0
tags: [analysis, project, complexity, health]

mcp:
  project-analysis:
    command: node
    args: [node_modules/strray-ai/dist/plugin/mcps/knowledge-skills/project-analysis.server.js]
---

# Project Analysis Skill

Provides comprehensive project analysis capabilities including:

## Tools Available

- **analyze_project_structure**: Analyze complete project structure including file organization, directory hierarchy, and module distribution
- **assess_project_complexity**: Assess overall project complexity including code metrics, maintainability, and technical debt indicators
- **identify_project_patterns**: Identify architectural patterns, code patterns, and structural patterns in the project
- **analyze_project_health**: Provide comprehensive project health assessment including quality metrics and improvement recommendations

## Usage

This skill analyzes your project's codebase to provide insights about:
- Code organization and structure
- Complexity metrics and maintainability
- Architectural patterns and anti-patterns
- Health indicators and improvement recommendations

## Integration

Activated automatically when project analysis is requested through the skills system.