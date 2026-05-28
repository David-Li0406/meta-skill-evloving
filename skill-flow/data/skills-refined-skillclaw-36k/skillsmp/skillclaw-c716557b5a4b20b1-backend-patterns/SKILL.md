---
name: backend-patterns
description: Use this skill when you need to implement backend architecture patterns, API design, database optimization, and server-side best practices for scalable applications using Node.js, Express, Next.js, Django, FastAPI, or Flask.
---

# Backend Development Patterns

Backend architecture patterns and best practices for scalable server-side applications.

## API Design Patterns

### RESTful API Structure

```typescript
// ✅ Resource-based URLs
GET    /api/markets                 # List resources
GET    /api/markets/:id             # Get single resource
POST   /api/markets                 # Create resource
PUT    /api/markets/:id             # Replace resource
PATCH  /api/markets/:id             # Update resource
DELETE /api/markets/:id             # Delete resource

// ✅ Query parameters for filtering, sorting, pagination
GET /api/markets?status=active&sort=volume&limit=20&offset=0
```

### Repository Pattern

```typescript
// Abstract data access logic
interface MarketRepository {
  findAll(filters?: MarketFilters): Promise<Market[]>;
  findById(id: string): Promise<Market | null>;
  create(data: CreateMarketDto): Promise<Market>;
  update(id: string, data: UpdateMarketDto): Promise<Market>;
  delete(id: string): Promise<void>;
}

class SupabaseMarketRepository implements MarketRepository {
  async findAll(filters?: MarketFilters): Promise<Market[]> {
    let query = supabase.from('markets').select('*');

    if (filters?.status) {
      query = query.eq('status', filters.status);
    }

    if (filters?.limit) {
      query = query.limit(filters.limit);
    }

    const { data, error } = await query;

    if (error) throw new Error(error.message);
    return data;
  }

  // Other methods...
}
```

### Service Layer Pattern

```typescript
// Business logic separated from data access
class MarketService {
  constructor(private marketRepo: MarketRepository) {}

  async searchMarkets(query: string, limit: number = 10): Promise<Market[]> {
    // Business logic
    const embedding = await generateEmbedding(query);
    const results = await this.vectorSearch(embedding, limit);

    // Fetch full data
    const markets = await this.marketRepo.findByIds(results.map(r => r.id));

    // Sort by similarity
    return markets.sort((a, b) => {
      const scoreA = results.find(r => r.id === a.id)?.score || 0;
      const scoreB = results.find(r => r.id === b.id)?.score || 0;
      return scoreA - scoreB;
    });
  }

  private async vectorSearch(embedding: number[], limit: number) {
    // Vector search implementation
  }
}
```