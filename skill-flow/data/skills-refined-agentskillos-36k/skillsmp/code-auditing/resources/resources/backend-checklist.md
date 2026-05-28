# Backend Performance Checklist

## 🗄️ Database (PostgreSQL/Prisma)
- [ ] **Indexing**: Are foreign keys and frequently searched columns indexed?
- [ ] **N+1 Problem**: Are you fetching related data in a loop? Use `include` (Prisma) or `Dataloader`.
- [ ] **Select Fields**: Are you selecting `*` (or default all fields) when you only need `id` and `name`?
- [ ] **Connection Pooling**: Are you exhausting DB connections? Use a pooler (e.g., PgBouncer/Supabase Transaction Mode).

## ⚡ API & HTTP
- [ ] **Compression**: Is Gzip/Brotli enabled? (Express: `app.use(compression())`)
- [ ] **Caching**:
  - **Browser**: Are you setting `Cache-Control` headers for static/public data?
  - **Server**: Are you using Redis/Memory to cache expensive query results?
- [ ] **Validation**: Are you validating input *before* processing logic? (Fail fast).

## 🟢 Node.js Runtime
- [ ] **Event Loop**: Are you blocking the event loop with synchronous crypto or fs calls?
- [ ] **Async/Await**: Are you using `Promise.all` for parallel tasks instead of serial `await`?
- [ ] **Logging**: ensuring logging levels (Info/Debug) don't flood stdout in production.
