# System Design Interview Preparation Guide

## Overview

System design interviews assess your ability to design large-scale distributed systems. Common for Senior+ engineering roles (L5+).

**Typical Duration**: 45-60 minutes
**Format**: Whiteboard/virtual board collaborative design
**Evaluation Criteria**: Scalability, reliability, trade-off analysis, communication

---

## Interview Framework (RESHADED)

Use this mnemonic to structure your approach:

### 1. **R**equirements (5-10 min)

#### Functional Requirements
Ask clarifying questions to define scope:
- "What are the core features we need to support?"
- "Are there any features explicitly out of scope?"
- "What are the critical user flows?"

**Example (Design Twitter)**:
- ✅ In scope: Post tweets, follow users, view timeline
- ❌ Out of scope: Direct messages, trending topics, ads

#### Non-Functional Requirements
Quantify system constraints:
- **Scale**: DAU (Daily Active Users), QPS (Queries Per Second), data volume
- **Performance**: Latency targets (p50, p95, p99)
- **Availability**: Uptime SLA (99.9% = 43 min downtime/month)
- **Consistency**: Strong vs eventual consistency trade-offs

**Questions to Ask**:
- "How many users do we expect?"
- "What's the read-to-write ratio?"
- "Are there regional requirements (GDPR, data residency)?"

### 2. **E**stimation (5 min)

Back-of-the-envelope calculations to size the system.

**Common Metrics**:
| Metric | Calculation | Example (Twitter-like) |
|--------|-------------|------------------------|
| **DAU** | Given or assumed | 200M DAU |
| **QPS** | DAU × actions/day ÷ 86400s | 200M × 5 ÷ 86400 ≈ 11.5K QPS |
| **Peak QPS** | QPS × 3-5 (diurnal pattern) | 11.5K × 3 = 35K QPS |
| **Storage** | Entities × size × retention | 500M tweets/day × 1KB × 5yr ≈ 900TB |
| **Bandwidth** | QPS × avg response size | 35K × 2KB = 70MB/s |

**Pro Tips**:
- Round aggressively (200M ≈ 2×10⁸)
- Show units (11.5K **QPS**, not just 11.5K)
- Justify assumptions ("Assuming 5 tweets per user per day based on industry averages")

### 3. **S**chema Design (5-10 min)

Define core entities and relationships.

**Example: Twitter Schema**

```sql
-- Users table
CREATE TABLE users (
  user_id BIGINT PRIMARY KEY,
  username VARCHAR(50) UNIQUE,
  email VARCHAR(255),
  created_at TIMESTAMP,
  follower_count INT,
  following_count INT
);

-- Tweets table
CREATE TABLE tweets (
  tweet_id BIGINT PRIMARY KEY,
  user_id BIGINT REFERENCES users(user_id),
  content TEXT,
  created_at TIMESTAMP,
  like_count INT,
  retweet_count INT,
  INDEX idx_user_created (user_id, created_at)  -- For user timeline
);

-- Follower graph (adjacency list)
CREATE TABLE followers (
  follower_id BIGINT REFERENCES users(user_id),
  followee_id BIGINT REFERENCES users(user_id),
  created_at TIMESTAMP,
  PRIMARY KEY (follower_id, followee_id),
  INDEX idx_followee (followee_id)  -- For follower list queries
);
```

**Key Decisions**:
- **Normalization**: 3NF for transactional data, denormalize for read-heavy (e.g., store `follower_count` instead of `COUNT(*)`)
- **Indexes**: Add for frequent query patterns (user timeline, search)
- **Partitioning**: Shard by `user_id` for horizontal scaling

### 4. **H**igh-Level Design (10-15 min)

Draw the architecture diagram with major components.

**Template Architecture**:

```
┌─────────┐         ┌──────────────┐         ┌──────────┐
│ Client  │────────▶│ Load Balancer│────────▶│   CDN    │
└─────────┘         └──────────────┘         └──────────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
    ┌──────────┐      ┌──────────┐     ┌──────────┐
    │ Web Svr  │      │ Web Svr  │     │ Web Svr  │
    └──────────┘      └──────────┘     └──────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ▼
                    ┌───────────────┐
                    │  API Gateway  │
                    └───────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
    ┌──────────┐      ┌──────────┐     ┌──────────┐
    │ App Svr  │      │ App Svr  │     │ App Svr  │
    └──────────┘      └──────────┘     └──────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
    ┌──────────┐      ┌──────────┐     ┌──────────┐
    │  Cache   │      │    DB    │     │  Queue   │
    │ (Redis)  │      │(Postgres)│     │ (Kafka)  │
    └──────────┘      └──────────┘     └──────────┘
```

**Components to Include**:
- **Client Layer**: Web/mobile apps
- **Edge Layer**: CDN, WAF, DDoS protection
- **Application Layer**: Stateless API servers
- **Data Layer**: Databases, caches, object storage
- **Async Processing**: Message queues, workers

### 5. **A**PI Design (5 min)

Define RESTful or RPC endpoints for core features.

**Example: Twitter API**

```http
# Post a tweet
POST /v1/tweets
Content-Type: application/json
{
  "content": "Hello world!",
  "media_ids": ["12345"]
}
Response: 201 Created
{
  "tweet_id": "987654321",
  "created_at": "2025-01-20T10:30:00Z"
}

# Get user timeline
GET /v1/users/{user_id}/timeline?limit=20&cursor=xyz
Response: 200 OK
{
  "tweets": [...],
  "next_cursor": "abc123"
}

# Follow a user
POST /v1/users/{user_id}/follow
{
  "target_user_id": "123456"
}
```

**Best Practices**:
- Use nouns for resources (`/tweets` not `/getTweets`)
- Version APIs (`/v1/`, `/v2/`)
- Paginate with cursors for large result sets
- Include rate limiting headers (`X-RateLimit-Remaining`)

### 6. **D**eep Dives (10-15 min)

Pick 1-2 critical components and explain in detail.

#### Example: News Feed Generation

**Problem**: Generate personalized timeline for 200M users in < 200ms

**Approach 1: Pull Model (Fanout on Read)**
```python
def get_timeline(user_id, limit=20):
    # 1. Get list of followees
    followees = db.query("SELECT followee_id FROM followers WHERE follower_id = ?", user_id)

    # 2. Fetch recent tweets from all followees
    tweets = db.query("""
        SELECT * FROM tweets
        WHERE user_id IN (?)
        ORDER BY created_at DESC
        LIMIT ?
    """, followees, limit)

    # 3. Rank and return
    return rank_tweets(tweets)
```

**Pros**: Write-efficient, consistent
**Cons**: Slow for users with many followees (O(N) followees)

**Approach 2: Push Model (Fanout on Write)**
```python
def post_tweet(user_id, content):
    tweet_id = db.insert_tweet(user_id, content)

    # Fanout to all followers' timelines
    followers = db.query("SELECT follower_id FROM followers WHERE followee_id = ?", user_id)
    for follower in followers:
        cache.lpush(f"timeline:{follower}", tweet_id)  # Redis list
```

**Pros**: Read-efficient (O(1) timeline fetch)
**Cons**: Write amplification for celebrities (1M followers = 1M writes)

**Hybrid Approach** (Twitter's actual solution):
- **Push for regular users** (< 100K followers)
- **Pull for celebrities** (> 100K followers)
- **Client merges** both timelines

### 7. **E**xtensions (5 min)

Discuss scalability and advanced features.

**Common Topics**:
- **Caching Strategy**: Cache-aside, write-through, TTL policies
- **Database Sharding**: Consistent hashing, shard key selection
- **Replication**: Leader-follower, multi-leader, leaderless
- **CDN**: Static asset caching, edge compute
- **Monitoring**: Metrics (Prometheus), logs (ELK), traces (Jaeger)
- **Disaster Recovery**: Backups, multi-region failover

**Advanced Features**:
- **Search**: Elasticsearch for full-text search
- **Recommendations**: ML pipeline for content ranking
- **Rate Limiting**: Token bucket algorithm
- **Analytics**: Lambda architecture (batch + stream processing)

---

## Common System Design Questions

### Easy (Junior/Mid-Level)
1. **URL Shortener** (bit.ly)
   - Key: Hash function, base62 encoding, redirect service
2. **Pastebin** (pastebin.com)
   - Key: Content storage, expiration, syntax highlighting
3. **Rate Limiter**
   - Key: Token bucket, sliding window, distributed counters

### Medium (Senior)
4. **Instagram** (photo sharing)
   - Key: CDN for images, news feed, graph database for followers
5. **Uber** (ride-sharing)
   - Key: Geospatial indexing (QuadTree), WebSockets, ETA calculation
6. **WhatsApp** (messaging)
   - Key: WebSocket connections, message queue, read receipts

### Hard (Staff+)
7. **YouTube** (video streaming)
   - Key: Video encoding pipeline, adaptive bitrate, CDN, recommendation engine
8. **Google Drive** (file storage)
   - Key: Block-level deduplication, conflict resolution, delta sync
9. **Ticketmaster** (event booking)
   - Key: Distributed transactions, seat locking, queue fairness

---

## Trade-Off Decision Matrix

Use this framework when comparing solutions:

| Factor | Option A | Option B | Winner |
|--------|----------|----------|--------|
| **Latency** | 50ms (cache) | 200ms (DB) | A |
| **Consistency** | Eventual | Strong | B |
| **Cost** | $10K/mo (Redis) | $2K/mo (DB) | B |
| **Complexity** | High (cache invalidation) | Low | B |

**Communicate thinking**: "I'd choose Option B because strong consistency is critical for financial transactions, and the 200ms latency is acceptable for the use case. We can optimize later with read replicas."

---

## Red Flags to Avoid

❌ **Starting to code immediately** — Always clarify requirements first
❌ **Single point of failure** — Add redundancy (load balancers, DB replicas)
❌ **Ignoring scale** — Design for stated requirements, not your laptop
❌ **Magic scaling** — Explain how components scale (horizontal/vertical)
❌ **No monitoring** — Always include observability layer
❌ **Overengineering** — KISS principle; don't add Kafka for 100 QPS

---

## Resources

### Books
- *Designing Data-Intensive Applications* by Martin Kleppmann
- *System Design Interview* by Alex Xu (Volumes 1 & 2)

### Online Courses
- [Grokking the System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)
- [System Design Primer (GitHub)](https://github.com/donnemartin/system-design-primer)

### Practice Platforms
- [Pramp](https://www.pramp.com/) — Peer mock interviews
- [interviewing.io](https://interviewing.io/) — Anonymous interviews with engineers
- [Exponent](https://www.tryexponent.com/) — Video courses + practice

---

## Cheat Sheet

**Numbers Every Engineer Should Know** (2025 Update):

| Operation | Latency |
|-----------|---------|
| L1 cache reference | 0.5 ns |
| Branch mispredict | 5 ns |
| L2 cache reference | 7 ns |
| Mutex lock/unlock | 25 ns |
| Main memory reference | 100 ns |
| SSD random read | 16 μs |
| Round trip in datacenter | 500 μs |
| Disk seek | 2 ms |
| Packet CA → Netherlands → CA | 150 ms |

**Availability Math**:
- 99% = 3.65 days downtime/year
- 99.9% = 8.76 hours downtime/year
- 99.99% = 52.6 minutes downtime/year
- 99.999% = 5.26 minutes downtime/year

**Storage Units**:
- 1 KB = 10³ bytes (or 2¹⁰ = 1,024 bytes in binary)
- 1 MB = 10⁶ bytes
- 1 GB = 10⁹ bytes
- 1 TB = 10¹² bytes
- 1 PB = 10¹⁵ bytes

---

## Final Tips

1. **Practice whiteboarding** — Draw clearly, use consistent notation
2. **Think aloud** — Interviewers grade your process, not just the solution
3. **Ask for hints** — Shows collaboration, not weakness
4. **Manage time** — Spend 30% on requirements, 50% on design, 20% on deep dives
5. **Stay calm** — No perfect solution exists; demonstrate trade-off analysis

Good luck! 🚀
