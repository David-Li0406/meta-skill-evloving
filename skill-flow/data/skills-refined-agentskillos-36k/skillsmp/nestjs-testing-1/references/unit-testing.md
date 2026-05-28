# NestJS Unit Testing

## Service Testing

```typescript
import { Test, TestingModule } from '@nestjs/testing';

describe('UsersService', () => {
  let service: UsersService;
  let repository: MockType<Repository<User>>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UsersService,
        {
          provide: getRepositoryToken(User),
          useFactory: repositoryMockFactory,
        },
      ],
    }).compile();

    service = module.get<UsersService>(UsersService);
    repository = module.get(getRepositoryToken(User));
  });

  describe('findOne', () => {
    it('should return a user', async () => {
      const user = { id: 1, name: 'John', email: 'john@test.com' };
      repository.findOne.mockResolvedValue(user);

      const result = await service.findOne(1);

      expect(result).toEqual(user);
      expect(repository.findOne).toHaveBeenCalledWith({ where: { id: 1 } });
    });

    it('should throw NotFoundException', async () => {
      repository.findOne.mockResolvedValue(null);

      await expect(service.findOne(999)).rejects.toThrow(NotFoundException);
    });
  });
});

// Mock factory
const repositoryMockFactory = () => ({
  find: jest.fn(),
  findOne: jest.fn(),
  save: jest.fn(),
  create: jest.fn(),
  update: jest.fn(),
  delete: jest.fn(),
});

type MockType<T> = {
  [P in keyof T]?: jest.Mock;
};
```

## Controller Testing

```typescript
describe('UsersController', () => {
  let controller: UsersController;
  let service: UsersService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [UsersController],
      providers: [
        {
          provide: UsersService,
          useValue: {
            findAll: jest.fn(),
            findOne: jest.fn(),
            create: jest.fn(),
          },
        },
      ],
    }).compile();

    controller = module.get<UsersController>(UsersController);
    service = module.get<UsersService>(UsersService);
  });

  describe('findAll', () => {
    it('should return an array of users', async () => {
      const users = [{ id: 1, name: 'John' }];
      jest.spyOn(service, 'findAll').mockResolvedValue(users);

      expect(await controller.findAll()).toBe(users);
    });
  });

  describe('create', () => {
    it('should create a user', async () => {
      const dto = { name: 'John', email: 'john@test.com' };
      const user = { id: 1, ...dto };
      jest.spyOn(service, 'create').mockResolvedValue(user);

      expect(await controller.create(dto)).toBe(user);
      expect(service.create).toHaveBeenCalledWith(dto);
    });
  });
});
```

## Mocking Patterns

```typescript
// Mock entire module
jest.mock('../services/email.service');

// Partial mock
jest.mock('../services/email.service', () => ({
  ...jest.requireActual('../services/email.service'),
  sendEmail: jest.fn(),
}));

// Spy on method
const spy = jest.spyOn(service, 'method');
spy.mockResolvedValue(result);

// Mock implementation
mockService.method.mockImplementation((arg) => {
  return arg === 'special' ? specialResult : defaultResult;
});

// Reset mocks
beforeEach(() => {
  jest.clearAllMocks();
});
```

## E2E Testing

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import * as request from 'supertest';

describe('UsersController (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  it('/users (GET)', () => {
    return request(app.getHttpServer())
      .get('/users')
      .expect(200)
      .expect((res) => {
        expect(Array.isArray(res.body)).toBe(true);
      });
  });

  it('/users (POST)', () => {
    return request(app.getHttpServer())
      .post('/users')
      .send({ name: 'John', email: 'john@test.com' })
      .expect(201)
      .expect((res) => {
        expect(res.body).toHaveProperty('id');
        expect(res.body.name).toBe('John');
      });
  });
});
```
