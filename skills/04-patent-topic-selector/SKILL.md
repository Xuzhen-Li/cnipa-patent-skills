---
name: "04-patent-topic-selector"
description: "Organize a confirmed technical disclosure, screen patentable subject matter, unity, commercial coverage, and infringement detectability, and prepare search elements. Do not invent technology the inventor did not disclose. 用于从简单发明想法或 03-invention-status-check 推荐的早期材料中挖掘技术披露，建立技术问题—技术手段—技术效果链，初筛可专利主题、总的发明构思、单一性、商业覆盖和侵权可识别性，并形成可复核检索要素；不得替发明人虚构技术方案。"
---

# 04-patent-topic-selector

## Purpose

Using a senior invention-patent attorney's working method, turn scattered ideas into a technical disclosure the inventor can confirm, that can be searched, and that can later become claims (权利要求书). This node finds and organizes technical contribution that already exists. It does not invent structures, steps, parameters, or effects the inventor does not have.

## Trigger and inputs

Run when skill 03 names this node as the earliest one that still needs work. Required inputs:

- Skill 03's `handoff/next-node-input.json`, with both `next_skill` and `recommended_start_skill` set to this node.
- The user's inventive idea, the use setting, and every source file skill 03 recommended.
- Any prototype, sketch, flow, experiment, failure record, or requirements material. If none exists, record that absence.

User materials are read-only. If the materials do not even identify the technical object and its basic use, return to skill 03. Do not fill the gap by invention.

## Node directory

In the current project, create `patent-deliverables/04-patent-topic-selector/` and the seven standard subdirectories: `input/`, `output/`, `process-records/`, `handoff/`, `deliverables/`, `stages/`, and `patent-files/`. Every result stays there. Do not edit the user's original files.

## Working rules

- Mark every item as `用户明确确认` (confirmed by the user), `材料直接记载` (stated directly in the materials), `代理人归纳` (attorney restatement), `代理人建议设想` (attorney proposal), or `待发明人确认` (awaiting the inventor).
- An attorney restatement must not change the technical meaning. A proposal must not go straight into later patent text or claims.
- Prefer technical means that actually solve a technical problem. Do not treat a business goal, a wished-for function, a use benefit, or a slogan as the invention.
- Also consider patentable subject matter (保护客体), unity (单一性), whether the invention can be carried out (可实施性), commercial coverage, how hard the invention is to design around, and how detectable infringement would be. This node does not make a final novelty or inventive-step conclusion.

## Steps

1. Build a source list and `fact-hypothesis-layers.json`. For each item, record where it came from and its confirmation status.
2. Separate the technical field, technical object, use setting, current practice, concrete defects, and constraints.
3. Build `problem-means-effect-chain.json`. Every effect must be tied to the technical feature that produces it. If the basis is missing, mark it as awaiting verification.
4. Screen whether the matter is a technical solution. Flag pure business rules, rules for mental activities, diagnostic or therapeutic methods, purely aesthetic designs, or other subject-matter risks. Output a risk note only. Do not issue a definitive legal conclusion on your own.
5. From confirmed facts, state one or more candidate inventive concepts. Separate the core technical contribution, cooperating features, implementation details, and alternatives.
6. Make a first pass on whether the candidates share one general inventive concept (总的发明构思). Record themes that have no technical relationship separately. Do not force them together.
7. Assess candidate protection themes for product coverage, competing solutions, likely design-around paths, and whether infringement evidence could be obtained.
8. Turn unconfirmed structures, parameters, effects, and alternatives into a question list and ask the inventor to confirm each item. An unconfirmed proposal must not enter the search fact set.
9. From confirmed content, write Chinese and English keywords, synonyms, broader and narrower concepts, part relationships, functional relationships, and possible IPC/CPC directions, and hand them to skill 05.
10. After the user confirms the boundary of the technical facts and the candidate inventive concepts, write the handoff and stop. Do not run skill 05 in the same turn.

## Required outputs

- `deliverables/technical-disclosure.md`
- `deliverables/fact-hypothesis-layers.json`
- `deliverables/problem-means-effect-chain.json`
- `deliverables/patentable-subject-screen.md`
- `deliverables/candidate-concepts-unity.md`
- `deliverables/commercial-coverage-detectability.md`
- `deliverables/search-elements-keywords.json`
- `deliverables/inventor-open-questions.md`
- The three standard process records (`process-log.md`, `open-questions.md`, `quality-gate-record.md`) and `handoff/next-node-input.json`

## Handoff rules

The handoff must state:

- `current_skill=04-patent-topic-selector`
- `next_skill=05-patent-prior-art-search`
- Existing-materials and dynamic-routing fields, copied unchanged
- `confirmed_fact_file`, `problem_solution_effect_file`, `candidate_inventive_concepts_file`
- `subject_matter_risks`, `unity_risks`, `design_around_risks`, `detectability_risks`
- `inventor_confirmation_status`, `unconfirmed_proposals`
- `search_elements_file`, `source_files`, `deliverables`, `open_questions`
- `quality_gate_status`, `can_continue`, `must_stop_reason`

## Quality gate and stops

- The technical problem, technical means, and technical effect form a sourced causal chain.
- Confirmed facts stay strictly separate from attorney proposals. Every element proposed for search has a factual basis.
- Candidate concepts have a preliminary technical character, can be carried out, and have a clear search boundary.
- Set `can_continue=false` when the inventor has not confirmed a key fact, a technical effect, or a proposal.
- Stop and list the materials needed when a subject-matter, ownership, publication, or authenticity risk cannot be judged.
- Do not promise that a patent will be granted. Do not package market demand or an ideal function as a finished technical solution.
