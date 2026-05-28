---
name: code-reviewer
description: |
  코드 리뷰 전문 skill. TypeScript, JavaScript, Python, Swift, Kotlin, Go 지원. 정적 분석, 베스트 프랙티스 검사, 보안 스캔, 리뷰 체크리스트 생성.
  사용 시기: (1) PR 리뷰 시 (2) 코드 품질 피드백 시 (3) 보안 취약점 식별 시 (4) 코드 표준 검사 시 (project)
---

# Code Reviewer

Complete toolkit for code reviewer with modern tools and best practices.

## Quick Start

```bash
# 1. 정적 분석 (ktlint, eslint, flake8)
python script/code_review_analyzer.py --output .claude/review-report.json

# 2. PR 분석 (파일별 리스크, 리뷰 우선순위)
python script/pr_analyzer.py --pr 123 --output .claude/pr-analysis.json

# 3. 마크다운 리포트 생성
python script/review_report_generator.py --input .claude/review-report.json
```

## Core Capabilities

### 1. Code Review Analyzer

정적 분석 도구(ktlint, eslint, flake8)를 통합하여 JSON 리포트를 생성합니다.

**Features:**
- 언어별 린터 자동 실행 (Kotlin: ktlint, TS/JS: eslint, Python: flake8)
- 심각도 분류 (error/warning/info)
- 자동 수정 가능 여부 표시 (auto_fixable)
- 파일별 이슈 집계 및 상위 문제 파일 식별

**Usage:**
```bash
python script/code_review_analyzer.py --output .claude/review-report.json
```

### 2. PR Analyzer

GitHub PR의 변경사항을 분석하여 리스크 수준과 리뷰 우선순위를 산정합니다.

**Features:**
- 파일별 리스크 평가 (critical/high/medium/low)
- 고위험 패턴 자동 식별 (보안, 설정, 인증 관련)
- 변경량 기반 리스크 가중치
- 리뷰 우선순위 자동 정렬

**Usage:**
```bash
# GitHub PR 분석
python script/pr_analyzer.py --pr 123

# 로컬 변경사항 분석 (git diff)
python script/pr_analyzer.py --base main
```

### 3. Review Report Generator

JSON 분석 결과를 마크다운 리뷰 리포트로 변환합니다.

**Features:**
- Critical/Warning/Suggestion 분류
- 파일:라인 형식으로 위치 표시
- 파일별 이슈 그룹핑
- GitHub PR 코멘트 형식 지원

**Usage:**
```bash
# JSON → 마크다운 변환
python script/review_report_generator.py -i .claude/review-report.json -o .claude/review-report.md

# stdout 출력
python script/review_report_generator.py --print
```

## Reference Documentation

### Code Review Checklist

Comprehensive guide available in `references/code_review_checklist.md`:

- Detailed patterns and practices
- Code examples
- Best practices
- Anti-patterns to avoid
- Real-world scenarios

### Coding Standards

Complete workflow documentation in `references/coding_standards.md`:

- Step-by-step processes
- Optimization strategies
- Tool integrations
- Performance tuning
- Troubleshooting guide

### Common Antipatterns

Technical reference guide in `references/common_antipatterns.md`:

- Technology stack details
- Configuration examples
- Integration patterns
- Security considerations
- Scalability guidelines

## Tech Stack

**Languages:** TypeScript, JavaScript, Python, Go, Swift, Kotlin
**Frontend:** React, Next.js, React Native, Flutter
**Backend:** Node.js, Express, GraphQL, REST APIs
**Database:** PostgreSQL, Prisma, NeonDB, Supabase
**DevOps:** Docker, Kubernetes, Terraform, GitHub Actions, CircleCI
**Cloud:** AWS, GCP, Azure

## Development Workflow

### 1. Setup and Configuration

```bash
# Install dependencies
npm install
# or
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

### 2. Run Quality Checks

```bash
# 코드 리뷰 분석 실행
python script/code_review_analyzer.py --output .claude/review-report.json

# 리포트 확인 후 수정
```

### 3. Implement Best Practices

Follow the patterns and practices documented in:
- `references/code_review_checklist.md`
- `references/coding_standards.md`
- `references/common_antipatterns.md`

## Best Practices Summary

### Code Quality
- Follow established patterns
- Write comprehensive tests
- Document decisions
- Review regularly

### Performance
- Measure before optimizing
- Use appropriate caching
- Optimize critical paths
- Monitor in production

### Security
- Validate all inputs
- Use parameterized queries
- Implement proper authentication
- Keep dependencies updated

### Maintainability
- Write clear code
- Use consistent naming
- Add helpful comments
- Keep it simple

## Common Commands

```bash
# Development
npm run dev
npm run build
npm run test
npm run lint

# Analysis
python script/code_review_analyzer.py --output .claude/review-report.json

# Deployment
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```

## Troubleshooting

### Common Issues

Check the comprehensive troubleshooting section in `references/common_antipatterns.md`.

### Getting Help

- Review reference documentation
- Check script output messages
- Consult tech stack documentation
- Review error logs

## Resources

- Pattern Reference: `references/code_review_checklist.md`
- Workflow Guide: `references/coding_standards.md`
- Technical Guide: `references/common_antipatterns.md`
- Tool Scripts: `script/` directory
