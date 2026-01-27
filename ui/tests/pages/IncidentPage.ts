import { Page, Locator } from '@playwright/test';

/**
 * Page Object Model for the Financial Incident Replay page.
 * 
 * Encapsulates all interactions with the incident replay UI including:
 * - Navigation
 * - Element locators
 * - User actions
 * - Assertions
 */
export class IncidentPage {
  readonly page: Page;
  
  // Header elements
  readonly pageTitle: Locator;
  readonly incidentReference: Locator;
  
  // Incident information section
  readonly incidentIdValue: Locator;
  readonly erpReferenceValue: Locator;
  readonly incidentTypeValue: Locator;
  readonly statusBadge: Locator;
  readonly descriptionText: Locator;
  
  // Analysis state indicators
  readonly noAnalysisMessage: Locator;
  readonly runAnalysisButton: Locator;
  
  // Analysis results sections
  readonly summarySection: Locator;
  readonly summaryContent: Locator;
  readonly detailsSection: Locator;
  readonly detailsContent: Locator;
  readonly conclusionSection: Locator;
  readonly conclusionContent: Locator;
  
  // Decision badge
  readonly decisionBadge: Locator;
  readonly decisionText: Locator;
  
  // Footer
  readonly footerText: Locator;

  constructor(page: Page) {
    this.page = page;
    
    // Header locators
    this.pageTitle = page.locator('h1').filter({ hasText: 'Financial Incident Replay' }).first();
    this.incidentReference = page.locator('.header p');
    
    // Incident information locators (using data-testid where possible, fallback to text/class)
    this.incidentIdValue = page.locator('[data-testid="incident-id"]').or(
      page.locator('.metadata-value').first()
    );
    this.erpReferenceValue = page.locator('[data-testid="erp-reference"]').or(
      page.locator('.metadata-item', { has: page.locator(':has-text("ERP Reference")') }).locator('.metadata-value')
    );
    this.incidentTypeValue = page.locator('[data-testid="incident-type"]').or(
      page.locator('.metadata-item', { has: page.locator(':has-text("Incident Type")') }).locator('.metadata-value')
    );
    this.statusBadge = page.locator('.status-badge');
    this.descriptionText = page.locator('.description-box');
    
    // Analysis state locators
    this.noAnalysisMessage = page.locator('.no-analysis');
    this.runAnalysisButton = page.locator('button').filter({ hasText: /Run Replay|Analyze|Replay/ });
    
    // Analysis results locators
    this.summarySection = page.locator('.section', { has: page.locator(':has-text("Summary")') });
    this.summaryContent = page.locator('[data-testid="summary-content"]').or(
      this.summarySection.locator('.content-box')
    );
    this.detailsSection = page.locator('.section', { has: page.locator(':has-text("Details")') });
    this.detailsContent = page.locator('[data-testid="details-content"]').or(
      this.detailsSection.locator('.content-box')
    );
    this.conclusionSection = page.locator('.section', { has: page.locator(':has-text("Conclusion")') });
    this.conclusionContent = page.locator('[data-testid="conclusion-content"]').or(
      this.conclusionSection.locator('.decision-box p')
    );
    
    // Decision badge locators
    this.decisionBadge = page.locator('.decision-badge');
    this.decisionText = this.decisionBadge.locator('text=');
    
    // Footer
    this.footerText = page.locator('.footer');
  }

  /**
   * Navigate to the incident replay page by incident ID.
   * 
   * @param incidentId - The ID of the incident to view
   */
  async navigateToIncident(incidentId: number): Promise<void> {
    await this.page.goto(`/ui/incidents/${incidentId}`);
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * Verify the page title is visible.
   */
  async verifyPageTitleVisible(): Promise<void> {
    await this.pageTitle.waitFor({ state: 'visible' });
  }

  /**
   * Get the incident ERP reference from the header.
   */
  async getIncidentReference(): Promise<string> {
    await this.incidentReference.waitFor({ state: 'visible' });
    return await this.incidentReference.textContent() || '';
  }

  /**
   * Get the current status of the incident.
   */
  async getIncidentStatus(): Promise<string> {
    await this.statusBadge.waitFor({ state: 'visible' });
    return await this.statusBadge.textContent() || '';
  }

  /**
   * Check if the incident has been analyzed (status == ANALYZED).
   */
  async isAnalyzed(): Promise<boolean> {
    const status = await this.getIncidentStatus();
    return status.trim() === 'ANALYZED';
  }

  /**
   * Check if the "no analysis" message is visible.
   */
  async hasNoAnalysisMessage(): Promise<boolean> {
    try {
      await this.noAnalysisMessage.waitFor({ state: 'visible', timeout: 2000 });
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Get the incident type.
   */
  async getIncidentType(): Promise<string> {
    return await this.incidentTypeValue.textContent() || '';
  }

  /**
   * Get the incident description.
   */
  async getDescription(): Promise<string> {
    return await this.descriptionText.textContent() || '';
  }

  /**
   * Click the "Run Replay Analysis" button to trigger analysis.
   * 
   * Note: In the current implementation, this button might not be visible.
   * The test assumes the backend processes the replay via a POST request.
   */
  async clickRunAnalysisButton(): Promise<void> {
    try {
      await this.runAnalysisButton.waitFor({ state: 'visible', timeout: 2000 });
      await this.runAnalysisButton.click();
    } catch {
      // Button might not be visible in current implementation
      console.log('Run Analysis button not found - analysis may need to be triggered via API');
    }
  }

  /**
   * Verify the Analysis Summary section is visible.
   */
  async verifySummarySectionVisible(): Promise<void> {
    await this.summarySection.waitFor({ state: 'visible' });
  }

  /**
   * Get the summary content text.
   */
  async getSummaryContent(): Promise<string> {
    return await this.summaryContent.textContent() || '';
  }

  /**
   * Verify the Analysis Details section is visible.
   */
  async verifyDetailsSectionVisible(): Promise<void> {
    await this.detailsSection.waitFor({ state: 'visible' });
  }

  /**
   * Get the details content text.
   */
  async getDetailsContent(): Promise<string> {
    return await this.detailsContent.textContent() || '';
  }

  /**
   * Verify the Conclusion section is visible.
   */
  async verifyConclusionSectionVisible(): Promise<void> {
    await this.conclusionSection.waitFor({ state: 'visible' });
  }

  /**
   * Get the conclusion content text.
   */
  async getConclusionContent(): Promise<string> {
    return await this.conclusionContent.textContent() || '';
  }

  /**
   * Verify a decision badge is visible.
   */
  async verifyDecisionBadgeVisible(): Promise<void> {
    await this.decisionBadge.waitFor({ state: 'visible' });
  }

  /**
   * Get the decision badge text.
   */
  async getDecisionBadgeText(): Promise<string> {
    await this.decisionBadge.waitFor({ state: 'visible' });
    return await this.decisionBadge.textContent() || '';
  }

  /**
   * Check if a specific decision type is shown in the badge.
   * 
   * @param decisionType - The decision type to check (e.g., 'APPROVED_WITH_RISK', 'REJECTED')
   */
  async hasDecisionType(decisionType: string): Promise<boolean> {
    const badgeText = await this.getDecisionBadgeText();
    return badgeText.toUpperCase().includes(decisionType.toUpperCase());
  }

  /**
   * Wait for the page to load completely.
   */
  async waitForPageLoad(): Promise<void> {
    await this.pageTitle.waitFor({ state: 'visible' });
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * Get the page URL.
   */
  getPageUrl(): string {
    return this.page.url();
  }

  /**
   * Take a screenshot for debugging.
   */
  async takeScreenshot(filename: string): Promise<void> {
    await this.page.screenshot({ path: `./tests/screenshots/${filename}.png` });
  }
}
