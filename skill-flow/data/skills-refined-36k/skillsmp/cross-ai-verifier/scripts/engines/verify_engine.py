"""Verify Engine

코드 검증 핵심 엔진.
"""

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# 부모 디렉토리를 sys.path에 추가
_PARENT_DIR = Path(__file__).parent.parent
if str(_PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(_PARENT_DIR))

from providers.router import ProviderRouter, VerifyResult
from prompts.verify_prompt import build_verify_prompt, FocusType


@dataclass
class VerificationReport:
    """검증 보고서."""

    file_path: str | None = None
    language: str = "python"
    focus: str = "all"
    results: list[VerifyResult] = field(default_factory=list)
    aggregated: dict[str, Any] = field(default_factory=dict)

    def summary(self) -> str:
        """요약 문자열 생성."""
        total_issues = len(self.aggregated.get("issues", []))
        high = sum(
            1 for i in self.aggregated.get("issues", []) if i.get("severity") == "high"
        )
        medium = sum(
            1
            for i in self.aggregated.get("issues", [])
            if i.get("severity") == "medium"
        )
        low = sum(
            1 for i in self.aggregated.get("issues", []) if i.get("severity") == "low"
        )

        providers = ", ".join(self.aggregated.get("providers_used", []))
        confidence = self.aggregated.get("avg_confidence", 0) * 100

        return f"""
## Cross-AI 검증 결과

| 항목 | 값 |
|------|-----|
| 파일 | {self.file_path or "직접 입력"} |
| 언어 | {self.language} |
| Focus | {self.focus} |
| Providers | {providers} |
| 신뢰도 | {confidence:.1f}% |

### 발견된 이슈 ({total_issues}개)
- 🔴 High: {high}
- 🟡 Medium: {medium}
- 🟢 Low: {low}

### 상세 이슈
"""

    def format_issues(self) -> str:
        """이슈 상세 포맷."""
        lines = []
        for issue in self.aggregated.get("issues", []):
            severity = issue.get("severity", "unknown")
            line_num = issue.get("line", "?")
            message = issue.get("message", "")
            source = issue.get("source", "")

            icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(severity, "⚪")
            lines.append(f"{icon} **Line {line_num}** [{source}]: {message}")

        return "\n".join(lines) if lines else "이슈가 발견되지 않았습니다. ✅"


class VerifyEngine:
    """코드 검증 엔진.

    Multi-AI Auth의 토큰을 사용하여 외부 AI에 코드 검증 요청.

    Example:
        engine = VerifyEngine()

        # 단일 Provider
        report = await engine.verify("def foo(): pass", "python", "security", "openai")

        # 병렬 검증
        report = await engine.verify_parallel("def foo(): pass", "python", "all")
    """

    def __init__(self):
        """초기화."""
        self.router = ProviderRouter()

    async def verify(
        self,
        code: str,
        language: str = "python",
        focus: FocusType = "all",
        provider: str = "openai",
        file_path: str | None = None,
    ) -> VerificationReport:
        """단일 Provider 검증.

        Args:
            code: 검증할 코드
            language: 프로그래밍 언어
            focus: 검증 초점
            provider: 사용할 Provider
            file_path: 원본 파일 경로 (보고서용)

        Returns:
            VerificationReport: 검증 보고서
        """
        prompt = build_verify_prompt(code, language, focus)
        result = await self.router.verify(code, provider, prompt, language)

        report = VerificationReport(
            file_path=file_path,
            language=language,
            focus=focus,
            results=[result],
            aggregated=self.router.aggregate_results([result]),
        )

        return report

    async def verify_parallel(
        self,
        code: str,
        language: str = "python",
        focus: FocusType = "all",
        providers: list[str] | None = None,
        file_path: str | None = None,
    ) -> VerificationReport:
        """다중 Provider 병렬 검증.

        Args:
            code: 검증할 코드
            language: 프로그래밍 언어
            focus: 검증 초점
            providers: 사용할 Provider 목록 (기본: 모두)
            file_path: 원본 파일 경로 (보고서용)

        Returns:
            VerificationReport: 검증 보고서
        """
        prompt = build_verify_prompt(code, language, focus)
        results = await self.router.verify_parallel(code, prompt, providers, language)

        report = VerificationReport(
            file_path=file_path,
            language=language,
            focus=focus,
            results=results,
            aggregated=self.router.aggregate_results(results),
        )

        return report

    async def verify_file(
        self,
        file_path: str,
        focus: FocusType = "all",
        provider: str | None = None,
        parallel: bool = False,
    ) -> VerificationReport:
        """파일 검증.

        Args:
            file_path: 파일 경로
            focus: 검증 초점
            provider: 사용할 Provider (parallel=False일 때)
            parallel: 병렬 검증 여부

        Returns:
            VerificationReport: 검증 보고서
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

        code = path.read_text(encoding="utf-8")
        language = self._detect_language(path.suffix)

        if parallel:
            return await self.verify_parallel(
                code, language, focus, file_path=file_path
            )
        else:
            return await self.verify(
                code, language, focus, provider or "openai", file_path=file_path
            )

    def _detect_language(self, suffix: str) -> str:
        """파일 확장자로 언어 감지.

        Args:
            suffix: 파일 확장자 (예: ".py")

        Returns:
            str: 언어 이름
        """
        mapping = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".jsx": "javascript",
            ".java": "java",
            ".go": "go",
            ".rs": "rust",
            ".rb": "ruby",
            ".php": "php",
            ".cs": "csharp",
            ".cpp": "cpp",
            ".c": "c",
            ".swift": "swift",
            ".kt": "kotlin",
        }
        return mapping.get(suffix.lower(), "text")
