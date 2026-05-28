# Workflow Checkpoint

## 현재 상태
- 작업명: {{TASK_NAME}}
- 현재 Phase: {{CURRENT_PHASE}}
- 현재 작업: {{CURRENT_TASK}}
- 마지막 업데이트: {{UPDATED_AT}}

## 완료된 작업
{{COMPLETED_TASKS}}

## 다음 단계
- 다음 Phase: {{NEXT_PHASE}}
- 다음 작업: {{NEXT_TASK}}
- 담당 Agent: {{NEXT_AGENT}}

## 재개 명령어
```
풀스택 워크플로우 재개
```
또는
```
/fullstack-workflow resume
```

## 컨텍스트 파일 참조
- PRD 문서: prd.md
- Task 문서: task.md
- Todo 파일: .workflow/todo.md
- Phase 1 결과: .workflow/context/phase1-result.md
- Phase 2 결과: .workflow/context/phase2-result.md
- Phase 3 결과: .workflow/context/phase3-result.md
- 리뷰 결과: .workflow/context/review-result.md

## 변경된 파일 목록
{{CHANGED_FILES}}

## 재개 시 주의사항
1. checkpoint.md와 todo.md를 먼저 읽어 현재 상태 파악
2. 필요한 context 파일만 로드하여 컨텍스트 절약
3. 다음 작업부터 순차적으로 진행
