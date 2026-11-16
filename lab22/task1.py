from pathlib import Path

NAME = "Yaroslav"
SURNAME = "Korolchuk"
GROUP = "IT-31"
YEAR = "2006"
LANGUAGE = "Python"


def main() -> None:
    script = Path(__file__).resolve()
    script_dir = script.parent
    cwd = Path.cwd()
    home = Path.home()

    for folder in ("data", "reports", "backups"):
        (script_dir / folder).mkdir(exist_ok=True)

    profile = script_dir / "data" / "profile.txt"
    profile.write_text(
        "\n".join(
            (
                f"name: {NAME}",
                f"surname: {SURNAME}",
                f"group: {GROUP}",
                f"year: {YEAR}",
                f"language: {LANGUAGE}",
                "",
            )
        ),
        encoding="utf-8",
    )

    print(f"{'cwd:':<13}{cwd.as_posix()}")
    print(f"{'script:':<13}{script.as_posix()}")
    print(f"{'script dir:':<13}{script_dir.as_posix()}")
    print(f"{'home:':<13}{home.as_posix()}")
    print()
    print(f"{'profile path:':<14}{profile.as_posix()}")
    print(f"{'relative:':<14}{profile.relative_to(script_dir).as_posix()}")
    print(f"{'name:':<14}{profile.name}")
    print(f"{'stem:':<14}{profile.stem}")
    print(f"{'suffix:':<14}{profile.suffix}")
    print(f"{'parent:':<14}{profile.parent.name}")
    print(f"{'size:':<14}{profile.stat().st_size} bytes")
    print()
    print("project tree:")
    show_tree(script_dir)


def show_tree(root: Path, indent: str = "  ") -> None:
    children = sorted(root.iterdir(), key=lambda path: (not path.is_dir(), path.name.lower()))
    for child in children:
        if child.name == "__pycache__":
            continue
        if child.is_dir():
            print(f"{indent}{child.name}/")
            show_tree(child, indent + "  ")
        else:
            print(f"{indent}{child.name}")


main()
