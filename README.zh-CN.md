# 发明专利 Skill

作者：Xuzhen Li

第二版发明专利流程的私人双语工作副本。它把技术想法写成中国发明专利（发明专利）的 Word 工作稿。它不代替专利代理师审查。

智能体（Codex、Claude Code、Cursor 等）加载各技能的 `SKILL.md`。`SKILL.zh-CN.md` 是同一套流程的中文全文。

## 安装

项目模式只安装到 `<目录>/.agents/skills`，并且只替换这 12 个同名技能。

```bash
bash install.sh --target project "/你的/项目路径" --mode copy
bash install.sh --target project "/你的/项目路径" --mode link --dry-run
```

只有在明确指定时，才安装到用户技能目录：

```bash
bash install.sh --target cursor
bash install.sh --target claude
bash install.sh --target codex
bash install.sh --target all
```

Windows：

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 --target project "C:\你的\项目路径"
powershell -ExecutionPolicy Bypass -File .\install.ps1 --target cursor --mode link --dry-run
```

`--mode copy` 是默认。`--mode link` 把每个已安装技能指向本包。`--dry-run` 只打印动作，不写入。`-h` 打印帮助。

安装到项目后，在该项目目录中打开所使用的智能体（Codex、Claude Code、Cursor 等）。若当前任务是在安装前创建的，请新建任务，使智能体重新发现项目级技能。

## 启动

可使用下列任一说法：

- `开始发明专利`
- `发明专利开始工作`
- `单独走发明专利流程`
- `把这个想法写成发明专利`
- `start invention patent`
- `turn this idea into an invention patent`

`01-patent-master-control` 在实质工作前展示下面的说明，并等待用户以 `yes` 或 `确认` 等自然表达表示同意。不设固定原句。

> 本流程只提供发明专利撰写辅助，不是法律意见。提交申请前应由注册专利代理师审查。在申请提交前，应对发明内容保密。

用户同意之前，不得创建交付目录、读取材料或撰写正文。

## 路线

`启动说明` → `01-patent-master-control` → `02-patent-init`（三项素材询问与评估）→ `03-invention-status-check` → 推荐的 04–12 节点 → 按正常顺序到 `12-patent-word-generator`。

进入 02 后，系统必须优先询问：

1. 是否已有专利框架？
2. 是否已完成专利初稿？
3. 是否已有专利相关材料？

若任一项为“是”，在 `patent-deliverables/02-patent-init/input/` 下创建 `<编号>-user-existing-materials/`，编号从 `01` 开始递增。原始文件放入该目录后回复 `我已将已有素材放入指定文件夹`。系统不会修改原始素材。

推荐依据文件内容和前置缺口，不按文件数量，也不由用户自行选择。若多个环节存在缺口，从编号最小的缺口节点开始，然后按正常顺序继续。

### 动态分支

- 三项均为“否”，或素材只是零散想法：03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12。
- 技术问题和核心方案明确，但缺检索：03 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12。
- 已有检索证据，但创新点未定：03 → 06 → 07 → 08 → 09 → 10 → 11 → 12。
- 创新点明确，但缺可用摘要：03 → 07 → 08 → 09 → 10 → 11 → 12。
- 摘要和核心特征可用，但权利要求待处理：03 → 08 → 09 → 10 → 11 → 12。
- 摘要和权利要求可用，但缺少合格附图、统一事实源或母版：03 → 09 → 10 → 11 → 12。
- 已有 3–7 张候选附图，但未经逐张实图一致性校验：03 → 10 → 11 → 12。
- 附图已通过实图校验，但说明书待处理：03 → 11 → 12。
- 正文、3–7 张附图、实图校验和三向一致性记录均完整，仅待汇总：03 → 12。

03 必须根据文件实际内容选择最早需要补齐的节点。不得仅凭文件数量、文件名或用户声称“已有完整初稿”跳过前置缺口。

## 附图质量门

- 附图总数按技术表达需要确定，必须为 3–7 张，不固定为 3 张，也不要求写满 7 张。
- 09 先审查全部可用材料并冻结图1整体结构母版，其他视图必须从同一母版派生。
- 摘要附图从通过校验的图集中选择，不再独立生成另一套结构。
- 10 必须打开全部实际图片，逐张检查事实、跨图、权利要求和标号一致性；结构矛盾必须退回 09。
- 同类生成式结构错误连续两轮后，必须切换 CAD、矢量或受控参考图编辑，或要求补充图纸、尺寸和结构资料。
- 11 和 12 只能使用 10 通过校验且哈希一致的附图副本。

任何部件增减、换形、换连接、位置漂移、朝向改变或内外关系矛盾都必须在 10 阻断并返回 09。任一图片重绘后，10 重新检查全套图片。

## 交接

每个节点输出 `patent-deliverables/<技能名>/handoff/next-node-input.json` 后，才允许进入下一个节点。从 03 动态起步时，还必须传递素材目录、评估状态、推荐节点和路由来源。若节点写入 `can_continue=false`，总控必须停止并说明缺口。

每个节点使用：

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

## 技能

| 目录 | 作用 |
| --- | --- |
| `01-patent-master-control` | 启动门槛与调度 |
| `02-patent-init` | 素材三问、评估、起始节点推荐 |
| `03-invention-status-check` | 复核并动态路由 |
| `04-patent-topic-selector` | 技术披露与检索要素 |
| `05-patent-prior-art-search` | 现有技术检索、新颖性、创造性 |
| `06-innovation-point-finder` | 总的发明构思与创新层级 |
| `07-abstract-generator` | 摘要初稿，不超过 300 字 |
| `08-claims-writer` | 权利要求书，不超过 10 项 |
| `09-patent-drawing-generator` | 母版与 3–7 张候选附图 |
| `10-drawing-consistency-validator` | 附图实质门与形式门 |
| `11-description-writer` | 说明书与摘要定稿 |
| `12-patent-word-generator` | Word 工作稿 |

合并工作稿为 `patent-final.docx`。拆开的中国申请文件保持中文文件名：`权利要求书.docx`、`说明书.docx`、`说明书摘要.docx`、`说明书附图.docx` 和 `摘要附图`。

重命名表：`docs/rename_map.json`。包说明：`docs/PACK_MANIFEST.md`。
