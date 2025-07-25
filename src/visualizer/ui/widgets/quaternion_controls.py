import math
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QDoubleSpinBox, QPushButton, QLabel, QGroupBox,
    QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from ...core.math.quaternion import Quaternion
from ...core.math.vector3 import Vector3
from ..styles.theme import DarkTheme
from ..styles.fonts import UIFonts

class QuaternionControls(QWidget):
    quaternion_changed = Signal(object)
    axis_changed = Signal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_quaternion = Quaternion(1.0, 0.0, 0.0, 0.0)
        self.setup_ui()
        self.connect_signals()
        self.update_computed_values()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        self.setup_quaternion_input_group(layout)
        self.setup_computed_display_group(layout)
        
    def setup_quaternion_input_group(self, parent_layout):
        """Input for Unit Quaternion as per specification"""
        group = QGroupBox("Unit Quaternion Input (w + xi + yj + zk)")
        group.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE, QFont.Weight.Bold))
        group.setStyleSheet(DarkTheme.group_box())
        
        layout = QFormLayout(group)
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.setVerticalSpacing(6)
        
        # Create input spinboxes
        self.w_input = QDoubleSpinBox()
        self.x_input = QDoubleSpinBox()
        self.y_input = QDoubleSpinBox()
        self.z_input = QDoubleSpinBox()
        
        # Configure all spinboxes
        for spinbox in [self.w_input, self.x_input, self.y_input, self.z_input]:
            spinbox.setRange(-1.0, 1.0)
            spinbox.setDecimals(4)
            spinbox.setSingleStep(0.01)
            spinbox.setMinimumWidth(100)
            spinbox.setStyleSheet(DarkTheme.spin_box())
        
        # Set default identity quaternion
        self.w_input.setValue(1.0)
        self.x_input.setValue(0.0)
        self.y_input.setValue(0.0)
        self.z_input.setValue(0.0)
        
        # Add to layout with proper labels
        w_label = QLabel("w:")
        w_label.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        w_label.setStyleSheet(DarkTheme.label())
        layout.addRow(w_label, self.w_input)
        
        x_label = QLabel("x:")
        x_label.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        x_label.setStyleSheet(DarkTheme.label())
        layout.addRow(x_label, self.x_input)
        
        y_label = QLabel("y:")
        y_label.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        y_label.setStyleSheet(DarkTheme.label())
        layout.addRow(y_label, self.y_input)
        
        z_label = QLabel("z:")
        z_label.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        z_label.setStyleSheet(DarkTheme.label())
        layout.addRow(z_label, self.z_input)
        
        parent_layout.addWidget(group)
        
    def setup_computed_display_group(self, parent_layout):
        group = QGroupBox("Computed Axis & Angle")
        group.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE, QFont.Weight.Bold))
        group.setStyleSheet(DarkTheme.group_box())
        
        layout = QFormLayout(group)
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.setVerticalSpacing(4)
        
        # Axis display
        axis_container = QWidget()
        axis_layout = QHBoxLayout(axis_container)
        axis_layout.setContentsMargins(0, 0, 0, 0)
        axis_layout.setSpacing(4)
        
        self.axis_x_display = QLabel("0.000")
        self.axis_y_display = QLabel("0.000")
        self.axis_z_display = QLabel("1.000")
        
        for label in [self.axis_x_display, self.axis_y_display, self.axis_z_display]:
            label.setFont(QFont(UIFonts.MONOSPACE_FAMILY, UIFonts.SMALL_SIZE))
            label.setStyleSheet(f"color: #E0E0E0; background-color: #2A2A2A; padding: 2px 4px; border: 1px solid #404040; border-radius: 2px;")
            label.setMinimumWidth(50)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        x_label = QLabel("x:")
        x_label.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        x_label.setStyleSheet(DarkTheme.label())
        
        y_label = QLabel("y:")
        y_label.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        y_label.setStyleSheet(DarkTheme.label())
        
        z_label = QLabel("z:")
        z_label.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        z_label.setStyleSheet(DarkTheme.label())
        
        axis_layout.addWidget(x_label)
        axis_layout.addWidget(self.axis_x_display)
        axis_layout.addWidget(y_label)
        axis_layout.addWidget(self.axis_y_display)
        axis_layout.addWidget(z_label)
        axis_layout.addWidget(self.axis_z_display)
        axis_layout.addStretch()
        
        axis_title = QLabel("Axis:")
        axis_title.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        axis_title.setStyleSheet(DarkTheme.label())
        layout.addRow(axis_title, axis_container)
        
        # Angle display
        self.angle_display = QLabel("0.0°")
        self.angle_display.setFont(QFont(UIFonts.MONOSPACE_FAMILY, UIFonts.SMALL_SIZE))
        self.angle_display.setStyleSheet(f"color: #E0E0E0; background-color: #2A2A2A; padding: 4px 8px; border: 1px solid #404040; border-radius: 3px;")
        self.angle_display.setMinimumWidth(80)
        self.angle_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        angle_title = QLabel("Angle:")
        angle_title.setFont(QFont(UIFonts.FAMILY, UIFonts.SMALL_SIZE))
        angle_title.setStyleSheet(DarkTheme.label())
        layout.addRow(angle_title, self.angle_display)
        
        parent_layout.addWidget(group)
        
    def connect_signals(self):
        # Quaternion input changes
        self.w_input.valueChanged.connect(self.on_quaternion_changed)
        self.x_input.valueChanged.connect(self.on_quaternion_changed)
        self.y_input.valueChanged.connect(self.on_quaternion_changed)
        self.z_input.valueChanged.connect(self.on_quaternion_changed)
        
    def on_quaternion_changed(self):
        w = self.w_input.value()
        x = self.x_input.value()
        y = self.y_input.value()
        z = self.z_input.value()
        
        self.current_quaternion = Quaternion(w, x, y, z)
        self.update_computed_values()
        
        # Emit signals
        self.quaternion_changed.emit(self.current_quaternion)
        
        try:
            axis, angle = self.current_quaternion.to_axis_angle()
            self.axis_changed.emit(axis)
        except:
            pass
        
    def update_computed_values(self):
        try:
            axis, angle = self.current_quaternion.to_axis_angle()
            
            self.axis_x_display.setText(f"{axis.x:.3f}")
            self.axis_y_display.setText(f"{axis.y:.3f}")
            self.axis_z_display.setText(f"{axis.z:.3f}")
            self.angle_display.setText(f"{angle:.1f}°")
            
        except Exception as e:
            self.axis_x_display.setText("0.000")
            self.axis_y_display.setText("0.000")
            self.axis_z_display.setText("1.000")
            self.angle_display.setText("0.0°")
            
    def reset_to_identity(self):
        self.block_signals(True)
        self.w_input.setValue(1.0)
        self.x_input.setValue(0.0)
        self.y_input.setValue(0.0)
        self.z_input.setValue(0.0)
        self.block_signals(False)
        
        self.on_quaternion_changed()
        
    def get_current_quaternion(self):
        return self.current_quaternion
        
    def get_current_angle(self):
        try:
            _, angle = self.current_quaternion.to_axis_angle()
            return angle
        except:
            return 0.0
            
    def block_signals(self, block):
        self.w_input.blockSignals(block)
        self.x_input.blockSignals(block)
        self.y_input.blockSignals(block)
        self.z_input.blockSignals(block)
    
    def get_rotation(self):
        return self.current_quaternion