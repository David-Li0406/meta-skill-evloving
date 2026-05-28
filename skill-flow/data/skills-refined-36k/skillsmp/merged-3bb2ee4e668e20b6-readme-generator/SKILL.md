---
name: readme-generator
description: Use this skill to generate comprehensive README.md files for projects, ensuring all necessary information is included and well-structured.
---

# README Generator

Create clear, succinct, and professional README.md files for projects by following a structured approach.

## Instructions

### Step 1: Analyze Project Structure

1. **Explore the project directory** to understand the structure.
2. **Identify the project type** by looking for key files:
   - Python: `setup.py`, `pyproject.toml`, `requirements.txt`, `Pipfile`
   - Node.js: `package.json`, `package-lock.json`, `yarn.lock`
   - Rust: `Cargo.toml`, `Cargo.lock`
   - Go: `go.mod`, `go.sum`
   - Java: `pom.xml`, `build.gradle`
   - Other: Look for configuration files, main entry points.

3. **Read configuration files** to extract:
   - Project name and description
   - Version information
   - Dependencies and requirements
   - Scripts and commands
   - License information
   - Author/maintainer information

### Step 2: Identify Key Components

1. **Find the main entry point**:
   - Look for `main.py`, `index.js`, `src/main.rs`, `main.go`, etc.
   - Check package.json "bin" field, setup.py entry_points, etc.

2. **Discover project features**:
   - Read source files to understand what the project does.
   - Check for example files, demo scripts, or test files.

3. **Identify usage patterns**:
   - Look for CLI commands defined in package.json, setup.py, or Cargo.toml.
   - Find example usage in code comments or test files.

### Step 3: Generate README Sections

Create a well-structured README.md with these sections (include only relevant ones):

#### Required Sections:

1. **Project Title** - Clear, descriptive title.
2. **Description** - What the project does.
3. **Installation** - How to install.
4. **Usage** - How to use the project.

#### Optional Sections (include if relevant):

5. **Features** - Key features and capabilities.
6. **Configuration** - Setup and configuration options.
7. **Development** - For contributors.
8. **Requirements/Dependencies** - What's needed.
9. **Contributing** - How to contribute.
10. **License** - Project license.
11. **Author/Credits** - Who made it.
12. **Badges** - Status badges (optional).

### Step 4: Write the README

1. **Use markdown formatting**:
   - Headers for sections.
   - Code blocks with language tags for examples.
   - Lists for features, requirements, etc.

2. **Make it scannable**:
   - Use clear section headers.
   - Include a table of contents for long READMEs (if > 5 sections).

3. **Include actual examples**:
   - Copy relevant code snippets from the project.
   - Show actual CLI commands from the project.

4. **Check for existing README**:
   - If README.md exists, read it first to preserve important information.
   - Enhance and update rather than completely replace.

### Step 5: Verify and Complete

1. **Read the generated README** back to ensure:
   - All sections are properly formatted.
   - No placeholder text remains.
   - Examples are accurate and work.

2. **Ensure completeness**:
   - Installation instructions are clear.
   - Usage examples are practical.
   - All necessary information is included.

## Best Practices

1. **Be specific**: Use actual project information, not generic placeholders.
2. **Match style**: Follow existing code style and naming conventions in the project.
3. **Practical examples**: Show real usage patterns from the codebase.
4. **Complete**: Include all necessary information for someone new to the project.
5. **Accurate**: Verify all commands and examples work with the actual project setup.

## Notes

- Always analyze the actual project before generating the README.
- Don't guess - read configuration files and source code.
- Adapt the README structure to the project's complexity.