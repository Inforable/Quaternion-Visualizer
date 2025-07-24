from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtCore import Qt

from ..styles.theme import DarkTheme

class BasePanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(DarkTheme.control_panel())
        self.setFrameStyle(QFrame.styledPanel)

class ControlPanel(BasePanel):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Setup untuk layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(8)

        # Set ukuran tetap dari panel
        self.setFixedWidth(300)
    
    def add_widget(self, widget: QWidget):
        self.layout.addWidget(widget)
    
    def add_section_spacing(self):
        self.layout.addSpacing(10)
    
    def add_stretch(self):
        self.layout.addStretch()

class HorizontalPanel(BasePanel):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Setup untuk layout horizontal
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)
    
    def add_widget(self, widget: QWidget):
        self.layout.addWidget(widget)
    
    def add_stretch(self):
        self.layout.addStretch()

class SectionPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Setup untuk layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(4)
    
    def add_widget(self, widget: QWidget):
        self.layout.addWidget(widget)
    
    def add_spacing(self, spacing):
        self.layout.addSpacing(spacing)

class ActionButtonPanel(HorizontalPanel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedHeight(50)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(8)