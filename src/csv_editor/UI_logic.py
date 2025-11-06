import pandas as pd
from PyQt5.QtCore import QThread
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog
from .concat import ConcatWorker
from .sort import SortWorker
from .merge import MergeWorker


# =====================================================
# === WORKING WITH UI ===
# =====================================================

class UICallbacks:

    # SETTINGS
    def __init__(self, main_window_instance):
        self.main_window = main_window_instance
        self.concat_thread = None
        self.concat_worker = None
    # ---------------------------------------------------------
    # ATTACHING FILES (WORKING)

    def _populate_list_wiget(self, list_wiget: QtWidgets.QListWidget, columns: list[str]):
        """
        Supporting function for populate list wiget
        """
        for colum in columns:
            item_csv = QtWidgets.QListWidgetItem(colum)
            item_csv.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item_csv.setCheckState(QtCore.Qt.Unchecked)
            list_wiget.addItem(item_csv)

    def attach_file_1(self):
        dialog = QFileDialog(self.main_window)
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        dialog.setNameFilter("*.csv")
        if dialog.exec_():
            fileName = dialog.selectedFiles()
            if fileName:
                new_path = fileName[0] # ["/home/file.csv"]
                try:
                    response = self.main_window.add_path(num_of_file=1, new_path=new_path)
                except Exception as ex:
                    print(f'[ERROR]: {ex}')
                    return
                if response:
                    self.main_window.ui.path_text_1.setPlainText(new_path)
                    self.main_window.ui.listWidget_1.clear()
                    df = pd.read_csv(new_path,
                                    sep=',',
                                    header=0,
                                    na_values=['', 'N/A'])
                    csv_columns = list(df.columns)
                    self._populate_list_wiget(self.main_window.ui.listWidget_1, csv_columns)

    def attach_file_2(self):
        dialog = QFileDialog(self.main_window)
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        dialog.setNameFilter("*.csv")
        if dialog.exec_():
            fileName = dialog.selectedFiles()
            if fileName:
                new_path = fileName[0] # ["/home/file.csv"]
                try:
                    response = self.main_window.add_path(num_of_file=2, new_path=new_path)
                except Exception as ex:
                    print(f'[ERROR]: {ex}')
                    return
                if response:
                    self.main_window.ui.path_text_2.setPlainText(new_path)
                    self.main_window.ui.listWidget_2.clear()
                    df = pd.read_csv(new_path,
                                    sep=',',
                                    header=0,
                                    na_values=['', 'N/A'])
                    csv_columns = list(df.columns)
                    self._populate_list_wiget(self.main_window.ui.listWidget_2, csv_columns)

    # ---------------------------------------------------------
    # SELECTING OUTPUT PATH (WORKING)

    def output_pth(self):
        output_dir = QFileDialog.getExistingDirectory(self.main_window, "Select a Directory")
        if output_dir:
            self.main_window.ui.path_text_3.setPlainText(output_dir)
            self.main_window.set_output_path(output_dir)
            print(f'[INFO]: Successfully! The OUTPUT directory ({output_dir}) has been added.')

    # ---------------------------------------------------------
    # CONCATING (WORKING)

    def concat(self):
        params = self.main_window.get_concat_params()

        self.concat_thread = QThread()

        self.concat_worker = ConcatWorker(**params) # makes an object of ConcatWorker
        self.concat_worker.moveToThread(self.concat_thread) # moves concat_worker (object) into concat_thread (thread)

        self.concat_thread.started.connect(self.concat_worker.start_concatenation) # start concatination
        self.concat_worker.status_update.connect(self.main_window.ui.status_text.appendPlainText) # connects status_update method with status_text field

        self.concat_worker.finished.connect(self.concat_thread.quit) # if the thread finished
        self.concat_worker.finished.connect(self.concat_worker.deleteLater)
        self.concat_thread.finished.connect(self.concat_thread.deleteLater)

        self.concat_thread.start() # start the thread

    # ---------------------------------------------------------
    # SORTING (WORKING)

    def sort(self):
        params = self.main_window.get_sort_params()

        self.sort_thread = QThread()

        self.sort_worker = SortWorker(**params)
        self.sort_worker.moveToThread(self.sort_thread)

        self.sort_thread.started.connect(self.sort_worker.start_sorting)
        self.sort_worker.status_update.connect(self.main_window.ui.status_text.appendPlainText)

        self.sort_worker.finished.connect(self.sort_thread.quit)
        self.sort_worker.finished.connect(self.sort_worker.deleteLater)
        self.sort_thread.finished.connect(self.sort_thread.deleteLater)

        self.sort_thread.start()

    # ---------------------------------------------------------
    # MERGING

    def merge(self):

        params = self.main_window.get_merge_params()

        self.merge_thread = QThread()

        self.merge_worker = MergeWorker(**params)
        self.merge_worker.moveToThread(self.merge_thread)

        self.merge_thread.started.connect(self.merge_worker.start_merge)
        self.merge_worker.status_update.connect(self.main_window.ui.status_text.appendPlainText)

        self.merge_worker.finished.connect(self.merge_thread.quit)
        self.merge_worker.finished.connect(self.merge_worker.deleteLater)
        self.merge_thread.finished.connect(self.merge_thread.deleteLater)

        self.merge_thread.start()
