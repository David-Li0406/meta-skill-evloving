---
name: classting-token
description: Classting 서비스의 access_token을 획득합니다. ai.classting.net에 접속하여 OIDC 로그인 후 JWT 토큰을 반환합니다. Classting API 호출, e2e 테스트, 인증이 필요한 작업 시 사용합니다.
compatibility: Chrome browser required, Chrome DevTools MCP server connection required
---

# Classting Token

Classting 서비스의 access_token을 Chrome MCP를 통해 획득합니다.

## When to Use This Skill

**Proactively use this skill when:**
- Classting API 호출이 필요한데 인증 토큰이 없을 때
- e2e 테스트에서 인증된 사용자 세션이 필요할 때
- 사용자가 "Classting 토큰", "access_token" 획득을 요청할 때
- minerva-api, ai-web 테스트 시 인증이 필요할 때

**DO NOT use when:**
- 이미 유효한 토큰이 있을 때
- Chrome MCP가 연결되지 않았을 때

## Instructions

### 1. Collect Credentials

AskUserQuestion 도구로 인증 정보 수집:
- 이메일 주소
- 비밀번호

### 2. Navigate to ai.classting.net

```
mcp__chrome-devtools__navigate_page:
  type: url
  url: https://ai.classting.net
```

로그인 페이지로 리디렉션됨 (accounts.classting.net)

### 3. Take Snapshot and Locate Login Button

```
mcp__chrome-devtools__take_snapshot
```

"Sign in with Email" 버튼 uid 확인

### 4. Click Email Login

```
mcp__chrome-devtools__click:
  uid: <email_login_button_uid>
```

### 5. Fill Credentials

```
mcp__chrome-devtools__fill_form:
  elements:
    - uid: <email_field_uid>
      value: <user_email>
    - uid: <password_field_uid>
      value: <user_password>
```

### 6. Submit Login

```
mcp__chrome-devtools__click:
  uid: <signin_button_uid>
```

### 7. Wait for Redirect

페이지가 ai.classting.net/home으로 리디렉션될 때까지 대기

### 8. Extract Token from Network Requests

```
mcp__chrome-devtools__list_network_requests:
  resourceTypes: ["fetch", "xhr"]
  pageSize: 30
```

`/oidc/token` 요청 찾기

### 9. Get Token Details

```
mcp__chrome-devtools__get_network_request:
  reqid: <token_request_id>
```

Response Body에서 access_token 추출

### 10. Output Token

access_token 값만 출력:
```
<access_token_value>
```

## Error Handling

- **Chrome MCP 미연결**: "Chrome MCP가 연결되지 않았습니다. /chrome 명령으로 연결해주세요."
- **로그인 실패**: "로그인에 실패했습니다. 이메일과 비밀번호를 확인해주세요."
- **토큰 없음**: "토큰을 찾을 수 없습니다. 페이지를 새로고침 후 다시 시도해주세요."
- **2FA/CAPTCHA**: "추가 인증이 필요합니다. 브라우저에서 직접 완료해주세요."

## Notes

- 토큰 유효기간: access_token은 15분 (900초)
- 필요 시 refresh_token으로 갱신 가능
- Chrome 브라우저가 열려 있어야 함
