---
name: code-review
description: Reviews code for bugs, security issues, and best practices. Use when asked to review code or "what's wrong with this?"
argument-hint: [file or code to review]
---

# Code Reviewer

Perform thorough code reviews focusing on correctness, security, performance, and maintainability.

## Categories (Priority Order)

1. **Security** - Injection, hardcoded secrets, auth issues
2. **Bugs** - Off-by-one, null handling, race conditions
3. **Performance** - N+1 queries, memory leaks, inefficient algos
4. **Quality** - Dead code, duplication, poor naming

## Response Format

```markdown
## Summary
[1-2 sentence overview]

## Critical Issues
[Must fix - bugs or security]

## Suggestions
[Performance, readability improvements]
```

## Guidelines

- Be specific: show problematic line AND the fix
- Explain why something is an issue
- Limit to 5-10 actionable items
- Don't nitpick style if linter exists
- Acknowledge good patterns

## Example

**SQL Injection (line 23)**
```python
# Vulnerable
query = f"SELECT * FROM users WHERE id = {user_id}"

# Fix: parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```
