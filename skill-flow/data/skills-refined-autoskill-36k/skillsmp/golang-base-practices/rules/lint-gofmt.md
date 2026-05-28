---
title: Code Formatting
impact: MEDIUM
impactDescription: Consistent code style
tags: lint, gofmt, goimports
---

## Code Formatting

Use gofmt and goimports to maintain consistent code style.

**gofmt - Standard Formatting:**

```bash
# Format single file
gofmt -w file.go

# Format entire project
gofmt -w .

# Check without modifying (for CI)
gofmt -d . | grep -q . && echo "Formatting needed" && exit 1
```

**goimports - Formatting + Import Organization:**

```bash
# Install
go install golang.org/x/tools/cmd/goimports@latest

# Format and organize imports
goimports -w .

# Specify local package prefix (for import grouping)
goimports -w -local mycompany.com/myproject .
```

**Import Grouping Convention:**

```go
import (
    // Standard library
    "context"
    "fmt"
    "net/http"

    // Third-party libraries
    "github.com/gin-gonic/gin"
    "gorm.io/gorm"

    // Local packages
    "mycompany.com/myproject/internal/domain"
    "mycompany.com/myproject/pkg/errors"
)
```

**IDE/Editor Configuration:**

VS Code settings.json:
```json
{
    "go.formatTool": "goimports",
    "editor.formatOnSave": true,
    "[go]": {
        "editor.defaultFormatter": "golang.go"
    }
}
```

**Git hooks (pre-commit):**

```bash
#!/bin/sh
# .git/hooks/pre-commit

STAGED_GO_FILES=$(git diff --cached --name-only | grep ".go$")
if [ -z "$STAGED_GO_FILES" ]; then
    exit 0
fi

UNFMT=$(gofmt -l $STAGED_GO_FILES)
if [ -n "$UNFMT" ]; then
    echo "The following files need formatting:"
    echo "$UNFMT"
    exit 1
fi
```
