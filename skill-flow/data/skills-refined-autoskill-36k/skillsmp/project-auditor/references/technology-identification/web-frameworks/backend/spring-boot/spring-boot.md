# Spring Boot

**Category**: web-frameworks/backend
**Description**: Spring Boot makes it easy to create stand-alone, production-grade Spring applications

## Package Detection

### MAVEN
- `spring-boot-starter-web`
- `spring-boot-starter`
- `spring-boot`

### GRADLE
- `org.springframework.boot:spring-boot-starter-web`
- `org.springframework.boot:spring-boot-starter`

### Related Packages
- `spring-boot-starter-data-jpa`
- `spring-boot-starter-security`
- `spring-boot-starter-test`
- `spring-boot-starter-actuator`
- `spring-boot-devtools`

## Import Detection

### Java
File extensions: .java

**Pattern**: `import org\.springframework\.boot\.`
- Spring Boot core imports
- Example: `import org.springframework.boot.SpringApplication;`

**Pattern**: `@SpringBootApplication`
- Spring Boot application annotation
- Example: `@SpringBootApplication public class Application {...}`

**Pattern**: `@RestController|@Controller`
- Spring MVC controller annotations
- Example: `@RestController public class UserController {...}`

**Pattern**: `@GetMapping|@PostMapping|@PutMapping|@DeleteMapping`
- Spring request mapping annotations
- Example: `@GetMapping("/users") public List<User> getUsers() {...}`

### Common Imports
- `org.springframework.boot.SpringApplication`
- `org.springframework.boot.autoconfigure.SpringBootApplication`
- `org.springframework.web.bind.annotation.*`

## Environment Variables

*Spring Boot environment variables*

- `SPRING_APPLICATION_NAME`
- `SPRING_PROFILES_ACTIVE`
- `SERVER_PORT`
- `SPRING_DATASOURCE_URL`

## Configuration Files

- `pom.xml`
- `build.gradle`
- `application.properties`
- `application.yml`
- `application.yaml`

## Detection Notes

- Spring Boot is Java-based
- Uses Maven or Gradle
- Starter dependencies simplify setup

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 70% (MEDIUM)
- **API Endpoint Detection**: 75% (MEDIUM)
