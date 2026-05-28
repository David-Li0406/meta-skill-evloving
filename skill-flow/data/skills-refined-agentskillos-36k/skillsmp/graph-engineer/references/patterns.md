# Graph Engineer

## Patterns


---
  #### **Name**
Bounded Edge Cardinality
  #### **Description**
Design schema with explicit cardinality limits per node type
  #### **When**
Designing any graph schema
  #### **Example**
    # Define cardinality budgets in schema documentation
    """
    Node Type       | Max Inbound | Max Outbound | Strategy
    ----------------|-------------|--------------|----------
    User            | 1000        | 10000        | Aggregate after 1000
    Memory          | 100         | 50           | Prune weak edges
    Entity          | 500         | 500          | Partition by time window
    Concept         | 10000       | 10000        | Use hierarchical concepts
    """
    
    # Enforce in application code
    async def add_edge(source_id, target_id, edge_type):
        count = await graph.query(
            "MATCH (n)-[r:$type]->() WHERE n.id = $id RETURN count(r)",
            {"id": source_id, "type": edge_type}
        )
        if count >= CARDINALITY_LIMITS[edge_type]:
            await consolidate_edges(source_id, edge_type)
    

---
  #### **Name**
Temporal Edge Validity
  #### **Description**
All edges have valid_from/valid_until for time-aware queries
  #### **When**
Any relationship that can change over time
  #### **Example**
    // Create edge with temporal validity
    CREATE (u:User {id: $user_id})-[r:BELIEVES {
        valid_from: datetime(),
        valid_until: null,
        confidence: 0.8,
        evidence_count: 1
    }]->(e:Entity {id: $entity_id})
    
    // Query only active relationships
    MATCH (u:User {id: $user_id})-[r:BELIEVES]->(e:Entity)
    WHERE r.valid_until IS NULL
      AND r.confidence > 0.5
    RETURN e
    
    // Expire old belief (don't delete!)
    MATCH (u:User)-[r:BELIEVES]->(e:Entity)
    WHERE r.id = $edge_id
    SET r.valid_until = datetime()
    

---
  #### **Name**
Causal Edge Schema
  #### **Description**
Model cause-effect relationships with full metadata
  #### **When**
Building causal graphs for prediction or explanation
  #### **Example**
    @dataclass
    class CausalEdge:
        source_id: UUID
        target_id: UUID
        relationship: str  # "causes", "correlates", "prevents"
    
        # Causal metadata
        causal_direction: Literal["causes", "correlates", "prevents"]
        causal_strength: float  # 0-1
    
        # Temporal
        valid_from: datetime
        valid_until: Optional[datetime]
        temporal_conditions: List[str]  # ["morning", "weekday"]
    
        # Evidence
        evidence_count: int
        confidence: float
        discovery_method: str  # "statistical", "expert", "observed"
    
    # Cypher creation
    CREATE (c:Cause {id: $source_id})-[r:CAUSES {
        strength: $strength,
        confidence: $confidence,
        evidence_count: $evidence_count,
        valid_from: datetime(),
        temporal_conditions: $conditions
    }]->(e:Effect {id: $target_id})
    

---
  #### **Name**
Index-First Query Design
  #### **Description**
Design queries around available indexes, not business logic
  #### **When**
Writing any Cypher query
  #### **Example**
    // WRONG: Full scan then filter
    MATCH (n) WHERE n.user_id = $user_id RETURN n
    
    // RIGHT: Index lookup
    MATCH (n:Memory {user_id: $user_id}) RETURN n
    
    // Create indexes for common access patterns
    CREATE INDEX memory_user_idx FOR (m:Memory) ON (m.user_id)
    CREATE INDEX memory_level_idx FOR (m:Memory) ON (m.temporal_level)
    CREATE INDEX entity_name_idx FOR (e:Entity) ON (e.name)
    
    // Composite index for frequent filters
    CREATE INDEX memory_user_level_idx FOR (m:Memory)
    ON (m.user_id, m.temporal_level)
    

## Anti-Patterns


---
  #### **Name**
God Nodes
  #### **Description**
Nodes with hundreds of thousands of edges
  #### **Why**
Every query touching that node scans all edges. Performance collapses.
  #### **Instead**
Partition by time, aggregate counts, use hierarchical structure

---
  #### **Name**
Unbounded Traversal
  #### **Description**
MATCH paths without depth limits
  #### **Why**
Graph traversal is exponential. Unbounded queries never return.
  #### **Instead**
Always use *1..3 or similar depth limits in path patterns

---
  #### **Name**
Property Blobs
  #### **Description**
Storing large JSON blobs in node properties
  #### **Why**
Graphs are for relationships. Large properties slow everything down.
  #### **Instead**
Store reference to blob storage, keep properties small

---
  #### **Name**
Cycles in Causal Graphs
  #### **Description**
Allowing A causes B causes A
  #### **Why**
Causal graphs are DAGs. Cycles break inference and create infinite loops.
  #### **Instead**
Validate DAG property on edge insertion

---
  #### **Name**
No Entity Resolution
  #### **Description**
Creating nodes without deduplication
  #### **Why**
"John Smith" and "J. Smith" become separate nodes. Graph becomes noise.
  #### **Instead**
Implement entity resolution before graph insertion