# Broken Link Checker

마크다운 문서의 깨진 링크를 자동으로 찾아주는 스킬

## 왜 만들었나요

- 문서가 많아지면 링크가 깨지는 걸 놓치기 쉬움
- 파일 이름 변경하거나 문서 구조 바꿀 때 어디가 깨졌는지 일일이 확인하기 번거로움
- 이 스킬로 한 번에 모든 마크다운 파일의 링크 상태를 점검할 수 있음

## 이렇게 쓰고 있어요

- AI가 주기적으로 스케줄링하여 문서 품질 체크
- 깨진 링크 발견 시 자동으로 수정 PR 생성
- 문서 리팩토링 후 링크 상태 점검

## 사용 방법

### 빠른 시작

```bash
bash ./skills/broken-link-checker/check-broken-links.sh
```

### 상세 설정 (선택)

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--path <dir>` | 프로젝트 루트 | 특정 디렉토리만 검사 |
| `--verbose, -v` | false | 상세 진행 상황 표시 |

```bash
# 특정 디렉토리만 검사
bash ./skills/broken-link-checker/check-broken-links.sh --path ./docs

# 상세 로그 보기
bash ./skills/broken-link-checker/check-broken-links.sh --verbose
```

## 필요한 것

- `grep`, `sed`, `perl` (대부분 시스템에 기본 설치됨)

## 주의사항

- 외부 URL(https://, mailto:, tel:)은 검사하지 않고 스킵함
- node_modules, .git, dist 디렉토리는 자동 제외
- 앵커 링크는 GitHub 스타일 ID 변환 규칙 적용