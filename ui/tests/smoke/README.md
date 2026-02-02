# Smoke Tests

## Overview

Smoke tests validate **critical user paths only** with **minimal assertions**. They are designed to be fast and catch catastrophic failures before running the full E2E suite.

## What Smoke Tests DO

✅ Verify application loads  
✅ Test happy path user flows  
✅ Validate basic navigation works  
✅ Check critical UI elements render  
✅ Run in < 10 seconds total  

## What Smoke Tests DON'T DO

❌ Test AI analysis results  
❌ Validate complex business logic  
❌ Check error scenarios  
❌ Wait for long-running operations  
❌ Perform deep data validation  

## Running Smoke Tests

### Smoke tests only (recommended for CI fast feedback)
```bash
pytest -m smoke
```

### Smoke + E2E tests
```bash
pytest -m "smoke or e2e"
```

### Run all tests
```bash
pytest
```

### Smoke with verbose output
```bash
pytest -m smoke -v
```

### Smoke in headed mode (debug)
```bash
pytest -m smoke --headed
```

## Test Coverage

| Test File | What It Tests | Duration |
|-----------|---------------|----------|
| `test_smoke_critical_path.py` | Create incident → Navigate to incident page | ~5s |

## CI/CD Integration

### Recommended Pipeline
```yaml
stages:
  - smoke      # Run first (fast fail)
  - e2e        # Run if smoke passes
  - full       # Complete test suite

smoke:
  script: pytest -m smoke --browser chromium
  
e2e:
  script: pytest -m e2e --browser chromium
  needs: [smoke]
```

## Adding New Smoke Tests

1. Create test file in `tests/smoke/`
2. Add `@pytest.mark.smoke` decorator
3. Keep test < 10 seconds
4. Use happy path only
5. Minimal assertions (just verify it works)

```python
@pytest.mark.smoke
def test_new_critical_path(page):
    # Test only critical happy path
    # No deep validation
    pass
```

## When to Run

- **Every commit** - Smoke tests  
- **Before merge** - Smoke + E2E  
- **Nightly** - Full suite  
- **Pre-release** - Full suite + manual testing  
