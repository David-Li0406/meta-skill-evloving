---
name: clean-architecture-ts
description: Use this skill when implementing Clean Architecture in Remix/TypeScript apps to ensure separation of concerns and maintainable code structure.
---

# Clean Architecture for Remix/TypeScript Apps

As Remix apps grow, `loader` and `action` functions can become bloated "God Functions". This skill emphasizes separation of concerns.

## 1. The Layers

### A. The Web Layer (Loaders/Actions)
**Responsibility**: Parsing requests, input validation (Zod), and returning Responses (JSON/Redirect).  
**Rule**: NO business logic here. Only orchestration.

```typescript
// app/routes/app.products.update.ts
export const action = async ({ request }: ActionFunctionArgs) => {
  const { shop } = await authenticate.admin(request);
  const formData = await request.formData();
  
  // 1. Validate Input
  const input = validateProductUpdate(formData);

  // 2. Call Service
  const updatedProduct = await ProductService.updateProduct(shop, input);

  // 3. Return Response
  return json({ product: updatedProduct });
};
```

### B. The Service Layer (Business Logic)
**Responsibility**: The "What". Rules, calculations, error handling, complex flows.  
**Rule**: Framework agnostic. Should not know about "Request" or "Response" objects.

```typescript
// app/services/product.service.ts
export class ProductService {
  static async updateProduct(shop: string, input: ProductUpdateInput) {
    // Business Rule: Can't update archived products
    const existing = await ProductRepository.findByShopAndId(shop, input.id);
    if (existing.status === 'ARCHIVED') {
      throw new BusinessError("Cannot update archived product");
    }

    // Business Logic
    const result = await ProductRepository.save({
      ...existing,
      ...input,
      updatedAt: new Date()
    });

    return result;
  }
}
```

### C. The Repository Layer (Data Access)
**Responsibility**: The "How". Interaction with Database (Prisma), APIs (Shopify Admin), or File System.  
**Rule**: Only this layer touches the DB/API.

```typescript
// app/repositories/product.repository.ts
export class ProductRepository {
  static async findByShopAndId(shop: string, id: string) {
    return prisma.product.findFirstOrThrow({
      where: { shop, id: BigInt(id) }
    });
  }
}
```

## 2. Directory Structure

```
app/
  routes/         # Web Layer
  services/       # Business Logic
  repositories/   # Data Access (DB/API)
  models/         # Domain Types / Interfaces
  utils/          # Pure functions
```