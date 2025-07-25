from .colors import UIColors
from .fonts import UIFonts

class DarkTheme:
    @staticmethod
    def main_window() -> str:
        return f"""
        QMainWindow {{
            background-color: {UIColors.BACKGROUND_DARK};
            color: {UIColors.TEXT_PRIMARY};
        }}
        """
    
    @staticmethod
    def title_label() -> str:
        return f"""
        QLabel {{ 
            color: {UIColors.PRIMARY_BLUE}; 
            padding: 4px;
            border-bottom: 1px solid {UIColors.PRIMARY_BLUE};
            margin-bottom: 2px;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                stop:0 {UIColors.BACKGROUND_LIGHT}, stop:1 {UIColors.BACKGROUND_MEDIUM});
            font-family: {UIFonts.FAMILY};
            font-size: {UIFonts.TITLE_SIZE}px;
            font-weight: bold;
        }}
        """
    
    @staticmethod
    def control_panel() -> str:
        return f"""
        QFrame {{
            background-color: {UIColors.PANEL_BACKGROUND};
            color: {UIColors.TEXT_PRIMARY};
            border: 1px solid {UIColors.BORDER_COLOR};
            border-radius: 4px;
        }}
        """
    
    @staticmethod
    def section_title() -> str:
        return f"""
        QLabel {{ 
            color: {UIColors.ACCENT_BLUE}; 
            border-bottom: 1px solid {UIColors.ACCENT_BLUE}; 
            padding-bottom: 3px; 
            margin-bottom: 5px;
            background: transparent;
            font-family: {UIFonts.FAMILY};
            font-size: {UIFonts.NORMAL_SIZE}px;
            font-weight: bold;
        }}
        """
    
    @staticmethod
    def group_box() -> str:
        return f"""
        QGroupBox {{ 
            font-weight: bold;
            color: {UIColors.TEXT_PRIMARY};
            border: 1px solid {UIColors.BORDER_COLOR};
            border-radius: 4px;
            margin-top: 8px;
            padding-top: 4px;
            background-color: {UIColors.GROUP_BACKGROUND};
            font-family: {UIFonts.FAMILY};
            font-size: {UIFonts.SMALL_SIZE}px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 8px;
            padding: 0 4px 0 4px;
            color: {UIColors.TEXT_PRIMARY};
        }}
        """
    
    @staticmethod
    def primary_button() -> str:
        return f"""
        QPushButton {{ 
            padding: 8px; 
            font-size: {UIFonts.NORMAL_SIZE}px; 
            font-weight: bold;
            background-color: {UIColors.PRIMARY_BLUE}; 
            color: {UIColors.TEXT_ON_PRIMARY}; 
            border-radius: 4px;
            min-height: 28px;
            border: none;
            font-family: {UIFonts.FAMILY};
        }}
        QPushButton:hover {{
            background-color: {UIColors.PRIMARY_BLUE_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {UIColors.PRIMARY_BLUE_PRESSED};
        }}
        QPushButton:disabled {{
            background-color: {UIColors.BUTTON_DISABLED};
            color: {UIColors.TEXT_DISABLED};
        }}
        """
    
    @staticmethod
    def secondary_button() -> str:
        return f"""
        QPushButton {{ 
            padding: 6px; 
            font-size: {UIFonts.SMALL_SIZE}px; 
            background-color: {UIColors.BUTTON_SECONDARY};
            color: {UIColors.TEXT_PRIMARY};
            border: 1px solid {UIColors.BORDER_COLOR};
            border-radius: 3px;
            min-height: 24px;
            font-family: {UIFonts.FAMILY};
        }}
        QPushButton:hover {{
            background-color: {UIColors.BUTTON_SECONDARY_HOVER};
            border: 1px solid {UIColors.BORDER_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {UIColors.BUTTON_SECONDARY_PRESSED};
        }}
        """
    
    @staticmethod
    def warning_button() -> str:
        return f"""
        QPushButton {{ 
            padding: 6px; 
            font-size: {UIFonts.SMALL_SIZE}px; 
            background-color: {UIColors.WARNING_ORANGE};
            color: {UIColors.TEXT_ON_PRIMARY};
            border: 1px solid {UIColors.WARNING_ORANGE};
            border-radius: 3px;
            min-height: 24px;
            font-family: {UIFonts.FAMILY};
        }}
        QPushButton:hover {{
            background-color: {UIColors.WARNING_ORANGE_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {UIColors.WARNING_ORANGE_PRESSED};
        }}
        """
    
    @staticmethod
    def text_edit() -> str:
        return f"""
        QTextEdit {{
            background-color: {UIColors.INPUT_BACKGROUND};
            color: {UIColors.TEXT_PRIMARY};
            border: 1px solid {UIColors.BORDER_COLOR};
            border-radius: 4px;
            padding: 6px;
            font-family: {UIFonts.MONOSPACE_FAMILY};
            font-size: {UIFonts.SMALL_SIZE}px;
        }}
        QScrollBar:vertical {{
            background-color: {UIColors.SCROLLBAR_BACKGROUND};
            width: 12px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {UIColors.SCROLLBAR_HANDLE};
            border-radius: 6px;
            min-height: 20px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {UIColors.SCROLLBAR_HANDLE_HOVER};
        }}
        """
    
    @staticmethod
    def spin_box() -> str:
        return f"""
        QDoubleSpinBox, QSpinBox {{
            background-color: {UIColors.INPUT_BACKGROUND};
            color: {UIColors.TEXT_PRIMARY};
            border: 1px solid {UIColors.BORDER_COLOR};
            border-radius: 3px;
            padding: 4px;
            min-height: 20px;
            font-family: {UIFonts.FAMILY};
            font-size: {UIFonts.SMALL_SIZE}px;
        }}
        QDoubleSpinBox:focus, QSpinBox:focus {{
            border: 1px solid {UIColors.PRIMARY_BLUE};
        }}
        """
    
    @staticmethod
    def combo_box() -> str:
        return f"""
        QComboBox {{
            background-color: {UIColors.INPUT_BACKGROUND};
            color: {UIColors.TEXT_PRIMARY};
            border: 1px solid {UIColors.BORDER_COLOR};
            border-radius: 3px;
            padding: 4px;
            min-height: 20px;
            font-family: {UIFonts.FAMILY};
            font-size: {UIFonts.SMALL_SIZE}px;
        }}
        QComboBox:focus {{
            border: 1px solid {UIColors.PRIMARY_BLUE};
        }}
        QComboBox::drop-down {{
            border: none;
        }}
        QComboBox QAbstractItemView {{
            background-color: {UIColors.INPUT_BACKGROUND};
            color: {UIColors.TEXT_PRIMARY};
            selection-background-color: {UIColors.PRIMARY_BLUE};
        }}
        """
    
    @staticmethod
    def label() -> str:
        return f"""
        QLabel {{
            color: {UIColors.TEXT_PRIMARY};
            font-family: {UIFonts.FAMILY};
            font-size: {UIFonts.SMALL_SIZE}px;
        }}
        """
    
    @staticmethod
    def separator() -> str:
        return f"""
        QFrame {{
            background-color: {UIColors.BORDER_COLOR};
            border: none;
        }}
        """
    
    @staticmethod
    def get_complete_stylesheet() -> str:
        return f"""
        {DarkTheme.main_window()}
        {DarkTheme.control_panel()}
        {DarkTheme.group_box()}
        {DarkTheme.primary_button()}
        {DarkTheme.secondary_button()}
        {DarkTheme.warning_button()}
        {DarkTheme.text_edit()}
        {DarkTheme.spin_box()}
        {DarkTheme.combo_box()}
        {DarkTheme.label()}
        {DarkTheme.separator()}
        """