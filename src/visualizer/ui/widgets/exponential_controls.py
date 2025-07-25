from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QDoubleSpinBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Signal

from ...core.math.exponential_map import ExponentialMap
from ...core.math.vector3 import Vector3
from ..styles.theme import DarkTheme
from ..styles.fonts import UIFonts

class ExponentialControls(QWidget):
    valueChanged = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        layout = QGridLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(2)
        
        # Info label
        info_label = QLabel("Rotation Vector (ω):")
        info_label.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        info_label.setStyleSheet(DarkTheme.label())
        layout.addWidget(info_label, 0, 0, 1, 2)
        
        # X component
        x_label = QLabel("ωx:")
        x_label.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        x_label.setStyleSheet(DarkTheme.label())
        layout.addWidget(x_label, 1, 0)
        
        self.omega_x_spin = QDoubleSpinBox()
        self.omega_x_spin.setRange(-10.0, 10.0)
        self.omega_x_spin.setValue(0.0)
        self.omega_x_spin.setSingleStep(0.1)
        self.omega_x_spin.setDecimals(2)
        self.omega_x_spin.setStyleSheet(DarkTheme.spin_box())
        layout.addWidget(self.omega_x_spin, 1, 1)
        
        # Y component
        y_label = QLabel("ωy:")
        y_label.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        y_label.setStyleSheet(DarkTheme.label())
        layout.addWidget(y_label, 2, 0)
        
        self.omega_y_spin = QDoubleSpinBox()
        self.omega_y_spin.setRange(-10.0, 10.0)
        self.omega_y_spin.setValue(0.0)
        self.omega_y_spin.setSingleStep(0.1)
        self.omega_y_spin.setDecimals(2)
        self.omega_y_spin.setStyleSheet(DarkTheme.spin_box())
        layout.addWidget(self.omega_y_spin, 2, 1)
        
        # Z component
        z_label = QLabel("ωz:")
        z_label.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        z_label.setStyleSheet(DarkTheme.label())
        layout.addWidget(z_label, 3, 0)
        
        self.omega_z_spin = QDoubleSpinBox()
        self.omega_z_spin.setRange(-10.0, 10.0)
        self.omega_z_spin.setValue(0.785)  # ~45 degrees in radians
        self.omega_z_spin.setSingleStep(0.1)
        self.omega_z_spin.setDecimals(3)
        self.omega_z_spin.setStyleSheet(DarkTheme.spin_box())
        layout.addWidget(self.omega_z_spin, 3, 1)
    
    def connect_signals(self):
        self.omega_x_spin.valueChanged.connect(self.valueChanged.emit)
        self.omega_y_spin.valueChanged.connect(self.valueChanged.emit)
        self.omega_z_spin.valueChanged.connect(self.valueChanged.emit)
    
    def get_rotation(self):
        omega = Vector3(
            self.omega_x_spin.value(),
            self.omega_y_spin.value(),
            self.omega_z_spin.value()
        )
        return ExponentialMap(omega)
        
    def reset_to_identity(self):
        self.omega_x_spin.setValue(0.0)
        self.omega_y_spin.setValue(0.0)
        self.omega_z_spin.setValue(0.0)