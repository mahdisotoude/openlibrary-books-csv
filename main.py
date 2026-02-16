from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, cast

import requests

url: str = "https://openlibrary.org/search.json"
params: dict[str, str | int] = {
    "q": "first_publish_year:*",
    "sort": "random",
    "limit": 50,
    "fields": "title,author_name,first_publish_year,edition_count",
}

response: requests.Response = requests.get(url, params=params, timeout=20)
response.raise_for_status()

data: dict[str, Any] = cast(dict[str, Any], response.json())
docs_any: Any = data.get("docs", [])
docs: list[dict[str, Any]] = cast(list[dict[str, Any]], docs_any)

filtered_docs: list[dict[str, Any]] = []

for doc in docs:
    year: int | None = cast(int | None, doc.get("first_publish_year"))
    if year is not None and year > 2000:
        filtered_docs.append(doc)

docs = filtered_docs

docs.sort(key=lambda d: cast(int, d["first_publish_year"]), reverse=True)

OUTPUT_PATH: Path = Path("output/books.csv")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

fieldnames: list[str] = ["title", "author", "first_publish_year", "edition_count"]

with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for doc in docs:
        title: str = cast(str, doc.get("title") or "")
        year: int | None = cast(int | None, doc.get("first_publish_year"))
        edition_count: int = cast(int, doc.get("edition_count") or 0)

        authors: list[str] = cast(list[str], doc.get("author_name") or [])
        author: str = authors[0] if authors else ""

        row: dict[str, Any] = {
            "title": title,
            "author": author,
            "first_publish_year": year,
            "edition_count": edition_count,
        }

        writer.writerow(row)

print("Number of books after filter:", len(docs))
print("CSV file location:", OUTPUT_PATH)
print("Program finished")
