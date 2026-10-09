"""Installer smoke tests. They never write outside pytest's temporary directory."""

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "install.sh"
SKILLS = [
    "01-patent-master-control",
    "02-patent-init",
    "03-invention-status-check",
    "04-patent-topic-selector",
    "05-patent-prior-art-search",
    "06-innovation-point-finder",
    "07-abstract-generator",
    "08-claims-writer",
    "09-patent-drawing-generator",
    "10-drawing-consistency-validator",
    "11-description-writer",
    "12-patent-word-generator",
]


def run(*args):
    return subprocess.run(
        ["bash", str(INSTALL), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_help():
    proc = run("-h")
    assert proc.returncode == 0
    assert "--target" in proc.stdout
    assert "project" in proc.stdout


def test_missing_target():
    proc = run()
    assert proc.returncode == 2


def test_dry_run_does_not_write(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    proc = run("--dry-run", "--target", "project", str(project), "--mode", "copy")
    assert proc.returncode == 0, proc.stderr
    assert "nothing written" in proc.stdout
    assert not (project / ".agents").exists()


def test_project_copy_keeps_other_skills(tmp_path):
    project = tmp_path / "project"
    other = project / ".agents" / "skills" / "other-skill"
    other.mkdir(parents=True)
    (other / "SKILL.md").write_text("keep\n", encoding="utf-8")
    proc = run("--target", "project", str(project), "--mode", "copy")
    assert proc.returncode == 0, proc.stderr
    dest = project / ".agents" / "skills"
    for name in SKILLS:
        assert (dest / name / "SKILL.md").is_file()
    assert (other / "SKILL.md").read_text(encoding="utf-8") == "keep\n"
    assert "12" in proc.stdout


def test_project_link(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    proc = run("--target", "project", str(project), "--mode", "link")
    assert proc.returncode == 0, proc.stderr
    link = project / ".agents" / "skills" / "01-patent-master-control"
    assert link.is_symlink()
    assert os.path.realpath(link) == os.path.realpath(ROOT / "skills" / "01-patent-master-control")


def test_missing_project_directory(tmp_path):
    missing = tmp_path / "missing"
    proc = run("--target", "project", str(missing))
    assert proc.returncode == 1
