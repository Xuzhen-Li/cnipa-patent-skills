---
name: "09-patent-drawing-generator"
description: "Review the technical record, freeze one master, and plan 3–7 drawings. Generative images of physical devices are prototypes only; formal candidates come from traceable CAD, vector, or controlled engineering sources. 用于以资深专利代理人和专利制图审查标准，审查全部技术文本，按机械装置、电气系统、软件、流程、化学/生物或混合类型建立唯一事实源和统一制图母版，动态规划 3–7 张附图；实体装置的生成式图片仅可作为原型，正式候选图必须来自可追溯的确定性矢量、CAD或受控工程源。"
---

# 09-patent-drawing-generator

## Purpose

Treat the drawings (附图) as patent technical expression and as a consistency job for the legal documents, not as a standalone image-generation task. First lock the facts, the claims (权利要求书), the parts or steps, the marks (附图标记), and the relationships among views. Then output 3–7 formal candidate drawings that are structurally consistent, whose sources can be traced, and that skill 10 can review.

## Trigger and inputs

- Run after skill 08 finishes, when skill 03 recommends this node directly, or after skill 10 writes `retry_skill=09-patent-drawing-generator`.
- Read the direct upstream handoff, the user's materials from skill 02, every available result from skills 04–08, any existing description, sketches, photos, CAD, or dimension data, and any rework audit.
- When arriving directly from skill 03, both `next_skill` and `recommended_start_skill` must be this node, and the abstract and claims must be usable. If they are not, return to the earlier node.

Do not read only the abstract or the claims and then write a prompt. Conflicting facts must be confirmed by the inventor. The drawing node must not choose between them on its own.

## Node directory

Create `patent-deliverables/09-patent-drawing-generator/` and the seven standard subdirectories. Under `deliverables/`, also create `concept-prototypes/`, `deterministic-engineering-sources/`, and `candidate-drawings/`. User originals are read-only. Every version must keep its source and its hash.

## Drawing rules to read first

Read [references/分类型专利附图规范.md](references/分类型专利附图规范.md) and the English counterpart [references/分类型专利附图规范.en.md](references/分类型专利附图规范.en.md). Load only the section for the current invention type, plus the general form rules. A mixed invention loads every relevant section.

## Drawing-route split

Write `drawing_route_type` before any drawing starts:

- `mechanical_device`: machines, devices, physical structures.
- `electrical_circuit`: circuits, control systems, signal connections.
- `software_system`: software modules, data flow, computing architecture.
- `process_flow`: method steps, process flows, state changes.
- `chemical_biological`: chemical structures, reaction or preparation flows, biological experiments or systems.
- `mixed`: two or more of the above must be shown together.

Each type uses its own master: a physical-structure master, a circuit-topology master, a module/data-dictionary master, a flow-node and branch master, or a professional chemical drawing source. Do not force the mechanical-device rules onto every invention.

## Single fact source and master

1. After reading the whole record, build `technical-fact-source.json`, `part-or-step-master.json`, `structure-logic-matrix.json`, `motion-state-constraints.json`, and `drawing-mark-master.json`.
2. For each fact, record `fact_id`, the source file and location, confirmation status, related claims, and why it must be shown.
3. Give every part, module, or step one ID. Record its name, count, shape or symbol, connection or order, position or level, inputs and outputs, state, and stable attributes.
4. Finish the Figure 1 (图1) overall master and freeze it. Figures 2–7 must be derived from the same engineering source, topology, or logic master.
5. Allowed differences are only the planned viewpoint, occlusion, section, exploded spacing, partial enlargement, working state, or flow branch. Do not change identity, count, shape features, connections, installed position, orientation, inside/outside relationship, step order, or data direction.

## Planning 3–7 drawings

- The total must be 3–7, set by what the technology needs to show. Do not fix it at 3, and do not add duplicate figures to fill a number.
- For each figure, record what it expresses, which facts or claims it covers, why it is not replaceable, the view type, allowed changes, and forbidden changes.
- Do not add figures when 3 are enough to express the invention completely. If 7 are still not enough, stop and ask for more materials or professional drawing. Do not drop a necessary structure to stay inside the limit.
- The abstract figure (摘要附图) is chosen from the set that passes skill 10. Do not generate a separate structural variant.

## Formal drawing route

Priority: normalize and redraw from existing CAD or professional source files, then programmatic vector engineering drawings, then controlled edits of the frozen engineering source, then generative images as concept prototypes only.

- For a machine, a physical product, or a precise spatial structure, a generative image may be used only to discuss composition and viewpoint. It must not be a formal candidate.
- Formal candidates must be exported from CAD, an SVG or other vector program, a professional circuit, flow, or chemical drawing tool, or a reproducible controlled engineering source. Save the source file, the version, and the export parameters.
- No structure that appears only in a generative prototype may be written back into the fact source. Only the original disclosure and the inventor's confirmation can change the fact source.
- If the same class of prototype still drifts structurally for two rounds in a row, stop the generative route and ask for dimensions, sketches, photos, or engineering drawings.

## Steps

1. Decide the drawing type, review the facts in the full text, resolve conflicts, and build the master data.
2. Write `drawing-view-plan.json`, `cross-view-constraints.json`, and `drawing-form-spec.md`.
3. Make the Figure 1 overall master. Check it item by item against the facts, claims, parts or steps, marks, and technical relationships, and write `master-freeze-record.json`.
4. Make the figures one at a time from the view plan. Derive only one figure per pass. Keep the engineering source, export version, drawing rules, and fact trace for each figure.
5. Run this node's pre-check: structure or logic, relationships among figures, marks, form, readability when scaled, and whether the engineering source can be reproduced.
6. When the user draws in an external tool, say for each figure which master to use, what may change, what must not change, the file name, and the save path. When finished, ask for the reply `我已将全部候选附图放入指定文件夹`.
7. After checking that 3–7 images and the matching deterministic engineering sources actually exist, hand off to skill 10 and stop.

## Required outputs

- `deliverables/drawing-route-decision.md`
- `deliverables/technical-fact-source.json`
- `deliverables/part-or-step-master.json`
- `deliverables/structure-logic-matrix.json`
- `deliverables/motion-state-constraints.json`
- `deliverables/drawing-mark-master.json`
- `deliverables/drawing-view-plan.json`
- `deliverables/cross-view-constraints.json`
- `deliverables/drawing-form-spec.md`
- `deliverables/master-freeze-record.json`
- `deliverables/per-figure-drawing-spec.md`
- `deliverables/drawing-fact-trace.json`
- `deliverables/deterministic-source-manifest.json`
- `deliverables/candidate-drawing-manifest.json` and 3–7 actual images in `candidate-drawings/`
- The three standard process records and `handoff/next-node-input.json`

## Handoff rules

The handoff must state:

- `current_skill=09-patent-drawing-generator`
- `next_skill=10-drawing-consistency-validator`
- Existing-materials and dynamic-routing fields, copied unchanged
- `drawing_route_type`, `technical_fact_source_file`, `part_or_step_master_file`
- `relationship_matrix_file`, `view_plan_file`, `cross_view_constraints_file`
- `master_freeze_file`, `deterministic_source_manifest_file`
- `candidate_figure_count` (3–7), `candidate_figure_files`, `candidate_figure_hashes`
- `generative_prototypes_used`, `formal_candidates_are_deterministic`
- `source_files`, `deliverables`, `open_questions`, `quality_gate_status`, `can_continue`, `must_stop_reason`

## Quality gate and stops

- The drawing type, the single fact source, the overall master, the need for each of the 3–7 views, and the cross-view constraints are all confirmed.
- Every formal candidate of a physical device comes from a deterministic engineering source. Prototypes and formal figures stay in separate folders.
- Every formal figure has a reproducible source file, a version, a hash, and a trace to facts and claims.
- The pre-check passes for form rules, marks, section / detail / state definitions, and readability when scaled.
- Set `can_continue=false` when the master is not frozen, an engineering source is missing, the image count is out of range, a structural contradiction exists, or the user has not confirmed the candidates.
- Do not change the facts, the claims, or the description to fit a wrong figure. Do not skip skill 10.
