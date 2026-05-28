---
name: Cobra CLI
description: Modern CLI framework used by kubectl, docker, and more.
metadata:
  labels: [golang, cobra, cli, command]
  triggers:
    files: ['cmd/**/*.go', '**/root.go']
    keywords: [cobra, Command, RunE, Flags, PersistentFlags]
---

# Cobra CLI Standards

## Basic Setup

```go
// cmd/root.go
package cmd

import (
    "os"
    "github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
    Use:   "myapp",
    Short: "A brief description",
    Long:  `A longer description...`,
}

func Execute() {
    if err := rootCmd.Execute(); err != nil {
        os.Exit(1)
    }
}

func init() {
    rootCmd.PersistentFlags().StringP("config", "c", "", "config file")
    rootCmd.PersistentFlags().BoolP("verbose", "v", false, "verbose output")
}
```

```go
// main.go
package main

import "myapp/cmd"

func main() {
    cmd.Execute()
}
```

## Subcommands

```go
// cmd/serve.go
var serveCmd = &cobra.Command{
    Use:   "serve",
    Short: "Start the server",
    RunE: func(cmd *cobra.Command, args []string) error {
        port, _ := cmd.Flags().GetInt("port")
        return startServer(port)
    },
}

func init() {
    rootCmd.AddCommand(serveCmd)
    serveCmd.Flags().IntP("port", "p", 8080, "server port")
}

// cmd/db.go - nested commands
var dbCmd = &cobra.Command{
    Use:   "db",
    Short: "Database operations",
}

var dbMigrateCmd = &cobra.Command{
    Use:   "migrate",
    Short: "Run migrations",
    RunE: func(cmd *cobra.Command, args []string) error {
        return runMigrations()
    },
}

func init() {
    rootCmd.AddCommand(dbCmd)
    dbCmd.AddCommand(dbMigrateCmd)
}
```

## Flags

```go
var cfgFile string
var verbose bool

func init() {
    // Persistent flags (inherited by subcommands)
    rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file")
    rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "verbose")

    // Local flags (only for this command)
    serveCmd.Flags().IntP("port", "p", 8080, "port number")
    serveCmd.Flags().StringSlice("hosts", []string{}, "allowed hosts")

    // Required flags
    serveCmd.MarkFlagRequired("port")

    // Flag groups
    serveCmd.MarkFlagsRequiredTogether("cert", "key")
    serveCmd.MarkFlagsMutuallyExclusive("json", "yaml")
}
```

## Arguments

```go
var echoCmd = &cobra.Command{
    Use:   "echo [message]",
    Short: "Echo a message",
    Args:  cobra.ExactArgs(1),  // Require exactly 1 arg
    RunE: func(cmd *cobra.Command, args []string) error {
        fmt.Println(args[0])
        return nil
    },
}

// Argument validators
cobra.NoArgs           // No arguments allowed
cobra.ExactArgs(n)     // Exactly n arguments
cobra.MinimumNArgs(n)  // At least n arguments
cobra.MaximumNArgs(n)  // At most n arguments
cobra.RangeArgs(m, n)  // Between m and n arguments

// Custom validation
Args: func(cmd *cobra.Command, args []string) error {
    if len(args) < 1 {
        return errors.New("requires at least one argument")
    }
    return nil
},
```

## Viper Integration

```go
import (
    "github.com/spf13/cobra"
    "github.com/spf13/viper"
)

func init() {
    cobra.OnInitialize(initConfig)
    rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file")

    // Bind flags to viper
    rootCmd.PersistentFlags().String("database-url", "", "database URL")
    viper.BindPFlag("database.url", rootCmd.PersistentFlags().Lookup("database-url"))
}

func initConfig() {
    if cfgFile != "" {
        viper.SetConfigFile(cfgFile)
    } else {
        viper.SetConfigName("config")
        viper.SetConfigType("yaml")
        viper.AddConfigPath(".")
        viper.AddConfigPath("$HOME/.myapp")
    }

    viper.AutomaticEnv()
    viper.ReadInConfig()
}
```

## Pre/Post Hooks

```go
var rootCmd = &cobra.Command{
    Use: "myapp",
    PersistentPreRunE: func(cmd *cobra.Command, args []string) error {
        // Runs before any command
        return initLogger()
    },
    PersistentPostRunE: func(cmd *cobra.Command, args []string) error {
        // Runs after any command
        return cleanup()
    },
}

var serveCmd = &cobra.Command{
    Use: "serve",
    PreRunE: func(cmd *cobra.Command, args []string) error {
        // Runs before this command only
        return validateConfig()
    },
    RunE: func(cmd *cobra.Command, args []string) error {
        return serve()
    },
}
```

## Shell Completions

```go
// Auto-generated completions
rootCmd.GenBashCompletionFile("completions/myapp.bash")
rootCmd.GenZshCompletionFile("completions/myapp.zsh")
rootCmd.GenFishCompletionFile("completions/myapp.fish")

// Custom completions
var userCmd = &cobra.Command{
    Use: "user [username]",
    ValidArgsFunction: func(cmd *cobra.Command, args []string, toComplete string) ([]string, cobra.ShellCompDirective) {
        users := fetchUsernames()
        return users, cobra.ShellCompDirectiveNoFileComp
    },
}
```

## Best Practices

1. **Structure**: One file per command in `cmd/` directory
2. **Errors**: Use `RunE` and return errors, don't `os.Exit`
3. **Flags**: Use persistent flags for shared options
4. **Viper**: Integrate for config file support
5. **Help**: Write clear Use, Short, and Long descriptions
