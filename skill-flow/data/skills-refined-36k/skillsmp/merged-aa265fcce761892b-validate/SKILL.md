---
name: validate
description: 이 스킬은 린트, 타입체크 및 테스트를 실행하고 모든 문제를 자동으로 수정할 때 사용합니다.
---

# Validate

**IMPORTANT: 모든 설명과 요약은 한국어로 작성하세요. 단, 코드 예시와 명령어는 원문 그대로 유지합니다.**

린트, 타입체크 및 테스트를 실행하고 모든 실패를 수정합니다. 모든 검사가 통과할 때까지 반복합니다.

## 규칙

- 파일을 완전히 읽고 수정합니다.
- 증상이 아닌 근본 원인을 수정합니다.
- 최소한의 집중된 변경을 합니다.
- 실패를 건너뛰거나 무시하지 않습니다.
- 각 수정 후에 검사를 다시 실행합니다.

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
1. 오류 메시지를 주의 깊게 읽습니다.
2. 영향을 받은 파일 전체를 읽습니다.
3. 근본 원인을 식별합니다.
4. 최소한의 변경으로 수정합니다.
5. 린트를 다시 실행합니다.

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
1. 타입 오류 메시지를 읽습니다.
2. 타입 흐름을 추적합니다.
3. 타입 정의 또는 사용을 수정합니다.
4. 타입체크를 다시 실행합니다.

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
1. 테스트 실패 출력을 읽습니다.
2. 실패한 테스트 코드를 읽습니다.
3. 테스트 중인 구현을 읽습니다.
4. 테스트 또는 코드가 잘못되었는지 결정합니다.
5. 근본 원인을 수정합니다.
6. 테스트를 다시 실행합니다.

### 5. 최종 검증
모든 검사를 순서대로 다시 실행합니다:
1. 린트
2. 타입체크
3. 테스트

모두 통과해야 완료됩니다.

### 6. 요약 보고
```
## Validation Summary

Checks Run:
- Lint: PASS (fixed 3 issues)
- Typecheck: PASS
- Tests: PASS (15 tests)

Files Modified:
- src/utils.ts: Fixed unused variable
- src/api.ts: Fixed type error
- src/config.ts: Fixed missing return type
```

## 일반적인 수정 사항

### 린트 문제
- 사용하지 않는 변수: 제거하거나 사용합니다.
- 누락된 세미콜론: 추가합니다 (스타일에 따라 필요 시).
- 일관되지 않은 따옴표: 표준화합니다.
- 임포트 순서: 알파벳순으로 정렬합니다.

### 타입 문제
- 누락된 타입: 명시적 타입 주석을 추가합니다.
- 타입 불일치: 불일치의 원인을 수정합니다.
- Null/undefined: 적절한 null 검사를 추가합니다.
- 제네릭 추론: 명시적 타입 매개변수를 추가합니다.

### 테스트 문제
- 단언 실패: 코드를 수정하거나 테스트 기대치를 업데이트합니다.
- 타임아웃: 최적화하거나 타임아웃을 늘립니다.
- 누락된 모의: 적절한 모의/스텁을 추가합니다.
- 불안정한 테스트: 경쟁 조건을 수정합니다.

## 안티 패턴

- 정당한 이유 없이 린트 규칙을 비활성화하지 마십시오.
- 타입 오류를 우회하기 위해 `any` 타입을 사용하지 마십시오.
- 실패하는 테스트를 건너뛰지 마십시오.
- 근본 원인을 수정하지 않고 `// @ts-ignore`를 추가하지 마십시오.
- 이유를 이해하지 않고 테스트 기대치를 수정하지 마십시오.