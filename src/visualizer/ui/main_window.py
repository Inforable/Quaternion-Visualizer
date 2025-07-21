import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit)
from PySide6.QtCore import Qt

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from visualizer.core.io.obj_loader import OBJLoader, OBJData

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
                  "Gunakan tombol di sebelah kiri untuk memuat file OBJ\n" \
                  "Objek yang dimuat akan ditampilkan di area output."
        
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
            self.display_obj_data()
        
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
