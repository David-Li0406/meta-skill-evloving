# Viper Config Loading

## Basic Usage

```go
import "github.com/spf13/viper"

func LoadConfig() error {
    // Config file name (without extension)
    viper.SetConfigName("config")
    
    // Config file type
    viper.SetConfigType("yaml")
    
    // Search paths
    viper.AddConfigPath(".")
    viper.AddConfigPath("./config")
    viper.AddConfigPath("$HOME/.myapp")
    
    // Read config
    if err := viper.ReadInConfig(); err != nil {
        if _, ok := err.(viper.ConfigFileNotFoundError); ok {
            // Config file not found, use defaults
        } else {
            return err
        }
    }
    
    return nil
}

// Access values
func main() {
    LoadConfig()
    
    host := viper.GetString("server.host")
    port := viper.GetInt("server.port")
    debug := viper.GetBool("debug")
    timeout := viper.GetDuration("timeout")
    hosts := viper.GetStringSlice("allowed_hosts")
}
```

## Defaults

```go
func SetDefaults() {
    viper.SetDefault("server.host", "localhost")
    viper.SetDefault("server.port", 8080)
    viper.SetDefault("database.driver", "postgres")
    viper.SetDefault("log.level", "info")
    viper.SetDefault("timeout", "30s")
}
```

## Environment Variables

```go
func LoadConfig() {
    // Prefix for env vars (e.g., MYAPP_SERVER_PORT)
    viper.SetEnvPrefix("MYAPP")
    
    // Replace dots with underscores in env var names
    viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))
    
    // Automatically bind all keys to env vars
    viper.AutomaticEnv()
    
    // Or bind specific keys
    viper.BindEnv("server.port", "PORT") // Binds PORT env var
}

// Example: MYAPP_SERVER_PORT=9000 overrides server.port
```

## Unmarshal to Struct

```go
type Config struct {
    Server   ServerConfig   `mapstructure:"server"`
    Database DatabaseConfig `mapstructure:"database"`
    Log      LogConfig      `mapstructure:"log"`
}

type ServerConfig struct {
    Host string `mapstructure:"host"`
    Port int    `mapstructure:"port"`
}

type DatabaseConfig struct {
    Driver   string `mapstructure:"driver"`
    Host     string `mapstructure:"host"`
    Port     int    `mapstructure:"port"`
    Name     string `mapstructure:"name"`
    User     string `mapstructure:"user"`
    Password string `mapstructure:"password"`
}

type LogConfig struct {
    Level  string `mapstructure:"level"`
    Format string `mapstructure:"format"`
}

func LoadConfig() (*Config, error) {
    viper.SetConfigName("config")
    viper.AddConfigPath(".")
    
    if err := viper.ReadInConfig(); err != nil {
        return nil, err
    }
    
    var config Config
    if err := viper.Unmarshal(&config); err != nil {
        return nil, err
    }
    
    return &config, nil
}
```

## Watch for Changes

```go
func WatchConfig(onChange func()) {
    viper.WatchConfig()
    viper.OnConfigChange(func(e fsnotify.Event) {
        log.Println("Config file changed:", e.Name)
        onChange()
    })
}
```

## Multiple Config Files

```go
func LoadConfigs() error {
    // Main config
    viper.SetConfigName("config")
    viper.AddConfigPath(".")
    if err := viper.ReadInConfig(); err != nil {
        return err
    }
    
    // Merge additional config
    viper.SetConfigName("secrets")
    if err := viper.MergeInConfig(); err != nil {
        // Secrets file optional
    }
    
    return nil
}
```

## Example Config File

```yaml
# config.yaml
server:
  host: localhost
  port: 8080

database:
  driver: postgres
  host: localhost
  port: 5432
  name: myapp
  user: postgres
  password: ${DB_PASSWORD}  # Use env var

log:
  level: info
  format: json

features:
  enable_cache: true
  cache_ttl: 5m

allowed_origins:
  - http://localhost:3000
  - https://example.com
```
