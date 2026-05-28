# Advanced Features

Config watching, remote configuration, and writing configs.

## Watching Config Changes

Automatically reload config when file changes.

```go
import "github.com/fsnotify/fsnotify"

viper.OnConfigChange(func(e fsnotify.Event) {
    fmt.Println("Config changed:", e.Name)
})
viper.WatchConfig()
```

### Thread Safety Warning

Config watching causes race conditions. Protect access with mutex.

```go
var (
    config     Config
    configLock sync.RWMutex
)

viper.OnConfigChange(func(e fsnotify.Event) {
    configLock.Lock()
    defer configLock.Unlock()
    viper.Unmarshal(&config)
})
viper.WatchConfig()

func GetConfig() Config {
    configLock.RLock()
    defer configLock.RUnlock()
    return config
}
```

## Writing Config Files

```go
viper.WriteConfig()                      // Overwrite loaded file
viper.SafeWriteConfig()                  // Only if file doesn't exist
viper.WriteConfigAs("/path/config.yaml") // Write to specific path
viper.SafeWriteConfigAs("/path/cfg.yaml")// Safe write to path
```

## Remote Configuration

Read config from key/value stores. Requires import:

```go
import _ "github.com/spf13/viper/remote"
```

### Supported Providers

- **etcd/etcd3** - Distributed key-value store
- **consul** - Service mesh config store
- **firestore** - Google Cloud Firestore
- **nats** - NATS messaging system

### Examples

```go
// etcd
viper.AddRemoteProvider("etcd3", "http://127.0.0.1:2379", "/config/app.json")
viper.SetConfigType("json")
viper.ReadRemoteConfig()

// Consul
viper.AddRemoteProvider("consul", "localhost:8500", "myapp/config")
viper.SetConfigType("json")
viper.ReadRemoteConfig()

// Firestore
viper.AddRemoteProvider("firestore", "project-id", "collection/document")
viper.SetConfigType("json")
viper.ReadRemoteConfig()
```

### Watching Remote Config

```go
go func() {
    for {
        time.Sleep(5 * time.Second)
        viper.WatchRemoteConfig()
    }
}()
```

### Encrypted Remote Config

```go
viper.AddSecureRemoteProvider("etcd", "http://127.0.0.1:2379",
    "/config/app.json", "/path/to/keyring.gpg")
```

## Multiple Viper Instances

Avoid global state, useful for testing.

```go
v := viper.New()
v.SetConfigName("config")
v.AddConfigPath(".")
v.ReadInConfig()
```

## Key Aliases

Map multiple keys to same value (useful for migrations).

```go
viper.RegisterAlias("verbose", "log.debug")
viper.Set("log.debug", true)
viper.GetBool("verbose")  // true
```

## Pflags Integration

Bind command-line flags (typically with Cobra).

```go
import "github.com/spf13/pflag"

pflag.Int("port", 8080, "Server port")
pflag.Parse()

viper.BindPFlag("server.port", pflag.Lookup("port"))
// Or bind all: viper.BindPFlags(pflag.CommandLine)
```

## Further Reading

- Viper: https://github.com/spf13/viper
- Mapstructure: https://github.com/mitchellh/mapstructure
- Pflag: https://github.com/spf13/pflag
- Cobra: https://github.com/spf13/cobra
