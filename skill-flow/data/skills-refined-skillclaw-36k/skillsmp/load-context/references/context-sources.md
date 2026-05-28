# Context Sources Reference

> load-context Skill이 수집하는 컨텍스트 소스 상세

## 소스 우선순위

```text
1. specs/{domain}/     ← 요구사항/설계 (최우선)
2. domain/{domain}/    ← 실제 구현
3. git log            ← 변경 이력
4. GitHub Issues      ← 관련 이슈
5. tests/             ← 테스트 현황
```

---

## 1. Spec Documents

### 경로
```text
specs/{domain}/
├── spec.md    # 요구사항 정의
├── plan.md    # 기술 계획
└── tasks.md   # 작업 항목
```

### 수집 명령어
```bash
# 존재 여부 확인
ls specs/{domain}/ 2>/dev/null

# 내용 읽기
cat specs/{domain}/spec.md
cat specs/{domain}/plan.md
cat specs/{domain}/tasks.md
```

### 추출 정보
| 파일 | 추출 내용 |
|------|----------|
| spec.md | 기능 설명, 요구사항, AC |
| plan.md | 기술 스택, 아키텍처 결정 |
| tasks.md | 작업 목록, 진행 상태 |

---

## 2. Source Code

### 경로
```text
src/main/kotlin/com/semicolon/{project}/domain/{domain}/
├── entity/
├── repository/
├── service/
├── web/
└── exception/
```

### 수집 명령어
```bash
# 디렉토리 구조
find domain/{domain} -type f -name "*.kt" | head -20

# 주요 클래스 목록
grep -l "class\|interface\|object" domain/{domain}/**/*.kt

# Entity 필드 확인
grep -A 20 "^data class\|^class" domain/{domain}/entity/*.kt

# Service 메서드 확인
grep "suspend fun\|fun " domain/{domain}/service/*.kt

# Controller 엔드포인트 확인
grep "@.*Mapping\|@Get\|@Post\|@Put\|@Delete" domain/{domain}/web/*.kt
```

### 추출 정보
| 대상 | 추출 내용 |
|------|----------|
| Entity | 필드 목록, 테이블명 |
| Repository | 커스텀 쿼리 메서드 |
| Service | public 메서드 시그니처 |
| Controller | 엔드포인트 목록 |
| Exception | 예외 종류 |

---

## 3. Git History

### 수집 명령어
```bash
# 최근 커밋 (도메인별)
git log --oneline -10 -- domain/{domain}/

# 상세 변경 내용
git log -5 --stat -- domain/{domain}/

# 최근 diff
git diff HEAD~3 -- domain/{domain}/

# 담당자 확인
git log --format='%an' -10 -- domain/{domain}/ | sort | uniq -c | sort -rn
```

### 추출 정보
| 항목 | 설명 |
|------|------|
| 커밋 해시 | 변경 식별자 |
| 커밋 메시지 | 변경 이유 |
| 변경 파일 | 영향받은 파일 |
| 담당자 | 주요 작업자 |

---

## 4. GitHub Issues

### 수집 명령어
```bash
# 도메인 라벨로 이슈 검색
gh issue list --label "{domain}" --state all --limit 10

# 키워드로 검색
gh issue list --search "{domain}" --state all --limit 10

# 이슈 상세
gh issue view {issue_number}
```

### 추출 정보
| 항목 | 설명 |
|------|------|
| 이슈 번호 | 참조용 |
| 제목 | 이슈 요약 |
| 상태 | open/closed |
| 라벨 | 분류 정보 |
| 담당자 | 할당된 사람 |

---

## 5. Test Files

### 경로
```text
src/test/kotlin/com/semicolon/{project}/domain/{domain}/
├── {Domain}RepositoryTest.kt
├── {Domain}CommandServiceTest.kt
├── {Domain}QueryServiceTest.kt
└── {Domain}ControllerTest.kt
```

### 수집 명령어
```bash
# 테스트 파일 목록
find src/test -name "*{Domain}*.kt" -type f

# 테스트 메서드 목록
grep "@Test" src/test/**/*{Domain}*.kt

# 테스트 실행 결과 (최근)
./gradlew test --tests "*{Domain}*" --info 2>&1 | tail -50
```

### 추출 정보
| 항목 | 설명 |
|------|------|
| 테스트 파일 수 | 커버리지 힌트 |
| 테스트 메서드 | 테스트 시나리오 |
| 통과/실패 | 현재 상태 |

---

## 연관 도메인 탐지

### 방법
```bash
# Import 분석
grep "import.*domain\." domain/{domain}/**/*.kt | grep -v "{domain}" | sort | uniq

# 의존성 주입 분석
grep -h "private val\|private lateinit var" domain/{domain}/service/*.kt | grep -oP '\w+(?=Repository|\w+Service)'
```

### 추출 정보
- 참조하는 다른 도메인
- 의존성 방향

---

## 출력 우선순위

### 기본 모드
1. Spec 상태 요약 (있음/없음)
2. 코드 구조 개요
3. 최근 변경 3건
4. 관련 이슈 상위 3건

### --deep 모드
1. Spec 전체 내용
2. 주요 클래스 코드
3. 최근 변경 10건 + diff
4. 모든 관련 이슈
5. 테스트 현황

### --spec-only 모드
- Spec 문서만 상세 출력

### --code-only 모드
- 코드 구조 + 주요 메서드만

### --history 모드
- Git 이력 중심 상세 출력
