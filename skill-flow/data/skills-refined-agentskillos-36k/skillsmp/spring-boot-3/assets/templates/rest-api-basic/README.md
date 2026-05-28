# Basic REST API Template

A production-ready Spring Boot 3.x REST API template with best practices.

## Quick Start

```bash
# Generate project at https://start.spring.io
# Dependencies: Web, JPA, PostgreSQL, Validation, Actuator, Lombok, Test

# Or use Maven:
mvn archetype:generate \
  -DgroupId=com.example \
  -DartifactId=demo \
  -DarchetypeArtifactId=maven-archetype-quickstart \
  -DinteractiveMode=false
```

## Project Structure

```
src/main/java/com/example/demo/
├── DemoApplication.java          # Main application
├── config/
│   ├── SecurityConfig.java       # Security configuration
│   └── OpenApiConfig.java        # API documentation
├── controller/
│   └── UserController.java       # REST endpoints
├── service/
│   └── UserService.java          # Business logic
├── repository/
│   └── UserRepository.java       # Data access
├── model/
│   └── User.java                 # JPA entity
├── dto/
│   └── UserDTO.java              # API response
├── request/
│   └── CreateUserRequest.java    # API request
├── exception/
│   ├── ResourceNotFoundException.java
│   ├── DuplicateResourceException.java
│   └── GlobalExceptionHandler.java
└── mapper/
    └── UserMapper.java           # Entity-DTO mapping
```

## Essential Files

### pom.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
        <relativePath/>
    </parent>

    <groupId>com.example</groupId>
    <artifactId>demo</artifactId>
    <version>1.0.0</version>
    <name>Demo Application</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>17</java.version>
        <springdoc.version>2.2.0</springdoc.version>
    </properties>

    <dependencies>
        <!-- Spring Boot Web -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <!-- Spring Data JPA -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>

        <!-- Validation -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>

        <!-- PostgreSQL Driver -->
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
        </dependency>

        <!-- Lombok -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>

        <!-- Actuator -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>

        <!-- OpenAPI/Swagger -->
        <dependency>
            <groupId>org.springdoc</groupId>
            <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
            <version>${springdoc.version}</version>
        </dependency>

        <!-- Test -->
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
                <configuration>
                    <excludes>
                        <exclude>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

### application.yml

```yaml
spring:
  application:
    name: demo

  datasource:
    url: jdbc:postgresql://localhost:5432/demo
    username: ${DB_USERNAME:postgres}
    password: ${DB_PASSWORD:postgres}
    driver-class-name: org.postgresql.Driver
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5

  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false
    properties:
      hibernate:
        dialect: org.hibernate.dialect.PostgreSQLDialect
        format_sql: true

server:
  port: 8080

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
  endpoint:
    health:
      show-details: always

springdoc:
  api-docs:
    path: /api-docs
  swagger-ui:
    path: /swagger-ui.html
```

### DemoApplication.java

```java
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

## Configuration Files

### OpenApiConfig.java

```java
package com.example.demo.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.Contact;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("Demo API")
                .version("1.0.0")
                .description("Spring Boot REST API")
                .contact(new Contact()
                    .name("Developer")
                    .email("dev@example.com")));
    }
}
```

## Running the Application

```bash
# Development
mvn spring-boot:run

# Build JAR
mvn clean package
java -jar target/demo-1.0.0.jar

# With profile
java -jar target/demo-1.0.0.jar --spring.profiles.active=prod
```

## Accessing the Application

- **API**: http://localhost:8080/api/
- **Swagger UI**: http://localhost:8080/swagger-ui.html
- **Actuator**: http://localhost:8080/actuator/health
- **API Docs**: http://localhost:8080/api-docs

## Next Steps

1. Copy this template structure
2. Rename `com.example.demo` to your package
3. Configure database connection
4. Add your entities, services, controllers
5. Run tests: `mvn test`
6. Build and deploy

## See Also

- [Secure REST API Template](../rest-api-secure/) - Adds JWT authentication
- [Microservice Template](../microservice/) - Adds Spring Cloud features
