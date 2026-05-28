# ID8Labs Agent Suite - Manifest

**Version:** 1.2.0
**Purpose:** Complete idea-to-exit pipeline for ID8Labs products
**Philosophy:** Claude Code IS the orchestrator. Each skill shapes Claude's approach for a specific lifecycle phase.

---

## Quick Reference

| Skill | Purpose | Trigger |
|-------|---------|---------|
| **Today** | Daily task management, methods library, cross-domain | "today", daily tasks, productivity methods |
| **Tracker** | Pipeline heartbeat, decay mechanics, dashboards | "status", "dashboard", project tracking |
| **Scout** | Market validation, competitive analysis | "validate idea", "should I build", "market research" |
| **Architect** | Technical architecture, stack selection | "how to build", "architecture", "system design" |
| **Launch** | Go-to-market, positioning, launch sequencing | "launch", "GTM", "pricing", "Product Hunt" |
| **Growth** | Growth loops, analytics, optimization | "grow", "scale", "metrics", "experiments" |
| **Ops** | SOPs, systems, delegation, team | "operations", "systematize", "SOP", "hire" |
| **Exit** | Exit prep, valuation, due diligence | "exit", "sell", "acquisition", "valuation" |
| **LLC Ops** | Entity operations, compliance, tax strategy | "LLC", "taxes", "expenses", "compliance", "filing" |
| **Media Factory** | AI media production (images, video, voice) | "video", "media", "voiceover", "production", "demo" |
| **App Store Readiness** | iOS App Store submission, first-try approval | "app store", "iOS submission", "apple review", "privacy manifest" |

---

## Skill Categories

### Daily Operations
- **today/** - Daily command center. Manages tasks across ID8 projects, TV production, and life admin. Library of 14 productivity methods with context-aware suggestions.

### Pipeline Control
- **tracker/** - The nervous system. Tracks all projects through lifecycle states, enforces quality gates, calculates decay, generates dashboards, runs review rituals.

### Validation
- **scout/** - Market validation engine. Researches TAM/SAM/SOM, analyzes competitors, mines community signals, renders BUILD/PIVOT/KILL verdicts.

### Build
- **architect/** - Technical design. Creates architecture docs, selects stack, designs data models, produces build roadmaps.

### Launch
- **launch/** - Go-to-market execution. Positioning, pricing, launch sequencing, landing page copy, press kits.

### Growth
- **growth/** - Scale engine. Growth loops, analytics dashboards, acquisition channels, retention optimization, A/B testing.

### Operations
- **ops/** - Operational systems. SOPs, delegation frameworks, customer success, team building.

### Exit
- **exit/** - Exit preparation. Valuation, due diligence, data rooms, deal structure, term sheet analysis.

### Entity Operations
- **llc-ops/** - LLC operations for ID8Labs LLC (Florida single-member). 9 specialized agents providing PhD-level expertise: Sentinel (compliance), Ledger (accounting), Filer (procedures), Advisor (legal/tax), Strategist (tax optimization), Guardian (risk), Comptroller (financial), Monitor (regulatory), Mentor (teaching).

### Media Production
- **media-factory/** - AI-powered multimedia production pipeline. Orchestrates Nano Banana Pro (images via fal.ai), KLING AI (video generation/animation), and ElevenLabs (voiceover) to create product demos, marketing videos, social content, and multimedia assets.

### App Store Submission
- **appstore-readiness/** - iOS App Store submission expert. 9 specialized agents (Reviewer, Designer, Privacy, Commerce, Metadata, Technical, Sentinel, Fixer, Mentor) ensure first-submission approval. Hard gate at ID8Pipeline Stage 9.

---

## Pipeline Stages

```
                    scout
                       |
          [CAPTURED] ──────> [VALIDATING] ──────> [VALIDATED]
                                                       |
                                                  architect
                                                       |
                                               [ARCHITECTING]
                                                       |
                                          ┌──── 11-stage pipeline ────┐
                                          │      (actual build)       │
                                          └───────────────────────────┘
                                                       |
                                                 [BUILDING]
                                                       |
                                                  launch
                                                       |
                                                [LAUNCHING]
                                                       |
                                                  growth
                                                       |
                                                 [GROWING]
                                                       |
                                                   ops
                                                       |
                                                [OPERATING]
                                                       |
                                                  exit
                                                       |
                                                 [EXITING]
                                                       |
                                                  [EXITED]
```

---

## Routing Logic

### When to invoke today
- User starts a work day and needs to organize tasks
- User asks "what should I do today" or "help me prioritize"
- User wants to apply a productivity method (Eisenhower, GTD, Pomodoro, etc.)
- User needs to capture tasks across domains (ID8/TV/Life)
- User asks for method suggestion based on context
- End of day review or tomorrow setup
- Morning setup ritual

### When to invoke tracker
- User asks for "status", "dashboard", or "how's the project"
- User starts a session (suggest daily pulse if not run today)
- User wants to create, update, ice, or kill a project
- After completing any other ID8Labs skill (log activity)
- Weekly/monthly review rituals

### When to invoke scout
- User has a new idea to evaluate
- User asks "should I build X?"
- User wants market research on a concept
- User needs competitive analysis
- User wants to understand if there's demand
- Project is in CAPTURED or VALIDATING state

### When to invoke architect
- scout returned BUILD verdict
- User asks "how should I build X?"
- User needs stack recommendations
- User needs database schema design
- User needs API structure
- Project is in VALIDATED state

### When to invoke launch
- Product is built and ready for users
- User asks "how do I launch X?"
- User needs landing page copy
- User needs launch strategy
- User needs pricing help
- User preparing for Product Hunt
- Project is in BUILDING (near complete) or LAUNCHING state

### When to invoke growth
- Product is live with initial users
- User asks "how do I grow X?"
- User needs help with retention/churn
- User wants analytics guidance
- User considering paid acquisition
- User wants to build viral loops
- Project is in LAUNCHING or GROWING state

### When to invoke ops
- Product has enough traction to need systems
- User is drowning in operational tasks
- User needs to document processes
- User considering hiring/delegation
- User needs customer support strategy
- Project is in GROWING or OPERATING state

### When to invoke exit
- User thinking about exit strategy
- User has received acquisition interest
- User wants to understand valuation
- User needs to prepare for due diligence
- User evaluating term sheet
- Project is in OPERATING or EXITING state

### When to invoke llc-ops
- User mentions LLC, taxes, expenses, deductions, compliance
- User asks about deadlines, annual reports, estimated taxes
- User wants to log/categorize an expense
- User needs filing guidance (EIN, 1099, annual report)
- User asks tax strategy questions (S-Corp, QBI, retirement)
- User wants to understand LLC operations, liability, protection
- User asks for financial health check (runway, cash flow)
- User wants to learn about business operations (invoke Mentor)

### When to invoke media-factory
- User needs to create video content (demos, promos, ads)
- User wants to generate images for marketing
- User needs voiceover or narration
- User asks "create a video for X"
- User wants product demo content
- User needs social media video assets
- User is preparing launch content (Stage 9)
- User wants to animate still images
- User needs explainer or tutorial video

### When to invoke appstore-readiness
- User mentions "app store", "iOS submission", "apple review"
- User asks "will this pass review?" or "check my app"
- User needs privacy manifest, privacy labels, or ATT help
- User asks about in-app purchase or subscription rules
- User needs screenshot or metadata guidance
- User receives app rejection and needs help responding
- User asks about Human Interface Guidelines (HIG)
- User preparing for TestFlight or App Store Connect
- Project reaches ID8Pipeline Stage 9 (Launch Prep) for iOS app
- User wants to know typical review timeline or submission timing

---

## Skill Relationships

### Output → Input Chains

| From Skill | Output | To Skill | Input |
|------------|--------|----------|-------|
| scout | Validation Report (BUILD) | architect | Requirements |
| architect | Architecture Doc + Roadmap | 11-stage pipeline | Build plan |
| 11-stage pipeline | Built product | launch | Launch candidate |
| launch | Live product | growth | Growth baseline |
| growth | Stable metrics | ops | Ops requirements |
| ops | Systematized business | exit | Exit candidate |

### Tracker Integration

ALL skills log activity to tracker on completion:

```
After completing work:
1. Save outputs to appropriate location
2. Log to tracker: `/tracker log {project-slug} "{skill}: {summary}"`
3. If state transition warranted, suggest: `/tracker update {project-slug} {new-state}`
```

---

## MCP Tool Assignments

| Skill | Primary MCPs | Purpose |
|-------|--------------|---------|
| today | - | Uses tracker for project tasks |
| tracker | Memory | Store cross-project patterns |
| scout | Perplexity, Firecrawl | Market research, competitor scraping |
| architect | - | Uses existing skills (database-design, supabase-expert) |
| launch | Perplexity, Firecrawl | Positioning research, landing page analysis |
| growth | Supabase | Query user data for analysis |
| ops | Supabase | Operational data queries |
| exit | Perplexity, GitHub | Comparable exits, repo cleanup |
| llc-ops | Firecrawl, Notion (planned) | Regulatory research, expense tracking |
| media-factory | Firecrawl, Perplexity | Reference research, trend analysis |
| appstore-readiness | Perplexity, Firecrawl | Guideline updates, Apple docs |

---

## Subagent Assignments

| Skill | Primary Subagent | Purpose |
|-------|------------------|---------|
| today | operations-manager | Daily task coordination |
| scout | market-intelligence-analyst | Research support |
| architect | backend-architect | Technical design |
| launch | frontend-developer | Landing page copy |
| growth | - | Claude direct |
| ops | operations-manager | Ops coordination |
| exit | strategic-think-tank | Exit strategy |
| llc-ops | - | 9 internal expert agents |
| media-factory | nana-image-generator | Batch image generation |
| appstore-readiness | - | 9 internal expert agents |

---

## Existing Skills Integration

ID8Labs works alongside these existing skills:

### UI/UX
- **landing-page-designer** - Used by launch for conversion-focused pages
- **ui-builder** - Used during BUILD phase for components

### Database
- **database-design** - Used by architect for schema patterns
- **supabase-expert** - Used by architect for Supabase-specific patterns

### Analytics
- **analytics-tracking** - Used by growth for instrumentation

### Testing
- **testing-qa** - Used during BUILD phase (11-stage pipeline)

---

## Commands

All ID8Labs skills are invoked as slash commands:

| Command | Skill | Description |
|---------|-------|-------------|
| `/today` | today | Show today's task view |
| `/today add <task>` | today | Capture a new task |
| `/today done <task>` | today | Mark task complete |
| `/today apply <method>` | today | Apply productivity method |
| `/today suggest` | today | Get context-aware method suggestion |
| `/today close` | today | End-of-day review |
| `/today tomorrow` | today | Set up tomorrow's priorities |
| `/today week` | today | Weekly planning view |
| `/tracker status` | tracker | Show portfolio dashboard |
| `/tracker pulse` | tracker | Daily 2-minute check |
| `/tracker review` | tracker | Weekly 15-minute review |
| `/tracker strategy` | tracker | Monthly 30-minute strategy |
| `/tracker new <slug> <name>` | tracker | Create new project |
| `/tracker update <slug> <state>` | tracker | Transition project state |
| `/tracker ice <slug>` | tracker | Freeze project |
| `/tracker thaw <slug>` | tracker | Revive frozen project |
| `/tracker kill <slug>` | tracker | Terminate project |
| `/tracker log <slug> <activity>` | tracker | Log activity |
| `/scout <idea>` | scout | Validate an idea |
| `/architect <project>` | architect | Design architecture |
| `/launch <project>` | launch | Create launch plan |
| `/growth <project>` | growth | Create growth model |
| `/ops <project>` | ops | Create ops playbook |
| `/exit <project>` | exit | Create exit memo |
| `sentinel: <query>` | llc-ops | Check deadlines, compliance |
| `ledger: <expense>` | llc-ops | Categorize expenses |
| `filer: <filing>` | llc-ops | Step-by-step filing guide |
| `advisor: <question>` | llc-ops | Legal/tax counsel |
| `strategist: <goal>` | llc-ops | Tax optimization |
| `guardian: <risk>` | llc-ops | Risk & protection |
| `comptroller: <query>` | llc-ops | Financial health |
| `monitor: <topic>` | llc-ops | Regulatory updates |
| `mentor: <topic>` | llc-ops | Learn LLC operations |
| `/media-factory plan <concept>` | media-factory | Create production plan |
| `/media-factory image <prompt>` | media-factory | Generate image (Nano Banana) |
| `/media-factory video <prompt>` | media-factory | Generate video (KLING) |
| `/media-factory voice <script>` | media-factory | Generate voiceover (ElevenLabs) |
| `/media-factory storyboard <concept>` | media-factory | Generate visual storyboard |
| `/appstore-readiness` | appstore-readiness | Full 6-phase App Store audit |
| `/appstore-review` | appstore-readiness | Quick compliance check |
| `/appstore-submit` | appstore-readiness | Step-by-step submission guide |

---

## Data Locations

```
.id8labs/
├── projects/
│   ├── active/          # Active project cards (.md)
│   ├── ice/             # Frozen projects
│   └── archive/         # Completed/killed projects
├── dashboard/
│   └── DASHBOARD.md     # Auto-generated portfolio view
├── today/
│   ├── today.md         # Current day's tasks
│   ├── tomorrow.md      # Tomorrow's planned priorities
│   ├── parking-lot.md   # Captured tasks for processing
│   └── preferences.md   # Method preferences, defaults
└── config/
    └── settings.yaml    # Reminder/decay configuration
```

---

## Philosophy

**ID8Labs** is an ideation studio for nonlinear thinking tools.

This pipeline embodies:
1. **Decay mechanics** - Ideas that don't move forward decay and freeze
2. **Stage gates** - Quality checkpoints prevent premature advancement
3. **Calibration** - All estimates assume AI-augmented solo builder, not enterprise dev teams
4. **Review rituals** - Sustainable discipline through daily/weekly/monthly rhythms
5. **Skill chaining** - Outputs from one phase feed naturally into the next

The goal: Make building repeatable, teachable, and finishable.

---

*Manifest Version 1.4.0 - Updated 2025-12-29 (Added App Store Readiness: 9-agent iOS submission system with hard gate at Stage 9)*
