---
name: faion-hr-recruiter
description: "HR Recruiter role: talent acquisition, employer branding, EVP, structured interviews, STAR method, candidate experience, onboarding, 30-60-90 day plans, ATS optimization, retention strategies, hiring compliance, DEI in hiring. 5 methodologies."
user-invocable: false
allowed-tools: Read, Write, Edit, Task, WebSearch, AskUserQuestion, TodoWrite, Glob
---

# HR Recruiter Domain Skill

**Communication: User's language. Job descriptions and HR documents: target audience language.**

## Purpose

Orchestrates all HR and recruiting activities from talent acquisition strategy to employee retention. Covers employer branding, structured hiring, interviewing, onboarding, HR tech stack optimization, and compliance.

---

## Agents

| Agent | Purpose | Modes/Skills |
|-------|---------|--------------|
| faion-recruiter-agent | Full-cycle recruiting | sourcing, screening, interviewing |
| faion-onboarding-agent | Employee onboarding | 30-60-90 plans, orientation |
| faion-employer-brand-agent | Employer branding & EVP | content, careers page |

---

## References

Detailed technical context for specialized areas:

| Reference | Content | Lines |
|-----------|---------|-------|
| [ats-platforms.md](ats-platforms.md) | ATS comparison, AI recruiting tools | ~400 |
| [hr-compliance.md](hr-compliance.md) | Hiring laws, DEI compliance, GDPR | ~300 |
| [interview-questions.md](interview-questions.md) | STAR questions bank by competency | ~500 |

---

## Workflows

### Workflow 1: Full-Cycle Recruiting

```
Job requisition → Job description → Sourcing → Screening → Interviews → Offer → Onboarding
```

### Workflow 2: Employer Branding

```
EVP audit → Employee research → Competitor analysis → EVP development → Content creation → Career page
```

### Workflow 3: Structured Hiring

```
Define competencies → Create scorecard → Design interview → Train interviewers → Execute → Debrief
```

### Workflow 4: Onboarding

```
Pre-boarding → Day 1 orientation → 30-day plan → 60-day check → 90-day review
```

---

## Methodologies (45)

### Talent Acquisition (12)

#### recruitment-funnel-optimization

**Problem:** High candidate drop-off, long time-to-hire.

**Framework:**
| Stage | Metric | Benchmark |
|-------|--------|-----------|
| Awareness | Career page visits | - |
| Application | Application rate | 8-12% |
| Screening | Screen-to-interview | 20-30% |
| Interview | Interview-to-offer | 15-25% |
| Offer | Offer acceptance | 85-95% |
| Onboarding | 90-day retention | 90%+ |

**Agent:** faion-recruiter-agent

#### multi-channel-sourcing

**Problem:** Over-reliance on job boards, limited talent pool.

**Framework:**
| Channel | Best For | Effort |
|---------|----------|--------|
| LinkedIn | Passive candidates | High |
| Employee referrals | Culture fit | Low |
| Job boards | Active seekers | Medium |
| University partnerships | Entry-level | Medium |
| Communities/Slack | Niche roles | Medium |
| Agency | Hard-to-fill | $$$$ |

**Agent:** faion-recruiter-agent

#### skills-based-hiring

**Problem:** Degree requirements exclude qualified candidates.

**Framework:**
1. Identify essential skills for role
2. Remove unnecessary degree requirements
3. Create skills assessments
4. Evaluate portfolio/projects
5. Use structured interviews

**Result:** 76% of orgs report successful hires from previously "unqualified" candidates.

**Agent:** faion-recruiter-agent

#### job-description-writing

**Problem:** JDs that don't attract qualified candidates.

**Framework:**
| Section | Content |
|---------|---------|
| Hook | Why this role matters |
| Impact | What you'll accomplish |
| Requirements | Must-have skills (5-7 max) |
| Nice-to-have | Bonus skills (3-4 max) |
| Benefits | Compensation, perks |
| Culture | Team, values |

**Agent:** faion-recruiter-agent

#### candidate-persona-development

**Problem:** Unclear target candidate profile.

**Framework:**
```markdown
## Candidate Persona: [Name]

### Demographics
- Experience: X-Y years
- Current role: [title]
- Industry: [sectors]

### Motivations
- Career goals: [what they want]
- Values: [what matters]
- Deal-breakers: [what they avoid]

### Channels
- Where they spend time online
- How they job search
- What content they consume

### Messaging
- What resonates with them
- Objections to address
```

**Agent:** faion-employer-brand-agent

#### passive-candidate-outreach

**Problem:** Low response rates from passive candidates.

**Framework:**
| Element | Best Practice |
|---------|---------------|
| Subject | Personalized, no "job opportunity" |
| Opening | Reference their work specifically |
| Value prop | Why this matters to THEM |
| CTA | Low commitment (chat, not apply) |
| Follow-up | 3 touches, different angles |

**Response rate target:** 25-40%

**Agent:** faion-recruiter-agent

#### internal-mobility-program

**Problem:** Losing talent to external opportunities.

**Framework:**
| Component | Implementation |
|-----------|----------------|
| Internal job board | All roles posted internally first |
| Skills inventory | Track employee skills/interests |
| Career conversations | Quarterly development talks |
| Stretch assignments | Cross-functional projects |
| Transparency | Clear promotion criteria |

**Agent:** faion-recruiter-agent

#### talent-pipeline-building

**Problem:** Reactive hiring, scrambling when role opens.

**Framework:**
1. Identify critical roles
2. Build warm candidate list
3. Nurture with content/updates
4. Track engagement
5. Activate when role opens

**Agent:** faion-recruiter-agent

#### recruitment-metrics-dashboard

**Problem:** No visibility into recruiting performance.

**Framework:**
| Metric | Frequency | Target |
|--------|-----------|--------|
| Time-to-fill | Weekly | < 45 days |
| Cost-per-hire | Monthly | < $4,000 |
| Quality of hire | Quarterly | > 80% performance |
| Offer acceptance | Weekly | > 85% |
| Source effectiveness | Monthly | By channel |
| Candidate NPS | Ongoing | > 50 |

**Agent:** faion-recruiter-agent

#### ats-optimization

**Problem:** ATS bottlenecks, poor candidate experience.

**Framework:**
| Area | Optimization |
|------|--------------|
| Application | < 5 min, mobile-friendly |
| Parsing | Test with real resumes |
| Automation | Auto-reject, auto-schedule |
| Communication | Templated but personalized |
| Analytics | Track funnel conversion |

**Agent:** faion-recruiter-agent

#### ai-recruiting-tools

**Problem:** Manual screening takes too long.

**Framework:**
| Tool Type | Use Case |
|-----------|----------|
| AI sourcing | Find passive candidates |
| Resume screening | Match skills to JD |
| Chatbots | Answer FAQs, schedule |
| Video interviewing | Async first rounds |
| Assessment | Skills/culture fit |

**Ethics:** Audit for bias, ensure transparency.

**Agent:** faion-recruiter-agent

#### recruitment-marketing

**Problem:** Employer brand not reaching target candidates.

**Framework:**
| Channel | Content Type |
|---------|--------------|
| Career page | Company culture, benefits |
| LinkedIn | Employee stories, behind-scenes |
| Glassdoor | Response to reviews |
| Events | Tech talks, meetups |
| Blog | Engineering/team content |

**Agent:** faion-employer-brand-agent

### Employer Branding (8)

#### employee-value-proposition

**Problem:** No clear reason for candidates to choose you.

**Framework:**
| Component | Question |
|-----------|----------|
| Compensation | What do they earn? |
| Benefits | What perks do they get? |
| Career | How will they grow? |
| Culture | What's it like to work here? |
| Purpose | Why does the work matter? |

**EVP Statement:**
```
For [target candidates]
Who want [career goals]
[Company] offers [key benefits]
That enable [outcomes]
Unlike [competitors]
We [differentiator]
```

**Agent:** faion-employer-brand-agent

#### employer-brand-audit

**Problem:** Disconnected perception vs reality.

**Framework:**
| Source | Analysis |
|--------|----------|
| Glassdoor | Rating, review themes |
| LinkedIn | Follower growth, engagement |
| Candidate surveys | Experience feedback |
| Employee surveys | What they value |
| Exit interviews | Why people leave |

**Agent:** faion-employer-brand-agent

#### careers-page-optimization

**Problem:** Career page doesn't convert visitors.

**Framework:**
| Element | Best Practice |
|---------|---------------|
| Headline | Clear EVP statement |
| Video | 60-90s culture video |
| Jobs | Easy search, filter |
| Content | Employee testimonials |
| CTA | Simple apply process |
| Mobile | Fully responsive |

**Agent:** faion-employer-brand-agent

#### employee-testimonials

**Problem:** No authentic employee voices.

**Framework:**
| Format | Use Case |
|--------|----------|
| Written quotes | Career page, JDs |
| Video testimonials | Social, careers page |
| Day-in-the-life | Blog content |
| LinkedIn posts | Organic reach |
| Podcast/interview | Deep dive |

**Prompt questions:**
- Why did you join?
- What surprised you?
- What's your favorite part?
- How have you grown?

**Agent:** faion-employer-brand-agent

#### glassdoor-management

**Problem:** Negative reviews hurting recruiting.

**Framework:**
| Action | Frequency |
|--------|-----------|
| Monitor reviews | Weekly |
| Respond professionally | Within 48h |
| Encourage happy employees | Quarterly |
| Address feedback internally | Ongoing |
| Track rating trend | Monthly |

**Agent:** faion-employer-brand-agent

#### employer-brand-content-calendar

**Problem:** Inconsistent employer brand content.

**Framework:**
| Week | Content | Channel |
|------|---------|---------|
| 1 | Employee spotlight | LinkedIn |
| 2 | Behind-the-scenes | Instagram |
| 3 | Culture moment | LinkedIn |
| 4 | Job opening promo | All |

**Agent:** faion-employer-brand-agent

#### dei-employer-branding

**Problem:** Not attracting diverse candidates.

**Framework:**
| Element | Implementation |
|---------|----------------|
| Language | Inclusive JD language |
| Images | Diverse representation |
| ERGs | Highlight employee groups |
| Commitment | Clear DEI statements |
| Data | Share diversity metrics |

**Agent:** faion-employer-brand-agent

#### talent-community-building

**Problem:** Candidates lost after rejection.

**Framework:**
1. Invite quality candidates to talent community
2. Send monthly newsletter (content, not jobs)
3. Notify when relevant role opens
4. Track engagement
5. Prioritize engaged candidates

**Agent:** faion-employer-brand-agent

### Interviewing & Selection (10)

#### structured-interview-design

**Problem:** Inconsistent, biased interviews.

**Framework:**
| Component | Implementation |
|-----------|----------------|
| Competencies | 4-6 key skills for role |
| Questions | Same questions for all candidates |
| Scoring | 1-5 scale with rubric |
| Panel | Multiple interviewers |
| Debrief | Structured discussion |

**Agent:** faion-recruiter-agent

#### star-interview-method

**Problem:** Vague, unhelpful interview answers.

**Framework:**
| Component | Prompt |
|-----------|--------|
| **S**ituation | "Tell me about a time when..." |
| **T**ask | "What was your responsibility?" |
| **A**ction | "What did you do?" |
| **R**esult | "What was the outcome?" |

**Follow-ups:**
- "What would you do differently?"
- "What did you learn?"

**Agent:** faion-recruiter-agent

#### behavioral-interview-questions

**Problem:** Wrong questions, wrong hires.

**Framework by competency:**
| Competency | Question |
|------------|----------|
| Leadership | "Tell me about leading a team through change" |
| Problem-solving | "Describe solving a complex problem" |
| Collaboration | "Give an example of cross-functional work" |
| Communication | "Describe delivering difficult feedback" |
| Adaptability | "Tell me about adjusting to major change" |

**Agent:** faion-recruiter-agent

#### interview-scorecard

**Problem:** Subjective, undocumented evaluations.

**Framework:**
```markdown
## Interview Scorecard: [Candidate] - [Role]

### Competency Ratings (1-5)
| Competency | Score | Notes |
|------------|-------|-------|
| Technical skills | 4 | Strong Python, weak SQL |
| Communication | 5 | Articulate, clear examples |
| Problem-solving | 3 | Needed prompting |
| Culture fit | 4 | Values aligned |

### Overall: Hire / No Hire / Maybe

### Key Strengths:
### Areas of Concern:
### Questions for Next Round:
```

**Agent:** faion-recruiter-agent

#### technical-assessment-design

**Problem:** Can't verify technical skills.

**Framework:**
| Type | Best For |
|------|----------|
| Take-home project | Deep evaluation, async |
| Live coding | Problem-solving, thinking |
| Code review | Real-world skills |
| System design | Senior roles |
| Pair programming | Collaboration |

**Best practices:**
- Time-box (2-4 hours max)
- Real-world scenarios
- Clear evaluation criteria
- Compensate candidate time

**Agent:** faion-recruiter-agent

#### culture-fit-assessment

**Problem:** Technical match, culture mismatch.

**Framework:**
| Approach | Implementation |
|----------|----------------|
| Values interview | Questions on values alignment |
| Team lunch/coffee | Informal culture assessment |
| Work simulation | Day-in-the-life scenario |
| Reference questions | "How did they handle X?" |

**Warning:** "Culture fit" ≠ "like us". Focus on values, not personality.

**Agent:** faion-recruiter-agent

#### reference-check-framework

**Problem:** References don't reveal real performance.

**Framework:**
| Question | Purpose |
|----------|---------|
| "What was their role?" | Verify claims |
| "What did they excel at?" | Strengths |
| "Where could they improve?" | Development areas |
| "How did they handle pressure?" | Stress response |
| "Would you rehire them?" | Ultimate question |

**Agent:** faion-recruiter-agent

#### interviewer-training

**Problem:** Interviewers introduce bias.

**Framework:**
| Topic | Training Content |
|-------|-----------------|
| Structured interviews | Why and how |
| Bias awareness | Common biases to avoid |
| Legal compliance | What you can't ask |
| Evaluation | Using scorecards |
| Candidate experience | Creating positive interaction |

**Agent:** faion-recruiter-agent

#### hiring-committee-debrief

**Problem:** Loudest voice wins hiring decision.

**Framework:**
1. Submit scorecards before debrief
2. No discussion until all submitted
3. Review discrepancies first
4. Focus on evidence, not impressions
5. Decide: Hire / No hire / More info needed

**Agent:** faion-recruiter-agent

#### offer-management

**Problem:** Losing candidates at offer stage.

**Framework:**
| Stage | Action |
|-------|--------|
| Pre-offer | Verbal commitment, understand expectations |
| Offer | Competitive, personalized package |
| Negotiation | Know your limits, be flexible |
| Close | Create urgency, address concerns |
| Counter-offer | Prepare for competing offers |

**Agent:** faion-recruiter-agent

### Onboarding (8)

#### 30-60-90-day-plan

**Problem:** New hires flounder without direction.

**Framework:**
| Phase | Focus | Goals |
|-------|-------|-------|
| **Days 1-30** | Learn | Company, team, processes |
| **Days 31-60** | Contribute | Small projects, collaboration |
| **Days 61-90** | Execute | Independent work, measurable output |

**Template:**
```markdown
## 30-60-90 Day Plan: [Name] - [Role]

### Days 1-30: Learning
- [ ] Complete orientation
- [ ] Meet all team members
- [ ] Understand key processes
- [ ] Shadow team members
- [ ] Complete required training

### Days 31-60: Contributing
- [ ] Own first small project
- [ ] Participate in meetings actively
- [ ] Build cross-functional relationships
- [ ] Identify one improvement area

### Days 61-90: Executing
- [ ] Deliver first major project
- [ ] Work independently
- [ ] Contribute to team goals
- [ ] Plan next quarter priorities
```

**Agent:** faion-onboarding-agent

#### preboarding-process

**Problem:** New hires anxious before day 1.

**Framework:**
| Timeline | Action |
|----------|--------|
| Offer signed | Welcome email, next steps |
| 2 weeks before | Equipment shipping, accounts setup |
| 1 week before | Schedule, team intro email |
| Day before | Reminder, point of contact |

**Agent:** faion-onboarding-agent

#### day-one-orientation

**Problem:** Chaotic, overwhelming first day.

**Framework:**
| Time | Activity |
|------|----------|
| 9:00 | Welcome, intro to buddy |
| 9:30 | HR paperwork, benefits |
| 10:30 | IT setup, tools walkthrough |
| 12:00 | Team lunch |
| 1:30 | Company overview, culture |
| 3:00 | Manager 1:1, expectations |
| 4:00 | Self-paced onboarding |

**Agent:** faion-onboarding-agent

#### buddy-program

**Problem:** New hires feel isolated.

**Framework:**
| Element | Implementation |
|---------|----------------|
| Selection | Tenured, positive employees |
| Training | Set expectations, guidelines |
| Duration | 90 days minimum |
| Check-ins | Weekly for first month |
| Topics | Culture, unwritten rules, navigation |

**Agent:** faion-onboarding-agent

#### onboarding-checklist

**Problem:** Missing critical setup items.

**Framework:**
```markdown
## Onboarding Checklist: [Name]

### Before Day 1
- [ ] Equipment ordered/shipped
- [ ] Accounts created (email, Slack, tools)
- [ ] Welcome email sent
- [ ] Team notified
- [ ] Buddy assigned

### Day 1
- [ ] Warm welcome from team
- [ ] IT setup complete
- [ ] Paperwork signed
- [ ] Benefits enrollment
- [ ] First 1:1 with manager

### Week 1
- [ ] All key meetings scheduled
- [ ] Access to all systems verified
- [ ] Training modules assigned
- [ ] Introduction to key stakeholders

### Month 1
- [ ] 30-day check-in complete
- [ ] Goals defined
- [ ] Feedback collected
- [ ] Blockers addressed
```

**Agent:** faion-onboarding-agent

#### manager-onboarding-guide

**Problem:** Managers unprepared for new hires.

**Framework:**
| Timeframe | Manager Action |
|-----------|----------------|
| Pre-start | Set up workspace, schedule 1:1s |
| Day 1 | Welcome, set expectations |
| Week 1 | Daily check-ins, introduce team |
| Month 1 | Weekly 1:1s, early feedback |
| Month 3 | 90-day review, goal setting |

**Agent:** faion-onboarding-agent

#### onboarding-feedback-loop

**Problem:** Don't know if onboarding works.

**Framework:**
| Touchpoint | Survey/Action |
|------------|---------------|
| Week 1 | Quick pulse survey |
| Day 30 | Detailed onboarding survey |
| Day 60 | Check-in conversation |
| Day 90 | Full review, eNPS |

**Questions:**
- Did you feel welcomed?
- Was your role clear?
- Did you have the tools you needed?
- How could we improve?

**Agent:** faion-onboarding-agent

#### remote-onboarding

**Problem:** Remote hires feel disconnected.

**Framework:**
| Challenge | Solution |
|-----------|----------|
| Isolation | Virtual coffee chats, buddy program |
| Equipment | Ship well before day 1 |
| Culture | Extra culture sessions, documentation |
| Communication | Over-communicate, multiple channels |
| Bonding | Virtual team activities |

**Agent:** faion-onboarding-agent

### Retention & Development (4)

#### employee-retention-strategies

**Problem:** High turnover, losing talent.

**Framework:**
| Driver | Strategy |
|--------|----------|
| Compensation | Market-rate pay, regular reviews |
| Growth | Clear career paths, L&D budget |
| Recognition | Regular appreciation, bonuses |
| Flexibility | Remote options, work-life balance |
| Culture | Belonging, inclusion, purpose |

**Retention formula:** Stay interviews > Exit interviews

**Agent:** faion-recruiter-agent

#### stay-interview-framework

**Problem:** Only learn why people leave after they leave.

**Framework:**
| Question | Purpose |
|----------|---------|
| "What do you look forward to at work?" | Engagement drivers |
| "What would make you leave?" | Risk factors |
| "What would you change?" | Improvement areas |
| "Do you feel recognized?" | Recognition needs |
| "What can I do to support you?" | Manager actions |

**Frequency:** Quarterly for high performers

**Agent:** faion-recruiter-agent

#### exit-interview-analysis

**Problem:** Exit interviews not driving change.

**Framework:**
| Step | Action |
|------|--------|
| Conduct | Standardized questions, HR-led |
| Document | Consistent recording |
| Analyze | Quarterly trend analysis |
| Report | Share themes with leadership |
| Act | Implement changes |

**Key questions:**
- Why are you leaving?
- What could have kept you?
- Would you recommend us?

**Agent:** faion-recruiter-agent

#### talent-review-process

**Problem:** No visibility into talent bench.

**Framework:**
| Component | Implementation |
|-----------|----------------|
| Performance | Current results |
| Potential | Future growth capability |
| Flight risk | Likelihood of leaving |
| Succession | Ready for next role? |
| Development | What do they need? |

**9-Box Grid:**
```
        Low Perf   Med Perf   High Perf
High Pot   ?        Rising     Star
Med Pot   Risk      Solid      Strong
Low Pot   Exit      Stable     Expert
```

**Agent:** faion-recruiter-agent

### Compliance & Process (3)

#### hiring-compliance-checklist

**Problem:** Legal risk in hiring process.

**Framework:**
| Area | Requirement |
|------|-------------|
| Job posting | No discriminatory language |
| Applications | Only job-relevant questions |
| Interviews | No protected class questions |
| Assessments | Validated, job-related |
| Background checks | Proper consent, FCRA |
| Offers | Consistent criteria |
| Records | Retain per regulations |

**Agent:** faion-recruiter-agent

#### dei-hiring-practices

**Problem:** Homogeneous workforce, lack of diversity.

**Framework:**
| Stage | DEI Practice |
|-------|--------------|
| Sourcing | Diverse candidate slates |
| Job posts | Inclusive language tools |
| Screening | Blind resume review |
| Interviews | Diverse interview panels |
| Evaluation | Structured, objective criteria |
| Offers | Pay equity analysis |

**Diverse slate:** Minimum 2 underrepresented candidates for every final round

**Agent:** faion-recruiter-agent

#### recruitment-process-audit

**Problem:** Inefficiencies and inconsistencies.

**Framework:**
| Area | Audit Questions |
|------|-----------------|
| Time-to-fill | Where are delays? |
| Drop-off | Where do candidates leave? |
| Quality | Are hires performing? |
| Experience | What do candidates say? |
| Compliance | Are we legally compliant? |
| Cost | Where can we optimize? |

**Agent:** faion-recruiter-agent

---

## Execution

### Full-Cycle Recruiting

```python
# Define hiring need
AskUserQuestion(
    questions=[
        {
            "question": "What type of role?",
            "options": [
                {"label": "Technical", "description": "Engineering, DevOps, Data"},
                {"label": "Non-technical", "description": "Sales, Marketing, Ops"},
                {"label": "Leadership", "description": "Manager, Director, VP"}
            ]
        },
        {
            "question": "Hiring urgency?",
            "options": [
                {"label": "Urgent", "description": "< 30 days"},
                {"label": "Normal", "description": "30-60 days"},
                {"label": "Pipeline", "description": "Future need"}
            ]
        }
    ]
)

# Generate job description
Task(subagent_type="faion-recruiter-agent",
     prompt=f"Write job description for {role} with skills: {skills}")

# Design interview process
Task(subagent_type="faion-recruiter-agent",
     prompt=f"Create structured interview plan with {num_rounds} rounds")
```

### Employer Branding

```python
Task(subagent_type="faion-employer-brand-agent",
     prompt=f"Audit current employer brand across {channels}")

Task(subagent_type="faion-employer-brand-agent",
     prompt=f"Develop EVP based on {employee_research}")

Task(subagent_type="faion-employer-brand-agent",
     prompt=f"Create careers page content for {company}")
```

### Onboarding

```python
Task(subagent_type="faion-onboarding-agent",
     prompt=f"Create 30-60-90 day plan for {role}")

Task(subagent_type="faion-onboarding-agent",
     prompt=f"Design onboarding checklist for {department}")
```

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| faion-communicator | Interview communication, stakeholder dialogue |
| faion-project-manager | Hiring project management |
| faion-marketing-manager | Employer brand content, careers page |

---

*Domain Skill v1.0 - HR Recruiter*
*45 Methodologies | 3 Agents*
*Based on: SHRM BASK, AIHR, Gartner HR research*
