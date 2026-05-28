---
name: handoff-writer
description: Automatically generates handoff documents for the next agent after completing a stage
---

# Handoff Writer Skill

## 목적
에이전트 작업 완료 시 다음 에이전트를 위한 핸드오프 문서 자동 생성

## 실행 시점
모든 에이전트 작업 완료 직후

## 작성 내용
1. **수행한 작업**: 구체적인 작업 내용 나열
2. **중요 기술적 결정**: 기술 스택, 아키텍처, 라이브러리 선택 등 중요한 결정과 근거
3. **생성/수정한 파일**: 파일 경로와 목적
4. **다음 에이전트에게 전달할 정보**: 다음 단계에서 반드시 알아야 할 핵심 내용
5. **미해결 이슈나 주의사항**: 해결되지 않은 문제나 주의해야 할 사항
6. **검증 결과**: 테스트/검증 수행 여부 및 결과

## 출력 형식
마크다운 형식으로 `.agent/handoffs/XX-{stage}-summary.md`에 저장

### 파일명 규칙
- `01-plan-summary.md` - 계획 수립 단계
- `02-architect-summary.md` - 아키텍처 설계 단계
- `03-implement-summary.md` - 구현 단계
- `04-test-summary.md` - 테스트 단계
- `05-docs-summary.md` - 문서화 단계
- `06-final-summary.md` - 최종 검증 단계

### 템플릿 구조

```markdown
# {에이전트명} 작업 완료 요약

## 수행한 작업
- 구체적인 작업 내용 1
- 구체적인 작업 내용 2
- ...

## 주요 결정사항
### {결정 제목}
- **결정 내용**: ...
- **선택 이유**: ...
- **대안 검토**: ...

## 생성/수정한 파일
- `파일경로1` - 목적 및 주요 기능
- `파일경로2` - 목적 및 주요 기능
- ...

## 다음 에이전트에게 전달할 정보
### 필수 확인 사항
- 다음 단계에서 반드시 알아야 할 내용

### 참조할 파일
- `파일경로` - 참조 목적

## 미해결 이슈 및 주의사항
- [ ] 미해결 이슈 1
- [ ] 미해결 이슈 2
- ⚠️ 주의사항: ...

## 검증 결과
- [x] 구문 검증 통과
- [x] 테스트 실행 성공
- [ ] 보안 체크 (다음 단계에서 수행)

## 다음 단계 추천
다음 단계: {다음 워크플로우명}
진행 가능 여부: [가능/조건부 가능/불가능]
```

## 주의사항
- **비개발자도 이해할 수 있도록** 쉬운 언어 사용
- 기술 용어는 간단한 설명 추가 (예: "JWT(사용자 인증 토큰)")
- 다음 단계 진행 여부를 판단할 수 있을 만큼 **충분한 정보** 제공
- 주관적 판단보다는 **객관적 사실** 중심으로 작성
- 실패나 문제점도 솔직하게 기록

## 실행 예시

### 사용자 요청
```
agy chat "계획 수립 완료. handoff 문서 생성해줘"
```

### AI 응답
```
✅ 핸드오프 문서 생성 완료: .agent/handoffs/01-plan-summary.md

다음 단계를 진행하려면:
bash .agent/scripts/checkpoint.sh ".agent/handoffs/01-plan-summary.md" "아키텍처 설계"
```

## Context 업데이트
핸드오프 문서 생성 후 `current-context.json`도 함께 업데이트:

```json
{
  "project_name": "쇼핑몰 백엔드",
  "current_stage": "architecture",
  "completed_stages": ["planning"],
  "next_stage": "implementation",
  "key_decisions": [
    "기술 스택: Python/FastAPI 선택",
    "데이터베이스: PostgreSQL 사용"
  ],
  "project_structure": {
    "backend": "src/",
    "tests": "tests/",
    "docs": "docs/"
  },
  "pending_issues": []
}
```

## 통합 워크플로우 예시

```bash
# 1. 계획 수립
agy chat "/plan 쇼핑몰 백엔드 프로젝트"

# 2. 핸드오프 문서 자동 생성 (self-checker가 자동 호출)
# → .agent/handoffs/01-plan-summary.md 생성됨

# 3. 체크포인트 실행 (수동)
bash .agent/scripts/checkpoint.sh ".agent/handoffs/01-plan-summary.md" "아키텍처 설계"

# 4. 다음 단계 진행 (이전 핸드오프 자동 로드)
agy chat "/build"
# → 자동으로 01-plan-summary.md를 읽고 컨텍스트 이어받음
```
