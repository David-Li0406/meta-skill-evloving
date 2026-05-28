# Retriever 구현 가이드

## Retriever 계층

```
RetrieverPort (Abstract)
├── LocalAssetRetriever (기본)
│   └─ JSON 파일 기반 검색
└── TagBasedRetriever (Contextual)
    └─ 품목/상황 태그 기반 검색
```

---

## LocalAssetRetriever

```python
# infrastructure/retrieval/local_asset_retriever.py
from apps.chat_worker.application.ports.retrieval.retriever import RetrieverPort

class LocalAssetRetriever(RetrieverPort):
    """JSON 파일 기반 기본 Retriever"""

    def __init__(self, asset_path: str = "assets/data/source"):
        self._asset_path = Path(asset_path)
        self._data: dict[str, dict] = {}
        self._loaded = False

        # 카테고리 약어 매핑
        self._abbreviations = {
            "재활용": "재활용폐기물",
            "음식물": "음식물류폐기물",
            "일반": "일반종량제폐기물",
            "대형": "대형폐기물",
            "유해": "생활계유해폐기물",
        }

    async def _ensure_loaded(self) -> None:
        """Lazy 로딩"""
        if self._loaded:
            return

        for json_file in self._asset_path.glob("*.json"):
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                key = json_file.stem  # 파일명 (확장자 제외)
                self._data[key] = data

        self._loaded = True

    async def search(
        self,
        category: str,
        subcategory: str | None = None,
        limit: int = 3,
    ) -> dict | None:
        """카테고리 기반 검색"""
        await self._ensure_loaded()

        # 약어 확장
        full_category = self._abbreviations.get(category, category)

        # 키 구성: {카테고리}_{서브카테고리}
        if subcategory:
            key = f"{full_category}_{subcategory}"
        else:
            key = full_category

        # 정확 매칭
        if key in self._data:
            return {"key": key, "category": category, "data": self._data[key]}

        # 부분 매칭 (서브카테고리 없이)
        for data_key in self._data:
            if data_key.startswith(full_category):
                return {"key": data_key, "category": category, "data": self._data[data_key]}

        return None

    async def search_by_keyword(
        self,
        keyword: str,
        limit: int = 3,
    ) -> dict | None:
        """키워드 기반 폴백 검색"""
        await self._ensure_loaded()

        keyword_lower = keyword.lower()

        for key, data in self._data.items():
            # 키에서 매칭
            if keyword_lower in key.lower():
                return {"key": key, "category": key.split("_")[0], "data": data}

            # 데이터 내용에서 매칭
            content = json.dumps(data, ensure_ascii=False).lower()
            if keyword_lower in content:
                return {"key": key, "category": key.split("_")[0], "data": data}

        return None

    async def get_all_categories(self) -> list[str]:
        """사용 가능한 카테고리 목록"""
        await self._ensure_loaded()
        return list(self._data.keys())
```

---

## TagBasedRetriever (Anthropic Contextual Pattern)

```python
# infrastructure/retrieval/tag_based_retriever.py
from dataclasses import dataclass
import yaml

@dataclass
class ContextualSearchResult:
    """Contextual 검색 결과"""
    chunk_id: str
    category: str
    quoted_text: str
    relevance: str  # "high" | "medium" | "low"
    matched_tags: list[str]

class TagBasedRetriever(LocalAssetRetriever):
    """태그 기반 Contextual Retriever (Anthropic Pattern)"""

    def __init__(
        self,
        asset_path: str = "assets/data/source",
        item_list_path: str = "assets/data/item_class_list.yaml",
        tags_path: str = "assets/data/situation_tags.yaml",
    ):
        super().__init__(asset_path)
        self._item_index: dict[str, tuple[str, str]] = {}  # item → (major, minor)
        self._situation_tags: dict[str, str] = {}  # tag → instruction

        self._load_item_list(item_list_path)
        self._load_situation_tags(tags_path)

    def _load_item_list(self, path: str) -> None:
        """품목 분류 인덱스 로드"""
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        for major, minors in data.items():
            for minor, items in minors.items():
                for item in items:
                    self._item_index[item] = (major, minor)

    def _load_situation_tags(self, path: str) -> None:
        """상황 태그 로드"""
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # tag → instruction 매핑
        for tag_info in data:
            self._situation_tags[tag_info["tag"]] = tag_info["instruction"]

    def extract_context(self, message: str) -> dict:
        """메시지에서 품목/상황 태그 추출"""
        matched_items = []
        matched_tags = []

        # 품목 매칭
        for item, (major, minor) in self._item_index.items():
            if item in message:
                matched_items.append({
                    "item": item,
                    "major_category": major,
                    "minor_category": minor,
                })

        # 상황 태그 매칭
        for tag in self._situation_tags:
            if tag in message:
                matched_tags.append(tag)

        return {
            "items": matched_items,
            "situation_tags": matched_tags,
        }

    async def search_with_context(
        self,
        message: str,
        limit: int = 3,
    ) -> list[ContextualSearchResult]:
        """Contextual 검색"""
        context = self.extract_context(message)
        results = []

        # 매칭된 품목으로 검색
        for item_info in context["items"]:
            search_result = await self.search(
                category=item_info["major_category"],
                subcategory=item_info["minor_category"],
            )

            if search_result:
                # 관련 텍스트 추출 (80자)
                quoted = self._extract_quote(search_result["data"], 80)

                results.append(ContextualSearchResult(
                    chunk_id=search_result["key"],
                    category=item_info["major_category"],
                    quoted_text=quoted,
                    relevance="high",
                    matched_tags=context["situation_tags"],
                ))

        # Relevance 점수 기반 정렬 & 제한
        return sorted(
            results,
            key=lambda r: {"high": 0, "medium": 1, "low": 2}[r.relevance],
        )[:limit]

    def _extract_quote(self, data: dict, max_len: int = 80) -> str:
        """데이터에서 대표 인용문 추출"""
        if "배출방법_공통" in data and data["배출방법_공통"]:
            text = data["배출방법_공통"][0]
        elif "대상_설명" in data:
            text = data["대상_설명"]
        else:
            text = json.dumps(data, ensure_ascii=False)

        return text[:max_len] + "..." if len(text) > max_len else text

    def get_instruction_for_tag(self, tag: str) -> str | None:
        """상황 태그에 대한 안내 문구"""
        return self._situation_tags.get(tag)
```

---

## 상황 태그 예시

```yaml
# situation_tags.yaml
- tag: "라벨_부착"
  instruction: "라벨을 떼면 더 좋아요!"
  keywords: ["라벨", "스티커", "비닐 라벨"]

- tag: "내용물_있음"
  instruction: "내용물을 비워주세요!"
  keywords: ["내용물", "남은", "덜 먹은"]

- tag: "뚜껑_있음"
  instruction: "뚜껑은 따로 분리해주세요!"
  keywords: ["뚜껑", "캡", "마개"]

- tag: "오염됨"
  instruction: "헹궈서 배출하면 완벽해요!"
  keywords: ["오염", "더러운", "묻은"]
```

---

## Port 정의

```python
# application/ports/retrieval/retriever.py
from abc import ABC, abstractmethod

class RetrieverPort(ABC):
    """Retriever 추상 인터페이스"""

    @abstractmethod
    async def search(
        self,
        category: str,
        subcategory: str | None = None,
        limit: int = 3,
    ) -> dict | None:
        """카테고리 기반 검색"""
        ...

    @abstractmethod
    async def search_by_keyword(
        self,
        keyword: str,
        limit: int = 3,
    ) -> dict | None:
        """키워드 폴백 검색"""
        ...

    async def search_with_context(
        self,
        message: str,
        limit: int = 3,
    ) -> list:
        """Contextual 검색 (Optional)"""
        return []
```
