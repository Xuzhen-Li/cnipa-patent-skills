---
name: "06-innovation-point-finder"
description: "Confirm one general inventive concept and the related core, secondary, and fallback innovation points, with problem-means-effect evidence, feature levels, and unity. No fixed word count and no forced single isolated point. 用于结合最接近现有技术和原始技术披露，确认一个总的发明构思及相互关联的核心、次级和备用创新点，建立问题—手段—效果证据链、必要与可选特征层级、参数依据和单一性分析；不设固定字数，不强迫只选一个孤立创新点。"
---

# 06-innovation-point-finder

## 节点目的

以资深专利代理人的视角，把检索结果转化为有原始依据、能支持权利要求层级且具有合理退守位置的发明构思。最终由发明人确认技术事实，代理人负责提出保护结构和风险意见。

## 触发与输入

05 完成后触发，或 03 在已有材料含可复核检索证据时直接推荐。必需输入：

- 上游交接和推荐来源文件。
- 最接近现有技术、技术特征对比矩阵、新颖性和创造性初评。
- 原始技术披露、已确认事实及技术问题—手段—效果链。

从 03 直达时必须核验真实检索记录、对比文件全文和候选差异；缺失时返回 05。

## 节点目录

在当前项目创建 `patent-deliverables/06-innovation-point-finder/` 及标准七类子目录。用户原始文件和检索证据只读使用。

## 资深代理人分析规则

- 不要求只确认一个孤立创新点。应先确认一个总的发明构思，再组织与其存在技术关联的核心、次级、优选和备用保护点。
- 区别特征不当然等于创造性特征；必须分析其解决的客观技术问题、产生的技术效果及现有技术是否给出启示。
- 技术效果按 `实测证据`、`用户确认经验`、`可由机理直接推导`、`尚待验证` 分级。尚待验证效果不得作为确定性结论。
- 参数范围、材料选择、结构位置、步骤顺序和控制条件必须有原始依据；不得为扩大保护范围临时补造。
- 同一申请内的保护点必须接受单一性检查；缺少共同或相应特定技术特征的主题不得强行合并。

## 执行步骤

1. 复核最接近现有技术和逐特征对比，排除没有原始披露依据的候选差异。
2. 提炼总的发明构思，明确其核心技术贡献和共同特定技术特征。
3. 建立核心创新点、次级创新点、优选限定和备用退守点的层级，不固定数量，也不为凑数增加内容。
4. 对每个创新层级建立技术问题—技术手段—技术效果证据链，并关联对比文件和原始披露位置。
5. 区分独立权利要求可能需要的必要技术特征、从属项适合的可选限定和仅适合实施例记载的细节。
6. 检查可替代结构、等效手段、参数边界、工作状态和可能规避路径，记录哪些内容已披露、哪些需要发明人补充。
7. 分析每个候选保护点的创造性贡献、商业价值、侵权可识别性、举证难度和退守价值。
8. 向发明人展示完整发明构思和创新层级，逐项确认技术事实、效果、参数及替代方案。代理人建议设想必须单独确认并补入技术披露后才能采用。
9. 按保护范围完整、证据充分和后续权利要求可操作性形成最终结论，不设置固定字数要求。
10. 用户确认后交接 07 并停止，不得同轮执行 07。

## 必需输出

- `deliverables/general-inventive-concept.md`
- `deliverables/innovation-hierarchy.json`
- `deliverables/problem-means-effect-evidence.json`
- `deliverables/essential-optional-features.json`
- `deliverables/parameter-effect-evidence.json`
- `deliverables/alternatives-design-around.md`
- `deliverables/unity-preliminary.md`
- `deliverables/missing-experiments-materials.md`
- 三份标准过程记录及 `handoff/next-node-input.json`

## 交接规则

交接文件必须写明：

- `current_skill=06-innovation-point-finder`
- `next_skill=07-abstract-generator`
- 已有素材、动态路由字段原样传递
- `general_inventive_concept`、`innovation_hierarchy_file`
- `essential_features`、`optional_features`、`backup_features`
- `effect_evidence_file`、`parameter_basis_file`、`unity_status`
- `inventor_confirmation_status`、`unverified_effects`、`missing_technical_materials`
- `source_files`、`deliverables`、`open_questions`
- `quality_gate_status`、`can_continue`、`must_stop_reason`

## 质量门与阻断

- 总的发明构思、创新层级及共同特定技术特征清楚。
- 每个正式创新点均有原始披露、现有技术差异和技术效果依据。
- 必要、可选及实施例细节划分合理，参数和效果证据状态明确。
- 发明人未确认关键技术事实、待验证效果被当作确定效果、或单一性问题未处理时 `can_continue=false`。
- 不得按固定字数扩写，不得强迫只保留一个创新点，不得把区别特征直接等同于创造性。
