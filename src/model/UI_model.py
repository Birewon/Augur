import sys
import pandas as pd
from PyQt5.QtCore import QThread
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog


# =====================================================
# === WORKING WITH MODEL UI ===
# =====================================================

class UIModelCallbacks:

    # SETTINGS
    def __init__(self, main_window_instance):
        self.main_window = main_window_instance


    # ---------------------------------------------------------
    # ATTACHING FILES

    def _populate_list_widget(self, list_wiget: QtWidgets.QListWidget, columns: list[str]):
        """
        Supporting function for populate list wiget
        """
        for colum in columns:
            item_csv = QtWidgets.QListWidgetItem(colum)
            item_csv.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item_csv.setCheckState(QtCore.Qt.Unchecked)
            list_wiget.addItem(item_csv)

    def _select_all_checkbox(self):
        list_widget = self.main_window.ui.model_listwidget_factors
        is_check = self.main_window.ui.model_checkbox_select_all.checkState()

        if is_check:
            for index in range(list_widget.count()):
                column = list_widget.item(index)
                column.setCheckState(QtCore.Qt.Checked)
        else:
            for index in range(list_widget.count()):
                column = list_widget.item(index)
                column.setCheckState(QtCore.Qt.Unchecked)

    def browse_new_model(self):

        sys.stdout = self.main_window.stdout_stream_model
        sys.stderr = self.main_window.stderr_stream_model

        dialog = QFileDialog(self.main_window)
        dialog.setNameFilter("*.csv")
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        if dialog.exec_():
            filename = dialog.selectedFiles()
            if filename:
                path = filename[0]
                try:
                    response = self.main_window.add_model_path(True, path)
                    if response:
                        self.main_window.ui.model_plaintext_browse_new_model.setPlainText(path)
                        self.main_window.ui.model_listwidget_factors.clear()
                        self.main_window.ui.model_listwidget_argument.clear()
                        df = pd.read_csv(
                            path,
                            sep=',',
                            header=0,
                            na_values=['', 'N/A']
                        )
                        model_columns = list(df.columns)
                        self._populate_list_widget(self.main_window.ui.model_listwidget_factors, model_columns)
                        self._populate_list_widget(self.main_window.ui.model_listwidget_argument, model_columns)
                except Exception as ex:
                    print(f'[ERROR]: {ex}')
            else:
                print("[INFO]: The file was not attached")

        sys.stdout = self.main_window.stdout_stream
        sys.stderr = self.main_window.stderr_stream

    def select_output_model(self):

        sys.stdout = self.main_window.stdout_stream_model
        sys.stderr = self.main_window.stderr_stream_model

        output_dir = QFileDialog.getExistingDirectory(self.main_window, "Select a Directory")
        if output_dir:
            self.main_window.ui.model_plaintext_output.setPlainText(output_dir)
            self.main_window.set_model_output_path(output_dir)
            print(f'[INFO]: Successfully! The OUTPUT directory ({output_dir}) has been added.')

        sys.stdout = self.main_window.stdout_stream
        sys.stderr = self.main_window.stderr_stream