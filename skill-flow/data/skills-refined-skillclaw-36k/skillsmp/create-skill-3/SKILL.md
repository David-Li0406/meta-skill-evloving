---
name: create-skill
description: Guide for authoring agent skills. Use when creating new skills, writing SKILL.md files, or improving existing skills.
---

# Creating Skills

## SKILL.md Structure

```yaml
---
name: my-skill-name        # lowercase, hyphens, max 64 chars
description: Does X and Y. Use when Z happens.  # max 1024 chars, third person
---

# Skill Title

[Instructions go here]
```

## Core Principles

### Be Concise
Agents are smart. Only add context the agent doesn't already have. Challenge each sentence: "Does this justify its token cost?"

### Match Specificity to Risk
- **High freedom** (general guidance): Multiple valid approaches, context-dependent
- **Low freedom** (exact scripts): Fragile operations, specific sequences required

### Write Effective Descriptions
- Use third person ("Processes files" not "I process files")
- Include what it does AND when to use it
- Be specific with key terms for discovery

## Progressive Disclosure

Keep SKILL.md under 500 lines. Link to separate files for advanced content:

```markdown
## Quick start
[Essential instructions here]

## Advanced
- **Feature A**: See [FEATURE_A.md](FEATURE_A.md)
- **Reference**: See [reference.md](reference.md)
```

Keep references **one level deep** from SKILL.md.

## Workflows

For complex tasks, provide checklists:

```markdown
## Workflow

- [ ] Step 1: Analyze input
- [ ] Step 2: Validate results
- [ ] Step 3: Apply changes
- [ ] Step 4: Verify output
```

Include feedback loops: validate → fix errors → repeat.

## Common Patterns

**Templates**: Provide output format examples
**Examples**: Show input/output pairs
**Conditional workflows**: Guide through decision points

## Anti-Patterns

- Verbose explanations of concepts agents already know
- Time-sensitive information ("after August 2025...")
- Inconsistent terminology
- Deeply nested file references
- Windows-style paths (`\` instead of `/`)
- Multiple equivalent options without a default

## With Executable Scripts

Add scripts to skills when you need to abstract over complex operations.
Use .NET file-based apps to write the scripts. Use the "dotnet-file-based-apps"
skill to aide in creating scripts.

### Scripts Directory Structure

```
my-skill/
├── SKILL.md
├── reference.md
└── scripts/
    ├── analyze.cs
    ├── validate.cs
    └── apply.cs
```

### Document Scripts Clearly

````markdown
## Utility Scripts

**analyze.cs**: Extract metadata from input file
```bash
dotnet scripts/analyze.cs input.pdf > metadata.json
```

**validate.cs**: Check for errors before proceeding
```bash
dotnet scripts/validate.cs metadata.json
# Returns "OK" or lists specific errors
```
````

### Execute vs. Read

Be explicit about intent:
- **Execute**: "Run `dotnet scripts/validate.cs` to check the output"
- **Read**: "See `scripts/validate.cs` for the validation algorithm"

Execution is preferred—it's more reliable and doesn't consume context tokens.

### Handle Errors in Scripts

```csharp
// Good: Handle errors explicitly
string Process(string path)
{
    if (!File.Exists(path))
    {
        Console.WriteLine($"Creating {path} with defaults");
        File.WriteAllText(path, "");
        return "";
    }
    return File.ReadAllText(path);
}

// Bad: Let the agent figure it out
string Process(string path) => File.ReadAllText(path);
```

### Document Constants

```csharp
// Good: Self-documenting
const int RequestTimeout = 30;  // Most requests complete within 30s
const int MaxRetries = 3;       // Intermittent failures resolve by retry 2

// Bad: Magic numbers
const int Timeout = 47;
const int Retries = 5;
```

### List Dependencies

````markdown
## Setup

Add required packages as directives in your script:
```csharp
#:package CliWrap@3.6.6
#:package System.CommandLine@*
```
````

## Checklist

- [ ] Description is specific with key terms
- [ ] Description says what AND when
- [ ] SKILL.md under 500 lines
- [ ] No time-sensitive information
- [ ] Consistent terminology
- [ ] File references one level deep
- [ ] Tested with target models
