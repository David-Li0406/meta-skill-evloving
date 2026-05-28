---
name: remote-work
description: Use this skill when you want to execute tasks on remote Azure VMs with automatic region and resource selection.
---

# Remote Work Skill

Execute amplihack tasks on remote Azure VMs using the `/amplihack:remote` command.

## When to Use

Use this skill when you want to:
- Run long-running tasks on remote VMs
- Leverage more powerful Azure compute
- Distribute work across multiple machines
- Isolate experimental or risky work
- Work in specific Azure regions

## How It Works

When you say things like:
- "Run this remotely"
- "Execute on an eastus VM"
- "Offload this to Azure"
- "Use a remote machine for this"

I will:
1. Extract your task description.
2. Detect region preferences (if mentioned).
3. Recommend appropriate VM size based on task complexity.
4. Execute `/amplihack:remote` with proper options.
5. Guide you on accessing results.

## Region Detection

I automatically detect Azure regions from your request:
- "eastus", "east us" → --region eastus
- "westus", "west us" → --region westus
- "centralus" → --region centralus
- (and other Azure regions)

## VM Size Recommendations

Based on your task complexity keywords:

**Small (size s)**: Quick analysis, simple fixes
- Keywords: "quick", "simple", "small", "analyze"
- Size: s (8GB RAM)

**Medium (size m)**: Standard development work
- Keywords: "implement", "feature", "refactor"
- Size: m (64GB RAM) - **default**

**Large (size l)**: Complex refactoring, large codebases
- Keywords: "large", "comprehensive", "complex", "entire codebase"
- Size: l (128GB RAM)

**Extra Large (size xl)**: Intensive compute tasks
- Keywords: "intensive", "heavy", "massive"
- Size: xl (256GB RAM)

## Instructions

When activated:

1. **Parse the user's request** to extract:
   - The task description
   - Region preference (if mentioned)
   - Complexity hints for VM sizing

2. **Determine VM size** based on keywords:
   - Default to "m" unless keywords suggest otherwise
   - Use "s" for simple/quick tasks
   - Use "l" for large/complex tasks
   - Use "xl" for intensive/massive tasks

3. **Construct the command**:
   ```
   /amplihack:remote --region {region} --vm-size {size} auto "{task}"
   ```
   If no region is mentioned, omit --region (uses azlin default).

4. **Execute the command** using the SlashCommand tool.

5. **Guide the user** on next steps:
   - Results will be provided based on the execution.