---
name: fabric
context: fork
model: sonnet
description: Intelligent pattern selection for Fabric CLI. Automatically selects the right pattern from 242+ specialized prompts based on your intent - threat modeling, analysis, summarization, content creation, extraction, and more. USE WHEN processing content, analyzing data, creating summaries, threat modeling, or transforming text.
---

# Fabric Skill

## Setup Check - Fabric Repository

**IMPORTANT: Before using this skill, verify the Fabric repository is available:**

```bash
# Check if Fabric exists
fabric --version && \
test -f ~/.config/fabric/patterns/pattern_explanations.md && echo 'Fabric is properly installed and configured'
```

**If Fabric is not installed, alert the user, make sure it is installed.**

## When to Activate This Skill

**Primary Use Cases:**
- "Create a threat model for..."
- "Summarize this article/video/paper..."
- "Extract wisdom/insights from..."
- "Analyze this [code/malware/claims/debate]..."
- "Improve my writing/code/prompt..."
- "Create a [visualization/summary/report]..."
- "Rate/review/judge this content..."

**The Goal:** Select the RIGHT pattern from 242+ available patterns based on what you're trying to accomplish.

## 🎯 Pattern Selection Strategy

When a user requests Fabric processing, follow this decision tree:

### 1. Identify Intent Category

**Threat Modeling & Security:**
- Threat model → `create_threat_model` or `create_stride_threat_model`
- Threat scenarios → `create_threat_scenarios`
- Security update → `create_security_update`
- Security rules → `create_sigma_rules`, `write_nuclei_template_rule`, `write_semgrep_rule`
- Threat analysis → `analyze_threat_report`, `analyze_threat_report_trends`

**Summarization:**
- General summary → `summarize`
- 5-sentence summary → `create_5_sentence_summary`
- Micro summary → `create_micro_summary` or `summarize_micro`
- Meeting → `summarize_meeting`
- Paper/research → `summarize_paper`
- Video/YouTube → `youtube_summary`
- Newsletter → `summarize_newsletter`
- Code changes → `summarize_git_changes` or `summarize_git_diff`

**Wisdom Extraction:**
- General wisdom → `extract_wisdom`
- Article wisdom → `extract_article_wisdom`
- Book ideas → `extract_book_ideas`
- Insights → `extract_insights` or `extract_insights_dm`
- Main idea → `extract_main_idea`
- Recommendations → `extract_recommendations`
- Controversial ideas → `extract_controversial_ideas`

**Analysis:**
- Malware → `analyze_malware`
- Code → `analyze_code` or `review_code`
- Claims → `analyze_claims`
- Debate → `analyze_debate`
- Logs → `analyze_logs`
- Paper → `analyze_paper`
- Threat report → `analyze_threat_report`
- Product feedback → `analyze_product_feedback`
- Sales call → `analyze_sales_call`

**Content Creation:**
- PRD → `create_prd`
- Design document → `create_design_document`
- User story → `create_user_story`
- Visualization → `create_visualization`, `create_mermaid_visualization`, `create_markmap_visualization`
- Essay → `write_essay`
- Report finding → `create_report_finding`
- Newsletter entry → `create_newsletter_entry`

**Improvement:**
- Writing → `improve_writing`
- Academic writing → `improve_academic_writing`
- Prompt → `improve_prompt`
- Report finding → `improve_report_finding`
- Code → `review_code`

**Rating/Evaluation:**
- AI response → `rate_ai_response`
- Content quality → `rate_content`
- Value assessment → `rate_value`
- General judgment → `judge_output`

### 2. Execute Pattern

```bash
# Basic format
fabric [input] -p [selected_pattern]

# From URL
fabric -u "URL" -p [pattern]

# From YouTube
fabric -y "YOUTUBE_URL" -p [pattern]

# From file
cat file.txt | fabric -p [pattern]

# Direct text
fabric "your text here" -p [pattern]
```

## 📚 Pattern Categories (242 Total)

**Full pattern reference:** `read ${PAI_DIR}/skills/fabric/fabric-patterns-reference.md`

| Category | Count | Common Patterns |
|----------|-------|-----------------|
| Security & Threat Modeling | 15 | `create_threat_model`, `create_stride_threat_model`, `analyze_incident` |
| Summarization | 20 | `summarize`, `create_5_sentence_summary`, `youtube_summary` |
| Extraction | 30+ | `extract_wisdom`, `extract_insights`, `extract_main_idea` |
| Analysis | 35+ | `analyze_claims`, `analyze_code`, `analyze_paper` |
| Creation | 50+ | `create_prd`, `create_mermaid_visualization`, `create_user_story` |
| Improvement | 10 | `improve_writing`, `improve_prompt`, `review_code` |
| Rating | 8 | `rate_content`, `judge_output`, `rate_ai_response` |

## 🔄 Updating Patterns

The Fabric patterns exists in `~/.config/fabric/patterns/`.


**To see all available patterns:**

```bash
ls ~/.config/fabric/patterns/
```

## 💡 Usage Examples

**Threat Modeling:**
```bash
# User: "Create a threat model for our new API"
fabric "API that handles user authentication and payment processing" -p create_threat_model
```

**Summarization:**
```bash
# User: "Summarize this blog post"
fabric -u "https://example.com/blog-post" -p summarize

# User: "Give me a 5-sentence summary"
fabric -u "https://example.com/article" -p create_5_sentence_summary
```

**Wisdom Extraction:**
```bash
# User: "Extract wisdom from this video"
fabric -y "https://youtube.com/watch?v=..." -p extract_wisdom

# User: "What are the main ideas?"
fabric -u "URL" -p extract_main_idea
```

**Analysis:**
```bash
# User: "Analyze this code for issues"
fabric "$(cat code.py)" -p analyze_code

# User: "Analyze these security claims"
fabric "security claims text" -p analyze_claims
```

## 🎯 Pattern Selection Decision Matrix

| User Request Contains | Likely Intent | Recommended Patterns |
|----------------------|---------------|----------------------|
| "threat model" | Security modeling | `create_threat_model`, `create_stride_threat_model` |
| "summarize", "summary" | Summarization | `summarize`, `create_5_sentence_summary` |
| "extract wisdom", "insights" | Wisdom extraction | `extract_wisdom`, `extract_insights` |
| "analyze [X]" | Analysis | `analyze_[X]` (match X to pattern) |
| "improve", "enhance" | Improvement | `improve_writing`, `improve_prompt` |
| "create [visualization]" | Visualization | `create_mermaid_visualization`, `create_markmap_visualization` |
| "rate", "judge", "evaluate" | Rating | `rate_content`, `judge_output` |
| "main idea", "core message" | Core extraction | `extract_main_idea`, `extract_core_message` |

## 🚀 Advanced Usage

**Pipe content through Fabric:**
```bash
cat article.txt | fabric -p extract_wisdom
pbpaste | fabric -p summarize
curl -s "https://..." | fabric -p analyze_claims
```

**Process YouTube videos:**
```bash
# Fabric handles download + transcription + processing
fabric -y "https://youtube.com/watch?v=..." -p youtube_summary
```

**Chain patterns (manual):**
```bash
# Extract then summarize
fabric -u "URL" -p extract_wisdom > wisdom.txt
cat wisdom.txt | fabric -p create_5_sentence_summary
```

## 🤖 Model Selection

**Comprehensive Model Guide**: `read ${PAI_DIR}/skils/fabric/fabric-model-reference.md`

**Quick Recommendations**:

- **High Volume/Free**: `gemini-2.5-flash` (free, ultra-fast)
- **Balanced Quality**: `claude-sonnet-4-5-20250929` (best general purpose, recommended)
- **Maximum Quality**: `claude-opus-4-20250514` (highest quality)
- **Reasoning Tasks**: `gemini-2.0-flash-thinking-exp` (extended thinking mode)
- **Cost Sensitive**: `claude-3-5-haiku-20241022` (ultra-low cost)

**List Available Models**: `fabric --listmodels`

**Specify Model**: `fabric "content" -p pattern_name --model claude-sonnet-4-5-20250929`

## 📖 Supplementary Resources

**Strategy Reference:** `read ${PAI_DIR}/skils/fabric/fabric-strategies-reference.md`
Task-based pattern selection guide with workflows and test cases

**Pattern Reference (Complete):** `read ${PAI_DIR}/skils/fabric/fabric-patterns-reference.md`
Comprehensive categorized reference for all 240 patterns

**Model Reference:** `read ${PAI_DIR}/skils/fabric/fabric-model-reference.md`
**Full Pattern List:** `ls ~/.config/fabric/patterns/`
**Fabric Documentation:** https://github.com/danielmiessler/fabric
**Pattern Templates:** See `~/.config/fabric/patterns/official_pattern_template/`

## 🔑 Key Insight

**The skill's value is in selecting the RIGHT pattern for the task.**

When user says "Create a threat model using Fabric", your job is to:
1. Recognize "threat model" intent
2. Know available options: `create_threat_model`, `create_stride_threat_model`, `create_threat_scenarios`
3. Select the best match (usually `create_threat_model` unless STRIDE specified)
4. Execute: `fabric "[content]" -p create_threat_model`

**Not:** "Here are the patterns, pick one"
**Instead:** "I'll use `create_threat_model` for this" → execute immediately
