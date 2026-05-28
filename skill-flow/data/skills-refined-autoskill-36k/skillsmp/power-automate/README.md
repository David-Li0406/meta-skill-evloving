# Power Automate Skill for Claude Code

Build and deploy Microsoft Power Automate flows using natural language.

## Installation

In Claude Code:

1. Run `/plugin`
2. Select **marketplace**
3. Paste: `https://github.com/wtandler/power-automate-claude`

That's it!

## Prerequisites

1. **.NET SDK 6.0+**
   - Download: https://dotnet.microsoft.com/download

2. **PAC CLI**
   ```powershell
   dotnet tool install --global Microsoft.PowerApps.CLI.Tool
   ```

3. **Power Platform Access**
   - Microsoft 365 account with Power Platform license
   - Or Power Platform developer environment

## Usage

Once installed, just ask Claude:

- "Create a Power Automate flow that runs daily at 9am"
- "Build a flow with a button trigger that sends an email"
- "Deploy my flow to the dev environment"
- "Export flows from Power Platform"

## Authentication

First-time setup requires authentication:

```powershell
pac auth create --deviceCode
pac env list
pac org select --environment "YOUR-ENV-ID"
```

## What You Can Build

- **Scheduled flows** - Run on a timer (daily, weekly, etc.)
- **Button flows** - Triggered manually with input
- **HTTP flows** - Webhook endpoints
- **Connector flows** - SharePoint, Outlook, Teams triggers

## File Structure

```
.claude/skills/power-automate/
├── SKILL.md     # Main skill instructions (Claude reads this)
└── README.md    # This file (for humans)
```
