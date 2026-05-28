/**
 * Course Modules Data
 * Complete curriculum for Microservices Learning Platform
 * Each module contains detailed, beginner-friendly explanations
 */

export const modules = [
  // ============================================
  // MODULE 0: SHOULD YOU USE MICROSERVICES?
  // This is the most important module - START HERE
  // ============================================
  {
    number: 0,
    slug: "should-you-use-microservices",
    title: "Should You Use Microservices?",
    description: "The most important module. Learn when microservices are the WRONG choice, the true costs nobody talks about, and alternatives like the Modular Monolith.",
    difficulty: "beginner",
    topics: ["Microservices Hype", "True Costs", "Monolith Benefits", "Modular Monolith", "Decision Framework", "Common Mistakes"],
    prerequisites: ["None - START HERE"],
    isRequired: true,
    learningOutcomes: [
      "Identify when microservices are NOT the right choice",
      "Calculate the true cost of microservices adoption",
      "Explain the benefits of starting with a monolith",
      "Describe the Modular Monolith as an alternative",
      "Make informed architecture decisions based on team size and requirements"
    ],
    estimatedTime: "30–45 minutes",
    content: {
      intro: `🛑 **STOP. Read this before learning anything else.**

This is the most important module in the entire course. Before you learn HOW to build microservices, you need to understand WHETHER you should build them at all.

**The Uncomfortable Truth:**

Most companies that adopt microservices shouldn't have. They add complexity, slow down small teams, and solve problems you probably don't have yet.

**This module will help you:**
- Avoid the #1 mistake teams make (adopting microservices too early)
- Understand the REAL costs (not just the benefits you see in blog posts)
- Learn about alternatives that might be better for you
- Make an informed decision, not a hype-driven one

**Be honest with yourself as you read this.** If anything describes your situation, you probably shouldn't use microservices yet.`,
      sections: [
        {
          title: "The Microservices Hype Problem",
          content: `**Why is everyone talking about microservices?**

Because Netflix, Amazon, Google, and Uber use them. And if it works for them, it must work for us, right?

**Wrong.**

Netflix has:
- 2,000+ engineers
- 200+ million users
- $30+ billion revenue
- Dedicated platform teams

You probably have:
- 5-50 engineers
- Thousands to millions of users
- A fraction of their resources
- Everyone wearing multiple hats

**The Survivorship Bias:**

You hear about Netflix's success with microservices. You DON'T hear about:
- The thousands of startups that failed because they over-engineered with microservices
- The companies that quietly migrated BACK to monoliths
- The teams that spent months on infrastructure instead of features

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│                    WHAT YOU HEAR VS REALITY                      │
│                                                                  │
│   Blog Posts / Conferences:        Reality:                     │
│   ────────────────────────         ────────                     │
│   "Microservices enabled us        "We have 200 engineers       │
│    to scale to 1M users!"          and it took 3 years to       │
│                                    get here"                    │
│                                                                  │
│   "Independent deployments         "We have 15 dedicated        │
│    changed everything!"            DevOps engineers"            │
│                                                                  │
│   "Our teams are so much           "We spent $2M on            │
│    more productive!"               infrastructure first"        │
│                                                                  │
│   What they DON'T mention:                                      │
│   ─────────────────────────                                     │
│   • How many engineers they had before starting                 │
│   • How long it took to get the infrastructure right            │
│   • How much money they spent on tooling                        │
│   • The failed attempts before it worked                        │
└─────────────────────────────────────────────────────────────────┘
\`\`\``,
          keyPoints: [
            "Netflix has 2,000+ engineers. You probably don't.",
            "Success stories have survivorship bias - failures are silent",
            "Microservices solve organizational problems, not technical ones",
            "What works at scale doesn't work for small teams"
          ]
        },
        {
          title: "The True Cost of Microservices",
          content: `Nobody talks about the REAL costs. Let's fix that.

**1. Infrastructure Complexity (10-100x more complex)**

Monolith needs:
- 1 server / container
- 1 database
- 1 deployment pipeline
- Basic monitoring

Microservices need:
- Kubernetes cluster (or equivalent)
- Service mesh (Istio/Linkerd)
- Multiple databases
- Message queue (Kafka/RabbitMQ)
- API Gateway
- Service discovery
- Distributed tracing
- Centralized logging
- Secret management
- 10+ deployment pipelines

**Estimated additional cost: $50,000 - $500,000/year** (cloud + tooling)

**2. Team Expertise Requirements**

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│           SKILLS NEEDED FOR MICROSERVICES                        │
│                                                                  │
│  Monolith:                    Microservices:                    │
│  ─────────                    ──────────────                    │
│  ✅ Backend development        ✅ Backend development            │
│  ✅ Database skills            ✅ Database skills               │
│  ✅ Basic deployment           ✅ Docker                        │
│                               ✅ Kubernetes                     │
│                               ✅ Service mesh                   │
│                               ✅ Message queues                 │
│                               ✅ Distributed tracing            │
│                               ✅ CI/CD pipelines                │
│                               ✅ Infrastructure as Code         │
│                               ✅ Distributed systems theory     │
│                               ✅ Network debugging              │
│                                                                  │
│  Team size needed: 2-5        Team size needed: 10-20+          │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**3. Cognitive Load**

With a monolith:
- "Where is the user authentication code?" → \`src/auth/\`
- Debug an issue → Look at one log file
- Understand the flow → Read one codebase

With microservices:
- "Where is the user authentication code?" → Which service? Auth? User? Gateway?
- Debug an issue → Check 5 services, correlate logs, trace requests across network
- Understand the flow → Read 10 repos, understand message queues, trace events

**4. Development Speed (Initially SLOWER)**

\`\`\`
Feature Development Time:
─────────────────────────

Monolith:
  Week 1: Build feature
  Week 2: Test & deploy
  ✅ Done in 2 weeks

Microservices (first time):
  Week 1-2: Figure out which services need changes
  Week 3-4: Update service contracts / APIs
  Week 5-6: Build feature across services
  Week 7-8: Integration testing
  Week 9-10: Deploy and debug distributed issues
  ✅ Done in 10 weeks (5x slower!)
\`\`\`

This improves over time, but the initial slowdown is REAL.`,
          keyPoints: [
            "Infrastructure costs: $50K-$500K/year additional",
            "You need 2-3x more engineers with specialized skills",
            "Debugging is 10x harder across distributed services",
            "Initial development is 2-5x slower"
          ]
        },
        {
          title: "The Monolith is NOT the Enemy",
          content: `**Successful companies running monoliths TODAY:**

- **Shopify** - $5B+ revenue, powers 10% of US e-commerce
- **Stack Overflow** - Serves 100M+ developers monthly
- **Basecamp** - Profitable for 20+ years
- **Etsy** - $13B market cap, moved BACK from microservices

**Why Monoliths Work:**

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│              MONOLITH ADVANTAGES                                 │
│                                                                  │
│  1. SIMPLE DEVELOPMENT                                          │
│     • One codebase to understand                                │
│     • Local development is easy                                 │
│     • IDE features work perfectly (find references, refactor)   │
│                                                                  │
│  2. SIMPLE DEPLOYMENT                                           │
│     • One thing to deploy                                       │
│     • One thing to monitor                                      │
│     • Rollback is straightforward                               │
│                                                                  │
│  3. SIMPLE DEBUGGING                                            │
│     • Stack traces show the full picture                        │
│     • No network calls to trace                                 │
│     • One log file to check                                     │
│                                                                  │
│  4. NO DISTRIBUTED SYSTEMS PROBLEMS                             │
│     • No network partitions                                     │
│     • No eventual consistency                                   │
│     • No message queue failures                                 │
│     • ACID transactions work normally                           │
│                                                                  │
│  5. FAST                                                        │
│     • Function calls, not network calls                         │
│     • No serialization/deserialization                          │
│     • No network latency                                        │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**"But what if my monolith becomes a Big Ball of Mud?"**

That's a code organization problem, not an architecture problem. A poorly organized monolith becomes a poorly organized set of microservices (often called a "Distributed Monolith" - the worst of both worlds).

**The solution? Modular Monolith.**`,
          keyPoints: [
            "Shopify, Stack Overflow, and Etsy run on monoliths",
            "Monoliths are simpler to develop, deploy, and debug",
            "A messy monolith becomes a messy distributed system",
            "Fix code organization first, not architecture"
          ]
        },
        {
          title: "The Modular Monolith: The Best of Both Worlds",
          content: `**What is a Modular Monolith?**

A single deployable application, but internally organized into well-defined modules with clear boundaries.

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│                    MODULAR MONOLITH                              │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    SINGLE APPLICATION                       │ │
│  │                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   USERS     │  │   ORDERS    │  │  PRODUCTS   │        │ │
│  │  │   MODULE    │  │   MODULE    │  │   MODULE    │        │ │
│  │  │             │  │             │  │             │        │ │
│  │  │ • Entities  │  │ • Entities  │  │ • Entities  │        │ │
│  │  │ • Services  │  │ • Services  │  │ • Services  │        │ │
│  │  │ • Repos     │  │ • Repos     │  │ • Repos     │        │ │
│  │  │ • API       │  │ • API       │  │ • API       │        │ │
│  │  │             │  │             │  │             │        │ │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │ │
│  │         │                │                │                │ │
│  │         └────────────────┴────────────────┘                │ │
│  │                          │                                  │ │
│  │              ┌───────────▼───────────┐                     │ │
│  │              │    SHARED KERNEL      │                     │ │
│  │              │  (Common utilities)   │                     │ │
│  │              └───────────────────────┘                     │ │
│  │                                                             │ │
│  └────────────────────────────────────────────────────────────┘ │
│                           │                                      │
│                           ▼                                      │
│                  ┌─────────────────┐                            │
│                  │  ONE DATABASE   │                            │
│                  │  (Separate      │                            │
│                  │   schemas OK)   │                            │
│                  └─────────────────┘                            │
│                                                                  │
│  ✅ Clear boundaries between modules                            │
│  ✅ Single deployment                                           │
│  ✅ Can extract to microservices later                         │
│  ✅ No distributed systems complexity                          │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**Rules for Modular Monolith:**

1. **Modules communicate through public APIs only**
   \`\`\`typescript
   // ❌ BAD: Direct access to another module's internals
   import { UserRepository } from '../users/repositories/user.repository';
   
   // ✅ GOOD: Use the module's public API
   import { UsersModule } from '../users';
   const user = await UsersModule.getUser(userId);
   \`\`\`

2. **Each module owns its database tables**
   - Users module → users, profiles, auth tables
   - Orders module → orders, order_items tables
   - No direct cross-module table access!

3. **Modules can define clear interfaces**
   \`\`\`typescript
   // users/public-api.ts
   export interface UsersModuleAPI {
     getUser(id: string): Promise<User>;
     validateCredentials(email: string, password: string): Promise<boolean>;
   }
   \`\`\`

**Migration Path to Microservices:**

When you're ready (team size 20+, clear scaling needs), extract modules one by one:

\`\`\`
Phase 1: Modular Monolith (Team: 5-15)
───────────────────────────────────────
[Users Module] [Orders Module] [Products Module]
                    ↓
Phase 2: Extract high-traffic module (Team: 15-30)
───────────────────────────────────────
[Users Module] [Orders Module]    [Products Service] ← Extracted
        Monolith                    Microservice
                    ↓
Phase 3: Full microservices (Team: 30+)
───────────────────────────────────────
[Users Service] [Orders Service] [Products Service]
              All Microservices
\`\`\``,
          keyPoints: [
            "Modular Monolith = clear boundaries without distributed complexity",
            "Modules communicate through public APIs, not direct imports",
            "Each module owns its data (separate schemas/tables)",
            "Easy migration path: extract modules when needed"
          ]
        },
        {
          title: "Decision Framework: Should YOU Use Microservices?",
          content: `**Answer these questions honestly:**

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│              MICROSERVICES DECISION CHECKLIST                    │
│                                                                  │
│  TEAM SIZE                                           Score      │
│  ──────────                                                     │
│  □ We have fewer than 10 engineers                    -2        │
│  □ We have 10-30 engineers                             0        │
│  □ We have 30+ engineers                              +2        │
│                                                                  │
│  DEVOPS EXPERTISE                                               │
│  ───────────────                                                │
│  □ No dedicated DevOps/Platform team                  -2        │
│  □ 1-2 people handle infrastructure                   -1        │
│  □ Dedicated platform team (3+ people)                +2        │
│                                                                  │
│  DEPLOYMENT NEEDS                                               │
│  ────────────────                                               │
│  □ We deploy monthly or less                          -1        │
│  □ We deploy weekly                                    0        │
│  □ We need to deploy multiple times per day           +2        │
│                                                                  │
│  SCALING REQUIREMENTS                                           │
│  ────────────────────                                           │
│  □ Traffic is relatively uniform across features      -1        │
│  □ Some features need independent scaling             +1        │
│  □ Wildly different scaling needs per feature         +2        │
│                                                                  │
│  TECHNOLOGY REQUIREMENTS                                        │
│  ───────────────────────                                        │
│  □ One language/framework works for everything        -1        │
│  □ Some features need different tech stacks           +1        │
│                                                                  │
│  ORGANIZATIONAL STRUCTURE                                       │
│  ────────────────────────                                       │
│  □ Cross-functional teams work on all parts            0        │
│  □ Teams own specific business domains                +2        │
│                                                                  │
│  CURRENT STATE                                                  │
│  ─────────────                                                  │
│  □ Building a new product / MVP                       -3        │
│  □ Existing product with growing pains                +1        │
│  □ Proven product with clear boundaries               +2        │
│                                                                  │
│  ═══════════════════════════════════════════════════════════   │
│                                                                  │
│  SCORE INTERPRETATION:                                          │
│  ─────────────────────                                          │
│  -10 to -3:  🔴 DEFINITELY use a Monolith                       │
│   -2 to +2:  🟡 Consider Modular Monolith                       │
│   +3 to +5:  🟢 Microservices might make sense                  │
│   +6 to +10: ✅ Microservices are probably right for you        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**Red Flags - DO NOT use microservices if:**

❌ You're building an MVP or new product
❌ Your team has fewer than 10 engineers
❌ You don't have dedicated DevOps expertise
❌ You haven't clearly identified service boundaries
❌ "Because Netflix does it" is your main reason`,
          keyPoints: [
            "Be honest with the checklist - bias towards monolith if unsure",
            "Team size is the #1 factor (< 10 people = don't do it)",
            "MVPs should ALWAYS start as monoliths",
            "'Because Netflix does it' is never a good reason"
          ]
        },
        {
          title: "Real Stories: Companies That Went Back to Monoliths",
          content: `**These are real examples, not theoretical:**

**1. Segment (Data Platform)**
- Started with microservices
- Had 100+ microservices
- Went back to monolith
- CEO quote: "Microservices added latency and complexity without proportional benefit"

**2. Kelsey Hightower (Google, Kubernetes co-creator)**
"Monoliths are the future... Microservices were a mistake for most companies."

**3. Amazon Prime Video (2023)**
- Moved from microservices to monolith for video monitoring
- Reduced costs by 90%
- Improved performance significantly
- Blog post: "Scaling up the Prime Video audio/video monitoring service and reducing costs by 90%"

**4. Etsy**
- Experimented with microservices
- Went back to their PHP monolith
- Still serving millions of users successfully

**Common Patterns in Failed Microservices Adoptions:**

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│           WHY MICROSERVICES ADOPTIONS FAIL                       │
│                                                                  │
│  1. PREMATURE DECOMPOSITION                                     │
│     "We split into microservices before we understood           │
│      our domain. Now services are constantly calling            │
│      each other."                                               │
│     → Created a distributed monolith                            │
│                                                                  │
│  2. INFRASTRUCTURE UNDERESTIMATION                              │
│     "We thought we could just deploy multiple apps.             │
│      We didn't realize we needed Kubernetes, service            │
│      mesh, distributed tracing..."                              │
│     → Spent 6 months on infrastructure, 0 features              │
│                                                                  │
│  3. TEAM SIZE MISMATCH                                          │
│     "We have 8 engineers and 20 microservices.                  │
│      Everyone is on-call for everything."                       │
│     → Burnout, high turnover                                    │
│                                                                  │
│  4. WRONG REASONS                                               │
│     "Our CTO saw a conference talk about microservices          │
│      at Netflix..."                                             │
│     → Solution looking for a problem                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**The Pattern That Works:**

\`\`\`
SUCCESSFUL PATH:
────────────────

Year 1-2: Monolith (5-15 engineers)
  • Focus on product-market fit
  • Ship features fast
  • Learn your domain

Year 2-3: Modular Monolith (15-30 engineers)
  • Establish clear module boundaries
  • Teams own modules
  • Prepare for extraction

Year 3+: Gradual Microservices (30+ engineers)
  • Extract one service at a time
  • Only when you have a specific need
  • Keep most things in the monolith

FAILED PATH:
────────────

Day 1: "Let's use microservices from the start!"
Month 3: Still setting up Kubernetes
Month 6: First feature deployed
Year 1: Competitors have lapped you
Year 2: Company shuts down
\`\`\``,
          keyPoints: [
            "Segment, Amazon Prime Video, and Etsy moved back to monoliths",
            "Even Kubernetes creators recommend monoliths for most teams",
            "Premature decomposition is the #1 cause of failure",
            "The successful path: Monolith → Modular → Gradual extraction"
          ]
        }
      ],
      codeExample: {
        title: "Modular Monolith Structure Example",
        language: "typescript",
        filename: "modular-monolith/src/modules/orders/index.ts",
        code: `// ============================================
// MODULAR MONOLITH: Example Structure
// ============================================
// This shows how to organize a monolith with clear
// module boundaries - ready for future extraction

// Project Structure:
// src/
// ├── modules/
// │   ├── users/
// │   │   ├── index.ts           ← Public API only
// │   │   ├── users.module.ts
// │   │   ├── entities/
// │   │   ├── services/
// │   │   └── repositories/
// │   ├── orders/
// │   │   ├── index.ts           ← Public API only
// │   │   ├── orders.module.ts
// │   │   ├── entities/
// │   │   ├── services/
// │   │   └── repositories/
// │   └── products/
// │       └── ...
// └── shared/
//     └── kernel/                ← Shared utilities only

// ============================================
// FILE: modules/users/index.ts
// This is the ONLY file other modules can import!
// ============================================

// Public types
export interface User {
  id: string;
  email: string;
  name: string;
}

// Public API - other modules use ONLY these
export class UsersAPI {
  constructor(private usersService: UsersService) {}

  async getUser(id: string): Promise<User | null> {
    return this.usersService.findById(id);
  }

  async getUsersByIds(ids: string[]): Promise<User[]> {
    return this.usersService.findByIds(ids);
  }

  async validateUser(email: string, password: string): Promise<User | null> {
    return this.usersService.validateCredentials(email, password);
  }
}

// ============================================
// FILE: modules/orders/services/orders.service.ts
// Notice: Uses UsersAPI, NOT direct imports
// ============================================

import { UsersAPI } from '../../users';  // ✅ Public API only

export class OrdersService {
  constructor(
    private ordersRepo: OrdersRepository,
    private usersAPI: UsersAPI,  // Injected dependency
  ) {}

  async createOrder(userId: string, items: OrderItem[]) {
    // Get user through PUBLIC API, not direct DB access
    const user = await this.usersAPI.getUser(userId);
    if (!user) throw new Error('User not found');

    const order = await this.ordersRepo.create({
      userId,
      userEmail: user.email,  // Denormalize what we need
      userName: user.name,
      items,
      status: 'pending',
    });

    return order;
  }
}

// ============================================
// RULES FOR MODULAR MONOLITH:
// ============================================
//
// 1. Only import from other modules' index.ts
//    ❌ import { UserRepository } from '../users/repositories/...'
//    ✅ import { UsersAPI } from '../users'
//
// 2. Each module owns its database tables
//    - Users module → users, sessions tables
//    - Orders module → orders, order_items tables
//    - No direct cross-module queries!
//
// 3. Async communication for non-critical flows
//    - Order created → Emit event
//    - Email module → Listens and sends email
//
// 4. Shared kernel for truly shared code only
//    - Utilities (dates, validation)
//    - Base classes
//    - NOT business logic
//
// WHEN READY TO EXTRACT TO MICROSERVICE:
// ────────────────────────────────────────
// 1. Module already has clean public API ✓
// 2. Module owns its data ✓
// 3. Just need to:
//    - Create separate repo
//    - Replace function calls with HTTP/gRPC
//    - Add message queue for events
//
// The module structure BECOMES the microservice!
// ============================================`
      },
      nextSteps: `Now that you understand WHEN to use microservices (and when not to), you're ready to learn the fundamentals. The next module covers what microservices actually are and how they differ from monoliths.

**But remember:** If you scored low on the decision framework, strongly consider building a Modular Monolith instead. You can always come back to microservices later.`
    }
  },
  {
    number: 1,
    slug: "introduction",
    title: "Introduction to Microservices",
    description: "Understand the fundamentals of microservices architecture, when to use it, and how it compares to monolithic applications.",
    difficulty: "beginner",
    topics: ["What are Microservices", "Monolith vs Microservices", "Benefits & Challenges", "When to Use", "Real-world Examples"],
    prerequisites: ["None required"],
    learningOutcomes: [
      "Explain what microservices are and why they matter",
      "Differentiate microservices from monolithic apps",
      "Identify benefits and common challenges",
      "Recognize real-world scenarios where microservices fit"
    ],
    estimatedTime: "15–25 minutes",
    content: {
      intro: `Welcome to your microservices journey! 🚀

In this module, you'll learn the fundamental concepts that form the foundation of modern distributed systems. By the end, you'll understand exactly what microservices are, why companies like Netflix, Amazon, and Uber use them, and most importantly - when YOU should (and shouldn't) use this architecture.

**What you'll learn:**
- The core philosophy behind microservices
- Key differences from traditional monolithic applications 
- Real-world scenarios where microservices shine
- Common pitfalls to avoid`,
      sections: [
        {
          title: "What are Microservices?",
          content: `Imagine you're building a large e-commerce platform. In the traditional approach (monolith), you'd build ONE big application that handles everything - user accounts, product catalog, shopping cart, payments, shipping, and notifications. All these features live in a single codebase and get deployed together.

**Microservices take a different approach.**

Instead of one giant application, you break it down into small, independent services:

🔹 **User Service** - Handles registration, login, and profiles
🔹 **Product Service** - Manages the product catalog and inventory
🔹 **Cart Service** - Handles shopping cart operations
🔹 **Payment Service** - Processes payments securely
🔹 **Notification Service** - Sends emails and push notifications

Each service is like a mini-application that:
- Has its own codebase
- Can be deployed independently
- Communicates with other services via APIs
- Can use different programming languages or databases

**Think of it like a restaurant:**
- Monolith = One chef does everything (cooking, serving, billing)
- Microservices = Specialized staff (chef, waiter, cashier) each doing their job well`,
        keyPoints: [
          "Each service focuses on ONE business function (Single Responsibility)",
          "Services communicate via APIs (usually REST or message queues)",
            "Each service can be scaled independently based on demand",
            "Teams can work on different services without stepping on each other's toes",
            "A failure in one service doesn't necessarily crash the entire system"
          ]
        },
        {
          title: "Monolith vs Microservices: A Detailed Comparison",
          content: `Let's dive deep into the differences between these two architectural styles. Understanding this comparison will help you make informed decisions for your projects.

**Monolithic Architecture:**

In a monolith, all your code lives together. When you deploy, everything goes live at once. If you need to change the payment logic, you redeploy the entire application.

\`\`\`
┌─────────────────────────────────────────┐
│           MONOLITHIC APP                │
│                                         │
│  ┌─────────┐ ┌──────────┐ ┌─────────┐  │
│  │  User   │ │ Product  │ │  Cart   │  │
│  │ Module  │ │  Module  │ │ Module  │  │
│  └─────────┘ └──────────┘ └─────────┘  │
│                                         │
│  ┌─────────┐ ┌──────────┐ ┌─────────┐  │
│  │ Payment │ │ Shipping │ │  Admin  │  │
│  │ Module  │ │  Module  │ │ Module  │  │
│  └─────────┘ └──────────┘ └─────────┘  │
│                                         │
│         ┌─────────────────┐            │
│         │  ONE DATABASE   │            │
│         └─────────────────┘            │
└─────────────────────────────────────────┘
\`\`\`

**Microservices Architecture:**

Each service is independent with its own database and deployment pipeline.

\`\`\`
┌──────────┐    ┌──────────┐    ┌──────────┐
│   User   │    │ Product  │    │   Cart   │
│ Service  │◄──►│ Service  │◄──►│ Service  │
└────┬─────┘    └────┬─────┘    └────┬─────┘
     │               │               │
┌────┴─────┐    ┌────┴─────┐    ┌────┴─────┐
│ Postgres │    │ MongoDB  │    │  Redis   │
└──────────┘    └──────────┘    └──────────┘
\`\`\``,
          comparison: {
            monolith: {
              pros: ["Simple to develop initially - everything in one place", "Easy to test end-to-end before deployment", "Simple deployment - just one application to deploy", "Low latency between modules (no network calls)"],
              cons: ["Gets harder to maintain as codebase grows (spaghetti code)", "Stuck with one technology stack for everything", "Scaling means scaling the ENTIRE app, even if only one part needs it", "One bug can bring down the entire application"]
            },
            microservices: {
              pros: ["Each service can be scaled independently (save costs)", "Teams can use the best technology for each service", "Faster deployments - change one service without touching others", "A crash in one service doesn't kill everything"],
              cons: ["More complex to set up and manage initially", "Network communication adds latency", "Debugging across services is challenging", "Requires DevOps expertise (Docker, Kubernetes, etc.)"]
            }
          }
        },
        {
          title: "When Should You Use Microservices?",
          content: `This is the most important question. Microservices are NOT always the right choice. Let me give you clear guidelines:

**✅ USE Microservices when:**

1. **Your team is growing** - If you have 10+ developers, they can work on separate services without conflicts.

2. **Different parts need different scaling** - Example: Your product catalog gets 100x more traffic than your admin panel. No point scaling both together.

3. **You need technology flexibility** - Maybe Python is best for your ML recommendation engine, but Node.js is perfect for real-time chat.

4. **You're building for the long term** - If you expect the system to grow for years, investing in microservices pays off.

5. **High availability is critical** - Banks, health systems, e-commerce - where downtime means losing money or lives.

**❌ DON'T USE Microservices when:**

1. **It's a small project or MVP** - You're just adding complexity. Build a monolith first, split later if needed.

2. **Your team is small (< 5 people)** - You'll spend more time on infrastructure than building features.

3. **You don't have DevOps expertise** - Without knowledge of Docker, Kubernetes, and CI/CD, you'll struggle.

4. **The domain isn't clearly separable** - If services need to constantly share data, you'll create a "distributed monolith".

**🤔 Real-world example:**

Amazon started as a monolith in 2002. Only after they understood their domain AND grew to hundreds of developers did they switch to microservices. They didn't start with it!`,
          keyPoints: [
            "Start with a monolith if you're unsure - you can always split later",
            "Microservices solve organizational problems, not just technical ones",
            "The overhead of microservices only pays off at scale",
            "Don't let hype drive your architecture decisions",
            "Netflix has 1000+ microservices, but they also have 1000+ engineers"
          ]
        }
      ],
      codeExample: {
        title: "Microservices Architecture in Practice",
        language: "text",
        filename: "architecture-overview.txt",
        code: `EXAMPLE: E-commerce Platform Architecture
==========================================

                    ┌─────────────────┐
     Internet ────► │   API Gateway   │ ◄─── Authentication
                    │  (Entry Point)  │      Rate Limiting
                    └────────┬────────┘      Logging
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│    USER      │    │   PRODUCT    │    │    ORDER     │
│   SERVICE    │    │   SERVICE    │    │   SERVICE    │
│              │    │              │    │              │
│ • Sign up    │    │ • Catalog    │    │ • Create     │
│ • Login      │    │ • Search     │    │ • Track      │
│ • Profile    │    │ • Inventory  │    │ • Cancel     │
│ • Passwords  │    │ • Categories │    │ • History    │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  PostgreSQL  │    │   MongoDB    │    │   MongoDB    │
│  (Relational │    │  (Flexible   │    │  (Order      │
│   user data) │    │   product    │    │   documents) │
│              │    │   schemas)   │    │              │
└──────────────┘    └──────────────┘    └──────────────┘

         ┌─────────────────────────────────┐
         │        MESSAGE QUEUE            │
         │        (RabbitMQ/Kafka)         │
         │                                 │
         │  Events: order_created,         │
         │  payment_completed,             │
         │  inventory_updated              │
         └─────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   PAYMENT    │  │ NOTIFICATION │  │  SHIPPING    │
│   SERVICE    │  │   SERVICE    │  │   SERVICE    │
└──────────────┘  └──────────────┘  └──────────────┘

KEY POINTS:
-----------
1. Each service has its OWN database (no sharing!)
2. Services communicate via REST APIs or message queues
3. The API Gateway is the single entry point for clients
4. Events keep services loosely coupled`
      },
      nextSteps: `In the next module, you'll learn NestJS - our framework of choice for building microservices. NestJS provides excellent built-in support for microservices patterns.`
    }
  },
  {
    number: 2,
    slug: "nestjs-fundamentals",
    title: "NestJS Fundamentals",
    description: "Learn NestJS, a progressive Node.js framework for building efficient and scalable server-side applications.",
    difficulty: "beginner",
    topics: ["Installation", "Modules", "Controllers", "Providers", "Dependency Injection", "Decorators"],
    prerequisites: ["Basic JavaScript/TypeScript knowledge", "Node.js installed"],
    learningOutcomes: [
      "Explain NestJS core concepts (modules, controllers, providers)",
      "Understand dependency injection and decorators",
      "Create and structure a NestJS project",
      "Wire REST endpoints and services"
    ],
    estimatedTime: "40–60 minutes",
    content: {
      intro: `Now that you understand what microservices are, let's learn the tool we'll use to build them - **NestJS**.

**Why NestJS for Microservices?**

NestJS is a Node.js framework that:
- Has **first-class microservices support** built-in
- Uses **TypeScript** for better code quality (but works with JavaScript too)
- Follows a **modular architecture** perfect for microservices
- Provides built-in support for REST, GraphQL, WebSockets, and more
- Has a massive ecosystem and active community

By the end of this module, you'll understand the core building blocks of NestJS and be ready to create your first service.`,
      sections: [
        {
          title: "Setting Up Your First NestJS Project",
          content: `Let's get your development environment ready. We'll install NestJS and create a new project step by step.

**Step 1: Prerequisites**

Make sure you have Node.js installed (version 16 or higher):
\`\`\`bash
node --version  # Should show v16.x or higher
npm --version   # Should show 8.x or higher
\`\`\`

**Step 2: Install the NestJS CLI**

The NestJS CLI helps you create and manage projects:
\`\`\`bash
npm install -g @nestjs/cli
\`\`\`

**Step 3: Create a New Project**

\`\`\`bash
nest new user-service
\`\`\`

Choose npm when asked. This creates a new project with this structure:

\`\`\`
user-service/
├── src/
│   ├── app.controller.ts    # Handles HTTP requests
│   ├── app.module.ts        # Main application module
│   ├── app.service.ts       # Business logic
│   └── main.ts              # Entry point
├── test/                    # Test files
├── package.json
└── tsconfig.json
\`\`\`

**Step 4: Start the Development Server**

\`\`\`bash
cd user-service
npm run start:dev
\`\`\`

Visit http://localhost:3000 - you should see "Hello World!"`,
          keyPoints: [
            "The CLI generates a complete project structure for you",
            "Hot-reload is enabled in dev mode - changes apply instantly",
            "The src/ folder contains all your application code",
            "Entry point is main.ts which bootstraps the application"
          ]
        },
        {
          title: "Understanding Modules: Organizing Your Code",
          content: `**Modules** are the core organizational unit in NestJS. Think of them as self-contained features of your application.

**Why Modules Matter:**

Imagine you're building a user service. You might have:
- Authentication features (login, logout)
- Profile features (update profile, upload avatar)
- Admin features (manage users)

Instead of dumping everything in one place, you create separate modules:

\`\`\`
src/
├── auth/
│   ├── auth.module.ts
│   ├── auth.controller.ts
│   └── auth.service.ts
├── profile/
│   ├── profile.module.ts
│   ├── profile.controller.ts
│   └── profile.service.ts
└── admin/
    ├── admin.module.ts
    └── ...
\`\`\`

**Creating a Module:**

Every module is a class decorated with \`@Module()\`:`,
          keyPoints: [
            "Modules group related functionality together",
            "Each feature of your app should have its own module",
            "Modules can import other modules to share functionality",
            "The root module (AppModule) bootstraps your application"
          ]
        },
        {
          title: "Controllers: Handling HTTP Requests",
          content: `**Controllers** are responsible for handling incoming requests and returning responses. They're like the receptionists of your application - they receive requests, talk to the right people (services), and give back answers.

**How Controllers Work:**

When a user visits \`/users/123\`, the controller:
1. Receives the request
2. Extracts the user ID (123)
3. Calls the service to get user data
4. Returns the response

**Key Decorators:**

- \`@Controller('users')\` - Defines the base route (/users)
- \`@Get()\` - Handles GET requests
- \`@Post()\` - Handles POST requests
- \`@Param('id')\` - Extracts route parameters
- \`@Body()\` - Extracts request body`,
          keyPoints: [
            "Controllers should be thin - only handle HTTP logic",
            "Business logic belongs in services, not controllers",
            "Each route method handles one specific endpoint",
            "Decorators make routes declarative and readable"
          ]
        },
        {
          title: "Services: Where the Business Logic Lives",
          content: `**Services** (also called Providers) contain the actual business logic of your application. While controllers handle HTTP stuff, services do the real work.

**The Philosophy:**

- Controllers answer: "What endpoint is being called?"
- Services answer: "What should we actually DO?"

**Example Flow:**

1. User sends POST /users with { name: "John" }
2. Controller receives request, extracts body
3. Controller calls \`usersService.create(userData)\`
4. Service validates data, saves to database, returns result
5. Controller sends response back to user

**Dependency Injection:**

NestJS automatically creates and manages service instances. You just declare what you need in the constructor:

\`\`\`javascript
class UsersController {
  constructor(private usersService: UsersService) {
    // NestJS automatically injects the UsersService!
  }
}
\`\`\`

This is called **Dependency Injection** - you declare dependencies, NestJS provides them.`,
          keyPoints: [
            "Services are marked with @Injectable() decorator",
            "NestJS handles creating and injecting service instances",
            "Services can be shared across multiple controllers",
            "Keep controllers thin, services fat with logic"
          ]
        }
      ],
      codeExample: {
        title: "Complete Module Example: Users Feature",
        language: "typescript",
        filename: "src/users/users.module.ts",
        code: `// ============================================
// FILE: src/users/users.module.ts
// PURPOSE: Defines the Users feature module
// ============================================

import { Module } from '@nestjs/common';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';

@Module({
  controllers: [UsersController],  // Handles HTTP requests
  providers: [UsersService],       // Contains business logic
  exports: [UsersService],         // Makes service available to other modules
})
export class UsersModule {}


// ============================================
// FILE: src/users/users.service.ts
// PURPOSE: Contains all user-related business logic
// ============================================

import { Injectable, NotFoundException } from '@nestjs/common';

// Define what a user looks like
interface User {
  id: number;
  name: string;
  email: string;
  createdAt: Date;
}

@Injectable()  // This marks it as a provider that can be injected
export class UsersService {
  // In-memory database (replace with real DB later)
  private users: User[] = [];
  private idCounter = 1;

  // Get all users
  findAll(): User[] {
    return this.users;
  }

  // Find one user by ID
  findOne(id: number): User {
    const user = this.users.find(u => u.id === id);
    if (!user) {
      throw new NotFoundException(\`User with ID \${id} not found\`);
    }
    return user;
  }

  // Create a new user
  create(name: string, email: string): User {
    const newUser: User = {
      id: this.idCounter++,
      name,
      email,
      createdAt: new Date(),
    };
    this.users.push(newUser);
    return newUser;
  }

  // Delete a user
  remove(id: number): boolean {
    const index = this.users.findIndex(u => u.id === id);
    if (index === -1) {
      throw new NotFoundException(\`User with ID \${id} not found\`);
    }
    this.users.splice(index, 1);
    return true;
  }
}


// ============================================
// FILE: src/users/users.controller.ts
// PURPOSE: Handles HTTP requests for /users endpoints
// ============================================

import { Controller, Get, Post, Delete, Param, Body } from '@nestjs/common';
import { UsersService } from './users.service';

@Controller('users')  // All routes start with /users
export class UsersController {
  // NestJS automatically injects the UsersService
  constructor(private readonly usersService: UsersService) {}

  // GET /users - Get all users
  @Get()
  getAllUsers() {
    return this.usersService.findAll();
  }

  // GET /users/5 - Get user with ID 5
  @Get(':id')
  getUser(@Param('id') id: string) {
    return this.usersService.findOne(parseInt(id));
  }

  // POST /users - Create a new user
  // Body: { "name": "John", "email": "john@test.com" }
  @Post()
  createUser(@Body() body: { name: string; email: string }) {
    return this.usersService.create(body.name, body.email);
  }

  // DELETE /users/5 - Delete user with ID 5
  @Delete(':id')
  deleteUser(@Param('id') id: string) {
    return this.usersService.remove(parseInt(id));
  }
}


// ============================================
// HOW TO TEST WITH CURL:
// ============================================
// 
// Create a user:
// curl -X POST http://localhost:3000/users \\
//   -H "Content-Type: application/json" \\
//   -d '{"name":"John Doe","email":"john@example.com"}'
//
// Get all users:
// curl http://localhost:3000/users
//
// Get specific user:
// curl http://localhost:3000/users/1
//
// Delete user:
// curl -X DELETE http://localhost:3000/users/1`
      },
      nextSteps: `Excellent! You now understand NestJS fundamentals. Next, we'll learn about distributed systems fundamentals - the theory you MUST understand before building microservices.`
    }
  },
  // ============================================
  // MODULE 3: DISTRIBUTED SYSTEMS FUNDAMENTALS
  // Critical theory for understanding microservices
  // ============================================
  {
    number: 3,
    slug: "distributed-systems",
    title: "Distributed Systems Fundamentals",
    description: "Learn the critical theory behind distributed systems: CAP theorem, consistency models, the 8 fallacies, and why networks fail.",
    difficulty: "beginner",
    topics: ["8 Fallacies", "CAP Theorem", "Consistency Models", "Idempotency", "Network Partitions", "Message Delivery"],
    prerequisites: ["Introduction to Microservices"],
    isRequired: true,
    learningOutcomes: [
      "Explain the 8 Fallacies of Distributed Computing",
      "Apply CAP theorem to architecture decisions",
      "Differentiate between consistency models",
      "Design idempotent operations",
      "Handle network failures gracefully"
    ],
    estimatedTime: "45–60 minutes",
    content: {
      intro: `**Microservices ARE distributed systems.** 

Before you write a single line of microservices code, you MUST understand what that means. This module covers the theory that separates working microservices from disaster.

**Why This Module Matters:**

Most microservices failures happen because developers treat network calls like function calls. They're not. Networks fail, messages get lost, clocks drift, and timeouts happen.

**You'll learn:**
- Why your assumptions about networks are wrong
- What happens when you can't have it all (CAP theorem)
- How to design operations that survive failures
- The difference between consistency models`,
      sections: [
        {
          title: "The 8 Fallacies of Distributed Computing",
          content: `In 1994, Peter Deutsch (and later James Gosling) identified 8 false assumptions that developers make about distributed systems. **Every single one will bite you.**

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│            THE 8 FALLACIES OF DISTRIBUTED COMPUTING             │
│                                                                  │
│  These are things developers ASSUME are true, but ARE NOT:      │
│                                                                  │
│  1. The network is reliable                                     │
│     → Packets get dropped. Connections break. Timeouts happen.  │
│                                                                  │
│  2. Latency is zero                                             │
│     → Network calls add 1-100ms+. This adds up FAST.            │
│                                                                  │
│  3. Bandwidth is infinite                                       │
│     → Large payloads slow everything down.                      │
│                                                                  │
│  4. The network is secure                                       │
│     → Traffic can be intercepted, spoofed, or manipulated.      │
│                                                                  │
│  5. Topology doesn't change                                     │
│     → Servers come and go. IPs change. Routes change.           │
│                                                                  │
│  6. There is one administrator                                  │
│     → Multiple teams, multiple policies, multiple failures.     │
│                                                                  │
│  7. Transport cost is zero                                      │
│     → Serialization, network transfer, deserialization = cost.  │
│                                                                  │
│  8. The network is homogeneous                                  │
│     → Different services, protocols, versions, languages.       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**Real-World Impact:**

\`\`\`typescript
// Code that IGNORES the fallacies (will fail in production):
async function placeOrder(order) {
  const user = await userService.getUser(order.userId);      // What if this times out?
  const stock = await inventoryService.check(order.items);   // What if inventory is wrong?
  const payment = await paymentService.charge(order.total);  // What if this succeeds but we never get the response?
  const shipment = await shippingService.create(order);      // What if shipping is down?
  return { success: true };  // Is it really successful?
}

// Code that RESPECTS the fallacies:
async function placeOrder(order) {
  const user = await userService.getUser(order.userId)
    .timeout(5000)                      // Fallacy 1 & 2: Network fails, latency exists
    .retry(3)                           // Retry transient failures
    .fallback(cachedUser);              // Use cache if service is down
    
  // ... more defensive code
}
\`\`\``,
          keyPoints: [
            "The network WILL fail. Design for it.",
            "Every network call adds latency. Minimize them.",
            "Services go up and down. Don't assume availability.",
            "Always have timeouts, retries, and fallbacks"
          ]
        },
        {
          title: "CAP Theorem: You Can't Have Everything",
          content: `**CAP Theorem** states that a distributed system can only guarantee TWO of these three properties:

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│                      CAP THEOREM                                 │
│                                                                  │
│                     CONSISTENCY (C)                              │
│                    /             \\                               │
│                   /               \\                              │
│                  /                 \\                             │
│                 /   You can only    \\                            │
│                /    pick 2 of 3!     \\                           │
│               /                       \\                          │
│      AVAILABILITY (A) ─────────── PARTITION                     │
│                                  TOLERANCE (P)                   │
│                                                                  │
│  C - Consistency:     Every read returns the most recent write  │
│  A - Availability:    Every request gets a response             │
│  P - Partition        System works even when network fails      │
│      Tolerance:       between nodes                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**The Reality: You MUST Choose P**

Network partitions WILL happen. You can't prevent them. So your real choice is:

**CP (Consistency + Partition Tolerance):**
- When partition occurs, system becomes unavailable for writes
- Returns errors rather than stale data
- **Example:** Banking systems, inventory counts

**AP (Availability + Partition Tolerance):**
- When partition occurs, system stays available
- Might return stale/inconsistent data
- **Example:** Social media feeds, shopping carts

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│                  CP vs AP DECISION                               │
│                                                                  │
│  Scenario: Network partition between Service A and Service B    │
│                                                                  │
│  CP SYSTEM (Choose Consistency):                                │
│  ─────────────────────────────                                  │
│  Client: "GET /balance"                                         │
│  System: "Sorry, cannot verify latest balance. Try later."     │
│  → User annoyed but no incorrect data                           │
│                                                                  │
│  AP SYSTEM (Choose Availability):                               │
│  ─────────────────────────────                                  │
│  Client: "GET /balance"                                         │
│  System: "$1000" (might be stale)                               │
│  → User gets a response but might be outdated                   │
│                                                                  │
│  WHICH TO CHOOSE?                                               │
│  ────────────────                                               │
│  • Money/inventory → CP (correctness critical)                  │
│  • Social posts/recommendations → AP (availability preferred)   │
│  • Shopping cart → AP (can reconcile later)                     │
│  • Payment processing → CP (must be correct)                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
\`\`\``,
          keyPoints: [
            "CAP theorem = pick 2 of 3 (really: pick C or A, P is mandatory)",
            "CP = Consistent but might be unavailable during partitions",
            "AP = Available but might return stale data during partitions",
            "Different parts of your system can make different choices"
          ]
        },
        {
          title: "Consistency Models: Strong vs Eventual",
          content: `Not all consistency is equal. You have options on a spectrum:

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│                  CONSISTENCY SPECTRUM                            │
│                                                                  │
│  STRONG                                        EVENTUAL          │
│  CONSISTENCY ◄────────────────────────────────► CONSISTENCY     │
│                                                                  │
│  ├─────────┼─────────┼─────────┼─────────┼─────────┤           │
│  │         │         │         │         │         │           │
│  │ Linear- │ Serial- │ Causal  │  Read   │ Eventual│           │
│  │ izable  │ izable  │         │  Your   │         │           │
│  │         │         │         │  Writes │         │           │
│  │         │         │         │         │         │           │
│  │ Slowest │         │         │         │ Fastest │           │
│  │ Safest  │         │         │         │ Riskiest│           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**Strong Consistency:**
- Every read returns the most recent write
- All nodes see the same data at the same time
- Requires coordination (slow)
- Example: Traditional SQL databases

**Eventual Consistency:**
- Reads might return stale data temporarily
- Eventually, all nodes converge to the same state
- No coordination needed (fast)
- Example: DNS, social media feeds, search indexes

**Practical Example:**

\`\`\`
STRONG CONSISTENCY (Bank Balance):
────────────────────────────────
Time 0: Balance = $100
Time 1: Withdraw $50 (from ATM in NYC)
Time 2: Check balance (from phone in LA)
→ Must show $50 (latest value)

EVENTUAL CONSISTENCY (Twitter Follower Count):
─────────────────────────────────────────────
Time 0: Followers = 1000
Time 1: New follower (server in Europe)
Time 2: Check followers (server in Asia)
→ Might show 1000 or 1001 (eventually correct)
→ Nobody cares if it's briefly wrong!
\`\`\`

**Key Insight:** Most data doesn't need strong consistency. Ask yourself: "What's the worst that happens if this data is a few seconds stale?"`,
          keyPoints: [
            "Strong consistency = slow but always correct",
            "Eventual consistency = fast but temporarily stale",
            "Most data can tolerate eventual consistency",
            "Different data in same system can have different consistency"
          ]
        },
        {
          title: "Idempotency: Your Best Defense",
          content: `**An operation is idempotent if doing it multiple times has the same effect as doing it once.**

**Why This Matters:**

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│           WHY YOU NEED IDEMPOTENCY                               │
│                                                                  │
│  The Scenario:                                                  │
│  ─────────────                                                  │
│  1. Client sends "Charge $100" to Payment Service               │
│  2. Payment Service processes the charge                        │
│  3. Response gets lost in the network! 📡❌                      │
│  4. Client thinks it failed, RETRIES                            │
│  5. Payment Service receives same request again                 │
│                                                                  │
│  WITHOUT Idempotency:                                           │
│  → Customer charged $200! 😱                                    │
│                                                                  │
│  WITH Idempotency:                                              │
│  → Second request recognized as duplicate                       │
│  → Customer charged $100 ✅                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**How to Implement Idempotency:**

**Method 1: Idempotency Keys**
\`\`\`typescript
// Client generates unique key for each logical operation
POST /payments
{
  "idempotency_key": "order_123_payment_attempt_1",  // Unique!
  "amount": 100,
  "customer_id": "cust_456"
}

// Server implementation:
async function processPayment(request) {
  // Check if we've seen this key before
  const existing = await db.idempotencyKeys.find(request.idempotency_key);
  
  if (existing) {
    // Already processed! Return the previous result.
    return existing.result;
  }
  
  // First time - process the payment
  const result = await chargeCustomer(request);
  
  // Store the result with the key
  await db.idempotencyKeys.save({
    key: request.idempotency_key,
    result: result,
    expiresAt: Date.now() + 24 * 60 * 60 * 1000  // Keep for 24h
  });
  
  return result;
}
\`\`\`

**Method 2: Natural Idempotency**
\`\`\`typescript
// ❌ NOT idempotent - each call adds $10
POST /accounts/123/add-funds { amount: 10 }

// ✅ Idempotent - sets absolute value
PUT /accounts/123/balance { balance: 110 }

// ✅ Idempotent - references specific transaction
POST /accounts/123/transactions/txn_789 { amount: 10 }
\`\`\`

**Common Idempotent Patterns:**

| HTTP Method | Idempotent? | Example |
|-------------|-------------|---------|
| GET | ✅ Yes | Retrieving data |
| PUT | ✅ Yes | Update to specific value |
| DELETE | ✅ Yes | Delete specific resource |
| POST | ❌ No | Must add idempotency key |`,
          keyPoints: [
            "Networks fail and retries happen - plan for duplicates",
            "Every write operation should be idempotent",
            "Use idempotency keys for POST operations",
            "Store and check keys before processing"
          ]
        },
        {
          title: "Message Delivery Guarantees",
          content: `When services communicate via messages, how many times is a message delivered?

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│              MESSAGE DELIVERY GUARANTEES                         │
│                                                                  │
│  AT-MOST-ONCE                                                   │
│  ─────────────                                                  │
│  • Message sent once, no retries                                │
│  • Might be lost (0 or 1 delivery)                              │
│  • Fast but unreliable                                          │
│  • Use for: Metrics, logs (where loss is acceptable)            │
│                                                                  │
│  AT-LEAST-ONCE                                                  │
│  ─────────────                                                  │
│  • Retry until acknowledged                                     │
│  • Never lost, but might duplicate (1 or more deliveries)       │
│  • Consumer MUST be idempotent                                  │
│  • Use for: Most business events                                │
│                                                                  │
│  EXACTLY-ONCE                                                   │
│  ────────────                                                   │
│  • Message delivered exactly once                               │
│  • THE HOLY GRAIL (very hard to achieve)                        │
│  • Usually approximated with at-least-once + idempotency        │
│  • Use for: Financial transactions (with idempotency)           │
│                                                                  │
│  ═══════════════════════════════════════════════════════════   │
│                                                                  │
│  THE TRUTH ABOUT "EXACTLY-ONCE":                                │
│  ────────────────────────────────                               │
│  True exactly-once is nearly impossible in distributed systems. │
│  What systems actually do:                                      │
│                                                                  │
│  "Exactly-once" = At-least-once delivery                        │
│                 + Idempotent consumer                           │
│                 = Exactly-once PROCESSING                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**Practical Implementation:**

\`\`\`typescript
// Consumer that handles at-least-once delivery
@EventPattern('order_created')
async handleOrderCreated(event: OrderCreatedEvent) {
  // STEP 1: Check if already processed (idempotency)
  const processed = await this.db.processedEvents.exists(event.id);
  if (processed) {
    console.log(\`Event \${event.id} already processed, skipping\`);
    return; // Duplicate - ignore
  }
  
  // STEP 2: Process the event
  await this.processOrder(event);
  
  // STEP 3: Mark as processed
  await this.db.processedEvents.save({
    eventId: event.id,
    processedAt: new Date()
  });
}
\`\`\``,
          keyPoints: [
            "At-most-once: Might lose messages",
            "At-least-once: Might duplicate messages (use idempotency)",
            "Exactly-once: Really means at-least-once + idempotent consumers",
            "Always design consumers to handle duplicates"
          ]
        },
        {
          title: "Time is an Illusion (Clock Skew)",
          content: `**Clocks on different machines are NOT synchronized.**

This seems minor until you try to order events across services:

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│                  CLOCK SKEW PROBLEM                              │
│                                                                  │
│  Server A (Clock: 10:00:00.000)                                 │
│  Server B (Clock: 10:00:00.150)  ← 150ms ahead!                 │
│                                                                  │
│  Sequence of events:                                            │
│  ──────────────────                                             │
│  1. User updates profile on Server A at 10:00:00.100            │
│  2. User updates profile on Server B at 10:00:00.200            │
│                                                                  │
│  According to timestamps:                                       │
│  ─────────────────────────                                      │
│  Server A says: 10:00:00.100                                    │
│  Server B says: 10:00:00.350 (200 + 150 skew)                   │
│                                                                  │
│  Looks correct! But what if:                                    │
│  ────────────────────────────                                   │
│  1. User updates on Server A at 10:00:00.100                    │
│  2. User updates on Server B at 10:00:00.050 (50ms EARLIER)     │
│                                                                  │
│  According to timestamps:                                       │
│  ─────────────────────────                                      │
│  Server A says: 10:00:00.100                                    │
│  Server B says: 10:00:00.200 (50 + 150 skew)                    │
│                                                                  │
│  Server B's update (which happened FIRST) appears LATER!        │
│  Which update wins? 😱                                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**Solutions:**

1. **Use Logical Clocks (Lamport Timestamps)**
   - Increment counter on each event
   - Include counter in messages
   - Receiver updates its clock: max(local, received) + 1

2. **Use Vector Clocks**
   - Each node maintains a vector of counters
   - Can detect concurrent events

3. **Use a Centralized Sequence Generator**
   - Single source for ordering (but creates bottleneck)

4. **Accept Uncertainty**
   - Design system to handle out-of-order events
   - Use event content (not time) for conflict resolution

**Practical Advice:**

\`\`\`typescript
// ❌ Don't rely on timestamps for ordering
if (event.timestamp > lastEvent.timestamp) {
  // This can be wrong!
}

// ✅ Use sequence numbers or version vectors
if (event.sequenceNumber > lastEvent.sequenceNumber) {
  // This is reliable
}

// ✅ Or use content-based conflict resolution
function mergeProfiles(profile1, profile2) {
  // Merge based on business rules, not timestamps
  return {
    name: profile2.name,  // Last value wins
    email: profile1.email || profile2.email,  // First non-null wins
  };
}
\`\`\``,
          keyPoints: [
            "Server clocks can be seconds or minutes apart",
            "Never use wall-clock time for ordering distributed events",
            "Use logical clocks or sequence numbers instead",
            "Design conflict resolution based on business rules, not time"
          ]
        }
      ],
      codeExample: {
        title: "Idempotent Payment Service Implementation",
        language: "typescript",
        filename: "payment-service.ts",
        code: `// ============================================
// IDEMPOTENT PAYMENT SERVICE
// ============================================
// This service handles payments with proper idempotency,
// demonstrating distributed systems best practices.

interface PaymentRequest {
  idempotencyKey: string;    // Client-provided unique key
  customerId: string;
  amount: number;
  currency: string;
}

interface PaymentResult {
  transactionId: string;
  status: 'success' | 'failed' | 'pending';
  amount: number;
}

@Injectable()
export class PaymentService {
  constructor(
    private readonly db: Database,
    private readonly paymentGateway: PaymentGateway,
  ) {}

  async processPayment(request: PaymentRequest): Promise<PaymentResult> {
    // ════════════════════════════════════════════════════
    // STEP 1: Check for existing result (idempotency)
    // ════════════════════════════════════════════════════
    const existingResult = await this.db.idempotencyStore.findOne({
      key: request.idempotencyKey
    });

    if (existingResult) {
      console.log(\`[Idempotency] Request \${request.idempotencyKey} already processed\`);
      // Return the SAME result as before - no double charge!
      return existingResult.result;
    }

    // ════════════════════════════════════════════════════
    // STEP 2: Mark as "in progress" (prevent race conditions)
    // ════════════════════════════════════════════════════
    try {
      await this.db.idempotencyStore.insert({
        key: request.idempotencyKey,
        status: 'in_progress',
        createdAt: new Date(),
        // Use unique constraint on 'key' to prevent duplicates
      });
    } catch (error) {
      if (error.code === 'DUPLICATE_KEY') {
        // Another request with same key is in progress
        // Wait and retry to get the result
        return this.waitForResult(request.idempotencyKey);
      }
      throw error;
    }

    // ════════════════════════════════════════════════════
    // STEP 3: Process the payment
    // ════════════════════════════════════════════════════
    let result: PaymentResult;
    
    try {
      // Call external payment gateway
      const gatewayResponse = await this.paymentGateway.charge({
        amount: request.amount,
        currency: request.currency,
        customerId: request.customerId,
        // Pass idempotency key to gateway too!
        idempotencyKey: request.idempotencyKey,
      });

      result = {
        transactionId: gatewayResponse.id,
        status: 'success',
        amount: request.amount,
      };
    } catch (error) {
      result = {
        transactionId: null,
        status: 'failed',
        amount: 0,
      };
    }

    // ════════════════════════════════════════════════════
    // STEP 4: Store the result (for future duplicate requests)
    // ════════════════════════════════════════════════════
    await this.db.idempotencyStore.update(
      { key: request.idempotencyKey },
      { 
        status: 'completed',
        result: result,
        completedAt: new Date()
      }
    );

    return result;
  }

  private async waitForResult(key: string, maxRetries = 10): Promise<PaymentResult> {
    for (let i = 0; i < maxRetries; i++) {
      await sleep(100 * (i + 1)); // Exponential backoff
      
      const record = await this.db.idempotencyStore.findOne({ key });
      if (record?.status === 'completed') {
        return record.result;
      }
    }
    throw new Error('Timeout waiting for idempotent result');
  }
}

// ════════════════════════════════════════════════════
// CLIENT USAGE:
// ════════════════════════════════════════════════════
// 
// const idempotencyKey = \`order_\${orderId}_payment_\${Date.now()}\`;
// 
// // Even if this is called multiple times (due to retries),
// // the customer is only charged once!
// const result = await paymentService.processPayment({
//   idempotencyKey,
//   customerId: 'cust_123',
//   amount: 99.99,
//   currency: 'USD'
// });
// ════════════════════════════════════════════════════`
      },
      nextSteps: `You now understand the theory behind distributed systems. This knowledge will help you avoid the most common microservices pitfalls. Next, we'll learn how to define service boundaries using Domain-Driven Design.`
    }
  },
  // ============================================
  // MODULE 4: DOMAIN-DRIVEN DESIGN FOR SERVICE BOUNDARIES
  // The hardest part of microservices!
  // ============================================
  {
    number: 4,
    slug: "domain-driven-design",
    title: "Domain-Driven Design & Service Boundaries",
    description: "Learn how to define microservice boundaries using DDD. Master bounded contexts, aggregates, and avoid the distributed monolith.",
    difficulty: "intermediate",
    topics: ["Bounded Contexts", "Aggregates", "Context Mapping", "Event Storming", "Service Boundaries", "Data Ownership"],
    prerequisites: ["Distributed Systems Fundamentals"],
    isRequired: true,
    learningOutcomes: [
      "Define service boundaries using bounded contexts",
      "Identify aggregates and their boundaries",
      "Map relationships between contexts",
      "Avoid common boundary mistakes",
      "Apply Event Storming for discovery"
    ],
    estimatedTime: "60–90 minutes",
    content: {
      intro: `**This is the hardest and most important skill in microservices.**

Defining service boundaries incorrectly leads to the "Distributed Monolith" - a system with all the complexity of microservices and none of the benefits.

**Domain-Driven Design (DDD)** gives us the tools to find natural service boundaries based on business domains, not technical concerns.

**What You'll Learn:**
- How to identify bounded contexts (natural service boundaries)
- How to group related concepts into aggregates
- How to handle communication between contexts
- Common mistakes that lead to distributed monoliths`,
      sections: [
        {
          title: "The #1 Mistake: Wrong Service Boundaries",
          content: `**Most microservices projects fail because of wrong boundaries.**

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│        WRONG VS RIGHT SERVICE BOUNDARIES                         │
│                                                                  │
│  ❌ WRONG: Split by TECHNICAL LAYER                             │
│  ──────────────────────────────────                             │
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│  │   Auth      │ │  Database   │ │   API       │               │
│  │   Service   │ │   Service   │ │   Service   │               │
│  └─────────────┘ └─────────────┘ └─────────────┘               │
│                                                                  │
│  Problems:                                                      │
│  • Every feature requires ALL services                          │
│  • Can't deploy independently                                   │
│  • Tight coupling through shared data                           │
│  → This is a DISTRIBUTED MONOLITH                               │
│                                                                  │
│  ═══════════════════════════════════════════════════════════   │
│                                                                  │
│  ✅ RIGHT: Split by BUSINESS DOMAIN                             │
│  ─────────────────────────────────                              │
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│  │   Orders    │ │   Users     │ │  Inventory  │               │
│  │   Domain    │ │   Domain    │ │   Domain    │               │
│  │             │ │             │ │             │               │
│  │ • API       │ │ • API       │ │ • API       │               │
│  │ • Logic     │ │ • Logic     │ │ • Logic     │               │
│  │ • Database  │ │ • Database  │ │ • Database  │               │
│  └─────────────┘ └─────────────┘ └─────────────┘               │
│                                                                  │
│  Benefits:                                                      │
│  • Each service is a complete vertical slice                    │
│  • Can develop, deploy, scale independently                     │
│  • Clear ownership (one team per domain)                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**The Litmus Test:**

Can a team make most changes to their service WITHOUT coordinating with other teams?

- **YES** → Good boundaries ✅
- **NO** → You have a distributed monolith ❌`,
          keyPoints: [
            "Split by BUSINESS DOMAIN, not technical layer",
            "Each service should be a complete vertical slice",
            "If changes require multiple teams, boundaries are wrong",
            "A distributed monolith is worse than a real monolith"
          ]
        },
        {
          title: "Bounded Contexts: Natural Service Boundaries",
          content: `**A Bounded Context is a boundary within which a domain model is defined and consistent.**

Think of it as: "Within these walls, 'Customer' means THIS specific thing."

**Example: The word "Product" means different things:**

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│     SAME WORD, DIFFERENT MEANINGS IN DIFFERENT CONTEXTS         │
│                                                                  │
│  CATALOG Context:              INVENTORY Context:               │
│  ─────────────────             ────────────────────             │
│  Product {                     Product {                        │
│    id                            sku                            │
│    name                          warehouseLocation              │
│    description                   quantityOnHand                 │
│    images[]                      reorderPoint                   │
│    price                         lastCountDate                  │
│    categories[]                }                                │
│  }                                                              │
│                                                                  │
│  SHIPPING Context:             PRICING Context:                 │
│  ─────────────────             ───────────────────              │
│  Product {                     Product {                        │
│    sku                           sku                            │
│    weight                        basePrice                      │
│    dimensions                    discounts[]                    │
│    isFragile                     taxCategory                    │
│    shippingClass                 priceHistory[]                 │
│  }                             }                                │
│                                                                  │
│  ═══════════════════════════════════════════════════════════   │
│                                                                  │
│  Each bounded context has its OWN definition of "Product"!      │
│  This is GOOD - it reflects real business complexity.           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**Finding Bounded Contexts:**

1. **Listen to the language.** When different teams use the same word differently, you've found a boundary.

2. **Look for organizational boundaries.** Different departments often = different contexts.

3. **Find where data interpretations differ.** Same data, different meaning = different context.

**Bounded Context ≈ Microservice**

Each bounded context is a strong candidate for a microservice. The service owns:
- Its definition of domain terms
- Its data
- Its business rules`,
          keyPoints: [
            "Bounded Context = boundary where terms have consistent meaning",
            "Same word can mean different things in different contexts",
            "Each bounded context is a candidate for a microservice",
            "Listen to how different teams describe the same concepts"
          ]
        },
        {
          title: "Aggregates: Consistency Boundaries",
          content: `**An Aggregate is a cluster of domain objects treated as a single unit for data changes.**

**Why Aggregates Matter:**

In distributed systems, you can't have transactions across services. Aggregates define what CAN be transactionally consistent.

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│                     AGGREGATE EXAMPLE: ORDER                     │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │                    ORDER AGGREGATE                      │     │
│  │                    (Consistency Boundary)               │     │
│  │                                                         │     │
│  │   ┌──────────────────────────────────────────────┐    │     │
│  │   │              Order (Root)                     │    │     │
│  │   │   • orderId                                   │    │     │
│  │   │   • status                                    │    │     │
│  │   │   • customerId (reference, not object)       │    │     │
│  │   │   • totalAmount                              │    │     │
│  │   └────────────────────┬─────────────────────────┘    │     │
│  │                        │                               │     │
│  │                        │ contains                      │     │
│  │                        ▼                               │     │
│  │   ┌──────────────────────────────────────────────┐    │     │
│  │   │           OrderLineItem[]                     │    │     │
│  │   │   • productId (reference, not object)        │    │     │
│  │   │   • quantity                                  │    │     │
│  │   │   • unitPrice                                │    │     │
│  │   │   • lineTotal                                │    │     │
│  │   └──────────────────────────────────────────────┘    │     │
│  │                                                         │     │
│  │   RULES:                                                │     │
│  │   • All changes go through Order (the root)            │     │
│  │   • OrderLineItems can't exist without Order           │     │
│  │   • Everything inside is transactionally consistent    │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                  │
│   OUTSIDE THE AGGREGATE (Just References):                      │
│   • Customer (owned by User Context)                            │
│   • Product (owned by Catalog Context)                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**Aggregate Rules:**

1. **One aggregate = One transaction**
   - Everything inside an aggregate is saved together
   - No transactions spanning multiple aggregates

2. **Reference other aggregates by ID only**
   - Don't embed full objects from other aggregates
   - Use IDs and look up when needed

3. **Keep aggregates small**
   - Large aggregates = more contention
   - Large aggregates = slower loads

\`\`\`typescript
// ✅ CORRECT: Reference by ID
class Order {
  customerId: string;  // Just the ID
  items: OrderLineItem[];  // Embedded (same aggregate)
}

// ❌ WRONG: Embedding other aggregates
class Order {
  customer: Customer;  // Don't embed! Customer is separate aggregate
  items: OrderLineItem[];
}
\`\`\``,
          keyPoints: [
            "Aggregate = group of objects that change together",
            "All changes within an aggregate are transactional",
            "Reference other aggregates by ID, not by embedding",
            "Keep aggregates small for performance and concurrency"
          ]
        },
        {
          title: "Context Mapping: How Contexts Relate",
          content: `Bounded contexts don't exist in isolation. They need to communicate. **Context Mapping** defines how.

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│               CONTEXT RELATIONSHIP PATTERNS                      │
│                                                                  │
│  1. SHARED KERNEL                                               │
│  ─────────────────                                              │
│  Two contexts share a subset of the model.                      │
│  ┌─────────┐     ┌─────────┐                                   │
│  │Context A│◄───►│Context B│  Both depend on shared code       │
│  └────┬────┘     └────┬────┘                                   │
│       └──────┬───────┘                                         │
│         ┌────▼────┐                                            │
│         │ Shared  │                                            │
│         │ Kernel  │                                            │
│         └─────────┘                                            │
│  ⚠️ Use sparingly - creates coupling!                          │
│                                                                  │
│  2. CUSTOMER-SUPPLIER (Upstream/Downstream)                     │
│  ──────────────────────────────────────────                     │
│  One context provides data, other consumes it.                  │
│  ┌──────────────┐      ┌──────────────┐                        │
│  │   Orders     │ ───► │  Reporting   │                        │
│  │  (Upstream)  │      │ (Downstream) │                        │
│  └──────────────┘      └──────────────┘                        │
│  Upstream dictates the model. Downstream adapts.               │
│                                                                  │
│  3. ANTI-CORRUPTION LAYER (ACL)                                 │
│  ──────────────────────────────                                 │
│  Downstream protects itself from upstream's model.              │
│  ┌───────────┐     ┌───────────────┐     ┌──────────┐         │
│  │ Legacy    │ ──► │    ACL        │ ──► │ New      │         │
│  │ System    │     │ (Translator)  │     │ System   │         │
│  └───────────┘     └───────────────┘     └──────────┘         │
│  ACL translates between models. New system stays clean.        │
│                                                                  │
│  4. PUBLISHED LANGUAGE                                          │
│  ────────────────────                                           │
│  Shared language for integration (like events/APIs).            │
│  ┌───────────┐                     ┌──────────┐                │
│  │Context A  │ ──► JSON Schema ──► │Context B │                │
│  └───────────┘     (Contract)      └──────────┘                │
│  Both agree on the published format.                           │
│                                                                  │
│  5. SEPARATE WAYS                                               │
│  ───────────────                                                │
│  No integration. Contexts are completely independent.           │
│  ┌───────────┐         ┌──────────┐                            │
│  │Context A  │    ✕    │Context B │                            │
│  └───────────┘         └──────────┘                            │
│  Sometimes the best integration is no integration!             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**Practical Example: E-commerce Context Map**

\`\`\`
                    ┌────────────────┐
                    │   Customers    │
                    │   (Identity)   │
                    └───────┬────────┘
                            │ ACL
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
        ┌───────────────┐     ┌────────────────┐
        │    Orders     │     │    Support     │
        │   Context     │     │    Context     │
        └───────┬───────┘     └────────────────┘
                │ Published Language (Events)
        ┌───────┴───────┬─────────────┐
        ▼               ▼             ▼
┌───────────────┐ ┌───────────┐ ┌───────────┐
│   Shipping    │ │ Inventory │ │  Billing  │
│   Context     │ │  Context  │ │  Context  │
└───────────────┘ └───────────┘ └───────────┘
\`\`\``,
          keyPoints: [
            "Contexts communicate through well-defined relationships",
            "ACL protects your context from external model changes",
            "Published Language = shared contracts (APIs, events)",
            "Sometimes separate ways (no integration) is best"
          ]
        },
        {
          title: "Event Storming: Discovering Boundaries",
          content: `**Event Storming** is a workshop technique to discover domain events and service boundaries.

**How It Works:**

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│                    EVENT STORMING PROCESS                        │
│                                                                  │
│  Materials: Orange sticky notes (events), Blue (commands),      │
│             Yellow (aggregates), Pink (systems), Green (users)  │
│                                                                  │
│  STEP 1: Identify Domain Events (Orange)                        │
│  ────────────────────────────────────────                       │
│  • What HAPPENED in the business?                               │
│  • Use past tense: "Order Placed", "Payment Received"           │
│  • Put ALL events on the wall, no filtering                     │
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│  │   Order     │ │  Payment    │ │   Order     │               │
│  │   Placed    │ │  Received   │ │   Shipped   │               │
│  └─────────────┘ └─────────────┘ └─────────────┘               │
│                                                                  │
│  STEP 2: Add Commands (Blue)                                    │
│  ───────────────────────────                                    │
│  • What TRIGGERED the event?                                    │
│  • "Place Order" → "Order Placed"                               │
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐                            │
│  │   Place     │ ─► │   Order     │                            │
│  │   Order     │    │   Placed    │                            │
│  └─────────────┘    └─────────────┘                            │
│                                                                  │
│  STEP 3: Group into Aggregates (Yellow)                         │
│  ──────────────────────────────────────                         │
│  • Which events belong together?                                │
│  • What's the "thing" these events are about?                   │
│                                                                  │
│  ┌─────────────────────────────────────────┐                   │
│  │             ORDER AGGREGATE             │                   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐  │                   │
│  │  │ Order   │ │ Order   │ │ Order   │  │                   │
│  │  │ Placed  │ │ Paid    │ │ Shipped │  │                   │
│  │  └─────────┘ └─────────┘ └─────────┘  │                   │
│  └─────────────────────────────────────────┘                   │
│                                                                  │
│  STEP 4: Draw Bounded Context Boundaries                        │
│  ──────────────────────────────────────────                     │
│  • Where do terms change meaning?                               │
│  • Where could a different team own this?                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**Example Output:**

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│          E-COMMERCE: EVENT STORMING RESULT                       │
│                                                                  │
│  ╔═══════════════════════════════════════╗                     │
│  ║         ORDERING CONTEXT              ║                     │
│  ║  ┌────────────────────────────────┐  ║                     │
│  ║  │        CART Aggregate          │  ║                     │
│  ║  │  • Item Added to Cart          │  ║                     │
│  ║  │  • Item Removed from Cart      │  ║                     │
│  ║  │  • Cart Cleared                │  ║                     │
│  ║  └────────────────────────────────┘  ║                     │
│  ║  ┌────────────────────────────────┐  ║                     │
│  ║  │        ORDER Aggregate         │  ║                     │
│  ║  │  • Order Placed                │  ║                     │
│  ║  │  • Order Confirmed             │  ║                     │
│  ║  │  • Order Cancelled             │  ║                     │
│  ║  └────────────────────────────────┘  ║                     │
│  ╚═══════════════════════════════════════╝                     │
│                                                                  │
│  ╔═══════════════════════════════════════╗                     │
│  ║         PAYMENT CONTEXT               ║                     │
│  ║  ┌────────────────────────────────┐  ║                     │
│  ║  │       PAYMENT Aggregate        │  ║                     │
│  ║  │  • Payment Initiated           │  ║                     │
│  ║  │  • Payment Succeeded           │  ║                     │
│  ║  │  • Payment Failed              │  ║                     │
│  ║  │  • Refund Issued               │  ║                     │
│  ║  └────────────────────────────────┘  ║                     │
│  ╚═══════════════════════════════════════╝                     │
│                                                                  │
│  ╔═══════════════════════════════════════╗                     │
│  ║         SHIPPING CONTEXT              ║                     │
│  ║  ┌────────────────────────────────┐  ║                     │
│  ║  │      SHIPMENT Aggregate        │  ║                     │
│  ║  │  • Shipment Created            │  ║                     │
│  ║  │  • Shipment Dispatched         │  ║                     │
│  ║  │  • Shipment Delivered          │  ║                     │
│  ║  │  • Delivery Failed             │  ║                     │
│  ║  └────────────────────────────────┘  ║                     │
│  ╚═══════════════════════════════════════╝                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
\`\`\``,
          keyPoints: [
            "Event Storming brings domain experts and developers together",
            "Focus on EVENTS first (what happened), then commands (what triggered)",
            "Group events into aggregates, aggregates into bounded contexts",
            "Boundaries emerge from the domain, not from technical concerns"
          ]
        },
        {
          title: "Data Ownership: The Golden Rule",
          content: `**THE GOLDEN RULE: Each piece of data has exactly ONE owner.**

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│                  DATA OWNERSHIP RULES                            │
│                                                                  │
│  ✅ CORRECT: Single Owner                                       │
│  ────────────────────────────                                   │
│                                                                  │
│  User Service OWNS:           Order Service OWNS:               │
│  • User profiles              • Orders                          │
│  • Authentication             • Order items                     │
│  • Preferences                • Order status                    │
│                                                                  │
│  If Order Service needs user name, it:                          │
│  1. Asks User Service via API, OR                               │
│  2. Listens to events and keeps a local copy                    │
│                                                                  │
│  ═══════════════════════════════════════════════════════════   │
│                                                                  │
│  ❌ WRONG: Shared Database (Multiple owners)                    │
│  ───────────────────────────────────────────                    │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Orders    │  │    Users    │  │  Payments   │             │
│  │   Service   │  │   Service   │  │   Service   │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         │                │                │                     │
│         └────────────────┼────────────────┘                     │
│                          ▼                                      │
│                ┌──────────────────┐                            │
│                │  SHARED DATABASE │                            │
│                │                  │                            │
│                │ • users table    │ ← Who owns this?           │
│                │ • orders table   │ ← Multiple services        │
│                │ • payments table │   read AND write!          │
│                └──────────────────┘                            │
│                                                                  │
│  Problems:                                                      │
│  • Who is responsible for the schema?                           │
│  • A change in User table breaks Order Service                 │
│  • Can't deploy services independently                          │
│  • No clear ownership = no accountability                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**Handling Shared Data Needs:**

\`\`\`
Scenario: Order Service needs customer name for display

OPTION 1: API Call (Real-time)
─────────────────────────────
Order Service → GET /users/123 → User Service
Pros: Always current
Cons: Runtime dependency, latency

OPTION 2: Data Replication (Eventually consistent)
─────────────────────────────────────────────────
User Service publishes: user_updated { id, name, email }
Order Service stores: customer_cache { userId, name }

Pros: No runtime dependency, fast reads
Cons: Stale data possible

OPTION 3: Denormalization at Write Time
──────────────────────────────────────
When creating order, copy the customer name INTO the order:
Order { customerId: 123, customerName: "John" }

Pros: Self-contained order document
Cons: Stale if name changes (often acceptable for orders)
\`\`\`

**Which to Choose?**

| Need | Pattern | Example |
|------|---------|---------|
| Always need current data | API Call | Check real-time inventory |
| Eventual consistency OK | Data Replication | Display customer name |
| Historical accuracy | Denormalization | Invoice with address |`,
          keyPoints: [
            "One service owns each piece of data - no exceptions",
            "Never share databases between services",
            "Need data you don't own? API call or event-based replication",
            "Denormalize at write time for historical accuracy"
          ]
        }
      ],
      codeExample: {
        title: "Bounded Context Implementation Example",
        language: "typescript",
        filename: "bounded-contexts-example.ts",
        code: `// ============================================
// BOUNDED CONTEXTS IN PRACTICE
// ============================================
// Notice how "Product" means different things
// in different contexts!

// ════════════════════════════════════════════════════
// CATALOG CONTEXT
// "Product" = What customers see and browse
// ════════════════════════════════════════════════════

// catalog-context/product.entity.ts
class CatalogProduct {
  id: string;
  name: string;
  description: string;
  images: string[];
  categories: string[];
  price: Money;
  specifications: Map<string, string>;
  reviews: Review[];
  averageRating: number;
  
  // Catalog-specific behavior
  isInCategory(categoryId: string): boolean { }
  hasPositiveReviews(): boolean { }
}

// catalog-context/product.service.ts
class CatalogProductService {
  // Only catalog-related operations
  search(query: string): CatalogProduct[] { }
  getByCategory(categoryId: string): CatalogProduct[] { }
  getRecommendations(userId: string): CatalogProduct[] { }
}


// ════════════════════════════════════════════════════
// INVENTORY CONTEXT  
// "Product" = What's in the warehouse
// ════════════════════════════════════════════════════

// inventory-context/product.entity.ts
class InventoryProduct {
  sku: string;                    // Different ID system!
  warehouseId: string;
  location: string;               // "Aisle 5, Shelf 3"
  quantityOnHand: number;
  quantityReserved: number;
  reorderPoint: number;
  lastCountDate: Date;
  
  // Inventory-specific behavior
  isAvailable(quantity: number): boolean {
    return (this.quantityOnHand - this.quantityReserved) >= quantity;
  }
  needsReorder(): boolean {
    return this.quantityOnHand <= this.reorderPoint;
  }
}

// inventory-context/product.service.ts
class InventoryProductService {
  // Only inventory-related operations
  reserve(sku: string, quantity: number): Reservation { }
  release(reservationId: string): void { }
  adjustStock(sku: string, adjustment: number): void { }
}


// ════════════════════════════════════════════════════
// SHIPPING CONTEXT
// "Product" = What needs to be packaged and shipped
// ════════════════════════════════════════════════════

// shipping-context/product.entity.ts
class ShippingProduct {
  sku: string;
  weight: number;                 // In grams
  dimensions: Dimensions;         // L x W x H
  isFragile: boolean;
  requiresRefrigeration: boolean;
  hazardClass?: string;
  
  // Shipping-specific behavior
  getShippingClass(): 'standard' | 'oversized' | 'hazmat' { }
  requiresSpecialHandling(): boolean { }
}


// ════════════════════════════════════════════════════
// ORDER CONTEXT
// Uses REFERENCES to other contexts, not full objects
// ════════════════════════════════════════════════════

// order-context/order.aggregate.ts
class Order {
  id: string;
  customerId: string;              // Reference to User Context
  items: OrderLineItem[];
  status: OrderStatus;
  
  // Order has its OWN copy of price at time of order
  // (doesn't change if catalog price changes later)
}

class OrderLineItem {
  productId: string;               // Reference to Catalog Context
  sku: string;                     // Reference to Inventory Context
  productName: string;             // Denormalized - copied at order time
  unitPrice: Money;                // Denormalized - copied at order time
  quantity: number;
}

// order-context/order.service.ts
class OrderService {
  constructor(
    private orderRepo: OrderRepository,
    private inventoryClient: InventoryClient,  // Anti-corruption layer
    private catalogClient: CatalogClient,      // Anti-corruption layer
  ) {}

  async placeOrder(customerId: string, items: CartItem[]): Promise<Order> {
    // Get current product info from Catalog Context
    const products = await this.catalogClient.getProducts(
      items.map(i => i.productId)
    );
    
    // Reserve inventory in Inventory Context
    const reservations = await Promise.all(
      items.map(item => this.inventoryClient.reserve(item.sku, item.quantity))
    );
    
    // Create order with denormalized data
    const order = new Order({
      customerId,
      items: items.map(item => ({
        productId: item.productId,
        sku: item.sku,
        productName: products[item.productId].name,  // Copy!
        unitPrice: products[item.productId].price,   // Copy!
        quantity: item.quantity,
      })),
      status: 'PENDING'
    });
    
    return this.orderRepo.save(order);
  }
}


// ════════════════════════════════════════════════════
// ANTI-CORRUPTION LAYER EXAMPLE
// Translates between contexts
// ════════════════════════════════════════════════════

// order-context/clients/inventory.client.ts
class InventoryClient {
  // This class translates Inventory Context language
  // into Order Context language
  
  async reserve(sku: string, quantity: number): Promise<string> {
    // Call Inventory Service's API
    const response = await this.http.post('/inventory/reservations', {
      sku,
      quantity,
      reason: 'ORDER'
    });
    
    // Translate response to our context's terms
    return response.reservationId;
  }
}

// ════════════════════════════════════════════════════
// KEY TAKEAWAYS:
// ════════════════════════════════════════════════════
//
// 1. Same word (Product) = different classes in different contexts
// 2. Each context has its own database/tables
// 3. Contexts communicate via APIs or events
// 4. Anti-corruption layer translates between contexts
// 5. Denormalize data that's needed for historical accuracy
// ════════════════════════════════════════════════════`
      },
      nextSteps: `You now understand how to define service boundaries using DDD. This is the foundation for avoiding the distributed monolith trap. Next, we'll build your first microservice with these principles in mind.`
    }
  },
  // Old module 3 - renumbered to 5
  {
    number: 5,
    slug: "first-microservice",
    title: "Your First Microservice",
    description: "Build your first microservice with NestJS. Learn REST APIs, CRUD operations, validation, and error handling.",
    difficulty: "beginner",
    topics: ["Project Setup", "REST APIs", "CRUD Operations", "DTO & Validation", "Error Handling", "Testing"],
    prerequisites: ["NestJS fundamentals", "Basic REST concepts"],
    learningOutcomes: [
      "Create a NestJS module with controllers and services",
      "Implement REST endpoints and CRUD operations",
      "Use DTOs for validation and error handling"
    ],
    estimatedTime: "60–90 minutes",
    content: {
      intro: `Time to build something real! 🛠️

In this module, we'll create a complete **Product Service** - a microservice that manages products for an e-commerce platform. This is the kind of service you'd find in production systems at companies like Amazon or Shopify.

**What We'll Build:**

A fully functional REST API that can:
- ✅ Create new products
- ✅ List all products with filtering
- ✅ Get product details by ID
- ✅ Update product information
- ✅ Delete products
- ✅ Validate input data
- ✅ Handle errors gracefully

Let's build it step by step!`,
      sections: [
        {
          title: "Step 1: Project Setup & Structure",
          content: `First, let's create our project and understand the folder structure we'll use.

**Create the Project:**

\`\`\`bash
nest new product-service
cd product-service
\`\`\`

**Install Required Dependencies:**

\`\`\`bash
# For validation
npm install class-validator class-transformer

# For database (we'll use SQLite for simplicity)
npm install @nestjs/typeorm typeorm sqlite3
\`\`\`

**Our Target Folder Structure:**

\`\`\`
product-service/
├── src/
│   ├── products/
│   │   ├── dto/                    # Data Transfer Objects
│   │   │   ├── create-product.dto.ts
│   │   │   └── update-product.dto.ts
│   │   ├── entities/
│   │   │   └── product.entity.ts   # Database model
│   │   ├── products.controller.ts  # HTTP endpoints
│   │   ├── products.service.ts     # Business logic
│   │   └── products.module.ts
│   ├── app.module.ts
│   └── main.ts
└── package.json
\`\`\`

**Why This Structure?**

- **dto/** - Defines the shape of data coming in (validation)
- **entities/** - Defines how data is stored in database
- **controller** - HTTP layer (routes)
- **service** - Business logic (where the real work happens)
- **module** - Ties everything together`,
          keyPoints: [
            "Each microservice should have a clear, consistent structure",
            "Separate concerns: HTTP handling vs business logic vs data",
            "DTOs ensure we validate and transform incoming data",
            "Entities define our database schema"
          ]
        },
        {
          title: "Step 2: Define the Product Entity (Database Model)",
          content: `The **entity** defines how our product data is stored in the database. Think of it as a blueprint for a database table.

**What is an Entity?**

An entity is just a class that maps to a database table. Each property becomes a column:

\`\`\`
Product Entity          →    Products Table
---------------              --------------
id: number             →    id INTEGER (primary key)
name: string           →    name VARCHAR
description: string    →    description TEXT
price: number          →    price DECIMAL
stock: number          →    stock INTEGER
category: string       →    category VARCHAR
createdAt: Date        →    created_at TIMESTAMP
\`\`\`

**The Complete Entity:**

See the code example below for the full implementation with decorators explained.`,
          keyPoints: [
            "@Entity() marks a class as a database table",
            "@PrimaryGeneratedColumn() creates an auto-incrementing ID",
            "@Column() defines table columns with their types",
            "@CreateDateColumn() automatically sets creation timestamp"
          ]
        },
        {
          title: "Step 3: Create DTOs for Validation",
          content: `**DTO = Data Transfer Object**

DTOs define what data we EXPECT from API requests. They help us:
1. **Validate** - Reject invalid data before it causes problems
2. **Document** - Show exactly what the API expects
3. **Transform** - Convert data to the right types

**Example Problem Without DTOs:**

Someone sends: \`{ "price": "not-a-number" }\`
Without validation, this could crash your app or corrupt data!

**With DTOs:**

We define rules:
- \`name\` must be a string, 3-100 characters
- \`price\` must be a positive number
- \`stock\` must be 0 or greater

If rules are broken, we automatically reject with helpful error messages.`,
          keyPoints: [
            "DTOs catch bad data at the API boundary",
            "class-validator provides decorators like @IsString(), @Min(), @Max()",
            "Validation happens automatically in the request pipeline",
            "Users get clear error messages explaining what's wrong"
          ]
        },
        {
          title: "Step 4: Build the Service (Business Logic)",
          content: `The **Service** contains all the business logic. It's where:
- We interact with the database
- We apply business rules
- We handle edge cases

**Business Rules We'll Implement:**

1. Product names must be unique
2. Price cannot be negative
3. Stock cannot go below 0
4. Deleting a product requires confirmation
5. Updating stock emits an event (for other services)

**Why Keep Logic in Services?**

- **Reusability**: Multiple controllers can use the same service
- **Testing**: Services are easy to unit test
- **Organization**: Clear separation of concerns`,
          keyPoints: [
            "Services are decorated with @Injectable()",
            "Use TypeORM Repository pattern for database operations",
            "Throw proper HTTP exceptions for error cases",
            "Keep controllers thin, services contain the real logic"
          ]
        }
      ],
      codeExample: {
        title: "Complete Product Service Implementation",
        language: "typescript",
        filename: "src/products/products.service.ts",
        code: `// ============================================
// FILE: src/products/entities/product.entity.ts
// PURPOSE: Defines the product database table
// ============================================

import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn } from 'typeorm';

@Entity('products')  // Table name in database
export class Product {
  @PrimaryGeneratedColumn()  // Auto-incrementing ID
  id: number;

  @Column({ length: 100 })  // VARCHAR(100) - product name
  name: string;

  @Column('text', { nullable: true })  // TEXT - optional description  
  description: string;

  @Column('decimal', { precision: 10, scale: 2 })  // 10 digits, 2 decimals
  price: number;

  @Column('int', { default: 0 })  // Stock quantity
  stock: number;

  @Column({ length: 50 })  // Category name
  category: string;

  @CreateDateColumn()  // Automatically set on creation
  createdAt: Date;

  @UpdateDateColumn()  // Automatically updated on save
  updatedAt: Date;
}


// ============================================
// FILE: src/products/dto/create-product.dto.ts
// PURPOSE: Validation rules for creating products
// ============================================

import { IsString, IsNumber, IsOptional, Min, Length } from 'class-validator';

export class CreateProductDto {
  @IsString()
  @Length(3, 100, { message: 'Name must be between 3 and 100 characters' })
  name: string;

  @IsOptional()
  @IsString()
  description?: string;

  @IsNumber()
  @Min(0.01, { message: 'Price must be greater than 0' })
  price: number;

  @IsNumber()
  @Min(0, { message: 'Stock cannot be negative' })
  stock: number;

  @IsString()
  @Length(2, 50, { message: 'Category must be between 2 and 50 characters' })
  category: string;
}


// ============================================
// FILE: src/products/products.service.ts
// PURPOSE: All product business logic
// ============================================

import { Injectable, NotFoundException, ConflictException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Product } from './entities/product.entity';
import { CreateProductDto } from './dto/create-product.dto';

@Injectable()
export class ProductsService {
  constructor(
    @InjectRepository(Product)
    private productRepository: Repository<Product>,
  ) {}

  // CREATE: Add a new product
  async create(createProductDto: CreateProductDto): Promise<Product> {
    // Check if product name already exists
    const existing = await this.productRepository.findOne({
      where: { name: createProductDto.name }
    });
    
    if (existing) {
      throw new ConflictException('A product with this name already exists');
    }

    // Create and save the product
    const product = this.productRepository.create(createProductDto);
    return await this.productRepository.save(product);
  }

  // READ: Get all products (with optional category filter)
  async findAll(category?: string): Promise<Product[]> {
    if (category) {
      return this.productRepository.find({
        where: { category },
        order: { createdAt: 'DESC' }
      });
    }
    return this.productRepository.find({
      order: { createdAt: 'DESC' }
    });
  }

  // READ: Get single product by ID
  async findOne(id: number): Promise<Product> {
    const product = await this.productRepository.findOne({
      where: { id }
    });
    
    if (!product) {
      throw new NotFoundException(\`Product with ID \${id} not found\`);
    }
    
    return product;
  }

  // UPDATE: Modify an existing product
  async update(id: number, updateData: Partial<CreateProductDto>): Promise<Product> {
    const product = await this.findOne(id);  // Throws if not found
    
    // Merge updates with existing data
    Object.assign(product, updateData);
    
    return await this.productRepository.save(product);
  }

  // DELETE: Remove a product
  async remove(id: number): Promise<void> {
    const product = await this.findOne(id);  // Throws if not found
    await this.productRepository.remove(product);
  }

  // BUSINESS LOGIC: Update stock after an order
  async updateStock(id: number, quantity: number): Promise<Product> {
    const product = await this.findOne(id);
    
    if (product.stock < quantity) {
      throw new ConflictException(\`Insufficient stock. Available: \${product.stock}\`);
    }
    
    product.stock -= quantity;
    return await this.productRepository.save(product);
  }
}


// ============================================
// API ENDPOINTS SUMMARY:
// ============================================
//
// POST   /products          Create new product
// GET    /products          Get all products
// GET    /products?category=electronics   Filter by category
// GET    /products/:id      Get single product
// PATCH  /products/:id      Update product
// DELETE /products/:id      Delete product
//
// ============================================`
      },
      nextSteps: `Congratulations! You've built a complete microservice. Next, we'll learn how microservices communicate with each other using different patterns.`
    }
  },
  // Old module 4 - renumbered to 6
  {
    number: 6,
    slug: "communication",
    title: "Inter-service Communication",
    description: "Master different communication patterns between microservices: synchronous (HTTP, gRPC) and asynchronous (message queues), plus data access strategies.",
    difficulty: "intermediate",
    topics: ["HTTP/REST", "gRPC", "Message Queues", "RabbitMQ", "Apache Kafka", "Event-Driven Architecture", "API Composition", "Data Access Patterns"],
    prerequisites: ["NestJS fundamentals"],
    learningOutcomes: [
      "Explain synchronous vs asynchronous communication patterns",
      "Implement HTTP/gRPC clients and servers",
      "Use message queues for async workflows",
      "Choose the right pattern for cross-service data access",
      "Implement API Composition for aggregating data"
    ],
    estimatedTime: "60–90 minutes",
    content: {
      intro: `Now that you can build individual microservices, the next critical skill is making them **talk to each other**.

**The Challenge:**

In a monolith, calling another function is easy - it's just a function call. In microservices, services run on different servers, potentially in different data centers!

**Two Main Approaches:**

1. **Synchronous** - Service A calls Service B and WAITS for a response (like a phone call)
2. **Asynchronous** - Service A sends a message and continues working (like sending an email)

Let's explore both in detail with real examples.`,
      sections: [
        {
          title: "Synchronous Communication (HTTP/REST)",
          content: `**When to Use:**
- You need an immediate response
- The operation is simple and fast
- It's a direct request-response pattern

**Example Scenario:**

Order Service needs to check if a product exists before creating an order:

\`\`\`
ORDER SERVICE                    PRODUCT SERVICE
     │                                 │
     │  GET /products/123              │
     │ ──────────────────────────────► │
     │                                 │
     │  { id: 123, name: "Laptop" }    │
     │ ◄────────────────────────────── │
     │                                 │
     ▼ (continues with order)          │
\`\`\`

**The Problem:**

What if Product Service is down? Order Service is stuck waiting!

**Solutions:**
- Timeouts: Don't wait forever
- Retries: Try again if it fails
- Circuit Breakers: Stop trying if service is down
- Fallbacks: Use cached data or default response`,
          keyPoints: [
            "Simple to implement and understand",
            "Creates tight coupling between services",
            "Can cause cascading failures if one service is slow/down",
            "Use HTTP clients with proper timeout and retry logic"
          ]
        },
        {
          title: "Asynchronous Communication (Message Queues)",
          content: `**When to Use:**
- The sender doesn't need an immediate response
- Operations are slow (emails, reports, processing)
- You want loose coupling between services
- High throughput is needed

**How It Works:**

Instead of calling another service directly, you put a message on a queue. The other service picks it up when ready.

\`\`\`
ORDER SERVICE         MESSAGE QUEUE         EMAIL SERVICE
     │                    ┌────┐                  │
     │ ──► order_created ─│    │                  │
     │    (continues      │ ▸▸ │◄───────────────  │
     │     immediately)   │    │   (picks up      │
     ▼                    └────┘    when ready)   │
                                                  │
                                                  ▼
                                         (sends confirmation
                                          email to customer)
\`\`\`

**Benefits:**

1. **Decoupling**: Services don't need to know about each other
2. **Resilience**: If Email Service is down, messages wait in queue
3. **Scalability**: Add more consumers to process faster
4. **Reliability**: Messages are persisted, won't be lost`,
          keyPoints: [
            "Messages persist in queue even if consumer is down",
            "Producers and consumers are completely decoupled",
            "Perfect for workflows, notifications, data processing",
            "Adds complexity (need to manage queue infrastructure)"
          ]
        },
        {
          title: "RabbitMQ vs Apache Kafka",
          content: `Two most popular messaging systems - but they're designed for different use cases:

**RabbitMQ:**
- Traditional message broker
- Messages are deleted after consumption
- Complex routing capabilities
- Best for: Task queues, RPC, simple pub/sub

**Apache Kafka:**
- Distributed event streaming platform
- Messages are retained (can replay history)
- Ultra-high throughput (millions/sec)
- Best for: Event sourcing, log aggregation, real-time analytics

**When to Use What:**

| Scenario | Best Choice |
|----------|-------------|
| Send email after signup | RabbitMQ |
| Process real-time analytics | Kafka |
| Simple task queue | RabbitMQ |
| Event sourcing (replay events) | Kafka |
| Need complex routing | RabbitMQ |
| Very high volume (100k+ msg/sec) | Kafka |`,
          keyPoints: [
            "RabbitMQ: Traditional broker, simpler, good for most use cases",
            "Kafka: Event streaming, retention, very high throughput",
            "Start with RabbitMQ if unsure - easier to learn and operate",
            "Kafka has a steeper learning curve but scales massively"
          ]
        },
        {
          title: "gRPC: High-Performance Service Communication",
          content: `**What is gRPC?**

gRPC (Google Remote Procedure Call) is a high-performance framework for service-to-service communication. Unlike REST which uses JSON over HTTP/1.1, gRPC uses Protocol Buffers (protobuf) over HTTP/2.

**Why gRPC for Microservices?**

\`\`\`
REST (HTTP/JSON)                    gRPC (HTTP/2 + Protobuf)
─────────────────                   ────────────────────────
❌ Text-based (larger payloads)     ✅ Binary (10x smaller)
❌ HTTP/1.1 (one request/conn)      ✅ HTTP/2 (multiplexed)
❌ No built-in types               ✅ Strongly typed contracts
❌ Request-Response only           ✅ Bi-directional streaming
\`\`\`

**When to Use gRPC:**
- Internal service-to-service calls (not public APIs)
- High-throughput, low-latency requirements
- Polyglot environments (auto-generates clients for any language)
- Streaming data (real-time updates)

**The Contract (Proto file):**
\`\`\`protobuf
// user.proto - The contract between services
syntax = "proto3";

service UserService {
  rpc GetUser (GetUserRequest) returns (User);
  rpc ListUsers (ListUsersRequest) returns (stream User);  // Streaming!
}

message GetUserRequest {
  string user_id = 1;
}

message User {
  string id = 1;
  string name = 2;
  string email = 3;
}
\`\`\`

**Key Benefit:** From this ONE file, you auto-generate clients for Node.js, Go, Java, Python, etc. No more mismatched API contracts!`,
          keyPoints: [
            "10x faster than REST for internal communication",
            "Strongly typed - catch errors at compile time, not runtime",
            "Use REST for public APIs, gRPC for internal service calls",
            "Streaming support for real-time use cases"
          ]
        },
        {
          title: "API Composition: Querying Data Across Services",
          content: `**The Problem:**

Your frontend needs to display an order with customer details and product info. But that data lives in THREE different services:

\`\`\`
Order Service   → { orderId, userId, items: [{productId, qty}] }
User Service    → { userId, name, email }
Product Service → { productId, name, price }
\`\`\`

You need to COMBINE them. How?

**Solution: API Composition Pattern**

Create a "composer" (often in the API Gateway) that:
1. Calls multiple services in parallel
2. Combines the results
3. Returns one unified response

\`\`\`
┌──────────────────────────────────────────────────────────────────┐
│                    API COMPOSITION FLOW                          │
│                                                                  │
│  Client: GET /orders/123/full                                    │
│                      │                                           │
│                      ▼                                           │
│              ┌──────────────┐                                    │
│              │ API Gateway  │                                    │
│              │ (Composer)   │                                    │
│              └──────┬───────┘                                    │
│                     │                                            │
│      ┌──────────────┼──────────────┐  (parallel calls)          │
│      │              │              │                             │
│      ▼              ▼              ▼                             │
│ ┌─────────┐   ┌─────────┐   ┌─────────┐                        │
│ │ Order   │   │  User   │   │ Product │                        │
│ │ Service │   │ Service │   │ Service │                        │
│ └────┬────┘   └────┬────┘   └────┬────┘                        │
│      │              │              │                             │
│      ▼              ▼              ▼                             │
│  { orderId,     { name,       { name,                           │
│    items }       email }       price }                           │
│                     │                                            │
│              ┌──────▼───────┐                                    │
│              │   COMBINE    │                                    │
│              └──────┬───────┘                                    │
│                     ▼                                            │
│  {                                                               │
│    orderId: "123",                                               │
│    customer: { name: "John", email: "john@..." },                │
│    items: [{ name: "Laptop", price: 999, qty: 1 }],              │
│    total: 999                                                    │
│  }                                                               │
└──────────────────────────────────────────────────────────────────┘
\`\`\`

**Code Example:**
\`\`\`typescript
// api-gateway/order-composer.service.ts
async getOrderDetails(orderId: string) {
  // 1. Get the order first (we need userId and productIds)
  const order = await this.orderService.getOrder(orderId);
  
  // 2. Fetch related data IN PARALLEL
  const [customer, products] = await Promise.all([
    this.userService.getUser(order.userId),
    this.productService.getProducts(order.items.map(i => i.productId))
  ]);
  
  // 3. Compose the response
  return {
    orderId: order.id,
    status: order.status,
    customer: {
      name: customer.name,
      email: customer.email
    },
    items: order.items.map(item => ({
      ...products.find(p => p.id === item.productId),
      quantity: item.quantity
    })),
    total: this.calculateTotal(order.items, products)
  };
}
\`\`\`

**Trade-offs:**
- ✅ Client gets all data in ONE call
- ✅ Backend handles complexity
- ❌ Gateway becomes complex
- ❌ Latency = slowest service call
- ❌ If any service fails, entire request fails`,
          keyPoints: [
            "Use Promise.all() to call services in parallel",
            "The composer can live in API Gateway or a dedicated BFF (Backend for Frontend)",
            "Consider caching frequently accessed data",
            "Implement fallbacks for non-critical data"
          ]
        },
        {
          title: "Decision Framework: How to Get Data You Don't Own",
          content: `**The Fundamental Question:**

"My service needs data owned by another service. What should I do?"

**Use this decision tree:**

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│  Q1: Do you need REAL-TIME (latest) data?                       │
└─────────────────────────────────────────────────────────────────┘
                        │
           ┌────────────┴────────────┐
          YES                        NO
           │                         │
           ▼                         ▼
┌─────────────────────┐    ┌─────────────────────┐
│ SYNC API CALL       │    │ DATA REPLICATION    │
│                     │    │                     │
│ • HTTP/gRPC call    │    │ • Subscribe to      │
│ • API Composition   │    │   events            │
│ • BFF Pattern       │    │ • Keep local copy   │
│                     │    │ • Update on change  │
│ Trade-offs:         │    │                     │
│ ❌ Runtime coupling │    │ Trade-offs:         │
│ ❌ Added latency    │    │ ❌ Eventual         │
│ ❌ Failure risk     │    │   consistency       │
│ ✅ Always fresh     │    │ ❌ Storage cost     │
│                     │    │ ✅ Fast (local)     │
│                     │    │ ✅ No dependency    │
└─────────────────────┘    └─────────────────────┘
\`\`\`

**Pattern Comparison:**

| Pattern | Use When | Latency | Coupling | Consistency |
|---------|----------|---------|----------|-------------|
| Sync API Call | Need real-time data | High | High | Strong |
| API Composition | Aggregate for display | High | High | Strong |
| Data Replication | Can tolerate staleness | Low | Low | Eventual |
| CQRS | High read volume | Low | Low | Eventual |
| Shared Database | ⚠️ AVOID | Low | Very High | Strong |

**Example Scenarios:**

1. **"Show user name on order"** → Data Replication
   - User name rarely changes
   - Cache it locally, update via events
   
2. **"Check real-time inventory"** → Sync API Call
   - Must be current (can't oversell)
   - Accept the latency cost

3. **"Display order history with products"** → API Composition
   - Historical data, doesn't change
   - Compose at read time

4. **"Real-time dashboard"** → Event Streaming
   - Subscribe to events
   - Build materialized view`,
          keyPoints: [
            "There's no one-size-fits-all answer",
            "Always prefer eventual consistency if business allows",
            "The more services you call synchronously, the more fragile your system",
            "Data replication trades storage for availability"
          ]
        }
      ],
      codeExample: {
        title: "Complete RabbitMQ Example in NestJS",
        language: "typescript",
        filename: "order-service/orders.service.ts",
        code: `// ============================================
// ORDER SERVICE - Publishing Events to RabbitMQ
// ============================================
// When an order is created, we publish an event
// so other services can react (send email, update inventory, etc.)

import { Injectable } from '@nestjs/common';
import { ClientProxy, ClientProxyFactory, Transport } from '@nestjs/microservices';

@Injectable()
export class OrdersService {
  private messageClient: ClientProxy;

  constructor() {
    // Connect to RabbitMQ
    this.messageClient = ClientProxyFactory.create({
      transport: Transport.RMQ,
      options: {
        urls: ['amqp://localhost:5672'],  // RabbitMQ server address
        queue: 'orders_queue',             // Queue name
        queueOptions: { durable: true },   // Survive broker restart
      },
    });
  }

  async createOrder(orderData: CreateOrderDto) {
    // 1. Save order to database
    const order = await this.saveToDatabase(orderData);
    
    // 2. Publish event to message queue
    //    Other services will receive this and react!
    this.messageClient.emit('order_created', {
      orderId: order.id,
      customerId: order.customerId,
      items: order.items,
      total: order.total,
      createdAt: new Date(),
    });
    
    // 3. Return immediately (don't wait for email to be sent)
    return order;
  }
}


// ============================================
// EMAIL SERVICE - Consuming Events from RabbitMQ  
// ============================================
// This service listens for order_created events
// and sends confirmation emails

import { Controller } from '@nestjs/common';
import { EventPattern, Payload } from '@nestjs/microservices';

@Controller()
export class EmailController {
  
  // This method is called whenever an 'order_created' event arrives
  @EventPattern('order_created')
  async handleOrderCreated(@Payload() data: any) {
    console.log('📧 Received order_created event:', data.orderId);
    
    // Send confirmation email
    await this.emailService.sendOrderConfirmation({
      to: data.customerEmail,
      orderId: data.orderId,
      items: data.items,
      total: data.total,
    });
    
    console.log('✅ Confirmation email sent for order:', data.orderId);
  }
}


// ============================================
// INVENTORY SERVICE - Also listening to same event
// ============================================
// Multiple services can react to the same event!

@Controller()
export class InventoryController {
  
  @EventPattern('order_created')
  async handleOrderCreated(@Payload() data: any) {
    console.log('📦 Updating inventory for order:', data.orderId);
    
    // Reduce stock for each ordered item
    for (const item of data.items) {
      await this.inventoryService.reduceStock(item.productId, item.quantity);
    }
    
    console.log('✅ Inventory updated for order:', data.orderId);
  }
}


// ============================================
// THE FLOW:
// ============================================
//
// 1. Customer places order
// 2. Order Service creates order in database
// 3. Order Service publishes 'order_created' to RabbitMQ
// 4. Order Service returns success to customer (FAST!)
// 5. Meanwhile, in the background:
//    - Email Service receives event → sends email
//    - Inventory Service receives event → updates stock
//    - Analytics Service receives event → records metrics
//
// ============================================`
      },
      nextSteps: `Now you understand how services communicate. Next, we'll tackle one of the hardest problems in microservices - managing data across services.`
    }
  },
  // Old module 5 - renumbered to 7
  {
    number: 7,
    slug: "database-patterns",
    title: "Database Patterns",
    description: "Learn database strategies for microservices: database per service, saga pattern, outbox pattern, CQRS, event sourcing, and data replication.",
    difficulty: "intermediate",
    topics: ["Database per Service", "Data Consistency", "Saga Pattern", "Outbox Pattern", "Data Replication", "CQRS", "Event Sourcing"],
    prerequisites: ["Inter-service Communication"],
    learningOutcomes: [
      "Understand database-per-service pattern and its implications",
      "Implement the Saga pattern for distributed transactions",
      "Use the Outbox pattern for reliable event publishing",
      "Apply CQRS to separate read and write models",
      "Understand when to use Event Sourcing",
      "Implement data replication for local caching"
    ],
    estimatedTime: "90–120 minutes",
    content: {
      intro: `Data management is the **hardest part** of microservices.

In a monolith, you have one database. Need to join users with orders? Easy - one query.

In microservices, each service should own its data. But what happens when:
- Order Service needs user info (owned by User Service)?
- A transaction spans multiple services?
- You need to keep data consistent across services?

Let's solve these challenges!`,
      sections: [
        {
          title: "The Database-per-Service Pattern",
          content: `**The Rule:** Each microservice has its own private database.

**Why?**

1. **Loose Coupling**: Services can evolve independently
2. **Technology Freedom**: Use PostgreSQL for users, MongoDB for products
3. **Scaling**: Scale each database based on its service's needs
4. **Clear Ownership**: The User Service is the only one who touches user data

\`\`\`
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   User Service   │     │  Order Service   │     │ Product Service  │
└────────┬─────────┘     └────────┬─────────┘     └────────┬─────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   PostgreSQL     │     │    MongoDB       │     │   PostgreSQL     │
│                  │     │                  │     │                  │
│ • users table    │     │ • orders         │     │ • products       │
│ • profiles       │     │ • order_items    │     │ • categories     │
│ • authentcation  │     │ • payments       │     │ • inventory      │
└──────────────────┘     └──────────────────┘     └──────────────────┘
\`\`\`

**The Challenge:**

No more JOINs across tables! You can't do:
\`\`\`sql
SELECT * FROM users JOIN orders ON users.id = orders.user_id
\`\`\`

Instead, services must communicate through APIs.`,
          keyPoints: [
            "Each service's database is PRIVATE - no direct access by others",
            "Want user data in Order Service? Call the User Service API",
            "This enables true independence but adds complexity",
            "It's okay to duplicate some data for performance"
          ]
        },
        {
          title: "Handling Data Consistency: The Saga Pattern",
          content: `**The Problem:**

Creating an order involves multiple services:
1. ✅ Reserve inventory (Inventory Service)
2. ✅ Charge payment (Payment Service)  
3. ✅ Create shipment (Shipping Service)

What if payment fails after inventory is reserved?

**The Saga Pattern:**

A saga is a sequence of local transactions. If one fails, we run **compensating transactions** to undo previous steps.

\`\`\`
SUCCESS PATH:
─────────────
Reserve    →    Charge    →    Create      →    COMPLETE ✅
Inventory       Payment        Shipment

FAILURE PATH (payment fails):
────────────────────────────
Reserve    →    Charge ❌  →    Release      →    CANCELLED
Inventory       (FAILS)         Inventory
                               (COMPENSATE)
\`\`\`

**Two Saga Approaches:**

1. **Choreography**: Each service listens to events and knows what to do
2. **Orchestration**: A central "saga orchestrator" tells services what to do`,
          keyPoints: [
            "Sagas provide eventual consistency (not immediate)",
            "Every action needs a compensating action defined",
            "Orchestration is easier to understand and debug",
            "Choreography is more decoupled but harder to track"
          ]
        },
        {
          title: "The Outbox Pattern: Reliable Event Publishing",
          content: `**The Critical Problem Nobody Talks About:**

Look at this common code:

\`\`\`typescript
async createOrder(data) {
  // Step 1: Save to database
  const order = await this.db.orders.save(data);
  
  // Step 2: Publish event
  await this.messageQueue.publish('order_created', order);
  
  return order;
}
\`\`\`

**What if the app CRASHES between Step 1 and Step 2?**
- ✅ Order is saved in database
- ❌ Event is NEVER published
- ❌ Other services never know about the order
- ❌ Customer never gets confirmation email
- ❌ Inventory is never reserved

**This is called the "Dual Write Problem"** - you're writing to TWO systems (DB + Queue) without a transaction spanning both.

**The Solution: Outbox Pattern**

Instead of publishing directly to the queue, save the event to an "outbox" table IN THE SAME TRANSACTION as your business data.

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│                    OUTBOX PATTERN                                │
│                                                                  │
│  Order Service                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    SINGLE TRANSACTION                    │    │
│  │                                                          │    │
│  │  ┌──────────────────┐    ┌──────────────────┐           │    │
│  │  │   orders table   │    │   outbox table   │           │    │
│  │  │                  │    │                  │           │    │
│  │  │ INSERT order     │    │ INSERT event     │           │    │
│  │  │                  │    │ {                │           │    │
│  │  │                  │    │   type: 'order_  │           │    │
│  │  │                  │    │         created' │           │    │
│  │  │                  │    │   payload: {...} │           │    │
│  │  │                  │    │   published:false│           │    │
│  │  │                  │    │ }                │           │    │
│  │  └──────────────────┘    └────────┬─────────┘           │    │
│  │                                   │                      │    │
│  └───────────────────────────────────┼──────────────────────┘    │
│                                      │                           │
│                            ┌─────────▼─────────┐                 │
│                            │  Outbox Publisher │                 │
│                            │  (Background Job) │                 │
│                            │                   │                 │
│                            │  1. Poll outbox   │                 │
│                            │  2. Publish to MQ │                 │
│                            │  3. Mark published│                 │
│                            └─────────┬─────────┘                 │
│                                      │                           │
│                                      ▼                           │
│                            ┌───────────────────┐                 │
│                            │   Message Queue   │                 │
│                            └───────────────────┘                 │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**Implementation:**

\`\`\`typescript
// CORRECT: Using Outbox Pattern
async createOrder(data) {
  return await this.db.transaction(async (tx) => {
    // Both operations in SAME transaction
    const order = await tx.orders.save(data);
    
    await tx.outbox.save({
      eventType: 'order_created',
      aggregateId: order.id,
      payload: JSON.stringify(order),
      createdAt: new Date(),
      published: false
    });
    
    return order;
  });
  // If ANYTHING fails, BOTH are rolled back!
}

// Background job (runs every few seconds)
async publishOutboxEvents() {
  const unpublished = await this.db.outbox.find({ published: false });
  
  for (const event of unpublished) {
    try {
      await this.messageQueue.publish(event.eventType, event.payload);
      await this.db.outbox.update(event.id, { published: true });
    } catch (error) {
      // Will retry on next poll
      console.error('Failed to publish:', event.id);
    }
  }
}
\`\`\`

**Key Insight:** The outbox table acts as a reliable buffer. Even if the message queue is down, events are safely stored and will be published when it comes back.`,
          keyPoints: [
            "NEVER write to DB and message queue separately",
            "The outbox table guarantees at-least-once delivery",
            "Consumers must be idempotent (handle duplicates)",
            "Alternative: Use Change Data Capture (CDC) like Debezium"
          ]
        },
        {
          title: "Data Replication: Keeping Local Copies",
          content: `**The Scenario:**

Order Service displays orders with customer names. Customer data is owned by User Service.

**Option A: Call User Service every time (Bad for performance)**
\`\`\`
GET /orders/123 → Order Service → Call User Service → Return combined data
                                  (adds 50-200ms latency every time!)
\`\`\`

**Option B: Keep a local copy of what you need (Data Replication)**
\`\`\`
Order Service has its OWN table:
customer_cache: { userId, name, email }

Updates automatically via events from User Service
\`\`\`

**How It Works:**

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│                    DATA REPLICATION FLOW                         │
│                                                                  │
│  User Service (Source of Truth)                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ users: { id, name, email, address, phone, ... }         │    │
│  └────────────────────────────┬────────────────────────────┘    │
│                               │                                  │
│                     user_updated event                           │
│                     { userId, name, email }                      │
│                               │                                  │
│                               ▼                                  │
│                    ┌─────────────────┐                           │
│                    │  Message Queue  │                           │
│                    └────────┬────────┘                           │
│                             │                                    │
│         ┌───────────────────┼───────────────────┐               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Order     │    │  Shipping   │    │  Billing    │         │
│  │   Service   │    │   Service   │    │   Service   │         │
│  │             │    │             │    │             │         │
│  │ LOCAL COPY: │    │ LOCAL COPY: │    │ LOCAL COPY: │         │
│  │ {userId,    │    │ {userId,    │    │ {userId,    │         │
│  │  name}      │    │  name,      │    │  name,      │         │
│  │             │    │  address}   │    │  email}     │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                  │
│  Each service stores ONLY the fields it needs!                   │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**Implementation:**

\`\`\`typescript
// Order Service - Event Handler
@EventPattern('user_updated')
async handleUserUpdated(event: { userId: string; name: string; email: string }) {
  // Update our local cache
  await this.customerCache.upsert({
    userId: event.userId,
    name: event.name,
    // We only store what WE need
  });
}

// Now when we need customer name:
async getOrderWithCustomer(orderId: string) {
  const order = await this.orders.findOne(orderId);
  const customer = await this.customerCache.findOne(order.userId);
  // No network call! Local database read.
  return { ...order, customerName: customer.name };
}
\`\`\`

**Trade-offs:**

| Aspect | API Call | Data Replication |
|--------|----------|------------------|
| Latency | +50-200ms | ~0ms (local) |
| Availability | Depends on other service | Works offline |
| Consistency | Always current | Eventually consistent |
| Complexity | Simple | Need event handlers |
| Storage | None | Duplicate data |

**When to Use Data Replication:**
- ✅ Data changes infrequently (user names, product titles)
- ✅ You can tolerate slightly stale data
- ✅ High read volume
- ❌ NOT for frequently changing data (stock levels, prices)
- ❌ NOT when you need strong consistency`,
          keyPoints: [
            "Replicate ONLY the fields you need",
            "Always have a single source of truth",
            "Handle events idempotently (same event twice = same result)",
            "Consider cache invalidation strategies"
          ]
        },
        {
          title: "CQRS: Separate Reads from Writes",
          content: `**CQRS = Command Query Responsibility Segregation**

The idea: Use DIFFERENT models for reading and writing data.

**Why?**

In most apps, reads vastly outnumber writes (often 100:1). But we use the same database model for both, leading to compromises:
- Writes need normalized data (avoid duplication)
- Reads often need denormalized data (avoid JOINs)

**Traditional Approach (Same Model):**

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│                    TRADITIONAL (SAME MODEL)                      │
│                                                                  │
│    createOrder()  ──┐                                            │
│    updateOrder()  ──┼──►  orders table  ◄──┬── getOrder()       │
│    cancelOrder()  ──┘     (normalized)     └── listOrders()     │
│                                                                  │
│    Problem: Complex queries need JOINs across many tables        │
│    Problem: Can't optimize for both writes AND reads             │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**CQRS Approach (Separate Models):**

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│                    CQRS (SEPARATE MODELS)                        │
│                                                                  │
│    COMMAND SIDE                    QUERY SIDE                   │
│    (Writes)                        (Reads)                      │
│                                                                  │
│    createOrder() ──┐               ┌── getOrderDetails()        │
│    updateOrder() ──┼─►             ◄──┤                         │
│    cancelOrder() ──┘               └── searchOrders()           │
│                                                                  │
│         │                               │                        │
│         ▼                               ▼                        │
│    ┌─────────────┐    events      ┌─────────────┐               │
│    │ Write DB    │ ─────────────► │  Read DB    │               │
│    │ (normalized)│                │(denormalized)│               │
│    │             │                │              │               │
│    │ orders      │                │ order_views  │               │
│    │ order_items │                │ {            │               │
│    │ customers   │                │   orderId,   │               │
│    │ products    │                │   customer,  │               │
│    └─────────────┘                │   items,     │               │
│                                   │   total      │               │
│                                   │ }            │               │
│                                   └─────────────┘               │
│                                                                  │
│    Write DB: PostgreSQL           Read DB: MongoDB/Elasticsearch │
│    (Strong consistency)           (Optimized for queries)        │
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**The Sync Process:**

\`\`\`typescript
// When an order is created (Command side)
async createOrder(data) {
  const order = await this.writeDb.orders.save(data);
  
  // Publish event for read side to consume
  await this.events.publish('order_created', {
    orderId: order.id,
    customerId: order.customerId,
    items: order.items
  });
  
  return order;
}

// Read side event handler
@EventPattern('order_created')
async handleOrderCreated(event) {
  // Build denormalized view
  const customer = await this.customerCache.get(event.customerId);
  const products = await this.productCache.getMany(event.items.map(i => i.productId));
  
  await this.readDb.orderViews.save({
    orderId: event.orderId,
    customerName: customer.name,
    customerEmail: customer.email,
    items: event.items.map(item => ({
      name: products[item.productId].name,
      price: products[item.productId].price,
      quantity: item.quantity
    })),
    total: this.calculateTotal(event.items, products),
    createdAt: new Date()
  });
}
\`\`\`

**When to Use CQRS:**
- ✅ Complex queries that require many JOINs
- ✅ Different read/write scaling needs
- ✅ Event sourcing architectures
- ❌ Simple CRUD applications (overkill)
- ❌ When you need immediate consistency`,
          keyPoints: [
            "CQRS adds complexity - only use when needed",
            "Read models can use different databases (Elasticsearch, Redis)",
            "Accept eventual consistency between write and read models",
            "Often combined with Event Sourcing"
          ]
        },
        {
          title: "Event Sourcing: Store Events, Not State",
          content: `**Traditional Approach:**

Store the CURRENT state:
\`\`\`
orders table: { id: 1, status: 'shipped', total: 100 }
\`\`\`

If status changed from 'pending' → 'paid' → 'shipped', you only see 'shipped'. The history is LOST.

**Event Sourcing Approach:**

Store the EVENTS that led to current state:
\`\`\`
events table:
  { orderId: 1, type: 'OrderCreated', data: { total: 100 } }
  { orderId: 1, type: 'PaymentReceived', data: { amount: 100 } }
  { orderId: 1, type: 'OrderShipped', data: { trackingNo: 'XYZ' } }
\`\`\`

Current state = replay all events!

**Visual Comparison:**

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│               TRADITIONAL vs EVENT SOURCING                      │
│                                                                  │
│  TRADITIONAL (State):         EVENT SOURCING (Events):          │
│                                                                  │
│  ┌─────────────────┐         ┌─────────────────────────────┐   │
│  │ orders          │         │ events                       │   │
│  │                 │         │                              │   │
│  │ id: 1           │         │ 1. OrderCreated { total:100 }│   │
│  │ status: shipped │    ◄──  │ 2. PaymentReceived           │   │
│  │ total: 100      │  derive │ 3. ItemAdded { product: X }  │   │
│  │                 │         │ 4. ItemRemoved { product: Y }│   │
│  │                 │         │ 5. OrderShipped { track: Z } │   │
│  └─────────────────┘         └─────────────────────────────┘   │
│                                                                  │
│  ❌ History lost             ✅ Complete audit trail            │
│  ❌ "Why is total 100?"      ✅ Can answer any historical query │
│  ✅ Simple queries           ❌ Must replay to get current state│
└─────────────────────────────────────────────────────────────────┘
\`\`\`

**Key Concepts:**

1. **Event Store:** Append-only log of events
2. **Aggregate:** Entity that events apply to (e.g., Order)
3. **Projection:** Derived view from events (for queries)
4. **Replay:** Rebuild state by replaying events

**Implementation:**

\`\`\`typescript
// Event Store
class OrderEventStore {
  async append(orderId: string, event: OrderEvent) {
    await this.db.events.insert({
      aggregateId: orderId,
      type: event.type,
      data: event.data,
      version: event.version,
      timestamp: new Date()
    });
  }
  
  async getEvents(orderId: string): Promise<OrderEvent[]> {
    return this.db.events.find({ aggregateId: orderId })
      .orderBy('version', 'asc');
  }
}

// Rebuild state from events
class Order {
  private state: OrderState = { status: 'new', items: [], total: 0 };
  
  static async load(orderId: string, eventStore: OrderEventStore) {
    const order = new Order();
    const events = await eventStore.getEvents(orderId);
    
    for (const event of events) {
      order.apply(event);  // Replay each event
    }
    
    return order;
  }
  
  private apply(event: OrderEvent) {
    switch (event.type) {
      case 'OrderCreated':
        this.state.status = 'pending';
        break;
      case 'ItemAdded':
        this.state.items.push(event.data.item);
        this.state.total += event.data.item.price;
        break;
      case 'OrderShipped':
        this.state.status = 'shipped';
        break;
    }
  }
}
\`\`\`

**When to Use Event Sourcing:**
- ✅ Audit requirements (finance, healthcare)
- ✅ Need to answer "what happened and when"
- ✅ Complex domain with many state transitions
- ✅ Event replay for debugging or analytics
- ❌ Simple CRUD (massive overkill)
- ❌ When storage costs are a concern`,
          keyPoints: [
            "Events are immutable - NEVER delete or modify",
            "Current state is derived, not stored",
            "Usually combined with CQRS for efficient queries",
            "Kafka is excellent for event sourcing (retention + replay)"
          ]
        }
      ],
      codeExample: {
        title: "Saga Orchestrator Implementation",
        language: "typescript",
        filename: "order-saga.orchestrator.ts",
        code: `// ============================================
// SAGA ORCHESTRATOR: Manages order creation across services
// ============================================
// This coordinates the entire order flow:
// 1. Reserve inventory
// 2. Process payment
// 3. Create shipment
// If any step fails, compensating transactions run

interface OrderData {
  orderId: string;
  customerId: string;
  items: Array<{ productId: string; quantity: number }>;
  paymentMethod: string;
  shippingAddress: string;
}

class OrderSagaOrchestrator {
  private inventoryService: InventoryClient;
  private paymentService: PaymentClient;
  private shippingService: ShippingClient;

  async executeOrderSaga(order: OrderData): Promise<SagaResult> {
    console.log('🚀 Starting order saga for:', order.orderId);
    
    // Track what we've done (for rollback)
    const completedSteps: string[] = [];

    try {
      // ============================================
      // STEP 1: Reserve Inventory
      // ============================================
      console.log('📦 Step 1: Reserving inventory...');
      await this.inventoryService.reserveItems({
        orderId: order.orderId,
        items: order.items,
      });
      completedSteps.push('INVENTORY_RESERVED');
      console.log('✅ Inventory reserved successfully');

      // ============================================
      // STEP 2: Process Payment
      // ============================================
      console.log('💳 Step 2: Processing payment...');
      const paymentResult = await this.paymentService.charge({
        orderId: order.orderId,
        customerId: order.customerId,
        amount: order.totalAmount,
        method: order.paymentMethod,
      });
      completedSteps.push('PAYMENT_PROCESSED');
      console.log('✅ Payment processed:', paymentResult.transactionId);

      // ============================================
      // STEP 3: Create Shipment
      // ============================================
      console.log('🚚 Step 3: Creating shipment...');
      const shipment = await this.shippingService.createShipment({
        orderId: order.orderId,
        items: order.items,
        address: order.shippingAddress,
      });
      completedSteps.push('SHIPMENT_CREATED');
      console.log('✅ Shipment created:', shipment.trackingNumber);

      // ============================================
      // ALL STEPS COMPLETED!
      // ============================================
      console.log('🎉 Order saga completed successfully!');
      return {
        success: true,
        orderId: order.orderId,
        status: 'CONFIRMED',
        trackingNumber: shipment.trackingNumber,
      };

    } catch (error) {
      // ============================================
      // SOMETHING FAILED - RUN COMPENSATIONS
      // ============================================
      console.error('❌ Saga failed at step:', error.step);
      console.log('🔄 Running compensating transactions...');

      await this.compensate(order, completedSteps, error);

      return {
        success: false,
        orderId: order.orderId,
        status: 'CANCELLED',
        reason: error.message,
      };
    }
  }

  // Undo completed steps in reverse order
  private async compensate(
    order: OrderData, 
    completedSteps: string[],
    originalError: Error
  ) {
    // Process in reverse order
    const stepsToUndo = [...completedSteps].reverse();

    for (const step of stepsToUndo) {
      try {
        switch (step) {
          case 'SHIPMENT_CREATED':
            console.log('↩️ Cancelling shipment...');
            await this.shippingService.cancelShipment(order.orderId);
            console.log('✅ Shipment cancelled');
            break;

          case 'PAYMENT_PROCESSED':
            console.log('↩️ Refunding payment...');
            await this.paymentService.refund(order.orderId);
            console.log('✅ Payment refunded');
            break;

          case 'INVENTORY_RESERVED':
            console.log('↩️ Releasing inventory...');
            await this.inventoryService.releaseItems(order.orderId);
            console.log('✅ Inventory released');
            break;
        }
      } catch (compensationError) {
        // Log but continue - don't fail the compensation
        console.error('⚠️ Compensation failed for', step, compensationError);
        // This might need manual intervention later
        await this.alertOpsTeam(order.orderId, step, compensationError);
      }
    }
  }
}




// ============================================
// USAGE EXAMPLE:
// ============================================
//
// const saga = new OrderSagaOrchestrator();
// const result = await saga.executeOrderSaga({
//   orderId: 'ORD-12345',
//   customerId: 'USR-789',
//   items: [
//     { productId: 'PROD-001', quantity: 2 },
//     { productId: 'PROD-042', quantity: 1 },
//   ],
//   paymentMethod: 'credit_card',
//   shippingAddress: '123 Main St, City',
// });
//
// if (result.success) {
//   console.log('Order confirmed!', result.trackingNumber);
// } else {
//   console.log('Order failed:', result.reason);
// }
//
// ============================================`
      },
      nextSteps: `Understanding data patterns is crucial. Next, we'll build an API Gateway - the single entry point that routes requests to your microservices.`
    }
  }
];

// Add remaining modules with basic structure for brevity
// In production, each would have equally detailed content

const additionalModules = [
  {
    number: 8,
    slug: "api-gateway",
    title: "API Gateway Pattern",
    description: "Implement an API Gateway to handle cross-cutting concerns like authentication, rate limiting, and request routing.",
    difficulty: "intermediate",
    topics: ["Gateway Pattern", "Kong", "Express Gateway", "Authentication", "Rate Limiting", "Load Balancing"],
    learningOutcomes: [
      "Explain the purpose and benefits of an API Gateway",
      "Implement routing, rate limiting, and authentication at the gateway level",
      "Choose between different gateway solutions (Kong, Express Gateway)",
      "Understand BFF (Backend for Frontend) pattern"
    ],
    estimatedTime: "45-60 minutes",
    content: {
      intro: `Directly communicating with dozens of microservices is a nightmare for clients. 😱
      
Enter the **API Gateway** - the receptionist of your microservices architecture.

**The Problem:**
Without a gateway, a client (like a mobile app) has to:
- KNOW the address of every service (User, Product, Order services)
- Handle authentication for EVERY call
- Make 20 calls to build one screen
- Deal with protocol differences (gRPC, REST, AMQP)

**The Solution:**
The API Gateway sits between clients and services. It acts as a single entry point that handles:
1. **Routing** - Sending requests to the right service
2. **Aggregation** - Combining results from multiple services
3. **Authentication** - Verifying identity once
4. **Rate Limiting** - Protecting services from overload`,
      sections: [
        {
          title: "Core Functions of an API Gateway",
          content: `The API Gateway is more than just a proxy. It handles "cross-cutting concerns" - things that every service needs but shouldn't have to implement themselves.

**1. Request Routing:**
Client sends request to \`/api/users/123\`. Gateway looks up routing table and forwards to \`user-service:3000/users/123\`.

**2. Authentication Termination:**
Gateway checks the JWT token. If valid, it passes the request to services (often adding a "X-User-Id" header). Services blindly trust the gateway.

**3. Rate Limiting:**
"User X can only make 100 requests per minute". Gateway tracks this and returns 429 Too Many Requests if exceeded.

**4. Protocol Translation:**
Client speaks HTTP/JSON. Internal services speak gRPC (faster). Gateway translates between them.`,
          keyPoints: [
            "Gateway decouples clients from services",
            "Centralizes security and policy enforcement",
            "Reduces chatter for mobile clients (backend-for-frontend)",
            "Standardizes error responses"
          ]
        },
        {
          title: "Popular Gateway Tools",
          content: `You rarely build a gateway from scratch. You use battle-tested tools:

- **Kong:** Open-source, based on Nginx. Extremely popular and performant.
- **Traefik:** Cloud-native, integrates perfectly with Docker/Kubernetes.
- **NestJS (Custom):** You can build a custom gateway using NestJS logic (good for aggregation).
- **Apollo Gateway:** Best if you are using GraphQL federation.`,
          comparison: {
            monolith: {
              pros: ["No network hop latency", "Simple interface"],
              cons: ["Tight coupling", "Security scattered"]
            },
            microservices: {
              pros: ["Centralized security", "Can modify responses on the fly", "Hide internal architecture"],
              cons: ["Single point of failure (if not HA)", "Extra network hop adds latency"]
            }
          }
        }
      ],
      codeExample: {
        title: "Simple Gateway with NestJS",
        language: "typescript",
        filename: "gateway/app.module.ts",
        code: `// A simple gateway using http-proxy-middleware
// In production, use Kong or Nginx, but this shows the concept.

import { Module, MiddlewareConsumer, NestModule } from '@nestjs/common';
import { createProxyMiddleware } from 'http-proxy-middleware';

@Module({})
export class GatewayModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    
    // Route /users requests to User Service
    consumer
      .apply(createProxyMiddleware({
        target: 'http://user-service:3000',
        changeOrigin: true,
        pathRewrite: { '^/api/users': '' } // Remove /api prefix
      }))
      .forRoutes('/api/users');

    // Route /products requests to Product Service
    consumer
      .apply(createProxyMiddleware({
        target: 'http://product-service:3001',
        changeOrigin: true,
      }))
      .forRoutes('/api/products');
      
    // Route /orders requests to Order Service
    consumer
      .apply(createProxyMiddleware({
        target: 'http://order-service:3002',
        changeOrigin: true,
      }))
      .forRoutes('/api/orders');
  }
}`
      },
      nextSteps: `Now that we have a gateway, how do services find each other when IP addresses change? Next up: Service Discovery.`
    }
  },
  {
    number: 9,
    slug: "service-discovery",
    title: "Service Discovery",
    description: "Learn how services find each other in a dynamic environment using service discovery patterns and tools.",
    difficulty: "intermediate",
    topics: ["Why Service Discovery", "Consul", "Kubernetes DNS", "Health Checks", "Load Balancing", "Client-side vs Server-side"],
    learningOutcomes: [
      "Explain why static IPs don't work in microservices",
      "Implement service registration and discovery with Consul",
      "Use Kubernetes DNS for service discovery",
      "Differentiate client-side vs server-side discovery"
    ],
    estimatedTime: "45-60 minutes",
    content: {
      intro: `In the world of microservices, things move fast. Containers die, new ones are born, and IP addresses change constantly. 🏃‍♂️

**The Challenge:**
If Service A needs to call Service B, how does it know Service B's IP address?

Hardcoding IPs? \`http://192.168.1.50:3000\`? ❌
**NO!** That IP will change the next time you deploy.

**The Solution: Service Discovery**
Think of it like a phone book for your services.
1. **Registration:** When Service B starts, it calls the directory: "Hi, I'm Service B, my IP is 10.0.0.5".
2. **Discovery:** When Service A needs Service B, it asks the directory: "Where is Service B?".`,
      sections: [
        {
          title: "How It Works: The Registry",
          content: `The heart of service discovery is the **Service Registry**.

**Popular Registries:**
- **Consul:** HashiCorp's tool. Very popular.
- **Eureka:** Netflix's tool (Java heavy).
- **Etcd:** The brain of Kubernetes.
- **Kubernetes DNS:** If you use K8s, this is built-in!

**The Flow:**
1. **Startup:** Service B spins up.
2. **Register:** Service B sends heartbeat to Registry. "I'm alive at IP X".
3. **Health Check:** Registry pings Service B every 10s. If it fails, it removes B from the list.
4. **Lookup:** Service A asks Registry for "Service B". Registry returns list of healthy IPs.`,
          keyPoints: [
            "Never hardcode IP addresses in microservices",
            "Health checks ensure we don't send traffic to dead instances",
            "Client-side discovery: Client asks registry, then calls service",
            "Server-side discovery: Client calls load balancer, LB asks registry"
          ]
        },
        {
          title: "Kubernetes Service Discovery",
          content: `If you are deploying to Kubernetes (which you probably will), it makes this incredibly easy.

You don't need a separate tool like Consul. Kubernetes uses **DNS**.

If you have a service named \`my-product-service\`, ANY other container in the cluster can just call:
\`http://my-product-service\`

Kubernetes DNS automatically resolves that name to the Load Balancer IP of the service. Magic! ✨`,
          comparison: {
            monolith: {
              pros: ["Function calls are local", "No network addressing needed"],
              cons: ["Single codebase limit"]
            },
            microservices: {
              pros: ["Dynamic scaling", "Resilience (bad nodes removed automatically)"],
              cons: ["Complex infrastructure", "Need for a registry tool"]
            }
          }
        }
      ],
      codeExample: {
        title: "Connecting to a Service (Concept)",
        language: "typescript",
        filename: "consumer-service.ts",
        code: `// WITHOUT Service Discovery (Bad)
const response = await axios.get('http://10.20.30.40:3000/users');

// WITH Service Discovery (Good)
// The name 'user-service' resolves to the dynamic IP
const response = await axios.get('http://user-service/users');

// How it looks in Docker Compose/Kubernetes:
// The hostname matches the service name defined in YAML.

/*
// docker-compose.yml
services:
  user-service:   <-- This becomes the hostname
    image: my-user-service
    
  order-service:
    image: my-order-service
    environment:
      USER_SERVICE_URL: http://user-service:3000  <-- Easy!
*/`
      },
      nextSteps: `We have the concepts down. Now let's package our apps so they can run anywhere. Enter Docker.`
    }
  },
  {
    number: 10,
    slug: "docker",
    title: "Docker & Containerization",
    description: "Containerize your microservices with Docker. Learn Dockerfiles, Docker Compose, networking, and best practices.",
    difficulty: "intermediate",
    topics: ["Containers Basics", "Dockerfile", "Docker Compose", "Multi-stage Builds", "Networking", "Volumes"],
    learningOutcomes: [
      "Write efficient Dockerfiles with multi-stage builds",
      "Use Docker Compose for local development",
      "Understand container networking and volumes",
      "Apply Docker best practices for production"
    ],
    estimatedTime: "60-90 minutes",
    content: {
      intro: `**Docker** is the standard unit of deployment for microservices. 🐳

**Why?**
"It works on my machine" is the most famous developer excuse.
Docker solves this. If it works in Docker, it works ANYWHERE - your laptop, your colleague's laptop, AWS, Azure, Google Cloud.

**What is a Container?**
It's a lightweight package that contains EVERYTHING your app needs to run:
- Code
- Runtime (Node.js, Python)
- System libraries
- Settings

It isolates your app from the host OS.`,
      sections: [
        {
          title: "The Dockerfile",
          content: `The \`Dockerfile\` is a recipe for building your container image.

**Key Instructions:**
- \`FROM\`: Base image (e.g., \`node:18-alpine\`)
- \`WORKDIR\`: Where to put files inside container
- \`COPY\`: Copy files from host to container
- \`RUN\`: Run commands (like \`npm install\`)
- \`CMD\`: Command to start the app`,
          keyPoints: [
            "Use Alpine images for smaller size",
            "Order matters! Put frequently changed layers (code) last",
            "Multi-stage builds separate build tools from runtime",
            ".dockerignore is crucial to exclude node_modules"
          ]
        },
        {
          title: "Docker Compose: Running Multiple Services",
          content: `Microservices means MULTIPLE apps. specificyng \`docker run\` for 10 services is painful.

**Docker Compose** lets you define your entire system in one YAML file.

\`\`\`yaml
version: '3'
services:
  api-gateway:
    build: ./gateway
    ports: ["8080:8080"]
    
  user-service:
    build: ./users
    environment:
      - DB_HOST=postgres
      
  postgres:
    image: postgres:13
    volumes:
      - db_data:/var/lib/postgresql/data
\`\`\`

One command: \`docker-compose up\` starts EVERYTHING.`,
          comparison: {
            monolith: {
              pros: ["Easy to run", "One server needed"],
              cons: ["Dependency hell (e.g. conflicts between app library versions)"]
            },
            microservices: {
              pros: ["Environment consistency", "Isolation", "Easy CI/CD"],
              cons: ["Image management", "Overlay networking complexity"]
            }
          }
        }
      ],
      codeExample: {
        title: "Production-Ready Dockerfile",
        language: "dockerfile",
        filename: "Dockerfile",
        code: `# STAGE 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
# Install ALL dependencies (including devDependencies like TypeScript)
RUN npm install

COPY . .
# Build the NestJS app (creates dist folder)
RUN npm run build

# STAGE 2: Run
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
# Install ONLY production dependencies
RUN npm install --only=production

# Copy built code from builder stage
COPY --from=builder /app/dist ./dist

EXPOSE 3000

CMD ["node", "dist/main"]`
      },
      nextSteps: `Your apps are packaged. Now, how do we secure them? Next up: Authentication & Security.`
    }
  },
  {
    number: 11,
    slug: "authentication",
    title: "Authentication & Security",
    description: "Secure your microservices with JWT, OAuth2, API keys, and implement service-to-service authentication.",
    difficulty: "intermediate",
    topics: ["JWT Authentication", "OAuth2", "API Keys", "Service-to-Service Auth", "mTLS", "Security Best Practices"],
    learningOutcomes: [
      "Implement JWT-based authentication in microservices",
      "Secure service-to-service communication",
      "Apply OAuth2 flows for third-party integration",
      "Understand mTLS for zero-trust architectures"
    ],
    estimatedTime: "60-90 minutes",
    content: {
      intro: `Security in microservices is harder than in monoliths.
In a monolith, you log in once and the session is stored in memory.

In microservices:
- Services are stateless (no sessions!)
- Requests jump between 10 services
- How does Service C know who the user is?
- How do we prevent Service A from hacking Service B?

**The Golden Standard: JWT (JSON Web Tokens)**`,
      sections: [
        {
          title: "The Authentication Flow",
          content: `1. **Client** sends username/password to **Auth Service**.
2. **Auth Service** validates creds and signs a **JWT**.
3. **Client** stores JWT and sends it in \`Authorization: Bearer <token>\` header for ALL requests.
4. **API Gateway** validates the signature of the JWT.
5. **Gateway** passes the request to internal services, often attaching the decoded user ID in a header.

**Why JWT?**
It's stateless! The token *itself* contains the data (user ID, role). Services verify the cryptographic signature to trust it. No need to call the database for every request.`,
          keyPoints: [
            "Never implement your own crypto",
            "Use short expiration times for access tokens (e.g. 15 mins)",
            "Use Refresh Tokens to get new access tokens",
            "Service-to-Service auth can use mTLS (mutual TLS) for max security"
          ]
        },
        {
          title: "Service-to-Service Security",
          content: `It's not just about users. What if a hacker gets into your network? You don't want them calling your Payment Service directly.

**Defense in Depth:**
1. **Network Policies:** Only Order Service can talk to Payment Service (firewall rules).
2. **mTLS:** Services use certificates to prove their identity to each other.
3. **API Keys:** Simple but effective for internal services.`,
          comparison: {
            monolith: {
              pros: ["Simple session cookies", "One security boundary"],
              cons: ["If breached, everything is exposed"]
            },
            microservices: {
              pros: ["Zero Trust model", "Fine-grained access control"],
              cons: ["Complex token management", "Certificate rotation is hard"]
            }
          }
        }
      ],
      codeExample: {
        title: "JWT Strategy in NestJS",
        language: "typescript",
        filename: "auth/jwt.strategy.ts",
        code: `import { ExtractJwt, Strategy } from 'passport-jwt';
import { PassportStrategy } from '@nestjs/passport';
import { Injectable } from '@nestjs/common';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor() {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: 'YOUR_SECRET_KEY', // Use env vars in production!
    });
  }

  async validate(payload: any) {
    // This runs after the signature is verified valid
    // We return what we want available in request.user
    return { userId: payload.sub, username: payload.username };
  }
}

// PROTECTING A ROUTE
// @UseGuards(JwtAuthGuard)
// @Get('profile')
// getProfile(@Request() req) {
//   return req.user;
// }`
      },
      nextSteps: `Security: check. Now let's tackle the 800-pound gorilla of microservices: Kubernetes.`
    }
  },
  {
    number: 12,
    slug: "kubernetes",
    title: "Kubernetes Fundamentals",
    description: "Deploy and manage microservices on Kubernetes. Learn pods, deployments, services, ConfigMaps, and Helm.",
    difficulty: "advanced",
    topics: ["Kubernetes Basics", "Pods", "Deployments", "Services", "ConfigMaps & Secrets", "Ingress", "Helm Charts"],
    learningOutcomes: [
      "Deploy microservices to a Kubernetes cluster",
      "Use deployments, services, and ingress resources",
      "Manage configuration with ConfigMaps and Secrets",
      "Package applications with Helm charts"
    ],
    estimatedTime: "90-120 minutes",
    content: {
      intro: `**Kubernetes (K8s)** is the operating system for the cloud. ⚓️

Docker runs containers. Kubernetes runs **clusters** of containers.

**Why K8s?**
Imagine you have 50 microservices.
- Service A needs 3 copies (replicas).
- Service B needs 10 copies but only during daytime.
- One server dies. Who restarts the containers?
- How do you update without downtime?

Kubernetes handles all of this automatically.`,
      sections: [
        {
          title: "Key Concepts",
          content: `**1. Pod:**
The smallest unit. Usually one container (e.g. your node app). K8s manages Pods, not containers directly.

**2. Deployment:**
Manages connection of Pods. You verify: "I want 3 replicas of User Service". The Deployment ensures there are ALWAYS 3 running. If one crashes, it starts a new one immediately.

**3. Service:**
The stable network address. Pods appear and vanish (and change IPs). The Service gives a stable IP to front them.

**4. Ingress:**
The door to the outside world. Routes traffic from \`api.myapp.com\` to your internal services.`,
          keyPoints: [
            "K8s is declarative: You say WHAT you want, K8s makes it happen",
            "Everything is defined in YAML",
            "It automatically heals (restarts) failed containers",
            "It handles rolling updates with zero downtime"
          ]
        },
        {
          title: "The YAML Nightmare (and Salvation)",
          content: `Yes, K8s involves a lot of YAML. But it gives you superpowers.

**Self-Healing Example:**
You pull the plug on a server. K8s notices 5 pods are gone. It instantly schedules 5 new pods on the remaining healthy servers. You sleep through the night. 😴`,
          comparison: {
            monolith: {
              pros: ["Deploy to a single VPS", "Simple bash scripts"],
              cons: ["Manual scaling", "Downtime during updates"]
            },
            microservices: {
              pros: ["Infinite scaling", "Self-healing", "Infrastructure as Code"],
              cons: ["Steep learning curve", "Overkill for small apps"]
            }
          }
        }
      ],
      codeExample: {
        title: "Basic Deployment YAML",
        language: "yaml",
        filename: "deployment.yaml",
        code: `apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service-deployment
spec:
  replicas: 3  # We want 3 copies!
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
      - name: user-service
        image: my-registry/user-service:v1
        ports:
        - containerPort: 3000
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  selector:
    app: user-service
  ports:
    - port: 80
      targetPort: 3000`
      },
      nextSteps: `With great power comes great complexity. How do we know what's happening inside all these pods? Next up: Monitoring.`
    }
  },
  {
    number: 13,
    slug: "monitoring",
    title: "Monitoring & Observability",
    description: "Monitor your microservices with Prometheus, Grafana, distributed tracing with Jaeger, and centralized logging.",
    difficulty: "advanced",
    topics: ["Prometheus", "Grafana", "Distributed Tracing", "Jaeger", "ELK Stack", "Alerting"],
    learningOutcomes: [
      "Implement the three pillars of observability (logs, metrics, traces)",
      "Set up Prometheus and Grafana for metrics",
      "Use distributed tracing with Jaeger/Zipkin",
      "Centralize logs with ELK stack"
    ],
    estimatedTime: "60-90 minutes",
    content: {
      intro: `In a monolith, if something breaks, you check \`/var/log/syslog\`.
In microservices, you have 50 services, 3 replicas each... that's 150 logs. Where do you look? 🕵️‍♂️

**Observability** is about three pillars:
1. **Logs:** "What happened?" (Error: NullPointerException)
2. **Metrics:** "Is it happening a lot?" (CPU usage, requests/sec)
3. **Tracing:** "Where did it happen?" (User -> Gateway -> Order -> Payment ❌)`,
      sections: [
        {
          title: "The ELK Stack (Logs)",
          content: `**Elasticsearch, Logstash, Kibana.**
All your containers ship logs to a central server (Elasticsearch). You search them in Kibana.
Query: \`service:payment AND level:error\`. Boom, all payment errors in one place.`,
          keyPoints: [
            "Never log to a file in a container! Log to stdout (console)",
            "Centralize logs immediately",
            "Use correlation IDs to link logs across services"
          ]
        },
        {
          title: "Prometheus & Grafana (Metrics)",
          content: `**Prometheus** scrapes your services every 15s: "How much RAM are you using? How many 500 errors?"
**Grafana** visualize this data.

You build dashboards:
- "Red alert if 500 errors > 1% of traffic"
- "Warn if request latency > 200ms"`,
          comparison: null
        },
        {
          title: "Distributed Tracing (The Secret Weapon)",
          content: `A user reports "The checkout is slow".
With **Jaeger** or **Zipkin**, you see a timeline graph:

\`\`\`
Gateway: |--------- (200ms)
  Auth:  |-- (20ms)
  Order:    |---------------- (150ms)
    DB:     |---- (140ms!!!) <-- FOUND IT! Slow query.
\`\`\`

Without tracing, finding this bottleneck is guessing work.`,
          keyPoints: [
            "Tracing follows a request across service boundaries",
            "Requires passing a 'Trace ID' header in every HTTP call",
            "OpenTelemetry is the industry standard for this"
          ]
        }
      ],
      codeExample: {
        title: "Adding Prometheus Metrics (NestJS)",
        language: "typescript",
        filename: "app.module.ts",
        code: `import { Module } from '@nestjs/common';
import { PrometheusModule } from '@willsoto/nestjs-prometheus';

@Module({
  imports: [
    PrometheusModule.register({
      path: '/metrics', // Prometheus scrapes this URL
    }),
  ],
})
export class AppModule {}

// In your service:
// @InjectMetric('orders_total') 
// public counter: Counter<string>;
//
// this.counter.inc(); // +1 order`
      },
      nextSteps: `We can see everything now. But things will still break. Let's learn how to fail gracefully. Next up: Resilience Patterns.`
    }
  },
  {
    number: 14,
    slug: "resilience",
    title: "Resilience Patterns",
    description: "Build resilient microservices with circuit breakers, retries, bulkheads, and graceful degradation.",
    difficulty: "advanced",
    topics: ["Circuit Breaker", "Retry Pattern", "Timeout", "Bulkhead", "Fallback", "Health Checks"],
    learningOutcomes: [
      "Implement circuit breakers to prevent cascading failures",
      "Apply retry patterns with exponential backoff",
      "Use bulkheads to isolate failures",
      "Design graceful degradation strategies"
    ],
    estimatedTime: "60-90 minutes",
    content: {
      intro: `In distributed systems, failure is inevitable.
- Network glitches 🌐
- Database timeouts ⏱️
- Service crashes 💥

If Service A waits forever for Service B, Service A will eventually crash too (running out of threads). This is a **Cascading Failure**.

**Resilience Patterns** prevent one small failure from taking down the whole system.`,
      sections: [
        {
          title: "The Circuit Breaker Pattern",
          content: `Think of a literal electrical circuit breaker.
If the current is too high, it "trips" (opens) to stop the flow and prevent a fire.

**In Software:**
1. **Closed (Normal):** Requests flow to Service B.
2. **Open (Tripped):** Service B failed 5 times in a row. Stop sending requests! Fail fast immediately.
3. **Half-Open (Testing):** Wait 10s. Let 1 request through. If it works, close the circuit. If it fails, open it again.

**Why?**
It gives the failing service time to recover and prevents the caller from hanging.`,
          keyPoints: [
            "Use Circuit Breakers for all external calls",
            "Combine with **Retries** (for transient errors)",
            "Combine with **Timeouts** (don't wait forever)",
            "Implement **Fallbacks** (return cached data if service is down)"
          ]
        },
        {
          title: "Bulkhead Pattern",
          content: `Named after ship bulkheads. If a ship's hull is breached, water is contained in one section so the ship doesn't sink.

**In Software:**
Isolate resources (thread pools) so that if one feature is slow, it doesn't kill the app.
- Pool A: For "User Profile" requests
- Pool B: For "Image Upload" requests

If Image Upload is slow/stuck, Pool B fills up. But Pool A is free, so User Profile still works!`,
          comparison: null
        }
      ],
      codeExample: {
        title: "Circuit Breaker (NestJS)",
        language: "typescript",
        filename: "http-service.ts",
        code: `// Ideally use a library like 'opossum' or 'resilience4j'
import CircuitBreaker from 'opossum';

const breaker = new CircuitBreaker(asyncFetchFunction, {
  timeout: 3000, // If function takes longer than 3 seconds, trigger failure
  errorThresholdPercentage: 50, // When 50% of requests fail, trip the breaker
  resetTimeout: 30000 // After 30 seconds, try again
});

breaker.fallback(() => 'Service Unavailable (Fallback)');

// Usage
try {
  const result = await breaker.fire('http://slow-service/api');
  return result;
} catch (e) {
  // Circuit is open or service failed
  return "Cached Response";
}`
      },
      nextSteps: `We've built it, secured it, and made it tough. But does it actually work? Next up: Testing Strategies.`
    }
  },
  {
    number: 15,
    slug: "testing",
    title: "Testing Strategies",
    description: "Test your microservices effectively with unit tests, integration tests, contract testing, and end-to-end testing.",
    difficulty: "advanced",
    topics: ["Unit Testing", "Integration Testing", "Contract Testing", "Pact", "E2E Testing", "Test Containers"],
    learningOutcomes: [
      "Apply the test pyramid to microservices",
      "Use contract testing with Pact",
      "Write integration tests with TestContainers",
      "Design effective E2E testing strategies"
    ],
    estimatedTime: "60-90 minutes",
    content: {
      intro: `Testing microservices is HARD.
- Unit tests are easy.
- But how do you test if Service A works with Service B?
- Spinning up all 50 services for a test environment is slow and brittle.

We need a smarter strategy.`,
      sections: [
        {
          title: "The Testing Pyramid",
          content: `1. **Unit Tests (70%)**: Test logic inside a single class/function. Fast. mock everything else.
2. **Integration Tests (20%)**: Test a service with its database (use **TestContainers**!). Mock external APIs.
3. **E2E Tests (10%)**: Spin up the whole world and test critical user flows. Slow, flaky, expensive.

**The Missing Link: Contract Testing**
How do we ensure Service A and Service B speak the same language without running both?

**Contract Testing (Pact):**
Service A (Consumer) says: "I expect Service B to return { id: number }". This is a contract.
Service B (Provider) verifies: "Do I return { id: number }?".
If yes, they are compatible. No need to run them together!`,
          keyPoints: [
            "Don't rely heavily on E2E tests",
            "Use Service Virtualization (Mocks) for external dependencies",
            "Contract tests enable teams to deploy independently with confidence"
          ]
        },
        {
          title: "TestContainers",
          content: `Stop mocking your database in integration tests!
Use **TestContainers** to spin up a REAL Docker Postgres instance for your test suite.

\`\`\`typescript
// Starts a throwaway Postgres container
const pg = await new PostgreSqlContainer().start();
// Run tests...
await pg.stop();
\`\`\`

It ensures your SQL queries actually work against a real DB.`,
          comparison: null
        }
      ],
      codeExample: {
        title: "Integration Test with Supertest (NestJS)",
        language: "typescript",
        filename: "users.e2e-spec.ts",
        code: `import * as request from 'supertest';
import { Test } from '@nestjs/testing';
import { AppModule } from './../src/app.module';

describe('UsersController (e2e)', () => {
  let app;

  beforeAll(async () => {
    const moduleFixture = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  it('/users (POST)', () => {
    return request(app.getHttpServer())
      .post('/users')
      .send({ name: 'John', email: 'john@test.com' })
      .expect(201)
      .expect((res) => {
        expect(res.body.id).toBeDefined();
        expect(res.body.name).toEqual('John');
      });
  });
});`
      },
      nextSteps: `Code is tested. How do we get it to production without breaking things manually? Next up: CI/CD.`
    }
  },
  {
    number: 16,
    slug: "cicd",
    title: "CI/CD Pipelines",
    description: "Automate your microservices deployment with GitHub Actions, Jenkins, ArgoCD, and deployment strategies.",
    difficulty: "advanced",
    topics: ["GitHub Actions", "Jenkins", "ArgoCD", "GitOps", "Blue-Green Deployment", "Canary Releases"],
    learningOutcomes: [
      "Build CI/CD pipelines with GitHub Actions",
      "Implement GitOps with ArgoCD",
      "Use blue-green and canary deployment strategies",
      "Automate testing and security in pipelines"
    ],
    estimatedTime: "60-90 minutes",
    content: {
      intro: `CI/CD = Continuous Integration / Continuous Deployment.

**The Goal:**
Developer pushes code -> Magic happens -> Code is live in production.
(With zero downtime and full confidence).

**The Pipeline:**
1. **CI:** Build, lint, unit test.
2. **Publish:** Build Docker image, push to Registry.
3. **CD:** Update Kubernetes to use new image.`,
      sections: [
        {
          title: "Deployment Strategies",
          content: `You can't just "restart" the server. Users are using it!

**1. Rolling Update (Standard):**
K8s replaces pods one by one.
- v1, v1, v1
- v2, v1, v1
- v2, v2, v1
- v2, v2, v2

**2. Blue/Green:**
Spin up a full copy of the new version (Green) alongside old (Blue). Switch traffic instantly.
Pros: Instant rollback. Cons: Costs double resources.

**3. Canary Release:**
Send 1% of users to new version. Monitor errors. If good, increase to 10%, 50%, 100%.
Safest methods for big changes.`,
          keyPoints: [
            "Automate everything. No manual ssh.",
            "GitOps: Your infrastructure state is defined in Git (ArgoCD)",
            "Never deploy to prod on Friday evening! 😉"
          ]
        },
        {
          title: "GitOps with ArgoCD",
          content: `**Traditional CD:** Jenkins runs \`kubectl apply\`.

**GitOps (Modern):**
1. Jenkins updates \`deployment.yaml\` in a Git repo.
2. **ArgoCD** (running inside K8s) sees Git changed.
3. ArgoCD syncs the cluster to match Git.

This prevents "configuration drift". Git is the single source of truth.`,
          comparison: null
        }
      ],
      codeExample: {
        title: "GitHub Actions Workflow",
        language: "yaml",
        filename: ".github/workflows/deploy.yml",
        code: `name: Build and Deploy

on:
  push:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker Image
      run: docker build . -t myregistry/myapp:\${{ github.sha }}
      
    - name: Push Image
      run: docker push myregistry/myapp:\${{ github.sha }}
      
    - name: Update K8s Manifest
      run: |
        # Update the image tag in deployment.yaml
        sed -i "s|image: .*|image: myregistry/myapp:\${{ github.sha }}|" k8s/deployment.yaml
        
    - name: Commit & Push
      # ... git commit and push changes ...`
      },
      nextSteps: `We are almost there! Final module: Running in production.`
    }
  },
  {
    number: 17,
    slug: "production",
    title: "Production Deployment",
    description: "Deploy your microservices to production. Learn scaling strategies, cost optimization, and best practices checklist.",
    difficulty: "advanced",
    topics: ["Scaling Strategies", "Auto-scaling", "Cost Optimization", "Troubleshooting", "Best Practices", "Production Checklist"],
    learningOutcomes: [
      "Apply production-ready scaling strategies",
      "Implement auto-scaling based on metrics",
      "Optimize costs in cloud environments",
      "Follow the production deployment checklist"
    ],
    estimatedTime: "45-60 minutes",
    content: {
      intro: `Congratulations! You've made it to the end. 🎓
But building a system is easy. Keeping it running at 3am is hard.

This module is your **Launch Checklist**. Don't go live without it.`,
      sections: [
        {
          title: "Production Checklist",
          content: `**1. Security:**
- [ ] Are secrets (API keys) managed securely (Vault/Secrets Manager)?
- [ ] Is HTTPs/TLS enabled everywhere?
- [ ] Are you scanning images for vulnerabilities?

**2. Observability:**
- [ ] Can you see logs from all services in one place?
- [ ] Do you have alerts for critical failures?

**3. Resilience:**
- [ ] What happens if the database dies?
- [ ] What happens if S3 is down?

**4. Performance:**
- [ ] Have you load tested?
- [ ] Is Auto-scaling configured (HPA)?`,
          keyPoints: [
            "Document your runbooks (how to fix known issues)",
            "Practice 'Game Days' (simulate failures)",
            "Keep it simple. Boring architecture is good architecture."
          ]
        },
        {
          title: "Scaling Strategies",
          content: `**Horizontal Pod Autoscaling (HPA):**
Tell K8s: "If CPU > 70%, add more pods. If CPU < 30%, remove pods."

**Cluster Autoscaling:**
"If we run out of nodes (servers), add a new VM from AWS/GCP."

**Database Scaling:**
Read Replicas for read-heavy apps. Sharding for write-heavy apps (hard!).`,
          comparison: null
        }
      ],
      codeExample: {
        title: "Horizontal Pod Autoscaler",
        language: "yaml",
        filename: "hpa.yaml",
        code: `apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: user-service-hpa
spec:
  scaleTargetRef:
    kind: Deployment
    name: user-service
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70`
      },
      nextSteps: `You are now a Microservices Architect! Go build something amazing. 🚀`
    }
  },
];

// Add placeholder content for additional modules
// Add additional modules
additionalModules.forEach(mod => {
  // Only add placeholder if content is not already defined
  if (!mod.content) {
    mod.content = {
      intro: `This module is coming soon! We're adding detailed, step-by-step content for ${mod.title}.`,
      sections: [
        {
          title: "Content Coming Soon",
          content: `We're working on comprehensive content for this module. Check back soon!`,
          keyPoints: mod.topics.map(t => `Learn about ${t}`)
        }
      ],
      codeExample: {
        title: "Example Coming Soon",
        language: "typescript",
        filename: "example.ts",
        code: `// Detailed examples will be added for ${mod.title}`
      }
    };
  }
  modules.push(mod);
});

// Helper function to get module by slug
export function getModuleBySlug(slug) {
  return modules.find(m => m.slug === slug);
}

// Get all module slugs for static generation
export function getAllModuleSlugs() {
  return modules.map(m => m.slug);
}
