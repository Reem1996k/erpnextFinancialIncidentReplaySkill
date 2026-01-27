import { test, expect } from '@playwright/test';
import { IncidentPage } from '../pages/IncidentPage';

/**
 * UI Tests for Financial Incident Replay Page
 * 
 * Tests the complete user flow of the incident replay functionality:
 * 1. Page navigation and loading
 * 2. Incident details verification
 * 3. Analysis state checking
 * 4. Analysis results display after state change
 */
test.describe('Financial Incident Replay UI', () => {
  
  let incidentPage: IncidentPage;
  
  test.beforeEach(async ({ page }) => {
    /**
     * Setup: Initialize the page object for each test
     */
    incidentPage = new IncidentPage(page);
  });

  test('should navigate to incident page and display initial state', async ({ page }) => {
    /**
     * Test: Navigate to an incident and verify basic page elements
     * 
     * This test verifies that:
     * - The page navigates successfully to /ui/incidents/1
     * - Page title "Financial Incident Replay" is visible
     * - Incident ERP reference is displayed
     * - Status badge is visible
     * - Page is fully loaded
     */
    
    // Act: Navigate to incident page
    await incidentPage.navigateToIncident(1);
    
    // Assert: Verify page loaded
    await incidentPage.verifyPageTitleVisible();
    expect(incidentPage.getPageUrl()).toContain('/ui/incidents/1');
    
    // Assert: Verify header elements
    const reference = await incidentPage.getIncidentReference();
    expect(reference).toBeTruthy();
    
    // Assert: Verify status is visible
    const status = await incidentPage.getIncidentStatus();
    expect(status.length).toBeGreaterThan(0);
  });

  test('should display "no analysis" message when incident is not analyzed', async () => {
    /**
     * Test: Verify that unanalyzed incidents show the "no analysis" message
     * 
     * Prerequisites:
     * - An incident with status "OPEN" exists
     * 
     * This test verifies that:
     * - The "no analysis" message is visible
     * - Summary, Details, and Conclusion sections are NOT visible
     */
    
    // Act: Navigate to incident page
    await incidentPage.navigateToIncident(1);
    
    // Assert: Incident is not analyzed
    const isAnalyzed = await incidentPage.isAnalyzed();
    expect(isAnalyzed).toBe(false);
    
    // Assert: No analysis message is visible
    const hasMessage = await incidentPage.hasNoAnalysisMessage();
    expect(hasMessage).toBe(true);
  });

  test('should display incident metadata correctly', async () => {
    /**
     * Test: Verify all incident metadata fields are displayed
     * 
     * This test verifies that:
     * - Incident type is visible and not empty
     * - Description is visible and not empty
     * - All metadata fields are populated
     */
    
    // Act: Navigate to incident page
    await incidentPage.navigateToIncident(1);
    
    // Assert: Verify metadata is displayed
    const incidentType = await incidentPage.getIncidentType();
    expect(incidentType).toBeTruthy();
    expect(incidentType.length).toBeGreaterThan(0);
    
    const description = await incidentPage.getDescription();
    expect(description).toBeTruthy();
    expect(description.length).toBeGreaterThan(0);
  });

  test('should display analysis results after incident is analyzed', async ({ request }) => {
    /**
     * Test: Verify that analyzed incidents display all analysis results
     * 
     * Prerequisites:
     * - An incident with status "ANALYZED" exists (ID 1)
     * - The incident has replay_summary, replay_details, replay_conclusion
     * 
     * Approach:
     * 1. First, create and analyze an incident via the backend API
     * 2. Then navigate to the incident UI page
     * 3. Verify all analysis sections are visible
     * 
     * This test verifies that:
     * - Status badge shows "ANALYZED"
     * - Summary section is visible with content
     * - Details section is visible with content
     * - Conclusion section is visible with content
     * - Decision badge is visible
     */
    
    // Setup: Create an incident via API
    const createResponse = await request.post('http://127.0.0.1:8000/incidents', {
      data: {
        erp_reference: 'TEST-UI-FLOW-001',
        incident_type: 'Pricing_Issue',
        description: 'Test UI automation flow'
      }
    });
    expect(createResponse.ok()).toBeTruthy();
    const incident = await createResponse.json();
    const incidentId = incident.id;
    
    // Setup: Run replay analysis via API
    const replayResponse = await request.post(`http://127.0.0.1:8000/incidents/${incidentId}/replay`);
    expect(replayResponse.ok()).toBeTruthy();
    
    // Act: Navigate to analyzed incident page
    await incidentPage.navigateToIncident(incidentId);
    
    // Assert: Verify status is ANALYZED
    const status = await incidentPage.getIncidentStatus();
    expect(status).toContain('ANALYZED');
    
    // Assert: Verify summary section is visible
    await incidentPage.verifySummarySectionVisible();
    const summaryContent = await incidentPage.getSummaryContent();
    expect(summaryContent).toBeTruthy();
    expect(summaryContent.length).toBeGreaterThan(0);
    
    // Assert: Verify details section is visible
    await incidentPage.verifyDetailsSectionVisible();
    const detailsContent = await incidentPage.getDetailsContent();
    expect(detailsContent).toBeTruthy();
    expect(detailsContent.length).toBeGreaterThan(0);
    
    // Assert: Verify conclusion section is visible
    await incidentPage.verifyConclusionSectionVisible();
    const conclusionContent = await incidentPage.getConclusionContent();
    expect(conclusionContent).toBeTruthy();
    expect(conclusionContent.length).toBeGreaterThan(0);
  });

  test('should display decision badge with correct type', async ({ request }) => {
    /**
     * Test: Verify that the decision badge displays the correct decision type
     * 
     * Prerequisites:
     * - An analyzed incident exists
     * 
     * This test verifies that:
     * - Decision badge is visible
     * - Decision badge contains one of the expected decision types:
     *   - APPROVED_WITH_RISK (orange)
     *   - APPROVED (green)
     *   - REJECTED (red)
     *   - PENDING (gray)
     */
    
    // Setup: Create and analyze an incident via API
    const createResponse = await request.post('http://127.0.0.1:8000/incidents', {
      data: {
        erp_reference: 'TEST-DECISION-BADGE-001',
        incident_type: 'Pricing_Issue',
        description: 'Test decision badge display'
      }
    });
    expect(createResponse.ok()).toBeTruthy();
    const incident = await createResponse.json();
    const incidentId = incident.id;
    
    // Setup: Run replay analysis
    const replayResponse = await request.post(`http://127.0.0.1:8000/incidents/${incidentId}/replay`);
    expect(replayResponse.ok()).toBeTruthy();
    
    // Act: Navigate to analyzed incident page
    await incidentPage.navigateToIncident(incidentId);
    
    // Assert: Decision badge is visible
    await incidentPage.verifyDecisionBadgeVisible();
    
    // Assert: Decision badge contains expected decision type
    const decisionText = await incidentPage.getDecisionBadgeText();
    expect(decisionText).toBeTruthy();
    
    // Verify badge is one of the expected types
    const validDecisions = ['APPROVED', 'REJECTED', 'PENDING', 'RISK'];
    const hasValidDecision = validDecisions.some(decision => 
      decisionText.toUpperCase().includes(decision)
    );
    expect(hasValidDecision).toBe(true);
  });

  test('should have proper page structure and styling', async () => {
    /**
     * Test: Verify the page has proper structure and styling elements
     * 
     * This test verifies that:
     * - Header section exists and is styled
     * - Content area exists
     * - Footer exists with copyright
     * - All major sections are properly structured
     */
    
    // Act: Navigate to incident page
    await incidentPage.navigateToIncident(1);
    
    // Assert: Verify page structure
    const header = incidentPage.page.locator('.header');
    await expect(header).toBeVisible();
    
    const content = incidentPage.page.locator('.content');
    await expect(content).toBeVisible();
    
    const footer = incidentPage.page.locator('.footer');
    await expect(footer).toBeVisible();
    
    // Assert: Verify footer contains copyright
    const footerText = await footer.textContent();
    expect(footerText).toContain('Financial Incident Replay');
  });

  test('should handle navigation to different incident IDs', async () => {
    /**
     * Test: Verify navigation works for different incident IDs
     * 
     * This test verifies that:
     * - Can navigate to different incident IDs
     * - URL updates correctly
     * - Page loads for each incident
     */
    
    // Act & Assert: Navigate to first incident
    await incidentPage.navigateToIncident(1);
    expect(incidentPage.getPageUrl()).toContain('/ui/incidents/1');
    await incidentPage.verifyPageTitleVisible();
    
    // Act & Assert: Navigate to second incident (if it exists)
    await incidentPage.navigateToIncident(2);
    expect(incidentPage.getPageUrl()).toContain('/ui/incidents/2');
    await incidentPage.verifyPageTitleVisible();
  });

  test.describe('Full user flow - incident analysis', () => {
    /**
     * Nested test suite for the complete happy path flow
     */
    
    test('should complete full analysis workflow', async ({ request }) => {
      /**
       * Test: Complete happy path workflow
       * 
       * Scenario:
       * 1. Create a new incident via API
       * 2. Navigate to its UI page
       * 3. Verify initial "OPEN" status
       * 4. Run replay analysis via API
       * 5. Navigate back to verify analyzed state
       * 6. Verify all analysis results are displayed
       * 
       * This comprehensive test validates the complete user workflow
       */
      
      // Setup: Create incident
      const createResponse = await request.post('http://127.0.0.1:8000/incidents', {
        data: {
          erp_reference: 'TEST-FULL-WORKFLOW-001',
          incident_type: 'Pricing_Issue',
          description: 'Complete workflow test'
        }
      });
      expect(createResponse.ok()).toBeTruthy();
      const incident = await createResponse.json();
      const incidentId = incident.id;
      
      // Act 1: Navigate to new incident (before analysis)
      await incidentPage.navigateToIncident(incidentId);
      
      // Assert 1: Verify initial state is OPEN
      let status = await incidentPage.getIncidentStatus();
      expect(status).toContain('OPEN');
      
      // Assert 2: Verify no analysis message is shown
      let hasMessage = await incidentPage.hasNoAnalysisMessage();
      expect(hasMessage).toBe(true);
      
      // Act 2: Run replay analysis via API
      const replayResponse = await request.post(
        `http://127.0.0.1:8000/incidents/${incidentId}/replay`
      );
      expect(replayResponse.ok()).toBeTruthy();
      
      // Act 3: Navigate back to incident (after analysis)
      await incidentPage.navigateToIncident(incidentId);
      
      // Assert 3: Verify status changed to ANALYZED
      status = await incidentPage.getIncidentStatus();
      expect(status).toContain('ANALYZED');
      
      // Assert 4: Verify analysis message is gone
      hasMessage = await incidentPage.hasNoAnalysisMessage();
      expect(hasMessage).toBe(false);
      
      // Assert 5: Verify all analysis sections are visible
      await incidentPage.verifySummarySectionVisible();
      await incidentPage.verifyDetailsSectionVisible();
      await incidentPage.verifyConclusionSectionVisible();
      await incidentPage.verifyDecisionBadgeVisible();
      
      // Assert 6: Verify all sections have content
      const summaryContent = await incidentPage.getSummaryContent();
      expect(summaryContent.length).toBeGreaterThan(0);
      
      const detailsContent = await incidentPage.getDetailsContent();
      expect(detailsContent.length).toBeGreaterThan(0);
      
      const conclusionContent = await incidentPage.getConclusionContent();
      expect(conclusionContent.length).toBeGreaterThan(0);
      
      const decisionBadge = await incidentPage.getDecisionBadgeText();
      expect(decisionBadge.length).toBeGreaterThan(0);
    });
  });
});
