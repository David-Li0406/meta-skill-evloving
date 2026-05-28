NAME := aix
VERSION := $(shell git describe --tags --always --dirty 2>/dev/null || echo "dev")
COMMIT := $(shell git rev-parse --short HEAD 2>/dev/null || echo "none")
DATE := $(shell date -u +%Y-%m-%dT%H:%M:%SZ)
LDFLAGS := -ldflags "-X main.version=$(VERSION) -X main.commit=$(COMMIT) -X main.buildDate=$(DATE)"

.PHONY: build install clean test

build:
	go build $(LDFLAGS) -o $(NAME) ./cmd/$(NAME)

install: build
	cp $(NAME) ~/bin/

clean:
	rm -f $(NAME)

test:
	go test ./...
