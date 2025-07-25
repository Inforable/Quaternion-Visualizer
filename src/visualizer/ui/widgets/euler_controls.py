from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QDoubleSpinBox, QComboBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Signal

from ...core.math.euler_angle import EulerAngle
from ..styles.theme import DarkTheme
from ..styles.fonts import UIFonts

class EulerControls(QWidget):
    valueChanged = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        layout = QGridLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(2)
        
        # Rotation order
        order_label = QLabel("Rotation Order:")
        order_label.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        order_label.setStyleSheet(DarkTheme.label())
        layout.addWidget(order_label, 0, 0)
        
        self.order_combo = QComboBox()
        self.order_combo.addItems(EulerAngle.ROTATION_ORDERS)
        self.order_combo.setStyleSheet(DarkTheme.combo_box())
        layout.addWidget(self.order_combo, 0, 1)
        
        # X rotation
        x_label = QLabel("X Rotation (°):")
        x_label.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        x_label.setStyleSheet(DarkTheme.label())
        layout.addWidget(x_label, 1, 0)
        
        self.x_angle_spin = QDoubleSpinBox()
        self.x_angle_spin.setRange(-360.0, 360.0)
        self.x_angle_spin.setValue(0.0)
        self.x_angle_spin.setSingleStep(1.0)
        self.x_angle_spin.setDecimals(1)
        self.x_angle_spin.setStyleSheet(DarkTheme.spin_box())
        layout.addWidget(self.x_angle_spin, 1, 1)
        
        # Y rotation
        y_label = QLabel("Y Rotation (°):")
        y_label.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        y_label.setStyleSheet(DarkTheme.label())
        layout.addWidget(y_label, 2, 0)
        
        self.y_angle_spin = QDoubleSpinBox()
        self.y_angle_spin.setRange(-360.0, 360.0)
        self.y_angle_spin.setValue(0.0)
        self.y_angle_spin.setSingleStep(1.0)
        self.y_angle_spin.setDecimals(1)
        self.y_angle_spin.setStyleSheet(DarkTheme.spin_box())
        layout.addWidget(self.y_angle_spin, 2, 1)
        
        # Z rotation
        z_label = QLabel("Z Rotation (°):")
        z_label.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        z_label.setStyleSheet(DarkTheme.label())
        layout.addWidget(z_label, 3, 0)
        
        self.z_angle_spin = QDoubleSpinBox()
        self.z_angle_spin.setRange(-360.0, 360.0)
        self.z_angle_spin.setValue(45.0)
        self.z_angle_spin.setSingleStep(1.0)
        self.z_angle_spin.setDecimals(1)
        self.z_angle_spin.setStyleSheet(DarkTheme.spin_box())
        layout.addWidget(self.z_angle_spin, 3, 1)
    
    def connect_signals(self):
        self.order_combo.currentTextChanged.connect(self.valueChanged.emit)
        self.x_angle_spin.valueChanged.connect(self.valueChanged.emit)
        self.y_angle_spin.valueChanged.connect(self.valueChanged.emit)
        self.z_angle_spin.valueChanged.connect(self.valueChanged.emit)
    
    def get_rotation(self):
        return EulerAngle(
            self.x_angle_spin.value(),
            self.y_angle_spin.value(),
            self.z_angle_spin.value(),
            self.order_combo.currentText()
        )
        
    def reset_to_identity(self):
        self.x_angle_spin.setValue(0.0)
        self.y_angle_spin.setValue(0.0)
        self.z_angle_spin.setValue(0.0)
        self.order_combo.setCurrentIndex(0)