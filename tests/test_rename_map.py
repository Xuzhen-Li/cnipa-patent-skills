"""Rename-map order and protected Chinese filing names."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "docs" / "apply_rename_map.py"


def load():
    spec = importlib.util.spec_from_file_location("apply_rename_map", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_self_test_cli():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--self-test"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "self-test ok" in proc.stdout


def test_map_file_matches_script_and_is_longest_first():
    module = load()
    document = json.loads((ROOT / "docs" / "rename_map.json").read_text(encoding="utf-8"))
    assert document["count"] == len(document["replacements"])
    assert document["count"] == len(module.replacement_rows())
    # --self-test no longer rewrites the file, so compare the whole content.
    assert document == json.loads(json.dumps(module.map_document(), ensure_ascii=False))
    lengths = [len(row["from"]) for row in document["replacements"]]
    assert lengths == sorted(lengths, reverse=True)
    protected = set(document["protected_filenames"])
    assert protected == {
        "权利要求书.docx",
        "说明书.docx",
        "说明书摘要.docx",
        "说明书附图.docx",
    }
    blob = "\n".join(protected) + "\n摘要附图\n"
    assert module.apply_replacements(blob) == blob
