---
name: vercel-deployment
description: >
  Vercel 배포, Preview/Production 환경 관리, Edge Functions,
  환경 변수 설정, CI/CD 파이프라인 통합 전문 스킬.
version: 2.0.0

triggers:
  keywords:
    - "vercel"
    - "vercel deploy"
    - "preview 배포"
    - "production 배포"
    - "Edge Function"
    - "serverless"
  file_patterns:
    - "vercel.json"
    - ".vercel/**/*"
    - "api/**/*.ts"
    - "api/**/*.js"
  context:
    - "Vercel 배포 설정"
    - "프로덕션 배포"
    - "서버리스 함수"

capabilities:
  - deploy_preview
  - deploy_production
  - manage_env_vars
  - setup_edge_functions
  - configure_domains

model_preference: sonnet

auto_trigger: true
---

# Vercel Deployment Skill

Vercel 배포 및 서버리스 인프라 관리를 위한 전문 스킬입니다.

## Quick Start

```bash
# Vercel CLI 설치
npm install -g vercel

# 로그인
vercel login

# 프로젝트 연결
vercel link

# 배포 (Preview)
vercel

# 배포 (Production)
vercel --prod
```

## 환경 변수 설정

### 필수 환경 변수

| 변수 | 용도 | 획득 위치 |
|------|------|----------|
| `VERCEL_TOKEN` | CLI/API 인증 | Vercel > Settings > Tokens |
| `VERCEL_ORG_ID` | 조직 ID | `vercel link` 후 `.vercel/project.json` |
| `VERCEL_PROJECT_ID` | 프로젝트 ID | `vercel link` 후 `.vercel/project.json` |

### 토큰 생성

```
Vercel Dashboard > Settings > Tokens > Create Token
├── Name: claude-deploy (또는 원하는 이름)
├── Scope: Full Account (또는 특정 프로젝트)
└── Expiration: No Expiration (또는 기간 설정)
```

## 핵심 기능

### 1. 배포 명령어

```bash
# Preview 배포 (기본)
vercel

# Production 배포
vercel --prod

# 특정 환경 변수와 함께 배포
vercel --env KEY=value --env KEY2=value2

# 빌드 스킵 (이미 빌드된 경우)
vercel --prebuilt

# 배포 후 URL 출력
vercel --prod 2>&1 | tail -1
```

### 2. 프로젝트 구조

```
project/
├── vercel.json          # Vercel 설정
├── .vercel/
│   └── project.json     # 프로젝트 연결 정보
├── api/                 # Serverless Functions
│   ├── hello.ts
│   └── users/
│       └── [id].ts
├── public/              # 정적 파일
└── src/                 # 앱 소스
```

### 3. vercel.json 설정

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm install",

  "regions": ["icn1"],

  "env": {
    "NODE_ENV": "production"
  },

  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Access-Control-Allow-Origin", "value": "*" }
      ]
    }
  ],

  "redirects": [
    {
      "source": "/old-path",
      "destination": "/new-path",
      "permanent": true
    }
  ],

  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://api.example.com/:path*"
    }
  ]
}
```

### 4. Serverless Functions

#### 기본 함수

```typescript
// api/hello.ts
import type { VercelRequest, VercelResponse } from '@vercel/node';

export default function handler(req: VercelRequest, res: VercelResponse) {
  const { name = 'World' } = req.query;
  res.status(200).json({ message: `Hello ${name}!` });
}
```

#### 동적 라우트

```typescript
// api/users/[id].ts
import type { VercelRequest, VercelResponse } from '@vercel/node';

export default function handler(req: VercelRequest, res: VercelResponse) {
  const { id } = req.query;
  res.status(200).json({ userId: id });
}
```

#### Edge Function

```typescript
// api/edge-hello.ts
export const config = {
  runtime: 'edge',
};

export default function handler(request: Request) {
  return new Response(
    JSON.stringify({ message: 'Hello from Edge!' }),
    {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    }
  );
}
```

### 5. 환경 변수 관리

#### CLI로 관리

```bash
# 환경 변수 추가
vercel env add MY_VAR production
vercel env add MY_VAR preview
vercel env add MY_VAR development

# 환경 변수 목록
vercel env ls

# 환경 변수 삭제
vercel env rm MY_VAR production

# 로컬로 환경 변수 가져오기
vercel env pull .env.local
```

#### 환경별 설정

| 환경 | 용도 | 트리거 |
|------|------|--------|
| Production | 프로덕션 배포 | `vercel --prod` |
| Preview | PR/브랜치 미리보기 | `vercel` (기본) |
| Development | 로컬 개발 | `vercel dev` |

### 6. 도메인 관리

```bash
# 도메인 추가
vercel domains add example.com

# 도메인 목록
vercel domains ls

# 도메인 제거
vercel domains rm example.com

# DNS 레코드 확인
vercel dns ls example.com
```

### 7. 로컬 개발

```bash
# Vercel 환경으로 로컬 실행
vercel dev

# 특정 포트로 실행
vercel dev --listen 3000

# 환경 변수 포함
vercel dev --env .env.local
```

## CI/CD 통합

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Vercel

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Vercel CLI
        run: npm install -g vercel

      - name: Pull Vercel Environment
        run: vercel pull --yes --environment=preview --token=${{ secrets.VERCEL_TOKEN }}

      - name: Build
        run: vercel build --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy Preview
        if: github.event_name == 'pull_request'
        run: vercel deploy --prebuilt --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy Production
        if: github.ref == 'refs/heads/main'
        run: vercel deploy --prebuilt --prod --token=${{ secrets.VERCEL_TOKEN }}
```

### 환경별 빌드

```bash
# Preview 환경 빌드
vercel build

# Production 환경 빌드
vercel build --prod

# Prebuilt로 배포 (빌드 결과물만)
vercel deploy --prebuilt --prod
```

## CLI 명령어 참조

| 명령어 | 용도 |
|--------|------|
| `vercel` | Preview 배포 |
| `vercel --prod` | Production 배포 |
| `vercel dev` | 로컬 개발 서버 |
| `vercel build` | 로컬 빌드 |
| `vercel deploy --prebuilt` | 빌드된 결과물 배포 |
| `vercel env ls` | 환경 변수 목록 |
| `vercel env pull` | 환경 변수 로컬로 가져오기 |
| `vercel domains ls` | 도메인 목록 |
| `vercel logs <url>` | 배포 로그 확인 |
| `vercel inspect <url>` | 배포 상세 정보 |
| `vercel rollback` | 이전 배포로 롤백 |
| `vercel alias <url> <domain>` | 커스텀 도메인 연결 |

## 체크리스트

### 초기 설정

- [ ] Vercel CLI 설치 (`npm i -g vercel`)
- [ ] 로그인 (`vercel login`)
- [ ] 프로젝트 연결 (`vercel link`)
- [ ] 환경 변수 설정 (Dashboard 또는 CLI)

### 배포 전

- [ ] `vercel.json` 설정 확인
- [ ] 환경 변수 확인 (`vercel env ls`)
- [ ] 로컬 빌드 테스트 (`vercel build`)
- [ ] 로컬 실행 테스트 (`vercel dev`)

### Production 배포

- [ ] Preview 배포 테스트
- [ ] 환경 변수 Production 설정
- [ ] 도메인 설정 (필요시)
- [ ] `vercel --prod` 실행

## Anti-Patterns

| 금지 | 이유 | 대안 |
|------|------|------|
| 토큰 코드에 노출 | 보안 위험 | 환경 변수 사용 |
| Production 직접 배포 | 검증 누락 | Preview 먼저 테스트 |
| 환경 변수 하드코딩 | 환경별 분리 불가 | `vercel env` 사용 |
| `--force` 남용 | 캐시 무효화 | 필요시만 사용 |

## 연동

| 스킬/에이전트 | 연동 시점 |
|---------------|----------|
| `supabase-integration` | 백엔드 API 연결 |
| `github-engineer` | CI/CD 파이프라인 |
| `frontend-dev` | 프론트엔드 빌드 |
| `devops-engineer` | 인프라 설정 |

## 트러블슈팅

### 빌드 실패

```bash
# 로컬에서 빌드 테스트
vercel build

# 빌드 로그 확인
vercel logs <deployment-url>

# 캐시 초기화
vercel deploy --force
```

### 환경 변수 누락

```bash
# 현재 환경 변수 확인
vercel env ls

# 로컬로 동기화
vercel env pull .env.local

# 특정 환경 변수 확인
vercel env ls | grep MY_VAR
```

### 함수 타임아웃

```typescript
// vercel.json에서 함수별 설정
{
  "functions": {
    "api/long-task.ts": {
      "maxDuration": 60  // 최대 60초 (Pro 플랜)
    }
  }
}
```

### CORS 오류

```json
// vercel.json
{
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Access-Control-Allow-Credentials", "value": "true" },
        { "key": "Access-Control-Allow-Origin", "value": "*" },
        { "key": "Access-Control-Allow-Methods", "value": "GET,POST,PUT,DELETE,OPTIONS" },
        { "key": "Access-Control-Allow-Headers", "value": "Content-Type, Authorization" }
      ]
    }
  ]
}
```

---

## 참조 문서

- [Vercel CLI Overview](https://vercel.com/docs/cli)
- [Vercel Deploy Command](https://vercel.com/docs/cli/deploy)
- [Deploying from CLI](https://vercel.com/docs/cli/deploying-from-cli)
