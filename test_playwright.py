import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("Testing Playwright with msedge channel...")
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page()
        page.goto("https://creators.spotify.com")
        print(f"Page title: {page.title()}")
        print(f"Current URL: {page.url}")
        browser.close()
    print("Playwright with msedge works cleanly!")
except Exception as e:
    print(f"Error testing Playwright: {e}")
