import pandas as pd
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt
from PyQt5 import QtWidgets


# =====================================================
# === ASYNCHRONOUS SORTING ===
# =====================================================

class SortWorker(QObject):

    status_update = pyqtSignal(str)
    finished = pyqtSignal()

    # ---------------------------------------------------------
    # INITIALIZATION

    def __init__(
            self,

            path_to_csv: str,

            list_widget_columns: QtWidgets.QListWidget,
            how_ascending: bool,

            output_path: str,
            output_name: str
        ):
        super().__init__()

        self.path_to_csv = path_to_csv

        self.list_widget_columns = list_widget_columns
        self.how_ascending = how_ascending

        self.output_path = output_path
        self.output_name = output_name

    # ---------------------------------------------------------
    # MAIN

    @pyqtSlot()
    def start_sorting(self):
        self.status_update.emit('STARTING SORTING')

        try:
            by_columns = self._extract_columns(self.list_widget_columns)
            self._sort(
                path=self.path_to_csv,
                output_path=self.output_path,
                output_name=self.output_name,
                by=by_columns,
                ascending=self.how_ascending
            )
            self.status_update.emit('SUCCESSFULY SORTING')

        except Exception as ex:
            self.status_update.emit(f'[ERROR]: {ex}')

        self.finished.emit()

    # ---------------------------------------------------------
    # ADDITIONAL FUNCTIONS

    def _extract_columns(self, ListWidget: QtWidgets.QListWidget):
        columns = []
        for index in range(ListWidget.count()):
            if ListWidget.item(index).checkState() == Qt.Checked:
                columns.append(index)
        return columns

    def _sort(self, path: str, output_path: str, output_name: str, by: list, ascending: bool):
        df = pd.read_csv(path)
        full_path = output_path + '/' + output_name
        if isinstance(by, list):
            columns = []
            for i in by:
                columns.append(list(df.columns)[i])
            sorted_csv = df.sort_values(columns, ascending=ascending)
        else:
            sorted_csv = pd.read_csv(path)

        sorted_csv.to_csv(full_path, index=False)
