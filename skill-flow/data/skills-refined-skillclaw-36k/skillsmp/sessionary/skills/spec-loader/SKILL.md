---
name: spec-loader
description: >
  Sessionary 프로젝트 spec 문서를 context에 로드하는 skill.
  사용자가 도메인 개념(Lecture, Session, Subscription, Folder, 티켓 시스템)에 대해 질문하거나,
  비즈니스 로직/접근 권한 규칙을 확인하거나,
  인프라(비디오 스트리밍, Cloudflare, MinIO) 관련 작업을 하거나,
  프론트엔드 비디오 플레이어 구현하거나,
  디자인 토큰이나 색상값이 필요할 때 사용.
  키워드 - spec, 기획, 도메인, lecture, session, subscription, ticket, folder, video, streaming, cloudflare, minio, design token
---

# Spec Loader

Sessionary 프로젝트의 spec 문서를 효율적으로 context에 로드한다.

## 문서 위치

`docs/spec/` 폴더에 위치한다.

## 문서 매핑

| 키워드 | 문서 | 내용 |
|--------|------|------|
| lecture, 강의, 접근권한, 티켓 | `domain/lecture.md` | Lecture 개념, 티켓 차감 플로우, 접근 권한 테이블 |
| session, 세션, 타입 | `domain/session.md` | Session 5가지 타입 (PLAY/TALK/JAM/BASIC/SHEET) |
| subscription, 구독, plan, 플랜, 결제 | `domain/subscription.md` | 4가지 구독 플랜, 결제 연동 참고사항 |
| folder, 재생목록, 플레이리스트 | `domain/folder.md` | 커스텀 재생목록 개념 |
| video, streaming, cloudflare, minio, 스트리밍 | `infrastructure/video-streaming.md` | Cloudflare Stream 설정, MinIO 로컬 환경 |
| player, 플레이어, hls | `frontend/video-player.md` | 비디오 플레이어 구현 계획 |
| design, token, 색상, color | `design/design-tokens.md` | 브랜드 색상, Session 타입별 색상 |

## 사용 방법

1. 사용자 질문에서 키워드를 파악한다
2. 해당하는 문서만 선택적으로 Read 한다
3. 여러 문서가 필요하면 병렬로 Read 한다

## 예시

**질문**: "티켓 차감 로직이 어떻게 되나요?"
→ `docs/spec/domain/lecture.md` 읽기 (티켓 시스템 섹션)

**질문**: "구독 플랜 종류가 뭐가 있나요?"
→ `docs/spec/domain/subscription.md` 읽기

**질문**: "비디오 스트리밍 어떻게 구현하나요?"
→ `docs/spec/infrastructure/video-streaming.md` + `docs/spec/frontend/video-player.md` 병렬 읽기

**질문**: "Session 타입별 색상이 뭔가요?"
→ `docs/spec/domain/session.md` 또는 `docs/spec/design/design-tokens.md` 읽기

## 전체 개요가 필요한 경우

프로젝트 전반적인 이해가 필요하면 `docs/spec/README.md`를 먼저 읽는다.
