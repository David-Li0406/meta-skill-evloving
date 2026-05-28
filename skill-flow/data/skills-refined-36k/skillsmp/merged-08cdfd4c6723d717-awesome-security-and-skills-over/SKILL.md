---
name: awesome-security-and-skills-overview
description: Use this skill when contributing to curated resource lists for game security, Web3 security, and AI coding agent skills, ensuring high-quality, well-categorized, and non-duplicated entries.
---

# Awesome Security and Skills - Project Overview

## Purpose

This is a curated collection of resources related to game security, Web3 security, and AI coding agent skills. The project serves as a comprehensive reference for security researchers, game developers, pentesters, auditors, and AI enthusiasts.

## Project Structure

```
awesome-security-and-skills/
├── README.md                # Main resource list (curated)
├── LICENSE                  # License
└── ref/                     # Optional reference notes (not curated)
    ├── notes/               # Personal notes, drafts, checklists
    └── Crypto-resources/    # Reference lists (used for gap checks)
```

## README.md Format Convention

### Category Structure

Each category follows this format:

```markdown
## Category Name
> Subcategory (optional)
- https://github.com/user/repo [Brief description]
```

### Link Format

- Always use full URLs.
- Add brief descriptions in square brackets `[description]`.
- Use consistent spacing and formatting.
- Group related resources under subcategories with `>`.

### Example Entry

```markdown
## Game Security
> Cheat/Hacking
- https://github.com/example/cheat [Memory manipulation tool]

## Web3 Security
> Decompilers
- https://example.com/tool [EVM decompiler]
```

## Main Categories

1. **Game Development**: Engines, renderers, networking, physics
2. **Graphics APIs**: DirectX, OpenGL, Vulkan hooks and tools
3. **Cheat/Hacking**: Memory manipulation, injection, bypasses
4. **Anti-Cheat**: Protection systems, detection methods
5. **Reverse Engineering**: Debuggers, disassemblers, analysis tools
6. **Web3 Security**: Blockchain, smart contracts, DeFi
7. **Agent Skills**: Skills for AI coding agents like Claude, Codex, and Copilot

## Contribution Guidelines

1. **Check for duplicates** before adding new resources.
2. **Verify links** are working and point to original repositories.
3. **Add descriptions** that clearly explain the resource's purpose.
4. **Place in correct category** based on primary functionality.
5. **Follow existing format** for consistency.

## Quality Criteria

- Resource should be actively maintained or historically significant.
- Should provide unique value not covered by existing entries.
- Prefer original repositories over forks unless the fork adds significant value.
- Include language/platform tags when helpful (e.g., `[Rust]`, `[Unity]`).

## Duplicate Policy

**No duplicate URLs in README.md.** If a link fits multiple categories, pick the primary one.

## Contribution Checklist

1. Check for duplicates in `README.md` before adding.
2. Verify the link points to the canonical source (avoid low-value forks).
3. Keep the description English and useful.
4. Put it into the most appropriate category.
5. Prefer minimal changes over reformatting large sections.