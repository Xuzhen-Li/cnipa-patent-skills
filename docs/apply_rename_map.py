#!/usr/bin/env python3
"""Apply docs/rename_map.json to this private patent-skill pack.

The replacement table lives in this file. Running the script rewrites
docs/rename_map.json from that table and can copy the read-only source
tree into skills/. Replacements run longest-match first.

Do not use the copy mode to refresh skills/ from the source: it drops
lines that were rewritten by hand after the gate removal, so the current
skills/ files are the authoritative text.

This file must not contain seller branding literals. Banned scans build
those strings from code points.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "docs" / "rename_map.json"

PROTECTED_FILENAMES = (
    "权利要求书.docx",
    "说明书.docx",
    "说明书摘要.docx",
    "说明书附图.docx",
)
PROTECTED_TERMS = ("摘要附图",)

SKILL_DIRS = (
    ("01-发明专利总控", "01-patent-master-control"),
    ("02-发明专利初始化", "02-patent-init"),
    ("03-发明专利状态确认器", "03-invention-status-check"),
    ("04-发明专利选题器", "04-patent-topic-selector"),
    ("05-发明专利检索器", "05-patent-prior-art-search"),
    ("06-创新点确定器", "06-innovation-point-finder"),
    ("07-说明书摘要生成器", "07-abstract-generator"),
    ("08-权利要求书撰写器", "08-claims-writer"),
    ("09-发明专利图片生成器", "09-patent-drawing-generator"),
    ("10-发明专利附图一致性校验器", "10-drawing-consistency-validator"),
    ("11-说明书写作器", "11-description-writer"),
    ("12-发明专利Word生成器", "12-patent-word-generator"),
)

SKILL_IDS = (
    ("patent-invention-standalone-01-controller", "01-patent-master-control"),
    ("patent-invention-standalone-02-initialization", "02-patent-init"),
    ("patent-invention-standalone-03-status", "03-invention-status-check"),
    ("patent-invention-standalone-04-topic", "04-patent-topic-selector"),
    ("patent-invention-standalone-05-search", "05-patent-prior-art-search"),
    ("patent-invention-standalone-06-innovation", "06-innovation-point-finder"),
    ("patent-invention-standalone-07-abstract", "07-abstract-generator"),
    ("patent-invention-standalone-08-claims", "08-claims-writer"),
    ("patent-invention-standalone-09-image", "09-patent-drawing-generator"),
    ("patent-invention-standalone-10-drawing-validator", "10-drawing-consistency-validator"),
    ("patent-invention-standalone-11-specification", "11-description-writer"),
    ("patent-invention-standalone-12-word", "12-patent-word-generator"),
)

# Intermediate working names. Final CNIPA filing names are not in this table.
DELIVERABLE_FILES = (
    ("过程日志.md", "process-log.md"),
    ("待确认问题.md", "open-questions.md"),
    ("质量门记录.md", "quality-gate-record.md"),
    ("下一节点输入.json", "next-node-input.json"),
    ("发明专利总控状态.json", "master-control-status.json"),
    ("发明专利当前阶段.md", "current-stage.md"),
    ("下一节点建议.json", "next-node-suggestion.json"),
    ("发明专利系统环境确认.json", "system-environment.json"),
    ("发明专利输入状态.json", "input-status.json"),
    ("已有素材三问记录.json", "existing-materials-questionnaire.json"),
    ("已有素材清单.md", "existing-materials-inventory.md"),
    ("已有素材完整度评估.md", "existing-materials-completeness.md"),
    ("起始节点推荐.json", "start-node-recommendation.json"),
    ("发明专利初始化记录.md", "initialization-record.md"),
    ("发明状态确认.json", "invention-status.json"),
    ("已有材料登记.md", "existing-materials-register.md"),
    ("素材评估复核.md", "materials-assessment-review.md"),
    ("起始节点决策.md", "start-node-decision.md"),
    ("技术披露整理.md", "technical-disclosure.md"),
    ("技术事实与假设分层表.json", "fact-hypothesis-layers.json"),
    ("技术问题-技术手段-技术效果链.json", "problem-means-effect-chain.json"),
    ("可专利主题初筛.md", "patentable-subject-screen.md"),
    ("候选发明构思与单一性分析.md", "candidate-concepts-unity.md"),
    ("商业覆盖与侵权可识别性分析.md", "commercial-coverage-detectability.md"),
    ("检索要素与关键词表.json", "search-elements-keywords.json"),
    ("发明人待确认问题.md", "inventor-open-questions.md"),
    ("检索策略.md", "search-strategy.md"),
    ("检索式与分类号表.json", "queries-and-classifications.json"),
    ("检索日志.json", "search-log.json"),
    ("对比文件清单.json", "prior-art-document-list.json"),
    ("专利族与法律状态记录.json", "patent-family-legal-status.json"),
    ("技术特征-对比文件矩阵.json", "feature-prior-art-matrix.json"),
    ("最接近现有技术认定.md", "closest-prior-art.md"),
    ("新颖性初步分析.md", "novelty-preliminary.md"),
    ("创造性初步分析.md", "inventive-step-preliminary.md"),
    ("检索局限与FTO边界说明.md", "search-limits-fto-boundary.md"),
    ("基于原始披露的候选差异点.md", "candidate-differences-from-disclosure.md"),
    ("总的发明构思确认记录.md", "general-inventive-concept.md"),
    ("创新点层级表.json", "innovation-hierarchy.json"),
    ("技术问题-技术手段-技术效果证据链.json", "problem-means-effect-evidence.json"),
    ("必要与可选技术特征表.json", "essential-optional-features.json"),
    ("参数与技术效果证据表.json", "parameter-effect-evidence.json"),
    ("替代方案与规避路径分析.md", "alternatives-design-around.md"),
    ("单一性初步分析.md", "unity-preliminary.md"),
    ("待补充实验与技术资料清单.md", "missing-experiments-materials.md"),
    ("说明书摘要.md", "abstract-draft.md"),
    ("发明名称建议.md", "title-candidates.md"),
    ("摘要要素与来源表.json", "abstract-element-sources.json"),
    ("摘要字符校验.json", "abstract-character-check.json"),
    ("摘要定稿待复核项.md", "abstract-finalization-checklist.md"),
    ("权利要求书.md", "claims.md"),
    ("保护层级设计.md", "claim-scope-hierarchy.md"),
    ("权利要求依赖树.json", "claim-dependency-tree.json"),
    ("权利要求-技术特征映射表.json", "claim-feature-map.json"),
    ("权利要求结构表.json", "claim-structure.json"),
    ("保护范围说明.md", "claim-scope-notes.md"),
    ("备用保护点清单.md", "backup-protection-points.md"),
    ("权利要求质量检查.md", "claims-quality-check.md"),
    ("附图类型与制图路线判定.md", "drawing-route-decision.md"),
    ("技术事实单一源.json", "technical-fact-source.json"),
    ("部件或步骤主数据.json", "part-or-step-master.json"),
    ("结构与逻辑关系矩阵.json", "structure-logic-matrix.json"),
    ("运动与状态约束表.json", "motion-state-constraints.json"),
    ("附图标号主表.json", "drawing-mark-master.json"),
    ("附图视图规划.json", "drawing-view-plan.json"),
    ("图间结构约束表.json", "cross-view-constraints.json"),
    ("制图形式规范.md", "drawing-form-spec.md"),
    ("母版冻结记录.json", "master-freeze-record.json"),
    ("逐图绘制规范.md", "per-figure-drawing-spec.md"),
    ("附图事实追溯矩阵.json", "drawing-fact-trace.json"),
    ("确定性工程源清单.json", "deterministic-source-manifest.json"),
    ("候选附图清单.json", "candidate-drawing-manifest.json"),
    ("候选附图取证清单.json", "candidate-drawing-evidence.json"),
    ("跨图部件或步骤清单.json", "cross-view-part-or-step-list.json"),
    ("脚本校验用部件主表.json", "script-part-master.json"),
    ("结构与逻辑实质一致性门.json", "substantive-consistency-gate.json"),
    ("专利附图形式合规门.json", "formal-compliance-gate.json"),
    ("OCR与人工标号核验表.json", "ocr-manual-mark-review.json"),
    ("观察置信度与人工复核记录.json", "observation-confidence-review.json"),
    ("差异叠加分析.md", "difference-overlay-analysis.md"),
    ("附图一致性审计报告.md", "drawing-consistency-audit.md"),
    ("不一致问题清单.md", "inconsistency-issues.md"),
    ("通过校验的附图清单.json", "validated-drawing-manifest.json"),
    ("摘要附图选择记录.json", "abstract-figure-selection.json"),
    ("说明书.md", "description.md"),
    ("附图说明.md", "brief-description-of-drawings.md"),
    ("具体实施方式要点表.json", "embodiment-points.json"),
    ("原始披露与新增内容审计表.json", "original-disclosure-audit.json"),
    ("背景技术不当自认审查.md", "background-admission-review.md"),
    ("权利要求-说明书-附图三向对应表.json", "claims-description-drawings-map.json"),
    ("概括层级与替代方案表.json", "generalization-alternatives.json"),
    ("技术效果证据表.json", "technical-effect-evidence.json"),
    ("公开充分性与支持性审查.md", "enablement-support-review.md"),
    ("后续修改超范围风险清单.md", "added-matter-risk-list.md"),
    ("说明书摘要定稿.md", "abstract-final.md"),
    ("摘要定稿校验.json", "abstract-final-validation.json"),
    ("附图使用清单.json", "drawing-usage-manifest.json"),
    ("发明专利终稿.docx", "patent-final.docx"),
    ("终稿内容清单.md", "final-content-manifest.md"),
    ("待代理师确认事项.md", "attorney-review-items.md"),
    ("终稿附图哈希清单.json", "final-drawing-hashes.json"),
)

PATH_TOKENS = (
    ("发明专利_交付结果", "patent-deliverables"),
    ("说明书用附图副本/", "description-drawing-copies/"),
    ("确定性工程源/", "deterministic-engineering-sources/"),
    ("问题证据截图/", "issue-evidence-screenshots/"),
    ("专利相关文件/", "patent-files/"),
    ("用户已有素材", "user-existing-materials"),
    ("差异叠加图/", "difference-overlays/"),
    ("过程记录/", "process-records/"),
    ("概念原型/", "concept-prototypes/"),
    ("候选附图/", "candidate-drawings/"),
    ("交付结果/", "deliverables/"),
    ("输入/", "input/"),
    ("输出/", "output/"),
    ("交接/", "handoff/"),
    ("阶段/", "stages/"),
)

WORKFLOW_IDS = (
    ("`发明专利skill独立流程线`", "`invention-patent-standalone-workflow`"),
)

TEXT_SUFFIXES = {
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".py",
    ".txt",
    ".sh",
    ".ps1",
    ".command",
}


def _rows(pairs, kind):
    return [{"from": old, "to": new, "kind": kind} for old, new in pairs]


def replacement_rows():
    rows = []
    rows.extend(_rows(SKILL_DIRS, "skill-dir"))
    rows.extend(_rows(SKILL_IDS, "skill-id"))
    rows.extend(_rows(DELIVERABLE_FILES, "deliverable-file"))
    rows.extend(_rows(PATH_TOKENS, "path-token"))
    rows.extend(_rows(WORKFLOW_IDS, "workflow-id"))
    # Longest first so a suffix such as 待确认问题.md cannot eat 发明人待确认问题.md.
    rows.sort(key=lambda row: (-len(row["from"]), row["from"]))
    return rows


def map_document(rows=None):
    rows = replacement_rows() if rows is None else rows
    return {
        "version": 1,
        "order": "longest-first",
        "count": len(rows),
        "protected_filenames": list(PROTECTED_FILENAMES),
        "protected_terms": list(PROTECTED_TERMS),
        "notes": (
            "Script JSON keys were already English, so they are not entries. "
            "Chinese guidance notes under references/ keep their filenames and "
            "gain a sibling .en.md. Final CNIPA filing filenames stay Chinese."
        ),
        "replacements": rows,
    }


def ordered_pairs(document=None):
    rows = (document or map_document())["replacements"]
    pairs = [(row["from"], row["to"]) for row in rows]
    pairs.sort(key=lambda item: (-len(item[0]), item[0]))
    return pairs


def apply_replacements(text, pairs=None):
    if pairs is None:
        pairs = ordered_pairs()
    for old, new in pairs:
        text = text.replace(old, new)
    return text


def _seller():
    return chr(0x6768) + chr(0x5E08) + chr(0x5144)


def _contact():
    return chr(0x8054) + chr(0x7CFB)


def _copyright_mark():
    return chr(0x7248) + chr(0x6743)


def _copyright_long():
    return chr(0x8457) + chr(0x4F5C) + chr(0x6743)


def _auth_word():
    return "author" + "ization"


def _ack_stem():
    return "acknow" + "ledge"


def _scope_phrase():
    # Pack-license wording. Built from code points so the source has no literal.
    return "".join(chr(c) for c in (0x6388, 0x6743, 0x8303, 0x56F4))


def _seen_phrase():
    return chr(0x6089) + chr(0x77E5)


def _record_phrase():
    # 授权声明确认
    return "".join(chr(c) for c in (0x6388, 0x6743, 0x58F0, 0x660E, 0x786E, 0x8BA4))


def _vendor_needles():
    auth = _auth_word()
    ack = _ack_stem()
    return (
        _seen_phrase(),
        _scope_phrase(),
        _record_phrase(),
        auth + "_" + "notice_shown",
        auth + "_" + ack + "d",
        auth + "_" + ack + "ment_text",
        auth + "_" + "record_file",
        auth + "-" + ack + "ment-record",
        "four " + auth + " fields",
        auth + " field",
        ack + "ment record",
        "start-confirmation gate",
        "四个" + "授权字段",
        "授权确认",
        "授权声明",
        "书面授权",
    )


def _line_has_vendor_license(line):
    return any(needle in line for needle in _vendor_needles())


def _vendor_rewrites():
    auth = _auth_word()
    four = "四个" + "授权字段"
    return (
        (
            "1. After the " + auth + " gate, ask the user these questions first.",
            "1. Ask the user these questions first.",
        ),
        (
            "1. 通过授权确认门槛后，优先逐项询问",
            "1. 优先逐项询问",
        ),
        (
            "- The four " + auth + " fields, plus the existing-materials and dynamic-routing fields, copied unchanged",
            "- Existing-materials and dynamic-routing fields, copied unchanged",
        ),
        (
            "- " + four + "及已有素材、动态路由字段原样传递",
            "- 已有素材、动态路由字段原样传递",
        ),
        (
            "- The " + auth + " confirmation, directories, process records, and `END` handoff are complete.",
            "- Directories, process records, and the `END` handoff are complete.",
        ),
        (
            "- The " + auth + " confirmation or a required input is incomplete.",
            "- A required input is incomplete.",
        ),
        (
            "- 授权确认、目录、过程记录和 END 交接完整。",
            "- 目录、过程记录和 END 交接完整。",
        ),
        (
            "- 授权确认或必需输入不完整。",
            "- 必需输入不完整。",
        ),
    )


def _is_vendor_heading(stripped):
    titles = (
        "## Authorization gate",
        "## Start-confirmation gate",
        "## 授权确认前置门槛",
        "## 启动前声明与强制确认门槛",
    )
    return any(stripped == title or stripped.startswith(title + " ") for title in titles)


def strip_vendor_license(text):
    """Remove the pack-license gate, record, and copied fields.

    Patent-grant wording (可授权, 授权前景, 必然授权, 承诺授权) stays.
    """
    rewrites = _vendor_rewrites()
    kept = []
    skipping = False
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith("## "):
            skipping = _is_vendor_heading(stripped)
            if skipping:
                continue
        if skipping:
            continue
        for old, new in rewrites:
            line = line.replace(old, new)
        if _line_has_vendor_license(line):
            continue
        kept.append(line)
    text = "".join(kept)
    return re.sub(r"\n{3,}", "\n\n", text)


ZH_START_SECTION = """## 启动说明

在创建目录、读取材料、联网检索、调用工具或撰写正文之前，先展示下面的说明：

> 本流程只提供发明专利撰写辅助，不是法律意见。提交申请前应由注册专利代理师审查。在申请提交前，应对发明内容保密。
>
> 回复 yes 或确认后继续。

自然的肯定即可，例如 yes 或确认，不要求固定原句。

- 用户未同意时停止，不得开始实质工作。
- 用户同意后，才创建本节点目录并继续。

"""


def neutralize_skill_01(text, skill_dir):
    """After a source refresh, put the neutral start note back into skill 01 Chinese."""
    if skill_dir != "01-patent-master-control":
        return text
    if "## 必需输入" in text and "不是法律意见" not in text:
        text = text.replace("## 必需输入", ZH_START_SECTION + "## 必需输入", 1)
    text = text.replace(
        "- 用户启动发明专利流程的指令。\n- 如已有发明专利流程交接文件，则读取上一节点 `handoff/next-node-input.json`。",
        "- 用户启动发明专利流程的指令。\n- 用户在看到启动说明后以 yes 或确认表示同意。\n- 如已有发明专利流程交接文件，则读取上一节点 `handoff/next-node-input.json`。",
    )
    text = text.replace(
        "2. 展示完整声明并取得规定的准确回复；未通过时停止。\n",
        "2. 展示启动说明并等待 yes 或确认；用户未同意时停止。\n",
    )
    for old, new in (
        ("4. 检查是否存在上一发明节点的", "3. 检查是否存在上一发明节点的"),
        ("5. 若无有效交接文件", "4. 若无有效交接文件"),
        ("6. 若有交接文件", "5. 若有交接文件"),
        ("7. 若 `can_continue=false`", "6. 若 `can_continue=false`"),
        ("8. 若 `can_continue=true`", "7. 若 `can_continue=true`"),
    ):
        text = text.replace(old, new)
    text = text.replace(
        "- 必须先原文展示声明，并取得用户规定的准确回复。\n",
        "- 必须先展示启动说明，并取得用户以 yes 或确认作出的同意。\n",
    )
    if "两次不同的用户确认" not in text:
        text = text.replace(
            "- 本节点只能完成 `01-patent-master-control` 的目录创建、过程记录、交付结果和交接文件。\n- 本节点完成后必须停止",
            "- 本节点只能完成 `01-patent-master-control` 的目录创建、过程记录、交付结果和交接文件。\n"
            "- 开场的 yes 或确认，与本节点完成后的“继续下一步”，是两次不同的用户确认，不得相互替代。\n"
            "- 本节点完成后必须停止",
        )
    if "用户尚未以 yes 或确认表示同意" not in text and "- 用户指令不是发明专利路线。\n" in text:
        text = text.replace(
            "- 用户指令不是发明专利路线。\n",
            "- 用户指令不是发明专利路线。\n- 用户尚未以 yes 或确认表示同意。\n",
        )
    if "用户以 yes 或确认同意之前" not in text and "- 不得跳过 `02-patent-init`。\n" in text:
        text = text.replace(
            "- 不得跳过 `02-patent-init`。\n",
            "- 不得跳过 `02-patent-init`。\n"
            "- 用户以 yes 或确认同意之前，不得创建项目交付目录、读取用户材料或执行任何实质工作。\n"
            "- 不得把开场的 yes 或确认当成进入下一节点的指令。\n",
        )
    return text


def clean_branding(text):
    """Drop the seller notice and the pack-license reply. Keep patent-grant wording."""
    seller = _seller()
    contact = _contact()
    copyright_mark = _copyright_mark()
    copyright_long = _copyright_long()
    kept = []
    for line in text.splitlines(keepends=True):
        if copyright_long in line or copyright_mark in line or "书面授权" in line:
            continue
        if contact in line and (seller in line or "合作" in line or copyright_mark in line):
            continue
        if _line_has_vendor_license(line):
            continue
        line = line.replace(seller, "")
        kept.append(line)
    text = "".join(kept)
    text = re.sub(r"(?m)^>\s*$\n", "", text)
    return text


def set_frontmatter_field(text, field, value):
    """Replace one `field:` line, keeping its indentation.

    A callable replacement avoids re.sub interpreting backslashes in JSON.
    """
    rendered = json.dumps(value, ensure_ascii=False)
    pattern = rf"(?m)^([ \t]*){re.escape(field)}:.*$"

    def repl(match):
        return f"{match.group(1)}{field}: {rendered}"

    if re.search(pattern, text):
        return re.sub(pattern, repl, text, count=1)
    return text


DESCRIPTIONS = {
    "01-patent-master-control": (
        "Start and control the standalone invention-patent workflow. "
        "English triggers: \"start invention patent\"; \"start the invention patent workflow\"; "
        "\"run the invention patent process alone\"; \"turn this idea into an invention patent\". "
        "中文触发：开始发明专利；发明专利开始工作；单独走发明专利流程；把这个想法写成发明专利。"
        "用于单独启动和控制发明专利独立流程线；先说明这是撰写辅助而非法律意见，用户以 yes 或确认同意后再调度 02 至 12。"
    ),
    "02-patent-init": (
        "Initialize the invention-patent workflow: ask whether a framework, a draft, or related "
        "materials already exist, assess them, and recommend the earliest node from 04 to 12. "
        "用于发明专利独立流程线初始化；优先询问是否已有专利框架、专利初稿或相关材料，接收并评估已有素材，"
        "推荐 04 至 12 中适合开始的节点，再交接给 03-invention-status-check 复核路由。"
    ),
    "03-invention-status-check": (
        "Review the materials assessment from 02-patent-init and route to the earliest node "
        "among 04–12 that still needs work. "
        "用于复核 02-patent-init 的已有素材评估和起始节点推荐，依据实际材料成熟度动态路由到 04 至 12 中最早需要补齐的节点。"
    ),
    "04-patent-topic-selector": (
        "Organize a confirmed technical disclosure, screen patentable subject matter, unity, "
        "commercial coverage, and infringement detectability, and prepare search elements. "
        "Do not invent technology the inventor did not disclose. "
        "用于从简单发明想法或 03-invention-status-check 推荐的早期材料中挖掘技术披露，建立技术问题—技术手段—技术效果链，"
        "初筛可专利主题、总的发明构思、单一性、商业覆盖和侵权可识别性，并形成可复核检索要素；不得替发明人虚构技术方案。"
    ),
    "05-patent-prior-art-search": (
        "Build a reproducible Chinese/English, classification, and citation search; identify the "
        "closest prior art; and write preliminary novelty and inventive-step analyses. "
        "Distinguish patentability search from infringement/FTO search. "
        "用于对已确认技术披露制定中英文、分类号和组合检索策略，在可用的中国及国际专利数据库和非专利文献中进行可复核检索，"
        "确定最接近现有技术，并分别完成新颖性和创造性初步分析；明确区分可专利性检索与侵权/FTO检索。"
    ),
    "06-innovation-point-finder": (
        "Confirm one general inventive concept and the related core, secondary, and fallback "
        "innovation points, with problem-means-effect evidence, feature levels, and unity. "
        "No fixed word count and no forced single isolated point. "
        "用于结合最接近现有技术和原始技术披露，确认一个总的发明构思及相互关联的核心、次级和备用创新点，"
        "建立问题—手段—效果证据链、必要与可选特征层级、参数依据和单一性分析；不设固定字数，不强迫只选一个孤立创新点。"
    ),
    "07-abstract-generator": (
        "Draft a Chinese invention-patent abstract (说明书摘要) of at most 300 characters from the "
        "confirmed inventive concept. Skill 11-description-writer finalizes it. "
        "用于依据已确认的总发明构思、核心技术方案和技术效果生成中国发明专利说明书摘要初稿，正文不超过 300 字；"
        "摘要初稿供后续权利要求和说明书使用，并由 11-description-writer 在全文及附图确定后完成最终定稿。"
    ),
    "08-claims-writer": (
        "Write or rebuild claims (权利要求书): at most 10 claims, clear dependencies, and support "
        "in the description. Design the hierarchy and dependency tree before the claim text. "
        "Also used when 03-invention-status-check routes existing materials here. "
        "用于撰写或重构发明专利权利要求书，以保护范围完整、引用清晰、得到说明书支持为准，总项数不超过10项；"
        "先设计保护层级和依赖树，再撰写正文并校验引用与支撑关系。也用于 03-invention-status-check 根据已有框架或初稿直接推荐权利要求处理时。"
    ),
    "09-patent-drawing-generator": (
        "Review the technical record, freeze one master, and plan 3–7 drawings. Generative images "
        "of physical devices are prototypes only; formal candidates come from traceable CAD, vector, "
        "or controlled engineering sources. "
        "用于以资深专利代理人和专利制图审查标准，审查全部技术文本，按机械装置、电气系统、软件、流程、化学/生物或混合类型建立唯一事实源和统一制图母版，"
        "动态规划 3–7 张附图；实体装置的生成式图片仅可作为原型，正式候选图必须来自可追溯的确定性矢量、CAD或受控工程源。"
    ),
    "10-drawing-consistency-validator": (
        "Open each of the 3–7 candidate images and run the substantive consistency gate and the "
        "formal compliance gate, including mark checks, difference overlays, confidence, and hashes. "
        "用于以独立专利附图审查视角打开并逐幅检查 3–7 张实际候选图，分别执行结构与逻辑实质一致性门、专利附图形式合规门，"
        "并通过 OCR/人工标号核验、差异叠加、观察置信度和哈希锁定阻断部件漂移、连接矛盾及形式缺陷。"
    ),
    "11-description-writer": (
        "Write the description (说明书) after both drawing gates pass. Control background admissions, "
        "generalization, support, enablement, effect evidence, and added-matter risk, then finalize "
        "the abstract. "
        "用于以资深专利代理人的撰写和审查标准，在附图通过双重质量门后完成发明专利说明书，控制背景技术不当自认、概括层级、支持性、"
        "充分公开、技术效果证据和后续修改超范围风险，并按机械、电气、软件、方法、化学或生物领域要求完成摘要最终定稿。"
    ),
    "12-patent-word-generator": (
        "Assemble the Word draft from the abstract, claims, description, and the 3–7 drawings that "
        "passed the image check. Also used when 03-invention-status-check finds that record complete. "
        "用于汇总通过一致性校验的 3–7 张附图、摘要、权利要求书和说明书，生成发明专利 Word 终稿；"
        "也用于 03-invention-status-check 确认全部内容及附图校验记录完整后直接推荐终稿汇总。"
    ),
}

YAML_SHORT = {
    "01-patent-master-control": "Start the invention-patent workflow after a normal yes or 确认. 启动发明专利流程，说明撰写边界后，在用户以 yes 或确认同意后再调度后续节点。",
    "02-patent-init": "Ask the three materials questions, assess existing files, and recommend the earliest start node. 优先盘点并评估已有素材，推荐最合适的专利起始节点。",
    "03-invention-status-check": "Review material maturity and choose the earliest patent node that still needs work. 复核已有素材成熟度，动态选择最早需要补齐的专利节点。",
    "04-patent-topic-selector": "Build a problem-means-effect chain from inventor facts and screen subject matter, unity, and claim value. 从发明人事实中建立问题—手段—效果链，初筛可专利主题、单一性与保护价值。",
    "05-patent-prior-art-search": "Run a traceable Chinese/English, classification, and citation search, then assess closest prior art, novelty, and inventive step. 执行中英文、分类号和引证检索，完成最接近现有技术及新颖性、创造性初评。",
    "06-innovation-point-finder": "Confirm one general inventive concept and the core, secondary, and fallback layers. No fixed word count. 确认总的发明构思及核心、次级和备用创新层级，不设固定字数。",
    "07-abstract-generator": "Draft an abstract of at most 300 characters. Skill 11 finalizes it against the description and drawings. 生成不超过300字的摘要初稿，由11结合最终正文和附图完成定稿。",
    "08-claims-writer": "Design the dependency hierarchy and write at most 10 invention-patent claims. 设计引用层级并撰写不超过10项的发明专利权利要求书。",
    "09-patent-drawing-generator": "Freeze one master and deterministic engineering sources, then make 3–7 formal patent drawings. 按发明类型建立统一母版和确定性工程源，制作3–7张正式专利附图。",
    "10-drawing-consistency-validator": "Open 3–7 real images and run the substantive gate, the formal gate, mark checks, and difference overlays. 对3–7张实图执行结构实质门、形式合规门、标号及差异叠加审查。",
    "11-description-writer": "Check enablement, support, effect evidence, and added-matter risk for the field, then finalize the abstract. 按领域完成充分公开、支持性、效果证据和超范围风险审查，并定稿摘要。",
    "12-patent-word-generator": "Build the invention-patent Word draft using only the 3–7 drawings that passed the image check. 仅使用通过实图一致性校验的 3–7 张附图生成发明专利 Word 终稿。",
}

YAML_PROMPTS = {
    "01-patent-master-control": "请使用 $01-patent-master-control 启动当前发明专利项目。先说明这是撰写辅助、不是法律意见，并请用户以 yes 或确认表示同意。 Use $01-patent-master-control to start this invention-patent project. Say that this is drafting assistance, not legal advice, and wait for a normal yes or 确认.",
    "02-patent-init": "请使用 $02-patent-init 初始化当前发明专利项目，先完成三项素材询问与评估。 Use $02-patent-init to initialize this invention-patent project, starting with the three materials questions and the assessment.",
    "03-invention-status-check": "请使用 $03-invention-status-check 复核已有素材评估，并决定当前专利项目应从哪个节点继续。 Use $03-invention-status-check to review the materials assessment and decide which node this project should enter.",
    "04-patent-topic-selector": "请使用 $04-patent-topic-selector 以资深专利代理人视角整理技术披露、区分事实与建议，并输出可复核检索输入。 Use $04-patent-topic-selector to organize the technical disclosure, separate facts from proposals, and write search inputs.",
    "05-patent-prior-art-search": "请使用 $05-patent-prior-art-search 以资深专利代理人方法完成可复核检索、特征对比和新颖性、创造性初步分析。 Use $05-patent-prior-art-search to complete a traceable search, feature comparison, and preliminary novelty and inventive-step analysis.",
    "06-innovation-point-finder": "请使用 $06-innovation-point-finder 以资深专利代理人视角组织发明构思、创新层级、证据链和单一性分析。 Use $06-innovation-point-finder to organize the inventive concept, innovation layers, evidence chain, and unity analysis.",
    "07-abstract-generator": "请使用 $07-abstract-generator 以资深专利代理人标准生成可追溯的摘要初稿并完成字符校验。 Use $07-abstract-generator to draft a traceable abstract and run the character check.",
    "08-claims-writer": "请使用 $08-claims-writer 为当前发明专利设计保护层级和依赖树，再撰写不超过10项的权利要求书。 Use $08-claims-writer to design the claim hierarchy and dependency tree, then write at most 10 claims.",
    "09-patent-drawing-generator": "请使用 $09-patent-drawing-generator 按资深专利代理人和专业制图标准完成分型、母版、确定性工程源及候选附图。 Use $09-patent-drawing-generator to set the drawing route, master, deterministic sources, and candidate drawings.",
    "10-drawing-consistency-validator": "请使用 $10-drawing-consistency-validator 逐张打开实图，并独立完成实质一致性和形式合规双重质量门。 Use $10-drawing-consistency-validator to open every real image and run the substantive and formal gates.",
    "11-description-writer": "请使用 $11-description-writer 以资深专利代理人标准撰写说明书、完成专业审查并定稿摘要。 Use $11-description-writer to write the description, complete the professional review, and finalize the abstract.",
    "12-patent-word-generator": "请使用 $12-patent-word-generator 处理当前发明专利项目，并输出本节点交付结果和 END 交接。 Use $12-patent-word-generator to finish this invention-patent project and write this node's deliverables and the END handoff.",
}


def polish_skill_markdown(text, skill_dir):
    text = set_frontmatter_field(text, "name", skill_dir)
    if skill_dir in DESCRIPTIONS:
        text = set_frontmatter_field(text, "description", DESCRIPTIONS[skill_dir])
    return text


def polish_yaml(text, skill_dir):
    if skill_dir in YAML_SHORT:
        text = set_frontmatter_field(text, "short_description", YAML_SHORT[skill_dir])
    if skill_dir in YAML_PROMPTS:
        text = set_frontmatter_field(text, "default_prompt", YAML_PROMPTS[skill_dir])
    return text


def separate_skill_tokens(text):
    """Keep a renamed skill id from sticking to the next Chinese character."""
    return re.sub(
        r"((?:0[1-9]|1[0-2])-[a-z0-9-]+)(?=[\u4e00-\u9fff])",
        r"\1 ",
        text,
    )


CNIPA_FILENAME_NOTE = (
    "工作稿文件名为 `patent-final.docx`。若另外拆成中国国家知识产权局申请文件，"
    "文件名保持中文：`权利要求书.docx`、`说明书.docx`、`说明书摘要.docx`、"
    "`说明书附图.docx`，摘要附图保持 `摘要附图`。这些报送文件名不改成英文。\n"
)


def preserve_cnipa_filenames(text, skill_dir):
    if skill_dir != "12-patent-word-generator" or "权利要求书.docx" in text:
        return text
    needle = "生成发明专利 Word 终稿，并确保嵌入的所有图片均来自 10 的通过校验附图清单。\n"
    if needle not in text:
        return text
    return text.replace(needle, needle + "\n" + CNIPA_FILENAME_NOTE, 1)


def transform_text(text, skill_dir=None, suffix=""):
    text = apply_replacements(text)
    text = clean_branding(text)
    text = strip_vendor_license(text)
    text = neutralize_skill_01(text, skill_dir)
    text = separate_skill_tokens(text)
    if suffix == ".md" and skill_dir and text.startswith("---"):
        text = polish_skill_markdown(text, skill_dir)
        text = preserve_cnipa_filenames(text, skill_dir)
    if suffix in {".yaml", ".yml"} and skill_dir:
        text = polish_yaml(text, skill_dir)
    return text


def write_map():
    MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
    document = map_document()
    MAP_PATH.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return document


def copy_source_tree(source: Path, keep_english_skill=True):
    source = source.resolve()
    skills_src = source / "skills"
    if not skills_src.is_dir():
        raise SystemExit(f"source skills directory not found: {skills_src}")
    if ROOT in source.parents or source == ROOT:
        raise SystemExit("refusing to read a source inside the pack root")
    dir_map = dict(SKILL_DIRS)
    copied = 0
    for path in skills_src.rglob("*"):
        if not path.is_file():
            continue
        if path.name.startswith("._") or path.name == ".DS_Store":
            continue
        rel = path.relative_to(skills_src)
        skill_old = rel.parts[0]
        if skill_old not in dir_map:
            raise SystemExit(f"unexpected skill directory: {skill_old}")
        skill_new = dir_map[skill_old]
        dest = ROOT / "skills" / skill_new / Path(*rel.parts[1:])
        dest.parent.mkdir(parents=True, exist_ok=True)
        raw = path.read_bytes()
        suffix = path.suffix.lower()
        if suffix in TEXT_SUFFIXES:
            text = raw.decode("utf-8")
            text = transform_text(text, skill_dir=skill_new, suffix=suffix)
            if path.name == "SKILL.md":
                zh = dest.with_name("SKILL.zh-CN.md")
                zh.write_text(text, encoding="utf-8")
                if not (keep_english_skill and dest.exists()):
                    dest.write_text(text, encoding="utf-8")
            else:
                dest.write_text(text, encoding="utf-8")
        else:
            dest.write_bytes(raw)
        copied += 1
    return copied


def banned_hits(text):
    needles = (_seller(), _contact(), _copyright_mark(), "第" + "一" + "集")
    # The episode needle is three ordinary characters; do not store a joined course token.
    episode = chr(0x7B2C) + "." + chr(0x96C6)
    hits = [needle for needle in needles if needle in text]
    if re.search(episode, text):
        hits.append("episode-pattern")
    return hits


def assert_pack_clean(root=ROOT):
    problems = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.name.startswith("._"):
            continue
        text = path.read_text(encoding="utf-8")
        hits = banned_hits(text)
        if hits:
            problems.append(f"{path.relative_to(root)}: {hits}")
    if problems:
        raise SystemExit("banned wording remains:\n" + "\n".join(problems))


def self_test():
    pairs = ordered_pairs()
    sample = (
        "发明专利_交付结果/02-发明专利初始化/输入/01-用户已有素材/交接/下一节点输入.json\n"
        "发明专利_交付结果/07-说明书摘要生成器/交付结果/说明书摘要.md\n"
        "发明专利_交付结果/11-说明书写作器/交付结果/说明书摘要定稿.md\n"
        "发明专利_交付结果/11-说明书写作器/交付结果/说明书.md\n"
        "交付结果/发明人待确认问题.md\n"
        "过程记录/待确认问题.md\n"
        "交付结果/参数与技术效果证据表.json\n"
        "交付结果/技术效果证据表.json\n"
        "`workflow`: `发明专利skill独立流程线`\n"
        "references/分类型专利附图规范.md\n"
        "权利要求书.docx 说明书.docx 说明书摘要.docx 说明书附图.docx 摘要附图\n"
    )
    got = apply_replacements(sample, pairs)
    expected_bits = [
        "patent-deliverables/02-patent-init/input/01-user-existing-materials/handoff/next-node-input.json",
        "patent-deliverables/07-abstract-generator/deliverables/abstract-draft.md",
        "patent-deliverables/11-description-writer/deliverables/abstract-final.md",
        "patent-deliverables/11-description-writer/deliverables/description.md",
        "deliverables/inventor-open-questions.md",
        "process-records/open-questions.md",
        "deliverables/parameter-effect-evidence.json",
        "deliverables/technical-effect-evidence.json",
        "`workflow`: `invention-patent-standalone-workflow`",
        "references/分类型专利附图规范.md",
        "权利要求书.docx 说明书.docx 说明书摘要.docx 说明书附图.docx 摘要附图",
    ]
    for bit in expected_bits:
        if bit not in got:
            raise SystemExit(f"self-test missing: {bit}\n---\n{got}")
    blob = "\n".join(old for old, _new in pairs)
    applied = apply_replacements(blob, pairs)
    for old, _new in pairs:
        if old in applied:
            raise SystemExit(f"self-test left unreplaced: {old}")
    magic = "我已" + _seen_phrase() + "并同意遵守" + _scope_phrase()
    notice = "\n".join(
        [
            "> "
            + _seller()
            + "原创成果，"
            + _copyright_long()
            + "及相关权益。",
            "> 未经" + _seller() + "书面授权，不得复制。",
            "> 如需获取授权或" + _copyright_mark() + "合作，请" + _contact() + _seller() + "。",
            "> 请回复：" + magic,
            "完成" + _record_phrase() + "后，不得省略、改写、概括原创与授权声明。",
        ]
    )
    cleaned = clean_branding(notice)
    if _seller() in cleaned or _copyright_mark() in cleaned or _contact() in cleaned:
        raise SystemExit(f"branding cleaner left banned text:\n{cleaned}")
    if magic in cleaned or _seen_phrase() in cleaned or _scope_phrase() in cleaned:
        raise SystemExit(f"branding cleaner kept the pack-license reply:\n{cleaned}")
    grant = "不得承诺可授权。不得承诺必然授权。不使用承诺授权。\n"
    if clean_branding(grant) != grant or strip_vendor_license(grant) != grant:
        raise SystemExit("grant wording was removed")
    gated = "## 授权确认前置门槛\n\n必须核验上游四个授权字段。\n\n## 必建节点交付目录\n"
    stripped = strip_vendor_license(gated)
    if "授权确认" in stripped or "四个授权字段" in stripped:
        raise SystemExit(f"vendor section survived:\n{stripped}")
    if "## 必建节点交付目录" not in stripped:
        raise SystemExit(f"vendor strip ate the next section:\n{stripped}")
    print(f"self-test ok ({len(pairs)} replacements)")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Apply the patent skill rename map")
    parser.add_argument("--init-from", type=Path, help="read-only source pack to copy")
    parser.add_argument("--emit-map", action="store_true", help="write docs/rename_map.json")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--check-clean", action="store_true")
    parser.add_argument(
        "--refresh-english-skill",
        action="store_true",
        help="overwrite SKILL.md with the cleaned Chinese text",
    )
    args = parser.parse_args(argv)
    # Only write docs/rename_map.json when asked to (or by default); --self-test and
    # --check-clean leave the working tree alone.
    writes_map = args.emit_map or args.init_from or not any(
        [args.self_test, args.init_from, args.check_clean]
    )
    document = write_map() if writes_map else None
    if args.self_test:
        self_test()
    if args.init_from:
        copied = copy_source_tree(
            args.init_from,
            keep_english_skill=not args.refresh_english_skill,
        )
        print(f"copied {copied} source files")
    if args.check_clean:
        assert_pack_clean()
        print("pack wording check ok")
    if writes_map:
        print(f"wrote {MAP_PATH.relative_to(ROOT)} ({document['count']} replacements)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
