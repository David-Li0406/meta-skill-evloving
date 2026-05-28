# Digital Humans - Validations

## No API keys in code

### **Id**
no-api-keys-hardcoded
### **Severity**
critical
### **Description**
Digital human API keys must use environment variables
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml,json}
  #### **Match**
(HEYGEN_API|SYNTHESIA_API|DID_API|TAVUS_).*=.*['"][^'"]{20,}['"]
  #### **Exclude**
process\.env|import\.meta\.env|os\.environ|\$\{
### **Message**
API key hardcoded. Use environment variables.
### **Autofix**


## Custom avatar requires consent documentation

### **Id**
consent-documentation
### **Severity**
critical
### **Description**
Any custom avatar creation should reference consent documentation
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
(create_avatar|clone|custom_avatar|upload.*face)
  #### **Exclude**
consent|agreement|permission|authorized|licensed|stock
### **Message**
Custom avatar creation without consent reference. Add consent documentation.
### **Autofix**


## AI avatar content needs disclosure

### **Id**
disclosure-in-content
### **Severity**
high
### **Description**
Published avatar content should include AI disclosure
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml,md}
  #### **Match**
(publish|upload|post).*(avatar|digital.human|synthesia|heygen)
  #### **Exclude**
disclosure|ai.generated|synthetic|label
### **Message**
Publishing avatar content without disclosure mention. Add AI disclosure.
### **Autofix**


## Avatar generation needs error handling

### **Id**
error-handling-generation
### **Severity**
high
### **Description**
Digital human API calls should handle failures gracefully
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
await.*(heygen|synthesia|did|tavus).*(generate|create|render)
  #### **Exclude**
try|catch|error|Error|except|finally|\.catch
### **Message**
Avatar generation without error handling. Wrap in try/catch.
### **Autofix**


## Check script length before generation

### **Id**
script-length-check
### **Severity**
medium
### **Description**
Long scripts should be validated before expensive generation
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
generate.*(avatar|video|talking)
  #### **Exclude**
length|duration|limit|validate|check
### **Message**
Avatar generation without script length validation. Check duration before generating.
### **Autofix**


## Specify output resolution

### **Id**
resolution-specified
### **Severity**
medium
### **Description**
Avatar video generation should specify resolution for predictable output
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
(heygen|synthesia|did).*generate
  #### **Exclude**
resolution|quality|1080|720|4K|size
### **Message**
Avatar generation without resolution specification. Set output quality.
### **Autofix**


## Track avatar generation costs

### **Id**
cost-tracking-avatar
### **Severity**
medium
### **Description**
Avatar API calls should log estimated costs
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
(heygen|synthesia|did|tavus)\.(generate|create|render)
  #### **Exclude**
cost|minutes|duration|track|log|budget
### **Message**
Avatar generation without cost tracking. Log duration for budget management.
### **Autofix**


## Avatar and voice should be matched

### **Id**
avatar-voice-matching
### **Severity**
medium
### **Description**
Avatar appearance and voice should be compatible
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
avatar.*voice|voice.*avatar
  #### **Exclude**
match|compatible|appropriate|selected
### **Message**
Avatar and voice pairing without matching consideration. Verify compatibility.
### **Autofix**


## Verify language support before generation

### **Id**
language-support-check
### **Severity**
medium
### **Description**
Multi-language generation should verify language support
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
language.*!=.*en|locale|translate.*avatar
  #### **Exclude**
support|available|check|verify|list
### **Message**
Non-English avatar generation without language support check.
### **Autofix**


## Batch avatar generation needs rate limiting

### **Id**
rate-limiting-avatar
### **Severity**
high
### **Description**
Multiple avatar generations should respect rate limits
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
Promise\.all.*(avatar|heygen|synthesia)|for.*await.*(generate.*avatar)
  #### **Exclude**
queue|limit|throttle|batch|concurrent|delay|sequential
### **Message**
Batch avatar generation without rate limiting. Add concurrency control.
### **Autofix**


## Script should be optimized for avatar delivery

### **Id**
script-optimization
### **Severity**
low
### **Description**
Scripts for avatars should be simplified and properly punctuated
### **Pattern**
  #### **File Glob**
**/*.{ts,js,yaml,md}
  #### **Match**
script.*[:=].*"[^"]{500,}"
  #### **Exclude**
simplified|reviewed|optimized
### **Message**
Long script for avatar. Consider simplifying for better AI delivery.
### **Autofix**


## Save avatar generation metadata

### **Id**
avatar-metadata-saved
### **Severity**
low
### **Description**
Avatar outputs should be saved with generation settings
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
(save|download|store).*avatar.*\.mp4|video
  #### **Exclude**
metadata|settings|script|avatar_id|json
### **Message**
Saving avatar video without metadata. Store settings for reference.
### **Autofix**


## Specify background for avatar

### **Id**
background-specification
### **Severity**
low
### **Description**
Avatar generation should specify background for consistent branding
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
(heygen|synthesia|did).*generate
  #### **Exclude**
background|green.screen|transparent|setting
### **Message**
Avatar generation without background specification. Set background for brand consistency.
### **Autofix**
