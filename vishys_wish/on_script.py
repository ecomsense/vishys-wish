from playwright.sync_api import Playwright, sync_playwright
from constants import O_CNFG
from datetime import datetime
username = O_CNFG["developer"]["username"]
password = O_CNFG["developer"]["password"]
url_to_update = O_CNFG["developer"]["url_to_update"]


def run(playwright: Playwright, url_to_update) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://developers.kite.trade/login")
    page.get_by_label("E-mail:").click()
    page.get_by_label("E-mail:").fill(username)
    page.get_by_label("E-mail:").press("Tab")
    page.get_by_label("Password:").click()
    page.get_by_label("Password:").fill(password)
    page.get_by_role("button", name="Login").click()
    page.get_by_role("link", name="Quantiply Jaynesh").click()
    page.get_by_label("Redirect URL:").click()
    page.screenshot(path=f"../data/on_script_{str(datetime.now()).replace(':','_')}.png")
    page.get_by_label("Redirect URL:").press("Control+a")
    page.get_by_label("Redirect URL:").fill(url_to_update)
    
    page.get_by_role("button", name="Save").click()
    page.get_by_text("App updated.").click() #https://api.quantiply.tech/brokers/zerodha/redirect/DV8802

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright, url_to_update)
