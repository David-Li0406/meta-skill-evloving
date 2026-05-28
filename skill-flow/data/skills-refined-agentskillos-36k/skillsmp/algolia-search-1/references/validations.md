# Algolia Search - Validations

## Admin API Key in Client Code

### **Id**
admin-key-client
### **Severity**
error
### **Description**
Admin API key must never be exposed to client-side code
### **Pattern**
  (NEXT_PUBLIC|REACT_APP|VITE).*ADMIN.*KEY
  
### **Message**
Admin API key exposed to client. Use search-only key.
### **Autofix**


## Hardcoded Algolia API Key

### **Id**
hardcoded-api-key
### **Severity**
error
### **Description**
API keys should use environment variables
### **Pattern**
  algoliasearch\s*\(\s*['"][A-Z0-9]{8,}['"]
  
### **Message**
Hardcoded Algolia credentials. Use environment variables.
### **Autofix**


## Search Key Used for Indexing

### **Id**
search-key-indexing
### **Severity**
error
### **Description**
Indexing operations require admin key, not search key
### **Pattern**
  SEARCH_KEY.*saveObject|SEARCH_KEY.*deleteObject
  
### **Message**
Search key used for indexing. Use admin key for write operations.
### **Autofix**


## Single Record Indexing in Loop

### **Id**
single-record-indexing
### **Severity**
warning
### **Description**
Batch records together for efficient indexing
### **Pattern**
  (for|while|forEach|map).*saveObject\((?!s)
  
### **Message**
Single record indexing in loop. Use saveObjects for batch indexing.
### **Autofix**


## Using deleteBy for Deletion

### **Id**
delete-by-usage
### **Severity**
warning
### **Description**
deleteBy is expensive and rate-limited
### **Pattern**
  \.deleteBy\s*\(
  
### **Message**
deleteBy is expensive. Prefer deleteObjects with specific IDs.
### **Autofix**


## Frequent Full Reindex

### **Id**
full-reindex-daily
### **Severity**
warning
### **Description**
Full reindex wastes operations on unchanged data
### **Pattern**
  replaceAllObjects.*cron|schedule.*replaceAllObjects
  
### **Message**
Frequent full reindex. Consider incremental sync for unchanged data.
### **Autofix**


## Full Client Instead of Lite

### **Id**
no-lite-client
### **Severity**
info
### **Description**
Use lite client for smaller bundle in frontend
### **Pattern**
  import.*from\s+['"]algoliasearch['"](?!.*lite)
  
### **Anti Pattern**
  lite|server|node
  
### **Message**
Full Algolia client imported. Use algoliasearch/lite for frontend.
### **Autofix**


## Regular InstantSearch in Next.js

### **Id**
instantsearch-not-nextjs
### **Severity**
warning
### **Description**
Use react-instantsearch-nextjs for SSR support
### **Pattern**
  import.*InstantSearch.*from\s+['"]react-instantsearch['"]
  
### **Message**
Using regular InstantSearch. Use InstantSearchNext for Next.js SSR.
### **Autofix**


## Missing Searchable Attributes Configuration

### **Id**
no-searchable-attributes
### **Severity**
warning
### **Description**
Configure searchableAttributes for better relevance
### **Pattern**
  setSettings\s*\(\s*\{[^}]*\}
  
### **Anti Pattern**
  searchableAttributes
  
### **Message**
No searchableAttributes configured. Set attribute priority for relevance.
### **Autofix**


## Missing Custom Ranking

### **Id**
no-custom-ranking
### **Severity**
info
### **Description**
Custom ranking improves business relevance
### **Pattern**
  setSettings\s*\(\s*\{[^}]*\}
  
### **Anti Pattern**
  customRanking
  
### **Message**
No customRanking configured. Add business metrics (popularity, rating).
### **Autofix**


## Search Without Debouncing

### **Id**
no-debounce-search
### **Severity**
warning
### **Description**
Manual search should be debounced to save operations
### **Pattern**
  (keyup|keydown|onChange).*\.search\s*\(
  
### **Anti Pattern**
  debounce|throttle|timeout|InstantSearch
  
### **Message**
Search on keystroke without debouncing. Add debounce to reduce operations.
### **Autofix**


## Search Key Without Rate Limiting

### **Id**
no-rate-limit-key
### **Severity**
warning
### **Description**
Rate limit search keys to prevent abuse
### **Pattern**
  addApiKey.*acl.*search
  
### **Anti Pattern**
  maxQueriesPerIPPerHour|maxHitsPerQuery
  
### **Message**
Search key without rate limits. Add maxQueriesPerIPPerHour.
### **Autofix**
