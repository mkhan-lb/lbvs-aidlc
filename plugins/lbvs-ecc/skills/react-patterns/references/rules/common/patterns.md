> AIDLC reference only: this bundled ECC rule is not installed as a project rule. Existing project conventions and canonical AIDLC artifacts prevail; use within the selected task, without automatic installs, CI changes, hooks, or session changes.

# Common Patterns

## Skeleton Projects

For an explicitly requested new-project scaffold (not changes to an existing app):
1. Search for battle-tested skeleton projects
2. If authorized agent tools are available, use them to evaluate options; otherwise evaluate inline:
   - Security assessment
   - Extensibility analysis
   - Relevance scoring
   - Implementation planning
3. Propose the best match; clone only with explicit authorization for the destination and remote access
4. Iterate within proven structure

## Design Patterns

### Repository Pattern

Encapsulate data access behind a consistent interface:
- Define standard operations: findAll, findById, create, update, delete
- Concrete implementations handle storage details (database, API, file, etc.)
- Business logic depends on the abstract interface, not the storage mechanism
- Enables easy swapping of data sources and simplifies testing with mocks

### API Response Format

Use a consistent envelope for all API responses:
- Include a success/status indicator
- Include the data payload (nullable on error)
- Include an error message field (nullable on success)
- Include metadata for paginated responses (total, page, limit)
