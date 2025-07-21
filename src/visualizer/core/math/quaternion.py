import math
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from .vector3 import Vector3

class Quaternion:
    def __init__(self, w:float = 1.0, x:float = 0.0, y:float = 0.0, z:float = 0.0):
        self.w = w
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return f"Quaternion({self.w:.3f}, {self.x:.3f}, {self.y:.3f}, {self.z:.3f})"
    
    @staticmethod
    def from_axis_angle(axis: Vector3, angle_degress: float):
        angle_red = math.radians(angle_degress)
        half_angle = angle_red / 2.0

        normalized_axis = axis.normalize()

        sin_half_angle = math.sin(half_angle)
        cos_half_angle = math.cos(half_angle)

        return Quaternion(
            w=cos_half_angle,
            x=normalized_axis.x * sin_half_angle,
            y=normalized_axis.y * sin_half_angle,
            z=normalized_axis.z * sin_half_angle
        )
    
    def __mul__(self, other):
        w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
        x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
        y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
        z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
        return Quaternion(w, x, y, z)

    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)
    
    def rotate_vector(self, vector: Vector3) -> Vector3:
        # Konversi vector ke quaternion
        vector_quat = Quaternion(0, vector.x, vector.y, vector.z)

        # Rotasi vector dengan quaternion
        rotated_vector_quat = self * vector_quat * self.conjugate()

        return Vector3(rotated_vector_quat.x, rotated_vector_quat.y, rotated_vector_quat.z)