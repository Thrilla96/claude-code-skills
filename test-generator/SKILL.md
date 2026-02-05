---
name: test-generator
description: Generates unit tests for code. Use when asked to write tests, create test cases, or "test this function".
argument-hint: [function or file to test]
---

# Test Generator

Generate comprehensive unit tests with good edge case coverage.

## Test Structure (AAA Pattern)

1. **Arrange** - Set up test data
2. **Act** - Execute code under test
3. **Assert** - Verify results

## What to Test

1. **Happy path** - Normal inputs
2. **Edge cases** - Boundaries, empty, limits
3. **Error cases** - Invalid inputs, expected failures

## Naming Convention

```
test_<function>_<scenario>_<expected>
```

Examples:
- `test_divide_by_zero_raises_error`
- `test_parse_empty_string_returns_none`

## Example Output

Given:
```python
def calculate_discount(price: float, percent: float) -> float:
    if price < 0:
        raise ValueError("Price cannot be negative")
    return price * (1 - percent / 100)
```

Tests:
```python
import pytest

class TestCalculateDiscount:
    def test_standard_discount(self):
        assert calculate_discount(100.0, 20.0) == 80.0

    def test_zero_discount(self):
        assert calculate_discount(50.0, 0.0) == 50.0

    def test_negative_price_raises(self):
        with pytest.raises(ValueError):
            calculate_discount(-10.0, 20.0)
```

## Guidelines

- Generate 5-10 tests per function
- Mock external dependencies
- Test behavior, not implementation
- Use parameterized tests for similar cases
