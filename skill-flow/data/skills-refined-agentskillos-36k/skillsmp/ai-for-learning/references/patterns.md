# AI for Learning

## Patterns


---
  #### **Name**
AI Tutor Implementation
  #### **Description**
Building AI tutoring into courses
  #### **When To Use**
When adding AI-powered tutoring
  #### **Implementation**
    ## AI Tutor Implementation
    
    ### AI Tutor Capabilities
    | Capability | Use Case |
    |------------|----------|
    | Q&A | Answer student questions 24/7 |
    | Explanation | Re-explain concepts differently |
    | Practice | Generate practice problems |
    | Feedback | Review and critique work |
    | Encouragement | Motivate stuck students |
    
    ### Implementation Stack
    | Component | Options |
    |-----------|---------|
    | LLM | GPT-4, Claude, open source |
    | Context | Course content as RAG |
    | Interface | Chat widget, dedicated page |
    | Guardrails | Stay on topic, escalate to human |
    
    ### Prompt Engineering for Tutors
    ```
    You are a tutor for [Course Name].
    
    Your knowledge is limited to:
    [Course content/syllabus]
    
    Rules:
    - Never give direct answers to assessments
    - Use Socratic method (guide, don't tell)
    - If unsure, say "Let me connect you with the instructor"
    - Be encouraging but honest
    ```
    
    ### Hybrid Model
    | Question Type | Handle With |
    |---------------|-------------|
    | Concept clarification | AI |
    | Technical how-to | AI |
    | Personal situation | Human |
    | Complaints/feedback | Human |
    | Advanced questions | Human |
    

---
  #### **Name**
Personalized Learning Paths
  #### **Description**
AI-driven adaptive learning
  #### **When To Use**
When creating personalized experiences
  #### **Implementation**
    ## Personalized Learning Paths
    
    ### Personalization Levels
    | Level | What Adapts | Complexity |
    |-------|-------------|------------|
    | Basic | Content recommendations | Low |
    | Medium | Path through modules | Medium |
    | Advanced | Difficulty + pace + format | High |
    
    ### Basic Implementation
    1. Pre-assessment quiz
    2. AI determines starting point
    3. Skip known content
    4. Focus on gaps
    
    ### Adaptive Path Logic
    ```
    IF score < 70% on module quiz:
      → Review + alternative explanation
      → Practice problems
      → Re-assess
    IF score > 90%:
      → Skip to advanced content
      → Offer bonus challenges
    ```
    
    ### Data Points for Personalization
    - Quiz scores
    - Time spent per lesson
    - Questions asked
    - Completion patterns
    - Self-reported preferences
    
    ### Practical Personalization
    | Input | Adaptation |
    |-------|------------|
    | Failed quiz | Extra practice |
    | Fast completion | Accelerated path |
    | Repeated wrong answer | Different explanation |
    | Long time on topic | Simplified version |
    

---
  #### **Name**
AI Content Generation
  #### **Description**
Using AI to create course content
  #### **When To Use**
When developing course materials with AI
  #### **Implementation**
    ## AI Content Generation
    
    ### What AI Can Generate
    | Content Type | AI Quality | Human Role |
    |--------------|------------|------------|
    | Quiz questions | Good | Review, refine |
    | Practice problems | Good | Verify accuracy |
    | Summaries | Good | Add personality |
    | Explanations | Medium | Verify, contextualize |
    | Video scripts | Medium | Rewrite in your voice |
    | Full lessons | Low | Major editing needed |
    
    ### AI-Assisted Workflow
    1. Human: Outline and key points
    2. AI: Generate first draft
    3. Human: Edit for accuracy and voice
    4. AI: Generate variations
    5. Human: Select and refine
    
    ### Quiz Generation Prompt
    ```
    Create 5 multiple-choice questions about [topic].
    
    Format:
    - 1 correct answer
    - 3 plausible wrong answers
    - Brief explanation for correct answer
    
    Difficulty: [intermediate]
    Test: [application, not recall]
    ```
    
    ### Content Repurposing with AI
    | Source | Generate |
    |--------|----------|
    | Video transcript | Blog post, summary |
    | Blog post | Social posts, quiz |
    | Lesson | Practice problems |
    | Q&A | FAQ document |
    

---
  #### **Name**
Automated Assessment
  #### **Description**
AI-powered grading and feedback
  #### **When To Use**
When scaling assessment and feedback
  #### **Implementation**
    ## Automated Assessment
    
    ### What AI Can Assess
    | Type | AI Reliability | Best For |
    |------|----------------|----------|
    | Multiple choice | 100% | Knowledge checks |
    | Fill-in-blank | 95% | Specific answers |
    | Short answer | 80% | Concept understanding |
    | Essay/long-form | 70% | First-pass feedback |
    | Code | 85% | Functional testing |
    
    ### AI Feedback System
    1. Student submits work
    2. AI generates initial feedback
    3. Human reviews (optional for low-stakes)
    4. Student receives feedback
    5. Student can ask AI for clarification
    
    ### Rubric-Based AI Grading
    ```
    Evaluate this [essay/code/project] against:
    
    Rubric:
    - Criterion 1: [description] (X points)
    - Criterion 2: [description] (X points)
    - ...
    
    Provide:
    - Score per criterion
    - Specific feedback
    - Suggestions for improvement
    ```
    
    ### Human-in-the-Loop
    | Situation | Process |
    |-----------|---------|
    | Low-stakes quiz | AI only |
    | Practice assignments | AI + optional human |
    | Graded projects | AI draft + human review |
    | Final assessments | Human primary |
    

## Anti-Patterns


---
  #### **Name**
AI as Content Dump
  #### **Description**
Using AI to generate entire courses
  #### **Why Bad**
    Generic, soulless content.
    No unique perspective.
    Students can use AI too.
    No differentiation.
    
  #### **What To Do Instead**
    AI assists, human creates.
    Add your unique experience.
    AI for scaling, not core content.
    Keep your voice.
    

---
  #### **Name**
Over-Automation
  #### **Description**
Removing human touch entirely
  #### **Why Bad**
    Students feel isolated.
    No accountability.
    Missing the "why" this instructor.
    No relationship building.
    
  #### **What To Do Instead**
    AI for routine, human for connection.
    Regular human touchpoints.
    AI handles scale, human handles edge cases.
    Keep community human.
    

---
  #### **Name**
AI Without Guardrails
  #### **Description**
AI that goes off-topic or gives wrong answers
  #### **Why Bad**
    Misinformation to students.
    Off-topic conversations.
    Legal/liability issues.
    Student confusion.
    
  #### **What To Do Instead**
    Constrain AI to course content.
    Clear escalation to human.
    Regular monitoring.
    Feedback loop for errors.
    