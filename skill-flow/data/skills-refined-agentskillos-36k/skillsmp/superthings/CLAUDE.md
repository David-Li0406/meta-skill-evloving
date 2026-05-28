# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**SuperThings** is an intelligent Things 3 integration plugin that:
- Provides an MCP server for Things 3 task management
- Includes Claude Code commands for inbox triage and GTD workflows
- **Learns from your corrections** to improve title suggestions and project assignments over time

## Plugin Structure

```
SuperThings/
├── src/                    # MCP server TypeScript source
├── dist/                   # Compiled MCP server
├── commands/               # Claude Code slash commands
│   ├── thingsinbox.md     # Inbox triage with learning
│   └── gtd.md             # GTD workflow
├── data/                   # Learning data
│   ├── patterns.json      # Learned patterns
│   └── history.jsonl      # Correction history
├── SKILL.md               # Skill instructions for Claude
└── CLAUDE.md              # This file
```

## Learning System

The plugin learns from corrections made during inbox triage:
- **Title transforms**: Regex patterns for title rewrites
- **Project hints**: Keyword → project mappings with confidence
- **Exact overrides**: Specific title mappings

Patterns are stored in `data/patterns.json` and history in `data/history.jsonl`.

## Development Commands

### Build and Run
- `npm run build` - Compile TypeScript to JavaScript (output to `dist/`)
- `npm run dev` - Run TypeScript compiler in watch mode for development
- `npm start` - Run the compiled server from `dist/index.js`

### Code Quality
- `npm run lint` - Run ESLint on all TypeScript files in `src/`
- `npm run format` - Format code with Prettier

### Testing
- `npm test` - Run Jest test suite
- `npm run test:watch` - Run Jest in watch mode

## Architecture

### Technology Stack
- **Runtime**: Node.js with ES modules (`"type": "module"`)
- **Language**: TypeScript with strict mode enabled
- **MCP SDK**: `@modelcontextprotocol/sdk` for MCP server implementation
- **Validation**: Zod for schema validation
- **Testing**: Jest

### Project Structure
- `src/` - TypeScript source files (entry point will be `src/index.ts`)
- `dist/` - Compiled JavaScript output
- TypeScript targets ES2022 with Node16 module resolution

### TypeScript Configuration
The project uses strict TypeScript settings including:
- All strict checks enabled
- No unused locals/parameters allowed
- No implicit returns
- Consistent casing enforced

## MCP Server Context

This server is designed to provide secure integration between MCP-compatible tools and the Things 3 task management application. When implementing features, consider:
- Security implications of task data access
- MCP protocol compliance
- Proper error handling and validation using Zod schemas

## Testing Strategy

This project follows a pragmatic TDD (Test-Driven Development) approach:

### Testing Principles
1. **Write tests first** - Define expected behavior before implementation
2. **Avoid duplication** - Don't re-test Zod validations in integration tests (already covered in unit tests)
3. **Focus on behavior** - Test contracts and important edge cases, not implementation details
4. **Well-organized tests** - Separate unit from integration tests, use clear describe/it blocks
5. **Smart coverage** - Test critical paths and error cases, don't aim for 100% coverage

### What to Test
- **Unit tests**: Core logic, error handling, data transformations
- **Integration tests**: Tool orchestration, MCP protocol compliance, end-to-end flows
- **Mock appropriately**: Mock external dependencies (AppleScript execution, file system)

### What NOT to Test
- Zod schema validations in integration tests (trust unit tests)
- Trivial getters/setters or boilerplate code
- Every parameter combination (trust Zod validation)
- Implementation details that might change

### Example Approach
- `urlscheme.ts`: Test URL construction and auth handling, but not parameter validation
- `applescript.ts`: Test secure execution and parsing, mock actual execution
- Tool handlers: Test orchestration and responses, trust already-tested libraries

## Email Lookup Integration

When using SuperThings and a person is mentioned, automatically resolve their email address before proceeding.

### Auto-Trigger

Apply this workflow when:
- Todo involves contacting someone by name
- User mentions a person without providing their email
- Keywords appear: "email", "contact", "reach out", "follow up with", "send to"
- Any task that would benefit from having someone's email address

### Lookup Cascade

Always follow this order:

1. **Check Cache First**: Read `~/claudesync/data/email-cache.json` for existing entries (key format: `lowercase name|domain`)

2. **Gmail/Contacts Search**: Use `mcp__zapier__gmail_find_email` with the person's name

3. **Hunter API**: If Gmail doesn't find the email, use Hunter MCP server:
   - Infer the company domain from context
   - Use Hunter to find email by name + domain
   - Verify the email if needed

4. **Ask User**: If all lookups fail, ask for the email address

### Domain Inference

Infer company domain from context clues:

| Context | Inferred Domain |
|---------|-----------------|
| "John at Acme Corp" | acme.com, acmecorp.com |
| "Sarah from Google" | google.com |
| Company mentioned in conversation | that company's domain |
| LinkedIn profile visible | company from profile |

Try common patterns: `company.com`, `companyinc.com`, `thecompany.com`, `company.io`

### Caching Results

After finding an email, update `~/claudesync/data/email-cache.json`:

```json
{
  "contacts": {
    "john smith|acme": {
      "email": "john.smith@acme.com",
      "source": "hunter",
      "found": "2025-01-01",
      "verified": true
    }
  }
}
```

### Example Flow

**User says:** "Create a todo to email John Smith at Acme about the proposal"

1. Check cache for `john smith|acme` → not found
2. Gmail search for "John Smith" → no matching contacts
3. Hunter: find email for "John Smith" at "acme.com" → `john.smith@acme.com`
4. Update cache with new entry
5. Create todo: "Email John Smith about the proposal" with `john.smith@acme.com` in notes

### Tool Reference

- **Gmail**: `mcp__zapier__gmail_find_email` with query containing person name
- **Hunter**: Use Hunter MCP tools to find/verify emails by name + domain
- **Cache**: `~/claudesync/data/email-cache.json` (syncs via GitHub)