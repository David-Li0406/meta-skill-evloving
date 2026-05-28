---
name: sessionary
description: This is a new rule
---

## 코딩 컨벤션

- 주석 대신 private method로 리팩터링하여 실행 순서가 드러나게 작성하세요.
- 꼭 필요한 경우에만 주석 사용
- 응답은 한국어로 작성

# Sessionary 프로젝트 규칙

## 참조 문서

도메인 지식과 기획 문서는 `docs/spec/` 폴더를 참조하세요.

### 문서 구조

```
docs/spec/
├── README.md                    # 프로젝트 개요
├── domain/                      # 도메인 용어 및 비즈니스 로직
│   ├── lecture.md              # Lecture 용어 + 티켓 시스템
│   ├── session.md              # Session 타입
│   ├── subscription.md         # 구독 플랜
│   └── folder.md               # 커스텀 재생목록
├── infrastructure/              # 인프라 설정
│   └── video-streaming.md      # 비디오 스트리밍
├── frontend/                    # 프론트엔드 구현
│   └── video-player.md         # 비디오 플레이어
└── design/                      # 디자인 시스템
    └── design-tokens.md        # 디자인 토큰
```

> **Note**: API 명세는 backend 코드(`/docs` 엔드포인트)가 Single Source of Truth입니다.
