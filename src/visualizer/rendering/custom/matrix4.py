import math
from typing import List, Tuple, Union

class Matrix4:
    def __init__(self, matrix=None):
        if matrix is None:
            # Identity matrix
            self.m = [
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]
            ]
        else:
            self.m = [row[:] for row in matrix]
    
    @staticmethod
    def identity():
        return Matrix4()
    
    @staticmethod
    def translation(x: float, y: float, z: float):
        matrix = Matrix4()
        matrix.m[0][3] = x
        matrix.m[1][3] = y
        matrix.m[2][3] = z
        return matrix
    
    def translate(self, x: float, y: float, z: float):
        trans_matrix = Matrix4.translation(x, y, z)
        result = self.multiply_matrix(trans_matrix)
        self.m = result.m

    @staticmethod
    def rotation_x(angle_deg: float):
        angle_rad = math.radians(angle_deg)
        cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)

        return Matrix4([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, cos_a, -sin_a, 0.0],
            [0.0, sin_a, cos_a, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
    
    @staticmethod
    def rotation_y(angle_deg: float):
        angle_rad = math.radians(angle_deg)
        cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)

        return Matrix4([
            [cos_a, 0.0, sin_a, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [-sin_a, 0.0, cos_a, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
    
    @staticmethod
    def rotation_z(angle_deg: float):
        angle_rad = math.radians(angle_deg)
        cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)

        return Matrix4([
            [cos_a, -sin_a, 0.0, 0.0],
            [sin_a, cos_a, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
    
    @staticmethod
    def scale(sx: float, sy: float, sz: float):
        return Matrix4([
            [sx, 0.0, 0.0, 0.0],
            [0.0, sy, 0.0, 0.0],
            [0.0, 0.0, sz, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
    
    @staticmethod
    def perspective(fov_deg: float, aspect: float, near: float, far: float):
        fov_rad = math.radians(fov_deg)
        f = 1.0 / math.tan(fov_rad / 2.0)

        return Matrix4([
            [f / aspect, 0.0, 0.0, 0.0],
            [0.0, f, 0.0, 0.0],
            [0.0, 0.0, (far + near) / (near - far), (2 * far * near) / (near - far)],
            [0.0, 0.0, -1.0, 0.0]
        ])
    
    @staticmethod
    def look_at(eye: List[float], center: List[float], up: List[float]):
        # Calculate camera coordinate system
        f = [center[i] - eye[i] for i in range(3)]  # Forward vector
        f_len = math.sqrt(sum(x * x for x in f))
        if f_len > 0:
            f = [x / f_len for x in f]

        # Right = forward x up
        right = [
            f[1] * up[2] - f[2] * up[1],
            f[2] * up[0] - f[0] * up[2],
            f[0] * up[1] - f[1] * up[0]
        ]

        right_len = math.sqrt(sum(x * x for x in right))
        if right_len > 0:
            right = [x / right_len for x in right]
        
        # Up = right x forward
        up_corrected = [
            right[1] * f[2] - right[2] * f[1],
            right[2] * f[0] - right[0] * f[2],
            right[0] * f[1] - right[1] * f[0]
        ]

        # Create view matrix
        return Matrix4([
            [right[0], up_corrected[0], -f[0], -(right[0]*eye[0] + right[1]*eye[1] + right[2]*eye[2])],
            [right[1], up_corrected[1], -f[1], -(up_corrected[0]*eye[0] + up_corrected[1]*eye[1] + up_corrected[2]*eye[2])],
            [right[2], up_corrected[2], -f[2], -(-f[0]*eye[0] + -f[1]*eye[1] + -f[2]*eye[2])],
            [0.0, 0.0, 0.0, 1.0]
        ])
    
    def multiply_matrix(self, other):
        result = Matrix4()
        for i in range(4):
            for j in range(4):
                result.m[i][j] = 0.0
                for k in range(4):
                    result.m[i][j] += self.m[i][k] * other.m[k][j]
        return result
    
    def multiply(self, other):
        return self.multiply_matrix(other)
    
    def multiply_vector(self, vector: List[float]) -> List[float]:
        if len(vector) == 3:
            vector = vector + [1.0]  # Convert to homogeneous

        x, y, z, w = vector

        return [
            self.m[0][0]*x + self.m[0][1]*y + self.m[0][2]*z + self.m[0][3]*w,
            self.m[1][0]*x + self.m[1][1]*y + self.m[1][2]*z + self.m[1][3]*w,
            self.m[2][0]*x + self.m[2][1]*y + self.m[2][2]*z + self.m[2][3]*w,
            self.m[3][0]*x + self.m[3][1]*y + self.m[3][2]*z + self.m[3][3]*w
        ]
    
    def __mul__(self, other):
        if isinstance(other, Matrix4):
            return self.multiply_matrix(other)
        elif isinstance(other, list):
            return self.multiply_vector(other)
        else:
            raise TypeError("Unsupported type for Matrix4 multiplication")
    
    def __str__(self):
        result = "Matrix4:\n"
        for row in self.m:
            result += f"[{', '.join(f'{x:8.3f}' for x in row)}]\n"
        return result