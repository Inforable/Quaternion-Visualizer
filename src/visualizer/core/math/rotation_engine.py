from .vector3 import Vector3
from .quaternion import Quaternion
from ..io.obj_loader import OBJLoader, OBJData

class RotationEngine:
    @staticmethod
    def rotate_obj_data(obj_data: OBJData, axis: Vector3, angle_degrees: float) -> OBJData:
        # Cek apakah obj_data valid
        if not obj_data or not obj_data.vertices:
            raise ValueError("OBJJ data yang tersedia tidak valid atau tidak memiliki vertex.")

        # Cek apakah axis rotasi adalah nol
        if axis.magnitude() == 0:
            raise ValueError("Axis rotasi tidak boleh nol.")

        rotation_quat = Quaternion.from_axis_angle(axis, angle_degrees)

        rotated_data = OBJData()
        rotated_data.filename = f"{obj_data.filename}_rotated_{angle_degrees:.1f}deg"

        rotated_data.faces = obj_data.faces.copy()

        for vertex in obj_data.vertices:
            vector = Vector3(vertex.x, vertex.y, vertex.z)
            rotated_vector = rotation_quat.rotate_vector(vector)
            rotated_vertex = rotated_vector.to_vertex()
            rotated_data.vertices.append(rotated_vertex)
        
        return rotated_data
    
    @staticmethod
    def get_rotation_info(axis: Vector3, angle_degrees: float) -> str:
        # Cek apakah axis rotasi adalah nol
        if axis.magnitude() == 0:
            return "Axis rotasi tidak boleh nol."
        
        quat = Quaternion.from_axis_angle(axis, angle_degrees)
        axis_norm = axis.normalize()

        info = f"Rotasi:\n"
        info += f"Axis: {axis_norm}\n"
        info += f"Angle: {angle_degrees} degrees\n"
        info += f"Quaternion: {quat}\n"

        return info
    
    @staticmethod
    def validate_rotation_parameters(axis: Vector3, angle_degrees: float) -> tuple[bool, str]:
        if axis is None:
            return False, "Axis rotasi tidak boleh None."

        if axis.magnitude() == 1e-10:
            return False, "Axis rotasi tidak boleh mendekati nol."
        
        if not isinstance(angle_degrees, (int, float)):
            return False, "Sudut rotasi harus berupa angka (int atau float)."

        return True, "Parameter valid."
            