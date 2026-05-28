---
tags:
- 30_Resources
---
# Git Skill Manager - Quick Reference

## 📦 설치 (Install)

```bash
python .claude/skills/git-skill-manager/scripts/manage.py install --git-url "URL"
```

**옵션:**
- `--git-url` (필수): GitHub repository URL
- `--plugin-name` (선택): 커스텀 플러그인 이름
- `--target-path` (선택): 설치 경로 (기본: `.claude`)

**예시:**
```bash
# 기본 설치
python scripts/manage.py install --git-url "https://github.com/kepano/obsidian-skills"

# 커스텀 이름으로 설치
python scripts/manage.py install --git-url "https://github.com/user/repo" --plugin-name "my-plugin"
```

---

## 📋 목록 조회 (List)

```bash
python .claude/skills/git-skill-manager/scripts/manage.py list
```

**옵션:**
- `--target-path` (선택): 대상 경로 (기본: `.claude`)

**예시:**
```bash
# 설치된 모든 plugin 보기
python scripts/manage.py list
```

---

## 🗑️ 제거 (Uninstall)

```bash
python .claude/skills/git-skill-manager/scripts/manage.py uninstall --skill-name "NAME"
```

**옵션:**
- `--skill-name` (필수): 제거할 skill 이름
- `--target-path` (선택): 대상 경로 (기본: `.claude`)

**예시:**
```bash
# skill 제거
python scripts/manage.py uninstall --skill-name "json-canvas"
```

---

## 💡 Tips

### 설치된 skill 이름 확인
```bash
python scripts/manage.py list
```

### 도움말 보기
```bash
python scripts/manage.py --help
python scripts/manage.py install --help
python scripts/manage.py uninstall --help
python scripts/manage.py list --help
```

### 상대 경로에서 실행
현재 위치가 프로젝트 루트일 때:
```bash
python .claude/skills/git-skill-manager/scripts/manage.py list
```

현재 위치가 skill 폴더일 때:
```bash
python scripts/manage.py list
```

---

## 📁 파일 위치

- **설치 스크립트**: `.claude/skills/git-skill-manager/scripts/manage.py`
- **레지스트리**: `.claude/skills/git-skill-manager/assets/registry.json`
- **설치된 skills**: `.claude/skills/[skill-name]/`

---

## ⚠️ 주의사항

1. **인터넷 연결 필요**: GitHub API를 사용하므로 네트워크 연결이 필요합니다.
2. **GitHub URL 형식**: `https://github.com/owner/repo` 형식이어야 합니다.
3. **Skill 이름**: 제거할 때는 plugin 이름이 아닌 개별 skill 이름을 사용합니다.

---

## 🔧 문제 해결

### "skill을 찾을 수 없습니다" 에러
→ `list` 명령으로 정확한 skill 이름 확인

### HTTP 에러
→ GitHub URL이 올바른지 확인
→ 인터넷 연결 확인
→ Repository가 public인지 확인

### 권한 에러
→ `.claude/skills` 폴더에 쓰기 권한이 있는지 확인

---

**자세한 문서**: [SKILL.md](SKILL.md) | [README.md](README.md) | [MIGRATION.md](MIGRATION.md)
