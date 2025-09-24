import pathlib
import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.treasurydirect.gov/TA_WS/securities/auctioned?format=json"

OUT_DIR = pathlib.Path("data")
OUT_DIR.mkdir(exist_ok=True)
html_PATH = os.path.join(OUT_DIR,"TreasuryDir.json")

session = requests.Session()
session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
})

resp = session.get(URL, timeout=30)
resp.raise_for_status()

with open(html_PATH, "w", encoding=resp.encoding) as f:
    f.write(resp.text)