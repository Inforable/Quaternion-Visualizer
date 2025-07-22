import sys
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QDoubleSpinBox, QTextEdit,
    QFileDialog, QMessageBox, QSplitter, QFrame,
    QGroupBox, QGridLayout, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from ...config import (
    APP_NAME, 
    MODELS_DIR, 
    SUPPORTED_3D_FORMATS,
    DEFAULT_ROTATION_AXIS,
    DEFAULT_ROTATION_ANGLE,
    CONTROL_PANEL_WIDTH
)
from ...core.math import Vector3, Quaternion, RotationEngine
from ...core.io import OBJLoader, OBJData
from ...rendering.opengl.opengl_view import OpenGLView
from ...core.math.rotation_factory import RotationMethod, RotationFactory
from ..widgets.rotation_method_widget import RotationMethodWidget

class MainWindow(QMainWindow):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        # Data storage
        self.current_obj_data: Optional[OBJData] = None
        self.rotated_obj_data: Optional[OBJData] = None
        self.obj_loader = OBJLoader()
        
        # UI References
        self.opengl_view: Optional[OpenGLView] = None
        self.output_text: Optional[QTextEdit] = None

        # rotation method
        self.current_method = RotationMethod.QUATERNION
        self.rotation_method_widget: Optional[RotationMethodWidget] = None
        
        # Initialize UI
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f"{APP_NAME}")
        self.setMinimumSize(900, 550)
        self.resize(1000, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(4)
        main_layout.setContentsMargins(4, 4, 4, 4)
        
        # Title header
        title_label = QLabel(f"{APP_NAME}")
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel { 
                color: #1976D2; 
                padding: 4px;
                border-bottom: 1px solid #1976D2;
                margin-bottom: 2px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f8f8f8, stop:1 #e8e8e8);
            }
        """)
        title_label.setMaximumHeight(26)
        main_layout.addWidget(title_label)
        
        # Content area with splitter
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(content_splitter)
        
        # Create panels
        left_panel = self.create_left_panel()
        viewer_panel = self.create_viewer_panel()
        
        content_splitter.addWidget(left_panel)
        content_splitter.addWidget(viewer_panel)
        
        # Set panel proportions
        content_splitter.setSizes([280, 720])
    
    def create_left_panel(self) -> QWidget:
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        panel.setMaximumWidth(320)
        panel.setMinimumWidth(280)
        panel.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                color: #ffffff;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(8)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Controls section header
        controls_title = QLabel("Controls")
        controls_title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        controls_title.setStyleSheet("""
            QLabel { 
                color: #4FC3F7; 
                border-bottom: 1px solid #4FC3F7; 
                padding-bottom: 3px; 
                margin-bottom: 5px;
                background: transparent;
            }
        """)
        layout.addWidget(controls_title)
        
        # File operations group
        file_group = QGroupBox("File Operations")
        file_group.setFont(QFont("Arial", 9))
        file_group.setStyleSheet("""
            QGroupBox { 
                font-weight: bold;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 4px;
                background-color: #3a3a3a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px 0 4px;
                color: #ffffff;
            }
        """)
        file_layout = QVBoxLayout(file_group)
        file_layout.setContentsMargins(8, 15, 8, 8)
        file_layout.setSpacing(4)
        
        self.load_button = QPushButton("Load OBJ File")
        self.load_button.clicked.connect(self.load_obj_file)
        self.load_button.setStyleSheet("""
            QPushButton { 
                padding: 6px; 
                font-size: 10px; 
                min-height: 24px;
                background-color: #4a4a4a;
                color: #ffffff;
                border: 1px solid #666666;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
                border: 1px solid #777777;
            }
            QPushButton:pressed {
                background-color: #3a3a3a;
            }
        """)
        file_layout.addWidget(self.load_button)
        
        layout.addWidget(file_group)
        
        # Rotation parameters group
        rotation_group = QGroupBox("Rotation Method & Parameters")
        rotation_group.setFont(QFont("Arial", 9))
        rotation_group.setStyleSheet("""
            QGroupBox { 
                font-weight: bold;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 4px;
                background-color: #3a3a3a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px 0 4px;
                color: #ffffff;
            }
        """)
        rotation_layout = QVBoxLayout(rotation_group)
        rotation_layout.setContentsMargins(8, 15, 8, 8)
        rotation_layout.setSpacing(4)
        
        self.rotation_method_widget = RotationMethodWidget()
        self.rotation_method_widget.method_changed.connect(self.on_method_changed)
        rotation_layout.addWidget(self.rotation_method_widget)
        
        layout.addWidget(rotation_group)
        
        # Action buttons group
        actions_group = QGroupBox("Actions")
        actions_group.setFont(QFont("Arial", 9))
        actions_group.setStyleSheet("""
            QGroupBox { 
                font-weight: bold;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 4px;
                background-color: #3a3a3a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px 0 4px;
                color: #ffffff;
            }
        """)
        actions_layout = QVBoxLayout(actions_group)
        actions_layout.setContentsMargins(8, 15, 8, 8)
        actions_layout.setSpacing(6)

        self.apply_button = QPushButton("Apply Rotation")
        self.apply_button.clicked.connect(self.apply_rotation)
        self.apply_button.setStyleSheet("""
            QPushButton { 
                padding: 8px; 
                font-size: 11px; 
                font-weight: bold;
                background-color: #2196F3; 
                color: white; 
                border-radius: 4px;
                min-height: 28px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        actions_layout.addWidget(self.apply_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_view)
        self.reset_button.setStyleSheet("""
            QPushButton { 
                padding: 6px; 
                font-size: 10px; 
                background-color: #4a4a4a;
                color: #ffffff;
                border: 1px solid #666666;
                border-radius: 3px;
                min-height: 24px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
            QPushButton:pressed {
                background-color: #3a3a3a;
            }
        """)
        actions_layout.addWidget(self.reset_button)
        
        layout.addWidget(actions_group)
        
        # Object information section
        info_title = QLabel("Object Information")
        info_title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        info_title.setStyleSheet("""
            QLabel { 
                color: #4FC3F7; 
                border-bottom: 1px solid #4FC3F7; 
                padding-bottom: 3px; 
                margin-top: 8px;
                margin-bottom: 5px;
                background: transparent;
            }
        """)
        layout.addWidget(info_title)
        
        # Output text area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Consolas", 8))
        self.output_text.setMaximumHeight(200)
        self.output_text.setMinimumHeight(150)
        self.output_text.setStyleSheet("""
            QTextEdit { 
                background-color: #1e1e1e; 
                color: #E8E8E8; 
                border: 1px solid #555555; 
                border-radius: 4px;
                padding: 6px;
            }
            QScrollBar:vertical {
                background-color: #2b2b2b;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #555555;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #666666;
            }
        """)
        self.output_text.setText("No model loaded. Please select an OBJ file to begin.")
        layout.addWidget(self.output_text)
        
        return panel
    
    def create_viewer_panel(self) -> QWidget:
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(2, 2, 2, 2)
        
        try:
            self.opengl_view = OpenGLView()
            layout.addWidget(self.opengl_view)
        except ImportError as e:
            placeholder = QLabel(f"3D Viewer\n(OpenGL not available: {e})\n\nEnsure PyOpenGL is installed:\npip install PyOpenGL PyOpenGL-accelerate")
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setStyleSheet("background-color: #2C2C2C; color: white; font-size: 12px; padding: 20px;")
            placeholder.setMinimumHeight(400)
            layout.addWidget(placeholder)
            self.opengl_view = None
        
        return panel
    
    def load_obj_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Load OBJ File",
                str(MODELS_DIR),
                "OBJ Files (*.obj);;All Files (*)"
            )
            
            if not file_path:
                return
            
            self.current_obj_data = self.obj_loader.load_from_file(file_path)
            self.rotated_obj_data = None
            
            self.display_obj_data()
            
            if self.opengl_view:
                self.opengl_view.set_obj_data(self.current_obj_data, None)
                # Update rotation visualization
                self.update_rotation_preview()
            
            self.output_text.append(f"\nSuccessfully loaded: {Path(file_path).name}")
            
        except Exception as e:
            error_msg = f"Error loading file: {e}"
            self.output_text.append(f"\n{error_msg}")
            QMessageBox.critical(self, "Load Error", error_msg)
    
    def on_method_changed(self, method: RotationMethod):
        self.current_method = method
        self.update_rotation_preview()
    
    def update_rotation_preview(self):
        if self.opengl_view and self.rotation_method_widget:
            try:
                rotation_obj = self.rotation_method_widget.get_rotation_object()
                viz_data = RotationFactory.get_visualization_data(rotation_obj, self.current_method)
                self.opengl_view.set_rotation_visualization(viz_data)
            except Exception as e:
                print(f"Error update preview: {e}, {rotation_obj}")

    def apply_rotation(self):
        try:
            if not self.current_obj_data:
                QMessageBox.warning(self, "Tidak ada data", "Tolong muat file OBJ.")
                return
            
            rotation_obj = self.rotation_method_widget.get_rotation_object()
            
            # Terapkan rotasi pada data objek
            self.rotated_obj_data = RotationFactory.rotate_obj_data(
                self.current_obj_data, rotation_obj, self.current_method
            )
            
            if self.opengl_view:
                self.opengl_view.set_obj_data(self.current_obj_data, self.rotated_obj_data)
                
                # Update visualisasi rotasi
                viz_data = RotationFactory.get_visualization_data(rotation_obj, self.current_method)
                self.opengl_view.set_rotation_visualization(viz_data)
            
            # Show informasi rotasi
            rotation_info = RotationFactory.get_rotation_info(rotation_obj, self.current_method)
            self.output_text.append(f"\n{rotation_info}")
            self.output_text.append("Rotation applied successfully!")
            
        except Exception as e:
            error_msg = f"Error applying rotation: {e}"
            self.output_text.append(f"\n{error_msg}")
            QMessageBox.critical(self, "Rotation Error", error_msg)
    
    def reset_view(self):
        try:
            # Reset ke default metode
            self.rotation_method_widget.method_combo.setCurrentIndex(0)  # Quaternion
            
            # Reset kontrol rotasi
            if hasattr(self.rotation_method_widget.quaternion_controls, 'axis_x_spin'):
                self.rotation_method_widget.quaternion_controls.axis_x_spin.setValue(0.0)
                self.rotation_method_widget.quaternion_controls.axis_y_spin.setValue(0.0)
                self.rotation_method_widget.quaternion_controls.axis_z_spin.setValue(1.0)
                self.rotation_method_widget.quaternion_controls.angle_spin.setValue(45.0)
            
            self.rotated_obj_data = None
            
            if self.opengl_view:
                self.opengl_view.set_obj_data(self.current_obj_data, None)
                self.update_rotation_preview()
            
            self.output_text.append("\nView reset to default rotation method and parameters.")
            
        except Exception as e:
            error_msg = f"Error saat set ulang: {e}"
            self.output_text.append(f"\n{error_msg}")
    
    def display_obj_data(self):
        if not self.current_obj_data:
            return
        
        try:
            output = f"File: {self.current_obj_data.filename}\n"
            output += f"Vertices: {len(self.current_obj_data.vertices)} | Faces: {len(self.current_obj_data.faces)}\n"
            
            if self.current_obj_data.vertices:
                output += f"Sample vertices:\n"
                for i, vertex in enumerate(self.current_obj_data.vertices[:3]):
                    output += f"  v{i}: ({vertex.x:.2f}, {vertex.y:.2f}, {vertex.z:.2f})\n"
                
                if len(self.current_obj_data.vertices) > 3:
                    remaining = len(self.current_obj_data.vertices) - 3
                    output += f"  ... +{remaining} more\n"
            
            if self.current_obj_data.faces:
                output += f"Sample faces:\n"
                for i, face in enumerate(self.current_obj_data.faces[:2]):
                    indices_str = ", ".join(str(idx) for idx in face.vertex_indices[:4])
                    if len(face.vertex_indices) > 4:
                        indices_str += "..."
                    output += f"  f{i}: [{indices_str}]\n"
                
                if len(self.current_obj_data.faces) > 2:
                    remaining = len(self.current_obj_data.faces) - 2
                    output += f"  ... +{remaining} more\n"
            
            if self.current_obj_data.vertices:
                vertices = self.current_obj_data.vertices
                min_x = min(v.x for v in vertices)
                max_x = max(v.x for v in vertices)
                min_y = min(v.y for v in vertices)
                max_y = max(v.y for v in vertices)
                min_z = min(v.z for v in vertices)
                max_z = max(v.z for v in vertices)
                
                output += f"\nBounds:\n"
                output += f"X: {min_x:.2f} to {max_x:.2f}\n"
                output += f"Y: {min_y:.2f} to {max_y:.2f}\n"
                output += f"Z: {min_z:.2f} to {max_z:.2f}\n"
            
            self.output_text.setText(output)
            
        except Exception as e:
            self.output_text.setText(f"Error saat menampilkan data objek: {e}")