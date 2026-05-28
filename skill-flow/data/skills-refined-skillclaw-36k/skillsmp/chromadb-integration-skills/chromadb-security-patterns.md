# ChromaDB Security & Privacy Patterns

**Purpose**: Security and privacy best practices for ChromaDB integrations

**Use When**: Handling sensitive data, PII, or confidential information in ChromaDB

---

## Security Principles

1. **Least Privilege**: Only store what's necessary
2. **Data Minimization**: Reduce sensitive data exposure
3. **Sanitization First**: Clean data before storage
4. **Encryption in Transit**: Use HTTPS for ChromaDB connections
5. **Access Control**: Implement collection-level permissions
6. **Audit Logging**: Track all sensitive data access

---

## PII Detection & Redaction

### Automatic PII Detection

```javascript
function detectPII(text) {
  const piiPatterns = {
    email: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g,
    phone: /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g,
    ssn: /\b\d{3}-\d{2}-\d{4}\b/g,
    creditCard: /\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/g,
    ipAddress: /\b(?:\d{1,3}\.){3}\d{1,3}\b/g
  };

  const detected = [];
  for (const [type, pattern] of Object.entries(piiPatterns)) {
    const matches = text.match(pattern);
    if (matches) {
      detected.push({ type, values: matches });
    }
  }

  return detected;
}
```

### PII Redaction

```javascript
function redactPII(text, preserveFormat = true) {
  let redacted = text;

  // Email redaction
  redacted = redacted.replace(
    /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g,
    preserveFormat ? '[EMAIL_REDACTED]' : '***'
  );

  // Phone redaction
  redacted = redacted.replace(
    /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g,
    preserveFormat ? '[PHONE_REDACTED]' : '***'
  );

  // SSN redaction
  redacted = redacted.replace(
    /\b\d{3}-\d{2}-\d{4}\b/g,
    preserveFormat ? '[SSN_REDACTED]' : '***-**-****'
  );

  // Credit card redaction
  redacted = redacted.replace(
    /\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/g,
    preserveFormat ? '[CARD_REDACTED]' : '****-****-****-****'
  );

  // IP address redaction
  redacted = redacted.replace(
    /\b(?:\d{1,3}\.){3}\d{1,3}\b/g,
    preserveFormat ? '[IP_REDACTED]' : '***.***.***'
  );

  return redacted;
}

// Usage
const originalText = "Contact john.doe@example.com or call 555-123-4567";
const sanitized = redactPII(originalText);
// Result: "Contact [EMAIL_REDACTED] or call [PHONE_REDACTED]"
```

### PII Mapping Storage

```javascript
// Store PII mapping separately (encrypted)
const piiMap = {};

function redactAndMapPII(text, documentId) {
  const piiDetected = detectPII(text);
  let redacted = text;

  piiDetected.forEach(({ type, values }) => {
    values.forEach(value => {
      const token = `[${type.toUpperCase()}_${generateToken()}]`;
      redacted = redacted.replace(value, token);

      // Store mapping (ENCRYPT THIS IN PRODUCTION)
      piiMap[documentId] = piiMap[documentId] || {};
      piiMap[documentId][token] = value;
    });
  });

  return { redacted, hasPII: piiDetected.length > 0 };
}

function generateToken() {
  return Math.random().toString(36).substr(2, 8).toUpperCase();
}
```

---

## Data Sanitization

### Path Sanitization

```javascript
function sanitizePaths(text) {
  // Remove absolute paths
  let sanitized = text.replace(
    /\/home\/[a-zA-Z0-9_-]+/g,
    '/home/[USER]'
  );

  sanitized = sanitized.replace(
    /C:\\Users\\[^\\]+/g,
    'C:\\Users\\[USER]'
  );

  // Remove temp directories with timestamps
  sanitized = sanitized.replace(
    /\/tmp\/[a-z0-9-]+/g,
    '/tmp/[TEMP]'
  );

  return sanitized;
}
```

### API Key & Token Redaction

```javascript
function redactSecrets(text) {
  let redacted = text;

  // GitHub tokens (ghp_...)
  redacted = redacted.replace(
    /ghp_[a-zA-Z0-9]{36}/g,
    '[GITHUB_TOKEN_REDACTED]'
  );

  // AWS keys (AKIA...)
  redacted = redacted.replace(
    /AKIA[0-9A-Z]{16}/g,
    '[AWS_KEY_REDACTED]'
  );

  // Generic API keys (common patterns)
  redacted = redacted.replace(
    /['\"]?api[_-]?key['\"]?\s*[:=]\s*['\"]?([a-zA-Z0-9_-]{20,})['\"]?/gi,
    'api_key: [REDACTED]'
  );

  // Bearer tokens
  redacted = redacted.replace(
    /Bearer\s+[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+/g,
    'Bearer [JWT_REDACTED]'
  );

  return redacted;
}
```

### User ID Hashing

```javascript
import crypto from 'crypto';

function hashUserId(userId, salt = 'your-secret-salt') {
  return crypto
    .createHash('sha256')
    .update(userId + salt)
    .digest('hex')
    .substring(0, 16);  // First 16 chars for readability
}

// Usage - store hashed IDs instead of real user IDs
const metadata = {
  user_id: hashUserId('john.doe@example.com'),  // a3f5c8d2e9b1f4c7
  action: 'login',
  timestamp: Date.now()
};
```

---

## Access Control Patterns

### Collection-Level Access Control

```javascript
const collectionPermissions = {
  'research_findings_confidential': ['research_team', 'admin'],
  'bug_patterns_security': ['security_team', 'admin'],
  'customer_feedback': ['product_team', 'support_team', 'admin']
};

function checkAccess(collectionName, userRole) {
  const allowedRoles = collectionPermissions[collectionName] || ['admin'];

  if (!allowedRoles.includes(userRole)) {
    throw new Error(
      `Access denied: User role '${userRole}' cannot access collection '${collectionName}'. ` +
      `Required roles: ${allowedRoles.join(', ')}`
    );
  }
}

// Usage
try {
  checkAccess('research_findings_confidential', 'eng_team');  // Throws error
} catch (error) {
  console.error(error.message);
}
```

### Metadata-Based Row-Level Security

```javascript
function queryWithRowSecurity(collectionName, query, userDepartment) {
  // Users can only see documents from their department
  const results = mcp__chroma__query_documents({
    collection_name: collectionName,
    query_texts: [query],
    n_results: 20,
    where: {
      "$or": [
        { "department": userDepartment },
        { "visibility": "public" }
      ]
    }
  });

  return results;
}

// Usage
const results = queryWithRowSecurity('company_docs', 'product roadmap', 'engineering');
// Only returns docs where department='engineering' OR visibility='public'
```

---

## Audit Logging

### Log All Sensitive Operations

```javascript
function auditLog(operation, collectionName, user, metadata = {}) {
  const logEntry = {
    timestamp: new Date().toISOString(),
    operation: operation,  // 'query', 'add', 'update', 'delete'
    collection: collectionName,
    user: user,
    metadata: metadata,
    ip_address: getCurrentIPAddress(),
    session_id: getCurrentSessionId()
  };

  // Store in secure audit log (separate from ChromaDB)
  writeToAuditLog(logEntry);

  // For sensitive collections, also alert
  if (isSensitiveCollection(collectionName)) {
    alertSecurityTeam(logEntry);
  }
}

// Usage
auditLog('query', 'customer_pii', 'john.doe', {
  query: 'customer credit card information',
  results_count: 5
});
```

---

## Secure Document Storage Workflow

### Complete Sanitization Pipeline

```javascript
async function secureAddDocuments(collectionName, documents, ids, metadatas, user) {
  // Step 1: Access control check
  checkAccess(collectionName, user.role);

  // Step 2: Sanitize documents
  const sanitizedDocs = documents.map(doc => {
    let sanitized = redactPII(doc);
    sanitized = redactSecrets(sanitized);
    sanitized = sanitizePaths(sanitized);
    return sanitized;
  });

  // Step 3: Add security metadata
  const secureMetadatas = metadatas.map(meta => ({
    ...meta,
    added_by: user.id,
    added_at: new Date().toISOString(),
    sanitized: true,
    department: user.department
  }));

  // Step 4: Audit log
  auditLog('add', collectionName, user.id, {
    document_count: documents.length,
    sanitized: true
  });

  // Step 5: Add to ChromaDB
  await mcp__chroma__add_documents({
    collection_name: collectionName,
    documents: sanitizedDocs,
    ids: ids,
    metadatas: secureMetadatas
  });

  return { success: true, documents_added: documents.length };
}
```

---

## Compliance Considerations

### GDPR Right to be Forgotten

```javascript
async function deleteUserData(userId, collections) {
  const hashedId = hashUserId(userId);

  for (const collectionName of collections) {
    // Find all documents by this user
    const userDocs = await mcp__chroma__get_documents({
      collection_name: collectionName,
      where: { "user_id": hashedId }
    });

    if (userDocs.ids.length > 0) {
      // Delete user's documents
      await mcp__chroma__delete_documents({
        collection_name: collectionName,
        ids: userDocs.ids
      });

      // Audit log
      auditLog('gdpr_deletion', collectionName, 'system', {
        user_id: hashedId,
        documents_deleted: userDocs.ids.length
      });
    }
  }
}
```

### Data Retention Enforcement

```javascript
async function enforceRetentionPolicy(collectionName, retentionDays) {
  const cutoffDate = new Date();
  cutoffDate.setDate(cutoffDate.getDate() - retentionDays);

  // Find old documents
  const oldDocs = await mcp__chroma__get_documents({
    collection_name: collectionName,
    where: {
      "created_at": { "$lt": cutoffDate.toISOString() }
    }
  });

  if (oldDocs.ids.length > 0) {
    // Archive before deletion (optional)
    await archiveDocuments(collectionName, oldDocs);

    // Delete old documents
    await mcp__chroma__delete_documents({
      collection_name: collectionName,
      ids: oldDocs.ids
    });

    console.log(`Deleted ${oldDocs.ids.length} documents older than ${retentionDays} days`);
  }
}
```

---

## Security Checklist

Before deploying ChromaDB with sensitive data:

- [ ] **PII Detection**: Scan all documents for PII before storage
- [ ] **Redaction**: Redact or hash PII, API keys, secrets
- [ ] **Path Sanitization**: Remove absolute paths and user identifiers
- [ ] **Access Control**: Implement collection-level permissions
- [ ] **Row-Level Security**: Filter by user department/role in queries
- [ ] **Audit Logging**: Log all operations on sensitive collections
- [ ] **Encryption**: Use HTTPS for ChromaDB connections
- [ ] **Data Retention**: Enforce retention policies and auto-deletion
- [ ] **GDPR Compliance**: Implement right to be forgotten
- [ ] **Security Review**: Review all metadata for sensitive information

---

## Antipatterns (Avoid These)

❌ **Storing raw PII**: `{ user: "john.doe@example.com", ssn: "123-45-6789" }`
✅ **Store hashed**: `{ user_hash: "a3f5c8d2", has_pii: true }`

❌ **Exposing paths**: `/home/john/secret-project/api-keys.txt`
✅ **Sanitized**: `/home/[USER]/[PROJECT]/api-keys.txt`

❌ **No access control**: Anyone can query any collection
✅ **Role-based**: Check permissions before every operation

❌ **No audit log**: Silent data access
✅ **Log all sensitive ops**: Who, what, when, why

---

**Version**: 1.0
**Created**: 2025-11-14
**Part of**: chromadb-integration-skills ecosystem
**Compliance**: GDPR, CCPA, HIPAA considerations included
