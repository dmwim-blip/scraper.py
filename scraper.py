# scraper.py
from playwright.sync_api import sync_playwright
import time
import requests
import firebase_config

def scrape_aviator_data():
    with sync_playwright() as p:
        print("[🚀] Launching browser...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("[🌐] Opening Aviator demo game...")
        page.goto("https://demo.spribe.io/launch/aviator?currency=USD&lang=EN&return_url=https://spribe.co/games")

        print("[⏳] Waiting for the game to load...")
        page.wait_for_timeout(10000)  # wait 10 seconds for full load

        while True:
            try:
                # ✅ Get multiplier values from the new selector
                payouts = page.query_selector_all(".payouts-block span")
                multipliers = [p.inner_text() for p in payouts if "x" in p.inner_text()]

                if multipliers:
                    print("[📊] Multipliers:", multipliers)

                    # 🔥 Push to Firebase
                    data = {"multipliers": multipliers, "timestamp": int(time.time())}
                    response = requests.post(
                        f"{firebase_config.FIREBASE_URL}/aviator_data.json", json=data
                    )
                    print("[✅] Uploaded to Firebase:", response.status_code)
                else:
                    print("[⚠️] No multipliers found.")

            except Exception as e:
                print("[❌] Error while scraping:", str(e))

            time.sleep(5)

if __name__ == "__main__":
    scrape_aviator_data()
