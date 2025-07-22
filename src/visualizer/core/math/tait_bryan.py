import math
from .vector3 import Vector3
from .quaternion import Quaternion

class TaitBryan:
    def __init__(self, roll: float = 0.0, pitch: float = 0.0, yaw: float = 0.0):
        self.roll = roll # Roll (X-axis rotation)
        self.pitch = pitch # Pitch (Y-axis rotation)
        self.yaw = yaw # Yaw (Z-axis rotation)
    
    def __str__(self):
        return f"TaitBryan(roll={self.roll:.3f}, pitch={self.pitch:.3f}, yaw={self.yaw:.3f})"

    def __repr__(self):
        return self.__str__()

    def to_rotation_matrix(self) -> list:
        # Konversi ke radian
        roll_rad = math.radians(self.roll)
        pitch_rad = math.radians(self.pitch)
        yaw_rad = math.radians(self.yaw)

        # Prekomputasi nilai trigonometri
        cr = math.cos(roll_rad)
        sr = math.sin(roll_rad)
        cp = math.cos(pitch_rad)
        sp = math.sin(pitch_rad)
        cy = math.cos(yaw_rad)
        sy = math.sin(yaw_rad)

        # Matriks rotasi Tait-Bryan (Roll-Pitch-Yaw)
        R = [
            [cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr],
            [sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr],
            [-sp, cp * sr, cp * cr]
        ]
        return R

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
    
    def get_rotation_sequence(self) -> list:
        return [
            (Vector3(0, 0, 1), self.yaw, "Yaw"),
            (Vector3(1, 0, 0), self.pitch, "Pitch"),
            (Vector3(0, 1, 0), self.roll, "Roll")
        ]
    
    def to_quaternion(self) -> Quaternion:
        # Konversi ke radian
        roll_rad = math.radians(self.roll)
        pitch_rad = math.radians(self.pitch)
        yaw_rad = math.radians(self.yaw)

        # Prekomputasi nilai trigonometri
        cr = math.cos(roll_rad / 2.0)
        sr = math.sin(roll_rad / 2.0)
        cp = math.cos(pitch_rad / 2.0)
        sp = math.sin(pitch_rad / 2.0)
        cy = math.cos(yaw_rad / 2.0)
        sy = math.sin(yaw_rad / 2.0)

        # Komponen quaternion
        w = cr * cp * cy + sr * sp * sy
        x = sr * cp * cy - cr * sp * sy
        y = cr * sp * cy + sr * cp * sy
        z = cr * cp * sy - sr * sp * cy

        return Quaternion(w, x, y, z)
    
    def get_aircraft_orientation(self) -> dict:
        return {
            "roll": f"{self.roll:.1f}° {'left' if self.roll < 0 else 'right'}",
            "pitch": f"{self.pitch:.1f}° {'down' if self.pitch < 0 else 'up'}",  
            "yaw": f"{self.yaw:.1f}° {'left' if self.yaw < 0 else 'right'}"
        }
