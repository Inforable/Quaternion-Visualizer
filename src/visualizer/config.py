from pathlib import Path
from typing import Tuple, List

# Application Information
APP_NAME = "Quaternion Visualizer"
APP_DESCRIPTION = "3D Rotation Visualizer using Quaternions"

# Paths Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
MODELS_DIR = ASSETS_DIR / "models"
ICONS_DIR = ASSETS_DIR / "icons"
STYLES_DIR = ASSETS_DIR / "styles"

# Window Configuration
DEFAULT_WINDOW_SIZE: Tuple[int, int] = (1400, 900)
MIN_WINDOW_SIZE: Tuple[int, int] = (1000, 700)
CONTROL_PANEL_WIDTH: int = 300
INFO_PANEL_WIDTH: int = 0

# Format Configuration
SUPPORTED_3D_FORMATS: List[str] = [".obj"]

# 3D Rendering Configuration
DEFAULT_CAMERA_DISTANCE: float = 8.0
DEFAULT_CAMERA_ROTATION_X: float = 25.0
DEFAULT_CAMERA_ROTATION_Y: float = 0.0
TARGET_FPS: int = 60
ENABLE_VSYNC: bool = True

# Rotation Defaults
DEFAULT_ROTATION_AXIS: Tuple[float, float, float] = (0.0, 0.0, 1.0)  # Z-axis
DEFAULT_ROTATION_ANGLE: float = 45.0  # degrees
AXIS_RANGE: Tuple[float, float] = (-10.0, 10.0)
ANGLE_RANGE: Tuple[float, float] = (-360.0, 360.0)

# Theme Configuration
DEFAULT_THEME: str = "dark"

# Material Design Colors
class Colors:
    # Primary Colors
    PRIMARY = "#1976D2"
    PRIMARY_LIGHT = "#42A5F5"
    PRIMARY_DARK = "#0D47A1"
    
    # Secondary Colors  
    SECONDARY = "#00BCD4"
    SECONDARY_LIGHT = "#4DD0E1"
    SECONDARY_DARK = "#0097A7"
    
    # Background Colors
    BACKGROUND_DARK = "#121212"
    BACKGROUND_LIGHT = "#FFFFFF"
    SURFACE_DARK = "#1E1E1E"
    SURFACE_LIGHT = "#F5F5F5"
    
    # Text Colors
    TEXT_PRIMARY_DARK = "#FFFFFF"
    TEXT_PRIMARY_LIGHT = "#000000"
    TEXT_SECONDARY_DARK = "#B3B3B3"
    TEXT_SECONDARY_LIGHT = "#666666"
    
    # Status Colors
    SUCCESS = "#4CAF50"
    WARNING = "#FF9800"
    ERROR = "#F44336"
    INFO = "#2196F3"

# Performance Configuration
RENDER_QUALITY: str = "high"
ENABLE_ANTI_ALIASING: bool = True
ENABLE_SHADOWS: bool = True
ENABLE_WIREFRAME_SMOOTHING: bool = True