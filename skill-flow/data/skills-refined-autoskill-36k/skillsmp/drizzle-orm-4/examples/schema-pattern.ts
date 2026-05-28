/**
 * Example Schema Pattern - Neon Database
 */

import { pgTable, pgEnum, index, text, timestamp, integer, varchar } from "drizzle-orm/pg-core"
import type { InferSelectModel, InferInsertModel } from "drizzle-orm"

// ============================================================================
// Enums
// ============================================================================

export const statusEnum = pgEnum("status", ["draft", "published", "archived"])

// ============================================================================
// Tables
// ============================================================================

export const posts = pgTable("posts", {
  id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
  title: varchar("title", { length: 255 }).notNull(),
  content: text("content").notNull(),
  status: statusEnum("status").notNull().default("draft"),
  author_id: integer("author_id").notNull().references(() => users.id, { onDelete: "cascade" }),
  created_at: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updated_at: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
}, (table) => [
  index("idx_posts_title").on(table.title),
  index("idx_posts_author_id").on(table.author_id),
  index("idx_posts_status").on(table.status),
])

export const users = pgTable("users", {
  id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
  email: varchar("email", { length: 255 }).notNull().unique(),
  name: varchar("name", { length: 255 }).notNull(),
  created_at: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
}, (table) => [
  index("idx_users_email").on(table.email),
])

// ============================================================================
// Type Exports
// ============================================================================

export type Post = InferSelectModel<typeof posts>
export type InsertPost = InferInsertModel<typeof posts>

export type User = InferSelectModel<typeof users>
export type InsertUser = InferInsertModel<typeof users>

// Serialized types for JSON responses
export type PostSerialized = Omit<Post, "created_at" | "updated_at" | "status"> & {
  status: string
  created_at?: string
  updated_at?: string
}
