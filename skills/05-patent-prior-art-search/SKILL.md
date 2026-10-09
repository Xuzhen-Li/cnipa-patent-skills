---
name: "05-patent-prior-art-search"
description: "Build a reproducible Chinese/English, classification, and citation search; identify the closest prior art; and write preliminary novelty and inventive-step analyses. Distinguish patentability search from infringement/FTO search. 用于对已确认技术披露制定中英文、分类号和组合检索策略，在可用的中国及国际专利数据库和非专利文献中进行可复核检索，确定最接近现有技术，并分别完成新颖性和创造性初步分析；明确区分可专利性检索与侵权/FTO检索。"
---

# 05-patent-prior-art-search

## Purpose

Using a senior patent attorney's search and analysis method, produce a prior-art investigation that can be repeated and whose evidence can be traced. It gives skill 06 a basis for the general inventive concept (总的发明构思) and the distinguishing features. The conclusion is a professional pre-filing assessment. It is not an examination decision, a validity opinion, or a freedom-to-operate opinion.

## Trigger and inputs

Run after skill 04 finishes, or when skill 03 recommends this node directly. Required inputs:

- The upstream handoff and every recommended source file.
- Confirmed technical facts, the problem–means–effect chain, the candidate inventive concepts, and the search elements.
- The intended filing date or a relevant priority date. If that date is not set, use the search date as a temporary cutoff and state that limit.

When arriving directly from skill 03, both `next_skill` and `recommended_start_skill` must be this node, and the materials must be enough to rebuild the items above. Otherwise return to skill 03 or skill 04.

## Node directory

In the current project, create `patent-deliverables/05-patent-prior-art-search/` and the seven standard subdirectories. Search pages, exports, full texts, search logs, and analysis stay there. Do not edit the user's original materials.

## Search boundary

- Patentability search: patent and non-patent technical disclosures made available to the public before the relevant date, used for a first look at novelty (新颖性) and inventive step (创造性).
- FTO / infringement search: in-force claims and legal status in a specific country. The purpose and method are different. This node does not give an FTO or non-infringement conclusion. It only records in-force risks that may need a separate investigation.
- Not found does not mean absent. Database coverage, language, classification, publication delay, and the search date must all be written into the limitations note.

## Steps

1. Lock the search fact set and the relevant date. Do not mix unconfirmed attorney proposals into the search subject.
2. Split each candidate concept into essential core features, relationship features, functional features, effect features, and optional features, and build search concept groups.
3. Build Chinese terms, English terms, abbreviations, synonyms, broader and narrower concepts, old names, and likely misspellings. Expand with IPC/CPC, applicants, inventors, citations, and similar documents.
4. Search in rounds: whole concept, then core combinations, then key single features, then classification, then applicant/inventor, then the citation network. Prefer accessible patent databases such as CNIPA, WIPO Patentscope, Espacenet, and Google Patents, and add non-patent literature such as papers, standards, product manuals, and archived web pages.
5. For every round, record the database, the full query, filters, date, hit count, why items were kept or dropped, and the export file. Do not record keywords alone.
6. Check each candidate reference for publication date, priority, patent family, relevant text version, and a readable full text. Legal status is only an auxiliary note. It does not decide whether the document is prior art as of the relevant date.
7. Select one or more closest prior-art documents and build a feature-by-feature comparison matrix. Every "disclosed" judgment must point to a specific passage, claim, or drawing.
8. The novelty first look must test every technical feature against a single reference. Do not destroy novelty by stitching several documents together.
9. The inventive-step first look uses the closest prior art, the distinguishing features, the objective technical problem actually solved, the teaching or motivation to combine, and the technical effect. When combining documents, say why a person skilled in the art would or would not make that combination.
10. If the prior art is close, look only in the user's original disclosure for real differences and fallback positions. A new idea from the attorney must be marked separately and sent to the inventor for verification. Do not automatically write it up as "three new innovation points".
11. If the databases cannot be reached, output only a manual search plan and set `can_continue=false`. Hand off to skill 06 only after reviewable document evidence exists.

## Required outputs

- `deliverables/search-strategy.md`
- `deliverables/queries-and-classifications.json`
- `deliverables/search-log.json`
- `deliverables/prior-art-document-list.json`
- `deliverables/patent-family-legal-status.json`
- `deliverables/feature-prior-art-matrix.json`
- `deliverables/closest-prior-art.md`
- `deliverables/novelty-preliminary.md`
- `deliverables/inventive-step-preliminary.md`
- `deliverables/search-limits-fto-boundary.md`
- `deliverables/candidate-differences-from-disclosure.md`
- The three standard process records and `handoff/next-node-input.json`

## Handoff rules

The handoff must state:

- `current_skill=05-patent-prior-art-search`
- `next_skill=06-innovation-point-finder`
- Existing-materials and dynamic-routing fields, copied unchanged
- `relevant_date`, `searched_databases`, `search_log_file`
- `closest_prior_art`, `feature_matrix_file`
- `novelty_preliminary_status`, `inventive_step_preliminary_status`
- `patentability_search_limitations`, `potential_fto_flags`
- `confirmed_difference_candidates`, `unconfirmed_agent_proposals`
- `source_files`, `deliverables`, `open_questions`
- `quality_gate_status`, `can_continue`, `must_stop_reason`

## Quality gate and stops

- Complete the applicable routes among keywords, classification, and citation/party search, and save a full reviewable log.
- The relevant dates, text versions, and specific evidence locations of the key references have been checked.
- The single-document novelty comparison and the combination analysis for inventive step stay strictly separate.
- Do not give `pass` when the search missed a key concept, only an abstract is available, the relevant date is unknown, or the closest prior art cannot be identified.
- Do not promise "not disclosed", "certainly inventive", "non-infringing", or "certain to be granted".
- Do not write a post-search idea, an unverified effect, or a difference with no original basis as an inventive fact.
