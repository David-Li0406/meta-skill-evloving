---
name: GraalVM Native
description: Native image compilation, reflection configuration, and build optimization.
metadata:
  labels: [java, graalvm, native, aot]
  triggers:
    files: ['**/*.java', 'native-image.properties', 'META-INF/native-image/**', 'pom.xml', 'build.gradle']
    keywords: [GraalVM, native-image, reflection-config, reachability-metadata, '@RegisterForReflection']
---

# GraalVM Native Standards

## Building Native Image

```bash
# Maven with Spring Boot
./mvnw -Pnative native:compile

# Maven with Quarkus
./mvnw package -Dnative

# Gradle
./gradlew nativeCompile
```

## Reflection Configuration

```java
// Quarkus - register for reflection
@RegisterForReflection
public class User {
    private String name;
    private String email;
}

// Spring Boot - hints
@Configuration
@ImportRuntimeHints(MyRuntimeHints.class)
public class NativeConfig {}

public class MyRuntimeHints implements RuntimeHintsRegistrar {
    @Override
    public void registerHints(RuntimeHints hints, ClassLoader classLoader) {
        hints.reflection().registerType(User.class,
            MemberCategory.PUBLIC_FIELDS,
            MemberCategory.INVOKE_PUBLIC_CONSTRUCTORS,
            MemberCategory.INVOKE_PUBLIC_METHODS);
    }
}
```

## Native Image Configuration Files

```
src/main/resources/META-INF/native-image/
├── reflect-config.json
├── resource-config.json
├── serialization-config.json
└── native-image.properties
```

```json
// reflect-config.json
[
  {
    "name": "com.example.User",
    "allDeclaredConstructors": true,
    "allPublicMethods": true,
    "allDeclaredFields": true
  }
]
```

```json
// resource-config.json
{
  "resources": {
    "includes": [
      {"pattern": "application\\.yml"},
      {"pattern": "db/migration/.*"}
    ]
  }
}
```

## Performance Tips

```java
// Use build-time initialization
@BuildTimeInit
public class Constants {
    public static final Map<String, String> CONFIG = loadConfig();
}

// Avoid runtime class loading
// DON'T: Class.forName("com.example.MyClass")
// DO: Reference classes directly

// Use static configuration
// Avoid dynamic proxies when possible
```

## References

- [Native Image Config](references/native-image-config.md) - Full configuration options
