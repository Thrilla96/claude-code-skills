---
name: dependency-audit
description: Audits dependencies for vulnerabilities and outdated packages. Use when asked to check deps or "are my packages secure?"
disable-model-invocation: true
argument-hint: [package manager or file]
---

# Dependency Audit

Audit project dependencies for security and updates.

## Commands by Package Manager

**npm:**
```bash
npm audit              # Security check
npm outdated           # Check versions
npm audit fix          # Auto-fix safe issues
```

**pip:**
```bash
pip-audit              # Security check
pip list --outdated    # Check versions
```

**cargo:**
```bash
cargo audit            # Security check
cargo outdated         # Check versions
```

**go:**
```bash
govulncheck ./...      # Security check
go list -u -m all      # Check versions
```

## Response Format

```markdown
## Summary
**Package Manager:** npm
**Total Dependencies:** 234

## Critical Vulnerabilities
| Package | Issue | Fix |
|---------|-------|-----|
| lodash | Prototype Pollution | Upgrade to 4.17.21 |

## Outdated Packages
| Package | Current | Latest | Type |
|---------|---------|--------|------|
| react | 17.0.2 | 18.2.0 | Major |

## Recommendations
1. Fix critical vulns immediately
2. Update security patches soon
3. Plan major updates

## Commands
```bash
npm install lodash@4.17.21
npm audit fix
```
```

## Issues to Flag

**Security:**
- Known CVEs
- Abandoned packages (no updates 2+ years)
- Very low download count

**Maintenance:**
- Deprecated packages
- Better alternatives exist

## Guidelines

- Prioritize security over outdated
- Provide specific fix commands
- Warn about breaking changes
- Suggest changelog review for majors
