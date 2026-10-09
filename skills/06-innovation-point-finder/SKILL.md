---
name: "06-innovation-point-finder"
description: "Confirm one general inventive concept and the related core, secondary, and fallback innovation points, with problem-means-effect evidence, feature levels, and unity. No fixed word count and no forced single isolated point. 用于结合最接近现有技术和原始技术披露，确认一个总的发明构思及相互关联的核心、次级和备用创新点，建立问题—手段—效果证据链、必要与可选特征层级、参数依据和单一性分析；不设固定字数，不强迫只选一个孤立创新点。"
---

# 06-innovation-point-finder

## Purpose

From a senior patent attorney's point of view, turn the search results into an inventive concept that has an original basis, can support a claim hierarchy, and has reasonable fallback positions. The inventor confirms the technical facts. The attorney proposes the protection structure and the risk opinion.

## Trigger and inputs

Run after skill 05 finishes, or when skill 03 recommends this node directly because the existing materials include reviewable search evidence. Required inputs:

- The upstream handoff and recommended source files.
- The closest prior art, the feature-comparison matrix, and the preliminary novelty and inventive-step analyses.
- The original technical disclosure, the confirmed facts, and the problem–means–effect chain.

When arriving directly from skill 03, check that real search records, full texts of the references, and candidate differences exist. If they do not, return to skill 05.

## Node directory

In the current project, create `patent-deliverables/06-innovation-point-finder/` and the seven standard subdirectories. User originals and search evidence are read-only.

## Analysis rules

- Do not require a single isolated innovation point. First confirm one general inventive concept (总的发明构思), then organize the core, secondary, preferred, and fallback points that are technically related to it.
- A distinguishing feature is not automatically an inventive feature. Analyze the objective technical problem it solves, the technical effect it produces, and whether the prior art gives a teaching.
- Grade technical effects as `实测证据` (measured evidence), `用户确认经验` (experience the user confirmed), `可由机理直接推导` (follows directly from the mechanism), or `尚待验证` (not yet verified). An unverified effect must not be stated as a certainty.
- Parameter ranges, material choices, structural positions, step order, and control conditions must have an original basis. Do not invent them in order to widen the scope.
- Protection points in the same application must pass a unity (单一性) check. Do not force together themes that lack a common or corresponding special technical feature.

## Steps

1. Re-check the closest prior art and the feature-by-feature comparison. Drop candidate differences that have no basis in the original disclosure.
2. State the general inventive concept and its core technical contribution and common special technical features.
3. Build layers for the core innovation point, secondary innovation points, preferred limitations, and fallback positions. Do not fix the count, and do not add content just to fill a number.
4. For each layer, build a problem–means–effect evidence chain and tie it to the reference and the place in the original disclosure.
5. Separate features that an independent claim may need, optional limitations that suit dependent claims, and details that belong only in an embodiment.
6. Check alternative structures, equivalents, parameter boundaries, working states, and likely design-around paths. Record what is already disclosed and what the inventor still needs to supply.
7. For each candidate protection point, analyze inventive contribution, commercial value, how detectable infringement would be, how hard it is to prove, and fallback value.
8. Show the inventor the full inventive concept and the innovation layers. Confirm technical facts, effects, parameters, and alternatives item by item. An attorney proposal must be confirmed separately and added to the technical disclosure before it can be used.
9. Reach the final conclusion by complete scope, sufficient evidence, and whether later claims can actually be drafted. Do not set a fixed word count.
10. After the user confirms, hand off to skill 07 and stop. Do not run skill 07 in the same turn.

## Required outputs

- `deliverables/general-inventive-concept.md`
- `deliverables/innovation-hierarchy.json`
- `deliverables/problem-means-effect-evidence.json`
- `deliverables/essential-optional-features.json`
- `deliverables/parameter-effect-evidence.json`
- `deliverables/alternatives-design-around.md`
- `deliverables/unity-preliminary.md`
- `deliverables/missing-experiments-materials.md`
- The three standard process records and `handoff/next-node-input.json`

## Handoff rules

The handoff must state:

- `current_skill=06-innovation-point-finder`
- `next_skill=07-abstract-generator`
- Existing-materials and dynamic-routing fields, copied unchanged
- `general_inventive_concept`, `innovation_hierarchy_file`
- `essential_features`, `optional_features`, `backup_features`
- `effect_evidence_file`, `parameter_basis_file`, `unity_status`
- `inventor_confirmation_status`, `unverified_effects`, `missing_technical_materials`
- `source_files`, `deliverables`, `open_questions`
- `quality_gate_status`, `can_continue`, `must_stop_reason`

## Quality gate and stops

- The general inventive concept, the innovation layers, and the common special technical features are clear.
- Every formal innovation point has an original disclosure, a difference from the prior art, and a basis for its technical effect.
- The split among essential features, optional features, and embodiment details is reasonable, and the evidence status of parameters and effects is explicit.
- Set `can_continue=false` when the inventor has not confirmed a key technical fact, an unverified effect is treated as certain, or a unity problem is unresolved.
- Do not expand the text to hit a fixed word count. Do not force the case down to one innovation point. Do not treat a distinguishing feature as inventive step by itself.
