# Mirrord Skill Installation

## Structure
```
mirrord/
├── SKILL.md                    # Main skill instructions
└── references/
    ├── configuration.md        # Configuration reference (1805 lines)
    └── schema.json            # JSON Schema (3208 lines)
```

## Installation

1. Copy the entire `mirrord` directory to `/mnt/skills/user/` in your Claude environment
2. The skill will automatically appear in your available skills list
3. Claude will read the reference files when you ask mirrord-related questions

## Usage

Just ask Claude to:
- "Generate a mirrord config for pod X in namespace Y"
- "Validate my mirrord.json" (attach your config)
- "Help me configure mirrord to steal traffic on port 8080"

Claude will automatically load the schema and configuration references before responding.

## Changes from Original

✓ Removed vector DB/retrieval assumptions  
✓ Uses `view` tool to read references instead  
✓ Works with actual Claude skill architecture  
✓ Kept all operational guidance and quality requirements  
✓ Streamlined for clarity
