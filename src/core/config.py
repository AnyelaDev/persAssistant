import os
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    
    # Look for .env file in project root
    env_path = Path(__file__).parent.parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded environment variables from {env_path}")
    else:
        print(f".env file not found at {env_path} - using system environment variables")
        
except ImportError:
    print("python-dotenv not installed - using system environment variables only")


class AppConfig:
    APP_TITLE = "Personal Assistance"
    
    @classmethod
    def get_app_title(cls):
        return cls.APP_TITLE
    
    @classmethod
    def set_app_title(cls, title):
        cls.APP_TITLE = title
    
    @classmethod
    def get_ai_enabled(cls) -> bool:
        """Check if AI features are enabled via environment variables."""
        return bool(os.getenv("HF_API_KEY") or 
                   os.getenv("OPENAI_API_KEY") or 
                   os.getenv("ANTHROPIC_API_KEY"))
    
    @classmethod
    def get_debug_mode(cls) -> bool:
        """Check if debug mode is enabled."""
        return os.getenv("DEBUG", "false").lower() in ["true", "1", "yes"]