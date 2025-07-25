from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QStackedWidget, QFrame
from PySide6.QtGui import QFont
from PySide6.QtCore import Signal

from ...core.math.rotation_factory import RotationMethod
from .quaternion_controls import QuaternionControls
from .euler_controls import EulerControls
from .tait_bryan_controls import TaitBryanControls
from .exponential_controls import ExponentialControls
from ..styles.theme import DarkTheme
from ..styles.fonts import UIFonts

class RotationMethodWidget(QWidget):
    rotation_changed = Signal(object)  # Emit rotation object
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Method selection
        title_label = QLabel("Rotation Method")
        title_label.setFont(QFont(UIFonts.FAMILY, UIFonts.NORMAL_SIZE, QFont.Weight.Bold))
        title_label.setStyleSheet(DarkTheme.label())
        layout.addWidget(title_label)
        
        self.method_combo = QComboBox()
        self.method_combo.addItem("Unit Quaternion", RotationMethod.QUATERNION)
        self.method_combo.addItem("Euler Angle", RotationMethod.EULER_ANGLE)
        self.method_combo.addItem("Tait-Bryan", RotationMethod.TAIT_BRYAN)
        self.method_combo.addItem("Exponential Map", RotationMethod.EXPONENTIAL_MAP)
        self.method_combo.setStyleSheet(DarkTheme.combo_box())
        layout.addWidget(self.method_combo)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet(DarkTheme.separator())
        layout.addWidget(separator)
        
        # Stacked widget for different control types
        self.parameter_stack = QStackedWidget()
        
        # Initialize control widgets
        self.quaternion_widget = QuaternionControls()
        self.parameter_stack.addWidget(self.quaternion_widget)
        
        self.euler_widget = EulerControls()
        self.parameter_stack.addWidget(self.euler_widget)
        
        self.tait_bryan_widget = TaitBryanControls()
        self.parameter_stack.addWidget(self.tait_bryan_widget)
        
        self.exponential_widget = ExponentialControls()
        self.parameter_stack.addWidget(self.exponential_widget)
        
        layout.addWidget(self.parameter_stack)
        
        # Set default to quaternion
        self.method_combo.setCurrentIndex(0)
        self.parameter_stack.setCurrentIndex(0)
    
    def connect_signals(self):
        self.method_combo.currentIndexChanged.connect(self.on_method_changed)
        
        self.quaternion_widget.quaternion_changed.connect(self.on_quaternion_changed)
        self.euler_widget.valueChanged.connect(self.on_euler_changed)
        self.tait_bryan_widget.valueChanged.connect(self.on_tait_bryan_changed)
        self.exponential_widget.valueChanged.connect(self.on_exponential_changed)
    
    def on_method_changed(self, index):
        self.parameter_stack.setCurrentIndex(index)
        # Emit current rotation immediately when method changes
        self.emit_current_rotation()
    
    def on_quaternion_changed(self):
        if self.get_current_method() == RotationMethod.QUATERNION:
            rotation = self.quaternion_widget.get_rotation()
            if rotation:
                self.rotation_changed.emit(rotation)
    
    def on_euler_changed(self):
        if self.get_current_method() == RotationMethod.EULER_ANGLE:
            rotation = self.euler_widget.get_rotation()
            if rotation:
                self.rotation_changed.emit(rotation)
    
    def on_tait_bryan_changed(self):
        if self.get_current_method() == RotationMethod.TAIT_BRYAN:
            rotation = self.tait_bryan_widget.get_rotation()
            if rotation:
                self.rotation_changed.emit(rotation)
    
    def on_exponential_changed(self):
        if self.get_current_method() == RotationMethod.EXPONENTIAL_MAP:
            rotation = self.exponential_widget.get_rotation()
            if rotation:
                self.rotation_changed.emit(rotation)
    
    def emit_current_rotation(self):
        try:
            current_widget = self.parameter_stack.currentWidget()
            if hasattr(current_widget, 'get_rotation'):
                rotation = current_widget.get_rotation()
                if rotation:
                    self.rotation_changed.emit(rotation)
                else:
                    print(f"Warning: get_rotation() returned None for {type(current_widget).__name__}")
            else:
                print(f"Warning: Current widget {type(current_widget).__name__} has no get_rotation() method")
        except Exception as e:
            print(f"Error in emit_current_rotation: {e}")
    
    def get_current_method(self):
        try:
            return self.method_combo.currentData()
        except Exception as e:
            print(f"Error getting current method: {e}")
            return RotationMethod.QUATERNION
    
    def get_current_rotation(self):
        try:
            current_widget = self.parameter_stack.currentWidget()
            method = self.get_current_method()
            
            print(f"DEBUG: Current method: {method}")
            print(f"DEBUG: Current widget: {type(current_widget).__name__}")
            
            if hasattr(current_widget, 'get_rotation'):
                rotation = current_widget.get_rotation()
                print(f"DEBUG: Rotation object: {rotation}")
                print(f"DEBUG: Rotation type: {type(rotation).__name__ if rotation else 'None'}")
                return rotation
            else:
                print(f"ERROR: Widget {type(current_widget).__name__} has no get_rotation() method")
                return None
                
        except Exception as e:
            print(f"Error getting current rotation: {e}")
            return None
    
    def reset_to_identity(self):
        try:
            current_widget = self.parameter_stack.currentWidget()
            if hasattr(current_widget, 'reset_to_identity'):
                current_widget.reset_to_identity()
                # Emit reset rotation
                self.emit_current_rotation()
            else:
                print(f"Warning: Widget {type(current_widget).__name__} has no reset_to_identity() method")
        except Exception as e:
            print(f"Error resetting to identity: {e}")