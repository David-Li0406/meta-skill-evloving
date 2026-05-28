# Performance Hunter

## Patterns


---
  #### **Name**
Profiled Optimization
  #### **Description**
Profile before optimizing, measure after
  #### **When**
Any performance improvement task
  #### **Example**
    import cProfile
    import pstats
    import io
    from functools import wraps
    import time
    from contextlib import contextmanager
    
    class Profiler:
        """Profile code execution with actionable output."""
    
        @contextmanager
        def profile(self, label: str):
            """Context manager for profiling a block."""
            profiler = cProfile.Profile()
            profiler.enable()
            start = time.perf_counter()
    
            yield
    
            elapsed = time.perf_counter() - start
            profiler.disable()
    
            # Format results
            s = io.StringIO()
            ps = pstats.Stats(profiler, stream=s)
            ps.sort_stats('cumulative')
            ps.print_stats(20)  # Top 20 functions
    
            logger.info(f"Profile [{label}]: {elapsed:.3f}s")
            logger.debug(s.getvalue())
    
        def profile_async(self, label: str):
            """Decorator for profiling async functions."""
            def decorator(func):
                @wraps(func)
                async def wrapper(*args, **kwargs):
                    start = time.perf_counter()
                    result = await func(*args, **kwargs)
                    elapsed = time.perf_counter() - start
    
                    if elapsed > 0.1:  # Log slow calls
                        logger.warning(
                            f"Slow call [{label}]: {elapsed:.3f}s"
                        )
    
                    LATENCY_HISTOGRAM.labels(operation=label).observe(elapsed)
                    return result
                return wrapper
            return decorator
    
    # Usage
    profiler = Profiler()
    
    async def optimize_retrieval():
        # Profile current performance
        with profiler.profile("retrieval_baseline"):
            results = await retrieve_memories(query)
    
        # After optimization
        with profiler.profile("retrieval_optimized"):
            results = await retrieve_memories_optimized(query)
    

---
  #### **Name**
Multi-Level Caching
  #### **Description**
Cache at multiple layers with appropriate TTLs
  #### **When**
Repeated expensive computations or queries
  #### **Example**
    from aiocache import Cache, cached
    from aiocache.serializers import PickleSerializer
    import hashlib
    from functools import wraps
    
    class MultiLevelCache:
        """L1 (memory) + L2 (Redis) caching with proper invalidation."""
    
        def __init__(self, redis_client):
            # L1: Process memory (fast, small)
            self.l1 = Cache(Cache.MEMORY, ttl=60, namespace="l1")
    
            # L2: Redis (slower, larger, shared)
            self.l2 = Cache(
                Cache.REDIS,
                endpoint=redis_client,
                ttl=3600,
                namespace="l2",
                serializer=PickleSerializer(),
            )
    
        async def get(self, key: str):
            # Try L1 first
            value = await self.l1.get(key)
            if value is not None:
                return value
    
            # Try L2
            value = await self.l2.get(key)
            if value is not None:
                # Populate L1
                await self.l1.set(key, value)
                return value
    
            return None
    
        async def set(
            self,
            key: str,
            value,
            l1_ttl: int = 60,
            l2_ttl: int = 3600,
        ):
            await self.l1.set(key, value, ttl=l1_ttl)
            await self.l2.set(key, value, ttl=l2_ttl)
    
        async def invalidate(self, key: str):
            await self.l1.delete(key)
            await self.l2.delete(key)
    
        async def invalidate_pattern(self, pattern: str):
            """Invalidate all keys matching pattern."""
            # L1 doesn't support patterns - clear all
            await self.l1.clear()
            # L2 (Redis) supports patterns
            await self.l2.delete_pattern(pattern)
    
    def cached_with_key(key_fn, ttl: int = 3600):
        """Cache decorator with custom key function."""
        def decorator(func):
            @wraps(func)
            async def wrapper(self, *args, **kwargs):
                cache_key = key_fn(*args, **kwargs)
    
                cached_value = await self.cache.get(cache_key)
                if cached_value is not None:
                    CACHE_HITS.labels(cache="retrieval").inc()
                    return cached_value
    
                CACHE_MISSES.labels(cache="retrieval").inc()
                result = await func(self, *args, **kwargs)
                await self.cache.set(cache_key, result, l2_ttl=ttl)
                return result
            return wrapper
        return decorator
    

---
  #### **Name**
Batched Database Operations
  #### **Description**
Batch queries to avoid N+1 patterns
  #### **When**
Multiple related database queries in a loop
  #### **Example**
    from typing import List, Dict
    from uuid import UUID
    import asyncpg
    
    class BatchedMemoryLoader:
        """Load memories in batches to avoid N+1."""
    
        def __init__(self, pool: asyncpg.Pool):
            self.pool = pool
            self.batch_size = 100
    
        async def load_many(
            self,
            memory_ids: List[UUID],
        ) -> Dict[UUID, Memory]:
            """Load many memories in batched queries."""
            if not memory_ids:
                return {}
    
            results = {}
    
            # Batch into chunks
            for i in range(0, len(memory_ids), self.batch_size):
                batch = memory_ids[i:i + self.batch_size]
    
                async with self.pool.acquire() as conn:
                    rows = await conn.fetch(
                        """
                        SELECT * FROM memories
                        WHERE memory_id = ANY($1)
                        """,
                        batch
                    )
    
                for row in rows:
                    results[row['memory_id']] = Memory.from_row(row)
    
            return results
    
        async def load_with_relations(
            self,
            memory_ids: List[UUID],
        ) -> List[MemoryWithRelations]:
            """Load memories with related data in parallel queries."""
    
            async with self.pool.acquire() as conn:
                # Single query for memories
                memories_query = conn.fetch(
                    "SELECT * FROM memories WHERE memory_id = ANY($1)",
                    memory_ids
                )
    
                # Single query for entities
                entities_query = conn.fetch(
                    """
                    SELECT * FROM memory_entities
                    WHERE memory_id = ANY($1)
                    """,
                    memory_ids
                )
    
                # Single query for relations
                relations_query = conn.fetch(
                    """
                    SELECT * FROM memory_relations
                    WHERE source_id = ANY($1) OR target_id = ANY($1)
                    """,
                    memory_ids
                )
    
                # Execute in parallel
                memories, entities, relations = await asyncio.gather(
                    memories_query,
                    entities_query,
                    relations_query,
                )
    
            # Assemble results
            return self._assemble(memories, entities, relations)
    

---
  #### **Name**
Connection Pooling
  #### **Description**
Proper connection pooling for database and external services
  #### **When**
Any database or service client
  #### **Example**
    import asyncpg
    from redis.asyncio import ConnectionPool, Redis
    from contextlib import asynccontextmanager
    
    class ConnectionManager:
        """Manage connection pools for all external services."""
    
        def __init__(self, config: Config):
            self.config = config
            self._pg_pool = None
            self._redis_pool = None
            self._http_session = None
    
        async def initialize(self):
            """Initialize all connection pools."""
    
            # PostgreSQL pool
            self._pg_pool = await asyncpg.create_pool(
                dsn=self.config.database_url,
                min_size=5,      # Minimum connections
                max_size=20,     # Maximum connections
                max_inactive_connection_lifetime=300,  # 5 min idle timeout
                command_timeout=30,  # Query timeout
            )
    
            # Redis pool
            self._redis_pool = ConnectionPool.from_url(
                self.config.redis_url,
                max_connections=20,
                socket_timeout=5,
                socket_connect_timeout=5,
            )
            self._redis = Redis(connection_pool=self._redis_pool)
    
            # HTTP session with connection pooling
            connector = aiohttp.TCPConnector(
                limit=100,  # Total connections
                limit_per_host=20,  # Per-host limit
                ttl_dns_cache=300,  # DNS cache
            )
            self._http_session = aiohttp.ClientSession(connector=connector)
    
        async def close(self):
            """Close all connection pools."""
            if self._pg_pool:
                await self._pg_pool.close()
            if self._redis_pool:
                await self._redis_pool.disconnect()
            if self._http_session:
                await self._http_session.close()
    
        @asynccontextmanager
        async def db(self):
            """Get database connection from pool."""
            async with self._pg_pool.acquire() as conn:
                yield conn
    
        @property
        def redis(self) -> Redis:
            return self._redis
    
        @property
        def http(self) -> aiohttp.ClientSession:
            return self._http_session
    

## Anti-Patterns


---
  #### **Name**
Sync I/O in Async Code
  #### **Description**
Blocking calls that freeze the event loop
  #### **Why**
Single blocking call stalls all concurrent operations. Defeats async purpose.
  #### **Instead**
Use async versions of all I/O operations

---
  #### **Name**
N+1 Queries
  #### **Description**
Querying in a loop instead of batching
  #### **Why**
N+1 creates N database round trips. Latency adds up linearly.
  #### **Instead**
Batch queries with WHERE IN or bulk fetch

---
  #### **Name**
No Connection Pooling
  #### **Description**
Creating new connections for each request
  #### **Why**
Connection establishment is expensive. Pool amortizes this cost.
  #### **Instead**
Use connection pools for database, Redis, HTTP clients

---
  #### **Name**
Cache Without Metrics
  #### **Description**
Caching without measuring hit rate
  #### **Why**
Cache might be worthless (low hit rate) or thrashing. You won't know.
  #### **Instead**
Track hit rate, miss rate, eviction rate

---
  #### **Name**
Optimizing Without Profiling
  #### **Description**
"I think this is slow" without measurement
  #### **Why**
Intuition is wrong. You will optimize the wrong thing.
  #### **Instead**
Profile first, identify actual bottleneck, then optimize