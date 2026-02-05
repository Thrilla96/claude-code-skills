# Claude Code Skills

Custom skills for [Claude Code](https://claude.ai/code) that enhance development workflows. These skills follow the [Agent Skills](https://agentskills.io) open standard.

## Installation

```bash
git clone https://github.com/Thrilla96/claude-code-skills.git ~/.claude/skills
```

If you already have skills installed:
```bash
git clone https://github.com/Thrilla96/claude-code-skills.git /tmp/skills
cp -r /tmp/skills/*/ ~/.claude/skills/
```

## Skills Included

### Auto-Invoke Skills
These activate automatically when Claude detects relevant context:

| Skill | Description | Trigger Examples |
|-------|-------------|------------------|
| `explain-error` | Explains error messages and suggests fixes | Share an error or stack trace |
| `code-review` | Reviews code for bugs, security issues, and best practices | "Review this code" |
| `regex-helper` | Builds, explains, and tests regular expressions | "Regex for email validation" |
| `sql-optimizer` | Optimizes SQL queries for better performance | "Why is this query slow?" |
| `test-generator` | Generates unit tests for code | "Write tests for this function" |
| `api-docs` | Generates API documentation from code | "Document this endpoint" |
| `shell-explainer` | Explains shell commands and pipelines | "What does this command do?" |
| `env-setup` | Helps set up environment variables and .env files | "Set up env vars for Node.js" |

### Manual-Only Skills
Invoke these directly with `/skill-name`:

| Skill | Command | Description |
|-------|---------|-------------|
| `git-commit` | `/git-commit` | Writes clear conventional commit messages |
| `changelog` | `/changelog` | Generates changelogs from git history |
| `dependency-audit` | `/dependency-audit` | Audits packages for vulnerabilities |

## Usage

Once installed, skills work automatically in Claude Code:

```
# Auto-invoke examples
> TypeError: Cannot read properties of undefined
  (Claude uses explain-error skill)

> Review this function for issues
  (Claude uses code-review skill)

# Manual invoke examples
> /git-commit
> /changelog v1.0.0..v1.1.0
> /dependency-audit
```

## Skill Format

Each skill follows the Claude Code format:

```
skill-name/
└── SKILL.md
```

The `SKILL.md` contains YAML frontmatter and markdown instructions:

```yaml
---
name: skill-name
description: What it does and when to use it (max 200 chars)
argument-hint: [optional arguments]
disable-model-invocation: true  # For manual-only skills
---

# Skill Title

Instructions for Claude...
```

## Customization

Feel free to fork and modify these skills. Key files:
- Edit `description` to change when Claude auto-invokes
- Add `disable-model-invocation: true` to make any skill manual-only
- Add `allowed-tools` to restrict what tools a skill can use

## Resources

- [Claude Code Skills Documentation](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Agent Skills Specification](https://agentskills.io)

## License

MIT
