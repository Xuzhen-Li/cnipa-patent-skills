---
name: "08-claims-writer"
description: "Write or rebuild claims (权利要求书): at most 10 claims, clear dependencies, and support in the description. Design the hierarchy and dependency tree before the claim text. Also used when 03-invention-status-check routes existing materials here. 用于撰写或重构发明专利权利要求书，以保护范围完整、引用清晰、得到说明书支持为准，总项数不超过10项；先设计保护层级和依赖树，再撰写正文并校验引用与支撑关系。也用于 03-invention-status-check 根据已有框架或初稿直接推荐权利要求处理时。"
---

# 08-claims-writer

## 节点目的

形成保护范围完整、引用层级清晰、具有合理退守位置且得到说明书或已确认事实源支持的权利要求体系，总项数不超过 10 项。

## 触发时机

07-abstract-generator 完成后触发，或 03-invention-status-check 根据已有素材评估直接推荐本节点时触发。

## 必需输入

- 说明书摘要。
- 明确创新点或已有材料。
- 核心技术特征表。
- 已有说明书、专利框架或初稿；尚无说明书时，必须提供可供后续说明书落实的已确认技术事实源。
- 若从 03 直接进入：03 交接文件及其 `recommended_source_files`。

## 从 03 动态起步规则

- 仅当 03 交接文件中的 `next_skill` 和 `recommended_start_skill` 均为 `08-claims-writer` 时，才允许跳过 04–07 直接进入本节点。
- 必须确认已有可用摘要、明确创新点和核心技术特征，或初稿中存在足以重构权利要求的对应内容；user-existing-materials只读使用，不得改写原始文件。
- 前置要素不足时停止并返回 03，改从相应更早节点开始，不得为凑齐权利要求而编造技术特征。
- 本节点完成后恢复正常顺序，交接给 `09-patent-drawing-generator`。

## 必建节点交付目录

开始实质工作前，必须在当前专利项目内创建以下目录。目录名必须与本 Skill 名称一致，不得增加项目编号层级：

```text
patent-deliverables/08-claims-writer/
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

1. 识别保护主题、必要技术特征、可选限定和不同类别的保护对象。
2. 根据技术方案决定独立权利要求的数量和类别；不得为了凑数增加独立权利要求。
3. 在撰写正文前，先生成 `claim-scope-hierarchy.md`、`claim-dependency-tree.json` 和 `claim-feature-map.json`。
4. 按“引用与保护层级规则”设计核心主干、平行分支和逐层退守位置。
5. 根据保护需要和事实支撑确定实际项数；至少包含 1 项独立权利要求，独立权利要求与从属权利要求合计不得超过 10 项，不要求写满 10 项。
6. 按依赖树撰写正文。从属权利要求必须包含引用部分和新增限定，只能引用在前权利要求。
7. 将每项必要技术特征和新增限定映射到已有说明书的具体支撑位置；尚无说明书时，映射到已确认事实源并记录后续说明书必须落实的支撑需求。
8. 若候选保护点会使总项数超过 10 项，按“超出 10 项的处理规则”重新整理，不得直接截断。
9. 完成编号、引用、依赖层级、事实源、说明书支撑、术语一致性和总项数检查，并生成 `claims-quality-check.md`。
10. 全部质量门通过后生成交接文件并建议下一步运行 `09-patent-drawing-generator`；本节点完成后必须停止。

## 引用与保护层级规则

- 将每项独立权利要求作为一棵依赖树的根节点；不同保护类别可分别建立分支，但必须符合技术主题和单一性要求。
- 第一层从属权利要求用于限定关键子系统、结构、步骤、参数、材料或应用方式，可以直接引用对应的独立权利要求。
- 后续从属权利要求优先引用最接近且已经包含其前提特征的在前权利要求，形成宽、中、窄的逐层退守结构。
- 平行且互不依赖的技术方案可以分别直接引用独立权利要求；不得为了制造层级而把所有从属项机械串成一条长链。
- 不得无分析地让全部从属权利要求直接引用权利要求 1。若全部从属项确属平行方案，必须在 `claim-scope-hierarchy.md` 中逐项证明其不存在前提依赖并说明直接引用理由；不能证明时必须重构依赖树。
- 每项从属权利要求必须记录 `parent_claims`、新增限定、前提特征、退守价值、事实源和说明书支撑需求。
- 多项从属权利要求必须以择一方式引用在前权利要求，不得作为另一多项从属权利要求的引用基础。
- 权利要求主题名称、部件名称、步骤名称、附图标记和被引用权利要求保持一致。

## 超出 10 项的处理规则

1. 不得直接删除第 11 项及以后内容，也不得截断已经编号的文本。
2. 合并重复、重叠或保护价值过近的限定，避免以不同措辞重复同一退守点。
3. 按创造性贡献、商业价值、侵权可识别性和退守价值排序，保留不超过 10 项的核心体系。
4. 将未进入正式权利要求书的内容写入 `backup-protection-points.md`，注明未纳入原因和建议处理方式。

## 必需输出

本节点正式成果至少保存到：

- `patent-deliverables/08-claims-writer/deliverables/`

本节点过程记录必须保存到：

- `patent-deliverables/08-claims-writer/process-records/process-log.md`
- `patent-deliverables/08-claims-writer/process-records/open-questions.md`
- `patent-deliverables/08-claims-writer/process-records/quality-gate-record.md`

本节点交接文件必须保存到：

- `patent-deliverables/08-claims-writer/handoff/next-node-input.json`

必交付文件：

- claims.md
- claim-scope-hierarchy.md
- claim-dependency-tree.json
- claim-feature-map.json
- claim-structure.json
- claim-scope-notes.md
- backup-protection-points.md
- claims-quality-check.md
- next-node-input.json

## 独立运行与用户确认规则

- 本节点只能完成保护层级设计、依赖树、权利要求书、技术特征映射、结构表、保护范围说明、备用保护点、质量检查和交接文件。
- 本节点完成后必须停止，向用户展示本节点主要输出文件路径、权利要求结构概要和下一节点建议。
- 用户明确回复继续、确认进入下一步或类似指令后，才允许在新一轮运行 `09-patent-drawing-generator`。
- 不得在本节点同一轮中直接执行 `09-patent-drawing-generator`。

## 交接规则

`next-node-input.json` 必须写明：

- `current_skill`: `08-claims-writer`
- `next_skill`: `09-patent-drawing-generator`
- `existing_materials_folder`: 与上游一致
- `materials_assessment_status`: 与上游一致
- `recommended_start_skill`: 与上游一致
- `routing_origin_skill`: 与上游一致
- `claims_total`: 权利要求总项数，取值 1 至 10
- `independent_claims`: 独立权利要求编号列表
- `dependent_claims`: 从属权利要求编号列表
- `claim_tree_file`: `claim-dependency-tree.json` 路径
- `support_mapping_file`: `claim-feature-map.json` 路径
- `drawing_required_features`: 必须由附图表达的权利要求特征、部件关系和对应权利要求编号
- `drawing_fact_sources`: 上述制图要素的事实来源及说明书支撑位置
- `claim_count_limit_passed`: true / false
- `claim_dependency_check_passed`: true / false
- `specification_support_check_passed`: true / false
- `source_files`: 本节点读取的来源文件
- `deliverables`: 本节点产生的交付结果
- `open_questions`: 待用户或代理师确认的问题
- `quality_gate_status`: `pass`、`warning` 或 `fail`
- `can_continue`: 是否允许进入下一节点
- `must_stop_reason`: 如果不能继续，写明原因

## 质量门

- 若从 03 动态进入，本节点必须与 03 的推荐一致，且推荐素材包含可用摘要、明确创新点和核心技术特征。
- 必须在撰写正文前完成保护层级设计、依赖树和技术特征映射。
- 以保护范围完整、引用清晰、得到说明书支持为准，总项数不超过 10 项。
- 必须至少包含 1 项独立权利要求。
- 编号必须连续，所有引用必须指向在前权利要求且不存在循环。
- 从属权利要求必须形成有理由的主干和分支；不得无分析地全部直接引用权利要求 1，也不得机械串成单一长链。
- 多项从属权利要求必须择一引用，且不得引用另一多项从属权利要求。
- 每项新增限定必须具有事实源，并由已有说明书支撑；尚无说明书时必须形成明确的后续说明书支撑需求。
- 已有说明书时，技术特征映射必须标明具体支撑文件和位置；不得仅写“说明书有记载”。
- 不得凭空补造未由用户提供或未由检索支撑的技术事实。
- 每个节点必须创建 `patent-deliverables/<Skill名称>/`，不得增加项目编号层级。
- 过程记录、阶段文件和专利相关文件必须收纳在本节点目录内。
- 下一节点只能读取本节点 `handoff/next-node-input.json`，不得依赖聊天口头上下文。

## 阻断条件

- 03 的动态推荐不是本节点，或推荐素材缺少权利要求撰写所需的前置要素。
- 核心技术特征不足以写权利要求。
- 权利要求总项数超过 10，或编号不连续。
- 存在引用在后权利要求、循环引用、无效多项从属引用或主题名称不一致。
- 全部从属权利要求直接引用权利要求 1，但无法证明均为互不依赖的平行方案。
- 必要技术特征或新增限定没有事实源、说明书支撑或明确的后续说明书支撑需求。
- 依赖树、正文、技术特征映射表或保护层级设计之间不一致。
- 缺少本节点必需输入。
- 用户未完成必须人工确认的选择。
- 存在无法判断的公开风险、权属风险或材料真实性风险。

## 禁止事项

- 不得跳过节点交付目录。
- 不得以固定字数为目标扩写权利要求书。
- 不得为了写满 10 项而增加无支撑或无保护价值的权利要求。
- 不得在候选项超过 10 项时简单截断或直接删除后续保护点。
- 不得先生成“全部引用权利要求 1”的扁平文本，再省略保护层级分析。
- 不得把未确认内容包装成正式结论。
- 不得新增未由用户材料、检索记录或人工确认支撑的技术特征、外观特征、技术效果或参数范围。
- 不得让下一节点依赖口头上下文。
