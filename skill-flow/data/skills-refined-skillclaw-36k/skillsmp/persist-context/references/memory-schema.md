# Memory Schema 상세

> skill:memory에서 사용하는 데이터 스키마

## 저장소 구조

```text
.claude/memory/
├── decisions.json      # 아키텍처 결정 사항
├── preferences.json    # 팀/사용자 선호도
├── cache/              # 패턴 캐시
│   ├── patterns.json
│   └── snippets.json
└── context/            # 프로젝트별 맥락
    └── {project}.json
```

## decisions.json

```json
{
  "version": "1.0.0",
  "updated_at": "2025-12-10T10:00:00Z",
  "decisions": {
    "{key}": {
      "value": "결정 내용",
      "created_at": "2025-12-10T10:00:00Z",
      "context": "결정 배경"
    }
  }
}
```

### 필드 설명

| 필드 | 타입 | 설명 |
|------|------|------|
| version | string | 스키마 버전 |
| updated_at | ISO8601 | 마지막 수정 시간 |
| decisions | object | 결정 사항 맵 |
| decisions.{key}.value | string | 결정 내용 |
| decisions.{key}.created_at | ISO8601 | 생성 시간 |
| decisions.{key}.context | string | 결정 배경 (선택) |

## preferences.json

```json
{
  "version": "1.0.0",
  "updated_at": "2025-12-10T10:00:00Z",
  "preferences": {
    "naming-convention": {
      "variables": "camelCase",
      "components": "PascalCase",
      "files": "kebab-case"
    },
    "code-style": {
      "indent": 2,
      "quotes": "single",
      "semicolon": false
    },
    "language": "ko"
  }
}
```

### 표준 선호도 키

| 키 | 설명 | 예시 값 |
|-----|------|---------|
| naming-convention | 네이밍 규칙 | camelCase, PascalCase |
| code-style | 코드 스타일 | indent, quotes |
| language | 응답 언어 | ko, en |
| framework | 프레임워크 선호 | Next.js, React |

## context/{project}.json

```json
{
  "project": "cm-office",
  "updated_at": "2025-12-10T10:00:00Z",
  "architecture": {
    "framework": "Next.js 14",
    "database": "Supabase",
    "styling": "Tailwind CSS"
  },
  "patterns": {
    "data-fetching": "Server Actions",
    "state-management": "Zustand"
  },
  "recent_files": [
    "src/app/dashboard/page.tsx",
    "src/components/Button.tsx"
  ]
}
```

## 버전 마이그레이션

스키마 버전이 변경될 경우:

```text
1. 기존 파일 백업 (.bak)
2. 새 스키마로 변환
3. 변환 실패 시 백업 복원
```
