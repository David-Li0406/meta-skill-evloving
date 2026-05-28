# NestJS Search Patterns

## Elasticsearch Integration

```typescript
import { ElasticsearchModule, ElasticsearchService } from '@nestjs/elasticsearch';

@Module({
  imports: [
    ElasticsearchModule.register({
      node: 'http://localhost:9200',
    }),
  ],
})
export class SearchModule {}

@Injectable()
export class ProductSearchService {
  constructor(private readonly esService: ElasticsearchService) {}

  async indexProduct(product: Product) {
    await this.esService.index({
      index: 'products',
      id: product.id,
      document: {
        name: product.name,
        description: product.description,
        category: product.category,
        price: product.price,
      },
    });
  }

  async search(query: string, options?: { page?: number; limit?: number }) {
    const { page = 1, limit = 10 } = options || {};

    const result = await this.esService.search({
      index: 'products',
      from: (page - 1) * limit,
      size: limit,
      query: {
        multi_match: {
          query,
          fields: ['name^3', 'description', 'category'],
          fuzziness: 'AUTO',
        },
      },
    });

    return {
      hits: result.hits.hits.map(hit => hit._source),
      total: result.hits.total,
    };
  }

  async deleteIndex(id: string) {
    await this.esService.delete({ index: 'products', id });
  }
}
```

## PostgreSQL Full-Text Search

```typescript
import { Repository } from 'typeorm';

@Injectable()
export class ArticleSearchService {
  constructor(
    @InjectRepository(Article)
    private articleRepo: Repository<Article>,
  ) {}

  async search(query: string) {
    return this.articleRepo
      .createQueryBuilder('article')
      .where(
        `to_tsvector('english', article.title || ' ' || article.content) @@ plainto_tsquery('english', :query)`,
        { query },
      )
      .orderBy(
        `ts_rank(to_tsvector('english', article.title || ' ' || article.content), plainto_tsquery('english', :query))`,
        'DESC',
      )
      .getMany();
  }
}

// Migration for GIN index
export class AddSearchIndex implements MigrationInterface {
  async up(queryRunner: QueryRunner) {
    await queryRunner.query(`
      CREATE INDEX idx_article_search
      ON article
      USING GIN (to_tsvector('english', title || ' ' || content))
    `);
  }
}
```

## Search with Filters

```typescript
async advancedSearch(params: SearchParams) {
  const { query, category, minPrice, maxPrice, sort } = params;

  const must = [];
  const filter = [];

  if (query) {
    must.push({
      multi_match: { query, fields: ['name', 'description'] },
    });
  }

  if (category) {
    filter.push({ term: { category } });
  }

  if (minPrice || maxPrice) {
    filter.push({
      range: {
        price: {
          ...(minPrice && { gte: minPrice }),
          ...(maxPrice && { lte: maxPrice }),
        },
      },
    });
  }

  return this.esService.search({
    index: 'products',
    query: { bool: { must, filter } },
    sort: sort ? [{ [sort.field]: sort.order }] : undefined,
  });
}
```
