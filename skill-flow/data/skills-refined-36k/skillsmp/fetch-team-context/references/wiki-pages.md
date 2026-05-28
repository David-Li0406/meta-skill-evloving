# Wiki Pages Reference

## Topic to Wiki Page Mapping

| Topic | Wiki Page | URL |
|-------|-----------|-----|
| **Git & Commits** | Team Codex | https://github.com/semicolon-devteam/docs/wiki/Team-Codex |
| **Code Quality** | Team Codex | https://github.com/semicolon-devteam/docs/wiki/Team-Codex |
| **Workflow** | Collaboration Process | https://github.com/semicolon-devteam/docs/wiki/Collaboration-Process |
| **Architecture** | Development Philosophy | https://github.com/semicolon-devteam/docs/wiki/Development-Philosophy |
| **Estimation** | Estimation Guide | https://github.com/semicolon-devteam/docs/wiki/Estimation-Guide |
| **Epic Creation** | Process Phase 1 | https://github.com/semicolon-devteam/docs/wiki/Process-Phase-1-Epic-Creation |
| **Task Creation** | Process Phase 2 | https://github.com/semicolon-devteam/docs/wiki/Process-Phase-2-Task-Creation |
| **Development** | Process Phase 3 | https://github.com/semicolon-devteam/docs/wiki/Process-Phase-3-Development |
| **Deployment** | Process Phase 4 | https://github.com/semicolon-devteam/docs/wiki/Process-Phase-4-Deployment |

## Fetch Methods

### GitHub API

```bash
# List all wiki pages
gh api repos/semicolon-devteam/docs/contents | jq '.[].name'
```

### Web Fetch Fallback

```javascript
// Use web_fetch tool
web_fetch({
  url: "https://github.com/semicolon-devteam/docs/wiki/Team-Codex",
  extract: "main content",
});
```

## 문서 유효성 검증 필수

docs 레포지토리 문서 참조 시 404 응답이면 반드시 사용자에게 알림:

```
⚠️ **문서 참조 실패**
- 참조 문서: {document_name}
- 예상 경로: {url}
- 상태: 404 Not Found (문서가 이동되었거나 삭제됨)
- 권장 조치: docs 레포지토리에서 최신 문서 목록 확인
```
