from .base import QtLogger
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QApplication, QGridLayout, QLineEdit, QPushButton
from sys import argv


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.lay = QGridLayout(self)
        self.logger = QtLogger(self, log_folder="logs", font=QFont("Consolas", 10))
        self.logger.start()
        self.lay.addWidget(self.logger)

        self.line = QLineEdit(self)
        self.lay.addWidget(self.line, 1, 0)
        self.info_btn = QPushButton("Info", self)
        self.info_btn.clicked.connect(self.info)
        self.lay.addWidget(self.info_btn, 1, 1)
        self.debug_btn = QPushButton("Debug", self)
        self.debug_btn.clicked.connect(self.debug)
        self.lay.addWidget(self.debug_btn, 1, 2)
        self.warning_btn = QPushButton("Warning", self)
        self.warning_btn.clicked.connect(self.warning)
        self.lay.addWidget(self.warning_btn, 1, 3)
        self.error_btn = QPushButton("Error", self)
        self.error_btn.clicked.connect(self.error)
        self.lay.addWidget(self.error_btn, 1, 4)
        self.success_btn = QPushButton("Success", self)
        self.success_btn.clicked.connect(self.success)
        self.lay.addWidget(self.success_btn, 1, 5)

        self.setLayout(self.lay)
        self.resize(800, 600)
        

        self.show()

    def closeEvent(self, event):
        self.logger.stop()
        super().closeEvent(event)

    def info(self):
        self.logger.info(self.line.text())

    def debug(self):
        self.logger.debug(self.line.text())

    def warning(self):
        self.logger.warning(self.line.text())

    def error(self):
        self.logger.error(self.line.text())

    def success(self):
        self.logger.success(self.line.text())




if __name__ == "__main__":
    app = QApplication(argv)
    window = MainWindow()
    app.exec()
