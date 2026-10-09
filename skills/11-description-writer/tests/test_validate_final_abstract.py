"""Smoke tests for the final abstract character check."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_final_abstract.py"


def load():
    spec = importlib.util.spec_from_file_location("validate_final_abstract", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_body_matches_draft_rules():
    assert load().abstract_body("# 标题\n\n甲 乙\n") == "甲乙"


def test_cli_pass_at_300(tmp_path):
    path = tmp_path / "abstract-final.md"
    path.write_text("甲" * 300, encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert json.loads(proc.stdout)["pass"] is True


def test_cli_fail_over_300(tmp_path):
    path = tmp_path / "abstract-final.md"
    path.write_text("甲" * 301, encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1
    payload = json.loads(proc.stdout)
    assert payload["limit"] == 300
    assert payload["pass"] is False


def test_usage_rejects_extra_limit(tmp_path):
    path = tmp_path / "abstract-final.md"
    path.write_text("甲", encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(path), "300"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2
    assert "usage:" in proc.stderr
