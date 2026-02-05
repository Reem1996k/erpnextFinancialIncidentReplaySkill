# Backend Test Plan

**Date:** February 4, 2026 | **Status:** Active

---

## 1. What to Test

### 1.1 API Tests (16 Total)

**Incidents API** (`tests/api/test_incidents_api.py`) - 6 tests:

| Test | Endpoint | Expected |
|------|----------|----------|
| `test_create_incident_success` | POST `/incidents/` | 201, status=OPEN |
| `test_create_duplicate_incident_returns_409` | POST `/incidents/` | 409 Conflict |
| `test_get_incidents_returns_empty_list_when_no_data` | GET `/incidents/` | Empty list |
| `test_get_incidents_returns_created_incidents` | GET `/incidents/` | List with incident |
| `test_get_incident_by_id_success` | GET `/incidents/{id}` | Incident data |
| `test_get_incident_by_id_not_found` | GET `/incidents/{id}` | 404 |

**Analysis API** (`tests/api/test_analysis_api.py`) - 7 tests:

| Test | Expected |
|------|----------|
| `test_analyze_incident_success` | status=RESOLVED |
| `test_analyze_incident_not_found` | 404 |
| `test_analyze_incident_internal_error` | status=UNDER_REVIEW |
| `test_analyze_incident_with_partial_erp_data` | status=RESOLVED |
| `test_analyze_incident_response_structure_completeness` | All required fields |
| `test_analyze_incident_resolve_returns_none` | 404 |
| `test_analyze_incident_unexpected_exception` | 500 |

**Integration Tests** (`tests/integration/test_analysis_integration.py`) - 3 tests:

| Test | Dependencies | Expected |
|------|--------------|----------|
| `test_analyze_incident_real_erp_success` | ERPNext + Claude | status=RESOLVED |
| `test_analyze_incident_invoice_not_found_in_erp` | ERPNext + Claude | status=UNDER_REVIEW |
| `test_analyze_incident_id_not_found` | None | 404 |

---

## 2. How to Test

### 2.1 Framework: Pytest

**Commands:**
- All tests: `pytest tests/ -v`
- API only: `pytest tests/api/ -v`
- Integration only: `pytest tests/integration/ -v`
- With coverage: `pytest tests/ --cov=app --cov-report=html`

### 2.2 API Tests - Full Mocking

| Component | Mock |
|-----------|------|
| AI Client | `tests/mocks/mock_ai_client.py` |
| ERP Client | `tests/mocks/mock_erp_client.py` |
| Database | Fresh SQLite per test (`test.db`) |

### 2.3 Integration Tests - Real Services

| Component | Mode |
|-----------|------|
| ERPNext | REAL (via ngrok) |
| Claude AI | REAL |
| Database | SQLite (`test_integration.db`) |

**Required Environment Variables:**
- `ERPNEXT_BASE_URL`, `ERPNEXT_API_KEY`, `ERPNEXT_API_SECRET`
- `ANTHROPIC_API_KEY`, `AI_ENABLED=true`

If missing → tests skipped via `pytest.skip()`

---

## 3. Exit Criteria

| Criterion | Target |
|-----------|--------|
| API tests pass rate | 100% |
| Integration tests | Pass when env configured, skip otherwise |
| Critical defects | 0 open |
| Coverage | ≥ 60% |

**Testing Complete When:**
- [ ] All 13 API tests pass
- [ ] All 3 integration tests pass (or skipped if no env)
- [ ] No P1/P2 defects open
- [ ] CI pipeline green
