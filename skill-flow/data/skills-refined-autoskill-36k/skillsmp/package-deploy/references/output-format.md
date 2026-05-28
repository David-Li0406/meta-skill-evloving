# Output Format

> package-deploy Skill의 출력 형식

## 성공 시

```json
{
  "status": "✅ SUCCESS",
  "package": "semo-next",
  "source": "sax/packages/semo-next/",
  "target": "/path/to/project/.claude/",
  "version": "3.19.0",
  "mode": "install",
  "files_deployed": {
    "claude_md": 1,
    "agents": 12,
    "skills": 13,
    "commands": 4,
    "total": 30
  },
  "next_steps": [
    ".claude/CLAUDE.md 설정",
    "/SEMO:health-check 실행",
    "git commit -m '📝 [SEMO] Sync to v3.19.0'"
  ]
}
```

## 업데이트 성공 시

```json
{
  "status": "✅ SUCCESS",
  "package": "semo-next",
  "mode": "update",
  "version": {
    "previous": "3.18.0",
    "current": "3.19.0"
  },
  "changes": {
    "added": 2,
    "updated": 5,
    "removed": 1
  },
  "next_steps": [
    "CHANGELOG 확인: sax/CHANGELOG/3.19.0.md",
    "변경사항 테스트",
    "git commit -m '📝 [SEMO] Sync to v3.19.0'"
  ]
}
```

## 실패 시

```json
{
  "status": "❌ FAIL",
  "package": "semo-next",
  "target": "/path/to/project/",
  "error": "대상 경로를 찾을 수 없습니다",
  "resolution": "경로 확인 후 재시도"
}
```

## Error Types

| Error | 설명 | 해결 방법 |
|-------|------|----------|
| TARGET_NOT_FOUND | 대상 경로 없음 | 경로 확인 |
| TARGET_NOT_WRITABLE | 쓰기 권한 없음 | 권한 확인 |
| PACKAGE_NOT_FOUND | 소스 패키지 없음 | docs 레포 확인 |
| SCRIPT_NOT_FOUND | deploy.sh 없음 | sax/scripts/ 확인 |
| VERSION_SAME | 동일 버전 | --update 생략 가능 |

## 터미널 출력 예시

### 신규 설치

```
[SEMO] Skill: package-deploy 호출 - semo-next → /path/to/project

🚀 배포 시작: semo-next

소스: sax/packages/semo-next/
대상: /path/to/project/.claude/
버전: v3.19.0

Deploying SEMO-Next to /path/to/project
✅ SEMO-Next deployed successfully!
Note: Update your CLAUDE.md to reference SEMO-Next package

Deployment complete!
SEMO Version: 3.19.0

[SEMO] Deploy: semo-next → /path/to/project 배포 완료 (v3.19.0)
```

### 업데이트

```
[SEMO] Skill: package-deploy 호출 - semo-next → /path/to/project (update)

🔄 업데이트 시작: semo-next

Current version in target: 3.18.0
Source version: 3.19.0

Deploying SEMO-Next to /path/to/project
✅ SEMO-Next deployed successfully!

📋 CHANGELOG 확인 권장:
gh api repos/semicolon-devteam/docs/contents/sax/CHANGELOG/3.19.0.md \
  --jq '.content' | base64 -d

[SEMO] Deploy: semo-next 업데이트 완료 (3.18.0 → 3.19.0)
```
