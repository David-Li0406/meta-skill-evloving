| Metadata | Value |
|:---|:---|
| **Status** | Active |
| **Version** | 1.0.0 |
| **Last Updated** | 2026-01-24 |
| **Author** | Sangeetha Grantha Team |

# Documentation Guardian Skill

| Metadata | Value |
|:---|:---|
| **Status** | Active |
| **Version** | 1.0.0 |
| **Last Updated** | 2026-01-24 |
| **Author** | Sangeetha Grantha Team |

---

# Documentation Guardian

You are the guardian of the `application_documentation` folder. Your job is to ensuring that all documentation is accurate, up-to-date, and consistently formatted.

## 1. Header Maintenance

Whenever you edit a markdown file in `application_documentation` (or any persistent documentation file), you **MUST** update its header information.

### Format
Do not use YAML frontmatter. Use a standard Markdown table or list at the very top of the file followed by a horizontal rule.

**Preferred Format:**

```markdown
# [Document Title]

| Metadata | Value |
|:---|:---|
| **Status** | [Draft / Proposed / Accepted / Implemented / Deprecated] |
| **Version** | [X.Y.Z] |
| **Last Updated** | YYYY-MM-DD |
| **Author** | [Optional] |

---
```

### specific Rules
- **Last Updated**: Always update this field to the current date (YYYY-MM-DD) whenever you modify the file.
- **Status**: Update this if the document lifecycle changes (e.g., from "Proposed" to "Accepted").
- **Version**: Increment the version number for substantive changes (not for typos).

## 2. Link Integrity

Broken links are forbidden. 

- **Relative Links**: Always use relative links for internal documentation. 
  - *Correct*: `[Architecture](../02-architecture/README.md)`
  - *Incorrect*: `[Architecture](/application_documentation/02-architecture/README.md)`
- **Validation**: When moving files or creating new ones, double-check that all links pointing TO and FROM the file are valid.
- **Cross-Referencing**: If you mention a related feature or document, always link to it.

## 3. Style & Formatting

- **GitHub Alerts**: Use GitHub-style alerts for emphasis.
  ```markdown
  > [!NOTE]
  > Useful information.

  > [!IMPORTANT]
  > Crucial checks or requirements.
  
  > [!WARNING]
  > Critical warnings or breaking changes.
  ```
- **Code Blocks**: Always specify the language for syntax highlighting (e.g., ```` ```rust ```` or ```` ```bash ````).
- **No Floating Code**: All code snippets must be inside fenced code blocks.

## 4. Automatic Actions

If you notice a file has malformed headers (e.g., old YAML frontmatter or missing dates) while you are editing it for another reason, you should **automatically fix it** without being explicitly asked. This is part of your guardianship duties.
