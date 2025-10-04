import pandas as pd

class TechnicalAnalysisAgent:
    def __init__(self):
        pass

    def compute_technical_indicators(self, historical_data):
        df = historical_data.copy()
        df["SMA_20"] = df["Close"].rolling(window=20).mean()
        df["SMA_50"] = df["Close"].rolling(window=50).mean()
        df["RSI"] = self.compute_rsi(df["Close"])
        return df

    def compute_rsi(self, series, period=14):
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
