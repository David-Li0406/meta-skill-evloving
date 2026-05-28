# Phase Details Reference

## SDD Phase 상세

### Phase 0 - Brainstorm (Auto-detect)

0. 아이디어가 모호한 경우 자동 활성화
   - **활성화 조건**: 모호한 표현, 아이디어 키워드, 탐색적 질문 감지
   - **프로세스**: 단일 질문 → 객관식 옵션 → 디자인 합의
   - **출력**: `design-brief.md`
   - **Skip if**: 명확한 기능 요청인 경우

**상세 워크플로우**:
1. Step 1 - 아이디어 이해: 프로젝트 상태 파악, 단일 질문으로 핵심 파악
2. Step 2 - 접근 방식 탐색: 2-3가지 객관식 옵션 제시, 트레이드오프 설명
3. Step 3 - 디자인 합의: 구조화된 디자인 브리프 작성, 섹션별 검증

> 📖 상세 가이드: [Brainstorming Guide](brainstorming-guide.md)

### Phase 1 - Specify

1. Run `/speckit.specify [feature-description]`
   - Create feature branch: `N-short-name`
   - Generate `specs/N-short-name/spec.md`
   - Validate quality

### Phase 2 - Clarify (Automatic)

2. Run `/speckit.clarify`
   - Analyze spec.md for underspecified areas
   - Generate up to 5 targeted clarification questions
   - Collect user answers
   - Update spec.md with clarifications
   - **Skip if**: No [NEEDS CLARIFICATION] markers found

### Phase 3 - Plan

3. Run `/speckit.plan`
   - Map requirements to DDD layers
   - Document technical approach
   - Create `specs/N-short-name/plan.md`

### Phase 4 - Checklist (Optional)

4. Ask user: "커스텀 체크리스트 생성할까요? (y/n)"
   - **yes** → Run `/speckit.checklist`
   - **no** → Skip to next phase

### Phase 5 - Tasks

5. Run `/speckit.tasks`
   - Break down plan into actionable tasks
   - Group by DDD layer
   - Create `specs/N-short-name/tasks.md`

### Phase 6 - Create Issues (Optional)

6. Ask user: "GitHub Issues로 변환할까요? (y/n)"
   - **yes** → Invoke `skill:create-issues`
   - **no** → Skip

### Phase 7 - Report Completion

7. Summarize all created artifacts

## Phase Flow Diagram

```
brainstorm? → specify → clarify? → plan → checklist? → tasks → issues? → report
     ↓           ↓         ↓         ↓         ↓          ↓        ↓        ↓
design-brief  spec.md  (auto)   plan.md   (ask)    tasks.md   (ask)   summary
  (auto)                                          checklist.md      GitHub
```

## Configuration Options

```yaml
# Agent can configure behavior
auto_brainstorm: true # Auto-detect vague ideas (default: true)
auto_clarify: true # Always run clarify (default: true)
auto_checklist: false # Skip checklist prompt (default: false)
auto_issues: false # Skip issues prompt (default: false)
```
