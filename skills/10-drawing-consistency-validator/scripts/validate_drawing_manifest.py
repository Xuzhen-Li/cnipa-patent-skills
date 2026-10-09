#!/usr/bin/env python3
"""Validate normalized part identities across patent drawing views.

The script validates structured declarations only. A human/model must still inspect
the actual images as required by SKILL.md.
"""

import json
import sys
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def records(data, key):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        value = data.get(key, [])
        return value if isinstance(value, list) else []
    return []


def main():
    if len(sys.argv) != 3:
        print(
            "usage: validate_drawing_manifest.py "
            "<normalized-part-master.json> <observed-view-parts.json>",
            file=sys.stderr,
        )
        return 1
    master_data = load(sys.argv[1])
    view_data = load(sys.argv[2])
    master_parts = records(master_data, "parts")
    views = records(view_data, "views")
    errors = []
    if not 3 <= len(views) <= 7:
        errors.append(f"figure count must be 3-7, got {len(views)}")
    master = {}
    marks = set()
    for part in master_parts:
        pid = part.get("part_id")
        mark = str(part.get("drawing_mark", ""))
        name = part.get("standard_name")
        if not pid or not mark or not name:
            errors.append(f"incomplete master part: {part}")
            continue
        if pid in master:
            errors.append(f"duplicate part_id {pid}")
        if mark in marks:
            errors.append(f"duplicate drawing mark {mark}")
        master[pid] = part
        marks.add(mark)
    view_ids = set()
    for view in views:
        view_id = view.get("view_id", "UNKNOWN")
        if not view.get("view_id"):
            errors.append("view without view_id")
        elif view_id in view_ids:
            errors.append(f"duplicate view_id {view_id}")
        view_ids.add(view_id)
        seen = set()
        for item in view.get("parts", []):
            pid = item.get("part_id")
            if pid not in master:
                errors.append(f"{view_id}: unknown part_id {pid}")
                continue
            if pid in seen:
                errors.append(f"{view_id}: duplicate part_id {pid}")
            seen.add(pid)
            base = master[pid]
            for field in ("drawing_mark", "standard_name", "quantity"):
                if field in item and item[field] != base.get(field):
                    errors.append(
                        f"{view_id}/{pid}: {field}={item[field]!r} conflicts with master {base.get(field)!r}"
                    )
            stable = base.get("stable_attributes", {})
            observed = item.get("observed_attributes", {})
            not_observable = set(item.get("not_observable", []))
            reasons = item.get("not_observable_reasons", {})
            unknown_exclusions = not_observable - set(stable)
            if unknown_exclusions:
                errors.append(
                    f"{view_id}/{pid}: not_observable contains unknown stable attributes "
                    f"{sorted(unknown_exclusions)}"
                )
            for field in not_observable:
                reason = reasons.get(field, "")
                if not isinstance(reason, str) or not reason.strip():
                    errors.append(
                        f"{view_id}/{pid}: not_observable field {field} requires a specific reason"
                    )
            for field, expected in stable.items():
                if field in not_observable:
                    continue
                if field not in observed:
                    errors.append(f"{view_id}/{pid}: stable attribute {field} was not assessed")
                elif observed[field] != expected:
                    errors.append(
                        f"{view_id}/{pid}: stable attribute {field}={observed[field]!r} "
                        f"conflicts with master {expected!r}"
                    )
        required = set(view.get("required_part_ids", []))
        missing = required - seen
        if missing:
            errors.append(f"{view_id}: missing required parts {sorted(missing)}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {len(master)} master parts across {len(views)} views")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
