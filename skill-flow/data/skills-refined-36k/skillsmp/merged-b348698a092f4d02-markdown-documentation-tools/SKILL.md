---
name: markdown-documentation-tools
description: Use this skill when you need to manage and validate Markdown documentation in a project, including writing tests, checking for broken links, and listing documents.
---

# Markdown Documentation Tools

이 스킬은 프로젝트 내 Markdown 문서의 관리 및 검증을 위한 다양한 도구를 제공합니다. 테스트 코드 작성 가이드라인, 깨진 링크 검사, 문서 목록 조회 기능을 포함합니다.

## 1. 테스트 작성 가이드라인

테스트 코드를 작성할 때 다음 원칙과 패턴을 따릅니다.

### 테스트 원칙

- **F**ast: 빠르게 실행되어야 함
- **I**ndependent: 다른 테스트에 의존하지 않음
- **R**epeatable: 어떤 환경에서도 같은 결과
- **S**elf-validating: 성공/실패가 명확
- **T**imely: 프로덕션 코드와 함께 작성

### AAA 패턴

모든 테스트는 다음 구조를 따릅니다:

```javascript
test('should do something', () => {
  const input = createTestData();
  const result = functionToTest(input);
  expect(result).toBe(expectedValue);
});
```

### 테스트 명명 규칙

형식: `should [expected behavior] when [condition]`

### 테스트 종류별 가이드

- **단위 테스트 (Unit Test)**: 하나의 함수/메서드만 테스트
- **통합 테스트 (Integration Test)**: 여러 컴포넌트 간 상호작용 테스트
- **E2E 테스트**: 사용자 시나리오 전체 테스트

### 모킹 가이드

외부 API 호출, 데이터베이스 접근, 시간 의존적 코드 등을 모킹합니다.

### 테스트 커버리지

- 목표 커버리지: 라인 80% 이상, 브랜치 70% 이상

### 테스트 안티패턴

피해야 할 것들: 구현 세부사항 테스트, 테스트 간 의존성 등.

### 테스트 파일 구조

```
src/
├── userService.js
└── __tests__/
    └── userService.test.js
```

### 테스트 작성 순서

1. 가장 간단한 성공 케이스
2. 엣지 케이스들
3. 에러 케이스들
4. 경계값 테스트

## 2. 깨진 링크 검사

프로젝트 내 모든 Markdown 파일(.md)에서 깨진 링크를 검사합니다.

### 사용 방법

```bash
bash ./.claude/skills/broken-link-checker/check-broken-links.sh
```

### 옵션

- 기본 검사
- 특정 디렉토리만 검사: `--path ./docs`

### 출력 형식

```
╔════════════════════════════════════════════════════════════════╗
║  Broken Link Checker                                           ║
╚════════════════════════════════════════════════════════════════╝

📁 검사 대상: 15개 마크다운 파일

❌ 깨진 링크 발견: 2개
```

### 검증 규칙

- 내부 링크: 파일 존재 여부, 대소문자 정확성 검사
- 앵커 링크: 헤딩 ID 존재 여부 확인

## 3. 문서 목록 조회

프로젝트의 Markdown 문서를 TOON 포맷으로 조회합니다.

### 사용 방법

```bash
# 모든 문서 조회
/list-docs

# 특정 경로 하위 문서만 조회
/list-docs --path=src
```

### 출력 형식 (TOON)

```
docs[3]{path,desc}:
docs/architecture.md,시스템 아키텍처; 레이어 구조; 의존성 흐름
```

### 메타데이터 형식

각 Markdown 파일 상단에 YAML frontmatter로 메타데이터를 추가하세요:

```yaml
---
name: 문서 이름
description: 이 문서에서 알 수 있는 구체적인 내용
---
```

**description 작성 팁:** 세미콜론(`;`)으로 키워드 구분, 100자 이내 권장.