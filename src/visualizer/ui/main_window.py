import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit, QDoubleSpinBox, QSpinBox)
from PySide6.QtCore import Qt

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from visualizer.core.io.obj_loader import OBJLoader, OBJData
from visualizer.core.math.vector3 import Vector3
from visualizer.core.math.quaternion import Quaternion
from visualizer.core.math.rotation_engine import RotationEngine

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_obj_data: OBJData = None
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Quaternion Visualizer")
        self.setGeometry(100, 100, 1000, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout()

        # Left panel for controls
        controls = QWidget()
        controls.setFixedWidth(250)
        controls_layout = QVBoxLayout()

        # Load OBJ button
        self.load_button = QPushButton("Memuat File OBJ")
        self.load_button.clicked.connect(self.load_obj_file)
        controls_layout.addWidget(self.load_button)

        # Status label
        self.status_label = QLabel("Status: Tidak ada file yang dimuat.")
        self.status_label.setWordWrap(True)
        controls_layout.addWidget(self.status_label)

        controls_layout.addWidget(QLabel("Kontrol"))

        # Input Axis x
        controls_layout.addWidget(QLabel("Input Axis X:"))
        self.axis_x = QDoubleSpinBox()
        self.axis_x.setRange(-10.0, 10.0)
        self.axis_x.setValue(0.0)
        self.axis_x.setDecimals(2)
        controls_layout.addWidget(self.axis_x)

        # Input Axis y
        controls_layout.addWidget(QLabel("Input Axis Y:"))
        self.axis_y = QDoubleSpinBox()
        self.axis_y.setRange(-10.0, 10.0)
        self.axis_y.setValue(0.0)
        self.axis_y.setDecimals(2)
        controls_layout.addWidget(self.axis_y)

        # Input Axis z
        controls_layout.addWidget(QLabel("Input Axis Z:"))
        self.axis_z = QDoubleSpinBox()
        self.axis_z.setRange(-10.0, 10.0)
        self.axis_z.setValue(0.0)
        self.axis_z.setDecimals(2)
        controls_layout.addWidget(self.axis_z)

        # Input Angle
        controls_layout.addWidget(QLabel("Input Angle (derajat):"))
        self.angle_input = QSpinBox()
        self.angle_input.setRange(-360, 360)
        self.angle_input.setValue(45)
        controls_layout.addWidget(self.angle_input)

        # Tombol Rotation
        self.rotate_button = QPushButton("Rotasi Objek")
        self.rotate_button.clicked.connect(self.apply_rotation)
        self.rotate_button.setEnabled(False) # False selama tidak ada file dimuat
        controls_layout.addWidget(self.rotate_button)

        # Tombol reset
        self.reset_button = QPushButton("Reset Objek")
        self.reset_button.clicked.connect(self.reset_object)
        self.reset_button.setEnabled(False) # False selama tidak ada file dimuat
        controls_layout.addWidget(self.reset_button)

        # Set layout ke controls
        controls.setLayout(controls_layout)

        # Right panel for output
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        # Layout
        main_layout.addWidget(controls)
        main_layout.addWidget(self.output_text)
        central_widget.setLayout(main_layout)

        # Initial text
        self.show_welcome_message()
    
    def show_welcome_message(self):
        welcome = "Selamat datang di Quaternion Visualizer!\n\n" \
                  "Cara menggunakan:\n" \
                    "1. Klik 'Memuat File OBJ' untuk memuat file OBJ.\n" \
                    "2. Atur rotasi axis (x, y, z) dan sudut rotasi.\n" \
                    "3. Klik 'Apply Rotation' untuk menerapkan rotasi.\n" \
                    "4. Output akan ditampilkan di panel kanan.\n\n" \
        
        self.output_text.setText(welcome)
    
    def load_obj_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Pilih File OBJ",
            "",
            "File OBJ (*.obj);;All File (*)"
        )

        if file_path:
            self.load_obj_from_path(file_path)
    
    def load_obj_from_path(self, file_path: str):
        try:
            self.current_obj_data = OBJLoader.load_obj(file_path)
            self.status_label.setText(f"Status: Berhasil memuat {self.current_obj_data.filename}")
            
            self.rotate_button.setEnabled(True)
        
        except FileNotFoundError as e:
            self.status_label.setText(f"Status: {str(e)}")
            self.output_text.setText("Error: File tidak ditemukan.")
        except Exception as e:
            self.status_label.setText("Status: Terjadi kesalahan saat memuat file.")
            self.output_text.setText(f"Error: {str(e)}")
    
    def display_obj_data(self):
        if not self.current_obj_data:
            return
        
        output = f"File: {self.current_obj_data.filename}\n\n"

        # Display vertices
        output += "Vertices:\n"
        for i, vertex in enumerate(self.current_obj_data.vertices[:10]):
            output += f"v{i:3d}: {vertex}\n"
        
        if len(self.current_obj_data.vertices) > 10:
            output += f"... dan {len(self.current_obj_data.vertices) - 10} vertex lainnya.\n\n"
        
        # Display faces
        output += "Faces:\n"
        for i, face in enumerate(self.current_obj_data.faces[:10]):
            output += f"f{i:3d}: {face}\n"

        if len(self.current_obj_data.faces) > 10:
            output += f"... dan {len(self.current_obj_data.faces) - 10} face lainnya.\n"
        
        if self.current_obj_data.get_attributes():
            min_x = min(v.x for v in self.current_obj_data.vertices)
            max_x = max(v.x for v in self.current_obj_data.vertices)
            min_y = min(v.y for v in self.current_obj_data.vertices)
            max_y = max(v.y for v in self.current_obj_data.vertices)
            min_z = min(v.z for v in self.current_obj_data.vertices)
            max_z = max(v.z for v in self.current_obj_data.vertices)

            output += f"\nAttributes:\n" \
                        f"Jumlah Vertices: {len(self.current_obj_data.vertices)}\n" \
                        f"Jumlah Faces: {len(self.current_obj_data.faces)}\n" \
                        f"Rentang X: {min_x:.2f} - {max_x:.2f}\n" \
                        f"Rentang Y: {min_y:.2f} - {max_y:.2f}\n" \
                        f"Rentang Z: {min_z:.2f} - {max_z:.2f}\n"

        output += f"Berhasil memuat file: {self.current_obj_data.filename}\n"

        self.output_text.setText(output)
    
    def apply_rotation(self):
        if not self.current_obj_data:
            self.output_text.setText("Error: Tidak ada file yang dimuat.")
            return

        axis = Vector3(
            self.axis_x.value(),
            self.axis_y.value(),
            self.axis_z.value()
        )
        angle = self.angle_input.value()

        # Validasi axis
        if axis.magnitude() == 0:
            self.output_text.setText("Error: Axis tidak boleh nol.")
            return
        
        try:
            # Terapkan rotasi quaternion
            rotated_data = RotationEngine.rotate_obj_data(self.current_obj_data, axis, angle)

            # Tampilkan hasil rotasi
            output = ""
            output += f"Hasil rotasi:\n"
            output += RotationEngine.get_rotation_info(axis, angle)

            # Perbandingan sebelum dan sesudah
            output += "Perbandingan 5 vertices awal\n"
            for i in range(min(5, len(self.current_obj_data.vertices))):
                orig = self.current_obj_data.vertices[i]
                rot = rotated_data.vertices[i]
                output += f"v{i}: {orig}\n"
                output += f"    → {rot}\n"
            
            if len(self.current_obj_data.vertices) > 5:
                output += f"... dan {len(self.current_obj_data.vertices) - 5} vertices lainnya.\n"
            
            self.output_text.setText(output)
            self.reset_button.setEnabled(True)

            # Update data
            self.current_obj_data = rotated_data
        
        except Exception as e:
            error = f"Error saat menerapkan rotasi: {str(e)}"
            self.output_text.setText(error)
    
    def reset_object(self):
        if hasattr(self, 'original_obj_data') and self.original_obj_data:
            self.current_obj_data = OBJData()
            self.current_obj_data.filename = self.original_obj_data.filename
            self.current_obj_data.vertices = [v for v in self.original_obj_data.vertices]
            self.current_obj_data.faces = [f for f in self.original_obj_data.faces]
            
            self.status_label.setText(f"Status: Objek telah direset ke {self.current_obj_data.filename}")
            self.output_text.setText("Objek telah direset.")
        else:
            self.status_label.setText("Status: Tidak ada objek yang dimuat untuk direset.")
            self.output_text.setText("Error: Tidak ada objek yang dimuat untuk direset.")

