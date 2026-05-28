# Docusaurus Expert Claude Skill

A production-ready Claude Skill for building fast, SEO-optimized static sites with Docusaurus v3.9.2.

## What is a Claude Skill?

Claude Skills are modular packages of instructions, executable code, and resources that extend Claude's capabilities with domain-specific expertise. This Skill equips Claude with specialized knowledge about Docusaurus, enabling it to help you:

- **Setup** Docusaurus projects from scratch
- **Optimize** content for search engines (SEO)
- **Configure** plugins for sitemaps, image optimization, analytics, and PWAs
- **Deploy** to GitHub Pages with best practices
- **Debug** build issues and performance problems
- **Author** Markdown/MDX docs with proper frontmatter for social sharing

## How to Use

### Option 1: Claude.ai (Web)
1. Go to [claude.ai](https://claude.ai/) → Settings → Features → Skills
2. Upload the `docusaurus-expert` folder as a zip file
3. In any conversation, ask Claude about Docusaurus and it will use the skill automatically

### Option 2: Claude API (Python)
```python
from anthropic import Anthropic

client = Anthropic(
    default_headers={
        "anthropic-beta": "skills-2025-10-02,code-execution-2025-08-25,files-api-2025-04-14"
    }
)

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    container={
        "skills": [
            {"type": "custom", "skill_id": "docusaurus-expert"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{
        "role": "user",
        "content": "Set up a Docusaurus site with SEO plugins and deploy to GitHub Pages"
    }]
)
```

### Option 3: Claude Code
1. Place the `docusaurus-expert` folder in `.claude/skills/` of your project
2. Claude will discover and use it automatically in conversations

## Skill Contents

### SKILL.md
The main skill file containing:
- **Metadata**: Name and description for discovery
- **Core expertise**: Content pipeline, SEO strategy, plugin architecture, deployment
- **Mental models**: Key concepts for understanding Docusaurus
- **Actionable workflows**: Day 0 to Week 2 progression
- **20% features for 80% results**: Minimal but impactful optimizations
- **Common pitfalls**: Issues and fixes
- **Debugging tips**: Tools and commands for troubleshooting
- **Template patterns**: Copy-paste ready examples
- **Glossary**: Key terms explained
- **Quick reference**: Commands and configurations
- **When to use**: Docusaurus vs. alternatives (Hugo, MkDocs, Next.js, Astro)
- **Resources**: Links to official documentation

## Key Features

### Coverage (~1200 words)
- ✅ Complete setup (Node.js 18+, npm/yarn)
- ✅ Production-ready patterns
- ✅ SEO optimization (metadata, sitemaps, social cards)
- ✅ Plugin configuration (sitemap, ideal-image, analytics, PWA)
- ✅ GitHub Pages deployment
- ✅ Markdown/MDX authoring
- ✅ Common pitfalls and fixes
- ✅ Debugging and observability
- ✅ Real-world use cases

### Progressive Disclosure Architecture
Claude loads information on-demand:
1. **Startup**: Skill metadata pre-loaded
2. **Trigger**: When you ask about Docusaurus, Claude reads SKILL.md
3. **Access**: If you ask about specific topics, Claude reads relevant sections
4. **Execute**: Claude can run code examples (with code execution enabled)

## Compatibility

| Platform | Support | Notes |
|----------|---------|-------|
| Claude.ai | ✅ Yes | Upload zip file via Settings → Skills |
| Claude API | ✅ Yes | Requires beta headers (see example above) |
| Claude Code | ✅ Yes | Place in `.claude/skills/` directory |
| Claude Agent SDK | ✅ Yes | Filesystem-based discovery |

## Requirements

### For Using the Skill
- Claude subscription or Claude API key
- Code execution enabled (optional but recommended)
- Files API enabled (optional, for uploading/downloading generated files)

### For Running Example Commands
- Node.js 18+ or higher
- Yarn or npm
- Git

## Example Prompts

Try asking Claude about:

- "Set up a Docusaurus site with complete SEO configuration for an API reference"
- "How do I add the ideal-image plugin and optimize all my blog post images?"
- "Deploy my Docusaurus docs to GitHub Pages with a custom domain"
- "Debug my sitemap generation and add social meta tags to all pages"
- "Create a versioned documentation setup with Docusaurus"
- "What's the difference between Docusaurus and Hugo for my documentation site?"
- "Generate a production-ready docusaurus.config.ts with analytics and PWA"
- "How do I create MDX components in Docusaurus?"

## Skill Structure

```
docusaurus-expert/
├── SKILL.md          # Main skill file with instructions and guidance
└── README.md         # This file
```

## Security

This skill:
- ✅ Contains only instructions and best practices (no malicious code)
- ✅ Does not make external API calls
- ✅ Does not access your files without permission
- ✅ Does not require any sensitive credentials
- ✅ Is safe for production use

## Supported Versions

- **Docusaurus**: v3.9.2 (latest stable)
- **Node.js**: 18.x, 20.x, 22.x+
- **Claude**: Claude Sonnet 4.5 and later

## Resources

- 📖 [Docusaurus Official Docs](https://docusaurus.io/docs)
- 🚀 [Claude Skills Documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- 🔧 [Claude API Reference](https://platform.claude.com/docs/en/api/overview)
- 📚 [Claude Cookbook: Skills](https://github.com/anthropics/claude-cookbooks/tree/main/skills)

## Issues & Feedback

This skill is designed for intermediate developers with:
- ✅ Basic JavaScript/Node.js knowledge
- ✅ Git and GitHub familiarity
- ✅ Understanding of Markdown basics
- ✅ Some React knowledge (helpful, not required)

For questions or improvements, refer to the official Docusaurus and Claude documentation resources above.

## License

This Claude Skill is provided as-is for use with Claude.

---

**Ready to build fast, SEO-rich documentation?** Upload this skill and ask Claude to help you set up your Docusaurus site!
