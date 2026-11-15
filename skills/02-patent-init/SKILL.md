---
name: "02-patent-init"
description: "用于发明专利独立流程线初始化；优先询问是否已有专利框架、专利初稿或相关材料，接收并评估已有素材，推荐 04 至 12 中适合开始的节点，再交接给 03-invention-status-check 复核路由。"
---

# 02-patent-init

## 节点目的

初始化发明专利skill独立流程线，优先盘点、接收和评估user-existing-materials，并形成有证据支撑的起始节点推荐。该节点只服务发明专利，不询问其他专利类型。

## 触发时机

`01-patent-master-control` 判断需要启动发明专利skill独立流程线时触发。

## 必需输入

- `patent-deliverables/01-patent-master-control/handoff/next-node-input.json`
- 用户的发明专利启动需求。
- 用户对三项素材盘点问题的逐项回答。

## 必建节点交付目录

开始实质工作前，必须在当前专利项目内创建以下目录。目录名必须与本 Skill 名称一致，不得增加项目编号层级：

```text
patent-deliverables/02-patent-init/
  input/
    01-user-existing-materials/        # 用户有任一类已有素材时创建；后续批次编号递增
  output/
  process-records/
  handoff/
  deliverables/
  stages/
  patent-files/
```

`<编号>-user-existing-materials` 中的编号采用两位数字，从 `01` 开始。若已存在同名目录，取当前最大编号加 1，例如 `02-user-existing-materials`；不得覆盖、移动、重命名或改写用户原始文件。

本节点产生的过程记录、阶段文件和专利相关文件都必须保存在该节点目录内；不得在项目根目录额外创建 `stages/`、`process-records/` 或 `patent-files/`。

## 执行步骤

1. 优先逐项询问用户，不得先询问电脑系统或其他初始化问题：
   1. 是否已有专利框架？
   2. 是否已完成专利初稿？
   3. 是否已有专利相关材料？
2. 要求用户分别回答“是/否”，允许多项同时为“是”；不得将三项压缩成一个笼统的“是否有材料”。
3. 若三项均为“否”，记录无已有素材，不创建user-existing-materials目录，按评估规则推荐从 `04-patent-topic-selector` 开始。
4. 若任一项为“是”，在本节点 `input/` 下创建下一个可用编号的 `<编号>-user-existing-materials/`，明确展示绝对路径，并指导用户将所有相关原始文件放入该目录；完成后请用户回复：`我已将已有素材放入指定文件夹`。
5. 创建目录并给出放置指引后必须停止，等待上述明确回复；在此之前将 `can_continue` 设为 `false`，不得假设文件已经存在，不得评估空目录。
6. 用户确认放置完成后，遍历目录内全部有效文件，忽略 `.DS_Store`、`Thumbs.db`、`desktop.ini` 等系统元数据；记录文件名、格式、大小、可读状态、材料类别、可支撑节点、明显缺失和相互冲突。不能读取的文件必须标为“待转换/待人工确认”。
7. 结合材料数量、覆盖范围、完整度、可读性、内容成熟度和相互一致性进行评估。用户口头声称“已有框架”或“初稿完成”只能作为线索，不能替代文件核验。
8. 按“起始节点推荐规则”选择 `04` 至 `12` 中最早需要补齐的节点，并写明逐项证据、缺口、风险和推荐理由；不得让用户自行选择节点，不得只按文件数量判断。
9. 完成素材评估后，再确认电脑系统为 Mac 或 Windows；若为 Mac，确认是否允许 Computer Use；记录专利类型固定为发明专利。
10. 将问卷、素材目录、评估结果和推荐节点写入交接文件，`next_skill` 固定为 `03-invention-status-check`，由 03 复核推荐后执行动态路由。本节点不得在同一轮执行 03 或推荐节点。

## 起始节点推荐规则

根据材料可用性选择“最早需要补齐”的节点；后段材料存在不代表可以跳过前段基础缺口：

- 推荐 `04-patent-topic-selector`：没有足以界定技术领域、应用场景、技术问题和核心方案的材料，或仅有零散想法。
- 推荐 `05-patent-prior-art-search`：技术问题和核心方案已基本明确，但缺少可复核的现有技术检索记录或公开风险判断。
- 推荐 `06-innovation-point-finder`：已有可复核检索证据和候选差异点，但最终创新点、技术效果或拟保护特征尚未明确。
- 推荐 `07-abstract-generator`：创新点和核心技术特征已经明确，但缺少可用摘要，或现有框架/初稿需要从摘要与发明名称开始统一主线。
- 推荐 `08-claims-writer`：已有可用摘要、明确创新点和核心技术特征，但权利要求缺失、结构不完整或保护范围需要重构。
- 推荐 `09-patent-drawing-generator`：摘要和权利要求可用，但附图少于 3 张、多于 7 张、缺失/不可用，或缺少统一事实源、结构母版和标号基准，需要规划或重绘。
- 推荐 `10-drawing-consistency-validator`：已有 3–7 张候选附图及足够结构基准，但尚未逐张完成事实、跨图、权利要求和标号一致性实图校验。
- 推荐 `11-description-writer`：3–7 张附图已经通过实图一致性校验，摘要和权利要求可用，但说明书五部分缺失、不完整或不能充分支撑权利要求。
- 推荐 `12-patent-word-generator`：摘要、权利要求书、说明书、3–7 张附图、附图实图校验记录和三向一致性记录均完整可用，仅需排版和 Word 汇总。

若同一批材料同时存在多个缺口，必须推荐编号最小、最早需要补齐的节点。不得因文档标题为“完整初稿”就直接推荐 12。

## 必需输出

本节点正式成果至少保存到：

- `patent-deliverables/02-patent-init/deliverables/`

本节点过程记录必须保存到：

- `patent-deliverables/02-patent-init/process-records/process-log.md`
- `patent-deliverables/02-patent-init/process-records/open-questions.md`
- `patent-deliverables/02-patent-init/process-records/quality-gate-record.md`

本节点交接文件必须保存到：

- `patent-deliverables/02-patent-init/handoff/next-node-input.json`

必交付文件：

- `system-environment.json`
- `input-status.json`
- `existing-materials-questionnaire.json`
- `existing-materials-inventory.md`
- `existing-materials-completeness.md`
- `start-node-recommendation.json`
- `initialization-record.md`
- `next-node-input.json`

## 独立运行与用户确认规则

- 本节点只能完成三项优先询问、素材接收、素材评估、起始节点推荐、环境确认、过程记录、交付结果和交接文件。
- 若创建了 `<编号>-user-existing-materials/`，必须在等待用户放置文件和完成评估之间至少停止一次；不得在创建空目录的同一轮声称已完成评估。
- 本节点完成后必须停止，向用户展示本节点主要输出文件路径和下一节点建议。
- 用户明确回复继续、确认进入下一步或类似指令后，才允许在新一轮运行 `03-invention-status-check`。
- 不得在本节点同一轮中直接执行 `03-invention-status-check` 或推荐的 04 至 12 节点。

## 交接规则

`next-node-input.json` 必须写明：

- `current_skill`: `02-patent-init`
- `next_skill`: `03-invention-status-check`
- `workflow`: `invention-patent-standalone-workflow`
- `patent_type`: `发明专利`
- `computer_system`: `Mac` 或 `Windows`
- `computer_use_allowed`: true / false / null
- `has_patent_framework`: true / false
- `has_patent_draft`: true / false
- `has_related_materials`: true / false
- `invention_input_status`: `simple_idea` 或 `existing_materials_assessed`
- `existing_materials_folder`: 素材目录路径；三项均为否时为 null
- `materials_upload_confirmed`: true / false
- `materials_assessment_status`: `not_required`、`waiting_for_upload`、`completed` 或 `blocked`
- `material_readiness_by_stage`: 04 至 12 各节点的 ready / partial / missing 结论及证据
- `recommended_start_skill`: `04-patent-topic-selector` 至 `12-patent-word-generator` 之一
- `recommendation_reason`
- `missing_prerequisites`
- `recommended_source_files`
- `source_files`
- `deliverables`
- `open_questions`
- `quality_gate_status`
- `can_continue`
- `must_stop_reason`

## 质量门

- 三项素材问题必须优先、逐项询问并分别记录。
- 用户任一项回答“是”时，必须创建编号素材目录、等待用户放置完成并核验实际文件。
- 素材评估必须基于文件内容，覆盖 04 至 12 的就绪度、缺口和证据；对附图必须区分“已有候选图”和“已通过实图一致性校验”。
- 推荐节点必须是最早需要补齐的节点，并有可审计理由。
- 电脑系统必须明确。
- Mac 是否允许 Computer Use 必须明确。
- 专利类型必须固定为发明专利。
- 每个节点必须创建 `patent-deliverables/<Skill名称>/`，不得增加项目编号层级。
- 下一节点只能读取本节点 `handoff/next-node-input.json`。

## 阻断条件

- 用户未逐项回答三项素材问题。
- 用户声称有素材，但尚未回复 `我已将已有素材放入指定文件夹`、目录无有效文件或文件均不可读。
- 素材内容不足以判断最早需要补齐的节点，且用户未补充必要事实。
- 用户未确认电脑系统。
- Mac 路线未确认 Computer Use 权限。

## 禁止事项

- 不得询问其他专利类型分流。
- 不得在用户回答素材三问之前先询问电脑系统、Computer Use 或其他初始化问题。
- 不得覆盖、移动、重命名或改写 `<编号>-user-existing-materials/` 中的用户原始文件。
- 不得仅按文件数量、文件名或用户自述判断成熟度；必须检查实际内容和前置依赖。
- 不得让用户自行选择起始节点，也不得固定把“已有初稿”映射到某一节点。
- 不得跳过 `03-invention-status-check`。
- 不得让下一节点依赖口头上下文。
