# List Docs

프로젝트의 마크다운 문서 목록을 [TOON 포맷](https://github.com/toon-format/toon)으로 출력하는 스킬

## 왜 만들었나요

- AI가 컨벤션 기반으로 코드를 작성하고 도와주려면 관련 문서를 참조해야 함
- 근데 문서가 많으면 `ls`로 파일명만 보고 추측해서 하나씩 열어봄
- 결국 불필요한 토큰 소모 + 응답 시간 증가
- 이 스킬로 문서 경로와 설명을 한번에 보여주면 AI가 필요한 문서만 바로 찾아감

## 이렇게 쓰고 있어요

- AI가 프로젝트 규칙/가이드라인 파악할 때 먼저 실행
- 필요한 문서만 골라서 읽을 수 있어서 토큰 절약
- 문서에 description 메타데이터 추가하면 AI가 더 정확하게 찾아감

## 사용 방법

### 빠른 시작

```bash
bash ./skills/list-docs/list-docs.sh
```

### 상세 설정 (선택)

| 옵션 | 설명 |
|------|------|
| `--path=<dir>` | 특정 경로 하위 문서만 조회 |

```bash
# 특정 디렉토리만 조회
bash ./skills/list-docs/list-docs.sh --path=src
bash ./skills/list-docs/list-docs.sh --path=src/modules/
```

## 출력 예시

```
docs[3]{path,desc}:
docs/architecture.md,시스템 아키텍처; 레이어 구조; 의존성 흐름
docs/api-guide.md,REST API 엔드포인트; 인증 방식; 에러 코드
README.md,프로젝트 개요; 설치 가이드
```

## 문서에 메타데이터 추가하기

각 마크다운 파일 상단에 YAML frontmatter를 추가하면 설명이 함께 출력됨:

```yaml
---
name: API 가이드
description: REST API 엔드포인트; 인증 방식; 에러 코드
---
```

**description 작성 팁:**
- 세미콜론(`;`)으로 키워드 구분
- AI가 검색하기 좋은 구체적인 용어 사용
- 100자 이내 권장

## 주의사항

- `node_modules/`, `.next/`, `.git/`, `.github/`, `dist/`, `build/`, `coverage/`, `.context/` 자동 제외
- `CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, `AGENTS-GOVERNANCE.md` 등 이미 컨텍스트에 로드되는 파일은 제외
- `.claude/` 폴더도 제외