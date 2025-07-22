from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QDoubleSpinBox
from PySide6.QtGui import QFont

from ...core.math.tait_bryan import TaitBryan

class TaitBryanControls(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QGridLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(2)
        
        # Info label
        info_label = QLabel("Aircraft-style Rotation:")
        info_label.setFont(QFont("Arial", 9))
        layout.addWidget(info_label, 0, 0, 1, 2)
        
        # Roll control
        roll_label = QLabel("Roll (X-axis, °):")
        roll_label.setFont(QFont("Arial", 8))
        layout.addWidget(roll_label, 1, 0)
        self.roll_spin = QDoubleSpinBox()
        self.roll_spin.setRange(-360.0, 360.0)
        self.roll_spin.setValue(0.0)
        self.roll_spin.setSingleStep(1.0)
        self.roll_spin.setDecimals(1)
        self.roll_spin.setMaximumHeight(18)
        layout.addWidget(self.roll_spin, 1, 1)
        
        # Pitch control
        pitch_label = QLabel("Pitch (Y-axis, °):")
        pitch_label.setFont(QFont("Arial", 8))
        layout.addWidget(pitch_label, 2, 0)
        self.pitch_spin = QDoubleSpinBox()
        self.pitch_spin.setRange(-360.0, 360.0)
        self.pitch_spin.setValue(0.0)
        self.pitch_spin.setSingleStep(1.0)
        self.pitch_spin.setDecimals(1)
        self.pitch_spin.setMaximumHeight(18)
        layout.addWidget(self.pitch_spin, 2, 1)
        
        # Yaw control
        yaw_label = QLabel("Yaw (Z-axis, °):")
        yaw_label.setFont(QFont("Arial", 8))
        layout.addWidget(yaw_label, 3, 0)
        self.yaw_spin = QDoubleSpinBox()
        self.yaw_spin.setRange(-360.0, 360.0)
        self.yaw_spin.setValue(45.0)
        self.yaw_spin.setSingleStep(1.0)
        self.yaw_spin.setDecimals(1)
        self.yaw_spin.setMaximumHeight(18)
        layout.addWidget(self.yaw_spin, 3, 1)
    
    def get_rotation(self):
        return TaitBryan(
            self.roll_spin.value(),
            self.pitch_spin.value(),
            self.yaw_spin.value()
        )