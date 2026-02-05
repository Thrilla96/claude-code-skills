---
name: changelog
description: Generates changelogs from git history. Use when asked to create release notes or "what changed since last release?"
disable-model-invocation: true
argument-hint: [version or tag range]
---

# Changelog Generator

Generate organized changelogs from git history.

## Format (Keep a Changelog)

```markdown
## [Version] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes in existing functionality

### Fixed
- Bug fixes

### Security
- Security patches
```

## Commit Type Mapping

| Commit | Section |
|--------|---------|
| `feat` | Added |
| `fix` | Fixed |
| `perf` | Changed |
| `BREAKING` | Changed (highlight) |
| `security` | Security |

## Process

1. Gather commits since last release
2. Group by type
3. Write user-friendly descriptions (not raw commits)
4. Highlight breaking changes
5. Order by importance

## Example

Given commits:
```
feat(auth): add OAuth2 support
fix(api): handle null response
BREAKING: remove /v1/users endpoint
```

Output:
```markdown
## [2.1.0] - 2024-01-15

### Added
- OAuth2 login support for Google and GitHub

### Changed
- **BREAKING:** Removed `/v1/users` endpoint. Use `/v2/users`

### Fixed
- Payment API handles null responses gracefully
```

## Guidelines

- Write for users, not developers
- Be specific about what changed
- Group related changes
- Omit internal changes (refactors, tests)
- Link issues/PRs: `Fixed crash (#123)`
