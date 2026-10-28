import time
import os
from playwright.sync_api import sync_playwright

def capture():
    os.makedirs("screenshots", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 960}, device_scale_factor=2)
        page = context.new_page()

        print("Navigating to http://localhost:8501...")
        page.goto("http://localhost:8501", wait_until="networkidle")
        time.sleep(3)

        # 1. Route Planner (Standard Campus)
        print("Capturing Route Planner...")
        page.screenshot(path="screenshots/01_route_planner.png", full_page=True)

        # 2. Algorithm Comparison Tab
        print("Capturing Algorithm Comparison Tab...")
        tab_buttons = page.query_selector_all("button[data-baseweb='tab']")
        if len(tab_buttons) >= 2:
            tab_buttons[1].click()
            time.sleep(2)
            page.screenshot(path="screenshots/02_algorithm_comparison.png", full_page=True)

        # 3. About the Project Tab
        print("Capturing About Project Tab...")
        if len(tab_buttons) >= 3:
            tab_buttons[2].click()
            time.sleep(2)
            page.screenshot(path="screenshots/03_project_overview.png", full_page=True)

        # 4. Switch to Extended University Campus map and capture
        print("Capturing Extended Campus Map...")
        if len(tab_buttons) >= 1:
            tab_buttons[0].click()
            time.sleep(1)
            # Find the selectbox for dataset
            selectboxes = page.query_selector_all("div[data-baseweb='select']")
            if selectboxes:
                # Click the first selectbox (campus map dataset)
                selectboxes[0].click()
                time.sleep(1)
                options = page.query_selector_all("li[role='option']")
                for opt in options:
                    if "Extended" in opt.inner_text():
                        opt.click()
                        time.sleep(3)
                        break
                page.screenshot(path="screenshots/04_extended_campus_map.png", full_page=True)

        browser.close()
        print("Screenshots captured successfully!")

if __name__ == "__main__":
    capture()
