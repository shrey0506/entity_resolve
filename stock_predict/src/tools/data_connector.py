import pandas as pd

def load_dnb(path: str = "data/dnb.csv"):
    return pd.read_csv(path)

def load_cmd(path: str = "data/cmd.csv"):
    return pd.read_csv(path)
