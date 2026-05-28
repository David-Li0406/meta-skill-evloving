# LLM 프로바이더 가이드

## 지원 프로바이더 개요

| 프로바이더 | 특징 | 권장 용도 | 비용 |
|-----------|------|----------|------|
| OpenAI | 높은 품질, 다양한 모델 | 복잡한 추론, 코드 생성 | 유료 |
| Google Gemini | 빠른 속도, 긴 컨텍스트 | 문서 분석, 빠른 응답 | 유료 (무료 티어 있음) |
| Anthropic | 안전성, 긴 응답 | 상세 분석, 장문 생성 | 유료 |
| Ollama | 로컬 실행, 프라이버시 | 민감한 데이터, 비용 절감 | 무료 |

## OpenAI

### 설정
```bash
export OPENAI_API_KEY="sk-..."
```

### 주요 모델

| 모델 | 컨텍스트 | 특징 |
|------|---------|------|
| gpt-4o | 128K | 최신, 멀티모달, 빠름 |
| gpt-4o-mini | 128K | 저비용, 빠름 |
| gpt-4-turbo | 128K | 고성능 |
| o1-preview | 128K | 복잡한 추론 특화 |
| o1-mini | 128K | 추론 특화, 저비용 |

### 사용 예시
```python
from llm_client import LLMClientFactory

client = LLMClientFactory.create("openai", model="gpt-4o")
response = client.chat([Message(role="user", content="Hello")])
```

### 비용 (2024년 12월 기준, 1M 토큰당)
- gpt-4o: 입력 $2.50 / 출력 $10.00
- gpt-4o-mini: 입력 $0.15 / 출력 $0.60

---

## Google Gemini

### 설정
```bash
export GOOGLE_API_KEY="..."
```

### 주요 모델

| 모델 | 컨텍스트 | 특징 |
|------|---------|------|
| gemini-2.0-flash | 1M | 매우 빠름, 저비용 |
| gemini-1.5-pro | 2M | 초장문 컨텍스트 |
| gemini-1.5-flash | 1M | 빠름 |

### 사용 예시
```python
client = LLMClientFactory.create("gemini", model="gemini-2.0-flash")
response = client.chat([Message(role="user", content="Hello")])
```

### 특징
- 매우 긴 컨텍스트 윈도우 (최대 2M 토큰)
- 무료 티어 제공
- 빠른 응답 속도

---

## Anthropic Claude

### 설정
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 주요 모델

| 모델 | 컨텍스트 | 특징 |
|------|---------|------|
| claude-opus-4-20250514 | 200K | 최고 성능 |
| claude-sonnet-4-20250514 | 200K | 균형잡힌 성능 |
| claude-haiku-3-5-20241022 | 200K | 빠름, 저비용 |

### 사용 예시
```python
client = LLMClientFactory.create("anthropic", model="claude-sonnet-4-20250514")
response = client.chat([Message(role="user", content="Hello")])
```

### 특징
- 안전성과 도움됨의 균형
- 긴 응답 생성에 강점
- 복잡한 지시 따르기 우수

---

## Ollama (로컬 LLM)

### 설치
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# 서비스 시작
ollama serve
```

### 모델 다운로드
```bash
ollama pull llama3.2
ollama pull codellama
ollama pull mistral
```

### 주요 모델

| 모델 | 크기 | 특징 |
|------|-----|------|
| llama3.2 | 3B/8B | 범용, Meta 최신 |
| codellama | 7B/13B | 코드 특화 |
| mistral | 7B | 범용, 효율적 |
| mixtral | 8x7B | 고성능, MoE |

### 사용 예시
```python
client = LLMClientFactory.create("ollama", model="llama3.2")
response = client.chat([Message(role="user", content="Hello")])
```

### 환경 변수 (선택)
```bash
export OLLAMA_HOST="http://localhost:11434"  # 기본값
```

### 장점
- 완전 무료
- 데이터 프라이버시 보장
- 인터넷 연결 불필요
- 커스터마이징 가능

### 단점
- 하드웨어 요구사항 (GPU 권장)
- 클라우드 모델 대비 낮은 성능
- 모델 크기 제한

---

## 프로바이더 선택 가이드

### 작업별 권장 프로바이더

| 작업 유형 | 1순위 | 2순위 | 이유 |
|----------|------|------|------|
| 복잡한 코드 생성 | OpenAI | Anthropic | 높은 정확도 |
| 코드 리뷰 | Anthropic | OpenAI | 상세한 피드백 |
| 긴 문서 분석 | Gemini | Anthropic | 긴 컨텍스트 |
| 빠른 응답 | Gemini | Ollama | 낮은 지연 |
| 민감한 데이터 | Ollama | - | 로컬 처리 |
| 비용 절감 | Ollama | Gemini | 무료/저비용 |
| 브레인스토밍 | OpenAI | Gemini | 창의성 |

### 멀티 에이전트 조합 예시

**코드 개발 팀:**
```yaml
- architect: openai/gpt-4o (설계 능력)
- developer: gemini/gemini-2.0-flash (빠른 구현)
- reviewer: anthropic/claude-sonnet (상세 리뷰)
- tester: ollama/codellama (비용 절감)
```

**문서 분석 팀:**
```yaml
- analyzer: gemini/gemini-1.5-pro (긴 문서)
- critic: openai/gpt-4o (비판적 분석)
- synthesizer: anthropic/claude-sonnet (종합)
```

---

## 공통 파라미터

### temperature
창의성 조절 (0~1 또는 0~2)
- 0: 결정적, 일관된 응답
- 0.7: 균형 (기본값)
- 1+: 창의적, 다양한 응답

```python
response = client.chat(messages, temperature=0.3)
```

### max_tokens
최대 출력 토큰 수
```python
response = client.chat(messages, max_tokens=2048)
```

### timeout
요청 타임아웃 (초)
```python
response = client.chat(messages, timeout=60)
```

---

## 에러 처리

### 공통 에러

| 에러 | 원인 | 해결 |
|-----|------|-----|
| 401 Unauthorized | API 키 오류 | 키 확인 및 재설정 |
| 429 Too Many Requests | 요청 제한 | 대기 후 재시도 |
| 500 Internal Error | 서버 오류 | 재시도 |
| Timeout | 응답 지연 | 타임아웃 증가 |

### 재시도 로직
```python
import time
from requests.exceptions import RequestException

def call_with_retry(client, messages, max_retries=3):
    for i in range(max_retries):
        try:
            return client.chat(messages)
        except RequestException as e:
            if i == max_retries - 1:
                raise
            time.sleep(2 ** i)  # 지수 백오프
```

---

## 비용 최적화 팁

1. **적절한 모델 선택**: 단순 작업에는 mini/flash 모델
2. **캐싱 활용**: 동일 요청 결과 캐싱
3. **프롬프트 최적화**: 불필요한 토큰 줄이기
4. **로컬 LLM 활용**: 민감하지 않은 반복 작업
5. **배치 처리**: 가능한 경우 요청 묶기
