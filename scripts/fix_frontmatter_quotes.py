#!/usr/bin/env python3
"""Replace curly/smart quotes with straight quotes in YAML frontmatter."""

import sys
import re
from pathlib import Path

CURLY_MAP = {
    "“": '"',  # "
    "”": '"',  # "
    "‘": "'",  # '
    "’": "'",  # '
}


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return False

    end = text.find("---", 3)
    if end == -1:
        return False

    frontmatter = text[: end + 3]
    body = text[end + 3 :]

    fixed = frontmatter
    for curly, straight in CURLY_MAP.items():
        fixed = fixed.replace(curly, straight)

    if fixed == frontmatter:
        return False

    path.write_text(fixed + body, encoding="utf-8")
    return True


if __name__ == "__main__":
    paths = [Path(p) for p in sys.argv[1:]] if len(sys.argv) > 1 else []
    if not paths:
        print("Usage: fix_frontmatter_quotes.py <file1.md> [file2.md ...]")
        sys.exit(1)

    for p in paths:
        if fix_file(p):
            print(f"FIXED: {p}")
        else:
            print(f"OK: {p}")
