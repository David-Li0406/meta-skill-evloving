# Better Auth Setup Guide

Complete setup instructions for Better Auth with Next.js 15+, Node.js, and FastAPI backends.

## Prerequisites

- Node.js 18+
- Next.js 15+ or React 18+
- Database (PostgreSQL, MySQL, or MongoDB)
- Python 3.9+ (for FastAPI)

## Installation

### Next.js 15+ Frontend

```bash
npm install better-auth
```

### Node.js Backend

```bash
npm install better-auth
npm install -D @types/node
```

### FastAPI Backend

```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

## Environment Variables

Create `.env.local` (Next.js) or `.env` (backend):

```env
# Database (choose one)
# PostgreSQL
DATABASE_URL="postgresql://user:password@localhost:5432/dbname"

# MySQL
DATABASE_URL="mysql://user:password@localhost:3306/dbname"

# MongoDB
DATABASE_URL="mongodb://localhost:27017/dbname"

# Better Auth
BETTER_AUTH_SECRET="your-secret-key-min-32-chars"
BETTER_AUTH_URL="http://localhost:3000" # Your app URL

# OAuth (optional)
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"
GITHUB_CLIENT_ID="your-github-client-id"
GITHUB_CLIENT_SECRET="your-github-client-secret"
```

## Next.js 15+ Setup

### 1. Create Auth Configuration

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";
import { prisma } from "@/lib/prisma";

export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: "postgresql", // or "mysql" or "mongodb"
  }),
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Set to true in production
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
  },
});

export type Session = typeof auth.$Infer.Session;
```

### 2. Create API Route Handler

```typescript
// app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

### 3. Create Auth Client

```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
});

export const {
  signIn,
  signUp,
  signOut,
  useSession,
  user,
} = authClient;
```

### 4. Add Session Provider

```typescript
// app/layout.tsx
import { SessionProvider } from "@/lib/auth-client";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <SessionProvider>
          {children}
        </SessionProvider>
      </body>
    </html>
  );
}
```

## Node.js/Express Backend Setup

### 1. Initialize Better Auth

```typescript
// src/auth.ts
import { betterAuth } from "better-auth";
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

export const auth = betterAuth({
  database: {
    provider: "postgresql",
    pool,
  },
  emailAndPassword: {
    enabled: true,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
  },
});
```

### 2. Create Express Middleware

```typescript
// src/middleware/auth.ts
import { Request, Response, NextFunction } from "express";
import { auth } from "../auth";

export async function requireAuth(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const session = await auth.api.getSession({
    headers: req.headers,
  });

  if (!session) {
    return res.status(401).json({ error: "Unauthorized" });
  }

  req.user = session.user;
  req.session = session.session;
  next();
}

// Extend Express Request type
declare global {
  namespace Express {
    interface Request {
      user?: any;
      session?: any;
    }
  }
}
```

### 3. Setup Auth Routes

```typescript
// src/routes/auth.ts
import express from "express";
import { auth } from "../auth";

const router = express.Router();

router.post("/signup", async (req, res) => {
  const result = await auth.api.signUpEmail({
    body: req.body,
    headers: req.headers,
  });

  return res.json(result);
});

router.post("/signin", async (req, res) => {
  const result = await auth.api.signInEmail({
    body: req.body,
    headers: req.headers,
  });

  return res.json(result);
});

router.post("/signout", async (req, res) => {
  await auth.api.signOut({
    headers: req.headers,
  });

  return res.json({ success: true });
});

router.get("/session", async (req, res) => {
  const session = await auth.api.getSession({
    headers: req.headers,
  });

  return res.json(session);
});

export default router;
```

### 4. Setup Express Server

```typescript
// src/index.ts
import express from "express";
import cors from "cors";
import authRoutes from "./routes/auth";
import { requireAuth } from "./middleware/auth";

const app = express();

app.use(cors({
  origin: process.env.CLIENT_URL,
  credentials: true,
}));
app.use(express.json());

// Auth routes
app.use("/api/auth", authRoutes);

// Protected route example
app.get("/api/protected", requireAuth, (req, res) => {
  res.json({ user: req.user });
});

app.listen(3001, () => {
  console.log("Server running on http://localhost:3001");
});
```

## FastAPI Backend Setup

### 1. Create Auth Configuration

```python
# app/auth.py
from better_auth import BetterAuth
from better_auth.adapters import SQLAlchemyAdapter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

auth = BetterAuth(
    database=SQLAlchemyAdapter(engine),
    email_and_password={
        "enabled": True,
        "require_email_verification": False,
    },
    session={
        "expires_in": 60 * 60 * 24 * 7,  # 7 days
    },
    secret=os.getenv("BETTER_AUTH_SECRET"),
)
```

### 2. Create Auth Dependencies

```python
# app/dependencies.py
from fastapi import Depends, HTTPException, status, Request
from app.auth import auth
from typing import Optional

async def get_current_user(request: Request):
    """Dependency to get current authenticated user"""
    session = await auth.get_session(headers=dict(request.headers))

    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    return session["user"]

async def get_optional_user(request: Request) -> Optional[dict]:
    """Dependency to get user if authenticated, None otherwise"""
    try:
        session = await auth.get_session(headers=dict(request.headers))
        return session["user"] if session else None
    except:
        return None
```

### 3. Create Auth Routes

```python
# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, EmailStr
from app.auth import auth

router = APIRouter(prefix="/auth", tags=["auth"])

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup")
async def signup(data: SignUpRequest, request: Request):
    try:
        result = await auth.sign_up_email(
            email=data.email,
            password=data.password,
            name=data.name,
            headers=dict(request.headers),
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/signin")
async def signin(data: SignInRequest, request: Request):
    try:
        result = await auth.sign_in_email(
            email=data.email,
            password=data.password,
            headers=dict(request.headers),
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/signout")
async def signout(request: Request):
    await auth.sign_out(headers=dict(request.headers))
    return {"success": True}

@router.get("/session")
async def get_session(request: Request):
    session = await auth.get_session(headers=dict(request.headers))
    return session
```

### 4. Setup FastAPI Application

```python
# app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth
from app.dependencies import get_current_user

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")

# Protected route example
@app.get("/api/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"user": user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Database Setup

### PostgreSQL with Prisma (Next.js)

```bash
npm install prisma @prisma/client
npx prisma init
```

```prisma
// prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id            String    @id @default(uuid())
  email         String    @unique
  emailVerified Boolean   @default(false)
  name          String?
  image         String?
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
  sessions      Session[]
  accounts      Account[]
  passwords     Password?
  roles         UserRole[]
}

model Session {
  id        String   @id @default(uuid())
  userId    String
  expiresAt DateTime
  token     String   @unique
  ipAddress String?
  userAgent String?
  createdAt DateTime @default(now())
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
  @@index([token])
}

model Account {
  id                String   @id @default(uuid())
  userId            String
  accountId         String
  provider          String
  providerAccountId String
  accessToken       String?
  refreshToken      String?
  expiresAt         DateTime?
  tokenType         String?
  scope             String?
  idToken           String?
  createdAt         DateTime @default(now())
  updatedAt         DateTime @updatedAt
  user              User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([provider, providerAccountId])
  @@index([userId])
}

model Password {
  userId         String   @id
  hashedPassword String
  createdAt      DateTime @default(now())
  updatedAt      DateTime @updatedAt
  user           User     @relation(fields: [userId], references: [id], onDelete: Cascade)
}
```

```bash
npx prisma migrate dev --name init
npx prisma generate
```

### MongoDB with Mongoose (Node.js)

```bash
npm install mongoose
```

```typescript
// src/models/User.ts
import mongoose from "mongoose";

const userSchema = new mongoose.Schema({
  id: { type: String, required: true, unique: true },
  email: { type: String, required: true, unique: true },
  emailVerified: { type: Boolean, default: false },
  name: String,
  image: String,
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now },
});

export const User = mongoose.model("User", userSchema);
```

## Testing the Setup

### Test Authentication Flow

```bash
# Signup
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123","name":"Test User"}'

# Signin
curl -X POST http://localhost:3000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Get session
curl http://localhost:3000/api/auth/session \
  -H "Cookie: session=YOUR_SESSION_TOKEN"
```

## Troubleshooting

### Common Issues

1. **Database connection errors**
   - Verify DATABASE_URL is correct
   - Ensure database is running
   - Check firewall settings

2. **CORS errors**
   - Verify CLIENT_URL in backend
   - Enable credentials in CORS config

3. **Session not persisting**
   - Check cookie settings
   - Verify secure/sameSite attributes
   - Check domain configuration

4. **OAuth not working**
   - Verify client IDs and secrets
   - Check redirect URLs in provider settings
   - Ensure callback URL is correctly configured

## Next Steps

- See [api-patterns.md](api-patterns.md) for authentication endpoint patterns
- See [client-patterns.md](client-patterns.md) for frontend integration
- See [rbac-guide.md](rbac-guide.md) for role-based access control
