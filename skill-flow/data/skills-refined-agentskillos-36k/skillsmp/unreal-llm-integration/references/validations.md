# Unreal Llm Integration - Validations

## Synchronous HTTP Request

### **Id**
ue-sync-http
### **Severity**
critical
### **Type**
regex
### **Pattern**
BlockingRequest|WaitForCompletion|GetContent.*while
### **Message**
Synchronous HTTP detected. Will block game thread and cause hitching.
### **Fix Action**
Use FHttpModule async with OnProcessRequestComplete delegate
### **Applies To**
  - *.cpp
  - *.h

## JSON Parsing on Game Thread

### **Id**
ue-gamethread-json
### **Severity**
high
### **Type**
regex
### **Pattern**
TJsonReader|FJsonSerializer::Deserialize
### **Negative Pattern**
AsyncTask|BackgroundTask|FRunnable
### **Message**
JSON parsing may block game thread. Consider async parsing for large responses.
### **Fix Action**
Parse JSON in async task, return result to game thread
### **Applies To**
  - *.cpp

## No Network Availability Check

### **Id**
ue-no-network-check
### **Severity**
high
### **Type**
regex
### **Pattern**
ProcessRequest|HttpRequest
### **Negative Pattern**
IsNetworkAvailable|IsConnected|HasNetworkConnection
### **Message**
HTTP request without network check. Will fail on offline consoles.
### **Fix Action**
Check network availability, provide offline fallback
### **Applies To**
  - *.cpp

## HTTP Request Without Timeout

### **Id**
ue-no-timeout
### **Severity**
high
### **Type**
regex
### **Pattern**
CreateRequest|ProcessRequest
### **Negative Pattern**
SetTimeout|Timeout
### **Message**
HTTP request without timeout. May hang indefinitely.
### **Fix Action**
Set request timeout: Request->SetTimeout(5.0f)
### **Applies To**
  - *.cpp

## Hardcoded API Key

### **Id**
ue-hardcoded-api-key
### **Severity**
critical
### **Type**
regex
### **Pattern**
sk-[a-zA-Z0-9]{20,}|api[_-]?key.*=.*"[a-zA-Z0-9]+
### **Message**
Hardcoded API key. Will be exposed in packaged game.
### **Fix Action**
Use runtime configuration or secure key management
### **Applies To**
  - *.cpp
  - *.h

## No HTTP Error Handling

### **Id**
ue-no-error-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
OnProcessRequestComplete
### **Negative Pattern**
bWasSuccessful|IsValid|GetResponseCode
### **Message**
HTTP callback without error checking. Failed requests not handled.
### **Fix Action**
Check bWasSuccessful and response code before processing
### **Applies To**
  - *.cpp