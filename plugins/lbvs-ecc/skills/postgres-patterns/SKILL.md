---
name: postgres-patterns
description: PostgreSQL database patterns for query optimization, schema design, indexing, and security. Based on Supabase best practices. Use when designing PostgreSQL schemas, indexes, or RLS policies, or when a query is too slow.
metadata:
  origin: ECC
---

## AIDLC integration

Use this optional reference with the [AIDLC skill-library guidance](../../../docs/USAGE.md#12-use-the-optional-ecc-skill-library). Existing project conventions and canonical AIDLC artifacts prevail. Skill use is not authority for installs, commits, remote writes, deployment, or global/session changes. Examples are reference material, not automatic execution steps; adapt them to the project’s actual dependencies and versions.

# PostgreSQL Patterns

Quick reference for PostgreSQL best practices. For detailed guidance, consult the optional upstream-only [database-reviewer reference](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/agents/database-reviewer.md); that ECC agent is not installed or assumed available here.

## When to Activate

- Writing SQL queries or migrations
- Designing database schemas
- Troubleshooting slow queries
- Implementing Row Level Security
- Setting up connection pooling

## Quick Reference

### Index Cheat Sheet

| Query Pattern | Index Type | Example |
|--------------|------------|---------|
| `WHERE col = value` | B-tree (default) | `CREATE INDEX idx ON t (col)` |
| `WHERE col > value` | B-tree | `CREATE INDEX idx ON t (col)` |
| `WHERE a = x AND b > y` | Composite | `CREATE INDEX idx ON t (a, b)` |
| `WHERE jsonb @> '{}'` | GIN | `CREATE INDEX idx ON t USING gin (col)` |
| `WHERE tsv @@ query` | GIN | `CREATE INDEX idx ON t USING gin (col)` |
| Time-series ranges | BRIN | `CREATE INDEX idx ON t USING brin (col)` |

### Data Type Quick Reference

| Use Case | Correct Type | Avoid |
|----------|-------------|-------|
| IDs | `bigint` | `int`, random UUID |
| Strings | `text` | `varchar(255)` |
| Timestamps | `timestamptz` | `timestamp` |
| Money | `numeric(10,2)` | `float` |
| Flags | `boolean` | `varchar`, `int` |

### Common Patterns

**Composite Index Order:**
```sql
-- Equality columns first, then range columns
CREATE INDEX idx ON orders (status, created_at);
-- Works for: WHERE status = 'pending' AND created_at > '2024-01-01'
```

**Covering Index:**
```sql
CREATE INDEX idx ON users (email) INCLUDE (name, created_at);
-- Avoids table lookup for SELECT email, name, created_at
```

**Partial Index:**
```sql
CREATE INDEX idx ON users (email) WHERE deleted_at IS NULL;
-- Smaller index, only includes active users
```

**RLS Policy (Optimized):**
```sql
CREATE POLICY policy ON orders
  USING ((SELECT auth.uid()) = user_id);  -- Wrap in SELECT!
```

**UPSERT:**
```sql
INSERT INTO settings (user_id, key, value)
VALUES (123, 'theme', 'dark')
ON CONFLICT (user_id, key)
DO UPDATE SET value = EXCLUDED.value;
```

**Cursor Pagination:**
```sql
SELECT * FROM products WHERE id > $last_id ORDER BY id LIMIT 20;
-- O(1) vs OFFSET which is O(n)
```

**Queue Processing:**
```sql
UPDATE jobs SET status = 'processing'
WHERE id = (
  SELECT id FROM jobs WHERE status = 'pending'
  ORDER BY created_at LIMIT 1
  FOR UPDATE SKIP LOCKED
) RETURNING *;
```

### Anti-Pattern Detection

```sql
-- Find unindexed foreign keys
SELECT conrelid::regclass, a.attname
FROM pg_constraint c
JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
WHERE c.contype = 'f'
  AND NOT EXISTS (
    SELECT 1 FROM pg_index i
    WHERE i.indrelid = c.conrelid AND a.attnum = ANY(i.indkey)
  );

-- Find slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
WHERE mean_exec_time > 100
ORDER BY mean_exec_time DESC;

-- Check table bloat
SELECT relname, n_dead_tup, last_vacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

### Configuration Template

**Execution scope:** This template changes cluster-wide settings, extensions, and schema privileges; it is not a diagnostic read. Require explicit authority for the selected database/environment and each intended change, assess impact and rollback, and use the project’s migration/operations process. Read-only review does not authorize these statements or `pg_reload_conf()`. Discover the actual database client/tool first and stop execution if unavailable; do not install or invent an integration. The `auth.uid()` RLS example is Supabase-specific and requires its authentication schema, not plain PostgreSQL alone.

```sql
-- Connection limits (adjust for RAM)
ALTER SYSTEM SET max_connections = 100;
ALTER SYSTEM SET work_mem = '8MB';

-- Timeouts
ALTER SYSTEM SET idle_in_transaction_session_timeout = '30s';
ALTER SYSTEM SET statement_timeout = '30s';

-- Monitoring
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Security defaults
REVOKE ALL ON SCHEMA public FROM public;

SELECT pg_reload_conf();
```

## Related

- Optional upstream-only [database-reviewer](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/agents/database-reviewer.md) - Full database review reference; no local agent is assumed.
- Optional upstream-only [clickhouse-io](https://github.com/affaan-m/ECC/blob/8321021c54d670126ce3b2969d5deb880b4b0c2a/skills/clickhouse-io/SKILL.md) - ClickHouse analytics patterns.
- [backend-patterns](../backend-patterns/SKILL.md) - API and backend patterns

---

*Based on Supabase Agent Skills (credit: Supabase team) (MIT License)*

The supplementary [Supabase MIT notice](SUPABASE-LICENSE) is retained from
[Supabase revision 8331f910](https://github.com/supabase/agent-skills/blob/8331f910845103c08d51f6ca1d86ebb7d1f745e3/LICENSE).
ECC does not identify the original Supabase revision used for its adaptation.
