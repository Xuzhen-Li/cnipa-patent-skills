# Invention patent skills

Author: Xuzhen Li

Private bilingual working copy of the second-edition invention-patent skill workflow. It drafts a Chinese invention patent (发明专利) from a technical idea through a Word draft. It does not replace review by a patent attorney (专利代理师).

The agent (Codex, Claude Code, Cursor, …) loads each skill from `SKILL.md`. `SKILL.zh-CN.md` is the same workflow in Chinese.

## Install

Project mode installs only into `<dir>/.agents/skills` and replaces only these 12 skill names.

```bash
bash install.sh --target project "/your/project" --mode copy
bash install.sh --target project "/your/project" --mode link --dry-run
```

User skill directories, only when you ask for them:

```bash
bash install.sh --target cursor
bash install.sh --target claude
bash install.sh --target codex
bash install.sh --target all
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 --target project "C:\your\project"
powershell -ExecutionPolicy Bypass -File .\install.ps1 --target cursor --mode link --dry-run
```

`--mode copy` is the default. `--mode link` points each installed skill at this pack. `--dry-run` prints the actions and writes nothing. `-h` prints help.

After installing into a project, open that project in the agent (Codex, Claude Code, Cursor, …). If the current task was created before installation, start a new task so the agent discovers the project skills.

## Start

Say any of these:

- `开始发明专利`
- `发明专利开始工作`
- `单独走发明专利流程`
- `把这个想法写成发明专利`
- `start invention patent`
- `turn this idea into an invention patent`

`01-patent-master-control` shows this notice before any substantive work, then waits for a natural confirmation such as `yes` or `确认`. There is no fixed sentence.

> This workflow is drafting assistance, not legal advice. A registered patent agent (专利代理师) should review the draft before filing. Keep the invention confidential until filing.

Until the user agrees, do not create the delivery directory, read materials, or draft.

## Route

`start confirmation` → `01-patent-master-control` → `02-patent-init` (materials questions and assessment) → `03-invention-status-check` → the recommended node among 04–12 → normal order through `12-patent-word-generator`.

After skill 02 starts, it asks, before any other setup question:

1. Is there already a patent framework?
2. Is there already a patent draft?
3. Are there already related patent materials?

If any answer is yes, skill 02 creates `patent-deliverables/02-patent-init/input/<nn>-user-existing-materials/`, starting at `01`. After you put the original files there, reply `我已将已有素材放入指定文件夹`. The originals are not modified.

The recommendation uses file contents and missing prerequisites, not file count, and not a node you pick. If several gaps exist, start at the lowest-numbered gap and then continue in order.

### Dynamic branches

- No materials, or only scattered ideas: 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12.
- Technical problem and core solution are clear, but search is missing: 03 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12.
- Search evidence exists, innovation points are not settled: 03 → 06 → 07 → 08 → 09 → 10 → 11 → 12.
- Innovation points are clear, usable abstract is missing: 03 → 07 → 08 → 09 → 10 → 11 → 12.
- Abstract and core features are usable, claims still need work: 03 → 08 → 09 → 10 → 11 → 12.
- Abstract and claims are usable, but qualified drawings, a single fact source, or a master is missing: 03 → 09 → 10 → 11 → 12.
- 3–7 candidate drawings exist but have not been checked image by image: 03 → 10 → 11 → 12.
- Drawings passed the image check, description still needs work: 03 → 11 → 12.
- Text, 3–7 drawings, the image check, and the three-way consistency record are complete: 03 → 12.

Skill 03 chooses the earliest node that still needs work from the file contents. It must not skip an earlier gap because of a file count, a file name, or a claim that a complete draft already exists.

## Drawing gates

- The drawing count is whatever the technology needs, and it must be 3–7. It is not fixed at 3, and it does not have to fill 7.
- Skill 09 reviews the available materials and freezes a Figure 1 (图1) master. Later views are derived from that master.
- The abstract figure (摘要附图) is chosen from the set that passes the check. It is not a second structure.
- Skill 10 opens every actual image and checks facts, cross-view consistency, claims, and marks. A structural contradiction goes back to skill 09.
- After two rounds of the same class of generative structural error, switch to CAD, vector, or controlled reference-image editing, or ask for drawings, dimensions, and structural data.
- Skills 11 and 12 may use only the drawing copies that passed skill 10 and whose hashes match.

Any added or removed part, shape change, connection change, position drift, orientation change, or inside/outside contradiction stops at skill 10 and returns to skill 09. After any image is redrawn, skill 10 checks the full set again.

## Handoff

A node may be followed only after it writes `patent-deliverables/<skill-name>/handoff/next-node-input.json`. A dynamic start from skill 03 also carries the materials directory, assessment status, recommended node, and routing source. If a node sets `can_continue=false`, the controller stops and tells you the gap.

Each node uses:

```text
patent-deliverables/<skill-name>/
  input/
  output/
  process-records/
  handoff/
  deliverables/
  stages/
  patent-files/
```

## Skills

| Directory | Role |
| --- | --- |
| `01-patent-master-control` | Start gate and scheduling |
| `02-patent-init` | Materials questions, assessment, start-node recommendation |
| `03-invention-status-check` | Review and dynamic route |
| `04-patent-topic-selector` | Technical disclosure and search elements |
| `05-patent-prior-art-search` | Prior-art search, novelty, inventive step |
| `06-innovation-point-finder` | General inventive concept and innovation layers |
| `07-abstract-generator` | Draft abstract, at most 300 characters |
| `08-claims-writer` | Claims, at most 10 |
| `09-patent-drawing-generator` | Master and 3–7 candidate drawings |
| `10-drawing-consistency-validator` | Substantive and formal drawing gates |
| `11-description-writer` | Description and final abstract |
| `12-patent-word-generator` | Word draft |

The combined working draft is `patent-final.docx`. Split CNIPA filing files keep Chinese names: `权利要求书.docx`, `说明书.docx`, `说明书摘要.docx`, `说明书附图.docx`, and `摘要附图`.

Rename table: `docs/rename_map.json`. Pack notes: `docs/PACK_MANIFEST.md`.
