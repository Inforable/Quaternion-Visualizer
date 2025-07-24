from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Signal

from ..styles.theme import DarkTheme

class PrimaryButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(DarkTheme.primary_button())
    
class SecondaryButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(DarkTheme.secondary_button())

class WarningButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(DarkTheme.warning_button())

class ToggleRendererButton(WarningButton):
    renderer_toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__("Switch to Custom Renderer", parent)
        self.use_custom = False

        self.clicked.connect(self.on_clicked)
    
    def on_clicked(self):
        self.use_custom = not self.use_custom
        self._update_text()
        self.renderer_toggled.emit(self.use_custom)
    
    def _update_text(self):
        if self.use_custom:
            self.setText("Switch to OpenGL Renderer")
        else:
            self.setText("Switch to Custom Renderer")
    
class LoadModelButton(PrimaryButton):
    model_loaded = Signal(str)

    def __init__(self, parent=None):
        super().__init__("Load OBJ File", parent)

class ApplyRotationButton(PrimaryButton):
    def __init__(self, parent=None):
        super().__init__("Apply Rotation", parent)

class ResetViewButton(SecondaryButton):
    def __init__(self, parent=None):
        super().__init__("Reset View", parent)