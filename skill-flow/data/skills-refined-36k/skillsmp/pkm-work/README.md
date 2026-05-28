# PKM Work Documentation Skill

GitHub Pull Request를 분석하여 Obsidian PKM 시스템에 자동으로 문서화하는 skill입니다.

## 기능

- GitHub Enterprise (github.kakaocorp.com) PR에서 정보를 자동으로 수집 및 분석
- Obsidian inbox에 work 템플릿 기반 노트 자동 생성
- Daily journal에 시간대별 백링크 자동 추가
- 여러 repository에서 PR 자동 검색 및 중복 확인

## 지원 Repository

- `kjk/goomba-hub`
- `kjk/flutter_epub_viewer`
- `kjk/pluto_grid`
- `kjk/flutter_ocr`

## 사용 방법

### 1. PKM Agent를 통한 사용 (권장)

**PR 번호만 제공 (자동 검색)**
```
@agent/pkm PR #123 문서화해줘
```

**전체 URL 제공**
```
@agent/pkm https://github.kakaocorp.com/kjk/goomba-hub/pull/123 작업 내용 정리해줘
```

**Repository 힌트 제공**
```
@agent/pkm goomba-hub PR #123 정리해줘
```

### 2. 직접 Skill 호출

OpenCode에서 직접 skill을 로드하여 사용:

```
/skill pkm-work
```

그 후 PR URL 또는 번호를 제공하면 자동으로 처리됩니다.

## 출력 결과

### Work Note 생성
- 위치: `007 inbox/YYYY-MM-DD [PR Title].md`
- 내용:
  - PR 요약 (summary callout)
  - 작업 목적
  - 주요 변경사항
  - 기술적 의사결정
  - 테스트 내용
  - 참고 링크

### Daily Journal 업데이트
- 위치: `005 journals/YYYY/YYYY-MM-DD.md`
- 현재 시간에 따라 적절한 섹션에 백링크 추가:
  - Morning (06:00-11:59)
  - Afternoon (12:00-17:59)
  - Evening (18:00-23:59)

## 필수 조건

1. **GitHub Enterprise CLI 설치 및 인증**
   ```bash
   # GitHub Enterprise 인증
   gh auth login --hostname github.kakaocorp.com
   ```

2. **Obsidian MCP 서버 설정**
   - OpenCode의 Obsidian MCP가 활성화되어 있어야 함

3. **Vault 구조**
   - `007 inbox/` 디렉토리 존재
   - `005 journals/YYYY/` 디렉토리 존재
   - Daily note 형식: `YYYY-MM-DD.md`

4. **Repository 접근 권한**
   - 지원하는 모든 repository에 대한 읽기 권한 필요

## 예제

### 시나리오 1: PR 번호만 제공 (단일 매치)
```
입력: PR #456 문서화
처리: goomba-hub에서 PR #456 발견
출력: 자동으로 문서 생성
```

### 시나리오 2: PR 번호만 제공 (중복 매치)
```
입력: PR #123 문서화
처리: 여러 repo에서 발견
출력: 
  PR #123을 다음 repository에서 발견했습니다:
  1. goomba-hub: "Add dark mode toggle"
  2. flutter_epub_viewer: "Fix page calculation"
  
  어떤 PR을 문서화할까요? (번호 입력)
사용자 선택: 1
결과: goomba-hub의 PR 문서화
```

### 시나리오 3: 전체 URL 제공
```
입력: https://github.kakaocorp.com/kjk/goomba-hub/pull/789
출력: 자동으로 문서 생성
```

## 카테고리 자동 판단

변경된 파일 경로를 분석하여 자동으로 카테고리를 설정합니다:

| 파일 경로 패턴 | 카테고리 |
|--------------|---------|
| `lib/`, `src/` | development |
| `android/`, `ios/` | mobile |
| `test/`, `spec/` | testing |
| `docs/`, `README` | documentation |
| `.github/`, `ci/` | devops |

## 문제 해결

### PR을 찾을 수 없음
- GitHub Enterprise CLI 인증 상태 확인: `gh auth status --hostname github.kakaocorp.com`
- Repository 접근 권한 확인
- PR 번호가 정확한지 확인
- 지원하는 repository 목록 확인

### 여러 PR이 발견됨
- Skill이 자동으로 목록을 표시합니다
- 원하는 repository의 번호를 선택하세요
- 또는 전체 URL을 제공하여 명확하게 지정하세요

### Daily journal 섹션이 없음
- Skill이 자동으로 섹션을 생성합니다
- Daily note가 없으면 생성을 시도합니다

### 파일명 충돌
- 이미 같은 이름의 파일이 있으면 숫자를 추가합니다
- 예: `2026-01-15 PR Title 2.md`

## 향후 개선 사항

- [ ] 더 많은 repository 지원 추가
- [ ] PR 리뷰 코멘트 포함
- [ ] 관련 JIRA 티켓 자동 링크
- [ ] 커밋 히스토리 분석
- [ ] 작업 시간 추정
- [ ] GitHub.com (public) 지원
- [ ] GitLab 지원
