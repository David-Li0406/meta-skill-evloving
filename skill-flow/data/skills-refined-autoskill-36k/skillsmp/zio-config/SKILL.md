---
name: zio-config
description: Standardized patterns for creating and reading ZIO configuration using zio-config with magnolia derivation. Use when creating new configuration classes, reading configuration values, or refactoring existing config code to follow project standards.
---

# ZIO Config Pattern

## Overview

Use these patterns to maintain consistency across the codebase when working with ZIO configuration.

## Config Definition Pattern

Create config classes following this structure:

1. **Wrapper case class** - Define a final case class containing the config values
2. **Given Config[T]** - Create using `deriveConfig[T]` from `zio.config.magnolia`
3. **Namespace nesting** - Nest config under appropriate namespaces using `.nested()`
4. **Strong typing** - Parse values to domain types with custom `DeriveConfig[T]` instances

### Namespace Nesting

**Important:** zio-config applies `nested()` parameters in **reverse order**.

```scala
given config: Config[GraphqlCorsConfig] = deriveConfig[GraphqlCorsConfig]
  .nested("cors")
  .nested("graphql")
```

This searches the `graphql.cors` namespace (not `cors.graphql`).

### Examples

**Simple config:**

```scala
final case class GraphqlCorsConfig(allowedOrigin: String)

object GraphqlCorsConfig {
  given config: Config[GraphqlCorsConfig] =
    deriveConfig[GraphqlCorsConfig]
      .nested("cors")
      .nested("graphql")
}
```

**Config with strong types:**

```scala
case class ConnectionSecretsServiceConfig(namespace: String, kmsKeyArn: Arn)

object ConnectionSecretsServiceConfig {
  given arnConfig: DeriveConfig[Arn] =
    DeriveConfig[String].map(Arn.fromString)

  given config: Config[ConnectionSecretsServiceConfig] =
    deriveConfig[ConnectionSecretsServiceConfig]
      .nested("connection-secrets-service")
}
```

**Prompt for namespace** - When creating new configs, ask the user which namespace to nest the config under.

## Config Reading Pattern

Use `ZIO.config[T]` to read configuration values.

### Simple ZLayer

For layers with constructor dependencies, use `ZLayer.derive[T]`:

```scala
final case class MyService(config: MyConfig, otherDep: OtherService)

object MyService {
  val layer: ZLayer[OtherService, Config.Error, MyService] =
    ZLayer.derive[MyService]
}
```

The macro automatically calls `ZIO.config[MyConfig]` when constructing the service.

### Complex ZLayer

For layers requiring custom initialization logic, use `ZLayer.fromZIO` with `ZIO.config[T]`:

```scala
val devLayer: ZLayer[Any, Config.Error, DynamoDbClient] = ZLayer.fromZIO {
  for {
    config <- ZIO.config[LocalDynamoDbConfig]
    tables <- DynamoDbConfig.tables
    client  = DynamoDbClient
                .builder()
                .endpointOverride(URI.create(s"http://${config.host}:${config.port}"))
                .credentialsProvider(
                  StaticCredentialsProvider.create(
                    AwsBasicCredentials.create("dummyKey", "dummySecret")
                  )
                )
                .region(US_EAST_1)
                .build()
    _       = LocalDynamoDb.createTablesIfNotExists(client, tables)
  } yield client
}
```

## Required Imports

```scala
import zio.Config
import zio.config.magnolia.deriveConfig
```

For strong typing:
```scala
import zio.config.magnolia.DeriveConfig
```
