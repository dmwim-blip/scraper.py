from playwright.sync_api import sync_playwright
import requests
import time
from firebase_config import firebase_url

aviator_url = "https://aviator-demo.spribegaming.com/?currency=USD&operator=demo&jurisdiction=CW&lang=EN&return_url=https:%2F%2Fspribe.co%2Fgames&user=54175&token=Ynyx3X8IHkq1BeqqS9LC9apbQatq8hSM"

def send_to_firebase(data):
    res = requests.post(f"{firebase_url}/aviator.json", json=data)
    print("[📤] Sent to Firebase:", res.status_code)

def scrape_aviator_data():
    with sync_playwright() as p:
        print("[🚀] Launching browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(aviator_url)
        print("[⏳] Waiting for iframe...")

        # Wait and switch to iframe
        page.wait_for_selector("iframe", timeout=30000)
        iframe = page.frame_locator("iframe").first

        print("[🔍] Waiting for history items...")
        while True:
            try:
                # Updated selector for the colored history multipliers above plane
                elements = iframe.locator(".coefficient")  # this matches the multiplier boxes
                elements.wait_for(timeout=15000)

                values = elements.all_inner_texts()
                print("[✅] Data:", values)

                payload = {
                    "timestamp": int(time.time()),
                    "multipliers": values
                }
                send_to_firebase(payload)

            except Exception as e:
                print("[❌] Error:", e)

            time.sleep(5)

if __name__ == "__main__":
    scrape_aviator_data()
