# Enterprise Context Management

Multi-tenant, compliant, and scalable context systems for enterprise AI.

## Enterprise Requirements

| Requirement      | Description                              | Priority |
| ---------------- | ---------------------------------------- | -------- |
| Multi-tenancy    | Isolated contexts per tenant/project     | Critical |
| Compliance       | Audit trails, data retention, privacy    | Critical |
| Scale            | Handle 10M+ documents, 1000+ users       | High     |
| Integration      | Connect to enterprise knowledge systems  | High     |
| Security         | Access control, encryption, governance   | Critical |

## Multi-Tenant Architecture

```
┌─────────────────────────────────────────────────┐
│              Context Management Layer            │
├─────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐         │
│  │Tenant A │  │Tenant B │  │Tenant C │ ...     │
│  ├─────────┤  ├─────────┤  ├─────────┤         │
│  │ Context │  │ Context │  │ Context │         │
│  │  Store  │  │  Store  │  │  Store  │         │
│  └─────────┘  └─────────┘  └─────────┘         │
├─────────────────────────────────────────────────┤
│           Shared Infrastructure                  │
│  Vector DB  │  Knowledge Graph  │  Audit Log    │
└─────────────────────────────────────────────────┘
```

## Context Isolation

```python
class TenantContextManager:
    def __init__(self, tenant_id):
        self.tenant_id = tenant_id
        self.context_prefix = f"tenant:{tenant_id}:"

    def get_context(self, context_id):
        """Get context with tenant isolation."""
        full_id = f"{self.context_prefix}{context_id}"
        context = self.store.get(full_id)

        # Verify tenant ownership
        if context and context.get('tenant_id') != self.tenant_id:
            raise PermissionError("Context belongs to different tenant")

        return context

    def save_context(self, context_id, context):
        """Save context with tenant metadata."""
        context['tenant_id'] = self.tenant_id
        context['saved_at'] = datetime.utcnow().isoformat()
        full_id = f"{self.context_prefix}{context_id}"
        self.store.set(full_id, context)
        self.audit_log.log('context_save', self.tenant_id, context_id)
```

## Compliance & Audit

```python
class ComplianceAuditLog:
    def __init__(self, storage):
        self.storage = storage

    def log(self, action, tenant_id, context_id, user_id=None, details=None):
        """Log all context operations for compliance."""
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'action': action,
            'tenant_id': tenant_id,
            'context_id': context_id,
            'user_id': user_id,
            'details': details,
            'ip_address': get_request_ip(),
            'session_id': get_session_id()
        }
        self.storage.append(entry)

    def get_audit_trail(self, context_id, start_date=None, end_date=None):
        """Retrieve audit trail for compliance reporting."""
        query = {'context_id': context_id}
        if start_date:
            query['timestamp'] = {'$gte': start_date}
        if end_date:
            query['timestamp']['$lte'] = end_date
        return self.storage.query(query)
```

## Data Retention Policies

```python
class RetentionPolicy:
    def __init__(self, tenant_config):
        self.config = tenant_config

    def apply(self, context):
        """Apply retention policies to context."""
        retention_days = self.config.get('retention_days', 90)
        context_age = self.calculate_age(context)

        if context_age > retention_days:
            if self.config.get('archive_before_delete', True):
                self.archive(context)
            return self.delete(context)

        # Apply PII scrubbing if required
        if self.config.get('scrub_pii', False):
            context = self.scrub_pii(context)

        return context

    def scrub_pii(self, context):
        """Remove personally identifiable information."""
        pii_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'  # Phone
        ]
        # Apply patterns...
        return scrubbed_context
```

## Enterprise Integrations

### SharePoint Integration

```python
class SharePointContextSource:
    def __init__(self, client_id, client_secret, tenant_id):
        self.auth = SharePointAuth(client_id, client_secret, tenant_id)

    def fetch_documents(self, site_id, folder_path):
        """Fetch documents from SharePoint for context."""
        token = self.auth.get_token()
        docs = self.client.get_folder_contents(site_id, folder_path)

        contexts = []
        for doc in docs:
            content = self.client.get_document_content(doc.id)
            contexts.append({
                'source': 'sharepoint',
                'source_id': doc.id,
                'title': doc.name,
                'content': extract_text(content),
                'metadata': {
                    'author': doc.created_by,
                    'modified': doc.modified_at,
                    'path': doc.web_url
                }
            })

        return contexts
```

### Confluence Integration

```python
class ConfluenceContextSource:
    def __init__(self, base_url, api_token):
        self.client = ConfluenceClient(base_url, api_token)

    def fetch_space_content(self, space_key, content_type='page'):
        """Fetch Confluence pages for context."""
        pages = self.client.get_space_content(space_key, content_type)

        contexts = []
        for page in pages:
            body = self.client.get_page_body(page.id)
            contexts.append({
                'source': 'confluence',
                'source_id': page.id,
                'title': page.title,
                'content': html_to_text(body),
                'metadata': {
                    'space': space_key,
                    'labels': page.labels,
                    'version': page.version,
                    'last_modified': page.updated
                }
            })

        return contexts
```

### Notion Integration

```python
class NotionContextSource:
    def __init__(self, integration_token):
        self.client = NotionClient(integration_token)

    def fetch_database_pages(self, database_id):
        """Fetch Notion database pages for context."""
        pages = self.client.query_database(database_id)

        contexts = []
        for page in pages:
            blocks = self.client.get_page_blocks(page.id)
            contexts.append({
                'source': 'notion',
                'source_id': page.id,
                'title': page.title,
                'content': blocks_to_text(blocks),
                'properties': page.properties,
                'metadata': {
                    'created': page.created_time,
                    'last_edited': page.last_edited_time
                }
            })

        return contexts
```

## Scalable Infrastructure

```yaml
# Context Management Infrastructure
services:
  context-api:
    replicas: 3
    resources:
      cpu: "2"
      memory: "4Gi"
    autoscaling:
      min: 3
      max: 10
      target_cpu: 70%

  vector-db:
    type: pinecone  # or weaviate, qdrant
    pods: 2
    replicas: 2
    pod_type: p2.x2

  knowledge-graph:
    type: neo4j
    cluster_size: 3
    memory: "16Gi"

  cache:
    type: redis-cluster
    nodes: 6
    memory: "8Gi"
```

## Access Control

```python
class ContextAccessControl:
    def __init__(self, policy_engine):
        self.policy = policy_engine

    def can_access(self, user, context, action):
        """Check if user can perform action on context."""
        permissions = self.policy.get_user_permissions(user.id)

        # Check tenant access
        if context.tenant_id not in user.tenant_access:
            return False

        # Check role-based permissions
        required_role = self.get_required_role(action)
        if required_role not in user.roles:
            return False

        # Check resource-level permissions
        if context.restricted:
            return context.allowed_users.contains(user.id)

        return True

    def filter_contexts(self, user, contexts):
        """Filter contexts to only those user can access."""
        return [c for c in contexts if self.can_access(user, c, 'read')]
```

## Guidelines

1. Implement strict tenant isolation at all layers
2. Log all context operations for audit compliance
3. Apply retention policies automatically
4. Integrate with existing enterprise knowledge systems
5. Use caching to handle scale
6. Implement fine-grained access control
7. Support data residency requirements
8. Enable PII scrubbing for sensitive contexts

## Related

- [Context Save](./context-save.md)
- [Context Restore](./context-restore.md)
- [Vector Databases](./vector-databases.md)
