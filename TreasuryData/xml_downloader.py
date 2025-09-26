import argparse
from playwright.sync_api import sync_playwright
from pathlib import Path
from urllib.parse import urljoin
import os

out = []
OUTDIR = Path(r"C:\Users\upalmier\Documents\CreateDataset\td_xml\4week")
OUTDIR.mkdir(parents=True, exist_ok=True)

ROOT = "https://treasurydirect.gov/auctions/announcements-data-results/announcement-results-press-releases/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)
    page = browser.new_page()
    page.goto(ROOT, wait_until="domcontentloaded")

    bill_row = page.locator("#contenttablejqxGrid [role='row']").filter(has_text="Bill").first
    bill_row.scroll_into_view_if_needed()                                                               # scrolls to the bills section    
    bill_row.locator("[role='gridcell'][columnindex='0']").first.click()
    page.wait_for_timeout(300)

    term_row = page.locator("#contenttablejqxGrid [role='row']").filter(has_text="4-Week").first
    term_row.scroll_into_view_if_needed()
    term_row.locator("[role='gridcell'][columnindex='1']").first.click()

    xml_links = page.locator(
        "#contenttablejqxGrid [role='row']:has-text('4-Week') a[href$='.xml'], "
        "#contenttablejqxGrid [role='row']:has-text('4-Week') a[href*='.xml?']"
    )

    req = p.request.new_context()
    for i in range(xml_links.count()):
        href = xml_links.nth(i).get_attribute("href") or ""
        url = urljoin(page.url, href)
        fn = (url.split("/")[-1].split("?")[0]) or f"file_{i+1}.xml"
        (OUTDIR / fn).write_bytes(req.get(url).body())
        print("Saved:", fn)
    req.dispose()
    browser.close()