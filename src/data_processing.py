import pandas as pd

    # The class working with DataFrames
class DataProcessing:
    """
    This class working with DataFrames
    """
    def read_csv_file(self, file_path: str):
            """
            Reading .csv file.
            Returns DataFrame or None
            """
            try:
                df = pd.read_csv(file_path, sep=',', header=0, na_values=['','N/A'])
                return {
                    "status": 1,
                    "msg": df
                }
            except FileNotFoundError as ex:
                return {
                    "status": 0,
                    "msg": f"[ERROR]: {ex}"
                }
            except Exception as ex:
                return {
                    "status": 0,
                    "msg": f"[ERROR]: {ex}"
                }

    def save_dataframe_to_csv(self, df: pd.DataFrame, output_full_path: str, filename: str | None = "new_csv", index: bool | None = False):
            """
            Saving the DataFrame to .csv file to path
            """
            if df is None:
                return {
                    "status": 0,
                    "msg": "save_dataframe_to_csv [ERROR]: The DataFrame is empty."
                }
            try:
                df.to_csv(output_full_path+"/"+filename+".csv", index=index)
                return {
                    "status": 1,
                    "msg": f"Successfuly saving the new file: {filename}",
                    "filename": filename
                }
            except Exception as ex:
                return {
                    "status": 0,
                    "msg": f"save_dataframe_to_csv [ERROR]: {ex}"
                }

    def concat_files(self, file1_df: pd.DataFrame, file2_df: pd.DataFrame, output_path: str,  filename: str | None = "new_file", axis: int | None = 1, index: bool | None = False):
            """
            Concating two files
            """
            try:
                new_file = pd.concat([file1_df, file2_df], axis=axis)
                raw_name = self.save_dataframe_to_csv(new_file, output_path, filename, index=index)
                return {
                    "status": 1,
                    "msg": raw_name.get("msg")
                }
            except Exception as ex:
                 return {
                    "status": 0,
                    "msg": f"[ERROR]: {ex}"
                 }

    def get_file_columns(self, df: pd.DataFrame) -> list:
            """
            Reading the csv file and return:
            Successfuly: the list of columns names
            Error: Error message
            """
            try:
                # columns = [column for column in df.columns]
                return {
                    "status": 1,
                    "msg": df.columns
                }
            except FileNotFoundError as ex:
                return {
                    "status": 0,
                    "msg": f"get_file_columns [ERROR]: {ex}"
                }

    def sort_df(self, df: pd.DataFrame, by: list[str], how_ascending: bool | None = True):
        try:
            print(by)
            new_df = df.sort_values(by, ascending=how_ascending)
            return {
                 "status": 1,
                 "msg": new_df
            }
        except Exception as ex:
             return{
                  "status": 0,
                  "msg": f"sort_df [ERROR]: {ex}"
             }

    def merge_dfs(self, left_df: pd.DataFrame, right_df: pd.DataFrame, csv_columns_1: list, csv_columns_2: list, merge_how:str, merge_on: str | None):
        try:
            if (len(csv_columns_1) == 0) or (len(csv_columns_2) == 0): # Need to add 'and' instead of 'or'
                return "Select columns"
            # ====Future improvement====
            # elif len(csv_columns_1) == 0:
            #     df1 = pd.read_csv(left_df, usecols=csv_columns_2)
            #     return df1
            # elif len(csv_columns_2) == 0:
            #     df2 = pd.read_csv(right_df, usecols=csv_columns_1)
            #     return df2

            
            # print(left_df)
            # print("===")
            # print(right_df)
            result = pd.merge(left=left_df, right=right_df, how=merge_how, on=merge_on)
        except Exception as ex:
            result = f"merge_dfs [ERROR]: {ex}"
        finally:
            return result