# Backend Review Standards (Late 2025)
## 1. Cloud Architecture: Edge-Native & Serverless
In 2025, backends are "Distributed by Default." Review code for readiness in ephemeral, multi-region environments.
### The "Cold Start" Audit
- [ ] **Runtime Choice:** Is the runtime optimized for the environment? (e.g., Bun or lightweight Node for Edge; Rust/Go for heavy compute).
- [ ] **SnapStart / Snapshotting:** For AWS Lambda (Java/.NET), is SnapStart enabled? For others, is initialization logic minimized to avoid the "Cold Start Tax"?
- [ ] **V8 Isolates Compatibility:** If deploying to Edge (Cloudflare/Vercel), does the code avoid Node-specific APIs (like `fs` or `net`) that aren't supported?
### API & Data Flow
- [ ] **tRPC v11/v12 Patterns:** Are procedures using `experimental_trpc_core` (or current stable) for shared logic across multiple routers?
- [ ] **Response Streaming:** Does the API utilize HTTP Streaming for long-running AI completions or heavy data exports?
- [ ] **Idempotency Keys:** For mutations (Server Actions/POST), are idempotency keys implemented to handle client retries safely?
## 2. The 2025 Data Layer
PostgreSQL has become the "OS of the Database," while Drizzle has eclipsed Prisma in the Serverless sector.
### ORM & Query Review
- [ ] **Drizzle vs. Prisma:** Is the ORM choice justified? 
    - *Reviewer Note:* Prefer **Drizzle** for Edge/Serverless (<100ms cold starts). Use **Prisma v6+** only if its new Wasm engine is leveraged.
- [ ] **Connection Pooling:** Is a proxy used? (e.g., Prisma Accelerate, Neon Connection Pooler, or RDS Proxy). *Direct connections in Serverless are a 🔴 Critical risk.*
- [ ] **Schema-as-Code:** Are migrations versioned and applied in CI, never manually from a developer's machine?
### AI & Vector Strategy
- [ ] **pgvector Utilization:** For RAG/Search logic, are vectors stored in Postgres? (Avoid specialized Vector DBs unless dataset > 100M).
- [ ] **Indexing (HNSW):** Does the vector column have an `hnsw` index? (Review for appropriate `m` and `ef_construction` parameters).
- [ ] **Embedding Locality:** Are embeddings generated as close to the database as possible to reduce egress/ingress latency?
## 3. Distributed Systems Security
- [ ] **Zero Trust Internal:** Do internal service-to-service calls use mTLS or signed headers (e.g., AWS SigV4) rather than "Trusting the VPC"?
- [ ] **Statelessness:** Verify no `Map` or `let` variables are used for cross-request state. All state must be in Redis (e.g., Upstash) or the DB.
- [ ] **Circuit Breakers:** Are external API calls (OpenAI, Stripe) wrapped in timeouts and circuit breakers to prevent cascading failures?
## 4. Performance Benchmarks
| Component | 2025 Standard | Check |
| :--- | :--- | :--- |
| **API Latency** | **P95 < 150ms** | Check for N+1 queries and heavy middleware. |
| **Cold Start** | **< 200ms** | Check dependency bloat and init logic. |
| **DB Query** | **< 20ms** | Verify index usage on all `WHERE` clauses. |
| **Edge Cache** | **> 80% Hit Rate** | Ensure `Cache-Control` is set for public GETs. |
