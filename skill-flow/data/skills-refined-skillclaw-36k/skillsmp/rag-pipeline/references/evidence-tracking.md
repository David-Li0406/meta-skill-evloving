# Evidence 추적 가이드

## Evidence 구조

RAG 결과의 출처와 신뢰도를 추적하는 메타데이터.

```python
@dataclass
class Evidence:
    """RAG Evidence"""
    chunk_id: str           # 소스 문서 ID (예: "재활용폐기물_플라스틱류")
    relevance: str          # "high" | "medium" | "low"
    quoted_text: str        # 인용 텍스트 (80자 제한)
    matched_tags: list[str] # 매칭된 상황 태그
    method: str             # "classification" | "contextual" | "keyword"
```

---

## SearchRAGOutput

```python
@dataclass
class SearchRAGOutput:
    """RAG 검색 결과"""
    found: bool
    disposal_rules: dict | None
    search_method: str
    matched_keyword: str | None
    events: list[str]       # 감사 로그
    evidence: list[Evidence] # Phase 1-4용 Evidence
```

---

## Evidence 생성 흐름

### 1. Classification 기반 (Vision 결과)

```python
async def _search_by_classification(
    self,
    input: SearchRAGInput,
) -> SearchRAGOutput:
    """Vision 분류 결과로 검색"""
    classification = input.classification_result

    result = await self.retriever.search(
        category=classification["major_category"],
        subcategory=classification.get("minor_category"),
    )

    if not result:
        return SearchRAGOutput(found=False, ...)

    evidence = Evidence(
        chunk_id=result["key"],
        relevance="high",  # Classification은 높은 신뢰도
        quoted_text=self._extract_quote(result["data"]),
        matched_tags=[],
        method="classification",
    )

    return SearchRAGOutput(
        found=True,
        disposal_rules=result,
        search_method="classification",
        evidence=[evidence],
        events=["classification_search_success"],
    )
```

### 2. Contextual 기반 (태그 매칭)

```python
async def _search_contextual(
    self,
    input: SearchRAGInput,
) -> SearchRAGOutput:
    """Contextual (태그 기반) 검색"""
    results = await self.retriever.search_with_context(
        message=input.message,
        limit=3,
    )

    if not results:
        return SearchRAGOutput(found=False, ...)

    # 최고 Relevance 결과 선택
    best = results[0]

    # Evidence 리스트 생성
    evidence_list = [
        Evidence(
            chunk_id=r.chunk_id,
            relevance=r.relevance,
            quoted_text=r.quoted_text,
            matched_tags=r.matched_tags,
            method="contextual",
        )
        for r in results
    ]

    return SearchRAGOutput(
        found=True,
        disposal_rules=await self._get_full_data(best.chunk_id),
        search_method="contextual",
        evidence=evidence_list,
        events=["contextual_search_success"],
    )
```

### 3. Keyword 폴백

```python
async def _search_keyword(
    self,
    input: SearchRAGInput,
) -> SearchRAGOutput:
    """키워드 폴백 검색"""
    # 폐기물 관련 키워드 추출
    keywords = self._extract_waste_keywords(input.message)

    for keyword in keywords:
        result = await self.retriever.search_by_keyword(keyword)

        if result:
            evidence = Evidence(
                chunk_id=result["key"],
                relevance="low",  # Keyword는 낮은 신뢰도
                quoted_text=self._extract_quote(result["data"]),
                matched_tags=[],
                method="keyword",
            )

            return SearchRAGOutput(
                found=True,
                disposal_rules=result,
                search_method="keyword",
                matched_keyword=keyword,
                evidence=[evidence],
                events=[f"keyword_search_success:{keyword}"],
            )

    return SearchRAGOutput(
        found=False,
        search_method="none",
        evidence=[],
        events=["all_search_strategies_failed"],
    )
```

---

## Evidence 활용

### Answer Generation에서 Citation

```python
def build_answer_context(
    disposal_rules: dict,
    evidence: list[Evidence],
) -> str:
    """답변 생성용 컨텍스트 구성"""
    context_parts = []

    # 규정 데이터
    context_parts.append(f"## 분리배출 규정\n{json.dumps(disposal_rules, ensure_ascii=False)}")

    # Evidence Citation
    if evidence:
        citations = []
        for e in evidence:
            citations.append(f"- [{e.chunk_id}] (신뢰도: {e.relevance}): {e.quoted_text}")
        context_parts.append(f"## 참조 출처\n" + "\n".join(citations))

    # 상황 태그 안내
    all_tags = set()
    for e in evidence:
        all_tags.update(e.matched_tags)

    if all_tags:
        tips = []
        for tag in all_tags:
            instruction = get_instruction_for_tag(tag)
            if instruction:
                tips.append(f"- {tag}: {instruction}")
        context_parts.append(f"## 상황별 팁\n" + "\n".join(tips))

    return "\n\n".join(context_parts)
```

### Phase 1 평가에서 Citation 추적

```python
async def evaluate_citation(
    query: str,
    answer: str,
    evidence: list[Evidence],
) -> dict:
    """Phase 1: Citation 평가"""
    cited_chunks = []
    context_relevance = 0.0

    for e in evidence:
        # 답변에서 Evidence 내용 참조 확인
        if any(keyword in answer for keyword in e.quoted_text.split()):
            cited_chunks.append(e.chunk_id)

    # Relevance 점수 계산
    if cited_chunks:
        relevance_scores = {
            "high": 1.0,
            "medium": 0.7,
            "low": 0.4,
        }
        scores = [
            relevance_scores[e.relevance]
            for e in evidence
            if e.chunk_id in cited_chunks
        ]
        context_relevance = sum(scores) / len(scores)

    return {
        "cited_chunks": cited_chunks,
        "context_relevance": context_relevance,
    }
```

---

## Audit Trail (events)

```python
# Evidence와 함께 검색 이벤트 로깅
events = [
    "classification_search_started",
    "classification_search_success",
    "contextual_search_skipped",  # Classification 성공 시 스킵
]

# 실패 시
events = [
    "classification_search_started",
    "classification_search_no_result",
    "contextual_search_started",
    "contextual_search_success",
]
```

---

## 데이터 구조 예시

```json
{
  "found": true,
  "disposal_rules": {
    "key": "재활용폐기물_플라스틱류",
    "category": "재활용",
    "data": {
      "배출방법_공통": ["라벨 제거", "내용물 비우기", "헹구기"],
      "대상_설명": "플라스틱 용기 및 포장재"
    }
  },
  "search_method": "contextual",
  "evidence": [
    {
      "chunk_id": "재활용폐기물_플라스틱류",
      "relevance": "high",
      "quoted_text": "플라스틱 용기는 라벨을 제거하고 내용물을 비운 후...",
      "matched_tags": ["라벨_부착", "내용물_있음"],
      "method": "contextual"
    }
  ],
  "events": [
    "classification_search_no_result",
    "contextual_search_started",
    "contextual_search_success"
  ]
}
```
