# 프롬프트 최적화 기법

## 최적화 전략

```
1. Prompt Compression   → 토큰 절약
2. Few-Shot Selection   → 관련 예시 선택
3. Chain-of-Thought     → 추론 품질 향상
4. Self-Consistency     → 답변 신뢰도 향상
5. Iterative Refinement → 점진적 개선
```

---

## 1. Prompt Compression

### 불필요한 표현 제거

```text
# BEFORE (장황함)
당신은 환경 보호에 관심이 많은 친환경 분리배출 도우미 AI 어시스턴트입니다.
사용자가 분리배출에 대해 질문하면 친절하고 자세하게 답변해주세요.
답변할 때는 항상 정확한 정보를 제공하도록 노력해주세요.

# AFTER (간결함)
당신은 '에코', 친환경 분리배출 도우미입니다.

규칙:
- 정확한 정보만 제공
- 3문장 이내
- 친근한 존댓말
```

### 컨텍스트 요약

```python
def compress_context(context: dict, max_tokens: int = 500) -> dict:
    """컨텍스트 압축"""
    compressed = {}

    # 필수 필드만 유지
    if "disposal_rules" in context:
        rules = context["disposal_rules"]
        compressed["rules"] = {
            "category": rules.get("category"),
            "method": rules.get("data", {}).get("배출방법_공통", [])[:3],
        }

    # 태그는 그대로
    if "situation_tags" in context:
        compressed["tags"] = context["situation_tags"]

    return compressed
```

---

## 2. Few-Shot Selection

### 유사도 기반 예시 선택

```python
from sentence_transformers import SentenceTransformer

class FewShotSelector:
    """동적 Few-Shot 예시 선택"""

    def __init__(self, examples: list[dict]):
        self._examples = examples
        self._model = SentenceTransformer("jhgan/ko-sroberta-multitask")
        self._embeddings = self._model.encode(
            [ex["question"] for ex in examples]
        )

    def select(self, query: str, k: int = 3) -> list[dict]:
        """쿼리와 유사한 예시 k개 선택"""
        query_emb = self._model.encode([query])
        similarities = cosine_similarity(query_emb, self._embeddings)[0]

        # 상위 k개
        top_indices = similarities.argsort()[-k:][::-1]
        return [self._examples[i] for i in top_indices]
```

### 다양성 고려

```python
def select_diverse_examples(
    query: str,
    examples: list[dict],
    k: int = 3,
    diversity_weight: float = 0.3,
) -> list[dict]:
    """유사성 + 다양성 균형"""
    selected = []
    candidates = examples.copy()

    for _ in range(k):
        if not candidates:
            break

        scores = []
        for ex in candidates:
            # 유사성 점수
            similarity = compute_similarity(query, ex["question"])

            # 다양성 점수 (이미 선택된 것과의 거리)
            if selected:
                diversity = min(
                    compute_similarity(ex["question"], s["question"])
                    for s in selected
                )
                diversity = 1 - diversity  # 거리가 멀수록 높은 점수
            else:
                diversity = 1.0

            # 종합 점수
            score = (1 - diversity_weight) * similarity + diversity_weight * diversity
            scores.append(score)

        # 최고 점수 선택
        best_idx = scores.index(max(scores))
        selected.append(candidates.pop(best_idx))

    return selected
```

---

## 3. Chain-of-Thought

### 단계별 추론

```text
## 답변 과정

다음 단계로 생각하세요:

1. **품목 파악**: 사용자가 언급한 폐기물이 무엇인지 확인
2. **분류 확인**: disposal_rules에서 해당 품목의 분류 찾기
3. **방법 추출**: 올바른 배출 방법 추출
4. **팁 추가**: situation_tags가 있으면 관련 팁 추가
5. **답변 작성**: 친근하고 간결하게 작성

각 단계를 순서대로 수행한 후 최종 답변만 출력하세요.
```

### Zero-Shot CoT

```text
이 문제를 단계별로 생각해봅시다.

{question}

단계별로 생각한 후 최종 답변을 제공하세요.
```

---

## 4. Self-Consistency

### 다중 샘플링 후 투표

```python
async def self_consistency(
    prompt: str,
    llm: LLMClientPort,
    n_samples: int = 5,
    temperature: float = 0.7,
) -> str:
    """Self-Consistency로 신뢰도 높은 답변"""
    responses = []

    for _ in range(n_samples):
        response = await llm.generate(prompt, temperature=temperature)
        responses.append(response)

    # 가장 빈번한 답변 (또는 유사도 기반 클러스터링)
    from collections import Counter
    counter = Counter(responses)
    most_common = counter.most_common(1)[0][0]

    return most_common
```

### 신뢰도 점수

```python
def compute_consistency_score(responses: list[str]) -> float:
    """응답 일관성 점수"""
    if len(responses) <= 1:
        return 1.0

    # 페어별 유사도 계산
    similarities = []
    for i, r1 in enumerate(responses):
        for r2 in responses[i+1:]:
            sim = compute_similarity(r1, r2)
            similarities.append(sim)

    return sum(similarities) / len(similarities)
```

---

## 5. Iterative Refinement

### 자기 개선 루프

```python
REFINE_PROMPT = """
다음 답변을 개선하세요.

원래 질문: {question}
현재 답변: {current_answer}
피드백: {feedback}

개선된 답변:
"""

async def iterative_refine(
    question: str,
    initial_answer: str,
    llm: LLMClientPort,
    max_iterations: int = 3,
) -> str:
    """반복적 답변 개선"""
    current = initial_answer

    for i in range(max_iterations):
        # 평가
        eval_result = await evaluate_answer(question, current, llm)

        # 품질 충분하면 종료
        if eval_result["score"] >= 0.9:
            break

        # 피드백 기반 개선
        feedback = eval_result.get("feedback", "더 간결하고 명확하게")
        prompt = REFINE_PROMPT.format(
            question=question,
            current_answer=current,
            feedback=feedback,
        )
        current = await llm.generate(prompt)

    return current
```

---

## 최적화 파이프라인

```python
class PromptOptimizer:
    """프롬프트 최적화 파이프라인"""

    def __init__(
        self,
        base_template: str,
        examples: list[dict],
        llm: LLMClientPort,
    ):
        self._template = base_template
        self._selector = FewShotSelector(examples)
        self._llm = llm

    async def optimize(
        self,
        query: str,
        context: dict,
        use_cot: bool = True,
        use_consistency: bool = False,
    ) -> str:
        """최적화된 프롬프트로 답변 생성"""

        # 1. 컨텍스트 압축
        compressed_ctx = compress_context(context)

        # 2. Few-Shot 선택
        examples = self._selector.select(query, k=3)

        # 3. 프롬프트 구성
        prompt = self._build_prompt(query, compressed_ctx, examples, use_cot)

        # 4. 답변 생성
        if use_consistency:
            answer = await self_consistency(prompt, self._llm, n_samples=3)
        else:
            answer = await self._llm.generate(prompt)

        return answer

    def _build_prompt(
        self,
        query: str,
        context: dict,
        examples: list[dict],
        use_cot: bool,
    ) -> str:
        """프롬프트 구성"""
        parts = [self._template]

        # 컨텍스트
        parts.append(f"## 컨텍스트\n{json.dumps(context, ensure_ascii=False)}")

        # Few-Shot
        if examples:
            ex_str = "\n\n".join(f"Q: {e['question']}\nA: {e['answer']}" for e in examples)
            parts.append(f"## 예시\n{ex_str}")

        # CoT
        if use_cot:
            parts.append("단계별로 생각한 후 최종 답변을 제공하세요.")

        # 질문
        parts.append(f"## 질문\n{query}")

        return "\n\n".join(parts)
```
