from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QDoubleSpinBox, QComboBox
from PySide6.QtGui import QFont

from ...core.math.euler_angle import EulerAngle

class EulerControls(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QGridLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(2)
        
        # Rotation order
        order_label = QLabel("Rotation Order:")
        order_label.setFont(QFont("Arial", 9))
        layout.addWidget(order_label, 0, 0)
        self.order_combo = QComboBox()
        self.order_combo.addItems(EulerAngle.ROTATION_ORDERS)
        self.order_combo.setMaximumHeight(18)
        layout.addWidget(self.order_combo, 0, 1)
        
        # X rotation
        x_label = QLabel("X Rotation (°):")
        x_label.setFont(QFont("Arial", 8))
        layout.addWidget(x_label, 1, 0)
        self.x_angle_spin = QDoubleSpinBox()
        self.x_angle_spin.setRange(-360.0, 360.0)
        self.x_angle_spin.setValue(0.0)
        self.x_angle_spin.setSingleStep(1.0)
        self.x_angle_spin.setDecimals(1)
        self.x_angle_spin.setMaximumHeight(18)
        layout.addWidget(self.x_angle_spin, 1, 1)
        
        # Y rotation
        y_label = QLabel("Y Rotation (°):")
        y_label.setFont(QFont("Arial", 8))
        layout.addWidget(y_label, 2, 0)
        self.y_angle_spin = QDoubleSpinBox()
        self.y_angle_spin.setRange(-360.0, 360.0)
        self.y_angle_spin.setValue(0.0)
        self.y_angle_spin.setSingleStep(1.0)
        self.y_angle_spin.setDecimals(1)
        self.y_angle_spin.setMaximumHeight(18)
        layout.addWidget(self.y_angle_spin, 2, 1)
        
        # Z rotation
        z_label = QLabel("Z Rotation (°):")
        z_label.setFont(QFont("Arial", 8))
        layout.addWidget(z_label, 3, 0)
        self.z_angle_spin = QDoubleSpinBox()
        self.z_angle_spin.setRange(-360.0, 360.0)
        self.z_angle_spin.setValue(45.0)
        self.z_angle_spin.setSingleStep(1.0)
        self.z_angle_spin.setDecimals(1)
        self.z_angle_spin.setMaximumHeight(18)
        layout.addWidget(self.z_angle_spin, 3, 1)
    
    def get_rotation(self):
        return EulerAngle(
            self.x_angle_spin.value(),
            self.y_angle_spin.value(),
            self.z_angle_spin.value(),
            self.order_combo.currentText()
        )