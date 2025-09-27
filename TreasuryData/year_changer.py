import argparse
from playwright.sync_api import sync_playwright
from pathlib import Path
from urllib.parse import urljoin
import os

out = []
OUTDIR = Path(r"C:\Users\upalmier\Documents\CreateDataset\td_xml\2-year")
OUTDIR.mkdir(parents=True, exist_ok=True)

ROOT = "https://treasurydirect.gov/auctions/announcements-data-results/announcement-results-press-releases/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)
    page = browser.new_page()
    page.goto(ROOT, wait_until="domcontentloaded")
    page.wait_for_timeout(300)

    page.get_by_role("combobox").click()   # the year dropdown
    page.get_by_role("listbox").get_by_role("option", name="2017", exact=True).click()
    page.wait_for_timeout(300)
    page.locator("#jqButtonYear").click() 
    page.wait_for_timeout(300)

    browser.close()