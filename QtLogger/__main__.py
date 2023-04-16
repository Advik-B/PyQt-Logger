from qtpy.QtWidgets import QWidget, QTextEdit
import datetime
import inspect

LOG_LEVELS = {
    "DEBUG": "blue",

class QtLogger(QWidget):
    def __init__(self, parent=None, log_folder: str = None, font: QFont = None):
        super(QtLogger, self).__init__(parent)
        self.log_folder = log_folder
        self.font = font

        self._setup_ui()

    def _setup_ui(self):
        self.logger_view = QTextEdit(self)
        self.logger_view.setReadOnly(True)
        self.logger_view.setLineWrapMode(QTextEdit.NoWarp)

        # Highlight things like these
        # [DEBUG]-[time]-[module]: message <--- This one is blue
        # [INFO]-[time]-[module]: message <--- This one is green
        # [WARNING]-[t  ime]-[module]: message <--- This one is yellow
        # [ERROR]-[time]-[module]: message <--- This one is red
        # [CRITICAL]-[time]-[module]: message <--- This one is orange

        # Set the font
        self.logger_view.setFont(self.font)
        # Date
        self.date = datetime.now().strftime("%d-%m-%Y")

    def log(self, message: str, level: str = "INFO"):
        # Get the module name from the stack and store it in a variable
        module_name = inspect.stack()[1][1].split("\\")[-1].split(".")[0]
        time = datetime.now().strftime("%H:%M:%S")