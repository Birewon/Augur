import pandas as pd
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt
import PyQt5.QtWidgets

class MergeWorker(QObject):
    '''
    Merging two DataFrames (by(parameter=on) identical columns)
        how parameter - any value from:

    "inner" (default) - final DataFrame includes ONLY those lines
        that have matches in both DataFrames.

    "left" - final DataFrame includes all lines from first DataFrame and
        the corresponding lines from the second DataFrame. Empty cells = NaN.

    "right" - final DataFrame includes all lines from second DataFrame and
        the corresponding lines from the first DataFrame. Empty cells = NaN.

    "outer" - final DataFrame includes all lines from both DataFrames and
        the Empty cells = NaN.

    on parameter - can take "str" or [list] values. Final DataFrame will be sorted
        by identical name(s) of column(s).

    DON'T WORKING:
    right_on/left_on parametr - merging two DataFrames by two not identical columns
    '''

    status_update = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(
            self,
            pth_1: str,
            pth_2: str,

            list_widget_csv_1: PyQt5.QtWidgets.QListWidget,
            is_selected_all_1: bool,
            list_widget_csv_2: PyQt5.QtWidgets.QListWidget,
            is_selected_all_2: bool,

            on: str | list[str],
            how: str,
            index: bool,

            output_pth: str,
            output_name: str
        ):
        super().__init__()

        self.left = pth_1
        self.right = pth_2

        self.list_widget_1 = list_widget_csv_1
        self.is_selected_all_1 = is_selected_all_1
        self.list_widget_2 = list_widget_csv_2
        self.is_selected_all_2 = is_selected_all_2

        self.on = on
        self.how = how
        self.index = index

        self.output_path = output_pth
        self.output_name = output_name

    def start_merge(self):
        self.status_update.emit('STARTING MERGE')

        try:
            csv_columns_1 = self._extract_columns(self.list_widget_1, self.is_selected_all_1)
            csv_columns_2 = self._extract_columns(self.list_widget_2, self.is_selected_all_2)

            self._merge(
                self.left,
                csv_columns_1,

                self.right,
                csv_columns_2,

                self.on,
                self.how,

                self.index,

                self.output_path,
                self.output_name
            )

            self.status_update.emit('SUCCESSFULY MERGE')
        except Exception as ex:
            self.status_update.emit(f'[ERROR]: {ex}')

        self.finished.emit()

    def _extract_columns(self, list_widget: PyQt5.QtWidgets.QListWidget, is_all: bool):
        columns = []
        if is_all:
            for index in range(list_widget.count()):
                list_widget.item(index).setCheckState(Qt.CheckState.Checked)
                columns.append(index)
        else:
            for index in range(list_widget.count()):
                if list_widget.item(index).checkState() == Qt.Checked:
                    columns.append(index)
        return columns

    def _merge(self, left, csv_columns_1, right, csv_columns_2, on, how, index, output_path, output_name):

        if not left:
            raise ValueError('Please, select the FIRST CSV FILE and try again')
        if not right:
            raise ValueError('Please, set the SECOND CSV FILE and try again')
        if not output_name:
            raise ValueError('Please, set the NAME of the result file and try again')
        if not output_path:
            raise ValueError('Please, set the OUTPUT PATH of the result file and try again')
        if output_name[-4:] != '.csv':
            output_name += '.csv'

        full_outpath = output_path + '/' + output_name
        df1 = pd.read_csv(left, usecols=csv_columns_1)
        df2 = pd.read_csv(right, usecols=csv_columns_2)

        print(df1)
        print('=====================================')
        print(df2)

        if on:
            result = pd.merge(df1, df2, how, on)
            result.to_csv(full_outpath, index=index, na_rep='NaN')
        else:
            result = pd.merge(df1, df2, how)
            result.to_csv(full_outpath, index=index, na_rep='NaN')
