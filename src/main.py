from PyQt5 import QtWidgets
import sys
import os
import pandas as pd
from CSVeditor.gui import Ui_MainWindow
from UI_logic import UICallbacks

# os.environ["QT_SCALE_FACTOR"] = "2"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
# QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.callbacks = UICallbacks(self)

        self.csv_path_1 = ""
        self.csv_path_2 = ""
        self.csv_output_path = ""
        self.csv_output_name = ""

        self.list_widget_csv_1 = None
        self.list_widget_csv_2 = None

        self.parameter_on = ""
        self.parameter_how = ""
        self.parameter_index = ""

        self.RESPONSE_TEXT = ""

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


def main():
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()