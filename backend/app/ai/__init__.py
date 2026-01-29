"""
AI Integration Module

This package provides AI-assisted analysis for financial incidents.
It follows a factory pattern similar to ERP clients for flexibility
and testability.

Components:
- ai_client_base: Abstract base class for AI providers
- ai_client_openai: OpenAI implementation
- ai_client_mock: Mock implementation for testing
- prompt_builder: Constructs detailed analysis prompts
- ai_factory: Factory for AI client selection
"""
