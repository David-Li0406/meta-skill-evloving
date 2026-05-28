---
name: package-deploy
description: SEMO 패키지를 외부 프로젝트에 배포. Use when (1) 새 프로젝트에 SEMO 설치, (2) 기존 프로젝트 SEMO 업데이트, (3) 브라운필드 프로젝트 SEMO 도입.
tools: [Bash, Read, Grep]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: package-deploy 호출 - {패키지} → {대상}` 시스템 메시지를 첫 줄에 출력하세요.

# package-deploy Skill

> SEMO 패키지를 외부 프로젝트에 배포하는 자동화 Skill
>
> **SoT 참조**: 패키징 규칙은 `semo-core/PACKAGING.md`에서 관리됩니다.

## Purpose

`sax/packages/{package}/`를 외부 프로젝트의 `.claude/` 디렉토리에 배포합니다.

## Quick Start

```bash
# 방법 1: install-sax.sh 스크립트 사용 (권장)
./install-sax.sh next

# 방법 2: 업데이트 모드
./install-sax.sh next --update

# 방법 3: 수동 배포
mkdir -p /path/to/project/.claude/agents
mkdir -p /path/to/project/.claude/skills
cp -r sax/packages/semo-next/agents/* /path/to/project/.claude/agents/
cp -r sax/packages/semo-next/skills/* /path/to/project/.claude/skills/
```

## Windows 지원

> Windows 환경에서는 심링크 대신 **직접 복사** 방식을 사용합니다.

### OS 자동 감지

install-sax.sh가 OS를 자동 감지하여 적절한 방식을 선택합니다:

- **Linux/macOS**: 심링크 사용
- **Windows** (Git Bash, MSYS, Cygwin): 복사 사용

### Windows 업데이트 주의사항

Windows 복사 모드에서는 원본 업데이트 후 복사본 갱신이 필요합니다:

```bash
# 원본 업데이트
git submodule update --remote

# 복사본 갱신
./install-sax.sh next --update
```

## Supported Packages

| 패키지 | 대상 프로젝트 | 용도 |
|--------|-------------|------|
| semo-core | command-center | 공통 규칙 |
| semo-po | cm-template | PO/기획자 지원 |
| semo-next | cm-template, cm-* | Next.js 개발 |
| semo-qa | cm-template | QA 테스트 |
| semo-pm | 모든 프로젝트 | PM/프로젝트 관리 |
| semo-backend | core-backend | 백엔드 개발 |
| semo-infra | 인프라 프로젝트 | DevOps/인프라 |
| semo-design | 디자인 프로젝트 | UI/UX 디자인 |
| semo-ms | ms-* | 마이크로서비스 개발 |

## Deployment Options

| 옵션 | 설명 | 사용 시점 |
|------|------|----------|
| 기본 | 전체 덮어쓰기 | 신규 설치 |
| `--update` | 버전 비교 후 업데이트 | 기존 설치 업데이트 |

## SEMO Message

```markdown
[SEMO] Skill: package-deploy 실행

[SEMO] Deploy: {package} → {target_path} 배포 완료 (v{version})
```

## Related

- [package-sync Skill](../package-sync/SKILL.md) - docs 내부 동기화
- [version-manager Skill](../version-manager/SKILL.md) - 버저닝
- [install-sax.sh Script](../../scripts/install-sax.sh) - 설치/배포 스크립트

## References

For detailed documentation, see:

- [Deploy Workflow](references/deploy-workflow.md) - 배포 프로세스 상세
- [Target Setup](references/target-setup.md) - 대상 프로젝트 설정
- [Output Format](references/output-format.md) - 성공/실패 출력 형식
