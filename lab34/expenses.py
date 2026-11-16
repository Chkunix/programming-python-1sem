from pathlib import Path


def parse_line(line: str) -> dict:
    parts = line.strip().split(";")
    if len(parts) != 4:
        raise ValueError(f"expected 4 fields, got {len(parts)}")
    date, category, amount_text, comment = parts
    try:
        amount = float(amount_text)
    except ValueError as error:
        raise ValueError(f"amount is not a number: {amount_text}") from error
    return {
        "date": date,
        "category": category,
        "amount": amount,
        "comment": comment,
    }


def total_by_category(records: list[dict]) -> dict[str, float]:
    totals: dict[str, float] = {}
    for record in records:
        category = record["category"]
        totals[category] = totals.get(category, 0.0) + record["amount"]
    return {category: round(total, 2) for category, total in totals.items()}


def load_expenses(path) -> list[dict]:
    records = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        records.append(parse_line(stripped))
    return records
