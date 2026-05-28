# Interview Question Sets

## Frontend Engineer - Mid-Level

### Technical Questions (60 min)

#### JavaScript Core (20 min)
1. **Closures & Scope**
   - Q: Explain the output of this code and why:
     ```javascript
     for (var i = 0; i < 3; i++) {
       setTimeout(() => console.log(i), 1000);
     }
     ```
   - Expected: Understanding of var hoisting, event loop, closure solutions (let/IIFE)

2. **Async Programming**
   - Q: What's the difference between Promise.all(), Promise.race(), and Promise.allSettled()?
   - Expected: Error handling strategies, use case scenarios

3. **Event Loop**
   - Q: What's the execution order?
     ```javascript
     console.log('1');
     setTimeout(() => console.log('2'), 0);
     Promise.resolve().then(() => console.log('3'));
     console.log('4');
     ```
   - Expected: 1, 4, 3, 2 — understanding microtask vs macrotask queue

#### React/Vue (20 min)
4. **State Management**
   - Q: When would you use useReducer instead of useState?
   - Expected: Complex state logic, state dependencies, performance optimization

5. **Performance Optimization**
   - Q: How do you prevent unnecessary re-renders in React?
   - Expected: React.memo, useMemo, useCallback, component structure

6. **Virtual DOM**
   - Q: Explain the reconciliation process in React/Vue
   - Expected: Diffing algorithm, key prop importance, fiber architecture (React)

#### CSS/Styling (10 min)
7. **Layout**
   - Q: Implement a 3-column layout where center column is fluid and side columns are fixed 200px
   - Expected: Flexbox or Grid solution, fallback for older browsers

8. **Specificity**
   - Q: Which style applies and why?
     ```css
     div#main .content { color: blue; }
     #main div.content { color: red; }
     ```
   - Expected: Specificity calculation (1,1,1 vs 1,0,2)

#### Browser/Web APIs (10 min)
9. **Storage**
   - Q: Compare localStorage, sessionStorage, IndexedDB, and cookies
   - Expected: Size limits, persistence, use cases, security

10. **Security**
    - Q: How do you prevent XSS attacks in a React app?
    - Expected: Input sanitization, dangerouslySetInnerHTML risks, CSP headers

---

## Backend Engineer - Senior Level

### System Design (90 min)

#### Design Question 1: Rate Limiter (45 min)
**Scenario**: Design a distributed rate limiting service for an API gateway handling 100K RPS

**Expected Discussion Points**:
- Algorithm choice (Token Bucket, Leaky Bucket, Fixed Window, Sliding Window)
- Data store (Redis with sliding window + Lua script)
- Distributed consistency (race conditions, clock skew)
- Scalability (sharding strategy, cache hierarchy)
- Monitoring (error budgets, alerting thresholds)

**Sample Solution**:
```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Client    │─────▶│  API Gateway │─────▶│   Backend   │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │ Rate Limiter │
                     │  (Redis)     │
                     └──────────────┘
                            │
                      ┌─────┴─────┐
                      ▼           ▼
                  [Shard 1]   [Shard 2]
```

#### Design Question 2: News Feed (45 min)
**Scenario**: Design Instagram-like news feed with 500M DAU

**Key Requirements**:
- Feed generation (pull vs push vs hybrid)
- Ranking algorithm (engagement score, recency, personalization)
- Cache strategy (user feed cache, post cache)
- Database schema (followers graph, posts, interactions)
- Scale estimation (storage, bandwidth, QPS)

---

## Algorithm & Data Structures (60 min)

### Easy (15 min)
1. **Two Sum** (LeetCode #1)
   - Input: `nums = [2,7,11,15], target = 9`
   - Output: `[0,1]`
   - Expected: Hash map solution, O(n) time complexity

### Medium (30 min)
2. **LRU Cache** (LeetCode #146)
   - Implement get() and put() in O(1) time
   - Expected: Hash map + doubly linked list, explain eviction policy

3. **Binary Tree Level Order Traversal** (LeetCode #102)
   - Input: `[3,9,20,null,null,15,7]`
   - Output: `[[3],[9,20],[15,7]]`
   - Expected: BFS with queue, discuss DFS alternative

### Hard (15 min)
4. **Merge k Sorted Lists** (LeetCode #23)
   - Expected: Min heap approach, analyze O(N log k) complexity
   - Follow-up: How would you optimize for very large k?

---

## Behavioral Questions (30 min)

### Leadership & Collaboration
1. **Conflict Resolution**
   - Q: "Tell me about a time you disagreed with a technical decision"
   - STAR framework expected:
     - **S**ituation: Monolith vs microservices debate
     - **T**ask: Balance scalability needs with team capacity
     - **A**ction: Created POC, analyzed trade-offs, presented data
     - **R**esult: Hybrid approach adopted, reduced deployment time by 40%

2. **Project Ownership**
   - Q: "Describe your most challenging project and how you delivered it"
   - Look for: Scope definition, risk management, stakeholder communication

### Growth Mindset
3. **Learning from Failure**
   - Q: "Tell me about a production incident you caused"
   - Red flags: Blame others, no lessons learned
   - Green flags: Take ownership, implemented safeguards, shared learnings

4. **Mentorship**
   - Q: "How do you help junior engineers grow?"
   - Expected: Code review practices, pairing sessions, documentation culture

---

## Difficulty Level Legend
- 🟢 **Junior**: 1-2 years experience
- 🟡 **Mid**: 3-5 years experience
- 🔴 **Senior**: 5+ years experience
- 🟣 **Staff**: 8+ years, architecture focus

## Time Allocation Guide
| Role Level | Coding | System Design | Behavioral |
|------------|--------|---------------|------------|
| Junior     | 60%    | 10%           | 30%        |
| Mid        | 50%    | 25%           | 25%        |
| Senior     | 30%    | 45%           | 25%        |
| Staff      | 15%    | 60%           | 25%        |
