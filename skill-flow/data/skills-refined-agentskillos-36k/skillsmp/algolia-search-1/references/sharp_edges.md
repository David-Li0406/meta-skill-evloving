# Algolia Search - Sharp Edges

## Admin API Key in Frontend Code

### **Id**
admin-key-exposure
### **Severity**
critical
### **Description**
  The Admin API key provides full control over your Algolia indices,
  including the ability to delete all data. If exposed in frontend code,
  attackers can view, modify, or delete your entire search index.
  
### **Wrong Way**
  // DISASTER: Admin key in client code
  const client = algoliasearch(
    process.env.NEXT_PUBLIC_ALGOLIA_APP_ID,
    process.env.NEXT_PUBLIC_ALGOLIA_ADMIN_KEY  // EXPOSED!
  );
  
  // Attacker can now do this:
  // client.deleteIndex('products');
  // client.clearObjects('products');
  
### **Right Way**
  // Frontend: Search-only key only
  const searchClient = algoliasearch(
    process.env.NEXT_PUBLIC_ALGOLIA_APP_ID!,
    process.env.NEXT_PUBLIC_ALGOLIA_SEARCH_KEY!  // Search only
  );
  
  // Backend: Admin key for indexing
  // lib/algolia-admin.ts (server-only file)
  const adminClient = algoliasearch(
    process.env.ALGOLIA_APP_ID!,
    process.env.ALGOLIA_ADMIN_KEY!  // Never exposed to client
  );
  
  // Even better: Use secured API keys for user-specific access
  const securedKey = adminClient.generateSecuredApiKey(searchKey, {
    filters: `userId:${userId}`,
    validUntil: Math.floor(Date.now() / 1000) + 3600,
  });
  
### **Detection Patterns**
  - ADMIN_KEY.*NEXT_PUBLIC
  - ALGOLIA_ADMIN.*client
  - admin.*searchClient
### **References**
  - https://www.algolia.com/doc/guides/security/api-keys

## Indexing Rate Limits and Throttling

### **Id**
rate-limit-indexing
### **Severity**
high
### **Description**
  Algolia limits indexing operations to 10,000 per unit. When limits
  are hit, the API returns HTTP 429 errors. Indexing is deprioritized
  vs search during high load, causing delays.
  
  deleteBy is especially expensive and heavily rate-limited.
  
### **Wrong Way**
  // One-at-a-time indexing - creates queue backup
  for (const product of products) {
    await index.saveObject(product);  // 10K calls = 10K operations
  }
  
  // Using deleteBy for cleanup - very expensive
  await index.deleteBy({
    filters: 'category:deprecated',
  });  // Can trigger rate limit quickly
  
### **Right Way**
  // Batch indexing - much more efficient
  const BATCH_SIZE = 1000;
  
  for (let i = 0; i < products.length; i += BATCH_SIZE) {
    const batch = products.slice(i, i + BATCH_SIZE);
    await index.saveObjects(batch);
  
    // Optional: Add delay between batches if hitting limits
    if (i + BATCH_SIZE < products.length) {
      await new Promise(r => setTimeout(r, 100));
    }
  }
  
  // Delete by objectID instead of deleteBy
  const idsToDelete = await getDeprecatedProductIds();
  await index.deleteObjects(idsToDelete);
  
  // Handle rate limit errors
  try {
    await index.saveObjects(records);
  } catch (error) {
    if (error.status === 429) {
      console.log('Rate limited, waiting...');
      await new Promise(r => setTimeout(r, 5000));
      await index.saveObjects(records);  // Retry
    }
    throw error;
  }
  
### **Detection Patterns**
  - saveObject\((?!s)
  - deleteBy\(
  - for.*await.*saveObject
### **References**
  - https://support.algolia.com/hc/en-us/articles/4406975251089-Is-there-a-rate-limit-for-indexing-on-Algolia
  - https://www.algolia.com/doc/guides/scaling/algolia-service-limits

## Record Size and Index Limits

### **Id**
record-size-limits
### **Severity**
medium
### **Description**
  Each record has a 100KB size limit. The total index size affects
  pricing and performance. Large attributes (descriptions, HTML)
  should be truncated or excluded.
  
### **Wrong Way**
  // Indexing large HTML content
  await index.saveObject({
    objectID: article.id,
    title: article.title,
    content: article.fullHtmlContent,  // Could be > 100KB!
    rawData: JSON.stringify(article),  // Unnecessary data
  });
  
### **Right Way**
  // Truncate and extract searchable content
  function prepareRecord(article: Article) {
    // Strip HTML and truncate
    const textContent = stripHtml(article.content);
    const truncated = textContent.slice(0, 10000);  // ~10KB max
  
    return {
      objectID: article.id,
      title: article.title,
      excerpt: textContent.slice(0, 500),  // For display
      content: truncated,  // For search
      // Don't index non-searchable data
      // Store URL to fetch full content when needed
      url: `/articles/${article.slug}`,
    };
  }
  
  // Check record size before indexing
  function validateRecordSize(record: object): boolean {
    const size = Buffer.byteLength(JSON.stringify(record));
    if (size > 100000) {  // 100KB limit
      console.warn(`Record too large: ${size} bytes`);
      return false;
    }
    return true;
  }
  
### **Detection Patterns**
  - innerHTML.*saveObject
  - fullContent.*saveObject
  - JSON\.stringify.*saveObject
### **References**
  - https://www.algolia.com/doc-beta/guides/sending-and-managing-data/prepare-your-data/in-depth/index-and-records-size-and-usage-limitations

## PII in Index Names Visible in Network

### **Id**
pii-in-index-names
### **Severity**
medium
### **Description**
  Index names appear in network requests and are publicly visible.
  Never include personally identifiable information (PII) or
  sensitive data in index names.
  
### **Wrong Way**
  // Index names with PII - visible in network tab
  const index = client.initIndex(`user_${userId}_documents`);
  const index = client.initIndex(`company_${companyName}_products`);
  
### **Right Way**
  // Generic index names with filtering
  const index = client.initIndex('documents');
  
  // Use filters for user-specific data
  const results = await index.search('query', {
    filters: `userId:${userId}`,
  });
  
  // Or use secured API keys to restrict access
  const securedKey = client.generateSecuredApiKey(searchKey, {
    filters: `userId:${userId}`,
  });
  
### **Detection Patterns**
  - initIndex.*userId
  - initIndex.*email
  - initIndex.*\$\{.*\}
### **References**
  - https://www.algolia.com/doc/libraries/javascript/v5/methods/search/

## Searchable Attributes Order Affects Relevance

### **Id**
searchable-attributes-order
### **Severity**
medium
### **Description**
  The order of searchableAttributes determines matching priority.
  Attributes listed first have higher weight. Not configuring this
  means all attributes are searched equally, reducing relevance.
  
### **Wrong Way**
  // No searchable attributes configured
  // All fields searched equally - poor relevance
  
  // Or wrong order - description matches rank same as title
  await index.setSettings({
    searchableAttributes: [
      'description',  // Should be last
      'title',        // Should be first
      'category',
    ],
  });
  
### **Right Way**
  // Ordered by importance
  await index.setSettings({
    searchableAttributes: [
      'title',            // Most important - exact product name
      'brand',            // Second - brand matching
      'category',         // Third - category matching
      'tags',             // Fourth - tags/keywords
      'description',      // Last - general text
    ],
  });
  
  // Unordered attributes (same priority)
  await index.setSettings({
    searchableAttributes: [
      'title',
      'unordered(synonyms)',  // Same priority as title
      'description',
    ],
  });
  
### **Detection Patterns**
  - searchableAttributes.*description.*title
### **References**
  - https://www.algolia.com/doc/guides/managing-results/relevance-overview/in-depth/ranking-criteria/#searchable-attributes

## Full Reindex Consumes All Operations

### **Id**
full-reindex-operations
### **Severity**
medium
### **Description**
  Full reindexing replaces all records, consuming operations for
  every record. If you have 100K records and reindex daily, that's
  3M operations/month just for syncing unchanged data.
  
### **Wrong Way**
  // Daily full reindex - wastes operations
  async function dailySync() {
    const allProducts = await db.products.findMany();
  
    // Deletes all, reindexes all
    await index.replaceAllObjects(allProducts);
  }
  
### **Right Way**
  // Incremental sync based on changes
  async function incrementalSync(lastSyncTime: Date) {
    // Only changed records
    const updated = await db.products.findMany({
      where: { updatedAt: { gt: lastSyncTime } },
    });
  
    if (updated.length > 0) {
      await index.saveObjects(updated);
    }
  
    // Deleted records
    const deleted = await db.deletedProducts.findMany({
      where: { deletedAt: { gt: lastSyncTime } },
    });
  
    if (deleted.length > 0) {
      await index.deleteObjects(deleted.map(d => d.id));
    }
  
    await saveLastSyncTime(new Date());
  }
  
  // Partial updates for specific field changes
  async function updatePrice(productId: string, price: number) {
    await index.partialUpdateObject({
      objectID: productId,
      price,
      updatedAt: Date.now(),
    });
  }
  
### **Detection Patterns**
  - replaceAllObjects
  - clearIndex.*saveObjects
### **References**
  - https://www.algolia.com/doc/guides/sending-and-managing-data/send-and-update-your-data/in-depth/the-different-synchronization-strategies

## Every Keystroke Counts as Search Operation

### **Id**
search-counts-operations
### **Severity**
medium
### **Description**
  In search-as-you-type implementations, every keystroke triggers
  a search operation. A user typing "laptop" = 6 operations.
  Without rate limiting, bots can exhaust your quota quickly.
  
### **Wrong Way**
  // No rate limiting on search API key
  const searchClient = algoliasearch(appId, publicSearchKey);
  
  // No debouncing on custom implementation
  input.addEventListener('keyup', () => {
    index.search(input.value);  // Fires on every keystroke
  });
  
### **Right Way**
  // Create rate-limited search key
  const { key } = await adminClient.addApiKey({
    acl: ['search'],
    indexes: ['products'],
    maxQueriesPerIPPerHour: 1000,  // Limit per IP
  });
  
  // InstantSearch handles debouncing automatically
  <SearchBox
    searchAsYouType={true}  // Built-in debouncing
  />
  
  // Manual debouncing for custom implementations
  import { debounce } from 'lodash';
  
  const debouncedSearch = debounce(
    (query: string) => index.search(query),
    300  // Wait 300ms after last keystroke
  );
  
  input.addEventListener('keyup', () => {
    debouncedSearch(input.value);
  });
  
### **Detection Patterns**
  - keyup.*search\(
  - onChange.*search\(
  - search\(.*value\)
### **References**
  - https://support.algolia.com/hc/en-us/articles/4905140190353-How-can-I-rate-limit-an-API-key

## SSR Hydration Mismatch with InstantSearch

### **Id**
ssr-hydration-mismatch
### **Severity**
medium
### **Description**
  Using regular InstantSearch with Next.js SSR causes hydration
  mismatches. Server renders empty, client renders results.
  Must use react-instantsearch-nextjs package.
  
### **Wrong Way**
  // Regular InstantSearch in Next.js - hydration mismatch
  import { InstantSearch } from 'react-instantsearch';
  
  export default function SearchPage() {
    return (
      <InstantSearch searchClient={client} indexName="products">
        <SearchBox />
        <Hits />  // Different content on server vs client
      </InstantSearch>
    );
  }
  
### **Right Way**
  // Use Next.js-specific package
  import { InstantSearchNext } from 'react-instantsearch-nextjs';
  
  // Force dynamic rendering
  export const dynamic = 'force-dynamic';
  
  export default function SearchPage() {
    return (
      <InstantSearchNext
        searchClient={client}
        indexName="products"
      >
        <SearchBox />
        <Hits />
      </InstantSearchNext>
    );
  }
  
### **Detection Patterns**
  - import.*InstantSearch.*from 'react-instantsearch'
  - InstantSearch.*Next\.js
### **References**
  - https://www.npmjs.com/package/react-instantsearch-nextjs
  - https://github.com/algolia/instantsearch/discussions/5413

## Replica Indices for Sorting Multiply Storage

### **Id**
replica-indices-cost
### **Severity**
low
### **Description**
  Each sort option requires a replica index (copy of your data).
  4 sort options = 5x storage (primary + 4 replicas). This affects
  pricing and requires syncing replicas during indexing.
  
### **Wrong Way**
  // Creating many replicas without considering cost
  await index.setSettings({
    replicas: [
      'products_price_asc',
      'products_price_desc',
      'products_rating_asc',
      'products_rating_desc',
      'products_date_asc',
      'products_date_desc',  // 6 replicas = 7x storage!
    ],
  });
  
### **Right Way**
  // Only create replicas for essential sort options
  await index.setSettings({
    replicas: [
      'products_price_asc',    // Essential: price low to high
      'products_rating_desc',  // Essential: top rated
    ],
    // Primary index handles relevance (default sort)
  });
  
  // Or use virtual replicas (less storage, more compute)
  await index.setSettings({
    replicas: [
      'virtual(products_price_asc)',
      'virtual(products_rating_desc)',
    ],
  });
  
  // Consider if customRanking can achieve the sort
  // without replicas (for single-sort scenarios)
  
### **Detection Patterns**
  - replicas.*\[.*,.*,.*,.*,.*\]
### **References**
  - https://www.algolia.com/doc/guides/managing-results/refine-results/sorting/in-depth/replicas/

## Faceting Requires attributesForFaceting Declaration

### **Id**
facet-attribute-not-declared
### **Severity**
medium
### **Description**
  RefinementList, Menu, and other facet widgets require attributes
  to be declared in attributesForFaceting. Without this, facet
  values won't appear and filtering fails silently.
  
### **Wrong Way**
  // Using RefinementList without configuring faceting
  <RefinementList attribute="category" />  // Shows nothing!
  
  // Index settings missing faceting config
  await index.setSettings({
    searchableAttributes: ['name', 'category'],
    // Missing: attributesForFaceting
  });
  
### **Right Way**
  // Configure faceting in index settings
  await index.setSettings({
    attributesForFaceting: [
      'category',                    // Regular facet
      'brand',                       // Regular facet
      'searchable(tags)',            // Searchable in facet dropdown
      'filterOnly(inStock)',         // For filtering only (no facet count)
    ],
  });
  
  // Now facet widgets work
  <RefinementList attribute="category" />  // Shows values!
  <RefinementList
    attribute="tags"
    searchable  // Works because of searchable()
    searchablePlaceholder="Search tags"
  />
  
### **Detection Patterns**
  - RefinementList.*attribute.*(?!attributesForFaceting)
  - Menu.*attribute.*(?!attributesForFaceting)
### **References**
  - https://www.algolia.com/doc/guides/managing-results/refine-results/faceting/