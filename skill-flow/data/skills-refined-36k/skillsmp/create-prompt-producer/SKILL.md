---
name: create-prompt-producer
description: Create the definition files for the Renku Prompt Producer, which leverages an LLM to generate high-quality, structured prompts or audio narration texts consumed by downstream media generation models within the Renku video-creation blueprint.
allowed-tools: Read, Grep, Glob, AskUserQuestion
---

# Prompt Producer Creation Skill

This skill helps you create the necessary files to define a prompt producer. Prompt producers are used generally in the first stage of a Renku blueprint (workflow definition for generating videos). They create the required prompts, narrative texts etc. for the downstream media generators using an LLM of user's choice automatically based on the user requirements provided as inputs. 

## Prerequisites

Before creating blueprints, ensure Renku is initialized:

1. Check if `~/.config/renku/cli-config.json` exists
2. If not, run `renku init --root=~/renku-workspace` 
3. The config file contains the `catalog` path where blueprints and producers are installed

Read `~/.config/renku/cli-config.json` to find the **catalog** path, you will be using this to locate the producers and models for the blueprint.

```bash
cat ~/.config/renku/cli-config.json
```

## How to Create

### Step 1: Requirements
