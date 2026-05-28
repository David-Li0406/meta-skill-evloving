# Phase 1-4 평가 가이드

## 개요

RAG 품질을 4단계로 평가하는 프레임워크.

```
Phase 1: Citation       → 출처 추적 (chunk 참조)
Phase 2: Completeness   → 정보 완전성 (nugget 커버리지)
Phase 3: Groundedness   → 근거 검증 (hallucination 탐지)
Phase 4: Next Steps     → 후속 액션 (Just-in-Time Context)
```

---

## Phase 1: Citation (출처 추적)

답변이 어떤 소스 chunk를 참조했는지 추적.

```python
@dataclass
class Phase1Result:
    """Citation 평가 결과"""
    context_relevance: float  # 0.0 ~ 1.0
    cited_chunks: list[str]   # 참조된 chunk ID 목록
    uncited_chunks: list[str] # 미참조 chunk 목록

async def evaluate_phase1(
    answer: str,
    evidence: list[Evidence],
) -> Phase1Result:
    """Phase 1: Citation 평가"""
    cited = []
    uncited = []

    for e in evidence:
        # 답변에서 Evidence 내용 참조 확인
        keywords = e.quoted_text.split()[:5]  # 처음 5단어
        if any(kw in answer for kw in keywords):
            cited.append(e.chunk_id)
        else:
            uncited.append(e.chunk_id)

    # Relevance 점수 계산
    relevance = len(cited) / len(evidence) if evidence else 0.0

    return Phase1Result(
        context_relevance=relevance,
        cited_chunks=cited,
        uncited_chunks=uncited,
    )
```

---

## Phase 2: Nugget Completeness (정보 완전성)

필수 정보(nugget)가 모두 포함되었는지 검증.

```python
@dataclass
class Phase2Result:
    """Completeness 평가 결과"""
    completeness: float       # 0.0 ~ 1.0
    covered_nuggets: list[str]
    missing_nuggets: list[str]

# 폐기물 분리배출 필수 nugget
WASTE_NUGGETS = [
    "배출 방법",      # HOW: 어떻게 배출하는지
    "배출 장소",      # WHERE: 어디에 배출하는지
    "주의 사항",      # CAUTION: 주의할 점
    "분리 여부",      # SEPARATE: 분리해야 하는 부분
]

async def evaluate_phase2(
    query: str,
    answer: str,
) -> Phase2Result:
    """Phase 2: Nugget Completeness 평가"""
    covered = []
    missing = []

    # 각 nugget 존재 여부 확인
    nugget_keywords = {
        "배출 방법": ["방법", "하세요", "해주세요", "버리세요"],
        "배출 장소": ["분리수거함", "배출함", "수거함", "종량제"],
        "주의 사항": ["주의", "안됩니다", "금지", "조심"],
        "분리 여부": ["분리", "따로", "별도", "제거"],
    }

    for nugget, keywords in nugget_keywords.items():
        if any(kw in answer for kw in keywords):
            covered.append(nugget)
        else:
            missing.append(nugget)

    completeness = len(covered) / len(WASTE_NUGGETS)

    return Phase2Result(
        completeness=completeness,
        covered_nuggets=covered,
        missing_nuggets=missing,
    )
```

---

## Phase 3: Groundedness (근거 검증)

답변의 모든 주장이 소스에 근거하는지 검증.

```python
@dataclass
class Phase3Result:
    """Groundedness 평가 결과"""
    groundedness: float       # 0.0 ~ 1.0
    supported_claims: list[str]
    unsupported_claims: list[str]

async def evaluate_phase3(
    answer: str,
    evidence: list[Evidence],
    llm: LLMClientPort,
) -> Phase3Result:
    """Phase 3: Groundedness 평가 (LLM 기반)"""

    # 답변에서 주장(claim) 추출
    claims = await extract_claims(answer, llm)

    # 각 주장이 Evidence에 근거하는지 확인
    source_text = "\n".join(e.quoted_text for e in evidence)

    supported = []
    unsupported = []

    for claim in claims:
        is_supported = await verify_claim(claim, source_text, llm)
        if is_supported:
            supported.append(claim)
        else:
            unsupported.append(claim)

    groundedness = len(supported) / len(claims) if claims else 1.0

    return Phase3Result(
        groundedness=groundedness,
        supported_claims=supported,
        unsupported_claims=unsupported,
    )

async def extract_claims(answer: str, llm: LLMClientPort) -> list[str]:
    """답변에서 사실적 주장 추출"""
    prompt = f"""
    다음 답변에서 사실적 주장(claim)을 추출하세요.
    - 의견이나 조언이 아닌 사실 진술만 추출
    - 각 주장은 한 문장으로

    답변: {answer}

    주장 목록:
    """
    response = await llm.generate(prompt)
    return response.strip().split("\n")
```

---

## Phase 4: Next Steps (후속 액션)

사용자가 다음에 필요할 정보나 액션 제안.

```python
@dataclass
class Phase4Result:
    """Next Steps 평가 결과"""
    suggested_queries: list[str]  # 후속 질문 제안
    action_items: list[str]       # 실행 가능한 액션
    urgency: str                  # "high" | "medium" | "low"

async def evaluate_phase4(
    query: str,
    answer: str,
    evidence: list[Evidence],
) -> Phase4Result:
    """Phase 4: Next Steps 제안"""
    suggestions = []
    actions = []

    # 상황 태그 기반 후속 액션
    all_tags = set()
    for e in evidence:
        all_tags.update(e.matched_tags)

    if "라벨_부착" in all_tags:
        actions.append("라벨 제거 방법 확인하기")

    if "오염됨" in all_tags:
        actions.append("올바른 세척 방법 확인하기")

    # 정보 부족 시 후속 질문 제안
    if "위치" not in answer.lower():
        suggestions.append("가까운 분리수거함 위치가 궁금하시면 물어봐주세요!")

    if "대형" in query and "신청" not in answer:
        suggestions.append("대형폐기물 수거 신청 방법도 알려드릴까요?")

    # Urgency 판단
    urgency = "low"
    if "유해" in query or "위험" in query:
        urgency = "high"
    elif any(tag in all_tags for tag in ["오염됨", "내용물_있음"]):
        urgency = "medium"

    return Phase4Result(
        suggested_queries=suggestions,
        action_items=actions,
        urgency=urgency,
    )
```

---

## 통합 평가

```python
@dataclass
class FeedbackResult:
    """Phase 1-4 통합 평가 결과"""
    phase1: Phase1Result
    phase2: Phase2Result
    phase3: Phase3Result
    phase4: Phase4Result

    @property
    def overall_score(self) -> float:
        """전체 품질 점수"""
        return (
            self.phase1.context_relevance * 0.2 +
            self.phase2.completeness * 0.3 +
            self.phase3.groundedness * 0.4 +
            0.1  # Phase 4는 점수 아님
        )

    @property
    def needs_improvement(self) -> bool:
        """개선 필요 여부"""
        return self.overall_score < 0.7

async def evaluate_all_phases(
    query: str,
    answer: str,
    evidence: list[Evidence],
    llm: LLMClientPort,
) -> FeedbackResult:
    """전체 Phase 평가"""
    phase1 = await evaluate_phase1(answer, evidence)
    phase2 = await evaluate_phase2(query, answer)
    phase3 = await evaluate_phase3(answer, evidence, llm)
    phase4 = await evaluate_phase4(query, answer, evidence)

    return FeedbackResult(
        phase1=phase1,
        phase2=phase2,
        phase3=phase3,
        phase4=phase4,
    )
```

---

## Rule-Based vs LLM-Based

| Phase | Rule-Based | LLM-Based |
|-------|------------|-----------|
| Phase 1 | 키워드 매칭 | - |
| Phase 2 | Nugget 키워드 | LLM 추출 |
| Phase 3 | 불가능 | Claim 검증 |
| Phase 4 | 태그 기반 | LLM 제안 |

**전략**: Phase 1, 2는 Rule-Based (빠름/무료), Phase 3은 LLM 필요 시에만.
