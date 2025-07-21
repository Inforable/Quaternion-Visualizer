import sys
import os
from PySide6.QtWidgets import QApplication

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from ui.main_window import MainWindow

def run_app():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_app()