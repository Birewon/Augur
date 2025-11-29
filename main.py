from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
import sys
import os
from src.raw.gui import Ui_MainWindow
from src.csv_editor.UI_logic import UICallbacks
from src.model.UI_model import UIModelCallbacks


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
        # CREATING AN INSTANCE OF A UI CLASSES

        self.callbacks = UICallbacks(self)
        self.model_callbacks = UIModelCallbacks(self)

        # --------------------------------
        # MAIN VARIABLES

        self.csv_path_1 = ""
        self.csv_path_2 = ""
        self.csv_output_path = ""

        # self.parameter_on = ""
        # self.parameter_how = ""
        # self.parameter_index = ""

        # --------------------------------
        # MAIN MODEL VARIABLES

        self.new_model_path = ""
        self.output_model_path = ""
        self.predict_model_path = ""

        # --------------------------------
        # REDIRECTING PRINT AND WARNINGS TO status_text

        self.stdout_stream = Output()
        self.stderr_stream = Output()

        self.stdout_stream_model = Output()
        self.stderr_stream_model = Output()

        sys.stdout = self.stdout_stream
        sys.stderr = self.stderr_stream
        self.stdout_stream.newText.connect(self.ui.status_text.appendPlainText)
        self.stderr_stream.newText.connect(self.ui.status_text.appendPlainText)

        self.stdout_stream_model.newText.connect(self.ui.model_status.appendPlainText)
        self.stderr_stream_model.newText.connect(self.ui.model_status.appendPlainText)

        # --------------------------------
        # CONNECTING BUTTONS CSV_EDITOR

        self.ui.attach_btn_1.clicked.connect(self.callbacks.attach_file_1)
        self.ui.attach_btn_2.clicked.connect(self.callbacks.attach_file_2)
        self.ui.attach_btn_3.clicked.connect(self.callbacks.output_pth)
        self.ui.concat_btn.clicked.connect(self.callbacks.concat)
        self.ui.sort_btn.clicked.connect(self.callbacks.sort)
        self.ui.merge_btn.clicked.connect(self.callbacks.merge)

        self.ui.select_all_1.stateChanged.connect(self.callbacks.select_all_checkbox_1)
        self.ui.select_all_2.stateChanged.connect(self.callbacks.select_all_checkbox_2)
        self.ui.clear_button.clicked.connect(self.ui.status_text.clear)

        # --------------------------------
        # CONNECTING BUTTONS MODEL

        self.ui.model_button_browse_new_model.clicked.connect(self.model_callbacks.browse_new_model)
        self.ui.model_checkbox_select_all.clicked.connect(self.model_callbacks._select_all_checkbox)
        self.ui.model_button_output.clicked.connect(self.model_callbacks.select_output_model)
        self.ui.model_clear.clicked.connect(self.ui.model_status.clear)


    # Functions working with globals variables
    def add_path(self, num_of_file: int, new_path: str):
            """
            Adding the path to the file to path variable.
            Validating addition first and second files

            params:

            new_path: str -> New path for addition to path variable
            """
            # if self.csv_path_1 and self.csv_path_2: # Validating of max. files
            #     self.csv_path_1 = ""
            #     self.csv_path_2 = ""
            #     print("[Warning]: There are too many files, please select all files again")
            #     return 0
            #==========Add new path to 1/2 file===========#
            try:
                if num_of_file == 1:
                    self.csv_path_1 = new_path
                    print(f'[INFO]: Successfully! The FIRST file ({new_path}) has been added.')
                    return 1
                elif num_of_file == 2:
                    self.csv_path_2 = new_path
                    print(f'[INFO]: Successfully! The SECOND file ({new_path}) has been added.')
                    return 1
            except Exception as ex:
                 print(f'[ERROR]: {ex}')
                 return 0

    def set_output_path(self, output_path: str):
            """
            Saving output path
            """
            self.csv_output_path = output_path
            return output_path

    def get_concat_params(self):
        params = {
            'pth_1': self.csv_path_1,
            'pth_2': self.csv_path_2,
            'output_pth': self.csv_output_path,
            'output_name': self.ui.name_of_output_file_plain_text_1.toPlainText(),
            'list_widget_csv_1': self.ui.listWidget_1,
            'list_widget_csv_2': self.ui.listWidget_2,
        }
        return params

    def get_sort_params(self):
        ascending = self.ui.how_plain_text_1.toPlainText()

        if ascending.lower() == 'true':
             ascending = True
        elif ascending.lower() == 'false':
             ascending = False
        else:
             ascending = True

        params = {
            'path_to_csv_1': self.csv_path_1,
            'path_to_csv_2': self.csv_path_2,
            'list_widget_columns_1': self.ui.listWidget_1,
            'list_widget_columns_2': self.ui.listWidget_2,
            'how_ascending': ascending,
            'output_path': self.csv_output_path,
            'output_name': self.ui.name_of_output_file_plain_text_1.toPlainText(),
        }
        return params

    def get_merge_params(self):
        index = self.ui.index_plain_text_1.toPlainText()

        if index.lower() == 'false':
            index = False
        else:
            index = True

        params = {
            'pth_1': self.csv_path_1,
            'pth_2': self.csv_path_2,
            'list_widget_csv_1': self.ui.listWidget_1,
            'is_selected_all_1': self.ui.select_all_1.isChecked(),
            'list_widget_csv_2': self.ui.listWidget_2,
            'is_selected_all_2': self.ui.select_all_2.isChecked(),
            'on': self.ui.on_plain_text_1.toPlainText(),
            'how': self.ui.how_plain_text_1.toPlainText(),
            'index': index,
            'output_pth': self.csv_output_path,
            'output_name': self.ui.name_of_output_file_plain_text_1.toPlainText()
        }
        return params


    def add_model_path(self, is_new: bool, new_path: str):
        try:
            if is_new:
                self.new_model_path = new_path
                print(f'[INFO]: Successfuly. The path to model: {new_path}')
                print('[INFO]: Please, select any factors and ONE argument')
                return 1
            else:
                return 1
        except Exception as ex:
            print(f'[ERROR]: {ex}')
            return 0

    def set_model_output_path(self, output_path: str):
            """
            Saving output path
            """
            self.output_model_path = output_path
            return output_path

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