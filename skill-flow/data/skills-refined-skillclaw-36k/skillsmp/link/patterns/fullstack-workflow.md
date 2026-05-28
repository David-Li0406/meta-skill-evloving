# Full-Stack Feature Implementation Workflow

Step-by-step guide for implementing features that span both packages/web and packages/api.

## Prerequisites

- [ ] Feature requirements clear
- [ ] Database schema designed (if needed)
- [ ] API contract defined

## Phase 1: Backend (packages/api)

### Step 1: Database Schema
```typescript
// packages/api/src/db/schema/feature.ts
import { pgTable, text, timestamp, uuid } from "drizzle-orm/pg-core";
import { user } from "./auth";

export const feature = pgTable("feature", {
  id: uuid("id").primaryKey().defaultRandom(),
  userId: text("user_id").notNull().references(() => user.id),
  name: text("name").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export type Feature = typeof feature.$inferSelect;
export type NewFeature = typeof feature.$inferInsert;
```

**Actions:**
- [ ] Create schema file
- [ ] Export from `db/schema/index.ts`
- [ ] Generate migration: `bun run db:generate`
- [ ] Apply migration: `bun run db:migrate`

### Step 2: Repository Layer
```typescript
// packages/api/src/services/repository/feature.ts
import { db } from "../../db";
import { feature, type NewFeature } from "../../db/schema";
import { eq, and } from "drizzle-orm";
import type { RequestContext } from "../../types";

export class FeatureRepository {
  async findAll(ctx: RequestContext) {
    return db.query.feature.findMany({
      where: eq(feature.userId, ctx.userId),
      orderBy: (feature, { desc }) => [desc(feature.createdAt)],
    });
  }

  async findOne(ctx: RequestContext, id: string) {
    return db.query.feature.findFirst({
      where: and(
        eq(feature.id, id),
        eq(feature.userId, ctx.userId)
      ),
    });
  }

  async create(ctx: RequestContext, data: Omit<NewFeature, "userId">) {
    const [result] = await db.insert(feature)
      .values({ ...data, userId: ctx.userId })
      .returning();
    return result;
  }

  async update(ctx: RequestContext, id: string, data: Partial<NewFeature>) {
    const [result] = await db.update(feature)
      .set(data)
      .where(and(
        eq(feature.id, id),
        eq(feature.userId, ctx.userId)
      ))
      .returning();
    return result;
  }

  async delete(ctx: RequestContext, id: string) {
    await db.delete(feature)
      .where(and(
        eq(feature.id, id),
        eq(feature.userId, ctx.userId)
      ));
  }
}
```

**Actions:**
- [ ] Create repository class
- [ ] Implement CRUD methods
- [ ] Include `ctx` for user scoping
- [ ] Use singular table names

### Step 3: Business Service
```typescript
// packages/api/src/services/business/feature.ts
import { FeatureRepository } from "../repository/feature";
import { NotFoundException } from "../../utils/http-exceptions";
import type { RequestContext } from "../../types";
import type { NewFeature } from "../../db/schema";

export class FeatureService {
  constructor(private repo: FeatureRepository) {}

  async getAll(ctx: RequestContext) {
    return this.repo.findAll(ctx);
  }

  async getOne(ctx: RequestContext, id: string) {
    const item = await this.repo.findOne(ctx, id);
    if (!item) {
      throw new NotFoundException("Feature not found");
    }
    return item;
  }

  async create(ctx: RequestContext, data: Omit<NewFeature, "userId">) {
    // Add business logic here (validation, transformations, etc.)
    return this.repo.create(ctx, data);
  }

  async update(ctx: RequestContext, id: string, data: Partial<NewFeature>) {
    const existing = await this.getOne(ctx, id); // Validates existence
    return this.repo.update(ctx, id, data);
  }

  async delete(ctx: RequestContext, id: string) {
    await this.getOne(ctx, id); // Validates existence
    return this.repo.delete(ctx, id);
  }
}
```

**Actions:**
- [ ] Create service class
- [ ] Inject repository via constructor
- [ ] Add business logic validation
- [ ] Throw appropriate HTTP exceptions

### Step 4: Service Registration
```typescript
// packages/api/src/plugins/services.ts
import { FeatureRepository } from "../services/repository/feature";
import { FeatureService } from "../services/business/feature";

export const servicesPlugin = new Elysia({ name: "services" }).derive(
  { as: "global" },
  async () => {
    // ... existing services ...
    const featureRepo = new FeatureRepository();
    const featureService = new FeatureService(featureRepo);

    return {
      services: {
        // ... existing services ...
        featureRepo,
        featureService,
      },
    };
  },
);
```

**Actions:**
- [ ] Instantiate repository
- [ ] Instantiate service with repository
- [ ] Add to services return object

### Step 5: Route Handler
```typescript
// packages/api/src/api/routes/feature.ts
import { Elysia, t } from "elysia";
import { errorMiddleware } from "../../middleware/error";
import { servicesPlugin } from "../../plugins/services";
import { authGuard } from "../../middleware/auth-guard";

export const featureRoutes = new Elysia({ prefix: "/feature" })
  .use(errorMiddleware)
  .use(servicesPlugin)
  .use(authGuard)
  .get("/", ({ ctx, services }) => {
    return services.featureService.getAll(ctx!);
  })
  .get("/:id", ({ ctx, services, params }) => {
    return services.featureService.getOne(ctx!, params.id);
  }, {
    params: t.Object({
      id: t.String(),
    }),
  })
  .post("/", ({ body, ctx, services, set }) => {
    set.status = 201;
    return services.featureService.create(ctx!, body);
  }, {
    body: t.Object({
      name: t.String(),
    }),
  })
  .patch("/:id", ({ body, ctx, services, params }) => {
    return services.featureService.update(ctx!, params.id, body);
  }, {
    params: t.Object({
      id: t.String(),
    }),
    body: t.Partial(t.Object({
      name: t.String(),
    })),
  })
  .delete("/:id", ({ ctx, services, params, set }) => {
    services.featureService.delete(ctx!, params.id);
    set.status = 204;
  }, {
    params: t.Object({
      id: t.String(),
    }),
  });
```

**Actions:**
- [ ] Create route file
- [ ] Use errorMiddleware, servicesPlugin, authGuard
- [ ] Define Elysia type validators
- [ ] Set appropriate HTTP status codes

### Step 6: Register Route in App
```typescript
// packages/api/src/index.ts
import { featureRoutes } from "./api/routes/feature";

export const app = new Elysia()
  // ... existing middleware ...
  .use(featureRoutes) // Add this
  // ... existing routes ...
```

**Actions:**
- [ ] Import route
- [ ] Add `.use()` call

## Phase 2: Frontend (packages/web)

### Step 7: Custom Hook
```typescript
// packages/web/src/hooks/use-features.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { toast } from "sonner";

export function useFeatures() {
  return useQuery({
    queryKey: ["features"],
    queryFn: async () => {
      const { data, error } = await api.api.feature.get();
      if (error) throw error;
      return data;
    },
  });
}

export function useFeature(id: string) {
  return useQuery({
    queryKey: ["features", id],
    queryFn: async () => {
      const { data, error } = await api.api.feature[id].get();
      if (error) throw error;
      return data;
    },
    enabled: !!id,
  });
}

export function useCreateFeature() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (values: { name: string }) => {
      const { data, error } = await api.api.feature.post(values);
      if (error) throw error;
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["features"] });
      toast.success("Feature creada exitosamente");
    },
    onError: (error) => {
      toast.error(error.message || "Error al crear feature");
    },
  });
}

export function useUpdateFeature() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, data }: { id: string; data: { name?: string } }) => {
      const { data: result, error } = await api.api.feature[id].patch(data);
      if (error) throw error;
      return result;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["features"] });
      queryClient.invalidateQueries({ queryKey: ["features", variables.id] });
      toast.success("Feature actualizada exitosamente");
    },
    onError: (error) => {
      toast.error(error.message || "Error al actualizar feature");
    },
  });
}

export function useDeleteFeature() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string) => {
      const { error } = await api.api.feature[id].delete();
      if (error) throw error;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["features"] });
      toast.success("Feature eliminada exitosamente");
    },
    onError: (error) => {
      toast.error(error.message || "Error al eliminar feature");
    },
  });
}
```

**Actions:**
- [ ] Create hooks file
- [ ] Use edenTreaty API client
- [ ] Spanish toast messages
- [ ] Invalidate queries on mutations

### Step 8: Form Component
```typescript
// packages/web/src/components/features/feature-form.tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useCreateFeature } from "@/hooks/use-features";

const formSchema = z.object({
  name: z.string().min(2, { message: "Mínimo 2 caracteres" }),
});

type FormValues = z.infer<typeof formSchema>;

export function FeatureForm() {
  const { mutate, isPending } = useCreateFeature();

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
    },
  });

  function onSubmit(values: FormValues) {
    mutate(values);
    form.reset();
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Nombre</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" disabled={isPending}>
          {isPending ? "Guardando..." : "Guardar"}
        </Button>
      </form>
    </Form>
  );
}
```

**Actions:**
- [ ] Use react-hook-form + zod
- [ ] Spanish labels and messages
- [ ] Use shadcn/ui components
- [ ] Handle loading states

### Step 9: List Component
```typescript
// packages/web/src/components/features/feature-list.tsx
import { useFeatures, useDeleteFeature } from "@/hooks/use-features";
import { Button } from "@/components/ui/button";
import { Trash2 } from "lucide-react";

export function FeatureList() {
  const { data: features, isLoading } = useFeatures();
  const { mutate: deleteFeature } = useDeleteFeature();

  if (isLoading) {
    return <div>Cargando...</div>;
  }

  if (!features?.length) {
    return <div>No hay features</div>;
  }

  return (
    <div className="space-y-2">
      {features.map((feature) => (
        <div
          key={feature.id}
          className="flex items-center justify-between p-4 border rounded-lg"
        >
          <span>{feature.name}</span>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => deleteFeature(feature.id)}
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      ))}
    </div>
  );
}
```

**Actions:**
- [ ] Use custom hooks
- [ ] Spanish UI text
- [ ] Handle loading/empty states
- [ ] Use shadcn/ui components

### Step 10: Page Integration
```typescript
// packages/web/src/routes/dashboard/features.tsx
import { FeatureForm } from "@/components/features/feature-form";
import { FeatureList } from "@/components/features/feature-list";

export default function FeaturesPage() {
  return (
    <div className="container mx-auto py-8 space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Features</h1>
        <p className="text-muted-foreground">
          Gestiona tus features
        </p>
      </div>

      <FeatureForm />
      <FeatureList />
    </div>
  );
}
```

**Actions:**
- [ ] Create page route
- [ ] Use theme-aware classes
- [ ] Spanish text
- [ ] Compose components

## Testing Checklist

- [ ] Backend compiles without errors
- [ ] Database migration applied
- [ ] API endpoints respond correctly (test with curl/Postman)
- [ ] Frontend compiles without errors
- [ ] Type safety verified (no `any` warnings)
- [ ] UI displays data correctly
- [ ] Forms validate properly
- [ ] CRUD operations work end-to-end
- [ ] Error handling works (try invalid data)
- [ ] Authentication required (test without auth)
- [ ] Spanish text everywhere in UI

## Common Pitfalls

1. **Forgot to register service** in `plugins/services.ts`
2. **Used plural table names** instead of singular
3. **Forgot to invalidate queries** after mutations
4. **Used English** in UI instead of Spanish
5. **Hardcoded colors** instead of CSS variables
6. **Missing `ctx!` assertion** in route handlers
7. **Forgot to export** types from schema
8. **Relative imports** instead of `@/` alias in web
