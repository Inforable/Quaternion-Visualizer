import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from .config import (
    APP_NAME, 
    ICONS_DIR,
    DEFAULT_WINDOW_WIDTH,
    DEFAULT_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    MIN_WINDOW_HEIGHT
)
from .ui.windows.main_window import MainWindow

def setup_application():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    icon_path = ICONS_DIR / 'app_icon.png'
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    app.setStyle("Fusion")
    
    return app

def setup_directories():
    try:
        ICONS_DIR.mkdir(parents=True, exist_ok=True)
        logs_dir = Path(__file__).parent.parent.parent / "logs"
        logs_dir.mkdir(exist_ok=True)
    except Exception as e:
        print(f"Warning: Could not create directories: {e}")

def main():
    try:
        setup_directories()
        app = setup_application()
        
        main_window = MainWindow()
        main_window.resize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        main_window.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        main_window.showMaximized()

        main_window.show()
        
        sys.exit(app.exec())
    
    except Exception as e:
        QMessageBox.critical(None, "Application Error", f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()