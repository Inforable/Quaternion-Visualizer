from typing import List
import os

# Kelas untuk vertex
class Vertex:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return f"Vertex({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"

    def __repr__(self):
        return self.__str__()

# Kelas untuk face
class Face:
    def __init__(self, vertex_indices: List[int]):
        self.vertex_indices = vertex_indices # Dari index 0

    def __str__(self):
        return f"Face({self.vertex_indices})"

# Kelas untuk data OBJ
class OBJData:
    def __init__(self):
        self.vertices: List[Vertex] = []
        self.faces: List[Face] = []
        self.filename: str = ""

    def get_attributes(self) -> str:
        return f"Vertices: {len(self.vertices)}, Faces: {len(self.faces)}, File: {self.filename}"

# Kelas untuk loader file OBJ
class OBJLoader:
    @staticmethod
    def load_obj(file_path: str) -> OBJData:
        obj_data = OBJData()
        obj_data.filename = os.path.basename(file_path)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f" File {file_path} tidak ditemukan.")

        try:
            with open(file_path, 'r') as file:
                line_number = 0
                for line in file:
                    line_number += 1
                    line = line.strip()

                    # Skip untuk baris kosong atau komentar
                    if not line or line.startswith('#'):
                        continue

                    parts = line.split()
                    if not parts:
                        continue

                    # Parse untuk vartices
                    if parts[0] == 'v':
                        if len(parts) < 4:
                            print(f"Warning: Baris {line_number} tidak valid untuk vertex: {line}")
                            continue
                        try:
                            x = float(parts[1])
                            y = float(parts[2])
                            z = float(parts[3])
                            obj_data.vertices.append(Vertex(x, y, z))
                        except ValueError:
                            print(f"Warning: Baris {line_number} tidak valid untuk vertex: {line}")
                    
                    # Parse untuk faces
                    elif parts[0] == 'f':
                        if len(parts) < 4:
                            print(f"Warning: Baris {line_number} tidak valid untuk face: {line}")
                            continue
                        try:
                            face_indices = []
                            for i in range(1, len(parts)):
                                # Handle untuk tiap format yang berbeda : "1", "1/1", "1/1/1", "1//1"
                                vertex_str = parts[i].split('/')[0]  # Ambil index vertex saja
                                vertex_index = int(vertex_str) - 1 # Konversi ke index 0

                                # Validasi index
                                if vertex_index < 0:
                                    raise ValueError(f"Index vertex tidak valid: {vertex_index + 1} pada baris {line_number}")
                                
                                face_indices.append(vertex_index)
                            
                            obj_data.faces.append(Face(face_indices))
                        except (ValueError, IndexError):
                            print(f"Warning: Baris {line_number} tidak valid untuk face: {line}")
                    
        except Exception as e:
            raise Exception(f"Error saat membaca file {file_path}: {e}")
        
        # Validasi data yang dimuat
        OBJLoader._validate_obj_data(obj_data)

        print(f"File {file_path} berhasil dimuat.")
        print(obj_data.get_attributes())
        return obj_data

    @staticmethod
    def _validate_obj_data(obj_data: OBJData):
        max_vertex_index = len(obj_data.vertices) - 1 # dari index 0

        for i, face in enumerate(obj_data.faces):
            for vertex_index in face.vertex_indices:
                if vertex_index > max_vertex_index:
                    print(f"Warning: Face {i} mengandung index vertex tidak valid: {vertex_index + 1}")
    
    @staticmethod
    def save_obj(obj_data: OBJData, file_path: str):
        try:
            with open(file_path, 'w') as file:
                file.write(f'# Result from {obj_data.filename}\n')

                # Write vertices
                for vertex in obj_data.vertices:
                    file.write(f'v {vertex.x:.6f} {vertex.y:.6f} {vertex.z:.6f}\n')
                
                file.write('\n')

                # Write faces
                for face in obj_data.faces:
                    face_str = ' '.join(str(index + 1) for index in face.vertex_indices)
                    file.write(f'f {face_str}\n')

            print(f"File {file_path} berhasil disimpan.")
        except Exception as e:
            raise Exception(f"Error saat menyimpan file {file_path}: {e}")