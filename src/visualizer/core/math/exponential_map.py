import math
from .vector3 import Vector3
from .quaternion import Quaternion

class ExponentialMap:
    def __init__(self, omega: Vector3):
        self.omega = omega
    
    def __str__(self):
        angle_deg = math.degrees(self.omega.magnitude())
        if self.omega.magnitude() > 0:
            axis = self.omega.normalize()
            return f"ExpMap(axis: {axis}, angle: {angle_deg:.3f} degrees)"
        else :
            return "ExpMap(Tidak ada rotasi, omega nol)"
    
    @classmethod
    def from_axis_angle(cls, axis: Vector3, angle_degrees: float) -> 'ExponentialMap':
        if axis.magnitude() == 0:
            return cls(Vector3(0, 0, 0))  # Tidak ada rotasi jika axis nol
        
        angle_rad = math.radians(angle_degrees)
        normalized_axis = axis.normalize()
        omega = normalized_axis * angle_rad

        return cls(omega)
    
    def get_axis_angle(self) -> tuple:
        angle_rad = self.omega.magnitude()
        angle_deg = math.degrees(angle_rad)

        if angle_rad == 0:
            return Vector3(0, 0, 1), 0.0
        
        axis = self.omega.normalize()
        return axis, angle_deg

    def to_rotation_matrix(self) -> list:
        angle = self.omega.magnitude()

        if angle == 0:
            return [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ]
        
        # Normalisasi rotasi axis
        axis = self.omega.normalize()

        # Skew-symmetric matrix
        K = [
            [0, -axis.z, axis.y],
            [axis.z, 0, -axis.x],
            [-axis.y, axis.x, 0]
        ]

        # Rodrigues' rotation formula: R = I + sin(theta) * K + (1 - cos(theta)) * K^2
        sin_angle = math.sin(angle)
        cos_angle = math.cos(angle)

        # Calculate K^2
        K_squared = self._multiply_matrices(K, K)

        # Rotation matrix
        R = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        for i in range(3):
            for j in range(3):
                I_ij = 1 if i == j else 0
                R[i][j] = I_ij + sin_angle * K[i][j] + (1 - cos_angle) * K_squared[i][j]
        
        return R
    
    def _multiply_matrices(self, A: list, B: list) -> list:
        result = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    result[i][j] += A[i][k] * B[k][j]
        
        return result
    
    def _apply_matrix(self, matrix: list, vector: Vector3) -> Vector3:
        x = matrix[0][0] * vector.x + matrix[0][1] * vector.y + matrix[0][2] * vector.z
        y = matrix[1][0] * vector.x + matrix[1][1] * vector.y + matrix[1][2] * vector.z
        z = matrix[2][0] * vector.x + matrix[2][1] * vector.y + matrix[2][2] * vector.z
        return Vector3(x, y, z)
    
    def rotate_vector(self, vector: Vector3) -> Vector3:
        if vector.magnitude() == 0:
            return Vector3(0, 0, 0)

        rotation_matrix = self.to_rotation_matrix()
        return self._apply_matrix(rotation_matrix, vector)
    
    def to_quaternion(self) -> Quaternion:
        axis, angle_deg = self.get_axis_angle()
        return Quaternion.from_axis_angle(axis, angle_deg)
    
    def get_logarithmic_coordinates(self) -> Vector3:
        return self.omega
    
    def get_so3_matrix(self) -> list:
        return [
            [0, -self.omega.z, self.omega.y],
            [self.omega.z, 0, -self.omega.x],
            [-self.omega.y, self.omega.x, 0]
        ]