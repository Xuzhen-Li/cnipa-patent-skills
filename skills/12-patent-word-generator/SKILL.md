---
name: "12-patent-word-generator"
description: "Assemble the Word draft from the abstract, claims, description, and the 3–7 drawings that passed the image check. Also used when 03-invention-status-check finds that record complete. 用于汇总通过一致性校验的 3–7 张附图、摘要、权利要求书和说明书，生成发明专利 Word 终稿；也用于 03-invention-status-check 确认全部内容及附图校验记录完整后直接推荐终稿汇总。"
---

# 12-patent-word-generator

## Purpose

Produce the invention-patent Word draft and make sure every embedded image comes from the passed-drawing list of skill 10.

The working draft file is `patent-final.docx`. If the draft is also split into CNIPA filing documents, keep these Chinese filenames: `权利要求书.docx`, `说明书.docx`, `说明书摘要.docx`, `说明书附图.docx`, and the abstract figure `摘要附图`. Those filing names stay Chinese.

## When it runs

- Run after `11-description-writer` passes and the user confirms.
- Skill 03 may recommend this node directly from the materials assessment, but only when the full text, the three-way consistency record, and the actual-image drawing check are already complete.

## Required inputs

- The abstract (说明书摘要), the claims (权利要求书), the description (说明书), and the brief description of the drawings (附图说明).
- Skill 11's `handoff/next-node-input.json`, with `quality_gate_status=pass` and `can_continue=true`.
- Skill 10's passed-drawing list, image hashes, abstract-figure selection record, and `description-drawing-copies/`.
- The claims–description–drawings map.
- When entering from skill 03: that handoff and materials proving that all of the results above are complete, consistent with each other, and that the drawings passed the actual-image check.

## Direct entry from skill 03

- Skip skills 04–11 only when both `next_skill` and `recommended_start_skill` in the skill 03 handoff are this node.
- Check, item by item, the full text, the 3–7 drawings, the unified marks, the three-way consistency, and the actual-image check record.
- If the drawings were not verified, return to skill 10. If the description or the three-way map is incomplete, return to skill 11. If images or the structural baseline are missing, return to skill 09.
- When this node finishes, write `END`.

## Required node directory

```text
patent-deliverables/12-patent-word-generator/
  input/
  output/
  process-records/
  handoff/
  deliverables/
  stages/
  patent-files/
```

## Steps

1. Lock every text version and the image-hash list from skill 10.
2. Arrange the filing sections in invention-patent order: abstract (说明书摘要), abstract figure (摘要附图), claims (权利要求书), description (说明书), and drawing sheets (说明书附图).
3. The abstract figure uses only the passed image designated by skill 10. The description drawings are embedded only from `description-drawing-copies/`. Do not use other candidates and do not generate images again.
4. Before embedding each image, recompute its hash and compare it with the pass list. Stop if they differ.
5. Check figure-number order, the brief description of the drawings, marks, page breaks, equal-ratio scaling, and whether the scaled images can still be read.
6. Write the Word draft, the content manifest, and the items still awaiting a patent attorney.
7. Set `next_skill=END` in the handoff and stop.

## Required outputs

- `deliverables/patent-final.docx`
- `deliverables/final-content-manifest.md`
- `deliverables/attorney-review-items.md`
- `deliverables/final-drawing-hashes.json`
- `process-records/process-log.md`, `open-questions.md`, `quality-gate-record.md`
- `handoff/next-node-input.json`

## Handoff rules

`next-node-input.json` must include:

- `current_skill`: `12-patent-word-generator`
- `next_skill`: `END`
- Existing-materials and dynamic-routing fields, copied unchanged
- `validated_figure_count`: 3–7
- `validated_figure_files`, `validated_figure_hashes`, `abstract_figure_file`
- `embedded_figure_hashes`
- `source_files`, `deliverables`, `open_questions`
- `quality_gate_status`, `can_continue`, `must_stop_reason`

## Quality gate

- Skill 11 passed and the three-way map is complete, or the existing materials meet an equivalent standard.
- There are actually 3–7 drawings, all of them come from skill 10's pass list, and the hashes match before and after embedding.
- The abstract figure comes from that same passed set. There is no separately generated structural variant.
- Text order, figure numbers, marks, page breaks, and readability after scaling meet the draft requirements.
- State clearly that a patent attorney (专利代理师) still needs to review the draft.
- Directories, process records, and the `END` handoff are complete.

## Stop conditions

- Skill 11 did not pass, or the three-way consistency record is missing.
- The image count is outside 3–7, a hash does not match, a source is not on the pass list, or an unchecked image is present.
- Any required text is missing, or the text disagrees with the brief description of the drawings.
- A required input is incomplete.

## Do not

- Do not embed an image that skill 10 did not check. Do not regenerate, locally edit, or replace an image.
- Do not treat a simple paste-up as a finished quality check, and do not hide a contradiction between the text and the drawings.
- Do not start a new invention-patent node. Do not let the draft depend on spoken chat context.
