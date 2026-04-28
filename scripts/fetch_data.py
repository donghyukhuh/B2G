import requests
import json
import os
from datetime import datetime

SERVICE_KEY = os.getenv("SERVICE_KEY")

KEYWORDS_FILE = "keywords.json"
OUTPUT_FILE = "data/results.json"

BASE_URL = "http://apis.data.go.kr/1230000/ad/BidPublicInfoService"

def load_keywords():
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)["keywords"]

def contains_keyword(title, keywords):
    return any(k in title for k in keywords)

def valid_region(text):
    allow = ["서울", "경기", "전국"]
    return any(a in text for a in allow)

def fetch_list(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    params = {
        "serviceKey": SERVICE_KEY,
        "numOfRows": 50,
        "pageNo": 1,
        "type": "json"
    }
    res = requests.get(url, params=params)
    data = res.json()

    try:
        items = data["response"]["body"]["items"]
        return items if isinstance(items, list) else [items]
    except:
        return []

def process(items, keywords):
    results = []
    for item in items:
        title = item.get("bidNtceNm", "")
        region = item.get("rgstTyNm", "")

        if contains_keyword(title, keywords) and valid_region(region):
            results.append({
                "title": title,
                "amount": item.get("asignBdgtAmt", ""),
                "org": item.get("ntceInsttNm", ""),
                "deadline": item.get("bidClseDt", ""),
                "link": item.get("bidNtceDtlUrl", "#")
            })

    return results[:10]

def main():
    keywords = load_keywords()

    pre = fetch_list("getBidPblancListInfoServcPPSSrch")
    bid = fetch_list("getBidPblancListInfoServcPPSSrch")
    low = fetch_list("getBidPblancListInfoServcPPSSrch")

    data = {
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "pre": process(pre, keywords),
        "bid": process(bid, keywords),
        "low": process(low, keywords)
    }

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
