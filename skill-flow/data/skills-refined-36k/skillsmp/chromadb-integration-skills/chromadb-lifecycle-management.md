# ChromaDB Data Lifecycle Management

**Purpose**: Manage ChromaDB collections through their lifecycle - creation, growth, versioning, archival, and deletion

**Use When**: Planning long-term ChromaDB strategy, handling schema changes, or managing storage costs

---

## Collection Lifecycle Stages

```
1. Creation → 2. Active Use → 3. Mature → 4. Archive → 5. Deletion
```

**Creation**: Initial setup, ingestion starts
**Active Use**: Regular queries, frequent updates (< 100K docs)
**Mature**: Large collection (> 100K docs), slowing growth
**Archive**: Rarely queried, historical reference only
**Deletion**: No longer needed, cleanup

---

## Stage 1: Collection Creation

### Naming Convention for Versioning

```javascript
function createVersionedCollection(domain, purpose, version = 'v1') {
  const collectionName = `${domain}_${purpose}_${version}`;

  mcp__chroma__create_collection({
    collection_name: collectionName,
    embedding_function_name: "default",
    metadata: {
      version: version,
      created_at: new Date().toISOString(),
      domain: domain,
      purpose: purpose,
      lifecycle_stage: 'creation',
      schema_version: '1.0',
      retention_days: 730,  // 2 years default
      total_documents: 0
    }
  });

  return collectionName;
}

// Usage
const collection = createVersionedCollection('research', 'ml_papers', 'v1');
// Result: "research_ml_papers_v1"
```

---

## Stage 2: Active Use

### Monitor Collection Growth

```javascript
async function monitorCollectionHealth(collectionName) {
  const info = await mcp__chroma__get_collection_info({
    collection_name: collectionName
  });

  const count = await mcp__chroma__get_collection_count({
    collection_name: collectionName
  });

  const health = {
    name: collectionName,
    document_count: count,
    created_at: info.metadata.created_at,
    age_days: calculateAgeDays(info.metadata.created_at),
    size_estimate_mb: estimateSize(count),
    lifecycle_stage: determineStage(count),
    action_needed: null
  };

  // Determine actions
  if (count > 100000) {
    health.action_needed = 'CONSIDER_ARCHIVING';
  } else if (count > 50000) {
    health.action_needed = 'MONITOR_GROWTH';
  }

  return health;
}

function determineStage(documentCount) {
  if (documentCount < 10000) return 'active';
  if (documentCount < 100000) return 'mature';
  return 'archive_candidate';
}

function estimateSize(documentCount, avgDocSizeKB = 2) {
  return (documentCount * avgDocSizeKB) / 1024;  // MB
}
```

---

## Stage 3: Schema Evolution & Versioning

### Metadata Schema Migration

```javascript
async function migrateCollectionSchema(oldCollection, newSchemaVersion) {
  const newCollection = `${oldCollection}_v${newSchemaVersion}`;

  // Step 1: Create new collection with updated schema
  await mcp__chroma__create_collection({
    collection_name: newCollection,
    metadata: {
      version: `v${newSchemaVersion}`,
      migrated_from: oldCollection,
      schema_version: newSchemaVersion,
      created_at: new Date().toISOString()
    }
  });

  // Step 2: Retrieve all documents from old collection
  const allDocs = await mcp__chroma__get_documents({
    collection_name: oldCollection,
    limit: 100000,  // Adjust based on size
    include: ['documents', 'metadatas', 'embeddings']
  });

  // Step 3: Transform metadata to new schema
  const transformedMetadatas = allDocs.metadatas.map(oldMeta => {
    return transformMetadataSchema(oldMeta, newSchemaVersion);
  });

  // Step 4: Batch insert into new collection
  const BATCH_SIZE = 1000;
  for (let i = 0; i < allDocs.ids.length; i += BATCH_SIZE) {
    await mcp__chroma__add_documents({
      collection_name: newCollection,
      documents: allDocs.documents.slice(i, i + BATCH_SIZE),
      ids: allDocs.ids.slice(i, i + BATCH_SIZE),
      metadatas: transformedMetadatas.slice(i, i + BATCH_SIZE)
    });

    console.log(`Migrated ${Math.min(i + BATCH_SIZE, allDocs.ids.length)} / ${allDocs.ids.length} documents`);
  }

  // Step 5: Mark old collection as deprecated
  await mcp__chroma__modify_collection({
    collection_name: oldCollection,
    new_metadata: {
      lifecycle_stage: 'deprecated',
      deprecated_at: new Date().toISOString(),
      replacement: newCollection
    }
  });

  return { old: oldCollection, new: newCollection, documents_migrated: allDocs.ids.length };
}

function transformMetadataSchema(oldMeta, newVersion) {
  // Example schema transformation
  if (newVersion === '2.0') {
    return {
      ...oldMeta,
      // v2 adds new fields with defaults
      priority: oldMeta.priority || 'normal',
      tags: oldMeta.tags || [],
      // v2 renames field
      created_date: oldMeta.date,
      // Remove deprecated fields
      legacy_id: undefined
    };
  }

  return oldMeta;
}
```

### Versioning Strategy

```javascript
// Semantic versioning for collections
const versioningStrategy = {
  // Major version: Breaking schema changes
  major: 'Incompatible metadata structure, requires migration',

  // Minor version: Additive changes (new fields with defaults)
  minor: 'New optional fields, backward compatible',

  // Patch version: Bug fixes, no schema change
  patch: 'Documentation updates, no migration needed'
};

// Example progression:
// research_ml_papers_v1 (original)
// research_ml_papers_v1.1 (added 'tags' field with default [])
// research_ml_papers_v2 (renamed 'date' to 'created_date', requires migration)
```

---

## Stage 4: Archiving

### When to Archive

Archive when:
- Collection > 100K documents
- Query frequency < 10 queries/day
- Data is historical reference only
- Storage costs becoming significant

### Archive Process

```javascript
async function archiveCollection(collectionName) {
  const archiveName = `${collectionName}_archived_${Date.now()}`;

  // Step 1: Export to JSON (backup)
  const allDocs = await mcp__chroma__get_documents({
    collection_name: collectionName,
    limit: 1000000,
    include: ['documents', 'metadatas', 'embeddings']
  });

  const archiveData = {
    collection_name: collectionName,
    archived_at: new Date().toISOString(),
    document_count: allDocs.ids.length,
    documents: allDocs.documents,
    ids: allDocs.ids,
    metadatas: allDocs.metadatas,
    embeddings: allDocs.embeddings
  };

  // Write to file system or object storage
  await writeJSONFile(`/archives/${archiveName}.json`, archiveData);
  console.log(`Archived ${allDocs.ids.length} documents to ${archiveName}.json`);

  // Step 2: Create archived collection (read-only, compressed)
  await mcp__chroma__create_collection({
    collection_name: archiveName,
    metadata: {
      lifecycle_stage: 'archived',
      original_collection: collectionName,
      archived_at: new Date().toISOString(),
      read_only: true,
      document_count: allDocs.ids.length
    }
  });

  // Step 3: Add documents to archived collection
  await mcp__chroma__add_documents({
    collection_name: archiveName,
    documents: allDocs.documents,
    ids: allDocs.ids,
    metadatas: allDocs.metadatas
  });

  // Step 4: Delete active collection (after verification)
  console.log(`MANUAL STEP: Verify archive ${archiveName} before deleting ${collectionName}`);

  return { archive_name: archiveName, document_count: allDocs.ids.length };
}
```

### Restore from Archive

```javascript
async function restoreFromArchive(archiveName) {
  // Read from archived JSON
  const archiveData = await readJSONFile(`/archives/${archiveName}.json`);

  // Recreate collection
  const restoredName = archiveData.collection_name;
  await mcp__chroma__create_collection({
    collection_name: restoredName,
    metadata: {
      restored_from: archiveName,
      restored_at: new Date().toISOString(),
      original_created_at: archiveData.archived_at
    }
  });

  // Batch restore documents
  await mcp__chroma__add_documents({
    collection_name: restoredName,
    documents: archiveData.documents,
    ids: archiveData.ids,
    metadatas: archiveData.metadatas
  });

  return { restored: restoredName, document_count: archiveData.ids.length };
}
```

---

## Stage 5: Retention & Deletion

### Auto-Deletion Based on Retention Policy

```javascript
async function enforceRetentionPolicies() {
  const collections = await mcp__chroma__list_collections();

  for (const collectionName of collections) {
    const info = await mcp__chroma__get_collection_info({
      collection_name: collectionName
    });

    const retentionDays = info.metadata.retention_days || 730;  // Default 2 years
    const createdAt = new Date(info.metadata.created_at);
    const ageDays = (Date.now() - createdAt.getTime()) / (1000 * 60 * 60 * 24);

    if (ageDays > retentionDays) {
      console.log(`Collection ${collectionName} exceeded retention (${ageDays} > ${retentionDays} days)`);

      // Archive before deletion
      await archiveCollection(collectionName);

      // Delete active collection
      await mcp__chroma__delete_collection({
        collection_name: collectionName
      });

      console.log(`Deleted collection ${collectionName} (archived first)`);
    }
  }
}
```

### Safe Deletion with Confirmation

```javascript
async function safeDeleteCollection(collectionName, confirmationCode) {
  // Step 1: Verify confirmation code
  const expectedCode = hashString(collectionName).substring(0, 6);
  if (confirmationCode !== expectedCode) {
    throw new Error(
      `Confirmation code mismatch. To delete ${collectionName}, ` +
      `provide code: ${expectedCode}`
    );
  }

  // Step 2: Final backup
  await archiveCollection(collectionName);

  // Step 3: Delete
  await mcp__chroma__delete_collection({
    collection_name: collectionName
  });

  console.log(`Deleted collection ${collectionName} permanently`);
}

// Usage
// await safeDeleteCollection('old_collection', 'a3f5c8');  // Must match hash
```

---

## Lifecycle Automation

### Scheduled Maintenance Tasks

```javascript
// Run daily at midnight
async function dailyMaintenanceTasks() {
  console.log('Starting ChromaDB maintenance...');

  // Task 1: Monitor collection health
  const collections = await mcp__chroma__list_collections();
  for (const collection of collections) {
    const health = await monitorCollectionHealth(collection);

    if (health.action_needed === 'CONSIDER_ARCHIVING') {
      console.log(`⚠️ ${collection}: Consider archiving (${health.document_count} docs)`);
    }
  }

  // Task 2: Enforce retention policies
  await enforceRetentionPolicies();

  // Task 3: Clean up deprecated collections
  await cleanupDeprecatedCollections();

  console.log('Maintenance complete');
}

async function cleanupDeprecatedCollections() {
  const collections = await mcp__chroma__list_collections();

  for (const collectionName of collections) {
    const info = await mcp__chroma__get_collection_info({
      collection_name: collectionName
    });

    if (info.metadata.lifecycle_stage === 'deprecated') {
      const deprecatedAt = new Date(info.metadata.deprecated_at);
      const daysSince = (Date.now() - deprecatedAt.getTime()) / (1000 * 60 * 60 * 24);

      if (daysSince > 30) {
        console.log(`Deleting deprecated collection: ${collectionName} (deprecated ${daysSince} days ago)`);
        await mcp__chroma__delete_collection({ collection_name: collectionName });
      }
    }
  }
}
```

---

## Lifecycle Management Checklist

- [ ] **Versioning**: Use semantic versioning (v1, v1.1, v2)
- [ ] **Metadata**: Include lifecycle_stage, created_at, retention_days
- [ ] **Monitoring**: Track document count, query frequency, age
- [ ] **Migration**: Plan schema changes, test migration process
- [ ] **Archiving**: Export to JSON before deletion
- [ ] **Retention**: Enforce retention policies automatically
- [ ] **Cleanup**: Delete deprecated collections after grace period
- [ ] **Backup**: Regular backups to object storage
- [ ] **Documentation**: Document schema changes and migration paths

---

**Version**: 1.0
**Created**: 2025-11-14
**Part of**: chromadb-integration-skills ecosystem
