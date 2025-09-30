from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
import sys
import os
import pandas as pd
from src.CSVeditor.gui import Ui_MainWindow
from src.UI_logic import UICallbacks


# =====================================================
# === APP SETTINGS===
# =====================================================

# os.environ["QT_SCALE_FACTOR"] = "2"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
# QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)


# =====================================================
# === MAIN ===
# =====================================================

# === Redirecting print ===
class Output(QtCore.QObject):
    # 1. Redirecting print
    newText = QtCore.pyqtSignal(str)
    def write(self, text):
         self.newText.emit(str(text))
    # 2. STATIC METHOD! Logging uncaught exceptions
    @staticmethod
    def log_uncaught_exceptions(ex_cls, ex, tb):
        '''
        ex_cls - an instance of a exception_type class
        ex - error text
        tb - error traceback
        '''
        text = f'{ex_cls.__name__}: {ex}:\n'
        import traceback
        text += ''.join(traceback.format_tb(tb))
        print(text) # to status_text
        QMessageBox.critical(None, 'Critical Error', text)
        quit()
sys.excepthook = Output.log_uncaught_exceptions

# === The heart ===
class mywindow(QtWidgets.QMainWindow):
    def __init__(self):

        # DEFAULT
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # --------------------------------
        # CREATING AN INSTANCE OF A UI CLASS

        self.callbacks = UICallbacks(self)

        # --------------------------------
        # MAIN VARIABLES

        self.csv_path_1 = ""
        self.csv_path_2 = ""
        self.csv_output_path = ""
        self.csv_output_name = ""

        self.list_widget_csv_1 = None
        self.list_widget_csv_2 = None

        self.parameter_on = ""
        self.parameter_how = ""
        self.parameter_index = ""

        # --------------------------------
        # REDIRECTING PRINT AND WARNINGS TO status_text

        stdout_stream = Output()
        stderr_stream = Output()
        sys.stdout = stdout_stream
        sys.stderr = stderr_stream
        stdout_stream.newText.connect(self.ui.status_text.appendPlainText)
        stderr_stream.newText.connect(self.ui.status_text.appendPlainText)

        # --------------------------------
        # CONNECTING BUTTONS

        self.ui.attach_btn_1.clicked.connect(self.callbacks.attach_file_1)
        self.ui.attach_btn_2.clicked.connect(self.callbacks.attach_file_2)
        self.ui.attach_btn_3.clicked.connect(self.callbacks.output_pth)
        self.ui.concat_btn.clicked.connect(self.callbacks.concat)
        self.ui.sort_btn.clicked.connect(self.callbacks.sort)
        self.ui.merge_btn.clicked.connect(self.callbacks.merge)

    # Functions working with globals variables
    def add_df(self, num_of_file: int, new_df: pd.DataFrame):
            """
            Adding the path to the file to path_df.
            Validating addition first and second files

            params:

            new_path: str -> New path for addition to path_df
            """
            if self.csv_path_1 and self.csv_path_2: # Validating of max. files
                self.csv_path_1 = ""
                self.csv_path_2 = ""
                return {
                    "msg": "Error! Maximum files",
                    "status": 0
                }
            #==========Add new path to 1/2 file===========#
            if num_of_file == 1:
                self.csv_path_1 = new_df
                return {
                    "msg": f"The first file was selected: {new_df}",
                    "status": 1
                }
            elif num_of_file == 2:
                self.csv_path_2 = new_df
                return {
                    "msg": f"The second file was selected: {new_df}",
                    "status": 1
                }
            else:
                return {
                     "msg": "add_df [ERROR]: Unknown error",
                     "status": 0
                }

    def set_output_path(self, output_path: str):
            """
            Saving output path
            """
            self.csv_output_path = output_path
            return output_path

    def update_response_text(self, response_text: str):
            """
            Adding response text
            """
            self.RESPONSE_TEXT += response_text + "\n"
            return self.RESPONSE_TEXT


## =====================================================
# === DEFAULT ===
# =====================================================

def main():
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()