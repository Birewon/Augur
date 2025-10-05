import pandas as pd
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt
from PyQt5 import QtWidgets


# =====================================================
# === ASYNCHRONOUS CONCAT ===
# =====================================================

class ConcatWorker(QObject):

    status_update = pyqtSignal(str)
    finished = pyqtSignal()

    # ---------------------------------------------------------
    # INITIALIZATION

    def __init__(
            self,

            pth_1: str,
            pth_2: str,

            list_widget_csv_1: QtWidgets.QListWidget,
            list_widget_csv_2: QtWidgets.QListWidget,

            output_pth: str,
            output_name: str
        ):
        super().__init__()

        self.pth_1 = pth_1
        self.pth_2 = pth_2

        self.list_widget_csv_1 = list_widget_csv_1
        self.list_widget_csv_2 = list_widget_csv_2

        self.output_pth = output_pth
        self.output_name = output_name

    # ---------------------------------------------------------
    # MAIN

    @pyqtSlot()
    def start_concatenation(self):
        self.status_update.emit('STARTING CONCATENATION')

        try:
            csv_columns_1 = self._extract_columns(self.list_widget_csv_1)
            csv_columns_2 = self._extract_columns(self.list_widget_csv_2)

            self._concat(
                self.pth_1,
                csv_columns_1,

                self.pth_2,
                csv_columns_2,

                self.output_pth,
                self.output_name
            )
            self.status_update.emit('SUCCESSFULY CONCATENATION')
        except Exception as ex:
            self.status_update.emit(f'[ERROR]: {ex}')

        self.finished.emit()

    # ---------------------------------------------------------
    # ADDITIONAL FUNCTIONS

    def _extract_columns(self, list_widget: QtWidgets.QListWidget):
        columns = []
        for index in range(list_widget.count()):
            if list_widget.item(index).checkState() == Qt.Checked:
                columns.append(index)
        return columns

    def _concat(self, path_1: str, csv_columns_1, path_2: str, csv_columns_2, output_path: str, output_name: str):
        csv_output_path = output_path + '/' + output_name
        df1 = pd.read_csv(path_1, usecols=csv_columns_1)
        df2 = pd.read_csv(path_2, usecols=csv_columns_2)

        result = pd.concat([df1, df2], axis=1)
        result.to_csv(csv_output_path, index=False)