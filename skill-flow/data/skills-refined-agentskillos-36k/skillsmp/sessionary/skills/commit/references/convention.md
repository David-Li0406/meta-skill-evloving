# Commit Convention

## 커밋 메시지 형식

```text
{type}: {description}

[optional body]

[optional footer]
```

## 커밋 타입

| 타입 | 설명 | 예시 |
|------|------|------|
| `feat` | 새로운 기능 추가 | `feat: 로그인 API 구현` |
| `fix` | 버그 수정 | `fix: 세션 만료 처리 오류 수정` |
| `test` | 테스트 코드 추가/수정 | `test: 결제 서비스 단위 테스트 추가` |
| `refactor` | 기능 변경 없는 코드 개선 | `refactor: 인증 로직 함수 분리` |
| `docs` | 문서 수정 | `docs: API 엔드포인트 주석 추가` |
| `style` | 코드 포맷팅, 세미콜론 등 | `style: 린터 경고 수정` |
| `chore` | 빌드, 설정, 패키지 관리 | `chore: 의존성 업데이트` |
| `perf` | 성능 개선 | `perf: 쿼리 인덱스 최적화` |

## 작성 규칙

### Description

- 한글 사용
- 명령형으로 작성 (예: "구현", "수정", "추가", "제거")
- 50자 이내
- 마침표 없음

### Body (선택)

- 무엇을, 왜 변경했는지 설명
- 72자마다 줄바꿈

### Footer (선택)

- 이슈 참조: `Closes #123`, `Fixes #456`
- Breaking change: `BREAKING CHANGE: 설명`

## TDD 커밋 패턴

RED-GREEN-REFACTOR 사이클에서:

```text
test: {기능} 테스트 추가        # RED phase
feat: {기능} 구현               # GREEN phase
refactor: {기능} 코드 정리      # REFACTOR phase
```

## 크기 제한

- **단일 커밋**: 100줄 이하 권장
- **PR 총 변경량**: 800줄 초과 시 브랜치 분리

## Co-Author

Claude Code 사용 시:
```text
Co-Authored-By: Claude <noreply@anthropic.com>
```
