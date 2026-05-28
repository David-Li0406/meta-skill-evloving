# Twilio Communications - Validations

## Hardcoded Twilio Credentials

### **Id**
hardcoded-credentials
### **Severity**
error
### **Description**
Twilio credentials must never be hardcoded
### **Pattern**
  (AC[a-f0-9]{32}|SK[a-f0-9]{32})
  
### **Message**
Hardcoded Twilio SID detected. Use environment variables.
### **Autofix**


## Auth Token in Source Code

### **Id**
auth-token-in-code
### **Severity**
error
### **Description**
Auth tokens should be in environment variables
### **Pattern**
  auth_token\s*=\s*["'][a-f0-9]{32}["']
  
### **Message**
Hardcoded auth token. Use os.environ['TWILIO_AUTH_TOKEN'].
### **Autofix**


## Webhook Without Signature Validation

### **Id**
no-webhook-validation
### **Severity**
error
### **Description**
Twilio webhooks must validate X-Twilio-Signature
### **Pattern**
  @app\.route.*twilio|/webhooks/.*sms|/webhooks/.*voice
  
### **Anti Pattern**
  (RequestValidator|validate.*signature|X-Twilio-Signature)
  
### **Message**
Webhook without signature validation. Add RequestValidator check.
### **Autofix**


## Twilio Credentials in Client-Side Code

### **Id**
credentials-client-side
### **Severity**
error
### **Description**
Never expose Twilio credentials to browsers
### **Pattern**
  (window\.|document\.|localStorage\.|export\s+const).*TWILIO
  
### **Message**
Twilio credentials exposed client-side. Only use server-side.
### **Autofix**


## No E.164 Phone Number Validation

### **Id**
no-e164-validation
### **Severity**
warning
### **Description**
Phone numbers should be validated before sending
### **Pattern**
  messages\.create\(.*to=
  
### **Anti Pattern**
  (e164|E\.164|\+\d|validate.*phone|format.*phone)
  
### **Message**
Sending to phone without E.164 validation.
### **Autofix**


## Hardcoded Phone Numbers

### **Id**
hardcoded-phone-numbers
### **Severity**
warning
### **Description**
Phone numbers should come from config or database
### **Pattern**
  to=["']\+\d{10,15}["']
  
### **Message**
Hardcoded phone number. Use config or environment variable.
### **Autofix**


## No Twilio Exception Handling

### **Id**
no-twilio-error-handling
### **Severity**
warning
### **Description**
Twilio calls should handle TwilioRestException
### **Pattern**
  (client\.messages\.create|client\.calls\.create)
  
### **Anti Pattern**
  (TwilioRestException|except.*Twilio|try:)
  
### **Message**
Twilio API call without error handling. Catch TwilioRestException.
### **Autofix**


## Not Handling Specific Error Codes

### **Id**
ignoring-error-codes
### **Severity**
info
### **Description**
Handle common Twilio error codes specifically
### **Pattern**
  except TwilioRestException
  
### **Anti Pattern**
  (error\.code|e\.code|21610|30003|63016)
  
### **Message**
Consider handling specific error codes (21610, 30003, etc.).
### **Autofix**


## No Opt-Out Keyword Handling

### **Id**
no-opt-out-handling
### **Severity**
warning
### **Description**
SMS systems must handle STOP/UNSUBSCRIBE keywords
### **Pattern**
  incoming.*sms|sms.*webhook|receive.*message
  
### **Anti Pattern**
  (STOP|UNSUBSCRIBE|opt.?out|opted.?out)
  
### **Message**
No opt-out handling. Check for STOP/UNSUBSCRIBE keywords.
### **Autofix**


## Not Checking Opt-Out Before Sending

### **Id**
no-opt-out-check-before-send
### **Severity**
warning
### **Description**
Check if user has opted out before sending SMS
### **Pattern**
  messages\.create
  
### **Anti Pattern**
  (opt.?out|is.?subscribed|can.?message)
  
### **Message**
Consider checking opt-out status before sending.
### **Autofix**


## No Delivery Status Callback

### **Id**
no-status-callback
### **Severity**
info
### **Description**
Consider adding status callbacks to track delivery
### **Pattern**
  messages\.create\([^)]+\)
  
### **Anti Pattern**
  status_callback
  
### **Message**
No status_callback set. Add to track delivery status.
### **Autofix**


## No Rate Limiting on Verify Endpoint

### **Id**
no-rate-limiting
### **Severity**
warning
### **Description**
Verify endpoints should have rate limiting
### **Pattern**
  (send_verification|verify.*send|/verify)
  
### **Anti Pattern**
  (rate.?limit|RateLimiter|throttle|@limiter)
  
### **Message**
Verify endpoint without rate limiting. Add rate limiting.
### **Autofix**


## No Exponential Backoff on Retry

### **Id**
no-retry-backoff
### **Severity**
info
### **Description**
Retries should use exponential backoff
### **Pattern**
  (retry|Retry|max_retries)
  
### **Anti Pattern**
  (exponential|backoff|delay.*\*|2\s*\*\*)
  
### **Message**
Retry without exponential backoff. Use increasing delays.
### **Autofix**


## No WhatsApp Session Window Tracking

### **Id**
no-session-tracking
### **Severity**
warning
### **Description**
Track 24-hour session windows for WhatsApp
### **Pattern**
  whatsapp.*message|send.*whatsapp
  
### **Anti Pattern**
  (session|24.?hour|window|template)
  
### **Message**
No session window tracking. Track 24-hour window for WhatsApp.
### **Autofix**
