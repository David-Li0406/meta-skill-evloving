# ChromaDB Testing Patterns

**Purpose**: Comprehensive testing strategies for ChromaDB integrations

**Use When**: Writing tests for agents using ChromaDB, validating semantic search accuracy

---

## Testing Strategy

### Test Pyramid for ChromaDB

```
        E2E Tests (10%)
       /               \
      /  Integration    \
     /    Tests (30%)    \
    /                     \
   /_______________________\
   Unit Tests (60%)
```

**60% Unit Tests**: Mock ChromaDB, test logic in isolation
**30% Integration Tests**: Real ChromaDB, test full workflows
**10% E2E Tests**: Complete agent workflows with real data

---

## Unit Tests (Mock ChromaDB)

### Mock Setup

```javascript
// mock-chroma.js
class MockChromaDB {
  constructor() {
    this.collections = {};
  }

  create_collection({ collection_name, metadata }) {
    if (this.collections[collection_name]) {
      throw new Error(`Collection ${collection_name} already exists`);
    }
    this.collections[collection_name] = {
      documents: [],
      ids: [],
      metadatas: [],
      metadata: metadata
    };
  }

  add_documents({ collection_name, documents, ids, metadatas }) {
    const collection = this.collections[collection_name];
    if (!collection) {
      throw new Error(`Collection ${collection_name} not found`);
    }
    collection.documents.push(...documents);
    collection.ids.push(...ids);
    collection.metadatas.push(...metadatas);
  }

  query_documents({ collection_name, query_texts, n_results, where }) {
    const collection = this.collections[collection_name];
    if (!collection) {
      throw new Error(`Collection ${collection_name} not found`);
    }

    // Simple mock: return first n documents
    return {
      ids: [collection.ids.slice(0, n_results)],
      documents: [collection.documents.slice(0, n_results)],
      metadatas: [collection.metadatas.slice(0, n_results)],
      distances: [collection.ids.slice(0, n_results).map(() => 0.2)]
    };
  }

  list_collections() {
    return Object.keys(this.collections);
  }
}

// Export mock
global.mockChroma = new MockChromaDB();
```

### Unit Test Examples

```javascript
// test-collection-creation.js
import { mockChroma } from './mock-chroma';
import { createResearchCollection } from '../agent';

describe('ChromaDB Collection Creation', () => {
  beforeEach(() => {
    mockChroma.collections = {};  // Reset
  });

  test('creates collection with correct metadata', () => {
    const result = createResearchCollection('ml_transformers');

    expect(mockChroma.list_collections()).toContain('research_literature_ml_transformers');
    expect(mockChroma.collections['research_literature_ml_transformers'].metadata)
      .toHaveProperty('topic', 'ML Transformers');
  });

  test('handles duplicate collection creation', () => {
    createResearchCollection('ml_transformers');

    expect(() => {
      createResearchCollection('ml_transformers');
    }).toThrow('Collection research_literature_ml_transformers already exists');
  });
});
```

```javascript
// test-document-ingestion.js
describe('Document Ingestion', () => {
  test('validates document format before adding', () => {
    const invalidDoc = { title: 'Missing text field' };

    expect(() => {
      addDocumentToCollection('my_collection', invalidDoc);
    }).toThrow('Document must be string');
  });

  test('generates unique IDs for documents', () => {
    const doc1 = addDocument('Test document');
    const doc2 = addDocument('Test document');  // Same content

    expect(doc1.id).not.toBe(doc2.id);  // IDs should differ
  });

  test('batches documents efficiently', () => {
    const docs = Array(250).fill('Test doc');
    const spy = jest.spyOn(mockChroma, 'add_documents');

    batchAddDocuments('my_collection', docs);

    // Should batch into 3 calls (100, 100, 50)
    expect(spy).toHaveBeenCalledTimes(3);
  });
});
```

---

## Integration Tests (Real ChromaDB)

### Setup Real ChromaDB Instance

```javascript
// test-setup.js
import { ChromaClient } from 'chromadb';

let chromaClient;

beforeAll(async () => {
  chromaClient = new ChromaClient({
    path: 'http://localhost:8000'  // Local test instance
  });
});

afterAll(async () => {
  // Cleanup: Delete test collections
  const collections = await chromaClient.listCollections();
  for (const collection of collections) {
    if (collection.name.startsWith('test_')) {
      await chromaClient.deleteCollection({ name: collection.name });
    }
  }
});
```

### Integration Test Examples

```javascript
// integration-test-semantic-search.js
describe('ChromaDB Semantic Search Integration', () => {
  let collectionName;

  beforeEach(async () => {
    collectionName = `test_semantic_${Date.now()}`;
    await chromaClient.createCollection({ name: collectionName });
  });

  test('semantic search returns relevant documents', async () => {
    // Add documents
    await chromaClient.add({
      collection_name: collectionName,
      documents: [
        'Machine learning uses neural networks for pattern recognition',
        'Deep learning is a subset of machine learning using multiple layers',
        'Python is a programming language used for data science',
        'JavaScript is used for web development and frontend frameworks'
      ],
      ids: ['doc1', 'doc2', 'doc3', 'doc4']
    });

    // Query
    const results = await chromaClient.query({
      collection_name: collectionName,
      query_texts: ['neural networks and deep learning'],
      n_results: 2
    });

    // Assertions
    expect(results.ids[0]).toContain('doc1');  // ML neural networks
    expect(results.ids[0]).toContain('doc2');  // Deep learning
    expect(results.distances[0][0]).toBeLessThan(0.4);  // High relevance
  });

  test('metadata filters work correctly', async () => {
    await chromaClient.add({
      collection_name: collectionName,
      documents: ['Doc 1', 'Doc 2', 'Doc 3'],
      ids: ['1', '2', '3'],
      metadatas: [
        { year: 2023, category: 'A' },
        { year: 2024, category: 'A' },
        { year: 2024, category: 'B' }
      ]
    });

    const results = await chromaClient.query({
      collection_name: collectionName,
      query_texts: ['Doc'],
      where: { year: 2024, category: 'A' },
      n_results: 10
    });

    expect(results.ids[0]).toEqual(['2']);  // Only doc2 matches filter
  });
});
```

### Edge Case Tests

```javascript
describe('ChromaDB Edge Cases', () => {
  test('handles empty collection queries', async () => {
    const emptyCollection = `test_empty_${Date.now()}`;
    await chromaClient.createCollection({ name: emptyCollection });

    const results = await chromaClient.query({
      collection_name: emptyCollection,
      query_texts: ['test query'],
      n_results: 10
    });

    expect(results.ids[0]).toEqual([]);
    expect(results.documents[0]).toEqual([]);
  });

  test('handles large batch inserts (1000+ documents)', async () => {
    const largeBatch = Array(1500).fill(0).map((_, i) => `Document ${i}`);
    const ids = largeBatch.map((_, i) => `doc_${i}`);

    await chromaClient.add({
      collection_name: collectionName,
      documents: largeBatch,
      ids: ids
    });

    const count = await chromaClient.count({ collection_name: collectionName });
    expect(count).toBe(1500);
  });

  test('handles special characters in documents', async () => {
    const specialDoc = 'Document with "quotes", <tags>, and émojis 🚀';

    await chromaClient.add({
      collection_name: collectionName,
      documents: [specialDoc],
      ids: ['special']
    });

    const results = await chromaClient.get({
      collection_name: collectionName,
      ids: ['special']
    });

    expect(results.documents[0]).toBe(specialDoc);
  });
});
```

---

## Semantic Search Accuracy Tests

### Distance Threshold Validation

```javascript
describe('Distance Threshold Tuning', () => {
  beforeAll(async () => {
    // Add known similar and dissimilar documents
    await chromaClient.add({
      collection_name: testCollection,
      documents: [
        'Machine learning and artificial intelligence',  // Similar to query
        'Machine learning algorithms',                   // Similar to query
        'Python programming language',                   // Dissimilar
        'Cooking recipes for pasta'                      // Very dissimilar
      ],
      ids: ['sim1', 'sim2', 'dissim1', 'dissim2']
    });
  });

  test('distance < 0.3 returns highly similar documents', async () => {
    const results = await chromaClient.query({
      collection_name: testCollection,
      query_texts: ['machine learning'],
      n_results: 10
    });

    const highlyRelevant = results.ids[0].filter((id, idx) =>
      results.distances[0][idx] < 0.3
    );

    expect(highlyRelevant).toContain('sim1');
    expect(highlyRelevant).toContain('sim2');
    expect(highlyRelevant).not.toContain('dissim1');
    expect(highlyRelevant).not.toContain('dissim2');
  });
});
```

### Precision and Recall Tests

```javascript
describe('Semantic Search Quality Metrics', () => {
  test('achieves >80% precision on known dataset', async () => {
    // Ground truth: Documents 1-5 are relevant, 6-10 are not
    const relevantIds = ['doc1', 'doc2', 'doc3', 'doc4', 'doc5'];

    const results = await chromaClient.query({
      collection_name: testCollection,
      query_texts: ['relevant query'],
      n_results: 10
    });

    const retrievedIds = results.ids[0];
    const truePositives = retrievedIds.filter(id => relevantIds.includes(id)).length;
    const precision = truePositives / retrievedIds.length;

    expect(precision).toBeGreaterThan(0.8);  // 80% precision target
  });
});
```

---

## Test Fixtures

### Sample Documents

```javascript
// test-fixtures.js
export const sampleDocuments = {
  research: [
    {
      id: 'paper1',
      document: 'Attention Is All You Need. Introduces transformer architecture.',
      metadata: { year: 2017, citations: 50000, venue: 'NIPS' }
    },
    {
      id: 'paper2',
      document: 'BERT: Pre-training of Deep Bidirectional Transformers.',
      metadata: { year: 2018, citations: 40000, venue: 'NAACL' }
    }
  ],

  bugs: [
    {
      id: 'bug1',
      document: 'Bug #123: Authentication fails with 401 after password reset',
      metadata: { severity: 'high', status: 'resolved', component: 'auth' }
    },
    {
      id: 'bug2',
      document: 'Bug #456: Session expires prematurely after 5 minutes',
      metadata: { severity: 'medium', status: 'resolved', component: 'auth' }
    }
  ]
};
```

### Assertion Helpers

```javascript
// test-helpers.js
export function assertSemanticMatch(results, expectedIds, threshold = 0.4) {
  const retrievedIds = results.ids[0];
  const distances = results.distances[0];

  expectedIds.forEach(expectedId => {
    const index = retrievedIds.indexOf(expectedId);
    expect(index).toBeGreaterThanOrEqual(0);  // ID found
    expect(distances[index]).toBeLessThan(threshold);  // Within threshold
  });
}

export function assertMetadataFilter(results, expectedMetadata) {
  results.metadatas[0].forEach(metadata => {
    for (const [key, value] of Object.entries(expectedMetadata)) {
      expect(metadata[key]).toBe(value);
    }
  });
}
```

---

## End-to-End Tests

### Full Agent Workflow Test

```javascript
describe('Research Agent E2E', () => {
  test('complete research workflow: ingest → query → cross-validate', async () => {
    // Step 1: Ingest research papers
    const papers = await fetchPapersFromAPI('machine learning');
    await ingestResearchPapers('ml_research', papers);

    // Step 2: Semantic query
    const results = await findSimilarPapers('attention mechanisms');

    // Step 3: Cross-validate with historical research
    const validated = await crossValidateFindings(results);

    // Assertions
    expect(results.length).toBeGreaterThan(0);
    expect(validated.consistency_score).toBeGreaterThan(0.8);
  });
});
```

---

## Testing Checklist

- [ ] **Unit Tests**: Mock ChromaDB, test logic (60% coverage)
- [ ] **Integration Tests**: Real ChromaDB, test workflows (30% coverage)
- [ ] **E2E Tests**: Full agent workflows (10% coverage)
- [ ] **Semantic Accuracy**: Distance thresholds validated
- [ ] **Edge Cases**: Empty collections, large batches, special chars
- [ ] **Error Handling**: Connection failures, validation errors
- [ ] **Performance**: Batch operations, query optimization
- [ ] **Cleanup**: Delete test collections after tests

---

**Version**: 1.0
**Created**: 2025-11-14
**Part of**: chromadb-integration-skills ecosystem
