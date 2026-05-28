---
name: rag-pipeline
description: RAG (Retrieval-Augmented Generation) 파이프라인 구현 가이드. Contextual Retrieval, Evidence Tracking, Phase 1-4 평가 시 참조. "rag", "retrieval", "retriever", "evidence", "citation", "nugget" 키워드로 트리거.
---

# RAG Pipeline Guide

## Eco² RAG 아키텍처

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    RAG Pipeline (Anthropic Pattern)                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  User Query                                                              │
│      │                                                                   │
│      ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Strategy Selection                                              │    │
│  │  1. Classification (Vision 결과 활용)                            │    │
│  │  2. Contextual (태그 기반 매칭)                                  │    │
│  │  3. Keyword (폴백)                                               │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│      │                                                                   │
│      ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Retriever                                                       │    │
│  │  ├─ LocalAssetRetriever (기본)                                   │    │
│  │  └─ TagBasedRetriever (Contextual)                               │    │
│  │      ├─ item_class_list.yaml (~200 품목)                         │    │
│  │      └─ situation_tags.yaml (~100 태그)                          │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│      │                                                                   │
│      ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Evidence & Answer Generation                                    │    │
│  │  ├─ Evidence: chunk_id, quoted_text, relevance, matched_tags    │    │
│  │  └─ Answer: Global + Local[intent] 프롬프트                      │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│      │                                                                   │
│      ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Phase 1-4 Evaluation (Optional)                                 │    │
│  │  ├─ Phase 1: Citation (chunk 참조 추적)                          │    │
│  │  ├─ Phase 2: Nugget Completeness (정보 완전성)                   │    │
│  │  ├─ Phase 3: Groundedness (근거 기반 검증)                       │    │
│  │  └─ Phase 4: Next Steps (후속 액션 제안)                         │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 검색 전략 우선순위

| 순위 | 전략 | 트리거 | 신호 강도 |
|------|------|--------|-----------|
| 1 | Classification | Vision 결과 존재 | 높음 |
| 2 | Contextual | 품목/상황 태그 매칭 | 중간 |
| 3 | Keyword | 폐기물 키워드 포함 | 낮음 |

## Reference Files

- **Retriever 구현**: See [retriever-implementation.md](./references/retriever-implementation.md)
- **Evidence 추적**: See [evidence-tracking.md](./references/evidence-tracking.md)
- **Phase 1-4 평가**: See [evaluation-phases.md](./references/evaluation-phases.md)
- **프롬프트 전략**: See [prompt-strategy.md](./references/prompt-strategy.md)

## Quick Start

### 1. SearchRAGCommand (전략 선택)

```python
@dataclass
class SearchRAGCommand:
    """RAG 검색 커맨드"""

    retriever: RetrieverPort

    async def execute(self, input: SearchRAGInput) -> SearchRAGOutput:
        # Strategy 1: Classification 기반
        if input.classification_result:
            result = await self._search_by_classification(input)
            if result.found:
                return result

        # Strategy 2: Contextual 기반
        result = await self._search_contextual(input)
        if result.found:
            return result

        # Strategy 3: Keyword 폴백
        return await self._search_keyword(input)
```

### 2. TagBasedRetriever (Contextual)

```python
class TagBasedRetriever(RetrieverPort):
    """태그 기반 Contextual Retriever"""

    async def search_with_context(
        self,
        message: str,
    ) -> list[ContextualSearchResult]:
        # 1. 품목/상황 태그 추출
        context = self.extract_context(message)

        # 2. 태그 기반 검색
        results = await self._search_by_tags(context)

        # 3. Relevance 점수 계산
        return self._rank_results(results)
```

### 3. Evidence 구조

```python
@dataclass
class Evidence:
    """RAG Evidence (Phase 1-4용)"""
    chunk_id: str           # 소스 식별자
    relevance: str          # "high" | "medium" | "low"
    quoted_text: str        # 인용 텍스트 (80자)
    matched_tags: list[str] # 매칭된 태그
    method: str             # 검색 방법
```

### 4. Phase 1-4 평가

```python
@dataclass
class FeedbackResult:
    """Phase 1-4 평가 결과"""
    # Phase 1: Citation
    context_relevance: float
    cited_chunks: list[str]

    # Phase 2: Nugget Completeness
    completeness: float
    covered_nuggets: list[str]
    missing_nuggets: list[str]

    # Phase 3: Groundedness
    groundedness: float
    unsupported_claims: list[str]

    # Phase 4: Next Steps
    suggested_queries: list[str]
    action_items: list[str]
```
