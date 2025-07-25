import sys
import os
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QSplitter, QFrame, QLabel, QGroupBox, QPushButton, 
    QTextEdit, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from ...config import APP_NAME
from ...core.io.obj_loader import OBJLoader
from ...core.math.rotation_factory import RotationFactory, RotationMethod
from ...core.math.vector3 import Vector3
from ...rendering.opengl.opengl_view import OpenGLView
from ...rendering.custom.custom_renderer import CustomRenderer
from ..widgets.rotation_method_widget import RotationMethodWidget
from ..styles.theme import DarkTheme
from ..styles.fonts import UIFonts

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.current_obj_data = None
        self.rotated_obj_data = None
        self.current_method = RotationMethod.QUATERNION
        
        self.opengl_view = None
        self.custom_view = None
        self.current_renderer = "opengl"
        
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        self.setWindowTitle(f"{APP_NAME}")
        self.setMinimumSize(1000, 600)
        self.resize(1200, 700)
        
        # Apply theme safely
        try:
            self.setStyleSheet(DarkTheme.get_complete_stylesheet())
        except Exception as e:
            print(f"Warning: Could not apply stylesheet: {e}")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(6)
        main_layout.setContentsMargins(6, 6, 6, 6)
        
        # Left panel for controls
        left_panel = self.create_left_panel()
        
        # Right panel for 3D viewer
        viewer_panel = self.create_viewer_panel()
        
        main_layout.addWidget(left_panel)
        main_layout.addWidget(viewer_panel)
        
        # Set stretch factors
        main_layout.setStretch(0, 0)  # Left panel fixed width
        main_layout.setStretch(1, 1)  # Viewer panel expandable
    
    def create_left_panel(self) -> QWidget:
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        panel.setFixedWidth(320)
        
        try:
            panel.setStyleSheet(DarkTheme.control_panel())
        except Exception as e:
            print(f"Warning: Could not apply panel stylesheet: {e}")
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(8)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Title
        title_label = QLabel(f"{APP_NAME}")
        title_label.setFont(QFont(UIFonts.FAMILY, UIFonts.TITLE_SIZE, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        try:
            title_label.setStyleSheet(DarkTheme.title_label())
        except Exception:
            pass
        layout.addWidget(title_label)
        
        # File operations
        file_group = self.create_file_operations_group()
        layout.addWidget(file_group)
        
        # Rotation configuration
        rotation_group = self.create_rotation_configuration_group()
        layout.addWidget(rotation_group)
        
        # Actions
        actions_group = self.create_actions_group()
        layout.addWidget(actions_group)
        
        # Object info
        info_group = self.create_info_group()
        layout.addWidget(info_group)
        
        layout.addStretch()
        
        return panel
    
    def create_file_operations_group(self) -> QGroupBox:
        file_group = QGroupBox("File Operations")
        file_group.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        try:
            file_group.setStyleSheet(DarkTheme.group_box())
        except Exception:
            pass
        
        file_layout = QVBoxLayout(file_group)
        file_layout.setContentsMargins(8, 15, 8, 8)
        file_layout.setSpacing(4)
        
        self.load_button = QPushButton("Load OBJ File")
        self.load_button.clicked.connect(self.load_obj_file)
        try:
            self.load_button.setStyleSheet(DarkTheme.secondary_button())
        except Exception:
            pass
        file_layout.addWidget(self.load_button)
        
        return file_group
    
    def create_rotation_configuration_group(self) -> QGroupBox:
        rotation_group = QGroupBox("Rotation Configuration")
        rotation_group.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        try:
            rotation_group.setStyleSheet(DarkTheme.group_box())
        except Exception:
            pass
        
        rotation_layout = QVBoxLayout(rotation_group)
        rotation_layout.setContentsMargins(8, 15, 8, 8)
        
        self.rotation_method_widget = RotationMethodWidget()
        rotation_layout.addWidget(self.rotation_method_widget)
        
        return rotation_group
    
    def create_actions_group(self) -> QGroupBox:
        actions_group = QGroupBox("Actions")
        actions_group.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        try:
            actions_group.setStyleSheet(DarkTheme.group_box())
        except Exception:
            pass
        
        actions_layout = QVBoxLayout(actions_group)
        actions_layout.setContentsMargins(8, 15, 8, 8)
        actions_layout.setSpacing(4)
        
        self.apply_button = QPushButton("Apply Rotation")
        self.apply_button.clicked.connect(self.apply_rotation)
        try:
            self.apply_button.setStyleSheet(DarkTheme.primary_button())
        except Exception:
            pass
        actions_layout.addWidget(self.apply_button)
        
        self.toggle_renderer_button = QPushButton("Switch to Custom Renderer")
        self.toggle_renderer_button.clicked.connect(self.toggle_renderer)
        try:
            self.toggle_renderer_button.setStyleSheet(DarkTheme.warning_button())
        except Exception:
            pass
        actions_layout.addWidget(self.toggle_renderer_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_view)
        try:
            self.reset_button.setStyleSheet(DarkTheme.secondary_button())
        except Exception:
            pass
        actions_layout.addWidget(self.reset_button)
        
        return actions_group
    
    def create_info_group(self) -> QGroupBox:
        info_group = QGroupBox("Object Information")
        info_group.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        try:
            info_group.setStyleSheet(DarkTheme.group_box())
        except Exception:
            pass
        
        info_layout = QVBoxLayout(info_group)
        info_layout.setContentsMargins(8, 15, 8, 8)
        
        self.output_text = QTextEdit()
        self.output_text.setMaximumHeight(120)
        self.output_text.setFont(QFont(UIFonts.MONOSPACE_FAMILY, UIFonts.SMALL_SIZE))
        self.output_text.setReadOnly(True)
        try:
            self.output_text.setStyleSheet(DarkTheme.text_edit())
        except Exception:
            pass
        self.output_text.setText("No model loaded. Please select an OBJ file to begin.")
        info_layout.addWidget(self.output_text)
        
        return info_group
        
    def create_viewer_panel(self) -> QWidget:
        self.renderer_container = QWidget()
        renderer_layout = QVBoxLayout(self.renderer_container)
        renderer_layout.setContentsMargins(0, 0, 0, 0)
        renderer_layout.setSpacing(0)
        
        try:
            self.opengl_view = OpenGLView()
            self.custom_view = CustomRenderer()
            
            renderer_layout.addWidget(self.opengl_view)
            renderer_layout.addWidget(self.custom_view)
            
            self.custom_view.hide()
            
        except Exception as e:
            print(f"Error initializing renderers: {e}")
            error_label = QLabel(f"Error initializing 3D renderers: {e}")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            try:
                error_label.setStyleSheet(DarkTheme.label())
            except Exception:
                pass
            renderer_layout.addWidget(error_label)
        
        return self.renderer_container
    
    def setup_connections(self):
        try:
            if hasattr(self, 'rotation_method_widget'):
                if hasattr(self.rotation_method_widget, 'rotation_changed'):
                    self.rotation_method_widget.rotation_changed.connect(self.on_rotation_changed)
                    
        except Exception as e:
            print(f"Warning: Could not setup all connections: {e}")
    
    def on_rotation_changed(self, rotation_obj):
        try:
            if rotation_obj:
                # Extract axis and angle from rotation object
                axis, angle = self.extract_axis_angle(rotation_obj)
                
                # Update visualization in current renderer
                current_renderer = self.get_current_renderer()
                if current_renderer and hasattr(current_renderer, 'set_rotation_parameters'):
                    current_renderer.set_rotation_parameters(axis, angle)
                
                # Update method for visualization data
                self.current_method = self.rotation_method_widget.get_current_method()
                
        except Exception as e:
            print(f"Error handling rotation change: {e}")
    
    def extract_axis_angle(self, rotation_obj):
        try:
            if hasattr(rotation_obj, 'to_axis_angle'):
                return rotation_obj.to_axis_angle()
            
            elif hasattr(rotation_obj, 'get_axis') and hasattr(rotation_obj, 'get_angle'):
                return rotation_obj.get_axis(), rotation_obj.get_angle()
            
            elif hasattr(rotation_obj, 'to_quaternion'):
                quaternion = rotation_obj.to_quaternion()
                if hasattr(quaternion, 'to_axis_angle'):
                    return quaternion.to_axis_angle()
                elif hasattr(quaternion, 'get_axis') and hasattr(quaternion, 'get_angle'):
                    return quaternion.get_axis(), quaternion.get_angle()
            
            elif hasattr(rotation_obj, 'x') and hasattr(rotation_obj, 'y') and hasattr(rotation_obj, 'z'):
                # Use the largest rotation as primary axis
                angles = [rotation_obj.x, rotation_obj.y, rotation_obj.z]
                axes = [Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, 1)]
                max_index = max(range(len(angles)), key=lambda i: abs(angles[i]))
                return axes[max_index], angles[max_index]
            
            elif hasattr(rotation_obj, 'roll') and hasattr(rotation_obj, 'pitch') and hasattr(rotation_obj, 'yaw'):
                # Use yaw as primary (Z-axis rotation)
                return Vector3(0, 0, 1), rotation_obj.yaw
            
            elif hasattr(rotation_obj, 'omega'):
                omega = rotation_obj.omega
                if hasattr(omega, 'magnitude') and omega.magnitude() > 0:
                    axis = omega.normalize()
                    angle = omega.magnitude() * 180.0 / 3.14159265359  # Convert to degrees
                    return axis, angle
            
            # Default fallback
            return Vector3(0, 0, 1), 0.0
            
        except Exception as e:
            print(f"Error extracting axis-angle: {e}")
            return Vector3(0, 0, 1), 0.0
    
    def load_obj_file(self):
        try:
            file_dialog = QFileDialog()
            
            file_path, _ = file_dialog.getOpenFileName(
                self, 
                "Select OBJ File", 
                str(Path.home()), 
                "OBJ Files (*.obj);;All Files (*)"
            )
            
            if file_path:
                self.current_obj_data = OBJLoader.load_obj(file_path)
                self.rotated_obj_data = None
                
                # Update renderers
                if self.opengl_view and hasattr(self.opengl_view, 'set_obj_data'):
                    self.opengl_view.set_obj_data(self.current_obj_data, None)
                if self.custom_view and hasattr(self.custom_view, 'set_obj_data'):
                    self.custom_view.set_obj_data(self.current_obj_data, None)
                
                self.display_obj_data()
                
        except Exception as e:
            error_msg = f"Error loading OBJ file: {e}"
            QMessageBox.critical(self, "Load Error", error_msg)
            self.output_text.setText(error_msg)
    
    def apply_rotation(self):
        try:
            if not self.current_obj_data:
                QMessageBox.warning(self, "No Data", "Please load an OBJ file first.")
                return
            
            # Get rotation from current widget
            rotation_obj = self.rotation_method_widget.get_current_rotation()
            if not rotation_obj:
                QMessageBox.warning(self, "No Rotation", "Please set rotation parameters.")
                return
            
            # Get current method
            method = self.rotation_method_widget.get_current_method()
            
            # Apply rotation using RotationFactory with method parameter
            try:
                self.rotated_obj_data = RotationFactory.rotate_obj_data(
                    self.current_obj_data, rotation_obj, method
                )
            except Exception as e:
                print(f"Warning: RotationFactory.rotate_obj_data failed with method parameter: {e}")
                # Create a simple rotation by converting to quaternion
                if hasattr(rotation_obj, 'to_quaternion'):
                    quaternion = rotation_obj.to_quaternion()
                    # Apply quaternion rotation manually or use a simplified approach
                    self.rotated_obj_data = self.apply_rotation_manually(self.current_obj_data, rotation_obj)
                else:
                    raise e
            
            # Update renderers
            if self.opengl_view and hasattr(self.opengl_view, 'set_obj_data'):
                self.opengl_view.set_obj_data(self.current_obj_data, self.rotated_obj_data)
            if self.custom_view and hasattr(self.custom_view, 'set_obj_data'):
                self.custom_view.set_obj_data(self.current_obj_data, self.rotated_obj_data)
            
            # Update visualization
            axis, angle = self.extract_axis_angle(rotation_obj)
            
            current_renderer = self.get_current_renderer()
            if current_renderer and hasattr(current_renderer, 'set_rotation_parameters'):
                current_renderer.set_rotation_parameters(axis, angle)
            
            # Show rotation info
            try:
                if hasattr(RotationFactory, 'get_rotation_info'):
                    rotation_info = RotationFactory.get_rotation_info(rotation_obj, method)
                    self.output_text.append(f"\n{rotation_info}")
                else:
                    # Simplified rotation info
                    rotation_info = f"Method: {method.value if hasattr(method, 'value') else method}"
                    rotation_info += f"\nAxis: ({axis.x:.3f}, {axis.y:.3f}, {axis.z:.3f})"
                    rotation_info += f"\nAngle: {angle:.2f}°"
                    self.output_text.append(f"\n{rotation_info}")
            except Exception as e:
                self.output_text.append(f"\nRotation applied (info error: {e})")
                
            self.output_text.append("Rotation applied successfully!")
            
        except Exception as e:
            error_msg = f"Error applying rotation: {e}"
            self.output_text.append(f"\n{error_msg}")
            QMessageBox.critical(self, "Rotation Error", error_msg)
    
    def apply_rotation_manually(self, obj_data, rotation_obj):
        try:
            # Create new OBJData
            from ...core.io.obj_loader import OBJData, Vertex
            
            rotated_data = OBJData()
            rotated_data.filename = f"{obj_data.filename}_rotated"
            rotated_data.faces = obj_data.faces.copy()
            
            # Apply rotation to each vertex
            for vertex in obj_data.vertices:
                vector = Vector3(vertex.x, vertex.y, vertex.z)
                
                # Try to rotate using the rotation object
                if hasattr(rotation_obj, 'rotate_vector'):
                    rotated_vector = rotation_obj.rotate_vector(vector)
                else:
                    # Simple identity transformation
                    rotated_vector = vector
                
                rotated_vertex = Vertex(rotated_vector.x, rotated_vector.y, rotated_vector.z)
                rotated_data.vertices.append(rotated_vertex)
            
            return rotated_data
            
        except Exception as e:
            print(f"Error in manual rotation: {e}")
            return obj_data  # Return original if rotation fails
    
    def toggle_renderer(self):
        try:
            if self.current_renderer == "opengl":
                if self.opengl_view:
                    self.opengl_view.hide()
                if self.custom_view:
                    self.custom_view.show()
                self.current_renderer = "custom"
                self.toggle_renderer_button.setText("Switch to OpenGL Renderer")
            else:
                if self.custom_view:
                    self.custom_view.hide()
                if self.opengl_view:
                    self.opengl_view.show()
                self.current_renderer = "opengl"
                self.toggle_renderer_button.setText("Switch to Custom Renderer")
            
            # Update current renderer with existing data
            current_renderer = self.get_current_renderer()
            if current_renderer and hasattr(current_renderer, 'set_obj_data'):
                current_renderer.set_obj_data(self.current_obj_data, self.rotated_obj_data)
                
                rotation_obj = self.rotation_method_widget.get_current_rotation()
                if rotation_obj and hasattr(current_renderer, 'set_rotation_parameters'):
                    axis, angle = self.extract_axis_angle(rotation_obj)
                    current_renderer.set_rotation_parameters(axis, angle)
                
        except Exception as e:
            print(f"Error toggling renderer: {e}")
    
    def get_current_renderer(self):
        if self.current_renderer == "opengl":
            return self.opengl_view
        else:
            return self.custom_view
    
    def reset_view(self):
        try:
            if hasattr(self, 'rotation_method_widget'):
                if hasattr(self.rotation_method_widget, 'reset_to_identity'):
                    self.rotation_method_widget.reset_to_identity()
            
            # Clear rotated object
            self.rotated_obj_data = None
            
            # Reset renderers
            if self.opengl_view:
                if hasattr(self.opengl_view, 'set_obj_data'):
                    self.opengl_view.set_obj_data(self.current_obj_data, None)
                if hasattr(self.opengl_view, 'reset_camera'):
                    self.opengl_view.reset_camera()
                    
            if self.custom_view:
                if hasattr(self.custom_view, 'set_obj_data'):
                    self.custom_view.set_obj_data(self.current_obj_data, None)
                if hasattr(self.custom_view, 'reset_camera'):
                    self.custom_view.reset_camera()
            
            # Reset display
            if self.current_obj_data:
                self.display_obj_data()
            else:
                self.output_text.setText("No model loaded. Please select an OBJ file to begin.")
                
        except Exception as e:
            print(f"Error resetting view: {e}")
    
    def display_obj_data(self):
        try:
            if not self.current_obj_data:
                self.output_text.setText("No model loaded.")
                return
            
            obj_data = self.current_obj_data
            output = f"File: {getattr(obj_data, 'filename', 'Unknown')}\n"
            output += f"Vertices: {len(obj_data.vertices) if obj_data.vertices else 0}\n"
            output += f"Faces: {len(obj_data.faces) if obj_data.faces else 0}\n"
            
            if obj_data.vertices and len(obj_data.vertices) > 0:
                vertices = obj_data.vertices
                try:
                    min_x = min(v.x for v in vertices)
                    max_x = max(v.x for v in vertices)
                    min_y = min(v.y for v in vertices)
                    max_y = max(v.y for v in vertices)
                    min_z = min(v.z for v in vertices)
                    max_z = max(v.z for v in vertices)
                    
                    output += f"\nBounding Box:\n"
                    output += f"X: {min_x:.2f} to {max_x:.2f}\n"
                    output += f"Y: {min_y:.2f} to {max_y:.2f}\n"
                    output += f"Z: {min_z:.2f} to {max_z:.2f}\n"
                except Exception as e:
                    output += f"\nError calculating bounding box: {e}\n"
            
            self.output_text.setText(output)
            
        except Exception as e:
            self.output_text.setText(f"Error displaying object data: {e}")