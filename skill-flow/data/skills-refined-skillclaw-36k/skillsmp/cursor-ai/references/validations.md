# Cursor Ai - Validations

## Cursorrules File in Wrong Location

### **Id**
cursorrules-in-wrong-location
### **Severity**
high
### **Type**
filepath
### **Pattern**
src/\.cursorrules|\.cursor/rules\.mdc|cursorrules\.md
### **Message**
.cursorrules must be in project root, or use .cursor/rules/*.mdc
### **Fix Action**
Move to project root or .cursor/rules/ directory
### **Applies To**
  - **/.cursorrules
  - **/*.mdc

## MDC File Without Frontmatter

### **Id**
mdc-missing-frontmatter
### **Severity**
high
### **Type**
regex
### **Pattern**
^[^-]|^-[^-]
### **Message**
.mdc files require YAML frontmatter with description and globs
### **Fix Action**
  Add frontmatter: ---
  description: ...
  globs: [...]
  ---
### **Applies To**
  - .cursor/rules/*.mdc

## Glob Pattern Too Broad

### **Id**
overly-broad-glob
### **Severity**
medium
### **Type**
regex
### **Pattern**
globs:\s*\[\s*"\*\*\/\*"\s*\]
### **Message**
Glob matches all files. Consider more specific patterns to reduce token usage.
### **Fix Action**
Use specific globs like ["src/**/*.ts"] or split into multiple files
### **Applies To**
  - .cursor/rules/*.mdc

## Rules File Exceeds Recommended Size

### **Id**
cursorrules-too-large
### **Severity**
medium
### **Type**
line_count
### **Threshold**

### **Message**
Rules file is very large. Consider splitting into .cursor/rules/*.mdc files.
### **Fix Action**
Split by concern: core.mdc, testing.mdc, api.mdc
### **Applies To**
  - .cursorrules

## Dangerous Command Not Blocked in Rules

### **Id**
dangerous-command-allowed
### **Severity**
medium
### **Type**
regex
### **Pattern**
rm -rf|git push.*force|git reset.*hard|DROP TABLE
### **Negative Pattern**
never|forbidden|do not|dont|NEVER
### **Message**
Dangerous commands mentioned without explicit prohibition.
### **Fix Action**
Add to FORBIDDEN or NEVER sections in rules
### **Applies To**
  - .cursorrules
  - .cursor/rules/*.mdc

## Rules Without Tech Stack Context

### **Id**
no-tech-stack-defined
### **Severity**
low
### **Type**
regex
### **Pattern**
---\ndescription
### **Negative Pattern**
stack|framework|language|typescript|react|next
### **Message**
Rules file doesn't specify tech stack. AI may make wrong assumptions.
### **Fix Action**
Add Tech Stack section listing frameworks and languages
### **Applies To**
  - .cursor/rules/core.mdc
  - .cursorrules

## Vague Instructions in Rules

### **Id**
vague-instructions
### **Severity**
low
### **Type**
regex
### **Pattern**
write good code|be careful|use best practices|follow standards
### **Message**
Vague instructions are ignored. Be specific about what you want.
### **Fix Action**
Replace with specific, actionable instructions
### **Applies To**
  - .cursorrules
  - .cursor/rules/*.mdc

## Potentially Conflicting Rules

### **Id**
conflicting-rules
### **Severity**
low
### **Type**
regex
### **Pattern**
(always|never).*\n.*(always|never)
### **Message**
Multiple always/never rules may conflict. Review for consistency.
### **Fix Action**
Ensure rules don't contradict each other
### **Applies To**
  - .cursorrules
  - .cursor/rules/*.mdc