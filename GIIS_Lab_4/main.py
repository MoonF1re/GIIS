from PyQt5.QtWidgets import QApplication
from editor import Editor
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Editor()
    window.show()
    sys.exit(app.exec_())