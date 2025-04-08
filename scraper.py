from playwright.sync_api import sync_playwright
import requests
import datetime
from firebase_config import FIREBASE_URL

GAME_URL = "https://aviator-demo.spribegaming.com/?currency=USD&operator=demo&jurisdiction=CW&lang=EN&return_url=https%3A%2F%2Fspribe.co%2Fgames&user=34367&token=QtYFB4ypLkmb1bf31E6ujcKqsf8TpxoO"

def send_to_firebase(data):
    res = requests.post(f"{FIREBASE_URL}/aviator.json", json=data)
    print("Data sent to Firebase:", res.status_code, res.text)

def scrape_aviator_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(GAME_URL)
        print("Loaded Aviator demo game...")

        page.wait_for_timeout(10000)  # wait 10 seconds for game data to load

        # Example: extract multiplier values
        multipliers = page.query_selector_all(".crash-point")  # adjust selector based on website structure

        for item in multipliers:
            text = item.inner_text()
            data = {
                "multiplier": text,
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "game_url": GAME_URL
            }
            send_to_firebase(data)

        browser.close()

if __name__ == "__main__":
    scrape_aviator_data()
