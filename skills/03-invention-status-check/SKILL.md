---
name: "03-invention-status-check"
description: "Review the materials assessment from 02-patent-init and route to the earliest node among 04–12 that still needs work. 用于复核 02-patent-init 的已有素材评估和起始节点推荐，依据实际材料成熟度动态路由到 04 至 12 中最早需要补齐的节点。"
---

# 03-invention-status-check

## Purpose

Review how mature the existing materials actually are, independently choose the earliest node that still needs work, and route to one of nodes 04 through 12.

## When it runs

Run after `02-patent-init` finishes.

## Required inputs

- `patent-deliverables/02-patent-init/handoff/next-node-input.json`.
- The three-question record, materials inventory, completeness assessment, and start-node recommendation produced by skill 02.
- The user's existing-materials directory, or null when all three answers were no.

## Required node directory

Before substantive work, create this directory in the current patent project. The directory name must match this skill name. Do not add a project-number level.

```text
patent-deliverables/03-invention-status-check/
  input/
  output/
  process-records/
  handoff/
  deliverables/
  stages/
  patent-files/
```

Process records, stage files, patent text, drawings, intermediate Word files, and other patent files from this node stay inside this directory. Do not also create `stages/`, `process-records/`, or `patent-files/` at the project root.

## Steps

1. Read skill 02's three-question record, materials directory, file-by-file inventory, readiness assessment for nodes 04–12, recommended node, and reasons.
2. If the user claims any class of materials, check that the directory exists, that the user confirmed the files were placed, and that every file cited by the assessment really exists. Do not merely repeat what the user said.
3. Re-check each prerequisite using skill 02's start-node rules, and choose the lowest-numbered node that still needs work. For drawings, separately check whether the actual count is 3–7, whether a structural master and fact baseline exist, and whether there is a per-image pass record. Having image files is not the same as having passed skill 10.
4. If this review disagrees with skill 02, follow the conclusion with the stronger evidence and explain each change in `start-node-decision.md`.
5. Do not ask the user to pick the start node. Show the recommended node, usable materials, gaps, reasons, and the route that follows.
6. Set `next_skill` to the final recommended node from `04` through `12`, write the handoff, and stop. Do not run the recommended node in this same turn.

## Required outputs

Formal results for this node go under:

- `patent-deliverables/03-invention-status-check/deliverables/`

Process records:

- `patent-deliverables/03-invention-status-check/process-records/process-log.md`
- `patent-deliverables/03-invention-status-check/process-records/open-questions.md`
- `patent-deliverables/03-invention-status-check/process-records/quality-gate-record.md`

Handoff:

- `patent-deliverables/03-invention-status-check/handoff/next-node-input.json`

Required files:

- `invention-status.json`
- `existing-materials-register.md`
- `materials-assessment-review.md`
- `start-node-decision.md`
- `next-node-input.json`

## Standalone run and user confirmation

- This node only reviews the materials assessment, decides the start node, and writes process records, deliverables, and the handoff.
- When this node finishes, stop. Show the main output paths and the next node after routing.
- Run the `04`–`12` node named in the handoff only in a later turn, after the user clearly says to continue or to enter the next step.
- Do not run the next node in the same turn as this node.

## Handoff rules

`next-node-input.json` must include:

- `current_skill`: `03-invention-status-check`
- `next_skill`: one of `04-patent-topic-selector` through `12-patent-word-generator`
- `has_patent_framework`: same as upstream
- `has_patent_draft`: same as upstream
- `has_related_materials`: same as upstream
- `existing_materials_folder`: same as upstream
- `materials_upload_confirmed`: same as upstream
- `materials_assessment_status`: same as upstream
- `material_readiness_by_stage`: readiness for nodes 04–12 after this review
- `recommended_start_skill`: same as `next_skill`
- `recommendation_reason`: this node's final reasons
- `missing_prerequisites`
- `recommended_source_files`: materials the recommended node should read first
- `routing_origin_skill`: `03-invention-status-check`
- `source_files`: files this node read
- `deliverables`: results this node produced
- `open_questions`: questions for the user or the patent attorney (专利代理师)
- `quality_gate_status`: `pass`, `warning`, or `fail`
- `can_continue`: whether the next node may start
- `must_stop_reason`: the reason, if it may not

## Quality gate

- The three-question record, materials assessment, and recommendation must be complete. When the user has materials, the actual directory and files must be checked.
- The final recommendation must be the earliest node that still needs work, and it must be one of 04 through 12.
- The recommendation must list usable evidence, the key gaps, and the inputs the recommended node needs.
- Do not invent technical facts that the user did not provide and that search did not support.
- Each node creates `patent-deliverables/<skill-name>/` with no extra project-number level.
- Process records, stage files, and patent files stay inside this node's directory.
- The next node may read only this node's `handoff/next-node-input.json`. It must not rely on spoken chat context.

## Stop conditions

- Skill 02 did not finish the three materials questions or has no start-node recommendation.
- The user claims materials exist, but upload was not confirmed, the directory is missing or empty, or a file cited by the assessment does not exist.
- The evidence is not enough to choose the earliest node among 04–12 that still needs work.
- A required input for this node is missing.
- A publication risk, ownership risk, or materials-authenticity risk cannot be judged.

## Do not

- Do not skip the node delivery directory.
- Do not keep the fixed two-way route "simple idea / existing materials".
- Do not let the user pick the start node for the system. Judge from the materials.
- Do not skip an earlier prerequisite that is still unmet just because a framework or draft already exists.
- Do not package unconfirmed content as a formal conclusion.
- Do not add technical features, appearance features, technical effects, or parameter ranges that are not supported by the user's materials, search records, or a human confirmation.
- Do not let the next node depend on spoken chat context.
