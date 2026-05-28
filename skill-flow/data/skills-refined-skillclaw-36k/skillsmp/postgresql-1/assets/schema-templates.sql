-- ============================================
-- PostgreSQL Schema Templates for Aurora
-- ============================================

-- ============================================
-- 1. STANDARD TABLE TEMPLATE
-- ============================================

CREATE TABLE IF NOT EXISTS "TableName" (
    -- Primary key (UUID recommended for Aurora)
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),

    -- Auto-increment row ID (for ordering, legacy compatibility)
    "rowId" BIGSERIAL NOT NULL,

    -- Business fields
    "code" VARCHAR(64),
    "name" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "status" VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',

    -- Metadata
    "meta" JSONB DEFAULT '{}',
    "tags" TEXT[] DEFAULT '{}',

    -- Audit fields
    "createdAt" TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    "updatedAt" TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    "deletedAt" TIMESTAMP WITH TIME ZONE,

    -- Constraints
    PRIMARY KEY ("id"),
    UNIQUE ("rowId"),
    UNIQUE ("code")
);

-- Essential indexes
CREATE INDEX IF NOT EXISTS "idx_TableName_createdAt" ON "TableName" ("createdAt" DESC);
CREATE INDEX IF NOT EXISTS "idx_TableName_status" ON "TableName" ("status") WHERE "deletedAt" IS NULL;
CREATE INDEX IF NOT EXISTS "idx_TableName_tags" ON "TableName" USING GIN ("tags");
CREATE INDEX IF NOT EXISTS "idx_TableName_meta" ON "TableName" USING GIN ("meta");


-- ============================================
-- 2. MULTI-TENANT TABLE TEMPLATE
-- ============================================

CREATE TABLE IF NOT EXISTS "TenantEntity" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "rowId" BIGSERIAL NOT NULL,

    -- Tenant reference (required for multi-tenant)
    "tenantId" UUID NOT NULL,

    -- Business fields
    "code" VARCHAR(64),
    "name" VARCHAR(255) NOT NULL,

    -- Audit
    "createdAt" TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    "updatedAt" TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    "deletedAt" TIMESTAMP WITH TIME ZONE,

    PRIMARY KEY ("id"),
    UNIQUE ("rowId"),
    UNIQUE ("tenantId", "code"),  -- Unique per tenant
    FOREIGN KEY ("tenantId") REFERENCES "IamTenant" ("id") ON DELETE CASCADE
);

-- Indexes for multi-tenant queries
CREATE INDEX IF NOT EXISTS "idx_TenantEntity_tenantId" ON "TenantEntity" ("tenantId");
CREATE INDEX IF NOT EXISTS "idx_TenantEntity_tenant_code" ON "TenantEntity" ("tenantId", "code");


-- ============================================
-- 3. PIVOT/JUNCTION TABLE TEMPLATE
-- ============================================

CREATE TABLE IF NOT EXISTS "EntityRelation" (
    -- Composite primary key
    "entityAId" UUID NOT NULL,
    "entityBId" UUID NOT NULL,

    -- Optional: additional fields
    "createdAt" TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    PRIMARY KEY ("entityAId", "entityBId"),
    FOREIGN KEY ("entityAId") REFERENCES "EntityA" ("id") ON DELETE CASCADE,
    FOREIGN KEY ("entityBId") REFERENCES "EntityB" ("id") ON DELETE CASCADE
);

-- Indexes for reverse lookups
CREATE INDEX IF NOT EXISTS "idx_EntityRelation_entityBId" ON "EntityRelation" ("entityBId");


-- ============================================
-- 4. ENUM TYPE TEMPLATE
-- ============================================

-- Create enum type
DO $$ BEGIN
    CREATE TYPE "order_status" AS ENUM (
        'DRAFT',
        'PENDING',
        'CONFIRMED',
        'IN_PROGRESS',
        'COMPLETED',
        'CANCELLED'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Use in table
CREATE TABLE IF NOT EXISTS "Order" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "status" order_status NOT NULL DEFAULT 'DRAFT',
    PRIMARY KEY ("id")
);

-- Add new enum value (safe migration)
ALTER TYPE "order_status" ADD VALUE IF NOT EXISTS 'ON_HOLD' AFTER 'CONFIRMED';


-- ============================================
-- 5. JSONB WITH VALIDATION TEMPLATE
-- ============================================

CREATE TABLE IF NOT EXISTS "Product" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "name" VARCHAR(255) NOT NULL,

    -- JSONB with structure
    "specs" JSONB NOT NULL DEFAULT '{}',
    "attributes" JSONB NOT NULL DEFAULT '[]',

    -- Validation constraints
    CONSTRAINT "valid_specs" CHECK (
        jsonb_typeof("specs") = 'object' AND
        "specs" ? 'weight' AND
        "specs" ? 'dimensions'
    ),
    CONSTRAINT "valid_attributes" CHECK (
        jsonb_typeof("attributes") = 'array'
    ),

    PRIMARY KEY ("id")
);

-- GIN indexes for JSONB queries
CREATE INDEX IF NOT EXISTS "idx_Product_specs" ON "Product" USING GIN ("specs");
CREATE INDEX IF NOT EXISTS "idx_Product_specs_path" ON "Product" USING GIN ("specs" jsonb_path_ops);


-- ============================================
-- 6. FULL-TEXT SEARCH TABLE TEMPLATE
-- ============================================

CREATE TABLE IF NOT EXISTS "Article" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "title" VARCHAR(255) NOT NULL,
    "body" TEXT NOT NULL,
    "tags" TEXT[] DEFAULT '{}',

    -- Full-text search vector
    "searchVector" TSVECTOR,

    "createdAt" TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    "updatedAt" TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    PRIMARY KEY ("id")
);

-- GIN index for full-text search
CREATE INDEX IF NOT EXISTS "idx_Article_search" ON "Article" USING GIN ("searchVector");

-- Trigger to auto-update search vector
CREATE OR REPLACE FUNCTION "update_article_search_vector"() RETURNS trigger AS $$
BEGIN
    NEW."searchVector" :=
        setweight(to_tsvector('english', COALESCE(NEW."title", '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW."body", '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(array_to_string(NEW."tags", ' '), '')), 'C');
    RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER "tsvector_update_Article"
    BEFORE INSERT OR UPDATE ON "Article"
    FOR EACH ROW EXECUTE FUNCTION "update_article_search_vector"();


-- ============================================
-- 7. RANGE/BOOKING TABLE TEMPLATE
-- ============================================

CREATE TABLE IF NOT EXISTS "RoomBooking" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "roomId" UUID NOT NULL,
    "userId" UUID NOT NULL,

    -- Range type for booking period
    "during" TSTZRANGE NOT NULL,

    "createdAt" TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    PRIMARY KEY ("id"),

    -- Exclusion constraint: no overlapping bookings for same room
    CONSTRAINT "no_overlapping_bookings"
        EXCLUDE USING GIST ("roomId" WITH =, "during" WITH &&)
);

-- Index for range queries
CREATE INDEX IF NOT EXISTS "idx_RoomBooking_during" ON "RoomBooking" USING GIST ("during");
CREATE INDEX IF NOT EXISTS "idx_RoomBooking_roomId" ON "RoomBooking" ("roomId");


-- ============================================
-- 8. PARTITIONED TABLE TEMPLATE (Time-based)
-- ============================================

-- Parent table
CREATE TABLE IF NOT EXISTS "AuditLog" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "entityType" VARCHAR(64) NOT NULL,
    "entityId" UUID NOT NULL,
    "action" VARCHAR(32) NOT NULL,
    "changes" JSONB,
    "userId" UUID,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
) PARTITION BY RANGE ("createdAt");

-- Create partitions by month
CREATE TABLE IF NOT EXISTS "AuditLog_2024_01" PARTITION OF "AuditLog"
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE IF NOT EXISTS "AuditLog_2024_02" PARTITION OF "AuditLog"
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
-- Continue for each month...

-- Default partition for future data
CREATE TABLE IF NOT EXISTS "AuditLog_default" PARTITION OF "AuditLog" DEFAULT;

-- Indexes on partitioned table (created on each partition automatically)
CREATE INDEX IF NOT EXISTS "idx_AuditLog_entityType_entityId"
    ON "AuditLog" ("entityType", "entityId");
CREATE INDEX IF NOT EXISTS "idx_AuditLog_userId"
    ON "AuditLog" ("userId");


-- ============================================
-- 9. HIERARCHICAL DATA TEMPLATE (Closure Table)
-- ============================================

-- Main entity table
CREATE TABLE IF NOT EXISTS "Category" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "parentId" UUID,
    "name" VARCHAR(255) NOT NULL,
    "level" INTEGER NOT NULL DEFAULT 0,

    PRIMARY KEY ("id"),
    FOREIGN KEY ("parentId") REFERENCES "Category" ("id") ON DELETE CASCADE
);

-- Closure table for efficient ancestor/descendant queries
CREATE TABLE IF NOT EXISTS "CategoryClosure" (
    "ancestorId" UUID NOT NULL,
    "descendantId" UUID NOT NULL,
    "depth" INTEGER NOT NULL,

    PRIMARY KEY ("ancestorId", "descendantId"),
    FOREIGN KEY ("ancestorId") REFERENCES "Category" ("id") ON DELETE CASCADE,
    FOREIGN KEY ("descendantId") REFERENCES "Category" ("id") ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS "idx_CategoryClosure_descendant"
    ON "CategoryClosure" ("descendantId");


-- ============================================
-- 10. SOFT DELETE WITH HISTORY TEMPLATE
-- ============================================

CREATE TABLE IF NOT EXISTS "Document" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "version" INTEGER NOT NULL DEFAULT 1,
    "name" VARCHAR(255) NOT NULL,
    "content" TEXT,

    "createdAt" TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    "updatedAt" TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    "deletedAt" TIMESTAMP WITH TIME ZONE,
    "deletedBy" UUID,

    PRIMARY KEY ("id")
);

-- History table for versioning
CREATE TABLE IF NOT EXISTS "DocumentHistory" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "documentId" UUID NOT NULL,
    "version" INTEGER NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "content" TEXT,
    "changedAt" TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    "changedBy" UUID,

    PRIMARY KEY ("id"),
    UNIQUE ("documentId", "version"),
    FOREIGN KEY ("documentId") REFERENCES "Document" ("id") ON DELETE CASCADE
);

-- Trigger to create history on update
CREATE OR REPLACE FUNCTION "create_document_history"() RETURNS trigger AS $$
BEGIN
    INSERT INTO "DocumentHistory" ("documentId", "version", "name", "content", "changedBy")
    VALUES (OLD."id", OLD."version", OLD."name", OLD."content", NEW."deletedBy");
    NEW."version" := OLD."version" + 1;
    RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER "document_history_trigger"
    BEFORE UPDATE ON "Document"
    FOR EACH ROW EXECUTE FUNCTION "create_document_history"();


-- ============================================
-- 11. EXTENSION SETUP
-- ============================================

-- Common extensions for Aurora projects
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";      -- UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";       -- Crypto functions
CREATE EXTENSION IF NOT EXISTS "pg_trgm";        -- Fuzzy text search
CREATE EXTENSION IF NOT EXISTS "citext";         -- Case-insensitive text
CREATE EXTENSION IF NOT EXISTS "btree_gist";     -- Exclusion constraints with =
