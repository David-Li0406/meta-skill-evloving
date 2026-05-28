# OpenCode Reviewer Role

External subprocess reviewer for fresh perspective analysis.

---

## Characteristics

- **Fresh perspective:** No prior context, sees spec as newcomer would
- **Multiple models:** OpenAI or Google, different reasoning patterns
- **Independent:** Separate process, no shared state
- **Quick:** Focused on provided content only

---

## Strengths

- Catches assumptions that insiders miss
- Different models catch different issues
- Simulates new team member perspective
- Validates clarity for external audiences

---

## Review Focus

1. **Completeness:** What's missing that a newcomer would need?
2. **Consistency:** Are terms and concepts self-consistent?
3. **Feasibility:** Do described tasks make logical sense?
4. **Clarity:** Can someone unfamiliar understand this?

---

## Available Models

**OpenAI:**
- `openai/gpt-5.2` - Base GPT-5.2 model
- `openai/gpt-5.2-codex` - Code-specialized variant
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
timeout 1200 opencode run --model "{MODEL}" --variant high-medium "[Review prompt with spec content]"
```

**Examples:**
```bash
# OpenAI GPT-5.2 Pro
opencode run --model "openai/gpt-5.2-pro" --variant high-medium "{prompt}"

# Google Gemini 3 Pro
opencode run --model "google/gemini-3-pro-preview" --variant high-medium "{prompt}"

# OpenAI Codex (code-focused)
opencode run --model "openai/gpt-5.2-codex" --variant high-medium "{prompt}"
```

5-minute timeout prevents hanging.

---

## Expected Behavior

- Analyzes only provided content
- No access to codebase (fresh perspective)
- Outputs structured YAML report
- Highlights clarity issues effectively

---

## Limitations

- Cannot verify against actual codebase
- May flag "issues" that are project conventions
- Limited context for integration feasibility
- Depends on external service availability
