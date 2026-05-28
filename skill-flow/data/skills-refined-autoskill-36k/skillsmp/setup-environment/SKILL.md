---
name: setup-environment
description: |
  Vercel/Supabase 개발 환경 설정. Use when (1) 새 프로젝트 시작,
  (2) CLI 설정 필요, (3) 환경변수 구성, (4) Greenfield P0 단계.
tools: [Bash, Read, Write, AskUserQuestion]
model: inherit
---

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: setup-environment 호출` 메시지를 첫 줄에 출력하세요.

# setup-environment Skill

> Vercel + Supabase 개발 환경 사전 설정

## Purpose

Greenfield 워크플로우의 P0 단계로, 개발/배포 환경을 사전 구성합니다.

## Workflow

```text
환경 설정 요청
    ↓
1. Vercel CLI 확인 및 설정
2. Supabase CLI 확인 및 설정
3. 환경변수 구성
4. 연결 검증
    ↓
완료
```

## Input

```yaml
# 프로젝트 정보 (선택)
project_name: "my-project"       # Vercel 프로젝트명
supabase_ref: "abcdefghijk"      # Supabase 프로젝트 ref
```

## Execution Steps

### Step 1: Vercel CLI 확인

```bash
# 버전 확인
vercel --version

# 설치 안된 경우
npm i -g vercel
```

### Step 2: Vercel 로그인 및 연결

```bash
# 로그인 상태 확인
vercel whoami

# 로그인 필요시
vercel login

# 프로젝트 연결
vercel link
```

### Step 3: Supabase CLI 확인

```bash
# 버전 확인
supabase --version

# 설치 안된 경우 (macOS)
brew install supabase/tap/supabase

# 또는 npm
npm i -g supabase
```

### Step 4: Supabase 로그인 및 연결

```bash
# 로그인
supabase login

# 프로젝트 연결
supabase link --project-ref {ref}
```

### Step 5: 환경변수 설정

사용자에게 Supabase 대시보드에서 키 확인 요청 (AskUserQuestion):

```yaml
questions:
  - question: "Supabase 프로젝트 URL을 입력해주세요"
    header: "URL"
    options:
      - label: "직접 입력"
        description: "https://xxx.supabase.co 형식"
```

`.env.local` 생성:

```bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIs...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIs...
```

### Step 6: 연결 검증

```bash
# Vercel 환경변수 동기화 (선택)
vercel env pull .env.local

# Supabase 연결 테스트
supabase db push --dry-run
```

## Output

```markdown
[SEMO] Skill: setup-environment 완료

✅ **환경 설정 완료**

| 항목 | 상태 | 값 |
| ---- | ---- | --- |
| Vercel CLI | 연결됨 | {project_name} |
| Supabase CLI | 연결됨 | {ref} |
| .env.local | 생성됨 | 4개 변수 |

---

### 환경변수 목록

- `NEXT_PUBLIC_SUPABASE_URL`: ✅
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`: ✅
- `SUPABASE_SERVICE_ROLE_KEY`: ✅

---

다음 단계: Phase 2 Planning 진행
```

## Error Handling

| 에러 | 처리 |
| ---- | ---- |
| Vercel CLI 없음 | `npm i -g vercel` 안내 |
| Supabase CLI 없음 | `brew install supabase/tap/supabase` 안내 |
| 로그인 실패 | 브라우저 인증 재시도 안내 |
| 프로젝트 없음 | Vercel/Supabase 대시보드에서 생성 안내 |

## Environment Variables

| 변수 | 필수 | 설명 |
| ---- | ---- | ---- |
| `NEXT_PUBLIC_SUPABASE_URL` | 필수 | Supabase 프로젝트 URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | 필수 | 공개 API 키 |
| `SUPABASE_SERVICE_ROLE_KEY` | 필수 | 서버사이드 전용 키 |
| `SUPABASE_DB_URL` | 선택 | Direct DB 연결 (마이그레이션용) |

## Security Notes

- `SUPABASE_SERVICE_ROLE_KEY`는 절대 클라이언트에 노출하지 마세요
- `.env.local`은 `.gitignore`에 포함되어야 합니다
- Vercel에 환경변수 설정 시 Production/Preview/Development 구분

## Related Skills

- `health-check` - 개발 환경 상태 확인
- `deploy-service` - 서비스 배포
- `workflow-start` - 워크플로우 시작
