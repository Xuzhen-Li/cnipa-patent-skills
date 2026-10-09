---
name: "07-abstract-generator"
description: "Draft a Chinese invention-patent abstract (说明书摘要) of at most 300 characters from the confirmed inventive concept. Skill 11-description-writer finalizes it. 用于依据已确认的总发明构思、核心技术方案和技术效果生成中国发明专利说明书摘要初稿，正文不超过 300 字；摘要初稿供后续权利要求和说明书使用，并由 11-description-writer 在全文及附图确定后完成最终定稿。"
---

# 07-abstract-generator

## Purpose

Using a senior patent attorney's method, write a structurally accurate and objectively worded draft abstract (说明书摘要). The abstract does not define the scope of protection. This node must not let the abstract narrow claims (权利要求书) that are not written yet. Skill 11 finalizes the abstract against the claims, the description (说明书), and the abstract figure (摘要附图) that passed the drawing check.

## Trigger and inputs

Run after skill 06 finishes, or when skill 03 recommends this node directly because the existing materials meet the conditions. Required inputs:

- The upstream handoff and every recommended source file.
- Title candidates, the general inventive concept, the technical problem, the core technical solution, the main technical effects, and the use.
- The essential/optional feature table, the evidence status of the effects, and the inventor's confirmation record.

When arriving directly from skill 03, check that each of those elements has a source. If not, return to the earlier node that should supply it.

## Node directory

In the current project, create `patent-deliverables/07-abstract-generator/` and the seven standard subdirectories. Every result stays there. User originals are read-only.

## Abstract rules

- The abstract body is at most 300 characters. Do not aim for the ceiling. Aim to state what is necessary and accurate.
- Usually organize it as title / technical field, the technical problem to be solved, the core technical solution, the main technical effect, and the main use.
- The core solution must show the main technical features and how they relate. Do not write only functions, goals, or effects.
- State only effects that have evidence. Do not write an unverified advantage as a settled fact.
- Do not use promotional language, evaluative language, language that promises a patent will be granted (承诺授权), language that widens the scope, or marketing language.
- Do not write the search history, an evaluation of the references, claim numbers, or embodiment details that are not needed.
- The title of the invention (发明名称) should state the subject to be protected accurately. Avoid trademarks, model numbers, slogans, and limitations that are not needed.
- This node only records what the abstract figure needs to express. The abstract figure is chosen later from the drawings that pass skill 10.

## Steps

1. Lock the confirmed general inventive concept, the essential core features, and the technical effects that have enough evidence.
2. Draft title candidates and check that they match the subject to be protected, the technical solution, and the later claim subject.
3. Build an abstract-element table. Tie each sentence to a fact source and an innovation layer.
4. Write the abstract body. Cut repeated background, optional features, and promotional effects.
5. Run `python3 scripts/validate_abstract.py <abstract-draft.md>` and confirm the abstract body is at most 300 non-whitespace characters. If it is over the limit, shorten the substance. Do not only delete necessary technical relationships.
6. Mark `abstract_status=preliminary`. List what skill 11 must fill back or re-check against the claims, the description, and the drawings.
7. After the user confirms the draft abstract, hand off to skill 08 and stop. Do not run skill 08 in the same turn.

## Required outputs

- `deliverables/abstract-draft.md`: the draft abstract, still the input skill 08 expects
- `deliverables/title-candidates.md`
- `deliverables/abstract-element-sources.json`
- `deliverables/abstract-character-check.json`
- `deliverables/abstract-finalization-checklist.md`
- The three standard process records and `handoff/next-node-input.json`

## Handoff rules

The handoff must state:

- `current_skill=07-abstract-generator`
- `next_skill=08-claims-writer`
- Existing-materials and dynamic-routing fields, copied unchanged
- `abstract_file`, `abstract_status=preliminary`, `abstract_character_count`
- `title_candidates_file`, `abstract_element_source_file`
- `abstract_drawing_requirements`, `finalization_required_at_skill=11-description-writer`
- `unverified_effects_excluded`, `source_files`, `deliverables`, `open_questions`
- `quality_gate_status`, `can_continue`, `must_stop_reason`

## Quality gate and stops

- The abstract body is at most 300 characters. The technical problem, core solution, effect, and use are objective and consistent with each other.
- Every substantive statement has a source. The abstract contains no unconfirmed parameter, structure, or technical effect.
- The title, the general inventive concept, and the subject to be protected agree.
- Do not pass the node if the character check fails, the core solution is unclear, or a key effect has no evidence.
- Do not mark the draft abstract as the final abstract. Do not generate an abstract figure on its own. Do not expand the text to hit a fixed length.
