---
name: "02-patent-init"
description: "Initialize the invention-patent workflow: ask whether a framework, a draft, or related materials already exist, assess them, and recommend the earliest node from 04 to 12. 用于发明专利独立流程线初始化；优先询问是否已有专利框架、专利初稿或相关材料，接收并评估已有素材，推荐 04 至 12 中适合开始的节点，再交接给 03-invention-status-check 复核路由。"
---

# 02-patent-init

## Purpose

Initialize the standalone invention-patent (发明专利) workflow. First inventory, receive, and assess materials the user already has, then recommend a start node backed by evidence. This node serves invention patents only. Do not ask about other patent types.

## When it runs

Run when `01-patent-master-control` decides the standalone invention-patent workflow should start.

## Required inputs

- `patent-deliverables/01-patent-master-control/handoff/next-node-input.json`
- The user's request to start an invention patent.
- A separate answer to each of the three materials questions.

## Required node directory

Before substantive work, create this directory in the current patent project. The directory name must match this skill name. Do not add a project-number level.

```text
patent-deliverables/02-patent-init/
  input/
    01-user-existing-materials/   # create when the user has any existing material; later batches increment
  output/
  process-records/
  handoff/
  deliverables/
  stages/
  patent-files/
```

The number in `<nn>-user-existing-materials` is two digits starting at `01`. If that directory already exists, use one more than the current maximum, for example `02-user-existing-materials`. Do not overwrite, move, rename, or edit the user's original files.

Process records, stage files, and patent files from this node stay inside this directory. Do not also create `stages/`, `process-records/`, or `patent-files/` at the project root.

## Steps

1. Ask the user these questions first. Do not ask about the computer or other setup questions before them:
   1. Is there already a patent framework?
   2. Is there already a patent draft?
   3. Are there already related patent materials?
2. Require a yes/no answer to each question. More than one may be yes. Do not collapse the three questions into one vague "do you have materials?" question.
3. If all three answers are no, record that there are no existing materials, do not create a user-materials directory, and recommend starting at `04-patent-topic-selector`.
4. If any answer is yes, create the next free `<nn>-user-existing-materials/` under this node's `input/`, show its absolute path, and tell the user to put every related original file there. Ask the user to reply: `我已将已有素材放入指定文件夹`.
5. After creating the directory and giving that instruction, stop and wait for that exact reply. Until then set `can_continue` to `false`. Do not assume the files are already there, and do not assess an empty directory.
6. After the user confirms, walk every valid file in the directory. Ignore system metadata such as `.DS_Store`, `Thumbs.db`, and `desktop.ini`. Record the file name, format, size, readable state, material class, which nodes it can support, obvious gaps, and conflicts. Mark unreadable files as "needs conversion / needs human confirmation".
7. Assess quantity, coverage, completeness, readability, maturity, and consistency. A spoken claim that "there is a framework" or "the draft is done" is only a clue. It does not replace inspecting the files.
8. Under "Start-node recommendation rules", choose the earliest node from `04` through `12` that still needs work. Record the evidence, gaps, risks, and reasons item by item. Do not let the user pick the node, and do not judge by file count alone.
9. After the materials assessment, confirm whether the computer is Mac or Windows. On a Mac, confirm whether Computer Use is allowed. Record the patent type as invention patent (发明专利).
10. Write the questionnaire, materials directory, assessment, and recommended node into the handoff. `next_skill` is always `03-invention-status-check`. Skill 03 reviews the recommendation and routes. Do not run skill 03 or the recommended node in this same turn.

## Start-node recommendation rules

Choose the earliest node that still needs work. Later materials do not justify skipping an earlier gap:

- Recommend `04-patent-topic-selector` when the materials do not define the technical field, use setting, technical problem, and core solution, or when there are only scattered ideas.
- Recommend `05-patent-prior-art-search` when the technical problem and core solution are basically clear, but there is no reviewable prior-art search record or publication-risk judgment.
- Recommend `06-innovation-point-finder` when there is reviewable search evidence and candidate differences, but the final innovation points, technical effects, or features to be protected are not yet settled.
- Recommend `07-abstract-generator` when the innovation points and core technical features are clear, but there is no usable abstract (说明书摘要), or an existing framework/draft should be aligned starting from the abstract and the title of the invention (发明名称).
- Recommend `08-claims-writer` when a usable abstract, clear innovation points, and core technical features exist, but the claims (权利要求书) are missing, structurally incomplete, or need their scope rebuilt.
- Recommend `09-patent-drawing-generator` when the abstract and claims are usable, but the drawings are fewer than 3, more than 7, missing or unusable, or there is no single fact source, structural master, and mark baseline, so the drawings must be planned or redrawn.
- Recommend `10-drawing-consistency-validator` when there are already 3–7 candidate drawings and enough structural baseline, but no drawing-by-drawing check of facts, cross-view consistency, claims, and marks has been done on the actual images.
- Recommend `11-description-writer` when 3–7 drawings have passed the actual-image consistency check and the abstract and claims are usable, but the five sections of the description (说明书: 技术领域, 背景技术, 发明内容, 附图说明, 具体实施方式) are missing, incomplete, or do not fully support the claims.
- Recommend `12-patent-word-generator` when the abstract, claims, description, 3–7 drawings, the actual-image drawing check, and the three-way consistency record are all complete and only layout and the Word assembly remain.

If one batch has several gaps, recommend the lowest-numbered node, the earliest one that still needs work. Do not recommend 12 merely because a document is titled "complete draft".

## Required outputs

Formal results for this node go under:

- `patent-deliverables/02-patent-init/deliverables/`

Process records:

- `patent-deliverables/02-patent-init/process-records/process-log.md`
- `patent-deliverables/02-patent-init/process-records/open-questions.md`
- `patent-deliverables/02-patent-init/process-records/quality-gate-record.md`

Handoff:

- `patent-deliverables/02-patent-init/handoff/next-node-input.json`

Required files:

- `system-environment.json`
- `input-status.json`
- `existing-materials-questionnaire.json`
- `existing-materials-inventory.md`
- `existing-materials-completeness.md`
- `start-node-recommendation.json`
- `initialization-record.md`
- `next-node-input.json`

## Standalone run and user confirmation

- This node only completes the three priority questions, receipt of materials, assessment, start-node recommendation, environment confirmation, process records, deliverables, and the handoff.
- If `<nn>-user-existing-materials/` was created, stop at least once between waiting for the files and finishing the assessment. Do not claim the assessment is done in the same turn that created an empty directory.
- When this node finishes, stop. Show the main output paths and the next-node suggestion.
- Run `03-invention-status-check` only in a later turn, after the user clearly says to continue or to enter the next step.
- Do not run `03-invention-status-check` or the recommended nodes 04–12 in the same turn as this node.

## Handoff rules

`next-node-input.json` must include:

- `current_skill`: `02-patent-init`
- `next_skill`: `03-invention-status-check`
- `workflow`: `invention-patent-standalone-workflow`
- `patent_type`: `发明专利`
- `computer_system`: `Mac` or `Windows`
- `computer_use_allowed`: true / false / null
- `has_patent_framework`: true / false
- `has_patent_draft`: true / false
- `has_related_materials`: true / false
- `invention_input_status`: `simple_idea` or `existing_materials_assessed`
- `existing_materials_folder`: path of the materials directory, or null when all three answers are no
- `materials_upload_confirmed`: true / false
- `materials_assessment_status`: `not_required`, `waiting_for_upload`, `completed`, or `blocked`
- `material_readiness_by_stage`: ready / partial / missing for each node from 04 to 12, with evidence
- `recommended_start_skill`: one of `04-patent-topic-selector` through `12-patent-word-generator`
- `recommendation_reason`
- `missing_prerequisites`
- `recommended_source_files`
- `source_files`
- `deliverables`
- `open_questions`
- `quality_gate_status`
- `can_continue`
- `must_stop_reason`

## Quality gate

- The three materials questions must be asked first, one by one, and recorded separately.
- When the user answers yes to any item, create the numbered materials directory, wait until the user has placed the files, and check the actual files.
- The assessment must be based on file contents and must cover readiness, gaps, and evidence for nodes 04 through 12. For drawings, distinguish "candidate drawings exist" from "the actual-image consistency check has passed".
- The recommended node must be the earliest one that still needs work, with an auditable reason.
- The computer system must be explicit.
- On a Mac, whether Computer Use is allowed must be explicit.
- The patent type must stay invention patent (发明专利).
- Each node creates `patent-deliverables/<skill-name>/` with no extra project-number level.
- The next node may read only this node's `handoff/next-node-input.json`.

## Stop conditions

- The user did not answer the three materials questions separately.
- The user says materials exist, but has not replied `我已将已有素材放入指定文件夹`, the directory has no valid files, or none of the files can be read.
- The materials are not enough to decide the earliest node that still needs work, and the user has not supplied the missing facts.
- The user has not confirmed the computer system.
- The Mac route has no Computer Use decision.

## Do not

- Do not ask which other patent type to use.
- Do not ask about the computer, Computer Use, or other setup questions before the three materials questions are answered.
- Do not overwrite, move, rename, or edit the user's original files in `<nn>-user-existing-materials/`.
- Do not judge maturity only by file count, file names, or the user's own description. Check the contents and the prerequisite dependencies.
- Do not let the user choose the start node, and do not map "an existing draft" to one fixed node.
- Do not skip `03-invention-status-check`.
- Do not let the next node depend on spoken chat context.
