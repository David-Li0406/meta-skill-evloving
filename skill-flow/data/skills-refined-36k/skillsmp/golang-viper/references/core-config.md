# Core Configuration

Reading config files, setting defaults, and managing config paths.

## Setting Config File Location

```go
// Config file name (without extension)
viper.SetConfigName("config")

// Explicit file type (optional if extension present)
viper.SetConfigType("yaml")  // json, toml, yaml, ini, envfile, properties

// Search paths (checked in order added)
viper.AddConfigPath("/etc/myapp/")
viper.AddConfigPath("$HOME/.myapp")
viper.AddConfigPath("./config")
viper.AddConfigPath(".")
```

## Reading Config Files

### Basic Reading

```go
err := viper.ReadInConfig()
if err != nil {
    panic(fmt.Errorf("fatal config error: %w", err))
}
```

### Handle Missing File Gracefully

```go
if err := viper.ReadInConfig(); err != nil {
    if _, ok := err.(viper.ConfigFileNotFoundError); ok {
        // Config file not found; use defaults only
        fmt.Println("No config file found, using defaults")
    } else {
        // Config file found but error reading it
        return fmt.Errorf("error reading config: %w", err)
    }
}
```

### Read From Specific Path

```go
viper.SetConfigFile("/path/to/config.yaml")
err := viper.ReadInConfig()
```

### Read From io.Reader

```go
viper.SetConfigType("yaml")

yamlData := []byte(`
server:
  host: localhost
  port: 8080
`)

viper.ReadConfig(bytes.NewBuffer(yamlData))
```

## Setting Defaults

Set before calling `ReadInConfig()`. Defaults are lowest priority.

```go
// Simple values
viper.SetDefault("server.host", "0.0.0.0")
viper.SetDefault("server.port", 8080)
viper.SetDefault("debug", false)

// Maps
viper.SetDefault("database", map[string]interface{}{
    "host": "localhost",
    "port": 5432,
    "name": "myapp",
})

// Slices
viper.SetDefault("allowed_origins", []string{"http://localhost:3000"})
```

## Runtime Overrides with Set

`Set()` has highest priority, overrides everything.

```go
viper.Set("verbose", true)
viper.Set("server.port", 9000)
```

## Multiple Config Files

Use separate Viper instances for different config files.

```go
// Main config (settings)
mainViper := viper.New()
mainViper.SetConfigName("config")
mainViper.AddConfigPath(".")
mainViper.ReadInConfig()

// Secrets config (credentials)
secretsViper := viper.New()
secretsViper.SetConfigName("secrets")
secretsViper.AddConfigPath(".")
if err := secretsViper.ReadInConfig(); err != nil {
    if _, ok := err.(viper.ConfigFileNotFoundError); ok {
        fmt.Println("Warning: secrets.yaml not found")
    } else {
        return err
    }
}

// Use both
host := mainViper.GetString("server.host")
apiKey := secretsViper.GetString("api_key")
```

## Merging Multiple Config Files

Read additional configs that merge with existing values.

```go
viper.SetConfigName("config")
viper.ReadInConfig()

// Merge in overrides (won't error if file missing)
viper.SetConfigName("config.local")
viper.MergeInConfig()
```

## Getting the Config File Used

```go
fmt.Println("Config file used:", viper.ConfigFileUsed())
```

## Supported File Formats

| Format | Extensions | SetConfigType |
|--------|------------|---------------|
| YAML | .yaml, .yml | "yaml" |
| JSON | .json | "json" |
| TOML | .toml | "toml" |
| INI | .ini | "ini" |
| ENV | .env | "envfile" |
| Properties | .properties | "properties" |

## Key Access Patterns

Nested keys use dot notation.

```yaml
# config.yaml
server:
  host: localhost
  port: 8080
database:
  connection:
    timeout: 30
```

```go
viper.GetString("server.host")           // "localhost"
viper.GetInt("server.port")              // 8080
viper.GetInt("database.connection.timeout") // 30
```

## Check If Key Exists

```go
if viper.IsSet("server.api_key") {
    // Key has a value (not just default)
}
```

## Get All Settings

```go
all := viper.AllSettings()  // map[string]interface{}

// Get sub-tree as map
serverSettings := viper.Sub("server").AllSettings()
```
