from pathlib import Path


def find_root(start: Path, marker: str = "pyproject.toml") -> Path:
    current = start.resolve()

    for parent in [current, *current.parents]:
        if (parent / marker).exists():
            return parent

    raise FileNotFoundError(f"Cannot find {marker} from {start}")


WORKSPACE_ROOT = find_root(Path(__file__))