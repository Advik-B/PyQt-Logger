from qtpy.QtWidgets import QWidget, QTextEdit
import datetime
import inspect

# Hex codes for the colors of the log levels
LOG_LEVELS = {
    "DEBUG": "#ab47bc",
    "INFO": "#0288d1",
    "ERROR": "#d32f2f",
    "WARNING": "#f57c00",
    "SUCCESS": "#388e3c"
}


class QtLogger(QWidget):
    def __init__(self, parent=None, log_folder: str = None, font: QFont = None, custom_colors: dict = None):
        super(QtLogger, self).__init__(parent)
        self.log_folder = log_folder
        self.font = font
        self.custom_colors = custom_colors or LOG_LEVELS  # If custom_colors is None, use the default colors
        self._setup_ui()

    def _setup_ui(self):
        self.logger_view = QTextEdit(self)
        self.logger_view.setReadOnly(True)
        self.logger_view.setLineWrapMode(QTextEdit.NoWarp)

        # Highlight things like these
        # [DEBUG]-[time]-[module]: message <--- This one is purple
        # [INFO]-[time]-[module]: message <--- This one is blue
        # [WARNING]-[time]-[module]: message <--- This one is yellow
        # [ERROR]-[time]-[module]: message <--- This one is red
        # [SUCCESS]-[time]-[module]: message <--- This one is green
        # Set the font
        self.logger_view.setFont(self.font)
        # Date
        self.date = datetime.now().strftime("%d-%m-%Y")
        self.started = False

    def start(self):
        # Create a file with the date as the name
        self.log_file = open(f"{self.log_folder}/{self.date}.log", "a")
        # Write the date to the file
        self.log_file.write(f"Date: {self.date}\n")
        # Set started to True
        self.started = True

    def log(self, message: str, level: str = "INFO"):
        if not self.started:
            raise Exception("You need to start the logger before you can log anything!")

        # Get the module name from the stack and store it in a variable
        module_name = inspect.stack()[1][1].split("\\")[-1].split(".")[0]
        time = datetime.now().strftime("%H:%M:%S")
        # If the level is not in the LOG_LEVELS dict, set it to INFO
        if level not in LOG_LEVELS:
            level = "INFO"
        # If the level is in the custom_colors dict, use that color
        colour = self.custom_colors[level]
        # We don't need to check if it's in the dict because we already checked that in the if statement above
        # Create the log message
        log_message = f"[{level}]-[{time}]-[{module_name}]: {message}"
        # Add the log message to the logger view with the correct color
        self.logger_view.append(f"<font color={colour}>{log_message}</font>")
        # Write the log message to the log file
        self.log_file.write(f"{log_message}\n")
