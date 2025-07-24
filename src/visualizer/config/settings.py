# Informasi aplikasi
APP_NAME = "Quaternion Visualizer"
APP_DESCRIPTION = "Aplikasi visualisasi rotasi 3D menggunakan Quaternion, Euler Angle, Tait-Bryan, dan Exponential Map."

# Seting window
DEFAULT_WINDOW_WIDTH = 1000
DEFAULT_WINDOW_HEIGHT = 600
MIN_WINDOW_WIDTH = 900
MIN_WINDOW_HEIGHT = 550
CONTROL_PANEL_WIDTH = 320

# Setting rendering
DEFAULT_FOV = 60.0 # field of View dalam derajat
DEFAULT_NEAR_PLANE = 0.1 # jarak dari kamera ke objek terdekat
DEFAULT_FAR_PLANE = 100.0 # jarak dari kamera ke objek terjauh
DEFAULT_CAMERA_DISTANCE = 15.0 # jarak kamera dari pusat objek

# Setting default dari rotasi
DEFAULT_ROTATION_AXIS = (0.0, 0.0, 1.0) # sumbu rotasi default, Z-axis
DEFAULT_ROTATION_ANGLE = 0.0
SUPPORTED_ROTATION_METHODS = [
    "Quaternion", 
    "Euler Angle", 
    "Tait-Bryan", 
    "Exponential Map"
]

# Setting file
SUPPORTED_3D_FORMATS = [".obj"]

# Setting font
TITLE_FONT_SIZE = 12
NORMAL_FONT_SIZE = 10
SMALL_FONT_SIZE = 8
FONT_FAMILY = "Arial"
MONOSPACE_FONT_FAMILY = "Courier"

# Setting warna untuk visualisasi
VISUALIZATION_COLORS = {
    # Warna sumbu koordinat
    'X_AXIS': (1.0, 0.0, 0.0),      # Red
    'Y_AXIS': (0.0, 1.0, 0.0),      # Green
    'Z_AXIS': (0.0, 0.0, 1.0),      # Blue

    # Warna objek
    'ORIGINAL_OBJECT': (0.4, 0.6, 1.0),    # Light Blue
    'ROTATED_OBJECT': (1.0, 0.4, 0.4),     # Light Red
    'WIREFRAME': (1.0, 1.0, 1.0),          # White

    # Warna metode rotasi
    'QUATERNION': (1.0, 1.0, 0.0),         # Yellow
    'EULER': (1.0, 0.0, 1.0),              # Magenta
    'TAIT_BRYAN': (0.0, 1.0, 1.0),         # Cyan
    'EXPONENTIAL': (1.0, 0.65, 0.0),       # Orange
    
    # Warna background
    'OPENGL_BACKGROUND': (0.1, 0.1, 0.1, 1.0),     # Dark Gray
    'CUSTOM_BACKGROUND': (0.12, 0.12, 0.12, 1.0),  # Slightly Lighter
}

# Setting animasi
ANIMATION_DURATION_MS = 300 # Dalam milidetik
SMOOTH_ANIMATION = True

# Setting performa
MAX_VERTICES_DISPLAY = 10000 # Limit vertices yang ditampilkan
ENABLE_WIREFRAME_OPTIMIZATION = True

# Setting mouse
MOUSE_ORBIT_SENSITIVITY = 0.5 
MOUSE_ZOOM_SENSITIVITY = 0.1
MOUSE_PAN_SENSITIVITY = 0.01

# Batas kamera
CAMERA_MIN_DISTANCE = 2.0 # Jarak minimum kamera dari objek
CAMERA_MAX_DISTANCE = 50.0 # Jarak maksimum kamera dari objek
CAMERA_MIN_ELEVATION = -90.0 # Elevasi minimum kamera
CAMERA_MAX_ELEVATION = 90.0 # Elevasi maksimum kamera

# Setting lebar garis
COORDINATE_AXIS_WIDTH = 2.0
ROTATION_AXIS_WIDTH = 3.0
WIREFRAME_WIDTH = 1.0

# Setting grid
GRID_SIZE = 10
GRID_SPACING = 1.0
SHOW_GRID_DEFAULT = False