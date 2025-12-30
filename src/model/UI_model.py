import sys
import os
import pickle
from datetime import datetime
import pandas as pd
from PyQt5.QtCore import QThread
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog
from .predict import Model


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
                        print(df.info())
                        print('='*100)
                        print(df.describe())
                        print('='*100)
                except Exception as ex:
                    print(f'[ERROR]: {ex}')
            else:
                print("[INFO]: The file was not attached")

        sys.stdout = self.main_window.stdout_stream
        sys.stderr = self.main_window.stderr_stream

    def select_output_model(self): # select output path for trained model --> main: output_model_path
        sys.stdout = self.main_window.stdout_stream_model
        sys.stderr = self.main_window.stderr_stream_model

        output_dir = QFileDialog.getExistingDirectory(self.main_window, "Select a Directory")
        if output_dir:
            self.main_window.ui.model_plaintext_output.setPlainText(output_dir)
            self.main_window.output_model_path = output_dir
            print(f'[INFO]: Successfully! The OUTPUT directory for MODEL ({output_dir}) has been added.')

        sys.stdout = self.main_window.stdout_stream
        sys.stderr = self.main_window.stderr_stream

    def select_load_model(self): # LOAD CSV for prediction --> main: predict_model_path

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
                    response = self.main_window.add_model_path(False, path)
                    if response:
                        self.main_window.ui.model_plaintext_predict_path_csv.setPlainText(path)
                        self.main_window.ui.model_listwidget_factors.clear()
                        self.main_window.ui.model_listwidget_argument.clear()
                        df = pd.read_csv(
                            path,
                            sep=',',
                            header=0,
                            na_values=['', 'N/A']
                        )
                        print(df.info())
                        print('='*100)
                        print(df.describe())
                        print('='*100)
                except Exception as ex:
                    print(f'[ERROR]: {ex}')
            else:
                print("[INFO]: The file was not attached")

        sys.stdout = self.main_window.stdout_stream
        sys.stderr = self.main_window.stderr_stream

    def generate_formula(self):
        sys.stdout = self.main_window.stdout_stream_model
        sys.stderr = self.main_window.stderr_stream_model

        features = []
        features_WD = self.main_window.ui.model_listwidget_factors
        argument = []
        argument_WD = self.main_window.ui.model_listwidget_argument

        try:
            # Parsing QtWidgets:
            for column in range(features_WD.count()):
                item = features_WD.item(column)
                if item.checkState() == QtCore.Qt.CheckState.Checked:
                    features.append(item.text())

            for column in range(argument_WD.count()):
                item = argument_WD.item(column)
                if item.checkState() == QtCore.Qt.CheckState.Checked:
                    argument.append(item.text())
                    break

            formula = f'{argument[0]} ~ {'+'.join([column for column in features if column != argument[0] and column != "Unnamed: 0"])}'
            self.main_window.ui.model_plaintext_formula.setPlainText(formula)

        except Exception as ex:
            print(f'[ERROR]: Please, select factors and an argument. Error: {ex}')

        sys.stdout = self.main_window.stdout_stream
        sys.stderr = self.main_window.stderr_stream

    # ---------------------------------------------------------
    # MODEL

    def create_new_model(self): # TRAIN MAIN

        params = self.main_window.get_model_params()

        self.new_model_thread = QThread()

        self.new_model_worker = Model(**params)
        self.new_model_worker.moveToThread(self.new_model_thread)

        self.new_model_thread.started.connect(self.new_model_worker.train)
        self.new_model_worker.status_update.connect(self.main_window.ui.model_status.appendPlainText)

        self.new_model_worker.formula_signal.connect(self.main_window.ui.model_plaintext_formula.setPlainText) # TAKE FORMULA
        self.new_model_worker.save_model.connect(self.save_model_to_var) # TAKE THE MODEL

        self.new_model_worker.finished.connect(self.new_model_thread.quit)
        self.new_model_worker.finished.connect(self.new_model_worker.deleteLater)
        self.new_model_thread.finished.connect(self.new_model_thread.deleteLater)

        self.new_model_thread.start()

    def save_model_to_var(self, model):
        self.main_window.model = model

    def save_model_to_file(self):
        sys.stdout = self.main_window.stdout_stream_model
        sys.stderr = self.main_window.stderr_stream_model

        model = self.main_window.model
        output_path = self.main_window.output_model_path

        if not output_path:
            output_path = os.path.expanduser('~/Documents')
            self.main_window.ui.model_plaintext_output.setPlainText(os.path.expanduser('~/Documents'))

        from datetime import datetime
        time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"model_{time}.pkl"

        if model:
            try:
                with open(os.path.join(output_path, filename), 'wb') as file:
                    pickle.dump(model, file)
                print(f'[INFO]: The model was saved --> {output_path}')
            except Exception as ex:
                print(f'[ERROR]: {ex}')
        else:
            print('[!!!]: If you want to save the model, you must select an output path.')

        sys.stdout = self.main_window.stdout_stream
        sys.stderr = self.main_window.stderr_stream
        return


    def load_model(self): # LOAD MODEL.pkl
        sys.stdout = self.main_window.stdout_stream_model
        sys.stderr = self.main_window.stderr_stream_model

        dialog = QFileDialog(self.main_window)
        dialog.setNameFilter("*.pkl")
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        if dialog.exec_():
            filename = dialog.selectedFiles()
            if filename:
                path = filename[0]
                try:
                    with open(path, 'rb') as file:
                        self.main_window.model = pickle.load(file)
                    self.main_window.ui.model_plaintext_load.setPlainText(path)
                    print('[+++]: The model was loaded!')
                except Exception as ex:
                    print(f'[ERROR]: {ex}')
            else:
                print("[ATTENTION]: The model was not loaded")

    def predict_loaded_model(self):
        model = self.main_window.model
        if not model:
            sys.stdout = self.main_window.stdout_stream_model
            sys.stderr = self.main_window.stderr_stream_model
            print('[!!!]: MODEL NOT FOUND')
            sys.stdout = self.main_window.stdout_stream_model
            sys.stderr = self.main_window.stderr_stream_model
        else:
            params = self.main_window.get_model_params_for_predict()

            self.predict_thread = QThread()

            self.predict_worker = Model(**params)
            self.predict_worker.moveToThread(self.predict_thread)

            self.predict_thread.started.connect(self.predict_worker.predict)
            self.predict_worker.status_update.connect(self._predict_loaded_model_save_response)

            self.predict_worker.finished.connect(self.predict_thread.quit)
            self.predict_worker.finished.connect(self.predict_worker.deleteLater)
            self.predict_thread.finished.connect(self.predict_thread.deleteLater)

            self.predict_thread.start()

    def _predict_loaded_model_save_response(self, response):
        self.main_window.ui.model_status.appendPlainText(response)
        self.main_window.predict_response = response

    def _select_output(self):
        sys.stdout = self.main_window.stdout_stream_model
        sys.stderr = self.main_window.stderr_stream_model

        output_dir = QFileDialog.getExistingDirectory(self.main_window, "Select a Directory")
        if output_dir:
            self.main_window.ui.model_set_output_predict_text.setPlainText(output_dir)
            self.main_window.predict_response_path = output_dir
            print(f'[INFO]: Successfully! The OUTPUT directory for PREDICTION ({output_dir}) has been added.')

        sys.stdout = self.main_window.stdout_stream
        sys.stderr = self.main_window.stderr_stream

    def set_path_and_filename(self):
        self._select_output()
        self.main_window.predict_response_filename = self.main_window.ui.model_set_filename_predict_text.toPlainText()

    def save_predict_data(self):
        sys.stdout = self.main_window.stdout_stream_model
        sys.stderr = self.main_window.stderr_stream_model

        path = self.main_window.predict_response_path
        filename = self.main_window.ui.model_set_filename_predict_text.toPlainText()
        data = self.main_window.predict_response

        if not path:
            path = os.path.expanduser('~/Documents')
            self.main_window.ui.model_set_output_predict_text.setPlainText(os.path.expanduser('~/Documents'))
        if not filename:
            time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"prediction_{time}.txt"

        try:
            full_name = os.path.expanduser(os.path.join(path, filename))
            with open(full_name, 'w') as file:
                file.write(data)
                print(f"[INFO]: Saved predict: {full_name}")
        except Exception as ex:
            print(f'[ERROR]: {ex}, Press "Predict"')

        sys.stdout = self.main_window.stdout_stream_model
        sys.stderr = self.main_window.stderr_stream_model