# Aws Serverless - Validations

## Hardcoded AWS Credentials

### **Id**
hardcoded-credentials
### **Severity**
error
### **Description**
AWS credentials must never be hardcoded
### **Pattern**
  (AKIA[0-9A-Z]{16}|aws_access_key_id\s*=\s*["'][A-Z0-9]{20}["'])
  
### **Message**
Hardcoded AWS access key detected. Use IAM roles or environment variables.
### **Autofix**


## AWS Secret Key in Source Code

### **Id**
secret-key-in-code
### **Severity**
error
### **Description**
Secret keys should use Secrets Manager or environment variables
### **Pattern**
  aws_secret_access_key\s*=\s*["'][A-Za-z0-9/+=]{40}["']
  
### **Message**
Hardcoded AWS secret key. Use IAM roles or Secrets Manager.
### **Autofix**


## Overly Permissive IAM Policy

### **Id**
overly-permissive-policy
### **Severity**
warning
### **Description**
Avoid wildcard permissions in Lambda IAM roles
### **Pattern**
  (Action.*:\s*\*|Resource.*:\s*\*).*Effect.*Allow
  
### **Message**
Overly permissive IAM policy. Use least privilege principle.
### **Autofix**


## Lambda Handler Without Error Handling

### **Id**
no-error-handling
### **Severity**
warning
### **Description**
Lambda handlers should have try/catch for graceful errors
### **Pattern**
  exports\.handler\s*=\s*async.*\{[^}]*await
  
### **Anti Pattern**
  (try\s*\{|catch\s*\()
  
### **Message**
Lambda handler without error handling. Add try/catch.
### **Autofix**


## Missing callbackWaitsForEmptyEventLoop

### **Id**
missing-callback-wait
### **Severity**
info
### **Description**
Node.js handlers should set callbackWaitsForEmptyEventLoop
### **Pattern**
  exports\.handler\s*=\s*async
  
### **Anti Pattern**
  callbackWaitsForEmptyEventLoop
  
### **Message**
Consider setting context.callbackWaitsForEmptyEventLoop = false
### **Autofix**


## Default Memory Configuration

### **Id**
default-memory
### **Severity**
info
### **Description**
Default 128MB may be too low for many workloads
### **Pattern**
  MemorySize:\s*128
  
### **Message**
Using default 128MB memory. Consider increasing for better performance.
### **Autofix**


## Low Timeout Configuration

### **Id**
low-timeout
### **Severity**
warning
### **Description**
Very low timeout may cause unexpected failures
### **Pattern**
  Timeout:\s*[1-3]\s*$
  
### **Message**
Timeout of 1-3 seconds may be too low. Increase if making external calls.
### **Autofix**


## No Dead Letter Queue Configuration

### **Id**
no-dlq
### **Severity**
warning
### **Description**
Async functions should have DLQ for failed invocations
### **Pattern**
  Type:\s*AWS::Serverless::Function
  
### **Anti Pattern**
  (DeadLetterQueue|DeadLetterConfig|DestinationConfig)
  
### **Message**
No DLQ configured. Add for async invocations.
### **Autofix**


## Importing Full AWS SDK v2

### **Id**
full-aws-sdk-import
### **Severity**
warning
### **Description**
Import specific clients from AWS SDK v3 for smaller packages
### **Pattern**
  require\(['"]aws-sdk['"]\)
  
### **Message**
Importing full AWS SDK. Use modular SDK v3 imports for smaller packages.
### **Autofix**


## Hardcoded DynamoDB Table Name

### **Id**
hardcoded-table-name
### **Severity**
warning
### **Description**
Table names should come from environment variables
### **Pattern**
  TableName:\s*["'][A-Za-z][A-Za-z0-9-_]+["']
  
### **Anti Pattern**
  (process\.env|os\.environ|!Ref|!GetAtt)
  
### **Message**
Hardcoded table name. Use environment variable for portability.
### **Autofix**


## Hardcoded S3 Bucket Name

### **Id**
hardcoded-bucket-name
### **Severity**
warning
### **Description**
Bucket names should come from environment variables
### **Pattern**
  Bucket:\s*["'][a-z0-9.-]+["']
  
### **Anti Pattern**
  (process\.env|os\.environ|!Ref|!GetAtt)
  
### **Message**
Hardcoded bucket name. Use environment variable.
### **Autofix**
