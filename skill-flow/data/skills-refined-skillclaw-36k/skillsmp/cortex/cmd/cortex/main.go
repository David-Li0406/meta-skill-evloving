package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"io"
	"math"
	"net/http"
	"os"
	"os/exec"
	"os/signal"
	"path/filepath"
	"strings"
	stdsync "sync"
	"syscall"
	"time"

	"github.com/Napageneral/cortex/internal/adapters"
	"github.com/Napageneral/cortex/internal/bus"
	"github.com/Napageneral/cortex/internal/chunk"
	"github.com/Napageneral/cortex/internal/compute"
	"github.com/Napageneral/cortex/internal/config"
	"github.com/Napageneral/cortex/internal/db"
	"github.com/Napageneral/cortex/internal/documents"
	"github.com/Napageneral/cortex/internal/gemini"
	"github.com/Napageneral/cortex/internal/identify"
	"github.com/Napageneral/cortex/internal/importer"
	"github.com/Napageneral/cortex/internal/live"
	"github.com/Napageneral/cortex/internal/me"
	"github.com/Napageneral/cortex/internal/query"
	"github.com/Napageneral/cortex/internal/search"
	"github.com/Napageneral/cortex/internal/sync"
	"github.com/Napageneral/cortex/internal/tag"
	"github.com/Napageneral/cortex/internal/timeline"
	"github.com/fsnotify/fsnotify"
	"github.com/spf13/cobra"
)

var (
	version    = "dev"
	commit     = "none"
	buildDate  = "unknown"
	jsonOutput bool
)

func main() {
	rootCmd := &cobra.Command{
		Use:   "cortex",
		Short: "Workspace intelligence layer",
		Long: `Cortex aggregates your communications across all channels 
(iMessage, Gmail, Slack, AI sessions, etc.) into a single 
queryable event store with identity resolution.`,
	}

	rootCmd.PersistentFlags().BoolVarP(&jsonOutput, "json", "j", false, "Output as JSON")

	// version command
	rootCmd.AddCommand(&cobra.Command{
		Use:   "version",
		Short: "Print version info",
		Run: func(cmd *cobra.Command, args []string) {
			if jsonOutput {
				printJSON(map[string]string{
					"version": version,
					"commit":  commit,
					"date":    buildDate,
				})
			} else {
				fmt.Printf("cortex %s (%s, %s)\n", version, commit, buildDate)
			}
		},
	})

	// init command
	rootCmd.AddCommand(&cobra.Command{
		Use:   "init",
		Short: "Initialize cortex config and database",
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK        bool   `json:"ok"`
				Message   string `json:"message,omitempty"`
				ConfigDir string `json:"config_dir,omitempty"`
				DataDir   string `json:"data_dir,omitempty"`
				DBPath    string `json:"db_path,omitempty"`
			}

			result := Result{OK: true}

			// Get directories
			configDir, err := config.GetConfigDir()
			if err != nil {
				result.OK = false
				result.Message = fmt.Sprintf("Failed to get config directory: %v", err)
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			result.ConfigDir = configDir

			dataDir, err := config.GetDataDir()
			if err != nil {
				result.OK = false
				result.Message = fmt.Sprintf("Failed to get data directory: %v", err)
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			result.DataDir = dataDir

			// Create config directory
			if err := os.MkdirAll(configDir, 0755); err != nil {
				result.OK = false
				result.Message = fmt.Sprintf("Failed to create config directory: %v", err)
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Create data directory
			if err := os.MkdirAll(dataDir, 0755); err != nil {
				result.OK = false
				result.Message = fmt.Sprintf("Failed to create data directory: %v", err)
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Initialize database
			if err := db.Init(); err != nil {
				result.OK = false
				result.Message = fmt.Sprintf("Failed to initialize database: %v", err)
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			dbPath, err := db.GetPath()
			if err != nil {
				result.OK = false
				result.Message = fmt.Sprintf("Failed to get database path: %v", err)
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			result.DBPath = dbPath

			result.Message = "Cortex initialized successfully"

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Printf("✓ Config directory: %s\n", result.ConfigDir)
				fmt.Printf("✓ Data directory: %s\n", result.DataDir)
				fmt.Printf("✓ Database: %s\n", result.DBPath)
				fmt.Println("\nCortex initialized successfully!")
			}
		},
	})

	// me command
	meCmd := &cobra.Command{
		Use:   "me",
		Short: "Configure user identity",
		Long:  "Manage your identity configuration (name, phone, email, etc.)",
	}

	// me set command
	meSetCmd := &cobra.Command{
		Use:   "set",
		Short: "Set your identity information",
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK      bool   `json:"ok"`
				Message string `json:"message,omitempty"`
			}

			name, _ := cmd.Flags().GetString("name")
			phone, _ := cmd.Flags().GetString("phone")
			email, _ := cmd.Flags().GetString("email")

			if name == "" && phone == "" && email == "" {
				result := Result{
					OK:      false,
					Message: "At least one of --name, --phone, or --email must be provided",
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			database, err := db.Open()
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to open database: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			// Set name if provided
			if name != "" {
				if err := me.SetMeName(database, name); err != nil {
					result := Result{
						OK:      false,
						Message: fmt.Sprintf("Failed to set name: %v", err),
					}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
			}

			// Add phone identity if provided
			if phone != "" {
				if err := me.AddIdentity(database, "phone", phone); err != nil {
					result := Result{
						OK:      false,
						Message: fmt.Sprintf("Failed to add phone: %v", err),
					}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
			}

			// Add email identity if provided
			if email != "" {
				if err := me.AddIdentity(database, "email", email); err != nil {
					result := Result{
						OK:      false,
						Message: fmt.Sprintf("Failed to add email: %v", err),
					}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
			}

			result := Result{
				OK:      true,
				Message: "Identity updated successfully",
			}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Println("✓ Identity updated successfully")
				if name != "" {
					fmt.Printf("  Name: %s\n", name)
				}
				if phone != "" {
					fmt.Printf("  Phone: %s\n", phone)
				}
				if email != "" {
					fmt.Printf("  Email: %s\n", email)
				}
			}
		},
	}

	meSetCmd.Flags().String("name", "", "Your full name")
	meSetCmd.Flags().String("phone", "", "Your phone number")
	meSetCmd.Flags().String("email", "", "Your email address")

	// me show command
	meShowCmd := &cobra.Command{
		Use:   "show",
		Short: "Show your current identity configuration",
		Run: func(cmd *cobra.Command, args []string) {
			type IdentityInfo struct {
				Channel    string `json:"channel"`
				Identifier string `json:"identifier"`
			}

			type Result struct {
				OK         bool           `json:"ok"`
				Message    string         `json:"message,omitempty"`
				Name       string         `json:"name,omitempty"`
				Identities []IdentityInfo `json:"identities,omitempty"`
			}

			database, err := db.Open()
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to open database: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			person, err := me.GetMePerson(database)
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to get identity: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			if person == nil {
				result := Result{
					OK:      false,
					Message: "Identity not configured. Run 'cortex me set --name \"Your Name\"' to configure.",
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "%s\n", result.Message)
				}
				os.Exit(1)
			}

			identities, err := me.GetIdentities(database, person.ID)
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to get identities: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{
				OK:   true,
				Name: person.CanonicalName,
			}

			for _, id := range identities {
				result.Identities = append(result.Identities, IdentityInfo{
					Channel:    id.Channel,
					Identifier: id.Identifier,
				})
			}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Printf("Name: %s\n", person.CanonicalName)
				if len(identities) > 0 {
					fmt.Println("\nIdentities:")
					for _, id := range identities {
						fmt.Printf("  %s: %s\n", id.Channel, id.Identifier)
					}
				} else {
					fmt.Println("\nNo identities configured")
				}
			}
		},
	}

	meCmd.AddCommand(meSetCmd)
	meCmd.AddCommand(meShowCmd)
	rootCmd.AddCommand(meCmd)

	// adapters command
	adaptersCmd := &cobra.Command{
		Use:   "adapters",
		Short: "List configured adapters",
		Run: func(cmd *cobra.Command, args []string) {
			type AdapterInfo struct {
				Name    string `json:"name"`
				Type    string `json:"type"`
				Enabled bool   `json:"enabled"`
				Status  string `json:"status"`
			}

			type Result struct {
				OK       bool          `json:"ok"`
				Message  string        `json:"message,omitempty"`
				Adapters []AdapterInfo `json:"adapters,omitempty"`
			}

			cfg, err := config.Load()
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to load config: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{OK: true}

			if len(cfg.Adapters) == 0 {
				result.Message = "No adapters configured. Run 'cortex connect <adapter>' to configure one."
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Println(result.Message)
				}
				return
			}

			// Determine adapter status based on enabled flag and prerequisites
			for name, adapter := range cfg.Adapters {
				status := "disabled"
				if adapter.Enabled {
					status = checkAdapterStatus(name, adapter)
				}

				result.Adapters = append(result.Adapters, AdapterInfo{
					Name:    name,
					Type:    adapter.Type,
					Enabled: adapter.Enabled,
					Status:  status,
				})
			}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Println("Configured adapters:")
				for _, a := range result.Adapters {
					statusSymbol := "✗"
					if a.Status == "ready" {
						statusSymbol = "✓"
					}
					enabledStr := "disabled"
					if a.Enabled {
						enabledStr = "enabled"
					}
					fmt.Printf("  %s %s (%s) - %s - %s\n", statusSymbol, a.Name, a.Type, enabledStr, a.Status)
				}
			}
		},
	}
	rootCmd.AddCommand(adaptersCmd)

	// connect command
	connectCmd := &cobra.Command{
		Use:   "connect",
		Short: "Configure an adapter",
		Long:  "Configure and enable an adapter for syncing communications",
	}

	// connect imessage
	connectImessageCmd := &cobra.Command{
		Use:   "imessage",
		Short: "Configure iMessage adapter (via Eve)",
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK      bool   `json:"ok"`
				Message string `json:"message,omitempty"`
			}

			// Check if Eve database exists
			home, err := os.UserHomeDir()
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to get home directory: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			eveDBPath := filepath.Join(home, "Library", "Application Support", "Eve", "eve.db")
			if _, err := os.Stat(eveDBPath); os.IsNotExist(err) {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Eve database not found at %s. Install and run Eve first: brew install Napageneral/tap/eve && eve init && eve sync", eveDBPath),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n\n", result.Message)
					fmt.Fprintf(os.Stderr, "To fix this:\n")
					fmt.Fprintf(os.Stderr, "  1. Install Eve: brew install Napageneral/tap/eve\n")
					fmt.Fprintf(os.Stderr, "  2. Initialize Eve: eve init\n")
					fmt.Fprintf(os.Stderr, "  3. Sync Eve: eve sync\n")
				}
				os.Exit(1)
			}

			cfg, err := config.Load()
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to load config: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			cfg.Adapters["imessage"] = config.AdapterConfig{
				Type:    "eve",
				Enabled: true,
			}

			if err := cfg.Save(); err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to save config: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{
				OK:      true,
				Message: "iMessage adapter configured successfully",
			}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Println("✓ iMessage adapter configured")
				fmt.Printf("  Eve database: %s\n", eveDBPath)
				fmt.Println("\nRun 'cortex sync' to sync iMessage events")
			}
		},
	}

	// connect gmail
	connectGmailCmd := &cobra.Command{
		Use:   "gmail",
		Short: "Configure Gmail adapter (via gogcli)",
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK      bool   `json:"ok"`
				Message string `json:"message,omitempty"`
			}

			account, _ := cmd.Flags().GetString("account")
			if account == "" {
				result := Result{
					OK:      false,
					Message: "The --account flag is required (e.g., --account user@gmail.com)",
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			account = strings.TrimSpace(strings.ToLower(account))
			adapterName := fmt.Sprintf("gmail-%s", account)
			workers, _ := cmd.Flags().GetInt("workers")
			qps, _ := cmd.Flags().GetFloat64("qps")

			// TODO: Check if gogcli is installed and authenticated
			// For now, just add the config

			cfg, err := config.Load()
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to load config: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			opts := map[string]interface{}{
				"account": account,
			}
			if workers > 0 {
				opts["workers"] = workers
			}
			if qps > 0 {
				opts["qps"] = qps
			}

			cfg.Adapters[adapterName] = config.AdapterConfig{
				Type:    "gogcli",
				Enabled: true,
				Options: opts,
			}

			if err := cfg.Save(); err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to save config: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{
				OK:      true,
				Message: "Gmail adapter configured successfully",
			}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Println("✓ Gmail adapter configured")
				fmt.Printf("  Adapter: %s\n", adapterName)
				fmt.Printf("  Account: %s\n", account)
				fmt.Println("\nNote: Ensure gogcli is installed and authenticated:")
				fmt.Println("  brew install steipete/tap/gogcli")
				fmt.Printf("  gog auth add %s\n", account)
				fmt.Printf("\nRun 'cortex sync --adapter %s' to sync Gmail events\n", adapterName)
			}
		},
	}
	connectGmailCmd.Flags().String("account", "", "Gmail account email address")
	connectGmailCmd.Flags().Int("workers", 0, "Parallel thread fetch workers (default: adapter default)")
	connectGmailCmd.Flags().Float64("qps", 0, "Approx API requests/sec for thread fetch (default: adapter default)")

	connectCmd.AddCommand(connectImessageCmd)
	connectCmd.AddCommand(connectGmailCmd)

	// connect calendar
	connectCalendarCmd := &cobra.Command{
		Use:   "calendar",
		Short: "Configure Google Calendar adapter (via gogcli)",
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK      bool   `json:"ok"`
				Message string `json:"message,omitempty"`
			}

			account, _ := cmd.Flags().GetString("account")
			if account == "" {
				result := Result{OK: false, Message: "The --account flag is required (e.g., --account user@gmail.com)"}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			account = strings.TrimSpace(strings.ToLower(account))
			adapterName := fmt.Sprintf("calendar-%s", account)

			cfg, err := config.Load()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to load config: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			cfg.Adapters[adapterName] = config.AdapterConfig{
				Type:    "gogcli_calendar",
				Enabled: true,
				Options: map[string]interface{}{
					"account": account,
				},
			}
			if err := cfg.Save(); err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to save config: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{OK: true, Message: "Calendar adapter configured successfully"}
			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Println("✓ Calendar adapter configured")
				fmt.Printf("  Adapter: %s\n", adapterName)
				fmt.Printf("  Account: %s\n", account)
				fmt.Println("\nNote: Ensure gogcli is installed and authenticated:")
				fmt.Println("  brew install steipete/tap/gogcli")
				fmt.Printf("  gog auth add %s\n", account)
				fmt.Printf("\nRun 'cortex sync --adapter %s' to sync calendar events\n", adapterName)
			}
		},
	}
	connectCalendarCmd.Flags().String("account", "", "Google account email address")
	connectCmd.AddCommand(connectCalendarCmd)

	// connect contacts
	connectContactsCmd := &cobra.Command{
		Use:   "contacts",
		Short: "Configure Google Contacts adapter (via gogcli)",
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK      bool   `json:"ok"`
				Message string `json:"message,omitempty"`
			}

			account, _ := cmd.Flags().GetString("account")
			if account == "" {
				result := Result{OK: false, Message: "The --account flag is required (e.g., --account user@gmail.com)"}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			account = strings.TrimSpace(strings.ToLower(account))
			adapterName := fmt.Sprintf("contacts-%s", account)

			cfg, err := config.Load()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to load config: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			cfg.Adapters[adapterName] = config.AdapterConfig{
				Type:    "gogcli_contacts",
				Enabled: true,
				Options: map[string]interface{}{
					"account": account,
				},
			}
			if err := cfg.Save(); err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to save config: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{OK: true, Message: "Contacts adapter configured successfully"}
			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Println("✓ Contacts adapter configured")
				fmt.Printf("  Adapter: %s\n", adapterName)
				fmt.Printf("  Account: %s\n", account)
				fmt.Println("\nNote: Ensure People API is enabled for your gogcli OAuth project:")
				fmt.Println("  People API: https://console.cloud.google.com/apis/library/people.googleapis.com")
				fmt.Println("\nRun 'cortex sync --adapter " + adapterName + " --full' to ingest contacts and unify identities")
			}
		},
	}
	connectContactsCmd.Flags().String("account", "", "Google account email address")
	connectCmd.AddCommand(connectContactsCmd)

	// connect google (gmail + calendar + contacts)
	connectGoogleCmd := &cobra.Command{
		Use:   "google",
		Short: "Configure Gmail+Calendar+Contacts for an account and start backfills",
		Run: func(cmd *cobra.Command, args []string) {
			account, _ := cmd.Flags().GetString("account")
			startBackfill, _ := cmd.Flags().GetBool("start")
			if account == "" {
				fmt.Fprintf(os.Stderr, "Error: --account is required\n")
				os.Exit(1)
			}
			account = strings.TrimSpace(strings.ToLower(account))

			// Configure adapters by reusing connect subcommands logic (direct config edits).
			cfg, err := config.Load()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to load config: %v\n", err)
				os.Exit(1)
			}

			gmailName := fmt.Sprintf("gmail-%s", account)
			calName := fmt.Sprintf("calendar-%s", account)
			contactsName := fmt.Sprintf("contacts-%s", account)

			if cfg.Adapters == nil {
				cfg.Adapters = map[string]config.AdapterConfig{}
			}
			cfg.Adapters[gmailName] = config.AdapterConfig{
				Type:    "gogcli",
				Enabled: true,
				Options: map[string]interface{}{"account": account},
			}
			cfg.Adapters[calName] = config.AdapterConfig{
				Type:    "gogcli_calendar",
				Enabled: true,
				Options: map[string]interface{}{"account": account},
			}
			cfg.Adapters[contactsName] = config.AdapterConfig{
				Type:    "gogcli_contacts",
				Enabled: true,
				Options: map[string]interface{}{"account": account},
			}

			if err := cfg.Save(); err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to save config: %v\n", err)
				os.Exit(1)
			}

			fmt.Println("✓ Google adapters configured")
			fmt.Printf("  Gmail: %s\n", gmailName)
			fmt.Printf("  Calendar: %s\n", calName)
			fmt.Printf("  Contacts: %s\n", contactsName)

			fmt.Println("\nEnable APIs (open these once, enable, done):")
			fmt.Println("  People API: https://console.cloud.google.com/apis/library/people.googleapis.com")
			fmt.Println("  Gmail API: https://console.cloud.google.com/apis/library/gmail.googleapis.com")
			fmt.Println("  Calendar API: https://console.cloud.google.com/apis/library/calendar-json.googleapis.com")
			fmt.Println("  Pub/Sub API (for realtime): https://console.cloud.google.com/apis/library/pubsub.googleapis.com")

			if startBackfill {
				// Start background backfills immediately.
				fmt.Println("\nStarting background backfills...")
				_ = exec.Command(os.Args[0], "sync", "--adapter", gmailName, "--full", "--background").Run()
				_ = exec.Command(os.Args[0], "sync", "--adapter", calName, "--full", "--background").Run()
				_ = exec.Command(os.Args[0], "sync", "--adapter", contactsName, "--full", "--background").Run()
				fmt.Println("Run: cortex sync status")
			} else {
				fmt.Println("\nBackfills not started (use --start to kick off automatically).")
			}

			fmt.Println("\nRealtime (Gmail):")
			fmt.Println("  1) Run: cortex watch gmail")
			fmt.Println("  2) Configure Pub/Sub topic + start watch:")
			fmt.Printf("     gog gmail watch start --account %s --topic projects/.../topics/... --hook-url http://127.0.0.1:8799/hook/gmail\n", account)
		},
	}
	connectGoogleCmd.Flags().String("account", "", "Google account email address")
	connectGoogleCmd.Flags().Bool("start", true, "Start background backfills immediately")
	connectCmd.AddCommand(connectGoogleCmd)

	// connect cursor (via aix)
	connectCursorCmd := &cobra.Command{
		Use:   "cursor",
		Short: "Configure Cursor AI sessions adapter (via aix)",
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK      bool   `json:"ok"`
				Message string `json:"message,omitempty"`
			}

			home, err := os.UserHomeDir()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to get home directory: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			aixDBPath := filepath.Join(home, "Library", "Application Support", "aix", "aix.db")
			if _, err := os.Stat(aixDBPath); os.IsNotExist(err) {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("aix database not found at %s. Run aix first: aix init && aix sync --source cursor (or --all)", aixDBPath),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n\n", result.Message)
					fmt.Fprintf(os.Stderr, "To fix this:\n")
					fmt.Fprintf(os.Stderr, "  1. Build/install aix\n")
					fmt.Fprintf(os.Stderr, "  2. Run: aix init\n")
					fmt.Fprintf(os.Stderr, "  3. Run: aix sync --source cursor (or: aix sync --all)\n")
				}
				os.Exit(1)
			}

			cfg, err := config.Load()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to load config: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			cfg.Adapters["cursor"] = config.AdapterConfig{
				Type:    "aix",
				Enabled: true,
				Options: map[string]interface{}{
					"source": "cursor",
				},
			}

			if err := cfg.Save(); err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to save config: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{OK: true, Message: "Cursor adapter configured successfully"}
			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Println("✓ Cursor adapter configured")
				fmt.Printf("  aix database: %s\n", aixDBPath)
				fmt.Println("\nRun 'cortex sync --adapter cursor' to sync Cursor AI sessions")
			}
		},
	}

	connectCmd.AddCommand(connectCursorCmd)

	// connect x (via bird)
	connectXCmd := &cobra.Command{
		Use:   "x",
		Short: "Configure X/Twitter adapter (via bird CLI)",
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK      bool   `json:"ok"`
				Message string `json:"message,omitempty"`
			}

			cfg, err := config.Load()
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to load config: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			cfg.Adapters["x"] = config.AdapterConfig{
				Type:    "bird",
				Enabled: true,
				Options: map[string]interface{}{},
			}

			if err := cfg.Save(); err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to save config: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{
				OK:      true,
				Message: "X/Twitter adapter configured successfully",
			}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Println("✓ X/Twitter adapter configured")
				fmt.Println("\nNote: Ensure bird is installed and authenticated:")
				fmt.Println("  brew install steipete/tap/bird")
				fmt.Println("  bird check")
				fmt.Println("\nRun 'cortex sync' to sync X events (bookmarks, likes, mentions)")
			}
		},
	}
	connectCmd.AddCommand(connectXCmd)
	rootCmd.AddCommand(connectCmd)

	// sync command
	syncCmd := &cobra.Command{
		Use:   "sync [adapter]",
		Short: "Sync communications from adapters",
		Long:  "Synchronize communications from all enabled adapters or a specific adapter",
		Args:  cobra.MaximumNArgs(1),
		Example: strings.TrimSpace(`
cortex sync
cortex sync imessage
cortex sync --adapter gmail --full
cortex sync --background
`),
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK       bool                 `json:"ok"`
				Message  string               `json:"message,omitempty"`
				Adapters []sync.AdapterResult `json:"adapters,omitempty"`
				Mode     string               `json:"mode,omitempty"`
			}

			adapterFlag, _ := cmd.Flags().GetString("adapter")
			full, _ := cmd.Flags().GetBool("full")
			background, _ := cmd.Flags().GetBool("background")

			if adapterFlag != "" && len(args) > 0 {
				result := Result{
					OK:      false,
					Message: "Provide adapter as a positional arg or via --adapter, not both",
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			adapterName := adapterFlag
			if adapterName == "" && len(args) > 0 {
				adapterName = args[0]
			}

			// Background mode: re-exec without --background and return immediately.
			if background {
				dataDir, err := config.GetDataDir()
				if err != nil {
					result := Result{OK: false, Message: fmt.Sprintf("Failed to get data dir: %v", err)}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
				logPath := filepath.Join(dataDir, "cortex-sync.log")

				argv := make([]string, 0, len(os.Args))
				for _, a := range os.Args {
					// Drop --background variants.
					if a == "--background" || a == "--background=true" {
						continue
					}
					argv = append(argv, a)
				}
				// Ensure we have at least the binary name.
				if len(argv) == 0 {
					argv = []string{os.Args[0]}
				}

				f, err := os.OpenFile(logPath, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
				if err != nil {
					result := Result{OK: false, Message: fmt.Sprintf("Failed to open log file: %v", err)}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
				defer f.Close()

				bg := exec.Command(argv[0], argv[1:]...)
				bg.Stdout = f
				bg.Stderr = f
				if err := bg.Start(); err != nil {
					result := Result{OK: false, Message: fmt.Sprintf("Failed to start background sync: %v", err)}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}

				result := Result{
					OK:      true,
					Message: fmt.Sprintf("Background sync started (pid %d). Logs: %s", bg.Process.Pid, logPath),
					Mode:    "background",
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Printf("✓ %s\n", result.Message)
					fmt.Println("Run: cortex sync status")
				}
				return
			}

			// Load config
			cfg, err := config.Load()
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to load config: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Open database
			database, err := db.Open()
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to open database: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			// Create context
			ctx := cmd.Context()

			// Sync adapters
			var syncResult sync.SyncResult
			if adapterName != "" {
				syncResult = sync.SyncOne(ctx, database, cfg, adapterName, full)
			} else {
				syncResult = sync.SyncAll(ctx, database, cfg, full)
			}

			result := Result{
				OK:       syncResult.OK,
				Message:  syncResult.Message,
				Adapters: syncResult.Adapters,
				Mode:     "foreground",
			}

			if jsonOutput {
				printJSON(result)
			} else {
				if !syncResult.OK && syncResult.Message != "" {
					fmt.Fprintf(os.Stderr, "Error: %s\n", syncResult.Message)
					os.Exit(1)
				}

				if len(syncResult.Adapters) == 0 {
					fmt.Println(syncResult.Message)
					return
				}

				// Print results for each adapter
				fmt.Println("Sync results:")
				for _, adapterResult := range syncResult.Adapters {
					if adapterResult.Success {
						fmt.Printf("\n✓ %s\n", adapterResult.AdapterName)
						fmt.Printf("  Events created: %d\n", adapterResult.EventsCreated)
						fmt.Printf("  Events updated: %d\n", adapterResult.EventsUpdated)
						fmt.Printf("  Persons created: %d\n", adapterResult.PersonsCreated)
						fmt.Printf("  Threads created: %d\n", adapterResult.ThreadsCreated)
						fmt.Printf("  Threads updated: %d\n", adapterResult.ThreadsUpdated)
						fmt.Printf("  Attachments created: %d\n", adapterResult.AttachmentsCreated)
						fmt.Printf("  Attachments updated: %d\n", adapterResult.AttachmentsUpdated)
						fmt.Printf("  Reactions created: %d\n", adapterResult.ReactionsCreated)
						fmt.Printf("  Reactions updated: %d\n", adapterResult.ReactionsUpdated)
						fmt.Printf("  Duration: %s\n", adapterResult.Duration)
						if len(adapterResult.Perf) > 0 {
							// Print a few high-signal perf keys if present.
							keys := []string{"watermark_read", "incremental_sync_query", "backfill_windows", "backfill_total", "backfill_last", "total", "hint_takeout"}
							for _, k := range keys {
								if v, ok := adapterResult.Perf[k]; ok && v != "" {
									fmt.Printf("  %s: %s\n", k, v)
								}
							}
						}
					} else {
						fmt.Printf("\n✗ %s\n", adapterResult.AdapterName)
						fmt.Printf("  Error: %s\n", adapterResult.Error)
					}
				}

				// If any adapter failed, exit with error code
				if !syncResult.OK {
					os.Exit(1)
				}
			}
		},
	}
	syncCmd.Flags().String("adapter", "", "Sync specific adapter (e.g., imessage, gmail)")
	syncCmd.Flags().Bool("full", false, "Force full re-sync instead of incremental")
	syncCmd.Flags().Bool("background", false, "Run sync in background (writes logs to cortex-sync.log)")

	// sync status subcommand
	syncStatusCmd := &cobra.Command{
		Use:   "status",
		Short: "Show sync job progress/status",
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK      bool             `json:"ok"`
				Jobs    []sync.JobStatus `json:"jobs,omitempty"`
				Message string           `json:"message,omitempty"`
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			jobs, err := sync.ListJobs(database)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to list jobs: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			if len(jobs) == 0 {
				result := Result{OK: true, Message: "No job status found yet. Run: cortex sync"}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Println(result.Message)
				}
				return
			}

			result := Result{OK: true, Jobs: jobs}
			if jsonOutput {
				printJSON(result)
				return
			}

			fmt.Println("Sync job status:")
			for _, j := range jobs {
				updated := time.Unix(j.UpdatedAt, 0).Local().Format(time.RFC3339)
				fmt.Printf("\n• %s\n", j.Adapter)
				fmt.Printf("  Status: %s\n", j.Status)
				fmt.Printf("  Phase: %s\n", j.Phase)
				if j.Cursor != nil && *j.Cursor != "" {
					fmt.Printf("  Cursor: %s\n", *j.Cursor)
				}
				fmt.Printf("  Updated: %s\n", updated)
				if j.LastError != nil && *j.LastError != "" {
					fmt.Printf("  Error: %s\n", *j.LastError)
				}
				// Print a couple of common progress fields if present.
				if j.Progress != nil {
					if v, ok := j.Progress["eta_seconds"]; ok {
						fmt.Printf("  ETA: %v seconds\n", v)
					}
					if v, ok := j.Progress["hint_takeout"]; ok {
						fmt.Printf("  Hint: %v\n", v)
					}
					if bf, ok := j.Progress["backfill"].(map[string]interface{}); ok {
						if wd, ok := bf["windows_done"]; ok {
							if wt, ok := bf["windows_total"]; ok {
								fmt.Printf("  Backfill: %v/%v windows\n", wd, wt)
							}
						}
						if cw, ok := bf["current_window"]; ok {
							fmt.Printf("  Window: %v\n", cw)
						}
					}
					if th, ok := j.Progress["threads"].(map[string]interface{}); ok {
						if td, ok := th["done"]; ok {
							if tt, ok := th["total"]; ok {
								fmt.Printf("  Threads: %v/%v\n", td, tt)
							}
						}
					}
				}
			}
		},
	}
	syncCmd.AddCommand(syncStatusCmd)
	rootCmd.AddCommand(syncCmd)

	// import command
	importCmd := &cobra.Command{
		Use:   "import",
		Short: "Import external data into cortex",
	}

	// import mbox (Google Takeout)
	importMBoxCmd := &cobra.Command{
		Use:   "mbox",
		Short: "Import Gmail MBOX (Google Takeout)",
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK      bool   `json:"ok"`
				Message string `json:"message,omitempty"`

				MessagesSeen      int    `json:"messages_seen,omitempty"`
				EventsCreated     int    `json:"events_created,omitempty"`
				EventsUpdated     int    `json:"events_updated,omitempty"`
				PersonsCreated    int    `json:"persons_created,omitempty"`
				MessagesTruncated int    `json:"messages_truncated,omitempty"`
				Duration          string `json:"duration,omitempty"`
			}

			adapterName, _ := cmd.Flags().GetString("adapter")
			account, _ := cmd.Flags().GetString("account")
			path, _ := cmd.Flags().GetString("file")
			limit, _ := cmd.Flags().GetInt("limit")
			dryRun, _ := cmd.Flags().GetBool("dry-run")

			if adapterName == "" {
				result := Result{OK: false, Message: "The --adapter flag is required (e.g., gmail-tyler@intent-systems.com)"}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			if account == "" {
				result := Result{OK: false, Message: "The --account flag is required (Gmail account email address)"}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			if path == "" {
				result := Result{OK: false, Message: "The --file flag is required (path to .mbox)"}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			ctx := context.Background()
			res, err := importer.ImportMBox(ctx, database, importer.MBoxImportOptions{
				AdapterName:     adapterName,
				AccountEmail:    account,
				Path:            path,
				Source:          "takeout",
				LimitMessages:   limit,
				DryRun:          dryRun,
				MaxMessageBytes: 50 * 1024 * 1024,
				CommitEvery:     500,
			})
			if err != nil && err != io.EOF {
				result := Result{OK: false, Message: fmt.Sprintf("Import failed: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{
				OK:                true,
				Message:           "MBOX import completed",
				MessagesSeen:      res.MessagesSeen,
				EventsCreated:     res.EventsCreated,
				EventsUpdated:     res.EventsUpdated,
				PersonsCreated:    res.PersonsCreated,
				MessagesTruncated: res.MessagesTruncated,
				Duration:          res.Duration.String(),
			}
			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Println("✓ MBOX import completed")
				fmt.Printf("  Messages seen: %d\n", res.MessagesSeen)
				fmt.Printf("  Events created: %d\n", res.EventsCreated)
				fmt.Printf("  Events updated: %d\n", res.EventsUpdated)
				fmt.Printf("  Persons created: %d\n", res.PersonsCreated)
				if res.MessagesTruncated > 0 {
					fmt.Printf("  Messages truncated: %d\n", res.MessagesTruncated)
				}
				fmt.Printf("  Duration: %s\n", res.Duration)
				fmt.Println("\nNext: run an incremental API sync to establish history baseline:")
				fmt.Printf("  cortex sync --adapter %s\n", adapterName)
			}
		},
	}
	importMBoxCmd.Flags().String("adapter", "", "Adapter instance name (e.g., gmail-tyler@intent-systems.com)")
	importMBoxCmd.Flags().String("account", "", "Gmail account email address (used for sent/received inference)")
	importMBoxCmd.Flags().String("file", "", "Path to MBOX file (Google Takeout)")
	importMBoxCmd.Flags().Int("limit", 0, "Only import first N messages (debug)")
	importMBoxCmd.Flags().Bool("dry-run", false, "Parse and count but do not write to database")

	importCmd.AddCommand(importMBoxCmd)
	rootCmd.AddCommand(importCmd)

	// watch command
	watchCmd := &cobra.Command{
		Use:   "watch",
		Short: "Run a local webhook receiver to trigger sync",
	}

	// watch run: run all live-enabled watchers with restart + heartbeats
	watchRunCmd := &cobra.Command{
		Use:   "run",
		Short: "Run all live-enabled adapter watchers",
		Run: func(cmd *cobra.Command, args []string) {
			heartbeatSec, _ := cmd.Flags().GetInt("heartbeat-seconds")
			restartSec, _ := cmd.Flags().GetInt("restart-seconds")

			cfg, err := config.Load()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to load config: %v\n", err)
				os.Exit(1)
			}

			database, err := db.Open()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to open database: %v\n", err)
				os.Exit(1)
			}
			defer database.Close()

			ctx, cancel := context.WithCancel(context.Background())
			defer cancel()

			sigChan := make(chan os.Signal, 1)
			signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)
			go func() {
				<-sigChan
				fmt.Fprintf(os.Stderr, "\nStopping live watchers...\n")
				cancel()
			}()

			manager := live.NewManager(database, cfg)
			if heartbeatSec > 0 {
				manager.HeartbeatInterval = time.Duration(heartbeatSec) * time.Second
			}
			if restartSec > 0 {
				manager.RestartBackoff = time.Duration(restartSec) * time.Second
			}

			fmt.Println("Starting live watchers (Ctrl+C to stop)...")
			if err := manager.Run(ctx); err != nil {
				fmt.Fprintf(os.Stderr, "watch run error: %v\n", err)
				os.Exit(1)
			}
		},
	}
	watchRunCmd.Flags().Int("heartbeat-seconds", 10, "Heartbeat interval for live status")
	watchRunCmd.Flags().Int("restart-seconds", 3, "Base restart backoff seconds")

	// watch status: show live watcher status
	watchStatusCmd := &cobra.Command{
		Use:   "status",
		Short: "Show live watcher status",
		Run: func(cmd *cobra.Command, args []string) {
			cfg, err := config.Load()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to load config: %v\n", err)
				os.Exit(1)
			}

			database, err := db.Open()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to open database: %v\n", err)
				os.Exit(1)
			}
			defer database.Close()

			statuses, err := live.GetStatuses(database, cfg)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to get status: %v\n", err)
				os.Exit(1)
			}

			if jsonOutput {
				printJSON(map[string]any{"ok": true, "watchers": statuses})
				return
			}

			for _, st := range statuses {
				lastBeat := "-"
				if st.LastHeartbeat != nil {
					lastBeat = time.Unix(*st.LastHeartbeat, 0).Format(time.RFC3339)
				}
				status := st.Status
				if status == "" {
					status = "unknown"
				}
				fmt.Printf("%s (%s) enabled=%v supported=%v status=%s last_heartbeat=%s restarts=%d\n",
					st.Adapter, st.Type, st.Enabled, st.Supported, status, lastBeat, st.Restarts)
				if st.LastError != "" {
					fmt.Printf("  last_error: %s\n", st.LastError)
				}
			}
		},
	}

	// watch gmail: receive forwarded Pub/Sub events from `gog gmail watch serve`
	watchGmailCmd := &cobra.Command{
		Use:   "gmail",
		Short: "Receive gog Gmail watch webhooks and sync",
		Run: func(cmd *cobra.Command, args []string) {
			bind, _ := cmd.Flags().GetString("bind")
			port, _ := cmd.Flags().GetInt("port")
			path, _ := cmd.Flags().GetString("path")
			token, _ := cmd.Flags().GetString("token")
			adapterOnly, _ := cmd.Flags().GetString("adapter")
			debounceSec, _ := cmd.Flags().GetInt("debounce-seconds")

			cfg, err := config.Load()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to load config: %v\n", err)
				os.Exit(1)
			}

			database, err := db.Open()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to open database: %v\n", err)
				os.Exit(1)
			}
			defer database.Close()

			type adapterRunState struct {
				running bool
				lastAt  time.Time
			}
			var mu stdsync.Mutex
			stateByAdapter := map[string]*adapterRunState{}

			selectAdapters := func() []string {
				if adapterOnly != "" {
					return []string{adapterOnly}
				}
				var out []string
				for name, a := range cfg.Adapters {
					if !a.Enabled {
						continue
					}
					if a.Type == "gogcli" {
						out = append(out, name)
					}
				}
				return out
			}

			runAdapter := func(adapterName string) {
				mu.Lock()
				st, ok := stateByAdapter[adapterName]
				if !ok {
					st = &adapterRunState{}
					stateByAdapter[adapterName] = st
				}
				if st.running {
					mu.Unlock()
					return
				}
				if debounceSec > 0 && !st.lastAt.IsZero() && time.Since(st.lastAt) < time.Duration(debounceSec)*time.Second {
					mu.Unlock()
					return
				}
				st.running = true
				st.lastAt = time.Now()
				mu.Unlock()

				go func() {
					defer func() {
						mu.Lock()
						st.running = false
						mu.Unlock()
					}()

					res := sync.SyncOne(context.Background(), database, cfg, adapterName, false)
					if !res.OK {
						fmt.Fprintf(os.Stderr, "watch sync error (%s): %s\n", adapterName, res.Message)
					} else {
						fmt.Printf("watch sync OK (%s)\n", adapterName)
					}
				}()
			}

			mux := http.NewServeMux()
			mux.HandleFunc(path, func(w http.ResponseWriter, r *http.Request) {
				if r.Method != http.MethodPost && r.Method != http.MethodPut {
					w.WriteHeader(http.StatusMethodNotAllowed)
					return
				}
				if token != "" {
					ok := false
					// Accept either Authorization: Bearer <token> or ?token=<token>.
					auth := r.Header.Get("Authorization")
					if strings.HasPrefix(strings.ToLower(auth), "bearer ") && strings.TrimSpace(auth[7:]) == token {
						ok = true
					}
					if r.URL.Query().Get("token") == token {
						ok = true
					}
					if !ok {
						w.WriteHeader(http.StatusUnauthorized)
						return
					}
				}

				// Drain body (ignore contents; Gmail adapter will use History API baseline).
				_, _ = io.ReadAll(io.LimitReader(r.Body, 256*1024))
				_ = r.Body.Close()

				for _, a := range selectAdapters() {
					runAdapter(a)
				}

				w.WriteHeader(http.StatusOK)
				_, _ = w.Write([]byte("ok\n"))
			})

			addr := fmt.Sprintf("%s:%d", bind, port)
			fmt.Printf("Listening on http://%s%s\n", addr, path)
			fmt.Println("To connect gogcli watch forwarding to this receiver:")
			fmt.Printf("  gog gmail watch serve --bind %s --port 8788 --path /gmail-pubsub --hook-url http://%s%s", bind, addr, path)
			if token != "" {
				fmt.Printf(" --hook-token %s", token)
			}
			fmt.Println()
			fmt.Println("Then start/renew watch (requires Pub/Sub topic):")
			fmt.Println("  gog gmail watch start --topic projects/.../topics/... --account <acct>")

			srv := &http.Server{
				Addr:    addr,
				Handler: mux,
			}
			if err := srv.ListenAndServe(); err != nil {
				fmt.Fprintf(os.Stderr, "watch server stopped: %v\n", err)
				os.Exit(1)
			}
		},
	}
	watchGmailCmd.Flags().String("bind", "127.0.0.1", "Bind address")
	watchGmailCmd.Flags().Int("port", 8799, "Listen port")
	watchGmailCmd.Flags().String("path", "/hook/gmail", "Webhook path")
	watchGmailCmd.Flags().String("token", "", "Shared token (Authorization Bearer or ?token=)")
	watchGmailCmd.Flags().String("adapter", "", "Only trigger sync for this adapter (default: all gogcli adapters)")
	watchGmailCmd.Flags().Int("debounce-seconds", 10, "Minimum seconds between sync triggers per adapter")

	// watch imessage: watch chat.db for changes and trigger incremental sync
	watchIMessageCmd := &cobra.Command{
		Use:   "imessage",
		Short: "Watch chat.db for new messages and sync incrementally",
		Run: func(cmd *cobra.Command, args []string) {
			debounceSec, _ := cmd.Flags().GetInt("debounce-seconds")

			database, err := db.Open()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to open database: %v\n", err)
				os.Exit(1)
			}
			defer database.Close()

			adapter, err := adapters.NewIMessageAdapter()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to create iMessage adapter: %v\n", err)
				os.Exit(1)
			}

			// Get chat.db path
			chatDBPath := os.ExpandEnv("$HOME/Library/Messages/chat.db")
			if override := os.Getenv("EVE_SOURCE_CHAT_DB"); override != "" {
				chatDBPath = os.ExpandEnv(override)
			}
			chatDBDir := filepath.Dir(chatDBPath)

			// Create file watcher
			watcher, err := fsnotify.NewWatcher()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to create watcher: %v\n", err)
				os.Exit(1)
			}
			defer watcher.Close()

			// Watch the Messages directory (catches chat.db and WAL changes)
			if err := watcher.Add(chatDBDir); err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to watch %s: %v\n", chatDBDir, err)
				os.Exit(1)
			}

			fmt.Printf("Watching for iMessage changes in %s (debounce: %ds)\n", chatDBDir, debounceSec)
			fmt.Println("Press Ctrl+C to stop")

			// Debounce timer
			var debounceTimer *time.Timer
			debounceDelay := time.Duration(debounceSec) * time.Second

			// Sync function with debouncing
			triggerSync := func() {
				if debounceTimer != nil {
					debounceTimer.Stop()
				}
				debounceTimer = time.AfterFunc(debounceDelay, func() {
					ctx := context.Background()
					result, err := adapter.Sync(ctx, database, false)
					if err != nil {
						fmt.Printf("[%s] Sync error: %v\n", time.Now().Format("15:04:05"), err)
						return
					}
					totalNew := result.EventsCreated + result.ReactionsCreated
					if totalNew > 0 {
						fmt.Printf("[%s] Synced %d new events (%d messages, %d reactions, %d attachments)\n",
							time.Now().Format("15:04:05"),
							totalNew,
							result.EventsCreated,
							result.ReactionsCreated,
							result.AttachmentsCreated,
						)
					}
				})
			}

			// Initial sync to catch up
			fmt.Printf("[%s] Running initial sync...\n", time.Now().Format("15:04:05"))
			ctx := context.Background()
			result, err := adapter.Sync(ctx, database, false)
			if err != nil {
				fmt.Printf("[%s] Initial sync error: %v\n", time.Now().Format("15:04:05"), err)
			} else if result.EventsCreated > 0 || result.ReactionsCreated > 0 {
				fmt.Printf("[%s] Initial sync: %d events, %d reactions\n",
					time.Now().Format("15:04:05"),
					result.EventsCreated,
					result.ReactionsCreated,
				)
			} else {
				fmt.Printf("[%s] Already up to date\n", time.Now().Format("15:04:05"))
			}

			// Watch for file changes
			for {
				select {
				case event, ok := <-watcher.Events:
					if !ok {
						return
					}
					// Only trigger on chat.db or WAL file changes
					if strings.Contains(event.Name, "chat.db") {
						triggerSync()
					}
				case err, ok := <-watcher.Errors:
					if !ok {
						return
					}
					fmt.Printf("[%s] Watch error: %v\n", time.Now().Format("15:04:05"), err)
				}
			}
		},
	}
	watchIMessageCmd.Flags().Int("debounce-seconds", 2, "Minimum seconds between sync triggers")

	// watch aix: watch aix.db for changes and trigger incremental sync
	watchAIXCmd := &cobra.Command{
		Use:   "aix",
		Short: "Watch aix.db for new AI session events and sync incrementally",
		Run: func(cmd *cobra.Command, args []string) {
			source, _ := cmd.Flags().GetString("source")
			debounceSec, _ := cmd.Flags().GetInt("debounce-seconds")
			extractMetadata, _ := cmd.Flags().GetBool("extract-metadata")

			database, err := db.Open()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to open database: %v\n", err)
				os.Exit(1)
			}
			defer database.Close()

			adapter, err := adapters.NewAixAdapter(source)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to create AIX adapter: %v\n", err)
				os.Exit(1)
			}

			aixDBPath, err := adapters.DefaultAixDBPath()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to determine aix.db path: %v\n", err)
				os.Exit(1)
			}
			aixDBDir := filepath.Dir(aixDBPath)

			watcher, err := fsnotify.NewWatcher()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to create watcher: %v\n", err)
				os.Exit(1)
			}
			defer watcher.Close()

			if err := watcher.Add(aixDBDir); err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to watch %s: %v\n", aixDBDir, err)
				os.Exit(1)
			}

			fmt.Printf("Watching for AIX changes in %s (debounce: %ds)\n", aixDBDir, debounceSec)
			fmt.Println("Press Ctrl+C to stop")

			getLastSync := func() int64 {
				var lastSync int64
				_ = database.QueryRow(`SELECT last_sync_at FROM sync_watermarks WHERE adapter = ?`, adapter.Name()).Scan(&lastSync)
				return lastSync
			}

			runSync := func() {
				ctx := context.Background()
				lastSync := getLastSync()
				result, err := adapter.Sync(ctx, database, false)
				if err != nil {
					fmt.Printf("[%s] Sync error: %v\n", time.Now().Format("15:04:05"), err)
					return
				}
				if result.EventsCreated > 0 || result.EventsUpdated > 0 {
					fmt.Printf("[%s] Synced %d events (%d new, %d updated)\n",
						time.Now().Format("15:04:05"),
						result.EventsCreated+result.EventsUpdated,
						result.EventsCreated,
						result.EventsUpdated,
					)
				} else {
					fmt.Printf("[%s] No new AIX events\n", time.Now().Format("15:04:05"))
				}

				if extractMetadata {
					extractor := adapters.NewAIXFacetExtractor(database)
					extractResult, err := extractor.ExtractFacetsFromMetadata(ctx, adapter.Name(), lastSync)
					if err != nil {
						fmt.Printf("[%s] AIX metadata extraction error: %v\n", time.Now().Format("15:04:05"), err)
						return
					}
					if extractResult.FacetsCreated > 0 {
						fmt.Printf("[%s] Extracted %d facets (%d episodes)\n",
							time.Now().Format("15:04:05"),
							extractResult.FacetsCreated,
							extractResult.EpisodesCreated,
						)
					} else {
						fmt.Printf("[%s] No new AIX metadata facets\n", time.Now().Format("15:04:05"))
					}
				}
			}

			// Initial sync to catch up
			fmt.Printf("[%s] Running initial sync...\n", time.Now().Format("15:04:05"))
			runSync()

			var debounceTimer *time.Timer
			debounceDelay := time.Duration(debounceSec) * time.Second

			triggerSync := func() {
				if debounceTimer != nil {
					debounceTimer.Stop()
				}
				debounceTimer = time.AfterFunc(debounceDelay, runSync)
			}

			for {
				select {
				case event, ok := <-watcher.Events:
					if !ok {
						return
					}
					if strings.Contains(event.Name, "aix.db") {
						triggerSync()
					}
				case err, ok := <-watcher.Errors:
					if !ok {
						return
					}
					fmt.Printf("[%s] Watch error: %v\n", time.Now().Format("15:04:05"), err)
				}
			}
		},
	}
	watchAIXCmd.Flags().String("source", "cursor", "AIX source (cursor, codex, ...)")
	watchAIXCmd.Flags().Int("debounce-seconds", 2, "Minimum seconds between sync triggers")
	watchAIXCmd.Flags().Bool("extract-metadata", true, "Extract facets from AIX metadata after sync")

	watchCmd.AddCommand(watchRunCmd)
	watchCmd.AddCommand(watchStatusCmd)
	watchCmd.AddCommand(watchGmailCmd)
	watchCmd.AddCommand(watchIMessageCmd)
	watchCmd.AddCommand(watchAIXCmd)
	rootCmd.AddCommand(watchCmd)

	// bus command
	busCmd := &cobra.Command{
		Use:   "bus",
		Short: "Inspect the cortex event bus",
	}

	busListCmd := &cobra.Command{
		Use:   "list",
		Short: "List bus events",
		Run: func(cmd *cobra.Command, args []string) {
			since, _ := cmd.Flags().GetInt64("since")
			limit, _ := cmd.Flags().GetInt("limit")

			database, err := db.Open()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to open database: %v\n", err)
				os.Exit(1)
			}
			defer database.Close()

			events, err := bus.List(database, since, limit)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to list bus events: %v\n", err)
				os.Exit(1)
			}

			if jsonOutput {
				printJSON(map[string]any{"ok": true, "events": events})
				return
			}

			if len(events) == 0 {
				fmt.Println("No bus events.")
				return
			}
			for _, e := range events {
				t := time.Unix(e.CreatedAt, 0).Local().Format(time.RFC3339)
				adapter := ""
				if e.Adapter != nil {
					adapter = *e.Adapter
				}
				ce := ""
				if e.CommsEvent != nil {
					ce = *e.CommsEvent
				}
				fmt.Printf("%d\t%s\t%s\t%s\t%s\n", e.Seq, t, e.Type, adapter, ce)
			}
		},
	}
	busListCmd.Flags().Int64("since", 0, "Only show events with seq > since")
	busListCmd.Flags().Int("limit", 200, "Max events to return")

	busTailCmd := &cobra.Command{
		Use:   "tail",
		Short: "Tail bus events (optionally follow)",
		Run: func(cmd *cobra.Command, args []string) {
			since, _ := cmd.Flags().GetInt64("since")
			follow, _ := cmd.Flags().GetBool("follow")
			intervalSec, _ := cmd.Flags().GetInt("interval-seconds")
			limit, _ := cmd.Flags().GetInt("limit")

			database, err := db.Open()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: failed to open database: %v\n", err)
				os.Exit(1)
			}
			defer database.Close()

			emit := func(events []bus.Event) {
				for _, e := range events {
					t := time.Unix(e.CreatedAt, 0).Local().Format(time.RFC3339)
					adapter := ""
					if e.Adapter != nil {
						adapter = *e.Adapter
					}
					ce := ""
					if e.CommsEvent != nil {
						ce = *e.CommsEvent
					}
					fmt.Printf("%d\t%s\t%s\t%s\t%s\n", e.Seq, t, e.Type, adapter, ce)
					since = e.Seq
				}
			}

			for {
				events, err := bus.List(database, since, limit)
				if err != nil {
					fmt.Fprintf(os.Stderr, "Error: failed to list bus events: %v\n", err)
					os.Exit(1)
				}
				if jsonOutput {
					printJSON(map[string]any{"ok": true, "events": events})
					if !follow {
						return
					}
				} else {
					emit(events)
					if !follow {
						return
					}
				}
				if intervalSec <= 0 {
					intervalSec = 1
				}
				time.Sleep(time.Duration(intervalSec) * time.Second)
			}
		},
	}
	busTailCmd.Flags().Int64("since", 0, "Start tailing from seq > since")
	busTailCmd.Flags().Bool("follow", true, "Keep polling for new events")
	busTailCmd.Flags().Int("interval-seconds", 1, "Polling interval in seconds when following")
	busTailCmd.Flags().Int("limit", 200, "Max events per poll")

	busCmd.AddCommand(busListCmd)
	busCmd.AddCommand(busTailCmd)
	rootCmd.AddCommand(busCmd)

	// identify command
	identifyCmd := &cobra.Command{
		Use:   "identify",
		Short: "Manage identity resolution and person merging",
		Long:  "List, search, merge, and manage person identities across channels",
		Run: func(cmd *cobra.Command, args []string) {
			type IdentityInfo struct {
				Channel    string `json:"channel"`
				Identifier string `json:"identifier"`
			}

			type PersonInfo struct {
				ID          string         `json:"id"`
				Name        string         `json:"name"`
				DisplayName string         `json:"display_name,omitempty"`
				IsMe        bool           `json:"is_me"`
				Identities  []IdentityInfo `json:"identities"`
				EventCount  int            `json:"event_count"`
			}

			type Result struct {
				OK      bool         `json:"ok"`
				Message string       `json:"message,omitempty"`
				Persons []PersonInfo `json:"persons,omitempty"`
			}

			// Open database
			database, err := db.Open()
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to open database: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			searchTerm, _ := cmd.Flags().GetString("search")

			var persons []identify.PersonWithIdentities
			if searchTerm != "" {
				persons, err = identify.Search(database, searchTerm)
				if err != nil {
					result := Result{
						OK:      false,
						Message: fmt.Sprintf("Failed to search persons: %v", err),
					}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
			} else {
				persons, err = identify.ListAll(database)
				if err != nil {
					result := Result{
						OK:      false,
						Message: fmt.Sprintf("Failed to list persons: %v", err),
					}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
			}

			result := Result{OK: true}

			if len(persons) == 0 {
				result.Message = "No persons found"
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Println(result.Message)
				}
				return
			}

			// Convert to result format
			for _, p := range persons {
				personInfo := PersonInfo{
					ID:         p.ID,
					Name:       p.CanonicalName,
					IsMe:       p.IsMe,
					EventCount: p.EventCount,
				}
				if p.DisplayName != nil {
					personInfo.DisplayName = *p.DisplayName
				}
				for _, id := range p.Identities {
					personInfo.Identities = append(personInfo.Identities, IdentityInfo{
						Channel:    id.Channel,
						Identifier: id.Identifier,
					})
				}
				result.Persons = append(result.Persons, personInfo)
			}

			if jsonOutput {
				printJSON(result)
			} else {
				if searchTerm != "" {
					fmt.Printf("Search results for '%s':\n\n", searchTerm)
				} else {
					fmt.Printf("All persons (%d total):\n\n", len(persons))
				}

				for _, p := range persons {
					nameStr := p.CanonicalName
					if p.IsMe {
						nameStr += " (me)"
					}
					fmt.Printf("• %s\n", nameStr)
					fmt.Printf("  ID: %s\n", p.ID)
					if p.DisplayName != nil {
						fmt.Printf("  Display name: %s\n", *p.DisplayName)
					}
					if p.EventCount > 0 {
						fmt.Printf("  Events: %d\n", p.EventCount)
					}
					if len(p.Identities) > 0 {
						fmt.Printf("  Identities:\n")
						for _, id := range p.Identities {
							fmt.Printf("    - %s: %s\n", id.Channel, id.Identifier)
						}
					}
					fmt.Println()
				}
			}
		},
	}

	identifyCmd.Flags().String("search", "", "Search for persons by name or identifier")

	// identify --merge command
	identifyMergeCmd := &cobra.Command{
		Use:   "merge <person1> <person2>",
		Short: "Merge two persons (union-find operation)",
		Long:  "Merge person2 into person1. All identities and events from person2 will be transferred to person1.",
		Args:  cobra.ExactArgs(2),
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK      bool   `json:"ok"`
				Message string `json:"message,omitempty"`
			}

			person1Name := args[0]
			person2Name := args[1]

			// Open database
			database, err := db.Open()
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to open database: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			// Find person1 by name
			person1, err := identify.GetPersonByName(database, person1Name)
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to find person1: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			if person1 == nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Person '%s' not found", person1Name),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Find person2 by name
			person2, err := identify.GetPersonByName(database, person2Name)
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to find person2: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			if person2 == nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Person '%s' not found", person2Name),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Merge person2 into person1
			err = identify.Merge(database, person1.ID, person2.ID)
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to merge persons: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{
				OK:      true,
				Message: fmt.Sprintf("Successfully merged '%s' into '%s'", person2Name, person1Name),
			}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Printf("✓ Merged '%s' into '%s'\n", person2Name, person1Name)
				fmt.Printf("  All identities and events from '%s' are now associated with '%s'\n", person2Name, person1Name)
			}
		},
	}

	// identify --add command
	identifyAddCmd := &cobra.Command{
		Use:   "add <person> --email <email> | --phone <phone> | --identifier <channel>:<identifier>",
		Short: "Add an identity to a person",
		Long:  "Add a new identity (email, phone, or custom identifier) to an existing person",
		Args:  cobra.ExactArgs(1),
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK      bool   `json:"ok"`
				Message string `json:"message,omitempty"`
			}

			personName := args[0]
			email, _ := cmd.Flags().GetString("email")
			phone, _ := cmd.Flags().GetString("phone")
			identifier, _ := cmd.Flags().GetString("identifier")

			if email == "" && phone == "" && identifier == "" {
				result := Result{
					OK:      false,
					Message: "At least one of --email, --phone, or --identifier must be provided",
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Open database
			database, err := db.Open()
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to open database: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			// Find person by name
			person, err := identify.GetPersonByName(database, personName)
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to find person: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			if person == nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Person '%s' not found", personName),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Add identities
			var added []string

			if email != "" {
				err = identify.AddIdentityToPerson(database, person.ID, "email", email)
				if err != nil {
					result := Result{
						OK:      false,
						Message: fmt.Sprintf("Failed to add email: %v", err),
					}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
				added = append(added, fmt.Sprintf("email: %s", email))
			}

			if phone != "" {
				err = identify.AddIdentityToPerson(database, person.ID, "phone", phone)
				if err != nil {
					result := Result{
						OK:      false,
						Message: fmt.Sprintf("Failed to add phone: %v", err),
					}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
				added = append(added, fmt.Sprintf("phone: %s", phone))
			}

			if identifier != "" {
				// Parse channel:identifier format
				parts := strings.SplitN(identifier, ":", 2)
				if len(parts) != 2 {
					result := Result{
						OK:      false,
						Message: "Identifier must be in format 'channel:identifier'",
					}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
				channel, id := parts[0], parts[1]

				err = identify.AddIdentityToPerson(database, person.ID, channel, id)
				if err != nil {
					result := Result{
						OK:      false,
						Message: fmt.Sprintf("Failed to add identifier: %v", err),
					}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
				added = append(added, fmt.Sprintf("%s: %s", channel, id))
			}

			result := Result{
				OK:      true,
				Message: fmt.Sprintf("Successfully added identities to '%s'", personName),
			}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Printf("✓ Added identities to '%s':\n", personName)
				for _, a := range added {
					fmt.Printf("  - %s\n", a)
				}
			}
		},
	}

	identifyAddCmd.Flags().String("email", "", "Email address to add")
	identifyAddCmd.Flags().String("phone", "", "Phone number to add")
	identifyAddCmd.Flags().String("identifier", "", "Custom identifier in format 'channel:identifier'")

	identifyCmd.AddCommand(identifyMergeCmd)
	identifyCmd.AddCommand(identifyAddCmd)

	// identify suggestions command - generate merge suggestions
	identifySuggestCmd := &cobra.Command{
		Use:   "suggest",
		Short: "Generate merge suggestions for similar persons",
		Long:  "Analyze the identity graph and generate merge suggestions based on name similarity, shared domains, etc.",
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK                 bool   `json:"ok"`
				Message            string `json:"message,omitempty"`
				SuggestionsCreated int    `json:"suggestions_created"`
			}

			minEvents, _ := cmd.Flags().GetInt("min-events")
			minConfidence, _ := cmd.Flags().GetFloat64("min-confidence")
			maxSuggestions, _ := cmd.Flags().GetInt("max")

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			opts := identify.SuggestionOptions{
				MinEventCount:  minEvents,
				MinConfidence:  minConfidence,
				MaxSuggestions: maxSuggestions,
				NameSimilarity: true,
				SharedDomain:   true,
			}

			count, err := identify.GenerateSuggestions(database, opts)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to generate suggestions: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{OK: true, SuggestionsCreated: count}
			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Printf("Generated %d merge suggestions\n", count)
				fmt.Println("Use 'cortex identify suggestions' to review them")
			}
		},
	}
	identifySuggestCmd.Flags().Int("min-events", 5, "Minimum event count for persons to consider")
	identifySuggestCmd.Flags().Float64("min-confidence", 0.5, "Minimum confidence threshold")
	identifySuggestCmd.Flags().Int("max", 100, "Maximum suggestions to generate")

	// identify suggestions list command
	identifySuggestionsCmd := &cobra.Command{
		Use:   "suggestions",
		Short: "List pending merge suggestions",
		Long:  "Show merge suggestions that need user review",
		Run: func(cmd *cobra.Command, args []string) {
			type SuggestionInfo struct {
				ID           string  `json:"id"`
				Person1      string  `json:"person1"`
				Person2      string  `json:"person2"`
				EvidenceType string  `json:"evidence_type"`
				Evidence     any     `json:"evidence,omitempty"`
				Confidence   float64 `json:"confidence"`
				EventCount   int     `json:"combined_event_count"`
			}

			type Result struct {
				OK          bool             `json:"ok"`
				Message     string           `json:"message,omitempty"`
				Count       int              `json:"count"`
				Suggestions []SuggestionInfo `json:"suggestions,omitempty"`
			}

			status, _ := cmd.Flags().GetString("status")
			limit, _ := cmd.Flags().GetInt("limit")

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			suggestions, err := identify.ListSuggestions(database, status, limit)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to list suggestions: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			var infos []SuggestionInfo
			for _, s := range suggestions {
				infos = append(infos, SuggestionInfo{
					ID:           s.ID,
					Person1:      s.Person1Name,
					Person2:      s.Person2Name,
					EvidenceType: s.EvidenceType,
					Evidence:     s.Evidence,
					Confidence:   s.Confidence,
					EventCount:   s.Person1EventCount + s.Person2EventCount,
				})
			}

			result := Result{OK: true, Count: len(infos), Suggestions: infos}
			if jsonOutput {
				printJSON(result)
			} else {
				if len(infos) == 0 {
					fmt.Println("No pending suggestions. Run 'cortex identify suggest' to generate some.")
				} else {
					fmt.Printf("Found %d pending suggestions:\n\n", len(infos))
					for _, s := range infos {
						fmt.Printf("  [%s] %s ↔ %s\n", s.ID[:8], s.Person1, s.Person2)
						fmt.Printf("    Evidence: %s (confidence: %.1f%%)\n", s.EvidenceType, s.Confidence*100)
						fmt.Printf("    Combined events: %d\n\n", s.EventCount)
					}
					fmt.Println("Use 'cortex identify accept <id>' or 'cortex identify reject <id>'")
				}
			}
		},
	}
	identifySuggestionsCmd.Flags().String("status", "pending", "Filter by status (pending, accepted, rejected, expired)")
	identifySuggestionsCmd.Flags().Int("limit", 50, "Maximum suggestions to show")

	// identify accept command
	identifyAcceptCmd := &cobra.Command{
		Use:   "accept <suggestion-id>",
		Short: "Accept a merge suggestion (merges the two persons)",
		Args:  cobra.ExactArgs(1),
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK      bool   `json:"ok"`
				Message string `json:"message,omitempty"`
			}

			suggestionID := args[0]

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			// Support short IDs
			if len(suggestionID) < 36 {
				// Try to find full ID
				var fullID string
				err := database.QueryRow(`SELECT id FROM merge_suggestions WHERE id LIKE ? AND status = 'pending' LIMIT 1`, suggestionID+"%").Scan(&fullID)
				if err == nil {
					suggestionID = fullID
				}
			}

			err = identify.AcceptSuggestion(database, suggestionID)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to accept suggestion: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{OK: true, Message: "Suggestion accepted - persons merged"}
			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Println("✓ Suggestion accepted - persons merged")
			}
		},
	}

	// identify reject command
	identifyRejectCmd := &cobra.Command{
		Use:   "reject <suggestion-id>",
		Short: "Reject a merge suggestion",
		Args:  cobra.ExactArgs(1),
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK      bool   `json:"ok"`
				Message string `json:"message,omitempty"`
			}

			suggestionID := args[0]

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			// Support short IDs
			if len(suggestionID) < 36 {
				var fullID string
				err := database.QueryRow(`SELECT id FROM merge_suggestions WHERE id LIKE ? AND status = 'pending' LIMIT 1`, suggestionID+"%").Scan(&fullID)
				if err == nil {
					suggestionID = fullID
				}
			}

			err = identify.RejectSuggestion(database, suggestionID)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to reject suggestion: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{OK: true, Message: "Suggestion rejected"}
			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Println("✓ Suggestion rejected")
			}
		},
	}

	identifyCmd.AddCommand(identifySuggestCmd)
	identifyCmd.AddCommand(identifySuggestionsCmd)
	identifyCmd.AddCommand(identifyAcceptCmd)
	identifyCmd.AddCommand(identifyRejectCmd)

	// identify resolve - run full identity resolution
	var resolveAutoMerge bool
	var resolveDryRun bool
	var resolveSkipSoft bool
	var resolveTier1Only bool
	identifyResolveCmd := &cobra.Command{
		Use:   "resolve",
		Short: "Run identity resolution to find and merge matching persons",
		Long: `Run the identity resolution algorithm to detect matching persons
and generate merge suggestions.

The algorithm runs in three phases:
1. Hard identifier collisions (same email, phone, etc.)
2. Compound matches (name + birthdate, name + employer + city)
3. Soft identifier accumulation (weighted scoring)`,
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK                      bool   `json:"ok"`
				HardCollisions          int    `json:"hard_collisions"`
				CompoundMatches         int    `json:"compound_matches"`
				SoftAccumulations       int    `json:"soft_accumulations"`
				MergeSuggestionsCreated int    `json:"merge_suggestions_created"`
				AutoMergesExecuted      int    `json:"auto_merges_executed,omitempty"`
				Message                 string `json:"message,omitempty"`
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			includeSoft := !resolveSkipSoft
			tier1Only := resolveTier1Only

			if resolveDryRun {
				// Just show what would happen
				var hardCollisions []identify.FactCollision
				var compoundMatches []identify.CompoundMatch
				if tier1Only {
					hardCollisions, _ = identify.DetectTier1IDCollisions(database)
				} else {
					hardCollisions, _ = identify.DetectHardIDCollisions(database)
					compoundMatches, _ = identify.DetectCompoundMatches(database)
				}

				result := Result{
					OK:              true,
					HardCollisions:  len(hardCollisions),
					CompoundMatches: len(compoundMatches),
					Message:         "Dry run - no changes made",
				}
				if includeSoft && !tier1Only {
					softScores, _ := identify.ScoreSoftIdentifiers(database)
					for _, s := range softScores {
						if s.Score >= 0.6 {
							result.SoftAccumulations++
						}
					}
				}

				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Println("Dry run results:")
					fmt.Printf("  Hard identifier collisions: %d\n", result.HardCollisions)
					fmt.Printf("  Compound matches: %d\n", result.CompoundMatches)
					fmt.Printf("  Soft accumulation matches (>=0.6): %d\n", result.SoftAccumulations)
				}
				return
			}

			res, err := identify.RunFullResolution(database, resolveAutoMerge, includeSoft, tier1Only)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to run resolution: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{
				OK:                      true,
				HardCollisions:          res.HardCollisions,
				CompoundMatches:         res.CompoundMatches,
				SoftAccumulations:       res.SoftAccumulations,
				MergeSuggestionsCreated: res.MergeSuggestionsCreated,
				AutoMergesExecuted:      res.AutoMergesExecuted,
			}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Println("✓ Identity resolution complete:")
				fmt.Printf("  Hard identifier collisions: %d\n", res.HardCollisions)
				fmt.Printf("  Compound matches: %d\n", res.CompoundMatches)
				fmt.Printf("  Soft accumulations: %d\n", res.SoftAccumulations)
				fmt.Printf("  Merge suggestions created: %d\n", res.MergeSuggestionsCreated)
				if resolveAutoMerge {
					fmt.Printf("  Auto-merges executed: %d\n", res.AutoMergesExecuted)
				} else {
					fmt.Println("\nUse 'cortex identify merges' to review pending suggestions")
				}
			}
		},
	}
	identifyResolveCmd.Flags().BoolVar(&resolveAutoMerge, "auto", false, "Automatically execute high-confidence merges")
	identifyResolveCmd.Flags().BoolVar(&resolveDryRun, "dry-run", false, "Show what would be detected without making changes")
	identifyResolveCmd.Flags().BoolVar(&resolveSkipSoft, "skip-soft", false, "Skip soft identifier accumulation (faster)")
	identifyResolveCmd.Flags().BoolVar(&resolveTier1Only, "tier1-only", true, "Use Tier 1 identifiers only (skip compound/soft)")

	// identify merges - list pending merge events
	var mergesStatus string
	var mergesAutoOnly bool
	var mergesLimit int
	identifyMergesCmd := &cobra.Command{
		Use:   "merges",
		Short: "List pending identity merge suggestions",
		Run: func(cmd *cobra.Command, args []string) {
			type MergeInfo struct {
				ID              string   `json:"id"`
				SourcePersonID  string   `json:"source_person_id"`
				SourceName      string   `json:"source_name"`
				TargetPersonID  string   `json:"target_person_id"`
				TargetName      string   `json:"target_name"`
				MergeType       string   `json:"merge_type"`
				Confidence      float64  `json:"confidence"`
				AutoEligible    bool     `json:"auto_eligible"`
				TriggeringFacts []string `json:"triggering_facts,omitempty"`
			}

			type Result struct {
				OK      bool        `json:"ok"`
				Merges  []MergeInfo `json:"merges"`
				Message string      `json:"message,omitempty"`
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			status := mergesStatus
			if status == "" {
				status = "pending"
			}

			merges, err := identify.ListPendingMerges(database, status, mergesLimit)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to list merges: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			var infos []MergeInfo
			for _, m := range merges {
				if mergesAutoOnly && !m.AutoEligible {
					continue
				}

				info := MergeInfo{
					ID:             m.ID,
					SourcePersonID: m.SourcePersonID,
					TargetPersonID: m.TargetPersonID,
					MergeType:      m.MergeType,
					Confidence:     m.SimilarityScore,
					AutoEligible:   m.AutoEligible,
				}

				// Get person names
				database.QueryRow(`SELECT canonical_name FROM persons WHERE id = ?`, m.SourcePersonID).Scan(&info.SourceName)
				database.QueryRow(`SELECT canonical_name FROM persons WHERE id = ?`, m.TargetPersonID).Scan(&info.TargetName)

				for _, f := range m.TriggeringFacts {
					info.TriggeringFacts = append(info.TriggeringFacts, fmt.Sprintf("%s=%s", f.FactType, f.FactValue))
				}

				infos = append(infos, info)
			}

			result := Result{OK: true, Merges: infos}

			if jsonOutput {
				printJSON(result)
			} else {
				if len(infos) == 0 {
					fmt.Println("No pending merge suggestions.")
					fmt.Println("\nRun 'cortex identify resolve' to generate suggestions")
				} else {
					fmt.Printf("Found %d %s merge suggestions:\n\n", len(infos), status)
					for _, m := range infos {
						autoStr := ""
						if m.AutoEligible {
							autoStr = " [AUTO]"
						}
						fmt.Printf("  [%s]%s %s ↔ %s\n", m.ID[:8], autoStr, m.SourceName, m.TargetName)
						fmt.Printf("    Type: %s, Confidence: %.0f%%\n", m.MergeType, m.Confidence*100)
						if len(m.TriggeringFacts) > 0 {
							fmt.Printf("    Facts: %v\n", m.TriggeringFacts)
						}
						fmt.Println()
					}
					fmt.Println("Use 'cortex identify accept <id>' or 'cortex identify reject <id>'")
				}
			}
		},
	}
	identifyMergesCmd.Flags().StringVar(&mergesStatus, "status", "pending", "Filter by status (pending, accepted, rejected, executed)")
	identifyMergesCmd.Flags().BoolVar(&mergesAutoOnly, "auto-eligible", false, "Show only auto-eligible merges")
	identifyMergesCmd.Flags().IntVar(&mergesLimit, "limit", 50, "Maximum merges to show")

	// identify accept-all - accept all auto-eligible merges
	identifyAcceptAllCmd := &cobra.Command{
		Use:   "accept-all",
		Short: "Accept and execute all auto-eligible merges",
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK       bool   `json:"ok"`
				Executed int    `json:"executed"`
				Message  string `json:"message,omitempty"`
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			executed, err := identify.ExecuteAutoMerges(database)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to execute merges: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{OK: true, Executed: executed}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Printf("✓ Executed %d auto-eligible merges\n", executed)
			}
		},
	}

	// identify status - show resolution statistics
	identifyStatusCmd := &cobra.Command{
		Use:   "status",
		Short: "Show identity resolution statistics",
		Run: func(cmd *cobra.Command, args []string) {
			database, err := db.Open()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: %v\n", err)
				os.Exit(1)
			}
			defer database.Close()

			stats, err := identify.GetResolutionStats(database)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: %v\n", err)
				os.Exit(1)
			}

			if jsonOutput {
				printJSON(map[string]any{
					"ok":                   true,
					"active_persons":       stats.ActivePersons,
					"merged_persons":       stats.MergedPersons,
					"total_facts":          stats.TotalFacts,
					"hard_identifiers":     stats.HardIdentifiers,
					"pending_merges":       stats.PendingMerges,
					"auto_eligible_merges": stats.AutoEligibleMerges,
					"unresolved_facts":     stats.UnresolvedFacts,
					"cross_channel_linked": stats.CrossChannelLinked,
				})
			} else {
				fmt.Println("Identity Resolution Status:")
				fmt.Printf("  Active persons: %d\n", stats.ActivePersons)
				fmt.Printf("  Merged persons: %d\n", stats.MergedPersons)
				fmt.Printf("  Total facts: %d\n", stats.TotalFacts)
				fmt.Printf("  Hard identifiers: %d\n", stats.HardIdentifiers)
				fmt.Println()
				fmt.Printf("  Pending merges: %d\n", stats.PendingMerges)
				fmt.Printf("  Auto-eligible: %d\n", stats.AutoEligibleMerges)
				fmt.Printf("  Unresolved facts: %d\n", stats.UnresolvedFacts)
				fmt.Printf("  Cross-channel linked: %d persons\n", stats.CrossChannelLinked)
			}
		},
	}

	identifyCmd.AddCommand(identifyResolveCmd)
	identifyCmd.AddCommand(identifyMergesCmd)
	identifyCmd.AddCommand(identifyAcceptAllCmd)
	identifyCmd.AddCommand(identifyStatusCmd)
	rootCmd.AddCommand(identifyCmd)

	// events command
	eventsCmd := &cobra.Command{
		Use:   "events",
		Short: "Query communication events",
		Long:  "Query and filter communication events across all channels",
		Run: func(cmd *cobra.Command, args []string) {
			type ParticipantInfo struct {
				Name string `json:"name"`
				Role string `json:"role"`
			}

			type EventInfo struct {
				ID           string            `json:"id"`
				Timestamp    int64             `json:"timestamp"`
				TimestampStr string            `json:"timestamp_str"`
				Channel      string            `json:"channel"`
				ContentTypes string            `json:"content_types"`
				Content      string            `json:"content"`
				Direction    string            `json:"direction"`
				ThreadID     *string           `json:"thread_id,omitempty"`
				ReplyTo      *string           `json:"reply_to,omitempty"`
				Participants []ParticipantInfo `json:"participants"`
			}

			type Result struct {
				OK      bool        `json:"ok"`
				Message string      `json:"message,omitempty"`
				Count   int         `json:"count"`
				Events  []EventInfo `json:"events,omitempty"`
			}

			// Parse flags
			personName, _ := cmd.Flags().GetString("person")
			channel, _ := cmd.Flags().GetString("channel")
			sinceStr, _ := cmd.Flags().GetString("since")
			untilStr, _ := cmd.Flags().GetString("until")
			direction, _ := cmd.Flags().GetString("direction")
			limit, _ := cmd.Flags().GetInt("limit")

			// Build filters
			filters := query.EventFilters{
				PersonName: personName,
				Channel:    channel,
				Direction:  direction,
				Limit:      limit,
			}

			// Parse since date
			if sinceStr != "" {
				since, err := parseDate(sinceStr)
				if err != nil {
					result := Result{
						OK:      false,
						Message: fmt.Sprintf("Invalid since date: %v. Use format YYYY-MM-DD", err),
					}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
				filters.Since = since
			}

			// Parse until date
			if untilStr != "" {
				until, err := parseDate(untilStr)
				if err != nil {
					result := Result{
						OK:      false,
						Message: fmt.Sprintf("Invalid until date: %v. Use format YYYY-MM-DD", err),
					}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
				filters.Until = until
			}

			// Validate direction
			if direction != "" && direction != "sent" && direction != "received" && direction != "observed" {
				result := Result{
					OK:      false,
					Message: "Invalid direction. Must be one of: sent, received, observed",
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Open database
			database, err := db.Open()
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to open database: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			// Query events
			events, err := query.QueryEvents(database, filters)
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to query events: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{
				OK:    true,
				Count: len(events),
			}

			// Convert events to result format
			for _, e := range events {
				eventInfo := EventInfo{
					ID:           e.ID,
					Timestamp:    e.Timestamp,
					TimestampStr: query.FormatTimestamp(e.Timestamp),
					Channel:      e.Channel,
					ContentTypes: e.ContentTypes,
					Content:      e.Content,
					Direction:    e.Direction,
					ThreadID:     e.ThreadID,
					ReplyTo:      e.ReplyTo,
				}

				for _, p := range e.Participants {
					eventInfo.Participants = append(eventInfo.Participants, ParticipantInfo{
						Name: p.Name,
						Role: p.Role,
					})
				}

				result.Events = append(result.Events, eventInfo)
			}

			if jsonOutput {
				printJSON(result)
			} else {
				if len(events) == 0 {
					fmt.Println("No events found matching the specified filters.")
					return
				}

				// Build filter description
				filterParts := []string{}
				if personName != "" {
					filterParts = append(filterParts, fmt.Sprintf("person: %s", personName))
				}
				if channel != "" {
					filterParts = append(filterParts, fmt.Sprintf("channel: %s", channel))
				}
				if direction != "" {
					filterParts = append(filterParts, fmt.Sprintf("direction: %s", direction))
				}
				if sinceStr != "" {
					filterParts = append(filterParts, fmt.Sprintf("since: %s", sinceStr))
				}
				if untilStr != "" {
					filterParts = append(filterParts, fmt.Sprintf("until: %s", untilStr))
				}

				if len(filterParts) > 0 {
					fmt.Printf("Events (%s):\n", strings.Join(filterParts, ", "))
				} else {
					fmt.Printf("Recent events (showing up to %d):\n", limit)
				}
				fmt.Printf("Found %d event(s)\n\n", len(events))

				for i, e := range events {
					if i > 0 {
						fmt.Println("---")
					}

					fmt.Printf("ID: %s\n", e.ID)
					fmt.Printf("Time: %s\n", query.FormatTimestamp(e.Timestamp))
					fmt.Printf("Channel: %s\n", e.Channel)
					fmt.Printf("Direction: %s\n", e.Direction)

					if len(e.Participants) > 0 {
						fmt.Println("Participants:")
						for _, p := range e.Participants {
							fmt.Printf("  - %s (%s)\n", p.Name, p.Role)
						}
					}

					if e.Content != "" {
						// Truncate long content for display
						content := e.Content
						if len(content) > 200 {
							content = content[:200] + "..."
						}
						fmt.Printf("Content: %s\n", content)
					}

					if e.ThreadID != nil {
						fmt.Printf("Thread: %s\n", *e.ThreadID)
					}
				}
			}
		},
	}

	eventsCmd.Flags().String("person", "", "Filter by person name")
	eventsCmd.Flags().String("channel", "", "Filter by channel (e.g., imessage, gmail)")
	eventsCmd.Flags().String("since", "", "Filter by start date (YYYY-MM-DD)")
	eventsCmd.Flags().String("until", "", "Filter by end date (YYYY-MM-DD)")
	eventsCmd.Flags().String("direction", "", "Filter by direction (sent, received, observed)")
	eventsCmd.Flags().Int("limit", 100, "Maximum number of events to return")
	rootCmd.AddCommand(eventsCmd)

	// people command
	peopleCmd := &cobra.Command{
		Use:   "people [name]",
		Short: "List and search contacts",
		Long:  "List all persons, search by name, or show details for a specific person",
		Args:  cobra.MaximumNArgs(1),
		Run: func(cmd *cobra.Command, args []string) {
			type IdentityInfo struct {
				Channel    string `json:"channel"`
				Identifier string `json:"identifier"`
			}

			type PersonInfo struct {
				ID           string         `json:"id"`
				Name         string         `json:"name"`
				DisplayName  string         `json:"display_name,omitempty"`
				IsMe         bool           `json:"is_me"`
				Relationship string         `json:"relationship,omitempty"`
				Identities   []IdentityInfo `json:"identities"`
				EventCount   int            `json:"event_count"`
				LastEventAt  string         `json:"last_event_at,omitempty"`
			}

			type Result struct {
				OK      bool         `json:"ok"`
				Message string       `json:"message,omitempty"`
				Count   int          `json:"count,omitempty"`
				Persons []PersonInfo `json:"persons,omitempty"`
			}

			// Open database
			database, err := db.Open()
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to open database: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			// Handle specific person detail view
			if len(args) == 1 {
				personName := args[0]
				person, err := identify.GetPersonByName(database, personName)
				if err != nil {
					result := Result{
						OK:      false,
						Message: fmt.Sprintf("Failed to get person: %v", err),
					}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}

				if person == nil {
					result := Result{
						OK:      false,
						Message: fmt.Sprintf("Person '%s' not found", personName),
					}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}

				// Convert to result format
				personInfo := PersonInfo{
					ID:         person.ID,
					Name:       person.CanonicalName,
					IsMe:       person.IsMe,
					EventCount: person.EventCount,
				}
				if person.DisplayName != nil {
					personInfo.DisplayName = *person.DisplayName
				}
				if person.RelationType != nil {
					personInfo.Relationship = *person.RelationType
				}
				if person.LastEventAt != nil {
					personInfo.LastEventAt = query.FormatTimestamp(person.LastEventAt.Unix())
				}
				for _, id := range person.Identities {
					personInfo.Identities = append(personInfo.Identities, IdentityInfo{
						Channel:    id.Channel,
						Identifier: id.Identifier,
					})
				}

				result := Result{
					OK:      true,
					Count:   1,
					Persons: []PersonInfo{personInfo},
				}

				if jsonOutput {
					printJSON(result)
				} else {
					nameStr := person.CanonicalName
					if person.IsMe {
						nameStr += " (me)"
					}
					fmt.Printf("%s\n", nameStr)
					fmt.Printf("ID: %s\n", person.ID)
					if person.DisplayName != nil {
						fmt.Printf("Display name: %s\n", *person.DisplayName)
					}
					if person.RelationType != nil {
						fmt.Printf("Relationship: %s\n", *person.RelationType)
					}
					fmt.Printf("\nStatistics:\n")
					fmt.Printf("  Events: %d\n", person.EventCount)
					if person.LastEventAt != nil {
						fmt.Printf("  Last event: %s\n", query.FormatTimestamp(person.LastEventAt.Unix()))
					}
					if len(person.Identities) > 0 {
						fmt.Printf("\nIdentities:\n")
						for _, id := range person.Identities {
							fmt.Printf("  - %s: %s\n", id.Channel, id.Identifier)
						}
					}
				}
				return
			}

			// Handle list/search mode
			searchTerm, _ := cmd.Flags().GetString("search")
			topN, _ := cmd.Flags().GetInt("top")

			var persons []identify.PersonWithIdentities
			if searchTerm != "" {
				persons, err = identify.Search(database, searchTerm)
				if err != nil {
					result := Result{
						OK:      false,
						Message: fmt.Sprintf("Failed to search persons: %v", err),
					}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
			} else {
				persons, err = identify.ListAll(database)
				if err != nil {
					result := Result{
						OK:      false,
						Message: fmt.Sprintf("Failed to list persons: %v", err),
					}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
			}

			// Apply top N limit if specified
			if topN > 0 && topN < len(persons) {
				persons = persons[:topN]
			}

			result := Result{
				OK:    true,
				Count: len(persons),
			}

			if len(persons) == 0 {
				result.Message = "No persons found"
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Println(result.Message)
				}
				return
			}

			// Convert to result format
			for _, p := range persons {
				personInfo := PersonInfo{
					ID:         p.ID,
					Name:       p.CanonicalName,
					IsMe:       p.IsMe,
					EventCount: p.EventCount,
				}
				if p.DisplayName != nil {
					personInfo.DisplayName = *p.DisplayName
				}
				if p.RelationType != nil {
					personInfo.Relationship = *p.RelationType
				}
				if p.LastEventAt != nil {
					personInfo.LastEventAt = query.FormatTimestamp(p.LastEventAt.Unix())
				}
				for _, id := range p.Identities {
					personInfo.Identities = append(personInfo.Identities, IdentityInfo{
						Channel:    id.Channel,
						Identifier: id.Identifier,
					})
				}
				result.Persons = append(result.Persons, personInfo)
			}

			if jsonOutput {
				printJSON(result)
			} else {
				// Print header
				if searchTerm != "" {
					fmt.Printf("Search results for '%s':\n", searchTerm)
				} else if topN > 0 {
					fmt.Printf("Top %d contacts by event count:\n", len(persons))
				} else {
					fmt.Printf("All contacts (%d total):\n", len(persons))
				}
				fmt.Println()

				// Print person list
				for _, p := range persons {
					nameStr := p.CanonicalName
					if p.IsMe {
						nameStr += " (me)"
					}
					if p.DisplayName != nil && *p.DisplayName != p.CanonicalName {
						nameStr += fmt.Sprintf(" [%s]", *p.DisplayName)
					}

					fmt.Printf("• %s\n", nameStr)
					if p.EventCount > 0 {
						fmt.Printf("  Events: %d", p.EventCount)
						if p.LastEventAt != nil {
							fmt.Printf(" (last: %s)", query.FormatTimestamp(p.LastEventAt.Unix()))
						}
						fmt.Println()
					}
					if len(p.Identities) > 0 {
						fmt.Printf("  Identities: ")
						identStrs := []string{}
						for _, id := range p.Identities {
							identStrs = append(identStrs, fmt.Sprintf("%s:%s", id.Channel, id.Identifier))
						}
						fmt.Println(strings.Join(identStrs, ", "))
					}
					fmt.Println()
				}
			}
		},
	}

	peopleCmd.Flags().String("search", "", "Search for persons by name")
	peopleCmd.Flags().Int("top", 0, "Show only top N persons by event count")
	rootCmd.AddCommand(peopleCmd)

	// person command - view person details and facts
	personCmd := &cobra.Command{
		Use:   "person",
		Short: "View and manage person details",
	}

	// person facts - show all facts for a person
	var factsIncludeEvidence bool
	var factsCategory string
	personFactsCmd := &cobra.Command{
		Use:   "facts <person_name_or_id>",
		Short: "Show all extracted facts for a person",
		Args:  cobra.ExactArgs(1),
		Run: func(cmd *cobra.Command, args []string) {
			type FactInfo struct {
				Category   string  `json:"category"`
				FactType   string  `json:"fact_type"`
				FactValue  string  `json:"fact_value"`
				Confidence float64 `json:"confidence"`
				Source     string  `json:"source,omitempty"`
				Channel    string  `json:"channel,omitempty"`
				Evidence   string  `json:"evidence,omitempty"`
			}

			type Result struct {
				OK         bool       `json:"ok"`
				PersonID   string     `json:"person_id"`
				PersonName string     `json:"person_name"`
				Facts      []FactInfo `json:"facts"`
				Message    string     `json:"message,omitempty"`
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			// Find person by name or ID
			personRef := args[0]
			var personID, personName string

			// Try by ID first
			err = database.QueryRow(`SELECT id, canonical_name FROM persons WHERE id = ?`, personRef).Scan(&personID, &personName)
			if err != nil {
				// Try by name
				err = database.QueryRow(`
					SELECT id, canonical_name FROM persons 
					WHERE canonical_name LIKE ? OR display_name LIKE ?
					LIMIT 1
				`, "%"+personRef+"%", "%"+personRef+"%").Scan(&personID, &personName)
			}
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Person not found: %s", personRef)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Get facts
			var facts []identify.PersonFact
			if factsCategory != "" {
				facts, err = identify.GetFactsByCategory(database, personID, factsCategory)
			} else {
				facts, err = identify.GetFactsForPerson(database, personID)
			}
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to get facts: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			var infos []FactInfo
			for _, f := range facts {
				info := FactInfo{
					Category:   f.Category,
					FactType:   f.FactType,
					FactValue:  f.FactValue,
					Confidence: f.Confidence,
					Source:     f.SourceType,
				}
				if f.SourceChannel != nil {
					info.Channel = *f.SourceChannel
				}
				if factsIncludeEvidence && f.Evidence != nil {
					info.Evidence = *f.Evidence
				}
				infos = append(infos, info)
			}

			result := Result{OK: true, PersonID: personID, PersonName: personName, Facts: infos}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Printf("Facts for %s (%s):\n\n", personName, personID[:8])
				if len(infos) == 0 {
					fmt.Println("  No facts extracted yet.")
					fmt.Println("\n  Run 'cortex extract pii' to extract facts from segments")
				} else {
					currentCat := ""
					for _, f := range infos {
						if f.Category != currentCat {
							currentCat = f.Category
							fmt.Printf("\n  [%s]\n", currentCat)
						}
						confidenceStr := ""
						if f.Confidence >= 0.8 {
							confidenceStr = "●●●"
						} else if f.Confidence >= 0.5 {
							confidenceStr = "●●○"
						} else {
							confidenceStr = "●○○"
						}
						fmt.Printf("    %s: %s  %s\n", f.FactType, f.FactValue, confidenceStr)
						if f.Evidence != "" {
							// Truncate evidence
							ev := f.Evidence
							if len(ev) > 80 {
								ev = ev[:77] + "..."
							}
							fmt.Printf("      └─ \"%s\"\n", ev)
						}
					}
				}
			}
		},
	}
	personFactsCmd.Flags().BoolVar(&factsIncludeEvidence, "include-evidence", false, "Include source evidence quotes")
	personFactsCmd.Flags().StringVar(&factsCategory, "category", "", "Filter by category (core_identity, contact_information, etc.)")

	// person profile - formatted profile view
	personProfileCmd := &cobra.Command{
		Use:   "profile <person_name_or_id>",
		Short: "Show formatted profile view for a person",
		Args:  cobra.ExactArgs(1),
		Run: func(cmd *cobra.Command, args []string) {
			database, err := db.Open()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: %v\n", err)
				os.Exit(1)
			}
			defer database.Close()

			// Find person
			personRef := args[0]
			var personID, personName string
			var displayName sql.NullString

			err = database.QueryRow(`SELECT id, canonical_name, display_name FROM persons WHERE id = ?`, personRef).Scan(&personID, &personName, &displayName)
			if err != nil {
				err = database.QueryRow(`
					SELECT id, canonical_name, display_name FROM persons 
					WHERE canonical_name LIKE ? OR display_name LIKE ?
					LIMIT 1
				`, "%"+personRef+"%", "%"+personRef+"%").Scan(&personID, &personName, &displayName)
			}
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: Person not found: %s\n", personRef)
				os.Exit(1)
			}

			// Get all facts
			facts, _ := identify.GetFactsForPerson(database, personID)

			// Get identities
			rows, _ := database.Query(`SELECT channel, identifier FROM identities WHERE person_id = ?`, personID)
			var identities []string
			if rows != nil {
				for rows.Next() {
					var ch, id string
					rows.Scan(&ch, &id)
					identities = append(identities, fmt.Sprintf("%s:%s", ch, id))
				}
				rows.Close()
			}

			// Get event count
			var eventCount int
			database.QueryRow(`SELECT COUNT(*) FROM event_participants WHERE person_id = ?`, personID).Scan(&eventCount)

			// Format output
			fmt.Println("╭─────────────────────────────────────────╮")
			fmt.Printf("│  %s\n", personName)
			if displayName.Valid && displayName.String != "" && displayName.String != personName {
				fmt.Printf("│  aka %s\n", displayName.String)
			}
			fmt.Println("╰─────────────────────────────────────────╯")
			fmt.Printf("  ID: %s\n", personID[:8])
			fmt.Printf("  Events: %d\n", eventCount)
			fmt.Println()

			if len(identities) > 0 {
				fmt.Println("  📇 Identities:")
				for _, id := range identities {
					fmt.Printf("     • %s\n", id)
				}
				fmt.Println()
			}

			// Group facts by category
			factsByCategory := make(map[string][]identify.PersonFact)
			for _, f := range facts {
				factsByCategory[f.Category] = append(factsByCategory[f.Category], f)
			}

			categoryOrder := []string{
				identify.CategoryCoreIdentity,
				identify.CategoryContactInfo,
				identify.CategoryProfessional,
				identify.CategoryRelationships,
				identify.CategoryLocation,
				identify.CategoryEducation,
			}

			categoryEmoji := map[string]string{
				identify.CategoryCoreIdentity:    "👤",
				identify.CategoryContactInfo:     "📞",
				identify.CategoryProfessional:    "💼",
				identify.CategoryRelationships:   "👨‍👩‍👧‍👦",
				identify.CategoryLocation:        "📍",
				identify.CategoryEducation:       "🎓",
				identify.CategoryDigitalIdentity: "🌐",
				identify.CategoryGovernmentID:    "🪪",
			}

			for _, cat := range categoryOrder {
				catFacts, ok := factsByCategory[cat]
				if !ok || len(catFacts) == 0 {
					continue
				}
				emoji := categoryEmoji[cat]
				if emoji == "" {
					emoji = "📋"
				}
				fmt.Printf("  %s %s:\n", emoji, cat)
				for _, f := range catFacts {
					fmt.Printf("     %s: %s\n", f.FactType, f.FactValue)
				}
				fmt.Println()
			}
		},
	}

	personCmd.AddCommand(personFactsCmd)
	personCmd.AddCommand(personProfileCmd)
	rootCmd.AddCommand(personCmd)

	// unattributed command - manage unattributed facts
	unattributedCmd := &cobra.Command{
		Use:   "unattributed",
		Short: "Manage facts that couldn't be attributed to a person",
	}

	// unattributed list - list unattributed facts
	var unattributedUnresolved bool
	unattributedListCmd := &cobra.Command{
		Use:   "list",
		Short: "List unattributed facts",
		Run: func(cmd *cobra.Command, args []string) {
			type FactInfo struct {
				ID        string `json:"id"`
				FactType  string `json:"fact_type"`
				FactValue string `json:"fact_value"`
				SharedBy  string `json:"shared_by,omitempty"`
				Context   string `json:"context,omitempty"`
				Resolved  bool   `json:"resolved"`
			}

			type Result struct {
				OK      bool       `json:"ok"`
				Facts   []FactInfo `json:"facts"`
				Message string     `json:"message,omitempty"`
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			query := `
				SELECT uf.id, uf.fact_type, uf.fact_value, p.canonical_name, uf.context, uf.resolved_to_person_id
				FROM unattributed_facts uf
				LEFT JOIN persons p ON uf.shared_by_person_id = p.id
			`
			if unattributedUnresolved {
				query += ` WHERE uf.resolved_to_person_id IS NULL`
			}
			query += ` ORDER BY uf.created_at DESC LIMIT 100`

			rows, err := database.Query(query)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to query: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer rows.Close()

			var infos []FactInfo
			for rows.Next() {
				var info FactInfo
				var sharedBy, context, resolvedTo sql.NullString
				rows.Scan(&info.ID, &info.FactType, &info.FactValue, &sharedBy, &context, &resolvedTo)
				if sharedBy.Valid {
					info.SharedBy = sharedBy.String
				}
				if context.Valid {
					info.Context = context.String
				}
				info.Resolved = resolvedTo.Valid
				infos = append(infos, info)
			}

			result := Result{OK: true, Facts: infos}

			if jsonOutput {
				printJSON(result)
			} else {
				if len(infos) == 0 {
					fmt.Println("No unattributed facts found.")
				} else {
					fmt.Printf("Found %d unattributed facts:\n\n", len(infos))
					for _, f := range infos {
						resolvedStr := ""
						if f.Resolved {
							resolvedStr = " [RESOLVED]"
						}
						fmt.Printf("  [%s]%s %s: %s\n", f.ID[:8], resolvedStr, f.FactType, f.FactValue)
						if f.SharedBy != "" {
							fmt.Printf("    Shared by: %s\n", f.SharedBy)
						}
						if f.Context != "" {
							ctx := f.Context
							if len(ctx) > 60 {
								ctx = ctx[:57] + "..."
							}
							fmt.Printf("    Context: %s\n", ctx)
						}
						fmt.Println()
					}
				}
			}
		},
	}
	unattributedListCmd.Flags().BoolVar(&unattributedUnresolved, "unresolved", false, "Show only unresolved facts")

	// unattributed attribute - resolve a fact to a person
	unattributedAttributeCmd := &cobra.Command{
		Use:   "attribute <fact_id> <person_name_or_id>",
		Short: "Attribute a fact to a person",
		Args:  cobra.ExactArgs(2),
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK      bool   `json:"ok"`
				Message string `json:"message,omitempty"`
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			factRef := args[0]
			personRef := args[1]

			// Find the fact (try full ID first, then prefix match)
			var factID string
			err = database.QueryRow(`SELECT id FROM unattributed_facts WHERE id = ?`, factRef).Scan(&factID)
			if err != nil {
				err = database.QueryRow(`SELECT id FROM unattributed_facts WHERE id LIKE ?`, factRef+"%").Scan(&factID)
			}
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Fact not found: %s", factRef)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Find person
			var personID string
			err = database.QueryRow(`SELECT id FROM persons WHERE id = ?`, personRef).Scan(&personID)
			if err != nil {
				err = database.QueryRow(`
					SELECT id FROM persons 
					WHERE canonical_name LIKE ? OR display_name LIKE ?
					LIMIT 1
				`, "%"+personRef+"%", "%"+personRef+"%").Scan(&personID)
			}
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Person not found: %s", personRef)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Update the fact
			now := time.Now().Unix()
			_, err = database.Exec(`
				UPDATE unattributed_facts 
				SET resolved_to_person_id = ?, resolution_evidence = 'manual attribution', resolved_at = ?
				WHERE id = ?
			`, personID, now, factID)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to update: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{OK: true, Message: "Fact attributed successfully"}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Println("✓ Fact attributed successfully")
			}
		},
	}

	unattributedCmd.AddCommand(unattributedListCmd)
	unattributedCmd.AddCommand(unattributedAttributeCmd)
	rootCmd.AddCommand(unattributedCmd)

	// timeline command
	timelineCmd := &cobra.Command{
		Use:   "timeline [period]",
		Short: "Show events in a time period",
		Long: `Display events grouped by day for a specified time period.

Examples:
  cortex timeline 2026-01         # January 2026
  cortex timeline 2026-01-15      # Specific day
  cortex timeline --today         # Today's events
  cortex timeline --week          # This week (Mon-Sun)`,
		Args: cobra.MaximumNArgs(1),
		Run: func(cmd *cobra.Command, args []string) {
			type DayResult struct {
				Date        string         `json:"date"`
				TotalEvents int            `json:"total_events"`
				BySender    map[string]int `json:"by_sender"`
				ByChannel   map[string]int `json:"by_channel"`
				ByDirection map[string]int `json:"by_direction"`
			}

			type Result struct {
				OK        bool        `json:"ok"`
				Message   string      `json:"message,omitempty"`
				StartDate string      `json:"start_date,omitempty"`
				EndDate   string      `json:"end_date,omitempty"`
				Days      []DayResult `json:"days,omitempty"`
			}

			result := Result{OK: true}

			// Determine time range
			var opts timeline.TimelineOptions
			var rangeDesc string

			useToday, _ := cmd.Flags().GetBool("today")
			useWeek, _ := cmd.Flags().GetBool("week")

			if useToday {
				opts = timeline.GetTodayRange()
				rangeDesc = "today"
			} else if useWeek {
				opts = timeline.GetWeekRange()
				rangeDesc = "this week"
			} else if len(args) == 1 {
				var err error
				opts, err = timeline.ParseTimelineArg(args[0])
				if err != nil {
					result.OK = false
					result.Message = err.Error()
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
				rangeDesc = args[0]
			} else {
				result.OK = false
				result.Message = "Please specify a time period (e.g., '2026-01') or use --today or --week"
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n\n", result.Message)
					fmt.Fprintf(os.Stderr, "Usage:\n")
					fmt.Fprintf(os.Stderr, "  cortex timeline 2026-01         # Month view\n")
					fmt.Fprintf(os.Stderr, "  cortex timeline 2026-01-15      # Single day\n")
					fmt.Fprintf(os.Stderr, "  cortex timeline --today         # Today\n")
					fmt.Fprintf(os.Stderr, "  cortex timeline --week          # This week\n")
				}
				os.Exit(1)
			}

			result.StartDate = opts.StartDate.Format("2006-01-02")
			result.EndDate = opts.EndDate.Format("2006-01-02")

			// Open database
			database, err := db.Open()
			if err != nil {
				result.OK = false
				result.Message = fmt.Sprintf("Failed to open database: %v", err)
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			// Query timeline
			days, err := timeline.QueryTimeline(database, opts)
			if err != nil {
				result.OK = false
				result.Message = fmt.Sprintf("Failed to query timeline: %v", err)
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Convert to result format
			for _, day := range days {
				result.Days = append(result.Days, DayResult{
					Date:        day.Date,
					TotalEvents: day.TotalEvents,
					BySender:    day.BySender,
					ByChannel:   day.ByChannel,
					ByDirection: day.ByDirection,
				})
			}

			if jsonOutput {
				printJSON(result)
			} else {
				// Text output
				fmt.Printf("Timeline for %s (%s to %s)\n\n", rangeDesc, result.StartDate, result.EndDate)

				if len(days) == 0 {
					fmt.Println("No events found in this time period.")
					return
				}

				for _, day := range days {
					fmt.Printf("📅 %s (%d events)\n", day.Date, day.TotalEvents)

					// Show top senders
					if len(day.BySender) > 0 {
						fmt.Print("  Senders: ")
						senderStrs := []string{}
						for sender, count := range day.BySender {
							senderStrs = append(senderStrs, fmt.Sprintf("%s (%d)", sender, count))
						}
						fmt.Println(strings.Join(senderStrs, ", "))
					}

					// Show channels
					if len(day.ByChannel) > 0 {
						fmt.Print("  Channels: ")
						channelStrs := []string{}
						for channel, count := range day.ByChannel {
							channelStrs = append(channelStrs, fmt.Sprintf("%s (%d)", channel, count))
						}
						fmt.Println(strings.Join(channelStrs, ", "))
					}

					// Show direction breakdown
					if len(day.ByDirection) > 0 {
						fmt.Print("  Direction: ")
						dirStrs := []string{}
						for direction, count := range day.ByDirection {
							dirStrs = append(dirStrs, fmt.Sprintf("%s (%d)", direction, count))
						}
						fmt.Println(strings.Join(dirStrs, ", "))
					}

					fmt.Println()
				}
			}
		},
	}

	timelineCmd.Flags().Bool("today", false, "Show today's events")
	timelineCmd.Flags().Bool("week", false, "Show this week's events")
	rootCmd.AddCommand(timelineCmd)

	// tag command
	tagCmd := &cobra.Command{
		Use:   "tag",
		Short: "Manage event tags",
		Long:  "Apply and manage soft tags on events for categorization and discovery",
	}

	// tag list command
	tagListCmd := &cobra.Command{
		Use:   "list",
		Short: "List all tags",
		Long:  "List all tags or filter by type",
		Run: func(cmd *cobra.Command, args []string) {
			type TagInfo struct {
				ID             string   `json:"id"`
				EventID        string   `json:"event_id"`
				TagType        string   `json:"tag_type"`
				Value          string   `json:"value"`
				Confidence     *float64 `json:"confidence,omitempty"`
				Source         string   `json:"source"`
				EventTimestamp int64    `json:"event_timestamp,omitempty"`
				EventChannel   string   `json:"event_channel,omitempty"`
			}

			type Result struct {
				OK      bool      `json:"ok"`
				Message string    `json:"message,omitempty"`
				Count   int       `json:"count"`
				Tags    []TagInfo `json:"tags,omitempty"`
			}

			// Open database
			database, err := db.Open()
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to open database: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			// Get filter flags
			tagType, _ := cmd.Flags().GetString("type")

			var tags []tag.TagWithEvent
			if tagType != "" {
				tags, err = tag.ListByType(database, tagType)
			} else {
				tags, err = tag.ListAll(database)
			}

			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to list tags: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{
				OK:    true,
				Count: len(tags),
			}

			// Convert to result format
			for _, t := range tags {
				tagInfo := TagInfo{
					ID:             t.ID,
					EventID:        t.EventID,
					TagType:        t.TagType,
					Value:          t.Value,
					Confidence:     t.Confidence,
					Source:         t.Source,
					EventTimestamp: t.EventTimestamp,
					EventChannel:   t.EventChannel,
				}
				result.Tags = append(result.Tags, tagInfo)
			}

			if jsonOutput {
				printJSON(result)
			} else {
				if len(tags) == 0 {
					fmt.Println("No tags found")
					return
				}

				if tagType != "" {
					fmt.Printf("Tags of type '%s' (%d total):\n\n", tagType, len(tags))
				} else {
					fmt.Printf("All tags (%d total):\n\n", len(tags))
				}

				for _, t := range tags {
					fmt.Printf("• %s:%s\n", t.TagType, t.Value)
					fmt.Printf("  ID: %s\n", t.ID)
					fmt.Printf("  Event: %s (%s)\n", t.EventID, t.EventChannel)
					fmt.Printf("  Source: %s\n", t.Source)
					if t.Confidence != nil {
						fmt.Printf("  Confidence: %.2f\n", *t.Confidence)
					}
					// Show event content preview
					if t.EventContent != "" {
						content := t.EventContent
						if len(content) > 100 {
							content = content[:100] + "..."
						}
						fmt.Printf("  Event content: %s\n", content)
					}
					fmt.Println()
				}
			}
		},
	}

	tagListCmd.Flags().String("type", "", "Filter by tag type (topic, entity, emotion, project, context)")

	// tag add command
	tagAddCmd := &cobra.Command{
		Use:   "add",
		Short: "Add tags to events",
		Long: `Add a tag to a specific event or multiple events matching a filter.

Examples:
  # Tag a specific event
  cortex tag add --event abc123 --tag project:htaa

  # Bulk tag events by person
  cortex tag add --person "Dane" --tag context:business

  # Bulk tag events by channel and time
  cortex tag add --channel imessage --since 2026-01-01 --tag topic:planning`,
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK           bool   `json:"ok"`
				Message      string `json:"message,omitempty"`
				EventsTagged int    `json:"events_tagged,omitempty"`
			}

			// Parse flags
			eventID, _ := cmd.Flags().GetString("event")
			tagStr, _ := cmd.Flags().GetString("tag")
			personName, _ := cmd.Flags().GetString("person")
			channel, _ := cmd.Flags().GetString("channel")
			sinceStr, _ := cmd.Flags().GetString("since")
			untilStr, _ := cmd.Flags().GetString("until")
			confidenceVal, _ := cmd.Flags().GetFloat64("confidence")

			// Validate required flags
			if tagStr == "" {
				result := Result{
					OK:      false,
					Message: "The --tag flag is required",
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Parse tag (format: type:value)
			parts := strings.SplitN(tagStr, ":", 2)
			if len(parts) != 2 {
				result := Result{
					OK:      false,
					Message: "Tag must be in format 'type:value' (e.g., 'project:htaa')",
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			tagType, tagValue := parts[0], parts[1]

			// Determine mode: single event or bulk
			if eventID == "" && personName == "" && channel == "" && sinceStr == "" && untilStr == "" {
				result := Result{
					OK:      false,
					Message: "Either --event or at least one filter (--person, --channel, --since, --until) must be provided",
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Open database
			database, err := db.Open()
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to open database: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			// Handle confidence
			var confidence *float64
			if confidenceVal > 0 {
				confidence = &confidenceVal
			}

			// Single event mode
			if eventID != "" {
				err = tag.Add(database, eventID, tagType, tagValue, confidence, "user")
				if err != nil {
					result := Result{
						OK:      false,
						Message: fmt.Sprintf("Failed to add tag: %v", err),
					}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}

				result := Result{
					OK:           true,
					Message:      fmt.Sprintf("Tag '%s:%s' added to event %s", tagType, tagValue, eventID),
					EventsTagged: 1,
				}

				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Printf("✓ Added tag '%s:%s' to event %s\n", tagType, tagValue, eventID)
				}
				return
			}

			// Bulk mode - build filter
			filter := tag.EventFilter{
				PersonName: personName,
				Channel:    channel,
			}

			// Parse dates
			if sinceStr != "" {
				since, err := parseDate(sinceStr)
				if err != nil {
					result := Result{
						OK:      false,
						Message: fmt.Sprintf("Invalid since date: %v. Use format YYYY-MM-DD", err),
					}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
				filter.Since = &since
			}

			if untilStr != "" {
				until, err := parseDate(untilStr)
				if err != nil {
					result := Result{
						OK:      false,
						Message: fmt.Sprintf("Invalid until date: %v. Use format YYYY-MM-DD", err),
					}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
				filter.Until = &until
			}

			// Add tags in bulk
			tagged, err := tag.AddBulk(database, filter, tagType, tagValue, confidence, "user")
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to add tags: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{
				OK:           true,
				Message:      fmt.Sprintf("Tag '%s:%s' added to %d event(s)", tagType, tagValue, tagged),
				EventsTagged: tagged,
			}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Printf("✓ Added tag '%s:%s' to %d event(s)\n", tagType, tagValue, tagged)

				// Show filter description
				filterParts := []string{}
				if personName != "" {
					filterParts = append(filterParts, fmt.Sprintf("person: %s", personName))
				}
				if channel != "" {
					filterParts = append(filterParts, fmt.Sprintf("channel: %s", channel))
				}
				if sinceStr != "" {
					filterParts = append(filterParts, fmt.Sprintf("since: %s", sinceStr))
				}
				if untilStr != "" {
					filterParts = append(filterParts, fmt.Sprintf("until: %s", untilStr))
				}

				if len(filterParts) > 0 {
					fmt.Printf("  Filter: %s\n", strings.Join(filterParts, ", "))
				}
			}
		},
	}

	tagAddCmd.Flags().String("event", "", "Event ID to tag")
	tagAddCmd.Flags().String("tag", "", "Tag in format 'type:value' (e.g., 'project:htaa')")
	tagAddCmd.Flags().String("person", "", "Filter events by person name (bulk mode)")
	tagAddCmd.Flags().String("channel", "", "Filter events by channel (bulk mode)")
	tagAddCmd.Flags().String("since", "", "Filter events since date YYYY-MM-DD (bulk mode)")
	tagAddCmd.Flags().String("until", "", "Filter events until date YYYY-MM-DD (bulk mode)")
	tagAddCmd.Flags().Float64("confidence", 0, "Confidence score (0.0-1.0) for analysis-discovered tags")

	tagCmd.AddCommand(tagListCmd)
	tagCmd.AddCommand(tagAddCmd)
	rootCmd.AddCommand(tagCmd)

	// db command
	dbCmd := &cobra.Command{
		Use:   "db",
		Short: "Database operations",
		Long:  "Perform database operations like raw SQL queries",
	}

	// db query command
	dbQueryCmd := &cobra.Command{
		Use:   "query <sql>",
		Short: "Execute raw SQL query",
		Long: `Execute a raw SQL query against the cortex database.

By default, only SELECT statements are allowed for safety.
Use --write flag to allow mutations (INSERT, UPDATE, DELETE, etc.).

Examples:
  cortex db query "SELECT COUNT(*) FROM events"
  cortex db query "SELECT * FROM persons LIMIT 10"
  cortex db query --write "UPDATE persons SET display_name = 'Dad' WHERE canonical_name = 'Father'"`,
		Args: cobra.ExactArgs(1),
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK      bool                     `json:"ok"`
				Message string                   `json:"message,omitempty"`
				Rows    []map[string]interface{} `json:"rows,omitempty"`
				Count   int                      `json:"count,omitempty"`
			}

			sqlQuery := args[0]
			allowWrite, _ := cmd.Flags().GetBool("write")

			// Check if it's a mutation query without --write flag
			upperQuery := strings.ToUpper(strings.TrimSpace(sqlQuery))
			isMutation := false
			for _, keyword := range []string{"INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "TRUNCATE"} {
				if strings.HasPrefix(upperQuery, keyword) {
					isMutation = true
					break
				}
			}

			if isMutation && !allowWrite {
				result := Result{
					OK:      false,
					Message: "Query appears to modify data. Use --write flag to allow mutations.",
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Open database
			database, err := db.Open()
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to open database: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			// Execute query
			rows, err := database.Query(sqlQuery)
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Query failed: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer rows.Close()

			// Get column names
			columns, err := rows.Columns()
			if err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Failed to get columns: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Fetch results
			results := []map[string]interface{}{}
			for rows.Next() {
				// Create a slice of interface{} to hold each column value
				values := make([]interface{}, len(columns))
				valuePtrs := make([]interface{}, len(columns))
				for i := range values {
					valuePtrs[i] = &values[i]
				}

				// Scan the row
				if err := rows.Scan(valuePtrs...); err != nil {
					result := Result{
						OK:      false,
						Message: fmt.Sprintf("Failed to scan row: %v", err),
					}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}

				// Build map for this row
				rowMap := make(map[string]interface{})
				for i, col := range columns {
					val := values[i]
					// Convert []byte to string for text fields
					if b, ok := val.([]byte); ok {
						rowMap[col] = string(b)
					} else {
						rowMap[col] = val
					}
				}
				results = append(results, rowMap)
			}

			if err := rows.Err(); err != nil {
				result := Result{
					OK:      false,
					Message: fmt.Sprintf("Error iterating rows: %v", err),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{
				OK:    true,
				Rows:  results,
				Count: len(results),
			}

			if jsonOutput {
				printJSON(result)
			} else {
				// Text output
				if len(results) == 0 {
					fmt.Println("No rows returned.")
				} else {
					// Print as a simple table
					// Print header
					fmt.Println(strings.Join(columns, "\t"))
					fmt.Println(strings.Repeat("-", 80))

					// Print rows
					for _, row := range results {
						values := make([]string, len(columns))
						for i, col := range columns {
							val := row[col]
							if val == nil {
								values[i] = "NULL"
							} else {
								values[i] = fmt.Sprintf("%v", val)
							}
						}
						fmt.Println(strings.Join(values, "\t"))
					}

					fmt.Printf("\n%d row(s) returned\n", len(results))
				}
			}
		},
	}

	dbQueryCmd.Flags().Bool("write", false, "Allow mutation queries (INSERT, UPDATE, DELETE, etc.)")
	dbCmd.AddCommand(dbQueryCmd)
	rootCmd.AddCommand(dbCmd)

	// chunk command
	chunkCmd := &cobra.Command{
		Use:   "chunk",
		Short: "Chunk events into segments",
		Long:  "Create segments by applying chunking strategies defined in segment_definitions",
	}

	// chunk run command
	chunkRunCmd := &cobra.Command{
		Use:   "run",
		Short: "Run chunking for a definition",
		Long:  "Apply an episode definition's chunking strategy to create episodes",
		Args:  cobra.MaximumNArgs(1),
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK              bool   `json:"ok"`
				Message         string `json:"message,omitempty"`
				DefinitionName  string `json:"definition_name,omitempty"`
				EpisodesCreated int    `json:"episodes_created,omitempty"`
				EventsProcessed int    `json:"events_processed,omitempty"`
				Duration        string `json:"duration,omitempty"`
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			definitionName, _ := cmd.Flags().GetString("definition")

			// If no definition specified, check for positional arg
			if definitionName == "" && len(args) > 0 {
				definitionName = args[0]
			}

			if definitionName == "" {
				result := Result{OK: false, Message: "Definition name is required (use --definition or provide as argument)"}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Look up definition by name
			var definitionID string
			err = database.QueryRow("SELECT id FROM episode_definitions WHERE name = ?", definitionName).Scan(&definitionID)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Definition '%s' not found", definitionName)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Get chunker for this definition
			chunker, err := chunk.GetChunkerForDefinition(context.Background(), database, definitionID)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to create chunker: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Run chunking
			chunkResult, err := chunker.Chunk(context.Background(), database, definitionID)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Chunking failed: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{
				OK:              true,
				DefinitionName:  definitionName,
				EpisodesCreated: chunkResult.EpisodesCreated,
				EventsProcessed: chunkResult.EventsProcessed,
				Duration:        chunkResult.Duration.String(),
			}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Printf("Chunked %d events into %d episodes using '%s' in %s\n",
					result.EventsProcessed, result.EpisodesCreated, result.DefinitionName, result.Duration)
			}
		},
	}
	chunkRunCmd.Flags().String("definition", "", "Segment definition name")

	// chunk list command
	chunkListCmd := &cobra.Command{
		Use:   "list",
		Short: "List segment definitions",
		Long:  "Show all segment definitions and their configurations",
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK          bool               `json:"ok"`
				Message     string             `json:"message,omitempty"`
				Definitions []chunk.Definition `json:"definitions,omitempty"`
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			definitions, err := chunk.ListDefinitions(context.Background(), database)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to list definitions: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{OK: true, Definitions: definitions}

			if jsonOutput {
				printJSON(result)
			} else {
				if len(definitions) == 0 {
					fmt.Println("No segment definitions found")
					fmt.Println("\nRun 'cortex chunk seed' to create default definitions")
				} else {
					fmt.Printf("Found %d segment definition(s):\n\n", len(definitions))
					for _, def := range definitions {
						channel := def.Channel
						if channel == "" {
							channel = "all"
						}
						fmt.Printf("  %s\n", def.Name)
						fmt.Printf("    Strategy: %s\n", def.Strategy)
						fmt.Printf("    Channel:  %s\n", channel)
						fmt.Printf("    Config:   %s\n", def.ConfigJSON)
						if def.Description != "" {
							fmt.Printf("    Description: %s\n", def.Description)
						}
						fmt.Println()
					}
				}
			}
		},
	}

	// chunk seed command
	chunkSeedCmd := &cobra.Command{
		Use:   "seed",
		Short: "Seed default segment definitions",
		Long:  "Create default segment definitions for common chunking strategies",
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK      bool   `json:"ok"`
				Message string `json:"message,omitempty"`
				Created int    `json:"created,omitempty"`
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			ctx := context.Background()
			created := 0

			// Create imessage_3hr definition
			timeGapConfig := chunk.TimeGapConfig{
				GapSeconds: 10800, // 3 hours
				Scope:      "thread",
			}
			_, err = chunk.CreateDefinition(ctx, database, "imessage_3hr", "imessage", "time_gap", timeGapConfig,
				"iMessage segments with 3-hour gap threshold, scoped to threads")
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to create imessage_3hr: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			created++

			// Create gmail_thread definition
			threadConfig := chunk.ThreadConfig{}
			_, err = chunk.CreateDefinition(ctx, database, "gmail_thread", "gmail", "thread", threadConfig,
				"Gmail segments using native thread boundaries")
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to create gmail_thread: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			created++

			// Create single_event definition (channel-agnostic)
			singleEventConfig := chunk.SingleEventConfig{}
			_, err = chunk.CreateDefinition(ctx, database, "single_event", "", "single_event", singleEventConfig,
				"Single-event segments (one event per event)")
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to create single_event: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			created++

			// Create ai_session definition
			aiThreadConfig := chunk.ThreadConfig{}
			_, err = chunk.CreateDefinition(ctx, database, "ai_session", "cursor", "thread", aiThreadConfig,
				"AI sessions (one segment per session thread)")
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to create ai_session: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			created++

			// Create ai_turn_pair definition
			turnPairConfig := chunk.TurnPairConfig{IncludeTools: true}
			_, err = chunk.CreateDefinition(ctx, database, "ai_turn_pair", "cursor", "turn_pair", turnPairConfig,
				"AI turn pairs (user + assistant responses, includes tool events)")
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to create ai_turn_pair: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			created++

			result := Result{OK: true, Created: created}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Printf("Created %d segment definition(s):\n", created)
				fmt.Println("  - imessage_3hr (3-hour gap, thread-scoped)")
				fmt.Println("  - gmail_thread (native Gmail threads)")
				fmt.Println("  - single_event (one event per segment)")
				fmt.Println("  - ai_session (AI sessions by thread)")
				fmt.Println("  - ai_turn_pair (AI turn pairs, includes tools)")
			}
		},
	}

	chunkCmd.AddCommand(chunkListCmd)
	chunkCmd.AddCommand(chunkSeedCmd)
	chunkCmd.AddCommand(chunkRunCmd)
	rootCmd.AddCommand(chunkCmd)

	// ==================== COMPUTE COMMAND ====================
	computeCmd := &cobra.Command{
		Use:   "compute",
		Short: "AI compute engine for analysis and embeddings",
	}

	var computeWorkers int
	var computeAnalysisModel string
	var computeEmbeddingModel string
	var computePreload bool
	var computeDisableAdaptive bool
	var computeEmbedBatchSize int

	// compute run - run the compute engine
	computeRunCmd := &cobra.Command{
		Use:   "run",
		Short: "Run the compute engine to process queued jobs",
		Run: func(cmd *cobra.Command, args []string) {
			database, err := db.Open()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: %v\n", err)
				os.Exit(1)
			}
			defer database.Close()

			apiKey := os.Getenv("GEMINI_API_KEY")
			geminiClient := gemini.NewClient(apiKey)

			cfg := compute.DefaultConfig()
			if computeWorkers > 0 {
				cfg.WorkerCount = computeWorkers
			}
			if computeAnalysisModel != "" {
				cfg.AnalysisModel = computeAnalysisModel
			}
			if computeEmbeddingModel != "" {
				cfg.EmbeddingModel = computeEmbeddingModel
			}
			if computeEmbedBatchSize > 0 {
				cfg.EmbeddingBatchSize = computeEmbedBatchSize
			}
			cfg.DisableAdaptive = computeDisableAdaptive

			engine, err := compute.NewEngine(database, geminiClient, cfg)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error creating engine: %v\n", err)
				os.Exit(1)
			}
			defer engine.Close() // Ensure TxBatchWriter is flushed

			fmt.Printf("Starting compute engine with %d workers...\n", cfg.WorkerCount)
			if cfg.UseBatchWriter {
				fmt.Printf("TxBatchWriter enabled (batch size: %d)\n", cfg.BatchSize)
			}
			fmt.Printf("Analysis model: %s, Embedding model: %s\n", cfg.AnalysisModel, cfg.EmbeddingModel)
			if cfg.DisableAdaptive {
				fmt.Println("Adaptive controllers: disabled (fixed worker pool only)")
			} else {
				fmt.Println("Adaptive controllers: enabled (auto-RPM, adaptive concurrency)")
			}

			// Pre-encode segments if requested (for maximum throughput)
			if computePreload {
				fmt.Println("Pre-loading segments into cache...")
				ctx := context.Background()
				count, err := engine.PreloadSegments(ctx)
				if err != nil {
					fmt.Fprintf(os.Stderr, "Warning: preload failed: %v\n", err)
				} else {
					fmt.Printf("Pre-loaded %d segments into cache\n", count)
				}
			}

			// Setup signal handling for graceful shutdown
			ctx, cancel := context.WithCancel(context.Background())
			defer cancel()

			sigChan := make(chan os.Signal, 1)
			signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)
			go func() {
				<-sigChan
				fmt.Println("\nShutting down gracefully...")
				cancel()
			}()

			startTime := time.Now()
			stats, err := engine.Run(ctx)
			duration := time.Since(startTime)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: %v\n", err)
				os.Exit(1)
			}

			// Get job metrics and controller stats
			jobMetrics := engine.JobMetrics().Snapshot()
			ctrlStats := engine.ControllerStats()
			analysisRPM, embedRPM := engine.EffectiveRPM()

			// Calculate throughput
			throughput := 0.0
			if duration.Seconds() > 0 {
				throughput = float64(stats.Succeeded) / duration.Seconds()
			}

			if jsonOutput {
				printJSON(map[string]any{
					"ok":                     true,
					"succeeded":              stats.Succeeded,
					"failed":                 stats.Failed,
					"skipped":                stats.Skipped,
					"duration_sec":           duration.Seconds(),
					"throughput_jobs_per_s":  throughput,
					"workers":                cfg.WorkerCount,
					"analysis_model":         cfg.AnalysisModel,
					"embed_model":            cfg.EmbeddingModel,
					"analysis_rpm_effective": analysisRPM,
					"embed_rpm_effective":    embedRPM,
					"job_metrics":            jobMetrics,
					"controller_stats":       ctrlStats,
				})
			} else {
				fmt.Printf("\nCompute complete: %d succeeded, %d failed, %d skipped\n",
					stats.Succeeded, stats.Failed, stats.Skipped)
				fmt.Printf("Duration: %.1fs, Throughput: %.2f jobs/sec\n", duration.Seconds(), throughput)
				fmt.Printf("Effective RPM: analysis=%d, embedding=%d\n", analysisRPM, embedRPM)

				// Print job metrics summary
				if jobMetrics != nil {
					if analysis, ok := jobMetrics["analysis"].(map[string]any); ok {
						if total, _ := analysis["total"].(int); total > 0 {
							fmt.Printf("\nAnalysis metrics (%d jobs):\n", total)
							if avgMs, ok := analysis["avg_ms"].(map[string]any); ok {
								fmt.Printf("  Avg API call: %.0fms, DB write: %.0fms, Overall: %.0fms\n",
									avgMs["api_call"], avgMs["db_write"], avgMs["overall"])
							}
						}
					}
					if embedding, ok := jobMetrics["embedding"].(map[string]any); ok {
						if total, _ := embedding["total"].(int); total > 0 {
							fmt.Printf("\nEmbedding metrics (%d jobs):\n", total)
							if avgMs, ok := embedding["avg_ms"].(map[string]any); ok {
								fmt.Printf("  Avg API call: %.0fms, DB write: %.0fms, Overall: %.0fms\n",
									avgMs["api_call"], avgMs["db_write"], avgMs["overall"])
							}
						}
					}
				}
			}
		},
	}
	computeRunCmd.Flags().IntVarP(&computeWorkers, "workers", "w", 50, "Number of concurrent workers (default: 50 for Tier-3 keys)")
	computeRunCmd.Flags().StringVar(&computeAnalysisModel, "analysis-model", "", "Gemini model for analysis")
	computeRunCmd.Flags().StringVar(&computeEmbeddingModel, "embedding-model", "", "Gemini model for embeddings")
	computeRunCmd.Flags().BoolVar(&computePreload, "preload", false, "Pre-load all segments into cache for max throughput")
	computeRunCmd.Flags().BoolVar(&computeDisableAdaptive, "no-adaptive", false, "Disable adaptive concurrency controller")
	computeRunCmd.Flags().IntVar(&computeEmbedBatchSize, "embed-batch-size", 100, "Embedding batch size (max 100)")

	// compute enqueue - queue jobs
	computeEnqueueCmd := &cobra.Command{
		Use:   "enqueue [type]",
		Short: "Enqueue jobs (analysis or embeddings)",
		Long:  "Enqueue jobs for processing. Type can be 'analysis' or 'embeddings'",
		Args:  cobra.ExactArgs(1),
		Run: func(cmd *cobra.Command, args []string) {
			database, err := db.Open()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: %v\n", err)
				os.Exit(1)
			}
			defer database.Close()

			geminiClient := gemini.NewClient("")
			engine, err := compute.NewEngine(database, geminiClient, compute.DefaultConfig())
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: %v\n", err)
				os.Exit(1)
			}

			ctx := context.Background()
			jobType := args[0]
			var count int

			switch jobType {
			case "analysis":
				analysisType, _ := cmd.Flags().GetString("analysis-type")
				if analysisType == "" {
					analysisType = "convo-all-v1"
				}
				count, err = engine.EnqueueAnalysis(ctx, analysisType)
			case "embeddings":
				count, err = engine.EnqueueEmbeddings(ctx)
			case "facet-embeddings":
				count, err = engine.EnqueueFacetEmbeddings(ctx)
			case "person-embeddings":
				count, err = engine.EnqueuePersonEmbeddings(ctx)
			case "document-embeddings":
				count, err = engine.EnqueueDocumentEmbeddings(ctx)
			case "all-embeddings":
				// Enqueue all embedding types
				c1, e1 := engine.EnqueueEmbeddings(ctx)
				c2, e2 := engine.EnqueueFacetEmbeddings(ctx)
				c3, e3 := engine.EnqueuePersonEmbeddings(ctx)
				c4, e4 := engine.EnqueueDocumentEmbeddings(ctx)
				count = c1 + c2 + c3 + c4
				if e1 != nil {
					err = e1
				} else if e2 != nil {
					err = e2
				} else if e3 != nil {
					err = e3
				} else {
					err = e4
				}
				if jsonOutput {
					printJSON(map[string]any{
						"ok":            err == nil,
						"segments": c1,
						"facets":        c2,
						"persons":       c3,
						"documents":     c4,
						"total":         count,
					})
					return
				}
			default:
				fmt.Fprintf(os.Stderr, "Unknown job type: %s\n", jobType)
				fmt.Fprintf(os.Stderr, "Available types: analysis, embeddings, facet-embeddings, person-embeddings, document-embeddings, all-embeddings\n")
				os.Exit(1)
			}

			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: %v\n", err)
				os.Exit(1)
			}

			if jsonOutput {
				printJSON(map[string]any{"ok": true, "queued": count})
			} else {
				fmt.Printf("Queued %d %s jobs\n", count, jobType)
			}
		},
	}
	computeEnqueueCmd.Flags().String("analysis-type", "convo-all-v1", "Analysis type name")

	// compute stats - show queue stats
	computeStatsCmd := &cobra.Command{
		Use:   "stats",
		Short: "Show compute queue statistics",
		Run: func(cmd *cobra.Command, args []string) {
			database, err := db.Open()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: %v\n", err)
				os.Exit(1)
			}
			defer database.Close()

			geminiClient := gemini.NewClient("")
			engine, err := compute.NewEngine(database, geminiClient, compute.DefaultConfig())
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: %v\n", err)
				os.Exit(1)
			}

			stats, err := engine.QueueStats()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: %v\n", err)
				os.Exit(1)
			}

			if jsonOutput {
				printJSON(stats)
			} else {
				fmt.Printf("Queue Statistics:\n")
				fmt.Printf("  Pending:   %d\n", stats.Pending)
				fmt.Printf("  Leased:    %d\n", stats.Leased)
				fmt.Printf("  Succeeded: %d\n", stats.Succeeded)
				fmt.Printf("  Failed:    %d\n", stats.Failed)
				fmt.Printf("  Dead:      %d\n", stats.Dead)
				fmt.Printf("  Total:     %d\n", stats.Total)
			}
		},
	}

	// compute seed - seed default analysis types
	computeSeedCmd := &cobra.Command{
		Use:   "seed",
		Short: "Seed default analysis types",
		Run: func(cmd *cobra.Command, args []string) {
			database, err := db.Open()
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: %v\n", err)
				os.Exit(1)
			}
			defer database.Close()

			ctx := context.Background()
			now := time.Now().Unix()

			promptDir := os.Getenv("COMMS_PROMPTS_DIR")
			if strings.TrimSpace(promptDir) == "" {
				promptDir = "prompts"
			}
			readPrompt := func(filename string) string {
				path := filepath.Join(promptDir, filename)
				raw, err := os.ReadFile(path)
				if err != nil {
					fmt.Fprintf(os.Stderr, "Error reading prompt %s: %v\n", path, err)
					os.Exit(1)
				}
				return string(raw)
			}

			// Seed convo-all-v1 analysis type
			promptTemplate := `# Conversation Analysis

Analyze the following conversation and extract:
1. A short summary (10-50 words)
2. Key entities mentioned (people, places, organizations)
3. Main topics discussed
4. Emotions expressed by each participant
5. Any humor or jokes

Return as JSON with keys: summary, entities, topics, emotions, humor

Conversation:
{{{conversation_text}}}`

			facetsConfig := `{
				"mappings": [
					{"json_path": "entities[]", "facet_type": "entity"},
					{"json_path": "topics[]", "facet_type": "topic"},
					{"json_path": "emotions[]", "facet_type": "emotion"},
					{"json_path": "humor[]", "facet_type": "humor"}
				]
			}`

			_, err = database.ExecContext(ctx, `
				INSERT INTO analysis_types (id, name, version, description, output_type, facets_config_json, prompt_template, model, created_at, updated_at)
				VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
				ON CONFLICT(name) DO NOTHING
			`, "convo-all-v1", "convo-all-v1", "1.0.0",
				"Extract entities, topics, emotions, and humor from segments",
				"structured", facetsConfig, promptTemplate,
				"gemini-2.0-flash", now, now)

			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: %v\n", err)
				os.Exit(1)
			}

			// Seed pii_extraction_v1 analysis type
			piiPromptTemplate := `# PII Extraction

Extract ALL personally identifiable information from this conversation chunk. This creates a comprehensive identity graph for each person mentioned, enabling cross-channel identity resolution through identifier collisions.

## Task

Extract ALL PII for EVERY person mentioned in this conversation:
1. **The primary contact** - the person the user is communicating with
2. **The user themselves** - any PII about the user mentioned in the conversation
3. **Third parties** - any other people mentioned (family, friends, colleagues, etc.)

For each piece of information:
- Quote the exact evidence from the messages
- Indicate confidence level (high/medium/low)
- Note whether this is self-disclosed or mentioned by someone else

## Complete PII Taxonomy

Extract any of the following if present:

### Core Identity
full_legal_name, given_name, middle_name, family_name, maiden_name, previous_names, nicknames, aliases, date_of_birth, age, birth_year, place_of_birth, gender, pronouns, nationality, ethnicity, languages

### Physical Description
height, weight, eye_color, hair_color, hair_style, skin_tone, distinguishing_marks, glasses, facial_hair

### Contact Information
email_personal, email_work, email_school, email_other, phone_mobile, phone_home, phone_work, phone_fax, address_home, address_work, address_mailing, address_previous

### Digital Identity
username_*, social_twitter, social_instagram, social_linkedin, social_facebook, social_tiktok, social_youtube, social_reddit, social_discord, social_other, website_personal, website_business, gaming_handle, login_email, password_hints

### Relationships
spouse, partner, ex_spouse, children, parents, siblings, grandparents, grandchildren, aunts_uncles, cousins, in_laws, nieces_nephews, friends, roommates, neighbors, pets, emergency_contact, next_of_kin

### Professional
**IMPORTANT**: Distinguish between EMPLOYMENT (working FOR someone) vs OWNERSHIP (owning a business).

Employment: employer_current, employer_previous, job_title_current, job_title_previous, department, role_description, manager, direct_reports, colleagues, employee_id

Ownership: business_owned, business_role, business_founded, business_invested, board_member_of

General: profession, industry, years_experience, professional_certifications, professional_licenses, work_email, work_phone, work_address, business_partners, salary, work_schedule

### Education
school_current, school_previous, degree, major, minor, graduation_year, gpa, student_id, certifications, licenses, awards, activities

### Government & Legal IDs
ssn, passport_number, passport_country, drivers_license, drivers_license_state, national_id, visa_type, visa_status, tax_id, voter_registration, military_id, criminal_record, court_cases

### Financial
bank_name, bank_account, credit_cards, paypal, venmo, cashapp, zelle, crypto_wallet, income, net_worth, credit_score, debts, mortgage, investments

### Medical & Health
conditions, disabilities, medications, allergies, blood_type, height_medical, weight_medical, doctor, dentist, specialists, hospital, insurance_health, insurance_dental, pharmacy, medical_history, mental_health

### Life Events & Dates
birthday, birth_date_full, wedding_date, divorce_date, graduation_dates, job_start_dates, job_end_dates, move_dates, retirement_date, death_date, significant_events

### Location & Presence
location_current, location_state, location_country, location_timezone, location_previous, location_hometown, location_vacation, location_frequent, commute, travel_current, travel_planned, travel_history

### Preferences & Lifestyle
political_affiliation, religious_affiliation, hobbies, sports_played, sports_watched, music_preferences, movie_preferences, book_preferences, food_preferences, dietary_restrictions, restaurant_favorites, drink_preferences, smoking, alcohol, exercise, sleep_schedule

### Vehicles & Property
vehicle_make, vehicle_model, vehicle_year, vehicle_color, license_plate, vehicle_previous, motorcycle, boat, property_owned, rental

## Output Format

Return JSON with this structure:

{
  "persons": [
    {
      "reference": "Dad",
      "is_primary_contact": true,
      "confidence_is_primary": 0.99,
      "pii": {
        "core_identity": {
          "full_legal_name": {
            "value": "James Brandt",
            "confidence": "high",
            "evidence": ["meeting up with Jim and Janet", "Jim@napageneralstore.com"],
            "self_disclosed": false
          },
          "nicknames": {
            "value": ["Jim", "Dad"],
            "confidence": "high",
            "evidence": ["labeled as Dad in contacts", "refers to self as Jim"],
            "self_disclosed": true
          }
        },
        "contact_information": {
          "email_work": {
            "value": "jim@napageneralstore.com",
            "confidence": "high",
            "evidence": ["the recovery email is my jim@napageneralstore.com"],
            "self_disclosed": true
          }
        },
        "professional": {
          "business_owned": {
            "value": ["Napa General Store"],
            "confidence": "high",
            "evidence": ["jim@napageneralstore.com", "owns the store"]
          }
        }
      }
    }
  ],
  "new_identity_candidates": [
    {
      "reference": "Janet",
      "known_facts": {
        "given_name": "Janet",
        "relationship_to_primary": "friend/travel companion"
      }
    }
  ],
  "unattributed_facts": [
    {
      "fact_type": "phone",
      "fact_value": "+15551234567",
      "shared_by": "Dad",
      "context": "Sent as standalone message with no explanation",
      "possible_attributions": ["Dad's alternate number", "Third party contact"]
    }
  ]
}

## Important Rules

1. **Extract EVERYTHING** - Even small details can help with identity resolution
2. **Quote exact evidence** - Always include message text that supports extraction
3. **Attribute correctly** - Be very careful about WHO each piece of PII belongs to
4. **Flag sensitive data** - Mark SSN, financial, medical info
5. **Note self-disclosure** - Mark when someone shares their own info vs being mentioned
6. **Create identity candidates** - Flag third parties with enough detail
7. **Use unattributed_facts** - If identifier shared without clear ownership, put in unattributed_facts
8. **Owner vs Employer** - Someone who owns a restaurant is NOT employed BY it
9. **Confidence levels**: high (explicit), medium (implied), low (inferred)
10. **Don't hallucinate** - Only extract what's in the messages

Conversation:
{{{conversation_text}}}`

			piiFacetsConfig := `{
				"mappings": [
					{"json_path": "persons[].pii.core_identity.full_legal_name.value", "facet_type": "pii_full_name"},
					{"json_path": "persons[].pii.core_identity.given_name.value", "facet_type": "pii_given_name"},
					{"json_path": "persons[].pii.core_identity.family_name.value", "facet_type": "pii_family_name"},
					{"json_path": "persons[].pii.core_identity.nicknames.value[]", "facet_type": "pii_nickname"},
					{"json_path": "persons[].pii.contact_information.email_personal.value", "facet_type": "pii_email_personal"},
					{"json_path": "persons[].pii.contact_information.email_work.value", "facet_type": "pii_email_work"},
					{"json_path": "persons[].pii.contact_information.phone_mobile.value", "facet_type": "pii_phone_mobile"},
					{"json_path": "persons[].pii.contact_information.phone_home.value", "facet_type": "pii_phone_home"},
					{"json_path": "persons[].pii.contact_information.phone_work.value", "facet_type": "pii_phone_work"},
					{"json_path": "persons[].pii.contact_information.address_home.value", "facet_type": "pii_address_home"},
					{"json_path": "persons[].pii.digital_identity.social_twitter.value", "facet_type": "pii_social_twitter"},
					{"json_path": "persons[].pii.digital_identity.social_instagram.value", "facet_type": "pii_social_instagram"},
					{"json_path": "persons[].pii.digital_identity.social_linkedin.value", "facet_type": "pii_social_linkedin"},
					{"json_path": "persons[].pii.professional.employer_current.value", "facet_type": "pii_employer"},
					{"json_path": "persons[].pii.professional.business_owned.value[]", "facet_type": "pii_business_owned"},
					{"json_path": "persons[].pii.professional.profession.value", "facet_type": "pii_profession"},
					{"json_path": "persons[].pii.location_presence.location_current.value", "facet_type": "pii_location"},
					{"json_path": "persons[].pii.relationships.spouse.value", "facet_type": "pii_spouse"},
					{"json_path": "persons[].pii.relationships.children.value[]", "facet_type": "pii_child"}
				]
			}`

			_, err = database.ExecContext(ctx, `
				INSERT INTO analysis_types (id, name, version, description, output_type, facets_config_json, prompt_template, model, created_at, updated_at)
				VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
				ON CONFLICT(name) DO NOTHING
			`, "pii_extraction_v1", "pii_extraction", "1.0.0",
				"Extract all PII from segments for identity resolution",
				"structured", piiFacetsConfig, piiPromptTemplate,
				"gemini-2.0-flash", now, now)

			if err != nil {
				fmt.Fprintf(os.Stderr, "Error seeding pii_extraction_v1: %v\n", err)
				os.Exit(1)
			}

			// Seed nexus_cli_invocations_v1 analysis type (local extraction)
			nexusCliPromptTemplate := `# Nexus CLI Invocation Extraction

This analysis is generated locally from tool invocation events.
Conversation:
{{{conversation_text}}}`

			nexusCliFacetsConfig := `{
				"mappings": [
					{"json_path": "invocations[]", "facet_type": "nexus_invocation"},
					{"json_path": "commands[]", "facet_type": "nexus_command"},
					{"json_path": "subcommands[]", "facet_type": "nexus_subcommand"},
					{"json_path": "binaries[]", "facet_type": "nexus_binary"}
				]
			}`

			_, err = database.ExecContext(ctx, `
				INSERT INTO analysis_types (id, name, version, description, output_type, facets_config_json, prompt_template, model, created_at, updated_at)
				VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
				ON CONFLICT(name) DO NOTHING
			`, "nexus_cli_invocations_v1", "nexus_cli_invocations", "1.0.0",
				"Extract nexus CLI invocations from Cursor tool executions",
				"structured", nexusCliFacetsConfig, nexusCliPromptTemplate,
				"local", now, now)

			if err != nil {
				fmt.Fprintf(os.Stderr, "Error seeding nexus_cli_invocations_v1: %v\n", err)
				os.Exit(1)
			}

			// Seed terminal_invocations_v1 analysis type (local extraction)
			terminalPromptTemplate := `# Terminal Invocation Extraction

This analysis is generated locally from tool invocation events.
Conversation:
{{{conversation_text}}}`

			terminalFacetsConfig := `{
				"mappings": [
					{"json_path": "invocations[]", "facet_type": "terminal_invocation"},
					{"json_path": "commands[]", "facet_type": "terminal_command"},
					{"json_path": "subcommands[]", "facet_type": "terminal_subcommand"},
					{"json_path": "binaries[]", "facet_type": "terminal_binary"}
				]
			}`

			_, err = database.ExecContext(ctx, `
				INSERT INTO analysis_types (id, name, version, description, output_type, facets_config_json, prompt_template, model, created_at, updated_at)
				VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
				ON CONFLICT(name) DO NOTHING
			`, "terminal_invocations_v1", "terminal_invocations", "1.0.0",
				"Extract terminal command invocations from Cursor tool executions",
				"structured", terminalFacetsConfig, terminalPromptTemplate,
				"local", now, now)

			if err != nil {
				fmt.Fprintf(os.Stderr, "Error seeding terminal_invocations_v1: %v\n", err)
				os.Exit(1)
			}

			// Seed self_preference_extraction_v1 analysis type
			selfPreferencePrompt := readPrompt("self-preference-extraction-v1.prompt.md")
			selfPreferenceFacetsConfig := `{
				"mappings": [
					{"json_path": "preferences[].memory_entry", "facet_type": "self_preference"}
				]
			}`
			_, err = database.ExecContext(ctx, `
				INSERT INTO analysis_types (id, name, version, description, output_type, facets_config_json, prompt_template, model, created_at, updated_at)
				VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
				ON CONFLICT(name) DO NOTHING
			`, "self_preference_extraction_v1", "self_preference_extraction_v1", "1.0.0",
				"Extract user preferences for memory synthesis",
				"structured", selfPreferenceFacetsConfig, selfPreferencePrompt,
				"gemini-2.0-flash", now, now)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error seeding self_preference_extraction_v1: %v\n", err)
				os.Exit(1)
			}

			// Seed self_knowledge_extraction_v1 analysis type
			selfKnowledgePrompt := readPrompt("self-knowledge-extraction-v1.prompt.md")
			selfKnowledgeFacetsConfig := `{
				"mappings": [
					{"json_path": "knowledge[].memory_entry", "facet_type": "self_knowledge"}
				]
			}`
			_, err = database.ExecContext(ctx, `
				INSERT INTO analysis_types (id, name, version, description, output_type, facets_config_json, prompt_template, model, created_at, updated_at)
				VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
				ON CONFLICT(name) DO NOTHING
			`, "self_knowledge_extraction_v1", "self_knowledge_extraction_v1", "1.0.0",
				"Extract user knowledge and expertise for memory synthesis",
				"structured", selfKnowledgeFacetsConfig, selfKnowledgePrompt,
				"gemini-2.0-flash", now, now)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error seeding self_knowledge_extraction_v1: %v\n", err)
				os.Exit(1)
			}

			// Seed correction_extraction_v1 analysis type
			correctionPrompt := readPrompt("correction-extraction-v1.prompt.md")
			correctionFacetsConfig := `{
				"mappings": [
					{"json_path": "corrections[].memory_entry", "facet_type": "self_correction"},
					{"json_path": "frustration_signals[].implied_rule", "facet_type": "self_correction"}
				]
			}`
			_, err = database.ExecContext(ctx, `
				INSERT INTO analysis_types (id, name, version, description, output_type, facets_config_json, prompt_template, model, created_at, updated_at)
				VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
				ON CONFLICT(name) DO NOTHING
			`, "correction_extraction_v1", "correction_extraction_v1", "1.0.0",
				"Extract AI corrections and behavioral rules for memory synthesis",
				"structured", correctionFacetsConfig, correctionPrompt,
				"gemini-2.0-flash", now, now)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error seeding correction_extraction_v1: %v\n", err)
				os.Exit(1)
			}

			// Seed relationship_context_extraction_v1 analysis type
			relationshipPrompt := readPrompt("relationship-context-extraction-v1.prompt.md")
			relationshipFacetsConfig := `{
				"mappings": [
					{"json_path": "relationships[].memory_entry", "facet_type": "relationship_context"}
				]
			}`
			_, err = database.ExecContext(ctx, `
				INSERT INTO analysis_types (id, name, version, description, output_type, facets_config_json, prompt_template, model, created_at, updated_at)
				VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
				ON CONFLICT(name) DO NOTHING
			`, "relationship_context_extraction_v1", "relationship_context_extraction_v1", "1.0.0",
				"Extract relationship context for user memory",
				"structured", relationshipFacetsConfig, relationshipPrompt,
				"gemini-2.0-flash", now, now)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error seeding relationship_context_extraction_v1: %v\n", err)
				os.Exit(1)
			}

			// Seed workspace_pattern_extraction_v1 analysis type
			workspacePatternPrompt := readPrompt("workspace-pattern-extraction-v1.prompt.md")
			workspacePatternFacetsConfig := `{
				"mappings": [
					{"json_path": "workspace_patterns[].memory_entry", "facet_type": "workspace_convention"}
				]
			}`
			_, err = database.ExecContext(ctx, `
				INSERT INTO analysis_types (id, name, version, description, output_type, facets_config_json, prompt_template, model, created_at, updated_at)
				VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
				ON CONFLICT(name) DO NOTHING
			`, "workspace_pattern_extraction_v1", "workspace_pattern_extraction_v1", "1.0.0",
				"Extract workspace conventions and patterns for shared memory",
				"structured", workspacePatternFacetsConfig, workspacePatternPrompt,
				"gemini-2.0-flash", now, now)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error seeding workspace_pattern_extraction_v1: %v\n", err)
				os.Exit(1)
			}

			// Seed turn_quality_v1 analysis type
			turnQualityPrompt := readPrompt("checkpoint-feedback-v1.prompt.md")
			turnQualityFacetsConfig := `{
				"mappings": [
					{"json_path": "feedback[].sentiment", "facet_type": "turn_sentiment"},
					{"json_path": "feedback[].correction", "facet_type": "turn_correction"},
					{"json_path": "feedback[].frustration", "facet_type": "turn_frustration"},
					{"json_path": "feedback[].praise", "facet_type": "turn_praise"},
					{"json_path": "feedback[].confusion", "facet_type": "turn_confusion"},
					{"json_path": "feedback[].acceptance", "facet_type": "turn_acceptance"},
					{"json_path": "aggregate.quality_band", "facet_type": "turn_quality_band"},
					{"json_path": "aggregate.quality_score", "facet_type": "turn_quality_score"},
					{"json_path": "aggregate.correction_count", "facet_type": "turn_correction_count"},
					{"json_path": "aggregate.frustration_count", "facet_type": "turn_frustration_count"},
					{"json_path": "aggregate.praise_count", "facet_type": "turn_praise_count"}
				]
			}`
			_, err = database.ExecContext(ctx, `
				INSERT INTO analysis_types (id, name, version, description, output_type, facets_config_json, prompt_template, model, created_at, updated_at)
				VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
				ON CONFLICT(name) DO NOTHING
			`, "turn_quality_v1", "turn_quality_v1", "1.0.0",
				"Extract per-turn quality signals from AI feedback",
				"structured", turnQualityFacetsConfig, turnQualityPrompt,
				"gemini-2.0-flash", now, now)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error seeding turn_quality_v1: %v\n", err)
				os.Exit(1)
			}

			if jsonOutput {
				printJSON(map[string]any{"ok": true, "message": "Seeded analysis types"})
			} else {
				fmt.Println("Seeded analysis types:")
				fmt.Println("  - convo-all-v1 (structured extraction)")
				fmt.Println("  - pii_extraction_v1 (PII extraction for identity resolution)")
				fmt.Println("  - nexus_cli_invocations_v1 (nexus CLI extraction)")
				fmt.Println("  - terminal_invocations_v1 (terminal command extraction)")
				fmt.Println("  - self_preference_extraction_v1 (user preferences)")
				fmt.Println("  - self_knowledge_extraction_v1 (user knowledge)")
				fmt.Println("  - correction_extraction_v1 (AI corrections)")
				fmt.Println("  - relationship_context_extraction_v1 (relationship context)")
				fmt.Println("  - workspace_pattern_extraction_v1 (workspace conventions)")
				fmt.Println("  - turn_quality_v1 (turn-level quality signals)")
			}
		},
	}

	computeCmd.AddCommand(computeRunCmd)
	computeCmd.AddCommand(computeEnqueueCmd)
	computeCmd.AddCommand(computeStatsCmd)
	computeCmd.AddCommand(computeSeedCmd)
	rootCmd.AddCommand(computeCmd)

	// search command - semantic search using embeddings
	var searchChannel string
	var searchLimit int
	var searchModel string

	searchCmd := &cobra.Command{
		Use:   "search [query]",
		Short: "Semantic search across segments using embeddings",
		Long: `Search segments using semantic similarity.

Uses AI embeddings to find segments that match the meaning
of your query, not just keyword matches.

Examples:
  cortex search "when did we talk about moving"
  cortex search "restaurant recommendations" --channel imessage
  cortex search "project deadlines" --limit 5`,
		Args: cobra.MinimumNArgs(1),
		Run: func(cmd *cobra.Command, args []string) {
			type SearchResult struct {
				EpisodeID      string  `json:"episode_id"`
				Channel        string  `json:"channel,omitempty"`
				ThreadID       string  `json:"thread_id,omitempty"`
				ThreadName     string  `json:"thread_name,omitempty"`
				StartTime      int64   `json:"start_time"`
				EndTime        int64   `json:"end_time"`
				EventCount     int     `json:"event_count"`
				Similarity     float64 `json:"similarity"`
				Preview        string  `json:"preview,omitempty"`
			}

			type Result struct {
				OK      bool           `json:"ok"`
				Query   string         `json:"query"`
				Results []SearchResult `json:"results"`
				Message string         `json:"message,omitempty"`
			}

			queryText := strings.Join(args, " ")
			if queryText == "" {
				result := Result{OK: false, Message: "Search query is required"}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			// Get API key
			apiKey := os.Getenv("GEMINI_API_KEY")
			if apiKey == "" {
				result := Result{OK: false, Query: queryText, Message: "GEMINI_API_KEY environment variable required for semantic search"}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Query: queryText, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			ctx := context.Background()

			embedder := &search.GeminiEmbedder{Client: gemini.NewClient(apiKey)}
			model := searchModel
			if model == "" {
				model = "gemini-embedding-001"
			}

			searcher := search.NewSearcher(database, embedder)
			resp, err := searcher.SearchSegments(ctx, search.SegmentSearchRequest{
				Query:         queryText,
				Channel:       searchChannel,
				Limit:         searchLimit,
				Model:         model,
				UseEmbeddings: true,
			})
			if err != nil {
				result := Result{OK: false, Query: queryText, Message: fmt.Sprintf("Failed to search segments: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			results := make([]SearchResult, 0, len(resp.Results))
			for _, r := range resp.Results {
				results = append(results, SearchResult{
					EpisodeID:  r.EpisodeID,
					Channel:    r.Channel,
					ThreadID:   r.ThreadID,
					ThreadName: r.ThreadName,
					StartTime:  r.StartTime,
					EndTime:    r.EndTime,
					EventCount: r.EventCount,
					Similarity: r.Score,
				})
			}

			// Get preview for top results
			for i := range results {
				preview, _ := getEpisodePreview(ctx, database, results[i].EpisodeID, 200)
				results[i].Preview = preview
			}

			result := Result{
				OK:      true,
				Query:   queryText,
				Results: results,
			}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Printf("Search results for: %q\n\n", queryText)
				if len(results) == 0 {
					fmt.Println("No matching segments found.")
					fmt.Println("\nTip: Make sure you have embeddings generated (run: cortex compute enqueue embeddings && cortex compute run)")
				} else {
					for i, r := range results {
						timeStr := time.Unix(r.StartTime, 0).Format("2006-01-02 15:04")
						fmt.Printf("%d. [%.2f] %s", i+1, r.Similarity, timeStr)
						if r.ThreadName != "" {
							fmt.Printf(" - %s", r.ThreadName)
						} else if r.Channel != "" {
							fmt.Printf(" - %s", r.Channel)
						}
						fmt.Printf(" (%d messages)\n", r.EventCount)
						if r.Preview != "" {
							// Truncate and indent preview
							preview := r.Preview
							if len(preview) > 150 {
								preview = preview[:147] + "..."
							}
							fmt.Printf("   %s\n", preview)
						}
						fmt.Println()
					}
				}
			}
		},
	}

	searchCmd.Flags().StringVar(&searchChannel, "channel", "", "Filter by channel (imessage, gmail, aix, etc.)")
	searchCmd.Flags().IntVar(&searchLimit, "limit", 10, "Maximum number of results")
	searchCmd.Flags().StringVar(&searchModel, "model", "gemini-embedding-001", "Embedding model to use")
	rootCmd.AddCommand(searchCmd)

	// route command - candidate segments for routing
	var routeChannel string
	var routeDefinition string
	var routeLimit int
	var routeModel string
	var routeMinScore float64

	routeCmd := &cobra.Command{
		Use:   "route [query]",
		Short: "Find candidate segments for routing",
		Long: `Find candidate segments for routing decisions.

Examples:
  cortex route "continue auth refactor"
  cortex route "fix lint errors" --definition ai_turn_pair --limit 5`,
		Args: cobra.MinimumNArgs(1),
		Run: func(cmd *cobra.Command, args []string) {
			type RouteCandidate struct {
				EpisodeID      string  `json:"episode_id"`
				DefinitionName string  `json:"definition_name,omitempty"`
				Channel        string  `json:"channel,omitempty"`
				ThreadID       string  `json:"thread_id,omitempty"`
				ThreadName     string  `json:"thread_name,omitempty"`
				StartTime      int64   `json:"start_time"`
				EndTime        int64   `json:"end_time"`
				EventCount     int     `json:"event_count"`
				Score          float64 `json:"score"`
				Preview        string  `json:"preview,omitempty"`
			}

			type Result struct {
				OK         bool             `json:"ok"`
				Query      string           `json:"query"`
				Candidates []RouteCandidate `json:"candidates"`
				Message    string           `json:"message,omitempty"`
			}

			queryText := strings.Join(args, " ")
			if strings.TrimSpace(queryText) == "" {
				result := Result{OK: false, Message: "Query is required"}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			apiKey := os.Getenv("GEMINI_API_KEY")
			if apiKey == "" {
				result := Result{OK: false, Query: queryText, Message: "GEMINI_API_KEY environment variable required for routing search"}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Query: queryText, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			model := routeModel
			if strings.TrimSpace(model) == "" {
				model = "gemini-embedding-001"
			}

			definitionName := strings.TrimSpace(routeDefinition)
			segmentReq := search.SegmentSearchRequest{
				Query:         queryText,
				Channel:       routeChannel,
				DefinitionName: definitionName,
				Limit:         routeLimit,
				MinScore:      routeMinScore,
				Model:         model,
				UseEmbeddings: true,
			}

			searcher := search.NewSearcher(database, &search.GeminiEmbedder{Client: gemini.NewClient(apiKey)})
			resp, err := searcher.SearchSegments(cmd.Context(), segmentReq)
			if err != nil {
				result := Result{OK: false, Query: queryText, Message: fmt.Sprintf("Failed to search segments: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			candidates := make([]RouteCandidate, 0, len(resp.Results))
			for _, r := range resp.Results {
				candidates = append(candidates, RouteCandidate{
					EpisodeID:      r.EpisodeID,
					DefinitionName: r.DefinitionName,
					Channel:        r.Channel,
					ThreadID:       r.ThreadID,
					ThreadName:     r.ThreadName,
					StartTime:      r.StartTime,
					EndTime:        r.EndTime,
					EventCount:     r.EventCount,
					Score:          r.Score,
				})
			}

			for i := range candidates {
				preview, _ := getEpisodePreview(cmd.Context(), database, candidates[i].EpisodeID, 200)
				candidates[i].Preview = preview
			}

			result := Result{
				OK:         true,
				Query:      queryText,
				Candidates: candidates,
			}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Printf("Route candidates for: %q\n\n", queryText)
				if len(candidates) == 0 {
					fmt.Println("No matching segments found.")
					return
				}
				for i, c := range candidates {
					timeStr := time.Unix(c.StartTime, 0).Format("2006-01-02 15:04")
					fmt.Printf("%d. [%.2f] %s", i+1, c.Score, timeStr)
					if c.ThreadName != "" {
						fmt.Printf(" - %s", c.ThreadName)
					} else if c.Channel != "" {
						fmt.Printf(" - %s", c.Channel)
					}
					fmt.Printf(" (%d messages)\n", c.EventCount)
					if c.Preview != "" {
						preview := c.Preview
						if len(preview) > 150 {
							preview = preview[:147] + "..."
						}
						fmt.Printf("   %s\n", preview)
					}
					fmt.Println()
				}
			}
		},
	}

	routeCmd.Flags().StringVar(&routeChannel, "channel", "", "Filter by channel (imessage, gmail, cursor, etc.)")
	routeCmd.Flags().StringVar(&routeDefinition, "definition", "ai_turn_pair", "Segment definition to route against")
	routeCmd.Flags().IntVar(&routeLimit, "limit", 5, "Maximum number of candidates")
	routeCmd.Flags().Float64Var(&routeMinScore, "min-score", 0.0, "Minimum similarity score")
	routeCmd.Flags().StringVar(&routeModel, "model", "gemini-embedding-001", "Embedding model to use")
	rootCmd.AddCommand(routeCmd)

	// documents command - search document-style events
	var docSearchChannels string
	var docSearchLimit int
	var docSearchModel string
	var docSearchMinScore float64
	var docSearchEmbeddings bool
	var docSearchLexical bool
	var docSearchTrack bool

	documentsCmd := &cobra.Command{
		Use:   "documents",
		Short: "Search document-style events (skills, docs, memory, tools)",
	}

	documentsSearchCmd := &cobra.Command{
		Use:   "search [query]",
		Short: "Semantic search across documents",
		Long: `Search document-style events using hybrid semantic + lexical scoring.

Examples:
  cortex documents search "send email"
  cortex documents search "routing spec" --channel doc --limit 5
  cortex documents search "whatsapp" --lexical-only`,
		Args: cobra.MinimumNArgs(1),
		Run: func(cmd *cobra.Command, args []string) {
			queryText := strings.Join(args, " ")
			if strings.TrimSpace(queryText) == "" {
				if jsonOutput {
					printJSON(map[string]any{"ok": false, "message": "Search query is required"})
				} else {
					fmt.Fprintln(os.Stderr, "Error: Search query is required")
				}
				os.Exit(1)
			}

			database, err := db.Open()
			if err != nil {
				if jsonOutput {
					printJSON(map[string]any{"ok": false, "message": fmt.Sprintf("Failed to open database: %v", err)})
				} else {
					fmt.Fprintf(os.Stderr, "Error: %v\n", err)
				}
				os.Exit(1)
			}
			defer database.Close()

			useEmbeddings := docSearchEmbeddings
			useLexical := docSearchLexical
			if !useEmbeddings && !useLexical {
				useEmbeddings = true
				useLexical = true
			}

			var embedder search.Embedder
			if useEmbeddings {
				apiKey := os.Getenv("GEMINI_API_KEY")
				if apiKey == "" {
					useEmbeddings = false
					if !jsonOutput {
						fmt.Fprintln(os.Stderr, "Warning: GEMINI_API_KEY not set, falling back to lexical search")
					}
				} else {
					embedder = &search.GeminiEmbedder{Client: gemini.NewClient(apiKey)}
				}
			}

			channels := []string{}
			if strings.TrimSpace(docSearchChannels) != "" {
				for _, ch := range strings.Split(docSearchChannels, ",") {
					ch = strings.TrimSpace(ch)
					if ch != "" {
						channels = append(channels, ch)
					}
				}
			}

			searcher := search.NewSearcher(database, embedder)
			resp, err := searcher.SearchDocuments(context.Background(), search.DocumentSearchRequest{
				Query:          queryText,
				Channels:       channels,
				Limit:          docSearchLimit,
				MinScore:       docSearchMinScore,
				Model:          docSearchModel,
				UseEmbeddings:  useEmbeddings,
				UseLexical:     useLexical,
				TrackRetrieval: docSearchTrack,
			})
			if err != nil {
				if jsonOutput {
					printJSON(map[string]any{"ok": false, "message": err.Error()})
				} else {
					fmt.Fprintf(os.Stderr, "Error: %v\n", err)
				}
				os.Exit(1)
			}

			if jsonOutput {
				printJSON(resp)
				return
			}

			fmt.Printf("Document search results for: %q\n\n", queryText)
			if len(resp.Results) == 0 {
				fmt.Println("No matching documents found.")
				return
			}

			for i, r := range resp.Results {
				fmt.Printf("%d. [%.2f] %s (%s)\n", i+1, r.Score, r.DocKey, r.Channel)
				if r.Title != "" {
					fmt.Printf("   Title: %s\n", r.Title)
				}
				if r.Description != "" {
					fmt.Printf("   Description: %s\n", r.Description)
				}
				if r.Snippet != "" {
					fmt.Printf("   Snippet: %s\n", r.Snippet)
				}
				fmt.Println()
			}
		},
	}

	documentsSearchCmd.Flags().StringVar(&docSearchChannels, "channel", "", "Filter by channel (comma-separated)")
	documentsSearchCmd.Flags().IntVar(&docSearchLimit, "limit", 10, "Maximum number of results")
	documentsSearchCmd.Flags().Float64Var(&docSearchMinScore, "min-score", 0.0, "Minimum score threshold")
	documentsSearchCmd.Flags().StringVar(&docSearchModel, "model", "gemini-embedding-001", "Embedding model to use")
	documentsSearchCmd.Flags().BoolVar(&docSearchEmbeddings, "embeddings", true, "Enable embedding-based search")
	documentsSearchCmd.Flags().BoolVar(&docSearchLexical, "lexical", true, "Enable lexical search")
	documentsSearchCmd.Flags().BoolVar(&docSearchTrack, "track", false, "Track retrieval metrics")

	// documents index - index skills and docs into document_heads
	var indexSkillsPath string
	
	documentsIndexCmd := &cobra.Command{
		Use:   "index",
		Short: "Index skills and docs into document_heads",
		Long: `Index skills from the nexus skills directory into document_heads for search.

Examples:
  cortex documents index
  cortex documents index --skills-path ~/nexus/skills`,
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK       bool   `json:"ok"`
				Indexed  int    `json:"indexed"`
				Skipped  int    `json:"skipped"`
				Errors   int    `json:"errors"`
				Duration string `json:"duration"`
				Message  string `json:"message,omitempty"`
			}

			start := time.Now()

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			// Determine skills path
			skillsPath := indexSkillsPath
			if skillsPath == "" {
				home, _ := os.UserHomeDir()
				skillsPath = filepath.Join(home, "nexus", "skills")
			}

			var indexed, skipped, errors int

			// Walk skills directory
			walkFn := func(path string, info os.FileInfo, walkErr error) error {
				if walkErr != nil {
					return nil
				}
				if info.IsDir() {
					return nil
				}
				if filepath.Base(path) != "SKILL.md" {
					return nil
				}

				content, err := os.ReadFile(path)
				if err != nil {
					errors++
					return nil
				}

				// Extract skill name from path
				dir := filepath.Dir(path)
				skillName := filepath.Base(dir)
				skillType := filepath.Base(filepath.Dir(dir)) // tools, guides, connectors

				docKey := fmt.Sprintf("skill:%s", skillName)
				title := skillName
				description := fmt.Sprintf("%s skill (%s)", skillName, skillType)

				input := documents.DocumentInput{
					DocKey:        docKey,
					Channel:       "skill",
					Content:       string(content),
					Title:         title,
					Description:   description,
					SourceAdapter: "nexus-skills",
					Metadata: map[string]any{
						"skill_type": skillType,
						"path":       path,
					},
				}

				result, err := documents.UpsertDocument(cmd.Context(), database, input)
				if err != nil {
					errors++
					return nil
				}

				if result.Skipped {
					skipped++
				} else {
					indexed++
				}
				return nil
			}

			if err := filepath.Walk(skillsPath, walkFn); err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Walk failed: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{
				OK:       true,
				Indexed:  indexed,
				Skipped:  skipped,
				Errors:   errors,
				Duration: time.Since(start).String(),
			}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Println("Document Indexing Results:")
				fmt.Printf("  Indexed: %d\n", indexed)
				fmt.Printf("  Skipped (unchanged): %d\n", skipped)
				fmt.Printf("  Errors: %d\n", errors)
				fmt.Printf("  Duration: %s\n", result.Duration)
			}
		},
	}
	documentsIndexCmd.Flags().StringVar(&indexSkillsPath, "skills-path", "", "Path to skills directory (default: ~/nexus/skills)")

	documentsCmd.AddCommand(documentsSearchCmd)
	documentsCmd.AddCommand(documentsIndexCmd)
	rootCmd.AddCommand(documentsCmd)

	// ==================== EXTRACT COMMAND ====================
	extractCmd := &cobra.Command{
		Use:   "extract",
		Short: "Extract data from segments using AI",
	}

	// extract pii - extract PII from segments
	var extractChannel string
	var extractSince string
	var extractSegment string
	var extractPerson string
	var extractDryRun bool
	var extractLimit int
	var extractDefinition string

	extractPIICmd := &cobra.Command{
		Use:   "pii",
		Short: "Extract PII from segments for identity resolution",
		Long: `Extract all personally identifiable information from segments
using AI analysis. Creates person_facts for identity resolution.

Examples:
  cortex extract pii --channel imessage --since 30d
  cortex extract pii --segment <segment_id>
  cortex extract pii --person "Dad" --limit 50`,
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK                     bool   `json:"ok"`
				JobsEnqueued           int    `json:"jobs_enqueued"`
				ConversationsToProcess int    `json:"segments_to_process,omitempty"`
				Message                string `json:"message,omitempty"`
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			// Build query to find segments to process
			querySQL := `
				SELECT c.id FROM segments c
				WHERE NOT EXISTS (
					SELECT 1 FROM analysis_runs ar
					JOIN analysis_types at ON ar.analysis_type_id = at.id
					WHERE ar.segment_id = c.id
					AND at.name = 'pii_extraction'
				)
			`
			var queryArgs []interface{}
			var defID string
			var hasDefinition bool

			if extractDefinition != "" {
				err := database.QueryRow(`SELECT id FROM segment_definitions WHERE name = ?`, extractDefinition).Scan(&defID)
				if err != nil {
					result := Result{OK: false, Message: fmt.Sprintf("Definition '%s' not found", extractDefinition)}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
				hasDefinition = true
				querySQL += ` AND c.definition_id = ?`
				queryArgs = append(queryArgs, defID)
			}

			if extractChannel != "" {
				querySQL += ` AND c.channel = ?`
				queryArgs = append(queryArgs, extractChannel)
			}

			if extractSince != "" {
				// Parse since duration (e.g., "30d", "7d", "1h")
				var sinceTime time.Time
				if strings.HasSuffix(extractSince, "d") {
					days, _ := fmt.Sscanf(extractSince, "%dd", new(int))
					if days > 0 {
						var d int
						fmt.Sscanf(extractSince, "%dd", &d)
						sinceTime = time.Now().AddDate(0, 0, -d)
					}
				} else if strings.HasSuffix(extractSince, "h") {
					var h int
					fmt.Sscanf(extractSince, "%dh", &h)
					sinceTime = time.Now().Add(-time.Duration(h) * time.Hour)
				} else {
					// Try parsing as date
					sinceTime, _ = time.Parse("2006-01-02", extractSince)
				}
				if !sinceTime.IsZero() {
					querySQL += ` AND c.start_time >= ?`
					queryArgs = append(queryArgs, sinceTime.Unix())
				}
			}

			if extractSegment != "" {
				querySQL = `SELECT c.id FROM segments c WHERE c.id = ?`
				queryArgs = []interface{}{extractSegment}
				if hasDefinition {
					querySQL += ` AND c.definition_id = ?`
					queryArgs = append(queryArgs, defID)
				}
			}

			if extractPerson != "" {
				querySQL = `
					SELECT DISTINCT c.id FROM segments c
					JOIN segment_events ce ON c.id = ce.segment_id
					JOIN event_participants ep ON ce.event_id = ep.event_id
					JOIN persons p ON ep.person_id = p.id
					WHERE (p.canonical_name LIKE ? OR p.display_name LIKE ?)
					AND NOT EXISTS (
						SELECT 1 FROM analysis_runs ar
						JOIN analysis_types at ON ar.analysis_type_id = at.id
						WHERE ar.segment_id = c.id
						AND at.name = 'pii_extraction'
					)
				`
				queryArgs = []interface{}{"%" + extractPerson + "%", "%" + extractPerson + "%"}
				if hasDefinition {
					querySQL += ` AND c.definition_id = ?`
					queryArgs = append(queryArgs, defID)
				}
			}

			querySQL += ` ORDER BY c.start_time DESC`

			if extractLimit > 0 {
				querySQL += fmt.Sprintf(` LIMIT %d`, extractLimit)
			}

			// Execute query
			rows, err := database.Query(querySQL, queryArgs...)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to query segments: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			var convIDs []string
			for rows.Next() {
				var id string
				if err := rows.Scan(&id); err != nil {
					continue
				}
				convIDs = append(convIDs, id)
			}
			rows.Close()

			if extractDryRun {
				result := Result{
					OK:                     true,
					ConversationsToProcess: len(convIDs),
					Message:                fmt.Sprintf("Would enqueue %d segments for PII extraction", len(convIDs)),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Printf("Dry run: would enqueue %d segments for PII extraction\n", len(convIDs))
					if len(convIDs) > 0 && len(convIDs) <= 10 {
						fmt.Println("\nSegments:")
						for _, id := range convIDs {
							fmt.Printf("  %s\n", id)
						}
					}
				}
				return
			}

			// Enqueue analysis jobs
			apiKey := os.Getenv("GEMINI_API_KEY")
			geminiClient := gemini.NewClient(apiKey)
			engine, err := compute.NewEngine(database, geminiClient, compute.DefaultConfig())
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to create compute engine: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			ctx := context.Background()
			count, err := engine.EnqueueAnalysis(ctx, "pii_extraction", convIDs...)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to enqueue analysis: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{
				OK:           true,
				JobsEnqueued: count,
				Message:      fmt.Sprintf("Enqueued %d PII extraction jobs", count),
			}
			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Printf("✓ Enqueued %d PII extraction jobs\n", count)
				fmt.Println("\nRun 'cortex compute run' to process the queue")
			}
		},
	}
	extractPIICmd.Flags().StringVar(&extractChannel, "channel", "", "Filter by channel (imessage, gmail, all)")
	extractPIICmd.Flags().StringVar(&extractSince, "since", "", "Only process segments since (e.g., 30d, 7d, 2024-01-01)")
	extractPIICmd.Flags().StringVar(&extractSegment, "segment", "", "Process specific segment ID")
	extractPIICmd.Flags().StringVar(&extractSegment, "conversation", "", "Alias for --segment")
	extractPIICmd.Flags().StringVar(&extractPerson, "person", "", "Process segments involving specific person")
	extractPIICmd.Flags().BoolVar(&extractDryRun, "dry-run", false, "Show what would be processed without enqueueing")
	extractPIICmd.Flags().IntVar(&extractLimit, "limit", 0, "Limit number of segments to process")
	extractPIICmd.Flags().StringVar(&extractDefinition, "definition", "", "Filter by segment definition name")

	// extract nexus-cli - extract nexus CLI invocations from segments
	var extractNexusChannel string
	var extractNexusSince string
	var extractNexusSegment string
	var extractNexusDryRun bool
	var extractNexusLimit int
	var extractNexusDefinition string

	extractNexusCmd := &cobra.Command{
		Use:   "nexus-cli",
		Short: "Extract nexus CLI invocations from AI sessions",
	Long: `Extract nexus CLI invocations from AI tool executions.

Examples:
  cortex extract nexus-cli --channel cursor --since 15d
  cortex extract nexus-cli --definition ai_session --since 15d`,
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK                     bool   `json:"ok"`
				JobsEnqueued           int    `json:"jobs_enqueued"`
				ConversationsToProcess int    `json:"segments_to_process,omitempty"`
				Message                string `json:"message,omitempty"`
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			querySQL := `
				SELECT c.id FROM segments c
				WHERE NOT EXISTS (
					SELECT 1 FROM analysis_runs ar
					JOIN analysis_types at ON ar.analysis_type_id = at.id
					WHERE ar.segment_id = c.id
					AND at.name = 'nexus_cli_invocations'
				)
			`
			var queryArgs []interface{}
			var defID string
			var hasDefinition bool

			if extractNexusDefinition != "" {
				err := database.QueryRow(`SELECT id FROM segment_definitions WHERE name = ?`, extractNexusDefinition).Scan(&defID)
				if err != nil {
					result := Result{OK: false, Message: fmt.Sprintf("Definition '%s' not found", extractNexusDefinition)}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
				hasDefinition = true
				querySQL += ` AND c.definition_id = ?`
				queryArgs = append(queryArgs, defID)
			}

			if extractNexusChannel != "" {
				querySQL += ` AND c.channel = ?`
				queryArgs = append(queryArgs, extractNexusChannel)
			}

			if extractNexusSince != "" {
				var sinceTime time.Time
				if strings.HasSuffix(extractNexusSince, "d") {
					var d int
					fmt.Sscanf(extractNexusSince, "%dd", &d)
					if d > 0 {
						sinceTime = time.Now().AddDate(0, 0, -d)
					}
				} else if strings.HasSuffix(extractNexusSince, "h") {
					var h int
					fmt.Sscanf(extractNexusSince, "%dh", &h)
					if h > 0 {
						sinceTime = time.Now().Add(-time.Duration(h) * time.Hour)
					}
				} else {
					sinceTime, _ = time.Parse("2006-01-02", extractNexusSince)
				}
				if !sinceTime.IsZero() {
					querySQL += ` AND c.start_time >= ?`
					queryArgs = append(queryArgs, sinceTime.Unix())
				}
			}

			if extractNexusSegment != "" {
				querySQL = `SELECT c.id FROM segments c WHERE c.id = ?`
				queryArgs = []interface{}{extractNexusSegment}
				if hasDefinition {
					querySQL += ` AND c.definition_id = ?`
					queryArgs = append(queryArgs, defID)
				}
			}

			querySQL += ` ORDER BY c.start_time DESC`
			if extractNexusLimit > 0 {
				querySQL += fmt.Sprintf(` LIMIT %d`, extractNexusLimit)
			}

			rows, err := database.Query(querySQL, queryArgs...)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to query segments: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			var convIDs []string
			for rows.Next() {
				var id string
				if err := rows.Scan(&id); err != nil {
					continue
				}
				convIDs = append(convIDs, id)
			}
			rows.Close()

			if extractNexusDryRun {
				result := Result{
					OK:                     true,
					ConversationsToProcess: len(convIDs),
					Message:                fmt.Sprintf("Would enqueue %d segments for nexus CLI extraction", len(convIDs)),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Printf("Dry run: would enqueue %d segments for nexus CLI extraction\n", len(convIDs))
					if len(convIDs) > 0 && len(convIDs) <= 10 {
						fmt.Println("\nSegments:")
						for _, id := range convIDs {
							fmt.Printf("  %s\n", id)
						}
					}
				}
				return
			}

			geminiClient := gemini.NewClient("")
			engine, err := compute.NewEngine(database, geminiClient, compute.DefaultConfig())
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to create compute engine: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			ctx := context.Background()
			count, err := engine.EnqueueAnalysis(ctx, "nexus_cli_invocations", convIDs...)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to enqueue analysis: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{
				OK:           true,
				JobsEnqueued: count,
				Message:      fmt.Sprintf("Enqueued %d nexus CLI extraction jobs", count),
			}
			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Printf("✓ Enqueued %d nexus CLI extraction jobs\n", count)
				fmt.Println("\nRun 'cortex compute run' to process the queue")
			}
		},
	}
	extractNexusCmd.Flags().StringVar(&extractNexusChannel, "channel", "", "Filter by channel (cursor, etc.)")
	extractNexusCmd.Flags().StringVar(&extractNexusSince, "since", "", "Only process segments since (e.g., 15d, 7d, 2024-01-01)")
	extractNexusCmd.Flags().StringVar(&extractNexusSegment, "segment", "", "Process specific segment ID")
	extractNexusCmd.Flags().StringVar(&extractNexusSegment, "conversation", "", "Alias for --segment")
	extractNexusCmd.Flags().BoolVar(&extractNexusDryRun, "dry-run", false, "Show what would be processed without enqueueing")
	extractNexusCmd.Flags().IntVar(&extractNexusLimit, "limit", 0, "Limit number of segments to process")
	extractNexusCmd.Flags().StringVar(&extractNexusDefinition, "definition", "", "Filter by segment definition name")

	// extract terminal - extract terminal command invocations
	var extractTerminalChannel string
	var extractTerminalSince string
	var extractTerminalSegment string
	var extractTerminalDryRun bool
	var extractTerminalLimit int
	var extractTerminalDefinition string

	extractTerminalCmd := &cobra.Command{
		Use:   "terminal",
	Short: "Extract terminal command invocations from AI sessions",
	Long: `Extract terminal command invocations from AI tool executions.

Examples:
  cortex extract terminal --channel cursor --since 15d
  cortex extract terminal --definition ai_session --since 15d`,
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK                     bool   `json:"ok"`
				JobsEnqueued           int    `json:"jobs_enqueued"`
				ConversationsToProcess int    `json:"segments_to_process,omitempty"`
				Message                string `json:"message,omitempty"`
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			querySQL := `
				SELECT c.id FROM segments c
				WHERE NOT EXISTS (
					SELECT 1 FROM analysis_runs ar
					JOIN analysis_types at ON ar.analysis_type_id = at.id
					WHERE ar.segment_id = c.id
					AND at.name = 'terminal_invocations'
				)
			`
			var queryArgs []interface{}
			var defID string
			var hasDefinition bool

			if extractTerminalDefinition != "" {
				err := database.QueryRow(`SELECT id FROM segment_definitions WHERE name = ?`, extractTerminalDefinition).Scan(&defID)
				if err != nil {
					result := Result{OK: false, Message: fmt.Sprintf("Definition '%s' not found", extractTerminalDefinition)}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
				hasDefinition = true
				querySQL += ` AND c.definition_id = ?`
				queryArgs = append(queryArgs, defID)
			}

			if extractTerminalChannel != "" {
				querySQL += ` AND c.channel = ?`
				queryArgs = append(queryArgs, extractTerminalChannel)
			}

			if extractTerminalSince != "" {
				var sinceTime time.Time
				if strings.HasSuffix(extractTerminalSince, "d") {
					var d int
					fmt.Sscanf(extractTerminalSince, "%dd", &d)
					if d > 0 {
						sinceTime = time.Now().AddDate(0, 0, -d)
					}
				} else if strings.HasSuffix(extractTerminalSince, "h") {
					var h int
					fmt.Sscanf(extractTerminalSince, "%dh", &h)
					if h > 0 {
						sinceTime = time.Now().Add(-time.Duration(h) * time.Hour)
					}
				} else {
					sinceTime, _ = time.Parse("2006-01-02", extractTerminalSince)
				}
				if !sinceTime.IsZero() {
					querySQL += ` AND c.start_time >= ?`
					queryArgs = append(queryArgs, sinceTime.Unix())
				}
			}

			if extractTerminalSegment != "" {
				querySQL = `SELECT c.id FROM segments c WHERE c.id = ?`
				queryArgs = []interface{}{extractTerminalSegment}
				if hasDefinition {
					querySQL += ` AND c.definition_id = ?`
					queryArgs = append(queryArgs, defID)
				}
			}

			querySQL += ` ORDER BY c.start_time DESC`
			if extractTerminalLimit > 0 {
				querySQL += fmt.Sprintf(` LIMIT %d`, extractTerminalLimit)
			}

			rows, err := database.Query(querySQL, queryArgs...)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to query segments: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			var convIDs []string
			for rows.Next() {
				var id string
				if err := rows.Scan(&id); err != nil {
					continue
				}
				convIDs = append(convIDs, id)
			}
			rows.Close()

			if extractTerminalDryRun {
				result := Result{
					OK:                     true,
					ConversationsToProcess: len(convIDs),
					Message:                fmt.Sprintf("Would enqueue %d segments for terminal extraction", len(convIDs)),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Printf("Dry run: would enqueue %d segments for terminal extraction\n", len(convIDs))
					if len(convIDs) > 0 && len(convIDs) <= 10 {
						fmt.Println("\nConversations:")
						for _, id := range convIDs {
							fmt.Printf("  %s\n", id)
						}
					}
				}
				return
			}

			geminiClient := gemini.NewClient("")
			engine, err := compute.NewEngine(database, geminiClient, compute.DefaultConfig())
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to create compute engine: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			ctx := context.Background()
			count, err := engine.EnqueueAnalysis(ctx, "terminal_invocations", convIDs...)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to enqueue analysis: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{
				OK:           true,
				JobsEnqueued: count,
				Message:      fmt.Sprintf("Enqueued %d terminal extraction jobs", count),
			}
			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Printf("✓ Enqueued %d terminal extraction jobs\n", count)
				fmt.Println("\nRun 'cortex compute run' to process the queue")
			}
		},
	}
	extractTerminalCmd.Flags().StringVar(&extractTerminalChannel, "channel", "", "Filter by channel (cursor, etc.)")
	extractTerminalCmd.Flags().StringVar(&extractTerminalSince, "since", "", "Only process segments since (e.g., 15d, 7d, 2024-01-01)")
	extractTerminalCmd.Flags().StringVar(&extractTerminalSegment, "segment", "", "Process specific segment ID")
	extractTerminalCmd.Flags().StringVar(&extractTerminalSegment, "conversation", "", "Alias for --segment")
	extractTerminalCmd.Flags().BoolVar(&extractTerminalDryRun, "dry-run", false, "Show what would be processed without enqueueing")
	extractTerminalCmd.Flags().IntVar(&extractTerminalLimit, "limit", 0, "Limit number of segments to process")
	extractTerminalCmd.Flags().StringVar(&extractTerminalDefinition, "definition", "", "Filter by segment definition name")

	// extract turn-quality - extract turn-level quality signals
	var extractTurnQualityChannel string
	var extractTurnQualitySince string
	var extractTurnQualitySegment string
	var extractTurnQualityDryRun bool
	var extractTurnQualityLimit int
	var extractTurnQualityDefinition string

	extractTurnQualityCmd := &cobra.Command{
		Use:   "turn-quality",
		Short: "Extract turn-level quality signals from AI turns",
		Long: `Extract turn-level quality signals (correction, frustration, praise).

Examples:
  cortex extract turn-quality --definition ai_turn_pair --since 7d
  cortex extract turn-quality --segment <segment_id>`,
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK                     bool   `json:"ok"`
				JobsEnqueued           int    `json:"jobs_enqueued"`
				ConversationsToProcess int    `json:"segments_to_process,omitempty"`
				Message                string `json:"message,omitempty"`
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			querySQL := `
				SELECT c.id FROM segments c
				WHERE NOT EXISTS (
					SELECT 1 FROM analysis_runs ar
					JOIN analysis_types at ON ar.analysis_type_id = at.id
					WHERE ar.segment_id = c.id
					AND at.name = 'turn_quality_v1'
				)
			`
			var queryArgs []interface{}
			var defID string
			var hasDefinition bool

			if extractTurnQualityDefinition != "" {
				err := database.QueryRow(`SELECT id FROM segment_definitions WHERE name = ?`, extractTurnQualityDefinition).Scan(&defID)
				if err != nil {
					result := Result{OK: false, Message: fmt.Sprintf("Definition '%s' not found", extractTurnQualityDefinition)}
					if jsonOutput {
						printJSON(result)
					} else {
						fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
					}
					os.Exit(1)
				}
				hasDefinition = true
				querySQL += ` AND c.definition_id = ?`
				queryArgs = append(queryArgs, defID)
			}

			if extractTurnQualityChannel != "" {
				querySQL += ` AND c.channel = ?`
				queryArgs = append(queryArgs, extractTurnQualityChannel)
			}

			if extractTurnQualitySince != "" {
				var sinceTime time.Time
				if strings.HasSuffix(extractTurnQualitySince, "d") {
					var d int
					fmt.Sscanf(extractTurnQualitySince, "%dd", &d)
					if d > 0 {
						sinceTime = time.Now().AddDate(0, 0, -d)
					}
				} else if strings.HasSuffix(extractTurnQualitySince, "h") {
					var h int
					fmt.Sscanf(extractTurnQualitySince, "%dh", &h)
					if h > 0 {
						sinceTime = time.Now().Add(-time.Duration(h) * time.Hour)
					}
				} else {
					sinceTime, _ = time.Parse("2006-01-02", extractTurnQualitySince)
				}
				if !sinceTime.IsZero() {
					querySQL += ` AND c.start_time >= ?`
					queryArgs = append(queryArgs, sinceTime.Unix())
				}
			}

			if extractTurnQualitySegment != "" {
				querySQL = `SELECT c.id FROM segments c WHERE c.id = ?`
				queryArgs = []interface{}{extractTurnQualitySegment}
				if hasDefinition {
					querySQL += ` AND c.definition_id = ?`
					queryArgs = append(queryArgs, defID)
				}
			}

			querySQL += ` ORDER BY c.start_time DESC`
			if extractTurnQualityLimit > 0 {
				querySQL += fmt.Sprintf(` LIMIT %d`, extractTurnQualityLimit)
			}

			rows, err := database.Query(querySQL, queryArgs...)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to query segments: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			var convIDs []string
			for rows.Next() {
				var id string
				if err := rows.Scan(&id); err != nil {
					continue
				}
				convIDs = append(convIDs, id)
			}
			rows.Close()

			if extractTurnQualityDryRun {
				result := Result{
					OK:                     true,
					ConversationsToProcess: len(convIDs),
					Message:                fmt.Sprintf("Would enqueue %d segments for turn-quality extraction", len(convIDs)),
				}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Printf("Dry run: would enqueue %d segments for turn-quality extraction\n", len(convIDs))
					if len(convIDs) > 0 && len(convIDs) <= 10 {
						fmt.Println("\nSegments:")
						for _, id := range convIDs {
							fmt.Printf("  %s\n", id)
						}
					}
				}
				return
			}

			geminiClient := gemini.NewClient("")
			engine, err := compute.NewEngine(database, geminiClient, compute.DefaultConfig())
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to create compute engine: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			ctx := context.Background()
			count, err := engine.EnqueueAnalysis(ctx, "turn_quality_v1", convIDs...)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to enqueue analysis: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{
				OK:           true,
				JobsEnqueued: count,
				Message:      fmt.Sprintf("Enqueued %d turn-quality extraction jobs", count),
			}
			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Printf("✓ Enqueued %d turn-quality extraction jobs\n", count)
				fmt.Println("\nRun 'cortex compute run' to process the queue")
			}
		},
	}
	extractTurnQualityCmd.Flags().StringVar(&extractTurnQualityChannel, "channel", "", "Filter by channel (cursor, etc.)")
	extractTurnQualityCmd.Flags().StringVar(&extractTurnQualitySince, "since", "", "Only process segments since (e.g., 7d, 2024-01-01)")
	extractTurnQualityCmd.Flags().StringVar(&extractTurnQualitySegment, "segment", "", "Process specific segment ID")
	extractTurnQualityCmd.Flags().StringVar(&extractTurnQualitySegment, "conversation", "", "Alias for --segment")
	extractTurnQualityCmd.Flags().BoolVar(&extractTurnQualityDryRun, "dry-run", false, "Show what would be processed without enqueueing")
	extractTurnQualityCmd.Flags().IntVar(&extractTurnQualityLimit, "limit", 0, "Limit number of segments to process")
	extractTurnQualityCmd.Flags().StringVar(&extractTurnQualityDefinition, "definition", "ai_turn_pair", "Filter by segment definition name")

	// extract sync - sync facets to person_facts
	extractSyncCmd := &cobra.Command{
		Use:   "sync",
		Short: "Sync extracted facets to person_facts table",
		Long:  "Process completed PII extraction analysis runs and sync facets to person_facts",
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK                    bool   `json:"ok"`
				AnalysisRunsProcessed int    `json:"analysis_runs_processed"`
				FacetsProcessed       int    `json:"facets_processed"`
				FactsCreated          int    `json:"facts_created"`
				UnattributedCreated   int    `json:"unattributed_created"`
				ThirdPartiesCreated   int    `json:"third_parties_created"`
				Errors                int    `json:"errors"`
				Message               string `json:"message,omitempty"`
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			stats, err := identify.SyncFacetsToPersonFacts(database)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to sync facets: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{
				OK:                    true,
				AnalysisRunsProcessed: stats.AnalysisRunsProcessed,
				FacetsProcessed:       stats.FacetsProcessed,
				FactsCreated:          stats.FactsCreated,
				UnattributedCreated:   stats.UnattributedCreated,
				ThirdPartiesCreated:   stats.ThirdPartiesCreated,
				Errors:                stats.Errors,
			}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Printf("✓ Synced %d analysis runs:\n", stats.AnalysisRunsProcessed)
				fmt.Printf("  Facets processed: %d\n", stats.FacetsProcessed)
				fmt.Printf("  Facts created: %d\n", stats.FactsCreated)
				fmt.Printf("  Unattributed facts: %d\n", stats.UnattributedCreated)
				fmt.Printf("  Third parties created: %d\n", stats.ThirdPartiesCreated)
				if stats.Errors > 0 {
					fmt.Printf("  Errors: %d\n", stats.Errors)
				}
			}
		},
	}

	// extract status - show extraction status
	extractStatusCmd := &cobra.Command{
		Use:   "status",
		Short: "Show PII extraction status",
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK                 bool   `json:"ok"`
				TotalConversations int    `json:"total_segments"`
				Pending            int    `json:"pending"`
				Running            int    `json:"running"`
				Completed          int    `json:"completed"`
				Failed             int    `json:"failed"`
				Blocked            int    `json:"blocked"`
				Message            string `json:"message,omitempty"`
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			var totalConvs int
			database.QueryRow(`SELECT COUNT(*) FROM segments`).Scan(&totalConvs)

			var pending, running, completed, failed, blocked int
			database.QueryRow(`
				SELECT COUNT(*) FROM analysis_runs ar
				JOIN analysis_types at ON ar.analysis_type_id = at.id
				WHERE at.name = 'pii_extraction' AND ar.status = 'pending'
			`).Scan(&pending)
			database.QueryRow(`
				SELECT COUNT(*) FROM analysis_runs ar
				JOIN analysis_types at ON ar.analysis_type_id = at.id
				WHERE at.name = 'pii_extraction' AND ar.status = 'running'
			`).Scan(&running)
			database.QueryRow(`
				SELECT COUNT(*) FROM analysis_runs ar
				JOIN analysis_types at ON ar.analysis_type_id = at.id
				WHERE at.name = 'pii_extraction' AND ar.status = 'completed'
			`).Scan(&completed)
			database.QueryRow(`
				SELECT COUNT(*) FROM analysis_runs ar
				JOIN analysis_types at ON ar.analysis_type_id = at.id
				WHERE at.name = 'pii_extraction' AND ar.status = 'failed'
			`).Scan(&failed)
			database.QueryRow(`
				SELECT COUNT(*) FROM analysis_runs ar
				JOIN analysis_types at ON ar.analysis_type_id = at.id
				WHERE at.name = 'pii_extraction' AND ar.status = 'blocked'
			`).Scan(&blocked)

			result := Result{
				OK:                 true,
				TotalConversations: totalConvs,
				Pending:            pending,
				Running:            running,
				Completed:          completed,
				Failed:             failed,
				Blocked:            blocked,
			}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Println("PII Extraction Status:")
				fmt.Printf("  Total segments: %d\n", totalConvs)
				notStarted := totalConvs - pending - running - completed - failed - blocked
				fmt.Printf("  Not started: %d\n", notStarted)
				fmt.Printf("  Pending: %d\n", pending)
				fmt.Printf("  Running: %d\n", running)
				fmt.Printf("  Completed: %d\n", completed)
				fmt.Printf("  Failed: %d\n", failed)
				fmt.Printf("  Blocked: %d\n", blocked)
			}
		},
	}

	// extract aix-metadata - extract facets from AIX metadata
	var extractAIXChannel string
	var extractAIXSince string

	extractAIXMetadataCmd := &cobra.Command{
		Use:   "aix-metadata",
		Short: "Extract facets from AIX event metadata",
		Long: `Extract structured facets from AIX (Cursor) event metadata.

This extracts:
- File references (relevantFiles)
- Tool invocations (toolFormerData)
- Mode (agentic vs normal)
- Capabilities used

Examples:
  cortex extract aix-metadata --channel cursor
  cortex extract aix-metadata --since 7d`,
		Run: func(cmd *cobra.Command, args []string) {
			type Result struct {
				OK              bool   `json:"ok"`
				EventsProcessed int    `json:"events_processed"`
				EpisodesCreated int    `json:"episodes_created"`
				FacetsCreated   int    `json:"facets_created"`
				Duration        string `json:"duration"`
				Message         string `json:"message,omitempty"`
			}

			database, err := db.Open()
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Failed to open database: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}
			defer database.Close()

			// Parse since flag
			var sinceTS int64
			if extractAIXSince != "" {
				var sinceTime time.Time
				if strings.HasSuffix(extractAIXSince, "d") {
					var d int
					fmt.Sscanf(extractAIXSince, "%dd", &d)
					if d > 0 {
						sinceTime = time.Now().AddDate(0, 0, -d)
					}
				} else if strings.HasSuffix(extractAIXSince, "h") {
					var h int
					fmt.Sscanf(extractAIXSince, "%dh", &h)
					if h > 0 {
						sinceTime = time.Now().Add(-time.Duration(h) * time.Hour)
					}
				} else {
					sinceTime, _ = time.Parse("2006-01-02", extractAIXSince)
				}
				if !sinceTime.IsZero() {
					sinceTS = sinceTime.Unix()
				}
			}

			channel := extractAIXChannel
			if channel == "" {
				channel = "cursor"
			}

			extractor := adapters.NewAIXFacetExtractor(database)
			extractResult, err := extractor.ExtractFacetsFromMetadata(cmd.Context(), channel, sinceTS)
			if err != nil {
				result := Result{OK: false, Message: fmt.Sprintf("Extraction failed: %v", err)}
				if jsonOutput {
					printJSON(result)
				} else {
					fmt.Fprintf(os.Stderr, "Error: %s\n", result.Message)
				}
				os.Exit(1)
			}

			result := Result{
				OK:              true,
				EventsProcessed: extractResult.EventsProcessed,
				EpisodesCreated: extractResult.EpisodesCreated,
				FacetsCreated:   extractResult.FacetsCreated,
				Duration:        extractResult.Duration.String(),
			}

			if jsonOutput {
				printJSON(result)
			} else {
				fmt.Println("AIX Metadata Extraction Results:")
				fmt.Printf("  Events processed: %d\n", result.EventsProcessed)
				fmt.Printf("  Episodes created: %d\n", result.EpisodesCreated)
				fmt.Printf("  Facets created: %d\n", result.FacetsCreated)
				fmt.Printf("  Duration: %s\n", result.Duration)
			}
		},
	}
	extractAIXMetadataCmd.Flags().StringVar(&extractAIXChannel, "channel", "cursor", "Channel to extract from")
	extractAIXMetadataCmd.Flags().StringVar(&extractAIXSince, "since", "", "Only process events since (e.g., 30d, 7d)")

	extractCmd.AddCommand(extractPIICmd)
	extractCmd.AddCommand(extractNexusCmd)
	extractCmd.AddCommand(extractTerminalCmd)
	extractCmd.AddCommand(extractTurnQualityCmd)
	extractCmd.AddCommand(extractSyncCmd)
	extractCmd.AddCommand(extractStatusCmd)
	extractCmd.AddCommand(extractAIXMetadataCmd)
	rootCmd.AddCommand(extractCmd)

	if err := rootCmd.Execute(); err != nil {
		os.Exit(1)
	}
}

func printJSON(v interface{}) {
	enc := json.NewEncoder(os.Stdout)
	enc.SetIndent("", "  ")
	enc.Encode(v)
}

// parseDate parses a date string in YYYY-MM-DD format
func parseDate(dateStr string) (time.Time, error) {
	return time.Parse("2006-01-02", dateStr)
}

// checkAdapterStatus checks if an adapter's prerequisites are met
func checkAdapterStatus(name string, adapter config.AdapterConfig) string {
	switch adapter.Type {
	case "eve":
		// Check if Eve database exists
		home, err := os.UserHomeDir()
		if err != nil {
			return "error"
		}
		eveDBPath := filepath.Join(home, "Library", "Application Support", "Eve", "eve.db")
		if _, err := os.Stat(eveDBPath); os.IsNotExist(err) {
			return "missing Eve database"
		}
		return "ready"

	case "gogcli":
		// Check if account is configured
		if account, ok := adapter.Options["account"].(string); ok && account != "" {
			// TODO: Check if gogcli is installed and authenticated
			// For now, assume ready if account is configured
			return "ready (check gogcli auth)"
		}
		return "missing account"

	case "aix":
		home, err := os.UserHomeDir()
		if err != nil {
			return "error"
		}
		aixDBPath := filepath.Join(home, "Library", "Application Support", "aix", "aix.db")
		if _, err := os.Stat(aixDBPath); os.IsNotExist(err) {
			return "missing aix database (run: aix sync --all)"
		}
		if source, ok := adapter.Options["source"].(string); ok && source != "" {
			return "ready"
		}
		return "missing source"

	case "nexus":
		eventsDir := ""
		if v, ok := adapter.Options["events_dir"].(string); ok && v != "" {
			eventsDir = v
		} else if v, ok := adapter.Options["state_dir"].(string); ok && v != "" {
			eventsDir = filepath.Join(v, "events")
		} else {
			home, err := os.UserHomeDir()
			if err != nil {
				return "error"
			}
			eventsDir = filepath.Join(home, "nexus", "state", "events")
		}
		if _, err := os.Stat(eventsDir); os.IsNotExist(err) {
			return "missing nexus events dir"
		}
		return "ready"

	case "bird":
		// Check if bird CLI is available
		if _, err := exec.LookPath("bird"); err != nil {
			return "bird not installed (brew install steipete/tap/bird)"
		}
		return "ready"

	default:
		return "unknown adapter type"
	}
}

// blobToFloat64Slice converts embedding blob to float64 slice (little-endian)
func blobToFloat64Slice(blob []byte) []float64 {
	if len(blob)%8 != 0 {
		return nil
	}
	values := make([]float64, len(blob)/8)
	for i := 0; i < len(values); i++ {
		bits := uint64(0)
		for j := 0; j < 8; j++ {
			bits |= uint64(blob[i*8+j]) << (j * 8)
		}
		values[i] = math.Float64frombits(bits)
	}
	return values
}

// cosineSimilarity calculates cosine similarity between two vectors
func cosineSimilarity(a, b []float64) float64 {
	if len(a) != len(b) || len(a) == 0 {
		return 0
	}

	var dotProduct, normA, normB float64
	for i := range a {
		dotProduct += a[i] * b[i]
		normA += a[i] * a[i]
		normB += b[i] * b[i]
	}

	if normA == 0 || normB == 0 {
		return 0
	}

	return dotProduct / (math.Sqrt(normA) * math.Sqrt(normB))
}

// getEpisodePreview returns a text preview of an episode
func getEpisodePreview(ctx context.Context, database *sql.DB, episodeID string, maxLen int) (string, error) {
	rows, err := database.QueryContext(ctx, `
		SELECT e.content, p.canonical_name
		FROM episode_events ee
		JOIN events e ON ee.event_id = e.id
		LEFT JOIN event_participants ep ON e.id = ep.event_id AND ep.role = 'sender'
		LEFT JOIN persons p ON ep.person_id = p.id
		WHERE ee.episode_id = ?
		ORDER BY ee.position
		LIMIT 5
	`, episodeID)
	if err != nil {
		return "", err
	}
	defer rows.Close()

	var parts []string
	for rows.Next() {
		var content, name sql.NullString
		if err := rows.Scan(&content, &name); err != nil {
			continue
		}
		if content.Valid && content.String != "" {
			msg := content.String
			if name.Valid && name.String != "" {
				msg = name.String + ": " + msg
			}
			parts = append(parts, msg)
		}
	}

	preview := strings.Join(parts, " | ")
	if len(preview) > maxLen {
		preview = preview[:maxLen-3] + "..."
	}
	return preview, nil
}
