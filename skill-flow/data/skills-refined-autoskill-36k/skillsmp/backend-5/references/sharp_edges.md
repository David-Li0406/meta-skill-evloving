# Backend - Sharp Edges

## N1 Query Massacre

### **Id**
n1-query-massacre
### **Summary**
ORM loops fire N+1 queries instead of single batched query
### **Severity**
critical
### **Situation**
Using ORM lazy loading in loops, accessing relations without eager loading
### **Why**
  Works great with 10 users. With 1,000 users, you've fired 1,001 queries.
  Database CPU spikes, response times balloon from milliseconds to seconds.
  ORMs hide the queries. Testing with small datasets masks the problem.
  
### **Solution**
  // WRONG - N+1 (fires query for each user's posts)
  const users = await prisma.user.findMany()
  for (const user of users) {
    const posts = await prisma.post.findMany({ where: { authorId: user.id } })
  }
  
  // RIGHT - Eager loading with include
  const users = await prisma.user.findMany({
    include: { posts: true }
  })
  // 1 query with JOIN, or 2 queries with IN clause
  
### **Symptoms**
  - Response time grows linearly with data size
  - Database CPU high, app CPU low
  - Query logs show repeated similar queries
### **Detection Pattern**
for\\s*\\([^)]*\\)\\s*\\{[^}]*await.*find

## Transaction Timeout Trap

### **Id**
transaction-timeout-trap
### **Summary**
External API calls inside database transactions hold locks
### **Severity**
critical
### **Situation**
Wrapping payment/webhook/external service calls in database transactions
### **Why**
  Transaction holds locks while external API is slow. 30 second API call means
  30 seconds of locked rows. Other requests queue up. Connection pool exhausts.
  Everything freezes.
  
### **Solution**
  // WRONG - External call inside transaction
  await prisma.$transaction(async (tx) => {
    const order = await tx.order.create({ data: orderData })
    const payment = await paymentService.charge(order.total) // Can take 30s!
    await tx.order.update({ where: { id: order.id }, data: { paymentId: payment.id } })
  })
  
  // RIGHT - External calls outside transaction
  const order = await prisma.order.create({ data: { ...orderData, status: 'pending' } })
  const payment = await paymentService.charge(order.total)
  await prisma.order.update({ where: { id: order.id }, data: { paymentId: payment.id, status: 'paid' } })
  
### **Symptoms**
  - Database lock wait timeouts
  - Connection pool exhaustion
  - External service latency correlates with DB issues
### **Detection Pattern**
\\$transaction[^}]*(?:fetch|axios|http|stripe|twilio|sendgrid)

## Missing Idempotency

### **Id**
missing-idempotency
### **Summary**
Duplicate requests cause duplicate operations (double charges, duplicate orders)
### **Severity**
critical
### **Situation**
Mutations without idempotency keys, webhooks without event ID tracking
### **Why**
  User clicks Pay twice. Network retry fires. Webhook retries on timeout.
  Without idempotency, you charge twice, create duplicate orders, send duplicate
  emails. Now you're dealing with refunds and angry customers.
  
### **Solution**
  // WRONG - No idempotency
  app.post('/api/charge', async (req, res) => {
    await paymentService.charge(userId, amount) // Can double-charge
  })
  
  // RIGHT - Idempotency key
  app.post('/api/charge', async (req, res) => {
    const { idempotencyKey } = req.body
    const existing = await db.payment.findUnique({ where: { idempotencyKey } })
    if (existing) return res.json(existing.response) // Return cached
  
    const result = await paymentService.charge(userId, amount)
    await db.payment.create({ data: { idempotencyKey, response: result } })
    res.json(result)
  })
  
### **Symptoms**
  - Customer complaints about double charges
  - Duplicate records in database
  - Same operation appears twice in audit logs
### **Detection Pattern**
charge|createOrder|sendEmail

## Sql Injection

### **Id**
sql-injection
### **Summary**
User input concatenated into queries enables data theft/destruction
### **Severity**
critical
### **Situation**
Building SQL queries with string concatenation, unvalidated query params
### **Why**
  Attacker sends email = "'; DROP TABLE users; --". Your database executes it.
  They download your user table, or delete it entirely. Single quotes in normal
  input also break queries.
  
### **Solution**
  // WRONG - SQL Injection
  const query = `SELECT * FROM users WHERE email = '${email}'`
  
  // RIGHT - Parameterized queries
  const query = 'SELECT * FROM users WHERE email = $1'
  const result = await db.query(query, [email])
  
  // RIGHT - ORM with explicit type coercion
  const user = await prisma.user.findUnique({
    where: { email: String(req.body.email) }
  })
  
  // RIGHT - Input validation with Zod
  const UserInput = z.object({
    email: z.string().email(),
    name: z.string().min(1).max(100)
  })
  
### **Symptoms**
  - String concatenation with user input in queries
  - Errors contain SQL syntax
  - No input validation middleware
### **Detection Pattern**
`SELECT.*\\$\\{|\\+.*req\\.(?:body|query|params)

## Race Condition Balance

### **Id**
race-condition-balance
### **Summary**
Check-then-act patterns allow invalid states under concurrency
### **Severity**
critical
### **Situation**
Reading value, checking condition, then updating (like balance checks)
### **Why**
  User has $100. Two concurrent requests each check, see $100, deduct $80.
  Both succeed. Balance is -$60. You've given away free money. Reproducing
  in tests is hard because timing has to be exact.
  
### **Solution**
  // WRONG - Race condition
  const user = await db.user.findUnique({ where: { id: userId } })
  if (user.balance >= amount) {
    await db.user.update({ where: { id: userId }, data: { balance: user.balance - amount } })
  }
  
  // RIGHT - Atomic update with condition
  const result = await db.user.updateMany({
    where: { id: userId, balance: { gte: amount } },
    data: { balance: { decrement: amount } }
  })
  if (result.count === 0) throw new Error('Insufficient balance')
  
  // RIGHT - Pessimistic locking
  await prisma.$transaction(async (tx) => {
    const user = await tx.$queryRaw`SELECT * FROM users WHERE id = ${userId} FOR UPDATE`
    if (user.balance < amount) throw new Error('Insufficient balance')
    await tx.user.update({ where: { id: userId }, data: { balance: { decrement: amount } } })
  })
  
### **Symptoms**
  - Financial discrepancies in audits
  - "Impossible" states in data
  - Check-then-act patterns in code
### **Detection Pattern**
if\\s*\\([^)]*balance[^)]*\\)[^}]*update

## Unbounded Query

### **Id**
unbounded-query
### **Summary**
Queries without LIMIT can return millions of rows and crash everything
### **Severity**
high
### **Situation**
List endpoints without pagination, admin tools, data export features
### **Why**
  Works in dev with 100 records. Production has 10 million. Query runs for
  60 seconds, uses 8GB RAM, crashes server. Or returns 2GB JSON that crashes client.
  
### **Solution**
  // WRONG - No limits
  const users = await db.user.findMany() // All 10 million
  
  // RIGHT - Always paginate
  const limit = Math.min(parseInt(req.query.limit) || 20, 100) // Max 100
  const skip = (page - 1) * limit
  const users = await db.user.findMany({ skip, take: limit })
  
  // RIGHT - Cursor pagination for large datasets
  const users = await db.user.findMany({
    take: limit + 1,
    cursor: cursor ? { id: cursor } : undefined,
    orderBy: { id: 'asc' }
  })
  
### **Symptoms**
  - Endpoints that can return unlimited data
  - Memory spikes during certain requests
  - Database slow queries on SELECT without LIMIT
### **Detection Pattern**
findMany\\(\\s*\\)|findMany\\(\\s*\\{\\s*where

## Unhandled Async Error

### **Id**
unhandled-async-error
### **Summary**
Fire-and-forget async operations lose errors silently
### **Severity**
high
### **Situation**
Background jobs, setTimeout/setInterval, not awaiting promises
### **Why**
  Background job throws. Nobody catches it. Process continues in corrupted state.
  Data inconsistency discovered days later. UnhandledPromiseRejectionWarning
  in logs that nobody reads.
  
### **Solution**
  // WRONG - Not awaited, errors lost
  app.post('/api/signup', (req, res) => {
    createUser(req.body) // Not awaited
    sendWelcomeEmail(req.body.email) // Not awaited
    res.json({ success: true }) // Returns before work done
  })
  
  // RIGHT - Await and handle errors
  app.post('/api/signup', async (req, res, next) => {
    try {
      const user = await createUser(req.body)
      await queue.add('send-welcome-email', { userId: user.id })
      res.json({ success: true })
    } catch (error) {
      next(error)
    }
  })
  
### **Symptoms**
  - UnhandledPromiseRejectionWarning in logs
  - Missing data that should exist
  - Jobs that "ran" but had no effect
### **Detection Pattern**
(?<!await\\s)createUser|sendEmail|process(?!\\.)\\(

## Secrets In Code

### **Id**
secrets-in-code
### **Summary**
API keys and passwords committed to repository
### **Severity**
critical
### **Situation**
Hardcoded credentials, secrets in config files, missing .gitignore
### **Why**
  Repo becomes public. Or someone clones it. All production credentials exposed.
  AWS keys get crypto-mined. Database gets ransomwared. "Just for development"
  becomes production.
  
### **Solution**
  // WRONG - Hardcoded secrets
  const STRIPE_KEY = 'sk_live_abc123...'
  const DB_URL = 'postgres://admin:password@prod-db.com/main'
  
  // RIGHT - Environment variables
  const STRIPE_KEY = process.env.STRIPE_SECRET_KEY
  if (!STRIPE_KEY) throw new Error('STRIPE_SECRET_KEY required')
  
  // .gitignore
  .env
  .env.local
  .env.*.local
  
  // Use secret managers in production
  // AWS Secrets Manager, GCP Secret Manager, Vault
  
### **Symptoms**
  - Strings that look like keys/passwords in code
  - No .env.example in repo
  - git log shows sensitive values
### **Detection Pattern**
sk_live_|sk_test_|password\s*=\s*['"][^'"]+['"]|api_key\s*=\s*['"]

## Missing Rate Limit

### **Id**
missing-rate-limit
### **Summary**
Endpoints without rate limiting enable brute force and DoS
### **Severity**
high
### **Situation**
Login endpoints, password reset, API without throttling
### **Why**
  Attacker brute-forces at 1000 requests/second. Either they get in, or your
  service falls over. Either way, you lose. Login has no failed attempt
  tracking.
  
### **Solution**
  // WRONG - No rate limiting
  app.post('/api/login', async (req, res) => {
    const user = await authenticate(req.body)
    res.json({ token: createToken(user) })
  })
  
  // RIGHT - Rate limiting
  const authLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 5, // 5 attempts per email
    keyGenerator: (req) => req.body.email || req.ip
  })
  
  app.post('/api/login', authLimiter, loginHandler)
  
### **Symptoms**
  - Auth endpoints without rate limiting
  - No failed attempt tracking
  - High volume of 401 responses from same IP
### **Detection Pattern**
post\(['"].*login|post\(['"].*auth

## Cascading Delete Disaster

### **Id**
cascading-delete-disaster
### **Summary**
CASCADE DELETE on large tables causes long transactions and locks
### **Severity**
high
### **Situation**
User deletes account with CASCADE DELETE on relations
### **Why**
  User deletes account. CASCADE triggers. Posts delete. Comments delete.
  Replies delete. Millions of rows. Transaction takes 10 minutes. Database
  locked. Everything else waits.
  
### **Solution**
  // WRONG - Cascading delete spirals
  model User {
    posts Post[] @relation(onDelete: Cascade)
  }
  // Deleting user with 100k posts = disaster
  
  // RIGHT - Soft delete
  async function deleteUser(userId: string) {
    await db.user.update({
      where: { id: userId },
      data: { deletedAt: new Date() }
    })
    await queue.add('cleanup-user', { userId }) // Background batched cleanup
  }
  
  // RIGHT - Batched hard delete
  async function hardDeleteUser(userId: string) {
    while (true) {
      const deleted = await db.post.deleteMany({
        where: { authorId: userId },
        take: 1000
      })
      if (deleted.count === 0) break
      await sleep(100) // Don't hammer DB
    }
    await db.user.delete({ where: { id: userId } })
  }
  
### **Symptoms**
  - Long-running DELETE statements
  - Transaction timeouts on deletes
  - CASCADE DELETE in schema without volume analysis
### **Detection Pattern**
onDelete:\\s*Cascade

## Sync File Processing

### **Id**
sync-file-processing
### **Summary**
Processing file uploads synchronously blocks requests and times out
### **Severity**
high
### **Situation**
Image processing, video transcoding, PDF generation in request handler
### **Why**
  User uploads file. Server processes synchronously - parsing, resizing, storing.
  Large file takes 2 minutes. Connection times out. User retries. Now processing
  same file twice.
  
### **Solution**
  // WRONG - Synchronous processing
  app.post('/api/upload', async (req, res) => {
    const processed = await processImage(req.file) // Minutes for large files
    const uploaded = await uploadToS3(processed)
    res.json({ url: uploaded.url }) // Times out
  })
  
  // RIGHT - Async with job queue
  app.post('/api/upload', async (req, res) => {
    const rawUrl = await uploadRawToS3(req.file) // Quick
    const job = await fileQueue.add('process', { fileUrl: rawUrl })
    res.json({ jobId: job.id, status: 'processing', checkUrl: `/api/jobs/${job.id}` })
  })
  
  // Worker processes in background
  const worker = new Worker('file-processing', async (job) => {
    const processed = await processImage(job.data.fileUrl)
    await notifyUser(job.data.userId, { status: 'complete' })
  })
  
### **Symptoms**
  - Request timeouts on upload endpoints
  - No job queue in architecture
  - User complaints about "stuck" uploads
### **Detection Pattern**
processImage|resize|transcode|generatePdf

## Uncached Repeated Query

### **Id**
uncached-repeated-query
### **Summary**
Same query executed thousands of times for rarely-changing data
### **Severity**
high
### **Situation**
User preferences on every request, permission checks, config lookups
### **Why**
  Every page load queries user preferences. Every API call validates permissions.
  Thousands of queries for data that changes once a day. Database groans under
  load of serving identical data repeatedly.
  
### **Solution**
  // WRONG - Query on every request
  async function getUser(req, res) {
    const user = await db.user.findUnique({
      where: { id: req.userId },
      include: { preferences: true }
    }) // Called 10,000 times/minute for same user
  }
  
  // RIGHT - Cache with appropriate TTL
  async function getUser(userId: string) {
    const cacheKey = `user:${userId}`
    const cached = await redis.get(cacheKey)
    if (cached) return JSON.parse(cached)
  
    const user = await db.user.findUnique({ where: { id: userId }, include: { preferences: true } })
    await redis.setex(cacheKey, 300, JSON.stringify(user)) // 5 min cache
    return user
  }
  
  // Invalidate on update
  async function updateUser(userId: string, data) {
    await db.user.update({ where: { id: userId }, data })
    await redis.del(`user:${userId}`)
  }
  
### **Symptoms**
  - Same query appears thousands of times in logs
  - Database load doesn't match complexity
  - Adding Redis dramatically improves performance
### **Detection Pattern**
findUnique.*preferences|findUnique.*permissions