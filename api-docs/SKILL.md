---
name: api-docs
description: Generates API documentation from code. Use when asked to document an API or "create docs for this endpoint".
argument-hint: [endpoint or file to document]
---

# API Documentation Generator

Generate clear API documentation from code.

## Document Each Endpoint

1. **Endpoint** - Method and path
2. **Description** - What it does
3. **Auth** - Required authentication
4. **Parameters** - Path, query, body
5. **Response** - Success and errors
6. **Example** - curl or code

## Output Format

```markdown
## Endpoint Name

Brief description.

### Request

`POST /users/:id/orders`

**Auth:** Bearer token

**Path Parameters:**
| Name | Type | Description |
|------|------|-------------|
| id | string | User ID |

**Body:**
```json
{"product_id": "abc", "quantity": 2}
```

### Response

**201 Created:**
```json
{"order": {"id": "...", "status": "pending"}}
```

**Errors:**
| Status | Description |
|--------|-------------|
| 400 | Invalid body |
| 401 | Unauthorized |

### Example
```bash
curl -X POST https://api.example.com/users/123/orders \
  -H "Authorization: Bearer token" \
  -d '{"product_id": "abc", "quantity": 2}'
```
```

## Guidelines

- Infer error responses even if not in code
- Use realistic example values
- Note rate limits if apparent
- Document pagination patterns
