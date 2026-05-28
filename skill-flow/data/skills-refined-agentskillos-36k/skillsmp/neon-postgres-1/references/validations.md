# Neon Postgres - Validations

## Direct Database URL in Client Code

### **Id**
direct-url-exposed
### **Severity**
error
### **Description**
Direct database URLs should never be exposed to client
### **Pattern**
  (NEXT_PUBLIC|REACT_APP|VITE).*DIRECT.*URL
  
### **Message**
Direct URL exposed to client. Only pooled URLs for server-side use.
### **Autofix**


## Hardcoded Database Connection String

### **Id**
hardcoded-connection-string
### **Severity**
error
### **Description**
Connection strings should use environment variables
### **Pattern**
  postgres://[^$\{]+@.*neon\.tech
  
### **Message**
Hardcoded connection string. Use environment variables.
### **Autofix**


## Missing SSL Mode in Connection String

### **Id**
missing-ssl-mode
### **Severity**
warning
### **Description**
Neon requires SSL connections
### **Pattern**
  DATABASE_URL.*neon\.tech(?!.*sslmode)
  
### **Message**
Missing sslmode=require. Add to connection string.
### **Autofix**


## Prisma Missing directUrl for Migrations

### **Id**
prisma-missing-direct-url
### **Severity**
error
### **Description**
Prisma needs directUrl for migrations through PgBouncer
### **Pattern**
  datasource.*postgresql.*url.*pooler(?!.*directUrl)
  
### **Message**
Using pooled URL without directUrl. Migrations will fail.
### **Autofix**


## Prisma directUrl Points to Pooler

### **Id**
prisma-pooled-direct-url
### **Severity**
error
### **Description**
directUrl should be non-pooled connection
### **Pattern**
  directUrl.*pooler
  
### **Message**
directUrl points to pooler. Use non-pooled endpoint for migrations.
### **Autofix**


## High Pool Size in Serverless Function

### **Id**
high-pool-size-serverless
### **Severity**
warning
### **Description**
High pool sizes exhaust connections with many function instances
### **Pattern**
  max:\s*[2-9][0-9]|max:\s*1[0-9][0-9]
  
### **Message**
Pool size too high for serverless. Use max: 5-10.
### **Autofix**


## Creating New Client Per Request

### **Id**
new-client-per-request
### **Severity**
warning
### **Description**
Creating new clients per request wastes connections
### **Pattern**
  new Client\(.*\).*await.*connect\(\).*end\(\)
  
### **Message**
Creating client per request. Use connection pool or neon() driver.
### **Autofix**


## Branch Creation Without Cleanup Strategy

### **Id**
branch-without-cleanup
### **Severity**
warning
### **Description**
Branches should have cleanup automation
### **Pattern**
  branches create(?!.*delete)
  
### **Message**
Creating branch without cleanup. Add delete-branch-action to PR close.
### **Autofix**


## Scale-to-Zero Enabled on Production

### **Id**
production-scale-to-zero
### **Severity**
warning
### **Description**
Scale-to-zero adds latency in production
### **Pattern**
  production.*suspend.*5.*minutes|main.*scale.*zero
  
### **Message**
Scale-to-zero on production. Disable for low-latency.
### **Autofix**


## HTTP Driver Used for Transactions

### **Id**
http-driver-transaction
### **Severity**
error
### **Description**
neon() HTTP driver doesn't support transactions
### **Pattern**
  neon\(.*\).*BEGIN|neon\(.*\).*COMMIT|neon\(.*\).*transaction
  
### **Message**
HTTP driver with transaction. Use Pool from @neondatabase/serverless.
### **Autofix**


## pg Driver in Edge Runtime

### **Id**
pg-driver-in-edge
### **Severity**
warning
### **Description**
TCP connections don't work in all edge environments
### **Pattern**
  import.*from ['"]pg['"].*edge|runtime.*edge.*pg
  
### **Message**
pg driver in edge runtime. Use @neondatabase/serverless instead.
### **Autofix**
