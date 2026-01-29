"""AI client factory - PRODUCTION ONLY.

ARCHITECTURE RULE: ONE AI CLIENT ONLY.
- Returns ONLY AIClientAnthropic when AI_PROVIDER=claude
- No mocks in production paths
- All configuration from .env only
"""

import os
import logging
from typing import Optional
from app.ai.ai_client_base import AIClientBase
from app.ai.ai_client_anthropic import AIClientAnthropic

logger = logging.getLogger(__name__)


def get_ai_client() -> AIClientBase:
    """
    Get Claude AI client for incident analysis.
    
    GUARANTEE: 
    - If AI_ENABLED=true, returns initialized AIClientAnthropic
    - All config from environment variables
    - Raises RuntimeError if configuration invalid
    
    Returns:
        AIClientAnthropic instance
    
    Raises:
        RuntimeError: If CLAUDE_API_KEY not set or client init fails
    """
    ai_enabled = os.getenv("AI_ENABLED", "").strip().lower() in ("true", "1", "yes", "on")
    ai_provider = os.getenv("AI_PROVIDER", "").strip().lower()
    
    logger.info(
        f"AI Factory: AI_ENABLED={ai_enabled}, AI_PROVIDER={ai_provider}"
    )
    
    if not ai_enabled:
        raise RuntimeError("AI_ENABLED must be true to use get_ai_client()")
    
    if ai_provider != "claude":
        raise RuntimeError(
            f"Only AI_PROVIDER=claude is supported. Got: {ai_provider}"
        )
    
    claude_key = os.getenv("CLAUDE_API_KEY", "").strip()
    if not claude_key:
        raise RuntimeError(
            "CLAUDE_API_KEY environment variable not set"
        )
    
    logger.info("Initializing Anthropic Claude client")
    try:
        client = AIClientAnthropic()
        logger.info(f"Claude client initialized: model={client.model}")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Claude client: {e}")
        raise RuntimeError(f"Failed to initialize Claude client: {e}") from e

