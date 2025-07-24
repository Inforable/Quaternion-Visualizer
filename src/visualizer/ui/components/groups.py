from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout
from PySide6.QtCore import Qt

from ..styles.theme import DarkTheme

class BaseGroupBox(QGroupBox):
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.setStyleSheet(DarkTheme.group_box())

class VerticalGroupBox(BaseGroupBox):
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        
        # Setup layout vertikal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(8, 15, 8, 8)
        self.layout.setSpacing(4)
    
    def add_widget(self, widget):
        self.layout.addWidget(widget)
    
    def add_spacing(self, spacing):
        self.layout.addSpacing(spacing)

class HorizontalGroupBox(BaseGroupBox):
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        
        # Setup layout horizontal
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(8, 15, 8, 8)
        self.layout.setSpacing(4)
    
    def add_widget(self, widget):
        self.layout.addWidget(widget)
    
    def add_stretch(self):
        self.layout.addStretch()

class GridGroupBox(BaseGroupBox):
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        
        # Setup layout grid
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(8, 15, 8, 8)
        self.layout.setSpacing(4)

        self.current_row = 0
    
    def add_widget_pair(self, label_widget, input_widget):
        self.layout.addWidget(label_widget, self.current_row, 0)
        self.layout.addWidget(input_widget, self.current_row, 1)
        self.current_row += 1
    
    def add_widget_full_row(self, widget):
        self.layout.addWidget(widget, self.current_row, 0, 1, 2)
        self.current_row += 1
    
    def add_widget_at(self, widget, row, column, row_span=1, col_span=1):
        self.layout.addWidget(widget, row, column, row_span, col_span)

        # Update current_row
        if row + row_span > self.current_row:
            self.current_row = row + row_span

class MethodGroupBox(VerticalGroupBox):
    def __init__(self, parent=None):
        super().__init__("Rotation Methods", parent)

class AxisGroupBox(VerticalGroupBox):
    def __init__(self, parent=None):
        super().__init__("Rotation Axis", parent)

class AngleGroupBox(VerticalGroupBox):
    def __init__(self, parent=None):
        super().__init__("Rotation Angle", parent)

class FileGroupBox(VerticalGroupBox):
    def __init__(self, parent=None):
        super().__init__("File Settings", parent)

class ActionsGroupBox(HorizontalGroupBox):
    def __init__(self, parent=None):
        super().__init__("Actions", parent)