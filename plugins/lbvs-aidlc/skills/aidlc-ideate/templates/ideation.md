# Ideation: {{topic_id}}

Topic ID: {{topic_id}}
Date: record the actual date
Mode: ordinary AIDLC ideation
Status: candidate directions; no change selected

Use for ordinary `/aidlc-ideate`, not as a replacement for CE's own rendering contract. Replace instructions with actual context. A topic is not a change. This is supporting discovery, not requirements, a canonical plan, or permission to implement. In read-only mode label the whole proposal **not saved**; never claim a saved path without a successful write and subsequent Read.

## Focus and boundaries

Describe the actual repository area, feature, flow, or workflow explored and the engineer's stated constraints. Distinguish explicit direction from inferred scope. Note the exact selected source when continuing prior ideation; preserve existing ideas, rejection reasons, and user notes. Do not silently choose a recent artifact.

## Grounding and coverage

Cite the code/document paths actually read, relevant lessons under the resolved artifact root's `solutions/`, and applicable user-supplied evidence. Separate current observations, user reports, historical lessons, and reasoned assumptions. State unavailable or thin grounding, what was not examined, and that external research was not performed. Do not turn a historical learning into proof of current behavior.

## Ranked ideas

Keep only ideas that survive comparison; zero survivors is valid. Repeat the following fields for each survivor with a stable descriptive title and its current rank. Do not pad to reach a count.

### Rank and idea title

- **Proposal:** Describe the concrete improvement and the problem it might address without declaring final requirements.
- **Basis:** Cite observed code/docs or local evidence. If speculative, label it **reasoned / unverified** and spell out why the inference could apply.
- **Expected value:** Connect the basis to a useful observable outcome; do not fabricate metrics, demand, or savings.
- **Tradeoffs and burden:** State likely cost, risks, constraints, and the strongest downside. Distinguish estimates from facts.
- **Why this rank:** Compare with another candidate or the current approach using evidence strength, relevance, value, burden, and overlap, not unsupported numerical precision.
- **Open questions:** Identify uncertainties that intent capture would need to clarify and what evidence could change the recommendation.

## Rejected or deferred candidates

Record every candidate that did not survive with an explicit comparative reason. Explain overlap, weak evidence, an already-solved problem, disproportionate burden, or a scope mismatch rather than quietly omitting weaker ideas. Preserve previous rejection history when updating; distinguish rejected from deferred when future evidence could matter.

| Candidate | Rejected or deferred | Reason and stronger alternative, when applicable |
| --- | --- | --- |

## Recommendation and unresolved choices

Name the strongest candidate, its main tradeoff, and what might overturn the recommendation. A ranking is the assistant's proposal, not the engineer's decision. Attribute only choices the engineer actually made; record any later selection without treating it as blanket acceptance of all details.

## Next step

Ask the engineer to select an idea by title/rank, refine the set, or stop. After selection, manually invoke `/aidlc-intent <new-change-id>` and provide this exact saved path plus the selected idea in the conversation. Intent re-reads the source, carries provenance, tradeoffs and unknowns, and clarifies the outcome. For an unsaved proposal, supply the exact selected text and label it unsaved. Do not create `changes/<topic-id>/`, launch brainstorming automatically, or advance directly to design, planning, or implementation.
