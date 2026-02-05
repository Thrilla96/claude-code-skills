---
name: shell-explainer
description: Explains shell commands and pipelines. Use when asked "what does this command do?" or to explain flags/options.
argument-hint: [command to explain]
---

# Shell Command Explainer

Break down shell commands into understandable parts.

## Response Format

1. **Summary** - One sentence: what it does
2. **Breakdown** - Each component explained
3. **Data flow** - For pipes: what each step outputs
4. **Notes** - Warnings or alternatives

## Example: Simple

**Command:** `grep -rn "TODO" --include="*.py" .`

**Summary:** Search for "TODO" in Python files recursively with line numbers.

| Part | Meaning |
|------|---------|
| `grep` | Search for patterns |
| `-r` | Recursive |
| `-n` | Show line numbers |
| `--include="*.py"` | Only .py files |
| `.` | Current directory |

## Example: Pipeline

**Command:** `ps aux | grep python | awk '{print $2}' | xargs kill`

**Summary:** Kill all Python processes.

| Part | Meaning |
|------|---------|
| `ps aux` | List all processes |
| `grep python` | Filter to python |
| `awk '{print $2}'` | Extract PID column |
| `xargs kill` | Kill each PID |

**Data Flow:**
```
ps aux → grep python → awk → xargs kill
(all)    (filtered)   (PIDs)  (killed)
```

**Note:** Use `pkill python` as safer alternative.

## Common Symbols

| Symbol | Meaning |
|--------|---------|
| `>` | Redirect to file |
| `>>` | Append to file |
| `2>&1` | Stderr to stdout |
| `&&` | Run if success |
| `||` | Run if fail |
| `&` | Background |
