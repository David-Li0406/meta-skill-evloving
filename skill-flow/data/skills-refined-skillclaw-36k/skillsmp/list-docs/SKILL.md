---
name: list-docs
description: 프로젝트의 마크다운 문서 목록을 TOON 포맷으로 출력합니다
---

# List Docs

프로젝트의 마크다운 문서를 토큰 효율적인 TOON 포맷으로 조회합니다.

AI가 프로젝트 규칙과 가이드라인을 파악할 때 유용합니다.

## What it does

- 프로젝트 전체에서 `*.md` 파일 탐색
- `--path` 옵션으로 특정 경로 하위 문서만 필터링
- TOON 포맷으로 출력 (토큰 효율적)

## Excluded

- `node_modules/`, `.next/`, `.git/`, `.github/`, `dist/`, `build/`, `coverage/`, `.context/`
- `CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, `AGENTS-GOVERNANCE.md` (이미 컨텍스트에 로드됨)
- `.claude/` 폴더

## How to use

```bash
# 모든 문서 조회
/list-docs

# 특정 경로 하위 문서만 조회
/list-docs --path=src
/list-docs --path=src/modules/
```

## Output Format (TOON)

```
docs[3]{path,desc}:
docs/architecture.md,시스템 아키텍처; 레이어 구조; 의존성 흐름
docs/api-guide.md,REST API 엔드포인트; 인증 방식
README.md,프로젝트 개요; 설치 가이드
```

## Metadata Format

각 마크다운 파일 상단에 YAML frontmatter로 메타데이터를 추가하세요:

```yaml
---
name: 문서 이름
description: 이 문서에서 알 수 있는 구체적인 내용
---
```

**description 작성 팁:**
- 세미콜론(`;`)으로 키워드 구분
- AI가 검색하기 좋은 구체적인 용어 사용
- 100자 이내 권장
