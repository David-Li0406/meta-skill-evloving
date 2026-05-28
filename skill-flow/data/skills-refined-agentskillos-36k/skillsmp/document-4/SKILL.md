---
name: document
description: 문서화 작업 위임. 스펙 문서 작성, 아키텍처 문서화, 의사결정 기록 시 자동 호출
---

# 문서화 프로토콜

## 실행 조건
- 스펙 문서 작성/업데이트
- 아키텍처 문서화
- 의사결정 기록
- Progress 대량 업데이트

## 위임 전략

| 문서 유형 | 에이전트 | 모델 |
|-----------|----------|------|
| 스펙 문서 | `code-architect` | **opus** |
| 아키텍처 | `code-architect` | **opus** |
| 분석 리포트 | `code-explorer` | sonnet |

## 프롬프트 템플릿

```
[대상]에 대한 문서를 작성해줘.

출력 경로: {Docs/Specs/...}
참고 포맷: {기존 문서 경로}

요구사항:
- 기존 문서 스타일 준수
- 표 형식 선호
- 불필요한 설명 최소화

완료 후 보고:
## 완료 보고
- 수행: (1줄)
- 결과: (파일 경로)
- 확인 필요: (있으면 기술)
```

## 문서 위치

| 유형 | 경로 |
|------|------|
| Assembly 스펙 | `Docs/Specs/{Assembly}.md` |
| 클래스 상세 | `Docs/Specs/{Assembly}/{Class}.md` |
| 의사결정 | `Docs/Portfolio/Decisions/{Category}.md` |
| 진행상황 | `Docs/PROGRESS.md` |
