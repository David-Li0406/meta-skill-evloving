# AI Agent References

Complete documentation for the AI system implemented in Wellness-Link using VoltAgent framework.

## Documentation Index

### Core Framework

**[VoltAgent Guide](../../../docs/ai-voltagent-guide.md)**
- Complete guide to VoltAgent framework
- Core concepts: Agent, Tools, Memory, SubAgents
- Workflows, Guardrails, Hooks
- RAG capabilities and Observability
- 80+ LLM providers supported

### Implementation References

**[AI Tools Reference](../../../docs/ai-tools-reference.md)**
- Catalog of 10+ implemented tools
- Tool creation patterns with `createTool()`
- Categories: Patient, Services, Appointments, FAQ, Payments, WhatsApp
- Best practices and examples

**[AI Agent Reference](../../../docs/ai-agent-reference.md)**
- Architecture of the medical chat agent
- Configuration (MiniMax M2.1, temperature, maxSteps)
- LibSQL memory system
- Context management
- Structured response parser
- API routes (chat, stream, escalate)

**[AI UI Reference](../../../docs/ai-ui-reference.md)**
- Part-based UI system
- 8 part types: text, services-list, availability, reservation, faq, calendar, patient-form, confirmation
- Factory pattern (MessageRenderer, PartRenderer)
- Handler callbacks for interactivity
- Chat widget system

**[AI Patterns Guide](../../../docs/ai-patterns.md)**
- Step-by-step: Add a new tool
- Step-by-step: Add a new UI part
- Frontend-backend integration
- Practical examples
- Troubleshooting

## Quick Start

### For Backend Development

1. Read **[VoltAgent Guide](../../../docs/ai-voltagent-guide.md)** for framework concepts
2. Read **[AI Tools Reference](../../../docs/ai-tools-reference.md)** for tool patterns
3. Reference **[AI Agent Reference](../../../docs/ai-agent-reference.md)** for architecture

### For Frontend Development

1. Read **[AI UI Reference](../../../docs/ai-ui-reference.md)** for part system
2. Reference **[AI Patterns Guide](../../../docs/ai-patterns.md)** for adding new parts

### For Extending the System

1. **Add a tool**: Follow [AI Tools Reference → Tool Creation](../../../docs/ai-tools-reference.md#patrón-de-creación-de-tools)
2. **Add a UI part**: Follow [AI Patterns Guide → Agregar Nueva Parte UI](../../../docs/ai-patterns.md#agregar-una-nueva-parte-ui)
3. **Integration**: See [AI Patterns Guide → Integración](../../../docs/ai-patterns.md#integración-frontend-backend)

## File Locations

### Backend (packages/api)
```
src/services/ai/chat/
├── agent.ts              # Agent factory & singleton
├── config.ts             # Configuration & prompts
├── parser.ts             # Structured response parser
├── schema.ts             # Zod schemas
├── memory/config.ts      # LibSQL memory
└── tools/                # Tool implementations
    ├── patient.ts
    ├── services.ts
    ├── appointments.ts
    ├── faq.ts
    ├── payment-methods.ts
    ├── whatsapp-context.ts
    └── pause-for-human.ts
```

### Frontend (packages/web)
```
src/components/ai-ui/
├── types.ts              # TypeScript interfaces
├── factory.tsx           # MessageRenderer & PartRenderer
├── text-part.tsx
├── services-part.tsx
├── availability-part.tsx
├── reservation-part.tsx
├── faq-part.tsx
├── calendar-part.tsx
├── patient-form-part.tsx
└── confirmation-part.tsx
```

## Key Technologies

| Layer | Technology |
|-------|-----------|
| **AI Framework** | [@voltagent/core](https://voltagent.dev) v2.1.6 |
| **Memory** | [@voltagent/libsql](https://voltagent.dev) v2.0.3 |
| **AI SDK** | [Vercel AI SDK](https://sdk.vercel.ai) v6.0.26 |
| **Provider** | MiniMax M2.1 (Anthropic-compatible) |
| **Validation** | Zod v4.1.13 |
| **Frontend** | React 19 + Tailwind v4 + shadcn/ui |
| **Backend** | Bun + Elysia + Drizzle ORM |

## Related Skills

- **[link](../SKILL.md)** - Full-stack monorepo expert
- See [Web Agent](web-agent.md) for frontend patterns
- See [API Agent](api-agent.md) for backend patterns
