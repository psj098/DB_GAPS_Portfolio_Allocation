import pandas as pd

def load_data(file_path, column_names):
    fn_data = pd.read_csv(file_path, skiprows=13)
    fn_data.columns = column_names
    fn_data.iloc[:, 1:] = fn_data.iloc[:, 1:].replace(",", "", regex=True).astype(float)
    fn_data["Date"] = pd.to_datetime(fn_data["Date"])
    fn_data.set_index("Date", inplace=True)
    return fn_data
