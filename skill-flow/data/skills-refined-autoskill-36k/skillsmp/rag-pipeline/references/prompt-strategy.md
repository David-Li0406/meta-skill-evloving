# 프롬프트 전략 가이드

## Local Prompt Optimization (arxiv:2504.20355)

Global (고정) + Local (의도별) 프롬프트 조합.

```
FINAL_PROMPT = GLOBAL + LOCAL[intent]

GLOBAL: 캐릭터 정의, 톤, 공통 규칙
LOCAL:  의도별 최적화된 지침
```

---

## 프롬프트 구조

```
infrastructure/assets/prompts/
├── global/
│   └── eco_character.txt      # 캐릭터 정의 (모든 의도 공통)
└── local/
    ├── waste_instruction.txt  # 분리배출 질문용
    ├── character_instruction.txt
    ├── location_instruction.txt
    ├── web_instruction.txt
    └── general_instruction.txt
```

---

## Global Prompt (eco_character.txt)

```text
당신은 '에코'라는 이름의 친환경 분리배출 도우미입니다.

## 캐릭터 특성
- 밝고 친근한 말투 (존댓말 사용)
- 환경 보호에 열정적
- 칭찬과 격려를 잘 함
- 이모지 적절히 사용 (과하지 않게)

## 공통 규칙
1. 항상 정확한 정보만 제공하세요
2. 확실하지 않으면 "정확한 정보는 관할 지자체에 문의해주세요"라고 안내
3. 사용자의 노력을 격려해주세요
4. 짧고 명확하게 답변하세요 (3문장 이내 권장)
```

---

## Local Prompt: waste_instruction.txt

```text
## 분리배출 답변 지침

### 컨텍스트 활용
당신에게 제공되는 컨텍스트:
- `disposal_rules`: 분리배출 규정 데이터
- `classification`: Vision 분류 결과 (있는 경우)
- `situation_tags`: 매칭된 상황 태그

### 답변 구조
1. **핵심 답변** (1-2문장): 무엇을 어디에 버리는지
2. **구체적 방법** (필요시): 단계별 설명
3. **상황별 팁** (태그 있을 때):
   - 라벨_부착 → "라벨을 떼면 더 좋아요!"
   - 내용물_있음 → "내용물을 비워주세요!"
   - 뚜껑_있음 → "뚜껑은 따로 분리해주세요!"
   - 오염됨 → "헹궈서 배출하면 완벽해요!"

### 예시
Q: 페트병 어떻게 버려요?
A: 페트병은 **투명 페트병 전용 분리수거함**에 버려주세요! 🌿

라벨을 떼고, 내용물을 비운 후 찌그러뜨려서 배출하시면 됩니다.
뚜껑은 플라스틱류에 따로 분리해주세요!

환경을 생각하는 멋진 실천이에요! ♻️
```

---

## Local Prompt: general_instruction.txt

```text
## 일반 대화 지침

### 대화 유형 처리
1. **인사/감사**: 따뜻하게 응대, 환경 관련 한마디 추가
2. **잡담**: 자연스럽게 환경 주제로 연결 (강요 X)
3. **환경 상식**: 친근하게 설명

### 자연스러운 연결 예시
- "오늘 날씨 좋네요" → "맑은 날씨만큼 맑은 지구를 위해 오늘도 분리배출!"
- "심심해요" → "심심할 때 우리 집 분리배출 상태 점검해보는 건 어때요?"

### 주의사항
- 환경 주제로 억지 연결하지 않기
- 사용자가 원하지 않으면 일반 대화도 OK
- 자연스러운 마무리 권장
```

---

## PromptBuilder 구현

```python
from functools import lru_cache
from pathlib import Path

class PromptBuilder:
    """Global + Local 프롬프트 빌더"""

    def __init__(self, prompts_path: str = "infrastructure/assets/prompts"):
        self._base_path = Path(prompts_path)
        self._intent_map = {
            "waste_query": "waste_instruction.txt",
            "character": "character_instruction.txt",
            "location": "location_instruction.txt",
            "web_search": "web_instruction.txt",
            "general": "general_instruction.txt",
        }

    @lru_cache(maxsize=10)
    def _load_file(self, filename: str) -> str:
        """프롬프트 파일 로드 (캐싱)"""
        path = self._base_path / filename
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""

    def build(self, intent: str) -> str:
        """단일 의도 프롬프트 생성"""
        # Global
        global_prompt = self._load_file("global/eco_character.txt")

        # Local
        local_file = self._intent_map.get(intent, "general_instruction.txt")
        local_prompt = self._load_file(f"local/{local_file}")

        return f"{global_prompt}\n\n{local_prompt}"

    def build_multi(self, intents: list[str]) -> str:
        """복합 의도 프롬프트 생성 (DialogUSR 패턴)"""
        # Global
        global_prompt = self._load_file("global/eco_character.txt")

        # Multiple Local (정책 조합)
        local_parts = []
        for intent in intents:
            local_file = self._intent_map.get(intent)
            if local_file:
                content = self._load_file(f"local/{local_file}")
                local_parts.append(f"### {intent} 지침\n{content}")

        combined_local = "\n\n".join(local_parts)

        return f"{global_prompt}\n\n## 복합 의도 처리\n{combined_local}"
```

---

## AnswerContext 통합

```python
@dataclass
class AnswerContext:
    """답변 생성용 컨텍스트"""
    classification: dict | None      # Vision 결과
    disposal_rules: dict | None      # RAG 결과
    character_context: dict | None   # 캐릭터 Subagent
    location_context: dict | None    # 위치 Subagent
    web_search_results: str | None   # 웹 검색
    user_input: str

    def to_prompt_context(self) -> str:
        """LLM용 컨텍스트 포맷"""
        parts = []

        if self.classification:
            parts.append(f"## 이미지 분류 결과\n```json\n{json.dumps(self.classification, ensure_ascii=False, indent=2)}\n```")

        if self.disposal_rules:
            parts.append(f"## 분리배출 규정\n```json\n{json.dumps(self.disposal_rules, ensure_ascii=False, indent=2)}\n```")

        if self.character_context:
            parts.append(f"## 캐릭터 정보\n```json\n{json.dumps(self.character_context, ensure_ascii=False, indent=2)}\n```")

        if self.location_context:
            parts.append(f"## 위치 정보\n```json\n{json.dumps(self.location_context, ensure_ascii=False, indent=2)}\n```")

        if self.web_search_results:
            parts.append(f"## 웹 검색 결과\n{self.web_search_results}")

        parts.append(f"## 사용자 질문\n{self.user_input}")

        return "\n\n".join(parts)
```

---

## 최종 프롬프트 구성

```python
async def generate_answer(
    intent: str,
    context: AnswerContext,
    llm: LLMClientPort,
    prompt_builder: PromptBuilder,
) -> str:
    """답변 생성"""
    # 1. 시스템 프롬프트 (Global + Local)
    system_prompt = prompt_builder.build(intent)

    # 2. 사용자 컨텍스트
    user_context = context.to_prompt_context()

    # 3. LLM 호출
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_context},
    ]

    return await llm.generate(messages)
```
