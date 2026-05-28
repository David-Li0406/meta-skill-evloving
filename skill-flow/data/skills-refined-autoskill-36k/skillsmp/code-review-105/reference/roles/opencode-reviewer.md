# OpenCode Reviewer Role

External subprocess reviewer for fresh perspective analysis.

---

## Characteristics

- **Fresh perspective:** No prior context, sees code as newcomer would
- **Multiple models:** OpenAI or Google, different reasoning patterns
- **Independent:** Separate process, no shared state
- **Code-focused:** Specialized models available (Codex)

---

## Strengths

- Catches assumptions that insiders miss
- Different models catch different issues
- Simulates new team member perspective
- Validates readability for external audiences
- Code-specialized models excel at pattern detection

---

## Review Focus

1. **Correctness:** Does the logic make sense standalone?
2. **Style:** Is naming clear without context?
3. **Performance:** Are there obvious inefficiencies?
4. **Security:** Common vulnerability patterns
5. **Architecture:** Is structure understandable?

---

## Available Models

**OpenAI:**
- `openai/gpt-5.2` - Base GPT-5.2 model
- `openai/gpt-5.2-codex` - Code-specialized variant (recommended)
- `openai/gpt-5.2-pro` - Pro tier with extended capabilities

**Google:**
- `google/gemini-3-flash-preview` - Fast, efficient model
- `google/gemini-3-pro-preview` - Advanced reasoning capabilities

**Reasoning Effort (--variant flag):**

Format: `{reasoning}-medium` (verbosity fixed at medium)

- `low-medium` - Quick responses, minimal deliberation
- `medium-medium` - Balanced reasoning
- `high-medium` - Deep analysis, thorough deliberation (recommended for reviews)
- `xhigh-medium` - Maximum reasoning (GPT-5.2 only)

---

## Dispatch Configuration

**Template:**
```bash
timeout 1200 opencode run --model "{MODEL}" --variant high-medium "[Review prompt with code content]"
```

**Examples:**
```bash
# OpenAI Codex (code-focused, recommended)
opencode run --model "openai/gpt-5.2-codex" --variant high-medium "{prompt}"

# OpenAI GPT-5.2 Pro
opencode run --model "openai/gpt-5.2-pro" --variant high-medium "{prompt}"

# Google Gemini 3 Pro
opencode run --model "google/gemini-3-pro-preview" --variant high-medium "{prompt}"
```

5-minute timeout prevents hanging.

---

## Expected Behavior

- Analyzes only provided code
- No access to codebase (fresh perspective)
- Outputs structured YAML report
- Highlights clarity and readability issues effectively
- Catches common anti-patterns

---

## Limitations

- Cannot verify against actual codebase
- May flag "issues" that are project conventions
- Limited context for architecture assessment
- Depends on external service availability
