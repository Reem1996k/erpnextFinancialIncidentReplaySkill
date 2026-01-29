"""
AI-assisted incident analyzer using LLM integration.

This module provides AI-powered analysis when rule-based analyzers
cannot determine a clear outcome. It uses structured prompts and JSON
responses to ensure consistent, parseable analysis results.

Supports multiple LLM providers through environment variables:
- OPENAI_API_KEY: Use OpenAI API
- ANTHROPIC_API_KEY: Use Anthropic Claude API
- LLM_API_URL: Custom LLM API endpoint
"""

import json
import os
from typing import Dict, Any, Optional
from app.services.incident_analyzers import AnalysisResult


class AIAnalyzerConfig:
    """Configuration for AI analyzer."""
    
    def __init__(self):
        """Initialize AI analyzer configuration from environment."""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.custom_api_url = os.getenv("LLM_API_URL")
        self.model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
        self.timeout = int(os.getenv("LLM_TIMEOUT", "30"))
    
    def is_configured(self) -> bool:
        """Check if AI analysis is configured."""
        return bool(
            self.openai_api_key or 
            self.anthropic_api_key or 
            self.custom_api_url
        )


class AIAnalyzer:
    """
    AI-powered incident analyzer.
    
    Uses LLM to analyze financial incidents when rule-based analysis
    returns UNDETERMINED. Requests structured JSON responses to ensure
    consistent parsing and handling.
    
    Never modifies ERP data or writes to database directly.
    """
    
    def __init__(self, config: Optional[AIAnalyzerConfig] = None):
        """
        Initialize AI analyzer with configuration.
        
        Args:
            config: AIAnalyzerConfig instance. If None, creates new from env.
        """
        self.config = config or AIAnalyzerConfig()
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate that AI analysis is properly configured."""
        if not self.config.is_configured():
            raise ValueError(
                "AI Analyzer requires one of: OPENAI_API_KEY, ANTHROPIC_API_KEY, or LLM_API_URL"
            )
    
    def analyze(self, erp_data: Dict[str, Any], incident_description: str) -> AnalysisResult:
        """
        Analyze incident using AI.
        
        Args:
            erp_data: Dictionary containing ERP data (invoice, sales order, customer)
            incident_description: User-provided incident description
        
        Returns:
            AnalysisResult with AI-generated analysis
        """
        try:
            # Build structured prompt
            prompt = self._build_prompt(erp_data, incident_description)
            
            # Call LLM
            ai_response = self._call_llm(prompt)
            
            # Parse structured response
            analysis = self._parse_ai_response(ai_response)
            
            return AnalysisResult(
                decision=analysis.get("decision", "PENDING_REVIEW"),
                summary=analysis.get("root_cause_summary", "AI analysis completed"),
                details=self._format_details(analysis),
                conclusion=analysis.get("recommended_actions_summary", "Review recommended"),
                confidence=analysis.get("confidence", 0.7),
                analysis_source="AI"
            )
        
        except Exception as e:
            # Fallback to manual review on any AI analysis error
            return AnalysisResult(
                decision="PENDING_REVIEW",
                summary="AI analysis failed",
                details=f"Error during AI analysis: {str(e)}",
                conclusion="Manual review recommended due to AI analysis failure",
                confidence=0.0,
                analysis_source="FALLBACK"
            )
    
    def _build_prompt(self, erp_data: Dict[str, Any], incident_description: str) -> str:
        """
        Build structured prompt for LLM analysis.
        
        Args:
            erp_data: ERP data dictionary
            incident_description: Incident description
        
        Returns:
            Formatted prompt string
        """
        invoice = erp_data.get("invoice", {})
        sales_order = erp_data.get("sales_order", {})
        customer = erp_data.get("customer", {})
        
        prompt = f"""You are a financial incident analyst for an ERP system. 
Analyze the following incident and provide a structured JSON response.

INCIDENT DESCRIPTION:
{incident_description}

INVOICE DATA:
- Name: {invoice.get('name', 'N/A')}
- Customer: {invoice.get('customer_name', 'N/A')}
- Amount: {invoice.get('total_amount', 'N/A')} {invoice.get('currency', 'USD')}
- Items Count: {len(invoice.get('items', []))}
- Date: {invoice.get('posting_date', 'N/A')}
- Due Date: {invoice.get('due_date', 'N/A')}
- Status: {invoice.get('docstatus', 'N/A')}

LINKED SALES ORDER DATA:
- Name: {sales_order.get('name', 'N/A')}
- Amount: {sales_order.get('total_amount', 'N/A')}
- Delivery Status: {sales_order.get('delivery_status', 'N/A')}
- Billing Status: {sales_order.get('billing_status', 'N/A')}
- Status: {sales_order.get('docstatus', 'N/A')}

CUSTOMER DATA:
- Group: {customer.get('customer_group', 'N/A')}
- Credit Limit: {customer.get('credit_limit', 'N/A')}
- Outstanding Amount: {customer.get('outstanding_amount', 'N/A')}

KNOWN BUSINESS RULES:
1. Pricing variance within ±20% is acceptable with review
2. Invoice amounts must match linked sales order
3. Delivery and billing statuses must align
4. Duplicates detected by matching: amount, vendor, date
5. All financial decisions require audit trail

BUSINESS RULES CONTEXT:
- System prevents data modification - analysis only
- All recommendations must be actionable
- Confidence scores guide manual review needs
- Risk levels: Low (< 10% variance), Medium (10-50%), High (> 50%)

RESPOND WITH VALID JSON ONLY (no markdown, no extra text):
{{
  "suggested_incident_type": "string (Pricing_Issue | Duplicate_Invoice | Delivery_or_Billing_Mismatch | Other)",
  "root_cause_summary": "string (one-line summary of likely root cause)",
  "key_findings": ["string", "string"] (list of 2-3 key findings),
  "risk_level": "string (Low | Medium | High)",
  "decision": "string (APPROVED_WITH_RISK | REJECTED | PENDING_REVIEW)",
  "recommended_actions": ["string", "string"] (list of 2-3 recommended actions),
  "confidence": 0.0-1.0 (your confidence in this analysis),
  "reasoning": "string (brief explanation of your reasoning)"
}}

Analyze and respond with JSON only:"""
        
        return prompt
    
    def _call_llm(self, prompt: str) -> str:
        """
        Call LLM with prompt.
        
        Args:
            prompt: Prompt to send to LLM
        
        Returns:
            LLM response string
        
        Raises:
            RuntimeError: If LLM call fails
        """
        if self.config.openai_api_key:
            return self._call_openai(prompt)
        elif self.config.anthropic_api_key:
            return self._call_anthropic(prompt)
        elif self.config.custom_api_url:
            return self._call_custom_api(prompt)
        else:
            raise RuntimeError("No LLM provider configured")
    
    def _call_openai(self, prompt: str) -> str:
        """
        Call OpenAI API.
        
        Args:
            prompt: Prompt to analyze
        
        Returns:
            Response content
        """
        try:
            import openai
            openai.api_key = self.config.openai_api_key
            
            response = openai.ChatCompletion.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": "You are a financial analyst. Respond with JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                timeout=self.config.timeout
            )
            
            return response.choices[0].message.content
        except ImportError:
            raise RuntimeError("openai package not installed. Install with: pip install openai")
    
    def _call_anthropic(self, prompt: str) -> str:
        """
        Call Anthropic Claude API.
        
        Args:
            prompt: Prompt to analyze
        
        Returns:
            Response content
        """
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.config.anthropic_api_key)
            response = client.messages.create(
                model=self.config.model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text
        except ImportError:
            raise RuntimeError("anthropic package not installed. Install with: pip install anthropic")
    
    def _call_custom_api(self, prompt: str) -> str:
        """
        Call custom LLM API.
        
        Args:
            prompt: Prompt to analyze
        
        Returns:
            Response content
        """
        try:
            import requests
            
            payload = {
                "prompt": prompt,
                "model": self.config.model,
                "max_tokens": 1024
            }
            
            response = requests.post(
                self.config.custom_api_url,
                json=payload,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get("response", data.get("text", ""))
        except ImportError:
            raise RuntimeError("requests package not installed. Install with: pip install requests")
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """
        Parse structured JSON response from AI.
        
        Args:
            response: LLM response string
        
        Returns:
            Parsed JSON as dictionary
        
        Raises:
            ValueError: If response is not valid JSON
        """
        # Try to extract JSON from response (in case of markdown formatting)
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
        
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response from AI: {str(e)}. Response: {response}")
    
    def _format_details(self, analysis: Dict[str, Any]) -> str:
        """
        Format AI analysis into details string.
        
        Args:
            analysis: Parsed AI analysis
        
        Returns:
            Formatted details string
        """
        findings = analysis.get("key_findings", [])
        details = "Key Findings:\n"
        for finding in findings:
            details += f"- {finding}\n"
        
        details += f"\nRisk Level: {analysis.get('risk_level', 'Unknown')}\n"
        details += f"Reasoning: {analysis.get('reasoning', 'N/A')}\n"
        
        return details
