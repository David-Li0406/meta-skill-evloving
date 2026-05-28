# Changelog Format

> version-manager의 Keep a Changelog 템플릿

## CHANGELOG 템플릿

```markdown
# SEMO v{new_version} - {YYYY-MM-DD}

{changes를 Keep a Changelog 형식으로 변환}

### Added

- **{Component Name}** ({Package})
  - {설명}

### Changed

- **{Component Name}** ({Package})
  - {변경 내용}

### Removed

- **{Component Name}** ({Package})
  - {제거 이유}

### Fixed

- **{Component Name}** ({Package})
  - {수정 내용}

### Migration Guide (MAJOR/MINOR만)

**{Package} 사용자**:

1. {변경사항 설명}
2. {마이그레이션 절차}
```

## Migration Guide Generation

MAJOR 또는 MINOR 버전 변경 시, Migration Guide 자동 생성:

```markdown
### Migration Guide

**{영향받는 패키지} 사용자**:

{변경 유형에 따른 가이드}

**Added**:
- 새 기능 사용법 안내

**Changed**:
- 변경된 API 사용법
- 기존 코드 수정 방법

**Removed**:
- 대체 방법 안내
- 마이그레이션 절차
```

## Keep a Changelog 원칙

1. **Guiding Principles**:
   - Changelogs are for humans, not machines
   - There should be an entry for every single version
   - The same types of changes should be grouped

2. **Types of Changes**:
   - `Added` for new features
   - `Changed` for changes in existing functionality
   - `Deprecated` for soon-to-be removed features
   - `Removed` for now removed features
   - `Fixed` for any bug fixes
   - `Security` in case of vulnerabilities

3. **Format**:
   - Date format: YYYY-MM-DD
   - Newest version at top
   - Link to version comparison
