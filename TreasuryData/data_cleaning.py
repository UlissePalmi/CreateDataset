import json
from pathlib import Path
from typing import List, Dict, Any

path = Path("data") / "TreasuryDir.json"

def read_auctions_json(path: str | Path) -> List[Dict[str, Any]]:

    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Optional: basic shape check
    if not isinstance(data, list):
        raise ValueError(f"Expected a list in {p}, got {type(data).__name__}")
    return data

data = read_auctions_json(path)

KEEP = ["cusip", "securityType", "securityTerm", "auctionDate", "offeringAmount"]

slim = [{k: a.get(k) for k in KEEP} for a in data]


for s in slim:                                                                              # offered ammount in B.
    s["offeringAmount"] = int(int(s["offeringAmount"])/1000000000)
    
for s in slim:                                                                              # offered ammount in B.
    s["auctionDate"] = s["auctionDate"][:10]
    




print(slim)