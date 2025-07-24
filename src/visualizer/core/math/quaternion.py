import math

from .vector3 import Vector3

class Quaternion:
    def __init__(self, w:float = 1.0, x:float = 0.0, y:float = 0.0, z:float = 0.0):
        self.w = w
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return f"Quaternion({self.w:.3f}, {self.x:.3f}, {self.y:.3f}, {self.z:.3f})"
    
    def __repr__(self):
        return self.__str__()
    
    @staticmethod
    def from_axis_angle(axis: Vector3, angle_degrees: float) -> 'Quaternion':
        # Cek apakah axis rotasi adalah nol
        if axis.magnitude() == 0:
            raise ValueError("Axis rotasi tidak boleh nol.")

        # Konversi sudut dari derajat ke radian
        angle_rad = math.radians(angle_degrees)
        half_angle = angle_rad / 2.0

        normalized_axis = axis.normalize()

        # Menghitung komponen quaternion
        sin_half_angle = math.sin(half_angle)
        cos_half_angle = math.cos(half_angle)

        return Quaternion(
            w=cos_half_angle,
            x=normalized_axis.x * sin_half_angle,
            y=normalized_axis.y * sin_half_angle,
            z=normalized_axis.z * sin_half_angle
        )
    
    def __mul__(self, other) -> 'Quaternion':
        w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
        x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
        y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
        z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
        return Quaternion(w, x, y, z)

    def conjugate(self) -> 'Quaternion':
        return Quaternion(self.w, -self.x, -self.y, -self.z)
    
    def magnitude(self) -> float:
        return math.sqrt(self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def normalize(self) -> 'Quaternion':
        mag = self.magnitude()
        # Jika magnitudo adalah nol, kembalikan quaternion nol
        if mag == 0:
            return Quaternion(0, 0, 0, 0)
        
        return Quaternion(self.w / mag, self.x / mag, self.y / mag, self.z / mag)
    
    def rotate_vector(self, vector: Vector3) -> Vector3:
        # Cek apakah vector yang diberikan adalah nol
        if vector.magnitude() == 0:
            return Vector3(0, 0, 0)
        
        # Konversi vector ke quaternion
        vector_quat = Quaternion(0, vector.x, vector.y, vector.z)

        # Rotasi vector dengan quaternion
        rotated_vector_quat = self * vector_quat * self.conjugate()

        return Vector3(rotated_vector_quat.x, rotated_vector_quat.y, rotated_vector_quat.z)
    
    def to_axis_angle(self) -> tuple[Vector3, float]:
        # Normalisasi quaternion
        q = self.normalize()

        # Cek apakah w mendekati 1 atau -1
        if abs(q.w) >= 1.0:
            return Vector3(0, 0, 1), 0.0

        # Hitung sudut rotasi
        angle_rad = 2 * math.acos(abs(q.w))
        angle_degrees = math.degrees(angle_rad)

        # Hitung axis rotasi
        sin_half_angle = math.sqrt(1.0 - q.w ** 2)

        # Jika sin_half_angle adalah nol, axis rotasi tidak terdefinisi
        if sin_half_angle < 1e-6:
            return Vector3(1, 0, 0), angle_degrees
        
        axis = Vector3(q.x / sin_half_angle, q.y / sin_half_angle, q.z / sin_half_angle)

        return axis.normalize(), angle_degrees

    def copy(self) -> 'Quaternion':
        return Quaternion(self.w, self.x, self.y, self.z)