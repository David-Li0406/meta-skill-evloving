package main

import (
	"os"

	"github.com/Dicklesworthstone/ntm/internal/cli"
)

func main() {
	if err := cli.Execute(); err != nil {
		os.Exit(1)
	}
}
