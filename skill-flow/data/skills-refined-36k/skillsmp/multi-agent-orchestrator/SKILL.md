---
name: multi-agent-orchestrator
description: |
  Marketing multi-agent orchestration system for complex, parallelizable campaigns. Coordinates specialized AI agents for: (1) Research + synthesis + content creation pipelines, (2) Platform-specific content generation at scale (Reddit, LinkedIn, Twitter, Email), (3) Lead generation and outbound campaigns, (4) Human-in-the-loop review before any external execution, (5) Automated posting with natural timing patterns. Triggers: "build me a marketing team", "orchestrate agents", "outbound campaign", "multi-platform content", "lead generation system", "social media blitz", or any request implying coordinated marketing specialist work.
---

# Marketing Multi-Agent Orchestrator

Coordinate specialized AI agents to accomplish complex marketing workflows that would overwhelm a single agent. Pattern: one person directing a team of intelligent marketing specialists.

## Core Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     MARKETING TEAM LEAD                         │
│  • Loads context (voice, product, story, constraints)           │
│  • Decomposes campaign → subtasks                               │
│  • Assigns agents, monitors progress                            │
└─────────────────┬───────────────────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌───────┐   ┌───────┐     ┌───────┐
│RESEARCH│   │RESEARCH│     │  ...  │  ← Parallel market research
│Agent 1 │   │Agent 2 │     │       │
└───┬────┘   └───┬────┘     └───────┘
    │            │
    └─────┬──────┘
          ▼
    ┌───────────┐
    │CONTENT LEAD│  ← Synthesizes research, briefs copywriters
    └─────┬─────┘
          │
    ┌─────┼─────┐
    ▼     ▼     ▼
┌─────┐┌─────┐┌─────┐
│COPY ││COPY ││COPY │  ← Platform-specific copywriters
│  1  ││  2  ││  3  │
└──┬──┘└──┬──┘└──┬──┘
   └──────┼──────┘
          ▼
    ┌───────────┐
    │REVIEW HUB │  ← Human approval gate (REQUIRED)
    └─────┬─────┘
          ▼
    ┌───────────┐
    │ EXECUTION │  ← Browser agents, schedulers, follow-up
    └───────────┘
```

## When to Use This Skill

- **Outbound lead generation campaigns** — Finding and engaging prospects across platforms
- **Multi-platform content launches** — Coordinated messaging across Reddit, LinkedIn, Twitter, etc.
- **Research-to-content pipelines** — Market research → insights → platform-native content
- **Personalized outreach at scale** — Email sequences, DM campaigns, comment strategies
- **Brand awareness blitzes** — Rapid, coordinated presence building

## Workflow Execution

### Phase 1: Context Loading

Marketing Team Lead immediately gathers:

1. **Voice Profile** — Tone, vocabulary, personality markers, brand guidelines
2. **Product/Service Brief** — What you're selling, key differentiators, pricing
3. **Target Persona** — ICP details, pain points, where they hang out online
4. **Story Arc** — Founder journey, credibility signals, social proof, case studies
5. **Constraints** — Platforms, budget, timeline, compliance rules, no-go topics

```markdown
## Context Checklist

- [ ] Voice profile loaded (tone, vocabulary, do's/don'ts)
- [ ] Product brief reviewed (features, benefits, differentiators)
- [ ] Target persona defined (demographics, psychographics, platforms)
- [ ] Story elements ready (founder story, testimonials, proof points)
- [ ] Constraints documented (platforms, budget, compliance)
```

### Phase 2: Campaign Decomposition

Break user request into parallel-executable subtasks:

```
User: "Get me leads from Reddit and LinkedIn"
     ↓
Subtasks:
  [Research-Reddit] → Find relevant posts via API/browse
  [Research-LinkedIn] → Browse for matching discussions
  [Synthesize] → Combine findings, dedupe, prioritize
  [Create-Reddit] → Draft Reddit-native comments
  [Create-LinkedIn] → Draft LinkedIn-native comments
  [Review] → Human approval checkpoint
  [Execute] → Post with natural timing
  [Monitor] → Track responses, escalate replies
```

### Phase 3: Agent Assignment

Each subtask maps to a specialist role:

| Role                    | Responsibility                                   | Output                     |
| ----------------------- | ------------------------------------------------ | -------------------------- |
| **Reddit Scout**        | Find relevant posts, assess engagement potential | Ranked opportunity list    |
| **LinkedIn Scout**      | Identify target posts/profiles                   | Prospect list with context |
| **Content Lead**        | Synthesize research, create briefs               | Platform-specific briefs   |
| **Reddit Copywriter**   | Community-native comments                        | Draft comments + context   |
| **LinkedIn Copywriter** | Professional engagement copy                     | Draft comments/messages    |
| **Twitter Copywriter**  | Thread-aware, punchy copy                        | Tweets/thread drafts       |
| **Email Copywriter**    | Personalized outreach                            | Email sequences            |
| **Execution Agent**     | Post approved content                            | Confirmation + metrics     |

**Key principle**: Specialists don't multitask. One agent = one job.

### Phase 4: Research Execution

Research agents operate in parallel:

**Reddit Scout**:

- Search keywords in target subreddits
- Filter by recency, engagement, relevance
- Flag posts where authentic engagement makes sense
- Note community rules and norms

**LinkedIn Scout**:

- Browse industry hashtags and topics
- Identify high-engagement posts from non-competitors
- Find prospects matching ICP
- Note connection opportunities

**Output format**:

```markdown
## Research Finding

**Platform**: Reddit
**Location**: r/startups
**Post**: "How I got my first 10 customers"
**Engagement**: 47 comments, 234 upvotes
**Relevance**: HIGH — discusses exact pain point we solve
**Angle**: Share relevant insight, mention similar experience
**Risk**: LOW — genuine value-add opportunity
```

### Phase 5: Content Lead Synthesis

Content Lead does NOT write final content. Instead:

1. **Synthesizes** research into actionable briefs
2. **Identifies** platform-specific requirements
3. **Creates** detailed specs for each copywriter
4. **Maintains** brand voice consistency across outputs

**Brief format**:

```markdown
## Content Brief: Reddit Comment

**Target**: r/startups post about first customers
**Goal**: Add value, build credibility, soft brand mention
**Angle**: Share a specific tactic that worked for us
**Voice**: Casual, helpful, founder-to-founder
**Length**: 2-3 paragraphs max
**CTA**: None explicit — just be helpful
**Avoid**: Self-promotion smell, link dropping, sales pitch
```

### Phase 6: Specialist Execution

Platform specialists receive briefs and produce drafts:

**Reddit Copywriter**:

- Conversational, community-native tone
- Avoids self-promo smell (critical for Reddit)
- Adds genuine value before any mention
- Respects subreddit culture

**LinkedIn Copywriter**:

- Professional but not corporate
- Credibility-forward (stats, results, experience)
- Hook-driven opening
- Clear value proposition

**Twitter Copywriter**:

- Punchy, thread-aware
- Hashtag-strategic (not hashtag-spam)
- Quote-tweet friendly
- Engagement-optimized

**Email Copywriter**:

- Personalized opening (research-based)
- Clear, single CTA
- Spam-filter-aware language
- Follow-up sequence ready

### Phase 7: Review Hub (REQUIRED Human-in-the-Loop)

**Critical gate before ANY external action.**

Present to user:

1. All generated content with source context
2. Target destinations (specific posts, profiles, emails)
3. Proposed timing/schedule
4. One-click approve/edit/reject per item

```markdown
## Review Queue

### Item 1: Reddit Comment

**Target**: r/startups — "How I got my first 10 customers"
**Draft**:

> Great breakdown! We had a similar experience with our first 10.
> What worked for us was [specific tactic]. The key insight was
> [value-add]. Happy to share more details if helpful.

**Timing**: Today, 2:34 PM (3 hours from now)
**Status**: ⏳ Awaiting approval

[✓ Approve] [✏️ Edit] [✗ Reject]

---

### Item 2: LinkedIn Comment

**Target**: Jane Doe's post on B2B sales
**Draft**:

> This resonates. We saw a 40% increase in response rates when
> we shifted from [old approach] to [new approach]. The data
> backed what you're saying here.

**Timing**: Tomorrow, 9:15 AM
**Status**: ⏳ Awaiting approval

[✓ Approve] [✏️ Edit] [✗ Reject]
```

### Phase 8: Execution Layer

After approval, execution agents:

1. **Post content** at staggered, natural intervals
2. **Send messages** / connection requests
3. **Monitor** for replies → escalate to user immediately
4. **Track** engagement metrics
5. **Report** daily summary

**Timing rules** (critical for not looking like a bot):

- 3-15 minute random intervals between actions
- Respect platform rate limits strictly
- Pause during off-hours (user's timezone)
- Vary posting times across days
- Never bulk-post

---

## Safety & Compliance Rules

1. **Never auto-execute** — All external actions require human approval
2. **Rate limit respect** — Agents must honor platform limits (hard requirement)
3. **Identity disclosure** — Don't claim to be human when asked directly
4. **Privacy boundaries** — No scraping private data without consent
5. **Compliance hooks** — Flag potential legal/regulatory issues before execution
6. **No spam** — Quality over quantity, always
7. **Authentic value** — Every interaction must genuinely help the recipient

---

## Quick Start: Lead Gen Campaign

```bash
# 1. Load context
Team Lead reads: voice profile, product brief, target persona

# 2. Spin up research agents (parallel)
Reddit Scout: Search [keywords] in [subreddits], last 7 days, min 10 engagement
LinkedIn Scout: Browse [industry] posts, engagement > 50, last 7 days

# 3. Synthesize findings
Content Lead produces briefs for top 15 opportunities

# 4. Generate content (parallel)
Reddit Copywriter: Draft comments for 8 Reddit opportunities
LinkedIn Copywriter: Draft comments for 7 LinkedIn opportunities

# 5. Review (REQUIRED)
Present all 15 drafts in review hub
User approves 12, edits 2, rejects 1

# 6. Execute
Execution agents post 14 approved items over 2 days
Natural timing: 3-15 min random intervals
Pause overnight

# 7. Monitor & Report
Track engagement, escalate replies immediately
Daily summary: 14 posted, 3 replies, 2 profile views
```

---

## MCP Integration Points

For external services, create MCP servers:

| Service  | MCP Server   | Key Tools                                      |
| -------- | ------------ | ---------------------------------------------- |
| Reddit   | reddit-mcp   | `search_posts`, `get_comments`, `post_comment` |
| LinkedIn | linkedin-mcp | `search_posts`, `get_profile`, `send_message`  |
| Twitter  | twitter-mcp  | `search_tweets`, `post_tweet`, `reply`         |
| CRM      | crm-mcp      | `get_leads`, `update_lead`, `create_task`      |
| Email    | email-mcp    | `draft_email`, `send_email`, `schedule`        |

---

## Metrics to Track

| Metric              | Description                    | Target     |
| ------------------- | ------------------------------ | ---------- |
| Engagement rate     | Replies + reactions / posts    | >5%        |
| Reply rate          | Direct responses received      | >10%       |
| Lead conversion     | Engaged → qualified lead       | >2%        |
| Time to first reply | Hours until prospect responds  | <24h       |
| Platform health     | No warnings, bans, rate limits | 100% clean |

---

## Anti-Patterns to Avoid

| Don't                  | Do                                     |
| ---------------------- | -------------------------------------- |
| Bulk post same content | Customize each interaction             |
| Drop links immediately | Add value first, link later (if ever)  |
| Ignore community norms | Research subreddit/group culture first |
| Over-automate          | Human review on every external action  |
| Chase vanity metrics   | Focus on genuine conversations         |
| Sound like a bot       | Match platform's native voice          |
| Spam hashtags          | Use 2-3 relevant tags max              |
| Mass DM strangers      | Engage publicly first, then DM         |
