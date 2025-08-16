"""
AI module for Personal Assistant Application

This module provides AI-powered functionality including:
- ToDo list grooming and optimization
- Task clarification and organization
- Intelligent task breakdown
"""

from .grooming_service import GroomingService
from .config import AIConfig

__all__ = ['GroomingService', 'AIConfig']