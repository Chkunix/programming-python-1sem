import sys
from datetime import datetime
from pathlib import Path

NAME = "Yaroslav"
SURNAME = "Korolchuk"
GROUP = "IT-31"

USAGE = """\
usage: python3 task3.py add <date> <category> <amount> <note>
       python3 task3.py list
       python3 task3.py report"""


def expense_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "expenses.csv"


def report_path() -> Path:
    return Path(__file__).resolve().parent / "reports" / "expenses_report.txt"


def print_usage() -> None:
    print(USAGE)


def ensure_store(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("# date;category;amount;note\n", encoding="utf-8")


def load_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        date, category, amount, note = stripped.split(";", 3)
        records.append(
            {
                "date": date,
                "category": category,
                "amount": float(amount),
                "note": note,
            }
        )
    return records


def command_add(args: list[str]) -> int:
    if len(args) < 4:
        print("error: add needs date, category, amount and note")
        print_usage()
        return 1
    date, category, amount_text, *note_parts = args
    try:
        amount = float(amount_text)
    except ValueError:
        print("error: amount must be a number")
        print_usage()
        return 1
    note = " ".join(note_parts)
    path = expense_path()
    ensure_store(path)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"{date};{category};{amount:.2f};{note}\n")
    print(f"added: {date} {category} {amount:.2f} ({note})")
    return 0


def command_list() -> int:
    records = load_records(expense_path())
    headers = ("date", "category", "amount", "note")
    date_w = max([len(headers[0]), *(len(row["date"]) for row in records)] or [len(headers[0])])
    cat_w = max([len(headers[1]), *(len(row["category"]) for row in records)] or [len(headers[1])])
    amount_w = max(len(headers[2]), 8)
    print(f"{headers[0]:<{date_w}}  {headers[1]:<{cat_w}}  {headers[2]:>{amount_w}}  {headers[3]}")
    total = 0.0
    for row in records:
        total += row["amount"]
        print(
            f"{row['date']:<{date_w}}  {row['category']:<{cat_w}}  "
            f"{row['amount']:>{amount_w}.2f}  {row['note']}"
        )
    print(f"{len(records)} records, total {total:.2f}")
    return 0


def build_report(records: list[dict]) -> str:
    dates = [datetime.strptime(row["date"], "%Y-%m-%d").date() for row in records]
    first, last = min(dates), max(dates)
    span = (last - first).days + 1
    grand = sum(row["amount"] for row in records)

    grouped: dict[str, list] = {}
    per_day: dict = {}
    for row in records:
        bucket = grouped.setdefault(row["category"], [0, 0.0])
        bucket[0] += 1
        bucket[1] += row["amount"]
        per_day[row["date"]] = per_day.get(row["date"], 0.0) + row["amount"]

    ranked = sorted(grouped.items(), key=lambda item: (-item[1][1], item[0]))
    top_day = max(per_day.items(), key=lambda item: item[1])
    expensive = max(records, key=lambda row: row["amount"])

    lines = [
        f"Expenses report for {NAME} {SURNAME} ({GROUP})",
        f"Period: {first.isoformat()} .. {last.isoformat()}",
        f"Records: {len(records)}",
        "",
        f"{'category':<12} {'count':>5} {'total':>9} {'share':>7}  chart",
        "-" * 52,
    ]
    for category, (count, total) in ranked:
        share = (total / grand * 100) if grand else 0.0
        chart = "#" * int(round(share / 5))
        lines.append(f"{category:<12} {count:>5} {total:>9.2f} {share:>6.1f}%  {chart}")
    lines.extend(
        [
            "-" * 52,
            f"{'total':<12} {len(records):>5} {grand:>9.2f} {'100.0%':>7}",
            "",
            f"Top day: {top_day[0]} ({top_day[1]:.2f})",
            f"Most expensive: {expensive['category']} {expensive['amount']:.2f} ({expensive['note']})",
            f"Average per day: {grand / span:.2f}",
        ]
    )
    return "\n".join(lines) + "\n"


def command_report() -> int:
    records = load_records(expense_path())
    if not records:
        print("error: no expenses to report")
        return 1
    text = build_report(records)
    path = report_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(text, end="")
    print(f"report saved to: {path.relative_to(path.parent.parent).as_posix()}")
    return 0


def main(argv: list[str]) -> int:
    if not argv:
        print_usage()
        return 0
    command, *args = argv
    if command == "add":
        return command_add(args)
    if command == "list":
        return command_list()
    if command == "report":
        return command_report()
    print(f"error: unknown command {command}")
    print_usage()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
