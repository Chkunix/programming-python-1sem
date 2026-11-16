import sys
from pathlib import Path

from tabulate import tabulate

NAME = "Yaroslav"
SURNAME = "Korolchuk"
GROUP = "IT-31"


def load_expenses(path: Path) -> list[dict]:
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#"):
            continue
        date, category, amount, note = raw.split(";")
        records.append(
            {
                "date": date,
                "category": category,
                "amount": float(amount),
                "note": note,
            }
        )
    return records


def main() -> None:
    print(f"{NAME} {SURNAME}, {GROUP}")
    path = Path(__file__).resolve().parent / "data" / "expenses.csv"
    if not path.is_file():
        print(f"error: {path.as_posix()} not found", file=sys.stderr)
        sys.exit(1)

    grouped: dict[str, list] = {}
    for row in load_expenses(path):
        bucket = grouped.setdefault(row["category"], [0, 0.0])
        bucket[0] += 1
        bucket[1] += row["amount"]

    table = [
        [category, count, round(total, 2)]
        for category, (count, total) in grouped.items()
    ]
    table.append(["TOTAL", sum(row[1] for row in table), round(sum(row[2] for row in table), 2)])
    print(
        tabulate(
            table,
            headers=["category", "count", "total"],
            tablefmt="github",
            floatfmt=".2f",
        )
    )


if __name__ == "__main__":
    main()
