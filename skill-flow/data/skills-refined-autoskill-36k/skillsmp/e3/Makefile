# e3 - East Execution Engine
# Top-level Makefile for building all components

.PHONY: all build test clean install dev help lint link unlink fuzz fuzz-quick fuzz-stress fuzz-build set-east-version

# Default target
all: build

help:
	@echo "e3 - East Execution Engine"
	@echo ""
	@echo "Available targets:"
	@echo "  make build          - Build all packages"
	@echo "  make test           - Run all tests"
	@echo "  make lint           - Run linters"
	@echo "  make install        - Install all dependencies"
	@echo "  make clean          - Clean all build artifacts"
	@echo "  make dev            - Install dependencies and build for development"
	@echo "  make link           - Link e3 CLI to PATH (makes 'e3' command available)"
	@echo "  make unlink         - Unlink e3 CLI from PATH"
	@echo "  make fuzz           - Run fuzz tests (100 iterations)"
	@echo "  make fuzz-quick     - Run quick fuzz tests (1 iteration, all scenarios)"
	@echo "  make fuzz-stress    - Run stress fuzz tests (1000 iterations)"

# Install all dependencies (using npm workspaces)
install:
	@echo "Installing dependencies via npm workspaces..."
	npm install

# Build all packages (in dependency order)
build:
	@echo "Building all packages..."
	npm run build --workspace=packages/e3-types
	npm run build --workspace=packages/e3
	npm run build --workspace=packages/e3-core
	npm run build --workspace=packages/e3-api-client
	npm run build --workspace=packages/e3-cli
	npm run build --workspace=packages/e3-api-server
	npm run build --workspace=packages/e3-api-tests
	npm run build --workspace=test/integration
	npm run build --workspace=test/fuzz

# Run all tests
test:
	@echo "Running tests..."
	npm run test

# Run all linters
lint:
	@echo "Linting all packages..."
	npm run lint

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf node_modules/ package-lock.json
	rm -rf packages/*/dist/
	rm -rf packages/*/node_modules/
	rm -rf test/*/dist/
	rm -rf test/*/node_modules/
	@echo "Clean complete"

# Development setup
dev: install build
	@echo ""
	@echo "Development environment ready!"
	@echo ""
	@echo "To run the CLI:"
	@echo "  cd packages/e3-cli && npm run dev"
	@echo ""
	@echo "To make 'e3' available globally:"
	@echo "  make link"

# Link CLI to PATH
link: build
	@echo "Linking e3 CLI to PATH..."
	chmod +x packages/e3-cli/dist/src/cli.js
	cd packages/e3-cli && npm link --force
	@echo ""
	@echo "✓ e3 CLI is now available globally"
	@echo "  Run 'e3 --help' to verify"

# Unlink CLI from PATH
unlink:
	@echo "Unlinking e3 CLI from PATH..."
	cd packages/e3-cli && npm unlink -g @elaraai/e3-cli || true
	@echo "✓ e3 CLI has been unlinked"

# Build fuzz tests
fuzz-build:
	@echo "Building fuzz tests..."
	npm run build --workspace=e3-fuzz

# Run fuzz tests (100 iterations)
fuzz: fuzz-build
	@echo "Running fuzz tests..."
	npm run fuzz --workspace=e3-fuzz

# Run quick fuzz tests (10 iterations)
fuzz-quick: fuzz-build
	@echo "Running quick fuzz tests..."
	npm run fuzz:quick --workspace=e3-fuzz

# Run stress fuzz tests (1000 iterations)
fuzz-stress: fuzz-build
	@echo "Running stress fuzz tests..."
	npm run fuzz:stress --workspace=e3-fuzz


# Update @elaraai/east version across all packages
# Usage: make set-east-version VERSION=0.0.1-beta.1
set-east-version:
ifndef VERSION
	$(error VERSION is required. Usage: make set-east-version VERSION=0.0.1-beta.1)
endif
	@echo "Updating @elaraai/east to version $(VERSION)..."
	@find . -name "package.json" -exec sed -i 's/"@elaraai\/east": "[^"]*"/"@elaraai\/east": "^$(VERSION)"/g' {} \;
	@echo "Done. Run 'npm install' to update dependencies."

# Update @elaraai/east-node-std version across all packages
# Usage: make set-east-node-std-version VERSION=0.0.1-beta.1
set-east-node-std-version:
ifndef VERSION
	$(error VERSION is required. Usage: make set-east-node-std-version VERSION=0.0.1-beta.1)
endif
	@echo "Updating @elaraai/east-node-std to version $(VERSION)..."
	@find . -name "package.json" -exec sed -i 's/"@elaraai\/east-node-std": "[^"]*"/"@elaraai\/east-node-std": "^$(VERSION)"/g' {} \;
	@echo "Done. Run 'npm install' to update dependencies."
