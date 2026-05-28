---
name: zio-dependency-injection
description: Standardized patterns for ZIO dependency injection using the ZIO service pattern with ZLayer.derive. Use when creating new ZIO service classes, refactoring existing ZIO code to follow this pattern, reviewing code that incorrectly uses ZIO.service in business logic, or when working with ZIO layers and dependency injection. Apply this pattern for all service classes in the Scala backend.
---

# ZIO Dependency Injection

## Overview

Use the ZIO service pattern where all class dependencies are injected as constructor parameters and every service class has a layer built using `ZLayer.derive`, which automatically wires up constructor parameters.

**Key principle**: Only use `ZIO.service` accessor methods in main application files for composing the application, or for accessing contextual information from the environment (like `MemberAuthContext`). Never use them in service implementations.

## The Service Pattern

### Structure

Every service follows this three-part structure:

1. **Trait**: Defines the service interface
2. **Case class implementation**: All dependencies as constructor parameters
3. **Companion object**: Contains `ZLayer.derive` for automatic dependency wiring

### Example

```scala
// 1. Trait defining the service interface
trait UpdateSyncService {
  def createSync(
      project: Project,
      integrationId: UUID,
      source: Source,
      destination: Destination,
      transformation: Option[Spec],
  ): IO[StrataError, Sync]
}

// 2. Case class with all dependencies as constructor parameters
final case class UpdateSyncServiceLive(
    syncRepo: SyncRepo,
    syncJobScheduler: SyncJobScheduler,
    integrationService: IntegrationService,
    buildService: BuildService,
    deploymentRepo: SyncFunctionDeploymentRepo,
) extends UpdateSyncService {

  override def createSync(
      project: Project,
      integrationId: UUID,
      source: Source,
      destination: Destination,
      transformation: Option[Spec],
  ): IO[StrataError, Sync] = {
    // Implementation uses dependencies directly from constructor
    for {
      sync <- syncRepo.createSync(...)
      _    <- syncJobScheduler.scheduleForConnection(...)
    } yield sync
  }
}

// 3. Companion object with ZLayer.derive, omit the type and allow the compiler to infer it
object UpdateSyncServiceLive {
  val layer = ZLayer.derive[UpdateSyncServiceLive]
}
```

**Key points:**
- Dependencies are class constructor parameters, NOT accessed via `ZIO.service`
- `ZLayer.derive` automatically inspects constructor and wires dependencies
- Type signature can be explicit or inferred (both are acceptable)

## Anti-Patterns

### ❌ Manual Layer Construction When Not Required

**Bad:**
```scala
object StrataJwtServiceLive {
  val layer: ZLayer[JwtValidation & Config.Error, StrataJwtServiceLive] =
    ZLayer.fromZIO(
      for {
        config        <- ZIO.config[StrataJwtServiceConfig]
        jwtValidation <- ZIO.service[JwtValidation]
      } yield StrataJwtServiceLive(config, jwtValidation)
    )
}
```

**Good:**
```scala
object StrataJwtServiceLive {
  val layer = ZLayer.derive[StrataJwtServiceLive]
}
```

**Why it's bad:**
- Manual wiring is verbose and error-prone
- `ZLayer.derive` does this automatically
- Changes to constructor require updating the for-comprehension

### ❌ Using ZIO.service or ZIO.serviceWith in Business Logic

**Bad:**
```scala
final case class UpdateSyncServiceLive() extends UpdateSyncService {
  override def createSync(...): IO[StrataError, Sync] = {
    for {
      syncRepo          <- ZIO.service[SyncRepo]
      syncJobScheduler  <- ZIO.service[SyncJobScheduler]
      integrationService <- ZIO.service[IntegrationService]
      sync              <- syncRepo.createSync(...)
      _                 <- syncJobScheduler.scheduleForConnection(...)
    } yield sync
  }
}
```

**Good:**
```scala
final case class UpdateSyncServiceLive(
    syncRepo: SyncRepo,
    syncJobScheduler: SyncJobScheduler,
    integrationService: IntegrationService,
) extends UpdateSyncService {
  override def createSync(...): IO[StrataError, Sync] = {
    for {
      sync <- syncRepo.createSync(...)
      _    <- syncJobScheduler.scheduleForConnection(...)
    } yield sync
  }
}
```

**Why it's bad:**
- Makes dependencies implicit and hard to track
- Requires adding services to the environment type of every method
- Makes testing harder (can't easily inject mocks)
- Defeats the purpose of constructor-based dependency injection

## When ZIO.service IS Appropriate

### Main Application Files

Use `ZIO.service` in main application files to compose the application:

```scala
object ConnectApiApp extends StrataAppDefault {
  val app = for {
    corsConfig    <- ZIO.config[ApiCorsConfig]
    appModeConfig <- ZIO.config[AppModeConfig]
    oauthRoutes   <- ZIO.serviceWith[OAuth2Routes](_.routes)
  } yield routes ++ HealthCheckRoutes.routes.requestLogging(appModeConfig)

  override val run = app
    .flatMap(_.serve)
    .provideSomeAuto(
      // ... all other layers
    )
}
```

**Why this is appropriate:**
- Main app is responsible for composing the entire application
- This is the one place where we wire everything together
- Dependencies are provided via `.provideSomeAuto()`

### Accessing Contextual Information

Use `ZIO.serviceWith` to access contextual information from the environment:

```scala
// Define contextual information
case class MemberAuthContext(org: Organization, project: Project, member: Member)

// Use in resolvers/handlers
def getIntegration(args: IntegrationArgs): ZIO[MemberAuthContext, GraphqlError, Option[Integration]] = {
  for {
    project     <- ZIO.serviceWith[MemberAuthContext](_.project)
    integration <- integrationService.getIntegrationById(project.id, args.integrationId)
  } yield integration
}
```

**Why this is appropriate:**
- `MemberAuthContext` is request-scoped contextual information
- It's provided by middleware on a per-request basis
- It's not a "dependency" in the traditional sense—it's runtime context
- Services shouldn't require it as a constructor parameter

**Rule of thumb:**
- If it's request-scoped or operation-scoped context: use `ZIO.service`
- If it's a service/repository/component: constructor parameter

## Applying the Pattern

When creating a new service:

1. Define the trait with the service interface
2. Create a case class implementation with all dependencies as constructor parameters
3. Add companion object with `val layer = ZLayer.derive[ServiceNameLive]`
4. Never use `ZIO.service` or `ZIO.serviceWith` in the implementation

When reviewing code:

1. Check that service implementations use constructor parameters, not `ZIO.service`
2. Verify layers use `ZLayer.derive`, not manual construction
3. Confirm `ZIO.service` is only used in main app files or for contextual information
