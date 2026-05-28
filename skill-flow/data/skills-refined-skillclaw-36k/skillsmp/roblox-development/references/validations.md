# Roblox Development - Validations

## Server-Side Validation Required

### **Id**
check-server-validation
### **Description**
RemoteEvents must validate all incoming data
### **Pattern**
OnServerEvent:Connect
### **File Glob**
**/*.lua
### **Match**
present
### **Context Pattern**
typeof|type\(|assert
### **Message**
Validate all RemoteEvent arguments on server
### **Severity**
error
### **Autofix**


## No Client Trust Pattern

### **Id**
check-no-client-trust
### **Description**
Server should never trust client-provided values for important logic
### **Pattern**
OnServerEvent:Connect.*function.*player.*damage|health|coins|level
### **File Glob**
**/*.lua
### **Match**
present
### **Message**
Don't accept damage/health/currency values from client - calculate on server
### **Severity**
error
### **Autofix**


## DataStore Error Handling

### **Id**
check-datastore-pcall
### **Description**
DataStore calls should be wrapped in pcall
### **Pattern**
GetAsync|SetAsync|UpdateAsync
### **File Glob**
**/*.lua
### **Match**
present
### **Context Pattern**
pcall|xpcall
### **Message**
Wrap DataStore calls in pcall for error handling
### **Severity**
error
### **Autofix**


## BindToClose for Server Shutdown

### **Id**
check-bindtoclose
### **Description**
Save player data on server shutdown
### **Pattern**
DataStore
### **File Glob**
**/*.lua
### **Match**
present
### **Context Pattern**
BindToClose
### **Message**
Use BindToClose to save data on server shutdown
### **Severity**
warning
### **Autofix**


## Loop Yield Required

### **Id**
check-loop-yield
### **Description**
Loops must contain wait/yield to prevent freezing
### **Pattern**
while.*true.*do|while.*do
### **File Glob**
**/*.lua
### **Match**
present
### **Context Pattern**
wait|task.wait|Heartbeat|RenderStepped
### **Message**
Add wait() or task.wait() in loops to prevent freezing
### **Severity**
error
### **Autofix**


## Connection Cleanup

### **Id**
check-connection-cleanup
### **Description**
Event connections should be cleaned up
### **Pattern**
:Connect\(
### **File Glob**
**/*.lua
### **Match**
present
### **Context Pattern**
:Disconnect|Maid|Janitor
### **Message**
Consider cleaning up connections to prevent memory leaks
### **Severity**
info
### **Autofix**


## No Remote Module Loading

### **Id**
check-require-module-id
### **Description**
Don't require modules by ID (security risk)
### **Pattern**
require\(\d{6,}\)
### **File Glob**
**/*.lua
### **Match**
present
### **Message**
Don't require modules by ID - security risk and unreliable
### **Severity**
error
### **Autofix**


## HttpService Usage Review

### **Id**
check-http-service
### **Description**
HttpService calls should be intentional
### **Pattern**
HttpService:GetAsync|HttpService:PostAsync
### **File Glob**
**/*.lua
### **Match**
present
### **Message**
Review HttpService usage - ensure it's intentional and secure
### **Severity**
warning
### **Autofix**


## Text Filtering Required

### **Id**
check-text-filtering
### **Description**
User-generated text must be filtered
### **Pattern**
TextLabel|TextBox|Chat
### **File Glob**
**/*.lua
### **Match**
present
### **Context Pattern**
FilterStringAsync|TextService
### **Message**
Filter all user-generated text with TextService
### **Severity**
warning
### **Autofix**


## Mobile Optimization

### **Id**
check-mobile-optimization
### **Description**
Consider mobile/low-end device performance
### **Pattern**
ParticleEmitter|Beam|Trail
### **File Glob**
**/*.lua
### **Match**
present
### **Context Pattern**
TouchEnabled|Platform
### **Message**
Consider reducing effects for mobile players
### **Severity**
info
### **Autofix**
