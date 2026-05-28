# Cobra Command Patterns

## Basic Structure

```go
package cmd

import (
    "fmt"
    "os"
    "github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
    Use:   "myapp",
    Short: "A brief description of your application",
    Long: `A longer description that spans multiple lines
and likely contains examples and usage of using your application.`,
    Run: func(cmd *cobra.Command, args []string) {
        // Root command logic (or show help)
    },
}

func Execute() {
    if err := rootCmd.Execute(); err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
}

func init() {
    // Initialize flags and configuration
    cobra.OnInitialize(initConfig)
    
    // Persistent flags (available to this command and all subcommands)
    rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file")
    rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "verbose output")
    
    // Local flags (only for this command)
    rootCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
```

## Subcommands

```go
package cmd

import (
    "fmt"
    "github.com/spf13/cobra"
)

var createCmd = &cobra.Command{
    Use:   "create [name]",
    Short: "Create a new resource",
    Long:  `Create a new resource with the specified name.`,
    Args:  cobra.ExactArgs(1), // Require exactly 1 argument
    RunE: func(cmd *cobra.Command, args []string) error {
        name := args[0]
        
        // Get flag values
        dryRun, _ := cmd.Flags().GetBool("dry-run")
        template, _ := cmd.Flags().GetString("template")
        
        if dryRun {
            fmt.Printf("Would create: %s\n", name)
            return nil
        }
        
        return createResource(name, template)
    },
}

func init() {
    rootCmd.AddCommand(createCmd)
    
    createCmd.Flags().BoolP("dry-run", "n", false, "Dry run mode")
    createCmd.Flags().StringP("template", "t", "default", "Template to use")
    createCmd.MarkFlagRequired("template")
}
```

## Argument Validation

```go
var cmd = &cobra.Command{
    Use:   "process [file...]",
    Short: "Process files",
    // Argument validators
    Args: cobra.MinimumNArgs(1),           // At least 1
    // Args: cobra.MaximumNArgs(3),         // At most 3
    // Args: cobra.ExactArgs(2),            // Exactly 2
    // Args: cobra.RangeArgs(1, 3),         // 1 to 3
    // Args: cobra.NoArgs,                  // None allowed
    
    // Custom validator
    Args: func(cmd *cobra.Command, args []string) error {
        for _, arg := range args {
            if !isValidFile(arg) {
                return fmt.Errorf("invalid file: %s", arg)
            }
        }
        return nil
    },
    
    RunE: func(cmd *cobra.Command, args []string) error {
        for _, file := range args {
            if err := processFile(file); err != nil {
                return err
            }
        }
        return nil
    },
}
```

## Flag Types

```go
var (
    stringFlag   string
    intFlag      int
    boolFlag     bool
    stringSlice  []string
    stringToString map[string]string
    durationFlag time.Duration
)

func init() {
    // String
    cmd.Flags().StringVarP(&stringFlag, "name", "n", "default", "Description")
    
    // Int
    cmd.Flags().IntVarP(&intFlag, "count", "c", 10, "Number of items")
    
    // Bool
    cmd.Flags().BoolVarP(&boolFlag, "verbose", "v", false, "Enable verbose")
    
    // String slice (can be specified multiple times)
    cmd.Flags().StringSliceVarP(&stringSlice, "tag", "t", nil, "Tags")
    
    // String to string map
    cmd.Flags().StringToStringVar(&stringToString, "label", nil, "Labels (key=value)")
    
    // Duration
    cmd.Flags().DurationVar(&durationFlag, "timeout", 30*time.Second, "Timeout")
}
```

## Hooks

```go
var cmd = &cobra.Command{
    Use: "deploy",
    
    // Runs before Run
    PreRunE: func(cmd *cobra.Command, args []string) error {
        return validateConfig()
    },
    
    // Main execution
    RunE: func(cmd *cobra.Command, args []string) error {
        return deploy()
    },
    
    // Runs after Run (even if Run errors)
    PostRunE: func(cmd *cobra.Command, args []string) error {
        return cleanup()
    },
    
    // Persistent versions run for all child commands too
    PersistentPreRun: func(cmd *cobra.Command, args []string) {
        initLogging()
    },
}
```

## Nested Commands

```go
// rootCmd → userCmd → createUserCmd
var userCmd = &cobra.Command{
    Use:   "user",
    Short: "User management",
}

var createUserCmd = &cobra.Command{
    Use:   "create [name]",
    Short: "Create a user",
    RunE: func(cmd *cobra.Command, args []string) error {
        return createUser(args[0])
    },
}

var listUserCmd = &cobra.Command{
    Use:   "list",
    Short: "List users",
    RunE: func(cmd *cobra.Command, args []string) error {
        return listUsers()
    },
}

func init() {
    rootCmd.AddCommand(userCmd)
    userCmd.AddCommand(createUserCmd)
    userCmd.AddCommand(listUserCmd)
}
```

## Completions

```go
var cmd = &cobra.Command{
    Use: "set-env [environment]",
    ValidArgsFunction: func(cmd *cobra.Command, args []string, toComplete string) ([]string, cobra.ShellCompDirective) {
        return []string{"dev", "staging", "production"}, cobra.ShellCompDirectiveNoFileComp
    },
}

// Generate completions
// myapp completion bash > /etc/bash_completion.d/myapp
// myapp completion zsh > "${fpath[1]}/_myapp"
```
