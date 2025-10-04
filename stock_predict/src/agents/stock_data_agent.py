import yfinance as yf

class StockDataAgent:
    def __init__(self):
        pass

    def fetch_stock_data(self, stock_symbol):
        stock = yf.Ticker(stock_symbol)
        hist = stock.history(period="1y")
        info = stock.info
        return {
            "historical_data": hist,
            "info": info
        }
