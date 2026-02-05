---
name: sql-optimizer
description: Optimizes SQL queries for better performance. Use when asked to make queries faster or "why is this query slow?"
argument-hint: [SQL query to optimize]
---

# SQL Query Optimizer

Analyze SQL queries and provide optimization recommendations.

## Common Anti-Patterns

### SELECT *
```sql
-- Bad
SELECT * FROM users WHERE status = 'active';
-- Better
SELECT id, name, email FROM users WHERE status = 'active';
```

### Functions on Indexed Columns
```sql
-- Bad (index won't be used)
WHERE YEAR(created_at) = 2024
-- Better
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'
```

### N+1 Queries
```sql
-- Bad: loop per user
SELECT * FROM orders WHERE user_id = ?;
-- Better: single query
SELECT * FROM orders WHERE user_id IN (1, 2, 3);
```

### Leading Wildcards
```sql
-- Bad: full scan
WHERE name LIKE '%phone%'
-- Better (or use full-text search)
WHERE name LIKE 'phone%'
```

## Response Format

```markdown
## Analysis
[What the query does, current issues]

## Optimizations
### 1. Issue Name
**Current:** [code]
**Optimized:** [code]
**Impact:** High/Medium/Low

## Recommended Indexes
[CREATE INDEX statements]
```

## Guidelines

- Explain WHY each optimization helps
- Note trade-offs (indexes slow writes)
- Suggest EXPLAIN/ANALYZE for verification
- Consider database-specific syntax
