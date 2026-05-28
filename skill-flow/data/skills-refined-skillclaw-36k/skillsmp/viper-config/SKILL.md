---
name: Viper Config
description: Complete configuration solution for Go applications.
metadata:
  labels: [golang, viper, config, configuration]
  triggers:
    files: ['**/config.go', 'config.yaml', 'config.json']
    keywords: [viper, GetString, SetDefault, ReadInConfig]
---

# Viper Config Standards

## Basic Setup

```go
import "github.com/spf13/viper"

func initConfig() {
    viper.SetConfigName("config")      // config file name (no extension)
    viper.SetConfigType("yaml")        // config file type
    viper.AddConfigPath(".")           // look in current dir
    viper.AddConfigPath("$HOME/.app")  // look in home dir
    viper.AddConfigPath("/etc/app/")   // look in /etc

    if err := viper.ReadInConfig(); err != nil {
        if _, ok := err.(viper.ConfigFileNotFoundError); ok {
            // Config file not found, use defaults
        } else {
            log.Fatalf("Error reading config: %v", err)
        }
    }
}
```

## Configuration File

```yaml
# config.yaml
server:
  host: localhost
  port: 8080
  timeout: 30s

database:
  url: postgres://user:pass@localhost/db
  max_connections: 100

features:
  cache_enabled: true
  debug_mode: false

allowed_origins:
  - http://localhost:3000
  - https://example.com
```

## Reading Values

```go
// Strings
host := viper.GetString("server.host")

// Integers
port := viper.GetInt("server.port")

// Booleans
debug := viper.GetBool("features.debug_mode")

// Duration
timeout := viper.GetDuration("server.timeout")

// Slices
origins := viper.GetStringSlice("allowed_origins")

// Maps
settings := viper.GetStringMapString("settings")

// Check if key exists
if viper.IsSet("database.url") {
    // ...
}
```

## Defaults

```go
func setDefaults() {
    viper.SetDefault("server.host", "localhost")
    viper.SetDefault("server.port", 8080)
    viper.SetDefault("database.max_connections", 10)
    viper.SetDefault("features.cache_enabled", true)
}
```

## Environment Variables

```go
func initConfig() {
    // Automatically read env vars
    viper.AutomaticEnv()

    // Replace . with _ in env var names
    viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))

    // Prefix for env vars: APP_SERVER_PORT
    viper.SetEnvPrefix("APP")

    // Bind specific env var
    viper.BindEnv("database.url", "DATABASE_URL")
}

// Environment: APP_SERVER_PORT=9000
// viper.GetInt("server.port") returns 9000
```

## Unmarshal to Struct

```go
type Config struct {
    Server   ServerConfig   `mapstructure:"server"`
    Database DatabaseConfig `mapstructure:"database"`
}

type ServerConfig struct {
    Host    string        `mapstructure:"host"`
    Port    int           `mapstructure:"port"`
    Timeout time.Duration `mapstructure:"timeout"`
}

type DatabaseConfig struct {
    URL            string `mapstructure:"url"`
    MaxConnections int    `mapstructure:"max_connections"`
}

func LoadConfig() (*Config, error) {
    var cfg Config
    if err := viper.Unmarshal(&cfg); err != nil {
        return nil, err
    }
    return &cfg, nil
}

// Sub-config
func LoadServerConfig() (*ServerConfig, error) {
    var cfg ServerConfig
    if err := viper.UnmarshalKey("server", &cfg); err != nil {
        return nil, err
    }
    return &cfg, nil
}
```

## Live Watching

```go
import "github.com/fsnotify/fsnotify"

func initConfig() {
    viper.WatchConfig()
    viper.OnConfigChange(func(e fsnotify.Event) {
        fmt.Println("Config changed:", e.Name)
        // Reload application config
        reloadConfig()
    })
}
```

## Cobra Integration

```go
import (
    "github.com/spf13/cobra"
    "github.com/spf13/viper"
)

var cfgFile string

var rootCmd = &cobra.Command{
    Use: "app",
    PersistentPreRunE: func(cmd *cobra.Command, args []string) error {
        return initConfig()
    },
}

func init() {
    rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file")
    rootCmd.PersistentFlags().Int("port", 8080, "server port")

    // Bind flag to viper
    viper.BindPFlag("server.port", rootCmd.PersistentFlags().Lookup("port"))
}

func initConfig() error {
    if cfgFile != "" {
        viper.SetConfigFile(cfgFile)
    } else {
        viper.SetConfigName("config")
        viper.AddConfigPath(".")
    }

    viper.AutomaticEnv()
    return viper.ReadInConfig()
}
```

## Multiple Config Files

```go
// Merge multiple configs
viper.SetConfigName("config")
viper.ReadInConfig()

viper.SetConfigName("config.local")
viper.MergeInConfig()  // Merge with existing

// Or read specific file
viper.SetConfigFile("/path/to/config.yaml")
viper.MergeInConfig()
```

## Writing Config

```go
// Write current config
viper.WriteConfig()

// Write to specific file
viper.WriteConfigAs("./config.new.yaml")

// Safe write (don't overwrite)
viper.SafeWriteConfig()

// Set values programmatically
viper.Set("server.port", 9000)
viper.WriteConfig()
```

## Best Practices

1. **Defaults**: Always set sensible defaults
2. **Environment**: Use `AutomaticEnv()` for 12-factor apps
3. **Struct binding**: Unmarshal to typed config structs
4. **Validation**: Validate config after loading
5. **Secrets**: Use env vars for secrets, not config files
