from PySide6.QtCore import QTimer
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtGui import QMouseEvent, QWheelEvent

import OpenGL.GL as gl
import OpenGL.GLU as glu
import math

from typing import Optional
from ...core.io.obj_loader import OBJData
from ...core.math.vector3 import Vector3

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
        
        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # 60 FPS
        
        # Enable mouse tracking
        self.setMouseTracking(True)
    
    def set_obj_data(self, original_obj: OBJData, rotated_obj: OBJData = None):
        self.original_obj = original_obj
        self.rotated_obj = rotated_obj
        self.update()

    def set_rotation_parameters(self, axis: Vector3, angle: float):
        if axis.magnitude() > 0:
            self.rotation_axis = axis.normalize()
        else:
            self.rotation_axis = Vector3(0, 0, 1)
        self.rotation_angle = angle
        self.update()
    
    def initializeGL(self):
        # Clear error state first
        while gl.glGetError() != gl.GL_NO_ERROR:
            pass
        
        gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthFunc(gl.GL_LESS)
        
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        
        gl.glEnable(gl.GL_LINE_SMOOTH)
        gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)
        
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        
        light_pos = [5.0, 5.0, 5.0, 1.0]
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, light_pos)
        
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT, gl.GL_AMBIENT_AND_DIFFUSE)
    
    def resizeGL(self, width, height):
        if height == 0:
            height = 1
        
        aspect_ratio = width / height
        
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        
        glu.gluPerspective(45.0, aspect_ratio, 0.1, 100.0)
        
        gl.glMatrixMode(gl.GL_MODELVIEW)
    
    def paintGL(self):
        try:
            # Clear any previous errors
            while gl.glGetError() != gl.GL_NO_ERROR:
                pass
            
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            
            # Reset modelview matrix
            gl.glLoadIdentity()
            
            # Setup camera
            glu.gluLookAt(
                self.camera_distance * math.cos(math.radians(self.camera_rotation_y)) * math.cos(math.radians(self.camera_rotation_x)),
                self.camera_distance * math.sin(math.radians(self.camera_rotation_x)),
                self.camera_distance * math.sin(math.radians(self.camera_rotation_y)) * math.cos(math.radians(self.camera_rotation_x)),
                0.0, 0.0, 0.0,
                0.0, 1.0, 0.0
            )
            
            # Draw all components safely
            self.draw_coordinate_axes()
            self.draw_rotation_axis()  
            self.draw_angle_visualization()
            
            # Draw objects
            if self.original_obj:
                gl.glPushMatrix()
                gl.glTranslatef(-2.0, 0.0, 0.0)
                self.draw_obj(self.original_obj, color=(0.3, 0.5, 1.0))
                gl.glPopMatrix()
            
            if self.rotated_obj:
                gl.glPushMatrix()
                gl.glTranslatef(2.0, 0.0, 0.0)
                self.draw_obj(self.rotated_obj, color=(1.0, 0.3, 0.3))
                gl.glPopMatrix()
            
        except Exception as e:
            print(f"OpenGL Error in paintGL: {e}")
    
    def draw_coordinate_axes(self):
        """Draw XYZ coordinate axes safely."""
        try:
            gl.glDisable(gl.GL_LIGHTING)
            gl.glLineWidth(2.0)

            axis_length = 2.0

            # Draw main axes lines
            gl.glBegin(gl.GL_LINES)
            try:
                # X axis (red)
                gl.glColor3f(1.0, 0.0, 0.0)
                gl.glVertex3f(0.0, 0.0, 0.0)
                gl.glVertex3f(axis_length, 0.0, 0.0)
                
                # Y axis (green)  
                gl.glColor3f(0.0, 1.0, 0.0)
                gl.glVertex3f(0.0, 0.0, 0.0)
                gl.glVertex3f(0.0, axis_length, 0.0)
                
                # Z axis (blue)
                gl.glColor3f(0.0, 0.0, 1.0)
                gl.glVertex3f(0.0, 0.0, 0.0)
                gl.glVertex3f(0.0, 0.0, axis_length)
            finally:
                gl.glEnd()  # ALWAYS call glEnd in finally block
            
            # Draw axis labels as points
            gl.glPointSize(12.0)
            gl.glBegin(gl.GL_POINTS)
            try:
                # X label
                gl.glColor3f(1.0, 0.0, 0.0)
                gl.glVertex3f(axis_length + 0.2, 0.0, 0.0)
                
                # Y label
                gl.glColor3f(0.0, 1.0, 0.0)
                gl.glVertex3f(0.0, axis_length + 0.2, 0.0)
                
                # Z label
                gl.glColor3f(0.0, 0.0, 1.0)
                gl.glVertex3f(0.0, 0.0, axis_length + 0.2)
            finally:
                gl.glEnd()  # ALWAYS call glEnd in finally block

            # Draw arrow heads
            self.draw_axis_arrow_head(Vector3(axis_length, 0, 0), Vector3(1, 0, 0), 0.2, (1.0, 0.0, 0.0))
            self.draw_axis_arrow_head(Vector3(0, axis_length, 0), Vector3(0, 1, 0), 0.2, (0.0, 1.0, 0.0))
            self.draw_axis_arrow_head(Vector3(0, 0, axis_length), Vector3(0, 0, 1), 0.2, (0.0, 0.0, 1.0))
            
            gl.glEnable(gl.GL_LIGHTING)
            gl.glLineWidth(1.0)
            gl.glPointSize(1.0)
            
        except Exception as e:
            print(f"Error drawing coordinate axes: {e}")
    
    def draw_axis_arrow_head(self, position: Vector3, direction: Vector3, size: float, color: tuple):
        """Draw arrow head safely."""
        try:
            gl.glColor3f(*color)
            gl.glLineWidth(2.0)
            
            gl.glPushMatrix()
            gl.glTranslatef(position.x, position.y, position.z)
            
            # Create perpendicular vectors
            if abs(direction.z) < 0.9:
                perpendicular1 = Vector3(0, 0, 1).cross(direction).normalize() * size
            else:
                perpendicular1 = Vector3(1, 0, 0).cross(direction).normalize() * size
            
            perpendicular2 = direction.cross(perpendicular1).normalize() * size
            back_point = direction * (-size * 2)
            
            # Draw arrow head lines safely
            gl.glBegin(gl.GL_LINES)
            try:
                gl.glVertex3f(0, 0, 0)
                gl.glVertex3f(back_point.x + perpendicular1.x, back_point.y + perpendicular1.y, back_point.z + perpendicular1.z)
                
                gl.glVertex3f(0, 0, 0)
                gl.glVertex3f(back_point.x - perpendicular1.x, back_point.y - perpendicular1.y, back_point.z - perpendicular1.z)
                
                gl.glVertex3f(0, 0, 0)
                gl.glVertex3f(back_point.x + perpendicular2.x, back_point.y + perpendicular2.y, back_point.z + perpendicular2.z)
                
                gl.glVertex3f(0, 0, 0)
                gl.glVertex3f(back_point.x - perpendicular2.x, back_point.y - perpendicular2.y, back_point.z - perpendicular2.z)
            finally:
                gl.glEnd()  # ALWAYS call glEnd
                
            gl.glPopMatrix()
            gl.glLineWidth(1.0)
            
        except Exception as e:
            print(f"Error drawing arrow head: {e}")
    
    def draw_rotation_axis(self):
        """Draw rotation axis safely."""
        if self.rotation_axis.magnitude() == 0:
            return
        
        try:
            gl.glDisable(gl.GL_LIGHTING)
            gl.glColor3f(1.0, 1.0, 0.0)
            gl.glLineWidth(4.0)
            
            axis = self.rotation_axis.normalize()
            axis_length = 3.5
            
            # Draw rotation axis line
            gl.glBegin(gl.GL_LINES)
            try:
                gl.glVertex3f(-axis.x * axis_length, -axis.y * axis_length, -axis.z * axis_length)
                gl.glVertex3f(axis.x * axis_length, axis.y * axis_length, axis.z * axis_length)
            finally:
                gl.glEnd()
            
            # Draw arrow heads
            self.draw_rotation_arrow_head(
                Vector3(axis.x * axis_length, axis.y * axis_length, axis.z * axis_length), 
                axis, 0.4
            )
            self.draw_rotation_arrow_head(
                Vector3(-axis.x * axis_length, -axis.y * axis_length, -axis.z * axis_length), 
                axis * -1, 0.4
            )
            
            # Draw points at axis ends
            gl.glPointSize(8.0)
            gl.glBegin(gl.GL_POINTS)
            try:
                gl.glColor3f(1.0, 1.0, 1.0)
                gl.glVertex3f(axis.x * (axis_length + 0.5), axis.y * (axis_length + 0.5), axis.z * (axis_length + 0.5))
            finally:
                gl.glEnd()
            
            gl.glEnable(gl.GL_LIGHTING)
            gl.glLineWidth(1.0)
            gl.glPointSize(1.0)
            
        except Exception as e:
            print(f"Error drawing rotation axis: {e}")
    
    def draw_rotation_arrow_head(self, position: Vector3, direction: Vector3, size: float):
        """Draw rotation arrow head safely."""
        try:
            gl.glColor3f(1.0, 1.0, 0.0)
            gl.glLineWidth(3.0)
            
            gl.glPushMatrix()
            gl.glTranslatef(position.x, position.y, position.z)
            
            # Create perpendicular vectors
            if abs(direction.z) < 0.9:
                perpendicular1 = Vector3(0, 0, 1).cross(direction).normalize() * size
            else:
                perpendicular1 = Vector3(1, 0, 0).cross(direction).normalize() * size
            
            perpendicular2 = direction.cross(perpendicular1).normalize() * size
            back_point = direction * (-size * 1.5)
            
            # Draw arrow head safely
            gl.glBegin(gl.GL_LINES)
            try:
                gl.glVertex3f(0, 0, 0)
                gl.glVertex3f(back_point.x + perpendicular1.x, back_point.y + perpendicular1.y, back_point.z + perpendicular1.z)
                
                gl.glVertex3f(0, 0, 0)
                gl.glVertex3f(back_point.x - perpendicular1.x, back_point.y - perpendicular1.y, back_point.z - perpendicular1.z)
                
                gl.glVertex3f(0, 0, 0)
                gl.glVertex3f(back_point.x + perpendicular2.x, back_point.y + perpendicular2.y, back_point.z + perpendicular2.z)
                
                gl.glVertex3f(0, 0, 0)
                gl.glVertex3f(back_point.x - perpendicular2.x, back_point.y - perpendicular2.y, back_point.z - perpendicular2.z)
            finally:
                gl.glEnd()  # ALWAYS call glEnd
                
            gl.glPopMatrix()
            gl.glLineWidth(1.0)
            
        except Exception as e:
            print(f"Error drawing rotation arrow head: {e}")
    
    def draw_angle_visualization(self):
        """Draw angle visualization safely."""
        if abs(self.rotation_angle) < 0.1 or self.rotation_axis.magnitude() == 0:
            return
        
        try:
            gl.glDisable(gl.GL_LIGHTING)
            
            axis = self.rotation_axis.normalize()
            radius = 1.8
            
            # Create perpendicular vectors
            if abs(axis.z) < 0.9:
                u = Vector3(0, 0, 1).cross(axis).normalize()
            else:
                u = Vector3(1, 0, 0).cross(axis).normalize()
            
            v = axis.cross(u).normalize()
            
            # Draw arc safely
            gl.glColor3f(1.0, 0.6, 0.0)
            gl.glLineWidth(3.0)
            
            steps = max(12, int(abs(self.rotation_angle) / 3))
            gl.glBegin(gl.GL_LINE_STRIP)
            try:
                for i in range(steps + 1):
                    angle_progress = (i / steps) * math.radians(abs(self.rotation_angle))
                    if self.rotation_angle < 0:
                        angle_progress = -angle_progress
                    
                    cos_a = math.cos(angle_progress)
                    sin_a = math.sin(angle_progress)
                    
                    point = (u * cos_a + v * sin_a) * radius
                    gl.glVertex3f(point.x, point.y, point.z)
            finally:
                gl.glEnd()  # ALWAYS call glEnd
            
            # Draw radius lines safely
            gl.glColor3f(0.8, 0.4, 0.0)
            gl.glLineWidth(2.0)
            gl.glBegin(gl.GL_LINES)
            try:
                # Start line
                start_point = u * radius
                gl.glVertex3f(0, 0, 0)
                gl.glVertex3f(start_point.x, start_point.y, start_point.z)
                
                # End line
                end_angle = math.radians(self.rotation_angle)
                cos_end = math.cos(end_angle)
                sin_end = math.sin(end_angle)
                end_point = (u * cos_end + v * sin_end) * radius
                gl.glVertex3f(0, 0, 0)
                gl.glVertex3f(end_point.x, end_point.y, end_point.z)
            finally:
                gl.glEnd()  # ALWAYS call glEnd
            
            # Draw points safely
            gl.glPointSize(8.0)
            gl.glBegin(gl.GL_POINTS)
            try:
                # Start point (green)
                start_point = u * radius
                gl.glColor3f(0.0, 1.0, 0.0)
                gl.glVertex3f(start_point.x, start_point.y, start_point.z)
                
                # End point (red)
                end_angle = math.radians(self.rotation_angle)
                cos_end = math.cos(end_angle)
                sin_end = math.sin(end_angle)
                end_point = (u * cos_end + v * sin_end) * radius
                gl.glColor3f(1.0, 0.0, 0.0)
                gl.glVertex3f(end_point.x, end_point.y, end_point.z)
                
                # Mid point (white)
                mid_angle = math.radians(self.rotation_angle / 2)
                cos_mid = math.cos(mid_angle)
                sin_mid = math.sin(mid_angle)
                mid_point = (u * cos_mid + v * sin_mid) * (radius * 1.3)
                gl.glColor3f(1.0, 1.0, 1.0)
                gl.glVertex3f(mid_point.x, mid_point.y, mid_point.z)
            finally:
                gl.glEnd()  # ALWAYS call glEnd

            gl.glEnable(gl.GL_LIGHTING)
            gl.glLineWidth(1.0)
            gl.glPointSize(1.0)
            
        except Exception as e:
            print(f"Error drawing angle visualization: {e}")
    
    def draw_obj(self, obj_data: OBJData, color=(1.0, 1.0, 1.0)):
        """Draw object safely."""
        if not obj_data or not obj_data.vertices or not obj_data.faces:
            return
        
        try:
            # Set material
            gl.glMaterialfv(gl.GL_FRONT, gl.GL_AMBIENT_AND_DIFFUSE, [*color, 1.0])
            gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])
            gl.glMaterialf(gl.GL_FRONT, gl.GL_SHININESS, 32.0)

            normals = self.calculate_face_normals(obj_data)
            
            # Draw faces safely
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
            for i, face in enumerate(obj_data.faces):
                if len(face.vertex_indices) >= 3:
                    gl.glBegin(gl.GL_POLYGON)
                    try:
                        if i < len(normals):
                            normal = normals[i]
                            gl.glNormal3f(normal.x, normal.y, normal.z)
                        else:
                            gl.glNormal3f(0.0, 0.0, 1.0)
                        
                        for vertex_index in face.vertex_indices:
                            if 0 <= vertex_index < len(obj_data.vertices):
                                vertex = obj_data.vertices[vertex_index]
                                gl.glVertex3f(vertex.x, vertex.y, vertex.z)
                    finally:
                        gl.glEnd()  # ALWAYS call glEnd

            # Draw wireframe safely
            gl.glDisable(gl.GL_LIGHTING)
            gl.glColor3f(*[c * 0.8 for c in color])
            gl.glLineWidth(1.5)
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
            
            for face in obj_data.faces:
                if len(face.vertex_indices) >= 3:
                    gl.glBegin(gl.GL_POLYGON)
                    try:
                        for vertex_index in face.vertex_indices:
                            if 0 <= vertex_index < len(obj_data.vertices):
                                vertex = obj_data.vertices[vertex_index]
                                gl.glVertex3f(vertex.x, vertex.y, vertex.z)
                    finally:
                        gl.glEnd()  # ALWAYS call glEnd
            
            # Draw label point safely
            gl.glPointSize(10.0)
            gl.glBegin(gl.GL_POINTS)
            try:
                gl.glColor3f(1.0, 1.0, 1.0)
                
                if obj_data.vertices:
                    center_x = sum(v.x for v in obj_data.vertices) / len(obj_data.vertices)
                    center_y = sum(v.y for v in obj_data.vertices) / len(obj_data.vertices)
                    center_z = sum(v.z for v in obj_data.vertices) / len(obj_data.vertices)
                    
                    gl.glVertex3f(center_x, center_y + 2.0, center_z)
            finally:
                gl.glEnd()  # ALWAYS call glEnd
            
            gl.glPointSize(1.0)
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
            gl.glEnable(gl.GL_LIGHTING)
            gl.glLineWidth(1.0)
            
        except Exception as e:
            print(f"Error drawing object: {e}")
    
    def calculate_face_normals(self, obj_data: OBJData) -> list:
        """Calculate face normals safely."""
        normals = []
        
        try:
            for face in obj_data.faces:
                if len(face.vertex_indices) >= 3:
                    v0_idx = face.vertex_indices[0]
                    v1_idx = face.vertex_indices[1]
                    v2_idx = face.vertex_indices[2]
                    
                    if (0 <= v0_idx < len(obj_data.vertices) and 
                        0 <= v1_idx < len(obj_data.vertices) and 
                        0 <= v2_idx < len(obj_data.vertices)):
                        
                        v0 = obj_data.vertices[v0_idx]
                        v1 = obj_data.vertices[v1_idx]
                        v2 = obj_data.vertices[v2_idx]
                        
                        edge1 = Vector3(v1.x - v0.x, v1.y - v0.y, v1.z - v0.z)
                        edge2 = Vector3(v2.x - v0.x, v2.y - v0.y, v2.z - v0.z)
                        
                        normal = edge1.cross(edge2)
                        if normal.magnitude() > 0:
                            normal = normal.normalize()
                        else:
                            normal = Vector3(0, 0, 1)
                        
                        normals.append(normal)
                    else:
                        normals.append(Vector3(0, 0, 1))
                else:
                    normals.append(Vector3(0, 0, 1))
        except Exception as e:
            print(f"Error calculating normals: {e}")
            normals.append(Vector3(0, 0, 1))
        
        return normals
    
    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        zoom_factor = 1.1
        
        if delta > 0:
            self.camera_distance /= zoom_factor
        else:
            self.camera_distance *= zoom_factor
        
        self.camera_distance = max(2.0, min(25.0, self.camera_distance))
        
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
            self.update()
    
    def mouseReleaseEvent(self, event):
        self.last_mouse_pos = None