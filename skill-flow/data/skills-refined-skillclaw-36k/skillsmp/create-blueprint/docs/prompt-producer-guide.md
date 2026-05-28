# Prompt Producer Authoring Guide

This guide teaches you how to create prompt producers - LLM-based producers that generate structured content (scripts, prompts, metadata) used by downstream asset producers.

## Table of Contents

1. [Introduction](#introduction)
2. [File Organization](#file-organization)
3. [The Three Files of a Prompt Producer](#the-three-files-of-a-prompt-producer)
4. [TOML Prompt Template Reference](#toml-prompt-template-reference)
5. [Variable Binding: Connecting YAML to TOML](#variable-binding-connecting-yaml-to-toml)
6. [Example Walkthroughs](#example-walkthroughs)
7. [Common Pitfalls](#common-pitfalls)
8. [Quick Reference Checklist](#quick-reference-checklist)

---

## Introduction

Prompt producers are LLM-powered components that generate structured content. Unlike asset producers (which call media APIs to generate images, videos, audio), prompt producers call language models to generate:

- Scripts and narratives
- Image/video prompts for downstream generators
- Metadata and conditional flags
- Structured JSON outputs

Every prompt producer consists of three files that work together to define what the LLM receives and what it outputs.

---

## File Organization

All prompt producers follow this standard structure:

```
catalog/producers/prompt/{producer-name}/
├── {producer-name}.toml           # Prompt template (system + user prompts)
├── {producer-name}.yaml           # Producer definition (inputs, outputs, metadata)
└── {producer-name}-output.json    # JSON Schema for structured output
```

**Naming conventions:**
- Files use **kebab-case** (e.g., `ad-script.toml`)
- Producer IDs use **PascalCase** (e.g., `AdScriptProducer`)
- Variable names use **PascalCase** (e.g., `NumOfSegments`)

---

## The Three Files of a Prompt Producer

### 3.1 The TOML File (Prompt Template)

The TOML file defines **what the LLM sees**. It has exactly three sections:

```toml
variables = ["Variable1", "Variable2", "Variable3"]

systemPrompt = """
Static instructions that establish the AI's role and guidelines.
"""

userPrompt = """
Dynamic template with {{Variable1}} interpolation.
"""
```

### 3.2 The YAML File (Producer Definition)

The YAML file defines **what the producer accepts and produces**:

```yaml
meta:
  name: Human Readable Name
  description: What this producer does
  id: ProducerIdPascalCase
  version: 0.1.0
  promptFile: ./producer-name.toml
  outputSchema: ./producer-name-output.json

inputs:
  - name: Variable1          # Must match TOML variable name!
    description: Purpose
    type: string             # string, int, or other types

artifacts:
  - name: OutputName
    type: json               # The structured output
    arrays:
      - path: Items
        countInput: NumOfItems
```

### 3.3 The JSON Schema File (Output Schema)

The JSON schema defines **the structure of LLM output**:

```json
{
  "name": "OutputName",
  "strict": true,
  "schema": {
    "type": "object",
    "properties": {
      "Title": { "type": "string" },
      "Items": {
        "type": "array",
        "items": { ... }
      }
    },
    "required": ["Title", "Items"],
    "additionalProperties": false
  }
}
```

---

## TOML Prompt Template Reference

### 4.1 Variables Section (CRITICAL)

The `variables` array declares all template variables that can be interpolated in prompts:

```toml
variables = ["ProductDescription", "NumOfClips", "Style", "Audience"]
```

**Rules:**
- Variable names **MUST exactly match** YAML input names (case-sensitive!)
- Use **PascalCase** for all variables
- Order does not matter
- Every variable listed here can be used as `{{VariableName}}` in prompts

### 4.2 System Prompt Section

The `systemPrompt` establishes the AI's role and provides static guidelines:

```toml
systemPrompt = """
You are an expert filmmaker.

Guidelines:
- Create engaging narratives
- Follow the exact JSON schema provided
- Ensure content matches the specified duration

The output must follow the exact JSON schema provided.
"""
```

**Best practices:**
- Clearly define the AI's expertise/role
- List specific guidelines and constraints
- Reference the JSON schema requirement
- Include domain-specific instructions
- Keep it static - no variable interpolation here

### 4.3 User Prompt Section

The `userPrompt` provides the dynamic, user-specific request:

```toml
userPrompt = """
Create a video script with the following specifications:

**Product:** {{ProductDescription}}
**Style:** {{Style}}
**Number of Clips:** {{NumOfClips}}

Generate {{NumOfClips}} scene descriptions that showcase the product.
"""
```

**Variable interpolation:**
- Use `{{VariableName}}` syntax (double curly braces)
- Can use the same variable multiple times
- Can embed in sentences: `"Generate {{NumOfSegments}} segments"`
- Works with all types (strings display as-is, ints as numbers)

---

## Variable Binding: Connecting YAML to TOML

This is the most critical concept. The binding flows like this:

```
YAML Input Definition → TOML Variables Array → User Prompt Interpolation
       ↓                        ↓                        ↓
- name: Duration        "Duration"              {{Duration}}
- name: Style           "Style"                 {{Style}}
- name: NumOfSegments   "NumOfSegments"         {{NumOfSegments}}
```

**The contract:**
1. Every input in YAML that you want to use in prompts must be listed in TOML `variables`
2. The names must match **exactly** (case-sensitive)
3. The `{{VariableName}}` in prompts must also match exactly

**Example from ad-script producer:**

YAML inputs:
```yaml
inputs:
  - name: ProductDescription
    type: string
  - name: NumOfClips
    type: int
```

TOML variables:
```toml
variables = ["ProductDescription", "NumOfClips", ...]
```

TOML userPrompt:
```toml
userPrompt = """
**Product:** {{ProductDescription}}
**Number of Clips:** {{NumOfClips}}
"""
```

---

## Example Walkthroughs

The catalog contains several prompt producers worth studying. Here's what makes each unique:

### Example 1: Ad Script (`catalog/producers/prompt/ad-script/`)

**Unique patterns:**
- **Character-product centric design**: Generates separate image prompts for both a character AND a product
- **Per-scene narration control**: Each scene has a `HasNarration` boolean, this controls whether narration audio should be generated or not
- **Strict schema enforcement**: Uses `"strict": true` in JSON schema

Key TOML structure:
```toml
variables = ["ProductDescription", "CharacterDescription", "AdConcept", "NumOfClips", ...]
```

The system prompt instructs: "Not all scenes need narration - some can be purely visual" - demonstrating how to give the LLM flexibility within structured output.

### Example 2: Flow Video (`catalog/producers/prompt/flow-video/`)

**Unique patterns:**
- **Sliding window image architecture**: Generates N+1 images for N segments
- **Transition-aware design**: Images serve as boundaries between segments (end of segment N = start of segment N+1)
- **Synchronized multi-modal outputs**: Produces script, video prompts, AND image prompts in one call

Key YAML artifact with offset:
```yaml
artifacts:
  - name: ImagePrompts
    type: array
    itemType: string
    countInput: NumOfSegments
    countInputOffset: 1          # <-- Produces N+1 images!
```

The system prompt explains the sliding window concept directly to the LLM:
> "You will also be creating a set of image prompts that are one larger than the total number of segments. These images will be used as the starting and ending images for each segment in a sliding window."

### Example 3: Documentary Talking Head (`catalog/producers/prompt/documentary-talkinghead/`)

**Unique patterns:**
- **Enum-based narration types**: Segments can be `ImageNarration`, `VideoNarration`, `TalkingHead`, or `MapNarration`
- **Conditional content generation**: Different fields are populated based on NarrationType
- **Nested array structure**: Segments contain ImagePrompts arrays

Key YAML with nested arrays:
```yaml
artifacts:
  - name: VideoScript
    type: json
    arrays:
      - path: Segments
        countInput: NumOfSegments
      - path: Segments.ImagePrompts          # <-- Nested array
        countInput: NumOfImagesPerSegment
```

The system prompt defines four distinct narration types and what content each requires.

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| **Variable name mismatch** | Runtime error: variable not found | Ensure YAML input names exactly match TOML variables (case-sensitive!) |
| **Missing variable in array** | Template renders with `{{Literal}}` | Add the variable to TOML `variables = [...]` array |
| **Wrong interpolation syntax** | Variable not substituted | Use `{{Variable}}` not `{Variable}` or `{{ Variable }}` |
| **Schema mismatch** | LLM output doesn't match artifacts | Ensure JSON schema paths match YAML artifact array paths |
| **Missing `countInput`** | "Missing size for dimension" error | Add `countInput: InputName` to array artifacts and loops |
| **Forgetting `strict: true`** | LLM adds extra fields | Add `"strict": true` to JSON schema |

### The Most Common Mistake

Forgetting to add a variable to the TOML `variables` array:

```toml
# WRONG - Duration is used but not declared
variables = ["InquiryPrompt", "Style"]

userPrompt = """
Duration: {{Duration}}  # <-- Will fail! Duration not in variables array
"""
```

```toml
# CORRECT - All used variables are declared
variables = ["InquiryPrompt", "Style", "Duration"]

userPrompt = """
Duration: {{Duration}}  # <-- Works!
"""
```

---

## Quick Reference Checklist

When creating a prompt producer, verify:

- [ ] **Three files created** in `catalog/producers/prompt/{name}/`
  - [ ] `{name}.toml` - Prompt template
  - [ ] `{name}.yaml` - Producer definition
  - [ ] `{name}-output.json` - Output schema

- [ ] **TOML file has all three sections**
  - [ ] `variables = [...]` array
  - [ ] `systemPrompt = """..."""`
  - [ ] `userPrompt = """..."""`

- [ ] **Variable binding is correct**
  - [ ] Every TOML variable has matching YAML input (same name, case-sensitive)
  - [ ] Every `{{Variable}}` in prompts is in the variables array
  - [ ] No typos in variable names

- [ ] **YAML meta section is complete**
  - [ ] `promptFile:` points to correct TOML path
  - [ ] `outputSchema:` points to correct JSON path

- [ ] **Array artifacts have sizing**
  - [ ] `countInput:` specified for array types
  - [ ] `countInputOffset:` if needed (like N+1 pattern)
  - [ ] Nested arrays have separate count inputs

- [ ] **JSON schema matches YAML**
  - [ ] Array paths in schema match `arrays.path` in YAML
  - [ ] `"strict": true` for reliable output
  - [ ] All required fields listed

---

For more examples, explore the catalog at your Renku workspace:
- `catalog/producers/prompt/` - All prompt producer definitions
- `catalog/blueprints/` - See how producers are composed into workflows
