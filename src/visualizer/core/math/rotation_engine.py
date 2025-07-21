import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from .vector3 import Vector3
from .quaternion import Quaternion
from ..io.obj_loader import OBJLoader, OBJData

class RotationEngine:
    @staticmethod
    def rotate_obj_data(obj_data: OBJData, axis: Vector3, angle_degress: float) -> OBJData:
        rotation_quat = Quaternion.from_axis_angle(axis, angle_degress)

        rotated_data = OBJData()
        rotated_data.filename = f"{obj_data.filename}_rotated_{angle_degress}deg"
        rotated_data.faces = obj_data.faces.copy()

        for vertex in obj_data.vertices:
            vector = Vector3(vertex.x, vertex.y, vertex.z)
            rotated_vector = rotation_quat.rotate_vector(vector)
            rotated_vertex = rotated_vector.to_vertex()
            rotated_data.vertices.append(rotated_vertex)
        
        return rotated_data
    
    @staticmethod
    def get_rotation_info(exis: Vector3, angle_degress: float) -> str:
        quat = Quaternion.from_axis_angle(exis, angle_degress)
        axis_norm = exis.normalize()

        info += f"Axis: {axis_norm}\n"
        info += f"Angle: {angle_degress} degrees\n"
        info += f"Quaternion: {quat}\n"

        return info
            