# Notice: agent definitions adapted from awslabs/aidlc-workflows

## Provenance

- Upstream repository: <https://github.com/awslabs/aidlc-workflows>
- Pinned commit: `be94bde7cae6f9e4d431d045e148c8d5d8eaa508` (`main` on the date consulted, committed 2026-09-17T04:10:59Z).
- Consulted files (sha256 at the pinned commit):
  - `core/agents/aidlc-architecture-reviewer-agent.md` — `69efa6bdaddc9c439860e584efd7f48429d8c88157bdadb25193eb6a16aeddcd` → adapted into `.claude/agents/lbvs-aidlc-design-reviewer.md`
  - `core/agents/aidlc-devsecops-agent.md` — `8abba85622c5556350935d138bfec616edbfb86e8ac3e3095a965d4e80b8962b` → adapted into `.claude/agents/lbvs-aidlc-threat-modeler.md`
  - `LICENSE` — `7cb750713252efd1d578837ba8785b61319109906f0c10b87adab7cf4badfc42`
- Date consulted: 2026-09-17.

## Licensing

The upstream repository is licensed **MIT No Attribution (MIT-0)**, "Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved." MIT-0 permits use, copying, modification and redistribution without requiring the copyright or permission notice to be retained. This notice is kept voluntarily so the provenance of the adapted agents stays traceable; nothing in it is a licence obligation.

The `.claude/agents/lbvs-aidlc-threat-modeler.md` "Do not flag" list is additionally adapted from `agents/security-reviewer.md` in affaan-m/ECC at commit `8321021c54d670126ce3b2969d5deb880b4b0c2a` (MIT). That repository's copyright and permission notice is already retained at [`../ecc/LICENSE`](../ecc/LICENSE) and its pin is recorded in [`../ecc/manifest.json`](../ecc/manifest.json); no separate copy is needed here.

## What was adapted

No upstream text is reproduced verbatim; both local agents are rewritten in our own words for the lbvs-aidlc artifact set (`changes/<id>/intent.md`, `spec.md`, `plan.md`, `docs/adr/`, `docs/platform/platform.md`, `docs/security/`).

`lbvs-aidlc-design-reviewer` keeps from the AWS architecture reviewer: the fresh-eyes adversarial posture (try to refute, READY is what survives), the evidence-grounding rule (taste is a suggestion, not grounds for NOT READY), the "could a developer build this without asking" readiness test, the advisory-pass framing (verdict informs the human gate and never approves), the bounded pass list, the identity marker as the first output line, and the write-the-verdict-before-the-turn-cap rule. Dropped: the `aidlc-orchestrate.ts`/`aidlc-state.ts` preamble, `tier`/`maxTurns`/`disallowedTools` frontmatter, validation-tool runs, and the sibling-unit access rules; added: EARS/R-ID coverage checks, ADR consistency, platform-orb fit, NFR and threat-model passes.

`lbvs-aidlc-threat-modeler` keeps from the AWS DevSecOps agent: STRIDE per component and data flow, attack-surface and trust-boundary enumeration, likelihood/impact scoring, sensitive-data-flow and third-party review, and the principles defence in depth, least privilege, assume breach, secure by default and validate all input. Dropped: SAST/DAST/IaC pipeline sections, AWS-service-specific validation (IAM, KMS, GuardDuty, Security Hub), compliance-framework mapping, collaboration/memory sections and the inherit-all-tools stance (the local agent is Read/Glob/Grep only and proposes, never writes). From ECC: the false-positive list (fixtures and example env files, marked test credentials, intentionally public keys, checksum hashes) generalised and extended with documented accepted risks and verified framework-provided protections.

`.omp/agents/lbvs-aidlc-design-reviewer.md` and `.omp/agents/lbvs-aidlc-threat-modeler.md` contain no upstream content; they defer to the Claude definitions.

`.claude/agents/lbvs-aidlc-conventions-checker.md` adapts ideas only from `core/agents/aidlc-quality-agent.md` (`a1119a0b93e46dce0b93f10c39181ec798c0e38fbe3cfc26829eac88f86acec6`: quality gates as documented pass/fail criteria, test the requirement not the implementation) and `core/agents/aidlc-developer-agent.md` (`e8e62fef63ad052e8564796c291fc3674eaa405ef91b8efbb8ec0251f7dd2e14`: convention over configuration, consistency with the codebase over preference), both unchanged at the pinned commit; its evidence-gated, zero-findings-is-valid posture comes from affaan-m/ECC `agents/code-reviewer.md` at the pin recorded in [`../ecc/manifest.json`](../ecc/manifest.json) (MIT, [`../ecc/LICENSE`](../ecc/LICENSE)). No upstream text is reproduced; `.omp/agents/lbvs-aidlc-conventions-checker.md` defers to the Claude definition.
