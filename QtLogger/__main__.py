from .base import QtLogger
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QApplication, QGridLayout
from sys import argv


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.lay = QGridLayout(self)
        self.logger = QtLogger(self, log_folder="logs", font=QFont("Consolas", 10))
        self.logger.start()
        self.lay.addWidget(self.logger)

        self.show()

    def closeEvent(self, event):
        self.logger.stop()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(argv)
    window = MainWindow()
    app.exec()
