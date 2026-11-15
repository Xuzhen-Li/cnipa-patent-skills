"""Pack integrity: skill names, local links, and banned wording."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".sh", ".ps1", ".txt"}

EXPECTED = [
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


def _seller():
    return chr(0x6768) + chr(0x5E08) + chr(0x5144)


def _contact():
    return chr(0x8054) + chr(0x7CFB)


def _copyright_mark():
    return chr(0x7248) + chr(0x6743)


def test_twelve_chinese_skills():
    found = sorted(path.name for path in SKILLS.iterdir() if path.is_dir())
    assert found == EXPECTED
    for name in EXPECTED:
        skill = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
        assert f'name: "{name}"' in skill
        assert not (SKILLS / name / "SKILL.zh-CN.md").exists()
        description = re.search(r'^description: "(.*)"$', skill, re.M).group(1)
        assert re.match(r"[\u4e00-\u9fff]", description), name
        if name == "01-patent-master-control":
            for trigger in (
                "开始发明专利",
                "发明专利开始工作",
                "单独走发明专利流程",
                "把这个想法写成发明专利",
            ):
                assert trigger in description


def test_guidance_is_chinese_only():
    pairs = [
        SKILLS / "09-patent-drawing-generator/references/分类型专利附图规范.md",
        SKILLS / "10-drawing-consistency-validator/references/附图双重质量门检查表.md",
        SKILLS / "11-description-writer/references/领域化说明书审查基准.md",
    ]
    for path in pairs:
        assert path.is_file()
        assert not path.with_name(path.name.replace(".md", ".en.md")).exists()


def test_local_links_and_script_paths_exist():
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    script_re = re.compile(r"python3 (scripts/\S+)")
    for path in SKILLS.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in link_re.findall(text):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (path.parent / target).resolve()
            assert resolved.is_file(), f"{path} -> {target}"
        for target in script_re.findall(text):
            script = target.strip("<>")
            # The command is relative to the skill directory, not the markdown file.
            skill_dir = path.parent if path.parent.name != "references" else path.parent.parent
            if path.name.startswith("SKILL"):
                skill_dir = path.parent
            assert (skill_dir / script).is_file(), f"{path} -> {script}"


def test_skill_identifiers_exist():
    known = set(EXPECTED) | {"END", "null"}
    field_re = re.compile(
        r"(?:current_skill|next_skill|recommended_start_skill|retry_skill|"
        r"finalization_required_at_skill|routing_origin_skill)"
        r"(?:=|:)\s*`?([0-9]{2}-[a-z0-9-]+|END|null)`?"
    )
    token_re = re.compile(r"\b\d{2}-[a-z0-9-]+\b")
    for path in SKILLS.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        if path.suffix.lower() == ".md":
            for match in field_re.findall(text):
                assert match in known, f"{path} references {match}"
        for token in token_re.findall(text):
            assert token in known or token.endswith("-user-existing-materials"), (
                f"{path} unknown skill token {token}"
            )


def test_runtime_output_root_is_named():
    """Delivery paths are runtime outputs; the pack documents the root."""
    blob = "\n".join(
        path.read_text(encoding="utf-8")
        for path in SKILLS.rglob("SKILL.md")
    )
    assert "patent-deliverables/" in blob
    assert "handoff/next-node-input.json" in blob


def test_banned_wording_absent():
    episode = re.compile(chr(0x7B2C) + "." + chr(0x96C6))
    needles = (_seller(), _contact(), _copyright_mark())
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.name.startswith("._"):
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            assert needle not in text, path
        assert episode.search(text) is None, path


def test_old_frontmatter_ids_are_gone_from_skills():
    old_ids = [
        "patent-invention-standalone-01-controller",
        "patent-invention-standalone-12-word",
    ]
    blob = "\n".join(path.read_text(encoding="utf-8") for path in SKILLS.rglob("*") if path.is_file())
    for old in old_ids:
        assert old not in blob
    # The historical names live only in the rename map.
    raw = (ROOT / "docs" / "rename_map.json").read_text(encoding="utf-8")
    document = json.loads(raw)
    assert document["count"] == len(document["replacements"])
    assert ("author" + "ization-" + "acknow" + "ledgement-record.md") not in raw


def test_vendor_license_gate_is_gone_and_patent_grant_wording_stays():
    seen = chr(0x6089) + chr(0x77E5)
    scope = "".join(chr(c) for c in (0x6388, 0x6743, 0x8303, 0x56F4))
    rg_needles = (
        seen,
        scope,
        "我已" + seen + "并同意遵守" + scope,
        "author" + "ization field",
        "license " + "scope",
        "acknow" + "ledg",
    )
    extra = (
        "四个" + "授权字段",
        "授权确认字段",
        "授权声" + "明确认",
        "授权确认门槛",
        "授权确认前置",
    )
    # The rename script and this test name the old phrases so they can reject them.
    helper_names = {"apply_rename_map.py", "test_pack_integrity.py"}
    offenders = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.name.startswith("._"):
            continue
        text = path.read_text(encoding="utf-8")
        needles = rg_needles if path.name in helper_names else rg_needles + extra
        for needle in needles:
            if needle in text:
                offenders.append(f"{path.relative_to(ROOT)}: {needle}")
    assert offenders == []
    assert "必然授权" in (SKILLS / "05-patent-prior-art-search/SKILL.md").read_text(encoding="utf-8")
    assert "不得承诺可授权" in (SKILLS / "04-patent-topic-selector/SKILL.md").read_text(encoding="utf-8")
    assert "承诺授权" in (SKILLS / "07-abstract-generator/SKILL.md").read_text(encoding="utf-8")
    assert "不是法律意见" in (SKILLS / "01-patent-master-control/SKILL.md").read_text(encoding="utf-8")
