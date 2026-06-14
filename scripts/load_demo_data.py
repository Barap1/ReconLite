"""Load ReconLite demo records into MongoDB."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEMO_DATA_FILE = PROJECT_ROOT / "sample_data" / "demo_results.json"


def load_records() -> list[dict]:
    with DEMO_DATA_FILE.open("r", encoding="utf-8") as demo_file:
        records = json.load(demo_file)
    if not isinstance(records, list):
        raise ValueError("demo data must be a JSON list")
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Load safe ReconLite demo data into MongoDB.")
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Delete existing records from the target collection before inserting demo data.",
    )
    args = parser.parse_args()

    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    database_name = os.getenv("DATABASE_NAME", "scannerdb")
    collection_name = os.getenv("COLLECTION_NAME", "sslchecker")

    from pymongo import MongoClient

    client = MongoClient(mongo_uri)
    collection = client[database_name][collection_name]
    records = load_records()

    if args.clear:
        deleted = collection.delete_many({}).deleted_count
        print(f"Deleted {deleted} existing records.")

    result = collection.insert_many(records)
    print(f"Inserted {len(result.inserted_ids)} demo records into {database_name}.{collection_name}.")


if __name__ == "__main__":
    main()
