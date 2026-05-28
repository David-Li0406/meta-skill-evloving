#!/usr/bin/env python3
"""
기획 결과 머지 모듈
여러 에이전트의 기획 결과를 분석하고 통합합니다.
"""

import asyncio
import json
import os
from typing import Optional

# Anthropic SDK 사용 여부 확인
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


def get_merge_prompt(topic: str, results: list[dict]) -> str:
    """머지 프롬프트 생성"""
    plans_text = ""
    for r in results:
        agent = r["agent"]
        result = r["result"]
        plans_text += f"""
### {agent['name']} 기획안

{result}

---
"""

    return f"""다음은 "{topic}"에 대해 여러 AI 에이전트가 작성한 개별 기획안들입니다.
이들을 분석하고 통합된 최종 기획안을 작성해주세요.

{plans_text}

## 통합 기획안 작성 지침

1. **공통 아이디어**: 여러 에이전트가 공통으로 제안한 핵심 아이디어를 정리
2. **고유 아이디어**: 특정 에이전트만 제안한 창의적인 아이디어를 별도 정리
3. **최종 권장안**: 가장 효과적인 요소들을 조합한 통합 기획안
4. **의사결정 포인트**: 사용자가 선택해야 할 옵션들 (체크리스트 형태)
5. **충돌 해결**: 에이전트 간 상반된 제안이 있다면 각각의 장단점 분석

다음 형식으로 작성해주세요:

## 공통 아이디어
- ...

## 고유 아이디어
### {results[0]['agent']['name']}만 제안
- ...

### {results[1]['agent']['name'] if len(results) > 1 else '기타'}만 제안
- ...

## 최종 권장 기획안

### 핵심 목표
...

### 주요 기능 (우선순위 순)
1. [필수] ...
2. [필수] ...
3. [권장] ...

### 구현 로드맵
1. Phase 1: ...
2. Phase 2: ...

### 예상 리스크 및 대응
| 리스크 | 대응 방안 |
|-------|---------|
| ... | ... |

## 의사결정 체크리스트

아래 항목들은 사용자의 판단이 필요합니다:

- [ ] **선택 1**: A 방식 vs B 방식
  - A 방식: [장점/단점]
  - B 방식: [장점/단점]

- [ ] **선택 2**: ...

## 에이전트별 강점 요약
| 에이전트 | 강점 포인트 |
|---------|------------|
| ... | ... |
"""


async def merge_plans(
    topic: str,
    results: list[dict],
    model: str = "claude-sonnet-4-20250514",
    timeout: int = 180
) -> str:
    """
    여러 에이전트의 기획 결과를 머지합니다.

    Args:
        topic: 기획 주제
        results: 에이전트별 결과 리스트 [{"agent": {...}, "result": "..."}]
        model: 머지에 사용할 Claude 모델
        timeout: 타임아웃 (초)

    Returns:
        통합된 기획안 텍스트
    """
    # 결과가 1개면 머지 불필요
    if len(results) == 1:
        return f"""## 단일 에이전트 결과

에이전트가 1개뿐이므로 머지 없이 해당 기획안을 사용합니다.

{results[0]['result']}
"""

    # 모든 결과가 오류인 경우
    valid_results = [r for r in results if not r["result"].startswith("[오류]")]
    if not valid_results:
        return """## 머지 실패

모든 에이전트에서 오류가 발생했습니다. 개별 오류 메시지를 확인해주세요.
"""

    prompt = get_merge_prompt(topic, results)
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        # API 키가 없으면 간단한 텍스트 머지 수행
        return _simple_merge(topic, results)

    if HAS_ANTHROPIC:
        return await _merge_with_sdk(prompt, model, timeout, api_key)
    else:
        return await _merge_with_curl(prompt, model, timeout, api_key)


async def _merge_with_sdk(
    prompt: str,
    model: str,
    timeout: int,
    api_key: str
) -> str:
    """Anthropic SDK를 사용하여 머지"""
    try:
        client = anthropic.Anthropic(api_key=api_key)

        def sync_call():
            response = client.messages.create(
                model=model,
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text

        result = await asyncio.wait_for(
            asyncio.to_thread(sync_call),
            timeout=timeout
        )
        return result

    except asyncio.TimeoutError:
        return f"[머지 타임아웃] {timeout}초 초과. 개별 기획안을 직접 검토해주세요."
    except Exception as e:
        return f"[머지 오류] {str(e)}"


async def _merge_with_curl(
    prompt: str,
    model: str,
    timeout: int,
    api_key: str
) -> str:
    """curl을 사용하여 머지"""
    payload = {
        "model": model,
        "max_tokens": 4096,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    cmd = [
        "curl", "-s",
        "-X", "POST",
        "https://api.anthropic.com/v1/messages",
        "-H", f"x-api-key: {api_key}",
        "-H", "anthropic-version: 2023-06-01",
        "-H", "content-type: application/json",
        "-d", json.dumps(payload)
    ]

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await asyncio.wait_for(
            proc.communicate(),
            timeout=timeout
        )

        if proc.returncode != 0:
            return f"[머지 오류] curl 실패: {stderr.decode()}"

        response = json.loads(stdout.decode())

        if "error" in response:
            return f"[머지 오류] API 오류: {response['error']['message']}"

        return response["content"][0]["text"]

    except asyncio.TimeoutError:
        return f"[머지 타임아웃] {timeout}초 초과"
    except Exception as e:
        return f"[머지 오류] {str(e)}"


def _simple_merge(topic: str, results: list[dict]) -> str:
    """API 없이 간단한 텍스트 머지"""
    merged = f"""## 통합 기획안 (간단 머지)

> ANTHROPIC_API_KEY가 설정되지 않아 AI 기반 머지를 수행할 수 없습니다.
> 아래는 각 에이전트의 기획안을 나열한 것입니다.

---

"""

    for i, r in enumerate(results, 1):
        agent = r["agent"]
        merged += f"""### {agent['name']} 주요 포인트

{r['result'][:500]}...

---

"""

    merged += """
## 다음 단계

1. 위 기획안들을 직접 검토하세요
2. 각 기획안에서 좋은 아이디어를 선별하세요
3. 필요시 ANTHROPIC_API_KEY를 설정하고 다시 실행하면 AI 기반 머지가 수행됩니다
"""

    return merged
