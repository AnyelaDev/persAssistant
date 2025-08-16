"""
AI Service Configuration

Handles environment variables, API keys, and service settings for AI integration.
"""

import os
from pathlib import Path
from typing import Optional

# Ensure environment variables are loaded
try:
    from dotenv import load_dotenv
    
    # Look for .env file in project root
    env_path = Path(__file__).parent.parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
except ImportError:
    pass  # dotenv not available


class AIConfig:
    """Configuration management for AI services."""
    
    def __init__(self):
        """Initialize AI configuration from environment variables."""
        # API Keys
        self.hf_api_key = os.getenv("HF_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        
        # Service Settings
        self.timeout = int(os.getenv("AI_SERVICE_TIMEOUT", "30"))
        self.max_retries = int(os.getenv("AI_MAX_RETRIES", "2"))
        self.fallback_enabled = os.getenv("AI_FALLBACK_ENABLED", "true").lower() == "true"
        
        # HuggingFace Configuration
        self.hf_base_url = "https://api-inference.huggingface.co/models/"
        self.hf_model = "mistralai/Mistral-7B-Instruct-v0.2"
        
        # Retry Configuration
        self.retry_delay = 2  # seconds between retries
        self.exponential_backoff = True
    
    @property
    def has_hf_key(self) -> bool:
        """Check if HuggingFace API key is available."""
        return bool(self.hf_api_key and self.hf_api_key.strip())
    
    @property 
    def has_openai_key(self) -> bool:
        """Check if OpenAI API key is available."""
        return bool(self.openai_api_key and self.openai_api_key.strip())
    
    @property
    def has_anthropic_key(self) -> bool:
        """Check if Anthropic API key is available."""
        return bool(self.anthropic_api_key and self.anthropic_api_key.strip())
    
    @property
    def primary_service(self) -> str:
        """Get the primary AI service to use based on available keys."""
        if self.has_hf_key:
            return "huggingface"
        elif self.has_openai_key:
            return "openai"
        elif self.has_anthropic_key:
            return "anthropic"
        else:
            return "fallback"
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a specific service."""
        service_keys = {
            "huggingface": self.hf_api_key,
            "openai": self.openai_api_key,
            "anthropic": self.anthropic_api_key
        }
        return service_keys.get(service.lower())
    
    def validate_configuration(self) -> tuple[bool, str]:
        """
        Validate AI configuration.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not any([self.has_hf_key, self.has_openai_key, self.has_anthropic_key]):
            if not self.fallback_enabled:
                return False, "No AI service keys configured and fallback is disabled"
            else:
                return True, "Using fallback mode - basic grooming only"
        
        if self.timeout <= 0:
            return False, "AI service timeout must be greater than 0"
        
        if self.max_retries < 0:
            return False, "Max retries must be >= 0"
        
        return True, "Configuration valid"