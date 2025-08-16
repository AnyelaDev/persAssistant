"""
Color Palette for Personal Assistant Application

Centralized color definitions for consistent theming and easy customization.
Colors are defined with semantic names and include accessibility-compliant combinations.
"""


class ColorPalette:
    """Centralized color palette for the personal assistant application."""
    
    # Primary Colors - Lighter, more readable backgrounds
    BACKGROUND_PRIMARY = (0.95, 0.95, 0.95, 1)  # Very light gray
    BACKGROUND_SECONDARY = (0.98, 0.98, 0.98, 1)  # Almost white
    
    # Text Colors - High contrast for readability
    TEXT_PRIMARY = (0.05, 0.05, 0.05, 1)  # Almost black for maximum contrast
    TEXT_SECONDARY = (0.2, 0.2, 0.2, 1)  # Dark gray for good contrast
    TEXT_MUTED = (0.4, 0.4, 0.4, 1)  # Medium gray
    
    # Button Colors - Lighter, more accessible versions
    BUTTON_PRIMARY = (0.85, 0.92, 0.85, 1)  # Light green
    BUTTON_SECONDARY = (0.85, 0.92, 0.92, 1)  # Light cyan
    BUTTON_TERTIARY = (0.85, 0.88, 0.95, 1)  # Light blue
    BUTTON_NEUTRAL = (0.92, 0.92, 0.92, 1)  # Light gray
    
    # Legacy color mappings for backward compatibility
    # These map the old hardcoded colors to new semantic colors
    LEGACY_DARK_TEXT = TEXT_PRIMARY  # (0.2, 0.2, 0.2, 1) -> darker text
    LEGACY_MEDIUM_TEXT = TEXT_SECONDARY  # (0.4, 0.4, 0.4, 1) -> medium text
    LEGACY_GREEN_BUTTON = BUTTON_PRIMARY  # (0.8, 0.9, 0.7, 1) -> light green
    LEGACY_CYAN_BUTTON = BUTTON_SECONDARY  # (0.7, 0.9, 0.8, 1) -> light cyan  
    LEGACY_BLUE_BUTTON = BUTTON_TERTIARY  # (0.7, 0.8, 0.9, 1) -> light blue
    LEGACY_GRAY_BACKGROUND = BACKGROUND_PRIMARY  # (0.9, 0.9, 0.9, 1) -> light gray
    
    # Accent Colors for special elements
    ACCENT_BLUE = (0.3, 0.7, 0.9, 1)  # Brighter blue for highlights
    
    @classmethod
    def get_color(cls, color_name: str) -> tuple:
        """
        Get a color by name with fallback to a default color.
        
        Args:
            color_name: Name of the color attribute
            
        Returns:
            RGBA tuple representing the color
        """
        return getattr(cls, color_name.upper(), cls.BACKGROUND_PRIMARY)