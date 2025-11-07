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

            path_to_csv_1: str | None,
            path_to_csv_2: str | None,

            list_widget_columns_1: QtWidgets.QListWidget | None,
            list_widget_columns_2: QtWidgets.QListWidget | None,
            how_ascending: bool,

            output_path: str,
            output_name: str
        ):
        super().__init__()

        self.path_to_csv_1 = path_to_csv_1
        self.path_to_csv_2 = path_to_csv_2

        self.list_widget_columns_1 = list_widget_columns_1
        self.list_widget_columns_2 = list_widget_columns_2
        self.how_ascending = how_ascending

        self.output_path = output_path
        self.output_name = output_name

    # ---------------------------------------------------------
    # MAIN

    @pyqtSlot()
    def start_sorting(self):
        self.status_update.emit('STARTING SORTING')

        if not self.path_to_csv_1 and not self.path_to_csv_2:
            self.status_update.emit('[ERROR]: You should add any file!')
        else:
            try:
                if self.path_to_csv_1 and self.list_widget_columns_1:
                    by_columns_1 = self._extract_columns(self.list_widget_columns_1)
                if self.path_to_csv_2 and self.list_widget_columns_2:
                    by_columns_2 = self._extract_columns(self.list_widget_columns_2)

                if by_columns_1:
                    self._sort(
                        path=self.path_to_csv_1,
                        output_path=self.output_path,
                        output_name=self.output_name+'_1',
                        by=by_columns_1,
                        ascending=self.how_ascending
                    )
                    self.status_update.emit('FIRST FILE SUCCESSFULY SORTED')
                if by_columns_2:
                    self._sort(
                        path=self.path_to_csv_2,
                        output_path=self.output_path,
                        output_name=self.output_name+'_2',
                        by=by_columns_2,
                        ascending=self.how_ascending
                    )
                    self.status_update.emit('SECOND FILE SUCCESSFULY SORTED')

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

        if not path:
            raise ValueError('Please, select the FIRST CSV FILE and try again')
        if not output_name:
            raise ValueError('Please, set the NAME of the result file and try again')
        if not output_path:
            raise ValueError('Please, set the OUTPUT PATH of the result file and try again')
        if output_name[-4:] != '.csv':
            output_name += '.csv'

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
