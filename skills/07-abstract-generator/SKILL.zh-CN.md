---
name: "07-abstract-generator"
description: "Draft a Chinese invention-patent abstract (说明书摘要) of at most 300 characters from the confirmed inventive concept. Skill 11-description-writer finalizes it. 用于依据已确认的总发明构思、核心技术方案和技术效果生成中国发明专利说明书摘要初稿，正文不超过 300 字；摘要初稿供后续权利要求和说明书使用，并由 11-description-writer 在全文及附图确定后完成最终定稿。"
---

# 07-abstract-generator

## 节点目的

以资深专利代理人的摘要撰写方法形成结构准确、用语客观的摘要初稿。摘要不用于确定保护范围；本节点不得让摘要反向限制尚未完成的权利要求。最终摘要由 11 结合权利要求、说明书和通过校验的摘要附图定稿。

## 触发与输入

06 完成后触发，或 03 在已有材料满足条件时直接推荐。必需输入：

- 上游交接和全部推荐来源文件。
- 发明名称候选、总的发明构思、技术问题、核心技术方案、主要技术效果和用途。
- 必要与可选技术特征表、效果证据状态和发明人确认记录。

从 03 直达时必须核验上述要素均已有来源；不足时返回相应更早节点。

## 节点目录

在当前项目创建 `patent-deliverables/07-abstract-generator/` 及标准七类子目录。所有成果收纳其中，用户原始材料只读使用。

## 摘要撰写规则

- 摘要正文不超过 300 字，不以接近上限为目标；以准确概括必要内容为准。
- 通常按发明名称/技术领域、要解决的技术问题、核心技术方案、主要技术效果和主要用途组织。
- 核心方案应体现主要技术特征及其关系，不能只写功能、目标或效果。
- 仅写有证据支撑的效果；尚待验证的优势不得写成确定事实。
- 不使用宣传、评价、承诺授权、扩大保护范围或商业营销性表述。
- 不写检索过程、对比文件评价、权利要求编号或无必要的实施例细节。
- 发明名称应准确反映保护主题，避免商标、型号、宣传词和不必要限定。
- 本节点只记录摘要附图候选表达需求；摘要附图最终从 10 通过的附图中选择。

## 执行步骤

1. 锁定已确认总发明构思、核心必要特征和证据充分的技术效果。
2. 形成发明名称候选并检查与拟保护客体、技术方案及后续权利要求主题一致。
3. 建立摘要要素表，每句话关联事实来源和创新层级。
4. 撰写摘要正文，压缩重复背景、可选特征和宣传性效果。
5. 运行 `python3 scripts/validate_abstract.py <abstract-draft.md>`，确认摘要正文不超过 300 个非空白字符；超出时必须实质精简，不得只删除必要技术关系。
6. 标记 `abstract_status=preliminary`，列明需在 11 根据权利要求、说明书和附图回填或复核的内容。
7. 用户确认摘要初稿后交接 08 并停止，不得同轮执行 08。

## 必需输出

- `deliverables/abstract-draft.md`：摘要初稿，保持与现有 08 输入兼容
- `deliverables/title-candidates.md`
- `deliverables/abstract-element-sources.json`
- `deliverables/abstract-character-check.json`
- `deliverables/abstract-finalization-checklist.md`
- 三份标准过程记录及 `handoff/next-node-input.json`

## 交接规则

交接文件必须写明：

- `current_skill=07-abstract-generator`
- `next_skill=08-claims-writer`
- 已有素材、动态路由字段原样传递
- `abstract_file`、`abstract_status=preliminary`、`abstract_character_count`
- `title_candidates_file`、`abstract_element_source_file`
- `abstract_drawing_requirements`、`finalization_required_at_skill=11-description-writer`
- `unverified_effects_excluded`、`source_files`、`deliverables`、`open_questions`
- `quality_gate_status`、`can_continue`、`must_stop_reason`

## 质量门与阻断

- 摘要正文不超过 300 字，技术问题、核心方案、效果和用途表达客观且相互一致。
- 每项实质内容均有来源，不包含未确认参数、结构或技术效果。
- 发明名称、总的发明构思和拟保护客体一致。
- 摘要字符校验失败、核心方案不清或关键效果无证据时不得放行。
- 不得把摘要初稿标为最终摘要，不得独立生成摘要附图，不得以固定字数为目标扩写。
