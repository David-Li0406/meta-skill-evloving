---
name: study-plan-generator
description: Generate structured study plans for 42 projects with clear phases, tasks, and learning goals. Use when planning project work, breaking down complex assignments, or organizing learning.
---

# Study Plan Generator

Create comprehensive, actionable study plans for 42 School projects.

## Purpose

Help students break down complex projects into manageable phases with:
- Clear learning objectives
- Progressive task breakdown
- Time estimates
- Checkpoints and milestones
- Resource references

## Study Plan Structure

### 1. Project Overview
```markdown
# [Project Name] - Study Plan

**Estimated Time:** [X days/weeks]  
**Difficulty:** [Beginner/Intermediate/Advanced]  
**Key Concepts:** [List main concepts]

## Project Goals
- [Goal 1]
- [Goal 2]
- [Goal 3]
```

### 2. Prerequisites Check
```markdown
## Prerequisites ✅

Before starting, you should know:
- [ ] Concept 1 (e.g., C basics)
- [ ] Concept 2 (e.g., Makefiles)
- [ ] Concept 3 (e.g., Memory management)

**Missing knowledge?** Study these first:
- [Resource for concept 1]
- [Resource for concept 2]
```

### 3. Phase Breakdown

**Standard phases for most 42 projects:**

#### Phase 0: Understanding (10-20% of time)
- Read subject thoroughly
- Research core concepts
- Understand requirements
- Check forbidden/allowed functions

#### Phase 1: Research & Planning (15-25% of time)
- Study theoretical concepts
- Analyze similar implementations
- Design data structures
- Plan architecture

#### Phase 2: Core Implementation (40-50% of time)
- Set up project structure
- Implement basic features
- Handle mandatory part
- Test continuously

#### Phase 3: Edge Cases & Bonus (15-20% of time)
- Test edge cases
- Fix bugs
- Implement bonus features
- Optimize if needed

#### Phase 4: Polish & Documentation (5-10% of time)
- Clean code
- Check norminette
- Write documentation
- Final testing

### 4. Day-by-Day Plan Template

```markdown
## Day 1: [Phase Name]

### Morning Session (2-3 hours)
**Goal:** [Specific achievable goal]

**Tasks:**
- [ ] Task 1 (30 min)
- [ ] Task 2 (45 min)
- [ ] Task 3 (30 min)

**Deliverable:** [What you should have by end]

### Afternoon Session (2-3 hours)
**Goal:** [Specific achievable goal]

**Tasks:**
- [ ] Task 1
- [ ] Task 2

**Checkpoint:** [How to verify progress]

### Learning Resources:
- [Link 1]
- [Link 2]
```

### 5. Checkpoints & Milestones

```markdown
## Checkpoints 🎯

### Checkpoint 1: [Name] (Day X)
**Verify:**
- [ ] Feature X works
- [ ] No compilation errors
- [ ] Basic test passes

**Tests:**
```bash
./program test_case_1
./program test_case_2
```

**If stuck:** [Troubleshooting tip or resource]
```

### 6. Study Techniques Section

```markdown
## Study Techniques 📚

### Active Learning
- Don't just read - code along
- Explain concepts out loud
- Draw diagrams
- Test immediately after learning

### For Focus Issues (TDAH/ADHD)
- Use Pomodoro: 25 min work + 5 min break
- Set clear micro-goals per session
- Physical movement between sessions
- Visual timers
- Reward system after checkpoints

### Practice Strategies
- Code without looking at references
- Implement twice (throw away first attempt)
- Peer review/pair programming
- Explain to rubber duck
```

## Project-Specific Templates

### For Algorithm Projects (push_swap, philosophers, etc.)

```markdown
## Phase Breakdown

### Week 1: Theory & Algorithm
**Days 1-2:** Understand the problem
- [ ] Read subject 3x
- [ ] Understand constraints
- [ ] Research algorithm types

**Days 3-4:** Design solution
- [ ] Pseudocode algorithm
- [ ] Test on paper examples
- [ ] Calculate complexity

**Day 5:** Start implementation
- [ ] Basic structure
- [ ] Input parsing
- [ ] Basic algorithm skeleton

### Week 2: Implementation
[Continue with detailed tasks...]
```

### For System Programming (minitalk, pipex, minishell)

```markdown
## Phase Breakdown

### Week 1: System Concepts
**Days 1-2:** Study system calls
- [ ] Read man pages for required functions
- [ ] Test each syscall individually
- [ ] Understand error handling

**Days 3-5:** Design architecture
- [ ] Process flow diagram
- [ ] Error handling strategy
- [ ] Test plan
```

### For Graphics Projects (so_long, cub3d, fdf)

```markdown
## Phase Breakdown

### Week 1: Library & Basics
**Days 1-2:** Learn graphics library
- [ ] MLX/miniLibX documentation
- [ ] Basic window creation
- [ ] Event handling

**Days 3-5:** Parse input
- [ ] File format understanding
- [ ] Parsing implementation
- [ ] Validation
```

## Time Management Guidelines

### Project Size Estimation
- **Small projects** (2-3 weeks): libft, get_next_line, ft_printf
- **Medium projects** (3-4 weeks): push_swap, philosophers, minitalk
- **Large projects** (4-6 weeks): minishell, cub3d, webserv

### Daily Time Blocks
- **Deep Work:** 4-6 hours of focused coding
- **Research:** 1-2 hours reading/learning
- **Testing:** 1 hour debugging/testing
- **Review:** 30 min code review/refactor

### Buffer Time
Always add 20-30% buffer for:
- Unexpected bugs
- Concept re-learning
- Evaluation prep
- Documentation

## Task Breakdown Formula

For each major feature:

1. **Understand** (10%)
   - Read about it
   - Find examples
   - Understand why needed

2. **Plan** (15%)
   - Pseudocode
   - Data structures
   - Edge cases

3. **Implement** (50%)
   - Basic version
   - Handle errors
   - Test basic cases

4. **Test & Debug** (20%)
   - Edge cases
   - Memory leaks
   - Stress tests

5. **Refactor** (5%)
   - Clean code
   - Norminette
   - Comments

## Progress Tracking

```markdown
## Progress Tracker

### Week 1
- [x] Day 1: Understanding phase ✅
- [x] Day 2: Core concepts ✅
- [ ] Day 3: Data structures
- [ ] Day 4: Basic implementation
- [ ] Day 5: Testing

### Completed Checkpoints
- [x] ✅ Checkpoint 1: Project compiles
- [x] ✅ Checkpoint 2: Basic functionality works
- [ ] Checkpoint 3: Handles edge cases
- [ ] Checkpoint 4: Norminette pass

### Blockers
- Issue: [Description]
- Solution attempted: [What you tried]
- Status: [Resolved/Pending]
```

## Learning Resources Template

```markdown
## Resources by Topic

### [Topic 1: e.g., Threading]
**Essential:**
- [Resource 1 with description]
- [Resource 2 with description]

**Advanced:**
- [Resource 3]

**Practice:**
- [Exercise or example]

### [Topic 2]
[Same structure...]
```

## Study Session Template

For daily sessions:

```markdown
## Session [Date] - [Time]

**Duration:** 25 minutes  
**Goal:** [One specific goal]

### Before Starting
- [ ] Timer set
- [ ] Distractions removed
- [ ] Goal is clear

### Tasks
1. [ ] [Specific task - 10 min]
2. [ ] [Specific task - 10 min]
3. [ ] [Review/test - 5 min]

### After Session
**Completed:** [What worked]  
**Learned:** [New knowledge]  
**Next:** [What's next session]  
**Blockers:** [Any issues]
```

## Anti-Patterns to Avoid

❌ **Don't:**
- Start coding before understanding
- Skip planning phase
- Work on everything at once
- Ignore testing until the end
- Copy-paste without understanding
- Work 10 hours straight

✅ **Do:**
- Break into small, testable pieces
- Test after each feature
- Take regular breaks
- Ask for help when stuck 2+ hours
- Review code before moving forward
- Maintain consistent daily progress

## Example: Mini Study Plan

```markdown
# philosophers - 5 Day Intensive Plan

## Day 1: Theory (4 hours)
- [ ] Morning: Read subject + understand problem (2h)
- [ ] Afternoon: Study threads & mutexes basics (2h)
- **Checkpoint:** Can explain problem to someone

## Day 2: Setup (6 hours)
- [ ] Morning: Project structure + parsing (3h)
- [ ] Afternoon: Data structures + init (3h)
- **Checkpoint:** Program compiles and validates input

## Day 3: Core Logic (8 hours)
- [ ] Morning: Thread creation + routine (4h)
- [ ] Afternoon: Eat/sleep/think actions (4h)
- **Checkpoint:** One philosopher works

## Day 4: Synchronization (8 hours)
- [ ] Morning: Multiple philos + fork handling (4h)
- [ ] Afternoon: Death detection + monitor (4h)
- **Checkpoint:** 5 philos run without dying

## Day 5: Polish (6 hours)
- [ ] Morning: Edge cases + testing (3h)
- [ ] Afternoon: Norminette + cleanup (3h)
- **Checkpoint:** Ready for evaluation
```

## Adaptation Tips

### For ADHD/Focus Issues:
- Reduce session length to 15-20 min
- More frequent rewards
- Physical activity between sessions
- Visual progress trackers
- Accountability partner

### For Fast Learners:
- Combine phases
- Add bonus challenges
- Explore optimization
- Help peers (teaching reinforces)

### For Struggling Students:
- Extend timeframes
- More checkpoints
- Pair programming
- Seek help earlier
- Focus on understanding over speed
