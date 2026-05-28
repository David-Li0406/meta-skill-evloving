"""Provider Router

Provider 선택 및 병렬 검증 관리.
OAuth 토큰 우선, API 키 환경변수 fallback.
"""

import asyncio
from dataclasses import dataclass, field
from pathlib import Path
import sys
from typing import Any, Literal

# 경로 설정을 가장 먼저 수행
_ROUTER_DIR = Path(__file__).resolve().parent

# 부모 디렉토리 (cross-ai-verifier/scripts)
_PARENT_DIR = _ROUTER_DIR.parent
if str(_PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(_PARENT_DIR))

# ultimate-debate 패키지 경로 추가
_ULTIMATE_DEBATE_SRC = (
    _ROUTER_DIR.parent.parent.parent.parent.parent / "ultimate-debate" / "src"
)
if str(_ULTIMATE_DEBATE_SRC) not in sys.path:
    sys.path.insert(0, str(_ULTIMATE_DEBATE_SRC))

# TokenStore import (ultimate-debate.auth에서)
try:
    from ultimate_debate.auth.storage import TokenStore

    HAS_TOKEN_STORAGE = True
except ImportError:
    HAS_TOKEN_STORAGE = False
    TokenStore = None

# Adapters import
from providers.adapters.openai_adapter import OpenAIAdapter
from providers.adapters.gemini_adapter import GeminiAdapter

ProviderType = Literal["openai", "gemini"]


@dataclass
class VerifyResult:
    """검증 결과."""

    provider: str
    issues: list[dict] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    confidence: float = 0.0
    raw_response: str = ""
    error: str | None = None


class ProviderRouter:
    """Provider 라우터.

    다중 AI Provider 관리 및 병렬 검증 지원.

    인증 우선순위:
    1. OAuth 토큰 (TokenStorage에서 로드)
    2. API 키 환경변수 (fallback)

    Example:
        # OAuth 토큰 또는 API 키 자동 로드
        router = ProviderRouter()
        result = await router.verify(code, "openai", prompt)

        # 병렬 검증
        results = await router.verify_parallel(code, prompt)
    """

    SUPPORTED_PROVIDERS = ["openai", "gemini"]

    def __init__(self):
        """초기화.

        OAuth 토큰을 우선 로드하고, 없으면 API 키 환경변수 사용.
        """
        self._token_storage = TokenStore() if HAS_TOKEN_STORAGE else None

    def _get_oauth_token(self, provider: str) -> str | None:
        """OAuth 토큰 조회.

        Args:
            provider: Provider 이름

        Returns:
            OAuth access_token 또는 None
        """
        if not self._token_storage:
            return None

        # Provider 이름 매핑 (cross-ai-verifier → multi-ai-auth)
        storage_name = "openai" if provider == "openai" else "google"
        token = self._token_storage.get_valid_token(storage_name)

        if token:
            return token.access_token
        return None

    def _get_adapter(self, provider: str):
        """어댑터 생성.

        OAuth 토큰을 우선 사용하고, 없으면 API 키 환경변수 fallback.

        Args:
            provider: Provider 이름

        Returns:
            해당 Provider의 어댑터

        Raises:
            ValueError: 지원하지 않는 Provider
        """
        # OAuth 토큰 우선 조회
        oauth_token = self._get_oauth_token(provider)

        if provider == "openai":
            return OpenAIAdapter(token=oauth_token)
        elif provider == "gemini":
            return GeminiAdapter(token=oauth_token)
        else:
            raise ValueError(f"지원하지 않는 Provider: {provider}")

    async def verify(
        self, code: str, provider: ProviderType, prompt: str, language: str = "python"
    ) -> VerifyResult:
        """단일 Provider 검증.

        API 키는 환경변수에서 자동 로드됩니다.

        Args:
            code: 검증할 코드
            provider: 사용할 Provider
            prompt: 검증 프롬프트
            language: 프로그래밍 언어

        Returns:
            VerifyResult: 검증 결과
        """
        try:
            adapter = self._get_adapter(provider)
            response = await adapter.verify_code(code, language, prompt)

            return VerifyResult(
                provider=provider,
                issues=response.issues,
                suggestions=response.suggestions,
                confidence=response.confidence,
                raw_response=response.raw_response,
            )

        except Exception as e:
            return VerifyResult(provider=provider, error=str(e))

    async def verify_parallel(
        self,
        code: str,
        prompt: str,
        providers: list[ProviderType] | None = None,
        language: str = "python",
    ) -> list[VerifyResult]:
        """다중 Provider 병렬 검증.

        Args:
            code: 검증할 코드
            prompt: 검증 프롬프트
            providers: 사용할 Provider 목록 (기본: 모두)
            language: 프로그래밍 언어

        Returns:
            list[VerifyResult]: 각 Provider의 검증 결과
        """
        providers = providers or self.SUPPORTED_PROVIDERS

        tasks = [
            self.verify(code, provider, prompt, language) for provider in providers
        ]

        return await asyncio.gather(*tasks)

    def aggregate_results(self, results: list[VerifyResult]) -> dict[str, Any]:
        """결과 집계.

        Args:
            results: 검증 결과 목록

        Returns:
            dict: 집계된 결과
        """
        all_issues = []
        all_suggestions = []
        confidences = []
        errors = []

        for result in results:
            if result.error:
                errors.append({"provider": result.provider, "error": result.error})
            else:
                all_issues.extend(
                    [{**issue, "source": result.provider} for issue in result.issues]
                )
                all_suggestions.extend(result.suggestions)
                confidences.append(result.confidence)

        # 중복 제거 (같은 라인, 비슷한 메시지)
        unique_issues = self._deduplicate_issues(all_issues)

        return {
            "issues": unique_issues,
            "suggestions": list(set(all_suggestions)),
            "avg_confidence": (
                sum(confidences) / len(confidences) if confidences else 0.0
            ),
            "providers_used": [r.provider for r in results if not r.error],
            "errors": errors,
        }

    def _deduplicate_issues(self, issues: list[dict]) -> list[dict]:
        """이슈 중복 제거.

        같은 라인에서 발견된 비슷한 이슈는 병합.

        Args:
            issues: 이슈 목록

        Returns:
            list[dict]: 중복 제거된 이슈
        """
        seen = {}
        for issue in issues:
            key = (issue.get("line", 0), issue.get("severity", ""))
            if key not in seen:
                seen[key] = issue
            else:
                # 같은 라인/심각도면 source 병합
                existing = seen[key]
                existing_sources = existing.get("source", "")
                new_source = issue.get("source", "")
                if new_source and new_source not in existing_sources:
                    existing["source"] = f"{existing_sources}, {new_source}"

        return list(seen.values())
