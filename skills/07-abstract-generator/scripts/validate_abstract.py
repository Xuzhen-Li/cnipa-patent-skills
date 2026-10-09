#!/usr/bin/env python3
"""Check the non-whitespace length of a Markdown patent abstract body."""

import json
import re
import sys
from pathlib import Path


def abstract_body(text):
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        lines.append(stripped)
    body = "".join(lines)
    body = re.sub(r"[`*_>]", "", body)
    return re.sub(r"\s+", "", body)


def main():
    if len(sys.argv) not in (2, 3):
        print("usage: validate_abstract.py <abstract.md> [limit]", file=sys.stderr)
        return 2
    limit = int(sys.argv[2]) if len(sys.argv) == 3 else 300
    body = abstract_body(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = {"character_count": len(body), "limit": limit, "pass": len(body) <= limit}
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
