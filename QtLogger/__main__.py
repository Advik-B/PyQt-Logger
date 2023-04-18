from .base import QtLogger
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QApplication

from sys import argv


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.logger = QtLogger(self, log_folder="logs", font=QFont("JetBrains Mono", 10))
        self.logger.start()
        self.show()

    def closeEvent(self, event):
        self.logger.stop()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(argv)
    window = MainWindow()
    app.exec()
