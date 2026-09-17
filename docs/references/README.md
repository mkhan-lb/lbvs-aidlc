# Library references

Where the stages record which current documentation they relied on. Every design, plan, build or fix that touches a library, framework, SDK or cloud API looks the docs up first — Context7 MCP (`resolve-library-id`, then `query-docs`) or the `documentation-lookup` skill — instead of trusting training data, and cites the result in the artifact. When a lookup settles something worth reusing, add or update a row in [`libraries.md`](libraries.md) inside the same change so the next engineer starts from the same page.

Rules: one row per library, the Context7 ID exactly as resolved (`/org/project` or `/org/project/version`), the version the repository actually uses, the pages that answered real questions, and dated gotchas with the change ID that hit them. Delete rows for libraries the repository no longer uses. This is reference material, not policy: a rule that must hold goes in `AGENTS.md` or `.claude/rules/`.
