# Pandoc Makefile Template
# Copy this to your project directory and customize

# Configuration
PANDOC = pandoc
PYTHON = python3
PLUGIN_DIR = ~/.claude/marketplaces/cadrianmae-claude-marketplace/plugins/pandoc
VALIDATE = $(PYTHON) $(PLUGIN_DIR)/skills/pandoc/scripts/validate.py

# Project files
MAIN_DOC = document.md
OUTPUT_PDF = document.pdf
OUTPUT_HTML = document.html
OUTPUT_DOCX = document.docx

# Pandoc options
PDF_ENGINE = pdflatex
PANDOC_OPTS = --number-sections
CITE_OPTS = --citeproc

# Default target
all: pdf

# PDF output
pdf: $(OUTPUT_PDF)

$(OUTPUT_PDF): $(MAIN_DOC)
	@echo "Validating $(MAIN_DOC)..."
	@$(VALIDATE) $(MAIN_DOC)
	@echo "Converting to PDF..."
	$(PANDOC) $(MAIN_DOC) -o $(OUTPUT_PDF) \
		--pdf-engine=$(PDF_ENGINE) \
		$(PANDOC_OPTS) \
		$(CITE_OPTS)
	@echo "✅ Created: $(OUTPUT_PDF)"

# HTML output
html: $(OUTPUT_HTML)

$(OUTPUT_HTML): $(MAIN_DOC)
	@echo "Validating $(MAIN_DOC)..."
	@$(VALIDATE) $(MAIN_DOC)
	@echo "Converting to HTML..."
	$(PANDOC) $(MAIN_DOC) -o $(OUTPUT_HTML) \
		--standalone \
		--self-contained \
		--toc
	@echo "✅ Created: $(OUTPUT_HTML)"

# DOCX output
docx: $(OUTPUT_DOCX)

$(OUTPUT_DOCX): $(MAIN_DOC)
	@echo "Validating $(MAIN_DOC)..."
	@$(VALIDATE) $(MAIN_DOC)
	@echo "Converting to DOCX..."
	$(PANDOC) $(MAIN_DOC) -o $(OUTPUT_DOCX) \
		--standalone \
		$(CITE_OPTS)
	@echo "✅ Created: $(OUTPUT_DOCX)"

# Validation only
validate:
	@$(VALIDATE) $(MAIN_DOC)

# Watch for changes and rebuild
watch:
	@echo "Watching $(MAIN_DOC) for changes..."
	@while true; do \
		inotifywait -e modify $(MAIN_DOC) 2>/dev/null && make pdf; \
	done

# Clean generated files
clean:
	rm -f $(OUTPUT_PDF) $(OUTPUT_HTML) $(OUTPUT_DOCX)
	rm -f *.aux *.log *.out *.toc

# Install project scripts locally
setup:
	@echo "Copying validation script to project..."
	@mkdir -p ./scripts
	@cp $(PLUGIN_DIR)/skills/pandoc/scripts/validate.py ./scripts/
	@chmod +x ./scripts/validate.py
	@echo "✅ Setup complete - validation script available at ./scripts/validate.py"

# Help
help:
	@echo "Available targets:"
	@echo "  all (default) - Build PDF"
	@echo "  pdf           - Build PDF document"
	@echo "  html          - Build HTML document"
	@echo "  docx          - Build DOCX document"
	@echo "  validate      - Validate document only"
	@echo "  watch         - Watch for changes and rebuild"
	@echo "  setup         - Copy scripts to project directory"
	@echo "  clean         - Remove generated files"
	@echo "  help          - Show this help message"

.PHONY: all pdf html docx validate watch clean setup help
