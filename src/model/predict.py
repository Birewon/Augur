# import os
import pandas as pd
import statsmodels.formula.api as smf
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt
from sklearn.model_selection import train_test_split


class Model(QObject):

    formula_signal = pyqtSignal(str)

    status_update = pyqtSignal(str)
    finished = pyqtSignal()

    save_model = pyqtSignal(object)

    def __init__(self, path_to_csv: str, features: list, argument: list, formula: str | bool = False):
        super().__init__()
        self.path = path_to_csv
        self.features = features
        self.argument = argument
        self.formula = formula
        self.df = None # create_df()

        self.model = None # train()

    def create_df(self, path: str, features: list, argument: list) -> pd.DataFrame:
        columns = features + argument
        df = pd.read_csv(path, usecols=columns)
        self.df = df
        return df

    def division_train_test(self, df, target):
        try:
            X = df.drop(target, axis=1)
            Y = df[target[0]]
        except Exception as ex:
            print(f'[ERROR]: {ex}')
            return
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def create_formula(self, formula: str, features: list, argument: list) -> str:
        if not formula:
            cFormula = f'{argument[0]} ~ {'+'.join([column for column in features if column != argument[0] and column != "Unnamed: 0"])}'
            self.formula = cFormula
            return cFormula
        self.formula = formula
        return formula

    @pyqtSlot()
    def train(self):
        try:
            self.create_df(self.path, self.features, self.argument) # CREATE DataFrame
            self.X_train, self.X_test, self.y_train, self.y_test = self.division_train_test(self.df, self.argument) # DIVISION_TRAIN_TEST
            self.create_formula(self.formula, self.features, self.argument) # CREATE Formula
            df_train = pd.concat([self.y_train, self.X_train], axis=1) # MAKE !TRAIN!

            self.model = smf.ols(self.formula, data=df_train).fit()
            self.save_model.emit(self.model)
            self.status_update.emit(self.model.summary().as_text())
            self.formula_signal.emit(self.formula)

            self.finished.emit()
        except Exception as ex:
            self.status_update.emit(f'[ERROR]: {ex}')
            self.finished.emit()



# df = pd.read_csv('/home/birewon/Documents/PyQT-5/test/diabet.csv')
# features = list(df.columns[:-2])
# argument = [list(df.columns)[-1]]
# gener = Model('/home/birewon/Documents/PyQT-5/test/diabet.csv', os.path.join('/home/birewon/me', 'model.joblib'), features, argument)
# gener.train_model()
