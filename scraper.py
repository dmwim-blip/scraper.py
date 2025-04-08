from playwright.sync_api import sync_playwright
import time
import requests
import json
from firebase_config import firebase_url

def scrape_aviator_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("[🚀] Opening Aviator demo...")
        page.goto("https://aviator-demo.spribegaming.com/?currency=USD&operator=demo&jurisdiction=CW&lang=EN&return_url=https:%2F%2Fspribe.co%2Fgames&user=54175&token=Ynyx3X8IHkq1BeqqS9LC9apbQatq8hSM")

        print("[⏳] Waiting for the game to load...")

        # Wait for game history to appear
        page.wait_for_selector(".recent-history", timeout=60000)

        while True:
            try:
                page.reload()
                time.sleep(2)

                # Get the latest multiplier value
                multiplier_element = page.query_selector(".history-item__value")
                if not multiplier_element:
                    print("[⚠️] Game data not found yet. Waiting...")
                    time.sleep(1)
                    continue

                multiplier_text = multiplier_element.inner_text().strip()
                multiplier_value = float(multiplier_text.replace("x", ""))

                # Prepare data to store
                game_data = {
                    "multiplier": multiplier_value,
                    "timestamp": int(time.time()),
                    "game_url": page.url
                }

                # Send data to Firebase
                response = requests.post(f"{firebase_url}/aviator.json", data=json.dumps(game_data))
                if response.status_code == 200:
                    print(f"[✅] Sent: {multiplier_value}x")
                else:
                    print("[⚠️] Failed to send to Firebase:", response.text)

                time.sleep(1)

            except Exception as e:
                print("[❌] Error while scraping:", e)
                time.sleep(2)

if __name__ == "__main__":
    scrape_aviator_data()
