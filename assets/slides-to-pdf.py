#!/usr/bin/env python3
"""Convert a RevealJS slide deck to PDF using Playwright.

Usage: python slides-to-pdf.py <url> <output.pdf>

Waits for RevealJS and MathJax to fully render before printing.
"""

import sys
import time
from playwright.sync_api import sync_playwright, Error as PlaywrightError

# RevealJS default slide dimensions
SLIDE_WIDTH = 960
SLIDE_HEIGHT = 700

MAX_RETRIES = 5
RETRY_DELAY = 3  # seconds


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <url> <output.pdf>")
        sys.exit(1)

    url, output = sys.argv[1], sys.argv[2]

    # Append ?print-pdf for RevealJS print layout
    sep = "&" if "?" in url else "?"
    print_url = f"{url}{sep}print-pdf"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_viewport_size({"width": SLIDE_WIDTH, "height": SLIDE_HEIGHT})

        # Retry loop — preview server may not be ready yet
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                print(f"  Loading {print_url} (attempt {attempt})")
                page.goto(print_url, wait_until="networkidle", timeout=30000)
                break
            except PlaywrightError as e:
                if attempt == MAX_RETRIES:
                    print(f"  Failed after {MAX_RETRIES} attempts")
                    browser.close()
                    sys.exit(1)
                print(f"  Connection failed, retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)

        # Wait for RevealJS to initialize
        page.wait_for_function(
            "typeof Reveal !== 'undefined' && Reveal.isReady()",
            timeout=15000,
        )

        # Wait for MathJax to finish typesetting (supports v2 and v3)
        page.set_default_timeout(30000)
        page.evaluate(
            """
            async () => {
                if (typeof MathJax === 'undefined') return;
                if (MathJax.startup) {
                    // MathJax 3
                    await MathJax.startup.promise;
                    if (MathJax.typesetPromise) {
                        await MathJax.typesetPromise();
                    }
                } else if (MathJax.Hub) {
                    // MathJax 2 — drain the typeset queue
                    await new Promise(resolve => MathJax.Hub.Queue(resolve));
                }
            }
        """
        )

        # Verify no unprocessed math remains (best-effort: MathJax 2 may keep
        # preview text with visibility:hidden, which innerText still picks up)
        try:
            page.wait_for_function(
                """() => {
                    const body = document.body.innerText;
                    return !body.includes('\\\\(') && !body.includes('\\\\[');
                }""",
                timeout=15000,
            )
        except PlaywrightError:
            print("  Warning: math check timed out — proceeding (MathJax 2 preview text may persist)")

        # Hide slide numbers from the PDF
        page.evaluate(
            """
            document.querySelectorAll('.slide-number').forEach(el => el.remove());
        """
        )

        # Extra pause for fonts and remaining rendering
        time.sleep(2)

        page.pdf(
            path=output,
            print_background=True,
            prefer_css_page_size=True,
        )

        browser.close()
        print(f"  Saved {output}")


if __name__ == "__main__":
    main()
