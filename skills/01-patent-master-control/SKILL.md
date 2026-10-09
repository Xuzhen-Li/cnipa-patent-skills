---
name: "01-patent-master-control"
description: "Start and control the standalone invention-patent workflow. English triggers: \"start invention patent\"; \"start the invention patent workflow\"; \"run the invention patent process alone\"; \"turn this idea into an invention patent\". 中文触发：开始发明专利；发明专利开始工作；单独走发明专利流程；把这个想法写成发明专利。用于单独启动和控制发明专利独立流程线；先说明这是撰写辅助而非法律意见，用户以 yes 或确认同意后再调度 02 至 12。"
---

# 01-patent-master-control

## Purpose

Entry controller for the standalone invention-patent (发明专利) workflow. This node schedules only that workflow.

## When it runs

Run when the user enters any of these, or a close variant:

- `开始发明专利`
- `发明专利开始工作`
- `单独走发明专利流程`
- `把这个想法写成发明专利`
- `start invention patent`
- `start the invention patent workflow`
- `run the invention patent process alone`
- `turn this idea into an invention patent`

## Start confirmation

Before creating directories, reading materials, searching the web, calling tools, analyzing the invention, drafting text, or any other substantive work, show this notice:

> This workflow is drafting assistance, not legal advice. A registered patent agent (专利代理师) should review the draft before filing. Keep the invention confidential until filing.
>
> Reply yes or 确认 to continue.

A natural confirmation is enough, for example `yes` or `确认`. There is no fixed sentence.

- If the user does not agree, stop and do no substantive work.
- After the user agrees, create this node's directories and continue.

## Required inputs

- The user's command to start the invention-patent workflow.
- A clear confirmation such as `yes` or `确认` after the user has seen the notice.
- If a prior handoff exists, read that node's `handoff/next-node-input.json`.

## Required node directory

Before substantive work, create this directory in the current patent project. The directory name must match this skill name. Do not add a project-number level.

```text
patent-deliverables/01-patent-master-control/
  input/
  output/
  process-records/
  handoff/
  deliverables/
  stages/
  patent-files/
```

Process records, stage files, and patent files from this node stay inside this directory. Do not also create `stages/`, `process-records/`, or `patent-files/` at the project root.

## Steps

1. Decide whether the user clearly asked for the standalone invention-patent workflow.
2. Show the start notice and wait for yes or 确认. Stop if the user has not agreed.
3. Check for a previous invention node's `handoff/next-node-input.json`.
4. If there is no valid handoff, write one and recommend `02-patent-init` next.
5. If a handoff exists, read `next_skill`, `can_continue`, and `must_stop_reason`.
6. If `can_continue=false`, stop and state the blocking reason.
7. If `can_continue=true`, only name the next invention node recorded in the handoff. Do not run that node in the same turn.

## Required outputs

Formal results for this node go under:

- `patent-deliverables/01-patent-master-control/deliverables/`

Process records:

- `patent-deliverables/01-patent-master-control/process-records/process-log.md`
- `patent-deliverables/01-patent-master-control/process-records/open-questions.md`
- `patent-deliverables/01-patent-master-control/process-records/quality-gate-record.md`

Handoff:

- `patent-deliverables/01-patent-master-control/handoff/next-node-input.json`

Required files:

- `master-control-status.json`
- `current-stage.md`
- `next-node-suggestion.json`
- `next-node-input.json`

## Standalone run and user confirmation

- This node only creates its directories, process records, deliverables, and handoff for `01-patent-master-control`.
- The opening yes or 确认 and the later reply that enters the next step are two different confirmations. Neither replaces the other.
- When this node finishes, stop. Show the main output paths and `next-node-suggestion.json`.
- Run `02-patent-init` only in a later turn, after the user clearly says to continue or to enter the next step.
- Do not run `02-patent-init` or any later node in the same turn as this node.

## Handoff rules

`next-node-input.json` must include:

- `current_skill`: `01-patent-master-control`
- `next_skill`: `02-patent-init`
- `workflow`: `invention-patent-standalone-workflow`
- `source_files`
- `deliverables`
- `open_questions`
- `quality_gate_status`
- `can_continue`
- `must_stop_reason`

## Quality gate

- Confirm that only the invention-patent route is running.
- Show the start notice and obtain a clear yes or 确认 before substantive work.
- Do not branch into a non-invention patent route.
- Name the next invention node explicitly.
- Each node creates `patent-deliverables/<skill-name>/` with no extra project-number level.
- The next node may read only this node's `handoff/next-node-input.json`.

## Stop conditions

- The user command is not an invention-patent route.
- The user has not agreed with yes or 确认.
- No valid handoff exists and initialization cannot start.
- The previous node set `can_continue=false`.

## Do not

- Do not skip `02-patent-init`.
- Before the user agrees with yes or 确认, do not create the project delivery directory, read user materials, or do any substantive work.
- Do not treat the opening yes or 确认 as the instruction to enter the next node.
- Do not enter a non-invention patent route.
- Do not let the next node depend on spoken chat context.
