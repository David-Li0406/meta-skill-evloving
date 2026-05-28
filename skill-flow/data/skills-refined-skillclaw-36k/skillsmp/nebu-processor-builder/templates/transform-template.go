// Package main provides a standalone CLI for the {NAME} processor.
//
// {DESCRIPTION}
package main

import (
	"github.com/spf13/cobra"
	"github.com/withObsrvr/nebu/pkg/processor/cli"
)

var version = "0.1.0"

// Custom flags for this processor
var (
	// TODO: Add processor-specific flags here
	// Example:
	// minAmount int64
	// assetCode string
)

func main() {
	config := cli.TransformConfig{
		Name:        "{NAME}",
		Description: "{DESCRIPTION}",
		Version:     version,
	}

	cli.RunTransformCLI(config, transformEvent, addFlags)
}

// transformEvent processes a single event
// Returns:
//   - (nil, nil) to filter out the event
//   - (event, nil) to pass through (modified or unmodified)
//   - (nil, error) to stop the pipeline with an error
func transformEvent(event map[string]interface{}) (map[string]interface{}, error) {
	// TODO: Implement your transform logic here

	// Example: Filter by field value
	// if value, ok := event["field"].(string); ok {
	//     if value != "expected" {
	//         return nil, nil // Filter out
	//     }
	// }

	// Example: Enrich event
	// event["enriched_field"] = "value"

	return event, nil
}

// addFlags adds custom flags to the command
func addFlags(cmd *cobra.Command) {
	// TODO: Add your flags here
	// Example:
	// cmd.Flags().Int64Var(&minAmount, "min", 0, "Minimum amount threshold")
	// cmd.Flags().StringVar(&assetCode, "asset", "", "Filter by asset code")
}
