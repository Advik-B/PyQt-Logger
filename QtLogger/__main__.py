from qtpy.QtWidgets import QWidget, QTextEdit

class QtLogger(QWidget):
    def __init__(self, parent=None):
        super(QtLogger, self).__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self.logger_view = QTextEdit(self)
        self.logger_view.setReadOnly(True)
        self.logger_view.setLineWrapMode(QTextEdit.NoWrap)
        
