"""Gemini API Adapter

Google Gemini Pro를 사용한 코드 검증.
API 키 또는 OAuth 토큰 지원.
"""

import json
import os
from dataclasses import dataclass

import httpx


@dataclass
class GeminiResponse:
    """Gemini API 응답."""

    issues: list[dict]
    suggestions: list[str]
    confidence: float
    raw_response: str


class GeminiAdapter:
    """Google Gemini Pro API 어댑터.

    API 키(환경변수) 또는 OAuth 토큰 지원.

    Example:
        # API 키 사용 (환경변수에서 자동 로드)
        adapter = GeminiAdapter()
        result = await adapter.verify_code(code, "python", "security")

        # 또는 토큰 직접 전달
        adapter = GeminiAdapter(token=api_key)
    """

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    TIMEOUT = 30.0

    def __init__(self, token: str | None = None):
        """초기화.

        Args:
            token: API 키 또는 OAuth 토큰 (없으면 환경변수에서 로드)

        Raises:
            ValueError: 토큰/API 키가 없는 경우
        """
        self.token = (
            token
            or os.environ.get("GEMINI_API_KEY")
            or os.environ.get("GOOGLE_API_KEY")
        )

        if not self.token:
            raise ValueError(
                "Gemini API 키가 필요합니다.\n"
                "환경변수를 설정하세요:\n"
                "  set GEMINI_API_KEY=your-key"
            )

    async def verify_code(
        self, code: str, language: str, prompt: str
    ) -> GeminiResponse:
        """코드 검증 요청.

        Args:
            code: 검증할 코드
            language: 프로그래밍 언어
            prompt: 검증 프롬프트

        Returns:
            GeminiResponse: 검증 결과
        """
        url = f"{self.BASE_URL}?key={self.token}"

        async with httpx.AsyncClient(timeout=self.TIMEOUT) as client:
            response = await client.post(
                url,
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": f"당신은 시니어 코드 리뷰어입니다. JSON 형식으로만 응답하세요.\n\n{prompt}"
                                }
                            ]
                        }
                    ],
                    "generationConfig": {"temperature": 0.3, "maxOutputTokens": 2000},
                },
            )
            response.raise_for_status()
            data = response.json()

        # Gemini 응답 구조에서 텍스트 추출
        raw_response = data["candidates"][0]["content"]["parts"][0]["text"]
        return self._parse_response(raw_response)

    def _parse_response(self, raw: str) -> GeminiResponse:
        """응답 파싱.

        Args:
            raw: 원본 응답 텍스트

        Returns:
            GeminiResponse: 파싱된 결과
        """
        try:
            # JSON 추출 (마크다운 코드블록 처리)
            json_str = raw
            if "```json" in raw:
                json_str = raw.split("```json")[1].split("```")[0]
            elif "```" in raw:
                json_str = raw.split("```")[1].split("```")[0]

            parsed = json.loads(json_str.strip())

            return GeminiResponse(
                issues=parsed.get("issues", []),
                suggestions=parsed.get("suggestions", []),
                confidence=float(parsed.get("confidence", 0.8)),
                raw_response=raw,
            )
        except (json.JSONDecodeError, IndexError, KeyError):
            # 파싱 실패 시 기본값
            return GeminiResponse(
                issues=[],
                suggestions=["응답 파싱 실패 - 원본 확인 필요"],
                confidence=0.0,
                raw_response=raw,
            )
