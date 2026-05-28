# Slack Bot Builder - Sharp Edges

## Missing 3-Second Acknowledgment (Timeout)

### **Id**
3-second-acknowledgment
### **Severity**
critical
### **Situation**
Handling slash commands, shortcuts, or interactive components
### **Symptom**
  User sees "This command timed out" or "Something went wrong."
  The action never completes even though your code runs.
  Works in development but fails in production.
  
### **Why**
  Slack requires acknowledgment within 3 seconds for ALL interactive requests:
  - Slash commands
  - Button/select menu clicks
  - Modal submissions
  - Shortcuts
  
  If you do ANY slow operation (database, API call, LLM) before responding,
  you'll miss the window. Slack shows an error even if your bot eventually
  processes the request correctly.
  
### **Solution**
  ## Acknowledge immediately, process later
  
  ```python
  from slack_bolt import App
  from slack_bolt.adapter.socket_mode import SocketModeHandler
  import threading
  
  app = App(token=os.environ["SLACK_BOT_TOKEN"])
  
  @app.command("/slow-task")
  def handle_slow_task(ack, command, client, respond):
      # ACK IMMEDIATELY - before any processing
      ack("Processing your request...")
  
      # Do slow work in background
      def do_work():
          result = call_slow_api(command["text"])  # Takes 10 seconds
          respond(f"Done! Result: {result}")
  
      threading.Thread(target=do_work).start()
  
  @app.view("modal_submission")
  def handle_modal(ack, body, client, view):
      # ACK with response_action for modals
      ack(response_action="clear")  # Or "update" with new view
  
      # Process in background
      user_id = body["user"]["id"]
      values = view["state"]["values"]
      # ... slow processing
  ```
  
  ## For Bolt framework - use lazy listeners
  
  ```python
  # Bolt handles ack() automatically with lazy listeners
  @app.command("/slow-task")
  def handle_slow_task(ack, command, respond):
      ack()  # Still call ack() first!
  
  @handle_slow_task.lazy
  def process_slow_task(command, respond):
      # This runs after ack, can take as long as needed
      result = slow_operation(command["text"])
      respond(result)
  ```
  
### **Detection Pattern**
  - timed out
  - 3 second
  - acknowledge
  - ack

## Not Validating OAuth State Parameter (CSRF)

### **Id**
oauth-state-parameter
### **Severity**
critical
### **Situation**
Implementing OAuth installation flow
### **Symptom**
  Bot appears to work, but you're vulnerable to CSRF attacks.
  Attackers could trick users into installing malicious configurations.
  
### **Why**
  The OAuth state parameter prevents CSRF attacks. Flow:
  1. You generate random state, store it, send to Slack
  2. User authorizes in Slack
  3. Slack redirects back with code + state
  4. You MUST verify state matches what you stored
  
  Without this, an attacker can craft a malicious OAuth URL and trick
  admins into completing the flow with attacker's authorization code.
  
### **Solution**
  ## Proper state validation
  
  ```python
  import secrets
  from flask import Flask, request, session, redirect
  from slack_sdk.oauth import AuthorizeUrlGenerator
  from slack_sdk.oauth.state_store import FileOAuthStateStore
  
  app = Flask(__name__)
  app.secret_key = os.environ["SESSION_SECRET"]
  
  # Use Slack SDK's state store (Redis recommended for production)
  state_store = FileOAuthStateStore(
      expiration_seconds=300,  # 5 minutes
      base_dir="./oauth_states"
  )
  
  @app.route("/slack/install")
  def install():
      # Generate cryptographically secure state
      state = state_store.issue()
  
      # Store in session for verification
      session["oauth_state"] = state
  
      authorize_url = AuthorizeUrlGenerator(
          client_id=os.environ["SLACK_CLIENT_ID"],
          scopes=["channels:history", "chat:write"],
          user_scopes=[]
      ).generate(state)
  
      return redirect(authorize_url)
  
  @app.route("/slack/oauth/callback")
  def oauth_callback():
      # CRITICAL: Verify state
      received_state = request.args.get("state")
      stored_state = session.get("oauth_state")
  
      if not received_state or received_state != stored_state:
          return "Invalid state parameter - possible CSRF attack", 403
  
      # Also use state_store.consume() for one-time use
      if not state_store.consume(received_state):
          return "State already used or expired", 403
  
      # Now safe to exchange code for token
      code = request.args.get("code")
      # ... complete OAuth flow
  ```
  
### **Detection Pattern**
  - state
  - oauth
  - csrf
  - install

## Exposing Bot/User Tokens

### **Id**
token-exposure
### **Severity**
critical
### **Situation**
Storing or logging Slack tokens
### **Symptom**
  Unauthorized messages sent from your bot. Attackers reading private
  channels. Token found in logs, git history, or client-side code.
  
### **Why**
  Slack tokens provide FULL access to whatever scopes they have:
  - Bot tokens (xoxb-*): Access workspaces where installed
  - User tokens (xoxp-*): Access as that specific user
  - App-level tokens (xapp-*): Socket Mode connections
  
  Common exposure points:
  - Hardcoded in source code
  - Logged in error messages
  - Sent to frontend/client
  - Stored in database without encryption
  
### **Solution**
  ## Never hardcode or log tokens
  
  ```python
  # BAD - never do this
  client = WebClient(token="xoxb-12345-...")
  
  # GOOD - environment variables
  client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
  
  # BAD - logging tokens
  logger.error(f"API call failed with token {token}")
  
  # GOOD - never log tokens
  logger.error(f"API call failed for team {team_id}")
  
  # BAD - sending token to frontend
  return {"token": bot_token}
  
  # GOOD - only send what frontend needs
  return {"channels": channel_list}
  ```
  
  ## Encrypt tokens in database
  
  ```python
  from cryptography.fernet import Fernet
  
  class TokenStore:
      def __init__(self, encryption_key: str):
          self.cipher = Fernet(encryption_key)
  
      def save_token(self, team_id: str, token: str):
          encrypted = self.cipher.encrypt(token.encode())
          db.execute(
              "INSERT INTO installations (team_id, encrypted_token) VALUES (?, ?)",
              (team_id, encrypted)
          )
  
      def get_token(self, team_id: str) -> str:
          row = db.execute(
              "SELECT encrypted_token FROM installations WHERE team_id = ?",
              (team_id,)
          ).fetchone()
          return self.cipher.decrypt(row[0]).decode()
  ```
  
  ## Rotate tokens if exposed
  
  ```
  1. Slack API > Your App > OAuth & Permissions
  2. Click "Rotate" for the exposed token
  3. Update all deployments immediately
  4. Review Slack audit logs for unauthorized access
  ```
  
### **Detection Pattern**
  - xoxb-
  - xoxp-
  - xapp-
  - token

## Requesting Unnecessary OAuth Scopes

### **Id**
over-requesting-scopes
### **Severity**
high
### **Situation**
Configuring OAuth scopes for your app
### **Symptom**
  Users hesitate to install due to scary permission warnings.
  Lower install rates. Security team blocks deployment.
  App rejected from Slack App Directory.
  
### **Why**
  Each OAuth scope grants specific permissions. Requesting more than
  you need:
  - Makes install consent screen scary
  - Increases attack surface if token leaked
  - May violate enterprise security policies
  - Can get your app rejected from App Directory
  
  Common over-requests:
  - `admin` when you just need `chat:write`
  - `channels:read` when you only message one channel
  - `users:read.email` when you don't need emails
  
### **Solution**
  ## Request minimum required scopes
  
  ```python
  # For a simple notification bot
  MINIMAL_SCOPES = [
      "chat:write",        # Post messages
      "channels:join",     # Join public channels (if needed)
  ]
  
  # NOT NEEDED for basic notification:
  # - channels:read (unless you list channels)
  # - users:read (unless you look up users)
  # - channels:history (unless you read messages)
  
  # For a slash command bot
  SLASH_COMMAND_SCOPES = [
      "commands",          # Register slash commands
      "chat:write",        # Respond to commands
  ]
  
  # For a bot that responds to mentions
  MENTION_BOT_SCOPES = [
      "app_mentions:read", # Receive @mentions
      "chat:write",        # Reply to mentions
  ]
  ```
  
  ## Scope reference by use case
  
  | Use Case | Required Scopes |
  |----------|-----------------|
  | Post messages | `chat:write` |
  | Slash commands | `commands` |
  | Respond to @mentions | `app_mentions:read`, `chat:write` |
  | Read channel messages | `channels:history` (public), `groups:history` (private) |
  | Read user info | `users:read` |
  | Open modals | `commands` or trigger from event |
  | Add reactions | `reactions:write` |
  | Upload files | `files:write` |
  
  ## Progressive scope requests
  
  ```python
  # Start with minimal scopes
  INITIAL_SCOPES = ["chat:write", "commands"]
  
  # Request additional scopes only when needed
  @app.command("/enable-reactions")
  def enable_reactions(ack, client, command):
      ack()
  
      # Check if we have the scope
      auth_result = client.auth_test()
      # If missing reactions:write, prompt re-auth
      if needs_additional_scope:
          # Send user to re-auth with additional scope
          pass
  ```
  
### **Detection Pattern**
  - scope
  - permission
  - oauth
  - install

## Exceeding Block Kit Limits

### **Id**
block-kit-limits
### **Severity**
medium
### **Situation**
Building complex message UIs with Block Kit
### **Symptom**
  Message fails to send with "invalid_blocks" error.
  Modal won't open. Message truncated unexpectedly.
  
### **Why**
  Block Kit has strict limits that aren't always obvious:
  - 50 blocks per message/modal
  - 3000 characters per text block
  - 10 elements per actions block
  - 100 options per select menu
  - Modal: 50 blocks, 24KB total
  - Home tab: 100 blocks
  
  Exceeding these causes silent failures or cryptic errors.
  
### **Solution**
  ## Know and respect the limits
  
  ```python
  # Constants for Block Kit limits
  BLOCK_KIT_LIMITS = {
      "blocks_per_message": 50,
      "blocks_per_modal": 50,
      "blocks_per_home": 100,
      "text_block_chars": 3000,
      "elements_per_actions": 10,
      "options_per_select": 100,
      "modal_total_bytes": 24 * 1024,  # 24KB
  }
  
  def validate_blocks(blocks: list) -> tuple[bool, str]:
      """Validate blocks before sending."""
      if len(blocks) > BLOCK_KIT_LIMITS["blocks_per_message"]:
          return False, f"Too many blocks: {len(blocks)} > 50"
  
      for block in blocks:
          if block.get("type") == "section":
              text = block.get("text", {}).get("text", "")
              if len(text) > BLOCK_KIT_LIMITS["text_block_chars"]:
                  return False, f"Text too long: {len(text)} > 3000"
  
          if block.get("type") == "actions":
              elements = block.get("elements", [])
              if len(elements) > BLOCK_KIT_LIMITS["elements_per_actions"]:
                  return False, f"Too many actions: {len(elements)} > 10"
  
      return True, "OK"
  
  # Paginate long content
  def paginate_blocks(blocks: list, page: int = 0, per_page: int = 45):
      """Paginate blocks with navigation."""
      start = page * per_page
      end = start + per_page
      page_blocks = blocks[start:end]
  
      # Add pagination controls
      if len(blocks) > per_page:
          page_blocks.append({
              "type": "actions",
              "elements": [
                  {"type": "button", "text": {"type": "plain_text", "text": "Previous"},
                   "action_id": f"page_{page-1}", "disabled": page == 0},
                  {"type": "button", "text": {"type": "plain_text", "text": "Next"},
                   "action_id": f"page_{page+1}",
                   "disabled": end >= len(blocks)}
              ]
          })
  
      return page_blocks
  ```
  
### **Detection Pattern**
  - invalid_blocks
  - block
  - limit
  - 50
  - 3000

## Using Socket Mode in Production

### **Id**
socket-mode-production
### **Severity**
high
### **Situation**
Deploying Slack bot to production
### **Symptom**
  Bot works in development but is unreliable in production.
  Missed events. Connection drops. Can't scale horizontally.
  
### **Why**
  Socket Mode is designed for development:
  - Single WebSocket connection per app
  - Can't scale to multiple instances
  - Connection can drop (needs reconnect logic)
  - No built-in load balancing
  
  For production with multiple instances or high traffic,
  HTTP webhooks are more reliable.
  
### **Solution**
  ## Socket Mode: Only for development
  
  ```python
  # Development with Socket Mode
  if os.environ.get("ENVIRONMENT") == "development":
      from slack_bolt.adapter.socket_mode import SocketModeHandler
      handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
      handler.start()
  ```
  
  ## Production: Use HTTP endpoints
  
  ```python
  # Production with HTTP (Flask example)
  from slack_bolt.adapter.flask import SlackRequestHandler
  from flask import Flask, request
  
  flask_app = Flask(__name__)
  handler = SlackRequestHandler(app)
  
  @flask_app.route("/slack/events", methods=["POST"])
  def slack_events():
      return handler.handle(request)
  
  @flask_app.route("/slack/commands", methods=["POST"])
  def slack_commands():
      return handler.handle(request)
  
  @flask_app.route("/slack/interactions", methods=["POST"])
  def slack_interactions():
      return handler.handle(request)
  ```
  
  ## If you must use Socket Mode in production
  
  ```python
  from slack_bolt.adapter.socket_mode import SocketModeHandler
  import time
  
  class RobustSocketHandler:
      def __init__(self, app, app_token):
          self.app = app
          self.app_token = app_token
          self.handler = None
  
      def start(self):
          while True:
              try:
                  self.handler = SocketModeHandler(self.app, self.app_token)
                  self.handler.start()
              except Exception as e:
                  logger.error(f"Socket Mode disconnected: {e}")
                  time.sleep(5)  # Backoff before reconnect
  ```
  
### **Detection Pattern**
  - socket mode
  - production
  - websocket
  - scale

## Not Verifying Request Signatures

### **Id**
request-signing-bypass
### **Severity**
critical
### **Situation**
Receiving webhooks from Slack
### **Symptom**
  Attackers can send fake requests to your webhook endpoints.
  Spoofed slash commands. Fake event notifications processed.
  
### **Why**
  Slack signs all requests with X-Slack-Signature header using your
  signing secret. Without verification, anyone who knows your webhook
  URL can send fake requests.
  
  This is different from OAuth tokens - signing verifies the REQUEST
  came from Slack, not that you have permission to call Slack.
  
### **Solution**
  ## Bolt handles this automatically
  
  ```python
  from slack_bolt import App
  
  # Bolt verifies signatures automatically when you provide signing_secret
  app = App(
      token=os.environ["SLACK_BOT_TOKEN"],
      signing_secret=os.environ["SLACK_SIGNING_SECRET"]
  )
  # All requests to your handlers are verified
  ```
  
  ## Manual verification (if not using Bolt)
  
  ```python
  import hmac
  import hashlib
  import time
  from flask import Flask, request, abort
  
  SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
  
  def verify_slack_signature(request):
      timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
      signature = request.headers.get("X-Slack-Signature", "")
  
      # Reject old timestamps (replay attack prevention)
      if abs(time.time() - int(timestamp)) > 60 * 5:
          return False
  
      # Compute expected signature
      sig_basestring = f"v0:{timestamp}:{request.get_data(as_text=True)}"
      expected_sig = "v0=" + hmac.new(
          SIGNING_SECRET.encode(),
          sig_basestring.encode(),
          hashlib.sha256
      ).hexdigest()
  
      # Constant-time comparison
      return hmac.compare_digest(expected_sig, signature)
  
  @app.route("/slack/events", methods=["POST"])
  def slack_events():
      if not verify_slack_signature(request):
          abort(403)
      # Safe to process
  ```
  
### **Detection Pattern**
  - signature
  - signing
  - verify
  - X-Slack