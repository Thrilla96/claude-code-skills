---
name: explain-error
description: Explains error messages and suggests fixes. Use when users share errors, stack traces, or ask "what does this error mean?"
---

# Error Explainer

When a user shares an error message, stack trace, or asks about an error, follow this structured approach.

## Response Format

### 1. Quick Summary
One-sentence plain English explanation of what went wrong.

### 2. Root Cause
Why this error occurs - the underlying issue, not just the symptom.

### 3. Fix
The most likely fix with a concrete code example or command.

### 4. Prevention (optional)
If relevant, briefly mention how to avoid this error in the future.

## Guidelines

- Be concise - developers want quick answers
- Prioritize the most common cause first
- Show actual code/commands, not just descriptions
- If the error could have multiple causes, list top 2-3 ranked by likelihood
- For stack traces, identify the relevant line (usually first one in user code)
