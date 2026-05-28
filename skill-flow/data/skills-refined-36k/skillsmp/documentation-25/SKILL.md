---
name: documentation
description: README, 마크다운 문서, 아키텍처 문서 등 사용자가 읽을 수 있는 문서를 작성할 때 사용. 다이어그램 형식과 문서 구조 가이드라인을 따름.
---

# 문서화 가이드라인

## 다이어그램

모든 다이어그램은 **Mermaid** 문법을 사용합니다.

### 지원 다이어그램 유형
- 플로우차트 (flowchart)
- 시퀀스 다이어그램 (sequenceDiagram)
- 클래스 다이어그램 (classDiagram)
- ER 다이어그램 (erDiagram)
- 상태 다이어그램 (stateDiagram)

### 금지 사항
- ASCII 아트 다이어그램
- 일반 텍스트 박스 다이어그램

### 이유
- GitHub에서 올바르게 렌더링
- IDE 미리보기 지원
- 문서 사이트에서 시각화

## 예시

```mermaid
flowchart LR
    A[사용자] --> B[컨트롤러]
    B --> C[서비스]
    C --> D[리포지토리]
    D --> E[(데이터베이스)]
```

```mermaid
sequenceDiagram
    participant U as 사용자
    participant C as 컨트롤러
    participant S as 서비스

    U->>C: 요청
    C->>S: 처리
    S-->>C: 결과
    C-->>U: 응답
```
