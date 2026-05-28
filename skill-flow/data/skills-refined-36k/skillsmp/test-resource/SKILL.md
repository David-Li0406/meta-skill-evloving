---
name: test-resource
description: Crea pruebas unitarias aisladas para Servicios y Resolvers de NestJS usando Mocks de Mongoose y Jest, adaptado a la arquitectura del proyecto.
---

# Backend Unit Testing (Jest + Mongoose + GraphQL)

Esta skill te guía para crear pruebas unitarias robustas y aisladas.

> [!IMPORTANT]
> **Regla de Oro:** NUNCA uses `MongooseModule.forRoot` ni conectes a la DB real en pruebas unitarias. SIEMPRE mockea los Modelos y Servicios.

---

## 1. Testing de Servicios (`.service.spec.ts`)

Objetivo: Probar la lógica de negocio y la integración con Mongoose (mocked).

### Template

```typescript
// src/modules/[nombre]/services/[nombre].service.spec.ts

import { Test, TestingModule } from '@nestjs/testing';
import { getModelToken } from '@nestjs/mongoose';
import { [Nombre]Service } from './[nombre].service';
import { [Nombre] } from '../entities/[nombre].entity';
import { createMock } from '@golevelup/ts-jest'; // Opcional: si usas esta librería, sino usa jest.fn()
import { Model } from 'mongoose';

describe('[Nombre]Service', () => {
  let service: [Nombre]Service;
  let model: Model<[Nombre]>;

  // 1. Mock del Modelo Mongoose
  // Simula los métodos de Mongoose que usa BaseService y el servicio
  const mock[Nombre]Model = {
    new: jest.fn().mockResolvedValue({}),
    constructor: jest.fn().mockResolvedValue({}),
    find: jest.fn(),
    findOne: jest.fn(),
    findById: jest.fn(),
    create: jest.fn(),
    findByIdAndUpdate: jest.fn(),
    findByIdAndDelete: jest.fn(),
    exec: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        [Nombre]Service,
        {
          provide: getModelToken([Nombre].name), // Token de inyección correcto
          useValue: mock[Nombre]Model,
        },
      ],
    }).compile();

    service = module.get<[Nombre]Service>([Nombre]Service);
    model = module.get<Model<[Nombre]>>(getModelToken([Nombre].name));
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  describe('findAll', () => {
    it('debe retornar un array de [nombre]s', async () => {
      // Arrange
      const resultExpected = [{ _id: '1', nombre: 'Test' }];
      // Mockear la cadena: find() -> sort() -> skip() -> limit() -> exec()
      // BaseService suele usar exec() al final
      const mockQuery = {
        sort: jest.fn().mockReturnThis(),
        skip: jest.fn().mockReturnThis(),
        limit: jest.fn().mockReturnThis(),
        exec: jest.fn().mockResolvedValue(resultExpected),
      };
      
      jest.spyOn(model, 'find').mockReturnValue(mockQuery as any);

      // Act
      const result = await service.findAll();

      // Assert
      expect(result).toBe(resultExpected);
      expect(model.find).toHaveBeenCalled();
    });
  });

  describe('create', () => {
    it('debe crear un nuevo [nombre]', async () => {
      // Arrange
      const createDto = { campo1: 'Valor' };
      const userId = 'user123';
      const createdDoc = { ...createDto, _id: 'newId' };

      jest.spyOn(model, 'create').mockResolvedValue(createdDoc as any);

      // Act
      // Nota: BaseService requiere userId como ObjectId, asegura pasar el tipo correcto o mockearlo
      const result = await service.create(createDto as any, userId as any);

      // Assert
      expect(result).toEqual(createdDoc);
      expect(model.create).toHaveBeenCalledWith({ ...createDto, createdBy: userId, updatedBy: userId });
    });
  });
});
```

---

## 2. Testing de Resolvers (`.resolver.spec.ts`)

Objetivo: Probar la capa GraphQL, asegurando que llama correctamente al servicio y maneja los guards (aunque guards se suelen probar en e2e, aquí probamos la lógica del resolver).

> [!TIP]
> Aquí mockeamos el `[Nombre]Service` completo. No necesitamos mockear Mongoose aquí.

### Template

```typescript
// src/modules/[nombre]/resolvers/[nombre].resolver.spec.ts

import { Test, TestingModule } from '@nestjs/testing';
import { [Nombre]Resolver } from './[nombre].resolver';
import { [Nombre]Service } from '../services/[nombre].service';
import { Create[Nombre]Input } from '../dtos/create-[nombre].input';

describe('[Nombre]Resolver', () => {
  let resolver: [Nombre]Resolver;
  let service: [Nombre]Service;

  // Mock del Servicio
  const mock[Nombre]Service = {
    create: jest.fn(),
    findAll: jest.fn(),
    findById: jest.fn(),
    update: jest.fn(),
    softDelete: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        [Nombre]Resolver,
        {
          provide: [Nombre]Service,
          useValue: mock[Nombre]Service,
        },
      ],
    }).compile();

    resolver = module.get<[Nombre]Resolver>([Nombre]Resolver);
    service = module.get<[Nombre]Service>([Nombre]Service);
  });

  it('should be defined', () => {
    expect(resolver).toBeDefined();
  });

  describe('create', () => {
    it('debe llamar al servicio.create con los argumentos correctos', async () => {
      // Arrange
      const dto = { campo1: 'Test' } as Create[Nombre]Input;
      const user = { _id: 'userId' }; // Mock UserRequest
      const expectedResult = { _id: '1', ...dto };

      mock[Nombre]Service.create.mockResolvedValue(expectedResult);

      // Act
      const result = await resolver.create(dto, user as any);

      // Assert
      expect(service.create).toHaveBeenCalledWith(dto, expect.anything()); // userId transformation check
      expect(result).toEqual(expectedResult);
    });
  });

  describe('findAll', () => {
    it('debe retornar un array de [nombre]s', async () => {
      // Arrange
      const expectedDocs = [{ _id: '1' }];
      mock[Nombre]Service.findAll.mockResolvedValue(expectedDocs as any);

      // Act
      const result = await resolver.findAll();

      // Assert
      expect(service.findAll).toHaveBeenCalled();
      expect(result).toEqual(expectedDocs);
    });
  });
});
```

---

## 3. Claves del Éxito

1.  **Mock Chain**: Mongoose usa encadenamiento (`find().sort().exec()`). Asegúrate de que tus mocks soporten esto (`mockReturnThis()`).
2.  **BaseService**: Al extender `BaseService`, recuerda que `findAll` llama a `find()`, pero `create` llama a `model.create()`.
3.  **Tipos**: Usa `any` o `as Type` pragmáticamente en los mocks para evitar pelear con tipos complejos de MongooseDocument en los tests.
