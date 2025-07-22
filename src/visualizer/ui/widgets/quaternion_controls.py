from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QDoubleSpinBox
from PySide6.QtGui import QFont

from ...core.math.vector3 import Vector3
from ...core.math.quaternion import Quaternion

class QuaternionControls(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Apply dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #3a3a3a;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                background: transparent;
            }
            QDoubleSpinBox {
                background-color: #4a4a4a;
                color: #ffffff;
                border: 1px solid #666666;
                border-radius: 3px;
                padding: 2px;
            }
            QDoubleSpinBox:focus {
                border: 1px solid #2196F3;
            }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                background-color: #5a5a5a;
                border: 1px solid #666666;
            }
            QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
                background-color: #6a6a6a;
            }
        """)
        
        layout = QGridLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        layout.setColumnStretch(1, 1)
        
        # Axis controls
        axis_label = QLabel("Rotation Axis:")
        axis_label.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        layout.addWidget(axis_label, 0, 0, 1, 2)
        
        # X axis
        x_label = QLabel("X:")
        x_label.setFont(QFont("Arial", 8))
        x_label.setMinimumWidth(20)
        layout.addWidget(x_label, 1, 0)
        self.axis_x_spin = QDoubleSpinBox()
        self.axis_x_spin.setRange(-10.0, 10.0)
        self.axis_x_spin.setValue(0.0)
        self.axis_x_spin.setSingleStep(0.1)
        self.axis_x_spin.setDecimals(2)
        self.axis_x_spin.setMinimumHeight(22)
        self.axis_x_spin.setMaximumHeight(26)
        layout.addWidget(self.axis_x_spin, 1, 1)
        
        # Y axis
        y_label = QLabel("Y:")
        y_label.setFont(QFont("Arial", 8))
        y_label.setMinimumWidth(20)
        layout.addWidget(y_label, 2, 0)
        self.axis_y_spin = QDoubleSpinBox()
        self.axis_y_spin.setRange(-10.0, 10.0)
        self.axis_y_spin.setValue(0.0)
        self.axis_y_spin.setSingleStep(0.1)
        self.axis_y_spin.setDecimals(2)
        self.axis_y_spin.setMinimumHeight(22)
        self.axis_y_spin.setMaximumHeight(26)
        layout.addWidget(self.axis_y_spin, 2, 1)
        
        # Z axis
        z_label = QLabel("Z:")
        z_label.setFont(QFont("Arial", 8))
        z_label.setMinimumWidth(20)
        layout.addWidget(z_label, 3, 0)
        self.axis_z_spin = QDoubleSpinBox()
        self.axis_z_spin.setRange(-10.0, 10.0)
        self.axis_z_spin.setValue(1.0)
        self.axis_z_spin.setSingleStep(0.1)
        self.axis_z_spin.setDecimals(2)
        self.axis_z_spin.setMinimumHeight(22)
        self.axis_z_spin.setMaximumHeight(26)
        layout.addWidget(self.axis_z_spin, 3, 1)
        
        # Spacer
        spacer = QLabel("")
        spacer.setMaximumHeight(6)
        layout.addWidget(spacer, 4, 0, 1, 2)
        
        # Angle control
        angle_label = QLabel("Angle (degrees):")
        angle_label.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        layout.addWidget(angle_label, 5, 0, 1, 2)
        
        self.angle_spin = QDoubleSpinBox()
        self.angle_spin.setRange(-360.0, 360.0)
        self.angle_spin.setValue(45.0)
        self.angle_spin.setSingleStep(1.0)
        self.angle_spin.setDecimals(1)
        self.angle_spin.setMinimumHeight(22)
        self.angle_spin.setMaximumHeight(26)
        layout.addWidget(self.angle_spin, 6, 0, 1, 2)
    
    def get_rotation(self):
        axis = Vector3(
            self.axis_x_spin.value(),
            self.axis_y_spin.value(),
            self.axis_z_spin.value()
        )
        angle = self.angle_spin.value()
        return Quaternion.from_axis_angle(axis, angle)