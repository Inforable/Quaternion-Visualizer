import math

from .vector3 import Vector3
from .quaternion import Quaternion

class EulerAngle:
    ROTATION_ORDERS = ["XYZ", "XZY", "YXZ", "YZX", "ZXY", "ZYX"]

    def __init__(self, x_angle: float = 0.0, y_angle: float = 0.0, z_angle: float = 0.0, order: str = "XYZ"):
        self.x_angle = x_angle
        self.y_angle = y_angle
        self.z_angle = z_angle
        self.order = order.upper()

        if order not in self.ROTATION_ORDERS:
            raise ValueError(f"Urutan rotasi tidak valid, harus salah satu dari {self.ROTATION_ORDERS}")
    
    def __str__(self):
        return f"EulerAngle({self.x_angle:.3f}, {self.y_angle:.3f}, {self.z_angle:.3f}, order={self.order})"
    
    def __repr__(self):
        return self.__str__()
    
    def to_rotation_matrix(self) -> list:
        # Konversi ke radian
        x_rad = math.radians(self.x_angle)
        y_rad = math.radians(self.y_angle)
        z_rad = math.radians(self.z_angle)

        # Matriks rotasi untuk setiap sumbu
        Rx = [
            [1, 0, 0],
            [0, math.cos(x_rad), -math.sin(x_rad)],
            [0, math.sin(x_rad), math.cos(x_rad)]
        ]

        Ry = [
            [math.cos(y_rad), 0, math.sin(y_rad)],
            [0, 1, 0],
            [-math.sin(y_rad), 0, math.cos(y_rad)]
        ]

        Rz = [
            [math.cos(z_rad), -math.sin(z_rad), 0],
            [math.sin(z_rad), math.cos(z_rad), 0],
            [0, 0, 1]
        ]

        # Terapkan urutan rotasi
        if self.order == "XYZ":
            return self._multiply_matrices(self._multiply_matrices(Rz, Ry), Rx)
        elif self.order == "XZY":
            return self._multiply_matrices(self._multiply_matrices(Ry, Rz), Rx)
        elif self.order == "YXZ":
            return self._multiply_matrices(self._multiply_matrices(Rz, Rx), Ry)
        elif self.order == "YZX":
            return self._multiply_matrices(self._multiply_matrices(Rx, Rz), Ry)
        elif self.order == "ZXY":
            return self._multiply_matrices(self._multiply_matrices(Ry, Rx), Rz)
        elif self.order == "ZYX":
            return self._multiply_matrices(self._multiply_matrices(Rx, Ry), Rz)
        
    def _multiply_matrices(self, A: list, B: list) -> list:
        # Perkalian matriks A dan B
        result = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    result[i][j] += A[i][k] * B[k][j]
        return result

    def _apply_matrix(self, matrix: list, vector: Vector3) -> Vector3:
        # Terapkan matriks rotasi ke vektor
        x = matrix[0][0] * vector.x + matrix[0][1] * vector.y + matrix[0][2] * vector.z
        y = matrix[1][0] * vector.x + matrix[1][1] * vector.y + matrix[1][2] * vector.z
        z = matrix[2][0] * vector.x + matrix[2][1] * vector.y + matrix[2][2] * vector.z
        return Vector3(x, y, z)

    def rotate_vector(self, vector: Vector3) -> Vector3:
        # Rotasi vektor dengan Euler Angle
        if vector.magnitude() == 0:
            return Vector3(0, 0, 0)
        
        rotation_matrix = self.to_rotation_matrix()
        return self._apply_matrix(rotation_matrix, vector)

    def get_rotation_axes(self) -> list:
        # Mengambil sumbu rotasi berdasarkan urutan Euler Angle
        axes = []

        for char in self.order:
            if char == 'X':
                axes.append((Vector3(1, 0, 0), self.x_angle))
            elif char == 'Y':
                axes.append((Vector3(0, 1, 0), self.y_angle))
            elif char == 'Z':
                axes.append((Vector3(0, 0, 1), self.z_angle))
        
        return axes
    
    def to_quaternion(self) -> Quaternion:
        # Konversi tiap rotasi ke quaternion dan kalikan
        qx = Quaternion.from_axis_angle(Vector3(1, 0, 0), self.x_angle)
        qy = Quaternion.from_axis_angle(Vector3(0, 1, 0), self.y_angle)  
        qz = Quaternion.from_axis_angle(Vector3(0, 0, 1), self.z_angle)

        # terapkan urutan rotasi
        if self.order == "XYZ":
            return qz * qy * qx
        elif self.order == "XZY":
            return qy * qz * qx
        elif self.order == "YXZ":
            return qz * qx * qy
        elif self.order == "YZX":
            return qx * qz * qy
        elif self.order == "ZXY":
            return qy * qx * qz
        elif self.order == "ZYX":
            return qx * qy * qz
        
        return qx * qy * qz  # Default to XYZ