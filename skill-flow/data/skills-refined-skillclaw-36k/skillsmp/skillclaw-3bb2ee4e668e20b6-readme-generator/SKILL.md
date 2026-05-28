---
name: readme-generator
description: Use this skill when you need to create a comprehensive README.md file for a project, ensuring all essential information is included.
---

# README Generator

Create a clear and professional README.md file for your project by following these structured steps.

## Instructions

### Step 1: Analyze Project Structure

1. **Explore the project directory** to understand its structure.
2. **Identify the project type** by looking for key files:
   - Python: `setup.py`, `pyproject.toml`, `requirements.txt`, `Pipfile`
   - Node.js: `package.json`, `package-lock.json`, `yarn.lock`
   - Rust: `Cargo.toml`, `Cargo.lock`
   - Go: `go.mod`, `go.sum`
   - Java: `pom.xml`, `build.gradle`
   - Other: Look for relevant configuration files.

3. **Read configuration files** to extract:
   - Project name and description
   - Version information
   - Dependencies and requirements
   - License information
   - Author/maintainer information

### Step 2: Identify Key Components

1. **Find the main entry point** of the project:
   - Look for files like `main.py`, `index.js`, `src/main.rs`, etc.
   - Check for executable scripts or entry points in configuration files.

2. **Discover project features** by reading source files to understand functionality.

3. **Identify usage patterns** by looking for CLI commands or example usage in code comments.

### Step 3: Generate README Sections

Create a well-structured README.md with the following sections (include only relevant ones):

#### Required Sections:

1. **Project Title** - A clear, descriptive title.
2. **Description** - What the project does and its main features.
3. **Installation** - Step-by-step setup instructions.
4. **Usage** - Minimal code example with expected output.
5. **License** - Specify the open source license.

#### Optional Sections (include if relevant):

- **Badges** - Build status, version, coverage (use shields.io).
- **Visuals** - Screenshots or GIFs if applicable.
- **Support** - Where to get help (issues, discussions).
- **Authors** - Credit contributors.

## Guidelines

- Keep it scannable: use headers, bullet points, and code blocks.
- Lead with the most important information.
- Show, don't tell: include a usage example.
- Assume the reader is unfamiliar with the project.
- Link to detailed documentation rather than duplicating content.

## Do Not Include

- Contributing guidelines (these belong in CONTRIBUTING.md).
- Roadmap or future plans.
- Verbose explanations.
- Redundant badges.