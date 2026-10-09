---
name: "11-description-writer"
description: "Write the description (说明书) after both drawing gates pass. Control background admissions, generalization, support, enablement, effect evidence, and added-matter risk, then finalize the abstract. 用于以资深专利代理人的撰写和审查标准，在附图通过双重质量门后完成发明专利说明书，控制背景技术不当自认、概括层级、支持性、充分公开、技术效果证据和后续修改超范围风险，并按机械、电气、软件、方法、化学或生物领域要求完成摘要最终定稿。"
---

# 11-description-writer

## 节点目的

形成能够支持权利要求、使所属技术领域技术人员能够实现、且与通过校验附图一致的说明书。该节点不仅生成五个章节，还必须完成原始披露、权利要求、说明书、附图和技术效果之间的专业审查，并最终定稿摘要。

## 触发与输入

- 10 的实质一致性门和形式合规门均通过、用户确认后触发。
- 03 直达时，必须具有等效的附图双重质量门记录；否则返回 10，附图或事实基准不足时返回 09。
- 必须读取：上游交接、07 摘要初稿、08 权利要求及依赖树、10 通过图集和哈希、04/06 的原始技术事实与确认记录、05 对比文件及分析、部件/步骤主数据和关系矩阵。

## 节点目录与领域规范

创建 `patent-deliverables/11-description-writer/` 及标准七类子目录。10 的附图副本只读使用，不得修改。

开始撰写前读取 [references/领域化说明书审查基准.md](references/领域化说明书审查基准.md)，根据 `drawing_route_type` 和技术主题加载对应章节；混合发明读取所有相关章节。

## 资深代理人撰写原则

- 以申请前已经存在并由发明人确认的技术事实为基础。新补充事实可以在申请前纳入，但必须保存发明人确认、来源和时间；不得由模型虚构。
- 每项权利要求特征必须有说明书明确或可直接、毫无疑义确定的支持位置；宽泛概括必须有足够实施方式和替代方案支撑。
- 背景技术应客观、准确，避免无证据使用“公知”“常规”“均已解决”等表述，也避免把本发明关键特征误写成申请人承认的现有技术。
- 技术效果必须关联产生效果的具体技术特征和证据状态，不使用“显著”“完全”“彻底”等无依据绝对表述。
- 实施例用于支持和说明，不得无意把独立权利要求限定为单一尺寸、材料、形状或工作状态。

## 执行步骤

1. 锁定原始技术披露基线、发明人后续确认记录、权利要求版本、事实源版本和 10 的附图哈希。
2. 建立 `original-disclosure-audit.json`。将每项拟写内容标记为原始记载、申请前补充确认、代理人概括或无依据；无依据内容禁止进入正文。
3. 撰写发明名称和技术领域，确保与独立权利要求保护客体一致。
4. 撰写背景技术：说明最接近现有技术及客观缺陷，必要时引用对比文件；执行背景技术不当自认检查。
5. 撰写发明内容：依次说明技术问题、技术方案和有依据的有益效果。技术方案至少覆盖各独立权利要求的必要技术特征，并合理呈现从属层级。
6. 撰写附图说明，只引用 10 通过的 3–7 张图；图号、视图类型、标号和状态说明必须与通过清单一致。
7. 撰写具体实施方式：说明结构/步骤关系、工作原理、操作过程、参数来源、替代方案及必要实验或数据，使所属领域技术人员能够实现权利要求覆盖的方案。
8. 按领域规范检查机械、电气、软件、方法、化学或生物技术的特殊公开要求。资料不足时形成补充清单，不得用通用套话掩盖。
9. 建立 `claims-description-drawings-map.json` 和 `generalization-alternatives.json`，逐特征记录段落、图号、标号、实施例、替代方式和事实来源。
10. 执行支持性、清楚性、充分公开、单一性、技术效果证据和申请后修改超范围风险审查。发现权利要求超出披露范围时不得靠扩写虚构支持，应退回 08 或要求发明人补充确认。
11. 结合最终权利要求、说明书和 10 选定摘要附图，修订 07 摘要初稿，输出不超过 300 字的摘要定稿，并运行 `python3 scripts/validate_final_abstract.py <abstract-final.md>`。
12. 用户确认说明书、摘要定稿及风险清单后交接 12 并停止。

## 必需输出

- `deliverables/description.md`
- `deliverables/brief-description-of-drawings.md`
- `deliverables/embodiment-points.json`
- `deliverables/original-disclosure-audit.json`
- `deliverables/background-admission-review.md`
- `deliverables/claims-description-drawings-map.json`
- `deliverables/generalization-alternatives.json`
- `deliverables/technical-effect-evidence.json`
- `deliverables/enablement-support-review.md`
- `deliverables/added-matter-risk-list.md`
- `deliverables/abstract-final.md`
- `deliverables/abstract-final-validation.json`
- `deliverables/drawing-usage-manifest.json`
- 三份标准过程记录及 `handoff/next-node-input.json`

## 摘要最终定稿规则

- 07 的摘要是初稿，不得原样默认通过。
- 摘要定稿必须与最终独立权利要求的技术主题、说明书核心方案及摘要附图一致，正文不超过 300 字。
- 摘要不得新增说明书未记载内容，也不得用宣传性或扩大保护范围的表达。
- 摘要附图只能使用 10 指定的通过校验图片，不得重绘或另行生成。

## 交接规则

交接文件必须写明：

- `current_skill=11-description-writer`
- `next_skill=12-patent-word-generator`
- 已有素材、动态路由字段原样传递
- `specification_file`、`final_abstract_file`、`final_abstract_character_count`
- `claims_specification_drawing_mapping_file`、`original_disclosure_audit_file`
- `enablement_review_status`、`support_review_status`、`added_matter_risk_status`
- `background_admission_review_status`、`effect_evidence_status`
- `validated_figure_count`（3–7）、`validated_figure_files`、`validated_figure_hashes`、`abstract_figure_file`
- `source_files`、`deliverables`、`open_questions`、`quality_gate_status`、`can_continue`、`must_stop_reason`

## 质量门与阻断

- 10 两个附图质量门均为 pass，使用图像与哈希清单完全一致。
- 说明书各部分完整，但不以固定篇幅为目标；以支持权利要求和充分公开为准。
- 每项权利要求特征均有具体支持位置，概括范围有足够实施方式和替代方案支撑。
- 背景技术无明显不当自认，技术效果有特征和证据依据。
- 领域特殊公开要求已满足，摘要定稿不超过 300 字且与全文及附图一致。
- 关键实施信息、实验/参数依据、发明人补充确认或支持位置缺失时 `can_continue=false`。
- 不得通过虚构实施例、参数、替代方案或效果弥补权利要求缺陷；不得修改已校验图片掩盖正文矛盾。
