# Makefile for OpenShift Cluster Health MCP Server
# Implements Phase 0.3 build targets

.PHONY: help build test lint clean docker-build docker-build-debug docker-push run

# Variables
BINARY_NAME=mcp-server
VERSION?=0.1.0
IMAGE_REGISTRY?=quay.io
IMAGE_ORG?=openshift-aiops
IMAGE_NAME=$(IMAGE_REGISTRY)/$(IMAGE_ORG)/cluster-health-mcp
GOPATH?=$(shell go env GOPATH)
GOCMD=go
GOBUILD=$(GOCMD) build
GOTEST=$(GOCMD) test
GOCLEAN=$(GOCMD) clean
GOGET=$(GOCMD) get

# Default target
help:
	@echo "OpenShift Cluster Health MCP Server - Build Targets"
	@echo "===================================================="
	@echo ""
	@echo "Development:"
	@echo "  make build          - Build binary locally"
	@echo "  make test           - Run unit tests"
	@echo "  make test-coverage  - Run tests with coverage report"
	@echo "  make lint           - Run linters (golangci-lint)"
	@echo "  make run            - Run server locally"
	@echo "  make clean          - Clean build artifacts"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build        - Build production container image"
	@echo "  make docker-build-debug  - Build debug container image"
	@echo "  make docker-push         - Push image to registry"
	@echo "  make docker-run          - Run container locally"
	@echo ""
	@echo "Deployment:"
	@echo "  make helm-lint      - Lint Helm chart"
	@echo "  make helm-install   - Install to cluster"
	@echo "  make helm-upgrade   - Upgrade deployment"
	@echo ""
	@echo "Variables:"
	@echo "  VERSION=$(VERSION)"
	@echo "  IMAGE_NAME=$(IMAGE_NAME)"

# Build binary locally
build:
	@echo "Building $(BINARY_NAME)..."
	mkdir -p bin
	$(GOBUILD) -o bin/$(BINARY_NAME) ./cmd/mcp-server
	@echo "Binary built: bin/$(BINARY_NAME)"

# Build with optimizations (production build)
build-prod:
	@echo "Building $(BINARY_NAME) with optimizations..."
	mkdir -p bin
	CGO_ENABLED=0 $(GOBUILD) \
		-ldflags="-s -w -X main.Version=$(VERSION)" \
		-trimpath \
		-o bin/$(BINARY_NAME) \
		./cmd/mcp-server
	@echo "Production binary built: bin/$(BINARY_NAME)"
	@ls -lh bin/$(BINARY_NAME)

# Run tests
test:
	@echo "Running tests..."
	$(GOTEST) -v ./...

# Run tests with coverage
test-coverage:
	@echo "Running tests with coverage..."
	mkdir -p coverage
	$(GOTEST) -v -coverprofile=coverage/coverage.out ./...
	$(GOCMD) tool cover -html=coverage/coverage.out -o coverage/coverage.html
	@echo "Coverage report: coverage/coverage.html"

# Lint code (requires golangci-lint)
lint:
	@echo "Running linters..."
	@which golangci-lint > /dev/null || (echo "golangci-lint not found. Install: curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(GOPATH)/bin"; exit 1)
	golangci-lint run ./...

# Run server locally
run:
	@echo "Running MCP server (stdio transport)..."
	$(GOCMD) run ./cmd/mcp-server

# Clean build artifacts
clean:
	@echo "Cleaning..."
	$(GOCLEAN)
	rm -rf bin/
	rm -rf coverage/
	@echo "Clean complete"

# Docker: Build production image
docker-build:
	@echo "Building Docker image $(IMAGE_NAME):$(VERSION)..."
	docker build \
		-t $(IMAGE_NAME):$(VERSION) \
		-t $(IMAGE_NAME):latest \
		-f Dockerfile \
		.
	@echo "Docker image built: $(IMAGE_NAME):$(VERSION)"
	@docker images $(IMAGE_NAME)

# Docker: Build debug image
docker-build-debug:
	@echo "Building debug Docker image..."
	docker build \
		-t $(IMAGE_NAME):$(VERSION)-debug \
		-f Dockerfile.debug \
		.
	@echo "Debug image built: $(IMAGE_NAME):$(VERSION)-debug"

# Docker: Push to registry
docker-push:
	@echo "Pushing $(IMAGE_NAME):$(VERSION) to registry..."
	docker push $(IMAGE_NAME):$(VERSION)
	docker push $(IMAGE_NAME):latest
	@echo "Image pushed successfully"

# Docker: Run container locally
docker-run:
	@echo "Running container locally..."
	docker run --rm -it \
		-e MCP_TRANSPORT=stdio \
		-v $(HOME)/.kube:/home/nonroot/.kube:ro \
		$(IMAGE_NAME):$(VERSION)

# Docker: Multi-arch build (amd64, arm64)
docker-buildx:
	@echo "Building multi-arch image..."
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		-t $(IMAGE_NAME):$(VERSION) \
		-t $(IMAGE_NAME):latest \
		--push \
		.

# Helm: Lint chart
helm-lint:
	@echo "Linting Helm chart..."
	helm lint charts/openshift-cluster-health-mcp

# Helm: Install to cluster
helm-install:
	@echo "Installing Helm chart..."
	helm install cluster-health-mcp ./charts/openshift-cluster-health-mcp \
		--namespace cluster-health-mcp-dev \
		--create-namespace \
		--set image.tag=$(VERSION)

# Helm: Upgrade deployment
helm-upgrade:
	@echo "Upgrading Helm release..."
	helm upgrade cluster-health-mcp ./charts/openshift-cluster-health-mcp \
		--namespace cluster-health-mcp-dev \
		--set image.tag=$(VERSION)

# Helm: Uninstall
helm-uninstall:
	@echo "Uninstalling Helm release..."
	helm uninstall cluster-health-mcp --namespace cluster-health-mcp-dev

# Development: Watch and rebuild on changes (requires entr)
watch:
	@echo "Watching for changes..."
	@which entr > /dev/null || (echo "entr not found. Install: dnf install entr"; exit 1)
	find . -name '*.go' | entr -r make build

# Generate Go modules
mod-download:
	@echo "Downloading Go modules..."
	$(GOCMD) mod download

mod-tidy:
	@echo "Tidying Go modules..."
	$(GOCMD) mod tidy

mod-vendor:
	@echo "Vendoring dependencies..."
	$(GOCMD) mod vendor

# Security: Scan for vulnerabilities
security-scan:
	@echo "Scanning for vulnerabilities..."
	@which trivy > /dev/null || (echo "trivy not found. Install from: https://github.com/aquasecurity/trivy"; exit 1)
	trivy image $(IMAGE_NAME):$(VERSION)

# Security: Run gosec
security-gosec:
	@echo "Running gosec security scanner..."
	@which gosec > /dev/null || (go install github.com/securego/gosec/v2/cmd/gosec@latest)
	gosec ./...
