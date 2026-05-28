# Agent Skills Specification

## Directory structure

A skill is a directory containing at minimum a `SKILL.md` file:

```
skill-name/
└── SKILL.md          # Required
```

Optionally include `scripts/`, `references/`, and `assets/` directories.

## SKILL.md format

YAML frontmatter followed by Markdown content.

### Frontmatter (required)

```yaml  theme={null}
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

With optional fields:

```yaml  theme={null}
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents.
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
---
```

| Field           | Required | Constraints                                                                                                       |
| --------------- | -------- | ----------------------------------------------------------------------------------------------------------------- |
| `name`          | Yes      | Max 64 characters. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen.             |
| `description`   | Yes      | Max 1024 characters. Non-empty. Describes what the skill does and when to use it.                                 |
| `license`       | No       | License name or reference to a bundled license file.                                                              |
| `compatibility` | No       | Max 500 characters. Indicates environment requirements (intended product, system packages, network access, etc.). |
| `metadata`      | No       | Arbitrary key-value mapping for additional metadata.                                                              |
| `allowed-tools` | No       | Space-delimited list of pre-approved tools the skill may use. (Experimental)                                      |

#### `name` field

- 1-64 characters, lowercase alphanumeric and hyphens only
- No leading/trailing/consecutive hyphens
- Must match parent directory name

#### `description` field

- 1-1024 characters
- Describe what the skill does AND when to use it
- Include keywords that help agents identify relevant tasks

#### `license` field (optional)

License name or reference to bundled license file.

#### `compatibility` field (optional)

- 1-500 characters
- Environment requirements (product, system packages, network access)

#### `metadata` field (optional)

String key-value map for additional properties.

#### `allowed-tools` field (optional, experimental)

Space-delimited list of pre-approved tools. Example: `Bash(git:*) Bash(jq:*) Read`

### Body content

Markdown instructions after frontmatter. No format restrictions. Recommended: step-by-step instructions, examples, edge cases. Split long content into referenced files.

## Optional directories

### scripts/

Executable code (Python, Bash, JavaScript). Self-contained with clear dependencies and error handling.

### references/

Documentation loaded on demand. Keep files focused for efficient context use.

### assets/

Static resources: templates, images, data files, schemas.

## Progressive disclosure

1. Metadata (~100 tokens) - loaded at startup for all skills
2. Instructions (\<5000 tokens) - loaded when skill activates
3. Resources (as needed) - loaded only when required

Keep SKILL.md under 500 lines. Move detailed content to separate files.

## File references

Use relative paths from skill root. Keep references one level deep.

## Validation

```bash
skills-ref validate ./my-skill
```
