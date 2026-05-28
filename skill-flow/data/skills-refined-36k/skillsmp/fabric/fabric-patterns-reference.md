# Fabric Patterns - Complete Categorized Reference

**Total Patterns: 240**

**Purpose**: Quick reference for selecting the right Fabric pattern based on task type and content domain.

**Last Updated**: 2025-11-14

---

## Quick Category Navigation

- [Analysis Patterns (36)](#analysis-patterns)
- [Creation Patterns (62)](#creation-patterns)
- [Extraction Patterns (41)](#extraction-patterns)
- [Summarization Patterns (20)](#summarization-patterns)
- [Improvement Patterns (12)](#improvement-patterns)
- [Security & Threat Modeling (17)](#security--threat-modeling-patterns)
- [Rating & Evaluation (8)](#rating--evaluation-patterns)
- [Utility & Transformation (22)](#utility--transformation-patterns)
- [Personal Development (22)](#personal-development-patterns)

---

## Analysis Patterns

**Purpose**: Deep analysis of content, code, documents, and claims

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `analyze_answers` | Analyze interview or survey answers | Structured analysis |
| `analyze_bill` | Full analysis of legislation or bills | Detailed breakdown |
| `analyze_bill_short` | Quick legislative analysis | Brief summary |
| `analyze_candidates` | Evaluate job or election candidates | Comparison matrix |
| `analyze_cfp_submission` | Review conference talk proposals | Feedback report |
| `analyze_claims` | Fact-check and validate claims | Truth assessment |
| `analyze_comments` | Analyze comment sections or feedback | Pattern identification |
| `analyze_debate` | Break down debate arguments | Argument mapping |
| `analyze_email_headers` | Technical email header analysis | Security analysis |
| `analyze_incident` | Security or operational incident analysis | Incident report |
| `analyze_interviewer_techniques` | Evaluate interviewer methods | Technique breakdown |
| `analyze_logs` | Log file analysis and pattern detection | Issue identification |
| `analyze_malware` | Malware behavior analysis | Threat analysis |
| `analyze_military_strategy` | Strategic military analysis | Strategic breakdown |
| `analyze_mistakes` | Learn from errors and failures | Lesson extraction |
| `analyze_paper` | Academic paper analysis | Comprehensive review |
| `analyze_paper_simple` | Quick academic paper overview | Brief analysis |
| `analyze_patent` | Patent document analysis | Technical breakdown |
| `analyze_personality` | Personality trait analysis | Profile assessment |
| `analyze_presentation` | Presentation effectiveness analysis | Improvement suggestions |
| `analyze_product_feedback` | Product feedback analysis | Feature insights |
| `analyze_proposition` | Analyze business or logical propositions | Validation report |
| `analyze_prose` | Literary prose analysis | Writing analysis |
| `analyze_prose_json` | Prose analysis in JSON format | Structured data |
| `analyze_prose_pinker` | Steven Pinker-style prose analysis | Style assessment |
| `analyze_risk` | Risk assessment and analysis | Risk matrix |
| `analyze_sales_call` | Sales conversation analysis | Performance review |
| `analyze_spiritual_text` | Religious/spiritual text analysis | Meaning extraction |
| `analyze_tech_impact` | Technology impact assessment | Impact analysis |
| `analyze_terraform_plan` | Terraform infrastructure analysis | Change assessment |
| `analyze_threat_report` | Cybersecurity threat report analysis | Threat intelligence |
| `analyze_threat_report_cmds` | Extract commands from threat reports | Command list |
| `analyze_threat_report_trends` | Identify threat trends over time | Trend analysis |
| `compare_and_contrast` | Compare two items or concepts | Comparison table |
| `identify_job_stories` | Identify job-to-be-done stories | User story list |
| `t_analyze_challenge_handling` | Personal challenge handling analysis | Self-reflection |

---

## Creation Patterns

**Purpose**: Generate new content, documents, visualizations, and artifacts

### Documentation & Planning

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `create_prd` | Product Requirements Document | PRD document |
| `create_design_document` | Technical design documentation | Design spec |
| `create_loe_document` | Level of Effort estimate document | Effort estimate |
| `create_user_story` | User story generation | Agile stories |
| `agility_story` | Agile story creation | Story format |
| `create_coding_project` | Software project specification | Project plan |
| `create_coding_feature` | Feature specification | Feature doc |
| `create_report_finding` | Security or audit finding report | Finding doc |
| `create_upgrade_pack` | Software upgrade documentation | Upgrade guide |

### Visualizations

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `create_visualization` | General data visualization | Various formats |
| `create_mermaid_visualization` | Mermaid diagram generation | Mermaid code |
| `create_mermaid_visualization_for_github` | GitHub-compatible Mermaid | Mermaid code |
| `create_markmap_visualization` | Mind map visualization | Markmap code |
| `create_excalidraw_visualization` | Excalidraw diagram | Excalidraw JSON |
| `create_graph_from_input` | Graph from text data | Graph format |
| `create_conceptmap` | Concept mapping | Concept map |
| `create_investigation_visualization` | Investigation flow diagram | Visual diagram |
| `create_ttrc_graph` | Time-to-resolution graph | Graph data |

### Content Creation

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `write_essay` | General essay writing | Essay |
| `write_essay_pg` | Paul Graham-style essay | PG-style essay |
| `write_micro_essay` | Short-form essay | Micro essay |
| `create_academic_paper` | Academic paper generation | Academic paper |
| `create_keynote` | Keynote presentation outline | Presentation |
| `create_newsletter_entry` | Newsletter content | Newsletter item |
| `create_show_intro` | Podcast/show introduction | Show intro |
| `create_story_about_people_interaction` | Story about interaction | Narrative |
| `create_story_about_person` | Biographical story | Biography |
| `create_story_explanation` | Explanatory story | Story format |
| `enrich_blog_post` | Enhance existing blog content | Enriched post |

### Learning & Education

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `create_flash_cards` | Study flashcard generation | Flashcards |
| `to_flashcards` | Convert content to flashcards | Flashcards |
| `create_quiz` | Quiz generation | Quiz questions |
| `create_reading_plan` | Reading plan creation | Reading schedule |
| `create_mnemonic_phrases` | Memory aid creation | Mnemonics |

### Creative & Art

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `create_art_prompt` | AI art prompt generation | Art prompt |
| `create_logo` | Logo design brief | Logo design |
| `create_podcast_image` | Podcast cover art description | Image spec |
| `create_aphorisms` | Philosophical aphorisms | Aphorisms |

### Technical & Code

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `create_command` | CLI command creation | Shell command |
| `create_pattern` | New Fabric pattern creation | Pattern file |
| `create_git_diff_commit` | Git commit message from diff | Commit message |
| `generate_code_rules` | Code style rules generation | Linting rules |
| `create_sigma_rules` | SIGMA detection rules | SIGMA YAML |
| `write_nuclei_template_rule` | Nuclei scanner template | Nuclei template |
| `write_semgrep_rule` | Semgrep static analysis rule | Semgrep rule |

### Business & Strategy

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `create_ai_jobs_analysis` | AI impact on jobs analysis | Job analysis |
| `create_hormozi_offer` | Alex Hormozi-style offer | Offer framework |
| `create_idea_compass` | Idea exploration framework | Compass diagram |
| `create_better_frame` | Reframe problems/situations | New perspective |
| `prepare_7s_strategy` | McKinsey 7S strategy framework | Strategy doc |

### Gaming & RPG

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `create_npc` | RPG non-player character | NPC profile |
| `create_rpg_summary` | RPG session summary | Session notes |

### Miscellaneous

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `create_diy` | DIY project instructions | Project guide |
| `create_formal_email` | Formal email drafting | Email text |
| `create_prediction_block` | Prediction statement | Prediction |
| `create_recursive_outline` | Multi-level outline | Outline |
| `create_tags` | Content tag generation | Tag list |
| `create_video_chapters` | YouTube chapter markers | Timestamps |
| `t_create_h3_career` | Career planning (H3 framework) | Career plan |
| `t_create_opening_sentences` | Opening sentence generation | Opening lines |

---

## Extraction Patterns

**Purpose**: Extract specific information, insights, or wisdom from content

### Wisdom & Insights

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `extract_wisdom` | General wisdom extraction | Key insights |
| `extract_wisdom_dm` | Daniel Miessler-style wisdom | DM-style insights |
| `extract_wisdom_nometa` | Wisdom without metadata | Pure insights |
| `extract_wisdom_agents` | Multi-agent wisdom extraction | Agent insights |
| `extract_article_wisdom` | Article-specific wisdom | Article insights |
| `extract_insights` | General insight extraction | Insights list |
| `extract_insights_dm` | Daniel Miessler-style insights | DM insights |

### Ideas & Concepts

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `extract_ideas` | General idea extraction | Idea list |
| `extract_business_ideas` | Business opportunities | Business ideas |
| `extract_book_ideas` | Key concepts from books | Book concepts |
| `extract_controversial_ideas` | Controversial points | Controversial list |
| `extract_main_idea` | Core message/thesis | Main point |
| `extract_core_message` | Central message | Core message |

### Specific Content

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `extract_recommendations` | Action recommendations | Recommendation list |
| `extract_predictions` | Future predictions | Prediction list |
| `extract_questions` | Questions raised | Question list |
| `extract_references` | Citations and references | Reference list |
| `extract_instructions` | Step-by-step instructions | Instruction list |
| `extract_patterns` | Recurring patterns | Pattern list |
| `extract_sponsors` | Sponsor mentions | Sponsor list |
| `extract_quotes` | Notable quotes | Quote list |
| `extract_skills` | Skills mentioned | Skill list |
| `extract_product_features` | Product features | Feature list |

### Technical

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `extract_algorithm_update_recommendations` | Algorithm improvements | Tech recommendations |
| `extract_poc` | Proof-of-concept code | PoC code |
| `extract_ctf_writeup` | CTF challenge writeup | Writeup text |
| `extract_domains` | Domain names from text | Domain list |
| `extract_videoid` | YouTube video IDs | Video ID list |

### Problem/Solution

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `extract_primary_problem` | Main problem identification | Problem statement |
| `extract_primary_solution` | Main solution identification | Solution statement |

### Creative & Media

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `extract_jokes` | Humor extraction | Joke list |
| `extract_song_meaning` | Song interpretation | Song analysis |
| `extract_characters` | Character list from story | Character profiles |
| `extract_main_activities` | Key activities/events | Activity list |
| `extract_latest_video` | Latest video info | Video metadata |

### Specialized

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `extract_extraordinary_claims` | Extraordinary claim identification | Claim list |
| `extract_most_redeeming_thing` | Most valuable aspect | Value statement |
| `extract_book_recommendations` | Book suggestions | Book list |
| `extract_recipe` | Recipe extraction | Recipe format |
| `extract_alpha` | Alpha/edge information | Alpha insights |
| `t_extract_intro_sentences` | Introduction sentences | Intro text |
| `t_extract_panel_topics` | Discussion panel topics | Topic list |

---

## Summarization Patterns

**Purpose**: Condense content into shorter, digestible formats

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `summarize` | General summarization | Summary |
| `create_summary` | Detailed summary creation | Long summary |
| `create_5_sentence_summary` | Ultra-concise 5-line summary | 5 sentences |
| `create_micro_summary` | Micro summary | Tweet-length |
| `summarize_micro` | Micro summarization | Brief summary |
| `summarize_meeting` | Meeting notes summary | Meeting summary |
| `summarize_paper` | Academic paper summary | Paper summary |
| `summarize_lecture` | Lecture summary | Lecture notes |
| `summarize_newsletter` | Newsletter summary | Newsletter brief |
| `summarize_debate` | Debate summary | Debate recap |
| `summarize_legislation` | Legislation summary | Bill summary |
| `summarize_rpg_session` | RPG session summary | Session recap |
| `summarize_board_meeting` | Board meeting summary | Board recap |
| `summarize_git_changes` | Git changes summary | Change log |
| `summarize_git_diff` | Git diff summary | Diff summary |
| `summarize_pull-requests` | PR summary | PR description |
| `summarize_prompt` | Prompt summary | Prompt brief |
| `youtube_summary` | YouTube video summary | Video summary |
| `create_cyber_summary` | Cybersecurity news summary | Security brief |
| `create_ul_summary` | Unsupervised Learning summary | UL summary |

---

## Improvement Patterns

**Purpose**: Enhance and refine existing content

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `improve_writing` | General writing improvement | Improved text |
| `improve_academic_writing` | Academic writing enhancement | Academic text |
| `improve_prompt` | Prompt engineering improvement | Better prompt |
| `improve_report_finding` | Security finding improvement | Enhanced finding |
| `improve_wr` | Writing refinement | Refined text |
| `review_code` | Code review and suggestions | Code review |
| `review_design` | Design review | Design feedback |
| `refine_design_document` | Design document refinement | Refined design |
| `humanize` | Make AI text more human | Humanized text |
| `clean_text` | Text cleanup and formatting | Clean text |
| `fix_typos` | Typo correction | Corrected text |
| `sanitize_broken_html_to_markdown` | HTML to clean markdown | Markdown |

---

## Security & Threat Modeling Patterns

**Purpose**: Security analysis, threat modeling, and security documentation

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `create_threat_model` | General threat modeling | Threat model |
| `create_stride_threat_model` | STRIDE methodology threat model | STRIDE model |
| `create_threat_scenarios` | Threat scenario generation | Scenarios |
| `t_threat_model_plans` | Threat model for personal plans | Personal threat model |
| `create_security_update` | Security update documentation | Security update |
| `create_network_threat_landscape` | Network threat landscape | Threat landscape |
| `ask_secure_by_design_questions` | Secure design questioning | Security questions |
| `create_sigma_rules` | SIGMA detection rule creation | SIGMA rules |
| `write_nuclei_template_rule` | Nuclei scanner template | Nuclei template |
| `write_semgrep_rule` | Semgrep static analysis rule | Semgrep rule |
| `analyze_incident` | Security incident analysis | Incident report |
| `analyze_malware` | Malware analysis | Malware report |
| `analyze_threat_report` | Threat report analysis | Threat analysis |
| `analyze_threat_report_cmds` | Extract commands from threats | Command list |
| `analyze_threat_report_trends` | Threat trend analysis | Trend report |
| `analyze_risk` | Risk analysis | Risk assessment |
| `write_hackerone_report` | HackerOne bug report | Bug report |

---

## Rating & Evaluation Patterns

**Purpose**: Assess quality, value, and effectiveness

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `rate_ai_response` | Rate AI-generated responses | Quality score |
| `rate_ai_result` | Rate AI results | Result score |
| `rate_content` | Rate content quality | Content score |
| `rate_value` | Rate value proposition | Value score |
| `judge_output` | General output judgment | Judgment |
| `label_and_rate` | Label and rate content | Label + rating |
| `check_agreement` | Agreement checking | Agreement analysis |
| `get_wow_per_minute` | Content engagement rating | WPM score |

---

## Utility & Transformation Patterns

**Purpose**: Format conversion, data transformation, and utility functions

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `convert_to_markdown` | Convert to markdown format | Markdown |
| `export_data_as_csv` | Export data as CSV | CSV file |
| `apply_ul_tags` | Apply UL tags | Tagged content |
| `md_callout` | Create markdown callouts | Callout format |
| `translate` | Text translation | Translated text |
| `ts_to_js` | TypeScript to JavaScript | JavaScript code |
| `re_js` | JavaScript regex operations | Regex |
| `tweet` | Format content as tweet | Tweet text |
| `transcribe_minutes` | Transcribe meeting minutes | Minutes text |
| `explain_code` | Code explanation | Code docs |
| `explain_docs` | Documentation explanation | Simplified docs |
| `explain_math` | Math concept explanation | Math explanation |
| `explain_project` | Project explanation | Project overview |
| `explain_terms` | Terminology explanation | Term definitions |
| `show_fabric_options_markmap` | Show Fabric options as markmap | Markmap |
| `suggest_pattern` | Suggest appropriate pattern | Pattern suggestion |
| `raw_query` | Raw LLM query | Direct response |
| `raycast` | Raycast command integration | Raycast output |
| `coding_master` | Coding assistance | Code solution |
| `solve_with_cot` | Chain-of-thought problem solving | CoT solution |
| `write_latex` | LaTeX document writing | LaTeX code |
| `write_pull-request` | Pull request description | PR text |

---

## Personal Development Patterns

**Purpose**: Self-reflection, personal growth, and life optimization

| Pattern | Use Case | Output Type |
|---------|----------|-------------|
| `t_check_dunning_kruger` | Self-awareness check | DK assessment |
| `t_check_metrics` | Personal metrics tracking | Metrics analysis |
| `t_describe_life_outlook` | Life outlook description | Outlook summary |
| `t_find_blindspots` | Identify personal blindspots | Blindspot list |
| `t_find_negative_thinking` | Negative thinking patterns | Thought patterns |
| `t_find_neglected_goals` | Identify neglected goals | Goal list |
| `t_give_encouragement` | Personal encouragement | Encouragement |
| `t_red_team_thinking` | Challenge your thinking | Critical analysis |
| `t_visualize_mission_goals_projects` | Visualize life goals | Goal visualization |
| `t_year_in_review` | Annual review | Year summary |
| `find_female_life_partner` | Life partner criteria | Partner profile |
| `find_hidden_message` | Find hidden meanings | Message analysis |
| `find_logical_fallacies` | Identify logical fallacies | Fallacy list |
| `heal_person` | Healing guidance | Healing advice |
| `provide_guidance` | General guidance | Guidance text |
| `predict_person_actions` | Predict behavior | Behavior prediction |
| `recommend_yoga_practice` | Yoga practice recommendations | Yoga plan |
| `dialog_with_socrates` | Socratic dialogue | Philosophical dialogue |
| `ask_uncle_duke` | Uncle Duke advice | Advice column |
| `model_as_sherlock_freud` | Sherlock/Freud analysis style | Character analysis |
| `philocapsulate` | Philosophical encapsulation | Philosophy summary |
| `capture_thinkers_work` | Capture thinker's methodology | Thinker profile |

---

## Advanced Pattern Selection

### Pattern Selection Decision Tree

```text
START: What do you need to do?
│
├─ ANALYZE something
│  ├─ Code → analyze_code, review_code
│  ├─ Security → analyze_malware, analyze_incident, analyze_threat_report
│  ├─ Document → analyze_paper, analyze_bill, analyze_claims
│  ├─ Business → analyze_sales_call, analyze_product_feedback
│  └─ Other → find matching analyze_* pattern
│
├─ CREATE something
│  ├─ Documentation → create_prd, create_design_document, create_report_finding
│  ├─ Visualization → create_mermaid_visualization, create_markmap_visualization
│  ├─ Security → create_threat_model, create_stride_threat_model, create_sigma_rules
│  ├─ Content → write_essay, create_keynote, create_newsletter_entry
│  └─ Other → find matching create_* or write_* pattern
│
├─ EXTRACT information
│  ├─ Wisdom/Insights → extract_wisdom, extract_insights, extract_article_wisdom
│  ├─ Ideas → extract_ideas, extract_business_ideas, extract_main_idea
│  ├─ Specific items → extract_recommendations, extract_references, extract_questions
│  └─ Technical → extract_poc, extract_algorithm_update_recommendations
│
├─ SUMMARIZE content
│  ├─ Ultra-brief → create_5_sentence_summary, create_micro_summary
│  ├─ Meeting → summarize_meeting, summarize_board_meeting
│  ├─ Technical → summarize_git_changes, summarize_paper
│  ├─ Video → youtube_summary
│  └─ General → summarize, create_summary
│
├─ IMPROVE existing content
│  ├─ Writing → improve_writing, improve_academic_writing
│  ├─ Code → review_code
│  ├─ Prompt → improve_prompt
│  └─ Cleanup → clean_text, fix_typos, humanize
│
├─ RATE or EVALUATE
│  ├─ AI output → rate_ai_response, rate_ai_result
│  ├─ Content → rate_content, rate_value
│  └─ General → judge_output, check_agreement
│
├─ TRANSFORM or CONVERT
│  ├─ Format → convert_to_markdown, export_data_as_csv
│  ├─ Code → ts_to_js, explain_code
│  └─ Language → translate
│
└─ PERSONAL DEVELOPMENT
   ├─ Self-reflection → t_find_blindspots, t_check_dunning_kruger
   ├─ Planning → t_visualize_mission_goals_projects, t_year_in_review
   └─ Growth → provide_guidance, t_give_encouragement
```

### Common Use Case Quick Reference

| User Says | Pattern Category | Top 3 Patterns |
|-----------|------------------|----------------|
| "threat model" | Security | `create_threat_model`, `create_stride_threat_model`, `create_threat_scenarios` |
| "summarize" | Summarization | `summarize`, `create_5_sentence_summary`, `create_micro_summary` |
| "extract wisdom" | Extraction | `extract_wisdom`, `extract_insights`, `extract_article_wisdom` |
| "analyze code" | Analysis | `analyze_code`, `review_code`, `explain_code` |
| "improve writing" | Improvement | `improve_writing`, `improve_academic_writing`, `humanize` |
| "create visualization" | Creation | `create_mermaid_visualization`, `create_markmap_visualization`, `create_graph_from_input` |
| "rate this" | Evaluation | `rate_content`, `judge_output`, `rate_value` |
| "main idea" | Extraction | `extract_main_idea`, `extract_core_message`, `create_5_sentence_summary` |
| "youtube" | Summarization | `youtube_summary`, `extract_wisdom`, `summarize` |
| "security update" | Security | `create_security_update`, `analyze_threat_report`, `create_threat_scenarios` |

---

## Pattern Naming Conventions

**Prefixes**:

- `analyze_*` - Deep analysis (36 patterns)
- `create_*` - Generate new content (48 patterns)
- `extract_*` - Pull specific information (41 patterns)
- `summarize_*` - Condense content (15 patterns)
- `improve_*` - Enhance existing content (5 patterns)
- `write_*` - Writing tasks (7 patterns)
- `t_*` - Personal/thinking patterns (14 patterns)
- `rate_*` / `judge_*` - Evaluation (6 patterns)

**Suffixes**:

- `*_summary` - Summarization output
- `*_visualization` - Visual output
- `*_document` - Document creation
- `*_report` - Report generation
- `*_model` - Model creation (threat models, etc.)

---

## Usage Tips

### Chaining Patterns

Patterns can be chained manually for complex workflows:

```bash
# Extract then summarize
fabric -u "URL" -p extract_wisdom > wisdom.txt
cat wisdom.txt | fabric -p create_5_sentence_summary

# Analyze then create report
fabric "$(cat code.py)" -p analyze_code > analysis.txt
cat analysis.txt | fabric -p create_report_finding
```

### Model Selection per Pattern Type

**Fast operations (extraction, summarization)**:

```bash
fabric "content" -p extract_main_idea --model gemini-2.5-flash
```

**High-quality analysis**:

```bash
fabric "content" -p analyze_paper --model claude-sonnet-4-5-20250929
```

**Maximum quality (security, threat modeling)**:

```bash
fabric "content" -p create_threat_model --model claude-opus-4-20250514
```

### Input Methods

```bash
# From URL
fabric -u "https://example.com/article" -p summarize

# From YouTube
fabric -y "https://youtube.com/watch?v=..." -p youtube_summary

# From clipboard (macOS)
pbpaste | fabric -p extract_wisdom

# From file
cat document.txt | fabric -p analyze_claims

# Direct text
fabric "your text here" -p create_5_sentence_summary
```

---

## Maintenance

**Update this reference when**:

- New patterns are added to Fabric
- Pattern categories change
- Usage patterns evolve

**To refresh pattern list**:

```bash
fabric --listpatterns
```

**See also**:

- Model Reference: `~/.claude/skills/fabric/fabric-model-reference.md`
- Fabric Skill: `~/.claude/skills/fabric/SKILL.md`

---

## Meta Patterns

**Special utility patterns for working with Fabric itself**:

- `suggest_pattern` - Get pattern suggestions based on task
- `show_fabric_options_markmap` - Visualize Fabric patterns as markmap
- `create_pattern` - Create new Fabric patterns
- `official_pattern_template` - Pattern template reference

---

**Document Version**: 1.0
**Total Patterns Documented**: 240
**Last Verified**: 2025-11-14
