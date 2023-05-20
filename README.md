# PyQt-Logger
A small widget to show some logs with basic syntax
![python_7Z3AFD1Nlw.png](https://i.imgur.com/6h16OaY.png)

## Features

- Show logs with different colors based on their log level
- Customizable log level colors
- Auto archive the logs
- Ability to read and display older logs

## Installation

```bash
pip install PyQt-Logger
```

## Usage

> Importing
```python
from QtLogger import QtLogger
```

> Full usage example
```python
from QtLogger import QtLogger
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QtLogger Example")
        self.resize(500, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.button = QPushButton("Log something")
        self.button.clicked.connect(self.log_something)
        self.layout.addWidget(self.button)

        self.logger = QtLogger()
        self.layout.addWidget(self.logger)

    def log_something(self):
        self.logger.log("This is a log", "info")

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
```