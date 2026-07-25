from playwright.sync_api import sync_playwright


def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto("https://mobile.de")

        input("Tryck Enter för att stänga...")

        browser.close()


if __name__ == "__main__":
    test()