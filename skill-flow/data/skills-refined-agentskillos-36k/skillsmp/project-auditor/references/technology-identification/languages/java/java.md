# Java

**Category**: languages
**Description**: Java programming language - object-oriented, platform-independent language for enterprise and Android development
**Homepage**: https://www.java.com

## Package Detection

### MAVEN
- `org.apache.maven:maven-core`
- `javax.*`
- `jakarta.*`

### GRADLE
- `org.gradle:gradle-core`

## Configuration Files

- `pom.xml`
- `build.gradle`
- `build.gradle.kts`
- `settings.gradle`
- `settings.gradle.kts`
- `gradle.properties`
- `gradlew`
- `gradlew.bat`
- `mvnw`
- `mvnw.cmd`
- `.mvn/`
- `.gradle/`
- `MANIFEST.MF`
- `build.xml` (Ant)
- `.java-version`

## File Extensions

- `.java`
- `.jar`
- `.war`
- `.ear`
- `.class`
- `.jks` (keystore)

## Import Detection

### Java
**Pattern**: `^package\s+[\w.]+;`
- Package declaration
- Example: `package com.example.app;`

**Pattern**: `^import\s+[\w.]+;`
- Import statement
- Example: `import java.util.List;`

**Pattern**: `^import\s+static\s+[\w.]+;`
- Static import
- Example: `import static org.junit.Assert.*;`

**Pattern**: `public\s+class\s+\w+`
- Class declaration
- Example: `public class Application {}`

**Pattern**: `public\s+static\s+void\s+main\(`
- Main method
- Example: `public static void main(String[] args) {}`

## Environment Variables

- `JAVA_HOME`
- `JDK_HOME`
- `JAVA_OPTS`
- `MAVEN_HOME`
- `M2_HOME`
- `GRADLE_HOME`
- `GRADLE_USER_HOME`
- `CLASSPATH`

## Version Indicators

- Java 21 LTS (current LTS)
- Java 17 LTS (widely used)
- Java 11 LTS (legacy LTS)
- Java 8 (legacy, still common)

## Detection Notes

- Look for `.java` files in repository
- pom.xml indicates Maven project
- build.gradle indicates Gradle project
- Check for src/main/java directory structure
- Look for wrapper scripts (mvnw, gradlew)

## Detection Confidence

- **File Extension Detection**: 95% (HIGH)
- **Build File Detection**: 95% (HIGH)
- **Package Detection**: 90% (HIGH)
