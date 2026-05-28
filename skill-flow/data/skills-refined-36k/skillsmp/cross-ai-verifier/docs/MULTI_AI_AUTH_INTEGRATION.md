# Multi-AI Auth 통합 가이드

Cross-AI Verifier와 Multi-AI Auth Skill 통합 방법

## 개요

Cross-AI Verifier는 **OAuth 로그인 방식만 지원**합니다.
API 키 환경변수는 지원하지 않습니다.

ProviderRouter는 Multi-AI Auth의 TokenStore를 통해 OAuth 토큰을 자동으로 관리합니다.

## 사용 방법

### OAuth 로그인 (필수)

검증을 실행하기 전에 반드시 로그인해야 합니다:

```bash
# OpenAI 로그인 (ChatGPT Plus/Pro 구독 필요)
/ai-auth login --provider openai

# Google 로그인 (Gemini 사용)
/ai-auth login --provider google
```

### 검증 실행

```python
from providers.router import ProviderRouter

router = ProviderRouter()  # Multi-AI Auth 필수
result = await router.verify(code, "openai", prompt)

# 토큰이 없으면 자동으로 에러 발생:
# ❌ OPENAI 인증이 필요합니다.
#    다음 명령어로 로그인하세요:
#    /ai-auth login --provider openai
```

## 구현 상세

### TokenStore Import 경로

```python
# 절대 경로로 안정적인 import
.claude/skills/cross-ai-verifier/
└── scripts/providers/router.py
    └── imports from: .claude/skills/multi-ai-auth/scripts/storage/token_store.py
```

### 주요 메서드

| 메서드 | 역할 |
|--------|------|
| `__init__()` | TokenStore 초기화 (필수) |
| `ensure_authenticated(provider)` | 토큰 확인 + 로그인 안내 |
| `_get_token(provider)` | TokenStore에서 토큰 조회 |

### 에러 메시지

토큰이 없는 경우:
```
❌ OPENAI 인증이 필요합니다.
   다음 명령어로 로그인하세요:
   /ai-auth login --provider openai
```

Multi-AI Auth 스킬이 없는 경우:
```
Multi-AI Auth 스킬이 필요합니다.
OAuth 로그인을 위해 multi-ai-auth 스킬을 설치하세요.
```

## 의존성

- **Multi-AI Auth Skill 필수**: 스킬이 없으면 ProviderRouter 초기화 실패
- **OAuth 토큰 필수**: 토큰 없이는 검증 불가

## 보안

- API 키 환경변수 지원 없음 (보안 강화)
- OAuth 토큰은 OS 자격증명 저장소에 안전하게 보관
- 토큰 만료 시 자동 확인 및 재로그인 안내
