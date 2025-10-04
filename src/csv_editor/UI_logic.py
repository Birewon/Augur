import pandas as pd
from PyQt5.QtCore import QThread, QObject
from PyQt5 import QtWidgets, QtCore, Qt
from PyQt5.QtWidgets import QFileDialog, QListWidget
from src.csv_editor.data_processing import DataProcessing
from .concat import ConcatWorker


# =====================================================
# === WORKING WITH UI ===
# =====================================================

class UICallbacks:

    # SETTINGS
    def __init__(self, main_window_instance):
        self.main_window = main_window_instance
        self.data_processor = DataProcessing()
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

        self.concat_worker = ConcatWorker(**params)
        self.concat_worker.moveToThread(self.concat_thread)

        self.concat_thread.started.connect(self.concat_worker.start_concatenation)
        self.concat_worker.status_update.connect(self.main_window.ui.status_text.appendPlainText)

        self.concat_worker.finished.connect(self.concat_thread.quit)
        self.concat_worker.finished.connect(self.concat_worker.deleteLater)
        self.concat_thread.finished.connect(self.concat_thread.deleteLater)

        self.concat_thread.start()

    # ---------------------------------------------------------
    # SORTING

    def _check_columns_bar(self, list_widget: QtWidgets.QListWidget):
        checked_list = []
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                checked_list.append(item.text())
        return checked_list

    def sort(self):
        df = self.main_window.dfs[0] # take first df
        columns = self._check_columns_bar(self.main_window.ui.listWidget_1) # get columns from df
        output_path = self.main_window.OUTPUT_PATH # get output path
        new_df = DataProcessing.sort_df(self.data_processor, df=df, by=columns, how_ascending=True) # SORT!!!!
        if new_df.get("status") == 1: # if SORT if OK
            status_text = "Successfuly!" # Logging
            self.main_window.update_response_text(status_text) # Logging
            self.print_status_text() # Logging
            message = DataProcessing.save_dataframe_to_csv(self.data_processor, df=new_df.get("msg"), output_full_path=output_path, filename=self.main_window.ui.name_of_output_file_plain_text_1.toPlainText()) # SAVING NEW DF TO CSV !!
            if message.get("status") == 1:
                result_text = f"The file: {message.get("filename")} has sorted and saved in {output_path}" # Logging
                self.main_window.update_response_text(result_text) # Logging
            else:
                self.main_window.update_response_text(message.get("msg"))
            self.print_status_text()
        else: # if SORT isn't OK
            self.main_window.update_response_text(new_df.get("msg"))
            self.print_status_text()

    # ---------------------------------------------------------
    # MERGING

    def merge(self):
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

        def iterate_selected_columns(list_widget: QListWidget) -> list[str]:
            csv_columns = []
            for index in range(list_widget.count()):
                if list_widget.item(index).checkState() == Qt.Checked:

                    print(f'[LOG]: {list_widget.item(index).text()} = 1')

                    csv_columns.append(index)
                else:
                    print(f'[LOG]: {list_widget.item(index).text()} = 0')

            return csv_columns

        try:
            csv_columns_1 = iterate_selected_columns(self.main_window.ui.listWidget_1)
            csv_columns_2 = iterate_selected_columns(self.main_window.ui.listWidget_2)

            print(f'[LOG]: {csv_columns_1} +\n+ {csv_columns_2}')

            df1 = self.main_window.dfs[0]
            df2 = self.main_window.dfs[1]
            output_path = self.main_window.OUTPUT_PATH
            filename = self.main_window.ui.name_of_output_file_plain_text_1.toPlainText()
            how = self.main_window.ui.how_plain_text_1.toPlainText()
            on = self.main_window.ui.on_plain_text_1.toPlainText()
        except Exception as ex:
            self.main_window.update_response_text(f"merge [ERROR]: {ex}\n{df1}\n{df2}\n{output_path}\n{filename}")
            self.print_status_text()
            return
        merge_response = DataProcessing.merge_dfs(self.data_processor, left_df=df1, right_df=df2, csv_columns_1=csv_columns_1, csv_columns_2=csv_columns_2, merge_how=how, merge_on=on)
        if isinstance(merge_response, str):
            self.main_window.update_response_text(merge_response)
        elif isinstance(merge_response, pd.DataFrame):
            save_response = DataProcessing.save_dataframe_to_csv(self.data_processor, df=merge_response, output_full_path=output_path, filename=filename)
            self.main_window.update_response_text(save_response.get('msg'))
        self.print_status_text()
