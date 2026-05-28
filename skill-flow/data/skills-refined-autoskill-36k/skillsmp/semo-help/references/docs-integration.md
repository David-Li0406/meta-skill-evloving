# docs 레포 연동 가이드

> semo-help 스킬에서 docs 레포 정보를 조회하는 방법

## docs 레포 구조

```text
semicolon-devteam/docs
├── wiki/                # 팀 위키 문서
├── sax/                 # SEMO 관련 문서
│   ├── core/           # SEMO Core 문서
│   │   ├── PRINCIPLES.md
│   │   ├── MESSAGE_RULES.md
│   │   └── TEAM_RULES.md
│   └── packages/       # 패키지별 문서
└── README.md
```

## GitHub CLI 조회

### 위키 문서 목록

```bash
gh api repos/semicolon-devteam/docs/contents/wiki \
  --jq '.[].name'
```

### 특정 문서 조회

```bash
# TEAM_RULES.md 조회
gh api repos/semicolon-devteam/docs/contents/sax/core/TEAM_RULES.md \
  --jq '.content' | base64 -d
```

### SEMO 패키지 문서 조회

```bash
# 패키지 목록
gh api repos/semicolon-devteam/docs/contents/sax/packages \
  --jq '.[].name'

# 특정 패키지 문서
gh api repos/semicolon-devteam/docs/contents/sax/packages/{package_name} \
  --jq '.content' | base64 -d
```

## 응답 템플릿

### docs 참조 시

```markdown
[SEMO] Skill: semo-help 응답

## {질문 주제}

{docs 레포에서 조회한 내용}

---
📚 출처: [docs/wiki/{문서명}](https://github.com/semicolon-devteam/docs/wiki/{문서명})
```

### 문서 없음 시

```markdown
⚠️ **관련 문서 없음**

요청하신 '{주제}'에 대한 docs 문서가 없습니다.
semo-core 문서를 참조하거나, 팀 위키에 추가를 요청하세요.
```

## 캐싱 전략

- docs 레포 내용은 세션 내에서 캐싱 권장
- 동일 문서 반복 조회 시 이전 결과 재사용
- 캐시 무효화: `/SEMO:update` 실행 시
