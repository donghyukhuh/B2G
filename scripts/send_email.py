import yagmail
import json
import os

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def load_data():
    with open("data/results.json", "r", encoding="utf-8") as f:
        return json.load(f)

def make_content(data):
    text = f"입찰정보 업데이트 ({data['updated']})\n\n"

    for section in ["pre", "bid", "low"]:
        text += f"[{section.upper()}]\n"
        for item in data[section]:
            text += f"- {item['title']}\n"
            text += f"  기관: {item['org']}\n"
            text += f"  마감: {item['deadline']}\n\n"

    return text

def main():
    data = load_data()
    content = make_content(data)

    yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)

    yag.send(
        to="dongpr1018@gmail.com",
        subject="나라장터 맞춤 입찰정보",
        contents=content
    )

if __name__ == "__main__":
    main()
