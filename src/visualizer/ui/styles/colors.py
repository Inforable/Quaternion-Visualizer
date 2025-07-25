class UIColors:
    # Warna background utama
    BACKGROUND_DARK = "#1e1e1e" # Utama
    BACKGROUND_MEDIUM = "#2b2b2b" # Panel
    BACKGROUND_LIGHT = "#3a3a3a"  # Grup

    # Warna panel dan kontainer
    PANEL_BACKGROUND = "#2b2b2b" # Panel kontrol di kiri
    GROUP_BACKGROUND = "#3a3a3a" # Group box
    INPUT_BACKGROUND = "#1e1e1e" # Input field

    # Warna teks
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#cccccc"
    TEXT_DISABLED = "#666666"
    TEXT_ON_PRIMARY = "#ffffff"

    # Warna tombol
    PRIMARY_BLUE = "#2196F3"
    PRIMARY_BLUE_HOVER = "#1976D2"
    PRIMARY_BLUE_PRESSED = "#0D47A1"

    # Warna highlight
    ACCENT_BLUE = "#4FC3F7" # Judul dari section
    ACCENT_GREEN = "#4CAF50" # Success
    ACCENT_RED = "#F44336" # Error

    # Warna peringatan
    WARNING_ORANGE = "#FF9800"
    WARNING_ORANGE_HOVER = "#F57C00"
    WARNING_ORANGE_PRESSED = "#E65100"

    # Warna tombol sekunder
    BUTTON_SECONDARY = "#4a4a4a"
    BUTTON_SECONDARY_HOVER = "#5a5a5a"
    BUTTON_SECONDARY_PRESSED = "#3a3a3a"
    BUTTON_DISABLED = "#2a2a2a"

    # Warna border dan outline
    BORDER_COLOR = "#555555" # Default
    BORDER_HOVER = "#777777" # Hover

    # Warna scrollbar
    SCROLLBAR_BACKGROUND = "#2b2b2b" # Background
    SCROLLBAR_HANDLE = "#555555" # Handle
    SCROLLBAR_HANDLE_HOVER = "#666666" # Handle saat hover

class VisualizationColors:
    # Warna sumbu koordinat
    X_AXIS = (1.0, 0.0, 0.0) # Red
    Y_AXIS = (0.0, 1.0, 0.0) # Green
    Z_AXIS = (0.0, 0.0, 1.0) # Blue

    # Warna objek 3D
    ORIGINAL_OBJECT = (0.4, 0.6, 1.0) # Light Blue
    ROTATED_OBJECT = (1.0, 0.4, 0.4)  # Light Red
    WIREFRAME = (1.0, 1.0, 1.0)       # White

    # Warna metode rotasi
    QUATERNION = (1.0, 1.0, 0.0) # Yellow
    EULER = (1.0, 0.0, 1.0) # Magenta
    TAIT_BRYAN = (0.0, 1.0, 1.0) # Cyan
    EXPONENTIAL = (1.0, 0.65, 0.0) # Orange

    # Warna background renderer
    OPENGL_BACKGROUND = (0.1, 0.1, 0.1, 1.0) # Dark Gray untuk OpenGL
    CUSTOM_BACKGROUND = (0.12, 0.12, 0.12, 1.0) # Light Gray untuk Custom

def hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

def rgb_to_hex(rgb_color: tuple) -> str:
    return '#' + ''.join(f'{int(c * 255):02x}' for c in rgb_color)

def get_method_color(method_name: str) -> tuple[float, float, float]:
    method_colors = {
        "Quaternion": VisualizationColors.QUATERNION,
        "Euler Angle": VisualizationColors.EULER,
        "Tait-Bryan": VisualizationColors.TAIT_BRYAN,
        "Exponential Map": VisualizationColors.EXPONENTIAL
    }
    return method_colors.get(method_name, (1.0, 1.0, 1.0))  # Default