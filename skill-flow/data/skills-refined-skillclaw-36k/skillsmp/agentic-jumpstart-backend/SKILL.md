---
name: agentic-jumpstart-backend
description: Backend development patterns for TanStack Start with server functions, middleware, Zod validation, and Nitro. Use when creating API endpoints, server functions, handling authentication, processing webhooks, file uploads, or when the user mentions backend, API, server, endpoint, or middleware.
---

# Backend Development Patterns

## Server Functions

### Standard Pattern

Server functions require: middleware, input validator, and should call use cases (not data-access directly).

```typescript
import { createServerFn } from "@tanstack/react-start";
import { authenticatedMiddleware } from "~/lib/auth";
import { z } from "zod";
import { updateUserUseCase } from "~/use-cases/users";

export const updateUserFn = createServerFn()
  .middleware([authenticatedMiddleware])
  .inputValidator(
    z.object({
      name: z.string().min(1).max(100),
      bio: z.string().max(500).optional(),
    })
  )
  .handler(async ({ data, context }) => {
    return updateUserUseCase(context.userId, data);
  });
```

### Naming Convention

- Server functions: `verbNounFn` (e.g., `updateUserFn`, `getSegmentsFn`)
- Export from `/src/fn/` directory

### Middleware Options

```typescript
import {
  authenticatedMiddleware,  // Requires authenticated user
  adminMiddleware,          // Requires admin permission
  unauthenticatedMiddleware, // Optional auth (userId may be undefined)
} from "~/lib/auth";

// For authenticated users
export const protectedFn = createServerFn()
  .middleware([authenticatedMiddleware])
  .handler(async ({ context }) => {
    // context.userId is guaranteed
    // context.isAdmin is boolean
    // context.email is string
  });

// For admin only
export const adminFn = createServerFn()
  .middleware([adminMiddleware])
  .handler(async ({ context }) => {
    // Only admins can access
  });

// For public with optional user
export const publicFn = createServerFn()
  .middleware([unauthenticatedMiddleware])
  .handler(async ({ context }) => {
    // context.userId may be undefined
    // context.user may be undefined
  });
```

### POST Method for Mutations

Use POST for mutations that modify data:

```typescript
export const createSegmentFn = createServerFn({ method: "POST" })
  .middleware([adminMiddleware])
  .inputValidator(segmentCreateSchema)
  .handler(async ({ data }) => {
    return createSegmentUseCase(data);
  });
```

## Input Validation

### Common Zod Schemas

```typescript
import { z } from "zod";

// ID validation
const idSchema = z.number().int().positive();

// Pagination
const paginationSchema = z.object({
  page: z.number().int().min(1).default(1),
  limit: z.number().int().min(1).max(100).default(20),
});

// Search with pagination
const searchSchema = z.object({
  query: z.string().max(200).optional(),
  ...paginationSchema.shape,
});

// Date range
const dateRangeSchema = z.object({
  start: z.string().datetime(),
  end: z.string().datetime(),
});

// Segment update
const segmentUpdateSchema = z.object({
  segmentId: z.number(),
  field: z.enum(["summary", "content", "transcripts"]),
  value: z.string(),
});
```

### Array Validation

```typescript
export const reorderSegmentsFn = createServerFn()
  .middleware([adminMiddleware])
  .inputValidator(
    z.array(
      z.object({
        id: z.number(),
        order: z.number(),
      })
    )
  )
  .handler(async ({ data }) => {
    return reorderSegmentsUseCase(data);
  });
```

## Calling Server Functions

Always pass data via the `data` property:

```typescript
// Correct
const result = await getSegmentFn({ data: { id: segmentId } });

// Incorrect - don't do this
// const result = await getSegmentFn({ id: segmentId });
```

## File Uploads with Presigned URLs

### Generate Upload URL

```typescript
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { PutObjectCommand } from "@aws-sdk/client-s3";

export const getUploadUrlFn = createServerFn({ method: "POST" })
  .middleware([authenticatedMiddleware])
  .inputValidator(
    z.object({
      fileName: z.string().max(255),
      contentType: z.string(),
      fileSize: z.number().max(500 * 1024 * 1024), // 500MB max
    })
  )
  .handler(async ({ data, context }) => {
    const key = `uploads/${context.userId}/${Date.now()}-${data.fileName}`;

    const command = new PutObjectCommand({
      Bucket: env.R2_BUCKET_NAME,
      Key: key,
      ContentType: data.contentType,
      ContentLength: data.fileSize,
    });

    const url = await getSignedUrl(s3Client, command, { expiresIn: 3600 });

    return { uploadUrl: url, fileKey: key };
  });
```

### Generate Download URL

```typescript
import { GetObjectCommand } from "@aws-sdk/client-s3";

export const getDownloadUrlFn = createServerFn()
  .middleware([authenticatedMiddleware])
  .inputValidator(z.object({ fileKey: z.string() }))
  .handler(async ({ data }) => {
    const command = new GetObjectCommand({
      Bucket: env.R2_BUCKET_NAME,
      Key: data.fileKey,
    });

    return getSignedUrl(s3Client, command, { expiresIn: 3600 });
  });
```

## Webhook Handling

### Stripe Webhook Pattern

```typescript
// src/routes/api/stripe/webhook.ts
import Stripe from "stripe";

export const Route = createAPIFileRoute("/api/stripe/webhook")({
  POST: async ({ request }) => {
    const body = await request.text();
    const signature = request.headers.get("stripe-signature");

    if (!signature) {
      return new Response("Missing signature", { status: 400 });
    }

    const stripe = new Stripe(env.STRIPE_SECRET_KEY);

    try {
      const event = stripe.webhooks.constructEvent(
        body,
        signature,
        env.STRIPE_WEBHOOK_ENDPOINT_SECRET
      );

      switch (event.type) {
        case "checkout.session.completed":
          await handleCheckoutComplete(event.data.object);
          break;
        case "customer.subscription.updated":
          await handleSubscriptionUpdate(event.data.object);
          break;
        case "customer.subscription.deleted":
          await handleSubscriptionDelete(event.data.object);
          break;
      }

      return new Response("OK", { status: 200 });
    } catch (err) {
      console.error("Webhook error:", err);
      return new Response("Webhook error", { status: 400 });
    }
  },
});
```

## Error Handling

### PublicError Pattern

```typescript
// src/use-cases/errors.ts
export class PublicError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "PublicError";
  }
}

export class NotFoundError extends PublicError {
  constructor(resource: string) {
    super(`${resource} not found`);
    this.name = "NotFoundError";
  }
}

export class UnauthorizedError extends PublicError {
  constructor(message = "Unauthorized") {
    super(message);
    this.name = "UnauthorizedError";
  }
}
```

### Using Errors in Use Cases

```typescript
export async function getSegmentByIdUseCase(id: number) {
  const segment = await getSegmentById(id);
  if (!segment) {
    throw new NotFoundError("Segment");
  }
  return segment;
}
```

## Email Sending

### Using AWS SES

```typescript
import { SESClient, SendEmailCommand } from "@aws-sdk/client-ses";

const sesClient = new SESClient({ region: env.AWS_REGION });

export async function sendEmail({
  to,
  subject,
  html,
}: {
  to: string;
  subject: string;
  html: string;
}) {
  const command = new SendEmailCommand({
    Source: env.EMAIL_FROM,
    Destination: { ToAddresses: [to] },
    Message: {
      Subject: { Data: subject },
      Body: { Html: { Data: html } },
    },
  });

  return sesClient.send(command);
}
```

### React Email Templates

```typescript
import { render } from "@react-email/render";
import { WelcomeEmail } from "~/emails/WelcomeEmail";

export async function sendWelcomeEmail(user: User) {
  const html = await render(<WelcomeEmail name={user.name} />);

  await sendEmail({
    to: user.email,
    subject: "Welcome!",
    html,
  });
}
```

## OpenAI Integration

```typescript
import OpenAI from "openai";

const openai = new OpenAI({ apiKey: env.OPENAI_API_KEY });

export async function generateSummary(content: string): Promise<string> {
  const response = await openai.chat.completions.create({
    model: "gpt-4-turbo-preview",
    messages: [
      { role: "system", content: "Summarize the following content briefly." },
      { role: "user", content },
    ],
    max_tokens: 500,
  });

  return response.choices[0]?.message?.content ?? "";
}
```

## Backend Checklist

- [ ] Server functions use appropriate middleware
- [ ] Input is validated with Zod schemas
- [ ] Server functions call use cases, not data-access
- [ ] POST method used for mutations
- [ ] Data passed via `data` property when calling
- [ ] File uploads use presigned URLs
- [ ] Webhooks verify signatures
- [ ] Errors use PublicError pattern
- [ ] Sensitive operations require admin middleware
- [ ] Functions follow `verbNounFn` naming convention
