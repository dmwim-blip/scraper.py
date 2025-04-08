from playwright.sync_api import sync_playwright
import time
import json
import requests
from firebase_config import firebase_url

def scrape_aviator_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("[🚀] Opening Aviator demo...")
        page.goto("https://aviator-demo.spribegaming.com/?currency=USD&operator=demo&jurisdiction=CW&lang=EN&return_url=https:%2F%2Fspribe.co%2Fgames&user=54175&token=Ynyx3X8IHkq1BeqqS9LC9apbQatq8hSM", wait_until="networkidle")

        print("[⏳] Waiting for iframe to load...")
        page.wait_for_selector("iframe", timeout=60000)

        # Get the iframe element
        iframe_element = page.query_selector("iframe")
        frame = iframe_element.content_frame()

        print("[✅] Inside iframe")

        while True:
            try:
                # Reload iframe contents
                frame.reload()
                time.sleep(2)

                # Wait for history block to load
                frame.wait_for_selector(".history", timeout=30000)

                # Select all multipliers
                values = frame.query_selector_all(".history .history-item__value")
                if not values:
                    print("[⚠️] No values found. Retrying...")
                    time.sleep(1)
                    continue

                # Get latest (first) multiplier
                multiplier_text = values[0].inner_text().strip()
                multiplier_value = float(multiplier_text.replace("x", ""))

                game_data = {
                    "multiplier": multiplier_value,
                    "timestamp": int(time.time()),
                    "game_url": page.url
                }

                # Send to Firebase
                response = requests.post(f"{firebase_url}/aviator.json", data=json.dumps(game_data))
                if response.status_code == 200:
                    print(f"[✅] Sent: {multiplier_value}x")
                else:
                    print("[⚠️] Firebase error:", response.text)

                time.sleep(1)

            except Exception as e:
                print("[❌] Error while scraping:", e)
                time.sleep(3)

if __name__ == "__main__":
    scrape_aviator_data()
