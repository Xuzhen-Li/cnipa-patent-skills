# Pack manifest

- Edition: second
- Pack date: 2026-08-03
- Private bilingual working copy
- Author: Xuzhen Li

## What this pack does

This pack is one standalone skill line for invention patents (发明专利) only.

## Skill count

- Standalone entry skills: 2 (`01-patent-master-control`, `02-patent-init`)
- Workflow node skills: 10 (03 through 12)
- Total: 12

## Layout

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
  skills/<skill-name>/SKILL.md
  skills/<skill-name>/SKILL.zh-CN.md
```

Chinese guidance notes stay under `references/` and have an `.en.md` sibling. Final CNIPA filenames stay Chinese: `权利要求书.docx`, `说明书.docx`, `说明书摘要.docx`, `说明书附图.docx`, and `摘要附图`.

## Install scope

- `install.sh --target project <dir>` installs into `<dir>/.agents/skills`.
- `cursor`, `claude`, `codex`, and `all` install into the matching user skill directories only when that target is explicit.
- Reinstalling replaces only these 12 skill directory names. Other skills in the destination are left in place.
- `--mode copy` copies. `--mode link` symlinks. `--dry-run` writes nothing.

## Completeness

- The installer accepts the 12 skills in this manifest. It stops if any directory or `SKILL.md` is missing.
- The pack does not contain `.DS_Store`, caches, run products, user patent materials, or a global install directory.
- `tests/fixtures/` holds anonymous structured samples for the drawing-consistency script. It does not contain an inventor's real data.

## Start confirmation

- Before substantive work, `01-patent-master-control` shows a short notice: this is drafting assistance, not legal advice; a registered patent agent (专利代理师) should review the draft before filing; keep the invention confidential until filing.
- The user continues with a natural confirmation such as `yes` or `确认`. There is no fixed sentence and no confirmation record.
- Until the user agrees, do not create the delivery directory, read materials, call tools, or do patent work.

## Materials assessment and dynamic start

- Skill 02 first asks whether a patent framework, a patent draft, or related materials already exist.
- If any answer is yes, it creates `<nn>-user-existing-materials/` under `patent-deliverables/02-patent-init/input/`, starting at `01`. It does not overwrite or rewrite the originals.
- After the user confirms the files are in place, skill 02 assesses readiness for nodes 04–12 and recommends the earliest node that still needs work.
- Skill 03 reviews that evidence and routes to the recommended node. It does not always send existing materials to skill 07.
- After the recommended node finishes, the normal order continues through skill 12.

## Drawing constraints

- Skill 09 reviews the available text and materials, builds one fact source, freezes the Figure 1 master, and plans 3–7 drawings.
- Figures 2–7 are derived from that master. A complex device is not a set of unrelated text-to-image tasks.
- Skill 10 opens every actual image and checks them against each other. A structural contradiction is a hard failure and returns to skill 09.
- The abstract figure is chosen from the passed set. Skills 11 and 12 use only the passed drawing copies from skill 10.

## Node delivery

Each node creates:

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

The next skill reads the previous skill's `handoff/next-node-input.json`.

## Scripts

Three validators are unchanged in logic from the second edition:

- `skills/07-abstract-generator/scripts/validate_abstract.py`
- `skills/10-drawing-consistency-validator/scripts/validate_drawing_manifest.py`
- `skills/11-description-writer/scripts/validate_final_abstract.py`

Their JSON keys were already English. `validate_drawing_manifest.py` returns exit code 1 for a usage error; the abstract validators return 2. That difference was left as-is.
