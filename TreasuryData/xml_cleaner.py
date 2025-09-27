from pathlib import Path
import os
import csv
import re

maturity = "4-week"
destination = "UST_csv.csv"
Folder = Path("td_xml") / maturity

def data_type(file):
    letter = file[0]
    if letter == "A":
        Data_type = "RECOMMENDATION_FOR_THIS_REFUNDING"
    elif letter == "R":
        Data_type = "HISTORICAL_REFERENCE"
    else:
        Data_type = None
    return Data_type

def jsoncreater(content, data_type_value):
    match = re.search(r"<SecurityTermWeekYear>(.*?)<\/SecurityTermWeekYear>", content)
    Maturity, Units = match.group(1).split('-')[0], match.group(1).split('-')[1]

    match = re.search(r"<SecurityType>(.*?)</SecurityType>", content)
    Security_type = match.group(1)

    match = re.search(r"<AuctionDate>(.*?)</AuctionDate>", content)
    Auction_date = match.group(1)
    Auction_month = match.group(1)[:7]
    
    match = re.search(r"<OfferingAmount>(.*?)</OfferingAmount>", content)
    Offered_amount = match.group(1).split(".")[0]

    UST_Data = {
        "Security_type": Security_type,
        "Maturity": Maturity,
        "Units": Units,
        "Auction_month": Auction_month,
        "Auction_date": Auction_date,
        "Offered_amount": Offered_amount,
        "data_type": data_type_value
    }
    return UST_Data

UST_Data = []
for file in os.listdir(Folder):

    filepath = Folder / file

    with open(filepath, 'r') as f:
        content = f.read()
        data_type_value = data_type(file)
        UST_Data.append(jsoncreater(content, data_type_value))

print("Finished cleaning the data")

with open(destination, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=UST_Data[0].keys())
    writer.writeheader()  # write column names
    writer.writerows(UST_Data)

print(f"Data saved in {destination}")