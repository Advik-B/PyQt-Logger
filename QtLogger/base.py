from PyQt6.QtGui import QFont
from qtpy.QtWidgets import QWidget, QTextEdit, QGridLayout
from .exceptions import LoggerNotStartedException
import inspect
import os
import zipfile
from datetime import datetime

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
        if parent:
            super().__init__(parent)
            self.resize(parent.size())
        else:
            super().__init__()

        self.log_folder = log_folder
        self.font = font
        self.custom_colors = custom_colors or LOG_LEVELS  # If custom_colors is None, use the default colors
        self._setup_ui()

        # Enable resizing of the widget
        # self.setFixedSize(self.sizeHint())

    def _setup_ui(self):
        self.lay = QGridLayout(self)
        self.logger_view = QTextEdit(self)
        self.logger_view.setReadOnly(True)
        self.logger_view.setLineWrapMode(QTextEdit.NoWrap)

        # Highlight things like these
        # [DEBUG]-[time]-[module]: message <--- This one is purple
        # [INFO]-[time]-[module]: message <--- This one is blue
        # [WARNING]-[time]-[module]: message <--- This one is yellow
        # [ERROR]-[time]-[module]: message <--- This one is red
        # [SUCCESS]-[time]-[module]: message <--- This one is green
        # Set the font
        self.logger_view.setFont(self.font or QFont("Monospace", 10))
        self.lay.addWidget(self.logger_view, 0, 0, 1, 1)
        # Date
        self.date = datetime.now().strftime("%d-%m-%Y")

        self.started = False

    def prerequisites(self) -> None:
        """
        Check if the log folder exists, if it doesn't, create it, if it does, do nothing
        """
        if not self.log_folder:
            return

        # Check if the log folder exists
        if not os.path.exists(self.log_folder):
            # If it doesn't, create it
            os.mkdir(self.log_folder)

        self.date = datetime.now().strftime("%d-%m-%Y")
        # Check if the log file exists
        if not os.path.exists(f"{self.log_folder}/{date}.log"):
            # If it doesn't, create it
            with open(f"{self.log_folder}/{date}.log", "w") as f:
                f.write(f"Date: {date}\n")

        # Load the previous logs
        self.load_previous_logs()

    def load_previous_logs(self) -> None:



    def start(self) -> None:
        if self.started:
            return

        if not self.log_folder:
            self.started = True
            return

        self.prerequisites()

        self.log_file = open(f"{self.log_folder}/{self.date}.log", "a")
        # Set started to True
        self.started = True

    def load_logs(self) -> None:
        if not self.log_folder:
            return

        with open(f"{self.log_folder}/{self.date}.log", "r") as f:
            for line in f:
                level = line.split("-")[0].replace("[", "").replace("]", "")
                colour = self.custom_colors[level]
                time = line.split("-")[1].replace("[", "").replace("]", "")
                module = line.split("-")[2].replace("(", "").replace(")", "")
                message = line.split(":")[1].strip()
                log_message = f"[{level}]-[{time}]-({module}): {message}"
                self.logger_view.append(f"<font color={colour}>{log_message}</font>")


    def log(self, message: str, level: str = "INFO", module: str = None):
        if not self.started:
            raise LoggerNotStartedException("You need to start the logger before you can log anything!")

        # Get the name of the module that called the log function
        if not module:
            module = inspect.stack()[1].function

        # Get the current time
        time = datetime.now().strftime("%H:%M:%S")
        level = level.upper()
        # If the level is not in the LOG_LEVELS dict, set it to INFO
        if level not in LOG_LEVELS:
            level = "INFO"
        # If the level is in the custom_colors dict, use that color
        colour = self.custom_colors[level]
        # We don't need to check if it's in the dict because we already checked that in the if statement above
        # Create the log message
        log_message = f"[{level}]-[{time}]-({module}): {message}"
        # Add the log message to the logger view with the correct color
        self.logger_view.append(f"<font color={colour}>{log_message}</font>")
        if not self.log_folder:
            return
        # Write the log message to the log file
        self.log_file.write(f"{log_message}\n")

    def debug(self, message: str, module: str = None):
        """Alias for log(message, "DEBUG")"""
        module_name = module or inspect.stack()[1].function
        self.log(message, "DEBUG", module_name)

    def info(self, message: str, m: str = None):
        """Alias for log(message, "INFO")"""
        module_name = m or inspect.stack()[1].function
        self.log(message, "INFO", module_name)

    def warning(self, message: str, m: str = None):
        """Alias for log(message, "WARNING")"""
        module_name = m or inspect.stack()[1].function
        self.log(message, "WARNING", module_name)

    def error(self, message: str, m: str = None):
        """Alias for log(message, "ERROR")"""
        module_name = m or inspect.stack()[1].function
        self.log(message, "ERROR", module_name)

    def success(self, message: str, m: str = None):
        """Alias for log(message, "SUCCESS")"""
        module_name = m or inspect.stack()[1].function
        self.log(message, "SUCCESS", module_name)


    def beforestop(self):
        # Archive any logs that are older than 1 day
        if not self.log_folder:
            return

        # Get all the files in the log folder
        files = os.listdir(self.log_folder)
        # Loop through the files
        for file in files:
            # Get the file's name and extension (only txt files are allowed)
            name, extension = file.split(".")
            # If the extension is not txt, skip the file
            if extension != "txt":
                continue
            # Get the date of the file
            file_date = datetime.strptime(name, "%d-%m-%Y")
            # Get the date of today
            today = datetime.now()
            # Get the difference between the file date and today
            difference = today - file_date
            # If the difference is greater than 1 day, archive the file
            if difference.days > 1:
                # Create a zip file with the file's name
                with zipfile.ZipFile(f"{self.log_folder}/{file}.zip", "w") as zip_file:
                    # Add the file to the zip file
                    zip_file.write(f"{self.log_folder}/{file}")
                    # Delete the file
                    os.remove(f"{self.log_folder}/{file}")

    def clear(self):
        self.logger_view.clear()
        self.stop()
        # Delete all the files in the log folder
        for file in os.listdir(self.log_folder):
            # Find the file's extension
            extension = file.split(".")[-1]
            # If the extension is not txt, skip the file
            if extension != ["txt", "zip"]:
                continue
            # Delete the file
            os.remove(f"{self.log_folder}/{file}")
        self.start()

    def stop(self):
        if not self.started:
            return
        if not self.log_folder:
            self.started = False
            return

        self.log_file.close()
        self.started = False
