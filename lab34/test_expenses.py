import subprocess
import sys
from pathlib import Path

import pytest

import expenses

DATA = Path(__file__).resolve().parent / "data" / "expenses.csv"


def test_import_prints_nothing():
    completed = subprocess.run(
        [sys.executable, "-c", "import expenses"],
        cwd=Path(__file__).resolve().parent,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0
    assert completed.stdout == ""
    assert completed.stderr == ""


def test_parse_line():
    assert expenses.parse_line("2026-11-03;food;95.00;lunch at canteen") == {
        "date": "2026-11-03",
        "category": "food",
        "amount": 95.0,
        "comment": "lunch at canteen",
    }


def test_parse_line_bad_field_count():
    with pytest.raises(ValueError):
        expenses.parse_line("2026-11-03;food;95.00")


def test_parse_line_bad_amount():
    with pytest.raises(ValueError):
        expenses.parse_line("2026-11-03;food;abc;lunch")


def test_total_by_category_rounds_to_kopecks():
    records = [
        {"category": "food", "amount": 0.1},
        {"category": "food", "amount": 0.2},
        {"category": "transport", "amount": 20},
    ]
    assert expenses.total_by_category(records) == {"food": 0.3, "transport": 20.0}


def test_load_expenses_skips_comments_and_blank_lines(tmp_path):
    path = tmp_path / "expenses.csv"
    path.write_text(
        "# date;category;amount;note\n\n2026-11-03;food;95.00;lunch\n\n# skip\n",
        encoding="utf-8",
    )
    assert expenses.load_expenses(path) == [
        {"date": "2026-11-03", "category": "food", "amount": 95.0, "comment": "lunch"}
    ]


def test_load_real_file_matches_category_totals():
    records = expenses.load_expenses(DATA)
    assert len(records) == 13
    assert expenses.total_by_category(records) == {
        "food": 645.5,
        "transport": 60.0,
        "coffee": 115.0,
        "stationery": 85.0,
        "internet": 199.0,
    }
