import requests
import csv
from pathlib import Path

url = "https://openlibrary.org/search.json"
params = {
    "q": "first_publish_year:*",
    "sort": "random",
    "limit": 50,
    "fields": "title,author_name,first_publish_year,edition_count",
}


response = requests.get(url, params=params, timeout=20)
response.raise_for_status()

data = response.json()
docs = data.get("docs", [])
filtered_docs = []

for doc in docs:
    year = doc.get("first_publish_year")
    if year is not None and year > 2000:
        filtered_docs.append(doc)

docs = filtered_docs

docs.sort(key=lambda d: d["first_publish_year"], reverse=True)

OUTPUT_PATH = Path("output/books.csv")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

fieldnames = ["title", "author", "first_publish_year", "edition_count"]

with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for doc in docs:
        title = doc.get("title") or ""
        year = doc.get("first_publish_year")
        edition_count = doc.get("edition_count") or 0

        authors = doc.get("author_name") or []
        author = authors[0] if authors else ""

        row = {
            "title": title,
            "author": author,
            "first_publish_year": year,
            "edition_count": edition_count,
        }

        writer.writerow(row)

print("Fetched:", len(data.get("docs", [])))
print("After filter:", len(docs))
print("Saved:", OUTPUT_PATH)

for doc in docs[:5]:
    print(doc.get("first_publish_year"), "-", doc.get("title"))