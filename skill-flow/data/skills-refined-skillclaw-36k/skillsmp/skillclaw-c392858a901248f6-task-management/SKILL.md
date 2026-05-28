---
name: task-management
description: Use this skill when you need to manage issue assignments, track progress, and interact with a Supabase database for automation.
---

# Skill body

## Purpose

This skill allows you to manage issue assignments, track progress, and automate workflows using a Supabase database. It includes functionalities for assigning tasks, checking progress, and directly querying the database.

## 🔴 Data Source

| Version | Data Source | Method |
|---------|-------------|--------|
| v1.x    | GitHub Projects | GraphQL API |
| **v2.0**| **Supabase** | `issues` and `issue_status_history` tables |

## Triggers

- `/SEMO:task-management` command
- Keywords: "어디까지 했어", "현황", "체크리스트", "진행도"
- Automatically invoked when an issue number is provided

## Execution Flow

1. **Check Current Issue Status**
   ```sql
   SELECT
     i.number,
     i.title,
     i.type,
     i.status,
     i.state,
     i.labels,
     i.estimation_point,
     ap.name AS assignee_name,
     TO_CHAR(i.created_at, 'YYYY-MM-DD') AS created_at,
     TO_CHAR(i.updated_at, 'YYYY-MM-DD') AS updated_at
   FROM issues i
   LEFT JOIN agent_personas ap ON i.assignee_id = ap.id
   WHERE i.number = 123
     AND i.office_id = '{office_uuid}';
   ```

2. **Update Issue Assignment**
   ```sql
   UPDATE issues
   SET
     assignee_id = '{assignee_uuid}',
     estimation_point = 4,
     body = body || E'\n\n---\n\n## 📊 작업량 산정\n\n- [ ] API 엔드포인트 구현: 2점\n- [ ] DTO 클래스 작성: 1점\n- [ ] 테스트 코드 작성: 1점\n\n**총점: 4점** (예상 소요: 2일)',
     status = 'todo',
     updated_at = NOW()
   WHERE number = 123;
   ```

3. **Check Status Change History**
   ```sql
   SELECT
     ish.from_status,
     ish.to_status,
     TO_CHAR(ish.changed_at, 'YYYY-MM-DD HH24:MI') AS changed_at,
     ap.name AS changed_by
   FROM issue_status_history ish
   LEFT JOIN agent_personas ap ON ish.changed_by = ap.id
   WHERE ish.issue_id = (
     SELECT id FROM issues WHERE number = 123
   )
   ORDER BY ish.changed_at DESC;
   ```

4. **Direct Supabase Queries (Fallback)**
   - Use when the Spring Boot backend is down or for direct database access.
   - Example command to select data:
   ```bash
   curl -s "${SUPABASE_URL}/rest/v1/{table}?select=*" \
     -H "apikey: ${SERVICE_ROLE_KEY}" \
     -H "Authorization: Bearer ${SERVICE_ROLE_KEY}"
   ```

## Quick Checks

| Step | Command |
|------|---------|
| Current Branch | `git branch --show-current` |
| PR Check | `gh pr list --head {branch} --json number,isDraft` |
| Lint | `npm run lint` |
| Type Check | `npm run type-check` |

## Notes

- Ensure to use the correct environment variables for Supabase access.
- The skill integrates with Slack for notifications when tasks are assigned.