---
name: regex-helper
description: Builds, explains, and tests regular expressions. Use for "regex for...", "explain this regex", or pattern matching help.
argument-hint: [pattern to match or regex to explain]
---

# Regex Helper

Build, explain, and test regular expressions with clear explanations.

## When Building

1. Show the regex
2. Explain each part
3. Provide test cases (matches AND non-matches)
4. Note edge cases

## When Explaining

1. Break into components
2. Plain English for each part
3. Show what matches/doesn't

## Quick Reference

| Pattern | Matches |
|---------|---------|
| `\d` | Digit |
| `\w` | Word char |
| `\s` | Whitespace |
| `.` | Any char |
| `^` / `$` | Start/end |
| `[abc]` | a, b, or c |
| `a*` | Zero+ |
| `a+` | One+ |
| `a?` | Zero or one |
| `(abc)` | Group |
| `a|b` | a or b |

## Example

**Request:** "Regex for email"

```regex
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```

| Part | Meaning |
|------|---------|
| `^` | Start |
| `[a-zA-Z0-9._%+-]+` | Local part |
| `@` | Literal @ |
| `[a-zA-Z0-9.-]+` | Domain |
| `\.[a-zA-Z]{2,}$` | TLD (2+ letters) |

**Matches:** `user@example.com`
**Doesn't match:** `@nodomain.com`, `missing@tld`
