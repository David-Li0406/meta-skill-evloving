# Reducing Permission Prompts During Kyotee Execution

The goal of Kyotee is to front-load all decisions during Discovery and Planning phases, then let execution run unattended.

## The Kyotee Permission Model

```
┌─────────────────────────────────────────────────────────────────┐
│  DISCOVERY MODE (Interactive)                                    │
│  - User answers questions about project type, tech stack         │
│  - User reviews and approves spec                                │
│  - THIS is where human input happens                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  EXECUTE MODE (Autonomous)                                       │
│  - Context, Plan, Implement, Verify, Deliver                     │
│  - Should run without prompts                                    │
│  - Loop on failures automatically                                │
└─────────────────────────────────────────────────────────────────┘
```

## Configuring Claude Code for Autonomous Execution

### Option 1: Project-Level Allowlist (Recommended)

Create `.claude/settings.json` in your project:

```json
{
  "permissions": {
    "allow": [
      "Write(*)",
      "Edit(*)",
      "Bash(bun *)",
      "Bash(npm *)",
      "Bash(wrangler *)",
      "Bash(go *)",
      "Bash(tsc *)",
      "Bash(mkdir *)",
      "Bash(rm -rf node_modules)",
      "Bash(rm -rf .wrangler)"
    ]
  }
}
```

This allows:
- All file writes and edits
- Package manager commands
- Build/dev tooling
- Cleanup operations

### Option 2: Directory-Scoped Writes

More restrictive - only allow writes within project:

```json
{
  "permissions": {
    "allow": [
      "Write(./src/**)",
      "Write(./public/**)",
      "Write(./package.json)",
      "Write(./tsconfig.json)",
      "Write(./wrangler.toml)",
      "Write(./.kyotee/**)",
      "Edit(*)"
    ]
  }
}
```

### Option 3: Per-Tech-Stack Settings

Create settings based on your common tech stacks:

**For Cloudflare Workers projects:**
```json
{
  "permissions": {
    "allow": [
      "Write(*)",
      "Edit(*)",
      "Bash(bun *)",
      "Bash(wrangler *)",
      "Bash(tsc *)"
    ]
  }
}
```

**For Go projects:**
```json
{
  "permissions": {
    "allow": [
      "Write(*)",
      "Edit(*)",
      "Bash(go *)",
      "Bash(make *)"
    ]
  }
}
```

## How Kyotee Uses This

During execution:

1. **Context Phase** - Reads files (no prompts needed)
2. **Plan Phase** - Creates plan (no prompts needed)
3. **Implement Phase** - Writes files (allowlisted = no prompts)
4. **Verify Phase** - Runs build checks (allowlisted = no prompts)
5. **Deliver Phase** - Outputs summary (no prompts needed)

## Trust Boundary

The trust boundary is at **spec approval**:

```
User reviews spec → Approves → Execution begins
       ↑
  Trust boundary
```

Once you approve the spec, you're trusting Kyotee to:
- Write files matching the spec
- Run build/dev commands
- Loop on failures until success

## What Still Prompts

Even with allowlists, Claude Code will prompt for:

1. **Destructive operations** outside allowlist:
   - `rm -rf /` (blocked by default)
   - Writing to system paths

2. **Network operations** (if not allowlisted):
   - Installing unknown packages
   - Fetching from URLs

3. **Sensitive file access**:
   - Reading `.env` files
   - Accessing credentials

## Recommended Setup for Kyotee

Add to your `~/.claude/settings.json` (global) or project `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Write(*)",
      "Edit(*)",
      "Bash(bun *)",
      "Bash(npm *)",
      "Bash(npx *)",
      "Bash(pnpm *)",
      "Bash(yarn *)",
      "Bash(wrangler *)",
      "Bash(go *)",
      "Bash(cargo *)",
      "Bash(python *)",
      "Bash(pip *)",
      "Bash(tsc *)",
      "Bash(eslint *)",
      "Bash(prettier *)",
      "Bash(mkdir *)",
      "Bash(cp *)",
      "Bash(mv *)",
      "Bash(rm -rf node_modules)",
      "Bash(rm -rf .wrangler)",
      "Bash(rm -rf dist)",
      "Bash(rm -rf build)"
    ]
  }
}
```

## Summary

1. **Discovery Mode** = Interactive, user answers questions
2. **Plan Approval** = Trust boundary, user reviews spec
3. **Execute Mode** = Autonomous, runs with allowlisted permissions
4. **Configure allowlists** = Enable unattended execution

The goal: approve the spec, walk away, come back to working code.
