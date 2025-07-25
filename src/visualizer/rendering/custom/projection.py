import math
from typing import List, Tuple, Optional
from .matrix4 import Matrix4

class ProjectionEngine:
    def __init__(self):
        self.viewport_width = 800
        self.viewport_height = 600
        
        # Z-buffer for depth testing
        self.z_buffer = None
        self.enable_z_buffer = True
    
    def set_viewport(self, width: int, height: int):
        self.viewport_width = width
        self.viewport_height = height
        
        # Initialize Z-buffer
        if self.enable_z_buffer:
            self.z_buffer = [[float('inf') for _ in range(width)] for _ in range(height)]
    
    def clear_z_buffer(self):
        if self.z_buffer:
            for row in self.z_buffer:
                for i in range(len(row)):
                    row[i] = float('inf')
    
    def project_vertex(self, vertex_3d: List[float], mvp_matrix: Matrix4) -> Optional[Tuple[int, int, float]]:
        if len(vertex_3d) == 3:
            vertex_4d = vertex_3d + [1.0]
        else:
            vertex_4d = vertex_3d[:]
    
        # Apply MVP transformation
        transformed = mvp_matrix * vertex_4d

        # Check for valid w component
        if abs(transformed[3]) < 1e-6:
            return None
        
        # Perspective divide
        x = transformed[0] / transformed[3]
        y = transformed[1] / transformed[3]
        z = transformed[2] / transformed[3]

        if z < -1.0 or z > 1.0:
            return None
        
        # Convert to screen coordinates
        screen_x = int((x + 1.0) * self.viewport_width / 2.0)
        screen_y = int((1.0 - y) * self.viewport_height / 2.0)

        # Clamp to viewport bounds
        screen_x = max(0, min(self.viewport_width - 1, screen_x))
        screen_y = max(0, min(self.viewport_height - 1, screen_y))

        return (screen_x, screen_y, z)

    def project_line_3d(self, start_3d: List[float], end_3d: List[float], mvp_matrix: Matrix4) -> Optional[Tuple[Tuple[int, int], Tuple[int,int]]]:
        start_2d = self.project_vertex(start_3d, mvp_matrix)
        end_2d = self.project_vertex(end_3d, mvp_matrix)

        if start_2d is None or end_2d is None:
            return None

        return ((start_2d[0], start_2d[1]), (end_2d[0], end_2d[1]))

    def is_point_in_viewport(self, x: int, y: int) -> bool:
        return 0 <= x < self.viewport_width and 0 <= y < self.viewport_height

    def depth_test(self, x: int, y: int, z: float) -> bool:
        if not self.enable_z_buffer or not self.z_buffer:
            return True
            
        if not self.is_point_in_viewport(x, y):
            return False
            
        if z < self.z_buffer[y][x]:
            self.z_buffer[y][x] = z
            return True
        return False

    def clip_line_to_viewport(self, start: Tuple[int, int], end: Tuple[int, int]) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        x1, y1 = start
        x2, y2 = end
        
        # Cohen-Sutherland line clipping algorithm
        INSIDE = 0
        LEFT = 1
        RIGHT = 2
        BOTTOM = 4
        TOP = 8
        
        def compute_outcode(x, y):
            code = INSIDE
            if x < 0:
                code |= LEFT
            elif x >= self.viewport_width:
                code |= RIGHT
            if y < 0:
                code |= TOP
            elif y >= self.viewport_height:
                code |= BOTTOM
            return code
        
        outcode1 = compute_outcode(x1, y1)
        outcode2 = compute_outcode(x2, y2)

        while True:
            if outcode1 == 0 and outcode2 == 0:
                return ((x1, y1), (x2, y2))
            
            if outcode1 & outcode2:
                return None
            
            outcode_out = outcode1 if outcode1 != 0 else outcode2
            
            if outcode_out & TOP:
                x = x1 + (x2 - x1) * (0 - y1) / (y2 - y1)
                y = 0
            elif outcode_out & BOTTOM:
                x = x1 + (x2 - x1) * (self.viewport_height - 1 - y1) / (y2 - y1)
                y = self.viewport_height - 1
            elif outcode_out & RIGHT:
                y = y1 + (y2 - y1) * (self.viewport_width - 1 - x1) / (x2 - x1)
                x = self.viewport_width - 1
            elif outcode_out & LEFT:
                y = y1 + (y2 - y1) * (0 - x1) / (x2 - x1)
                x = 0
            
            x, y = int(x), int(y)
            
            if outcode_out == outcode1:
                x1, y1 = x, y
                outcode1 = compute_outcode(x1, y1)
            else:
                x2, y2 = x, y
                outcode2 = compute_outcode(x2, y2)

    def rasterize_triangle(self, v1: Tuple[int, int, float], v2: Tuple[int, int, float], v3: Tuple[int, int, float]):
        # Sort vertices by Y coordinate
        vertices = sorted([v1, v2, v3], key=lambda v: v[1])
        y1, y2, y3 = vertices[0][1], vertices[1][1], vertices[2][1]
        
        if y1 == y3:  # Degenerate triangle
            return []
        
        pixels = []
        
        # Interpolate edges
        for y in range(y1, y3 + 1):
            if y < 0 or y >= self.viewport_height:
                continue
                
            # Find X intersections with edges
            x_intersections = []
            
            # Edge 1-3
            if y3 != y1:
                t = (y - y1) / (y3 - y1)
                x = vertices[0][0] + t * (vertices[2][0] - vertices[0][0])
                z = vertices[0][2] + t * (vertices[2][2] - vertices[0][2])
                x_intersections.append((x, z))
            
            # Edge 1-2 or 2-3
            if y <= y2 and y2 != y1:
                t = (y - y1) / (y2 - y1)
                x = vertices[0][0] + t * (vertices[1][0] - vertices[0][0])
                z = vertices[0][2] + t * (vertices[1][2] - vertices[0][2])
                x_intersections.append((x, z))
            elif y > y2 and y3 != y2:
                t = (y - y2) / (y3 - y2)
                x = vertices[1][0] + t * (vertices[2][0] - vertices[1][0])
                z = vertices[1][2] + t * (vertices[2][2] - vertices[1][2])
                x_intersections.append((x, z))
            
            if len(x_intersections) == 2:
                x1, z1 = x_intersections[0]
                x2, z2 = x_intersections[1]
                
                if x1 > x2:
                    x1, x2, z1, z2 = x2, x1, z2, z1
                
                x1, x2 = int(x1), int(x2)
                
                for x in range(max(0, x1), min(self.viewport_width, x2 + 1)):
                    if x2 != x1:
                        t = (x - x1) / (x2 - x1)
                        z = z1 + t * (z2 - z1)
                    else:
                        z = z1
                    
                    if self.depth_test(x, y, z):
                        pixels.append((x, y, z))
        
        return pixels


class Object3D:
    def __init__(self, vertices: List[List[float]], faces: List[List[int]]):
        self.vertices = vertices
        self.faces = faces
        self.transform = Matrix4.identity()
        self.visible = True
        self.color = (255, 255, 255)
        
    def set_transform(self, transform: Matrix4):
        self.transform = transform
    
    def set_color(self, color: Tuple[int, int, int]):
        self.color = color
    
    def get_transformed_vertices(self) -> List[List[float]]:
        transformed = []
        for vertex in self.vertices:
            vertex_4d = vertex + [1.0] if len(vertex) == 3 else vertex[:]
            transformed_4d = self.transform * vertex_4d
            transformed.append(transformed_4d[:3])
        return transformed
    
    def get_wireframe_lines(self) -> List[Tuple[List[float], List[float]]]:
        lines = []
        transformed_vertices = self.get_transformed_vertices()
        
        for face in self.faces:
            for i in range(len(face)):
                start_idx = face[i]
                end_idx = face[(i + 1) % len(face)]
                
                if start_idx < len(transformed_vertices) and end_idx < len(transformed_vertices):
                    start_vertex = transformed_vertices[start_idx]
                    end_vertex = transformed_vertices[end_idx]
                    lines.append((start_vertex, end_vertex))
        
        return lines
    
    def calculate_face_normal(self, face_indices: List[int]) -> List[float]:
        if len(face_indices) < 3:
            return [0, 0, 1]
        
        v1 = self.vertices[face_indices[0]]
        v2 = self.vertices[face_indices[1]]
        v3 = self.vertices[face_indices[2]]
        
        # Calculate normal using cross product
        edge1 = [v2[i] - v1[i] for i in range(3)]
        edge2 = [v3[i] - v1[i] for i in range(3)]
        
        normal = [
            edge1[1] * edge2[2] - edge1[2] * edge2[1],
            edge1[2] * edge2[0] - edge1[0] * edge2[2],
            edge1[0] * edge2[1] - edge1[1] * edge2[0]
        ]
        
        # Normalize
        length = math.sqrt(sum(n * n for n in normal))
        if length > 0:
            normal = [n / length for n in normal]
        
        return normal


class AxisRenderer:
    def __init__(self, length: float = 3.0):
        self.length = length
        self.axes = self._create_axes()
    
    def _create_axes(self) -> List[Tuple[List[float], List[float], Tuple[int, int, int]]]:
        origin = [0.0, 0.0, 0.0]
        
        axes = [
            (origin, [self.length, 0.0, 0.0], (255, 80, 80)),   # X - Red
            (origin, [0.0, self.length, 0.0], (80, 255, 80)),   # Y - Green
            (origin, [0.0, 0.0, self.length], (80, 80, 255))    # Z - Blue
        ]
        
        return axes
    
    def get_axis_lines(self) -> List[Tuple[List[float], List[float], Tuple[int, int, int]]]:
        return self.axes


class RotationAxisRenderer: 
    def __init__(self):
        self.rotation_axes = []
    
    def clear_axes(self):
        self.rotation_axes.clear()
    
    def add_axis(self, start: List[float], end: List[float], color: Tuple[int, int, int]):
        self.rotation_axes.append((start, end, color))
    
    def get_axis_lines(self) -> List[Tuple[List[float], List[float], Tuple[int, int, int]]]:
        return self.rotation_axes


class LightingEngine:
    def __init__(self):
        self.light_position = [5.0, 5.0, 5.0]
        self.light_color = [1.0, 1.0, 1.0]
        self.ambient_intensity = 0.3
        self.diffuse_intensity = 0.7
        
    def calculate_lighting(self, normal: List[float], vertex_pos: List[float]) -> float:
        # Calculate light direction
        light_dir = [
            self.light_position[i] - vertex_pos[i] for i in range(3)
        ]
        
        # Normalize light direction
        light_length = math.sqrt(sum(d * d for d in light_dir))
        if light_length > 0:
            light_dir = [d / light_length for d in light_dir]
        
        # Calculate dot product for diffuse lighting
        dot_product = sum(normal[i] * light_dir[i] for i in range(3))
        dot_product = max(0, dot_product)  # Clamp to positive
        
        # Combine ambient and diffuse
        intensity = self.ambient_intensity + self.diffuse_intensity * dot_product
        return min(1.0, intensity)  # Clamp to [0, 1]