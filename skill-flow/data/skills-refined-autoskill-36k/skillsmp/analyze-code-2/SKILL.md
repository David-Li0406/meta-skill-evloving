---
name: analyze-code
description: |
  코드 종합 분석 (품질/보안/성능/아키텍처). Use when:
  (1) 코드 분석 요청, (2) 보안 취약점 스캔,
  (3) 성능 병목 식별, (4) 아키텍처 검토.
tools: [Read, Glob, Grep, Bash]
model: inherit
---

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: analyze-code 호출 - {분석 유형}` 시스템 메시지를 첫 줄에 출력하세요.

# analyze-code Skill

> Spring Boot + Kotlin + WebFlux 코드 종합 분석 Skill

## Purpose

코드베이스를 다각도로 분석하여 문제점과 개선 기회를 식별합니다.

### 분석 유형 (Focus)

| Focus | 설명 | 핵심 검사 |
|-------|------|----------|
| **quality** | 코드 품질 분석 | 복잡도, 중복, 코드 스멜 |
| **security** | 보안 취약점 스캔 | OWASP Top 10, 인증/인가 |
| **performance** | 성능 병목 식별 | N+1, 블로킹, 메모리 |
| **architecture** | 아키텍처 검토 | 레이어 의존성, SOLID |
| **all** | 전체 분석 | 모든 Focus 통합 |

## Quick Start

```bash
# 전체 분석
analyze-code --focus all

# 특정 Focus
analyze-code src/service --focus security

# 빠른 분석 (핵심만)
analyze-code --depth quick
```

## Workflow

### Phase 1: 탐색 (Discover)

```text
파일 탐색
├─ src/main/kotlin/**/*.kt
├─ 언어/프레임워크 감지
└─ 프로젝트 구조 분석

탐색 명령:
find src/main -name "*.kt" | head -50
```

### Phase 2: 스캔 (Scan)

```text
Focus별 분석 적용
├─ Quality: 코드 스멜 패턴 검사
├─ Security: 취약점 패턴 검사
├─ Performance: 성능 안티패턴 검사
└─ Architecture: 의존성/구조 검사
```

### Phase 3: 평가 (Evaluate)

```text
발견 항목 우선순위화
├─ Critical: 즉시 수정 필요
├─ High: 빠른 수정 권장
├─ Medium: 계획된 수정
└─ Low: 개선 기회
```

### Phase 4: 보고 (Report)

```text
종합 분석 리포트 생성
├─ 요약 대시보드
├─ Focus별 상세
├─ 액션 아이템
└─ 개선 로드맵
```

## Focus별 분석 패턴

### Quality Focus

```bash
# 복잡도 분석
grep -rn "when\|if.*else\|for\|while" src/ --include="*.kt" | wc -l

# 긴 메서드 탐지 (30줄 이상)
awk '/^[[:space:]]*(fun|suspend fun)/{start=NR} /^[[:space:]]*\}$/{if(NR-start>30) print FILENAME":"start}' src/**/*.kt

# 중복 코드 패턴
grep -rn "TODO\|FIXME\|XXX\|HACK" src/ --include="*.kt"
```

**검사 항목:**
- 순환 복잡도 > 10
- 메서드 라인 > 30
- 클래스 라인 > 300
- 중복 코드 블록
- 코드 스멜 패턴

### Security Focus

```bash
# SQL Injection 취약점
grep -rn "sql\|query" src/ --include="*.kt" | grep -v "bind\|parameter"

# 하드코딩된 비밀
grep -rn "password\|secret\|apiKey\|token" src/ --include="*.kt"

# 취약한 의존성
grep -rn "@Suppress.*\"UNCHECKED\|\"DEPRECATION\"" src/ --include="*.kt"
```

**검사 항목:**
- SQL/NoSQL Injection
- 하드코딩된 비밀
- 인증/인가 우회
- XSS 취약점
- 안전하지 않은 역직렬화

### Performance Focus

```bash
# N+1 쿼리 패턴
grep -rn "flatMap.*repository\|forEach.*find" src/ --include="*.kt"

# 블로킹 호출
grep -rn "\.block()\|Thread\.sleep\|\.get()" src/ --include="*.kt"

# 메모리 누수 가능성
grep -rn "mutableListOf\|ArrayList\|HashMap" src/ --include="*.kt"
```

**검사 항목:**
- N+1 쿼리
- 블로킹 호출
- 무한 스트림
- 캐시 미사용
- 불필요한 객체 생성

### Architecture Focus

```bash
# 레이어 의존성 위반
grep -rn "import.*controller" src/main/**/service/**/*.kt
grep -rn "import.*repository" src/main/**/controller/**/*.kt

# 순환 의존성
# (복잡한 분석 - 패키지별 import 그래프 구성 필요)
```

**검사 항목:**
- 레이어 의존성 위반
- 순환 의존성
- SOLID 원칙 위반
- 패키지 구조 문제
- 도메인 경계 침해

## Output Format

### 분석 완료 (요약)

```markdown
[SEMO] Skill: analyze-code 완료

## 📊 분석 요약

| Focus | Critical | High | Medium | Low | Score |
|-------|----------|------|--------|-----|-------|
| Quality | 0 | 2 | 5 | 8 | 78/100 |
| Security | 1 | 1 | 3 | 2 | 65/100 |
| Performance | 2 | 3 | 1 | 4 | 62/100 |
| Architecture | 0 | 1 | 2 | 3 | 85/100 |

**전체 점수**: 72.5/100

## 🔴 Critical Issues (즉시 수정)

1. **Security**: 하드코딩된 API 키
   - 위치: `ExternalApiClient.kt:23`
   - 위험: 비밀 노출

2. **Performance**: 블로킹 호출
   - 위치: `UserService.kt:45`
   - 영향: 스레드 블로킹

## 📋 권장 조치

1. 환경 변수로 비밀 이동 (Security)
2. `.block()` → 코루틴 변환 (Performance)
3. 메서드 분리 리팩토링 (Quality)
```

### Focus별 상세 리포트

```markdown
## 🔒 Security 상세 분석

### Critical

#### SEC-001: 하드코딩된 비밀
- **위치**: `ExternalApiClient.kt:23`
- **코드**:
  ```kotlin
  val apiKey = "sk-1234567890"  // CRITICAL!
  ```
- **위험**: Git 히스토리에 비밀 노출
- **수정**:
  ```kotlin
  @Value("\${external.api.key}")
  private lateinit var apiKey: String
  ```

### High

#### SEC-002: SQL 인젝션 가능성
- **위치**: `CustomRepository.kt:45`
- **패턴**: 문자열 연결로 쿼리 생성
- **수정**: 파라미터 바인딩 사용
```

## SEMO Message Format

```markdown
[SEMO] Skill: analyze-code 호출 - {focus}

[SEMO] Skill: analyze-code 스캔 중 - {current}/{total} 파일

[SEMO] Skill: analyze-code 완료 - {issues}건 발견 (Critical: {n})
```

## Integration with Other Components

### quality-master 연동

```text
quality-master 호출 시:
├─ 검증 전: analyze-code --focus quality --depth quick
└─ 검증 후: 결과 포함 리포트
```

### improve-code 연동

```text
analyze-code 완료 후:
├─ Critical/High 이슈 → improve-code 제안
└─ 자동 수정 가능 항목 표시
```

### debug-master 연동

```text
에러 발생 시:
├─ analyze-code --focus security (보안 관련 에러)
├─ analyze-code --focus performance (성능 관련 에러)
└─ 근본 원인 분석 지원
```

## Depth Options

| Depth | 설명 | 소요 시간 |
|-------|------|----------|
| **quick** | 핵심 패턴만 | ~30초 |
| **standard** | 기본 분석 | ~2분 |
| **deep** | 전체 분석 | ~5분 |

## References

- [Analysis Patterns](references/analysis-patterns.md) - Focus별 분석 패턴
- [Severity Definitions](references/severity-definitions.md) - 심각도 정의
- [Score Calculation](references/score-calculation.md) - 점수 계산 로직
