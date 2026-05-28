---
id: structured-interview-design
name: "Structured Interview Design"
domain: HR
skill: faion-hr-recruiter
category: "interviewing"
---

# Structured Interview Design

## Metadata

| Field | Value |
|-------|-------|
| **ID** | structured-interview-design |
| **Name** | Structured Interview Design |
| **Category** | Interviewing |
| **Difficulty** | Intermediate |
| **Agent** | faion-recruiter-agent |
| **Related** | star-interview-method, interview-scorecard, hiring-committee-debrief |

---

## Problem

Unstructured interviews are unreliable predictors of job performance. When interviewers ask different questions and evaluate subjectively, hiring becomes inconsistent and biased. Studies show structured interviews are 2x more predictive of job performance.

---

## Framework

### Structured Interview Principles

| Principle | Implementation |
|-----------|----------------|
| **Same questions** | All candidates answer identical questions |
| **Job-related** | Questions directly tied to competencies |
| **Standardized scoring** | Rating scale with clear criteria |
| **Multiple interviewers** | Panel reduces individual bias |
| **Independent evaluation** | Score before discussing |
| **Evidence-based decisions** | Focus on examples, not impressions |

### Design Process

```
1. DEFINE JOB REQUIREMENTS
   └── Identify 4-6 key competencies

2. CREATE QUESTIONS
   └── 2-3 behavioral questions per competency

3. BUILD SCORECARD
   └── 1-5 scale with behavioral anchors

4. TRAIN INTERVIEWERS
   └── Calibration session, practice scoring

5. EXECUTE CONSISTENTLY
   └── Same process for every candidate

6. DEBRIEF OBJECTIVELY
   └── Independent scores before discussion
```

### Competency Mapping

| Role Level | Typical Competencies |
|------------|---------------------|
| **Individual Contributor** | Technical skills, problem-solving, communication, collaboration |
| **Manager** | Leadership, delegation, developing others, strategic thinking |
| **Executive** | Vision, influence, business acumen, change management |

### Question Types

| Type | When to Use | Example |
|------|-------------|---------|
| **Behavioral** | Past performance | "Tell me about a time..." |
| **Situational** | Hypothetical scenarios | "What would you do if..." |
| **Technical** | Skill assessment | "How would you design..." |
| **Motivational** | Fit and values | "Why do you want to..." |

---

## Templates

### Interview Design Document

```markdown
# Structured Interview Design: [Role]

## Role Overview
- **Title:** [Job title]
- **Level:** [IC/Manager/Director/etc.]
- **Department:** [Team]
- **Hiring Manager:** [Name]

## Key Competencies

| # | Competency | Weight | Definition |
|---|------------|--------|------------|
| 1 | Technical Skills | 30% | [Define for role] |
| 2 | Problem-Solving | 25% | [Define for role] |
| 3 | Communication | 20% | [Define for role] |
| 4 | Collaboration | 15% | [Define for role] |
| 5 | Culture Fit | 10% | [Define for role] |

## Interview Structure

### Round 1: Initial Screen (30 min)
**Interviewer:** Recruiter
**Format:** Phone/Video
**Focus:** Background, motivation, basic qualifications

**Questions:**
1. "Walk me through your background and what brought you here."
2. "What interests you about this role/company?"
3. "Tell me about your experience with [key skill]."

### Round 2: Technical/Skills (60 min)
**Interviewer:** [Name], [Title]
**Format:** Video/On-site
**Focus:** Competency 1 (Technical) and Competency 2 (Problem-Solving)

**Questions:**
1. [Technical question 1 - 20 min]
2. [Technical question 2 - 20 min]
3. "Tell me about the most complex problem you've solved." (STAR)
4. "Describe a time you had to troubleshoot under pressure." (STAR)

### Round 3: Cross-Functional (45 min)
**Interviewer:** [Name], [Title]
**Format:** Video/On-site
**Focus:** Competency 3 (Communication) and Competency 4 (Collaboration)

**Questions:**
1. "Tell me about a time you had to explain something complex to a non-technical audience." (STAR)
2. "Describe your most successful cross-functional project." (STAR)
3. "Give an example of how you handled disagreement with a colleague." (STAR)

### Round 4: Manager/Culture (45 min)
**Interviewer:** Hiring Manager
**Format:** On-site
**Focus:** Competency 5 (Culture Fit), career goals, final questions

**Questions:**
1. "What type of work environment brings out your best work?"
2. "Tell me about a time when you had to adapt to a significant change." (STAR)
3. "Where do you see yourself in 2-3 years?"
4. Candidate questions

## Scoring Guidelines

### Rating Scale
| Score | Definition |
|-------|------------|
| 5 | Exceptional - Far exceeds expectations |
| 4 | Strong - Exceeds expectations |
| 3 | Meets - Meets expectations |
| 2 | Developing - Below expectations |
| 1 | Insufficient - Does not meet requirements |

### Behavioral Anchors: Problem-Solving

| Score | Behavior |
|-------|----------|
| 5 | Solved complex, ambiguous problems; created frameworks others use |
| 4 | Identified root causes; implemented lasting solutions |
| 3 | Solved standard problems with guidance; logical approach |
| 2 | Needed significant help; struggled with ambiguity |
| 1 | Could not demonstrate problem-solving ability |
```

### Interview Scorecard

```markdown
## Interview Scorecard

**Candidate:** [Name]
**Role:** [Title]
**Interviewer:** [Your Name]
**Date:** [Date]
**Interview Type:** [Round 2 - Technical]

### Competency Scores

| Competency | Score (1-5) | Evidence/Notes |
|------------|-------------|----------------|
| Technical Skills | | |
| Problem-Solving | | |
| Communication | | |
| Collaboration | | |
| Culture Fit | | |

**Weighted Score:** [Calculate]

### Question-by-Question Notes

**Q1: [Question]**
- S: [Situation]
- T: [Task]
- A: [Action]
- R: [Result]
- Score: [ ]

**Q2: [Question]**
- S:
- T:
- A:
- R:
- Score: [ ]

### Overall Assessment

**Strengths:**
1.
2.

**Concerns:**
1.
2.

**Questions for Future Rounds:**

### Hiring Recommendation

[ ] Strong Hire - Exceeds bar, would advocate
[ ] Hire - Meets bar
[ ] Lean Hire - Meets bar with reservations
[ ] Lean No Hire - Below bar with some positives
[ ] No Hire - Does not meet bar
[ ] Strong No Hire - Clear no

**Rationale:**
```

---

## Examples

### Example: Engineering Role

**Competencies:**
1. Technical proficiency (35%)
2. System design (25%)
3. Problem-solving (20%)
4. Communication (10%)
5. Collaboration (10%)

**Interview flow:**
- Screen: Recruiter (30 min)
- Technical: Live coding (60 min)
- System Design: Architecture (45 min)
- Team Fit: Behavioral (45 min)
- Final: Engineering Manager (30 min)

### Example: Product Manager Role

**Competencies:**
1. Product sense (30%)
2. Analytical skills (25%)
3. Communication (20%)
4. Leadership without authority (15%)
5. Execution (10%)

**Interview flow:**
- Screen: Recruiter (30 min)
- Product case: Strategy/prioritization (60 min)
- Cross-functional: Work with eng/design (45 min)
- Leadership: Behavioral (45 min)
- Final: VP Product (30 min)

---

## Implementation Checklist

- [ ] Define key competencies for role
- [ ] Create standardized question bank
- [ ] Build scoring rubric with anchors
- [ ] Design interview flow (rounds, interviewers)
- [ ] Train all interviewers
- [ ] Run calibration session
- [ ] Create scorecard templates
- [ ] Set up debrief process
- [ ] Review and iterate quarterly

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Different questions | Can't compare candidates | Standardize questions |
| No scoring rubric | Subjective evaluation | Define behavioral anchors |
| Interviewers discuss first | Groupthink, bias | Independent scoring |
| Assessing "gut feel" | Not predictive | Focus on evidence |
| Too many interviewers | Candidate fatigue, redundancy | 4-5 total max |
| No training | Inconsistent execution | Calibration sessions |

---

## Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Interview-to-offer rate | 15-25% | Offer/interview ratio |
| Quality of hire | >80% meet expectations | 1-year review scores |
| Time in interview | Predictable | Track by round |
| Interviewer calibration | >80% agreement | Compare independent scores |
| Candidate experience | >4.0/5 | Post-interview survey |

---

## Related Methodologies

- **star-interview-method:** Behavioral interviewing technique
- **interview-scorecard:** Evaluation documentation
- **interviewer-training:** Calibrate interview team
- **hiring-committee-debrief:** Evidence-based decisions
- **candidate-persona-development:** Define target candidate

---

*Methodology: structured-interview-design | Interviewing | faion-recruiter-agent*
