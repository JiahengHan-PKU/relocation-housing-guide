"""Print a local HTML file to PDF with Chrome."""

import os
import sys

from playwright.sync_api import sync_playwright


def render_pdf(html_path, pdf_path):
    """Save a PDF using the page's own CSS page size.

    Args:
        html_path: Local HTML file.
        pdf_path: Destination PDF file.

    Returns:
        The output size in megabytes.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page()
        page.goto("file://" + os.path.abspath(html_path), wait_until="load")
        page.pdf(path=pdf_path, prefer_css_page_size=True, print_background=True, tagged=True, outline=True)
        browser.close()
    return round(os.path.getsize(pdf_path) / 1e6, 2)


if __name__ == "__main__":
    print(render_pdf(sys.argv[1], sys.argv[2]), "MB")
