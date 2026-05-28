# Community Building - Validations

## Hardcoded Discord/Slack Webhook URL

### **Id**
hardcoded-webhook-url
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - discord\.com/api/webhooks/\d+
  - hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+
### **Message**
Hardcoded webhook URL exposed. Use environment variables.
### **Fix Action**
Move webhook URLs to environment variables (DISCORD_WEBHOOK_URL, SLACK_WEBHOOK_URL)
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
### **Exceptions**
  - process\.env|import\.meta\.env|env\.

## Community API Without Rate Limiting

### **Id**
missing-rate-limit-community
### **Severity**
high
### **Type**
regex
### **Pattern**
  - discord\.js|@slack/web-api|slack/bolt
  - client\.channels|client\.guilds|app\.client
### **Message**
Community platform integration without rate limiting.
### **Fix Action**
Implement rate limiting for Discord/Slack API calls
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - rateLimit|rate-limit|rateLimiter|throttle|bottleneck

## Discord Bot Without Member Verification

### **Id**
no-member-verification
### **Severity**
medium
### **Type**
regex
### **Pattern**
  - discord\.js
  - client\.on\(['"]guildMemberAdd['"]
### **Message**
Member join handler without verification process.
### **Fix Action**
Add verification step or captcha for new members
### **Applies To**
  - **/*.ts
  - **/*.js
### **Exceptions**
  - verify|captcha|screening|pending|quarantine

## Moderation Action Without Logging

### **Id**
no-moderation-logging
### **Severity**
medium
### **Type**
regex
### **Pattern**
  - ban|kick|mute|timeout|delete.*message
  - \.ban\(|\.kick\(|\.timeout\(
### **Message**
Moderation action without audit logging.
### **Fix Action**
Log all moderation actions with timestamp, actor, target, and reason
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - log|audit|record|track|modLog

## Bot Command Without Error Handler

### **Id**
missing-error-handler-bot
### **Severity**
medium
### **Type**
regex
### **Pattern**
  - client\.on\(['"]interactionCreate['"]
  - command\.execute|interaction\.reply
### **Message**
Bot command handler without proper error handling.
### **Fix Action**
Wrap command execution in try-catch with user-friendly error responses
### **Applies To**
  - **/*.ts
  - **/*.js
### **Exceptions**
  - try.*catch|\.catch\(|error.*handler|onError

## Admin Command Without Permission Check

### **Id**
no-permission-check
### **Severity**
high
### **Type**
regex
### **Pattern**
  - ban|kick|mute|role.*add|channel.*create
  - admin|moderator|manage
### **Message**
Admin action without permission verification.
### **Fix Action**
Check user permissions before executing admin commands
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - hasPermission|checkPermission|permissions\.has|isAdmin|isModerator

## User Input Without Content Moderation

### **Id**
no-content-filter
### **Severity**
medium
### **Type**
regex
### **Pattern**
  - message\.content|interaction\.options
  - userInput|userMessage|content
### **Message**
User-generated content without moderation filter.
### **Fix Action**
Implement content filtering for spam, links, or inappropriate content
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - filter|moderate|automod|profanity|spam.*check|content.*check

## Member Join Without Welcome Flow

### **Id**
no-welcome-flow
### **Severity**
info
### **Type**
regex
### **Pattern**
  - guildMemberAdd|memberJoin|onJoin
### **Message**
New member event without welcome/onboarding flow.
### **Fix Action**
Add welcome message with community guidelines and onboarding steps
### **Applies To**
  - **/*.ts
  - **/*.js
### **Exceptions**
  - welcome|onboard|intro|guideline|rules

## Discord Embed Without Input Sanitization

### **Id**
missing-embed-sanitization
### **Severity**
medium
### **Type**
regex
### **Pattern**
  - EmbedBuilder|MessageEmbed|new.*Embed
  - setDescription|setTitle|addField
### **Message**
Embed content potentially unsanitized from user input.
### **Fix Action**
Sanitize user input before embedding to prevent injection
### **Applies To**
  - **/*.ts
  - **/*.js
### **Exceptions**
  - sanitize|escape|clean|encode|safe

## Community Feature Without Engagement Metrics

### **Id**
no-engagement-tracking
### **Severity**
info
### **Type**
regex
### **Pattern**
  - discord\.js|@slack/bolt
  - message|reaction|interaction
### **Message**
Community feature without engagement tracking.
### **Fix Action**
Track engagement metrics (messages, reactions, active users)
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - analytics|metrics|track|telemetry|stats|engagement

## Hardcoded Channel IDs

### **Id**
hardcoded-channel-id
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ['"]\d{17,19}['"]
  - channelId.*=.*['"]\d{17,19}['"]
### **Message**
Hardcoded Discord channel IDs will break across environments.
### **Fix Action**
Use environment variables or configuration for channel IDs
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
### **Exceptions**
  - process\.env|config\.|CHANNEL_ID|getChannel

## Community System Without Fallback Contact

### **Id**
no-backup-contact
### **Severity**
info
### **Type**
regex
### **Pattern**
  - discord|slack|community
  - config|setup|initialize
### **Message**
Community platform without backup contact method.
### **Fix Action**
Collect email or secondary contact for members (platform lock-in protection)
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - email|newsletter|backup|fallback|secondary

## Public Channel Without Rate Control

### **Id**
missing-slow-mode
### **Severity**
info
### **Type**
regex
### **Pattern**
  - createChannel|channelCreate
  - public|general|help|support
### **Message**
Public channel creation without slow mode configuration.
### **Fix Action**
Consider adding slow mode to high-traffic channels
### **Applies To**
  - **/*.ts
  - **/*.js
### **Exceptions**
  - slowMode|rateLimitPerUser|cooldown

## Event Creation Without Reminder System

### **Id**
no-event-reminder
### **Severity**
info
### **Type**
regex
### **Pattern**
  - createEvent|scheduledEvent|GuildScheduledEvent
  - event.*create|schedule.*event
### **Message**
Community event without reminder system.
### **Fix Action**
Add reminder notifications for upcoming events
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - reminder|notify|notification|alert|ping

## Channel Content Without Archive Strategy

### **Id**
missing-archive-strategy
### **Severity**
info
### **Type**
regex
### **Pattern**
  - message|thread|discussion
  - important|decision|faq|resource
### **Message**
Important community content without archival strategy.
### **Fix Action**
Implement content archival for important discussions (platform lock-in protection)
### **Applies To**
  - **/*.ts
  - **/*.md
### **Exceptions**
  - archive|backup|export|persist|save