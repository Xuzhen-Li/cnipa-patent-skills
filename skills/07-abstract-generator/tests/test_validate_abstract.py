"""Smoke tests for the abstract character check."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_abstract.py"


def load():
    spec = importlib.util.spec_from_file_location("validate_abstract", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_body_skips_headings_markup_and_whitespace():
    body = load().abstract_body("# 标题\n\n甲 *乙* `丙`\n> 丁\n")
    assert body == "甲乙丙丁"


def test_cli_pass(tmp_path):
    path = tmp_path / "abstract-draft.md"
    path.write_text("一种短摘要。\n", encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload["pass"] is True
    assert payload["limit"] == 300
    assert payload["character_count"] == 6


def test_cli_over_limit(tmp_path):
    path = tmp_path / "abstract-draft.md"
    path.write_text("甲" * 301, encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1
    payload = json.loads(proc.stdout)
    assert payload == {"character_count": 301, "limit": 300, "pass": False}


def test_custom_limit(tmp_path):
    path = tmp_path / "abstract-draft.md"
    path.write_text("甲乙丙", encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(path), "2"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1
    assert json.loads(proc.stdout)["limit"] == 2


def test_usage_exit_code():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2
    assert "usage:" in proc.stderr
