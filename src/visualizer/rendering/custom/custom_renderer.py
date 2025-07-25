import math
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QFontMetrics
from PySide6.QtCore import QPoint

from .projection import ProjectionEngine
from .matrix4 import Matrix4
from .camera import Camera
from ...core.math.vector3 import Vector3

class CustomRenderer(QWidget): 
    def __init__(self, parent=None):
        super().__init__(parent)

        # Komponen Graphics Engine
        self.projection = ProjectionEngine()
        self.camera = Camera(distance=8.0)
        
        # Mouse control
        self.last_mouse_pos = None
        self.mouse_button_pressed = None
        
        # 3D Objects
        self.original_obj = None
        self.rotated_obj = None
        
        # Parameter rotasi 
        self.rotation_axis = Vector3(0, 0, 1)
        self.rotation_angle = 0.0
        
        # Visualization data
        self.viz_data = None
        
        # Display flags
        self.show_coordinate_axes = True
        self.show_rotation_visualization = True
        self.show_labels = True
        self.show_grid = False
        self.wireframe_mode = False
        
        # Rendering settings
        self.axis_length = 4.0
        self.grid_size = 10
        self.grid_spacing = 1.0
        
        # Colors
        self.background_color = QColor(26, 26, 26)
        self.grid_color = QColor(60, 60, 70, 120)
        self.x_axis_color = QColor(255, 80, 80)
        self.y_axis_color = QColor(80, 255, 80)
        self.z_axis_color = QColor(80, 80, 255)
        self.rotation_axis_color = QColor(255, 255, 0)
        self.original_color = QColor(76, 128, 255)
        self.rotated_color = QColor(255, 76, 76)
        self.angle_label_color = QColor(255, 255, 255)
        
        # Setup initial camera
        self.setup_initial_camera()
        
        # Text rendering setup
        self.setup_text_rendering()
        
        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(33)

        self.setMouseTracking(True)
    
    def setup_initial_camera(self):
        self.camera.distance = 8.0
        self.camera.angle_x = 20.0
        self.camera.angle_y = 45.0
        self.camera.target = [0.0, 0.0, 0.0]

    def setup_text_rendering(self):
        self.label_font = QFont("Arial", 14, QFont.Weight.Bold)
        self.axis_font = QFont("Arial", 9, QFont.Weight.Normal)
        self.angle_font = QFont("Arial", 16, QFont.Weight.Bold)

        self.font_metrics = QFontMetrics(self.label_font)
        self.axis_font_metrics = QFontMetrics(self.axis_font)
        self.angle_font_metrics = QFontMetrics(self.angle_font)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        
        # Clear background
        painter.fillRect(self.rect(), self.background_color)
        
        try:
            # Setup projection viewport
            self.projection.set_viewport(self.width(), self.height())

            # Hitung matriks
            aspect_ratio = self.width() / self.height() if self.height() > 0 else 1.0
            proj_matrix = self.camera.get_projection_matrix(aspect_ratio)
            view_matrix = self.camera.get_view_matrix()
            mvp_matrix = proj_matrix.multiply_matrix(view_matrix)
            
            # Render scene components
            if self.show_coordinate_axes:
                self._draw_coordinate_system(painter, mvp_matrix)
            
            if self.show_rotation_visualization:
                self._draw_rotation_visualization(painter, mvp_matrix)
            
            # Render 3D objects
            if self.original_obj:
                self._draw_obj_data(
                    painter, mvp_matrix, self.original_obj,
                    offset=Vector3(-3.0, 0.0, 0.0),
                    color=self.original_color,
                    label="Original Object"
                )
            
            if self.rotated_obj:
                self._draw_obj_data(
                    painter, mvp_matrix, self.rotated_obj,
                    offset=Vector3(3.0, 0.0, 0.0),
                    color=self.rotated_color,
                    label="Rotated Object"
                )
            
        except Exception as e:
            print(f"Error in custom renderer paint: {e}")
            
        painter.end()
    
    def _draw_coordinate_system(self, painter: QPainter, mvp_matrix: Matrix4):
        # label 'i'
        painter.setPen(QPen(self.x_axis_color, 3))
        self._draw_line_3d(painter, mvp_matrix, [0, 0, 0], [self.axis_length, 0, 0])
        self._draw_enhanced_arrow(painter, mvp_matrix, [self.axis_length, 0, 0], [1, 0, 0], self.x_axis_color)
        
        # label 'j'
        painter.setPen(QPen(self.y_axis_color, 3))
        self._draw_line_3d(painter, mvp_matrix, [0, 0, 0], [0, self.axis_length, 0])
        self._draw_enhanced_arrow(painter, mvp_matrix, [0, self.axis_length, 0], [0, 1, 0], self.y_axis_color)
        
        # label 'k'
        painter.setPen(QPen(self.z_axis_color, 3))
        self._draw_line_3d(painter, mvp_matrix, [0, 0, 0], [0, 0, self.axis_length])
        self._draw_enhanced_arrow(painter, mvp_matrix, [0, 0, self.axis_length], [0, 0, 1], self.z_axis_color)
        
        if self.show_labels:
            self._draw_axis_labels_ijk(painter, mvp_matrix)
    
    def _draw_enhanced_arrow(self, painter: QPainter, mvp_matrix: Matrix4, tip_pos, direction, color):
        arrow_size = 0.3
        arrow_width = 0.15
        
        # Calculate perpendicular vectors for arrow
        if abs(direction[1]) < 0.9:
            perp1 = [-direction[1], direction[0], 0]
        else:
            perp1 = [0, -direction[2], direction[1]]
            
        # Normalize
        perp_mag = math.sqrt(sum(x*x for x in perp1))
        if perp_mag > 0:
            perp1 = [x/perp_mag for x in perp1]
            
        # Second perpendicular
        perp2 = [
            direction[1]*perp1[2] - direction[2]*perp1[1],
            direction[2]*perp1[0] - direction[0]*perp1[2],
            direction[0]*perp1[1] - direction[1]*perp1[0]
        ]
        
        # Arrow base
        base = [tip_pos[i] - direction[i] * arrow_size * 2 for i in range(3)]
        
        # Draw arrow lines
        painter.setPen(QPen(color, 3))
        num_segments = 4
        for i in range(num_segments):
            angle = 2 * math.pi * i / num_segments
            p = [base[j] + arrow_width * (math.cos(angle) * perp1[j] + math.sin(angle) * perp2[j]) for j in range(3)]
            self._draw_line_3d(painter, mvp_matrix, tip_pos, p)
    
    def _draw_rotation_visualization(self, painter: QPainter, mvp_matrix: Matrix4):
        if self.rotation_axis.magnitude() > 0:
            self._draw_rotation_axis(painter, mvp_matrix, self.rotation_axis)
            
            if abs(self.rotation_angle) > 0.1:
                self._draw_rotation_arc(painter, mvp_matrix, self.rotation_axis, self.rotation_angle)
                
            if self.show_labels:
                self._draw_rotation_angle_label(painter, mvp_matrix, self.rotation_axis, self.rotation_angle)
    
    def _draw_rotation_axis(self, painter: QPainter, mvp_matrix: Matrix4, axis):
        # Normalize axis
        axis_mag = axis.magnitude()
        if axis_mag < 0.0001:
            return
        
        norm_axis = Vector3(axis.x / axis_mag, axis.y / axis_mag, axis.z / axis_mag)

        axis_len = 5.0
        start = [-norm_axis.x * axis_len, -norm_axis.y * axis_len, -norm_axis.z * axis_len]
        end = [norm_axis.x * axis_len, norm_axis.y * axis_len, norm_axis.z * axis_len]
        
        painter.setPen(QPen(self.rotation_axis_color, 5))
        self._draw_line_3d(painter, mvp_matrix, start, end)
    
    def _draw_rotation_arc(self, painter: QPainter, mvp_matrix: Matrix4, axis, angle):
        # Normalize axis
        axis_mag = axis.magnitude()
        if axis_mag < 0.0001:
            return
        
        norm_axis = Vector3(axis.x / axis_mag, axis.y / axis_mag, axis.z / axis_mag)
        
        if abs(norm_axis.z) < 0.9:
            perp1 = Vector3(0, 0, 1).cross(norm_axis).normalize()
        else:
            perp1 = Vector3(1, 0, 0).cross(norm_axis).normalize()
        
        perp2 = norm_axis.cross(perp1).normalize()
        
        radius = 2.5
        segments = max(16, int(abs(angle) / 2))
        angle_rad = math.radians(abs(angle))
        if angle < 0:
            angle_rad = -angle_rad

        painter.setPen(QPen(QColor(255, 150, 0), 4))

        prev_point = None
        for i in range(segments + 1):
            t = i / segments
            current_angle = angle_rad * t
            
            cos_a = math.cos(current_angle)
            sin_a = math.sin(current_angle)
            
            # Calculate point on arc
            arc_point = [
                (perp1.x * cos_a + perp2.x * sin_a) * radius,
                (perp1.y * cos_a + perp2.y * sin_a) * radius,
                (perp1.z * cos_a + perp2.z * sin_a) * radius
            ]
            
            projected = self.projection.project_vertex(arc_point, mvp_matrix)
            if projected:
                x, y, z = projected
                if self.projection.is_point_in_viewport(x, y):
                    if prev_point:
                        painter.drawLine(prev_point[0], prev_point[1], int(x), int(y))
                    prev_point = (int(x), int(y))
    
    def _draw_obj_data(self, painter: QPainter, mvp_matrix: Matrix4, obj_data, offset=None, color=None, label=None):
        if not obj_data or not hasattr(obj_data, 'vertices') or not hasattr(obj_data, 'faces'):
            return
        
        if offset is None:
            offset = Vector3(0, 0, 0)
        if color is None:
            color = QColor(255, 255, 255)
        
        # Project all vertices
        projected_vertices = []
        for vertex in obj_data.vertices:
            world_pos = [
                vertex.x + offset.x,
                vertex.y + offset.y,
                vertex.z + offset.z
            ]
            projected = self.projection.project_vertex(world_pos, mvp_matrix)
            projected_vertices.append(projected)
        
        self._draw_wireframe(painter, mvp_matrix, obj_data.faces, projected_vertices, color)
    
    def _draw_wireframe(self, painter: QPainter, mvp_matrix: Matrix4, faces, projected_vertices, color):
        painter.setPen(QPen(color, 2))
        painter.setBrush(QBrush())
        
        for face in faces:
            if len(face.vertex_indices) >= 3:
                for i in range(len(face.vertex_indices)):
                    start_idx = face.vertex_indices[i]
                    end_idx = face.vertex_indices[(i + 1) % len(face.vertex_indices)]
                    
                    if (0 <= start_idx < len(projected_vertices) and 
                        0 <= end_idx < len(projected_vertices)):
                        
                        start_proj = projected_vertices[start_idx]
                        end_proj = projected_vertices[end_idx]
                        
                        if start_proj and end_proj:
                            x1, y1, z1 = start_proj
                            x2, y2, z2 = end_proj
                            
                            if (self.projection.is_point_in_viewport(x1, y1) or 
                                self.projection.is_point_in_viewport(x2, y2)):
                                painter.drawLine(int(x1), int(y1), int(x2), int(y2))
    
    def _draw_axis_labels_ijk(self, painter: QPainter, mvp_matrix: Matrix4):
        label_ratio = 0.7
        
        # Label positions
        labels = [
            ([self.axis_length * label_ratio, 0.0, 0.0], "i", self.x_axis_color),
            ([0.0, self.axis_length * label_ratio, 0.0], "j", self.y_axis_color),
            ([0.0, 0.0, self.axis_length * label_ratio], "k", self.z_axis_color)
        ]
        
        for pos_3d, text, color in labels:
            projected = self.projection.project_vertex(pos_3d, mvp_matrix)
            if projected:
                x, y, z = projected
                if self.projection.is_point_in_viewport(x, y):
                    painter.setFont(self.label_font)
                    painter.setPen(color)
                    painter.drawText(int(x + 2), int(y - 5), text)
    
    def _draw_rotation_angle_label(self, painter: QPainter, mvp_matrix: Matrix4, axis, angle):
        if abs(angle) < 0.1:
            return
        
        # Normalize axis
        axis_mag = axis.magnitude()
        if axis_mag < 0.0001:
            return
        
        norm_axis = Vector3(axis.x / axis_mag, axis.y / axis_mag, axis.z / axis_mag)
        
        if abs(norm_axis.z) < 0.9:
            u = Vector3(0, 0, 1).cross(norm_axis).normalize()
        else:
            u = Vector3(1, 0, 0).cross(norm_axis).normalize()
        
        label_radius = 3.0
        mid_angle = math.radians(angle / 2)
        
        # Simplified position calculation
        mid_x = u.x * math.cos(mid_angle) * label_radius
        mid_y = u.y * math.cos(mid_angle) * label_radius + 0.5
        mid_z = u.z * math.cos(mid_angle) * label_radius
        
        projected = self.projection.project_vertex([mid_x, mid_y, mid_z], mvp_matrix)
        if projected:
            x, y, z = projected
            if self.projection.is_point_in_viewport(x, y):
                painter.setFont(self.angle_font)
                painter.setPen(QColor(255, 255, 255))
                
                degree_text = f"{angle:.1f}°"
                
                metrics = painter.fontMetrics()
                text_rect = metrics.boundingRect(degree_text)
                
                bg_rect = text_rect.translated(x + 10, y - text_rect.height())
                bg_rect.adjust(-2, -1, 2, 1)
                
                painter.fillRect(bg_rect, QColor(0, 0, 0, 128))
                painter.drawText(int(x + 12), int(y), degree_text)
    
    def _draw_line_3d(self, painter: QPainter, mvp_matrix: Matrix4, start_pos, end_pos):
        start_projected = self.projection.project_vertex(start_pos, mvp_matrix)
        end_projected = self.projection.project_vertex(end_pos, mvp_matrix)
        
        if start_projected and end_projected:
            x1, y1, z1 = start_projected
            x2, y2, z2 = end_projected
            
            if (self.projection.is_point_in_viewport(x1, y1) or 
                self.projection.is_point_in_viewport(x2, y2)):
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_mouse_pos = event.position()
            self.mouse_button_pressed = Qt.MouseButton.LeftButton
    
    def mouseMoveEvent(self, event):
        if self.last_mouse_pos is None or self.mouse_button_pressed != Qt.MouseButton.LeftButton:
            return
        
        delta_x = event.position().x() - self.last_mouse_pos.x()
        delta_y = event.position().y() - self.last_mouse_pos.y()
        
        self.camera.angle_y += delta_x * 0.5
        self.camera.angle_x -= delta_y * 0.5
        
        self.camera.angle_x = max(-90, min(90, self.camera.angle_x))
        
        self.last_mouse_pos = event.position()
        self.update()
    
    def mouseReleaseEvent(self, event):
        self.last_mouse_pos = None
        self.mouse_button_pressed = None
    
    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        zoom_factor = 1.1
        
        if delta > 0:
            self.camera.distance /= zoom_factor
        else:
            self.camera.distance *= zoom_factor
        
        self.camera.distance = max(2.0, min(25.0, self.camera.distance))
        self.update()
    
    def set_obj_data(self, original_obj, rotated_obj=None):
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
    
    def reset_camera(self):
        self.setup_initial_camera()
        self.update()