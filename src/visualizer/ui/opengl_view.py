import sys
import os
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import QTimer
from PySide6.QtGui import QMouseEvent

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from visualizer.core.io.obj_loader import OBJData
from visualizer.core.math.vector3 import Vector3

class OpenGL3DView(QOpenGLWidget):
    def __init__(self):
        super().__init__()

        # Camera control
        self.camera_distance = 8.0
        self.camera_rotation_x = 20.0
        self.camera_rotation_y = 45.0
        self.last_mouse_pos = None

        # Data to render
        self.original_obj = None
        self.rotated_obj = None
        self.rotation_axis = Vector3(0, 0, 1) # Rotasi default pada sumbu Z
        self.rotation_angle = 0.0

        # Rendering flags
        self.show_axes = True
        self.show_rotation_axis = True
        self.show_original = True
        self.show_rotated = True

        # Timer for animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16) # 60 FPS
    
    def initializeGL(self):
        # Enable depth testing
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        
        # Enable Lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)  

        # Background color
        glClearColor(0.05, 0.05, 0.15, 1.0)

        # Light setup
        light_position = [10.0, 10.0, 10.0, 1.0]
        light_ambient = [0.3, 0.3, 0.3, 1.0]
        light_diffuse = [0.8, 0.8, 0.8, 1.0]

        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)

        # Enable blending for transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def resizeGL(self, width, height):
        if height == 0:
            height = 1

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Set perspective projection
        aspect_ratio = width / height
        gluPerspective(45.0, aspect_ratio, 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Apply camera transformations
        glTranslatef(0.0, 0.0, -self.camera_distance)
        glRotatef(self.camera_rotation_x, 1.0, 0.0, 0.0)
        glRotatef(self.camera_rotation_y, 0.0, 1.0, 0.0)

        # Draw scene elements
        if self.show_axes:
            self.draw_coordinate_axes()
        
        if self.show_rotation_axis and self.rotation_axis.magnitude() > 0:
            self.draw_rotation_axis()
        
        if self.show_original and self.original_obj:
            self.draw_original_object()
        
        if self.show_rotated and self.rotated_obj:
            self.draw_rotated_object()
        
        # Draw angle label
        if self.rotation_angle != 0 and self.show_rotation_axis:
            self.draw_angle_label()
    
    def draw_coordinate_axes(self):
        glDisable(GL_LIGHTING)
        glLineWidth(4.0)

        axis_length = 3.0

        glBegin(GL_LINES)

        # X Axis (Red)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(axis_length, 0.0, 0.0)

        # Y Axis (Green)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, axis_length, 0.0)

        # Z Axis (Blue)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, axis_length)

        glEnd()

        # Draw axis labels
        self.draw_axis_labels(axis_length)

        glEnable(GL_LIGHTING)
        glLineWidth(1.0)
    
    def draw_axis_labels(self, axis_length):
        label_offset = axis_length * 0.3
        label_size = 0.2

        # X label
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINES)
        glVertex3f(label_offset - label_size, label_size, 0)
        glVertex3f(label_offset + label_size, -label_size, 0)
        glVertex3f(label_offset - label_size, -label_size, 0)
        glVertex3f(label_offset + label_size, label_size, 0)
        glEnd()

        # Y label
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_LINES)
        glVertex3f(0, label_offset, 0)
        glVertex3f(-label_size, label_offset + label_size, 0)
        glVertex3f(0, label_offset, 0)
        glVertex3f(label_size, label_offset + label_size, 0)
        glVertex3f(0, label_offset, 0)
        glVertex3f(0, label_offset - label_size, 0)
        glEnd()

        # Z label
        glColor3f(0.0, 0.0, 1.0)
        glBegin(GL_LINES)
        glVertex3f(-label_size, label_size, label_offset)
        glVertex3f(label_size, label_size, label_offset)
        glVertex3f(label_size, label_size, label_offset)
        glVertex3f(-label_size, -label_size, label_offset)
        glVertex3f(-label_size, -label_size, label_offset)
        glVertex3f(label_size, -label_size, label_offset)
        glEnd()
    
    def draw_arrow_head(self, x, y, z, direction):
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 1.0, 0.0)
        glPointSize(8.0)

        glBegin(GL_POINTS)
        glVertex3f(x, y, z)
        glEnd()

        glEnable(GL_LIGHTING)
        glPointSize(1.0)
    
    def draw_rotation_axis(self):
        if self.rotation_axis.magnitude() == 0:
            return
        
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 1.0, 0.0)  # Rotation axis color
        glLineWidth(6.0)
        
        # Normalize and scale axis
        axis = self.rotation_axis.normalize()
        scale = 5.0
        
        glBegin(GL_LINES)
        glVertex3f(-axis.x * scale, -axis.y * scale, -axis.z * scale)
        glVertex3f(axis.x * scale, axis.y * scale, axis.z * scale)
        glEnd()
        
        # Draw arrow heads
        self.draw_arrow_head(axis.x * scale, axis.y * scale, axis.z * scale, axis)
        self.draw_arrow_head(-axis.x * scale, -axis.y * scale, -axis.z * scale, axis * -1)
        
        glEnable(GL_LIGHTING)
        glLineWidth(1.0)
    
    def draw_original_object(self):
        if not self.original_obj or not self.original_obj.faces:
            return

        glDisable(GL_LIGHTING)
        glColor4f(0.2, 0.5, 1.0, 0.8) # Original object color
        glLineWidth(2.0)

        for face in self.original_obj.faces:
            glBegin(GL_LINE_LOOP)
            for vertex_index in face.vertex_indices:
                if vertex_index < len(self.original_obj.vertices):
                    v = self.original_obj.vertices[vertex_index]
                    glVertex3f(v.x, v.y, v.z)
            glEnd()
        
        glPointSize(1.0)
    
    def draw_rotated_object(self):
        if not self.rotated_obj or not self.rotated_obj.faces:
            return

        glEnable(GL_LIGHTING)
        glColor4f(1.0, 0.3, 0.2, 0.8) # Rotated object color

        for face in self.rotated_obj.faces:
            if len(face.vertex_indices) >= 3:
                self.calculate_and_set_normal(face)
                
                glBegin(GL_POLYGON)
                for vertex_index in face.vertex_indices:
                    if vertex_index < len(self.rotated_obj.vertices):
                        v = self.rotated_obj.vertices[vertex_index]
                        glVertex3f(v.x, v.y, v.z)
                glEnd()
    
    def calculate_and_set_normal(self, face):
        if len(face.vertex_indices) < 3:
            return
        
        vertices = self.rotated_obj.vertices
        
        # Get first three vertices
        v0_idx = face.vertex_indices[0]
        v1_idx = face.vertex_indices[1]
        v2_idx = face.vertex_indices[2]
        
        if (v0_idx < len(vertices) and v1_idx < len(vertices) and v2_idx < len(vertices)):
            v0 = vertices[v0_idx]
            v1 = vertices[v1_idx]
            v2 = vertices[v2_idx]
            
            # Calculate two edge vectors
            edge1 = Vector3(v1.x - v0.x, v1.y - v0.y, v1.z - v0.z)
            edge2 = Vector3(v2.x - v0.x, v2.y - v0.y, v2.z - v0.z)
            
            # Cross product for normal
            normal = edge1.cross(edge2).normalize()
            glNormal3f(normal.x, normal.y, normal.z)
    
    def draw_angle_label(self):
        if self.rotation_angle == 0:
            return
        
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 1.0, 1.0)  # White
        
        # Simple angle indicator
        axis = self.rotation_axis.normalize()
        radius = 1.5
        
        glLineWidth(2.0)
        glBegin(GL_LINE_STRIP)
        
        # Draw a small arc to indicate rotation
        for i in range(0, int(abs(self.rotation_angle/10)) + 1):
            angle_rad = math.radians(i * 10)
            x = radius * math.cos(angle_rad)
            y = radius * math.sin(angle_rad)
            glVertex3f(x, y, 0)
        
        glEnd()
        
        glEnable(GL_LIGHTING)
        glLineWidth(1.0)
    
    def mousePressEvent(self, event: QMouseEvent):
        self.last_mouse_pos = event.pos()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.last_mouse_pos:
            dx = event.x() - self.last_mouse_pos.x()
            dy = event.y() - self.last_mouse_pos.y()
            
            # Update camera rotation
            self.camera_rotation_y += dx * 0.5
            self.camera_rotation_x += dy * 0.5
            
            # Clamp vertical rotation
            self.camera_rotation_x = max(-90, min(90, self.camera_rotation_x))
            
            self.last_mouse_pos = event.pos()
            self.update()
    
    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        zoom_factor = 0.9 if delta > 0 else 1.1
        
        self.camera_distance *= zoom_factor
        
        # Limit zoom range
        self.camera_distance = max(2.0, min(50.0, self.camera_distance))
        
        self.update()
    
    # Public methods for updating display data
    def set_original_object(self, obj_data: OBJData):
        """Set original object to display"""
        self.original_obj = obj_data
        self.update()
    
    def set_rotated_object(self, obj_data: OBJData):
        """Set rotated object to display"""
        self.rotated_obj = obj_data
        self.update()
    
    def set_rotation_info(self, axis: Vector3, angle: float):
        """Set rotation axis and angle for display"""
        self.rotation_axis = axis
        self.rotation_angle = angle
        self.update()
    
    def clear_rotated_object(self):
        """Clear rotated object (for reset)"""
        self.rotated_obj = None
        self.rotation_angle = 0.0
        self.update()
    
    def toggle_axes(self):
        """Toggle coordinate axes visibility"""
        self.show_axes = not self.show_axes
        self.update()
    
    def toggle_rotation_axis(self):
        """Toggle rotation axis visibility"""
        self.show_rotation_axis = not self.show_rotation_axis
        self.update()
    
    def reset_camera(self):
        """Reset camera to default position"""
        self.camera_distance = 8.0
        self.camera_rotation_x = 20.0
        self.camera_rotation_y = 45.0
        self.update()
