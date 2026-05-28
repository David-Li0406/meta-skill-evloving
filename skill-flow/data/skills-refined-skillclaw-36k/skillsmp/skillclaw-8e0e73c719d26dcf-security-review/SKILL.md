---
name: security-review
description: Use this skill when a user requests a security review, security check, vulnerability scan, or mentions security.
---

# Security Review Skill

## Desktop Application Security Focus
- ✅ Local data protection, API key management, Tauri command security, SQL injection prevention
- ❌ Not applicable: CSRF, CSP (Web application security measures)

## Security Checklist

### 1. Key Management
- [ ] No hardcoded API keys, passwords, tokens
- [ ] All keys use environment variables
- [ ] Sensitive configurations are stored encrypted

```rust
// ✓ Correct
let api_key = env::var("OPENAI_API_KEY")?;

// ✗ Incorrect
const API_KEY: &str = "sk-1234567890";
```

### 2. Tauri Command Security
- [ ] All command parameters are validated
- [ ] Use validator crate
- [ ] Error messages do not expose internal information

```rust
#[derive(Deserialize, Validate, Type)]
pub struct CreateFormulaDto {
    #[validate(length(min = 2, max = 50))]
    pub name: String,
}

#[tauri::command]
#[specta::specta]
pub async fn create_formula(dto: CreateFormulaDto) -> ApiResponse<Formula> {
    if let Err(e) = dto.validate() {
        return api_err(format!("Input validation failed: {}", e));
    }
    // ...
}
```

### 3. SQL Injection Prevention
- [ ] Use SQLx parameterized queries
- [ ] Prohibit string concatenation in SQL
- [ ] Use QueryBuilder for dynamic queries

```rust
// ✓ Correct
sqlx::query_as!(Formula, "SELECT * FROM formulas WHERE name = ?", name)

// ✗ Incorrect
let sql = format!("SELECT * FROM formulas WHERE name = '{}'", name);
```

### 4. Input Validation
- [ ] Frontend validation (first line of defense)
- [ ] Backend validation (must be present)
- [ ] File path validation to prevent path traversal

```rust
pub fn validate_file_path(path: &str) -> Result<PathBuf> {
    let path = Path::new(path);
    if path.components().any(|c| c == std::path::Component::ParentDir) {
        return Err(anyhow!("Using .. paths is not allowed"));
    }
    Ok(path.to_path_buf())
}
```

### 5. Sensitive Data Protection
- [ ] No keys or passwords in logs
- [ ] Error messages do not expose internal information

```rust
// ✓ Correct
info!(formula_id = formula.id, "Formula created successfully");

// ✗ Incorrect
info!("API Key: {}", api_key);
```

### 6. Dependency Security
```bash
cargo audit      # Check for security vulnerabilities
cargo outdated   # Check for outdated dependencies
cargo update     # Update dependencies
```

## Security Review Trigger Conditions
- [ ] Adding new Tauri commands
- [ ] Modifying database access layer
- [ ] Handling user file uploads/imports
- [ ] Integrating third-party APIs
- [ ] Adding new configuration items

## Pre-Submission Checks
- [ ] `cargo clippy` has no security warnings
- [ ] `cargo audit` has no known vulnerabilities
- [ ] No hardcoded keys
- [ ] All SQL queries use parameterization
- [ ] All Tauri command parameters are validated
- [ ] No sensitive information in logs

## Common Security Pitfalls
1. **Trusting frontend validation** → Backend must validate again
2. **Logging sensitive information** → Only log necessary information
3. **SQL string concatenation** → Use parameterized queries
4. **Overly detailed error messages** → Return generic error messages