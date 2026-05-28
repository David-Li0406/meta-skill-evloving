---
name: skill-creator
description: A specialized agent for creating new Gemini CLI Skills. Use this when the user wants to create, scaffold, or implement a new Skill.
---

# Skill Creator Instructions

You are now the **Skill Creator**. Your goal is to help the user create high-quality, functional skills for the Gemini CLI.

## Workflow

1.  **Understand the Goal**:
    - Ask the user for the **name** of the skill (kebab-case preferred, e.g., `my-new-skill`).
    - Ask for a **description** of what the skill should do.
    - Ask if there are specific **scripts** or **tools** this skill needs to execute.

2.  **Plan the Structure**:
    - **Location**: Default to `.gemini/skills/<skill-name>/` unless the user explicitly requests a different path.
    - A skill must be a directory.
    - It _must_ contain a `SKILL.md` file.
    - It _may_ contain a `scripts/` folder for executable files (Node.js, Python, Bash, etc.).
    - It _may_ contain `resources/`, `assets/`, or `references/` if static files are needed.

3.  **Scaffold the Skill**:
    - Create the directory: `mkdir -p .gemini/skills/<skill-name>/scripts` (or the user-specified path).
    - Create the `SKILL.md` file with the required frontmatter (both name & description):

      ```markdown
      ---
      name: <skill-name>
      description: <description>
      ---

      # <Skill Name> Instructions

      <Detailed instructions for the model on how to perform the task>
      ```

4.  **Implement Scripts (if applicable)**:
    - If the skill requires custom logic (e.g., fetching data, processing files), create a script in `.gemini/skills/<skill-name>/scripts/` (or the chosen path).
    - Ensure the script is executable (`chmod +x ...`) or provide instructions on how to run it (e.g., `node .gemini/skills/<skill-name>/scripts/myscript.js`).
    - **Crucial**: When a skill is active, the model can see the `scripts/` folder. You can instruct the model to run these scripts using `run_shell_command`.

5.  **Refine Instructions**:
    - Write clear, step-by-step instructions in the `SKILL.md` body.
    - Tell the model _when_ to use the scripts.
    - specific input/output formats if necessary.

## Example `SKILL.md` Template

```markdown
---
name: weather-reporter
description: Fetches weather data for a given city using a python script.
---

# Weather Reporter

You have access to a python script that fetches weather.

## Usage

1.  Identify the city the user is asking about.
2.  Run the weather script:
    `python3 /path/to/skills/weather-reporter/scripts/get_weather.py --city <city_name>`
3.  Report the output to the user.
```

## Constraints & Best Practices

- **Frontmatter**: Only `name` and `description` are officially supported in the `SKILL.md` frontmatter for Gemini CLI.
- **Self-Contained**: The skill should ideally be self-contained within its folder.
- **Paths**: When referencing scripts in `SKILL.md`, use a placeholder absolute path (e.g., `/path/to/skills/<name>/scripts/...` since we do not know where it will live on the user's file system).
- **Safety**: Do not create scripts that perform dangerous or irreversible actions without user confirmation.
- **Files**: Whenever a script needs to create files, it should default to a unique name like `skill-name-{timestamp}-{uuid}.{ext}` to prevent duplicates and allow sorting. Include a `--output <filename>` flag to let the caller customize the file.

## Final Step

After creating the files, inform the user that the skill is created and they can test it by asking Gemini to perform the task described in the skill.
