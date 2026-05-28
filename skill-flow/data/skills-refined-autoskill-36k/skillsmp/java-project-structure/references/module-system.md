# Java Module System (JPMS)

## Module Declaration

```java
// src/main/java/module-info.java
module com.example.myapp {
    // Required modules (dependencies)
    requires java.base;           // Implicit, always available
    requires java.sql;            // JDK module
    requires java.logging;
    requires spring.boot;         // Third-party module
    requires spring.web;
    requires transitive com.example.common;  // Transitive dependency

    // Exported packages (public API)
    exports com.example.myapp.api;
    exports com.example.myapp.model;
    exports com.example.myapp.dto to com.example.client;  // Qualified export

    // Opened packages (for reflection)
    opens com.example.myapp.model to spring.core, hibernate.core;
    opens com.example.myapp to spring.beans;

    // Service provider
    provides com.example.spi.PaymentProcessor
        with com.example.myapp.StripeProcessor;

    // Service consumer
    uses com.example.spi.NotificationService;
}
```

## Module Keywords

```java
// requires - declare dependency
requires java.sql;                    // Regular dependency
requires transitive spring.core;      // Transitive (consumers get it too)
requires static lombok;               // Optional (compile-time only)

// exports - make packages accessible
exports com.example.api;              // Export to all
exports com.example.internal to com.example.test;  // Qualified export

// opens - allow reflection
opens com.example.model;              // Open to all for reflection
opens com.example.entity to hibernate.core;  // Qualified open

// open module - everything open for reflection
open module com.example.app {
    requires spring.boot;
    exports com.example.api;
}
```

## Automatic Modules

For JARs without module-info.java (most legacy libraries):

```java
// Module name derived from JAR filename or Automatic-Module-Name manifest
// guava-31.1-jre.jar → guava
// commons-lang3-3.12.0.jar → commons.lang3

module com.example.app {
    requires guava;         // Automatic module
    requires commons.lang3; // Automatic module
}
```

**Manifest entry (recommended for libraries):**
```
Automatic-Module-Name: com.google.guava
```

## Module Path vs Class Path

```bash
# Module path (JPMS)
java --module-path mods -m com.example.app/com.example.Main

# Class path (traditional)
java -cp "lib/*:app.jar" com.example.Main

# Mixed (automatic modules on module path)
java --module-path mods --add-modules ALL-MODULE-PATH -cp legacy.jar com.example.Main
```

## Migration Strategy

### 1. Bottom-up Migration

```
1. Identify leaf modules (no internal dependencies)
2. Add module-info.java to leaf modules
3. Move up the dependency tree
4. Use automatic modules for unmigrated dependencies
```

### 2. Handling Reflection

```java
// Spring/Hibernate need reflection access
module com.example.app {
    // Open specific packages
    opens com.example.entity to hibernate.core;
    opens com.example.config to spring.core;

    // Or open entire module
    // open module com.example.app { ... }
}
```

### 3. Split Packages

```java
// PROBLEM: Same package in multiple JARs
// javax.annotation in jsr305.jar AND java.annotation module

// SOLUTION: Exclude duplicate JAR or merge packages
// In Maven: use <exclusions>
```

## Compile and Run

```bash
# Compile
javac -d out --module-source-path src $(find src -name "*.java")

# Package
jar --create --file mods/com.example.app.jar \
    --main-class com.example.Main \
    -C out/com.example.app .

# Run
java --module-path mods -m com.example.app

# With VM args
java --module-path mods \
     --add-opens java.base/java.lang=com.example.app \
     -m com.example.app
```

## Debugging Module Issues

```bash
# Show module resolution
java --show-module-resolution -m com.example.app

# Describe module
jar --describe-module --file=app.jar

# List modules
java --list-modules

# Check for split packages
jdeps --multi-release 21 -s app.jar
```
