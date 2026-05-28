# Maven Project Layout

## Standard Directory Structure

```
project/
├── pom.xml
├── src/
│   ├── main/
│   │   ├── java/                    # Java source files
│   │   ├── resources/               # Resources bundled in JAR
│   │   │   ├── application.yml
│   │   │   ├── logback.xml
│   │   │   └── META-INF/
│   │   └── filters/                 # Resource filter files
│   └── test/
│       ├── java/                    # Test source files
│       └── resources/               # Test resources
│           └── application-test.yml
├── target/                          # Build output (generated)
└── .mvn/                            # Maven wrapper
    └── wrapper/
        └── maven-wrapper.properties
```

## POM Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
    </parent>

    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <properties>
        <java.version>21</java.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

    <profiles>
        <profile>
            <id>dev</id>
            <activation>
                <activeByDefault>true</activeByDefault>
            </activation>
            <properties>
                <spring.profiles.active>dev</spring.profiles.active>
            </properties>
        </profile>
        <profile>
            <id>prod</id>
            <properties>
                <spring.profiles.active>prod</spring.profiles.active>
            </properties>
        </profile>
    </profiles>
</project>
```

## Multi-Module Project

```
parent/
├── pom.xml                 # Parent POM
├── common/
│   ├── pom.xml
│   └── src/main/java/
├── api/
│   ├── pom.xml
│   └── src/main/java/
└── service/
    ├── pom.xml
    └── src/main/java/
```

**Parent POM:**

```xml
<project>
    <groupId>com.example</groupId>
    <artifactId>parent</artifactId>
    <version>1.0.0</version>
    <packaging>pom</packaging>

    <modules>
        <module>common</module>
        <module>api</module>
        <module>service</module>
    </modules>

    <dependencyManagement>
        <dependencies>
            <!-- Shared dependency versions -->
            <dependency>
                <groupId>com.example</groupId>
                <artifactId>common</artifactId>
                <version>${project.version}</version>
            </dependency>
        </dependencies>
    </dependencyManagement>
</project>
```

**Child POM:**

```xml
<project>
    <parent>
        <groupId>com.example</groupId>
        <artifactId>parent</artifactId>
        <version>1.0.0</version>
    </parent>

    <artifactId>api</artifactId>

    <dependencies>
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>common</artifactId>
        </dependency>
    </dependencies>
</project>
```

## Resource Filtering

```xml
<!-- pom.xml -->
<build>
    <resources>
        <resource>
            <directory>src/main/resources</directory>
            <filtering>true</filtering>
        </resource>
    </resources>
</build>
```

```yaml
# application.yml
app:
  version: @project.version@
  build-time: @maven.build.timestamp@
```

## Common Commands

```bash
# Build
mvn clean install

# Skip tests
mvn clean install -DskipTests

# Run specific profile
mvn clean install -Pprod

# Dependency tree
mvn dependency:tree

# Effective POM
mvn help:effective-pom

# Update versions
mvn versions:set -DnewVersion=2.0.0

# Check for dependency updates
mvn versions:display-dependency-updates
```
