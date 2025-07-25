from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QDoubleSpinBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Signal

from ...core.math.tait_bryan import TaitBryan
from ..styles.theme import DarkTheme
from ..styles.fonts import UIFonts

class TaitBryanControls(QWidget):
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
        info_label = QLabel("Tait-Bryan Rotation:")
        info_label.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        info_label.setStyleSheet(DarkTheme.label())
        layout.addWidget(info_label, 0, 0, 1, 2)
        
        # Roll control
        roll_label = QLabel("Roll (X-axis, °):")
        roll_label.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        roll_label.setStyleSheet(DarkTheme.label())
        layout.addWidget(roll_label, 1, 0)
        
        self.roll_spin = QDoubleSpinBox()
        self.roll_spin.setRange(-360.0, 360.0)
        self.roll_spin.setValue(0.0)
        self.roll_spin.setSingleStep(1.0)
        self.roll_spin.setDecimals(1)
        self.roll_spin.setStyleSheet(DarkTheme.spin_box())
        layout.addWidget(self.roll_spin, 1, 1)
        
        # Pitch control
        pitch_label = QLabel("Pitch (Y-axis, °):")
        pitch_label.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        pitch_label.setStyleSheet(DarkTheme.label())
        layout.addWidget(pitch_label, 2, 0)
        
        self.pitch_spin = QDoubleSpinBox()
        self.pitch_spin.setRange(-360.0, 360.0)
        self.pitch_spin.setValue(0.0)
        self.pitch_spin.setSingleStep(1.0)
        self.pitch_spin.setDecimals(1)
        self.pitch_spin.setStyleSheet(DarkTheme.spin_box())
        layout.addWidget(self.pitch_spin, 2, 1)
        
        # Yaw control
        yaw_label = QLabel("Yaw (Z-axis, °):")
        yaw_label.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        yaw_label.setStyleSheet(DarkTheme.label())
        layout.addWidget(yaw_label, 3, 0)
        
        self.yaw_spin = QDoubleSpinBox()
        self.yaw_spin.setRange(-360.0, 360.0)
        self.yaw_spin.setValue(45.0)
        self.yaw_spin.setSingleStep(1.0)
        self.yaw_spin.setDecimals(1)
        self.yaw_spin.setStyleSheet(DarkTheme.spin_box())
        layout.addWidget(self.yaw_spin, 3, 1)
    
    def connect_signals(self):
        self.roll_spin.valueChanged.connect(self.valueChanged.emit)
        self.pitch_spin.valueChanged.connect(self.valueChanged.emit)
        self.yaw_spin.valueChanged.connect(self.valueChanged.emit)
    
    def get_rotation(self):
        return TaitBryan(
            self.roll_spin.value(),
            self.pitch_spin.value(),
            self.yaw_spin.value()
        )
        
    def reset_to_identity(self):
        self.roll_spin.setValue(0.0)
        self.pitch_spin.setValue(0.0)
        self.yaw_spin.setValue(0.0)