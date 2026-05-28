# gencast Styles and Audiences

gencast supports 4 podcast styles and 4 audience levels, creating 16 possible combinations for different content needs.

## Podcast Styles

### educational (DEFAULT)
**Format:** Structured learning with explanations and examples

**Characteristics:**
- Clear topic progression
- Explanatory dialogue
- Examples and analogies
- Reinforcement of key concepts

**Best for:**
- Lecture notes
- Tutorial content
- Course materials
- Technical documentation

**Example:**
```bash
gencast lecture.md --minimal --style educational
```

---

### interview
**Format:** Question and answer conversational style

**Characteristics:**
- HOST1 asks questions
- HOST2 provides answers
- Follow-up questions
- Clarifications and elaborations

**Best for:**
- FAQ documents
- Documentation with examples
- Expert explanations
- Technical deep-dives

**Example:**
```bash
gencast api_guide.md --minimal --style interview
```

---

### casual
**Format:** Relaxed, friendly discussion

**Characteristics:**
- Conversational tone
- Natural flow
- Lighter language
- Accessible explanations

**Best for:**
- Introductory content
- Blog posts
- General overviews
- Beginner materials

**Example:**
```bash
gencast intro_guide.md --minimal --style casual
```

---

### debate
**Format:** Contrasting perspectives and critical analysis

**Characteristics:**
- Different viewpoints presented
- Critical examination
- Pros and cons discussion
- Analytical depth

**Best for:**
- Research papers
- Comparative analyses
- Opinion pieces
- Academic discussions

**Example:**
```bash
gencast research_paper.md --minimal --style debate
```

---

## Target Audiences

### general (DEFAULT)
**Level:** Broad accessibility, no assumed knowledge

**Language:**
- Plain language
- Common terms
- Analogies to everyday concepts
- Minimal jargon

**Best for:**
- Public-facing content
- Introductions
- Overviews
- General interest topics

**Example:**
```bash
gencast overview.md --minimal --audience general
```

---

### technical
**Level:** Assumes domain knowledge and technical background

**Language:**
- Technical terminology
- Industry-specific terms
- Implementation details
- Code-level discussions

**Best for:**
- API documentation
- Implementation guides
- Technical specifications
- Developer content

**Example:**
```bash
gencast api_spec.md --minimal --audience technical
```

---

### academic
**Level:** Scholarly approach with formal language

**Language:**
- Formal terminology
- Research-oriented
- Citations and references
- Theoretical frameworks

**Best for:**
- Research papers
- Academic articles
- Scholarly analyses
- Theoretical discussions

**Example:**
```bash
gencast thesis_chapter.md --minimal --audience academic
```

---

### beginner
**Level:** Introductory level, assumes no prior knowledge

**Language:**
- Simple explanations
- Step-by-step progression
- Frequent clarifications
- Encouraging tone

**Best for:**
- Getting started guides
- First-time learner content
- Introductory courses
- Onboarding materials

**Example:**
```bash
gencast getting_started.md --minimal --audience beginner
```

---

## Style × Audience Matrix

| Style/Audience | general | technical | academic | beginner |
|----------------|---------|-----------|----------|----------|
| **educational** | Course materials | Technical training | Academic lectures | Intro tutorials |
| **interview** | General Q&A | Tech deep-dives | Research discussions | Beginner FAQs |
| **casual** | Blog posts | Dev chats | Informal seminars | Friendly intros |
| **debate** | Opinion pieces | Tech comparisons | Academic critique | Simple pros/cons |

## Common Combinations

### 1. Educational + General (DEFAULT)
```bash
gencast doc.md --minimal
```
Structured learning for broad audience - most versatile combination.

### 2. Interview + Technical
```bash
gencast api_docs.md --minimal --style interview --audience technical
```
Q&A format for developers - great for documentation.

### 3. Casual + Beginner
```bash
gencast intro.md --minimal --style casual --audience beginner
```
Friendly, approachable introduction - best for onboarding.

### 4. Debate + Academic
```bash
gencast paper.md --minimal --style debate --audience academic
```
Scholarly critical analysis - ideal for research content.

### 5. Educational + Technical
```bash
gencast training.md --minimal --style educational --audience technical
```
Structured technical training - good for engineering courses.

### 6. Interview + General
```bash
gencast faq.md --minimal --style interview --audience general
```
Accessible Q&A - works well for product docs.

## Selection Guide

### By Content Type

**Lecture Notes:** educational + general/technical
**API Documentation:** interview + technical
**Research Paper:** debate + academic
**Blog Post:** casual + general
**Tutorial:** educational + beginner/general
**FAQ:** interview + general/beginner
**Whitepaper:** educational + academic
**Product Guide:** casual + general
**Course Material:** educational + beginner/general
**Technical Spec:** educational + technical

### By Learning Goal

**Understanding concepts:** educational + audience level
**Exploring details:** interview + audience level
**Getting comfortable:** casual + beginner/general
**Critical thinking:** debate + audience level

## Tips

1. **Start with defaults** - educational + general works for most content
2. **Match formality** - casual/beginner for approachable, academic for formal
3. **Consider prior knowledge** - beginner assumes nothing, technical assumes domain expertise
4. **Use debate sparingly** - best for content with multiple perspectives
5. **Interview for Q&A** - natural format for FAQ-style documents
