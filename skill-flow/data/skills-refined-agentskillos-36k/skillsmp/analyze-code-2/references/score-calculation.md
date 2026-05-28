# Score Calculation

> 분석 점수 계산 로직

## 점수 체계

### 기본 점수

각 Focus는 100점 만점:
- 기본 점수: 100점
- 이슈 발견 시 감점

### 감점 공식

```text
Score = 100 - Σ(Issue_Penalty)

Issue_Penalty:
├─ Critical: -25점
├─ High: -10점
├─ Medium: -3점
└─ Low: -1점
```

### 최소/최대 점수

- 최소: 0점
- 최대: 100점

## Focus별 계산

### Quality Score

```text
Quality Score = 100 - (
    Critical_Count × 25 +
    High_Count × 10 +
    Medium_Count × 3 +
    Low_Count × 1
)

최소 0점
```

**예시**:
```text
발견 이슈:
- Critical: 0
- High: 2 (순환 복잡도 25, 메서드 60줄)
- Medium: 5 (중복 코드, 긴 파라미터 등)
- Low: 8 (네이밍, 문서화 등)

Score = 100 - (0×25 + 2×10 + 5×3 + 8×1)
      = 100 - (0 + 20 + 15 + 8)
      = 100 - 43
      = 57점
```

### Security Score

```text
Security Score = 100 - (
    Critical_Count × 25 +
    High_Count × 10 +
    Medium_Count × 3 +
    Low_Count × 1
)

⚠️ Critical 1개 이상 → 자동 0점 처리 가능 (옵션)
```

**예시**:
```text
발견 이슈:
- Critical: 1 (하드코딩 비밀)
- High: 1 (불완전 검증)
- Medium: 3 (@Suppress 사용)
- Low: 2 (모범 사례)

Score = 100 - (1×25 + 1×10 + 3×3 + 2×1)
      = 100 - (25 + 10 + 9 + 2)
      = 100 - 46
      = 54점

(Critical 자동 0점 옵션 시: 0점)
```

### Performance Score

```text
Performance Score = 100 - (
    Critical_Count × 25 +
    High_Count × 10 +
    Medium_Count × 3 +
    Low_Count × 1
)
```

### Architecture Score

```text
Architecture Score = 100 - (
    Critical_Count × 25 +
    High_Count × 10 +
    Medium_Count × 3 +
    Low_Count × 1
)
```

## 전체 점수 (Overall Score)

### 기본 계산

```text
Overall = (Quality + Security + Performance + Architecture) / 4
```

### 가중치 적용 (선택)

프로젝트 특성에 따라 가중치 조정 가능:

```text
Overall = (
    Quality × 0.25 +
    Security × 0.30 +
    Performance × 0.25 +
    Architecture × 0.20
)
```

**권장 가중치 (백엔드)**:
| Focus | 가중치 | 이유 |
|-------|--------|------|
| Security | 0.30 | 보안 최우선 |
| Performance | 0.25 | Reactive 환경 중요 |
| Quality | 0.25 | 유지보수성 |
| Architecture | 0.20 | 장기 확장성 |

## 등급 체계

| 점수 범위 | 등급 | 설명 |
|----------|------|------|
| 90-100 | A | Excellent - 배포 권장 |
| 80-89 | B | Good - 배포 가능 |
| 70-79 | C | Fair - 개선 권장 |
| 60-69 | D | Poor - 개선 필요 |
| 0-59 | F | Fail - 배포 차단 |

## 트렌드 분석

### 시간별 추적

```text
Sprint 1: 65점 (D)
Sprint 2: 72점 (C) ↑ +7
Sprint 3: 78점 (C) ↑ +6
Sprint 4: 82점 (B) ↑ +4
```

### 변경 영향 분석

```text
이번 PR 영향:
├─ Quality: 78 → 75 (-3) ⚠️
├─ Security: 85 → 85 (0)
├─ Performance: 70 → 82 (+12) ✅
└─ Architecture: 88 → 88 (0)

Overall: 80.25 → 82.5 (+2.25) ✅
```

## 리포트 템플릿

### 점수 대시보드

```markdown
## 📊 Code Quality Score

| Focus | Score | Grade | Trend |
|-------|-------|-------|-------|
| Quality | 78/100 | C | ↑ +3 |
| Security | 65/100 | D | → 0 |
| Performance | 62/100 | D | ↓ -5 |
| Architecture | 85/100 | B | ↑ +2 |

**Overall: 72.5/100 (C)**

### Grade Distribution
A ████░░░░░░ 1 module
B ██████░░░░ 2 modules
C ████████░░ 3 modules
D ██░░░░░░░░ 1 module
F ░░░░░░░░░░ 0 modules
```

### 이슈 분포

```markdown
## 🔍 Issue Distribution

| Severity | Quality | Security | Performance | Architecture | Total |
|----------|---------|----------|-------------|--------------|-------|
| 🔴 Critical | 0 | 1 | 2 | 0 | 3 |
| 🟠 High | 2 | 1 | 3 | 1 | 7 |
| 🟡 Medium | 5 | 3 | 1 | 2 | 11 |
| 🟢 Low | 8 | 2 | 4 | 3 | 17 |
| **Total** | 15 | 7 | 10 | 6 | 38 |
```

## 목표 설정

### 팀 목표 예시

```text
현재: Overall 72점 (C)
목표: Overall 85점 (B) by Q2

Focus별 목표:
├─ Quality: 78 → 85 (+7)
├─ Security: 65 → 90 (+25) ⭐ 우선순위
├─ Performance: 62 → 80 (+18)
└─ Architecture: 85 → 88 (+3)
```

### 마일스톤

```text
M1 (Week 2): Critical 이슈 0개
M2 (Week 4): Security 80점+
M3 (Week 6): Performance 75점+
M4 (Week 8): Overall 85점+
```
