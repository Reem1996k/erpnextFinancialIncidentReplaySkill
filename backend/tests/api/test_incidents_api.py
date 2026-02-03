from tests.mocks.mock_incident_data import (
    get_valid_incident_payload,
    get_duplicate_incident_payload,
    get_expected_incident_status,
)


class TestIncidentsAPI:
    """
    API tests for /incidents endpoints.
    These tests are fully isolated and do not depend on execution order.
    """

    # =========================
    # POST /incidents
    # =========================

    def test_create_incident_success(self, client):
        """
        Happy path: create a new incident successfully.
        """

        # Arrange
        payload = get_valid_incident_payload()

        # Act
        response = client.post("/incidents/", json=payload)

        # Assert
        assert response.status_code == 201

        data = response.json()

        assert "id" in data
        assert isinstance(data["id"], int)

        assert data["erp_reference"] == payload["erp_reference"]
        assert data["incident_type"] == payload["incident_type"]
        assert data["description"] == payload["description"]
        assert data["status"] == get_expected_incident_status()

    def test_create_duplicate_incident_returns_409(self, client):
        """
        Creating an incident with the same ERP reference should fail.
        """

        payload = get_valid_incident_payload()

        # First creation
        first_response = client.post("/incidents/", json=payload)
        assert first_response.status_code == 201

        # Duplicate creation
        second_response = client.post("/incidents/", json=payload)

        assert second_response.status_code == 409
        assert "already exists" in second_response.json()["detail"].lower()

    # =========================
    # GET /incidents
    # =========================

    def test_get_incidents_returns_empty_list_when_no_data(self, client):
        """
        If no incidents exist, API should return an empty list.
        """

        response = client.get("/incidents/")

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert data == []

    def test_get_incidents_returns_created_incidents(self, client):
        """
        After creating incidents, GET /incidents should return them.
        """

        # Arrange
        payload = get_valid_incident_payload()

        create_response = client.post("/incidents/", json=payload)
        assert create_response.status_code == 201

        created_id = create_response.json()["id"]

        # Act
        response = client.get("/incidents/")

        # Assert
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1

        incident = data[0]
        assert incident["id"] == created_id
        assert incident["erp_reference"] == payload["erp_reference"]

    # =========================
    # GET /incidents/{id}
    # =========================

    def test_get_incident_by_id_success(self, client):
        """
        Get incident by ID when it exists.
        """

        payload = get_valid_incident_payload()

        create_response = client.post("/incidents/", json=payload)
        assert create_response.status_code == 201

        incident_id = create_response.json()["id"]

        # Act
        response = client.get(f"/incidents/{incident_id}")

        # Assert
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == incident_id
        assert data["erp_reference"] == payload["erp_reference"]
        assert data["status"] == get_expected_incident_status()

    def test_get_incident_by_id_not_found(self, client):
        """
        Requesting a non-existing incident should return 404.
        """

        response = client.get("/incidents/999999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
