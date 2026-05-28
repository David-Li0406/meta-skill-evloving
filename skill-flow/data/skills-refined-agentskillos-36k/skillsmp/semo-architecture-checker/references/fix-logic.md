# Fix Logic

> install-sax.sh와 동일한 로직으로 .claude 구조 수정

## 🔴 Windows 환경 지원

> **Windows에서는 심링크 생성에 관리자 권한 또는 개발자 모드가 필요합니다.**
> 심링크 실패 시 자동으로 파일/디렉토리 복사로 폴백합니다.

### OS 감지

```bash
detect_os() {
  case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*) echo "windows" ;;
    Darwin) echo "macos" ;;
    Linux) echo "linux" ;;
    *) echo "unknown" ;;
  esac
}

OS=$(detect_os)
```

### 심링크 생성 (폴백 포함)

```bash
# 심링크 시도, 실패 시 복사로 폴백
# 반환값: 0=심링크 성공, 1=복사로 대체
SYMLINK_FALLBACK_USED=false

create_link_or_copy() {
  local target=$1
  local link_path=$2

  # 기존 파일/심링크 제거
  rm -rf "$link_path"

  # 심링크 시도
  if ln -s "$target" "$link_path" 2>/dev/null; then
    return 0
  fi

  # 실패 시 파일/디렉토리 복사
  if [ -d "$(dirname "$link_path")/$target" ]; then
    cp -r "$(dirname "$link_path")/$target" "$link_path"
  elif [ -f "$(dirname "$link_path")/$target" ]; then
    cp "$(dirname "$link_path")/$target" "$link_path"
  else
    echo "  ❌ 대상 없음: $target"
    return 2
  fi

  SYMLINK_FALLBACK_USED=true
  echo "  ⚠️ 심링크 실패 → 복사로 대체: $(basename "$link_path")"
  return 1
}
```

### 폴백 사용 시 안내 메시지

```bash
print_fallback_warning() {
  if [ "$SYMLINK_FALLBACK_USED" = true ]; then
    echo ""
    echo "⚠️ **Windows 환경 알림**"
    echo ""
    echo "일부 심링크가 파일 복사로 대체되었습니다."
    echo "원본 파일 수정 시 수동으로 다시 설치해야 합니다:"
    echo "\`\`\`"
    echo "./install-sax.sh {패키지} --force"
    echo "\`\`\`"
    echo ""
    echo "심링크를 사용하려면:"
    echo "1. Windows 설정 → 개발자용 → 개발자 모드 활성화"
    echo "2. 또는 관리자 권한으로 터미널 실행"
  fi
}
```

## 패키지 감지

```bash
detect_packages() {
  local pkgs=()
  for pkg in po next qa meta pm backend infra design; do
    [ -d ".claude/semo-$pkg" ] && pkgs+=("$pkg")
  done
  echo "${pkgs[@]}"
}

detect_package() {
  local pkgs=($(detect_packages))
  if [ ${#pkgs[@]} -gt 0 ]; then
    echo "${pkgs[0]}"
  else
    echo "unknown"
  fi
}

# 다중 패키지 감지
check_multiple_packages() {
  local pkgs=($(detect_packages))
  if [ ${#pkgs[@]} -gt 1 ]; then
    echo "🔴 **다중 패키지 설치 감지**"
    echo ""
    echo "설치된 패키지: ${pkgs[*]}"
    echo ""
    echo "⚠️ 하나의 프로젝트에는 하나의 SEMO 패키지만 권장됩니다."
    echo "충돌로 인해 일부 기능이 정상 동작하지 않을 수 있습니다."
    echo ""
    echo "**해결 방법**: \`./install-sax.sh {원하는패키지} --force\`"
    return 1
  fi
  return 0
}

PKG=$(detect_package)
```

## CLAUDE.md 수정

```bash
fix_claude_md() {
  local pkg=$1

  cd .claude

  # create_link_or_copy 사용 (심링크 또는 복사)
  create_link_or_copy "semo-$pkg/CLAUDE.md" "CLAUDE.md"
  local result=$?

  cd ..

  if [ $result -eq 0 ]; then
    echo "Fixed: CLAUDE.md -> semo-$pkg/CLAUDE.md (symlink)"
  elif [ $result -eq 1 ]; then
    echo "Fixed: CLAUDE.md (copied from semo-$pkg/CLAUDE.md)"
  else
    echo "Error: CLAUDE.md 생성 실패"
  fi
}
```

## 🔴 중첩 심링크 처리 (핵심)

> **문제**: `.claude/skills`가 `semo-{pkg}/skills`로 심링크된 경우, 그 안에 생성하는 심링크 경로가 꼬임
>
> **해결**: 심링크 디렉토리를 실제 디렉토리로 교체 후 병합

```bash
ensure_real_directory() {
  local dir_path=$1  # e.g., ".claude/skills"

  # 심링크인 경우 → 실제 디렉토리로 교체
  if [ -L "$dir_path" ]; then
    echo "  ⚠️ $dir_path is symlink, converting to real directory"
    rm -f "$dir_path"
    mkdir -p "$dir_path"
  elif [ ! -d "$dir_path" ]; then
    mkdir -p "$dir_path"
  fi
}
```

## 병합 디렉토리 수정 (agents/, skills/)

```bash
fix_merged_dir() {
  local dir_type=$1  # agents or skills
  local pkg=$2

  # 🔴 심링크 → 실제 디렉토리 변환
  ensure_real_directory ".claude/$dir_type"

  # .merged 마커 생성
  touch ".claude/$dir_type/.merged"

  # 기존 심링크 모두 제거 (클린 슬레이트)
  find ".claude/$dir_type" -maxdepth 1 -type l -delete

  # 1. semo-core 심링크 (기본 레이어)
  if [ -d ".claude/semo-core/$dir_type" ]; then
    cd ".claude/$dir_type"
    for item in ../semo-core/$dir_type/*/; do
      if [ -d "$item" ]; then
        local name=$(basename "$item")
        create_link_or_copy "../semo-core/$dir_type/$name" "$name"
        echo "  [core] $name"
      fi
    done
    cd ../..
  fi

  # 2. semo-{pkg} 심링크 (우선 레이어, 덮어쓰기)
  if [ -d ".claude/semo-$pkg/$dir_type" ]; then
    cd ".claude/$dir_type"
    for item in ../semo-$pkg/$dir_type/*/; do
      if [ -d "$item" ]; then
        local name=$(basename "$item")
        # core 것이 있으면 제거 (패키지 우선)
        rm -rf "$name"
        create_link_or_copy "../semo-$pkg/$dir_type/$name" "$name"
        echo "  [pkg] $name"
      fi
    done
    cd ../..
  fi

  # 3. 🔴 검증: 심링크 실제 접근 가능 여부 확인
  local broken=0
  for link in .claude/$dir_type/*/; do
    if [ -L "${link%/}" ] && [ ! -e "${link%/}" ]; then
      echo "  ❌ BROKEN: ${link%/}"
      broken=$((broken + 1))
    fi
  done

  if [ $broken -gt 0 ]; then
    echo "  ⚠️ $broken broken symlinks detected"
  fi
}
```

## commands/SEMO 수정

```bash
fix_commands() {
  local pkg=$1

  # 🔴 심링크 → 실제 디렉토리 변환
  ensure_real_directory ".claude/commands"
  ensure_real_directory ".claude/commands/SEMO"

  # .merged 마커 생성
  touch ".claude/commands/SEMO/.merged"

  # 기존 심링크 모두 제거
  find ".claude/commands/SEMO" -maxdepth 1 -type l -delete

  # 1. semo-core 커맨드 심링크
  if [ -d ".claude/semo-core/commands/SEMO" ]; then
    cd ".claude/commands/SEMO"
    for item in ../../semo-core/commands/SEMO/*.md; do
      if [ -f "$item" ]; then
        local name=$(basename "$item")
        create_link_or_copy "../../semo-core/commands/SEMO/$name" "$name"
        echo "  [core] $name"
      fi
    done
    cd ../../..
  fi

  # 2. semo-{pkg} 커맨드 심링크 (우선)
  if [ -d ".claude/semo-$pkg/commands/SEMO" ]; then
    cd ".claude/commands/SEMO"
    for item in ../../semo-$pkg/commands/SEMO/*.md; do
      if [ -f "$item" ]; then
        local name=$(basename "$item")
        rm -rf "$name"
        create_link_or_copy "../../semo-$pkg/commands/SEMO/$name" "$name"
        echo "  [pkg] $name"
      fi
    done
    cd ../../..
  fi

  # 3. 🔴 검증: 심링크 실제 접근 가능 여부 확인
  local broken=0
  for link in .claude/commands/SEMO/*.md; do
    if [ -L "$link" ] && [ ! -e "$link" ]; then
      echo "  ❌ BROKEN: $link"
      broken=$((broken + 1))
    fi
  done

  if [ $broken -gt 0 ]; then
    echo "  ⚠️ $broken broken symlinks detected"
  fi
}
```

## 전체 수정 실행

```bash
run_fix() {
  # 다중 패키지 체크 (최우선)
  check_multiple_packages
  local multi_pkg_status=$?

  local pkg=$(detect_package)

  if [ "$pkg" = "unknown" ]; then
    echo "Error: SEMO 패키지를 찾을 수 없습니다"
    return 1
  fi

  echo "패키지: semo-$pkg"
  echo ""

  if [ $multi_pkg_status -ne 0 ]; then
    echo "⚠️ 다중 패키지 감지됨 - 첫 번째 패키지($pkg)로 수정 진행"
    echo ""
  fi

  echo "=== CLAUDE.md 수정 ==="
  fix_claude_md "$pkg"
  echo ""

  echo "=== agents/ 수정 ==="
  fix_merged_dir "agents" "$pkg"
  echo ""

  echo "=== skills/ 수정 ==="
  fix_merged_dir "skills" "$pkg"
  echo ""

  echo "=== commands/SEMO/ 수정 ==="
  fix_commands "$pkg"
  echo ""

  echo "완료!"

  if [ $multi_pkg_status -ne 0 ]; then
    echo ""
    echo "⚠️ 다중 패키지 문제 해결을 위해 \`./install-sax.sh $pkg --force\` 실행을 권장합니다."
  fi

  # Windows 폴백 사용 시 안내
  print_fallback_warning
}
```

## 심링크 경로 규칙

| 대상 | 심링크 경로 | 비고 |
|------|-------------|------|
| CLAUDE.md | `semo-{pkg}/CLAUDE.md` | 직접 심링크 |
| agents/{name} | `../semo-{core|pkg}/agents/{name}` | 실제 디렉토리 내 심링크 |
| skills/{name} | `../semo-{core|pkg}/skills/{name}` | 실제 디렉토리 내 심링크 |
| commands/SEMO/{name}.md | `../../semo-{core|pkg}/commands/SEMO/{name}.md` | 실제 디렉토리 내 심링크 |

## 🔴 중첩 심링크 문제 해결

### 문제 상황

```text
.claude/
├── skills → semo-next/skills (심링크)  ← 문제!
├── semo-core/
└── semo-next/
```

기존 방식에서 semo-core 심링크 생성 시:

```bash
ln -s "../semo-core/skills/feedback" ".claude/skills/feedback"
```

경로 해석:

```text
.claude/skills/feedback
→ semo-next/skills/feedback (1단계 심링크)
→ semo-next/skills/../semo-core/skills/feedback
→ semo-next/semo-core/skills/feedback (존재하지 않음!)
```

### 해결 방법

**심링크 디렉토리를 실제 디렉토리로 교체**:

```bash
# 심링크인 경우 삭제 후 실제 디렉토리 생성
if [ -L ".claude/skills" ]; then
  rm -f ".claude/skills"
  mkdir -p ".claude/skills"
fi
```

교체 후 구조:

```text
.claude/
├── skills/  (실제 디렉토리)
│   ├── feedback → ../semo-core/skills/feedback
│   ├── notify-slack → ../semo-core/skills/notify-slack
│   └── ... (semo-pkg skills)
├── semo-core/
└── semo-next/
```

## 병합 우선순위

1. **기본 (semo-core)**: 공통 컴포넌트
2. **우선 (semo-{pkg})**: 패키지별 컴포넌트 (동일 이름이면 덮어쓰기)

## 🔴 누락 심링크 감지 (NEW - Issue #7 대응)

> **문제**: 패키지 업데이트 후 새로 추가된 스킬/에이전트/커맨드의 심링크가 생성되지 않음
>
> **해결**: 소스 디렉토리와 병합 디렉토리를 비교하여 누락된 심링크 자동 감지 및 생성

### 누락 감지 로직

```bash
# 누락된 심링크 감지 함수
# 반환: 누락된 컴포넌트 목록 (newline 구분)
detect_missing_symlinks() {
  local dir_type=$1  # agents, skills
  local pkg=$2
  local missing=""

  # 1. semo-core에서 누락된 것 찾기
  if [ -d ".claude/semo-core/$dir_type" ]; then
    for item in .claude/semo-core/$dir_type/*/; do
      if [ -d "$item" ]; then
        local name=$(basename "$item")
        local target=".claude/$dir_type/$name"

        # 병합 디렉토리에 없으면 누락
        if [ ! -e "$target" ] && [ ! -L "$target" ]; then
          missing="$missing[core] $name\n"
        fi
      fi
    done
  fi

  # 2. semo-{pkg}에서 누락된 것 찾기
  if [ -d ".claude/semo-$pkg/$dir_type" ]; then
    for item in .claude/semo-$pkg/$dir_type/*/; do
      if [ -d "$item" ]; then
        local name=$(basename "$item")
        local target=".claude/$dir_type/$name"

        # 병합 디렉토리에 없으면 누락
        if [ ! -e "$target" ] && [ ! -L "$target" ]; then
          missing="$missing[pkg] $name\n"
        fi
      fi
    done
  fi

  echo -e "$missing"
}

# commands/SEMO 누락 감지
detect_missing_commands() {
  local pkg=$1
  local missing=""

  # 1. semo-core 커맨드 누락 확인
  if [ -d ".claude/semo-core/commands/SEMO" ]; then
    for item in .claude/semo-core/commands/SEMO/*.md; do
      if [ -f "$item" ]; then
        local name=$(basename "$item")
        local target=".claude/commands/SEMO/$name"

        if [ ! -e "$target" ] && [ ! -L "$target" ]; then
          missing="$missing[core] $name\n"
        fi
      fi
    done
  fi

  # 2. semo-{pkg} 커맨드 누락 확인
  if [ -d ".claude/semo-$pkg/commands/SEMO" ]; then
    for item in .claude/semo-$pkg/commands/SEMO/*.md; do
      if [ -f "$item" ]; then
        local name=$(basename "$item")
        local target=".claude/commands/SEMO/$name"

        if [ ! -e "$target" ] && [ ! -L "$target" ]; then
          missing="$missing[pkg] $name\n"
        fi
      fi
    done
  fi

  echo -e "$missing"
}
```

### 누락 심링크 자동 생성

```bash
# 누락된 심링크만 생성 (기존 것 유지)
fix_missing_symlinks() {
  local dir_type=$1  # agents, skills
  local pkg=$2
  local added=0

  echo "=== $dir_type/ 누락 심링크 확인 ==="

  # 병합 디렉토리 확인/생성
  ensure_real_directory ".claude/$dir_type"
  [ ! -f ".claude/$dir_type/.merged" ] && touch ".claude/$dir_type/.merged"

  # 1. semo-core 누락 심링크 생성
  if [ -d ".claude/semo-core/$dir_type" ]; then
    for item in .claude/semo-core/$dir_type/*/; do
      if [ -d "$item" ]; then
        local name=$(basename "$item")
        local target=".claude/$dir_type/$name"

        # 없으면 생성
        if [ ! -e "$target" ] && [ ! -L "$target" ]; then
          cd ".claude/$dir_type"
          create_link_or_copy "../semo-core/$dir_type/$name" "$name"
          echo "  ✅ [core] $name 추가됨"
          cd ../..
          added=$((added + 1))
        fi
      fi
    done
  fi

  # 2. semo-{pkg} 누락 심링크 생성 (우선 적용)
  if [ -d ".claude/semo-$pkg/$dir_type" ]; then
    for item in .claude/semo-$pkg/$dir_type/*/; do
      if [ -d "$item" ]; then
        local name=$(basename "$item")
        local target=".claude/$dir_type/$name"

        # 없으면 생성
        if [ ! -e "$target" ] && [ ! -L "$target" ]; then
          cd ".claude/$dir_type"
          create_link_or_copy "../semo-$pkg/$dir_type/$name" "$name"
          echo "  ✅ [pkg] $name 추가됨"
          cd ../..
          added=$((added + 1))
        fi
      fi
    done
  fi

  if [ $added -eq 0 ]; then
    echo "  (누락 없음)"
  else
    echo "  → $added개 심링크 추가됨"
  fi

  return $added
}

# commands/SEMO 누락 심링크 생성
fix_missing_commands() {
  local pkg=$1
  local added=0

  echo "=== commands/SEMO/ 누락 심링크 확인 ==="

  # 병합 디렉토리 확인/생성
  ensure_real_directory ".claude/commands"
  ensure_real_directory ".claude/commands/SEMO"
  [ ! -f ".claude/commands/SEMO/.merged" ] && touch ".claude/commands/SEMO/.merged"

  # 1. semo-core 커맨드 누락 생성
  if [ -d ".claude/semo-core/commands/SEMO" ]; then
    for item in .claude/semo-core/commands/SEMO/*.md; do
      if [ -f "$item" ]; then
        local name=$(basename "$item")
        local target=".claude/commands/SEMO/$name"

        if [ ! -e "$target" ] && [ ! -L "$target" ]; then
          cd ".claude/commands/SEMO"
          create_link_or_copy "../../semo-core/commands/SEMO/$name" "$name"
          echo "  ✅ [core] $name 추가됨"
          cd ../../..
          added=$((added + 1))
        fi
      fi
    done
  fi

  # 2. semo-{pkg} 커맨드 누락 생성
  if [ -d ".claude/semo-$pkg/commands/SEMO" ]; then
    for item in .claude/semo-$pkg/commands/SEMO/*.md; do
      if [ -f "$item" ]; then
        local name=$(basename "$item")
        local target=".claude/commands/SEMO/$name"

        if [ ! -e "$target" ] && [ ! -L "$target" ]; then
          cd ".claude/commands/SEMO"
          create_link_or_copy "../../semo-$pkg/commands/SEMO/$name" "$name"
          echo "  ✅ [pkg] $name 추가됨"
          cd ../../..
          added=$((added + 1))
        fi
      fi
    done
  fi

  if [ $added -eq 0 ]; then
    echo "  (누락 없음)"
  else
    echo "  → $added개 심링크 추가됨"
  fi

  return $added
}
```

### 통합 누락 체크 및 수정

```bash
# 전체 누락 심링크 체크 및 수정
# --check-only 모드: 감지만 수행, 수정 안함
# 기본 모드: 감지 + 자동 수정
run_missing_check() {
  local pkg=$(detect_package)
  local check_only=${1:-false}
  local total_missing=0
  local total_added=0

  echo ""
  echo "## 누락 심링크 검사"
  echo ""

  # agents 누락 확인
  local agents_missing=$(detect_missing_symlinks "agents" "$pkg")
  if [ -n "$agents_missing" ]; then
    echo "### agents/ 누락 발견:"
    echo -e "$agents_missing"
    total_missing=$((total_missing + $(echo -e "$agents_missing" | grep -c '\[' || echo 0)))
  fi

  # skills 누락 확인
  local skills_missing=$(detect_missing_symlinks "skills" "$pkg")
  if [ -n "$skills_missing" ]; then
    echo "### skills/ 누락 발견:"
    echo -e "$skills_missing"
    total_missing=$((total_missing + $(echo -e "$skills_missing" | grep -c '\[' || echo 0)))
  fi

  # commands 누락 확인
  local commands_missing=$(detect_missing_commands "$pkg")
  if [ -n "$commands_missing" ]; then
    echo "### commands/SEMO/ 누락 발견:"
    echo -e "$commands_missing"
    total_missing=$((total_missing + $(echo -e "$commands_missing" | grep -c '\[' || echo 0)))
  fi

  if [ $total_missing -eq 0 ]; then
    echo "✅ 모든 심링크가 동기화되어 있습니다."
    return 0
  fi

  echo ""
  echo "**총 $total_missing개 누락 발견**"

  # --check-only 모드면 여기서 종료
  if [ "$check_only" = true ]; then
    echo ""
    echo "**결과**: ⚠️ 누락 발견 (자동 수정 필요)"
    return 1
  fi

  # 자동 수정 실행
  echo ""
  echo "## 자동 수정 실행"
  echo ""

  fix_missing_symlinks "agents" "$pkg"
  total_added=$((total_added + $?))

  fix_missing_symlinks "skills" "$pkg"
  total_added=$((total_added + $?))

  fix_missing_commands "$pkg"
  total_added=$((total_added + $?))

  echo ""
  echo "✅ $total_added개 심링크가 추가되었습니다."

  # 심링크 변경 시 세션 재시작 권장
  if [ $total_added -gt 0 ]; then
    echo ""
    echo "⚠️ **세션 재시작 권장**"
    echo ""
    echo "새 스킬/에이전트가 추가되었습니다."
    echo "Claude Code가 변경된 경로를 인식하도록 **새 세션을 시작**하는 것을 권장합니다."
  fi

  return 0
}
```

### --check-only 모드 출력 형식

```markdown
[SEMO] Skill: semo-architecture-checker --check-only 실행

## 구조 검증 결과

| 항목 | 상태 | 비고 |
|------|------|------|
| semo-core | ✅ | 존재 |
| semo-{pkg} | ✅ | semo-po |
| CLAUDE.md | ✅ | 심링크 유효 |
| agents/ | ✅ | 5 symlinks |
| skills/ | ⚠️ | 누락 1개 (list-bugs) |
| commands/SEMO | ✅ | 6 symlinks |

**결과**: ⚠️ 문제 발견 (자동 수정 필요)
```

### 기본 모드 출력 형식

```markdown
[SEMO] Skill: semo-architecture-checker 실행

## .claude 디렉토리 검증 결과

| 항목 | 상태 | 비고 |
|------|------|------|
| 패키지 | ✅ | semo-po |
| CLAUDE.md | ✅ | semo-po/CLAUDE.md |
| agents/ | ✅ | 5 symlinks |
| skills/ | ⚠️ → ✅ | 1개 심링크 추가 (list-bugs) |
| commands/SEMO | ✅ | 6 symlinks |

**결과**: 1개 항목 자동 수정됨

⚠️ **세션 재시작 권장**

새 스킬/에이전트가 추가되었습니다.
Claude Code가 변경된 경로를 인식하도록 **새 세션을 시작**하는 것을 권장합니다.
```
