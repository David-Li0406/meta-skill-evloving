---
name: doc-writer
description: |
  코드 문서화 전문 skill. 주석 작성, 인라인 주석 추가, 문서화 품질 검토를 수행합니다.
  사용 시기: (1) 코드에 주석 추가 요청 시 (2) 문서화 품질 검토 요청 시 (3) "문서화", "docs", "주석 추가" 키워드 사용 시 (4) 새 API endpoint 작성 후 (project)
---

# Doc Writer

코드 문서화를 수행합니다. 언어에 따라 적절한 문서화 스타일을 적용합니다.

## 지원 문서화 스타일

| 언어 | 스타일 | 예시 |
|------|--------|------|
| Kotlin | KDoc | `/** @param ... */` |
| Java | Javadoc | `/** @param ... */` |
| JavaScript/TypeScript | JSDoc | `/** @param {type} ... */` |
| Python | Docstring | `"""..."""` |
| Go | GoDoc | `// FunctionName ...` |

## 핵심 원칙

1. **DRY**: Interface에 문서 작성 시 Impl에 중복 금지
2. **독자 중심**: "왜"와 "어떻게"에 집중, "무엇"은 코드가 설명
3. **Self-Documenting Code**: 좋은 네이밍이 최고의 문서

## 문서화 우선순위

| 레이어 | 우선순위 | 방식 |
|--------|----------|------|
| Public API/Controller | ⭐⭐⭐ 필수 | Doc comment (endpoint, params, response) |
| Interface/Abstract | ⭐⭐ 권장 | Doc comment (business meaning) |
| Implementation | ⭐ 선택 | Inline comments only |
| Data types (simple) | ⭐⭐ 권장 | Inline comments |
| Data types (complex) | ⭐⭐ 권장 | Doc comment |
| Private functions | ⭐ 선택 | Inline comments |

## 워크플로우

1. 대상 파일 읽기
2. 언어 감지 및 적절한 문서화 스타일 선택
3. 레이어 유형 판단 (Controller/Service/DTO 등)
4. 우선순위에 따라 문서화 수준 결정
5. `.claude/rules/`의 프로젝트별 규칙 확인
6. 문서 주석 또는 인라인 주석 작성
7. DRY 원칙 확인 (중복 체크)
