---
name: semo-feedback-management
description: Use this skill when you need to collect, analyze, and manage user feedback for SEMO packages using the Supabase database.
---

# Skill body

## Purpose

This skill is designed to collect user feedback related to SEMO packages, analyze it, and manage the creation of issues in the Supabase `issues` table.

## 🔴 Data Source Change (v2.0.0)

| Version | Data Source | Method |
|---------|-------------|--------|
| v1.x    | GitHub Issues | `gh api` CLI |
| **v2.0** | **Supabase** | Querying the `issues` table |

## Workflow

1. **Collect Feedback**: Gather feedback type (bug or feature), title, and detailed description from the user.
2. **Create Issue**: Insert the feedback into the Supabase `issues` table.
3. **Analyze Feedback**: Retrieve and analyze existing feedback issues to prioritize and recommend actions.

## 🔴 Phase 1: Collecting Feedback

### Step 1: Gather Feedback Information

Collect the following from the user:
- Feedback type (bug / feature)
- Title
- Detailed description (steps to reproduce, expected results, etc.)

### Step 2: Insert Feedback into Supabase

```typescript
// Using Supabase client to create an issue
const { data, error } = await supabase
  .from('issues')
  .insert({
    office_id: officeId,  // Current Office ID
    title: `[Feedback] ${title}`,
    body: body,
    type: feedbackType,  // 'bug' or 'feature'
    state: 'open',
    status: 'backlog',
    labels: ['feedback', packageName]
  })
  .select('number')
  .single();
```

### Step 3: Output Completion Message

Provide the user with the issue number once the feedback has been successfully recorded.

## 🔴 Phase 2: Analyzing Feedback

### Step 1: Retrieve Feedback Issues

```typescript
// Querying feedback issues from Supabase
const { data: feedbacks, error } = await supabase
  .from('issues')
  .select(`
    number,
    title,
    body,
    type,
    status,
    labels,
    created_at,
    assignee:agent_personas(name)
  `)
  .eq('state', 'open')
  .contains('labels', ['feedback'])
  .order('created_at', { ascending: false });
```

### Step 2: Analyze Feedback

Evaluate each feedback issue based on:
- Validity: Is the request clear and feasible?
- Duplication: Does it overlap with existing issues?
- Implementation: Which package/skill needs modification?
- Difficulty: What is the scope and complexity of the change?
- Impact: How does it affect other functionalities?

### Step 3: Identify Duplicates

```sql
-- Check for similar closed issues
SELECT number, title, state
FROM issues
WHERE title ILIKE '%{keyword}%'
  AND state = 'closed'
ORDER BY created_at DESC
LIMIT 5;
```

## 🔴 Non-Negotiable Rules

- **Local Modifications Prohibited**: This skill must not modify local skill files directly.
- **Feedback must include 'feedback' label**: Ensure that the `labels` column contains the value `feedback`.

## Conclusion

This skill integrates the processes of collecting and managing user feedback for SEMO packages, ensuring that all feedback is properly recorded and analyzed for future improvements.