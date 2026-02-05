---
name: env-setup
description: Helps set up environment variables and .env files. Use when asked about env vars, configuration, or "create .env file".
argument-hint: [framework or service]
---

# Environment Setup Helper

Guide setup of environment variables and config files.

## Standard Files

```bash
.env           # Local secrets (NEVER commit)
.env.example   # Template (safe to commit)
```

## Response Format

1. List required variables with descriptions
2. Show .env.example template
3. Explain framework-specific loading
4. Security reminders

## Framework Loading

**Node.js:**
```javascript
require('dotenv').config();
const key = process.env.API_KEY;
```

**Python:**
```python
from dotenv import load_dotenv
load_dotenv()
key = os.getenv("API_KEY")
```

**Next.js:**
```bash
# NEXT_PUBLIC_ prefix for client-side
NEXT_PUBLIC_API_URL=https://api.example.com
SECRET_KEY=server_only
```

## Naming Convention

```bash
# SCREAMING_SNAKE_CASE
DATABASE_URL=...
STRIPE_API_KEY=...

# Prefix by service
AWS_ACCESS_KEY_ID=...
AWS_REGION=...
```

## Security Checklist

**Do:**
- Add `.env` to `.gitignore`
- Use `.env.example` as template
- Different values per environment
- Use secret managers in production

**Don't:**
- Commit `.env` with real secrets
- Log environment variables
- Expose secrets to client-side
- Share secrets via Slack/email

## Validation

```javascript
const required = ['DATABASE_URL', 'API_KEY'];
required.forEach(key => {
  if (!process.env[key]) {
    throw new Error(`Missing: ${key}`);
  }
});
```
