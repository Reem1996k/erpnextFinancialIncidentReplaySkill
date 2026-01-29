"""
Rule-based incident analyzers for known incident types.

This module provides deterministic analyzers for specific incident types:
- Pricing_Issue: Compares invoice amount vs. expected amount
- Duplicate_Invoice: Detects duplicate invoices
- Delivery_or_Billing_Mismatch: Compares delivery and billing statuses

Each analyzer returns a standardized analysis result with:
- decision: APPROVED_WITH_RISK | REJECTED | PENDING_REVIEW
- summary: Brief explanation
- details: Detailed findings
- conclusion: Full analysis conclusion
- confidence: Confidence score (0.0-1.0)
"""

from typing import Dict, Any
from app.db.models import Incident
from app.integrations.erpnext_client_base import BaseERPNextClient


class AnalysisResult:
    """Standardized analysis result structure."""
    
    def __init__(
        self,
        decision: str,
        summary: str,
        details: str,
        conclusion: str,
        confidence: float = 0.9,
        analysis_source: str = "RULE"
    ):
        """
        Initialize an analysis result.
        
        Args:
            decision: APPROVED_WITH_RISK | REJECTED | PENDING_REVIEW | UNDETERMINED
            summary: Brief one-line explanation
            details: Detailed findings
            conclusion: Full conclusion with reasoning
            confidence: Score from 0.0 to 1.0
            analysis_source: "RULE" or "AI"
        """
        self.decision = decision
        self.summary = summary
        self.details = details
        self.conclusion = conclusion
        self.confidence = confidence
        self.analysis_source = analysis_source
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "decision": self.decision,
            "summary": self.summary,
            "details": self.details,
            "conclusion": self.conclusion,
            "confidence": self.confidence,
            "analysis_source": self.analysis_source
        }
    
    def is_undetermined(self) -> bool:
        """Check if analysis result is undetermined (requires AI fallback)."""
        return self.decision == "UNDETERMINED"


class PricingIssueAnalyzer:
    """Analyzer for Pricing_Issue incident type."""
    
    def __init__(self, erp_client: BaseERPNextClient):
        """Initialize with ERP client."""
        self.erp_client = erp_client
    
    def analyze(self, incident: Incident) -> AnalysisResult:
        """
        Analyze a pricing issue incident.
        
        Compares invoice amount against linked sales order to detect overcharges.
        
        Args:
            incident: Incident to analyze
        
        Returns:
            AnalysisResult with decision and reasoning
        """
        try:
            invoice_id = incident.erp_reference
            
            # Fetch invoice data
            invoice_data = self.erp_client.get_invoice(invoice_id)
            if not invoice_data:
                return AnalysisResult(
                    decision="UNDETERMINED",
                    summary="Invoice data not found",
                    details=f"Could not retrieve invoice data for {invoice_id}",
                    conclusion="Manual review required - invoice data unavailable",
                    confidence=0.0
                )
            
            # Get linked sales order (try multiple field names)
            sales_order_id = (
                invoice_data.get("sales_order") or
                invoice_data.get("so_no") or
                invoice_data.get("linked_sales_order")
            )
            if not sales_order_id:
                return AnalysisResult(
                    decision="UNDETERMINED",
                    summary="No linked sales order found",
                    details=f"Invoice {invoice_id} has no linked sales order",
                    conclusion="Cannot determine pricing variance without sales order",
                    confidence=0.3
                )
            
            # Fetch sales order data
            sales_order_data = self.erp_client.get_sales_order(sales_order_id)
            if not sales_order_data:
                return AnalysisResult(
                    decision="UNDETERMINED",
                    summary="Sales order data not found",
                    details=f"Could not retrieve sales order {sales_order_id}",
                    conclusion="Manual review required - sales order data unavailable",
                    confidence=0.0
                )
            
            # Extract amounts
            invoice_amount = float(invoice_data.get("total_amount", 0))
            expected_amount = float(sales_order_data.get("expected_amount", 0))
            currency = invoice_data.get("currency", "USD")
            
            # Calculate variance
            difference = invoice_amount - expected_amount
            percentage_variance = (difference / expected_amount * 100) if expected_amount > 0 else 0
            
            # Decision logic: 20% threshold
            threshold = 20.0
            if abs(percentage_variance) <= threshold:
                decision = "APPROVED_WITH_RISK"
            else:
                decision = "REJECTED"
            
            # Build response
            summary = f"Invoice variance: {percentage_variance:+.1f}% vs. expected amount"
            details = (
                f"Invoice ID: {invoice_id}\n"
                f"Sales Order ID: {sales_order_id}\n"
                f"Expected amount: {currency} {expected_amount:,.2f}\n"
                f"Invoice amount: {currency} {invoice_amount:,.2f}\n"
                f"Difference: {currency} {difference:+,.2f}\n"
                f"Variance percentage: {percentage_variance:+.1f}%\n"
                f"Threshold: ±{threshold}%\n"
                f"Invoice Status: {invoice_data.get('status', 'Unknown')}\n"
                f"Order Status: {sales_order_data.get('status', 'Unknown')}"
            )
            conclusion = (
                f"Decision: {decision}. Invoice shows a {abs(percentage_variance):.1f}% variance "
                f"({'positive' if difference > 0 else 'negative'}) against the sales order amount. "
                f"Variance is {'within' if abs(percentage_variance) <= threshold else 'outside'} "
                f"the acceptable threshold of ±{threshold}%. "
                f"{'Risk is acceptable with review.' if decision == 'APPROVED_WITH_RISK' else 'Variance exceeds acceptable limits.'}"
            )
            
            return AnalysisResult(
                decision=decision,
                summary=summary,
                details=details,
                conclusion=conclusion,
                confidence=0.95
            )
        
        except Exception as e:
            return AnalysisResult(
                decision="UNDETERMINED",
                summary=f"Analysis error: {str(e)}",
                details=f"Error analyzing pricing issue: {str(e)}",
                conclusion="Manual review required due to analysis error",
                confidence=0.0
            )


class DuplicateInvoiceAnalyzer:
    """Analyzer for Duplicate_Invoice incident type."""
    
    def __init__(self, erp_client: BaseERPNextClient):
        """Initialize with ERP client."""
        self.erp_client = erp_client
    
    def analyze(self, incident: Incident) -> AnalysisResult:
        """
        Analyze a duplicate invoice incident.
        
        Checks for duplicate invoices based on amount, vendor, and date.
        
        Args:
            incident: Incident to analyze
        
        Returns:
            AnalysisResult with decision and reasoning
        """
        try:
            invoice_id = incident.erp_reference
            
            # Fetch invoice data
            invoice_data = self.erp_client.get_invoice(invoice_id)
            if not invoice_data:
                return AnalysisResult(
                    decision="UNDETERMINED",
                    summary="Invoice data not found",
                    details=f"Could not retrieve invoice {invoice_id}",
                    conclusion="Manual review required - invoice data unavailable",
                    confidence=0.0
                )
            
            # Extract key fields for duplicate detection
            invoice_amount = invoice_data.get("total_amount", 0)
            vendor_name = invoice_data.get("vendor_name", "Unknown")
            posting_date = invoice_data.get("posting_date", "Unknown")
            
            # In production, would query for duplicates in ERP
            # For now, return undetermined - AI would handle this
            return AnalysisResult(
                decision="UNDETERMINED",
                summary="Duplicate detection requires AI analysis",
                details=(
                    f"Invoice: {invoice_id}\n"
                    f"Amount: {invoice_amount}\n"
                    f"Vendor: {vendor_name}\n"
                    f"Date: {posting_date}"
                ),
                conclusion="Insufficient rule data for duplicate detection. AI analysis recommended.",
                confidence=0.5
            )
        
        except Exception as e:
            return AnalysisResult(
                decision="UNDETERMINED",
                summary=f"Analysis error: {str(e)}",
                details=f"Error analyzing duplicate invoice: {str(e)}",
                conclusion="Manual review required due to analysis error",
                confidence=0.0
            )


class DeliveryBillingMismatchAnalyzer:
    """Analyzer for Delivery_or_Billing_Mismatch incident type."""
    
    def __init__(self, erp_client: BaseERPNextClient):
        """Initialize with ERP client."""
        self.erp_client = erp_client
    
    def analyze(self, incident: Incident) -> AnalysisResult:
        """
        Analyze a delivery/billing mismatch incident.
        
        Compares delivery status and billing status in sales order.
        
        Args:
            incident: Incident to analyze
        
        Returns:
            AnalysisResult with decision and reasoning
        """
        try:
            invoice_id = incident.erp_reference
            
            # Fetch invoice data
            invoice_data = self.erp_client.get_invoice(invoice_id)
            if not invoice_data:
                return AnalysisResult(
                    decision="UNDETERMINED",
                    summary="Invoice data not found",
                    details=f"Could not retrieve invoice {invoice_id}",
                    conclusion="Manual review required - invoice data unavailable",
                    confidence=0.0
                )
            
            # Get linked sales order (try multiple field names)
            sales_order_id = (
                invoice_data.get("sales_order") or
                invoice_data.get("so_no") or
                invoice_data.get("linked_sales_order")
            )
            if not sales_order_id:
                return AnalysisResult(
                    decision="UNDETERMINED",
                    summary="No linked sales order found",
                    details=f"Invoice {invoice_id} has no linked sales order",
                    conclusion="Cannot assess delivery/billing mismatch without sales order",
                    confidence=0.3
                )
            
            # Fetch sales order data
            sales_order_data = self.erp_client.get_sales_order(sales_order_id)
            if not sales_order_data:
                return AnalysisResult(
                    decision="UNDETERMINED",
                    summary="Sales order data not found",
                    details=f"Could not retrieve sales order {sales_order_id}",
                    conclusion="Manual review required - sales order data unavailable",
                    confidence=0.0
                )
            
            # Extract delivery and billing status
            delivery_status = sales_order_data.get("delivery_status", "Unknown")
            billing_status = sales_order_data.get("billing_status", "Unknown")
            
            # Simple mismatch detection
            is_mismatch = delivery_status != billing_status
            
            if is_mismatch:
                decision = "REJECTED"
            else:
                decision = "APPROVED_WITH_RISK"
            
            summary = f"Delivery status ({delivery_status}) vs Billing status ({billing_status})"
            details = (
                f"Sales Order: {sales_order_id}\n"
                f"Invoice: {invoice_id}\n"
                f"Delivery Status: {delivery_status}\n"
                f"Billing Status: {billing_status}\n"
                f"Mismatch Detected: {'Yes' if is_mismatch else 'No'}"
            )
            conclusion = (
                f"Decision: {decision}. "
                f"The sales order shows delivery status '{delivery_status}' "
                f"and billing status '{billing_status}'. "
                f"{'These statuses do not match, indicating a mismatch.' if is_mismatch else 'Statuses are aligned.'} "
                f"Manual verification recommended."
            )
            
            return AnalysisResult(
                decision=decision,
                summary=summary,
                details=details,
                conclusion=conclusion,
                confidence=0.85
            )
        
        except Exception as e:
            return AnalysisResult(
                decision="UNDETERMINED",
                summary=f"Analysis error: {str(e)}",
                details=f"Error analyzing delivery/billing mismatch: {str(e)}",
                conclusion="Manual review required due to analysis error",
                confidence=0.0
            )


class IncidentAnalyzerFactory:
    """Factory for creating appropriate incident analyzer based on type."""
    
    _ANALYZERS = {
        "Pricing_Issue": PricingIssueAnalyzer,
        "Duplicate_Invoice": DuplicateInvoiceAnalyzer,
        "Delivery_or_Billing_Mismatch": DeliveryBillingMismatchAnalyzer,
    }
    
    @classmethod
    def get_analyzer(cls, incident_type: str, erp_client: BaseERPNextClient):
        """
        Get analyzer for incident type.
        
        Args:
            incident_type: Type of incident
            erp_client: ERP client instance
        
        Returns:
            Analyzer instance or None if type not found
        """
        analyzer_class = cls._ANALYZERS.get(incident_type)
        if analyzer_class:
            return analyzer_class(erp_client)
        return None
