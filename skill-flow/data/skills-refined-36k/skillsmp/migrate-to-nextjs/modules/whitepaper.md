# Whitepaper Generation

Documentation for generating pre-migration and post-migration whitepaper packages.

## Pre-Migration Whitepaper

### Overview

`migrate-analyze` 명령에 `--whitepaper` 플래그를 사용하면 클라이언트 제출용 전문 백서 패키지를 생성할 수 있습니다.

### Usage

```bash
# 전체 백서 패키지 생성 (기본 경로: ./whitepaper/)
/jikime:migrate-1-analyze "./my-vue-app" --whitepaper --client "ABC Corp" --target nextjs

# 영문 백서 생성
/jikime:migrate-1-analyze "./my-vue-app" --whitepaper --client "ABC Corp" --target nextjs --lang en

# 일본어 백서 생성
/jikime:migrate-1-analyze "./my-vue-app" --whitepaper --client "株式会社ABC" --target nextjs --lang ja

# 커스텀 출력 경로 지정
/jikime:migrate-1-analyze "./my-vue-app" --whitepaper --client "ABC Corp" --whitepaper-output ./docs/pre-migration

# 기본 분석만 실행 (백서 없음)
/jikime:migrate-1-analyze "./my-vue-app"
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--whitepaper` | - | 백서 생성 활성화 |
| `--whitepaper-output` | `./whitepaper/` | 백서 출력 디렉토리 |
| `--client` | "Client Company" | 클라이언트 회사명 (표지에 사용) |
| `--target` | - | 대상 프레임워크 힌트 (nextjs\|vite\|fastapi) |
| `--lang` | conversation_language | 백서 언어 (ko\|en\|ja\|zh) |

### Language Support

| Code | Language | Description |
|------|----------|-------------|
| `ko` | Korean | 한국어 백서 |
| `en` | English | English whitepaper |
| `ja` | Japanese | 日本語ホワイトペーパー |
| `zh` | Chinese | 中文白皮书 |

**Default**: `--lang` 미지정 시 사용자의 `conversation_language` 설정 사용

### Package Structure

**기본 출력 경로**: `{--whitepaper-output}` 또는 `./whitepaper/` (프로젝트 홈)

```
./whitepaper/                      # 백서 패키지 (--whitepaper 시)
    ├── 00_cover.md                # 표지 및 목차
    ├── 01_executive_summary.md    # 경영진 요약
    ├── 02_feasibility_report.md   # 타당성 보고서
    ├── 03_architecture_report.md  # 아키텍처 보고서
    ├── 04_complexity_matrix.md    # 복잡도 매트릭스
    ├── 05_migration_roadmap.md    # 마이그레이션 로드맵
    └── 06_baseline_report.md      # 보안/성능 기준선
```

### Document Descriptions

| Document | Purpose | Target Audience |
|----------|---------|-----------------|
| **Cover** | 표지, 목차, 기밀 고지 | 모든 독자 |
| **Executive Summary** | 핵심 요약, 권장 사항 | 경영진, 의사결정자 |
| **Feasibility Report** | 기술/경제적 타당성, 리스크 분석 | PM, Tech Lead |
| **Architecture Report** | AS-IS/TO-BE 아키텍처 비교 | 개발팀, 아키텍트 |
| **Complexity Matrix** | 컴포넌트별 복잡도, 공수 산정 | PM, Tech Lead |
| **Migration Roadmap** | 상세 일정, 마일스톤, 품질 게이트 | 전체 팀 |
| **Baseline Report** | 보안/성능 현황 및 목표 | 보안팀, DevOps |

### Agent Delegation

| Document | Primary Agent | Supporting Agents |
|----------|---------------|-------------------|
| Executive Summary | manager-docs | manager-strategy |
| Feasibility Report | manager-strategy | frontend |
| Architecture Report | frontend | manager-strategy |
| Complexity Matrix | frontend | - |
| Migration Roadmap | manager-strategy | manager-spec |
| Baseline Report | security-auditor | optimizer |

### Quality Checklist

- [ ] 모든 7개 문서 생성 완료 (표지 + 6개 보고서)
- [ ] 클라이언트 이름이 표지에 표시됨
- [ ] 모든 Mermaid 다이어그램 정상 렌더링
- [ ] 공수 추정이 현실적이고 근거 있음
- [ ] 리스크에 대응하는 완화 전략 포함
- [ ] 경영진 요약은 비기술적 용어 사용
- [ ] 로드맵에 명확한 마일스톤 포함
- [ ] 플레이스홀더 텍스트 없음

---

## Post-Migration Whitepaper (완료 보고서)

### Overview

마이그레이션 완료 후 `--whitepaper-report` 플래그를 사용하면 Before/After 비교 기반의 완료 보고서를 생성합니다.

### Usage

```bash
# 마이그레이션 완료 후 결과 보고서 생성 (기본 경로: ./whitepaper-report/)
/jikime:migrate-3-execute my-vue-app --whitepaper-report --client "ABC Corp"

# 영문 완료 보고서 생성
/jikime:migrate-3-execute my-vue-app --whitepaper-report --client "ABC Corp" --lang en

# 일본어 완료 보고서 생성
/jikime:migrate-3-execute my-vue-app --whitepaper-report --client "株式会社ABC" --lang ja

# 커스텀 출력 경로 지정
/jikime:migrate-3-execute my-vue-app --whitepaper-report --client "ABC Corp" --whitepaper-output ./docs/post-migration
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--whitepaper-report` | - | 완료 보고서 생성 활성화 |
| `--whitepaper-output` | `./whitepaper-report/` | 완료 보고서 출력 디렉토리 |
| `--client` | "Client Company" | 클라이언트 회사명 (표지에 사용) |
| `--lang` | conversation_language | 보고서 언어 (ko\|en\|ja\|zh) |

### Package Structure

**기본 출력 경로**: `{--whitepaper-output}` 또는 `./whitepaper-report/` (프로젝트 홈)

```
./whitepaper-report/                 # 완료 보고서 패키지 (--whitepaper-report 시)
├── 00_cover.md                      # 표지 및 핵심 성과 요약
├── 01_executive_summary.md          # 경영진 보고용 요약
├── 02_performance_comparison.md     # 성능 Before/After 비교
├── 03_security_improvement.md       # 보안 개선 사항
├── 04_code_quality_report.md        # 코드 품질 비교
├── 05_architecture_evolution.md     # 아키텍처 진화
├── 06_cost_benefit_analysis.md      # ROI 및 비용 효과 분석
└── 07_maintenance_guide.md          # 유지보수 가이드
```

### Document Descriptions

| Document | Purpose | Target Audience |
|----------|---------|-----------------|
| **Cover** | 핵심 성과 요약, Before/After 지표 | 모든 독자 |
| **Executive Summary** | 투자 정당성, ROI 요약 | 경영진, 의사결정자 |
| **Performance Comparison** | Core Web Vitals, 번들 크기 비교 | 기술팀, PM |
| **Security Improvement** | OWASP 대응, 취약점 해결 현황 | 보안팀, 컴플라이언스 |
| **Code Quality Report** | 타입 안전성, 테스트 커버리지 비교 | 개발팀, Tech Lead |
| **Architecture Evolution** | 기술 스택 변화, 구조 개선 | 아키텍트, 개발팀 |
| **Cost-Benefit Analysis** | 투자 회수 기간, 5년 ROI | 경영진, 재무팀 |
| **Maintenance Guide** | 개발 가이드, 운영 매뉴얼 | 개발팀, DevOps |

### Agent Delegation

| Document | Primary Agent | Supporting Agents |
|----------|---------------|-------------------|
| Executive Summary | manager-docs | manager-strategy |
| Performance Comparison | optimizer | frontend |
| Security Improvement | security-auditor | - |
| Code Quality Report | manager-quality | refactorer |
| Architecture Evolution | frontend | manager-strategy |
| Cost-Benefit Analysis | manager-strategy | - |
| Maintenance Guide | manager-docs | devops |

### Quality Checklist (Post-Migration)

- [ ] 모든 8개 문서 생성 완료
- [ ] Before/After 지표가 정확하게 측정됨
- [ ] 성능 개선율이 실측 데이터 기반
- [ ] ROI 계산이 현실적이고 근거 있음
- [ ] 유지보수 가이드가 실행 가능함
- [ ] 플레이스홀더 텍스트 없음

---

## Templates Location

백서 문서 템플릿은 다음 위치에 있습니다:

### Pre-Migration Templates
```
.claude/skills/jikime-migration-to-nextjs/templates/pre-migration/
├── 00_cover.md
├── 01_executive_summary.md
├── 02_feasibility_report.md
├── 03_architecture_report.md
├── 04_complexity_matrix.md
├── 05_migration_roadmap.md
└── 06_baseline_report.md
```

### Post-Migration Templates
```
.claude/skills/jikime-migration-to-nextjs/templates/post-migration/
├── 00_cover.md
├── 01_executive_summary.md
├── 02_performance_comparison.md
├── 03_security_improvement.md
├── 04_code_quality_report.md
├── 05_architecture_evolution.md
├── 06_cost_benefit_analysis.md
└── 07_maintenance_guide.md
```

각 템플릿은 `{{PLACEHOLDER}}` 형식의 변수를 포함하며, 실제 분석 데이터로 대체됩니다.

---

Version: 2.1.0
Source: jikime-migration-to-nextjs SKILL.md
