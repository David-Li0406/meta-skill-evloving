# Atlas Decorators Cheat Sheet

| Decorator | Purpose | Usage |
|-----------|---------|-------|
| `@column({ isPrimary: true })` | Primary key | `@column({ isPrimary: true }) id!: number` |
| `@column()` | Standard database column | `@column() name!: string` |
| `@HasOne(() => Target)` | 1:1 relationship | `@HasOne(() => Profile) profile!: Profile` |
| `@HasMany(() => Target)` | 1:N relationship | `@HasMany(() => Post) posts!: Post[]` |
| `@BelongsTo(() => Target)` | Inverse of HasOne/Many | `@BelongsTo(() => User) user!: User` |

## Model Definition Template
```typescript
import { Model, column } from '@gravito/atlas'

export class MyModel extends Model {
  static table = 'my_table'

  @column({ isPrimary: true })
  id!: number

  @column()
  createdAt!: string
}
```
