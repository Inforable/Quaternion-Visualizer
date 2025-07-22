from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QStackedWidget
from PySide6.QtCore import Signal

from ...core.math.rotation_factory import RotationMethod
from .quaternion_controls import QuaternionControls
from .euler_controls import EulerControls
from .tait_bryan_controls import TaitBryanControls
from .exponential_controls import ExponentialControls

class RotationMethodWidget(QWidget):
    method_changed = Signal(RotationMethod)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.current_method = RotationMethod.QUATERNION
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        
        # Method selector
        self.method_combo = QComboBox()
        for method in RotationMethod:
            self.method_combo.addItem(method.value, method)
        self.method_combo.currentDataChanged.connect(self._on_method_changed)
        self.method_combo.setMaximumHeight(20)
        layout.addWidget(self.method_combo)
        
        # Stacked widget for different control panels
        self.stacked_widget = QStackedWidget()
        
        # Create control widgets
        self.quaternion_controls = QuaternionControls()
        self.euler_controls = EulerControls()
        self.tait_bryan_controls = TaitBryanControls()
        self.exponential_controls = ExponentialControls()
        
        # Add to stacked widget
        self.stacked_widget.addWidget(self.quaternion_controls)
        self.stacked_widget.addWidget(self.euler_controls)
        self.stacked_widget.addWidget(self.tait_bryan_controls)
        self.stacked_widget.addWidget(self.exponential_controls)
        
        layout.addWidget(self.stacked_widget)
    
    def _on_method_changed(self, method: RotationMethod):
        self.current_method = method
        
        # Switch to appropriate control panel
        if method == RotationMethod.QUATERNION:
            self.stacked_widget.setCurrentWidget(self.quaternion_controls)
        elif method == RotationMethod.EULER_ANGLE:
            self.stacked_widget.setCurrentWidget(self.euler_controls)
        elif method == RotationMethod.TAIT_BRYAN:
            self.stacked_widget.setCurrentWidget(self.tait_bryan_controls)
        elif method == RotationMethod.EXPONENTIAL_MAP:
            self.stacked_widget.setCurrentWidget(self.exponential_controls)
        
        self.method_changed.emit(method)
    
    def get_rotation_object(self):
        """Get current rotation object based on active method."""
        if self.current_method == RotationMethod.QUATERNION:
            return self.quaternion_controls.get_rotation()
        elif self.current_method == RotationMethod.EULER_ANGLE:
            return self.euler_controls.get_rotation()
        elif self.current_method == RotationMethod.TAIT_BRYAN:
            return self.tait_bryan_controls.get_rotation()
        elif self.current_method == RotationMethod.EXPONENTIAL_MAP:
            return self.exponential_controls.get_rotation()