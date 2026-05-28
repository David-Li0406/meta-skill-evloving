---
name: readme-generator
description: Use this skill to generate comprehensive README.md files for projects, ensuring all necessary information is included for users and contributors.
---

# README Generator

Create clear, professional README.md files for projects by following a structured approach.

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

1. **Find the main entry point** by looking for files like `main.py`, `index.js`, etc.
2. **Discover project features** by reading source files to understand functionality.
3. **Identify usage patterns** from CLI commands or example files.

### Step 3: Generate README Sections

Create a well-structured README.md with these sections (include only relevant ones):

#### Required Sections:

1. **Project Title** - Clear, descriptive title.
2. **Description** - What the project does, extracted from config files or source code.
3. **Installation** - Step-by-step setup instructions based on project type.
4. **Usage** - Basic usage examples and CLI commands if applicable.

#### Optional Sections (include if relevant):

5. **Features** - Key features and capabilities.
6. **Configuration** - Environment variables and configuration files.
7. **Development** - Instructions for setting up the development environment.
8. **Requirements/Dependencies** - Key dependencies and system requirements.
9. **Contributing** - Link to contributing guidelines or basic instructions.
10. **License** - Project license information.
11. **Author/Credits** - Contributors and authors.
12. **Badges** - Status badges if applicable.

### Step 4: Write the README

1. **Use markdown formatting** for clarity and organization.
2. **Make it scannable** with clear section headers and consistent formatting.
3. **Include actual examples** from the project to enhance understanding.
4. **Check for existing README** to preserve important information and enhance it.

### Step 5: Verify and Complete

1. **Read the generated README** to ensure proper formatting and accuracy.
2. **Ensure completeness** of installation instructions and usage examples.

## Best Practices

- Be specific and use actual project information.
- Match style with existing code conventions.
- Provide practical examples from the codebase.
- Verify all commands and examples work with the actual project setup.

## Notes

- Always analyze the actual project before generating the README.
- Adapt the README structure to the project's complexity.