# Azure Functions - Validations

## Hardcoded Connection String

### **Id**
hardcoded-connection-string
### **Severity**
error
### **Description**
Connection strings must never be hardcoded
### **Pattern**
  (DefaultEndpointsProtocol=https;AccountName=|Server=.*Password=|mongodb\+srv://.*@)
  
### **Message**
Hardcoded connection string. Use Key Vault or App Settings.
### **Autofix**


## Hardcoded API Key in Code

### **Id**
hardcoded-api-key
### **Severity**
error
### **Description**
API keys should use Key Vault or App Settings
### **Pattern**
  (api[_-]?key\s*=\s*["'][A-Za-z0-9]{20,}["']|Bearer\s+[A-Za-z0-9._-]{20,})
  
### **Message**
Hardcoded API key. Use Key Vault or environment variables.
### **Autofix**


## Anonymous Authorization Level in Production

### **Id**
authorization-level-anonymous
### **Severity**
warning
### **Description**
Anonymous endpoints should be protected by other means
### **Pattern**
  AuthorizationLevel\.Anonymous
  
### **Message**
Anonymous authorization. Ensure protected by API Management or other auth.
### **Autofix**


## Blocking .Result Call

### **Id**
blocking-result
### **Severity**
error
### **Description**
Using .Result blocks threads and causes deadlocks
### **Pattern**
  \.(Result|GetAwaiter\(\)\.GetResult\(\))
  
### **Message**
Blocking .Result call. Use await instead.
### **Autofix**


## Blocking .Wait() Call

### **Id**
blocking-wait
### **Severity**
error
### **Description**
Using .Wait() blocks threads
### **Pattern**
  \.Wait\(\)
  
### **Message**
Blocking .Wait() call. Use await instead.
### **Autofix**


## Thread.Sleep Usage

### **Id**
thread-sleep
### **Severity**
error
### **Description**
Thread.Sleep blocks threads
### **Pattern**
  Thread\.Sleep\(
  
### **Message**
Thread.Sleep blocks threads. Use await Task.Delay() instead.
### **Autofix**


## New HttpClient Instance

### **Id**
new-httpclient
### **Severity**
warning
### **Description**
Creating HttpClient per request causes socket exhaustion
### **Pattern**
  new\s+HttpClient\s*\(
  
### **Message**
New HttpClient per request. Use IHttpClientFactory or static client.
### **Autofix**


## HttpClient in Using Statement

### **Id**
using-httpclient
### **Severity**
warning
### **Description**
Disposing HttpClient causes socket exhaustion
### **Pattern**
  using\s*\(.*HttpClient
  
### **Message**
HttpClient in using statement. Use IHttpClientFactory for proper lifecycle.
### **Autofix**


## In-Process FunctionName Attribute

### **Id**
in-process-function-name
### **Severity**
info
### **Description**
In-process model deprecated November 2026
### **Pattern**
  \[FunctionName\(
  
### **Message**
In-process FunctionName attribute. Consider migrating to isolated worker.
### **Autofix**


## Missing Function Attribute

### **Id**
missing-function-attribute
### **Severity**
warning
### **Description**
Isolated worker requires [Function] attribute
### **Pattern**
  public.*Task.*\[HttpTrigger
  
### **Anti Pattern**
  \[Function\(
  
### **Message**
HttpTrigger without [Function] attribute (isolated worker requires it).
### **Autofix**


## Missing Timeout Configuration

### **Id**
missing-timeout-config
### **Severity**
info
### **Description**
Function timeout should be explicitly configured
### **File Pattern**
host.json
### **Pattern**
  "version":\s*"2\.0"
  
### **Anti Pattern**
  "functionTimeout"
  
### **Message**
No functionTimeout in host.json. Consider configuring explicitly.
### **Autofix**


## Verbose Logging Level

### **Id**
verbose-logging-production
### **Severity**
info
### **Description**
Verbose logging impacts performance
### **File Pattern**
host.json
### **Pattern**
  "logLevel".*"Trace"|"logLevel".*"Debug"
  
### **Message**
Verbose log level. Use Information or Warning in production.
### **Autofix**


## Non-Deterministic Code in Orchestrator

### **Id**
durable-non-deterministic
### **Severity**
error
### **Description**
Orchestrators must be deterministic
### **Pattern**
  \[OrchestrationTrigger\].*\n.*DateTime\.(Now|UtcNow)|Guid\.NewGuid\(\)|Random\(
  
### **Message**
Non-deterministic code in orchestrator. Use context.CurrentUtcDateTime.
### **Autofix**


## Await Non-Activity in Orchestrator

### **Id**
durable-await-non-activity
### **Severity**
warning
### **Description**
Orchestrators should only await activity/sub-orchestrator calls
### **Pattern**
  \[OrchestrationTrigger\].*await\s+(?!context\.)
  
### **Message**
Await non-activity in orchestrator. Use context.CallActivityAsync.
### **Autofix**
