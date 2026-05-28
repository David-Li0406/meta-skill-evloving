# Modify Workflow Checkpoint

## 현재 상태
- 작업명: [작업명]
- 현재 Phase: [1-6]
- 현재 작업: [작업 번호]
- 마지막 업데이트: YYYY-MM-DD HH:MM

## Phase 진행 상황

| Phase | 상태 | 완료 시간 |
|-------|------|----------|
| Phase 1: 현황 분석 | 대기/진행중/완료 | - |
| Phase 2: 요구사항 명확화 | 대기/진행중/완료 | - |
| Phase 3: 계획 수립 | 대기/진행중/완료 | - |
| Phase 4: 구현 | 대기/진행중/완료 | - |
| Phase 5: 코드 리뷰 | 대기/진행중/완료 | - |
| Phase 6: 완료 | 대기/진행중/완료 | - |

## 다음 단계
- 다음 Phase: [Phase 번호]
- 다음 작업: [작업 설명]
- 담당 Agent: [Agent 타입]

## 재개 명령어

```
앱 수정 워크플로우 재개
```

또는

```
/app-modify-workflow resume
```

## 컨텍스트 파일 참조
- modify-todo.md: .workflow/modify-todo.md
- 분석 결과: .workflow/context/analysis-result.md
- 요구사항: .workflow/modify-requirements.md
- Phase 결과: .workflow/context/phase[N]-result.md

## 재개 시 필요한 컨텍스트

### 현재 Phase에서 필요한 파일
1. [파일 1]
2. [파일 2]

### 이전 Phase 결과 요약
- Phase 1 결과: [요약]
- Phase 2 결과: [요약]
- ...

## 보류된 이슈

| 이슈 | 상태 | 메모 |
|------|------|------|
| [이슈 1] | 보류/진행중 | [메모] |

## 메모
- [추가 메모 사항]
