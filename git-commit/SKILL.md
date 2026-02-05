---
name: git-commit
description: Writes clear conventional commit messages. Use when asked to commit, write a commit message, or "what should I call this commit?"
disable-model-invocation: true
argument-hint: [optional message context]
---

# Git Commit Message Writer

Generate clear, conventional commit messages.

## Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Types

| Type | Use |
|------|-----|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Neither fix nor feature |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `chore` | Maintenance, deps, configs |

## Rules

1. **Subject**: Max 50 chars, imperative mood ("Add" not "Added"), no period
2. **Body**: Wrap at 72 chars, explain what and why
3. **Scope**: Optional, area affected (e.g., `auth`, `api`)

## Process

1. Look at staged/described changes
2. Identify primary change type
3. Determine scope if focused
4. Write subject in imperative mood
5. Add body only if "why" isn't obvious

## Example

```
feat(api): add rate limiting to public endpoints

Implement token bucket algorithm with 100 req/min per IP.
Prevents abuse and ensures fair usage across consumers.

Fixes #123
```
