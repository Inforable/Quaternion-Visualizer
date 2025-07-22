from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QDoubleSpinBox
from PySide6.QtGui import QFont

from ...core.math.vector3 import Vector3
from ...core.math.exponential_map import ExponentialMap

class ExponentialControls(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QGridLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(2)
        
        # Info label
        info_label = QLabel("Rotation Vector (ω):")
        info_label.setFont(QFont("Arial", 9))
        layout.addWidget(info_label, 0, 0, 1, 2)
        
        # Omega X
        x_label = QLabel("ωx (rad):")
        x_label.setFont(QFont("Arial", 8))
        layout.addWidget(x_label, 1, 0)
        self.omega_x_spin = QDoubleSpinBox()
        self.omega_x_spin.setRange(-10.0, 10.0)
        self.omega_x_spin.setValue(0.0)
        self.omega_x_spin.setSingleStep(0.1)
        self.omega_x_spin.setDecimals(3)
        self.omega_x_spin.setMaximumHeight(18)
        layout.addWidget(self.omega_x_spin, 1, 1)
        
        # Omega Y
        y_label = QLabel("ωy (rad):")
        y_label.setFont(QFont("Arial", 8))
        layout.addWidget(y_label, 2, 0)
        self.omega_y_spin = QDoubleSpinBox()
        self.omega_y_spin.setRange(-10.0, 10.0)
        self.omega_y_spin.setValue(0.0)
        self.omega_y_spin.setSingleStep(0.1)
        self.omega_y_spin.setDecimals(3)
        self.omega_y_spin.setMaximumHeight(18)
        layout.addWidget(self.omega_y_spin, 2, 1)
        
        # Omega Z
        z_label = QLabel("ωz (rad):")
        z_label.setFont(QFont("Arial", 8))
        layout.addWidget(z_label, 3, 0)
        self.omega_z_spin = QDoubleSpinBox()
        self.omega_z_spin.setRange(-10.0, 10.0)
        self.omega_z_spin.setValue(0.785)  # π/4 ≈ 45°
        self.omega_z_spin.setSingleStep(0.1)
        self.omega_z_spin.setDecimals(3)
        self.omega_z_spin.setMaximumHeight(18)
        layout.addWidget(self.omega_z_spin, 3, 1)
    
    def get_rotation(self):
        omega = Vector3(
            self.omega_x_spin.value(),
            self.omega_y_spin.value(),
            self.omega_z_spin.value()
        )
        return ExponentialMap(omega)