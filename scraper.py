# scraper.py

import time
import json
import requests
from datetime import datetime
from playwright.sync_api import sync_playwright
from firebase_config import firebase_url

def scrape_aviator_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Demo Aviator game URL
        url = "https://aviator-demo.spribegaming.com/?currency=USD&operator=demo&jurisdiction=CW&lang=EN&return_url=https:%2F%2Fspribe.co%2Fgames&user=54175&token=Ynyx3X8IHkq1BeqqS9LC9apbQatq8hSM"
        page.goto(url)

        print("[⏳] Waiting for the game to load...")
        page.wait_for_timeout(15000)  # wait 15 seconds for game data

        while True:
            try:
                result = page.eval_on_selector(".history-item__value", "el => el.innerText")
                timestamp = datetime.utcnow().isoformat()

                data = {
                    "timestamp": timestamp,
                    "result": result
                }

                print(f"[✅] Collected: {data}")

                requests.post(f"{firebase_url}/aviator.json", data=json.dumps(data))
                time.sleep(1)

            except Exception as e:
                print("[❌] Error while scraping:", str(e))
                time.sleep(5)

if __name__ == "__main__":
    scrape_aviator_data()
