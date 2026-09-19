# Repository profile: <repository>

Last verified: <YYYY-MM-DD> at <full commit sha>
Manifests: <space-separated repo-relative paths, e.g. pyproject.toml package.json .pre-commit-config.yaml .circleci/config.yml>
Profiled by: lbvs-aidlc-repo-scout via /lbvs-aidlc-onboard | /lbvs-aidlc-init

<!-- The four header lines above are parsed by `python3 scripts/aidlc.py profile`: keep their labels and order exactly. `Manifests` lists the real files whose change makes this profile stale; `Last verified` is bumped only after a scout pass confirms the sections. Every fact below cites a repository-root-relative path or says `Unknown: <what was looked for>`. Never copy credentials, tokens or production URLs here. -->

## Identity

- Company: <Logicbroker | Virtualstock> (the `glossary-context.sh` hook reads this word to pick the glossary index it injects at session start)
- Glossary: docs/glossary/<logicbroker-glossary.md | virtualstock-glossary.md>
- Platform: docs/platform/platform.md (<filled | bracketed items remain | absent>)
- Service / catalog name: <name from catalog-info.yaml or manifest, with path>

## Stack

<Languages and versions, frameworks, databases/ORMs, build tooling, CI platform — each with the manifest or config path it was read from.>

## Layout

| Directory | Purpose |
|-----------|---------|
| `<dir>/` | <purpose; mark entry points, frozen or generated areas> |

## Commands

| Task | Command (verbatim) | Source |
|------|--------------------|--------|
| build | `<command>` | `<path>` |
| test | `<command>` | `<path>` |
| lint | `<command>` | `<path>` |
| format | `<command>` | `<path>` |
| run | `<command>` | `<path>` |

## Conventions

- Formatter: <tool and config path, or Unknown>
- Linter: <tool and config path, or Unknown>
- Pre-commit: <.pre-commit-config.yaml hooks, or none>
- Commit title format: <e.g. `VS-1234: <imperative title>` or Conventional Commits; cite git log or CONTRIBUTING.md>
- Branch naming: <pattern, cite evidence>
- PR template: <.github/pull_request_template.md or none>

## Testing

- Framework: <name and version, config path>
- Layout: <where tests live, file naming>
- Fixtures: <shared fixtures/mocks and their paths>
- Run one test: `<command>` (source: `<path>`)

## Generated paths

<Paths that are never hand-edited, each with the generator command and its source path, e.g. `src/client/` — `<command>` (`<path>`). Write `None found` if none.>

## Hotspots and risks

<Frozen or legacy packages, fragile modules, security-relevant paths, convention conflicts, TODO/FIXME clusters, missing tests — each with a path.>

## Ownership

<CODEOWNERS entries or team mapping with the file path; `Unknown: no CODEOWNERS` otherwise.>

## Existing agent instructions

<Each of CLAUDE.md, AGENTS.md, .claude/rules/**, .cursorrules, .github/copilot-instructions.md found: path, scope, anything it forbids or mandates. `None found` otherwise. These files remain authoritative over this profile.>

## Knowledge stores

| Store | Path | Template | Index | Naming |
|-------|------|----------|-------|--------|
| ADR | docs/adr/ | docs/adr/template.md | docs/adr/README.md | NNNN-kebab-title.md |
| Incidents | docs/incidents/ | docs/incidents/template.md | docs/incidents/README.md | YYYY-MM-DD-slug.md |
| Security | docs/security/ | docs/security/threat-model-template.md | docs/security/README.md | threat-models/<name>.md, findings/YYYY-MM-DD-<source>.md |
| References | docs/references/ | none | docs/references/libraries.md (one row per library) | — |
| Playbooks | docs/playbooks/ | docs/playbooks/template.md | docs/playbooks/README.md | kebab-title.md |
| Lessons | docs/solutions/ | .claude/skills/lbvs-aidlc-learn/templates/learning.md | none | <category>/<topic>.md |

<!-- Rows above are the package defaults. Where the repository keeps a store elsewhere or in another form, edit its row to the real path, template, index and naming (e.g. `| ADR | docs/adr/ | docs/adr/0000-template.md | none — directory listing | NNNN-kebab-title.md |`, `| Lessons | .claude/knowledge/ | none — prose sections per domain | none | <domain>.md |`). `Index: none` = append no row; `Template: none — <form>` = follow that form. Skills read their store's row from this table; a missing row means the package default. -->

## Playbooks

<Links to docs/playbooks/<name>.md entries that apply to this repository, or `None yet`.>

## Open questions

- <Fact the scout could not establish and who can answer it.>
