---
name: "03-invention-status-check"
description: "用于复核 02-patent-init 的已有素材评估和起始节点推荐，依据实际材料成熟度动态路由到 04 至 12 中最早需要补齐的节点。"
---

# 03-invention-status-check

## 节点目的

复核已有素材的实际成熟度，独立确定最早需要补齐的节点，并动态分流到 04 至 12。

## 触发时机

`02-patent-init` 完成后触发。

## 必需输入

- `patent-deliverables/02-patent-init/handoff/next-node-input.json`。
- 02 生成的三问记录、素材清单、完整度评估和起始节点推荐。
- user-existing-materials目录；三项均为否时可为 null。

## 必建节点交付目录

开始实质工作前，必须在当前专利项目内创建以下目录。目录名必须与本 Skill 名称一致，不得增加项目编号层级：

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

本节点产生的过程记录、阶段文件、专利正文、附图、Word 中间稿和其他专利相关文件，都必须保存在该节点目录内；不得在项目根目录额外创建 `stages/`、`process-records/` 或 `patent-files/`。

## 执行步骤

1. 读取 02 的三问记录、素材目录、逐文件清单、04 至 12 就绪度评估、推荐节点和推荐理由。
2. 若用户声称有任一类素材，核验素材目录存在、用户已确认放置完成且评估所引用的文件真实存在；不得仅复述用户自述。
3. 按 02 的“起始节点推荐规则”复核每个前置依赖，并选择编号最小、最早需要补齐的节点。对附图单独核验实际数量是否为 3–7、是否存在结构母版/事实基准，以及是否有逐张实图一致性通过记录；只有图片文件不等于已经通过 10。
4. 若复核结论与 02 推荐不同，以证据更充分的结论为准，并在 `start-node-decision.md` 中逐项说明调整理由。
5. 不要求用户自行选择从哪个节点开始；只向用户展示推荐节点、可用素材、缺失项、判断依据和后续路线。
6. 将 `next_skill` 写为最终推荐的 `04` 至 `12` 节点，生成交接文件并停止；不得在同一轮执行被推荐节点。

## 必需输出

本节点正式成果至少保存到：

- `patent-deliverables/03-invention-status-check/deliverables/`

本节点过程记录必须保存到：

- `patent-deliverables/03-invention-status-check/process-records/process-log.md`
- `patent-deliverables/03-invention-status-check/process-records/open-questions.md`
- `patent-deliverables/03-invention-status-check/process-records/quality-gate-record.md`

本节点交接文件必须保存到：

- `patent-deliverables/03-invention-status-check/handoff/next-node-input.json`

必交付文件：

- invention-status.json
- existing-materials-register.md
- materials-assessment-review.md
- start-node-decision.md
- next-node-input.json

## 独立运行与用户确认规则

- 本节点只能完成素材评估复核、起始节点决策、过程记录、交付结果和交接文件。
- 本节点完成后必须停止，向用户展示本节点主要输出文件路径和分流后的下一节点。
- 用户明确回复继续、确认进入下一步或类似指令后，才允许在新一轮运行交接文件指定的 `04` 至 `12` 节点。
- 不得在本节点同一轮中直接执行下一节点。

## 交接规则

`next-node-input.json` 必须写明：

- `current_skill`: `03-invention-status-check`
- `next_skill`: `04-patent-topic-selector` 至 `12-patent-word-generator` 之一
- `has_patent_framework`: 与上游一致
- `has_patent_draft`: 与上游一致
- `has_related_materials`: 与上游一致
- `existing_materials_folder`: 与上游一致
- `materials_upload_confirmed`: 与上游一致
- `materials_assessment_status`: 与上游一致
- `material_readiness_by_stage`: 经本节点复核后的 04 至 12 就绪度结论
- `recommended_start_skill`: 与 `next_skill` 一致
- `recommendation_reason`: 本节点最终判断理由
- `missing_prerequisites`
- `recommended_source_files`: 被推荐节点应优先读取的素材文件
- `routing_origin_skill`: `03-invention-status-check`
- `source_files`: 本节点读取的来源文件
- `deliverables`: 本节点产生的交付结果
- `open_questions`: 待用户或代理师确认的问题
- `quality_gate_status`: `pass`、`warning` 或 `fail`
- `can_continue`: 是否允许进入下一节点
- `must_stop_reason`: 如果不能继续，写明原因

## 质量门

- 三问记录、素材评估和推荐结论必须完整；用户有素材时必须核验实际目录和文件。
- 最终推荐必须是最早需要补齐的节点，且范围只能为 04 至 12。
- 推荐结论必须列出可用证据、关键缺口和被推荐节点所需输入。
- 不得凭空补造未由用户提供或未由检索支撑的技术事实。
- 每个节点必须创建 `patent-deliverables/<Skill名称>/`，不得增加项目编号层级。
- 过程记录、阶段文件和专利相关文件必须收纳在本节点目录内。
- 下一节点只能读取本节点 `handoff/next-node-input.json`，不得依赖聊天口头上下文。

## 阻断条件

- 02 未完成三项素材询问或缺少起始节点推荐。
- 用户声称有素材，但上传未确认、目录不存在、目录为空或评估引用文件不存在。
- 现有证据不足以在 04 至 12 中确定最早需要补齐的节点。
- 缺少本节点必需输入。
- 存在无法判断的公开风险、权属风险或材料真实性风险。

## 禁止事项

- 不得跳过节点交付目录。
- 不得继续采用“简单想法 / 已有材料”二分法固定路由。
- 不得让用户代替系统选择起始节点；必须依据素材内容自行判断。
- 不得仅因已有框架或初稿就跳过更早但尚未满足的前置节点。
- 不得把未确认内容包装成正式结论。
- 不得新增未由用户材料、检索记录或人工确认支撑的技术特征、外观特征、技术效果或参数范围。
- 不得让下一节点依赖口头上下文。
