# Generation Process

## Phase 3: Execute Generation

### 1. Run create-service.sh

```bash
./scripts/create-service.sh {project_name} {supabase_project_id} implement-dist/{project_name}
```

### 2. Update .env.local

```bash
# Replace placeholder keys with actual values
sed -i '' "s/your-anon-key-here/{anon_key}/" implement-dist/{project_name}/.env.local
sed -i '' "s/your-service-role-key-here/{service_role_key}/" implement-dist/{project_name}/.env.local
```

### 3. Update .claude.json

Update with Supabase access token (if available)

## Output Structure

```
implement-dist/
└── {project_name}/
    ├── src/
    │   ├── app/
    │   ├── components/
    │   ├── lib/
    │   ├── hooks/
    │   └── models/
    ├── public/
    ├── .claude/
    │   ├── agents/
    │   └── skills/
    ├── .husky/
    ├── CLAUDE.md           # 플레이스홀더 치환됨
    ├── README.md           # 플레이스홀더 치환됨
    ├── .env.local          # 실제 키 설정됨
    ├── .claude.json        # project-ref 업데이트됨
    ├── package.json        # name 업데이트됨
    ├── tsconfig.json
    ├── tailwind.config.ts
    ├── next.config.ts
    └── ...
```

## Phase 4: Report Success

```markdown
## 🎉 프로젝트 생성 완료!

**{service_title}** 프로젝트가 생성되었습니다.

### 📁 생성 위치

implement-dist/{project_name}/
├── src/              # 소스 코드
├── public/           # 정적 파일
├── .claude/          # Claude 에이전트/스킬
├── CLAUDE.md         # AI 가이드 (커스터마이즈됨)
├── README.md         # 프로젝트 문서 (커스터마이즈됨)
├── .env.local        # 환경 변수 (키 설정됨)
├── package.json      # 의존성 (이름 변경됨)
└── ...

### 🚀 다음 단계

1. **폴더 복사**:
   ```bash
   cp -r implement-dist/{project_name} ~/your-workspace/{project_name}
   cd ~/your-workspace/{project_name}
   ```

2. **의존성 설치**:
   ```bash
   npm install
   ```

3. **개발 서버 시작**:
   ```bash
   npm run dev
   ```

4. **GitHub 연결**:
   ```bash
   git remote add origin https://github.com/semicolon-devteam/{project_name}.git
   git push -u origin main
   ```

### 📚 참고 문서

- [Team Codex](https://github.com/semicolon-devteam/docs/wiki/Team-Codex)
- [CLAUDE.md](implement-dist/{project_name}/CLAUDE.md)

---

⚠️ `implement-dist/` 폴더는 임시 출력 폴더입니다.
필요한 위치로 복사 후 삭제해도 됩니다.
```

## Clean Up

After user copies the project:

```bash
# Optional: Clean up implement-dist
rm -rf implement-dist/{project_name}

# Or clean all
rm -rf implement-dist/*
```

## Dependencies

- `scripts/create-service.sh` - Core generation script
- `templates/CLAUDE.template.md` - CLAUDE.md template
- `templates/README.template.md` - README.md template
