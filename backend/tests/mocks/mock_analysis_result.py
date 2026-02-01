def get_successful_analysis_result():
    """
    Mock AI / analysis output (normalized).
    """
    return {
        "replay_summary": (
            "Invoice total is higher than sales order due to an additional "
            "freight charge of 2000 ILS applied at invoice level."
        ),
        "replay_details": (
            "Sales Order subtotal: 10000 ILS\n"
            "Invoice subtotal: 10000 ILS\n"
            "Additional charge: Freight and Forwarding Charges - 2000 ILS\n"
            "Final invoice total: 12000 ILS"
        ),
        "replay_conclusion": (
            "Remove or correct the freight charge if it was not agreed "
            "in the original sales order."
        ),
        "confidence_score": 0.95,
        "analysis_source": "AI"
    }


def get_failed_analysis_result():
    """
    Mock AI failure scenario.
    """
    return {
        "replay_summary": "AI analysis failed",
        "replay_details": "External AI service unavailable",
        "replay_conclusion": "Manual review required",
        "confidence_score": 0.0,
        "analysis_source": "AI_FAILED"
    }
