"""Render a JavaScript page with the local Chrome."""

from playwright.sync_api import sync_playwright


def render_page(url, wait_ms=5000):
    """Open a page in headless Chrome and return its visible text.

    Args:
        url: Page to open.
        wait_ms: Extra time for scripts to finish after load.

    Returns:
        A (status, text) tuple, where status is the HTTP status code.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page()
        response = page.goto(url, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(wait_ms)
        text = page.inner_text("body")
        browser.close()
    return response.status, text
