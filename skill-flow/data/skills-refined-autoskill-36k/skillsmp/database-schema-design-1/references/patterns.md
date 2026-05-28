# Database Schema Design

## Patterns


---
  #### **Name**
Explicit NOT NULL with Defaults
  #### **Description**
Every column declares nullability explicitly with sensible defaults
  #### **When**
Designing any new table or adding columns
  #### **Example**
    // GOOD - Explicit, defensive
    model User {
      id        String   @id @default(uuid())
      email     String   @unique
      name      String   @default("")    // NOT NULL with default
      bio       String?                  // Explicitly nullable
      isActive  Boolean  @default(true)  // NOT NULL with default
      createdAt DateTime @default(now())
      updatedAt DateTime @updatedAt
    }
    
    // BAD - Implicit nullability, missing defaults
    model User {
      id    String  @id
      email String
      name  String  // NULL or NOT NULL? Depends on ORM default
      bio   String  // Probably nullable but unclear
    }
    

---
  #### **Name**
UUID v7 for Distributed Systems
  #### **Description**
Use time-ordered UUIDs for better index performance and sortability
  #### **When**
Distributed systems, sharding, or when you need both uniqueness and ordering
  #### **Example**
    // PostgreSQL 18+ (Fall 2025)
    CREATE TABLE orders (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid_v7(),
      created_at TIMESTAMPTZ DEFAULT NOW()
    );
    
    // Node.js with uuid package v10+
    import { v7 as uuidv7 } from 'uuid';
    
    model Order {
      id String @id @default(dbgenerated("gen_random_uuid()"))
      // For app-generated v7: use middleware to set id = uuidv7()
    }
    
    // Why v7 over v4:
    // - Time-ordered: preserves insertion order in B-tree
    // - Sortable: no need for separate createdAt for ordering
    // - Distributed: no central sequence required
    

---
  #### **Name**
Soft Delete with Unique Constraint Handling
  #### **Description**
Mark records deleted instead of removing, but handle unique constraints properly
  #### **When**
Need audit trails, recovery capability, or legal/compliance requirements
  #### **Example**
    model User {
      id        String    @id @default(uuid())
      email     String    // NOT unique alone
      deletedAt DateTime?
    
      @@unique([email, deletedAt]) // Composite unique
      // email + NULL = unique active user
      // email + timestamp = unique deleted record
    }
    
    // Alternative: Partial unique index (PostgreSQL)
    CREATE UNIQUE INDEX users_email_unique
      ON users(email)
      WHERE deleted_at IS NULL;
    
    // Query pattern
    const activeUsers = await prisma.user.findMany({
      where: { deletedAt: null }
    });
    

---
  #### **Name**
Junction Table with Metadata
  #### **Description**
Many-to-many with additional relationship data on the junction table
  #### **When**
Relationships have their own attributes (role, joined_at, permissions)
  #### **Example**
    // Junction table IS an entity when it has data
    model TeamMembership {
      id       String   @id @default(uuid())
      userId   String
      teamId   String
      role     Role     @default(MEMBER)
      joinedAt DateTime @default(now())
    
      user User @relation(fields: [userId], references: [id])
      team Team @relation(fields: [teamId], references: [id])
    
      @@unique([userId, teamId])
      @@index([teamId])  // Query: "all members of team X"
      @@index([userId])  // Query: "all teams for user Y"
    }
    
    enum Role {
      OWNER
      ADMIN
      MEMBER
    }
    

---
  #### **Name**
Exclusive Arc for Polymorphic Associations
  #### **Description**
Use separate foreign keys with check constraints instead of type discriminator
  #### **When**
Entity can belong to one of several parent types (comments on posts/products/users)
  #### **Example**
    // GOOD - Exclusive arc with database-enforced integrity
    model Comment {
      id        String  @id @default(uuid())
      content   String
    
      // One of these will be set, others NULL
      postId    String?
      productId String?
      userId    String?
    
      post    Post?    @relation(fields: [postId], references: [id])
      product Product? @relation(fields: [productId], references: [id])
      user    User?    @relation(fields: [userId], references: [id])
    }
    
    -- PostgreSQL: Enforce exactly one parent
    ALTER TABLE comments ADD CONSTRAINT comment_single_parent CHECK (
      (CASE WHEN post_id IS NOT NULL THEN 1 ELSE 0 END +
       CASE WHEN product_id IS NOT NULL THEN 1 ELSE 0 END +
       CASE WHEN user_id IS NOT NULL THEN 1 ELSE 0 END) = 1
    );
    
    // BAD - Type discriminator (no FK enforcement)
    model Comment {
      commentableType String  // "Post" | "Product" | "User"
      commentableId   String  // Can't enforce FK!
    }
    

---
  #### **Name**
Audit Trail with Immutable Append
  #### **Description**
Track all changes by appending records, never updating history
  #### **When**
Compliance requirements, debugging, undo functionality
  #### **Example**
    model Order {
      id        String   @id @default(uuid())
      status    String   @default("pending")
      total     Decimal
      updatedAt DateTime @updatedAt
    
      history OrderHistory[]
    }
    
    model OrderHistory {
      id        String   @id @default(uuid())
      orderId   String
      status    String
      changedBy String
      changedAt DateTime @default(now())
      metadata  Json?    // What changed and why
    
      order Order @relation(fields: [orderId], references: [id])
    
      @@index([orderId, changedAt])
    }
    
    // On every status change:
    await prisma.$transaction([
      prisma.order.update({ where: { id }, data: { status: newStatus } }),
      prisma.orderHistory.create({
        data: { orderId: id, status: newStatus, changedBy: userId }
      })
    ]);
    

## Anti-Patterns


---
  #### **Name**
Implicit Nullability
  #### **Description**
Not specifying NULL/NOT NULL and relying on ORM defaults
  #### **Why**
Different ORMs have different defaults. PostgreSQL columns are nullable by default. You'll have NULL checks everywhere in application code.
  #### **Instead**
Every column explicitly declares nullability. Default to NOT NULL with sensible defaults.

---
  #### **Name**
Type Discriminator Polymorphism
  #### **Description**
Using commentableType + commentableId instead of separate foreign keys
  #### **Why**
Database cannot enforce referential integrity. Orphaned records accumulate. Joins require CASE statements.
  #### **Instead**
Use exclusive arc pattern with separate nullable FKs and CHECK constraint.

---
  #### **Name**
Missing Index on Foreign Key
  #### **Description**
Creating foreign key relationships without explicit indexes
  #### **Why**
JOINs become full table scans. DELETE of parent record locks entire child table. Works in dev, dies in production.
  #### **Instead**
Always add @@index on foreign key columns. PostgreSQL doesn't auto-create them.

---
  #### **Name**
VARCHAR Without Length
  #### **Description**
Using VARCHAR/TEXT without considering reasonable limits
  #### **Why**
Users paste entire documents. Storage bloats. Queries slow down. No validation at database level.
  #### **Instead**
Set VARCHAR(n) with reasonable max. Use TEXT only when truly unbounded content is expected.

---
  #### **Name**
Over-Normalization
  #### **Description**
Splitting every piece of data into its own table for theoretical purity
  #### **Why**
Simple queries require 10 JOINs. Performance suffers. Developer productivity tanks.
  #### **Instead**
Normalize for integrity, denormalize for reads. User.fullName is fine - no need for separate Names table.

---
  #### **Name**
Under-Normalization
  #### **Description**
Storing denormalized data everywhere without thinking about updates
  #### **Why**
Order shows customer name. Customer updates name. Now orders show old name. Data inconsistency spreads.
  #### **Instead**
Normalize transactional data. Denormalize only for read-heavy analytics or caching layers.