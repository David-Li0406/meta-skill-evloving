# Discord Bot Architect - Validations

## Hardcoded Discord Token

### **Id**
hardcoded-token
### **Severity**
error
### **Description**
Discord tokens must never be hardcoded
### **Pattern**
  (MTI|MTM|MTQ|NTI|NjI|NjM|NzI|NzM|ODI|ODM|OTI|OTM)[A-Za-z0-9_-]{23,27}\.[A-Za-z0-9_-]{6}\.[A-Za-z0-9_-]{38}
  
### **Message**
Hardcoded Discord token detected. Use environment variables.
### **Autofix**


## Token Variable Assignment

### **Id**
token-in-code
### **Severity**
error
### **Description**
Tokens should come from environment, not strings
### **Pattern**
  (token|TOKEN)\s*=\s*["'][A-Za-z0-9_.-]+["']
  
### **Anti Pattern**
  (process\.env|os\.environ|getenv|dotenv)
  
### **Message**
Token assigned from string literal. Use environment variable.
### **Autofix**


## Token in Client-Side Code

### **Id**
token-in-client
### **Severity**
error
### **Description**
Never expose Discord tokens to browsers
### **Pattern**
  (window\.|document\.|localStorage\.|NEXT_PUBLIC_).*DISCORD.*(TOKEN|SECRET)
  
### **Message**
Discord credentials exposed client-side. Only use server-side.
### **Autofix**


## Slow Operation Without Defer

### **Id**
missing-defer
### **Severity**
warning
### **Description**
Slow operations should be deferred to avoid timeout
### **Pattern**
  async\s+(execute|run)\s*\([^)]*interaction[^)]*\)\s*\{[^}]*(await\s+fetch|axios|prisma|database|openai|anthropic)
  
### **Anti Pattern**
  (deferReply|deferUpdate|defer\()
  
### **Message**
Slow operation without defer. Interaction may timeout.
### **Autofix**


## Interaction Without Error Handling

### **Id**
missing-error-handling
### **Severity**
warning
### **Description**
Interactions should have try/catch for graceful errors
### **Pattern**
  async\s+execute\s*\([^)]*interaction[^)]*\)\s*\{[^}]*await\s+interaction
  
### **Anti Pattern**
  (try\s*\{|catch\s*\()
  
### **Message**
Interaction without error handling. Add try/catch.
### **Autofix**


## Using Message Content Intent

### **Id**
message-content-intent
### **Severity**
warning
### **Description**
Message Content is privileged, prefer slash commands
### **Pattern**
  (GatewayIntentBits\.MessageContent|intents\.message_content\s*=\s*True|MessageContent)
  
### **Message**
Using Message Content intent. Consider slash commands instead.
### **Autofix**


## Requesting All Intents

### **Id**
all-intents
### **Severity**
warning
### **Description**
Only request intents you actually need
### **Pattern**
  (Intents\.all\(\)|\.all\(\))
  
### **Message**
Requesting all intents. Only enable what you need.
### **Autofix**


## Syncing Commands on Ready Event

### **Id**
sync-on-ready
### **Severity**
warning
### **Description**
Don't sync commands on every bot startup
### **Pattern**
  on_ready.*sync_commands|ready.*application\.commands\.set
  
### **Message**
Syncing commands on startup. Use separate deploy script.
### **Autofix**


## Registering Commands in Loop

### **Id**
command-registration-loop
### **Severity**
warning
### **Description**
Use bulk registration, not individual calls
### **Pattern**
  for.*\.(commands\.create|put.*applicationGuildCommands)
  
### **Message**
Registering commands in loop. Use bulk registration.
### **Autofix**


## No Rate Limit Handling

### **Id**
no-rate-limit-handling
### **Severity**
info
### **Description**
Consider handling rate limits for bulk operations
### **Pattern**
  for\s*\([^)]+\)\s*\{[^}]*(send|edit|delete|create)[^}]+\}
  
### **Anti Pattern**
  (setTimeout|sleep|delay|queue|throttle)
  
### **Message**
Bulk operation without rate limit handling.
### **Autofix**


## No Sharding Implementation

### **Id**
no-sharding-consideration
### **Severity**
info
### **Description**
Consider sharding for large bots (2500+ guilds required)
### **Pattern**
  new\s+Client\s*\(
  
### **Anti Pattern**
  (ShardingManager|AutoShardedBot|AutoShardedClient)
  
### **Message**
No sharding implementation. Required at 2500+ guilds.
### **Autofix**
