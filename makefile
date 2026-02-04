# ============================================================
# Makefile for Quarto slides (streamlined)
# ============================================================

PORT := $(shell python3 -c "import socket; s=socket.socket(); s.bind(('',0)); print(s.getsockname()[1]); s.close()")
CHROME = /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome

SLIDES_DIR = slides
OUTPUT_DIR = docs

SLIDE_FILES = $(wildcard $(SLIDES_DIR)/*.qmd)
SLIDE_NAMES = $(notdir $(basename $(SLIDE_FILES)))

SLIDE_HTMLS = $(addprefix $(OUTPUT_DIR)/$(SLIDES_DIR)/,$(addsuffix .html,$(SLIDE_NAMES)))
SLIDE_PDFS  = $(addprefix $(OUTPUT_DIR)/$(SLIDES_DIR)/,$(addsuffix .pdf,$(SLIDE_NAMES)))

.PHONY: all website slides pdfs preview stop clean

all: website slides pdfs

# ------------------------------------------------------------
# Website / HTML
# ------------------------------------------------------------

website:
	quarto render

slides: $(SLIDE_HTMLS)

$(OUTPUT_DIR)/$(SLIDES_DIR)/%.html: $(SLIDES_DIR)/%.qmd
	quarto render $<

# ------------------------------------------------------------
# PDF generation (single preview server)
# ------------------------------------------------------------

pdfs: preview $(SLIDE_PDFS) stop

preview:
	quarto preview --no-browser --port $(PORT) &
	sleep 4

$(OUTPUT_DIR)/$(SLIDES_DIR)/%.pdf: $(OUTPUT_DIR)/$(SLIDES_DIR)/%.html
	decktape reveal "http://localhost:$(PORT)/$(SLIDES_DIR)/$*.html" $@

stop:
	pkill -f "quarto preview" || true

# ------------------------------------------------------------
# Convenience targets
# ------------------------------------------------------------

$(SLIDE_NAMES): %: $(OUTPUT_DIR)/$(SLIDES_DIR)/%.html $(OUTPUT_DIR)/$(SLIDES_DIR)/%.pdf

$(addsuffix -html,$(SLIDE_NAMES)): %-html: $(OUTPUT_DIR)/$(SLIDES_DIR)/%.html

$(addsuffix -pdf,$(SLIDE_NAMES)): %-pdf: preview $(OUTPUT_DIR)/$(SLIDES_DIR)/%.pdf

clean:
	rm -f $(SLIDE_HTMLS) $(SLIDE_PDFS)