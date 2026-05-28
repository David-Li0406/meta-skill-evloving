# Environment Variables

Binding and reading environment variables with Viper.

## Key Behavior

**Environment variables ARE case-sensitive** (unlike config keys).
- `APP_PORT` and `app_port` are different env vars
- Config keys `server.port` and `SERVER.PORT` are the same

## Setting Env Prefix

Prefix all env var lookups. Avoids naming collisions.

```go
viper.SetEnvPrefix("MYAPP")

// Now viper.Get("port") looks for MYAPP_PORT
// viper.Get("server.host") looks for MYAPP_SERVER_HOST
```

## Binding Individual Env Vars

### BindEnv with Key Only

```go
viper.BindEnv("port")
// Looks for: PORT (no prefix) or MYAPP_PORT (with prefix)

value := viper.GetInt("port")
```

### BindEnv with Explicit Var Name

```go
viper.BindEnv("port", "SERVICE_PORT")
// Always looks for SERVICE_PORT, ignores prefix

viper.BindEnv("host", "SERVICE_HOST", "HOSTNAME")
// Tries SERVICE_HOST first, then HOSTNAME
```

## AutomaticEnv

Automatically check env vars for all `Get()` calls.

```go
viper.SetEnvPrefix("APP")
viper.AutomaticEnv()

// viper.GetString("server.host") now checks APP_SERVER_HOST
// viper.GetInt("port") now checks APP_PORT
```

## Key Replacer

Transform config key names to env var names.

```go
// Replace dots with underscores
viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))

// Now:
// viper.Get("server.host") checks APP_SERVER_HOST
// viper.Get("database.connection.timeout") checks APP_DATABASE_CONNECTION_TIMEOUT
```

### Multiple Replacements

```go
viper.SetEnvKeyReplacer(strings.NewReplacer(
    ".", "_",
    "-", "_",
))
// server.api-key → APP_SERVER_API_KEY
```

## Complete Setup Pattern

```go
func initConfig() {
    viper.SetConfigName("config")
    viper.AddConfigPath(".")

    // Env var setup
    viper.SetEnvPrefix("MYAPP")
    viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))
    viper.AutomaticEnv()

    // Set defaults
    viper.SetDefault("server.host", "0.0.0.0")
    viper.SetDefault("server.port", 8080)

    // Read config file (env vars will override)
    viper.ReadInConfig()
}
```

## Precedence Example

```yaml
# config.yaml
server:
  port: 8080
```

```bash
export MYAPP_SERVER_PORT=9000
```

```go
viper.SetEnvPrefix("MYAPP")
viper.AutomaticEnv()
viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))
viper.ReadInConfig()

port := viper.GetInt("server.port")  // 9000 (env wins over file)
```

## Checking Env Var Source

```go
viper.SetEnvPrefix("APP")
viper.AutomaticEnv()

// Check if value came from env or config
if os.Getenv("APP_DEBUG") != "" {
    fmt.Println("Debug mode set via environment")
}
```

## Common Patterns

### 12-Factor App Config

```go
viper.SetEnvPrefix("APP")
viper.AutomaticEnv()
viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))

// Defaults for local dev
viper.SetDefault("database.host", "localhost")
viper.SetDefault("database.port", 5432)

// In production: APP_DATABASE_HOST and APP_DATABASE_PORT override
```

### Optional Config File with Env Override

```go
viper.SetConfigName("config")
viper.AddConfigPath(".")
viper.SetEnvPrefix("APP")
viper.AutomaticEnv()

// Config file optional
_ = viper.ReadInConfig()

// Env vars always work regardless of config file
```

## Gotchas

### Empty String vs Unset

```go
// os.Setenv("APP_NAME", "")  // Set to empty string
// vs not setting APP_NAME at all

// Viper treats empty string as a value
// Use IsSet() to check if key has any value
if viper.IsSet("name") {
    name := viper.GetString("name")  // Could be ""
}
```

### BindEnv Must Be Called Before Get

```go
// This works
viper.BindEnv("port")
viper.GetInt("port")

// AutomaticEnv() is easier - no need to bind each key
viper.AutomaticEnv()
viper.GetInt("port")  // Automatically checks env
```
