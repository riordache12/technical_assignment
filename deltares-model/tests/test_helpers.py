import os
import tempfile
from datetime import datetime

import pytest

from deltares_model.helpers import read_csv_as_dicts, parse_date


# AI-ASSIST:
def test_read_csv_as_dicts_reads_rows_correctly():
    # Create a temporary CSV file
    tmpfile = tempfile.NamedTemporaryFile(
        delete=False, mode="w", newline="", encoding="utf-8"
    )
    tmpfile.write("date,precip_mm,et_mm\n")
    tmpfile.write("2024-01-01,5.0,1.0\n")
    tmpfile.write("2024-01-02,0.0,1.5\n")
    tmpfile.close()

    rows = read_csv_as_dicts(tmpfile.name)

    assert isinstance(rows, list)
    assert len(rows) == 2
    assert rows[0]["date"] == "2024-01-01"
    assert rows[0]["precip_mm"] == "5.0"
    assert rows[1]["et_mm"] == "1.5"

    os.remove(tmpfile.name)


def test_read_csv_as_dicts_empty_file():
    tmpfile = tempfile.NamedTemporaryFile(
        delete=False, mode="w", newline="", encoding="utf-8"
    )
    tmpfile.write("date,precip_mm\n")  # header only
    tmpfile.close()

    rows = read_csv_as_dicts(tmpfile.name)
    assert rows == []

    os.remove(tmpfile.name)


def test_parse_date_isoformat():
    d = parse_date("2025-11-12")
    assert isinstance(d, datetime)
    assert d.year == 2025 and d.month == 11 and d.day == 12


@pytest.mark.parametrize(
    "date_str,expected",
    [
        ("30/11/2025", datetime(2025, 11, 30)),
        ("11/30/2025", datetime(2025, 11, 30)),
        ("2025/11/30", datetime(2025, 11, 30)),
        ("30-11-2025", datetime(2025, 11, 30)),
    ],
)
def test_parse_date_multiple_formats(date_str, expected):
    d = parse_date(date_str)
    assert d == expected


def test_parse_date_invalid_returns_default():
    d = parse_date("not-a-date")
    assert d == datetime(1970, 1, 1)
