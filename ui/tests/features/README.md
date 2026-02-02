# Feature Tests

Feature tests validate specific UI functionality in isolation.

## Overview

- **Scope**: Individual features/components
- **Duration**: 5-20 seconds per test
- **Focus**: UI behavior, not business logic
- **Assertions**: Minimal, focused on feature correctness

## Running Feature Tests

```bash
# Run all feature tests
pytest -m feature

# Run specific feature test file
pytest tests/features/test_refresh_functionality.py

# Run feature tests with verbose output
pytest -m feature -v
```

## Current Feature Tests

### Refresh Functionality
**File**: `test_refresh_functionality.py`

Tests the refresh button on incident details page:
- ✅ Refresh reloads incident data
- ✅ Status remains visible after refresh
- ✅ RESOLVED status persists after refresh

## Adding New Feature Tests

1. Create test file: `tests/features/test_<feature_name>.py`
2. Add `@pytest.mark.feature` decorator
3. Use existing Page Objects (no selectors in tests)
4. Focus on UI behavior only
5. Keep tests independent and repeatable

### Example Template

```python
import pytest
from tests.pages.some_page import SomePage

@pytest.mark.feature
def test_feature_name(page):
    """
    FEATURE: Brief description
    
    Test steps:
    1. Setup
    2. Action
    3. Verification
    """
    some_page = SomePage(page)
    
    # Test implementation
    some_page.perform_action()
    some_page.expect_result()
```

## Guidelines

✅ **DO**
- Test one feature per test
- Use descriptive test names
- Add docstrings explaining what you're testing
- Reuse existing Page Objects
- Keep tests independent

❌ **DON'T**
- Test business logic (use integration tests)
- Add deep data validation
- Mix multiple features in one test
- Hardcode selectors in tests
- Depend on test execution order
