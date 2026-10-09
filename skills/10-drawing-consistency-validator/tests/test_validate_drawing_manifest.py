"""Smoke tests for the drawing-manifest validator."""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_drawing_manifest.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run(*names):
    args = [sys.executable, str(SCRIPT)]
    args.extend(str(FIXTURES / name) for name in names)
    return subprocess.run(args, capture_output=True, text=True, check=False)


def test_consistent_views_pass():
    proc = run("part-master.json", "consistent-views.json")
    assert proc.returncode == 0
    assert "PASS: 2 master parts across 3 views" in proc.stdout


def test_contradictory_views_fail():
    proc = run("part-master.json", "contradictory-views.json")
    assert proc.returncode == 1
    assert "conflicts with master" in proc.stderr
    assert "P2" in proc.stderr


def test_declared_section_and_exploded_views_pass():
    proc = run("part-master.json", "declared-section-views.json")
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.startswith("PASS:")


def test_usage_exit_code():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1
    assert "usage:" in proc.stderr
