# Config Templates

Create the following config files in `apps/web/`:

## wrangler.jsonc

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "<project-name>",
  "compatibility_date": "2024-01-01",
  "main": ".output/server/index.mjs",
  "assets": {
    "directory": ".output/public"
  },
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "<project-name>-db",
      "database_id": "<database-id>"
    }
  ],
  "r2_buckets": [
    {
      "binding": "BUCKET",
      "bucket_name": "<project-name>-bucket"
    }
  ]
}
```

## drizzle.config.ts

```typescript
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: "./src/infra/schema/*.ts",
  out: "./drizzle",
  dialect: "sqlite",
  driver: "d1-http",
});
```

## vitest.config.ts

```typescript
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "node",
  },
});
```

## .env.example

```bash
# Google OAuth
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# Better Auth
BETTER_AUTH_SECRET=

# Cloudflare
CLOUDFLARE_ACCOUNT_ID=
CLOUDFLARE_API_TOKEN=
```

## Cloudflare Resources

```bash
wrangler d1 create <project-name>-db
wrangler r2 bucket create <project-name>-bucket
```

After creating D1 database, update `database_id` in wrangler.jsonc.
