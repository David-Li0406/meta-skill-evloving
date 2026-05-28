# 프롬프트 평가 가이드

## 평가 차원

| 차원 | 설명 | 측정 방법 |
|------|------|-----------|
| Relevance | 질문에 대한 적합성 | Phase 1 Citation |
| Completeness | 필수 정보 포함 | Phase 2 Nugget |
| Groundedness | 근거 기반 여부 | Phase 3 Claim 검증 |
| Fluency | 자연스러운 표현 | 사람 평가 |
| Consistency | 캐릭터 일관성 | 톤/스타일 검사 |

---

## 자동 평가 메트릭

### 1. 길이 기반

```python
def evaluate_length(answer: str) -> dict:
    """길이 기반 평가"""
    words = len(answer.split())
    sentences = answer.count('.') + answer.count('!') + answer.count('?')

    return {
        "word_count": words,
        "sentence_count": sentences,
        "is_concise": sentences <= 3,  # 3문장 이내
        "score": 1.0 if sentences <= 3 else max(0, 1 - (sentences - 3) * 0.2),
    }
```

### 2. 키워드 커버리지

```python
def evaluate_coverage(
    answer: str,
    required_keywords: list[str],
) -> dict:
    """필수 키워드 커버리지"""
    found = [kw for kw in required_keywords if kw in answer]
    missing = [kw for kw in required_keywords if kw not in answer]

    return {
        "found_keywords": found,
        "missing_keywords": missing,
        "coverage": len(found) / len(required_keywords) if required_keywords else 1.0,
    }
```

### 3. 캐릭터 일관성

```python
def evaluate_character_consistency(answer: str) -> dict:
    """캐릭터 일관성 검사"""
    checks = {
        "uses_honorific": any(h in answer for h in ["요", "습니다", "세요"]),
        "has_emoji": any(c in answer for c in "🌿♻️📦🔍"),
        "is_encouraging": any(e in answer for e in ["멋져요", "좋아요", "완벽", "훌륭"]),
        "avoids_negative": not any(n in answer for n in ["안됩니다", "틀렸", "잘못"]),
    }

    score = sum(checks.values()) / len(checks)

    return {
        "checks": checks,
        "consistency_score": score,
    }
```

---

## LLM 기반 평가

### Relevance 평가

```python
RELEVANCE_EVAL_PROMPT = """
다음 질문과 답변의 관련성을 1-5점으로 평가하세요.

질문: {question}
답변: {answer}

평가 기준:
5: 질문에 완벽히 답변
4: 대부분 답변, 약간의 추가 정보 포함
3: 부분적으로 답변
2: 관련은 있으나 핵심 누락
1: 전혀 관련 없음

JSON 형식으로 응답:
{{"score": <1-5>, "reason": "<평가 이유>"}}
"""

async def evaluate_relevance(
    question: str,
    answer: str,
    llm: LLMClientPort,
) -> dict:
    prompt = RELEVANCE_EVAL_PROMPT.format(
        question=question,
        answer=answer,
    )
    response = await llm.generate(prompt)
    return json.loads(response)
```

### Groundedness 평가

```python
GROUNDEDNESS_EVAL_PROMPT = """
답변의 각 주장이 소스에 근거하는지 평가하세요.

소스:
{source}

답변:
{answer}

각 주장에 대해:
- "supported": 소스에 근거함
- "unsupported": 소스에 없는 내용
- "partially": 부분적으로 근거

JSON 형식:
{{"claims": [{{"text": "<주장>", "status": "<상태>", "source_ref": "<근거 위치>"}}]}}
"""
```

---

## A/B 테스트

### 프롬프트 버전 비교

```python
@dataclass
class PromptVariant:
    name: str
    template: str
    version: str

async def ab_test(
    variants: list[PromptVariant],
    test_cases: list[dict],
    llm: LLMClientPort,
) -> dict:
    """A/B 테스트 실행"""
    results = {v.name: [] for v in variants}

    for case in test_cases:
        for variant in variants:
            prompt = variant.template.format(**case["context"])
            answer = await llm.generate(prompt)

            # 평가
            eval_result = {
                "relevance": await evaluate_relevance(case["question"], answer, llm),
                "length": evaluate_length(answer),
                "coverage": evaluate_coverage(answer, case.get("keywords", [])),
                "consistency": evaluate_character_consistency(answer),
            }

            results[variant.name].append({
                "case_id": case["id"],
                "answer": answer,
                "evaluation": eval_result,
            })

    # 집계
    summary = {}
    for name, variant_results in results.items():
        scores = [r["evaluation"]["relevance"]["score"] for r in variant_results]
        summary[name] = {
            "avg_relevance": sum(scores) / len(scores),
            "sample_count": len(variant_results),
        }

    return {"results": results, "summary": summary}
```

---

## 평가 데이터셋

### 테스트 케이스 구조

```python
TEST_CASES = [
    {
        "id": "waste_001",
        "intent": "waste_query",
        "question": "페트병 어떻게 버려요?",
        "context": {
            "disposal_rules": {...},
            "situation_tags": ["라벨_부착"],
        },
        "keywords": ["투명", "페트", "라벨"],
        "expected_elements": ["배출 장소", "라벨 제거 안내"],
    },
    {
        "id": "general_001",
        "intent": "general",
        "question": "안녕하세요",
        "context": {},
        "keywords": [],
        "expected_elements": ["인사 응대"],
    },
]
```

### 골든 데이터셋

```python
GOLDEN_ANSWERS = {
    "waste_001": {
        "question": "페트병 어떻게 버려요?",
        "golden_answer": "페트병은 **투명 페트병 전용함**에 버려주세요! 🌿\n라벨 떼고, 비우고, 찌그러뜨려서 배출하세요.",
        "score_threshold": 0.8,
    },
}

async def evaluate_against_golden(
    answer: str,
    golden: str,
    llm: LLMClientPort,
) -> float:
    """골든 답변 대비 평가"""
    prompt = f"""
    다음 두 답변의 유사도를 0-1 사이로 평가하세요.

    골든 답변: {golden}
    생성 답변: {answer}

    숫자만 응답하세요.
    """
    score = float(await llm.generate(prompt))
    return score
```

---

## 평가 리포트

```python
def generate_eval_report(results: dict) -> str:
    """평가 리포트 생성"""
    report = []
    report.append("# 프롬프트 평가 리포트\n")

    for variant, data in results["summary"].items():
        report.append(f"## {variant}")
        report.append(f"- 평균 관련성: {data['avg_relevance']:.2f}")
        report.append(f"- 테스트 수: {data['sample_count']}")
        report.append("")

    # 상세 결과
    report.append("## 상세 결과\n")
    for variant, variant_results in results["results"].items():
        report.append(f"### {variant}")
        for r in variant_results[:5]:  # 상위 5개
            report.append(f"- Case {r['case_id']}: {r['evaluation']['relevance']['score']}/5")
        report.append("")

    return "\n".join(report)
```
