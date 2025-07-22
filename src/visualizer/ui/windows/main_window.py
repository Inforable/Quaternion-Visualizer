"""
Main application window for Quaternion Visualizer.
Implements complete GUI with all required controls and visualization.
"""

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


class MainWindow(QMainWindow):
    """Main application window with complete quaternion visualization interface."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        # Data storage
        self.current_obj_data: Optional[OBJData] = None
        self.rotated_obj_data: Optional[OBJData] = None
        self.obj_loader = OBJLoader()
        
        # UI References
        self.opengl_view: Optional[OpenGLView] = None
        self.output_text: Optional[QTextEdit] = None
        
        # Rotation controls
        self.axis_x_spin: Optional[QDoubleSpinBox] = None
        self.axis_y_spin: Optional[QDoubleSpinBox] = None  
        self.axis_z_spin: Optional[QDoubleSpinBox] = None
        self.angle_spin: Optional[QDoubleSpinBox] = None
        
        # Initialize UI
        self.init_ui()
    
    def init_ui(self):
        """Initialize the complete user interface."""
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
        """Create compact control panel with all rotation controls."""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        panel.setMaximumWidth(300)
        panel.setMinimumWidth(250)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(4)
        layout.setContentsMargins(6, 6, 6, 6)
        
        # Controls section header
        controls_title = QLabel("Controls")
        controls_title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        controls_title.setStyleSheet("color: #1976D2; border-bottom: 1px solid #1976D2; padding-bottom: 1px; margin-bottom: 1px;")
        layout.addWidget(controls_title)
        
        # File operations group
        file_group = QGroupBox("File Operations")
        file_group.setFont(QFont("Arial", 9))
        file_group.setStyleSheet("QGroupBox { margin-top: 2px; }")
        file_layout = QVBoxLayout(file_group)
        file_layout.setContentsMargins(3, 3, 3, 3)
        file_layout.setSpacing(1)
        
        self.load_button = QPushButton("Load OBJ File")
        self.load_button.clicked.connect(self.load_obj_file)
        self.load_button.setStyleSheet("QPushButton { padding: 3px; font-size: 10px; max-height: 20px; }")
        file_layout.addWidget(self.load_button)
        
        layout.addWidget(file_group)
        
        # Rotation parameters group
        rotation_group = QGroupBox("Rotation Parameters")
        rotation_group.setFont(QFont("Arial", 9))
        rotation_group.setStyleSheet("QGroupBox { margin-top: 2px; }")
        rotation_layout = QGridLayout(rotation_group)
        rotation_layout.setContentsMargins(3, 3, 3, 3)
        rotation_layout.setSpacing(1)
        rotation_layout.setVerticalSpacing(1)
        rotation_layout.setHorizontalSpacing(2)
        
        # Axis controls header
        axis_label = QLabel("Rotation Axis:")
        axis_label.setFont(QFont("Arial", 9))
        rotation_layout.addWidget(axis_label, 0, 0, 1, 2)
        
        # X axis control
        x_label = QLabel("X:")
        x_label.setFont(QFont("Arial", 8))
        rotation_layout.addWidget(x_label, 1, 0)
        self.axis_x_spin = QDoubleSpinBox()
        self.axis_x_spin.setRange(-10.0, 10.0)
        self.axis_x_spin.setValue(DEFAULT_ROTATION_AXIS[0])
        self.axis_x_spin.setSingleStep(0.1)
        self.axis_x_spin.setDecimals(2)
        self.axis_x_spin.setMaximumHeight(18)
        self.axis_x_spin.setStyleSheet("QDoubleSpinBox { font-size: 8px; }")
        self.axis_x_spin.valueChanged.connect(self.update_rotation_preview)
        rotation_layout.addWidget(self.axis_x_spin, 1, 1)
        
        # Y axis control
        y_label = QLabel("Y:")
        y_label.setFont(QFont("Arial", 8))
        rotation_layout.addWidget(y_label, 2, 0)
        self.axis_y_spin = QDoubleSpinBox()
        self.axis_y_spin.setRange(-10.0, 10.0)
        self.axis_y_spin.setValue(DEFAULT_ROTATION_AXIS[1])
        self.axis_y_spin.setSingleStep(0.1)
        self.axis_y_spin.setDecimals(2)
        self.axis_y_spin.setMaximumHeight(18)
        self.axis_y_spin.setStyleSheet("QDoubleSpinBox { font-size: 8px; }")
        self.axis_y_spin.valueChanged.connect(self.update_rotation_preview)
        rotation_layout.addWidget(self.axis_y_spin, 2, 1)
        
        # Z axis control
        z_label = QLabel("Z:")
        z_label.setFont(QFont("Arial", 8))
        rotation_layout.addWidget(z_label, 3, 0)
        self.axis_z_spin = QDoubleSpinBox()
        self.axis_z_spin.setRange(-10.0, 10.0)
        self.axis_z_spin.setValue(DEFAULT_ROTATION_AXIS[2])
        self.axis_z_spin.setSingleStep(0.1)
        self.axis_z_spin.setDecimals(2)
        self.axis_z_spin.setMaximumHeight(18)
        self.axis_z_spin.setStyleSheet("QDoubleSpinBox { font-size: 8px; }")
        self.axis_z_spin.valueChanged.connect(self.update_rotation_preview)
        rotation_layout.addWidget(self.axis_z_spin, 3, 1)
        
        # Angle control
        angle_label = QLabel("Angle (degrees):")
        angle_label.setFont(QFont("Arial", 8))
        rotation_layout.addWidget(angle_label, 4, 0)
        self.angle_spin = QDoubleSpinBox()
        self.angle_spin.setRange(-360.0, 360.0)
        self.angle_spin.setValue(DEFAULT_ROTATION_ANGLE)
        self.angle_spin.setSingleStep(1.0)
        self.angle_spin.setDecimals(1)
        self.angle_spin.setMaximumHeight(18)
        self.angle_spin.setStyleSheet("QDoubleSpinBox { font-size: 8px; }")
        self.angle_spin.valueChanged.connect(self.update_rotation_preview)
        rotation_layout.addWidget(self.angle_spin, 4, 1)
        
        layout.addWidget(rotation_group)
        
        # Action buttons group
        actions_group = QGroupBox("Actions")
        actions_group.setFont(QFont("Arial", 9))
        actions_group.setStyleSheet("QGroupBox { margin-top: 2px; }")
        actions_layout = QVBoxLayout(actions_group)
        actions_layout.setContentsMargins(3, 3, 3, 3)
        actions_layout.setSpacing(1)
        
        self.apply_button = QPushButton("Apply Rotation")
        self.apply_button.clicked.connect(self.apply_rotation)
        self.apply_button.setStyleSheet("""
            QPushButton { 
                padding: 3px; 
                font-size: 10px; 
                background-color: #1976D2; 
                color: white; 
                border-radius: 2px;
                max-height: 20px;
            }
        """)
        actions_layout.addWidget(self.apply_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_view)
        self.reset_button.setStyleSheet("""
            QPushButton { 
                padding: 3px; 
                font-size: 10px; 
                border-radius: 2px;
                max-height: 20px;
            }
        """)
        actions_layout.addWidget(self.reset_button)
        
        layout.addWidget(actions_group)
        
        # Object information section
        info_title = QLabel("Object Information")
        info_title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        info_title.setStyleSheet("color: #1976D2; border-bottom: 1px solid #1976D2; padding-bottom: 1px; margin-top: 2px;")
        layout.addWidget(info_title)
        
        # Output text area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Consolas", 7))
        self.output_text.setMaximumHeight(200)
        self.output_text.setMinimumHeight(150)
        self.output_text.setStyleSheet("""
            QTextEdit { 
                background-color: #2C2C2C; 
                color: #FFFFFF; 
                border: 1px solid #555; 
                padding: 2px;
            }
        """)
        self.output_text.setText("No model loaded. Please select an OBJ file to begin.")
        layout.addWidget(self.output_text)
        
        return panel
    
    def create_viewer_panel(self) -> QWidget:
        """Create the 3D visualization panel."""
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
    
    def update_rotation_preview(self):
        """Update rotation visualization when parameters change."""
        if self.opengl_view:
            axis = Vector3(
                self.axis_x_spin.value(),
                self.axis_y_spin.value(),
                self.axis_z_spin.value()
            )
            angle = self.angle_spin.value()
            
            # Update rotation axis and angle visualization
            self.opengl_view.set_rotation_parameters(axis, angle)
    
    def load_obj_file(self):
        """Load an OBJ file using file dialog."""
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
    
    def apply_rotation(self):
        """Apply quaternion rotation to the current object."""
        try:
            if not self.current_obj_data:
                QMessageBox.warning(self, "No Data", "Please load an OBJ file first.")
                return
            
            axis = Vector3(
                self.axis_x_spin.value(),
                self.axis_y_spin.value(), 
                self.axis_z_spin.value()
            )
            angle = self.angle_spin.value()
            
            is_valid, error_msg = RotationEngine.validate_rotation_parameters(axis, angle)
            if not is_valid:
                QMessageBox.warning(self, "Invalid Parameters", error_msg)
                return
            
            self.rotated_obj_data = RotationEngine.rotate_obj_data(
                self.current_obj_data, axis, angle
            )
            
            if self.opengl_view:
                self.opengl_view.set_obj_data(self.current_obj_data, self.rotated_obj_data)
                self.opengl_view.set_rotation_parameters(axis, angle)
            
            rotation_info = RotationEngine.get_rotation_info(axis, angle)
            self.output_text.append(f"\n{rotation_info}")
            self.output_text.append("Rotation applied successfully!")
            
        except Exception as e:
            error_msg = f"Error applying rotation: {e}"
            self.output_text.append(f"\n{error_msg}")
            QMessageBox.critical(self, "Rotation Error", error_msg)
    
    def reset_view(self):
        """Reset the view to original state."""
        try:
            self.axis_x_spin.setValue(DEFAULT_ROTATION_AXIS[0])
            self.axis_y_spin.setValue(DEFAULT_ROTATION_AXIS[1])
            self.axis_z_spin.setValue(DEFAULT_ROTATION_AXIS[2])
            self.angle_spin.setValue(DEFAULT_ROTATION_ANGLE)
            
            self.rotated_obj_data = None
            
            if self.opengl_view:
                self.opengl_view.set_obj_data(self.current_obj_data, None)
                self.update_rotation_preview()
            
            self.output_text.append("\nView reset to original state")
            
        except Exception as e:
            error_msg = f"Error resetting view: {e}"
            self.output_text.append(f"\n{error_msg}")
    
    def display_obj_data(self):
        """Display information about the loaded OBJ data.""" 
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
            self.output_text.setText(f"Error displaying object data: {e}")