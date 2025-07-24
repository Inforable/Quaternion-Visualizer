from pathlib import Path

# Direktori root
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
SRC_DIR = PROJECT_ROOT / "src"
ASSETS_DIR = PROJECT_ROOT / "assets"

# Subdirektori assets
MODELS_DIR = ASSETS_DIR / "models"
ICONS_DIR = ASSETS_DIR / "icons"

# Icon aplikasi
APP_ICON = ICONS_DIR / "app_icon.png"

# Subdirektori src
VISUALIZER_DIR = SRC_DIR / "visualizer"

# Subdirektori visualizer
CONFIG_DIR = VISUALIZER_DIR / "config"
CORE_DIR = VISUALIZER_DIR / "core"
RENDERING_DIR = VISUALIZER_DIR / "rendering"
UI_DIR = VISUALIZER_DIR / "ui"

# Subdirektori ui
STYLES_DIR = UI_DIR / "styles"
COMPONENTS_DIR = UI_DIR / "components"
WIDGETS_DIR = UI_DIR / "widgets"
WINDOWS_DIR = UI_DIR / "windows"

# Subdirektori rendering
OPENGL_DIR = RENDERING_DIR / "opengl"
CUSTOM_DIR = RENDERING_DIR / "custom"