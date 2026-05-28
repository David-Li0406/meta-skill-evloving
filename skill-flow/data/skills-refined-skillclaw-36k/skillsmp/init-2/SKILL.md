---
name: init
description: Initialize project with AG4ONE system, detecting existing vs blank projects
allowed-tools: ["read", "write", "edit", "glob", "bash", "serena_list_dir", "serena_find_file", "serena_check_onboarding_performed", "serena_onboarding"]
---

# Project Initialization

## Objective
Initialize the current project with the AG4ONE system, detecting whether it's an existing project or blank project and configuring the appropriate structure.

## Process

### 1. Check Current Project State
Analyze the current directory to determine project type:
- Check for package.json, requirements.txt, Cargo.toml, go.mod, etc.
- Look for source code directories (src/, lib/, app/, etc.)
- Identify existing configuration files
- Determine if this is a blank/new project

### 2. Check AG4ONE Installation Status
Verify AG4ONE components are available:
- Check if .ag4one directory exists and has required structure
- Verify .serena directory exists
- Validate agents, commands, scripts, skills are present
- Check if onboarding has been performed

### 3. For Existing Projects
If project has existing code/config:
- Preserve existing structure and files
- Integrate AG4ONE components without disruption
- Set up project-specific AGENTS.md with existing tech stack
- Configure Serena tools to work with existing codebase
- Create integration plan for existing workflows

### 4. For Blank Projects
If project is new/empty:
- Set up basic project structure with AG4ONE
- Initialize with standard development patterns
- Create blank AGENTS.md template
- Set up Serena for new development
- Provide project scaffolding options

### 5. Configure Serena Integration
- Activate appropriate Serena project context
- Set up file indexing for the project type
- Configure search patterns and tools
- Initialize Serena memory if needed

### 6. Create Project Configuration
Generate project-specific configuration:
- Create STATE.md with project context
- Set up AG4-STYLE.md if needed
- Initialize AGENTS.md with project details
- Configure tools and workflows for project type

### 7. Provide Next Steps
Guide user to appropriate AG4ONE commands:
- For existing projects: `/ag4:map-codebase`, `/ag4:plan-milestone-gaps`
- For blank projects: `/ag4:new-project`, `/ag4:define-requirements`
- Both: `/ag4:help` for available commands

## Completion Criteria
- Project is properly initialized with AG4ONE system
- AG4ONE directory structure is in place
- Serena integration is configured
- User has clear guidance on next steps
- Project type (existing vs blank) is correctly identified and handled