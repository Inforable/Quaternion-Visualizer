import math
from typing import List, Tuple
from .matrix4 import Matrix4

class Camera:
    def __init__(self, distance: float = 10.0, target: List[float] = None):
        # Posisi kamera
        self.distance = distance
        self.angle_x = 0.0  # Vertical angle
        self.angle_y = 0.0  # Horizontal angle

        # Titik target
        self.target = target or [0.0, 0.0, 0.0]

        # Parameter kamera
        self.fov = 60.0
        self.near = 0.1
        self.far = 100.0

        # Sensitivitas kontrol
        self.orbit_sensitivity = 0.5
        self.zoom_sensitivity = 0.1

        # Constraints
        self.min_distance = 1.0
        self.max_distance = 50.0
        self.min_elevation = -89.0
        self.max_elevation = 89.0
    
    def get_position(self) -> List[float]:
        # Konversi sudut ke radian
        angle_x_rad = math.radians(self.angle_x)
        angle_y_rad = math.radians(self.angle_y)

        x = self.distance * math.cos(angle_x_rad) * math.cos(angle_y_rad)
        y = self.distance * math.sin(angle_x_rad)
        z = self.distance * math.cos(angle_x_rad) * math.sin(angle_y_rad)

        # Add target offset
        return [
            x + self.target[0],
            y + self.target[1],
            z + self.target[2]
        ]
    
    def get_view_matrix(self) -> Matrix4:
        eye = self.get_position()
        up = [0.0, 1.0, 0.0]
        return Matrix4.look_at(eye, self.target, up)
    
    def get_projection_matrix(self, aspect_ratio: float) -> Matrix4:
        return Matrix4.perspective(self.fov, aspect_ratio, self.near, self.far)

    def orbit(self, delta_x: float, delta_y: float):
        # Update angle based on mouse
        self.angle_y += delta_x * self.orbit_sensitivity
        self.angle_x += delta_y * self.orbit_sensitivity

        # Apply constraints
        self.angle_x = max(self.min_elevation, min(self.max_elevation, self.angle_x))
        self.angle_y = self.angle_y % 360.0
    
    def zoom(self, delta: float):
        zoom_factor = 1.0 + (delta * self.zoom_sensitivity)
        self.distance *= zoom_factor
        self.distance = max(self.min_distance, min(self.max_distance, self.distance))
    
    def pan(self, delta_x: float, delta_y: float):
        eye = self.get_position()

        # Calculate camera coordinate system
        forward = [self.target[i] - eye[i] for i in range(3)]
        forward_len = math.sqrt(sum(x * x for x in forward))

        if forward_len > 0:
            forward = [x / forward_len for x in forward]
        
        # Right vector 
        world_up = [0.0, 1.0, 0.0]
        right = [
            world_up[1] * forward[2] - world_up[2] * forward[1],
            world_up[2] * forward[0] - world_up[0] * forward[2],
            world_up[0] * forward[1] - world_up[1] * forward[0]
        ]
        right_len = math.sqrt(sum(x * x for x in right))
        if right_len > 0:
            right = [x / right_len for x in right]

        # Up vector
        up = [
            right[1] * forward[2] - right[2] * forward[1],
            right[2] * forward[0] - right[0] * forward[2],
            right[0] * forward[1] - right[1] * forward[0]
        ]

        pan_speed = self.distance * 0.001
        for i in range(3):
            self.target[i] += (right[i] * delta_x + up[i] * delta_y) * pan_speed
    
    def reset(self):
        # Reset camera to default position
        self.distance = 10.0
        self.angle_x = 0.0
        self.angle_y = 0.0
        self.target = [0.0, 0.0, 0.0]
    
    def set_target(self, target: List[float]):
        self.target = target[:]
    
    def get_info(self) -> dict:
        position = self.get_position()
        return {
            'position': position,
            'target': self.target,
            'distance': self.distance,
            'angle_x': self.angle_x,
            'angle_y': self.angle_y,
            'fov': self.fov
        }