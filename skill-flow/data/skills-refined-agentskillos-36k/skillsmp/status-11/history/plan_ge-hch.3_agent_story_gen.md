Plan: Agent story generation + Discord telemetry emitter

Created features/tasks:
- ge-hch.5.1 Agent: Story Author (Ink)
  - ge-hch.5.1.1 Docs: Agent spec (Story Author)
  - ge-hch.5.1.2 Implement: Story Author harness
  - ge-hch.5.1.3 Tests: Generated story validation
- ge-hch.3.1 Implement: Telemetry Discord emitter (webhook)
- ge-hch.5.2 Secure: Telemetry webhook secret storage

Decisions made:
- Static demo will be deployed to GitHub Pages (no file:// runs).
- LLM provider: OpenAI-compatible endpoint; agent must support configurable endpoint.
- Telemetry will POST Discord rich embeds to provided webhook (initially unsecured). A follow-up bead (ge-hch.5.2) tracks securing it.

Files referenced/created by this plan:
- history/plan_ge-hch.3_agent_story_gen.md (this file)
- history/ai/agent-story-author.md (spec task will create)
- web/stories/generated/ (target for generated stories)

Open Questions:
- LLM credentials: will use online authentication (GitHub Copilot + OpenAI compatible endpoint). Confirm CI secret names: OPENAI_API_KEY, TELEMETRY_WEBHOOK.
- Discord webhook message embeds: format designed by Build; confirm if additional fields required.
