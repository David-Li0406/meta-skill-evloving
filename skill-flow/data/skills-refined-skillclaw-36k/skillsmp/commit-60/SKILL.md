---
name: commit
description: 사용자가 '커밋해줘', 'commit', '/commit' 등 커밋을 요청할 때 사용. 레이어별/기능별 커밋 분리 원칙과 메시지 형식을 따름.
---

# 커밋 가이드라인

커밋은 기능/구현 단위로 분리하여 step-by-step으로 수행합니다.

## 커밋 분리 원칙

1. **레이어별 분리**: 같은 기능이라도 레이어가 다르면 분리
   - Domain 레이어 (인터페이스, DTO, 엔티티)
   - Application 레이어 (서비스 구현)
   - Presentation 레이어 (컨트롤러, 템플릿)

2. **기능별 분리**: 독립적인 기능은 별도 커밋
   - 예: 검색 기능과 정렬 기능이 별개라면 분리
   - 예: UI 개선과 버그 수정은 분리

3. **설정/인프라 분리**: 빌드 설정, 테스트 설정 등은 별도 커밋
   - 예: JaCoCo 설정, ES 설정 등

## 커밋 메시지 형식

```
<type>: <한글 제목> (<관련 User Story>)

<본문 - 변경 내용 상세>
```

**Type 종류:**
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `refactor`: 리팩토링
- `chore`: 빌드, 설정 변경
- `docs`: 문서 변경
- `test`: 테스트 추가/수정

## 커밋 순서 예시

복잡한 기능 구현 시 권장 순서:

1. Domain 레이어: 인터페이스, DTO, 엔티티
2. Infrastructure/Application: 구현체, 서비스
3. Presentation: 컨트롤러, 뷰
4. Configuration: 빌드 설정, 환경 설정

```bash
# 예시: 용어 검색 기능 구현
git commit -m "feat: SourceDocumentAnalyzer 인터페이스에 검색 메서드 추가"
git commit -m "feat: ElasticsearchSourceDocumentAnalyzer 검색 구현"
git commit -m "feat: GlossaryService 검색 기능 추가"
git commit -m "feat: 용어 검색 UI 구현"
```
