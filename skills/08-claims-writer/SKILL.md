---
name: "08-claims-writer"
description: "Write or rebuild claims (权利要求书): at most 10 claims, clear dependencies, and support in the description. Design the hierarchy and dependency tree before the claim text. Also used when 03-invention-status-check routes existing materials here. 用于撰写或重构发明专利权利要求书，以保护范围完整、引用清晰、得到说明书支持为准，总项数不超过10项；先设计保护层级和依赖树，再撰写正文并校验引用与支撑关系。也用于 03-invention-status-check 根据已有框架或初稿直接推荐权利要求处理时。"
---

# 08-claims-writer

## Purpose

Produce a claim set (权利要求书) whose scope is complete, whose citation hierarchy is clear, which has reasonable fallback positions, and which is supported by the description (说明书) or by a confirmed fact source. The total is at most 10 claims.

## When it runs

Run after `07-abstract-generator` finishes, or when `03-invention-status-check` recommends this node directly from the materials assessment.

## Required inputs

- The abstract (说明书摘要).
- Settled innovation points or existing materials.
- The core technical-feature table.
- An existing description, patent framework, or draft. If there is no description yet, there must be a confirmed technical fact source that the later description can implement.
- If entering from skill 03: that handoff and its `recommended_source_files`.

## Direct entry from skill 03

- Skip skills 04–07 and enter this node only when both `next_skill` and `recommended_start_skill` in the skill 03 handoff are `08-claims-writer`.
- Confirm that a usable abstract, clear innovation points, and core technical features already exist, or that the draft contains enough corresponding content to rebuild the claims. User materials are read-only. Do not edit the original files.
- If a prerequisite is missing, stop and return to skill 03 so the work starts at the earlier node that is actually needed. Do not invent technical features in order to fill out the claims.
- After this node, return to the normal order and hand off to `09-patent-drawing-generator`.

## Required node directory

Before substantive work, create this directory in the current patent project. The directory name must match this skill name. Do not add a project-number level.

```text
patent-deliverables/08-claims-writer/
  input/
  output/
  process-records/
  handoff/
  deliverables/
  stages/
  patent-files/
```

Process records, stage files, patent text, drawings, intermediate Word files, and other patent files from this node stay inside this directory. Do not also create `stages/`, `process-records/`, or `patent-files/` at the project root.

## Steps

1. Identify the subject to be protected, the essential technical features, the optional limitations, and the different categories of subject matter.
2. Decide how many independent claims are needed, and of which categories, from the technical solution. Do not add independent claims just to increase the count.
3. Before writing the claim text, write `claim-scope-hierarchy.md`, `claim-dependency-tree.json`, and `claim-feature-map.json`.
4. Design the core trunk, parallel branches, and layered fallback positions under "Citation and protection-layer rules".
5. Set the actual count from the protection needed and the factual support. Include at least one independent claim. Independent claims plus dependent claims must total at most 10. Do not fill all 10 unless they are needed.
6. Write the text from the dependency tree. A dependent claim must have a citation part and a new limitation, and it may cite only an earlier claim.
7. Map every essential technical feature and every new limitation to a specific support location in the existing description. If there is no description yet, map it to the confirmed fact source and record the support the later description must supply.
8. If the candidate protection points would push the total over 10, reorganize under "What to do when there are more than 10". Do not simply cut the text off.
9. Check numbering, citations, dependency depth, fact sources, description support, consistent terminology, and the total count, and write `claims-quality-check.md`.
10. After every quality gate passes, write the handoff and recommend `09-patent-drawing-generator` next. Then stop.

## Citation and protection-layer rules

- Each independent claim is the root of a dependency tree. Different categories of protection may have separate branches, but they must fit the technical subject and unity (单一性).
- First-level dependent claims limit a key subsystem, structure, step, parameter, material, or way of applying the invention, and may cite the corresponding independent claim directly.
- Later dependent claims should cite the closest earlier claim that already contains their prerequisite features, so the fallback runs wide, then medium, then narrow.
- Parallel technical solutions that do not depend on each other may each cite the independent claim directly. Do not string every dependent claim into one long chain just to manufacture depth.
- Do not, without analysis, make every dependent claim cite claim 1 directly. If every dependent claim really is a parallel solution, `claim-scope-hierarchy.md` must prove item by item that there is no prerequisite dependency and must state why the direct citation is right. If that cannot be proved, rebuild the tree.
- For every dependent claim, record `parent_claims`, the new limitation, the prerequisite features, the fallback value, the fact source, and the description-support need.
- A multiple-dependent claim must cite earlier claims in the alternative. It must not be the basis of another multiple-dependent claim.
- Keep the claim subject name, part names, step names, drawing marks, and the cited claim numbers consistent.

## What to do when there are more than 10

1. Do not simply delete claim 11 and everything after it, and do not cut off text that is already numbered.
2. Merge limitations that repeat, overlap, or protect almost the same fallback point in different words.
3. Rank by inventive contribution, commercial value, how detectable infringement would be, and fallback value, and keep a core set of at most 10 claims.
4. Write anything left out of the formal claims into `backup-protection-points.md`, with the reason it was left out and the suggested handling.

## Required outputs

Formal results for this node go under:

- `patent-deliverables/08-claims-writer/deliverables/`

Process records:

- `patent-deliverables/08-claims-writer/process-records/process-log.md`
- `patent-deliverables/08-claims-writer/process-records/open-questions.md`
- `patent-deliverables/08-claims-writer/process-records/quality-gate-record.md`

Handoff:

- `patent-deliverables/08-claims-writer/handoff/next-node-input.json`

Required files:

- `claims.md`
- `claim-scope-hierarchy.md`
- `claim-dependency-tree.json`
- `claim-feature-map.json`
- `claim-structure.json`
- `claim-scope-notes.md`
- `backup-protection-points.md`
- `claims-quality-check.md`
- `next-node-input.json`

## Standalone run and user confirmation

- This node only designs the protection layers and dependency tree, and writes the claims, the feature map, the structure table, the scope note, the backup points, the quality check, and the handoff.
- When this node finishes, stop. Show the main output paths, a short claim-structure summary, and the next-node suggestion.
- Run `09-patent-drawing-generator` only in a later turn, after the user clearly says to continue or to enter the next step.
- Do not run `09-patent-drawing-generator` in the same turn as this node.

## Handoff rules

`next-node-input.json` must include:

- `current_skill`: `08-claims-writer`
- `next_skill`: `09-patent-drawing-generator`
- `existing_materials_folder`: same as upstream
- `materials_assessment_status`: same as upstream
- `recommended_start_skill`: same as upstream
- `routing_origin_skill`: same as upstream
- `claims_total`: total claim count, from 1 to 10
- `independent_claims`: list of independent-claim numbers
- `dependent_claims`: list of dependent-claim numbers
- `claim_tree_file`: path of `claim-dependency-tree.json`
- `support_mapping_file`: path of `claim-feature-map.json`
- `drawing_required_features`: claim features, part relationships, and claim numbers that the drawings must show
- `drawing_fact_sources`: the fact sources of those drawing elements and where the description supports them
- `claim_count_limit_passed`: true / false
- `claim_dependency_check_passed`: true / false
- `specification_support_check_passed`: true / false
- `source_files`: files this node read
- `deliverables`: results this node produced
- `open_questions`: questions for the user or the patent attorney
- `quality_gate_status`: `pass`, `warning`, or `fail`
- `can_continue`: whether the next node may start
- `must_stop_reason`: the reason, if it may not

## Quality gate

- If this node was entered from skill 03, it must match skill 03's recommendation, and the recommended materials must include a usable abstract, clear innovation points, and core technical features.
- Finish the protection-layer design, the dependency tree, and the feature map before writing the claim text.
- Judge by complete scope, clear citations, and support in the description. The total is at most 10 claims.
- There must be at least one independent claim.
- Numbering must be continuous. Every citation must point to an earlier claim, with no cycle.
- Dependent claims must form a trunk and branches that have a reason. Do not cite claim 1 from every dependent claim without analysis, and do not string them into one mechanical chain.
- A multiple-dependent claim must cite in the alternative, and must not cite another multiple-dependent claim.
- Every new limitation must have a fact source and support in an existing description. If there is no description yet, there must be an explicit support requirement for the later description.
- When a description already exists, the feature map must name the supporting file and the location. Do not write only "the description mentions it".
- Do not invent technical facts that the user did not provide and that search did not support.
- Each node creates `patent-deliverables/<skill-name>/` with no extra project-number level.
- Process records, stage files, and patent files stay inside this node's directory.
- The next node may read only this node's `handoff/next-node-input.json`. It must not rely on spoken chat context.

## Stop conditions

- Skill 03's dynamic recommendation is not this node, or the recommended materials lack a prerequisite for writing claims.
- The core technical features are not enough to write claims.
- The total exceeds 10 claims, or the numbering is not continuous.
- A claim cites a later claim, there is a circular citation, a multiple-dependent citation is invalid, or subject names do not match.
- Every dependent claim cites claim 1 directly, but it cannot be shown that they are mutually independent parallel solutions.
- An essential technical feature or a new limitation has no fact source, no description support, and no explicit support requirement for the later description.
- The dependency tree, the claim text, the feature map, and the protection-layer design disagree.
- A required input for this node is missing.
- The user has not made a choice that must be confirmed by a person.
- A publication risk, ownership risk, or materials-authenticity risk cannot be judged.

## Do not

- Do not skip the node delivery directory.
- Do not expand the claims to hit a fixed word count.
- Do not add unsupported or worthless claims in order to fill 10 claims.
- Do not simply cut off or delete later protection points when there are more than 10 candidates.
- Do not first write a flat text in which everything cites claim 1, and then skip the protection-layer analysis.
- Do not package unconfirmed content as a formal conclusion.
- Do not add technical features, appearance features, technical effects, or parameter ranges that are not supported by the user's materials, search records, or a human confirmation.
- Do not let the next node depend on spoken chat context.
