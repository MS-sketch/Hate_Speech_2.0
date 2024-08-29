from PyQt6.QtCore import *
import sys
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from mainwin_ui import Ui_MainWindow
import functions


class Worker(QThread):
    result_ready = pyqtSignal(str)
    show_warning = pyqtSignal(str)

    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):
        if functions.hs_detector(self.message):
            final_msg = functions.hs_neuraliser(self.message)
            self.show_warning.emit(final_msg)
        else:
            self.result_ready.emit(self.message)


class MainWindow:
    def __init__(self):
        # Initialize main window with UI file
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        self.ui.SendButton_2.setDisabled(True)
        self.ui.SendButton_2.clicked.connect(self.start_send_message_thread)
        self.ui.MessageInput_2.textChanged.connect(self.msg_integrity_check)

    def msg_integrity_check(self):
        prompt = self.ui.MessageInput_2.text()

        if prompt.strip() != "":
            self.ui.SendButton_2.setEnabled(True)

        else:
            self.ui.SendButton_2.setDisabled(True)

    def start_send_message_thread(self):
        message = self.ui.MessageInput_2.text()
        self.worker = Worker(message)
        self.worker.result_ready.connect(self.update_ui_with_message)
        self.worker.show_warning.connect(self.show_warning_message)
        self.worker.start()

    def update_ui_with_message(self, final_msg):
        self.ui.output_window.addItem("You: \n" + final_msg)
        self.ui.MessageInput_2.setText("")

    def show_warning_message(self, warning_message):
        text_limit = QMessageBox()
        text_limit.setWindowTitle("Wait There!")
        text_limit.setText(warning_message)
        text_limit.setStandardButtons(QMessageBox.StandardButton.Ok)
        text_limit.setIcon(QMessageBox.Icon.Warning)
        text_limit.exec()

    def show(self):
        # Show the main window
        self.main_win.show()


# RUN APP
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
