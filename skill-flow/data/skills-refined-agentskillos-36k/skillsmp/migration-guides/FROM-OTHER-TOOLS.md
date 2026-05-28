# Migrating from Other AI Tools

Detailed migration guides for moving from popular AI coding assistants to Claude Code.

## From GitHub Copilot

### Overview

GitHub Copilot is an autocomplete-focused tool integrated into IDEs. Claude Code operates differently as an agentic CLI tool.

### Key Differences

| Aspect | Copilot | Claude Code |
|--------|---------|-------------|
| Paradigm | Autocomplete + Chat | Agentic CLI |
| Context | Current file + neighbors | Full project |
| Execution | Suggestions only | Full tool use |
| Integration | IDE plugin | Terminal + IDE |
| Customization | Limited | CLAUDE.md, hooks, MCP |

### What You Lose

- **Inline autocomplete**: Claude Code doesn't provide keystroke-by-keystroke suggestions
- **Ghost text**: No grayed-out completions as you type
- **Tab completion**: No single-key acceptance of suggestions

### What You Gain

- **Multi-file operations**: Edit many files in one request
- **Agentic execution**: Claude plans and executes complex tasks
- **Deep customization**: Hooks, skills, MCP servers
- **Better context**: Project-wide understanding
- **Git integration**: Native commit, PR workflows

### Migration Steps

1. **Keep Copilot for autocomplete** (optional)
   - Claude Code and Copilot can coexist
   - Use Copilot for line completions
   - Use Claude Code for larger tasks

2. **Migrate Copilot instructions**

   **From** `.github/copilot-instructions.md`:
   ```markdown
   Always use TypeScript.
   Prefer functional components.
   Use async/await over promises.
   ```

   **To** `CLAUDE.md`:
   ```markdown
   # Project Guidelines

   ## Code Style
   - Always use TypeScript
   - Prefer functional components
   - Use async/await over promises
   ```

3. **Translate common workflows**

   | Copilot Action | Claude Code Command |
   |---------------|---------------------|
   | `/explain` selection | `claude "explain [file:line-range]"` |
   | `/fix` error | `claude "fix the error in [file]"` |
   | `/tests` for function | `claude "write tests for [function]"` |
   | `/doc` for code | `claude "add documentation to [file]"` |

4. **Set up equivalent automation**

   Copilot auto-suggestions become explicit commands:
   ```bash
   # Instead of waiting for suggestions
   claude "implement the UserService.create method"
   ```

### Copilot Chat Commands Mapping

| Copilot Chat | Claude Code |
|--------------|-------------|
| `@workspace /explain` | Automatic context, just ask |
| `@workspace /fix` | `claude "fix..."` |
| `@workspace /tests` | `claude "write tests for..."` |
| `@workspace /new` | `claude "create a new..."` |
| `@terminal` | Bash tool (automatic) |
| `@vscode` | Not applicable |

---

## From Cursor

### Overview

Cursor is a fork of VS Code with deep AI integration. Migration involves moving from GUI-based interactions to CLI-based workflows.

### Key Differences

| Aspect | Cursor | Claude Code |
|--------|--------|-------------|
| Interface | Full IDE | CLI + any editor |
| Composer | GUI multi-file | CLI agentic |
| Rules | `.cursorrules` | `CLAUDE.md` |
| Context | `@` mentions | Automatic + prompts |
| Tab | Autocomplete | Not available |

### What You Lose

- **Cursor Tab**: No autocomplete integration
- **Visual composer**: No GUI for multi-file edits
- **@ mentions**: No `@codebase`, `@docs` syntax
- **Inline diff view**: Diffs shown in terminal

### What You Gain

- **Editor independence**: Use any IDE/editor
- **Deeper automation**: Hooks at every stage
- **MCP extensibility**: Connect to any data source
- **Scripting**: Full CLI for automation
- **Skills system**: Reusable expertise modules

### Migration Steps

1. **Migrate .cursorrules to CLAUDE.md**

   **From** `.cursorrules`:
   ```
   You are an expert in TypeScript and React.
   Always use functional components with hooks.
   Follow the Airbnb style guide.
   Use Tailwind CSS for styling.
   Never use any instead of proper types.
   ```

   **To** `CLAUDE.md`:
   ```markdown
   # Project Context

   ## Tech Stack
   - TypeScript with strict mode
   - React with functional components and hooks
   - Tailwind CSS for styling

   ## Code Conventions
   - Follow Airbnb style guide
   - Never use `any` - always provide proper types
   - Use functional components exclusively
   ```

2. **Replace @ mentions**

   | Cursor @ Mention | Claude Code Equivalent |
   |-----------------|----------------------|
   | `@codebase` | Automatic (Glob + Grep) |
   | `@docs [url]` | WebFetch tool or MCP |
   | `@file` | Specify path in prompt |
   | `@folder` | Specify folder in prompt |
   | `@code` | Automatic context |
   | `@git` | Git tool (automatic) |
   | `@definitions` | Automatic code analysis |

3. **Translate Composer workflows**

   **Cursor Composer:**
   ```
   @codebase Create a new API endpoint for user registration
   that validates email, hashes password, and stores in database
   ```

   **Claude Code:**
   ```bash
   claude "Create a new API endpoint for user registration that validates email, hashes password, and stores in database. Follow the patterns in src/api/"
   ```

4. **Migrate Cursor settings**

   **From** `.cursor/settings.json`:
   ```json
   {
     "cursor.aiModel": "gpt-4",
     "cursor.enableAutoComplete": true
   }
   ```

   **To** `.claude/settings.json`:
   ```json
   {
     "permissions": {
       "allow": ["Read", "Glob", "Grep"],
       "deny": []
     }
   }
   ```

### Cursor Feature Mapping

| Cursor Feature | Claude Code Alternative |
|---------------|------------------------|
| Cursor Tab | Use dedicated autocomplete (Copilot) |
| Composer | `claude` agentic mode |
| Chat | `claude` interactive mode |
| Ctrl+K edit | `claude "edit [selection]..."` |
| Ctrl+L chat | `claude` |
| @ context | Describe in prompt or use CLAUDE.md |
| Rules | CLAUDE.md |

---

## From Sourcegraph Cody

### Overview

Cody uses embeddings and code graph for context. Claude Code uses real-time search and explicit context.

### Key Differences

| Aspect | Cody | Claude Code |
|--------|------|-------------|
| Context | Embeddings + graph | Glob + Grep |
| Search | Semantic | Pattern-based |
| Indexing | Required | Not required |
| Commands | Built-in | Customizable |
| Enterprise | Sourcegraph integration | MCP servers |

### What You Lose

- **Semantic search**: Embeddings-based code search
- **Code graph**: Symbol relationships
- **Sourcegraph integration**: Direct repo browser integration
- **Pre-indexed context**: Instant semantic retrieval

### What You Gain

- **No indexing needed**: Works immediately
- **Real-time context**: Always current code
- **Full execution**: Not just chat
- **Custom automation**: Hooks and skills
- **MCP flexibility**: Connect any data source

### Migration Steps

1. **Migrate Cody configuration**

   **From** `.sourcegraph/cody.json`:
   ```json
   {
     "contextFiles": ["README.md", "docs/**"],
     "customCommands": {
       "explain": "Explain this code",
       "test": "Write tests for this"
     }
   }
   ```

   **To** `CLAUDE.md` + `.claude/commands/`:
   ```markdown
   <!-- CLAUDE.md -->
   # Project Context

   Key documentation: README.md, docs/

   ## Commands
   - /explain - Explain selected code
   - /test - Generate tests
   ```

   ```markdown
   <!-- .claude/commands/explain.md -->
   ---
   description: Explain code in detail
   ---
   Explain the following code, including:
   - Purpose and functionality
   - Key algorithms or patterns
   - Dependencies and side effects
   ```

2. **Replace Cody commands**

   | Cody Command | Claude Code |
   |--------------|-------------|
   | `Explain Code` | `/explain` or prompt |
   | `Generate Unit Test` | `/test` or prompt |
   | `Generate Docstring` | `claude "add docstring to..."` |
   | `Find Code Smells` | `claude "review for code smells"` |
   | `Custom Command` | `.claude/commands/*.md` |

3. **Adapt to search model**

   **Cody** (semantic search):
   ```
   Ask: "Where is user authentication handled?"
   Cody searches embeddings for semantically related code
   ```

   **Claude Code** (pattern search):
   ```bash
   claude "Find where user authentication is handled. Search for auth, login, authenticate patterns"
   ```

   Claude uses Grep and Glob to search, so being specific about patterns helps.

4. **Handle enterprise context**

   If using Cody with Sourcegraph enterprise:
   - Set up MCP server for internal docs
   - Use WebFetch for internal URLs
   - Create CLAUDE.md with key file locations

---

## From Aider

### Overview

Aider is a CLI-based AI coding assistant. Migration is smoother since both are CLI tools.

### Key Differences

| Aspect | Aider | Claude Code |
|--------|-------|-------------|
| Interface | CLI | CLI |
| Model | Multiple (GPT, Claude) | Claude only |
| File handling | Explicit `/add` | Automatic |
| Git | Automatic commits | On request |
| Config | `.aider.conf.yml` | Multiple files |

### What You Lose

- **Model flexibility**: Aider supports multiple AI providers
- **Automatic git commits**: Aider commits after each change
- **Explicit file control**: `/add`, `/drop` commands

### What You Gain

- **Better tool use**: Native file, search, bash tools
- **Hooks system**: Automation at every stage
- **MCP extensibility**: External data sources
- **Skills**: Reusable expertise modules
- **Permission control**: Granular approval

### Migration Steps

1. **Migrate Aider configuration**

   **From** `.aider.conf.yml`:
   ```yaml
   model: claude-3-opus
   auto-commits: true
   gitignore: true
   pretty: true
   ```

   **To** `.claude/settings.json`:
   ```json
   {
     "permissions": {
       "allow": ["Read", "Glob", "Grep"]
     }
   }
   ```

   Note: Claude Code doesn't auto-commit. Request commits explicitly:
   ```bash
   claude "make these changes and commit them"
   ```

2. **Translate Aider commands**

   | Aider Command | Claude Code |
   |---------------|-------------|
   | `/add file` | Automatic (mention file) |
   | `/drop file` | Not needed |
   | `/ask question` | Just ask |
   | `/code request` | Just request |
   | `/commit` | `claude "commit these changes"` |
   | `/diff` | Git tool shows diffs |
   | `/undo` | `git checkout` / `git reset` |
   | `/run cmd` | Bash tool (automatic) |

3. **Handle git workflow**

   **Aider** auto-commits:
   ```
   > Fix the bug in parser.py
   [Aider makes changes and commits automatically]
   ```

   **Claude Code** requires explicit request:
   ```bash
   claude "Fix the bug in parser.py and commit the changes with a descriptive message"
   ```

   Or use a hook for auto-commit behavior.

4. **Adapt file context**

   **Aider** needs explicit file addition:
   ```
   > /add src/parser.py src/lexer.py
   > Now fix the parsing bug
   ```

   **Claude Code** auto-discovers:
   ```bash
   claude "Fix the parsing bug in src/parser.py - check src/lexer.py for related context"
   ```

---

## From Other Tools

### From Tabnine

- Tabnine focuses on autocomplete
- Use with Claude Code (they complement each other)
- Migrate team configuration to CLAUDE.md

### From Amazon CodeWhisperer

- Similar to Copilot migration
- Migrate security scan workflows to hooks
- Use Claude Code for complex tasks

### From Replit AI

- Replit AI is IDE-specific
- Claude Code works with any editor
- Migrate .replit configuration to CLAUDE.md

### From Continue.dev

- Continue uses similar concepts
- Migrate `.continue/config.json` to CLAUDE.md
- Migrate custom slash commands to `.claude/commands/`

## General Migration Checklist

- [ ] Install Claude Code
- [ ] Create initial CLAUDE.md
- [ ] Test basic file operations
- [ ] Migrate rules/instructions
- [ ] Set up hooks for automation
- [ ] Create custom slash commands
- [ ] Configure MCP servers if needed
- [ ] Document team workflows
- [ ] Train team on new patterns
- [ ] Gather feedback and iterate
