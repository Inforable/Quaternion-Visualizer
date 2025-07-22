from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QDoubleSpinBox
from PySide6.QtGui import QFont

from ...core.math.vector3 import Vector3
from ...core.math.quaternion import Quaternion

class QuaternionControls(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QGridLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(2)
        
        # Axis controls
        axis_label = QLabel("Rotation Axis:")
        axis_label.setFont(QFont("Arial", 9))
        layout.addWidget(axis_label, 0, 0, 1, 2)
        
        # X axis
        x_label = QLabel("X:")
        x_label.setFont(QFont("Arial", 8))
        layout.addWidget(x_label, 1, 0)
        self.axis_x_spin = QDoubleSpinBox()
        self.axis_x_spin.setRange(-10.0, 10.0)
        self.axis_x_spin.setValue(0.0)
        self.axis_x_spin.setSingleStep(0.1)
        self.axis_x_spin.setDecimals(2)
        self.axis_x_spin.setMaximumHeight(18)
        layout.addWidget(self.axis_x_spin, 1, 1)
        
        # Y axis
        y_label = QLabel("Y:")
        y_label.setFont(QFont("Arial", 8))
        layout.addWidget(y_label, 2, 0)
        self.axis_y_spin = QDoubleSpinBox()
        self.axis_y_spin.setRange(-10.0, 10.0)
        self.axis_y_spin.setValue(0.0)
        self.axis_y_spin.setSingleStep(0.1)
        self.axis_y_spin.setDecimals(2)
        self.axis_y_spin.setMaximumHeight(18)
        layout.addWidget(self.axis_y_spin, 2, 1)
        
        # Z axis
        z_label = QLabel("Z:")
        z_label.setFont(QFont("Arial", 8))
        layout.addWidget(z_label, 3, 0)
        self.axis_z_spin = QDoubleSpinBox()
        self.axis_z_spin.setRange(-10.0, 10.0)
        self.axis_z_spin.setValue(1.0)
        self.axis_z_spin.setSingleStep(0.1)
        self.axis_z_spin.setDecimals(2)
        self.axis_z_spin.setMaximumHeight(18)
        layout.addWidget(self.axis_z_spin, 3, 1)
        
        # Angle control
        angle_label = QLabel("Angle (degrees):")
        angle_label.setFont(QFont("Arial", 8))
        layout.addWidget(angle_label, 4, 0)
        self.angle_spin = QDoubleSpinBox()
        self.angle_spin.setRange(-360.0, 360.0)
        self.angle_spin.setValue(45.0)
        self.angle_spin.setSingleStep(1.0)
        self.angle_spin.setDecimals(1)
        self.angle_spin.setMaximumHeight(18)
        layout.addWidget(self.angle_spin, 4, 1)
    
    def get_rotation(self):
        axis = Vector3(
            self.axis_x_spin.value(),
            self.axis_y_spin.value(),
            self.axis_z_spin.value()
        )
        angle = self.angle_spin.value()
        return Quaternion.from_axis_angle(axis, angle)