from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QStackedWidget, QFrame, QLabel
from PySide6.QtGui import QFont
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
        layout.setSpacing(6)
        
        # Apply dark theme to widget
        self.setStyleSheet("""
            QWidget {
                background-color: #3a3a3a;
                color: #ffffff;
            }
        """)
        
        # Method selector
        method_label = QLabel("Method:")
        method_label.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        method_label.setStyleSheet("color: #ffffff; background: transparent;")
        layout.addWidget(method_label)
        
        self.method_combo = QComboBox()
        for method in RotationMethod:
            self.method_combo.addItem(method.value, method)

        self.method_combo.currentIndexChanged.connect(self._on_method_changed)
        self.method_combo.setMinimumHeight(24)
        self.method_combo.setMaximumHeight(28)
        self.method_combo.setStyleSheet("""
            QComboBox {
                padding: 4px;
                border: 1px solid #666666;
                border-radius: 3px;
                background-color: #4a4a4a;
                color: #ffffff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
                background-color: #5a5a5a;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
                background-color: #ffffff;
            }
            QComboBox QAbstractItemView {
                background-color: #4a4a4a;
                color: #ffffff;
                selection-background-color: #2196F3;
                border: 1px solid #666666;
            }
        """)
        layout.addWidget(self.method_combo)
        
        # Separator
        separator = QFrame()
        separator.setFrameStyle(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #666666; margin: 4px 0px;")
        layout.addWidget(separator)
        
        # Stacked widget for different control panels
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("""
            QStackedWidget {
                border: 1px solid #555555;
                border-radius: 3px;
                background-color: #3a3a3a;
                padding: 2px;
            }
        """)
        
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
    
    def _on_method_changed(self, index: int):
        method = self.method_combo.itemData(index)
        if method is None:
            method = RotationMethod.QUATERNION
        
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

        return self.quaternion_controls.get_rotation() 