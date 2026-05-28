---
name: validate
description: 이 스킬은 린트, 타입체크 및 테스트를 실행하고 모든 문제를 자동으로 수정할 때 사용합니다.
---

# Skill body

## 규칙

- 파일을 완전히 읽고 수정하기
- 증상이 아닌 근본 원인 수정하기
- 최소한의 집중된 변경하기
- 실패를 건너뛰거나 무시하지 않기
- 각 수정 후 체크 재실행하기

## 프로세스

### 1. 프로젝트 유형 감지
구성 파일을 스캔하여 프로젝트 유형을 결정합니다:

| 파일 | 프로젝트 유형 | 도구 |
|------|--------------|-------|
| `package.json` | Node.js | npm/pnpm 스크립트 |
| `pyproject.toml` / `setup.py` | Python | pytest, mypy, ruff/pylint |
| `go.mod` | Go | go vet, golangci-lint, go test |

### 2. 린트 실행
```bash
# Node.js (주요)
npm run lint
pnpm lint
npx eslint .

# Python
ruff check .
pylint **/*.py

# Go
golangci-lint run
go vet ./...
```

실패 시:
1. 오류 메시지를 주의 깊게 읽기
2. 영향을 받은 파일 전체 읽기
3. 근본 원인 식별하기
4. 최소한의 변경으로 수정하기
5. 린트 재실행하기

### 3. 타입체크 실행
```bash
# Node.js (TypeScript) (주요)
npm run typecheck
pnpm typecheck
npx tsc --noEmit

# Python
mypy .
pyright

# Go (내장)
go build ./...
```

실패 시:
1. 타입 오류 메시지 읽기
2. 타입 흐름 추적하기
3. 타입 정의 또는 사용 수정하기
4. 타입체크 재실행하기

### 4. 테스트 실행
```bash
# Node.js (주요)
npm test
pnpm test
npx jest
npx vitest

# Python
pytest

# Go
go test ./...
```

실패 시:
1. 테스트 실패 출력 읽기
2. 실패한 테스트 코드 읽기
3. 테스트 중인 구현 읽기
4. 테스트 또는 코드가 잘못되었는지 판단하기
5. 근본 원인 수정하기
6. 테스트 재실행하기

### 5. 최종 검증
모든 체크를 순서대로 재실행합니다:
1. 린트
2. 타입체크
3. 테스트

모두 통과해야 완료됩니다.

### 6. 요약 보고
```
## 검증 요약

실행된 체크:
- 린트: PASS (3개 문제 수정)
- 타입체크: PASS
- 테스트: PASS (15개 테스트)

수정된 파일:
- src/utils.ts: 사용되지 않는 변수 수정
- src/api.ts: 타입 오류 수정
- src/config.ts: 누락된 반환 타입 수정
```

## 일반적인 수정 사항

### 린트 문제
- 사용되지 않는 변수: 제거하거나 사용하기
- 누락된 세미콜론: 추가하기 (스타일에 따라 필요 시)
- 일관되지 않은 따옴표: 표준화하기
- 임포트 순서: 알파벳 순으로 정렬하기

### 타입 문제
- 누락된 타입: 명시적 타입 주석 추가하기
- 타입 불일치: 불일치의 원인 수정하기
- Null/undefined: 적절한 null 체크 추가하기
- 제네릭 문제: 제네릭 타입 수정하기