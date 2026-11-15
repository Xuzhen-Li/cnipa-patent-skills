---
name: "12-patent-word-generator"
description: "用于汇总通过一致性校验的 3–7 张附图、摘要、权利要求书和说明书，生成发明专利 Word 终稿；也用于 03-invention-status-check 确认全部内容及附图校验记录完整后直接推荐终稿汇总。"
---

# 12-patent-word-generator

## 节点目的

生成发明专利 Word 终稿，并确保嵌入的所有图片均来自 10 的通过校验附图清单。

工作稿文件名为 `patent-final.docx`。若另外拆成中国国家知识产权局申请文件，文件名保持中文：`权利要求书.docx`、`说明书.docx`、`说明书摘要.docx`、`说明书附图.docx`，摘要附图保持 `摘要附图`。这些报送文件名不改成英文。

## 触发时机

- 11-description-writer 通过且用户确认后触发。
- 03 根据已有素材评估直接推荐本节点时触发，但必须具备完整正文、三向一致性记录和附图实图校验记录。

## 必需输入

- 说明书摘要、权利要求书、说明书和附图说明。
- 11 的 `handoff/next-node-input.json`，其中 `quality_gate_status=pass` 且 `can_continue=true`。
- 10 的通过校验附图清单、图片哈希、摘要附图选择记录和 `description-drawing-copies/`。
- 权利要求-说明书-附图三向对应表。
- 从 03 直接进入时：03 交接及能证明上述全部成果完整、相互一致且附图已通过实图校验的材料。

## 从 03 动态起步规则

- 仅当 03 的 `next_skill` 与 `recommended_start_skill` 均为本节点时，才允许跳过 04–11。
- 必须逐项核验全部正文、3–7 张附图、统一标号、三向一致性和实图校验记录。
- 附图未经验证时返回 10；说明书或三向对应不完整时返回 11；图片或结构基准缺失时返回 09。
- 本节点完成后写入 `END`。

## 必建节点目录

```text
patent-deliverables/12-patent-word-generator/
  input/
  output/
  process-records/
  handoff/
  deliverables/
  stages/
  patent-files/
```

## 执行步骤

1. 锁定全部正文版本和 10 的图片哈希清单。
2. 按发明专利文件顺序整理说明书摘要、摘要附图、权利要求书、说明书及说明书附图。
3. 摘要附图只使用 10 指定的通过校验图片；说明书附图只从 `description-drawing-copies/` 嵌入，不得使用其他候选图或重新生成图片。
4. 嵌入图片前逐一复算哈希并与通过清单比较；不一致时停止。
5. 检查图号顺序、附图说明、标号、分页、图片等比例缩放和缩放后辨识度。
6. 生成 Word 终稿、终稿内容清单和待代理师确认事项。
7. 交接文件 `next_skill=END`，本节点停止。

## 必需输出

- `deliverables/patent-final.docx`
- `deliverables/final-content-manifest.md`
- `deliverables/attorney-review-items.md`
- `deliverables/final-drawing-hashes.json`
- `process-records/process-log.md`、`open-questions.md`、`quality-gate-record.md`
- `handoff/next-node-input.json`

## 交接规则

`next-node-input.json` 必须写明：

- `current_skill`: `12-patent-word-generator`
- `next_skill`: `END`
- 已有素材、动态路由字段原样传递
- `validated_figure_count`: 3–7
- `validated_figure_files`、`validated_figure_hashes`、`abstract_figure_file`
- `embedded_figure_hashes`
- `source_files`、`deliverables`、`open_questions`
- `quality_gate_status`、`can_continue`、`must_stop_reason`

## 质量门

- 11 通过且三向对应完整，或已有材料达到等效标准。
- 附图实际数量为 3–7，全部来自 10 的通过清单，嵌入前后哈希一致。
- 摘要附图来自同一通过图集，没有独立生成的结构变体。
- 正文顺序、图号、标号、分页和缩放可读性符合终稿要求。
- 明确提示终稿仍需专利代理师审查。
- 目录、过程记录和 END 交接完整。

## 阻断条件

- 11 未通过，或缺少三向一致性记录。
- 图片不在 3–7 张范围、哈希不一致、来源不在通过清单，或存在未经校验图片。
- 缺少任一必需正文，或正文与附图说明不一致。
- 必需输入不完整。

## 禁止事项

- 不得嵌入未经 10 校验的图片，不得重新生成、局部修改或替换图片。
- 不得把简单拼版误判为完成质量核验，不得掩盖正文与附图矛盾。
- 不得启动新的发明专利节点，不得让终稿依赖聊天口头上下文。
