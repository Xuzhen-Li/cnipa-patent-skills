---
name: "11-description-writer"
description: "Write the description (说明书) after both drawing gates pass. Control background admissions, generalization, support, enablement, effect evidence, and added-matter risk, then finalize the abstract. 用于以资深专利代理人的撰写和审查标准，在附图通过双重质量门后完成发明专利说明书，控制背景技术不当自认、概括层级、支持性、充分公开、技术效果证据和后续修改超范围风险，并按机械、电气、软件、方法、化学或生物领域要求完成摘要最终定稿。"
---

# 11-description-writer

## Purpose

Write a description (说明书) that supports the claims (权利要求书), that a person skilled in the art can carry out, and that matches the drawings which passed the check. This node does not only generate the five sections of the description. It also reviews the original disclosure, the claims, the description, the drawings, and the technical effects, and it finalizes the abstract (说明书摘要).

## Trigger and inputs

- Run after both the substantive gate and the formal gate of skill 10 have passed and the user has confirmed.
- When arriving directly from skill 03, there must be an equivalent record of both drawing gates. Otherwise return to skill 10. If the drawings or the fact baseline are not enough, return to skill 09.
- Read: the upstream handoff, the draft abstract from skill 07, the claims and dependency tree from skill 08, the passed drawing set and hashes from skill 10, the original technical facts and confirmation records from skills 04 and 06, the references and analysis from skill 05, and the part/step master and relationship matrix.

## Node directory and field rules

Create `patent-deliverables/11-description-writer/` and the seven standard subdirectories. The drawing copies from skill 10 are read-only. Do not modify them.

Before writing, read [references/领域化说明书审查基准.md](references/领域化说明书审查基准.md) and the English counterpart [references/领域化说明书审查基准.en.md](references/领域化说明书审查基准.en.md). Load the section that matches `drawing_route_type` and the technical subject. A mixed invention loads every relevant section.

## Drafting rules

- Start from technical facts that already existed before filing and that the inventor confirmed. A newly supplied fact may be added before filing, but the inventor's confirmation, the source, and the time must be saved. The model must not invent facts.
- Every claim feature must have a place in the description that states it expressly, or from which it can be determined directly and unambiguously. A broad generalization must be supported by enough embodiments and alternatives.
- Background art should be objective and accurate. Do not use "well known", "conventional", or "already solved" without evidence, and do not write a key feature of this invention as prior art the applicant admits.
- A technical effect must be tied to the specific technical feature that produces it and to the evidence status. Do not use unsupported absolutes such as "significant", "complete", or "thorough".
- Embodiments support and illustrate. Do not accidentally limit an independent claim to one size, material, shape, or working state.

## Steps

1. Lock the original-disclosure baseline, later inventor confirmations, the claim version, the fact-source version, and the drawing hashes from skill 10.
2. Build `original-disclosure-audit.json`. Mark each item to be written as originally recorded, confirmed as a pre-filing supplement, an attorney generalization, or unsupported. Unsupported content must not enter the text.
3. Write the title of the invention (发明名称) and the technical field (技术领域) so they match the subject protected by the independent claims.
4. Write the background art (背景技术): the closest prior art and its objective defects, citing references where needed. Run the improper-admission check on the background art.
5. Write the contents of the invention (发明内容): the technical problem, the technical solution, and the supported advantageous effects, in that order. The technical solution must at least cover the essential technical features of each independent claim and should present the dependent-claim layers in a reasonable way.
6. Write the brief description of the drawings (附图说明). Cite only the 3–7 figures that passed skill 10. Figure numbers, view types, marks, and state notes must match the pass list.
7. Write the specific embodiments (具体实施方式): structural or step relationships, working principle, operation, where parameters come from, alternatives, and the experiments or data that are needed, so a person skilled in the art can carry out the solutions the claims cover.
8. Check the special disclosure requirements for mechanical, electrical, software, method, chemical, or biological technology under the field rules. If materials are missing, write a supplement list. Do not hide the gap with boilerplate.
9. Build `claims-description-drawings-map.json` and `generalization-alternatives.json`. For each feature, record the paragraph, figure number, mark, embodiment, alternative, and fact source.
10. Review support, clarity, enablement (充分公开), unity, technical-effect evidence, and the risk that a later amendment would add matter (修改超范围). If a claim goes beyond the disclosure, do not invent support by expanding the text. Return to skill 08 or ask the inventor to confirm a supplement.
11. Using the final claims, the description, and the abstract figure selected by skill 10, revise the draft abstract from skill 07. Output a final abstract of at most 300 characters and run `python3 scripts/validate_final_abstract.py <abstract-final.md>`.
12. After the user confirms the description, the final abstract, and the risk list, hand off to skill 12 and stop.

## Required outputs

- `deliverables/description.md`
- `deliverables/brief-description-of-drawings.md`
- `deliverables/embodiment-points.json`
- `deliverables/original-disclosure-audit.json`
- `deliverables/background-admission-review.md`
- `deliverables/claims-description-drawings-map.json`
- `deliverables/generalization-alternatives.json`
- `deliverables/technical-effect-evidence.json`
- `deliverables/enablement-support-review.md`
- `deliverables/added-matter-risk-list.md`
- `deliverables/abstract-final.md`
- `deliverables/abstract-final-validation.json`
- `deliverables/drawing-usage-manifest.json`
- The three standard process records and `handoff/next-node-input.json`

## Final abstract rules

- The abstract from skill 07 is a draft. Do not pass it through unchanged by default.
- The final abstract must match the technical subject of the final independent claims, the core solution in the description, and the abstract figure. The body is at most 300 characters.
- The abstract must not add content the description does not contain, and it must not use promotional language or language that widens the scope.
- The abstract figure may use only the passed image designated by skill 10. Do not redraw it or generate another one.

## Handoff rules

The handoff must state:

- `current_skill=11-description-writer`
- `next_skill=12-patent-word-generator`
- Existing-materials and dynamic-routing fields, copied unchanged
- `specification_file`, `final_abstract_file`, `final_abstract_character_count`
- `claims_specification_drawing_mapping_file`, `original_disclosure_audit_file`
- `enablement_review_status`, `support_review_status`, `added_matter_risk_status`
- `background_admission_review_status`, `effect_evidence_status`
- `validated_figure_count` (3–7), `validated_figure_files`, `validated_figure_hashes`, `abstract_figure_file`
- `source_files`, `deliverables`, `open_questions`, `quality_gate_status`, `can_continue`, `must_stop_reason`

## Quality gate and stops

- Both drawing gates from skill 10 are `pass`, and the images in use match the hash list exactly.
- Each part of the description is complete. Do not aim for a fixed length. Aim to support the claims and to enable the invention.
- Every claim feature has a specific support location. The generalized scope has enough embodiments and alternatives.
- The background art (背景技术) has no clear improper admission. Technical effects have a feature and an evidence basis.
- The field-specific disclosure requirements are met. The final abstract is at most 300 characters and agrees with the full text and the drawings.
- Set `can_continue=false` when key implementation information, experiment or parameter basis, an inventor supplement, or a support location is missing.
- Do not repair a claim defect by inventing embodiments, parameters, alternatives, or effects. Do not edit a checked image to hide a contradiction with the text.
