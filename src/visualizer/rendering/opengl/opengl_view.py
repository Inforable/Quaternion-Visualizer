from PySide6.QtCore import QTimer, Qt
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtGui import QMouseEvent, QWheelEvent, QPainter, QFont, QColor

import OpenGL.GL as gl
import OpenGL.GLU as glu
import math

from typing import Optional
from ...core.io.obj_loader import OBJData
from ...core.math.vector3 import Vector3
from ...core.math.rotation_factory import RotationMethod

class OpenGLView(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 3D scene data
        self.original_obj: OBJData = None
        self.rotated_obj: OBJData = None

        # Rotation parameters
        self.rotation_axis: Vector3 = Vector3(0, 0, 1)
        self.rotation_angle: float = 0.0
        
        # Camera controls
        self.camera_distance = 8.0
        self.camera_rotation_x = 20.0
        self.camera_rotation_y = 45.0
        
        # Mouse interaction
        self.last_mouse_pos = None
        
        # Cached matrices untuk stable labels
        self.cached_modelview = None
        self.cached_projection = None
        self.cached_viewport = None
        
        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(33)  # 30 FPS untuk stability
        
        # Text rendering setup
        self.label_font = QFont("Arial", 14, QFont.Weight.Bold)
        self.degree_font = QFont("Arial", 16, QFont.Weight.Bold)
        
        # Label caching untuk prevent flickering
        self.label_cache = {}
        self.cache_counter = 0
    
    def set_obj_data(self, original_obj: OBJData, rotated_obj: OBJData = None):
        self.original_obj = original_obj
        self.rotated_obj = rotated_obj
        self.update()

    def set_rotation_parameters(self, axis: Vector3, angle: float):
        if axis and axis.magnitude() > 0:
            self.rotation_axis = axis.normalize()
        else:
            self.rotation_axis = Vector3(0, 0, 1)
        self.rotation_angle = angle
        self.update()
    
    def reset_camera(self):
        self.camera_distance = 8.0
        self.camera_rotation_x = 20.0
        self.camera_rotation_y = 45.0
        self.update()
    
    def initializeGL(self):
        gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_LINE_SMOOTH)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        
        # Setup lighting
        light_pos = [5.0, 5.0, 5.0, 1.0]
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, light_pos)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        
        gl.glEnable(gl.GL_COLOR_MATERIAL)
    
    def resizeGL(self, width, height):
        if height == 0:
            height = 1
        
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(45.0, width / height, 0.1, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        
        self.label_cache.clear()
    
    def paintGL(self):
        try:
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            gl.glLoadIdentity()
            
            # Setup camera
            self.setup_camera()
            
            # Cache matrices setelah camera setup
            self.cache_matrices()
            
            # Draw coordinate axes
            self.draw_coordinate_axes()
            
            # Draw rotation visualization
            self.draw_rotation_visualization()
            
            # Draw objects
            self.draw_objects()
                
        except Exception as e:
            print(f"OpenGL Error: {e}")
    
    def paintEvent(self, event):
        super().paintEvent(event)
        # Only draw labels if matrices are cached
        if self.cached_modelview is not None:
            self.draw_2d_labels()
    
    def cache_matrices(self):
        try:
            self.cached_modelview = gl.glGetDoublev(gl.GL_MODELVIEW_MATRIX)
            self.cached_projection = gl.glGetDoublev(gl.GL_PROJECTION_MATRIX)
            self.cached_viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
        except Exception as e:
            print(f"Error caching matrices: {e}")
    
    def setup_camera(self):
        glu.gluLookAt(
            self.camera_distance * math.cos(math.radians(self.camera_rotation_y)) * math.cos(math.radians(self.camera_rotation_x)),
            self.camera_distance * math.sin(math.radians(self.camera_rotation_x)),
            self.camera_distance * math.sin(math.radians(self.camera_rotation_y)) * math.cos(math.radians(self.camera_rotation_x)),
            0.0, 0.0, 0.0,
            0.0, 1.0, 0.0
        )
    
    def draw_coordinate_axes(self):
        try:
            gl.glDisable(gl.GL_LIGHTING)
            gl.glLineWidth(3.0)
            axis_length = 4.0

            # Draw axes
            gl.glBegin(gl.GL_LINES)

            # X axis
            gl.glColor3f(1.0, 0.0, 0.0)
            gl.glVertex3f(0.0, 0.0, 0.0)
            gl.glVertex3f(axis_length, 0.0, 0.0)
            
            # Y axis
            gl.glColor3f(0.0, 1.0, 0.0)
            gl.glVertex3f(0.0, 0.0, 0.0)
            gl.glVertex3f(0.0, axis_length, 0.0)
            
            # Z axix
            gl.glColor3f(0.0, 0.0, 1.0)
            gl.glVertex3f(0.0, 0.0, 0.0)
            gl.glVertex3f(0.0, 0.0, axis_length)
            gl.glEnd()

            arrow_size = 0.3
            self.draw_arrow_head(Vector3(axis_length, 0, 0), Vector3(1, 0, 0), arrow_size, (1.0, 0.0, 0.0))
            self.draw_arrow_head(Vector3(0, axis_length, 0), Vector3(0, 1, 0), arrow_size, (0.0, 1.0, 0.0))
            self.draw_arrow_head(Vector3(0, 0, axis_length), Vector3(0, 0, 1), arrow_size, (0.0, 0.0, 1.0))
            
            gl.glEnable(gl.GL_LIGHTING)
            gl.glLineWidth(1.0)
            
        except Exception as e:
            print(f"Error drawing axes: {e}")
    
    def draw_arrow_head(self, position: Vector3, direction: Vector3, size: float, color: tuple):
        try:
            gl.glColor3f(*color)
            gl.glLineWidth(3.0)
            gl.glPushMatrix()
            gl.glTranslatef(position.x, position.y, position.z)
            
            # Simple arrow head using lines
            gl.glBegin(gl.GL_LINES)
            back_x = -direction.x * size * 2
            back_y = -direction.y * size * 2
            back_z = -direction.z * size * 2
            
            # Create perpendicular vectors for arrow head
            if abs(direction.z) < 0.9:
                perp1 = Vector3(0, 0, 1).cross(direction).normalize()
            else:
                perp1 = Vector3(1, 0, 0).cross(direction).normalize()
            perp2 = direction.cross(perp1).normalize()
            
            # Draw arrow lines
            gl.glVertex3f(0, 0, 0)
            gl.glVertex3f(back_x + perp1.x * size, back_y + perp1.y * size, back_z + perp1.z * size)
            gl.glVertex3f(0, 0, 0)
            gl.glVertex3f(back_x - perp1.x * size, back_y - perp1.y * size, back_z - perp1.z * size)
            gl.glVertex3f(0, 0, 0)
            gl.glVertex3f(back_x + perp2.x * size, back_y + perp2.y * size, back_z + perp2.z * size)
            gl.glVertex3f(0, 0, 0)
            gl.glVertex3f(back_x - perp2.x * size, back_y - perp2.y * size, back_z - perp2.z * size)
            gl.glEnd()
            
            gl.glPopMatrix()
            gl.glLineWidth(1.0)
        except Exception as e:
            print(f"Error drawing arrow head: {e}")
    
    def draw_rotation_visualization(self):
        if abs(self.rotation_angle) < 0.1:
            return
            
        try:
            gl.glDisable(gl.GL_LIGHTING)

            # Draw rotation axis
            axis = self.rotation_axis.normalize()
            axis_length = 5.0
            
            gl.glColor3f(1.0, 1.0, 0.0)
            gl.glLineWidth(5.0)
            gl.glBegin(gl.GL_LINES)
            gl.glVertex3f(-axis.x * axis_length, -axis.y * axis_length, -axis.z * axis_length)
            gl.glVertex3f(axis.x * axis_length, axis.y * axis_length, axis.z * axis_length)
            gl.glEnd()
            
            # Draw angle arc
            self.draw_angle_arc()
            
            gl.glEnable(gl.GL_LIGHTING)
            gl.glLineWidth(1.0)
            
        except Exception as e:
            print(f"Error drawing rotation: {e}")
    
    def draw_angle_arc(self):
        try:
            axis = self.rotation_axis.normalize()
            radius = 2.5

            # Create perpendicular vectors
            if abs(axis.z) < 0.9:
                u = Vector3(0, 0, 1).cross(axis).normalize()
            else:
                u = Vector3(1, 0, 0).cross(axis).normalize()
            v = axis.cross(u).normalize()
            
            # Draw arc
            gl.glColor3f(1.0, 0.6, 0.0)
            gl.glLineWidth(4.0)

            steps = max(16, int(abs(self.rotation_angle) / 2))
            gl.glBegin(gl.GL_LINE_STRIP)
            for i in range(steps + 1):
                angle_progress = (i / steps) * math.radians(abs(self.rotation_angle))
                if self.rotation_angle < 0:
                    angle_progress = -angle_progress
                
                cos_a = math.cos(angle_progress)
                sin_a = math.sin(angle_progress)
                
                point_x = (u.x * cos_a + v.x * sin_a) * radius
                point_y = (u.y * cos_a + v.y * sin_a) * radius
                point_z = (u.z * cos_a + v.z * sin_a) * radius
                
                gl.glVertex3f(point_x, point_y, point_z)
            gl.glEnd()
            
            gl.glLineWidth(1.0)
            
        except Exception as e:
            print(f"Error drawing angle arc: {e}")
    
    def draw_objects(self):
        try:
            if self.original_obj:
                gl.glPushMatrix()
                gl.glTranslatef(-3.0, 0.0, 0.0)
                self.draw_obj(self.original_obj, color=(0.3, 0.5, 1.0))
                gl.glPopMatrix()
            
            if self.rotated_obj:
                gl.glPushMatrix()
                gl.glTranslatef(3.0, 0.0, 0.0)
                self.draw_obj(self.rotated_obj, color=(1.0, 0.3, 0.3))
                gl.glPopMatrix()
        except Exception as e:
            print(f"Error drawing objects: {e}")
    
    def draw_obj(self, obj_data: OBJData, color=(1.0, 1.0, 1.0)):
        if not obj_data or not obj_data.vertices or not obj_data.faces:
            return
        
        try:
            # Set material
            gl.glMaterialfv(gl.GL_FRONT, gl.GL_AMBIENT_AND_DIFFUSE, [*color, 1.0])
            
            # Draw faces
            for face in obj_data.faces:
                if len(face.vertex_indices) >= 3:
                    gl.glBegin(gl.GL_POLYGON)
                    for vertex_index in face.vertex_indices:
                        if 0 <= vertex_index < len(obj_data.vertices):
                            vertex = obj_data.vertices[vertex_index]
                            gl.glVertex3f(vertex.x, vertex.y, vertex.z)
                    gl.glEnd()
            
            # Draw wireframe
            gl.glDisable(gl.GL_LIGHTING)
            gl.glColor3f(*[c * 0.8 for c in color])
            gl.glLineWidth(1.5)
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
            
            for face in obj_data.faces:
                if len(face.vertex_indices) >= 3:
                    gl.glBegin(gl.GL_POLYGON)
                    for vertex_index in face.vertex_indices:
                        if 0 <= vertex_index < len(obj_data.vertices):
                            vertex = obj_data.vertices[vertex_index]
                            gl.glVertex3f(vertex.x, vertex.y, vertex.z)
                    gl.glEnd()
            
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
            gl.glEnable(gl.GL_LIGHTING)
            gl.glLineWidth(1.0)
            
        except Exception as e:
            print(f"Error drawing object: {e}")
    
    def draw_2d_labels(self):
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
            
            axis_length = 4.0
            label_position_ratio = 0.7
            
            label_distance = axis_length * label_position_ratio
            
            positions = self.get_axis_line_positions(label_distance)
            
            if positions['x_pos']:
                painter.setFont(self.label_font)
                painter.setPen(QColor(255, 80, 80))
                painter.drawText(int(positions['x_pos'][0] + 2), int(positions['x_pos'][1] - 5), "i")
            
            if positions['y_pos']:
                painter.setFont(self.label_font)
                painter.setPen(QColor(80, 255, 80))
                painter.drawText(int(positions['y_pos'][0] + 2), int(positions['y_pos'][1] - 5), "j")
            
            if positions['z_pos']:
                painter.setFont(self.label_font)
                painter.setPen(QColor(80, 80, 255))
                painter.drawText(int(positions['z_pos'][0] + 2), int(positions['z_pos'][1] - 5), "k")
            
            self.draw_stable_degree_label(painter)
            
            painter.end()
            
        except Exception as e:
            print(f"Error drawing 2D labels: {e}")
    
    def get_axis_line_positions(self, label_distance):
        positions = {
            'x_pos': None,
            'y_pos': None,
            'z_pos': None
        }
        
        try:
            cache_key = f"axis_{self.camera_rotation_x:.0f}_{self.camera_rotation_y:.0f}_{self.camera_distance:.0f}"
            
            # Check cache dengan reduced frequency untuk stability
            if cache_key in self.label_cache and self.cache_counter % 5 == 0:
                return self.label_cache[cache_key]
            
            # X-axis label position
            positions['x_pos'] = self.stable_world_to_screen(label_distance, 0, 0)
            
            # Y-axis label position 
            positions['y_pos'] = self.stable_world_to_screen(0, label_distance, 0)
            
            # Z-axis label position
            positions['z_pos'] = self.stable_world_to_screen(0, 0, label_distance)
            
            # Cache results
            self.label_cache[cache_key] = positions
            self.cache_counter += 1
            
            # Limit cache size untuk performance
            if len(self.label_cache) > 15:
                keys_to_remove = list(self.label_cache.keys())[:-8]
                for key in keys_to_remove:
                    del self.label_cache[key]
            
            return positions
            
        except Exception as e:
            print(f"Error getting axis line positions: {e}")
            return positions
    
    def draw_stable_degree_label(self, painter):
        if abs(self.rotation_angle) < 0.1:
            return
        
        try:
            axis = self.rotation_axis.normalize()
            
            # Use simpler calculation untuk stability
            if abs(axis.z) < 0.9:
                u = Vector3(0, 0, 1).cross(axis).normalize()
            else:
                u = Vector3(1, 0, 0).cross(axis).normalize()
            
            label_radius = 3.0
            mid_angle = math.radians(self.rotation_angle / 2)
            
            # Simplified position calculation
            mid_x = u.x * math.cos(mid_angle) * label_radius
            mid_y = u.y * math.cos(mid_angle) * label_radius + 0.5
            mid_z = u.z * math.cos(mid_angle) * label_radius
            
            label_screen = self.stable_world_to_screen(mid_x, mid_y, mid_z)
            
            if label_screen and self.is_position_visible(label_screen):
                painter.setFont(self.degree_font)
                painter.setPen(QColor(255, 255, 255))
                
                # Background untuk better visibility
                degree_text = f"{self.rotation_angle:.1f}°"
                text_rect = painter.fontMetrics().boundingRect(degree_text)
                
                # Draw semi-transparent background
                painter.fillRect(
                    int(label_screen[0] + 10),
                    int(label_screen[1] - text_rect.height()),
                    text_rect.width() + 4,
                    text_rect.height() + 2,
                    QColor(0, 0, 0, 128)
                )
                
                painter.drawText(int(label_screen[0] + 12), int(label_screen[1]), degree_text)
            
        except Exception as e:
            print(f"Error drawing stable degree label: {e}")
    
    def stable_world_to_screen(self, x, y, z):
        try:
            if not all([self.cached_modelview is not None, 
                       self.cached_projection is not None, 
                       self.cached_viewport is not None]):
                return None
            
            screen_coords = glu.gluProject(
                x, y, z, 
                self.cached_modelview, 
                self.cached_projection, 
                self.cached_viewport
            )
            
            if screen_coords:
                screen_x = round(screen_coords[0])
                screen_y = round(self.height() - screen_coords[1])
                return (screen_x, screen_y)
            return None
            
        except Exception as e:
            return None
    
    def world_to_screen(self, x, y, z):
        return self.stable_world_to_screen(x, y, z)
    
    def is_position_visible(self, screen_pos):
        if not screen_pos:
            return False
        x, y = screen_pos
        margin = 50
        return -margin <= x <= self.width() + margin and -margin <= y <= self.height() + margin
    
    # Mouse interactions
    def wheelEvent(self, event):
        """Handle mouse wheel for zoom"""
        delta = event.angleDelta().y()
        zoom_factor = 1.1
        
        if delta > 0:
            self.camera_distance /= zoom_factor
        else:
            self.camera_distance *= zoom_factor
        
        self.camera_distance = max(2.0, min(25.0, self.camera_distance))
        
        # Clear cache on camera change
        self.label_cache.clear()
        self.update()
    
    def mousePressEvent(self, event):
        self.last_mouse_pos = event.position()
    
    def mouseMoveEvent(self, event):
        if self.last_mouse_pos and event.buttons():
            dx = event.position().x() - self.last_mouse_pos.x()
            dy = event.position().y() - self.last_mouse_pos.y()
            
            self.camera_rotation_y += dx * 0.5
            self.camera_rotation_x -= dy * 0.5
            
            self.camera_rotation_x = max(-90, min(90, self.camera_rotation_x))
            
            self.last_mouse_pos = event.position()
            
            # Clear cache on camera movement
            self.label_cache.clear()
            self.update()
    
    def mouseReleaseEvent(self, event):
        self.last_mouse_pos = None