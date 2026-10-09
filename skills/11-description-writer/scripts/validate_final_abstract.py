#!/usr/bin/env python3
"""Check the non-whitespace length of a final Markdown patent abstract."""

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
    return re.sub(r"\s+", "", re.sub(r"[`*_>]", "", "".join(lines)))


def main():
    if len(sys.argv) != 2:
        print("usage: validate_final_abstract.py <abstract.md>", file=sys.stderr)
        return 2
    body = abstract_body(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = {"character_count": len(body), "limit": 300, "pass": len(body) <= 300}
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
