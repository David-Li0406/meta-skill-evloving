---
name: smart-push
description: Use this skill when you need to analyze changes, generate appropriate commit messages, and securely push to a remote repository.
---

# 스마트 푸시 워크플로우

1. **커밋 메시지 제안**: 분석한 내용을 바탕으로 '타입(범위): 내용' 형식의 메시지를 제안합니다.
2. **보안 점검**: 푸시될 파일 중에 민감한 정보(비밀번호 등)가 포함되어 있는지 마지막으로 체크합니다.
3. **버전 관리 명령 실행**: `git add .`, `git commit`, `git push origin main`을 순차적으로 실행합니다.

## 실행 가이드
1. 사용자가 푸시해줘 요청하면 이 지침을 따릅니다.