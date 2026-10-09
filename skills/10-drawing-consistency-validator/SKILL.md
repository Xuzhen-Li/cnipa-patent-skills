---
name: "10-drawing-consistency-validator"
description: "Open each of the 3–7 candidate images and run the substantive consistency gate and the formal compliance gate, including mark checks, difference overlays, confidence, and hashes. 用于以独立专利附图审查视角打开并逐幅检查 3–7 张实际候选图，分别执行结构与逻辑实质一致性门、专利附图形式合规门，并通过 OCR/人工标号核验、差异叠加、观察置信度和哈希锁定阻断部件漂移、连接矛盾及形式缺陷。"
---

# 10-drawing-consistency-validator

## Purpose

Act as an independent quality gate. Review the actual images, not the prompts or the file names. The substantive consistency gate must pass first, then the formal compliance gate. If either gate fails, the description (说明书) must not start.

## Trigger and inputs

- Run after skill 09 has output 3–7 formal candidates and allowed the workflow to continue.
- Skill 03 may send the work here directly when the user already has 3–7 drawings that have not had an independent check of the actual images. If a reliable fact source, master, or engineering source cannot be rebuilt, return to skill 09.
- Read the upstream handoff, the candidate images, the deterministic-source manifest, the fact source, the part/step master, the relationship matrix, the state constraints, the claims, the view plan, the mark master, and the master-freeze record.

User original images are read-only. Stop immediately if there are fewer than 3 candidates, more than 7, or any image that cannot be opened.

## Node directory and review basis

Create `patent-deliverables/10-drawing-consistency-validator/` and the seven standard subdirectories. Under `deliverables/`, also create `difference-overlays/`, `issue-evidence-screenshots/`, and `description-drawing-copies/`.

Before review, read [references/附图双重质量门检查表.md](references/附图双重质量门检查表.md) and the English counterpart [references/附图双重质量门检查表.en.md](references/附图双重质量门检查表.en.md).

## Basic evidence

1. List every candidate. Record the file path, SHA-256, format, pixel size, color mode, engineering source, export version, and modification time.
2. Open each image at its original size with a visual image tool. Record the view type, direction, visible parts or steps, marks, connections, positions, and form problems. Do not pass any figure that was not actually opened.
3. For views that can be compared, make an outline or transparency difference overlay to help see part drift, scale anomalies, interface changes, and mark shifts. Do not subtract pixels mechanically across different viewpoints. Explain those with the master and the view definition.
4. Use OCR or image recognition to extract marks and necessary text, then have a person or the model look again. OCR is only supporting evidence. It does not replace visual confirmation.
5. Mark every observation `high`, `medium`, or `low`, with the reason. A key structure at `medium` or `low` must go to human review. Do not judge `pass` before that confirmation.

## First gate: substantive consistency

1. From the actual observations, build `cross-view-part-or-step-list.json`. Write visible stable attributes into `observed_attributes`. Write fields that truly cannot be judged because of a section, occlusion, or viewpoint into `not_observable`, with a specific reason.
2. Use skill 09's `part-or-step-master.json` and `drawing-mark-master.json` as read-only sources. In this node's `input/`, build `script-part-master.json`. That file must use the fields the script requires: a top-level `parts` array; each part has `part_id`, `drawing_mark`, `standard_name`, `quantity`, and a dictionary `stable_attributes`. The keys of `stable_attributes` must match the `observed_attributes` / `not_observable` keys in the cross-view list. Record the source files and the field mapping. Do not edit skill 09's original master.
3. Run:

```bash
python3 scripts/validate_drawing_manifest.py <script-part-master.json> <cross-view-part-or-step-list.json>
```

A script failure must not pass. A script pass does not replace visual review.

4. Check five layers: figure against fact source, figure against figure, figure against claims, marks against the master, and formal figures against the deterministic engineering source.
5. For a physical structure, check identity, count, shape, connection, installed position, orientation, inside/outside relationship, motion, and state. For a circuit, software system, or flow, check modules, ports, signals, data, steps, branches, order, and the actor that performs each step. For a chemical or biological figure, check structure, bond type, substitution position, and the reaction or experiment flow.
6. Accept only viewpoint, section, exploded, detail, and working-state differences that were declared in advance and that the fact source supports.

All of the following are hard failures: adding or removing a part or step without a basis, changing shape, mirroring a key structure, changing a connection, position drift, changing orientation or the inside/outside relationship, changing signal or step direction, a count that disagrees in the same state, one mark for several objects, or several marks for one object.

## Second gate: formal compliance

After the substantive gate passes, check:

- Figure numbers for the 3–7 drawings are continuous and the citations are complete. The abstract figure (摘要附图) comes from the same set.
- White background and black lines. Outlines and symbols are clear. No photographic look, color, grayscale rendering, shadow, gradient, or decorative background.
- Marks, leader lines, arrows, section symbols, detail enlargements, and state marks are clear and do not cover key structure.
- No unrelated text, promotional notes, or dimensions or scales without a basis. Necessary text uses the same terms as the description.
- The drawing is still readable when scaled to the application-page size. Page orientation, margins, multi-figure layout, and output sharpness meet the electronic-filing rules that currently apply.
- Every formal figure has a reproducible engineering source, and the exported image matches that source.

When a form rule has an uncertain version or interpretation, mark it for review by a practicing patent attorney. Do not guess `pass`.

## Judgment and rework

- `pass`: both gates pass, and every key observation is high confidence or has been confirmed by a person.
- `warning`: only a minor form problem that does not change the technical content. Until the warning is closed, `can_continue=false`.
- `fail`: any substantive contradiction, a key feature that cannot be read, an engineering source that does not match, or a serious form defect.

On failure, output the specific image, the problem location, the part or step ID, the fact ID, the claim, an evidence screenshot, and a directed correction. Write `next_skill=null`, `can_continue=false`, and `retry_skill=09-patent-drawing-generator`.

Any edit to a figure, including a change that only touches a mark, a leader line, the layout, or sharpness, must:

1. Produce a new version and a new hash. Do not overwrite the version already reviewed.
2. Re-check both gates on the full set of 3–7 figures.
3. Update the difference overlays, the OCR/mark record, and the pass list.

## Required outputs

- `deliverables/candidate-drawing-evidence.json`
- `deliverables/cross-view-part-or-step-list.json`
- `input/script-part-master.json`
- `deliverables/substantive-consistency-gate.json`
- `deliverables/formal-compliance-gate.json`
- `deliverables/ocr-manual-mark-review.json`
- `deliverables/observation-confidence-review.json`
- `deliverables/difference-overlay-analysis.md` and `difference-overlays/`
- `deliverables/drawing-consistency-audit.md`
- `deliverables/inconsistency-issues.md`
- `deliverables/validated-drawing-manifest.json`
- `deliverables/abstract-figure-selection.json`
- `deliverables/description-drawing-copies/`
- The three standard process records and `handoff/next-node-input.json`

## Release and handoff

Stop after the audit. Write the following into the handoff only when both gates are `pass`, every warning is closed, every key low-confidence item has been confirmed by a person, and the user has confirmed the audit:

- `current_skill=10-drawing-consistency-validator`
- `next_skill=11-description-writer`
- Existing-materials and dynamic-routing fields, copied unchanged
- `substantive_gate_status=pass`, `formal_gate_status=pass`
- `validated_figure_count` (3–7), `validated_figure_files`, `validated_figure_hashes`
- `abstract_figure_file`, `engineering_source_manifest_file`
- `ocr_review_status`, `human_review_status`, `unresolved_low_confidence_items=[]`
- `quality_gate_status=pass`, `can_continue=true`, `retry_allowed=false`

Do not run skill 11 in the same turn.

## Do not

- Do not check only the prompts, file names, logs, OCR, or the structured lists.
- Do not downgrade a structural contradiction to a form warning, and do not explain it away as "just a different viewpoint".
- Do not pass automatically while a person has not confirmed a key medium or low confidence observation.
- Do not copy an unchecked image, an image changed after the check, or an image whose hash does not match to skill 11 or skill 12.
