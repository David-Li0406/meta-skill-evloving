# Padroes de Teste

## Estrutura AAA (Arrange-Act-Assert)

```typescript
it('should calculate total correctly', () => {
  // Arrange - preparar dados
  const items = [
    { price: 10, quantity: 2 },
    { price: 5, quantity: 3 }
  ];

  // Act - executar acao
  const total = calculateTotal(items);

  // Assert - verificar resultado
  expect(total).toBe(35);
});
```

## Nomenclatura de Testes

```typescript
// Formato: should [comportamento] when [condicao]

// BOM
it('should return empty array when input is null', () => {});
it('should throw error when user not found', () => {});
it('should create user when data is valid', () => {});

// RUIM
it('test create', () => {});
it('should work', () => {});
it('user test', () => {});
```

## Organizacao com describe

```typescript
describe('UserService', () => {
  describe('create', () => {
    describe('when data is valid', () => {
      it('should create user', () => {});
      it('should return user id', () => {});
    });

    describe('when email already exists', () => {
      it('should throw ConflictError', () => {});
    });

    describe('when data is invalid', () => {
      it('should throw ValidationError', () => {});
    });
  });

  describe('findById', () => {
    // ...
  });
});
```

## Mocking

### Mock de Dependencias

```typescript
// Mock de modulo
jest.mock('../services/emailService');

// Mock de funcao
const mockSendEmail = jest.fn();
emailService.send = mockSendEmail;

// Verificar chamada
expect(mockSendEmail).toHaveBeenCalledWith({
  to: 'user@example.com',
  subject: 'Welcome'
});
```

### Mock de Database

```typescript
// Mock de repository
const mockUserRepo = {
  findById: jest.fn(),
  save: jest.fn(),
  delete: jest.fn()
};

// Setup
mockUserRepo.findById.mockResolvedValue({ id: '1', name: 'Test' });

// Usar no teste
const service = new UserService(mockUserRepo);
const user = await service.getUser('1');

expect(user.name).toBe('Test');
```

## Testes de Erro

```typescript
describe('error handling', () => {
  it('should throw NotFoundError when user does not exist', async () => {
    mockRepo.findById.mockResolvedValue(null);

    await expect(service.getUser('invalid-id'))
      .rejects
      .toThrow(NotFoundError);
  });

  it('should throw ValidationError when email is invalid', async () => {
    const invalidData = { email: 'not-an-email' };

    await expect(service.createUser(invalidData))
      .rejects
      .toThrow(ValidationError);
  });
});
```

## Testes de Edge Cases

```typescript
describe('edge cases', () => {
  it('should handle null input', () => {
    expect(processData(null)).toEqual([]);
  });

  it('should handle empty array', () => {
    expect(processData([])).toEqual([]);
  });

  it('should handle undefined', () => {
    expect(processData(undefined)).toEqual([]);
  });

  it('should handle very large input', () => {
    const largeInput = Array(10000).fill({ value: 1 });
    expect(() => processData(largeInput)).not.toThrow();
  });

  it('should handle special characters', () => {
    const input = { name: '<script>alert("xss")</script>' };
    const result = sanitize(input);
    expect(result.name).not.toContain('<script>');
  });
});
```

## Setup e Teardown

```typescript
describe('Feature', () => {
  let testDb: TestDatabase;
  let service: MyService;

  // Roda uma vez antes de todos os testes
  beforeAll(async () => {
    testDb = await TestDatabase.create();
  });

  // Roda uma vez depois de todos os testes
  afterAll(async () => {
    await testDb.destroy();
  });

  // Roda antes de cada teste
  beforeEach(async () => {
    await testDb.clear();
    service = new MyService(testDb);
  });

  // Roda depois de cada teste
  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should ...', () => {});
});
```

## Testes Assincronos

```typescript
// Com async/await
it('should fetch user', async () => {
  const user = await service.getUser('1');
  expect(user).toBeDefined();
});

// Com promises
it('should fetch user', () => {
  return service.getUser('1').then(user => {
    expect(user).toBeDefined();
  });
});

// Com done callback
it('should emit event', (done) => {
  emitter.on('event', (data) => {
    expect(data).toBe('value');
    done();
  });
  emitter.emit('event', 'value');
});
```

## Testes de Integracao

```typescript
describe('API Integration', () => {
  let app: Express;

  beforeAll(() => {
    app = createApp();
  });

  it('should create user via API', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', password: 'password123' })
      .expect(201);

    expect(response.body.id).toBeDefined();
    expect(response.body.email).toBe('test@example.com');
  });

  it('should return 400 for invalid data', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'invalid' })
      .expect(400);

    expect(response.body.error).toBeDefined();
  });
});
```
