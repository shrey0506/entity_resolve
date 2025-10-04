import json

class MacroMicroAgent:
    def __init__(self, llm):
        self.llm = llm

    def fetch_macro_data(self):
        prompt = """
        Provide the latest values for the following macroeconomic indicators:
        GDP growth rate, inflation rate, interest rate, and unemployment rate.
        Format the response as JSON with indicator names as keys.
        """
        response = self.llm.query(prompt)
        try:
            macro_data = json.loads(response)
        except json.JSONDecodeError:
            macro_data = {"error": response}
        return macro_data

    def fetch_micro_data(self, stock_symbol):
        prompt = f"""
        Provide the latest microeconomic details for the company with stock symbol {stock_symbol},
        including earnings, revenue growth, and overall industry trend.
        Format the response as JSON with keys: earnings, revenue_growth, industry_trend.
        """
        response = self.llm.query(prompt)
        try:
            micro_data = json.loads(response)
        except json.JSONDecodeError:
            micro_data = {"error": response}
        return micro_data

    def get_grounded_economic_context(self, stock_symbol):
        macro = self.fetch_macro_data()
        micro = self.fetch_micro_data(stock_symbol)
        return {
            "macro": macro,
            "micro": micro,
        }
