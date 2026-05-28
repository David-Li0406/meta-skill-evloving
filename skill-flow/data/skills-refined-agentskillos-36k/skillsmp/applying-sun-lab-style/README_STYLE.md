# README Style Guide

Conventions for README files in Sun Lab projects.

---

## Structure

README files use the following section order. Sections marked as optional may be omitted based on project type.

1. **Title**: Project name as H1 heading (`# project-name`)
2. **One-line description**: Brief summary immediately after the title
3. **Badges**: PyPI/language badges, tooling badges, license, status (no blank line before badges)
4. **Horizontal rule**: `___` to separate header from content
5. **Detailed Description**: Expanded explanation of the library's purpose
6. **Features** *(optional)*: Bulleted list of key features
7. **Table of Contents**: Links to all major sections using Markdown anchors
8. **Dependencies**: External requirements and automatic installation notes
9. **Installation**: Source and pip installation instructions
10. **Usage**: Detailed usage instructions with subsections
11. **API Documentation**: Link to hosted documentation
12. **Developers** *(optional)*: Development setup and automation
13. **Versioning**: Semantic versioning statement with link to repository tags
14. **Authors**: List of contributors with GitHub profile links
15. **License**: License type with link to LICENSE file
16. **Acknowledgments**: Credits to Sun lab members and dependency creators

Use horizontal rules (`___`) to separate major sections.

---

## Writing Style

**Voice**: Use third person throughout. Refer to the project as "this library," "the library," or by its name. Avoid
first person ("I," "we") and second person ("you") where possible.

```markdown
<!-- Good -->
This library abstracts all necessary steps for acquiring and saving video data.
The library supports Windows, Linux, and macOS.

<!-- Avoid -->
We provide tools for acquiring and saving video data.
You can use this library on Windows, Linux, and macOS.
```

**Tense**: Use present tense as the default. Avoid "will" unless omitting it makes the sentence awkward or unclear.

```markdown
<!-- Good - present tense -->
The method returns a tuple of timestamps.
This command generates a configuration file.

<!-- Good - "will" where natural -->
These dependencies will be automatically resolved when the library is installed.

<!-- Avoid - unnecessary "will" -->
The method will return a tuple of timestamps.
```

**Notes and warnings**: Use `**Note!**` or `***Note!***` for important information. Use `**Warning!**`,
`***Warning!***`, or `***Critical!***` for dangerous operations or essential requirements.

---

## Example

```markdown
# sl-unity-tasks

VR behavioral experiment tasks for the Sun Lab's mesoscope experiments.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

___

This project provides infinite corridor VR environments where animals navigate through visual cue sequences while
receiving stimuli based on behavior. The system integrates with sl-experiment for data acquisition via MQTT messaging.

## Table of Contents

- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
...
```

---

## Codebase Cross-Referencing

When writing or updating README content that describes how the library works, you MUST cross-reference against the
current state of the codebase to ensure accuracy.

**Sections requiring verification:**
- Architecture descriptions
- API usage examples
- Configuration options
- File paths and directory structures
- Class names, method signatures, and parameters
- Workflow descriptions

**Verification process:**
1. Identify all technical claims in the README section
2. Use `/explore-codebase` skill if unfamiliar with the relevant code
3. Read source files to verify each claim
4. Update README content to match actual implementation
5. Remove references to deprecated or non-existent features

---

## Standard Sections

**Acknowledgments**: Use the standard format for crediting Sun lab members and dependencies:

```markdown
## Acknowledgments

- All Sun lab [members](https://neuroai.github.io/sunlab/people) for providing the inspiration
  and comments during the development of this library.
- The creators of all other dependencies and projects listed in the
  [pyproject.toml](pyproject.toml) file.
```

**Versioning**: Use the standard semantic versioning statement:

```markdown
## Versioning

This project uses [semantic versioning](https://semver.org/). See the
[tags on this repository](https://github.com/Sun-Lab-NBB/project-name/tags) for the available
project releases.
```

**License**: Use the standard license statement:

```markdown
## License

This project is licensed under the GPL3 License: see the [LICENSE](LICENSE) file for details.
```

---

## MCP Server Documentation

Libraries that provide MCP servers should document this functionality in the README under Usage.

**Structure**: Include the following information:

1. Brief description of what the MCP server exposes
2. How to start the server (CLI command)
3. List of available tools with brief descriptions
4. Configuration instructions (e.g., Claude Desktop setup)

**Example**:

```markdown
### MCP Server

This library provides an MCP server that exposes camera discovery, video session management, and
runtime checks for AI agent integration.

#### Starting the Server

Start the MCP server using the CLI:

```
axvs mcp
```

#### Available Tools

| Tool                         | Description                                    |
|------------------------------|------------------------------------------------|
| `list_cameras`               | Discovers all compatible cameras on the system |
| `start_video_session`        | Starts a video capture session                 |
| `stop_video_session`         | Stops the active video session                 |

#### Claude Desktop Configuration

Add the following to the Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "ataraxis-video-system": {
      "command": "axvs",
      "args": ["mcp"]
    }
  }
}
```
```

---

## Verification Checklist

**You MUST verify your edits against this checklist before submitting any changes to README files.**

```
README Style Compliance:
- [ ] Title as H1 heading with project name
- [ ] One-line description immediately after title
- [ ] Badges for license and status indicators
- [ ] Horizontal rule (`___`) after badges
- [ ] Detailed description section
- [ ] Table of Contents with links to sections
- [ ] Third-person voice throughout (no "I", "we", "you")
- [ ] Present tense as default
- [ ] All required sections included (Dependencies, Installation, Usage, etc.)
- [ ] Technical descriptions cross-referenced against codebase
- [ ] File paths and class names verified to exist
- [ ] API examples tested against actual implementation
```
