# OpenLibrary Books CSV Exporter

A small Python script that fetches 50 random books from the public **OpenLibrary Search API**, filters books published **after 2000**, sorts them by publish year, and exports the results to a CSV file.

## Features
- Fetch 50 books from OpenLibrary API (`sort=random`)
- Filter: keep only items with `first_publish_year > 2000`
- Sort: by `first_publish_year` (descending)
- Export to CSV: `output/books.csv`

## Requirements
- Python 3.x
- requests

Install dependencies:
```bash
pip install -r requirements.txt
```

## How to run
```bash
python main.py
```

## Output
The script generates:
- `output/books.csv`

CSV columns:
- `title`
- `author`
- `first_publish_year`
- `edition_count`

## Notes
- The query used is `first_publish_year:*` so results come from a broad set of books.
- Some results may not include `first_publish_year`; those entries are ignored.
- A sample output file is committed in the repository as requested.
