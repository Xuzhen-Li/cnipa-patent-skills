---
name: "05-patent-prior-art-search"
description: "用于对已确认技术披露制定中英文、分类号和组合检索策略，在可用的中国及国际专利数据库和非专利文献中进行可复核检索，确定最接近现有技术，并分别完成新颖性和创造性初步分析；明确区分可专利性检索与侵权/FTO检索。"
---

# 05-patent-prior-art-search

## 节点目的

以资深专利代理人的检索与分析方法，形成可重复执行、证据可追溯的现有技术调查，为 06 确定总的发明构思和差异特征提供基础。检索结论是申请前专业初评，不等同于审查结论、稳定性意见或自由实施意见。

## 触发与输入

04 完成后触发，或 03 直接推荐本节点时触发。必需输入：

- 上游交接文件和全部推荐来源文件。
- 已确认技术事实、技术问题—手段—效果链、候选发明构思及检索要素。
- 拟申请日或相关优先权日；尚未确定时以检索日为临时截止日并明确局限。

从 03 直达时，`next_skill` 与 `recommended_start_skill` 必须均为本节点，且材料足以重建上述内容；否则返回 03 或 04。

## 节点目录

在当前项目创建 `patent-deliverables/05-patent-prior-art-search/` 及标准七类子目录。检索页面、导出文件、文献全文、检索日志和分析成果必须收纳其中，不得改写用户原始材料。

## 检索边界

- 可专利性检索：关注相关日期以前向公众公开的专利和非专利技术资料，用于新颖性、创造性初评。
- FTO/侵权检索：关注特定国家有效权利要求及法律状态，目的和方法不同。本节点不提供 FTO 或不侵权结论，只记录可能需要另行调查的在权风险。
- 未检出不等于不存在，数据库覆盖、语言、分类、公开延迟和检索时间均必须写入局限说明。

## 执行步骤

1. 锁定检索事实集和相关日期，禁止把未确认的代理人设想混入检索对象。
2. 将候选构思拆为核心必要特征、关系特征、功能特征、效果特征和可选特征，建立检索概念组。
3. 构造中文、英文、缩写、同义词、上位/下位概念、旧称及可能误拼；结合 IPC/CPC、申请人、发明人、引证和相似文献扩展。
4. 按“整体概念 → 核心组合 → 关键单特征 → 分类号 → 申请人/发明人 → 引证网络”逐轮检索。优先使用可访问的 CNIPA、WIPO Patentscope、Espacenet、Google Patents 等专利数据库，并补充论文、标准、产品手册、网页存档等非专利文献。
5. 对每轮记录数据库、完整检索式、过滤条件、日期、命中数、筛选理由和导出文件；不得只记录关键词。
6. 核验候选对比文件的公开日、优先权、专利族、相关文本版本和可读全文。法律状态仅作辅助记录，不影响其是否构成现有技术的时间判断。
7. 选定一项或数项最接近现有技术，制作逐特征对比矩阵。每个“已公开”判断必须指向具体文献段落、权利要求或附图。
8. 新颖性初评必须逐项以单一对比文件检查全部技术特征，不得用多篇文件拼接否定新颖性。
9. 创造性初评按最接近现有技术、区别特征、实际解决的技术问题、技术启示/结合动机和技术效果进行分析；组合文献时说明为何本领域技术人员会或不会作出结合。
10. 若现有技术接近，只能从用户原始披露中寻找真实差异和退守点。代理人提出的新设想必须单独标记并交发明人验证，不得自动写成“3个新创新点”。
11. 无法访问数据库时仅输出人工检索方案，`can_continue=false`；只有取得可复核文献证据后才可交接 06。

## 必需输出

- `deliverables/search-strategy.md`
- `deliverables/queries-and-classifications.json`
- `deliverables/search-log.json`
- `deliverables/prior-art-document-list.json`
- `deliverables/patent-family-legal-status.json`
- `deliverables/feature-prior-art-matrix.json`
- `deliverables/closest-prior-art.md`
- `deliverables/novelty-preliminary.md`
- `deliverables/inventive-step-preliminary.md`
- `deliverables/search-limits-fto-boundary.md`
- `deliverables/candidate-differences-from-disclosure.md`
- 三份标准过程记录及 `handoff/next-node-input.json`

## 交接规则

交接文件必须写明：

- `current_skill=05-patent-prior-art-search`
- `next_skill=06-innovation-point-finder`
- 已有素材、动态路由字段原样传递
- `relevant_date`、`searched_databases`、`search_log_file`
- `closest_prior_art`、`feature_matrix_file`
- `novelty_preliminary_status`、`inventive_step_preliminary_status`
- `patentability_search_limitations`、`potential_fto_flags`
- `confirmed_difference_candidates`、`unconfirmed_agent_proposals`
- `source_files`、`deliverables`、`open_questions`
- `quality_gate_status`、`can_continue`、`must_stop_reason`

## 质量门与阻断

- 至少完成关键词、分类号和引证/主体中的适用检索路线，并保存完整可复核日志。
- 关键对比文件的相关日期、文本版本和具体证据位置已核验。
- 新颖性单篇对比和创造性组合分析严格分开。
- 检索未覆盖关键概念、只有摘要无全文、相关日期不明或最接近现有技术无法确定时，不得给出 pass。
- 不得承诺“未公开”“必然具备创造性”“不侵权”或“必然授权”。
- 不得把检索后临时构想、未验证效果或无原始依据差异写成发明事实。
