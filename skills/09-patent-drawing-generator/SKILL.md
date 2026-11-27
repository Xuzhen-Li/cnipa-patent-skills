---
name: "09-patent-drawing-generator"
description: "用于以资深专利代理人和专利制图审查标准，审查全部技术文本，按机械装置、电气系统、软件、流程、化学/生物或混合类型建立唯一事实源和统一制图母版，动态规划 3–7 张附图；实体装置的生成式图片仅可作为原型，正式候选图必须来自可追溯的确定性矢量、CAD或受控工程源。"
---

# 09-patent-drawing-generator

## 节点目的

把附图制作作为专利技术表达和法定文件一致性工程，而不是独立图片生成任务。先锁定事实、权利要求、部件/步骤、标号和视图关系，再输出 3–7 张结构一致、来源可追溯、可交 10 审核的正式候选附图。

## 触发与输入

- 08 完成后、03 直接推荐本节点时，或 10 写入 `retry_skill=09-patent-drawing-generator` 后触发。
- 必须读取直接上游交接、02 用户素材、04–08 全部可用成果、已有说明书/草图/照片/CAD/尺寸资料及返工审计报告。
- 从 03 直达时，`next_skill` 与 `recommended_start_skill` 必须均为本节点，摘要和权利要求必须可用；不足时返回更早节点。

不得只读取摘要或权利要求后直接写提示词。冲突事实必须由发明人确认，不能由制图节点自行选择。

## 节点目录

创建 `patent-deliverables/09-patent-drawing-generator/` 及标准七类子目录，并在 `deliverables/` 下创建 `concept-prototypes/`、`deterministic-engineering-sources/`、`candidate-drawings/`。用户原始材料只读使用，所有版本必须保留来源和哈希。

## 必读制图规范

先读取 [references/分类型专利附图规范.md](references/分类型专利附图规范.md)，只加载与当前发明类型对应的章节及通用形式规则。混合发明读取所有相关章节。

## 制图类型分流

必须在开始绘图前写入 `drawing_route_type`：

- `mechanical_device`：机械、装置、实体结构。
- `electrical_circuit`：电路、控制系统、信号连接。
- `software_system`：软件模块、数据流、计算架构。
- `process_flow`：方法步骤、工艺流程、状态转换。
- `chemical_biological`：化学结构、反应/制备流程、生物实验或系统。
- `mixed`：两种以上类型共同表达。

不同类型采用不同母版：实体结构母版、电路拓扑母版、模块/数据字典母版、流程节点与分支母版或专业化学绘图源。不得用机械装置图规则强套所有发明。

## 唯一事实源与母版

1. 全文审查后建立 `technical-fact-source.json`、`part-or-step-master.json`、`structure-logic-matrix.json`、`motion-state-constraints.json` 和 `drawing-mark-master.json`。
2. 每项事实记录 `fact_id`、来源文件及位置、确认状态、关联权利要求和需要图示的原因。
3. 每个部件、模块或步骤使用唯一 ID，记录名称、数量、形状/符号、连接或顺序、位置/层级、输入输出、状态及稳定属性。
4. 先完成图1总体母版并冻结；图2–图7必须由同一工程源、拓扑或逻辑母版派生。
5. 允许差异仅包括已规划的视角、遮挡、剖切、爆炸间距、局部放大、工作状态或流程分支；不得改变身份、数量、形状特征、连接、安装位置、朝向、内外关系、步骤顺序或数据方向。

## 3–7 张动态规划

- 总数必须为 3–7 张，由技术表达需要决定，不固定为 3 张，也不为凑数增加重复图。
- 每幅图记录表达目的、覆盖事实/权利要求、不可替代性、视图类型、允许变化和禁止变化。
- 3 张足以完整表达时不得增加；7 张仍不足时停止并要求补充资料或专业制图，不得压缩掉必要结构。
- 摘要附图从 10 通过的图集中选择，不得另行生成结构变体。

## 正式制图路线

优先级为：已有 CAD/专业源文件规范重绘 → 程序化矢量工程图 → 基于冻结工程源的受控编辑 → 生成式图片概念原型。

- 对机械装置、实体产品和精确空间结构，生成式图片只能用于讨论构图和视角，不得直接作为正式候选图。
- 正式候选图必须由 CAD、SVG/矢量程序、专业电路/流程/化学绘图工具或可重现的受控工程源导出，并保存源文件、版本和导出参数。
- 生成式原型中的任何结构都不得反向写入事实源；只有原始披露和发明人确认可以改变事实源。
- 同类原型连续两轮仍出现结构漂移时立即停止生成式路线，要求补充尺寸、草图、照片或工程图。

## 执行步骤

1. 完成制图类型判定、全文事实审查、冲突解决及母版数据建立。
2. 生成 `drawing-view-plan.json`、`cross-view-constraints.json` 和 `drawing-form-spec.md`。
3. 制作图1总体母版，逐项核对事实、权利要求、部件/步骤、标号和技术关系，生成 `master-freeze-record.json`。
4. 按视图规划逐图制作，每次只派生一幅；每幅图保留工程源、导出版本、绘制规范和事实追溯。
5. 执行本节点预检：结构/逻辑、图间关系、标号、形式、缩放可读性和工程源可重现性。
6. 用户在外部工具制图时，逐图说明使用哪个母版、允许改动项、禁止项、命名和保存路径。完成后要求回复 `我已将全部候选附图放入指定文件夹`。
7. 核验实际存在 3–7 张图片及对应确定性工程源后，交接 10 并停止。

## 必需输出

- `deliverables/drawing-route-decision.md`
- `deliverables/technical-fact-source.json`
- `deliverables/part-or-step-master.json`
- `deliverables/structure-logic-matrix.json`
- `deliverables/motion-state-constraints.json`
- `deliverables/drawing-mark-master.json`
- `deliverables/drawing-view-plan.json`
- `deliverables/cross-view-constraints.json`
- `deliverables/drawing-form-spec.md`
- `deliverables/master-freeze-record.json`
- `deliverables/per-figure-drawing-spec.md`
- `deliverables/drawing-fact-trace.json`
- `deliverables/deterministic-source-manifest.json`
- `deliverables/candidate-drawing-manifest.json` 及 `candidate-drawings/` 中 3–7 张实际图片
- 三份标准过程记录及 `handoff/next-node-input.json`

## 交接规则

交接文件必须写明：

- `current_skill=09-patent-drawing-generator`
- `next_skill=10-drawing-consistency-validator`
- 已有素材、动态路由字段原样传递
- `drawing_route_type`、`technical_fact_source_file`、`part_or_step_master_file`
- `relationship_matrix_file`、`view_plan_file`、`cross_view_constraints_file`
- `master_freeze_file`、`deterministic_source_manifest_file`
- `candidate_figure_count`（3–7）、`candidate_figure_files`、`candidate_figure_hashes`
- `generative_prototypes_used`、`formal_candidates_are_deterministic`
- `source_files`、`deliverables`、`open_questions`、`quality_gate_status`、`can_continue`、`must_stop_reason`

## 质量门与阻断

- 制图类型、唯一事实源、总体母版、3–7 张视图必要性及跨图约束均已确认。
- 实体装置正式候选图全部来自确定性工程源；原型与正式图严格分区。
- 每张正式图均有可重现源文件、版本、哈希和事实/权利要求追溯。
- 形式规则、标号、剖切/局部/状态定义和缩放可读性通过预检。
- 母版未冻结、工程源缺失、图片数量越界、存在结构矛盾或用户未确认候选图时 `can_continue=false`。
- 不得通过修改事实、权利要求或说明书迁就错误图，不得绕过 10。
