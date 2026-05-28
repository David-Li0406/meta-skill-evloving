---
name: research
description: |
  DuckDuckGo 기반 빠른 웹 검색 스킬.
  특정 사실 확인, 최신 뉴스 조회, 간단한 정보 수집에 사용.
  
  사용 시점:
  (1) 특정 사실을 빠르게 확인해야 할 때
  (2) 최신 뉴스나 이벤트를 조회할 때
  (3) 심층 분석 전 초기 정보 수집 시
  (4) 슬래시 커맨드 /quick-search 실행 시
---

# Research Skill (Quick Search)

DuckDuckGo 기반 빠른 웹 검색. API 키 불필요.

## 디렉토리 구조

```
research/
├── SKILL.md           # 이 문서
└── scripts/
    ├── load_env.sh    # 환경 변수 로더
    ├── run.py         # 메인 실행 스크립트
    └── test_search.py # 테스트 코드
```

## 빠른 시작

```bash
# 스킬 디렉토리로 이동
cd ~/.config/opencode/skill/research

# 테스트 실행
python scripts/test_search.py

# 검색 실행
python scripts/run.py "Python best practices"
```

## 사용법

### CLI

```bash
# 슬래시 커맨드
/quick-search "검색어"

# 스킬 스크립트 직접 실행
python ~/.config/opencode/skill/research/scripts/run.py "검색어" [max_results]
```

### Python API

```python
from scripts.run import search

results = search("machine learning trends", max_results=5)
for r in results:
    print(f"{r['title']}: {r['url']}")
```

## 출력 형식

```
🔍 Searching for: Python frameworks
Title: Top Python Web Frameworks in 2026
URL: https://example.com/article/...
Snippet: Django, FastAPI, and Flask continue to dominate...
----------------------------------------
```

## 의존성

```
duckduckgo-search>=3.0.0
```

## 관련 스킬

- **deep-research**: 심층 분석이 필요한 경우
- **memory**: 검색 결과 장기 저장 시
