# ID8Labs Agent Suite

**Complete idea-to-exit pipeline for solo builders**

The ID8Labs Agent Suite is a collection of 9 interconnected Claude Code skills that manage the entire product lifecycle - from initial idea validation through successful exit. Built for AI-augmented solo builders who want structure without bureaucracy.

---

## Philosophy

> Structure creates momentum. Every stage has a clear exit. The documentation isn't bureaucracy—it's breadcrumbs for when you get lost.

**Core Principles:**
- **Decay mechanics** - Ideas that don't move forward decay and freeze
- **Stage gates** - Quality checkpoints prevent premature advancement
- **Calibration** - All estimates assume AI-augmented solo builder, not enterprise dev teams
- **Review rituals** - Sustainable discipline through daily/weekly/monthly rhythms
- **Skill chaining** - Outputs from one phase feed naturally into the next

---

## The 9 Skills

### 1. Tracker - Pipeline Heartbeat
The nervous system of the entire suite. Tracks all projects through lifecycle states, enforces quality gates, calculates decay, and generates dashboards.

**Commands:**
- `/tracker status` - Portfolio dashboard
- `/tracker pulse` - Daily 2-minute check
- `/tracker review` - Weekly 15-minute review
- `/tracker strategy` - Monthly 30-minute strategy
- `/tracker new <slug> <name>` - Create project
- `/tracker update <slug> <state>` - Transition state
- `/tracker ice <slug>` - Freeze project
- `/tracker kill <slug>` - Terminate project

**Features:**
- 10 lifecycle states with defined transitions
- Decay windows per state (e.g., CAPTURED=14 days, BUILDING=90 days)
- Warning at 50% decay, auto-freeze at 100%
- Gate verification before state transitions

---

### 2. Scout - Market Validation
Transforms ideas into validated (or invalidated) opportunities. Research-heavy, verdict-driven.

**Command:** `/scout <idea>`

**Process:**
1. **INTAKE** - Capture the raw idea
2. **MARKET** - TAM/SAM/SOM analysis
3. **COMPETITION** - Systematic competitive teardown
4. **COMMUNITY** - Reddit, YouTube, forum signal mining
5. **CALIBRATE** - Founder-market fit assessment
6. **SYNTHESIZE** - Final verdict

**Output:** Validation Report with BUILD / PIVOT / KILL verdict and confidence level

**Tools:** Perplexity MCP (research), Firecrawl MCP (competitor scraping)

---

### 3. Architect - Technical Design
Transforms validated ideas into buildable technical plans. Optimized for solo builder velocity.

**Command:** `/architect <project>`

**Process:**
1. **REQUIREMENTS** - Extract from validation report
2. **ARCHITECTURE** - System design patterns
3. **STACK** - Technology selection
4. **DATA** - Database schema design
5. **API** - Interface contracts
6. **INFRASTRUCTURE** - Deployment, CI/CD
7. **ROADMAP** - Phased implementation plan

**Output:** Architecture Doc + Build Roadmap (MVP → V1 → V2)

**Integrations:** database-design skill, supabase-expert skill

---

### 4. Launch - Go-to-Market
Gets built products to market effectively. One channel done well beats five done poorly.

**Command:** `/launch <project>`

**Process:**
1. **POSITIONING** - Differentiation, messaging
2. **PRICING** - Models, psychology, tiers
3. **MESSAGING** - Headlines, value props, CTAs
4. **CHANNELS** - Platform selection
5. **SEQUENCE** - Launch timeline
6. **ASSETS** - Landing page, press kit
7. **EXECUTE** - Launch day playbook

**Platform Playbooks:** Product Hunt, Hacker News, Reddit, Twitter/X

**Tools:** Perplexity MCP (positioning research), landing-page-designer skill

---

### 5. Growth - Scale Engine
Systematic experimentation and optimization. Retention beats acquisition.

**Command:** `/growth <project>`

**Process:**
1. **BASELINE** - Current metrics snapshot
2. **MODEL** - Growth loop design
3. **DIAGNOSE** - Funnel analysis (AARRR)
4. **HYPOTHESIZE** - Experiment ideas
5. **PRIORITIZE** - ICE scoring
6. **EXECUTE** - Run experiments
7. **LEARN** - Document results

**Frameworks:**
- AARRR Funnel: Acquisition → Activation → Retention → Revenue → Referral
- Growth Loops: Viral, Content, Paid, Sales
- Cohort Analysis, A/B Testing, CRO

**Tools:** Supabase MCP (user data queries), analytics-tracking skill

---

### 6. Ops - Operations Systems
Build systems, not task lists. If twice, document. If ten times, automate.

**Command:** `/ops <project>`

**Process:**
1. **AUDIT** - Current state assessment
2. **SYSTEMATIZE** - Identify repeatable processes
3. **AUTOMATE** - Build automation where ROI justifies
4. **DELEGATE** - Define handoff criteria
5. **MEASURE** - Track operational metrics
6. **OPTIMIZE** - Continuous improvement

**Templates:**
- SOP Template (Trigger → Action → Outcome)
- Ops Playbook
- Hiring Scorecard
- Delegation Framework

---

### 7. Exit - Exit Preparation
Position for and execute successful exits. 12-month prep timeline.

**Command:** `/exit <project>`

**Process:**
1. **ASSESS** - Exit readiness evaluation
2. **POSITION** - Make yourself acquirable
3. **VALUE** - Valuation methods, multiples
4. **PREPARE** - Data room, due diligence docs
5. **NEGOTIATE** - Term sheet analysis
6. **EXECUTE** - Deal close

**Exit Types:** Acqui-hire, Asset Sale, Strategic Acquisition, Private Equity, IPO (rare for solo)

**Templates:** Data Room Checklist, Exit Memo, Term Sheet Review

---

### 8. Today - Daily Operations
Daily command center for task management across all domains. Context-aware productivity method suggestions.

**Commands:**
- `/today` - Show today's view
- `/today add <task>` - Capture task
- `/today done <task>` - Mark complete
- `/today apply <method>` - Apply productivity method
- `/today suggest` - Get context-aware method suggestion
- `/today close` - End-of-day review
- `/today tomorrow` - Set up tomorrow
- `/today week` - Weekly planning view

**14 Productivity Methods:**

| Method | Best For |
|--------|----------|
| Eisenhower Matrix | Separating urgent from important |
| GTD (Getting Things Done) | Processing overload |
| Pomodoro | Focus and time awareness |
| Eat the Frog | Overcoming procrastination |
| Time Blocking | Deep work protection |
| Ivy Lee | Simple daily prioritization |
| 1-3-5 Rule | Balanced daily planning |
| Must-Should-Could | Flexible prioritization |
| Energy Mapping | Matching tasks to energy |
| Weekly Themes | Reducing context switching |
| Personal Kanban | Visual workflow |
| Two-Minute Rule | Quick task dispatch |
| Batching | Grouping similar tasks |
| Hybrid Recipes | Method combinations |

**Domains:** ID8 Projects, TV Production, Life Admin

---

### 9. LLC Ops - Entity Operations
Expert LLC operations management for ID8Labs LLC. 9 specialized agents providing PhD-level expertise in compliance, tax strategy, asset protection, and business operations.

**Agent Roster:**
| Agent | Role | Expertise |
|-------|------|-----------|
| **Sentinel** | Compliance Radar | Deadlines, audit windows |
| **Ledger** | Accounting Strategist | Expenses, deductions |
| **Filer** | Procedures Expert | Step-by-step filings |
| **Advisor** | Legal/Tax Counsel | Structure decisions |
| **Strategist** | Tax Optimizer | Proactive planning |
| **Guardian** | Risk & Protection | Insurance, liability |
| **Comptroller** | Financial Officer | Cash flow, runway |
| **Monitor** | Regulatory Tracker | Law changes, IRS updates |
| **Mentor** | Teaching Partner | Learning, proficiency |

**Quick Dispatch:**
- `sentinel: what's coming up?` - Check deadlines
- `ledger: categorize $500 MacBook charger` - Expense categorization
- `filer: walk me through 1099-NEC` - Filing guidance
- `advisor: should I elect S-Corp?` - Strategic counsel
- `strategist: minimize taxes legally` - Tax optimization
- `guardian: what insurance do I need?` - Risk assessment
- `comptroller: what's my runway?` - Financial health
- `monitor: tax law changes?` - Regulatory updates
- `mentor: explain estimated taxes` - Learning mode

**Entity:** ID8Labs LLC (Florida single-member, formed Jan 2025)

---

## Pipeline Flow

```
IDEA
  │
  ▼
┌─────────────┐
│  Scout   │  ──▶  BUILD / PIVOT / KILL
└─────────────┘
  │ BUILD
  ▼
┌─────────────┐
│ Architect│  ──▶  Architecture Doc + Roadmap
└─────────────┘
  │
  ▼
┌─────────────┐
│  [BUILD]    │  ──▶  11-Stage Pipeline (actual code)
└─────────────┘
  │
  ▼
┌─────────────┐
│  Launch  │  ──▶  Live Product
└─────────────┘
  │
  ▼
┌─────────────┐
│  Growth  │  ──▶  Stable Metrics
└─────────────┘
  │
  ▼
┌─────────────┐
│   Ops    │  ──▶  Systematized Business
└─────────────┘
  │
  ▼
┌─────────────┐
│   Exit   │  ──▶  Successful Exit
└─────────────┘

Throughout: Tracker monitors all │ Today manages daily execution
```

---

## Project Lifecycle States

| State | Description | Decay Window |
|-------|-------------|--------------|
| CAPTURED | Raw idea logged | 14 days |
| VALIDATING | Scout running | 7 days |
| VALIDATED | Scout approved, ready for architecture | 14 days |
| ARCHITECTING | Technical design in progress | 14 days |
| BUILDING | Active development | 90 days |
| LAUNCHING | Go-to-market execution | 30 days |
| GROWING | Scale and optimization | 180 days |
| OPERATING | Stable, generating revenue | 365 days |
| EXITING | Exit process active | 180 days |
| EXITED | Successfully sold/transitioned | ∞ |

**Special States:** ICE (frozen), KILLED (terminated), ARCHIVED (historical)

---

## Data Storage

All data stored as markdown files for portability and version control:

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

## MCP & Subagent Integrations

| Skill | MCPs | Subagents |
|-------|------|-----------|
| Tracker | Memory | - |
| Scout | Perplexity, Firecrawl | market-intelligence-analyst |
| Architect | - | backend-architect, database-architect |
| Launch | Perplexity, Firecrawl | frontend-developer |
| Growth | Supabase | - |
| Ops | Supabase | operations-manager |
| Exit | Perplexity, GitHub | strategic-think-tank |
| Today | - | operations-manager |
| LLC Ops | Firecrawl | 9 internal expert agents |

---

## Quick Start

1. **Capture an idea:**
   ```
   /tracker new my-app "My Awesome App"
   ```

2. **Validate it:**
   ```
   /scout my-app
   ```

3. **If BUILD verdict, design it:**
   ```
   /architect my-app
   ```

4. **Build it** (using 11-stage pipeline)

5. **Launch it:**
   ```
   /launch my-app
   ```

6. **Grow it:**
   ```
   /growth my-app
   ```

7. **Systematize it:**
   ```
   /ops my-app
   ```

8. **Exit it:**
   ```
   /exit my-app
   ```

**Daily management:**
```
/today              # See today's tasks
/tracker pulse      # 2-minute portfolio check
```

---

## Built For

- **Solo founders** building multiple products
- **Indie hackers** who want structure without overhead
- **AI-augmented builders** moving fast with discipline
- **Serial builders** who need repeatable processes

---

## Version

**Current:** 1.2.0
**Last Updated:** 2025-12-21
**Skills:** 9 (including LLC Ops with 9 internal expert agents)
**Methods:** 14
**Files:** 94+

---

*Built by ID8Labs - Ideation studio for nonlinear thinking tools*
