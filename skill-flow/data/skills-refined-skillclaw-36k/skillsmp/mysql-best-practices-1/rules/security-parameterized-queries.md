---
title: Always Use Prepared Statements
impact: CRITICAL
impactDescription: Prevents SQL injection attacks completely
tags: security, sql-injection, prepared-statements, parameterized
---

## Always Use Prepared Statements

String concatenation in SQL enables injection attacks. Prepared statements separate SQL structure from data, making injection impossible.

**Incorrect (SQL injection vulnerable):**

```sql
-- ❌ String interpolation in application code
-- PHP example
$query = "SELECT * FROM users WHERE id = " . $_GET['id'];
$query = "SELECT * FROM users WHERE name = '" . $name . "'";

-- Python example
query = f"SELECT * FROM users WHERE id = {user_id}"
query = "SELECT * FROM users WHERE name = '%s'" % name

-- Attack: id = "1; DROP TABLE users; --"
-- Result: SELECT * FROM users WHERE id = 1; DROP TABLE users; --
```

**Correct (prepared statements):**

```sql
-- PHP PDO
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
$stmt->execute([$id]);

-- PHP MySQLi
$stmt = $mysqli->prepare("SELECT * FROM users WHERE id = ?");
$stmt->bind_param("i", $id);
$stmt->execute();

-- Python mysql-connector
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

-- Python SQLAlchemy
session.query(User).filter(User.id == user_id).all()

-- Node.js mysql2
connection.execute("SELECT * FROM users WHERE id = ?", [userId])

-- Java JDBC
PreparedStatement stmt = conn.prepareStatement(
    "SELECT * FROM users WHERE id = ?"
);
stmt.setInt(1, userId);
```

**Multiple parameters:**

```sql
-- PHP
$stmt = $pdo->prepare(
    "SELECT * FROM products WHERE category = ? AND price < ? AND active = ?"
);
$stmt->execute([$category, $maxPrice, true]);

-- Named parameters (where supported)
$stmt = $pdo->prepare(
    "SELECT * FROM users WHERE email = :email AND status = :status"
);
$stmt->execute(['email' => $email, 'status' => $status]);
```

**LIKE with prepared statements:**

```sql
-- ✓ Safe LIKE query
$search = '%' . $searchTerm . '%';
$stmt = $pdo->prepare("SELECT * FROM products WHERE name LIKE ?");
$stmt->execute([$search]);
```

Reference: [Prepared Statements](https://dev.mysql.com/doc/refman/8.0/en/sql-prepared-statements.html)
