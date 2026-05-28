# Unmarshaling Configuration

Converting Viper config to Go structs and accessing typed values.

## Type-Specific Getters

```go
viper.GetString("name")              // string
viper.GetInt("port")                 // int
viper.GetInt64("big_number")         // int64
viper.GetFloat64("rate")             // float64
viper.GetBool("enabled")             // bool
viper.GetDuration("timeout")         // time.Duration
viper.GetTime("created_at")          // time.Time
viper.GetStringSlice("hosts")        // []string
viper.GetIntSlice("ports")           // []int
viper.GetStringMap("headers")        // map[string]interface{}
viper.GetStringMapString("labels")   // map[string]string

value := viper.Get("key")            // interface{} (generic)
```

## Unmarshal to Struct

```go
type Config struct {
    Server   ServerConfig
    Database DatabaseConfig
}

type ServerConfig struct {
    Host string
    Port int
}

var config Config
err := viper.Unmarshal(&config)

// Or unmarshal specific key
var serverCfg ServerConfig
err = viper.UnmarshalKey("server", &serverCfg)
```

## Mapstructure Tags

Viper uses `mapstructure` for struct tags (not `json` or `yaml`).

```go
type Config struct {
    ServerHost string `mapstructure:"server_host"`  // Rename field
    Name       string `mapstructure:",omitempty"`   // Omit if empty
    Extra      map[string]interface{} `mapstructure:",remain"` // Catch unknown
}
```

## Embedded Structs

Use `squash` to flatten embedded structs.

```yaml
# config.yaml - flat structure
host: localhost
port: 8080
debug: true
```

```go
type ServerConfig struct {
    Host string
    Port int
}

type Config struct {
    ServerConfig `mapstructure:",squash"`  // Flatten into parent
    Debug        bool
}
// Result: cfg.Host, cfg.Port, cfg.Debug all at top level
```

## Custom Types

### String-Based Types

```go
type Secret string

func (s Secret) String() string { return "***REDACTED***" }

type Config struct {
    APIKey Secret `mapstructure:"api_key"`
}
// Works automatically - mapstructure converts string to Secret
```

### TextUnmarshaler Interface

```go
type LogLevel int

func (l *LogLevel) UnmarshalText(text []byte) error {
    switch string(text) {
    case "debug": *l = 0
    case "info":  *l = 1
    case "error": *l = 2
    default: return fmt.Errorf("unknown: %s", text)
    }
    return nil
}
```

## Decode Hooks

Custom type conversion during unmarshal.

```go
import "github.com/mitchellh/mapstructure"

var cfg Config
err := viper.Unmarshal(&cfg, viper.DecodeHook(
    mapstructure.ComposeDecodeHookFunc(
        mapstructure.StringToTimeDurationHookFunc(),  // "30s" → time.Duration
        mapstructure.StringToSliceHookFunc(","),      // "a,b,c" → []string
    ),
))
```

## Slices and Maps

```yaml
hosts: [localhost, 127.0.0.1]
ports: [8080, 8081]
headers:
  content-type: application/json
```

```go
type Config struct {
    Hosts   []string          `mapstructure:"hosts"`
    Ports   []int             `mapstructure:"ports"`
    Headers map[string]string `mapstructure:"headers"`
}
```

## Sub-Configs

Extract a subtree as a new Viper instance.

```go
dbViper := viper.Sub("database")
host := dbViper.GetString("host")  // Was "database.host"

var dbCfg DatabaseConfig
dbViper.Unmarshal(&dbCfg)
```

## Strict Unmarshaling

Error on unknown fields.

```go
err := viper.Unmarshal(&cfg, func(dc *mapstructure.DecoderConfig) {
    dc.ErrorUnused = true
})
```

## Default Values Gotcha

Viper defaults override struct field values. Set Viper defaults explicitly.

```go
// Wrong - struct default gets overwritten
var cfg Config
cfg.Port = 8080
viper.Unmarshal(&cfg)  // Port becomes 0 if not in config

// Right - use Viper defaults
viper.SetDefault("port", 8080)
viper.Unmarshal(&cfg)
```
