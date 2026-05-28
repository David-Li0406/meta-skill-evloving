# Output Format

> version-manager의 출력 형식 및 Edge Cases

## 성공 시

```json
{
  "status": "✅ SUCCESS",
  "old_version": "3.7.0",
  "new_version": "3.8.0",
  "version_type": "minor",
  "files_created": [
    "sax/CHANGELOG/3.8.0.md"
  ],
  "files_updated": [
    "sax/VERSION",
    "sax/CHANGELOG/INDEX.md"
  ],
  "summary": {
    "added": 4,
    "changed": 0,
    "removed": 2,
    "fixed": 0
  },
  "next_steps": [
    ".claude/ 동기화 (SEMO-PO만)",
    "git commit -m '📝 [SEMO] v3.8.0'"
  ]
}
```

## 실패 시

```json
{
  "status": "❌ FAIL",
  "error": "VERSION 파일을 찾을 수 없습니다",
  "current_version": null
}
```

## Edge Cases

### 동일 버전 재생성

**시나리오**: 3.8.0이 이미 존재하는데 3.8.0 재생성 요청

**처리**:
- ❌ 에러 반환: "버전 3.8.0이 이미 존재합니다"
- 해결 방법: PATCH 버전으로 변경 (3.8.1) 또는 기존 파일 수동 삭제

### 빈 변경사항

**시나리오**: changes 배열이 빈 상태

**처리**:
- ❌ 에러 반환: "변경사항이 없습니다"
- 버저닝 중단

### VERSION 파일 없음

**시나리오**: sax/VERSION 파일이 존재하지 않음

**처리**:
- ❌ 에러 반환: "VERSION 파일을 찾을 수 없습니다"
- 해결 방법: VERSION 파일 생성 후 재시도

### CHANGELOG 디렉토리 없음

**시나리오**: sax/CHANGELOG/ 디렉토리가 존재하지 않음

**처리**:
- ⚠️ 경고 후 자동 생성
- 또는 에러 반환 후 수동 생성 요청

## Error Types

| Error | 설명 | 해결 방법 |
|-------|------|----------|
| VERSION_NOT_FOUND | VERSION 파일 없음 | 파일 생성 |
| CHANGELOG_DIR_NOT_FOUND | CHANGELOG 디렉토리 없음 | 디렉토리 생성 |
| VERSION_EXISTS | 버전 이미 존재 | 다른 버전 사용 |
| EMPTY_CHANGES | 변경사항 없음 | 변경사항 추가 |
| INVALID_VERSION_FORMAT | 버전 형식 오류 | x.y.z 형식 사용 |
