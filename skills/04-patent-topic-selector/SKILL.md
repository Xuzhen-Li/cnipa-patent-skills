---
name: "04-patent-topic-selector"
description: "用于从简单发明想法或 03-invention-status-check 推荐的早期材料中挖掘技术披露，建立技术问题—技术手段—技术效果链，初筛可专利主题、总的发明构思、单一性、商业覆盖和侵权可识别性，并形成可复核检索要素；不得替发明人虚构技术方案。"
---

# 04-patent-topic-selector

## 节点目的

以资深发明专利代理人的办案方法，把零散想法整理为可由发明人确认、可检索、可进一步形成权利要求的技术披露。该节点负责发现和组织已有技术贡献，不负责替发明人创造不存在的结构、步骤、参数或效果。

## 触发与输入

03 将本节点确定为最早需要补齐的节点时触发。必需输入：

- 03 的 `handoff/next-node-input.json`，且 `next_skill`、`recommended_start_skill` 均为本节点。
- 用户的发明想法、应用场景及 03 推荐的全部来源文件。
- 已有样机、草图、流程、实验、故障记录或需求资料；没有时明确记录缺失。

user-existing-materials只读使用。材料连技术对象和基本用途都无法确定时返回 03，不得补造。

## 节点目录

在当前项目创建 `patent-deliverables/04-patent-topic-selector/` 及标准七类子目录：`input/`、`output/`、`process-records/`、`handoff/`、`deliverables/`、`stages/`、`patent-files/`。所有成果必须收纳其中，用户原始文件不得改写。

## 资深代理人工作原则

- 每项内容标记为 `用户明确确认`、`材料直接记载`、`代理人归纳`、`代理人建议设想` 或 `待发明人确认`。
- 代理人归纳不得改变技术含义；建议设想不得直接进入后续专利正文或权利要求。
- 优先识别真正解决技术问题的技术手段，避免把商业目标、功能愿望、使用效果或宣传口号当作发明点。
- 同时考虑保护客体、单一性、可实施性、商业覆盖、规避难度和侵权可识别性，但本节点不作新颖性或创造性最终结论。

## 执行步骤

1. 建立材料来源清单和 `fact-hypothesis-layers.json`，逐项记录来源位置和确认状态。
2. 拆解技术领域、技术对象、使用场景、现有做法、具体缺陷及约束条件。
3. 建立 `problem-means-effect-chain.json`。每个效果必须关联产生该效果的技术特征；缺少依据时标记待验证。
4. 初筛是否属于技术方案，识别纯商业规则、智力活动规则、诊断治疗方法、纯审美设计或其他保护客体风险；只输出风险提示，不擅自作确定法律结论。
5. 从已确认事实中归纳一个或多个候选发明构思，区分核心技术贡献、配合特征、实施细节和可替代方案。
6. 初步分析各候选构思是否具有一个总的发明构思；明显无技术关联的主题分开记录，不强行合并。
7. 从产品覆盖、竞争方案、可能规避路径和侵权证据可获得性角度评估候选保护主题。
8. 将待确认结构、参数、效果和替代方案形成问题清单，请发明人逐项确认。未确认设想不得进入检索事实集。
9. 基于已确认内容生成中英文关键词、同义词、上位/下位概念、部件关系、功能关系及可能 IPC/CPC 方向，交接给 05。
10. 用户确认技术事实边界和候选发明构思后生成交接文件并停止，不得同轮执行 05。

## 必需输出

- `deliverables/technical-disclosure.md`
- `deliverables/fact-hypothesis-layers.json`
- `deliverables/problem-means-effect-chain.json`
- `deliverables/patentable-subject-screen.md`
- `deliverables/candidate-concepts-unity.md`
- `deliverables/commercial-coverage-detectability.md`
- `deliverables/search-elements-keywords.json`
- `deliverables/inventor-open-questions.md`
- 三份标准过程记录及 `handoff/next-node-input.json`

## 交接规则

交接文件必须写明：

- `current_skill=04-patent-topic-selector`
- `next_skill=05-patent-prior-art-search`
- 已有素材、动态路由字段原样传递
- `confirmed_fact_file`、`problem_solution_effect_file`、`candidate_inventive_concepts_file`
- `subject_matter_risks`、`unity_risks`、`design_around_risks`、`detectability_risks`
- `inventor_confirmation_status`、`unconfirmed_proposals`
- `search_elements_file`、`source_files`、`deliverables`、`open_questions`
- `quality_gate_status`、`can_continue`、`must_stop_reason`

## 质量门与阻断

- 技术问题、技术手段和技术效果能够形成有来源的因果链。
- 已确认事实与代理人建议严格分开；所有拟检索要素均有事实依据。
- 候选构思具有初步技术性、可实施性和明确检索边界。
- 发明人尚未确认关键事实、技术效果或建议设想时 `can_continue=false`。
- 保护客体、权属、公开或材料真实性风险无法判断时停止并列明所需资料。
- 不得承诺可授权，不得把市场需求或理想功能包装为已完成技术方案。
