import csv
from typing import Dict, List, Any


# AI-assist
class CSVWriter:
    """Class to write rows to a CSV file with fixed headers."""
    @staticmethod
    def write(path: str, rows: List[Dict[str, Any]]) -> None:
        fieldnames = ["date", "reach", "q_m3s", "c_mgL"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for r in rows:
                w.writerow(r)
