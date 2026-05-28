---
name: agent-ops-migrate
description: Use this skill when you need to migrate a project into another, ensuring functionality and validating complete content transfer, such as during monorepo consolidation, template upgrades, or codebase mergers.
---

# Project Migration Workflow

## Purpose

Migrate code, configuration, and content from a source project into a target project while:

- Ensuring the target project works after migration
- Validating all content has been transferred
- Handling conflicts and incompatibilities
- Providing rollback capability if issues arise

## When to Use

- Consolidating multiple projects into a monorepo
- Upgrading from an old project template to a new one
- Merging two codebases
- Moving functionality between projects
- Adopting a new framework while preserving logic

## Migration Types

| Type | Description | Complexity |
|------|-------------|------------|
| **Full merge** | Entire source → target | High |
| **Selective** | Specific modules/features only | Medium |
| **Template upgrade** | Apply new template, preserve custom code | Medium |
| **Framework migration** | Change underlying framework | High |
| **Monorepo consolidation** | Multiple repos → single repo | High |

## Procedure

### Phase 1: Pre-Migration Analysis

1. **Scan source project** using `agent-ops-project-sections`:
   - Identify all sections and their dependencies
   - Map file structure
   - Identify configuration files
   - Note external dependencies

2. **Scan target project** (if exists):
   - Identify existing structure
   - Note potential conflicts
   - Check compatibility

3. **Create migration manifest**:
   ```yaml
   migration:
     source: /path/to/source
     target: /path/to/target
     type: full_merge | selective | template_upgrade
     
   sections:
     - name: api
       source_path: src/api/
       target_path: src/api/
       action: copy | merge | skip
       
     - name: config
       source_path: config/
       target_path: config/
       action: merge
       conflicts: [.env, settings.py]
   ```

### Phase 2: Dependency Analysis

1. **Compare dependency files**:
   - `package.json` vs `package.json`
   - `pyproject.toml` vs `pyproject.toml`
   - `*.csproj` vs `*.csproj`

2. **Identify conflicts**:
   - Version mismatches
   - Incompatible packages
   - Missing dependencies

3. **Resolve conflicts**:
   - Update versions
   - Replace incompatible packages
   - Add missing dependencies

### Phase 3: Migration Execution

1. **Execute migration** based on the manifest:
   - Copy or merge files as specified
   - Apply configuration changes
   - Update dependencies

2. **Run tests** to ensure functionality:
   - Execute unit tests
   - Perform integration tests
   - Validate user acceptance

3. **Rollback if necessary**:
   - Use backup or version control to revert changes if issues arise.

### Phase 4: Post-Migration Validation

1. **Validate content transfer**:
   - Ensure all files are present
   - Check for data integrity

2. **Document changes**:
   - Update project documentation
   - Note any changes in functionality or structure