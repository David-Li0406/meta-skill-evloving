---
name: pkm-work
description: GitHub Pull Request를 분석하여 Obsidian PKM 시스템에 work 노트를 자동 생성하고 daily journal에 백링크를 추가합니다. PR URL 또는 PR 번호를 전달하면 자동으로 처리됩니다.
---

# PKM Work Documentation Skill

이 skill은 GitHub Pull Request를 분석하여 Obsidian vault의 inbox에 작업 문서를 생성하고, 오늘의 업무 일지에 자동으로 백링크를 추가합니다.

## 사용 방법

### 입력 파라미터
- `pr_url` 또는 `pr_number`: GitHub Pull Request URL 또는 PR 번호
- `repo` (선택): Repository 이름 (PR 번호만 제공할 경우, 아래 목록에서 선택)

### 지원 Repository 목록
PR 번호만 제공하는 경우, 다음 repository에서 검색합니다:
1. `https://github.kakaocorp.com/kjk/goomba-hub`
2. `https://github.kakaocorp.com/kjk/flutter_epub_viewer`
3. `https://github.kakaocorp.com/kjk/pluto_grid`
4. `https://github.kakaocorp.com/kjk/flutter_ocr`

**중복 처리**: 동일한 PR 번호가 여러 repository에 존재하는 경우, 사용자에게 어떤 repository의 PR인지 확인을 요청합니다.

### Repository 확인 프로세스
1. PR 번호만 제공된 경우, 모든 지원 repository에서 해당 PR 검색
2. 발견된 PR 목록을 사용자에게 제시:
   ```
   PR #123을 다음 repository에서 발견했습니다:
   1. goomba-hub: "Add dark mode feature"
   2. flutter_epub_viewer: "Fix page calculation bug"
   
   어떤 PR을 문서화할까요? (번호 입력)
   ```
3. 사용자 선택 후 해당 PR 처리

### 처리 프로세스

1. **PR 정보 수집**
   - GitHub에서 PR 데이터 가져오기 (제목, 본문, 변경사항)
   - 변경된 파일 목록 및 diff 분석
   - 관련 이슈/티켓 추출

2. **Work 노트 생성**
   - 위치: `007 inbox/[PR Title].md`
   - work 템플릿 기반 마크다운 문서 생성
   - **문체 가이드**: 정확하고 프로페셔널하며 간결한 문체 사용. 서술형 구어체 지양.
   - 구조:
     ```markdown
     ---
     created: YYYY-MM-DD HH:mm:ss
     modified: YYYY-MM-DD HH:mm:ss
     date: YYYY-MM-DD
     tags:
       - work
     category: [적절한 카테고리]
     pr_url: [GitHub PR URL]
     repository: [repo-name]
     ---
     
     >[!summary] 
     >- [핵심 변경사항 1]
     >- [핵심 변경사항 2]
     >- [핵심 변경사항 3]

     ## 개요
     - **목적**: [명확한 목적]
     - **변경 범위**: [영향받는 모듈/컴포넌트]
     - **상태**: [OPEN/MERGED/CLOSED]

     ## 변경사항

     ### 주요 구현
     - **[모듈/파일명]**: [변경 내용]
     - **[모듈/파일명]**: [변경 내용]

     ### 아키텍처
     ```mermaid
     [필요시 시퀀스/플로우/컴포넌트 다이어그램으로 변경사항 시각화]
     ```

     ### 기술 스택
     - [사용된 주요 기술/라이브러리]
     - [적용된 디자인 패턴]

     ## 기술적 의사결정

     | 선택지 | 선택 이유 | Trade-off |
     |--------|----------|-----------|
     | [선택한 방식] | [이유] | [장단점] |

     ## 테스트
     - **단위 테스트**: [커버리지 또는 주요 테스트 케이스]
     - **통합 테스트**: [시나리오]
     - **검증 결과**: [Pass/Fail 및 주요 발견사항]

     ## 후속 작업

     ### 개선 가능 영역
     - [ ] [리팩토링이 필요한 부분]
     - [ ] [최적화 가능한 영역]
     - [ ] [기술 부채]

     ### 확장 아이디어
     - [ ] [추가 기능 제안]
     - [ ] [적용 가능한 다른 영역]

     ## 참고
     - **PR**: [URL]
     - **Related Issues**: [#issue-number]
     - **Discussion**: [주요 논의사항 링크]
     - **Dependencies**: [연관 PR/이슈]
     ```

3. **Daily Journal 업데이트**
   - 현재 시간 기준으로 적절한 섹션 결정:
     - Morning (오전): 06:00 ~ 11:59
     - Afternoon (오후): 12:00 ~ 17:59
     - Evening (저녁): 18:00 ~ 23:59
   - 해당 섹션에 백링크 추가: `- [[PR Title]]`
   - Daily journal 위치: `005 journals/YYYY/YYYY-MM-DD.md`
   - **중요**: MCP의 `obsidian_patch_content` 또는 `obsidian_append_content` 도구를 사용하지 말 것
   - **반드시** 다음 프로세스를 따를 것:
     1. `Read` 도구로 해당 일자의 daily journal 파일을 직접 읽기
     2. 파일이 없으면 전체 구조를 생성 (frontmatter + Morning/Afternoon/Evening 섹션)
     3. 파일이 있으면 시간대에 맞는 섹션 찾기
     4. 해당 섹션이 없으면 섹션 헤더 추가
     5. `Edit` 도구로 해당 섹션에 백링크 추가 (섹션 마지막에 `- [[노트 제목]]` 형식으로 추가)
     6. 기존 내용을 보존하면서 새 백링크만 추가

## 구현 세부사항

### PR 분석 로직
1. GitHub CLI (`gh`) 또는 GitHub API를 사용하여 PR 정보 수집
2. PR 제목에서 JIRA 티켓 번호, 이슈 번호 등 추출
3. Changed files를 카테고리별로 분류 (frontend, backend, docs, test 등)
4. 주요 변경사항을 간결하게 요약 (추가된 기능, 수정된 버그, 리팩토링 등)
5. 복잡한 로직/플로우는 mermaid 다이어그램으로 시각화:
   - Sequence diagram: API 호출 플로우, 사용자 인터랙션
   - Flowchart: 조건 분기, 처리 로직
   - Class diagram: 구조 변경
   - Graph: 컴포넌트 관계, 의존성
6. 후속 작업 인사이트 도출:
   - 리팩토링 가능 영역 식별
   - 성능 최적화 기회 탐색
   - 확장 가능한 기능 제안
   - 관련 기술 부채 파악

### 파일명 생성 규칙
- 형식: `[PR Title].md`
- PR 제목이 너무 길면 적절히 축약 (최대 100자)
- 특수문자는 제거하거나 대체 (`/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|` → `-`)

### 카테고리 자동 판단
PR은 항상 `tags: work`로 설정합니다.

`category`는 PR 제목과 커밋 메시지의 타입 프리픽스를 분석하여 결정합니다:

**Conventional Commits 타입 기반 매핑:**
- `feat:`, `feature:` → **feature** (기능 개발, 구현)
- `fix:` → **fix** (버그 수정, 이슈 대응)
- `refactor:` → **refactor** (코드 구조 개선, 리팩토링)
- `docs:` → **docs** (문서 작성, 가이드 정리)
- `chore:`, `build:`, `ci:`, `style:` → **chore** (빌드 설정, 패키지 관리, 코드 스타일)
- `test:` → **chore** (테스트 코드는 chore로 분류)

**특수 케이스:**
- 제목에 "troubleshoot", "debug", "error", "issue" 포함 → **troubleshooting**
- 제목에 "plan", "design", "architecture" 포함 → **planning**
- 제목에 "setup", "config", "environment" 포함 → **setup**

**기본값:**
- 타입을 판단할 수 없는 경우 → **feature** (대부분의 PR이 기능 개발)

### 시간대 판단
```javascript
const now = new Date();
const hour = now.getHours();
let timeSection;
if (hour >= 6 && hour < 12) {
  timeSection = "Morning";
} else if (hour >= 12 && hour < 18) {
  timeSection = "Afternoon";
} else {
  timeSection = "Evening";
}
```

### Daily Journal 업데이트 구현
**중요**: MCP 도구 대신 직접 파일 읽기/쓰기를 사용합니다.

1. **파일 경로 결정**
   ```
   const vaultPath = [Obsidian vault 경로];
   const year = new Date().getFullYear();
   const date = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
   const journalPath = `${vaultPath}/005 journals/${year}/${date}.md`;
   ```

2. **파일 읽기 및 분석**
   - `Read` 도구로 journal 파일 읽기
   - 파일이 없으면 다음 구조로 생성:
     ```markdown
     ---
     date: YYYY-MM-DD
     tags:
       - daily
     ---
     
     ## Morning
     
     ## Afternoon
     
     ## Evening
     ```

3. **섹션 찾기 및 백링크 추가**
   - 시간대에 해당하는 섹션 헤더 찾기 (예: `## Afternoon`)
   - 해당 섹션의 마지막 줄 또는 다음 섹션 직전에 백링크 추가
   - `Edit` 도구 사용:
     ```
     oldString: 현재 섹션 내용
     newString: 현재 섹션 내용 + "\n- [[노트 제목]]"
     ```
   - 섹션이 비어있다면: `## Afternoon\n` → `## Afternoon\n- [[노트 제목]]`
   - 기존 항목이 있다면: 마지막 항목 뒤에 추가

4. **에러 처리**
   - 파일 읽기 실패: 새 파일 생성
   - 섹션이 없음: 해당 섹션 추가
   - 중복 백링크 방지: 동일한 백링크가 이미 있는지 확인

## 예제

### 입력 1: PR URL 제공
```
pr_url: "https://github.com/owner/repo/pull/123"
```

### 입력 2: PR 번호만 제공
```
pr_number: 123
# 자동으로 모든 repository에서 검색하여 사용자에게 선택 요청
```

### 입력 3: Repository 지정
```
pr_number: 123
repo: "goomba-hub"
```

### 출력
```
✅ Work note created: 007 inbox/다크모드 토글 기능 구현.md
✅ Daily journal updated: 005 journals/2026/2026-01-15.md (Afternoon section)
```

## 의존성
- GitHub CLI (`gh`) 또는 GitHub API 액세스
- Obsidian vault 파일 시스템 접근 (Read/Write/Edit 도구 사용)
- 날짜/시간 처리 유틸리티

**참고**: Work 노트 생성 시 MCP Obsidian 도구를 사용해도 되지만, Daily Journal 업데이트는 반드시 `Read`와 `Edit` 도구를 직접 사용해야 합니다.

## 에러 처리
- PR을 찾을 수 없는 경우: 명확한 에러 메시지 출력
- GitHub API 인증 실패: 인증 방법 안내
- 파일 생성 실패: Obsidian vault 경로 확인 요청
- Daily journal이 없는 경우: 자동으로 생성

## 주의사항
- 이미 같은 이름의 파일이 존재하는 경우 덮어쓰지 않고 번호를 추가 (예: `2026-01-15 PR Title 2.md`)
- Daily journal의 섹션 구조가 없으면 자동으로 생성
- Private repository의 경우 적절한 GitHub 권한 필요
