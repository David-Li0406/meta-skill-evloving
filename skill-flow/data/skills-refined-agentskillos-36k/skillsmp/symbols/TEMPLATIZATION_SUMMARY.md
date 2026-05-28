# Symbols Skill Templatization Summary

## Overview

Successfully templatized the symbols skill files to make them reusable across different projects by replacing MeatyPrompts-specific references with `{{VARIABLE}}` placeholders.

## Files Modified

### 1. SKILL.md
**Location**: `claude-export/skills/symbols/SKILL.md`

**Changes Made**:
- Added template variable documentation header listing all variables used
- Replaced project-specific paths with `{{PROJECT_PATHS.*}}` variables
- Replaced symbol file references with `{{SYMBOL_FILES.*}}` variables
- Replaced architecture references with `{{PROJECT_ARCHITECTURE}}` and `{{LAYER_ARCHITECTURE}}`
- Replaced component/service examples with `{{PROJECT_EXAMPLES.*}}` variables
- Replaced project name "MeatyPrompts" with `{{PROJECT_NAME}}`
- Updated all code examples to use template variables
- Made layer descriptions generic with architecture-specific notes

**Variable Categories Used**:
- `{{PROJECT_NAME}}` - Project name throughout documentation
- `{{PROJECT_PATHS.web}}` - Web app directory path
- `{{PROJECT_PATHS.api}}` - Backend API directory path
- `{{PROJECT_PATHS.ui}}` - UI package directory path
- `{{PROJECT_PATHS.symbolsDir}}` - Symbol files directory
- `{{SYMBOL_FILES.api}}` - API symbol file location
- `{{SYMBOL_FILES.web}}` - Web symbol file location
- `{{PROJECT_ARCHITECTURE}}` - Architecture pattern description
- `{{LAYER_ARCHITECTURE}}` - Detailed layer breakdown
- `{{PROJECT_EXAMPLES.component}}` - Example component name
- `{{PROJECT_EXAMPLES.service}}` - Example service name

**Preserved Generic Content**:
- Symbol system concepts and capabilities
- Tool names and function signatures
- Symbol generation workflow and lifecycle
- Query patterns and API reference
- Token efficiency guidelines
- Progressive loading strategy

### 2. symbols.config.json
**Location**: `claude-export/skills/symbols/symbols.config.json`

**Changes Made**:
- Replaced `"projectName": "MeatyPrompts"` with `"projectName": "{{PROJECT_NAME}}"`
- Replaced `"symbolsDir": "ai"` with `"symbolsDir": "{{PROJECT_PATHS.symbolsDir}}"`
- Updated domain descriptions to use framework/architecture variables
- Replaced directory paths in extraction config with `{{PROJECT_PATHS.*}}` variables
- Updated layer descriptions to reference configuration variables
- Added comprehensive `_template_notes` section with:
  - Variable replacement instructions
  - List of required variables with descriptions
  - Step-by-step customization guide
  - Reference to template-config.json

**Variable Categories Used**:
- `{{PROJECT_NAME}}` - Project name in metadata
- `{{PROJECT_PATHS.symbolsDir}}` - Symbol files directory (e.g., "ai")
- `{{PROJECT_PATHS.api}}` - Backend API path (e.g., "services/api")
- `{{PROJECT_PATHS.web}}` - Web app path (e.g., "apps/web")
- `{{PROJECT_PATHS.mobile}}` - Mobile app path (e.g., "apps/mobile")
- `{{PROJECT_PATHS.ui}}` - UI package path (e.g., "packages/ui")
- `{{PROJECT_PATHS.tokens}}` - Tokens package path (e.g., "packages/tokens")
- `{{FRONTEND_FRAMEWORK}}` - Frontend framework name (e.g., "Next.js")
- `{{BACKEND_FRAMEWORK}}` - Backend framework name (e.g., "FastAPI")
- `{{DATABASE}}` - Database and ORM (e.g., "PostgreSQL with SQLAlchemy")
- `{{PROJECT_ARCHITECTURE}}` - Architecture description
- `{{LAYER_ARCHITECTURE}}` - Layer breakdown

**Preserved Configuration**:
- JSON schema reference
- Domain structure pattern
- API layers structure pattern
- File extensions and exclude patterns
- Test file separation logic
- Metadata structure

## Templatization Approach

### What Was Replaced

**Project-Specific Values**:
- "MeatyPrompts" → `{{PROJECT_NAME}}`
- "services/api" → `{{PROJECT_PATHS.api}}`
- "apps/web" → `{{PROJECT_PATHS.web}}`
- "ai/symbols-api.json" → `{{SYMBOL_FILES.api}}`
- "Button", "PromptCard" → `{{PROJECT_EXAMPLES.component}}`
- "FastAPI" → `{{BACKEND_FRAMEWORK}}`
- "Next.js" → `{{FRONTEND_FRAMEWORK}}`

**Architecture-Specific Patterns**:
- Router → Service → Repository → DB → `{{PROJECT_ARCHITECTURE}}`
- Layer descriptions → Based on `{{LAYER_ARCHITECTURE}}`
- Example layer names → "or equivalent in your architecture"

**Path References**:
- Hardcoded paths → `{{PROJECT_PATHS.*}}`
- Symbol file paths → `{{SYMBOL_FILES.*}}`
- Directory structures → Configurable via template variables

### What Was NOT Replaced

**Generic Concepts**:
- Symbol system methodology
- Token efficiency principles
- Query function signatures
- Tool names (query_symbols, load_domain, etc.)
- Symbol kinds (component, hook, function, etc.)
- Progressive loading strategy

**Technical Implementation**:
- Script names (extract_symbols_typescript.py, etc.)
- Function names and APIs
- Symbol structure schema
- JSON configuration patterns
- Layer tagging methodology

**Documentation Structure**:
- Section organization
- Capability descriptions
- Usage patterns
- Best practices
- Troubleshooting guidance

## Usage Instructions

### For New Projects

1. **Copy the templatized files** to your project:
   ```bash
   cp claude-export/skills/symbols/SKILL.md .claude/skills/symbols/SKILL.md
   cp claude-export/skills/symbols/symbols.config.json .claude/skills/symbols/symbols.config.json
   ```

2. **Replace template variables** in both files:
   - Use find & replace: `{{PROJECT_NAME}}` → "YourProject"
   - Use find & replace: `{{PROJECT_PATHS.api}}` → "backend"
   - Continue for all required variables

3. **Customize symbols.config.json**:
   - Update `domains` section to match your project structure
   - Configure `apiLayers` to match your backend architecture
   - Update `extraction.python.directories` with your backend paths
   - Update `extraction.typescript.directories` with your frontend paths
   - Remove `_template_notes` section after customization

4. **Update SKILL.md examples**:
   - Replace `{{PROJECT_EXAMPLES.*}}` with real component/service names
   - Verify all paths and references are correct
   - Update layer descriptions to match your architecture

5. **Test the configuration**:
   ```bash
   # Test symbol extraction
   python .claude/skills/symbols/scripts/extract_symbols_typescript.py <your_web_path>

   # Verify symbol queries work
   /symbols:query --name="YourComponent"
   ```

### Variable Reference

See `claude-export/config/template-config.json` for complete variable documentation including:
- Required vs. optional variables
- Data types and examples
- Default values
- Usage context

## Benefits of Templatization

### Reusability
- Symbols skill can be used across any project structure
- Architecture-agnostic approach supports various patterns
- No MeatyPrompts-specific assumptions

### Maintainability
- Clear separation of generic vs. project-specific content
- Easy to update core functionality without affecting customizations
- Template variables clearly marked with `{{VARIABLE}}` format

### Documentation
- Self-documenting with variable placeholders
- `_template_notes` in config provides inline guidance
- Links to comprehensive variable documentation

### Flexibility
- Supports different project structures (monorepo, multi-repo, etc.)
- Works with various tech stacks (Python/FastAPI, Node/Express, etc.)
- Adaptable to different architectural patterns

## Related Files

- **`config/template-config.json`** - Complete variable documentation
- **`TEMPLATIZATION_GUIDE.md`** - Project-wide templatization guide
- **`skills/symbols/symbols-config-schema.json`** - JSON schema for validation
- **`skills/symbols/scripts/*.py`** - Symbol extraction scripts (generic, no changes needed)

## Validation Checklist

- [x] All MeatyPrompts-specific references replaced with variables
- [x] Architecture references made generic with variable placeholders
- [x] Path references use `{{PROJECT_PATHS.*}}` variables
- [x] Example code uses `{{PROJECT_EXAMPLES.*}}` variables
- [x] Generic concepts and tool names preserved
- [x] Template variable documentation added
- [x] Customization instructions included in config
- [x] JSON structure remains valid
- [x] Markdown formatting preserved
- [x] Links and references updated to use variables

## Next Steps

1. Update `TEMPLATIZATION_GUIDE.md` to reference symbols skill templatization
2. Add symbols skill variables to `config/template-config.json` if not already present
3. Test templatized files with a different project structure
4. Consider creating a substitution script to automate variable replacement
5. Document symbols skill customization in main CLAUDE.md

---

**Completed**: 2025-11-05
**Files Modified**: 2 (SKILL.md, symbols.config.json)
**Variables Added**: 15+ template variables
**Backward Compatible**: Yes (MeatyPrompts can replace variables with original values)
