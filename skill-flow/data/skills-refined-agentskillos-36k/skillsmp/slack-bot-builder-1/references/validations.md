# Slack Bot Builder - Validations

## Hardcoded Slack Token

### **Id**
hardcoded-token
### **Severity**
error
### **Description**
Slack tokens must never be hardcoded
### **Pattern**
  (xoxb-[0-9]+-[0-9A-Za-z]+|xoxp-[0-9]+-[0-9]+-[0-9A-Za-z]+|xapp-[0-9]+-[A-Za-z0-9]+)
  
### **Message**
Hardcoded Slack token detected. Use environment variables.
### **Autofix**


## Signing Secret in Source Code

### **Id**
signing-secret-in-code
### **Severity**
error
### **Description**
Signing secrets should be in environment variables
### **Pattern**
  signing_secret\s*=\s*["'][a-f0-9]{32}["']
  
### **Message**
Hardcoded signing secret. Use os.environ['SLACK_SIGNING_SECRET'].
### **Autofix**


## Webhook Without Signature Verification

### **Id**
no-signature-verification
### **Severity**
error
### **Description**
Slack webhooks must verify X-Slack-Signature
### **Pattern**
  @app\.route.*slack|/slack/events|/slack/commands
  
### **Anti Pattern**
  (verify.*signature|X-Slack-Signature|signing_secret|SlackRequestHandler)
  
### **Message**
Webhook without signature verification. Use Bolt or verify manually.
### **Autofix**


## Slack Token in Client-Side Code

### **Id**
token-in-frontend
### **Severity**
error
### **Description**
Never expose Slack tokens to browsers
### **Pattern**
  (window\.|document\.|localStorage\.|export\s+const).*SLACK.*(TOKEN|SECRET)
  
### **Message**
Slack credentials exposed client-side. Only use server-side.
### **Autofix**


## Slow Operation Before Acknowledgment

### **Id**
slow-before-ack
### **Severity**
warning
### **Description**
ack() must be called before slow operations
### **Pattern**
  @app\.(command|action|shortcut|view).*\n.*(?:requests\.|httpx\.|aiohttp\.|fetch\(|client\.)
  
### **Anti Pattern**
  ack\(\).*\n.*(?:requests\.|httpx\.)
  
### **Message**
Slow operation before ack(). Call ack() first, then process.
### **Autofix**


## Missing Acknowledgment Call

### **Id**
missing-ack
### **Severity**
warning
### **Description**
Interactive handlers must call ack()
### **Pattern**
  @app\.(command|action|shortcut|view)\([^)]+\)\s*\ndef\s+\w+\([^)]*\):
  
### **Anti Pattern**
  ack\(
  
### **Message**
Handler missing ack() call. Must acknowledge within 3 seconds.
### **Autofix**


## OAuth Without State Validation

### **Id**
no-state-validation
### **Severity**
error
### **Description**
OAuth callback must validate state parameter
### **Pattern**
  oauth.*callback|/slack/oauth
  
### **Anti Pattern**
  (state|StateStore|verify.*state)
  
### **Message**
OAuth without state validation. Vulnerable to CSRF attacks.
### **Autofix**


## Token Storage Without Encryption

### **Id**
token-not-encrypted
### **Severity**
warning
### **Description**
Tokens should be encrypted at rest
### **Pattern**
  (INSERT|UPDATE).*token.*VALUES
  
### **Anti Pattern**
  (encrypt|cipher|fernet|aes)
  
### **Message**
Token stored without encryption. Encrypt tokens at rest.
### **Autofix**


## Requesting Admin Scopes

### **Id**
over-scoped-request
### **Severity**
warning
### **Description**
Avoid admin scopes unless absolutely necessary
### **Pattern**
  scopes.*admin\.|admin\.\w+.*scope
  
### **Message**
Requesting admin scope. Use minimal required scopes.
### **Autofix**


## Potentially Unused Scope

### **Id**
unused-scope
### **Severity**
info
### **Description**
Check if all requested scopes are used
### **Pattern**
  users:read\.email
  
### **Anti Pattern**
  (email|profile\.email)
  
### **Message**
Requesting users:read.email but may not use email. Verify necessity.
### **Autofix**


## Blocks Not Validated Before Sending

### **Id**
unvalidated-blocks
### **Severity**
info
### **Description**
Validate Block Kit JSON before sending
### **Pattern**
  chat_postMessage\(.*blocks=
  
### **Anti Pattern**
  (validate.*blocks|BlockKit|check.*blocks)
  
### **Message**
Consider validating blocks before sending to catch limit errors.
### **Autofix**


## Potentially Long Text Block

### **Id**
long-text-block
### **Severity**
info
### **Description**
Text blocks limited to 3000 characters
### **Pattern**
  "type":\s*"section".*"text":\s*\{.*"text":\s*[^}]{200,}
  
### **Message**
Long text in section block. Limit is 3000 characters.
### **Autofix**


## No Rate Limit Handling

### **Id**
no-rate-limit-handling
### **Severity**
warning
### **Description**
Handle Slack API rate limits with exponential backoff
### **Pattern**
  (chat_postMessage|conversations\.|files\.upload)
  
### **Anti Pattern**
  (rate.*limit|Retry-After|backoff|sleep.*429)
  
### **Message**
No rate limit handling. Implement exponential backoff.
### **Autofix**


## Socket Mode in Production Config

### **Id**
socket-mode-production
### **Severity**
warning
### **Description**
Socket Mode not recommended for production
### **Pattern**
  SocketModeHandler.*start\(\)
  
### **Anti Pattern**
  (development|dev|test|ENVIRONMENT)
  
### **Message**
Socket Mode in production. Use HTTP webhooks for reliability.
### **Autofix**
