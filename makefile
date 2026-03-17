# ============================================================
# Makefile for Econ 502 course materials
# ============================================================

PORT := $(shell python3 -c "import socket; s=socket.socket(); s.bind(('',0)); print(s.getsockname()[1]); s.close()")
SLIDES_TO_PDF = python3 assets/slides-to-pdf.py

SLIDES_DIR = slides
OUTPUT_DIR = docs

SLIDE_FILES = $(wildcard $(SLIDES_DIR)/*.qmd)
SLIDE_NAMES = $(notdir $(basename $(SLIDE_FILES)))

SLIDE_HTMLS = $(addprefix $(OUTPUT_DIR)/$(SLIDES_DIR)/,$(addsuffix .html,$(SLIDE_NAMES)))
SLIDE_PDFS  = $(addprefix $(OUTPUT_DIR)/$(SLIDES_DIR)/,$(addsuffix .pdf,$(SLIDE_NAMES)))

# Source directories that accumulate preview artifacts (docs/ is never touched)
SOURCE_DIRS = slides add-content practice-problems exams content

.PHONY: all website slides pdfs preview stop clean clean-aux

all: website pdfs

# ------------------------------------------------------------
# Website / HTML
# ------------------------------------------------------------

website:
	quarto render

slides: $(SLIDE_HTMLS)

$(OUTPUT_DIR)/$(SLIDES_DIR)/%.html: $(SLIDES_DIR)/%.qmd
	quarto render $<

# ------------------------------------------------------------
# Slide PDFs (Playwright + preview server)
# ------------------------------------------------------------

pdfs: preview $(SLIDE_PDFS) stop

preview:
	quarto preview --no-browser --port $(PORT) &
	@echo "Waiting for preview server on port $(PORT)..."
	@for i in 1 2 3 4 5 6 7 8 9 10; do \
		curl -s -o /dev/null http://localhost:$(PORT) && break; \
		sleep 1; \
	done

$(OUTPUT_DIR)/$(SLIDES_DIR)/%.pdf: $(OUTPUT_DIR)/$(SLIDES_DIR)/%.html
	@echo "Generating PDF for $*..."
	$(SLIDES_TO_PDF) "http://localhost:$(PORT)/$(SLIDES_DIR)/$*.html" $@

stop:
	@pkill -f "quarto preview" 2>/dev/null || true

# ------------------------------------------------------------
# Convenience targets
# ------------------------------------------------------------

$(SLIDE_NAMES): %: $(OUTPUT_DIR)/$(SLIDES_DIR)/%.html $(OUTPUT_DIR)/$(SLIDES_DIR)/%.pdf

$(addsuffix -html,$(SLIDE_NAMES)): %-html: $(OUTPUT_DIR)/$(SLIDES_DIR)/%.html

$(addsuffix -pdf,$(SLIDE_NAMES)): %-pdf: preview $(OUTPUT_DIR)/$(SLIDES_DIR)/%.pdf stop

clean:
	rm -f $(SLIDE_HTMLS) $(SLIDE_PDFS)

# Remove HTML, PDF, figure dirs, and LaTeX aux files created by quarto preview
# in source directories. Never touches docs/.
clean-aux:
	@echo "Removing preview artifacts from source directories..."
	@find $(SOURCE_DIRS) \( \
		-name "*.html" -o \
		-name "*.pdf" -o \
		-name "*.aux" -o \
		-name "*.log" -o \
		-name "*.toc" -o \
		-name "*.out" -o \
		-name "*.synctex.gz" -o \
		-name "*.fls" -o \
		-name "*.fdb_latexmk" -o \
		-name "*.quarto_ipynb" \
	\) -delete 2>/dev/null || true
	@find $(SOURCE_DIRS) -type d -name "*_files" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf site_libs
	@echo "Done."
