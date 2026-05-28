# Graph Engineer - Sharp Edges

## God Node Performance

### **Id**
god-node-performance
### **Summary**
Single node with 100K+ edges brings queries to halt
### **Severity**
critical
### **Situation**
  Your graph has a popular node - maybe a common entity like "United States"
  or a power user. Every query that touches it scans all edges. Response
  times go from milliseconds to minutes.
  
### **Why**
  Graph databases optimize for traversal, not filtering. When you match
  on a god node, every edge must be examined. With 100K edges, that's
  100K operations per query. Compound with joins and it's game over.
  
### **Solution**
  # Strategy 1: Partition by time window
  # Instead of: (user)-[:VISITED]->(location)
  # Use: (user)-[:VISITED_2024_Q1]->(location)
  
  # Strategy 2: Aggregate counts
  # Instead of: 1M edges from Entity->Mention
  # Use: (entity)-[:MENTIONED_IN {count: 1000000}]->(source_type)
  
  # Strategy 3: Hierarchical bucketing
  CREATE (e:Entity {name: "USA"})
  CREATE (e)-[:HAS_BUCKET]->(b:EntityBucket {range: "A-M"})
  CREATE (b)-[:CONTAINS]->(ref:Reference)
  
  # Strategy 4: Detect and alert
  async def check_cardinality(node_id):
      count = await graph.query(
          "MATCH (n)-[r]-() WHERE n.id = $id RETURN count(r)",
          {"id": node_id}
      )
      if count > 10000:
          alert(f"Node {node_id} approaching god node status: {count} edges")
  
### **Symptoms**
  - Queries timeout on specific nodes
  - One query works fast, adding join makes it hang
  - Performance degrades as data grows
  - Memory usage spikes on certain queries
### **Detection Pattern**
MATCH.*\\(\\w+\\)-\\[.*\\]-.*WHERE.*\\.id\\s*=
### **Version Range**
>=1.0.0

## Falkordb Redis Memory

### **Id**
falkordb-redis-memory
### **Summary**
FalkorDB inherits Redis memory limits
### **Severity**
critical
### **Situation**
  You're using FalkorDB (Redis-based graph database). Everything works in
  development. In production, with real data, writes start failing silently
  or the server OOMs.
  
### **Why**
  FalkorDB runs as a Redis module. Redis keeps data in memory by default.
  Your graph is limited by available RAM. Unlike disk-based databases,
  you can't just "add more storage."
  
### **Solution**
  # 1. Calculate memory requirements BEFORE choosing FalkorDB
  # Rule of thumb: 1M nodes + 10M edges ≈ 4-8 GB RAM
  
  # 2. Set Redis memory limits explicitly
  # redis.conf:
  maxmemory 16gb
  maxmemory-policy noeviction  # Don't silently drop data!
  
  # 3. Monitor memory usage
  async def check_graph_memory():
      info = await redis.info("memory")
      used = info["used_memory"]
      max_mem = info["maxmemory"]
      if used / max_mem > 0.8:
          alert("Graph memory at 80% capacity")
  
  # 4. Consider alternatives for large graphs
  # - Neo4j: Disk-based, larger datasets
  # - AWS Neptune: Managed, auto-scaling
  # - Keep FalkorDB for hot data, archive cold to disk
  
### **Symptoms**
  - Write operations fail silently
  - Redis OOM killer terminates process
  - Graph operations slow as memory fills
  - Data loss after restart (if RDB disabled)
### **Detection Pattern**
FalkorDB|falkordb|redis.*graph
### **Version Range**
>=1.0.0

## Cypher Cartesian Product

### **Id**
cypher-cartesian-product
### **Summary**
Multiple MATCH clauses create Cartesian products
### **Severity**
high
### **Situation**
  You write a query with multiple MATCH clauses to find connected patterns.
  Query works on small data, hangs forever on production data.
  
### **Why**
  Separate MATCH clauses without shared variables create Cartesian products.
  If first MATCH returns 1000 rows and second returns 1000 rows, you get
  1,000,000 combinations. This grows exponentially with more MATCH clauses.
  
### **Solution**
  // WRONG: Cartesian product (1000 x 1000 = 1M rows)
  MATCH (u:User)
  MATCH (m:Memory)
  WHERE u.id = m.user_id
  RETURN u, m
  
  // RIGHT: Connected pattern (1000 rows)
  MATCH (u:User)-[:HAS_MEMORY]->(m:Memory)
  RETURN u, m
  
  // RIGHT: If you must use separate MATCH, use WITH
  MATCH (u:User {id: $user_id})
  WITH u
  MATCH (u)-[:HAS_MEMORY]->(m:Memory)
  RETURN u, m
  
  // Use PROFILE to detect Cartesian products
  PROFILE MATCH (a:A) MATCH (b:B) RETURN a, b
  // Look for "CartesianProduct" in plan
  
### **Symptoms**
  - Query works on dev, hangs on prod
  - Memory explodes during query
  - PROFILE shows CartesianProduct operator
  - Query time grows quadratically with data
### **Detection Pattern**
MATCH.*\\n.*MATCH(?!.*WITH)
### **Version Range**
>=1.0.0

## Missing Temporal Validity

### **Id**
missing-temporal-validity
### **Summary**
Adding time validity to edges after data exists is painful
### **Severity**
high
### **Situation**
  You build your graph with simple edges: (user)-[:KNOWS]->(entity).
  Later, you need to track when relationships started/ended. Migrating
  existing data is a nightmare.
  
### **Why**
  Without temporal validity from the start, you can't answer "what did
  the user believe 6 months ago?" Retroactive addition requires scanning
  and updating every edge, often with guessed timestamps.
  
### **Solution**
  // ALWAYS include temporal validity from day one
  CREATE (u:User)-[r:BELIEVES {
      valid_from: datetime(),
      valid_until: null,  // null = still valid
      created_at: datetime()
  }]->(e:Entity)
  
  // Expire relationship (never delete!)
  MATCH (u:User)-[r:BELIEVES]->(e:Entity)
  WHERE r.id = $edge_id
  SET r.valid_until = datetime()
  
  // Query historical state
  MATCH (u:User {id: $user_id})-[r:BELIEVES]->(e:Entity)
  WHERE r.valid_from <= $point_in_time
    AND (r.valid_until IS NULL OR r.valid_until > $point_in_time)
  RETURN e
  
  // If you must migrate:
  MATCH (u)-[r:KNOWS]->(e)
  WHERE r.valid_from IS NULL
  SET r.valid_from = r.created_at ?? datetime("2020-01-01"),
      r.valid_until = null
  
### **Symptoms**
  - Can't answer 'what did they know on date X'
  - History lost when relationships updated
  - Audit requirements can't be met
  - Migration estimated in weeks
### **Detection Pattern**
CREATE.*\\[r:.*\\{(?!.*valid_from)
### **Version Range**
>=1.0.0

## Entity Resolution Skipped

### **Id**
entity-resolution-skipped
### **Summary**
Graph becomes noise without entity resolution
### **Severity**
high
### **Situation**
  You extract entities from text and create nodes directly. "John Smith",
  "J. Smith", "John S.", and "Smith, John" become four separate nodes.
  Your graph becomes useless.
  
### **Why**
  Entity resolution is 80% of knowledge graph work. Without it, you have
  disconnected fragments instead of a connected graph. Queries return
  partial results. Relationship counts are wrong.
  
### **Solution**
  # Entity resolution pipeline
  async def resolve_entity(raw_name: str, entity_type: str) -> UUID:
      # 1. Normalize
      normalized = normalize_name(raw_name)
  
      # 2. Generate candidates
      candidates = await fuzzy_search(normalized, entity_type)
  
      # 3. Score candidates
      scored = [(c, similarity_score(normalized, c.name)) for c in candidates]
  
      # 4. Apply threshold
      matches = [(c, s) for c, s in scored if s > 0.85]
  
      if matches:
          # 5. Return best match
          return max(matches, key=lambda x: x[1])[0].id
      else:
          # 6. Create new entity
          return await create_entity(normalized, entity_type)
  
  # Use canonical IDs in graph
  async def link_mention(mention: str, user_id: UUID):
      entity_id = await resolve_entity(mention, "person")
      await graph.query(
          "MATCH (u:User {id: $uid}), (e:Entity {id: $eid}) "
          "MERGE (u)-[:MENTIONS]->(e)",
          {"uid": user_id, "eid": entity_id}
      )
  
### **Symptoms**
  - Same real-world entity has multiple nodes
  - Relationship counts are lower than expected
  - Can't find connections that should exist
  - Fuzzy search returns same entity multiple times
### **Detection Pattern**
MERGE.*\\(.*\\{name:.*\\$
### **Version Range**
>=1.0.0

## Optional Match Performance

### **Id**
optional-match-performance
### **Summary**
OPTIONAL MATCH is surprisingly expensive
### **Severity**
medium
### **Situation**
  You use OPTIONAL MATCH to include related data that might not exist.
  Query is much slower than expected.
  
### **Why**
  OPTIONAL MATCH must attempt the match for every input row, even when
  there's no result. It can't short-circuit. Combined with large result
  sets, this creates significant overhead.
  
### **Solution**
  // SLOW: OPTIONAL MATCH on every row
  MATCH (u:User {id: $user_id})-[:HAS_MEMORY]->(m:Memory)
  OPTIONAL MATCH (m)-[:RELATES_TO]->(e:Entity)
  RETURN m, collect(e)
  
  // FASTER: Split into two queries when optional data rarely exists
  // Query 1: Get memories
  MATCH (u:User {id: $user_id})-[:HAS_MEMORY]->(m:Memory)
  RETURN m
  
  // Query 2: Get related entities for memories that have them
  MATCH (m:Memory)-[:RELATES_TO]->(e:Entity)
  WHERE m.id IN $memory_ids AND m.has_entities = true
  RETURN m.id, collect(e)
  
  // OR: Use exists() to filter before OPTIONAL MATCH
  MATCH (u:User {id: $user_id})-[:HAS_MEMORY]->(m:Memory)
  WHERE exists((m)-[:RELATES_TO]->(:Entity))
  MATCH (m)-[:RELATES_TO]->(e:Entity)
  RETURN m, collect(e)
  
### **Symptoms**
  - Query slower than similar non-optional version
  - PROFILE shows high row counts in optional match
  - Performance degrades with data size
### **Detection Pattern**
OPTIONAL MATCH(?!.*exists)
### **Version Range**
>=1.0.0

## Cycle In Causal Graph

### **Id**
cycle-in-causal-graph
### **Summary**
Cycles in causal graphs break inference
### **Severity**
high
### **Situation**
  Your causal graph has A->B->C->A. Inference algorithms go infinite.
  Counterfactual queries return nonsense.
  
### **Why**
  Causal graphs must be DAGs (Directed Acyclic Graphs). Cycles imply
  time travel (A causes B which causes A). Inference algorithms assume
  acyclicity for correctness.
  
### **Solution**
  # Validate DAG property on edge creation
  async def create_causal_edge(source_id: str, target_id: str):
      # Check if adding this edge creates a cycle
      result = await graph.query(
          """
          MATCH path = (t:Entity {id: $target})-[:CAUSES*]->(s:Entity {id: $source})
          RETURN count(path) > 0 AS creates_cycle
          """,
          {"source": source_id, "target": target_id}
      )
  
      if result[0]["creates_cycle"]:
          raise CycleError(f"Edge {source_id}->{target_id} would create cycle")
  
      await graph.query(
          "MATCH (s:Entity {id: $source}), (t:Entity {id: $target}) "
          "CREATE (s)-[:CAUSES {created_at: datetime()}]->(t)",
          {"source": source_id, "target": target_id}
      )
  
  # Periodic validation
  async def check_for_cycles():
      result = await graph.query(
          """
          MATCH path = (n)-[:CAUSES*]->(n)
          RETURN n.id AS node_in_cycle
          LIMIT 1
          """
      )
      if result:
          alert(f"Cycle detected involving node: {result[0]['node_in_cycle']}")
  
### **Symptoms**
  - Infinite loops in graph algorithms
  - Counterfactual queries never return
  - Causal inference gives contradictory results
  - Path queries return unexpectedly long paths
### **Detection Pattern**

### **Version Range**
>=1.0.0

## No Query Parameterization

### **Id**
no-query-parameterization
### **Summary**
Query plan cache misses from string concatenation
### **Severity**
medium
### **Situation**
  You build Cypher queries with string formatting. Every unique value
  generates a new query plan. Query performance is inconsistent.
  
### **Why**
  Databases cache query plans for parameterized queries. String
  concatenation creates unique query text each time, forcing recompilation.
  This adds latency and wastes memory.
  
### **Solution**
  // WRONG: String formatting
  query = f"MATCH (u:User {{id: '{user_id}'}}) RETURN u"
  await graph.query(query)
  
  // RIGHT: Parameterized query
  query = "MATCH (u:User {id: $user_id}) RETURN u"
  await graph.query(query, {"user_id": user_id})
  
  // WRONG: IN with formatted list
  ids_str = ",".join([f"'{id}'" for id in ids])
  query = f"MATCH (u:User) WHERE u.id IN [{ids_str}] RETURN u"
  
  // RIGHT: IN with parameter
  query = "MATCH (u:User) WHERE u.id IN $ids RETURN u"
  await graph.query(query, {"ids": ids})
  
### **Symptoms**
  - First query is slow, not repeated
  - Memory usage grows over time
  - Same query has variable performance
  - Query plan cache hit rate is low
### **Detection Pattern**
query.*f".*\\{.*\\}"
### **Version Range**
>=1.0.0

## Storing Embeddings In Graph

### **Id**
storing-embeddings-in-graph
### **Summary**
Large vectors in graph properties kill performance
### **Severity**
medium
### **Situation**
  You store 1536-dimensional embedding vectors as node properties.
  Graph queries become slow. Storage balloons.
  
### **Why**
  Graph databases optimize for relationship traversal, not vector math.
  Large properties slow down node loading and increase memory usage.
  Vector search requires specialized indexes (HNSW, IVF) not graph indexes.
  
### **Solution**
  // WRONG: Embedding in graph property
  CREATE (m:Memory {
      id: $id,
      content: $content,
      embedding: $embedding  // 1536 floats = 12KB per node!
  })
  
  // RIGHT: Store embedding reference, vector in vector DB
  CREATE (m:Memory {
      id: $id,
      content: $content,
      embedding_id: $embedding_id  // Just the reference
  })
  
  // Query pattern: Vector search first, then graph enrichment
  # Step 1: Vector search in Qdrant/pgvector
  similar_ids = await vector_db.search(query_embedding, limit=20)
  
  # Step 2: Graph enrichment
  results = await graph.query(
      """
      MATCH (m:Memory)-[:RELATES_TO]->(e:Entity)
      WHERE m.id IN $ids
      RETURN m, collect(e) AS entities
      """,
      {"ids": similar_ids}
  )
  
### **Symptoms**
  - Graph memory usage 10x expected
  - Node loading is slow
  - Vector similarity queries not possible
  - Each node is several KB
### **Detection Pattern**
embedding.*List\\[float\\]|embedding.*\\$
### **Version Range**
>=1.0.0