---
name: create-resource
description: Genera un recurso Backend completo en NestJS (Module, Entity, Service, Resolver, DTOs, Interface, Controller) siguiendo la arquitectura Code First del proyecto iqEngi.
---

# Crear Recurso Backend (NestJS + MongoDB + GraphQL)

Usa esta skill cuando necesites crear una nueva entidad (ej. `Certificado`, `Leccion`, `Progreso`).

## Arquitectura del Proyecto

El proyecto utiliza una arquitectura **Code First** con:
- **NestJS** como framework
- **Mongoose** para la base de datos MongoDB
- **GraphQL** con Apollo Server
- **Soft Delete** pattern para eliminación lógica
- **JWT + Roles** para autenticación y autorización

---

## 1. Estructura de Archivos

Generar los archivos en `src/modules/[nombre-recurso]/`:

```
src/modules/[nombre-recurso]/
├── [nombre-recurso].module.ts
├── entities/
│   └── [nombre-recurso].entity.ts     # Combina Schema + ObjectType
├── interfaces/
│   └── [nombre-recurso].interface.ts  # TypeScript interfaces
├── dtos/
│   ├── create-[nombre-recurso].input.ts
│   └── update-[nombre-recurso].input.ts
├── services/
│   └── [nombre-recurso].service.ts
├── resolvers/
│   └── [nombre-recurso].resolver.ts
└── controllers/
    └── [nombre-recurso].controller.ts  # REST (opcional, vacío por defecto)
```

---

## 2. Archivos a Generar

### 2.1 Interface (`interfaces/[nombre].interface.ts`)

Define las interfaces TypeScript para tipado estricto.

```typescript
// src/modules/[nombre]/interfaces/[nombre].interface.ts

import { Types } from 'mongoose';
import { IdInterface } from 'src/common/interfaces/id.interface';

export interface I[Nombre] extends IdInterface {
  _id: Types.ObjectId;
  // Propiedades específicas de la entidad
  campo1: string;
  campo2?: number;
}

export type I[Nombre]Input = Omit<I[Nombre], '_id'>;
```

---

### 2.2 Entity (`entities/[nombre].entity.ts`)

> [!IMPORTANT]
> La Entity combina **Mongoose Schema** + **GraphQL ObjectType** en un solo archivo.

```typescript
// src/modules/[nombre]/entities/[nombre].entity.ts

import { Field, ID, ObjectType } from '@nestjs/graphql';
import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Types } from 'mongoose';
import { I[Nombre] } from '../interfaces/[nombre].interface';

import { AuditFields } from 'src/common/clases/audit-fields.class';
import { addSoftDeleteMiddleware } from 'src/common/middlewares/soft-delete.middleware';

@ObjectType()
@Schema({ timestamps: true })
export class [Nombre] extends AuditFields implements I[Nombre] {
  @Field(() => ID)
  _id: Types.ObjectId;

  @Field()
  @Prop({ required: true })
  campo1: string;

  @Field({ nullable: true })
  @Prop()
  campo2?: number;

  @Field()
  @Prop({ default: false })
  deleted: boolean;
}

export const [Nombre]Schema = SchemaFactory.createForClass([Nombre]);

// Índice para soft delete
[Nombre]Schema.index({ deleted: 1 });

// Middleware para soft delete automático
addSoftDeleteMiddleware<[Nombre], [Nombre]>([Nombre]Schema);
```

**Relaciones con otros documentos:**

```typescript
// Referencia a otro documento
@Field(() => ID)
@Prop({ type: Types.ObjectId, ref: 'OtraEntidad', required: true })
otraEntidadId: Types.ObjectId;

// Array de referencias
@Field(() => [ID], { nullable: true })
@Prop({ type: [Types.ObjectId], ref: 'OtraEntidad', default: [] })
items: Types.ObjectId[];
```

---

### 2.3 DTOs (`dtos/`)

#### Create Input

```typescript
// src/modules/[nombre]/dtos/create-[nombre].input.ts

import { InputType, Field } from '@nestjs/graphql';
import { IsNotEmpty, IsString, IsOptional, IsNumber } from 'class-validator';
import { I[Nombre]Input } from '../interfaces/[nombre].interface';

@InputType()
export class Create[Nombre]Input implements I[Nombre]Input {
  @Field()
  @IsNotEmpty()
  @IsString()
  campo1: string;

  @Field({ nullable: true })
  @IsOptional()
  @IsNumber()
  campo2?: number;
}
```

#### Update Input

```typescript
// src/modules/[nombre]/dtos/update-[nombre].input.ts

import { InputType, PartialType } from '@nestjs/graphql';
import { Create[Nombre]Input } from './create-[nombre].input';

@InputType()
export class Update[Nombre]Input extends PartialType(Create[Nombre]Input) {}
```

---

### 2.4 Service (`services/[nombre].service.ts`)

> [!TIP]
> Extiende `BaseService` para heredar operaciones CRUD + soft delete automáticamente.

```typescript
// src/modules/[nombre]/services/[nombre].service.ts

import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { [Nombre] } from '../entities/[nombre].entity';
import { Create[Nombre]Input } from '../dtos/create-[nombre].input';
import { Update[Nombre]Input } from '../dtos/update-[nombre].input';
import { BaseService } from 'src/common/services/base.service';
import SearchField from 'src/common/clases/search-field.class';
import { SearchTextArgs, PaginationArgs } from 'src/common/dtos';

@Injectable()
export class [Nombre]Service extends BaseService<
  [Nombre],
  Update[Nombre]Input,
  Create[Nombre]Input
> {
  constructor(
    @InjectModel([Nombre].name)
    private readonly [nombre]Model: Model<[Nombre]>,
  ) {
    super([nombre]Model);
  }

  // Métodos adicionales específicos del recurso
  async findAllByCampo1(
    searchTextArgs: SearchTextArgs,
    paginationArgs?: PaginationArgs,
  ): Promise<[Nombre][]> {
    const searchField: SearchField<[Nombre]> = new SearchField();
    searchField.field = 'campo1';

    return super.findAllBy(
      searchTextArgs,
      searchField,
      paginationArgs,
    ) as Promise<[Nombre][]>;
  }
}
```

**Métodos heredados de BaseService:**
- `create(dto, userId)` - Crear documento
- `findAll(pagination?)` - Listar todos
- `findById(id)` - Buscar por ID
- `update(id, dto, userId)` - Actualizar
- `softDelete(id, userId)` - Eliminación lógica
- `hardDelete(id)` - Eliminación permanente
- `hardDeleteAllSoftDeleted()` - Limpiar soft deleted
- `findSoftDeleted(pagination?)` - Listar eliminados
- `restore(id, userId)` - Restaurar

---

### 2.5 Resolver (`resolvers/[nombre].resolver.ts`)

```typescript
// src/modules/[nombre]/resolvers/[nombre].resolver.ts

import { Args, ID, Mutation, Query, Resolver } from '@nestjs/graphql';
import { [Nombre] } from '../entities/[nombre].entity';
import { [Nombre]Service } from '../services/[nombre].service';

import { UseGuards } from '@nestjs/common';
import { JwtGqlAuthGuard } from 'src/modules/auth/jwt-auth/jwt-auth.guard/jwt-auth.guard';
import { RolesGuard } from 'src/modules/auth/roles-guards/roles.guard';
import { RolesDec } from 'src/modules/auth/decorators/roles.decorator';
import { CurrentUser } from 'src/modules/auth/decorators/current-user.decorator';
import { UserRequest } from 'src/modules/auth/entities/user-request.entity';
import { PaginationArgs, SearchTextArgs } from 'src/common/dtos';
import { administradorUp, RolEnum } from 'src/common/enums/rol.enum';
import { IdPipe } from 'src/common/pipes/mongo-id/mongo-id.pipe';
import { Types } from 'mongoose';
import { DeletedCountOutput } from 'src/modules/usuario/dtos/usuarios-dtos/deleted-count.output';
import { Update[Nombre]Input } from '../dtos/update-[nombre].input';
import { Create[Nombre]Input } from '../dtos/create-[nombre].input';
import { IResolverBase } from 'src/common/interfaces/resolver-base.interface';
import { IsPublic } from 'src/modules/auth/decorators/public.decorator';

@UseGuards(JwtGqlAuthGuard, RolesGuard)
@Resolver(() => [Nombre])
export class [Nombre]Resolver
  implements IResolverBase<[Nombre], Create[Nombre]Input, Update[Nombre]Input>
{
  constructor(private readonly [nombre]Service: [Nombre]Service) {}

  // ═══════════════════════════════════════════════════════════════════
  // MUTATIONS
  // ═══════════════════════════════════════════════════════════════════

  /**
   * Crea un nuevo [nombre].
   * @Roles: ADMINISTRADOR, SUPERADMIN
   */
  @Mutation(() => [Nombre], { name: '[Nombre]s_create' })
  @RolesDec(...administradorUp)
  async create(
    @Args('create[Nombre]Input') create[Nombre]Input: Create[Nombre]Input,
    @CurrentUser() user: UserRequest,
  ): Promise<[Nombre]> {
    const userId = new Types.ObjectId(user._id);
    return this.[nombre]Service.create(create[Nombre]Input, userId);
  }

  /**
   * Actualiza un [nombre] existente.
   * @Roles: ADMINISTRADOR, SUPERADMIN
   */
  @Mutation(() => [Nombre], { name: '[Nombre]s_update' })
  @RolesDec(...administradorUp)
  async update(
    @Args('id', { type: () => ID }, IdPipe) id: Types.ObjectId,
    @Args('update[Nombre]Input') update[Nombre]Input: Update[Nombre]Input,
    @CurrentUser() user: UserRequest,
  ): Promise<[Nombre]> {
    const idUpdatedBy = new Types.ObjectId(user._id);
    return this.[nombre]Service.update(id, update[Nombre]Input, idUpdatedBy);
  }

  /**
   * Elimina lógicamente un [nombre].
   * @Roles: ADMINISTRADOR, SUPERADMIN
   */
  @Mutation(() => [Nombre], { name: '[Nombre]s_softDelete' })
  @RolesDec(...administradorUp)
  async softDelete(
    @Args('idRemove', { type: () => ID }, IdPipe) idRemove: Types.ObjectId,
    @CurrentUser() user: UserRequest,
  ): Promise<[Nombre]> {
    const idThanos = new Types.ObjectId(user._id);
    return this.[nombre]Service.softDelete(idRemove, idThanos);
  }

  /**
   * Elimina permanentemente un [nombre].
   * @Roles: SUPERADMIN
   */
  @Mutation(() => [Nombre], { name: '[Nombre]s_hardDelete' })
  @RolesDec(RolEnum.SUPERADMIN)
  async hardDelete(
    @Args('id', { type: () => ID }, IdPipe) id: Types.ObjectId,
  ): Promise<[Nombre]> {
    return this.[nombre]Service.hardDelete(id);
  }

  /**
   * Elimina permanentemente todos los [nombre]s soft deleted.
   * @Roles: SUPERADMIN
   */
  @Mutation(() => DeletedCountOutput, { name: '[Nombre]s_hardDeleteAllSoftDeleted' })
  @RolesDec(RolEnum.SUPERADMIN)
  async hardDeleteAllSoftDeleted(): Promise<DeletedCountOutput> {
    return this.[nombre]Service.hardDeleteAllSoftDeleted();
  }

  /**
   * Restaura un [nombre] eliminado.
   * @Roles: ADMINISTRADOR, SUPERADMIN
   */
  @Mutation(() => [Nombre], { name: '[Nombre]s_restore' })
  @RolesDec(...administradorUp)
  async restore(
    @Args('idRestore', { type: () => ID }, IdPipe) idRestore: Types.ObjectId,
    @CurrentUser() user: UserRequest,
  ): Promise<[Nombre]> {
    const userId = new Types.ObjectId(user._id);
    return this.[nombre]Service.restore(idRestore, userId);
  }

  // ═══════════════════════════════════════════════════════════════════
  // QUERIES
  // ═══════════════════════════════════════════════════════════════════

  /**
   * Obtiene todos los [nombre]s.
   * @Roles: PUBLIC (ajustar según necesidad)
   */
  @Query(() => [[Nombre]], { name: '[Nombre]s' })
  @IsPublic() // O usar @RolesDec(...administradorUp) si requiere autenticación
  async findAll(@Args() pagination?: PaginationArgs): Promise<[Nombre][]> {
    return this.[nombre]Service.findAll(pagination);
  }

  /**
   * Obtiene un [nombre] por ID.
   * @Roles: ADMINISTRADOR, SUPERADMIN
   */
  @Query(() => [Nombre], { name: '[Nombre]' })
  @RolesDec(...administradorUp)
  async findById(
    @Args('id', { type: () => ID }, IdPipe) id: Types.ObjectId,
  ): Promise<[Nombre]> {
    return this.[nombre]Service.findById(id);
  }

  /**
   * Busca [nombre]s por campo1.
   * @Roles: ADMINISTRADOR, SUPERADMIN
   */
  @Query(() => [[Nombre]], { name: '[Nombre]s_findAllByCampo1' })
  @RolesDec(...administradorUp)
  async findAllByCampo1(
    @Args() searchArgs: SearchTextArgs,
    @Args() pagination?: PaginationArgs,
  ): Promise<[Nombre][]> {
    return this.[nombre]Service.findAllByCampo1(searchArgs, pagination);
  }

  /**
   * Obtiene todos los [nombre]s eliminados.
   * @Roles: ADMINISTRADOR, SUPERADMIN
   */
  @Query(() => [[Nombre]], { name: '[Nombre]s_findSoftDeleted' })
  @RolesDec(...administradorUp)
  async findSoftDeleted(
    @Args({ type: () => PaginationArgs, nullable: true }) pagination?: PaginationArgs,
  ): Promise<[Nombre][]> {
    return this.[nombre]Service.findSoftDeleted(pagination);
  }
}
```

---

### 2.6 Controller (`controllers/[nombre].controller.ts`)

> [!NOTE]
> El controller REST es opcional. Déjalo vacío si solo usas GraphQL.

```typescript
// src/modules/[nombre]/controllers/[nombre].controller.ts

import { Controller } from '@nestjs/common';
import { ApiTags } from '@nestjs/swagger';

@ApiTags('[nombre]s')
@Controller('[nombre]s')
export class [Nombre]Controller {}
```

---

### 2.7 Module (`[nombre].module.ts`)

```typescript
// src/modules/[nombre]/[nombre].module.ts

import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';

import { [Nombre]Controller } from './controllers/[nombre].controller';
import { [Nombre]Service } from './services/[nombre].service';
import { [Nombre], [Nombre]Schema } from './entities/[nombre].entity';
import { [Nombre]Resolver } from './resolvers/[nombre].resolver';

@Module({
  imports: [
    MongooseModule.forFeature([
      { name: [Nombre].name, schema: [Nombre]Schema },
    ]),
    // Añadir forwardRef si hay dependencias circulares:
    // forwardRef(() => OtroModule),
  ],
  controllers: [[Nombre]Controller],
  providers: [[Nombre]Service, [Nombre]Resolver],
  exports: [[Nombre]Service], // Exportar si otros módulos lo necesitan
})
export class [Nombre]Module {}
```

---

## 3. Registro Global

> [!CAUTION]
> **Paso final obligatorio:** Importar el nuevo módulo en `src/app.module.ts`.

```typescript
// src/app.module.ts

import { [Nombre]Module } from './modules/[nombre]/[nombre].module';

@Module({
  imports: [
    // ... otros módulos ...
    [Nombre]Module, // ← Añadir en orden alfabético
  ],
})
export class AppModule {}
```

---

## 4. Decoradores de Roles Disponibles

| Decorator | Descripción |
|-----------|-------------|
| `@IsPublic()` | Endpoint público, sin autenticación |
| `@RolesDec(RolEnum.USUARIO)` | Solo usuarios autenticados |
| `@RolesDec(...administradorUp)` | Administrador y SuperAdmin |
| `@RolesDec(RolEnum.SUPERADMIN)` | Solo SuperAdmin |

---

## 5. Validadores Comunes (class-validator)

| Validador | Uso |
|-----------|-----|
| `@IsNotEmpty()` | Campo requerido |
| `@IsString()` | Debe ser string |
| `@IsNumber()` | Debe ser número |
| `@IsOptional()` | Campo opcional |
| `@IsEmail()` | Debe ser email válido |
| `@IsArray()` | Debe ser array |
| `@IsDate()` | Debe ser fecha |
| `@IsMongoId()` | Debe ser ObjectId válido |
| `@Min(n)` / `@Max(n)` | Valor mínimo/máximo |
| `@MinLength(n)` / `@MaxLength(n)` | Longitud de string |

---

## 6. Checklist de Verificación

- [ ] Interface creada con tipos correctos
- [ ] Entity extiende `AuditFields`
- [ ] Entity tiene `@ObjectType()` y `@Schema({ timestamps: true })`
- [ ] Soft delete middleware aplicado al Schema
- [ ] DTOs con validadores class-validator
- [ ] Service extiende `BaseService`
- [ ] Resolver implementa `IResolverBase`
- [ ] Resolver tiene guards `@UseGuards(JwtGqlAuthGuard, RolesGuard)`
- [ ] Module importa `MongooseModule.forFeature`
- [ ] Module registrado en `app.module.ts`
- [ ] Verificar que el servidor compila sin errores: `npm run start:dev`
- [ ] Schema GraphQL generado correctamente en `src/schema.gql`
