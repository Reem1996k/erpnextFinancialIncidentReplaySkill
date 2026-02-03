import pytest
from unittest.mock import patch
from tests.conftest import client
from tests.conftest import client
from tests.mocks.mock_incident_data import (
    get_valid_incident_payload,
    get_expected_analysis_response_fields,
    get_expected_incident_fields_after_analysis,
)
from tests.mocks.mock_ai_client import (
    get_mock_ai_client_success,
    get_mock_ai_client_exception,
)
from tests.mocks.mock_erp_client import get_mock_erp_client


class TestAnalysisAPI:

    def test_analyze_incident_success(self, client):
        payload = get_valid_incident_payload()
        create_response = client.post("/incidents/", json=payload)
        assert create_response.status_code == 201
        incident_id = create_response.json()["id"]

        with patch(
            "app.controllers.incident_controller.get_ai_client"
        ) as mock_ai_factory, patch(
            "app.controllers.incident_controller.get_erp_client"
        ) as mock_erp_factory:

            mock_ai_factory.return_value = get_mock_ai_client_success()
            mock_erp_factory.return_value = get_mock_erp_client()

            response = client.post(f"/incidents/{incident_id}/analyze")

        assert response.status_code == 200

        data = response.json()
        incident = data["incident"]

        assert incident["status"] == "RESOLVED"
        assert incident["analysis_source"] == "AI"
        assert 0.0 <= incident["confidence_score"] <= 1.0
        assert incident["replay_summary"]
        assert incident["replay_conclusion"]

    def test_analyze_incident_not_found(self, client):
        response = client.post("/incidents/999999/analyze")
        assert response.status_code == 404

    def test_analyze_incident_internal_error(self, client):
        payload = get_valid_incident_payload()
        create_response = client.post("/incidents/", json=payload)
        assert create_response.status_code == 201
        incident_id = create_response.json()["id"]

        with patch(
            "app.controllers.incident_controller.get_ai_client"
        ) as mock_ai_factory, patch(
            "app.controllers.incident_controller.get_erp_client"
        ) as mock_erp_factory:

            mock_ai_factory.return_value = get_mock_ai_client_exception()
            mock_erp_factory.return_value = get_mock_erp_client()

            response = client.post(f"/incidents/{incident_id}/analyze")

        assert response.status_code == 200

        incident = response.json()["incident"]
        assert incident["status"] == "UNDER_REVIEW"
        assert incident["analysis_source"] == "AI_FAILED"
        assert incident["confidence_score"] == 0.0

    def test_analyze_incident_with_partial_erp_data(self, client):
        payload = get_valid_incident_payload()
        create_response = client.post("/incidents/", json=payload)
        assert create_response.status_code == 201
        incident_id = create_response.json()["id"]

        with patch(
            "app.controllers.incident_controller.get_ai_client"
        ) as mock_ai_factory, patch(
            "app.controllers.incident_controller.get_erp_client"
        ) as mock_erp_factory:

            mock_ai_factory.return_value = get_mock_ai_client_success()
            mock_erp_factory.return_value = get_mock_erp_client()

            response = client.post(f"/incidents/{incident_id}/analyze")

        assert response.status_code == 200
        incident = response.json()["incident"]

        assert incident["status"] == "RESOLVED"

    def test_analyze_incident_response_structure_completeness(self, client):
        payload = get_valid_incident_payload()
        create_response = client.post("/incidents/", json=payload)
        assert create_response.status_code == 201
        incident_id = create_response.json()["id"]

        with patch(
            "app.controllers.incident_controller.get_ai_client"
        ) as mock_ai_factory, patch(
            "app.controllers.incident_controller.get_erp_client"
        ) as mock_erp_factory:

            mock_ai_factory.return_value = get_mock_ai_client_success()
            mock_erp_factory.return_value = get_mock_erp_client()

            response = client.post(f"/incidents/{incident_id}/analyze")

        assert response.status_code == 200

        incident = response.json()["incident"]
        required_fields = [
            "id",
            "erp_reference",
            "status",
            "analysis_source",
            "confidence_score",
            "replay_summary",
            "replay_conclusion",
        ]

        for field in required_fields:
            assert field in incident
            assert incident[field] is not None

    def test_analyze_incident_resolve_returns_none(self, client):
        payload = get_valid_incident_payload()
        create_response = client.post("/incidents/", json=payload)
        assert create_response.status_code == 201
        incident_id = create_response.json()["id"]

        with patch(
            "app.api.analysis.resolve_incident"
        ) as mock_resolve:

            mock_resolve.return_value = None

            response = client.post(f"/incidents/{incident_id}/analyze")

        assert response.status_code == 404
        data = response.json()
        assert "not found after analysis" in data["detail"]
    
    def test_analyze_incident_unexpected_exception(self, client):
        payload = get_valid_incident_payload()
        create_response = client.post("/incidents/", json=payload)
        assert create_response.status_code == 201
        incident_id = create_response.json()["id"]

        with patch(
            "app.api.analysis.resolve_incident"
        ) as mock_resolve:

            mock_resolve.side_effect = RuntimeError("boom")

            response = client.post(f"/incidents/{incident_id}/analyze")

        assert response.status_code == 500
        data = response.json()
        assert "Analysis failed" in data["detail"]

