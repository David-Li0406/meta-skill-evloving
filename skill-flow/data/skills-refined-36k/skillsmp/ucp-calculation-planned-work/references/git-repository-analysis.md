# Git Repository Analysis for UCP

## When to Use This Approach

Use git repository analysis when:
- Client has no Azure DevOps/Jira work items
- Work was done from planning documents
- Need retrospective analysis
- Want most accurate UCP measurement

## Process Overview

1. **Clone repository and analyze code structure**
2. **Identify use cases from:**
   - API endpoints
   - Service classes
   - Major features
   - Integration points
3. **Count transactions per use case**
4. **Classify complexity**
5. **Calculate UCP**

## Transaction Counting from Code

### Framework Operations (0.5 weight)
- HTTP routing (FastAPI, Express)
- Database queries (SQLAlchemy, Prisma ORM)
- SDK/API calls (OpenAI, Azure)
- Standard validation (Pydantic, Joi)

### Custom Logic (1.0 weight)
- Business logic
- Custom algorithms
- State management
- Orchestration
- Error handling
- Multi-step workflows

## Example: Agent Studio Pro

**Input:** 32,515 lines of code (Next.js, TypeScript, React, PostgreSQL, Redis, Pinecone, Azure, OpenAI)

**Analysis:**
- 30 use cases identified from features
- 485 UUCW from code analysis
- 15 actors (humans + systems)
- TCF 1.40 (high AI complexity)

**Result:** 821 UCP (100% coverage vs 32% from Azure DevOps User Stories alone)

## Advantages
- ✅ 100% coverage (all implemented work)
- ✅ Most accurate (±5-10%)
- ✅ No work item quality issues
- ✅ Captures infrastructure work

## Disadvantages
- ⚠️ Takes longer (2-3x time)
- ⚠️ Requires code access
- ⚠️ Retrospective only (can't estimate future)
