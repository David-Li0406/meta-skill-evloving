# NestJS TypeORM Patterns

## Entity Definition

```typescript
import { Entity, Column, PrimaryGeneratedColumn, CreateDateColumn, ManyToOne, OneToMany } from 'typeorm';

@Entity('users')
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ length: 100 })
  name: string;

  @Column({ unique: true })
  email: string;

  @Column({ default: true })
  isActive: boolean;

  @CreateDateColumn()
  createdAt: Date;

  @OneToMany(() => Post, post => post.author)
  posts: Post[];
}

@Entity('posts')
export class Post {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  title: string;

  @ManyToOne(() => User, user => user.posts)
  author: User;

  @Column()
  authorId: number;
}
```

## Repository Pattern

```typescript
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';

@Injectable()
export class UsersRepository {
  constructor(
    @InjectRepository(User)
    private readonly repo: Repository<User>,
  ) {}

  async findAll(): Promise<User[]> {
    return this.repo.find({ relations: ['posts'] });
  }

  async findById(id: number): Promise<User | null> {
    return this.repo.findOne({ where: { id }, relations: ['posts'] });
  }

  async create(data: CreateUserDto): Promise<User> {
    const user = this.repo.create(data);
    return this.repo.save(user);
  }

  async update(id: number, data: UpdateUserDto): Promise<User> {
    await this.repo.update(id, data);
    return this.findById(id);
  }

  async delete(id: number): Promise<void> {
    await this.repo.delete(id);
  }
}
```

## Query Builder

```typescript
async findWithFilters(filters: FilterDto): Promise<User[]> {
  const qb = this.repo.createQueryBuilder('user')
    .leftJoinAndSelect('user.posts', 'post');

  if (filters.name) {
    qb.andWhere('user.name ILIKE :name', { name: `%${filters.name}%` });
  }

  if (filters.isActive !== undefined) {
    qb.andWhere('user.isActive = :isActive', { isActive: filters.isActive });
  }

  return qb
    .orderBy('user.createdAt', 'DESC')
    .skip(filters.offset)
    .take(filters.limit)
    .getMany();
}
```

## Transactions

```typescript
import { DataSource } from 'typeorm';

@Injectable()
export class OrdersService {
  constructor(private dataSource: DataSource) {}

  async createOrder(dto: CreateOrderDto): Promise<Order> {
    const queryRunner = this.dataSource.createQueryRunner();
    await queryRunner.connect();
    await queryRunner.startTransaction();

    try {
      const order = await queryRunner.manager.save(Order, dto);
      await queryRunner.manager.update(Product, dto.productId, {
        stock: () => 'stock - 1',
      });
      await queryRunner.commitTransaction();
      return order;
    } catch (err) {
      await queryRunner.rollbackTransaction();
      throw err;
    } finally {
      await queryRunner.release();
    }
  }
}
```

## Module Setup

```typescript
import { TypeOrmModule } from '@nestjs/typeorm';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: 'localhost',
      port: 5432,
      database: 'mydb',
      entities: [User, Post],
      synchronize: false, // Use migrations in production
    }),
    TypeOrmModule.forFeature([User, Post]),
  ],
})
export class DatabaseModule {}
```
