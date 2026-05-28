# Fabric Pattern Strategies - Task-Based Selection Guide

**Purpose**: Match tasks and content types to optimal Fabric pattern workflows and strategies.

**Last Updated**: 2025-11-14

---

## Quick Navigation

- [Content Type Strategies](#content-type-strategies)
- [Task Type Strategies](#task-type-strategies)
- [Workflow Strategies](#workflow-strategies)
- [Domain-Specific Strategies](#domain-specific-strategies)
- [Quality Level Strategies](#quality-level-strategies)

---

## Content Type Strategies

### Blog Posts & Articles

| Goal | Strategy | Patterns | Model |
| ---- | -------- | -------- | ----- |
| Quick understanding | Extract + Summarize | `extract_main_idea` → `create_5_sentence_summary` | gemini-2.5-flash |
| Deep insights | Extract wisdom | `extract_article_wisdom` or `extract_wisdom` | claude-sonnet-4-5 |
| Content curation | Extract + Tag | `extract_insights` → `create_tags` | gemini-2.5-flash |
| Social sharing | Micro summary | `create_micro_summary` or `tweet` | claude-haiku |
| Learning | Flash cards | `create_flash_cards` or `to_flashcards` | gemini-2.5-flash |
| Fact checking | Analyze claims | `analyze_claims` → `extract_extraordinary_claims` | claude-sonnet-4-5 |
| Enhancement | Improve writing | `improve_writing` or `enrich_blog_post` | claude-sonnet-4-5 |

**Recommended Workflow**:

```bash
# Quick blog analysis workflow
fabric -u "BLOG_URL" -p extract_article_wisdom --model claude-sonnet-4-5 > insights.txt
cat insights.txt | fabric -p create_5_sentence_summary --model gemini-2.5-flash
```

### YouTube Videos

| Goal | Strategy | Patterns | Model |
| ---- | -------- | -------- | ----- |
| Quick overview | YouTube summary | `youtube_summary` | gemini-2.5-flash |
| Extract learning | Wisdom extraction | `extract_wisdom` or `extract_insights` | claude-sonnet-4-5 |
| Study material | Flash cards | `create_flash_cards` → `create_quiz` | gemini-2.5-flash |
| Key moments | Extract + Chapters | `extract_main_idea` + `create_video_chapters` | gemini-2.5-flash |
| Action items | Extract recommendations | `extract_recommendations` or `extract_instructions` | claude-sonnet-4-5 |
| Entertainment value | Engagement rating | `get_wow_per_minute` | gemini-2.5-flash |
| Humor analysis | Extract jokes | `extract_jokes` | gemini-2.5-flash |

**Recommended Workflow**:

```bash
# Comprehensive YouTube analysis
fabric -y "YOUTUBE_URL" -p youtube_summary --model gemini-2.5-flash > summary.txt
fabric -y "YOUTUBE_URL" -p extract_wisdom --model claude-sonnet-4-5 > wisdom.txt
cat wisdom.txt | fabric -p create_flash_cards --model gemini-2.5-flash
```

### Academic Papers

| Goal | Strategy | Patterns | Model |
| ---- | -------- | -------- | ----- |
| Quick scan | Simple analysis | `analyze_paper_simple` or `summarize_paper` | gemini-2.5-flash |
| Deep analysis | Full analysis | `analyze_paper` | claude-sonnet-4-5 |
| Literature review | Extract + Summarize | `extract_references` → `summarize_paper` | claude-sonnet-4-5 |
| Study prep | Flash cards + Quiz | `create_flash_cards` → `create_quiz` | gemini-2.5-flash |
| Research ideas | Extract insights | `extract_ideas` or `extract_business_ideas` | claude-sonnet-4-5 |
| Methodology | Extract instructions | `extract_instructions` or `extract_algorithm_update_recommendations` | claude-sonnet-4-5 |
| Writing your own | Improve writing | `improve_academic_writing` | claude-opus-4 |

**Recommended Workflow**:

```bash
# Academic paper workflow
cat paper.pdf | fabric -p analyze_paper --model claude-sonnet-4-5 > analysis.txt
cat paper.pdf | fabric -p extract_references --model claude-sonnet-4-5 > references.txt
cat analysis.txt | fabric -p create_flash_cards --model gemini-2.5-flash
```

### Code & Technical Content

| Goal | Strategy | Patterns | Model |
| ---- | -------- | -------- | ----- |
| Code review | Analyze + Review | `analyze_code` or `review_code` | claude-sonnet-4-5 |
| Documentation | Explain code | `explain_code` or `explain_project` | claude-sonnet-4-5 |
| Security audit | Security analysis | `analyze_code` → `create_security_update` | claude-opus-4 |
| Malware analysis | Threat analysis | `analyze_malware` → `analyze_threat_report` | claude-opus-4 |
| Git workflow | Commit messages | `create_git_diff_commit` or `summarize_git_changes` | claude-haiku |
| PR description | PR summary | `write_pull-request` or `summarize_pull-requests` | claude-sonnet-4-5 |
| Log analysis | Extract issues | `analyze_logs` | claude-sonnet-4-5 |
| Rules creation | Generate rules | `generate_code_rules` or `write_semgrep_rule` | claude-sonnet-4-5 |

**Recommended Workflow**:

```bash
# Code review workflow
cat code.py | fabric -p analyze_code --model claude-sonnet-4-5 > review.txt
cat code.py | fabric -p review_code --model claude-sonnet-4-5 > suggestions.txt
cat review.txt suggestions.txt | fabric -p create_report_finding --model claude-sonnet-4-5
```

### Social Media & Short Content

| Goal | Strategy | Patterns | Model |
| ---- | -------- | -------- | ----- |
| Tweet creation | Micro content | `tweet` or `create_micro_summary` | claude-haiku |
| Thread creation | Micro essay | `write_micro_essay` | claude-sonnet-4-5 |
| Engagement analysis | Rate content | `rate_content` or `analyze_comments` | gemini-2.5-flash |
| Viral potential | WPM score | `get_wow_per_minute` | gemini-2.5-flash |
| Controversy check | Find fallacies | `find_logical_fallacies` or `extract_controversial_ideas` | claude-sonnet-4-5 |

### Meeting Notes & Transcripts

| Goal | Strategy | Patterns | Model |
| ---- | -------- | -------- | ----- |
| Meeting summary | Summarize meeting | `summarize_meeting` or `summarize_board_meeting` | gemini-2.5-flash |
| Action items | Extract recommendations | `extract_recommendations` or `extract_instructions` | claude-sonnet-4-5 |
| Transcription | Transcribe | `transcribe_minutes` | gemini-2.5-flash |
| Decision log | Extract decisions | `extract_main_idea` → `create_summary` | claude-sonnet-4-5 |
| Follow-up | Create tasks | `extract_recommendations` → `create_user_story` | claude-sonnet-4-5 |

### News & Current Events

| Goal | Strategy | Patterns | Model |
| ---- | -------- | -------- | ----- |
| Daily briefing | Cyber summary | `create_cyber_summary` or `create_ul_summary` | gemini-2.5-flash |
| Threat intelligence | Threat analysis | `analyze_threat_report` → `analyze_threat_report_trends` | claude-sonnet-4-5 |
| Newsletter creation | Newsletter entry | `create_newsletter_entry` or `summarize_newsletter` | claude-sonnet-4-5 |
| Fact checking | Analyze claims | `analyze_claims` → `extract_extraordinary_claims` | claude-sonnet-4-5 |

---

## Task Type Strategies

### Learning & Education

**Goal**: Maximize retention and understanding

| Content Type | Primary Pattern | Secondary Pattern | Model Chain |
| ------------ | --------------- | ----------------- | ----------- |
| Any educational | `extract_wisdom` | `create_flash_cards` | sonnet → flash |
| Complex concepts | `explain_terms` | `create_conceptmap` | sonnet → sonnet |
| Math/technical | `explain_math` | `solve_with_cot` | sonnet → thinking |
| Video lectures | `youtube_summary` | `extract_insights` → `create_quiz` | flash → sonnet → flash |
| Books | `extract_book_ideas` | `create_reading_plan` | sonnet → flash |
| Practice | `create_quiz` | `create_flash_cards` | flash → flash |

**Workflow Example**:

```bash
# Complete learning workflow
fabric -y "LECTURE_URL" -p youtube_summary --model gemini-2.5-flash > lecture.txt
cat lecture.txt | fabric -p extract_wisdom --model claude-sonnet-4-5 > wisdom.txt
cat wisdom.txt | fabric -p create_flash_cards --model gemini-2.5-flash > cards.txt
cat wisdom.txt | fabric -p create_quiz --model gemini-2.5-flash > quiz.txt
```

### Research & Analysis

**Goal**: Deep understanding and insight generation

| Research Type | Primary Pattern | Secondary Pattern | Model |
| ------------- | --------------- | ----------------- | ----- |
| Literature review | `analyze_paper` | `extract_references` | opus |
| Competitive analysis | `compare_and_contrast` | `analyze_product_feedback` | sonnet |
| Market research | `extract_business_ideas` | `analyze_tech_impact` | sonnet |
| User research | `extract_insights` | `identify_job_stories` | sonnet |
| Data analysis | `extract_patterns` | `create_graph_from_input` | sonnet |
| Trend analysis | `extract_predictions` | `analyze_threat_report_trends` | sonnet |

**Workflow Example**:

```bash
# Research synthesis workflow
fabric -u "ARTICLE1" -p analyze_paper --model claude-opus-4 > paper1.txt
fabric -u "ARTICLE2" -p analyze_paper --model claude-opus-4 > paper2.txt
cat paper1.txt paper2.txt | fabric -p compare_and_contrast --model claude-sonnet-4-5 > comparison.txt
cat comparison.txt | fabric -p extract_insights --model claude-sonnet-4-5
```

### Content Creation

**Goal**: High-quality content generation

| Content Type | Primary Pattern | Enhancement Pattern | Model |
| ------------ | --------------- | ------------------- | ----- |
| Essays | `write_essay` | `improve_writing` | sonnet → opus |
| Paul Graham style | `write_essay_pg` | `improve_writing` | sonnet → sonnet |
| Micro content | `write_micro_essay` | `tweet` | sonnet → haiku |
| Academic | `create_academic_paper` | `improve_academic_writing` | opus → opus |
| Technical docs | `create_design_document` | `refine_design_document` | sonnet → sonnet |
| PRDs | `create_prd` | `review_design` | sonnet → sonnet |
| Blog posts | `write_essay` | `enrich_blog_post` | sonnet → sonnet |
| Presentations | `create_keynote` | `analyze_presentation` | sonnet → sonnet |

**Workflow Example**:

```bash
# Content creation workflow
fabric "Topic: AI ethics" -p write_essay --model claude-sonnet-4-5 > draft.txt
cat draft.txt | fabric -p improve_writing --model claude-opus-4 > improved.txt
cat improved.txt | fabric -p create_tags --model gemini-2.5-flash
```

### Security & Threat Modeling

**Goal**: Comprehensive security analysis

| Security Task | Primary Pattern | Secondary Pattern | Model |
| ------------- | --------------- | ----------------- | ----- |
| Threat modeling | `create_threat_model` | `create_threat_scenarios` | opus |
| STRIDE analysis | `create_stride_threat_model` | `create_security_update` | opus |
| Incident response | `analyze_incident` | `create_report_finding` | opus |
| Malware analysis | `analyze_malware` | `analyze_threat_report` | opus |
| Security design | `ask_secure_by_design_questions` | `create_threat_model` | opus |
| Detection rules | `create_sigma_rules` | `write_nuclei_template_rule` | sonnet |
| Network security | `create_network_threat_landscape` | `analyze_risk` | opus |
| CTF writeups | `extract_ctf_writeup` | `extract_poc` | sonnet |

**Workflow Example**:

```bash
# Threat modeling workflow
fabric "New payment API" -p create_stride_threat_model --model claude-opus-4 > threats.txt
cat threats.txt | fabric -p create_threat_scenarios --model claude-opus-4 > scenarios.txt
cat scenarios.txt | fabric -p create_security_update --model claude-sonnet-4-5 > update.txt
cat threats.txt | fabric -p create_sigma_rules --model claude-sonnet-4-5
```

### Code Development

**Goal**: High-quality code and documentation

| Dev Task | Primary Pattern | Secondary Pattern | Model |
| -------- | --------------- | ----------------- | ----- |
| Code review | `review_code` | `analyze_code` | sonnet |
| Refactoring | `analyze_code` | `improve_wr` | sonnet |
| Documentation | `explain_code` | `explain_project` | sonnet |
| Git commits | `create_git_diff_commit` | `summarize_git_diff` | haiku |
| Pull requests | `write_pull-request` | `summarize_pull-requests` | sonnet |
| Code rules | `generate_code_rules` | `write_semgrep_rule` | sonnet |
| Bug reports | `write_hackerone_report` | `create_report_finding` | sonnet |
| Feature specs | `create_coding_feature` | `create_user_story` | sonnet |

**Workflow Example**:

```bash
# Development workflow
git diff | fabric -p review_code --model claude-sonnet-4-5 > review.txt
git diff | fabric -p create_git_diff_commit --model claude-haiku > commit_msg.txt
cat review.txt | fabric -p improve_report_finding --model claude-sonnet-4-5
```

### Product Management

**Goal**: Clear requirements and user-centered design

| PM Task | Primary Pattern | Secondary Pattern | Model |
| ------- | --------------- | ----------------- | ----- |
| PRD creation | `create_prd` | `create_design_document` | sonnet |
| User stories | `create_user_story` | `identify_job_stories` | sonnet |
| Feature specs | `create_coding_feature` | `create_coding_project` | sonnet |
| Feedback analysis | `analyze_product_feedback` | `extract_insights` | sonnet |
| Strategy | `prepare_7s_strategy` | `create_better_frame` | opus |
| Roadmap | `create_recursive_outline` | `create_visualization` | sonnet |
| Customer research | `analyze_comments` | `extract_patterns` | sonnet |

**Workflow Example**:

```bash
# Product development workflow
fabric "Feature idea: dark mode" -p create_prd --model claude-sonnet-4-5 > prd.txt
cat prd.txt | fabric -p create_user_story --model claude-sonnet-4-5 > stories.txt
cat prd.txt | fabric -p create_threat_model --model claude-opus-4 > security.txt
```

### Personal Development

**Goal**: Self-improvement and growth

| Development Area | Primary Pattern | Secondary Pattern | Model |
| ---------------- | --------------- | ----------------- | ----- |
| Self-reflection | `t_find_blindspots` | `t_check_dunning_kruger` | sonnet |
| Goal setting | `t_visualize_mission_goals_projects` | `t_find_neglected_goals` | sonnet |
| Annual review | `t_year_in_review` | `t_describe_life_outlook` | sonnet |
| Critical thinking | `t_red_team_thinking` | `find_logical_fallacies` | sonnet |
| Encouragement | `t_give_encouragement` | `provide_guidance` | sonnet |
| Career planning | `t_create_h3_career` | `extract_skills` | sonnet |
| Philosophical | `dialog_with_socrates` | `philocapsulate` | opus |

---

## Workflow Strategies

### Speed-First Workflows

**When**: Quick answers, high volume, cost-sensitive

**Model**: `gemini-2.5-flash` (free, fast)

**Patterns**:

```bash
# Ultra-fast extraction
fabric -u "URL" -p extract_main_idea --model gemini-2.5-flash

# Quick summaries
fabric -u "URL" -p create_5_sentence_summary --model gemini-2.5-flash

# Rapid flash cards
cat content.txt | fabric -p create_flash_cards --model gemini-2.5-flash

# Fast tagging
fabric "content" -p create_tags --model gemini-2.5-flash
```

### Quality-First Workflows

**When**: Critical analysis, security, high-stakes decisions

**Model**: `claude-opus-4` (highest quality)

**Patterns**:

```bash
# Deep threat modeling
fabric "system design" -p create_stride_threat_model --model claude-opus-4

# Critical paper analysis
cat paper.pdf | fabric -p analyze_paper --model claude-opus-4

# High-quality writing
fabric "topic" -p write_essay --model claude-opus-4 | \
  fabric -p improve_writing --model claude-opus-4
```

### Balanced Workflows

**When**: General purpose, good quality/cost ratio

**Model**: `claude-sonnet-4-5` (recommended default)

**Patterns**:

```bash
# Standard analysis
fabric -u "URL" -p extract_wisdom --model claude-sonnet-4-5

# Code review
cat code.py | fabric -p review_code --model claude-sonnet-4-5

# Content creation
fabric "topic" -p write_essay --model claude-sonnet-4-5
```

### Reasoning Workflows

**When**: Complex problem solving, extended thinking required

**Model**: `gemini-2.0-flash-thinking-exp` (thinking mode)

**Patterns**:

```bash
# Complex problem solving
fabric "complex problem" -p solve_with_cot --model gemini-2.0-flash-thinking-exp

# Deep analysis with reasoning
fabric "scenario" -p analyze_risk --model gemini-2.0-flash-thinking-exp
```

### Multi-Stage Workflows

**When**: Complex tasks requiring multiple transformations

**Strategy**: Chain patterns with appropriate models

```bash
# Research → Synthesis → Documentation
fabric -u "URL1" -p analyze_paper --model claude-opus-4 > paper1.txt
fabric -u "URL2" -p analyze_paper --model claude-opus-4 > paper2.txt
cat paper1.txt paper2.txt | fabric -p compare_and_contrast --model claude-sonnet-4-5 > comparison.txt
cat comparison.txt | fabric -p create_academic_paper --model claude-opus-4 > output.txt

# Content → Extract → Learn → Test
fabric -y "URL" -p youtube_summary --model gemini-2.5-flash > summary.txt
cat summary.txt | fabric -p extract_wisdom --model claude-sonnet-4-5 > wisdom.txt
cat wisdom.txt | fabric -p create_flash_cards --model gemini-2.5-flash > cards.txt
cat wisdom.txt | fabric -p create_quiz --model gemini-2.5-flash > quiz.txt
```

---

## Domain-Specific Strategies

### Cybersecurity Domain

| Task | Pattern Chain | Model Strategy |
| ---- | ------------- | -------------- |
| Daily threat brief | `analyze_threat_report` → `create_cyber_summary` | sonnet → flash |
| Incident handling | `analyze_incident` → `create_report_finding` → `create_security_update` | opus → sonnet → sonnet |
| Detection engineering | `analyze_threat_report_cmds` → `create_sigma_rules` | sonnet → sonnet |
| Threat hunting | `analyze_logs` → `analyze_malware` → `extract_poc` | sonnet → opus → sonnet |
| Security design | `ask_secure_by_design_questions` → `create_stride_threat_model` | opus → opus |

### Software Engineering Domain

| Task | Pattern Chain | Model Strategy |
| ---- | ------------- | -------------- |
| Feature development | `create_prd` → `create_coding_feature` → `create_user_story` | sonnet → sonnet → sonnet |
| Code review cycle | `review_code` → `improve_report_finding` → `create_git_diff_commit` | sonnet → sonnet → haiku |
| Documentation | `explain_code` → `explain_project` → `improve_writing` | sonnet → sonnet → opus |
| Testing | `analyze_code` → `create_quiz` (for test cases) | sonnet → flash |
| Refactoring | `analyze_code` → `review_code` → `generate_code_rules` | sonnet → sonnet → sonnet |

### Content & Marketing Domain

| Task | Pattern Chain | Model Strategy |
| ---- | ------------- | -------------- |
| Blog workflow | `write_essay` → `improve_writing` → `enrich_blog_post` | sonnet → opus → sonnet |
| Social media | `create_micro_summary` → `tweet` → `rate_content` | sonnet → haiku → flash |
| Newsletter | `summarize_newsletter` → `create_newsletter_entry` | flash → sonnet |
| SEO content | `extract_main_idea` → `create_tags` → `improve_writing` | sonnet → flash → sonnet |
| Video content | `youtube_summary` → `create_video_chapters` → `create_show_intro` | flash → flash → sonnet |

### Academic & Research Domain

| Task | Pattern Chain | Model Strategy |
| ---- | ------------- | -------------- |
| Literature review | `analyze_paper` → `extract_references` → `summarize_paper` | opus → sonnet → flash |
| Writing papers | `create_academic_paper` → `improve_academic_writing` | opus → opus |
| Study prep | `extract_wisdom` → `create_flash_cards` → `create_quiz` | sonnet → flash → flash |
| Research synthesis | `compare_and_contrast` → `extract_insights` → `analyze_paper` | sonnet → sonnet → opus |

### Business & Strategy Domain

| Task | Pattern Chain | Model Strategy |
| ---- | ------------- | -------------- |
| Strategic planning | `prepare_7s_strategy` → `create_better_frame` → `t_visualize_mission_goals_projects` | opus → sonnet → sonnet |
| Market analysis | `analyze_tech_impact` → `extract_business_ideas` → `create_hormozi_offer` | sonnet → sonnet → sonnet |
| Product strategy | `create_prd` → `analyze_product_feedback` → `create_design_document` | sonnet → sonnet → sonnet |
| Sales optimization | `analyze_sales_call` → `extract_recommendations` → `improve_prompt` | sonnet → sonnet → sonnet |

---

## Quality Level Strategies

### Maximum Quality (Critical Work)

**Use Cases**: Security audits, critical decisions, high-stakes analysis, production code

**Model**: `claude-opus-4-20250514`

**Cost**: Highest ($15 input / $75 output per 1M tokens)

**Patterns to prioritize**:

- `create_stride_threat_model`
- `analyze_paper`
- `improve_academic_writing`
- `create_threat_model`
- `analyze_malware`
- `analyze_incident`

**Example**:

```bash
fabric "critical system" -p create_stride_threat_model --model claude-opus-4-20250514
```

### High Quality (Default)

**Use Cases**: General analysis, code review, content creation, research

**Model**: `claude-sonnet-4-5-20250929`

**Cost**: Balanced ($3 input / $15 output per 1M tokens)

**Patterns to prioritize**:

- `extract_wisdom`
- `analyze_code`
- `review_code`
- `write_essay`
- `create_prd`
- `analyze_claims`

**Example**:

```bash
fabric -u "URL" -p extract_wisdom --model claude-sonnet-4-5-20250929
```

### Speed & Cost Optimized

**Use Cases**: High volume, quick answers, learning, summaries

**Model**: `gemini-2.5-flash`

**Cost**: Free (with rate limits)

**Patterns to prioritize**:

- `create_5_sentence_summary`
- `extract_main_idea`
- `create_flash_cards`
- `youtube_summary`
- `create_tags`
- `get_wow_per_minute`

**Example**:

```bash
fabric -y "VIDEO_URL" -p youtube_summary --model gemini-2.5-flash
```

### Extended Thinking

**Use Cases**: Complex reasoning, problem solving, analysis requiring deep thought

**Model**: `gemini-2.0-flash-thinking-exp`

**Cost**: Mid-range

**Patterns to prioritize**:

- `solve_with_cot`
- `analyze_risk`
- `create_threat_model`
- `analyze_paper`
- `compare_and_contrast`

**Example**:

```bash
fabric "complex problem" -p solve_with_cot --model gemini-2.0-flash-thinking-exp
```

### Ultra-Low Cost

**Use Cases**: Testing, experimentation, non-critical summaries

**Model**: `claude-3-5-haiku-20241022`

**Cost**: Ultra-low ($0.80 input / $4 output per 1M tokens)

**Patterns to prioritize**:

- `create_git_diff_commit`
- `tweet`
- `create_micro_summary`
- `clean_text`
- `fix_typos`

**Example**:

```bash
git diff | fabric -p create_git_diff_commit --model claude-3-5-haiku-20241022
```

---

## Pattern Selection Decision Framework

### Step 1: Identify Content Type

```text
What are you processing?
├─ Article/Blog → extract_article_wisdom, summarize
├─ Video → youtube_summary, extract_wisdom
├─ Code → analyze_code, review_code
├─ Paper → analyze_paper, summarize_paper
├─ Meeting → summarize_meeting, extract_recommendations
├─ Social → tweet, create_micro_summary
└─ Security → create_threat_model, analyze_incident
```

### Step 2: Identify Goal

```text
What do you want to achieve?
├─ Learn → extract_wisdom, create_flash_cards
├─ Summarize → create_5_sentence_summary, summarize
├─ Analyze → analyze_*, compare_and_contrast
├─ Create → write_*, create_*
├─ Improve → improve_*, review_*
├─ Extract → extract_*
└─ Rate → rate_*, judge_output
```

### Step 3: Select Quality Level

```text
How critical is this task?
├─ Critical/Security → claude-opus-4
├─ Important/Production → claude-sonnet-4-5
├─ General/Learning → gemini-2.5-flash
├─ Quick/High-volume → gemini-2.5-flash
└─ Testing/Experimental → claude-haiku
```

### Step 4: Consider Chaining

```text
Does this need multiple steps?
├─ Yes → Chain patterns with appropriate models
│   ├─ Extract → Analyze → Create
│   ├─ Summarize → Extract → Learn
│   └─ Analyze → Compare → Synthesize
└─ No → Use single pattern
```

---

## Common Test Cases & Strategies

### Test Case 1: "Analyze this blog post"

**Default Strategy**:

```bash
fabric -u "URL" -p extract_article_wisdom --model claude-sonnet-4-5
```

**Speed Strategy**:

```bash
fabric -u "URL" -p extract_main_idea --model gemini-2.5-flash
```

**Deep Strategy**:

```bash
fabric -u "URL" -p extract_article_wisdom --model claude-sonnet-4-5 > wisdom.txt
cat wisdom.txt | fabric -p analyze_claims --model claude-opus-4 > analysis.txt
cat wisdom.txt | fabric -p create_5_sentence_summary --model gemini-2.5-flash
```

### Test Case 2: "Learn from this YouTube video"

**Default Strategy**:

```bash
fabric -y "URL" -p youtube_summary --model gemini-2.5-flash > summary.txt
cat summary.txt | fabric -p extract_wisdom --model claude-sonnet-4-5 > wisdom.txt
cat wisdom.txt | fabric -p create_flash_cards --model gemini-2.5-flash
```

**Speed Strategy**:

```bash
fabric -y "URL" -p youtube_summary --model gemini-2.5-flash
```

**Deep Strategy**:

```bash
fabric -y "URL" -p youtube_summary --model gemini-2.5-flash > summary.txt
cat summary.txt | fabric -p extract_wisdom --model claude-sonnet-4-5 > wisdom.txt
cat wisdom.txt | fabric -p create_flash_cards --model gemini-2.5-flash > cards.txt
cat wisdom.txt | fabric -p create_quiz --model gemini-2.5-flash > quiz.txt
cat wisdom.txt | fabric -p create_reading_plan --model claude-sonnet-4-5
```

### Test Case 3: "Review this code"

**Default Strategy**:

```bash
cat code.py | fabric -p review_code --model claude-sonnet-4-5
```

**Security Strategy**:

```bash
cat code.py | fabric -p analyze_code --model claude-opus-4 > analysis.txt
cat analysis.txt | fabric -p create_threat_model --model claude-opus-4 > threats.txt
cat code.py | fabric -p write_semgrep_rule --model claude-sonnet-4-5
```

**Documentation Strategy**:

```bash
cat code.py | fabric -p explain_code --model claude-sonnet-4-5 > docs.txt
cat code.py | fabric -p review_code --model claude-sonnet-4-5 > review.txt
cat docs.txt review.txt | fabric -p improve_writing --model claude-opus-4
```

### Test Case 4: "Create a threat model"

**Default Strategy**:

```bash
fabric "system description" -p create_threat_model --model claude-opus-4
```

**STRIDE Strategy**:

```bash
fabric "system" -p create_stride_threat_model --model claude-opus-4 > model.txt
cat model.txt | fabric -p create_threat_scenarios --model claude-opus-4 > scenarios.txt
cat scenarios.txt | fabric -p create_security_update --model claude-sonnet-4-5
```

**Comprehensive Strategy**:

```bash
fabric "system" -p create_stride_threat_model --model claude-opus-4 > model.txt
cat model.txt | fabric -p create_threat_scenarios --model claude-opus-4 > scenarios.txt
cat scenarios.txt | fabric -p create_sigma_rules --model claude-sonnet-4-5 > rules.txt
cat scenarios.txt | fabric -p create_network_threat_landscape --model claude-opus-4
```

### Test Case 5: "Summarize meeting notes"

**Default Strategy**:

```bash
cat notes.txt | fabric -p summarize_meeting --model gemini-2.5-flash
```

**Action Items Strategy**:

```bash
cat notes.txt | fabric -p summarize_meeting --model gemini-2.5-flash > summary.txt
cat summary.txt | fabric -p extract_recommendations --model claude-sonnet-4-5 > actions.txt
cat actions.txt | fabric -p create_user_story --model claude-sonnet-4-5
```

**Board Meeting Strategy**:

```bash
cat notes.txt | fabric -p summarize_board_meeting --model claude-sonnet-4-5 > summary.txt
cat summary.txt | fabric -p extract_main_idea --model gemini-2.5-flash
```

### Test Case 6: "Improve my writing"

**Default Strategy**:

```bash
cat draft.txt | fabric -p improve_writing --model claude-opus-4
```

**Academic Strategy**:

```bash
cat paper.txt | fabric -p improve_academic_writing --model claude-opus-4
```

**Blog Strategy**:

```bash
cat blog.txt | fabric -p improve_writing --model claude-opus-4 > improved.txt
cat improved.txt | fabric -p enrich_blog_post --model claude-sonnet-4-5 > enriched.txt
cat enriched.txt | fabric -p create_tags --model gemini-2.5-flash
```

### Test Case 7: "Extract insights from research"

**Default Strategy**:

```bash
cat research.txt | fabric -p extract_insights --model claude-sonnet-4-5
```

**Business Strategy**:

```bash
cat research.txt | fabric -p extract_business_ideas --model claude-sonnet-4-5 > ideas.txt
cat ideas.txt | fabric -p create_hormozi_offer --model claude-sonnet-4-5
```

**Deep Analysis Strategy**:

```bash
cat research.txt | fabric -p extract_insights --model claude-sonnet-4-5 > insights.txt
cat insights.txt | fabric -p extract_patterns --model claude-sonnet-4-5 > patterns.txt
cat patterns.txt | fabric -p create_visualization --model claude-sonnet-4-5
```

### Test Case 8: "Create content from idea"

**Essay Strategy**:

```bash
fabric "topic" -p write_essay --model claude-sonnet-4-5 > draft.txt
cat draft.txt | fabric -p improve_writing --model claude-opus-4
```

**Micro Content Strategy**:

```bash
fabric "topic" -p write_micro_essay --model claude-sonnet-4-5 > micro.txt
cat micro.txt | fabric -p tweet --model claude-haiku
```

**Technical Strategy**:

```bash
fabric "feature idea" -p create_prd --model claude-sonnet-4-5 > prd.txt
cat prd.txt | fabric -p create_design_document --model claude-sonnet-4-5 > design.txt
cat design.txt | fabric -p create_threat_model --model claude-opus-4
```

---

## Best Practices

### Model Selection Guidelines

1. **Start with balance** - Use `claude-sonnet-4-5` as default
2. **Upgrade for critical tasks** - Use `claude-opus-4` for security, critical analysis
3. **Downgrade for volume** - Use `gemini-2.5-flash` for high-volume, quick tasks
4. **Use thinking models** - Use `gemini-2.0-flash-thinking-exp` for complex reasoning
5. **Chain appropriately** - Use faster models for extraction, slower for synthesis

### Pattern Chaining Guidelines

1. **Extract → Analyze** - Fast model → Slow model
2. **Analyze → Create** - Slow model → Balanced model
3. **Create → Improve** - Balanced model → Slow model
4. **Extract → Learn** - Balanced model → Fast model

### Cost Optimization

```bash
# Bad: Using opus for everything
fabric -u "URL" -p extract_main_idea --model claude-opus-4  # Overkill

# Good: Match model to task
fabric -u "URL" -p extract_main_idea --model gemini-2.5-flash  # Perfect match

# Bad: Single expensive call
fabric -u "URL" -p extract_article_wisdom --model claude-opus-4  # Expensive

# Good: Chain with appropriate models
fabric -u "URL" -p extract_article_wisdom --model claude-sonnet-4-5 > wisdom.txt
cat wisdom.txt | fabric -p create_5_sentence_summary --model gemini-2.5-flash
```

---

## Quick Reference Matrix

| Task | Fast Strategy | Balanced Strategy | Quality Strategy |
| ---- | ------------- | ----------------- | ---------------- |
| Summarize | `create_5_sentence_summary` + flash | `summarize` + sonnet | `extract_wisdom` → `summarize` + opus |
| Learn | `youtube_summary` + flash | `extract_wisdom` + sonnet | `extract_wisdom` → `create_flash_cards` + opus/flash |
| Code review | `review_code` + haiku | `review_code` + sonnet | `analyze_code` + opus |
| Threat model | `create_threat_model` + sonnet | `create_stride_threat_model` + opus | Full STRIDE workflow + opus |
| Content | `write_micro_essay` + sonnet | `write_essay` + sonnet | `write_essay` → `improve_writing` + opus |
| Analysis | `extract_main_idea` + flash | `analyze_*` + sonnet | `analyze_*` → `compare_and_contrast` + opus |

---

## Meta Patterns

**When unsure which pattern to use**:

```bash
fabric "I need to [task description]" -p suggest_pattern --model claude-sonnet-4-5
```

**To visualize all options**:

```bash
fabric --listpatterns | fabric -p show_fabric_options_markmap --model claude-sonnet-4-5
```

---

**See Also**:

- Complete Pattern Reference: `~/.claude/skills/fabic/fabric-patterns-reference.md`
- Model Reference: `~/.claude/skills/fabic/fabric-model-reference.md`
- Fabric Skill: `~/.claude/skills/fabric/SKILL.md`

---

**Document Version**: 1.0
**Last Updated**: 2025-11-14
