# 交付清单

- 版本：第二版
- 整理日期：2026-08-03
- 私人双语工作副本
- 作者：Xuzhen Li

## 包用途

本包是发明专利路线的独立技能流程，只处理发明专利。

## 技能数量

- 发明专利独立入口技能：2 个（`01-patent-master-control`、`02-patent-init`）
- 工作流节点技能：10 个（03 至 12）
- 合计：12 个

## 目录

```text
patent-skills-private/
  README.md
  README.zh-CN.md
  install.sh
  install.ps1
  docs/PACK_MANIFEST.md
  docs/PACK_MANIFEST.zh-CN.md
  docs/rename_map.json
  docs/apply_rename_map.py
  skills/<技能名>/SKILL.md
  skills/<技能名>/SKILL.zh-CN.md
```

`references/` 中的中文审查说明保留原文件名，并另有 `.en.md`。中国申请文件若拆开保存，文件名保持：`权利要求书.docx`、`说明书.docx`、`说明书摘要.docx`、`说明书附图.docx` 和 `摘要附图`。

## 安装范围

- `install.sh --target project <目录>` 安装到 `<目录>/.agents/skills`。
- `cursor`、`claude`、`codex`、`all` 只有在明确指定时才写入对应用户技能目录。
- 重新安装时只替换这 12 个同名技能，不删除目标中的其他技能。
- `--mode copy` 复制。`--mode link` 做符号链接。`--dry-run` 不写入。

## 完整性

- 安装器只安装本清单中的 12 个技能。缺少任一目录或 `SKILL.md` 时立即停止。
- 本包不包含 `.DS_Store`、缓存、运行产物、用户专利材料或已经装好的全局目录。
- `tests/fixtures/` 只包含附图一致性校验脚本所需的匿名结构化样例，不含发明人的真实数据。

## 启动说明

- 正式工作前，`01-patent-master-control` 说明：这是撰写辅助，不是法律意见；提交前应由注册专利代理师审查；申请前对发明保密。
- 用户以 `yes` 或 `确认` 等自然表达表示同意即可。不设固定原句，也不写确认记录。
- 用户同意之前，不得创建交付目录、读取材料、调用工具或开展专利实质工作。

## 素材评估与动态起步

- 02 必须优先询问是否已有专利框架、是否已完成专利初稿、是否已有专利相关材料。
- 任一项为“是”时，在 `patent-deliverables/02-patent-init/input/` 下创建 `<编号>-user-existing-materials/`，编号从 `01` 起递增，不得覆盖或改写原始素材。
- 用户确认素材已放置后，02 必须逐文件评估 04 至 12 的就绪度，并推荐最早需要补齐的节点。
- 03 必须复核评估证据，并动态路由到推荐节点，不得固定把已有材料路由到 07。
- 被推荐节点完成后，恢复原有顺序继续推进到 12。

## 附图约束

- 09 必须审查全部可用文本和素材，建立唯一事实源，冻结图1整体结构母版，并按技术表达需要规划 3–7 张附图。
- 图2–图7必须从同一母版派生。复杂装置不得作为互不相关的独立文生图任务。
- 10 必须打开全部实际图片执行独立跨图校验。结构矛盾是硬失败，必须退回 09。
- 摘要附图从通过校验的图集中选择。11 和 12 只能使用 10 输出的通过校验附图副本。

## 节点交付

每个节点必须创建：

```text
patent-deliverables/<技能名>/
  input/
  output/
  process-records/
  handoff/
  deliverables/
  stages/
  patent-files/
```

下一个技能的输入必须来自上一个技能的 `handoff/next-node-input.json`。

## 脚本

三个校验脚本的逻辑与第二版一致：

- `skills/07-abstract-generator/scripts/validate_abstract.py`
- `skills/10-drawing-consistency-validator/scripts/validate_drawing_manifest.py`
- `skills/11-description-writer/scripts/validate_final_abstract.py`

脚本使用的 JSON 键本来就是英文。`validate_drawing_manifest.py` 在用法错误时返回退出码 1，两个摘要脚本返回 2。这一差别保持原样。
