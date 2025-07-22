from PySide6.QtCore import QTimer
from PySide6.QtOpenGLWidgets import QOpenGLWidget

import OpenGL.GL as gl
import OpenGL.GLU as glu
import math

from ...core.io.obj_loader import OBJData


class OpenGLView(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 3D scene data
        self.original_obj: OBJData = None
        self.rotated_obj: OBJData = None
        
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
    
    def initializeGL(self):
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
    
    def resizeGL(self, width, height):
        if height == 0:
            height = 1
        
        aspect_ratio = width / height
        
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        
        # Membuat perspektif
        glu.gluPerspective(45.0, aspect_ratio, 0.1, 100.0)
        
        gl.glMatrixMode(gl.GL_MODELVIEW)
    
    def paintGL(self):
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
        
        # Menggambar axis
        self.draw_axes()
        
        # Menggambar original object
        if self.original_obj:
            gl.glPushMatrix()
            gl.glTranslatef(-2.0, 0.0, 0.0)  # Move to left
            self.draw_obj(self.original_obj, color=(0.3, 0.5, 1.0))  # Blue
            gl.glPopMatrix()
        
        # Menggambar rotated object
        if self.rotated_obj:
            gl.glPushMatrix()
            gl.glTranslatef(2.0, 0.0, 0.0)  # Move to right
            self.draw_obj(self.rotated_obj, color=(1.0, 0.3, 0.3))  # Red
            gl.glPopMatrix()
    
    def draw_axes(self):
        gl.glDisable(gl.GL_LIGHTING)
        gl.glBegin(gl.GL_LINES)
        
        # X axis (red)
        gl.glColor3f(1.0, 0.0, 0.0)
        gl.glVertex3f(0.0, 0.0, 0.0)
        gl.glVertex3f(1.5, 0.0, 0.0)
        
        # Y axis (green)  
        gl.glColor3f(0.0, 1.0, 0.0)
        gl.glVertex3f(0.0, 0.0, 0.0)
        gl.glVertex3f(0.0, 1.5, 0.0)
        
        # Z axis (blue)
        gl.glColor3f(0.0, 0.0, 1.0)
        gl.glVertex3f(0.0, 0.0, 0.0)
        gl.glVertex3f(0.0, 0.0, 1.5)
        
        gl.glEnd()
        gl.glEnable(gl.GL_LIGHTING)
    
    def draw_obj(self, obj_data: OBJData, color=(1.0, 1.0, 1.0)):
        if not obj_data or not obj_data.vertices or not obj_data.faces:
            return
        
        # Atur material color
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_AMBIENT_AND_DIFFUSE, [*color, 1.0])
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])
        gl.glMaterialf(gl.GL_FRONT, gl.GL_SHININESS, 32.0)
        
        # Menggambar faces
        for face in obj_data.faces:
            if len(face.vertex_indices) >= 3:
                gl.glBegin(gl.GL_POLYGON)
                
                for vertex_index in face.vertex_indices:
                    if 0 <= vertex_index < len(obj_data.vertices):
                        vertex = obj_data.vertices[vertex_index]
                        
                        gl.glNormal3f(0.0, 0.0, 1.0)  # Placeholder normal
                        gl.glVertex3f(vertex.x, vertex.y, vertex.z)
                
                gl.glEnd()

        # Menggambar wireframe overlay
        gl.glDisable(gl.GL_LIGHTING)
        gl.glColor3f(*color)
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
    
    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        zoom_factor = 1.1
        
        if delta > 0:
            self.camera_distance /= zoom_factor
        else:
            self.camera_distance *= zoom_factor
        
        self.camera_distance = max(2.0, min(20.0, self.camera_distance))
        
        self.update()
    
    def mousePressEvent(self, event):
        self.last_mouse_pos = event.position()
    
    def mouseMoveEvent(self, event):
        if self.last_mouse_pos and event.buttons():
            dx = event.position().x() - self.last_mouse_pos.x()
            dy = event.position().y() - self.last_mouse_pos.y()
            
            # Update rotasi kamera
            self.camera_rotation_y += dx * 0.5
            self.camera_rotation_x -= dy * 0.5
            
            # clamp rotasi kamera
            self.camera_rotation_x = max(-90, min(90, self.camera_rotation_x))
            
            self.last_mouse_pos = event.position()
            self.update()
    
    def mouseReleaseEvent(self, event):
        self.last_mouse_pos = None