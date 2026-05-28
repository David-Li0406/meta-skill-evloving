# Setup Guide

Complete guide to setting up the Multi-Repo Workspace skill.

## Prerequisites

- Claude.ai account or Claude API access
- Multiple repositories in a workspace
- Basic understanding of your project structure

---

## Installation Methods

### Method 1: Claude Projects (Recommended)

**Best for**: Teams, long-term projects, persistent context

1. **Create a new Project**
   - Go to [Claude.ai](https://claude.ai)
   - Click "Projects" in the sidebar
   - Click "Create Project"
   - Name it (e.g., "My Workspace")

2. **Add the skill**
   - Open your project
   - Click "Project Knowledge"
   - Click "Add content"
   - Copy content from `skill.md`
   - Paste and save

3. **Start using**
   ```
   @workspace init my-project
   ```

**Pros**:
- Persistent across conversations
- Shared with team members
- Can add additional context files
- Best performance

**Cons**:
- Requires Claude Projects access
- Limited to Claude.ai web interface

---

### Method 2: Custom Instructions

**Best for**: Personal use, always-on behavior

1. **Open Settings**
   - Go to [Claude.ai](https://claude.ai)
   - Click Settings ⚙️
   - Select "Personalization"
   - Click "Custom Instructions"

2. **Add instructions**
   - Copy content from `custom-instructions.md`
   - Paste into the text area
   - Click "Save"

3. **Start using**
   - The skill is now active in all conversations
   ```
   @workspace init my-project
   ```

**Pros**:
- Always available
- Works in all conversations
- No project setup needed

**Cons**:
- Limited space (shorter version)
- Can't share with team
- Affects all conversations

---

### Method 3: Direct Prompt

**Best for**: One-time use, testing, API usage

1. **Copy the prompt**
   - Open `prompt.md`
   - Copy entire content

2. **Start conversation**
   - Paste at the beginning of your conversation
   - Continue with your commands

3. **Use the skill**
   ```
   @workspace init my-project
   ```

**Pros**:
- No setup required
- Works with API
- Full control over content

**Cons**:
- Must paste every conversation
- Takes up context space
- Not persistent

---

## Configuring Your Repositories

### Step 1: Create Configuration Directory

In each repository, create a `.claude` directory:

```bash
cd your-repo
mkdir .claude
```

### Step 2: Add Configuration File

Create `.claude/config.json`:

```bash
touch .claude/config.json
```

Use the template from `templates/.claude/config.json` as a starting point.

**Minimal configuration**:
```json
{
  "repository": {
    "name": "my-repo",
    "type": "frontend",
    "tech_stack": ["react", "typescript"]
  }
}
```

**Full configuration**:
See `templates/.claude/config.json` for all available options.

### Step 3: Add Context File

Create `.claude/context.md`:

```bash
touch .claude/context.md
```

Document:
- Repository purpose
- Architecture decisions
- Dependencies
- Common patterns
- Known issues

Use the template from `templates/.claude/context.md`.

### Step 4: Commit Configuration

```bash
git add .claude/
git commit -m "Add Claude workspace configuration"
```

---

## Workspace Setup

### Option A: Automatic Detection

Let Claude detect your workspace structure:

```
@workspace init my-workspace
```

Claude will ask for:
1. Base path of your workspace
2. Repositories to include

### Option B: Manual Configuration

Create `.workspace/config.json` in your workspace root:

```json
{
  "workspace": {
    "name": "my-workspace",
    "base_path": "/path/to/workspace"
  },
  "repositories": [
    {
      "name": "frontend",
      "path": "./frontend",
      "type": "frontend"
    },
    {
      "name": "backend",
      "path": "./backend",
      "type": "backend"
    }
  ]
}
```

---

## Verification

### Test the Setup

1. **Initialize workspace**
   ```
   @workspace init test-workspace
   ```

2. **Analyze workspace**
   ```
   @workspace analyze
   ```

   You should see:
   - List of detected repositories
   - Tech stacks
   - Dependencies
   - Configuration status

3. **Focus on a repo**
   ```
   @workspace focus frontend
   ```

   Claude should load the specific context for that repository.

4. **Try a task**
   ```
   @workspace task "Add a new API endpoint"
   ```

   Claude should identify affected repositories and propose coordinated changes.

---

## Troubleshooting

### Claude doesn't recognize @workspace commands

**Solution**: Verify the skill is properly installed
- For Projects: Check "Project Knowledge"
- For Custom Instructions: Check Settings → Personalization
- For Direct Prompt: Ensure you pasted the full prompt

### Configuration not detected

**Solution**: Check file locations
```bash
# Should exist:
your-repo/.claude/config.json
your-repo/.claude/context.md
```

Verify JSON syntax:
```bash
cat .claude/config.json | jq .
```

### Wrong repository type detected

**Solution**: Explicitly set type in config.json
```json
{
  "repository": {
    "type": "frontend"
  }
}
```

### Dependencies not recognized

**Solution**: Add to config.json
```json
{
  "dependencies": {
    "internal": ["@workspace/shared"],
    "external_critical": ["react"]
  }
}
```

---

## Best Practices

### 1. Keep Configuration Updated

Update `.claude/config.json` when you:
- Change tech stack
- Add/remove dependencies
- Change conventions
- Update development commands

### 2. Document Decisions

Use `.claude/context.md` to document:
- Why certain patterns were chosen
- Trade-offs made
- Future improvements planned
- Known limitations

### 3. Version Control

Always commit configuration files:
```bash
git add .claude/
git commit -m "Update Claude configuration"
```

### 4. Team Alignment

Ensure team members:
- Understand the configuration
- Keep it updated
- Use consistent conventions

### 5. Regular Analysis

Run `@workspace analyze` regularly to:
- Detect inconsistencies
- Find outdated dependencies
- Identify technical debt

---

## Next Steps

1. ✅ Install the skill
2. ✅ Configure your repositories
3. ✅ Set up workspace
4. ✅ Verify setup
5. 📖 Read [Commands Reference](./commands.md)
6. 📖 Read [Best Practices](./best-practices.md)
7. 🚀 Start using the skill!

---

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/llm-skills/issues)
- **Examples**: Check `examples/` directory
- **Templates**: Use files in `templates/` directory
