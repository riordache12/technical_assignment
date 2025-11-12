import csv
from typing import List, Dict, Any
from datetime import datetime

def read_csv_as_dicts(path: str) -> List[Dict[str, Any]]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

# AI-ASSIST:
def parse_date(date_str: str) -> datetime:
    formats = [
        "%Y-%m-%d",      # 2025-11-12
        "%d/%m/%Y",      # 12/11/2025
        "%m/%d/%Y",      # 11/12/2025
        "%Y/%m/%d",      # 2025/11/12
        "%d-%m-%Y",      # 12-11-2025
    ]

    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        pass

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    # If all fails, return a safe default
    return datetime(1970, 1, 1)