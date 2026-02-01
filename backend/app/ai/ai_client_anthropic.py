"""
Anthropic Claude AI client for real API calls.

This module provides a production-ready implementation that calls the Anthropic
Claude API directly, with proper error handling, logging, and response parsing.

CRITICAL: This client makes REAL HTTP requests to Anthropic servers.
- Requires CLAUDE_API_KEY environment variable
- Incurs API costs per token
- Raises exceptions on API failures (no fallback)
"""

import os
import re
import json
import logging
import requests
from typing import Dict, Any
from app.ai.ai_client_base import AIClientBase

logger = logging.getLogger(__name__)


class AIClientAnthropic(AIClientBase):
    """
    Real Anthropic Claude API client.
    
    Makes direct HTTPS calls to Anthropic API endpoint.
    Returns structured incident analysis responses.
    """
    #This is the URL to which your code sends an HTTP request to “talk” to Claude.
    API_ENDPOINT = "https://api.anthropic.com/v1/messages"
    API_VERSION = "2023-06-01"
    DEFAULT_MODEL = "claude-sonnet-4-20250514"
    
    def __init__(self):
        """Initialize Anthropic client with API key from environment."""
        self.api_key = os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "CLAUDE_API_KEY environment variable not set. "
                "Cannot initialize Anthropic Claude client."
            )
        
        self.api_key = self.api_key.strip()
        
        # Model name from environment variable (required for flexibility)
        self.model = os.getenv("CLAUDE_MODEL", self.DEFAULT_MODEL).strip()
        
        logger.info(
            f"Anthropic Claude client initialized with model: {self.model} "
            f"(API version: {self.API_VERSION})"
        )
    
    def is_available(self) -> bool:
        """Check if Claude API is available."""
        return bool(self.api_key)
    
    def analyze(self, prompt: str) -> Dict[str, Any]:
        """
        Send prompt to Claude API and get structured analysis response.
        
        Args:
            prompt: Analysis prompt containing incident context and ERP data
        
        Returns:
            Parsed AI response with required fields:
            {
                "root_cause": str,
                "recommended_actions": list,
                "customer_message": str,
                "confidence_score": float,
                "replay_summary": str,
                "replay_details": str,
                "replay_conclusion": str
            }
        
        Raises:
            RuntimeError: If API call fails or response is invalid
            ValueError: If response cannot be parsed as JSON
        """
        logger.info("Calling Anthropic Claude API for incident analysis")
        logger.debug(f"Model: {self.model}, API Version: {self.API_VERSION}")
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": self.API_VERSION,
            "content-type": "application/json"
        }
        
        request_body = {
            "model": self.model,
            "max_tokens": 2048,
            "system": (
                "You are a backend service. "
                "You MUST return VALID JSON ONLY. "
                "Do not use markdown. "
                "Do not add explanations. "
                "The response MUST start with '{' and end with '}'. "
                "If you cannot comply, return exactly: {\"error\":\"INVALID_OUTPUT\"}"
            ),
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        
        try:
            logger.debug(f"Sending request to {self.API_ENDPOINT}")
            response = requests.post(
                self.API_ENDPOINT,
                headers=headers,
                json=request_body,
                timeout=30
            )
            
            # Log API call for verification in Anthropic Console
            logger.info(
                f"Anthropic API call executed: "
                f"HTTP {response.status_code}, "
                f"model={self.model}"
            )
            
            if response.status_code != 200:
                error_detail = response.text
                logger.error(
                    f"Anthropic API error: {response.status_code} - {error_detail}"
                )
                raise RuntimeError(
                    f"Anthropic API returned {response.status_code}: {error_detail}"
                )
            
            api_response = response.json()
            logger.debug(f"Anthropic API response received: {api_response}")
            
            # Extract content from Claude response
            if "content" not in api_response or not api_response["content"]:
                raise ValueError("Anthropic API returned empty content")
            
            # Get the first content block (text)
            content_block = api_response["content"][0]
            if content_block.get("type") != "text":
                raise ValueError(
                    f"Unexpected content type: {content_block.get('type')}"
                )
            
            response_text = content_block.get("text", "")
            logger.debug(f"Claude response text: {response_text[:200]}...")
            logger.info(f"Full Claude response: {response_text}")  # Log full response for debugging
            
            # Parse Claude's JSON response
            parsed_response = self._parse_claude_response(response_text)
            
            logger.info(
                f"Anthropic analysis complete: "
                f"confidence={parsed_response.get('confidence_score', 'N/A')}"
            )
            
            return parsed_response
        
        except requests.exceptions.Timeout:
            logger.error("Anthropic API request timeout (30s)")
            raise RuntimeError("Anthropic API timeout: request exceeded 30 seconds")
        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Anthropic API connection error: {e}")
            raise RuntimeError(f"Anthropic API connection failed: {e}")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Anthropic API request error: {e}")
            raise RuntimeError(f"Anthropic API request error: {e}")
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Anthropic API response as JSON: {e}")
            raise ValueError(f"Anthropic API response is not valid JSON: {e}")
    
    def _parse_claude_response(self, response_text: str) -> Dict[str, Any]:
        response_text = response_text.strip()

        # 1️⃣ ניסיון JSON מלא
        try:
            parsed = json.loads(response_text)
            return self._normalize_response(parsed)
        except json.JSONDecodeError:
            pass

        # 2️⃣ חילוץ JSON מתוך טקסט
        match = re.search(r"\{[\s\S]*\}", response_text)
        if match:
            try:
                parsed = json.loads(match.group())
                return self._normalize_response(parsed)
            except json.JSONDecodeError:
                pass

        logger.error(f"Could not parse Claude response: {response_text[:500]}")
        raise ValueError(
            "Could not extract valid JSON from Claude response"
        )
    
    def _normalize_response(self, parsed: Dict[str, Any]) -> Dict[str, Any]:

        def safe_str(value) -> str:
            if value is None:
                return ""
            if isinstance(value, (dict, list)):
                return json.dumps(value, ensure_ascii=False)
            return str(value)

        # Support multiple field naming conventions:
        # 1. Old: replay_summary, replay_details, replay_conclusion
        # 2. Intermediate: summary, details, conclusion
        # 3. New generic prompt: root_cause, difference_breakdown, recommended_resolution
        
        replay_summary = safe_str(
            parsed.get("replay_summary") 
            or parsed.get("summary") 
            or parsed.get("root_cause")
            or ""
        )
        
        replay_details = safe_str(
            parsed.get("replay_details") 
            or parsed.get("details") 
            or parsed.get("difference_breakdown")
            or ""
        )
        
        replay_conclusion = safe_str(
            parsed.get("replay_conclusion") 
            or parsed.get("conclusion") 
            or parsed.get("recommended_resolution")
            or ""
        )

        confidence = parsed.get("confidence_score") or parsed.get("confidence") or 0.5
        try:
            confidence = float(confidence)
            confidence = max(0.0, min(1.0, confidence))
        except:
            confidence = 0.5

        # If we still don't have a summary, try to build one from available fields
        if not replay_summary:
            analysis = parsed.get("analysis", "")
            if isinstance(analysis, dict):
                replay_summary = safe_str(analysis.get("summary") or analysis.get("root_cause"))
            else:
                replay_summary = safe_str(analysis)
        
        # If still no summary, build from status
        if not replay_summary:
            status = parsed.get("status", "")
            analysis_text = parsed.get("analysis", "")
            if status or analysis_text:
                replay_summary = f"{status}: {analysis_text}" if status else safe_str(analysis_text)

        normalized = {
            "replay_summary": replay_summary,
            "replay_details": replay_details,
            "replay_conclusion": replay_conclusion,
            "confidence_score": confidence,
        }

        # validation – replay_summary MUST exist
        if not normalized["replay_summary"]:
            # As fallback, create a summary from whatever we got
            parsed_str = json.dumps(parsed, ensure_ascii=False)[:500]
            normalized["replay_summary"] = f"Analysis: {parsed_str}"

        return normalized
