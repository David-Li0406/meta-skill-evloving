package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"strings"
)

// ValidationResult represents the result of validating a single file
type ValidationResult struct {
	FilePath string
	Valid    bool
	Error    string
}

// ValidationSummary contains summary statistics
type ValidationSummary struct {
	Directory      string
	TotalFiles     int
	ValidFiles     int
	InvalidFiles   int
	InvalidDetails []ValidationResult
}

func main() {
	dir := flag.String("dir", "", "Directory to scan for JSON files")
	noRecursive := flag.Bool("no-recursive", false, "Scan only top-level directory")
	flag.Parse()

	if *dir == "" {
		fmt.Println("Usage: go run validate_json.go -dir <directory> [-no-recursive]")
		fmt.Println("\nOptions:")
		fmt.Println("  -dir           Path to directory to scan for JSON files")
		fmt.Println("  -no-recursive  Scan only the top-level directory (default: recursive)")
		os.Exit(1)
	}

	fmt.Printf("Validating JSON files in: %s\n", *dir)
	if *noRecursive {
		fmt.Println("(top-level only)")
	} else {
		fmt.Println("(recursive scan)")
	}
	fmt.Println()

	summary := validateJSONFiles(*dir, !*noRecursive)
	printSummary(summary)

	if summary.InvalidFiles > 0 {
		os.Exit(1)
	}
}

// validateJSONFiles validates all JSON files in the specified directory
func validateJSONFiles(directory string, recursive bool) ValidationSummary {
	summary := ValidationSummary{
		Directory: directory,
	}

	var jsonFiles []string
	var err error

	if recursive {
		jsonFiles, err = findJSONFilesRecursive(directory)
	} else {
		jsonFiles, err = findJSONFiles(directory)
	}

	if err != nil {
		fmt.Printf("Error scanning directory: %v\n", err)
		return summary
	}

	summary.TotalFiles = len(jsonFiles)

	for _, filePath := range jsonFiles {
		result := validateJSONFile(filePath)
		if result.Valid {
			summary.ValidFiles++
			fmt.Printf("✓ %s\n", filePath)
		} else {
			summary.InvalidFiles++
			summary.InvalidDetails = append(summary.InvalidDetails, result)
			fmt.Printf("✗ %s\n", filePath)
			fmt.Printf("  Error: %s\n", result.Error)
		}
	}

	return summary
}

// findJSONFilesRecursive finds all JSON files in directory and subdirectories
func findJSONFilesRecursive(root string) ([]string, error) {
	var jsonFiles []string

	err := filepath.WalkDir(root, func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}

		if !d.IsDir() && strings.HasSuffix(strings.ToLower(path), ".json") {
			jsonFiles = append(jsonFiles, path)
		}

		return nil
	})

	return jsonFiles, err
}

// findJSONFiles finds JSON files only in the top-level directory
func findJSONFiles(directory string) ([]string, error) {
	entries, err := os.ReadDir(directory)
	if err != nil {
		return nil, err
	}

	var jsonFiles []string
	for _, entry := range entries {
		if !entry.IsDir() && strings.HasSuffix(strings.ToLower(entry.Name()), ".json") {
			jsonFiles = append(jsonFiles, filepath.Join(directory, entry.Name()))
		}
	}

	return jsonFiles, nil
}

// validateJSONFile validates a single JSON file
func validateJSONFile(filePath string) ValidationResult {
	result := ValidationResult{
		FilePath: filePath,
		Valid:    true,
	}

	data, err := os.ReadFile(filePath)
	if err != nil {
		result.Valid = false
		result.Error = fmt.Sprintf("Error reading file: %v", err)
		return result
	}

	var v interface{}
	if err := json.Unmarshal(data, &v); err != nil {
		result.Valid = false
		result.Error = fmt.Sprintf("JSON decode error: %v", err)
		return result
	}

	return result
}

// printSummary prints the validation summary
func printSummary(summary ValidationSummary) {
	fmt.Println()
	fmt.Println("============================================================")
	fmt.Println("VALIDATION SUMMARY")
	fmt.Println("============================================================")
	fmt.Printf("Directory: %s\n", summary.Directory)
	fmt.Printf("Total JSON files: %d\n", summary.TotalFiles)
	fmt.Printf("Valid files: %d\n", summary.ValidFiles)
	fmt.Printf("Invalid files: %d\n", summary.InvalidFiles)

	if summary.InvalidFiles > 0 {
		fmt.Println()
		fmt.Println("Invalid files:")
		for _, detail := range summary.InvalidDetails {
			fmt.Printf("  - %s\n", detail.FilePath)
			fmt.Printf("    %s\n", detail.Error)
		}
	}

	fmt.Println("============================================================")
}
