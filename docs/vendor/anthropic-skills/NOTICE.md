# Notice: skills imported from anthropics/skills

## Provenance

- Upstream repository: <https://github.com/anthropics/skills>
- Pinned commit: `34040c9c568585f6929bedeaad110ad08f079624`
- Imported file: `skills/doc-coauthoring/SKILL.md` → `.claude/skills/doc-coauthoring/SKILL.md`
- Baseline hashes (sha256): upstream `2e47d78846faeea4a56e9809c52700087a15a2155a3f293a3efbaded81398ef4`, imported `22de9b728f57ccdd33ee747b34f54df1bfaedae82311a37582de05a572a23912`; full detail in [`manifest.json`](manifest.json).
- Date consulted: 2026-09-17.

## Licensing

At the pinned commit the repository has **no root `LICENSE` file**, and `skills/doc-coauthoring/` has **no per-skill `LICENSE.txt`** (both paths returned 404 from raw.githubusercontent.com on the date consulted). The only licensing statement is in the repository `README.md`, quoted exactly (its relative links point into the upstream repository, not this one):

```markdown
Many skills in this repo are open source (Apache 2.0). We've also included the document creation & editing skills that power [Claude's document capabilities](https://www.anthropic.com/news/create-files) under the hood in the [`skills/docx`](./skills/docx), [`skills/pdf`](./skills/pdf), [`skills/pptx`](./skills/pptx), and [`skills/xlsx`](./skills/xlsx) subfolders. These are source-available, not open source, but we wanted to share these with developers as a reference for more complex skills that are actively used in a production AI application.
```

`doc-coauthoring` is not one of the four source-available subfolders named there, so we record it as Apache-2.0 **per the README statement only**. No license text file is claimed to exist; the manifest's `license_file` points at this notice for that reason. Re-check the upstream repository before redistributing this file outside the project.

## Local adaptation

The upstream body is retained verbatim. AIDLC added a `when_to_use` frontmatter key and one integration paragraph after the frontmatter (scope, knowledge-store paths, confirmation-before-write, no invented content, tool-name mapping). Preserve these adaptations when updating from upstream; compare against the recorded `upstream_sha256` first.
