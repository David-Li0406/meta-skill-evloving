---
name: function-calling-agent
description: OpenAI/Gemini Function Calling을 활용한 에이전트 구현 가이드. LLM이 외부 API를 Tool로 호출하는 패턴. "function calling", "tool", "agent", "openai tools", "gemini tools" 키워드로 트리거.
---

# Function Calling Agent Guide

## 개요

LLM이 외부 API를 Tool로 호출하여 작업을 수행하는 에이전트 패턴.
OpenAI와 Gemini 모두 지원.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Function Calling Agent Loop                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  User Message ──────────────────────────────────────────────────────┐   │
│       │                                                              │   │
│       ▼                                                              │   │
│  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │                    LLM with Tools                            │    │   │
│  │                                                              │    │   │
│  │  "사용자 요청을 분석하고, 필요한 Tool을 선택하여 호출합니다"  │    │   │
│  │                                                              │    │   │
│  │  Available Tools:                                            │    │   │
│  │   ├── tool_a(param1, param2, ...)                           │    │   │
│  │   ├── tool_b(param1, ...)                                   │    │   │
│  │   └── tool_c(...)                                           │    │   │
│  └─────────────────────────────────────────────────────────────┘    │   │
│       │                                                              │   │
│       ▼                                                              │   │
│  ┌─────────────┐    No tool calls?                                  │   │
│  │ Tool Calls? │ ──────────────────────► Return final response      │   │
│  └─────────────┘                                                     │   │
│       │ Yes                                                          │   │
│       ▼                                                              │   │
│  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │              Tool Executor (External APIs)                   │    │   │
│  │  - Execute tools with LLM-generated arguments                │    │   │
│  │  - Return results to LLM                                     │    │   │
│  └─────────────────────────────────────────────────────────────┘    │   │
│       │                                                              │   │
│       └──────────────────────────────────────────────────────────────┘   │
│                            (Loop until no more tool calls)              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Tool 정의 Best Practices (2026)

### 핵심 원칙

1. **Prescriptive Description**: "무엇을 하는가"가 아닌 "언제 사용하는가" 명시
2. **Front-load Rules**: 핵심 규칙과 요구사항을 설명 앞부분에 배치
3. **Strict Mode**: OpenAI는 `strict: true`로 스키마 검증 강제 (GPT-5.2 필수 권장)
4. **Strong Typing**: enum, 범위 제한 등으로 잘못된 입력 방지
5. **Preambles**: GPT-5.2는 Tool 호출 전 reasoning을 출력하도록 설정 권장

### 지원 모델 (2026)

**OpenAI**:
- GPT-5.2, GPT-5.2-Codex (최신)
- Responses API 권장 (Chain-of-Thought 유지)

**Google**:
- Gemini 3 Pro, Gemini 3 Flash (최신)
- Parallel & Compositional function calling 지원

### OpenAI Format (Strict Mode)

```python
OPENAI_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_places",
            "description": (
                # Prescriptive: WHEN to use
                "키워드 기반 장소 검색. "
                "사용 시점: 사용자가 특정 장소 유형을 키워드로 찾을 때. "
                # Edge cases
                "좌표가 없으면 전국 검색, 있으면 주변 검색. "
                # Dependencies
                "주의: 지역명 언급 시 먼저 geocode로 좌표 획득 후 호출."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        # Clear description with examples
                        "description": (
                            "검색 키워드. 장소 유형만 포함. "
                            "예: '재활용센터', '제로웨이스트샵'. "
                            "지역명은 포함하지 않음 (좌표로 처리)."
                        ),
                    },
                    "latitude": {
                        "type": "number",
                        # Range constraints
                        "description": "검색 중심 위도. 범위: 33.0~43.0 (한국)",
                    },
                    "longitude": {
                        "type": "number",
                        "description": "검색 중심 경도. 범위: 124.0~132.0 (한국)",
                    },
                },
                "required": ["query"],
                # Strict mode requirement
                "additionalProperties": False,
            },
            # Enable strict schema validation
            "strict": True,
        },
    },
]
```

### Gemini Format (Gemini 3)

Gemini 3는 4가지 Function Calling Mode 지원:
- **AUTO** (기본): 모델이 텍스트/함수 호출 자동 결정
- **ANY**: 항상 함수 호출
- **NONE**: 함수 호출 금지
- **VALIDATED**: 스키마 준수 보장하며 텍스트/함수 선택

```python
GEMINI_TOOLS = [
    {
        "name": "search_places",
        "description": (
            "키워드 기반 장소 검색. "
            "사용 시점: 특정 장소를 찾을 때. "
            "지역명 언급 시 먼저 geocode로 좌표 획득 후 호출."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "검색 키워드 (장소 유형). 예: '재활용센터'",
                },
                "latitude": {
                    "type": "number",
                    "description": "검색 중심 위도. 주변 검색 시 필수.",
                },
                "longitude": {
                    "type": "number",
                    "description": "검색 중심 경도. 주변 검색 시 필수.",
                },
            },
            "required": ["query"],
        },
    },
]

# Gemini 3 Config 예시
config = types.GenerateContentConfig(
    tools=[gemini_tools],
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(
            mode="AUTO",  # or "ANY", "NONE", "VALIDATED"
        ),
    ),
    temperature=0,  # 결정론적 Tool 선택
)
```

### Tool Description Anti-patterns

```python
# ❌ BAD: 무엇을 하는지만 설명
"description": "장소를 검색합니다."

# ❌ BAD: 너무 장황하고 비규범적
"description": "이 함수는 다양한 장소를 검색할 수 있는 유용한 도구입니다..."

# ✅ GOOD: 언제 사용하는지 명시 + 규칙 + 예외
"description": (
    "키워드 기반 장소 검색. "
    "사용 시점: 특정 장소 유형을 찾을 때. "
    "주의: 지역명 언급 시 먼저 geocode 호출 필요."
)
```

## System Prompt Best Practices (2026)

### GPT-5.2 CTCO Framework

GPT-5.2는 구조화된 프롬프트를 선호. CTCO 패턴 권장:

```
# Context: 배경 정보
# Task: 수행할 작업
# Constraints: 제약 조건 (DO/DON'T)
# Output: 출력 형식
```

### Preambles 활성화

GPT-5.2는 Tool 호출 전 reasoning을 출력하는 Preambles 기능 지원:

```python
# System prompt에 추가
"Before you call a tool, briefly explain why you are calling it."
```

이점:
- Tool 호출 정확도 향상
- 디버깅 용이
- 사용자 신뢰도 증가

### Scope Discipline

GPT-5.2는 충분히 강력해서 "작업을 발명"할 수 있음. 범위 제한 필수:

```python
# ❌ BAD: 모호한 지시
"필요한 작업을 수행하세요"

# ✅ GOOD: 명확한 범위 제한
"search_places 또는 geocode만 사용. 다른 작업 수행 금지."
```

### 핵심 구조: RBOE 패턴

```
# Role: 역할 정의 + 경계
# Boundaries: 도구 사용 시점 (DO/DON'T)
# Ordering: 도구 호출 순서
# Error: 에러 처리 가이드
```

### 예시: Location Agent System Prompt

```python
SYSTEM_PROMPT = """# Role
당신은 Eco² 앱의 위치 기반 장소 검색 에이전트입니다.
재활용센터, 제로웨이스트샵, 주변 시설 검색을 도와줍니다.

# Tool 사용 규칙

## 사용 시점 (DO)
- 재활용센터, 제로웨이스트샵 검색 → search_places
- 주변 카페, 편의점, 약국 검색 → search_category
- 지역명 언급 + 좌표 없음 → geocode 먼저 호출

## 사용 금지 (DON'T)
- 분리배출 방법 질문 → 도구 사용 X, 직접 답변
- 일반 대화, 인사 → 도구 사용 X
- 이미 좌표가 있는데 geocode 호출 X

# Tool 호출 순서 (Critical)

"[지역명] 근처 [장소]" 패턴:
1. geocode(place_name="지역명") → 좌표 획득
2. search_places(query="장소", latitude=결과lat, longitude=결과lon)

"주변 [카테고리]" 패턴 (좌표 있음):
1. search_category(category="카테고리", latitude=lat, longitude=lon)

# 에러 처리

- geocode 실패 → "해당 지역을 찾을 수 없습니다" 안내
- 검색 결과 없음 → 대안 제시 (다른 검색어, 반경 확대)
- 좌표 없이 search_category 시도 → 호출 안함, 위치 요청
"""
```

### System Prompt Anti-patterns

```python
# ❌ BAD: 도구 목록만 나열
"사용 가능한 도구: search_places, geocode, search_category"

# ❌ BAD: 호출 순서 미지정
"적절한 도구를 선택해서 사용하세요"

# ✅ GOOD: 시점 + 순서 + 경계 명시
"""
## 사용 시점 (DO)
- 재활용센터 검색 → search_places

## 사용 금지 (DON'T)
- 일반 대화 → 도구 사용 X

## 호출 순서
지역명 언급 시: geocode → search_places
"""
```

### 참고 자료

- [GPT-5.2 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5-1_prompting_guide)
- [GPT-5 New Params and Tools](https://cookbook.openai.com/examples/gpt-5/gpt-5_new_params_and_tools)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Gemini Function Calling](https://ai.google.dev/gemini-api/docs/function-calling)

## OpenAI Function Calling 구현 (GPT-5.2)

GPT-5.2는 Responses API 권장이나, Chat Completions API도 호환.

```python
import json
from openai import AsyncOpenAI

async def run_openai_agent(
    client: AsyncOpenAI,
    model: str,
    user_message: str,
    tools: list[dict],
    tool_executor: ToolExecutor,
    system_prompt: str = "",
    max_iterations: int = 5,
) -> dict:
    """OpenAI Function Calling Agent Loop.

    Args:
        client: OpenAI AsyncClient
        model: 모델명 (gpt-5.2, gpt-5.2-codex, etc.)
        user_message: 사용자 메시지
        tools: Tool 정의 리스트 (OpenAI format)
        tool_executor: Tool 실행기
        system_prompt: 시스템 프롬프트 (Preambles 포함 권장)
        max_iterations: 최대 반복 횟수 (무한 루프 방지)

    Returns:
        {"success": bool, "response": str, "tool_results": list}
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_message})

    all_tool_results = []

    for iteration in range(max_iterations):
        # 1. LLM 호출 (with tools)
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",  # LLM이 자동으로 tool 선택
        )

        assistant_message = response.choices[0].message

        # 2. Tool call이 없으면 최종 응답
        if not assistant_message.tool_calls:
            return {
                "success": True,
                "response": assistant_message.content,
                "tool_results": all_tool_results,
            }

        # 3. Assistant 메시지를 대화 이력에 추가
        messages.append(assistant_message.model_dump())

        # 4. 각 Tool call 실행
        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name
            try:
                arguments = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                arguments = {}

            # Tool 실행
            result = await tool_executor.execute(tool_name, arguments)

            all_tool_results.append({
                "tool": tool_name,
                "arguments": arguments,
                "result": result.data if result.success else {"error": result.error},
                "success": result.success,
            })

            # 5. Tool 결과를 메시지에 추가
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": json.dumps(
                    result.data if result.success else {"error": result.error},
                    ensure_ascii=False,
                ),
            })

    # Max iterations 도달
    return {
        "success": True,
        "response": "최대 반복 횟수 도달",
        "tool_results": all_tool_results,
    }
```

## Gemini Function Calling 구현 (Gemini 3)

Gemini 3 시리즈는 Parallel & Compositional function calling 지원.

```python
from google import genai
from google.genai import types

async def run_gemini_agent(
    client: genai.Client,
    model: str,
    user_message: str,
    tools: list[dict],
    tool_executor: ToolExecutor,
    system_prompt: str = "",
    max_iterations: int = 5,
) -> dict:
    """Gemini Function Calling Agent Loop.

    Args:
        client: Gemini Client
        model: 모델명 (gemini-3-flash, gemini-3-pro, etc.)
        user_message: 사용자 메시지
        tools: Tool 정의 리스트 (Gemini format)
        tool_executor: Tool 실행기
        system_prompt: 시스템 프롬프트
        max_iterations: 최대 반복 횟수

    Returns:
        {"success": bool, "response": str, "tool_results": list}
    """
    # Tool 설정
    gemini_tools = types.Tool(function_declarations=tools)
    config = types.GenerateContentConfig(
        tools=[gemini_tools],
        system_instruction=system_prompt if system_prompt else None,
    )

    contents = [user_message]
    all_tool_results = []

    for iteration in range(max_iterations):
        # 1. Gemini 호출
        response = await client.aio.models.generate_content(
            model=model,
            contents=contents,
            config=config,
        )

        candidate = response.candidates[0]
        part = candidate.content.parts[0]

        # 2. Function call이 없으면 최종 응답
        if not hasattr(part, "function_call") or part.function_call is None:
            return {
                "success": True,
                "response": part.text if hasattr(part, "text") else "",
                "tool_results": all_tool_results,
            }

        # 3. Function call 실행
        function_call = part.function_call
        tool_name = function_call.name
        arguments = dict(function_call.args) if function_call.args else {}

        # Tool 실행
        result = await tool_executor.execute(tool_name, arguments)

        all_tool_results.append({
            "tool": tool_name,
            "arguments": arguments,
            "result": result.data if result.success else {"error": result.error},
            "success": result.success,
        })

        # 4. 대화 이력 업데이트
        contents.append(candidate.content)

        # 5. Function 결과 추가
        function_response = types.Part.from_function_response(
            name=tool_name,
            response=result.data if result.success else {"error": result.error},
        )
        contents.append(types.Content(role="user", parts=[function_response]))

    return {
        "success": True,
        "response": "최대 반복 횟수 도달",
        "tool_results": all_tool_results,
    }
```

## Tool Executor 패턴

```python
from dataclasses import dataclass
from typing import Any

@dataclass
class ToolResult:
    """Tool 실행 결과."""
    tool_name: str
    success: bool
    data: dict[str, Any] | None = None
    error: str | None = None


class ToolExecutor:
    """Tool 실행기 기본 클래스."""

    def __init__(self, **clients):
        """외부 API 클라이언트 주입."""
        self._clients = clients

    async def execute(self, tool_name: str, arguments: dict) -> ToolResult:
        """Tool 실행.

        Args:
            tool_name: Tool 이름
            arguments: LLM이 생성한 인자

        Returns:
            ToolResult
        """
        # Tool 이름에 해당하는 메서드 호출
        method = getattr(self, f"_execute_{tool_name}", None)
        if method is None:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                error=f"Unknown tool: {tool_name}",
            )

        try:
            return await method(arguments)
        except Exception as e:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                error=str(e),
            )

    async def _execute_tool_a(self, args: dict) -> ToolResult:
        """Tool A 구현."""
        # 외부 API 호출
        client = self._clients.get("api_a_client")
        response = await client.some_method(args["param1"])
        return ToolResult(
            tool_name="tool_a",
            success=True,
            data={"result": response},
        )
```

## LangGraph 노드로 통합

```python
def create_agent_node(
    tool_executor: ToolExecutor,
    tools: list[dict],
    event_publisher: ProgressNotifierPort,
    openai_client: AsyncOpenAI | None = None,
    gemini_client: genai.Client | None = None,
    default_model: str = "gpt-5.2",  # GPT-5.2 권장
    default_provider: str = "openai",
    system_prompt: str = "",
):
    """Function Calling Agent 노드 팩토리.

    Args:
        tool_executor: Tool 실행기
        tools: Tool 정의 리스트
        event_publisher: Progress 알림기
        openai_client: OpenAI 클라이언트 (선택)
        gemini_client: Gemini 클라이언트 (선택)
        default_model: 기본 모델
        default_provider: 기본 프로바이더
        system_prompt: 시스템 프롬프트

    Returns:
        LangGraph 노드 함수
    """

    async def agent_node(state: dict) -> dict:
        """LangGraph 노드."""
        job_id = state.get("job_id", "")
        message = state.get("message", "")

        # 프론트엔드가 보낸 모델/프로바이더 사용
        provider = state.get("llm_provider", default_provider)
        model = state.get("llm_model", default_model)

        await event_publisher.notify_stage(
            task_id=job_id,
            stage="agent",
            status="started",
            message="처리 중...",
        )

        try:
            if provider == "gemini" and gemini_client:
                result = await run_gemini_agent(
                    client=gemini_client,
                    model=model,
                    user_message=message,
                    tools=convert_to_gemini_format(tools),
                    tool_executor=tool_executor,
                    system_prompt=system_prompt,
                )
            elif openai_client:
                result = await run_openai_agent(
                    client=openai_client,
                    model=model,
                    user_message=message,
                    tools=tools,
                    tool_executor=tool_executor,
                    system_prompt=system_prompt,
                )
            else:
                # Fallback 로직
                result = {"success": False, "error": "No LLM client available"}

            await event_publisher.notify_stage(
                task_id=job_id,
                stage="agent",
                status="completed",
            )

            return {
                "agent_context": {
                    "success": result.get("success"),
                    "response": result.get("response"),
                    "tool_results": result.get("tool_results", []),
                },
            }

        except Exception as e:
            await event_publisher.notify_stage(
                task_id=job_id,
                stage="agent",
                status="failed",
                result={"error": str(e)},
            )
            return {"agent_context": {"success": False, "error": str(e)}}

    return agent_node
```

## Dependencies 설정

```python
# dependencies.py

# Raw SDK 클라이언트 싱글톤
_openai_async_client = None
_gemini_client = None


def get_openai_async_client() -> AsyncOpenAI | None:
    """OpenAI AsyncOpenAI 클라이언트 싱글톤."""
    global _openai_async_client
    if _openai_async_client is None:
        settings = get_settings()
        if not settings.openai_api_key:
            return None

        from openai import AsyncOpenAI
        import httpx

        http_client = httpx.AsyncClient(timeout=httpx.Timeout(60.0))
        _openai_async_client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            http_client=http_client,
            max_retries=3,
        )
    return _openai_async_client


def get_gemini_client() -> genai.Client | None:
    """Google Gemini Client 싱글톤."""
    global _gemini_client
    if _gemini_client is None:
        settings = get_settings()
        if not settings.google_api_key:
            return None

        from google import genai
        _gemini_client = genai.Client(api_key=settings.google_api_key)

    return _gemini_client
```

## 실제 적용 예시: Location Agent

```python
# Tool 정의
LOCATION_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_places",
            "description": "키워드로 장소 검색",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "geocode",
            "description": "장소명을 좌표로 변환",
            "parameters": {
                "type": "object",
                "properties": {"place_name": {"type": "string"}},
                "required": ["place_name"],
            },
        },
    },
]

# Tool Executor
class KakaoToolExecutor(ToolExecutor):
    async def _execute_search_places(self, args: dict) -> ToolResult:
        response = await self._clients["kakao"].search_keyword(
            query=args["query"],
            x=args.get("longitude"),
            y=args.get("latitude"),
        )
        return ToolResult(tool_name="search_places", success=True, data={...})

    async def _execute_geocode(self, args: dict) -> ToolResult:
        response = await self._clients["kakao"].search_keyword(
            query=args["place_name"], size=1
        )
        if response.places:
            return ToolResult(
                tool_name="geocode",
                success=True,
                data={"lat": ..., "lon": ...},
            )
        return ToolResult(tool_name="geocode", success=False, error="Not found")

# 노드 생성
location_node = create_agent_node(
    tool_executor=KakaoToolExecutor(kakao=kakao_client),
    tools=LOCATION_TOOLS,
    event_publisher=event_publisher,
    openai_client=openai_client,
    gemini_client=gemini_client,
    system_prompt="당신은 위치 기반 검색을 도와주는 어시스턴트입니다...",
)
```

## Best Practices (2026)

1. **Tool Description**: Prescriptive하게 "언제" 사용하는지 명시
2. **Strict Mode**: OpenAI는 항상 `strict: true` 활성화 (GPT-5.2 필수 권장)
3. **Preambles**: GPT-5.2에서 Tool 호출 전 reasoning 출력 활성화
4. **Scope Discipline**: 모델이 "작업을 발명"하지 않도록 범위 제한
5. **Low Temperature**: Gemini는 temperature 0으로 설정 (결정론적 Tool 선택)
6. **Max Iterations**: 무한 루프 방지를 위해 최대 반복 횟수 설정
7. **VALIDATED Mode**: Gemini 3에서 스키마 준수 보장 필요 시 사용
8. **Error Handling**: Tool 실패 시 의미 있는 에러 메시지 반환
9. **Tool 개수 제한**: 10-20개 이내로 유지 (정확도 최적화)

## Reference

- OpenAI Function Calling: https://platform.openai.com/docs/guides/function-calling
- GPT-5.2 Prompting Guide: https://cookbook.openai.com/examples/gpt-5/gpt-5-1_prompting_guide
- Gemini Function Calling: https://ai.google.dev/gemini-api/docs/function-calling
- LangGraph: https://langchain-ai.github.io/langgraph/
