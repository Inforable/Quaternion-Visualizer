from .settings import *
from .paths import *

__all__ = [
    # Informasi Aplikasi
    'APP_NAME',
    'APP_DESCRIPTION',
    
    # Pengaturan Window
    'DEFAULT_WINDOW_WIDTH',
    'DEFAULT_WINDOW_HEIGHT',
    'MIN_WINDOW_WIDTH',
    'MIN_WINDOW_HEIGHT',
    'CONTROL_PANEL_WIDTH',

    # Pengaturan Rendering
    'DEFAULT_FOV',
    'DEFAULT_NEAR_PLANE',
    'DEFAULT_FAR_PLANE',
    'DEFAULT_CAMERA_DISTANCE',

    # Pengaturan Rotasi
    'DEFAULT_ROTATION_AXIS',
    'DEFAULT_ROTATION_ANGLE',
    'SUPPORTED_ROTATION_METHODS',

    # Pengaturan File
    'SUPPORTED_3D_FORMATS',

    # Pengaturan Font
    'TITLE_FONT_SIZE',
    'NORMAL_FONT_SIZE',
    'SMALL_FONT_SIZE',
    'FONT_FAMILY',
    'MONOSPACE_FONT_FAMILY',

    # Pengaturan Warna
    'VISUALIZATION_COLORS',

    # Pengaturan Animasi
    'ANIMATION_DURATION_MS',
    'SMOOTH_ANIMATION',

    # Pengaturan Kinerja
    'MAX_VERTICES_DISPLAY',
    'ENABLE_WIREFRAME_OPTIMIZATION',

    # Pengaturan Mouse
    'MOUSE_ORBIT_SENSITIVITY',
    'MOUSE_ZOOM_SENSITIVITY',
    'MOUSE_PAN_SENSITIVITY',

    # Batas Kamera
    'CAMERA_MIN_DISTANCE',
    'CAMERA_MAX_DISTANCE',
    'CAMERA_MIN_ELEVATION',
    'CAMERA_MAX_ELEVATION',
    
    # Line widths
    'COORDINATE_AXIS_WIDTH',
    'ROTATION_AXIS_WIDTH',
    'WIREFRAME_WIDTH',

    # Pengaturan Grid
    'GRID_SIZE',
    'GRID_SPACING',
    'SHOW_GRID_DEFAULT',
    
    # Paths
    'PROJECT_ROOT',
    'SRC_DIR',
    'ASSETS_DIR',
    'MODELS_DIR',
    'ICONS_DIR',
    'APP_ICON',
    'VISUALIZER_DIR',
    'CONFIG_DIR',
    'CORE_DIR',
    'RENDERING_DIR',
    'UI_DIR',
    'STYLES_DIR',
    'COMPONENTS_DIR',
    'WIDGETS_DIR',
    'WINDOWS_DIR',
    'OPENGL_DIR',
    'CUSTOM_DIR',
]