---
name: "10-drawing-consistency-validator"
description: "Open each of the 3–7 candidate images and run the substantive consistency gate and the formal compliance gate, including mark checks, difference overlays, confidence, and hashes. 用于以独立专利附图审查视角打开并逐幅检查 3–7 张实际候选图，分别执行结构与逻辑实质一致性门、专利附图形式合规门，并通过 OCR/人工标号核验、差异叠加、观察置信度和哈希锁定阻断部件漂移、连接矛盾及形式缺陷。"
---

# 10-drawing-consistency-validator

## 节点目的

作为独立质量门，对实际图像而非提示词或文件名进行审查。必须先通过“实质一致性门”，再通过“形式合规门”；任一门未通过均不得进入说明书。

## 触发与输入

- 09 输出 3–7 张正式候选图并允许继续后触发。
- 03 判断用户已有 3–7 张附图但未经独立实图校验时可直达；不能重建可靠事实源、母版或工程源时返回 09。
- 必须读取上游交接、候选图、确定性工程源清单、事实源、部件/步骤主数据、关系矩阵、状态约束、权利要求、视图规划、标号主表和母版冻结记录。

用户原始图片只读使用。候选图少于 3 张、多于 7 张或任一图不可打开时立即阻断。

## 节点目录与审查基准

创建 `patent-deliverables/10-drawing-consistency-validator/` 及标准七类子目录，并在 `deliverables/` 下创建 `difference-overlays/`、`issue-evidence-screenshots/` 和 `description-drawing-copies/`。

审查前读取 [references/附图双重质量门检查表.md](references/附图双重质量门检查表.md)。

## 基础取证

1. 枚举全部候选图，记录文件路径、SHA-256、格式、像素尺寸、颜色模式、工程源、导出版本和修改时间。
2. 使用可视图像工具逐张打开原始尺寸图片，记录视图类型、方向、可见部件/步骤、标号、连接、位置和形式问题。任何图未实际打开不得放行。
3. 对可比较视图制作轮廓或透明度差异叠加图，辅助识别部件漂移、比例异常、接口变化和标号位移。不同视角不能机械像素相减，必须结合母版和视图定义解释。
4. 使用 OCR 或图像识别提取标号和必要文字，再由人工/模型目视复核；OCR 只作辅助证据，不得替代视觉确认。
5. 每个观察项标记 `high`、`medium` 或 `low` 置信度及原因。关键结构为 `medium/low` 时必须进入人工复核，未确认前不得判 pass。

## 第一质量门：实质一致性

1. 根据实际观察建立 `cross-view-part-or-step-list.json`。可见稳定属性写入 `observed_attributes`；确因剖切、遮挡或视角不可判断的字段写入 `not_observable` 和具体原因。
2. 以 09 的 `part-or-step-master.json` 和 `drawing-mark-master.json` 为只读来源，在本节点 `input/` 内建立 `script-part-master.json`。该文件必须使用脚本所需字段：顶层 `parts`；每个部件包含 `part_id`、`drawing_mark`、`standard_name`、`quantity` 和字典形式的 `stable_attributes`。`stable_attributes` 的键必须与跨图清单中的 `observed_attributes`/`not_observable` 键一致。必须记录来源文件和字段映射，不得改写 09 的原始主数据。
3. 运行：

```bash
python3 scripts/validate_drawing_manifest.py <script-part-master.json> <cross-view-part-or-step-list.json>
```

脚本失败不得放行，脚本通过也不能替代视觉审查。

4. 执行五层核验：图与事实源、图与图、图与权利要求、标号与主数据、正式图与确定性工程源一致。
5. 对实体结构核验身份、数量、形状、连接、安装位置、朝向、内外关系、运动和状态；对电路/软件/流程核验模块、端口、信号、数据、步骤、分支、顺序和执行主体；化学/生物图核验结构、键型、取代位置、反应或实验流程。
6. 只有预先声明且事实源支持的视角、剖切、爆炸、局部放大和工作状态差异可以接受。

以下均为硬失败：无依据增删部件/步骤、换形、镜像关键结构、换连接、位置漂移、朝向或内外关系改变、信号/步骤方向改变、同一状态数量不一致、一号多物或一物多号。

## 第二质量门：形式合规

在实质门通过后检查：

- 3–7 张图的图号连续、引用完整，摘要附图来自同一图集。
- 白底黑线、轮廓和符号清晰，无照片感、颜色、灰度渲染、阴影、渐变或装饰背景。
- 标号、引出线、箭头、剖切符号、局部放大和状态标记清楚，不压盖关键结构。
- 无无关文字、宣传说明、无依据尺寸或比例；必要文字与说明书术语一致。
- 缩放到申请文件版面后仍可辨认；页面方向、留白、分图布局和输出清晰度符合当前适用的电子申请要求。
- 正式图均有可重现工程源，且导出图与源文件一致。

形式规则存在版本或解释不确定时，标记待执业代理师复核，不得用主观猜测判 pass。

## 判定与返工

- `pass`：两个质量门均通过，所有关键观察为高置信度或已完成人工确认。
- `warning`：只有不改变技术内容的轻微形式问题；警告未关闭前 `can_continue=false`。
- `fail`：任何实质矛盾、关键不可辨识、工程源不一致或严重形式缺陷。

失败时输出具体图片、问题位置、部件/步骤 ID、事实 ID、权利要求、证据截图和定向修正要求，并写入 `next_skill=null`、`can_continue=false`、`retry_skill=09-patent-drawing-generator`。

任何修图，包括只改标号、引出线、版面或清晰度，都必须：

1. 生成新版本和新哈希，不得覆盖已审版本。
2. 重新检查全套 3–7 张图的两个质量门。
3. 更新差异叠加、OCR/标号记录和通过清单。

## 必需输出

- `deliverables/candidate-drawing-evidence.json`
- `deliverables/cross-view-part-or-step-list.json`
- `input/script-part-master.json`
- `deliverables/substantive-consistency-gate.json`
- `deliverables/formal-compliance-gate.json`
- `deliverables/ocr-manual-mark-review.json`
- `deliverables/observation-confidence-review.json`
- `deliverables/difference-overlay-analysis.md` 及 `difference-overlays/`
- `deliverables/drawing-consistency-audit.md`
- `deliverables/inconsistency-issues.md`
- `deliverables/validated-drawing-manifest.json`
- `deliverables/abstract-figure-selection.json`
- `deliverables/description-drawing-copies/`
- 三份标准过程记录及 `handoff/next-node-input.json`

## 放行与交接

完成审计后必须停止。只有两个质量门均为 pass、所有警告关闭、关键低置信度项已人工确认且用户确认审计结果后，交接文件才可写入：

- `current_skill=10-drawing-consistency-validator`
- `next_skill=11-description-writer`
- 已有素材、动态路由字段原样传递
- `substantive_gate_status=pass`、`formal_gate_status=pass`
- `validated_figure_count`（3–7）、`validated_figure_files`、`validated_figure_hashes`
- `abstract_figure_file`、`engineering_source_manifest_file`
- `ocr_review_status`、`human_review_status`、`unresolved_low_confidence_items=[]`
- `quality_gate_status=pass`、`can_continue=true`、`retry_allowed=false`

不得同轮执行 11。

## 禁止事项

- 不得只检查提示词、文件名、日志、OCR 或结构化清单。
- 不得将结构矛盾降级为形式警告，不得用“视角不同”笼统解释。
- 不得在人工未确认关键中低置信度观察时自动放行。
- 不得把未经校验、校验后改动或哈希不一致的图片复制给 11 或 12。
