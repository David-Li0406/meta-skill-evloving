# Skill Creator Pro

**Enhanced version** of Anthropic's official `julien-dev-tools-skill-creator` with comprehensive Skill Chaining documentation.

## 🆕 What's New in Pro Version

### Major Addition: Skill Chaining Framework

The Pro version adds a **complete documentation framework** for describing how skills interact with each other:

#### 8-Part Skill Chaining Documentation

1. **Skills Required Before** - Prerequisites with priority levels (obligatoire/recommandé/optionnel)
2. **Input Expected** - Precise format, environment, configuration requirements
3. **Output Produced** - Format, side effects, estimated duration
4. **Compatible Skills After** - What skills can/should follow
5. **Called By** - Parent skills, Git hooks, direct invocation scenarios
6. **Tools Used** - Claude Code tools with usage descriptions
7. **Visual Workflow** - ASCII diagrams showing skill position in workflow
8. **Usage Example** - Concrete real-world scenarios

### Why This Matters

**Without Skill Chaining documentation:**
- ❌ Users don't know which skill to use next
- ❌ Skills appear isolated, not part of workflows
- ❌ Debugging issues between skills is difficult
- ❌ Onboarding requires understanding each skill in isolation

**With Skill Chaining documentation:**
- ✅ **Discoverability**: Users/Claude know next steps
- ✅ **Workflow clarity**: Shows how skills connect
- ✅ **Bidirectional docs**: If A calls B, both mention each other
- ✅ **Debugging**: Clear Input/Output helps diagnose issues
- ✅ **Onboarding**: Understand complete workflows

## 📊 Comparison

| Feature | skill-creator (Anthropic) | skill-creator | Difference |
|---------|--------------------------|-------------------|------------|
| Basic skill structure | ✓ | ✓ | Same |
| Progressive disclosure | ✓ | ✓ | Same |
| Quality rubric (9 dimensions) | ✓ | ✓ | Same |
| Iterative improvement process | ✓ | ✓ | Same |
| **Skill Chaining documentation** | ❌ | ✅ | **NEW** |
| Input/Output specs | ❌ | ✅ | **NEW** |
| Visual workflows (ASCII) | ❌ | ✅ | **NEW** |
| Git hooks integration | ❌ | ✅ | **NEW** |
| Tools Used documentation | ❌ | ✅ | **NEW** |
| Real-world workflow examples | ❌ | ✅ | **NEW** |

## 📝 Example: Skill Chaining Section

```markdown
## 🔗 Skill Chaining

### Skills Required Before
- **local-testing** (recommandé): Validates code locally before deployment

### Input Expected
- Git branch ready to deploy: `main` or `staging`
- Code validated via **local-testing**: build succeeded
- SSH access configured: `automation@example.com`

### Output Produced
- **Format**: Application deployed and running on VPS
- **Side effects**: PM2 process restarted, new Git commit checked out
- **Duration**: 2-3 minutes

### Compatible Skills After
**Recommandés:**
- **accessibility-audit**: Check WCAG compliance
- **performance-monitoring**: Lighthouse scores

### Called By
- **git-workflow-manager**: Complete deployment workflows
- **post-push.sh hook**: Auto-deployment after git push
- Direct user invocation: Manual deployment

### Tools Used
- `Bash` (usage: rsync files, ssh commands, pm2 restart)
- `Read` (usage: verify config files exist)

### Visual Workflow
\`\`\`
User: git push origin staging
    ↓
pre-push.sh hook (validation)
    ↓
deployment-manager (this skill)
    ├─► rsync local → VPS
    ├─► npm install --production
    ├─► npm run build
    └─► pm2 restart app
    ↓
Site deployed
    ↓
[Optional next steps]
    └─► accessibility-audit
\`\`\`

### Usage Example
**Scenario**: Deploy feature to preview environment
**Command**: `git push origin staging`
**Result**: Site updated on https://preview.example.com in ~2-3 min
```

## 🎯 When to Use skill-creator vs skill-creator

### Use skill-creator when:
- ✅ Creating skills that are part of larger workflows
- ✅ Skills that interact with other skills
- ✅ Skills triggered by Git hooks or automation
- ✅ Complex workflows requiring multiple steps
- ✅ Skills used in team environments (documentation critical)

### Use skill-creator (Anthropic official) when:
- ✅ Creating simple, isolated skills
- ✅ Following official Anthropic guidelines exactly
- ✅ Contributing back to Anthropic repository
- ✅ Learning basic skill creation

## 🚀 Getting Started

1. **Read SKILL.md** for complete guide
2. **Initialize a new skill** using the workflow in Step 3
3. **Follow Step 4** to document your skill
4. **Add Skill Chaining section** (critical for workflow skills)
5. **Iterate** using the quality rubric in Step 6

## 📦 Scripts

The Anthropic skills repository includes helper scripts:
- `init_skill.py` - Generate skill template
- `package_skill.py` - Validate and package skill

To use these scripts:
```bash
# Clone Anthropic skills repo
git clone https://github.com/anthropics/skills
cd skills

# Initialize new skill
python scripts/init_skill.py my-new-skill --path ../my-marketplace/skills/

# Package after completion
python scripts/package_skill.py ../my-marketplace/skills/my-new-skill
```

## 🤝 Contributing

This enhanced version could be valuable to the broader Claude community. Consider:
- Using it in your own marketplace
- Proposing the Skill Chaining framework to Anthropic
- Sharing examples of well-documented skill chains

## 📄 License

Apache-2.0 (based on Anthropic's skill-creator)

## 🙏 Attribution

Based on the official `julien-dev-tools-skill-creator` from [Anthropic Skills Repository](https://github.com/anthropics/skills).

Enhanced with Skill Chaining documentation framework by Julien.
