# Self-Evolving Agent Makefile
# ===========================
# Unified command interface for development and usage
#
# Usage:
#   make help       - Show available commands
#   make validate   - Run all validations
#   make test       - Run test suite
#   make install    - Install to target project

.PHONY: help validate test install clean release lint check-env quick-test changelog changelog-save changelog-since recent memory-stats memory-recent verify-memory memory-sync deps-check pre-commit setup-file-suggestion

# Default target
.DEFAULT_GOAL := help

# Colors for output
CYAN := \033[0;36m
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m
BOLD := \033[1m

# Project info
VERSION := $(shell grep "^version:" skills/SKILL.md | head -1 | awk '{print $$2}')
PROJECT := self-evolving-agent

#==============================================================================
# Help
#==============================================================================

help: ## Show this help message
	@echo ""
	@echo "$(CYAN)╔══════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(CYAN)║$(NC)  $(BOLD)Self-Evolving Agent$(NC) - Make Commands                        $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)  Version: $(YELLOW)$(VERSION)$(NC)                                              $(CYAN)║$(NC)"
	@echo "$(CYAN)╚══════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(BOLD)Usage:$(NC) make $(CYAN)<command>$(NC)"
	@echo ""
	@echo "$(BOLD)Commands:$(NC)"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ { printf "  $(CYAN)%-15s$(NC) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""

#==============================================================================
# Validation & Testing
#==============================================================================

validate: ## Run all validation checks
	@echo "$(BOLD)Running full validation...$(NC)"
	@./scripts/validate-all.sh

check-env: ## Check environment setup
	@./scripts/check-env.sh

test: ## Run full test suite
	@echo "$(BOLD)Running test suite...$(NC)"
	@./tests/run_tests.sh

quick-test: ## Run quick validation tests only
	@echo "$(BOLD)Running quick tests...$(NC)"
	@./tests/run_tests.sh --quick

lint: ## Check markdown files for issues
	@echo "$(BOLD)Checking markdown files...$(NC)"
	@echo "Checking for markdown files with links..."
	@find skills -name "*.md" -type f | head -5
	@echo "$(GREEN)Lint check complete$(NC)"

#==============================================================================
# Installation
#==============================================================================

install: ## Install to a target project (use: make install TARGET=/path)
	@if [ -z "$(TARGET)" ]; then \
		echo "$(RED)Error: TARGET not specified$(NC)"; \
		echo "Usage: make install TARGET=/path/to/project"; \
		exit 1; \
	fi
	@echo "$(BOLD)Installing to $(TARGET)...$(NC)"
	@./scripts/quickstart.sh "$(TARGET)"

install-global: ## Install globally to ~/.claude/skills/
	@echo "$(BOLD)Installing globally...$(NC)"
	@./install.sh --global

install-local: ## Install to current directory
	@echo "$(BOLD)Installing to current project...$(NC)"
	@./scripts/quickstart.sh .

setup-file-suggestion: ## Setup file-suggestion for large codebase optimization
	@echo "$(BOLD)Setting up file-suggestion script...$(NC)"
	@mkdir -p ~/.claude
	@./scripts/setup-file-suggestion.sh
	@echo ""
	@echo "$(GREEN)✅ file-suggestion.sh installed to ~/.claude/$(NC)"
	@echo ""
	@echo "$(YELLOW)Next step: Add this to your ~/.claude/settings.json:$(NC)"
	@echo '  {'
	@echo '    "fileSuggestion": {'
	@echo '      "type": "command",'
	@echo '      "command": "~/.claude/file-suggestion.sh"'
	@echo '    }'
	@echo '  }'
	@echo ""

#==============================================================================
# Development
#==============================================================================

sync: ## Sync skill to global location
	@echo "$(BOLD)Syncing to global...$(NC)"
	@./scripts/sync-global.sh

verify-memory: ## Validate memory system
	@./scripts/validate-memory.sh

memory-stats: ## Show memory system statistics
	@echo "$(BOLD)Memory System Statistics:$(NC)"
	@echo ""
	@echo "  $(CYAN)Learnings:$(NC)    $$(find .claude/memory/learnings -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
	@echo "  $(CYAN)Failures:$(NC)     $$(find .claude/memory/failures -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
	@echo "  $(CYAN)Decisions:$(NC)    $$(find .claude/memory/decisions -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
	@echo "  $(CYAN)Patterns:$(NC)     $$(find .claude/memory/patterns -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
	@echo "  $(CYAN)Discoveries:$(NC)  $$(find .claude/memory/discoveries -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
	@echo "  $(CYAN)Strategies:$(NC)   $$(find .claude/memory/strategies -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
	@echo ""
	@echo "$(BOLD)Index Status:$(NC)"
	@if [ -f ".claude/memory/index.md" ]; then \
		echo "  Last updated: $$(stat -f '%Sm' .claude/memory/index.md 2>/dev/null || stat -c '%y' .claude/memory/index.md 2>/dev/null | cut -d' ' -f1)"; \
		echo "  Total index entries: $$(grep -c '^\- \[' .claude/memory/index.md 2>/dev/null || echo 0)"; \
	else \
		echo "  $(RED)index.md not found!$(NC)"; \
	fi
	@echo ""

memory-recent: ## Show recently modified memory files
	@echo "$(BOLD)Recently Modified Memory Files:$(NC)"
	@find .claude/memory -name "*.md" -type f -mtime -7 2>/dev/null | while read f; do \
		echo "  $$(stat -f '%Sm' "$$f" 2>/dev/null || stat -c '%y' "$$f" 2>/dev/null | cut -d' ' -f1-2)  $$f"; \
	done | sort -r | head -10
	@echo ""

verify-install: ## Verify skill installation
	@./scripts/verify-install.sh

memory-sync: ## Sync index.md with actual memory files
	@echo "$(BOLD)Syncing memory index...$(NC)"
	@echo ""
	@orphans=$$(./scripts/validate-memory.sh 2>&1 | grep "Orphan:" | wc -l | tr -d ' '); \
	if [ "$$orphans" -gt 0 ]; then \
		echo "$(YELLOW)Found $$orphans orphan files. Adding to index.md...$(NC)"; \
		for dir in learnings failures decisions patterns strategies discoveries; do \
			for file in .claude/memory/$$dir/*.md; do \
				[ ! -f "$$file" ] && continue; \
				filename=$$(basename "$$file"); \
				relative="$$dir/$$filename"; \
				if ! grep -q "$$relative" .claude/memory/index.md 2>/dev/null; then \
					title=$$(grep "^# " "$$file" | head -1 | sed 's/^# //'); \
					[ -z "$$title" ] && title="$$filename"; \
					section=$$(echo "$$dir" | tr '[:lower:]' '[:upper:]'); \
					echo "  Adding: $$relative"; \
				fi; \
			done; \
		done; \
		echo "$(GREEN)✅ Please manually update index.md with the orphan files above$(NC)"; \
	else \
		echo "$(GREEN)✅ Memory index is in sync$(NC)"; \
	fi

deps-check: ## Check required dependencies
	@echo "$(BOLD)Checking dependencies...$(NC)"
	@echo ""
	@missing=0; \
	for cmd in git bash grep find; do \
		if command -v $$cmd >/dev/null 2>&1; then \
			echo "  $(GREEN)✅$(NC) $$cmd: $$($$cmd --version 2>&1 | head -1)"; \
		else \
			echo "  $(RED)❌$(NC) $$cmd: not found"; \
			missing=$$((missing + 1)); \
		fi; \
	done; \
	echo ""; \
	if [ $$missing -gt 0 ]; then \
		echo "$(RED)Missing $$missing required dependencies$(NC)"; \
		exit 1; \
	else \
		echo "$(GREEN)All dependencies satisfied$(NC)"; \
	fi

pre-commit: lint verify-memory ## Quick pre-commit check (lint + memory)
	@echo ""
	@echo "$(GREEN)✅ Pre-commit checks passed$(NC)"

#==============================================================================
# Release
#==============================================================================

release: validate test ## Prepare for release (validate + test)
	@echo ""
	@echo "$(GREEN)╔══════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(GREEN)║$(NC)  $(BOLD)Ready for Release!$(NC)                                         $(GREEN)║$(NC)"
	@echo "$(GREEN)║$(NC)  Version: $(YELLOW)$(VERSION)$(NC)                                              $(GREEN)║$(NC)"
	@echo "$(GREEN)╚══════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Update CHANGELOG.md if needed"
	@echo "  2. Commit changes: git commit -am 'chore: prepare release $(VERSION)'"
	@echo "  3. Create tag: git tag v$(VERSION)"
	@echo "  4. Push: git push && git push --tags"
	@echo ""

changelog: ## Generate CHANGELOG.md (preview mode)
	@echo "$(BOLD)Generating CHANGELOG preview...$(NC)"
	@./scripts/generate-changelog.sh --preview

changelog-save: ## Generate and save CHANGELOG.md
	@echo "$(BOLD)Generating CHANGELOG.md...$(NC)"
	@./scripts/generate-changelog.sh --all --output CHANGELOG.md
	@echo "$(GREEN)CHANGELOG.md updated!$(NC)"

changelog-since: ## Generate changelog since a tag (use: make changelog-since TAG=v4.1.0)
	@if [ -z "$(TAG)" ]; then \
		echo "$(RED)Error: TAG not specified$(NC)"; \
		echo "Usage: make changelog-since TAG=v4.1.0"; \
		exit 1; \
	fi
	@echo "$(BOLD)Generating changelog since $(TAG)...$(NC)"
	@./scripts/generate-changelog.sh --since $(TAG) --preview

recent: ## Show recent commits (quick view)
	@echo "$(BOLD)Recent commits:$(NC)"
	@git log --oneline -10

version: ## Show current version
	@echo "$(PROJECT) version $(VERSION)"

#==============================================================================
# Cleanup
#==============================================================================

clean: ## Clean temporary files
	@echo "$(BOLD)Cleaning up...$(NC)"
	@find . -name ".DS_Store" -delete 2>/dev/null || true
	@find . -name "*.bak" -delete 2>/dev/null || true
	@echo "$(GREEN)Clean complete$(NC)"

#==============================================================================
# Documentation
#==============================================================================

docs: ## Open documentation
	@echo "$(BOLD)Documentation:$(NC)"
	@echo ""
	@echo "  Main:          skills/SKILL.md"
	@echo "  Modules:       skills/*/README.md"
	@echo "  Usage:         USAGE.md"
	@echo "  Troubleshoot:  docs/TROUBLESHOOTING.md"
	@echo ""
	@echo "Quick links:"
	@echo "  - Getting Started: skills/00-getting-started/"
	@echo "  - Core Flow:       skills/01-core/"
	@echo "  - Checkpoints:     skills/02-checkpoints/"
	@echo "  - Memory System:   skills/03-memory/"
	@echo "  - Emergence:       skills/04-emergence/"
	@echo "  - Integration:     skills/05-integration/"
	@echo "  - Scaling:         skills/06-scaling/"
	@echo ""

stats: ## Show project statistics
	@echo "$(BOLD)Project Statistics:$(NC)"
	@echo ""
	@echo "  Skill Files:    $$(find skills -name '*.md' -type f | wc -l | tr -d ' ')"
	@echo "  Total Lines:    $$(find skills -name '*.md' -type f -exec cat {} \; | wc -l | tr -d ' ')"
	@echo "  Modules:        $$(ls -d skills/*/ | wc -l | tr -d ' ')"
	@echo "  Scripts:        $$(find scripts -name '*.sh' | wc -l | tr -d ' ')"
	@echo "  Memory Files:   $$(find .claude/memory -name '*.md' -type f | wc -l | tr -d ' ')"
	@echo ""
	@echo "$(BOLD)Module Breakdown:$(NC)"
	@for dir in skills/*/; do \
		if [ -d "$$dir" ]; then \
			lines=$$(find "$$dir" -name "*.md" -type f -exec cat {} \; | wc -l | tr -d ' '); \
			printf "  %-25s %s lines\n" "$$(basename $$dir):" "$$lines"; \
		fi \
	done
