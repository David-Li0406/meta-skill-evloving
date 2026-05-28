---
name: doc-sync
description: Sync .claude/ documentation with code changes. Use when models/migrations/routes change, after completing features, or user says "update docs", "sync documentation", "docs out of date", "update DATABASE.md/API.md/TASKS.md".
---

# Documentation Sync

Keep `.claude/` docs current with code changes.

## Quick Start

```
Task Progress (copy and check off):
- [ ] 1. Detect changes (git diff or user input)
- [ ] 2. Determine which docs to update
- [ ] 3. Read current schema/routes/code
- [ ] 4. Generate updated content
- [ ] 5. Update documentation files
- [ ] 6. Validate consistency
```

## Target Documents

| Doc | Update When | Content |
|-----|-------------|---------|
| **DATABASE.md** | New models, migrations | ERD, table schemas, indexes |
| **API.md** | Routes, controllers | Routes table, controller docs |
| **TASKS.md** | Features complete | Progress checkboxes, percentages |
| **ARCHITECTURE.md** | Gems, services | Tech stack, infrastructure |

## Auto-Detection

Map file changes to docs:

```
db/migrate/*.rb → DATABASE.md
db/schema.rb → DATABASE.md
app/models/*.rb → DATABASE.md, API.md
app/controllers/*.rb → API.md
config/routes.rb → API.md
Gemfile → ARCHITECTURE.md
```

## DATABASE.md Updates

### Generate ERD

```
┌─────────────────────┐
│       users         │
├─────────────────────┤
│ id (PK)             │
│ email (unique)      │
│ name                │
└─────────────────────┘
          │ 1
          │ has_many
          ▼ N
┌─────────────────────┐
│       posts         │
├─────────────────────┤
│ id (PK)             │
│ user_id (FK)        │
│ title               │
└─────────────────────┘
```

### Table Schema

Read `db/schema.rb` and generate:

```markdown
## users 테이블

| 컬럼명 | 타입 | Null | Default | 설명 |
|--------|------|------|---------|------|
| id | bigint | NO | AUTO | Primary Key |
| email | string | NO | - | 이메일 (unique) |
| name | string | NO | - | 사용자 이름 |

**인덱스**:
- UNIQUE INDEX index_users_on_email (email)

**연관관계**:
- has_many :posts
- has_many :comments
```

## API.md Updates

### Routes Table

```bash
rails routes --expanded
```

Parse into markdown:

```markdown
| HTTP | Path | Controller#Action | 설명 |
|------|------|-------------------|------|
| GET | / | posts#index | 커뮤니티 홈 |
| GET | /posts/:id | posts#show | 게시글 상세 |
| POST | /posts | posts#create | 게시글 생성 |
```

### Controller Actions

Document each action:

```markdown
### PostsController#index

**경로**: `GET /posts`
**인증**: 불필요
**N+1 방지**: `includes(:user)`
```

## TASKS.md Updates

### Calculate Progress

```ruby
total = 20
completed = 8
progress = (8.0 / 20 * 100).round  # => 40%
```

Update:

```markdown
## 📊 전체 진행률

- 1주차: ✅✅✅✅✅ 100% (5/5)
- 2주차: ✅✅✅⬜⬜ 60% (3/5)

**전체**: 40% (8/20)
```

### Mark Complete

Check git commits:

```bash
git log --grep="notification"
```

Update checkboxes:

```markdown
- [x] User 모델 구현 ← 완료
- [x] 알림 시스템 ← 완료
- [ ] 이메일 인증 ← 진행 중
```

## Validation

Compare code vs docs:

```
⚠️ 문서 불일치:

DATABASE.md:
  - Notification 모델이 코드에만 존재 (문서에 없음)

API.md:
  - /notifications routes가 문서에 없음

수정:
  - DATABASE.md에 Notification 추가
  - API.md에 notifications routes 추가
```

## Automation Scripts

- **Database sync**: [sync_database_docs.rb](scripts/sync_database_docs.rb) - Auto-generates DATABASE.md from schema
- **API sync**: [sync_api_docs.sh](scripts/sync_api_docs.sh) - Auto-generates API.md from routes

```bash
# Run database sync
ruby .claude/skills/doc-sync/scripts/sync_database_docs.rb

# Run API sync
bash .claude/skills/doc-sync/scripts/sync_api_docs.sh
```

## Commands Reference

```bash
cat db/schema.rb           # Read schema
rails routes --expanded    # Get routes
ls app/models/*.rb         # List models
git diff HEAD~5            # Recent changes
```

## Examples

**New model added**:
```
User: "I added Notification model, update docs"

Actions:
1. Read db/schema.rb for notifications table
2. Update DATABASE.md with ERD and schema
3. Run rails routes
4. Update API.md with notification routes
5. Mark task complete in TASKS.md
```

**Routes changed**:
```
Modified: config/routes.rb

Actions:
1. Run rails routes
2. Update API.md routes table
```

## Checklist

- [ ] DATABASE.md has all current tables
- [ ] ERD shows relationships
- [ ] API.md has all routes
- [ ] TASKS.md progress updated
- [ ] No broken references
- [ ] Manual content preserved
