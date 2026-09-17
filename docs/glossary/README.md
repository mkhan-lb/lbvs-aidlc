# Glossaries

One glossary per company, in Markdown, read by engineers and by the stages. The idea follows the [AWS AI-DLC glossary](https://github.com/awslabs/aidlc-workflows/blob/main/docs/guide/glossary.md): a short, alphabetical, evidence-labelled vocabulary that every conversation reuses instead of re-deriving. AWS remains the reference for lifecycle words (intent, spec, plan, gate); these files hold organisation and product words.

| Glossary | Covers | Status | Review copy |
| --- | --- | --- | --- |
| [Logicbroker](logicbroker-glossary.md) | Trading partners, business documents, connectors, queues, identifiers | Draft 0.1, 58 terms, pending review | [Confluence](https://go.confluence.logicbroker.com/wiki/spaces/Engineering/pages/2881126401) |
| [Virtualstock](virtualstock-glossary.md) | Retailers, suppliers, product induction (PIM), Stock & Orders fulfilment | Draft 0.1, 51 terms, pending review | [Confluence](https://go.confluence.logicbroker.com/wiki/spaces/Engineering/pages/2880176168/Virtualstock+Glossary+Draft+for+Review) |
| [Logicbroker comparison](logicbroker-glossary-comparison.md) | How the engineering draft and the product team's glossary differ, what to merge, definitions to reconcile, wording to correct | Guide for the review, 11 September 2026 | — |

## Which one applies

The repository profile's Identity section (`docs/repo-profile.md`, written by `/aidlc-onboard` or `/aidlc-init`) names the company and the glossary file. Without a profile: Virtualstock repositories are `the-edge`, `the-edge-product-induct` and their siblings; Logicbroker repositories are `api`, `connectors`, `core`, `data-layer`, `queuing` and the services around them. A repository that spans both names both files. When the two glossaries define the same word differently (Order, Order line, SKU, Supplier, Workflow), say which company's meaning you are using.

## Source of truth

1. **This repository's Markdown** is what engineers and agents read. It is the most current text.
2. **The Confluence review copy** linked from each file is where domain owners comment and mark entries `Approved / Revise / Remove`.
3. Approved wording is copied back here in a reviewed pull request that records the Confluence page version and the approval date. No stage edits a glossary silently.

## How the stages use them

- `aidlc-intent` and `aidlc-design` use glossary terms verbatim in `intent.md` and `spec.md` (EARS lines name the system and its documents the way the glossary does). A word the glossary lacks is flagged as a **new term** in the artifact's open questions and offered as a draft entry from [`template.md`](template.md), written only on confirmation; it is never coined silently.
- `aidlc-review` and the pre-PR `aidlc-conventions-checker` report terminology that drifts from the glossary as a **nit**, never a blocker.
- `aidlc-repo-scout` and `aidlc-spike` cite the glossary instead of redefining domain words in their reports.
- Entries marked **Interpretation** carry a review question; a design that depends on one names it as an open question rather than resolving it in the spec.

## Entry format

Each entry has: term and aliases or code names; topic; evidence label (`Source-backed` or `Interpretation`); a one- or two-sentence definition; usage guidance; a review question where the meaning is undecided; sources pinned to a commit; and a review line (`Pending`, or `Approved / Revise / Remove` with reviewer and date). [`template.md`](template.md) is the blank entry. Keep business meaning first and code names second; one canonical definition per concept, cross-linked rather than duplicated.

## Related vocabularies

- [product-aidlc `Conventions/Glossary.md`](https://github.com/Logicbroker/product-aidlc/blob/main/Conventions/Glossary.md) — the product team's business and process vocabulary (internal repository); the comparison above says what to merge from it.
- [databricks `context/glossary.md`](https://github.com/Logicbroker/databricks/blob/main/context/glossary.md) — code-verified definitions of COGS, GMV, order volume and inventory as the gold-layer jobs compute them (internal repository).
