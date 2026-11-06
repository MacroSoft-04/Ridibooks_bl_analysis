import requests
from bs4 import BeautifulSoup
import csv

url = "https://ridibooks.com/keyword-finder/bl?set_id=15&page=1"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

groups = soup.find_all("div", "fig-lby2xw")

category = ["장르", "관계", "인물(공)", "인물(수)", "소재", "분위기/기타"]

with open("ridi_keyword.csv", "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["카테고리", "키워드"])
    for cat, group in zip(category, groups):
        tags = group.find_all("li")

        for tag in tags:
            text = tag.get_text().strip()
            writer.writerow([cat, text])
            print(f"{cat} : {text}")
print("save")
