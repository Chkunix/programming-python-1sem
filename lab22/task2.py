from datetime import datetime
from pathlib import Path

NAME = "Yaroslav"
SURNAME = "Korolchuk"


def count_runs(path: Path) -> int:
    if not path.exists():
        return 0
    lines = path.read_text(encoding="utf-8").splitlines()
    return sum(1 for line in lines if line.strip())


def add_run(path: Path, number: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"{number};{stamp};{NAME} {SURNAME}\n")


def show_history(path: Path, last: int = 3) -> None:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        number, stamp, student = line.split(";", 2)
        rows.append((number, stamp, student))

    print(f"runs so far: {len(rows)}")
    print("last runs:")
    for number, stamp, student in rows[-last:]:
        print(f"  # {number}  {stamp}  {student}")
    print(f"first run was at {rows[0][1]}")


def main() -> None:
    path = Path(__file__).resolve().parent / "data" / "runs.log"
    created = not path.exists()
    number = count_runs(path) + 1
    add_run(path, number)
    if created:
        print("data/runs.log was just created.")
    print(f"Hello, {NAME} {SURNAME}! This is run number {number}.")
    show_history(path, last=3)


main()
