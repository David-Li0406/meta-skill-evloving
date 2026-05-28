"""Verify Prompt Builder

검증 목적에 따른 프롬프트 생성.
"""

from typing import Literal

FocusType = Literal["security", "bugs", "performance", "all"]


FOCUS_PROMPTS = {
    "security": """보안 취약점을 분석하세요:
- SQL Injection, XSS, CSRF 등 OWASP Top 10
- 하드코딩된 비밀번호/API 키
- 안전하지 않은 암호화
- 권한 검증 누락
- 입력 검증 부재""",
    "bugs": """논리 오류 및 버그를 검사하세요:
- Off-by-one 에러
- Null/None 참조 가능성
- 예외 처리 누락
- 경쟁 조건 (Race Condition)
- 데드락 가능성
- 메모리 누수""",
    "performance": """성능 이슈를 검사하세요:
- 불필요한 루프/재계산
- N+1 쿼리 문제
- 메모리 사용량 최적화
- 알고리즘 복잡도 (O(n²) 이상)
- 캐싱 기회
- 비동기 처리 개선점""",
    "all": """종합적인 코드 리뷰를 수행하세요:
1. 보안: 취약점 및 민감정보 노출
2. 버그: 논리 오류 및 예외 처리
3. 성능: 최적화 가능 영역
4. 가독성: 코드 스타일 및 명명 규칙
5. 유지보수성: 구조 및 의존성""",
}


def build_verify_prompt(code: str, language: str, focus: FocusType = "all") -> str:
    """검증용 프롬프트 생성.

    Args:
        code: 검증할 코드
        language: 프로그래밍 언어
        focus: 검증 초점 (security, bugs, performance, all)

    Returns:
        str: AI에게 전달할 프롬프트
    """
    focus_instruction = FOCUS_PROMPTS.get(focus, FOCUS_PROMPTS["all"])

    return f"""다음 {language} 코드를 분석하세요.

{focus_instruction}

```{language}
{code}
```

반드시 다음 JSON 형식으로만 응답하세요:
{{
    "issues": [
        {{
            "severity": "high|medium|low",
            "line": 라인번호,
            "message": "문제 설명",
            "suggestion": "해결 방안"
        }}
    ],
    "suggestions": ["전반적인 개선 제안"],
    "confidence": 0.0부터 1.0 사이의 신뢰도
}}

이슈가 없으면 빈 배열을 반환하세요."""


def build_compare_prompt(results: list[dict]) -> str:
    """다중 AI 결과 비교 프롬프트.

    Args:
        results: 각 Provider의 검증 결과 목록

    Returns:
        str: 비교 분석 프롬프트
    """
    results_text = "\n\n".join(
        [f"=== {r['provider']} 결과 ===\n{r['raw_response']}" for r in results]
    )

    return f"""다음은 여러 AI 모델의 코드 검증 결과입니다:

{results_text}

이 결과들을 비교 분석하여 다음을 제공하세요:
1. 공통적으로 발견된 이슈
2. 특정 모델만 발견한 이슈
3. 종합 신뢰도 점수
4. 최종 권장 사항

JSON 형식으로 응답하세요."""
