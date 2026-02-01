"""
Integration Tests for POST /incidents/{incident_id}/analyze

🎯 PURPOSE:
These are REAL integration tests - NO MOCKS.
They validate the complete system behavior including:
- Real ERPNext API calls via ngrok
- Real Anthropic Claude AI analysis
- Real database operations
- Real error handling

🔧 PRODUCTION RISKS COVERED:
1. ERPNext connectivity and data extraction
2. AI API availability and response quality
3. Graceful degradation when AI fails
4. End-to-end data flow from ERP → AI → Database
5. Business logic validation (status transitions)

⚙️ REQUIREMENTS:
- Environment variables must be set:
  - ERPNEXT_BASE_URL (ngrok URL)
  - ERPNEXT_API_KEY
  - ERPNEXT_API_SECRET
  - ANTHROPIC_API_KEY
  - AI_ENABLED=true
- Real invoice must exist in ERPNext
- Tests will consume API credits (Anthropic)

📊 TEST STRATEGY:
- Use real invoice IDs from production ERPNext
- Validate business outcomes, not implementation details
- Assert graceful failures (HTTP 200 with UNDER_REVIEW)
- NO skips - if tests fail, system is broken
"""

import pytest
import os


class TestAnalysisIntegration:
    """
    Integration tests for incident analysis endpoint.
    
    These tests validate REAL system behavior with external dependencies.
    """

    # =========================
    # Configuration
    # =========================
    
    # Use a REAL invoice ID that exists in your ERPNext instance
    # This should be updated based on your test environment
    VALID_INVOICE_ID = "ACC-SINV-2026-00009"
    
    # Invalid invoice ID that does not exist in ERPNext
    INVALID_INVOICE_ID = "FAKE-INVOICE-99999"

    # =========================
    # Happy Path - Real ERP + Real AI
    # =========================

    def test_analyze_incident_real_erp_success(self, client):
        """
        ✅ INTEGRATION TEST: Full flow with real ERP and AI.
        
        Flow:
        1. Create incident with REAL invoice ID
        2. Call analyze endpoint
        3. System fetches REAL data from ERPNext
        4. System calls REAL Claude API
        5. AI returns analysis
        6. Incident status → RESOLVED
        
        Production Risk Coverage:
        - Validates ERPNext connectivity
        - Validates AI API availability
        - Validates complete data pipeline
        - Validates business logic correctness
        
        ⚠️ This test consumes real API credits.
        """
        
        # Arrange: Create incident with REAL invoice ID
        incident_payload = {
            "erp_reference": self.VALID_INVOICE_ID,
            "incident_type": "Pricing_Issue",
            "description": "Integration test - validate real ERP + AI flow"
        }
        
        create_response = client.post("/incidents/", json=incident_payload)
        assert create_response.status_code == 201, f"Failed to create incident: {create_response.json()}"
        
        incident_id = create_response.json()["id"]
        
        # Act: Trigger analysis with REAL external calls
        analyze_response = client.post(f"/incidents/{incident_id}/analyze")
        
        # Assert: Validate successful analysis
        assert analyze_response.status_code == 200, (
            f"Expected HTTP 200, got {analyze_response.status_code}. "
            f"Response: {analyze_response.json()}"
        )
        
        data = analyze_response.json()
        
        # Validate response structure
        assert data["success"] is True
        assert data["incident_id"] == incident_id
        assert "incident" in data
        
        incident = data["incident"]
        
        # Validate business outcome: AI succeeded
        assert incident["status"] == "RESOLVED", (
            f"Expected status RESOLVED for successful AI analysis, got {incident['status']}"
        )
        assert incident["analysis_source"] == "AI", (
            f"Expected analysis_source AI, got {incident['analysis_source']}"
        )
        
        # Validate AI analysis quality
        assert isinstance(incident["confidence_score"], (int, float)), (
            f"confidence_score must be numeric, got {type(incident['confidence_score'])}"
        )
        assert 0.0 <= incident["confidence_score"] <= 1.0, (
            f"confidence_score must be between 0 and 1, got {incident['confidence_score']}"
        )
        
        # Validate AI generated content
        assert incident["replay_summary"], "replay_summary must not be empty"
        assert len(incident["replay_summary"]) > 20, (
            "replay_summary too short - AI should provide detailed analysis"
        )
        
        assert incident["replay_conclusion"], "replay_conclusion must not be empty"
        assert len(incident["replay_conclusion"]) > 10, (
            "replay_conclusion too short - AI should provide actionable conclusion"
        )
        
        # Validate ERP reference is preserved
        assert incident["erp_reference"] == self.VALID_INVOICE_ID

    # =========================
    # Error Case - Invoice Not Found in ERP
    # =========================

    def test_analyze_incident_invoice_not_found_in_erp(self, client):
        """
        ⚠️ INTEGRATION TEST: AI handles missing ERP data gracefully.
        
        Flow:
        1. Create incident with FAKE invoice ID
        2. Call analyze endpoint
        3. System tries to fetch data from ERPNext → fails or returns empty
        4. AI analysis fails due to missing data
        5. Incident status → UNDER_REVIEW (graceful degradation)
        
        Production Risk Coverage:
        - Validates graceful handling of ERP errors
        - Validates AI failure path
        - Validates NO crashes on invalid data
        - API returns HTTP 200 (not 500) for business failures
        
        Business Requirement:
        - AI failures must NOT crash the API
        - System must mark incident as UNDER_REVIEW for manual intervention
        """
        
        # Arrange: Create incident with FAKE invoice ID
        incident_payload = {
            "erp_reference": self.INVALID_INVOICE_ID,
            "incident_type": "Data_Quality_Issue",
            "description": "Integration test - validate AI failure handling"
        }
        
        create_response = client.post("/incidents/", json=incident_payload)
        assert create_response.status_code == 201
        
        incident_id = create_response.json()["id"]
        
        # Act: Trigger analysis (ERP will return no data or error)
        analyze_response = client.post(f"/incidents/{incident_id}/analyze")
        
        # Assert: API does NOT crash - returns HTTP 200
        assert analyze_response.status_code == 200, (
            f"API should return 200 even for AI failures, got {analyze_response.status_code}. "
            f"Response: {analyze_response.json()}"
        )
        
        data = analyze_response.json()
        incident = data["incident"]
        
        # Validate graceful failure: UNDER_REVIEW (not RESOLVED)
        assert incident["status"] == "UNDER_REVIEW", (
            f"Expected status UNDER_REVIEW for AI failure, got {incident['status']}. "
            f"AI should NOT mark as RESOLVED when data is missing."
        )
        
        assert incident["analysis_source"] == "AI_FAILED", (
            f"Expected analysis_source AI_FAILED, got {incident['analysis_source']}"
        )
        
        # Validate failure indicators
        assert incident["confidence_score"] == 0.0, (
            f"confidence_score should be 0.0 for failed analysis, got {incident['confidence_score']}"
        )
        
        # System should provide error details
        assert incident["replay_summary"], "replay_summary must indicate failure"
        assert "fail" in incident["replay_summary"].lower() or "error" in incident["replay_summary"].lower(), (
            "replay_summary should indicate analysis failure"
        )

    # =========================
    # Error Case - Incident Not Found
    # =========================

    def test_analyze_incident_id_not_found(self, client):
        """
        ❌ INTEGRATION TEST: Validate 404 for non-existent incident.
        
        Flow:
        1. Call analyze endpoint with non-existent incident ID
        2. System returns HTTP 404
        
        Production Risk Coverage:
        - Validates proper error handling
        - Validates no crashes on invalid input
        - Validates correct HTTP status codes
        
        Business Logic:
        - 404 = incident does not exist (NOT AI failure)
        - 200 + UNDER_REVIEW = incident exists but AI failed
        """
        
        # Act: Try to analyze non-existent incident
        non_existent_id = 999999
        analyze_response = client.post(f"/incidents/{non_existent_id}/analyze")
        
        # Assert: Returns 404 NOT FOUND
        assert analyze_response.status_code == 404, (
            f"Expected HTTP 404 for non-existent incident, got {analyze_response.status_code}"
        )
        
        error_data = analyze_response.json()
        assert "detail" in error_data
        assert "not found" in error_data["detail"].lower(), (
            f"Error message should indicate incident not found. Got: {error_data['detail']}"
        )
        assert str(non_existent_id) in error_data["detail"], (
            "Error message should include the incident ID that was not found"
        )

   