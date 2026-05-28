---
name: search
description: 단순 검색 - Haiku 모델로 빠르고 저렴하게
---

# /search 스킬

단순 검색 요청 시 Haiku 모델을 사용하여 빠르고 저렴하게 처리합니다.

## 사용법

```
/search [검색어 또는 질문]
```

## 예시

```
/search translateKoToEn 함수 위치
/search package.json 파일들
/search TODO 주석
/search useEffect 사용처
```

## 실행 규칙

1. Task tool 호출
2. `subagent_type: "Explore"` 지정
3. `model: "haiku"` 지정
4. `thoroughness: "quick"`

## 프롬프트 템플릿

```
검색 요청: {user_query}

빠르게 검색하여 결과를 반환하세요:
- 파일 경로
- 라인 번호 (가능한 경우)
- 간단한 컨텍스트

상세 분석은 하지 마세요. 위치만 찾으면 됩니다.
```

## 적합한 작업

- 특정 함수/클래스 위치 찾기
- 파일 패턴 검색
- 간단한 grep 작업
- 키워드 검색

## 부적합한 작업 (→ /explore 사용)

- 코드 구조 분석
- 복잡한 의존성 파악
- 아키텍처 이해
- 심층 분석

## 결과

- Haiku 모델이 빠르게 검색
- 비용 절약: 약 90%
- 속도: Opus/Sonnet 대비 빠름
