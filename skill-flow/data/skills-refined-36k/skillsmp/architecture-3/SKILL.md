---
name: architecture
description: Experto en arquitectura limpia modularizada por features. Genera código optimizado, archivos cortos, desacoplados y con cumplimiento estricto de reglas de linter (0 warnings).
---

## Responsabilidad Única
Definir la estructura del proyecto y patrones arquitectónicos. NO incluye UI/UX, lógica de negocio, ni optimizaciones de performance.

---

## Estructura de Proyecto (Feature-First)
Para cada funcionalidad (feature_name), el agente debe organizar los archivos así:

```
lib/features/feature_name/
├── domain/
│   ├── entities/
│   ├── repositories/ (interfaces)
│   └── usecases/
├── data/
│   ├── models/
│   ├── datasources/
│   └── repositories/ (implementaciones)
└── presentation/
    ├── providers/ (Riverpod) o bloc/ (Bloc)
    ├── pages/
    └── widgets/
```

---

## Stack Técnico Core

### State Management
- **Riverpod**: Preferido para nuevos features (Notifier API, AsyncNotifier)
- **Bloc**: Alternativa válida (extender de Equatable para optimizar comparación de estados)

### Dependency Injection
- **GetIt**: Registro manual de dependencias en archivo centralizado `service_locator.dart`
- Registrar como singleton, lazy singleton o factory según el caso

### Navigation
- **GoRouter**: Routing declarativo con guards de autenticación
- Definir rutas en archivo centralizado
- Implementar Auth Guard usando Supabase Session

### Error Handling
- **fpdart**: Usar tipo `Either<Failure, Success>` para manejo funcional de errores
- Definir `Failure` classes en la capa Domain
- Nunca usar `print()` para errores, siempre retornar `Failure`

### Modelado de Datos
- **Models** (Data Layer): Incluir métodos `toEntity()` y `fromEntity()`
- **Entities** (Domain Layer): Clases inmutables con `freezed` o `equatable`
- Separación estricta: Models manejan JSON, Entities son puros

---

## Testing Strategy (TDD)

### Workflow TDD
Para cada feature, seguir este orden:
1. Escribir test del Use Case (usando Mocktail)
2. Implementar Use Case para que el test pase
3. Escribir test del Repository
4. Implementar Repository
5. Escribir test del Provider/Bloc
6. Implementar Provider/Bloc

### Tools
- **Mocktail**: Para mocks y stubs
- **flutter_test**: Testing framework
- **integration_test**: Para tests E2E

---

## Mandamientos de Código

### Inmutabilidad
- Todo widget debe usar `const` siempre que sea posible
- Clases de estado deben ser inmutables (`final` fields)
- Usar `freezed` o `equatable` para value objects

### Atomicidad
- **Máximo una clase principal por archivo**
- Si un Widget es complejo (>60 líneas), extraerlo a `widgets/` de la feature
- Archivos cortos: **150-200 líneas máximo**
- Priorizar composición sobre herencia

### Cero Tolerancia a Warnings
- Tras generar o editar código, verificar que no existan warnings
- Lints, tipos faltantes, imports sin usar: **TODO debe estar limpio**
- Usar `analysis_options.yaml` estricto

### Organización de Imports
```dart
// 1. Dart core
import 'dart:async';

// 2. Flutter
import 'package:flutter/material.dart';

// 3. Packages externos
import 'package:riverpod/riverpod.dart';

// 4. Imports internos (features)
import 'package:vector/features/packages/domain/entities/package.dart';
```

---

## Protocolo de Implementación

Al solicitar una nueva funcionalidad, el agente responderá en este orden:

1. **Entidad** (Domain) - Definir la entidad core
2. **Interfaz del Repositorio** (Domain) - Contrato del repositorio
3. **Casos de Uso** (Domain) - Lógica de negocio pura
4. **Modelo y DTOs** (Data) - Mappers `toEntity/fromEntity`
5. **Implementación del Repositorio** (Data) - Conexión con datasources
6. **Provider/Bloc** (Presentation) - State management
7. **UI Atómica** (Presentation) - Widgets pequeños y reutilizables

---

## Reglas de Separación de Capas

### Domain (Núcleo)
- ✅ Entities, Use Cases, Repository Interfaces
- ❌ **PROHIBIDO**: Importar Flutter, paquetes de terceros (excepto fpdart/equatable)

### Data
- ✅ Models, DataSources, Repository Implementations
- ✅ Puede importar: Supabase, HTTP clients, JSON serialization
- ❌ **PROHIBIDO**: Importar Flutter widgets

### Presentation
- ✅ Providers/Bloc, Pages, Widgets
- ✅ Puede importar: Flutter, Riverpod/Bloc, Domain entities
- ❌ **PROHIBIDO**: Importar Models de Data directamente

---

## File Naming Conventions

- **Entities**: `package.dart`, `delivery_route.dart`
- **Models**: `package_model.dart`, `delivery_route_model.dart`
- **Repositories**: `package_repository.dart` (interface y implementation)
- **Use Cases**: `get_packages.dart`, `create_package.dart`
- **Providers**: `package_provider.dart`
- **Screens**: `packages_screen.dart`, `add_package_screen.dart`
- **Widgets**: `package_card.dart`, `status_badge.dart`

---

## Ejemplo de Feature Completa

```
lib/features/packages/
├── domain/
│   ├── entities/
│   │   └── package.dart
│   ├── repositories/
│   │   └── package_repository.dart
│   └── usecases/
│       ├── get_packages.dart
│       └── create_package.dart
├── data/
│   ├── models/
│   │   └── package_model.dart
│   ├── datasources/
│   │   └── package_remote_datasource.dart
│   └── repositories/
│       └── package_repository_impl.dart
└── presentation/
    ├── providers/
    │   └── package_provider.dart
    ├── pages/
    │   └── packages_screen.dart
    └── widgets/
        └── package_card.dart
```