/**
 * Better Auth Server Configuration Template
 *
 * Usage:
 * 1. Copy this file to your project (e.g., src/lib/auth.ts)
 * 2. Replace DATABASE_ADAPTER with your ORM adapter
 * 3. Configure providers and plugins as needed
 * 4. Run: npx @better-auth/cli migrate
 */

import { betterAuth } from "better-auth";
import { nextCookies } from "better-auth/next-js"; // Remove if not using Next.js

// === CHOOSE YOUR DATABASE ADAPTER ===

// Option 1: Direct PostgreSQL
// import { Pool } from "pg";
// const database = new Pool({ connectionString: process.env.DATABASE_URL });

// Option 2: Drizzle
// import { drizzleAdapter } from "better-auth/adapters/drizzle";
// import { db } from "@/db";
// import * as schema from "@/db/auth-schema";
// const database = drizzleAdapter(db, { provider: "pg", schema });

// Option 3: Prisma
// import { prismaAdapter } from "better-auth/adapters/prisma";
// import { prisma } from "./prisma";
// const database = prismaAdapter(prisma, { provider: "postgresql" });

// Option 4: MongoDB
// import { mongodbAdapter } from "better-auth/adapters/mongodb";
// import { db } from "./mongodb";
// const database = mongodbAdapter(db);

// === PLACEHOLDER - REPLACE WITH YOUR ADAPTER ===
const database = null as any; // Replace this!

export const auth = betterAuth({
  // Database
  database,

  // App info
  appName: "My App",
  baseURL: process.env.BETTER_AUTH_URL,
  secret: process.env.BETTER_AUTH_SECRET,

  // Email/Password Authentication
  emailAndPassword: {
    enabled: true,
    // requireEmailVerification: true,
    // minPasswordLength: 8,
    // sendVerificationEmail: async ({ user, url }) => {
    //   await sendEmail({ to: user.email, subject: "Verify", html: `<a href="${url}">Verify</a>` });
    // },
    // sendResetPassword: async ({ user, url }) => {
    //   await sendEmail({ to: user.email, subject: "Reset", html: `<a href="${url}">Reset</a>` });
    // },
  },

  // Social Providers (uncomment as needed)
  socialProviders: {
    // google: {
    //   clientId: process.env.GOOGLE_CLIENT_ID!,
    //   clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    // },
    // github: {
    //   clientId: process.env.GITHUB_CLIENT_ID!,
    //   clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    // },
    // discord: {
    //   clientId: process.env.DISCORD_CLIENT_ID!,
    //   clientSecret: process.env.DISCORD_CLIENT_SECRET!,
    // },
  },

  // Session Configuration
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day
    cookieCache: {
      enabled: true,
      maxAge: 5 * 60, // 5 minutes
    },
  },

  // Custom User Fields (optional)
  // user: {
  //   additionalFields: {
  //     role: {
  //       type: "string",
  //       defaultValue: "user",
  //       input: false,
  //     },
  //   },
  // },

  // Rate Limiting
  // rateLimit: {
  //   window: 60,
  //   max: 10,
  // },

  // Plugins
  plugins: [
    nextCookies(), // Must be last - remove if not using Next.js

    // Uncomment plugins as needed:
    // jwt(), // For external API verification
    // twoFactor(), // 2FA
    // magicLink({ sendMagicLink: async ({ email, url }) => { ... } }),
    // organization(),
  ],
});

export type Auth = typeof auth;
