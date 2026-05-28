# Slash Command Validation Checklist

Comprehensive validation checklist for ensuring slash commands are correct, secure, and effective.

## Quick Validation (5 Minutes)

Use this for rapid pre-flight checks:

- [ ] File named with `.md` extension
- [ ] Lowercase-with-hyphens naming format
- [ ] Located in `.claude/commands/` or `~/.claude/commands/`
- [ ] YAML frontmatter valid if present (delimiters, no tabs)
- [ ] Prompt content is clear and actionable
- [ ] Tested with basic invocation

## Comprehensive Validation (15-20 Minutes)

### 1. File Structure Validation

#### 1.1 File Naming
- [ ] Filename uses only lowercase letters, numbers, and hyphens
- [ ] No underscores, spaces, or special characters
- [ ] File extension is `.md`
- [ ] Name is descriptive and indicates purpose
- [ ] Name length is reasonable (prefer under 32 characters)
- [ ] No conflicts with existing command names

**Validation Regex**: `^[a-z0-9-]+\.md$`

#### 1.2 File Location
- [ ] File is in correct directory:
  - `.claude/commands/` for project commands
  - `~/.claude/commands/` for personal commands
- [ ] Subdirectory path uses forward slashes (if namespaced)
- [ ] Directory exists and is accessible
- [ ] File permissions allow reading

#### 1.3 File Content Structure
- [ ] YAML frontmatter (if present) at very top of file
- [ ] Frontmatter delimiters properly placed
- [ ] Prompt content after frontmatter (or at top if no frontmatter)
- [ ] No syntax errors in markdown
- [ ] Encoding is UTF-8

### 2. YAML Frontmatter Validation

#### 2.1 Syntax
- [ ] Opening delimiter `---` present on line 1 (if using frontmatter)
- [ ] Closing delimiter `---` present after fields
- [ ] No tabs anywhere in YAML (use spaces only)
- [ ] Each field formatted as `key: value`
- [ ] No trailing spaces after values
- [ ] Consistent indentation (2 spaces standard)
- [ ] No syntax errors (validate with YAML parser if available)

#### 2.2 Required Fields

None are strictly required, but validate if present:

**description** (if present):
- [ ] Non-empty string
- [ ] Under 120 characters (recommended)
- [ ] Third-person voice (e.g., "Validates" not "Validate")
- [ ] Clear and specific
- [ ] Helpful for /help display

**allowed-tools** (if bash used):
- [ ] Format: `Bash(command:pattern)` or comma-separated list
- [ ] Each command explicitly listed
- [ ] Patterns specified (use `*` for any, or specific pattern)
- [ ] No unrestricted access: `Bash(*:*)`
- [ ] Only necessary commands included

**argument-hint** (if arguments used):
- [ ] Documents all arguments used in prompt
- [ ] Format: `[required-arg] <optional-arg>`
- [ ] Square brackets for required arguments
- [ ] Angle brackets for optional arguments
- [ ] Descriptive names (not just `[arg1]`)

**model** (if specified):
- [ ] Value is valid: `haiku`, `sonnet`, or `opus`
- [ ] Appropriate for command complexity
- [ ] Consider cost implications

**disable-model-invocation** (rare):
- [ ] Value is boolean: `true` or `false`
- [ ] Only used when automatic invocation should be prevented

#### 2.3 Field Values
- [ ] All string values properly quoted if containing special characters
- [ ] Boolean values are lowercase: `true`, `false` (not `True`, `False`)
- [ ] No undefined or null values where not appropriate
- [ ] Values match expected types for each field

### 3. Prompt Content Validation

#### 3.1 Clarity
- [ ] Instructions are explicit and direct
- [ ] No ambiguous language
- [ ] Purpose is clear
- [ ] Context is provided
- [ ] Output format is specified
- [ ] Audience is identified if relevant

#### 3.2 Completeness
- [ ] All necessary information included
- [ ] Edge cases are considered
- [ ] Error scenarios are addressed
- [ ] Examples provided where helpful
- [ ] No missing critical instructions

#### 3.3 Structure
- [ ] Logical organization
- [ ] Clear sections if complex
- [ ] XML tags used appropriately for structure
- [ ] Lists used for multiple items
- [ ] Formatting aids readability

#### 3.4 Best Practices Compliance
- [ ] Follows Claude prompting patterns
- [ ] Imperative voice for instructions
- [ ] Specific rather than general
- [ ] Examples match intended behavior
- [ ] Appropriate level of detail
- [ ] No contradictory instructions

### 4. Argument Validation

#### 4.1 Placeholder Syntax
- [ ] Correct format: `$1`, `$2`, ..., `$9` or `$ARGUMENTS`
- [ ] No typos: not `${1}`, `$arg1`, `$ARG1`
- [ ] Consistent usage throughout prompt
- [ ] Placeholders documented in argument-hint

#### 4.2 Argument Logic
- [ ] Arguments used make sense for command purpose
- [ ] Required arguments clearly identified
- [ ] Optional arguments have sensible defaults
- [ ] Edge case of missing arguments handled
- [ ] Multiple arguments are ordered logically

#### 4.3 Argument Documentation
- [ ] `argument-hint` present in frontmatter if arguments used
- [ ] All placeholders documented in hint
- [ ] Hint format correct: `[req] <opt>`
- [ ] Argument names are descriptive
- [ ] Order in hint matches usage in prompt

### 5. Bash Execution Validation

#### 5.1 Command Prefix
- [ ] All bash commands prefixed with `!`
- [ ] Prefix directly precedes command (no space)
- [ ] Commands are on their own lines or clearly separated

#### 5.2 Tool Restrictions
- [ ] `allowed-tools` field present in frontmatter if bash used
- [ ] Every bash command used is listed in allowed-tools
- [ ] Format is correct: `Bash(command:pattern)`
- [ ] Patterns appropriately restrict usage
- [ ] No overly permissive patterns

#### 5.3 Security
- [ ] No dangerous commands: `rm`, `dd`, `format`, `mkfs`
- [ ] No unrestricted access: `Bash(*:*)`
- [ ] Command arguments validated or restricted
- [ ] File operations are safe and bounded
- [ ] No command injection vulnerabilities

#### 5.4 Necessity
- [ ] Bash commands are actually necessary
- [ ] Can't be replaced with `@` file references
- [ ] Can't be done with Claude's tools directly
- [ ] Provides significant value

### 6. File Reference Validation

#### 6.1 Syntax
- [ ] File references use `@` prefix
- [ ] Format: `@path/to/file.ext`
- [ ] Paths are valid (absolute or relative)
- [ ] No extra spaces around @

#### 6.2 Usage
- [ ] Referenced files likely to exist
- [ ] Paths are reasonable and specific
- [ ] Not using wildcards inappropriately
- [ ] Handles missing files gracefully

#### 6.3 Context
- [ ] File references make sense for command purpose
- [ ] Instructions for what to do with file contents
- [ ] Multiple file references are clear and organized

### 7. Security Validation

#### 7.1 Bash Security
- [ ] No unrestricted command execution
- [ ] Commands are explicitly listed
- [ ] Patterns restrict to safe operations
- [ ] No commands that could damage system
- [ ] No network access unless necessary and justified

#### 7.2 Input Safety
- [ ] Arguments are validated or sanitized
- [ ] No SQL injection risks
- [ ] No command injection risks
- [ ] No path traversal vulnerabilities
- [ ] File access is controlled

#### 7.3 Information Disclosure
- [ ] No exposure of secrets or credentials
- [ ] No unrestricted file reading
- [ ] Output doesn't leak sensitive data
- [ ] Appropriate boundaries on operations

### 8. Integration Validation

#### 8.1 Git Integration
- [ ] Git commands use safe operations
- [ ] Read-only operations preferred
- [ ] No destructive git operations without explicit user request
- [ ] Repository context is appropriate

#### 8.2 GitHub CLI Integration
- [ ] Uses `gh` command correctly
- [ ] API operations are appropriate
- [ ] Rate limits considered
- [ ] Authentication handled properly
- [ ] Operations are non-destructive or clearly documented

#### 8.3 Tool Compatibility
- [ ] Commands work with available tools
- [ ] Dependencies are reasonable to expect
- [ ] Cross-platform considerations addressed
- [ ] Version requirements documented if relevant

### 9. Usability Validation

#### 9.1 Discoverability
- [ ] Command name indicates purpose
- [ ] Description (if present) is helpful
- [ ] Arguments are documented
- [ ] Command appears in /help appropriately

#### 9.2 User Experience
- [ ] Easy to invoke
- [ ] Arguments are intuitive
- [ ] Output is useful and well-formatted
- [ ] Error messages are helpful
- [ ] Provides value for effort

#### 9.3 Documentation
- [ ] Usage is clear from name and description
- [ ] Examples provided in comments if helpful
- [ ] Edge cases documented
- [ ] Limitations noted if applicable

### 10. Performance Validation

#### 10.1 Efficiency
- [ ] Command doesn't do unnecessary work
- [ ] Appropriate model specified (haiku for simple tasks)
- [ ] Bash commands are efficient
- [ ] File operations are reasonable in scope

#### 10.2 Cost
- [ ] Model choice is cost-effective
- [ ] Not overusing complex models for simple tasks
- [ ] Operations are bounded and won't run forever
- [ ] Resource usage is reasonable

### 11. Testing Validation

#### 11.1 Basic Tests Performed
- [ ] Command invokes without errors
- [ ] Output is as expected
- [ ] Arguments substitute correctly
- [ ] Bash commands execute (if applicable)
- [ ] File references work (if applicable)

#### 11.2 Edge Case Tests Performed
- [ ] Missing arguments handled
- [ ] Invalid arguments handled
- [ ] Missing files handled
- [ ] Unexpected input managed
- [ ] Error conditions tested

#### 11.3 Integration Tests Performed
- [ ] Works in git repository context
- [ ] Integrates with GitHub CLI (if applicable)
- [ ] Doesn't conflict with other commands
- [ ] Produces valuable output
- [ ] Real-world usage validated

## Validation Workflow

### Step 1: Automated Checks (2 min)
1. Verify filename format with regex
2. Check YAML syntax if frontmatter present
3. Validate file location
4. Check for common syntax errors

### Step 2: Manual Review (5 min)
1. Read through prompt content
2. Check clarity and completeness
3. Verify arguments make sense
4. Review bash restrictions if applicable
5. Assess security implications

### Step 3: Testing (5-10 min)
1. Invoke command with typical arguments
2. Test with edge cases
3. Verify bash execution if applicable
4. Check file references if applicable
5. Validate output quality

### Step 4: Sign-Off (1 min)
- [ ] All critical issues resolved
- [ ] Major improvements implemented
- [ ] Minor enhancements noted for future
- [ ] Command ready for use

## Common Issues and Fixes

### Issue: YAML Syntax Error
**Detection**: Command fails to load, parsing error

**Checks**:
- Missing or malformed delimiters
- Tabs instead of spaces
- Incorrect field format
- Special characters not quoted

**Fix**: Correct YAML syntax, validate with parser

### Issue: Arguments Not Working
**Detection**: `$1` appears literally in output

**Checks**:
- Placeholder syntax incorrect
- Not documented in argument-hint
- Arguments not provided when invoking

**Fix**: Correct syntax, document in frontmatter

### Issue: Bash Commands Not Executing
**Detection**: Commands don't run or permission error

**Checks**:
- Missing `!` prefix
- Not listed in allowed-tools
- Pattern too restrictive
- Command syntax incorrect

**Fix**: Add prefix, update allowed-tools

### Issue: Security Concerns
**Detection**: Overly permissive tool restrictions

**Checks**:
- Unrestricted bash: `Bash(*:*)`
- Dangerous commands allowed
- No input validation
- Broad file access

**Fix**: Restrict tools, validate inputs, limit scope

### Issue: Poor Usability
**Detection**: Users confused or command not helpful

**Checks**:
- Unclear command name
- Missing or vague description
- Arguments not documented
- Output not useful

**Fix**: Improve naming, add description, document arguments

## Validation Severity Levels

### Critical (Must Fix)
- YAML syntax errors
- Invalid file structure
- Security vulnerabilities
- Broken functionality
- Data loss risks

### Major (Should Fix)
- Missing documentation
- Poor argument handling
- Overly permissive restrictions
- Unclear instructions
- Missing edge case handling

### Minor (Nice to Have)
- Suboptimal naming
- Could be more efficient
- Missing examples
- Style inconsistencies
- Documentation improvements

## Sign-Off Criteria

Command is ready for deployment when:
- [ ] All critical issues resolved
- [ ] All major issues addressed or explicitly accepted
- [ ] Basic and edge case testing passed
- [ ] Security validation completed
- [ ] Documentation is sufficient
- [ ] Team reviewed if project command (optional but recommended)
- [ ] Ready for real-world usage

## Post-Deployment Validation

After command is deployed:
- [ ] Monitor actual usage patterns
- [ ] Collect user feedback
- [ ] Track error rates
- [ ] Assess value delivered
- [ ] Plan improvements based on learnings
