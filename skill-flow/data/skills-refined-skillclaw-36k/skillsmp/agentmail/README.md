# AgentMail Claude Skill

A Claude Skill that teaches Claude how to build email agents using the AgentMail API.

## What is a Claude Skill?

A Claude Skill is a "skill pack" that helps Claude learn to use specific APIs/tools. The core is a `SKILL.md` file containing essential information, best practices, and code examples.

## Structure

```
agentmail-claude-skill/
├── SKILL.md              # Core skill file (~400 lines)
└── references/
    ├── api-reference.md  # Complete API method signatures
    ├── webhook-events.md # Webhook event types and payloads
    └── examples.md       # Advanced agent patterns
```

## What's Included

### SKILL.md
- Quick start (installation, initialization, first email)
- Resource hierarchy (Organization → Pod → Inbox → Thread → Message)
- Common workflows (send, reply, webhooks, websockets)
- AI agent integration (agentmail-toolkit)
- Best practices (idempotency, deliverability)
- Critical gotchas

### references/api-reference.md
- All methods for: Inboxes, Messages, Threads, Webhooks, WebSockets, Domains, Pods, Drafts, API Keys, Metrics, Organizations
- Parameter types and return values
- Error types

### references/webhook-events.md
- All 7 event types with full payload examples
- `message.received`, `message.sent`, `message.delivered`, `message.bounced`, `message.complained`, `message.rejected`, `domain.verified`

### references/examples.md
- Event-driven agent (Flask + ngrok)
- WebSocket real-time agent
- Multi-step workflow with state
- Human-in-the-loop with drafts
- Label-based workflow
- Multi-tenant with pods
- Attachment processing
- TypeScript examples

## Installation

### For Personal Use
Copy the skill to your Cursor skills directory:

```bash
cp -r agentmail-claude-skill ~/.cursor/skills/agentmail
```

### For Project Use
Copy to your project's `.cursor/skills/` directory:

```bash
cp -r agentmail-claude-skill .cursor/skills/agentmail
```

## Usage

Once installed, Claude will automatically use this skill when:
- Building email automation
- Creating AI email agents
- Setting up webhooks for email notifications
- Integrating email into AI workflows
- Working with AgentMail, inboxes, or email agents

## Resources

- [AgentMail Documentation](https://docs.agentmail.to)
- [AgentMail Console](https://console.agentmail.to)
- [Python SDK](https://pypi.org/project/agentmail/)
- [Node.js SDK](https://www.npmjs.com/package/agentmail)

## License

MIT
