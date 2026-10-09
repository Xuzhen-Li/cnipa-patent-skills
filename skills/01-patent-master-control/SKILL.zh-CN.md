---
name: "01-patent-master-control"
description: "Start and control the standalone invention-patent workflow. English triggers: \"start invention patent\"; \"start the invention patent workflow\"; \"run the invention patent process alone\"; \"turn this idea into an invention patent\". 中文触发：开始发明专利；发明专利开始工作；单独走发明专利流程；把这个想法写成发明专利。用于单独启动和控制发明专利独立流程线；先说明这是撰写辅助而非法律意见，用户以 yes 或确认同意后再调度 02 至 12。"
---

# 01-patent-master-control

## 节点目的

作为发明专利skill独立流程线的总控入口。该节点只调度发明专利流程。

## 触发时机

用户输入以下或类似指令时触发：

- `开始发明专利`
- `发明专利开始工作`
- `单独走发明专利流程`
- `把这个想法写成发明专利`

## 启动说明

在创建目录、读取材料、联网检索、调用工具或撰写正文之前，先展示下面的说明：

> 本流程只提供发明专利撰写辅助，不是法律意见。提交申请前应由注册专利代理师审查。在申请提交前，应对发明内容保密。
>
> 回复 yes 或确认后继续。

自然的肯定即可，例如 yes 或确认，不要求固定原句。

- 用户未同意时停止，不得开始实质工作。
- 用户同意后，才创建本节点目录并继续。

## 必需输入

- 用户启动发明专利流程的指令。
- 用户在看到启动说明后以 yes 或确认表示同意。
- 如已有发明专利流程交接文件，则读取上一节点 `handoff/next-node-input.json`。

## 必建节点交付目录

开始实质工作前，必须在当前专利项目内创建以下目录。目录名必须与本 Skill 名称一致，不得增加项目编号层级：

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

本节点产生的过程记录、阶段文件和专利相关文件都必须保存在该节点目录内；不得在项目根目录额外创建 `stages/`、`process-records/` 或 `patent-files/`。

## 执行步骤

1. 判断用户是否明确要求进入发明专利skill独立流程线。
2. 展示启动说明并等待 yes 或确认；用户未同意时停止。
3. 检查是否存在上一发明节点的 `handoff/next-node-input.json`。
4. 若无有效交接文件，生成交接文件并建议下一步运行 `02-patent-init`。
5. 若有交接文件，读取 `next_skill`、`can_continue` 和 `must_stop_reason`。
6. 若 `can_continue=false`，停止并说明阻断原因。
7. 若 `can_continue=true`，只提示下一步应运行交接文件指定的下一发明节点，不得在同一轮自动执行下一节点。

## 必需输出

本节点正式成果至少保存到：

- `patent-deliverables/01-patent-master-control/deliverables/`

本节点过程记录必须保存到：

- `patent-deliverables/01-patent-master-control/process-records/process-log.md`
- `patent-deliverables/01-patent-master-control/process-records/open-questions.md`
- `patent-deliverables/01-patent-master-control/process-records/quality-gate-record.md`

本节点交接文件必须保存到：

- `patent-deliverables/01-patent-master-control/handoff/next-node-input.json`

必交付文件：

- `master-control-status.json`
- `current-stage.md`
- `next-node-suggestion.json`
- `next-node-input.json`

## 独立运行与用户确认规则

- 本节点只能完成 `01-patent-master-control` 的目录创建、过程记录、交付结果和交接文件。
- 开场的 yes 或确认，与本节点完成后的“继续下一步”，是两次不同的用户确认，不得相互替代。
- 本节点完成后必须停止，向用户展示本节点主要输出文件路径和下一节点建议。
- 用户明确回复继续、确认进入下一步或类似指令后，才允许在新一轮运行 `02-patent-init`。
- 不得在本节点同一轮中直接执行 `02-patent-init` 或后续任何节点。

## 交接规则

`next-node-input.json` 必须写明：

- `current_skill`: `01-patent-master-control`
- `next_skill`: `02-patent-init`
- `workflow`: `invention-patent-standalone-workflow`
- `source_files`
- `deliverables`
- `open_questions`
- `quality_gate_status`
- `can_continue`
- `must_stop_reason`

## 质量门

- 必须确认当前只运行发明专利路线。
- 必须先展示启动说明，并取得用户以 yes 或确认作出的同意。
- 不得分流到非发明专利路线。
- 必须明确下一发明节点。
- 每个节点必须创建 `patent-deliverables/<Skill名称>/`，不得增加项目编号层级。
- 下一节点只能读取本节点 `handoff/next-node-input.json`。

## 阻断条件

- 用户指令不是发明专利路线。
- 用户尚未以 yes 或确认表示同意。
- 找不到有效交接文件且无法进入初始化。
- 上一节点写入 `can_continue=false`。

## 禁止事项

- 不得跳过 `02-patent-init`。
- 用户以 yes 或确认同意之前，不得创建项目交付目录、读取用户材料或执行任何实质工作。
- 不得把开场的 yes 或确认当成进入下一节点的指令。
- 不得进入非发明专利路线。
- 不得让下一节点依赖口头上下文。
