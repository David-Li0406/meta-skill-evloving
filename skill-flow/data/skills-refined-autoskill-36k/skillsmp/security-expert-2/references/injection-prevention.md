# SQL Injection Prevention Reference

## Table of Contents
1. [SQL Injection Fundamentals](#fundamentals)
2. [Attack Vectors](#attack-vectors)
3. [Java/JDBC Safe Patterns](#jdbc-patterns)
4. [Spring Data JPA Patterns](#spring-data-jpa)
5. [JPA/Hibernate Protections](#jpa-hibernate)
6. [Input Validation vs Output Encoding](#validation-encoding)
7. [Testing for Injection](#testing)

## SQL Injection Fundamentals {#fundamentals}

### What Is SQL Injection?
Attacker manipulates SQL queries by injecting malicious input through user-controlled data.

### Impact
- **Data breach**: Read entire database
- **Data manipulation**: Modify/delete records
- **Authentication bypass**: Login as any user
- **Privilege escalation**: Become admin
- **Command execution**: In some databases, execute OS commands

### Why It Happens
```java
// Vulnerable: User input directly concatenated into SQL
String query = "SELECT * FROM users WHERE username = '" + username + "'";
```

Input: `admin' OR '1'='1`

Resulting query:
```sql
SELECT * FROM users WHERE username = 'admin' OR '1'='1'
-- Returns ALL users
```

## Attack Vectors {#attack-vectors}

### Classic Injection
```
Input: ' OR '1'='1
Input: ' OR '1'='1' --
Input: '; DROP TABLE users; --
```

### Union-Based Injection
```sql
-- Attacker extracts data from other tables
Input: ' UNION SELECT username, password FROM admin_users --
```

### Blind Injection
```sql
-- Boolean-based: different responses for true/false
Input: ' AND 1=1 --  (returns data)
Input: ' AND 1=2 --  (returns nothing)

-- Time-based: delays indicate true conditions
Input: ' AND SLEEP(5) --
```

### Second-Order Injection
Data stored safely, but used unsafely later:
```java
// Safe: Parameterized insert
userRepo.save(new User(userInput));

// Later, UNSAFE: Building query from stored data
String query = "SELECT * FROM logs WHERE user = '" + user.getName() + "'";
// If userInput was "admin'--", injection happens here
```

## Java/JDBC Safe Patterns {#jdbc-patterns}

### Parameterized Queries (PreparedStatement)
```java
// ❌ VULNERABLE: String concatenation
public User findUser(String username) {
    String sql = "SELECT * FROM users WHERE username = '" + username + "'";
    return jdbcTemplate.queryForObject(sql, userMapper);
}

// ✅ SAFE: PreparedStatement with parameters
public User findUser(String username) {
    String sql = "SELECT * FROM users WHERE username = ?";
    return jdbcTemplate.queryForObject(sql, userMapper, username);
}

// ✅ SAFE: Named parameters
public User findUser(String username) {
    String sql = "SELECT * FROM users WHERE username = :username";
    MapSqlParameterSource params = new MapSqlParameterSource()
        .addValue("username", username);
    return namedJdbcTemplate.queryForObject(sql, params, userMapper);
}
```

### Dynamic Column/Table Names
Parameters protect values, NOT identifiers. For dynamic table/column names, use allowlists:

```java
// ❌ VULNERABLE: Dynamic column name from user input
public List<User> sortBy(String column) {
    String sql = "SELECT * FROM users ORDER BY " + column;  // Injection!
    return jdbcTemplate.query(sql, userMapper);
}

// ✅ SAFE: Allowlist of permitted columns
private static final Set<String> ALLOWED_SORT_COLUMNS = Set.of(
    "username", "created_at", "email"
);

public List<User> sortBy(String column) {
    if (!ALLOWED_SORT_COLUMNS.contains(column)) {
        throw new IllegalArgumentException("Invalid sort column: " + column);
    }
    String sql = "SELECT * FROM users ORDER BY " + column;
    return jdbcTemplate.query(sql, userMapper);
}

// ✅ BETTER: Map to enum
public enum SortColumn {
    USERNAME("username"),
    CREATED("created_at"),
    EMAIL("email");

    private final String columnName;
    // constructor, getter
}

public List<User> sortBy(SortColumn column) {
    String sql = "SELECT * FROM users ORDER BY " + column.getColumnName();
    return jdbcTemplate.query(sql, userMapper);
}
```

### IN Clauses
```java
// ❌ VULNERABLE: Building IN clause with string concatenation
public List<User> findByIds(List<Long> ids) {
    String idList = ids.stream().map(String::valueOf).collect(Collectors.joining(","));
    String sql = "SELECT * FROM users WHERE id IN (" + idList + ")";
    return jdbcTemplate.query(sql, userMapper);
}

// ✅ SAFE: Using parameter expansion
public List<User> findByIds(List<Long> ids) {
    String sql = "SELECT * FROM users WHERE id IN (:ids)";
    MapSqlParameterSource params = new MapSqlParameterSource()
        .addValue("ids", ids);
    return namedJdbcTemplate.query(sql, params, userMapper);
}
```

### LIKE Clauses
```java
// ❌ VULNERABLE: User input in LIKE pattern
public List<User> search(String term) {
    String sql = "SELECT * FROM users WHERE name LIKE '%" + term + "%'";
    return jdbcTemplate.query(sql, userMapper);
}

// ✅ SAFE: Parameterized LIKE
public List<User> search(String term) {
    String sql = "SELECT * FROM users WHERE name LIKE ?";
    String pattern = "%" + escapeLikePattern(term) + "%";
    return jdbcTemplate.query(sql, userMapper, pattern);
}

// Escape LIKE wildcards in user input
private String escapeLikePattern(String input) {
    return input
        .replace("\\", "\\\\")
        .replace("%", "\\%")
        .replace("_", "\\_");
}
```

## Spring Data JPA Patterns {#spring-data-jpa}

### Derived Query Methods (Always Safe)
```java
public interface UserRepository extends JpaRepository<User, Long> {

    // ✅ SAFE: Method name parsed, parameters bound automatically
    List<User> findByUsername(String username);
    List<User> findByEmailContaining(String email);
    List<User> findByCreatedAtBetween(Instant start, Instant end);
    Optional<User> findByUsernameAndActiveTrue(String username);

    // ✅ SAFE: Even complex queries
    List<User> findByRolesNameInAndStatusNotAndCreatedAtAfter(
        List<String> roleNames, Status status, Instant date);
}
```

### @Query with JPQL (Safe with Parameters)
```java
public interface UserRepository extends JpaRepository<User, Long> {

    // ✅ SAFE: Named parameters
    @Query("SELECT u FROM User u WHERE u.username = :username")
    Optional<User> findByUsername(@Param("username") String username);

    // ✅ SAFE: Positional parameters
    @Query("SELECT u FROM User u WHERE u.email = ?1 AND u.active = ?2")
    List<User> findActiveByEmail(String email, boolean active);

    // ✅ SAFE: Complex queries with parameters
    @Query("""
        SELECT u FROM User u
        JOIN u.roles r
        WHERE r.name = :role
        AND u.createdAt > :since
        """)
    List<User> findByRoleSince(@Param("role") String role, @Param("since") Instant since);
}
```

### Native Queries (Caution Required)
```java
public interface UserRepository extends JpaRepository<User, Long> {

    // ✅ SAFE: Native query with parameters
    @Query(value = "SELECT * FROM users WHERE username = :username", nativeQuery = true)
    Optional<User> findByUsernameNative(@Param("username") String username);

    // ❌ VULNERABLE: SpEL expression with user input (rare but dangerous)
    // Don't use SpEL to build dynamic SQL from user input
    @Query("SELECT u FROM User u WHERE u.status = :#{#filter.status}")
    List<User> findWithFilter(@Param("filter") UserFilter filter);
    // This is safe IF filter.status is validated, but pattern is risky
}
```

### Dynamic Queries with Specifications (Safe)
```java
// ✅ SAFE: Criteria API based, always parameterized
public class UserSpecifications {

    public static Specification<User> hasUsername(String username) {
        return (root, query, cb) -> cb.equal(root.get("username"), username);
    }

    public static Specification<User> hasStatus(Status status) {
        return (root, query, cb) -> cb.equal(root.get("status"), status);
    }

    public static Specification<User> createdAfter(Instant date) {
        return (root, query, cb) -> cb.greaterThan(root.get("createdAt"), date);
    }
}

// Usage
userRepository.findAll(
    hasUsername(search).and(hasStatus(ACTIVE)).and(createdAfter(lastWeek))
);
```

### Querydsl (Safe)
```java
// ✅ SAFE: Type-safe queries, always parameterized
public List<User> searchUsers(String username, Status status) {
    QUser user = QUser.user;

    BooleanBuilder predicate = new BooleanBuilder();

    if (username != null) {
        predicate.and(user.username.containsIgnoreCase(username));
    }
    if (status != null) {
        predicate.and(user.status.eq(status));
    }

    return queryFactory
        .selectFrom(user)
        .where(predicate)
        .fetch();
}
```

## JPA/Hibernate Protections {#jpa-hibernate}

### JPQL Parameterized Queries
```java
// ✅ SAFE: Named parameters
public List<User> findUsers(String username) {
    return entityManager
        .createQuery("SELECT u FROM User u WHERE u.username = :username", User.class)
        .setParameter("username", username)
        .getResultList();
}

// ✅ SAFE: Positional parameters
public User findUser(String email, Status status) {
    return entityManager
        .createQuery("SELECT u FROM User u WHERE u.email = ?1 AND u.status = ?2", User.class)
        .setParameter(1, email)
        .setParameter(2, status)
        .getSingleResult();
}
```

### Criteria API (Always Safe)
```java
// ✅ SAFE: Programmatic query building, always parameterized
public List<User> searchUsers(UserSearchCriteria criteria) {
    CriteriaBuilder cb = entityManager.getCriteriaBuilder();
    CriteriaQuery<User> cq = cb.createQuery(User.class);
    Root<User> user = cq.from(User.class);

    List<Predicate> predicates = new ArrayList<>();

    if (criteria.getUsername() != null) {
        predicates.add(cb.equal(user.get("username"), criteria.getUsername()));
    }
    if (criteria.getMinAge() != null) {
        predicates.add(cb.greaterThanOrEqualTo(user.get("age"), criteria.getMinAge()));
    }

    cq.where(predicates.toArray(new Predicate[0]));
    return entityManager.createQuery(cq).getResultList();
}
```

### Native Queries (Requires Care)
```java
// ✅ SAFE: Parameterized native query
public List<Object[]> complexReport(String department) {
    return entityManager
        .createNativeQuery("SELECT * FROM complex_view WHERE dept = ?1")
        .setParameter(1, department)
        .getResultList();
}

// ❌ VULNERABLE: String concatenation in native query
public List<Object[]> vulnerableReport(String table) {
    return entityManager
        .createNativeQuery("SELECT * FROM " + table)  // Injection!
        .getResultList();
}
```

## Input Validation vs Output Encoding {#validation-encoding}

### Key Distinction
- **Input validation**: Reject bad input early (defense in depth)
- **Parameterized queries**: Primary protection (prevents injection)
- **Output encoding**: For display (prevents XSS, different from SQLi)

### Input Validation (Defense in Depth)
```java
public record UserSearchRequest(
    @NotBlank @Size(max = 100) @Pattern(regexp = "^[a-zA-Z0-9_]+$")
    String username,

    @Email
    String email,

    @Min(1) @Max(150)
    Integer age
) {}

@GetMapping("/users/search")
public List<User> search(@Valid UserSearchRequest request) {
    // Even with validation, STILL use parameterized queries
    return userRepository.findByUsernameContaining(request.username());
}
```

### What Validation Catches
- Obviously malicious patterns (`'; DROP TABLE`)
- Invalid format (email validation)
- Length limits (prevent buffer issues)
- Type constraints (age must be number)

### Why Validation Alone Isn't Enough
```java
// Validated input: "O'Brien" - valid name, but contains quote
// Without parameterization: "WHERE name = 'O'Brien'" breaks!

// Parameterized queries handle this correctly
// WHERE name = ?  with parameter "O'Brien" → safe
```

## Testing for Injection {#testing}

### Manual Testing Payloads
```
' OR '1'='1
' OR '1'='1' --
' UNION SELECT null,null,null --
'; WAITFOR DELAY '0:0:5' --
' AND (SELECT COUNT(*) FROM users) > 0 --
```

### JUnit Tests for SQL Injection
```java
@Test
void findByUsername_shouldNotBeVulnerableToInjection() {
    // Create legitimate user
    userRepository.save(new User("admin", "admin@test.com"));

    // Attempt injection
    String maliciousInput = "admin' OR '1'='1";
    List<User> result = userRepository.findByUsername(maliciousInput);

    // Should find no users (literal search for "admin' OR '1'='1")
    assertThat(result).isEmpty();
}

@Test
void search_shouldHandleSpecialCharactersSafely() {
    userRepository.save(new User("O'Brien", "obrien@test.com"));

    // Should find the user, not cause SQL error
    List<User> result = userRepository.findByUsername("O'Brien");
    assertThat(result).hasSize(1);
}

@Test
void search_shouldNotReturnAllUsersWithInjection() {
    userRepository.save(new User("alice", "alice@test.com"));
    userRepository.save(new User("bob", "bob@test.com"));

    // Classic injection attempt
    List<User> result = userRepository.findByUsername("' OR '1'='1");

    // Should NOT return all users
    assertThat(result).isEmpty();
}
```

### Automated Tools
```bash
# sqlmap - automated SQL injection testing
sqlmap -u "http://localhost:8080/api/users?username=test" --dbs

# OWASP ZAP - web app scanner with SQLi detection
zap-cli quick-scan http://localhost:8080

# Burp Suite - intercept and modify requests
```

### Security Testing in CI/CD
```yaml
# Include in pipeline
- name: OWASP Dependency Check
  run: ./gradlew dependencyCheckAnalyze

- name: Static Analysis (SpotBugs with FindSecBugs)
  run: ./gradlew spotbugsMain

- name: SAST Scan
  run: semgrep --config=p/java
```

## Quick Reference

### Always Safe
- Spring Data JPA derived methods
- `@Query` with named/positional parameters
- Criteria API / Querydsl
- `JdbcTemplate` with `?` placeholders

### Requires Care
- Native queries (use parameters)
- Dynamic table/column names (use allowlist)
- LIKE patterns (escape wildcards)
- IN clauses (use parameter expansion)

### Never Do
- String concatenation with user input
- `String.format()` for SQL
- Dynamic SQL from stored user data without validation

### Defense Layers
1. **Primary**: Parameterized queries (prevents injection)
2. **Secondary**: Input validation (rejects obvious attacks)
3. **Tertiary**: Least privilege DB accounts (limits damage)
4. **Monitoring**: Log/alert on SQL errors (detect attempts)
