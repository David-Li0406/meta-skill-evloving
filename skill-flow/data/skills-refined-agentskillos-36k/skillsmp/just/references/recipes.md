# Just Recipe Reference

## Basic Recipe

```just
# Comment appears in `just --list`
recipe-name:
    command1
    command2
```

## Parameters

```just
# Required parameter
build target:
    echo "Building {{target}}"

# Default value
test target="all":
    echo "Testing {{target}}"

# Variadic: one or more (+) or zero or more (*)
deploy +servers:
    echo "Deploying to {{servers}}"

backup *files:
    echo "Backing up {{files}}"

# Export as env var
run $PORT:
    ./server --port $PORT
```

## Dependencies

```just
# Prior dependencies (run before)
build: clean compile
    echo "Built"

# With arguments
release: (build "prod")
    echo "Released"

# Subsequent dependencies (run after)
all: build && test deploy
    echo "All done"
```

Dependencies run once per invocation regardless of how many times referenced.

## Shebang Recipes

Execute as script in any language:

```just
# Python
analyze:
    #!/usr/bin/env python3
    import json
    print(json.dumps({"status": "ok"}))

# Node.js
generate:
    #!/usr/bin/env node
    console.log("Generated");

# Bash with options
setup:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Setting up..."
```

## Aliases

```just
alias b := build
alias t := test
alias d := deploy
```

## Conditionals in Recipes

```just
greet name:
    {{ if name == "world" { "echo Hello, World!" } else { "echo Hello, " + name } }}
```
