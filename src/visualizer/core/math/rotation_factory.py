from enum import Enum
from .vector3 import Vector3
from .quaternion import Quaternion
from .euler_angle import EulerAngle
from .tait_bryan import TaitBryan
from .exponential_map import ExponentialMap
from ..io.obj_loader import OBJData

class RotationMethod(Enum):
    QUATERNION = "Quaternion"
    EULER_ANGLE = "Euler Angle"
    TAIT_BRYAN = "Tait-Bryan"
    EXPONENTIAL_MAP = "Exponential Map"

class RotationFactory:
    @staticmethod
    def create_rotation(method: RotationMethod, **kwargs):
        if method == RotationMethod.QUATERNION:
            axis = kwargs.get('axis', Vector3(0, 0, 1))
            angle = kwargs.get('angle', 0.0)
            return Quaternion.from_axis_angle(axis, angle)
        elif method == RotationMethod.EULER_ANGLE:
            x_angle = kwargs.get('x_angle', 0.0)
            y_angle = kwargs.get('y_angle', 0.0)
            z_angle = kwargs.get('z_angle', 0.0)
            order = kwargs.get('order', 'XYZ')
            return EulerAngle(x_angle, y_angle, z_angle, order)
        elif method == RotationMethod.TAIT_BRYAN:
            roll = kwargs.get('roll', 0.0)
            pitch = kwargs.get('pitch', 0.0)
            yaw = kwargs.get('yaw', 0.0)
            return TaitBryan(roll, pitch, yaw)
        elif method == RotationMethod.EXPONENTIAL_MAP:
            omega = kwargs.get('omega', Vector3(0, 0, 0))
            return ExponentialMap(omega)
        else:
            raise ValueError(f"Method tidak valid: {method}")
    
    @staticmethod
    def rotate_obj_data(obj_data: OBJData, rotation_obj, method: RotationMethod) -> OBJData:
        if not obj_data or not obj_data.vertices:
            raise ValueError("OBJ data yang tersedia tidak valid atau tidak memiliki vertex.")
        
        rotated_data = OBJData()
        rotated_data.filename = f"{obj_data.filename}_rotated_{method.value}"
        rotated_data.faces = obj_data.faces.copy()

        for vertex in obj_data.vertices:
            vector = Vector3(vertex.x, vertex.y, vertex.z)

            # Sesuaikan rotasi berdasarkan metode
            if method == RotationMethod.QUATERNION:
                rotated_vector = rotation_obj.rotate_vector(vector)
            elif method == RotationMethod.EULER_ANGLE:
                rotated_vector = rotation_obj.rotate_vector(vector)
            elif method == RotationMethod.TAIT_BRYAN:
                rotated_vector = rotation_obj.rotate_vector(vector)
            elif method == RotationMethod.EXPONENTIAL_MAP:
                rotated_vector = rotation_obj.rotate_vector(vector)
            else:
                rotated_vector = vector
            
            rotated_vertex = rotated_vector.to_vertex()
            rotated_data.vertices.append(rotated_vertex)
        
        return rotated_data
    
    @staticmethod
    def get_rotation_info(rotation_obj, method: RotationMethod) -> str:
        info = f"Method: {method.value}\n"
        info += f"Rotation Object: {rotation_obj}\n"

        if method == RotationMethod.QUATERNION:
            axis, angle = rotation_obj.to_axis_angle()
            info += f"Equivalent axis-angle: {axis}, {angle:.1f}°\n"
        
        elif method == RotationMethod.EULER_ANGLES:
            axes = rotation_obj.get_rotation_axes()
            info += f"Rotation sequence ({rotation_obj.order}):\n"
            for i, (axis, angle) in enumerate(axes):
                info += f"  {i+1}. {axis} @ {angle:.1f}°\n"
        
        elif method == RotationMethod.TAIT_BRYAN:
            orientation = rotation_obj.get_aircraft_orientation()
            info += f"Aircraft orientation:\n"
            info += f"  Roll: {orientation['roll']}\n"
            info += f"  Pitch: {orientation['pitch']}\n" 
            info += f"  Yaw: {orientation['yaw']}\n"
        
        elif method == RotationMethod.EXPONENTIAL_MAP:
            axis, angle = rotation_obj.get_axis_angle()
            omega = rotation_obj.get_logarithmic_coordinates()
            info += f"Rotation vector: {omega}\n"
            info += f"Equivalent axis-angle: {axis}, {angle:.1f}°\n"
        
        return info

    @staticmethod
    def get_visualization_data(rotation_obj, method: RotationMethod) -> dict:
        viz_data = {
            'method': method,
            'axes': [],
            'angles': [],
            'colors': []
        }

        if method == RotationMethod.QUATERNION:
            axis, angle = rotation_obj.to_axis_angle()
            viz_data['axes'] = [axis]
            viz_data['angles'] = [angle]
            viz_data['colors'] = [(1.0, 1.0, 0.0)]
        
        elif method == RotationMethod.EULER_ANGLES:
            rotation_axes = rotation_obj.get_rotation_axes()
            colors = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]
            
            for i, (axis, angle) in enumerate(rotation_axes):
                if abs(angle) > 0.1:
                    viz_data['axes'].append(axis)
                    viz_data['angles'].append(angle)
                    viz_data['colors'].append(colors[i % 3])
        
        elif method == RotationMethod.TAIT_BRYAN:
            sequence = rotation_obj.get_rotation_sequence()
            colors = [(0.0, 1.0, 1.0), (1.0, 0.0, 1.0), (1.0, 1.0, 0.0)]
            
            for i, (axis, angle, name) in enumerate(sequence):
                if abs(angle) > 0.1:
                    viz_data['axes'].append(axis)
                    viz_data['angles'].append(angle)
                    viz_data['colors'].append(colors[i])
        
        elif method == RotationMethod.EXPONENTIAL_MAP:
            axis, angle = rotation_obj.get_axis_angle()
            viz_data['axes'] = [axis]
            viz_data['angles'] = [angle]
            viz_data['colors'] = [(0.5, 1.0, 0.5)]
        
        return viz_data