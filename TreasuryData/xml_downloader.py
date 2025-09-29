import argparse
from playwright.sync_api import sync_playwright
from pathlib import Path
from urllib.parse import urljoin
import os

Security_type_list = {
    "Bill": ["4-Week", "8-Week", "13-Week", "17-Week", "26-Week", "52-Week"],
    #"Note": ["2-Year", "3-Year", "5-Year", "7-Year", "10-Year"], 
    #"Bond": ["20-Year", "30-Year"], 
    #"TIPS": ["5-Year", "10-Year", "30-Year"]
    #"FRN": ["2-Year"]
    }
year = 2025
ROOT = "https://treasurydirect.gov/auctions/announcements-data-results/announcement-results-press-releases/"

while year != 1996:
    for Security_type in Security_type_list.keys():
        print(Security_type)
        maturity_list = Security_type_list.get(Security_type)
        for maturity in maturity_list:
            print(maturity)
            OUTDIR = Path(fr"C:\Users\upalmier\Documents\CreateDataset\td_xml\{year}\{Security_type}\{maturity}")
            OUTDIR.mkdir(parents=True, exist_ok=True)
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False, slow_mo=300)
                page = browser.new_page()
                page.goto(ROOT, wait_until="domcontentloaded")
                page.wait_for_timeout(300)

                page.get_by_role("combobox").click()   # the year dropdown
                page.keyboard.type(f"{year}")
                page.get_by_role("option", name=f"{year}", exact=True).click()

                
                page.locator("#jqButtonYear").click() 
                page.wait_for_timeout(300)

                maturity_row = page.locator("#contenttablejqxGrid [role='row']").filter(has_text=Security_type).first
                maturity_row.scroll_into_view_if_needed()                                                                # scrolls to the bills section    
                maturity_row.locator("[role='gridcell'][columnindex='0']").first.click()
                page.wait_for_timeout(300)

                term_row = page.locator("#contenttablejqxGrid [role='row']").filter(has_text=maturity).first
                
                if term_row.count() == 0:
                    print(f"No {Security_type} {maturity} found")
                else:
                    term_row.scroll_into_view_if_needed()
                    term_row.locator("[role='gridcell'][columnindex='1']").first.click()

                    xml_links = page.locator(
                        f"#contenttablejqxGrid [role='row']:has-text('{maturity}') a[href$='.xml'], "
                        f"#contenttablejqxGrid [role='row']:has-text('{maturity}') a[href*='.xml?']"
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
    year = year - 1
    print(year)