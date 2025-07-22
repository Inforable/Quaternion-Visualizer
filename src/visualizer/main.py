import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QIcon

from .config import (
    APP_NAME, 
    ICONS_DIR,
    DEFAULT_WINDOW_SIZE,
    MIN_WINDOW_SIZE
)
from .ui.windows.main_window import MainWindow

def setup_application():
    # Membuat Qapplication 
    app = QApplication(sys.argv)

    # Mengatur nama aplikasi
    app.setApplicationName(APP_NAME)

    # Mengatur DPI scaling
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    # Ikon aplikasi
    icon_path = ICONS_DIR / 'app_icon.png'
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    else:
        QMessageBox.warning(None, "Icon Not Found", f"Icon not found at {icon_path}")
    
    # Mengatur style aplikasi
    app.setStyle("Fusion")

    return app

def setup_directories():
    try:
        # Pastikan direktori utama ada
        ICONS_DIR.mkdir(parents=True, exist_ok=True)

        # Buat direktori logs
        logs_dir = Path(__file__).parent.parent.parent / "logs"
        logs_dir.mkdir(exist_ok=True)
        
    except Exception as e:
        print(f"Warning: {e}")

def main():
    try:
        setup_directories()
        app = setup_application()

        # Membuat dan menampilkan jendela utama
        main_window = MainWindow()
        main_window.resize(*DEFAULT_WINDOW_SIZE)
        main_window.setMinimumSize(*MIN_WINDOW_SIZE)
        main_window.show()

        # Menjalankan aplikasi
        sys.exit(app.exec())
    
    except Exception as e:
        QMessageBox.critical(None, "Error", f"terdapat kesalahan: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()