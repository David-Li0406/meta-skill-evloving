# Workflow Checkpoint

## 현재 상태
- 작업명: [작업명]
- 현재 Phase: [1-5]
- 현재 작업: [작업 번호]
- 마지막 업데이트: YYYY-MM-DD HH:MM

## Phase 진행 현황

| Phase | 상태 | 완료일 |
|-------|------|--------|
| Phase 1: 계획 수립 | 대기/진행중/완료 | - |
| Phase 2: Agent 실행 | 대기/진행중/완료 | - |
| Phase 3: 코드 리뷰 | 대기/진행중/완료 | - |
| Phase 4: 최종 테스트 | 대기/진행중/완료 | - |
| Phase 5: 완료 | 대기/진행중/완료 | - |

## 다음 단계
- 다음 Phase: [Phase 번호]
- 다음 작업: [작업 설명]
- 담당 Agent: [Agent 타입]

## 재개 명령어

```
앱 개발 워크플로우 재개
```

## 컨텍스트 파일 참조
- prd.md: .workflow/prd.md
- todo.md: .workflow/todo.md
- Phase 1 결과: .workflow/context/phase1-result.md
- Phase 2 결과: .workflow/context/phase2-result.md
- Phase 3 결과: .workflow/context/phase3-result.md
- Phase 4 결과: .workflow/context/phase4-result.md

## 변경된 파일 목록

### 신규 생성
- [파일 경로]

### 수정됨
- [파일 경로]

## compact 후 필수 로드 정보

재개 시 다음 파일들을 먼저 읽어야 합니다:
1. .workflow/checkpoint.md (이 파일)
2. .workflow/todo.md (현재 작업 상태)
3. .workflow/context/phase[N]-result.md (현재 Phase 결과)
